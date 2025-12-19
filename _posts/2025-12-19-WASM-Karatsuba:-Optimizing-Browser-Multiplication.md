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

To understand why Karatsuba’s algorithm was such a revelation, we first have to look at what it replaced. For centuries, the "Grade School" method was the undisputed standard.

### The  Ceiling

In traditional multiplication, if you have two -digit numbers, you multiply every digit of the first number by every digit of the second. This results in  individual digit-multiplications. If you double the size of the numbers, the work quadruples.

In 1960, **Andrey Kolmogorov**—one of the titans of 20th-century mathematics—conjectured that this  bound was the absolute physical limit of multiplication. He organized a seminar to prove it. A 23-year-old student named **Anatoly Karatsuba** attended that seminar and, within a week, returned with a counter-proof that shattered the  assumption.

---

### The Strategy: Divide and Conquer

Karatsuba’s insight starts by splitting two large numbers, x and y, into two halves. Let B be the base (usually 10 or 2) and m be n/2:
x=x1​Bm+x0​
y=y1​Bm+y0​

For example, if x=1234, then x1​=12 and x0​=34 (where B=10 and m=2).

If we multiply these two binomials normally, we get:

xy=(x1​Bm+x0​)(y1​Bm+y0​)
xy=x1​y1​B2m+(x1​y0​+x0​y1​)Bm+x0​y0​


To calculate this, we seemingly need **four** multiplications:

x1​⋅y1​

x1​⋅y0​

x0​⋅y1​

x0​⋅y0​

In a recursive world, four multiplications on half-sized numbers still results in  complexity. We haven't actually gained anything yet.

---

### Karatsuba’s Algebraic "Cheat"

The genius of the algorithm is realizing that we don't actually need to know  and  individually. We only need their **sum**.

Karatsuba found he could get that sum using only **one** additional multiplication instead of two. He defined three variables:

    z2​=x1​⋅y1​

    z0​=x0​⋅y0​

    z1​=(x1​+x0​)⋅(y1​+y0​)−z2​−z0​

If you expand z1​, you'll see the magic:
(x1​+x0​)(y1​+y0​)=x1​y1​+x1​y0​+x0​y1​+x0​y0​

By subtracting z2​ (x1​y1​) and z0​ (x0​y0​), we are left exactly with (x1​y0​+x0​y1​).

We have reduced the problem from four multiplications of size n/2 to three.

We have reduced the problem from **four** multiplications of size  to **three**.

---

### The Efficiency Gain

By reducing the recursive branching factor from 4 to 3, the complexity shifts according to the Master Theorem:

| Method        | Recurrence Relation            | Complexity                          |
|---------------|--------------------------------|-------------------------------------|
| Grade School  | $T(n)=4T(n/2)+O(n)$           | $O(n^{\log_2 4}) = O(n^2)$          |
| Karatsuba     | $T(n)=3T(n/2)+O(n)$           | $O(n^{\log_2 3}) \approx O(n^{1.585})$ |

While  might not seem significantly smaller than , the gap widens exponentially as  grows. For a number with 1,000 digits, Karatsuba requires roughly  operations, whereas the grade school method requires .

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