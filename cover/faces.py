"""faces.py ID t1 t2 ... -> ID/faces.jpg (face crops with face width).
Run from the working folder that holds vids/<ID>.mp4, models/yunet.onnx and the per-reel folders."""
import sys,subprocess,cv2,numpy as np
from PIL import Image, ImageDraw
vid=sys.argv[1]; v=f'vids/{vid}.mp4'; ts=sys.argv[2:]
det=cv2.FaceDetectorYN.create('models/yunet.onnx','',(1080,1920),0.6); tiles=[]
for t in ts:
    png=subprocess.run(['ffmpeg','-v','error','-ss',t,'-i',v,'-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True).stdout
    a=cv2.imdecode(np.frombuffer(png,np.uint8),1); _,f=det.detect(a)
    if f is None: continue
    x,y,w,h=map(int,f[0][:4]); c=a[max(0,y-h):y+2*h, max(0,x-w):x+2*w]
    im=Image.fromarray(cv2.cvtColor(c,cv2.COLOR_BGR2RGB)).resize((300,300)); d=ImageDraw.Draw(im); d.rectangle((0,0,90,14),fill=0); d.text((3,2),f'{t}s w{w}',fill=(255,255,0)); tiles.append(im)
s=Image.new('RGB',(7*300,((len(tiles)+6)//7)*300))
for i,t in enumerate(tiles): s.paste(t,((i%7)*300,(i//7)*300))
s.save(f'{vid}/faces.jpg',quality=85)
