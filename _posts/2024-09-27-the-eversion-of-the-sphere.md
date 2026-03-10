---
layout: post
title: "The Eversion of the Sphere"
date: 2024-09-27
---

*A guided ascent from calculus to one of topology's most counter-intuitive theorems.*

---

# Prologue

In 1957, a struggling graduate student named Stephen Smale proved something that most mathematicians believed was impossible: a sphere can be turned inside out through a continuous, smooth deformation --- without ever cutting, tearing, or creasing the surface. The surface is allowed to pass through itself, but at every instant, it must remain a *smooth immersion*.

This result, known as **sphere eversion**, is an *existence proof*. Smale showed that the path exists in an abstract space of immersions; he never exhibited the deformation itself. It took decades before mathematicians constructed explicit eversions --- first Bernard Morin (who was blind) in the 1960s, then William Thurston's elegant corrugation method in the 1990s.

The animated eversion below, passing through the famous **Morin surface** halfway model, shows what the deformation looks like:

<p style="text-align: center;">
  <img src="/blog/assets/2024/eversion/eversion.gif" alt="Sphere eversion animation" style="max-width: 100%;">
</p>

This post will build your understanding from multivariable calculus to the heart of the proof. We assume you know partial derivatives, the chain rule, and basic linear algebra. Everything else, we construct from the ground up.

---

# Part I: The Language of Smooth Maps

## 1.1 What is a Sphere, Really?

In everyday life, a sphere is a rubber ball. In mathematics, we need precision. The **2-sphere** $S^2$ is the set of points in $\mathbb{R}^3$ at unit distance from the origin:

$$S^2 = \{(x, y, z) \in \mathbb{R}^3 : x^2 + y^2 + z^2 = 1\}.$$

But for our purposes, we care less about *where* the sphere sits and more about the sphere as an abstract 2-dimensional surface --- a **manifold**. Every point on $S^2$ has a neighborhood that looks like a patch of $\mathbb{R}^2$. We can cover $S^2$ with coordinate charts (for instance, stereographic projection from the north and south poles), and transitions between overlapping charts are smooth.

A **smooth map** $f: S^2 \to \mathbb{R}^3$ assigns to each point $p \in S^2$ a point $f(p) \in \mathbb{R}^3$. In local coordinates $(u, v)$ on a chart of $S^2$, we can write:

$$f(u, v) = \big(f_1(u,v),\; f_2(u,v),\; f_3(u,v)\big).$$

The standard inclusion $\iota: S^2 \hookrightarrow \mathbb{R}^3$, where each point maps to itself, is the simplest example. But there are many other smooth maps from $S^2$ into $\mathbb{R}^3$ --- stretched, twisted, even self-intersecting.

## 1.2 Immersions: The No-Crease Condition

Not every smooth map is geometrically well-behaved. Consider crushing the entire sphere to a single point --- that's smooth, but it destroys all geometric information. We need a condition that says "the surface never collapses."

**Definition.** A smooth map $f: S^2 \to \mathbb{R}^3$ is an **immersion** if its differential $df_p: T_pS^2 \to T_{f(p)}\mathbb{R}^3$ is injective at every point $p \in S^2$.

In coordinates, this means the **Jacobian matrix** of $f$ has full rank everywhere:

$$J_f(u,v) = \begin{pmatrix} \dfrac{\partial f_1}{\partial u} & \dfrac{\partial f_1}{\partial v} \\[8pt] \dfrac{\partial f_2}{\partial u} & \dfrac{\partial f_2}{\partial v} \\[8pt] \dfrac{\partial f_3}{\partial u} & \dfrac{\partial f_3}{\partial v} \end{pmatrix}$$

This is a $3 \times 2$ matrix. For $f$ to be an immersion, we need $\operatorname{rank}(J_f) = 2$ at every point --- the two columns must be linearly independent. Geometrically, the partial derivatives $\frac{\partial f}{\partial u}$ and $\frac{\partial f}{\partial v}$ span a tangent plane to the image surface at every point.

**What does rank 2 forbid?** It forbids **creases** --- points where the surface folds onto itself so sharply that the tangent plane degenerates into a line or a point. Think of folding a piece of paper: at the fold line, the two sides of the paper share the same tangent *line* rather than spanning a plane. An immersion is allowed to self-intersect (the surface passes through itself), but it must never crease.

**Calculus checkpoint.** If you've computed the tangent plane to a parametric surface $\mathbf{r}(u,v)$ by taking $\mathbf{r}_u \times \mathbf{r}_v$ and checking it's nonzero, you already understand the immersion condition: $\mathbf{r}_u \times \mathbf{r}_v \neq \mathbf{0}$ everywhere is equivalent to $\operatorname{rank}(J_f) = 2$.

**Worked examples.** To build intuition, let's look at curves (one dimension down). A curve $\gamma: \mathbb{R} \to \mathbb{R}^2$ is an immersion if $\gamma'(t) \neq \mathbf{0}$ for all $t$ --- the curve never "stops moving."

- **Figure-eight** $\gamma(t) = (\sin 2t, \sin t)$: This is an immersion. We have $\gamma'(t) = (2\cos 2t, \cos t)$, and you can verify this is never the zero vector. But the curve *crosses itself* at the origin. Self-intersection is fine --- immersion does not mean injective. What it does mean is that at the crossing point, the curve passes through cleanly, with a well-defined tangent direction on each branch.

- **Cusp** $\gamma(t) = (t^2, t^3)$: This is **not** an immersion. At $t=0$, we get $\gamma'(0) = (0, 0) = \mathbf{0}$ --- the velocity vanishes. The curve comes to a sharp point (a cusp). This is exactly the kind of degenerate behavior the immersion condition forbids.

The distinction for surfaces is analogous. An immersed sphere may pass through itself (creating curves of self-intersection), but at every point, the surface has a well-defined tangent *plane*. A non-immersion would have a point where the surface pinches down to a line or a point --- a crease or a cusp.

**Embedding vs. immersion.** An **embedding** is an immersion that is also injective (one-to-one) --- the surface doesn't touch itself at all. The standard sphere $\iota: S^2 \hookrightarrow \mathbb{R}^3$ is an embedding. During an eversion, the intermediate surfaces are immersions but *not* embeddings --- they must pass through themselves. The key constraint is that they remain immersions (no creases), even though they are not embeddings (they self-intersect).

## 1.3 What is Eversion?

The standard embedding $\iota$ maps $S^2$ into $\mathbb{R}^3$ with the "outside" facing outward. The **antipodal map** $\alpha: S^2 \to \mathbb{R}^3$ defined by $\alpha(p) = -p$ gives us the same geometric sphere, but with the orientation reversed --- inside facing out.

