---
layout: post
title: "On Multiplication, Vol. III: Schönhage-Strassen and Harvey-van der Hoeven"
date: 2025-12-19 12:02:00
mathjax: true
---

*On Multiplication:* [I](/blog/2025/12/19/On-Multiplication) · [II](/blog/2025/12/19/On-Multiplication-Vol-II) · **III** · [IV](/blog/2025/12/19/On-Multiplication-Vol-IV) · [V](/blog/2026/10/08/On-Multiplication-Vol-V)

# Schönhage-Strassen: Multiplication in $O(n \log n \log \log n)$

## The Precision Problem

The FFT-based multiplication pipeline described in [Vol. II](/blog/2025/12/19/On-Multiplication-Vol-II) works over the **complex numbers**. The twiddle factors $\omega_N^k = e^{2\pi i k/N}$ are irrational (for most $k$), and so are the intermediate values in the FFT. On a real computer, we approximate these with floating-point arithmetic.

For multiplying two numbers with $n$ digits, the convolution coefficients can be as large as $O(n B^2)$ (where $B$ is the base). To distinguish these integers exactly after rounding, we need floating-point precision of roughly $O(\log n + 2\log B)$ bits. For large $n$, this means we need **multi-precision floating-point arithmetic** inside the FFT itself -- and each multi-precision operation costs more than $O(1)$.

This creates a vicious circle: to multiply $n$-digit numbers, we use the FFT, but the FFT internally needs high-precision multiplications, which are themselves expensive. The complex-number FFT approach does not, by itself, yield a clean $O(n \log n)$ integer multiplication algorithm.

Schönhage and Strassen's 1971 breakthrough was to eliminate this precision problem entirely by moving from the complex numbers to an **exact algebraic setting** where roots of unity exist but rounding errors do not.

## From $\mathbb{C}$ to $\mathbb{Z}/(2^m + 1)\mathbb{Z}$: The Number Theoretic Transform

### Roots of unity in finite rings

The FFT algorithm does not actually require the complex numbers. It requires only a ring $R$ that contains:

1. An element $\omega$ of multiplicative order $N$ (an "$N$-th root of unity"), meaning $\omega^N = 1$ and $\omega^k \neq 1$ for $0 < k < N$.
2. An inverse of $N$ in $R$ (for the inverse transform).

If $R$ is a finite ring (like $\mathbb{Z}/p\mathbb{Z}$ for a prime $p$), then all arithmetic is exact -- no rounding, no precision issues. An FFT performed in such a ring is called a **Number Theoretic Transform (NTT)**.

**Example.** In $\mathbb{Z}/5\mathbb{Z}$, the element $2$ has order $4$: $2^1 = 2$, $2^2 = 4$, $2^3 = 3$, $2^4 = 1 \pmod{5}$. So $\omega = 2$ is a primitive $4$th root of unity in $\mathbb{Z}/5\mathbb{Z}$, and we can perform a 4-point NTT modulo 5 with exact arithmetic.

### Schönhage and Strassen's choice: Fermat-like rings

To multiply two $n$-bit integers, Schönhage and Strassen work in the ring:

$$
R = \mathbb{Z} / (2^m + 1)\mathbb{Z}
$$

for a carefully chosen $m$. This ring has a remarkable property: the element $\omega = 2$ (or more precisely, a small power of $2$) serves as a root of unity, and **multiplication by powers of 2 in this ring is just a bit-shift followed by a reduction modulo $2^m + 1$** -- an operation that costs $O(m)$, which is essentially free.

Why does $2$ behave as a root of unity here? Note that $2^m \equiv -1 \pmod{2^m + 1}$, so $2^{2m} \equiv 1 \pmod{2^m + 1}$. Thus $2$ has multiplicative order dividing $2m$ in this ring. With an appropriate choice of $m$, we can ensure that $2$ (or a power of it) is a primitive $N$-th root of unity for the $N$ we need.

The critical advantage: all the "twiddle factor multiplications" in the FFT butterfly -- which in the complex-number FFT require expensive multi-precision multiplications -- reduce to **bit-shifts and additions** in $\mathbb{Z}/(2^m + 1)\mathbb{Z}$. This makes the per-butterfly cost $O(m)$ instead of $O(m \log m \cdots)$, dramatically simplifying the recursion.

