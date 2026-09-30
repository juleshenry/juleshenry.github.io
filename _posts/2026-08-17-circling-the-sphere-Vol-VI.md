---
layout: post
title: "Back-of-the-Envelope: Sphere Eversion, Vol. VI: Seeing the Eversion"
date: 2026-08-17 12:05:00
categories: differential topology
mathjax: true
---

*Sphere Eversion:* [Vol. I](/blog/2026/08/17/circling-the-sphere) · [Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II) · [Vol. III](/blog/2026/08/17/circling-the-sphere-Vol-III) · [Vol. IV](/blog/2026/08/17/circling-the-sphere-Vol-IV) · [Vol. V](/blog/2026/08/17/circling-the-sphere-Vol-V) · **Vol. VI**

{% include eversion-kit.html %}

*The existence proof is done. This volume is about seeing it: slack, a formula you can type, and an honest way to say "halfway".*

[Vol. V](/blog/2026/08/17/circling-the-sphere-Vol-V) proved that $\iota(p)=p$ and $\alpha(p)=-p$ lie in the same path-component of $\operatorname{Imm}(S^2,\mathbb{R}^3)$. It did not produce a path. Nobody could picture one at first. The first explicit eversions came from Arnold Shapiro (published by Tony Phillips, 1966) and Bernard Morin (late 1960s), who was blind. Here are three windows onto what they saw.

<p style="text-align:center;">
  <img src="/blog/assets/2024/eversion/eversion.gif" alt="Sphere eversion through the Morin halfway model" style="max-width:100%;">
</p>

<div class="cs-toc">
<strong>Contents</strong>
<ol>
  <li><a href="#slack-that-does-not-crease">slack that does not crease</a></li>
  <li><a href="#a-formula-that-actually-everts-a-band">a formula that actually everts a band</a></li>
  <li><a href="#a-volume-that-must-cross-zero">a volume that must cross zero</a></li>
  <li><a href="#what-the-model-got-wrong">what the model got wrong</a></li>
  <li><a href="#the-arc">the arc</a></li>
</ol>
</div>

---

