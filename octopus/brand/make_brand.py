# -*- coding: utf-8 -*-
"""Logo CISO Assistant by Octopus Lab (SVG jasne/ciemne, tekst zamieniony na krzywe) + favicon.
Kolory z octopus-lab.pl: tlo #0a0d1a, powierzchnia #141937, akcent #4f63ff, tekst #eaeefb, eyebrow #8294ff.
"""
import io, os, glob
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(D, "..", "..", "frontend", "static", "fonts")
MARK = open(os.path.join(D, "octopus_path.txt")).read()
MARK_W, MARK_H = 640, 489


def load(weight):
    fn = os.path.join(FONTS, f"sora-latin-{weight}-normal.woff2")
    tt = TTFont(fn)
    buf = io.BytesIO(); tt.flavor = None; tt.save(buf)
    data = buf.getvalue()
    face = hb.Face(data); font = hb.Font(face)
    return TTFont(io.BytesIO(data)), font, face.upem


def text_path(weight, text, size, x, y, tracking=0.0):
    tt, font, upem = load(weight)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    gs = tt.getGlyphSet(); order = tt.getGlyphOrder()
    sc = size / upem
    pen = SVGPathPen(gs)
    cx = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        tp = TransformPen(pen, (sc, 0, 0, -sc, x + (cx + pos.x_offset) * sc, y - pos.y_offset * sc))
        gs[name].draw(tp)
        cx += pos.x_advance + tracking * upem
    width = (cx - tracking * upem) * sc
    return pen.getCommands(), width


def logo(mark_col, title_col, tag_col):
    mh = 92
    ms = mh / MARK_H
    mw = MARK_W * ms
    tx = mw + 18
    t1, w1 = text_path(700, "CISO Assistant", 34, tx, 54)
    t2, w2 = text_path(600, "BY OCTOPUS LAB", 16.5, tx + 1, 85, tracking=0.16)
    W = round(tx + max(w1, w2) + 4)
    H = 100
    return W, H, f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<title>CISO Assistant by Octopus Lab</title>
<g transform="translate(0,4) scale({ms:.5f})"><path fill="{mark_col}" fill-rule="evenodd" d="{MARK}"/></g>
<path fill="{title_col}" d="{t1}"/>
<path fill="{tag_col}" d="{t2}"/>
</svg>
'''


def mark_only(bg, fg, size=512, pad=0.16, radius=0.22):
    inner = size * (1 - 2 * pad)
    s = inner / MARK_W
    h = MARK_H * s
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
<rect width="{size}" height="{size}" rx="{size*radius:.1f}" fill="{bg}"/>
<g transform="translate({size*pad:.2f},{(size-h)/2:.2f}) scale({s:.5f})"><path fill="{fg}" fill-rule="evenodd" d="{MARK}"/></g>
</svg>
'''


if __name__ == "__main__":
    out = os.path.join(D, "out"); os.makedirs(out, exist_ok=True)
    W, H, light = logo("#141937", "#141937", "#4f63ff")
    _, _, dark = logo("#ffffff", "#eaeefb", "#8294ff")
    open(os.path.join(out, "octopus-logo-light.svg"), "w").write(light)
    open(os.path.join(out, "octopus-logo-dark.svg"), "w").write(dark)
    icon = mark_only("#141937", "#ffffff")
    open(os.path.join(out, "octopus-mark.svg"), "w").write(icon)
    print("logo", W, "x", H)
    # favicon z renderu SVG (Chromium)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 512, "height": 512})
        pg.set_content(f'<html><body style="margin:0;background:transparent">{icon}</body></html>')
        png = pg.screenshot(omit_background=True, clip={"x": 0, "y": 0, "width": 512, "height": 512})
        # podglad logo na jasnym i ciemnym tle
        pg.set_viewport_size({"width": 900, "height": 300})
        pg.set_content(f'''<html><body style="margin:0;display:flex">
          <div style="background:#f6f7fc;padding:30px;width:390px">{light.replace(f'width="{W}" height="{H}"','width="260"')}</div>
          <div style="background:#0a0d1a;padding:30px;width:390px">{dark.replace(f'width="{W}" height="{H}"','width="260"')}</div>
          </body></html>''')
        pg.screenshot(path=os.path.join(out, "preview.png"))
        b.close()
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    im.save(os.path.join(out, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    im.resize((180, 180), Image.LANCZOS).save(os.path.join(out, "apple-touch-icon.png"))
    im.resize((192, 192), Image.LANCZOS).save(os.path.join(out, "favicon-192.png"))
    print("ok")
