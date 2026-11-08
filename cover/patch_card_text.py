"""Replace 'Dee Emm Hyundai' with 'Dee Emm Mahindra' on the end card of DEM-2611-03.
usage: python3 patch_card.py test | video in.mp4 out.mp4
Method: build a corrected label on a clean pill from a steady reference frame; for every card frame, find the
card (multi-scale match, then sub-pixel affine ECC), estimate the card's fade level, and add
fade * (new label - old label) warped into place. Exact alignment makes the old word cancel out."""
import sys, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

FONT = '../node_modules/@fontsource/poppins/files/poppins-latin-700-normal.woff'
NEW = 'Dee Emm Mahindra'
LUM = np.array([.299, .587, .114], np.float32)
ref = cv2.cvtColor(cv2.imread('ref.png'), cv2.COLOR_BGR2RGB).astype(np.float32)
TX0, TY0, TX1, TY1 = 200, 1160, 880, 1300            # template area (pill + gold border + a bit of card)
T = ref[TY0:TY1, TX0:TX1].copy(); Tl = T @ LUM
R, G, B = T[..., 0], T[..., 1], T[..., 2]
# old label = dark navy pixels in the pill band
band = np.zeros(Tl.shape, bool); band[30:105, 40:640] = True
text = band & (Tl < 150) & (B >= R - 5)
ys, xs = np.where(text)
x0, x1 = np.percentile(xs, .3), np.percentile(xs, 99.7); y0, y1 = np.percentile(ys, .3), np.percentile(ys, 99.7)
ink = np.median(T[text & (Tl > np.percentile(Tl[text], 20)) & (Tl < np.percentile(Tl[text], 50))], axis=0)
# clean pill: per row, interpolate between the pill colour just left and right of the label
clean = T.copy(); bx0, bx1, by0, by1 = int(x0) - 8, int(x1) + 9, int(y0) - 6, int(y1) + 7
for y in range(by0, by1):
    lft = np.median(T[y, bx0 - 14:bx0], axis=0); rgt = np.median(T[y, bx1:bx1 + 14], axis=0)
    w = np.linspace(0, 1, bx1 - bx0)[:, None]; clean[y, bx0:bx1] = lft * (1 - w) + rgt * w
# vertical smoothing of the filled block so it matches the pill gradient
blk = clean[by0:by1, bx0:bx1]; clean[by0:by1, bx0:bx1] = cv2.GaussianBlur(blk, (1, 9), 0)
# new label, same cap height and centre as the old one, drawn at 4x
SS = 4; size = 20
while True:
    f = ImageFont.truetype(FONT, size * SS); hb = f.getbbox('Dee Emm Hyundai')
    if (hb[3] - hb[1]) / SS >= (y1 - y0): break
    size += 1
nb = f.getbbox(NEW); w = (nb[2] - nb[0]) / SS
maxw = (bx1 - bx0) + 40
if w > maxw:
    size = int(size * maxw / w); f = ImageFont.truetype(FONT, size * SS); nb = f.getbbox(NEW); hb = f.getbbox('Dee Emm Hyundai'); w = (nb[2] - nb[0]) / SS
lay = Image.new('L', (T.shape[1] * SS, T.shape[0] * SS), 0)
ImageDraw.Draw(lay).text((((x0 + x1) / 2 - w / 2) * SS - nb[0], y0 * SS - hb[1]), NEW, font=f, fill=255)
a = np.array(lay.resize((T.shape[1], T.shape[0]), Image.LANCZOS), np.float32)[..., None] / 255
new = clean * (1 - a) + ink * a
diff = (new - T); diff[~band] = 0
tm = text.astype(np.float32); bm = (band & ~cv2.dilate(text.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool)).astype(np.float32)
bm[:by0] = 0; bm[by1:] = 0
D0 = (Tl * bm).sum() / bm.sum() - (Tl * tm).sum() / tm.sum()
Tg = Tl.astype(np.uint8)

def locate(g):
    best = (-1, 0, 0, 1)
    for s in np.arange(0.84, 1.17, 0.02):
        t = cv2.resize(Tg, None, fx=s, fy=s); r = cv2.matchTemplate(g[950:1550], t, cv2.TM_CCOEFF_NORMED)
        _, mx, _, loc = cv2.minMaxLoc(r)
        if mx > best[0]: best = (mx, loc[0], loc[1] + 950, s)
    return best

LAST = {}
def soften(frame, warp):
    """blur the label area (feathered) so a half-faded label cannot be read"""
    m = np.zeros(band.shape, np.float32); m[max(0, by0 - 16):by1 + 16, max(0, bx0 - 34):bx1 + 34] = 1
    m = cv2.GaussianBlur(m, (0, 0), 6)
    Hh, Ww = frame.shape[:2]; mw = cv2.warpAffine(m, warp, (Ww, Hh))[..., None]
    bl = cv2.GaussianBlur(frame, (0, 0), 11).astype(np.float32)
    return np.clip(frame * (1 - mw) + bl * mw, 0, 255).astype(np.uint8)
