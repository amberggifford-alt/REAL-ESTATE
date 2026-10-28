# Walkthrough prompts: Layan Verde tropical-modern (PROPOSED palette)

> One locked materials line for every room, so all stills read as one home. Proposed from Layan Verde's resort positioning; swap for the developer's finish schedule once you have the brochure.

## Step 3: lock each room as a still

Upload the clay still as the image reference (structure/depth guide), then use the prompt. Keep the same materials line in every room; that's what makes it feel like one home.

### Entry: `stills/01_entry.png`

```
Photoreal architectural interior photograph of the entry foyer looking into the open-plan great room. Match the reference image exactly: same walls, openings, window positions and furniture layout. Materials: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Camera: eye height 1.5 m, 18 mm lens, level verticals. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

### Kitchen: `stills/02_kitchen.png`

```
Photoreal architectural interior photograph of the open kitchen with island and full-height cabinetry. Match the reference image exactly: same walls, openings, window positions and furniture layout. Materials: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Camera: eye height 1.5 m, 18 mm lens, level verticals. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

### Dining: `stills/03_dining.png`

```
Photoreal architectural interior photograph of the dining area with a six-seat table beside the kitchen. Match the reference image exactly: same walls, openings, window positions and furniture layout. Materials: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Camera: eye height 1.5 m, 18 mm lens, level verticals. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

### Living: `stills/04_living.png`

```
Photoreal architectural interior photograph of the living room facing the terrace glass. Match the reference image exactly: same walls, openings, window positions and furniture layout. Materials: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Camera: eye height 1.5 m, 18 mm lens, level verticals. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

### Terrace view: `stills/05_terrace-view.png`

```
Photoreal architectural interior photograph of the covered terrace with sun loungers and a private plunge pool. Match the reference image exactly: same walls, openings, window positions and furniture layout. Materials: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Camera: eye height 1.5 m, 18 mm lens, level verticals. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

### Great room: `stills/06_great-room.png`

```
Photoreal architectural interior photograph of the great room. Match the reference image exactly: same walls, openings, window positions and furniture layout. Materials: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Camera: eye height 1.5 m, 18 mm lens, level verticals. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

### Master bedroom: `stills/07_master-bedroom.png`

```
Photoreal architectural interior photograph of the master bedroom with king bed. Match the reference image exactly: same walls, openings, window positions and furniture layout. Materials: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Camera: eye height 1.5 m, 18 mm lens, level verticals. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

### Master view: `stills/08_master-view.png`

```
Photoreal architectural interior photograph of the master bedroom view out through floor-to-ceiling glass. Match the reference image exactly: same walls, openings, window positions and furniture layout. Materials: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Camera: eye height 1.5 m, 18 mm lens, level verticals. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

## Step 4: animate each move

Inputs per clip: **driving video** = the clay clip (camera motion to follow), **start frame** = the locked still of the first room, **end frame** = the locked still of the next room. The model doesn't replace the geometry, it follows it.

| # | Move | Length | Driving video | Start frame | End frame |
|---|---|---|---|---|---|
| 1 | Entry → Kitchen | 5.38 s | `clips/01_entry_to_kitchen.mp4` | locked `stills/01_entry.png` | locked `stills/02_kitchen.png` |
| 2 | Kitchen → Dining | 5.25 s | `clips/02_kitchen_to_dining.mp4` | locked `stills/02_kitchen.png` | locked `stills/03_dining.png` |
| 3 | Dining → Living | 7.38 s | `clips/03_dining_to_living.mp4` | locked `stills/03_dining.png` | locked `stills/04_living.png` |
| 4 | Living → Terrace view | 9.58 s | `clips/04_living_to_terrace-view.mp4` | locked `stills/04_living.png` | locked `stills/05_terrace-view.png` |
| 5 | Terrace view → Great room | 8.12 s | `clips/05_terrace-view_to_great-room.mp4` | locked `stills/05_terrace-view.png` | locked `stills/06_great-room.png` |
| 6 | Great room → Master bedroom | 10.96 s | `clips/06_great-room_to_master-bedroom.mp4` | locked `stills/06_great-room.png` | locked `stills/07_master-bedroom.png` |
| 7 | Master bedroom → Master view | 4.67 s | `clips/07_master-bedroom_to_master-view.mp4` | locked `stills/07_master-bedroom.png` | locked `stills/08_master-view.png` |

Prompt for every clip (only the room names change):

**1. Entry → Kitchen**

```
Smooth, slow gimbal walkthrough at eye height moving from the entry foyer looking into the open-plan great room to the open kitchen with island and full-height cabinetry. Follow the driving video's camera path and timing exactly, easing into the final framing. Keep geometry, materials and light identical to the start and end frames: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Photoreal, steady, no cuts. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

**2. Kitchen → Dining**

```
Smooth, slow gimbal walkthrough at eye height moving from the open kitchen with island and full-height cabinetry to the dining area with a six-seat table beside the kitchen. Follow the driving video's camera path and timing exactly, easing into the final framing. Keep geometry, materials and light identical to the start and end frames: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Photoreal, steady, no cuts. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

**3. Dining → Living**

```
Smooth, slow gimbal walkthrough at eye height moving from the dining area with a six-seat table beside the kitchen to the living room facing the terrace glass. Follow the driving video's camera path and timing exactly, easing into the final framing. Keep geometry, materials and light identical to the start and end frames: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Photoreal, steady, no cuts. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

**4. Living → Terrace view**

```
Smooth, slow gimbal walkthrough at eye height moving from the living room facing the terrace glass to the covered terrace with sun loungers and a private plunge pool. Follow the driving video's camera path and timing exactly, easing into the final framing. Keep geometry, materials and light identical to the start and end frames: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Photoreal, steady, no cuts. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

**5. Terrace view → Great room**

```
Smooth, slow gimbal walkthrough at eye height moving from the covered terrace with sun loungers and a private plunge pool to the great room. Follow the driving video's camera path and timing exactly, easing into the final framing. Keep geometry, materials and light identical to the start and end frames: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Photoreal, steady, no cuts. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

**6. Great room → Master bedroom**

```
Smooth, slow gimbal walkthrough at eye height moving from the great room to the master bedroom with king bed. Follow the driving video's camera path and timing exactly, easing into the final framing. Keep geometry, materials and light identical to the start and end frames: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Photoreal, steady, no cuts. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

**7. Master bedroom → Master view**

```
Smooth, slow gimbal walkthrough at eye height moving from the master bedroom with king bed to the master bedroom view out through floor-to-ceiling glass. Follow the driving video's camera path and timing exactly, easing into the final framing. Keep geometry, materials and light identical to the start and end frames: warm honed travertine floors, natural teak joinery, off-white lime-plaster walls, white linen upholstery, woven rattan accents, slim bronze window frames; soft late-afternoon tropical daylight through floor-to-ceiling glass; outside: lush green forested hills and a hazy Andaman Sea horizon beyond the terrace. Photoreal, steady, no cuts. Negative: no people, no text, no logos, no added walls, doors or windows, no changed room proportions, no fisheye distortion, no warping.
```

