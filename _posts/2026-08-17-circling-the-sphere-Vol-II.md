---
layout: post
title: "Back-of-the-Envelope: Sphere Eversion, Vol. II: Paths and Homotopy"
date: 2026-08-17 12:01:00
categories: differential topology
mathjax: true
---

*Sphere Eversion:* [I](/blog/2026/08/17/circling-the-sphere) · **II** · [III](/blog/2026/08/17/circling-the-sphere-Vol-III) · [IV](/blog/2026/08/17/circling-the-sphere-Vol-IV) · [V](/blog/2026/08/17/circling-the-sphere-Vol-V) · [VI](/blog/2026/08/17/circling-the-sphere-Vol-VI)

{% include eversion-kit.html %}

*Homotopy is continuous deformation. This volume builds it from the path of [Vol. I](/blog/2026/08/17/circling-the-sphere), and computes the two facts about spheres that Smale's proof will need.*

[Vol. I](/blog/2026/08/17/circling-the-sphere) ended with a restatement: an eversion is a *path* in the space $\operatorname{Imm}(S^2,\mathbb{R}^3)$. A path in a space of maps is a continuously varying family of maps. That has a name.

<div class="cs-toc">
<strong>Contents</strong>
<ol>
  <li><a href="#homotopy">homotopy</a></li>
  <li><a href="#loops-and-the-fundamental-group">loops and the fundamental group</a></li>
  <li><a href="#the-circle">the circle: π₁(S¹) = ℤ</a></li>
  <li><a href="#the-sphere">the sphere: π₁(S²) = 0</a></li>
  <li><a href="#higher-homotopy-groups">higher homotopy groups</a></li>
  <li><a href="#where-this-goes">where this goes</a></li>
</ol>
</div>

---

