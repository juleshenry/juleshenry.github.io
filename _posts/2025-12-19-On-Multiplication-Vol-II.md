---
layout: post
title: "On Multiplication, Vol. II: The Fourier Transform"
date: 2025-12-19 12:01:00
mathjax: true
---

*On Multiplication:* [I](/blog/2025/12/19/On-Multiplication) · **II** · [III](/blog/2025/12/19/On-Multiplication-Vol-III) · [IV](/blog/2025/12/19/On-Multiplication-Vol-IV) · [V](/blog/2026/10/08/On-Multiplication-Vol-V)

# The Fourier Transform: From Signals to Arithmetic

## Why We Need a New Idea

At the end of the Toom-Cook story in [Vol. I](/blog/2025/12/19/On-Multiplication) we noted a frustrating ceiling: as we increase the splitting parameter $k$, the exponent $\log_k(2k-1)$ drifts toward 1, but it never reaches it. Worse, the constant factor in the $O(n)$ additive work (evaluation and interpolation matrices of size $k \times k$, coefficient blowup at large evaluation points) grows so fast that no finite $k$ delivers practical gains beyond Toom-4 or so.

To break through this wall we need to abandon the strategy of evaluating at a handful of ad-hoc points and instead evaluate at a *structured infinite family* of points whose algebraic symmetry enables a radically faster algorithm. That family is the **complex roots of unity**, and the algorithm that exploits their symmetry is the **Fast Fourier Transform**.

Before we can state Schönhage and Strassen's multiplication algorithm, we must build the FFT from the ground up. This requires four conceptual layers: (1) the observation that integer multiplication is polynomial convolution, (2) the Discrete Fourier Transform as an evaluation map, (3) the Cooley-Tukey decomposition that makes the DFT fast, and (4) the inverse transform that recovers coefficients from point values.

---

## Multiplication Is Convolution

### Polynomials and digit vectors

We have already seen that an $n$-digit integer in base $B$ can be written as a polynomial evaluated at $B$. Let us now make the multiplication side precise. Given two integers with digit vectors $\mathbf{a} = (a_0, a_1, \ldots, a_{n-1})$ and $\mathbf{b} = (b_0, b_1, \ldots, b_{n-1})$, their product is a new integer whose digit vector $\mathbf{c} = (c_0, c_1, \ldots, c_{2n-2})$ satisfies:

$$
c_k = \sum_{j=0}^{k} a_j \, b_{k-j}
\qquad \text{for } k = 0, 1, \ldots, 2n-2
$$

(with the convention that $a_j = 0$ for $j \geq n$ and similarly for $b_j$). This is exactly the definition of the **linear convolution** of the sequences $\mathbf{a}$ and $\mathbf{b}$, or equivalently, the coefficient vector of the product polynomial $A(x) \cdot B(x)$ where:

$$
A(x) = \sum_{j=0}^{n-1} a_j x^j, \qquad B(x) = \sum_{j=0}^{n-1} b_j x^j
$$

Computing this convolution directly requires computing each of the $2n - 1$ output coefficients, and for each we sum up to $n$ products. The total cost is $O(n^2)$ -- schoolbook multiplication in disguise.

### The Convolution Theorem

The single most important theorem in this entire story is:

> **Convolution Theorem.** Let $\mathcal{F}$ denote the Discrete Fourier Transform (defined below). If $\mathbf{c} = \mathbf{a} \ast \mathbf{b}$ is the convolution of two sequences, then:
>
> $$\mathcal{F}(\mathbf{a} \ast \mathbf{b}) = \mathcal{F}(\mathbf{a}) \cdot \mathcal{F}(\mathbf{b})$$
>
> where $\cdot$ denotes *pointwise* (component-by-component) multiplication.

In words: convolution in the "coefficient domain" becomes pointwise multiplication in the "frequency domain." Since pointwise multiplication of two length-$N$ vectors costs only $O(N)$, the entire cost of multiplication reduces to the cost of *two forward transforms and one inverse transform*. If each transform costs $O(N \log N)$, the total cost is $O(N \log N)$ -- an exponential improvement over $O(N^2)$.

