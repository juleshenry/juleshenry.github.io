---
layout: post
title: "📦 Mr. Worldwide: Say Hello in 80 Languages, as a GIF"
date: 2026-03-30
---

[View on GitHub](https://github.com/juleshenry/mr.worldwide)

Mr. Worldwide generates animated GIFs of a single word -- "Hello," "Love," whatever you want -- translated into 80+ languages, with each translation rendered as a frame. Each frame can optionally display the translated word over a culturally relevant photograph from that country. The result is a looping, globe-trotting GIF that says your word in English, then Spanish, then Japanese, then Amharic, then Tibetan, then Yoruba, and on and on through 80+ languages.

The project is on [GitHub](https://github.com/juleshenry/mr.worldwide).

![Demo](https://github.com/juleshenry/mr.worldwide/blob/main/examples/demos/worldwide_demo.gif?raw=1)

## The Hard Problem: Rendering Every Script on Earth

Generating a GIF is easy. Pillow does that in five lines. The hard problem is rendering text correctly in 80+ writing systems.

"Hello" in English uses Latin characters. "こんにちは" uses CJK ideographs. "مرحبا" uses Arabic script (right-to-left). "สวัสดี" uses Thai. "ᓱᓇᑦᓯᐊᖅ" uses Canadian Aboriginal Syllabics. "བཀྲ་ཤིས་བདེ་ལེགས" uses Tibetan. Each of these scripts requires a different font, and many system fonts support only a handful of scripts.

Mr. Worldwide bundles 25+ Google Noto fonts to cover the full Unicode range. The font selection is automatic: for each character in the translated word, the tool checks which Unicode code point range it falls into and selects the corresponding Noto font. Arabic characters get NotoSansArabic, Devanagari gets NotoSansDevanagari, CJK gets NotoSansCJK, and so on.

The font sizing is also automatic. Each translation has a different string length and character width. "Hello" in English is 5 compact Latin characters. "Привет" in Russian is 6 Cyrillic characters of similar width. "こんにちは" in Japanese is 5 wide CJK characters. Mr. Worldwide measures the rendered text width for each translation and scales the font size to fit within the frame. No text gets cut off. No frames have tiny unreadable text in one corner.

## Smart Contrast Coloring

When overlaying text on a country photograph (say, "Bonjour" over a picture of the Eiffel Tower), the text needs to be legible. White text on a bright sky is invisible. Black text on a dark scene is invisible.

Mr. Worldwide solves this with k-means color clustering. For each background image:

1. Cluster the image pixels into dominant colors using `scipy.cluster.vq.kmeans`
2. Identify the most prominent background hues
3. Select a text color that maximizes both contrast (distance from the dominant colors) and vibrancy (saturation)

The result is text that pops against any background -- bright cyan over a dark forest, deep navy over a sunlit beach, vivid magenta over a gray cityscape.

## Flag-Color Text

An alternative to smart contrast: paint each character using the colors of the corresponding country's flag. "Hola" rendered in the red, yellow, and red of the Spanish flag. "Bonjour" in blue, white, and red. "Hallo" in the black, red, and gold of Germany.

The flag colors are extracted from SVG files stored in a `banderas/` directory (banderas is Spanish for "flags"). The tool parses the fill attributes from each SVG and maps them to character indices. Character 1 gets color 1, character 2 gets color 2, and so on, cycling through the palette.

![Flag Hello](https://github.com/juleshenry/mr.worldwide/blob/main/examples/demos/flag_hello.gif?raw=1)

## The Full CLI

```bash
python mr_worldwide.py --word Hello --use-icons --smart-colors --size 800x600
```

```bash
python mr_worldwide.py --word Love --flag-colors --delay 150 --output love_flags.gif
```

```bash
python mr_worldwide.py --text-array "Hola,Bonjour,Ciao,Hallo" --rainbow --sine-delay
```

Options include:

- `--use-icons` -- overlay text on country photographs
- `--smart-colors` -- k-means contrast text coloring
- `--flag-colors` -- paint text with country flag colors
- `--rainbow` -- hue-shift the text color across frames
- `--sine-delay` -- a sinusoidal timing effect that "dwells" on each frame in sequence, creating a wave-like viewing rhythm
- `--langs` -- filter to specific ISO language codes (e.g., `--langs es fr de ja`)
- `--size` -- output dimensions
- `--delay` -- milliseconds per frame

The example gallery includes 14 pre-built scripts covering every permutation of these options, each with a pre-generated demo GIF.

![Rainbow Demo](https://github.com/juleshenry/mr.worldwide/blob/main/examples/demos/test_rainbow.gif?raw=1)

## Design Decisions

**Why local translations instead of an API?** The 80+ translations are hardcoded in a `translations.json` file rather than fetched from Google Translate at runtime. This was deliberate. Machine translation APIs are rate-limited, cost money at scale, and produce inconsistent results for single-word translations (context-free translation of "Love" can yield wildly different results depending on the API's mood). By curating the translations manually, every output is verified and stable.

**Deduplication.** Many languages share the same word. "Hello" is "Halo" in both Indonesian and Malay. Rather than showing two identical frames, Mr. Worldwide deduplicates translations before rendering. The GIF only shows unique strings.

**Geographic ordering.** The translations are sorted by region (Europe, Asia, Africa, Americas, Oceania) with priority languages (English, Spanish, Italian, French) first. This gives the GIF a natural geographic flow rather than a random jumble.

**Background image sourcing.** The country photographs are fetched from the Pexels API and Wikimedia Commons, organized into per-country directories. The tool selects a random image from each country's directory, so regenerating the GIF produces visual variety even with the same parameters.

A fun intersection of internationalization, image processing, and creative coding. The kind of project that is both technically interesting (font detection across Unicode ranges, k-means color analysis) and produces something you can actually send to your friends.
