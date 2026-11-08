# Reel Cover Playbook — Mahindra Arav / Becarrot style

How the cover for **Arav_Mahindra_Oct_Reel_5** (final = v10) was made, written so another Claude session can repeat it for any reel. Everything here was re-run from scratch in a clean folder, and the output matched v10 **pixel for pixel**.

---

## 0. What the finished cover looks like (top to bottom)

| Zone (1080×1920) | Element |
|---|---|
| y ≈ 140–890 | 3-line headline (Anton, slanted, textured white/yellow, black outline + shadow), dry-brush red strokes peeking out behind, then a dark neon red box with a curiosity line |
| y ≈ 900–1260 | Reel's own explainer graphic on the left (gold glow border, tilted −4°); presenter's head and shoulders on the right, popping out of the frame below |
| y 1260–1700 | Glowing gold frame (showroom inside), a car in front on the left, presenter's body clipped inside the frame |
| y 1600–1740 | "WATCH THIS **FIRST!**" on a red dry-brush swipe |
| bottom 90px | Footer: MAHINDRA **ARAV** • MANESAR • GURGAON (only visible full-screen) |

No logo (removed in v10; it's already the account posting it).

---

## 1. Setup (once per session)

Run inside the working folder that will hold the cover files:

```bash
bash setup.sh
```

- **Fonts**
  - **Anton** (Regular 400), used for all headline, box and banner text. Get it from npm `@fontsource/anton@5.3.0`, file `node_modules/@fontsource/anton/files/anton-latin-400-normal.woff2`. It's also on Google Fonts: https://fonts.google.com/specimen/Anton
  - **Montserrat** ExtraBold 800, used for the footer only. Get it from npm `@fontsource/montserrat@5.3.0`, file `montserrat-latin-800-normal.woff2`. It's also on https://fonts.google.com/specimen/Montserrat
  - Google Fonts' CDN is usually blocked in the sandbox and npm works, so install from npm.
- **Python:** `rembg==2.0.86` + `onnxruntime`, `opencv-python-headless`, `pillow`, `numpy`. The rembg models download from GitHub on first use: `isnet-general-use` is about 180 MB (used for the presenter) and `u2net` is about 176 MB (only needed for the car step).
- **Rendering:** Playwright + Chromium are pre-installed. Don't reinstall them.

---

## 2. Step-by-step workflow

| # | Step | Command |
|---|---|---|
| 1 | Copy the reel into the working folder and make a contact sheet (1 frame/sec, labelled with the second) | `python3 01_frames.py reel.mp4` → look at `sheet.jpg` |
| 2 | Understand the reel: topic, hook, the presenter's lines (burnt-in subtitles), on-screen graphics, end card | read `sheet.jpg`; for the presenter's segments, re-run at `fps=3` |
| 3 | Pick and extract full-res frames (rules in §3) | `ffmpeg -v error -y -ss <sec> -i reel.mp4 -frames:v 1 presenter.png` (same for `bg.png`, `panel_bg.png`, `car_frame.png`, `graphic_frame.png`) |
| 4 | Cut out the presenter, fading off the bottom so subtitles and lap disappear | `python3 02_cutout.py presenter.png person.png 1240 1400` |
| 5 | Grade the presenter (natural studio look) | `python3 03_grade.py person.png person_natural.png [key_x key_y]` |
| 6 | Crop the reel's explainer graphic | e.g. `python3 -c "from PIL import Image; Image.open('graphic_frame.png').crop((120,170,960,780)).save('graphic.png')"` |
| 7 | Car cutout (optional, see §4.4) | `python3 06_car_cut.py car_frame.png car_final.png` (edit the boxes at the top first) |
| 8 | Generate textures (letter scratches + red brush strokes) | `python3 05_textures.py` |
| 9 | Copy `cover_template.html` → `cover.html`, edit the `[PER REEL]` parts (§6–§8) | — |
| 10 | Render | `node render.js $PWD/cover.html $PWD/cover.png` |
| 11 | QA: face lighting numbers, grid crop, and a look at full size | `python3 04_face_metrics.py cover.png x0 y0 x1 y1` · `python3 07_grid_check.py cover.png` |
| 12 | Send the PNG with SendUserFile (one file, 1080×1920) | — |

Frames used for Reel 5: presenter **3.8s**, bg **10.5s**, panel_bg **9.6s**, car **19.5s**, graphic **22.2s** (crop 120,170→960,780).

---

## 3. Picking the frames

**Presenter frame (most important)**
- Use the full-res frame (1080×1920), never the contact-sheet thumbnail.
- Pick an **expression that matches the hook**: a raised eyebrow or skeptical look for a question or dilemma ("Look, sir…" at 3.8s was the best for "apne naam pe ya wife ke?"). Surprise works for a reveal, pointing for "watch this" or a comparison.
- The eyes must be open and looking at the camera, and the mouth should be mid-word but not wide open. Reject blurry frames and frames where a hand covers the face.
- Seated presenters work. The cutout's bottom gets faded out anyway, which removes the burnt-in subtitles and lap.
- If no frame fits the hook, recommend that the client shoot 3–4 phone photos in the same shirt and light: thinking (hand on chin), a palms-up shrug, and pointing. Don't invent a new pose with AI without the presenter's approval.

**Background frame (`bg.png`)**: any showroom frame with cars and lights. It gets blurred and darkened to about 17–21% brightness.

**Frame interior (`panel_bg.png`)**: a showroom frame with cars. It gets lightly blurred.

**Explainer graphic (`graphic.png`)**: the reel's own animated card that sums up the topic (here, Your Profile vs Wife's Profile). Crop it tight to the cards. It ties the cover to the video.

**Car (`car_final.png`)**: a clean front three-quarter shot of the model the reel is about. Prefer a client showroom photo if one exists, since video frames are often partly blocked.

---

## 4. Presenter and background build

### 4.1 Cutout
`02_cutout.py`: rembg `isnet-general-use` on the full-res frame, then the alpha fades linearly from y 1240 to y 1400 and everything below is cropped. Check that the cutout doesn't touch the frame edges (if it does, hide that edge behind the frame or off-canvas).

