"""Skin tone readout: median Lab of cheeks+forehead (L 0-100, a/b centred at 0), chroma, hue angle."""
import sys, numpy as np, cv2, mediapipe as mp
from PIL import Image
from mediapipe.tasks.python import vision, BaseOptions
LM = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path='models/face_landmarker.task'), num_faces=1))
REG = [[116,117,118,100,126,142],[345,346,347,329,355,371],[10,109,67,338,297,151]]
def skin(path):
    rgb = np.array(Image.open(path).convert('RGB')); h, w = rgb.shape[:2]
    r = LM.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb)))
    P = np.array([(p.x*w, p.y*h) for p in r.face_landmarks[0]])
    m = np.zeros((h,w),np.uint8)
    for ids in REG: cv2.fillPoly(m,[cv2.convexHull(P[ids].astype(np.int32))],1)
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(float)[m==1]
    L = lab[:,0]*100/255; a = lab[:,1]-128; b = lab[:,2]-128
    return dict(L=np.median(L), a=np.median(a), b=np.median(b), chroma=np.median(np.hypot(a,b)), hue=np.degrees(np.arctan2(np.median(b),np.median(a))), Lspread=np.percentile(L,90)-np.percentile(L,10))
if __name__=='__main__':
    for f in sys.argv[1:]:
        d = skin(f); print(f'{f:42s}', ' '.join(f'{k} {v:5.1f}' for k,v in d.items()))