def patch(frame, force=None):
    g = (frame.astype(np.float32) @ LUM).astype(np.uint8)
    if force is not None:
        warp, score, s = force.copy(), 0.0, float(force[0, 0])
    else:
        score, px, py, s = locate(g)
        if score < 0.45: return frame, score, 0, s
        warp = np.array([[s, 0, px], [0, s, py]], np.float32)
    try:
        if force is not None: raise cv2.error('skip')
        _, warp = cv2.findTransformECC(Tg.astype(np.float32), g.astype(np.float32), warp, cv2.MOTION_AFFINE,
                                       (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1e-5), None, 5)
    except cv2.error:
        pass
    Hh, Ww = frame.shape[:2]
    LAST['warp'] = warp
    put = lambda img, interp=cv2.INTER_LINEAR: cv2.warpAffine(img, warp, (Ww, Hh), flags=interp)
    tmw, bmw = put(tm) > .5, put(bm) > .5
    L = frame.astype(np.float32) @ LUM
    alpha = float(np.clip((L[bmw].mean() - L[tmw].mean()) / D0, 0, 1))
    d = np.dstack([put(diff[..., c]) for c in range(3)])
    out = np.clip(frame.astype(np.float32) + alpha * d, 0, 255).astype(np.uint8)
    # clean-up: leftover dark marks of the old word = darker than the local pill colour but not part of the new label
    boxm = np.zeros(band.shape, np.float32); boxm[by0 - 2:by1 + 2, bx0 - 4:bx1 + 4] = 1
    bw = put(boxm) > .5; nl = put(a[..., 0]) > .06
    nl = cv2.dilate(nl.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    ys_, xs_ = np.where(bw)
    if len(ys_):
        Y0, Y1, X0, X1 = ys_.min(), ys_.max() + 1, xs_.min(), xs_.max() + 1
        sub = out[Y0:Y1, X0:X1]; Ls = sub.astype(np.float32) @ LUM
        loc = cv2.medianBlur(sub, 21).astype(np.float32) @ LUM
        res = bw[Y0:Y1, X0:X1] & ~nl[Y0:Y1, X0:X1] & ((loc - Ls) > max(5, 14 * alpha))
        res = cv2.dilate(res.astype(np.uint8), np.ones((3, 3), np.uint8)) * (~nl[Y0:Y1, X0:X1]).astype(np.uint8)
        if res.any():
            fixed = cv2.inpaint(sub, res * 255, 3, cv2.INPAINT_TELEA)
            out[Y0:Y1, X0:X1] = fixed
    return out, score, alpha, s

if sys.argv[1] == 'test':
    tiles = []
    for t in ['34.2', '34.5', '34.8', '35.2', '36.5', '37.9', '38.3']:
        png = subprocess.run(['ffmpeg', '-v', 'error', '-ss', t, '-i', '../../videos/DEM-2611-03.mp4', '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
        fr = cv2.cvtColor(cv2.imdecode(np.frombuffer(png, np.uint8), 1), cv2.COLOR_BGR2RGB)
        o, sc, al, s = patch(fr); print(t, 'match %.2f alpha %.2f scale %.2f' % (sc, al, s))
        tiles.append(np.hstack([fr[1120:1330, 150:930], o[1120:1330, 150:930]]))
    Image.fromarray(np.vstack(tiles)).resize((1040, 980)).save('patch_test.jpg', quality=92)
else:
    src, dst = sys.argv[2], sys.argv[3]
    Wd, Hd, fps = 1080, 1920, 30
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{Wd}x{Hd}', '-r', str(fps), '-i', '-',
                            '-i', src, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '22', '-maxrate', '6M', '-bufsize', '12M',
                            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-movflags', '+faststart', '-shortest', dst], stdin=subprocess.PIPE)
    n = 0; log = []; pend = []; SOFT_END = 34.45 * fps
    while True:
        buf = dec.stdout.read(Wd * Hd * 3)
        if len(buf) < Wd * Hd * 3: break
        fr = np.frombuffer(buf, np.uint8).reshape(Hd, Wd, 3)
        if 33.5 * fps <= n <= 38.7 * fps:
            o, sc, al, s = patch(fr)
            if 'warp' not in LAST:
                pend.append(fr); n += 1; continue          # card not found yet: hold the frame
            if pend:                                       # first lock: soften the held frames at this position
                for pf in pend:
                    enc.stdin.write(soften(pf, LAST['warp']).tobytes()); log.append(('soft',))
                pend = []
            if n < SOFT_END:
                fr = soften(fr, LAST['warp']); log.append(('soft',))
            else:
                fr = o; log.append((n, round(sc, 2), round(al, 2), round(s, 2)))
        enc.stdin.write(fr.tobytes()); n += 1
    enc.stdin.close(); enc.wait()
    print('frames', n, 'softened', sum(1 for l in log if l[0] == 'soft'), 'patched', sum(1 for l in log if len(l) == 4 and l[2] > 0), 'unpatched', [l[0] for l in log if len(l) == 4 and l[2] == 0])
