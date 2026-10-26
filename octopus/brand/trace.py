import os
import numpy as np, potrace
HERE = os.path.dirname(os.path.abspath(__file__))
from PIL import Image, ImageFilter
im = Image.open(os.path.join(HERE, 'logo_ink.png')).convert('RGBA')
a = im.split()[3]
S = 4
a = a.resize((a.width*S, a.height*S), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2))
bm = np.array(a) <= 128
path = potrace.Bitmap(bm).trace(turdsize=20, alphamax=1.0, opticurve=True, opttolerance=0.2)
def f(v): return f"{v/S:.2f}"
parts=[]
for curve in path:
    sp = curve.start_point
    d = [f"M{f(sp.x)},{f(sp.y)}"]
    for seg in curve.segments:
        if seg.is_corner:
            d.append(f"L{f(seg.c.x)},{f(seg.c.y)}L{f(seg.end_point.x)},{f(seg.end_point.y)}")
        else:
            d.append(f"C{f(seg.c1.x)},{f(seg.c1.y)} {f(seg.c2.x)},{f(seg.c2.y)} {f(seg.end_point.x)},{f(seg.end_point.y)}")
    d.append("Z")
    parts.append("".join(d))
D = "".join(parts)
open(os.path.join(HERE, 'octopus_path.txt'),'w').write(D)
print(len(path), 'curves', len(D), 'chars', im.size)
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {im.width} {im.height}"><path fill="#26213F" fill-rule="evenodd" d="{D}"/></svg>'
open(os.path.join(HERE, 'octopus_mark.svg'),'w').write(svg)
