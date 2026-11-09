"""emo.py ID emotion [n=12] [step=0.2] -> ID/emo_<emotion>.jpg: the frames whose presenter face best shows the emotion.
emotions: neutral happiness surprise sadness anger disgust fear contempt (FER+ model). Faces narrower than 90px are skipped."""
import sys, subprocess, numpy as np, cv2, onnxruntime as ort, json
from PIL import Image, ImageDraw
E=['neutral','happiness','surprise','sadness','anger','disgust','fear','contempt']
vid,emo=sys.argv[1],sys.argv[2]; n=int(sys.argv[3]) if len(sys.argv)>3 else 12; step=float(sys.argv[4]) if len(sys.argv)>4 else .2
v=f'vids/{vid}.mp4'
raw=subprocess.run(['ffmpeg','-v','error','-i',v,'-vf',f'fps={1/step}','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
fr=np.frombuffer(raw,np.uint8).reshape(-1,1920,1080,3)
det=cv2.FaceDetectorYN.create('models/yunet.onnx','',(1080,1920),0.7); sess=ort.InferenceSession('models/ferplus.onnx')
rows=[]
for i,f in enumerate(fr):
    _,fs=det.detect(f)
    if fs is None: continue
    x,y,w,h=map(int,fs[0][:4]); 
    if w<90: continue
    cx,cy,s=x+w//2,y+h//2,int(max(w,h)*1.15)
    c=cv2.cvtColor(f[max(0,cy-s//2):cy+s//2,max(0,cx-s//2):cx+s//2],cv2.COLOR_BGR2GRAY)
    if c.size==0: continue
    p=sess.run(None,{'Input3':cv2.resize(c,(64,64)).astype(np.float32)[None,None]})[0][0]; p=np.exp(p-p.max()); p/=p.sum()
    sharp=cv2.Laplacian(cv2.resize(c,(128,128)),cv2.CV_64F).var()
    rows.append(dict(i=i,t=round((i+.5)*step,2),w=w,sharp=sharp,**{e:float(p[k]) for k,e in enumerate(E)}))
print('frames',len(fr),'faces',len(rows));json.dump(rows,open(f'{vid}/emo.json','w'))
med=np.median([r['sharp'] for r in rows]) if rows else 0
cand=sorted([r for r in rows if r['sharp']>.5*med],key=lambda r:-r[emo])
pick=[];
for r in cand:  # keep picks at least 0.6s apart
    if all(abs(r['t']-q['t'])>=.6 for q in pick): pick.append(r)
    if len(pick)==n: break
tiles=[]
for r in pick:
    f=fr[r['i']]; _,fs=det.detect(f); x,y,w,h=map(int,fs[0][:4])
    c=f[max(0,y-h):y+2*h,max(0,x-w):x+2*w]; im=Image.fromarray(cv2.cvtColor(c,cv2.COLOR_BGR2RGB)).resize((300,300))
    d=ImageDraw.Draw(im); d.rectangle((0,0,170,14),fill=0); d.text((3,2),f"{r['t']}s {emo[:5]} {r[emo]:.2f}",fill=(255,255,0)); tiles.append(im)
s=Image.new('RGB',(6*300,((len(tiles)+5)//6)*300))
for i,t in enumerate(tiles): s.paste(t,((i%6)*300,(i//6)*300))
s.save(f'{vid}/emo_{emo}.jpg',quality=85)
print(vid,emo,[(r['t'],round(r[emo],2)) for r in pick])
