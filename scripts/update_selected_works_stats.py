#!/usr/bin/env python3
"""Regenerate selected-works.html (the Projects page) from public GitHub repos.

Star-sorted within each category. Blacklist + category map live beside this
script; the category map can also point a repo at its blog write-up, replace
its GitHub description with a better one, correct its language label, and
give the card a thumbnail. Live sites that are not repos are listed first,
from selected_works_sites.txt.
"""

from __future__ import annotations

import hashlib
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
SCRIPT_DIR = Path(__file__).resolve().parent
BLACKLIST_FILE = SCRIPT_DIR / "selected_works_blacklist.txt"
CATEGORIES_FILE = SCRIPT_DIR / "selected_works_categories.txt"
SITES_FILE = SCRIPT_DIR / "selected_works_sites.txt"

LANG_DOT = {
    "Python": "python",
    "JavaScript": "js",
    "TypeScript": "ts",
    "Shell": "shell",
    "CSS": "css",
    "Julia": "julia",
    "WebAssembly": "wasm",
    "Jupyter Notebook": "jupyter",
    "HTML": "js",
    "Rust": "shell",
    "Go": "shell",
}

def load_blacklist() -> set[str]:
    names: set[str] = set()
    if not BLACKLIST_FILE.exists():
        return names
    for line in BLACKLIST_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        names.add(line.split("/")[-1])
    return names


def load_sites() -> list[tuple[str, str, str, str]]:
    """Return [(name, url, description, image), ...] in file order."""
    sites: list[tuple[str, str, str, str]] = []
    if not SITES_FILE.exists():
        return sites
    for line in SITES_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, url, description, image = (
            [part.strip() for part in line.split("|", 3)] + ["", "", ""]
        )[:4]
        sites.append((name, url, description, image))
    return sites


def load_categories() -> tuple[
    list[str], dict[str, str], dict[str, str], dict[str, str], dict[str, str], dict[str, str]
]:
    """Return ([title, ...], and per repo name: title, writeup_url, description, language, image)."""
    order: list[str] = []
    mapping: dict[str, str] = {}
    writeups: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    languages: dict[str, str] = {}
    images: dict[str, str] = {}
    if not CATEGORIES_FILE.exists():
        return order, mapping, writeups, descriptions, languages, images
    current: str | None = None
    for line in CATEGORIES_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("## "):
            current = line[3:].split("|", 1)[0].strip()
            order.append(current)
            continue
        # plain # comments (not ## section headers)
        if line.startswith("#"):
            continue
        if current is None:
            continue
        fields = [part.strip() for part in line.split("|", 4)] + ["", "", "", ""]
        repo, writeup, description, language, image = (
            fields[0].split("/")[-1], fields[1], fields[2], fields[3], fields[4]
        )
        mapping[repo] = current
        if writeup:
            writeups[repo] = writeup
        if description:
            descriptions[repo] = description
        if language:
            languages[repo] = language
        if image:
            images[repo] = image
    return order, mapping, writeups, descriptions, languages, images


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


def lang_badge(language: str | None) -> str:
    if not language:
        return (
            '<span class="work-lang">'
            '<span class="lang-dot notes"></span>Other</span>'
        )
    dot = LANG_DOT.get(language, "notes")
    label = html.escape(language)
    return (
        f'<span class="work-lang">'
        f'<span class="lang-dot {dot}"></span>{label}</span>'
    )


def thumb(image: str, href: str) -> str:
    """Card thumbnail. A duplicate of the title link, so hidden from keyboard and screen readers."""
    if not image:
        return ""
    # Pages caches images for 10 minutes; a content hash makes a replaced thumbnail show at once
    local = ROOT / image.lstrip("/")
    if local.is_file():
        image += "?v=" + hashlib.sha1(local.read_bytes()).hexdigest()[:8]
    return (
        f'\n      <a class="work-thumb" href="{html.escape(href)}" tabindex="-1" aria-hidden="true">'
        f'<img src="{html.escape(image)}" alt="" width="160" height="120" loading="lazy" decoding="async"></a>'
    )


