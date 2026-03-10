---
layout: post
title: "✨ On Multiplication"
date: 2025-12-19
mathjax: true
---

# Intro

For centuries, multiplying two $n$-digit numbers meant performing $n^2$ single-digit multiplications. In 1960, the great Andrey Kolmogorov conjectured that this quadratic cost was an inescapable law of arithmetic. Within a week, a 23-year-old student named Anatoly Karatsuba proved him wrong.

This post traces the arc from schoolbook multiplication through the algorithms that successively shattered the $O(n^2)$ barrier: Karatsuba's $O(n^{1.585})$ divide-and-conquer trick, the polynomial interpolation of Toom-Cook, the Fourier-analytic machinery of Schönhage-Strassen, and finally the 2019 result of Harvey and van der Hoeven achieving the conjectured floor of $O(n \log n)$. We close by examining the deep structural parallel between multiplication and sorting -- both saturate the same information-theoretic bound.

A caveat: in practice, these faster algorithms only overtake schoolbook multiplication at enormous scales. The Harvey-Hoeven algorithm's crossover point lies somewhere beyond $2^{1729^{12}}$ digits -- a number so large it cannot be written down even if every atom in the observable universe were an ink molecule. These are "galactic algorithms," beautiful and useless in equal measure. But their existence reveals something profound about the structure of computation itself.

# Schoolbook Multiplication: Fundamentally $O(n^2)$

To understand why we are traditionally tethered to $O(n^2)$, let us cast our minds back to the elementary school chalkboard. When we multiply two $n$-digit integers—say, $A$ and $B$—we are essentially performing a series of repetitive, granular tasks that scale quadratically with the input size.
## The Anatomy of the Partial Product

First, consider the "multiplication phase." We take the first digit of the multiplier ($B$) and multiply it by every single digit of the multiplicand ($A$). If both numbers have $n$ digits, this initial step requires $n$ individual single-digit multiplications.

Now, we must repeat this process for the second digit of $B$, then the third, and so on, until we have exhausted all $n$ digits of the multiplier. Mathematically, we are performing $n$ sets of $n$ multiplications. This gives us $n \times n$, or $n^2$ fundamental operations.
## The Cost of Alignment and Addition

Once we have generated these $n$ rows of partial products, the work is not yet finished. We must then perform the "addition phase." Each row is shifted to the left—a symbolic representation of multiplying by powers of 10—and then summed together.

- Each partial product can have up to $n+1$ digits.
- We are summing $n$ such rows.
- The total number of additions required to collapse these rows into a final product also scales with $n^2$.

## The Quadratic Ceiling

In the lexicon of Big O notation, we ignore the smaller constants and focus on the dominant growth factor. While you might perform some clever carries or skip a few zeros, the fundamental structure of the algorithm remains a nested loop: for every digit in the bottom number, you must visit every digit in the top number.
$$
\sum_{i=1}^{n}\sum_{j=1}^{n} \big(A_j \times B_i\big) \;\Longrightarrow\; O(n^2)
$$

Thus, the "schoolbook" method represents a rigid, two-dimensional grid of operations. To break the $O(n^2)$ barrier, as Harvey and van der Hoeven have done, one must move beyond this grid entirely—treating integers not as mere strings of digits, but as polynomials or points in a complex plane.

# Karatsuba: Breaking $O(n^2)$ with $O(n^{\log_2 3})$

Kolmogorov organized a seminar in 1960 specifically to prove that $O(n^2)$ was the floor for multiplication. He was wrong. A 23-year-old student named **Anatoly Karatsuba** attended that seminar and, within a week, returned with a counterexample that reduced the exponent from 2 to $\log_2 3 \approx 1.585$.

The idea is pure divide-and-conquer, but with an algebraic twist that turns four sub-multiplications into three.

### Splitting the Numbers

Take two $n$-digit numbers $x$ and $y$. Cut each in half at position $m = \lfloor n/2 \rfloor$, writing them as a "high part" times a power of the base plus a "low part":

$$
\begin{aligned}
x &= x_1 B^m + x_0 \\
y &= y_1 B^m + y_0
\end{aligned}
$$

Concretely: if $x = 1234$ in base 10, then $x_1 = 12$, $x_0 = 34$, and $m = 2$.

Expanding the product naively gives:

$$
xy = x_1 y_1 \cdot B^{2m} + (x_1 y_0 + x_0 y_1) \cdot B^m + x_0 y_0
$$

This expression requires **four** half-size multiplications: $x_1 y_1$, $x_1 y_0$, $x_0 y_1$, and $x_0 y_0$. Four recursive calls on inputs of size $n/2$ gives recurrence $T(n) = 4T(n/2) + O(n)$, which solves to $O(n^2)$ by the Master Theorem -- no improvement at all.

### The Trick: Three Multiplications Suffice

Karatsuba's insight is that we never need the cross-terms $x_1 y_0$ and $x_0 y_1$ individually. We only need their **sum**. And that sum falls out for free from a single cleverly chosen multiplication.

Define three products:

$$
\begin{aligned}
z_2 &= x_1 \cdot y_1 \\
z_0 &= x_0 \cdot y_0 \\
z_1 &= (x_1 + x_0)(y_1 + y_0) - z_2 - z_0
\end{aligned}
$$

Expand $z_1$ to see why this works:

$$
(x_1 + x_0)(y_1 + y_0) = \underbrace{x_1 y_1}_{z_2} + x_1 y_0 + x_0 y_1 + \underbrace{x_0 y_0}_{z_0}
$$

Subtracting $z_2$ and $z_0$ cancels the terms we already know, leaving exactly the cross-term sum $x_1 y_0 + x_0 y_1$. We have extracted the middle coefficient using **one** multiplication and **two** subtractions -- operations that cost only $O(n)$, negligible compared to multiplication.

The final product assembles as:

$$
xy = z_2 \cdot B^{2m} + z_1 \cdot B^m + z_0
$$

Three multiplications. Not four. At every level of the recursion, we save 25% of the multiplicative work, and that savings compounds exponentially as we recurse deeper.

### The Payoff

The recurrence is now $T(n) = 3T(n/2) + O(n)$, and the Master Theorem gives:

| Method        | Recurrence                     | Complexity                              |
|---------------|--------------------------------|-----------------------------------------|
| Schoolbook    | $T(n)=4T(n/2)+O(n)$           | $O(n^{\log_2 4}) = O(n^2)$             |
| Karatsuba     | $T(n)=3T(n/2)+O(n)$           | $O(n^{\log_2 3}) \approx O(n^{1.585})$ |

The gap between $n^2$ and $n^{1.585}$ may look modest for small $n$, but it widens relentlessly. At 1,000 digits the schoolbook method performs $\sim 10^6$ primitive multiplications; Karatsuba performs $\sim 10^{4.75} \approx 56{,}000$ -- a 17$\times$ speedup. At 10,000 digits the ratio exceeds 100$\times$. The deeper the recursion, the more the saved quarter compounds.

The interactive visualization below shows the heart of the trick: how four multiplication blocks collapse into three.

<div id="karatsuba-viz" style="width: 100%; height: 520px; margin: 2em 0; border-radius: 8px; overflow: hidden; background: #0f172a; position: relative;">
  <div id="karatsuba-phase-label" style="position: absolute; top: 16px; left: 50%; transform: translateX(-50%); color: #e2e8f0; font-family: monospace; font-size: 15px; z-index: 10; pointer-events: none; text-align: center; white-space: nowrap;"></div>
  <div id="karatsuba-count-label" style="position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%); color: #94a3b8; font-family: monospace; font-size: 13px; z-index: 10; pointer-events: none; text-align: center;"></div>
</div>

