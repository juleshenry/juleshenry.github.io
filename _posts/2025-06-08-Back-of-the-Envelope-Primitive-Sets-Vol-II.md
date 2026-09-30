---
layout: post
title: "Back-of-the-Envelope: Primitive Sets, Vol. II: The Erdős Sum"
date: 2025-06-08 12:01:00
categories: number-theory
mathjax: true
---

*Primitive Sets:* [Vol. I](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets) · **Vol. II** · [Vol. III](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-III) · [Vol. IV](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-IV) · [Vol. V](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-V)

{% include primitive-kit.html %}

*To rank infinite sets we weigh each element and add. This volume builds the weight $1/(a\log a)$, explains why it is the only sensible choice, and computes the score to beat: $f(\mathcal{P}) = 1.6366\ldots$*

[Vol. I](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets) ended with a wish list for a ruler: notice small integers more than large ones, stay finite on infinite sets, and be exactly harsh enough that primitivity is what keeps the score bounded. Every item on that list is a statement about infinite sums, so we start there.

<div class="pv-toc">
<strong>Contents</strong>
<ol>
  <li><a href="#infinite-sums">infinite sums</a></li>
  <li><a href="#the-scale-fa">the scale f(A)</a></li>
  <li><a href="#why-this-weight">why this weight?</a></li>
  <li><a href="#why-fp-is-finite">why f(𝒫) is finite</a></li>
  <li><a href="#where-this-goes">where this goes</a></li>
</ol>
</div>

---

