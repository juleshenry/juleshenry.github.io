---
layout: post
title: "Back-of-the-Envelope: Primitive Sets, Vol. IV: Slots and the √v Packing"
date: 2025-06-08 12:03:00
categories: number-theory
mathjax: true
---

*Primitive Sets:* [Vol. I](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets) · [Vol. II](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-II) · [Vol. III](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-III) · **Vol. IV** · [Vol. V](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-V)

{% include primitive-kit.html %}

*The $e^\gamma$ bound treats every integer as a prime. This volume splits the contest into one slot per prime, measures how much a composite loses by not being prime, and proves that the composites which lose least cannot come in crowds.*

[Vol. III](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-III) proved $f(A) < e^\gamma \approx 1.781$ for every primitive set, against $f(\mathcal{P}) = 1.6366$ for the primes. It ended with a diagnosis: the argument charges a composite $a$ as if it were a prime, by replacing $\log a$ with $\log P(a)$. Closing the last $9\%$ means putting that charge back, and showing composites cannot evade it.

<div class="pv-toc">
<strong>Contents</strong>
<ol>
  <li><a href="#compete-slot-by-slot">compete slot by slot</a></li>
  <li><a href="#the-criterion-that-almost-works">the criterion that almost works</a></li>
  <li><a href="#how-close-to-prime">how close to prime?</a></li>
  <li><a href="#copies-and-the-sqrtv-packing">copies, and the √v packing</a></li>
  <li><a href="#where-this-goes">where this goes</a></li>
</ol>
</div>

---

