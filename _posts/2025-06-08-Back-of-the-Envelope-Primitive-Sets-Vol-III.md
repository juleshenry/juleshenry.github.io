---
layout: post
title: "Back-of-the-Envelope: Primitive Sets, Vol. III: Territories and the e^γ Bound"
date: 2025-06-08 12:02:00
categories: number-theory
mathjax: true
---

*Primitive Sets:* [I](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets) · [II](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-II) · **III** · [IV](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-IV) · [V](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-V)

{% include primitive-kit.html %}

*Erdős, 1935: every primitive set has a bounded score. The proof gives each element a private territory of integers, shows that primitivity keeps the territories apart, and lets the size of the number line pay the bill.*

[Vol. II](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-II) built the ruler $f(A) = \sum_{a\in A} 1/(a\log a)$ and showed it sits on a knife-edge: over all integers it diverges. So before asking which primitive set is heaviest, we need to know that every primitive set has a *finite* score, bounded by a constant that does not depend on the set. That is the 1935 theorem, and this volume proves it, modulo one named theorem of Mertens.

<div class="pv-toc">
<strong>Contents</strong>
<ol>
  <li><a href="#a-private-territory-for-each-a">a private territory for each a</a></li>
  <li><a href="#the-territories-do-not-overlap">the territories do not overlap</a></li>
  <li><a href="#the-budget">the budget</a></li>
  <li><a href="#mertens-theorem-and-a-uniform-bound">Mertens' theorem, and a uniform bound</a></li>
  <li><a href="#where-this-goes">where this goes</a></li>
</ol>
</div>

---

