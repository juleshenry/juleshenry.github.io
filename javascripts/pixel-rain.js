(function () {
  'use strict';

  // ── Config ──
  const NEON_COLORS = [
    '#ff2d8a', // hot pink
    '#39ff75', // hacker green
    '#38bdf8', // cyan
    '#f1e05a', // yellow
    '#a855f7', // purple
    '#ff6a13', // orange
    '#22d3ee', // teal
    '#ff4444', // red
    '#00ffcc', // mint
    '#ffff00', // bright yellow
    '#ff00ff', // magenta
    '#00ff00', // matrix green
  ];

  const BASE_PARTICLE_COUNT = 120;
  const DURATION_MS = 2400;
  const PIXEL_MIN = 2;
  const PIXEL_MAX = 5;
  const COLUMN_COUNT = 24; // number of "rain columns"
  const TAIL_LENGTH = 4;   // trailing glow segments per column

  // Reduce on mobile
  function getParticleCount() {
    if (window.innerWidth < 480) return 50;
    if (window.innerWidth < 768) return 75;
    return BASE_PARTICLE_COUNT;
  }

  // ── Particle Factory ──
  function createParticle(canvasW, canvasH) {
    var color = NEON_COLORS[Math.floor(Math.random() * NEON_COLORS.length)];
    var size = PIXEL_MIN + Math.random() * (PIXEL_MAX - PIXEL_MIN);
    // distribute across width in column-like bands
    var col = Math.floor(Math.random() * COLUMN_COUNT);
    var colWidth = canvasW / COLUMN_COUNT;
    var x = col * colWidth + Math.random() * colWidth;

    return {
      x: x,
      y: -size - Math.random() * canvasH * 0.3, // start above canvas, staggered
      size: size,
      color: color,
      speed: 2.5 + Math.random() * 4.5,         // fall speed px/frame
      drift: (Math.random() - 0.5) * 0.6,        // slight horizontal drift
      opacity: 0.7 + Math.random() * 0.3,
      glimmerPhase: Math.random() * Math.PI * 2,  // sparkle phase offset
      glimmerSpeed: 0.08 + Math.random() * 0.12,
      trail: [],
    };
  }

  // ── Render one header's pixel rain ──
  function triggerPixelRain(headerEl) {
    var rect = headerEl.getBoundingClientRect();
    var scrollX = window.pageXOffset || document.documentElement.scrollLeft;
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;

    // Canvas spans the header width and extends below it
    var canvasW = Math.max(rect.width + 60, 300);
    var canvasH = Math.min(window.innerHeight * 0.6, 450);
    var canvasLeft = rect.left + scrollX - 30;
    var canvasTop = rect.top + scrollY;

    var canvas = document.createElement('canvas');
    canvas.className = 'pixel-rain-canvas';
    canvas.width = canvasW * (window.devicePixelRatio || 1);
    canvas.height = canvasH * (window.devicePixelRatio || 1);
    canvas.style.width = canvasW + 'px';
    canvas.style.height = canvasH + 'px';
    canvas.style.left = canvasLeft + 'px';
    canvas.style.top = canvasTop + 'px';
    document.body.appendChild(canvas);

    var ctx = canvas.getContext('2d');
    ctx.scale(window.devicePixelRatio || 1, window.devicePixelRatio || 1);

    var count = getParticleCount();
    var particles = [];
    for (var i = 0; i < count; i++) {
      particles.push(createParticle(canvasW, canvasH));
    }

    var startTime = performance.now();
    var animId;

    function frame(now) {
      var elapsed = now - startTime;
      var progress = Math.min(elapsed / DURATION_MS, 1);
      // Global fade out in the last 30%
      var globalAlpha = progress > 0.7 ? 1 - (progress - 0.7) / 0.3 : 1;

      ctx.clearRect(0, 0, canvasW, canvasH);

      for (var i = 0; i < particles.length; i++) {
        var p = particles[i];

        // Update position
        p.y += p.speed;
        p.x += p.drift;

        // Glimmer: oscillate opacity
        p.glimmerPhase += p.glimmerSpeed;
        var glimmer = 0.5 + 0.5 * Math.sin(p.glimmerPhase);
        var alpha = p.opacity * glimmer * globalAlpha;

        if (alpha < 0.01) continue;

        // Store trail positions
        p.trail.unshift({ x: p.x, y: p.y });
        if (p.trail.length > TAIL_LENGTH) p.trail.pop();

        // Draw trail (fading tail segments)
        for (var t = p.trail.length - 1; t >= 0; t--) {
          var trailAlpha = alpha * (1 - t / TAIL_LENGTH) * 0.4;
          if (trailAlpha < 0.01) continue;
          ctx.globalAlpha = trailAlpha;
          ctx.fillStyle = p.color;
          var trailSize = p.size * (1 - t * 0.15);
          ctx.fillRect(
            Math.floor(p.trail[t].x),
            Math.floor(p.trail[t].y),
            Math.ceil(trailSize),
            Math.ceil(trailSize)
          );
        }

        // Draw main pixel
        ctx.globalAlpha = alpha;
        ctx.fillStyle = p.color;
        ctx.fillRect(
          Math.floor(p.x),
          Math.floor(p.y),
          Math.ceil(p.size),
          Math.ceil(p.size)
        );

        // Glow effect on brighter particles
        if (glimmer > 0.75 && p.size > 3) {
          ctx.globalAlpha = alpha * 0.35;
          ctx.shadowColor = p.color;
          ctx.shadowBlur = 8;
          ctx.fillRect(
            Math.floor(p.x) - 1,
            Math.floor(p.y) - 1,
            Math.ceil(p.size) + 2,
            Math.ceil(p.size) + 2
          );
          ctx.shadowBlur = 0;
        }
      }

      ctx.globalAlpha = 1;

      if (progress < 1) {
        animId = requestAnimationFrame(frame);
      } else {
        // Cleanup
        canvas.remove();
      }
    }

    animId = requestAnimationFrame(frame);
  }

  // ── Intersection Observer: trigger once per header ──
  function init() {
    var headers = document.querySelectorAll('h1, h2, h3');
    if (!headers.length) return;

    var triggered = new WeakSet();

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting && !triggered.has(entry.target)) {
            triggered.add(entry.target);
            // Small delay so the header is visible before rain starts
            setTimeout(function () {
              triggerPixelRain(entry.target);
            }, 80);
          }
        });
      },
      {
        threshold: 0.3,
        rootMargin: '0px 0px -10% 0px',
      }
    );

    headers.forEach(function (h) {
      observer.observe(h);
    });
  }

  // Run after DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
