"""Measure presenter face lighting on a finished cover (or reference screenshot).
usage: python3 04_face_metrics.py cover.png x0 y0 x1 y1   (box = face skin, forehead to chin)
Targets learned from the Mahindra Arav feed (L* scale 0-100):
  face brightness 52-60 | top-10% highlights 80-88 | contrast 20-25 | warmth (b*) 16-20 | face minus surroundings +9..+20"""
import sys, numpy as np, cv2
from PIL import Image
im=np.array(Image.open(sys.argv[1]).convert('RGB')); x0,y0,x1,y1=map(int,sys.argv[2:6])
face=im[y0:y1,x0:x1]; ycc=cv2.cvtColor(face,cv2.COLOR_RGB2YCrCb)
m=(ycc[...,1]>133)&(ycc[...,1]<180)&(ycc[...,2]>77)&(ycc[...,2]<135)
lab=cv2.cvtColor(face,cv2.COLOR_RGB2LAB).astype(float); L=lab[...,0]*100/255; B=lab[...,2]-128
w,h=x1-x0,y1-y0; X0,Y0=max(0,x0-w),max(0,y0-h); X1,Y1=min(im.shape[1],x1+w),min(im.shape[0],y1+h)
R=cv2.cvtColor(im[Y0:Y1,X0:X1],cv2.COLOR_RGB2LAB)[...,0].astype(float)*100/255
rm=np.ones(R.shape,bool); rm[y0-Y0:y1-Y0,x0-X0:x1-X0]=False
print(f"face L {L[m].mean():.1f} | highlights {np.percentile(L[m],90):.1f} | contrast {L[m].std():.1f} | warmth {B[m].mean():.1f} | vs surroundings {L[m].mean()-R[rm].mean():+.1f}")