# slack that does not crease
{: #slack-that-does-not-crease}
<div class="cs-q">
<strong>Student.</strong> Explain Thurston's magic formula, the one that proves eversion.
</div>

<div class="cs-a">
<strong>Teacher.</strong> There is no such formula, and Thurston did not prove existence — Smale did. What Thurston gave, in the 1970s (animated in the 1994 film <em>Outside In</em>), is a <em>construction</em>: corrugate the surface so that it has slack, pass the ripples through one another, then iron the ripples out. The model invented a condition on $\det J(g&#95;{t})>0$. The actual local move is a normal oscillation.
</div>

$$
\mathbf{f}_\varepsilon(\theta,\varphi)=\bigl(1+\varepsilon\sin\theta\sin(k\varphi)\bigr)\,\mathbf{r}(\theta,\varphi).
$$

The amplitude $\varepsilon\sin\theta$ dies at the poles, so the chart singularities of $\mathbf{r}$ stay chart singularities. For $\lvert\varepsilon\rvert<1$ the radial factor never vanishes, and a computation of $\mathbf{f}&#95;{\theta}\times\mathbf{f}&#95;{\varphi}$ shows that its component along $\mathbf{r}$ is $\rho^2\sin\theta$ with $\rho=1+\varepsilon\sin\theta\sin(k\varphi)>0$, while the ripple only adds tangential terms — so it is never zero away from the chart poles. This is an immersion for every $\varepsilon$ in that range (an embedding, even: each ray from the origin meets it once). It is **not** an eversion. It is the ingredient that makes an eversion possible: extra wiggles so that later, when you try to pass sheets through each other, you have room.

The September 2024 draft (see [Vol. I](/blog/2026/08/17/circling-the-sphere)) implemented "corrugation" and then multiplied $z$ by a factor passing through zero. That second step is $F&#95;{s}$ again. Here there is no second step. The two colours are the two sides of the surface. Drag both sliders as far as they go: the colours never trade places, and $\min\rho$ stays positive.

<div id="cs-corr" class="cs-stage" style="height:460px;">
  <div class="cs-hud cs-hud-tl" id="cs-corr-hud">corrugation</div>
  <div class="cs-hud cs-hud-tr"><span style="color:#6fa8f0;">outside</span> <span style="color:#f08a5d;">inside</span></div>
  <div class="cs-ctrl">
    <label>ε <input type="range" id="cs-eps" min="0" max="70" value="0"> <span id="cs-eps-v">0.00</span></label>
    <label>k <input type="range" id="cs-k" min="2" max="10" value="4"> <span id="cs-k-v">4</span></label>
  </div>
</div>
<p class="cs-cap">$\mathbf{f}&#95;{\varepsilon}=(1+\varepsilon\sin\theta\sin(k\varphi))\,\hat{\mathbf{r}}$. Blue is the outside, orange the inside. Increase $\varepsilon$: petals, no fold. This is slack, not eversion.</p>

<script>
CS.mount({
  id: 'cs-corr',
  height: 460,
  cam: [0, 0.2, 4.0],
  setup: function (api) {
    var T = api.THREE;
    var geo = new T.SphereGeometry(1, 72, 48);
    var pos = geo.getAttribute('position');
    var orig = new Float32Array(pos.array);
    var front = new T.MeshStandardMaterial({
      color: 0x3987e5, metalness: 0.28, roughness: 0.48,
      side: T.FrontSide, transparent: true, opacity: 0.88
    });
    var back = new T.MeshStandardMaterial({
      color: 0xd95926, metalness: 0.28, roughness: 0.48,
      side: T.BackSide, transparent: true, opacity: 0.88
    });
    api.group.add(new T.Mesh(geo, front));
    api.group.add(new T.Mesh(geo, back));
    api.group.add(new T.Mesh(geo, new T.MeshBasicMaterial({
      color: 0x9ec3f0, wireframe: true, transparent: true, opacity: 0.1, side: T.DoubleSide
    })));
    var hud = document.getElementById('cs-corr-hud');
    function apply() {
      var eps = parseFloat(document.getElementById('cs-eps').value) / 100;
      var k = parseInt(document.getElementById('cs-k').value, 10);
      document.getElementById('cs-eps-v').textContent = eps.toFixed(2);
      document.getElementById('cs-k-v').textContent = String(k);
      var arr = pos.array;
      var minR = 1e9;
      for (var i = 0; i < pos.count; i++) {
        var x = orig[3 * i], y = orig[3 * i + 1], z = orig[3 * i + 2];
        var th = Math.acos(Math.max(-1, Math.min(1, z)));
        var ph = Math.atan2(y, x);
        var rho = 1 + eps * Math.sin(th) * Math.sin(k * ph);
        if (rho < minR) minR = rho;
        arr[3 * i] = rho * x;
        arr[3 * i + 1] = rho * y;
        arr[3 * i + 2] = rho * z;
      }
      pos.needsUpdate = true;
      geo.computeVertexNormals();
      if (hud) {
        hud.innerHTML = 'ρ = 1 + ε sin θ sin kφ<br>min ρ = ' + minR.toFixed(3) +
          (minR > 0.02 ? '  (immersion)' : '  (collapsed)');
      }
    }
    document.getElementById('cs-eps').addEventListener('input', apply);
    document.getElementById('cs-k').addEventListener('input', apply);
    apply();
    return null;
  }
});
</script>

---

# a formula that actually everts a band
{: #a-formula-that-actually-everts-a-band}
Existence is not a picture. Morin gave the first explicit halfway model — a four-lobed immersion with a single quadruple point — and later Apéry wrote algebraic formulae. A family you can type into a shader is due to Adam and Witold Bednorz, *Analytic sphere eversion using ruled surfaces*, arXiv:1711.10466. They evert a cylinder (the sphere minus two polar caps) by a ruled surface, then close the caps by a damped inversion. We draw only the cylinder, so that every vertex is the displayed equation.

$$
\begin{aligned}
x&= t\cos\varphi + p\sin\bigl((n-1)\varphi\bigr) - h\sin\varphi,\\
y&= t\sin\varphi + p\cos\bigl((n-1)\varphi\bigr) + h\cos\varphi,\\
z&= h\sin(n\varphi) - \frac{t}{n}\cos(n\varphi) - q\,t\,h.
\end{aligned}
$$

Parameters: $n=2$ (Morin band) or $n=3$ (Boy band), $q=\tfrac23$, and $p=1-\lvert qt\rvert$, which is exactly the choice that keeps their smoothness inequality

$$(n-1)p\bigl(1-q\lvert t\rvert\bigr)+qt^2>0.$$

The coordinates are $(\varphi,h)\in S^1\times\mathbb{R}$. At $t=0$, $n=2$ this is the ruled halfway model: four sheets through the origin (the quadruple point $Q$), and no preferred side. Sliding $t$ from $-3/2$ to $3/2$ swaps the two rims of the cylinder. That swap, once the poles are sewn back on, is the eversion of the band.

<div id="cs-bednorz" class="cs-stage" style="height:500px;">
  <div class="cs-hud cs-hud-tl" id="cs-bed-hud">Bednorz ruled band</div>
  <div class="cs-hud cs-hud-tr"><span style="color:#6fa8f0;">front</span> <span style="color:#f08a5d;">back</span></div>
  <div class="cs-ctrl">
    <label>t <input type="range" id="cs-bt" min="-150" max="150" value="0"> <span id="cs-bt-v">0.00</span></label>
    <label>n
      <select id="cs-bn">
        <option value="2" selected>2 (Morin)</option>
        <option value="3">3 (Boy)</option>
      </select>
    </label>
  </div>
</div>
<p class="cs-cap">Equation (4) of Bednorz–Bednorz, $q=2/3$, $p=1-\lvert qt\rvert$, $h\in[-2.3,2.3]$. The poles are not closed; what you see is the formula, not a screenshot of <em>Outside In</em>. At $t=0$, $n=2$ you are looking at the ruled Morin halfway. At $n=3$, $t=0$ you are looking at a ruled Boy surface, an immersion of $\mathbb{RP}^2$.</p>

<script>
CS.mount({
  id: 'cs-bednorz',
  height: 500,
  cam: [0, 0.6, 6.2],
  rotX: 0.45,
  setup: function (api) {
    var T = api.THREE;
    var nH = 70, nP = 110;
    var geo = new T.PlaneGeometry(1, 1, nP, nH);
    var pos = geo.getAttribute('position');
    function bednorz(h, phi, t, n) {
      var q = 2 / 3;
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
    function fill() {
      var t = parseFloat(document.getElementById('cs-bt').value) / 100;
      var n = parseInt(document.getElementById('cs-bn').value, 10);
      document.getElementById('cs-bt-v').textContent = t.toFixed(2);
      var arr = pos.array;
      var i, maxR = 0;
      for (i = 0; i < pos.count; i++) {
        var col = i % (nP + 1);
        var row = (i / (nP + 1)) | 0;
        var phi = (col / nP) * Math.PI * 2 - Math.PI;
        var h = -2.3 + 4.6 * (row / nH);
        var xyz = bednorz(h, phi, t, n);
        arr[3 * i] = xyz[0];
        arr[3 * i + 1] = xyz[1];
        arr[3 * i + 2] = xyz[2];
        var r = Math.hypot(xyz[0], xyz[1], xyz[2]);
        if (r > maxR) maxR = r;
      }
      var sc = maxR > 1e-6 ? 2.15 / maxR : 1;
      for (i = 0; i < arr.length; i++) arr[i] *= sc;
      pos.needsUpdate = true;
      geo.computeVertexNormals();
      var hud = document.getElementById('cs-bed-hud');
      var q = 2 / 3;
      var p = 1 - Math.abs(q * t);
      if (hud) {
        hud.innerHTML = 'n = ' + n + ', t = ' + t.toFixed(2) + ', p = ' + p.toFixed(2) + ', q = 2/3' +
          (Math.abs(t) < 0.03 ? '<br>halfway' : '');
      }
    }
    api.group.add(new T.Mesh(geo, new T.MeshStandardMaterial({
      color: 0x3987e5, metalness: 0.32, roughness: 0.42,
      side: T.FrontSide, transparent: true, opacity: 0.86
    })));
    api.group.add(new T.Mesh(geo, new T.MeshStandardMaterial({
      color: 0xd95926, metalness: 0.32, roughness: 0.42,
      side: T.BackSide, transparent: true, opacity: 0.86
    })));
    api.group.add(new T.Mesh(geo, new T.MeshBasicMaterial({
      color: 0xe2e8f0, wireframe: true, transparent: true, opacity: 0.07, side: T.DoubleSide
    })));
    document.getElementById('cs-bt').addEventListener('input', fill);
    document.getElementById('cs-bn').addEventListener('change', fill);
    fill();
    return null;
  }
});
</script>

To finish the sphere one maps $h=\omega\sin\theta/\cos^n\theta$ and applies Bednorz's damped inversion (their (7)--(8)). That is a page of algebra and a second rendering pass. The point of this canvas is narrower: a halfway model you can audit against a paper.

---

# a volume that must cross zero
{: #a-volume-that-must-cross-zero}
<div class="cs-q">
<strong>Student.</strong> How do I know I am halfway?
</div>

<div class="cs-a">
<strong>Teacher.</strong> Track the signed volume enclosed. For any smooth $f:S^2\to\mathbb{R}^3$,
$$V(f)=\frac13\int_{S^2}f\cdot\bigl(f_\theta\times f_\varphi\bigr)\,d\theta\,d\varphi.$$
For an embedding with the outward frame this is the enclosed volume (divergence theorem, $\nabla\cdot\mathbf{x}=3$). For an immersion it counts volume with multiplicity and sign. $V(\iota)=4\pi/3$. For $\alpha(p)=-p$ one has $\alpha&#95;{\theta}\times\alpha&#95;{\varphi}=(-\mathbf{r}&#95;{\theta})\times(-\mathbf{r}&#95;{\varphi})=\mathbf{r}&#95;{\theta}\times\mathbf{r}&#95;{\varphi}$ while $\alpha=-\mathbf{r}$, so $V(\alpha)=-4\pi/3$. Along any regular homotopy $V$ is a continuous function of one real variable, so the intermediate-value theorem produces an $s^*$ with $V(f&#95;{s^*})=0$. That is halfway, in the crudest sense. Morin's halfway model is the geometric refinement: a quarter turn carries it to itself with its two sides swapped, which forces $V=0$ by symmetry.
</div>

For the illegal homotopy $F&#95;{s}$ the integrand is one line: $F&#95;{s}\cdot(\mathbf{F}&#95;{\theta}\times\mathbf{F}&#95;{\varphi})=(1-2s)\sin\theta$, so

$$V(F_s)=(1-2s)\,\frac{4\pi}{3}.$$

It crosses zero at $s=\tfrac12$, which is exactly where $F&#95;{s}$ creases: the cheap way to reach zero volume is to flatten. A genuine eversion must also pass through $V=0$, but with a surface that is still immersed, its self-intersections arranged so that positive and negative volume cancel.

**A correction.** An earlier version of this page measured "halfway" by the alignment of normals, $S(s)=\int&#95;{S^2}\mathbf{n}&#95;{0}\cdot\mathbf{n}&#95;{s}\,dA$, and claimed $S$ runs from $4\pi$ to $-4\pi$ along an eversion. It does not. The normal is computed from the pushed frame, and $d\alpha=-I$ flips both frame vectors, so $\mathbf{n}&#95;{\alpha}(p)=\mathbf{n}&#95;{\iota}(p)=p$ and $S=+4\pi$ at the end. What changes under eversion is not the normal but its relation to the position: at $\alpha(p)=-p$ the normal $p$ points *inward*. Signed volume sees that; normal alignment does not. Both are plotted below for $F&#95;{s}$, with $\alpha$'s values marked.

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
      : s < 0.5 ? 'Squashing the sphere. The signed volume falls linearly; the normals tilt toward the equator.'
      : 'Past the crease: the sphere is reflected. Signed volume negative. Normal alignment ends at −⅓, which is not what α gives.';
  }
  sl.addEventListener('input', on);
  on();
})();
</script>


---

# what the model got wrong
{: #what-the-model-got-wrong}
The May transcript is still worth reading. It is a record of the questions one actually asks. Here is the answer key.

<table class="cs-err">
  <thead>
    <tr><th>Claim in the Phi-3 notes</th><th>Fact</th></tr>
  </thead>
  <tbody>
    <tr><td>$H=(1-t)f&#95;{0}+tf&#95;{1}$ is a regular homotopy.</td><td>It is a homotopy of maps. Rank drops. See $F&#95;{s}$.</td></tr>
    <tr><td>$\partial&#95;{\theta}(1,0,0)=\mathbf{0}$.</td><td>Differentiate the chart, not the point. $\mathbf{r}&#95;{\theta}(1,0,0)=(0,0,-1)$.</td></tr>
    <tr><td>Jacobian of $f:\mathbb{R}^n\to\mathbb{R}^m$ is $n\times m$.</td><td>$m\times n$. For immersions $S^2\to\mathbb{R}^3$ it is $3\times 2$; there is no determinant.</td></tr>
    <tr><td>$\det J=-1$ means a saddle.</td><td>It means orientation reversal. A saddle is a critical point, which requires $\det J=0$ (in the square case).</td></tr>
    <tr><td>$S^2\times[0,1]$ is a ball.</td><td>It is a spherical shell. The ball is $D^3$.</td></tr>
    <tr><td>Smale's hairy ball theorem.</td><td>Poincaré–Brouwer. Smale classified immersions of $S^2$.</td></tr>
    <tr><td>Thurston's magic formula ($J(g&#95;{t})>0$) proves eversion.</td><td>Smale proved existence. Thurston gave corrugations. Bednorz wrote a ruled family.</td></tr>
    <tr><td>Eversion forbids self-intersection and uses contact / Reeb foliations.</td><td>Self-intersection is the point. Contact geometry is a different chapter.</td></tr>
    <tr><td>The complex exponential at $(0,\pi/2)$ has $\det J=-1$.</td><td>$\det J=e^{2x}=1$ there. The map is a local diffeomorphism everywhere.</td></tr>
  </tbody>
</table>

---

# the arc
{: #the-arc}
Topology gives the grammar: open sets, continuity, connectedness, homotopy ([Vols. I–II](/blog/2026/08/17/circling-the-sphere)). Calculus gives the language: charts, $J&#95;{f}$, $\mathbf{f}&#95;{u}\times\mathbf{f}&#95;{v}\neq\mathbf{0}$. Function spaces give the question: is $\operatorname{Imm}(S^2,\mathbb{R}^3)$ path-connected? Circles in the plane say no, by $\pi&#95;{1}(S^1)=\mathbb{Z}$. One dimension up, the same instinct produces $\pi&#95;{2}(V&#95;{3,2})$, and that group is zero. Smale's theorem is that computation plus a fibration argument. Morin, Thurston, and Bednorz are what you do if you want to *see* a path.

The May 2024 transcript asked. The September 2024 draft answered, and then drew the forbidden crease. These six volumes circle the sphere, starting from the definition of an open set, until the picture and the equation are the same object.

**Further reading.** S. Smale, *A classification of immersions of the two-sphere*, Trans. Amer. Math. Soc. 90 (1958). A. Bednorz and W. Bednorz, [arXiv:1711.10466](https://arxiv.org/abs/1711.10466). S. Levy, D. Maxwell, T. Munzner, *Outside In*, Geometry Center, 1994. Guillemin–Pollack, *Differential Topology*. J. Munkres, *Topology*. A. Hatcher, *Algebraic Topology* (free online). M. Hirsch, *Immersions of manifolds*, Trans. AMS 93 (1959). H. Whitney, *On regular closed curves in the plane*, Compositio Math. 4 (1937). The raw parent transcript: [Phi-3 notes](https://honghaptang.github.io/blog/2024/05/22/sphere-eversion-phi3-notes-I).

---

*Sphere Eversion:* [Vol. I](/blog/2026/08/17/circling-the-sphere) · [Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II) · [Vol. III](/blog/2026/08/17/circling-the-sphere-Vol-III) · [Vol. IV](/blog/2026/08/17/circling-the-sphere-Vol-IV) · [Vol. V](/blog/2026/08/17/circling-the-sphere-Vol-V) · **Vol. VI**
