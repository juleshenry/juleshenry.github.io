---
layout: post
title: "README Rosetta: Docs in Every Language"
date: 2026-04-06
description: "A CLI that translates READMEs and Sphinx docs with a local Ollama model, and the checks that stop the model from mangling code and links."
---

Most open source projects have English-only documentation. This is a barrier. A significant percentage of the global developer population reads English as a second language, and for many, the friction of parsing a technical README in a non-native language is enough to keep them from adopting a tool they would otherwise love.

[README Rosetta](https://github.com/juleshenry/readme_rosetta) automates the translation of README files and Sphinx documentation into 70+ languages using locally running LLMs via Ollama. It needs no API key, costs nothing to run, and sends no data off your machine:

```bash
readme-rosetta --langs es fr de ja zh ar hi
```

It is on [PyPI](https://pypi.org/project/readme-rosetta/) and MIT licensed.

## The Problem with LLM Translation of Structured Text

Raw LLMs are notoriously unreliable for translating Markdown. I learned this the hard way. Here is a non-exhaustive list of things that go wrong when you naively ask an LLM to translate a README:

1. **Code block corruption.** The LLM helpfully "translates" your Python code. `import requests` becomes `importar solicitudes`.
2. **Hallucinated links.** The original has `[docs](https://example.com/docs)`. The translation has `[documentos](https://ejemplo.com/documentos)`. That URL does not exist.
3. **Conversational preambles.** Instead of returning the translation, the model starts with "Sure! Here's the translation of your README into Spanish:" and then provides the translation. Now your translated README begins with an English sentence from the LLM.
4. **Line count explosion.** A single-sentence bullet point becomes a three-sentence paragraph because the LLM decided to elaborate.
5. **Placeholder mangling.** If you use `{variable}` template syntax, the LLM either translates the variable name or drops the braces.

README Rosetta addresses each of these. Template variables need one line of config: list them under `do-not-translate`, and any translation that alters one is rejected.

## Code Block Protection

README Rosetta parses the Markdown with markdown-it-py and sends the LLM only prose segments: headings, paragraphs, table cells and the text inside HTML blocks. A fenced code block such as

~~~
```python
def hello():
    print("world")
```
~~~

is copied to the output byte for byte. The LLM never sees the code. This is the single most important feature in the entire tool, and it is embarrassingly simple. Inline syntax inside the prose (code spans, link targets, URLs, HTML tags) is swapped for numbered tokens, `⟦0⟧`, `⟦1⟧` and so on, before a segment is sent, and swapped back after translation.

For Sphinx documentation, the same approach extends to reStructuredText syntax: directive markers, roles, inline literals, links and substitutions become tokens too. The LLM translates the prose. The markup survives.

## Hallucination Detection and Retry Logic

After each translation, README Rosetta validates the output:

1. **Placeholder count check.** Every token must come back exactly once. If the original had 5 tokens and the translation has 4, something was dropped. Retry.
2. **Link verification.** Link targets and URLs are tokens, so the LLM cannot edit them. If the translation contains a link, code span, heading or HTML tag that the original lacks, the LLM invented it. Retry.
3. **Conversational response detection.** Segments go to the LLM wrapped in `<seg id="N">` tags and only the text inside the tags is kept, so a preamble such as "Sure! Here's the translation:" in front of them is discarded.
4. **Line count sanity.** If a single input line comes back as several lines, the LLM elaborated instead of translating. Segments over 40 characters must also stay between a quarter and four times their original length. Retry.
5. **Language check.** Letters from an unrelated script (Thai inside an Arabic translation), a Hindi translation written largely in Latin letters, or a sentence handed back untranslated all fail. Retry.

Segments are translated in batches. A rejected segment is retried on its own, and each retry tells the LLM why the previous attempt failed: "A previous translation of this segment was rejected because it split a single line into several lines."

Up to 2 retries per segment. If both fail, the segment keeps its source text, the run lists it, and, unless you pass `--allow-fallback`, the command exits with a non-zero status so CI notices.

## Translation Caching

Translations are cached per segment in `.rosetta/cache.json`, keyed by a SHA-256 hash of the segment text together with the languages, model and glossary. If you re-run the tool after editing one paragraph of your README, only that paragraph gets re-translated. The rest is served from cache. This matters when you are translating into 20+ languages: you do not want to re-translate 500 segments because you fixed a typo in one paragraph.

## Output Modes

**Split mode** (default): Generates separate files: `README.es.md`, `README.fr.md`, `README.ja.md`, etc. Each file is self-contained and includes a language bar at the top (the "Rosetta stone") with links to all translated versions.

**Unified mode** (`--no-split`): Appends all translations to the main `README.md`, separated by HTML comment markers. Useful for projects that want everything in one file.

The language bar writes each language's name in that language and links only to translations that exist:

```
🌐 **English** · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [中文](README.zh.md)
```

## Sphinx Integration

For larger projects with Sphinx documentation in `docs/`, README Rosetta can set up the entire i18n pipeline:

```bash
readme-rosetta --sphinx --langs es fr de ja
```

This runs `sphinx-build -M gettext` to generate `.pot` files, runs `sphinx-intl` to create `.po` catalogs for each language, translates the new and fuzzy entries (with rST syntax protection), and builds localized HTML. The output is a complete set of translated Sphinx docs ready for hosting.

## GitHub Actions

The repository doubles as a GitHub Action. The example workflow in its README runs on every push to `main` that changes `README.md`, re-translates the changed paragraphs, and opens a pull request. It calls Claude with an API key; leave out the `backend` input and the action installs Ollama on the runner and pulls the model instead. Internationalization happens automatically in CI instead of being an aspirational backlog item that never gets done.

## Usage

```bash
pip install readme-rosetta
```

```bash
# Translate to 5 languages
readme-rosetta --langs es fr de ja zh

# A bigger model for non-Latin scripts
readme-rosetta --model qwen2.5:14b --langs ar hi ko

# Dry run (preview without writing)
readme-rosetta --dry-run --langs es

# Sphinx docs
readme-rosetta --sphinx --langs es fr de ja
```

Configuration can also live in `pyproject.toml`:

```toml
[tool.readme-rosetta]
model = "qwen2.5:14b"
langs = ["es", "fr", "de", "ja", "zh"]
```

## The Technical Core

The source is small. `markdown_handler.py` parses the Markdown and picks out the prose segments. `protect.py` swaps inline syntax for tokens and back. `translator.py` handles batching, validation, retries and caching, with `markup.py` and `langcheck.py` supplying the invented-markup and language checks. `backends.py` talks to Ollama or the Anthropic API. `readme.py` builds the language bar and unified mode. `sphinx_handler.py` handles the Sphinx i18n pipeline. `lang_codes.py` is a table of 70+ ISO language codes with their English and native names and writing systems. `cli.py` orchestrates everything.

The tool defaults to `qwen2.5:7b` via Ollama because it is small enough to run on a laptop, fast enough for batch translation, and in my use accurate enough for most technical prose. You can swap in any Ollama-compatible model.

The hallucination detection is regex-heavy by design. I considered using a second LLM call to validate the first LLM's output, but that doubles the cost and introduces a new failure mode (what if the validator hallucinates?). Pattern matching is deterministic, fast, and does not argue with you.

Translating documentation should not require a translation team or a localization budget. For a README, one command is enough.
