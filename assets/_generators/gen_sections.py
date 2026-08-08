#!/usr/bin/env python3
"""Generate the custom animated SVG furniture for every README section:
section headers, project cards, the tech-stack matrix and the footer."""
import pathlib, sys
from html import escape

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "profile_readme/assets")
OUT.mkdir(parents=True, exist_ok=True)

SANS = ("ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', "
        "Roboto, Helvetica, Arial, sans-serif")
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

BG0, BG1 = "#0b0d17", "#12141f"
LINE = "#2a2f4a"
DIM, TXT = "#8b93b8", "#e6ecff"
BLUE, PURPLE, CYAN, GREEN, AMBER = "#7aa2f7", "#bb9af7", "#2ac3de", "#9ece6a", "#e0af68"


def sans_w(s, fs):
    """Rough advance width for a sans string."""
    narrow = sum(c in "iljtfrI.,:;'|!()[]-" for c in s)
    wide = sum(c.isupper() or c in "mwMW@" for c in s)
    return fs * (0.53 * len(s) - 0.20 * narrow + 0.12 * wide)


def head(w, h, label, font=SANS):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" font-family="{font}" role="img" aria-label="{escape(label)}">')


def sweep(gid, c1, c2, c3, dur=8):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0%" stop-color="{c1}"/><stop offset="50%" stop-color="{c2}"/>'
            f'<stop offset="100%" stop-color="{c3}"/>'
            f'<animateTransform attributeName="gradientTransform" type="translate" '
            f'values="-1 0;1 0;-1 0" dur="{dur}s" repeatCount="indefinite"/></linearGradient>')


# ─────────────────────────────────────────────────────────── section headers
def section_header(num, title, sub, accent, fname):
    """Numbered section header. Carries its own dark panel — every asset has to
    stay legible on GitHub light mode, where the page background is white."""
    W, H = 1200, 78
    PAD = 26
    o = [head(W, H, f"{num} — {title}")]
    o.append('<defs>')
    o.append(sweep("hl", accent, "#ffffff", accent, 7))
    o.append(f'<linearGradient id="hbg" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG0}"/>'
             f'</linearGradient>')
    o.append(f'<linearGradient id="hr" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="{accent}" stop-opacity=".85"/>'
             f'<stop offset="100%" stop-color="{accent}" stop-opacity="0"/></linearGradient>')
    o.append(f'<radialGradient id="hglow" cx="4%" cy="50%" r="42%">'
             f'<stop offset="0%" stop-color="{accent}" stop-opacity=".22"/>'
             f'<stop offset="100%" stop-color="{accent}" stop-opacity="0"/></radialGradient>')
    o.append(f'<clipPath id="hc"><rect width="{W}" height="{H}" rx="14"/></clipPath>')
    o.append('</defs>')
    o.append('<style>@keyframes bp{0%,100%{opacity:.35}50%{opacity:1}}'
             '.bp{animation:bp 2.6s ease-in-out infinite}</style>')

    o.append('<g clip-path="url(#hc)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#hbg)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#hglow)"/>')

    o.append(f'<rect x="{PAD}" y="19" width="4" height="42" rx="2" fill="url(#hl)"/>')
    o.append(f'<text x="{PAD+20}" y="36" font-size="12" font-weight="700" letter-spacing="2.5" '
             f'fill="{accent}" opacity=".8">{num}</text>')
    o.append(f'<text x="{PAD+20}" y="62" font-size="27" font-weight="800" letter-spacing="1.2" '
             f'fill="{TXT}">{escape(title)}</text>')

    x = PAD + 20 + sans_w(title, 27) + 1.2 * len(title) + 22
    o.append(f'<text x="{x:.0f}" y="61" font-size="13" letter-spacing="1.6" fill="{DIM}" '
             f'opacity=".95">{escape(sub)}</text>')

    sx = x + sans_w(sub, 13) + 1.6 * len(sub) + 24
    o.append(f'<rect x="{sx:.0f}" y="53" width="{max(40, W - sx - 86):.0f}" height="1.5" '
             f'fill="url(#hr)"/>')
    for i, cx in enumerate((W - 40, W - 56, W - 72)):
        o.append(f'<circle class="bp" cx="{cx}" cy="54" r="3" fill="{accent}" '
                 f'style="animation-delay:{i*0.35:.2f}s"/>')

    o.append(f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="14" fill="none" '
             f'stroke="{LINE}" stroke-width="1.5"/>')
    o.append('</g></svg>')
    (OUT / fname).write_text("\n".join(o))


