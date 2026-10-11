#!/usr/bin/env python3
"""Render a self-hosted stats card from the GitHub GraphQL API.

Usage: GITHUB_TOKEN=... python3 scripts/stats.py <login> <out.svg>
Runs daily in .github/workflows/profile.yml, so no third-party stats service can break the README.
"""
import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import date, timedelta

from theme import BLOOD, HOT, IMPACT, INK, MONO, MUTED, RED, WHITE, backdrop, esc, spider, splatter, svg

QUERY = """query($login: String!) {
  user(login: $login) {
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
      totalCount
      nodes { languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
    }
    contributionsCollection {
      totalCommitContributions
      contributionCalendar { totalContributions weeks { contributionDays { contributionCount date } } }
    }
  }
}"""


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        body = json.load(res)
    if "errors" in body:
        raise SystemExit(f"GraphQL error: {body['errors']}")
    return body["data"]["user"]


def streaks(days):
    """(current, longest) runs of days with >= 1 contribution. Today may still be empty."""
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        longest = max(longest, run)
    current = 0
    for i, d in enumerate(reversed(days)):
        if d["contributionCount"]:
            current += 1
        elif i:  # an empty *today* doesn't break the streak
            break
    return current, longest


def top_languages(repos, n=5):
    sizes = Counter()
    for repo in repos:
        for edge in repo["languages"]["edges"]:
            sizes[edge["node"]["name"]] += edge["size"]
    total = sum(sizes.values()) or 1
    return [(name, size / total) for name, size in sizes.most_common(n)]


def render(user):
    cal = user["contributionsCollection"]["contributionCalendar"]
    days = [d for wk in cal["weeks"] for d in wk["contributionDays"]]
    current, longest = streaks(days)
    langs = top_languages(user["repositories"]["nodes"])

    w, h = 1200, 470
    parts = [backdrop(w, h, (.95, .05)), spider(1110, 400, 150, RED, .12), splatter(1130, 70, 16, 41, RED, .6)]

    tiles = [(f"{cal['totalContributions']:,}", "CONTRIBUTIONS · 1 YR"),
             (f"{current}d", "CURRENT STREAK"),
             (f"{longest}d", "LONGEST STREAK"),
             (f"{user['contributionsCollection']['totalCommitContributions']:,}", "COMMITS · 1 YR"),
             (str(user["repositories"]["totalCount"]), "PUBLIC REPOS")]
    tw = (w - 60) / len(tiles)
    for i, (big, label) in enumerate(tiles):
        x = 30 + i * tw
        parts.append(f'<rect x="{x + 6:.0f}" y="28" width="{tw - 12:.0f}" height="128" rx="10" fill="#120a0d" stroke="#3a1820" stroke-width="2"/>')
        parts.append(f'<text x="{x + tw / 2:.0f}" y="100" text-anchor="middle" fill="{RED if i % 2 == 0 else WHITE}" style="font:400 58px {IMPACT}">{esc(big)}</text>')
        parts.append(f'<text x="{x + tw / 2:.0f}" y="134" text-anchor="middle" fill="{MUTED}" style="font:700 15px {MONO}">{esc(label)}</text>')

    # Last 26 weeks as a red heatmap.
    recent = cal["weeks"][-26:]
    peak = max((d["contributionCount"] for wk in recent for d in wk["contributionDays"]), default=1) or 1
    cell, gap, x0, y0 = 19, 5, 36, 196
    parts.append(f'<text x="{x0}" y="184" fill="{MUTED}" style="font:700 16px {MONO};letter-spacing:2px">LAST 26 WEEKS</text>')
    for wi, wk in enumerate(recent):
        for d in wk["contributionDays"]:
            dow = date.fromisoformat(d["date"]).isoweekday() % 7
            c = d["contributionCount"]
            fill = "#1d1215" if not c else RED
            op = 1 if not c else .35 + .65 * min(1, c / peak)
            parts.append(f'<rect x="{x0 + wi * (cell + gap)}" y="{y0 + dow * (cell + gap)}" width="{cell}" height="{cell}" rx="4" fill="{fill}" fill-opacity="{op:.2f}"/>')

    # Top languages as bars.
    lx, ly = 690, 196
    parts.append(f'<text x="{lx}" y="184" fill="{MUTED}" style="font:700 16px {MONO};letter-spacing:2px">TOP LANGUAGES</text>')
    for i, (name, share) in enumerate(langs):
        y = ly + i * 48
        parts.append(f'<text x="{lx}" y="{y + 22}" fill="{WHITE}" style="font:700 20px {MONO}">{esc(name)}</text>')
        parts.append(f'<rect x="{lx + 180}" y="{y + 6}" width="270" height="18" rx="9" fill="#1d1215"/>')
        parts.append(f'<rect x="{lx + 180}" y="{y + 6}" width="{max(8, 270 * share):.0f}" height="18" rx="9" fill="{HOT if i == 0 else RED}" fill-opacity="{1 - i * .13:.2f}"/>')
        parts.append(f'<text x="{lx + 462}" y="{y + 22}" fill="{MUTED}" style="font:700 18px {MONO}">{share * 100:.0f}%</text>')

    parts.append(f'<text x="{w - 30}" y="{h - 16}" text-anchor="end" fill="{BLOOD}" style="font:700 14px {MONO}">updated {date.today().isoformat()}</text>')
    title = (f"{cal['totalContributions']} contributions in the last year, current streak {current} days, "
             f"longest {longest} days; top languages: " + ", ".join(n for n, _ in langs))
    return svg(w, h, "\n".join(parts), title)


def _check():
    mk = lambda counts: [{"contributionCount": c, "date": (date(2026, 1, 1) + timedelta(i)).isoformat()} for i, c in enumerate(counts)]
    assert streaks(mk([1, 1, 0, 1, 1, 1, 0])) == (3, 3)  # empty today doesn't reset
    assert streaks(mk([1, 1, 1, 0, 0])) == (0, 3)
    assert streaks(mk([0, 2, 3])) == (2, 2)


if __name__ == "__main__":
    _check()
    login, out = sys.argv[1], sys.argv[2]
    with open(out, "w") as f:
        f.write(render(fetch(login, os.environ["GITHUB_TOKEN"])))
    print(f"wrote {out}")
