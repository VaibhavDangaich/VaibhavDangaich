#!/usr/bin/env python3
"""Generated SVG furniture for the profile README: section headers, project
cards, the experience timeline, the publication card, the tech-stack matrix,
the signal strip and the footer.

Design rules, held across every asset:
  · One accent. Muted brass on ink, plus bone/mute/faint for hierarchy.
    Hue does not carry meaning here — weight, size and space do.
  · No bloom. Neon glow filters are the loudest generated-looking tell.
  · Hairlines, not borders. 1px at low contrast, never 2px at full.
  · Grain over gradient. Texture reads as printed; blobs read as rendered.
  · Motion is slow and sparse — a few things drift, nothing pulses in unison.
"""
import pathlib, sys
from html import escape

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "profile_readme/assets")
OUT.mkdir(parents=True, exist_ok=True)

SANS = ("ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', "
        "Roboto, Helvetica, Arial, sans-serif")
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SERIF = "'Iowan Old Style', 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif"

INK0, INK1, INK2 = "#08080A", "#0E0E12", "#15151A"
HAIR = "#26262E"
BONE, MUTE, FAINT = "#F0EDE8", "#9A9AA4", "#4E4E58"
BRASS = "#C6A87C"
SLATE = "#7E8A99"


def sans_w(s, fs):
    narrow = sum(c in "iljtfrI.,:;'|!()[]-" for c in s)
    wide = sum(c.isupper() or c in "mwMW@" for c in s)
    return fs * (0.53 * len(s) - 0.20 * narrow + 0.12 * wide)


def head(w, h, label, font=SANS):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" font-family="{font}" role="img" aria-label="{escape(label)}">')


def grain_def(gid="grain"):
    return (f'<filter id="{gid}" x="0" y="0" width="100%" height="100%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" '
            'stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/>'
            '<feComponentTransfer><feFuncA type="linear" slope=".55"/>'
            '</feComponentTransfer></filter>')


def grain(w, h, gid="grain", op=".05"):
    return (f'<rect width="{w}" height="{h}" filter="url(#{gid})" opacity="{op}" '
            'style="mix-blend-mode:overlay"/>')


def panel(gid, w, h):
    """Ink surface with a hairline edge — the shared substrate for every card."""
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0.4" y2="1">'
            f'<stop offset="0%" stop-color="{INK1}"/><stop offset="100%" stop-color="{INK0}"/>'
            f'</linearGradient>')


def warm_rule(gid, dur=18):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0%" stop-color="{BRASS}" stop-opacity="0"/>'
            f'<stop offset="45%" stop-color="{BRASS}" stop-opacity=".7"/>'
            f'<stop offset="100%" stop-color="{BRASS}" stop-opacity="0"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" '
            f'values="-1 0;1 0;-1 0" dur="{dur}s" repeatCount="indefinite"/></linearGradient>')


def chip(x, y, text, fs=12.5, h=26, dot=BRASS):
    """Hairline chip. Outlined in HAIR, not in the accent — accent is only the dot."""
    w = sans_w(text, fs) + 30
    return (w, f'<g><rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" '
               f'fill="{INK2}" stroke="{HAIR}" stroke-width="1"/>'
               f'<circle cx="{x+12:.1f}" cy="{y+h/2}" r="2.6" fill="{dot}" opacity=".9"/>'
               f'<text x="{x+22:.1f}" y="{y+h/2+4.3:.1f}" font-size="{fs}" fill="{MUTE}">'
               f'{escape(text)}</text></g>')


