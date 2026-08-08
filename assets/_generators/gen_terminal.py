#!/usr/bin/env python3
"""Animated terminal 'boot sequence' card.

Ink surface, bone text, one brass accent. Deliberately not the red/amber/green
traffic lights every generated terminal mockup ships with.
"""
import sys
from html import escape

INK0, INK1, INK2 = "#08080A", "#0E0E12", "#15151A"
HAIR = "#26262E"
BONE, MUTE, FAINT = "#F0EDE8", "#9A9AA4", "#4E4E58"
BRASS = "#C6A87C"

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

FS = 15.0
ADV = FS * 0.6
PADX, TOP = 28, 80
LH = 27.0
W = 860

# (kind, text) — kind: cmd | out | key
LINES = [
    ("cmd", "whoami"),
    ("out", "vaibhav dangaich — b.tech ai & ml @ bit mesra '27 · cgpa 8.4"),
    ("cmd", "cat ~/.focus"),
    ("out", "agents that finish the job · graphs that remember · tools devs keep"),
    ("cmd", "mnex --status"),
    ("key", "5-tier memory   planner -> executor -> critic   local-first   [v1.5.1]"),
    ("cmd", "arxiv --mine"),
    ("out", "2607.28662 · ontology-guided extraction for knowledge-graph construction"),
    ("cmd", "ls ~/shipped"),
    ("out", "foiatlas  mnex  context-graph  visual-activity-agent  order-supervisor"),
]

H = int(TOP + LH * len(LINES) + 44)

TYPE_PER_CHAR = 0.042
GAP_CMD, GAP_OUT = 0.42, 0.24
t, sched = 0.9, []
for kind, text in LINES:
    dur = max(0.32, len(text) * TYPE_PER_CHAR) if kind == "cmd" else 0.26
    sched.append((t, dur))
    t += dur + (GAP_CMD if kind == "cmd" else GAP_OUT)
TOTAL = round(t, 2)

COLORS = {"cmd": BONE, "out": MUTE, "key": BONE}

out = []
A = out.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  f'font-family="{MONO}" role="img" '
  'aria-label="terminal: whoami, focus, mnex status, arXiv preprint, shipped projects">')

A('<defs>')
A(f'<linearGradient id="tbg" x1="0" y1="0" x2="0.4" y2="1">'
  f'<stop offset="0%" stop-color="{INK1}"/><stop offset="100%" stop-color="{INK0}"/>'
  f'</linearGradient>')
A(f'<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1">'
  f'<stop offset="0%" stop-color="{INK2}"/><stop offset="100%" stop-color="#101015"/>'
  f'</linearGradient>')
A(f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">'
  f'<stop offset="0%" stop-color="{BRASS}" stop-opacity="0"/>'
  f'<stop offset="42%" stop-color="{BRASS}" stop-opacity=".55"/>'
  f'<stop offset="100%" stop-color="{BRASS}" stop-opacity="0"/>'
  '<animateTransform attributeName="gradientTransform" type="translate" '
  'values="-1 0;1 0;-1 0" dur="18s" repeatCount="indefinite"/></linearGradient>')
A('<filter id="tgrain" x="0" y="0" width="100%" height="100%">'
  '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/>'
  '<feColorMatrix type="saturate" values="0"/>'
  '<feComponentTransfer><feFuncA type="linear" slope=".55"/></feComponentTransfer></filter>')
A(f'<clipPath id="twin"><rect width="{W}" height="{H}" rx="14"/></clipPath>')

for i, (start, dur) in enumerate(sched):
    text = LINES[i][1]
    full = round(PADX + 22 + len(text) * ADV + 14, 1)
    k1, k2 = round(start / TOTAL, 4), round((start + dur) / TOTAL, 4)
    y = round(TOP + LH * i - FS, 1)
    A(f'<clipPath id="c{i}"><rect x="0" y="{y}" width="{full}" height="{LH}">'
      f'<animate attributeName="width" values="0;0;{full}" keyTimes="0;{k1};{k2}" '
      f'calcMode="linear" dur="{k2*TOTAL:.2f}s" fill="freeze"/></rect></clipPath>')
A('</defs>')

A('<style>@keyframes blink{0%,49%{opacity:.9}50%,100%{opacity:0}}'
  '.cur{animation:blink 1.15s step-end infinite}</style>')

A('<g clip-path="url(#twin)">')
A(f'<rect width="{W}" height="{H}" fill="url(#tbg)"/>')
A(f'<rect x="0" y="0" width="{W}" height="46" fill="url(#bar)"/>')
A(f'<line x1="0" y1="46" x2="{W}" y2="46" stroke="{HAIR}" stroke-width="1"/>')

# window controls, monochrome — one brass to signal focus
for cx, col, op in ((30, BRASS, ".85"), (50, MUTE, ".38"), (70, MUTE, ".38")):
    A(f'<circle cx="{cx}" cy="23" r="5" fill="{col}" opacity="{op}"/>')
A(f'<text x="{W/2}" y="27.5" text-anchor="middle" font-size="12" fill="{FAINT}" '
  'letter-spacing="1.4">vaibhav@github — zsh</text>')

for i, (kind, text) in enumerate(LINES):
    y = round(TOP + LH * i, 1)
    start, dur = sched[i]
    A(f'<g clip-path="url(#c{i})">')
    if kind == "cmd":
        A(f'<text x="{PADX}" y="{y}" font-size="{FS}" xml:space="preserve">'
          f'<tspan fill="{BRASS}">❯</tspan>'
          f'<tspan fill="{COLORS[kind]}" x="{PADX+22}">{escape(text)}</tspan></text>')
    elif kind == "key":
        A(f'<text x="{PADX+22}" y="{y}" font-size="{FS}" fill="{BONE}" opacity=".9" '
          f'xml:space="preserve">{escape(text)}</text>')
    else:
        A(f'<text x="{PADX+22}" y="{y}" font-size="{FS}" fill="{COLORS[kind]}" '
          f'xml:space="preserve">{escape(text)}</text>')
    A('</g>')

    if kind == "cmd":
        cx = round(PADX + 22 + len(text) * ADV + 3, 1)
        end = start + dur + GAP_CMD
        A(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;0" '
          f'keyTimes="0;{(start+dur)/end:.4f};{min((start+dur)/end+0.001,0.998):.4f};1" '
          f'dur="{end:.2f}s" fill="freeze"/>'
          f'<rect class="cur" x="{cx}" y="{y-FS+3}" width="8" height="{FS}" fill="{BRASS}"/></g>')

ly = round(TOP + LH * len(LINES), 1)
last_end = sched[-1][0] + sched[-1][1] + 0.2
A(f'<g opacity="1"><animate attributeName="opacity" values="0;0;1" '
  f'keyTimes="0;{(last_end-0.001)/last_end:.4f};1" dur="{last_end:.2f}s" fill="freeze"/>'
  f'<text x="{PADX}" y="{ly}" font-size="{FS}" fill="{BRASS}">❯</text>'
  f'<rect class="cur" x="{PADX+22}" y="{ly-FS+3}" width="8" height="{FS}" fill="{BRASS}"/></g>')

A(f'<rect width="{W}" height="{H}" filter="url(#tgrain)" opacity=".05" '
  'style="mix-blend-mode:overlay"/>')
A(f'<rect x="0" y="{H-3}" width="{W}" height="2" fill="url(#edge)"/>')
A(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{HAIR}" '
  'stroke-width="1"/>')
A('</g></svg>')

sys.stdout.write("\n".join(out))
