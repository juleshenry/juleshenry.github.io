---
layout: post
title: "Back-of-the-Envelope: Sphere Eversion, Vol. V: Frames and Smale's Theorem"
date: 2026-08-17 12:04:00
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
  <li><a href="#the-whole-derivative">the whole derivative</a></li>
  <li><a href="#fibre-bundles-and-fibrations">fibre bundles and fibrations</a></li>
  <li><a href="#rotations-quaternions-and-the-belt">rotations, quaternions, and the belt</a></li>
  <li><a href="#why-the-obstruction-vanishes">why the obstruction vanishes</a></li>
  <li><a href="#where-this-goes">where this goes</a></li>
</ol>
</div>

---

# the whole derivative
{: #the-whole-derivative}
<div class="cs-q">
<strong>Student.</strong> The Gauss map didn't obstruct anything. What does?
</div>

<div class="cs-a">
<strong>Teacher.</strong> The pair of tangent vectors itself. At each point an immersion $f$ hands you two linearly independent vectors $(\mathbf{f}&#95;{u},\mathbf{f}&#95;{v})$. The space of all such pairs is where the invariant lives.
</div>

<div class="ev-def"><strong>Definition (Stiefel manifold).</strong> $V&#95;{n,k}$ is the space of $k$-tuples of linearly independent vectors in $\mathbb{R}^n$.</div>

The pair $(\mathbf{f}&#95;{u},\mathbf{f}&#95;{v})$ lies in $V&#95;{3,2}$. One dimension down, the velocity $\gamma'$ of an immersed plane curve lies in $V&#95;{2,1}=\mathbb{R}^2\setminus\lbrace 0\rbrace$, which has the homotopy type of $S^1$, and $\pi&#95;{1}(V&#95;{2,1})=\mathbb{Z}$ is precisely the turning number. Whitney–Graustein *is* the one-dimensional case of the theorem this volume proves.

There is a catch. A frame needs coordinates $(u,v)$, and the sphere has no global coordinates with independent partials: a nowhere-zero field $\partial&#95;{u}$ on all of $S^2$ would be a hairy ball combed flat, and Poincaré–Brouwer says that is impossible. So we cannot simply map the whole sphere to $V&#95;{3,2}$. Smale's invariant works around this by using a disk, where coordinates do exist. We will get there; first, the tools.

---

# fibre bundles and fibrations
{: #fibre-bundles-and-fibrations}
<div class="ev-def"><strong>Definition (fibre bundle).</strong> A map $\pi:E\to B$ such that each point of $B$ has a neighbourhood $U$ with $\pi^{-1}(U)\cong U\times F$, compatibly with the projection to $U$. $F$ is the <em>fibre</em>.</div>

Locally a product, globally perhaps twisted. The cylinder $S^1\times[0,1]$ and the Möbius band are both bundles over the circle with fibre an interval; only the first is a product. Three bundles matter here:

- **The covering $\mathbb{R}\to S^1$** from [Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II). Fibre $\mathbb{Z}$, discrete.
- **The quaternion double cover $S^3\to SO(3)$**, below. Fibre $\lbrace\pm1\rbrace$, discrete.
- **$SO(3)\to S^2$, $R\mapsto R\,e&#95;{3}$** (where does the rotation send the north pole). Fibre: the rotations fixing $e&#95;{3}$, a circle $SO(2)$.

Bundles have the **homotopy lifting property** (Vol. II proved it for $\mathbb{R}\to S^1$ by chopping the square into small pieces; the general proof is the same). A map with that property is called a **fibration**, and every fibration comes with a machine for computing homotopy groups:

<div class="ev-def"><strong>Theorem (long exact sequence of a fibration).</strong> For a fibration $F\to E\to B$ there is an exact sequence
$$\cdots\to\pi_n(F)\to\pi_n(E)\to\pi_n(B)\to\pi_{n-1}(F)\to\pi_{n-1}(E)\to\cdots\to\pi_0(E)\to\pi_0(B).$$
</div>

**Exact** means: at each spot, the things killed by the outgoing arrow are exactly the things hit by the incoming one. The map $\pi&#95;{n}(B)\to\pi&#95;{n-1}(F)$ is the interesting one: lift an $n$-sphere in $B$ to an $n$-disk in $E$ (homotopy lifting), and look at where its boundary lands, an $(n-1)$-sphere in a fibre.

The only consequence we need: if both neighbours of a spot are $0$, the arrow through it is an isomorphism. Try it on Vol. II's covering. With $E=\mathbb{R}$ (contractible, all $\pi&#95;{n}=0$) and $F=\mathbb{Z}$:

$$0=\pi_1(\mathbb{R})\to\pi_1(S^1)\to\pi_0(\mathbb{Z})\to\pi_0(\mathbb{R})=\ast,$$

and $\pi&#95;{1}(S^1)\cong\pi&#95;{0}(\mathbb{Z})=\mathbb{Z}$. That is the lifting argument of Vol. II, compressed into one line.

---

# rotations, quaternions, and the belt
{: #rotations-quaternions-and-the-belt}
**$V&#95;{3,2}$ is the rotation group, up to homotopy.** Gram–Schmidt turns a pair of independent vectors into an orthonormal pair, continuously, and the straight-line path from each pair to its Gram–Schmidt output stays independent. So $V&#95;{3,2}$ deformation-retracts onto orthonormal pairs. An orthonormal pair $(v&#95;{1},v&#95;{2})$ extends uniquely to a rotation matrix with columns $(v&#95;{1},\,v&#95;{2},\,v&#95;{1}\times v&#95;{2})$. So

$$V_{3,2}\simeq SO(3).$$

**$SO(3)$ is a sphere with antipodes glued.** A unit quaternion $q=\cos\tfrac\theta2+\sin\tfrac\theta2\,(a\,i+b\,j+c\,k)$ acts on vectors $v\in\mathbb{R}^3$ (as pure quaternions) by $v\mapsto qvq^{-1}$, and that is the rotation by angle $\theta$ about the axis $(a,b,c)$. Unit quaternions form $S^3\subset\mathbb{R}^4$. Every rotation arises, from exactly two quaternions, $q$ and $-q$. So the map $S^3\to SO(3)$ is a two-sheeted covering, and

$$SO(3)\cong S^3/\lbrace\pm1\rbrace=\mathbb{RP}^3.$$

The long exact sequence of this covering, with fibre $\lbrace\pm1\rbrace$ and $\pi&#95;{1}(S^3)=0$, gives $\pi&#95;{1}(SO(3))\cong\mathbb{Z}/2$. A loop of rotations lifts to a path in $S^3$ that either closes up (trivial loop) or ends at $-1$ times its start (the nontrivial one). Rotating by $2\pi$ about a fixed axis is the nontrivial loop; rotating by $4\pi$ is the trivial one. You can feel this with a belt, or a plate held flat on your palm (Dirac's belt trick, the plate trick):

<div id="ev-belt" class="cs-stage" style="height:470px;">
  <div class="cs-hud cs-hud-tl" id="ev-belt-hud"></div>
  <div class="cs-hud cs-hud-tr"><span style="color:#6fa8f0;">belt, front</span><br><span style="color:#f08a5d;">belt, back</span></div>
  <div class="cs-ctrl">
    <label>loop <select id="ev-belt-mode"><option value="4">4π (720°)</option><option value="2">2π (360°)</option></select></label>
    <label>λ <input type="range" id="ev-belt-l" min="0" max="1000" value="0" style="width:34%"> <span id="ev-belt-lv">0.00</span></label>
    <label><input type="checkbox" id="ev-belt-play" checked> play</label>
  </div>
</div>
<p class="cs-cap">The belt is a path of rotations: the frame at distance $u$ along it is $p&#95;{\lambda}(u)\in SO(3)$, drawn as the direction the belt faces. The wall end is fixed at the identity. At $\lambda=0$ the belt carries a full $4\pi$ (or $2\pi$) twist. Slide $\lambda$: for $4\pi$ the explicit null-homotopy $p&#95;{\lambda}(u)=q&#95;{\lambda}(0)^{-1}q&#95;{\lambda}(u)$ untwists it completely with the plate held still. For $2\pi$ the same trick forces the plate to turn, by up to $180^\circ$. No trick can avoid that.</p>
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

The same sequence one step higher is the one we need. $\pi&#95;{2}$ of the fibre $\lbrace\pm1\rbrace$ is $0$ and $\pi&#95;{1}$ of it is $0$ too (as a based space, a discrete set has no loops), so

$$0\to\pi_2(S^3)\xrightarrow{\ \cong\ }\pi_2(SO(3))\to 0.$$

---

# why the obstruction vanishes
{: #why-the-obstruction-vanishes}
<div class="cs-q">
<strong>Student.</strong> Prove the existence. Use Smale's 1958 paper. I can understand it.
</div>

<div class="cs-a">
<strong>Teacher.</strong> The paper is <em>A classification of immersions of the two-sphere</em>, Trans. Amer. Math. Soc. <strong>90</strong> (1958). It does not use contact structures, Reeb foliations, or a "magic formula" of Thurston. Those are neighbouring subjects that the model dragged in. The argument is: regular homotopy classes of immersions $S^2\to\mathbb{R}^n$ are in bijection with $\pi&#95;{2}(V&#95;{n,2})$, and for $n=3$ that group is zero.
</div>

First the invariant, stated so that it avoids the hairy-ball catch. Take two immersions $f,g:S^2\to\mathbb{R}^3$. After a regular homotopy of one of them, they agree on a small disk $D&#95;{-}$ around the south pole. The rest of the sphere, $D&#95;{+}=S^2\setminus D&#95;{-}$, is a disk, and on a disk there *are* coordinates $(u,v)$. Each immersion gives a frame field on it, $(f&#95;{u},f&#95;{v})$ and $(g&#95;{u},g&#95;{v})$: two maps $D&#95;{+}\to V&#95;{3,2}$ that agree on the boundary circle. Glue two disks along their common boundary and you get a sphere. The glued map $S^2\to V&#95;{3,2}$ has a homotopy class

$$\Omega(f,g)\in\pi_2(V_{3,2}).$$

<div class="ev-def"><strong>Theorem (Smale, 1958).</strong> $f$ and $g$ are regularly homotopic if and only if $\Omega(f,g)=0$. More generally, for immersions $S^2\to\mathbb{R}^n$, regular homotopy classes correspond bijectively to $\pi&#95;{2}(V&#95;{n,2})$.</div>

The computation, written so each symbol is a space you can name:

1. $V&#95;{3,2}\simeq SO(3)$, by Gram–Schmidt and the cross product.
2. $SO(3)\cong\mathbb{RP}^3$, by the quaternion double cover. This is the belt.
3. The covering $S^3\to\mathbb{RP}^3$ has discrete fibre $\lbrace\pm 1\rbrace$, so its long exact sequence gives $\pi&#95;{2}(\mathbb{RP}^3)\cong\pi&#95;{2}(S^3)$.
4. $\pi&#95;{k}(S^n)=0$ for $k&lt;n$ ([Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II)). In particular $\pi&#95;{2}(S^3)=0$: a 2-sphere in a 3-sphere has room to shrink.

Therefore

$$\pi_2(V_{3,2})\cong\pi_2(SO(3))\cong\pi_2(\mathbb{RP}^3)\cong\pi_2(S^3)=0.$$

So $\Omega(f,g)=0$ for every pair. In particular $\iota$ and $\alpha$ lie in the same path component of $\operatorname{Imm}(S^2,\mathbb{R}^3)$. Step through it:

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
    { k: 1, t: 'Smale (1958): regular homotopy classes are classified by π₂(V₃,₂).', d: 'Given two immersions f, g, make them agree near a point. On the rest of the sphere, a disk, compare their derivative frames (df(e₁), df(e₂)) and (dg(e₁), dg(e₂)). The two frame fields agree on the boundary circle, so they glue into one map S² → V₃,₂. Its homotopy class Ω(f, g) is zero exactly when f and g are regularly homotopic.' },
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

**What the theorem costs.** The computation is the easy half. Smale's technical work is to show that the space of immersions of a disk with prescribed boundary behaviour is a fibration over the space of that boundary data, and that the fibre is weakly homotopy equivalent to the double loop space $\Omega^2V&#95;{n,2}$ (maps of a 2-disk into $V&#95;{n,2}$ with fixed boundary). That is why $\pi&#95;{0}$ of the fibre, the path components of immersions with fixed boundary, is $\pi&#95;{2}(V&#95;{n,2})$. You do not need the tower to believe the computation above; you need it to believe that the computation classifies immersions.

Hirsch (1959) extended this to any manifolds: when $\dim M&lt;\dim N$, the space of immersions $M\to N$ has the same homotopy type as the space of *formal immersions*, fibrewise-injective linear maps $TM\to TN$, with no integrability required. That is the first instance of what Gromov later named the **h-principle**: for many geometric problems, if there is no homotopy-theoretic obstruction, there is a solution. Sphere eversion is its most famous consequence.

**Why $\mathbb{R}^3$ is special.** For $n=4$ the same machine gives $\pi&#95;{2}(V&#95;{4,2})\cong\mathbb{Z}$. (Unit tangent vectors to $S^3$ form $S^3\times S^2$, because $S^3$, the unit quaternions, has three independent vector fields $qi, qj, qk$; so $V&#95;{4,2}\simeq S^3\times S^2$ and $\pi&#95;{2}=\pi&#95;{2}(S^2)=\mathbb{Z}$.) Immersions $S^2\to\mathbb{R}^4$ therefore have infinitely many regular homotopy classes, detected by the Euler number of the normal bundle (minus twice the algebraic count of double points). The vanishing is special to codimension one in $\mathbb{R}^3$.

---

# where this goes
{: #where-this-goes}
This is an existence proof. It produces no picture. It says that the obstruction group is zero, so no obstruction can stop you, and nothing more. Bott, Smale's advisor, first told him the result was obviously false, since no one could imagine the path. Finding explicit eversions took years more, and drawing them honestly is the last volume.

---

**Next:** [Vol. VI: Seeing the Eversion](/blog/2026/08/17/circling-the-sphere-Vol-VI)

*Sphere Eversion:* [Vol. I](/blog/2026/08/17/circling-the-sphere) · [Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II) · [Vol. III](/blog/2026/08/17/circling-the-sphere-Vol-III) · [Vol. IV](/blog/2026/08/17/circling-the-sphere-Vol-IV) · **Vol. V** · [Vol. VI](/blog/2026/08/17/circling-the-sphere-Vol-VI)
