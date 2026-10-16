---
layout: post
title: "On Multiplication, Vol. IV: Sorting and the Mirage of n log n"
date: 2025-12-19 12:03:00
description: "Why comparison sorting's n log n lower bound is a theorem and integer multiplication's never was, though their fast algorithms share one recurrence."
mathjax: true
---

*On Multiplication:* [I](/blog/2025/12/19/On-Multiplication) · [II](/blog/2025/12/19/On-Multiplication-Vol-II) · [III](/blog/2025/12/19/On-Multiplication-Vol-III) · **IV** · [V](/blog/2026/10/08/On-Multiplication-Vol-V)

# A Tempting Parallel: Sorting

Volumes [I](/blog/2025/12/19/On-Multiplication) through [III](/blog/2025/12/19/On-Multiplication-Vol-III) traced the 60-year descent from $O(n^2)$ to $O(n \log n)$ for integer multiplication. But if you have studied algorithms before, that destination, $O(n \log n)$, should feel familiar. It is the same complexity that governs comparison-based sorting: Merge Sort, Heapsort, and any optimal comparison sort all run in $\Theta(n \log n)$ time.

Is this a coincidence? For half a century it was natural to think not: that the two problems were related, and that $n \log n$ was a single barrier appearing in two places. The case for that view is worth laying out carefully, because every piece of it is individually true. The trouble is in what the pieces are taken to add up to.

## One Lower Bound Is a Theorem. The Other Never Was.

For sorting, the $n \log n$ does not come from any particular algorithmic trick. It comes from **entropy**: the amount of information the algorithm must acquire before it can know the answer.

### Sorting: Counting Permutations

Consider sorting $n$ elements. The input is some unknown permutation of $n$ distinct keys, and the algorithm must determine *which* of the $n!$ possible permutations it is looking at. Every comparison-based sorting algorithm can be modeled as a binary decision tree: at each internal node, the algorithm compares two elements and branches left or right. The leaves of this tree correspond to the $n!$ possible outcomes.

A binary tree with $L$ leaves has depth at least $\log_2 L$. Since our tree must have at least $n!$ leaves:

$$
\text{depth} \;\geq\; \log_2(n!)
$$

Stirling's approximation gives us:

$$
\log_2(n!) \;=\; \sum_{k=1}^{n} \log_2 k \;=\; n \log_2 n - n \log_2 e + O(\log n) \;=\; \Theta(n \log n)
$$

Each comparison provides at most 1 bit of information (left or right). Therefore, *any* comparison-based sorting algorithm must make $\Omega(n \log n)$ comparisons in the worst case. This is not a statement about any particular algorithm. It is a statement about the *information content* of the problem itself.

It is also a statement about a *model*. The proof counts comparisons, and it binds only algorithms that learn about their input through comparisons. Let the algorithm look inside its keys and the bound stops applying: on a word RAM, integers can be sorted in $O(n \log \log n)$ time (Han) and faster still with randomness (Han and Thorup). The $\Theta(n \log n)$ of sorting is a theorem, but it is a theorem about comparing.

### Multiplication: Counting Convolutions

Now consider multiplying two $n$-bit integers. The output is a $2n$-bit number, and each bit in its upper half can depend on every input bit from both operands. The "mixing" that must occur, the convolution of $n$ digits with $n$ digits, produces $2n - 1$ output coefficients, each of which is a sum of products involving up to $n$ terms.

It is tempting to run the same kind of argument here. The FFT is the canonical way to compute a length-$n$ convolution, and a radix-2 FFT performs $\frac{n}{2} \log_2 n$ butterfly operations, each combining two values. The data must pass through $\log_2 n$ stages, with $O(n)$ work per stage. Surely any algorithm that computes the same convolution must, in some sense, perform the same total information routing?

No such theorem exists, and none ever did. There is no decision tree here and nothing to count: the input is fully visible and the output is a fixed function of it, so the algorithm has nothing to *learn*. The only lower bound ever proved for multiplying two $n$-bit integers on a multitape Turing machine, with the whole input available from the start, is the trivial one, $\Omega(n)$, for reading the input. Schönhage and Strassen *conjectured* $n \log n$ in 1971. That conjecture is what a 2026 preprint, the subject of [Vol. V](/blog/2026/10/08/On-Multiplication-Vol-V), claims to refute.

Here is the comparison, row by row:

| | **Sorting** | **Multiplication** |
|---|---|---|
| **Problem** | Identify one permutation out of $n!$ | Compute a convolution of $n$ coefficients |
| **Classical algorithm** | Merge Sort | FFT-based (Schönhage-Strassen, Harvey-van der Hoeven) |
| **Per-step bandwidth** | $O(n)$ comparisons | $O(n)$ butterfly operations |
| **Steps** | $O(\log n)$ | $O(\log n)$ |
| **Total work** | $O(n \log n)$ | $O(n \log n)$ |
| **Lower bound** | $\Omega(n \log n)$ comparisons: **proved** | $\Omega(n \log n)$: **conjectured; the 2026 preprint claims a disproof** |

