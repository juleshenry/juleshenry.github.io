---
layout: post
title: "On Multiplication"
date: 2025-12-19
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

# Hand-waving Schönhage–Strassen $O(n \log n \log \log n)$
## Schönhage–Strassen: The FFT Singularity

If Karatsuba was a clever algebraic trick and Toom-Cook was a dive into polynomial interpolation, the Schönhage–Strassen algorithm represents a fundamental departure from arithmetic altogether. It is the moment where number theory meets signal processing.

In 1971, Arnold Schönhage and Volker Strassen arrived at a complexity of $O(n \log n \log \log n)$, a bound so tight it remained the world champion for nearly half a century until the 2019 breakthrough mentioned in the introduction.

## The Signal Processing Pivot

To grasp Schönhage–Strassen, one must stop viewing an integer as a value and start viewing it as a signal.

When we multiply two numbers in grade school, we are essentially performing a convolution of their digits. If you multiply $(10a+b) \times (10c+d)$, you are blending the sequences of digits together. In the world of computer science, convolution in the "time domain" (or digit domain) is computationally expensive ($O(n^2)$).

However, a core tenet of the Convolution Theorem is that convolution in the time domain is equivalent to simple pointwise multiplication in the frequency domain.

## The Roots of Unity: A Mathematical Shortcut

The "hand-waving" magic happens via the Fast Fourier Transform (FFT).

Recall that Toom-Cook evaluated polynomials at arbitrary points like $0, 1$, and $-1$. Schönhage and Strassen realized that if you evaluate polynomials at complex roots of unity (points on the unit circle in the complex plane), the symmetry of these points allows for a massive recursive shortcut.

1. **Transform**: Treat the digits of your numbers as a signal and run an FFT to move them into the frequency domain.
2. **Multiply**: Multiply the transformed results pointwise (this is now incredibly fast).
3. **Inverse Transform**: Perform an Inverse FFT to bring the product back into the digit domain.
4. **Carry**: Perform a final pass to handle the carries, as the FFT results will be "blurred" across the digits.

## The Logarithmic Horizon

The brilliance of this approach is that the FFT takes only $O(n \log n)$ time. However, Schönhage–Strassen has a slight "tax" of $\log \log n$ because it has to handle the precision of the complex numbers or work within specific finite rings to avoid rounding errors.
| Algorithm                  | Complexity                   | Historical Context               |
|----------------------------|-----------------------------|----------------------------------|
| Karatsuba                  | $O(n^{1.58})$               | The 1960 breakthrough.           |
| Schönhage–Strassen         | $O(n \log n \log \log n)$   | The 1971 "unbeatable" standard.  |
| Harvey & van der Hoeven    | $O(n \log n)$               | The 2019 "theoretical perfection." |

# Hand-waving Harvey–van der Hoeven:  $O(n \log n)$
## Harvey–van der Hoeven: Reaching the Mathematical Horizon

If Schönhage–Strassen was the "unbeatable" champion for 48 years, the 2019 paper by David Harvey and Joris van der Hoeven is the closing of the book. For decades, the mathematical community conjectured that $O(n \log n)$ was the absolute theoretical floor—the "speed of light" for multiplication. Harvey and van der Hoeven finally proved it possible, effectively finishing a quest that began with Kolmogorov and Karatsuba in the 1960s.

But how do you shave off that last, pesky $\log \log n$ factor that haunted Schönhage–Strassen?

## The Problem: The Recursive "Tax"

In Schönhage–Strassen, the algorithm uses FFTs to multiply numbers, but those FFTs themselves require multiplications. To handle those, the algorithm calls itself recursively. Each level of this recursion adds a "tax" of $\log \log n$ to the complexity.

To reach the $O(n \log n)$ holy grail, the researchers had to find a way to perform the multiplication while keeping the "administrative overhead" from growing with the size of the number.
### The Solution: Multi-dimensional FFTs

The "hand-wavy" explanation is that Harvey and van der Hoeven moved from the 1-dimensional world of standard FFTs into multi-dimensional space.

Imagine your number not as a long string of digits (a line), but as a high-dimensional hypercube (a grid). By rearranging the data into many dimensions—specifically, they suggested using a very large number of dimensions—they could use a technique called "vectorized FFTs."

