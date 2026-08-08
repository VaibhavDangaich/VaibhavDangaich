#!/usr/bin/env python3
"""Animated knowledge-graph hero banner.

Palette is deliberately monochrome — ink, bone, one muted brass accent. No
neon, no rainbow gradients, no bloom filters: those are the tells that make a
profile read as generated. Depth comes from hairlines, grain and restraint.
"""
import math, random, sys

W, H = 1200, 340
random.seed(7)

INK0, INK1 = "#08080A", "#101014"
HAIR = "#26262E"
BONE, MUTE, FAINT = "#F0EDE8", "#9A9AA4", "#4E4E58"
BRASS = "#C6A87C"

SERIF = "'Iowan Old Style', 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# --- node placement -----------------------------------------------------
TEXT_BOX = (240, 100, 960, 250)


def in_text_box(x, y, pad=20):
    x0, y0, x1, y1 = TEXT_BOX
    return (x0 - pad) < x < (x1 + pad) and (y0 - pad) < y < (y1 + pad)


nodes = []
attempts = 0
while len(nodes) < 44 and attempts < 8000:
    attempts += 1
    x = random.uniform(22, W - 22)
    y = random.uniform(20, H - 20)
    if in_text_box(x, y):
        continue
    if any((x - nx) ** 2 + (y - ny) ** 2 < 58 ** 2 for nx, ny, _ in nodes):
        continue
    nodes.append((round(x, 1), round(y, 1), random.choice([1.3, 1.6, 1.9, 2.3, 2.9])))

edges = set()
for i, (x, y, _) in enumerate(nodes):
    d = sorted((math.dist((x, y), (nx, ny)), j)
               for j, (nx, ny, _) in enumerate(nodes) if j != i)
    for dist, j in d[:2]:
        if dist < 200:
            edges.add(tuple(sorted((i, j))))
edges = sorted(edges)

out = []
A = out.append

A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  f'role="img" aria-label="Vaibhav Dangaich — AI agents, knowledge graphs, full-stack">')

A('<defs>')
A(f'<linearGradient id="bg" x1="0" y1="0" x2="0.35" y2="1">'
  f'<stop offset="0%" stop-color="{INK1}"/><stop offset="100%" stop-color="{INK0}"/>'
  f'</linearGradient>')

# one warm wash and one cool, both low — not an aurora blob
A(f'<radialGradient id="wash" cx="22%" cy="18%" r="62%">'
  f'<stop offset="0%" stop-color="{BRASS}" stop-opacity=".085"/>'
  f'<stop offset="100%" stop-color="{BRASS}" stop-opacity="0"/></radialGradient>')
A(f'<radialGradient id="wash2" cx="86%" cy="88%" r="55%">'
  f'<stop offset="0%" stop-color="#7E8A99" stop-opacity=".07"/>'
  f'<stop offset="100%" stop-color="#7E8A99" stop-opacity="0"/></radialGradient>')

# wordmark: bone, with one slow warm pass across it
A('<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">'
  f'<stop offset="0%" stop-color="{BONE}"/>'
  f'<stop offset="42%" stop-color="{BONE}"/>'
  '<stop offset="50%" stop-color="#FFF8EA"/>'
  f'<stop offset="58%" stop-color="{BONE}"/>'
  f'<stop offset="100%" stop-color="{BONE}"/>'
  '<animateTransform attributeName="gradientTransform" type="translate" '
  'values="-1.1 0;1.1 0;-1.1 0" dur="16s" repeatCount="indefinite"/>'
  '</linearGradient>')

A(f'<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
  f'<stop offset="0%" stop-color="{BRASS}" stop-opacity="0"/>'
  f'<stop offset="50%" stop-color="{BRASS}" stop-opacity=".55"/>'
  f'<stop offset="100%" stop-color="{BRASS}" stop-opacity="0"/></linearGradient>')

A(f'<radialGradient id="vignette" cx="50%" cy="50%" r="54%">'
  f'<stop offset="0%" stop-color="{INK0}" stop-opacity=".95"/>'
  f'<stop offset="66%" stop-color="{INK0}" stop-opacity=".62"/>'
  f'<stop offset="100%" stop-color="{INK0}" stop-opacity="0"/></radialGradient>')

# film grain — the texture cue that reads as printed rather than rendered
A('<filter id="grain" x="0" y="0" width="100%" height="100%">'
  '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/>'
  '<feColorMatrix type="saturate" values="0"/>'
  '<feComponentTransfer><feFuncA type="linear" slope=".55"/></feComponentTransfer></filter>')

