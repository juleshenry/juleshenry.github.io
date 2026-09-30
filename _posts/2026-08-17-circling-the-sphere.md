---
layout: post
title: "Back-of-the-Envelope: Sphere Eversion, Vol. I: Open, Closed, Clopen"
date: 2026-08-17 12:00:00
categories: differential topology
mathjax: true
---

*Sphere Eversion:* **Vol. I** · [Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II) · [Vol. III](/blog/2026/08/17/circling-the-sphere-Vol-III) · [Vol. IV](/blog/2026/08/17/circling-the-sphere-Vol-IV) · [Vol. V](/blog/2026/08/17/circling-the-sphere-Vol-V) · [Vol. VI](/blog/2026/08/17/circling-the-sphere-Vol-VI)

{% include eversion-kit.html %}

*A zero-to-hero guide to one theorem: a sphere can be turned inside out, smoothly, if it is allowed to pass through itself. We start with the definition of an open set.*

In May 2024 I asked a small language model, running locally, to talk me through Smale's theorem that any two immersions of $S^2$ in $\mathbb{R}^3$ are regularly homotopic. The transcript is [Sphere Eversion Phi3 Notes I](https://honghaptang.github.io/blog/2024/05/22/sphere-eversion-phi3-notes-I). The questions were the right questions. The proofs were not: a linear interpolation was offered as a regular homotopy, the hairy-ball theorem was credited to Smale, and $S^2\times[0,1]$ was described as a solid ball.

In September 2024 I wrote a straight exposition under the title *The Eversion of the Sphere*. It had the theorem right and the pictures wrong. The interactive "eversion" flattened $z$ through zero — exactly the crease the text forbade — and the "Morin surface" was an unnamed polynomial that did not match any formula on the page. That draft is folded into this series; the old URL redirects here.

This series is the two of them talking, rebuilt from the ground up. Whenever the Phi-3 transcript asked a good question, it appears as a boxed **Student** question, answered by the **Teacher**. Everything else is built from definitions. Every figure is an equation you can drag.

<p style="text-align:center;">
  <img src="/blog/assets/2024/eversion/eversion.gif" alt="Sphere eversion through the Morin halfway model" style="max-width:100%;">
</p>

The still above is a genuine eversion, passing through Morin's halfway model. By the end of [Vol. VI](/blog/2026/08/17/circling-the-sphere-Vol-VI) you will know exactly what it is a picture of, and why its existence was proved before anyone could draw it.

<table class="cs-err">
  <thead><tr><th>Vol.</th><th>Topic</th><th>What it contributes to the proof</th></tr></thead>
  <tbody>
    <tr><td><strong>I</strong></td><td>Open, closed, clopen</td><td>Spaces, continuity, connectedness: the reason an integer that varies continuously cannot jump.</td></tr>
    <tr><td><a href="/blog/2026/08/17/circling-the-sphere-Vol-II">II</a></td><td>Paths and homotopy</td><td>Homotopy, $\pi&#95;{1}(S^1)=\mathbb{Z}$, and $\pi&#95;{k}(S^n)=0$ for $k&lt;n$.</td></tr>
    <tr><td><a href="/blog/2026/08/17/circling-the-sphere-Vol-III">III</a></td><td>Manifolds and immersions</td><td>Charts, the Jacobian, immersions, regular homotopy, and a homotopy that cheats.</td></tr>
    <tr><td><a href="/blog/2026/08/17/circling-the-sphere-Vol-IV">IV</a></td><td>Curves in the plane</td><td>Turning number and Whitney–Graustein: why a circle cannot evert.</td></tr>
    <tr><td><a href="/blog/2026/08/17/circling-the-sphere-Vol-V">V</a></td><td>Frames and Smale's theorem</td><td>Fibrations, $SO(3)\cong\mathbb{RP}^3$, the belt trick, and $\pi&#95;{2}(V&#95;{3,2})=0$.</td></tr>
    <tr><td><a href="/blog/2026/08/17/circling-the-sphere-Vol-VI">VI</a></td><td>Seeing the eversion</td><td>Corrugations, a ruled formula for the halfway model, and how to tell you are halfway.</td></tr>
  </tbody>
</table>

<div class="cs-toc">
<strong>Contents</strong>
<ol>
  <li><a href="#the-question">the question</a></li>
  <li><a href="#open-balls-and-open-sets">open balls and open sets</a></li>
  <li><a href="#topologies">topologies</a></li>
  <li><a href="#clopen-sets-and-connectedness">clopen sets and connectedness</a></li>
  <li><a href="#continuity">continuity</a></li>
  <li><a href="#paths-and-path-connectedness">paths and path-connectedness</a></li>
  <li><a href="#compactness-and-why-immersions-have-room">compactness, and why immersions have room</a></li>
  <li><a href="#where-this-goes">where this goes</a></li>
</ol>
</div>

---

