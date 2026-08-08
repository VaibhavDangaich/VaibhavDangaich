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


# ─────────────────────────────────────────────────────────────────── build
section_header("01", "FEATURED BUILDS", "things I actually shipped", BLUE, "s-builds.svg")
section_header("02", "TECH STACK", "what I reach for", PURPLE, "s-stack.svg")
section_header("03", "BY THE NUMBERS", "commits, streaks, languages", CYAN, "s-stats.svg")
section_header("04", "THE SNAKE", "it eats my contribution graph", GREEN, "s-snake.svg")

project_card("mnex", ["Node", "LangGraph", "on npm"], BLUE, "card-mnex.svg")
project_card("FOIAtlas", ["Next.js", "Kùzu", "Gemini"], PURPLE, "card-foiatlas.svg")
project_card("Context Graph", ["Python", "Neo4j", "FastAPI"], CYAN, "card-contextgraph.svg")
project_card("Visual Activity Agent", ["Chrome MV3", "Supabase", "Gemini Vision"], GREEN,
             "card-vaa.svg")
project_card("Order Supervisor", ["Temporal", "Python", "durable"], AMBER, "card-supervisor.svg")
project_card("Servicing Agent", ["Policy-as-Code", "audit chain", "Python"], "#f7768e",
             "card-servicing.svg")

stack_matrix([
    ("Languages", BLUE, ["Python", "TypeScript", "JavaScript", "C++", "Go", "Bash"]),
    ("AI & agents", PURPLE, ["LangGraph", "LangChain", "Gemini", "Temporal", "Ollama"]),
    ("Web", CYAN, ["Next.js", "React", "React Native", "Node.js", "FastAPI", "Tailwind",
                   "Redux", "Three.js"]),
    ("Data", GREEN, ["Neo4j", "Kùzu", "PostgreSQL", "Supabase", "MongoDB", "Prisma"]),
    ("Ship it", AMBER, ["Git", "GitHub Actions", "Vercel", "Render", "npm"]),
], "stack.svg")

footer("footer.svg")
print("generated:", ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))
