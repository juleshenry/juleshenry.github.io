---
layout: post
title: "WASM Karatsuba: Optimizing Browser Multiplication"
date: 2025-12-19
---

# Intro
Who would have thought that the calculations of arithmetic are still works in progress? Indeed, as recently as 2019, researchers avid Harvey and Joris van der Hoeven fundamentally improved the theoretical computational bounds of integer multiplication to $O(n \log n)$. The typical caveat emptor applies: namely, such gains are limited to the lofty world of astronomically large numbers—think, $> 2^{1729^{12}}$. In practice, even the simpler Karatsuba algorithm fails to achieve superiority until numbers greater than $\sim 10^{96}$. Nevertheless, these exotic approaches to arithmetic elucidate the power of algorithms to overcome assumptions about the limits on the fundamental primitives of computation. 

## Overview
We will take the reader from gradeschool multiplication to Karatsuba to give credence to the idea of divide-and-conquer algorithms to speed up integer multiplication. 

Next, we will examine an implementation of Karatsuba algorithm in WASM to see how it performs in the browser.

Finally, we will work through the over-arching innovations of the ascendingly more efficient algorithms: Toom–Cook, Schönhage–Strassen, & Harvey-Hoeven. In conclusion, we will examine the parallels between integer multiplication and sorting algorithms to unpack why both are $O(n \log n)$.



# Schoolbook Multiplication: Fundamentally $O(n^2)$

To understand why we are traditionally tethered to $O(n^2)$, let us cast our minds back to the elementary school chalkboard. When we multiply two $n$-digit integers—say, $A$ and $B$—we are essentially performing a series of repetitive, granular tasks that scale quadratically with the input size.
## The Anatomy of the Partial Product

First, consider the "multiplication phase." We take the first digit of the multiplier ($B$) and multiply it by every single digit of the multiplicand ($A$). If both numbers have $n$ digits, this initial step requires $n$ individual single-digit multiplications.

Now, we must repeat this process for the second digit of $B$, then the third, and so on, until we have exhausted all $n$ digits of the multiplier. Mathematically, we are performing $n$ sets of $n$ multiplications. This gives us $n \times n$, or $n^2$ fundamental operations.
## The Cost of Alignment and Addition

Once we have generated these $n$ rows of partial products, the work is not yet finished. We must then perform the "addition phase." Each row is shifted to the left—a symbolic representation of multiplying by powers of 10—and then summed together.

- Each partial product can have up to $n+1$ digits.
- We are summing $n$ such rows.
- The total number of additions required to collapse these rows into a final product also scales with $n^2$.

## The Quadratic Ceiling

In the lexicon of Big O notation, we ignore the smaller constants and focus on the dominant growth factor. While you might perform some clever carries or skip a few zeros, the fundamental structure of the algorithm remains a nested loop: for every digit in the bottom number, you must visit every digit in the top number.
$$
\sum_{i=1}^{n}\sum_{j=1}^{n} \big(A_j \times B_i\big) \;\Longrightarrow\; O(n^2)
$$

Thus, the "schoolbook" method represents a rigid, two-dimensional grid of operations. To break the $O(n^2)$ barrier, as Harvey and van der Hoeven have done, one must move beyond this grid entirely—treating integers not as mere strings of digits, but as polynomials or points in a complex plane.

# Karatsuba: Innovation in $O(n^{\log_2 3})$

To understand why Karatsuba’s algorithm was such a revelation, we first have to look at what it replaced. For centuries, the "Grade School" method was the undisputed standard.

### The $O(n^2)$ Ceiling

In traditional multiplication, if you have two $n$-digit numbers, you multiply every digit of the first number by every digit of the second. This results in $n^2$ individual digit multiplications. If you double the size of the numbers, the work quadruples.

In 1960, **Andrey Kolmogorov**—one of the titans of 20th-century mathematics—conjectured that this $O(n^2)$ bound was the absolute physical limit of multiplication. He organized a seminar to prove it. A 23-year-old student named **Anatoly Karatsuba** attended that seminar and, within a week, returned with a counter-proof that shattered the $O(n^2)$ assumption.

---

### The Strategy: Divide and Conquer

Karatsuba's insight starts by splitting two large numbers, $x$ and $y$, into two halves. Let $B$ be the base (usually 10 or 2) and $m = n/2$:
$$
\begin{aligned}
x &= x_1 B^m + x_0 \\
y &= y_1 B^m + y_0
\end{aligned}
$$

