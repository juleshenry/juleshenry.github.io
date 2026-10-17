---
layout: post
title: "On Multiplication, Vol. III: Schönhage-Strassen and Harvey-van der Hoeven"
date: 2025-12-19 12:02:00
description: "Schönhage-Strassen multiplication modulo 2ᵐ + 1, where its log log n factor comes from, and how Harvey and van der Hoeven reached O(n log n) in 2019."
mathjax: true
---

*On Multiplication:* [I](/blog/2025/12/19/On-Multiplication) · [II](/blog/2025/12/19/On-Multiplication-Vol-II) · **III** · [IV](/blog/2025/12/19/On-Multiplication-Vol-IV) · [V](/blog/2026/10/08/On-Multiplication-Vol-V)

# Schönhage-Strassen: Multiplication in $O(n \log n \log \log n)$

## The Precision Problem

The FFT-based multiplication pipeline described in [Vol. II](/blog/2025/12/19/On-Multiplication-Vol-II) works over the **complex numbers**. The twiddle factors $\omega_N^k = e^{2\pi i k/N}$ are irrational (for most $k$), and so are the intermediate values in the FFT. On a real computer, we approximate these with floating-point arithmetic.

For multiplying two numbers with $n$ digits, the convolution coefficients can be as large as $O(n B^2)$ (where $B$ is the base). To distinguish these integers exactly after rounding, we need floating-point precision of roughly $O(\log n + 2\log B)$ bits. For large $n$, this means we need **multi-precision floating-point arithmetic** inside the FFT itself, and each multi-precision operation costs more than $O(1)$.

This creates a vicious circle: to multiply $n$-digit numbers, we use the FFT, but the FFT internally needs high-precision multiplications, which are themselves expensive. The complex-number FFT approach does not, by itself, yield a clean $O(n \log n)$ integer multiplication algorithm.

Schönhage and Strassen's 1971 breakthrough (the second of two algorithms in their paper; the first used the complex FFT) was to eliminate this precision problem entirely by moving from the complex numbers to an **exact algebraic setting** where roots of unity exist but rounding errors do not.

## From $\mathbb{C}$ to $\mathbb{Z}/(2^m + 1)\mathbb{Z}$: The Number Theoretic Transform

### Roots of unity in finite rings

The FFT algorithm does not actually require the complex numbers. It requires only a ring $R$ that contains:

1. An element $\omega$ of multiplicative order $N$ (an "$N$-th root of unity"), meaning $\omega^N = 1$ and $\omega^k \neq 1$ for $0 < k < N$. In a ring with zero divisors this is not quite enough: the inverse transform also needs $\sum_{j=0}^{N-1} \omega^{jk} = 0$ for $0 < k < N$, which holds automatically when $N$ is a power of two and $\omega^{N/2} = -1$.
2. An inverse of $N$ in $R$ (for the inverse transform).

If $R$ is a finite ring (like $\mathbb{Z}/p\mathbb{Z}$ for a prime $p$), then all arithmetic is exact: no rounding, no precision issues. An FFT performed in such a ring is called a **Number Theoretic Transform (NTT)**.

**Example.** In $\mathbb{Z}/5\mathbb{Z}$, the element $2$ has order $4$: $2^1 = 2$, $2^2 = 4$, $2^3 = 3$, $2^4 = 1 \pmod{5}$. So $\omega = 2$ is a primitive $4$th root of unity in $\mathbb{Z}/5\mathbb{Z}$, and we can perform a 4-point NTT modulo 5 with exact arithmetic.

### Schönhage and Strassen's choice: Fermat-like rings

To multiply two $n$-bit integers, Schönhage and Strassen work in the ring:

$$
R = \mathbb{Z} / (2^m + 1)\mathbb{Z}
$$

for a carefully chosen $m$. In this ring the element $\omega = 2$ (or more precisely, a small power of $2$) serves as a root of unity, and **multiplication by powers of 2 is just a bit-shift followed by a reduction modulo $2^m + 1$**, an operation that costs $O(m)$, which is essentially free.