# ───────────────────────────────────────────────────────────── project cards
def project_card(title, chips, accent, fname, motif="graph"):
    W, H = 620, 116
    o = [head(W, H, title)]
    o.append('<defs>')
    o.append(f'<linearGradient id="cb" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0%" stop-color="#141728"/><stop offset="100%" stop-color="{BG0}"/>'
             f'</linearGradient>')
    o.append(sweep("cbar", accent, "#ffffff", accent, 6))
    o.append(f'<radialGradient id="cglow" cx="88%" cy="12%" r="60%">'
             f'<stop offset="0%" stop-color="{accent}" stop-opacity=".30"/>'
             f'<stop offset="100%" stop-color="{accent}" stop-opacity="0"/></radialGradient>')
    o.append('<filter id="cg" x="-80%" y="-80%" width="260%" height="260%">'
             '<feGaussianBlur stdDeviation="2.4" result="b"/>'
             '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    o.append(f'<clipPath id="cc"><rect x="0" y="0" width="{W}" height="{H}" rx="14"/></clipPath>')
    o.append('</defs>')
    o.append('<style>@keyframes fl{0%,100%{opacity:.3;r:2.2}50%{opacity:1;r:3.4}}'
             '@keyframes sl{0%{transform:translateX(-120px)}100%{transform:translateX(700px)}}'
             '.fl{animation:fl 3s ease-in-out infinite}'
             '.sl{animation:sl 5.5s ease-in-out infinite}</style>')

    o.append('<g clip-path="url(#cc)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#cb)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#cglow)"/>')

    # motif: little constellation top-right
    pts = [(486, 30), (526, 18), (560, 42), (596, 26), (540, 66), (500, 62), (588, 62)]
    o.append('<g opacity=".55">')
    for a, b in ((0, 1), (1, 2), (2, 3), (2, 4), (4, 5), (0, 5), (3, 6), (4, 6)):
        o.append(f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}" '
                 f'stroke="{accent}" stroke-width="1" opacity=".35"/>')
    for i, (px, py) in enumerate(pts):
        o.append(f'<circle class="fl" cx="{px}" cy="{py}" r="2.6" fill="{accent}" '
                 f'filter="url(#cg)" style="animation-delay:{i*0.42:.2f}s"/>')
    o.append('</g>')

    # shine sweep
    o.append(f'<rect class="sl" x="-120" y="0" width="90" height="{H}" fill="#ffffff" '
             f'opacity=".035" transform="skewX(-18)"/>')

    # accent bar
    o.append(f'<rect x="0" y="0" width="5" height="{H}" fill="url(#cbar)"/>')

    o.append(f'<text x="26" y="46" font-size="24" font-weight="800" letter-spacing=".3" '
             f'fill="{TXT}">{escape(title)}</text>')

    # chips
    cx = 26.0
    for i, c in enumerate(chips):
        fs = 12.5
        w = sans_w(c, fs) + 30
        o.append(f'<g opacity=".95">'
                 f'<rect x="{cx:.1f}" y="70" width="{w:.1f}" height="26" rx="13" '
                 f'fill="{accent}" fill-opacity=".12" stroke="{accent}" stroke-opacity=".38" '
                 f'stroke-width="1"/>'
                 f'<circle class="fl" cx="{cx+12:.1f}" cy="83" r="3" fill="{accent}" '
                 f'style="animation-delay:{i*0.5:.2f}s"/>'
                 f'<text x="{cx+22:.1f}" y="87.5" font-size="{fs}" fill="{TXT}" '
                 f'opacity=".92">{escape(c)}</text></g>')
        cx += w + 9

    o.append(f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="14" fill="none" '
             f'stroke="{LINE}" stroke-width="1.5"/>')
    o.append('</g></svg>')
    (OUT / fname).write_text("\n".join(o))


