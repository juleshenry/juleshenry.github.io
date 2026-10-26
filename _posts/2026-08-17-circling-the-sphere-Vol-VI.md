---
layout: post
title: "Back-of-the-Envelope: Sphere Eversion, Vol. VI: Seeing the Eversion"
date: 2026-08-17 12:05:00
description: "Corrugations that give a sphere slack, the Bednorz ruled surface formula for the halfway model, and signed volume as a test for halfway."
categories: differential topology
mathjax: true
---

*Sphere Eversion:* [I](/blog/2026/08/17/circling-the-sphere) · [II](/blog/2026/08/17/circling-the-sphere-Vol-II) · [III](/blog/2026/08/17/circling-the-sphere-Vol-III) · [IV](/blog/2026/08/17/circling-the-sphere-Vol-IV) · [V](/blog/2026/08/17/circling-the-sphere-Vol-V) · **VI**

{% include eversion-kit.html %}

*The existence proof is done. This volume is about seeing it: slack, a formula you can type, and an honest way to say "halfway".*

[Vol. V](/blog/2026/08/17/circling-the-sphere-Vol-V) proved that $\iota(p)=p$ and $\alpha(p)=-p$ lie in the same path-component of $\operatorname{Imm}(S^2,\mathbb{R}^3)$. It did not produce a path. Nobody could picture one at first. The first explicit eversions came from Arnold Shapiro (around 1960, unpublished), Tony Phillips (published 1966), and Bernard Morin (late 1960s), who was blind. Here are three windows onto such a path.

<p style="text-align:center;">
  <img src="/blog/assets/2024/eversion/eversion.gif" alt="Thurston's corrugation sphere eversion, from the film Outside In" style="max-width:100%;">
</p>

<div class="cs-toc">
<strong>Contents</strong>
<ol>
  <li><a href="#slack-that-does-not-crease">Slack that does not crease</a></li>
  <li><a href="#a-formula-that-actually-everts-a-band">A formula that actually everts a band</a></li>
  <li><a href="#a-volume-that-must-cross-zero">A volume that must cross zero</a></li>
  <li><a href="#the-arc">The arc</a></li>
</ol>
</div>

---

