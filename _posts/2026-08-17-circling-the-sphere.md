---
layout: post
title: "Circling the Sphere"
date: 2026-08-17
categories: differential topology
mathjax: true
---

*A Socratic return to the two-sphere: the questions from a local Phi-3 session, answered so that the pictures are the equations.*

In May 2024 I asked a small language model, running locally, to talk me through Smale's theorem that any two immersions of $S^2$ in $\mathbb{R}^3$ are regularly homotopic. The transcript is [Sphere Eversion Phi3 Notes I](/blog/2024/05/22/sphere-eversion-phi3-notes-I). The questions were the right questions. The proofs were not: a linear interpolation was offered as a regular homotopy, the hairy-ball theorem was credited to Smale, and $S^2\times[0,1]$ was described as a solid ball.

In September I wrote a straight exposition, [The Eversion of the Sphere](/blog/2024/09/27/the-eversion-of-the-sphere). It had the theorem right and the pictures wrong. The interactive "eversion" flattened $z$ through zero --- exactly the crease the text forbade --- and the "Morin surface" was an unnamed polynomial that did not match any formula on the page.

This post is the two of them talking. The student is the transcript. The teacher is the theorem, at the level of a motivated undergraduate who has partial derivatives, the chain rule, and the rank of a matrix. Every canvas is a displayed equation with a slider.