# infinite sums
{: #infinite-sums}

We will compare primitive sets by adding infinitely many positive numbers. Two facts from calculus, and two applications, are the entire analytic toolkit.

A series of *positive* terms has only two possible fates. Its partial sums increase, so either they stay below some fixed number (and then they settle to a limit: the series **converges**), or they do not (and then they grow past every bound: the series **diverges**, and we write $\sum = \infty$). There is no oscillation to worry about. That is why every sum in this series can be manipulated freely: rearranged, grouped, split into pieces.

**The harmonic series diverges.** Group the terms of $\sum 1/n$ into blocks whose lengths are powers of two:

$$
1 + \frac12 + \underbrace{\Bigl(\frac13+\frac14\Bigr)}_{\ge \frac12} + \underbrace{\Bigl(\frac15+\cdots+\frac18\Bigr)}_{\ge \frac12} + \underbrace{\Bigl(\frac19+\cdots+\frac1{16}\Bigr)}_{\ge \frac12} + \cdots.
$$

There are infinitely many blocks, each at least $1/2$, so the sum is infinite. We write $\sum 1/n = \infty$. It diverges *slowly*: the first $N$ terms add up to about $\log N$.

**The integral test.** If $g(x)$ is positive and decreasing, the series $\sum_{n \ge N} g(n)$ and the integral $\int_N^\infty g(x)\,dx$ either both settle to a finite number or both run off to infinity. The picture is that the sum is a staircase of rectangles of height $g(n)$ and width $1$, and the integral is the area under the curve. The curve sits under the staircase starting at $N$ and over the staircase starting at $N+1$, so they sandwich each other.

Two integrals we will use. Substitute $u = \log x$, so $du = dx/x$:

$$
\int_3^{\infty} \frac{dx}{x\log x} \;=\; \int_{\log 3}^{\infty} \frac{du}{u} \;=\; \infty,
$$

$$
\int_3^{\infty} \frac{dx}{x(\log x)^2} \;=\; \int_{\log 3}^{\infty} \frac{du}{u^2} \;=\; \frac{1}{\log 3} \;<\; \infty.
$$

So $\sum 1/(n\log n)$ diverges, and $\sum 1/(n(\log n)^2)$ converges. One extra $\log$ in the denominator is the difference between "infinite" and "finite." That borderline is where the whole subject lives.

Notice *how slowly* $\sum 1/(n\log n)$ diverges: its partial sum up to $x$ is about $\log\log x$. At $x = 10^{100}$, $\log\log x \approx 5.4$. You would never see it diverge on a computer. Proofs, not experiments, decide convergence at this borderline.

A word on notation: we write $g(x) \sim h(x)$ to mean $g(x)/h(x) \to 1$ as $x \to \infty$. The two sides become indistinguishable as a percentage, even if they still differ by a large number. So $x^2 + x \sim x^2$, although the difference $x$ grows without bound.

---

# the scale $f(A)$
{: #the-scale-fa}

<div class="pv-def"><strong>Definition (the Erdős sum).</strong> For a set $A$ of integers greater than $1$,
$$ f(A) \;=\; \sum_{a \in A} \frac{1}{a \log a}. $$
We also write $f(a) = 1/(a\log a)$ for a single integer.</div>

Each integer $a$ is given a positive weight that gets smaller as $a$ gets larger, but slowly. (Reminder: $\log$ is $\ln$, so $\log 6 \approx 1.792$, not $\log_{10} 6$.)

<div class="pv-q"><strong>Student.</strong> Why the natural log? Would base $10$ change the answer?</div>
<div class="pv-a"><strong>Teacher.</strong> No. $\log_{10} a = \log a / \log 10$, so switching base multiplies every weight, and therefore every $f(A)$, by the same constant $\log 10$. Rankings do not change, and the theorem "the primes are heaviest" is true in every base. The numbers $1.6366$ and $e^\gamma$ are the natural-log versions.</div>

**A small set, computed by hand.** For $A = \lbrace 6, 10, 15\rbrace$:

$$
\log 6 \approx 1.792, \quad 6\log 6 \approx 10.75, \quad \frac{1}{6\log 6} \approx 0.093,
$$
$$
\log 10 \approx 2.303, \quad \frac{1}{10\log 10} \approx 0.043, \qquad \log 15 \approx 2.708, \quad \frac{1}{15\log 15} \approx 0.025.
$$

So $f(\lbrace 6,10,15\rbrace) \approx 0.161$. Tiny.

**The primes, the first few terms.** Write $\mathcal{P}$ for the set of all primes.

| $p$ | $f(p) = 1/(p\log p)$ | running sum |
|-----|----------------------|-------------|
| $2$ | $0.7213$ | $0.7213$ |
| $3$ | $0.3034$ | $1.0248$ |
| $5$ | $0.1243$ | $1.1490$ |
| $7$ | $0.0734$ | $1.2224$ |
| $11$ | $0.0379$ | $1.2604$ |
| $13$ | $0.0300$ | $1.2903$ |
| $17$ | $0.0208$ | $1.3111$ |
| $19$ | $0.0179$ | $1.3290$ |

The first two primes already contribute more than $1$. The first eight already contribute $1.33$, against $0.161$ for $\lbrace 6,10,15\rbrace$. Henri Cohen computed the full sum:

$$
f(\mathcal{P}) \;=\; 1.6366\ldots
$$

(That the infinite sum settles at all is not obvious. We prove it at the end of this volume.) This is the score to beat, and the theorem of the series is that nobody beats it.

<div class="pv-def"><strong>Theorem (Lichtman, 2022; conjectured by Erdős).</strong> For every primitive set $A$,
$$ f(A) \;\le\; f(\mathcal{P}) \;=\; 1.6366\ldots $$</div>

---

# why this weight?
{: #why-this-weight}

Why $1/(a\log a)$, and not another weight? Try the neighbours.

- **Weight $1/a$.** The primes score $\sum 1/p = \infty$. The numbers with $\Omega(n) = 2$ score infinity too: their sum $\sum_{p\le q} 1/(pq)$ contains $\frac12\bigl((\sum 1/p)^2 - \sum 1/p^2\bigr)$. The scale cannot tell the contestants apart.
- **Weight $1/a^2$.** Everything converges too easily. The primes score only $\sum_p 1/p^2 \approx 0.452$, and a pile of small composites can compete. The scale no longer sees the primes as special.
- **Weight $1/(a(\log a)^2)$.** The primes still converge, but for a bad reason: the integral test already says $\sum_n 1/(n(\log n)^2)$ converges, so *every* set of integers has a finite score. Primitivity is no longer the constraint that keeps the sum finite, and the contest stops being about the divisibility structure.

The weight $1/(a\log a)$ sits on the knife-edge: $\sum_n 1/(n\log n)$ diverges, while $\sum_p 1/(p\log p)$ converges. The scale is sensitive enough to see the primes as a finite budget, but not so harsh that composites become irrelevant. Primitivity is exactly what makes the sum finite. That is Erdős's theorem of 1935, and it is [Vol. III](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-III).

Watch the knife-edge. Pick a weight and drag the cutoff. The two curves are the partial sums over all integers $2\le n\le x$ and over the primes $p \le x$.

<div class="pv" id="pv-dial" aria-label="Partial sums of three weights over all integers and over primes">
  <div class="pv-title" id="pv-dial-title"></div>
  <div class="pv-sub" id="pv-dial-sub"></div>
  <svg id="pv-dial-svg" viewBox="0 0 640 300" role="img" aria-label="Partial sums against the cutoff x on a log scale; drag to move the cutoff"></svg>
  <div class="pv-read" id="pv-dial-read"></div>
  <div class="pv-ctl">
    <button type="button" data-w="0">1/a</button>
    <button type="button" data-w="1">1/(a log a)</button>
    <button type="button" data-w="2">1/(a log² a)</button>
    <span class="pv-key"><b style="background:#d95926"></b>all integers<b style="background:#3987e5"></b>primes only</span>
  </div>
</div>
<p class="pv-cap">The horizontal axis is logarithmic, from $10$ to $10^6$. Under $1/(a\log a)$ the orange curve keeps climbing, like $\log\log x$, while the blue one flattens toward the dashed line at $1.6366$. The shaded gap is the tail still to come, about $1/\log x$.</p>
<script>
(function () {
  var root = document.getElementById('pv-dial');
  if (!root || !window.PV) return;
  var svg = document.getElementById('pv-dial-svg'), E = PV.el, C = PV.C;
  var NMAX = 1000000, X0 = 60, X1 = 620, YT = 16, YB = 262, LMIN = 1, LMAX = 6, S = 240;
  var W = [function (n) { return 1 / n; }, function (n) { var l = Math.log(n); return 1 / (n * l); }, function (n) { var l = Math.log(n); return 1 / (n * l * l); }];
  var NAME = ['1/a', '1/(a log a)', '1/(a log² a)'];
  var sieve = new Uint8Array(NMAX + 1);
  for (var i = 2; i * i <= NMAX; i++) if (!sieve[i]) for (var j = i * i; j <= NMAX; j += i) sieve[j] = 1;
  var xs = [], all = [[], [], []], pr = [[], [], []];
  for (var k = 0; k <= S; k++) xs.push(Math.pow(10, LMIN + (LMAX - LMIN) * k / S));
  var tgt = xs.map(Math.floor), acc = [0, 0, 0], accp = [0, 0, 0], idx = 0;
  for (var n = 2; n <= NMAX; n++) {
    for (var w = 0; w < 3; w++) { var t = W[w](n); acc[w] += t; if (!sieve[n]) accp[w] += t; }
    while (idx <= S && n >= tgt[idx]) {
      for (var w2 = 0; w2 < 3; w2++) { all[w2].push(acc[w2]); pr[w2].push(accp[w2]); }
      idx++;
    }
  }
  var cur = 1, cut = 150;
  var gAx = E('g', {}, svg), gBand = E('g', {}, svg);
  var pA = E('path', { fill: 'none', stroke: C.orange, 'stroke-width': 2.5 }, svg);
  var pP = E('path', { fill: 'none', stroke: C.blue, 'stroke-width': 2.5 }, svg);
  var gLim = E('g', {}, svg);
  var vl = E('line', { y1: YT, y2: YB, stroke: C.ink2, 'stroke-width': 1.5, 'stroke-dasharray': '4 4' }, svg);
  var dA = E('circle', { r: 5, fill: C.orange }, svg), dP = E('circle', { r: 5, fill: C.blue }, svg);
  var hit = E('rect', { x: X0, y: YT, width: X1 - X0, height: YB - YT, fill: 'transparent', style: 'cursor:ew-resize' }, svg);
  PV.text(svg, (X0 + X1) / 2, 296, 'cutoff x (log scale) — drag on the plot', { 'text-anchor': 'middle', 'font-size': 13, style: 'fill:#c3c2b7' });
  function X(k) { return X0 + (X1 - X0) * k / S; }
  function draw() {
    var ymax = cur === 0 ? 15 : cur === 1 ? 3.2 : 2.4;
    var Y = function (v) { return YB - v / ymax * (YB - YT); };
    PV.clear(gAx);
    E('line', { x1: X0, x2: X1, y1: YB, y2: YB, stroke: '#444' }, gAx);
    for (var d = 1; d <= 6; d++) {
      var x = X((d - LMIN) / (LMAX - LMIN) * S);
      E('line', { x1: x, x2: x, y1: YB, y2: YB + 5, stroke: '#666' }, gAx);
      PV.text(gAx, x, YB + 19, '10' + ['', '', '²', '³', '⁴', '⁵', '⁶'][d], { 'text-anchor': 'middle', 'font-size': 12, style: 'fill:#c3c2b7' });
    }
    var step = cur === 0 ? 5 : 1;
    for (var v = 0; v <= ymax; v += step) {
      E('line', { x1: X0, x2: X1, y1: Y(v), y2: Y(v), stroke: '#242424' }, gAx);
      PV.text(gAx, X0 - 8, Y(v) + 4, v, { 'text-anchor': 'end', 'font-size': 12, style: 'fill:#c3c2b7' });
    }
    pA.setAttribute('d', PV.path(all[cur].map(function (s, k) { return [X(k), Y(Math.min(s, ymax))]; })));
    pP.setAttribute('d', PV.path(pr[cur].map(function (s, k) { return [X(k), Y(s)]; })));
    PV.clear(gLim); PV.clear(gBand);
    var x = xs[cut], sp = pr[cur][cut], sa = all[cur][cut];
    if (cur === 1) {
      E('line', { x1: X0, x2: X1, y1: Y(1.6366), y2: Y(1.6366), stroke: C.blue, 'stroke-dasharray': '6 5', 'stroke-opacity': 0.7 }, gLim);
      PV.text(gLim, X1 - 4, Y(1.6366) - 7, 'f(𝒫) = 1.6366', { 'text-anchor': 'end', 'font-size': 12, style: 'fill:#6fa8f0' });
      E('rect', { x: X(cut) - 6, width: 12, y: Y(1.6366), height: Math.max(0, Y(sp) - Y(1.6366)), fill: C.blue, 'fill-opacity': 0.25 }, gBand);
    }
    vl.setAttribute('x1', X(cut)); vl.setAttribute('x2', X(cut));
    dA.setAttribute('cx', X(cut)); dA.setAttribute('cy', Y(Math.min(sa, ymax)));
    dP.setAttribute('cx', X(cut)); dP.setAttribute('cy', Y(sp));
    root.querySelectorAll('[data-w]').forEach(function (b) { b.classList.toggle('on', +b.getAttribute('data-w') === cur); });
    document.getElementById('pv-dial-title').textContent = 'Weight ' + NAME[cur];
    document.getElementById('pv-dial-sub').textContent = [
      'Both diverge: all integers like log x, primes like log log x. No ranking possible.',
      'The knife-edge: all integers diverge (like log log x), the primes converge. Primitivity has to do real work.',
      'Both converge, so every set of integers has a finite score. Primitivity no longer matters.'][cur];
    var xr = Math.round(x).toLocaleString('en-US');
    var rd = 'x = <b>' + xr + '</b> &nbsp; all n ≤ x: <b>' + sa.toFixed(3) + '</b> &nbsp; primes ≤ x: <b>' + sp.toFixed(4) + '</b>';
    if (cur === 1) rd += ' &nbsp; gap to 1.6366: <b>' + (1.6366 - sp).toFixed(3) + '</b> vs 1/log x = <b>' + (1 / Math.log(x)).toFixed(3) + '</b>';
    document.getElementById('pv-dial-read').innerHTML = rd;
  }
  PV.drag(svg, hit, function (p) { cut = Math.max(0, Math.min(S, Math.round((p.x - X0) / (X1 - X0) * S))); draw(); });
  root.querySelectorAll('[data-w]').forEach(function (b) { b.addEventListener('click', function () { cur = +b.getAttribute('data-w'); draw(); }); });
  draw();
})();
</script>

There is also a calculus identity behind the weight. For any $a \ge 2$,

$$
\int_1^{\infty} a^{-t}\,dt \;=\; \frac{1}{a\log a}.
$$

To see it, write $a^{-t} = e^{-t\log a}$ and substitute $u = t\log a$, so $du = \log a\, dt$:

$$
\int_1^{\infty} e^{-t\log a}\,dt \;=\; \frac{1}{\log a} \int_{\log a}^{\infty} e^{-u}\,du \;=\; \frac{1}{\log a}\cdot e^{-\log a} \;=\; \frac{1}{a\log a}.
$$

So $1/(a\log a)$ is the $t$-average of the scores $a^{-t}$. We will not need this identity for the proof. It is here because it is where the weight comes from, and because it explains a warning: if you ask for the stronger comparison $\sum_{a \in A} a^{-t} \le \sum_p p^{-t}$ at *every* $t > 1$, the answer is no. That holds only for $t \ge \tau \approx 1.1403$. Shift the original weight slightly to $1/(a(\log a+h))$ and the primes stop winning as soon as $h \ge 1.04$. The theorem, once proved, is only just true.

---

# why $f(\mathcal{P})$ is finite
{: #why-fp-is-finite}

We have been using $f(\mathcal{P}) = 1.6366\ldots$ as a finite number. Here is why the series converges.

The **prime number theorem**, taken as a named fact, says that the number of primes up to $x$ is about $x/\log x$. Equivalently, near $t$ the primes have density about $1/\log t$, and the $n$th prime is $p_n \sim n\log n$. Then

$$
\frac{1}{p_n \log p_n} \;\sim\; \frac{1}{n\log n \cdot \log(n\log n)}.
$$

And $\log(n\log n) = \log n + \log\log n \sim \log n$, so

$$
\frac{1}{p_n \log p_n} \;\sim\; \frac{1}{n(\log n)^2}.
$$

We already know $\sum 1/(n(\log n)^2)$ converges, by the integral test. By the **limit comparison test**, a series of positive terms that behaves like a convergent series converges. So $\sum_p 1/(p\log p)$ converges.

The same integral explains the tail. The amount contributed by primes larger than $x$ is about

$$
\int_x^\infty \frac{1}{t\log t}\cdot\frac{dt}{\log t} \;=\; \frac{1}{\log x},
$$

where the second factor $dt/\log t$ is the prime number theorem's "number of primes in $[t, t+dt]$":

| primes up to | partial sum | gap to $1.6366$ | $1/\log x$ |
|-------------|-------------|-----------------|------------|
| $10^2$ | $1.4216$ | $0.215$ | $0.217$ |
| $10^4$ | $1.5282$ | $0.108$ | $0.109$ |
| $10^6$ | $1.5642$ | $0.072$ | $0.072$ |
| $10^8$ | $1.5823$ | $0.054$ | $0.054$ |

Each extra two orders of magnitude in the cutoff trims the gap by a factor of about $2/3$, not by an order of magnitude. That is what a $1/\log x$ tail looks like. It is also why the conjecture cannot be checked by adding up primitive sets until $10^{12}$ and comparing: the tail is large enough to hide a counterexample sitting out at infinity.

Where the sum sits among its neighbours:

| series | converges? | value / growth |
|--------|-----------|----------------|
| $\sum_p 1/p^2$ | yes | $0.4522\ldots$ |
| $\sum_p 1/(p\log p)$ | yes | $1.6366\ldots$ |
| $\sum_p 1/p$ | no | $\sim \log\log x$ |
| $\sum_n 1/(n\log n)$ | no | $\sim \log\log x$ |

The extra $\log$ in the denominator is not enough to make the sum over *all* integers converge. It *is* enough once you keep only the primes, because the primes themselves contribute another $1/\log n$ of sparsity. That second logarithm is a gift of the prime number theorem.

<details class="pv-ex"><summary><strong>Check yourself.</strong> The sums over the primes of $1/p$ and over all $n$ of $1/(n\log n)$ both grow like $\log\log x$. Why is that no coincidence?</summary>
<p>They are the same integral. The primes near $t$ have density $1/\log t$, so $\sum_{p\le x} 1/p \approx \int^x \frac{1}{t}\cdot\frac{dt}{\log t}$, which is exactly the integral that controls $\sum_{n\le x} 1/(n\log n)$. Substituting $u = \log t$ turns it into $\int du/u = \log u = \log\log x$. Thinning the integers to the primes costs one factor of $\log$, the same factor the weight $1/(a\log a)$ puts on every integer.</p>
</details>

---

# where this goes
{: #where-this-goes}

We have the ruler, $f(A) = \sum 1/(a\log a)$. We know it sits on the knife-edge: over all integers it diverges, over the primes it converges to $1.6366$. And we know experiments cannot settle anything here, because tails decay like $1/\log x$.

The first real question is whether *every* primitive set has a finite score. It does, and the proof is the most beautiful idea in the series: give each element of $A$ a private territory of integers, show that primitivity keeps the territories from overlapping, and let the size of the number line pay the bill. That is [Vol. III](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-III).

---

**Next:** [Vol. III: Territories and the $e^\gamma$ Bound](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-III)

*Primitive Sets:* [Vol. I](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets) · **Vol. II** · [Vol. III](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-III) · [Vol. IV](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-IV) · [Vol. V](/blog/2025/06/08/Back-of-the-Envelope-Primitive-Sets-Vol-V)
