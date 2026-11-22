"""Rótulo de GLiCor como en la cabecera de la web (index.html y glossary.css): «[GLiCor]» en
JetBrains Mono (800; corchetes en 500), sobre el fondo #1e1b4b con sus dos degradados."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = sys.argv[1]   # carpeta con JetBrainsMono-ExtraBold.ttf y JetBrainsMono-Medium.ttf
S = 4; size = 96*S
fb = ImageFont.truetype(f"{F}/JetBrainsMono-ExtraBold.ttf", size); fm = ImageFont.truetype(f"{F}/JetBrainsMono-Medium.ttf", size)
parts = [("[", fm, "#6366f1"), ("G", fb, "#ffffff"), ("Li", fb, "#e3a9f2"), ("Cor", fb, "#f43f5e"), ("]", fm, "#6366f1")]
track = -0.04*size
widths = [d.getlength(t) for t, d, _ in parts]
W, H = int(sum(widths) + track*(sum(len(t) for t,_,_ in parts)-1) + 0.3*size + 120*S), int(size*1.0 + 110*S)
bg = Image.new("RGB", (W, H), "#1e1b4b")
glow = Image.new("RGBA", (W, H), (0,0,0,0)); g = ImageDraw.Draw(glow)
g.ellipse((-W*0.5, -H*0.9, W*0.5, H*0.9), fill=(99,102,241,38)); g.ellipse((W*0.5, H*0.1, W*1.5, H*1.9), fill=(244,63,94,26))
bg = Image.alpha_composite(bg.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(60*S)))
d = ImageDraw.Draw(bg); x = 60*S; y = (H - size)//2 - int(0.12*size)
for (t, f, c) in parts:
    for ch in t:
        d.text((x, y), ch, font=f, fill=c); x += f.getlength(ch) + track
    if t == "]":   # cursor tras el corchete de cierre, como en la web
        cw = 0.08*size; x += 0.08*size - track
        d.rectangle((x, y + 0.2*size, x + cw, y + 1.0*size), fill="#f43f5e"); x += cw + 0.06*size
mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rounded_rectangle((0,0,W,H), radius=28*S, fill=255)
out = Image.new("RGBA", (W, H), (0,0,0,0)); out.paste(bg, (0,0), mask)
out = out.resize((W//S*2//2, H//S*2//2), Image.LANCZOS); out.save("figuras/logos/glicor.png")
print(out.size)