By spreading the computation across these dimensions, they could reduce the number of recursive steps required. Instead of the overhead stacking up as the numbers got larger, they managed to consolidate it.
### The "1729" Caveat: A Galactic Algorithm

While the proof is a masterpiece of modern mathematics, it belongs to the class of "Galactic Algorithms." These are algorithms that are theoretically superior but would only outperform existing methods on datasets so large they cannot exist in the observable universe.

As noted in the introduction, the "crossover point" where this algorithm becomes faster than Schönhage–Strassen is estimated at $2^{1729^{12}}$.

- For scale, there are roughly $10^{80}$ atoms in the observable universe.
- This number is so large it cannot even be written down in standard decimal notation without filling the entire universe with digits.

## Setup and Decomposition:
Split inputs into $\Theta(n / \log n)$ chunks.
Use the Chinese Remainder Theorem (CRT) to map the polynomial multiplication into a $d$-dimensional array convolution over complex numbers or a suitable ring.
Choose dimensions $s_1 \times s_2 \times \cdots \times s_d$ where each $s_i$ is a prime around $(n / \log n)^{1/d}$. This makes the total size $S \approx n / \log n$.

### Gaussian Resampling (The Magic Trick):
Direct multidimensional DFT on prime sizes would be slow or add log factors.
Instead, "resample" the input array using a Gaussian function (like a bell curve) to approximate the DFT.
This transforms the problem into a larger DFT of sizes $t_1 \times \cdots \times t_d$, where each $t_i$ is a power of 2 close to $s_i$.
Why Gaussian? It helps control errors when mapping frequencies between the irregular (prime) grid and the uniform (power-of-2) grid on a "torus" (think wrapped-around space).
Cost: This step uses linear maps with bounded norms, adding only $O(n \log n)$ work, and errors are tiny (handled by extra precision bits).

### Fast Evaluation with Synthetic FFTs:
Now compute the larger multidimensional DFT using Nussbaumer's polynomial transforms over rings like $\mathbb{C}[y] / (y^r + 1)$ (where $r$ is power of 2).
These "synthetic" FFTs mostly use additions/subtractions (cheap, $O(n)$) instead of multiplications.
Pointwise multiplications in the transformed space are done recursively (Kronecker substitution: flatten back to 1D integer mult).
Inverse DFT similarly to get back the convolution.

Recursion and Base Case:
Recurse on smaller subproblems (size roughly $n^{1/d + o(1)}$).
With large $d$, recursion depth is small, and total cost satisfies $M(n) \leq K \cdot n \cdot n' \cdot M(n') + O(n \log n)$, where $n' \ll n$, leading to $M(n) = O(n \log n)$.
For small $n$, fall back to $O(n^2)$.

## Discrete Fourier Transform (DFT) Primer

The Discrete Fourier Transform is a mathematical "prism." Just as a prism splits white light into its constituent colors (frequencies), the DFT takes a sequence of data and reveals the underlying periodic patterns.

In the context of multiplication, we treat our number $x$ as a vector of its digits: $\mathbf{a} = [a_0, a_1, \dots, a_{n-1}]$. We can think of these digits as the coefficients of a polynomial:
$$
A(x) = a_0 + a_1 x + a_2 x^2 + \dots + a_{n-1} x^{n-1}
$$

The DFT evaluates this polynomial at $n$ specific points: the complex roots of unity. These are points spaced evenly around the unit circle in the complex plane, defined as:
$$
\omega_n^k = e^{\frac{2\pi i k}{n}}
$$

By evaluating the polynomial at these symmetric points, the Fast Fourier Transform (FFT) can use a divide-and-conquer approach to compute all evaluations in $O(n \log n)$ time instead of the naive $O(n^2)$.
## Convolution Theorem

This is the "Secret Sauce" of modern high-speed multiplication.

When you multiply two polynomials, $A(x)$ and $B(x)$, the coefficients of the resulting polynomial $C(x)$ are the convolution of the coefficients of $A$ and $B$.

