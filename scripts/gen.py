#!/usr/bin/env python3
"""Render the static profile SVGs into assets/.  Run: python3 scripts/gen.py

GitHub shows the README about 830px wide, so a 1200px-wide asset is scaled to ~0.7.
Body text is therefore >= 20px in the source to land around 14px on screen.
"""
import textwrap
from pathlib import Path

from theme import (BLOOD, BLUE, HOT, IMPACT, INK, INK2, MONO, MUTED, RED, SANS, WHITE, YELLOW,
                   backdrop, chip, esc, spider, splatter, svg, swoosh, web)

OUT = Path(__file__).resolve().parent.parent / "assets"


def lines(text, width):
    return textwrap.wrap(text, width)


# --------------------------------------------------------------------------- hero
def hero():
    w, h = 1200, 440
    tag = "agents that finish the job · graphs that remember"
    tag_w = len(tag) * 26 * .6
    name = lambda fill, cls="": "\n".join(
        f'<text class="{cls}" x="70" y="{y}" fill="{fill}" style="font:400 132px {IMPACT};letter-spacing:2px">{t}</text>'
        for t, y in (("VAIBHAV", 200), ("DANGAICH", 318)))
    body = f"""{backdrop(w, h, (.8, .35))}
<rect x="560" width="640" height="{h}" fill="url(#halftone)" opacity=".22"/>
{spider(930, 215, 330, RED, .18)}
{swoosh(40, 330, 720, 46, RED, .95)}
{splatter(1040, 110, 34, 3)}
{splatter(780, 395, 22, 9, HOT, .8)}
{splatter(1150, 360, 16, 5, BLUE, .7)}
{web(0, 0, 230, 0, 90)}
<line x1="1200" y1="0" x2="985" y2="170" stroke="{WHITE}" stroke-opacity=".7" stroke-width="2" class="strand"/>
<g transform="translate(70 46) rotate(-2)">
  <rect width="430" height="40" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>
  <text x="16" y="28" fill="{INK}" style="font:800 19px {MONO};letter-spacing:2px">B.TECH AI&amp;ML · BIT MESRA '27</text>
</g>
<g class="blue">{name(BLUE)}</g>
<g class="red">{name(RED)}</g>
<g>{name(WHITE)}</g>
<clipPath id="type"><rect x="70" y="360" height="50" width="0">
  <animate attributeName="width" from="0" to="{tag_w + 10:.0f}" begin=".6s" dur="2.2s" fill="freeze"/></rect></clipPath>
<text x="72" y="396" clip-path="url(#type)" fill="{WHITE}" style="font:600 26px {MONO}">{esc(tag)}</text>
<rect x="74" y="374" width="14" height="28" fill="{HOT}" class="cursor">
  <animate attributeName="x" from="74" to="{74 + tag_w:.0f}" begin=".6s" dur="2.2s" fill="freeze"/></rect>
<g transform="translate(1000 300) rotate(-8)">
  <path d="M0 30 L22 0 L40 22 L66 -6 L82 20 L112 2 L118 34 L150 40 L120 58 L132 88 L98 74 L80 104 L64 76 L30 96 L36 64 L2 60 Z"
        fill="{YELLOW}" stroke="{INK}" stroke-width="4"/>
  <text x="70" y="58" text-anchor="middle" fill="{INK}" style="font:400 30px {IMPACT}">THWIP!</text>
</g>"""
    style = f"""
  .red  {{ animation: gr 4s infinite; transform: translate(5px,-4px); }}
  .blue {{ animation: gb 4s infinite; transform: translate(-5px,4px); }}
  @keyframes gr {{ 0%,86%,100% {{ transform: translate(5px,-4px); }} 88% {{ transform: translate(18px,-2px); }}
                   90% {{ transform: translate(-10px,-6px); }} 92% {{ transform: translate(8px,-3px); }} }}
  @keyframes gb {{ 0%,86%,100% {{ transform: translate(-5px,4px); }} 88% {{ transform: translate(-16px,6px); }}
                   90% {{ transform: translate(12px,2px); }} 92% {{ transform: translate(-7px,5px); }} }}
  .cursor {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .strand {{ stroke-dasharray: 280; stroke-dashoffset: 280; animation: thwip .9s .2s ease-out forwards; }}
  @keyframes thwip {{ to {{ stroke-dashoffset: 0; }} }}"""
    return svg(w, h, body, "Vaibhav Dangaich: agents that finish the job, graphs that remember", style=style)


