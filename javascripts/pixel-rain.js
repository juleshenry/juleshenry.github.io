(function () {
  'use strict';

  // Trigger a smooth banner-reveal animation on h2/h3 headings
  // inside the main content as they scroll into view.
  function init() {
    var headers = document.querySelectorAll('section#main_content h2, section#main_content h3');
    if (!headers.length) return;

    var triggered = new WeakSet();

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting && !triggered.has(entry.target)) {
            triggered.add(entry.target);
            entry.target.classList.add('banner-reveal');
          }
        });
      },
      {
        threshold: 0.25,
        rootMargin: '0px 0px -8% 0px',
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