Why does $2$ behave as a root of unity here? Note that $2^m \equiv -1 \pmod{2^m + 1}$, so $2^{2m} \equiv 1 \pmod{2^m + 1}$. Thus $2$ is a $2m$-th root of unity in this ring. For any power of two $N$ dividing $2m$, the element $\omega = 2^{2m/N}$ is then a primitive $N$-th root of unity with $\omega^{N/2} = 2^m = -1$, which is exactly the condition above. Choosing $m$ appropriately gives us the $N$ we need.

The payoff: all the "twiddle factor multiplications" in the FFT butterfly, which in the complex-number FFT require expensive multi-precision multiplications, reduce to **bit-shifts and additions** in $\mathbb{Z}/(2^m + 1)\mathbb{Z}$. This makes the per-butterfly cost $O(m)$ instead of $O(m \log m \cdots)$, which simplifies the recursion.

## The Algorithm in Detail

### Step 0: Setup

Given two $n$-bit integers $x$ and $y$, choose parameters:
- Let $K = 2^k$ for some $k$ (the number of chunks).
- Let $\ell = \lceil n / K \rceil$ (the chunk size in bits).
- Let $m \approx 2\ell + k$ (the size of a ring element in bits).
- Work in the ring $R = \mathbb{Z}/(2^m + 1)\mathbb{Z}$.

Why is $m$ about *twice* $\ell$? Because the ring has to hold the answer, not just the input. A convolution coefficient is a sum of up to $K$ products of two $\ell$-bit chunks, so it can be as large as $K \cdot 2^{2\ell} = 2^{2\ell + k}$. The modulus must exceed that, or the coefficients wrap around and are lost. This factor of two looks like bookkeeping. It turns out to be the entire source of the $\log \log n$, as we will see below.

The parameters are chosen so that $K \approx \sqrt{n}$, meaning we split each input into about $\sqrt{n}$ chunks of about $\sqrt{n}$ bits each, held in a ring whose elements are about $2\sqrt{n}$ bits wide.

### Step 1: Decomposition

Break each $n$-bit integer into $K$ chunks of $\ell$ bits:

$$
x = \sum_{j=0}^{K-1} a_j \cdot 2^{j\ell}, \qquad y = \sum_{j=0}^{K-1} b_j \cdot 2^{j\ell}
$$

Form the polynomials $A(z) = \sum a_j z^j$ and $B(z) = \sum b_j z^j$ over $R$, so that $x = A(2^\ell)$ and $y = B(2^\ell)$.

### Step 2: Forward NTT

Compute $\hat{\mathbf{a}} = \text{NTT}_N(\mathbf{a})$ and $\hat{\mathbf{b}} = \text{NTT}_N(\mathbf{b})$ in the ring $R$, where $N \geq 2K$ is a suitable power of 2.

The NTT is the same Cooley-Tukey FFT algorithm, but:
- All arithmetic is modular (mod $2^m + 1$).
- Twiddle factor multiplications $\omega^k \cdot v$ are implemented as **bit-shifts** of $v$, with the bits pushed past position $m$ subtracted back in at the bottom (since $2^m \equiv -1$), costing $O(m)$.
- Each butterfly costs $O(m)$: one bit-shift plus two modular additions.
- Total: $N/2 \cdot \log_2 N$ butterflies, each $O(m)$, giving $O(Nm \log N)$ bit operations.

### Step 3: Pointwise multiplication

Compute $\hat{c}_k = \hat{a}_k \cdot \hat{b}_k$ in $R$ for each $k = 0, \ldots, N - 1$.

Each of these is a multiplication of two $m$-bit numbers modulo $2^m + 1$. But this is itself a multiplication of smaller numbers. This is where the algorithm becomes **recursive**: we use the Schönhage-Strassen algorithm itself (on inputs of size $m$ instead of $n$) to perform these multiplications.

