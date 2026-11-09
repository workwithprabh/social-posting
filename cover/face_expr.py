"""Facial-expression analysis for reel covers (MediaPipe Face Landmarker: 478 landmarks + 52 muscle blendshapes).
  python3 face_expr.py image.png [...]            -> readout + expression scores for each image
  python3 face_expr.py --scan ID target [step]     -> scan vids/<ID>.mp4, write ID/expr_<target>.jpg with the best HELD frames
targets: confident_smile, warm_smile, shocked, emotional, serious
"""
import sys, json, subprocess, numpy as np, cv2, mediapipe as mp
from PIL import Image, ImageDraw
from mediapipe.tasks.python import vision, BaseOptions
_opt = vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path='models/face_landmarker.task'),
                                    output_face_blendshapes=True, output_facial_transformation_matrixes=True, num_faces=1)
LM = vision.FaceLandmarker.create_from_options(_opt)
INNER = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]
CHEEK_L, CHEEK_R, FOREHEAD = [116, 117, 118, 100, 126, 142], [345, 346, 347, 329, 355, 371], [10, 109, 67, 338, 297, 151]

def analyze(rgb):
    res = LM.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb)))
    if not res.face_blendshapes: return None
    b = {c.category_name: c.score for c in res.face_blendshapes[0]}
    h, w = rgb.shape[:2]; P = np.array([(p.x * w, p.y * h) for p in res.face_landmarks[0]])
    face_w = np.linalg.norm(P[234] - P[454])
    # teeth: bright, low-saturation pixels inside the inner-lip polygon, as a share of face width^2
    m = np.zeros((h, w), np.uint8); cv2.fillPoly(m, [P[INNER].astype(np.int32)], 1)
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(float); L = lab[..., 0] * 100 / 255; sat = np.hypot(lab[..., 1] - 128, lab[..., 2] - 128)
    teeth = ((m == 1) & (L > 62) & (sat < 22)).sum() / face_w ** 2 * 100
    mouth_open = m.sum() / face_w ** 2 * 100
    def region(ids):
        rm = np.zeros((h, w), np.uint8); cv2.fillPoly(rm, [cv2.convexHull(P[ids].astype(np.int32))], 1); return L[rm == 1]
    cl, cr, fh = region(CHEEK_L), region(CHEEK_R), region(FOREHEAD)
    skin = np.concatenate([cl, cr, fh])
    M = np.array(res.facial_transformation_matrixes[0]); yaw = np.degrees(np.arctan2(-M[2, 0], np.hypot(M[2, 1], M[2, 2]))); pitch = np.degrees(np.arctan2(M[2, 1], M[2, 2]))
    g = lambda *k: float(np.mean([b[x] for x in k]))
    d = dict(smile=g('mouthSmileLeft', 'mouthSmileRight'), smile_asym=abs(b['mouthSmileLeft'] - b['mouthSmileRight']),
             jaw=b['jawOpen'], teeth=teeth, mouth_open=mouth_open, funnel=g('mouthFunnel', 'mouthPucker'),
             stretch=g('mouthStretchLeft', 'mouthStretchRight', 'mouthUpperUpLeft', 'mouthUpperUpRight', 'mouthLowerDownLeft', 'mouthLowerDownRight'),
             frown=g('mouthFrownLeft', 'mouthFrownRight'), press=g('mouthPressLeft', 'mouthPressRight', 'mouthRollLower', 'mouthRollUpper'),
             cheek=g('cheekSquintLeft', 'cheekSquintRight'), brow_up=g('browInnerUp', 'browOuterUpLeft', 'browOuterUpRight'),
             brow_inner=b['browInnerUp'], brow_down=g('browDownLeft', 'browDownRight'), eye_wide=g('eyeWideLeft', 'eyeWideRight'),
             blink=g('eyeBlinkLeft', 'eyeBlinkRight'), squint=g('eyeSquintLeft', 'eyeSquintRight'),
             gaze_off=max(g('eyeLookOutLeft', 'eyeLookInRight'), g('eyeLookInLeft', 'eyeLookOutRight'), g('eyeLookUpLeft', 'eyeLookUpRight'), g('eyeLookDownLeft', 'eyeLookDownRight')),
             yaw=float(yaw), pitch=float(pitch), skin_L=float(np.median(skin)), glow=float(np.percentile(skin, 92) - np.percentile(skin, 30)),
             skin_even=float(abs(np.median(cl) - np.median(cr))), face_w=float(face_w))
    return d

