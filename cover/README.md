# Reel covers

`PLAYBOOK.md` is the cover recipe (Mahindra Arav feed style, built and approved in a separate Claude chat).
The scripts and `cover_template.html` here are extracted from its appendices; run `setup.sh` in a scratch
working folder, never inside this repo.

Extra helpers:
- `pick.py video out.jpg t1 t2 ...` tiles full-res upper-body crops at the given seconds, to choose the presenter frame.
- `clean.py in.png out.png <alpha threshold> [crop]` removes faint cutout leftovers and keeps the largest solid piece.

Notes from the first trial (AM-2611-01, DEM-2611-02):
- Brighter source frames than Reel 5 push the face above the target; fix it with a lower lift in `03_grade.py`
  (below) and re-check `04_face_metrics.py`. Do not use a CSS brightness filter on the presenter.
- For festival greetings, swap "WATCH THIS FIRST!" for the greeting (e.g. "HAPPY DIWALI!").
- `build.py <ID>` builds a cover from a per-reel folder (presenter.png, bg.png, panel_bg.png, graphic.png, optional
  car_final.png and a `cfg.json` with the text, theme `mahindra` or `hyundai`, and cutout fade). It finds the face
  with YuNet (`../models/yunet.onnx`), places and grades the presenter, swaps in the Hyundai blue theme, and
  auto-tunes face brightness to L* 53-60.
- `03_grade.py` takes an optional 5th argument, the mid-tone lift (playbook default 0.30). Bright source frames
  (white showroom light) need a negative lift to land the face in the playbook ranges; CH-2610-12 used -0.2.
  Fix brightness in the grade, never with a CSS brightness filter on the presenter (that made v1 grey and flat).
- Festival reels: same playbook template, headline from the reel's wish, banner "HAPPY DIWALI!".
- Festival headlines with a Hindi wish: Hindi line big, English line small (the user's call, Diwali 2026).
- Never put Claude's draft covers in the team's Thumbnail folder; drafts go to "Claude drafts" (see `CLAUDE.md`).