# ─────────────────────────────────────────────────────────── section headers
def section_header(num, title, sub, fname):
    W, H, PAD = 1200, 84, 28
    o = [head(W, H, f"{num} — {title}")]
    o.append('<defs>')
    o.append(panel("hbg", W, H))
    o.append(warm_rule("hrule"))
    o.append(f'<linearGradient id="hfade" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="{HAIR}"/>'
             f'<stop offset="100%" stop-color="{HAIR}" stop-opacity="0"/></linearGradient>')
    o.append(grain_def("hg"))
    o.append(f'<clipPath id="hc"><rect width="{W}" height="{H}" rx="14"/></clipPath>')
    o.append('</defs>')
    o.append('<g clip-path="url(#hc)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#hbg)"/>')

    o.append(f'<text x="{PAD}" y="32" font-family="{MONO}" font-size="10.5" '
             f'letter-spacing="2.4" fill="{BRASS}" opacity=".8">{num}</text>')
    o.append(f'<text x="{PAD}" y="65" font-family="{SERIF}" font-size="27" letter-spacing=".4" '
             f'fill="{BONE}">{escape(title)}</text>')

    x = PAD + sans_w(title, 27) * 1.02 + 26
    o.append(f'<text x="{x:.0f}" y="63" font-family="{MONO}" font-size="10.5" '
             f'letter-spacing="1.9" fill="{FAINT}">{escape(sub.upper())}</text>')

    sx = x + len(sub) * 8.0 + 28
    o.append(f'<rect x="{sx:.0f}" y="57" width="{max(60, W - sx - PAD):.0f}" height="1" '
             f'fill="url(#hfade)"/>')
    o.append(f'<rect x="{sx:.0f}" y="57" width="{max(60, W - sx - PAD):.0f}" height="1" '
             f'fill="url(#hrule)" opacity=".7"/>')

    o.append(grain(W, H, "hg", ".045"))
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" '
             f'stroke="{HAIR}" stroke-width="1"/>')
    o.append('</g></svg>')
    (OUT / fname).write_text("\n".join(o))


# ───────────────────────────────────────────────────────────── project cards
def project_card(title, chips, fname, seed=0):
    W, H = 620, 116
    o = [head(W, H, title)]
    o.append('<defs>')
    o.append(panel("cb", W, H))
    o.append(warm_rule("cbar", 14))
    o.append(f'<radialGradient id="cglow" cx="86%" cy="14%" r="58%">'
             f'<stop offset="0%" stop-color="{BRASS}" stop-opacity=".07"/>'
             f'<stop offset="100%" stop-color="{BRASS}" stop-opacity="0"/></radialGradient>')
    o.append(grain_def("cg"))
    o.append(f'<clipPath id="cc"><rect width="{W}" height="{H}" rx="14"/></clipPath>')
    o.append('</defs>')
    o.append('<style>@keyframes cb{0%,100%{opacity:.28}50%{opacity:.68}}</style>')

    o.append('<g clip-path="url(#cc)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#cb)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#cglow)"/>')

    # constellation motif, hairline — rotated per card so no two read the same
    base = [(486, 30), (528, 18), (560, 44), (596, 26), (540, 66), (500, 60), (588, 64)]
    pts = base[seed % len(base):] + base[:seed % len(base)]
    for a, b in ((0, 1), (1, 2), (2, 3), (2, 4), (4, 5), (0, 5), (3, 6)):
        o.append(f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}" '
                 f'stroke="{BONE}" stroke-width=".65" opacity=".13"/>')
    for i, (px, py) in enumerate(pts):
        col = BRASS if i == seed % len(pts) else BONE
        o.append(f'<circle cx="{px}" cy="{py}" r="2" fill="{col}" opacity=".45" '
                 f'style="animation:cb {7+(i%4)}s ease-in-out infinite;'
                 f'animation-delay:{i*0.8:.1f}s"/>')

    o.append(f'<rect x="0" y="0" width="3" height="{H}" fill="url(#cbar)"/>')
    o.append(f'<text x="28" y="46" font-family="{SERIF}" font-size="24" letter-spacing=".2" '
             f'fill="{BONE}">{escape(title)}</text>')

    cx = 28.0
    for i, c in enumerate(chips):
        w, markup = chip(cx, 70, c, dot=BRASS if i == 0 else MUTE)
        o.append(markup)
        cx += w + 9

    o.append(grain(W, H, "cg", ".05"))
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" '
             f'stroke="{HAIR}" stroke-width="1"/>')
    o.append('</g></svg>')
    (OUT / fname).write_text("\n".join(o))