<script>
(function() {
  function initKaratsuba() {
    if (typeof THREE === 'undefined') { setTimeout(initKaratsuba, 100); return; }

    var container = document.getElementById('karatsuba-viz');
    if (!container) return;

    var phaseLabel = document.getElementById('karatsuba-phase-label');
    var countLabel = document.getElementById('karatsuba-count-label');

    // --- Scene setup ---
    var scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0f172a);

    var W = container.clientWidth, H = 520;
    var camera = new THREE.PerspectiveCamera(50, W / H, 0.1, 100);
    camera.position.set(0, 2.5, 7.5);
    camera.lookAt(0, 0, 0);

    var renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(W, H);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // --- Lights ---
    scene.add(new THREE.AmbientLight(0xffffff, 0.45));
    var dLight = new THREE.DirectionalLight(0xffffff, 0.9);
    dLight.position.set(4, 6, 5);
    scene.add(dLight);
    var dLight2 = new THREE.DirectionalLight(0x6366f1, 0.35);
    dLight2.position.set(-4, -3, -4);
    scene.add(dLight2);

    // --- Colors ---
    var COL_Z2    = 0x6366f1; // indigo — z2 = x1*y1
    var COL_CROSS = 0xf59e0b; // amber  — cross terms
    var COL_Z0    = 0x22c55e; // green  — z0 = x0*y0
    var COL_Z1    = 0xa855f7; // purple — z1 (merged)
    var COL_SUB   = 0xef4444; // red    — subtraction blocks
    var COL_GHOST = 0x334155; // slate  — ghost/fading

    // --- Helper: create labeled block ---
    function makeBlock(w, h, d, color) {
      var geo = new THREE.BoxGeometry(w, h, d);
      var mat = new THREE.MeshStandardMaterial({
        color: color, metalness: 0.35, roughness: 0.55, transparent: true, opacity: 1.0
      });
      var mesh = new THREE.Mesh(geo, mat);
      return mesh;
    }

    // --- Helper: create text sprite ---
    function makeLabel(text, fontSize) {
      var canvas = document.createElement('canvas');
      var sz = fontSize || 48;
      canvas.width = 512; canvas.height = 128;
      var ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, 512, 128);
      ctx.fillStyle = '#e2e8f0';
      ctx.font = 'bold ' + sz + 'px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(text, 256, 64);
      var tex = new THREE.CanvasTexture(canvas);
      tex.minFilter = THREE.LinearFilter;
      var spriteMat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity: 1.0 });
      var sprite = new THREE.Sprite(spriteMat);
      sprite.scale.set(2.2, 0.55, 1);
      return sprite;
    }

    // --- Block dimensions ---
    var BW = 1.3, BH = 0.9, BD = 0.8;
    var GAP = 0.3;

    // --- Phase 1: Four schoolbook blocks (2x2 grid) ---
    var b_x1y1 = makeBlock(BW, BH, BD, COL_Z2);
    var b_x1y0 = makeBlock(BW, BH, BD, COL_CROSS);
    var b_x0y1 = makeBlock(BW, BH, BD, COL_CROSS);
    var b_x0y0 = makeBlock(BW, BH, BD, COL_Z0);

    // grid positions (centered)
    var gx = (BW + GAP) * 0.55;
    var gy = (BH + GAP) * 0.55;
    b_x1y1.position.set(-gx,  gy, 0);
    b_x1y0.position.set( gx,  gy, 0);
    b_x0y1.position.set(-gx, -gy, 0);
    b_x0y0.position.set( gx, -gy, 0);

    // labels for each block
    var l_x1y1 = makeLabel('x\u2081y\u2081');
    var l_x1y0 = makeLabel('x\u2081y\u2080');
    var l_x0y1 = makeLabel('x\u2080y\u2081');
    var l_x0y0 = makeLabel('x\u2080y\u2080');

    l_x1y1.position.set(0, 0, BD / 2 + 0.15);
    l_x1y0.position.set(0, 0, BD / 2 + 0.15);
    l_x0y1.position.set(0, 0, BD / 2 + 0.15);
    l_x0y0.position.set(0, 0, BD / 2 + 0.15);

    b_x1y1.add(l_x1y1);
    b_x1y0.add(l_x1y0);
    b_x0y1.add(l_x0y1);
    b_x0y0.add(l_x0y0);

    scene.add(b_x1y1); scene.add(b_x1y0);
    scene.add(b_x0y1); scene.add(b_x0y0);

    // --- Phase 2: Karatsuba merged block (z1) ---
    var b_z1 = makeBlock(BW, BH, BD, COL_Z1);
    var l_z1 = makeLabel('z\u2081', 40);
    l_z1.position.set(0, 0, BD / 2 + 0.15);
    b_z1.add(l_z1);
    b_z1.material.opacity = 0;
    b_z1.position.set(0, gy, 0); // will appear between the cross-term positions
    scene.add(b_z1);

    // Small subtraction indicators
    var subSize = 0.45;
    var b_subZ2 = makeBlock(subSize, subSize, subSize, COL_SUB);
    var l_subZ2 = makeLabel('-z\u2082', 36);
    l_subZ2.position.set(0, 0, subSize / 2 + 0.1);
    b_subZ2.add(l_subZ2);
    b_subZ2.material.opacity = 0;
    l_subZ2.material.opacity = 0;

    var b_subZ0 = makeBlock(subSize, subSize, subSize, COL_SUB);
    var l_subZ0 = makeLabel('-z\u2080', 36);
    l_subZ0.position.set(0, 0, subSize / 2 + 0.1);
    b_subZ0.add(l_subZ0);
    b_subZ0.material.opacity = 0;
    l_subZ0.material.opacity = 0;

    b_subZ2.position.set(-0.5, gy - BH * 0.7, 0.5);
    b_subZ0.position.set(0.5, gy - BH * 0.7, 0.5);
    scene.add(b_subZ2); scene.add(b_subZ0);

    // --- Phase 3: Final result labels ---
    var l_z2_final = makeLabel('z\u2082', 44);
    l_z2_final.material.opacity = 0;
    var l_z0_final = makeLabel('z\u2080', 44);
    l_z0_final.material.opacity = 0;

    // --- Easing ---
    function easeInOutCubic(t) {
      return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    function lerp(a, b, t) { return a + (b - a) * t; }

    // --- Animation state ---
    var PHASE_DURATION = 3.0;   // seconds per phase
    var PAUSE_DURATION = 1.5;   // pause between phases
    var TOTAL_CYCLE = PHASE_DURATION * 3 + PAUSE_DURATION * 4; // 3 phases + 4 pauses (before, between, after)
    var clock = new THREE.Clock();
    var elapsed = 0;

    // --- Target positions for phase 3 (horizontal row) ---
    var ROW_SPACING = BW + GAP + 0.2;
    var finalZ2pos = { x: -ROW_SPACING, y: 0, z: 0 };
    var finalZ1pos = { x: 0,            y: 0, z: 0 };
    var finalZ0pos = { x:  ROW_SPACING, y: 0, z: 0 };

    // Store initial positions for reset
    var init_x1y1 = b_x1y1.position.clone();
    var init_x1y0 = b_x1y0.position.clone();
    var init_x0y1 = b_x0y1.position.clone();
    var init_x0y0 = b_x0y0.position.clone();

    function animate() {
      requestAnimationFrame(animate);
      var dt = clock.getDelta();
      elapsed += dt;

      var cycleT = elapsed % TOTAL_CYCLE;
      var t, e;

      // Phase timeline:
      // [0, PAUSE] -> pause (show 4 blocks)
      // [PAUSE, PAUSE+DUR] -> phase 1: merge cross-terms
      // [PAUSE+DUR, 2*PAUSE+DUR] -> pause
      // [2*PAUSE+DUR, 2*PAUSE+2*DUR] -> phase 2: rearrange to row
      // [2*PAUSE+2*DUR, 3*PAUSE+2*DUR] -> pause
      // [3*PAUSE+2*DUR, 3*PAUSE+3*DUR] -> phase 3: reset
      // [3*PAUSE+3*DUR, 4*PAUSE+3*DUR] -> pause

      var P = PAUSE_DURATION, D = PHASE_DURATION;
      var t0 = P;
      var t1 = P + D;
      var t2 = 2 * P + D;
      var t3 = 2 * P + 2 * D;
      var t4 = 3 * P + 2 * D;
      var t5 = 3 * P + 3 * D;

      if (cycleT < t0) {
        // --- Initial pause: show 4 blocks in grid ---
        resetToPhase0();
        phaseLabel.textContent = 'Schoolbook: 4 multiplications';
        countLabel.textContent = 'x\u2081y\u2081 \u00B7 x\u2081y\u2080 \u00B7 x\u2080y\u2081 \u00B7 x\u2080y\u2080';

      } else if (cycleT < t1) {
        // --- Phase 1: merge cross-terms into z1 ---
        t = (cycleT - t0) / D;
        e = easeInOutCubic(t);

        phaseLabel.textContent = 'Karatsuba\'s trick: merge the cross-terms';
        countLabel.textContent = '(x\u2081+x\u2080)(y\u2081+y\u2080) - z\u2082 - z\u2080 = x\u2081y\u2080 + x\u2080y\u2081';

        // Cross-term blocks slide together and fade out
        b_x1y0.position.x = lerp(init_x1y0.x, 0, e);
        b_x1y0.position.y = lerp(init_x1y0.y, gy, e);
        b_x0y1.position.x = lerp(init_x0y1.x, 0, e);
        b_x0y1.position.y = lerp(init_x0y1.y, gy, e);

        // Fade out cross-term blocks in second half
        var fadeT = Math.max(0, (t - 0.4) / 0.6);
        var fadeE = easeInOutCubic(Math.min(1, fadeT));
        b_x1y0.material.opacity = 1 - fadeE;
        l_x1y0.material.opacity = 1 - fadeE;
        b_x0y1.material.opacity = 1 - fadeE;
        l_x0y1.material.opacity = 1 - fadeE;

        // Fade in z1 block
        var appearT = Math.max(0, (t - 0.3) / 0.7);
        var appearE = easeInOutCubic(Math.min(1, appearT));
        b_z1.material.opacity = appearE;
        l_z1.material.opacity = appearE;
        b_z1.position.set(0, gy, 0);

        // Fade in subtraction blocks
        var subT = Math.max(0, (t - 0.55) / 0.45);
        var subE = easeInOutCubic(Math.min(1, subT));
        b_subZ2.material.opacity = subE * 0.85;
        l_subZ2.material.opacity = subE;
        b_subZ0.material.opacity = subE * 0.85;
        l_subZ0.material.opacity = subE;

      } else if (cycleT < t2) {
        // --- Pause: show merged state ---
        setMergedState();
        phaseLabel.textContent = 'Result: 3 multiplications';
        countLabel.textContent = 'z\u2082 = x\u2081y\u2081  \u00B7  z\u2081 = (x\u2081+x\u2080)(y\u2081+y\u2080) - z\u2082 - z\u2080  \u00B7  z\u2080 = x\u2080y\u2080';

      } else if (cycleT < t3) {
        // --- Phase 2: rearrange into a horizontal row ---
        t = (cycleT - t2) / D;
        e = easeInOutCubic(t);

        phaseLabel.textContent = 'Assembling the product: z\u2082\u00B7B\u00B2\u1D50 + z\u2081\u00B7B\u1D50 + z\u2080';
        countLabel.textContent = '4 \u2192 3 multiplications \u00B7 25% saved per recursion level';

        // Move z2 (x1y1) to left position
        b_x1y1.position.x = lerp(init_x1y1.x, finalZ2pos.x, e);
        b_x1y1.position.y = lerp(init_x1y1.y, finalZ2pos.y, e);

        // Move z1 to center
        b_z1.position.x = lerp(0, finalZ1pos.x, e);
        b_z1.position.y = lerp(gy, finalZ1pos.y, e);

        // Move z0 (x0y0) to right position
        b_x0y0.position.x = lerp(init_x0y0.x, finalZ0pos.x, e);
        b_x0y0.position.y = lerp(init_x0y0.y, finalZ0pos.y, e);

        // Fade subtraction blocks out (absorbed into z1)
        var subFadeT = Math.max(0, (t - 0.1) / 0.5);
        var subFadeE = easeInOutCubic(Math.min(1, subFadeT));
        b_subZ2.material.opacity = 0.85 * (1 - subFadeE);
        l_subZ2.material.opacity = 1 - subFadeE;
        b_subZ0.material.opacity = 0.85 * (1 - subFadeE);
        l_subZ0.material.opacity = 1 - subFadeE;

        // Replace block labels with z-notation
        // Swap x1y1 label -> z2
        if (t > 0.5) {
          l_x1y1.material.opacity = 0;
          l_z2_final.material.opacity = easeInOutCubic((t - 0.5) / 0.5);
          l_z2_final.position.copy(b_x1y1.position);
          l_z2_final.position.z += BD / 2 + 0.25;
        }
        if (t > 0.5) {
          l_x0y0.material.opacity = 0;
          l_z0_final.material.opacity = easeInOutCubic((t - 0.5) / 0.5);
          l_z0_final.position.copy(b_x0y0.position);
          l_z0_final.position.z += BD / 2 + 0.25;
        }

      } else if (cycleT < t4) {
        // --- Pause: show final row ---
        setFinalRow();
        phaseLabel.textContent = 'xy = z\u2082\u00B7B\u00B2\u1D50 + z\u2081\u00B7B\u1D50 + z\u2080';
        countLabel.textContent = 'Three multiplications suffice.';

      } else if (cycleT < t5) {
        // --- Phase 3: reset back to 4 blocks ---
        t = (cycleT - t4) / D;
        e = easeInOutCubic(t);

        phaseLabel.textContent = '';
        countLabel.textContent = '';

        // Fade everything out, then snap back
        var fadeAll = 1 - easeInOutCubic(Math.min(1, t * 2));
        b_x1y1.material.opacity = fadeAll;
        l_x1y1.material.opacity = fadeAll;
        b_x0y0.material.opacity = fadeAll;
        l_x0y0.material.opacity = fadeAll;
        b_z1.material.opacity = fadeAll;
        l_z1.material.opacity = fadeAll;
        l_z2_final.material.opacity = 0;
        l_z0_final.material.opacity = 0;
        b_subZ2.material.opacity = 0;
        b_subZ0.material.opacity = 0;
        l_subZ2.material.opacity = 0;
        l_subZ0.material.opacity = 0;

        // In second half, fade 4 blocks back in at starting positions
        if (t > 0.5) {
          var fadeIn = easeInOutCubic((t - 0.5) / 0.5);
          resetPositions();
          b_x1y1.material.opacity = fadeIn;
          l_x1y1.material.opacity = fadeIn;
          b_x1y0.material.opacity = fadeIn;
          l_x1y0.material.opacity = fadeIn;
          b_x0y1.material.opacity = fadeIn;
          l_x0y1.material.opacity = fadeIn;
          b_x0y0.material.opacity = fadeIn;
          l_x0y0.material.opacity = fadeIn;
          b_z1.material.opacity = 0;
          l_z1.material.opacity = 0;
        }

      } else {
        // --- Final pause before loop ---
        resetToPhase0();
        phaseLabel.textContent = 'Schoolbook: 4 multiplications';
        countLabel.textContent = 'x\u2081y\u2081 \u00B7 x\u2081y\u2080 \u00B7 x\u2080y\u2081 \u00B7 x\u2080y\u2080';
      }

      // Gentle scene rotation
      scene.rotation.y = Math.sin(elapsed * 0.15) * 0.08;

      renderer.render(scene, camera);
    }

    function resetPositions() {
      b_x1y1.position.copy(init_x1y1);
      b_x1y0.position.copy(init_x1y0);
      b_x0y1.position.copy(init_x0y1);
      b_x0y0.position.copy(init_x0y0);
      b_z1.position.set(0, gy, 0);
      b_subZ2.position.set(-0.5, gy - BH * 0.7, 0.5);
      b_subZ0.position.set(0.5, gy - BH * 0.7, 0.5);
    }

    function resetToPhase0() {
      resetPositions();
      b_x1y1.material.opacity = 1; l_x1y1.material.opacity = 1;
      b_x1y0.material.opacity = 1; l_x1y0.material.opacity = 1;
      b_x0y1.material.opacity = 1; l_x0y1.material.opacity = 1;
      b_x0y0.material.opacity = 1; l_x0y0.material.opacity = 1;
      b_z1.material.opacity = 0;   l_z1.material.opacity = 0;
      b_subZ2.material.opacity = 0; l_subZ2.material.opacity = 0;
      b_subZ0.material.opacity = 0; l_subZ0.material.opacity = 0;
      l_z2_final.material.opacity = 0;
      l_z0_final.material.opacity = 0;
      b_x1y1.material.color.setHex(COL_Z2);
      b_x0y0.material.color.setHex(COL_Z0);
    }

    function setMergedState() {
      b_x1y1.position.copy(init_x1y1);
      b_x1y1.material.opacity = 1; l_x1y1.material.opacity = 1;
      b_x1y0.material.opacity = 0; l_x1y0.material.opacity = 0;
      b_x0y1.material.opacity = 0; l_x0y1.material.opacity = 0;
      b_x0y0.position.copy(init_x0y0);
      b_x0y0.material.opacity = 1; l_x0y0.material.opacity = 1;
      b_z1.position.set(0, gy, 0);
      b_z1.material.opacity = 1; l_z1.material.opacity = 1;
      b_subZ2.material.opacity = 0.85; l_subZ2.material.opacity = 1;
      b_subZ0.material.opacity = 0.85; l_subZ0.material.opacity = 1;
      l_z2_final.material.opacity = 0;
      l_z0_final.material.opacity = 0;
    }

    function setFinalRow() {
      b_x1y1.position.set(finalZ2pos.x, finalZ2pos.y, finalZ2pos.z);
      b_x1y1.material.opacity = 1; l_x1y1.material.opacity = 0;
      b_z1.position.set(finalZ1pos.x, finalZ1pos.y, finalZ1pos.z);
      b_z1.material.opacity = 1; l_z1.material.opacity = 1;
      b_x0y0.position.set(finalZ0pos.x, finalZ0pos.y, finalZ0pos.z);
      b_x0y0.material.opacity = 1; l_x0y0.material.opacity = 0;
      b_x1y0.material.opacity = 0; l_x1y0.material.opacity = 0;
      b_x0y1.material.opacity = 0; l_x0y1.material.opacity = 0;
      b_subZ2.material.opacity = 0; l_subZ2.material.opacity = 0;
      b_subZ0.material.opacity = 0; l_subZ0.material.opacity = 0;
      l_z2_final.position.set(finalZ2pos.x, finalZ2pos.y, finalZ2pos.z + BD / 2 + 0.25);
      l_z2_final.material.opacity = 1;
      l_z0_final.position.set(finalZ0pos.x, finalZ0pos.y, finalZ0pos.z + BD / 2 + 0.25);
      l_z0_final.material.opacity = 1;
    }

    scene.add(l_z2_final);
    scene.add(l_z0_final);

    // --- Resize handler ---
    window.addEventListener('resize', function() {
      var nw = container.clientWidth;
      camera.aspect = nw / H;
      camera.updateProjectionMatrix();
      renderer.setSize(nw, H);
    });

    animate();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initKaratsuba);
  } else {
    initKaratsuba();
  }
})();
</script>

# Toom-Cook: Generalizing Karatsuba via Polynomial Interpolation

## From Digits to Polynomials

Karatsuba showed that splitting a number in two and exploiting an algebraic identity could reduce four half-size multiplications to three. A natural question follows: what happens if we split into *three* pieces? Or $k$? This is exactly the generalization that Andrei Toom (1963) and Stephen Cook (1966) independently formalized. The resulting family of algorithms -- collectively known as **Toom-Cook** or **Toom-$k$** -- systematically trades more additions and scalar operations for fewer recursive multiplications, pushing the exponent ever closer to 1.

The key conceptual shift is to stop viewing integers as flat strings of digits and instead view them as **polynomials**. If we partition an $n$-digit number into $k$ blocks of roughly $m = \lceil n/k \rceil$ digits each, writing $B = 10^m$ (or $2^m$ in binary), then:

$$
x = a_{k-1} B^{k-1} + a_{k-2} B^{k-2} + \cdots + a_1 B + a_0
$$

This is simply the number $x$ evaluated at the point $z = B$ of the polynomial:

$$
P_x(z) = a_{k-1} z^{k-1} + a_{k-2} z^{k-2} + \cdots + a_1 z + a_0
$$

Multiplying two such integers $x$ and $y$ is therefore equivalent to computing the **product polynomial** $P_x(z) \cdot P_y(z)$ and then evaluating the result at $z = B$ (with appropriate carries). If each input polynomial has degree $k-1$, their product has degree $2(k-1) = 2k - 2$, and is therefore determined by exactly $2k - 1$ point-value pairs -- a fact guaranteed by the **Fundamental Theorem of Algebra**.

This is the heart of the speedup: instead of multiplying the coefficients pairwise (which would require $k^2$ recursive multiplications), we can recover the product polynomial from only $2k - 1$ pointwise products.

