"""Car-hero reel cover (no presenter): the car cut out large with a gold edge glow, floor reflection and the v2 headline.
usage: python3 build_car.py <ID>   reads <ID>/cfgcar.json:
 {"theme":"carbike","car":"car.png","bg":"bg.png","lines":[..],"box":[..], optional: car_w(1040), car_top(800),
  car_x(center), bg_blur(7), bg_bright(.9), bg_pos("center 40%"), car_filter, css}"""
import sys, os, json, subprocess, re
HERE = os.path.dirname(os.path.abspath(__file__)); ID = sys.argv[1]; D = os.path.join(HERE, ID)
C = json.load(open(os.path.join(D, 'cfgcar.json'))); os.chdir(D)
run = lambda *a: subprocess.run(a, check=True, capture_output=True, text=True).stdout
from PIL import Image
cw, ch = Image.open(C['car']).size
W = C.get('car_w', 1040); Hc = round(W * ch / cw); top = C.get('car_top', 800); left = C.get('car_x', (1080 - W) // 2)
bottom = top + Hc
T = dict(EDGE='#ffd23a', GLOW1='rgba(255,180,0,.75)', STKGLOW='rgba(255,170,0,.5)', BRUSH_W='brush_wide_b.png', BRUSH_D='brush_dense_b.png',
         BOXBG='linear-gradient(180deg,#1d1d1f 0%,#0b0b0c 55%,#19191b 100%)', BOXRIM='#fff3c4',
         BOXSHADOW='0 0 0 4px #ffb400,0 0 22px 6px rgba(255,180,0,1),0 0 64px 14px rgba(255,150,0,.5),inset 0 0 24px rgba(255,190,40,.4),0 14px 0 rgba(0,0,0,.45)')
tt = lambda t, c, w=None, mx=None: f'<span class="ln tt {c}"{f" data-w={w}" if w else ""}{f" data-max={mx}" if mx else ""} data-t="{t}">{t}</span>'
l1, l2 = C['lines']; b1, b2 = C['box']
head = (f'<div class="row r1">{tt(l1,"w",C.get("l1_w",860),C.get("l1_max",190))}</div>'
        f'<div class="row r2"><i class="stk"></i>{tt(l2,"y",C.get("l2_w",960),C.get("l2_max",300))}</div>'
        f'<div class="box"><div class="row first">{tt(b1,"w",C.get("b1_w",880),C.get("b_max",190))}</div>'
        f'<div class="row">{tt(b2,"y",C.get("b2_w",880),C.get("b_max",190))}</div></div>')
H = open('../cover_v2.html').read()
for cut in ['<div class="logo"><i></i><img src="logo.png"><i></i></div>', '<div class="watch"><div class="brush"></div><b>BANNERHTML</b></div>',
            '<div class="side"><img src="graphic.png"></div>', '<div class="pwrap"><img class="person" src="person_natural.png"></div>']:
    H = H.replace(cut, '')
H = H.replace("url(bg.png) center 40%/cover", f"url({C.get('bg','bg.png')}) {C.get('bg_pos','center 40%')}/cover")
rep = dict(BGBLUR=f"{C.get('bg_blur',7)}px", BGBRIGHT=str(C.get('bg_bright', .9)), HEADTOP=str(C.get('head_top', 60)), BOXW=str(C.get('box_w', 1010)),
           BOXPAD=C.get('box_pad', '30px 40px 34px'), HEADHTML=head, **T)
for k in sorted(rep, key=len, reverse=True): H = H.replace(k, rep[k])
car = C['car']
layers = (f'<div class="floor"></div><div class="halo"></div>'
          f'<img class="refl" src="{car}"><div class="contact"></div><img class="car" src="{car}"><div class="ground"></div>')
H = H.replace('<div class="head">', layers + '<div class="head">')
cf = C.get('car_filter', 'brightness(1.08) contrast(1.08) saturate(1.1)')
glow = C.get('glow_css', 'drop-shadow(0 0 1.5px #fff3c0) drop-shadow(0 0 4px rgba(255,205,60,.95)) drop-shadow(0 0 16px rgba(255,170,0,.65)) drop-shadow(0 0 42px rgba(255,130,0,.3))')
css = f"""
.shade{{background:linear-gradient(180deg,rgba(0,0,0,.80) 0%,rgba(0,0,0,.58) 22%,rgba(0,0,0,.20) 40%,rgba(0,0,0,.10) 58%,rgba(0,0,0,.30) 80%,rgba(0,0,0,.72) 100%)}}
.floor{{position:absolute;left:0;right:0;top:{bottom-140}px;bottom:0;background:linear-gradient(180deg,rgba(10,9,8,0) 0%,rgba(10,9,8,.2) 35%,rgba(8,7,6,.5) 100%)}}
.halo{{position:absolute;left:{left-60}px;width:{W+120}px;top:{top+Hc*.18:.0f}px;height:{Hc*.95:.0f}px;border-radius:50%;
  background:radial-gradient(ellipse at 50% 55%,rgba(255,214,120,.42) 0%,rgba(255,160,30,.22) 38%,rgba(255,140,0,0) 70%);filter:blur(20px)}}
.contact{{position:absolute;left:{left+W*.06:.0f}px;width:{W*.88:.0f}px;top:{bottom-70}px;height:110px;border-radius:50%;
  background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,.9) 0%,rgba(0,0,0,.6) 45%,rgba(0,0,0,0) 72%);filter:blur(8px)}}
.car{{position:absolute;left:{left}px;top:{top}px;width:{W}px;filter:{cf} {glow}}}
.refl{{position:absolute;left:{left}px;top:{bottom-6}px;width:{W}px;transform:scaleY(-1);opacity:{C.get('refl',.13)};filter:blur(3px) {cf};
  -webkit-mask-image:linear-gradient(0deg,#000 0%,rgba(0,0,0,.4) 60%,transparent 82%);mask-image:linear-gradient(0deg,#000 0%,rgba(0,0,0,.4) 60%,transparent 82%)}}
.ground{{position:absolute;left:{left+W*.04:.0f}px;width:{W*.92:.0f}px;top:{bottom-34}px;height:60px;border-radius:50%;
  background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,.75) 0%,rgba(0,0,0,.45) 50%,rgba(0,0,0,0) 75%);filter:blur(6px)}}
{C.get('css','')}"""
H = H.replace('</style>', css + '\n</style>')
open('covercar.html', 'w').write(H)
info = run('node', '../render.js', os.path.abspath('covercar.html'), os.path.abspath('covercar.png'))
print(ID, info.strip(), 'car', left, top, W, Hc, 'bottom', bottom)
