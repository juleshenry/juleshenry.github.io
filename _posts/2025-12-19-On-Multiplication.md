---
layout: post
title: "On Multiplication, Vol. I: Schoolbook, Karatsuba, Toom-Cook"
date: 2025-12-19 12:00:00
mathjax: true
---

*On Multiplication:* **I** · [II](/blog/2025/12/19/On-Multiplication-Vol-II) · [III](/blog/2025/12/19/On-Multiplication-Vol-III) · [IV](/blog/2025/12/19/On-Multiplication-Vol-IV) · [V](/blog/2026/10/08/On-Multiplication-Vol-V)

# Intro

For centuries, multiplying two $n$-digit numbers meant performing $n^2$ single-digit multiplications. In 1960, the great Andrey Kolmogorov conjectured that this quadratic cost was an inescapable law of arithmetic. Within a week, a 23-year-old student named Anatoly Karatsuba proved him wrong.

This series traces the arc from schoolbook multiplication through the algorithms that successively shattered the $O(n^2)$ barrier: Karatsuba's $O(n^{1.585})$ divide-and-conquer trick, the polynomial interpolation of Toom-Cook, the Fourier-analytic machinery of Schönhage-Strassen, and the 2019 result of Harvey and van der Hoeven reaching $O(n \log n)$, long conjectured to be the floor. [Vol. IV](/blog/2025/12/19/On-Multiplication-Vol-IV) examines the parallel with sorting that made that conjecture so easy to believe. [Vol. V](/blog/2026/10/08/On-Multiplication-Vol-V), added in October 2026, covers a preprint claiming to go *below* $n \log n$, what that does to the parallel, and the conclusion of the series.

A caveat: in practice, these faster algorithms only overtake schoolbook multiplication at enormous scales. The Harvey-Hoeven algorithm's crossover point lies somewhere beyond $2^{1729^{12}}$ digits -- a number so large it cannot be written down even if every atom in the observable universe were an ink molecule. These are "galactic algorithms," beautiful and useless in equal measure. But their existence reveals something profound about the structure of computation itself.

# Schoolbook Multiplication: Fundamentally $O(n^2)$

To understand why we are traditionally tethered to $O(n^2)$, let us cast our minds back to the elementary school chalkboard. When we multiply two $n$-digit integers—say, $A$ and $B$—we are essentially performing a series of repetitive, granular tasks that scale quadratically with the input size.
## The Anatomy of the Partial Product

First, consider the "multiplication phase." We take the first digit of the multiplier ($B$) and multiply it by every single digit of the multiplicand ($A$). If both numbers have $n$ digits, this initial step requires $n$ individual single-digit multiplications.

Now, we must repeat this process for the second digit of $B$, then the third, and so on, until we have exhausted all $n$ digits of the multiplier. Mathematically, we are performing $n$ sets of $n$ multiplications. This gives us $n \times n$, or $n^2$ fundamental operations.
## The Cost of Alignment and Addition

Once we have generated these $n$ rows of partial products, the work is not yet finished. We must then perform the "addition phase." Each row is shifted to the left—a symbolic representation of multiplying by powers of 10—and then summed together.

- Each partial product can have up to $n+1$ digits.
- We are summing $n$ such rows.
- The total number of additions required to collapse these rows into a final product also scales with $n^2$.

## The Quadratic Ceiling

In the lexicon of Big O notation, we ignore the smaller constants and focus on the dominant growth factor. While you might perform some clever carries or skip a few zeros, the fundamental structure of the algorithm remains a nested loop: for every digit in the bottom number, you must visit every digit in the top number.

$$
\sum_{i=1}^{n}\sum_{j=1}^{n} \big(A_j \times B_i\big) \;\Longrightarrow\; O(n^2)
$$

Thus, the "schoolbook" method represents a rigid, two-dimensional grid of operations. To break the $O(n^2)$ barrier, as Harvey and van der Hoeven have done, one must move beyond this grid entirely—treating integers not as mere strings of digits, but as polynomials or points in a complex plane.

# Karatsuba: Breaking $O(n^2)$ with $O(n^{\log_2 3})$