This is not a hand-wave. Let us now build the DFT rigorously and prove why it can be computed in $O(N \log N)$.

---

## The Discrete Fourier Transform

### Complex exponentials and Euler's formula

Before defining the DFT, we need the language of complex numbers. Recall **Euler's formula**:

$$
e^{i\theta} = \cos\theta + i\sin\theta
$$

This elegant identity tells us that the complex exponential $e^{i\theta}$ traces out the unit circle in the complex plane as $\theta$ varies from $0$ to $2\pi$. Every point on the unit circle can be written as $e^{i\theta}$ for some angle $\theta$.

### The $N$-th roots of unity

Fix a positive integer $N$. The **$N$-th roots of unity** are the $N$ complex numbers that satisfy $z^N = 1$. They are:

$$
\omega_N^k = e^{2\pi i k / N}, \qquad k = 0, 1, \ldots, N-1
$$

These are $N$ points spaced equally around the unit circle, like the vertices of a regular $N$-gon inscribed in the circle $\lvert z \rvert = 1$. The **primitive** $N$-th root of unity is:

$$
\omega_N = e^{2\pi i / N}
$$

so that $\omega_N^k = (\omega_N)^k$. We will usually drop the subscript $N$ when the context is clear.

The roots of unity possess remarkable algebraic properties that are the engine of the FFT:

1. **Periodicity:** $\omega^{k+N} = \omega^k$ for all $k$. The roots cycle with period $N$.

2. **Cancellation (Half-turn symmetry):** $\omega^{k + N/2} = -\omega^k$ when $N$ is even. Geometrically, the point diametrically opposite $\omega^k$ on the unit circle is $-\omega^k$. This is the single most important property for the FFT.

3. **Summation:** $\displaystyle\sum_{k=0}^{N-1} \omega^{jk} = \begin{cases} N & \text{if } N \mid j \cr 0 & \text{otherwise} \end{cases}$

   This orthogonality relation is what makes the inverse DFT work.

4. **Squaring (Halving):** If $N$ is even, then $\lbrace (\omega_N^k)^2 : k = 0, \ldots, N-1 \rbrace$ gives exactly the $N/2$-th roots of unity, each appearing twice. That is, $(\omega_N)^2 = \omega_{N/2}$.

### Definition of the DFT

Given a vector $\mathbf{x} = (x_0, x_1, \ldots, x_{N-1})$, its **Discrete Fourier Transform** is the vector $\mathbf{X} = (X_0, X_1, \ldots, X_{N-1})$ defined by:

$$
X_k = \sum_{j=0}^{N-1} x_j \, \omega_N^{jk}, \qquad k = 0, 1, \ldots, N-1
$$

Equivalently, $X_k = P(\omega^k)$ where $P(z) = \sum_{j} x_j z^j$ is the polynomial whose coefficients are the entries of $\mathbf{x}$. The DFT is nothing more than **evaluating the polynomial at all $N$-th roots of unity simultaneously**.

### The DFT matrix

We can express the DFT as a matrix-vector product $\mathbf{X} = F_N \, \mathbf{x}$ where the **DFT matrix** $F_N$ has entries:

$$
(F_N)_{k,j} = \omega_N^{jk}
$$

Explicitly, for $N = 4$ with $\omega = \omega_4 = e^{2\pi i/4} = i$:

$$
F_4 = \begin{pmatrix}
1 & 1 & 1 & 1 \\
1 & i & i^2 & i^3 \\
1 & i^2 & i^4 & i^6 \\
1 & i^3 & i^6 & i^9
\end{pmatrix}
= \begin{pmatrix}
1 & 1 & 1 & 1 \\
1 & i & -1 & -i \\
1 & -1 & 1 & -1 \\
1 & -i & -1 & i
\end{pmatrix}
$$