## The Five Phases of Toom-Cook

The algorithm proceeds through five clearly delineated stages:

### Phase 1: Splitting

Break each $n$-digit operand into $k$ blocks of $\sim n/k$ digits. For Toom-3, this yields three coefficients per number:

$$
\begin{aligned}
x &= a_2 B^{2m} + a_1 B^m + a_0  &\longleftrightarrow\quad P_x(z) &= a_2 z^2 + a_1 z + a_0 \\
y &= b_2 B^{2m} + b_1 B^m + b_0  &\longleftrightarrow\quad P_y(z) &= b_2 z^2 + b_1 z + b_0
\end{aligned}
$$

### Phase 2: Evaluation

Select $2k - 1$ distinct evaluation points. The standard choice for Toom-3 is the set $\{0,\; 1,\; -1,\; 2,\; \infty\}$, chosen because they minimize the size of intermediate values and keep the arithmetic simple. Evaluate both polynomials at each point:

$$
\begin{aligned}
P_x(0) &= a_0 & P_y(0) &= b_0 \\
P_x(1) &= a_2 + a_1 + a_0 & P_y(1) &= b_2 + b_1 + b_0 \\
P_x(-1) &= a_2 - a_1 + a_0 & P_y(-1) &= b_2 - b_1 + b_0 \\
P_x(2) &= 4a_2 + 2a_1 + a_0 & P_y(2) &= 4b_2 + 2b_1 + b_0 \\
P_x(\infty) &= a_2 & P_y(\infty) &= b_2
\end{aligned}
$$

The "evaluation at $\infty$" is a notational convenience: it extracts the leading coefficient of the polynomial, since $\lim_{z \to \infty} P(z)/z^{k-1}$ equals the leading coefficient.

### Phase 3: Pointwise Multiplication

Multiply the evaluated values at each point. These are the **only** recursive multiplications the algorithm performs:

$$
\begin{aligned}
W_0 &= P_x(0) \cdot P_y(0) = a_0 b_0 \\
W_1 &= P_x(1) \cdot P_y(1) \\
W_{-1} &= P_x(-1) \cdot P_y(-1) \\
W_2 &= P_x(2) \cdot P_y(2) \\
W_\infty &= P_x(\infty) \cdot P_y(\infty) = a_2 b_2
\end{aligned}
$$

Five multiplications on operands of size $\sim n/3$, rather than the nine that naive coefficient-by-coefficient expansion would require.

### Phase 4: Interpolation

The product polynomial $R(z) = P_x(z) \cdot P_y(z)$ has degree 4, so it has five coefficients $C_0, C_1, C_2, C_3, C_4$:

$$
R(z) = C_4 z^4 + C_3 z^3 + C_2 z^2 + C_1 z + C_0
$$

From the five evaluated products, we can read off:

$$
\begin{aligned}
W_0 &= C_0 \\
W_1 &= C_4 + C_3 + C_2 + C_1 + C_0 \\
W_{-1} &= C_4 - C_3 + C_2 - C_1 + C_0 \\
W_2 &= 16C_4 + 8C_3 + 4C_2 + 2C_1 + C_0 \\
W_\infty &= C_4
\end{aligned}
$$

This is a $5 \times 5$ linear system in the unknowns $C_0, \ldots, C_4$. Because $C_0 = W_0$ and $C_4 = W_\infty$ are immediate, the system reduces quickly. The remaining coefficients are solved by elimination:

$$
\begin{aligned}
C_0 &= W_0 \\[4pt]
C_4 &= W_\infty \\[4pt]
C_2 &= \frac{W_1 + W_{-1}}{2} - C_0 - C_4 \\[4pt]
C_3 &= \frac{W_2 - 2W_1 - 14C_4 - 2C_2 + C_0}{6} \\[4pt]
C_1 &= W_1 - C_4 - C_3 - C_2 - C_0
\end{aligned}
$$

Note that these expressions involve only additions, subtractions, and divisions by small constants (2 and 6) -- all $O(n)$ operations, negligible compared to the recursive multiplications.

### Phase 5: Recomposition

Reassemble the final integer from the product polynomial's coefficients:

$$
x \cdot y = C_4 B^{4m} + C_3 B^{3m} + C_2 B^{2m} + C_1 B^m + C_0
$$

The multiplications by powers of $B$ are simply left-shifts, and the final addition with carry propagation is $O(n)$.

## A Worked Example

To make this concrete, consider $x = 123{,}456{,}789$ and $y = 987{,}654{,}321$ in base 10 with $k = 3$ and $m = 3$ (so $B = 10^3 = 1000$):

$$
\begin{aligned}
x &= 123 \cdot 10^6 + 456 \cdot 10^3 + 789 \quad\Longleftrightarrow\quad P_x(z) = 123z^2 + 456z + 789 \\
y &= 987 \cdot 10^6 + 654 \cdot 10^3 + 321 \quad\Longleftrightarrow\quad P_y(z) = 987z^2 + 654z + 321
\end{aligned}
$$

Evaluating at the five standard points:

| Point | $P_x$ | $P_y$ | $W = P_x \cdot P_y$ |
|-------|--------|--------|----------------------|
| $0$   | $789$  | $321$  | $253{,}269$          |
| $1$   | $1{,}368$ | $1{,}962$ | $2{,}684{,}016$   |
| $-1$  | $456$  | $654$  | $298{,}224$          |
| $2$   | $2{,}193$ | $5{,}595$ | $12{,}269{,}835$   |
| $\infty$ | $123$ | $987$ | $121{,}401$          |

Interpolation then yields the five coefficients $C_0, \ldots, C_4$, and recomposition with $B = 1000$ recovers the product $121{,}932{,}631{,}112{,}635{,}269$.

## Complexity Analysis

The recurrence for Toom-$k$ is:

$$
T(n) = (2k - 1)\, T\!\left(\frac{n}{k}\right) + O(n)
$$

By the Master Theorem, this solves to:

$$
T(n) = O\!\left(n^{\log_k(2k-1)}\right)
$$

The exponent $\log_k(2k - 1)$ decreases monotonically as $k$ increases, approaching 1 from above:

| Algorithm             | Split ($k$) | Recursive Mults ($2k-1$) | Complexity                       |
|-----------------------|-------------|--------------------------|----------------------------------|
| Grade School          | $n$         | $n^2$                    | $O(n^2)$                         |
| Karatsuba (Toom-2)    | $2$         | $3$                      | $O(n^{\log_2 3}) \approx O(n^{1.585})$ |
| Toom-3                | $3$         | $5$                      | $O(n^{\log_3 5}) \approx O(n^{1.465})$ |
| Toom-4                | $4$         | $7$                      | $O(n^{\log_4 7}) \approx O(n^{1.404})$ |
| Toom-$k$              | $k$         | $2k-1$                   | $O\!\big(n^{\log_k(2k-1)}\big)$  |

### The Hidden Cost: Why We Cannot Simply Let $k \to \infty$

A tempting conclusion is that by choosing $k$ large enough, we can push the exponent arbitrarily close to 1 and achieve near-linear multiplication. In practice, this reasoning breaks down for two reasons:

1. **Evaluation and interpolation overhead.** The matrices involved in evaluation and interpolation grow as $O(k^2)$, and the entries grow in magnitude. For large $k$, the scalar additions and divisions in the interpolation phase cease to be negligible. The constant hidden in the $O(n)$ additive term balloons.

2. **Coefficient blowup.** Evaluating at points like $2, -2, 3, \ldots$ produces intermediate values that are significantly larger than the original coefficients. This "coefficient swell" increases the size of the sub-problems fed to the recursive multiplications, partially negating the savings.

The practical sweet spot is typically Toom-3 or Toom-4. Beyond that, the FFT-based methods (Schönhage-Strassen and its successors) offer a fundamentally better asymptotic trade-off. The transition from Toom-Cook to FFT-based multiplication is, in a sense, the transition from finite polynomial interpolation to interpolation at infinitely many structured points -- the roots of unity.

### Karatsuba as Toom-2: A Unifying Perspective

It is worth pausing to note that Karatsuba's algorithm is precisely Toom-Cook with $k = 2$. The "trick" of computing $(x_1 + x_0)(y_1 + y_0) - z_2 - z_0$ is the interpolation step for a degree-2 product polynomial evaluated at the points $\{0, 1, \infty\}$. Karatsuba's genius was to discover this special case in 1960; Toom and Cook's contribution was to recognize the general structure of which Karatsuba is the simplest instance.

# The Fourier Transform: From Signals to Arithmetic

## Why We Need a New Idea

At the end of the Toom-Cook story we noted a frustrating ceiling: as we increase the splitting parameter $k$, the exponent $\log_k(2k-1)$ drifts toward 1, but it never reaches it. Worse, the constant factor in the $O(n)$ additive work (evaluation and interpolation matrices of size $k \times k$, coefficient blowup at large evaluation points) grows so fast that no finite $k$ delivers practical gains beyond Toom-4 or so.

To break through this wall we need to abandon the strategy of evaluating at a handful of ad-hoc points and instead evaluate at a *structured infinite family* of points whose algebraic symmetry enables a radically faster algorithm. That family is the **complex roots of unity**, and the algorithm that exploits their symmetry is the **Fast Fourier Transform**.

Before we can state Schönhage and Strassen's multiplication algorithm, we must build the FFT from the ground up. This requires four conceptual layers: (1) the observation that integer multiplication is polynomial convolution, (2) the Discrete Fourier Transform as an evaluation map, (3) the Cooley-Tukey decomposition that makes the DFT fast, and (4) the inverse transform that recovers coefficients from point values.

---

## Multiplication Is Convolution

### Polynomials and digit vectors

We have already seen that an $n$-digit integer in base $B$ can be written as a polynomial evaluated at $B$. Let us now make the multiplication side precise. Given two integers with digit vectors $\mathbf{a} = (a_0, a_1, \ldots, a_{n-1})$ and $\mathbf{b} = (b_0, b_1, \ldots, b_{n-1})$, their product is a new integer whose digit vector $\mathbf{c} = (c_0, c_1, \ldots, c_{2n-2})$ satisfies:

$$
c_k = \sum_{j=0}^{k} a_j \, b_{k-j}
\qquad \text{for } k = 0, 1, \ldots, 2n-2
$$

(with the convention that $a_j = 0$ for $j \geq n$ and similarly for $b_j$). This is exactly the definition of the **linear convolution** of the sequences $\mathbf{a}$ and $\mathbf{b}$, or equivalently, the coefficient vector of the product polynomial $A(x) \cdot B(x)$ where:

$$
A(x) = \sum_{j=0}^{n-1} a_j x^j, \qquad B(x) = \sum_{j=0}^{n-1} b_j x^j
$$

Computing this convolution directly requires computing each of the $2n - 1$ output coefficients, and for each we sum up to $n$ products. The total cost is $O(n^2)$ -- schoolbook multiplication in disguise.

### The Convolution Theorem

The single most important theorem in this entire story is:

> **Convolution Theorem.** Let $\mathcal{F}$ denote the Discrete Fourier Transform (defined below). If $\mathbf{c} = \mathbf{a} \ast \mathbf{b}$ is the convolution of two sequences, then:
>
> $$\mathcal{F}(\mathbf{a} \ast \mathbf{b}) = \mathcal{F}(\mathbf{a}) \cdot \mathcal{F}(\mathbf{b})$$
>
> where $\cdot$ denotes *pointwise* (component-by-component) multiplication.

In words: convolution in the "coefficient domain" becomes pointwise multiplication in the "frequency domain." Since pointwise multiplication of two length-$N$ vectors costs only $O(N)$, the entire cost of multiplication reduces to the cost of *two forward transforms and one inverse transform*. If each transform costs $O(N \log N)$, the total cost is $O(N \log N)$ -- an exponential improvement over $O(N^2)$.

This is not a hand-wave. Let us now build the DFT rigorously and prove why it can be computed in $O(N \log N)$.

---

## The Discrete Fourier Transform

### Complex exponentials and Euler's formula

Before defining the DFT, we need the language of complex numbers. Recall **Euler's formula**:

$$
e^{i\theta} = \cos\theta + i\sin\theta
$$

This elegant identity tells us that the complex exponential $e^{i\theta}$ traces out the unit circle in the complex plane as $\theta$ varies from $0$ to $2\pi$. Every point on the unit circle can be written as $e^{i\theta}$ for some angle $\theta$.

### The $N$-th roots of unity

Fix a positive integer $N$. The **$N$-th roots of unity** are the $N$ complex numbers that satisfy $z^N = 1$. They are:

$$
\omega_N^k = e^{2\pi i k / N}, \qquad k = 0, 1, \ldots, N-1
$$

These are $N$ points spaced equally around the unit circle, like the vertices of a regular $N$-gon inscribed in the circle $|z| = 1$. The **primitive** $N$-th root of unity is:

$$
\omega_N = e^{2\pi i / N}
$$

so that $\omega_N^k = (\omega_N)^k$. We will usually drop the subscript $N$ when the context is clear.

The roots of unity possess remarkable algebraic properties that are the engine of the FFT:

1. **Periodicity:** $\omega^{k+N} = \omega^k$ for all $k$. The roots cycle with period $N$.

2. **Cancellation (Half-turn symmetry):** $\omega^{k + N/2} = -\omega^k$ when $N$ is even. Geometrically, the point diametrically opposite $\omega^k$ on the unit circle is $-\omega^k$. This is the single most important property for the FFT.

3. **Summation:** $\displaystyle\sum_{k=0}^{N-1} \omega^{jk} = \begin{cases} N & \text{if } N \mid j \\ 0 & \text{otherwise} \end{cases}$

   This orthogonality relation is what makes the inverse DFT work.

4. **Squaring (Halving):** If $N$ is even, then $\{(\omega_N^k)^2 : k = 0, \ldots, N-1\}$ gives exactly the $N/2$-th roots of unity, each appearing twice. That is, $(\omega_N)^2 = \omega_{N/2}$.

### Definition of the DFT

Given a vector $\mathbf{x} = (x_0, x_1, \ldots, x_{N-1})$, its **Discrete Fourier Transform** is the vector $\mathbf{X} = (X_0, X_1, \ldots, X_{N-1})$ defined by:

$$
X_k = \sum_{j=0}^{N-1} x_j \, \omega_N^{jk}, \qquad k = 0, 1, \ldots, N-1
$$

