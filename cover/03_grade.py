"""Natural studio-style grade for the presenter cutout (used for v4-v10).
usage: python3 03_grade.py person.png person_natural.png [key_x key_y]
key_x,key_y = centre of the soft key light in cutout pixels (default 430,560 = just
above-left of the face in a 1080-wide cutout). Put it slightly above/left of the face."""
import numpy as np, cv2, sys
from PIL import Image
src,dst=sys.argv[1],sys.argv[2]
KX=float(sys.argv[3]) if len(sys.argv)>3 else 430; KY=float(sys.argv[4]) if len(sys.argv)>4 else 560
LIFT=float(sys.argv[5]) if len(sys.argv)>5 else 0.30  # lower for already-bright source frames
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
L=curve(L,lift=LIFT)
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
