---
layout: post
title: "Back-of-the-Envelope: Sphere Eversion, Vol. IV: Curves in the Plane"
date: 2026-08-17 12:03:00
categories: differential topology
mathjax: true
---

*Sphere Eversion:* [I](/blog/2026/08/17/circling-the-sphere) · [II](/blog/2026/08/17/circling-the-sphere-Vol-II) · [III](/blog/2026/08/17/circling-the-sphere-Vol-III) · **IV** · [V](/blog/2026/08/17/circling-the-sphere-Vol-V) · [VI](/blog/2026/08/17/circling-the-sphere-Vol-VI)

{% include eversion-kit.html %}

*One dimension down, eversion is impossible, and the reason is an integer. This volume finds the integer, proves it cannot change, and shows exactly what goes wrong when you cheat.*

Recall from [Vol. III](/blog/2026/08/17/circling-the-sphere-Vol-III): an immersion is a smooth map whose derivative never drops rank, and a regular homotopy is a path of immersions. Everting $S^2$ means joining $\iota(p)=p$ to $\alpha(p)=-p$ by such a path. Before trying, do the same thing for $S^1$ in $\mathbb{R}^2$.

<div class="cs-toc">
<strong>Contents</strong>
<ol>
  <li><a href="#circling-in-one-dimension-less">circling in one dimension less</a></li>
  <li><a href="#whitney-graustein">Whitney–Graustein</a></li>
  <li><a href="#the-gauss-map-is-not-the-obstruction">the gauss map is not the obstruction</a></li>
</ol>
</div>

---