### 4.2 Grade (`03_grade.py`), the "natural but bright" look
These come from three rounds of feedback (v3 was too harsh, v4 was approved):
1. Light skin smoothing: a bilateral filter blended 45% on skin only.
2. **One exposure for the whole body** (face, neck and shirt together), using a filmic curve: lift the mids, keep hair and eyes dark, roll off the highlights softly, firm black point.
3. Wide, mild local contrast (blur radius 28, amount 0.32). Not gritty.
4. A soft key light from upper left: a Gaussian 330×300 centred just above-left of the face, +0.07 L. Pass `key_x key_y` if the face sits elsewhere in the cutout.
5. Warmth: skin b* +6.5, a* +2.5, whole body b* +2.
6. Warm rim spill on the outer edges (+0.10 L, b* +22, a* +8), so the orange glow looks like it's lighting him.

**Targets** (measured from 6 feed covers; check with `04_face_metrics.py`, L* scale 0–100):

| Metric | Feed avg | v10 result | Accept range |
|---|---|---|---|
| Face brightness | 53.8 | 57.9 | 52–60 |
| Brightest 10% (highlights) | 84.7 | 80.8 | 80–88 (above 92 looks blown) |
| Contrast on face | 23.7 | 18.7 | 18–25 |
| Skin warmth (b*) | 19.7 | 15.5 | 15–20 |
| Face minus surroundings | +19.6 | +16.0 | must be positive, about +9 to +20 |

For the v10 layout, the face skin box for the metric is `575 1050 820 1330`.

### 4.3 Presenter on the canvas
- Scale ×1.2: `width:1296px` for a 1080-wide cutout. Position `left:146px; top:412px`, which puts the face centre at about (700, 1180), on the right side.
- **Glow:** a 5px white outline (drop-shadows) plus `#ffd000` 8px, `rgba(255,160,0,.85)` 20px and `rgba(255,90,0,.55)` 44px.
- **Pop-out:** the wrapper `clip-path` shows everything above y 1260, and below that only inside the frame (x 30–1050, down to y 1700). The head therefore breaks out of the frame's top edge.
- **Keep the area right behind the head dark:** the `.shade` radial `ellipse 34% 15% at 66% 60%` is black at 55%. The face must be brighter than what surrounds it. In v2 the orange glow behind his head made the face look dark.

### 4.4 Car
rembg failed on a dark SUV with a person in front, so `06_car_cut.py`:
1. Blurs the number plate, then mirrors the frame. The car was cut off at the frame's right edge, and mirroring puts that cut off the canvas's left edge.
2. Runs u2net to find the person, dilates that mask, and marks it as definite background.
3. Runs GrabCut with probable and definite car boxes for 8 iterations, then keeps the largest component.
4. Erases the leftover background polygon.

The boxes at the top of the script are frame-specific, so edit them for each reel. On the canvas: `left:-20px; top:1165px; width:710px`, clipped at the frame bottom (y 1700), and `brightness(1.18) contrast(1.1)` plus a warm edge and a drop shadow.

### 4.5 Background layers (back to front)
1. `#0a0a0d` page.
2. `bg.png`: `blur(14px) saturate(.9) brightness(.32)`. Dark areas must land around the feed's #1F1414, 15–25% brightness.
3. `.shade`: a dark spot behind the head, a faint orange glow low in the frame (`rgba(255,110,0,.14)`), and a vertical vignette (72% black at the top, 15–18% in the middle, 92% at the bottom).
4. Gold frame `.panel`: 1020×440 at (30, 1260), radius 34, `0 0 0 7px #ffc400`, glow `rgba(255,170,0,.8)` 30px 8px and `rgba(255,90,0,.38)` 80px 18px. Inside: `panel_bg.png` blurred 6px, brightness .7, plus a warm tint.
5. Halo (soft orange blob behind the shoulders), car, presenter, explainer graphic, headline, banner, footer.

---

## 5. Canvas and safe zones

- **1080 × 1920 PNG** (9:16), rendered at deviceScaleFactor 1.
- **Reels tab / full screen** shows the whole cover.
- **Main profile grid** shows only the centre **3:4 crop, y 240 → 1680**. In v10 the top of "CAR LOAN" (ink top ≈ y 114) is cut in the main grid. The user accepted this to use the space the logo left. If the main grid matters for a reel, set `.head{top:250px}`, which puts the ink top at about y 224.
- Keep the face, the graphic and the red box inside y 240–1680.

---

## 6. Typography

### 6.1 Fonts and sizes (v10 computed values)

| Element | Font | Size | Cap height | Colour |
|---|---|---|---|---|
| Line 1 "CAR LOAN" | Anton 400, uppercase | 242.9px (fitted to 860px wide) | 209px | white gradient |
| Line 2 "APNE NAAM PE?" | Anton 400 | 170.3px (fitted to 1010px) | 147px | white gradient |
| Line 3 "YA WIFE KE?" | Anton 400 | 224.4px (fitted to 1010px) | 193px | yellow gradient |
| Red box text | Anton 400 | 74.1px (fitted so box ≈ 960px wide) | 64px | white + key word yellow |
| WATCH THIS **FIRST!** | Anton 400 | 100px, letter-spacing 2px, skewX −10° | — | white + yellow |
| Footer | Montserrat 800 | 32px, letter-spacing 2px | — | #FFFFFF + #FFD400 |

Anton cap height is 0.86 × font-size. Sizes are fitted automatically by the template's script, so don't hand-set them.

