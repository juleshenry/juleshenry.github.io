---
layout: post
title: "SuperWand"
date: 2026-03-23
---

# [SuperWand: A Magic Wand for Image and CSS Retheming](https://github.com/juleshenry/superwand)

SuperWand takes an image, identifies its dominant color regions using KMeans clustering, and replaces those colors with any of 18 curated aesthetic themes -- Vaporwave, Cyberpunk, Tropical, Arctic, and so on. It is a magic wand for recoloring. Point it at a posterized Charizard, pick "Midnight," and out comes a moonlit dragon.

The project is on [PyPI](https://pypi.org/project/superwand/) (v0.2.10) and [GitHub](https://github.com/juleshenry/superwand). Licensed under Apache 2.0.

## How It Works

The pipeline has three stages.

### 1. Region Identification

Given an image, SuperWand uses scikit-learn's KMeans to cluster all pixels into `k` regions (default 4) by color similarity. For large images, it downsamples before clustering (because running KMeans on a 4000x3000 image with 12 million pixels is a good way to watch your laptop overheat) and then applies the cluster assignments at full resolution.

Each pixel gets a label: region 0, region 1, region 2, region 3. These regions correspond roughly to the dominant color areas -- the sky, the ground, the subject, the shadows.

### 2. Theme Injection

Each region gets mapped to a color from the chosen theme. The 18 themes are hand-curated palettes:

| Theme | Vibe |
|-------|------|
| Tropical | Warm greens, coral, turquoise |
| Cyberpunk | Neon pink, electric blue, dark purple |
| Vaporwave | Pastel pink, lavender, mint |
| Arctic | Ice blue, white, steel gray |
| Retro80s | Hot pink, electric cyan, chrome yellow |
| Volcano | Deep red, orange, obsidian black |
| ... | (12 more) |

The mapping is straightforward: the brightest region gets the lightest theme color, the darkest region gets the darkest theme color, and intermediates are matched accordingly. The result is a recolored image that preserves the original structure (edges, shapes, textures) but wears an entirely different color palette.

![Charizard Themed Examples](https://github.com/juleshenry/superwand/blob/main/examples/charizards/Cyberpunk_charizard.png?raw=1)

### 3. Gradient Application

Flat color replacement looks... flat. So SuperWand supports five gradient styles that can be applied per region:

- **Bottom-up** / **Top-down** -- vertical gradient across the region
- **Left-right** / **Right-left** -- horizontal gradient
- **Radial** -- gradient radiating from the region's centroid outward

Each gradient has a configurable polarity/bias parameter that controls where the midpoint sits. The gradient is computed as a NumPy array and multiplied element-wise against the region's pixels. The result is smooth color transitions within each region instead of uniform blocks.

![Gradient Examples](https://github.com/juleshenry/superwand/blob/main/examples/charizards/gradient_radial_charizard.png?raw=1)

## SuperWand Studio

The CLI is fine for scripting, but the real fun is the Studio -- a Flask-based web UI served locally at `http://127.0.0.1:5001`. Upload an image, and you get an interactive workspace:

- Pick a theme or set custom per-region colors
- Adjust the number of KMeans clusters (more clusters = finer region detection)
- Apply different gradient styles to different regions
- Toggle morphological flood-fill smoothing (uses SciPy's binary dilation/closing to smooth jagged region boundaries)
- See the result instantly as a live preview

![Studio Preview](https://github.com/juleshenry/superwand/blob/main/examples/studio-preview.png?raw=1)

The Studio also handles CSS retheming. Upload a stylesheet, and SuperWand parses all hex color codes, clusters them with KMeans, and maps the clusters to your chosen theme. The before/after is surprisingly dramatic:

![CSS Before](https://github.com/juleshenry/superwand/blob/main/examples/css/before.png?raw=1)
![CSS After Tropical](https://github.com/juleshenry/superwand/blob/main/examples/css/after_tropical.png?raw=1)

## CLI Usage

```bash
pip install superwand
```

```bash
superwand zebra.png -theme Urban
```

```bash
superwand charizard.png -theme Vaporwave -k 6 -gradient radial
```

The `-k` flag controls the number of color regions. More regions means finer-grained recoloring. For simple posterized art (like the Charizard), 4 regions works well. For photographs with subtle gradients, 6-8 regions capture more detail.

## The Interesting Parts

The NumPy optimization was worth the effort. The naive approach -- iterating over each pixel in a Python loop to check its cluster assignment and replace its color -- is painfully slow for large images. The vectorized approach uses boolean mask indexing: `image[labels == k] = theme_color[k]` replaces an entire region in one operation. The gradient computation is similarly vectorized: generate the gradient array for the bounding box, mask it to the region shape, and multiply. No Python loops touch individual pixels.

The morphological flood filling (optional, via SciPy) addresses a visual artifact of KMeans clustering: jagged region boundaries. KMeans assigns each pixel independently, so the boundary between two regions can be noisy -- a few pixels of region 1 embedded in region 2 because their color was ambiguous. Binary dilation followed by closing smooths these boundaries, producing regions with cleaner edges. It is a post-processing step borrowed from medical image segmentation, applied here to make Charizards look better.

The CSS retheming feature came from a practical itch. I was reskinning a web project and manually hunting for every hex code in the stylesheets. SuperWand automates this: it parses hex patterns from the CSS file, clusters them (because many similar shades should map to the same theme color), replaces each cluster with the nearest theme color, and writes the new stylesheet. It is the kind of thing that saves you two hours of find-and-replace.

Eighteen themes. Five gradient styles. One wand.
