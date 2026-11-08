"""usage: clean.py in.png out.png thresh  -> drop faint alpha and keep only the largest solid piece"""
import sys, numpy as np, cv2
from PIL import Image
a=np.array(Image.open(sys.argv[1]).convert('RGBA')); t=int(sys.argv[3])
m=(a[...,3]>t).astype(np.uint8)
n,lab,st,_=cv2.connectedComponentsWithStats(m); k=1+np.argmax(st[1:,cv2.CC_STAT_AREA])
keep=cv2.dilate((lab==k).astype(np.uint8),np.ones((9,9),np.uint8))
keep=cv2.GaussianBlur(keep.astype(np.float32),(0,0),2)
a[...,3]=(a[...,3]*np.clip(keep,0,1)).astype(np.uint8)
im=Image.fromarray(a); im.crop(im.getbbox()).save(sys.argv[2]) if 'crop' in sys.argv else im.save(sys.argv[2])