# --------------------------------------------------------------------------- signal strip
def signal():
    w, h = 1200, 190
    stats = [("2", "ARXIV PREPRINTS"), ("400+", "DSA PROBLEMS"), ("TOP 5", "IEEE CTF · 200+"),
             ("8.4", "CGPA · BIT MESRA"), ("v1.5.1", "MNEX LIVE ON NPM")]
    pw = w / len(stats)
    parts = [f'<rect width="{w}" height="{h}" fill="{INK}"/>']
    for i, (big, label) in enumerate(stats):
        x = i * pw
        fill = INK2 if i % 2 else "#0f0b0e"
        parts.append(f'<g transform="skewX(-6) translate({x + 10:.0f} 0)">'
                     f'<rect x="4" y="18" width="{pw - 12:.0f}" height="{h - 36}" fill="{fill}" stroke="#3a1820" stroke-width="2"/>'
                     f'<rect x="4" y="18" width="{pw - 12:.0f}" height="{h - 36}" fill="url(#halftone)" opacity=".10"/></g>')
        cx = x + pw / 2
        color = RED if i % 2 == 0 else WHITE
        parts.append(f'<text x="{cx:.0f}" y="104" text-anchor="middle" fill="{color}" style="font:400 64px {IMPACT}">{esc(big)}</text>')
        parts.append(f'<text x="{cx:.0f}" y="142" text-anchor="middle" fill="{MUTED}" style="font:700 17px {MONO};letter-spacing:1px">{esc(label)}</text>')
    return svg(w, h, "\n".join(parts), "2 arXiv preprints · 400+ DSA problems · Top 5 of 200+ teams at IEEE CTF · CGPA 8.4 · mnex v1.5.1 on npm")


# --------------------------------------------------------------------------- section headers
def section(num, title, kicker, seed):
    w, h = 1200, 120
    tw = len(title) * 40
    body = f"""<rect width="{w}" height="{h}" fill="{INK}"/>
<rect x="{w - 420}" width="420" height="{h}" fill="url(#halftone)" opacity=".18"/>
{swoosh(150, 70, tw + 40, 30, RED, .9)}
{splatter(w - 120, 52, 16, seed, RED, .75)}
<text x="40" y="88" fill="{RED}" style="font:400 74px {IMPACT}">{num}</text>
<text x="160" y="86" fill="{WHITE}" style="font:400 66px {IMPACT};letter-spacing:2px">{esc(title)}</text>
<text x="{w - 40}" y="{h - 22}" text-anchor="end" fill="{MUTED}" style="font:700 17px {MONO};letter-spacing:3px">{esc(kicker)}</text>"""
    return svg(w, h, body, f"{num} {title}")


# --------------------------------------------------------------------------- experience timeline
JOBS = [
    ("123 OF AI", "SDE INTERN", "MAY – JUL 2026",
     "Razorpay payments, idempotent entitlements and a ledger-based credits system; a vector-search recommendation engine on Azure OpenAI."),
    ("KONECT U", "AI INTERN", "FEB – MAY 2026",
     "NiFi + Kafka ingestion for a defence intelligence project; Neo4j knowledge graphs lifted entity-search recall from 70% to 95% with zero false merges."),
    ("KONECT U", "FULL-STACK INTERN", "OCT – DEC 2025",
     "Full-stack delivery in an agile team, from client requirements to shipped features."),
    ("BIT MESRA", "B.TECH · AI & ML", "2023 – 2027",
     "CGPA 8.4 · final year · Ranchi, India."),
]