Kolmogorov organized a seminar in 1960 specifically to prove that $O(n^2)$ was the floor for multiplication. He was wrong. A 23-year-old student named **Anatoly Karatsuba** attended that seminar and, within a week, returned with a counterexample that reduced the exponent from 2 to $\log_2 3 \approx 1.585$.

The idea is pure divide-and-conquer, but with an algebraic twist that turns four sub-multiplications into three.

### Splitting the Numbers

Take two $n$-digit numbers $x$ and $y$. Cut each in half at position $m = \lfloor n/2 \rfloor$, writing them as a "high part" times a power of the base plus a "low part":

$$
\begin{aligned}
x &= x_1 B^m + x_0 \\
y &= y_1 B^m + y_0
\end{aligned}
$$

Concretely: if $x = 1234$ in base 10, then $x_1 = 12$, $x_0 = 34$, and $m = 2$.

Expanding the product naively gives:

$$
xy = x_1 y_1 \cdot B^{2m} + (x_1 y_0 + x_0 y_1) \cdot B^m + x_0 y_0
$$

This expression requires **four** half-size multiplications: $x_1 y_1$, $x_1 y_0$, $x_0 y_1$, and $x_0 y_0$. Four recursive calls on inputs of size $n/2$ gives recurrence $T(n) = 4T(n/2) + O(n)$, which solves to $O(n^2)$ by the Master Theorem -- no improvement at all.

### The Trick: Three Multiplications Suffice

Karatsuba's insight is that we never need the cross-terms $x_1 y_0$ and $x_0 y_1$ individually. We only need their **sum**. And that sum falls out for free from a single cleverly chosen multiplication.

Define three products:

$$
\begin{aligned}
z_2 &= x_1 \cdot y_1 \\
z_0 &= x_0 \cdot y_0 \\
z_1 &= (x_1 + x_0)(y_1 + y_0) - z_2 - z_0
\end{aligned}
$$

Expand $z_1$ to see why this works:

$$
(x_1 + x_0)(y_1 + y_0) = \underbrace{x_1 y_1}_{z_2} + x_1 y_0 + x_0 y_1 + \underbrace{x_0 y_0}_{z_0}
$$

Subtracting $z_2$ and $z_0$ cancels the terms we already know, leaving exactly the cross-term sum $x_1 y_0 + x_0 y_1$. We have extracted the middle coefficient using **one** multiplication and **two** subtractions -- operations that cost only $O(n)$, negligible compared to multiplication.

The final product assembles as:

$$
xy = z_2 \cdot B^{2m} + z_1 \cdot B^m + z_0
$$

Three multiplications. Not four. At every level of the recursion, we save 25% of the multiplicative work, and that savings compounds exponentially as we recurse deeper.

### The Payoff

The recurrence is now $T(n) = 3T(n/2) + O(n)$, and the Master Theorem gives:

| Method        | Recurrence                     | Complexity                              |
|---------------|--------------------------------|-----------------------------------------|
| Schoolbook    | $T(n)=4T(n/2)+O(n)$           | $O(n^{\log_2 4}) = O(n^2)$             |
| Karatsuba     | $T(n)=3T(n/2)+O(n)$           | $O(n^{\log_2 3}) \approx O(n^{1.585})$ |

The gap between $n^2$ and $n^{1.585}$ may look modest for small $n$, but it widens relentlessly. At 1,000 digits the schoolbook method performs $\sim 10^6$ primitive multiplications; Karatsuba performs $\sim 10^{4.75} \approx 56{,}000$ -- a 17$\times$ speedup. At 10,000 digits the ratio exceeds 100$\times$. The deeper the recursion, the more the saved quarter compounds.

The visualization below runs the trick on a real product, $3141 \times 2718$, drawn to scale as an area. Step through it with Next and Back, or the arrow keys.

<style>
.mviz { --viz-bg:#121212; --viz-ink:#f0f0f0; --viz-ink2:#c3c2b7; --viz-line:#2f2f2f; --viz-blue:#3987e5; --viz-orange:#d95926; --viz-aqua:#199e70; --viz-neutral:#3a3a3a;
  background:var(--viz-bg); color:var(--viz-ink); border:1px solid var(--viz-line); border-radius:8px; padding:16px; margin:2em 0; font-size:15px; line-height:1.45; }
