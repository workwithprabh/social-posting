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