A(f'<clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
A('<clipPath id="typeclip"><rect x="404" y="222" width="396" height="28">'
  '<animate attributeName="width" values="0;0;396" keyTimes="0;0.16;1" '
  'dur="3.4s" fill="freeze"/></rect></clipPath>')
A('</defs>')

A('<style>'
  '@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(0,-6px)}}'
  '@keyframes breathe{0%,100%{opacity:.30}50%{opacity:.72}}'
  '@keyframes blink{0%,49%{opacity:.85}50%,100%{opacity:0}}'
  '.cursor{animation:blink 1.15s step-end infinite}'
  '</style>')

A('<g clip-path="url(#frame)">')
A(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
A(f'<rect width="{W}" height="{H}" fill="url(#wash)"/>')
A(f'<rect width="{W}" height="{H}" fill="url(#wash2)"/>')

# hairline grid, barely there
A(f'<g stroke="{HAIR}" stroke-width=".5" opacity=".55">')
for gx in range(0, W + 1, 48):
    A(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}"/>')
for gy in range(0, H + 1, 48):
    A(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}"/>')
A('</g>')

# ---------------------------------------------------------------- graph
A('<g>')
for k, (i, j) in enumerate(edges):
    x1, y1, _ = nodes[i]
    x2, y2, _ = nodes[j]
    A(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BONE}" stroke-width=".65" '
      f'opacity=".10"><animate attributeName="opacity" values=".05;.17;.05" '
      f'dur="{7 + (k % 6):.0f}s" begin="{(k % 11) * 0.7:.1f}s" repeatCount="indefinite"/></line>')

# a handful of slow travellers, brass not neon
for k, (i, j) in enumerate(edges):
    if k % 5:
        continue
    x1, y1, _ = nodes[i]
    x2, y2, _ = nodes[j]
    dur = 5.5 + (k % 7) * 0.8
    A(f'<circle r="1.5" fill="{BRASS}" opacity=".8">'
      f'<animateMotion dur="{dur:.1f}s" begin="{(k % 13) * 0.9:.1f}s" repeatCount="indefinite" '
      f'path="M{x1} {y1} L{x2} {y2}"/>'
      f'<animate attributeName="opacity" values="0;.85;.85;0" dur="{dur:.1f}s" '
      f'begin="{(k % 13) * 0.9:.1f}s" repeatCount="indefinite"/></circle>')

for k, (x, y, r) in enumerate(nodes):
    col = BRASS if k % 7 == 0 else BONE
    A(f'<g style="animation:drift {12 + (k % 7)}s ease-in-out infinite;'
      f'animation-delay:{(k % 9) * .6:.1f}s">'
      f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" opacity=".45" '
      f'style="animation:breathe {6 + (k % 5)}s ease-in-out infinite;'
      f'animation-delay:{(k % 8) * .7:.1f}s"/></g>')
A('</g>')

A('<ellipse cx="600" cy="172" rx="480" ry="146" fill="url(#vignette)"/>')

# ---------------------------------------------------------------- wordmark
A(f'<text x="600" y="150" text-anchor="middle" font-family="{SERIF}" font-size="62" '
  f'letter-spacing="2" fill="url(#sheen)">Vaibhav Dangaich</text>')

A('<rect x="392" y="174" width="416" height="1" fill="url(#rule)"/>')

A(f'<text x="600" y="200" text-anchor="middle" font-family="{MONO}" font-size="11.5" '
  f'letter-spacing="5.6" fill="{MUTE}">AI AGENTS &#183; KNOWLEDGE GRAPHS &#183; FULL-STACK</text>')

A('<g clip-path="url(#typeclip)">'
  f'<text x="404" y="242" font-family="{MONO}" font-size="14" fill="{BONE}" opacity=".72">'
  f'<tspan fill="{FAINT}">~ $ </tspan>build --something-that-outlives-the-session'
  '</text></g>')
A(f'<rect class="cursor" x="800" y="231" width="7" height="14" fill="{BRASS}">'
  '<animate attributeName="x" values="404;404;800" keyTimes="0;0.16;1" '
  'dur="3.4s" fill="freeze"/></rect>')

A(f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".055" '
  'style="mix-blend-mode:overlay"/>')
A(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" '
  f'stroke="{HAIR}" stroke-width="1"/>')
A('</g>')
A('</svg>')

sys.stdout.write("\n".join(out))