.mviz svg { display:block; width:100%; height:auto; }
.mviz svg text { font-family:inherit; fill:var(--viz-ink); }
.mviz .mv-title { font-weight:600; min-height:2.9em; margin-bottom:8px; }
.mviz .mv-body { display:flex; flex-wrap:wrap; gap:16px; align-items:flex-start; }
.mviz .mv-fig { flex:1 1 320px; min-width:0; }
.mviz .mv-side { flex:1 1 220px; min-width:0; font-variant-numeric:tabular-nums; }
.mviz .mv-ledger { list-style:none; margin:0; padding:0; }
.mviz .mv-ledger li { padding:3px 0 3px 10px; border-left:2px solid transparent; color:var(--viz-ink2); }
.mviz .mv-ledger li.cur { border-left-color:var(--viz-orange); color:var(--viz-ink); }
.mviz .mv-count { margin-top:12px; color:var(--viz-ink2); }
.mviz .mv-dot { display:inline-block; width:12px; height:12px; border-radius:50%; border:2px solid var(--viz-ink2); margin-right:4px; vertical-align:-1px; }
.mviz .mv-dot.on { background:var(--viz-orange); border-color:var(--viz-orange); }
.mviz .mv-controls { display:flex; gap:8px; align-items:center; margin-top:14px; }
.mviz button { font:inherit; font-size:14px; color:var(--viz-ink); background:#1f1f1f; border:1px solid #444; border-radius:6px; padding:5px 12px; cursor:pointer; }
.mviz button:hover:not(:disabled) { border-color:var(--viz-ink2); }
.mviz button:disabled { opacity:.4; cursor:default; }
.mviz .mv-step { color:var(--viz-ink2); font-size:13px; margin-left:auto; }
.mviz .cell rect { transition:fill .35s, fill-opacity .35s; }
.mviz .cell text, .mviz .fade { transition:opacity .35s; }
.mviz pre.mv-sum { margin:8px 0 0; padding:0; background:none; border:0; color:var(--viz-ink); font-size:14px; line-height:1.35; }
</style>
<div class="mviz" id="kviz" tabindex="0" aria-label="Karatsuba multiplication, step by step">
  <div class="mv-title" id="kviz-title"></div>
  <div class="mv-body">
    <div class="mv-fig">
      <svg viewBox="0 0 490 300" role="img" aria-label="Area model of 3141 times 2718">
        <defs>
          <pattern id="kviz-hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#f0f0f0" stroke-width="1.5" stroke-opacity=".55"/></pattern>
        </defs>
        <g id="kviz-top-split" class="fade">
          <text x="187.5" y="36" text-anchor="middle" font-size="15">x₁ = 31</text>
          <text x="367.5" y="36" text-anchor="middle" font-size="15">x₀ = 41</text>
        </g>
        <g id="kviz-left-split" class="fade">
          <text x="100" y="122" text-anchor="end" font-size="15">y₁ = 27</text>
          <text x="100" y="235" text-anchor="end" font-size="15">y₀ = 18</text>
        </g>
        <g id="kviz-top-sum" class="fade" opacity="0">
          <text x="290" y="36" text-anchor="middle" font-size="15" style="fill:#d95926;font-weight:600">x₁ + x₀ = 72</text>
        </g>
        <g id="kviz-left-sum" class="fade" opacity="0">
          <text x="100" y="167" text-anchor="end" font-size="15" style="fill:#d95926;font-weight:600">y₁ + y₀ = 45</text>
        </g>
        <g class="cell" id="kviz-c-tl"><rect x="111" y="51" width="153" height="133" rx="3"/><rect class="hatch" x="111" y="51" width="153" height="133" rx="3" fill="url(#kviz-hatch)" opacity="0"/><text x="187.5" y="112" text-anchor="middle" font-size="14" class="nm"></text><text x="187.5" y="134" text-anchor="middle" font-size="18" font-weight="600" class="val"></text></g>
        <g class="cell" id="kviz-c-tr"><rect x="266" y="51" width="203" height="133" rx="3"/><rect class="hatch" x="266" y="51" width="203" height="133" rx="3" fill="url(#kviz-hatch)" opacity="0"/><text x="367.5" y="112" text-anchor="middle" font-size="14" class="nm"></text><text x="367.5" y="134" text-anchor="middle" font-size="18" font-weight="600" class="val"></text></g>
        <g class="cell" id="kviz-c-bl"><rect x="111" y="186" width="153" height="88" rx="3"/><rect class="hatch" x="111" y="186" width="153" height="88" rx="3" fill="url(#kviz-hatch)" opacity="0"/><text x="187.5" y="225" text-anchor="middle" font-size="14" class="nm"></text><text x="187.5" y="247" text-anchor="middle" font-size="18" font-weight="600" class="val"></text></g>
        <g class="cell" id="kviz-c-br"><rect x="266" y="186" width="203" height="88" rx="3"/><rect class="hatch" x="266" y="186" width="203" height="88" rx="3" fill="url(#kviz-hatch)" opacity="0"/><text x="367.5" y="225" text-anchor="middle" font-size="14" class="nm"></text><text x="367.5" y="247" text-anchor="middle" font-size="18" font-weight="600" class="val"></text></g>
        <rect id="kviz-outline" class="fade" x="108" y="48" width="364" height="229" rx="5" fill="none" stroke="#d95926" stroke-width="3" opacity="0"/>
        <g id="kviz-big" class="fade" opacity="0">
          <rect x="215" y="146" width="150" height="34" rx="17" fill="#121212" stroke="#d95926" stroke-width="2"/>
          <text x="290" y="169" text-anchor="middle" font-size="17" font-weight="600">72 × 45 = 3240</text>
        </g>
      </svg>
    </div>
    <div class="mv-side">
      <ul class="mv-ledger" id="kviz-ledger"></ul>
      <pre class="mv-sum fade" id="kviz-sum" style="opacity:0">  z₂·10⁴ =   8 370 000
+ z₁·10² =     166 500
+ z₀     =         738
─────────────────────
           8 537 238 ✓</pre>
      <div class="mv-count" id="kviz-count"></div>
    </div>
  </div>
  <div class="mv-controls">
    <button type="button" id="kviz-prev">◀ Back</button>
    <button type="button" id="kviz-next">Next ▶</button>
    <span class="mv-step" id="kviz-step"></span>
  </div>
</div>
<script>
(function () {
  var root = document.getElementById('kviz');
  if (!root) return;
  var BLUE = '#3987e5', AQUA = '#199e70', ORANGE = '#d95926', NEUTRAL = '#3a3a3a', EMPTY = '#1c1c1c';
  // cell state: [fill, fillOpacity, name, value, hatched]
  var blank = [EMPTY, 1, '', '', false];
  var S = [
    { title: 'Split 3141 × 2718 in half (base 100). The product is the area of this rectangle, cut into four blocks.',
      cells: { tl: [NEUTRAL, 1, 'x₁·y₁', '', false], tr: [NEUTRAL, 1, 'x₀·y₁', '', false], bl: [NEUTRAL, 1, 'x₁·y₀', '', false], br: [NEUTRAL, 1, 'x₀·y₀', '', false] },
      ledger: ['x = 3141 → x₁ = 31, x₀ = 41', 'y = 2718 → y₁ = 27, y₀ = 18'], mult: 0, max: 4 },
    { title: 'Schoolbook: compute every block. Four half-size multiplications.',
      cells: { tl: [NEUTRAL, 1, '31 × 27', '837', false], tr: [NEUTRAL, 1, '41 × 27', '1107', false], bl: [NEUTRAL, 1, '31 × 18', '558', false], br: [NEUTRAL, 1, '41 × 18', '738', false] },
      ledger: ['31 × 27 = 837', '41 × 27 = 1107', '31 × 18 = 558', '41 × 18 = 738'], mult: 4, max: 4 },
    { title: 'Karatsuba, multiplication 1: the top-left block, z₂ = x₁ · y₁.',
      cells: { tl: [BLUE, 1, 'z₂', '837', false], tr: blank, bl: blank, br: blank },
      ledger: ['z₂ = 31 × 27 = 837'], mult: 1, max: 3 },
    { title: 'Multiplication 2: the bottom-right block, z₀ = x₀ · y₀.',
      cells: { tl: [BLUE, 1, 'z₂', '837', false], tr: blank, bl: blank, br: [AQUA, 1, 'z₀', '738', false] },
      ledger: ['z₂ = 31 × 27 = 837', 'z₀ = 41 × 18 = 738'], mult: 2, max: 3 },
    { title: 'Multiplication 3: add the halves first, then multiply once. (x₁ + x₀)(y₁ + y₀) is the area of the whole rectangle, all four blocks at once.',
      cells: { tl: [BLUE, .35, '', '', false], tr: [ORANGE, .35, '', '', false], bl: [ORANGE, .35, '', '', false], br: [AQUA, .35, '', '', false] },
      outline: true, big: true, sum: true,
      ledger: ['z₂ = 31 × 27 = 837', 'z₀ = 41 × 18 = 738', '(31 + 41)(27 + 18) = 72 × 45 = 3240'], mult: 3, max: 3 },
    { title: 'No more multiplying. Subtract the two corners we already know; what is left is the two cross blocks, which were never computed on their own.',
      cells: { tl: [BLUE, .35, '− z₂', '837', true], tr: [ORANGE, 1, 'z₁', '', false], bl: [ORANGE, 1, '', '', false], br: [AQUA, .35, '− z₀', '738', true] },
      outline: true, sum: true, z1: true,
      ledger: ['z₂ = 837', 'z₀ = 738', '3240 − 837 − 738 = 1665 = z₁', 'check: 1107 + 558 = 1665'], mult: 3, max: 3 },
    { title: 'Shift and add: xy = z₂·10⁴ + z₁·10² + z₀. Three multiplications instead of four.',
      cells: { tl: [BLUE, 1, 'z₂', '837', false], tr: [ORANGE, 1, 'z₁', '', false], bl: [ORANGE, 1, '', '', false], br: [AQUA, 1, 'z₀', '738', false] },
      z1: true, total: true,
      ledger: ['z₂ = 837', 'z₁ = 1665', 'z₀ = 738'], mult: 3, max: 3 },
    { title: 'Recurse: each of the three products is itself split the same way. After k levels that is 3ᵏ small products instead of 4ᵏ.',
      cells: { tl: [BLUE, 1, 'z₂', '837', false], tr: [ORANGE, 1, 'z₁', '', false], bl: [ORANGE, 1, '', '', false], br: [AQUA, 1, 'z₀', '738', false] },
      z1: true,
      ledger: ['1 level: 3 vs 4', '5 levels (32 digits): 243 vs 1,024', '10 levels (1,024 digits): 59,049 vs 1,048,576'], mult: 3, max: 3 }
  ];
  var i = 0, $ = function (id) { return document.getElementById('kviz-' + id); };
  function cell(id, st, z1Label) {
    var g = $('c-' + id), r = g.querySelector('rect');
    r.setAttribute('fill', st[0]); r.setAttribute('fill-opacity', st[1]);
    g.querySelector('.hatch').setAttribute('opacity', st[4] ? 1 : 0);
    g.querySelector('.nm').textContent = st[2];
    g.querySelector('.val').textContent = st[3];
  }
  function render() {
    var s = S[i];
    $('title').textContent = s.title;
    ['tl', 'tr', 'bl', 'br'].forEach(function (k) { cell(k, s.cells[k]); });
    if (s.z1) { // z1 spans the two cross blocks: label it once, across both
      $('c-tr').querySelector('.nm').textContent = 'z₁ = x₁y₀ + x₀y₁';
      $('c-tr').querySelector('.val').textContent = '1665';
    }
    $('outline').setAttribute('opacity', s.outline ? 1 : 0);
    $('big').setAttribute('opacity', s.big ? 1 : 0);
    $('top-split').setAttribute('opacity', s.sum ? 0 : 1);
    $('left-split').setAttribute('opacity', s.sum ? 0 : 1);
    $('top-sum').setAttribute('opacity', s.sum ? 1 : 0);
    $('left-sum').setAttribute('opacity', s.sum ? 1 : 0);
    $('sum').style.opacity = s.total ? 1 : 0;
    $('ledger').innerHTML = s.ledger.map(function (t, j) {
      return '<li' + (j === s.ledger.length - 1 ? ' class="cur"' : '') + '>' + t + '</li>';
    }).join('');
    var dots = '';
    for (var d = 0; d < s.max; d++) dots += '<span class="mv-dot' + (d < s.mult ? ' on' : '') + '"></span>';
    $('count').innerHTML = (s.max === 4 ? 'Schoolbook' : 'Karatsuba') + ' multiplications: ' + dots + ' ' + s.mult;
    $('step').textContent = (i + 1) + ' / ' + S.length;
    $('prev').disabled = i === 0;
    $('next').disabled = i === S.length - 1;
  }
  function go(d) { i = Math.max(0, Math.min(S.length - 1, i + d)); render(); }
  $('prev').addEventListener('click', function () { go(-1); });
  $('next').addEventListener('click', function () { go(1); });
  root.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') { go(1); e.preventDefault(); }
    if (e.key === 'ArrowLeft') { go(-1); e.preventDefault(); }
  });
  render();
})();
</script>

