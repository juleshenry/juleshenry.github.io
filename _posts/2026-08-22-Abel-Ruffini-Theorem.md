---
layout: post
title: "Abel–Ruffini Theorem"
date: 2026-08-22
categories: algebra
mathjax: true
---

The quadratic formula is older than the word *algebra*. The cubic and the quartic were trophies of the sixteenth century. Then the formulae stop. Every generation of students is told that “the quintic has no formula,” which is both true and badly put. Quintics have roots. The [fundamental theorem of algebra](https://en.wikipedia.org/wiki/Fundamental_theorem_of_algebra) says so: a degree-five polynomial has five roots in $\mathbb{C}$, counted with multiplicity. What fails is not existence. What fails is a *uniform expression* for those roots in the coefficients, built from finitely many additions, subtractions, multiplications, divisions, and nested $n$th roots.

That is the [Abel–Ruffini theorem](https://en.wikipedia.org/wiki/Abel%E2%80%93Ruffini_theorem). The obstruction is not that five is a large number. It is that the family of roots of a general quintic admits more rearrangements than a tower of radicals can manufacture. The rest of this note is the walk from “roots exist” to “this symmetry is too large.”

If you are happy with polynomials over $\mathbb{Q}$, with $\mathbb{C}$ as a place roots can sit, and with the quadratic formula as a thing that *means* something, you are the intended reader. Groups, fields, and Galois groups are defined when they appear.

- [The fundamental theorem of algebra](#the-fundamental-theorem-of-algebra)
- [Group theory: symmetries of a labeled family](#group-theory-symmetries-of-a-labeled-family)
- [Field extensions: where the family lives](#field-extensions-where-the-family-lives)
- [Degree, and automorphisms of the home of the roots](#degree-and-automorphisms-of-the-home-of-the-roots)
- [The tower theorem](#the-tower-theorem)
- [Quintic symmetry](#quintic-symmetry)
- [History, scope, references](#history-scope-references)

---

# The fundamental theorem of algebra
{: #the-fundamental-theorem-of-algebra}

A **field** is a set with addition and multiplication in which you can add, subtract, multiply, and divide by anything except zero, with the usual rules. $\mathbb{Q}$, $\mathbb{R}$, and $\mathbb{C}$ are fields. A **polynomial** over a field $F$ is an expression $a_n x^n + \cdots + a_1 x + a_0$ with coefficients $a_i\in F$. Its **degree** is $n$ if $a_n\neq 0$. A **root** is a number $r$ (in some extension of $F$) with $p(r)=0$.

**Theorem (fundamental theorem of algebra).** Every non-constant polynomial $p\in\mathbb{C}[x]$ has at least one root in $\mathbb{C}$. Equivalently: $\mathbb{C}$ is **algebraically closed**. Equivalently: if $p$ has degree $n\ge 1$, then there exist $c,r_1,\ldots,r_n\in\mathbb{C}$ with

$$
p(x) = c(x-r_1)\cdots(x-r_n).
$$

The three statements are the same once you know polynomial division. Find a root $r_1$, divide by $x-r_1$, induct on degree.

This is an existence theorem. It does not produce a formula. It does not claim the roots lie in $\mathbb{Q}$, or even in $\mathbb{R}$. It does not claim they can be written by nesting radicals in the coefficients. For two centuries “the fundamental theorem of algebra” was, in practice, the *search* for such a formula. Gauss already suspected the search was the wrong problem. Abel and Ruffini proved it was.

## What we will use

Two corollaries, and nothing more from the analytic side.

**The family of roots.** Given $p$ of degree $n$, we may speak of a complete **family** $\{r_1,\ldots,r_n\}$ in $\mathbb{C}$. Labels are arbitrary; later we will ask which rearrangements of the labels can be realized by maps that fix the coefficients.

**Conjugate pairs.** If $p$ has *real* coefficients and $p(z)=0$, then $p(\overline{z})=0$, because conjugation is a field automorphism of $\mathbb{C}$ fixing $\mathbb{R}$. Non-real roots come in pairs. For a quintic with real coefficients, the number of non-real roots is even: $0$, $2$, or $4$. Equivalently, over $\mathbb{R}$ a quintic factors into linears and quadratics, and the number of irreducible quadratic factors is $0$, $1$, or $2$. The case of exactly one irreducible quadratic factor — exactly two non-real roots — will be a weapon: conjugation, restricted to the splitting field, becomes a transposition of those two roots.

A real quintic always has at least one real root, by the intermediate-value theorem ($x^5$ dominates, so $p(x)\to\pm\infty$ as $x\to\pm\infty$). That is the odd-degree case of the FTA’s real half, and it is why a real quintic cannot have zero real roots. The remaining possibilities are five real roots, or three real and two conjugate, or one real and two conjugate pairs. Only the middle possibility supplies a transposition from conjugation. The other two are silent about transpositions, which is why $x^5-2$ (one real root) slips through as solvable.

## A proof that does not hide the analysis

The theorem is not a theorem of algebra in the modern sense. Any proof uses some continuity. Here is one that uses as little as possible: polynomials grow at infinity, $\lvert p\rvert$ attains a minimum, and that minimum cannot be positive.

Write $p(z) = a_n z^n + a_{n-1}z^{n-1} + \cdots + a_0$ with $a_n\neq 0$ and $n\ge 1$. For $\lvert z\rvert$ large, the leading term dominates:

$$
\bigl\lvert p(z) - a_n z^n\bigr\rvert \le \bigl(\lvert a_{n-1}\rvert + \cdots + \lvert a_0\rvert\bigr)\,\lvert z\rvert^{n-1},
$$

so there is $R \gt 0$ such that $\lvert z\rvert \gt R$ implies $\lvert p(z)\rvert \ge \tfrac12 \lvert a_n\rvert\,\lvert z\rvert^n \gt \lvert p(0)\rvert$, say. On the compact disk $\lvert z\rvert\le R$, the continuous function $\lvert p\rvert$ attains a minimum at some $z_0$. The inequality just written forces $\lvert z_0\rvert \lt R$, so $z_0$ is interior. We claim $p(z_0)=0$.

Suppose not: $p(z_0)=a\neq 0$. Expand around $z_0$,

$$
p(z_0+w) = a + c_k w^k + c_{k+1}w^{k+1} + \cdots + c_n w^n,
$$

with $c_k\neq 0$ and $k\ge 1$. Choose a $k$th root of $-a/c_k$, call it $u$, so $c_k u^k = -a$. For small positive $t$, set $w=tu$. Then

$$
p(z_0+tu) = a(1-t^k) + O(t^{k+1}).
$$

For $t$ small enough, $\lvert p(z_0+tu)\rvert \lt \lvert a\rvert = \lvert p(z_0)\rvert$, contradicting minimality. Hence $p(z_0)=0$.

(If you prefer Liouville: if $p$ had no root then $1/p$ would be entire and bounded, hence constant, hence $p$ constant.)

The algebraic proofs in the literature assume two facts that themselves need the intermediate-value theorem: every real polynomial of odd degree has a real root, and every nonnegative real has a square root. From those one can show that $\mathbb{R}(i)$ is algebraically closed, which is the same theorem. We will not pretend this is a proof from the field axioms alone.

We now have a family of roots. The question is what we are allowed to *do* with them.

---

# Group theory: symmetries of a labeled family
{: #group-theory-symmetries-of-a-labeled-family}

Label the roots $r_1,\ldots,r_n$. A **permutation** of the labels is a bijection $\sigma:\{1,\ldots,n\}\to\{1,\ldots,n\}$. The set of all such bijections is the **symmetric group** $S_n$. There are $n!$ of them. Composition of functions is the group law: $(\sigma\tau)(i)=\sigma(\tau(i))$. The identity $\mathrm{id}$ does nothing; every $\sigma$ has an inverse.

This is the symmetry group of a labeled family of $n$ things. Whether a *particular* polynomial admits all $n!$ rearrangements as actual symmetries of its coefficients is a later question. First we need the group.

## Small pictures

$S_2=\{\mathrm{id},(1\,2)\}$. That is the quadratic: the two roots $\frac{-b\pm\sqrt{b^2-4ac}}{2a}$ are indistinguishable once you forget which sign you took. Swapping them is the only nontrivial symmetry.

$S_3$ has six elements: the identity, two $3$-cycles $(1\,2\,3)$ and $(1\,3\,2)$, and three transpositions $(1\,2)$, $(1\,3)$, $(2\,3)$. You can check the relations by hand. Already there is a distinction: some permutations reverse an ordering, some do not.

## Parity

Fix the usual order $1 \lt 2 \lt \cdots \lt n$. An **inversion** of $\sigma$ is a pair $i \lt j$ with $\sigma(i) \gt \sigma(j)$. The permutation is **even** or **odd** according to the parity of the number of inversions.

Equivalently — and this is the definition we will actually use — consider the Vandermonde product

$$
\Delta(x_1,\ldots,x_n) = \prod_{1\le i<j\le n}(x_i-x_j).
$$

Permuting the variables either leaves $\Delta$ alone or multiplies it by $-1$, because each factor $x_i-x_j$ is sent to $\pm$ another factor. Define

$$
\mathrm{sgn}(\sigma) := \frac{\Delta(x_{\sigma(1)},\ldots,x_{\sigma(n)})}{\Delta(x_1,\ldots,x_n)}\in\{+1,-1\}.
$$

This is a **homomorphism** $S_n\to\{+1,-1\}$: $\mathrm{sgn}(\sigma\tau)=\mathrm{sgn}(\sigma)\,\mathrm{sgn}(\tau)$. A transposition of two letters sends exactly one factor $x_i-x_j$ to its negative (and reorders the others without further signs that survive), so $\mathrm{sgn}$ of a transposition is $-1$. Therefore $\mathrm{sgn}(\sigma)=(-1)^m$ whenever $\sigma$ is a product of $m$ transpositions. The number $m$ is not unique, but its *parity* is: that is what $\mathrm{sgn}$ records. See [parity of a permutation](https://en.wikipedia.org/wiki/Parity_of_a_permutation) for the inversion-count, adjacent-transposition, and cycle-index proofs that these notions coincide.

The even permutations form a subgroup, the **alternating group** $A_n=\ker\mathrm{sgn}$. It has index $2$ in $S_n$, hence order $n!/2$ for $n\ge 2$. The odd permutations are the other coset; they do not form a subgroup, because odd times odd is even.

A $k$-cycle $(a_1\,a_2\,\cdots\,a_k)$ is a product of $k-1$ transpositions, for instance

$$
(a_1\,a_2\,\cdots\,a_k) = (a_1\,a_k)(a_1\,a_{k-1})\cdots(a_1\,a_2).
$$

So a $k$-cycle is even if and only if $k$ is odd: $3$-cycles are even, transpositions are odd, $5$-cycles are even. In a disjoint-cycle decomposition (including $1$-cycles if you like), the permutation is odd if and only if the number of even-length cycles is odd.

## Normal subgroups and quotients

A subgroup $N\le G$ is **normal**, written $N\trianglelefteq G$, if $gNg^{-1}=N$ for every $g\in G$. Equivalently, left and right cosets coincide, and the set of cosets $G/N$ inherits a group law. The kernel of any homomorphism is normal; $A_n\trianglelefteq S_n$ is the kernel of $\mathrm{sgn}$, and $S_n/A_n\cong C_2$, the cyclic group of order $2$.

For $n\ge 5$ (in fact $n\neq 6$), $A_n$ is the *only* nontrivial proper normal subgroup of $S_n$. We will need a piece of that: $A_n$ itself, for $n\ge 5$, has *no* nontrivial proper normal subgroups. Such a group is called **simple**. $A_5$ is the smallest non-abelian simple group.

## $A_5$ is simple (the sketch we need)

Three facts.

**(i) $A_n$ is generated by $3$-cycles**, for $n\ge 3$. A $3$-cycle is even, so lies in $A_n$. Conversely every even permutation is a product of an even number of transpositions, and

$$
(a\,b)(a\,c) = (a\,c\,b), \qquad (a\,b)(c\,d) = (a\,c\,b)(a\,c\,d)
$$

when $\{a,b\}\cap\{c,d\}=\emptyset$. So products of two transpositions are products of $3$-cycles.

**(ii) All $3$-cycles are conjugate in $A_n$ for $n\ge 5$.** In $S_n$ all $3$-cycles are conjugate. For $n\ge 5$ one can adjust the conjugating permutation by an extra transposition on the two unused letters, to land in $A_n$, without changing the conjugate.

**(iii) Any nontrivial normal subgroup $N\trianglelefteq A_n$ ($n\ge 5$) contains a $3$-cycle.** Take $\sigma\in N$, $\sigma\neq\mathrm{id}$. Because $N$ is normal, every conjugate of $\sigma$ by an even permutation is again in $N$, and so is every commutator $\tau\sigma\tau^{-1}\sigma^{-1}$ with $\tau\in A_n$. The cycle type of $\sigma$ is one of a short list, and each list item produces a $3$-cycle as follows.

If $\sigma$ moves at least three letters in a way that is not a $3$-cycle already, the usual trick is to conjugate by a $3$-cycle supported on three of those letters so that $\sigma$ and its conjugate fail to commute, and the commutator is a $3$-cycle. Two types need a line of their own.

- *A product of two disjoint transpositions*, say $\sigma=(1\,2)(3\,4)$. (This is even, so it can live in $A_n$.) For $n\ge 5$ there is a fifth letter. Conjugating by $(3\,4\,5)$ gives $(1\,2)(4\,5)$, and the product of $\sigma$ with that conjugate is $(3\,4\,5)$, a $3$-cycle in $N$.
- *A $5$-cycle*, say $\sigma=(1\,2\,3\,4\,5)$. Then $\sigma^2=(1\,3\,5\,2\,4)$ is also a $5$-cycle. Conjugating $\sigma$ by $(1\,2\,3)$ and forming a commutator produces a $3$-cycle; explicitly, in $A_5$,

  $$
  (1\,2\,3)\,\sigma\,(1\,2\,3)^{-1}\,\sigma^{-1} = (1\,2\,3)(1\,2\,3\,4\,5)(1\,3\,2)(1\,5\,4\,3\,2) = (1\,2\,4).
  $$

  (The same identity, with extra letters fixed, works in $A_n$ for $n \gt 5$.)

Once $N$ contains one $3$-cycle, it contains all of them by (ii), hence $N=A_n$ by (i).

Thus $A_5$ is simple. It is non-abelian: $(1\,2\,3)(3\,4\,5)\neq (3\,4\,5)(1\,2\,3)$. Therefore $A_5$ admits no chain of subgroups down to $\{1\}$ with abelian successive quotients, except the trivial two-step $\{1\}\trianglelefteq A_5$ whose quotient is not abelian. The same argument, with the extra room of unused letters, shows $A_n$ is simple for all $n\ge 5$.

## Solvable groups

A finite group $G$ is **solvable** if there is a chain

$$
\{1\} = G_0 \trianglelefteq G_1 \trianglelefteq \cdots \trianglelefteq G_k = G
$$

in which each quotient $G_{i+1}/G_i$ is abelian. (For finite groups one may equivalently demand that the quotients be cyclic: a finite abelian group is a product of cyclics, and one can refine the chain.) The name will justify itself when radicals appear. For now it is a constraint on how a group can be assembled from commutative pieces.

**$S_2$, $S_3$, $S_4$ are solvable.**

- $S_2\cong C_2$, already abelian.
- $\{1\}\trianglelefteq A_3 \trianglelefteq S_3$ with quotients $C_3$ and $C_2$. Here $A_3=\langle(1\,2\,3)\rangle$.
- $\{1\}\trianglelefteq V_4 \trianglelefteq A_4 \trianglelefteq S_4$, where $V_4=\{\mathrm{id},(1\,2)(3\,4),(1\,3)(2\,4),(1\,4)(2\,3)\}$ is the Klein four-group, abelian of order $4$. Quotients: $C_2\times C_2$, $C_3$, $C_2$.

$V_4$ is normal in $S_4$ because conjugation preserves cycle type, and the three non-identity elements of $V_4$ are *all* the products of two disjoint transpositions in $S_4$. So $S_4$ permutes those three elements among themselves and leaves $V_4$ invariant. The quotient $A_4/V_4$ has order $3$, hence is cyclic. This is the group-theoretic shadow of Ferrari’s method: the resolvent cubic of a quartic is the quotient $S_4\to S_3\cong S_4/V_4$, and solving that cubic (solvable, because $S_3$ is) is the step that reduces a quartic to nested quadratics.

**$S_n$ is not solvable for $n\ge 5$.** Any normal series of $S_n$ must pass through $A_n$: it is the unique subgroup of index $2$, kernel of $\mathrm{sgn}$, and for $n\neq 6$ the unique nontrivial proper normal subgroup of $S_n$. The factor $A_n$ is not abelian, and $A_n$ itself, being simple and non-abelian, cannot be broken into abelian quotients. There is no analogue of $V_4$ sitting normally inside $A_5$. That is the group-theoretic half of Abel–Ruffini, stated before we have fields. The rest of the note is the identification: a radical formula produces a solvable group of symmetries of the root family, and the general quintic’s group is $S_5$. Then $S_5$ is too big.

One more computational fact, used twice below.

**Lemma (adjacent transpositions generate $S_n$).** The transpositions $(1\,2),(2\,3),\ldots,(n-1\,n)$ generate $S_n$. Any transposition $(i\,j)$ with $j \gt i+1$ is a conjugate of an adjacent one:

$$
(i\,j) = (j-1\,j)\,(i\,j-1)\,(j-1\,j),
$$

and inducting on $j-i$ writes $(i\,j)$ in the adjacent generators. Every permutation is a product of (not necessarily adjacent) transpositions, so the adjacent ones suffice. Equivalently: a $p$-cycle $(1\,2\,\cdots\,p)$ together with the transposition $(1\,2)$ generate $S_p$, because conjugating the transposition by powers of the cycle produces every adjacent transposition.

---

# Field extensions: where the family lives
{: #field-extensions-where-the-family-lives}

The FTA placed the family $\{r_1,\ldots,r_n\}$ in $\mathbb{C}$. The coefficients may live in a much smaller field — classically $\mathbb{Q}$. The roots need not.

Take $x^2-2\in\mathbb{Q}[x]$. It is irreducible over $\mathbb{Q}$ (if $\sqrt{2}=p/q$ in lowest terms then $p^2=2q^2$, so $2$ divides $p$ and then $q$, contradiction). The family is $\{\sqrt{2},-\sqrt{2}\}$. Neither root is rational. Both live in the smallest field that contains $\mathbb{Q}$ and $\sqrt{2}$.

## Adjoining one element

If $F$ is a field and $\alpha$ lives in some bigger field, write $F(\alpha)$ for the **smallest field containing $F$ and $\alpha$**. Concretely, if $\alpha$ is algebraic over $F$ — if it satisfies a polynomial with coefficients in $F$ — there is a unique monic polynomial of least degree with this property, the **minimal polynomial** $m_{\alpha,F}$. Then

$$
F(\alpha) = \{ c_0 + c_1\alpha + \cdots + c_{d-1}\alpha^{d-1} : c_i\in F \},
$$

where $d=\deg m_{\alpha,F}$, with multiplication reduced using $m_{\alpha,F}(\alpha)=0$. In particular $F(\alpha)$ is a $d$-dimensional vector space over $F$, with basis $\{1,\alpha,\ldots,\alpha^{d-1}\}$.

For $\alpha=\sqrt{2}$ over $\mathbb{Q}$, the minimal polynomial is $x^2-2$, and $\mathbb{Q}(\sqrt{2})=\{a+b\sqrt{2}:a,b\in\mathbb{Q}\}$ with basis $\{1,\sqrt{2}\}$. The family of roots of $x^2-2$ *already lives entirely in this field*: $-\sqrt{2}$ is just $-1\cdot\sqrt{2}$.

## Splitting fields: the home of the whole family

Adjoining one root is not always enough.

**Definition.** A **splitting field** of $f\in F[x]$ over $F$ is an extension $E/F$ in which $f$ factors as a product of linear terms, and which is generated over $F$ by the roots of $f$. Equivalently: the smallest extension of $F$ containing the *entire family* of roots.

Existence: adjoin one root of an irreducible factor, repeat. Uniqueness up to an isomorphism fixing $F$: any two splitting fields are $F$-isomorphic. We work throughout with a splitting field sitting inside $\mathbb{C}$, which the FTA permits.

**Example: $x^2-2$ over $\mathbb{Q}$.** Splitting field $\mathbb{Q}(\sqrt{2})$. The family lives there.

**Example: $x^3-2$ over $\mathbb{Q}$.** The real cube root $\sqrt[3]{2}$ generates $\mathbb{Q}(\sqrt[3]{2})\subset\mathbb{R}$. That field contains *one* root of $x^3-2$. The other two are $\sqrt[3]{2}\,\zeta_3$ and $\sqrt[3]{2}\,\zeta_3^2$, where $\zeta_3=e^{2\pi i/3}=-\frac12+i\frac{\sqrt{3}}{2}$ is a primitive cube root of unity. They are not real. So $\mathbb{Q}(\sqrt[3]{2})$ is *not* a splitting field. The splitting field is $\mathbb{Q}(\sqrt[3]{2},\zeta_3)$. The family of three roots lives there and nowhere smaller.

This is the standing picture: coefficients in a base field $F$; family of roots in $\mathbb{C}$; splitting field $E=F(r_1,\ldots,r_n)$ the smallest house that holds them all.

## Nested radicals are a special kind of house

The quadratic formula is already a radical tower, and it is worth writing it that way so the later obstruction has something to obstruct. For $ax^2+bx+c$ with $a\neq 0$, set $F=\mathbb{Q}(a,b,c)$ (or $\mathbb{Q}$, if $a,b,c\in\mathbb{Q}$). The discriminant $d=b^2-4ac$ lives in $F$. The tower is

$$
F \subset F(\sqrt{d}),
$$

a single square-root step of degree $1$ or $2$, and both roots $\frac{-b\pm\sqrt{d}}{2a}$ live in the top field. The family $\{\sqrt{d},-\sqrt{d}\}$ is swapped by the unique nontrivial automorphism, which is why the two choices of sign in the formula are not a defect: they are the Galois group.

A **pure radical extension** of $F$ is $F(\sqrt[n]{a})$ for some $a\in F$ and $n\ge 2$: adjoin a root of $x^n-a$. A **radical tower** (a **solution in radicals**) over $F$ is a finite chain

$$
F = F_0 \subset F_1 \subset \cdots \subset F_k
$$

in which each $F_{i+1}=F_i(\alpha_i)$ with $\alpha_i^{n_i}\in F_i$ for some $n_i\ge 2$. Nested radicals are exactly this: $\sqrt{2+\sqrt{2}}$ lives in the tower $\mathbb{Q}\subset\mathbb{Q}(\sqrt{2})\subset\mathbb{Q}(\sqrt{2+\sqrt{2}})$. Cardano’s formula for a cubic is a (messy) tower of square roots and cube roots. Ferrari’s formula for a quartic is a longer such tower.

**Definition.** A polynomial $f\in F[x]$ is **solvable by radicals** over $F$ if there is a radical tower over $F$ whose top field contains a splitting field of $f$ — equivalently, contains the whole family of roots.

That is what “algebraic solution” meant to Abel. Not: the roots exist in $\mathbb{C}$. Not: they can be approximated. The roots can be *written* by starting from the coefficients and repeatedly extracting $n$th roots.

Two warnings, both classical.

First: adjoining *one* $n$th root is not the same as adjoining *all* of them. As with $x^3-2$, the real cube root of $2$ does not split $x^3-2$. A careful theory of radical towers inserts roots of unity when needed so that each step is a splitting field of a polynomial of the form $x^n-a$. We will come back to this; it is the gap in Ruffini’s argument.

Second: specific polynomials of every degree *are* solvable by radicals. $x^n-1$ is; the cyclotomic fields are radical (after Gauss) over $\mathbb{Q}$. Abel–Ruffini is a statement about the *general* polynomial, and, in the sharpened form, about those particular polynomials whose root-family is too symmetric.

Cardano’s formula, stripped of coefficients, has the shape

$$
\sqrt[3]{\,u + \sqrt{u^2 + v^3}\,} + \sqrt[3]{\,u - \sqrt{u^2 + v^3}\,},
$$

a square root nested inside two cube roots. That is a radical tower of length two (or three, if you count the two cube roots as separate steps, and four if you first adjoin $\zeta_3$ so the cube roots split). The family of three cubic roots lives in the top field; the Galois group is at most $S_3$, which we already know is solvable. Ferrari reduces a quartic to a cubic resolvent, then to quadratics — a longer tower, group at most $S_4$. There is no fifth-degree analogue of that reduction that stays inside radicals, and the reason will not be “we have not found it.” The reason is that $S_5$ has nothing like $V_4$ to quotient by.

---

# Degree, and automorphisms of the home of the roots
{: #degree-and-automorphisms-of-the-home-of-the-roots}

View an extension $E/F$ as a vector space over $F$. Its dimension, finite or infinite, is the **degree** $[E:F]$. (This is [the standard definition](https://en.wikipedia.org/wiki/Degree_of_a_field_extension#The_multiplicativity_formula_for_degrees).) For a simple algebraic extension, $[F(\alpha):F]=\deg m_{\alpha,F}$. So $[\mathbb{Q}(\sqrt{2}):\mathbb{Q}]=2$. Infinite degrees occur — $[\mathbb{Q}(x):\mathbb{Q}]=\infty$, because $1,x,x^2,\ldots$ are linearly independent over $\mathbb{Q}$ — but every splitting field of a polynomial is a finite extension, and we stay finite.

## Automorphisms that fix the coefficients

An **$F$-automorphism** of $E$ is a field automorphism $\sigma:E\to E$ with $\sigma(c)=c$ for every $c\in F$. Write $\mathrm{Aut}(E/F)$ for the group of all of them.

Let $E$ be a splitting field of $f\in F[x]$, with family of roots $\{r_1,\ldots,r_n\}$. If $\sigma\in\mathrm{Aut}(E/F)$ and $f(r_i)=0$, then

$$
f(\sigma(r_i))=\sigma(f(r_i))=0,
$$

because $\sigma$ fixes the coefficients of $f$. So $\sigma$ permutes the family. Since $E=F(r_1,\ldots,r_n)$, the automorphism is determined by this permutation. We obtain an injective homomorphism

$$
\mathrm{Aut}(E/F) \hookrightarrow S_n.
$$

The image is the **Galois group of $f$ over $F$**, written $\mathrm{Gal}(f/F)$ or $\mathrm{Gal}(E/F)$. It is the group of *realizable* symmetries of the family: the rearrangements that can be carried out by a field automorphism fixing the coefficients. It is a subgroup of $S_n$. It need not be all of $S_n$. When it *is* all of $S_n$, the family is maximally symmetric, and that is the case that will kill radical formulae.

## The splitting field of a separable polynomial is Galois

A polynomial is **separable** if its irreducible factors have distinct roots in a splitting field. Over $\mathbb{Q}$ (or any field of characteristic $0$), an irreducible $f$ is separable as soon as $f'\neq 0$, which it is not the zero polynomial; we work in characteristic $0$ from here and stop worrying. Multiple roots would make the embedding into $S_n$ land on fewer than $\deg f$ letters. Separability keeps the family of size $\deg f$.

**Theorem.** Let $E$ be a splitting field of a separable polynomial $f\in F[x]$. Then:

1. $\lvert \mathrm{Aut}(E/F)\rvert = [E:F]$;
2. the **fixed field** $\{\,x\in E : \sigma(x)=x\text{ for all }\sigma\in\mathrm{Aut}(E/F)\,\}$ equals $F$;
3. $E/F$ is **normal**: every irreducible in $F[x]$ with one root in $E$ splits completely in $E$.

A finite extension with these properties is called **Galois**. Conversely, every finite Galois extension is the splitting field of a separable polynomial. This is the content of the discussion at [Math.StackExchange 962898](https://math.stackexchange.com/questions/962898/on-a-proof-that-the-splitting-field-of-a-separable-polynomial-is-galois); the argument below is the standard one.

*Why $\lvert G\rvert=[E:F]$.* Always $\lvert \mathrm{Aut}(E/F)\rvert\le [E:F]$: an $F$-automorphism is determined by where it sends a primitive element (or, inductively, a sequence of adjoined roots), and each minimal polynomial has at most its degree many roots in $E$. For a splitting field of a separable $f$, each such choice *extends*. Induct on the number of roots of $f$ outside $F$. If $f$ already splits in $F$, then $E=F$ and both sides are $1$. Otherwise let $\alpha$ be a root of an irreducible factor $p$ of $f$, of degree $d\ge 2$. There are $d$ distinct $F$-embeddings $F(\alpha)\to E$, one per root of $p$. Each extends to an automorphism of $E$ because $E$ is still a splitting field of $f$ over $F(\alpha)$. By induction $\lvert \mathrm{Aut}(E/F(\alpha))\rvert=[E:F(\alpha)]$. Counting:

$$
\lvert \mathrm{Aut}(E/F)\rvert = d\cdot [E:F(\alpha)] = [F(\alpha):F]\,[E:F(\alpha)] = [E:F],
$$

where the last equality is the tower law, proved in the next section; if you want the logic acyclic, postpone this count until after that proof — the two results are meant to be read as a pair.

*Why the fixed field is $F$.* Let $F'$ be the fixed field of $G=\mathrm{Aut}(E/F)$. Then $F\subset F'\subset E$, and $G=\mathrm{Aut}(E/F')$. But $E$ is still a splitting field of the same separable $f$ over $F'$, so $\lvert \mathrm{Aut}(E/F')\rvert=[E:F']$. Combined with $\lvert \mathrm{Aut}(E/F)\rvert=[E:F]$ we get $[E:F']=[E:F]$, hence $F'=F$.

*Normality.* If an irreducible $p\in F[x]$ has one root $\alpha\in E$, then any other root $\beta$ (in a splitting field) is the image of $\alpha$ under an $F$-embedding $F(\alpha)\to\overline{F}$, and such embeddings extend to automorphisms of $E$ when $E/F$ is a splitting field of a separable polynomial; thus $\beta\in E$.

## Two examples, now with groups

**$\mathbb{Q}(\sqrt{2})/\mathbb{Q}$.** Degree $2$, Galois group $\{\mathrm{id},\,\sqrt{2}\mapsto-\sqrt{2}\}\cong C_2\cong S_2$. The family of $x^2-2$ has two labels; both rearrangements are realized.

**$\mathbb{Q}(\sqrt[3]{2},\zeta_3)/\mathbb{Q}$.** Let $\alpha=\sqrt[3]{2}\in\mathbb{R}$. Then $[\mathbb{Q}(\alpha):\mathbb{Q}]=3$. The polynomial $x^2+x+1$ is the minimal polynomial of $\zeta_3$ over $\mathbb{Q}(\alpha)$ (it is irreducible over $\mathbb{R}$, hence over $\mathbb{Q}(\alpha)\subset\mathbb{R}$), so $[E:\mathbb{Q}(\alpha)]=2$ and $[E:\mathbb{Q}]=6$. The Galois group has order $6$, hence is $S_3$ (the only subgroup of $S_3$ of order $6$ is $S_3$). Explicitly: you may send $\alpha$ to $\alpha\zeta_3^k$ for $k=0,1,2$, and independently send $\zeta_3$ to $\zeta_3^{\pm 1}$.

Label the family $r_0=\alpha$, $r_1=\alpha\zeta_3$, $r_2=\alpha\zeta_3^2$. The automorphism $\sigma$ with $\sigma(\alpha)=\alpha\zeta_3$ and $\sigma(\zeta_3)=\zeta_3$ cycles the roots: $r_0\mapsto r_1\mapsto r_2\mapsto r_0$, a $3$-cycle. The automorphism $\tau$ with $\tau(\alpha)=\alpha$ and $\tau(\zeta_3)=\zeta_3^{-1}=\zeta_3^2$ swaps $r_1$ and $r_2$ and fixes $r_0$, a transposition. These generate $S_3$, and $\tau\sigma\tau^{-1}=\sigma^{-1}$, the usual presentation. Complex conjugation, on this labeling, *is* $\tau$: it fixes the real root and swaps the two non-real ones. Degree three, two non-real roots — the $p-2$ pattern already, except $S_3$ is solvable, so Cardano still works. The same pattern at $p=5$ will not.

The dictionary is now in place. Section II gave us groups of rearrangements. This section realized some of those rearrangements as automorphisms of the splitting field. The Galois group is the symmetry the coefficients can actually see.

---

# The tower theorem
{: #the-tower-theorem}

Degrees multiply. That is the arithmetic of nested adjoining, and it is why a radical formula is a very particular kind of extension.

**Theorem (tower law).** If $K\subset L\subset M$ are fields, then

$$
[M:K] = [M:L]\cdot[L:K].
$$

The product is ordinary multiplication when both factors are finite, and a product of cardinals otherwise. In particular, if $M/K$ is finite then so are both steps; if either step is infinite, so is $M/K$. This is the [multiplicativity formula](https://en.wikipedia.org/wiki/Degree_of_a_field_extension#The_multiplicativity_formula_for_degrees) and the [tower law](https://artofproblemsolving.com/wiki/index.php/Tower_law).

## Proof, finite case

Let $d=[L:K]$ and $e=[M:L]$, both finite. Choose a basis $\{u_1,\ldots,u_d\}$ of $L$ as a $K$-vector space, and a basis $\{w_1,\ldots,w_e\}$ of $M$ as an $L$-vector space. The claim is that the $de$ products $\{u_m w_n\}$ form a basis of $M$ over $K$.

**They span.** Take $x\in M$. Write $x=\sum_{n=1}^e a_n w_n$ with $a_n\in L$. Write each $a_n=\sum_{m=1}^d b_{m,n} u_m$ with $b_{m,n}\in K$. Then

$$
x = \sum_{n=1}^e\sum_{m=1}^d b_{m,n}\,(u_m w_n).
$$

**They are linearly independent.** Suppose $\sum_{n,m} b_{m,n}(u_m w_n)=0$ with $b_{m,n}\in K$. Group as $\sum_n \bigl(\sum_m b_{m,n} u_m\bigr) w_n = 0$. Linear independence of the $w_n$ over $L$ forces $\sum_m b_{m,n} u_m = 0$ for each $n$. Linear independence of the $u_m$ over $K$ forces every $b_{m,n}=0$.

Hence $[M:K]=de$.

(The infinite case is the same argument with bases indexed by sets $A$ and $B$; the product basis is indexed by $A\times B$.)

## What the formula forbids

If $[M:K]$ is prime, there is no field strictly between $K$ and $M$: the only factorizations of a prime are $1\cdot p$ and $p\cdot 1$. Thus $\mathbb{C}/\mathbb{R}$, of degree $2$, has no intermediate field, and $\mathbb{Q}(\sqrt{2})/\mathbb{Q}$ has none either.

**Worked tower: $\mathbb{Q}(\sqrt{2},\sqrt{3})$. ** Let $L=\mathbb{Q}(\sqrt{2})$, so $[L:\mathbb{Q}]=2$. The polynomial $x^2-3$ remains irreducible over $L$ (if $\sqrt{3}=a+b\sqrt{2}$ then squaring and comparing rational and irrational parts yields a contradiction). So $[L(\sqrt{3}):L]=2$, hence $[\mathbb{Q}(\sqrt{2},\sqrt{3}):\mathbb{Q}]=4$. A basis is $\{1,\sqrt{2},\sqrt{3},\sqrt{6}\}$. This is a radical tower of two square-root steps, total degree $2\cdot 2=4$.

The same tower law reads the intermediate fields. Any proper subfield of a degree-$4$ extension has degree $2$ over $\mathbb{Q}$. There are three of them: $\mathbb{Q}(\sqrt{2})$, $\mathbb{Q}(\sqrt{3})$, and $\mathbb{Q}(\sqrt{6})$. Each is the fixed field of a subgroup of order $2$ in the Klein four-group $\mathrm{Gal}(\mathbb{Q}(\sqrt{2},\sqrt{3})/\mathbb{Q})\cong C_2\times C_2$, generated by the independent sign-flips $\sqrt{2}\mapsto\pm\sqrt{2}$ and $\sqrt{3}\mapsto\pm\sqrt{3}$. Nested square roots, in this instance, produce an abelian Galois group of exponent $2$ — as solvable as a group can be.

A nested radical need not denest. $\sqrt{2+\sqrt{2}}$ generates a degree-$4$ extension of $\mathbb{Q}$ (its minimal polynomial is $x^4-4x^2+2$, Eisenstein at $2$), sitting in the radical tower $\mathbb{Q}\subset\mathbb{Q}(\sqrt{2})\subset\mathbb{Q}(\sqrt{2+\sqrt{2}})$. Sometimes such expressions collapse — $\sqrt{5+2\sqrt{6}}=\sqrt{2}+\sqrt{3}$ — and the tower law is how you prove the collapse: both sides generate the same degree-$4$ field. When they do not collapse, you are genuinely climbing.

## Radical towers, measured

A pure radical step $F(\sqrt[n]{a})/F$ has degree *dividing* $n$: the minimal polynomial of $\sqrt[n]{a}$ over $F$ divides $x^n-a$. Once the $n$th roots of unity already live in $F$, the extension (if irreducible) is cyclic of degree $n$, with Galois group generated by $\sqrt[n]{a}\mapsto \zeta_n\sqrt[n]{a}$. That is **Kummer theory** in one sentence: adjoining an $n$th root, in the presence of the $n$th roots of unity, is a cyclic Galois extension.

A nested-radical formula is therefore a tower whose successive Galois groups — after one inserts the missing roots of unity, so that each step splits $x^{n_i}-a_i$ completely — are cyclic. The composite Galois group, by the correspondence below, is assembled from cyclic quotients: it is **solvable**.

The insertion of roots of unity is not a minor bookkeeping point. A radical $\sqrt[n]{a}$ has $n$ conjugates, the other $n$th roots of $a$, and they differ by $n$th roots of unity. If those roots of unity are not already in the current field, the pure-radical step $F(\sqrt[n]{a})/F$ is typically *not* Galois (the real cube root of $2$, again). The refined tower that Galois theory wants looks like

$$
F \subset F(\zeta_{n_1}) \subset F(\zeta_{n_1},\sqrt[n_1]{a_1}) \subset \cdots,
$$

each step Galois, first abelian (cyclotomic), then cyclic (Kummer). Cyclotomic extensions are themselves solvable — $\mathrm{Gal}(\mathbb{Q}(\zeta_n)/\mathbb{Q})\cong(\mathbb{Z}/n\mathbb{Z})^\times$ is abelian — so inserting them does not smuggle in non-solvable symmetry. It merely makes the correspondence apply at every rung.

## The Galois correspondence, used not exhibited

Let $E/F$ be finite Galois, $G=\mathrm{Gal}(E/F)$. There is an inclusion-reversing bijection

$$
\{\text{subgroups }H\le G\} \;\longleftrightarrow\; \{\text{fields }K\text{ with }F\subset K\subset E\}
$$

sending $H$ to its fixed field $E^H$ and sending $K$ to $\mathrm{Gal}(E/K)$. Degrees match orders: $[E:E^H]=\lvert H\rvert$ and $[E^H:F]=[G:H]$. Moreover $K/F$ is Galois if and only if $\mathrm{Gal}(E/K)$ is *normal* in $G$, in which case $\mathrm{Gal}(K/F)\cong G/\mathrm{Gal}(E/K)$.

This is the dictionary between the group theory of §II and the towers of this section. A chain of fields $F=F_0\subset F_1\subset\cdots\subset F_k=E$ with each $F_{i+1}/F_i$ Galois cyclic corresponds to a chain of groups $G=\mathrm{Gal}(E/F_0)\trianglerighteq \mathrm{Gal}(E/F_1)\trianglerighteq\cdots\trianglerighteq\{1\}$ with cyclic quotients. That is a solvable series.

**Theorem (Galois).** A separable polynomial $f\in F[x]$ is solvable by radicals over $F$ if and only if $\mathrm{Gal}(f/F)$ is a solvable group.

One direction: a radical tower, Galois-closed by adjoining roots of unity along the way (each cyclotomic extension $\mathbb{Q}(\zeta_n)/\mathbb{Q}$ has abelian Galois group $(\mathbb{Z}/n\mathbb{Z})^\times$, hence is itself solvable), produces a solvable Galois group of the splitting field. The other direction: if the Galois group is solvable, refine to cyclic prime-degree quotients, and realize each cyclic step as a radical extension by Kummer, after a cyclotomic base change. The roots then lie in a radical tower.

Ruffini assumed the radicals in a putative formula already lived *inside* the splitting field. That is extra. Cardano’s formula for $x^3-15x-20$ extracts cube roots of $10\pm 5i$, which do not lie in the splitting field over $\mathbb{Q}$ (the three roots are real). Abel’s theorem on natural irrationalities repairs the general-coefficient case; Galois’ criterion repairs all cases.

We now have the two halves. A radical formula $\Rightarrow$ solvable Galois group. $S_n$ for $n\ge 5$ is not solvable. It remains to see that the general quintic — and some perfectly concrete quintics over $\mathbb{Q}$ — actually *have* Galois group $S_5$. That is the symmetry of the quintic.

---

# Quintic symmetry
{: #quintic-symmetry}

## What a formula would be

Suppose there were a general radical formula for degree $n$: an expression built from the coefficients $a_1,\ldots,a_n$ by field operations and nested radicals, which, when the $a_i$ are specialized to the coefficients of any degree-$n$ polynomial, produces a root. Interpreting the $a_i$ as indeterminates, the expression would place a root in a radical tower over the field of rational functions $F=\mathbb{Q}(a_1,\ldots,a_n)$. The splitting field over $F$ would then sit in (a Galois closure of) a radical tower, and $\mathrm{Gal}(f/F)$ would be solvable.

So: if we can show that the Galois group of the general degree-$n$ polynomial is $S_n$, then for $n\ge 5$ there is no such formula.

## The general polynomial has symmetry $S_n$

Start from the roots, not the coefficients. Let $x_1,\ldots,x_n$ be indeterminates, and let

$$
P(x) = (x-x_1)\cdots(x-x_n) = x^n + b_1 x^{n-1} + \cdots + b_n,
$$

so the $b_i$ are the elementary symmetric polynomials in the $x_j$ (Vieta: $b_1=-(x_1+\cdots+x_n)$, etc.). Let $H=\mathbb{Q}(x_1,\ldots,x_n)$ and $K=\mathbb{Q}(b_1,\ldots,b_n)$. Every permutation of the $x_i$ extends to a field automorphism of $H$, and by Vieta it *fixes* $K$. Distinct permutations give distinct automorphisms, because they move the $x_i$ differently. Thus

$$
\mathrm{Gal}(H/K) \cong S_n.
$$

(The extension is Galois: $H$ is the splitting field of the separable polynomial $P$ over $K$.) The $b_i$ are algebraically independent — that is the fundamental theorem of symmetric polynomials — so the map sending each indeterminate coefficient $a_i$ to $b_i$ is an isomorphism from $\mathbb{Q}(a_1,\ldots,a_n)$ onto $K$. Transporting the Galois group along this isomorphism, the general polynomial of degree $n$ over $\mathbb{Q}(a_1,\ldots,a_n)$ has Galois group $S_n$.

There is a geometric way to hear the same fact. Think of the coefficients as a point in $\mathbb{C}^n$, and of the $n$ roots as an unordered $n$-tuple. As you walk a loop in coefficient space that avoids the discriminant locus (the hypersurface on which two roots collide), the roots move continuously and return to themselves as a set, but they may have been permuted. The permutation depends on the loop. For the general polynomial, every permutation arises from some loop: the complement of the discriminant is a $K(\pi,1)$ for the braid group, and passing to unordered roots gives a surjection onto $S_n$. A radical expression in the coefficients would be a single-valued algebraic function on a finite branched cover built from $z\mapsto z^n$ maps — and those covers have solvable monodromy. $S_5$ is not solvable, so it cannot arise as the monodromy of a nested-radical cover. (This is the seed of Arnold’s topological proof of Abel–Ruffini. We will not develop it; the Galois argument above is the same obstruction, written in fields rather than in loops.)

Specialization is how the general fact infects particular polynomials. If a formula in the indeterminate coefficients existed, substituting rational numbers for the $a_i$ would give a radical expression for every quintic over $\mathbb{Q}$. So it is enough, to kill a *uniform* formula, that $S_5$ be the Galois group in the indeterminate case. To kill *particular* quintics, one still has to check that the Galois group remains non-solvable after specialization. Hilbert irreducibility says that “most” specializations of the general quintic still have Galois group $S_5$ (or $A_5$). The $p-2$ real-roots theorem is a hands-on way to catch some of them.

**Abel–Ruffini theorem.** There is no formula, in the coefficients, by field operations and nested radicals, for the roots of the general polynomial of degree $n\ge 5$.

That is the original theorem: a statement about a formula in *indeterminates*. It does not, by itself, exhibit a polynomial with rational coefficients that cannot be solved by radicals. (In principle every *particular* quintic might have had its own private radical expression.) Galois’ criterion, plus the existence of polynomials over $\mathbb{Q}$ with Galois group $S_5$, closes that gap.

## Concrete quintics with $S_5$ symmetry

The following is a standard machine, of which [Math.StackExchange 3075225](https://math.stackexchange.com/questions/3075225/f-irreducible-polynomial-with-p-2-real-roots-rightarrow-gal-mathbbq-f) is one instance.

**Theorem.** Let $p\ge 5$ be prime, and let $f\in\mathbb{Q}[x]$ be irreducible of degree $p$, with exactly $p-2$ real roots (hence exactly one conjugate pair of non-real roots). Then $\mathrm{Gal}(f/\mathbb{Q})\cong S_p$.

*Proof.* Let $E\subset\mathbb{C}$ be a splitting field, $G=\mathrm{Gal}(E/\mathbb{Q})\le S_p$.

Irreducibility $\Rightarrow$ $G$ acts transitively on the $p$ roots. In particular $p$ divides $\lvert G\rvert=[E:\mathbb{Q}]$, by the orbit-stabilizer theorem (or: adjoining one root gives a subfield of degree $p$, and the tower law makes $p$ divide $[E:\mathbb{Q}]$). Cauchy’s theorem: $G$ contains an element of order $p$. The only elements of order $p$ in $S_p$ are $p$-cycles (a product of disjoint cycles has order the lcm of the lengths, and $p$ is prime). So $G$ contains a $p$-cycle.

Complex conjugation is an automorphism of $\mathbb{C}$ fixing $\mathbb{Q}$. It preserves $E$ because it permutes the roots of $f$ (real coefficients). It fixes each of the $p-2$ real roots and swaps the two non-real ones. Restricted to $E$, it is therefore a **transposition** in $G$.

**Lemma.** A subgroup of $S_p$ ($p$ prime) that contains a $p$-cycle and a transposition is all of $S_p$.

Relabel so the transposition is $(1\,2)$. Write the $p$-cycle as $(1\,a_2\,\cdots\,a_p)$. Some power of it sends $1$ to $2$, because the cycle acts transitively; replacing the cycle by that power, we may assume it is $(1\,2\,3\,\cdots\,p)$. Conjugating the transposition by powers of the cycle produces the adjacent transpositions:

$$
(1\,2\,3\,\cdots\,p)^k\,(1\,2)\,(1\,2\,3\,\cdots\,p)^{-k} = (k+1\,k+2),
$$

indices modulo $p$ in $\{1,\ldots,p\}$. Adjacent transpositions generate $S_p$, as already recorded. Hence $G=S_p$.

The hypothesis that $p$ is prime was used twice: to guarantee that an element of order $p$ is a single $p$-cycle, and to guarantee transitivity of that cycle on all $p$ letters. For composite degree the same counting can leave you in a proper transitive subgroup (dihedral, Frobenius, $A_n$, \ldots). Prime degree plus a transposition is a sledgehammer.

**Example: $f(x)=x^5-6x+3$.** Eisenstein at $3$: $3$ divides $6$ and $3$, $9$ does not divide $3$. Irreducible over $\mathbb{Q}$. Now count real roots. $f(-2)=-17$, $f(-1)=8$, $f(0)=3$, $f(1)=-2$, $f(2)=23$: three sign changes, so at least three real roots by the intermediate-value theorem. The derivative $f'(x)=5x^4-6$ has exactly two real zeros, $\pm(6/5)^{1/4}$. Rolle’s theorem: between any two real roots of $f$ lies a root of $f'$, so $f$ has *at most* three real roots. Exactly three real roots, two non-real. The theorem gives $\mathrm{Gal}(f/\mathbb{Q})\cong S_5$.

This polynomial is not solvable by radicals. Its five roots exist in $\mathbb{C}$, by the FTA. They do not lie in any radical tower over $\mathbb{Q}$.

**Example: $q(x)=x^5-x-1$,** the simplest polynomial Wikipedia records as unsolvable. Reduction modulo a prime, for a monic integer polynomial, produces cycle types in the Galois group (Dedekind–Frobenius): if $q$ factors modulo a prime $\ell$ not dividing the discriminant as a product of distinct irreducibles of degrees $d_1,\ldots,d_k$, then $G$ contains an element of cycle type $d_1+\cdots+d_k$. Modulo $2$, $q(x)\equiv (x^2+x+1)(x^3+x^2+1)$ in $\mathbb{F}_2[x]$, two irreducibles of degrees $2$ and $3$, hence a permutation of type $2+3$ in $G$; cubing it yields a transposition. Modulo $3$, $q$ is irreducible, hence $G$ contains a $5$-cycle. A transposition and a $5$-cycle generate $S_5$. Same conclusion, different pair of hands.

## Degree five is not the crime

The polynomial $x^5-2$ *is* solvable by radicals. Its splitting field is $\mathbb{Q}(\sqrt[5]{2},\zeta_5)$. The tower

$$
\mathbb{Q} \subset \mathbb{Q}(\zeta_5) \subset \mathbb{Q}(\zeta_5,\sqrt[5]{2})
$$

has degrees $\varphi(5)=4$ and $5$, product $20$ by the tower law. (You must adjoin $\zeta_5$ *first*, or at least somewhere: $\mathbb{Q}(\sqrt[5]{2})$ is a real field of degree $5$, hence not Galois over $\mathbb{Q}$, and does not contain the four non-real fifth roots of $2$. This is $x^3-2$ again, one degree up.) The Galois group has order $20$. It is the Frobenius group of affine transformations $x\mapsto ax+b$ over $\mathbb{F}_5$: an automorphism is determined by

$$
\sqrt[5]{2}\mapsto \sqrt[5]{2}\,\zeta_5^{b}, \qquad \zeta_5\mapsto\zeta_5^{a},
$$

with $a\in(\mathbb{Z}/5\mathbb{Z})^\times$ and $b\in\mathbb{Z}/5\mathbb{Z}$. The maps with $a=1$ form a normal cyclic subgroup $C_5$ (pure translation of the radical); the quotient is $C_4$ (the cyclotomic Galois group). Solvable series: $\{1\}\trianglelefteq C_5 \trianglelefteq C_5\rtimes C_4$. And indeed $\sqrt[5]{2}$ is a radical, and the other roots are $\sqrt[5]{2}\,\zeta_5^k$.

Compare the two quintics as permutation groups acting on their five roots. For $x^5-2$, complex conjugation fixes the one real root and inverts $\zeta_5$, which (on a suitable labeling) is a product of two disjoint transpositions, an even permutation of order $2$ — not a transposition of two roots. The $p-2$ real-roots theorem never fires, because there are not three real roots to fix. For $x^5-6x+3$, conjugation *is* a transposition, the group is forced up to $S_5$, and solvability dies.

The same degree, two different symmetries. $S_5$ has order $120$; the Frobenius group has order $20$. One is solvable, one is not. Abel–Ruffini forbids a *uniform* formula because the *general* quintic has the larger symmetry. Galois forbids a radical expression for $x^5-6x+3$ because *that* quintic has the larger symmetry too.

## Why degrees two, three, and four have formulae

$S_2$, $S_3$, $S_4$ are solvable. The Galois group of any polynomial of degree $\le 4$ embeds in one of these, hence is solvable, hence the polynomial is solvable by radicals. The quadratic formula, Cardano’s formula, and Ferrari’s formula are the radical towers those solvable series permit. One does not need to write the towers out to know they exist. (Writing them out is a different, older, and much messier story.)

The correspondence is visible in the groups we already wrote down.

- Degree $2$: $S_2\cong C_2$. One quadratic radical. The sign homomorphism *is* the Galois group.
- Degree $3$: $\{1\}\trianglelefteq A_3\trianglelefteq S_3$. The quadratic subextension is generated by $\sqrt{\Delta}$, where $\Delta=\prod_{i \lt j}(r_i-r_j)^2$ is the discriminant; adjoining it cuts $S_3$ down to $A_3\cong C_3$, which is then a pure cube-root step once $\zeta_3$ is present. Cardano’s nested square-then-cube is exactly this chain.
- Degree $4$: $\{1\}\trianglelefteq V_4\trianglelefteq A_4\trianglelefteq S_4$. The quotient $S_4/V_4\cong S_3$ is Cardano’s cubic resolvent. Solving it (by the previous bullet) lands you in a $V_4$-extension, which is a pair of quadratics. Ferrari is this chain written in coefficients.

There is no corresponding normal subgroup of $S_5$ with abelian — or even solvable — quotient except $A_5$, whose quotient is only $C_2$. Adjoining a square root of the discriminant cuts $S_5$ down to $A_5$, and $A_5$ does not budge. That is why “just adjoin $\sqrt{\Delta}$ and continue as in the cubic” dies on the quintic: you have spent your only normal subgroup, and what remains is simple.

For degree $\ge 5$ the embedding $\mathrm{Gal}(f/F)\hookrightarrow S_n$ is into a non-solvable group, which does not by itself prove unsolvability — a subgroup of a non-solvable group may be solvable, as $x^5-2$ shows. Unsolvability is the assertion that the Galois group *equals* (or contains) a non-solvable group, typically $A_n$ or $S_n$. The group $A_n$ for $n\ge 5$ is already enough: it is not solvable, so a polynomial with Galois group $A_5$ is equally unsolvable by radicals. Distinguishing $A_5$ from $S_5$ is the question of whether $\Delta$ is a square in the base field. Our examples were chosen to have a transposition, hence to meet $S_5$ rather than $A_5$; an odd permutation in the group is the whole distinction.

## Precis

- **Existence.** The fundamental theorem of algebra: a degree-$n$ polynomial has a family of $n$ roots in $\mathbb{C}$.
- **Symmetry.** The family may be rearranged. All rearrangements form $S_n$; the even ones form $A_n$. For $n\ge 5$, $A_n$ is simple and non-abelian, so $S_n$ is not solvable.
- **Housing.** The family lives in a splitting field over the coefficient field. Automorphisms of that field that fix the coefficients are the rearrangements the coefficients can see: the Galois group, a subgroup of $S_n$. The splitting field of a separable polynomial is Galois; the count of automorphisms equals the degree.
- **Towers.** Degrees multiply along a chain of fields. A nested-radical formula is a tower of pure radical steps. After inserting roots of unity, each step is cyclic Galois. The Galois group of a polynomial solvable by radicals is therefore a solvable group, and conversely.
- **Mismatch.** The general degree-$n$ polynomial has Galois group $S_n$. For $n\ge 5$ that group is not solvable. Hence there is no general radical formula. Particular polynomials over $\mathbb{Q}$, such as $x^5-6x+3$ and $x^5-x-1$, also have Galois group $S_5$, hence have no radical expression for their roots over $\mathbb{Q}$. Degree five is allowed to be solvable ($x^5-2$); $S_5$-sized symmetry is not.

That is the lack of an algebraic solution for quintic and higher equations, stated precisely: not that roots fail to exist, but that the symmetry of the root family cannot be assembled from the cyclic symmetries of nested radicals.

---

# History, scope, references
{: #history-scope-references}

Paolo Ruffini nearly proved the general-coefficient case in 1799, in *Teoria generale delle equazioni*. Cauchy believed him; Abel, later, found the memoir too tangled to adjudicate. The gap is the one already named: Ruffini treated radicals as if they lived in the splitting field. Abel published a six-page proof in 1824 (he paid for the printing, and saved paper) and a fuller one in 1826. He was at work on the *which* quintics question when he died in 1829.

Évariste Galois, at eighteen, submitted the criterion — solvability by radicals if and only if the group of the equation is solvable — to the Paris Academy. It was rejected as too sketchy. He died in 1832. Liouville published the memoir in 1846. Wantzel, already aware of Galois, noted in 1845 that Abel’s argument hits the *general* polynomial, while Galois produces *specific* unsolvable ones.

What this note does not claim: that roots cannot be approximated (they can, to any precision); that no closed form of any kind exists (Bring’s radical and elliptic modular functions give expressions outside the radical language); that every quintic is unsolvable (only those whose Galois group is not a solvable group). Cayley’s resolvent, a degree-six polynomial in the coefficients of a quintic, tests the solvable cases: an irreducible quintic is solvable by radicals if and only if that sextic has a rational root.

The sources woven here are the [fundamental theorem of algebra](https://en.wikipedia.org/wiki/Fundamental_theorem_of_algebra); [parity of a permutation](https://en.wikipedia.org/wiki/Parity_of_a_permutation); the [degree of a field extension](https://en.wikipedia.org/wiki/Degree_of_a_field_extension#The_multiplicativity_formula_for_degrees) and the [tower law](https://artofproblemsolving.com/wiki/index.php/Tower_law); [the splitting field of a separable polynomial is Galois](https://math.stackexchange.com/questions/962898/on-a-proof-that-the-splitting-field-of-a-separable-polynomial-is-galois); [irreducible of prime degree with $p-2$ real roots has Galois group $S_p$](https://math.stackexchange.com/questions/3075225/f-irreducible-polynomial-with-p-2-real-roots-rightarrow-gal-mathbbq-f); and the [Abel–Ruffini theorem](https://en.wikipedia.org/wiki/Abel%E2%80%93Ruffini_theorem). For the $S_p$ lemma in cleaner notes, Keith Conrad’s *Galois groups as permutation groups* is the standard blurb. Dummit and Foote, Chapter 14, is the textbook companion if you want every lemma with a number.
