"""Cut the presenter out of a full-res frame and fade off the bottom (removes burnt-in subtitles).
usage: python3 02_cutout.py frame.png person.png [fade_start=1240] [fade_end=1400]
Model: rembg isnet-general-use (downloads ~180MB from GitHub on first run)."""
import sys, numpy as np
from PIL import Image
from rembg import remove, new_session
src,dst=sys.argv[1],sys.argv[2]
y0=int(sys.argv[3]) if len(sys.argv)>3 else 1240; y1=int(sys.argv[4]) if len(sys.argv)>4 else 1400
out=remove(Image.open(src),session=new_session('isnet-general-use'))
a=np.array(out.convert('RGBA')); H=a.shape[0]
fade=np.ones(H); fade[y0:y1]=np.linspace(1,0,y1-y0); fade[y1:]=0
a[...,3]=(a[...,3]*fade[:,None]).astype('uint8')
Image.fromarray(a).crop((0,0,a.shape[1],y1)).save(dst); print('saved',dst)