Both algorithms do $O(n)$ work at each of $\log n$ stages. Only one of the two problems *requires* it.

## The Symmetry of the Recurrence

The resemblance that made the parallel so persuasive is algebraic: Merge Sort and the Fast Fourier Transform at the heart of fast multiplication satisfy the same *recurrence relation*.

### Merge Sort

Merge Sort divides $n$ elements into two halves, recursively sorts each half, and merges the results in $O(n)$ time:

$$
T(n) = 2\,T\!\left(\frac{n}{2}\right) + O(n)
$$

By the Master Theorem (Case 2: $a = 2$, $b = 2$, and the merge costs $\Theta(n) = \Theta(n^{\log_b a})$), this solves to:

$$
T(n) = O(n \log n)
$$

### The Fast Fourier Transform

A radix-2 FFT of length $n$ splits its input into even- and odd-indexed halves, transforms each half recursively, and recombines them with $n/2$ butterflies:

$$
T(n) = 2\,T\!\left(\frac{n}{2}\right) + O(n)
$$

It is the same recurrence, symbol for symbol, and it solves the same way:

$$
T(n) = O(n \log n)
$$

In both cases, the algorithm splits the problem into two halves and does $O(n)$ work to split and recombine. The $\log n$ factor is simply the depth of the recursion tree: $\log_2 n$ levels, each costing $O(n)$. (Splitting into any fixed number $k$ of pieces gives $k \cdot T(n/k) + O(n)$ and the same answer, with $\log_k n$ levels.)

Multiplying integers adds a *second* recursion on top of the transform, and this is where the two algorithms of [Vol. III](/blog/2025/12/19/On-Multiplication-Vol-III) part ways. In Schönhage-Strassen, the pointwise products are themselves multiplications, of numbers twice as wide as the chunks they came from. Every level of that recursion costs the same $O(n \log n)$, and there are $\log \log n$ levels. Harvey and van der Hoeven's achievement was to make the levels *shrink*. Their recurrence has the form

$$
M(n) \;<\; \frac{K n}{n'}\, M(n') + O(n \log n), \qquad n' = n^{1/d + o(1)},
$$

with $K = 1728$ and a number of dimensions $d$ that they are free to choose. They take $d = 1729$; any constant larger than $K$ would do. Measured against $n \log n$, each level then costs $K/d < 1$ times the one above it, so the levels sum like a geometric series and only the top one matters: one transform's worth of work, $O(n \log n)$, the same total as Merge Sort.

Note what this is a symmetry *between*: two algorithms. A recurrence is an upper bound. It tells you what one method costs, and nothing about what every method must cost.

## The Hypercube: A Shared Geometry

The most vivid way to see the resemblance is through **communication on a hypercube**, a model that describes both algorithms geometrically.

### What is a Hypercube?

A $d$-dimensional hypercube $Q_d$ is a graph with $2^d$ nodes. Each node is labeled by a $d$-bit binary string, and two nodes are connected by an edge if and only if their labels differ in exactly one bit. For example, $Q_3$ (the 3-cube) is the familiar wireframe cube with 8 vertices and 12 edges.

Three properties make the hypercube the natural "arena" for divide-and-conquer algorithms:

1. **Recursive decomposition.** $Q_d$ consists of two copies of $Q_{d-1}$ joined by edges along the $d$-th coordinate. This mirrors the way both Merge Sort and FFT-based multiplication split their input in half (or into $k$ parts) at each level.

2. **Logarithmic diameter.** Despite having $N = 2^d$ nodes, the longest shortest path in $Q_d$ has length $d = \log_2 N$. Any piece of information can reach any other node in at most $\log N$ steps. This is the geometric origin of the $\log n$ factor.

3. **Vertex symmetry.** Every node in $Q_d$ looks structurally identical to every other node: there are no bottlenecks, no privileged positions. This suits algorithms whose workload is spread evenly across all data items.

### Sorting on the Hypercube

To sort $n$ elements on a hypercube, we can use **Bitonic Sort** (Batcher, 1968). The idea is to treat the $n$ array positions as the $n$ nodes of a hypercube ($d = \log_2 n$ dimensions) and perform *compare-exchange* operations along each dimension sequentially.

In a single step along one dimension, the hypercube supports $n/2$ parallel comparisons, one across each edge in that dimension. This is the *bandwidth* of one dimension: $O(n)$ bits of information resolved per step.

There are $d = \log_2 n$ dimensions, and each dimension requires $O(d)$ compare-exchange rounds in Bitonic Sort, giving $O(\log^2 n)$ parallel steps. (The AKS network of Ajtai, Komlós and Szemerédi reaches the optimal $O(\log n)$ parallel steps, though its comparators do not follow hypercube edges.)