# ──────────────────────────────────────────────────────────── tech stack
def stack_matrix(groups, fname):
    W, PADL, LABW, ROWH, TOP = 1200, 28, 156, 56, 24
    H = TOP + ROWH * len(groups) + 20
    o = [head(W, H, "tech stack")]
    o.append('<defs>')
    o.append(panel("sb", W, H))
    o.append(grain_def("sg"))
    o.append(f'<clipPath id="sc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    o.append('</defs>')
    o.append('<g clip-path="url(#sc)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#sb)"/>')

    for gi, (label, items) in enumerate(groups):
        y = TOP + ROWH * gi
        if gi:
            o.append(f'<line x1="{PADL}" y1="{y-4}" x2="{W-PADL}" y2="{y-4}" stroke="{HAIR}" '
                     f'stroke-width="1" opacity=".7"/>')
        o.append(f'<text x="{PADL}" y="{y+29}" font-family="{MONO}" font-size="11" '
                 f'letter-spacing="1.8" fill="{BRASS}" opacity=".9">'
                 f'{escape(label.upper())}</text>')
        cx = float(PADL + LABW)
        for k, it in enumerate(items):
            w, markup = chip(cx, y + 9, it, fs=13, h=30,
                             dot=BRASS if k == 0 else MUTE)
            o.append(markup)
            cx += w + 10

    o.append(grain(W, H, "sg", ".045"))
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" '
             f'stroke="{HAIR}" stroke-width="1"/>')
    o.append('</g></svg>')
    (OUT / fname).write_text("\n".join(o))


# ───────────────────────────────────────────────────────── experience timeline
def timeline(entries, fname):
    W, PADL, SPINE, TOP = 1200, 28, 66, 32
    H = TOP + sum(78 + 22 * len(e[3]) for e in entries) + 16
    o = [head(W, H, "experience timeline")]
    o.append('<defs>')
    o.append(panel("tlbg", W, H))
    o.append(f'<linearGradient id="spine" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0%" stop-color="{BRASS}" stop-opacity=".7"/>'
             f'<stop offset="70%" stop-color="{HAIR}"/>'
             f'<stop offset="100%" stop-color="{HAIR}" stop-opacity="0"/></linearGradient>')
    o.append(grain_def("tg"))
    o.append(f'<clipPath id="tlc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    o.append('</defs>')
    o.append(f'<style>@keyframes fall{{0%{{transform:translateY(0);opacity:0}}'
             f'10%{{opacity:.9}}90%{{opacity:.9}}'
             f'100%{{transform:translateY({H-TOP-30}px);opacity:0}}}}'
             '.fall{animation:fall 9s linear infinite}</style>')
    o.append('<g clip-path="url(#tlc)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#tlbg)"/>')
    o.append(f'<rect x="{SPINE-0.5}" y="{TOP-8}" width="1" height="{H-TOP-8}" '
             f'fill="url(#spine)"/>')
    o.append(f'<circle class="fall" cx="{SPINE}" cy="{TOP-4}" r="2" fill="{BRASS}"/>')

    y = TOP
    for org, role, dates, lines in entries:
        o.append(f'<circle cx="{SPINE}" cy="{y+14}" r="4" fill="{BRASS}" opacity=".9"/>')
        o.append(f'<circle cx="{SPINE}" cy="{y+14}" r="9" fill="none" stroke="{HAIR}" '
                 f'stroke-width="1"/>')
        o.append(f'<text x="{SPINE+34}" y="{y+20}" font-family="{SERIF}" font-size="19" '
                 f'fill="{BONE}">{escape(org)}</text>')
        rx = SPINE + 34 + sans_w(org, 19) * 1.02 + 16
        o.append(f'<text x="{rx:.0f}" y="{y+20}" font-family="{MONO}" font-size="11.5" '
                 f'letter-spacing="1.2" fill="{BRASS}" opacity=".9">'
                 f'{escape(role.upper())}</text>')
        dw = len(dates) * 6.6 + 24
        o.append(f'<rect x="{W-PADL-dw:.0f}" y="{y+4}" width="{dw:.0f}" height="23" rx="11.5" '
                 f'fill="{INK2}" stroke="{HAIR}" stroke-width="1"/>')
        o.append(f'<text x="{W-PADL-dw/2:.0f}" y="{y+19.5}" text-anchor="middle" '
                 f'font-family="{MONO}" font-size="11" fill="{MUTE}">{escape(dates)}</text>')
        ly = y + 44
        for ln in lines:
            o.append(f'<text x="{SPINE+34}" y="{ly}" font-size="13.5" fill="{MUTE}">'
                     f'{escape(ln)}</text>')
            ly += 22
        y += 78 + 22 * len(lines)

    o.append(grain(W, H, "tg", ".045"))
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" '
             f'stroke="{HAIR}" stroke-width="1"/>')
    o.append('</g></svg>')
    (OUT / fname).write_text("\n".join(o))