# a private territory for each $a$
{: #a-private-territory-for-each-a}

The idea is to give each $a$ in a primitive set a block of integers that nobody else in the set is allowed to claim, then see that the blocks cannot cover more than the whole number line.

The obvious candidate, "all multiples of $a$," is too greedy. The multiples of $6$ and the multiples of $10$ share $30$, $60$, $90, \ldots$ even though $\lbrace 6,10\rbrace$ is primitive. We need a thinner territory: multiples of $a$, but only in a way that remembers $a$ was *first*.

<div class="pv-def"><strong>Definition (L-multiples).</strong> For each integer $a \ge 2$,
$$ L_a \;=\; \bigl\{ a\cdot b \,:\, b \ge 1,\; \text{every prime factor of } b \text{ is at least } P(a) \bigr\}. $$</div>

In words: start with $a$, and multiply by integers built only from primes $\ge$ the largest prime factor of $a$. The letter L alludes to *lexicographic*. Write the prime factorization of $n$ in nondecreasing order. Then $n$ is an L-multiple of $a$ when that factorization *starts with* the factorization of $a$, and continues with primes $\ge P(a)$. Think of $a$ as a *prefix*, and $L_a$ as every word that begins with it.

**Example: $a = 6$.** Here $6 = 2\cdot 3$, so $P(6) = 3$. Then $L_6$ is $6$ times any integer built from primes $\ge 3$:

$$
L_6 \;=\; \{6,\; 18,\; 30,\; 42,\; 54,\; 66,\; 78,\; 90,\; \ldots\}.
$$

Walk through a few membership tests, writing factorizations in nondecreasing order.

- $18 = 2\cdot 3\cdot 3$. This starts with $2\cdot 3$, and the leftover $3$ is $\ge 3$. In $L_6$.
- $12 = 2\cdot 2\cdot 3$. This starts with $2\cdot 2$, not with $2\cdot 3$. Equivalently $12 = 6\cdot 2$ and $2 < 3$. Not in $L_6$.
- $36 = 2\cdot 2\cdot 3\cdot 3$. Starts with $2\cdot 2$, not $2\cdot 3$. And $36 = 6\cdot 6$ with $6 = 2\cdot 3$ carrying a $2 < 3$. Not in $L_6$.
- $90 = 2\cdot 3\cdot 3\cdot 5$. Starts with $2\cdot 3$; leftover $3,5 \ge 3$. In $L_6$.

**Example: a prime $p$.** Here $P(p) = p$, so $L_p$ is $p$ times any integer built from primes $\ge p$. Equivalently: $L_p$ is the set of integers whose *smallest* prime factor is $p$. Thus $L_2$ is the even numbers, $L_3$ is $\lbrace 3, 9, 15, 21, 27, 33, \ldots\rbrace$, $L_5$ is $\lbrace 5, 25, 35, 55, \ldots\rbrace$, and so on. Every integer $n \ge 2$ has a unique smallest prime factor, so the sets $L_p$, as $p$ runs over the primes, split the integers $\ge 2$ into disjoint pieces whose union is everything except $1$. The primes use up the *entire* number line. Hold on to that; it is why they are the natural champion.

## density
{: #density}

Recall from [Vol. I](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets) that the natural density $d(S)$ is the long-run proportion of integers in $S$. The even numbers have density $1/2$. The multiples of $a$ have density $1/a$.

For $L_a$, a number $n$ lies in $L_a$ when $a$ divides $n$ *and* the cofactor $n/a$ is not divisible by any prime smaller than $P(a)$. So we need two things: "multiple of $a$", which has density $1/a$, and "avoids the primes $< P(a)$."

Why is the proportion of integers not divisible by any prime in a list $q_1, \ldots, q_k$ equal to $\prod_i (1-1/q_i)$? For one prime, the proportion not divisible by $2$ is $1-1/2$. For two primes, inclusion-exclusion:

$$
1 - \frac12 - \frac13 + \frac16 \;=\; \frac13 \;=\; \Bigl(1-\frac12\Bigr)\Bigl(1-\frac13\Bigr).
$$

The same pattern continues for any finite list (the sieve of Eratosthenes): the events "divisible by $q$" for distinct primes $q$ multiply, because a number is divisible by $q$ and $q'$ if and only if it is divisible by $qq'$. In probability language, divisibility by distinct primes are *independent events*. Hence

$$
d(L_a) \;=\; \frac{1}{a} \prod_{q < P(a)}\Bigl(1 - \frac{1}{q}\Bigr).
$$

**Check: $a = 6$, by hand.** The only prime $< P(6) = 3$ is $2$, so $d(L_6) = \frac16 \cdot \bigl(1-\frac12\bigr) = \frac1{12}$. Among $1, \ldots, 60$, first take the multiples of $6$:

$$
6,12,18,24,30,36,42,48,54,60.
$$

Now drop those whose cofactor $n/6$ is even (i.e. divisible by a prime $< 3$): $12=6\cdot 2$, $24=6\cdot 4$, $36=6\cdot 6$, $48=6\cdot 8$, $60=6\cdot 10$. What remains is $\lbrace 6, 18, 30, 42, 54\rbrace$, five numbers, and $60/12 = 5$.

**Check: a prime $p$.** Then $d(L_p) = \frac1p \prod_{q < p}(1-1/q)$, which is the proportion of integers with smallest prime factor $p$. For $p = 2$, the product is empty. An empty product equals $1$ (the same way an empty sum equals $0$), so $d(L_2) = 1/2$, matching "the even numbers." For $p=3$: $\frac13\cdot\frac12 = \frac16$, the odd multiples of $3$.

See them. Each chosen generator paints its territory. A cell hit by two territories turns red.

<div class="pv" id="pv-terr" aria-label="Territories L_a painted on the integers 1 to 120">
  <div class="pv-title" id="pv-terr-title"></div>
  <div class="pv-sub" id="pv-terr-sub"></div>
  <svg id="pv-terr-svg" viewBox="0 0 640 312" role="img" aria-label="Grid of the integers 1 to 120 coloured by which territory L_a contains them; click a number to add or remove it as a generator"></svg>
  <div class="pv-read" id="pv-terr-read"></div>
  <div class="pv-ctl">
    <button type="button" data-s="6,10,15">{6, 10, 15}</button>
    <button type="button" data-s="2,3,5,7">{2, 3, 5, 7}</button>
    <button type="button" data-s="4,6,9,10,15,25">Ω = 2 (small)</button>
    <button type="button" data-s="6,18">{6, 18}</button>
    <button type="button" data-s="6,9">{6, 9}</button>
    <button type="button" data-s="">clear</button>
    <span class="pv-key">click any number to toggle it as a generator<b style="background:#e5484d"></b>overlap</span>
  </div>
</div>
<p class="pv-cap">$\lbrace 6,18\rbrace$ is not primitive, and $L_6$ and $L_{18}$ collide at $18$, $54$ and $90$. $\lbrace 6,9\rbrace$ is primitive, yet ordinary multiples would collide at $18$; the L-territories do not, because $18 = 6\cdot 3$ is claimed by $6$, and $18 = 9\cdot 2$ carries a $2\lt P(9)$. The count column compares what you see in $1..120$ with $120\cdot d(L_a)$.</p>
<script>
(function () {
  var root = document.getElementById('pv-terr');
  if (!root || !window.PV) return;
  var svg = document.getElementById('pv-terr-svg'), E = PV.el, C = PV.C;
  var N = 120, COLS = 12, W = 51, H = 29, X0 = 14, Y0 = 8;
  var PAL = ['#3987e5', '#199e70', '#e0a100', '#a855f7', '#d95926', '#38bdf8', '#f472b6', '#84cc16'];
  var gens = [], cells = {};
  for (var n = 1; n <= N; n++) (function (n) {
    var x = X0 + ((n - 1) % COLS) * W, y = Y0 + Math.floor((n - 1) / COLS) * H;
    var g = E('g', { class: n > 1 ? 'pv-hit' : '' }, svg);
    var r = E('rect', { x: x + 2, y: y + 2, width: W - 4, height: H - 4, rx: 4, fill: '#1b1b1b', stroke: '#2c2c2c' }, g);
    var t = PV.text(g, x + W / 2, y + H / 2 + 5, n, { 'text-anchor': 'middle', 'font-size': 13 });
    cells[n] = { r: r, t: t };
    g.addEventListener('click', function () {
      if (n === 1) return;
      var i = gens.indexOf(n);
      if (i >= 0) gens.splice(i, 1); else if (gens.length < 8) gens.push(n);
      gens.sort(function (a, b) { return a - b; });
      draw();
    });
  })(n);
  function dens(a) {
    var Pa = PV.P(a), d = 1 / a;
    PV.primes(Pa).forEach(function (q) { if (q < Pa) d *= 1 - 1 / q; });
    return d;
  }
  function draw() {
    var owner = {}, clash = {}, counts = gens.map(function () { return 0; });
    for (var n = 2; n <= N; n++) {
      gens.forEach(function (a, i) {
        if (PV.inL(n, a)) { counts[i]++; if (owner[n] != null) clash[n] = 1; else owner[n] = i; }
      });
    }
    for (var m = 1; m <= N; m++) {
      var c = cells[m], o = owner[m], isGen = gens.indexOf(m) >= 0;
      var fill = clash[m] ? 'rgba(229,72,77,0.55)' : o != null ? PAL[o % PAL.length] : '#1b1b1b';
      c.r.setAttribute('fill', fill);
      c.r.setAttribute('fill-opacity', clash[m] ? 1 : o != null ? (isGen ? 0.85 : 0.38) : 1);
      c.r.setAttribute('stroke', isGen ? '#f0f0f0' : '#2c2c2c');
      c.r.setAttribute('stroke-width', isGen ? 2 : 1);
      c.t.setAttribute('style', m === 1 ? 'fill:#555' : 'fill:#f0f0f0');
    }
    var prim = true;
    for (var i = 0; i < gens.length; i++) for (var j = i + 1; j < gens.length; j++) if (gens[j] % gens[i] === 0) prim = false;
    var nClash = Object.keys(clash).length, budget = gens.reduce(function (s, a) { return s + dens(a); }, 0);
    document.getElementById('pv-terr-title').textContent = gens.length ? 'A = {' + gens.join(', ') + '}' + (prim ? ' (primitive)' : ' (not primitive)') : 'Choose generators';
    document.getElementById('pv-terr-sub').textContent = !gens.length ? 'Pick a preset or click numbers.' : nClash ? nClash + ' integers in 1..120 are claimed twice: ' + Object.keys(clash).slice(0, 8).join(', ') + (nClash > 8 ? ', …' : '') + '.' : 'No integer is claimed twice. Total density spent: Σ d(L_a) = ' + budget.toFixed(4) + ' ≤ 1.';
    document.getElementById('pv-terr-read').innerHTML = gens.map(function (a, i) {
      return '<span style="color:' + PAL[i % PAL.length] + '">■</span> L<sub>' + a + '</sub>: <b>' + counts[i] + '</b> vs ' + (120 * dens(a)).toFixed(1);
    }).join(' &nbsp; ');
  }
  root.querySelectorAll('[data-s]').forEach(function (b) {
    b.addEventListener('click', function () {
      var s = b.getAttribute('data-s');
      gens = s ? s.split(',').map(Number) : [];
      draw();
    });
  });
  gens = [6, 10, 15];
  draw();
})();
</script>

---

# the territories do not overlap
{: #the-territories-do-not-overlap}

<div class="pv-def"><strong>Disjointness lemma.</strong> If $A$ is primitive, then the sets $L_a$ for $a \in A$ are pairwise disjoint.</div>

In other words: two $L$-sets can meet only if one of the two generators divides the other. Primitivity forbids that, so the territories of a primitive set never share an integer.

Before the proof, a picture of what the lemma is saying. Take $n = 90$. Is $90$ in two different $L$-sets of a primitive pair?

- $90 = 6 \cdot 15$ and $15 = 3\cdot 5$, all of whose primes are $\ge P(6) = 3$. So $90 \in L_6$.
- $90 = 10 \cdot 9$ and $9 = 3^2$, but $3 < P(10) = 5$. So $90 \notin L_{10}$.
- $90 = 18 \cdot 5$ and $5 \ge P(18) = 3$. So $90 \in L_{18}$.

Thus $90 \in L_6 \cap L_{18}$. But $\lbrace 6, 18\rbrace$ is *not* primitive, because $6 \mid 18$. That is the lemma in one direction: if the territories meet, one generator divides the other.

The other direction, a primitive pair whose territories do *not* meet: $\lbrace 6,10\rbrace$. Here $P(6)=3 < 5=P(10)$. Suppose some $n = 6s = 10 s'$ were in both, with every prime of $s$ at least $3$ and every prime of $s'$ at least $5$. Then every prime of $6$ is $\le 3 < 5$, so $6$ shares no prime with $s'$. Euclid's lemma would force $6$ to divide $10$. It does not, so no such $n$ exists.

A same-largest-prime illustration, again not primitive: $\lbrace 9,27\rbrace$. Both have $P=3$, and $27 = 9\cdot 3$ with cofactor $3 \ge 3$, so $27 \in L_9$. The smaller exponent of $3$ divides the larger. That is the second case of the proof.

**Proof.** Suppose $n \in L_a \cap L_{a'}$ with $a \neq a'$ both in $A$. Write $n = a\cdot s = a'\cdot s'$, where every prime factor of $s$ is $\ge P(a)$ and every prime factor of $s'$ is $\ge P(a')$. Swap names if needed so that $P(a) \le P(a')$.

If $s' = 1$, then $n = a'$, so $a$ divides $a'$, contradicting primitivity.

Now suppose $s' > 1$. Every prime factor of $a$ is $\le P(a) \le P(a')$, and every prime factor of $s'$ is $\ge P(a')$.

- If $P(a) < P(a')$, these two ranges of primes do not overlap. So $a$ and $s'$ share no prime factors: $\gcd(a, s') = 1$. But $a$ divides $a s = a' s'$. Euclid's lemma: an integer that divides a product and is coprime to one factor must divide the other, so $a$ divides $a'$. Contradiction.
- If $P(a) = P(a') = p$, write $a = p^{\alpha} m$ and $a' = p^{\beta} m'$ with $p$ dividing neither $m$ nor $m'$. Then $m$ and $m'$ are built from primes $< p$, while $s$ and $s'$ are built from primes $\ge p$. From $p^{\alpha} m s = p^{\beta} m' s'$ we get that $m$ divides $m' s'$. But $m$ shares no primes with $s'$, so Euclid again: $m$ divides $m'$. The same argument the other way gives $m'$ divides $m$. Thus $m = m'$, and $a, a'$ are $p^{\alpha} m$ and $p^{\beta} m$: the one with the smaller exponent divides the other. Contradiction.

So no such $n$ exists. $\blacksquare$

In the prefix language the proof is one line: if two words both begin with prefixes $a$ and $a'$, one prefix is a prefix of the other, and a prefix of a factorization is a divisor. The argument used only finite arithmetic --- unique factorization and Euclid's lemma --- not density, not primes being infinite, nothing. It is the engine of everything that follows.

---

# the budget
{: #the-budget}

Because the $L_a$ are disjoint, they cannot cover more than the whole number line.

<div class="pv-q"><strong>Student.</strong> So just add up the densities and get at most $1$?</div>
<div class="pv-a"><strong>Teacher.</strong> Careful: density is not a measure, and infinitely many densities need not add. Every single integer $\lbrace n\rbrace$ has density $0$, yet the union of all of them is every integer, with density $1$. So "$0+0+0+\cdots = 1$" for densities. We avoid infinite unions entirely.</div>

For any *finite* subcollection of $A$, the corresponding $L_a$ are disjoint, the density of their union is the sum of their densities (finite additivity is fine), and a subset of the integers cannot have density greater than $1$. Every finite partial sum of the $d(L_a)$ is therefore $\le 1$. A series of positive terms whose partial sums are all $\le 1$ converges to something $\le 1$ ([Vol. II](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-II)):

$$
\sum_{a \in A} d(L_a) \;=\; \sum_{a \in A} \frac{1}{a} \prod_{q < P(a)}\Bigl(1 - \frac{1}{q}\Bigr) \;\le\; 1.
$$

This is a **budget**. Each $a \in A$ spends $d(L_a)$ of a total of at most $1$. The primes spend it all: $\sum_p d(L_p) = 1$, because the $L_p$ tile the integers $\ge 2$.

---

# Mertens' theorem, and a uniform bound
{: #mertens-theorem-and-a-uniform-bound}

The budget is in the currency of density. The score $f$ is in the currency $1/(a\log a)$. We need an exchange rate, and it is hiding in the product $\prod_{q < P(a)}(1-1/q)$. How large is it? A heuristic first, then the named theorem.

Taking logarithms, $\prod_{p \le x}(1-1/p) \approx \exp\bigl(-\sum_{p \le x} 1/p\bigr)$, because $\log(1-1/p) \approx -1/p$ for large $p$. The sum of reciprocals of primes up to $x$ grows like $\log\log x$ (one logarithm slower than the harmonic series, because the primes are about $1/\log t$ dense; see the exercise at the end of [Vol. II](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-II)). So the product is about

$$
\exp\bigl(-\log\log x\bigr) \;=\; \frac{1}{\log x}.
$$

The constant that makes the $\sim$ true, rather than just "about," is $e^{-\gamma}$. Here $\gamma = 0.57721\ldots$ is the Euler–Mascheroni constant

$$
\gamma \;=\; \lim_{N \to \infty} \Bigl( \sum_{n=1}^{N} \frac{1}{n} - \log N \Bigr),
$$

and $e^{\gamma} \approx 1.781$. Mertens proved in 1874 that

$$
\prod_{q \le x} \Bigl(1 - \frac{1}{q}\Bigr) \;\sim\; \frac{e^{-\gamma}}{\log x}.
$$

The harmonic sum and $\log N$ differ by $\gamma$ in the limit; Mertens is the prime-sieve version of that gap. We take the theorem as a named fact. Numerically it is already close by $x=100$:

| $x$ | $\prod_{p\le x}(1-1/p)$ | $e^{-\gamma}/\log x$ |
|-----|-------------------------|----------------------|
| $10$ | $0.229$ | $0.244$ |
| $100$ | $0.120$ | $0.122$ |
| $1000$ | $0.0810$ | $0.0813$ |

![Mertens' product versus $e^{-\gamma}/\log x$](/blog/assets/2025/primitivos/mertens.png)

Apply this with $x = P(a)$. The off-by-one between "primes $< P(a)$" and "primes $\le P(a)$" is absorbed in the $\sim$, and we get

$$
d(L_a) \;\sim\; \frac{e^{-\gamma}}{a \log P(a)},
$$

or, rearranged,

$$
\frac{1}{a \log P(a)} \;\sim\; e^{\gamma}\, d(L_a).
$$

That is the exchange rate: **one unit of density buys about $e^\gamma$ units of score**, provided you are scoring with $\log P(a)$ in place of $\log a$. Always $P(a) \le a$, so $\log P(a) \le \log a$, so $1/(a\log a) \le 1/(a\log P(a))$. Combining,

$$
\frac{1}{a\log a} \;\le\; \frac{1}{a\log P(a)} \;\approx\; e^{\gamma}\, d(L_a).
$$

Sum over $A$ and use the budget:

$$
f(A) \;\approx\text{at most}\; e^{\gamma} \sum_{a \in A} d(L_a) \;\le\; e^{\gamma} \cdot 1 \;=\; e^{\gamma} \approx 1.781.
$$

Lichtman and Pomerance (2019) turn the $\approx$ into a strict inequality $f(A) < e^{\gamma}$. Two ingredients: explicit numerical bounds on Mertens' product in place of the $\sim$, and the fact that a composite $a$ satisfies $a \ge 2P(a)$, hence $\log a \ge \log P(a) + \log 2$. (Equality holds for $a=4$ and for every $a=2p$; the strictness of $f(A)<e^{\gamma}$ comes from the explicit Mertens bounds as well as from this gap when it is present.)

<div class="pv-def"><strong>Theorem (Erdős 1935; Lichtman–Pomerance 2019).</strong> For every primitive set $A$, $f(A) < e^{\gamma} = 1.781\ldots$</div>

The primes score $1.6366$. The bound $1.781$ is about $9\%$ too large. That gap is the remaining problem.

<details class="pv-ex"><summary><strong>Check yourself.</strong> The primes spend the whole budget, $\sum_p d(L_p)=1$. So why do they score only $1.6366$ and not $e^\gamma$?</summary>
<p>Because Mertens is an asymptotic, and small primes dominate the score. For $p = 2$ the exchange rate is exactly $f(2)/d(L_2) = 0.7213/0.5 = 1.443 = 1/\log 2$, well below $e^\gamma \approx 1.781$. For $p=3$ it is $0.3034/(1/6) = 1.820$, slightly above. Only as $p\to\infty$ does the rate settle at $e^\gamma$. The primes' total is a weighted average of these rates, and the heavy weight on $2$ drags it down.</p>
</details>

Look back at the inequality $1/(a\log a) \le 1/(a\log P(a))$. This is an **equality** when $a$ is prime ($P(a) = a$), and a **loss** when $a$ is composite ($P(a) < a$). The 1935 argument treats every integer as if it were a prime. Lichtman's idea is to charge composites for that loss --- and to prove they cannot dodge the charge by clustering just below the primes.

---

# where this goes
{: #where-this-goes}

Three things to carry forward:

1. **Territories.** $L_a$ is $a$ followed by primes $\ge P(a)$, with density $d(L_a) = \frac1a\prod_{q\lt P(a)}(1-1/q)$. The $L_p$ are "smallest prime factor $p$" and tile the integers.
2. **The budget.** Primitive means disjoint territories, so $\sum_{a\in A} d(L_a) \le 1$. And if every $a$ lies inside some bigger territory $L_n$, the same argument gives $\sum d(L_a) \le d(L_n)$: a *local* budget.
3. **The exchange rate.** Mertens: density buys score at rate about $e^\gamma$ for primes, and at rate $e^\gamma \cdot \log P(a)/\log a$ for composites. The 1935 argument ignores that discount.

[Vol. IV](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-IV) stops competing globally and competes slot by slot, prime by prime, using the local budget. It then puts a number on the composite discount, and proves that the composites which barely pay it cannot come in crowds.

---

**Next:** [Vol. IV: Slots and the $\sqrt v$ Packing](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-IV)

*Primitive Sets:* [Vol. I](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets) · [Vol. II](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-II) · **Vol. III** · [Vol. IV](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-IV) · [Vol. V](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-V)