There are $N$ such multiplications, each on operands of size $m$. This is the "recursive nesting" that generates the $\log \log n$ factor.

### Step 4: Inverse NTT

Compute $\mathbf{c} = \text{INTT}_N(\hat{\mathbf{c}})$. Same cost as the forward NTT: $O(Nm \log N)$.

### Step 5: Carry propagation and reassembly

The vector $\mathbf{c}$ now contains the convolution of $\mathbf{a}$ and $\mathbf{b}$ modulo $2^m + 1$. (The parameters are chosen so that no coefficient is large enough to "wrap around" the modulus: the modulus is larger than any possible convolution coefficient.) Reassemble the final product by performing carries across the chunks.

## Why $\log \log n$?

The complexity breaks down as follows. At the top level we have:
- NTT and INTT: $O(Nm \log N)$ bit operations for the transforms, which is $O(n \log n)$.
- Pointwise multiplications: recursive multiplications on $m$-bit inputs.

How many recursive multiplications? One more detail matters here. A plain convolution of two length-$K$ sequences has $2K - 1$ coefficients, which is why the pipeline above pads the transform to length $N \geq 2K$. Schönhage and Strassen avoid the padding: they compute the product modulo $2^n + 1$, which turns the convolution into a *negatively wrapped* one of length exactly $K$ (terms that wrap around come back with a minus sign, because $2^n \equiv -1$). So only $K$ pointwise products are needed, each on ring elements of $m \approx 2n/K$ bits.

With $K \approx \sqrt{n}$, the recurrence is:

$$
T(n) = \sqrt{n} \cdot T\!\left(2\sqrt{n}\right) + O(n \log n)
$$

The $2$ inside the recursive call is the factor from Step 0: a product needs twice the bits of its factors. It is easy to drop, and dropping it changes the answer. To see why, count the cost *per bit*. Write $t(n) = T(n)/n$. The $\sqrt{n}$ sub-problems of size $2\sqrt{n}$ hold $2n$ bits between them, so

$$
t(n) = 2\,t\!\left(2\sqrt{n}\right) + O(\log n)
$$

Now trace the recursion. At depth $d$ the problem size is about $n^{1/2^d}$, so its logarithm is about $(\log n)/2^d$: the logarithm *halves* at every level. But the number of bits in play *doubles* at every level, because of that factor of two. The two effects cancel exactly:

$$
\underbrace{2^d \cdot n}_{\text{bits in play at depth } d} \;\times\; \underbrace{\frac{\log n}{2^d}}_{\text{log of the sub-problem size}} \;=\; n \log n
$$

Every level costs the same $O(n \log n)$. The recursion bottoms out when $n^{1/2^d} = O(1)$, which requires $2^d \approx \log n$, giving a recursion depth of $d = O(\log \log n)$. Summing equal contributions over $O(\log \log n)$ levels:

$$
T(n) = O(n \log n \cdot \log \log n)
$$

This is the Schönhage-Strassen bound, and it sits on a knife-edge. Without the doubling, the recurrence would be $T(n) = \sqrt{n} \cdot T(\sqrt{n}) + O(n \log n)$, the levels would shrink geometrically, $n \log n \,(1 + \tfrac12 + \tfrac14 + \cdots)$, and the total would be a clean $O(n \log n)$. With *more* than doubling (say $2K$ pointwise products instead of $K$, which quadruples the bits in play), the levels would grow geometrically and the total would be $O(n \log^2 n)$. The $\log \log n$ lives exactly at the balance point between the two. Harvey and van der Hoeven make the same observation about this recurrence in their own paper: the constant 2 "plays a crucial role in the complexity analysis," because it keeps the cost of the transforms the same at every level.

So the $\log \log n$ factor is not a deficiency of the FFT itself, which is $O(n \log n)$. It is the cost of the **recursive multiplications** needed at each level of the NTT, on numbers that are twice as wide as the chunks they came from.

## A Comparison