Computing $\mathbf{X} = F_N \mathbf{x}$ by brute-force matrix-vector multiplication costs $O(N^2)$. The entire point of the FFT is to exploit the structure of $F_N$ to compute this product in $O(N \log N)$.

### The Inverse DFT

The orthogonality of the roots of unity (property 3 above) guarantees that the DFT is invertible. The inverse is:

$$
x_j = \frac{1}{N} \sum_{k=0}^{N-1} X_k \, \omega_N^{-jk}
$$

or in matrix form, $\mathbf{x} = \frac{1}{N} F_N^{-1} \mathbf{X}$ where $F_N^{-1}$ is the matrix with entries $\omega_N^{-jk}$ -- the same as $F_N$ but with $\omega$ replaced by $\omega^{-1} = \overline{\omega}$ (the complex conjugate). In other words, **the inverse DFT is computed by the same algorithm as the forward DFT**, just with the twiddle factors conjugated and the output scaled by $1/N$. Any algorithm that computes the forward DFT efficiently also computes the inverse efficiently, for free.

**Proof of inversion.** We need to verify that $\frac{1}{N}F_N^{-1} F_N = I_N$, i.e., that:

$$
\frac{1}{N} \sum_{k=0}^{N-1} \omega^{-jk} \omega^{k\ell} = \frac{1}{N} \sum_{k=0}^{N-1} \omega^{k(\ell - j)} = \begin{cases} 1 & \text{if } j = \ell \\ 0 & \text{if } j \neq \ell \end{cases}
$$

When $j = \ell$, every term in the sum is $\omega^0 = 1$, so the sum is $N$ and we get $N/N = 1$. When $j \neq \ell$, let $m = \ell - j \not\equiv 0 \pmod{N}$. Then $\sum_{k=0}^{N-1} \omega^{mk}$ is a geometric series with ratio $r = \omega^m \neq 1$:

$$
\sum_{k=0}^{N-1} r^k = \frac{r^N - 1}{r - 1} = \frac{(\omega^N)^m - 1}{\omega^m - 1} = \frac{1 - 1}{\omega^m - 1} = 0
$$

since $\omega^N = 1$ by definition. $\blacksquare$

---

## The Fast Fourier Transform (Cooley-Tukey, Radix-2)

### The core idea: divide and conquer on even and odd indices

The breakthrough of Cooley and Tukey (1965) -- though the idea traces back to Gauss (1805) -- is to observe that when $N$ is even, the DFT of size $N$ can be decomposed into **two DFTs of size $N/2$** plus $O(N)$ additional work.

Write $N = 2M$. Split the input sequence $\mathbf{x}$ into its even-indexed and odd-indexed elements:

$$
\begin{aligned}
\mathbf{e} &= (x_0, x_2, x_4, \ldots, x_{N-2}) \quad \text{(even indices)} \\
\mathbf{d} &= (x_1, x_3, x_5, \ldots, x_{N-1}) \quad \text{(odd indices)}
\end{aligned}
$$

Now consider the DFT sum for an arbitrary output index $k$:

$$
X_k = \sum_{j=0}^{N-1} x_j \, \omega_N^{jk}
$$

Separate the even-indexed and odd-indexed terms:

$$
X_k = \underbrace{\sum_{m=0}^{M-1} x_{2m} \, \omega_N^{2mk}}_{E_k} + \underbrace{\omega_N^k \sum_{m=0}^{M-1} x_{2m+1} \, \omega_N^{2mk}}_{= \omega_N^k \cdot D_k}
$$

Using the **squaring property** $\omega_N^2 = \omega_M$ (where $M = N/2$), each of these inner sums is itself a DFT of size $M$:

$$
\begin{aligned}
E_k &= \sum_{m=0}^{M-1} x_{2m} \, \omega_M^{mk} = \text{DFT}_M(\mathbf{e})_k \\[4pt]
D_k &= \sum_{m=0}^{M-1} x_{2m+1} \, \omega_M^{mk} = \text{DFT}_M(\mathbf{d})_k
\end{aligned}
$$