def timeline():
    w, row = 1200, 150
    h = 40 + row * len(JOBS)
    parts = [backdrop(w, h, (.95, .1)), f'<line x1="70" y1="50" x2="70" y2="{h - 50}" stroke="{RED}" stroke-width="4" stroke-dasharray="2 10" stroke-linecap="round"/>']
    for i, (org, role, when, text) in enumerate(JOBS):
        y = 40 + i * row
        parts.append(f'<circle cx="70" cy="{y + 38}" r="13" fill="{INK}" stroke="{RED}" stroke-width="4"/>'
                     f'<circle cx="70" cy="{y + 38}" r="4" fill="{RED}"/>')
        parts.append(f'<text x="112" y="{y + 52}" fill="{WHITE}" style="font:400 44px {IMPACT};letter-spacing:1px">{esc(org)}</text>')
        ow = len(org) * 22 + 130
        parts.append(f'<text x="{ow}" y="{y + 50}" fill="{HOT}" style="font:800 20px {MONO};letter-spacing:2px">{esc(role)}</text>')
        c, cw = chip(0, 0, when, 18, WHITE, BLOOD, RED)
        parts.append(f'<g transform="translate({w - 50 - cw:.0f} {y + 22})">{c}</g>')
        for j, ln in enumerate(lines(text, 88)):
            parts.append(f'<text x="112" y="{y + 92 + j * 30}" fill="{MUTED}" style="font:500 22px {SANS}">{esc(ln)}</text>')
    return svg(w, h, "\n".join(parts), "Experience: " + "; ".join(f"{o} {r} {d}: {t}" for o, r, d, t in JOBS))


# --------------------------------------------------------------------------- research
PAPERS = [
    ("arXiv:2608.10644 · AUG 2026",
     "Curate Before You Connect: Identity and Ontology Tagging in a Production Knowledge Graph",
     ["98,795 docs", "537K entities", "2.2M relations", "spurious roles 36 → 4"]),
    ("arXiv:2607.28662 · JUL 2026",
     "An Ontology-Guided, Deduplication-Aware Extraction Layer for Knowledge Graph Construction",
     ["recall 70% → 95%", "zero false merges", "−94% catalog overhead", "Qwen3.5-9B"]),
]


def research():
    w, block = 1200, 230
    h = 30 + block * len(PAPERS)
    parts = [backdrop(w, h, (.1, .9)), spider(1080, h / 2, 260, RED, .1)]
    for i, (meta, title, chips) in enumerate(PAPERS):
        y = 30 + i * block
        parts.append(f'<rect x="30" y="{y}" width="{w - 60}" height="{block - 24}" rx="12" fill="#120a0d" stroke="#3a1820" stroke-width="2"/>')
        parts.append(f'<rect x="30" y="{y}" width="8" height="{block - 24}" fill="{RED}"/>')
        parts.append(f'<g transform="translate(64 {y + 22})"><rect width="118" height="32" fill="{YELLOW}"/>'
                     f'<text x="59" y="23" text-anchor="middle" fill="{INK}" style="font:800 17px {MONO};letter-spacing:2px">PREPRINT</text></g>')
        parts.append(f'<text x="200" y="{y + 45}" fill="{MUTED}" style="font:700 19px {MONO}">{esc(meta)}</text>')
        for j, ln in enumerate(lines(title, 58)):
            parts.append(f'<text x="64" y="{y + 95 + j * 38}" fill="{WHITE}" style="font:700 32px {SANS}">{esc(ln)}</text>')
        x = 64
        for c in chips:
            g, cw = chip(x, y + 155, c, 19, WHITE, BLOOD, RED)
            parts.append(g)
            x += cw + 12
    return svg(w, h, "\n".join(parts), "Research: " + " | ".join(t for _, t, _ in PAPERS))


# --------------------------------------------------------------------------- project cards
CARDS = {
    "mnex": ("MNEX", "Terminal coding agent: planner → executor → critic, 5-tier memory.", ["LangGraph", "Node.js", "npm"]),
    "orbit": ("ORBIT", "Distributed Go scheduler. Exactly-once runs, 1,000/1,000 jobs in 97s.", ["Go", "etcd", "Kafka", "K8s"]),
    "foiatlas": ("FOIATLAS", "FOIA records → knowledge graph. Every redaction is a node.", ["GraphRAG", "Kùzu", "Gemini"]),
    "servicing": ("SERVICING AGENT", "The LLM proposes, policy-as-code decides. Hash-chained audit trail.", ["Python", "Agents"]),
    "contextgraph": ("CONTEXT GRAPH", "Your AI agent's session as a Neo4j graph, so the next one resumes.", ["Neo4j", "FastAPI"]),
    "vaa": ("VISUAL ACTIVITY", "Chrome MV3 extension + Gemini vision explains your browsing.", ["MV3", "Node", "Gemini"]),
}