At the optimal depth, the total work is:

$$
\underbrace{O(n)}_{\text{comparisons per step}} \;\times\; \underbrace{O(\log n)}_{\text{steps}} \;=\; O(n \log n)
$$

The $n \log n$ is the entropy of $n!$ permutations being drained at a rate of $O(n)$ bits per step over $O(\log n)$ steps. When every lane of the hypercube is fully utilized at every step, we say the algorithm **saturates the bandwidth**. No comparison-based sorting algorithm can do better, because there is no more information capacity to exploit.

### Multiplication on the Hypercube

Now consider the FFT butterfly network for an $n$-point transform. Draw it as a diagram with $\log_2 n$ stages, each consisting of $n/2$ butterfly operations. If you squint at this diagram, you will notice something: *it is a hypercube*. Each butterfly connects two nodes whose indices differ in exactly one bit position (the bit corresponding to that stage). The FFT literally routes data along the edges of $Q_d$.

In Schönhage-Strassen, this hypercube routing is not quite "clean." The pointwise multiplications between the forward and inverse transforms are themselves done by recursive FFTs on smaller hypercubes, creating a nested hierarchy. The nesting depth is $\log \log n$, and the overhead at each level prevents the algorithm from fully saturating the bandwidth of the outer hypercube. There is "congestion": some lanes carry recursive sub-computations instead of direct data movement.

Harvey and van der Hoeven's breakthrough was, in geometric terms, a way to *eliminate the congestion*. By lifting the one-dimensional convolution into a multi-dimensional array and choosing the dimensions so that Nussbaumer's technique turns the multiplications inside the transform into additions and cyclic shifts, they ensured that the FFT butterfly at each level performs *pure data routing*. The recursive multiplications that remain shrink so fast from one level to the next that they add only a constant factor. Every lane of the hypercube carries useful information at every step.

The result: Harvey-van der Hoeven multiplication saturates the hypercube's bandwidth. Like Merge Sort, it moves $O(n)$ units of information per step across $O(\log n)$ steps, for a total of $O(n \log n)$. By 2019 the two problems, one about ordering elements and the other about convolving digits, looked like jobs for the *same geometric machine*.

## Where the Parallel Breaks

It is a short step from here to a grand claim: that sorting is multiplying and multiplying is sorting, that the two are projections of a single underlying phenomenon, and that there is a whole family of problems whose essence is routing $n$ items across $\log n$ dimensions at a cost of exactly $n \log n$.

The step is a mistake, and it is worth being precise about which one.

### A shared upper bound is not a shared lower bound

Everything in the two sections above compares *algorithms*: the same recurrence, the same network, the same bandwidth. All of that is still true. But two problems being solved by similar machines says nothing about whether either machine is necessary. Sorting has a separate, independent argument for necessity: the decision tree. Multiplication never had one. The parallel quietly lent multiplication a lower bound that belonged to sorting.

### Learning is not the same as moving

Sorting's bound counts information the algorithm must *acquire*: which of $n!$ arrangements is this? Nothing analogous is hidden in a multiplication. The $n \log n$ there was the cost of *moving* partial products to where they belong, one FFT stage at a time, and "you must move $n$ things through $\log n$ stages" is an assumption about method, not a consequence of the problem.

### Bits are not envelopes

The hypercube picture treats data as indivisible items that travel along edges. A permutation network really is limited that way. A computer is not: it can add two bits together, send the sum, and subtract later. The 2026 preprint's central procedure exchanges two address fields of an array stored on tape (a pure permutation in its final effect) by passing through XOR combinations of the data, and does it in fewer passes than moving the data would take. Routing arguments cannot see such an algorithm at all.

### A census

Four problems are natural candidates for that family. Here is where each one stands:

| Problem | Model | Is $n \log n$ a proved lower bound? | Status |
|---|---|---|---|
| Comparison sorting | comparisons | Yes, by the decision tree | stands |
| Integer multiplication | multitape Turing machine | No, only conjectured | $O(n (\log n)^{1-\kappa})$ claimed, $\kappa = 2^{-182}$ |
| Discrete Fourier transform | exact complex arithmetic, unrestricted coefficients | No (only for bounded coefficients) | $O(n (\log n)^{1 - 10^{-13}})$ claimed |
| Matrix transposition | multitape Turing machine | No (only for restricted machines, such as ones that may only move data) | falls with multiplication, as a corollary |

One of the four still stands at $n \log n$, and it is the one whose floor was a theorem rather than a guess.

So sorting and multiplication are not intertwined. Sorting is provably $\Theta(n \log n)$ in the comparison model. Multiplication has an upper bound that keeps falling and no meaningful lower bound at all. They looked like the same mountain from two valleys. One of them turned out to be a mountain, and the other a cloud that had been sitting at the same height.
