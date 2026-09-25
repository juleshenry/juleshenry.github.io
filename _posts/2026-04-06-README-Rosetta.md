---
layout: post
title: "README Rosetta: Open Source in Every Language"
date: 2026-04-06
---

[View on GitHub](https://github.com/juleshenry/readme_rosetta)

Most open source projects have English-only documentation. This is a barrier. A significant percentage of the global developer population reads English as a second language, and for many, the friction of parsing a technical README in a non-native language is enough to keep them from adopting a tool they would otherwise love.

README Rosetta automates the translation of README files and Sphinx documentation into 70+ languages using locally-running LLMs via Ollama. No API keys. No cloud costs. No data leaving your machine. One command:

```bash
readme-rosetta --langs es fr de ja zh ar hi
```

The project is on [PyPI](https://pypi.org/project/readme-rosetta/) (v0.1.7) and [GitHub](https://github.com/juleshenry/readme_rosetta). MIT licensed.

![Rosetta Stone](https://github.com/juleshenry/readme_rosetta/blob/main/readme_image.png?raw=1)

## The Problem with LLM Translation of Structured Text

Raw LLMs are notoriously unreliable for translating Markdown. I learned this the hard way. Here is a non-exhaustive list of things that go wrong when you naively ask an LLM to translate a README:

1. **Code block corruption.** The LLM helpfully "translates" your Python code. `import requests` becomes `importar solicitudes`. My God.
2. **Hallucinated links.** The original has `[docs](https://example.com/docs)`. The translation has `[documentos](https://ejemplo.com/documentos)`. That URL does not exist.
3. **Conversational preambles.** Instead of returning the translation, the model starts with "Sure! Here's the translation of your README into Spanish:" and then provides the translation. Now your translated README begins with an English sentence from the LLM.
4. **Line count explosion.** A single-sentence bullet point becomes a three-sentence paragraph because the LLM decided to elaborate.
5. **Placeholder mangling.** If you use `{variable}` template syntax, the LLM either translates the variable name or drops the braces.

README Rosetta addresses all of this with a multi-layered defense system.

## Code Block Protection

Before sending any text to the LLM, README Rosetta replaces all fenced code blocks with numbered placeholders:

~~~
```python
def hello():
    print("world")
```
~~~

becomes `ROSETTA_CB_0`. The LLM never sees the code. After translation, the placeholders are swapped back in. The code is untouched. This is the single most important feature in the entire tool, and it is embarrassingly simple.

For Sphinx documentation, the same approach extends to reStructuredText syntax: directives, roles, and inline literals are replaced with `ROSETTA_RST_N` placeholders. The LLM translates the prose. The markup survives.

## Hallucination Detection and Retry Logic

After each translation, README Rosetta validates the output:

1. **Placeholder count check.** If the original had 5 `ROSETTA_CB_N` placeholders and the translation has 4, something was dropped. Retry.
2. **Link verification.** Compare URLs in the original and translation. If the translation contains URLs not present in the original, the LLM hallucinated them. Retry.
3. **Conversational response detection.** If the translation starts with patterns like "Here is," "Sure!", "Of course," or "I'd be happy to," the LLM prefixed its response with preamble. Strip it or retry.
4. **Line count sanity.** If a single input line produced 5+ output lines, the LLM elaborated instead of translating. Retry.

Each retry uses an increasingly strict system prompt. The first attempt is polite: "Please translate the following Markdown content." The retry is firm: "Translate ONLY the text. Do NOT add any explanations, preambles, or commentary. Do NOT modify URLs, code blocks, or formatting."

Up to 2 retries per chunk. If all fail, the original text is preserved with a comment noting the failed translation.

## Translation Caching

Translations are cached in a `.rosetta_cache.json` file using MD5 hashes of the source content. If you re-run the tool after editing only one section of your README, only that section gets re-translated. The rest is served from cache. This matters when you are translating into 20+ languages -- you do not want to re-translate 500 chunks because you fixed a typo in one paragraph.

## Output Modes

**Split mode** (default): Generates separate files -- `README.es.md`, `README.fr.md`, `README.ja.md`, etc. Each file is self-contained and includes a navigation table at the top (the "Rosetta stone") with links to all translated versions.

**Unified mode** (`--no-split`): Appends all translations into a single `README.md`, separated by HTML comment markers. Useful for projects that want everything in one file.

The navigation table itself is auto-generated:

```
| [English](README.md) | [Español](README.es.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | ...
```

## Sphinx Integration

For larger projects with Sphinx documentation, README Rosetta can set up the entire i18n pipeline:

```bash
readme-rosetta --sphinx --langs es fr de ja --docs-dir ./docs
```

This runs `sphinx-build gettext` to generate `.pot` files, creates locale directories, translates the `.po` files (with rST syntax protection), and builds localized HTML. The output is a complete set of translated Sphinx docs ready for hosting.

## GitHub Actions

A workflow template is included that installs Ollama on a GitHub Actions runner, pulls the model, and auto-translates on every push to `main`. Internationalization that happens automatically in CI rather than being an aspirational backlog item that never gets done.

## Usage

```bash
pip install readme-rosetta
```

```bash
# Translate to 5 languages
readme-rosetta --langs es fr de ja zh

# Use a specific model
readme-rosetta --model llama3.2 --langs ar hi ko

# Dry run (preview without writing)
readme-rosetta --dry-run --langs es

# Sphinx docs
readme-rosetta --sphinx --langs es fr de ja --docs-dir ./docs
```

Configuration can also live in `pyproject.toml`:

```toml
[tool.readme-rosetta]
model = "llama3.2"
languages = ["es", "fr", "de", "ja", "zh"]
```

## The Technical Core

The source is 7 files. `translator.py` handles the Ollama integration, caching, and retry logic. `markdown_handler.py` handles code block protection/restoration and the navigation table. `sphinx_handler.py` handles the Sphinx i18n pipeline. `lang_codes.py` is a mapping of 70+ ISO language codes to language names. `cli.py` orchestrates everything.

The tool defaults to `llama3.2` via Ollama because it is small enough to run on a laptop, fast enough for batch translation, and accurate enough for technical prose. You can swap in any Ollama-compatible model.

The hallucination detection is regex-heavy by design. I considered using a second LLM call to validate the first LLM's output, but that doubles the cost and introduces a new failure mode (what if the validator hallucinates?). Pattern matching is deterministic, fast, and does not argue with you.

Making documentation accessible should not be hard. It should not require a translation team or a localization budget. It should be one command. That is what README Rosetta does.