For example, if $x = 1234$, then $x_1 = 12$ and $x_0 = 34$ (where $B = 10$ and $m = 2$).

If we multiply these two binomials normally, we get:
$$
\begin{aligned}
xy &= (x_1 B^m + x_0)(y_1 B^m + y_0) \\
   &= x_1 y_1 B^{2m} + (x_1 y_0 + x_0 y_1) B^m + x_0 y_0
\end{aligned}
$$

To calculate this, we seemingly need **four** multiplications:
- $x_1 \cdot y_1$
- $x_1 \cdot y_0$
- $x_0 \cdot y_1$
- $x_0 \cdot y_0$

In a recursive world, four multiplications on half-sized numbers still results in $O(n^2)$ complexity. We haven't actually gained anything yet.

---

### Karatsuba’s Algebraic "Cheat"

The genius of the algorithm is realizing that we don't actually need to know $x_1 y_0$ and $x_0 y_1$ individually. We only need their **sum**.

Karatsuba found he could get that sum using only **one** additional multiplication instead of two. He defined three variables:
$$
\begin{aligned}
z_2 &= x_1 \cdot y_1 \\
z_0 &= x_0 \cdot y_0 \\
z_1 &= (x_1 + x_0)(y_1 + y_0) - z_2 - z_0
\end{aligned}
$$

If you expand $z_1$, you'll see the magic:
$$
(x_1 + x_0)(y_1 + y_0) = x_1 y_1 + x_1 y_0 + x_0 y_1 + x_0 y_0
$$

By subtracting $z_2$ ($x_1 y_1$) and $z_0$ ($x_0 y_0$), we are left exactly with $(x_1 y_0 + x_0 y_1)$.

We have reduced the problem from **four** multiplications of size $n/2$ to **three**.

---

### The Efficiency Gain

By reducing the recursive branching factor from 4 to 3, the complexity shifts according to the Master Theorem:

| Method        | Recurrence Relation            | Complexity                          |
|---------------|--------------------------------|-------------------------------------|
| Grade School  | $T(n)=4T(n/2)+O(n)$           | $O(n^{\log_2 4}) = O(n^2)$          |
| Karatsuba     | $T(n)=3T(n/2)+O(n)$           | $O(n^{\log_2 3}) \approx O(n^{1.585})$ |

While $n^{1.585}$ might not seem significantly smaller than $n^2$, the gap widens exponentially as $n$ grows. For a number with 1,000 digits, Karatsuba requires roughly $n^{\log_2 3}$ operations, whereas the grade school method requires $n^2$.

# WASM Karatsuba: Empirically in the Browser

# Hand-waving Toom-Cook: $O(n \log n)$
## The Polynomial Perspective

To understand Toom-Cook, we have to stop thinking of numbers as strings of digits and start thinking of them as polynomials.

If we split a number $x$ into $k$ parts, we can represent it as a polynomial $P(x)$ of degree $k-1$. For Toom-3, a number is split into:
$$
\begin{aligned}
x &= a_2 B^{2m} + a_1 B^m + a_0 \\
P_x(z) &= a_2 z^2 + a_1 z + a_0
\end{aligned}
$$

Multiplying two such numbers is equivalent to multiplying two polynomials. The resulting product polynomial will have a degree of $2k-2$. To uniquely determine a polynomial of degree $d$, you only need $d+1$ points.

## The Five-Step Process

Toom-Cook replaces the "brute force" multiplication of coefficients with a more elegant algebraic detour:

1. **Splitting**: Break the large integers into $k$ smaller blocks.
2. **Evaluation**: Choose $2k-1$ simple points (like $0, 1, -1, 2, \infty$) and evaluate the polynomials at these points.
3. **Pointwise Multiplication**: Multiply the evaluated values (this is where the actual "multiplication" happens, but on much smaller numbers).
4. **Interpolation**: Use the results to "solve" for the coefficients of the product polynomial (essentially solving a system of linear equations).
5. **Recomposition**: Shift and add the coefficients to get the final integer result.

## Why it's faster (and when it's not)

In Toom-3, instead of the 9 multiplications required by the grade-school method (for a $3 \times 3$ split), we only need 5 multiplications.
| Algorithm             | Split ($k$) | Multiplications | Complexity                       |
|-----------------------|-------------|-----------------|----------------------------------|
| Grade School          | $n$         | $n^2$           | $O(n^2)$                         |
| Karatsuba (Toom-2)    | $2$         | $3$             | $O(n^{1.585})$                   |
| Toom-3                | $3$         | $5$             | $O(n^{1.465})$                   |
| Toom-$k$              | $k$         | $2k-1$          | $O\!\big(n^{\log_k(2k-1)}\big)$  |

