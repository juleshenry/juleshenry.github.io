# juleshenry.github.io

Source for [juleshenry.github.io](https://juleshenry.github.io): Julian Henry's writing and projects. Plain Jekyll, built by GitHub Pages from `main`, no plugins.

## Run it locally

```bash
bundle install
bundle exec jekyll serve
```

Then open `http://localhost:4000`. To check a build without touching the repo, point it at a scratch directory: `bundle exec jekyll build -d /tmp/site`.

## Layout

| Path | What it is |
|---|---|
| `_posts/` | Every post. Stubs with `redirect_to:` forward to wherever the post moved and are hidden from the index. |
| `_layouts/default.html`, `_layouts/post.html` | Page shell and post template. |
| `_includes/series-shelf.html` | The series listing on the home and Writing pages. |
| `_includes/post-list.html` | The listing of posts that are not part of a series. |
| `_includes/series-info.html` | Splits a post title into series, volume and chapter. |
| `_includes/*-kit.html` | Shared styles and helpers for the interactive figures in each series. |
| `_data/series.yml` | Topic and one-line blurb per series. |
| `stylesheets/site.css` | The whole theme. |
| `selected-works.html` | The Projects page. Generated; do not edit by hand. |
| `images/social/` | One 1200×630 share card per post, named after the post file. Generated. |
| `sitemap.xml`, `robots.txt` | Every page and post except redirect stubs, for search engines. |
| `scripts/` | The Projects generator, the share-card generator, and the figure scripts for individual posts. |

## Writing a post

`scripts/make_post.sh "Title of the post"` creates the file with today's date. Front matter:

```yaml
---
layout: post
title: "Title of the post"
date: 2026-10-09
description: "One sentence. Shown under the title on the Writing page and used as the meta description."
mathjax: true   # only if the post has math
---
```

The URL comes from `date:` in the front matter, not from the filename.

### Share cards

Each post gets its own card for link previews: the series and volume (or the date), the title, and for a series the row of numeral tiles. Once a post's title is final, run

```bash
node scripts/make_social_cards.mjs        # cards for posts that have none yet
node scripts/make_social_cards.mjs --all  # every card, after a title or series changes
```

It needs Playwright (`npm i -g playwright`) and Google Chrome. It also deletes cards for posts that are gone. A post without a card falls back to `images/social-card.png`.

### Series

A post joins a series through its title alone:

```yaml
title: "Sphere Eversion, Vol. III: Manifolds and Immersions"
```

Everything before `, Vol.` is the series name, the Roman numeral is the volume, and the rest is the chapter title. A leading `Back-of-the-Envelope:` is dropped for display. From that the site builds the series entry on the home and Writing pages, the kicker above the post title, and the previous/next links at the bottom of each volume. To give a new series a topic and blurb, add an entry to `_data/series.yml` with the same name.

Volumes still open with a hand-written switcher line, which the stylesheet turns into the row of numeral tiles:

```markdown
*Sphere Eversion:* [I](/blog/…) · [II](/blog/…) · **III**
```

Do not add a "Next" link or a volume list at the end of a volume. The post template adds the previous/next links.

### Headings and math

- Start sections at `#`. It renders as `<h2>`, because the post title is the page's only `<h1>`. Posts that start at `##` are styled to look the same.
- Inline math is `$…$` and is read as Markdown before MathJax sees it, so a few sequences need a safe spelling: `\lbrace`/`\rbrace` for set braces, `\lvert`/`\rvert` for bars, `^{\ast}` for a star, `\cr` for a row break. Display math is `$$…$$` with a blank line on each side.
- Mermaid and Three.js load only on pages that use them (a ```` ```mermaid ```` block, or a figure that references `THREE`).

## Projects page

`scripts/update_selected_works_stats.py` rebuilds `selected-works.html` from the public GitHub repos, and a workflow runs it daily. Three files beside it control the result:

- `selected_works_sites.txt`: live sites that are not repos, listed first (`name | URL | Description`).
- `selected_works_blacklist.txt`: repos to leave out.
- `selected_works_categories.txt`: which section each repo goes in, and optionally the post that writes it up, a description for the card, and a language label (`repo-name | /blog/… | Description | Language`).

Without a description there, the card shows the repo's description from GitHub; without a language label, the language GitHub detected.
