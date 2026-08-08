#!/usr/bin/env python3
"""Generate a custom animated knowledge-graph hero banner for the profile README."""
import math, random, sys

W, H = 1200, 340
random.seed(7)

# --- node placement -----------------------------------------------------
# Keep the centre band (where the name sits) sparse so text stays legible.
TEXT_BOX = (250, 105, 950, 245)  # x0,y0,x1,y1


def in_text_box(x, y, pad=18):
    x0, y0, x1, y1 = TEXT_BOX
    return (x0 - pad) < x < (x1 + pad) and (y0 - pad) < y < (y1 + pad)


nodes = []
attempts = 0
while len(nodes) < 40 and attempts < 6000:
    attempts += 1
    x = random.uniform(24, W - 24)
    y = random.uniform(22, H - 22)
    if in_text_box(x, y):
        continue
    if any((x - nx) ** 2 + (y - ny) ** 2 < 62 ** 2 for nx, ny, _ in nodes):
        continue
    r = random.choice([2.0, 2.4, 2.8, 3.4, 4.2, 5.2])
    nodes.append((round(x, 1), round(y, 1), r))

# --- edges: connect each node to its 2 nearest neighbours ---------------
edges = set()
for i, (x, y, _) in enumerate(nodes):
    d = sorted(
        ((math.dist((x, y), (nx, ny)), j) for j, (nx, ny, _) in enumerate(nodes) if j != i)
    )
    for dist, j in d[:2]:
        if dist < 210:
            edges.add(tuple(sorted((i, j))))
edges = sorted(edges)

PALETTE = ["#7aa2f7", "#bb9af7", "#2ac3de", "#9ece6a"]

out = []
A = out.append

A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  'font-family="ui-monospace, SFMono-Regular, Menlo, monospace" role="img" '
  'aria-label="Vaibhav Dangaich — AI agents, knowledge graphs, full-stack">')

# ---------------------------------------------------------------- defs
A('<defs>')
A('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
  '<stop offset="0%" stop-color="#0b0d17"/>'
  '<stop offset="55%" stop-color="#12141f"/>'
  '<stop offset="100%" stop-color="#1a1b2e"/></linearGradient>')

# animated sheen used to fill the name
A('<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">'
  '<stop offset="0%"   stop-color="#7aa2f7"/>'
  '<stop offset="35%"  stop-color="#e8eaff"/>'
  '<stop offset="50%"  stop-color="#ffffff"/>'
  '<stop offset="65%"  stop-color="#e8eaff"/>'
  '<stop offset="100%" stop-color="#bb9af7"/>'
  '<animateTransform attributeName="gradientTransform" type="translate" '
  'values="-1 0; 1 0; -1 0" dur="7s" repeatCount="indefinite"/>'
  '</linearGradient>')

A('<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
  '<stop offset="0%" stop-color="#7aa2f7" stop-opacity="0"/>'
  '<stop offset="50%" stop-color="#7aa2f7" stop-opacity=".9"/>'
  '<stop offset="100%" stop-color="#bb9af7" stop-opacity="0"/></linearGradient>')

A('<radialGradient id="vignette" cx="50%" cy="50%" r="52%">'
  '<stop offset="0%" stop-color="#0b0d17" stop-opacity=".92"/>'
  '<stop offset="70%" stop-color="#0b0d17" stop-opacity=".55"/>'
  '<stop offset="100%" stop-color="#0b0d17" stop-opacity="0"/></radialGradient>')