The still below is a genuine eversion (Morin's halfway model). We will not pretend to reproduce that movie with a one-line formula. We will write the formulae we *can* write, and refuse to draw a crease and call it an eversion.

<p style="text-align:center;">
  <img src="/blog/assets/2024/eversion/eversion.gif" alt="Sphere eversion through the Morin halfway model" style="max-width:100%;">
</p>

<style>
  .cs-q, .cs-a { padding: 0.8em 1em; margin: 1.5em 0 0.6em; border-radius: 0 8px 8px 0; }
  .cs-q { border-left: 3px solid #FFA7CC; background: rgba(255,167,204,0.07); }
  .cs-a { border-left: 3px solid #00FFFF; background: rgba(0,255,255,0.05); }
  .cs-q strong { color: #FFA7CC; }
  .cs-a strong { color: #00FFFF; }
  .cs-stage { width: 100%; margin: 1.4em 0 0.4em; border-radius: 8px; overflow: hidden; background: #0f172a; position: relative; touch-action: none; }
  .cs-hud { position: absolute; z-index: 10; font-family: inherit; font-size: 12px; color: #94a3b8; pointer-events: none; }
  .cs-hud-tl { top: 10px; left: 12px; }
  .cs-hud-tr { top: 10px; right: 12px; text-align: right; }
  .cs-ctrl { position: absolute; bottom: 8px; left: 10px; right: 10px; z-index: 10; text-align: center; color: #94a3b8; font-size: 13px; }
  .cs-ctrl label { display: inline-block; margin: 2px 8px; }
  .cs-ctrl input[type="range"] { width: 42%; vertical-align: middle; }
  .cs-ctrl select { background: #1e293b; color: #e2e8f0; border: 1px solid #475569; border-radius: 4px; padding: 2px 6px; font-family: inherit; font-size: 12px; }
  .cs-cap { color: #94a3b8; font-size: 0.92em; margin: 0 0 1.8em; }
  /* Override global table glass (white bg + light MathJax = invisible formulas). */
  .cs-err {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.95em;
    margin: 1em 0 2em;
    background: #141414 !important;
    color: #e8e8e8;
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 8px;
    overflow: hidden;
  }
  .cs-err th, .cs-err td {
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 0.7em 0.9em;
    vertical-align: top;
    color: #e8e8e8 !important;
    background: transparent !important;
    font-weight: 400;
  }
  .cs-err thead th {
    background: rgba(255, 167, 204, 0.14) !important;
    color: #fafafa !important;
    font-weight: 600;
  }
  .cs-err tbody tr:nth-child(even) td {
    background: rgba(255, 255, 255, 0.04) !important;
  }
  .cs-err mjx-container {
    color: #f5f5f5 !important;
  }
  .mermaid .nodeLabel, .mermaid .label, .mermaid .nodeLabel span {
    font-weight: 400 !important;
    color: #e2e8f0 !important;
  }
  .mermaid .edgeLabel, .mermaid .edgeLabel span {
    color: #cbd5e1 !important;
    background-color: transparent !important;
  }
</style>

<script>
(function () {
  window.CS = window.CS || {};
  CS.ready = function (cb) {
    var n = 0;
    (function wait() {
      if (typeof THREE !== 'undefined') { cb(window.THREE); return; }
      if (++n > 300) return;
      setTimeout(wait, 40);
    })();
  };
  CS.mount = function (opts) {
    CS.ready(function (THREE) {
      var el = document.getElementById(opts.id);
      if (!el || el.getAttribute('data-cs') === '1') return;
      function boot() {
        if (el.clientWidth < 16) { setTimeout(boot, 120); return; }
        if (el.getAttribute('data-cs') === '1') return;
        el.setAttribute('data-cs', '1');
        var height = opts.height || 420;
        var scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0f172a);
        var camera;
        if (opts.ortho) {
          var halfW = opts.orthoHalf || 3.3;
          var asp = el.clientWidth / height;
          camera = new THREE.OrthographicCamera(-halfW, halfW, halfW / asp, -halfW / asp, 0.05, 80);
        } else {
          camera = new THREE.PerspectiveCamera(50, el.clientWidth / height, 0.05, 200);
        }
        var cam = opts.cam || [0, 0.35, 4.1];
        camera.position.set(cam[0], cam[1], cam[2]);
        var renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        renderer.setSize(el.clientWidth, height);
        el.appendChild(renderer.domElement);
        var group = new THREE.Group();
        scene.add(group);
        if (!opts.noLights) {
          scene.add(new THREE.AmbientLight(0xffffff, 0.42));
          var d1 = new THREE.DirectionalLight(0xffffff, 0.9);
          d1.position.set(5, 5, 6);
          scene.add(d1);
          var d2 = new THREE.DirectionalLight(0x818cf8, 0.35);
          d2.position.set(-5, -2, -4);
          scene.add(d2);
        }
        var rotX = opts.rotX || 0.28;
        var rotY = opts.rotY || 0.45;
        var dragging = false, lx = 0, ly = 0, visible = true;
        function down(x, y) { dragging = true; lx = x; ly = y; }
        function move(x, y) {
          if (!dragging) return;
          rotY += (x - lx) * 0.008;
          rotX += (y - ly) * 0.008;
          if (rotX > 1.35) rotX = 1.35;
          if (rotX < -1.35) rotX = -1.35;
          lx = x; ly = y;
        }
        function up() { dragging = false; }
        el.addEventListener('mousedown', function (e) { down(e.clientX, e.clientY); });
        window.addEventListener('mouseup', up);
        window.addEventListener('mousemove', function (e) { move(e.clientX, e.clientY); });
        el.addEventListener('touchstart', function (e) {
          if (e.touches[0]) down(e.touches[0].clientX, e.touches[0].clientY);
        }, { passive: true });
        el.addEventListener('touchend', up);
        el.addEventListener('touchmove', function (e) {
          if (e.touches[0]) move(e.touches[0].clientX, e.touches[0].clientY);
        }, { passive: true });
        window.addEventListener('resize', function () {
          var w = el.clientWidth;
          if (w < 16) return;
          if (camera.isOrthographicCamera) {
            var hW = opts.orthoHalf || 3.3;
            var a = w / height;
            camera.left = -hW; camera.right = hW;
            camera.top = hW / a; camera.bottom = -hW / a;
          } else {
            camera.aspect = w / height;
          }
          camera.updateProjectionMatrix();
          renderer.setSize(w, height);
        });
        if (typeof IntersectionObserver !== 'undefined') {
          var io = new IntersectionObserver(function (ents) {
            visible = !!(ents[0] && ents[0].isIntersecting);
          }, { threshold: 0.04 });
          io.observe(el);
        }
        var api = { THREE: THREE, el: el, scene: scene, camera: camera, renderer: renderer, group: group };
        var tick = opts.setup ? opts.setup(api) : null;
        (function loop() {
          requestAnimationFrame(loop);
          if (!visible) return;
          if (!opts.freeze && !opts.noSpin && !dragging) rotY += 0.0028;
          if (!opts.freeze) group.rotation.set(rotX, rotY, 0);
          if (tick) tick(api);
          renderer.render(scene, camera);
        })();
      }
      boot();
    });
  };
})();
</script>

---

# the two-sphere, locally flat

<div class="cs-q">
<strong>Student.</strong> What is a manifold? What is a differentiable manifold? Give an example. Then give differentiable coordinates on $S^2$ and take a derivative at $(1,0,0)$.
</div>

<div class="cs-a">
<strong>Teacher.</strong> A manifold is a space that is Euclidean in the small. Formally, a smooth $n$-manifold is a Hausdorff space covered by charts $\varphi\sb{\alpha}: U\sb{\alpha}\to\mathbb{R}^n$ whose transition maps $\varphi\sb{\beta}\circ\varphi\sb{\alpha}^{-1}$ are $C^\infty$. You already know one: the surface of the Earth. No single paper map covers it, but an atlas does, and the overlap rules are smooth.
</div>

The **2-sphere** is the set of unit vectors,

$$S^2=\bigl\{(x,y,z)\in\mathbb{R}^3:x^2+y^2+z^2=1\bigr\}.$$

Spherical coordinates are a pair of charts (you need at least two: the azimuth $\varphi$ is not a global coordinate). On the complement of a meridian,

$$\mathbf{r}(\theta,\varphi)=\bigl(\sin\theta\cos\varphi,\;\sin\theta\sin\varphi,\;\cos\theta\bigr),\qquad \theta\in(0,\pi),\;\varphi\in(0,2\pi).$$

A **point** is not a function of $(\theta,\varphi)$. The model that answered you computed $\partial\sb{\theta}(1,0,0)=\mathbf{0}$ and called it a day. The object that has derivatives is the chart:

$$
\begin{aligned}
\mathbf{r}_\theta&=(\cos\theta\cos\varphi,\;\cos\theta\sin\varphi,\;-\sin\theta),\\
\mathbf{r}_\varphi&=(-\sin\theta\sin\varphi,\;\sin\theta\cos\varphi,\;0).
\end{aligned}
$$

At $(1,0,0)$ one has $(\theta,\varphi)=(\pi/2,\,0)$, so

$$\mathbf{r}_\theta=(0,0,-1),\qquad \mathbf{r}_\varphi=(0,1,0),\qquad \mathbf{r}_\theta\times\mathbf{r}_\varphi=(1,0,0)=\mathbf{r}.$$

Those two vectors are a basis of the tangent plane $T\sb{(1,0,0)}S^2$, the $yz$-plane. Drag the sliders; the cyan and pink arrows are exactly $\mathbf{r}\sb{\theta}$ and $\mathbf{r}\sb{\varphi}$.

<div id="cs-charts" class="cs-stage" style="height:440px;">
  <div class="cs-hud cs-hud-tl" id="cs-charts-eq">r, r_theta, r_phi</div>
  <div class="cs-ctrl">
    <label>theta <input type="range" id="cs-th" min="8" max="172" value="90"> <span id="cs-th-v">pi/2</span></label>
    <label>phi <input type="range" id="cs-ph" min="0" max="628" value="0"> <span id="cs-ph-v">0</span></label>
  </div>
</div>
<p class="cs-cap">The sphere is the image of $\mathbf{r}$. Cyan is $\mathbf{r}\sb{\theta}$, pink is $\mathbf{r}\sb{\varphi}$, gold is their cross product. At the poles $\sin\theta=0$ and the <em>chart</em> is singular; the sphere is not. That distinction is the whole subject.</p>

<script>
CS.mount({
  id: 'cs-charts',
  height: 440,
  cam: [0, 0.2, 3.6],
  setup: function (api) {
    var T = api.THREE;
    var geo = new T.SphereGeometry(1, 48, 32);
    api.group.add(new T.Mesh(geo, new T.MeshStandardMaterial({
      color: 0x312e81, metalness: 0.2, roughness: 0.55, transparent: true, opacity: 0.35, side: T.DoubleSide
    })));
    api.group.add(new T.Mesh(geo, new T.MeshBasicMaterial({
      color: 0xa5b4fc, wireframe: true, transparent: true, opacity: 0.18
    })));
    var pt = new T.Mesh(new T.SphereGeometry(0.045, 16, 16), new T.MeshStandardMaterial({ color: 0xfbbf24, emissive: 0xf59e0b, emissiveIntensity: 0.4 }));
    api.group.add(pt);
    var aTh = new T.ArrowHelper(new T.Vector3(0, 0, -1), new T.Vector3(1, 0, 0), 0.7, 0x22d3ee, 0.12, 0.08);
    var aPh = new T.ArrowHelper(new T.Vector3(0, 1, 0), new T.Vector3(1, 0, 0), 0.7, 0xf472b6, 0.12, 0.08);
    var aN  = new T.ArrowHelper(new T.Vector3(1, 0, 0), new T.Vector3(1, 0, 0), 0.55, 0xfbbf24, 0.1, 0.07);
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
          'r_theta x r_phi  =  sin(theta) r<br>' +
          '|r_theta x r_phi| = ' + nlen.toFixed(3) + (nlen < 0.08 ? '   chart singular' : '');
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
<strong>Student.</strong> Give a nonzero derivative --- a function that wraps around the sphere.
</div>

<div class="cs-a">
<strong>Teacher.</strong> Take the equator as a curve $\gamma:[0,2\pi]\to S^2$,
$$\gamma(t)=(\cos t,\;\sin t,\;0).$$
Then $\gamma'(t)=(-\sin t,\;\cos t,\;0)\neq\mathbf{0}$. At $t=0$ this is $(0,1,0)$, which is $\mathbf{r}\sb{\varphi}$ at $(1,0,0)$. The model wrote $\gamma(t)=(\sin(\pi t),0,\cos(\pi t))$ and claimed it was the equator with $\varphi$ fixed at $0$; that is a meridian, a semicircle from north pole to south, and at its midpoint the velocity is $(0,0,-\pi)$, not a trip around the equator. Wrapping around $S^2$ means the image of $\gamma$ is a closed loop that is not contractible in $S^2\setminus\{\text{two poles}\}$. We will need that loop.
</div>

---

# immersions, and the matrix that must not drop rank

<div class="cs-q">
<strong>Student.</strong> What is an immersion? What is a Jacobian? What happens when the Jacobian determinant is zero, or switches sign?
</div>

<div class="cs-a">
<strong>Teacher.</strong> For $f:\mathbb{R}^n\to\mathbb{R}^m$ the Jacobian is the $m\times n$ matrix of first partials --- rows are outputs, columns are inputs. The model wrote $n\times m$. An <strong>immersion</strong> $f:M\to N$ is a smooth map whose differential $df\sb{p}:T\sb{p}M\to T\sb{f(p)}N$ is injective at every $p$. For $f:S^2\to\mathbb{R}^3$ that is the statement that the $3\times 2$ matrix
$$
J_f=\begin{pmatrix}
\partial_u f_1 & \partial_v f_1 \\
\partial_u f_2 & \partial_v f_2 \\
\partial_u f_3 & \partial_v f_3
\end{pmatrix}
$$
has rank $2$ everywhere, equivalently $\mathbf{f}\sb{u}\times\mathbf{f}\sb{v}\neq\mathbf{0}$. There is no $2\times 2$ determinant to watch. The only vanishing that matters is that cross product.
</div>

A sign change of $\det J$ for a map $\mathbb{R}^n\to\mathbb{R}^n$ means the map reverses orientation. It does **not** mean a saddle: $f(x,y)=(e^x\cos y,\,e^x\sin y)$ has $\det J=e^{2x}>0$ everywhere (it is a local diffeomorphism, the complex exponential). At $(0,\pi/2)$ one has $\det J=1$, not $-1$, and there is no critical point. Vanishing of $\det J$ *does* mean the inverse-function theorem fails: the map is not a local diffeomorphism there.

Self-intersection is allowed. A figure-eight $\gamma(t)=(\sin 2t,\,\sin t)$ is an immersion --- $\gamma'$ never vanishes --- and it crosses itself. An **embedding** is an injective immersion (proper, on noncompact manifolds). The standard sphere $\iota(p)=p$ is an embedding. Mid-eversion surfaces are immersions and not embeddings.

---

# the homotopy that is not regular

<div class="cs-q">
<strong>Student.</strong> Any two $C^2$ immersions of $S^2$ in $E^3$ are regularly homotopic. Here is a proof: $H(x,t)=(1-t)f\sb{0}(x)+t f\sb{1}(x)$. Also, what is $S^2\times[0,1]$?
</div>

<div class="cs-a">
<strong>Teacher.</strong> $S^2\times[0,1]$ is a <em>thickened sphere</em>: a spherical shell, not the ball. Each point of $S^2$ grows an interval. A homotopy of maps $S^2\to\mathbb{R}^3$ is a single map
$$F:S^2\times[0,1]\to\mathbb{R}^3.$$
It is a <strong>regular homotopy</strong> when each slice $F(\,\cdot\,,t)$ is an immersion. Straight-line interpolation between immersions is a homotopy of smooth maps and almost never a regular homotopy. It routinely drops rank.
</div>

The sock-push is the interpolation from the identity to reflection through the equator,

$$F_s(\theta,\varphi)=\bigl(\sin\theta\cos\varphi,\;\sin\theta\sin\varphi,\;(1-2s)\cos\theta\bigr).$$

A short computation:

$$
\mathbf{F}_\theta\times\mathbf{F}_\varphi=\bigl((1-2s)\sin^2\theta\cos\varphi,\;(1-2s)\sin^2\theta\sin\varphi,\;\sin\theta\cos\theta\bigr),
$$

$$
\bigl\|\mathbf{F}_\theta\times\mathbf{F}_\varphi\bigr\|=\lvert\sin\theta\rvert\sqrt{(1-2s)^2\sin^2\theta+\cos^2\theta}.
$$

At $s=\tfrac12$ this is $\lvert\sin\theta\cos\theta\rvert$, which is zero all along the equator. The image is a disk covered twice, with a fold on the boundary. That is a crease. Colour in the canvas is $\lVert\mathbf{F}\sb{\theta}\times\mathbf{F}\sb{\varphi}\rVert$: indigo is a healthy tangent plane, red is rank drop.

<div id="cs-crease" class="cs-stage" style="height:460px;">
  <div class="cs-hud cs-hud-tl" id="cs-crease-hud">min |F_theta x F_phi|</div>
  <div class="cs-hud cs-hud-tr"><span style="color:#818cf8;">high rank</span><br><span style="color:#ef4444;">rank drop</span></div>
  <div class="cs-ctrl">
    <label>s <input type="range" id="cs-s" min="0" max="100" value="0"> <span id="cs-s-v">0.00</span></label>
  </div>
</div>
<p class="cs-cap">$F\sb{s}(\theta,\varphi)=(\sin\theta\cos\varphi,\,\sin\theta\sin\varphi,\,(1-2s)\cos\theta)$. This is <em>not</em> an eversion. At $s=1$ you have reflected the sphere through the $xy$-plane, and at $s=1/2$ you have left $\mathrm{Imm}(S^2,\mathbb{R}^3)$.</p>

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
      return [0.85 * (1 - u) + 0.39 * u, 0.18 * (1 - u) + 0.4 * u, 0.27 * (1 - u) + 0.95 * u, mag];
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
        hud.innerHTML = 'min |F_theta x F_phi| = ' + minJ.toFixed(3) +
          (minJ < 0.04 ? '<br>CREASE --- not an immersion' : '<br>immersion');
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

An **eversion** is a regular homotopy from the inclusion $\iota(p)=p$ to the antipodal embedding $\alpha(p)=-p$. The map $\alpha$ reverses orientation of $\mathbb{R}^3$ ($\det D\alpha=(-1)^3=-1$), and the outward normal of the image sphere at $-p$ is $-p$, while the pushed tangent frame produces the opposite normal. Inside has become outside. $F\sb{s}$ never reaches $\alpha$. It reaches a reflection, and it cheats.

---

# circling in one dimension less

<div class="cs-q">
<strong>Student.</strong> Why can't we just push it through? And if a sphere can turn inside out, can a circle?
</div>

<div class="cs-a">
<strong>Teacher.</strong> A circle cannot, not in the plane. That is the Whitney--Graustein theorem, and it is the reason eversion feels impossible.
</div>

An immersed closed curve $\gamma:S^1\to\mathbb{R}^2$ has a unit tangent $\mathbf{T}(t)=\gamma'(t)/\lVert\gamma'(t)\rVert\in S^1$. The **turning number** is how many times $\mathbf{T}$ wraps the unit circle,

$$\tau(\gamma)=\frac{1}{2\pi}\bigl(\theta(2\pi)-\theta(0)\bigr)=\frac{1}{2\pi}\int_{S^1}d\theta,\qquad \mathbf{T}=(\cos\theta,\sin\theta).$$

For $\gamma(t)=(\cos t,\sin t)$ one has $\mathbf{T}(t)=(-\sin t,\cos t)$ and $\tau=+1$. For the reflected parametrization $\bar\gamma(t)=(\cos t,-\sin t)$ one has $\tau=-1$. Turning number is an integer and varies continuously under regular homotopy, so it cannot jump. Therefore $\gamma$ and $\bar\gamma$ lie in different path-components of $\operatorname{Imm}(S^1,\mathbb{R}^2)$. The figure-eight $(\sin 2t,\,\sin t)$ has $\tau=0$.

The yellow curve on the right is the **tangent indicatrix**, the path of $\mathbf{T}$ on $S^1$. Count windings. That integer is the obstruction.

<div id="cs-turning" class="cs-stage" style="height:400px;">
  <div class="cs-hud cs-hud-tl" id="cs-turn-hud">turning number</div>
  <div class="cs-hud cs-hud-tr">left: gamma<br>right: T(S^1)</div>
  <div class="cs-ctrl">
    <label>curve
      <select id="cs-turn-sel">
        <option value="circle">circle, tau = +1</option>
        <option value="reflected">reflected, tau = -1</option>
        <option value="eight">figure-eight, tau = 0</option>
      </select>
    </label>
  </div>
</div>
<p class="cs-cap">Left: $\gamma$ and $\mathbf{T}$. Right: the indicatrix. $\tau$ is the winding of the yellow curve, accumulated live as the gold point runs.</p>

<script>
CS.mount({
  id: 'cs-turning',
  height: 400,
  ortho: true,
  orthoHalf: 3.15,
  freeze: true,
  noLights: true,
  noSpin: true,
  cam: [0, 0, 6],
  setup: function (api) {
    var T = api.THREE;
    var curves = {
      circle: function (t) { return [Math.cos(t), Math.sin(t)]; },
      reflected: function (t) { return [Math.cos(t), -Math.sin(t)]; },
      eight: function (t) { return [Math.sin(2 * t) * 0.85, Math.sin(t) * 1.15]; }
    };
    var dcurves = {
      circle: function (t) { return [-Math.sin(t), Math.cos(t)]; },
      reflected: function (t) { return [-Math.sin(t), -Math.cos(t)]; },
      eight: function (t) { return [1.7 * Math.cos(2 * t), 1.15 * Math.cos(t)]; }
    };
    var gCurve = new T.Group();
    var gTan = new T.Group();
    api.scene.add(gCurve);
    api.scene.add(gTan);
    var type = 'circle';
    var phase = 0;
    var hud = document.getElementById('cs-turn-hud');
    function unit(d) {
      var L = Math.hypot(d[0], d[1]) || 1;
      return [d[0] / L, d[1] / L];
    }
    function ang(u) { return Math.atan2(u[1], u[0]); }
    function unwrap(prev, a) {
      var d = a - prev;
      while (d > Math.PI) d -= 2 * Math.PI;
      while (d < -Math.PI) d += 2 * Math.PI;
      return prev + d;
    }
    function rebuild() {
      while (gCurve.children.length) {
        var c = gCurve.children[0];
        if (c.geometry) c.geometry.dispose();
        gCurve.remove(c);
      }
      while (gTan.children.length) {
        var d = gTan.children[0];
        if (d.geometry) d.geometry.dispose();
        gTan.remove(d);
      }
      var N = 220, pts = [], tpts = [], ref = [];
      var th0 = null, th = 0;
      for (var i = 0; i <= N; i++) {
        var t = (i / N) * 2 * Math.PI;
        var p = curves[type](t);
        var u = unit(dcurves[type](t));
        pts.push(new T.Vector3(p[0] - 1.35, p[1], 0));
        tpts.push(new T.Vector3(u[0] + 1.55, u[1], 0));
        var a = ang(u);
        if (th0 === null) { th0 = a; th = a; } else th = unwrap(th, a);
      }
      for (var j = 0; j <= 64; j++) {
        var s = (j / 64) * 2 * Math.PI;
        ref.push(new T.Vector3(Math.cos(s) + 1.55, Math.sin(s), 0));
      }
      gCurve.add(new T.Line(new T.BufferGeometry().setFromPoints(pts), new T.LineBasicMaterial({ color: 0x818cf8 })));
      gTan.add(new T.Line(new T.BufferGeometry().setFromPoints(tpts), new T.LineBasicMaterial({ color: 0xfbbf24 })));
      gTan.add(new T.Line(new T.BufferGeometry().setFromPoints(ref), new T.LineBasicMaterial({ color: 0x334155 })));
      api._tauClosed = (th - th0) / (2 * Math.PI);
    }
    var dotG = new T.Mesh(new T.SphereGeometry(0.07, 12, 12), new T.MeshBasicMaterial({ color: 0xfbbf24 }));
    var dotT = new T.Mesh(new T.SphereGeometry(0.07, 12, 12), new T.MeshBasicMaterial({ color: 0x22d3ee }));
    api.scene.add(dotG); api.scene.add(dotT);
    var arrow = new T.ArrowHelper(new T.Vector3(1, 0, 0), new T.Vector3(), 0.42, 0x22d3ee, 0.1, 0.07);
    api.scene.add(arrow);
    document.getElementById('cs-turn-sel').addEventListener('change', function () {
      type = this.value; phase = 0; rebuild();
    });
    rebuild();
    return function () {
      phase += 0.018;
      if (phase > 2 * Math.PI) phase -= 2 * Math.PI;
      var p = curves[type](phase);
      var u = unit(dcurves[type](phase));
      dotG.position.set(p[0] - 1.35, p[1], 0);
      dotT.position.set(u[0] + 1.55, u[1], 0);
      arrow.position.copy(dotG.position);
      arrow.setDirection(new T.Vector3(u[0], u[1], 0));
      var acc = 0, prev = ang(unit(dcurves[type](0)));
      var samples = 80;
      var until = phase;
      for (var i = 1; i <= samples; i++) {
        var t = until * (i / samples);
        var a = ang(unit(dcurves[type](t)));
        var nxt = unwrap(prev, a);
        acc += nxt - prev;
        prev = nxt;
      }
      if (hud) {
        hud.innerHTML = 'running Delta theta / 2pi = ' + (acc / (2 * Math.PI)).toFixed(2) +
          '<br>closed tau = ' + api._tauClosed.toFixed(2);
      }
    };
  }
});
</script>

The surprise is dimensional. The turning number of a curve is an element of $\pi\sb{1}(S^1)=\mathbb{Z}$. For a surface in $\mathbb{R}^3$ the analogous invariant lives in $\pi\sb{2}(V\sb{3,2})$, and that group is $0$. One extra dimension is enough room for the obstruction to die.

---

# the gauss map is not the obstruction

<div class="cs-q">
<strong>Student.</strong> So what invariant do we actually compute? The model mentioned Jacobians staying positive, and also something called the hairy ball theorem of Smale.
</div>

<div class="cs-a">
<strong>Teacher.</strong> The hairy ball theorem is Poincaré--Brouwer: $S^2$ admits no continuous nowhere-zero tangent vector field. Smale proved a classification of immersions. Different theorem, different decade. The Jacobian-sign story is a confusion with local diffeomorphisms of $\mathbb{R}^n$. What we do compute is a <em>tangential</em> invariant, and its coarsest shadow is the Gauss map.
</div>

Given an immersion $f$,

$$\mathbf{n}_f=\frac{\mathbf{f}_u\times\mathbf{f}_v}{\lVert\mathbf{f}_u\times\mathbf{f}_v\rVert}:S^2\to S^2.$$

The **degree** of a map $g:S^n\to S^n$ is the integer that records signed coverings of the target. For the inclusion, $\mathbf{n}\sb{\iota}(p)=p$, so $\deg\mathbf{n}\sb{\iota}=1$. Degree is a regular-homotopy invariant (an integer moving continuously cannot jump). Gauss--Bonnet supplies the same integer without Smale: $\deg\mathbf{n}=\tfrac12\chi(S^2)=1$. Every immersion $S^2\looparrowright\mathbb{R}^3$ has Gauss degree $1$. The everted sphere does too. Degree does not forbid eversion.

The canvas is an ellipsoid, not a round sphere, so that $\mathbf{n}$ is not the identity. For

$$\mathbf{f}(\theta,\varphi)=(a\sin\theta\cos\varphi,\;b\sin\theta\sin\varphi,\;c\cos\theta)$$

the Gauss map is the normalization of $(x/a^2,\,y/b^2,\,z/c^2)$. It is still degree $1$: the yellow point on the right covers $S^2$ once as the gold point tours the ellipsoid.

<div id="cs-gauss" class="cs-stage" style="height:440px;">
  <div class="cs-hud cs-hud-tl">left: ellipsoid f<br>right: n_f(S^2)</div>
  <div class="cs-hud cs-hud-tr" id="cs-gauss-hud">n</div>
</div>
<p class="cs-cap">$\mathbf{n}\sb{f}=(\mathbf{f}\sb{\theta}\times\mathbf{f}\sb{\varphi})/\lVert\cdot\rVert$. Gold on the left is a point of the domain; cyan on the right is its unit normal. The image of $\mathbf{n}\sb{f}$ is the whole target sphere, once.</p>

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
      color: 0x6366f1, metalness: 0.25, roughness: 0.45, transparent: true, opacity: 0.72, side: T.DoubleSide
    })));
    left.add(new T.Mesh(ell, new T.MeshBasicMaterial({ color: 0xc4b5fd, wireframe: true, transparent: true, opacity: 0.12 })));
    var sph = new T.Mesh(new T.SphereGeometry(1, 32, 24), new T.MeshStandardMaterial({
      color: 0x1e293b, metalness: 0.2, roughness: 0.6, transparent: true, opacity: 0.35, side: T.DoubleSide
    }));
    var right = new T.Group();
    right.position.x = 1.7;
    right.add(sph);
    right.add(new T.Mesh(sph.geometry, new T.MeshBasicMaterial({ color: 0x64748b, wireframe: true, transparent: true, opacity: 0.2 })));
    api.group.add(left);
    api.group.add(right);
    var pL = new T.Mesh(new T.SphereGeometry(0.05, 12, 12), new T.MeshStandardMaterial({ color: 0xfbbf24, emissive: 0xf59e0b, emissiveIntensity: 0.35 }));
    var pR = new T.Mesh(new T.SphereGeometry(0.06, 12, 12), new T.MeshStandardMaterial({ color: 0x22d3ee, emissive: 0x06b6d4, emissiveIntensity: 0.35 }));
    left.add(pL); right.add(pR);
    var arr = new T.ArrowHelper(new T.Vector3(1, 0, 0), new T.Vector3(), 0.55, 0x22d3ee, 0.1, 0.07);
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

The finer invariant records the whole **2-frame** $(\mathbf{f}\sb{u},\mathbf{f}\sb{v})$, not just its normal. That pair lives in the Stiefel manifold

$$V_{3,2}=\bigl\{(v_1,v_2)\in\mathbb{R}^3\times\mathbb{R}^3:v_1,v_2\text{ linearly independent}\bigr\}.$$

Normalizing, $V\sb{3,2}\simeq SO(3)$: a positively oriented orthonormal 2-frame completes uniquely to a rotation matrix. Each immersion $f$ gives a tangential map $T\sb{f}:S^2\to V\sb{3,2}$. Smale's invariant $\Omega(f,g)\in\pi\sb{2}(V\sb{3,2})$ is the homotopy class of the sphere you get by gluing $T\sb{f}$ to $T\sb{g}$ along a disk. Two immersions are regularly homotopic if and only if $\Omega(f,g)=0$.

---

# why the obstruction vanishes

<div class="cs-q">
<strong>Student.</strong> Prove the existence. Use Smale's 1958 paper. I can understand it.
</div>

<div class="cs-a">
<strong>Teacher.</strong> The paper is <em>A classification of immersions of the two-sphere</em>, Trans. Amer. Math. Soc. <strong>90</strong> (1958). It does not use contact structures, Reeb foliations, or a "magic formula" of Thurston. Those are neighbouring subjects that the model dragged in. The argument is: regular homotopy classes of immersions $S^2\to\mathbb{R}^n$ are in bijection with $\pi\sb{2}(V\sb{n,2})$, and for $n=3$ that group is zero.
</div>

The computation, written so each symbol is a space you can name:

1. $V\sb{3,2}\simeq SO(3)$. An oriented orthonormal 2-frame in $\mathbb{R}^3$ is the first two columns of a rotation.
2. $SO(3)\simeq\mathbb{RP}^3$. Unit quaternions are $S^3$. The map $q\mapsto$ (the rotation $v\mapsto qvq^{-1}$) identifies $q\sim -q$, so $SO(3)\simeq S^3/\{\pm 1\}=\mathbb{RP}^3$. This is the same double cover as the plate trick: a $2\pi$ rotation is a nontrivial loop, a $4\pi$ rotation is contractible.
3. The covering $S^3\to\mathbb{RP}^3$ has discrete fibre $S^0=\{\pm 1\}$. The long exact sequence of a fibration collapses, in degree $2$, to $\pi\sb{2}(\mathbb{RP}^3)\cong\pi\sb{2}(S^3)$.
4. $\pi\sb{k}(S^n)=0$ for $k<n$. In particular $\pi\sb{2}(S^3)=0$: a 2-sphere in a 3-sphere has room to shrink. (The same reason $\pi\sb{1}(S^2)=0$.)

Therefore

$$\pi_2(V_{3,2})\cong\pi_2(SO(3))\cong\pi_2(\mathbb{RP}^3)\cong\pi_2(S^3)=0.$$

So $\Omega(f,g)=0$ for every pair. In particular $\iota$ and $\alpha$ lie in the same path-component of $\operatorname{Imm}(S^2,\mathbb{R}^3)$.

```mermaid
%%{init: {"theme":"dark","themeVariables":{"primaryTextColor":"#e2e8f0","secondaryTextColor":"#e2e8f0","tertiaryTextColor":"#e2e8f0","lineColor":"#94a3b8","primaryColor":"#1e293b","primaryBorderColor":"#64748b","secondaryColor":"#334155","tertiaryColor":"#0f172a","fontFamily":"ui-monospace, SFMono-Regular, Menlo, monospace","fontSize":"16px"}}}%%
flowchart LR
  Imm["Imm(S^2, R^3)"] --> Tf["T_f : S^2 to V_3,2"]
  Tf --> Pi["pi_2(V_3,2)"]
  Pi --> SO["pi_2(SO(3))"]
  SO --> RP["pi_2(RP^3)"]
  RP --> Z["pi_2(S^3) = 0"]
```

This is an existence proof. It produces no picture. For $n=4$ the same machine gives $\pi\sb{2}(V\sb{4,2})\cong\mathbb{Z}$, so immersions $S^2\to\mathbb{R}^4$ have infinitely many regular homotopy classes, detected by the Euler class of the normal bundle (twice the algebraic self-intersection). The vanishing is special to codimension one in $\mathbb{R}^3$.

A **fiber bundle** $E\to B$ with fibre $F$ is a space that is locally $B\times F$ but perhaps twisted globally (a cylinder versus a Möbius strip). Smale's technical work is to show that "immersions of a disk with given boundary data" is a fibration over the space of that boundary data, and that the fibre is weakly homotopy equivalent to a loop space of $V\sb{n,2}$. That is why $\pi\sb{0}$ of the fibre --- path-components of immersions with fixed boundary --- is $\pi\sb{2}(V\sb{n,2})$. You do not need the tower to believe the computation above; you need it to believe that the computation classifies immersions.

---

# slack that does not crease

<div class="cs-q">
<strong>Student.</strong> Explain Thurston's magic formula, the one that proves eversion.
</div>

<div class="cs-a">
<strong>Teacher.</strong> There is no such formula, and Thurston did not prove existence --- Smale did. What Thurston gave, in the 1990s, is a <em>construction</em>: corrugate the surface so that it has slack, pass the ripples through one another, then iron the ripples out. The model invented a condition on $\det J(g\sb{t})>0$. The actual local move is a normal oscillation.
</div>

$$
\mathbf{f}_\varepsilon(\theta,\varphi)=\bigl(1+\varepsilon\sin\theta\sin(k\varphi)\bigr)\,\mathbf{r}(\theta,\varphi).
$$

The amplitude $\varepsilon\sin\theta$ dies at the poles, so the chart singularities of $\mathbf{r}$ stay chart singularities. For $\lvert\varepsilon\rvert<1$ the radial factor never vanishes, and a computation of $\mathbf{f}\sb{\theta}\times\mathbf{f}\sb{\varphi}$ shows the cross product stays a positive multiple of $\mathbf{r}$ plus a controlled ripple --- still nonzero. This is an immersion for every $\varepsilon$ in that range. It is **not** an eversion. It is the ingredient that makes an eversion possible: extra wiggles so that later, when you try to pass sheets through each other, you have room.

The old post implemented "corrugation" and then multiplied $z$ by a factor passing through zero. That second step is $F\sb{s}$ again. Here there is no second step. The heatmap is $\lVert\mathbf{f}\sb{\theta}\times\mathbf{f}\sb{\varphi}\rVert$; it should not go red.

<div id="cs-corr" class="cs-stage" style="height:460px;">
  <div class="cs-hud cs-hud-tl" id="cs-corr-hud">corrugation</div>
  <div class="cs-hud cs-hud-tr"><span style="color:#818cf8;">outside</span> <span style="color:#f97316;">inside</span></div>
  <div class="cs-ctrl">
    <label>eps <input type="range" id="cs-eps" min="0" max="70" value="0"> <span id="cs-eps-v">0.00</span></label>
    <label>k <input type="range" id="cs-k" min="2" max="10" value="4"> <span id="cs-k-v">4</span></label>
  </div>
</div>
<p class="cs-cap">$\mathbf{f}\sb{\varepsilon}=(1+\varepsilon\sin\theta\sin(k\varphi))\,\hat{\mathbf{r}}$. Indigo is the outside, orange the inside. Increase $\varepsilon$: petals, no fold. This is slack, not eversion.</p>

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
      color: 0x6366f1, metalness: 0.28, roughness: 0.48,
      side: T.FrontSide, transparent: true, opacity: 0.88
    });
    var back = new T.MeshStandardMaterial({
      color: 0xf97316, metalness: 0.28, roughness: 0.48,
      side: T.BackSide, transparent: true, opacity: 0.88
    });
    api.group.add(new T.Mesh(geo, front));
    api.group.add(new T.Mesh(geo, back));
    api.group.add(new T.Mesh(geo, new T.MeshBasicMaterial({
      color: 0xa5b4fc, wireframe: true, transparent: true, opacity: 0.1, side: T.DoubleSide
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
        hud.innerHTML = 'rho = 1 + eps sin(theta) sin(k phi)<br>min rho = ' + minR.toFixed(3) +
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

Existence is not a picture. Morin gave the first explicit halfway model --- a four-lobed immersion with a single quadruple point --- and later Apéry wrote algebraic formulae. A family you can type into a shader is due to Adam and Witold Bednorz, *Analytic sphere eversion using ruled surfaces*, arXiv:1711.10466. They evert a cylinder (the sphere minus two polar caps) by a ruled surface, then close the caps by a damped inversion. We draw only the cylinder, so that every vertex is the displayed equation.

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
  <div class="cs-hud cs-hud-tr"><span style="color:#818cf8;">front</span> <span style="color:#f97316;">back</span></div>
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
<p class="cs-cap">Equation (4) of Bednorz--Bednorz, $q=2/3$, $p=1-\lvert qt\rvert$, $h\in[-2.3,2.3]$. The poles are not closed; what you see is the formula, not a screenshot of <em>Outside In</em>. At $t=0$, $n=2$ you are looking at the ruled Morin halfway. At $n=3$, $t=0$ you are looking at a ruled Boy surface, an immersion of $\mathbb{RP}^2$.</p>

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
      color: 0x6366f1, metalness: 0.32, roughness: 0.42,
      side: T.FrontSide, transparent: true, opacity: 0.86
    })));
    api.group.add(new T.Mesh(geo, new T.MeshStandardMaterial({
      color: 0xf97316, metalness: 0.32, roughness: 0.42,
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

# an integral that must cross zero, and one that must not

<div class="cs-q">
<strong>Student.</strong> How do I know I am halfway?
</div>

<div class="cs-a">
<strong>Teacher.</strong> Track the average alignment of normals. For a path $f\sb{s}$ with unit normal $\mathbf{n}\sb{s}$,
$$S(s)=\int_{S^2}\mathbf{n}_0\cdot\mathbf{n}_s\,dA.$$
If $f\sb{s}$ is a genuine eversion, $S(0)=4\pi$ and $S(1)=-4\pi$, so the intermediate-value theorem --- freshman calculus, on a continuous function of one real variable --- produces an $s^*$ with $S(s^*)=0$. That is a reasonable definition of halfway. The Morin surface is a geometric refinement of that idea (four-fold symmetry, one quadruple point), not just the vanishing of an integral.
</div>

For the illegal homotopy $F\sb{s}$ one can compute the integrand in closed form, $\theta\in(0,\pi)$:

$$
\mathbf{n}_0\cdot\mathbf{n}_s=\frac{(1-2s)\sin^2\theta+\cos^2\theta}{\sqrt{(1-2s)^2\sin^2\theta+\cos^2\theta}}.
$$

Then $S(s)=2\pi\int\sb{0}^\pi(\mathbf{n}\sb{0}\cdot\mathbf{n}\sb{s})\sin\theta\,d\theta$. At $s=0$ this is $4\pi$. At $s=1$ it is $-4\pi/3$, not $-4\pi$: $F\sb{1}$ is equatorial reflection, not $\alpha$. At $s=\tfrac12$ the formula for $\mathbf{n}\sb{s}$ fails on the equator, because $F\sb{s}$ is not an immersion. The plot is that integral, by a trapezoid rule on the displayed integrand.

<div id="cs-sync-wrap" style="width:100%; margin:1.4em 0 0.4em; border-radius:8px; overflow:hidden; background:#0f172a; position:relative;">
  <canvas id="cs-sync" style="width:100%; height:280px; display:block;"></canvas>
  <div class="cs-ctrl" style="position:static; padding:8px 10px 12px;">
    <label>s <input type="range" id="cs-ss" min="0" max="100" value="0"> <span id="cs-ss-v">0.00</span></label>
  </div>
</div>
<p class="cs-cap">Gold: $S(s)/(4\pi)$ for the crease homotopy $F\sb{s}$. The red line is $s=1/2$, where the integrand is not the Gauss map of an immersion. A true eversion would run from $+1$ to $-1$ without that puncture.</p>

<script>
(function () {
  var canvas = document.getElementById('cs-sync');
  if (!canvas) return;
  function integrand(s, th) {
    var sth = Math.sin(th), cth = Math.cos(th);
    var den = Math.sqrt((1 - 2 * s) * (1 - 2 * s) * sth * sth + cth * cth);
    if (den < 1e-10) return 0;
    return ((1 - 2 * s) * sth * sth + cth * cth) / den;
  }
  function S(s) {
    var N = 240, acc = 0, i, th, w;
    for (i = 0; i <= N; i++) {
      th = Math.PI * i / N;
      w = (i === 0 || i === N) ? 0.5 : 1;
      acc += w * integrand(s, th) * Math.sin(th);
    }
    return 2 * Math.PI * acc * (Math.PI / N);
  }
  var cache = [];
  for (var k = 0; k <= 100; k++) cache[k] = S(k / 100) / (4 * Math.PI);
  function draw(s) {
    var w = canvas.clientWidth || 640;
    var h = 280;
    canvas.width = w * 2;
    canvas.height = h * 2;
    var ctx = canvas.getContext('2d');
    ctx.scale(2, 2);
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, w, h);
    var padL = 48, padR = 16, padT = 18, padB = 28;
    function X(u) { return padL + u * (w - padL - padR); }
    function Y(v) { return padT + (1.15 - v) / 2.35 * (h - padT - padB); }
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(1), Y(0));
    ctx.moveTo(X(0), Y(1.1)); ctx.lineTo(X(0), Y(-1.1));
    ctx.stroke();
    ctx.setLineDash([5, 5]);
    ctx.strokeStyle = '#ef4444';
    ctx.beginPath();
    ctx.moveTo(X(0.5), Y(1.1)); ctx.lineTo(X(0.5), Y(-1.1));
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (var i = 0; i <= 100; i++) {
      var x = X(i / 100), y = Y(cache[i]);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    var idx = Math.round(s * 100);
    ctx.fillStyle = '#22d3ee';
    ctx.beginPath();
    ctx.arc(X(s), Y(cache[idx]), 4.5, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#94a3b8';
    ctx.font = '12px ui-monospace, monospace';
    ctx.fillText('s', w - 22, Y(0) + 16);
    ctx.fillText('S / 4pi', 6, 16);
    ctx.fillText('+1', 8, Y(1) + 4);
    ctx.fillText('0', 14, Y(0) + 4);
    ctx.fillText(cache[idx].toFixed(2) + '   at s = ' + s.toFixed(2), X(0.58), 28);
  }
  var sl = document.getElementById('cs-ss');
  function on() {
    var s = parseFloat(sl.value) / 100;
    document.getElementById('cs-ss-v').textContent = s.toFixed(2);
    draw(s);
  }
  sl.addEventListener('input', on);
  window.addEventListener('resize', on);
  on();
})();
</script>

---

# what the model got wrong

The May transcript is still worth reading. It is a record of the questions one actually asks. Here is the answer key.

<table class="cs-err">
  <thead>
    <tr><th>Claim in the Phi-3 notes</th><th>Fact</th></tr>
  </thead>
  <tbody>
    <tr><td>$H=(1-t)f\sb{0}+tf\sb{1}$ is a regular homotopy.</td><td>It is a homotopy of maps. Rank drops. See $F\sb{s}$.</td></tr>
    <tr><td>$\partial\sb{\theta}(1,0,0)=\mathbf{0}$.</td><td>Differentiate the chart, not the point. $\mathbf{r}\sb{\theta}(1,0,0)=(0,0,-1)$.</td></tr>
    <tr><td>Jacobian of $f:\mathbb{R}^n\to\mathbb{R}^m$ is $n\times m$.</td><td>$m\times n$. For immersions $S^2\to\mathbb{R}^3$ it is $3\times 2$; there is no determinant.</td></tr>
    <tr><td>$\det J=-1$ means a saddle.</td><td>It means orientation reversal. A saddle is a critical point, which requires $\det J=0$ (in the square case).</td></tr>
    <tr><td>$S^2\times[0,1]$ is a ball.</td><td>It is a spherical shell. The ball is $D^3$.</td></tr>
    <tr><td>Smale's hairy ball theorem.</td><td>Poincaré--Brouwer. Smale classified immersions of $S^2$.</td></tr>
    <tr><td>Thurston's magic formula ($J(g\sb{t})>0$) proves eversion.</td><td>Smale proved existence. Thurston gave corrugations. Bednorz wrote a ruled family.</td></tr>
    <tr><td>Eversion forbids self-intersection and uses contact / Reeb foliations.</td><td>Self-intersection is the point. Contact geometry is a different chapter.</td></tr>
    <tr><td>The complex exponential at $(0,\pi/2)$ has $\det J=-1$.</td><td>$\det J=e^{2x}=1$ there. The map is a local diffeomorphism everywhere.</td></tr>
  </tbody>
</table>

---

# the arc

Calculus gives the language: charts, $J\sb{f}$, $\mathbf{f}\sb{u}\times\mathbf{f}\sb{v}\neq\mathbf{0}$. Function spaces give the question: is $\operatorname{Imm}(S^2,\mathbb{R}^3)$ path-connected? Circles in the plane say no, by $\pi\sb{1}(S^1)=\mathbb{Z}$. One dimension up, the same instinct produces $\pi\sb{2}(V\sb{3,2})$, and that group is zero. Smale's theorem is that computation plus a fibration argument. Morin, Thurston, and Bednorz are what you do if you want to *see* a path.

The first post asked. The second post answered, and then drew the forbidden crease. This one circles the sphere until the picture and the equation are the same object.

**Further reading.** S. Smale, *A classification of immersions of the two-sphere*, Trans. Amer. Math. Soc. 90 (1958). A. Bednorz and W. Bednorz, [arXiv:1711.10466](https://arxiv.org/abs/1711.10466). S. Levy, D. Maxwell, T. Munzner, *Outside In*, Geometry Center, 1994. Guillemin--Pollack, *Differential Topology*. The two parents of this page: [Phi-3 notes](/blog/2024/05/22/sphere-eversion-phi3-notes-I), [The Eversion of the Sphere](/blog/2024/09/27/the-eversion-of-the-sphere).