Equivalently, $X_k = P(\omega^k)$ where $P(z) = \sum_{j} x_j z^j$ is the polynomial whose coefficients are the entries of $\mathbf{x}$. The DFT is nothing more than **evaluating the polynomial at all $N$-th roots of unity simultaneously**.

### The DFT matrix

We can express the DFT as a matrix-vector product $\mathbf{X} = F_N \, \mathbf{x}$ where the **DFT matrix** $F_N$ has entries:

$$
(F_N)_{k,j} = \omega_N^{jk}
$$

Explicitly, for $N = 4$ with $\omega = \omega_4 = e^{2\pi i/4} = i$:

$$
F_4 = \begin{pmatrix}
1 & 1 & 1 & 1 \\
1 & i & i^2 & i^3 \\
1 & i^2 & i^4 & i^6 \\
1 & i^3 & i^6 & i^9
\end{pmatrix}
= \begin{pmatrix}
1 & 1 & 1 & 1 \\
1 & i & -1 & -i \\
1 & -1 & 1 & -1 \\
1 & -i & -1 & i
\end{pmatrix}
$$

Computing $\mathbf{X} = F_N \mathbf{x}$ by brute-force matrix-vector multiplication costs $O(N^2)$. The entire point of the FFT is to exploit the structure of $F_N$ to compute this product in $O(N \log N)$.

### The Inverse DFT

The orthogonality of the roots of unity (property 3 above) guarantees that the DFT is invertible. The inverse is:

$$
x_j = \frac{1}{N} \sum_{k=0}^{N-1} X_k \, \omega_N^{-jk}
$$

or in matrix form, $\mathbf{x} = \frac{1}{N} F_N^{-1} \mathbf{X}$ where $F_N^{-1}$ is the matrix with entries $\omega_N^{-jk}$ -- the same as $F_N$ but with $\omega$ replaced by $\omega^{-1} = \overline{\omega}$ (the complex conjugate). In other words, **the inverse DFT is computed by the same algorithm as the forward DFT**, just with the twiddle factors conjugated and the output scaled by $1/N$. Any algorithm that computes the forward DFT efficiently also computes the inverse efficiently, for free.

**Proof of inversion.** We need to verify that $\frac{1}{N}F_N^{-1} F_N = I_N$, i.e., that:

$$
\frac{1}{N} \sum_{k=0}^{N-1} \omega^{-jk} \omega^{k\ell} = \frac{1}{N} \sum_{k=0}^{N-1} \omega^{k(\ell - j)} = \begin{cases} 1 & \text{if } j = \ell \\ 0 & \text{if } j \neq \ell \end{cases}
$$

When $j = \ell$, every term in the sum is $\omega^0 = 1$, so the sum is $N$ and we get $N/N = 1$. When $j \neq \ell$, let $m = \ell - j \not\equiv 0 \pmod{N}$. Then $\sum_{k=0}^{N-1} \omega^{mk}$ is a geometric series with ratio $r = \omega^m \neq 1$:

$$
\sum_{k=0}^{N-1} r^k = \frac{r^N - 1}{r - 1} = \frac{(\omega^N)^m - 1}{\omega^m - 1} = \frac{1 - 1}{\omega^m - 1} = 0
$$

since $\omega^N = 1$ by definition. $\blacksquare$

---

## The Fast Fourier Transform (Cooley-Tukey, Radix-2)

### The core idea: divide and conquer on even and odd indices

The breakthrough of Cooley and Tukey (1965) -- though the idea traces back to Gauss (1805) -- is to observe that when $N$ is even, the DFT of size $N$ can be decomposed into **two DFTs of size $N/2$** plus $O(N)$ additional work.

Write $N = 2M$. Split the input sequence $\mathbf{x}$ into its even-indexed and odd-indexed elements:

$$
\begin{aligned}
\mathbf{e} &= (x_0, x_2, x_4, \ldots, x_{N-2}) \quad \text{(even indices)} \\
\mathbf{d} &= (x_1, x_3, x_5, \ldots, x_{N-1}) \quad \text{(odd indices)}
\end{aligned}
$$

Now consider the DFT sum for an arbitrary output index $k$:

$$
X_k = \sum_{j=0}^{N-1} x_j \, \omega_N^{jk}
$$

Separate the even-indexed and odd-indexed terms:

$$
X_k = \underbrace{\sum_{m=0}^{M-1} x_{2m} \, \omega_N^{2mk}}_{E_k} + \underbrace{\omega_N^k \sum_{m=0}^{M-1} x_{2m+1} \, \omega_N^{2mk}}_{= \omega_N^k \cdot D_k}
$$

Using the **squaring property** $\omega_N^2 = \omega_M$ (where $M = N/2$), each of these inner sums is itself a DFT of size $M$:

$$
\begin{aligned}
E_k &= \sum_{m=0}^{M-1} x_{2m} \, \omega_M^{mk} = \text{DFT}_M(\mathbf{e})_k \\[4pt]
D_k &= \sum_{m=0}^{M-1} x_{2m+1} \, \omega_M^{mk} = \text{DFT}_M(\mathbf{d})_k
\end{aligned}
$$

So the full DFT decomposes as:

$$
\boxed{X_k = E_k + \omega_N^k \cdot D_k}
$$

But we need $X_k$ for $k = 0, 1, \ldots, N-1$, while $E_k$ and $D_k$ are periodic with period $M = N/2$ (they are DFTs of size $M$). For the "upper half" $k + M$, the **cancellation property** $\omega_N^{k+M} = -\omega_N^k$ gives:

$$
\boxed{X_{k+M} = E_k - \omega_N^k \cdot D_k}
$$

These two equations together constitute the **butterfly operation**: from the pair $(E_k, D_k)$ and the **twiddle factor** $\omega_N^k$, we compute both $X_k$ and $X_{k+M}$ using **one** complex multiplication and **two** complex additions.

### The butterfly diagram

Each butterfly takes two inputs, multiplies one by a twiddle factor, and produces two outputs via addition and subtraction:

```
  E_k ──────────┬──── (+) ──── X_k
                 │
          ω^k    ×
                 │
  D_k ──────────┴──── (−) ──── X_{k+M}
```

For $M = N/2$ values of $k$ (namely $k = 0, 1, \ldots, M-1$), we perform $M$ butterflies, each costing $O(1)$. The total additional work at this level of recursion is $O(N)$.

### The recurrence and complexity

Let $T(N)$ denote the cost of computing a DFT of size $N$ (assumed a power of 2). The Cooley-Tukey decomposition gives:

$$
T(N) = 2\,T(N/2) + O(N)
$$

By the Master Theorem (case 2, with $a = 2$, $b = 2$, $f(N) = \Theta(N)$):

$$
T(N) = O(N \log N)
$$

compared to $O(N^2)$ for the naive DFT. For $N = 2^{20} \approx 10^6$, this is the difference between $\sim 10^{12}$ operations and $\sim 2 \times 10^7$ -- a speedup of 50,000$\times$.

### The full recursion tree

When $N = 2^s$, the recursion unfolds $s = \log_2 N$ levels deep. At each level, we partition the data, recurse on two halves, and combine with $N$ butterfly operations. The total work is:

$$
\underbrace{N}_{\text{level 0}} + \underbrace{N}_{\text{level 1}} + \cdots + \underbrace{N}_{\text{level } s-1} = s \cdot N = N \log_2 N
$$

Each level performs exactly $N/2$ butterflies (each costing one complex multiplication and two additions), for a total of $\frac{N}{2}\log_2 N$ complex multiplications.

### A worked example: 8-point FFT

Let $N = 8$ and $\omega = \omega_8 = e^{2\pi i/8} = e^{i\pi/4} = \frac{1+i}{\sqrt{2}}$. Consider the input $\mathbf{x} = (1, 1, 1, 1, 0, 0, 0, 0)$ (a rectangular pulse).

**Level 0 (split):** Separate into even and odd:

$$
\mathbf{e} = (x_0, x_2, x_4, x_6) = (1, 1, 0, 0), \qquad \mathbf{d} = (x_1, x_3, x_5, x_7) = (1, 1, 0, 0)
$$

**Level 1:** Each half recursively splits again. For $\mathbf{e}$:

$$
\mathbf{e}_{\text{even}} = (1, 0), \quad \mathbf{e}_{\text{odd}} = (1, 0)
$$

These are 2-point DFTs: $\text{DFT}_2(a, b) = (a + b, \; a - b)$. So:

$$
\text{DFT}_2(1, 0) = (1, 1) \quad \text{for both}
$$

**Level 1 butterfly (for $\mathbf{e}$):** Combine with twiddle factors $\omega_4^0 = 1$ and $\omega_4^1 = i$:

$$
E_0 = 1 + 1 \cdot 1 = 2, \quad E_2 = 1 - 1 \cdot 1 = 0
$$

$$
E_1 = 1 + i \cdot 1 = 1 + i, \quad E_3 = 1 - i \cdot 1 = 1 - i
$$

So $\text{DFT}_4(\mathbf{e}) = (2, \; 1+i, \; 0, \; 1-i)$.

An identical calculation gives $\text{DFT}_4(\mathbf{d}) = (2, \; 1+i, \; 0, \; 1-i)$.

**Level 0 butterfly:** Combine with twiddle factors $\omega_8^k$ for $k = 0, 1, 2, 3$:

$$
\begin{aligned}
X_0 &= E_0 + \omega^0 D_0 = 2 + 1 \cdot 2 = 4 \\
X_1 &= E_1 + \omega^1 D_1 = (1+i) + \tfrac{1+i}{\sqrt{2}}(1+i) = (1+i) + \tfrac{2i}{\sqrt{2}} = 1 + i + i\sqrt{2} \\
X_2 &= E_2 + \omega^2 D_2 = 0 + i \cdot 0 = 0 \\
X_3 &= E_3 + \omega^3 D_3 = (1-i) + \tfrac{-1+i}{\sqrt{2}}(1-i) = (1-i) + \tfrac{-1+i-i(-1)+i^2}{\sqrt{2}} \\
&\phantom{=}\; \text{(and the corresponding } X_{k+4} = E_k - \omega^k D_k \text{ for the upper half)}
\end{aligned}
$$

The key observation is not the specific numerical values but the *structure*: $3$ levels of $4$ butterflies each $= 12$ complex multiplications, versus $8^2 = 64$ for the naive DFT. The ratio $12/64 \approx 19\%$ -- and this ratio improves as $N$ grows.

The visualization below animates this 8-point butterfly network. Watch how data flows through three stages of butterflies -- each stage halving the sub-problem size -- with twiddle factors ($\omega^k$) applied at every crossing.

<div id="fft-viz" style="width: 100%; height: 560px; margin: 2em 0; border-radius: 8px; overflow: hidden; background: #0f172a; position: relative;">
  <div id="fft-phase-label" style="position: absolute; top: 16px; left: 50%; transform: translateX(-50%); color: #e2e8f0; font-family: monospace; font-size: 15px; z-index: 10; pointer-events: none; text-align: center; white-space: nowrap;"></div>
  <div id="fft-info-label" style="position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%); color: #94a3b8; font-family: monospace; font-size: 13px; z-index: 10; pointer-events: none; text-align: center;"></div>
</div>

