---
layout: post
title: "On Multiplication, Vol. IV: Sorting and the Structure of Computation"
date: 2025-12-19 12:03:00
mathjax: true
---

*On Multiplication:* [Vol. I](/blog/2025/12/19/On-Multiplication) · [Vol. II](/blog/2025/12/19/On-Multiplication-Vol-II) · [Vol. III](/blog/2025/12/19/On-Multiplication-Vol-III) · **Vol. IV**

# Connections to Sorting Algorithms

Volumes [I](/blog/2025/12/19/On-Multiplication) through [III](/blog/2025/12/19/On-Multiplication-Vol-III) traced the 60-year journey from $O(n^2)$ to $O(n \log n)$ for integer multiplication. But if you have studied algorithms before, that destination -- $O(n \log n)$ -- should feel familiar. It is the same complexity that governs comparison-based sorting: Merge Sort, Heapsort, and any optimal sorting algorithm all run in $\Theta(n \log n)$ time.

Is this a coincidence? It is not. The connection runs deep, and understanding it illuminates *why* $n \log n$ appears as a fundamental barrier across seemingly unrelated problems.

## The Information-Theoretic Lower Bound

The $n \log n$ term does not arise from any particular algorithmic trick. It arises from **entropy** -- from the sheer amount of information that must be processed to solve the problem at all.

### Sorting: Counting Permutations

Consider sorting $n$ elements. The input is some unknown permutation of $\{1, 2, \ldots, n\}$, and the algorithm must determine *which* of the $n!$ possible permutations it is looking at. Every comparison-based sorting algorithm can be modeled as a binary decision tree: at each internal node, the algorithm compares two elements and branches left or right. The leaves of this tree correspond to the $n!$ possible outcomes.

A binary tree with $L$ leaves has depth at least $\log_2 L$. Since our tree must have at least $n!$ leaves:

$$
\text{depth} \;\geq\; \log_2(n!)
$$

Stirling's approximation gives us:

$$
\log_2(n!) \;=\; \sum_{k=1}^{n} \log_2 k \;=\; n \log_2 n - n \log_2 e + O(\log n) \;=\; \Theta(n \log n)
$$

Each comparison provides at most 1 bit of information (left or right). Therefore, *any* comparison-based sorting algorithm must make at least $\Omega(n \log n)$ comparisons in the worst case. This is not a statement about any particular algorithm -- it is a statement about the *information content* of the problem itself.

### Multiplication: Counting Convolutions

Now consider multiplying two $n$-bit integers. The output is a $2n$-bit number, and each output bit can depend on every input bit from both operands. The "mixing" that must occur -- the convolution of $n$ digits with $n$ digits -- produces $2n - 1$ output coefficients, each of which is a sum of products involving up to $n$ terms.

The information-theoretic argument here is more subtle than in sorting (and, crucially, a tight $\Omega(n \log n)$ lower bound for integer multiplication has *not* been formally proven -- this remains a major open problem). But the heuristic reasoning is compelling: the FFT is the canonical way to compute a length-$n$ convolution, and the FFT requires $\frac{n}{2} \log_2 n$ butterfly operations, each combining two values. The data must pass through $\log_2 n$ stages, with $O(n)$ work per stage. Any algorithm that computes the same convolution must, in some sense, perform the same total information routing.

The structural parallel is striking:

| | **Sorting** | **Multiplication** |
|---|---|---|
| **Problem** | Identify one permutation out of $n!$ | Compute a convolution of $n$ coefficients |
| **Information content** | $\log_2(n!) = \Theta(n \log n)$ bits | $\Theta(n \log n)$ bits of mixing (conjectured) |
| **Per-step bandwidth** | $O(n)$ comparisons | $O(n)$ butterfly operations |
| **Minimum steps** | $\Omega(\log n)$ | $\Omega(\log n)$ |
| **Total work** | $\Omega(n \log n)$ | $O(n \log n)$ (achieved by HvH) |

Both problems hit the same wall: $n$ data items that must be "mixed" through $\log n$ stages of $O(n)$ work each.

## The Symmetry of the Recurrence

