"""Give a cut-out car its REAL floor shadow (user, 17 Nov 2026: drawn ellipses under the tyres looked "very fake").
Works with studio photos on a light floor (e.g. hyundai.com/in gallery shots): the shadow is how much darker the floor
is than the studio white, kept only below the car's mid-height and outside the car. It is laid over the glow halo but
under the car. usage:
  python3 hero_studio_shadow.py studio.jpg car_cut.png car_glow.png out.png [scale=2]
car_cut.png = rembg cut-out of the studio photo upscaled by `scale` and cropped to its bbox; car_glow.png = hero_glow.py
output of car_cut.png (pad 120). Prints the size and the lowest tyre row so the template floor `gy` can sit above the
rear tyres. For reel frames on a real floor, keep the reel's own floor instead of cutting the car out."""
import sys, json, numpy as np, cv2
from PIL import Image
from rembg import remove, new_session
src,cutp,glowp,dst=sys.argv[1:5]; k=int(sys.argv[5]) if len(sys.argv)>5 else 2
im=Image.open(src).convert('RGB'); im=im.resize((im.width*k,im.height*k),Image.LANCZOS)
al=np.array(remove(im,session=new_session('isnet-general-use')))[...,3].astype(np.float32)/255
bx=Image.fromarray((al*255).astype(np.uint8)).getbbox()
L=np.array(im).astype(np.float32).mean(axis=2); white=np.percentile(L[:60,:],90)
sh=np.clip((white-L)/white*1.25,0,1); sh[al>0.35]=0
ys,xs=np.where(al>0.5); sh[:int(ys.min()+(ys.max()-ys.min())*0.55),:]=0; sh=cv2.GaussianBlur(sh,(0,0),1.2)*0.9
glow=np.array(Image.open(glowp)).astype(np.float32)/255; cut=np.array(Image.open(cutp)).astype(np.float32)/255
pad=120; H,W=cut.shape[:2]; oh=glow.shape[0]+160
S=np.zeros((oh,glow.shape[1]),np.float32); ox,oy=pad-bx[0],pad-bx[1]
sy0,sx0=max(0,-oy),max(0,-ox); y0,x0=max(0,oy),max(0,ox)
h=min(sh.shape[0]-sy0,oh-y0); w=min(sh.shape[1]-sx0,glow.shape[1]-x0); S[y0:y0+h,x0:x0+w]=sh[sy0:sy0+h,sx0:sx0+w]
G=np.zeros((oh,glow.shape[1],4),np.float32); G[:glow.shape[0]]=glow
ca=np.zeros((oh,glow.shape[1]),np.float32); ca[pad:pad+H,pad:pad+W]=cut[...,3]; s_=S*(1-ca)
rgb=G[...,:3]*G[...,3:4]; a=G[...,3]; rgb=rgb*(1-s_[...,None]); a=a+s_*(1-a)
Image.fromarray((np.clip(np.dstack([rgb/np.maximum(a[...,None],1e-6),a]),0,1)*255).astype(np.uint8)).save(dst)
m=cut[...,3]>0.5; low=max(np.max(np.where(m[:,x])[0]) for x in range(W) if m[:,x].any())
print(json.dumps({'width':glow.shape[1],'height':oh,'lowest_tyre_y':pad+int(low)}))
