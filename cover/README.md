# Reel covers

`PLAYBOOK.md` is the cover recipe (Mahindra Arav feed style, built and approved in a separate Claude chat).
The scripts and `cover_template.html` here are extracted from its appendices; run `setup.sh` in a scratch
working folder, never inside this repo.

Extra helpers:
- `pick.py video out.jpg t1 t2 ...` tiles full-res upper-body crops at the given seconds, to choose the presenter frame.
- `clean.py in.png out.png <alpha threshold> [crop]` removes faint cutout leftovers and keeps the largest solid piece.

Notes from the first trial (AM-2611-01, DEM-2611-02):
- Brighter source frames than Reel 5 push the face above the target; tone the presenter with a CSS
  `brightness(.83-.85)` placed before the drop-shadows in `.person{filter:...}` and re-check `04_face_metrics.py`.
- For festival greetings, swap "WATCH THIS FIRST!" for the greeting (e.g. "HAPPY DIWALI!").
- `build.py <ID>` builds a cover from a per-reel folder (presenter.png, bg.png, panel_bg.png, graphic.png, optional
  car_final.png and a `cfg.json` with the text, theme `mahindra` or `hyundai`, and cutout fade). It finds the face
  with YuNet (`../models/yunet.onnx`), places and grades the presenter, swaps in the Hyundai blue theme, and
  auto-tunes face brightness to L* 53-60.
- `03_grade.py` takes an optional 5th argument, the mid-tone lift (playbook default 0.30). Bright source frames
  (white showroom light) need a negative lift to land the face in the playbook ranges; CH-2610-12 used -0.2.
  Fix brightness in the grade, never with a CSS brightness filter on the presenter (that made v1 grey and flat).
- Festival reels: same playbook template, headline from the reel's wish, banner "HAPPY DIWALI!".

## v2 style (the AM-2610-05 look; user, 9 Nov 2026: "the best thumbnail", use these rules from now on; samples pending sign-off)
What makes AM-2610-05 better than the v1 covers, measured on the file:
- Presenter big and bright: face ~26% of the cover width (v1: 19%), face L* ~62 (v1: 48-56), highlights ~85, rosy
  warmth (a* ~18), sharp. Body runs down behind the banner; no gold panel frame around him.
- Glow: a thin bright edge (~2px gold, `#fff2a8`/`#ffcc00`) plus a soft warm halo, not the 5px white sticker outline.
- Background: a real showroom/scene from the reel, lightly blurred (5px) and only slightly dimmed (scene L* ~50, v1
  darkened to ~20); dark only at the very top (headline) and bottom (logo).
- Headline: 2 lines (white topic, big yellow punch) + a neon box holding the main question in big type (white +
  yellow line), not a small curiosity strip. Brand logo at the bottom between two thin lines, not a text footer.
- A small tilted card on the left shows the reel's subject (news clipping, feature shot) without a heavy frame.
Face = the reel's emotion (user, 9 Nov 2026): decide the reel's tone first (happy/reassuring -> confident smile,
emotional -> emotional, shocking -> shocked), then `python3 emo.py <ID> <happiness|surprise|sadness|...>` scores
every 0.2 s with the FER+ model (`models/ferplus.onnx`, from huggingface.co/onnxmodelzoo/emotion-ferplus-8) and
tiles the best matches; choose among them by eye. Prefer close-ups (face 240+ px in the frame): a small face
enlarged 1.6x goes soft and blotchy (AM-2610-07 at 31.7 s). If no frame shows the emotion, say so; don't fake it.
Build: `python3 build_v2.py <ID>` with `<ID>/cfg2.json` (fields in the script); it tunes the face to L* ~62.
Brighten dark frames in the grade (`lift`), not with the CSS brightness, which turns skin orange.

## Faces: expression rules (user, 9 Nov 2026: open mouths, visible teeth and missing glow are "of no use")
A cover face must be a HELD expression, not a frame caught mid-word. In muscle terms (FACS / MediaPipe blendshapes):
- Confident smile: lip corners up (smile 0.4+), mouth closed (jaw < 0.08, no teeth), cheeks lifted, eyes on camera,
  head straight, symmetric. Warm/happy: a fuller smile that reaches the eyes (cheek squint); upper teeth only.
- Shocked: brows high (0.5+), upper lids raised (eyes wide), jaw dropped into a relaxed "O" (lips rounded, no teeth).
- Emotional/sad: inner brows raised and drawn together, lip corners down, mouth closed or pressed, eyes soft.
- Serious/thinking: brows level or one raised, lips pressed, slight head tilt.
- Always: eyes open and on the lens, face 240+ px wide in the frame, soft front light on both sides of the face.
`python3 face_expr.py image.png` prints these signals for any face; `python3 face_expr.py --scan <ID> <target>`
(targets: confident_smile, warm_smile, shocked, emotional, serious) scores every 0.1 s, rewards frames the face holds
for 0.4 s, and tiles the best ones. Needs `pip install mediapipe` and `apt-get install libegl1 libgles2`, plus
`models/face_landmarker.task` from storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/.
Glow: the even, luminous skin of AM-2610-05 (skin spread ~5) comes from soft front light; `build_v2.py` evens skin
gently (`glow` 1), but stronger settings make plastic skin, and side-lit frames can't be rescued.
Talk-to-camera reels rarely contain these faces (9 Nov check: DEH-2610-05 has no closed-mouth smile at all);
ask the team to hold each reel's expression for 3 seconds at the end of the take, in front light.

