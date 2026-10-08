---
layout: post
title: "Back-of-the-Envelope: Abel–Ruffini, Vol. II: Roots Exist"
date: 2026-08-22 12:01:00
categories: algebra
mathjax: true
---

*Abel–Ruffini:* [I](/blog/2026/08/22/Abel-Ruffini-Theorem) · **II** · [III](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-III) · [IV](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-IV) · [V](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-V) · [VI](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-VI)

*The fundamental theorem of algebra: every polynomial has its full family of roots in $\mathbb{C}$. Existence, not a formula — and the thing Vol. I's loops move around.*

# The fundamental theorem of algebra
{: #the-fundamental-theorem-of-algebra}

A **field** is a set with addition and multiplication in which you can add, subtract, multiply, and divide by anything except zero, with the usual rules. $\mathbb{Q}$, $\mathbb{R}$, and $\mathbb{C}$ are fields. A **polynomial** over a field $F$ is an expression $a_n x^n + \cdots + a_1 x + a_0$ with coefficients $a_i\in F$. Its **degree** is $n$ if $a_n\neq 0$. A **root** is a number $r$ (in some extension of $F$) with $p(r)=0$.

**Theorem (fundamental theorem of algebra).** Every non-constant polynomial $p\in\mathbb{C}[x]$ has at least one root in $\mathbb{C}$. Equivalently: $\mathbb{C}$ is **algebraically closed**. Equivalently: if $p$ has degree $n\ge 1$, then there exist $c,r_1,\ldots,r_n\in\mathbb{C}$ with

$$
p(x) = c(x-r_1)\cdots(x-r_n).
$$

The three statements are the same once you know polynomial division. Find a root $r_1$, divide by $x-r_1$, induct on degree.

This is an existence theorem. It does not produce a formula. It does not claim the roots lie in $\mathbb{Q}$, or even in $\mathbb{R}$. It does not claim they can be written by nesting radicals in the coefficients. For two centuries “the fundamental theorem of algebra” was, in practice, the *search* for such a formula. Gauss already suspected the search was the wrong problem. Abel and Ruffini proved it was.

What the rest of the argument needs from this theorem is only the family of roots. If you already accept that every non-constant polynomial has a complex root, you may skip the geometric proof below and go on to conjugate pairs.

## What we will use

Two corollaries, and nothing more from the analytic side.

**The family of roots.** Given $p$ of degree $n$, we may speak of a complete **family** $\lbrace r_1,\ldots,r_n\rbrace$ in $\mathbb{C}$. Labels are arbitrary; later we will ask which rearrangements of the labels can be realized by maps that fix the coefficients.

**Conjugate pairs.** If $p$ has *real* coefficients and $p(z)=0$, then $p(\overline{z})=0$, because conjugation $z\mapsto\overline{z}$ is a field automorphism of $\mathbb{C}$ fixing $\mathbb{R}$. Non-real roots therefore come in pairs $\lbrace z,\overline{z}\rbrace$.

We will sit the splitting field $E=\mathbb{Q}(r_1,\ldots,r_n)$ inside $\mathbb{C}$. Conjugation permutes those roots, hence sends the generating set of $E$ to itself, hence *restricts* to a field automorphism of $E$ fixing $\mathbb{Q}$. (That restriction will later be an element of the Galois group.) As a permutation of the five labeled roots it *fixes every real root* and *swaps each conjugate pair*.

A real quintic cannot have zero real roots: $x^{5}$ dominates, so $p(x)\to+\infty$ as $x\to+\infty$ and $p(x)\to-\infty$ as $x\to-\infty$, and the intermediate-value theorem supplies a real root. Combined with conjugate pairing (even number of non-real roots) and degree five, there are exactly three possibilities. Write the permutation type of conjugation in each:

- **Five real roots.** Conjugation fixes all five labels. It is the identity in $S_5$, which is not a transposition.
- **Three real roots and one conjugate pair.** Conjugation swaps those two non-real roots and fixes the three real ones. Cycle type: a single $2$-cycle. That *is* a transposition.
- **One real root and two conjugate pairs.** Conjugation swaps two pairs and fixes the real root. Cycle type: a product of two disjoint transpositions, an even permutation of order $2$ — not a $2$-cycle.

Only the middle case will later feed an $S_5$ machine (a transposition plus a $5$-cycle generate $S_5$). The other two are silent: they do not put a transposition among the coefficient-fixing symmetries of the roots. That is why $x^{5}-2$, which has one real fifth root of $2$ and two conjugate pairs among $\sqrt[5]{2}\,\zeta_5^{k}$ for $k=1,2,3,4$, slips through as solvable — conjugation on its roots is of the third type, not the second. We will compute those symmetries later; the group has order $20$, not $120$.

## A proof that does not hide the analysis (optional)

The theorem is not a theorem of algebra in the modern sense. Any proof uses some continuity. The argument below is geometric: identify $\mathbb{C}$ with the plane $\mathbb{R}^2$, view $\lvert p(z)\rvert$ as a height function over that plane, and find a closed disk on which the height is forced to dip to zero.

Write $p(z) = a_n z^n + a_{n-1}z^{n-1} + \cdots + a_0$ with $a_n\neq 0$ and $n\ge 1$. For $\lvert z\rvert$ large, the leading term dominates. Precisely: the reverse triangle inequality gives $\lvert p(z)\rvert \ge \lvert a_n z^n\rvert - \lvert p(z)-a_n z^n\rvert$, and

$$
\bigl\lvert p(z) - a_n z^n\bigr\rvert \le \bigl(\lvert a_{n-1}\rvert + \cdots + \lvert a_0\rvert\bigr)\,\lvert z\rvert^{n-1}.
$$

If $\lvert z\rvert\ge 1$ the right-hand side is at most $M\lvert z\rvert^{n-1}$ with $M=\lvert a_{n-1}\rvert+\cdots+\lvert a_0\rvert$, so $\lvert p(z)\rvert \ge \bigl(\lvert a_n\rvert - M/\lvert z\rvert\bigr)\lvert z\rvert^n$. Choose $R\ge 1$ large enough that $M/R \le \lvert a_n\rvert/2$ and also $\tfrac12\lvert a_n\rvert R^n \gt \lvert p(0)\rvert$. Then $\lvert z\rvert \ge R$ implies

$$
\lvert p(z)\rvert \ge \tfrac12 \lvert a_n\rvert\,\lvert z\rvert^n \gt \lvert p(0)\rvert.
$$

(The closed condition $\lvert z\rvert \ge R$, not just $\lvert z\rvert \gt R$, is the one we want: height already exceeds $\lvert p(0)\rvert$ on and beyond the circle of radius $R$.)

**The compact disk.** Write

$$
\overline{D}_R := \{\, z\in\mathbb{C} : \lvert z\rvert \le R \,\}
$$

for the **closed disk** of radius $R$ centered at the origin — the filled circle, boundary included. As a subset of the plane $\mathbb{R}^2$ it is closed and bounded, hence **compact** by Heine–Borel. The modulus $\lvert p\rvert : \mathbb{C}\to[0,\infty)$ is continuous (a polynomial is continuous, and $\lvert\,\cdot\,\rvert$ is continuous). A continuous real-valued function on a compact set attains its minimum: there exists $z_0\in\overline{D}_R$ with $\lvert p(z_0)\rvert \le \lvert p(z)\rvert$ for every $z\in\overline{D}_R$.

That minimum cannot live on the boundary. The origin $0$ lies in $\overline{D}_R$, so $\lvert p(z_0)\rvert \le \lvert p(0)\rvert$. But on the circle $\lvert z\rvert = R$ we already have $\lvert p(z)\rvert \gt \lvert p(0)\rvert$. Therefore $\lvert z_0\rvert \lt R$: $z_0$ is an **interior** point of the disk. The same comparison shows the disk-minimum is a minimum on all of $\mathbb{C}$: outside the disk, $\lvert p\rvert$ is already larger than $\lvert p(z_0)\rvert$. We claim $p(z_0)=0$.

The figure is this height function for the later quintic $p(z)=z^5-z-1$, with $R=1.6$. Five dark wells sit strictly inside the cyan circle; each well is a root. The real slice on the right is the same height restricted to $\overline{D}_R\cap\mathbb{R}=[-R,R]$.

<p style="text-align:center;">
  <img src="/blog/assets/2026/abel-ruffini/compact-disk.png" alt="Modulus of z^5-z-1 as a heatmap on the complex plane, with the compact disk of radius R outlined and all five roots interior" style="max-width:100%;">
</p>

Suppose not: $p(z_0)\neq 0$. Shift the putative minimum to the origin and scale it to $1$:

$$
q(z) \;=\; \frac{p(z+z_0)}{p(z_0)}.
$$

Then $q(0)=1$, and $\lvert q\rvert$ has a global minimum of $1$ at $0$. Write

$$
q(z) \;=\; 1 + b_k z^k + b_{k+1}z^{k+1} + \cdots + b_m z^m,
$$

where $k\ge 1$ is smallest with $b_k\neq 0$ — the first non-constant term. If we can produce a point at which $\lvert q\rvert<1$, the minimum is not a minimum.

The first term $b_k z^k$ can be *aimed*. We want a direction $\beta$ with $b_k\beta^k=-1$, so that walking a small real distance $t$ along $\beta$ subtracts $t^k$ from $1$ rather than rotating around it. That equation is $\beta^k=-1/b_k$: a $k$th root of a complex number. Here is the construction.

**De Moivre, and $k$th roots.**

> **De Moivre's theorem.** If $k$ is a positive integer and $\theta\in\mathbb{R}$, then
>
> $$(\cos\theta + i\sin\theta)^k \;=\; \cos(k\theta) + i\sin(k\theta).$$

The proof is induction on $k$, using the addition formulas $\cos(\theta+\varphi)=\cos\theta\cos\varphi-\sin\theta\sin\varphi$ and $\sin(\theta+\varphi)=\sin\theta\cos\varphi+\cos\theta\sin\varphi$. Those two identities are the whole of trigonometry that the argument needs.

Now take any $w\in\mathbb{C}$. Polar coordinates supply $r\ge 0$ and $\theta\in\mathbb{R}$ with $w=r(\cos\theta+i\sin\theta)$. The nonnegative real $r$ has a real $k$th root: $x\mapsto x^k$ is a continuous bijection $[0,\infty)\to[0,\infty)$, so it hits $r$ (intermediate-value theorem; uniqueness because the map is strictly increasing). De Moivre then gives

$$
\Bigl(r^{1/k}\bigl(\cos\tfrac{\theta}{k} + i\sin\tfrac{\theta}{k}\bigr)\Bigr)^k \;=\; w.
$$

Thus every complex number has a $k$th root. There are $k$ of them — replace $\theta$ by $\theta+2\pi j$ for $j=0,\ldots,k-1$; they sit equally spaced on the circle of radius $r^{1/k}$ — and we need only one. This is a statement about *points in the plane*, built from cosine, sine, and a real $k$th root of a length. It is not a radical formula in the coefficients of $p$. We will need that distinction later.

**The walk.** Let $\beta$ be a $k$th root of $-1/b_k$, so $b_k\beta^k=-1$. For $t\in(0,1)$,

$$
q(t\beta) \;=\; 1 + b_k(t\beta)^k + \sum_{j=k+1}^{m} b_j(t\beta)^j \;=\; 1 - t^k + t^{k+1}\,r(t),
$$

where $r(t)=\sum_{j=k+1}^{m} b_j t^{j-k-1}\beta^j$ is a polynomial, hence bounded on $[0,1]$: $\lvert r(t)\rvert\le C$ for some $C$. (If $q$ has no terms past $z^k$, take $C=0$.) Pick a constant $c>\max(C,1)$. The triangle inequality and $t\in(0,1)$ give

$$
\lvert q(t\beta)\rvert \;\le\; \lvert 1-t^k\rvert + t^{k+1}c \;=\; 1-t^k + c\,t^{k+1} \;=\; 1-t^k(1-ct).
$$

Take $t=1/(2c)$. Then $t\in(0,1)$ and $1-ct=\tfrac12$, so

$$
\lvert q(t\beta)\rvert \;\le\; 1-\tfrac12 t^k \;<\; 1,
$$

contradicting the assumption that the global minimum of $\lvert q\rvert$ is $1$. Hence $p(z_0)=0$.

The geometry: De Moivre aims $b_k(t\beta)^k$ *directly opposite* the constant term $1$, so the two cancel as real numbers $1-t^k$ rather than rotating around the unit circle. The leftover is one degree higher and, at $t=1/(2c)$, too small to push back outside the unit disk. A compressed writeup would hide the tail as $O(t^{k+1})$ and take $t$ small enough; the explicit $t=1/(2c)$ is the same estimate, with the constant named. (This walk is Axler's, from *Linear Algebra Done Right*, 4th ed., §4.12. The compactness that produces the minimum is the disk argument above.)

<p style="text-align:center;">
  <img src="/blog/assets/2026/abel-ruffini/de-moivre-walk.png" alt="Left: De Moivre placing the three cube roots of a complex number w equally spaced on a circle. Right: in the q-plane, the first non-constant term is aimed from 1 toward 0, and the higher-term error disk still lies inside the unit disk." style="max-width:100%;">
</p>

(If you prefer Liouville: if $p$ had no root then $1/p$ would be entire and bounded, hence constant, hence $p$ constant.)

The algebraic proofs in the literature assume two facts that themselves need the intermediate-value theorem: every real polynomial of odd degree has a real root, and every nonnegative real has a square root. From those one can show that $\mathbb{R}(i)$ is algebraically closed, which is the same theorem. We will not pretend this is a proof from the field axioms alone.

We now have a family of roots. The question is what we are allowed to *do* with them.

---

**Next:** [Vol. III: Symmetries of the Roots](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-III)

*Abel–Ruffini:* [Vol. I](/blog/2026/08/22/Abel-Ruffini-Theorem) · **Vol. II** · [Vol. III](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-III) · [Vol. IV](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-IV) · [Vol. V](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-V) · [Vol. VI](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-VI)