# ────────────────────────────────────────────────────────── publication card
def publication(arxiv_id, title_lines, authors, venue, results, fname):
    W = 1200
    H = 98 + 32 * len(title_lines) + 76
    o = [head(W, H, f"preprint {arxiv_id}: {' '.join(title_lines)}")]
    o.append('<defs>')
    o.append(panel("pbg", W, H))
    o.append(warm_rule("pbar", 16))
    o.append(f'<radialGradient id="pglow" cx="88%" cy="12%" r="52%">'
             f'<stop offset="0%" stop-color="{BRASS}" stop-opacity=".07"/>'
             f'<stop offset="100%" stop-color="{BRASS}" stop-opacity="0"/></radialGradient>')
    o.append(grain_def("pg"))
    o.append(f'<clipPath id="pc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    o.append('</defs>')
    o.append('<style>@keyframes pb{0%,100%{opacity:.3}50%{opacity:.7}}</style>')
    o.append('<g clip-path="url(#pc)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#pbg)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#pglow)"/>')
    o.append(f'<rect x="0" y="0" width="3" height="{H}" fill="url(#pbar)"/>')

    # redacted-document + graph motif, hairline
    o.append('<g transform="translate(1016,28)">')
    o.append(f'<rect x="0" y="0" width="50" height="64" rx="4" fill="none" stroke="{HAIR}" '
             f'stroke-width="1"/>')
    for i, ly in enumerate((13, 23, 33, 43, 53)):
        wd = (32, 28, 34, 20, 26)[i]
        redacted = i in (1, 3)
        o.append(f'<rect x="9" y="{ly}" width="{wd}" height="4" rx="1" '
                 f'fill="{BRASS if redacted else BONE}" '
                 f'opacity="{".55" if redacted else ".22"}"/>')
    gp = [(84, 12), (120, 30), (86, 52), (128, 62), (150, 24)]
    for a, b in ((0, 1), (1, 2), (1, 3), (1, 4), (2, 3)):
        o.append(f'<line x1="{gp[a][0]}" y1="{gp[a][1]}" x2="{gp[b][0]}" y2="{gp[b][1]}" '
                 f'stroke="{BONE}" stroke-width=".65" opacity=".16"/>')
    for i, (px, py) in enumerate(gp):
        o.append(f'<circle cx="{px}" cy="{py}" r="2.4" fill="{BRASS if i==1 else BONE}" '
                 f'opacity=".45" style="animation:pb {7+i}s ease-in-out infinite;'
                 f'animation-delay:{i*0.7:.1f}s"/>')
    o.append('</g>')

    o.append(f'<rect x="28" y="26" width="84" height="22" rx="11" fill="{INK2}" '
             f'stroke="{BRASS}" stroke-opacity=".4" stroke-width="1"/>')
    o.append(f'<text x="70" y="41" text-anchor="middle" font-family="{MONO}" font-size="10" '
             f'letter-spacing="1.8" fill="{BRASS}">PREPRINT</text>')
    o.append(f'<text x="124" y="41" font-family="{MONO}" font-size="12.5" fill="{MUTE}">'
             f'{escape(arxiv_id)}</text>')
    o.append(f'<text x="{124 + len(arxiv_id)*7.5 + 20:.0f}" y="41" font-family="{MONO}" '
             f'font-size="11.5" fill="{FAINT}">{escape(venue)}</text>')

    ty = 82
    for ln in title_lines:
        o.append(f'<text x="28" y="{ty}" font-family="{SERIF}" font-size="22" fill="{BONE}">'
                 f'{escape(ln)}</text>')
        ty += 32
    o.append(f'<text x="28" y="{ty}" font-size="13" fill="{FAINT}">{escape(authors)}</text>')

    cx, cy = 28.0, ty + 18
    for i, r in enumerate(results):
        w, markup = chip(cx, cy, r, fs=12.5, h=27, dot=BRASS if i == 0 else MUTE)
        o.append(markup)
        cx += w + 9

    o.append(grain(W, H, "pg", ".045"))
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" '
             f'stroke="{HAIR}" stroke-width="1"/>')
    o.append('</g></svg>')
    (OUT / fname).write_text("\n".join(o))