| Algorithm             | Complexity                     | Key Innovation                        |
|-----------------------|--------------------------------|---------------------------------------|
| Schoolbook            | $O(n^2)$                       | Direct digit-by-digit                 |
| Karatsuba             | $O(n^{1.585})$                 | 4 multiplications $\to$ 3            |
| Toom-3                | $O(n^{1.465})$                 | 9 multiplications $\to$ 5            |
| Schönhage-Strassen    | $O(n \log n \log \log n)$      | NTT in $\mathbb{Z}/(2^m+1)$         |
| Harvey-van der Hoeven | $O(n \log n)$                  | Multi-dimensional FFT (see below)    |

The jump from Toom-Cook to Schönhage-Strassen is qualitatively different from all previous improvements. Karatsuba and Toom-Cook are algebraic tricks that reduce the exponent toward 1 but never reach it. Schönhage-Strassen breaks through to a *nearly linear* bound by replacing interpolation at a fixed handful of points with evaluation at a number of roots of unity that grows with $n$. It does so in an exact algebraic ring where the symmetry of the roots makes the transform cheap.

The remaining $\log \log n$ factor is the residue of recursive nesting. Getting all the way down to $O(n \log n)$ required the multi-dimensional approach of Harvey and van der Hoeven (2019), which comes next.

# Harvey-van der Hoeven: $O(n \log n)$

## The Last Factor Standing

We have arrived at the algorithm that reaches $O(n \log n)$. First, a recap.

You now understand that multiplying two $n$-digit integers is really computing a convolution of their digits. You understand that the FFT evaluates a polynomial at all $N$-th roots of unity in $O(N \log N)$ time, and that the Convolution Theorem turns convolution into pointwise multiplication of those values. You understand that Schönhage and Strassen sidestepped floating-point precision by working in the ring $\mathbb{Z}/(2^m + 1)\mathbb{Z}$, where twiddle factors are just bit-shifts.

And you understand the one blemish: the $\log \log n$ factor. It comes from the fact that the NTT's pointwise multiplications are themselves multiplications on smaller numbers, requiring their own NTTs, which require their own pointwise multiplications, and so on. The recursion bottoms out after $\log \log n$ levels, each contributing $O(n \log n)$ work. Multiply those together: $O(n \log n \log \log n)$.

For 48 years, from 1971 to 2019, nobody could remove the extra factor entirely. In 2007 Martin Fürer shrank it from $\log \log n$ to the even slower-growing $2^{O(\log^{\ast} n)}$. Then David Harvey and Joris van der Hoeven removed it.

## The Intuition: Why $\log \log n$ Exists and How to Eliminate It

To understand the fix, we first need a sharper picture of the disease.

### The disease: every level costs the same

In Schönhage-Strassen, we split our $n$-bit number into $K \approx \sqrt{n}$ chunks of about $\sqrt{n}$ bits each, held in ring elements of $m \approx 2\sqrt{n}$ bits. The NTT on these chunks is cheap (just bit-shifts and additions), but the **pointwise multiplications** (the $K$ products of $m$-bit numbers in $\mathbb{Z}/(2^m+1)$) each require a recursive call to the entire algorithm.

At the next level down, each $m$-bit multiplication splits into about $\sqrt{m}$ chunks of about $\sqrt{m}$ bits, and so on. Up to constant factors, the problem sizes form a chain:

$$
n \;\to\; \sqrt{n} \;\to\; n^{1/4} \;\to\; n^{1/8} \;\to\; \cdots \;\to\; O(1)
$$

This chain has $\log \log n$ links (since $n^{1/2^d} = O(1)$ when $2^d \approx \log n$, giving $d \approx \log \log n$). Each link does $O(n \log n)$ work in total: the sub-problems shrink, but there are twice as many bits in play at every level, and the two effects cancel. The $\log \log n$ factor is simply the number of links in this chain.

### The cure: make each level cheaper than the last