# compete slot by slot
{: #compete-slot-by-slot}

The weight is front-loaded:

$$
f(2) = 0.721, \qquad f(3) = 0.303, \qquad f(5) = 0.124, \qquad f(6) = 0.093.
$$

If you put $6$ in a primitive set, you cannot also put $2$ or $3$. Starting from the primes and making that trade produces the primitive set $\lbrace 6\rbrace \cup \lbrace p : p \neq 2, 3\rbrace$, with score

$$
f(\mathcal{P}) - f(2) - f(3) + f(6) \;=\; f(\mathcal{P}) - 0.932.
$$

You sold the two heaviest elements in the store for pocket change. Any one-for-one substitution of a composite $a$ for the primes dividing $a$ looks like a bad deal. The conjecture says there is no clever *infinite* combination of such trades that comes out ahead.

The right way to organise the comparison is not globally but **slot by slot**. Every integer $a > 1$ has a smallest prime factor $p(a)$. Split any set $A$ by that prime:

$$
A_p \;=\; \{ a \in A : p(a) = p \}, \qquad A \;=\; \text{the disjoint union of the } A_p.
$$

More generally, for any integer $n\ge 2$ write $A_n := A \cap L_n$. When $n=p$ is prime this recovers the slot above, because $L_p$ is exactly the integers whose smallest prime factor is $p$ ([Vol. III](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-III)). Then $f(A) = \sum_p f(A_p)$, because the blocks $A_p$ do not overlap. The conjecture would follow if, for every prime $p$ and every primitive $A$,

$$
f(A_p) \;\le\; f(p) \;=\; \frac{1}{p\log p}.
$$

Simply: in the slot of numbers whose smallest prime factor is $p$, the single best choice is to take $\lbrace p\rbrace$ itself, not a primitive bunch of composites all divisible by $p$.

<div class="pv-def"><strong>Definition (Erdős-strong).</strong> A prime $p$ is <em>Erdős-strong</em> if $f(A_p) \le f(p)$ for every primitive set $A$. If every prime is Erdős-strong, summing over $p$ gives $f(A)\le f(\mathcal{P})$.</div>

The slot decomposition is the *local* version of the problem. Each prime $p$ faces its own challengers, all living in $L_p$, and they are constrained by the local budget from [Vol. III](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-III): $\sum_{a\in A_p} d(L_a) \le d(L_p)$.

A concrete odd slot, before any asymptotic. The slot $p=5$ consists of integers whose smallest prime factor is $5$. The triple $\lbrace 25, 35, 55\rbrace$ lives there (check: $5^2$, $5\cdot 7$, $5\cdot 11$, and none divides another):

$$
f(25)+f(35)+f(55) \;\approx\; 0.0124+0.0080+0.0045 \;=\; 0.025,
$$

against $f(5)\approx 0.124$. The slot $p=3$, skipping $3$ itself and taking $\lbrace 9,15,21,33\rbrace$:

$$
f(9)+f(15)+f(21)+f(33) \;\approx\; 0.0506+0.0246+0.0156+0.0087 \;=\; 0.099,
$$

against $f(3)\approx 0.303$. Any finite bunch of composites in an odd slot is a rout. The work is to prove that no infinite primitive combination in that slot can catch up.

---

# the criterion that almost works
{: #the-criterion-that-almost-works}

Here is a sufficient condition, from the 2019 bound. For $a \in A_p$ one has $p(a) = p$, so $a \in L_p$, and therefore $L_a \subset L_p$. By disjointness, $\sum_{a \in A_p} d(L_a) \le d(L_p)$. Combining with $f(a) \approx\text{at most } e^{\gamma}\, d(L_a)$,

$$
f(A_p) \;\approx\text{at most}\; e^{\gamma}\, d(L_p) \;=\; e^{\gamma} \cdot \frac{1}{p} \prod_{q < p}\Bigl(1 - \frac{1}{q}\Bigr).
$$

We want this $\le 1/(p\log p)$. Cancel $1/p$: it is enough that

$$
e^{\gamma} \prod_{q < p}\Bigl(1 - \frac{1}{q}\Bigr) \;\le\; \frac{1}{\log p}. \tag{$\star$}
$$

Mertens says the two sides of $(\star)$ are *asymptotically equal*. Direct computation shows that $(\star)$ holds for the first $10^8$ odd primes. For $p = 3$ it is already tight: the left side is $\approx 0.891$ and the right side is $1/\log 3 \approx 0.910$.

It **fails for $p = 2$**. The product over primes $q < 2$ is empty, hence equals $1$, and

$$
e^{\gamma} \approx 1.781 \qquad\text{while}\qquad \frac{1}{\log 2} \approx 1.443.
$$

Worse: even among odd primes, $(\star)$ is not a theorem. It fails for infinitely many primes, unconditionally. On the Riemann hypothesis it fails for a positive proportion of them (in log-density). The strategy "prove every prime is Erdős-strong via $(\star)$" cannot finish the conjecture. That is why the problem sat open.

<div class="pv-q"><strong>Student.</strong> If $(\star)$ fails for infinitely many primes, why doesn't the conjecture fail there too?</div>
<div class="pv-a"><strong>Teacher.</strong> Because $(\star)$ is what you get when you pretend the composites in the slot convert density into score at the full prime rate $e^\gamma$. They don't. $(\star)$ fails by a hair, a Mertens wobble of relative size tending to $0$. If we can prove composites convert at, say, $79\%$ of the prime rate, the hair is irrelevant. The rest of this volume and the next one earn that $79\%$.</div>

---

# how close to prime?
{: #how-close-to-prime}

The loss in the 1935 argument, for a single $a$, is the ratio $\log P(a)/\log a \le 1$. Give it a name.

<div class="pv-def"><strong>Definition (distance from prime).</strong> For an integer $a\ge 2$,
$$ v(a) \;=\; \frac{\log a}{\log P(a)} - 1 \;\ge\; 0. $$</div>

Then $v(a) = 0$ if and only if $P(a) = a$, if and only if $a$ is prime. Equivalently $a = P(a)^{1+v(a)}$: $v$ counts how many extra log-factors of $P(a)$ fit into $a$. For a prime power $p^k$ one has $v(p^k)=k-1$. Rearranging the definition,

$$
\frac{1}{a\log a} \;=\; \frac{1}{1+v(a)}\cdot \frac{1}{a\log P(a)} \;\approx\; \frac{e^{\gamma}}{1+v(a)}\, d(L_a).
$$

So $v(a)$ is the discount at which $a$ converts density into $f$-weight. Primes convert at full rate $e^{\gamma}$. A composite converts at rate $e^{\gamma}/(1+v(a))$.

Worked example: $a = 15 = 3\cdot 5$. Then $P(15) = 5$, and

$$
v(15) \;=\; \frac{\log 15}{\log 5} - 1 \;=\; \frac{2.708}{1.609} - 1 \;\approx\; 0.683, \qquad \frac{1}{1+v(15)} \;\approx\; 0.594.
$$

| $a$ | factorization | $P(a)$ | $v(a)$ | conversion $1/(1+v)$ |
|-----|----------------|--------|--------|----------------------|
| $7$ | $7$ | $7$ | $0$ | $1$ |
| $14$ | $2\cdot 7$ | $7$ | $0.356$ | $0.738$ |
| $22$ | $2\cdot 11$ | $11$ | $0.289$ | $0.776$ |
| $15$ | $3\cdot 5$ | $5$ | $0.683$ | $0.594$ |
| $6$ | $2\cdot 3$ | $3$ | $0.631$ | $0.613$ |
| $9$ | $3^2$ | $3$ | $1$ | $1/2$ |
| $8$ | $2^3$ | $2$ | $2$ | $1/3$ |
| $221$ | $13\cdot 17$ | $17$ | $0.905$ | $0.525$ |

Read the table against the 1935 loss. The **dangerous** composites are those with *small* $v$: a large prime times a small factor. For $a = 2p$,

$$
v(2p) \;=\; \frac{\log 2}{\log p} \;\longrightarrow\; 0 \quad\text{as } p \to \infty.
$$

So $2p$ looks almost like a prime to the 1935 bound: $P(2p) = p$ is a little more than half of $2p$, and the conversion rate tends to $1$. Numbers such as $9$ and $13\cdot 17$ are *very* composite in this sense ($P(a)^2 \approx a$, so $v \approx 1$) and convert at half rate or worse. They are no threat: even if they spent the whole density budget they would score at most $e^{\gamma}/2 \approx 0.89$, well below $f(\mathcal{P})$.

Lichtman's outline says the same thing in the other direction: the 1935 argument already saves a lot when $P(a)^2 < a$. The **critical case** is a composite with $P(a)$ close to $a$ in size --- a large prime with a small factor stuck on.

The remaining question: can a primitive set contain *many* dangerous (small-$v$) composites in the same slot? If it can fill the whole density of $L_p$ with $v \approx 0.01$ composites, the 1935 bound barely improves and $(\star)$ is still the bottleneck. If it cannot, we win.

<details class="pv-ex"><summary><strong>Check yourself.</strong> Which is more dangerous to the prime $3$: the composite $3\cdot 101$ or $3 \cdot 7$? Compute both $v$.</summary>
<p>$v(303) = \log 3/\log 101 \approx 0.238$, conversion $\approx 0.808$. $v(21) = \log 3/\log 7 \approx 0.565$, conversion $\approx 0.639$. The one with the bigger large prime is closer to prime, and more dangerous. In general $v(qp) = \log q/\log p$ for primes $q\lt p$: small cofactor, large prime, small $v$.</p>
</details>

---

# copies, and the $\sqrt{v}$ packing
{: #copies-and-the-sqrtv-packing}

A baby version of the idea. Suppose you have some disjoint subsets of the integers, of total density $D$, and suppose you can also fit a second family of disjoint copies of those subsets, still disjoint from the first family. Then $2D \le 1$, so $D \le 1/2$. More copies, smaller $D$. If each set comes with copies of total density $K$ times its own, all disjoint and all inside a region of density $R$, then $K\cdot D \le R$, so $D\le R/K$.

Lichtman produces many copies of each $L_a$, indexed by extra multipliers $c$, provided every $a$ in the set is uniformly $v$-close to being prime --- that is, $P(a)^{1+v} > a$, or equivalently $v(a) < v$. The copies live *inside* the ambient territory $L_n$ of the slot (for instance $L_p$ when we are competing with a prime $p$). That is the true statement, and it is local:

<div class="pv-def"><strong>Proposition (Lichtman).</strong> Let $A$ be primitive, let $n \notin A$, and suppose $P(a)^{1+v} > a$ for every $a$ in the slot $A_n = A \cap L_n$. Then
$$ \sum_{a \in A_n} d(L_a) \;\le\; \sqrt{v}\cdot\bigl(1+o(1)\bigr)\cdot d(L_n). $$</div>

For $v < 1$ this is strictly better than the trivial budget $\sum d(L_a) \le d(L_n)$. At $v = 1/4$ you may spend at most about half the slot; at $v = 1/100$, at most about a tenth. **A primitive set cannot fill a slot with numbers that are all nearly prime.**

Where does $\sqrt{v}$ come from? For each $a$, let $a^* = a/P(a)$ (so $a^*$ is $a$ with its largest prime stripped off), and let $Q = P(a^*)$ be the second-largest prime factor of $a$. The extra multipliers $c$ are the integers --- including $c = 1$ --- whose prime factors all lie in a window

$$
\bigl[Q,\; Q^{1/\sqrt{v}}\bigr).
$$

The one genuinely hard lemma in the paper, which we will not prove, is that the sets $L_{ac}$ ranging over $a \in A_n$ and over such $c$ remain pairwise disjoint, and all sit inside $L_n$, as long as $A$ is primitive and uniformly $v$-close. Primitivity is essential: the weaker "no one is an L-multiple of another" is enough for ordinary disjointness of the $L_a$, but not for the copies. (That is why the $e^{\gamma}$ bound is essentially sharp for that weaker class, while primitive sets can be pushed down to $f(\mathcal{P})$.) Everything after this lemma is Euler products, Mertens, and calculus.

Granting disjointness of the copies, their densities add, and cannot exceed $d(L_n)$. For each fixed $a$, the copy $L_{ac}$ is just $L_a$ scaled by $c$, so $d(L_{ac}) = d(L_a)/c$. The total copy-density attached to one $a$ is therefore $d(L_a)$ times $\sum 1/c$.

That sum is an Euler product. Unique factorization says every such $c$ is a product of primes from the window, so

$$
\sum_c \frac{1}{c} \;=\; \prod_{Q \le q < Q^{1/\sqrt{v}}} \Bigl(1 + \frac{1}{q} + \frac{1}{q^2} + \cdots\Bigr) \;=\; \prod_{Q \le q < Q^{1/\sqrt{v}}} \Bigl(1 - \frac{1}{q}\Bigr)^{-1},
$$

using the geometric series $1 + x + x^2 + \cdots = 1/(1-x)$ with $x = 1/q$. Mertens says $\prod_{q < x} (1-1/q)^{-1} \sim e^{\gamma} \log x$, so a product over a *range* is a **ratio of logarithms** (the $e^{\gamma}$ cancels):

$$
\frac{\log\bigl(Q^{1/\sqrt{v}}\bigr)}{\log Q} \;=\; \frac{1}{\sqrt{v}}.
$$

**A fully numerical window.** Take $a = 11\cdot 14653 = 161183$, a prime $14653 \approx 11^4$ with the small factor $11$ stuck on. Then

$$
v(a) \;=\; \frac{\log 11}{\log 14653} \;\approx\; 0.250, \qquad \sqrt v \approx 0.500, \qquad Q = 11, \qquad \bigl[Q, Q^{1/\sqrt v}\bigr) \approx [11,\, 121).
$$

The window holds the $26$ primes $11, 13, 17, \ldots, 113$, and the Euler product over them is

$$
\prod_{11\le q\lt 121}\Bigl(1-\frac1q\Bigr)^{-1} \;\approx\; 1.992, \qquad\text{against}\qquad \frac{1}{\sqrt v} \;\approx\; 2.000.
$$

So each such $L_a$ drags along about twice its own density in copies, and a slot of such numbers can spend at most about half its ambient density. The ratio of logarithms is an asymptotic statement, good when $Q$ is not tiny. At $Q = 2$ (the numbers $2p$) the window $[2, 2^{1/\sqrt v})$ holds only one or two primes and the Mertens estimate is off, which is one reason the paper treats the smallest primes with explicit numerics. Try it:

<div class="pv" id="pv-win" aria-label="The prime window from Q to Q to the power 1 over root v, and its Euler product">
  <div class="pv-title" id="pv-win-title"></div>
  <div class="pv-sub" id="pv-win-sub"></div>
  <svg id="pv-win-svg" viewBox="0 0 640 250" role="img" aria-label="Primes in the window on a log axis, and bars comparing the Euler product with 1 over root v"></svg>
  <div class="pv-read" id="pv-win-read"></div>
  <div class="pv-ctl">
    <label>Q <select id="pv-win-q"><option>2</option><option>3</option><option>5</option><option>11</option><option>31</option><option>101</option><option>1009</option></select></label>
    <label>v <input type="range" id="pv-win-v" min="5" max="100" value="25"></label>
    <span class="pv-key"><b style="background:#3987e5"></b>Euler product Σ 1/c<b style="background:#e0a100"></b>Mertens: 1/√v</span>
  </div>
</div>
<p class="pv-cap">Each tick is a prime in the window $[Q, Q^{1/\sqrt v})$ on a logarithmic axis. The Euler product (blue) is the exact copy multiplier; the gold bar is the Mertens prediction $1/\sqrt v$. For $Q\ge 11$ they agree to within a few percent; for $Q=2$ they do not. The packing cap on the slot is the reciprocal.</p>
<script>
(function () {
  var root = document.getElementById('pv-win');
  if (!root || !window.PV) return;
  var svg = document.getElementById('pv-win-svg'), E = PV.el, C = PV.C;
  var LIM = 4000000, sieve = null;
  function isP(n) {
    if (!sieve) {
      sieve = new Uint8Array(LIM + 1); sieve[0] = sieve[1] = 1;
      for (var i = 2; i * i <= LIM; i++) if (!sieve[i]) for (var j = i * i; j <= LIM; j += i) sieve[j] = 1;
    }
    return !sieve[n];
  }
  var qSel = document.getElementById('pv-win-q'), vIn = document.getElementById('pv-win-v');
  qSel.value = '11';
  var gAx = E('g', {}, svg), gT = E('g', {}, svg), gB = E('g', {}, svg);
  function draw() {
    var Q = +qSel.value || 11, v = Math.max(+vIn.value || 25, 5) / 100, sv = Math.sqrt(v), top = Math.pow(Q, 1 / sv);
    var ok = top <= LIM, prod = 1, cnt = 0, ps = [];
    if (ok) for (var q = Q; q < top; q++) if (isP(q)) { prod /= 1 - 1 / q; cnt++; if (ps.length < 4000) ps.push(q); }
    PV.clear(gAx); PV.clear(gT); PV.clear(gB);
    var X0 = 40, X1 = 600, Y = 70;
    var lx = function (x) { return X0 + (Math.log(x) - Math.log(Q)) / Math.max(Math.log(top) - Math.log(Q), 1e-9) * (X1 - X0); };
    E('line', { x1: X0, x2: X1, y1: Y, y2: Y, stroke: '#555', 'stroke-width': 1.5 }, gAx);
    PV.text(gAx, X0, Y + 24, 'Q = ' + Q, { 'text-anchor': 'middle', 'font-size': 13, style: 'fill:#c3c2b7' });
    PV.text(gAx, X1, Y + 24, 'Q^(1/√v) ≈ ' + (top < 1e6 ? top.toFixed(top < 100 ? 2 : 0) : top.toExponential(2)), { 'text-anchor': 'middle', 'font-size': 13, style: 'fill:#c3c2b7' });
    PV.text(gAx, (X0 + X1) / 2, 22, ok ? cnt + ' primes in the window (log scale)' : 'window too wide to list here; Mertens estimate only', { 'text-anchor': 'middle', 'font-size': 13, style: 'fill:#c3c2b7' });
    ps.forEach(function (q) { E('line', { x1: lx(q), x2: lx(q), y1: Y - 16, y2: Y + 4, stroke: C.blue, 'stroke-width': ps.length > 300 ? 0.6 : 1.8, 'stroke-opacity': 0.9 }, gT); });
    var BX = 170, BW = 380, BY = 130, BH = 30, vmax = Math.max(1 / sv, ok ? prod : 0, 1) * 1.08;
    function bar(y, val, col, lab) {
      E('rect', { x: BX, y: y, width: BW * val / vmax, height: BH, fill: col, 'fill-opacity': 0.75, rx: 3 }, gB);
      PV.text(gB, BX - 10, y + BH / 2 + 5, lab, { 'text-anchor': 'end', 'font-size': 13, style: 'fill:#c3c2b7' });
      PV.text(gB, BX + BW * val / vmax + 8, y + BH / 2 + 5, val.toFixed(3), { 'font-size': 13 });
    }
    if (ok) bar(BY, prod, C.blue, 'Σ 1/c = ∏(1−1/q)⁻¹');
    bar(BY + 46, 1 / sv, C.gold, '1/√v');
    document.getElementById('pv-win-title').textContent = 'Q = ' + Q + ', v = ' + v.toFixed(2);
    document.getElementById('pv-win-sub').textContent = 'Composites with second-largest prime Q and distance-from-prime below v get copies indexed by the window primes. Conversion rate 1/(1+v) = ' + (1 / (1 + v)).toFixed(3) + '.';
    document.getElementById('pv-win-read').innerHTML = (ok ? 'copy multiplier <b>' + prod.toFixed(3) + '</b> (' + (100 * (prod * sv - 1)).toFixed(1) + '% from Mertens) &nbsp; ' : '') + 'packing cap √v ≈ <b>' + sv.toFixed(3) + '</b> of the slot';
  }
  qSel.addEventListener('change', draw);
  vIn.addEventListener('input', draw);
  draw();
})();
</script>

Each original $L_a$ therefore comes with about $1/\sqrt{v}$ times as much copy-density. All of those copies still sit inside $L_n$, so

$$
\frac{1}{\sqrt{v}} \sum_{a \in A_n} d(L_a) \;\lesssim\; d(L_n) \qquad\Longrightarrow\qquad \sum_{a \in A_n} d(L_a) \;\lesssim\; \sqrt{v}\; d(L_n).
$$

The exponent $1/\sqrt{v}$ on the window is the largest Lichtman could take and still prove the copies disjoint. A larger window would improve $\sqrt{v}$ to a smaller power of $v$, and would improve the $\pi/4$ in [Vol. V](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-V).

When $v$ is small --- the dangerous $2p$ numbers --- the window $Q^{1/\sqrt{v}}$ is *large*, so there are many copies, so the original density is forced to be *small*. That is the packing constraint biting exactly on the critical case.

---

# where this goes
{: #where-this-goes}

Inside one slot $A_n$ of composites we now hold two opposing facts, both functions of the distance from prime $v$:

- **Conversion.** An element at level $v$ turns density into score at rate about $e^{\gamma}/(1+v)$. Small $v$ is valuable.
- **Packing.** All the elements with $v(a) < v$ together spend at most about $\sqrt{v}$ of the ambient density $d(L_n)$. Small $v$ is scarce.

A challenger wants cheap, nearly-prime composites, and there are not many of them. [Vol. V](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-V) plays the two facts against each other, finds the best possible challenger, and discovers that its score is a quarter-turn: $\pi/4$ of the prime's.

---

**Next:** [Vol. V: The Quarter-Turn](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-V)

*Primitive Sets:* [Vol. I](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets) · [Vol. II](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-II) · [Vol. III](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-III) · **Vol. IV** · [Vol. V](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-V)