**Why does $\alpha$ reverse orientation?** At any point $p$ on the sphere, the outward unit normal is $\mathbf{n}(p) = p$ (pointing away from the origin). Under the antipodal map, the point $p$ goes to $-p$. The differential of $\alpha$ maps each tangent vector $v$ to $-v$, so the cross product of two tangent vectors flips sign:

$$d\alpha(\mathbf{e}_1) \times d\alpha(\mathbf{e}_2) = (-\mathbf{e}_1) \times (-\mathbf{e}_2) = \mathbf{e}_1 \times \mathbf{e}_2$$

Wait --- the cross product of two negated vectors is the *same*? Yes, but the normal relative to the *new* position $-p$ now points inward: the outward normal at $-p$ on the standard sphere is $-p$, but our surface's normal (inherited from $\alpha$) is $+p$, which points *inward* at the new location. The surface has been turned inside out. More precisely, $\alpha$ is an orientation-reversing map because its Jacobian has determinant $(-1)^3 = -1$ (it negates all three coordinates).

An **eversion** is a smooth, continuous path of immersions connecting $\iota$ to $\alpha$. Formally:

**Definition.** A **regular homotopy** between two immersions $f_0, f_1: S^2 \to \mathbb{R}^3$ is a smooth map

$$F: S^2 \times [0,1] \to \mathbb{R}^3$$

such that:
1. $F(\cdot, 0) = f_0$ and $F(\cdot, 1) = f_1$,
2. For every $t \in [0,1]$, the map $f_t = F(\cdot, t): S^2 \to \mathbb{R}^3$ is an immersion.

A sphere eversion is a regular homotopy from $\iota$ to $\alpha$. At every instant $t$, the intermediate surface $f_t(S^2)$ must be a smooth immersion --- self-intersections are allowed, but creases are not.

**"Why can't we just push it through?"** A natural first attempt: push the north pole down through the south pole, like inverting a sock. The problem is that at the moment the north pole passes through the equator, the surface develops a **crease** --- a circle of points where the tangent plane degenerates. The equator becomes a fold line where the surface doubles back on itself, violating the immersion condition. Any "obvious" physical inversion creates creases. The genius of eversion is finding a path that avoids all creases, at the cost of allowing the surface to pass through itself in more subtle ways.

To see why this is hard, note that the immersion condition $\operatorname{rank}(J_f) = 2$ must hold at *every* point and at *every* instant $t \in [0,1]$. That's an infinite family of pointwise conditions. The eversion must thread through this infinite-dimensional needle.

**An analogy from calculus.** Think of the space of all immersions as an infinite-dimensional landscape. Each point in this landscape is a particular immersion $f: S^2 \to \mathbb{R}^3$. A regular homotopy is a *path* in this landscape. Smale's theorem says: the standard sphere $\iota$ and the everted sphere $\alpha$ lie in the same *path-connected component* of this landscape.

<div id="immersion-demo" style="width: 100%; height: 450px; margin: 2em 0; border-radius: 8px; overflow: hidden; background: #0f172a; position: relative;">
  <div style="position: absolute; bottom: 10px; left: 10px; right: 10px; z-index: 10; text-align: center;">
    <label style="color: #94a3b8; font-size: 14px; font-family: monospace;">Deformation parameter t:
      <input type="range" id="immersion-slider" min="0" max="100" value="0" style="width: 60%; margin-left: 10px; vertical-align: middle;">
      <span id="immersion-t-value" style="color: #e2e8f0; margin-left: 8px;">0.00</span>
    </label>
  </div>
</div>

<script>
(function() {
  function initImmersionDemo() {
    if (typeof THREE === 'undefined') {
      setTimeout(initImmersionDemo, 100);
      return;
    }
    const container = document.getElementById('immersion-demo');
    if (!container) return;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0f172a);

    const width = container.clientWidth;
    const height = 450;
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 100);
    camera.position.set(0, 0, 4);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // Sphere geometry
    const segments = 48;
    const geometry = new THREE.SphereGeometry(1, segments, segments);
    const positionAttr = geometry.getAttribute('position');
    const originalPositions = new Float32Array(positionAttr.array);

    const material = new THREE.MeshStandardMaterial({
      color: 0x6366f1,
      metalness: 0.3,
      roughness: 0.5,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.85,
      wireframe: false
    });
    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    // Wireframe overlay
    const wireMat = new THREE.MeshBasicMaterial({
      color: 0xa5b4fc,
      wireframe: true,
      transparent: true,
      opacity: 0.15
    });
    const wireMesh = new THREE.Mesh(geometry, wireMat);
    scene.add(wireMesh);

    // Lights
    scene.add(new THREE.AmbientLight(0xffffff, 0.4));
    const light1 = new THREE.DirectionalLight(0xffffff, 0.8);
    light1.position.set(5, 5, 5);
    scene.add(light1);
    const light2 = new THREE.DirectionalLight(0x818cf8, 0.4);
    light2.position.set(-5, -3, -5);
    scene.add(light2);

    const slider = document.getElementById('immersion-slider');
    const tLabel = document.getElementById('immersion-t-value');
    let t = 0;

    function deformSphere(t) {
      const positions = positionAttr.array;
      for (let i = 0; i < positions.length; i += 3) {
        const ox = originalPositions[i];
        const oy = originalPositions[i+1];
        const oz = originalPositions[i+2];
        const r = Math.sqrt(ox*ox + oy*oy + oz*oz);
        const theta = Math.atan2(Math.sqrt(ox*ox + oy*oy), oz);
        const phi = Math.atan2(oy, ox);

        // Smooth deformation: push the sphere through itself
        // Uses a corrugation-inspired deformation
        const corrugation = Math.sin(3 * theta) * Math.sin(2 * phi);
        const push = t * 2.0 * Math.cos(theta);
        const ripple = t * 0.4 * corrugation;

        const scale = 1.0 + ripple;
        const nx = ox * scale + t * 0.3 * Math.sin(3 * phi) * Math.sin(theta);
        const ny = oy * scale + t * 0.3 * Math.cos(3 * phi) * Math.sin(theta);
        const nz = oz * (1.0 - 2.0 * t) + push * 0.1;

        positions[i] = nx;
        positions[i+1] = ny;
        positions[i+2] = nz;
      }
      positionAttr.needsUpdate = true;
      geometry.computeVertexNormals();
    }

    slider.addEventListener('input', function() {
      t = parseFloat(this.value) / 100;
      tLabel.textContent = t.toFixed(2);
      deformSphere(t);
    });

    let mouseDown = false;
    let lastX = 0, lastY = 0;
    let rotX = 0, rotY = 0;

    container.addEventListener('mousedown', (e) => { mouseDown = true; lastX = e.clientX; lastY = e.clientY; });
    container.addEventListener('mouseup', () => mouseDown = false);
    container.addEventListener('mouseleave', () => mouseDown = false);
    container.addEventListener('mousemove', (e) => {
      if (!mouseDown) return;
      rotY += (e.clientX - lastX) * 0.005;
      rotX += (e.clientY - lastY) * 0.005;
      lastX = e.clientX;
      lastY = e.clientY;
    });

    function animate() {
      requestAnimationFrame(animate);
      mesh.rotation.set(rotX, rotY, 0);
      wireMesh.rotation.set(rotX, rotY, 0);
      renderer.render(scene, camera);
    }

    window.addEventListener('resize', () => {
      const w = container.clientWidth;
      camera.aspect = w / height;
      camera.updateProjectionMatrix();
      renderer.setSize(w, height);
    });

    animate();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initImmersionDemo);
  } else {
    initImmersionDemo();
  }
})();
</script>