So the full DFT decomposes as:

$$
\boxed{X_k = E_k + \omega_N^k \cdot D_k}
$$

But we need $X_k$ for $k = 0, 1, \ldots, N-1$, while $E_k$ and $D_k$ are periodic with period $M = N/2$ (they are DFTs of size $M$). For the "upper half" $k + M$, the **cancellation property** $\omega_N^{k+M} = -\omega_N^k$ gives:

$$
\boxed{X_{k+M} = E_k - \omega_N^k \cdot D_k}
$$

These two equations together constitute the **butterfly operation**: from the pair $(E_k, D_k)$ and the **twiddle factor** $\omega_N^k$, we compute both $X_k$ and $X_{k+M}$ using **one** complex multiplication and **two** complex additions.

### The butterfly diagram

Each butterfly takes two inputs, multiplies one by a twiddle factor, and produces two outputs via addition and subtraction:

```
  E_k ──────────┬──── (+) ──── X_k
                 │
          ω^k    ×
                 │
  D_k ──────────┴──── (−) ──── X_{k+M}
```

For $M = N/2$ values of $k$ (namely $k = 0, 1, \ldots, M-1$), we perform $M$ butterflies, each costing $O(1)$. The total additional work at this level of recursion is $O(N)$.

### The recurrence and complexity

Let $T(N)$ denote the cost of computing a DFT of size $N$ (assumed a power of 2). The Cooley-Tukey decomposition gives:

$$
T(N) = 2\,T(N/2) + O(N)
$$

By the Master Theorem (case 2, with $a = 2$, $b = 2$, $f(N) = \Theta(N)$):

$$
T(N) = O(N \log N)
$$

compared to $O(N^2)$ for the naive DFT. For $N = 2^{20} \approx 10^6$, this is the difference between $\sim 10^{12}$ operations and $\sim 2 \times 10^7$ -- a speedup of 50,000$\times$.

### The full recursion tree

When $N = 2^s$, the recursion unfolds $s = \log_2 N$ levels deep. At each level, we partition the data, recurse on two halves, and combine with $N$ butterfly operations. The total work is:

$$
\underbrace{N}_{\text{level 0}} + \underbrace{N}_{\text{level 1}} + \cdots + \underbrace{N}_{\text{level } s-1} = s \cdot N = N \log_2 N
$$

Each level performs exactly $N/2$ butterflies (each costing one complex multiplication and two additions), for a total of $\frac{N}{2}\log_2 N$ complex multiplications.

### A worked example: 8-point FFT

Let $N = 8$ and $\omega = \omega_8 = e^{2\pi i/8} = e^{i\pi/4} = \frac{1+i}{\sqrt{2}}$. Consider the input $\mathbf{x} = (1, 1, 1, 1, 0, 0, 0, 0)$ (a rectangular pulse).

**Level 0 (split):** Separate into even and odd:

$$
\mathbf{e} = (x_0, x_2, x_4, x_6) = (1, 1, 0, 0), \qquad \mathbf{d} = (x_1, x_3, x_5, x_7) = (1, 1, 0, 0)
$$

**Level 1:** Each half recursively splits again. For $\mathbf{e}$:

$$
\mathbf{e}_{\text{even}} = (1, 0), \quad \mathbf{e}_{\text{odd}} = (1, 0)
$$

These are 2-point DFTs: $\text{DFT}_2(a, b) = (a + b, \; a - b)$. So:

$$
\text{DFT}_2(1, 0) = (1, 1) \quad \text{for both}
$$

**Level 1 butterfly (for $\mathbf{e}$):** Combine with twiddle factors $\omega_4^0 = 1$ and $\omega_4^1 = i$:

$$
E_0 = 1 + 1 \cdot 1 = 2, \quad E_2 = 1 - 1 \cdot 1 = 0
$$

$$
E_1 = 1 + i \cdot 1 = 1 + i, \quad E_3 = 1 - i \cdot 1 = 1 - i
$$

