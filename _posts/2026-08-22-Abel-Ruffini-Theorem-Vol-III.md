---
layout: post
title: "Back-of-the-Envelope: Abel–Ruffini, Vol. III: Symmetries of the Roots"
date: 2026-08-22 12:02:00
categories: algebra
mathjax: true
---

*Abel–Ruffini:* [I](/blog/2026/08/22/Abel-Ruffini-Theorem) · [II](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-II) · **III** · [IV](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-IV) · [V](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-V) · [VI](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-VI)

*Permutations of the labeled roots, parity, normal subgroups, and why $S_5$ cannot be peeled into commutative layers. This is the group theory Vol. I used in one line, done properly.*

# Group theory: symmetries of a labeled family
{: #group-theory-symmetries-of-a-labeled-family}

Label the roots $r_1,\ldots,r_n$. A **permutation** of the labels is a bijection $\sigma$ of the set $\{1,\ldots,n\}$. The set of all such bijections is the **symmetric group** $S_n$. There are $n!$ of them. Composition of functions is the group law: $(\sigma\tau)(i)=\sigma(\tau(i))$, done right to left. The identity $\mathrm{id}$ does nothing; every $\sigma$ has an inverse.

This is the symmetry group of a labeled family of $n$ things. Whether a *particular* polynomial admits all $n!$ rearrangements as actual symmetries of its coefficients is a later question. First we need the group, and a few words for talking about groups.

A **subgroup** of $G$ is a subset that is itself a group under the same operation (contains the identity, inverses, and products). Two elements $a,b$ **commute** if $ab=ba$; a group is **abelian** if every pair commutes. The **cyclic group** $C_n$ is the group of $n$ rotations of a regular $n$-gon, equivalently $\{\,1,g,g^2,\ldots,g^{n-1}\,\}$ with $g^n=1$; it is abelian. A **homomorphism** $\varphi:G\to H$ is a map with $\varphi(ab)=\varphi(a)\varphi(b)$. Its **kernel** is $\{\,g\in G:\varphi(g)=\mathrm{id}_H\,\}$, always a subgroup. Two groups are **isomorphic**, written $G\cong H$, if there is a bijective homomorphism between them: the same group law, relabeled. A **(left) coset** of a subgroup $H\le G$ is a translate $gH=\{\,gh:h\in H\,\}$; the distinct cosets partition $G$.

## Small pictures

$S_2=\{\mathrm{id},(1\,2)\}$. That is the quadratic: the two roots $\frac{-b\pm\sqrt{b^2-4ac}}{2a}$ are indistinguishable once you forget which sign you took. Swapping them is the only nontrivial symmetry.

$S_3$ has six elements: the identity, two $3$-cycles $(1\,2\,3)$ and $(1\,3\,2)$, and three transpositions $(1\,2)$, $(1\,3)$, $(2\,3)$. Already there is a distinction: some permutations reverse an ordering, some do not.

## Parity

Fix the usual order $1 \lt 2 \lt \cdots \lt n$. An **inversion** of $\sigma$ is a pair $i \lt j$ with $\sigma(i) \gt \sigma(j)$. The permutation is **even** or **odd** according to the parity of the number of inversions.

Equivalently — and this is the definition we will actually use — consider the Vandermonde product

$$
\Delta(x_1,\ldots,x_n) = \prod_{1\le i<j\le n}(x_i-x_j).
$$

Permuting the variables either leaves $\Delta$ alone or multiplies it by $-1$, because each factor $x_i-x_j$ is sent to $\pm$ another factor. The square $\Delta^2=\prod_{i<j}(x_i-x_j)^2$ is the **discriminant** of the (monic) polynomial with those roots: it is unchanged by every permutation, hence is a polynomial in the coefficients. For $x^2+bx+c$ it is $b^2-4c$; the schoolbook $d=b^2-4ac$ of $ax^2+bx+c$ is $a^2$ times that quantity. We will need the name again when a prime is required not to divide the discriminant. Define

$$
\mathrm{sgn}(\sigma) := \frac{\Delta(x_{\sigma(1)},\ldots,x_{\sigma(n)})}{\Delta(x_1,\ldots,x_n)}\in\{+1,-1\}.
$$

This is a **homomorphism** $S_n\to\{+1,-1\}$: $\mathrm{sgn}(\sigma\tau)=\mathrm{sgn}(\sigma)\,\mathrm{sgn}(\tau)$. A transposition sends $\Delta$ to $-\Delta$, so $\mathrm{sgn}$ of a transposition is $-1$. (An *adjacent* transposition flips exactly one factor; a non-adjacent one, such as $(1\,3)$ in $S_4$, flips an odd number of factors. Either way the overall sign is $-1$.) Therefore $\mathrm{sgn}(\sigma)=(-1)^m$ whenever $\sigma$ is a product of $m$ transpositions. The number $m$ is not unique, but its *parity* is. See [parity of a permutation](https://en.wikipedia.org/wiki/Parity_of_a_permutation) for the inversion-count, adjacent-transposition, and cycle-index proofs that these notions coincide.

The even permutations form a subgroup, the **alternating group** $A_n=\ker\mathrm{sgn}$ — exactly the permutations sent to $+1$. It has index $2$ in $S_n$ (two cosets, even and odd), hence order $n!/2$ for $n\ge 2$. The odd permutations are the other coset $A_n\cdot(1\,2)$; they do not form a subgroup, because odd times odd is even.

A $k$-cycle $(a_1\,a_2\,\cdots\,a_k)$ is a product of $k-1$ transpositions, for instance

$$
(a_1\,a_2\,\cdots\,a_k) = (a_1\,a_k)(a_1\,a_{k-1})\cdots(a_1\,a_2).
$$

So a $k$-cycle is even if and only if $k$ is odd: $3$-cycles are even, transpositions are odd, $5$-cycles are even. In a disjoint-cycle decomposition (including $1$-cycles if you like), the permutation is odd if and only if the number of even-length cycles is odd.

**Conjugating a cycle relabels its entries.** If $\sigma=(a_1\,a_2\,\cdots\,a_k)$ and $\tau$ is any permutation, then

$$
\tau\sigma\tau^{-1} = \bigl(\tau(a_1)\,\tau(a_2)\,\cdots\,\tau(a_k)\bigr).
$$

The same rule applies factorwise to a product of disjoint cycles. This is the one computation used below to move $3$-cycles around $A_n$, to produce commutators in the simplicity argument, and to turn a $p$-cycle and a transposition into all adjacent transpositions.

## Normal subgroups and quotients

A subgroup $N\le G$ is **normal**, written $N\trianglelefteq G$, if $gNg^{-1}=N$ for every $g\in G$. Equivalently, left and right cosets coincide, and the set of cosets $G/N$ inherits a group law. Normality is what lets a symmetry group be *peeled into layers*: the quotient $G/N$ is the residual symmetry after the layer $N$ has been accounted for. The kernel of any homomorphism is normal; $A_n\trianglelefteq S_n$ is the kernel of $\mathrm{sgn}$, and $S_n/A_n\cong C_2$, the cyclic group of order $2$.

For $n\ge 5$ (in fact $n\neq 6$), $A_n$ is the *only* nontrivial proper normal subgroup of $S_n$. We will need a piece of that: $A_n$ itself, for $n\ge 5$, has *no* nontrivial proper normal subgroups. Such a group is called **simple**. $A_5$ is the smallest non-abelian simple group.

## Why simplicity matters

If a group is **simple**, it has no nontrivial proper normal subgroup, so it cannot be peeled into a smaller layer plus a quotient. Solvable groups are built from abelian pieces. A simple non-abelian group therefore cannot appear in a solvable series except as a dead end: you cannot start a stack of abelian quotients with it. That is why $A_5$ kills solvability of $S_5$: the only normal series of $S_5$ is $\{1\}\trianglelefteq A_5\trianglelefteq S_5$, and the factor $A_5$ is not abelian.

Contrast $S_4$, which *can* be peeled: $\{1\}\trianglelefteq V_4\trianglelefteq A_4\trianglelefteq S_4$, with abelian (in fact cyclic, after one refinement) quotients.

<p style="text-align:center;">
  <img src="/blog/assets/2026/abel-ruffini/lattice-s4-s5.png" alt="Solvable chain of S4 versus the dead-end chain of S5 through A5" style="max-width:100%;">
</p>

## $A_5$ is simple

The calculation below establishes that $A_5$ has no nontrivial proper normal subgroups. Its role in the main argument is only the paragraph above: $A_5$ cannot be part of a solvable chain. Three facts.

**(i) $A_n$ is generated by $3$-cycles**, for $n\ge 3$. A $3$-cycle is even, so lies in $A_n$. Conversely every even permutation is a product of an even number of transpositions, and

$$
(a\,b)(a\,c) = (a\,c\,b), \qquad (a\,b)(c\,d) = (a\,c\,b)(a\,c\,d)
$$

when $\{a,b\}\cap\{c,d\}=\emptyset$. So products of two transpositions are products of $3$-cycles.

**(ii) All $3$-cycles are conjugate in $A_n$ for $n\ge 5$.** In $S_n$, any two $3$-cycles are conjugate: if $\sigma=(1\,2\,3)$ then $\tau\sigma\tau^{-1}=(\tau(1)\,\tau(2)\,\tau(3))$. For $n\ge 5$ there are two unused letters, say $4$ and $5$. If the conjugating $\tau$ is odd, replace it by $\tau'=\tau\cdot(4\,5)$. Then $\tau'$ is even, so lies in $A_n$, and $\tau'\sigma(\tau')^{-1}=\tau\sigma\tau^{-1}$ because $(4\,5)$ does not meet $\{1,2,3\}$. Thus conjugacy of $3$-cycles still happens *inside* $A_n$.

**(iii) Any nontrivial normal subgroup $N\trianglelefteq A_n$ ($n\ge 5$) contains a $3$-cycle.** Take $\sigma\in N$, $\sigma\neq\mathrm{id}$. Because $N$ is normal, every $A_n$-conjugate of $\sigma$ is in $N$, and so is every commutator $\tau\sigma\tau^{-1}\sigma^{-1}$. The even cycle types that can occur in $A_5$ are $3$-cycles, products of two disjoint transpositions, and $5$-cycles. The first is already a $3$-cycle. The other two are handled by an explicit conjugation:

- *A product of two disjoint transpositions*, say $\sigma=(1\,2)(3\,4)$. (Even, so it can live in $A_n$.) For $n\ge 5$ there is a fifth letter. Conjugate by $\tau=(3\,4\,5)$:

  $$
  \tau\sigma\tau^{-1} = (1\,2)(4\,5).
  $$

  Then $\sigma\cdot(\tau\sigma\tau^{-1})=(1\,2)(3\,4)(1\,2)(4\,5)=(3\,4\,5)$, a $3$-cycle in $N$.
- *A $5$-cycle*, say $\sigma=(1\,2\,3\,4\,5)$. Let $\tau=(1\,2\,3)$. Conjugation by $\tau$ sends each letter $i$ in the cycle to $\tau(i)$, so $\tau\sigma\tau^{-1}=(2\,3\,1\,4\,5)$. The commutator, composing right to left, is the $3$-cycle $(1\,2\,4)$:

  $$
  \tau\sigma\tau^{-1}\sigma^{-1} = (1\,2\,3)(1\,2\,3\,4\,5)(1\,3\,2)(1\,5\,4\,3\,2) = (1\,2\,4).
  $$

  Track a letter if you want the arithmetic: $1\mapsto 2\mapsto 3\mapsto 1\mapsto 2$, then continue for $2,3,4,5$. (The same identity, unused letters fixed, works in $A_n$ for $n \gt 5$.)

Once $N$ contains *one* $3$-cycle, conjugacy (ii) puts *every* $3$-cycle in $N$, and generation (i) forces $N=A_n$. That is the whole of simplicity: a nontrivial normal subgroup cannot be proper.

Thus $A_5$ is simple. It is non-abelian: $(1\,2\,3)(3\,4\,5)\neq (3\,4\,5)(1\,2\,3)$. Therefore $A_5$ admits no chain of subgroups down to $\{1\}$ with abelian successive quotients, except the trivial two-step $\{1\}\trianglelefteq A_5$ whose quotient is not abelian. The same argument, with the extra room of unused letters, shows $A_n$ is simple for all $n\ge 5$.

## Solvable groups

<div class="note">
<p><strong>Solvable group.</strong> A finite group $G$ that admits a chain $\{1\}=G_0\trianglelefteq\cdots\trianglelefteq G_k=G$ with each quotient $G_{i+1}/G_i$ abelian. Built from commutative layers; the name of the constraint that radical formulas impose on symmetry.</p>
</div>

A finite group $G$ is **solvable** if there is a chain

$$
\{1\} = G_0 \trianglelefteq G_1 \trianglelefteq \cdots \trianglelefteq G_k = G
$$

in which each quotient $G_{i+1}/G_i$ is abelian. (For finite groups one may equivalently demand that the quotients be cyclic: a finite abelian group is a product of cyclics, and one can refine the chain.)

The picture is a stack of commutative layers. Each radical step $F(\sqrt[n]{a})/F$, once the $n$th roots of unity are present, has cyclic Galois group — one commutative layer. A nested-radical formula is a finite stack of such layers, so the Galois group of a polynomial solvable by radicals must be a group that *can be built by stacking abelian pieces*. That is the name. $S_3$ can (cyclic of order $3$, then $C_2$). $A_5$ cannot: it has no nontrivial abelian normal subgroup to start the stack.

**$S_2$, $S_3$, $S_4$ are solvable.**

- $S_2\cong C_2$, already abelian.
- $\{1\}\trianglelefteq A_3 \trianglelefteq S_3$ with quotients $C_3$ and $C_2$. Here $A_3=\langle(1\,2\,3)\rangle$.
- $\{1\}\trianglelefteq V_4 \trianglelefteq A_4 \trianglelefteq S_4$, where $V_4=\{\mathrm{id},(1\,2)(3\,4),(1\,3)(2\,4),(1\,4)(2\,3)\}$ is the Klein four-group, abelian of order $4$. Quotients: $C_2\times C_2$, $C_3$, $C_2$.

$V_4$ is normal in $S_4$ because conjugation preserves cycle type, and the three non-identity elements of $V_4$ are *all* the products of two disjoint transpositions in $S_4$. So $S_4$ permutes those three elements among themselves and leaves $V_4$ invariant. The quotient $A_4/V_4$ has order $3$, hence is cyclic. This is the group-theoretic shadow of Ferrari’s method: the resolvent cubic of a quartic is the quotient $S_4\to S_3\cong S_4/V_4$, and solving that cubic (solvable, because $S_3$ is) is the step that reduces a quartic to nested quadratics.

**$S_n$ is not solvable for $n\ge 5$.** Two facts, connected. First: for $n\neq 6$, $A_n$ is the unique nontrivial proper normal subgroup of $S_n$ (it is $\ker\mathrm{sgn}$, index $2$). So any normal series from $\{1\}$ up to $S_n$ has $A_n$ as its last proper term: $\{1\}\trianglelefteq\cdots\trianglelefteq A_n\trianglelefteq S_n$. Second: $A_n$ is simple and non-abelian, so the stretch $\{1\}\trianglelefteq\cdots\trianglelefteq A_n$ cannot be refined into abelian quotients — the only possibilities are to skip $A_n$ (impossible, by uniqueness) or to leave the non-abelian factor $A_n$ in the series. There is no analogue of $V_4$ sitting normally inside $A_5$. That is the group-theoretic half of Abel–Ruffini, stated before we have fields. The rest of the series ([Vol. IV](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-IV) through [Vol. VI](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-VI)) is the identification: a radical formula produces a solvable group of symmetries of the root family, and the general quintic’s group is $S_5$. Then $S_5$ is too big.

One more computational fact, used twice below.

**Lemma (adjacent transpositions generate $S_n$).** The transpositions $(1\,2),(2\,3),\ldots,(n-1\,n)$ generate $S_n$. Any transposition $(i\,j)$ with $j \gt i+1$ is a conjugate of an adjacent one:

$$
(i\,j) = (j-1\,j)\,(i\,j-1)\,(j-1\,j),
$$

and inducting on $j-i$ writes $(i\,j)$ in the adjacent generators. Every permutation is a product of (not necessarily adjacent) transpositions, so the adjacent ones suffice. Equivalently: a $p$-cycle $(1\,2\,\cdots\,p)$ together with the transposition $(1\,2)$ generate $S_p$, because conjugating the transposition by powers of the cycle produces every adjacent transposition.

---

**Next:** [Vol. IV: Where the Roots Live](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-IV)

*Abel–Ruffini:* [Vol. I](/blog/2026/08/22/Abel-Ruffini-Theorem) · [Vol. II](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-II) · **Vol. III** · [Vol. IV](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-IV) · [Vol. V](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-V) · [Vol. VI](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-VI)