*Drag to rotate. Use the slider to deform the sphere --- notice how the surface always remains smooth (no creases), even as it passes through itself.*

---

# Part II: The Space of Immersions

## 2.1 Configuration Space

Here is where the story shifts from individual maps to the *space of all possible maps*. This leap --- from studying objects to studying the space of objects --- is one of the most powerful ideas in modern mathematics.

Let $\operatorname{Imm}(S^2, \mathbb{R}^3)$ denote the space of all $C^2$ immersions of $S^2$ into $\mathbb{R}^3$. Each point in this space is an entire immersion $f: S^2 \to \mathbb{R}^3$. The topology on this space is the $C^1$ uniform topology: two immersions are "close" if they are close in value *and* their first derivatives are close, at every point of $S^2$.

This is an **infinite-dimensional** space. Just as a curve in $\mathbb{R}^3$ can be specified by three functions of one variable, an immersion $f: S^2 \to \mathbb{R}^3$ is specified by three functions of two variables --- and the "dimension" of the function space reflects the infinite degrees of freedom available.

**Analogy from calculus of variations.** In the calculus of variations, you study functionals like

$$\mathcal{L}[y] = \int_a^b L(x, y, y') \, dx$$

where each *function* $y(x)$ is a point in an infinite-dimensional function space. The Euler--Lagrange equation finds critical points of $\mathcal{L}$ in this space. Smale's approach is similar in spirit: he studies the *topology* of a function space (the space of immersions) rather than optimizing a functional on it.

## 2.2 Paths in Configuration Space

A **regular homotopy** $f_t$ with $t \in [0,1]$ is simply a continuous path in $\operatorname{Imm}(S^2, \mathbb{R}^3)$. Two immersions $f$ and $g$ are **regularly homotopic** if they lie in the same path-connected component of $\operatorname{Imm}(S^2, \mathbb{R}^3)$.

**What is a path-connected component?** Take all the points (immersions) in $\operatorname{Imm}(S^2, \mathbb{R}^3)$ and declare two of them equivalent if you can draw a continuous path between them. Each equivalence class is a "path-connected component." If the entire space has only one component, *every* immersion can be deformed into every other --- that's what Smale proves.

Smale's eversion theorem can now be stated with striking simplicity:

> **Theorem (Smale, 1958).** The space $\operatorname{Imm}(S^2, \mathbb{R}^3)$ is path-connected.

That's it. Every immersion of $S^2$ in $\mathbb{R}^3$ can be continuously deformed into every other immersion, through immersions. In particular, the standard embedding $\iota$ and the antipodal embedding $\alpha$ are connected by a path. The sphere can be everted.

## 2.3 Tangential Data and the Stiefel Manifold

To classify immersions, Smale extracted an invariant from the **tangential data** of each immersion. At each point $p \in S^2$, an immersion $f$ determines a 2-frame in $\mathbb{R}^3$: the pair of vectors

$$\left(\frac{\partial f}{\partial u}(p),\; \frac{\partial f}{\partial v}(p)\right)$$

which are linearly independent (by the immersion condition). This pair lives in the **Stiefel manifold**:

$$V_{3,2} = \{(v_1, v_2) \in \mathbb{R}^3 \times \mathbb{R}^3 : v_1, v_2 \text{ linearly independent}\}.$$

**Unpacking the Stiefel manifold.** $V_{3,2}$ is the space of all ordered pairs of linearly independent vectors in $\mathbb{R}^3$. Think of it as the space of all possible "coordinate frames" for a tangent plane sitting inside $\mathbb{R}^3$. Here "ordered" matters: the pair $(\mathbf{e}_1, \mathbf{e}_2)$ is a different point in $V_{3,2}$ from $(\mathbf{e}_2, \mathbf{e}_1)$, because swapping the vectors reverses the orientation of the frame.

**Concrete example.** At the north pole $(0,0,1)$ of the standard sphere, the tangent plane is the $xy$-plane, and the immersion $\iota$ gives us the frame $\left(\frac{\partial \iota}{\partial u}, \frac{\partial \iota}{\partial v}\right) = (\mathbf{e}_1, \mathbf{e}_2)$. At the equator point $(1,0,0)$, the tangent plane is the $yz$-plane, and the frame might be $(\mathbf{e}_2, -\mathbf{e}_3)$. As you move across the sphere, the frame varies continuously --- you get a continuous map $T_\iota: S^2 \to V_{3,2}$.

More precisely, we can normalize to get ordered pairs of *orthonormal* vectors, giving the compact Stiefel manifold $V_{3,2} \cong SO(3)$.

So each immersion $f$ induces a map $T_f: S^2 \to V_{3,2}$ --- the **tangential map** that records the tangent frame at each point. Smale's invariant $\Omega(f, g)$ measures the difference between the tangential maps of two immersions.

## 2.4 The Gauss Map Perspective

There is a closely related and perhaps more intuitive viewpoint. The **Gauss map** of an immersion $f$ is:

$$\mathbf{n}_f(p) = \frac{\frac{\partial f}{\partial u} \times \frac{\partial f}{\partial v}}{\left\|\frac{\partial f}{\partial u} \times \frac{\partial f}{\partial v}\right\|}$$

This assigns to each point $p \in S^2$ the unit normal vector to the image surface at $f(p)$. The Gauss map $\mathbf{n}_f: S^2 \to S^2$ has a **degree** --- the number of times the normal vector wraps around the target sphere.

A classical result states that the degree of the Gauss map equals $1$ for *any* immersion of $S^2$ in $\mathbb{R}^3$. This is reassuring: both the standard sphere (outward normals) and the everted sphere (inward normals, but now on the "outside") have Gauss map degree $1$. The Gauss map degree does not obstruct eversion.

But this is not the whole story --- the Gauss map captures only the normal direction, not the full tangent frame. Smale's invariant $\Omega(f,g)$ is finer, living in the homotopy group $\pi_2(V_{3,2})$.

---

# Part III: The Topology of the Proof

## 3.1 Why Eversion is Surprising

Before diving into Smale's argument, let's understand *why* eversion seems impossible.

**The 1-dimensional analogy.** Consider a circle $S^1$ immersed in $\mathbb{R}^2$. Can we evert it? An immersed circle in the plane has a well-defined **turning number** --- the total number of times the tangent vector winds around as you traverse the curve. The standard circle has turning number $+1$; its reflection has turning number $-1$. The Whitney--Graustein theorem tells us that two immersed curves in $\mathbb{R}^2$ are regularly homotopic if and only if they have the same turning number. Since $+1 \neq -1$, **a circle cannot be everted in the plane**.

**Concrete calculation.** Parametrize the unit circle as $\gamma(t) = (\cos t, \sin t)$ for $t \in [0, 2\pi]$. The unit tangent vector is:

$$\mathbf{T}(t) = \frac{\gamma'(t)}{\|\gamma'(t)\|} = (-\sin t, \cos t).$$

The angle this tangent makes with the $x$-axis is $\theta(t) = t + \pi/2$. As $t$ goes from $0$ to $2\pi$, $\theta$ increases by $2\pi$, so the turning number is $\frac{1}{2\pi}\Delta\theta = +1$.

For the reflected circle $\bar{\gamma}(t) = (\cos t, -\sin t)$ (traversed with opposite orientation), the tangent is $\bar{\mathbf{T}}(t) = (-\sin t, -\cos t)$, with angle $\theta(t) = -(t + \pi/2)$. Now $\theta$ *decreases* by $2\pi$, giving turning number $-1$.

Since turning number is invariant under regular homotopy (it's an integer and varies continuously, so it can't jump), $\gamma$ and $\bar{\gamma}$ can never be connected by a path of immersions.

**Why does this obstruction vanish in one dimension higher?** The turning number for $S^1 \subset \mathbb{R}^2$ lives in $\pi_1(S^1) = \mathbb{Z}$ --- the tangent direction traces a loop in the circle of unit vectors in $\mathbb{R}^2$, and $\mathbb{Z}$ has many distinct elements. For $S^2 \subset \mathbb{R}^3$, the analogous invariant lives in $\pi_2(V_{3,2})$, which turns out to be $0$. The extra dimension provides enough room for the obstruction to disappear.

<div id="turning-number-demo" style="width: 100%; height: 380px; margin: 2em 0; border-radius: 8px; overflow: hidden; background: #0f172a; position: relative;">
  <div style="position: absolute; top: 10px; left: 10px; z-index: 10; color: #94a3b8; font-family: monospace; font-size: 13px;">
    Turning Number Visualization
  </div>
  <div style="position: absolute; bottom: 10px; left: 10px; right: 10px; z-index: 10; text-align: center;">
    <label style="color: #94a3b8; font-size: 13px; font-family: monospace;">
      Curve type:
      <select id="turning-curve-select" style="background: #1e293b; color: #e2e8f0; border: 1px solid #475569; border-radius: 4px; padding: 2px 6px; font-family: monospace; font-size: 13px; margin-left: 6px;">
        <option value="circle">Circle (turning # = +1)</option>
        <option value="reflected">Reflected circle (turning # = -1)</option>
        <option value="figure8">Figure-eight (turning # = 0)</option>
      </select>
    </label>
  </div>
</div>

<script>
(function() {
  function initTurningDemo() {
    if (typeof THREE === 'undefined') {
      setTimeout(initTurningDemo, 100);
      return;
    }
    const container = document.getElementById('turning-number-demo');
    if (!container) return;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0f172a);

    const width = container.clientWidth;
    const height = 380;
    const camera = new THREE.OrthographicCamera(-3, 3, 3 * height / width, -3 * height / width, 0.1, 100);
    camera.position.set(0, 0, 5);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // Curve functions
    const curves = {
      circle: function(t) { return [Math.cos(t), Math.sin(t)]; },
      reflected: function(t) { return [Math.cos(t), -Math.sin(t)]; },
      figure8: function(t) { return [Math.sin(2 * t) * 0.8, Math.sin(t) * 1.2]; }
    };
    const tangents = {
      circle: function(t) { var d = [-Math.sin(t), Math.cos(t)]; var l = Math.sqrt(d[0]*d[0]+d[1]*d[1]); return [d[0]/l, d[1]/l]; },
      reflected: function(t) { var d = [-Math.sin(t), -Math.cos(t)]; var l = Math.sqrt(d[0]*d[0]+d[1]*d[1]); return [d[0]/l, d[1]/l]; },
      figure8: function(t) { var d = [2*Math.cos(2*t)*0.8, Math.cos(t)*1.2]; var l = Math.sqrt(d[0]*d[0]+d[1]*d[1]); return [d[0]/l, d[1]/l]; }
    };

    let curveGroup = new THREE.Group();
    scene.add(curveGroup);

    function buildCurve(type) {
      while (curveGroup.children.length > 0) {
        const child = curveGroup.children[0];
        if (child.geometry) child.geometry.dispose();
        if (child.material) child.material.dispose();
        curveGroup.remove(child);
      }

      const N = 200;
      const curveFn = curves[type];
      const tanFn = tangents[type];

      // Draw the curve
      const pts = [];
      for (let i = 0; i <= N; i++) {
        const t = (i / N) * 2 * Math.PI;
        const p = curveFn(t);
        pts.push(new THREE.Vector3(p[0] - 1.2, p[1], 0));
      }
      const curveGeom = new THREE.BufferGeometry().setFromPoints(pts);
      const curveMat = new THREE.LineBasicMaterial({ color: 0x6366f1, linewidth: 2 });
      curveGroup.add(new THREE.Line(curveGeom, curveMat));

      // Draw tangent arrows along the curve
      const arrowColor = 0x22d3ee;
      for (let i = 0; i < 16; i++) {
        const t = (i / 16) * 2 * Math.PI;
        const p = curveFn(t);
        const d = tanFn(t);
        const origin = new THREE.Vector3(p[0] - 1.2, p[1], 0);
        const dir = new THREE.Vector3(d[0], d[1], 0);
        const arrow = new THREE.ArrowHelper(dir, origin, 0.35, arrowColor, 0.1, 0.06);
        curveGroup.add(arrow);
      }

      // Draw the tangent indicatrix (path of tangent vector tip on unit circle)
      const tanPts = [];
      for (let i = 0; i <= N; i++) {
        const t = (i / N) * 2 * Math.PI;
        const d = tanFn(t);
        tanPts.push(new THREE.Vector3(d[0] + 1.5, d[1], 0));
      }
      const tanGeom = new THREE.BufferGeometry().setFromPoints(tanPts);
      const tanMat = new THREE.LineBasicMaterial({ color: 0xfbbf24 });
      curveGroup.add(new THREE.Line(tanGeom, tanMat));

      // Unit circle for reference
      const refPts = [];
      for (let i = 0; i <= 64; i++) {
        const t = (i / 64) * 2 * Math.PI;
        refPts.push(new THREE.Vector3(Math.cos(t) + 1.5, Math.sin(t), 0));
      }
      const refGeom = new THREE.BufferGeometry().setFromPoints(refPts);
      const refMat = new THREE.LineBasicMaterial({ color: 0x334155 });
      curveGroup.add(new THREE.Line(refGeom, refMat));
    }

    buildCurve('circle');

    document.getElementById('turning-curve-select').addEventListener('change', function() {
      buildCurve(this.value);
    });

    function animate() {
      requestAnimationFrame(animate);
      renderer.render(scene, camera);
    }

    window.addEventListener('resize', () => {
      const w = container.clientWidth;
      camera.right = 3;
      camera.left = -3;
      camera.top = 3 * height / w;
      camera.bottom = -3 * height / w;
      camera.updateProjectionMatrix();
      renderer.setSize(w, height);
    });

    animate();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTurningDemo);
  } else {
    initTurningDemo();
  }
})();
</script>

*Left: the immersed curve with tangent vectors (cyan arrows). Right: the **tangent indicatrix** --- the path traced by the tip of the unit tangent vector on the unit circle (yellow). The turning number is how many times the yellow curve winds around the unit circle. Select different curves to see how turning number changes.*

This is the source of the intuition that eversion should be impossible: in one dimension lower, it *is* impossible. The surprise is that going from $S^1 \subset \mathbb{R}^2$ to $S^2 \subset \mathbb{R}^3$, the obstruction vanishes.

## 3.2 Smale's Classification Theorem

Smale proved a far more general result. Let $V_{n,2}$ be the Stiefel manifold of 2-frames in $\mathbb{R}^n$.

> **Theorem A (Smale, 1958).** Two $C^2$ immersions $f, g: S^2 \to \mathbb{R}^n$ are regularly homotopic if and only if $\Omega(f,g) = 0$ in $\pi_2(V_{n,2})$.
>
> Moreover, for any $\Omega_0 \in \pi_2(V_{n,2})$ and any immersion $f$, there exists an immersion $g$ with $\Omega(f,g) = \Omega_0$.

This establishes a **one-to-one correspondence** between regular homotopy classes of immersions and elements of $\pi_2(V_{n,2})$.

## 3.3 Constructing the Invariant $\Omega(f,g)$

Here is how $\Omega(f,g)$ is defined. Start with two immersions $f$ and $g$ that agree on a neighborhood of some base point $z_0 \in S^2$ (we can always arrange this by a preliminary deformation).

Remove a small disk around $z_0$. On the remaining region (topologically a disk $D$), $f$ and $g$ induce two maps into $V_{n,2}$ that agree on the boundary $\partial D$. Glue these two maps together along $\partial D$ to get a single map:

$$\Phi: S^2 \to V_{n,2}.$$

**Intuition for the gluing.** Think of it this way: $f$ paints the disk $D$ one color pattern in $V_{n,2}$, and $g$ paints the same disk a different color pattern, but they agree on the boundary circle. If you take the disk painted by $f$ as the "northern hemisphere" and the disk painted by $g$ as the "southern hemisphere," and glue them along their shared boundary, you get a sphere mapped into $V_{n,2}$. The homotopy class of this map --- whether it can be shrunk to a point or wraps nontrivially around $V_{n,2}$ --- is the invariant $\Omega(f,g)$. If it can be shrunk to a point ($\Omega = 0$), then $f$ and $g$ are "the same" up to regular homotopy.

The homotopy class $[\Phi] \in \pi_2(V_{n,2})$ is the invariant $\Omega(f,g)$.

## 3.4 The Key Computation: $\pi_2(V_{3,2}) = 0$

For sphere eversion, we need $n = 3$. The classification reduces to computing $\pi_2(V_{3,2})$.

**Step 1.** The Stiefel manifold $V_{3,2}$ is homeomorphic to $SO(3)$, the rotation group of $\mathbb{R}^3$.

**Step 2.** $SO(3)$ is homeomorphic to $\mathbb{RP}^3$ (real projective 3-space). This follows from the quaternion double cover: $SU(2) \cong S^3$ maps onto $SO(3)$ with kernel $\{\pm 1\}$, so $SO(3) \cong S^3 / \{\pm 1\} = \mathbb{RP}^3$.

**What does this mean concretely?** A unit quaternion $q = a + bi + cj + dk$ with $a^2 + b^2 + c^2 + d^2 = 1$ represents a rotation of $\mathbb{R}^3$: the rotation by angle $2\cos^{-1}(a)$ about the axis $(b, c, d)/\|(b,c,d)\|$. But $q$ and $-q$ represent the *same* rotation (negating a quaternion flips both the axis direction and the rotation sense, which cancel out). So each rotation corresponds to a pair $\{q, -q\}$ of antipodal points on $S^3$. The space of such antipodal pairs is exactly $\mathbb{RP}^3 = S^3/\{\pm 1\}$. Hence $SO(3) \cong \mathbb{RP}^3$.

**Step 3.** We compute $\pi_2(\mathbb{RP}^3)$ using the long exact sequence of the double covering $p: S^3 \to \mathbb{RP}^3$ with fiber $S^0 = \{+1, -1\}$:

**What is a long exact sequence?** When one space covers another (like $S^3$ double-covering $\mathbb{RP}^3$), the homotopy groups of the three spaces involved --- the covering space, the base, and the fiber --- are linked by a chain of group homomorphisms. "Exact" means that at each position in the chain, the image of one map equals the kernel of the next. This constraint is so rigid that knowing some of the groups forces the others. In our case, it forces $\pi_2(\mathbb{RP}^3) \cong \pi_2(S^3)$.

The relevant portion of the sequence is:

$$\cdots \to \pi_2(S^0) \to \pi_2(S^3) \to \pi_2(\mathbb{RP}^3) \to \pi_1(S^0) \to \pi_1(S^3) \to \cdots$$

Since $\pi_k(S^0) = 0$ for $k \geq 1$ and $\pi_1(S^3) = 0$:

$$0 \to \pi_2(S^3) \to \pi_2(\mathbb{RP}^3) \to 0$$

so $\pi_2(\mathbb{RP}^3) \cong \pi_2(S^3)$.

**Step 4.** $\pi_2(S^3) = 0$ because every continuous map $S^2 \to S^3$ is homotopic to a constant --- intuitively, a 2-sphere in a 3-sphere has "room" to be contracted to a point (this is a special case of $\pi_k(S^n) = 0$ for $k < n$).

**Intuition for $\pi_k(S^n) = 0$ when $k < n$.** Think of a lower-dimensional analogy: a loop ($S^1$) drawn on the surface of a 2-sphere ($S^2$). No matter how complicated the loop is, you can always shrink it to a point --- that's $\pi_1(S^2) = 0$. The loop never gets "stuck" because the sphere has no holes for it to catch on. Similarly, a 2-sphere ($S^2$) mapped into a 3-sphere ($S^3$) can always be contracted to a point: the 3-sphere is simply connected in every dimension up to 2. The map $S^2 \to S^3$ is like drawing a surface inside a higher-dimensional space that has no "obstacles" at that dimension.

**Conclusion:**

$$\pi_2(V_{3,2}) \cong \pi_2(SO(3)) \cong \pi_2(\mathbb{RP}^3) \cong \pi_2(S^3) = 0.$$

Since $\pi_2(V_{3,2}) = 0$, the invariant $\Omega(f,g)$ is *always* zero. By Theorem A, any two immersions of $S^2$ in $\mathbb{R}^3$ are regularly homotopic. In particular, the standard embedding and its reflection are regularly homotopic.

**The sphere can be everted.**

**A note on what this proof does and does not give us.** The argument above tells us that an eversion *exists*. It does not show us what it looks like. The proof works by showing that the space $\operatorname{Imm}(S^2, \mathbb{R}^3)$ has only one path component (via the vanishing of $\pi_2(V_{3,2})$), so the two immersions must be connected by *some* path --- but the path is never constructed. This is why Smale's result was so astonishing and initially met with disbelief: mathematicians knew the eversion existed but couldn't picture it. It took Morin (1967) and later Thurston (1990s) to find explicit constructions.

## 3.5 The Fiber Bundle Machinery

How did Smale prove Theorem A? The proof is a masterpiece of algebraic topology, using fiber bundles and their homotopy sequences. Here is a roadmap.

**What is a fiber bundle?** Before diving in, let's build some intuition. A **fiber bundle** is a space $E$ (the "total space") that locally looks like a product $B \times F$, where $B$ is the "base space" and $F$ is the "fiber." There's a projection map $\pi: E \to B$ such that for each point $b \in B$, the preimage $\pi^{-1}(b)$ is a copy of the fiber $F$.

**Everyday example.** Consider a cylinder: it's a product $S^1 \times [0,1]$. The base is the circle $S^1$, each fiber is an interval $[0,1]$, and the projection sends each point on the cylinder to the corresponding point on the circle. A Mobius strip is *also* a fiber bundle over $S^1$ with fiber $[0,1]$ --- but it's twisted, so it's not a global product.

**In Smale's context:** The total space $E$ is the space of immersions of a disk. The base space $B$ records what happens on the boundary (boundary data). The fiber $\pi^{-1}(b)$ over a particular boundary condition $b$ consists of all immersions that match that boundary data. The question "are two immersions regularly homotopic?" reduces to asking whether they lie in the same path-component of a fiber.

**What is the Covering Homotopy Property (CHP)?** If $(E, \pi, B)$ has the CHP (also called being a "fibration"), it means: if you have a path in the base space $B$ and a starting point in $E$ above the path's start, you can "lift" the entire path to $E$. In Smale's setting, this means: if you continuously deform the boundary data, you can continuously deform the immersion to match. This is the key technical property that lets Smale relate questions about immersions to questions about homotopy groups.

Smale constructs a tower of function spaces:

| Space | Description |
|-------|-------------|
| $E$ | Regular maps of disk $D$ into $\mathbb{R}^n$, with $C^1$ topology |
| $B$ | Boundary data: maps from $\partial D$ into $V_{n,2} \times \mathbb{R}^n$ |
| $\pi: E \to B$ | Restriction to boundary |
| $E_0, B_0$ | Subspaces with fixed base point $x_0$ |
| $E', B_0'$ | Auxiliary spaces of maps $(D, p_0) \to (V, x_0)$ |

The key results in the proof chain are:

1. **Theorem 2.1:** $(E, \pi, B)$ has the **Covering Homotopy Property** (CHP) --- it's a fibration. This means homotopies in the base space $B$ can be "lifted" to homotopies in the total space $E$.

2. **Lemma 3.2:** The auxiliary space $E'$ is **contractible** (via the homotopy $H_t(f)(p) = f(h_t(p))$ where $h_t$ contracts $D$ to a point).

3. **Lemma 3.3:** $\pi_k(E_0) = 0$ for all $k \geq 0$ --- the space of immersions of a disk with fixed boundary data has trivial homotopy groups.

4. **Theorem 3.7:** The map $\phi_0: \Gamma_c \to \Omega_d$ between fibers is a **weak homotopy equivalence**.

5. **Lemma 3.8:** $\pi_k(\Omega_d) = \pi_{k+2}(V_{n,2})$ --- this connects the homotopy of the fibers to the homotopy of the Stiefel manifold.

6. **Theorem 3.9:** Combining everything: $\pi_k(\Gamma_c) = \pi_{k+2}(V_{n,2})$. For $k=0$: the set of path components of the fiber $\Gamma_c$ is in bijection with $\pi_2(V_{n,2})$.

This is the bridge: the topology of the fiber (which controls whether two immersions with the same boundary data are regularly homotopic) is captured by the homotopy group $\pi_2(V_{n,2})$.

## 3.6 Contrast: $S^2$ in $\mathbb{R}^4$

The magic of $\pi_2(V_{3,2}) = 0$ is specific to codimension 1. For $n = 4$:

$$\pi_2(V_{4,2}) \cong \mathbb{Z}.$$

This means there are **infinitely many** distinct regular homotopy classes of immersions $S^2 \to \mathbb{R}^4$, indexed by the integers. Smale's Theorem C relates these classes to the characteristic class of the normal bundle, which for $S^2$ in $\mathbb{R}^4$ equals twice the algebraic self-intersection number of the immersion. Two immersions are regularly homotopic if and only if they have the same algebraic self-intersection number.

---

# Part IV: Making it Concrete

## 4.1 Thurston's Corrugation Method

Smale's proof is pure existence --- it gives no recipe for constructing an eversion. The first *explicit* eversions were found by Bernard Morin. But the most conceptually transparent method is **Thurston's corrugation technique** (1990s).

The idea: introduce waves (corrugations) into the surface that create enough "slack" to push the sphere through itself. The corrugations are like the pleats in a skirt --- they add local complexity but allow global rearrangement.

**Intuition: why corrugations help.** Imagine trying to turn a rubber glove inside out, but the glove is rigid. You can't do it. Now imagine the glove is made of an accordion-pleated material --- the pleats let different parts of the surface slide past each other without creating creases. Corrugation works the same way: by adding high-frequency waves to the sphere, you create local "slack" that gives the surface freedom to rearrange globally. The waves are always smooth (satisfying the immersion condition), and their amplitude can be tuned continuously.

The procedure, at a high level:
1. **Start** with the standard sphere.
2. **Corrugation phase:** Introduce sinusoidal waves along the surface. The surface develops flower-like "petals" --- regions that bulge outward and inward in an alternating pattern. The frequency $k$ is chosen high enough that the petals have room to interleave.
3. **Interleaving phase:** The petals from the "outward" side and the "inward" side are pushed past each other. Because they are narrow corrugations (high frequency), they can slide through without ever creating a crease. This is the key step --- it's where the surface passes through itself.
4. **De-corrugation phase:** Smoothly reduce the corrugation amplitude back to zero, arriving at the everted sphere.

Each of these phases is a smooth deformation, and the composition is a regular homotopy.

The corrugation function modifies the immersion by adding oscillatory terms:

$$f_{\text{corr}}(u, v) = f(u, v) + \epsilon(t) \cdot \mathbf{n}(u,v) \cdot \sin(k \cdot u)$$

where $\mathbf{n}$ is the normal, $k$ controls the frequency of corrugations, and $\epsilon(t)$ is an amplitude that varies during the homotopy.

## 4.2 The Morin Surface

The **Morin surface** is the halfway model of a sphere eversion --- the self-intersecting surface at $t = 0.5$. It has a beautiful four-fold symmetry and a single quadruple point (where four sheets of the surface meet).

<div id="morin-demo" style="width: 100%; height: 500px; margin: 2em 0; border-radius: 8px; overflow: hidden; background: #0f172a; position: relative;">
  <div style="position: absolute; top: 10px; left: 10px; z-index: 10; color: #94a3b8; font-family: monospace; font-size: 13px;">
    Morin Surface &mdash; drag to rotate
  </div>
</div>

<script>
(function() {
  function initMorinDemo() {
    if (typeof THREE === 'undefined') {
      setTimeout(initMorinDemo, 100);
      return;
    }
    const container = document.getElementById('morin-demo');
    if (!container) return;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0f172a);

    const width = container.clientWidth;
    const height = 500;
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 100);
    camera.position.set(0, 1.5, 4.5);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // Morin surface parametrization (Boy's surface variant)
    // Using Apery's parametrization of Boy's surface
    const uSegments = 80;
    const vSegments = 80;
    const geometry = new THREE.BufferGeometry();
    const vertices = [];
    const indices = [];
    const normals = [];

    for (let i = 0; i <= uSegments; i++) {
      for (let j = 0; j <= vSegments; j++) {
        const u = (i / uSegments) * Math.PI;
        const v = (j / vSegments) * 2 * Math.PI;

        // Morin surface approximation using a modified Boy's surface
        const su = Math.sin(u);
        const cu = Math.cos(u);
        const sv = Math.sin(v);
        const cv = Math.cos(v);
        const s2v = Math.sin(2 * v);
        const c2v = Math.cos(2 * v);
        const s3v = Math.sin(3 * v);
        const c3v = Math.cos(3 * v);
        const su2 = su * su;

        // Modified parametrization for Morin-like surface
        const a = su * cv;
        const b = su * sv;
        const c = cu;

        const x = (2 * a * a - b * b - c * c + 2 * b * c * (b * b - c * c) + a * c * (c * c - b * b) + a * b * (b * b - c * c)) * 0.7;
        const y = (su2 * s2v / 2 + cu * su * (c3v * 0.5 + 0.5)) * 1.2;
        const z = (su * cu * cv + su2 * sv * cv * 0.5 - su2 * 0.3 * c2v) * 1.2;

        vertices.push(x, y, z);
        normals.push(0, 0, 1); // placeholder, will compute
      }
    }

    for (let i = 0; i < uSegments; i++) {
      for (let j = 0; j < vSegments; j++) {
        const a = i * (vSegments + 1) + j;
        const b = a + 1;
        const c = a + (vSegments + 1);
        const d = c + 1;
        indices.push(a, b, d);
        indices.push(a, d, c);
      }
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    geometry.setIndex(indices);
    geometry.computeVertexNormals();

    const material = new THREE.MeshStandardMaterial({
      color: 0xec4899,
      metalness: 0.4,
      roughness: 0.4,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.8
    });
    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    // Wireframe
    const wireMat = new THREE.MeshBasicMaterial({
      color: 0xfb7185,
      wireframe: true,
      transparent: true,
      opacity: 0.08
    });
    scene.add(new THREE.Mesh(geometry, wireMat));

    // Lights
    scene.add(new THREE.AmbientLight(0xffffff, 0.5));
    const dl1 = new THREE.DirectionalLight(0xffffff, 0.9);
    dl1.position.set(5, 5, 5);
    scene.add(dl1);
    const dl2 = new THREE.DirectionalLight(0xec4899, 0.3);
    dl2.position.set(-5, -3, -5);
    scene.add(dl2);

    // Mouse interaction
    let mouseDown = false, lastX = 0, lastY = 0, rotX = 0.3, rotY = 0;
    container.addEventListener('mousedown', (e) => { mouseDown = true; lastX = e.clientX; lastY = e.clientY; });
    container.addEventListener('mouseup', () => mouseDown = false);
    container.addEventListener('mouseleave', () => mouseDown = false);
    container.addEventListener('mousemove', (e) => {
      if (!mouseDown) return;
      rotY += (e.clientX - lastX) * 0.005;
      rotX += (e.clientY - lastY) * 0.005;
      lastX = e.clientX;
      lastY = e.clientY;
    });

    function animate() {
      requestAnimationFrame(animate);
      if (!mouseDown) rotY += 0.003;
      mesh.rotation.set(rotX, rotY, 0);
      renderer.render(scene, camera);
    }

    window.addEventListener('resize', () => {
      const w = container.clientWidth;
      camera.aspect = w / height;
      camera.updateProjectionMatrix();
      renderer.setSize(w, height);
    });

    animate();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMorinDemo);
  } else {
    initMorinDemo();
  }
})();
</script>