def scores(d):
    c = lambda x: float(np.clip(x, 0, 1))
    eyes_ok = c(1 - max(d['blink'] - .35, 0) * 3) * c(1 - max(d['gaze_off'] - .35, 0) * 2.5) * c(1 - max(abs(d['yaw']) - 12, 0) / 20)
    talking = c((d['stretch'] - .15) * 3 + max(d['jaw'] - .12, 0) * 2 * (1 - d['funnel']))  # mid-word mouth shapes
    teeth_pen = c((d['teeth'] - .4) / 2)
    return dict(
        confident_smile=eyes_ok * c(d['smile'] / .55) * c(1 - max(d['jaw'] - .08, 0) * 6) * (1 - teeth_pen) * c(1 - d['smile_asym'] * 2.5) * c(1 - d['brow_down'] * 1.5),
        warm_smile=eyes_ok * c(d['smile'] / .7) * c(.4 + d['cheek'] * 1.5) * c(1 - max(d['jaw'] - .22, 0) * 4) * c(1 - d['smile_asym'] * 2),
        shocked=eyes_ok * c(d['brow_up'] / .5) * c((d['eye_wide'] + .1) / .4) * c(min(d['jaw'] / .28, 1)) * c(1 - max(d['jaw'] - .7, 0) * 3) * c(1 - d['smile'] * 2) * c(1 - talking * .7),
        emotional=eyes_ok * c(d['brow_inner'] / .45) * c((d['frown'] + d['press'] * .5) / .3) * c(1 - d['jaw'] * 4) * c(1 - d['smile'] * 3),
        serious=eyes_ok * c(1 - d['jaw'] * 6) * c(1 - abs(d['smile'] - .12) * 3) * (1 - teeth_pen),
        talking=talking)

if __name__ == '__main__' and sys.argv[1] != '--scan':
    for f in sys.argv[1:]:
        d = analyze(np.array(Image.open(f).convert('RGB'))); s = scores(d) if d else {}
        print(f, json.dumps({k: round(v, 2) for k, v in {**(d or {}), **s}.items()}))
elif __name__ == '__main__':
    vid, target = sys.argv[2], sys.argv[3]; step = float(sys.argv[4]) if len(sys.argv) > 4 else .1
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'vids/{vid}.mp4', '-vf', f'fps={1/step}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 1920, 1080, 3); rows = []
    for i, f in enumerate(fr):
        d = analyze(f)
        if d and d['face_w'] > 150: rows.append(dict(i=i, t=round((i + .5) * step, 2), **d, **scores(d)))
    KEYS = ['smile', 'jaw', 'brow_up', 'eye_wide', 'frown', 'blink', 'stretch']
    for k, r in enumerate(rows):  # held: how little the face changes over +-0.2 s
        nb = [q for q in rows if 0 < abs(q['t'] - r['t']) <= .21]
        r['held'] = float(np.clip(1 - np.mean([np.abs(np.array([r[x] for x in KEYS]) - np.array([q[x] for q in [q] for x in KEYS])).mean() for q in nb]) * 6, 0, 1)) if nb else 0
        r['final'] = r[target] * (.5 + .5 * r['held'])
    json.dump(rows, open(f'{vid}/expr.json', 'w'))
    pick = []
    for r in sorted(rows, key=lambda r: -r['final']):
        if all(abs(r['t'] - q['t']) >= .5 for q in pick): pick.append(r)
        if len(pick) == 12: break
    tiles = []
    for r in pick:
        f = fr[r['i']]; det = LM.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(f)))
        P = np.array([(p.x * 1080, p.y * 1920) for p in det.face_landmarks[0]]); x0, y0 = P.min(0); x1, y1 = P.max(0); s = (x1 - x0) * .45
        im = Image.fromarray(f[int(max(0, y0 - s)):int(y1 + s * .6), int(max(0, x0 - s)):int(x1 + s)]).resize((300, 340))
        dr = ImageDraw.Draw(im); dr.rectangle((0, 0, 300, 28), fill=0)
        dr.text((3, 2), f"{r['t']}s {target[:8]} {r[target]:.2f} held {r['held']:.2f}", fill=(255, 255, 0))
        dr.text((3, 15), f"jaw {r['jaw']:.2f} teeth {r['teeth']:.1f} smile {r['smile']:.2f} brow {r['brow_up']:.2f}", fill=(200, 255, 200)); tiles.append(im)
    S = Image.new('RGB', (6 * 300, ((len(tiles) + 5) // 6) * 340))
    for i, t in enumerate(tiles): S.paste(t, ((i % 6) * 300, (i // 6) * 340))
    S.save(f'{vid}/expr_{target}.jpg', quality=85)
    print(vid, target, 'faces', len(rows), [(r['t'], round(r[target], 2), round(r['held'], 2)) for r in pick])
