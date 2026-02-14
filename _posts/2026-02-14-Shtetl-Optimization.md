---
layout: post
title: "Shtetl Optimization"
date: 2026-02-14
---

No secret that I am big fan of Scott Aaronson's blog, [Shtetl Optimized](https://scottaaronson.blog/). I have been reading it for years, a national treasure. Herein, I analyze the linguistic complexity of his blog compared to my own and two others, the also great [Simon Willison blog](https://simonwillison.net/) along with the ineffable [Alex Harri blog](https://alexharri.com/).


| Source | Flesch-Kincaid Grade | ARI Grade | Gunning Fog Grade | Lexical Diversity | Word Count |
|--------|----------------------|-----------|-------------------|-------------------|------------|
| alexharri_posts.csv | 9.77 | 9.55 | 12.40 | 0.228 | 3,866.5 |
| juleshenry_posts.csv | 15.51 | 16.31 | 17.78 | 0.458 | 2,000.4 |
| scottaaronson_blog_posts.csv | 13.01 | 13.31 | 15.61 | 0.543 | 966.8 |
| simonwillison_all_blogs.csv | 12.13 | 12.55 | 14.52 | 0.554 | 627.8 |


## Writing Stats Over Time

![Writing Stats](/blog/assets/2026/writing_stats_time.png)


The curiosity? Technical posts are considered more sophisticated when code is used because it has no "periods", qualifying as long Faulknerian sentences. Note the outliers in my own blog achieve Flesch-Kincaid of 80+. Therefore, I also include an "outliers removed summary to truly compare. Alex Harri, and Icelander, unsurprisingly writes at a lower grade level, even though his posts are incredibly engaging and informative. Simon Willison's posts are more accessible, while Scott Aaronson's posts are more complex, likely due to the technical nature of his content. Jules Henry's posts are the most complex, which may be due to the size of his ego.

## Interquartile Reduction of Outliers

| Source | Flesch-Kincaid Grade | ARI Grade | Gunning Fog Grade | Lexical Diversity | Word Count |
|--------|----------------------|-----------|-------------------|-------------------|------------|
| alexharri_posts.csv | 9.86 | 9.64 | 12.49 | 0.234 | 3,443.41 |
| juleshenry_posts.csv | 11.50 | 11.33 | 13.58 | 0.500 | 1,110.80 |
| scottaaronson_blog_posts.csv | 12.77 | 13.01 | 15.35 | 0.559 | 702.75 |
| simonwillison_all_blogs.csv | 11.80 | 12.12 | 14.21 | 0.568 | 482.81 |


A ha! So I do not write at a higher level than Scott *or* Simon, although I tend to be more verbose.


## Writing Stats Over Time Without Outliers

![Writing Stats](/blog/assets/2026/writing_stats_time_no.png)


That I am doing this on Valentine's Day should be a testament to how much of a great-big nerd I am. Love you, Scott! Solve NP vs. P when you have the chance, will ya?

Code analysis repostiory found [here](https://github.com/juleshenry/-shtetltleths-). 