*The Morin surface: a self-intersecting immersion of $S^2$ that serves as the "halfway point" of a sphere eversion. Drag to rotate.*

## 4.3 The Synchronicity Function

To track the progress of an eversion quantitatively, we define a **synchronicity function**. Let $f_t$ be a regular homotopy from $\iota$ (standard sphere) to $\alpha$ (everted sphere). Define:

$$S(t) = \int_{S^2} \mathbf{n}_{\text{initial}}(p) \cdot \mathbf{n}_t(p) \, dA$$

where $\mathbf{n}_{\text{initial}}(p)$ is the outward unit normal of the standard sphere at $p$, $\mathbf{n}_t(p)$ is the unit normal of the immersion $f_t$ at $p$, and $dA$ is the area element on $S^2$.

**Interpretation:**
- At $t = 0$: normals align perfectly, so $S(0) = \int_{S^2} 1 \, dA = 4\pi$.
- At $t = 1$: normals are reversed, so $S(1) = \int_{S^2} (-1) \, dA = -4\pi$.
- $S(t) = 0$ at some intermediate time: this is where the surface is, on average, "half everted."

The synchronicity function must be continuous (since $f_t$ varies continuously) and must cross zero --- by the Intermediate Value Theorem! The halfway point $S(t^*) = 0$ corresponds roughly to the Morin surface.