# Toom-Cook: Generalizing Karatsuba via Polynomial Interpolation

## From Digits to Polynomials

Karatsuba showed that splitting a number in two and exploiting an algebraic identity could reduce four half-size multiplications to three. A natural question follows: what happens if we split into *three* pieces? Or $k$? This is exactly the generalization that Andrei Toom (1963) and Stephen Cook (1966) independently formalized. The resulting family of algorithms -- collectively known as **Toom-Cook** or **Toom-$k$** -- systematically trades more additions and scalar operations for fewer recursive multiplications, pushing the exponent ever closer to 1.

The key conceptual shift is to stop viewing integers as flat strings of digits and instead view them as **polynomials**. If we partition an $n$-digit number into $k$ blocks of roughly $m = \lceil n/k \rceil$ digits each, writing $B = 10^m$ (or $2^m$ in binary), then:

$$
x = a_{k-1} B^{k-1} + a_{k-2} B^{k-2} + \cdots + a_1 B + a_0
$$

This is simply the number $x$ evaluated at the point $z = B$ of the polynomial:

$$
P_x(z) = a_{k-1} z^{k-1} + a_{k-2} z^{k-2} + \cdots + a_1 z + a_0
$$

Multiplying two such integers $x$ and $y$ is therefore equivalent to computing the **product polynomial** $P_x(z) \cdot P_y(z)$ and then evaluating the result at $z = B$ (with appropriate carries). If each input polynomial has degree $k-1$, their product has degree $2(k-1) = 2k - 2$, and is therefore determined by exactly $2k - 1$ point-value pairs -- a fact guaranteed by the **Fundamental Theorem of Algebra**.