<script>
(function() {
  function initFFTViz() {
    if (typeof THREE === 'undefined') { setTimeout(initFFTViz, 100); return; }

    var container = document.getElementById('fft-viz');
    if (!container) return;

    var phaseLabel = document.getElementById('fft-phase-label');
    var infoLabel = document.getElementById('fft-info-label');

    // --- Scene setup ---
    var scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0f172a);

    var W = container.clientWidth, H = 560;
    var camera = new THREE.OrthographicCamera(-7, 7, 4, -4, 0.1, 100);
    camera.position.set(0, 0, 10);
    camera.lookAt(0, 0, 0);

    var renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(W, H);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // --- Colors ---
    var COL_NODE    = 0x6366f1; // indigo
    var COL_WIRE    = 0x334155; // slate
    var COL_PULSE   = 0x22c55e; // green
    var COL_CROSS   = 0xf59e0b; // amber - twiddle factor lines
    var COL_ADD     = 0x3b82f6; // blue - addition lines
    var COL_SUB     = 0xef4444; // red - subtraction lines
    var COL_ACTIVE  = 0xa855f7; // purple - active stage highlight
    var COL_OUT     = 0x22c55e; // green - output

    var N = 8;
    var STAGES = 3; // log2(8) = 3

    // Bit-reversal permutation for N=8
    var bitRev = [0, 4, 2, 6, 1, 5, 3, 7];

    // Layout: 4 columns (input + 3 stages), 8 rows
    var XMIN = -5.5, XMAX = 5.5;
    var YMIN = -3.0, YMAX = 3.0;
    var cols = STAGES + 1; // 4 columns of nodes
    var colX = [];
    for (var c = 0; c <= STAGES; c++) {
      colX.push(XMIN + c * (XMAX - XMIN) / STAGES);
    }
    var rowY = [];
    for (var r = 0; r < N; r++) {
      rowY.push(YMAX - r * (YMAX - YMIN) / (N - 1));
    }

    // --- Create node spheres ---
    var nodeGeo = new THREE.SphereGeometry(0.12, 16, 16);
    var nodes = []; // nodes[col][row]
    for (c = 0; c <= STAGES; c++) {
      nodes[c] = [];
      for (r = 0; r < N; r++) {
        var mat = new THREE.MeshBasicMaterial({ color: c === 0 ? COL_NODE : 0x475569 });
        var sphere = new THREE.Mesh(nodeGeo, mat);
        sphere.position.set(colX[c], rowY[r], 0);
        scene.add(sphere);
        nodes[c][r] = sphere;
      }
    }

    // --- Input labels (bit-reversed order) ---
    var inputLabels = ['x\u2080', 'x\u2084', 'x\u2082', 'x\u2086', 'x\u2081', 'x\u2085', 'x\u2083', 'x\u2087'];
    var outputLabels = ['X\u2080', 'X\u2081', 'X\u2082', 'X\u2083', 'X\u2084', 'X\u2085', 'X\u2086', 'X\u2087'];

    function makeTextSprite(text, color, fontSize) {
      var canvas = document.createElement('canvas');
      canvas.width = 256; canvas.height = 64;
      var ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, 256, 64);
      ctx.fillStyle = color || '#e2e8f0';
      ctx.font = 'bold ' + (fontSize || 28) + 'px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(text, 128, 32);
      var tex = new THREE.CanvasTexture(canvas);
      tex.minFilter = THREE.LinearFilter;
      var spriteMat = new THREE.SpriteMaterial({ map: tex, transparent: true });
      var sprite = new THREE.Sprite(spriteMat);
      sprite.scale.set(1.4, 0.35, 1);
      return sprite;
    }

    for (r = 0; r < N; r++) {
      var lbl = makeTextSprite(inputLabels[r], '#94a3b8', 24);
      lbl.position.set(colX[0] - 0.9, rowY[r], 0);
      scene.add(lbl);

      var olbl = makeTextSprite(outputLabels[r], '#22c55e', 24);
      olbl.position.set(colX[STAGES] + 0.9, rowY[r], 0);
      scene.add(olbl);
    }

    // --- Stage labels ---
    var stageSprites = [];
    for (var s = 0; s < STAGES; s++) {
      var midX = (colX[s] + colX[s + 1]) / 2;
      var sl = makeTextSprite('Stage ' + (s + 1), '#64748b', 22);
      sl.position.set(midX, YMAX + 0.5, 0);
      scene.add(sl);
      stageSprites.push(sl);
    }

    // --- Build butterfly wiring ---
    // For each stage s (0-indexed), the butterfly span is 2^(STAGES - 1 - s)
    // Groups of size 2^(STAGES - s), with pairs separated by span
    var wires = []; // {from:[col,row], to:[col,row], type:'add'|'sub', twiddleExp: number, stage: s}

    for (s = 0; s < STAGES; s++) {
      var groupSize = 1 << (STAGES - s);
      var halfGroup = groupSize / 2;
      for (var g = 0; g < N; g += groupSize) {
        for (var k = 0; k < halfGroup; k++) {
          var top = g + k;
          var bot = g + k + halfGroup;
          var twiddleExp = k * (1 << s);
          // Top wire: straight across (add)
          wires.push({ from: [s, top], to: [s + 1, top], type: 'add', twiddleExp: twiddleExp, stage: s });
          // Bottom wire: straight across (add, but with subtraction semantics)
          wires.push({ from: [s, bot], to: [s + 1, bot], type: 'sub', twiddleExp: twiddleExp, stage: s });
          // Cross wire top->bot (twiddle, goes to add at bot)
          wires.push({ from: [s, top], to: [s + 1, bot], type: 'cross-down', twiddleExp: twiddleExp, stage: s });
          // Cross wire bot->top (twiddle, goes to add at top)
          wires.push({ from: [s, bot], to: [s + 1, top], type: 'cross-up', twiddleExp: twiddleExp, stage: s });
        }
      }
    }

    // --- Draw wires as lines ---
    var lineMat = new THREE.LineBasicMaterial({ color: COL_WIRE, transparent: true, opacity: 0.3 });
    var wireLines = [];
    for (var w = 0; w < wires.length; w++) {
      var wire = wires[w];
      var pts = [
        new THREE.Vector3(colX[wire.from[0]], rowY[wire.from[1]], 0),
        new THREE.Vector3(colX[wire.to[0]], rowY[wire.to[1]], 0)
      ];
      var geo = new THREE.BufferGeometry().setFromPoints(pts);
      var wMat = new THREE.LineBasicMaterial({ color: COL_WIRE, transparent: true, opacity: 0.25 });
      var line = new THREE.Line(geo, wMat);
      scene.add(line);
      wireLines.push({ line: line, mat: wMat, wire: wire });
    }

    // --- Twiddle factor labels on cross wires ---
    var twiddleSprites = [];
    for (w = 0; w < wires.length; w++) {
      wire = wires[w];
      if (wire.type === 'cross-down' && wire.twiddleExp > 0) {
        var mx = (colX[wire.from[0]] + colX[wire.to[0]]) / 2;
        var my = (rowY[wire.from[1]] + rowY[wire.to[1]]) / 2;
        var expStr = wire.twiddleExp === 1 ? '\u03C9' : '\u03C9' + String.fromCharCode(0x2070 + wire.twiddleExp);
        // Use simpler label for readability
        var tLabel = makeTextSprite('\u03C9^' + wire.twiddleExp, '#f59e0b', 18);
        tLabel.position.set(mx + 0.35, my, 0.1);
        tLabel.material.opacity = 0;
        scene.add(tLabel);
        twiddleSprites.push({ sprite: tLabel, stage: wire.stage });
      }
    }

    // --- Animated pulses ---
    var pulseGeo = new THREE.SphereGeometry(0.08, 12, 12);
    var pulses = [];
    var PULSE_COUNT = N; // one pulse per input line

    for (var p = 0; p < PULSE_COUNT; p++) {
      var pMat = new THREE.MeshBasicMaterial({ color: COL_PULSE, transparent: true, opacity: 0 });
      var pMesh = new THREE.Mesh(pulseGeo, pMat);
      pMesh.position.set(colX[0], rowY[p], 0.2);
      scene.add(pMesh);
      pulses.push({ mesh: pMesh, row: p, mat: pMat });
    }

    // --- Animation ---
    var clock = new THREE.Clock();
    var elapsed = 0;
    var STAGE_DUR = 2.5;  // seconds per stage
    var PAUSE_DUR = 1.0;
    var INTRO_DUR = 1.5;
    var TOTAL_CYCLE = INTRO_DUR + STAGES * STAGE_DUR + (STAGES + 1) * PAUSE_DUR;

    function easeInOutCubic(t) {
      t = Math.max(0, Math.min(1, t));
      return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    function lerp(a, b, t) { return a + (b - a) * t; }

    var phaseTexts = [
      'Stage 1: Butterflies span 4 (groups of 8)',
      'Stage 2: Butterflies span 2 (groups of 4)',
      'Stage 3: Butterflies span 1 (groups of 2)'
    ];

    var infoTexts = [
      '4 butterflies \u00B7 \u03C9\u2070 twiddle factor \u00B7 even/odd split of full sequence',
      '4 butterflies \u00B7 \u03C9\u2070,\u03C9\u00B2 twiddle factors \u00B7 sub-sequences of length 4',
      '4 butterflies \u00B7 \u03C9\u2070,\u03C9\u00B9,\u03C9\u00B2,\u03C9\u00B3 twiddle factors \u00B7 final recombination'
    ];

    function animate() {
      requestAnimationFrame(animate);
      var dt = clock.getDelta();
      elapsed += dt;
      var cycleT = elapsed % TOTAL_CYCLE;

      // Determine current phase
      var currentStage = -1; // -1 = intro/reset
      var stageProgress = 0;

      var t0 = INTRO_DUR;
      for (s = 0; s < STAGES; s++) {
        var stageStart = t0 + s * (STAGE_DUR + PAUSE_DUR);
        var stageEnd = stageStart + STAGE_DUR;
        if (cycleT >= stageStart && cycleT < stageEnd) {
          currentStage = s;
          stageProgress = (cycleT - stageStart) / STAGE_DUR;
          break;
        }
        if (cycleT >= stageEnd && cycleT < stageEnd + PAUSE_DUR) {
          currentStage = s;
          stageProgress = 1.0;
          break;
        }
      }

      // --- Update labels ---
      if (currentStage >= 0) {
        phaseLabel.textContent = phaseTexts[currentStage];
        infoLabel.textContent = infoTexts[currentStage];
      } else if (cycleT < INTRO_DUR * 0.5) {
        phaseLabel.textContent = '8-point FFT Butterfly Network';
        infoLabel.textContent = 'Bit-reversed input \u2192 3 stages of butterflies \u2192 DFT output';
      } else {
        phaseLabel.textContent = '8-point FFT Butterfly Network';
        infoLabel.textContent = N + '/2 = 4 butterflies per stage \u00B7 log\u2082(8) = 3 stages \u00B7 12 total multiplications';
      }

      // --- Update wire colors ---
      for (w = 0; w < wireLines.length; w++) {
        var wl = wireLines[w];
        var ws = wl.wire.stage;
        if (ws === currentStage && stageProgress > 0) {
          var e = easeInOutCubic(stageProgress);
          if (wl.wire.type === 'add') {
            wl.mat.color.setHex(COL_ADD);
            wl.mat.opacity = lerp(0.25, 0.9, e);
          } else if (wl.wire.type === 'sub') {
            wl.mat.color.setHex(COL_SUB);
            wl.mat.opacity = lerp(0.25, 0.7, e);
          } else if (wl.wire.type === 'cross-down') {
            wl.mat.color.setHex(COL_CROSS);
            wl.mat.opacity = lerp(0.25, 0.85, e);
          } else if (wl.wire.type === 'cross-up') {
            wl.mat.color.setHex(COL_CROSS);
            wl.mat.opacity = lerp(0.25, 0.65, e);
          }
        } else if (ws < currentStage) {
          // Already processed stage - dim but colored
          if (wl.wire.type === 'add') {
            wl.mat.color.setHex(COL_ADD);
          } else if (wl.wire.type === 'sub') {
            wl.mat.color.setHex(COL_SUB);
          } else {
            wl.mat.color.setHex(COL_CROSS);
          }
          wl.mat.opacity = 0.3;
        } else {
          wl.mat.color.setHex(COL_WIRE);
          wl.mat.opacity = 0.25;
        }
      }

      // --- Update twiddle labels ---
      for (var ti = 0; ti < twiddleSprites.length; ti++) {
        var ts = twiddleSprites[ti];
        if (ts.stage === currentStage && stageProgress > 0.2) {
          ts.sprite.material.opacity = easeInOutCubic((stageProgress - 0.2) / 0.5);
        } else if (ts.stage < currentStage) {
          ts.sprite.material.opacity = 0.4;
        } else {
          ts.sprite.material.opacity = 0;
        }
      }

      // --- Update node colors ---
      for (c = 0; c <= STAGES; c++) {
        for (r = 0; r < N; r++) {
          if (c === 0) {
            nodes[c][r].material.color.setHex(COL_NODE);
          } else if (c - 1 < currentStage || (c - 1 === currentStage && stageProgress > 0.8)) {
            nodes[c][r].material.color.setHex(COL_ACTIVE);
          } else if (c - 1 === currentStage) {
            var ne = easeInOutCubic(stageProgress);
            var col = new THREE.Color(0x475569);
            col.lerp(new THREE.Color(COL_ACTIVE), ne);
            nodes[c][r].material.color.copy(col);
          } else {
            nodes[c][r].material.color.setHex(0x475569);
          }
        }
      }

      // Final column goes green when all stages done
      if (currentStage === STAGES - 1 && stageProgress >= 1.0) {
        for (r = 0; r < N; r++) {
          nodes[STAGES][r].material.color.setHex(COL_OUT);
        }
      }

      // --- Animate pulses ---
      for (p = 0; p < PULSE_COUNT; p++) {
        var pulse = pulses[p];
        if (currentStage < 0) {
          // During intro: pulses sit at input
          pulse.mat.opacity = easeInOutCubic(Math.min(1, cycleT / INTRO_DUR));
          pulse.mesh.position.set(colX[0], rowY[p], 0.2);
        } else {
          // Each pulse progresses through stages
          // Compute global progress: which stage + how far through it
          var globalProg = currentStage + stageProgress;
          var pulseCol = Math.floor(globalProg);
          var pulseT = globalProg - pulseCol;

          if (pulseCol > STAGES - 1) {
            pulseCol = STAGES - 1;
            pulseT = 1.0;
          }

          // Determine where this pulse goes during current butterfly
          var pRow = p;
          var groupSize2 = 1 << (STAGES - pulseCol);
          var halfGroup2 = groupSize2 / 2;
          var group2 = Math.floor(pRow / groupSize2) * groupSize2;
          var posInGroup = pRow - group2;
          var isUpper = posInGroup < halfGroup2;

          // Pulse travels from col[pulseCol] to col[pulseCol+1]
          var fromX = colX[pulseCol];
          var toX = colX[Math.min(pulseCol + 1, STAGES)];
          var e2 = easeInOutCubic(pulseT);

          pulse.mesh.position.x = lerp(fromX, toX, e2);
          pulse.mesh.position.y = rowY[p];
          pulse.mat.opacity = 0.9;

          // Pulse glow effect
          var glowT = Math.sin(elapsed * 4 + p * 0.8) * 0.3 + 0.7;
          pulse.mesh.scale.setScalar(glowT);
        }
      }

      renderer.render(scene, camera);
    }

    // --- Resize handler ---
    window.addEventListener('resize', function() {
      var nw = container.clientWidth;
      var aspect = nw / H;
      camera.left = -7 * aspect / (W / H);
      camera.right = 7 * aspect / (W / H);
      camera.updateProjectionMatrix();
      renderer.setSize(nw, H);
      W = nw;
    });

    animate();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFFTViz);
  } else {
    initFFTViz();
  }
})();
</script>

---

## Putting It Together: FFT-Based Polynomial Multiplication

We now have all the pieces. To multiply two polynomials $A(x)$ and $B(x)$ of degree $n-1$ (and thereby two $n$-digit integers):

**Step 1. Pad.** The product polynomial has degree $2n - 2$, so we need at least $2n - 1$ evaluation points. Choose $N = 2^{\lceil \log_2(2n) \rceil}$ (the next power of 2 at or above $2n$). Pad both coefficient vectors with zeros to length $N$.

**Step 2. Forward FFT.** Compute $\hat{\mathbf{a}} = \text{FFT}_N(\mathbf{a})$ and $\hat{\mathbf{b}} = \text{FFT}_N(\mathbf{b})$. Cost: $O(N \log N)$ each.

**Step 3. Pointwise multiply.** Compute $\hat{c}_k = \hat{a}_k \cdot \hat{b}_k$ for $k = 0, \ldots, N-1$. Cost: $O(N)$.

**Step 4. Inverse FFT.** Compute $\mathbf{c} = \text{IFFT}_N(\hat{\mathbf{c}})$. Cost: $O(N \log N)$.

**Step 5. Carry propagation.** The entries of $\mathbf{c}$ are the exact convolution coefficients (no rounding -- yet). Each $c_k$ may exceed the base $B$, so we perform a single left-to-right carry pass: set $c_k \leftarrow c_k \bmod B$ and add $\lfloor c_k / B \rfloor$ to $c_{k+1}$. Cost: $O(N)$.

**Total cost: $O(N \log N) = O(n \log n)$.**

At this point you might ask: if the FFT already gives us $O(n \log n)$ multiplication, why do we need Schönhage-Strassen? The answer lies in a subtle but critical issue: **numerical precision**.