So $\text{DFT}_4(\mathbf{e}) = (2, \; 1+i, \; 0, \; 1-i)$.

An identical calculation gives $\text{DFT}_4(\mathbf{d}) = (2, \; 1+i, \; 0, \; 1-i)$.

**Level 0 butterfly:** Combine with twiddle factors $\omega_8^k$ for $k = 0, 1, 2, 3$:

$$
\begin{aligned}
X_0 &= E_0 + \omega^0 D_0 = 2 + 1 \cdot 2 = 4 \\
X_1 &= E_1 + \omega^1 D_1 = (1+i) + \tfrac{1+i}{\sqrt{2}}(1+i) = (1+i) + \tfrac{2i}{\sqrt{2}} = 1 + i + i\sqrt{2} \\
X_2 &= E_2 + \omega^2 D_2 = 0 + i \cdot 0 = 0 \\
X_3 &= E_3 + \omega^3 D_3 = (1-i) + \tfrac{-1+i}{\sqrt{2}}(1-i) = (1-i) + \tfrac{2i}{\sqrt{2}} = 1 - i + i\sqrt{2} \\
&\phantom{=}\; \text{(and the corresponding } X_{k+4} = E_k - \omega^k D_k \text{ for the upper half)}
\end{aligned}
$$

The key observation is not the specific numerical values but the *structure*: $3$ levels of $4$ butterflies each $= 12$ complex multiplications, versus $8^2 = 64$ for the naive DFT. The ratio $12/64 \approx 19\%$ -- and this ratio improves as $N$ grows.

The visualization below runs this exact example through the 8-point butterfly network, stage by stage. The input goes in bit-reversed, the butterflies span 1, then 2, then 4, and every value shown is computed live. Hover or tap any value to see which two numbers and which twiddle factor produced it.

<style>
.mviz { --viz-bg:#121212; --viz-ink:#f0f0f0; --viz-ink2:#c3c2b7; --viz-line:#2f2f2f; --viz-blue:#3987e5; --viz-orange:#d95926;
  background:var(--viz-bg); color:var(--viz-ink); border:1px solid var(--viz-line); border-radius:8px; padding:16px; margin:2em 0; font-size:15px; line-height:1.45; }