# homotopy
{: #homotopy}
<div class="cs-q">
<strong>Student.</strong> What is a homotopy?
</div>

<div class="cs-a">
<strong>Teacher.</strong> A movie of maps. Two maps $f,g:X\to Y$ are <em>homotopic</em> if one can be deformed continuously into the other: there is a continuous $H:X\times[0,1]\to Y$ with $H(\cdot,0)=f$ and $H(\cdot,1)=g$. Freeze the second coordinate at $s$ and you get the frame $H&#95;{s}=H(\cdot,s)$ of the movie. We write $f\simeq g$.
</div>

The notation $X\times[0,1]$ matters. For $X=S^2$ it is a thickened sphere, a spherical *shell*: each point of the sphere grows a little time-interval. It is not the solid ball. (The Phi-3 transcript got this wrong, and it is worth getting right: the homotopy parameter is a new direction, not a filling-in.)

In $\mathbb{R}^n$ every two maps are homotopic, by the **straight-line homotopy**

$$H(x,s)=(1-s)\,f(x)+s\,g(x).$$

The same formula works in any *convex* set, because the segment between $f(x)$ and $g(x)$ stays inside. Homotopy only becomes interesting when the target has a hole for the segment to fall into. Below, $\gamma&#95;{0}$ and $\gamma&#95;{1}$ are two paths from $A$ to $B$ and the orange curve is the frame $H&#95;{s}$.

<div class="mviz" id="ev-htpy" tabindex="0" aria-label="Straight-line homotopy between two paths, with and without a puncture">
  <div class="mv-title" id="ev-htpy-title"></div>
  <svg id="ev-htpy-svg" viewBox="0 0 640 330" role="img" aria-label="Two paths from A to B and the straight-line homotopy between them">
    <g id="ev-htpy-fam"></g>
    <path id="ev-htpy-g0" fill="none" stroke="#3987e5" stroke-width="2.5"/>
    <path id="ev-htpy-g1" fill="none" stroke="#199e70" stroke-width="2.5"/>
    <path id="ev-htpy-hs" fill="none" stroke="#d95926" stroke-width="3.5"/>
    <g id="ev-htpy-hole"></g>
    <circle id="ev-htpy-handle" r="9" fill="#199e70" stroke="#f0f0f0" stroke-width="2" class="drag"/>
    <g id="ev-htpy-labels"></g>
  </svg>
  <div class="mv-detail" id="ev-htpy-detail"></div>
  <div class="mv-controls">
    <label>s <input type="range" id="ev-htpy-s" min="0" max="1000" value="300"> <span id="ev-htpy-sv"></span></label>
    <button type="button" id="ev-htpy-punct">puncture: on</button>
    <span class="mv-key"><b style="background:#3987e5"></b>γ₀<b style="background:#199e70"></b>γ₁ (drag its handle)<b style="background:#d95926"></b>Hₛ</span>
  </div>
</div>
<p class="cs-cap">$H(t,s)=(1-s)\,\gamma&#95;{0}(t)+s\,\gamma&#95;{1}(t)$, with both endpoints held fixed. In the plane this always works. With the origin removed it works exactly when the loop "$\gamma&#95;{0}$ then $\gamma&#95;{1}$ backwards" has winding number $0$ around the hole. Drag the green handle across the hole and watch both facts change together.</p>
<script>
(function () {
  var root = document.getElementById('ev-htpy');
  if (!root || !window.EV) return;
  var svg = document.getElementById('ev-htpy-svg'), E = EV.el;
  var CX = 320, CY = 165, SC = 110, m = -0.9, punct = true;
  var X = function (p) { return CX + SC * p[0]; }, Y = function (p) { return CY - SC * p[1]; };
  var g0 = function (t) { return [-1.4 * Math.cos(Math.PI * t), Math.sin(Math.PI * t) - 0.2 * Math.sin(3 * Math.PI * t)]; };
  var g1 = function (t) { return [-1.4 * Math.cos(Math.PI * t), m * Math.sin(Math.PI * t)]; };
  var H = function (t, s) { var a = g0(t), b = g1(t); return [(1 - s) * a[0] + s * b[0], (1 - s) * a[1] + s * b[1]]; };
  var N = 240, sl = document.getElementById('ev-htpy-s');
  function curve(fn) { var p = []; for (var j = 0; j <= N; j++) { var q = fn(j / N); p.push([X(q), Y(q)]); } return EV.path(p); }
  var lab = document.getElementById('ev-htpy-labels');
  [[-1.4, 'A'], [1.4, 'B']].forEach(function (a) {
    E('circle', { cx: X([a[0], 0]), cy: Y([0, 0]), r: 5, fill: '#f0f0f0' }, lab);
    E('text', { x: X([a[0], 0]) + (a[0] < 0 ? -12 : 12), y: CY + 5, 'text-anchor': a[0] < 0 ? 'end' : 'start', 'font-size': 15 }, lab).textContent = a[1];
  });
  function winding() {
    var ang = [];
    for (var j = 0; j <= N; j++) { var p = g0(j / N); ang.push(Math.atan2(p[1], p[0])); }
    for (j = N; j >= 0; j--) { p = g1(j / N); ang.push(Math.atan2(p[1], p[0])); }
    return Math.round(EV.winding(ang));
  }
  function draw() {
    var s = sl.value / 1000;
    document.getElementById('ev-htpy-sv').textContent = s.toFixed(2);
    document.getElementById('ev-htpy-g0').setAttribute('d', curve(g0));
    document.getElementById('ev-htpy-g1').setAttribute('d', curve(g1));
    document.getElementById('ev-htpy-hs').setAttribute('d', curve(function (t) { return H(t, s); }));
    var fam = document.getElementById('ev-htpy-fam'); EV.clear(fam);
    for (var k = 1; k < 8; k++) E('path', { d: curve(function (t) { return H(t, k / 8); }), fill: 'none', stroke: '#3a3a3a', 'stroke-width': 1 }, fam);
    var h = document.getElementById('ev-htpy-handle'); h.setAttribute('cx', X([0, m])); h.setAttribute('cy', Y([0, m]));
    var hole = document.getElementById('ev-htpy-hole'); EV.clear(hole);
    if (punct) { E('circle', { cx: CX, cy: CY, r: 9, fill: '#121212', stroke: '#d95926', 'stroke-width': 2 }, hole); E('text', { x: CX + 14, y: CY - 10, 'font-size': 13, style: 'fill:#f08a5d' }, hole).textContent = 'hole'; }
    else { E('path', { d: 'M' + (CX - 5) + ',' + CY + 'h10M' + CX + ',' + (CY - 5) + 'v10', stroke: '#6a6a6a', 'stroke-width': 1.5 }, hole); }
    // H passes through 0 only at t = 1/2 (x = 0 there): y = (1 - s)*1.2 + s*m
    var y0 = 1.2, sStar = m < 0 ? y0 / (y0 - m) : null, w = winding(), ws = String(w).replace('-', '−');
    var hitsNow = punct && sStar !== null && Math.abs(s - sStar) < 0.012;
    document.getElementById('ev-htpy-hs').setAttribute('stroke', hitsNow ? '#f0f0f0' : '#d95926');
    var t = document.getElementById('ev-htpy-title'), d = document.getElementById('ev-htpy-detail');
    if (Math.abs(m) < 0.03 && punct) { t.textContent = 'γ₁ runs straight through the hole, so it is not even a path in the punctured plane. Drag the handle off it.'; d.textContent = ''; return; }
    if (!punct) {
      t.textContent = 'In the whole plane every intermediate path Hₛ is fine: the straight-line homotopy always works. ℝ² has no holes to catch on.';
      d.textContent = 'winding number of the loop γ₀ · γ₁⁻¹ around the origin: ' + ws + '   (irrelevant here: nothing is missing from ℝ²)';
      return;
    }
    t.textContent = sStar === null
      ? 'Both paths pass above the hole. Every intermediate path does too, so this is a homotopy in the punctured plane.'
      : hitsNow ? 'At s ≈ ' + sStar.toFixed(2) + ' the intermediate path runs through the hole: this straight-line homotopy leaves the punctured plane.'
      : 'The paths pass on opposite sides of the hole. Somewhere (s ≈ ' + sStar.toFixed(2) + ') the straight line has to cross it. Slide s there.';
    d.textContent = 'winding number of γ₀ · γ₁⁻¹ around the hole: ' + ws + (w === 0 ? '   → the paths are homotopic in ℝ² ∖ {0}' : '   → no homotopy in ℝ² ∖ {0} exists, straight-line or otherwise');
  }
  EV.drag(svg, document.getElementById('ev-htpy-handle'), function (p) { m = Math.max(-1.3, Math.min(1.3, (CY - p.y) / SC)); draw(); });
  sl.addEventListener('input', draw);
  var pb = document.getElementById('ev-htpy-punct');
  pb.addEventListener('click', function () { punct = !punct; pb.textContent = 'puncture: ' + (punct ? 'on' : 'off'); pb.classList.toggle('on', punct); draw(); });
  pb.classList.add('on');
  draw();
})();
</script>

When the endpoints are held fixed throughout, as here, the homotopy is called a homotopy **rel endpoints**. That is the right notion for paths; without it, any path could be reeled in to a constant one.

---

# loops and the fundamental group
{: #loops-and-the-fundamental-group}
A **loop** at $x&#95;{0}$ is a path that starts and ends at $x&#95;{0}$. Two loops can be **concatenated**: run the first at double speed, then the second.

<div class="ev-def"><strong>Definition (fundamental group).</strong> $\pi&#95;{1}(X,x&#95;{0})$ is the set of loops at $x&#95;{0}$ up to homotopy rel endpoints, with concatenation as the product. The identity is the constant loop; the inverse of a loop is the same loop run backwards.</div>

Checking the group laws is a matter of reparametrizing time, and every reparametrization is itself a homotopy. A space in which every loop is homotopic to a constant (and which is path-connected) is **simply connected**: $\pi&#95;{1}=0$. Every convex set is simply connected, by the straight-line homotopy.

The widget above shows the first nontrivial example. In $\mathbb{R}^2\setminus\lbrace 0\rbrace$, the loop "$\gamma&#95;{0}$ then $\gamma&#95;{1}$ backwards" is homotopic to a constant exactly when its winding number is $0$. To prove that, we need to define winding number properly, and the cleanest place to do that is the circle.

---

# the circle: π₁(S¹) = ℤ
{: #the-circle}
<div class="cs-q">
<strong>Student.</strong> Why is a loop around the circle not contractible? It seems obvious, but I can't prove it.
</div>

<div class="cs-a">
<strong>Teacher.</strong> Unroll the circle. Every loop on the circle lifts to a path on the real line, and where the lift ends is an integer that no homotopy can change.
</div>

The map

$$p:\mathbb{R}\to S^1,\qquad p(s)=(\cos 2\pi s,\ \sin 2\pi s)$$

wraps the line around the circle infinitely often. It is a **covering map**: every small arc $U$ of the circle has a preimage that is a disjoint union of copies of $U$ (one per integer), each mapped homeomorphically onto $U$. Picture the line as a helix sitting over the circle, with $p$ as vertical projection.

**Path lifting.** For every path $\gamma$ in $S^1$ starting at $p(0)$ there is exactly one path $\tilde\gamma$ in $\mathbb{R}$ with $\tilde\gamma(0)=0$ and $p\circ\tilde\gamma=\gamma$.

*Why.* By compactness of $[0,1]$ (Vol. I), chop time into finitely many pieces, each of which $\gamma$ maps into one small arc. Over a small arc, the covering is a stack of copies, and you have no choice but to stay on the copy you started in. Glue the pieces. $\square$

**Homotopy lifting.** The same argument, applied to a square $[0,1]\times[0,1]$ instead of an interval, lifts homotopies.

Now define the **degree** of a loop $\gamma$ at $p(0)$ to be $\tilde\gamma(1)$. It is an integer, because $p(\tilde\gamma(1))=\gamma(1)=p(0)$. A homotopy of loops lifts to a homotopy of lifts, along which the endpoint moves continuously in $p^{-1}(p(0))=\mathbb{Z}$. By Vol. I's corollary, it cannot move. So:

$$\deg:\pi_1(S^1)\xrightarrow{\ \cong\ }\mathbb{Z}.$$

(It is onto because $t\mapsto p(nt)$ has degree $n$, and one-to-one because two loops with the same lift endpoint have lifts related by a straight-line homotopy in the convex set $\mathbb{R}$, which projects down.)

<div id="ev-lift" class="cs-stage" style="height:460px;">
  <div class="cs-hud cs-hud-tl" id="ev-lift-hud"></div>
  <div class="cs-hud cs-hud-tr"><span style="color:#6fa8f0;">loop in S¹</span><br><span style="color:#f08a5d;">its lift to ℝ</span><br><span style="color:#e0e0e0;">● integers</span></div>
  <div class="cs-ctrl">
    <label>n <input type="range" id="ev-lift-n" min="-3" max="3" step="1" value="2" style="width:22%"> <span id="ev-lift-nv">2</span></label>
    <label>wiggle <input type="range" id="ev-lift-w" min="0" max="60" value="25" style="width:22%"> <span id="ev-lift-wv">0.25</span></label>
  </div>
</div>
<p class="cs-cap">The helix is $\mathbb{R}$, coiled so that $p(s)=(\cos 2\pi s,\sin 2\pi s)$ is "drop straight down onto the circle". The blue point runs a loop $\theta(t)=2\pi\bigl(nt+w\sin 2\pi t\bigr)$ on the circle; the orange point is its unique lift starting at $0$. However much you wiggle, the lift ends exactly on the integer $n$. That integer is the class of the loop in $\pi&#95;{1}(S^1)$. Drag to turn the picture.</p>
<script>
CS.mount({
  id: 'ev-lift',
  height: 460,
  cam: [0, 0.5, 6.0],
  rotX: 0.2,
  rotY: 0.5,
  noSpin: true,
  setup: function (api) {
    var T = api.THREE, H = 0.36, BASE = -1.75, SMAX = 3.3;
    api.group.position.y = 0.4;
    function helix(s) { return new T.Vector3(Math.cos(2 * Math.PI * s), H * s, Math.sin(2 * Math.PI * s)); }
    var hp = [];
    for (var i = 0; i <= 900; i++) hp.push(helix(-SMAX + 2 * SMAX * i / 900));
    api.group.add(new T.Line(new T.BufferGeometry().setFromPoints(hp), new T.LineBasicMaterial({ color: 0x5a5a5a })));
    var cp = [];
    for (i = 0; i <= 120; i++) cp.push(new T.Vector3(Math.cos(2 * Math.PI * i / 120), BASE, Math.sin(2 * Math.PI * i / 120)));
    api.group.add(new T.Line(new T.BufferGeometry().setFromPoints(cp), new T.LineBasicMaterial({ color: 0x3987e5 })));
    var marks = [];
    for (var k = -3; k <= 3; k++) {
      var mk = new T.Mesh(new T.SphereGeometry(0.05, 12, 12), new T.MeshBasicMaterial({ color: 0xd0d0d0 }));
      mk.position.copy(helix(k)); api.group.add(mk); marks.push(mk);
    }
    var bp = new T.Mesh(new T.SphereGeometry(0.05, 12, 12), new T.MeshBasicMaterial({ color: 0xd0d0d0 }));
    bp.position.set(1, BASE, 0); api.group.add(bp);
    var MAXP = 400, trailPos = new Float32Array(MAXP * 3), trailGeo = new T.BufferGeometry();
    trailGeo.setAttribute('position', new T.BufferAttribute(trailPos, 3));
    api.group.add(new T.Line(trailGeo, new T.LineBasicMaterial({ color: 0xd95926 })));
    var lp = new T.Mesh(new T.SphereGeometry(0.075, 16, 16), new T.MeshBasicMaterial({ color: 0xd95926 }));
    var cpnt = new T.Mesh(new T.SphereGeometry(0.075, 16, 16), new T.MeshBasicMaterial({ color: 0x3987e5 }));
    api.group.add(lp); api.group.add(cpnt);
    var dropGeo = new T.BufferGeometry().setFromPoints([new T.Vector3(), new T.Vector3()]);
    var drop = new T.Line(dropGeo, new T.LineDashedMaterial({ color: 0x8a8a8a, dashSize: 0.06, gapSize: 0.05 }));
    api.group.add(drop);
    var hud = document.getElementById('ev-lift-hud');
    var n = 2, w = 0.25, t = 0, hold = 0;
    function lift(tt) { return n * tt + w * Math.sin(2 * Math.PI * tt); }
    function sync() {
      n = parseInt(document.getElementById('ev-lift-n').value, 10);
      w = parseInt(document.getElementById('ev-lift-w').value, 10) / 100;
      document.getElementById('ev-lift-nv').textContent = n;
      document.getElementById('ev-lift-wv').textContent = w.toFixed(2);
      t = 0; hold = 0;
      marks.forEach(function (m, j) { m.material.color.setHex(j - 3 === n ? 0xf0f0f0 : 0x6a6a6a); m.scale.setScalar(j - 3 === n ? 1.6 : 1); });
    }
    document.getElementById('ev-lift-n').addEventListener('input', sync);
    document.getElementById('ev-lift-w').addEventListener('input', sync);
    sync();
    return function () {
      if (hold > 0) hold--; else { t += 0.004; if (t >= 1) { t = 1; hold = 70; } }
      if (hold === 1) t = 0;
      var cnt = Math.max(2, Math.round(t * (MAXP - 1)) + 1);
      for (var j = 0; j < cnt; j++) { var v = helix(lift(t * j / (cnt - 1))); trailPos[3 * j] = v.x; trailPos[3 * j + 1] = v.y; trailPos[3 * j + 2] = v.z; }
      trailGeo.attributes.position.needsUpdate = true;
      trailGeo.setDrawRange(0, cnt);
      var s = lift(t), top = helix(s), th = 2 * Math.PI * s;
      lp.position.copy(top);
      cpnt.position.set(Math.cos(th), BASE, Math.sin(th));
      dropGeo.setFromPoints([top, cpnt.position.clone()]);
      drop.computeLineDistances();
      if (hud) hud.innerHTML = 't = ' + t.toFixed(2) + '<br>lift s(t) = ' + (s < -0.005 ? '−' : '') + Math.abs(s).toFixed(2) +
        (t >= 1 ? '<br><span style="color:#f0f0f0">ends at ' + (n < 0 ? '−' : '') + Math.abs(n) + ' = the class in π₁(S¹)</span>' : '<br>start: s(0) = 0');
    };
  }
});
</script>

The **winding number** of a loop $\gamma$ in $\mathbb{R}^2\setminus\lbrace 0\rbrace$ is the degree of $\gamma/\lVert\gamma\rVert$, a loop on the unit circle. The straight-line homotopy $(1-s)\gamma+s\,\gamma/\lVert\gamma\rVert$ never hits $0$, so $\mathbb{R}^2\setminus\lbrace 0\rbrace$ and $S^1$ have the same loops up to homotopy: $\pi&#95;{1}(\mathbb{R}^2\setminus\lbrace 0\rbrace)\cong\mathbb{Z}$. That is the missing proof for the first widget.

Keep this pattern in mind; it is the whole of [Vol. V](/blog/2026/08/17/circling-the-sphere-Vol-V) in miniature. A covering map $E\to B$ with discrete fibre $F$ (here $\mathbb{R}\to S^1$, fibre $\mathbb{Z}$), plus the fact that $E$ has no interesting loops, computes the loops of $B$ from the points of $F$.

---

# the sphere: π₁(S²) = 0
{: #the-sphere}
Now go up a dimension. Take a loop on $S^2$. If it misses some point $q$, then it lives in $S^2\setminus\lbrace q\rbrace$, and **stereographic projection** from $q$ is a homeomorphism $S^2\setminus\lbrace q\rbrace\to\mathbb{R}^2$. In $\mathbb{R}^2$ the straight-line homotopy shrinks the loop to a point. Project back.

<div id="ev-s2loop" class="cs-stage" style="height:440px;">
  <div class="cs-hud cs-hud-tl" id="ev-s2-hud"></div>
  <div class="cs-hud cs-hud-tr"><span style="color:#f08a5d;">● removed points</span><br><span style="color:#e0a526;">the loop</span></div>
  <div class="cs-ctrl">
    <label>slide <input type="range" id="ev-s2-s" min="0" max="1000" value="0"></label>
    <label><input type="checkbox" id="ev-s2-n"> also remove the north pole</label>
  </div>
</div>
<p class="cs-cap">A loop drawn around the removed south pole. On $S^2\setminus\lbrace S\rbrace$ it slides up over the equator and shrinks to a point at the top: the sphere minus a point is a plane in disguise, and every loop in it is contractible. Remove the north pole too and the space becomes a cylinder; the same loop is caught between the two holes.</p>
<script>
CS.mount({
  id: 'ev-s2loop',
  height: 440,
  cam: [0, 0.3, 3.9],
  rotX: 0.35,
  setup: function (api) {
    var T = api.THREE;
    var geo = new T.SphereGeometry(1, 48, 32);
    api.group.add(new T.Mesh(geo, new T.MeshStandardMaterial({ color: 0x2c3e57, metalness: 0.15, roughness: 0.6, transparent: true, opacity: 0.5, side: T.DoubleSide, depthWrite: false })));
    api.group.add(new T.Mesh(geo, new T.MeshBasicMaterial({ color: 0x8a8a8a, wireframe: true, transparent: true, opacity: 0.12 })));
    function hole(y) {
      var m = new T.Mesh(new T.SphereGeometry(0.06, 16, 16), new T.MeshBasicMaterial({ color: 0xd95926 }));
      m.position.set(0, y, 0); api.group.add(m); return m;
    }
    hole(-1);
    var north = hole(1);
    var NP = 160;
    var tube = null, mat = new T.MeshBasicMaterial({ color: 0xc98500 });
    var hud = document.getElementById('ev-s2-hud'), sl = document.getElementById('ev-s2-s'), cb = document.getElementById('ev-s2-n');
    function update() {
      var s = sl.value / 1000, stuck = cb.checked;
      north.visible = stuck;
      var beta = 0.88 * Math.PI * (1 - s); // polar angle from the north pole
      var floor = 0.22;
      var capped = stuck && beta < floor;
      if (capped) beta = floor;
      var pts = [];
      for (var i = 0; i <= NP; i++) {
        var ph = 2 * Math.PI * i / NP, r = Math.sin(beta) * 1.012;
        pts.push(new T.Vector3(r * Math.cos(ph), 1.012 * Math.cos(beta), r * Math.sin(ph)));
      }
      if (tube) { api.group.remove(tube); tube.geometry.dispose(); }
      if (beta > 0.012) {
        tube = new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(pts, true), 160, 0.022, 8, true), mat);
        api.group.add(tube);
      } else tube = null;
      if (hud) hud.innerHTML = stuck
        ? (capped ? 'S² ∖ {S, N} is a cylinder.<br>The loop cannot pass the north hole:<br>it winds once around the cylinder.' : 'S² ∖ {S, N}: slide the loop up …')
        : (beta <= 0.012 ? 'S² ∖ {S}: the loop has shrunk to a point.<br>π₁(S²) = 0.' : 'S² ∖ {S}: the loop slides over the equator …');
    }
    sl.addEventListener('input', update);
    cb.addEventListener('change', update);
    update();
    return null;
  }
});
</script>

There is a real gap in that argument, and it is worth seeing. A continuous loop *can* hit every point of $S^2$: space-filling curves exist. The repair is to first homotope the loop to a smooth one (approximate it by a smooth loop close enough that the straight-line homotopy between them, pushed back onto the sphere, is well defined). A smooth map from a 1-dimensional thing into a 2-dimensional thing has an image of area zero (this is the easy case of **Sard's theorem**), so it misses a point. Then stereographic projection finishes. Therefore

$$\pi_1(S^2)=0.$$

Compare the circle: there the loop that goes once around cannot miss a point, and it is exactly the loop that does not shrink.

---

# higher homotopy groups
{: #higher-homotopy-groups}
A loop is a map from $S^1$. Replace $S^1$ by $S^k$ and you get the **higher homotopy groups**:

<div class="ev-def"><strong>Definition.</strong> $\pi&#95;{k}(X)$ is the set of maps $S^k\to X$ sending a base point to a base point, up to homotopy that keeps the base point fixed. For $k\ge 1$ it is a group; for $k\ge 2$ it is abelian. $\pi&#95;{0}(X)$ is the set of path components.</div>

The argument for $\pi&#95;{1}(S^2)=0$ works word for word in every dimension where the domain is smaller than the target:

<div class="ev-def"><strong>Theorem.</strong> $\pi&#95;{k}(S^n)=0$ for $k&lt;n$.</div>

*Proof.* Homotope $f:S^k\to S^n$ to a smooth map. Since $k&lt;n$, its image has $n$-dimensional measure zero (Sard), so it misses a point $q$. Stereographic projection from $q$ carries $S^n\setminus\lbrace q\rbrace$ to $\mathbb{R}^n$, where the straight-line homotopy contracts $f$ (to the base point, if we contract toward it). $\square$

We will use exactly one instance of this, in [Vol. V](/blog/2026/08/17/circling-the-sphere-Vol-V):

$$\pi_2(S^3)=0.$$

A 2-sphere inside a 3-sphere always has room to shrink. When the dimensions match, the answer is instead $\pi&#95;{n}(S^n)\cong\mathbb{Z}$, the **degree** again: how many times, with sign, the map covers the target. We met the $n=1$ case above; the $n=2$ case is the degree of the Gauss map in [Vol. IV](/blog/2026/08/17/circling-the-sphere-Vol-IV). And a warning, to show the theorem above is not "obvious": when the domain is *bigger*, things are wild. $\pi&#95;{3}(S^2)\cong\mathbb{Z}$, generated by the Hopf fibration, a map from the 3-sphere onto the 2-sphere that no homotopy can undo.

---

# where this goes
{: #where-this-goes}
Two computations to carry forward, and one principle:

1. $\pi&#95;{1}(S^1)=\mathbb{Z}$, via the covering $\mathbb{R}\to S^1$. It will reappear as the turning number of a plane curve in [Vol. IV](/blog/2026/08/17/circling-the-sphere-Vol-IV).
2. $\pi&#95;{2}(S^3)=0$, via Sard and stereographic projection. It will be the last link in the proof in [Vol. V](/blog/2026/08/17/circling-the-sphere-Vol-V).
3. **Homotopy invariants are discrete, and discrete things cannot move continuously.** That is Vol. I's corollary, and every obstruction in this series is an instance of it.

But nothing so far knows about *smoothness*. Homotopy lets a sphere be crushed to a point, folded flat, and unfolded. To say what is forbidden in an eversion we need derivatives, and a sphere to take them on.

---

**Next:** [Vol. III: Manifolds and Immersions](/blog/2026/08/17/circling-the-sphere-Vol-III)

*Sphere Eversion:* [Vol. I](/blog/2026/08/17/circling-the-sphere) · **Vol. II** · [Vol. III](/blog/2026/08/17/circling-the-sphere-Vol-III) · [Vol. IV](/blog/2026/08/17/circling-the-sphere-Vol-IV) · [Vol. V](/blog/2026/08/17/circling-the-sphere-Vol-V) · [Vol. VI](/blog/2026/08/17/circling-the-sphere-Vol-VI)