## AI expression edit (user, 9 Nov 2026: approved as the way forward; first finals DEH-2610-04, DEH-2610-05, AM-2610-07)
When the reel has no held frame with the right emotion, edit the presenter's expression with Canva's image tool:
1. Crop the chosen frame to 1080x1350 around the face; upload it (Canva `create-upload-url`, then POST the raw bytes).
2. `generate-image` with that media as the reference and aspect `PORTRAIT_4_5`. Prompt: keep the exact same person
   (face, identity, hair, clothes, mic, background), change only the expression (e.g. shocked: brows high, eyes wide,
   relaxed round "O", no teeth; confident smile: lips closed, cheeks lifted), looking into the camera, soft even
   front light, bright smooth glowing skin, natural and realistic.
3. The job returns only a 161x200 preview. For the full 1136x1408 file, add a page of that size to a scratch Canva
   design ("Cover export scratch", DAHaZBzI-To), `insert_fill` the media full-page, commit, `export-design` PNG.
4. Use the export as `frame` in `cfg2.json` with `lift` 0, `glow` 0.5, `sharpen` 0.3; set `fade` to end above any
   burnt-in subtitles in the edited image. Check the face with `face_expr.py` (no teeth, target score up).
Notes say "presenter's expression edited with AI" on these rows, so the team knows when they review.

No brand logos on reel thumbnails (user, 9 Nov 2026): leave `logo` out of `cfg2.json`; `build_v2.py` then drops the
logo strip, moves the banner lower and lets the presenter run further down.
Small or distant presenters (face under ~180 px): crop a tight 4:5 box around the face (face ~27% of the crop width)
and upscale it to 1080x1350 before the AI edit; MediaPipe misses faces that far away, so find them with YuNet.
If the edited photo ends in a hard edge through the hair or arm, set `"edge_fade": 140` in cfg2.json. Crop dealer
watermarks and subtitles out of the side card.

No "WATCH THIS FIRST!" banner on reel thumbnails (user, 9 Nov 2026). `build_v2.py` leaves it out unless a
cfg2.json sets `"banner"` explicitly.
`"human_mask": true` in cfg2.json keeps only the person (u2net_human_seg) when the cutout picks up a car door or
window frame (CH-2610-10). Customer testimonials: no AI face edit; hide the presenter (`.pwrap{display:none}`) and
show the real delivery photo as a large card, plates pixelated (MRH-2610-03).

## Hyundai brightness and glow (user, 9 Nov 2026: the Capital Hyundai covers lacked the glow and looked dim)
Dark hair against a dark showroom swallows the blue rim, and showroom light leaves the face warm and grey.
For Hyundai covers add these to cfg2.json (the CH-2610-06 to 11 reworks use them):
- `"strong_rim": true`: a brighter white-blue edge glow (`glow_css` overrides the whole filter if needed).
- `"backlight": 0.6`: a soft blue light behind the head so the hair separates from the background (1 reads as haze).
- `"face_light": 8`: a soft key light on the face that lifts shadows and spares highlights.
- Leave `skin_neutral` out (user, 9 Nov 2026: it made the skin look white). It cut skin chroma from ~36 to ~24;
  keep the warm tone of the earlier covers (skin chroma ~33-37, hue ~53, L ~76-78; check with `skin_tone.py`).
- `"target_L": 66`.
The glow also traces faded alpha, so a body that fades out mid-frame shows a white-blue haze band. Set `pfade`
(cover pixels, `[start, end]`) to end just above that band; to also hide a straight image edge at the side, override
the `.pwrap` mask in `css` with a second horizontal gradient (see CH-2610-09). When the edited photo is cut by a car
door, enlarge and lower the presenter (`face_w` 330, `face_c` [800, 1150], CH-2610-10) so the cut sits low.
Give each reel its own expression: skeptical (ADAS doubt), delighted (easy feature), playful (online vs real), warm
(parents), confident and knowing (checklist), proud (dealer trust). Six covers with the same mild smile look like
one post repeated.

## Skin tone (user, 9 Nov 2026: "the after thumbnails are just looking white"; fix approved on CH-2610-06)
Brightness was not the problem; the skin had lost a third of its colour (chroma 36 to 24) from `skin_neutral`.
Run `python3 skin_tone.py old.jpg new.jpg` against the earlier cover: match its chroma and keep hue near 53-62.
For a pale AI edit, `"skin_ab": [ka, kb]` scales red (a) and yellow (b) on skin pixels. Keep it gentle:
[1.25, 1.05] (CH-2610-08) and [1.3, 1.3] (CH-2610-10) worked; [2.8, 1.6] made the face red and the lips magenta, and
the cheek reading did not show it, so always look at a face crop too.