A('<filter id="glow" x="-80%" y="-80%" width="260%" height="260%">'
  '<feGaussianBlur stdDeviation="3.2" result="b"/>'
  '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
A('<filter id="softglow" x="-60%" y="-60%" width="220%" height="220%">'
  '<feGaussianBlur stdDeviation="7" result="b"/>'
  '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
A('<filter id="blur60"><feGaussianBlur stdDeviation="60"/></filter>')

A('<clipPath id="frame"><rect x="0" y="0" width="%d" height="%d" rx="18"/></clipPath>' % (W, H))
A('<clipPath id="typeclip"><rect x="390" y="222" width="422" height="30">'
  '<animate attributeName="width" values="0;0;422" keyTimes="0;0.14;1" '
  'dur="3.2s" fill="freeze"/></rect></clipPath>')
A('</defs>')

# ---------------------------------------------------------------- style
A('<style>'
  '.n{transform-box:fill-box;transform-origin:center;}'
  '@keyframes pulse{0%,100%{opacity:.35;transform:scale(.85)}50%{opacity:1;transform:scale(1.25)}}'
  '@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(0,-9px)}}'
  '@keyframes aurora1{0%,100%{transform:translate(0,0)}50%{transform:translate(120px,40px)}}'
  '@keyframes aurora2{0%,100%{transform:translate(0,0)}50%{transform:translate(-140px,-30px)}}'
  '@keyframes aurora3{0%,100%{transform:translate(0,0)}50%{transform:translate(60px,-60px)}}'
  '@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}'
  '@keyframes scan{0%{transform:translateY(-40px)}100%{transform:translateY(380px)}}'
  '@keyframes fadein{0%{opacity:0;transform:translateY(8px)}100%{opacity:1;transform:translateY(0)}}'
  '.cursor{animation:blink 1s step-end infinite}'
  '.scanline{animation:scan 6s linear infinite}'
  '.tag{animation:fadein .9s ease-out both}'
  '</style>')

A('<g clip-path="url(#frame)">')
A(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

# aurora blobs
A('<g filter="url(#blur60)" opacity=".55">')
A('<ellipse cx="180" cy="80"  rx="190" ry="120" fill="#7aa2f7" opacity=".38" '
  'style="animation:aurora1 16s ease-in-out infinite"/>')
A('<ellipse cx="1010" cy="270" rx="210" ry="130" fill="#bb9af7" opacity=".34" '
  'style="animation:aurora2 19s ease-in-out infinite"/>')
A('<ellipse cx="620" cy="20"  rx="230" ry="90"  fill="#2ac3de" opacity=".20" '
  'style="animation:aurora3 22s ease-in-out infinite"/>')
A('</g>')

# faint grid
A('<g stroke="#7aa2f7" stroke-width=".5" opacity=".07">')
for gx in range(0, W + 1, 40):
    A(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}"/>')
for gy in range(0, H + 1, 40):
    A(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}"/>')
A('</g>')

# ---------------------------------------------------------------- graph
A('<g opacity=".9">')
A('<g stroke-linecap="round">')
for k, (i, j) in enumerate(edges):
    x1, y1, _ = nodes[i]
    x2, y2, _ = nodes[j]
    col = PALETTE[k % len(PALETTE)]
    A(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="1" '
      f'opacity=".22"><animate attributeName="opacity" values=".10;.42;.10" '
      f'dur="{4 + (k % 7) * 0.6:.1f}s" begin="{(k % 11) * 0.4:.1f}s" repeatCount="indefinite"/></line>')
A('</g>')

# travelling packets along a subset of edges
for k, (i, j) in enumerate(edges):
    if k % 3:
        continue
    x1, y1, _ = nodes[i]
    x2, y2, _ = nodes[j]
    col = PALETTE[(k + 1) % len(PALETTE)]
    dur = 2.6 + (k % 9) * 0.45
    A(f'<circle r="2.1" fill="{col}" filter="url(#glow)" opacity=".95">'
      f'<animateMotion dur="{dur:.1f}s" begin="{(k % 13) * 0.5:.1f}s" repeatCount="indefinite" '
      f'path="M{x1} {y1} L{x2} {y2}"/>'
      f'<animate attributeName="opacity" values="0;1;1;0" dur="{dur:.1f}s" '
      f'begin="{(k % 13) * 0.5:.1f}s" repeatCount="indefinite"/></circle>')

# nodes
for k, (x, y, r) in enumerate(nodes):
    col = PALETTE[k % len(PALETTE)]
    A(f'<g style="animation:drift {9 + (k % 6)}s ease-in-out infinite;animation-delay:{(k%9)*.4:.1f}s">'
      f'<circle class="n" cx="{x}" cy="{y}" r="{r}" fill="{col}" filter="url(#glow)" '
      f'style="animation:pulse {3 + (k % 5) * 0.7:.1f}s ease-in-out infinite;'
      f'animation-delay:{(k % 8) * 0.45:.1f}s"/></g>')
A('</g>')

# vignette so the wordmark stays crisp
A(f'<ellipse cx="600" cy="172" rx="470" ry="140" fill="url(#vignette)"/>')

# ---------------------------------------------------------------- wordmark
A('<text x="600" y="150" text-anchor="middle" font-size="66" font-weight="700" '
  'letter-spacing="8" fill="url(#sheen)" filter="url(#softglow)">VAIBHAV DANGAICH</text>')

A('<rect x="300" y="171" width="600" height="1.5" fill="url(#rule)"/>')

A('<text x="600" y="198" text-anchor="middle" font-size="13" letter-spacing="4.2" '
  'fill="#7aa2f7" opacity=".9">AI AGENTS &#160;&#183;&#160; KNOWLEDGE GRAPHS &#160;&#183;&#160; '
  'FULL-STACK</text>')

# typed line
A('<g clip-path="url(#typeclip)">'
  '<text x="390" y="244" font-size="15" fill="#9ece6a">'
  '<tspan fill="#565f89">~ $ </tspan>build --something-that-outlives-the-session'
  '</text></g>')
A('<rect class="cursor" x="812" y="232" width="8" height="15" fill="#9ece6a" opacity=".9">'
  '<animate attributeName="x" values="390;390;812" keyTimes="0;0.14;1" '
  'dur="3.2s" fill="freeze"/></rect>')

# scanline sweep
A(f'<rect class="scanline" x="0" y="-40" width="{W}" height="40" fill="#7aa2f7" opacity=".045"/>')

# corner brackets
for (bx, by, sx, sy) in [(16, 16, 1, 1), (W - 16, 16, -1, 1), (16, H - 16, 1, -1), (W - 16, H - 16, -1, -1)]:
    A(f'<path d="M{bx} {by + sy*26} L{bx} {by} L{bx + sx*26} {by}" fill="none" '
      f'stroke="#7aa2f7" stroke-width="1.6" opacity=".45"/>')

A(f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="18" fill="none" '
  'stroke="#7aa2f7" stroke-width="1.5" opacity=".28"/>')
A('</g>')
A('</svg>')

svg = "\n".join(out)
sys.stdout.write(svg)
