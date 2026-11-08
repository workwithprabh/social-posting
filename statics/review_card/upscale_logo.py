"""Rebuild a flat one-colour logo's edges at a larger size (same shapes, crisp anti-aliased edges).
usage: python upscale_logo.py in.png out.png factor [white]"""
import sys, numpy as np
from PIL import Image, ImageFilter
src, dst, k = sys.argv[1], sys.argv[2], float(sys.argv[3])
im = Image.open(src).convert('RGBA'); w, h = im.size
a = im.getchannel('A').resize((round(w*k), round(h*k)), Image.BICUBIC).filter(ImageFilter.GaussianBlur(k*0.35))
a = np.array(a).astype(float) / 255
a = np.clip((a - 0.5) * 3.2 + 0.5, 0, 1)                      # steepen the edge back to a crisp, anti-aliased line
rgb = np.array(im.convert('RGB').resize(a.shape[::-1], Image.LANCZOS))
if len(sys.argv) > 4: rgb[:] = 255
Image.fromarray(np.dstack([rgb, (a*255).astype('uint8')]), 'RGBA').save(dst); print(dst, a.shape[::-1])
