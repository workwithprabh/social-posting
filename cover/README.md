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