# ──────────────────────────────────────────────────────────── tech stack
def stack_matrix(groups, fname):
    W = 1200
    PADL, LABW, ROWH, TOP = 26, 148, 56, 22
    H = TOP + ROWH * len(groups) + 18
    o = [head(W, H, "tech stack")]
    o.append('<defs>')
    o.append(f'<linearGradient id="sb" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG0}"/>'
             f'</linearGradient>')
    o.append('<filter id="sg" x="-80%" y="-80%" width="260%" height="260%">'
             '<feGaussianBlur stdDeviation="2" result="b"/>'
             '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    o.append(f'<clipPath id="sc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    o.append('</defs>')
    o.append('<style>@keyframes pd{0%,100%{opacity:.35}50%{opacity:1}}'
             '.pd{animation:pd 3.2s ease-in-out infinite}</style>')
    o.append('<g clip-path="url(#sc)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#sb)"/>')

    n = 0
    for gi, (label, accent, items) in enumerate(groups):
        y = TOP + ROWH * gi
        if gi:
            o.append(f'<line x1="{PADL}" y1="{y-4}" x2="{W-PADL}" y2="{y-4}" stroke="{LINE}" '
                     f'stroke-width="1" opacity=".7"/>')
        o.append(f'<rect x="{PADL}" y="{y+14}" width="3" height="20" rx="1.5" fill="{accent}"/>')
        o.append(f'<text x="{PADL+14}" y="{y+30}" font-size="13.5" font-weight="700" '
                 f'letter-spacing="1.1" fill="{accent}">{escape(label.upper())}</text>')
        cx = float(PADL + LABW)
        for it in items:
            fs = 13.5
            w = sans_w(it, fs) + 32
            o.append(f'<g><rect x="{cx:.1f}" y="{y+9}" width="{w:.1f}" height="30" rx="15" '
                     f'fill="{accent}" fill-opacity=".10" stroke="{accent}" '
                     f'stroke-opacity=".34" stroke-width="1"/>'
                     f'<circle class="pd" cx="{cx+13:.1f}" cy="{y+24}" r="3.2" fill="{accent}" '
                     f'filter="url(#sg)" style="animation-delay:{(n%9)*0.34:.2f}s"/>'
                     f'<text x="{cx+24:.1f}" y="{y+29}" font-size="{fs}" fill="{TXT}" '
                     f'opacity=".93">{escape(it)}</text></g>')
            cx += w + 10
            n += 1

    o.append(f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="16" fill="none" '
             f'stroke="{LINE}" stroke-width="1.5"/>')
    o.append('</g></svg>')
    (OUT / fname).write_text("\n".join(o))


# ───────────────────────────────────────────────────────────────── footer
def footer(fname):
    W, H = 1200, 200
    o = [head(W, H, "let's build something")]
    o.append('<defs>')
    o.append(f'<linearGradient id="fbg" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0%" stop-color="{BG0}"/><stop offset="100%" stop-color="#171a2b"/>'
             f'</linearGradient>')
    o.append(sweep("fw", BLUE, PURPLE, CYAN, 9))
    o.append('<filter id="fb"><feGaussianBlur stdDeviation="34"/></filter>')
    o.append(f'<clipPath id="fc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    o.append('</defs>')
    o.append('<style>@keyframes bk{0%,49%{opacity:1}50%,100%{opacity:0}}'
             '@keyframes wv{0%{transform:translateX(0)}100%{transform:translateX(-400px)}}'
             '@keyframes fp{0%,100%{opacity:.3}50%{opacity:.9}}'
             '.bk{animation:bk .95s step-end infinite}'
             '.wv{animation:wv 11s linear infinite}'
             '.fp{animation:fp 3.4s ease-in-out infinite}</style>')
    o.append('<g clip-path="url(#fc)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#fbg)"/>')
    o.append(f'<g filter="url(#fb)" opacity=".55">'
             f'<ellipse cx="260" cy="180" rx="240" ry="90" fill="{BLUE}" opacity=".35"/>'
             f'<ellipse cx="950" cy="30" rx="260" ry="90" fill="{PURPLE}" opacity=".30"/></g>')

    # drifting wave band
    o.append('<g class="wv" opacity=".5">')
    for k in range(5):
        ox = k * 400
        o.append(f'<path d="M{ox} 150 q 100 -34 200 0 t 200 0" fill="none" stroke="url(#fw)" '
                 f'stroke-width="2" opacity=".55"/>')
        o.append(f'<path d="M{ox} 168 q 100 -34 200 0 t 200 0" fill="none" stroke="url(#fw)" '
                 f'stroke-width="1.2" opacity=".32"/>')
    o.append('</g>')

    for i, (px, py, r) in enumerate([(90, 46, 3), (170, 92, 2.2), (250, 34, 2.6), (60, 128, 2.4),
                                     (1010, 40, 2.4), (1120, 88, 2.8), (940, 120, 2.2),
                                     (1150, 36, 2.0)]):
        col = [BLUE, PURPLE, CYAN, GREEN][i % 4]
        o.append(f'<circle class="fp" cx="{px}" cy="{py}" r="{r}" fill="{col}" '
                 f'style="animation-delay:{i*0.4:.1f}s"/>')

    o.append(f'<text x="{W/2}" y="72" text-anchor="middle" font-size="15" letter-spacing="4.5" '
             f'fill="{BLUE}" opacity=".85" font-family="{MONO}">GOT AN IDEA WORTH BUILDING?</text>')
    o.append(f'<text x="{W/2}" y="118" text-anchor="middle" font-size="38" font-weight="800" '
             f'letter-spacing="1" fill="url(#fw)">LET\'S MAKE IT RUN.</text>')

    line = "vaibhavdangaich@gmail.com"
    o.append(f'<text x="{W/2 - 12}" y="152" text-anchor="middle" font-size="14.5" '
             f'font-family="{MONO}" fill="{GREEN}">'
             f'<tspan fill="{DIM}">~ $ </tspan>mail {line}</text>')
    tw = len(f"~ $ mail {line}") * 8.7
    o.append(f'<rect class="bk" x="{W/2 - 12 + tw/2 + 5:.0f}" y="140" width="8.5" height="15" '
             f'fill="{GREEN}"/>')
    o.append(f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="16" fill="none" '
             f'stroke="{LINE}" stroke-width="1.5"/>')
    o.append('</g></svg>')
    (OUT / fname).write_text("\n".join(o))


# ───────────────────────────────────────────────────────── experience timeline
def timeline(entries, fname):
    """Vertical timeline: (org, role, dates, [desc lines], accent)."""
    W, PADL, SPINE = 1200, 26, 62
    TOP = 30
    heights = [78 + 22 * len(e[3]) for e in entries]
    H = TOP + sum(heights) + 16
    o = [head(W, H, "experience timeline")]
    o.append('<defs>')
    o.append(f'<linearGradient id="tlbg" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG0}"/>'
             f'</linearGradient>')
    o.append(f'<linearGradient id="spine" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0%" stop-color="{BLUE}" stop-opacity=".95"/>'
             f'<stop offset="55%" stop-color="{PURPLE}" stop-opacity=".7"/>'
             f'<stop offset="100%" stop-color="{CYAN}" stop-opacity=".15"/></linearGradient>')
    o.append('<filter id="tg" x="-90%" y="-90%" width="280%" height="280%">'
             '<feGaussianBlur stdDeviation="3" result="b"/>'
             '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    o.append(f'<clipPath id="tlc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    o.append('</defs>')
    o.append('<style>@keyframes np{0%,100%{opacity:.45}50%{opacity:1}}'
             '@keyframes fall{0%{transform:translateY(-14px);opacity:0}'
             '100%{transform:translateY(340px);opacity:0}'
             '12%{opacity:1}88%{opacity:1}}'
             '.np{animation:np 3s ease-in-out infinite}'
             '.fall{animation:fall 6s linear infinite}</style>')
    o.append('<g clip-path="url(#tlc)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#tlbg)"/>')
    o.append(f'<rect x="{SPINE-1}" y="{TOP-6}" width="2" height="{H-TOP-14}" fill="url(#spine)"/>')
    o.append(f'<circle class="fall" cx="{SPINE}" cy="{TOP}" r="2.6" fill="{CYAN}" '
             f'filter="url(#tg)"/>')

    y = TOP
    for org, role, dates, lines, accent in entries:
        o.append(f'<circle class="np" cx="{SPINE}" cy="{y+14}" r="6.5" fill="{accent}" '
                 f'filter="url(#tg)"/>')
        o.append(f'<circle cx="{SPINE}" cy="{y+14}" r="11" fill="none" stroke="{accent}" '
                 f'stroke-opacity=".35" stroke-width="1.5"/>')
        o.append(f'<text x="{SPINE+34}" y="{y+20}" font-size="19" font-weight="800" '
                 f'fill="{TXT}">{escape(org)}</text>')
        rx = SPINE + 34 + sans_w(org, 19) + 16
        o.append(f'<text x="{rx:.0f}" y="{y+20}" font-size="13.5" font-weight="600" '
                 f'letter-spacing=".4" fill="{accent}">{escape(role)}</text>')
        dw = sans_w(dates, 12) + 26
        o.append(f'<rect x="{W-PADL-dw:.0f}" y="{y+3}" width="{dw:.0f}" height="24" rx="12" '
                 f'fill="{accent}" fill-opacity=".12" stroke="{accent}" stroke-opacity=".32"/>')
        o.append(f'<text x="{W-PADL-dw/2:.0f}" y="{y+19}" text-anchor="middle" font-size="12" '
                 f'font-family="{MONO}" fill="{accent}">{escape(dates)}</text>')
        ly = y + 44
        for ln in lines:
            o.append(f'<text x="{SPINE+34}" y="{ly}" font-size="13.5" fill="{DIM}">'
                     f'{escape(ln)}</text>')
            ly += 22
        y += 78 + 22 * len(lines)

    o.append(f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="16" fill="none" '
             f'stroke="{LINE}" stroke-width="1.5"/>')
    o.append('</g></svg>')
    (OUT / fname).write_text("\n".join(o))


# ────────────────────────────────────────────────────────── publication card
def publication(arxiv_id, title_lines, authors, venue, results, fname):
    W = 1200
    H = 96 + 30 * len(title_lines) + 74
    o = [head(W, H, f"preprint {arxiv_id}: {' '.join(title_lines)}")]
    o.append('<defs>')
    o.append(f'<linearGradient id="pbg" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0%" stop-color="#15182a"/><stop offset="100%" stop-color="{BG0}"/>'
             f'</linearGradient>')
    o.append(sweep("pbar", PURPLE, "#ffffff", CYAN, 7))
    o.append(f'<radialGradient id="pglow" cx="90%" cy="10%" r="55%">'
             f'<stop offset="0%" stop-color="{PURPLE}" stop-opacity=".26"/>'
             f'<stop offset="100%" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>')
    o.append('<filter id="pg" x="-80%" y="-80%" width="260%" height="260%">'
             '<feGaussianBlur stdDeviation="2.4" result="b"/>'
             '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    o.append(f'<clipPath id="pc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    o.append('</defs>')
    o.append('<style>@keyframes pf{0%,100%{opacity:.3}50%{opacity:1}}'
             '.pf{animation:pf 3.2s ease-in-out infinite}</style>')
    o.append('<g clip-path="url(#pc)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#pbg)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#pglow)"/>')
    o.append(f'<rect x="0" y="0" width="5" height="{H}" fill="url(#pbar)"/>')

    # doc + graph motif, top right
    o.append(f'<g opacity=".5" transform="translate(1020,26)">')
    o.append(f'<rect x="0" y="0" width="52" height="66" rx="5" fill="none" stroke="{PURPLE}" '
             f'stroke-width="1.4" opacity=".7"/>')
    for i, ly in enumerate((14, 24, 34, 44, 54)):
        wd = (34, 30, 36, 22, 28)[i]
        col = "#f7768e" if i in (1, 3) else PURPLE
        o.append(f'<rect x="9" y="{ly}" width="{wd}" height="4" rx="2" fill="{col}" '
                 f'opacity="{0.75 if i in (1,3) else 0.4}"/>')
    gp = [(84, 12), (120, 30), (86, 52), (128, 62), (150, 24)]
    for a, b in ((0, 1), (1, 2), (1, 3), (1, 4), (2, 3)):
        o.append(f'<line x1="{gp[a][0]}" y1="{gp[a][1]}" x2="{gp[b][0]}" y2="{gp[b][1]}" '
                 f'stroke="{CYAN}" stroke-width="1" opacity=".45"/>')
    for i, (px, py) in enumerate(gp):
        o.append(f'<circle class="pf" cx="{px}" cy="{py}" r="3.4" fill="{CYAN}" '
                 f'filter="url(#pg)" style="animation-delay:{i*0.4:.1f}s"/>')
    o.append('</g>')

    o.append(f'<rect x="26" y="24" width="86" height="24" rx="12" fill="{PURPLE}" '
             f'fill-opacity=".16" stroke="{PURPLE}" stroke-opacity=".45"/>')
    o.append(f'<text x="69" y="40" text-anchor="middle" font-size="11.5" font-weight="700" '
             f'letter-spacing="1.6" fill="{PURPLE}">PREPRINT</text>')
    o.append(f'<text x="126" y="41" font-size="13" font-family="{MONO}" fill="{CYAN}">'
             f'{escape(arxiv_id)}</text>')
    o.append(f'<text x="{126 + len(arxiv_id)*7.8 + 18:.0f}" y="41" font-size="12.5" '
             f'fill="{DIM}">{escape(venue)}</text>')

    ty = 78
    for ln in title_lines:
        o.append(f'<text x="26" y="{ty}" font-size="21" font-weight="800" fill="{TXT}">'
                 f'{escape(ln)}</text>')
        ty += 30
    o.append(f'<text x="26" y="{ty+2}" font-size="13" fill="{DIM}">{escape(authors)}</text>')

    cx, cy = 26.0, ty + 20
    for i, r in enumerate(results):
        fs = 12.5
        w = sans_w(r, fs) + 30
        col = (CYAN, GREEN, BLUE, PURPLE, AMBER)[i % 5]
        o.append(f'<g><rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="27" rx="13.5" '
                 f'fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".38"/>'
                 f'<circle class="pf" cx="{cx+13:.1f}" cy="{cy+13.5}" r="3" fill="{col}" '
                 f'style="animation-delay:{i*0.45:.2f}s"/>'
                 f'<text x="{cx+24:.1f}" y="{cy+18}" font-size="{fs}" fill="{TXT}" '
                 f'opacity=".93">{escape(r)}</text></g>')
        cx += w + 9

    o.append(f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="16" fill="none" '
             f'stroke="{LINE}" stroke-width="1.5"/>')
    o.append('</g></svg>')
    (OUT / fname).write_text("\n".join(o))


# ──────────────────────────────────────────────────────────── signal tiles
def signal_strip(tiles, fname):
    W, H, PAD, GAP = 1200, 112, 26, 12
    tw = (W - 2 * PAD - GAP * (len(tiles) - 1)) / len(tiles)
    o = [head(W, H, "; ".join(f"{v} {l}" for v, l, _ in tiles))]
    o.append('<defs>')
    o.append(f'<linearGradient id="gbg" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG0}"/>'
             f'</linearGradient>')
    for i, (_, _, col) in enumerate(tiles):
        o.append(f'<linearGradient id="tv{i}" x1="0" y1="0" x2="0" y2="1">'
                 f'<stop offset="0%" stop-color="#ffffff"/>'
                 f'<stop offset="100%" stop-color="{col}"/></linearGradient>')
    o.append(f'<clipPath id="gc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    o.append('</defs>')
    o.append('<style>@keyframes tp{0%,100%{opacity:.25}50%{opacity:.75}}'
             '.tp{animation:tp 3.6s ease-in-out infinite}</style>')
    o.append('<g clip-path="url(#gc)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#gbg)"/>')
    for i, (val, label, col) in enumerate(tiles):
        x = PAD + i * (tw + GAP)
        o.append(f'<rect class="tp" x="{x:.1f}" y="18" width="{tw:.1f}" height="76" rx="12" '
                 f'fill="{col}" fill-opacity=".07" style="animation-delay:{i*0.5:.1f}s"/>')
        o.append(f'<rect x="{x:.1f}" y="18" width="{tw:.1f}" height="76" rx="12" fill="none" '
                 f'stroke="{col}" stroke-opacity=".28" stroke-width="1"/>')
        o.append(f'<text x="{x+tw/2:.1f}" y="58" text-anchor="middle" font-size="27" '
                 f'font-weight="800" fill="url(#tv{i})">{escape(val)}</text>')
        o.append(f'<text x="{x+tw/2:.1f}" y="80" text-anchor="middle" font-size="11.5" '
                 f'letter-spacing=".7" fill="{DIM}">{escape(label)}</text>')
    o.append(f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="16" fill="none" '
             f'stroke="{LINE}" stroke-width="1.5"/>')
    o.append('</g></svg>')
    (OUT / fname).write_text("\n".join(o))


# ─────────────────────────────────────────────────────────────────── build
section_header("01", "EXPERIENCE", "where I've shipped", BLUE, "s-exp.svg")
section_header("02", "RESEARCH", "preprint on arXiv", PURPLE, "s-research.svg")
section_header("03", "FEATURED BUILDS", "things I actually shipped", CYAN, "s-builds.svg")
section_header("04", "TECH STACK", "what I reach for", GREEN, "s-stack.svg")
section_header("05", "BY THE NUMBERS", "commits, streaks, languages", AMBER, "s-stats.svg")
section_header("06", "THE SNAKE", "it eats my contribution graph", "#f7768e", "s-snake.svg")

signal_strip([
    ("8.4", "CGPA · BIT MESRA", BLUE),
    ("400+", "DSA PROBLEMS SOLVED", PURPLE),
    ("TOP 5", "IEEE CTF · 200+ TEAMS", CYAN),
    ("arXiv", "PREPRINT PUBLISHED", GREEN),
    ("v1.5.1", "MNEX LIVE ON NPM", AMBER),
], "signal.svg")

timeline([
    ("123 of AI", "Software Development Engineer Intern", "May 2026 – Jul 2026", [
        "Cohort learning platform on Next.js + Node/TypeScript over Azure — enrollment, scheduling, streaks, XP leaderboards, certificates.",
        "Owned monetization: Razorpay orders, subscriptions and webhooks, idempotent entitlements, a ledger-based credits system across 3 tiers.",
        "Built a recommendation engine on vector embeddings and semantic search (Azure OpenAI) targeting each learner's weak concepts.",
    ], BLUE),
    ("Konect U", "Artificial Intelligence Intern", "Feb 2026 – May 2026", [
        "Secure real-time ingestion with Apache NiFi + Kafka routing 4 document formats for a defence-oriented government intelligence project.",
        "LangChain LLM workflows and Neo4j knowledge graphs lifted entity-search recall from 70% to 95% with zero false merges.",
    ], PURPLE),
    ("Konect U", "Full Stack Intern", "Oct 2025 – Dec 2025", [
        "Full-stack delivery in an agile team — client requirements into technical specs, third-party API integration.",
    ], CYAN),
    ("BIT Mesra", "B.Tech, Artificial Intelligence & Machine Learning", "Sep 2023 – Sep 2027", [
        "CGPA 8.4 · final year · Ranchi, India",
    ], GREEN),
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

project_card("mnex", ["5-tier memory", "LangGraph", "npm v1.5.1"], BLUE, "card-mnex.svg")
project_card("FOIAtlas", ["Kùzu", "Gemini", "GraphRAG"], PURPLE, "card-foiatlas.svg")
project_card("Context Graph", ["Python", "Neo4j", "FastAPI"], CYAN, "card-contextgraph.svg")
project_card("Visual Activity Agent", ["Chrome MV3", "Supabase", "Gemini Vision"], GREEN,
             "card-vaa.svg")
project_card("Order Supervisor", ["Temporal", "Python", "durable"], AMBER, "card-supervisor.svg")
project_card("Servicing Agent", ["Policy-as-Code", "audit chain", "Python"], "#f7768e",
             "card-servicing.svg")

stack_matrix([
    ("Languages", BLUE, ["Python", "TypeScript", "JavaScript", "C++", "C", "SQL"]),
    ("AI & agents", PURPLE, ["LangGraph", "LangChain", "Gemini", "Azure OpenAI", "Ollama",
                             "Temporal"]),
    ("Web", CYAN, ["Next.js", "React", "Node.js", "Express", "FastAPI", "Tailwind",
                   "Three.js"]),
    ("Data & graphs", GREEN, ["Neo4j", "Kùzu", "PostgreSQL", "MongoDB", "SQLite", "Supabase",
                              "Vector DBs"]),
    ("Infra & tools", AMBER, ["Docker", "Azure", "Kafka", "NiFi", "Git", "GitHub Actions",
                              "Vercel", "Postman", "Jest"]),
], "stack.svg")

footer("footer.svg")
print("generated:", ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))