# ──────────────────────────────────────────────────────────── signal tiles
def signal_strip(tiles, fname):
    W, H, PAD, GAP = 1200, 116, 28, 1
    tw = (W - 2 * PAD - GAP * (len(tiles) - 1)) / len(tiles)
    o = [head(W, H, " · ".join(f"{v} {l}" for v, l in tiles))]
    o.append('<defs>')
    o.append(panel("gbg", W, H))
    o.append(grain_def("gg"))
    o.append(f'<clipPath id="gc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    o.append('</defs>')
    o.append('<g clip-path="url(#gc)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#gbg)"/>')
    for i, (val, label) in enumerate(tiles):
        x = PAD + i * (tw + GAP)
        if i:
            o.append(f'<line x1="{x:.1f}" y1="30" x2="{x:.1f}" y2="{H-30}" stroke="{HAIR}" '
                     f'stroke-width="1"/>')
        o.append(f'<text x="{x+tw/2:.1f}" y="60" text-anchor="middle" font-family="{SERIF}" '
                 f'font-size="30" fill="{BONE}">{escape(val)}</text>')
        o.append(f'<rect x="{x+tw/2-10:.1f}" y="70" width="20" height="1" fill="{BRASS}" '
                 f'opacity=".6"/>')
        o.append(f'<text x="{x+tw/2:.1f}" y="88" text-anchor="middle" font-family="{MONO}" '
                 f'font-size="10" letter-spacing="1.6" fill="{FAINT}">{escape(label)}</text>')
    o.append(grain(W, H, "gg", ".045"))
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" '
             f'stroke="{HAIR}" stroke-width="1"/>')
    o.append('</g></svg>')
    (OUT / fname).write_text("\n".join(o))


# ───────────────────────────────────────────────────────────────── footer
def footer(fname):
    W, H = 1200, 190
    o = [head(W, H, "let's build something — vaibhavdangaich@gmail.com")]
    o.append('<defs>')
    o.append(panel("fbg", W, H))
    o.append(warm_rule("fw", 20))
    o.append(f'<radialGradient id="fglow" cx="50%" cy="120%" r="70%">'
             f'<stop offset="0%" stop-color="{BRASS}" stop-opacity=".10"/>'
             f'<stop offset="100%" stop-color="{BRASS}" stop-opacity="0"/></radialGradient>')
    o.append(grain_def("fg"))
    o.append(f'<clipPath id="fc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    o.append('</defs>')
    o.append('<style>@keyframes bk{0%,49%{opacity:.9}50%,100%{opacity:0}}'
             '@keyframes hz{0%,100%{opacity:.20}50%{opacity:.42}}'
             '.bk{animation:bk 1.15s step-end infinite}'
             '.hz{animation:hz 9s ease-in-out infinite}</style>')
    o.append('<g clip-path="url(#fc)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#fbg)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#fglow)"/>')

    # a horizon of hairlines instead of rainbow waves
    for i, (yy, op) in enumerate(((150, ".26"), (162, ".18"), (174, ".11"))):
        o.append(f'<path class="hz" d="M0 {yy} q 300 -22 600 0 t 600 0" fill="none" '
                 f'stroke="{BONE}" stroke-width=".8" opacity="{op}" '
                 f'style="animation-delay:{i*1.4:.1f}s"/>')

    o.append(f'<text x="{W/2}" y="66" text-anchor="middle" font-family="{MONO}" font-size="11" '
             f'letter-spacing="4.6" fill="{FAINT}">GOT AN IDEA WORTH BUILDING?</text>')
    o.append(f'<text x="{W/2}" y="112" text-anchor="middle" font-family="{SERIF}" '
             f'font-size="40" letter-spacing="1" fill="{BONE}">Let&#8217;s make it run.</text>')
    o.append(f'<rect x="{W/2-90}" y="126" width="180" height="1" fill="url(#fw)"/>')

    line = "mail vaibhavdangaich@gmail.com"
    tw = len(f"~ $ {line}") * 8.4
    o.append(f'<text x="{W/2 - 8}" y="154" text-anchor="middle" font-size="13.5" '
             f'font-family="{MONO}" fill="{MUTE}">'
             f'<tspan fill="{FAINT}">~ $ </tspan>{line}</text>')
    o.append(f'<rect class="bk" x="{W/2 - 8 + tw/2 + 5:.0f}" y="143" width="7" height="13" '
             f'fill="{BRASS}"/>')

    o.append(grain(W, H, "fg", ".045"))
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" '
             f'stroke="{HAIR}" stroke-width="1"/>')
    o.append('</g></svg>')
    (OUT / fname).write_text("\n".join(o))


# ───────────────────────────────────────────────────────── hairline divider
(OUT / "divider.svg").write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 4" width="1200" height="4" '
    f'role="img" aria-label="divider"><defs>{warm_rule("d", 20)}</defs>'
    f'<rect y="1.5" width="1200" height="1" fill="{HAIR}"/>'
    f'<rect y="1.5" width="1200" height="1" fill="url(#d)" opacity=".8"/></svg>')