This is the heart of the speedup: instead of multiplying the coefficients pairwise (which would require $k^2$ recursive multiplications), we can recover the product polynomial from only $2k - 1$ pointwise products.

## The Five Phases of Toom-Cook

The algorithm proceeds through five clearly delineated stages:

### Phase 1: Splitting

Break each $n$-digit operand into $k$ blocks of $\sim n/k$ digits. For Toom-3, this yields three coefficients per number:

$$
\begin{aligned}
x &= a_2 B^{2m} + a_1 B^m + a_0  &\longleftrightarrow\quad P_x(z) &= a_2 z^2 + a_1 z + a_0 \\
y &= b_2 B^{2m} + b_1 B^m + b_0  &\longleftrightarrow\quad P_y(z) &= b_2 z^2 + b_1 z + b_0
\end{aligned}
$$

### Phase 2: Evaluation

Select $2k - 1$ distinct evaluation points. The standard choice for Toom-3 is the set $\lbrace 0,\; 1,\; -1,\; 2,\; \infty \rbrace$, chosen because they minimize the size of intermediate values and keep the arithmetic simple. Evaluate both polynomials at each point:

$$
\begin{aligned}
P_x(0) &= a_0 & P_y(0) &= b_0 \\
P_x(1) &= a_2 + a_1 + a_0 & P_y(1) &= b_2 + b_1 + b_0 \\
P_x(-1) &= a_2 - a_1 + a_0 & P_y(-1) &= b_2 - b_1 + b_0 \\
P_x(2) &= 4a_2 + 2a_1 + a_0 & P_y(2) &= 4b_2 + 2b_1 + b_0 \\
P_x(\infty) &= a_2 & P_y(\infty) &= b_2
\end{aligned}
$$

