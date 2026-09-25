#!/usr/bin/env python3
"""Refresh Selected Works header stats and per-card star counts from GitHub."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

USER = "juleshenry"
PAGE = Path(__file__).resolve().parents[1] / "selected-works.html"
API = f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&sort=updated"


def fetch_repos() -> list[dict]:
    req = urllib.request.Request(
        API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"{USER}-selected-works-stats",
            **(
                {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
                if os.environ.get("GITHUB_TOKEN")
                else {}
            ),
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def main() -> int:
    try:
        repos = fetch_repos()
    except urllib.error.HTTPError as e:
        print(f"GitHub API error: {e.code} {e.reason}", file=sys.stderr)
        return 1

    by_full = {
        r["full_name"]: r
        for r in repos
        if not r.get("fork") and not r.get("archived")
    }

    html = PAGE.read_text(encoding="utf-8")

    # Featured cards on the page (order preserved)
    featured = re.findall(
        r'<p class="work-card-repo">([^<]+)</p>',
        html,
    )
    if not featured:
        print("No work-card-repo entries found", file=sys.stderr)
        return 1

    featured_repos = []
    for name in featured:
        name = name.strip()
        if name in by_full:
            featured_repos.append(by_full[name])
        else:
            print(f"warn: not found or skipped: {name}", file=sys.stderr)

    n_repos = len(featured)
    langs = sorted(
        {
            r["language"]
            for r in featured_repos
            if r.get("language")
        }
    )
    n_langs = len(langs)
    n_stars = sum(r.get("stargazers_count", 0) for r in featured_repos)

    # Replace the three labeled header stats (do not stop at nested </div>)
    stats_pat = re.compile(
        r'(<div class="works-stats">\s*'
        r'<div class="stat">\s*<span class="stat-number">)\d+'
        r'(</span>\s*<span class="stat-label">Repositories</span>[\s\S]*?'
        r'<span class="stat-number">)\d+'
        r'(</span>\s*<span class="stat-label">Languages</span>[\s\S]*?'
        r'<span class="stat-number">)\d+'
        r'(</span>\s*<span class="stat-label">Stars</span>)',
    )
    html2, n = stats_pat.subn(
        rf"\g<1>{n_repos}\g<2>{n_langs}\g<3>{n_stars}\g<4>",
        html,
        count=1,
    )
    if n != 1:
        print("Could not locate .works-stats block", file=sys.stderr)
        return 1
    html = html2

    # Per-card stars: for each card, find work-card-repo then nearest star-count
    star_re = re.compile(
        r'(<span class="star-count"><svg[^>]*>.*?</svg>)\s*\d+(</span>)',
        re.S,
    )

    def patch_card(card: str) -> str:
        m = re.search(r'<p class="work-card-repo">([^<]+)</p>', card)
        if not m:
            return card
        full = m.group(1).strip()
        repo = by_full.get(full)
        if not repo:
            return card
        stars = repo.get("stargazers_count", 0)

        def repl_stars(sm: re.Match[str]) -> str:
            return f"{sm.group(1)} {stars}{sm.group(2)}"

        return star_re.sub(repl_stars, card, count=1)

    html = re.sub(
        r'<li class="work-card">.*?</li>',
        lambda m: patch_card(m.group(0)),
        html,
        flags=re.S,
    )

    if html == PAGE.read_text(encoding="utf-8"):
        print(
            f"unchanged: {n_repos} repos, {n_langs} languages, {n_stars} stars"
        )
        return 0

    PAGE.write_text(html, encoding="utf-8")
    print(
        f"updated: {n_repos} repos, {n_langs} languages ({', '.join(langs)}), "
        f"{n_stars} stars"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