# ─────────────────────────────────────────────────────────────────── build
section_header("01", "Experience", "where I've shipped", "s-exp.svg")
section_header("02", "Research", "preprint on arXiv", "s-research.svg")
section_header("03", "Featured builds", "things I actually shipped", "s-builds.svg")
section_header("04", "Tech stack", "what I reach for", "s-stack.svg")
section_header("05", "By the numbers", "commits, streaks, languages", "s-stats.svg")
section_header("06", "The snake", "it eats my contribution graph", "s-snake.svg")

signal_strip([
    ("8.4", "CGPA · BIT MESRA"),
    ("400+", "DSA PROBLEMS SOLVED"),
    ("Top 5", "IEEE CTF · 200+ TEAMS"),
    ("arXiv", "PREPRINT PUBLISHED"),
    ("v1.5.1", "MNEX LIVE ON NPM"),
], "signal.svg")

timeline([
    ("123 of AI", "Software Development Engineer Intern", "May 2026 – Jul 2026", [
        "Cohort learning platform on Next.js + Node/TypeScript over Azure — enrollment, scheduling, streaks, XP leaderboards, certificates.",
        "Owned monetization: Razorpay orders, subscriptions and webhooks, idempotent entitlements, a ledger-based credits system across 3 tiers.",
        "Built a recommendation engine on vector embeddings and semantic search (Azure OpenAI) targeting each learner's weak concepts.",
    ]),
    ("Konect U", "Artificial Intelligence Intern", "Feb 2026 – May 2026", [
        "Secure real-time ingestion with Apache NiFi + Kafka routing 4 document formats for a defence-oriented government intelligence project.",
        "LangChain LLM workflows and Neo4j knowledge graphs lifted entity-search recall from 70% to 95% with zero false merges.",
    ]),
    ("Konect U", "Full Stack Intern", "Oct 2025 – Dec 2025", [
        "Full-stack delivery in an agile team — client requirements into technical specs, third-party API integration.",
    ]),
    ("BIT Mesra", "B.Tech, Artificial Intelligence & Machine Learning", "Sep 2023 – Sep 2027", [
        "CGPA 8.4 · final year · Ranchi, India",
    ]),
], "timeline.svg")

publication(
    "arXiv:2607.28662",
    ["An Ontology-Guided, Deduplication-Aware Extraction Layer for",
     "Knowledge Graph Construction from Heterogeneous Documents"],
    "Vaibhav Dangaich, Kevin Lewis, Kundeshwar Pundalik",
    "cs.AI · July 2026",
    ["recall 70% → 95%", "zero false merges", "−94% catalog overhead",
     "Qwen3.5-9B, self-hosted", "Kafka document stream"],
    "publication.svg")

project_card("mnex", ["5-tier memory", "LangGraph", "npm v1.5.1"], "card-mnex.svg", 0)
project_card("FOIAtlas", ["Kùzu", "Gemini", "GraphRAG"], "card-foiatlas.svg", 1)
project_card("Context Graph", ["Python", "Neo4j", "FastAPI"], "card-contextgraph.svg", 2)
project_card("Visual Activity Agent", ["Chrome MV3", "Supabase", "Gemini Vision"],
             "card-vaa.svg", 3)
project_card("Order Supervisor", ["Temporal", "Python", "durable"], "card-supervisor.svg", 4)
project_card("Servicing Agent", ["Policy-as-Code", "audit chain", "Python"],
             "card-servicing.svg", 5)

stack_matrix([
    ("Languages", ["Python", "TypeScript", "JavaScript", "C++", "C", "SQL"]),
    ("AI & agents", ["LangGraph", "LangChain", "Gemini", "Azure OpenAI", "Ollama", "Temporal"]),
    ("Web", ["Next.js", "React", "Node.js", "Express", "FastAPI", "Tailwind", "Three.js"]),
    ("Data & graphs", ["Neo4j", "Kùzu", "PostgreSQL", "MongoDB", "SQLite", "Supabase",
                       "Vector DBs"]),
    ("Infra & tools", ["Docker", "Azure", "Kafka", "NiFi", "Git", "GitHub Actions", "Vercel",
                       "Postman", "Jest"]),
], "stack.svg")

footer("footer.svg")
print("generated:", ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))
