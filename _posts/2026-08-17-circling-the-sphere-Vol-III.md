---
layout: post
title: "Back-of-the-Envelope: Sphere Eversion, Vol. III: Manifolds and Immersions"
date: 2026-08-17 12:02:00
categories: differential topology
mathjax: true
---

*Sphere Eversion:* [I](/blog/2026/08/17/circling-the-sphere) · [II](/blog/2026/08/17/circling-the-sphere-Vol-II) · **III** · [IV](/blog/2026/08/17/circling-the-sphere-Vol-IV) · [V](/blog/2026/08/17/circling-the-sphere-Vol-V) · [VI](/blog/2026/08/17/circling-the-sphere-Vol-VI)

{% include eversion-kit.html %}

*Calculus enters. Charts, tangent vectors, the Jacobian that must not drop rank, and the first honest definition of the word "eversion".*

In [Vol. I](/blog/2026/08/17/circling-the-sphere) we built topological spaces and continuity; in [Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II) we built paths, homotopies, and $\pi&#95;{1}$. Topology alone cannot see a crease: a homotopy is allowed to squash a sphere flat, fold it, and unfold it. The eversion problem is only interesting once we ask for *smooth* maps whose derivative never degenerates. This volume adds exactly that much calculus.

The boxed questions are from the Phi-3 transcript described in Vol. I; the answers are the corrections.

<div class="cs-toc">
<strong>Contents</strong>
<ol>
  <li><a href="#the-two-sphere-locally-flat">the two-sphere, locally flat</a></li>
  <li><a href="#immersions-and-the-matrix-that-must-not-drop-rank">immersions, and the matrix that must not drop rank</a></li>
  <li><a href="#the-homotopy-that-is-not-regular">the homotopy that is not regular</a></li>
</ol>
</div>

---

