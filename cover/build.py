"""Build one cover from cover_template.html.  usage: python3 build.py <ID>  (config in CFG below)
Assumes the per-reel folder already has: presenter.png bg.png panel_bg.png graphic.png [car_final.png]."""
import sys, re, json, subprocess, os, numpy as np, cv2
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ID = sys.argv[1]; D = os.path.join(HERE, ID); CFG = json.load(open(os.path.join(D, 'cfg.json')))
os.chdir(D)

def run(*a):
    return subprocess.run(a, check=True, capture_output=True, text=True).stdout

# --- presenter: cutout, clean, find face, grade
if not os.path.exists('person.png') or CFG.get('recut'):
    run('python3', '02_cutout.py', 'presenter.png', 'person.png', str(CFG['fade'][0]), str(CFG['fade'][1]))
    run('python3', '../clean.py', 'person.png', 'person.png', '60')
fr = cv2.imread('presenter.png'); H, W = fr.shape[:2]
det = cv2.FaceDetectorYN.create(os.path.join(HERE, '../models/yunet.onnx'), '', (W, H), 0.6)
_, faces = det.detect(fr)
fx, fy, fw, fh = faces[0][:4]
fcx, fcy = fx + fw / 2, fy + fh / 2
run('python3', '03_grade.py', 'person.png', 'person_natural.png', str(fcx - 70), str(fcy - 90))

# place: face width -> CFG face_w (default 205), centre -> CFG face_c (default 700,1150)
tw = CFG.get('face_w', 205); cx, cy = CFG.get('face_c', [700, 1150])
s = tw / fw
left, top, width = cx - fcx * s, cy - fcy * s, W * s
box = [int(cx - fw * s * .38), int(cy - fh * s * .30), int(cx + fw * s * .38), int(cy + fh * s * .45)]

# --- textures (+ Hyundai blue variants)
if not os.path.exists('brush_wide.png'):
    run('python3', '05_textures.py')
blue = CFG['theme'] == 'hyundai'
if blue:
    for b in ['brush_wide', 'brush_left', 'brush_right', 'brush_line', 'brush_dense']:
        a = np.array(Image.open(b + '.png')); r = a[..., 0].astype(float)
        out = a.copy(); out[..., 0] = (r * .10).astype('uint8'); out[..., 1] = (r * .45).astype('uint8'); out[..., 2] = np.clip(r * 1.0 + 20, 0, 255).astype('uint8')
        Image.fromarray(out).save(b + '_b.png')

T = open('cover_template.html').read()
def tt(t, c, small=False):
    return f'<span class="{"tt s" if small else "ln tt"} {c}" data-t="{t}">{t}</span>'
l1, l2, l3 = CFG['lines']
head = (f'<div class="row r1"><i class="stk"></i><span class="ln tt w" data-w="{CFG.get("l1_w", 860)}" data-t="{l1}">{l1}</span></div>\n'
        f'    <div class="row r2"><i class="stk"></i>{tt(l2, "w")}</div>\n'
        f'    <div class="row r3"><i class="stk"></i><i class="stk2"></i>{tt(l3, "y")}</div>\n'
        f'    <div class="boxrow"><div class="redbox"><span class="in">' + ''.join(tt(t, c, True) for t, c in CFG['box']) + '</span></div></div>')
T = re.sub(r'<div class="row r1">.*?</div></div>\n', head + '\n', T, flags=re.S)
b1, b2 = CFG.get('banner', ['WATCH THIS', 'FIRST!'])
T = T.replace('<span class="tt s w" data-t="WATCH THIS">WATCH THIS</span><span class="tt s y" data-t="FIRST!">FIRST!</span>',
              f'{tt(b1, "w", True)}{tt(b2, "y", True)}')
T = re.sub(r'<div class="foot">.*?</div>', f'<div class="foot">{CFG["foot"]}</div>', T)
if not os.path.exists('car_final.png'):
    T = T.replace('<img class="car" src="car_final.png">', '')
