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
fr = cv2.imread(C.get('frame', 'presenter.png')); H, W = fr.shape[:2]
det = cv2.FaceDetectorYN.create(os.path.join(HERE, 'models/yunet.onnx'), '', (W, H), 0.6)
fx, fy, fw, fh = det.detect(fr)[1][0][:4]; fcx, fcy = fx + fw / 2, fy + fh / 2
run('python3', '../03_grade.py', 'person2.png', 'person_natural.png', str(fcx - 70), str(fcy - 90), str(C.get('lift', .30)))
if C.get('sharpen', .5):
    im = cv2.imread('person_natural.png', cv2.IMREAD_UNCHANGED); rgb = im[..., :3].astype(np.float32)
    bl = cv2.GaussianBlur(rgb, (0, 0), 1.6); im[..., :3] = np.clip(rgb + C.get('sharpen', .5) * (rgb - bl), 0, 255).astype(np.uint8)
    cv2.imwrite('person_natural.png', im)
for f in ['grunge_light.png', 'brush_wide.png', 'brush_dense.png']:
    if not os.path.exists(f): run('python3', '../05_textures.py'); break
shutil.copy(C['logo'], 'logo.png')
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
bn = C.get('banner', ['WATCH THIS', 'FIRST!'])
banner = f'<span class="tt w" data-t="{bn[0]}">{bn[0]}</span><span class="tt y" data-t="{bn[1]}">{bn[1]}</span>'
H2 = open('../cover_v2.html').read()
rep = dict(BGBLUR=f"{C.get('bg_blur',5)}px", BGBRIGHT=str(C.get('bg_bright', .72)), PFADE0=str(C.get('pfade', [1560, 1690])[0]), PFADE1=str(C.get('pfade', [1560, 1690])[1]),
           SIDETOP=str(C.get('side_top', 860)), SIDEW=str(C.get('side_w', 420)), HEADTOP=str(C.get('head_top', 60)), BOXW=str(C.get('box_w', 1010)),
           BOXPAD=C.get('box_pad', '30px 40px 34px'), WATCHTOP=str(C.get('watch_top', 1440)), LOGOH=str(C.get('logo_h', 120)), HEADHTML=head, BANNERHTML=banner, **T)
for k in sorted(rep, key=len, reverse=True): H2 = H2.replace(k, rep[k])
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
for _ in range(4):
    L = float(m.split('face L ')[1].split(' ')[0])
    if abs(L - tgt) <= 2: break
    br = round(br * (tgt / L) ** 1.3, 3); info, m = render(br)
print(ID, info, '| brightness', br, '|', m)
