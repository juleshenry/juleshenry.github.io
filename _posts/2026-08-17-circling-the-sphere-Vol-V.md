---
layout: post
title: "Back-of-the-Envelope: Sphere Eversion, Vol. V: Frames and Smale's Theorem"
date: 2026-08-17 12:04:00
description: "Smale's existence proof for sphere eversion: tangent frames, fibrations, SO(3) as ℝP³ via quaternions and the belt trick, and why the obstruction vanishes."
categories: differential topology
mathjax: true
---

*Sphere Eversion:* [I](/blog/2026/08/17/circling-the-sphere) · [II](/blog/2026/08/17/circling-the-sphere-Vol-II) · [III](/blog/2026/08/17/circling-the-sphere-Vol-III) · [IV](/blog/2026/08/17/circling-the-sphere-Vol-IV) · **V** · [VI](/blog/2026/08/17/circling-the-sphere-Vol-VI)

{% include eversion-kit.html %}

*The existence proof. Record the whole derivative, find the space it lives in, and show that space has no room for an obstruction.*

[Vol. IV](/blog/2026/08/17/circling-the-sphere-Vol-IV) ended with a question. For plane curves the obstruction was the direction of the whole derivative $\gamma'$, counted in $\pi&#95;{1}(S^1)$. The Gauss map of a surface records only its normal, and its degree is always $1$. So record the whole derivative of the surface. This volume builds the three tools that make that computable: fibrations, the rotation group, and the long exact sequence. Then it runs Smale's argument.

<div class="cs-toc">
<strong>Contents</strong>
<ol>
  <li><a href="#the-whole-derivative">The whole derivative</a></li>
  <li><a href="#fibre-bundles-and-fibrations">Fibre bundles and fibrations</a></li>
  <li><a href="#rotations-quaternions-and-the-belt">Rotations, quaternions, and the belt</a></li>
  <li><a href="#why-the-obstruction-vanishes">Why the obstruction vanishes</a></li>
  <li><a href="#where-this-goes">Where this goes</a></li>
</ol>
</div>

---

