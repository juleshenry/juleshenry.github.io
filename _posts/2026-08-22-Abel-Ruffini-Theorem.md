---
layout: post
title: "Back-of-the-Envelope: Abel–Ruffini, Vol. I: The Short Proof"
date: 2026-08-22 12:00:00
categories: algebra
mathjax: true
---

*Abel–Ruffini:* **I** · [II](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-II) · [III](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-III) · [IV](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-IV) · [V](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-V) · [VI](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-VI)

*A zero-to-hero guide to one theorem: there is no formula in radicals for the roots of a general quintic. This volume proves it end to end, with loops and commutators and nothing else. The other five volumes rebuild it with Galois theory, which proves more.*

The quadratic formula is one recipe that solves every $ax^2+bx+c$. Sixteenth-century algebraists found similar recipes for cubics and quartics, though much messier ones. Then the pattern stops. No single recipe solves every quintic using the four arithmetic operations and finitely many nested roots.

That statement does **not** mean quintics have no roots. Every degree-five polynomial has five complex roots, counted with multiplicity ([Vol. II](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-II)). It also does not mean that no individual quintic can be solved by radicals: $x^{5}-2=0$ plainly can. The claim is about one universal method that works for arbitrary coefficients.

**Two different claims.** Abel–Ruffini says there is no radical recipe that works for *all* quintics. Galois theory goes further and says which *individual* quintics have no radical solution. The common misreading, "no quintic can be solved by radicals", is false.

---

# The idea in one paragraph

Wiggle the coefficients of a quintic around a closed loop and bring them back to where they started. The polynomial comes back, so its set of five roots comes back too. The individual roots, though, may have traded places. A radical formula can also trade places: $\sqrt{z}$ swaps its two values when $z$ circles the origin once. But radicals are **commutative bookkeepers**. The only thing an $n$th root remembers about a loop is how many times its argument wound around $0$, and winding numbers add. So a loop of the form "go around $A$, then $B$, then $A$ backwards, then $B$ backwards" leaves every radical where it started. Nest the roots $k$ deep and you need commutators nested $k$ deep, but the effect is the same. The roots of a quintic are *not* commutative bookkeepers. There are commutators of commutators of commutators, to any depth, that still move them. At some depth the formula stays put while the roots move, so the formula was never a root.

This is V. I. Arnold's proof, from his 1963 lectures to Moscow high-school students. The rest of this volume makes each sentence of that paragraph precise.

---

# What a formula is

Write the quintic as

$$
p_a(x) = x^5 + a_1x^4 + a_2x^3 + a_3x^2 + a_4x + a_5, \qquad a=(a_1,\ldots,a_5)\in\mathbb{C}^5.
$$

A **radical formula** is an expression built from $a_1,\ldots,a_5$ and complex constants using $+,-,\times,\div$ and $n$th roots $\sqrt[n]{\;\cdot\;}$. Its **depth** is the largest number of radical signs nested inside one another. The quadratic formula has depth $1$, Cardano's cubic formula has depth $2$ (a cube root of something containing a square root), and Ferrari's quartic formula has depth $3$.

A formula is **multivalued**, because each $\sqrt[n]{w}$ with $w\neq 0$ has $n$ values. What we can do is **follow a value continuously**. If the coefficients move along a path $a(t)$, pick one value of the formula at the start and let it move continuously with $t$. This works as long as no radicand passes through $0$ and no denominator vanishes. Near a nonzero $w$, each of the $n$ values of $\sqrt[n]{w}$ moves continuously and uniquely with $w$.

The formula **solves the quintic** if the value we follow is always a root: $p_{a(t)}(\text{value}(t))=0$ for every $t$.

<div class="note">
<p><strong>Fine print, once.</strong> Three things can go wrong along a path: two roots collide, a denominator hits $0$, or a radicand hits $0$. Each happens only on a "bad set" of coefficients cut out by complex equations, which has real codimension $2$ in $\mathbb{C}^5\cong\mathbb{R}^{10}$. A curve can always be nudged off such a set without changing which root goes where, just as a loop in 3-space can be nudged off a line. We fix the formula first, then choose a base point and finitely many building-block loops off the bad set. Every loop below is a concatenation of those blocks, so it avoids the bad set too. Also: a formula that gives a root for all coefficients near the base point keeps giving a root along any path, by analytic continuation. So "the value we follow is always a root" is not an extra assumption.</p>
</div>

---

# Step 1: loops of coefficients permute the roots