# Hand-waving Schönhage–Strassen $O(n \log n \log \log n)$
## Schönhage–Strassen: The FFT Singularity

If Karatsuba was a clever algebraic trick and Toom-Cook was a dive into polynomial interpolation, the Schönhage–Strassen algorithm represents a fundamental departure from arithmetic altogether. It is the moment where number theory meets signal processing.

In 1971, Arnold Schönhage and Volker Strassen arrived at a complexity of $O(n \log n \log \log n)$, a bound so tight it remained the world champion for nearly half a century until the 2019 breakthrough mentioned in the introduction.

## The Signal Processing Pivot

To grasp Schönhage–Strassen, one must stop viewing an integer as a value and start viewing it as a signal.

When we multiply two numbers in grade school, we are essentially performing a convolution of their digits. If you multiply $(10a+b) \times (10c+d)$, you are blending the sequences of digits together. In the world of computer science, convolution in the "time domain" (or digit domain) is computationally expensive ($O(n^2)$).

However, a core tenet of the Convolution Theorem is that convolution in the time domain is equivalent to simple pointwise multiplication in the frequency domain.

## The Roots of Unity: A Mathematical Shortcut

The "hand-waving" magic happens via the Fast Fourier Transform (FFT).

Recall that Toom-Cook evaluated polynomials at arbitrary points like $0, 1$, and $-1$. Schönhage and Strassen realized that if you evaluate polynomials at complex roots of unity (points on the unit circle in the complex plane), the symmetry of these points allows for a massive recursive shortcut.

1. **Transform**: Treat the digits of your numbers as a signal and run an FFT to move them into the frequency domain.
2. **Multiply**: Multiply the transformed results pointwise (this is now incredibly fast).
3. **Inverse Transform**: Perform an Inverse FFT to bring the product back into the digit domain.
4. **Carry**: Perform a final pass to handle the carries, as the FFT results will be "blurred" across the digits.

## The Logarithmic Horizon

The brilliance of this approach is that the FFT takes only $O(n \log n)$ time. However, Schönhage–Strassen has a slight "tax" of $\log \log n$ because it has to handle the precision of the complex numbers or work within specific finite rings to avoid rounding errors.
| Algorithm                  | Complexity                   | Historical Context               |
|----------------------------|-----------------------------|----------------------------------|
| Karatsuba                  | $O(n^{1.58})$               | The 1960 breakthrough.           |
| Schönhage–Strassen         | $O(n \log n \log \log n)$   | The 1971 "unbeatable" standard.  |
| Harvey & van der Hoeven    | $O(n \log n)$               | The 2019 "theoretical perfection." |

# Hand-waving Harvey–van der Hoeven:  $O(n \log n)$
## Harvey–van der Hoeven: Reaching the Mathematical Horizon

If Schönhage–Strassen was the "unbeatable" champion for 48 years, the 2019 paper by David Harvey and Joris van der Hoeven is the closing of the book. For decades, the mathematical community conjectured that $O(n \log n)$ was the absolute theoretical floor—the "speed of light" for multiplication. Harvey and van der Hoeven finally proved it possible, effectively finishing a quest that began with Kolmogorov and Karatsuba in the 1960s.

But how do you shave off that last, pesky $\log \log n$ factor that haunted Schönhage–Strassen?

## The Problem: The Recursive "Tax"

In Schönhage–Strassen, the algorithm uses FFTs to multiply numbers, but those FFTs themselves require multiplications. To handle those, the algorithm calls itself recursively. Each level of this recursion adds a "tax" of $\log \log n$ to the complexity.

To reach the $O(n \log n)$ holy grail, the researchers had to find a way to perform the multiplication while keeping the "administrative overhead" from growing with the size of the number.
### The Solution: Multi-dimensional FFTs

The "hand-wavy" explanation is that Harvey and van der Hoeven moved from the 1-dimensional world of standard FFTs into multi-dimensional space.

Imagine your number not as a long string of digits (a line), but as a high-dimensional hypercube (a grid). By rearranging the data into many dimensions—specifically, they suggested using a very large number of dimensions—they could use a technique called "vectorized FFTs."

By spreading the computation across these dimensions, they could reduce the number of recursive steps required. Instead of the overhead stacking up as the numbers got larger, they managed to consolidate it.
### The "1729" Caveat: A Galactic Algorithm

