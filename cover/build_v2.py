"""Build a v2 cover (the AM-2610-05 look).  usage: python3 build_v2.py <ID>
Reads <ID>/cfg2.json: {"theme":"mahindra|hyundai","frame":"presenter.png","lines":[l1,l2],"box":[b1,b2],
 "banner":["WATCH THIS","FIRST!"],"logo":"path.png","logo_h":120, optional: fade, lift, face_w(285), face_c([815,1040]),
 side_top(860), side_w(420), head_top(60), bg_blur(5), bg_bright(.72), target_L(62)}
Needs in <ID>/: presenter.png (frame with the reel's emotion), bg.png (showroom frame), graphic.png (left card)."""
import sys, os, re, json, subprocess, shutil, numpy as np, cv2
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ID = sys.argv[1]; D = os.path.join(HERE, ID)
C = json.load(open(os.path.join(D, 'cfg2.json'))); os.chdir(D)
run = lambda *a: subprocess.run(a, check=True, capture_output=True, text=True).stdout
fade = C.get('fade', [1240, 1400])
if not os.path.exists('person2.png') or C.get('recut'):
    run('python3', '../02_cutout.py', C.get('frame', 'presenter.png'), 'person2.png', str(fade[0]), str(fade[1]))
    run('python3', '../clean.py', 'person2.png', 'person2.png', '60')
    if C.get('human_mask'):  # drop car doors / furniture that isnet keeps: keep only what the human model sees
        from rembg import remove, new_session
        src = Image.open(C.get('frame', 'presenter.png')).convert('RGB')
        h = np.array(remove(src, session=new_session('u2net_human_seg')).convert('RGBA'))[..., 3].astype(np.float32) / 255
        hm = cv2.GaussianBlur((h > .3).astype(np.float32), (0, 0), 3)
        p = np.array(Image.open('person2.png').convert('RGBA')).astype(np.float32)
        p[..., 3] *= np.clip(hm[:p.shape[0], :p.shape[1]] * 1.2, 0, 1); Image.fromarray(p.astype(np.uint8)).save('person2.png')
fr = cv2.imread(C.get('frame', 'presenter.png')); H, W = fr.shape[:2]
det = cv2.FaceDetectorYN.create(os.path.join(HERE, 'models/yunet.onnx'), '', (W, H), 0.6)
fx, fy, fw, fh = det.detect(fr)[1][0][:4]; fcx, fcy = fx + fw / 2, fy + fh / 2
run('python3', '../03_grade.py', 'person2.png', 'person_natural.png', str(fcx - 70), str(fcy - 90), str(C.get('lift', .30)))
if C.get('glow', 1):
    # "glow up": even, luminous skin like AM-2610-05 (skin spread ~5 vs 11-22 on v1/v2 covers)
    im = cv2.imread('person_natural.png', cv2.IMREAD_UNCHANGED); rgb = im[..., :3]; a = im[..., 3].astype(np.float32) / 255
    ycc = cv2.cvtColor(rgb, cv2.COLOR_BGR2YCrCb)
    sk = ((ycc[..., 1] > 135) & (ycc[..., 1] < 178) & (ycc[..., 2] > 80) & (ycc[..., 2] < 132)).astype(np.float32)
    sk = cv2.GaussianBlur(cv2.morphologyEx(sk, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)), (0, 0), 6) * a
    g = float(C.get('glow', 1))
    smooth = cv2.bilateralFilter(rgb, 15, 38, 12).astype(np.float32)
    lab = cv2.cvtColor(smooth.astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32); L = lab[..., 0]
    base = cv2.GaussianBlur(L, (0, 0), 22)
    L2 = base + (L - base) * (1 - .3 * g)                       # flatten blotches and hot spots
    L2 = L2 + np.clip(175 - base, 0, None) * .22 * g             # fill light: lift the darker skin areas
    lab[..., 0] = L2; even = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)
    hi = np.clip((cv2.cvtColor(even.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32) - 150) / 105, 0, 1)
    bloom = cv2.GaussianBlur(even * hi[..., None], (0, 0), 10)
    even = 255 - (255 - even) * (255 - bloom * .35 * g) / 255     # soft sheen on highlights (screen)
    w = (sk * .85 * g)[..., None]; out = rgb.astype(np.float32) * (1 - w) + even * w
    im[..., :3] = np.clip(out, 0, 255).astype(np.uint8); cv2.imwrite('person_natural.png', im)
if C.get('edge_fade'):
    im = cv2.imread('person_natural.png', cv2.IMREAD_UNCHANGED); n = int(C['edge_fade'])
    ramp = np.clip(np.arange(im.shape[1]) / n, 0, 1); im[..., 3] = (im[..., 3] * ramp[None, :]).astype(np.uint8)
    cv2.imwrite('person_natural.png', im)
if C.get('sharpen', .5):
    im = cv2.imread('person_natural.png', cv2.IMREAD_UNCHANGED); rgb = im[..., :3].astype(np.float32)
    bl = cv2.GaussianBlur(rgb, (0, 0), 1.6); im[..., :3] = np.clip(rgb + C.get('sharpen', .5) * (rgb - bl), 0, 255).astype(np.uint8)
    cv2.imwrite('person_natural.png', im)
for f in ['grunge_light.png', 'brush_wide.png', 'brush_dense.png']:
    if not os.path.exists(f): run('python3', '../05_textures.py'); break