gw = CFG.get('graphic_w', 470); gtop = CFG.get('graphic_top', 925)
br = CFG.get('bright', .85)
css = f""".person{{left:{left:.0f}px;top:{top:.0f}px;width:{width:.0f}px;filter:brightness({br}) contrast({CFG.get('contrast',1.08)}) PERSONGLOW}}
.vs{{left:{CFG.get('graphic_left',16)}px;top:{gtop}px;width:{gw}px}}
{CFG.get('css','')}"""
if blue:
    T = re.sub(r'url\((brush_\w+)\.png\)', r'url(\1_b.png)', T)
    glow = 'drop-shadow(0 0 0 #fff) drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 -5px 0 #fff) drop-shadow(0 0 8px #7cc4ff) drop-shadow(0 0 20px rgba(40,140,255,.85)) drop-shadow(0 0 44px rgba(0,80,255,.55))'
    css += """
.tt{-webkit-text-stroke:6px #041638;text-shadow:4px 6px 0 #041638,6px 10px 18px rgba(0,8,30,.8)}
.tt.s{-webkit-text-stroke:4px #041638;text-shadow:3px 4px 0 #041638,4px 7px 12px rgba(0,8,30,.75)}
.stk{filter:drop-shadow(0 0 14px rgba(30,120,255,.5))}
.redbox{background:linear-gradient(180deg,#0b3aa8 0%,#062a7a 50%,#0a2f8c 100%);border:3px solid #e6f2ff;
  box-shadow:0 0 0 4px #1f6fff,0 0 20px 5px rgba(31,111,255,1),0 0 60px 12px rgba(0,90,255,.55),inset 0 0 0 2px rgba(80,160,255,.9),inset 0 0 22px rgba(80,160,255,.5),inset 0 -30px 50px rgba(0,0,0,.4),0 14px 0 rgba(0,0,0,.45)}
.redbox::before{background:radial-gradient(ellipse at 55% 50%,#fff 0%,#dff0ff 14%,rgba(60,150,255,.9) 36%,rgba(0,90,255,.35) 60%,rgba(0,60,255,0) 75%)}
.redbox::after{background:radial-gradient(ellipse at 30% 50%,#e8f4ff 0%,rgba(40,140,255,.85) 30%,rgba(0,60,255,0) 72%)}
.panel{box-shadow:0 0 0 7px #ffffff,0 0 30px 8px rgba(60,160,255,.85),0 0 80px 18px rgba(0,90,255,.4)}
.watch .brush{filter:drop-shadow(0 0 20px rgba(30,120,255,.9))}
.vs{box-shadow:0 0 0 6px #ffffff,0 0 34px 8px rgba(60,160,255,.85),0 20px 40px rgba(0,0,0,.7)}
.halo{background:radial-gradient(ellipse at center, rgba(255,150,40,.22), rgba(255,110,0,.08) 50%, rgba(255,80,0,0) 72%)}"""
else:
    glow = 'drop-shadow(0 0 0 #fff) drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 -5px 0 #fff) drop-shadow(0 0 8px #ffd000) drop-shadow(0 0 20px rgba(255,160,0,.85)) drop-shadow(0 0 44px rgba(255,90,0,.55))'
css = css.replace('PERSONGLOW', glow)
T = T.replace('</style>', css + '\n</style>')

def render(T):
    open('cover.html', 'w').write(T)
    info = run('node', 'render.js', os.path.abspath('cover.html'), os.path.abspath('cover.png'))
    m = run('python3', '04_face_metrics.py', 'cover.png', *map(str, box))
    return info.strip(), m.strip()

info, m = render(T)
# auto-tune face brightness toward L 57
for _ in range(3):
    L = float(m.split('face L ')[1].split(' ')[0])
    if 53 <= L <= 60: break
    nb = round(br * (57 / L) ** 1.3, 3)
    T = T.replace(f'filter:brightness({br})', f'filter:brightness({nb})'); br = nb
    info, m = render(T)
print(ID, info, '| brightness', br, '|', m, '| facebox', box)