---

# Schönhage-Strassen: Multiplication in $O(n \log n \log \log n)$

## The Precision Problem

The FFT-based multiplication pipeline described above works over the **complex numbers**. The twiddle factors $\omega_N^k = e^{2\pi i k/N}$ are irrational (for most $k$), and so are the intermediate values in the FFT. On a real computer, we approximate these with floating-point arithmetic.

For multiplying two numbers with $n$ digits, the convolution coefficients can be as large as $O(n B^2)$ (where $B$ is the base). To distinguish these integers exactly after rounding, we need floating-point precision of roughly $O(\log n + 2\log B)$ bits. For large $n$, this means we need **multi-precision floating-point arithmetic** inside the FFT itself -- and each multi-precision operation costs more than $O(1)$.

This creates a vicious circle: to multiply $n$-digit numbers, we use the FFT, but the FFT internally needs high-precision multiplications, which are themselves expensive. The complex-number FFT approach does not, by itself, yield a clean $O(n \log n)$ integer multiplication algorithm.

Schönhage and Strassen's 1971 breakthrough was to eliminate this precision problem entirely by moving from the complex numbers to an **exact algebraic setting** where roots of unity exist but rounding errors do not.

## From $\mathbb{C}$ to $\mathbb{Z}/(2^m + 1)\mathbb{Z}$: The Number Theoretic Transform

### Roots of unity in finite rings

The FFT algorithm does not actually require the complex numbers. It requires only a ring $R$ that contains:

1. An element $\omega$ of multiplicative order $N$ (an "$N$-th root of unity"), meaning $\omega^N = 1$ and $\omega^k \neq 1$ for $0 < k < N$.
2. An inverse of $N$ in $R$ (for the inverse transform).

If $R$ is a finite ring (like $\mathbb{Z}/p\mathbb{Z}$ for a prime $p$), then all arithmetic is exact -- no rounding, no precision issues. An FFT performed in such a ring is called a **Number Theoretic Transform (NTT)**.

**Example.** In $\mathbb{Z}/5\mathbb{Z}$, the element $2$ has order $4$: $2^1 = 2$, $2^2 = 4$, $2^3 = 3$, $2^4 = 1 \pmod{5}$. So $\omega = 2$ is a primitive $4$th root of unity in $\mathbb{Z}/5\mathbb{Z}$, and we can perform a 4-point NTT modulo 5 with exact arithmetic.

### Schönhage and Strassen's choice: Fermat-like rings

To multiply two $n$-bit integers, Schönhage and Strassen work in the ring:

$$
R = \mathbb{Z} / (2^m + 1)\mathbb{Z}
$$

for a carefully chosen $m$. This ring has a remarkable property: the element $\omega = 2$ (or more precisely, a small power of $2$) serves as a root of unity, and **multiplication by powers of 2 in this ring is just a bit-shift followed by a reduction modulo $2^m + 1$** -- an operation that costs $O(m)$, which is essentially free.

Why does $2$ behave as a root of unity here? Note that $2^m \equiv -1 \pmod{2^m + 1}$, so $2^{2m} \equiv 1 \pmod{2^m + 1}$. Thus $2$ has multiplicative order dividing $2m$ in this ring. With an appropriate choice of $m$, we can ensure that $2$ (or a power of it) is a primitive $N$-th root of unity for the $N$ we need.

The critical advantage: all the "twiddle factor multiplications" in the FFT butterfly -- which in the complex-number FFT require expensive multi-precision multiplications -- reduce to **bit-shifts and additions** in $\mathbb{Z}/(2^m + 1)\mathbb{Z}$. This makes the per-butterfly cost $O(m)$ instead of $O(m \log m \cdots)$, dramatically simplifying the recursion.

## The Algorithm in Detail

### Step 0: Setup

Given two $n$-bit integers $x$ and $y$, choose parameters:
- Let $K = 2^k$ for some $k$ (the number of chunks).
- Let $m = \lceil n / K \rceil + O(k)$ (the chunk size in bits, with some padding for carries).
- Work in the ring $R = \mathbb{Z}/(2^m + 1)\mathbb{Z}$.

The parameters are chosen so that $K \approx \sqrt{n}$ (roughly), meaning we split each input into about $\sqrt{n}$ chunks of about $\sqrt{n}$ bits each.

### Step 1: Decomposition

Break each $n$-bit integer into $K$ chunks of $\sim m$ bits:

$$
x = \sum_{j=0}^{K-1} a_j \cdot 2^{jm}, \qquad y = \sum_{j=0}^{K-1} b_j \cdot 2^{jm}
$$

Form the polynomials $A(z) = \sum a_j z^j$ and $B(z) = \sum b_j z^j$ over $R$, so that $x = A(2^m)$ and $y = B(2^m)$.

### Step 2: Forward NTT

Compute $\hat{\mathbf{a}} = \text{NTT}_N(\mathbf{a})$ and $\hat{\mathbf{b}} = \text{NTT}_N(\mathbf{b})$ in the ring $R$, where $N \geq 2K$ is a suitable power of 2.

The NTT is the same Cooley-Tukey FFT algorithm, but:
- All arithmetic is modular (mod $2^m + 1$).
- Twiddle factor multiplications $\omega^k \cdot v$ are implemented as **cyclic bit-shifts** of $v$, costing $O(m)$.
- Each butterfly costs $O(m)$: one bit-shift plus two modular additions.
- Total: $N/2 \cdot \log_2 N$ butterflies, each $O(m)$, giving $O(Nm \log N)$ bit operations.

### Step 3: Pointwise multiplication

Compute $\hat{c}_k = \hat{a}_k \cdot \hat{b}_k$ in $R$ for each $k = 0, \ldots, N - 1$.

Each of these is a multiplication of two $m$-bit numbers modulo $2^m + 1$. But wait -- this is itself a multiplication of smaller numbers! This is where the algorithm becomes **recursive**: we use the Schönhage-Strassen algorithm itself (on inputs of size $m$ instead of $n$) to perform these multiplications.

There are $N$ such multiplications, each on operands of size $m$. This is the "recursive nesting" that generates the $\log \log n$ factor.

### Step 4: Inverse NTT

Compute $\mathbf{c} = \text{INTT}_N(\hat{\mathbf{c}})$. Same cost as the forward NTT: $O(Nm \log N)$.

### Step 5: Carry propagation and reassembly

The vector $\mathbf{c}$ now contains the convolution of $\mathbf{a}$ and $\mathbf{b}$ modulo $2^m + 1$. (The parameters are chosen so that no coefficient is large enough to "wrap around" the modulus -- the modulus is larger than any possible convolution coefficient.) Reassemble the final product by performing carries across the chunks.

## Why $\log \log n$?

The complexity breaks down as follows. At the top level we have:
- NTT and INTT: $O(Nm \log N)$ bit operations for the transforms.
- Pointwise multiplications: $N$ recursive multiplications on $m$-bit inputs.

With $K \approx \sqrt{n}$ and $m \approx \sqrt{n}$, the recurrence is roughly:

$$
T(n) = O\!\left(\sqrt{n} \cdot T(\sqrt{n})\right) + O(n \log n)
$$

Let us trace the recursion. At depth $d$, the problem size is $n^{1/2^d}$. The recursion bottoms out when $n^{1/2^d} = O(1)$, which requires $2^d \approx \log n$, giving a recursion depth of $d = O(\log \log n)$.

At each recursion level, the non-recursive work is $O(n \log n)$ (the NTTs). Summing over $O(\log \log n)$ levels:

$$
T(n) = O(n \log n \cdot \log \log n)
$$

This is the Schönhage-Strassen bound. The $\log \log n$ factor is not a deficiency of the FFT itself -- the FFT is $O(n \log n)$. It is the cost of the **recursive multiplications** needed at each level of the NTT.

## A Comparison

| Algorithm             | Complexity                     | Key Innovation                        |
|-----------------------|--------------------------------|---------------------------------------|
| Schoolbook            | $O(n^2)$                       | Direct digit-by-digit                 |
| Karatsuba             | $O(n^{1.585})$                 | 4 multiplications $\to$ 3            |
| Toom-3                | $O(n^{1.465})$                 | 9 multiplications $\to$ 5            |
| Schönhage-Strassen    | $O(n \log n \log \log n)$      | NTT in $\mathbb{Z}/(2^m+1)$         |
| Harvey-van der Hoeven | $O(n \log n)$                  | Multi-dimensional NTT (see below)    |

The jump from Toom-Cook to Schönhage-Strassen is qualitatively different from all previous improvements. Karatsuba and Toom-Cook are algebraic tricks that reduce the exponent toward 1 but never reach it. Schönhage-Strassen breaks through to a *nearly-linear* bound by replacing polynomial interpolation at finitely many points with Fourier analysis at the roots of unity -- and crucially, by doing so in an exact algebraic ring where the symmetry of the roots makes the transform cheap.

The remaining $\log \log n$ factor is the residue of recursive nesting. Eliminating it required the multi-dimensional approach of Harvey and van der Hoeven (2019), which we now discuss.

# Harvey-van der Hoeven: $O(n \log n)$

## The Last Factor Standing

We have arrived at the final chapter. Let us take stock of where we are.

You now understand that multiplying two $n$-digit integers is really computing a convolution of their digits. You understand that the FFT evaluates a polynomial at all $N$-th roots of unity in $O(N \log N)$ time, and that the Convolution Theorem lets us turn this evaluation into multiplication. You understand that Schönhage and Strassen sidestepped floating-point precision by working in the ring $\mathbb{Z}/(2^m + 1)\mathbb{Z}$, where twiddle factors are just bit-shifts.

And you understand the one blemish: the $\log \log n$ factor. It comes from the fact that the NTT's pointwise multiplications are themselves multiplications on smaller numbers, requiring their own NTTs, which require their own pointwise multiplications, and so on. The recursion bottoms out after $\log \log n$ levels, each contributing $O(n \log n)$ work. Multiply those together: $O(n \log n \log \log n)$.

For 48 years -- from 1971 to 2019 -- nobody could kill that last factor. Then David Harvey and Joris van der Hoeven did.

## The Intuition: Why $\log \log n$ Exists and How to Eliminate It

To understand the fix, we first need a sharper picture of the disease.

### The disease: a long chain of recursive calls

In Schönhage-Strassen, we split our $n$-bit number into $K \approx \sqrt{n}$ chunks of $m \approx \sqrt{n}$ bits each. The NTT on these chunks is cheap (just bit-shifts and additions), but the **pointwise multiplications** -- the $K$ products of $m$-bit numbers in $\mathbb{Z}/(2^m+1)$ -- each require a recursive call to the entire algorithm.

At the next level down, each $m$-bit multiplication splits into $\sqrt{m}$ chunks of $\sqrt{m}$ bits, and so on. The problem sizes form a chain:

$$
n \;\to\; \sqrt{n} \;\to\; n^{1/4} \;\to\; n^{1/8} \;\to\; \cdots \;\to\; O(1)
$$

This chain has $\log \log n$ links (since $n^{1/2^d} = O(1)$ when $2^d \approx \log n$, giving $d \approx \log \log n$). Each link does $O(n \log n)$ work in total. The $\log \log n$ factor is simply the number of links in this chain.

### The cure: make the chain shorter

Harvey and van der Hoeven's idea, at its core, is beautifully simple: **if the recursion depth is the problem, reduce the recursion depth.**

Instead of splitting into $\sqrt{n}$ pieces (which halves the exponent at each level), split into **far more** pieces that are **far smaller**. If you split an $n$-bit number into $n/\log n$ pieces of $\log n$ bits each, then the recursive subproblems have size $\log n$ -- which is already small enough to multiply by schoolbook in $O((\log n)^2)$ time! The recursion bottoms out in a single step. No chain. No $\log \log n$.

But this creates a new problem. With $n / \log n$ chunks, the NTT must operate on a sequence of length $\sim n / \log n$, and the transform must happen in a ring large enough to hold the convolution without overflow. Finding a ring that simultaneously supports (a) cheap roots of unity, (b) sufficiently many of them, and (c) exact arithmetic with no precision loss -- all while keeping the transform cost to $O(n \log n)$ -- is the hard part. This is where the paper earns its 80 pages.

## The Architecture: Three Key Ideas

### Idea 1: Fold the sequence into a multi-dimensional array

Rather than treating the $n / \log n$ chunks as a flat list, Harvey and van der Hoeven reshape them into a $d$-dimensional array of size $s_1 \times s_2 \times \cdots \times s_d$, where each $s_i$ is a small prime and $\prod s_i \approx n / \log n$.

Why does this help? A $d$-dimensional convolution can be computed by performing **1-dimensional DFTs along each dimension** in succession (this is the standard "row-column" algorithm for multidimensional transforms). If each dimension $s_i$ is small, each 1D DFT is cheap. And crucially, the total number of 1D DFT operations is:

$$
\text{cost} = \sum_{i=1}^{d} \frac{S}{s_i} \cdot (\text{cost of a length-}s_i\text{ DFT})
$$

where $S = \prod s_i$. By choosing $d$ to grow with $n$ (specifically, $d \sim \log n / \log \log n$), each $s_i$ stays bounded by a constant, and the DFTs along each dimension have constant cost per element. The total transform cost is $O(S \cdot d) = O\!\left(\frac{n}{\log n} \cdot \frac{\log n}{\log \log n}\right) = O\!\left(\frac{n}{\log \log n}\right)$, which is well within the $O(n \log n)$ budget.

The problem is that the Cooley-Tukey radix-2 trick does not work on prime-sized dimensions. This is where the second idea comes in.

### Idea 2: Gaussian resampling -- making primes act like powers of 2

The Cooley-Tukey FFT requires the transform length to be a power of 2 (or at least highly composite). The dimensions $s_i$ are primes. How do we bridge this gap?

Harvey and van der Hoeven use a technique inspired by **Bluestein's algorithm**, but with a Gaussian twist. The idea is:

1. Embed the length-$s_i$ DFT into a slightly larger length-$t_i$ **cyclic convolution**, where $t_i$ is the next power of 2 above $s_i$.

2. Compute this cyclic convolution using Nussbaumer's algorithm (a multiplication-free polynomial transform), which only needs additions, subtractions, and cyclic shifts.