The "evaluation at $\infty$" is a notational convenience: it extracts the leading coefficient of the polynomial, since $\lim_{z \to \infty} P(z)/z^{k-1}$ equals the leading coefficient.

### Phase 3: Pointwise Multiplication

Multiply the evaluated values at each point. These are the **only** recursive multiplications the algorithm performs:

$$
\begin{aligned}
W_0 &= P_x(0) \cdot P_y(0) = a_0 b_0 \\
W_1 &= P_x(1) \cdot P_y(1) \\
W_{-1} &= P_x(-1) \cdot P_y(-1) \\
W_2 &= P_x(2) \cdot P_y(2) \\
W_\infty &= P_x(\infty) \cdot P_y(\infty) = a_2 b_2
\end{aligned}
$$

Five multiplications on operands of size $\sim n/3$, rather than the nine that naive coefficient-by-coefficient expansion would require.

### Phase 4: Interpolation

The product polynomial $R(z) = P_x(z) \cdot P_y(z)$ has degree 4, so it has five coefficients $C_0, C_1, C_2, C_3, C_4$:

$$
R(z) = C_4 z^4 + C_3 z^3 + C_2 z^2 + C_1 z + C_0
$$

From the five evaluated products, we can read off:

$$
\begin{aligned}
W_0 &= C_0 \\
W_1 &= C_4 + C_3 + C_2 + C_1 + C_0 \\
W_{-1} &= C_4 - C_3 + C_2 - C_1 + C_0 \\
W_2 &= 16C_4 + 8C_3 + 4C_2 + 2C_1 + C_0 \\
W_\infty &= C_4
\end{aligned}
$$