## The Algorithm in Detail

### Step 0: Setup

Given two $n$-bit integers $x$ and $y$, choose parameters:
- Let $K = 2^k$ for some $k$ (the number of chunks).
- Let $\ell = \lceil n / K \rceil$ (the chunk size in bits).
- Let $m \approx 2\ell + k$ (the size of a ring element in bits).
- Work in the ring $R = \mathbb{Z}/(2^m + 1)\mathbb{Z}$.

Why is $m$ about *twice* $\ell$? Because the ring has to hold the answer, not just the input. A convolution coefficient is a sum of up to $K$ products of two $\ell$-bit chunks, so it can be as large as $K \cdot 2^{2\ell} = 2^{2\ell + k}$. The modulus must exceed that, or the coefficients wrap around and are lost. This factor of two looks like bookkeeping. It turns out to be the entire source of the $\log \log n$, as we will see below.

The parameters are chosen so that $K \approx \sqrt{n}$ (roughly), meaning we split each input into about $\sqrt{n}$ chunks of about $\sqrt{n}$ bits each, held in a ring whose elements are about $2\sqrt{n}$ bits wide.

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
- Twiddle factor multiplications $\omega^k \cdot v$ are implemented as **cyclic bit-shifts** of $v$, costing $O(m)$.
- Each butterfly costs $O(m)$: one bit-shift plus two modular additions.
- Total: $N/2 \cdot \log_2 N$ butterflies, each $O(m)$, giving $O(Nm \log N)$ bit operations.

### Step 3: Pointwise multiplication

Compute $\hat{c}_k = \hat{a}_k \cdot \hat{b}_k$ in $R$ for each $k = 0, \ldots, N - 1$.

Each of these is a multiplication of two $m$-bit numbers modulo $2^m + 1$. But wait -- this is itself a multiplication of smaller numbers! This is where the algorithm becomes **recursive**: we use the Schönhage-Strassen algorithm itself (on inputs of size $m$ instead of $n$) to perform these multiplications.

There are $N$ such multiplications, each on operands of size $m$. This is the "recursive nesting" that generates the $\log \log n$ factor.

### Step 4: Inverse NTT

Compute $\mathbf{c} = \text{INTT}_N(\hat{\mathbf{c}})$. Same cost as the forward NTT: $O(Nm \log N)$.

### Step 5: Carry propagation and reassembly

The vector $\mathbf{c}$ now contains the convolution of $\mathbf{a}$ and $\mathbf{b}$ modulo $2^m + 1$. (The parameters are chosen so that no coefficient is large enough to "wrap around" the modulus -- the modulus is larger than any possible convolution coefficient.) Reassemble the final product by performing carries across the chunks.

## Why $\log \log n$?

The complexity breaks down as follows. At the top level we have:
- NTT and INTT: $O(Nm \log N)$ bit operations for the transforms, which is $O(n \log n)$.
- Pointwise multiplications: recursive multiplications on $m$-bit inputs.

How many recursive multiplications? One more detail matters here. A plain convolution of two length-$K$ sequences has $2K - 1$ coefficients, which is why the pipeline above pads the transform to length $N \geq 2K$. Schönhage and Strassen avoid the padding: they compute the product modulo $2^n + 1$, which turns the convolution into a *wrapped* one of length exactly $K$. So only $K$ pointwise products are needed, each on ring elements of $m \approx 2n/K$ bits.

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

This is the Schönhage-Strassen bound, and it sits on a knife-edge. Without the doubling -- if the recurrence were $T(n) = \sqrt{n} \cdot T(\sqrt{n}) + O(n \log n)$ -- the levels would shrink geometrically, $n \log n \,(1 + \tfrac12 + \tfrac14 + \cdots)$, and the total would be a clean $O(n \log n)$. With slightly *more* than doubling -- $2K$ pointwise products instead of $K$ -- the levels would grow geometrically and the total would be $O(n \log^2 n)$. The $\log \log n$ lives exactly at the balance point between the two. Harvey and van der Hoeven make the same observation about this recurrence in their own paper: the constant 2 "plays a crucial role in the complexity analysis," because it keeps the cost of the transforms the same at every level.