The knife-edge from the previous section points at the fix. The chain itself is harmless. What hurts is that every link costs the *same*. If each level cost a fixed fraction less than the one above it, the levels would sum like a geometric series and the whole chain would cost a constant times its first link: $O(n \log n)$.

Write the Schönhage-Strassen recurrence in the form

$$
M(n) \;\le\; \frac{2n}{n'}\, M(n') + O(n \log n), \qquad n' \approx n^{1/2}.
$$

Two numbers control it. The $2$ in the numerator is the expansion: a product needs twice the bits of its factors. The $1/2$ in the exponent is how fast the sub-problems shrink: taking a square root halves the logarithm. Measured against $n \log n$, each level costs $2 \times \tfrac12 = 1$ times the one above. That is the knife-edge.

Now suppose we could take $d$-th roots, not square roots, and pay an expansion of $K$ for it:

$$
M(n) \;<\; \frac{K n}{n'}\, M(n') + O(n \log n), \qquad n' = n^{1/d + o(1)}.
$$

Each level would cost $K/d$ times the one above. If $d$ can be made larger than $K$, the ratio drops below one and the $\log \log n$ disappears.

So the whole problem becomes: find a way to cut the problem size to a $d$-th root, for $d$ as large as we like, **without the expansion $K$ growing along with $d$**. Schönhage-Strassen cannot do it. In $\mathbb{Z}/(2^m+1)$ the number $2$ is a root of unity of order only $2m$, so a transform can have at most $2m$ points, and that ties the number of chunks to the size of each chunk. The split is stuck at $\sqrt{n}$. Getting unstuck is what the rest of Harvey and van der Hoeven's paper is for.

## The Architecture: Three Key Ideas

### Idea 1: Fold the sequence into a $d$-dimensional array

Split the $n$-bit inputs into chunks of about $\log n$ bits, which gives about $n / \log n$ coefficients. Now choose $d$ distinct primes $s_1, \ldots, s_d$, all about the same size, whose product is about $n / \log n$. Each one is roughly $(n/\log n)^{1/d}$.

Because the $s_i$ are distinct primes, they are pairwise coprime, and the Chinese Remainder Theorem identifies a position $k$ in a line of length $s_1 \cdots s_d$ with its list of remainders $(k \bmod s_1, \ldots, k \bmod s_d)$, a position in a $d$-dimensional grid. The same identification holds for the rings we are convolving in:

$$
\mathbb{Z}[x]/(x^{s_1 \cdots s_d} - 1) \;\cong\; \mathbb{Z}[x_1, \ldots, x_d]/(x_1^{s_1}-1, \ldots, x_d^{s_d}-1)
$$

On the left is one long cyclic convolution. On the right is the same computation arranged on an $s_1 \times \cdots \times s_d$ grid, where it can be done with a multi-dimensional Fourier transform: one-dimensional transforms along each axis in turn.

Two points are easy to get wrong. The number of dimensions $d$ is a fixed constant. It does not grow with $n$; it will turn out to be $1729$. And the sides are not small: each $s_i$ grows like the $d$-th root of the input. What the grid buys is that a transform along one axis only needs roots of unity of order about $n^{1/d}$, however long the whole array is. That is the escape from the constraint that pinned Schönhage-Strassen at $\sqrt{n}$.

The coefficients are treated as complex numbers in fixed-point arithmetic, carried to a number of bits proportional to $\log n$. The paper bounds the rounding error at every step, so that rounding the final answer recovers the exact integers.

### Idea 2: Use Gaussian resampling to make primes act like powers of 2

Fast transforms want power-of-two lengths. The sides $s_i$ are primes, because the Chinese Remainder Theorem needs them coprime, and no two powers of two are. How do we bridge the gap?

For each $i$, let $t_i$ be a power of two slightly larger than $s_i$. Harvey and van der Hoeven introduce a technique they call **Gaussian resampling**, which converts a DFT of length $s_i$ into a DFT of length $t_i$. The input is spread onto the longer grid with Gaussian weights, transformed there, and the spreading is then undone on the other side. It works because a Gaussian is its own Fourier transform, up to scaling: the weights stay sharply concentrated on both sides of the transform, so the conversion is cheap and loses only a controlled amount of precision.