This is a $5 \times 5$ linear system in the unknowns $C_0, \ldots, C_4$. Because $C_0 = W_0$ and $C_4 = W_\infty$ are immediate, the system reduces quickly. The remaining coefficients are solved by elimination:

$$
\begin{aligned}
C_0 &= W_0 \\[4pt]
C_4 &= W_\infty \\[4pt]
C_2 &= \frac{W_1 + W_{-1}}{2} - C_0 - C_4 \\[4pt]
C_3 &= \frac{W_2 - 2W_1 - 14C_4 - 2C_2 + C_0}{6} \\[4pt]
C_1 &= W_1 - C_4 - C_3 - C_2 - C_0
\end{aligned}
$$

Note that these expressions involve only additions, subtractions, and divisions by small constants (2 and 6) -- all $O(n)$ operations, negligible compared to the recursive multiplications.

### Phase 5: Recomposition

Reassemble the final integer from the product polynomial's coefficients:

$$
x \cdot y = C_4 B^{4m} + C_3 B^{3m} + C_2 B^{2m} + C_1 B^m + C_0
$$

The multiplications by powers of $B$ are simply left-shifts, and the final addition with carry propagation is $O(n)$.

## A Worked Example

To make this concrete, consider $x = 123{,}456{,}789$ and $y = 987{,}654{,}321$ in base 10 with $k = 3$ and $m = 3$ (so $B = 10^3 = 1000$):

$$
\begin{aligned}
x &= 123 \cdot 10^6 + 456 \cdot 10^3 + 789 \quad\Longleftrightarrow\quad P_x(z) = 123z^2 + 456z + 789 \\
y &= 987 \cdot 10^6 + 654 \cdot 10^3 + 321 \quad\Longleftrightarrow\quad P_y(z) = 987z^2 + 654z + 321
\end{aligned}
$$

