---
layout: post
title: "Back-of-the-Envelope: Abel–Ruffini, Vol. IV: Where the Roots Live"
date: 2026-08-22 12:03:00
categories: algebra
mathjax: true
---

*Abel–Ruffini:* [I](/blog/2026/08/22/Abel-Ruffini-Theorem) · [II](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-II) · [III](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-III) · **IV** · [V](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-V) · [VI](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-VI)

*Fields, splitting fields, radical towers, and the Galois group: the rearrangements of the roots that the coefficients can actually see.*

# Field extensions: where the family lives
{: #field-extensions-where-the-family-lives}

The FTA placed the family $\lbrace r_1,\ldots,r_n\rbrace$ in $\mathbb{C}$. The coefficients may live in a much smaller field — classically $\mathbb{Q}$. The roots need not.

Take $x^2-2\in\mathbb{Q}[x]$. It is irreducible over $\mathbb{Q}$ (if $\sqrt{2}=p/q$ in lowest terms then $p^2=2q^2$, so $2$ divides $p$ and then $q$, contradiction). The family is $\lbrace\sqrt{2},-\sqrt{2}\rbrace$. Neither root is rational. Both live in the smallest field that contains $\mathbb{Q}$ and $\sqrt{2}$.

## Adjoining one element

If $F$ is a field and $\alpha$ lives in some bigger field, write $F(\alpha)$ for the **smallest field containing $F$ and $\alpha$**. Concretely, if $\alpha$ is algebraic over $F$ — if it satisfies a polynomial with coefficients in $F$ — there is a unique monic polynomial of least degree with this property, the **minimal polynomial** $m_{\alpha,F}$. Then

$$
F(\alpha) = \{ c_0 + c_1\alpha + \cdots + c_{d-1}\alpha^{d-1} : c_i\in F \},
$$

where $d=\deg m_{\alpha,F}$, with multiplication reduced using $m_{\alpha,F}(\alpha)=0$. In particular $F(\alpha)$ is a $d$-dimensional vector space over $F$, with basis $\lbrace 1,\alpha,\ldots,\alpha^{d-1}\rbrace$.

For $\alpha=\sqrt{2}$ over $\mathbb{Q}$, the minimal polynomial is $x^2-2$, and $\mathbb{Q}(\sqrt{2})=\lbrace a+b\sqrt{2}:a,b\in\mathbb{Q}\rbrace$ with basis $\lbrace 1,\sqrt{2}\rbrace$. The family of roots of $x^2-2$ *already lives entirely in this field*: $-\sqrt{2}$ is just $-1\cdot\sqrt{2}$.

## Splitting fields: the home of the whole family

Adjoining one root is not always enough.

<div class="note">
<p><strong>Splitting field.</strong> An extension $E/F$ in which $f$ factors into linear terms, generated over $F$ by those roots. Equivalently: the smallest house containing the entire family.</p>
</div>

Existence: adjoin one root of an irreducible factor, repeat. Uniqueness up to an isomorphism fixing $F$: any two splitting fields are $F$-isomorphic. We work throughout with a splitting field sitting inside $\mathbb{C}$, which the FTA permits.

**Example: $x^2-2$ over $\mathbb{Q}$.** Splitting field $\mathbb{Q}(\sqrt{2})$. The family lives there.

**Example: $x^3-2$ over $\mathbb{Q}$.** The real cube root $\sqrt[3]{2}$ generates $\mathbb{Q}(\sqrt[3]{2})\subset\mathbb{R}$. That field contains *one* root of $x^3-2$. The other two are $\sqrt[3]{2}\,\zeta_3$ and $\sqrt[3]{2}\,\zeta_3^2$, where $\zeta_3=e^{2\pi i/3}=-\frac12+i\frac{\sqrt{3}}{2}$ is a primitive cube root of unity. They are not real. So $\mathbb{Q}(\sqrt[3]{2})$ is *not* a splitting field. The splitting field is $\mathbb{Q}(\sqrt[3]{2},\zeta_3)$. The family of three roots lives there and nowhere smaller.

This is the standing picture: coefficients in a base field $F$; family of roots in $\mathbb{C}$; splitting field $E=F(r_1,\ldots,r_n)$ the smallest house that holds them all.

<div class="warn">
<p><strong>Warning: not every radical step is Galois.</strong> Adjoining <em>one</em> $n$th root $F(\sqrt[n]{a})$ typically misses the other $n-1$ conjugates. They differ from the chosen root by $n$th roots of unity. For $x^3-2$, $\mathbb{Q}(\sqrt[3]{2})$ is real of degree $3$ and contains only one root; the extension is not Galois. To apply the Galois correspondence at that step we must also adjoin $\zeta_n$, so the step splits $x^n-a$ completely and becomes symmetric (cyclic, once $\zeta_n$ is present). That is why “radical tower $\Rightarrow$ solvable Galois group” requires a cyclotomic refinement, not the raw nested-radical expression alone.</p>
</div>

## Nested radicals are a special kind of house

The quadratic formula is already a radical tower, and it is worth writing it that way so the later obstruction has something to obstruct. For $ax^2+bx+c$ with $a\neq 0$, set $F=\mathbb{Q}(a,b,c)$ (or $\mathbb{Q}$, if $a,b,c\in\mathbb{Q}$). The discriminant $d=b^2-4ac$ lives in $F$. The tower is

$$
F \subset F(\sqrt{d}),
$$

a single square-root step of degree $1$ or $2$, and both roots $\frac{-b\pm\sqrt{d}}{2a}$ live in the top field. The family $\lbrace\sqrt{d},-\sqrt{d}\rbrace$ is swapped by the unique nontrivial automorphism, which is why the two choices of sign in the formula are not a defect: they are the Galois group.

A **pure radical extension** of $F$ is $F(\sqrt[n]{a})$ for some $a\in F$ and $n\ge 2$: adjoin a root of $x^n-a$. A **radical tower** over $F$ is a finite chain

$$
F = F_0 \subset F_1 \subset \cdots \subset F_k
$$

in which each $F_{i+1}=F_i(\alpha_i)$ with $\alpha_i^{n_i}\in F_i$ for some $n_i\ge 2$. A radical *expression* determines such a tower (each nested root is one step; a choice of branch is a choice of which root to adjoin). Conversely, the elements of a radical tower are the algebraic objects captured by nested radical constructions. Example: $\sqrt{2+\sqrt{2}}$ lives in $\mathbb{Q}\subset\mathbb{Q}(\sqrt{2})\subset\mathbb{Q}(\sqrt{2+\sqrt{2}})$. Cardano’s formula for a cubic is a messy tower of square roots and cube roots. Ferrari’s formula for a quartic is a longer such tower.

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

Let $E$ be a splitting field of $f\in F[x]$, with family of roots $\lbrace r_1,\ldots,r_n\rbrace$. If $\sigma\in\mathrm{Aut}(E/F)$ and $f(r_i)=0$, then

$$
f(\sigma(r_i))=\sigma(f(r_i))=0,
$$

because $\sigma$ fixes the coefficients of $f$. So $\sigma$ permutes the family. Since $E=F(r_1,\ldots,r_n)$, the automorphism is determined by this permutation. We obtain an injective homomorphism

$$
\mathrm{Aut}(E/F) \hookrightarrow S_n.
$$

The image is the **Galois group of $f$ over $F$**, written $\mathrm{Gal}(f/F)$ or $\mathrm{Gal}(E/F)$. It is the group of *realizable* symmetries of the family: the rearrangements that can be carried out by a field automorphism fixing the coefficients. It is a subgroup of $S_n$. It need not be all of $S_n$. When it *is* all of $S_n$, the family is maximally symmetric, and that is the case that will kill radical formulae.

## The splitting field of a separable polynomial is Galois

A polynomial is **separable** if its irreducible factors have distinct roots in a splitting field. We care because the Galois group injects into $S_n$ with $n=\deg f$ only when there are $n$ distinct letters to permute; a multiple root collapses two labels into one and the count $\lvert\mathrm{Aut}(E/F)\rvert=[E:F]$ fails. Over $\mathbb{Q}$ (characteristic $0$) an irreducible $f$ cannot share a root with its derivative $f'$ unless $f'$ is the zero polynomial, which it is not: $\deg f'\ge 0$ and the leading term of $f$ has not been killed by a characteristic. So every irreducible over $\mathbb{Q}$ is separable. (In characteristic $p$ one can have inseparables such as $x^p-a$.) We work in characteristic $0$ from here.

**Theorem (standard; proof sketch below).** Let $E$ be a splitting field of a separable polynomial $f\in F[x]$. Then:

1. $\lvert \mathrm{Aut}(E/F)\rvert = [E:F]$;
2. the **fixed field** $\lbrace\,x\in E : \sigma(x)=x\text{ for all }\sigma\in\mathrm{Aut}(E/F)\,\rbrace$ equals $F$;
3. $E/F$ is **normal**: every irreducible in $F[x]$ with one root in $E$ splits completely in $E$.

A finite extension with these properties is called **Galois**. Conversely, every finite Galois extension is the splitting field of a separable polynomial. This is the content of the discussion at [Math.StackExchange 962898](https://math.stackexchange.com/questions/962898/on-a-proof-that-the-splitting-field-of-a-separable-polynomial-is-galois); the argument below is the standard one.

*Why $\lvert G\rvert=[E:F]$.* Always $\lvert \mathrm{Aut}(E/F)\rvert\le [E:F]$: an $F$-automorphism is determined by where it sends a primitive element (or, inductively, a sequence of adjoined roots), and each minimal polynomial has at most its degree many roots in $E$. For a splitting field of a separable $f$, each such choice *extends* — this is the **isomorphism-extension theorem**, which we use as a standard fact rather than prove: an $F$-isomorphism between two fields extends to an isomorphism of splitting fields of the same separable polynomial. Induct on the number of roots of $f$ outside $F$. If $f$ already splits in $F$, then $E=F$ and both sides are $1$. Otherwise let $\alpha$ be a root of an irreducible factor $p$ of $f$, of degree $d\ge 2$. There are $d$ distinct $F$-embeddings $F(\alpha)\to E$, one per root of $p$. Each extends to an automorphism of $E$ because $E$ is still a splitting field of $f$ over $F(\alpha)$. By induction $\lvert \mathrm{Aut}(E/F(\alpha))\rvert=[E:F(\alpha)]$. Counting:

$$
\lvert \mathrm{Aut}(E/F)\rvert = d\cdot [E:F(\alpha)] = [F(\alpha):F]\,[E:F(\alpha)] = [E:F],
$$

where the last equality is the tower law, proved at the start of [Vol. V](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-V); if you want the logic acyclic, postpone this count until after that proof — the two results are meant to be read as a pair.

*Why the fixed field is $F$.* Let $F'$ be the fixed field of $G=\mathrm{Aut}(E/F)$. Then $F\subset F'\subset E$, and $G=\mathrm{Aut}(E/F')$. But $E$ is still a splitting field of the same separable $f$ over $F'$, so $\lvert \mathrm{Aut}(E/F')\rvert=[E:F']$. Combined with $\lvert \mathrm{Aut}(E/F)\rvert=[E:F]$ we get $[E:F']=[E:F]$, hence $F'=F$.

*Normality.* If an irreducible $p\in F[x]$ has one root $\alpha\in E$, then any other root $\beta$ (in a splitting field) is the image of $\alpha$ under an $F$-embedding $F(\alpha)\to\overline{F}$, and such embeddings extend to automorphisms of $E$ when $E/F$ is a splitting field of a separable polynomial; thus $\beta\in E$.

## Two examples, now with groups

**$\mathbb{Q}(\sqrt{2})/\mathbb{Q}$.** Degree $2$, Galois group $\lbrace\mathrm{id},\,\sqrt{2}\mapsto-\sqrt{2}\rbrace\cong C_2\cong S_2$. The family of $x^2-2$ has two labels; both rearrangements are realized.

**$\mathbb{Q}(\sqrt[3]{2},\zeta_3)/\mathbb{Q}$.** Let $\alpha=\sqrt[3]{2}\in\mathbb{R}$. Then $[\mathbb{Q}(\alpha):\mathbb{Q}]=3$. The polynomial $x^2+x+1$ is the minimal polynomial of $\zeta_3$ over $\mathbb{Q}(\alpha)$: it is irreducible over $\mathbb{R}$, hence over the real field $\mathbb{Q}(\alpha)$. So $[E:\mathbb{Q}(\alpha)]=2$ and $[E:\mathbb{Q}]=6$. (Symmetrically: $x^3-2$ stays irreducible over $\mathbb{Q}(\zeta_3)$, not because it is irreducible over $\mathbb{Q}$, but because a root in $\mathbb{Q}(\zeta_3)$ would embed a degree-$3$ field into a degree-$2$ extension, which the tower law forbids.) The Galois group has order $6$, hence is $S_3$. Explicitly: you may send $\alpha$ to $\alpha\zeta_3^k$ for $k=0,1,2$, and independently send $\zeta_3$ to $\zeta_3^{\pm 1}$.

Label the family $r_0=\alpha$, $r_1=\alpha\zeta_3$, $r_2=\alpha\zeta_3^2$. The automorphism $\sigma$ with $\sigma(\alpha)=\alpha\zeta_3$ and $\sigma(\zeta_3)=\zeta_3$ cycles the roots: $r_0\mapsto r_1\mapsto r_2\mapsto r_0$, a $3$-cycle. The automorphism $\tau$ with $\tau(\alpha)=\alpha$ and $\tau(\zeta_3)=\zeta_3^{-1}=\zeta_3^2$ swaps $r_1$ and $r_2$ and fixes $r_0$, a transposition. These generate $S_3$, and $\tau\sigma\tau^{-1}=\sigma^{-1}$, the usual presentation. Complex conjugation, on this labeling, *is* $\tau$: it fixes the real root and swaps the two non-real ones. Degree three, two non-real roots — the $p-2$ pattern already, except $S_3$ is solvable, so Cardano still works. The same pattern at $p=5$ will not.

**$x^4-2x^2+9$ over $\mathbb{Q}$: the relations decide the group.** Here the group is visibly smaller than $S_4$, and one can see *why* before computing a single field degree. Solving $x^2=1\pm 2\sqrt{2}\,i$ gives the four roots

$$
r_1=\sqrt{2}+i,\quad r_2=-\sqrt{2}-i,\quad r_3=\sqrt{2}-i,\quad r_4=-\sqrt{2}+i.
$$

Any automorphism must preserve every polynomial relation among the roots with rational coefficients. The polynomial is even, so $r_2=-r_1$ and $r_4=-r_3$. Its constant term is $9$ and its coefficients are palindromic up to scaling, so $3/r$ is a root whenever $r$ is: $r_1r_3=3$ and $r_2r_4=3$. Once you know where $r_1$ goes, those two relations fix where everything else goes. There are four choices for the image of $r_1$, so at most four automorphisms:

$$
\mathrm{id},\quad (1\,2)(3\,4),\quad (1\,3)(2\,4),\quad (1\,4)(2\,3).
$$

The splitting field is $\mathbb{Q}(\sqrt{2},i)$, of degree $4$, so all four exist. The group is the Klein four-group $V_4$, not $S_4$. Each order-$2$ subgroup fixes a quadratic field, and a symmetric expression in the swapped pair finds it: $(r_1+r_3)^2=8$ gives $\mathbb{Q}(\sqrt{2})$ for $\langle(1\,3)(2\,4)\rangle$; $(r_1+r_4)^2=-4$ gives $\mathbb{Q}(i)$ for $\langle(1\,4)(2\,3)\rangle$; $(r_1r_2+1)^2=-8$ gives $\mathbb{Q}(\sqrt{-2})$ for $\langle(1\,2)(3\,4)\rangle$. Every relation among the roots cuts the group down. A *general* polynomial has no relations beyond the ones Vieta forces, and that is why its group is all of $S_n$ ([Vol. VI](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-VI)).

The dictionary is now in place. [Vol. III](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-III) gave us groups of rearrangements. This volume realized some of those rearrangements as automorphisms of the splitting field. The Galois group is the symmetry the coefficients can actually see. The lattice below is the same story for $x^3-2$: $\mathbb{Q}(\zeta_3)$ corresponds to a *normal* subgroup and is Galois over $\mathbb{Q}$; $\mathbb{Q}(\alpha)$ corresponds to a non-normal subgroup and is not.

<p style="text-align:center;">
  <img src="/blog/assets/2026/abel-ruffini/lattice-cube2.png" alt="Field lattice for Q(2^{1/3}, zeta_3) opposite the inverted subgroup lattice of S3" style="max-width:100%;">
</p>

---

**Next:** [Vol. V: Towers and the Galois Correspondence](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-V)

*Abel–Ruffini:* [Vol. I](/blog/2026/08/22/Abel-Ruffini-Theorem) · [Vol. II](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-II) · [Vol. III](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-III) · **Vol. IV** · [Vol. V](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-V) · [Vol. VI](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-VI)