def card(key, seed):
    w, h = 600, 330
    title, hook, tags = CARDS[key]
    size = 66 if len(title) <= 10 else 52
    parts = [backdrop(w, h, (.9, .1)),
             f'<rect x="{w - 230}" width="230" height="{h}" fill="url(#halftone)" opacity=".2"/>',
             spider(w - 85, 95, 150, RED, .22),
             splatter(w - 60, h - 60, 14, seed, RED, .6),
             f'<rect width="{w}" height="10" fill="{RED}"/>',
             swoosh(28, 108, len(title) * size * .5 + 10, 22, RED, .85),
             f'<text x="32" y="112" fill="{WHITE}" style="font:400 {size}px {IMPACT};letter-spacing:1px">{esc(title)}</text>']
    for j, ln in enumerate(lines(hook, 38)):
        parts.append(f'<text x="34" y="{178 + j * 36}" fill="{WHITE}" fill-opacity=".88" style="font:600 27px {SANS}">{esc(ln)}</text>')
    x = 34
    for t in tags:
        g, cw = chip(x, h - 66, t, 20, WHITE, "#2a1218", RED)
        parts.append(g)
        x += cw + 10
    return svg(w, h, "\n".join(parts), f"{title.title()}: {hook}")


# --------------------------------------------------------------------------- footer
def footer():
    w, h = 1200, 260
    body = f"""{backdrop(w, h, (.5, 1.1))}
<rect width="{w}" height="{h}" fill="url(#halftone)" opacity=".12"/>
{web(w, h, 260, 180, 270)}
{web(0, h, 200, 270, 360)}
{splatter(220, 70, 20, 11, RED, .7)}
{splatter(990, 200, 18, 13, BLUE, .6)}
{spider(600, 34, 46, RED, .9)}
<text x="600" y="100" text-anchor="middle" fill="{MUTED}" style="font:700 19px {MONO};letter-spacing:5px">GOT AN IDEA WORTH BUILDING?</text>
{swoosh(330, 176, 540, 26, RED, .9)}
<text x="600" y="176" text-anchor="middle" fill="{WHITE}" style="font:400 84px {IMPACT};letter-spacing:2px">LET'S MAKE IT RUN.</text>
<text x="600" y="226" text-anchor="middle" fill="{WHITE}" style="font:600 24px {MONO}">~ $ mail <tspan fill="{HOT}">vaibhavdangaich@gmail.com</tspan></text>"""
    return svg(w, h, body, "Got an idea worth building? Let's make it run: vaibhavdangaich@gmail.com")


def main():
    OUT.mkdir(exist_ok=True)
    files = {
        "hero.svg": hero(),
        "signal.svg": signal(),
        "timeline.svg": timeline(),
        "research.svg": research(),
        "footer.svg": footer(),
        "s-exp.svg": section("01", "EXPERIENCE", "WHERE I'VE SHIPPED", 21),
        "s-research.svg": section("02", "RESEARCH", "PREPRINTS ON ARXIV", 22),
        "s-builds.svg": section("03", "FEATURED BUILDS", "THINGS I ACTUALLY SHIPPED", 23),
        "s-stack.svg": section("04", "TECH STACK", "WHAT I REACH FOR", 24),
        "s-stats.svg": section("05", "BY THE NUMBERS", "REGENERATED DAILY", 25),
    }
    for i, key in enumerate(CARDS):
        files[f"card-{key}.svg"] = card(key, 30 + i)
    for name, content in files.items():
        (OUT / name).write_text(content)
    print(f"wrote {len(files)} files to {OUT}")


if __name__ == "__main__":
    main()
