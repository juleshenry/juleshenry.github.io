---
layout: post
title: "Mr. Worldwide, the Friendly Github Landing Gif Maker"
date: 2024-03-23
categories: python gif polyglot
---
Mr.Worldwide
Description:
Mr.Worldwide is a Python script that takes a single word as input and generates a GIF showing that word translated into multiple languages.

Usage:

css
Copy code
python3 mr-worldwide.py [options]
Options:

--size: Size of the output GIF in pixels (e.g., "256,256").
--text: The word to be translated.
--font_path: Path to the font file to be used.
--font_color: Color of the text in RGB format (e.g., "256,32,32").
--background_color: Background color of the GIF in RGB format (e.g., "256,256,256").
--languages: Specify the languages to translate the word into (e.g., "all" for all supported languages).
--delay: Delay between frames in milliseconds.
--text_array: Specify multiple words separated by commas for translation into multiple languages.
--font_size: Size of the font.
--round_robin: Toggle round-robin translation mode (true or false).
--background_images: List of image paths for background images (must match the number of languages).
--smart_color_picker: Automatically pick font color based on background for optimal contrast.
Examples:

# Basic:

python3 mr-worldwide.py --size "256,256" --text hello! --font_path fonts/arial.ttf --font_color "256,32,32" --background_color "256,256,256" --languages all --delay 300

# Intermediate:

# Text Array Example
python3 mr-worldwide.py --size "1024,256" --text_array "你好, Hola, Hello, नमस्ते, السلام عليكم, হ্যালো, Olá, Привет, こんにちは, ਸਤ ਸ੍ਰੀ ਅਕਾਲ, Hallo, Halo, 呵呵, హలో, Xin chào, नमस्कार, 안녕하세요, Bonjour, வணக்கம், Merhaba, اسلام و علیکم, 哈囉, สวัสดี, નમસ્તે, Pronto" --font_path fonts/arial.ttf --font_color "0,0,0" --font_size=32 --background_color "256,256,256" --languages all --delay 300

# Sinusoidal Example
python3 mr-worldwide.py --size "256,256" --text hello! --font_path fonts/arial.ttf --font_color "256,32,32" --background_color "256,256,256" --languages all --delay sine:"500,100"




