"""Ground a cut-out car so it stands on the floor (user, 17 Nov 2026: covers looked like the car was flying).
Finds every tyre contact (local lows of the car's bottom outline: in a 3/4 view the near AND far wheels), fills the
footprint between them with a soft dark shadow, and adds a tight contact shadow under each tyre. The shadow is drawn
over the glow halo but under the car. usage: ground.py car_glow.png car_cut.png out.png  (glow made with pad 120)
Prints the contact points in output px; put the floor's horizon above the highest one."""
import sys, json, numpy as np, cv2
from PIL import Image
glow=np.array(Image.open(sys.argv[1])).astype(np.float32)/255
cut=np.array(Image.open(sys.argv[2])).astype(np.float32)/255
pad=120; H,W=cut.shape[:2]; a=cut[...,3]>0.5
low=np.array([np.max(np.where(a[:,x])[0]) if a[:,x].any() else -1 for x in range(W)])
peaks=[]
for x in range(40,W-40,4):
    w=low[x-40:x+41]
    if low[x]==w.max() and low[x]>0 and (not peaks or x-peaks[-1][0]>120): peaks.append((x,int(low[x])))
P=[(pad+x,pad+y) for x,y in peaks]
out=np.zeros((glow.shape[0]+int(H*0.08),glow.shape[1],4),np.float32)
sh=np.zeros(out.shape[:2],np.float32)
if len(P)>=3:
    hull=cv2.convexHull(np.array(P,np.int32)); cv2.fillPoly(sh,[hull],0.8)
    sh=cv2.GaussianBlur(sh,(0,0),14)
c=np.zeros_like(sh); ys=[p[1] for p in P]; ymin,ymax=min(ys),max(ys)
for x,y in P:
    near=(y-ymin)/max(1,ymax-ymin)                    # nearer wheels are lower and bigger
    cv2.ellipse(c,(x,y+3),(int(55+45*near),int(9+5*near)),0,0,360,1.0,-1)
c=cv2.GaussianBlur(c,(0,0),6)
s=np.clip(sh+c*0.95,0,0.95)
G=np.zeros_like(out); G[:glow.shape[0]]=glow
ca=np.zeros(out.shape[:2],np.float32); ca[pad:pad+H,pad:pad+W]=cut[...,3]
s_=s*(1-ca)
rgb=G[...,:3]*G[...,3:4]; al=G[...,3]; rgb=rgb*(1-s_[...,None]); al=al+s_*(1-al)
res=np.dstack([rgb/np.maximum(al[...,None],1e-6),al])
Image.fromarray((np.clip(res,0,1)*255).astype(np.uint8)).save(sys.argv[3])
print(json.dumps({'width':res.shape[1],'height':res.shape[0],'contacts':P,'highest_contact_y':ymin}))