# circling in one dimension less
{: #circling-in-one-dimension-less}
<div class="cs-q">
<strong>Student.</strong> Why can't we just push it through? And if a sphere can turn inside out, can a circle?
</div>

<div class="cs-a">
<strong>Teacher.</strong> A circle cannot, not in the plane. That is the Whitney–Graustein theorem, and it is the reason eversion feels impossible.
</div>

An immersed closed curve $\gamma:S^1\to\mathbb{R}^2$ has a unit tangent $\mathbf{T}(t)=\gamma'(t)/\lVert\gamma'(t)\rVert\in S^1$. The **turning number** is how many times $\mathbf{T}$ wraps the unit circle,

$$\tau(\gamma)=\frac{1}{2\pi}\bigl(\theta(2\pi)-\theta(0)\bigr)=\frac{1}{2\pi}\int_{S^1}d\theta,\qquad \mathbf{T}=(\cos\theta,\sin\theta).$$

For $\gamma(t)=(\cos t,\sin t)$ one has $\mathbf{T}(t)=(-\sin t,\cos t)$ and $\tau=+1$. For the reflected parametrization $\bar\gamma(t)=(\cos t,-\sin t)$ one has $\tau=-1$. Turning number is an integer and varies continuously under regular homotopy, so it cannot jump. Therefore $\gamma$ and $\bar\gamma$ lie in different path-components of $\operatorname{Imm}(S^1,\mathbb{R}^2)$. The figure-eight $(\sin 2t,\,\sin t)$ has $\tau=0$.


Step through five curves. On the left, $\gamma$ and its unit tangent $\mathbf{T}$. On the right, the direction of $\mathbf{T}$ is plotted as a polar angle with time as the radius, so that the path of $\mathbf{T}$ unrolls into a spiral instead of retracing the same circle. Count how many times the spiral goes around the centre. That integer is the obstruction. Written as a map $\mathbf{T}:S^1\to S^1$, it is the degree of $\mathbf{T}$, the element of $\pi&#95;{1}(S^1)=\mathbb{Z}$ from [Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II).

<div class="mviz" id="ev-turn" tabindex="0" aria-label="Turning number of five closed curves">
  <div class="mv-title" id="ev-turn-title"></div>
  <svg id="ev-turn-svg" viewBox="0 0 700 330" role="img" aria-label="Left: a closed curve with its unit tangent. Right: the direction of the tangent, plotted with time as radius.">
    <defs><marker id="ev-turn-head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#c98500"/></marker></defs>
    <text x="175" y="20" text-anchor="middle" font-size="13" style="fill:#c3c2b7">the curve γ</text>
    <text x="525" y="20" text-anchor="middle" font-size="13" style="fill:#c3c2b7">direction of T (angle) against time (radius)</text>
    <line x1="350" y1="30" x2="350" y2="315" stroke="#2a2a2a"/>
    <g id="ev-turn-ref"></g>
    <path id="ev-turn-curve" fill="none" stroke="#3987e5" stroke-width="2.5" stroke-linejoin="round"/>
    <path id="ev-turn-spiral" fill="none" stroke="#d95926" stroke-width="2.5" stroke-linejoin="round"/>
    <line id="ev-turn-ray" stroke="#4a4a4a" stroke-width="1" stroke-dasharray="3 3"/>
    <line id="ev-turn-tan" stroke="#c98500" stroke-width="2.5" marker-end="url(#ev-turn-head)"/>
    <circle id="ev-turn-pt" r="5.5" fill="#f0f0f0" stroke="#121212" stroke-width="2"/>
    <circle id="ev-turn-sp" r="5.5" fill="#f0f0f0" stroke="#121212" stroke-width="2"/>
    <circle cx="525" cy="170" r="3" fill="#c3c2b7"/>
  </svg>
  <div class="mv-detail" id="ev-turn-detail"></div>
  <div class="mv-controls">
    <button type="button" class="mv-prev">◀ Back</button>
    <button type="button" class="mv-next">Next ▶</button>
    <button type="button" id="ev-turn-play">Pause</button>
    <span class="mv-key"><b style="background:#3987e5"></b>γ<b style="background:#c98500"></b>T<b style="background:#d95926"></b>angle of T, unwrapped</span>
    <span class="mv-step"></span>
  </div>
</div>
<p class="cs-cap">Right panel: the orange trace sits at polar angle equal to the direction of $\mathbf{T}(t)$ and at radius growing with $t$, so windings stack up instead of overlapping. The number of times it goes around the centre, counted with sign, is $\tau$.</p>
<script>
(function () {
  var root = document.getElementById('ev-turn');
  if (!root || !window.EV) return;
  var L = function (a) {
    return { f: function (t) { return [Math.cos(t) + a * Math.cos(2 * t), Math.sin(t) + a * Math.sin(2 * t)]; },
             df: function (t) { return [-Math.sin(t) - 2 * a * Math.sin(2 * t), Math.cos(t) + 2 * a * Math.cos(2 * t)]; } };
  };
  var C = [
    { name: 'circle', title: 'The circle γ(t) = (cos t, sin t). T turns once, counter-clockwise: τ = +1.',
      f: function (t) { return [Math.cos(t), Math.sin(t)]; }, df: function (t) { return [-Math.sin(t), Math.cos(t)]; }, s: 105, cx: 0 },
    { name: 'reflected circle', title: 'The same circle run clockwise, γ(t) = (cos t, −sin t). T turns once the other way: τ = −1.',
      f: function (t) { return [Math.cos(t), -Math.sin(t)]; }, df: function (t) { return [-Math.sin(t), -Math.cos(t)]; }, s: 105, cx: 0 },
    { name: 'figure-eight', title: 'The figure-eight (sin 2t, sin t). T swings one way on the top lobe and back on the bottom: τ = 0.',
      f: function (t) { return [Math.sin(2 * t), Math.sin(t)]; }, df: function (t) { return [2 * Math.cos(2 * t), Math.cos(t)]; }, s: 118, cx: 0 },
    { name: 'curl', title: 'A circle with an inner curl, (cos t + 0.8 cos 2t, sin t + 0.8 sin 2t). The curl adds a full extra turn: τ = 2.',
      f: L(0.8).f, df: L(0.8).df, s: 78, cx: -0.42 },
    { name: 'rounded triangle', title: 'A rounded triangle (cos t + 0.2 cos 2t, sin t − 0.2 sin 2t). Wobbly, but T still turns exactly once: τ = +1. Wobbles do not count.',
      f: function (t) { return [Math.cos(t) + 0.2 * Math.cos(2 * t), Math.sin(t) - 0.2 * Math.sin(2 * t)]; },
      df: function (t) { return [-Math.sin(t) - 0.4 * Math.sin(2 * t), Math.cos(t) - 0.4 * Math.cos(2 * t)]; }, s: 100, cx: 0 }
  ];
  var N = 600, cur = 0, u = 0, playing = true, last = 0, angs = [], tau = 0;
  var CX = 175, CY = 170, SX = 525, R0 = 34, R1 = 136;
  var gx = function (p, c) { return CX + c.s * (p[0] + c.cx); }, gy = function (p, c) { return CY - c.s * p[1]; };
  function unwrapped(c) {
    var out = [], prev = null;
    for (var j = 0; j <= N; j++) {
      var d = c.df(2 * Math.PI * j / N), a = Math.atan2(d[1], d[0]);
      if (prev !== null) { while (a - prev > Math.PI) a -= 2 * Math.PI; while (a - prev < -Math.PI) a += 2 * Math.PI; }
      out.push(a); prev = a;
    }
    return out;
  }
  function spiralPt(j) { var r = R0 + (R1 - R0) * j / N; return [SX + r * Math.cos(angs[j]), CY - r * Math.sin(angs[j])]; }
  var ref = document.getElementById('ev-turn-ref');
  [R0, R1].forEach(function (r) { EV.el('circle', { cx: SX, cy: CY, r: r, fill: 'none', stroke: '#2a2a2a' }, ref); });
  EV.el('line', { x1: SX, y1: CY, x2: SX + R1 + 8, y2: CY, stroke: '#2a2a2a' }, ref);
  function draw() {
    var c = C[cur], j = Math.round(u * N), t = 2 * Math.PI * j / N, p = c.f(t), d = c.df(t), sp = Math.hypot(d[0], d[1]);
    var pt = document.getElementById('ev-turn-pt'); pt.setAttribute('cx', gx(p, c)); pt.setAttribute('cy', gy(p, c));
    var tan = document.getElementById('ev-turn-tan'), k = 38 / sp;
    tan.setAttribute('x1', gx(p, c)); tan.setAttribute('y1', gy(p, c));
    tan.setAttribute('x2', gx(p, c) + k * d[0]); tan.setAttribute('y2', gy(p, c) - k * d[1]);
    var pts = []; for (var i = 0; i <= j; i++) pts.push(spiralPt(i));
    document.getElementById('ev-turn-spiral').setAttribute('d', EV.path(pts));
    var e = spiralPt(j), s2 = document.getElementById('ev-turn-sp'), ray = document.getElementById('ev-turn-ray');
    s2.setAttribute('cx', e[0]); s2.setAttribute('cy', e[1]);
    ray.setAttribute('x1', SX); ray.setAttribute('y1', CY); ray.setAttribute('x2', e[0]); ray.setAttribute('y2', e[1]);
    var so = (angs[j] - angs[0]) / (2 * Math.PI);
    document.getElementById('ev-turn-detail').textContent = 'turning so far (Δθ / 2π) = ' + (so < -0.005 ? '−' : '') + Math.abs(so).toFixed(2) + '   ·   closed curve: τ = ' + (tau < 0 ? '−' : tau > 0 ? '+' : '') + Math.abs(tau);
  }
  function show(i) {
    cur = i; u = 0;
    var c = C[i], pts = [];
    for (var j = 0; j <= N; j++) { var p = c.f(2 * Math.PI * j / N); pts.push([gx(p, c), gy(p, c)]); }
    document.getElementById('ev-turn-curve').setAttribute('d', EV.path(pts));
    document.getElementById('ev-turn-title').textContent = c.title;
    angs = unwrapped(c);
    tau = Math.round((angs[N] - angs[0]) / (2 * Math.PI));
    draw();
  }
  var btn = document.getElementById('ev-turn-play');
  btn.addEventListener('click', function () { playing = !playing; btn.textContent = playing ? 'Pause' : 'Play'; });
  EV.stepper({ root: root, n: C.length, render: show });
  var vis = true;
  if (window.IntersectionObserver) new IntersectionObserver(function (e) { vis = e[0].isIntersecting; }).observe(root);
  (function tick(ts) {
    requestAnimationFrame(tick);
    var dt = Math.min(50, ts - (last || ts)); last = ts;
    if (!playing || !vis) return;
    u += 0.00011 * dt;
    if (u > 1.12) u = 0;
    var h = u; u = Math.min(u, 1); draw(); u = h;
  })(0);
})();
</script>


---

# whitney--graustein
{: #whitney-graustein}
<div class="ev-def"><strong>Theorem (Whitney 1937, conjectured by Graustein).</strong> Two immersions $S^1\to\mathbb{R}^2$ are regularly homotopic if and only if they have the same turning number.</div>

**Why $\tau$ cannot change.** Along a regular homotopy $\gamma&#95;{s}$ the velocity $\gamma&#95;{s}'(t)$ is never zero, so $\mathbf{T}&#95;{s}=\gamma&#95;{s}'/\lVert\gamma&#95;{s}'\rVert$ is defined and depends continuously on $(s,t)$. Then $\tau(\gamma&#95;{s})$ is a continuous function of $s$ with values in $\mathbb{Z}$. By [Vol. I](/blog/2026/08/17/circling-the-sphere), a continuous map from the connected space $[0,1]$ to the discrete space $\mathbb{Z}$ is constant. That is the whole proof, and it uses regularity exactly once: to divide by $\lVert\gamma&#95;{s}'\rVert$.

Drop regularity and the argument breaks, visibly. The family below is a perfectly good homotopy. At one instant its velocity vanishes, and at that instant, and only then, $\tau$ jumps.

<div class="mviz" id="ev-cusp" tabindex="0" aria-label="A one-parameter family of curves whose turning number jumps from 1 to 2 through a cusp">
  <div class="mv-title" id="ev-cusp-title"></div>
  <svg id="ev-cusp-svg" viewBox="0 0 700 330" role="img" aria-label="Left: the curve gamma a with its velocity at t equals pi. Right: the direction of its tangent against time.">
    <defs><marker id="ev-cusp-head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#c98500"/></marker></defs>
    <text x="175" y="20" text-anchor="middle" font-size="13" style="fill:#c3c2b7">γₐ(t) = (cos t + a cos 2t, sin t + a sin 2t)</text>
    <text x="525" y="20" text-anchor="middle" font-size="13" style="fill:#c3c2b7">direction of T against time</text>
    <line x1="350" y1="30" x2="350" y2="315" stroke="#2a2a2a"/>
    <g id="ev-cusp-ref"></g>
    <path id="ev-cusp-curve" fill="none" stroke="#3987e5" stroke-width="2.5" stroke-linejoin="round"/>
    <path id="ev-cusp-spiral" fill="none" stroke="#d95926" stroke-width="2.5" stroke-linejoin="round"/>
    <circle id="ev-cusp-ring" r="12" fill="none" stroke="#d95926" stroke-width="2" stroke-dasharray="3 3"/>
    <line id="ev-cusp-vel" stroke="#c98500" stroke-width="2.5" marker-end="url(#ev-cusp-head)"/>
    <circle id="ev-cusp-pt" r="5.5" fill="#f0f0f0" stroke="#121212" stroke-width="2"/>
    <text id="ev-cusp-tau" x="525" y="176" text-anchor="middle" font-size="18" font-weight="600"></text>
  </svg>
  <div class="mv-detail" id="ev-cusp-detail"></div>
  <div class="mv-controls">
    <label>a <input type="range" id="ev-cusp-a" min="0" max="100" value="30"> <span id="ev-cusp-av">0.30</span></label>
    <button type="button" id="ev-cusp-half">a = ½</button>
    <button type="button" id="ev-cusp-play">Sweep</button>
    <span class="mv-key"><b style="background:#c98500"></b>γₐ′(π) = (0, 2a − 1)</span>
  </div>
</div>
<p class="cs-cap">Drag $a$ across $\tfrac12$. The white dot is $\gamma&#95;{a}(\pi)$ and the gold arrow is the velocity there, $(0,\,2a-1)$. It shrinks, vanishes at $a=\tfrac12$ (a cusp: the curve is not an immersion), and reappears pointing the other way. On the right, $\tau$ jumps from $1$ to $2$ at exactly that instant and at no other.</p>
<script>
(function () {
  var root = document.getElementById('ev-cusp');
  if (!root || !window.EV) return;
  var N = 720, CX = 175, CY = 172, S = 72, SH = -0.45, SX = 525, R0 = 34, R1 = 136;
  var slider = document.getElementById('ev-cusp-a');
  var f = function (a, t) { return [Math.cos(t) + a * Math.cos(2 * t), Math.sin(t) + a * Math.sin(2 * t)]; };
  var df = function (a, t) { return [-Math.sin(t) - 2 * a * Math.sin(2 * t), Math.cos(t) + 2 * a * Math.cos(2 * t)]; };
  var X = function (p) { return CX + S * (p[0] + SH); }, Y = function (p) { return CY - S * p[1]; };
  var ref = document.getElementById('ev-cusp-ref');
  [R0, R1].forEach(function (r) { EV.el('circle', { cx: SX, cy: CY, r: r, fill: 'none', stroke: '#2a2a2a' }, ref); });
  function fmt(v) { var r = Math.round(v * 100) / 100; return (r < 0 ? '−' : '') + Math.abs(r).toFixed(2); }
  function draw(a) {
    var cp = [], sp = [], prev = null, first = null;
    for (var j = 0; j <= N; j++) {
      var t = 2 * Math.PI * j / N, p = f(a, t), d = df(a, t);
      cp.push([X(p), Y(p)]);
      if (Math.hypot(d[0], d[1]) < 1e-9) continue;
      var ang = Math.atan2(d[1], d[0]);
      if (prev !== null) { while (ang - prev > Math.PI) ang -= 2 * Math.PI; while (ang - prev < -Math.PI) ang += 2 * Math.PI; }
      if (first === null) first = ang;
      prev = ang;
      var r = R0 + (R1 - R0) * j / N;
      sp.push([SX + r * Math.cos(ang), CY - r * Math.sin(ang)]);
    }
    document.getElementById('ev-cusp-curve').setAttribute('d', EV.path(cp));
    document.getElementById('ev-cusp-spiral').setAttribute('d', EV.path(sp));
    var zero = Math.abs(2 * a - 1) < 1e-9, tau = a < 0.5 ? 1 : 2; // γ′ = i·e^(it)·(1 + 2a·e^(it)): one turn, plus one more once 1 + 2a·e^(it) winds round 0
    var p0 = f(a, Math.PI), v = 2 * a - 1, k = 70;
    var pt = document.getElementById('ev-cusp-pt'), ring = document.getElementById('ev-cusp-ring'), vel = document.getElementById('ev-cusp-vel');
    pt.setAttribute('cx', X(p0)); pt.setAttribute('cy', Y(p0));
    ring.setAttribute('cx', X(p0)); ring.setAttribute('cy', Y(p0)); ring.setAttribute('opacity', zero ? 1 : 0);
    vel.setAttribute('x1', X(p0)); vel.setAttribute('y1', Y(p0)); vel.setAttribute('x2', X(p0)); vel.setAttribute('y2', Y(p0) - k * v);
    vel.setAttribute('opacity', Math.abs(v) < 0.02 ? 0 : 1);
    document.getElementById('ev-cusp-tau').textContent = zero ? 'τ undefined' : 'τ = ' + tau;
    document.getElementById('ev-cusp-av').textContent = a.toFixed(2);
    document.getElementById('ev-cusp-title').textContent = zero
      ? 'a = ½: the velocity at t = π is zero. This curve is not an immersion; it is the only moment the turning number is allowed to change.'
      : a < 0.5 ? 'a < ½: a dented circle. The inner dent tightens as a grows, but T still turns once. τ = 1.'
      : 'a > ½: the dent has turned into a small loop. That loop is a full extra turn of T. τ = 2.';
    document.getElementById('ev-cusp-detail').textContent = 'γₐ′(π) = (0, ' + fmt(v) + ')   |γₐ′(π)| = ' + fmt(Math.abs(v)) + (zero ? '   ← rank drop' : '');
  }
  function fromSlider() { draw(slider.value / 100); }
  slider.addEventListener('input', function () { playing = false; btn.textContent = 'Sweep'; fromSlider(); });
  document.getElementById('ev-cusp-half').addEventListener('click', function () { playing = false; btn.textContent = 'Sweep'; slider.value = 50; fromSlider(); });
  var btn = document.getElementById('ev-cusp-play'), playing = false, ph = 0, last = 0, vis = true;
  btn.addEventListener('click', function () { playing = !playing; btn.textContent = playing ? 'Stop' : 'Sweep'; ph = Math.asin(Math.max(-1, Math.min(1, (slider.value / 100 - 0.5) / 0.35))); });
  if (window.IntersectionObserver) new IntersectionObserver(function (e) { vis = e[0].isIntersecting; }).observe(root);
  (function tick(ts) {
    requestAnimationFrame(tick);
    var dt = Math.min(50, ts - (last || ts)); last = ts;
    if (!playing || !vis) return;
    ph += 0.0009 * dt;
    var a = 0.5 + 0.35 * Math.sin(ph);
    slider.value = Math.round(a * 100);
    draw(a);
  })(0);
  fromSlider();
})();
</script>

The computation behind the picture: with $z=e^{it}$, $\gamma&#95;{a}=z+az^2$ and $\gamma&#95;{a}'=iz\,(1+2az)$. The factor $iz$ turns once. The factor $1+2az$ winds around $0$ once if $2a>1$ and not at all if $2a<1$. So $\tau=1$ for $a<\tfrac12$, $\tau=2$ for $a>\tfrac12$, and at $a=\tfrac12$ the factor vanishes at $z=-1$, which is $t=\pi$.

**Why equal $\tau$ is enough.** Rescale both curves to length $2\pi$ and parametrize by arc length (both steps are regular homotopies), so $\gamma&#95;{i}'(t)=e^{i\theta&#95;{i}(t)}$ with $\theta&#95;{i}(2\pi)-\theta&#95;{i}(0)=2\pi\tau$. Interpolate the *angles*, not the curves: $\theta&#95;{s}=(1-s)\theta&#95;{0}+s\theta&#95;{1}$. Integrating $e^{i\theta&#95;{s}}$ need not give a closed curve, so subtract the average:

$$\gamma_s(t)=\gamma_s(0)+\int_0^t\bigl(e^{i\theta_s(u)}-c_s\bigr)\,du,\qquad c_s=\frac{1}{2\pi}\int_0^{2\pi}e^{i\theta_s(u)}\,du.$$

Now $\gamma&#95;{s}(2\pi)=\gamma&#95;{s}(0)$. The velocity $e^{i\theta&#95;{s}}-c&#95;{s}$ is nonzero as long as $\lvert c&#95;{s}\rvert<1$, and an average of unit vectors has length $1$ only if they all point the same way. When $\tau\neq0$ the angle $\theta&#95;{s}$ must move, so they do not. (When $\tau=0$ one perturbs first to avoid a constant $\theta&#95;{s}$.) At $s=0$ and $s=1$, $c&#95;{s}=0$ because the original curves close up, so the family starts at $\gamma&#95;{0}$ and ends at $\gamma&#95;{1}$.

So the circle cannot be everted in the plane. Turning it inside out reverses the direction of travel, which sends $\tau=+1$ to $\tau=-1$, and no regular homotopy connects them.

The surprise is dimensional. The turning number of a curve is an element of $\pi&#95;{1}(S^1)=\mathbb{Z}$. For a surface in $\mathbb{R}^3$ the analogous invariant lives in $\pi&#95;{2}(V&#95;{3,2})$, and that group is $0$. One extra dimension is enough room for the obstruction to die.


---

# the gauss map is not the obstruction
{: #the-gauss-map-is-not-the-obstruction}
<div class="cs-q">
<strong>Student.</strong> So what invariant do we actually compute? The model mentioned Jacobians staying positive, and also something called the hairy ball theorem of Smale.
</div>

<div class="cs-a">
<strong>Teacher.</strong> The hairy ball theorem is Poincaré–Brouwer: $S^2$ admits no continuous nowhere-zero tangent vector field. Smale proved a classification of immersions. Different theorem, different decade. The Jacobian-sign story is a confusion with local diffeomorphisms of $\mathbb{R}^n$. What we do compute is a <em>tangential</em> invariant, and its coarsest shadow is the Gauss map.
</div>

Given an immersion $f$,

$$\mathbf{n}_f=\frac{\mathbf{f}_u\times\mathbf{f}_v}{\lVert\mathbf{f}_u\times\mathbf{f}_v\rVert}:S^2\to S^2.$$

The **degree** of a map $g:S^n\to S^n$ is the integer that records signed coverings of the target. For the inclusion, $\mathbf{n}&#95;{\iota}(p)=p$, so $\deg\mathbf{n}&#95;{\iota}=1$. Degree is a regular-homotopy invariant (an integer moving continuously cannot jump). Gauss–Bonnet supplies the same integer without Smale: $\deg\mathbf{n}=\tfrac12\chi(S^2)=1$. Every immersion $S^2\looparrowright\mathbb{R}^3$ has Gauss degree $1$. The everted sphere does too. Degree does not forbid eversion.

The canvas is an ellipsoid, not a round sphere, so that $\mathbf{n}$ is not the identity. For

$$\mathbf{f}(\theta,\varphi)=(a\sin\theta\cos\varphi,\;b\sin\theta\sin\varphi,\;c\cos\theta)$$

the Gauss map is the normalization of $(x/a^2,\,y/b^2,\,z/c^2)$. The ellipsoid is convex, so its Gauss map is a bijection onto $S^2$: it covers the target exactly once, degree $1$. The orange point on the right follows the unit normal as the white point tours the ellipsoid.

<div id="cs-gauss" class="cs-stage" style="height:440px;">
  <div class="cs-hud cs-hud-tl">left: ellipsoid f<br>right: n<sub>f</sub> on the unit sphere</div>
  <div class="cs-hud cs-hud-tr" id="cs-gauss-hud">n</div>
</div>
<p class="cs-cap">$\mathbf{n}&#95;{f}=(\mathbf{f}&#95;{\theta}\times\mathbf{f}&#95;{\varphi})/\lVert\cdot\rVert$. White on the left is a point of the surface and the gold arrow its unit normal; orange on the right is the same unit vector, placed on the target sphere. The image of $\mathbf{n}&#95;{f}$ is the whole target sphere, once.</p>

<script>
CS.mount({
  id: 'cs-gauss',
  height: 440,
  cam: [0, 0.2, 5.4],
  rotX: 0.2,
  setup: function (api) {
    var T = api.THREE;
    var a = 1.15, b = 0.75, c = 0.55;
    var ell = new T.SphereGeometry(1, 40, 28);
    var pa = ell.getAttribute('position');
    for (var i = 0; i < pa.count; i++) {
      pa.array[3 * i]     *= a;
      pa.array[3 * i + 1] *= b;
      pa.array[3 * i + 2] *= c;
    }
    pa.needsUpdate = true;
    ell.computeVertexNormals();
    var left = new T.Group();
    left.position.x = -1.55;
    left.add(new T.Mesh(ell, new T.MeshStandardMaterial({
      color: 0x3987e5, metalness: 0.25, roughness: 0.45, transparent: true, opacity: 0.72, side: T.DoubleSide
    })));
    left.add(new T.Mesh(ell, new T.MeshBasicMaterial({ color: 0x9ec3f0, wireframe: true, transparent: true, opacity: 0.12 })));
    var sph = new T.Mesh(new T.SphereGeometry(1, 32, 24), new T.MeshStandardMaterial({
      color: 0x3a3a3a, metalness: 0.2, roughness: 0.6, transparent: true, opacity: 0.35, side: T.DoubleSide
    }));
    var right = new T.Group();
    right.position.x = 1.7;
    right.add(sph);
    right.add(new T.Mesh(sph.geometry, new T.MeshBasicMaterial({ color: 0x8a8a8a, wireframe: true, transparent: true, opacity: 0.2 })));
    api.group.add(left);
    api.group.add(right);
    var pL = new T.Mesh(new T.SphereGeometry(0.05, 12, 12), new T.MeshStandardMaterial({ color: 0xf0f0f0, emissive: 0x777777, emissiveIntensity: 0.35 }));
    var pR = new T.Mesh(new T.SphereGeometry(0.06, 12, 12), new T.MeshStandardMaterial({ color: 0xd95926, emissive: 0x7a2e10, emissiveIntensity: 0.4 }));
    left.add(pL); right.add(pR);
    var arr = new T.ArrowHelper(new T.Vector3(1, 0, 0), new T.Vector3(), 0.55, 0xc98500, 0.1, 0.07);
    left.add(arr);
    var hud = document.getElementById('cs-gauss-hud');
    var u = 0;
    return function () {
      u += 0.01;
      var th = 0.55 + 0.85 * Math.sin(u * 0.37);
      var ph = u * 0.7;
      var sth = Math.sin(th), cth = Math.cos(th), sph = Math.sin(ph), cph = Math.cos(ph);
      var p = new T.Vector3(a * sth * cph, b * sth * sph, c * cth);
      var nx = p.x / (a * a), ny = p.y / (b * b), nz = p.z / (c * c);
      var n = new T.Vector3(nx, ny, nz).normalize();
      pL.position.copy(p);
      arr.position.copy(p);
      arr.setDirection(n);
      pR.position.copy(n);
      if (hud) {
        hud.innerHTML = 'n = (' + n.x.toFixed(2) + ', ' + n.y.toFixed(2) + ', ' + n.z.toFixed(2) + ')';
      }
    };
  }
});
</script>

The Gauss map remembers only the normal $\mathbf{n}=\mathbf{f}&#95;{u}\times\mathbf{f}&#95;{v}/\lVert\cdot\rVert$, and its degree is the same for every immersed sphere. The circle case suggests the right move: in the plane the invariant was the direction of the *whole* derivative $\gamma'$, not a normal. For surfaces the whole derivative is a pair of vectors, a 2-frame. Where that pair lives, and why the space it lives in has no room for an obstruction, is the next volume.

---

**Next:** [Vol. V: Frames and Smale's Theorem](/blog/2026/08/17/circling-the-sphere-Vol-V)

*Sphere Eversion:* [Vol. I](/blog/2026/08/17/circling-the-sphere) · [Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II) · [Vol. III](/blog/2026/08/17/circling-the-sphere-Vol-III) · **Vol. IV** · [Vol. V](/blog/2026/08/17/circling-the-sphere-Vol-V) · [Vol. VI](/blog/2026/08/17/circling-the-sphere-Vol-VI)
