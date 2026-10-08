---
layout: post
title: "On Multiplication, Vol. V: Below n log n"
date: 2026-10-08 12:00:00
mathjax: true
---

*On Multiplication:* [I](/blog/2025/12/19/On-Multiplication) · [II](/blog/2025/12/19/On-Multiplication-Vol-II) · [III](/blog/2025/12/19/On-Multiplication-Vol-III) · [IV](/blog/2025/12/19/On-Multiplication-Vol-IV) · **V**

# The Floor Gives Way

Ten months ago this series stopped at $O(n \log n)$. [Vol. III](/blog/2025/12/19/On-Multiplication-Vol-III) called the Harvey-van der Hoeven algorithm "the final chapter." The first edition of [Vol. IV](/blog/2025/12/19/On-Multiplication-Vol-IV) went further and argued that $n \log n$ was not just the best bound anyone had found but a *floor* -- the same floor that sorting stands on, "the price the universe charges for untangling $n$ things."

That claim now has a 73-page counterargument.

On October 6, 2026, OpenAI published a repository of 719 mathematical manuscripts written by an internal model. Number 109 in its catalogue is called *Integer multiplication below $n \log n$*, and its abstract is two sentences long:

> We give a deterministic algorithm that multiplies two $n$-bit integers in $O(n(\lg n)^{1-\kappa})$ worst-case time, with $\kappa = 2^{-182}$, on one fixed finite-alphabet Turing machine with a fixed finite number of one-dimensional tapes. The algorithm is exact for every input length and disproves the $n \log n$ optimality conjecture of Schönhage and Strassen in this model.

A companion manuscript does the same thing to the Fourier transform itself. And within a day of the release, a community repository started pushing $\kappa$ upward -- conditionally, assuming the original argument holds -- from $2^{-182}$ to better than $2^{-15}$ at the time of writing.