# Slack that does not crease
{: #slack-that-does-not-crease}
<div class="cs-q">
It is instructive to ask how Thurston turned the sphere inside out.
</div>

<div class="cs-a">
Smale's proof shows that an eversion exists without exhibiting one. What Thurston gave, in the 1970s (animated in the 1994 film <em>Outside In</em>), is a <em>construction</em>, which is itself a proof of Smale's theorem: corrugate the surface so that it has slack, pass the ripples through one another, then iron the ripples out. The local move is a normal oscillation: a wiggle of the surface back and forth along its normal direction.
</div>

The obvious move is to push the northern hemisphere down and the southern one up until they pass through each other. That works everywhere except along the equator. The band joining the two hemispheres is pulled into a tight loop, and pulling a loop tight ends in a crease: the same kink that the turning number of [Vol. IV](/blog/2026/08/17/circling-the-sphere-Vol-IV) says a curve cannot avoid.

Thurston's fix is to corrugate the sphere first, with $k$ ripples running from pole to pole like the segments of a pumpkin:

$$
\mathbf{f}_\varepsilon(\theta,\varphi)=\bigl(1+\varepsilon\sin^k\theta\,\sin(k\varphi)\bigr)\,\mathbf{r}(\theta,\varphi),\qquad 0<\varepsilon<1.
$$

On its own this does nothing. The radial factor stays positive, so every ray from the origin still meets the surface once: it is an embedded sphere, only bumpier. (The power $\sin^k\theta$ keeps the poles smooth, since $\sin^k\theta\sin(k\varphi)$ is the polynomial $\operatorname{Im}(x+iy)^k$.) What the ripples buy is room. With them in place the halves can pass through each other without pulling anything tight. The loops that form sit in the ripples, and rotating the band's two edges half a turn against each other unwinds them. Then the ripples are ironed out. The animation at the top of this page is that sequence: ripples appear, the halves pass through each other, the band twists, the ripples flatten.

---

# A formula that actually everts a band
{: #a-formula-that-actually-everts-a-band}
Existence is not a picture. Every explicit eversion has a *halfway model*, the surface at the midpoint of the movie, where inside and outside are equally exposed. Shapiro and Phillips used a doubly covered Boy surface. Boy's surface (Werner Boy, 1901) is an immersion in $\mathbb{R}^3$ of the projective plane, the sphere with antipodes glued, so running around it twice gives an immersed sphere. Morin found a four-lobed halfway model with a single quadruple point, a point where four sheets of the surface pass through one another, and later Apéry gave one cut out by polynomial equations. A family you can type into a graphics program is due to Adam and Witold Bednorz, *Analytic sphere eversion using ruled surfaces*, arXiv:1711.10466. A *ruled surface* is one swept out by a moving straight line: in the equations below, fixing $\varphi$ and letting $h$ vary traces a line. They take the sphere with its two poles removed, stretched into an infinite cylinder, evert it through a family of ruled surfaces, and then close the two ends back up by a damped inversion. We draw only the cylinder, so that every vertex is the displayed equation, up to one overall scale.

$$
\begin{aligned}
x&= t\cos\varphi + p\sin\bigl((n-1)\varphi\bigr) - h\sin\varphi,\\
y&= t\sin\varphi + p\cos\bigl((n-1)\varphi\bigr) + h\cos\varphi,\\
z&= h\sin(n\varphi) - \frac{t}{n}\cos(n\varphi) - q\,t\,h.
\end{aligned}
$$

Parameters: $n=2$ (the Morin band; $n=3$ gives a band through a Boy surface), $q=\tfrac23$, and $p=1-\lvert qt\rvert$, the paper's choice, which always satisfies their condition for the band to be an immersion (the paper calls it smoothness)

$$(n-1)p\bigl(1-q\lvert t\rvert\bigr)+qt^2>0.$$

The coordinates are $(\varphi,h)\in S^1\times\mathbb{R}$. At $t=0$, $n=2$ this is the ruled halfway model: four sheets through the origin (the quadruple point $Q$), and no preferred side. Sliding $t$ from $-3/2$ to $3/2$ swaps the two rims of the cylinder. That swap, once the poles are sewn back on, is the central step of the sphere eversion.

<div id="cs-bednorz" class="cs-stage" style="height:500px;">
  <div class="cs-hud cs-hud-tl" id="cs-bed-hud">Bednorz ruled band</div>
  <div class="cs-hud cs-hud-tr"><span style="color:#ffd166;">rim A</span> <span style="color:#7ee0b5;">rim B</span></div>
  <div class="cs-ctrl">
    <button type="button" id="cs-bplay">Play</button>
    <label>t <input type="range" id="cs-bt" min="-150" max="150" value="-150"> <span id="cs-bt-v">-1.50</span></label>
  </div>
</div>
<p class="cs-cap">Equation (4) of Bednorz–Bednorz with $n=2$, $q=2/3$, $p=1-\lvert qt\rvert$, $h\in[-2.3,2.3]$, drawn with $z$ up. Press play, or drag $t$, and watch the rims. Rim A starts above rim B and ends below it. Drag to turn the band. At $t=0$ the band is the four-sheeted Morin halfway model. The polar caps are left off, so you see the band only.</p>

<script>
CS.mount({
  id: 'cs-bednorz',
  height: 500,
  cam: [0, 0.6, 6.2],
  rotX: 0.3,
  noSpin: true,
  setup: function (api) {
    var T = api.THREE;
    var H = 2.3, RIM = 0.22, nH = 64, nP = 110, n = 2, q = 2 / 3;
    function bednorz(h, phi, t) {
      var p = 1 - Math.abs(q * t);
      var s = Math.sin(phi), c = Math.cos(phi);
      var sn = Math.sin(n * phi), cn = Math.cos(n * phi);
      var sm = Math.sin((n - 1) * phi), cm = Math.cos((n - 1) * phi);
      return [
        t * c + p * sm - h * s,
        t * s + p * cm + h * c,
        h * sn - (t / n) * cn - q * t * h
      ];
    }
    // One grid per strip of the band: the body, and a thin collar at each rim
    function strip(h0, h1, rows) { return { h0: h0, h1: h1, rows: rows, geo: new T.PlaneGeometry(1, 1, nP, rows) }; }
    var body = strip(-H + RIM, H - RIM, nH);
    var rimA = strip(H - RIM, H, 3);
    var rimB = strip(-H, -H + RIM, 3);
    var strips = [body, rimA, rimB];
    var slider = document.getElementById('cs-bt');
    var playBtn = document.getElementById('cs-bplay');
    var playing = false, dir = 1;
    function fill() {
      var t = parseFloat(slider.value) / 100;
      document.getElementById('cs-bt-v').textContent = t.toFixed(2);
      var maxR = 0;
      strips.forEach(function (st) {
        var arr = st.geo.getAttribute('position').array;
        for (var i = 0; i < arr.length / 3; i++) {
          var col = i % (nP + 1);
          var row = (i / (nP + 1)) | 0;
          var phi = (col / nP) * Math.PI * 2 - Math.PI;
          var h = st.h0 + (st.h1 - st.h0) * (row / st.rows);
          var xyz = bednorz(h, phi, t);
          // the paper's z is vertical; (x, y, z) -> (x, z, -y) is a rotation, so the sides keep their colours
          arr[3 * i] = xyz[0];
          arr[3 * i + 1] = xyz[2];
          arr[3 * i + 2] = -xyz[1];
          var r = Math.hypot(xyz[0], xyz[1], xyz[2]);
          if (r > maxR) maxR = r;
        }
      });
      var sc = maxR > 1e-6 ? 2.15 / maxR : 1;
      strips.forEach(function (st) {
        var attr = st.geo.getAttribute('position');
        for (var i = 0; i < attr.array.length; i++) attr.array[i] *= sc;
        attr.needsUpdate = true;
        st.geo.computeVertexNormals();
      });
      var hud = document.getElementById('cs-bed-hud');
      if (hud) hud.innerHTML = 't = ' + t.toFixed(2) + (Math.abs(t) < 0.03 ? '<br>halfway (Morin)' : '');
    }
    function side(color, s) {
      return new T.MeshStandardMaterial({ color: color, metalness: 0.32, roughness: 0.42, side: s, transparent: true, opacity: 0.86 });
    }
    api.group.add(new T.Mesh(body.geo, side(0x3987e5, T.FrontSide)));
    api.group.add(new T.Mesh(body.geo, side(0xd95926, T.BackSide)));
    api.group.add(new T.Mesh(body.geo, new T.MeshBasicMaterial({
      color: 0xe2e8f0, wireframe: true, transparent: true, opacity: 0.07, side: T.DoubleSide
    })));
    api.group.add(new T.Mesh(rimA.geo, new T.MeshStandardMaterial({ color: 0xffd166, roughness: 0.5, side: T.DoubleSide })));
    api.group.add(new T.Mesh(rimB.geo, new T.MeshStandardMaterial({ color: 0x7ee0b5, roughness: 0.5, side: T.DoubleSide })));
    function setPlaying(on) { playing = on; playBtn.textContent = on ? 'Pause' : 'Play'; playBtn.classList.toggle('on', on); }
    playBtn.addEventListener('click', function () {
      if (!playing && Math.abs(parseFloat(slider.value)) >= 150) dir = parseFloat(slider.value) > 0 ? -1 : 1;
      setPlaying(!playing);
    });
    slider.addEventListener('input', function () { setPlaying(false); fill(); });
    fill();
    return function () {
      if (!playing) return;
      var v = parseFloat(slider.value) + dir * 0.9;
      if (v >= 150 || v <= -150) { v = Math.max(-150, Math.min(150, v)); setPlaying(false); }
      slider.value = v;
      fill();
    };
  }
});
</script>

To finish the sphere one maps $h=\omega\cos\theta/\sin^n\theta$ (the paper writes $\omega\sin\theta/\cos^n\theta$, measuring $\theta$ from the equator) and applies the damped inversion of their equations (7)--(8). An inversion is a map like $\mathbf{x}\mapsto\mathbf{x}/\lVert\mathbf{x}\rVert^2$ that swaps near and far, so it brings the two infinitely distant ends of the cylinder ($h\to\pm\infty$, the poles) in to single points and closes the band into a sphere. The damping factors slow it down far out, so that the closed-up points stay smooth. That is a page of algebra and a second rendering pass. The point of this canvas is narrower: a halfway model you can audit against a paper.

---

# A volume that must cross zero
{: #a-volume-that-must-cross-zero}
<div class="cs-q">
It is worth asking how one knows an eversion is halfway done.
</div>

<div class="cs-a">
Track the signed volume enclosed. For any smooth $f:S^2\to\mathbb{R}^3$,
$$V(f)=\frac13\int_{S^2}f\cdot\bigl(f_\theta\times f_\varphi\bigr)\,d\theta\,d\varphi.$$
For an embedding with the outward frame this is the enclosed volume (divergence theorem, $\nabla\cdot\mathbf{x}=3$). For an immersion it counts volume with multiplicity and sign. $V(\iota)=4\pi/3$. For $\alpha(p)=-p$ one has $\alpha&#95;{\theta}\times\alpha&#95;{\varphi}=(-\mathbf{r}&#95;{\theta})\times(-\mathbf{r}&#95;{\varphi})=\mathbf{r}&#95;{\theta}\times\mathbf{r}&#95;{\varphi}$ while $\alpha=-\mathbf{r}$, so $V(\alpha)=-4\pi/3$. Along any regular homotopy $V$ is a continuous function of one real variable, so the intermediate-value theorem produces an $s^{\ast}$ with $V(f&#95;{s^{\ast}})=0$. That is halfway, in the crudest sense. Morin's halfway model is the geometric refinement: a quarter turn carries it to itself with its two sides swapped, which forces $V=0$ by symmetry.
</div>

For the illegal homotopy $F&#95;{s}$ the integrand is one line: $F&#95;{s}\cdot(\mathbf{F}&#95;{\theta}\times\mathbf{F}&#95;{\varphi})=(1-2s)\sin\theta$, so

$$V(F_s)=(1-2s)\,\frac{4\pi}{3}.$$

It crosses zero at $s=\tfrac12$, which is exactly where $F&#95;{s}$ creases: the cheap way to reach zero volume is to flatten. A genuine eversion must also pass through $V=0$, but with a surface that is still immersed, its self-intersections arranged so that positive and negative volume cancel.

**Normals cannot measure it.** Consider the alignment of normals, $S(s)=\int&#95;{S^2}\mathbf{n}&#95;{0}\cdot\mathbf{n}&#95;{s}\,dA$. Along an eversion it does not run from $4\pi$ to $-4\pi$. The normal is computed from the pushed frame, and $d\alpha=-I$ flips both frame vectors, so $\mathbf{n}&#95;{\alpha}(p)=\mathbf{n}&#95;{\iota}(p)=p$ and $S=+4\pi$ at the end. What changes under eversion is not the normal but its relation to the position: at $\alpha(p)=-p$ the normal $p$ points *inward*. Signed volume sees that; normal alignment does not. Both are plotted below for $F&#95;{s}$, with $\alpha$'s values marked.

<div class="mviz" id="ev-sync" tabindex="0" aria-label="Signed volume and normal alignment along the crease homotopy">
  <div class="mv-title" id="ev-sync-title"></div>
  <svg id="ev-sync-svg" viewBox="0 0 640 290" role="img" aria-label="Two curves against s from 0 to 1">
    <g id="ev-sync-axes"></g>
    <path id="ev-sync-S" fill="none" stroke="#c98500" stroke-width="2.5"/>
    <path id="ev-sync-V" fill="none" stroke="#3987e5" stroke-width="2.5"/>
    <g id="ev-sync-alpha"></g>
    <line id="ev-sync-cur" stroke="#c3c2b7" stroke-width="1"/>
    <circle id="ev-sync-dS" r="5.5" fill="#c98500" stroke="#121212" stroke-width="2"/>
    <circle id="ev-sync-dV" r="5.5" fill="#3987e5" stroke="#121212" stroke-width="2"/>
  </svg>
  <div class="mv-detail" id="ev-sync-detail"></div>
  <div class="mv-controls">
    <label>s <input type="range" id="ev-sync-s" min="0" max="100" value="0"> <span id="ev-sync-sv">0.00</span></label>
    <span class="mv-key"><b style="background:#3987e5"></b>signed volume V(s) / (4π/3)<b style="background:#c98500"></b>normal alignment S(s) / 4π</span>
  </div>
</div>
<p class="cs-cap">Both curves are computed live by a trapezoid rule on the integrands in the text, for the crease homotopy $F&#95;{s}$. The hollow markers at $s=1$ are the values for the true everted sphere $\alpha(p)=-p$: signed volume $-1$, but normal alignment $+1$. The orange band is $s=\tfrac12$, where $F&#95;{s}$ is not an immersion.</p>
<script>
(function () {
  var root = document.getElementById('ev-sync');
  if (!root || !window.EV) return;
  var E = EV.el, X0 = 64, X1 = 610, Y0 = 26, Y1 = 250;
  var X = function (s) { return X0 + s * (X1 - X0); }, Y = function (v) { return Y0 + (1.15 - v) / 2.3 * (Y1 - Y0); };
  // n_0 . n_s for F_s, and F_s . (F_theta x F_phi), both per unit dtheta dphi after the phi integral
  function align(s, th) {
    var st = Math.sin(th), ct = Math.cos(th), den = Math.sqrt((1 - 2 * s) * (1 - 2 * s) * st * st + ct * ct);
    return den < 1e-10 ? 0 : ((1 - 2 * s) * st * st + ct * ct) / den * st;
  }
  function vol(s, th) { return (1 - 2 * s) * Math.sin(th); }
  function integ(g, s) {
    var N = 240, acc = 0;
    for (var i = 0; i <= N; i++) acc += (i === 0 || i === N ? 0.5 : 1) * g(s, Math.PI * i / N);
    return 2 * Math.PI * acc * Math.PI / N;
  }
  var Sv = [], Vv = [];
  for (var k = 0; k <= 200; k++) { Sv.push(integ(align, k / 200) / (4 * Math.PI)); Vv.push(integ(vol, k / 200) / 3 / (4 * Math.PI / 3)); }
  var ax = document.getElementById('ev-sync-axes');
  E('rect', { x: X(0.494), y: Y0, width: X(0.506) - X(0.494), height: Y1 - Y0, fill: '#d95926', opacity: 0.35 }, ax);
  E('text', { x: X(0.5), y: Y1 + 34, 'text-anchor': 'middle', 'font-size': 12, style: 'fill:#f08a5d' }, ax).textContent = 'crease at s = ½';
  [1, 0.5, 0, -0.5, -1].forEach(function (v) {
    E('line', { x1: X0, x2: X1, y1: Y(v), y2: Y(v), stroke: v === 0 ? '#555' : '#2a2a2a' }, ax);
    E('text', { x: X0 - 8, y: Y(v) + 4, 'text-anchor': 'end', 'font-size': 12, style: 'fill:#c3c2b7' }, ax).textContent = (v < 0 ? '−' : v > 0 ? '+' : '') + Math.abs(v);
  });
  [0, 0.25, 0.5, 0.75, 1].forEach(function (s) {
    E('text', { x: X(s), y: Y1 + 18, 'text-anchor': 'middle', 'font-size': 12, style: 'fill:#c3c2b7' }, ax).textContent = 's = ' + s;
  });
  var al = document.getElementById('ev-sync-alpha');
  E('circle', { cx: X(1), cy: Y(-1), r: 9, fill: 'none', stroke: '#6fa8f0', 'stroke-width': 2 }, al);
  E('circle', { cx: X(1), cy: Y(1), r: 9, fill: 'none', stroke: '#e0a526', 'stroke-width': 2 }, al);
  E('text', { x: X(1) - 14, y: Y(1) + 4, 'text-anchor': 'end', 'font-size': 12, style: 'fill:#e0e0e0' }, al).textContent = 'α: S = +1';
  E('text', { x: X(1) - 14, y: Y(-1) + 18, 'text-anchor': 'end', 'font-size': 12, style: 'fill:#e0e0e0' }, al).textContent = 'α: V = −1';
  var pS = [], pV = [];
  for (k = 0; k <= 200; k++) { pS.push([X(k / 200), Y(Sv[k])]); pV.push([X(k / 200), Y(Vv[k])]); }
  document.getElementById('ev-sync-S').setAttribute('d', EV.path(pS));
  document.getElementById('ev-sync-V').setAttribute('d', EV.path(pV));
  var sl = document.getElementById('ev-sync-s');
  function f2(v) { return (v < -0.005 ? '−' : '+') + Math.abs(v).toFixed(2); }
  function on() {
    var s = sl.value / 100, k2 = Math.round(s * 200);
    document.getElementById('ev-sync-sv').textContent = s.toFixed(2);
    var c = document.getElementById('ev-sync-cur'); c.setAttribute('x1', X(s)); c.setAttribute('x2', X(s)); c.setAttribute('y1', Y0); c.setAttribute('y2', Y1);
    var a = document.getElementById('ev-sync-dS'), b = document.getElementById('ev-sync-dV');
    a.setAttribute('cx', X(s)); a.setAttribute('cy', Y(Sv[k2])); b.setAttribute('cx', X(s)); b.setAttribute('cy', Y(Vv[k2]));
    document.getElementById('ev-sync-detail').textContent = 'V / (4π/3) = ' + f2(Vv[k2]) + '   ·   S / 4π = ' + f2(Sv[k2]) + (k2 === 100 ? '   ·   F is not an immersion here' : '');
    document.getElementById('ev-sync-title').textContent = k2 === 100 ? 's = ½: the sphere is flattened to a doubly covered disk. Signed volume 0, and the surface has creased.'
      : s < 0.5 ? 'Squashing the sphere. The signed volume falls linearly; the normals tilt toward the vertical.'
      : 'Past the crease: the sphere is reflected. Signed volume negative. Normal alignment ends at −⅓, which is not what α gives.';
  }
  sl.addEventListener('input', on);
  on();
})();
</script>


---

# The arc
{: #the-arc}
Topology gives the grammar: open sets, continuity, connectedness, homotopy ([Vols. I–II](/blog/2026/08/17/circling-the-sphere)). Calculus gives the language: charts, $J&#95;{f}$, $\mathbf{f}&#95;{u}\times\mathbf{f}&#95;{v}\neq\mathbf{0}$. Function spaces give the question: is $\operatorname{Imm}(S^2,\mathbb{R}^3)$ path-connected? For circles in the plane the answer is no, by $\pi&#95;{1}(S^1)=\mathbb{Z}$. One dimension up, the same instinct produces $\pi&#95;{2}(V&#95;{3,2})$, and that group is zero. Smale's theorem is that computation plus a fibration argument. Morin, Thurston, and the Bednorzes are what you need if you want to *see* a path.

These six volumes circle the sphere, starting from the definition of an open set, until the picture and the equation are the same object.

**Further reading.** S. Smale, *A classification of immersions of the two-sphere*, Trans. Amer. Math. Soc. 90 (1959). A. Bednorz and W. Bednorz, [arXiv:1711.10466](https://arxiv.org/abs/1711.10466). S. Levy, D. Maxwell, T. Munzner, *Outside In*, Geometry Center, 1994. Guillemin–Pollack, *Differential Topology*. J. Munkres, *Topology*. A. Hatcher, *Algebraic Topology* (free online). M. Hirsch, *Immersions of manifolds*, Trans. Amer. Math. Soc. 93 (1959). H. Whitney, *On regular closed curves in the plane*, Compositio Math. 4 (1937).