So the $\log \log n$ factor is not a deficiency of the FFT itself -- the FFT is $O(n \log n)$. It is the cost of the **recursive multiplications** needed at each level of the NTT, on numbers that are twice as wide as the chunks they came from.

## A Comparison

| Algorithm             | Complexity                     | Key Innovation                        |
|-----------------------|--------------------------------|---------------------------------------|
| Schoolbook            | $O(n^2)$                       | Direct digit-by-digit                 |
| Karatsuba             | $O(n^{1.585})$                 | 4 multiplications $\to$ 3            |
| Toom-3                | $O(n^{1.465})$                 | 9 multiplications $\to$ 5            |
| Schönhage-Strassen    | $O(n \log n \log \log n)$      | NTT in $\mathbb{Z}/(2^m+1)$         |
| Harvey-van der Hoeven | $O(n \log n)$                  | Multi-dimensional NTT (see below)    |

The jump from Toom-Cook to Schönhage-Strassen is qualitatively different from all previous improvements. Karatsuba and Toom-Cook are algebraic tricks that reduce the exponent toward 1 but never reach it. Schönhage-Strassen breaks through to a *nearly-linear* bound by replacing polynomial interpolation at finitely many points with Fourier analysis at the roots of unity -- and crucially, by doing so in an exact algebraic ring where the symmetry of the roots makes the transform cheap.

The remaining $\log \log n$ factor is the residue of recursive nesting. Eliminating it required the multi-dimensional approach of Harvey and van der Hoeven (2019), which we now discuss.

# Harvey-van der Hoeven: $O(n \log n)$

## The Last Factor Standing

We have arrived at the final chapter -- or what was the final chapter until October 2026, when [Vol. V](/blog/2026/10/08/On-Multiplication-Vol-V) had to be added. Let us take stock of where we are.

You now understand that multiplying two $n$-digit integers is really computing a convolution of their digits. You understand that the FFT evaluates a polynomial at all $N$-th roots of unity in $O(N \log N)$ time, and that the Convolution Theorem lets us turn this evaluation into multiplication. You understand that Schönhage and Strassen sidestepped floating-point precision by working in the ring $\mathbb{Z}/(2^m + 1)\mathbb{Z}$, where twiddle factors are just bit-shifts.

And you understand the one blemish: the $\log \log n$ factor. It comes from the fact that the NTT's pointwise multiplications are themselves multiplications on smaller numbers, requiring their own NTTs, which require their own pointwise multiplications, and so on. The recursion bottoms out after $\log \log n$ levels, each contributing $O(n \log n)$ work. Multiply those together: $O(n \log n \log \log n)$.

For 48 years -- from 1971 to 2019 -- nobody could kill that last factor. Then David Harvey and Joris van der Hoeven did.

## The Intuition: Why $\log \log n$ Exists and How to Eliminate It

To understand the fix, we first need a sharper picture of the disease.

### The disease: a long chain of recursive calls

In Schönhage-Strassen, we split our $n$-bit number into $K \approx \sqrt{n}$ chunks of about $\sqrt{n}$ bits each, held in ring elements of $m \approx 2\sqrt{n}$ bits. The NTT on these chunks is cheap (just bit-shifts and additions), but the **pointwise multiplications** -- the $K$ products of $m$-bit numbers in $\mathbb{Z}/(2^m+1)$ -- each require a recursive call to the entire algorithm.

At the next level down, each $m$-bit multiplication splits into about $\sqrt{m}$ chunks of about $\sqrt{m}$ bits, and so on. Up to constant factors, the problem sizes form a chain:

$$
n \;\to\; \sqrt{n} \;\to\; n^{1/4} \;\to\; n^{1/8} \;\to\; \cdots \;\to\; O(1)
$$

This chain has $\log \log n$ links (since $n^{1/2^d} = O(1)$ when $2^d \approx \log n$, giving $d \approx \log \log n$). Each link does $O(n \log n)$ work in total: the sub-problems shrink, but there are twice as many bits in play at every level, and the two effects cancel. The $\log \log n$ factor is simply the number of links in this chain.