Beyond the information-theoretic parallel, there is an algebraic one: both optimal sorting and optimal multiplication satisfy the same *recurrence relation*.

### Merge Sort

Merge Sort divides $n$ elements into two halves, recursively sorts each half, and merges the results in $O(n)$ time:

$$
T(n) = 2\,T\!\left(\frac{n}{2}\right) + O(n)
$$

By the Master Theorem (Case 2: $a = 2$, $b = 2$, $f(n) = O(n)$, so $n^{\log_b a} = n^1 = n = f(n)$), this solves to:

$$
T(n) = O(n \log n)
$$

### Harvey-van der Hoeven Multiplication

The HvH algorithm decomposes an $n$-coefficient convolution into $K$ sub-convolutions of size $n/K$ each, with $O(n)$ work for the FFT and pointwise operations at each level:

$$
T(n) = K \cdot T\!\left(\frac{n}{K}\right) + O(n)
$$

This is the *same* Master Theorem case regardless of $K$: we have $a = K$, $b = K$, $n^{\log_b a} = n^1 = n = f(n)$, giving:

$$
T(n) = O(n \log n)
$$

The recurrences are structurally identical. In both cases, the algorithm splits the problem into $K$ pieces of size $n/K$ and does $O(n)$ work to split and recombine. The $\log n$ factor is simply the depth of the recursion tree: $\log_K n$ levels, each costing $O(n)$. The particular value of $K$ (2 for Merge Sort, $\sqrt{n}$ for Schönhage-Strassen, a carefully chosen composite for HvH) affects the constant factors but not the asymptotic complexity.

The critical difference is that Schönhage-Strassen's "recombine" step secretly contains *additional recursive multiplications* -- the pointwise products in $\mathbb{Z}/(2^m + 1)$ -- which add a $\log \log n$ overhead atop the clean recurrence. Harvey and van der Hoeven's achievement was making the recombine step *truly* $O(n)$ by using Nussbaumer's technique to eliminate those inner multiplications. Once they did, the recurrence collapsed to the same clean form as Merge Sort, and $O(n \log n)$ fell out immediately.

## The Hypercube: A Shared Geometry

The deepest way to see the connection is through the lens of **communication on a hypercube** -- a model that unifies both algorithms geometrically.

### What is a Hypercube?

A $d$-dimensional hypercube $Q_d$ is a graph with $2^d$ nodes. Each node is labeled by a $d$-bit binary string, and two nodes are connected by an edge if and only if their labels differ in exactly one bit. For example, $Q_3$ (the 3-cube) is the familiar wireframe cube with 8 vertices and 12 edges.

Three properties make the hypercube the natural "arena" for divide-and-conquer algorithms:

1. **Recursive decomposition.** $Q_d$ consists of two copies of $Q_{d-1}$ joined by edges along the $d$-th coordinate. This mirrors the way both Merge Sort and FFT-based multiplication split their input in half (or into $K$ parts) at each level.

2. **Logarithmic diameter.** Despite having $N = 2^d$ nodes, the longest shortest path in $Q_d$ has length $d = \log_2 N$. Any piece of information can reach any other node in at most $\log N$ steps. This is the geometric origin of the $\log n$ factor.

3. **Vertex symmetry.** Every node in $Q_d$ looks structurally identical to every other node -- there are no bottlenecks, no privileged positions. This ensures that the algorithm's workload is evenly distributed across all data items.

### Sorting on the Hypercube

To sort $n$ elements on a hypercube, we can use **Bitonic Sort** (Batcher, 1968). The idea is to treat the $n$ array positions as the $n$ nodes of a hypercube ($d = \log_2 n$ dimensions) and perform *compare-exchange* operations along each dimension sequentially.

In a single step along one dimension, the hypercube supports $n/2$ parallel comparisons -- one across each edge in that dimension. This is the *bandwidth* of one dimension: $O(n)$ bits of information resolved per step.

