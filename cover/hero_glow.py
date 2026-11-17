import sys, cv2, numpy as np
from PIL import Image
src,dst=sys.argv[1],sys.argv[2]; gamma=float(sys.argv[3]) if len(sys.argv)>3 else 0.62
im=np.array(Image.open(src)).astype(np.float32)/255; rgb=im[...,:3]; a=im[...,3]
rgb=np.power(rgb,gamma)                                   # open shadows
b=cv2.GaussianBlur(rgb,(0,0),4); rgb=np.clip(rgb+0.8*(rgb-b),0,1)   # clarity
H,W=a.shape; yy,xx=np.mgrid[0:H,0:W]
sheen=np.clip(1-np.abs((xx/W*0.8+yy/H*0.6)-0.55)/0.18,0,1)**2*0.28  # diagonal showroom sheen
rgb=1-(1-rgb)*(1-sheen[...,None]*np.array([0.85,0.95,1.0]))
rgb=np.clip((rgb-0.5)*1.08+0.52,0,1)
# rim + halo (white-blue), faded near the floor
am=(a>0.5).astype(np.uint8)
edge=cv2.dilate(am,np.ones((7,7),np.uint8))-am
fade=np.clip((H*0.92-yy)/(H*0.3),0,1)
rim=cv2.GaussianBlur(edge.astype(np.float32),(0,0),2)*fade
pad=120; A=np.pad(a,pad); halo=cv2.GaussianBlur(A,(0,0),45)*1.1; halo=np.clip(halo,0,1)
F=np.pad(fade,pad,mode='edge'); halo*=F
out=np.zeros((H+2*pad,W+2*pad,4),np.float32)
col=np.array([0.80,0.93,1.0])
out[...,:3]=col; out[...,3]=halo*0.75
car=np.zeros_like(out); car[pad:pad+H,pad:pad+W,:3]=rgb; car[pad:pad+H,pad:pad+W,3]=a
R=np.zeros_like(out); R[pad:pad+H,pad:pad+W,:3]=1.0; R[pad:pad+H,pad:pad+W,3]=np.clip(rim*1.2,0,1)
def over(top,bot):
    ta=top[...,3:4]; ba=bot[...,3:4]; oa=ta+ba*(1-ta)
    oc=(top[...,:3]*ta+bot[...,:3]*ba*(1-ta))/np.maximum(oa,1e-6); return np.dstack([oc,oa])
res=over(R,over(car,out))
Image.fromarray((res*255).astype(np.uint8)).save(dst); print(dst,res.shape)