### 6.2 Headline style
- The whole block is `rotate(-4deg) skewX(-9deg)` (forward slant plus upward tilt).
- **Outline and shadow** (the user's spec: "Anton + black shadow/stroke + slight texture/grunge overlay"):
  - Big lines: `-webkit-text-stroke:6px #000`, `text-shadow: 4px 6px 0 #000, 6px 10px 18px rgba(0,0,0,.8)`.
  - Small text (box and banner): stroke 4px, `3px 4px 0 #000, 4px 7px 12px rgba(0,0,0,.75)`.
- **Face fill:** an `::after` copy of the text (`data-t` must equal the visible text) with `background-clip:text`, using the gradient plus `grunge_light.png` speckles. This is because CSS text-shadow shows through transparent text, so the base span carries the stroke and shadow and the `::after` carries the gradient.
- **Spacing** (measured from the feed):
  - Each line is fitted to about 94% of the width (1010px). Line 1 is narrower (860px) only when it's a short phrase that would otherwise get too tall.
  - Gap between lines = **7%** of cap height.
  - Letter spacing **0**.
  - Headline to red box gap = **10%** of line 3's cap + 8px.
  - Red box width about **89%** (960px), vertical padding **30%** and horizontal padding **45%** of its text cap.
  - Each line's box is cropped to its exact cap height in JS (`capCrop`), so the gaps are true visual gaps.

---

## 7. Colours (hex)

| Use | Value |
|---|---|
| White text gradient (top → mid → bottom) | `#FFFFFF` → `#F4F3F3` → `#DCDCDC` (feed sampled #F4F3F3 / #DDDCDC) |
| Yellow text gradient | `#FCF314` → `#FBE206` → `#ECB308` (feed sampled exactly these; avoid orange like #FDCE02) |
| Outline / hard shadow | `#000000` |
| Letter grunge speckles | `#3C3C3C` dots / `#505050` scratches, alpha ≈ 28–84 (70% of the generated values) |
| Red brush strokes | dark `#780000` → bright `#FF0000`, hot core up to `#FF3C28`; feed sampled `#B00506`, `#DB2B2B`, `#7D0202` |
| Red box fill | `#3D0404` → `#160000` → `#2C0202` (almost black-red) |
| Red box neon | border 3px `#FFE3DA` (white-hot core), ring 4px `#FF2410`, glow `rgba(255,36,16,1)` 20px + `rgba(255,20,0,.6)` 60px, inner `rgba(255,40,20,.9)` |
| Red box top flare | radial `#FFFFFF` → `#FFE2C0` → `rgba(255,110,40,.9)` → transparent, 10px tall, 136% of box width |
| Gold frame | `#FFC400` 7px; glows `rgba(255,170,0,.8)`, `rgba(255,90,0,.38)` |
| Explainer graphic border | `#FFD400` 6px + glow `rgba(255,190,0,.8)` |
| Presenter rim | `#FFFFFF` 5px outline, glow `#FFD000` / `rgba(255,160,0,.85)` / `rgba(255,90,0,.55)` |
| Page background | `#0A0A0D`; dark areas should measure about `#1F1414`–`#28160E` |
| Footer | `#FFFFFF` + accent `#FFD400` |
| Red share of the whole cover | feed 2–8%; v10 about 9%. Don't go above 10% |

---

## 8. Wording rules

1. **Hinglish, ALL CAPS**, phrased the way the presenter talks in the reel.
2. **Three headline lines:**
   - Line 1 = topic (2 words, e.g. CAR LOAN).
   - Line 2 = first half of the question (white).
   - Line 3 = the twist or contrast (yellow).
   - Keep each line to about 13 characters or fewer.
   - End on a question mark when the hook is a dilemma.
3. **Red box = a curiosity line taken from the reel itself, not the answer.** "SAHI NAAM = EASY APPROVAL" (v2–v4) gave away the answer. "SIRF **REGISTRATION** SE NAHI HOTA!" is a quote from the reel. Put one key word in yellow. Shorter is better: the feed's boxes are about 12 characters ("LOAN REJECT?", "PRICE + EMI"). Long phrases force smaller text, so for long ones consider a short box plus a small white line under it, like "NOT ALWAYS!".
4. **Bottom banner** is always "WATCH THIS **FIRST!**", with FIRST! in yellow.
5. **Footer:** dealership name + locations. Mahindra Arav = MAHINDRA ARAV • MANESAR • GURGAON. For DM Mahindra content, write **DEE EMM MAHINDRA**, not "DM Mahindra".
6. **No made-up facts:** no statistics, prices or promises that aren't in the reel.

---

## 9. Element positions (v10, px on 1080×1920)

| Element | Position / size | Transform / notes |
|---|---|---|
| `.bg` | inset −40 | blur 14, saturate .9, brightness .32 |
| `.panel` (gold frame) | left 30, top 1260, 1020×440 | radius 34 |
| `.halo` | left 330, top 1180, 760×440 | blur 24 |
| `.car` | left −20, top 1165, width 710 | clipped at 535px (→ y 1700) |
| `.person` | left 146, top 412, width 1296 | clip: above y 1260 full width; below only x 30–1050 to y 1700 |
| `.vs` (graphic) | left 22, top 912, width 440 | rotate −4°, radius 24 |
| `.head` (headline + box) | top 140, full width, centred | rotate −4° skewX −9°, origin centre top; bottom ≈ y 889 |
| `.r1 .stk` brush | left −210, width 640, 96% of line height | `brush_left.png` |
| `.r2 .stk` brush | left −160 → right −60, 112% of line height | `brush_wide.png` |
| `.r3 .stk` brush | right −230, width 640, 90% of line height | `brush_right.png` |
| `.r3 .stk2` underline | left 4% → right −120, 34px below line 3 | `brush_line.png` |
| `.watch` banner | centred, top 1600, 920×140 | rotate −3°; brush inset −14/−70 (`brush_dense` over `brush_wide`) |
| `.foot` | bottom 90, centred | Montserrat 800 32px |

When the headline gets taller or shorter, shift `.vs`, `.person`, `.halo`, `.car`, `.panel` and the clip polygon together (the render prints `headBottom`). Keep the graphic's top about 20px below `headBottom`, and keep the frame top at the presenter's mouth or chin.

---

## 10. QA checklist before sending

- [ ] The face is the brightest thing around it, and `04_face_metrics.py` is inside the ranges in §4.2.
- [ ] The lighting looks natural: no hot spots, the neck and shirt match the face, and the orange glow sits behind the shoulders, not behind the head.
- [ ] `07_grid_check.py`: the headline reads at grid size, and you know what the 3:4 grid crop cuts.
- [ ] Yellow is lemon (#FBE206), not orange; red share of the cover ≤ 10%; the background is dark and neutral.
- [ ] The text in each `data-t` exactly matches the visible text (otherwise the gradient layer misaligns).
- [ ] Everything in the text matches what the reel says. Plates blurred if the image is mirrored. No stray logos.
- [ ] Deliver one PNG, 1080×1920 (no collage).

## 11. Feedback history (what was rejected and why)

| Version | Change | User verdict |
|---|---|---|
| v1 | Basic cover, Montserrat ribbon, CIBIL + VS text cards | Wanted glow + pop-out |
| v2 | Glow + pop-out frame | Presenter too dark (face 41.7 vs feed 53.8; orange glow brighter than the face) |
| v3 | Strong face grade | "Overwhelming, unnatural" (face-only lift, hot spots) |
| v4 | Natural whole-body grade + rim spill | Approved lighting |
| v5 | Bigger tilted 3-line headline, presenter right, car, the reel's own graphic, curiosity box | 8.5/10 |
| v6–v7 | Feed font style, then the exact feed colours (Anton + black stroke/shadow + light grunge) | Good |
| v8 | Feed spacing ratios | "Text spacing looking good" |
| v9 | Dry-brush red strokes + dark neon box (old red bar/box "looked very basic") | "Near perfection" |
| v10 | Logo removed, text pushed up, spacing rebalanced | Final |

---

## Appendix A — `setup.sh`
```bash
#!/usr/bin/env bash
# One-time setup inside the working folder (run from the folder that will hold the cover files)
set -e
npm i -s @fontsource/anton@5.3.0 @fontsource/montserrat@5.3.0
pip install --break-system-packages -q rembg==2.0.86 onnxruntime opencv-python-headless pillow numpy
# Playwright + Chromium are assumed pre-installed (require('playwright') must work). Do NOT reinstall.
```

## Appendix B — `01_frames.py`
```python
"""Contact sheets for choosing frames.
usage: python3 01_frames.py reel.mp4 [fps=1]
writes frames/f_XXX.jpg and sheet.jpg (9 columns, labelled with the second)."""
import sys, subprocess, glob, os
from PIL import Image, ImageDraw
v=sys.argv[1]; fps=float(sys.argv[2]) if len(sys.argv)>2 else 1
os.makedirs('frames',exist_ok=True)
for f in glob.glob('frames/*.jpg'): os.remove(f)
subprocess.run(['ffmpeg','-v','error','-i',v,'-vf',f'fps={fps},scale=270:-1','frames/f_%03d.jpg'],check=True)
fs=sorted(glob.glob('frames/*.jpg')); w,h=Image.open(fs[0]).size; cols=9; rows=(len(fs)+cols-1)//cols
s=Image.new('RGB',(cols*w,rows*(h+16)),(255,255,255)); d=ImageDraw.Draw(s)
for i,f in enumerate(fs):
    x,y=(i%cols)*w,(i//cols)*(h+16); s.paste(Image.open(f),(x,y)); d.text((x+4,y+h+2),f'{(i+0.5)/fps:.1f}s',fill=(0,0,0))
s.save('sheet.jpg',quality=85); print('sheet.jpg',s.size,len(fs),'frames')
```

## Appendix C — `02_cutout.py`
```python
"""Cut the presenter out of a full-res frame and fade off the bottom (removes burnt-in subtitles).
usage: python3 02_cutout.py frame.png person.png [fade_start=1240] [fade_end=1400]
Model: rembg isnet-general-use (downloads ~180MB from GitHub on first run)."""
import sys, numpy as np
from PIL import Image
from rembg import remove, new_session
src,dst=sys.argv[1],sys.argv[2]
y0=int(sys.argv[3]) if len(sys.argv)>3 else 1240; y1=int(sys.argv[4]) if len(sys.argv)>4 else 1400
out=remove(Image.open(src),session=new_session('isnet-general-use'))
a=np.array(out.convert('RGBA')); H=a.shape[0]
fade=np.ones(H); fade[y0:y1]=np.linspace(1,0,y1-y0); fade[y1:]=0
a[...,3]=(a[...,3]*fade[:,None]).astype('uint8')
Image.fromarray(a).crop((0,0,a.shape[1],y1)).save(dst); print('saved',dst)
```

## Appendix D — `03_grade.py`
```python
"""Natural studio-style grade for the presenter cutout (used for v4-v10).
usage: python3 03_grade.py person.png person_natural.png [key_x key_y]
key_x,key_y = centre of the soft key light in cutout pixels (default 430,560 = just
above-left of the face in a 1080-wide cutout). Put it slightly above/left of the face."""
import numpy as np, cv2, sys
from PIL import Image
src,dst=sys.argv[1],sys.argv[2]
KX=float(sys.argv[3]) if len(sys.argv)>3 else 430; KY=float(sys.argv[4]) if len(sys.argv)>4 else 560
im=np.array(Image.open(src).convert('RGBA'))
rgb=im[...,:3]; alpha=im[...,3].astype(np.float32)/255
H,W=alpha.shape
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)

# gentle skin smoothing (keeps texture, removes video grit)
smooth=cv2.bilateralFilter(rgb,9,28,9)
ycc=cv2.cvtColor(rgb,cv2.COLOR_RGB2YCrCb)
skin=((ycc[...,1]>133)&(ycc[...,1]<180)&(ycc[...,2]>77)&(ycc[...,2]<135)).astype(np.float32)
skin=cv2.GaussianBlur(skin,(0,0),5)*alpha
rgb=(rgb*(1-0.45*skin[...,None])+smooth*(0.45*skin[...,None])).astype(np.uint8)

lab=cv2.cvtColor(rgb,cv2.COLOR_RGB2LAB).astype(np.float32)
L=lab[...,0]/255; A=lab[...,1]-128; B=lab[...,2]-128

# 1) one exposure for the whole person (face, neck, shirt together) with a filmic curve
def curve(x, lift=0.30, shoulder=0.82):
    y=x+lift*(x**1.6)*(1-x)*2.6               # lift mids/skin, keep darks (hair, eyes) deep
    y=np.where(y>shoulder, shoulder+(1-shoulder)*np.tanh((y-shoulder)/(1-shoulder)), y)  # soft highlight roll-off
    return y
L=curve(L)
L=np.clip((L-0.035)/0.965,0,1)   # firm black point
# mild, wide local contrast (not gritty)
blur=cv2.GaussianBlur(L,(0,0),28); L=np.clip(L+(L-blur)*0.32,0,1)

# 2) broad soft key light from upper-left (camera-left), like a softbox
cx,cy=KX,KY
key=np.exp(-(((xx-cx)/330)**2+((yy-cy)/300)**2))
L=np.clip(L+0.07*key*(0.4+0.6*skin),0,1)

# 3) natural warmth: even warm skin, slight overall warm balance to match the orange scene
B=B+6.5*skin+2.0*alpha; A=A+2.5*skin+0.5*alpha

# 4) warm rim spill from the glow on the outer edges (strongest on sides/top)
inner=cv2.GaussianBlur((alpha>0.5).astype(np.float32),(0,0),14)
edge=np.clip((1-inner)*2.2,0,1)*(alpha>0.5)
edge=cv2.GaussianBlur(edge,(0,0),3)
L=np.clip(L+0.10*edge,0,1); B=B+22*edge; A=A+8*edge

lab2=np.dstack([L*255,A+128,B+128]).clip(0,255).astype(np.uint8)
out=cv2.cvtColor(lab2,cv2.COLOR_LAB2RGB)
Image.fromarray(np.dstack([out,(alpha*255).astype(np.uint8)]),'RGBA').save(dst)
```

## Appendix E — `04_face_metrics.py`
```python
"""Measure presenter face lighting on a finished cover (or reference screenshot).
usage: python3 04_face_metrics.py cover.png x0 y0 x1 y1   (box = face skin, forehead to chin)
Targets learned from the Mahindra Arav feed (L* scale 0-100):
  face brightness 52-60 | top-10% highlights 80-88 | contrast 20-25 | warmth (b*) 16-20 | face minus surroundings +9..+20"""
import sys, numpy as np, cv2
from PIL import Image
im=np.array(Image.open(sys.argv[1]).convert('RGB')); x0,y0,x1,y1=map(int,sys.argv[2:6])
face=im[y0:y1,x0:x1]; ycc=cv2.cvtColor(face,cv2.COLOR_RGB2YCrCb)
m=(ycc[...,1]>133)&(ycc[...,1]<180)&(ycc[...,2]>77)&(ycc[...,2]<135)
lab=cv2.cvtColor(face,cv2.COLOR_RGB2LAB).astype(float); L=lab[...,0]*100/255; B=lab[...,2]-128
w,h=x1-x0,y1-y0; X0,Y0=max(0,x0-w),max(0,y0-h); X1,Y1=min(im.shape[1],x1+w),min(im.shape[0],y1+h)
R=cv2.cvtColor(im[Y0:Y1,X0:X1],cv2.COLOR_RGB2LAB)[...,0].astype(float)*100/255
rm=np.ones(R.shape,bool); rm[y0-Y0:y1-Y0,x0-X0:x1-X0]=False
print(f"face L {L[m].mean():.1f} | highlights {np.percentile(L[m],90):.1f} | contrast {L[m].std():.1f} | warmth {B[m].mean():.1f} | vs surroundings {L[m].mean()-R[rm].mean():+.1f}")
```

## Appendix F — `05_textures.py`
```python
"""Generate the lettering scratch texture and the dry-brush red strokes.
usage: python3 05_textures.py   -> grunge_light.png, brush_wide.png, brush_left.png, brush_right.png, brush_line.png, brush_dense.png"""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
# scratch / speckle texture for letters (alpha already reduced to 70%)
rng=np.random.default_rng(7); W,H=1000,400
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
for _ in range(2600):
    x,y=rng.integers(0,W),rng.integers(0,H); r=rng.integers(1,3); d.ellipse((x,y,x+r,y+r),fill=(60,60,60,int(rng.integers(40,120))))
for _ in range(160):
    x,y=rng.integers(0,W),rng.integers(0,H); L=rng.integers(15,70); a=rng.uniform(-0.35,0.35)
    d.line((x,y,x+L*np.cos(a),y+L*np.sin(a)),fill=(80,80,80,int(rng.integers(40,100))),width=int(rng.integers(1,3)))
g=np.array(im.filter(ImageFilter.GaussianBlur(0.6))); g[...,3]=(g[...,3]*0.7).astype('uint8'); Image.fromarray(g).save('grunge_light.png')
def stroke(W,H,seed,out,taper_left=True,taper_right=True,density=1.0):
    rng=np.random.default_rng(seed)
    a=np.zeros((H,W),np.float32); tone=np.zeros((H,W),np.float32)
    x=np.arange(W)
    n=int(H*1.6*density)
    for i in range(n):
        y=rng.uniform(0,H); th=rng.uniform(1.0,4.5)
        # envelope: strokes thicker in the middle band
        band=1-abs((y/H)-0.5)*2
        if rng.random()>0.25+0.75*band: continue
        x0=rng.uniform(-0.1,0.35)*W if taper_left else -10; x1=rng.uniform(0.65,1.1)*W if taper_right else W+10
        L=np.clip((x-x0)/max(1,(x1-x0)),0,1)
        env=np.where((x>=x0)&(x<=x1),1.0,0.0)
        # dry brush: break-ups along the bristle
        noise=cv2.GaussianBlur(rng.random(W).astype(np.float32)[None,:],(0,0),sigmaX=rng.uniform(6,30))[0]
        noise=(noise-noise.min())/(np.ptp(noise)+1e-6)
        dry=np.clip((noise-rng.uniform(0.15,0.45))*3,0,1)
        fade=np.clip(L*6,0,1)*np.clip((1-L)*4,0,1)**0.6
        val=env*dry*fade*rng.uniform(0.55,1.0)
        yy=int(y); t=int(max(1,th))
        a[max(0,yy-t//2):yy+t//2+1]=np.maximum(a[max(0,yy-t//2):yy+t//2+1],val)
        tone[max(0,yy-t//2):yy+t//2+1]=np.maximum(tone[max(0,yy-t//2):yy+t//2+1],val*rng.uniform(0.4,1.0))
    # thin speed lines
    for i in range(int(6*density)):
        y=int(rng.uniform(0.05,0.95)*H); x0=int(rng.uniform(0,0.5)*W); x1=int(x0+rng.uniform(0.2,0.6)*W)
        cv2.line(a,(x0,y),(min(W-1,x1),y),float(rng.uniform(.5,.9)),1); cv2.line(tone,(x0,y),(min(W-1,x1),y),1.0,1)
    # ragged, tapered outline for the whole swipe
    rn=lambda: cv2.GaussianBlur(rng.random((H,1)).astype(np.float32),(0,0),sigmaX=0.1,sigmaY=2.5)[:,0]
    lb=(0.02+0.22*rn()+0.10*rng.random(H))*W; rb=(0.98-0.22*rn()-0.10*rng.random(H))*W
    X=x[None,:].astype(np.float32)
    tl=np.clip((X-lb[:,None])/(0.10*W),0,1)**1.4; tr=np.clip((rb[:,None]-X)/(0.10*W),0,1)**1.4
    a=a*tl*tr
    a=cv2.GaussianBlur(a,(0,0),sigmaX=2.2,sigmaY=0.6)
    tone=cv2.GaussianBlur(tone,(0,0),sigmaX=2.0,sigmaY=0.6)
    # colour: dark red -> bright red by tone, with a hot core
    r=np.clip(120+135*tone,0,255); g=np.clip(0+40*np.clip(tone-0.75,0,1)*4,0,60); b=np.clip(0+25*np.clip(tone-0.8,0,1)*5,0,40)
    img=np.dstack([r,g,b,np.clip(a*1.15,0,1)*255]).astype(np.uint8)
    Image.fromarray(img,'RGBA').save(out)
stroke(1300,170,11,'brush_wide.png')
stroke(700,120,23,'brush_left.png',taper_left=True)
stroke(700,120,37,'brush_right.png')
stroke(1100,40,51,'brush_line.png',density=0.6)
stroke(1300,170,77,'brush_dense.png',density=2.6)
print('textures written')
```

## Appendix G — `06_car_cut.py`
```python
"""Cut a car out of a reel frame when rembg fails (dark cars / people in front).
usage: python3 06_car_cut.py frame.png car_final.png  [edit the boxes below per frame]
Steps used for Reel 5: blur number plate -> mirror (so the frame-cut side is off the cover edge)
-> u2net finds the person in front -> GrabCut the car with that person marked as background."""
import sys, numpy as np, cv2
from PIL import Image, ImageFilter, ImageOps, ImageDraw
from rembg import remove, new_session
src,dst=sys.argv[1],sys.argv[2]
PLATE=(860,1025,1010,1080)        # number-plate box in the ORIGINAL frame (blurred so mirrored text never shows)
CROP=(0,690,800,1260)             # region of the MIRRORED frame that holds the car
PROB_FG=(0,40,560,520); DEF_FG=(20,230,380,430)   # in CROP coords: probable car area / sure car core (grille)
CLEAN=[(0,0),(240,0),(214,64),(93,150),(14,229),(0,229)]  # polygon of leftover background to erase
im=Image.open(src).convert('RGB'); im.paste(im.crop(PLATE).filter(ImageFilter.GaussianBlur(9)),PLATE[:2])
im=ImageOps.mirror(im); im.save('car_panel.png')
crop=np.array(im.crop(CROP)); H,W=crop.shape[:2]
man=np.array(remove(Image.fromarray(crop),session=new_session('u2net')))[...,3]>40
man=cv2.dilate(man.astype(np.uint8),np.ones((25,25),np.uint8))>0
mask=np.full((H,W),cv2.GC_PR_BGD,np.uint8)
x0,y0,x1,y1=PROB_FG; mask[y0:y1,x0:x1]=cv2.GC_PR_FGD
x0,y0,x1,y1=DEF_FG; mask[y0:y1,x0:x1]=cv2.GC_FGD
mask[:25,:]=cv2.GC_BGD; mask[man]=cv2.GC_BGD; mask[:,700:]=cv2.GC_BGD; mask[545:,:]=cv2.GC_BGD
bgd=np.zeros((1,65)); fgd=np.zeros((1,65))
cv2.grabCut(cv2.cvtColor(crop,cv2.COLOR_RGB2BGR),mask,None,bgd,fgd,8,cv2.GC_INIT_WITH_MASK)
m=np.where((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD),255,0).astype(np.uint8)
m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((7,7),np.uint8)); m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(m); k=1+np.argmax(st[1:,cv2.CC_STAT_AREA]); m=np.where(lab==k,255,0).astype(np.uint8)
m=cv2.GaussianBlur(m,(0,0),1.5)
cm=Image.new('L',(W,H),255); ImageDraw.Draw(cm).polygon(CLEAN,fill=0); cm=np.array(cm.filter(ImageFilter.GaussianBlur(2)))
a=(m.astype(float)*cm/255).astype(np.uint8)
out=Image.fromarray(np.dstack([crop,a])); out.crop(out.getbbox()).save(dst); print('saved',dst,out.getbbox())
```

## Appendix H — `render.js`
```javascript
// usage: node render.js /abs/path/cover.html /abs/path/out.png
// Renders at 1080x1920 (deviceScaleFactor 1). Prints measured headline data (cap heights, head bottom).
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.argv[2]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(900);
console.log(await p.evaluate(()=>JSON.stringify(document.body.dataset)));
await p.screenshot({path:process.argv[3]});await b.close();})();
```

## Appendix I — `07_grid_check.py`
```python
"""Preview a cover as Instagram shows it: full 9:16 (Reels tab) and centre 3:4 crop (main profile grid, y 240-1680).
usage: python3 07_grid_check.py cover.png [reference_tile.png ...]  -> grid_check.png"""
import sys
from PIL import Image
c=Image.open(sys.argv[1]).convert('RGB'); refs=[Image.open(f).convert('RGB') for f in sys.argv[2:]]
tiles=[c.resize((360,640)),c.crop((0,240,1080,1680)).resize((360,480))]+[r.resize((360,int(r.height*360/r.width))) for r in refs]
H=max(t.height for t in tiles); out=Image.new('RGB',(len(tiles)*370+10,H+20),(255,255,255))
for i,t in enumerate(tiles): out.paste(t,(10+i*370,10))
out.save('grid_check.png'); print('grid_check.png')
```

## Appendix J — `cover_template.html` (v10, exact)

Files it expects next to it: `node_modules/@fontsource/...`, `bg.png`, `panel_bg.png`, `person_natural.png`, `car_final.png`, `graphic.png`, `grunge_light.png`, `brush_left.png`, `brush_wide.png`, `brush_right.png`, `brush_line.png`, `brush_dense.png`. Edit the `[PER REEL]` comments.

```html
<!doctype html>
<html><head><meta charset="utf-8">
<title>Reel Cover</title>
<style>
@font-face{font-family:Anton;src:url(node_modules/@fontsource/anton/files/anton-latin-400-normal.woff2)}
@font-face{font-family:Mont;font-weight:900;src:url(node_modules/@fontsource/montserrat/files/montserrat-latin-900-normal.woff2)}
@font-face{font-family:Mont;font-weight:800;src:url(node_modules/@fontsource/montserrat/files/montserrat-latin-800-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:#0a0a0d;overflow:hidden}
.c{position:relative;width:1080px;height:1920px;overflow:hidden}

/* [PER REEL] bg.png = any showroom frame from the reel (blurred + darkened here) */
.bg{position:absolute;inset:-40px;background:url(bg.png) center 30%/cover;filter:blur(14px) saturate(.9) brightness(.32)}
.shade{position:absolute;inset:0;background:
  radial-gradient(ellipse 34% 15% at 66% 60%, rgba(0,0,0,.55), rgba(0,0,0,0) 80%),
  radial-gradient(ellipse 70% 25% at 50% 80%, rgba(255,110,0,.14), rgba(255,60,0,0) 70%),
  linear-gradient(180deg, rgba(0,0,0,.72) 0%, rgba(0,0,0,.18) 32%, rgba(0,0,0,.15) 62%, rgba(0,0,0,.92) 100%)}

/* glowing gold frame; presenter pops out of its top edge. panel_bg.png = a showroom/cars frame from the reel */
.panel{position:absolute;left:30px;top:1260px;width:1020px;height:440px;border-radius:34px;overflow:hidden;
  box-shadow:0 0 0 7px #ffc400,0 0 30px 8px rgba(255,170,0,.8),0 0 80px 18px rgba(255,90,0,.38)}
.panel .img{position:absolute;inset:-20px;background:url(panel_bg.png) center 34%/1080px auto no-repeat;filter:blur(6px) saturate(1.25) brightness(.7)}
.panel .tint{position:absolute;inset:0;background:
  radial-gradient(ellipse 55% 70% at 30% 30%, rgba(255,140,0,.28), rgba(0,0,0,0) 70%),
  linear-gradient(180deg, rgba(0,0,0,0) 55%, rgba(0,0,0,.6))}
.halo{position:absolute;left:330px;top:1180px;width:760px;height:440px;border-radius:50%;
  background:radial-gradient(ellipse at center, rgba(255,110,0,.24), rgba(255,60,0,.1) 50%, rgba(255,40,0,0) 72%);filter:blur(24px)}
.pwrap{position:absolute;left:0;top:0;width:1080px;height:1920px;
  clip-path:polygon(0 0,1080px 0,1080px 1260px,1050px 1260px,1050px 1700px,30px 1700px,30px 1260px,0 1260px)}
.person{position:absolute;left:146px;top:412px;width:1296px;
  filter:drop-shadow(0 0 0 #fff) drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 -5px 0 #fff)
         drop-shadow(0 0 8px #ffd000) drop-shadow(0 0 20px rgba(255,160,0,.85)) drop-shadow(0 0 44px rgba(255,90,0,.55))}

.car{position:absolute;left:-20px;top:1165px;width:710px;clip-path:inset(0 0 calc(100% - 535px) 0);filter:brightness(1.18) contrast(1.1) saturate(1.1) drop-shadow(0 0 3px rgba(255,220,150,.9)) drop-shadow(0 0 26px rgba(255,140,0,.55)) drop-shadow(0 30px 40px rgba(0,0,0,.8))}
/* [PER REEL] graphic.png = the reel's own on-screen graphic that explains the topic (here: Your Profile vs Wife's Profile) */
.vs{position:absolute;left:22px;top:912px;width:440px;border-radius:24px;overflow:hidden;transform:rotate(-4deg);
  box-shadow:0 0 0 6px #ffd400,0 0 34px 8px rgba(255,190,0,.8),0 20px 40px rgba(0,0,0,.7)}
.vs img{display:block;width:100%}

/* textured 3D lettering, matched to the feed's style */
.tt{position:relative;display:inline-block;white-space:pre;color:#000;-webkit-text-stroke:6px #000;text-shadow:4px 6px 0 #000,6px 10px 18px rgba(0,0,0,.8)}
.tt.s{text-shadow:3px 4px 0 #000,4px 7px 12px rgba(0,0,0,.75);-webkit-text-stroke:4px #000}
.tt::after{content:attr(data-t);position:absolute;left:0;top:0;white-space:pre;-webkit-text-stroke:0;text-shadow:none;color:transparent;
  -webkit-background-clip:text;background-clip:text;background-size:520px auto,100% 100%;background-repeat:repeat,no-repeat}
.tt.w::after{background-image:url(grunge_light.png),linear-gradient(180deg,#ffffff 0%,#f4f3f3 50%,#dcdcdc 100%)}
.tt.y::after{background-image:url(grunge_light.png),linear-gradient(180deg,#fcf314 0%,#fbe206 50%,#ecb308 100%)}

.head{position:absolute;left:0;right:0;top:140px;transform:rotate(-4deg) skewX(-9deg);transform-origin:center top;isolation:isolate}
.row{position:relative;width:max-content;margin:0 auto}
.ln{display:block;position:relative;font-family:Anton;text-transform:uppercase;letter-spacing:0;white-space:pre}
.stk{position:absolute;z-index:-1;background-repeat:no-repeat;background-size:100% 100%;filter:drop-shadow(0 0 14px rgba(255,0,0,.45))}
.r1 .stk{left:-210px;width:640px;top:2%;height:96%;background-image:url(brush_left.png)}
.r2 .stk{left:-160px;right:-60px;top:-6%;height:112%;background-image:url(brush_wide.png)}
.r3 .stk{right:-230px;width:640px;top:8%;height:90%;background-image:url(brush_right.png)}
.r3 .stk2{position:absolute;z-index:-1;left:4%;right:-120px;bottom:-34px;height:34px;background:url(brush_line.png) 0 0/100% 100% no-repeat}
.boxrow{position:relative;width:max-content;margin:0 auto}
.redbox{position:relative;white-space:nowrap;font-family:Anton;letter-spacing:0;border-radius:10px;
  background:linear-gradient(180deg,#3d0404 0%,#160000 50%,#2c0202 100%);border:3px solid #ffe3da;
  box-shadow:0 0 0 4px #ff2410,0 0 20px 5px rgba(255,36,16,1),0 0 60px 12px rgba(255,20,0,.6),
             inset 0 0 0 2px rgba(255,40,20,.9),inset 0 0 22px rgba(255,40,20,.55),inset 0 -30px 50px rgba(0,0,0,.6),0 14px 0 rgba(0,0,0,.45)}
.redbox::before{content:'';position:absolute;left:-18%;right:-18%;top:-7px;height:10px;border-radius:50%;
  background:radial-gradient(ellipse at 55% 50%,#fff 0%,#ffe2c0 14%,rgba(255,110,40,.9) 36%,rgba(255,40,0,.35) 60%,rgba(255,0,0,0) 75%);filter:blur(.6px)}
.redbox::after{content:'';position:absolute;left:8%;right:30%;bottom:-4px;height:5px;border-radius:50%;
  background:radial-gradient(ellipse at 30% 50%,#ffe8d8 0%,rgba(255,90,30,.85) 30%,rgba(255,0,0,0) 72%);filter:blur(.6px)}
.redbox .in{display:block;position:relative;white-space:pre}

.watch{position:absolute;left:50%;top:1600px;transform:translateX(-50%) rotate(-3deg);width:920px;height:140px}
.watch .brush{position:absolute;inset:-14px -70px;background:url(brush_dense.png) 0 0/100% 100% no-repeat,url(brush_wide.png) 0 0/100% 100% no-repeat;
  filter:drop-shadow(0 0 20px rgba(255,0,0,.9))}
.watch b{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:Anton;font-size:100px;letter-spacing:2px;transform:skewX(-10deg)}
.watch b .tt+.tt{margin-left:20px}
.foot{position:absolute;left:0;right:0;bottom:90px;text-align:center;font-family:Mont;font-weight:800;font-size:32px;color:#fff;letter-spacing:2px;opacity:.95}
.foot span{color:#ffd400}
</style></head>
<body><div class="c">
  <div class="bg"></div>
  <div class="shade"></div>

  <div class="panel"><div class="img"></div><div class="tint"></div></div>
  <div class="halo"></div>
  <img class="car" src="car_final.png">
  <div class="pwrap"><img class="person" src="person_natural.png"></div>

  <div class="vs"><img src="graphic.png"></div>

  <div class="head">
    <!-- [PER REEL] headline: 3 lines. data-t MUST equal the visible text. Line 1 data-w=860, others auto-fit to 1010px -->
    <div class="row r1"><i class="stk"></i><span class="ln tt w" data-w="860" data-t="CAR LOAN">CAR LOAN</span></div>
    <div class="row r2"><i class="stk"></i><span class="ln tt w" data-t="APNE NAAM PE?">APNE NAAM PE?</span></div>
    <div class="row r3"><i class="stk"></i><i class="stk2"></i><span class="ln tt y" data-t="YA WIFE KE?">YA WIFE KE?</span></div>
    <!-- [PER REEL] red box: curiosity line; wrap the key word in .y (yellow), rest .w (white) -->
    <div class="boxrow"><div class="redbox"><span class="in"><span class="tt s w" data-t="SIRF ">SIRF </span><span class="tt s y" data-t="REGISTRATION">REGISTRATION</span><span class="tt s w" data-t=" SE NAHI HOTA!"> SE NAHI HOTA!</span></span></div></div>
  </div>

  <div class="watch"><div class="brush"></div><b><span class="tt s w" data-t="WATCH THIS">WATCH THIS</span><span class="tt s y" data-t="FIRST!">FIRST!</span></b></div>
  <!-- [PER REEL] footer only shows in full-screen view -->
  <div class="foot">MAHINDRA <span>ARAV</span> &nbsp;&bull;&nbsp; MANESAR &nbsp;&bull;&nbsp; GURGAON</div>
</div>
<script>
// Spacing ratios measured from the Mahindra Arav feed covers:
const LINE_W=1010;      // each headline line fitted to ~94% of the cover width
const LINE_GAP=0.07;    // gap between lines = 7% of cap height (lines almost touch)
const BOX_GAP=0.10;     // headline -> red box gap = 10% of cap height
const BOX_W=960;        // red box spans ~89% of the width
const BOX_PADV=0.30, BOX_PADH=0.45; // red box padding as share of its text cap height
const cv=document.createElement('canvas').getContext('2d');
function metrics(fs){cv.font=fs+'px Anton';const m=cv.measureText('H');return {asc:m.fontBoundingBoxAscent,desc:m.fontBoundingBoxDescent,cap:m.actualBoundingBoxAscent};}
function capCrop(el,fs){ // make the element's box exactly the cap height
  const m=metrics(fs); const L=m.cap; el.style.fontSize=fs+'px'; el.style.lineHeight=L+'px'; el.style.height=L+'px';
  const base=(L-(m.asc+m.desc))/2+m.asc; el.style.top=(-(base-m.cap))+'px'; el.parentElement.style.height=L+'px'; return L;}
document.fonts.ready.then(()=>{
  let caps=[];
  document.querySelectorAll('.ln').forEach(el=>{
    el.style.fontSize='100px'; const w=el.offsetWidth; const fs=100*(+(el.dataset.w||LINE_W))/w; caps.push(capCrop(el,fs));
  });
  const rows=document.querySelectorAll('.row');
  rows.forEach((r,i)=>{ if(i>0) r.style.marginTop=(LINE_GAP*Math.min(caps[i-1],caps[i]))+'px'; });
  const box=document.querySelector('.redbox'), inn=box.querySelector('.in');
  inn.style.fontSize='100px'; const w100=inn.offsetWidth, r=metrics(100).cap/100;
  const fs=BOX_W/(w100/100 + 2*BOX_PADH*r); const cap=capCrop(inn,fs);
  box.style.padding=(BOX_PADV*cap)+'px '+(BOX_PADH*cap)+'px'; box.style.height='auto'; inn.parentElement.style.height='auto';
  box.parentElement.style.marginTop=(BOX_GAP*caps[2]+8)+'px';
  inn.querySelectorAll('.tt').forEach(t=>t.style.fontSize='inherit');
  const hb=document.querySelector('.head').getBoundingClientRect();
  document.body.dataset.headBottom=Math.round(hb.bottom); document.body.dataset.caps=caps.map(Math.round).join(',')+','+Math.round(cap);
});
</script>
</body></html>
```

