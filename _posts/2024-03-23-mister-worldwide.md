---
layout: post
title: "Mr. Worldwide, the Friendly Github Landing Gif Maker"
date: 2024-03-23
categories: python gif polyglot
---

**Mr. Worldwide** is a Python tool that generates animated GIFs of a single word translated into many languages, each displayed against a culturally relevant background image.

![Mr. Worldwide Demo](https://raw.githubusercontent.com/enrique/mr.worldwide/main/worldwide_demo.gif)

### Key Features

*   **Multi-language Support**: Automatically translates words like "Hello" and "Love" into over 100 languages.
*   **Dynamic Backgrounds**: Uses country-specific images when available (from `hello_assets/` and `love_assets/`).
*   **Smart Color Selection**: Automatically chooses the best text color and outline for maximum contrast against dynamic backgrounds.
*   **Automatic Font Scaling**: Ensures long translations fit perfectly within the image dimensions.
*   **Regional Ordering**: Frames are ordered by region (Europe, Asia, Africa, etc.) for a logical flow.
*   **Unicode Excellence**: Automatically selects the correct Noto font for different scripts (Arabic, Devanagari, CJK, etc.).
*   **Visual Effects**: Supports rainbow text and flag-colored text.

### Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/enrique/mr.worldwide.git
    cd mr.worldwide
    ```

2.  **Run the setup script**:
    ```bash
    bash setup.sh
    source venv/bin/activate
    ```

3.  **(Optional) Download assets**:
    ```bash
    python3 download_assets.py
    ```

### Usage Examples

#### Mr. Worldwide Mode (The Full Experience)
Generate a GIF with background images, smart colors, and regional ordering:
```bash
python3 mr-worldwide.py --text "Love" --use_icons --smart_color --delay 500 --gif_path "love_worldwide.gif"
```

#### Custom Text Array
Provide your own list of words:
```bash
python3 mr-worldwide.py --text_array "Hola, Bonjour, Ciao, привет" --size "400,200" --rainbow --delay 300
```

#### Basic Example
```bash
python3 mr-worldwide.py --text "Hello" --size "512,512" --delay 500
```

### Advanced Options

| Option | Description |
| :--- | :--- |
| `--text` | The word to translate (e.g., "Hello", "Love"). |
| `--use_icons` | Enable country-specific background images. |
| `--smart_color` | Pick high-contrast text colors automatically. |
| `--rainbow` | Apply a shifting rainbow effect to the text. |
| `--use_flag_colors` | Color the text based on the country's flag. |
| `--size` | Image dimensions in `width,height`. |
| `--delay` | Time between frames in milliseconds. |
| `--languages` | List of ISO codes or `all`. |





