"""Floor plan -> Blender clay model -> eye-height camera walkthrough.

Steps 1 and 2 of the floor-plan-to-walkthrough workflow:
  1. Build the real model from the plan (walls, openings, slabs, furniture blocks).
  2. Fly one camera line over the plan at eye height, easing to a hold in every room.

Outputs (in --out):
  plan.svg               plan with the camera line drawn on it
  driving.mp4            full clay walkthrough (the "Blender move")
  stills/NN_<room>.png   clay frame at each room hold (restyle these into locked stills)
  clips/NN_<a>_to_<b>.mp4  one driving clip per move, hold to hold (feed to the video model)
  shots.json             frame ranges and file names for every still and clip

Run with the Blender Python module (pip install bpy) or Blender itself:
  python build_walkthrough.py plans/2br-illustrative.json --out out/2br
  blender -b -P build_walkthrough.py -- plans/2br-illustrative.json --out out/2br
"""

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys

import bpy
from mathutils import Vector


# ---------------------------------------------------------------- plan model

def box(name, x, y, z, w, d, h, collection):
    """Axis-aligned box from its min corner and size, in metres."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x + w / 2, y + d / 2, z + h / 2))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (w, d, h)
    bpy.ops.object.transform_apply(scale=True)
    for c in obj.users_collection:
        c.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def wall_pieces(wall, thickness, height):
    """Split a straight wall into solid boxes around its openings.

    Returns (along_start, along_len, z, h) pieces in wall-local coordinates.
    """
    (ax, ay), (bx, by) = wall["a"], wall["b"]
    length = math.hypot(bx - ax, by - ay)
    pieces, cursor = [], 0.0
    for op in sorted(wall.get("openings", []), key=lambda o: o["at"]):
        sill = op.get("sill", 0.0)
        head = op.get("head", 2.2 if op["type"] == "door" else 2.4)
        if op["at"] > cursor:
            pieces.append((cursor, op["at"] - cursor, 0.0, height))
        if sill > 0:
            pieces.append((op["at"], op["w"], 0.0, sill))
        if head < height:
            pieces.append((op["at"], op["w"], head, height - head))
        cursor = op["at"] + op["w"]
    if cursor < length:
        pieces.append((cursor, length - cursor, 0.0, height))
    return pieces


def build_model(plan):
    col = bpy.data.collections.new("Model")
    bpy.context.scene.collection.children.link(col)
    t, h = plan["wall_thickness"], plan["ceiling_height"]

    s = plan["slab"]
    box("Floor", s["x"], s["y"], -0.2, s["w"], s["d"], 0.2, col)
    box("Ceiling", s["x"] - t, s["y"] - t, h, s["w"] + 2 * t, s["d"] + 2 * t, 0.25, col)

    if "terrace" in plan:
        tr = plan["terrace"]
        box("Terrace", tr["x"], tr["y"], -0.25, tr["w"], tr["d"], 0.2, col)
        box("Terrace edge", tr["x"], tr["y"] + tr["d"] - 0.1, -0.05, tr["w"], 0.1, 1.0, col)
        box("Terrace canopy", tr["x"], tr["y"], h, tr["w"], tr["d"] * 0.6, 0.25, col)

    if "pool" in plan:
        p = plan["pool"]
        # Pool shown as a recessed water plane with a coping rim.
        box("Pool water", p["x"], p["y"], -0.12, p["w"], p["d"], 0.02, col)
        box("Pool rim", p["x"] - 0.1, p["y"] - 0.1, -0.05, p["w"] + 0.2, 0.1, 0.1, col)

    for i, wall in enumerate(plan["walls"]):
        (ax, ay), (bx, by) = wall["a"], wall["b"]
        horizontal = abs(by - ay) < 1e-6
        for j, (start, length, z, ph) in enumerate(wall_pieces(wall, t, h)):
            name = f"Wall {i}.{j}"
            if horizontal:
                x0 = min(ax, bx) + start
                box(name, x0, ay - t / 2, z, length, t, ph, col)
            else:
                y0 = min(ay, by) + start
                box(name, ax - t / 2, y0, z, t, length, ph, col)

    for f in plan.get("furniture", []):
        box(f["name"], f["x"], f["y"], f.get("z", 0.0), f["w"], f["d"], f["h"], col)

    # Generic context: ground and a ring of low hills so window views are not empty.
    box("Ground", -60, -60, -1.2, 140, 140, 0.2, col)
    for k in range(9):
        ang = math.radians(40 + k * 12)
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=1, location=(6.5 + 70 * math.cos(ang), 10 + 55 * math.sin(ang), -6))
        hill = bpy.context.active_object
        hill.name = f"Hill {k}"
        hill.scale = (18 + 4 * (k % 3), 14, 12 + 3 * (k % 2))
        for c in hill.users_collection:
            c.objects.unlink(hill)
        col.objects.link(hill)


# ---------------------------------------------------------------- camera

def camera_keys(path, fps):
    """Turn waypoints into (frame, pos, look, label, is_hold_start) keys."""
    eye = path["eye_height"]
    speed = path["move_speed_mps"]
    hold = path["hold_seconds"]
    keys, frame, prev = [], 1, None
    for wp in path["waypoints"]:
        pos = Vector((*wp["pos"], eye))
        look = Vector((*wp["look"], eye - 0.1))
        if prev is not None:
            frame += max(1, round(max(1.0, (pos - prev).length / speed) * fps))
        keys.append({"frame": frame, "pos": pos, "look": look, "label": wp["label"], "hold": False})
        if wp["hold"]:
            # Slow drift during the hold: the look target slides 6% sideways.
            side = (look - pos).cross(Vector((0, 0, 1))).normalized() * (look - pos).length * 0.06
            frame += round(hold * fps)
            keys[-1]["hold"] = True
            keys.append({"frame": frame, "pos": pos + (look - pos).normalized() * 0.15,
                         "look": look + side, "label": wp["label"], "hold": False, "hold_end": True})
        prev = keys[-1]["pos"]
    return keys


def build_camera(plan, keys):
    path = plan["camera_path"]
    cam_data = bpy.data.cameras.new("Walkthrough cam")
    cam_data.lens = path["lens_mm"]
    cam_data.clip_start = 0.05
    cam = bpy.data.objects.new("Walkthrough cam", cam_data)
    target = bpy.data.objects.new("Look target", None)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.collection.objects.link(target)
    track = cam.constraints.new("TRACK_TO")
    track.target = target
    track.track_axis = "TRACK_NEGATIVE_Z"
    track.up_axis = "UP_Y"
    for k in keys:
        cam.location = k["pos"]
        cam.keyframe_insert("location", frame=k["frame"])
        target.location = k["look"]
        target.keyframe_insert("location", frame=k["frame"])
    # Blender's default Bezier keys with auto-clamped handles ease the camera
    # into and out of every hold, which gives the "slows down in every room" feel.
    bpy.context.scene.camera = cam
    return cam


# ---------------------------------------------------------------- render

def setup_render(scene, args, last_frame):
    w, h = (int(v) for v in args.res.split("x"))
    scene.render.resolution_x, scene.render.resolution_y = w, h
    scene.render.resolution_percentage = 100
    scene.render.fps = args.fps
    scene.frame_start, scene.frame_end = 1, last_frame
    scene.render.image_settings.file_format = "PNG"
    if args.engine == "workbench":
        scene.render.engine = "BLENDER_WORKBENCH"
        sh = scene.display.shading
        sh.light = "STUDIO"
        sh.color_type = "SINGLE"
        sh.single_color = (0.92, 0.91, 0.89)
        sh.show_cavity = True
        sh.cavity_type = "BOTH"
        sh.show_object_outline = True
        sh.object_outline_color = (0.1, 0.1, 0.1)
        sh.show_shadows = True
        sh.shadow_intensity = 0.35
        scene.display.render_aa = "8"
    else:
        scene.render.engine = "CYCLES"
        scene.cycles.device = "CPU"
        scene.cycles.samples = args.samples
        scene.cycles.use_denoising = True
        world = bpy.data.worlds.new("Sky")
        world.use_nodes = True
        world.node_tree.nodes["Background"].inputs[1].default_value = 1.5
        scene.world = world
        sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
        sun.data.energy = 3.0
        sun.rotation_euler = (math.radians(55), 0, math.radians(200))
        scene.collection.objects.link(sun)


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "move"


def render(args, keys):
    scene = bpy.context.scene
    frames_dir = os.path.join(args.out, "_frames")
    os.makedirs(frames_dir, exist_ok=True)
    scene.render.filepath = os.path.join(frames_dir, "f_")
    bpy.ops.render.render(animation=True)

    ff = shutil.which("ffmpeg")
    if not ff:
        print("ffmpeg not found: PNG frames left in", frames_dir)
        return
    encode = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18"]
    subprocess.run([ff, "-v", "error", "-y", "-framerate", str(args.fps), "-i",
                    os.path.join(frames_dir, "f_%04d.png"), *encode,
                    os.path.join(args.out, "driving.mp4")], check=True)

    holds = [k for k in keys if k["hold"]]
    os.makedirs(os.path.join(args.out, "stills"), exist_ok=True)
    os.makedirs(os.path.join(args.out, "clips"), exist_ok=True)
    shots = {"fps": args.fps, "resolution": args.res, "stills": [], "clips": []}
    for n, k in enumerate(holds, 1):
        mid = k["frame"] + round(args.fps * 0.5)
        name = f"{n:02d}_{slug(k['label'])}.png"
        shutil.copy(os.path.join(frames_dir, f"f_{mid:04d}.png"), os.path.join(args.out, "stills", name))
        shots["stills"].append({"room": k["label"], "frame": mid, "file": f"stills/{name}"})
    for n, (a, b) in enumerate(zip(holds, holds[1:]), 1):
        start, end = a["frame"], b["frame"] + round(args.fps * 0.5)
        name = f"{n:02d}_{slug(a['label'])}_to_{slug(b['label'])}.mp4"
        subprocess.run([ff, "-v", "error", "-y", "-framerate", str(args.fps), "-start_number", str(start),
                        "-i", os.path.join(frames_dir, "f_%04d.png"), "-frames:v", str(end - start + 1),
                        *encode, os.path.join(args.out, "clips", name)], check=True)
        shots["clips"].append({"from": a["label"], "to": b["label"], "frames": [start, end],
                               "seconds": round((end - start + 1) / args.fps, 2),
                               "driving_video": f"clips/{name}",
                               "start_frame": shots["stills"][n - 1]["file"],
                               "end_frame": shots["stills"][n]["file"]})
    with open(os.path.join(args.out, "shots.json"), "w") as fh:
        json.dump(shots, fh, indent=2)
    if not args.keep_frames:
        shutil.rmtree(frames_dir)


# ---------------------------------------------------------------- plan.svg

def write_svg(plan, keys, path):
    px = 60  # pixels per metre
    pad = 1.5
    s = plan["slab"]
    tr = plan.get("terrace", {"y": s["y"], "d": 0})
    max_y = max(s["y"] + s["d"], tr["y"] + tr["d"])
    W, H = (s["w"] + 2 * pad) * px, (max_y - min(s["y"], -1) + 2 * pad) * px
    oy = (-min(s["y"], -1) + pad) * px

    def P(x, y):
        return (x + pad) * px, oy + y * px

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
           f'font-family="Helvetica,Arial,sans-serif" font-size="13">',
           f'<rect width="100%" height="100%" fill="#f4f1ea"/>']
    if "terrace" in plan:
        x, y = P(tr["x"], tr["y"])
        out.append(f'<rect x="{x}" y="{y}" width="{tr["w"]*px}" height="{tr["d"]*px}" fill="#e6e0d3"/>')
    if "pool" in plan:
        p = plan["pool"]
        x, y = P(p["x"], p["y"])
        out.append(f'<rect x="{x}" y="{y}" width="{p["w"]*px}" height="{p["d"]*px}" fill="#bcd9e3" stroke="#6a9fb0"/>')
    for r in plan["rooms"]:
        x, y = P(r["x"] + r["w"] / 2, r["y"] + r["d"] / 2)
        out.append(f'<text x="{x}" y="{y}" text-anchor="middle" fill="#8a8578">{r["name"].upper()}</text>')
    for f in plan.get("furniture", []):
        x, y = P(f["x"], f["y"])
        out.append(f'<rect x="{x}" y="{y}" width="{f["w"]*px}" height="{f["d"]*px}" fill="none" stroke="#b5ae9f"/>')
    t = plan["wall_thickness"] * px
    for wall in plan["walls"]:
        (ax, ay), (bx, by) = wall["a"], wall["b"]
        horizontal = abs(by - ay) < 1e-6
        for start, length, z, ph in wall_pieces(wall, plan["wall_thickness"], plan["ceiling_height"]):
            if z > 0:
                continue
            if horizontal:
                x, y = P(min(ax, bx) + start, ay)
                out.append(f'<rect x="{x}" y="{y - t/2}" width="{length*px}" height="{t}" fill="#222"/>')
            else:
                x, y = P(ax, min(ay, by) + start)
                out.append(f'<rect x="{x - t/2}" y="{y}" width="{t}" height="{length*px}" fill="#222"/>')
        for op in wall.get("openings", []):
            if op["type"] in ("window", "glass"):
                if horizontal:
                    x, y = P(min(ax, bx) + op["at"], ay)
                    out.append(f'<line x1="{x}" y1="{y}" x2="{x + op["w"]*px}" y2="{y}" stroke="#6a9fb0" stroke-width="3"/>')
                else:
                    x, y = P(ax, min(ay, by) + op["at"])
                    out.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + op["w"]*px}" stroke="#6a9fb0" stroke-width="3"/>')
    pts = " ".join("{:.1f},{:.1f}".format(*P(k["pos"].x, k["pos"].y)) for k in keys)
    out.append(f'<polyline points="{pts}" fill="none" stroke="#2f4ab8" stroke-width="4" '
               f'stroke-linejoin="round" stroke-linecap="round"/>')
    for n, k in enumerate([k for k in keys if k["hold"]], 1):
        x, y = P(k["pos"].x, k["pos"].y)
        lx, ly = P(k["look"].x, k["look"].y)
        dx, dy = lx - x, ly - y
        d = math.hypot(dx, dy) or 1
        out.append(f'<line x1="{x}" y1="{y}" x2="{x + dx/d*40}" y2="{y + dy/d*40}" stroke="#2f4ab8" stroke-width="2"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="11" fill="#2f4ab8"/>'
                   f'<text x="{x}" y="{y + 4.5}" text-anchor="middle" fill="#fff" font-size="12">{n}</text>'
                   f'<text x="{x + 15}" y="{y - 10}" fill="#2f4ab8" font-size="12">{k["label"]}</text>')
    out.append(f'<text x="{pad*px}" y="{H - 18}" fill="#555">{plan["name"]} · camera at '
               f'{plan["camera_path"]["eye_height"]} m eye height · numbered dots = room holds</text>')
    out.append("</svg>")
    with open(path, "w") as fh:
        fh.write("\n".join(out))


# ---------------------------------------------------------------- main

def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--res", default="1280x720", help="e.g. 1280x720 (16:9) or 720x1280 (9:16)")
    ap.add_argument("--engine", choices=["workbench", "cycles"], default="workbench")
    ap.add_argument("--samples", type=int, default=16, help="Cycles samples")
    ap.add_argument("--svg-only", action="store_true", help="only write plan.svg (fast check of the camera line)")
    ap.add_argument("--keep-frames", action="store_true")
    args = ap.parse_args(argv)

    with open(args.plan) as fh:
        plan = json.load(fh)
    os.makedirs(args.out, exist_ok=True)

    keys = camera_keys(plan["camera_path"], args.fps)
    write_svg(plan, keys, os.path.join(args.out, "plan.svg"))
    if args.svg_only:
        return

    bpy.ops.wm.read_factory_settings(use_empty=True)
    build_model(plan)
    build_camera(plan, keys)
    setup_render(bpy.context.scene, args, keys[-1]["frame"])
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(os.path.join(args.out, "model.blend")))
    render(args, keys)


if __name__ == "__main__":
    main()
