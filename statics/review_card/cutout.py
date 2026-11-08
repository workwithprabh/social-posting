"""Cut a customer (and their car) out of a review photo for a photo review card.

usage: python cutout.py photo.jpg out.png [--plate x0 y0 x1 y1] [--erase x0 y0 x1 y1 ...] [--crop-right X]
- keeps only the largest solid piece (drops stray background bits)
- --plate pixelates the number plate (pixel box in the original photo); always do this when a plate is readable
- --erase clears leftovers that touch the subject (box in the original photo, repeatable)
- --crop-right cuts the subject at X (original-photo pixels) so it can bleed off the card's right edge
Model: rembg isnet-general-use (pip install rembg==2.0.86 onnxruntime opencv-python-headless).
Only for reviews whose "Photo OK?" column is Yes (the customer agreed).
"""
import argparse
import numpy as np, cv2
from PIL import Image
from rembg import remove, new_session

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('dst')
ap.add_argument('--plate', nargs=4, type=int)
ap.add_argument('--erase', nargs=4, type=int, action='append', default=[])
ap.add_argument('--crop-right', type=int)
a = ap.parse_args()
img = Image.open(a.src).convert('RGB')
px = np.array(remove(img, session=new_session('isnet-general-use')).convert('RGBA'))
for x0, y0, x1, y1 in a.erase:
    px[y0:y1, x0:x1, 3] = 0
n, lab, stats, _ = cv2.connectedComponentsWithStats((px[..., 3] > 30).astype('uint8'), 8)
px[lab != 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA]), 3] = 0
if a.plate:
    x0, y0, x1, y1 = a.plate
    blk = Image.fromarray(px[y0:y1, x0:x1, :3]); w, h = blk.size
    px[y0:y1, x0:x1, :3] = np.array(blk.resize((max(1, w // 45), max(1, h // 45)), Image.BILINEAR).resize((w, h), Image.NEAREST))
out = Image.fromarray(px)
bb = out.getchannel('A').point(lambda v: 255 if v > 30 else 0).getbbox()
out.crop((bb[0], bb[1], a.crop_right or bb[2], bb[3])).save(a.dst)
print('saved', a.dst, out.size)
