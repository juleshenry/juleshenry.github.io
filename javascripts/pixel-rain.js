(function () {
  'use strict';

  // ── Config ──
  var GREENS = [
    '#00ff00', // terminal green
    '#39ff75', // bright mint
    '#0f0',    // pure green shorthand
    '#22c55e', // medium green
    '#16a34a', // darker green
  ];

  var DURATION_MS   = 800;   // total glitch duration
  var FLICKER_COUNT = 5;     // number of glitch "frames"
  var SLICE_MIN     = 2;     // min slice height in px
  var SLICE_MAX     = 6;     // max slice height in px
  var SHIFT_MAX     = 12;    // max horizontal pixel shift
  var NOISE_DENSITY = 0.08;  // sparse noise dots
  var PIXEL_SIZE    = 2;     // size of each noise dot

  // ── Glitch one header ──
  function triggerGlitch(el) {
    var rect = el.getBoundingClientRect();
    var scrollX = window.pageXOffset || document.documentElement.scrollLeft;
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;

    var w = rect.width;
    var h = rect.height;
    if (w < 10 || h < 10) return;

    // pad a few px around the text
    var pad = 4;
    var cw = w + pad * 2;
    var ch = h + pad * 2;
    var dpr = window.devicePixelRatio || 1;

    var canvas = document.createElement('canvas');
    canvas.className = 'glitch-canvas';
    canvas.width  = Math.ceil(cw * dpr);
    canvas.height = Math.ceil(ch * dpr);
    canvas.style.width  = cw + 'px';
    canvas.style.height = ch + 'px';
    canvas.style.left   = (rect.left + scrollX - pad) + 'px';
    canvas.style.top    = (rect.top  + scrollY - pad) + 'px';
    document.body.appendChild(canvas);

    var ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);

    var flickerIndex = 0;
    var interval = DURATION_MS / FLICKER_COUNT;

    function drawGlitchFrame() {
      ctx.clearRect(0, 0, cw, ch);

      // progress 0..1
      var progress = flickerIndex / FLICKER_COUNT;
      // fade intensity toward end
      var intensity = 1 - progress * progress;

      // ── Horizontal slices: shifted bands of color ──
      var y = 0;
      while (y < ch) {
        var sliceH = SLICE_MIN + Math.random() * (SLICE_MAX - SLICE_MIN);
        if (y + sliceH > ch) sliceH = ch - y;

        // random chance to draw a glitch slice
        if (Math.random() < 0.35 * intensity) {
          var shift = (Math.random() - 0.5) * 2 * SHIFT_MAX * intensity;
          var color = GREENS[Math.floor(Math.random() * GREENS.length)];
          var alpha = (0.1 + Math.random() * 0.25) * intensity;

          ctx.globalAlpha = alpha;
          ctx.fillStyle = color;
          ctx.fillRect(shift, y, cw, sliceH);
        }

        y += sliceH;
      }

      // ── Horizontal scan lines ──
      ctx.globalAlpha = 0.06 * intensity;
      ctx.fillStyle = '#39ff75';
      for (var sy = 0; sy < ch; sy += 2) {
        ctx.fillRect(0, sy, cw, 1);
      }

      // ── Scattered noise pixels ──
      var noiseCount = Math.floor(cw * ch * NOISE_DENSITY * intensity / (PIXEL_SIZE * PIXEL_SIZE));
      for (var i = 0; i < noiseCount; i++) {
        var nx = Math.random() * cw;
        var ny = Math.random() * ch;
        var nc = GREENS[Math.floor(Math.random() * GREENS.length)];
        ctx.globalAlpha = (0.2 + Math.random() * 0.5) * intensity;
        ctx.fillStyle = nc;
        ctx.fillRect(Math.floor(nx), Math.floor(ny), PIXEL_SIZE, PIXEL_SIZE);
      }

      // ── Occasional full-width glitch bar ──
      if (Math.random() < 0.3 * intensity) {
        var barY = Math.random() * ch;
        var barH = 1 + Math.random() * 2;
        ctx.globalAlpha = (0.2 + Math.random() * 0.3) * intensity;
        ctx.fillStyle = GREENS[Math.floor(Math.random() * GREENS.length)];
        ctx.fillRect(-SHIFT_MAX, barY, cw + SHIFT_MAX * 2, barH);
      }

      ctx.globalAlpha = 1;

      flickerIndex++;
      if (flickerIndex < FLICKER_COUNT) {
        setTimeout(drawGlitchFrame, interval + (Math.random() - 0.5) * interval * 0.6);
      } else {
        // final cleanup
        canvas.remove();
      }
    }

    drawGlitchFrame();
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
            setTimeout(function () {
              triggerGlitch(entry.target);
            }, 60);
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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