# the question
{: #the-question}
<div class="cs-q">
<strong>Student.</strong> What does it even mean to turn a sphere inside out "smoothly"? Couldn't I just push the north pole through the south pole?
</div>

<div class="cs-a">
<strong>Teacher.</strong> You could, and you would crease it. The theorem is about a <em>path</em> of surfaces, each of them smooth, from the round sphere to the round sphere with its inside facing out. Before we can say "path of surfaces" we need to say what it means for two surfaces to be <em>close</em>. That is what topology is for. We will need very little of it, but we need it exactly.
</div>

Here is the target, stated once in full so that every word can be earned later. Let $\iota(p)=p$ be the standard sphere and $\alpha(p)=-p$ its antipodal copy, whose inside faces out.

<div class="ev-def"><strong>Theorem (Smale, 1958).</strong> The space $\operatorname{Imm}(S^2,\mathbb{R}^3)$ of immersions of the 2-sphere in 3-space is path-connected. In particular there is a path of immersions from $\iota$ to $\alpha$: a sphere eversion.</div>

"Immersion" is [Vol. III](/blog/2026/08/17/circling-the-sphere-Vol-III). This volume is about the words *space* and *path-connected*.

---

# open balls and open sets
{: #open-balls-and-open-sets}
Distance in $\mathbb{R}^n$ is $d(p,q)=\lVert p-q\rVert$. The **open ball** of radius $\varepsilon&gt;0$ about $p$ is

$$B(p,\varepsilon)=\{\,q\in\mathbb{R}^n:\ d(p,q)<\varepsilon\,\}.$$

<div class="ev-def"><strong>Definition (open set).</strong> $U\subseteq\mathbb{R}^n$ is <em>open</em> if every point of $U$ has some ball around it that stays inside $U$: for each $p\in U$ there is an $\varepsilon&gt;0$ with $B(p,\varepsilon)\subseteq U$.</div>

Open means *every point has room*. The open disk $\lbrace\lVert p\rVert&lt;1\rbrace$ is open: a point at distance $d&lt;1$ from the centre can use $\varepsilon=1-d$. The closed disk $\lbrace\lVert p\rVert\le 1\rbrace$ is not: a point on the edge belongs to the set, but every ball around it pokes outside.

<div class="ev-def"><strong>Definition (closed set).</strong> $C$ is <em>closed</em> if its complement is open.</div>

Equivalently, $C$ is closed when it contains every point it can get arbitrarily close to (its limit points). Closed is **not** the opposite of open. A set can be both, or neither. Try all three:

<div class="mviz" id="ev-open" tabindex="0" aria-label="Open, closed and half-open disks, with epsilon balls">
  <div class="mv-title" id="ev-open-title"></div>
  <svg id="ev-open-svg" viewBox="0 0 640 320" role="img" aria-label="A disk in the plane and a draggable point with its largest safe ball">
    <rect x="0" y="0" width="640" height="320" fill="#121212"/>
    <path id="ev-open-fill" fill="#3987e5" fill-opacity="0.22"/>
    <path id="ev-open-bd-in" fill="none" stroke="#3987e5" stroke-width="3"/>
    <path id="ev-open-bd-out" fill="none" stroke="#3987e5" stroke-width="2" stroke-dasharray="5 6"/>
    <circle id="ev-open-ball" fill="#c98500" fill-opacity="0.18" stroke="#c98500" stroke-width="2"/>
    <circle id="ev-open-pt" r="7" fill="#f0f0f0" stroke="#121212" stroke-width="2" class="drag"/>
    <text x="230" y="306" text-anchor="middle" font-size="13" style="fill:#c3c2b7">drag the white point anywhere, including onto the edge</text>
    <g id="ev-open-verdict"></g>
  </svg>
  <div class="mv-detail" id="ev-open-detail"></div>
  <div class="mv-controls">
    <button type="button" data-m="open">open disk</button>
    <button type="button" data-m="closed">closed disk</button>
    <button type="button" data-m="half">half-open disk</button>
    <button type="button" id="ev-open-edge">put point on the edge</button>
    <span class="mv-key"><b style="background:#3987e5"></b>edge included<b style="background:repeating-linear-gradient(90deg,#3987e5 0 5px,transparent 5px 9px)"></b>edge excluded<b style="background:#c98500"></b>ball B(p, ε)</span>
  </div>
</div>
<p class="cs-cap">Solid edge: those points belong to the set. Dashed edge: they do not. The gold disk is the biggest ball around your point that stays on one side. On the edge no ball works, and which side fails decides whether the set is open, closed, or neither.</p>
<script>
(function () {
  var root = document.getElementById('ev-open');
  if (!root || !window.EV) return;
  var svg = document.getElementById('ev-open-svg'), E = EV.el;
  var CX = 230, CY = 150, R = 115, mode = 'open', P = { x: 280, y: 120 }, phase = 0, last = 0;
  var verdict = document.getElementById('ev-open-verdict');
  function circlePath() { return 'M' + (CX - R) + ',' + CY + 'a' + R + ',' + R + ' 0 1 0 ' + 2 * R + ',0a' + R + ',' + R + ' 0 1 0 ' + (-2 * R) + ',0'; }
  // does the set contain the boundary point at angle a?
  function edgeIn(a) { return mode === 'closed' || (mode === 'half' && Math.sin(a) > 0); }
  function setMode(m) {
    mode = m;
    root.querySelectorAll('[data-m]').forEach(function (b) { b.classList.toggle('on', b.getAttribute('data-m') === m); });
    var fin = document.getElementById('ev-open-bd-in'), fout = document.getElementById('ev-open-bd-out');
    document.getElementById('ev-open-fill').setAttribute('d', circlePath());
    if (m === 'open') { fin.setAttribute('d', ''); fout.setAttribute('d', circlePath()); }
    if (m === 'closed') { fin.setAttribute('d', circlePath()); fout.setAttribute('d', ''); }
    if (m === 'half') { // top half solid, bottom half dashed
      fin.setAttribute('d', 'M' + (CX + R) + ',' + CY + 'A' + R + ',' + R + ' 0 0 0 ' + (CX - R) + ',' + CY);
      fout.setAttribute('d', 'M' + (CX - R) + ',' + CY + 'A' + R + ',' + R + ' 0 0 0 ' + (CX + R) + ',' + CY);
    }
    EV.clear(verdict);
    var rows = { open: ['open ✓', 'closed ✗'], closed: ['open ✗', 'closed ✓'], half: ['open ✗', 'closed ✗'] }[m];
    var names = { open: 'the open disk', closed: 'the closed disk', half: 'half-open disk' }[m];
    E('text', { x: 500, y: 110, 'text-anchor': 'middle', 'font-size': 14, style: 'fill:#c3c2b7' }, verdict).textContent = names;
    E('text', { x: 500, y: 145, 'text-anchor': 'middle', 'font-size': 20, 'font-weight': 600 }, verdict).textContent = rows[0];
    E('text', { x: 500, y: 178, 'text-anchor': 'middle', 'font-size': 20, 'font-weight': 600 }, verdict).textContent = rows[1];
    if (m === 'half') E('text', { x: 500, y: 208, 'text-anchor': 'middle', 'font-size': 14, style: 'fill:#c3c2b7' }, verdict).textContent = 'neither';
    document.getElementById('ev-open-title').textContent = {
      open: 'The open disk { |p − c| < r }: every point has some room. The edge is not part of the set.',
      closed: 'The closed disk { |p − c| ≤ r }: the edge is included, so edge points have no room inside; but the outside is open.',
      half: 'The open disk plus the top half of its edge. The top edge fails "open", the bottom edge fails "closed".'
    }[m];
    draw();
  }
  function draw() {
    var dx = P.x - CX, dy = P.y - CY, d = Math.hypot(dx, dy), a = Math.atan2(-dy, dx);
    var ball = document.getElementById('ev-open-ball'), pt = document.getElementById('ev-open-pt'), det = document.getElementById('ev-open-detail');
    pt.setAttribute('cx', P.x); pt.setAttribute('cy', P.y);
    ball.setAttribute('cx', P.x); ball.setAttribute('cy', P.y);
    var onEdge = Math.abs(d - R) < 0.5;
    if (!onEdge) {
      var eps = Math.abs(R - d);
      ball.setAttribute('r', eps); ball.setAttribute('stroke', '#c98500'); ball.setAttribute('fill', '#c98500');
      det.textContent = (d < R ? 'p is inside. ' : 'p is outside. ') + 'ε = ' + (eps / R).toFixed(2) + ' r works: the ball B(p, ε) stays ' + (d < R ? 'inside the set.' : 'outside the set.') + ' Move p toward the edge and watch ε shrink to nothing.';
    } else {
      // pulsing ball that always leaks: radius cycles 45 -> 4
      var r = 4 + 41 * (0.5 + 0.5 * Math.cos(phase));
      ball.setAttribute('r', r); ball.setAttribute('stroke', '#d95926'); ball.setAttribute('fill', '#d95926');
      det.textContent = edgeIn(a)
        ? 'p is on the edge and IN the set. Every ball around p, however small, pokes outside. So the set is not open.'
        : 'p is on the edge and NOT in the set, so p lies in the complement. Every ball around p pokes into the set, so the complement is not open, and the set is not closed.';
    }
  }
  function place(q) {
    var dx = q.x - CX, dy = q.y - CY, d = Math.hypot(dx, dy);
    if (Math.abs(d - R) < 9 && d > 0) { q = { x: CX + dx * R / d, y: CY + dy * R / d }; } // snap onto the edge
    P = { x: Math.max(8, Math.min(430, q.x)), y: Math.max(8, Math.min(290, q.y)) };
    draw();
  }
  EV.drag(svg, svg, place);
  root.querySelectorAll('[data-m]').forEach(function (b) { b.addEventListener('click', function () { setMode(b.getAttribute('data-m')); }); });
  var edgeAngles = { open: 0.9, closed: 0.9, half: -0.9 };
  document.getElementById('ev-open-edge').addEventListener('click', function () {
    var a = edgeAngles[mode]; P = { x: CX + R * Math.cos(a), y: CY - R * Math.sin(a) }; draw();
  });
  var vis = true;
  if (window.IntersectionObserver) new IntersectionObserver(function (e) { vis = e[0].isIntersecting; }).observe(root);
  (function tick(ts) {
    requestAnimationFrame(tick);
    var dt = Math.min(50, ts - (last || ts)); last = ts;
    if (!vis) return;
    phase += 0.0035 * dt;
    if (Math.abs(Math.hypot(P.x - CX, P.y - CY) - R) < 0.5) draw();
  })(0);
  setMode('open');
})();
</script>

The half-open disk is neither: its top edge has points *in* the set with no room (so it is not open), and its bottom edge has points *outside* the set with no room in the complement (so it is not closed). On the real line the same thing happens with $[0,1)$.

Two facts about open sets in $\mathbb{R}^n$ are worth checking by hand, because they become the definition of everything else:

1. **Any union of open sets is open.** If $p$ lies in the union it lies in one of the sets, and that set's ball works.
2. **A finite intersection of open sets is open.** If $p\in U&#95;{1}\cap\dots\cap U&#95;{k}$, take the smallest of the $k$ radii. With infinitely many sets the smallest radius may be $0$: $\bigcap&#95;{n}(-\tfrac1n,\tfrac1n)=\lbrace 0\rbrace$, which is not open.

---

# topologies
{: #topologies}
Those two facts, plus "$\varnothing$ and the whole space are open", are all we ever use. So we promote them to a definition and forget the distance.

<div class="ev-def"><strong>Definition (topological space).</strong> A set $X$ together with a collection $\mathcal{T}$ of subsets, called <em>open</em>, such that (i) $\varnothing$ and $X$ are open, (ii) any union of open sets is open, (iii) any finite intersection of open sets is open.</div>

Examples that will matter:

- **Metric topologies.** Any set with a distance function, open sets defined by balls exactly as above. This includes $\mathbb{R}^n$, the sphere $S^2$ (with distance measured in $\mathbb{R}^3$), and, crucially, **spaces of maps**. For maps $f,g:S^2\to\mathbb{R}^3$ with derivatives, $d(f,g)=\sup\lVert f-g\rVert+\sup\lVert df-dg\rVert$ is a distance. Two surfaces are close when their points *and their tangent planes* are close. That is the topology in which Smale's theorem lives.
- **The discrete topology.** Every subset is open. On $\mathbb{Z}$ with its usual distance this is what you get, since $B(n,\tfrac12)=\lbrace n\rbrace$.
- **The subspace topology.** If $Y\subseteq X$, a set is open in $Y$ when it is $U\cap Y$ for some $U$ open in $X$. Open-ness is relative to the ambient space, and this is where things get interesting.

---

# clopen sets and connectedness
{: #clopen-sets-and-connectedness}
<div class="cs-q">
<strong>Student.</strong> If a set can be both open and closed, what does that look like?
</div>

<div class="cs-a">
<strong>Teacher.</strong> Like a crack in the space. $\varnothing$ and $X$ are always both; call a set that is both <em>clopen</em>. Any other clopen set $A$ splits $X$ into $A$ and $X\setminus A$, two open pieces with nothing in between. A space with no such split is <em>connected</em>.
</div>

<div class="mviz" id="ev-clopen" tabindex="0" aria-label="A clopen subset of a disconnected space, step by step">
  <div class="mv-title" id="ev-clopen-title"></div>
  <svg id="ev-clopen-svg" viewBox="0 0 640 190" role="img" aria-label="Number line with the space X and open intervals"></svg>
  <div class="mv-detail" id="ev-clopen-detail"></div>
  <div class="mv-controls">
    <button type="button" class="mv-prev">◀ Back</button>
    <button type="button" class="mv-next">Next ▶</button>
    <span class="mv-key"><b style="background:#3987e5"></b>the space<b style="background:#c98500"></b>open interval of ℝ<b style="background:#d95926"></b>the intersection</span>
    <span class="mv-step"></span>
  </div>
</div>
<script>
(function () {
  var root = document.getElementById('ev-clopen');
  if (!root || !window.EV) return;
  var svg = document.getElementById('ev-clopen-svg'), E = EV.el, Y = 118;
  var x = function (v) { return 40 + (v + 0.8) * 560 / 4.6; };
  var axis = E('g', {}, svg);
  E('line', { x1: 30, x2: 610, y1: Y, y2: Y, stroke: '#3a3a3a', 'stroke-width': 1 }, axis);
  [0, 1, 2, 3].forEach(function (v) {
    E('line', { x1: x(v), x2: x(v), y1: Y + 14, y2: Y + 20, stroke: '#6a6a6a' }, axis);
    E('text', { x: x(v), y: Y + 36, 'text-anchor': 'middle', 'font-size': 13, style: 'fill:#c3c2b7' }, axis).textContent = v;
  });
  function seg(a, b, color, w, parent) {
    var g = E('g', {}, parent);
    E('line', { x1: x(a), x2: x(b), y1: Y, y2: Y, stroke: color, 'stroke-width': w, 'stroke-linecap': 'butt' }, g);
    return g;
  }
  function dot(v, filled, color, parent) { E('circle', { cx: x(v), cy: Y, r: 5.5, fill: filled ? color : '#121212', stroke: color, 'stroke-width': 2 }, parent); }
  function band(a, b, label, parent) {
    var g = E('g', {}, parent);
    E('rect', { x: x(a), y: Y - 34, width: x(b) - x(a), height: 68, fill: '#c98500', 'fill-opacity': 0.14 }, g);
    [a, b].forEach(function (v) { E('line', { x1: x(v), x2: x(v), y1: Y - 34, y2: Y + 34, stroke: '#c98500', 'stroke-width': 2, 'stroke-dasharray': '4 4' }, g); });
    E('text', { x: (x(a) + x(b)) / 2, y: Y - 44, 'text-anchor': 'middle', 'font-size': 14, style: 'fill:#e0a526' }, g).textContent = label;
    return g;
  }
  var L = {};
  L.X = E('g', { class: 'fade' }, svg); seg(0, 1, '#3987e5', 6, L.X); seg(2, 3, '#3987e5', 6, L.X); [0, 1, 2, 3].forEach(function (v) { dot(v, true, '#3987e5', L.X); });
  L.Xlab = E('text', { x: x(1.5), y: Y + 60, 'text-anchor': 'middle', 'font-size': 14, class: 'fade' }, svg); L.Xlab.textContent = 'X = [0, 1] ∪ [2, 3]';
  L.Y = E('g', { class: 'fade' }, svg); seg(0, 3, '#3987e5', 6, L.Y); dot(0, true, '#3987e5', L.Y); dot(3, true, '#3987e5', L.Y);
  L.Ylab = E('text', { x: x(1.5), y: Y + 60, 'text-anchor': 'middle', 'font-size': 14, class: 'fade' }, svg); L.Ylab.textContent = 'Y = [0, 3]';
  L.b1 = E('g', { class: 'fade' }, svg); band(-0.5, 1.5, '(−½, 3⁄2)', L.b1);
  L.b2 = E('g', { class: 'fade' }, svg); band(1.5, 3.5, '(3⁄2, 7⁄2)', L.b2);
  L.A = E('g', { class: 'fade' }, svg); seg(0, 1, '#d95926', 6, L.A); dot(0, true, '#d95926', L.A); dot(1, true, '#d95926', L.A);
  L.B = E('g', { class: 'fade' }, svg); seg(2, 3, '#d95926', 6, L.B); dot(2, true, '#d95926', L.B); dot(3, true, '#d95926', L.B);
  L.Yb = E('g', { class: 'fade' }, svg); seg(0, 1.5, '#d95926', 6, L.Yb); dot(0, true, '#d95926', L.Yb); dot(1.5, false, '#d95926', L.Yb);
  L.poke = E('g', { class: 'fade' }, svg);
  E('rect', { x: x(1.3), y: Y - 16, width: x(1.7) - x(1.3), height: 32, rx: 4, fill: 'none', stroke: '#f0f0f0', 'stroke-width': 1.5, 'stroke-dasharray': '3 3' }, L.poke);
  E('text', { x: x(1.5), y: Y - 24, 'text-anchor': 'middle', 'font-size': 13 }, L.poke).textContent = 'any interval around 3⁄2';
  var S = [
    { on: ['X', 'Xlab'], t: 'The space X = [0, 1] ∪ [2, 3], two closed segments, with the subspace topology: a set is open in X when it is (open set of ℝ) ∩ X.',
      d: 'Openness is relative. [0, 1] is not open in ℝ, because the point 1 has no room. Watch what happens inside X.' },
    { on: ['X', 'Xlab', 'b1', 'A'], t: 'A = [0, 1] equals X ∩ (−½, 3⁄2). That is an open set of ℝ intersected with X, so A is open in X.',
      d: 'Inside X, the point 1 does have room: the ball (½, 3⁄2) meets X only in (½, 1], which lies in A. There is nothing of X just to the right of 1.' },
    { on: ['X', 'Xlab', 'b2', 'B'], t: 'Its complement X ∖ A = [2, 3] equals X ∩ (3⁄2, 7⁄2), also open in X. A set whose complement is open is closed, so A is closed in X.',
      d: 'The same trick, applied to the other piece. The gap (1, 2) is what makes both intervals fit.' },
    { on: ['X', 'Xlab', 'b1', 'b2', 'A', 'B'], t: 'So A is clopen (open and closed), and it is neither ∅ nor X. By definition, X is disconnected.',
      d: 'A clopen set that is not ∅ or the whole space is exactly a clean split of the space into two pieces that do not touch.' },
    { on: ['Y', 'Ylab', 'b1', 'Yb'], t: 'Close the gap: Y = [0, 3]. The same interval now gives Y ∩ (−½, 3⁄2) = [0, 3⁄2), open in Y.',
      d: 'Its right end 3⁄2 is not included (hollow dot). So this set is open in Y. Is it also closed?' },
    { on: ['Y', 'Ylab', 'b1', 'Yb', 'poke'], t: 'No. Its complement [3⁄2, 3] is not open in Y: every interval around 3⁄2 reaches back into [0, 3⁄2). No proper clopen subset of [0, 3] exists at all.',
      d: 'That last sentence is the theorem "an interval is connected", proved in the text by taking a supremum. It is the engine behind every invariant in this series.' }
  ];
  EV.stepper({ root: root, n: S.length, render: function (i) {
    for (var k in L) L[k].setAttribute('opacity', S[i].on.indexOf(k) >= 0 ? 1 : 0);
    document.getElementById('ev-clopen-title').textContent = S[i].t;
    document.getElementById('ev-clopen-detail').textContent = S[i].d;
  } });
})();
</script>

<div class="ev-def"><strong>Definition (connected).</strong> $X$ is <em>connected</em> if its only clopen subsets are $\varnothing$ and $X$.</div>

**Theorem.** The interval $[0,1]$ is connected.

*Proof.* Suppose $A\subseteq[0,1]$ is clopen and contains $0$; we show $A=[0,1]$. Let $s=\sup\lbrace x: [0,x]\subseteq A\rbrace$. Because $A$ is closed, it contains the limit point $s$. Because $A$ is open (in $[0,1]$), if $s&lt;1$ some interval $[s,s+\varepsilon)$ also lies in $A$, contradicting the choice of $s$. So $s=1$ and $A=[0,1]$. If instead $0\notin A$, apply the argument to the complement, which is also clopen. $\square$

This is the completeness of the real numbers, wearing a topological hat. It is the single fact on which the rest of the series leans.

---

# continuity
{: #continuity}
In calculus, $f$ is continuous if for every $\varepsilon$ there is a $\delta$. In topology the same idea is one line.

<div class="ev-def"><strong>Definition (continuous).</strong> $f:X\to Y$ is <em>continuous</em> if the preimage $f^{-1}(V)=\lbrace x: f(x)\in V\rbrace$ of every open $V\subseteq Y$ is open in $X$.</div>

For $f:\mathbb{R}\to\mathbb{R}$ this is exactly $\varepsilon$--$\delta$: take $V=(f(x)-\varepsilon,\,f(x)+\varepsilon)$; "the preimage is open" says some $(x-\delta,\,x+\delta)$ maps into $V$. Drag the interval below and try to find an open $V$ whose preimage is not open.

<div class="mviz" id="ev-pre" tabindex="0" aria-label="Preimages of open intervals under a continuous function and a step function">
  <div class="mv-title" id="ev-pre-title"></div>
  <svg id="ev-pre-svg" viewBox="0 0 640 330" role="img" aria-label="Graph of a function, an open interval on the vertical axis, and its preimage on the horizontal axis">
    <g id="ev-pre-axes"></g>
    <rect id="ev-pre-band" x="60" width="560" fill="#c98500" fill-opacity="0.12"/>
    <g id="ev-pre-drop"></g>
    <path id="ev-pre-graph" fill="none" stroke="#3987e5" stroke-width="2.5"/>
    <g id="ev-pre-jump"></g>
    <line id="ev-pre-yint" x1="60" x2="60" stroke="#c98500" stroke-width="7"/>
    <circle id="ev-pre-ylo" cx="60" r="5.5" fill="#121212" stroke="#c98500" stroke-width="2"/>
    <circle id="ev-pre-yhi" cx="60" r="5.5" fill="#121212" stroke="#c98500" stroke-width="2"/>
    <g id="ev-pre-pre"></g>
    <text x="340" y="322" text-anchor="middle" font-size="13" style="fill:#c3c2b7">drag up and down on the plot to move the interval V</text>
  </svg>
  <div class="mv-detail" id="ev-pre-detail"></div>
  <div class="mv-controls">
    <button type="button" data-f="c">continuous f</button>
    <button type="button" data-f="s">step function g</button>
    <label>width of V <input type="range" id="ev-pre-w" min="10" max="90" value="40"></label>
    <span class="mv-key"><b style="background:#c98500"></b>open interval V<b style="background:#d95926"></b>its preimage</span>
  </div>
</div>
<p class="cs-cap">Hollow dot: endpoint not included. Filled dot: endpoint included. For the continuous function every preimage is a union of open intervals, wherever you put $V$. For the step function one position of $V$ produces a preimage with a filled endpoint, a point with no room, and that single failure is the discontinuity.</p>
<script>
(function () {
  var root = document.getElementById('ev-pre');
  if (!root || !window.EV) return;
  var svg = document.getElementById('ev-pre-svg'), E = EV.el;
  var X0 = 60, X1 = 620, YT = 20, YB = 270, XMAX = 4, YMAX = 3.2;
  var X = function (v) { return X0 + v / XMAX * (X1 - X0); }, Y = function (v) { return YB - v / YMAX * (YB - YT); };
  var F = {
    c: { name: 'f(x) = 1.5 + 0.9 sin(1.7x) + 0.15x, continuous', f: function (x) { return 1.5 + 0.9 * Math.sin(1.7 * x) + 0.15 * x; } },
    s: { name: 'g(x) = 1 for x < 2, and 2.3 for x ≥ 2', f: function (x) { return x < 2 ? 1 : 2.3; } }
  };
  var cur = 'c', c = 1.8;
  var ax = document.getElementById('ev-pre-axes');
  E('line', { x1: X0, x2: X1, y1: YB, y2: YB, stroke: '#555' }, ax);
  E('line', { x1: X0, x2: X0, y1: YT, y2: YB, stroke: '#555' }, ax);
  for (var i = 0; i <= 4; i++) E('text', { x: X(i), y: YB + 18, 'text-anchor': 'middle', 'font-size': 12, style: 'fill:#c3c2b7' }, ax).textContent = i;
  for (i = 1; i <= 3; i++) E('text', { x: X0 - 10, y: Y(i) + 4, 'text-anchor': 'end', 'font-size': 12, style: 'fill:#c3c2b7' }, ax).textContent = i;
  function hw() { return document.getElementById('ev-pre-w').value / 100; }
  function fmt(v) { return (Math.round(v * 100) / 100).toFixed(2); }
  // preimage of (lo, hi) under the continuous f on [0, 4], by sampling + bisection
  function preC(lo, hi) {
    var f = F.c.f, N = 800, segs = [], inside = false, start = 0;
    function edge(a, b) { // find crossing between a (state sa) and b
      var sa = f(a) > lo && f(a) < hi;
      for (var k = 0; k < 40; k++) { var m = (a + b) / 2, sm = f(m) > lo && f(m) < hi; if (sm === sa) a = m; else b = m; }
      return (a + b) / 2;
    }
    for (var j = 0; j <= N; j++) {
      var xx = XMAX * j / N, s = f(xx) > lo && f(xx) < hi;
      if (s && !inside) { start = j === 0 ? 0 : edge(XMAX * (j - 1) / N, xx); inside = true; }
      if (!s && inside) { segs.push([start, edge(XMAX * (j - 1) / N, xx)]); inside = false; }
    }
    if (inside) segs.push([start, XMAX]);
    return segs.map(function (sg) { return { a: sg[0], b: sg[1], aIn: false, bIn: false, aEdge: sg[0] === 0, bEdge: sg[1] === XMAX }; });
  }
  function preS(lo, hi) {
    var in1 = lo < 1 && 1 < hi, in2 = lo < 2.3 && 2.3 < hi;
    if (in1 && in2) return [{ a: 0, b: XMAX, aEdge: true, bEdge: true }];
    if (in1) return [{ a: 0, b: 2, aEdge: true, bIn: false }];
    if (in2) return [{ a: 2, b: XMAX, aIn: true, bEdge: true }];
    return [];
  }
  function draw() {
    var h = hw() / 2 + 0.05, lo = c - h, hi = c + h;
    var band = document.getElementById('ev-pre-band');
    band.setAttribute('y', Y(hi)); band.setAttribute('height', Y(lo) - Y(hi));
    var yi = document.getElementById('ev-pre-yint');
    yi.setAttribute('y1', Y(hi) + 6); yi.setAttribute('y2', Y(lo) - 6);
    document.getElementById('ev-pre-ylo').setAttribute('cy', Y(lo)); document.getElementById('ev-pre-yhi').setAttribute('cy', Y(hi));
    var segs = cur === 'c' ? preC(lo, hi) : preS(lo, hi), g = document.getElementById('ev-pre-pre'), dr = document.getElementById('ev-pre-drop');
    EV.clear(g); EV.clear(dr);
    var bad = false;
    segs.forEach(function (s) {
      E('rect', { x: X(s.a), y: Y(lo), width: X(s.b) - X(s.a), height: Y(0) - Y(lo), fill: '#d95926', 'fill-opacity': 0.08 }, dr);
      E('line', { x1: X(s.a), x2: X(s.b), y1: YB, y2: YB, stroke: '#d95926', 'stroke-width': 7 }, g);
      [[s.a, s.aIn, s.aEdge], [s.b, s.bIn, s.bEdge]].forEach(function (e) {
        if (e[2]) return; // runs off the edge of the window: no endpoint here
        E('circle', { cx: X(e[0]), cy: YB, r: 6, fill: e[1] ? '#d95926' : '#121212', stroke: '#d95926', 'stroke-width': 2 }, g);
        if (e[1]) bad = e[0];
      });
    });
    var det = document.getElementById('ev-pre-detail');
    var desc = segs.length === 0 ? '∅' : segs.map(function (s) {
      return (s.aEdge ? '(…' : (s.aIn ? '[' : '(') + fmt(s.a)) + ', ' + (s.bEdge ? '…)' : fmt(s.b) + (s.bIn ? ']' : ')'));
    }).join(' ∪ ');
    det.textContent = 'V = (' + fmt(lo) + ', ' + fmt(hi) + ')   preimage = ' + desc + '   ' +
      (bad !== false ? '← contains its endpoint x = 2, no ball around 2 fits inside: NOT open' : '← open ✓');
  }
  function setF(k) {
    cur = k;
    root.querySelectorAll('[data-f]').forEach(function (b) { b.classList.toggle('on', b.getAttribute('data-f') === k); });
    var pts = [], jg = document.getElementById('ev-pre-jump'); EV.clear(jg);
    if (k === 'c') { for (var j = 0; j <= 400; j++) { var xx = XMAX * j / 400; pts.push([X(xx), Y(F.c.f(xx))]); } document.getElementById('ev-pre-graph').setAttribute('d', EV.path(pts)); }
    else {
      document.getElementById('ev-pre-graph').setAttribute('d', 'M' + X(0) + ',' + Y(1) + 'L' + X(2) + ',' + Y(1) + 'M' + X(2) + ',' + Y(2.3) + 'L' + X(4) + ',' + Y(2.3));
      E('circle', { cx: X(2), cy: Y(1), r: 5.5, fill: '#121212', stroke: '#3987e5', 'stroke-width': 2 }, jg);
      E('circle', { cx: X(2), cy: Y(2.3), r: 5.5, fill: '#3987e5', stroke: '#3987e5', 'stroke-width': 2 }, jg);
    }
    document.getElementById('ev-pre-title').textContent = k === 'c'
      ? F.c.name + '. Continuity means: the preimage of every open set is open. Try to break it.'
      : F.s.name + '. Put V around 2.3 but not around 1, and the preimage becomes [2, …), which contains its endpoint.';
    draw();
  }
  EV.drag(svg, svg, function (p) { c = Math.max(0.1, Math.min(3.1, (YB - p.y) / (YB - YT) * YMAX)); draw(); });
  document.getElementById('ev-pre-w').addEventListener('input', draw);
  root.querySelectorAll('[data-f]').forEach(function (b) { b.addEventListener('click', function () { setF(b.getAttribute('data-f')); }); });
  setF('c');
})();
</script>

Now the payoff, in three lines.

**Theorem.** The continuous image of a connected space is connected.

*Proof.* If $f:X\to Y$ is continuous and onto and $B\subseteq Y$ is clopen, then $f^{-1}(B)$ is clopen in $X$ (preimages respect complements). If $X$ is connected, $f^{-1}(B)$ is $\varnothing$ or $X$, so $B$ is $\varnothing$ or $Y$. $\square$

**Corollary (intermediate value theorem).** A continuous $f:[0,1]\to\mathbb{R}$ takes every value between $f(0)$ and $f(1)$. (Otherwise a missed value $c$ splits the image into the clopen pieces below and above $c$.)

**Corollary (integers cannot jump).** *Every continuous map from a connected space to $\mathbb{Z}$ is constant.* $\mathbb{Z}$ is discrete, so each $\lbrace n\rbrace$ is clopen, and a connected image must be one point.

That last corollary is the engine of the whole subject. In [Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II) the integer is a winding number. In [Vol. IV](/blog/2026/08/17/circling-the-sphere-Vol-IV) it is the turning number of a curve, and it proves a circle cannot be turned inside out in the plane. In [Vol. V](/blog/2026/08/17/circling-the-sphere-Vol-V) the integer is replaced by an element of a group, and the group turns out to be zero.

---

# paths and path-connectedness
{: #paths-and-path-connectedness}
<div class="ev-def"><strong>Definition (path).</strong> A <em>path</em> in $X$ from $a$ to $b$ is a continuous map $\gamma:[0,1]\to X$ with $\gamma(0)=a$ and $\gamma(1)=b$. $X$ is <em>path-connected</em> if every two points are joined by a path.</div>

Path-connected spaces are connected: a clopen split of $X$ would pull back, along a path joining the two pieces, to a clopen split of $[0,1]$. The converse fails for exotic spaces (the *topologist's sine curve*), but not for anything in this series: for locally path-connected spaces, which include manifolds and the spaces of maps we care about, connected and path-connected agree.

The **path components** of $X$ are its maximal path-connected pieces; the set of them is written $\pi&#95;{0}(X)$. Now the theorem can be restated with no vague words left except "immersion":

$$\text{Smale:}\qquad \pi_0\bigl(\operatorname{Imm}(S^2,\mathbb{R}^3)\bigr)=\{\ast\}.$$

A *point* of this space is an entire immersed sphere. A *path* in it is a movie of immersed spheres, each close to the next in both position and tangent planes. An eversion is a path from $\iota$ to $\alpha$.

---

# compactness, and why immersions have room
{: #compactness-and-why-immersions-have-room}
One more word, because we will use it once in a crucial place.

<div class="ev-def"><strong>Definition (compact).</strong> $K$ is <em>compact</em> if every cover of $K$ by open sets has a finite subcover. In $\mathbb{R}^n$ (Heine–Borel): compact $\iff$ closed and bounded.</div>

$S^2$ is closed and bounded, so compact. The fact we need is: **a continuous real function on a compact space attains its minimum.** Apply it to an immersion $f$, whose tangent vectors $f&#95;{u},f&#95;{v}$ are independent everywhere, so $m=\min\lVert f&#95;{u}\times f&#95;{v}\rVert&gt;0$. The cross product is continuous in the derivatives, so any map $g$ whose derivatives are uniformly close enough to $f$'s (how close depends only on $m$ and on the size of $df$) still has $\lVert g&#95;{u}\times g&#95;{v}\rVert&gt;0$. So every immersion has a ball of immersions around it:

$$\operatorname{Imm}(S^2,\mathbb{R}^3)\ \text{is an open subset of}\ C^1(S^2,\mathbb{R}^3).$$

On a non-compact surface the minimum could be $0$ at infinity and there would be no room. On the sphere there always is. This is the fact that makes wiggling an immersion safe, and wiggling is how every eversion is built.

(The last axiom we need is **Hausdorff**: distinct points have disjoint open neighbourhoods, so limits are unique. Every metric space is Hausdorff. It shows up in the definition of a manifold in Vol. III and nowhere else.)

---

# where this goes
{: #where-this-goes}
We now have the language to ask the question. $\operatorname{Imm}(S^2,\mathbb{R}^3)$ is a topological space. Its path components are what we want to count. The tool for counting path components of spaces of maps is **homotopy**, and the first thing it counts is how many times a loop winds around a hole.

---

**Next:** [Vol. II: Paths and Homotopy](/blog/2026/08/17/circling-the-sphere-Vol-II)

*Sphere Eversion:* **Vol. I** · [Vol. II](/blog/2026/08/17/circling-the-sphere-Vol-II) · [Vol. III](/blog/2026/08/17/circling-the-sphere-Vol-III) · [Vol. IV](/blog/2026/08/17/circling-the-sphere-Vol-IV) · [Vol. V](/blog/2026/08/17/circling-the-sphere-Vol-V) · [Vol. VI](/blog/2026/08/17/circling-the-sphere-Vol-VI)
