---
layout: post
title: "WASM Karatsuba: Optimizing Browser Multiplication"
date: 2025-12-19
---

# Intro
Who would have thought that the calculations of arithmetic are still works in progress? Indeed, as recently as 2019, researchers avid Harvey and Joris van der Hoeven fundamentally improved the theoretical computational bounds of integer multiplication to $(O(n \log n))$. The typical caveat emptor applies: namely, such gains are limited to the lofty world of astronomically large numbers - think, >$2^{1729^12}$. In practice, even the simpler Karatsuba algorithm fails to achieve superiority until numbers greater than ~$10^96$. Nevertheless, these exotic approaches to arithmetic elucidate the power of algorithms to overcome assumptions about the limits on the fundamental primitives of computation. 

## Overview
We will take the reader from gradeschool multiplication to Karatsuba to give credence to the idea of divide-and-conquer algorithms to speed up integer multiplication. 

Next, we will examine an implementation of Karatsuba algorithm in WASM to see how it performs in the browser.

Finally, we will work through the over-arching innovations of the ascendingly more efficient algorithms: Toom–Cook, Schönhage–Strassen, & Harvey-Hoeven. In conclusion, we will examine the parallels between integer multiplication and sorting algorithms to unpack why both are $O(n \log n)$.



# Schoolbook Multiplication: Fundamentally $O(n^2)$

To understand why we are traditionally tethered to O(n2), let us cast our minds back to the elementary school chalkboard. When we multiply two n-digit integers—say, A and B—we are essentially performing a series of repetitive, granular tasks that scale quadratically with the input size.
## The Anatomy of the Partial Product

First, consider the "multiplication phase." We take the first digit of the multiplier (B) and multiply it by every single digit of the multiplicand (A). If both numbers have n digits, this initial step requires n individual single-digit multiplications.

Now, we must repeat this process for the second digit of B, then the third, and so on, until we have exhausted all n digits of the multiplier. Mathematically, we are performing n sets of n multiplications. This gives us n×n, or n2 fundamental operations.
## The Cost of Alignment and Addition

Once we have generated these n rows of partial products, the work is not yet finished. We must then perform the "addition phase." Each row is shifted to the left—a symbolic representation of multiplying by powers of 10—and then summed together.

    Each partial product can have up to n+1 digits.

    We are summing n such rows.

    The total number of additions required to collapse these rows into a final product also scales with n2.

## The Quadratic Ceiling

In the lexicon of Big O notation, we ignore the smaller constants and focus on the dominant growth factor. While you might perform some clever carries or skip a few zeros, the fundamental structure of the algorithm remains a nested loop: for every digit in the bottom number, you must visit every digit in the top number.
$$
\sum_{i=1}^{n}\sum_{j=1}^{n} \big(A_j \times B_i\big) \;\Longrightarrow\; O(n^2)
$$

Thus, the "schoolbook" method represents a rigid, two-dimensional grid of operations. To break the O(n2) barrier, as Harvey and van der Hoeven have done, one must move beyond this grid entirely—treating integers not as mere strings of digits, but as polynomials or points in a complex plane.

# Karatsuba: Innovation in $O(n^{\log_2 3})$

# WASM Karatsuba: Emprically in the Browser

# Hand-waving Toom-Cook: $O(n \log n)$

# Hand-waving Schönhage–Strassen $O(n \log n)$

# Hand-waving Harvey–van der Hoeven: $O(n \log n \log \log n)$

## Discrete Fourier Transform Primer

## Butterflies and Hypercubes : Eliminating $O(\log \log n)$

# Connections to Sorting Algorithms



## Further Reading
Wonderful Wikipedia : https://en.wikipedia.org/wiki/Multiplication_algorithm
Exploration of Varying Radix on Intel i3-4025U : https://miracl.com/blog/missing-a-trick-karatsuba-variations-michael-scott/