def render_site_card(name: str, url: str, description: str, image: str) -> str:
    return f"""    <li class="work{' has-thumb' if image else ''}">{thumb(image, url)}
      <h3 class="work-title"><a href="{html.escape(url)}">{html.escape(name)}</a></h3>
      <p class="work-desc">{html.escape(description)}</p>
      <p class="work-meta">
        <span class="work-lang"><span class="lang-dot site"></span>Live site</span>
      </p>
    </li>"""


def render_card(
    repo: dict,
    writeup: str | None,
    description: str | None,
    language: str | None,
    image: str | None,
) -> str:
    name = repo["name"]
    url = repo["html_url"]
    desc = (
        description
        or (repo.get("description") or "").strip()
        or "No description yet."
    )
    meta = lang_badge(language or repo.get("language"))
    if writeup:
        meta += f'\n        <a href="{html.escape(writeup)}">Write-up</a>'
    return f"""    <li class="work{' has-thumb' if image else ''}">{thumb(image or "", writeup or url)}
      <h3 class="work-title"><a href="{html.escape(url)}">{html.escape(name)}</a></h3>
      <p class="work-desc">{html.escape(desc)}</p>
      <p class="work-meta">
        {meta}
      </p>
    </li>"""


def render_section(
    title: str,
    repos: list[dict],
    writeups: dict[str, str],
    descriptions: dict[str, str],
    languages: dict[str, str],
    images: dict[str, str],
) -> str:
    cards = "\n\n".join(
        render_card(
            r,
            writeups.get(r["name"]),
            descriptions.get(r["name"]),
            languages.get(r["name"]),
            images.get(r["name"]),
        )
        for r in repos
    )
    return wrap_section(title, cards)


def wrap_section(title: str, cards: str) -> str:
    return f"""<section class="works-section">
  <h2 class="section-label">{html.escape(title)}</h2>
  <ul class="works-list">

{cards}

  </ul>
</section>"""


def render_page(
    repos: list[dict],
    sites: list[tuple[str, str, str, str]],
    cat_order: list[str],
    cat_map: dict[str, str],
    writeups: dict[str, str],
    descriptions: dict[str, str],
    languages: dict[str, str],
    images: dict[str, str],
) -> str:
    buckets: dict[str, list[dict]] = {title: [] for title in cat_order}
    other: list[dict] = []
    for r in repos:
        title = cat_map.get(r["name"])
        if title and title in buckets:
            buckets[title].append(r)
        else:
            other.append(r)

    for title in buckets:
        buckets[title].sort(
            key=lambda r: (-int(r.get("stargazers_count") or 0), r["name"].lower())
        )
    other.sort(
        key=lambda r: (-int(r.get("stargazers_count") or 0), r["name"].lower())
    )

    sections: list[str] = []
    if sites:
        sections.append(
            wrap_section("Live sites", "\n\n".join(render_site_card(*s) for s in sites))
        )
    for title in cat_order:
        if buckets[title]:
            sections.append(
                render_section(
                    title, buckets[title], writeups, descriptions, languages, images
                )
            )
    if other:
        sections.append(
            render_section("Other", other, writeups, descriptions, languages, images)
        )

    body = "\n\n".join(sections)
    return f"""---
layout: default
title: Projects
description: Live sites, open-source tools and experiments by Julian Henry, grouped by what they are for.
---

<header class="page-head">
  <h1>Projects</h1>
  <p class="page-lede">Live sites, then open-source tools grouped by what they are for. Each card links to the code, and to a write-up where there is one.</p>
  <p class="pills"><a class="pill" href="https://github.com/{USER}">GitHub</a></p>
</header>

<!-- AUTO-GENERATED by scripts/update_selected_works_stats.py. Edit the blacklist, categories and sites files, not the cards. -->
{body}
"""


def main() -> int:
    blacklist = load_blacklist()
    sites = load_sites()
    cat_order, cat_map, writeups, descriptions, languages, images = load_categories()
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

    page = render_page(
        selected, sites, cat_order, cat_map, writeups, descriptions, languages, images
    )
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
    uncategorized = [r["name"] for r in selected if r["name"] not in cat_map]
    if uncategorized:
        print("uncategorized → Other:", ", ".join(sorted(uncategorized)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
