"""Shared palette and SVG helpers: Miles Morales graffiti on black."""
import math
import random
from xml.sax.saxutils import escape

INK = "#09090c"
INK2 = "#15080b"
RED = "#e8132f"
HOT = "#ff2d55"
BLOOD = "#7a0818"
BLUE = "#2f6bff"
YELLOW = "#ffe14a"
WHITE = "#f5f2f0"
MUTED = "#a39a9e"

IMPACT = "Impact, 'Haettenschweiler', 'Arial Narrow Bold', 'Arial Black', sans-serif"
SANS = "-apple-system, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

esc = escape


def svg(w, h, body, title, extra_defs="", style=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<defs>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .07 0"/>
  </filter>
  <filter id="rough" x="-5%" y="-20%" width="110%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="3" seed="4"/>
    <feDisplacementMap in="SourceGraphic" scale="14"/>
  </filter>
  <pattern id="halftone" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(20)">
    <circle cx="6" cy="6" r="1.9" fill="{RED}"/>
  </pattern>
  <clipPath id="frame"><rect width="{w}" height="{h}" rx="16"/></clipPath>
  {extra_defs}
  <style>{style}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>
</defs>
<g clip-path="url(#frame)">
{body}
<rect width="{w}" height="{h}" filter="url(#grain)"/>
</g>
</svg>
"""


def backdrop(w, h, glow=(0.85, 0.3)):
    gx, gy = glow
    return f"""<defs><radialGradient id="glow" cx="{gx}" cy="{gy}" r=".75">
  <stop offset="0" stop-color="{BLOOD}" stop-opacity=".85"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/>
</radialGradient></defs>
<rect width="{w}" height="{h}" fill="{INK}"/>
<rect width="{w}" height="{h}" fill="url(#glow)"/>"""


def splatter(cx, cy, size, seed, color=RED, opacity=0.9):
    """Spray-paint blot: a core, satellite droplets and a few drips."""
    rnd = random.Random(seed)
    out = [f'<g fill="{color}" opacity="{opacity}">']
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{size * .55:.1f}"/>')
    for _ in range(int(size * .9)):
        a = rnd.uniform(0, 2 * math.pi)
        d = size * rnd.uniform(.35, 1.6) ** 1.4
        r = max(.8, size * .2 * rnd.random() ** 2.2)
        out.append(f'<circle cx="{cx + math.cos(a) * d:.1f}" cy="{cy + math.sin(a) * d:.1f}" r="{r:.1f}"/>')
    for _ in range(rnd.randint(2, 4)):
        x = cx + rnd.uniform(-size * .45, size * .45)
        length = rnd.uniform(size * .6, size * 2.2)
        wd = rnd.uniform(2, 5)
        out.append(f'<rect x="{x:.1f}" y="{cy:.1f}" width="{wd:.1f}" height="{length:.1f}" rx="{wd / 2:.1f}"/>')
        out.append(f'<circle cx="{x + wd / 2:.1f}" cy="{cy + length:.1f}" r="{wd * .9:.1f}"/>')
    out.append("</g>")
    return "\n".join(out)


def swoosh(x, y, w, h, color=RED, opacity=1):
    """Thick spray-paint brush stroke, roughened."""
    return (f'<path filter="url(#rough)" opacity="{opacity}" fill="{color}" d="M{x} {y + h * .6} '
            f'C{x + w * .25} {y - h * .1} {x + w * .7} {y + h * .15} {x + w} {y} '
            f'L{x + w * .98} {y + h * .55} C{x + w * .7} {y + h * .75} {x + w * .3} {y + h * .6} {x + 6} {y + h} Z"/>')


def spider(cx, cy, s, color, opacity=1):
    """Generic spider glyph."""
    legs = []
    for side in (-1, 1):
        for i, (ang, bend) in enumerate([(-60, -20), (-25, -5), (15, 20), (50, 40)]):
            a = math.radians(ang)
            x1 = cx + side * s * .18
            y1 = cy - s * .05 + i * s * .06
            x2 = cx + side * s * (.55 + .1 * math.cos(a))
            y2 = cy + s * .55 * math.sin(a) - s * .1
            x3 = cx + side * s * (.7 + .05 * i)
            y3 = y2 + s * (bend / 100 + .25)
            legs.append(f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f} L{x3:.1f} {y3:.1f}"/>')
    return (f'<g opacity="{opacity}" fill="{color}" stroke="{color}" stroke-width="{s * .045:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round">'
            f'<g fill="none">{"".join(legs)}</g>'
            f'<ellipse cx="{cx}" cy="{cy - s * .12:.1f}" rx="{s * .11:.1f}" ry="{s * .15:.1f}"/>'
            f'<ellipse cx="{cx}" cy="{cy + s * .22:.1f}" rx="{s * .15:.1f}" ry="{s * .26:.1f}"/>'
            f'<circle cx="{cx}" cy="{cy - s * .32:.1f}" r="{s * .08:.1f}"/></g>')


def web(cx, cy, radius, start, end, spokes=6, rings=5, color=WHITE, opacity=.14):
    """Corner cobweb: spokes between start/end angles (degrees) with sagging rings."""
    angs = [math.radians(start + (end - start) * i / (spokes - 1)) for i in range(spokes)]
    out = [f'<g fill="none" stroke="{color}" stroke-opacity="{opacity}" stroke-width="1.2">']
    for a in angs:
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + math.cos(a) * radius:.1f}" y2="{cy + math.sin(a) * radius:.1f}"/>')
    for k in range(1, rings + 1):
        r = radius * k / (rings + .5)
        pts = [(cx + math.cos(a) * r, cy + math.sin(a) * r) for a in angs]
        d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
        for (x0, y0), (x1, y1), a0, a1 in zip(pts, pts[1:], angs, angs[1:]):
            mid = (a0 + a1) / 2
            qx, qy = cx + math.cos(mid) * r * .82, cy + math.sin(mid) * r * .82
            d += f" Q{qx:.1f} {qy:.1f} {x1:.1f} {y1:.1f}"
        out.append(f'<path d="{d}"/>')
    out.append("</g>")
    return "\n".join(out)


def chip(x, y, label, size=17, fg=WHITE, bg="#24151a", stroke="#3d2228"):
    w = len(label) * size * .62 + 22
    return (f'<g><rect x="{x}" y="{y}" width="{w:.0f}" height="{size + 16}" rx="{(size + 16) / 2}" fill="{bg}" stroke="{stroke}"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + size + 4}" text-anchor="middle" fill="{fg}" '
            f'style="font:600 {size}px {MONO}">{esc(label)}</text></g>'), w
