#!/usr/bin/env python3
"""Regenerate selected-works.html from public GitHub repos (star-sorted)."""

from __future__ import annotations

import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

USER = "juleshenry"
ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "selected-works.html"
BLACKLIST_FILE = Path(__file__).resolve().parent / "selected_works_blacklist.txt"

LANG_DOT = {
    "Python": "python",
    "JavaScript": "js",
    "TypeScript": "ts",
    "Shell": "shell",
    "CSS": "css",
    "Julia": "julia",
    "WebAssembly": "wasm",
    "Jupyter Notebook": "python",
    "HTML": "js",
    "Rust": "shell",
    "Go": "shell",
}

STAR_SVG = (
    '<svg viewBox="0 0 16 16"><path d="M8 .25a.75.75 0 01.673.418l1.882 '
    "3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 "
    "01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 "
    "6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z\"/>"
    "</svg>"
)


def load_blacklist() -> set[str]:
    names: set[str] = set()
    if not BLACKLIST_FILE.exists():
        return names
    for line in BLACKLIST_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # allow owner/name or bare name
        names.add(line.split("/")[-1])
    return names


def is_notes_repo(name: str) -> bool:
    return bool(re.search(r"(^|[_-])notes?$", name, re.I))


def fetch_repos() -> list[dict]:
    out: list[dict] = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/users/{USER}/repos"
            f"?per_page=100&type=owner&sort=updated&page={page}"
        )
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": f"{USER}-selected-works",
                **(
                    {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
                    if os.environ.get("GITHUB_TOKEN")
                    else {}
                ),
            },
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            batch = json.load(resp)
        if not batch:
            break
        out.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return out


def display_title(name: str) -> str:
    # mr.worldwide → Mr. Worldwide; ghee → ghee; quantum-plankton-ml → Quantum Plankton Ml
    pretty = name.replace("_", " ").replace("-", " ")
    if pretty.lower() == name.lower() and "." in name:
        parts = name.split(".")
        return ".".join(p[:1].upper() + p[1:] if p else "" for p in parts)
    return " ".join(w[:1].upper() + w[1:] if w else "" for w in pretty.split())


def lang_badge(language: str | None) -> str:
    if not language:
        return (
            '<span class="lang-badge">'
            '<span class="lang-dot notes"></span>Other</span>'
        )
    dot = LANG_DOT.get(language, "notes")
    label = html.escape(language)
    return (
        f'<span class="lang-badge">'
        f'<span class="lang-dot {dot}"></span>{label}</span>'
    )


def render_card(repo: dict) -> str:
    full = repo["full_name"]
    name = repo["name"]
    url = repo["html_url"]
    desc = (repo.get("description") or "").strip() or "No description yet."
    stars = int(repo.get("stargazers_count") or 0)
    title = html.escape(display_title(name))
    return f"""    <li class="work-card">
      <div class="work-card-header">
        <h3 class="work-card-title"><a href="{html.escape(url)}">{title}</a></h3>
      </div>
      <p class="work-card-repo">{html.escape(full)}</p>
      <p class="work-card-desc">{html.escape(desc)}</p>
      <div class="work-card-meta">
        {lang_badge(repo.get("language"))}
        <span class="star-count">{STAR_SVG} {stars}</span>
      </div>
    </li>"""


def render_page(repos: list[dict]) -> str:
    n_repos = len(repos)
    langs = sorted({r["language"] for r in repos if r.get("language")})
    n_langs = len(langs)
    n_stars = sum(int(r.get("stargazers_count") or 0) for r in repos)
    cards = "\n\n".join(render_card(r) for r in repos)
    return f"""---
layout: default
title: Selected Works - Julian Henry — polyglot / software engineer / author
---

<h1>Selected Works</h1>
<p class="works-intro">
  Open-source projects spanning scientific computing, developer tools, image processing,
  language learning, and creative coding. Star-sorted from public GitHub repos
  (notes, the blog, and blacklisted one-offs omitted).
</p>

<div class="works-stats">
  <div class="stat">
    <span class="stat-number">{n_repos}</span>
    <span class="stat-label">Repositories</span>
  </div>
  <div class="stat">
    <span class="stat-number">{n_langs}</span>
    <span class="stat-label">Languages</span>
  </div>
  <div class="stat">
    <span class="stat-number">{n_stars}</span>
    <span class="stat-label">Stars</span>
  </div>
</div>

<!-- AUTO-GENERATED: scripts/update_selected_works_stats.py — do not hand-edit cards -->
<div class="works-section">
  <h2 class="works-section-title"><span>&#x2B50;</span> Public repositories</h2>
  <ul class="works-grid">

{cards}

  </ul>
</div>
"""


def main() -> int:
    blacklist = load_blacklist()
    try:
        raw = fetch_repos()
    except urllib.error.HTTPError as e:
        print(f"GitHub API error: {e.code} {e.reason}", file=sys.stderr)
        return 1

    selected: list[dict] = []
    skipped: list[str] = []
    for r in raw:
        name = r["name"]
        if r.get("fork") or r.get("private"):
            continue
        if name in blacklist or is_notes_repo(name):
            skipped.append(name)
            continue
        selected.append(r)

    selected.sort(
        key=lambda r: (-int(r.get("stargazers_count") or 0), r["name"].lower())
    )

    page = render_page(selected)
    if PAGE.exists() and PAGE.read_text(encoding="utf-8") == page:
        print(
            f"unchanged: {len(selected)} repos, "
            f"{sum(int(r.get('stargazers_count') or 0) for r in selected)} stars; "
            f"skipped {len(skipped)}"
        )
        return 0

    PAGE.write_text(page, encoding="utf-8")
    print(
        f"updated: {len(selected)} repos, "
        f"{sum(int(r.get('stargazers_count') or 0) for r in selected)} stars"
    )
    if skipped:
        print("skipped:", ", ".join(sorted(skipped)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