### The cure: make the chain shorter

Harvey and van der Hoeven's idea, at its core, is beautifully simple: **if the recursion depth is the problem, reduce the recursion depth.**

Instead of splitting into $\sqrt{n}$ pieces (which halves the exponent at each level), split into **far more** pieces that are **far smaller**. If you split an $n$-bit number into $n/\log n$ pieces of $\log n$ bits each, then the recursive subproblems have size $\log n$ -- which is already small enough to multiply by schoolbook in $O((\log n)^2)$ time! The recursion bottoms out in a single step. No chain. No $\log \log n$.

But this creates a new problem. With $n / \log n$ chunks, the NTT must operate on a sequence of length $\sim n / \log n$, and the transform must happen in a ring large enough to hold the convolution without overflow. Finding a ring that simultaneously supports (a) cheap roots of unity, (b) sufficiently many of them, and (c) exact arithmetic with no precision loss -- all while keeping the transform cost to $O(n \log n)$ -- is the hard part. This is where the paper earns its 80 pages.

## The Architecture: Three Key Ideas

### Idea 1: Fold the sequence into a multi-dimensional array

Rather than treating the $n / \log n$ chunks as a flat list, Harvey and van der Hoeven reshape them into a $d$-dimensional array of size $s_1 \times s_2 \times \cdots \times s_d$, where each $s_i$ is a small prime and $\prod s_i \approx n / \log n$.

Why does this help? A $d$-dimensional convolution can be computed by performing **1-dimensional DFTs along each dimension** in succession (this is the standard "row-column" algorithm for multidimensional transforms). If each dimension $s_i$ is small, each 1D DFT is cheap. And crucially, the total number of 1D DFT operations is:

$$
\text{cost} = \sum_{i=1}^{d} \frac{S}{s_i} \cdot (\text{cost of a length-}s_i\text{ DFT})
$$

where $S = \prod s_i$. By choosing $d$ to grow with $n$ (specifically, $d \sim \log n / \log \log n$), each $s_i$ stays bounded by a constant, and the DFTs along each dimension have constant cost per element. The total transform cost is $O(S \cdot d) = O\left(\frac{n}{\log n} \cdot \frac{\log n}{\log \log n}\right) = O\left(\frac{n}{\log \log n}\right)$, which is well within the $O(n \log n)$ budget.

The problem is that the Cooley-Tukey radix-2 trick does not work on prime-sized dimensions. This is where the second idea comes in.

### The Chinese Remainder Theorem: The Bridge Between Dimensions

In this algorithm, the Chinese Remainder Theorem (CRT) is the bridge that turns a massive, "one-dimensional" multiplication problem into a more manageable "multi-dimensional" one.

**What is the Chinese Remainder Theorem (CRT)?**

In general mathematics, the CRT is a theorem that allows you to uniquely identify a large number by its remainders when divided by a set of smaller, relatively prime numbers.

In the context of this paper, it is used to create an isomorphism (a structural match) between two different algebraic spaces:

- **One-Dimensional Space:** $\mathbb{Z}[x]/(x^{s_1 \cdots s_d} - 1)$ -- This represents the large integer split into one long line of chunks.

- **Multi-Dimensional Space:** $\mathbb{Z}[x_1, \ldots, x_d]/(x_1^{s_1}-1, \ldots, x_d^{s_d}-1)$ -- This represents the same data arranged on a $d$-dimensional grid (like a cube or hypercube).

**Why use CRT at all?**

The authors use the CRT for several critical reasons:

1. **To enable "Fast Polynomial Transforms."** The fastest tools for this algorithm (Nussbaumer's transforms) require the problem to be structured as a multidimensional grid. The CRT is what allows the authors to "reshape" the flat list of integer chunks into that grid.

2. **To reduce problem size.** By using the CRT to map the data onto a grid of size $s_1 \times s_2 \times \cdots \times s_d$, the problem of computing one giant Discrete Fourier Transform (DFT) is broken down into a collection of much smaller DFTs along each dimension.

3. **Efficient recursion.** The "multi-dimensional" approach is what allows the algorithm to reach the $O(n \log n)$ speed. By splitting the integer into $d$ different dimensions (where $d$ is a parameter they can choose, like 1729), they can reduce the size of the sub-problems much more aggressively at each step of the recursion.

**The Workflow Summary**

1. **Split:** Take the $n$-bit integer and split it into many small chunks.

2. **Map (CRT):** Use the CRT to arrange those chunks into a $d$-dimensional grid based on distinct prime numbers ($s_1, \ldots, s_d$).

3. **Multiply:** Perform the multiplication on this grid using fast Fourier transforms.

4. **Reverse:** Use the inverse of the CRT mapping to "flatten" the result back into a single large integer.

### Idea 2: Gaussian resampling -- making primes act like powers of 2

The Cooley-Tukey FFT requires the transform length to be a power of 2 (or at least highly composite). The dimensions $s_i$ are primes. How do we bridge this gap?

Harvey and van der Hoeven use a technique inspired by **Bluestein's algorithm**, but with a Gaussian twist. The idea is:

1. Embed the length-$s_i$ DFT into a slightly larger length-$t_i$ **cyclic convolution**, where $t_i$ is the next power of 2 above $s_i$.

2. Compute this cyclic convolution using Nussbaumer's algorithm (a multiplication-free polynomial transform), which only needs additions, subtractions, and cyclic shifts.

3. The "embedding" is done via multiplication by a **Gaussian chirp** -- a sequence of the form $e^{\pi i k^2 / s_i}$. The Gaussian chirp has the remarkable property that it converts a DFT into a convolution (this is the classical "chirp-$z$ transform" idea of Bluestein). And because the Gaussian is approximately its own Fourier transform, the approximation errors when rounding $s_i$ up to $t_i$ can be made exponentially small with only $O(1)$ extra bits of precision.

The net effect: each prime-sized DFT is replaced by a power-of-2-sized convolution that can be computed without any multiplications in the traditional sense -- only additions and shifts. The cost per element remains $O(1)$.

### Idea 3: Nussbaumer's algorithm -- transforms without multiplications

The inner convolutions (from Idea 2) are computed using **Nussbaumer's polynomial transform**, which operates over the ring $R[y]/(y^r + 1)$ for $r$ a power of 2. In this ring:

- Multiplication by $y$ is a **cyclic shift** (free, like multiplying by $2$ in $\mathbb{Z}/(2^m + 1)$ was free for Schönhage-Strassen).
- The transform uses only $O(r \log r)$ additions and subtractions -- **no multiplications** at this level.

This is the key that breaks the recursive chain. In Schönhage-Strassen, the pointwise multiplications in the NTT were genuine multiplications that demanded recursive calls. In Harvey-van der Hoeven, the analogous step uses Nussbaumer transforms that need **no multiplications**, only shifts and additions. No recursive call is needed. The chain has been cut.

The only remaining multiplications are tiny: each "pointwise product" in the Nussbaumer-transformed domain amounts to a multiplication of numbers with $O(\log n)$ bits, which can be done by schoolbook in $O((\log n)^2)$ time -- a cost that is absorbed into the $O(n \log n)$ total.

## How the Pieces Fit Together

The full algorithm, stripped to its skeleton:

1. **Split** the $n$-bit inputs into $S \approx n / \log n$ chunks of $\sim \log n$ bits each.

2. **Reshape** the chunk sequence into a $d$-dimensional array ($d \sim \log n / \log \log n$ dimensions, each of prime size $s_i = O(\log \log n)$).

3. **For each dimension** $i = 1, \ldots, d$:
   - Apply the Gaussian chirp to convert the length-$s_i$ DFT along that dimension into a cyclic convolution of length $t_i = O(s_i)$.
   - Compute that cyclic convolution using Nussbaumer's addition-only polynomial transform.

4. **Pointwise multiply** the transformed arrays. Each pointwise product involves numbers of $O(\log n)$ bits -- small enough for schoolbook.

5. **Invert** the multidimensional transform (same process in reverse).

6. **Carry-propagate** and reassemble the final product.

The total cost at each step:
- Steps 3 and 5 (transforms): $O(n)$ additions across $d$ dimensions, times $d = O(\log n / \log \log n)$, giving $O(n \log n / \log \log n)$ -- well within budget.
- Step 4 (pointwise): $S$ multiplications of $O(\log n)$-bit numbers at $O((\log n)^2)$ each, giving $O(n \log n)$.
- Steps 1, 2, 6: $O(n)$.

**Total: $O(n \log n)$.**

## Why 1729?

The algorithm's correctness depends on the Gaussian resampling errors being negligible, which requires extra precision bits. The number of extra bits grows with $d$, and $d$ grows with $n$. Working through the constants, the algorithm only becomes faster than Schönhage-Strassen when $n$ is so large that the constant-factor overhead of managing $d$ dimensions, Gaussian chirps, and Nussbaumer bookkeeping is finally absorbed.

Harvey and van der Hoeven estimate this crossover at numbers with more than $2^{1729^{12}}$ digits.

The appearance of **1729** -- Ramanujan's famous "taxicab number," the smallest number expressible as the sum of two cubes in two different ways -- is a coincidence, but a poetic one. The number arises from a chain of parameter optimizations in the proof, not from any deep connection to Ramanujan's work. But it is fitting that the algorithm that seemed, for a while, to close the book on multiplication complexity should bear, in its constant, an echo of one of mathematics' most beautiful stories.

To put $2^{1729^{12}}$ in perspective:
- The observable universe contains roughly $10^{80}$ atoms.
- $2^{1729^{12}}$ has approximately $10^{38}$ decimal digits in its *exponent alone*.
- If every atom in the universe were a hard drive, and every hard drive stored $10^{15}$ digits, you could store roughly $10^{95}$ digits. This is *nothing* compared to $2^{1729^{12}}$.

This is a **galactic algorithm** -- beautiful, true, and utterly useless for any computation that will ever be performed in the physical universe. But its existence answers a question that stood open for sixty years: **can multiplication be done in $O(n \log n)$?** The answer is yes.

## The View from the Summit

Let us look back at the full arc:

| Year | Algorithm | Complexity | Key Insight |
|------|-----------|-----------|-------------|
| antiquity | Schoolbook | $O(n^2)$ | Every digit meets every digit |
| 1960 | Karatsuba | $O(n^{1.585})$ | One clever identity saves 25% per level |
| 1963 | Toom-Cook | $O(n^{1+\varepsilon})$ for any $\varepsilon > 0$ | Polynomial interpolation at $k$ points |
| 1971 | Schönhage-Strassen | $O(n \log n \log \log n)$ | NTT in $\mathbb{Z}/(2^m+1)$; roots of unity via bit-shifts |
| 2019 | Harvey-van der Hoeven | $O(n \log n)$ | Multi-dim NTT; Nussbaumer kills the recursion |

Each breakthrough changed the *kind* of mathematics being used. Karatsuba's was an algebraic identity. Toom-Cook was polynomial algebra. Schönhage-Strassen was number-theoretic harmonic analysis. Harvey-van der Hoeven is multi-dimensional algebraic geometry fused with analytic number theory.

And yet the punchline is the same as it was in the schoolbook algorithm: we are still just multiplying digits together and adding up the results. Every advance has been about finding a cleverer *order* in which to do it.

*October 2026: the summit turned out to have more mountain behind it. A preprint now claims $O(n (\log n)^{1-\kappa})$ for a tiny $\kappa > 0$, built directly on top of the algorithm described here. See [Vol. V](/blog/2026/10/08/On-Multiplication-Vol-V).*

---

**Next:** [Vol. IV: Sorting and the Mirage of n log n](/blog/2025/12/19/On-Multiplication-Vol-IV)

*On Multiplication:* [Vol. I](/blog/2025/12/19/On-Multiplication) · [Vol. II](/blog/2025/12/19/On-Multiplication-Vol-II) · **Vol. III** · [Vol. IV](/blog/2025/12/19/On-Multiplication-Vol-IV) · [Vol. V](/blog/2026/10/08/On-Multiplication-Vol-V)
