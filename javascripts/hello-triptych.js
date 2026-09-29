(function () {
  'use strict';

  // Each .hello-panel-img starts on a lightweight placeholder JPG and
  // carries the real hq gif url in data-hq-src. We preload the hq gif
  // in the background and only swap it in once it's fully downloaded,
  // so the hero never blocks on a multi-MB gif before painting.
  //
  // Panels hidden by the mobile breakpoint (.hello-panel--side) are
  // skipped entirely so mobile never downloads gifs it won't show.
  function init() {
    var panels = document.querySelectorAll('.hello-panel-img');
    if (!panels.length) return;

    var isMobile = window.matchMedia('(max-width: 767px)').matches;

    panels.forEach(function (img) {
      var isSide = img.closest('.hello-panel--side');
      if (isMobile && isSide) return;

      var hqSrc = img.getAttribute('data-hq-src');
      if (!hqSrc) return;

      var preload = new Image();
      preload.onload = function () {
        img.src = hqSrc;
      };
      preload.src = hqSrc;
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