Start at coefficients $a$ with five distinct roots $r_1,\ldots,r_5$. Move $a$ around a closed loop $\gamma$ that avoids the bad set. Each root moves continuously, and at the end the polynomial is $p_a$ again, so the roots land on $\{r_1,\ldots,r_5\}$ again, perhaps in a different order. The loop $\gamma$ therefore defines a permutation $\pi(\gamma)\in S_5$.

**Every permutation is achievable.** Run the argument backwards. Choose any continuous motion of five points in the plane that never collide and that ends with the points permuted the way you want: for a swap, rotate $r_1$ and $r_2$ half a turn around their midpoint while the others stay still. Then define

$$
p_{a(t)}(x) = \bigl(x-r_1(t)\bigr)\cdots\bigl(x-r_5(t)\bigr).
$$

By Vieta, each coefficient is a polynomial in the $r_i(t)$, so it moves continuously. At the end the set of roots is the same, so the coefficients return: $a(t)$ is a loop, and it realizes the permutation we chose.

**Loops compose.** Write $\gamma\cdot\delta$ for "go around $\gamma$, then around $\delta$" and $\gamma^{-1}$ for "go around $\gamma$ backwards". Then $\pi(\gamma^{-1})=\pi(\gamma)^{-1}$, and $\pi(\gamma\cdot\delta)=\pi(\delta)\,\pi(\gamma)$, composing right to left: first $\gamma$ acts, then $\delta$. Only the endpoints matter here. What a root does halfway along $\gamma$ is irrelevant once we know where $\gamma$ sends it.

The **commutator** of two loops is

$$
[\gamma,\delta] = \gamma\cdot\delta\cdot\gamma^{-1}\cdot\delta^{-1}.
$$

It is a closed loop. Its permutation is $\pi(\delta)^{-1}\pi(\gamma)^{-1}\pi(\delta)\pi(\gamma)$, which is again a commutator of two permutations.

---

# Step 2: radicals only remember winding numbers

**Depth $0$.** An expression with no radicals is a rational function of the coefficients. It is single-valued, so after *any* loop it returns to its starting value. It cannot solve even a quadratic, because the swap loop of Step 1 sends $r_1$ to $r_2$ while the expression comes back to $r_1$. (This already says something: no root of $x^2+bx+c$ is a rational function of $b$ and $c$. You need a square root.)

**Depth $1$.** Take $\sqrt[n]{R}$ with $R$ a rational function of the coefficients. Along a loop $\gamma$, $R$ traces a closed curve in $\mathbb{C}\setminus\{0\}$ with some **winding number** $w(\gamma)\in\mathbb{Z}$ around $0$. Write $R=\rho e^{i\theta}$ with $\rho$ and $\theta$ varying continuously. The followed value of $\sqrt[n]{R}$ is $\rho^{1/n}e^{i\theta/n}$. At the end, $\rho$ is back where it started and $\theta$ has grown by $2\pi w(\gamma)$, so the root has been multiplied by

$$
e^{2\pi i\,w(\gamma)/n}.
$$

Winding numbers add along concatenation and change sign on reversal. For a commutator,

$$
w\bigl([\gamma,\delta]\bigr) = w(\gamma)+w(\delta)-w(\gamma)-w(\delta) = 0.
$$

So **every value of $\sqrt[n]{R}$ returns to itself after any commutator loop.** Sums, products and quotients of things that return also return. Here is where radicals fail: they can't tell $\gamma\cdot\delta$ from $\delta\cdot\gamma$.

**Every depth.** Define families of loops by

$$
\Gamma_0 = \{\text{all loops}\},\qquad \Gamma_{k+1} = \bigl\{[\gamma,\delta] : \gamma,\delta\in\Gamma_k\bigr\}.
$$

**Claim.** Every value of a formula of depth at most $k$ returns to itself after every loop in $\Gamma_k$.

*Proof, by induction on $k$.* Depth $0$ is done. Suppose the claim holds up to depth $k$. (Note that $\Gamma_k\subseteq\Gamma_{k-1}$ in effect: every loop in $\Gamma_k$ is a concatenation of loops in $\Gamma_{k-1}$ and their reverses.) A depth-$(k+1)$ formula is built by arithmetic from depth-$\le k$ pieces and radicals $\sqrt[n]{R}$ whose radicands $R$ have depth $\le k$. Every loop in $\Gamma_{k+1}$ is a concatenation of loops in $\Gamma_k$ and their reverses. By induction, each of those returns every value of the depth-$\le k$ pieces, so the concatenation does too. That leaves the new radicals. Take $\gamma,\delta\in\Gamma_k$ and follow a value of $R$. By induction it returns after $\gamma$ and after $\delta$. So along $[\gamma,\delta]$ it traces four closed curves in $\mathbb{C}\setminus\{0\}$, and each segment starts from exactly the configuration that $\gamma$ started from. The four windings are $w(\gamma)$, $w(\delta)$, $-w(\gamma)$, $-w(\delta)$, which sum to $0$. So each value of $\sqrt[n]{R}$ returns, exactly as at depth $1$. $\square$