The classical way to handle an awkward transform length is Bluestein's chirp trick, which re-expresses the DFT as a convolution. Gaussian resampling is a different tool for the same kind of problem, and it is the main new idea in the paper. (Bluestein's trick still has a job, as Idea 3 shows.)

The net effect: a transform on an $s_1 \times \cdots \times s_d$ grid is replaced by a transform on a $t_1 \times \cdots \times t_d$ grid whose sides are all powers of two.

### Idea 3: Use synthetic roots of unity to make transforms multiplication-free

With power-of-two sides, Bluestein's trick comes back: because every $t_i$ is even, the chirp repeats with period $t_i$, so it turns the DFT into a cyclic convolution on the same $t_1 \times \cdots \times t_d$ grid, with no padding. That convolution can be computed over a ring built to make transforms cheap. Take $R = \mathbb{C}[y]/(y^r + 1)$ for $r$ a power of two. In this ring:

- $y$ is a root of unity of order $2r$, since $y^r = -1$.
- Multiplying an element of $R$ by a power of $y$ is a **cyclic shift** of its coefficients with some sign changes (free, just as multiplying by $2$ in $\mathbb{Z}/(2^m + 1)$ was free for Schönhage-Strassen).

This is the same idea as Schönhage and Strassen's bit-shift roots of unity, in the polynomial form of Nussbaumer's fast polynomial transforms. In one dimension it runs into the wall described above: the transform can be no longer than the order of the root. In $d$ dimensions the wall is much further away. Each axis only needs roots of order $t_i$, so one ring $R$, with $r$ about the side length, covers the whole grid of about $r^d$ points: one axis becomes the variable $y$ itself, and the other $d - 1$ are transformed over $R$.

So the transforms themselves use **no multiplications** in the traditional sense, only additions, subtractions and shifts. The expensive multiplications that remain are the pointwise products of elements of $R$. Each is a product of two polynomials with about $r$ coefficients of about $\log n$ bits, which is an integer multiplication of roughly $n^{1/d}$ bits. Those are the recursive calls.

Note what has and has not changed. The recursion is still there. Harvey and van der Hoeven did not cut the chain; they changed how fast it shrinks. The sub-problems are now $d$-th roots of the input, not square roots.

## How the Pieces Fit Together

The full algorithm, stripped to its skeleton:

1. **Split** the $n$-bit inputs into about $n / \log n$ chunks of about $\log n$ bits each.

2. **Reshape** the chunks, by the Chinese Remainder Theorem, into a $d$-dimensional array with prime sides $s_1, \ldots, s_d$, each about $(n/\log n)^{1/d}$.

3. **Resample** along each axis, replacing the transform of size $s_1 \times \cdots \times s_d$ with one of size $t_1 \times \cdots \times t_d$, all powers of two.

4. **Transform**: Bluestein's trick turns the power-of-two DFT into a cyclic convolution, computed with transforms over $R = \mathbb{C}[y]/(y^r + 1)$, where multiplying by a root of unity is a signed cyclic shift.

5. **Pointwise multiply** in $R$. Each product is an integer multiplication of about $n^{1/d}$ bits, done by a recursive call.

6. **Invert** the transform and the resampling, round to integers, propagate carries and reassemble the product.

Everything except step 5 costs $O(n \log n)$. Step 5 makes about $K n / n'$ recursive calls on inputs of $n' = n^{1/d + o(1)}$ bits, which is the recurrence from the start of this section:

$$
M(n) \;<\; \frac{K n}{n'}\, M(n') + O(n \log n)
$$

The paper shows that $K = 1728$ is enough, whatever $d$ is. Each level therefore costs $K/d$ times the one above, and for any $d > 1728$ the levels form a convergent geometric series:

$$
M(n) = O(n \log n) \cdot \left(1 + \frac{K}{d} + \left(\frac{K}{d}\right)^2 + \cdots\right) = O(n \log n)
$$

**Total: $O(n \log n)$.** [Vol. IV](/blog/2025/12/19/On-Multiplication-Vol-IV) comes back to this recurrence.

## Why 1729?

Because it is $1728 + 1$. The dimension has to be larger than the expansion constant $K = 1728$, and $1729$ is the first integer that is. The authors chose the simplest proof over the smallest constant, and they [outline refinements](https://hal.science/hal-02070778) (Section 5.4) that bring $K$ down to about $8$, so that any $d \ge 9$ would do.

The appearance of **1729**, Ramanujan's famous "taxicab number" and the smallest number expressible as the sum of two cubes in two different ways, is, as far as the paper says, a coincidence, but a poetic one. The analysis produces $1728$, which happens to be $12^3$, so that $1729 = 12^3 + 1^3$, which is also $10^3 + 9^3$. But it is fitting that the algorithm that seemed, for a while, to close the book on multiplication complexity should bear, in its constant, an echo of Hardy's taxi ride to visit Ramanujan.

The price of all this machinery is the size at which it starts to work. The proof as written applies only to inputs of at least $2^{1729^{12}}$ bits. To put that number in perspective:
- The observable universe contains roughly $10^{80}$ atoms.
- The exponent $1729^{12}$ alone is a 39-digit number, so $2^{1729^{12}}$ written out in decimal would run to about $2 \times 10^{38}$ digits.
- If every atom in the universe were a hard drive, and every hard drive stored $10^{15}$ digits, you could store roughly $10^{95}$ digits. This is *nothing* compared to the $2^{1729^{12}}$ bits of a single input.

This is a **galactic algorithm**: correct, and useless for any computation that will ever be performed in the physical universe. But its existence answers a question that had stood open since Schönhage and Strassen's 1971 conjecture: **can multiplication be done in $O(n \log n)$?** The answer is yes.

## The View from the Summit

Looking back at the full arc:

| Year | Algorithm | Complexity | Key Insight |
|------|-----------|-----------|-------------|
| antiquity | Schoolbook | $O(n^2)$ | Every digit meets every digit |
| 1960 | Karatsuba | $O(n^{1.585})$ | One clever identity saves 25% per level |
| 1963 | Toom-Cook | $O(n^{1+\varepsilon})$ for any $\varepsilon > 0$ | Split into $k$ parts; interpolate at $2k-1$ points |
| 1971 | Schönhage-Strassen | $O(n \log n \log \log n)$ | NTT in $\mathbb{Z}/(2^m+1)$; roots of unity via bit-shifts |
| 2007 | Fürer | $n \log n \cdot 2^{O(\log^{\ast} n)}$ | Cheap synthetic roots of unity inside a complex FFT |
| 2019 | Harvey-van der Hoeven | $O(n \log n)$ | A 1,729-dimensional transform; each recursion level cheaper than the last |

Each breakthrough changed the *kind* of mathematics being used. Karatsuba's was an algebraic identity. Toom-Cook was polynomial algebra. Schönhage-Strassen was number-theoretic harmonic analysis. Harvey-van der Hoeven is multi-dimensional Fourier analysis carried out in carefully bounded approximate arithmetic.

And yet the punchline is the same as it was in the schoolbook algorithm: we are still just multiplying digits together and adding up the results. Every advance has been about finding a cleverer *order* in which to do it.

The summit has more mountain behind it. [Vol. IV](/blog/2025/12/19/On-Multiplication-Vol-IV) asks why $n \log n$ looked so much like a floor, and [Vol. V](/blog/2026/10/08/On-Multiplication-Vol-V) covers a 2026 preprint that claims $O(n (\log n)^{1-\kappa})$ for a tiny $\kappa > 0$, built directly on top of the algorithm described here.