Evaluating at the five standard points:

| Point | $P_x$ | $P_y$ | $W = P_x \cdot P_y$ |
|-------|--------|--------|----------------------|
| $0$   | $789$  | $321$  | $253{,}269$          |
| $1$   | $1{,}368$ | $1{,}962$ | $2{,}684{,}016$   |
| $-1$  | $456$  | $654$  | $298{,}224$          |
| $2$   | $2{,}193$ | $5{,}595$ | $12{,}269{,}835$   |
| $\infty$ | $123$ | $987$ | $121{,}401$          |

Interpolation then yields the five coefficients $C_0, \ldots, C_4$, and recomposition with $B = 1000$ recovers the product $121{,}932{,}631{,}112{,}635{,}269$.

## Complexity Analysis

The recurrence for Toom-$k$ is:

$$
T(n) = (2k - 1)\, T\!\left(\frac{n}{k}\right) + O(n)
$$

By the Master Theorem, this solves to:

$$
T(n) = O\!\left(n^{\log_k(2k-1)}\right)
$$

The exponent $\log_k(2k - 1)$ decreases monotonically as $k$ increases, approaching 1 from above:

| Algorithm             | Split ($k$) | Recursive Mults ($2k-1$) | Complexity                       |
|-----------------------|-------------|--------------------------|----------------------------------|
| Grade School          | $n$         | $n^2$                    | $O(n^2)$                         |
| Karatsuba (Toom-2)    | $2$         | $3$                      | $O(n^{\log_2 3}) \approx O(n^{1.585})$ |
| Toom-3                | $3$         | $5$                      | $O(n^{\log_3 5}) \approx O(n^{1.465})$ |
| Toom-4                | $4$         | $7$                      | $O(n^{\log_4 7}) \approx O(n^{1.404})$ |
| Toom-$k$              | $k$         | $2k-1$                   | $O\big(n^{\log_k(2k-1)}\big)$  |

### The Hidden Cost: Why We Cannot Simply Let $k \to \infty$

A tempting conclusion is that by choosing $k$ large enough, we can push the exponent arbitrarily close to 1 and achieve near-linear multiplication. In practice, this reasoning breaks down for two reasons:

1. **Evaluation and interpolation overhead.** The matrices involved in evaluation and interpolation grow as $O(k^2)$, and the entries grow in magnitude. For large $k$, the scalar additions and divisions in the interpolation phase cease to be negligible. The constant hidden in the $O(n)$ additive term balloons.

2. **Coefficient blowup.** Evaluating at points like $2, -2, 3, \ldots$ produces intermediate values that are significantly larger than the original coefficients. This "coefficient swell" increases the size of the sub-problems fed to the recursive multiplications, partially negating the savings.

The practical sweet spot is typically Toom-3 or Toom-4. Beyond that, the FFT-based methods (Schönhage-Strassen and its successors) offer a fundamentally better asymptotic trade-off. The transition from Toom-Cook to FFT-based multiplication is, in a sense, the transition from finite polynomial interpolation to interpolation at infinitely many structured points -- the roots of unity.

### Karatsuba as Toom-2: A Unifying Perspective

It is worth pausing to note that Karatsuba's algorithm is precisely Toom-Cook with $k = 2$. The "trick" of computing $(x_1 + x_0)(y_1 + y_0) - z_2 - z_0$ is the interpolation step for a degree-2 product polynomial evaluated at the points $\lbrace 0, 1, \infty \rbrace$. Karatsuba's genius was to discover this special case in 1960; Toom and Cook's contribution was to recognize the general structure of which Karatsuba is the simplest instance.

---

**Next:** [Vol. II: The Fourier Transform](/blog/2025/12/19/On-Multiplication-Vol-II)

*On Multiplication:* **Vol. I** · [Vol. II](/blog/2025/12/19/On-Multiplication-Vol-II) · [Vol. III](/blog/2025/12/19/On-Multiplication-Vol-III) · [Vol. IV](/blog/2025/12/19/On-Multiplication-Vol-IV) · [Vol. V](/blog/2026/10/08/On-Multiplication-Vol-V)
