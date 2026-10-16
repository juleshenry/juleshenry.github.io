---
layout: post
title: "Undergraduate Thesis: Queries in the Mist"
date: 2020-06-01
description: "My 2020 undergraduate thesis at Penn: can fake traffic hide real web activity? A classifier attack on the ISP Pollution tool, with the PDF."
---

*Queries in the Mist: Obfuscation as a Privacy Mechanism* is my undergraduate thesis in computer science at the University of Pennsylvania, completed in April 2020 and advised by Rajeev Alur.

It asks whether you can hide your real web activity from an observer by burying it in fake traffic. The test case is ISP Pollution, an open-source tool that generates random searches and page visits for exactly that purpose.

I trained a logistic-regression classifier to tell ISP Pollution's traffic apart from real search histories, taken from the 2006 AOL query dataset, and tested it in the role of two adversaries at noise ratios from 1:1 up to 20:1.

- **A search engine**, which sees the queries themselves. The noise did not help. Even at twenty fake queries for each real one, the classifier's F-score barely moved.
- **An internet service provider**, which sees only domain names. Here the noise did help: the classifier's F-score fell as the noise ratio rose, in line with earlier theoretical work.

The thesis also surveys the theory of differentially private obfuscation and earlier noise-injection tools such as TrackMeNot.

[Read the thesis (PDF)](/blog/assets/2020/QITM.pdf)

It was graded by the late [Dr. Max Mintz](https://almanac.upenn.edu/articles/max-mintz-computer-information-science).