If $A = [1, 2, 3]$ and $B = [4, 5, 6]$, the standard way to find the product involves a "sliding" multiplication of every element against every other element. This is essentially what happens in grade-school multiplication when you shift rows and add them up.

The Convolution Theorem states:

**The Fourier Transform of a convolution is the pointwise product of the Fourier Transforms.**

Mathematically, if $F$ denotes the Fourier Transform and $\ast$ denotes convolution:
$$
F(A \ast B) = F(A) \cdot F(B)
$$

## The 3-Step Shortcut

Because of this theorem, we can bypass the $O(n^2)$ "sliding" convolution entirely:

1. **Forward Transform**: Compute $A' = \operatorname{FFT}(A)$ and $B' = \operatorname{FFT}(B)$ (time: $O(n \log n)$).
2. **Pointwise Product**: Multiply the corresponding elements: $C_i' = A_i' \cdot B_i'$ (time: $O(n)$).
3. **Inverse Transform**: Compute $C = \operatorname{IFFT}(C')$ (time: $O(n \log n)$).

The result $C$ is the vector of coefficients for our product. After a quick final pass to handle the carries (since coefficients in $C$ might be larger than our base), we have our answer. We have successfully traded the "quadratic wall" of grade-school multiplication for the "logarithmic slope" of the FFT.

## Butterflies and Hypercubes: Eliminating $O(\log \log n)$

In the standard Schönhage–Strassen approach, the $\log \log n$ factor is the "shadow" cast by recursion. To multiply two $n$-bit integers, the algorithm breaks them into $2^k$ chunks. But these chunks are themselves large, requiring their own FFTs, which require their own multiplications, and so on. This recursive nesting creates a depth of complexity that prevents a clean $O(n \log n)$ result.

To eliminate this, Harvey and van der Hoeven turned to the geometry of the Hypercube and the efficiency of the FFT Butterfly.

## The Butterfly: Exploiting Symmetry

At the heart of any FFT is the "Butterfly" operation. When we evaluate a polynomial at roots of unity, we notice that many of the calculations are redundant. For example, $\omega^k$ and $\omega^{k+n/2}$ are just negatives of each other on the unit circle.

The Butterfly unit takes two inputs, performs a single multiplication and an addition/subtraction, and produces two outputs. By nesting these butterflies, we create a network that processes data in stages. In a standard 1D FFT, we have $\log n$ stages, each doing $O(n)$ work.
## The Hypercube: Multi-dimensional Locality

The breakthrough in the $O(n \log n)$ proof involves treating the data not as a linear array, but as a multi-dimensional hypercube.

By mapping the digits of a massive integer onto a high-dimensional grid (say, a $d$-dimensional cube), the researchers could perform FFTs along each dimension independently. This is essentially a "divide-and-conquer" approach on the structure of the data itself.

- **Reduction of Recursive Depth**: In a 1D FFT, the recursion depth is tied directly to $n$. In a multi-dimensional FFT, you can process smaller blocks more efficiently, preventing the precision requirements (and thus the extra $\log \log n$ multiplications) from stacking up.
- **The "Unit Cost" Assumption**: By using a specific type of Number Theoretic Transform (NTT) across these dimensions, they ensured that the "work" done at each node of the hypercube remained constant relative to the total input.

## Closing the Loop

The transition from Schönhage–Strassen to Harvey–van der Hoeven is effectively the transition from a linear pipeline to a massively parallel hypercube network.

While the "Butterflies" do the heavy lifting of the transform, the "Hypercube" architecture ensures that the data is organized so that the recursive overhead—that pesky $\log \log n$—finally collapses into the main $O(n \log n)$ term.

We have reached the theoretical limit. There is no $O(n)$ multiplication; the act of "reading" the $n$ digits and "sorting" them through the $\log n$ stages of a butterfly network is the fundamental physical constraint of our universe.
# Connections to Sorting Algorithms
To establish a formal mathematical symmetry between the Harvey–van der Hoeven (HvH) multiplication algorithm and comparison-based sorting, we must look at them through the lens of Information Theory and the Divide-and-Conquer recurrence.

The symmetry lies in the fact that both reach the "Information-Theoretic Wall" for their respective domains.
## The Information-Theoretic Lower Bound

In both fields, the nlogn term arises from the entropy of the state space.

In Sorting: To sort n elements, we must distinguish between n! possible permutations. Using Stirling's approximation:
log2​(n!)≈nlog2​n−nlog2​e

Each comparison provides at most 1 bit of information. Therefore, the lower bound is Ω(nlogn) bits of information.

In HvH Multiplication: To multiply two n-bit integers, we are essentially performing a convolution. The Schönhage-Strassen conjecture (finally proven by Harvey and van der Hoeven) posits that the complexity is O(nlogn). This mirrors the sorting bound because it represents the optimal distribution of "mixing" information across n bit-positions via the Fast Fourier Transform (FFT).

## The Symmetry of the Recurrence

The "Deep Form Factor" (DFF) or structural symmetry is found in the Master Theorem profile of both algorithms.
Comparison-Based Sorting (Merge Sort)

Merge Sort splits the domain into two sub-problems and requires O(n) work to merge (the "linear pass").
T(n)=2T(2n​)+O(n)
HvH Multiplication

The HvH algorithm uses a multi-dimensional FFT. By reducing a 1D convolution to a d-dimensional hypercube of size Ld, they manage the "overhead" of the recursion more efficiently than Schönhage-Strassen. However, the core structural symmetry remains:
T(n)=K⋅T(Kn​)+O(n)

Where O(n) represents the cost of the Fourier Transform/Pointwise multiplication at that level.


The mathematical symmetry is defined as follows: Both algorithms are optimal because they saturate the bandwidth of a d-dimensional hypercube. In sorting, this is the bandwidth of the decision tree; in HvH, it is the bandwidth of the FFT signal path. Harvey and van der Hoeven’s breakthrough was essentially finding a way to prevent the "log-star" (O(nlogn⋅2log∗n)) overhead from accumulating, effectively "sorting" the bit-information with the same efficiency that a heap or merge sort organizes a list.

To "saturate the bandwidth" of a d-dimensional hypercube essentially means that an algorithm is moving as much information as the geometry of the network physically allows.

At an undergraduate level, think of it this way: if you have a highway system, the "bandwidth" is the number of lanes. "Saturating" it means every lane is full of cars moving at top speed. In computer science, this "highway" is the data-dependency graph of your algorithm.
0. Why a Hypercube?

A d-dimensional hypercube (or Qd​) is a graph with 2d nodes. Each node is labeled with a d-bit binary string, and two nodes are connected if their labels differ by exactly one bit.
Why it works for both:

Recursive Structure: A d-cube is just two (d−1)-cubes joined together. This perfectly matches Divide and Conquer.

Logarithmic Diameter: Even with 2d nodes, you can get from any point to another in just d steps. Since d=log2​(nodes), this is the geometric origin of the logn factor in both algorithms.

Symmetry: Every node looks exactly like every other node. This ensures that no single part of the "multiplication" or "sorting" becomes a bottleneck.

1. Sorting to Hypercube: The "Compare-Exchange" Path

When you sort n items, you are trying to find one specific permutation out of n! possibilities.

The Hypercube Mapping: Imagine each node in a hypercube represents a state of your list.

The Exploration: In algorithms like Bitonic Sort, we treat the indices of our array as coordinates in a hypercube. To sort, we perform "Compare-Exchange" operations along each dimension of the cube sequentially.

Saturating the Bandwidth: In a single step, a hypercube can support n/2 parallel comparisons (one across every edge in a specific dimension). A "perfect" sorting algorithm uses every one of these available "lanes" in every step to resolve the uncertainty (entropy) of the list's order.

The Wall: Because you need log(n!)≈nlogn bits of information to sort, and the hypercube provides O(n) "lanes" per step, you physically must take logn steps.

## Multiplying to Hypercube: The "Convolution" Path

Multiplying two n-bit integers is essentially a convolution of their digits. The Harvey–van der Hoeven (HvH) breakthrough treats this convolution as a multi-dimensional problem.

The Hypercube Mapping: HvH breaks the large n-bit integers into many smaller chunks and arranges them as a d-dimensional grid (which is a subset of a hypercube).

The Exploration: The Fast Fourier Transform (FFT) is the engine here. The FFT's "butterfly" diagram is mathematically isomorphic to the edges of a hypercube. When the FFT runs, it is literally passing data back and forth along the dimensions of this hypercube to calculate how every digit affects every other digit (the carry-propagation).

Saturating the Bandwidth: Previous algorithms (like Schönhage–Strassen) had "congestion." They couldn't perfectly fill the hypercube lanes because of the overhead in managing the recursion (the O(loglogn) term).

The HvH Fix: Harvey and van der Hoeven used a "Gaussian" distribution of dimensions. They ensured that as the recursion goes deeper, the "recombination" work perfectly fills the available bandwidth of the hypercube at that level, without any wasted "empty lanes" or "traffic jams."

## Further Reading
Wonderful Wikipedia : https://en.wikipedia.org/wiki/Multiplication_algorithm

Exploration of Varying Radix on Intel i3-4025U : https://miracl.com/blog/missing-a-trick-karatsuba-variations-michael-scott/

Karatsuba paper: https://ieeexplore.ieee.org/document/4402691

Toom-Cook: A. L. Toom, "The Complexity of a Scheme of Functional Elements Realizing the Multiplication of Integers" (1963); S. A. Cook, "On the Minimum Computation Time of Functions" (1966, PhD Thesis, Harvard)

Schönhage–Strassen paper: 

Harvey and van der Hoeven's Paper : https://hal.archives-ouvertes.fr/hal-03182372/document


## Schönhage - Strassen

So having completed our foray to fast Fourier, we can unpack an algorithm for O(n log(n) log log(n)) mult.


## FFT (Fast Fourier Transform)
Polynomial Representations

    Coefficient Representation: c0 + c1x1 + c2x2^2 + ... + cd*xd

    Value Representation: From the Fundamental Theorem of Algebra, (d+1) points uniquely capture a polynomial of degree d: {(x0, P(x0)), ... (xd, P(xd))}

The Efficiency Goal

    Pointwise multiplication of polynomials is O(d), which is less than O(d^2).

    The Problem: We want: coeff => value, multiply, value => coeff.

    However, evaluating d+1 points in a polynomial of degree d will be O(d^2).

Cooley-Tukey of Radix-2

    Caveat: Assume power of 2 for simplicity (further reading).

    Divide and conquer on odds and evens.

    Expand domain to complex domain. Let N >= d+1; n = 2^k, k is an element of Z.

    w^(j + n/2) = -w^j -> (w^j, w^(j + n/2)) are +/- pairs.

The FFT Equations

    Xk = sum from m=0 to N/2-1 of (x_2m * e^(-2pii/N * 2m * k)) + sum from m=0 to N/2-1 of (x_2m+1 * e^(-2pii/N * (2m+1) * k))

    Xk = Ek + e^(-2pi*i/N * k) * Ok

    X_{k+n/2} = Ek - e^(-2pi*i/N * k) * Ok

Nth Roots of Unity

    z^n = 1

    e^(itheta) = cos(theta) + isin(theta)

    w = e^(2pi*i / n)

    (w^n)^2 = w^(n/2) ; e^(i4pi/n) = e^(i2pi/n)

Calculating the Value Representation of N1 * N2

    FFT: ([X0, X1, ... Xn-1]) -> [P(w^0), ... P(w^n-1)]

    Matrix form: P_vector = W * X_vector

    IFFT: ([P(w^0), ... P(w^n-1)]) -> [p0, p1, ... pn-1]

    W^-1 * P_vector = x_vector

    w = (1/n) * e^(-2pi*i / n)

## Harvey - Hoeven (abridged)

In conclusion, we will outline an abridged version of the Harvey-Hoeven algorithm for linearithmic multiplication.

    Caveat Emptor: The complexity gains are in galactic scale—meaning numbers at scale greater than atoms in the unknown universe.

    Of course, a joke could be made here about an efficient algorithm too grandiose for computation in the physical plane, similar to a topologist's ambivalence between a coffee mug and donut.

Le théorème des restes chinois, le génie de Sunzi

N:=∏i=1k​ni​