.mviz svg text { font-family:inherit; fill:var(--viz-ink); }
.mviz .mv-title { font-weight:600; min-height:2.9em; margin-bottom:8px; }
.mviz .mv-scroll { overflow-x:auto; -webkit-overflow-scrolling:touch; }
.mviz .mv-scroll svg { display:block; width:100%; min-width:620px; height:auto; }
.mviz .mv-detail { min-height:1.5em; margin-top:8px; color:var(--viz-ink2); font-variant-numeric:tabular-nums; }
.mviz .mv-controls { display:flex; gap:8px; align-items:center; margin-top:14px; flex-wrap:wrap; }
.mviz button { font:inherit; font-size:14px; color:var(--viz-ink); background:#1f1f1f; border:1px solid #444; border-radius:6px; padding:5px 12px; cursor:pointer; }
.mviz button:hover:not(:disabled) { border-color:var(--viz-ink2); }
.mviz button:disabled { opacity:.4; cursor:default; }
.mviz .mv-step { color:var(--viz-ink2); font-size:13px; margin-left:auto; }
.mviz .mv-key { color:var(--viz-ink2); font-size:13px; }
.mviz .mv-key b { display:inline-block; width:18px; height:3px; vertical-align:middle; margin:0 4px 0 10px; }
.mviz .chip rect { transition:stroke .25s, fill .25s; }
.mviz .chip, .mviz .wire, .mviz .tw { transition:opacity .35s; }
.mviz .chip.live { cursor:pointer; }
</style>
<div class="mviz" id="fviz" tabindex="0" aria-label="8-point FFT butterfly network, stage by stage">
  <div class="mv-title" id="fviz-title"></div>
  <div class="mv-scroll"><svg id="fviz-svg" viewBox="0 0 820 410" role="img" aria-label="8-point radix-2 FFT butterfly diagram"></svg></div>
  <div class="mv-detail" id="fviz-detail"></div>
  <div class="mv-controls">
    <button type="button" id="fviz-prev">◀ Back</button>
    <button type="button" id="fviz-next">Next ▶</button>
    <span class="mv-key"><b style="background:#3987e5"></b>a + ωᵏ·b<b style="background:#d95926"></b>a − ωᵏ·b</span>
    <span class="mv-step" id="fviz-step"></span>
  </div>
</div>
<script>
(function () {
  var root = document.getElementById('fviz');
  if (!root) return;
  var NS = 'http://www.w3.org/2000/svg', svg = document.getElementById('fviz-svg');
  var N = 8, BLUE = '#3987e5', ORANGE = '#d95926', DIM = '#4a4a4a';
  var SUB = '₀₁₂₃₄₅₆₇', SUP = '⁰¹²³⁴⁵⁶⁷';
  // Complex helpers, omega = e^(2πi/8) as in the text
  function mul(a, b) { return [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]]; }
  function add(a, b) { return [a[0] + b[0], a[1] + b[1]]; }
  function sub(a, b) { return [a[0] - b[0], a[1] - b[1]]; }
  function w(k) { var t = 2 * Math.PI * k / N; return [Math.cos(t), Math.sin(t)]; }
  function num(v) { var r = Math.round(v * 100) / 100; return String(Math.abs(r) < 1e-9 ? 0 : r); }
  function fmt(z) {
    var re = Math.abs(z[0]) < 1e-9 ? 0 : z[0], im = Math.abs(z[1]) < 1e-9 ? 0 : z[1];
    if (im === 0) return num(re);
    var imS = Math.abs(im) === 1 ? 'i' : num(Math.abs(im)) + 'i';
    if (re === 0) return (im < 0 ? '−' : '') + imS;
    return num(re) + (im < 0 ? '−' : '+') + imS;
  }
  function rev(r) { return ((r & 1) << 2) | (r & 2) | ((r & 4) >> 2); }
  // Compute every column: col 0 = bit-reversed input, col s = after stage s
  var x = [1, 1, 1, 1, 0, 0, 0, 0];
  var cols = [x.map(function (_, r) { return [x[rev(r)], 0]; })];
  var how = [[]]; // how[s][r] = {a, b, k, sign}
  for (var s = 1; s <= 3; s++) {
    var h = 1 << (s - 1), prev = cols[s - 1], cur = [], hw = [];
    for (var g = 0; g < N; g += 2 * h) for (var j = 0; j < h; j++) {
      var top = g + j, bot = top + h, k = j * (N / (2 * h)), t = mul(w(k), prev[bot]);
      cur[top] = add(prev[top], t); cur[bot] = sub(prev[top], t);
      hw[top] = { a: top, b: bot, k: k, sign: '+' }; hw[bot] = { a: top, b: bot, k: k, sign: '−' };
    }
    cols.push(cur); how.push(hw);
  }
  // Layout
  var CX = [66, 292, 518, 744], CW = 108, CH = 28, Y0 = 44, DY = 44;
  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var a in attrs) e.setAttribute(a, attrs[a]);
    (parent || svg).appendChild(e); return e;
  }
  var yOf = function (r) { return Y0 + r * DY; };
  ['Input (bit-reversed)', 'After stage 1', 'After stage 2', 'Output Xₖ'].forEach(function (t, c) {
    el('text', { x: CX[c], y: 20, 'text-anchor': 'middle', 'font-size': 13, style: 'fill:#c3c2b7' }).textContent = t;
  });
  var wires = [], tws = [], chips = [];
  for (s = 1; s <= 3; s++) {
    var gW = el('g', {}), x0 = CX[s - 1] + CW / 2, x1 = CX[s] - CW / 2;
    how[s].forEach(function (hh, r) {
      var fromTop = yOf(hh.a), fromBot = yOf(hh.b), to = yOf(r), color = hh.sign === '+' ? BLUE : ORANGE;
      [fromTop, fromBot].forEach(function (fy) {
        var p = el('line', { x1: x0, y1: fy, x2: x1, y2: to, 'stroke-width': 2, class: 'wire' }, gW);
        wires.push({ el: p, stage: s, color: color });
      });
    });
    // twiddle label on each butterfly's lower input
    how[s].forEach(function (hh, r) {
      if (hh.sign !== '+') return;
      var t = el('text', { x: x0 + 6, y: yOf(hh.b) - 7, 'font-size': 12, class: 'tw', style: 'fill:#f0f0f0;stroke:#121212;stroke-width:4px;paint-order:stroke' });
      t.textContent = '×ω' + SUP[hh.k];
      tws.push({ el: t, stage: s });
    });
  }
  for (var c = 0; c < 4; c++) for (var r = 0; r < N; r++) {
    var g2 = el('g', { class: 'chip' });
    el('rect', { x: CX[c] - CW / 2, y: yOf(r) - CH / 2, width: CW, height: CH, rx: 6, fill: '#1c1c1c', stroke: '#555', 'stroke-width': 1.5 }, g2);
    var label = c === 0 ? 'x' + SUB[rev(r)] + ' = ' + fmt(cols[0][r]) : c === 3 ? 'X' + SUB[r] + ' = ' + fmt(cols[3][r]) : fmt(cols[c][r]);
    el('text', { x: CX[c], y: yOf(r) + 5, 'text-anchor': 'middle', 'font-size': 14 }, g2).textContent = label;
    chips.push({ el: g2, col: c, row: r });
  }
  var S = [
    { title: 'Input x = (1, 1, 1, 1, 0, 0, 0, 0), a rectangular pulse, loaded in bit-reversed order: row r holds x at index r with its 3 bits reversed.', upto: 0 },
    { title: 'Stage 1: butterflies on neighbours (span 1). Twiddle ω⁰ = 1, so each pair becomes (a + b, a − b): four 2-point DFTs.', upto: 1 },
    { title: 'Stage 2: span 2, twiddles ω⁰ = 1 and ω² = i. Rows 0–3 now hold DFT₄ of the even samples (E), rows 4–7 DFT₄ of the odd samples (D).', upto: 2 },
    { title: 'Stage 3: span 4, twiddles ω⁰…ω³. Xₖ = Eₖ + ωᵏ·Dₖ and Xₖ₊₄ = Eₖ − ωᵏ·Dₖ. The output comes out in natural order.', upto: 3 },
    { title: '3 stages × 4 butterflies = 12 twiddle multiplications, against 8² = 64 for the direct DFT. At N points: (N/2)·log₂N versus N².', upto: 3, all: true }
  ];
  var i = 0, detail = document.getElementById('fviz-detail');
  function explain(ch) {
    var c = ch.col, r = ch.row;
    if (c === 0) { detail.textContent = 'Row ' + r + ' = ' + r.toString(2).padStart(3, '0') + '₂ holds x' + SUB[rev(r)] + ' (' + rev(r).toString(2).padStart(3, '0') + '₂ reversed).'; return; }
    var hh = how[c][r], a = cols[c - 1][hh.a], b = cols[c - 1][hh.b];
    detail.textContent = (c === 3 ? 'X' + SUB[r] : 'Stage ' + c + ', row ' + r) + ' = (' + fmt(a) + ') ' + hh.sign + ' ω' + SUP[hh.k] + '·(' + fmt(b) + ') = ' + fmt(cols[c][r]);
  }
  chips.forEach(function (ch) {
    ch.el.addEventListener('mouseenter', function () { if (ch.col <= S[i].upto) explain(ch); });
    ch.el.addEventListener('click', function () { if (ch.col <= S[i].upto) explain(ch); });
  });
  function render() {
    var st = S[i];
    document.getElementById('fviz-title').textContent = st.title;
    wires.forEach(function (wv) {
      var on = wv.stage <= st.upto, cur = wv.stage === st.upto && !st.all;
      wv.el.setAttribute('stroke', cur || st.all ? wv.color : DIM);
      wv.el.setAttribute('opacity', on ? (cur || st.all ? 1 : .6) : 0);
    });
    tws.forEach(function (t) { t.el.setAttribute('opacity', t.stage === st.upto || st.all ? 1 : 0); });
    chips.forEach(function (ch) {
      ch.el.setAttribute('opacity', ch.col <= st.upto ? 1 : .15);
      ch.el.classList.toggle('live', ch.col <= st.upto);
      ch.el.querySelector('rect').setAttribute('stroke', ch.col === st.upto && !st.all ? '#f0f0f0' : '#555');
    });
    detail.textContent = st.upto ? 'Hover or tap a value to see how it was computed.' : 'Hover or tap a row to see the bit reversal.';
    document.getElementById('fviz-step').textContent = (i + 1) + ' / ' + S.length;
    document.getElementById('fviz-prev').disabled = i === 0;
    document.getElementById('fviz-next').disabled = i === S.length - 1;
  }
  function go(d) { i = Math.max(0, Math.min(S.length - 1, i + d)); render(); }
  document.getElementById('fviz-prev').addEventListener('click', function () { go(-1); });
  document.getElementById('fviz-next').addEventListener('click', function () { go(1); });
  root.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') { go(1); e.preventDefault(); }
    if (e.key === 'ArrowLeft') { go(-1); e.preventDefault(); }
  });
  render();
})();
</script>

