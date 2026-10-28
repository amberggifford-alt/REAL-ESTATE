"""Write step 3 (locked still) and step 4 (video) prompts for a rendered walkthrough.

  python make_prompts.py out/2br/shots.json style.json > out/2br/prompts.md
"""

import json
import sys

ROOM_DETAIL = {
    "entry": "entry foyer looking into the open-plan great room",
    "kitchen": "open kitchen with island and full-height cabinetry",
    "dining": "dining area with a six-seat table beside the kitchen",
    "living": "living room facing the terrace glass",
    "terrace-view": "covered terrace with sun loungers and a private plunge pool",
    "master-bedroom": "master bedroom with king bed",
    "master-view": "master bedroom view out through floor-to-ceiling glass",
}


def detail(room):
    key = room.lower().replace(" ", "-")
    return ROOM_DETAIL.get(key, room.lower())


def main():
    shots = json.load(open(sys.argv[1]))
    style = json.load(open(sys.argv[2]))
    look = f"{style['materials']}; {style['light']}; outside: {style['outside']}"
    print(f"# Walkthrough prompts: {style['name']}\n")
    print(f"> {style['note']}\n")
    print("## Step 3: lock each room as a still\n")
    print("Upload the clay still as the image reference (structure/depth guide), then use the prompt. "
          "Keep the same materials line in every room; that's what makes it feel like one home.\n")
    for s in shots["stills"]:
        print(f"### {s['room']}: `{s['file']}`\n")
        print("```\nPhotoreal architectural interior photograph of the "
              f"{detail(s['room'])}. Match the reference image exactly: same walls, openings, "
              f"window positions and furniture layout. Materials: {look}. "
              f"Camera: {style['camera']}. Negative: {style['negative']}.\n```\n")
    print("## Step 4: animate each move\n")
    print("Inputs per clip: **driving video** = the clay clip (camera motion to follow), "
          "**start frame** = the locked still of the first room, **end frame** = the locked still of the next room. "
          "The model doesn't replace the geometry, it follows it.\n")
    print("| # | Move | Length | Driving video | Start frame | End frame |\n|---|---|---|---|---|---|")
    for n, c in enumerate(shots["clips"], 1):
        print(f"| {n} | {c['from']} → {c['to']} | {c['seconds']} s | `{c['driving_video']}` | "
              f"locked `{c['start_frame']}` | locked `{c['end_frame']}` |")
    print("\nPrompt for every clip (only the room names change):\n")
    for n, c in enumerate(shots["clips"], 1):
        print(f"**{n}. {c['from']} → {c['to']}**\n")
        print("```\nSmooth, slow gimbal walkthrough at eye height moving from the "
              f"{detail(c['from'])} to the {detail(c['to'])}. Follow the driving video's camera path "
              "and timing exactly, easing into the final framing. Keep geometry, materials and light "
              f"identical to the start and end frames: {look}. Photoreal, steady, no cuts. "
              f"Negative: {style['negative']}.\n```\n")


if __name__ == "__main__":
    main()