# the two-sphere, locally flat
{: #the-two-sphere-locally-flat}
<div class="cs-q">
<strong>Student.</strong> What is a manifold? What is a differentiable manifold? Give an example. Then give differentiable coordinates on $S^2$ and take a derivative at $(1,0,0)$.
</div>

<div class="cs-a">
<strong>Teacher.</strong> A manifold is a space that is Euclidean in the small. Formally, a smooth $n$-manifold is a Hausdorff space covered by charts $\varphi&#95;{\alpha}: U&#95;{\alpha}\to\mathbb{R}^n$ whose transition maps $\varphi&#95;{\beta}\circ\varphi&#95;{\alpha}^{-1}$ are $C^\infty$. You already know one: the surface of the Earth. No single paper map covers it, but an atlas does, and the overlap rules are smooth.
</div>

The **2-sphere** is the set of unit vectors,

$$S^2=\bigl\{(x,y,z)\in\mathbb{R}^3:x^2+y^2+z^2=1\bigr\}.$$

Spherical coordinates are a pair of charts (you need at least two: the azimuth $\varphi$ is not a global coordinate). On the complement of a meridian,

$$\mathbf{r}(\theta,\varphi)=\bigl(\sin\theta\cos\varphi,\;\sin\theta\sin\varphi,\;\cos\theta\bigr),\qquad \theta\in(0,\pi),\;\varphi\in(0,2\pi).$$

A **point** is not a function of $(\theta,\varphi)$. The model that answered me computed $\partial&#95;{\theta}(1,0,0)=\mathbf{0}$ and called it a day. The object that has derivatives is the chart:

$$
\begin{aligned}
\mathbf{r}_\theta&=(\cos\theta\cos\varphi,\;\cos\theta\sin\varphi,\;-\sin\theta),\\
\mathbf{r}_\varphi&=(-\sin\theta\sin\varphi,\;\sin\theta\cos\varphi,\;0).
\end{aligned}
$$

At $(1,0,0)$ one has $(\theta,\varphi)=(\pi/2,\,0)$, so

$$\mathbf{r}_\theta=(0,0,-1),\qquad \mathbf{r}_\varphi=(0,1,0),\qquad \mathbf{r}_\theta\times\mathbf{r}_\varphi=(1,0,0)=\mathbf{r}.$$

Those two vectors are a basis of the tangent plane $T&#95;{(1,0,0)}S^2$, the $yz$-plane. Drag the sliders; the blue and orange arrows are exactly $\mathbf{r}&#95;{\theta}$ and $\mathbf{r}&#95;{\varphi}$.

<div id="cs-charts" class="cs-stage" style="height:440px;">
  <div class="cs-hud cs-hud-tl" id="cs-charts-eq">r, r<sub>θ</sub>, r<sub>φ</sub></div>
  <div class="cs-ctrl">
    <label>θ <input type="range" id="cs-th" min="8" max="172" value="90"> <span id="cs-th-v">1.57</span></label>
    <label>φ <input type="range" id="cs-ph" min="0" max="628" value="0"> <span id="cs-ph-v">0</span></label>
  </div>
</div>
<p class="cs-cap">The sphere is the image of $\mathbf{r}$. Blue is $\mathbf{r}&#95;{\theta}$, orange is $\mathbf{r}&#95;{\varphi}$, gold is their cross product $\mathbf{r}&#95;{\theta}\times\mathbf{r}&#95;{\varphi}=\sin\theta\,\mathbf{r}$. At the poles $\sin\theta=0$ and the <em>chart</em> is singular; the sphere is not. That distinction is the whole subject.</p>

<script>
CS.mount({
  id: 'cs-charts',
  height: 440,
  cam: [0, 0.2, 3.6],
  setup: function (api) {
    var T = api.THREE;
    var geo = new T.SphereGeometry(1, 48, 32);
    api.group.add(new T.Mesh(geo, new T.MeshStandardMaterial({
      color: 0x2c3e57, metalness: 0.2, roughness: 0.55, transparent: true, opacity: 0.45, side: T.DoubleSide
    })));
    api.group.add(new T.Mesh(geo, new T.MeshBasicMaterial({
      color: 0x9aa3ad, wireframe: true, transparent: true, opacity: 0.16
    })));
    var pt = new T.Mesh(new T.SphereGeometry(0.045, 16, 16), new T.MeshStandardMaterial({ color: 0xf0f0f0, emissive: 0x888888, emissiveIntensity: 0.3 }));
    api.group.add(pt);
    var aTh = new T.ArrowHelper(new T.Vector3(0, 0, -1), new T.Vector3(1, 0, 0), 0.7, 0x3987e5, 0.12, 0.08);
    var aPh = new T.ArrowHelper(new T.Vector3(0, 1, 0), new T.Vector3(1, 0, 0), 0.7, 0xd95926, 0.12, 0.08);
    var aN  = new T.ArrowHelper(new T.Vector3(1, 0, 0), new T.Vector3(1, 0, 0), 0.55, 0xc98500, 0.1, 0.07);
    api.group.add(aTh); api.group.add(aPh); api.group.add(aN);
    var hud = document.getElementById('cs-charts-eq');
    function sync() {
      var th = parseFloat(document.getElementById('cs-th').value) * Math.PI / 180;
      var ph = parseFloat(document.getElementById('cs-ph').value) / 100;
      document.getElementById('cs-th-v').textContent = th.toFixed(2);
      document.getElementById('cs-ph-v').textContent = ph.toFixed(2);
      var sth = Math.sin(th), cth = Math.cos(th), sph = Math.sin(ph), cph = Math.cos(ph);
      var p = new T.Vector3(sth * cph, sth * sph, cth);
      var dth = new T.Vector3(cth * cph, cth * sph, -sth);
      var dph = new T.Vector3(-sth * sph, sth * cph, 0);
      var n = new T.Vector3().crossVectors(dth, dph);
      var nlen = n.length();
      pt.position.copy(p);
      aTh.position.copy(p); aPh.position.copy(p); aN.position.copy(p);
      if (dth.length() > 1e-8) aTh.setDirection(dth.clone().normalize());
      if (dph.length() > 1e-8) aPh.setDirection(dph.clone().normalize());
      if (nlen > 1e-8) aN.setDirection(n.clone().normalize());
      aTh.setLength(0.65, 0.12, 0.08);
      aPh.setLength(Math.min(0.65, 0.25 + 0.5 * sth), 0.12, 0.08);
      aN.setLength(0.5, 0.1, 0.07);
      if (hud) {
        hud.innerHTML =
          'r = (' + p.x.toFixed(2) + ', ' + p.y.toFixed(2) + ', ' + p.z.toFixed(2) + ')<br>' +
          'r<sub>θ</sub> × r<sub>φ</sub> = sin θ · r<br>' +
          '‖r<sub>θ</sub> × r<sub>φ</sub>‖ = ' + nlen.toFixed(3) + (nlen < 0.08 ? ' · chart singular, sphere fine' : '');
      }
    }
    document.getElementById('cs-th').addEventListener('input', sync);
    document.getElementById('cs-ph').addEventListener('input', sync);
    sync();
    return null;
  }
});
</script>

<div class="cs-q">
<strong>Student.</strong> Give a nonzero derivative — a function that wraps around the sphere.
</div>

<div class="cs-a">
<strong>Teacher.</strong> Take the equator as a curve $\gamma:[0,2\pi]\to S^2$,
$$\gamma(t)=(\cos t,\;\sin t,\;0).$$
Then $\gamma'(t)=(-\sin t,\;\cos t,\;0)\neq\mathbf{0}$. At $t=0$ this is $(0,1,0)$, which is $\mathbf{r}&#95;{\varphi}$ at $(1,0,0)$. The model wrote $\gamma(t)=(\sin(\pi t),0,\cos(\pi t))$ and claimed it was the equator with $\varphi$ fixed at $0$; that is a meridian, a semicircle from north pole to south, and at its midpoint the velocity is $(0,0,-\pi)$, not a trip around the equator. Wrapping around $S^2$ means the image of $\gamma$ is a closed loop that is not contractible in $S^2\setminus\{\text{two poles}\}$. We will need that loop.
</div>

---

# immersions, and the matrix that must not drop rank
{: #immersions-and-the-matrix-that-must-not-drop-rank}
<div class="cs-q">
<strong>Student.</strong> What is an immersion? What is a Jacobian? What happens when the Jacobian determinant is zero, or switches sign?
</div>

<div class="cs-a">
<strong>Teacher.</strong> For $f:\mathbb{R}^n\to\mathbb{R}^m$ the Jacobian is the $m\times n$ matrix of first partials — rows are outputs, columns are inputs. The model wrote $n\times m$. An <strong>immersion</strong> $f:M\to N$ is a smooth map whose differential $df&#95;{p}:T&#95;{p}M\to T&#95;{f(p)}N$ is injective at every $p$. For $f:S^2\to\mathbb{R}^3$ that is the statement that the $3\times 2$ matrix
$$
J_f=\begin{pmatrix}
\partial_u f_1 & \partial_v f_1 \\
\partial_u f_2 & \partial_v f_2 \\
\partial_u f_3 & \partial_v f_3
\end{pmatrix}
$$
has rank $2$ everywhere, equivalently $\mathbf{f}&#95;{u}\times\mathbf{f}&#95;{v}\neq\mathbf{0}$. There is no $2\times 2$ determinant to watch. The only vanishing that matters is that cross product.
</div>

A sign change of $\det J$ for a map $\mathbb{R}^n\to\mathbb{R}^n$ means the map reverses orientation. It does **not** mean a saddle: $f(x,y)=(e^x\cos y,\,e^x\sin y)$ has $\det J=e^{2x}>0$ everywhere (it is a local diffeomorphism, the complex exponential). At $(0,\pi/2)$ one has $\det J=1$, not $-1$, and there is no critical point. Vanishing of $\det J$ *does* mean the inverse-function theorem fails: the map is not a local diffeomorphism there.

Self-intersection is allowed. A figure-eight $\gamma(t)=(\sin 2t,\,\sin t)$ is an immersion — $\gamma'$ never vanishes — and it crosses itself. An **embedding** is an injective immersion (proper, on noncompact manifolds). The standard sphere $\iota(p)=p$ is an embedding. Mid-eversion surfaces are immersions and not embeddings.

Step through three curves. Watch the arrow, not the picture.

<div class="mviz" id="ev-imm" tabindex="0" aria-label="Three curves: embedding, immersion, and a non-immersion">
  <div class="mv-title" id="ev-imm-title"></div>
  <svg id="ev-imm-svg" viewBox="0 0 640 300" role="img" aria-label="A parametrized curve with its velocity vector">
    <defs><marker id="ev-imm-head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#c98500"/></marker></defs>
    <g id="ev-imm-axes"></g>
    <path id="ev-imm-curve" fill="none" stroke="#3987e5" stroke-width="2.5" stroke-linejoin="round"/>
    <g id="ev-imm-mark"></g>
    <line id="ev-imm-vel" stroke="#c98500" stroke-width="2.5" marker-end="url(#ev-imm-head)"/>
    <circle id="ev-imm-pt" r="6" fill="#f0f0f0" stroke="#121212" stroke-width="2"/>
  </svg>
  <div class="mv-detail" id="ev-imm-detail"></div>
  <div class="mv-controls">
    <button type="button" class="mv-prev">◀ Back</button>
    <button type="button" class="mv-next">Next ▶</button>
    <label>t <input type="range" id="ev-imm-t" min="0" max="1000" value="0"></label>
    <button type="button" id="ev-imm-play">Pause</button>
    <span class="mv-key"><b style="background:#3987e5"></b>γ<b style="background:#c98500"></b>γ′(t)</span>
    <span class="mv-step"></span>
  </div>
</div>
<p class="cs-cap">The gold arrow is the velocity $\gamma'(t)$, drawn at true relative length. An immersion is a curve whose arrow never shrinks to a point. Self-crossings are allowed; stopping is not.</p>
<script>
(function () {
  var root = document.getElementById('ev-imm');
  if (!root || !window.EV) return;
  var svg = document.getElementById('ev-imm-svg'), E = EV.el;
  var C = [
    { title: 'An embedding: γ(t) = (cos t, sin t). The velocity never vanishes and no two times land on the same point.',
      f: function (t) { return [Math.cos(t), Math.sin(t)]; }, df: function (t) { return [-Math.sin(t), Math.cos(t)]; },
      a: 0, b: 2 * Math.PI, s: 105, loop: true, verdict: 'immersion ✓   injective ✓   so an embedding' },
    { title: 'An immersion that is not an embedding: γ(t) = (sin 2t, sin t). It crosses itself at the origin (t = 0 and t = π), yet the arrow never shrinks.',
      f: function (t) { return [Math.sin(2 * t), Math.sin(t)]; }, df: function (t) { return [2 * Math.cos(2 * t), Math.cos(t)]; },
      a: 0, b: 2 * Math.PI, s: 110, loop: true, cross: [0, 0], verdict: 'immersion ✓   injective ✗ (γ(0) = γ(π))' },
    { title: 'Not an immersion: the cusp γ(t) = (t², t³). At t = 0 the velocity (2t, 3t²) is the zero vector; the curve stops dead and turns around.',
      f: function (t) { return [t * t - 0.7, t * t * t]; }, df: function (t) { return [2 * t, 3 * t * t]; },
      a: -1.2, b: 1.2, s: 72, loop: false, cusp: [-0.7, 0], verdict: 'immersion ✗ (γ′(0) = 0)' }
  ];
  var cur = 0, u = 0, playing = true, dir = 1, last = 0;
  var X = function (p, c) { return 320 + c.s * p[0]; }, Y = function (p, c) { return 150 - c.s * p[1]; };
  var slider = document.getElementById('ev-imm-t'), detail = document.getElementById('ev-imm-detail');
  function fmt(v) { var r = Math.round(v * 100) / 100; return (r < 0 ? '−' : '') + Math.abs(r).toFixed(2); }
  function draw() {
    var c = C[cur], t = c.a + (c.b - c.a) * u, p = c.f(t), v = c.df(t), sp = Math.hypot(v[0], v[1]);
    var pt = document.getElementById('ev-imm-pt'), ln = document.getElementById('ev-imm-vel');
    pt.setAttribute('cx', X(p, c)); pt.setAttribute('cy', Y(p, c));
    var k = 0.28;
    ln.setAttribute('x1', X(p, c)); ln.setAttribute('y1', Y(p, c));
    ln.setAttribute('x2', X([p[0] + k * v[0], p[1] + k * v[1]], c)); ln.setAttribute('y2', Y([p[0] + k * v[0], p[1] + k * v[1]], c));
    ln.setAttribute('opacity', sp < 0.02 ? 0 : 1);
    slider.value = Math.round(u * 1000);
    detail.textContent = 't = ' + fmt(t) + '   γ′(t) = (' + fmt(v[0]) + ', ' + fmt(v[1]) + ')   |γ′(t)| = ' + fmt(sp) + (sp < 0.02 ? '   ← zero: rank drops' : '') + '   ·   ' + c.verdict;
  }
  function show(i) {
    cur = i; u = 0; dir = 1;
    var c = C[i], pts = [], N = 400;
    for (var j = 0; j <= N; j++) { var p = c.f(c.a + (c.b - c.a) * j / N); pts.push([X(p, c), Y(p, c)]); }
    document.getElementById('ev-imm-curve').setAttribute('d', EV.path(pts));
    document.getElementById('ev-imm-title').textContent = c.title;
    var m = document.getElementById('ev-imm-mark'); EV.clear(m);
    if (c.cross) E('circle', { cx: X(c.cross, c), cy: Y(c.cross, c), r: 11, fill: 'none', stroke: '#d95926', 'stroke-width': 2, 'stroke-dasharray': '3 3' }, m);
    if (c.cusp) E('circle', { cx: X(c.cusp, c), cy: Y(c.cusp, c), r: 11, fill: 'none', stroke: '#d95926', 'stroke-width': 2, 'stroke-dasharray': '3 3' }, m);
    draw();
  }
  var ax = document.getElementById('ev-imm-axes');
  E('line', { x1: 40, x2: 600, y1: 150, y2: 150, stroke: '#2a2a2a' }, ax);
  E('line', { x1: 320, x2: 320, y1: 12, y2: 288, stroke: '#2a2a2a' }, ax);
  var btn = document.getElementById('ev-imm-play');
  btn.addEventListener('click', function () { playing = !playing; btn.textContent = playing ? 'Pause' : 'Play'; });
  slider.addEventListener('input', function () { playing = false; btn.textContent = 'Play'; u = slider.value / 1000; draw(); });
  EV.stepper({ root: root, n: C.length, render: show });
  var vis = true;
  if (window.IntersectionObserver) new IntersectionObserver(function (e) { vis = e[0].isIntersecting; }).observe(root);
  (function tick(ts) {
    requestAnimationFrame(tick);
    var dt = Math.min(50, ts - (last || ts)); last = ts;
    if (!playing || !vis) return;
    var c = C[cur], rate = c.loop ? 0.00012 : 0.00016;
    u += dir * rate * dt;
    if (c.loop) { if (u > 1) u -= 1; }
    else if (u > 1) { u = 1; dir = -1; } else if (u < 0) { u = 0; dir = 1; }
    draw();
  })(0);
})();
</script>

---

# the homotopy that is not regular
{: #the-homotopy-that-is-not-regular}
<div class="cs-q">
<strong>Student.</strong> Any two $C^2$ immersions of $S^2$ in $E^3$ are regularly homotopic. Here is a proof: $H(x,t)=(1-t)f&#95;{0}(x)+t f&#95;{1}(x)$. Also, what is $S^2\times[0,1]$?
</div>

<div class="cs-a">
<strong>Teacher.</strong> $S^2\times[0,1]$ is a <em>thickened sphere</em>: a spherical shell, not the ball. Each point of $S^2$ grows an interval. A homotopy of maps $S^2\to\mathbb{R}^3$ is a single map
$$F:S^2\times[0,1]\to\mathbb{R}^3.$$
It is a <strong>regular homotopy</strong> when each slice $F(\,\cdot\,,t)$ is an immersion. Straight-line interpolation between immersions is a homotopy of smooth maps and almost never a regular homotopy. It routinely drops rank.
</div>

<div class="ev-def"><strong>Definition (regular homotopy).</strong> A homotopy $F:S^2\times[0,1]\to\mathbb{R}^3$ such that every slice $f&#95;{t}=F(\cdot,t)$ is an immersion and the derivative $df&#95;{t}$ varies continuously with $t$. Equivalently: a path in the space $\operatorname{Imm}(S^2,\mathbb{R}^3)$ with the $C^1$ topology. That is <a href="/blog/2026/08/17/circling-the-sphere-Vol-II">Vol. II</a>'s homotopy, with one extra rule: no slice may crease.</div>

The sock-push is the interpolation from the identity to reflection through the equator,

$$F_s(\theta,\varphi)=\bigl(\sin\theta\cos\varphi,\;\sin\theta\sin\varphi,\;(1-2s)\cos\theta\bigr).$$

A short computation:

$$
\mathbf{F}_\theta\times\mathbf{F}_\varphi=\bigl((1-2s)\sin^2\theta\cos\varphi,\;(1-2s)\sin^2\theta\sin\varphi,\;\sin\theta\cos\theta\bigr),
$$

$$
\bigl\|\mathbf{F}_\theta\times\mathbf{F}_\varphi\bigr\|=\lvert\sin\theta\rvert\sqrt{(1-2s)^2\sin^2\theta+\cos^2\theta}.
$$

At $s=\tfrac12$ this is $\lvert\sin\theta\cos\theta\rvert$, which is zero all along the equator. The image is a disk covered twice, with a fold on the boundary. That is a crease. Colour in the canvas is $\lVert\mathbf{F}&#95;{\theta}\times\mathbf{F}&#95;{\varphi}\rVert$: blue is a healthy tangent plane, orange is rank drop. (The poles are orange at every $s$ for the boring reason that the <em>chart</em> is singular there; watch the equator.)

<div id="cs-crease" class="cs-stage" style="height:460px;">
  <div class="cs-hud cs-hud-tl" id="cs-crease-hud">min ‖F<sub>θ</sub> × F<sub>φ</sub>‖</div>
  <div class="cs-hud cs-hud-tr"><span style="color:#6fa8f0;">rank 2</span><br><span style="color:#f08a5d;">rank drop</span></div>
  <div class="cs-ctrl">
    <label>s <input type="range" id="cs-s" min="0" max="100" value="0"> <span id="cs-s-v">0.00</span></label>
  </div>
</div>
<p class="cs-cap">$F&#95;{s}(\theta,\varphi)=(\sin\theta\cos\varphi,\,\sin\theta\sin\varphi,\,(1-2s)\cos\theta)$. This is <em>not</em> an eversion. At $s=1$ you have reflected the sphere through the $xy$-plane, and at $s=1/2$ you have left $\mathrm{Imm}(S^2,\mathbb{R}^3)$.</p>

<script>
CS.mount({
  id: 'cs-crease',
  height: 460,
  cam: [0, 0.15, 3.7],
  setup: function (api) {
    var T = api.THREE;
    var nTh = 56, nPh = 72;
    var geo = new T.SphereGeometry(1, nPh, nTh);
    var pos = geo.getAttribute('position');
    var orig = new Float32Array(pos.array);
    var col = new Float32Array(pos.count * 3);
    geo.setAttribute('color', new T.BufferAttribute(col, 3));
    var mat = new T.MeshStandardMaterial({
      vertexColors: true, metalness: 0.15, roughness: 0.5,
      side: T.DoubleSide, transparent: true, opacity: 0.92
    });
    api.group.add(new T.Mesh(geo, mat));
    api.group.add(new T.Mesh(geo, new T.MeshBasicMaterial({
      color: 0xe2e8f0, wireframe: true, transparent: true, opacity: 0.08
    })));
    var hud = document.getElementById('cs-crease-hud');
    function jacColor(s, th, ph) {
      var sth = Math.sin(th), cth = Math.cos(th);
      var mag = Math.abs(sth) * Math.sqrt((1 - 2 * s) * (1 - 2 * s) * sth * sth + cth * cth);
      var u = Math.max(0, Math.min(1, mag / 1.0));
      return [0.85 * (1 - u) + 0.22 * u, 0.35 * (1 - u) + 0.53 * u, 0.15 * (1 - u) + 0.9 * u, mag];
    }
    function deform(s) {
      var arr = pos.array;
      var minJ = 1e9;
      for (var i = 0; i < pos.count; i++) {
        var x = orig[3 * i], y = orig[3 * i + 1], z = orig[3 * i + 2];
        var th = Math.acos(Math.max(-1, Math.min(1, z)));
        var ph = Math.atan2(y, x);
        var sth = Math.sin(th), cth = Math.cos(th);
        arr[3 * i]     = sth * Math.cos(ph);
        arr[3 * i + 1] = sth * Math.sin(ph);
        arr[3 * i + 2] = (1 - 2 * s) * cth;
        var c = jacColor(s, th, ph);
        col[3 * i] = c[0]; col[3 * i + 1] = c[1]; col[3 * i + 2] = c[2];
        if (c[3] < minJ) minJ = c[3];
      }
      pos.needsUpdate = true;
      geo.getAttribute('color').needsUpdate = true;
      geo.computeVertexNormals();
      if (hud) {
        hud.innerHTML = 'min ‖F<sub>θ</sub> × F<sub>φ</sub>‖ = ' + minJ.toFixed(3) +
          (minJ < 0.04 ? '<br>crease: not an immersion' : '<br>immersion (away from the chart poles)');
      }
    }
    var sl = document.getElementById('cs-s');
    sl.addEventListener('input', function () {
      var s = parseFloat(this.value) / 100;
      document.getElementById('cs-s-v').textContent = s.toFixed(2);
      deform(s);
    });
    deform(0);
    return null;
  }
});
</script>

An **eversion** is a regular homotopy from the inclusion $\iota(p)=p$ to the antipodal embedding $\alpha(p)=-p$. The map $\alpha$ reverses orientation of $\mathbb{R}^3$ ($\det D\alpha=(-1)^3=-1$), and the outward normal of the image sphere at $-p$ is $-p$, while the pushed tangent frame produces the opposite normal. Inside has become outside. $F&#95;{s}$ ends at the reflection $\rho(x,y,z)=(x,y,-z)$, which is $\alpha$ followed by a half-turn about the $z$-axis. Rotating an immersion keeps it an immersion, so reaching $\rho$ regularly would be as good as reaching $\alpha$. $F&#95;{s}$ gets there, but it cheats: at $s=\tfrac12$ it leaves $\operatorname{Imm}(S^2,\mathbb{R}^3)$.

So the question is sharp now. $\iota$ and $\alpha$ are both immersions (both embeddings, in fact). Is there a path between them in $\operatorname{Imm}(S^2,\mathbb{R}^3)$? The crease homotopy is not one. Before attacking the sphere we drop a dimension and ask the same question of circles in the plane, where the answer is *no* and the reason is an integer.

---

**Next:** [Vol. IV: Curves in the Plane](/blog/2026/08/17/circling-the-sphere-Vol-IV)

*Sphere Eversion:* [Vol. I](/blog/2026/08/17/circling-the-sphere) · [Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II) · **Vol. III** · [Vol. IV](/blog/2026/08/17/circling-the-sphere-Vol-IV) · [Vol. V](/blog/2026/08/17/circling-the-sphere-Vol-V) · [Vol. VI](/blog/2026/08/17/circling-the-sphere-Vol-VI)
