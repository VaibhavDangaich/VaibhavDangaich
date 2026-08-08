#!/usr/bin/env python3
"""Generate an animated terminal 'boot sequence' card for the profile README."""
import sys
from html import escape

FS = 15.0
ADV = FS * 0.6           # monospace advance width
PADX, TOP = 26, 78
LH = 27.0                # line height
W = 860

# (kind, text) — kind: cmd | out | ok
LINES = [
    ("cmd", "whoami"),
    ("out", "vaibhav dangaich — b.tech ai & ml @ bit mesra '27 · cgpa 8.4"),
    ("cmd", "cat ~/.focus"),
    ("out", "agents that finish the job · graphs that remember · tools devs keep"),
    ("cmd", "mnex --status"),
    ("ok",  "5-tier memory   planner -> executor -> critic   local-first   [v1.5.1]"),
    ("cmd", "arxiv --mine"),
    ("out", "2607.28662 · ontology-guided extraction for knowledge-graph construction"),
    ("cmd", "ls ~/shipped"),
    ("out", "foiatlas  mnex  context-graph  visual-activity-agent  order-supervisor"),
]

H = int(TOP + LH * len(LINES) + 44)

# ---- timing ------------------------------------------------------------
TYPE_PER_CHAR = 0.045
GAP_CMD, GAP_OUT = 0.45, 0.25
t, sched = 1.0, []
for kind, text in LINES:
    dur = max(0.35, len(text) * TYPE_PER_CHAR) if kind == "cmd" else 0.28
    sched.append((t, dur))
    t += dur + (GAP_CMD if kind == "cmd" else GAP_OUT)
TOTAL = round(t, 2)                # the reveal runs once, then freezes full

COLORS = {"cmd": "#c0caf5", "out": "#9aa5ce", "ok": "#9ece6a"}

out = []
A = out.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" role="img" '
  'aria-label="terminal: whoami, focus, mnex status, shipped projects">')

A('<defs>')
A('<linearGradient id="tbg" x1="0" y1="0" x2="1" y2="1">'
  '<stop offset="0%" stop-color="#12141f"/><stop offset="100%" stop-color="#0b0d17"/>'
  '</linearGradient>')
A('<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1">'
  '<stop offset="0%" stop-color="#232742"/><stop offset="100%" stop-color="#191c2e"/>'
  '</linearGradient>')
A('<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">'
  '<stop offset="0%" stop-color="#7aa2f7"/><stop offset="50%" stop-color="#bb9af7"/>'
  '<stop offset="100%" stop-color="#2ac3de"/>'
  '<animateTransform attributeName="gradientTransform" type="translate" '
  'values="-1 0;1 0;-1 0" dur="8s" repeatCount="indefinite"/></linearGradient>')

for i, (start, dur) in enumerate(sched):
    text = LINES[i][1]
    full = round(PADX + 22 + len(text) * ADV + 14, 1)
    k1, k2 = round(start / TOTAL, 4), round((start + dur) / TOTAL, 4)
    y = round(TOP + LH * i - FS, 1)
    A(f'<clipPath id="c{i}"><rect x="0" y="{y}" width="{full}" height="{LH}">'
      f'<animate attributeName="width" values="0;0;{full}" keyTimes="0;{k1};{k2}" '
      f'calcMode="linear" dur="{k2*TOTAL:.2f}s" fill="freeze"/></rect></clipPath>')
A('</defs>')

A('<style>'
  '@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}'
  '.cur{animation:blink .95s step-end infinite}'
  '</style>')

# window
A(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="url(#tbg)" '
  'stroke="#2a2f4a" stroke-width="1.5"/>')
A(f'<path d="M15 1 H{W-15} A14 14 0 0 1 {W-1} 15 V44 H1 V15 A14 14 0 0 1 15 1 Z" fill="url(#bar)"/>')
A(f'<line x1="1" y1="44" x2="{W-1}" y2="44" stroke="#2a2f4a" stroke-width="1.5"/>')
for cx, col in ((28, "#ff5f57"), (50, "#febc2e"), (72, "#28c840")):
    A(f'<circle cx="{cx}" cy="22.5" r="6" fill="{col}"/>')
A(f'<text x="{W/2}" y="27" text-anchor="middle" font-size="12.5" fill="#565f89" '
  'letter-spacing="1">vaibhav@github — zsh</text>')

# lines
for i, (kind, text) in enumerate(LINES):
    y = round(TOP + LH * i, 1)
    start, dur = sched[i]
    A(f'<g clip-path="url(#c{i})">')
    if kind == "cmd":
        A(f'<text x="{PADX}" y="{y}" font-size="{FS}" xml:space="preserve">'
          f'<tspan fill="#7aa2f7" font-weight="700">❯</tspan>'
          f'<tspan fill="{COLORS[kind]}" x="{PADX+22}">{escape(text)}</tspan></text>')
    else:
        A(f'<text x="{PADX+22}" y="{y}" font-size="{FS}" fill="{COLORS[kind]}" '
          f'xml:space="preserve">{escape(text)}</text>')
    A('</g>')

    if kind == "cmd":
        cx = round(PADX + 22 + len(text) * ADV + 3, 1)
        k2 = round((start + dur) / TOTAL, 4)
        k3 = round(min((start + dur + GAP_CMD) / TOTAL, 0.999), 4)
        end = start + dur + GAP_CMD
        A(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;0" '
          f'keyTimes="0;{(start+dur)/end:.4f};{min((start+dur)/end+0.001,0.998):.4f};1" '
          f'dur="{end:.2f}s" fill="freeze"/>'
          f'<rect class="cur" x="{cx}" y="{y-FS+3}" width="8.5" height="{FS+1}" fill="#9ece6a"/></g>')

# resting cursor after the last line
ly = round(TOP + LH * len(LINES), 1)
last_end = sched[-1][0] + sched[-1][1] + 0.2
A(f'<g opacity="1"><animate attributeName="opacity" values="0;0;1" '
  f'keyTimes="0;{(last_end-0.001)/last_end:.4f};1" dur="{last_end:.2f}s" fill="freeze"/>'
  f'<text x="{PADX}" y="{ly}" font-size="{FS}" fill="#7aa2f7" font-weight="700">❯</text>'
  f'<rect class="cur" x="{PADX+22}" y="{ly-FS+3}" width="8.5" height="{FS+1}" fill="#9ece6a"/></g>')

# accent underline
A(f'<rect x="1" y="{H-4}" width="{W-2}" height="3" rx="1.5" fill="url(#edge)" opacity=".85"/>')
A('</svg>')

sys.stdout.write("\n".join(out))