While the proof is a masterpiece of modern mathematics, it belongs to the class of "Galactic Algorithms." These are algorithms that are theoretically superior but would only outperform existing methods on datasets so large they cannot exist in the observable universe.

As noted in the introduction, the "crossover point" where this algorithm becomes faster than Schönhage–Strassen is estimated at $2^{1729^{12}}$.

- For scale, there are roughly $10^{80}$ atoms in the observable universe.
- This number is so large it cannot even be written down in standard decimal notation without filling the entire universe with digits.

## Setup and Decomposition:
Split inputs into $\Theta(n / \log n)$ chunks.
Use the Chinese Remainder Theorem (CRT) to map the polynomial multiplication into a $d$-dimensional array convolution over complex numbers or a suitable ring.
Choose dimensions $s_1 \times s_2 \times \cdots \times s_d$ where each $s_i$ is a prime around $(n / \log n)^{1/d}$. This makes the total size $S \approx n / \log n$.

### Gaussian Resampling (The Magic Trick):
Direct multidimensional DFT on prime sizes would be slow or add log factors.
Instead, "resample" the input array using a Gaussian function (like a bell curve) to approximate the DFT.
This transforms the problem into a larger DFT of sizes $t_1 \times \cdots \times t_d$, where each $t_i$ is a power of 2 close to $s_i$.
Why Gaussian? It helps control errors when mapping frequencies between the irregular (prime) grid and the uniform (power-of-2) grid on a "torus" (think wrapped-around space).
Cost: This step uses linear maps with bounded norms, adding only $O(n \log n)$ work, and errors are tiny (handled by extra precision bits).

### Fast Evaluation with Synthetic FFTs:
Now compute the larger multidimensional DFT using Nussbaumer's polynomial transforms over rings like $\mathbb{C}[y] / (y^r + 1)$ (where $r$ is power of 2).
These "synthetic" FFTs mostly use additions/subtractions (cheap, $O(n)$) instead of multiplications.
Pointwise multiplications in the transformed space are done recursively (Kronecker substitution: flatten back to 1D integer mult).
Inverse DFT similarly to get back the convolution.

Recursion and Base Case:
Recurse on smaller subproblems (size roughly $n^{1/d + o(1)}$).
With large $d$, recursion depth is small, and total cost satisfies $M(n) \leq K \cdot n \cdot n' \cdot M(n') + O(n \log n)$, where $n' \ll n$, leading to $M(n) = O(n \log n)$.
For small $n$, fall back to $O(n^2)$.

## Discrete Fourier Transform (DFT) Primer

The Discrete Fourier Transform is a mathematical "prism." Just as a prism splits white light into its constituent colors (frequencies), the DFT takes a sequence of data and reveals the underlying periodic patterns.

In the context of multiplication, we treat our number $x$ as a vector of its digits: $\mathbf{a} = [a_0, a_1, \dots, a_{n-1}]$. We can think of these digits as the coefficients of a polynomial:
$$
A(x) = a_0 + a_1 x + a_2 x^2 + \dots + a_{n-1} x^{n-1}
$$

The DFT evaluates this polynomial at $n$ specific points: the complex roots of unity. These are points spaced evenly around the unit circle in the complex plane, defined as:
$$
\omega_n^k = e^{\frac{2\pi i k}{n}}
$$

By evaluating the polynomial at these symmetric points, the Fast Fourier Transform (FFT) can use a divide-and-conquer approach to compute all evaluations in $O(n \log n)$ time instead of the naive $O(n^2)$.
## Convolution Theorem

This is the "Secret Sauce" of modern high-speed multiplication.

When you multiply two polynomials, $A(x)$ and $B(x)$, the coefficients of the resulting polynomial $C(x)$ are the convolution of the coefficients of $A$ and $B$.

If $A = [1, 2, 3]$ and $B = [4, 5, 6]$, the standard way to find the product involves a "sliding" multiplication of every element against every other element. This is essentially what happens in grade-school multiplication when you shift rows and add them up.

The Convolution Theorem states:

**The Fourier Transform of a convolution is the pointwise product of the Fourier Transforms.**

Mathematically, if $F$ denotes the Fourier Transform and $\ast$ denotes convolution:
$$
F(A \ast B) = F(A) \cdot F(B)
$$

## The 3-Step Shortcut

Because of this theorem, we can bypass the $O(n^2)$ "sliding" convolution entirely:

1. **Forward Transform**: Compute $A' = \operatorname{FFT}(A)$ and $B' = \operatorname{FFT}(B)$ (time: $O(n \log n)$).
2. **Pointwise Product**: Multiply the corresponding elements: $C_i' = A_i' \cdot B_i'$ (time: $O(n)$).
3. **Inverse Transform**: Compute $C = \operatorname{IFFT}(C')$ (time: $O(n \log n)$).

The result $C$ is the vector of coefficients for our product. After a quick final pass to handle the carries (since coefficients in $C$ might be larger than our base), we have our answer. We have successfully traded the "quadratic wall" of grade-school multiplication for the "logarithmic slope" of the FFT.

## Butterflies and Hypercubes: Eliminating $O(\log \log n)$

In the standard Schönhage–Strassen approach, the $\log \log n$ factor is the "shadow" cast by recursion. To multiply two $n$-bit integers, the algorithm breaks them into $2^k$ chunks. But these chunks are themselves large, requiring their own FFTs, which require their own multiplications, and so on. This recursive nesting creates a depth of complexity that prevents a clean $O(n \log n)$ result.

To eliminate this, Harvey and van der Hoeven turned to the geometry of the Hypercube and the efficiency of the FFT Butterfly.

## The Butterfly: Exploiting Symmetry

At the heart of any FFT is the "Butterfly" operation. When we evaluate a polynomial at roots of unity, we notice that many of the calculations are redundant. For example, $\omega^k$ and $\omega^{k+n/2}$ are just negatives of each other on the unit circle.

The Butterfly unit takes two inputs, performs a single multiplication and an addition/subtraction, and produces two outputs. By nesting these butterflies, we create a network that processes data in stages. In a standard 1D FFT, we have $\log n$ stages, each doing $O(n)$ work.
## The Hypercube: Multi-dimensional Locality

The breakthrough in the $O(n \log n)$ proof involves treating the data not as a linear array, but as a multi-dimensional hypercube.

By mapping the digits of a massive integer onto a high-dimensional grid (say, a $d$-dimensional cube), the researchers could perform FFTs along each dimension independently. This is essentially a "divide-and-conquer" approach on the structure of the data itself.

- **Reduction of Recursive Depth**: In a 1D FFT, the recursion depth is tied directly to $n$. In a multi-dimensional FFT, you can process smaller blocks more efficiently, preventing the precision requirements (and thus the extra $\log \log n$ multiplications) from stacking up.
- **The "Unit Cost" Assumption**: By using a specific type of Number Theoretic Transform (NTT) across these dimensions, they ensured that the "work" done at each node of the hypercube remained constant relative to the total input.

## Closing the Loop

The transition from Schönhage–Strassen to Harvey–van der Hoeven is effectively the transition from a linear pipeline to a massively parallel hypercube network.

While the "Butterflies" do the heavy lifting of the transform, the "Hypercube" architecture ensures that the data is organized so that the recursive overhead—that pesky $\log \log n$—finally collapses into the main $O(n \log n)$ term.

We have reached the theoretical limit. There is no $O(n)$ multiplication; the act of "reading" the $n$ digits and "sorting" them through the $\log n$ stages of a butterfly network is the fundamental physical constraint of our universe.
# Connections to Sorting Algorithms
To establish a formal mathematical symmetry between the Harvey–van der Hoeven (HvH) multiplication algorithm and comparison-based sorting, we must look at them through the lens of Information Theory and the Divide-and-Conquer recurrence.

The symmetry lies in the fact that both reach the "Information-Theoretic Wall" for their respective domains.
## The Information-Theoretic Lower Bound

In both fields, the nlogn term arises from the entropy of the state space.

In Sorting: To sort n elements, we must distinguish between n! possible permutations. Using Stirling's approximation:
log2​(n!)≈nlog2​n−nlog2​e

Each comparison provides at most 1 bit of information. Therefore, the lower bound is Ω(nlogn) bits of information.

In HvH Multiplication: To multiply two n-bit integers, we are essentially performing a convolution. The Schönhage-Strassen conjecture (finally proven by Harvey and van der Hoeven) posits that the complexity is O(nlogn). This mirrors the sorting bound because it represents the optimal distribution of "mixing" information across n bit-positions via the Fast Fourier Transform (FFT).

## The Symmetry of the Recurrence

The "Deep Form Factor" (DFF) or structural symmetry is found in the Master Theorem profile of both algorithms.
Comparison-Based Sorting (Merge Sort)

Merge Sort splits the domain into two sub-problems and requires O(n) work to merge (the "linear pass").
T(n)=2T(2n​)+O(n)
HvH Multiplication

The HvH algorithm uses a multi-dimensional FFT. By reducing a 1D convolution to a d-dimensional hypercube of size Ld, they manage the "overhead" of the recursion more efficiently than Schönhage-Strassen. However, the core structural symmetry remains:
T(n)=K⋅T(Kn​)+O(n)

Where O(n) represents the cost of the Fourier Transform/Pointwise multiplication at that level.


The mathematical symmetry is defined as follows: Both algorithms are optimal because they saturate the bandwidth of a d-dimensional hypercube. In sorting, this is the bandwidth of the decision tree; in HvH, it is the bandwidth of the FFT signal path. Harvey and van der Hoeven’s breakthrough was essentially finding a way to prevent the "log-star" (O(nlogn⋅2log∗n)) overhead from accumulating, effectively "sorting" the bit-information with the same efficiency that a heap or merge sort organizes a list.

To "saturate the bandwidth" of a d-dimensional hypercube essentially means that an algorithm is moving as much information as the geometry of the network physically allows.

At an undergraduate level, think of it this way: if you have a highway system, the "bandwidth" is the number of lanes. "Saturating" it means every lane is full of cars moving at top speed. In computer science, this "highway" is the data-dependency graph of your algorithm.
0. Why a Hypercube?

A d-dimensional hypercube (or Qd​) is a graph with 2d nodes. Each node is labeled with a d-bit binary string, and two nodes are connected if their labels differ by exactly one bit.
Why it works for both:

Recursive Structure: A d-cube is just two (d−1)-cubes joined together. This perfectly matches Divide and Conquer.

Logarithmic Diameter: Even with 2d nodes, you can get from any point to another in just d steps. Since d=log2​(nodes), this is the geometric origin of the logn factor in both algorithms.

Symmetry: Every node looks exactly like every other node. This ensures that no single part of the "multiplication" or "sorting" becomes a bottleneck.

1. Sorting to Hypercube: The "Compare-Exchange" Path

When you sort n items, you are trying to find one specific permutation out of n! possibilities.

The Hypercube Mapping: Imagine each node in a hypercube represents a state of your list.

The Exploration: In algorithms like Bitonic Sort, we treat the indices of our array as coordinates in a hypercube. To sort, we perform "Compare-Exchange" operations along each dimension of the cube sequentially.

Saturating the Bandwidth: In a single step, a hypercube can support n/2 parallel comparisons (one across every edge in a specific dimension). A "perfect" sorting algorithm uses every one of these available "lanes" in every step to resolve the uncertainty (entropy) of the list's order.

The Wall: Because you need log(n!)≈nlogn bits of information to sort, and the hypercube provides O(n) "lanes" per step, you physically must take logn steps.

## Multiplying to Hypercube: The "Convolution" Path

Multiplying two n-bit integers is essentially a convolution of their digits. The Harvey–van der Hoeven (HvH) breakthrough treats this convolution as a multi-dimensional problem.

The Hypercube Mapping: HvH breaks the large n-bit integers into many smaller chunks and arranges them as a d-dimensional grid (which is a subset of a hypercube).

The Exploration: The Fast Fourier Transform (FFT) is the engine here. The FFT's "butterfly" diagram is mathematically isomorphic to the edges of a hypercube. When the FFT runs, it is literally passing data back and forth along the dimensions of this hypercube to calculate how every digit affects every other digit (the carry-propagation).

Saturating the Bandwidth: Previous algorithms (like Schönhage–Strassen) had "congestion." They couldn't perfectly fill the hypercube lanes because of the overhead in managing the recursion (the O(loglogn) term).

The HvH Fix: Harvey and van der Hoeven used a "Gaussian" distribution of dimensions. They ensured that as the recursion goes deeper, the "recombination" work perfectly fills the available bandwidth of the hypercube at that level, without any wasted "empty lanes" or "traffic jams."

## Further Reading
Wonderful Wikipedia : https://en.wikipedia.org/wiki/Multiplication_algorithm

Exploration of Varying Radix on Intel i3-4025U : https://miracl.com/blog/missing-a-trick-karatsuba-variations-michael-scott/

Karatsuba paper: https://ieeexplore.ieee.org/document/4402691
Toom-Cook paper: 
Schönhage–Strassen paper: 
Harvey and van der Hoeven's Paper : https://hal.archives-ouvertes.fr/hal-03182372/document