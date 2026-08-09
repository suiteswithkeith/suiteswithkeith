/* Suites With Keith — subtle scroll-reveal.
   Content is fully visible without JS; this script only adds the effect.
   Skips entirely for users with reduced-motion enabled. */
(function () {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var SELECTORS = [
    '.rank-card',
    '.rank-intro .container > div',
    '.print-callout',
    '.rank-sidebar-grid > div',
    '.areas-grid > div',
    '.section-heading',
    '.guide-cta .container',
    '.hotel-grid',
    '.guide-card',
    '.fr-rule',
    '.fr-callout',
    '.property-header',
    '.td-day'
  ];
  var els = document.querySelectorAll(SELECTORS.join(','));
  if (!els.length) return;

  document.documentElement.classList.add('reveal-ready');

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-in');
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0 });

  var vh = window.innerHeight;
  els.forEach(function (el) {
    el.classList.add('reveal');
    var r = el.getBoundingClientRect();
    if (r.top < vh && r.bottom > 0) {
      /* Already on screen at load — show instantly, no flash */
      el.classList.add('reveal-in');
    } else {
      io.observe(el);
    }
  });
})();