# The whole derivative
{: #the-whole-derivative}
<div class="cs-q">
The Gauss map obstructed nothing. It is instructive to ask what could.
</div>

<div class="cs-a">
Look at the pair of tangent vectors itself. At each point an immersion $f$ hands you two linearly independent vectors $(\mathbf{f}&#95;{u},\mathbf{f}&#95;{v})$. The space of all such pairs is where the invariant lives.
</div>

<div class="ev-def"><strong>Definition (Stiefel manifold).</strong> $V&#95;{n,k}$ is the space of $k$-tuples of linearly independent vectors in $\mathbb{R}^n$.</div>

The pair $(\mathbf{f}&#95;{u},\mathbf{f}&#95;{v})$ lies in $V&#95;{3,2}$. One dimension down, the velocity $\gamma'$ of an immersed plane curve lies in $V&#95;{2,1}=\mathbb{R}^2\setminus\lbrace 0\rbrace$, which Vol. II's homotopy $(1-s)v+s\,v/\lVert v\rVert$ squeezes onto the unit circle $S^1$, and the class of $\gamma'$ in $\pi&#95;{1}(V&#95;{2,1})=\mathbb{Z}$ is precisely the turning number. Whitney–Graustein *is* the one-dimensional case of the theorem this volume proves.

There is a catch. A frame needs coordinates $(u,v)$, and the sphere has no global coordinates with independent partials: a nowhere-zero field $\partial&#95;{u}$ on all of $S^2$ would be a hairy ball combed flat, and Poincaré–Brouwer says that is impossible. So we cannot simply map the whole sphere to $V&#95;{3,2}$. Smale's invariant works around this by using a disk, where coordinates do exist. We will get there; first, the tools.

---

# Fibre bundles and fibrations
{: #fibre-bundles-and-fibrations}
<div class="ev-def"><strong>Definition (fibre bundle).</strong> A map $\pi:E\to B$ such that each point of $B$ has a neighbourhood $U$ with $\pi^{-1}(U)\cong U\times F$, by a homeomorphism that sends the part over each point $u$ to $\lbrace u\rbrace\times F$. $F$ is the <em>fibre</em>.</div>

Locally a product, globally perhaps twisted. The cylinder $S^1\times[0,1]$ and the Möbius band are both bundles over the circle with fibre an interval; only the first is a product. Three examples:

- **The covering $\mathbb{R}\to S^1$** from [Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II). Fibre $\mathbb{Z}$, discrete.
- **The quaternion double cover $S^3\to SO(3)$**, below. Fibre $\lbrace\pm1\rbrace$, discrete.
- **$SO(3)\to S^2$, $R\mapsto R\,e&#95;{3}$** (where does the rotation send the north pole). Fibre: the rotations fixing $e&#95;{3}$, which are the rotations of the $xy$-plane, a circle's worth called $SO(2)$. ($SO(3)$, the rotation group, is defined in the next section.)

Bundles have the **homotopy lifting property** (Vol. II proved it for $\mathbb{R}\to S^1$ by chopping the square into small pieces; the general proof uses the same idea). A map with that property is called a **fibration**, and every fibration comes with a machine for computing homotopy groups:

<div class="ev-def"><strong>Theorem (long exact sequence of a fibration).</strong> For a fibration $F\to E\to B$ there is an exact sequence
$$\cdots\to\pi_n(F)\to\pi_n(E)\to\pi_n(B)\to\pi_{n-1}(F)\to\pi_{n-1}(E)\to\cdots\to\pi_0(E)\to\pi_0(B).$$
</div>

The unlabeled arrows are the obvious ones: $F\to E$ is inclusion and $E\to B$ is the bundle map, and since a map sends spheres to spheres it induces a map of homotopy groups. This theorem is not proved here; every case of it that the series uses is proved directly below. **Exact** means: at each spot, the things killed by the outgoing arrow are exactly the things hit by the incoming one. The map $\pi&#95;{n}(B)\to\pi&#95;{n-1}(F)$ is the interesting one: view an $n$-sphere in $B$ as an $n$-disk with its boundary crushed to the base point, lift the disk to $E$ (homotopy lifting), and look at where its boundary lands: an $(n-1)$-sphere in the fibre over the base point.

The only consequence we need: in a stretch $0\to X\to Y\to 0$ of the sequence, the arrow $X\to Y$ is an isomorphism (at the $\pi&#95;{0}$ end a one-point set $\ast$ plays the role of $0$). Try it on Vol. II's covering. With $E=\mathbb{R}$ (contractible, all $\pi&#95;{n}=0$) and $F=\mathbb{Z}$:

$$0=\pi_1(\mathbb{R})\to\pi_1(S^1)\to\pi_0(\mathbb{Z})\to\pi_0(\mathbb{R})=\ast,$$

and $\pi&#95;{1}(S^1)\cong\pi&#95;{0}(\mathbb{Z})=\mathbb{Z}$. That is the lifting argument of Vol. II, compressed into one line.

---

# Rotations, quaternions, and the belt
{: #rotations-quaternions-and-the-belt}
**$V&#95;{3,2}$ is the rotation group, up to homotopy.** The **rotation group** $SO(3)$ is the set of $3\times 3$ real matrices $R$ with $R^{\mathsf T}R=I$ and $\det R=1$: the linear maps that preserve lengths and orientation. Its columns form an orthonormal basis $(v&#95;{1},v&#95;{2},v&#95;{3})$ with $v&#95;{3}=v&#95;{1}\times v&#95;{2}$. Gram–Schmidt turns a pair of independent vectors into an orthonormal pair, continuously, and the straight-line path from each pair to its Gram–Schmidt output stays independent. So $V&#95;{3,2}$ deformation-retracts onto orthonormal pairs. An orthonormal pair $(v&#95;{1},v&#95;{2})$ extends uniquely to a rotation matrix with columns $(v&#95;{1},\,v&#95;{2},\,v&#95;{1}\times v&#95;{2})$. So

$$V_{3,2}\simeq SO(3).$$

<div class="ev-def"><strong>Definition (deformation retraction).</strong> A <em>deformation retraction</em> of $X$ onto a subspace $A$ is a homotopy from the identity map of $X$ to a map into $A$, during which the points of $A$ stay put. Then $X$ and $A$ are <em>homotopy equivalent</em>, written $X\simeq A$. Every sphere in $X$, and every homotopy of spheres, can be pushed into $A$ by it, so $\pi&#95;{k}(X)\cong\pi&#95;{k}(A)$ for every $k$. Vol. II's homotopy $(1-s)v+s\,v/\lVert v\rVert$ is a deformation retraction of $\mathbb{R}^2\setminus\lbrace 0\rbrace$ onto $S^1$.</div>

**$SO(3)$ is a sphere with antipodes glued.** Quaternions are expressions $a+bi+cj+dk$ with real coefficients, multiplied like polynomials subject to $i^2=j^2=k^2=ijk=-1$. The length of a quaternion is the length of $(a,b,c,d)$ in $\mathbb{R}^4$, and lengths multiply. A unit quaternion $q=\cos\tfrac\theta2+\sin\tfrac\theta2\,(a\,i+b\,j+c\,k)$ acts on vectors $v\in\mathbb{R}^3$, written as pure quaternions $xi+yj+zk$, by $v\mapsto qvq^{-1}$, where for a unit quaternion $q^{-1}$ is $q$ with the signs of its $i$, $j$, $k$ parts flipped. That map preserves length and fixes the axis $(a,b,c)$, and a direct computation shows it is the rotation by angle $\theta$ about that axis. Unit quaternions form $S^3\subset\mathbb{R}^4$. Every rotation turns space by some angle about some axis (a $3\times 3$ rotation matrix always has eigenvalue $1$), so every rotation arises, from exactly two quaternions, $q$ and $-q$. So the map $S^3\to SO(3)$ is a two-sheeted covering, and

$$SO(3)\cong S^3/\lbrace\pm1\rbrace=\mathbb{RP}^3.$$

Here $S^3/\lbrace\pm1\rbrace$ is the sphere with each point $q$ glued to its antipode $-q$, called real projective space $\mathbb{RP}^3$: a point of it is a pair $\lbrace q,-q\rbrace$, or equivalently a line through the origin of $\mathbb{R}^4$. The map from pairs to rotations is a continuous bijection from a compact space, so its inverse is continuous too, by the fact from [Vol. III](/blog/2026/08/17/circling-the-sphere-Vol-III#immersions-and-the-matrix-that-must-not-drop-rank), and $\cong$ here is a homeomorphism.

The long exact sequence of this covering, with fibre $\lbrace\pm1\rbrace$ and $\pi&#95;{1}(S^3)=0$, gives $\pi&#95;{1}(SO(3))\cong\mathbb{Z}/2$, the group with two elements in which the non-identity element times itself is the identity. Directly: a loop of rotations lifts to a path in $S^3$ that either closes up or ends at $-1$ times its start. Homotopies lift, and the far end moves within the discrete fibre, so it cannot move: which case occurs is an invariant. A loop whose lift closes up is trivial, because the closed lift shrinks in $S^3$ ($\pi&#95;{1}(S^3)=0$) and the shrinking projects down. So there are exactly two classes. Rotating by $2\pi$ about a fixed axis is the nontrivial loop (its lift $\cos\tfrac\theta2+\sin\tfrac\theta2\,k$ runs from $1$ to $-1$ as $\theta$ goes from $0$ to $2\pi$); rotating by $4\pi$ is the trivial one. You can feel this with a belt, or a plate held flat on your palm (Dirac's belt trick, the plate trick):

<div id="ev-belt" class="cs-stage" style="height:470px;">
  <div class="cs-hud cs-hud-tl" id="ev-belt-hud"></div>
  <div class="cs-hud cs-hud-tr"><span style="color:#6fa8f0;">belt, front</span><br><span style="color:#f08a5d;">belt, back</span></div>
  <div class="cs-ctrl">
    <label>loop <select id="ev-belt-mode"><option value="4">4π (720°)</option><option value="2">2π (360°)</option></select></label>
    <label>λ <input type="range" id="ev-belt-l" min="0" max="1000" value="0" style="width:34%"> <span id="ev-belt-lv">0.00</span></label>
    <label><input type="checkbox" id="ev-belt-play" checked> play</label>
  </div>
</div>
<p class="cs-cap">The belt is a path of rotations: the frame at distance $u$ along it is $p&#95;{\lambda}(u)\in SO(3)$, drawn as the direction the belt faces. The wall end is fixed at the identity. At $\lambda=0$ the belt carries a full $4\pi$ (or $2\pi$) twist. Slide $\lambda$: for $4\pi$ the explicit homotopy to the constant loop $p&#95;{\lambda}(u)=q&#95;{\lambda}(0)^{-1}q&#95;{\lambda}(u)$ untwists it completely with the plate held still. For $2\pi$ the same trick forces the plate to turn, by up to $180^\circ$. No trick can avoid that.</p>
<script>
CS.mount({
  id: 'ev-belt',
  height: 470,
  cam: [0, 1.4, 6.1],
  rotX: 0.35,
  rotY: -0.45,
  noSpin: true,
  setup: function (api) {
    var T = api.THREE, NU = 180, L = 2.3, HW = 0.32;
    // quaternions as [w, x, y, z]
    function mul(a, b) { return [a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3], a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2], a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1], a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0]]; }
    function conj(a) { return [a[0], -a[1], -a[2], -a[3]]; }
    // q_lambda(u) = cos(phi) j + sin(phi) (cos(k u) + i sin(k u)), phi = (1 - lambda) pi / 2, k = 2pi (4pi loop) or pi (2pi loop)
    function q(u, lam, k) { var ph = (1 - lam) * Math.PI / 2, s = Math.sin(ph); return [s * Math.cos(k * u), s * Math.sin(k * u), Math.cos(ph), 0]; }
    function p(u, lam, k) { return mul(conj(q(0, lam, k)), q(u, lam, k)); }
    function toT(a) { return new T.Quaternion(a[1], a[2], a[3], a[0]); }
    var pos = new Float32Array((NU + 1) * 2 * 3), idx = [];
    for (var i = 0; i < NU; i++) { var a = 2 * i; idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); }
    var geo = new T.BufferGeometry();
    geo.setAttribute('position', new T.BufferAttribute(pos, 3));
    geo.setIndex(idx);
    api.group.add(new T.Mesh(geo, new T.MeshStandardMaterial({ color: 0x3987e5, side: T.FrontSide, roughness: 0.5, metalness: 0.1 })));
    api.group.add(new T.Mesh(geo, new T.MeshStandardMaterial({ color: 0xd95926, side: T.BackSide, roughness: 0.5, metalness: 0.1 })));
    var wall = new T.Mesh(new T.BoxGeometry(0.08, 1.4, 1.4), new T.MeshStandardMaterial({ color: 0x5a5a5a, roughness: 0.8 }));
    wall.position.set(-L - 0.04, 0, 0); api.group.add(wall);
    var plate = new T.Group();
    plate.add(new T.Mesh(new T.BoxGeometry(0.08, 0.95, 0.95), new T.MeshStandardMaterial({ color: 0xd0d0d0, roughness: 0.4 })));
    var tab = new T.Mesh(new T.BoxGeometry(0.1, 0.18, 0.5), new T.MeshStandardMaterial({ color: 0xc98500 }));
    tab.position.set(0.02, 0.5, 0); plate.add(tab);
    plate.position.set(L + 0.04, 0, 0); api.group.add(plate);
    var hud = document.getElementById('ev-belt-hud'), sl = document.getElementById('ev-belt-l'), md = document.getElementById('ev-belt-mode'), pl = document.getElementById('ev-belt-play');
    var lam = 0, dir = 1, hold = 60;
    function build() {
      var k = md.value === '4' ? 2 * Math.PI : Math.PI;
      for (var i = 0; i <= NU; i++) {
        var u = i / NU, w = new T.Vector3(0, 0, HW).applyQuaternion(toT(p(u, lam, k))), x = -L + 2 * L * u;
        pos[6 * i] = x + w.x; pos[6 * i + 1] = w.y; pos[6 * i + 2] = w.z;
        pos[6 * i + 3] = x - w.x; pos[6 * i + 4] = -w.y; pos[6 * i + 5] = -w.z;
      }
      geo.attributes.position.needsUpdate = true;
      geo.computeVertexNormals();
      var end = p(1, lam, k);
      plate.quaternion.copy(toT(end));
      var ang = 2 * Math.acos(Math.min(1, Math.abs(end[0]))) * 180 / Math.PI;
      sl.value = Math.round(lam * 1000);
      document.getElementById('ev-belt-lv').textContent = lam.toFixed(2);
      if (hud) hud.innerHTML = md.value === '4'
        ? 'loop of rotations by 4πu about the belt<br>plate turned by ' + ang.toFixed(0) + '°  (held still ✓)<br>' + (lam > 0.995 ? 'untwisted: the 4π loop is null-homotopic' : 'lift to S³ closes up: q(1) = q(0)')
        : 'loop of rotations by 2πu about the belt<br>plate turned by ' + ang.toFixed(0) + '°' + (ang > 0.5 ? '  ✗ the end moved' : '') + '<br>' + (lam < 0.005 ? 'lift to S³ ends at −q(0): not closed' : lam > 0.995 ? 'constant loop, but only by turning the plate on the way' : 'this family is not a homotopy of loops');
    }
    sl.addEventListener('input', function () { pl.checked = false; lam = sl.value / 1000; build(); });
    md.addEventListener('change', function () { lam = 0; dir = 1; hold = 60; build(); });
    build();
    return function () {
      if (!pl.checked) return;
      if (hold > 0) { hold--; return; }
      lam += dir * 0.004;
      if (lam >= 1) { lam = 1; dir = -1; hold = 70; }
      if (lam <= 0) { lam = 0; dir = 1; hold = 70; }
      build();
    };
  }
});
</script>

The same sequence one step higher is the one we need. $\pi&#95;{2}$ of the fibre $\lbrace\pm1\rbrace$ is $0$ and $\pi&#95;{1}$ of it is $0$ too (a map from a sphere into a discrete set is constant), so

$$0\to\pi_2(S^3)\xrightarrow{\ \cong\ }\pi_2(SO(3))\to 0.$$

The same conclusion comes straight from the lifting of [Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II#the-circle), with no exact sequence. Take a map $g:S^2\to SO(3)$ and lift it to $S^3$ one point at a time: join $x$ to the base point by a path in $S^2$, lift the image path, and let $\tilde g(x)$ be where the lift ends. Another path gives the same endpoint. Two paths with the same ends differ by a loop, the loop shrinks in $S^2$ because $\pi&#95;{1}(S^2)=0$, and the shrinking lifts; its far end moves within the discrete fibre over $g(x)$, so it cannot move at all. So $g$ is $\tilde g:S^2\to S^3$ followed by the covering. Since $\pi&#95;{2}(S^3)=0$, $\tilde g$ shrinks to a point in $S^3$, and projecting the shrinking down shrinks $g$. Every map $S^2\to SO(3)$ is homotopic to a constant.

---

# Why the obstruction vanishes
{: #why-the-obstruction-vanishes}
<div class="cs-q">
It is instructive to prove that an eversion exists by following Smale's 1959 paper, details included.
</div>

<div class="cs-a">
The paper is <a href="https://doi.org/10.1090/S0002-9947-1959-0104227-9"><em>A classification of immersions of the two-sphere</em></a>, Trans. Amer. Math. Soc. <strong>90</strong> (1959). It does not use contact structures, Reeb foliations, or a "magic formula" of Thurston. Those are neighbouring subjects that tend to get dragged in. The argument is: regular homotopy classes of immersions $S^2\to\mathbb{R}^n$ are in bijection with $\pi&#95;{2}(V&#95;{n,2})$, and for $n=3$ that group is zero.
</div>

First the invariant, stated so that it avoids the hairy-ball catch. Take two immersions $f,g:S^2\to\mathbb{R}^3$. After a regular homotopy of one of them, they agree on a small disk $D&#95;{-}$ around the south pole. (Translate $g$ so the two south poles coincide. Its frame there can be moved to $f$'s along a path in $V&#95;{3,2}$, which is connected because $SO(3)$ is: shrinking the angle joins any rotation to the identity. Once the two maps share a point and a frame, both are nearly linear on a tiny disk, and blending them there keeps rank $2$ by the openness of [Vol. I](/blog/2026/08/17/circling-the-sphere#compactness-and-why-immersions-have-room).) The rest of the sphere, $D&#95;{+}=S^2\setminus D&#95;{-}$, is a disk, and on a disk there *are* coordinates $(u,v)$. Each immersion gives a frame field on it, $(\mathbf{f}&#95;{u},\mathbf{f}&#95;{v})$ and $(\mathbf{g}&#95;{u},\mathbf{g}&#95;{v})$: two maps $D&#95;{+}\to V&#95;{3,2}$ that agree on the boundary circle. Glue two disks along their common boundary and you get a sphere. The glued map $S^2\to V&#95;{3,2}$ has a homotopy class

$$\Omega(f,g)\in\pi_2(V_{3,2}).$$

<div class="ev-def"><strong>Theorem (Smale, 1959).</strong> $f$ and $g$ are regularly homotopic if and only if $\Omega(f,g)=0$. More generally, for immersions $S^2\to\mathbb{R}^n$ with $n\ge3$, regular homotopy classes correspond bijectively to $\pi&#95;{2}(V&#95;{n,2})$.</div>

The computation, written so each symbol is a space you can name:

1. $V&#95;{3,2}\simeq SO(3)$, by Gram–Schmidt and the cross product.
2. $SO(3)\cong\mathbb{RP}^3$, by the quaternion double cover. This is the belt.
3. The covering $S^3\to\mathbb{RP}^3$ has discrete fibre $\lbrace\pm 1\rbrace$, so maps of $S^2$ lift through it, and $\pi&#95;{2}(\mathbb{RP}^3)\cong\pi&#95;{2}(S^3)$.
4. $\pi&#95;{k}(S^n)=0$ for $k&lt;n$ ([Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II)). In particular $\pi&#95;{2}(S^3)=0$: a 2-sphere in a 3-sphere has room to shrink.

Therefore

$$\pi_2(V_{3,2})\cong\pi_2(SO(3))\cong\pi_2(\mathbb{RP}^3)\cong\pi_2(S^3)=0.$$

So $\Omega(f,g)=0$ for every pair. In particular $\iota(p)=p$ and $\alpha(p)=-p$ lie in the same path component of $\operatorname{Imm}(S^2,\mathbb{R}^3)$. Step through it:

<style>
  .ev-chain { display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:0.4rem 0.3rem; margin:0.4em 0 0.6em; }
  .ev-chain .n { background:#1c1c1c; border:1.5px solid #3a3a3a; border-radius:6px; padding:0.5em 0.7em; color:#f0f0f0; transition:opacity .3s, border-color .3s; }
  .ev-chain .n.done { border-color:#3987e5; }
  .ev-chain .n.cur { border-color:#d95926; box-shadow:0 0 0 2px rgba(217,89,38,.25); }
  .ev-chain .n.todo { opacity:.35; }
  .ev-chain .a { color:#8a8a8a; }
  .ev-chain mjx-container { color:#f0f0f0 !important; }
</style>
<div class="mviz" id="ev-proof" tabindex="0" aria-label="The existence proof, one link at a time">
  <div class="mv-title" id="ev-proof-title"></div>
  <div class="ev-chain">
    <span class="n" data-k="0">$\pi&#95;{0}\operatorname{Imm}(S^2,\mathbb{R}^3)$</span><span class="a">↔</span>
    <span class="n" data-k="1">$\pi&#95;{2}(V&#95;{3,2})$</span><span class="a">≅</span>
    <span class="n" data-k="2">$\pi&#95;{2}(SO(3))$</span><span class="a">≅</span>
    <span class="n" data-k="3">$\pi&#95;{2}(\mathbb{RP}^3)$</span><span class="a">≅</span>
    <span class="n" data-k="4">$\pi&#95;{2}(S^3)$</span><span class="a">=</span>
    <span class="n" data-k="5">$0$</span>
  </div>
  <div class="mv-detail" id="ev-proof-detail" style="color:#e0e0e0"></div>
  <div class="mv-controls">
    <button type="button" class="mv-prev">◀ Back</button>
    <button type="button" class="mv-next">Next ▶</button>
    <span class="mv-step"></span>
  </div>
</div>
<script>
(function () {
  var root = document.getElementById('ev-proof');
  if (!root || !window.EV) return;
  var S = [
    { k: 0, t: 'The question.', d: 'Is the space of immersed spheres path-connected? Its path components are what π₀ counts. An eversion exists exactly when ι(p) = p and α(p) = −p land in the same one.' },
    { k: 1, t: 'Smale (1959): regular homotopy classes are classified by π₂(V₃,₂).', d: 'Given two immersions f, g, make them agree near a point. On the rest of the sphere, a disk, compare their derivative frames (df(e₁), df(e₂)) and (dg(e₁), dg(e₂)). The two frame fields agree on the boundary circle, so they glue into one map S² → V₃,₂. Its homotopy class Ω(f, g) is zero exactly when f and g are regularly homotopic.' },
    { k: 2, t: 'V₃,₂ ≃ SO(3).', d: 'Gram–Schmidt slides any pair of independent vectors continuously to an orthonormal pair, so V₃,₂ has the homotopy type of orthonormal 2-frames. An orthonormal pair (v₁, v₂) completes uniquely to a rotation matrix with third column v₁ × v₂.' },
    { k: 3, t: 'SO(3) ≅ ℝP³.', d: 'Unit quaternions form S³, and q ↦ (v ↦ q v q⁻¹) is a two-to-one map S³ → SO(3) identifying q with −q. So SO(3) is S³ with antipodes glued: ℝP³. This is the belt above: the 2π loop lifts to a path from 1 to −1, the 4π loop to a closed loop.' },
    { k: 4, t: 'π₂(ℝP³) ≅ π₂(S³).', d: 'S³ → ℝP³ is a covering with discrete fibre {±1}. In its long exact sequence π₂(fibre) → π₂(S³) → π₂(ℝP³) → π₁(fibre), both ends are 0 because a discrete set has no loops or spheres. So the middle map is an isomorphism.' },
    { k: 5, t: 'π₂(S³) = 0.', d: 'Vol. II: a smooth map S² → S³ misses a point (Sard), and S³ minus a point is ℝ³, where the straight-line homotopy shrinks it. A 2-sphere in a 3-sphere always has room to shrink.' },
    { k: 6, t: 'Therefore every Ω(f, g) is 0.', d: 'All immersions S² → ℝ³ are regularly homotopic to each other. In particular ι ≃ α: a sphere eversion exists. The proof names no path; it only shows that no obstruction can exist.' }
  ];
  var nodes = root.querySelectorAll('.n');
  EV.stepper({ root: root, n: S.length, render: function (i) {
    var k = S[i].k;
    nodes.forEach(function (nd) {
      var j = +nd.getAttribute('data-k');
      nd.className = 'n ' + (k === 6 ? 'done' : j < k ? 'done' : j === k ? 'cur' : 'todo');
    });
    document.getElementById('ev-proof-title').textContent = S[i].t;
    document.getElementById('ev-proof-detail').textContent = S[i].d;
  } });
})();
</script>

**What the theorem says, object by object.** The computation is the easy half, and it is proved above. The hard half is Smale's: that $\Omega(f,g)=0$ really does produce a regular homotopy. Its proof is serious analysis and is not reproduced here, but its statement uses only objects we can now name.

- **Immersions of a disk.** $\operatorname{Imm}(D^2,\mathbb{R}^3)$ is the space of immersions of the closed disk $D^2$ (the disk together with its boundary circle), with the $C^1$ distance of [Vol. I](/blog/2026/08/17/circling-the-sphere#topologies). It is homotopy equivalent to $V&#95;{3,2}$: shrinking the disk toward its centre deforms any immersed disk into a smaller and smaller one, which in the limit is nothing but its frame at the centre.
- **Boundary data.** Restrict an immersion of the disk to its boundary circle, but keep the first derivatives there: the curve the rim traces, and at each of its points the frame $(\mathbf{f}&#95;{u},\mathbf{f}&#95;{v})$, which says how the surface leaves the rim. Call this restriction map $\rho$.
- **A fibration.** Smale's main technical theorem is that $\rho$ has the homotopy lifting property. In words: however the boundary data moves, an immersed disk with that boundary can be moved along with it, starting from any disk you like.
- **The fibre.** The fibre of $\rho$ over fixed boundary data is the space of all immersed disks with that boundary: every way of filling in a fixed rim. Smale shows it is *weakly homotopy equivalent* to the double loop space $\Omega^2V&#95;{3,2}$, meaning there is a map between them that induces a bijection on every $\pi&#95;{k}$. The double loop space is the space of maps of a disk into $V&#95;{3,2}$ that send the whole boundary circle to one fixed frame. Crushing the boundary to a point makes each such map a sphere in $V&#95;{3,2}$, which is why its path components are the elements of $\pi&#95;{2}(V&#95;{3,2})$.

Put together: two fillings of the same rim are joined by a regular homotopy that holds the rim fixed exactly when they lie in the same path component of the fibre, and those path components are the elements of $\pi&#95;{2}(V&#95;{3,2})$. That is what $\Omega(f,g)$ measures. Once $f$ and $g$ agree on $D&#95;{-}$, they are two fillings of the rim of $D&#95;{+}$, and $\Omega(f,g)$ names the path component that separates them, or says that none does. Since $\pi&#95;{2}(V&#95;{3,2})=0$, none ever does.

Why the fibration theorem is hard, [Vol. IV](/blog/2026/08/17/circling-the-sphere-Vol-IV#whitney-graustein) already shows. There, once the turning numbers matched, the proof interpolated the derivative data (the angles) and repaired the result into a closed curve by subtracting an average. That repair takes one line, because any loop of nonzero vectors with average zero is the velocity of a closed curve. A field of frames on a disk has no such freedom: a pair $(\mathbf{a},\mathbf{b})$ is $(\mathbf{f}&#95;{u},\mathbf{f}&#95;{v})$ for some $\mathbf{f}$ only if $\partial&#95;{v}\mathbf{a}=\partial&#95;{u}\mathbf{b}$, and a homotopy of frame fields has no reason to respect that. Smale's analysis is the two-dimensional replacement for the one-line repair.

Hirsch (1959) extended this to arbitrary manifolds. A *formal immersion* $M\to N$ is a candidate derivative: a map $M\to N$ together with, at each point, an injective linear map from the tangent space of $M$ there to the tangent space of $N$ at the image point, varying continuously, with no requirement that it be the derivative of anything. The derivative of an immersion is one; a field of frames that fails $\partial&#95;{v}\mathbf{a}=\partial&#95;{u}\mathbf{b}$ is another. Hirsch's theorem: when $\dim M&lt;\dim N$, the space of immersions $M\to N$ is weakly homotopy equivalent to the space of formal immersions. Every candidate derivative can be deformed into a real one, and up to homotopy nothing is gained or lost. That is an early instance of what Gromov later named the **h-principle**: for many geometric problems, if there is no homotopy-theoretic obstruction, there is a solution. Sphere eversion is its most famous consequence.

**Why $\mathbb{R}^3$ is special.** For $n=4$ the same machine gives $\pi&#95;{2}(V&#95;{4,2})\cong\mathbb{Z}$. (An orthonormal pair $(v&#95;{1},v&#95;{2})$ in $\mathbb{R}^4$ is a point $v&#95;{1}\in S^3$ together with a unit tangent vector $v&#95;{2}$ to $S^3$ there. Unit tangent vectors to $S^3$ form $S^3\times S^2$, because $S^3$, the unit quaternions, has three independent vector fields $qi, qj, qk$ (at each $q$ these three are perpendicular to $q$ and to each other, a basis of the tangent space there); so $V&#95;{4,2}\simeq S^3\times S^2$ and $\pi&#95;{2}=\pi&#95;{2}(S^2)=\mathbb{Z}$.) Immersions $S^2\to\mathbb{R}^4$ therefore have infinitely many regular homotopy classes, detected by the normal Euler number. At each point of a surface in $\mathbb{R}^4$ the *normal plane* is the plane perpendicular to the tangent plane, and the Euler number counts, with signs, the zeros of a generic field of normal vectors. It equals minus twice the number of double points, the points where two sheets cross, counted with sign. For $n\ge5$ the group is $0$ again, because $V&#95;{n,2}$ is $(n-3)$-connected, meaning $\pi&#95;{k}(V&#95;{n,2})=0$ for every $k\le n-3$. In $\mathbb{R}^3$ connectivity does not explain the vanishing: $V&#95;{3,2}\simeq SO(3)$ is not even simply connected, and $\pi&#95;{2}$ vanishes because $SO(3)$ is covered by $S^3$.

---

# Where this goes
{: #where-this-goes}
This is an existence proof. It produces no picture. It says that the obstruction group is zero, so no obstruction can stop you, and nothing more. Bott, Smale's advisor, at first flatly told him he was wrong; once persuaded, he still wanted to see a direct eversion. Finding explicit eversions took years more, and drawing them honestly is the last volume.