There are $d = \log_2 n$ dimensions, and each dimension requires $O(d)$ compare-exchange rounds in Bitonic Sort, giving $O(\log^2 n)$ parallel steps. (An asymptotically optimal sorting network, like the AKS network, achieves $O(\log n)$ parallel steps, fully saturating the hypercube's bandwidth.)

The total work is:

$$
\underbrace{O(n)}_{\text{comparisons per step}} \;\times\; \underbrace{O(\log n)}_{\text{steps}} \;=\; O(n \log n)
$$

The $n \log n$ is precisely the entropy of $n!$ permutations being drained at a rate of $O(n)$ bits per step over $O(\log n)$ steps. When every lane of the hypercube is fully utilized at every step, we say the algorithm **saturates the bandwidth**. No sorting algorithm can do better, because there is no more information capacity to exploit.

### Multiplication on the Hypercube

Now consider the FFT butterfly network for an $n$-point transform. Draw it as a diagram with $\log_2 n$ stages, each consisting of $n/2$ butterfly operations. If you squint at this diagram, you will notice something: *it is a hypercube*. Each butterfly connects two nodes whose indices differ in exactly one bit position (the bit corresponding to that stage). The FFT literally routes data along the edges of $Q_d$.

In Schönhage-Strassen, this hypercube routing is not quite "clean." The pointwise multiplications at each stage are themselves recursive FFTs on smaller hypercubes, creating a nested hierarchy. The nesting depth is $\log \log n$, and the overhead at each level prevents the algorithm from fully saturating the bandwidth of the outer hypercube. There is "congestion" -- some lanes carry recursive sub-computations instead of direct data movement.

Harvey and van der Hoeven's breakthrough was, in geometric terms, a way to *eliminate the congestion*. By lifting the one-dimensional convolution into a multi-dimensional array and choosing the dimensions so that Nussbaumer's technique replaces the recursive multiplications with additions and cyclic shifts, they ensured that the FFT butterfly at each level performs *pure data routing* -- no hidden recursive work, no congestion. Every lane of the hypercube carries useful information at every step.

The result: multiplication, like sorting, saturates the hypercube's bandwidth. Both algorithms move $O(n)$ units of information per step across $O(\log n)$ steps, for a total of $O(n \log n)$. The two problems -- one about ordering elements, the other about convolving digits -- are solved by the *same geometric machine*.

## Sorting *Is* Multiplying. Multiplying *Is* Sorting.

We can now say something stronger than "sorting and multiplication are *analogous*." They are, in a precise algebraic sense, the *same operation* -- projections of a single underlying phenomenon onto different mathematical surfaces.

### The Shared Abstraction: Rearranging Information Across Dimensions

Consider what sorting actually does. You have $n$ data items, each sitting at some position. The items are "tangled" -- their current positions bear no relation to their values. To sort is to *untangle* them: to route each item from its current position to its correct position. The difficulty of sorting is exactly the difficulty of this routing problem. The items must move through a network (comparisons, swaps), and the network has finite bandwidth. The entropy $\log_2(n!)$ measures the total amount of routing information that must be resolved. The $n \log n$ is the cost of pushing that information through the $\log n$ dimensions of a hypercube, one dimension at a time.

Now consider what multiplication does. You have $n$ coefficients in one polynomial and $n$ coefficients in another. Each output coefficient of the product is a sum of terms $a_i \cdot b_j$ where $i + j$ equals the output index. The coefficients are "tangled" -- every input coefficient contributes to multiple output coefficients, and the contributions overlap. To multiply is to *untangle* them: to route each partial product $a_i \cdot b_j$ to its correct output position $i + j$ and accumulate the results. The FFT does this by decomposing the routing into $\log n$ stages of butterfly operations, each resolving one "dimension" of the entanglement.

Strip away the surface details -- the comparisons, the twiddle factors, the carry propagation -- and you are left with the same skeleton:

> **$n$ items are entangled across $\log n$ dimensions. Untangling them requires touching all $n$ items once per dimension. The cost is $n \log n$.**

Sorting untangles *order*. Multiplication untangles *convolution*. But "untangling" is the same verb in both sentences, and $n \log n$ is its conjugation.

### Making It Algebraic

We can make this even more precise. Both problems can be formulated as applying a *linear transform* to a vector of length $n$:

- **Sorting** is the application of a *permutation matrix* $P \in \{0,1\}^{n \times n}$ to the input vector. The "problem" is that we don't know which permutation matrix to apply until we've inspected the data. The decision tree that determines $P$ has depth $\Omega(\log_2(n!)) = \Omega(n \log n)$.

- **Multiplication** (via convolution) is the application of a *circulant matrix* $C \in \mathbb{Z}^{n \times n}$ to the input vector, where $C_{ij} = b_{(i-j) \bmod n}$. The FFT diagonalizes this circulant: $C = F^{-1} \hat{C} F$, where $F$ is the DFT matrix and $\hat{C}$ is diagonal. The cost of applying $F$ and $F^{-1}$ is $O(n \log n)$.

In both cases, we are applying a structured matrix to a vector of $n$ elements. The permutation matrix has $n!$ possible forms; the circulant matrix has $n$ free parameters but acts on a pair of inputs, yielding $O(n)$ degrees of freedom in the output. The algebraic structure of these matrices -- their factorization into sparse stages, their decomposition along the dimensions of a hypercube -- is *identical*. The DFT matrix $F$ factors into $\log n$ stages of sparse butterfly matrices. A sorting network factors into $\log n$ stages of sparse comparison-swap matrices. Both are "hypercube decompositions" of their respective transforms.

This is why the same $n \log n$ appears. It is not a coincidence, not a vague analogy, not a metaphor. It is the same theorem applied to two different matrix families.

### The Linearithmic Manifold

There is a beautiful way to see all of this in a single picture. Imagine a space of all "rearrangement problems" on $n$ items -- every computational task whose essence is routing $n$ pieces of information to their correct destinations through a network of finite bandwidth. Call this the **linearithmic manifold**: the space of problems whose optimal solutions require $\Theta(n \log n)$ operations.

Sorting lives on this manifold: $n$ items, $n!$ possible destinations, $\log n$ dimensions of routing.

Multiplication lives on this manifold: $n$ coefficients, $2n - 1$ output positions, $\log n$ dimensions of spectral decomposition.

The Fast Fourier Transform lives on this manifold: $n$ time-domain samples, $n$ frequency-domain samples, $\log n$ butterfly stages.

Even matrix transposition on a $\sqrt{n} \times \sqrt{n}$ matrix lives on this manifold: $n$ entries, each needing to swap its row and column coordinates, requiring $\Theta(n \log n)$ cache misses in the I/O model.

These problems are not merely "similar in complexity." They are *manifestations of the same geometric constraint*: the constraint that moving $n$ items across $\log n$ dimensions, with $O(n)$ bandwidth per dimension, costs exactly $n \log n$. The linearithmic manifold is not a metaphor -- it is the deep reason that $n \log n$ recurs so obsessively across computer science.

Sorting is multiplying in the permutation dimension.
Multiplying is sorting in the convolution dimension.
They are the same mountain, seen from different valleys.

---

# Conclusion: The Structure of Computation Itself

## What We've Witnessed

Let us step back and take in the full panorama.

We began with the schoolbook algorithm -- a method so natural, so seemingly inevitable, that Andrey Kolmogorov, one of the greatest mathematicians of the twentieth century, stood before his seminar in 1960 and conjectured that its $O(n^2)$ cost was a law of nature. Multiplication, he believed, was inherently quadratic. Every digit of one number must "see" every digit of the other, and there is no shortcut around that combinatorial explosion.

He was wrong within a week.

What Karatsuba discovered was not merely a faster algorithm. It was a *philosophical* rupture. The schoolbook method treats multiplication as a flat, two-dimensional grid: row meets column, partial product accumulates, carry propagates. Karatsuba's trick -- computing three half-size products where four seemed necessary -- revealed that this grid was not a law of arithmetic but an *artifact of how we happened to organize the computation*. The digits still meet. The partial products still accumulate. But by choosing a cleverer grouping, by exploiting the algebraic identity $(x_1 + x_0)(y_1 + y_0) = x_1 y_1 + x_1 y_0 + x_0 y_1 + x_0 y_0$, Karatsuba showed that some of those meetings are redundant -- their information content is already captured elsewhere.

This is the thread that runs through everything we've seen.

## The Changing Language of Speedup

Each breakthrough in this story didn't just produce a faster algorithm; it changed the *mathematical language* in which multiplication is expressed.

**Karatsuba** spoke the language of **algebra**: a single polynomial identity turns four sub-problems into three, and the Master Theorem does the rest. The savings are modest -- $O(n^{1.585})$ versus $O(n^2)$ -- but the conceptual leap is enormous. For the first time, the exponent on multiplication was negotiable.

**Toom-Cook** generalized this into the language of **polynomial interpolation**. If splitting a number in two and evaluating at three points (Karatsuba) drops the exponent to $\log_2 3$, then splitting into $k$ pieces and evaluating at $2k - 1$ points drops it to $\log_k (2k - 1)$. As $k$ grows, the exponent approaches $1 + \varepsilon$ for any $\varepsilon > 0$. This was the first hint that $O(n^{1+\varepsilon})$ was not the floor -- that perhaps the true cost of multiplication is not polynomial in $n$ at all, but something closer to $n$ times a slowly growing function.

**Schönhage-Strassen** rewrote multiplication in the language of **harmonic analysis**. The Convolution Theorem -- the deep fact that convolution in the time domain becomes pointwise multiplication in the frequency domain -- transforms the entire problem. Instead of asking "how do I combine digits?", we ask "how do I move between representations of a polynomial?" The Fast Fourier Transform answers that question in $O(n \log n)$ time. But the need for exact integer arithmetic, not floating-point approximations, forced Schönhage and Strassen into the ring $\mathbb{Z}/(2^m + 1)\mathbb{Z}$, where roots of unity are powers of two and "multiplication by a twiddle factor" is just a bit-shift. The cost of this exactness was a recursive structure whose depth -- $\log \log n$ levels -- contributed a stubborn extra factor.

**Harvey and van der Hoeven** completed the journey by fusing **multi-dimensional algebraic geometry** with **analytic number theory**. Their insight was architectural: by lifting the one-dimensional convolution into a multi-dimensional array, choosing dimensions via Gaussian integers in $\mathbb{Z}[i]$ to ensure coprimality, and using Nussbaumer's trick to eliminate the innermost recursive multiplications entirely, they flattened the recursive chain from $\log \log n$ levels to a constant. The $O(n \log n)$ barrier -- conjectured for decades, tantalizingly close since 1971 -- was finally reached.

The mathematical toolkit escalated at every stage: from high-school algebra, to polynomial interpolation, to Fourier analysis over finite rings, to algebraic geometry over Gaussian integers. And yet -- and this is the remarkable part -- the *problem never changed*. At every stage, we are still multiplying two numbers. We are still computing the same convolution of digits, still propagating the same carries. What changed is our understanding of the *geometry* of the computation: the realization that there exist clever rearrangements of the same arithmetic operations that cancel redundancies invisible from the schoolbook perspective.

## The Information-Theoretic Floor

Is $O(n \log n)$ truly optimal? We cannot prove it is, but there are strong reasons to believe it.

Multiplying two $n$-bit numbers produces a $2n$-bit result. Each bit of the output can depend on every bit of both inputs. The information that must flow through the computation -- the "mixing" of input bits into output bits -- is at least $\Omega(n \log n)$ by plausible circuit-complexity arguments, though a formal proof remains one of the great open problems in theoretical computer science.

What we *can* say is that multiplication has reached the same complexity class as sorting: $\Theta(n \log n)$. And as we showed in the previous section, this is not a coincidence -- it is the *same theorem*. Both problems live on what we called the linearithmic manifold: the space of computational tasks whose essence is routing $n$ pieces of information across $\log n$ dimensions of a finite-bandwidth network. Sorting routes elements to their correct positions in the permutation dimension. Multiplication routes partial products to their correct positions in the convolution dimension. The $n \log n$ is not an accident of algorithmic cleverness -- it is the price the universe charges for untangling $n$ things, regardless of *what* those things are or *why* they are tangled.

## Galactic Algorithms and the Nature of Truth

We should be honest about the practical situation. Karatsuba's algorithm overtakes schoolbook multiplication at around 20-40 digits, depending on the implementation. Toom-Cook-3 wins around 100-200 digits. Schönhage-Strassen becomes competitive at tens of thousands of digits -- the scale used by modern big-integer libraries like GMP. But Harvey-van der Hoeven? Its crossover point is somewhere beyond $2^{1729^{12}}$ digits. That number has more digits than there are atoms in the observable universe. No computer that will ever exist will multiply numbers that large. The Harvey-van der Hoeven algorithm will never be *run*.

And yet it matters enormously.

It matters because mathematics is not engineering. The question "what is the true complexity of integer multiplication?" is a question about the structure of arithmetic itself, not about what silicon can compute before the heat death of the universe. The existence of an $O(n \log n)$ algorithm -- even one that is galactically impractical -- tells us something true about the nature of numbers: that the information required to multiply them is not quadratic, not $n^{1.585}$, not $n \log n \log \log n$, but $n \log n$. That is a *theorem about reality*, not a software optimization.

Galactic algorithms are the astronomer's telescope pointed at the foundations of computation. We will never travel to a quasar, but knowing it exists changes our understanding of the universe. Similarly, we will never run Harvey-van der Hoeven on actual inputs, but knowing it exists changes our understanding of what multiplication *is*.

## The Punchline

Here is the thought to carry away.

Kolmogorov looked at schoolbook multiplication and saw $n^2$ -- a grid of partial products, rigid and inescapable. Karatsuba looked at the same grid and saw that some cells were redundant. Toom and Cook saw that the grid was really a polynomial, and polynomials can be evaluated at fewer points than their degree suggests. Schönhage and Strassen saw that the polynomial was really a signal, and signals can be decomposed into frequencies. Harvey and van der Hoeven saw that the signal lived in a multi-dimensional space whose geometry could be exploited to eliminate every last bit of overhead.

Each generation looked at the *same object* -- the product of two integers -- and saw deeper structure. The number didn't change. Our eyes did.

And when, at the end of this journey, we looked sideways and noticed that sorting -- a completely different problem about ordering, not arithmetic -- lands at exactly the same $n \log n$ cost for exactly the same geometric reasons, we glimpsed something deeper still. Sorting is multiplying in the permutation dimension. Multiplying is sorting in the convolution dimension. They are two faces of a single truth: that rearranging $n$ things across $\log n$ dimensions of entanglement costs $n \log n$, and not a single operation less.

That, in the end, is what mathematics is: the systematic refinement of vision. The history of multiplication algorithms is not a story about making computers faster. It is a story about learning to see -- and discovering, at the bottom, that everything we were looking at was the same thing all along.

---

## Further Reading
Wonderful Wikipedia : https://en.wikipedia.org/wiki/Multiplication_algorithm

Exploration of Varying Radix on Intel i3-4025U : https://miracl.com/blog/missing-a-trick-karatsuba-variations-michael-scott/

Karatsuba paper: https://ieeexplore.ieee.org/document/4402691

Toom-Cook: A. L. Toom, "The Complexity of a Scheme of Functional Elements Realizing the Multiplication of Integers" (1963); S. A. Cook, "On the Minimum Computation Time of Functions" (1966, PhD Thesis, Harvard)

Schönhage–Strassen paper: A. Schönhage and V. Strassen, "Schnelle Multiplikation großer Zahlen," *Computing* 7 (1971), pp. 281--292. https://doi.org/10.1007/BF02242355

Harvey and van der Hoeven's Paper : https://hal.archives-ouvertes.fr/hal-03182372/document

https://www.tcs.tifr.res.in/~ramprasad/assets/pubs/expositions/Schonhage-Strassen.pdf

https://www.youtube.com/watch?v=m5VZnlVU2n4

https://www.youtube.com/watch?v=OGUMsBkZqkc

---

*On Multiplication:* [Vol. I](/blog/2025/12/19/On-Multiplication) · [Vol. II](/blog/2025/12/19/On-Multiplication-Vol-II) · [Vol. III](/blog/2025/12/19/On-Multiplication-Vol-III) · **Vol. IV**