if C.get('logo'): shutil.copy(C['logo'], 'logo.png')
tw = C.get('face_w', 285); cx, cy = C.get('face_c', [815, 1040]); s = tw / fw
left, top, width = cx - fcx * s, cy - fcy * s, W * s
box = [int(cx - fw * s * .38), int(cy - fh * s * .30), int(cx + fw * s * .38), int(cy + fh * s * .45)]
hy = C['theme'] == 'hyundai'
if hy:
    for b in ['brush_wide', 'brush_dense']:
        a = np.array(Image.open(b + '.png')); r = a[..., 0].astype(float); o = a.copy()
        o[..., 0] = (r * .10).astype('uint8'); o[..., 1] = (r * .45).astype('uint8'); o[..., 2] = np.clip(r + 20, 0, 255).astype('uint8')
        Image.fromarray(o).save(b + '_b.png')
    T = dict(EDGE='#d6ecff', GLOW1='rgba(60,150,255,.75)', STKGLOW='rgba(30,120,255,.55)', BRUSH_W='brush_wide_b.png', BRUSH_D='brush_dense_b.png',
             BOXBG='linear-gradient(180deg,#0b2f86 0%,#061d57 55%,#0a2a7a 100%)', BOXRIM='#e6f2ff',
             BOXSHADOW='0 0 0 4px #1f6fff,0 0 22px 6px rgba(31,111,255,1),0 0 64px 14px rgba(0,90,255,.5),inset 0 0 24px rgba(80,160,255,.45),0 14px 0 rgba(0,0,0,.45)',
             GLOW='drop-shadow(0 0 1.5px #ffffff) drop-shadow(0 0 3px #9fd4ff) drop-shadow(0 0 12px rgba(40,140,255,.85)) drop-shadow(0 0 30px rgba(0,90,255,.38))')
else:
    T = dict(EDGE='#ffd23a', GLOW1='rgba(255,170,0,.75)', STKGLOW='rgba(255,0,0,.45)', BRUSH_W='brush_wide.png', BRUSH_D='brush_dense.png',
             BOXBG='linear-gradient(180deg,#3d0404 0%,#160000 55%,#2c0202 100%)', BOXRIM='#ffe3da',
             BOXSHADOW='0 0 0 4px #ff2410,0 0 22px 6px rgba(255,36,16,1),0 0 64px 14px rgba(255,20,0,.55),inset 0 0 24px rgba(255,40,20,.5),0 14px 0 rgba(0,0,0,.45)',
             GLOW='drop-shadow(0 0 1.5px #fff2a8) drop-shadow(0 0 3px #ffcc00) drop-shadow(0 0 12px rgba(255,170,0,.85)) drop-shadow(0 0 30px rgba(255,110,0,.4))')
tt = lambda t, c, w=None, mx=None: f'<span class="ln tt {c}"{f" data-w={w}" if w else ""}{f" data-max={mx}" if mx else ""} data-t="{t}">{t}</span>'
l1, l2 = C['lines']; b1, b2 = C['box']
head = (f'<div class="row r1">{tt(l1,"w",C.get("l1_w",860),C.get("l1_max",190))}</div>'
        f'<div class="row r2"><i class="stk"></i>{tt(l2,"y",C.get("l2_w",960),C.get("l2_max",300))}</div>'
        f'<div class="box"><div class="row first">{tt(b1,"w",C.get("b1_w",880),C.get("b_max",190))}</div>'
        f'<div class="row">{tt(b2,"y",C.get("b2_w",880),C.get("b_max",190))}</div></div>')
bn = C.get('banner')
banner = f'<span class="tt w" data-t="{bn[0]}">{bn[0]}</span><span class="tt y" data-t="{bn[1]}">{bn[1]}</span>' if bn else ''
H2 = open('../cover_v2.html').read()
if not C.get('logo'):
    H2 = H2.replace('<div class="logo"><i></i><img src="logo.png"><i></i></div>', '')
    C.setdefault('watch_top', 1600); C.setdefault('pfade', [1720, 1880])
    C['css'] = C.get('css', '') + '\n.shade::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 62%,rgba(0,0,0,.93) 74%,#050507 88%)}'
rep = dict(BGBLUR=f"{C.get('bg_blur',5)}px", BGBRIGHT=str(C.get('bg_bright', .72)), PFADE0=str(C.get('pfade', [1560, 1690])[0]), PFADE1=str(C.get('pfade', [1560, 1690])[1]),
           SIDETOP=str(C.get('side_top', 860)), SIDEW=str(C.get('side_w', 420)), HEADTOP=str(C.get('head_top', 60)), BOXW=str(C.get('box_w', 1010)),
           BOXPAD=C.get('box_pad', '30px 40px 34px'), WATCHTOP=str(C.get('watch_top', 1440)), LOGOH=str(C.get('logo_h', 120)), HEADHTML=head, BANNERHTML=banner, **T)
for k in sorted(rep, key=len, reverse=True): H2 = H2.replace(k, rep[k])
if not bn: H2 = H2.replace('<div class="watch"><div class="brush"></div><b></b></div>', '')
br = C.get('bright', 1.0)
def page(br):
    css = f".person{{left:{left:.0f}px;top:{top:.0f}px;width:{width:.0f}px;filter:brightness({br}) contrast(1.06) saturate(1.1) {T['GLOW']}}}\n{C.get('css','')}"
    return H2.replace('PFILTER', 'none').replace('</style>', css + '\n</style>')
def render(br):
    open('cover2.html', 'w').write(page(br))
    info = run('node', '../render.js', os.path.abspath('cover2.html'), os.path.abspath('cover2.png'))
    m = run('python3', '../04_face_metrics.py', 'cover2.png', *map(str, box))
    return info.strip(), m.strip()
info, m = render(br); tgt = C.get('target_L', 62)
for _ in range(0 if C.get("target_L",62)>100 else 4):
    L = float(m.split('face L ')[1].split(' ')[0])
    if abs(L - tgt) <= 2: break
    br = round(br * (tgt / L) ** 1.3, 3); info, m = render(br)
print(ID, info, '| brightness', br, '|', m)