---

## Putting It Together: FFT-Based Polynomial Multiplication

We now have all the pieces. To multiply two polynomials $A(x)$ and $B(x)$ of degree $n-1$ (and thereby two $n$-digit integers):

**Step 1. Pad.** The product polynomial has degree $2n - 2$, so we need at least $2n - 1$ evaluation points. Choose $N = 2^{\lceil \log_2(2n) \rceil}$ (the next power of 2 at or above $2n$). Pad both coefficient vectors with zeros to length $N$.

**Step 2. Forward FFT.** Compute $\hat{\mathbf{a}} = \text{FFT}_N(\mathbf{a})$ and $\hat{\mathbf{b}} = \text{FFT}_N(\mathbf{b})$. Cost: $O(N \log N)$ each.

**Step 3. Pointwise multiply.** Compute $\hat{c}_k = \hat{a}_k \cdot \hat{b}_k$ for $k = 0, \ldots, N-1$. Cost: $O(N)$.

**Step 4. Inverse FFT.** Compute $\mathbf{c} = \text{IFFT}_N(\hat{\mathbf{c}})$. Cost: $O(N \log N)$.

**Step 5. Carry propagation.** The entries of $\mathbf{c}$ are the exact convolution coefficients (no rounding -- yet). Each $c_k$ may exceed the base $B$, so we perform a single left-to-right carry pass: set $c_k \leftarrow c_k \bmod B$ and add $\lfloor c_k / B \rfloor$ to $c_{k+1}$. Cost: $O(N)$.

**Total cost: $O(N \log N) = O(n \log n)$.**

At this point you might ask: if the FFT already gives us $O(n \log n)$ multiplication, why do we need Schönhage-Strassen? The answer lies in a subtle but critical issue: **numerical precision**.

---

**Next:** [Vol. III: Schönhage-Strassen and Harvey-van der Hoeven](/blog/2025/12/19/On-Multiplication-Vol-III)

*On Multiplication:* [Vol. I](/blog/2025/12/19/On-Multiplication) · **Vol. II** · [Vol. III](/blog/2025/12/19/On-Multiplication-Vol-III) · [Vol. IV](/blog/2025/12/19/On-Multiplication-Vol-IV) · [Vol. V](/blog/2026/10/08/On-Multiplication-Vol-V)