The claim needs only that each building block is continuous and single-valued. So you can add $e^{z}$, $\sin z$, or any other entire function to the toolkit, and the proof goes through unchanged. What it rules out is the combination of arithmetic and roots, not some limitation of polynomials.

---

# Step 3: the roots of a quintic never run out of commutators

Now look at the roots instead. We want, for every $k$, a loop in $\Gamma_k$ whose permutation is *not* the identity. Everything reduces to one identity in $S_5$.

**Lemma.** Every $3$-cycle in $S_5$ is a commutator $aba^{-1}b^{-1}$ of two $3$-cycles $a,b$.

*Proof.* Compose right to left. Take $a=(1\,2\,3)$ and $b=(3\,4\,5)$, so $a^{-1}=(1\,3\,2)$ and $b^{-1}=(3\,5\,4)$. Track each letter through $b^{-1}$, then $a^{-1}$, then $b$, then $a$:

$$
\begin{aligned}
1 &\mapsto 1 \mapsto 3 \mapsto 4 \mapsto 4,\\
4 &\mapsto 3 \mapsto 2 \mapsto 2 \mapsto 3,\\
3 &\mapsto 5 \mapsto 5 \mapsto 3 \mapsto 1,
\end{aligned}
$$

and $2$ and $5$ are fixed. So $aba^{-1}b^{-1}=(1\,4\,3)$. For any other $3$-cycle $c=(x\,y\,z)$, pick $g\in S_5$ with $g(1)=x$, $g(4)=y$, $g(3)=z$. Conjugation relabels cycles, so

$$
(gag^{-1})(gbg^{-1})(gag^{-1})^{-1}(gbg^{-1})^{-1} = g(1\,4\,3)g^{-1} = (x\,y\,z),
$$

and $gag^{-1}$ and $gbg^{-1}$ are again $3$-cycles. $\square$

Notice what the lemma needs: two $3$-cycles that share **exactly one** letter. That takes $3+3-1=5$ letters. With four roots there is no room for it, and this is where degree five first appears.

**Corollary.** For every $k$ and every $3$-cycle $c$, some loop in $\Gamma_k$ has permutation $c$.

*Proof, by induction on $k$.* For $k=0$, Step 1 realizes any permutation. Suppose it holds for $k$. Given $c$, the lemma gives $3$-cycles $a,b$ with $c=aba^{-1}b^{-1}$. By induction there are loops $\gamma,\delta\in\Gamma_k$ with $\pi(\gamma)=b^{-1}$ and $\pi(\delta)=a^{-1}$, since inverses of $3$-cycles are $3$-cycles. By Step 1,

$$
\pi\bigl([\gamma,\delta]\bigr)=\pi(\delta)^{-1}\pi(\gamma)^{-1}\pi(\delta)\pi(\gamma) = a\,b\,a^{-1}\,b^{-1} = c,
$$

and $[\gamma,\delta]\in\Gamma_{k+1}$. $\square$

---

# Step 4: the contradiction

Suppose a radical formula of depth $k$ solves the general quintic. Start at a base point, and follow the value of the formula that equals the root $r_1$. By the corollary, some loop $\gamma\in\Gamma_k$ has permutation $(1\,2\,3)$. Go around it.

- The followed value is always a root and moves continuously, so it rides along with $r_1$ and ends at $r_2$.
- The formula has depth $k$ and $\gamma\in\Gamma_k$, so by Step 2 the followed value returns to $r_1$.

Since $r_1\neq r_2$, both can't happen. There is no such formula.

<div class="note">
<p><strong>Abel–Ruffini (degree 5).</strong> No expression built from the coefficients by $+,-,\times,\div$ and nested $n$th roots gives a root of every quintic $x^5+a_1x^4+\cdots+a_5$.</p>
</div>

For degree $n>5$, the same argument works. The $3$-cycles live on any five of the $n$ roots, and the lemma and corollary apply there unchanged.

---

# Why degrees two, three, and four escape

The same bookkeeping explains the formulas that *do* exist. Let $D_0=S_n$, and let $D_{k+1}$ be the group generated by all commutators of elements of $D_k$. Loops in $\Gamma_k$ produce permutations in $D_k$. The code below iterates the plain *set* of commutators instead, which for these small groups happens to coincide with the group it generates. A brute-force count:

```python
from itertools import permutations

def compose(s, t):                    # s after t
    return tuple(s[i] for i in t)

def inverse(s):
    r = [0] * len(s)
    for i, x in enumerate(s):
        r[x] = i
    return tuple(r)

def commutator(a, b):
    return compose(compose(compose(a, b), inverse(a)), inverse(b))

for n in (2, 3, 4, 5):
    level, sizes = set(permutations(range(n))), []
    while True:
        sizes.append(len(level))
        nxt = {commutator(a, b) for a in level for b in level}
        if nxt == level or len(nxt) == 1:
            sizes.append(len(nxt))
            break
        level = nxt
    print(n, sizes)
```

```
2 [2, 1]
3 [6, 3, 1]
4 [24, 12, 4, 1]
5 [120, 60, 60]
```

For $S_5$, the set of single commutators already has size $60$, so here it equals the group it generates. That group is $A_5$, the even permutations, and its commutators are $A_5$ again. It never shrinks, which is the lemma above seen from a computer.

- **Degree 2:** $S_2\to\{1\}$ in one step. Commutators already fix both roots, so nothing rules out depth $1$, and the quadratic formula has depth $1$.
- **Degree 3:** $S_3\to A_3\to\{1\}$. One layer of commutators still moves the roots, since $[(1\,2),(1\,3)]$ is a $3$-cycle, so no depth-$1$ formula exists. Two layers kill everything. So the formula needs a root inside a root, and Cardano's cube root of a square root is exactly that.
- **Degree 4:** $S_4\to A_4\to V_4\to\{1\}$, where $V_4$ consists of the three double transpositions and the identity. Two $3$-cycles in $S_4$ share at least two letters, and their commutator lands in $V_4$, which is commutative. So the quartic needs depth $3$, which is Ferrari.
- **Degree 5:** $S_5\to A_5\to A_5\to\cdots$ never reaches $\{1\}$.

That chain of groups is the **derived series**, and "reaches $\{1\}$" is the definition of a **solvable group** ([Vol. III](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-III)). The topological proof and the Galois proof are the same obstruction seen from two sides: loops of coefficients here, automorphisms of fields there.

---

# What this proof does not give you

The loop argument rules out a *formula*, meaning a single expression that tracks a root continuously as the coefficients vary. It says nothing about one fixed polynomial with rational coefficients, such as $x^5-6x+3$. A single polynomial has no coefficients to wiggle. For all this proof knows, each individual quintic could have its own private radical expression.

It doesn't. Galois theory proves that $x^5-6x+3$'s roots lie in no radical tower over $\mathbb{Q}$ at all, and says exactly which quintics are solvable ($x^5-2$ is; $x^5-x-1$ is not). That sharper theorem needs fields, and the remaining volumes build it:

| Vol. | Topic | What it contributes |
|---|---|---|
| **I** | The short proof | Loops, winding numbers, commutators: no uniform formula. |
| **[II](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-II)** | Roots exist | The fundamental theorem of algebra: the family of roots Vol. I moves around. |
| **[III](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-III)** | Symmetries of the roots | $S_n$, parity, $A_5$ is simple, $S_5$ is not solvable. |
| **[IV](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-IV)** | Where the roots live | Splitting fields, radical towers, the Galois group. |
| **[V](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-V)** | Towers and the Galois correspondence | Solvable by radicals $\iff$ solvable Galois group. |
| **[VI](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-VI)** | Quintic symmetry | The general quintic and $x^5-6x+3$ have group $S_5$. History and references. |

**Sources for this volume.** V. B. Alekseev, [*Abel's Theorem in Problems and Solutions*](https://link.springer.com/book/10.1007/1-4020-2187-9) (Kluwer, 2004), the write-up of Arnold's lectures. The video [*Short proof that 5th degree polynomial equations cannot be solved*](https://www.youtube.com/watch?v=zeRXVL6qPk4) animates exactly this argument on numerical quintics, and it is the source of the brute-force count. Two Galois-side videos, [*Why you can't solve quintic equations (Galois theory approach)*](https://www.youtube.com/watch?v=zCU9tZ2VkWc) and [*Everything You Ever Wanted To Know About Galois Theory*](https://www.youtube.com/watch?v=eVzIrn7hE4w), are annotated in [Vol. VI](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-VI).

---

**Next:** [Vol. II: Roots Exist](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-II)

*Abel–Ruffini:* **Vol. I** · [Vol. II](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-II) · [Vol. III](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-III) · [Vol. IV](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-IV) · [Vol. V](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-V) · [Vol. VI](/blog/2026/08/22/Abel-Ruffini-Theorem-Vol-VI)