Notice the elegant interplay: we used the **Intermediate Value Theorem** --- a tool from freshman calculus --- to say something meaningful about a process happening in an infinite-dimensional function space.

## 4.4 Stationary Points and Geometric Flows

One can also study the eversion through the lens of **geometric flows** on the space of immersions. Consider a functional like the **Willmore energy**:

$$W[f] = \int_{S^2} H^2 \, dA$$

where $H$ is the mean curvature. The Willmore flow

$$\frac{\partial f}{\partial t} = -\nabla W[f]$$

drives the surface toward a minimum of the Willmore energy (a round sphere). Stationary points of $W$ --- surfaces where $\nabla W = 0$ --- are called **Willmore surfaces**.

While the Willmore flow does not directly produce an eversion (it's a gradient flow that seeks minima, not a path between two configurations), it illustrates the general principle: one can study dynamics on $\operatorname{Imm}(S^2, \mathbb{R}^3)$ by defining energy functionals and studying their critical points and flow lines, exactly as in the calculus of variations.

---

# Part V: Homotopy Groups --- A Primer

For readers who want a deeper understanding of the algebraic machinery, here is a self-contained introduction to the homotopy groups that power Smale's proof.

## 5.1 What are Homotopy Groups?

Homotopy groups $\pi_n(X)$ are algebraic invariants that measure the "holes" in a topological space $X$ at different dimensions.

**$\pi_0(X)$** counts the **path-connected components** of $X$. If $\pi_0(X)$ has one element, the space is connected.

**$\pi_1(X)$** is the **fundamental group**: it classifies loops in $X$ up to continuous deformation. For $S^2$, $\pi_1(S^2) = 0$ --- every loop on a sphere can be shrunk to a point (there are no holes for a loop to "catch" on).

**$\pi_2(X)$** classifies maps from $S^2$ into $X$ up to homotopy. It measures "2-dimensional holes." For example, $\pi_2(S^2) = \mathbb{Z}$ --- the integer records how many times the map wraps $S^2$ around the target $S^2$ (the **degree**).

The pattern: $\pi_n(X)$ classifies maps $S^n \to X$ up to homotopy, detecting $n$-dimensional holes.

## 5.2 Isomorphism and Homeomorphism

When we write $\pi_2(SO(3)) \cong \pi_2(\mathbb{RP}^3)$, the $\cong$ denotes a **group isomorphism** --- a structure-preserving bijection. Two groups are isomorphic when they have identical algebraic structure.

This isomorphism holds because $SO(3)$ and $\mathbb{RP}^3$ are **homeomorphic** --- there exists a continuous bijection between them with continuous inverse. A homeomorphism preserves all topological properties, including all homotopy groups.

## 5.3 The Chain of Isomorphisms

Let's trace through the computation $\pi_2(V_{3,2}) = 0$ one more time, emphasizing *why* each step works:

$$\pi_2(V_{3,2}) \cong \pi_2(SO(3))$$

because $V_{3,2} \cong SO(3)$ (a 2-frame determines a rotation; conversely, a rotation determines a 2-frame).

$$\pi_2(SO(3)) \cong \pi_2(\mathbb{RP}^3)$$

because $SO(3) \cong S^3/\{\pm 1\} = \mathbb{RP}^3$ via the quaternion covering.

$$\pi_2(\mathbb{RP}^3) \cong \pi_2(S^3)$$

from the long exact sequence of the double cover $S^3 \to \mathbb{RP}^3$.

$$\pi_2(S^3) = 0$$

because $\pi_k(S^n) = 0$ for $k < n$: there is "not enough room" for a $k$-sphere to wrap nontrivially around an $n$-sphere when $k < n$.

**Therefore:** $\pi_2(V_{3,2}) = 0$, and the space of immersions $\operatorname{Imm}(S^2, \mathbb{R}^3)$ has only one path component. Every pair of immersions is regularly homotopic. The eversion exists.

---

# Epilogue

Let's step back and appreciate the logical arc:

1. **Calculus** gave us the language: smooth maps, Jacobians, the rank condition for immersions.
2. **Function spaces** gave us the framework: the space $\operatorname{Imm}(S^2, \mathbb{R}^3)$, paths in infinite-dimensional spaces.
3. **Algebraic topology** gave us the tool: homotopy groups, fiber bundles, covering spaces.
4. **A single computation** --- $\pi_2(V_{3,2}) = 0$ --- gave us the answer.

The eversion of the sphere is not a trick. It is a theorem that reveals deep structure in the topology of function spaces. The fact that this structure is encoded in a single homotopy group, computable through a chain of standard isomorphisms, is one of the most beautiful confluences in modern mathematics.

Smale's proof tells us the path exists. Morin showed us what it looks like. Thurston showed us how to construct it. And now, perhaps, you can see *why* it must be so.

For further exploration of tangent bundles, differential geometry, and related topics, see my companion post: [Differential Topology Q&A with Phi3](https://juleshenry.github.io/blog/2024/05/22/sphere-eversion-phi3-notes-I#what-is-a-tangent-bundle).

---

# Further Reading

- S. Smale, *A Classification of Immersions of the Two-Sphere*, Transactions of the AMS, 1958.
- V. Guillemin and A. Pollack, *Differential Topology*, AMS Chelsea Publishing.
- S. Levy, D. Maxwell, T. Munzner, *Outside In* (video), The Geometry Center, 1994.
- J. M. Sullivan, G. Francis, S. Levy, *The Optiverse*, 1998.
- S.-S. Chern and E. Spanier, *A Theorem on Orientable Surfaces in Four-Dimensional Space*.
- R. L. Cohen, *Immersions of Manifolds and Homotopy Theory*.
- S. Gudmundsson, *An Introduction to Riemannian Geometry*.
