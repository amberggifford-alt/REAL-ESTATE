# Floor plan → walkthrough (Layan Verde)

This adapts the "floor plan → walkthrough" reel workflow to Layan Verde. The reel's four steps:

| Step | Reel | Here |
|---|---|---|
| 1. Build the real model | Claude rebuilds the house in Blender from the plan. "Rough is fine"; every wall goes where the plan puts it. | `build_walkthrough.py` builds walls, openings, slabs and furniture blocks from a plan file (`plans/*.json`). |
| 2. Draw one line | One camera line drawn over the plan. Claude flies it at **1.5 m eye height** and **slows down in every room**. | `camera_path` in the plan file. The camera eases into a hold at each labelled room. `plan.svg` shows the line on the plan. |
| 3. Lock each room | Each room becomes a locked still, all using **one materials line** (reel: raw concrete, light pine, white linen, soft daylight) so it "feels like one house". | Clay stills come out in `stills/`. `make_prompts.py` writes one prompt per room using `style.json`. |
| 4. Video model | **Seedance 2.5**: Blender move as the **driving video**, plus a **start frame** and an **end frame**. "The AI doesn't replace the model. It follows it." | One clay driving clip per move in `clips/`. `shots.json` and `prompts.md` pair each clip with its start and end stills. |

## Run it

```bash
pip install bpy            # Blender as a Python module (or use Blender: blender -b -P build_walkthrough.py -- ...)
python build_walkthrough.py plans/2br-illustrative.json --out out/2br --svg-only   # check the camera line first
python build_walkthrough.py plans/2br-illustrative.json --out out/2br              # 16:9 clay walkthrough
python build_walkthrough.py plans/2br-illustrative.json --out out/2br-vertical --res 720x1280   # 9:16 for reels
python make_prompts.py out/2br/shots.json style.json > out/2br/prompts.md
```

Outputs: `plan.svg`, `model.blend`, `driving.mp4`, `stills/`, `clips/`, `shots.json`, `prompts.md`.

## Important: the plan is a placeholder

`plans/2br-illustrative.json` is **not** Layan Verde's official 2BR plan. The official plans couldn't be reached from this environment, so this is a stand-in sized to the published 2BR range (~110 m² plus terrace and plunge pool). It's there so the pipeline can be proven end to end. To make it real:

1. Get the developer's official plan for each unit type you're filming: studio, 1BR, 1BR pool, 2BR, penthouse.
2. Give it to Claude (image or PDF). Claude traces it into a new `plans/<unit>.json`: rooms, walls with door and window openings, furniture positions, and the camera line.
3. Run steps 1–2 again, then 3–4.

The `style.json` palette is also a proposal. Replace it with the developer's finish schedule.

## Steps 3–4: where to run them

Steps 3 and 4 need an image model and a video model; the reel uses Seedance 2.5 for step 4.
- **Not Higgsfield**, as requested.
- The EveryGen and HeyGen connectors in this session need paid plans, and we're not paying.

So run steps 3–4 in the video studio you already use, uploading the files listed in `prompts.md`. Every input is prepared: clay stills, driving clips, and start and end frame pairs.

## Plan file format (short)

- Units are metres. The origin is the top-left of the slab, x runs right and y runs down the plan toward the view side.
- `walls[]`: straight segments `a → b`. Each has `openings[]` with `at` (distance from `a`), `w`, and for windows `sill` and `head`.
- `furniture[]`: boxes `x, y, w, d, h` (with optional `z`), so the video model has scale cues.
- `camera_path.waypoints[]`: `pos` (where the camera stands), `look` (what it looks at), `hold` (true = slow down and pause here), and `label` (the room name used for stills and clips).

## Sample output (placeholder 2BR)

`sample-2br/` holds a full run on the placeholder plan:
- `driving.mp4`: 52 s clay walkthrough
- `stills/`: 8 room holds
- `clips/`: 7 driving clips of 4.7–11 s
- `plan.svg` and `plan.png`
- `shots.json` and `prompts.md`
- `model.blend`: open it in Blender to adjust

This proves the pipeline end to end. Rerun it on the official plans for real content.