3. The "embedding" is done via multiplication by a **Gaussian chirp** -- a sequence of the form $e^{\pi i k^2 / s_i}$. The Gaussian chirp has the remarkable property that it converts a DFT into a convolution (this is the classical "chirp-$z$ transform" idea of Bluestein). And because the Gaussian is approximately its own Fourier transform, the approximation errors when rounding $s_i$ up to $t_i$ can be made exponentially small with only $O(1)$ extra bits of precision.

The net effect: each prime-sized DFT is replaced by a power-of-2-sized convolution that can be computed without any multiplications in the traditional sense -- only additions and shifts. The cost per element remains $O(1)$.

### Idea 3: Nussbaumer's algorithm -- transforms without multiplications

The inner convolutions (from Idea 2) are computed using **Nussbaumer's polynomial transform**, which operates over the ring $R[y]/(y^r + 1)$ for $r$ a power of 2. In this ring:

- Multiplication by $y$ is a **cyclic shift** (free, like multiplying by $2$ in $\mathbb{Z}/(2^m + 1)$ was free for Schönhage-Strassen).
- The transform uses only $O(r \log r)$ additions and subtractions -- **no multiplications** at this level.

This is the key that breaks the recursive chain. In Schönhage-Strassen, the pointwise multiplications in the NTT were genuine multiplications that demanded recursive calls. In Harvey-van der Hoeven, the analogous step uses Nussbaumer transforms that need **no multiplications**, only shifts and additions. No recursive call is needed. The chain has been cut.

The only remaining multiplications are tiny: each "pointwise product" in the Nussbaumer-transformed domain amounts to a multiplication of numbers with $O(\log n)$ bits, which can be done by schoolbook in $O((\log n)^2)$ time -- a cost that is absorbed into the $O(n \log n)$ total.

## How the Pieces Fit Together

The full algorithm, stripped to its skeleton:

1. **Split** the $n$-bit inputs into $S \approx n / \log n$ chunks of $\sim \log n$ bits each.

2. **Reshape** the chunk sequence into a $d$-dimensional array ($d \sim \log n / \log \log n$ dimensions, each of prime size $s_i = O(\log \log n)$).

3. **For each dimension** $i = 1, \ldots, d$:
   - Apply the Gaussian chirp to convert the length-$s_i$ DFT along that dimension into a cyclic convolution of length $t_i = O(s_i)$.
   - Compute that cyclic convolution using Nussbaumer's addition-only polynomial transform.

4. **Pointwise multiply** the transformed arrays. Each pointwise product involves numbers of $O(\log n)$ bits -- small enough for schoolbook.

5. **Invert** the multidimensional transform (same process in reverse).

6. **Carry-propagate** and reassemble the final product.

The total cost at each step:
- Steps 3 and 5 (transforms): $O(n)$ additions across $d$ dimensions, times $d = O(\log n / \log \log n)$, giving $O(n \log n / \log \log n)$ -- well within budget.
- Step 4 (pointwise): $S$ multiplications of $O(\log n)$-bit numbers at $O((\log n)^2)$ each, giving $O(n \log n)$.
- Steps 1, 2, 6: $O(n)$.

**Total: $O(n \log n)$.**

## Why 1729?

The algorithm's correctness depends on the Gaussian resampling errors being negligible, which requires extra precision bits. The number of extra bits grows with $d$, and $d$ grows with $n$. Working through the constants, the algorithm only becomes faster than Schönhage-Strassen when $n$ is so large that the constant-factor overhead of managing $d$ dimensions, Gaussian chirps, and Nussbaumer bookkeeping is finally absorbed.

Harvey and van der Hoeven estimate this crossover at numbers with more than $2^{1729^{12}}$ digits.

The appearance of **1729** -- Ramanujan's famous "taxicab number," the smallest number expressible as the sum of two cubes in two different ways -- is a coincidence, but a poetic one. The number arises from a chain of parameter optimizations in the proof, not from any deep connection to Ramanujan's work. But it is fitting that the algorithm that closes the book on multiplication complexity should bear, in its constant, an echo of one of mathematics' most beautiful stories.

To put $2^{1729^{12}}$ in perspective:
- The observable universe contains roughly $10^{80}$ atoms.
- $2^{1729^{12}}$ has approximately $10^{38}$ decimal digits in its *exponent alone*.
- If every atom in the universe were a hard drive, and every hard drive stored $10^{15}$ digits, you could store roughly $10^{95}$ digits. This is *nothing* compared to $2^{1729^{12}}$.

This is a **galactic algorithm** -- beautiful, true, and utterly useless for any computation that will ever be performed in the physical universe. But its existence answers a question that stood open for sixty years: **can multiplication be done in $O(n \log n)$?** The answer is yes.

## The View from the Summit

Let us look back at the full arc:

| Year | Algorithm | Complexity | Key Insight |
|------|-----------|-----------|-------------|
| antiquity | Schoolbook | $O(n^2)$ | Every digit meets every digit |
| 1960 | Karatsuba | $O(n^{1.585})$ | One clever identity saves 25% per level |
| 1963 | Toom-Cook | $O(n^{1+\varepsilon})$ for any $\varepsilon > 0$ | Polynomial interpolation at $k$ points |
| 1971 | Schönhage-Strassen | $O(n \log n \log \log n)$ | NTT in $\mathbb{Z}/(2^m+1)$; roots of unity via bit-shifts |
| 2019 | Harvey-van der Hoeven | $O(n \log n)$ | Multi-dim NTT; Nussbaumer kills the recursion |

Each breakthrough changed the *kind* of mathematics being used. Karatsuba's was an algebraic identity. Toom-Cook was polynomial algebra. Schönhage-Strassen was number-theoretic harmonic analysis. Harvey-van der Hoeven is multi-dimensional algebraic geometry fused with analytic number theory.

And yet the punchline is the same as it was in the schoolbook algorithm: we are still just multiplying digits together and adding up the results. Every advance has been about finding a cleverer *order* in which to do it.

# Connections to Sorting Algorithms

We have just traced the 60-year journey from $O(n^2)$ to $O(n \log n)$ for integer multiplication. But if you have studied algorithms before, that destination -- $O(n \log n)$ -- should feel familiar. It is the same complexity that governs comparison-based sorting: Merge Sort, Heapsort, and any optimal sorting algorithm all run in $\Theta(n \log n)$ time.

Is this a coincidence? It is not. The connection runs deep, and understanding it illuminates *why* $n \log n$ appears as a fundamental barrier across seemingly unrelated problems.

## The Information-Theoretic Lower Bound

The $n \log n$ term does not arise from any particular algorithmic trick. It arises from **entropy** -- from the sheer amount of information that must be processed to solve the problem at all.

### Sorting: Counting Permutations

Consider sorting $n$ elements. The input is some unknown permutation of $\{1, 2, \ldots, n\}$, and the algorithm must determine *which* of the $n!$ possible permutations it is looking at. Every comparison-based sorting algorithm can be modeled as a binary decision tree: at each internal node, the algorithm compares two elements and branches left or right. The leaves of this tree correspond to the $n!$ possible outcomes.

A binary tree with $L$ leaves has depth at least $\log_2 L$. Since our tree must have at least $n!$ leaves:

$$
\text{depth} \;\geq\; \log_2(n!)
$$

Stirling's approximation gives us:

$$
\log_2(n!) \;=\; \sum_{k=1}^{n} \log_2 k \;=\; n \log_2 n - n \log_2 e + O(\log n) \;=\; \Theta(n \log n)
$$

Each comparison provides at most 1 bit of information (left or right). Therefore, *any* comparison-based sorting algorithm must make at least $\Omega(n \log n)$ comparisons in the worst case. This is not a statement about any particular algorithm -- it is a statement about the *information content* of the problem itself.

### Multiplication: Counting Convolutions

Now consider multiplying two $n$-bit integers. The output is a $2n$-bit number, and each output bit can depend on every input bit from both operands. The "mixing" that must occur -- the convolution of $n$ digits with $n$ digits -- produces $2n - 1$ output coefficients, each of which is a sum of products involving up to $n$ terms.

The information-theoretic argument here is more subtle than in sorting (and, crucially, a tight $\Omega(n \log n)$ lower bound for integer multiplication has *not* been formally proven -- this remains a major open problem). But the heuristic reasoning is compelling: the FFT is the canonical way to compute a length-$n$ convolution, and the FFT requires $\frac{n}{2} \log_2 n$ butterfly operations, each combining two values. The data must pass through $\log_2 n$ stages, with $O(n)$ work per stage. Any algorithm that computes the same convolution must, in some sense, perform the same total information routing.

The structural parallel is striking:

| | **Sorting** | **Multiplication** |
|---|---|---|
| **Problem** | Identify one permutation out of $n!$ | Compute a convolution of $n$ coefficients |
| **Information content** | $\log_2(n!) = \Theta(n \log n)$ bits | $\Theta(n \log n)$ bits of mixing (conjectured) |
| **Per-step bandwidth** | $O(n)$ comparisons | $O(n)$ butterfly operations |
| **Minimum steps** | $\Omega(\log n)$ | $\Omega(\log n)$ |
| **Total work** | $\Omega(n \log n)$ | $O(n \log n)$ (achieved by HvH) |

Both problems hit the same wall: $n$ data items that must be "mixed" through $\log n$ stages of $O(n)$ work each.

## The Symmetry of the Recurrence

Beyond the information-theoretic parallel, there is an algebraic one: both optimal sorting and optimal multiplication satisfy the same *recurrence relation*.

### Merge Sort

Merge Sort divides $n$ elements into two halves, recursively sorts each half, and merges the results in $O(n)$ time:

$$
T(n) = 2\,T\!\left(\frac{n}{2}\right) + O(n)
$$

By the Master Theorem (Case 2: $a = 2$, $b = 2$, $f(n) = O(n)$, so $n^{\log_b a} = n^1 = n = f(n)$), this solves to:

$$
T(n) = O(n \log n)
$$

### Harvey-van der Hoeven Multiplication

The HvH algorithm decomposes an $n$-coefficient convolution into $K$ sub-convolutions of size $n/K$ each, with $O(n)$ work for the FFT and pointwise operations at each level:

$$
T(n) = K \cdot T\!\left(\frac{n}{K}\right) + O(n)
$$

This is the *same* Master Theorem case regardless of $K$: we have $a = K$, $b = K$, $n^{\log_b a} = n^1 = n = f(n)$, giving:

$$
T(n) = O(n \log n)
$$

The recurrences are structurally identical. In both cases, the algorithm splits the problem into $K$ pieces of size $n/K$ and does $O(n)$ work to split and recombine. The $\log n$ factor is simply the depth of the recursion tree: $\log_K n$ levels, each costing $O(n)$. The particular value of $K$ (2 for Merge Sort, $\sqrt{n}$ for Schönhage-Strassen, a carefully chosen composite for HvH) affects the constant factors but not the asymptotic complexity.

The critical difference is that Schönhage-Strassen's "recombine" step secretly contains *additional recursive multiplications* -- the pointwise products in $\mathbb{Z}/(2^m + 1)$ -- which add a $\log \log n$ overhead atop the clean recurrence. Harvey and van der Hoeven's achievement was making the recombine step *truly* $O(n)$ by using Nussbaumer's technique to eliminate those inner multiplications. Once they did, the recurrence collapsed to the same clean form as Merge Sort, and $O(n \log n)$ fell out immediately.

## The Hypercube: A Shared Geometry

The deepest way to see the connection is through the lens of **communication on a hypercube** -- a model that unifies both algorithms geometrically.

### What is a Hypercube?

A $d$-dimensional hypercube $Q_d$ is a graph with $2^d$ nodes. Each node is labeled by a $d$-bit binary string, and two nodes are connected by an edge if and only if their labels differ in exactly one bit. For example, $Q_3$ (the 3-cube) is the familiar wireframe cube with 8 vertices and 12 edges.

Three properties make the hypercube the natural "arena" for divide-and-conquer algorithms:

1. **Recursive decomposition.** $Q_d$ consists of two copies of $Q_{d-1}$ joined by edges along the $d$-th coordinate. This mirrors the way both Merge Sort and FFT-based multiplication split their input in half (or into $K$ parts) at each level.

2. **Logarithmic diameter.** Despite having $N = 2^d$ nodes, the longest shortest path in $Q_d$ has length $d = \log_2 N$. Any piece of information can reach any other node in at most $\log N$ steps. This is the geometric origin of the $\log n$ factor.

3. **Vertex symmetry.** Every node in $Q_d$ looks structurally identical to every other node -- there are no bottlenecks, no privileged positions. This ensures that the algorithm's workload is evenly distributed across all data items.

### Sorting on the Hypercube

To sort $n$ elements on a hypercube, we can use **Bitonic Sort** (Batcher, 1968). The idea is to treat the $n$ array positions as the $n$ nodes of a hypercube ($d = \log_2 n$ dimensions) and perform *compare-exchange* operations along each dimension sequentially.

In a single step along one dimension, the hypercube supports $n/2$ parallel comparisons -- one across each edge in that dimension. This is the *bandwidth* of one dimension: $O(n)$ bits of information resolved per step.

