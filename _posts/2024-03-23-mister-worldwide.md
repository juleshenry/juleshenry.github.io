---
layout: post
title: "Mr. Worldwide: Turn a Word into a Multilingual GIF"
date: 2024-03-23
categories: python gif polyglot
---

[Mr. Worldwide](https://github.com/juleshenry/mr.worldwide) takes one word—say,
`Hello` or `Love`—and turns it into a looping GIF. Each frame shows a
translation in a different language, optionally paired with a country-specific
image.

## Demos

Here are a few of the pre-generated examples from the repository:

### Hello

![Hello translated into many languages](https://raw.githubusercontent.com/juleshenry/mr.worldwide/main/examples/demos/hello.gif)

### Love

![Love translated into many languages](https://raw.githubusercontent.com/juleshenry/mr.worldwide/main/examples/demos/love.gif)

### Love with regional backgrounds

![Love with country-specific backgrounds](https://raw.githubusercontent.com/juleshenry/mr.worldwide/main/examples/demos/love_regional.gif)

### Flag colors and rainbow text

![Love rendered with flag colors](https://raw.githubusercontent.com/juleshenry/mr.worldwide/main/examples/demos/flag_love.gif)

![Rainbow text demo](https://raw.githubusercontent.com/juleshenry/mr.worldwide/main/examples/demos/test_rainbow.gif)

The result is a small, friendly visual for a README, landing page, or anywhere
else a plain translation list would feel a little too static.

## Why it is interesting

The translation is only the beginning. A useful multilingual GIF also has to
solve a few visual problems:

- **Different scripts need different fonts.** Arabic, Devanagari, CJK, and
  other writing systems cannot reliably be rendered with one default font.
- **Translations have different shapes and lengths.** The renderer scales the
  text so that a long translation does not overflow the frame.
- **Backgrounds change the contrast.** Smart color selection chooses a text
  color and outline that remain readable over each image.
- **The sequence should feel intentional.** Frames can be ordered by region
  rather than appearing as an arbitrary list of languages.

The project also supports rainbow text and flag-colored text when the default
styling is not enough.

## Install it

Clone the repository and run its setup script:

```bash
git clone https://github.com/juleshenry/mr.worldwide.git
cd mr.worldwide
bash setup.sh
source venv/bin/activate
```

Background images are optional. Download them if you want to use the
image-backed mode:

```bash
python3 download_assets.py
```

## Make a GIF

This command generates the full experience: translated text, background
images, automatic contrast, and a 500 ms delay between frames.

```bash
python3 mr-worldwide.py \
  --text "Love" \
  --use_icons \
  --smart_color \
  --delay 500 \
  --gif_path "love_worldwide.gif"
```

For a lighter version without background images:

```bash
python3 mr-worldwide.py --text "Hello" --size "512,512" --delay 500
```

You can also provide your own sequence of words:

```bash
python3 mr-worldwide.py \
  --text_array "Hola, Bonjour, Ciao, привет" \
  --size "400,200" \
  --rainbow \
  --delay 300
```

## Options

| Option | Description |
| :--- | :--- |
| `--text` | Word to translate, such as `Hello` or `Love`. |
| `--text_array` | Use a custom comma-separated list instead of translations. |
| `--use_icons` | Add country-specific background images. |
| `--smart_color` | Choose high-contrast text colors automatically. |
| `--rainbow` | Apply a shifting rainbow effect to the text. |
| `--use_flag_colors` | Color each frame using the corresponding country’s flag. |
| `--size` | Set image dimensions as `width,height`. |
| `--delay` | Set the time between frames in milliseconds. |
| `--languages` | Choose language codes or use `all`. |

## A small project with a global output

Mr. Worldwide is deliberately simple: one input word becomes a sequence of
small visual moments. The interesting engineering is in the details that make
those moments hold together—font selection across Unicode scripts, sizing text
to its frame, and keeping the foreground legible as the background changes.

That combination makes the project more than a translation demo. It is a
compact example of how internationalization becomes a design problem as soon
as text leaves the terminal and enters an image.