Three warnings before we start. First, this is a preprint: it has not been refereed, and nobody has machine-checked it yet (details [below](#how-sure-are-we)). Second, it is a galactic algorithm in the fullest sense -- more galactic than Harvey-van der Hoeven, which is saying something. Third, it forces a retraction: the conclusion of this series has been rewritten, and it now sits at the bottom of this page.

# What Is Claimed

## The theorem

**Theorem** (OpenAI, preprint dated September 23, 2026). *There is one deterministic multitape Turing machine that, for every $n \ge 1$, computes the exact $2n$-bit product of two $n$-bit integers in worst-case time*

$$
T(n) \;=\; O\!\left(n \,(\lg n)^{1-\kappa}\right), \qquad \kappa = 2^{-182} \approx 1.6 \times 10^{-55}.
$$

Three things about that statement deserve attention.

**It is the same model as before.** Bit operations on a multitape Turing machine is the setting in which Schönhage and Strassen proved $O(n \log n \log \log n)$ in 1971, in which they conjectured $n \log n$ to be optimal, and in which Harvey and van der Hoeven reached $O(n \log n)$ in 2019. No random-access memory, no unit-cost arithmetic on big words. (Those models were never bound by $n \log n$ in the first place: Schönhage showed in 1980 that a pointer machine multiplies in linear time. The $n \log n$ conjecture was always a statement about tapes.)

**It is a power of the logarithm.** The saving is not a $\log \log n$ or a $\log^{\ast} n$ shaved off the side. The exponent on $\lg n$ itself drops below 1, so the ratio of the new bound to $n \log n$ is $(\lg n)^{-\kappa}$, which tends to zero. That is exactly what it takes to refute a conjectured $\Omega(n \log n)$.

**It drags other problems down with it.** Division with remainder and integer square roots follow by Newton iteration at the same cost. So does a less obvious one: transposing an $n \times n$ binary matrix stored row by row on tape, in $O(n^2 (\lg n)^{1-\kappa})$. Hold on to that last corollary. Transposition is a pure permutation -- no arithmetic at all, just bits changing places -- and it matters for what follows.

## Where the $n \log n$ was hiding

Recall the shape of Harvey-van der Hoeven from [Vol. III](/blog/2025/12/19/On-Multiplication-Vol-III). Chop the integers into chunks, lay the chunks out on a $d$-dimensional grid with prime side lengths via the Chinese Remainder Theorem, use Gaussian resampling to trade the prime lengths for powers of two, and compute the resulting transforms over a ring $\mathbb{C}[y]/(y^r + 1)$ in which the roots of unity are powers of $y$ -- so that multiplying by one is a cyclic shift with a sign. By the end, the transform involves no real multiplications. It consists of three kinds of work:

1. **rearranging addresses** (getting the right coordinates of the grid next to each other on the tape),
2. **signed shifts**, and
3. **two-point butterflies**, $(u, v) \mapsto (u + v, u - v)$.

All three are linear-time passes. And that is precisely the problem. The preprint puts it in one sentence:

> Scanning an array of $\Theta(n)$ stored bits at each of $\Theta(\log n)$ transform levels already costs $\Theta(n \log n)$.

Harvey and van der Hoeven had eliminated every cost *except* the passes. What remained was the bare skeleton of a Fourier transform: $\log n$ levels, each one a sweep over all the data. The first edition of Vol. IV looked at that skeleton, called it "saturating the bandwidth," and took it for proof that nothing better was possible. The preprint looks at the same skeleton and asks whether several levels can be done in fewer than several sweeps.

It needs two savings, one for movement and one for arithmetic. Write $V$ for the number of bits stored on the tape:

| Task | Obvious cost | Claimed cost |
|---|---|---|
| Swap two $u$-bit address fields of an array | $O(V \cdot u)$, one pass per bit | $O(V \cdot u^{\tau})$ with $\tau < 1$ |
| Apply the butterfly along $d$ axes at once | $O(V \cdot d)$, one pass per axis | $O(V \cdot d^{\lambda^{\prime}})$ with $\lambda^{\prime} < 1$ |

Each is a power saving in the *number of passes*. Everything else in the paper is the work of threading those two savings through the Harvey-van der Hoeven pipeline without losing them.

# The Trick: Compute Instead of Carry

## Three shears make a swap

Every programmer knows the XOR swap: `a ^= b; b ^= a; a ^= b` exchanges two variables without a temporary. Nothing is ever "moved." The values are mixed together and then unmixed in a different arrangement.

The preprint's address swap starts from the same observation, one level up. Treat the two address fields as numbers $H$ and $D$, with $H$ written earlier on the tape. Then three additions

$$
D \leftarrow D - H, \qquad H \leftarrow H + D, \qquad D \leftarrow H - D
$$

send $(H, D)$ to $(D, H)$. On a tape, the first and third are cheap: they adjust a *later* field using an *earlier* one, which amounts to rotating blocks during a single left-to-right pass. Only the middle one -- an earlier field updated from a later one -- is hard. So the whole problem of **moving** data across the tape collapses into one **shear**, $H \leftarrow H + D$.

## A gadget that swaps by mixing

The shear is carried out by a fixed, finite **linear network** -- call it the gadget. It has two banks of wires, $X$ and $Y$, plus a very large number of scratch wires. A fixed schedule of linear gates runs across them (the paper names the steps *copy*, *gather*, *scatter* and *side injection*), and when it finishes two things are true: the contents of the two banks have been exchanged, and every scratch wire holds exactly what it held at the start, *whatever that was*.

The ingredients are borrowed, and the preprint says from where:

- **Index coding.** If one receiver already knows $a$ and another already knows $b$, a broadcaster can serve both with the single message $a \oplus b$. A low-rank summary, plus what you already hold, yields what you wanted. The gadget's gather and scatter steps squeeze a whole bank through a narrow set of central wires, and its side wires subtract the cross-talk.
- **Set-intersection designs.** The wires are indexed by 3-element subsets of $\lbrace 1, \ldots, 100 \rbrace$, and how strongly wire $T$ leaks into wire $S$ depends only on the size of $S \cap T$. This is the Frankl-Wilson construction, which reached the paper by way of Alon's work on Shannon capacity.
- **Borrowed memory.** Scratch space that arrives full of someone else's data and is handed back unchanged is the signature of *catalytic* computation, due to Buhrman, Cleve, Koucký, Loff and Speelman.

Here is the heart of the bit version. There are $\binom{100}{3} = 161{,}700$ three-element subsets. Each bank has one wire for every ordered *triple* of them -- about $4.2 \times 10^{15}$ wires per bank -- and the gadget works along one of those three coordinates at a time. Within a stage, hold two of the subsets fixed and let the third, $T$, vary. To add $x_T$ into $y_T$ for all 161,700 choices of $T$ at once, the gadget first *gathers*: central wire $i$ receives the sum of every $x_T$ with $i \in T$. Then it *scatters*: $y_S$ receives the sum of the three central wires $i \in S$. The net coefficient from $x_T$ to $y_S$ is the size of $S \cap T$, modulo 2:

| Elements $S$ and $T$ share | Coefficient | |
|---|---|---|
| 3 (so $S = T$) | 1 | wanted |
| 2 | 0 | |
| 1 | 1 | unwanted -- cancelled by the side wires |
| 0 | 0 | |

One hundred central wires and a set of side corrections stand in for 161,700 separate transfers. Run three such stages -- forward, backward, forward, the three-shear pattern again -- and the banks are exchanged.

## Why mixing is cheaper than moving

So far the gadget swaps single values. Now promote every wire to an entire array: deal the rows of the tape out cyclically among the $W$ wires, so that each wire carries a stream holding a $1/W$ share of the data, and apply each gate entry by entry to matching positions. A gate costs a constant number of passes.

The idea that makes this useful is the **frame**. At each point in the schedule, a wire's array may be stored in a different coordinate system -- with its addresses sheared by some matrix. Gates work entrywise, so they do not care what frame the arrays are in, as long as all the arrays meeting at one gate share the *same* frame. Between consecutive gates, a wire has to be converted from one frame to the next, and each unit of conversion is a smaller instance of the original problem: a swap on address fields $1/m$ as wide.

Arrange the frames so that when the gadget finishes, every wire has travelled from "no shear" to "full shear." If each wire made that journey alone, it would need $m$ small conversions -- $W \cdot m$ in total, which is just the obvious algorithm again. But the bank wires do not make the journey alone. The gadget *exchanges* them, and the exchange -- carried out by gates, pointwise, in a constant number of passes -- covers part of the distance for free. The scratch wires give some of that back (the central wires have to retreat one step in mid-schedule), but not all of it.

The final count, with $m = 10^6$:

$$
W = 177{,}176{,}569{,}091{,}445{,}000{,}000 \ \text{wires}, \qquad
\frac{s}{W} = 999{,}999.999985 \ \text{conversions per wire, on average.}
$$

Not a million. A million minus fifteen millionths.

The bookkeeping is finite combinatorics, so you can check it yourself. This reproduces the paper's numbers:

```python
from math import comb

h = 100                       # ground set {1..100}
v = comb(h, 3)                # 161,700 three-element subsets
N = v**3                      # wires per bank
m = h**3                      # 10^6: sub-swaps a wire would need on its own
I = 3 * v * v                 # gadget invocations (3 stages)
z = 3 * comb(97, 2)           # subsets sharing exactly 1 element with a given one
W = 2*N + I * (v*z + 100)     # banks + side wires + central wires
L = I * 100 * h               # rank lost when the central wires step back
s = W*m - N + 2*L             # total sub-swaps actually performed

print(W)          # 177176569091445000000
print(s / W)      # 999999.9999849916
print(s < W * m)  # True
```

## Karatsuba, again

A deficit of fifteen parts in a trillion sounds like nothing. Fed to a recursion, it is an exponent. A swap of width $m f$ becomes $s$ swaps of width $f$, each on a stream of volume $V/W$. Writing $F(e)$ for the cost *per stored bit* of a width-$e$ swap:

$$
F(m f) \;\le\; \frac{s}{W}\, F(f) + O(1)
\quad\Longrightarrow\quad
F(e) = O\!\left(e^{\tau}\right), \qquad \tau = \log_m \frac{s}{W} \;<\; 1.
$$

If you have read [Vol. I](/blog/2025/12/19/On-Multiplication), you have seen this before.

| | Sub-problems you expect | Sub-problems you need | Exponent |
|---|---|---|---|
| Karatsuba (1960), integers | 4 | 3 | $\log_2 3 \approx 1.585$ instead of $2$ |
| Strassen (1969), matrices | 8 | 7 | $\log_2 7 \approx 2.807$ instead of $3$ |
| The 2026 gadget, tape swaps | $1{,}000{,}000$ per wire | $999{,}999.999985$ per wire | about $1 - 10^{-12}$ instead of $1$ |

It is the oldest trick in this series: **a finite identity with a strict deficit, amplified by recursion.** Karatsuba found his deficit in a $2 \times 2$ grid of products. This one lives in a network of $10^{20}$ wires and was, by OpenAI's account, found by a machine.

The second gadget, for butterflies, has the same skeleton with complex scalars in place of bits. Its frames are phases rather than shears, its wire count is about $1.9 \times 10^{21}$, and its relative deficit is $73 / 19{,}906{,}842{,}167{,}500 \approx 3.7 \times 10^{-12}$. It computes many butterfly levels in one recursive sweep the way the first gadget computes many digit-moves.

## From $10^{-11}$ to $2^{-182}$

Why is the final $\kappa$ so much smaller than the gadget's deficit? Because three small numbers get multiplied together. The paper rounds the gadget exponent to a convenient $\tau = 1 - 2^{-50}$. The transform is spread over $d \approx (\lg n)^{\epsilon}$ dimensions with $\epsilon = 2^{-75}$. The address chunks being swapped have width $K \approx d^c$ with $c = 2^{-56}$. The tightest line of the cost table is the chunk exchanges, whose exponent sits below 1 by

$$
\epsilon \cdot c \cdot (1 - \tau) \;=\; 2^{-75} \cdot 2^{-56} \cdot 2^{-50} \;=\; 2^{-181},
$$

and half of that is held in reserve to absorb stray $\log \log n$ factors. Hence $\kappa = 2^{-182}$. The paper is candid about it: "These constants are deliberately conservative; no optimization is claimed."

## What did not change

Almost everything else. The pipeline is still Harvey and van der Hoeven's: Chinese remaindering onto prime axes, Gaussian resampling onto power-of-two axes, Bluestein's chirp trick, Nussbaumer's synthetic roots of unity. The new machine even *calls* the 2019 algorithm: the small polynomial products at the bottom are handed to "the established $O(n \log n)$ multiplier" as an ordinary subroutine. Harvey-van der Hoeven has not been overthrown. It has been demoted to a library call.

# The Companion: A Fourier Transform Below $n \log n$

The second manuscript, *An explicit power saving for the exact discrete Fourier transform* (dated September 25), reuses the complex gadget for a different theorem: the discrete Fourier transform of *any* length $n$ can be computed in

$$
O\!\left(n \,(\log n)^{1 - 10^{-13}}\right)
$$

operations. (The sharper form is $O(n (\log n)^{\theta} (\log \log n)^{4 - \theta})$ with $\theta = 0.99999999999978935\ldots$) The engine is a faster way to apply $C^{\otimes k}$, the $k$-fold tensor power of the two-point kernel

$$
C = \frac{1}{2}\begin{pmatrix} 1+i & 1-i \\ 1-i & 1+i \end{pmatrix},
$$

in $O(2^k (k+1)^{\theta})$ operations instead of the $k \cdot 2^k$ that applying the $k$ factors one at a time would cost. Exact polynomial multiplication over $\mathbb{C}$ follows at the same price.

If you remember the butterfly diagrams of [Vol. II](/blog/2025/12/19/On-Multiplication-Vol-II), this is the claim that stings: $\tfrac{n}{2} \log_2 n$ butterflies is not the minimum.

But read the model carefully, because it is doing real work. Operations are **exact complex arithmetic at unit cost**, with **unrestricted coefficients** and no claim about numerical stability. The paper says outright that it "does not assert a corresponding improvement for stable floating-point FFTs or for bit complexity." That matters, because the FFT *does* have a proved $n \log n$ lower bound -- Morgenstern's, from 1973 -- for linear circuits whose coefficients are bounded. The new algorithm escapes that theorem the only way one can: by using coefficients that are not. In the world Morgenstern described, Cooley-Tukey is still optimal up to a constant, and FFTW is not about to get faster.

# The Exponent Race

After Fürer first got under Schönhage-Strassen in 2007, it took twelve years and a string of papers to grind his leftover factor of $2^{O(\log^{\ast} n)}$ down to $8^{\log^{\ast} n}$, then $4^{\log^{\ast} n}$, then nothing. The sequel is running on a different clock.

A day after OpenAI's release, a community repository -- `CrocSwap/integer-mult-bounds`, maintained by Douglas Colkitt, with nearly twenty named contributors and a good deal of AI assistance -- began treating the preprint's framework as given and optimizing inside it. Its ledger of successive witnesses reads like a countdown:

| Conditional $\kappa$ | Scope of the witness, per the repository's ledger |
|---|---|
| $2^{-182}$ | OpenAI's original parameters |
| $2^{-154}$ | original network and recurrence exponents |
| $2^{-129}$ | original network, sharper recurrence comparison |
| $2^{-107}$ | direct routing, original network |
| $2^{-76}$ | direct routing on a smaller network, tuned parameters |
| $2^{-59}$ | paired sums and a tighter Gaussian setup |
| above $2^{-34}$ | compact controls |
| $2^{-30}$ | a ternary circuit on five-element subsets |
| $\approx 5.1 \times 10^{-5}$, above $2^{-15}$ | a bit network with $m = 575$ and 137 million wires |

In under two days the conditional saving improved by a factor of more than $2^{167}$. The original gadget's $10^{20}$ wires turned out to be wildly more than the idea needs.

The word *conditional* is load-bearing, and the repository is scrupulous about it. Its README calls the work "conditional on the original OpenAI #109 framework" and says it is "not full formal verification, independent human peer review, a worldwide priority claim, or a practical multiplication benchmark." If the foundation moves, the whole tower moves with it. And the last row of that table will be stale by the time you read this.

# How Sure Are We?

Honestly: not yet sure. Here is the state of the evidence on October 8, 2026.

- **Provenance.** Both manuscripts are machine-written. OpenAI's README says the collection was produced by an unreleased internal model that was posed roughly 4,000 open problems, and that it "includes results at different stages of verification."
- **Formal verification.** About 42% of the collection's headline results have Lean formalizations. The Fourier-transform paper is among them: the catalogue lists Lean statements for its transform and convolution theorems. The integer-multiplication paper is **not**. As of today it rests on its 73 pages of prose.
- **Track record.** The day after release, three manuscripts in the collection were withdrawn over a sign error and fourteen more were revised. The README warns that "some of the unformalized results could have issues." That is the process working as intended, and also a reminder of which category the multiplication paper is in.
- **Scrutiny.** The proof is public, explicit about every constant, and being picked over by a great many people at once. The finite combinatorics is easy to recheck (the snippet above reproduces the paper's numbers). The hard part is the other sixty pages: the claim that the gadget's saving survives contact with an actual tape machine -- padding, precision, descriptors, cleanup -- at every depth of the recursion.

If the multiplication proof breaks, this volume will get a postscript, and the Fourier result will still stand in its own model. But notice that the rewritten conclusion below does not depend on the outcome. Its main point is that the $n \log n$ floor was never proved, and that was true all along.

# Still Galactic

To be fair to anyone hoping for a faster `BigInt`: no.

Harvey-van der Hoeven only pulls ahead beyond $2^{1729^{12}}$ digits, and $1729^{12} \approx 2^{129}$, so call it $2^{2^{129}}$. The new algorithm needs at least two dimensions before it can do anything at all, and with $d = \lfloor (\lg n)^{\epsilon} \rfloor$ and $\epsilon = 2^{-75}$ that requires

$$
\lg n \;\ge\; 2^{2^{75}}, \qquad\text{that is,}\qquad n \;\ge\; 2^{2^{2^{75}}} \ \text{bits.}
$$

Below its cutoff, the machine in the theorem -- this is in the paper -- uses **schoolbook multiplication**. And for the saving $(\lg n)^{\kappa}$ to amount to a mere factor of two, constants aside, you would need $n \approx 2^{2^{2^{182}}}$.

For Harvey-van der Hoeven, the *input* does not fit in the universe. Here, the *length of the input*, written out in decimal, does not fit in the universe. Even the community's $\kappa \approx 5 \times 10^{-5}$ would want $n \approx 2^{2^{19601}}$ before it bought that factor of two.

None of this is a criticism. As this series has said before, galactic algorithms are not for running. The arc now reads:

| Year | Result | Bit complexity | The idea |
|------|--------|----------------|----------|
| antiquity | Schoolbook | $O(n^2)$ | Every digit meets every digit |
| 1960 | Karatsuba | $O(n^{1.585})$ | Three products instead of four |
| 1963 | Toom-Cook | $O(n^{1+\varepsilon})$ | Evaluate and interpolate |
| 1971 | Schönhage-Strassen | $O(n \log n \log \log n)$ | An FFT in a ring where roots of unity are bit-shifts |
| 2007 | Fürer | $n \log n \cdot 2^{O(\log^{\ast} n)}$ | Cheap roots of unity most of the time |
| 2019 | Harvey-van der Hoeven | $O(n \log n)$ | Many dimensions; no multiplications inside the transform |
| 2026 | OpenAI preprint (unrefereed) | $O(n (\log n)^{1-\kappa})$, $\kappa = 2^{-182}$ | Mix the data instead of moving it |

---

# Conclusion: The Floor That Wasn't

*This conclusion replaces the one that closed Vol. IV from December 2025 until October 2026.*

## What We've Witnessed

Let us step back and take in the full panorama.

We began with the schoolbook algorithm -- a method so natural, so seemingly inevitable, that Andrey Kolmogorov, one of the greatest mathematicians of the twentieth century, stood before his seminar in 1960 and conjectured that its $O(n^2)$ cost was a law of nature. Multiplication, he believed, was inherently quadratic. Every digit of one number must "see" every digit of the other, and there is no shortcut around that combinatorial explosion.

He was wrong within a week.

What Karatsuba discovered was not merely a faster algorithm. It was a *philosophical* rupture. The schoolbook method treats multiplication as a flat, two-dimensional grid: row meets column, partial product accumulates, carry propagates. Karatsuba's trick -- computing three half-size products where four seemed necessary -- revealed that this grid was not a law of arithmetic but an *artifact of how we happened to organize the computation*. The digits still meet. The partial products still accumulate. But by choosing a cleverer grouping, by exploiting the algebraic identity $(x_1 + x_0)(y_1 + y_0) = x_1 y_1 + x_1 y_0 + x_0 y_1 + x_0 y_0$, Karatsuba showed that some of those meetings are redundant -- their information content is already captured elsewhere.

This is the thread that runs through everything we've seen.

It also runs through this series' own mistake. Kolmogorov looked at the best method anyone knew and took its cost for a law of arithmetic. Sixty-five years later, the first edition of this conclusion looked at the best method anyone knew -- one sweep over the data per level of a transform, $\log n$ levels -- and took *its* cost for a law of information. It is the same error, one logarithm further down.

## The Changing Language of Speedup

Each breakthrough in this story didn't just produce a faster algorithm; it changed the *mathematical language* in which multiplication is expressed.

**Karatsuba** spoke the language of **algebra**: a single polynomial identity turns four sub-problems into three, and the Master Theorem does the rest. The savings are modest -- $O(n^{1.585})$ versus $O(n^2)$ -- but the conceptual leap is enormous. For the first time, the exponent on multiplication was negotiable.

**Toom-Cook** generalized this into the language of **polynomial interpolation**. If splitting a number in two and evaluating at three points (Karatsuba) drops the exponent to $\log_2 3$, then splitting into $k$ pieces and evaluating at $2k - 1$ points drops it to $\log_k (2k - 1)$. As $k$ grows, the exponent approaches $1 + \varepsilon$ for any $\varepsilon > 0$. This was the first hint that $O(n^{1+\varepsilon})$ was not the floor -- that perhaps the true cost of multiplication is not polynomial in $n$ at all, but something closer to $n$ times a slowly growing function.

**Schönhage-Strassen** rewrote multiplication in the language of **harmonic analysis**. The Convolution Theorem -- the deep fact that convolution in the time domain becomes pointwise multiplication in the frequency domain -- transforms the entire problem. Instead of asking "how do I combine digits?", we ask "how do I move between representations of a polynomial?" The Fast Fourier Transform answers that question in $O(n \log n)$ time. But the need for exact integer arithmetic, not floating-point approximations, forced Schönhage and Strassen into the ring $\mathbb{Z}/(2^m + 1)\mathbb{Z}$, where roots of unity are powers of two and "multiplication by a twiddle factor" is just a bit-shift. The cost of this exactness was a recursive structure whose depth -- $\log \log n$ levels -- contributed a stubborn extra factor.

**Harvey and van der Hoeven** fused **multi-dimensional algebraic geometry** with **analytic number theory**. Their insight was architectural: by lifting the one-dimensional convolution into a multi-dimensional array, choosing dimensions via Gaussian integers in $\mathbb{Z}[i]$ to ensure coprimality, and using Nussbaumer's trick to eliminate the innermost recursive multiplications entirely, they flattened the recursive chain from $\log \log n$ levels to a constant. The $O(n \log n)$ bound -- conjectured for decades to be the end of the road, tantalizingly close since 1971 -- was finally reached.

**The 2026 preprint**, if it stands, speaks the language of **coding theory**. Its raw material is not arithmetic at all: index codes, set-intersection designs, scratch memory that is borrowed and returned. Its insight is that a machine asked to *move* data may instead *mix* it, and that mixing, organized around a finite gadget with a deficit of a few parts in a trillion, gets the data where it is going in fewer passes than moving does.

The mathematical toolkit escalated at every stage: from high-school algebra, to polynomial interpolation, to Fourier analysis over finite rings, to algebraic geometry over Gaussian integers, to linear codes on a network of $10^{20}$ wires. And yet -- and this is the remarkable part -- the *problem never changed*. At every stage, we are still multiplying two numbers. We are still computing the same convolution of digits, still propagating the same carries. What changed is our understanding of the *geometry* of the computation: the realization that there exist clever rearrangements of the same arithmetic operations that cancel redundancies invisible from the schoolbook perspective.

## The Floor That Was Never Proved

Is $O(n \log n)$ optimal? The first edition of this conclusion answered: "We cannot prove it is, but there are strong reasons to believe it." Half of that sentence has aged well.

Here is the complete list of what has been *proved* about the minimum time to multiply two $n$-bit integers on a multitape Turing machine: the machine has to read its input. $\Omega(n)$. Nothing more.

Everything else was conjecture or intuition. Schönhage and Strassen *proposed* $n \log n$ as the right answer in 1971; they did not prove it. The "plausible circuit-complexity arguments" this page once gestured at were hunches about mixing. The genuine $n \log n$ theorems in the neighborhood all concern restricted games:

- **on-line** multiplication, where each output digit must be committed before later input digits are seen (Paterson, Fischer and Meyer, 1974);
- Fourier transforms by linear circuits with **bounded coefficients** (Morgenstern, 1973);
- Boolean circuits, **conditionally** on an unproved conjecture about network coding (Afshani, Freksen, Kamma and Larsen, 2019).

Two of those buy their lower bound by forbidding something, and the third is on loan from a conjecture. None of them constrains ordinary, off-line multiplication on tapes.

So where is the true floor? Write $M(n)$ for the real cost of multiplying $n$-bit integers. It lies somewhere in the gap

$$
\Omega(n) \;\le\; M(n) \;\le\; O\!\left(n \,(\log n)^{1-\kappa}\right),
$$

and for now no theorem says where. It might be $n \log \log n$. It might be $n$, which is what a pointer machine already achieves. A lower bound may yet be found. What has changed is that the question no longer comes with a default answer.

## Sorting Was a Different Problem

Previously, it could have been thought that sorting and multiplication were related -- that the $n \log n$ they shared was a single barrier seen from two sides. This series did think so, at length, and [Vol. IV](/blog/2025/12/19/On-Multiplication-Vol-IV) preserves the case: the same bound, the same divide-and-conquer recurrence, the same hypercube-shaped network, with merge sort's compare-exchanges on one side and the FFT's butterflies on the other.

What that resemblance actually established is that the best *algorithms* we had for the two problems were built alike. It said nothing about the problems. Underneath, they are different in kind.

**Sorting's bound is a theorem about ignorance.** A comparison sort does not know which of $n!$ orderings it has been handed, and each comparison tells it at most one bit. So $\log_2(n!) = \Theta(n \log n)$ bits must be *learned*, and that many comparisons must be made. Two lines, airtight, settled long ago. (Note what kind of theorem it is: a statement about comparisons. Let the algorithm look inside its keys, and integer sorting drops below $n \log n$ too.)

**Multiplication's bound was a habit.** There is nothing to learn: the input is in plain sight and the output is a fixed function of it. No counting argument applies, because there is nothing to count. The $n \log n$ was the cost of one particular way of organizing the work -- $\log n$ sweeps over $n$ bits -- and it lasted exactly as long as nobody found another.

So the two are not intertwined at all. Sorting is provably $\Theta(n \log n)$ in its model. Multiplication sits somewhere between $n$ and $n (\log n)^{1-\kappa}$, with no lower bound in sight. Yet.

The specific intuition that failed deserves to be named. The first edition said that rearranging $n$ things across $\log n$ dimensions costs $n \log n$, "and not a single operation less." That is true of sealed envelopes. It is not true of bits, because bits can be *added together*. The preprint's address swap ends as a pure permutation -- every bit lands exactly where it was supposed to go -- yet in between, the tape holds XORs of data that no routing argument can follow. The paper is explicit that its procedure "lies outside models restricted to moving data." A year earlier, Harvey and van der Hoeven had proved that multiplication is at least as hard as transposing a matrix on tape, so that an $n \log n$ lower bound for transposition would have settled the conjecture. The implication now gets used in the other direction: multiplication got faster, and transposition came down with it.

## Galactic Algorithms and the Nature of Truth

We should be honest about the practical situation. Karatsuba's algorithm overtakes schoolbook multiplication at around 20-40 digits, depending on the implementation. Toom-Cook-3 wins around 100-200 digits. Schönhage-Strassen becomes competitive at tens of thousands of digits -- the scale used by modern big-integer libraries like GMP. But Harvey-van der Hoeven? Its crossover point is somewhere beyond $2^{1729^{12}}$ digits. That number has more digits than there are atoms in the observable universe. No computer that will ever exist will multiply numbers that large. The Harvey-van der Hoeven algorithm will never be *run*.

The 2026 algorithm is further out still. By its own parameter choices it does not switch on until the length of the input, written out in decimal, would overflow the universe.

And yet it matters enormously.

It matters because mathematics is not engineering. The question "what is the true complexity of integer multiplication?" is a question about the structure of arithmetic itself, not about what silicon can compute before the heat death of the universe. An algorithm -- even a galactically impractical one -- is a *proof*: a proof that the cost of multiplying is not quadratic, not $n^{1.585}$, not $n \log n \log \log n$, and now, if the preprint holds, not $n \log n$ either. An upper bound is a theorem about reality. A floor that nobody has proved is only a rumor about it.

Galactic algorithms are the astronomer's telescope pointed at the foundations of computation. We will never travel to a quasar, but knowing it exists changes our understanding of the universe. Similarly, we will never run these algorithms on actual inputs, but knowing they exist changes our understanding of what multiplication *is*. In 2019 the telescope showed what looked like the edge. In 2026 it shows more sky.

## The Punchline

Here is the thought to carry away.

Kolmogorov looked at schoolbook multiplication and saw $n^2$ -- a grid of partial products, rigid and inescapable. Karatsuba looked at the same grid and saw that some cells were redundant. Toom and Cook saw that the grid was really a polynomial, and polynomials can be evaluated at fewer points than their degree suggests. Schönhage and Strassen saw that the polynomial was really a signal, and signals can be decomposed into frequencies. Harvey and van der Hoeven saw that the signal lived in a multi-dimensional space whose geometry could be exploited to eliminate every last bit of overhead.

And then, by OpenAI's account, a machine looked at what was left -- the bare sweeps over the data, the one cost every earlier generation had filed under *unavoidable* -- and saw that even those could be shared.

Each generation looked at the *same object* -- the product of two integers -- and saw deeper structure. The number didn't change. Our eyes did. This time the eyes were not ours.

The first edition of this page ended by announcing that sorting and multiplication were the same thing all along. They are not. Sorting has a floor because somebody proved one. Multiplication has only ever had a ceiling, and for sixty-six years the ceiling has done nothing but come down: $n^2$, $n^{1.585}$, $n^{1+\varepsilon}$, $n \log n \log \log n$, $n \log n$, and now a hair below. More than one of those was mistaken for the floor. Each turned out to be a description of the best idea available at the time.

That is the correction, and it is also the lesson. $n \log n$ was never a fact about multiplication. It was a fact about 2019.

That, in the end, is what mathematics is: the systematic refinement of vision. The history of multiplication algorithms is not a story about making computers faster. It is a story about learning to see -- and about how often, just when we think we have reached the bottom, we turn out to have been looking at our own reflection.

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

**Added for Vol. V**

OpenAI, "Integer multiplication below n log n" (preprint, September 23, 2026): https://github.com/openai/math/blob/main/preprints/Integer-multiplication-below-n-log-n-September-23-2026/paper.pdf

OpenAI, "An explicit power saving for the exact discrete Fourier transform" (preprint, September 25, 2026): https://github.com/openai/math/blob/main/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/main.pdf

The OpenAI collection, with its verification notes and revision history: https://github.com/openai/math

Community improvements to the exponent, conditional on the preprint: https://github.com/CrocSwap/integer-mult-bounds

D. Harvey and J. van der Hoeven, "Integer multiplication is at least as hard as matrix transposition" (FOCS 2025): https://arxiv.org/abs/2503.22848

J. Morgenstern, "Note on a lower bound of the linear complexity of the fast Fourier transform," *Journal of the ACM* 20 (1973)

M. S. Paterson, M. J. Fischer and A. R. Meyer, "An improved overlap argument for on-line multiplication" (1974)

P. Afshani, C. B. Freksen, L. Kamma and K. G. Larsen, "Lower bounds for multiplication via network coding" (ICALP 2019)

H. Buhrman, R. Cleve, M. Koucký, B. Loff and F. Speelman, "Computing with a full memory: catalytic space" (STOC 2014)

---

*On Multiplication:* [Vol. I](/blog/2025/12/19/On-Multiplication) · [Vol. II](/blog/2025/12/19/On-Multiplication-Vol-II) · [Vol. III](/blog/2025/12/19/On-Multiplication-Vol-III) · [Vol. IV](/blog/2025/12/19/On-Multiplication-Vol-IV) · **Vol. V**