There are $d = \log_2 n$ dimensions, and each dimension requires $O(d)$ compare-exchange rounds in Bitonic Sort, giving $O(\log^2 n)$ parallel steps. (An asymptotically optimal sorting network, like the AKS network, achieves $O(\log n)$ parallel steps, fully saturating the hypercube's bandwidth.)

The total work is:

$$
\underbrace{O(n)}_{\text{comparisons per step}} \;\times\; \underbrace{O(\log n)}_{\text{steps}} \;=\; O(n \log n)
$$

The $n \log n$ is precisely the entropy of $n!$ permutations being drained at a rate of $O(n)$ bits per step over $O(\log n)$ steps. When every lane of the hypercube is fully utilized at every step, we say the algorithm **saturates the bandwidth**. No sorting algorithm can do better, because there is no more information capacity to exploit.

### Multiplication on the Hypercube

Now consider the FFT butterfly network for an $n$-point transform. Draw it as a diagram with $\log_2 n$ stages, each consisting of $n/2$ butterfly operations. If you squint at this diagram, you will notice something: *it is a hypercube*. Each butterfly connects two nodes whose indices differ in exactly one bit position (the bit corresponding to that stage). The FFT literally routes data along the edges of $Q_d$.

In Schönhage-Strassen, this hypercube routing is not quite "clean." The pointwise multiplications at each stage are themselves recursive FFTs on smaller hypercubes, creating a nested hierarchy. The nesting depth is $\log \log n$, and the overhead at each level prevents the algorithm from fully saturating the bandwidth of the outer hypercube. There is "congestion" -- some lanes carry recursive sub-computations instead of direct data movement.

Harvey and van der Hoeven's breakthrough was, in geometric terms, a way to *eliminate the congestion*. By lifting the one-dimensional convolution into a multi-dimensional array and choosing the dimensions so that Nussbaumer's technique replaces the recursive multiplications with additions and cyclic shifts, they ensured that the FFT butterfly at each level performs *pure data routing* -- no hidden recursive work, no congestion. Every lane of the hypercube carries useful information at every step.

The result: multiplication, like sorting, saturates the hypercube's bandwidth. Both algorithms move $O(n)$ units of information per step across $O(\log n)$ steps, for a total of $O(n \log n)$. The two problems -- one about ordering elements, the other about convolving digits -- are solved by the *same geometric machine*.

## Sorting *Is* Multiplying. Multiplying *Is* Sorting.

We can now say something stronger than "sorting and multiplication are *analogous*." They are, in a precise algebraic sense, the *same operation* -- projections of a single underlying phenomenon onto different mathematical surfaces.

### The Shared Abstraction: Rearranging Information Across Dimensions

Consider what sorting actually does. You have $n$ data items, each sitting at some position. The items are "tangled" -- their current positions bear no relation to their values. To sort is to *untangle* them: to route each item from its current position to its correct position. The difficulty of sorting is exactly the difficulty of this routing problem. The items must move through a network (comparisons, swaps), and the network has finite bandwidth. The entropy $\log_2(n!)$ measures the total amount of routing information that must be resolved. The $n \log n$ is the cost of pushing that information through the $\log n$ dimensions of a hypercube, one dimension at a time.

Now consider what multiplication does. You have $n$ coefficients in one polynomial and $n$ coefficients in another. Each output coefficient of the product is a sum of terms $a_i \cdot b_j$ where $i + j$ equals the output index. The coefficients are "tangled" -- every input coefficient contributes to multiple output coefficients, and the contributions overlap. To multiply is to *untangle* them: to route each partial product $a_i \cdot b_j$ to its correct output position $i + j$ and accumulate the results. The FFT does this by decomposing the routing into $\log n$ stages of butterfly operations, each resolving one "dimension" of the entanglement.

Strip away the surface details -- the comparisons, the twiddle factors, the carry propagation -- and you are left with the same skeleton:

> **$n$ items are entangled across $\log n$ dimensions. Untangling them requires touching all $n$ items once per dimension. The cost is $n \log n$.**

Sorting untangles *order*. Multiplication untangles *convolution*. But "untangling" is the same verb in both sentences, and $n \log n$ is its conjugation.

### Making It Algebraic

We can make this even more precise. Both problems can be formulated as applying a *linear transform* to a vector of length $n$:

- **Sorting** is the application of a *permutation matrix* $P \in \{0,1\}^{n \times n}$ to the input vector. The "problem" is that we don't know which permutation matrix to apply until we've inspected the data. The decision tree that determines $P$ has depth $\Omega(\log_2(n!)) = \Omega(n \log n)$.

- **Multiplication** (via convolution) is the application of a *circulant matrix* $C \in \mathbb{Z}^{n \times n}$ to the input vector, where $C_{ij} = b_{(i-j) \bmod n}$. The FFT diagonalizes this circulant: $C = F^{-1} \hat{C} F$, where $F$ is the DFT matrix and $\hat{C}$ is diagonal. The cost of applying $F$ and $F^{-1}$ is $O(n \log n)$.

In both cases, we are applying a structured matrix to a vector of $n$ elements. The permutation matrix has $n!$ possible forms; the circulant matrix has $n$ free parameters but acts on a pair of inputs, yielding $O(n)$ degrees of freedom in the output. The algebraic structure of these matrices -- their factorization into sparse stages, their decomposition along the dimensions of a hypercube -- is *identical*. The DFT matrix $F$ factors into $\log n$ stages of sparse butterfly matrices. A sorting network factors into $\log n$ stages of sparse comparison-swap matrices. Both are "hypercube decompositions" of their respective transforms.

This is why the same $n \log n$ appears. It is not a coincidence, not a vague analogy, not a metaphor. It is the same theorem applied to two different matrix families.

### The Linearithmic Manifold

There is a beautiful way to see all of this in a single picture. Imagine a space of all "rearrangement problems" on $n$ items -- every computational task whose essence is routing $n$ pieces of information to their correct destinations through a network of finite bandwidth. Call this the **linearithmic manifold**: the space of problems whose optimal solutions require $\Theta(n \log n)$ operations.

Sorting lives on this manifold: $n$ items, $n!$ possible destinations, $\log n$ dimensions of routing.

Multiplication lives on this manifold: $n$ coefficients, $2n - 1$ output positions, $\log n$ dimensions of spectral decomposition.

The Fast Fourier Transform lives on this manifold: $n$ time-domain samples, $n$ frequency-domain samples, $\log n$ butterfly stages.

Even matrix transposition on a $\sqrt{n} \times \sqrt{n}$ matrix lives on this manifold: $n$ entries, each needing to swap its row and column coordinates, requiring $\Theta(n \log n)$ cache misses in the I/O model.

These problems are not merely "similar in complexity." They are *manifestations of the same geometric constraint*: the constraint that moving $n$ items across $\log n$ dimensions, with $O(n)$ bandwidth per dimension, costs exactly $n \log n$. The linearithmic manifold is not a metaphor -- it is the deep reason that $n \log n$ recurs so obsessively across computer science.

Sorting is multiplying in the permutation dimension.
Multiplying is sorting in the convolution dimension.
They are the same mountain, seen from different valleys.

---

# Conclusion: The Structure of Computation Itself

## What We've Witnessed

Let us step back and take in the full panorama.

We began with the schoolbook algorithm -- a method so natural, so seemingly inevitable, that Andrey Kolmogorov, one of the greatest mathematicians of the twentieth century, stood before his seminar in 1960 and conjectured that its $O(n^2)$ cost was a law of nature. Multiplication, he believed, was inherently quadratic. Every digit of one number must "see" every digit of the other, and there is no shortcut around that combinatorial explosion.

He was wrong within a week.

What Karatsuba discovered was not merely a faster algorithm. It was a *philosophical* rupture. The schoolbook method treats multiplication as a flat, two-dimensional grid: row meets column, partial product accumulates, carry propagates. Karatsuba's trick -- computing three half-size products where four seemed necessary -- revealed that this grid was not a law of arithmetic but an *artifact of how we happened to organize the computation*. The digits still meet. The partial products still accumulate. But by choosing a cleverer grouping, by exploiting the algebraic identity $(x_1 + x_0)(y_1 + y_0) = x_1 y_1 + x_1 y_0 + x_0 y_1 + x_0 y_0$, Karatsuba showed that some of those meetings are redundant -- their information content is already captured elsewhere.

This is the thread that runs through everything we've seen.

## The Changing Language of Speedup

Each breakthrough in this story didn't just produce a faster algorithm; it changed the *mathematical language* in which multiplication is expressed.

**Karatsuba** spoke the language of **algebra**: a single polynomial identity turns four sub-problems into three, and the Master Theorem does the rest. The savings are modest -- $O(n^{1.585})$ versus $O(n^2)$ -- but the conceptual leap is enormous. For the first time, the exponent on multiplication was negotiable.

**Toom-Cook** generalized this into the language of **polynomial interpolation**. If splitting a number in two and evaluating at three points (Karatsuba) drops the exponent to $\log_2 3$, then splitting into $k$ pieces and evaluating at $2k - 1$ points drops it to $\log_k (2k - 1)$. As $k$ grows, the exponent approaches $1 + \varepsilon$ for any $\varepsilon > 0$. This was the first hint that $O(n^{1+\varepsilon})$ was not the floor -- that perhaps the true cost of multiplication is not polynomial in $n$ at all, but something closer to $n$ times a slowly growing function.

**Schönhage-Strassen** rewrote multiplication in the language of **harmonic analysis**. The Convolution Theorem -- the deep fact that convolution in the time domain becomes pointwise multiplication in the frequency domain -- transforms the entire problem. Instead of asking "how do I combine digits?", we ask "how do I move between representations of a polynomial?" The Fast Fourier Transform answers that question in $O(n \log n)$ time. But the need for exact integer arithmetic, not floating-point approximations, forced Schönhage and Strassen into the ring $\mathbb{Z}/(2^m + 1)\mathbb{Z}$, where roots of unity are powers of two and "multiplication by a twiddle factor" is just a bit-shift. The cost of this exactness was a recursive structure whose depth -- $\log \log n$ levels -- contributed a stubborn extra factor.

**Harvey and van der Hoeven** completed the journey by fusing **multi-dimensional algebraic geometry** with **analytic number theory**. Their insight was architectural: by lifting the one-dimensional convolution into a multi-dimensional array, choosing dimensions via Gaussian integers in $\mathbb{Z}[i]$ to ensure coprimality, and using Nussbaumer's trick to eliminate the innermost recursive multiplications entirely, they flattened the recursive chain from $\log \log n$ levels to a constant. The $O(n \log n)$ barrier -- conjectured for decades, tantalizingly close since 1971 -- was finally reached.

The mathematical toolkit escalated at every stage: from high-school algebra, to polynomial interpolation, to Fourier analysis over finite rings, to algebraic geometry over Gaussian integers. And yet -- and this is the remarkable part -- the *problem never changed*. At every stage, we are still multiplying two numbers. We are still computing the same convolution of digits, still propagating the same carries. What changed is our understanding of the *geometry* of the computation: the realization that there exist clever rearrangements of the same arithmetic operations that cancel redundancies invisible from the schoolbook perspective.

## The Information-Theoretic Floor

Is $O(n \log n)$ truly optimal? We cannot prove it is, but there are strong reasons to believe it.

Multiplying two $n$-bit numbers produces a $2n$-bit result. Each bit of the output can depend on every bit of both inputs. The information that must flow through the computation -- the "mixing" of input bits into output bits -- is at least $\Omega(n \log n)$ by plausible circuit-complexity arguments, though a formal proof remains one of the great open problems in theoretical computer science.

What we *can* say is that multiplication has reached the same complexity class as sorting: $\Theta(n \log n)$. And as we showed in the previous section, this is not a coincidence -- it is the *same theorem*. Both problems live on what we called the linearithmic manifold: the space of computational tasks whose essence is routing $n$ pieces of information across $\log n$ dimensions of a finite-bandwidth network. Sorting routes elements to their correct positions in the permutation dimension. Multiplication routes partial products to their correct positions in the convolution dimension. The $n \log n$ is not an accident of algorithmic cleverness -- it is the price the universe charges for untangling $n$ things, regardless of *what* those things are or *why* they are tangled.

## Galactic Algorithms and the Nature of Truth

We should be honest about the practical situation. Karatsuba's algorithm overtakes schoolbook multiplication at around 20-40 digits, depending on the implementation. Toom-Cook-3 wins around 100-200 digits. Schönhage-Strassen becomes competitive at tens of thousands of digits -- the scale used by modern big-integer libraries like GMP. But Harvey-van der Hoeven? Its crossover point is somewhere beyond $2^{1729^{12}}$ digits. That number has more digits than there are atoms in the observable universe. No computer that will ever exist will multiply numbers that large. The Harvey-van der Hoeven algorithm will never be *run*.

And yet it matters enormously.

It matters because mathematics is not engineering. The question "what is the true complexity of integer multiplication?" is a question about the structure of arithmetic itself, not about what silicon can compute before the heat death of the universe. The existence of an $O(n \log n)$ algorithm -- even one that is galactically impractical -- tells us something true about the nature of numbers: that the information required to multiply them is not quadratic, not $n^{1.585}$, not $n \log n \log \log n$, but $n \log n$. That is a *theorem about reality*, not a software optimization.

Galactic algorithms are the astronomer's telescope pointed at the foundations of computation. We will never travel to a quasar, but knowing it exists changes our understanding of the universe. Similarly, we will never run Harvey-van der Hoeven on actual inputs, but knowing it exists changes our understanding of what multiplication *is*.

## The Punchline

Here is the thought to carry away.

Kolmogorov looked at schoolbook multiplication and saw $n^2$ -- a grid of partial products, rigid and inescapable. Karatsuba looked at the same grid and saw that some cells were redundant. Toom and Cook saw that the grid was really a polynomial, and polynomials can be evaluated at fewer points than their degree suggests. Schönhage and Strassen saw that the polynomial was really a signal, and signals can be decomposed into frequencies. Harvey and van der Hoeven saw that the signal lived in a multi-dimensional space whose geometry could be exploited to eliminate every last bit of overhead.

Each generation looked at the *same object* -- the product of two integers -- and saw deeper structure. The number didn't change. Our eyes did.

And when, at the end of this journey, we looked sideways and noticed that sorting -- a completely different problem about ordering, not arithmetic -- lands at exactly the same $n \log n$ cost for exactly the same geometric reasons, we glimpsed something deeper still. Sorting is multiplying in the permutation dimension. Multiplying is sorting in the convolution dimension. They are two faces of a single truth: that rearranging $n$ things across $\log n$ dimensions of entanglement costs $n \log n$, and not a single operation less.

That, in the end, is what mathematics is: the systematic refinement of vision. The history of multiplication algorithms is not a story about making computers faster. It is a story about learning to see -- and discovering, at the bottom, that everything we were looking at was the same thing all along.

---

## Further Reading
Wonderful Wikipedia : https://en.wikipedia.org/wiki/Multiplication_algorithm

Exploration of Varying Radix on Intel i3-4025U : https://miracl.com/blog/missing-a-trick-karatsuba-variations-michael-scott/

Karatsuba paper: https://ieeexplore.ieee.org/document/4402691

Toom-Cook: A. L. Toom, "The Complexity of a Scheme of Functional Elements Realizing the Multiplication of Integers" (1963); S. A. Cook, "On the Minimum Computation Time of Functions" (1966, PhD Thesis, Harvard)

Schönhage–Strassen paper: A. Schönhage and V. Strassen, "Schnelle Multiplikation großer Zahlen," *Computing* 7 (1971), pp. 281--292. https://doi.org/10.1007/BF02242355

Harvey and van der Hoeven's Paper : https://hal.archives-ouvertes.fr/hal-03182372/document