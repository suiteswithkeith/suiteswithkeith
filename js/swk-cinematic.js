/* Suites With Keith — cinematic helpers.
   Pauses the pinned hero video once it's scrolled out of view
   (the sticky hero stays geometrically in the viewport, so we
   watch a sentinel matching the first viewport-height instead). */
(function () {
  var video = document.querySelector('.hero--video .hero-video');
  if (!video || !('IntersectionObserver' in window)) return;

  var sentinel = document.createElement('div');
  sentinel.style.cssText = 'position:absolute;top:0;left:0;width:1px;pointer-events:none;visibility:hidden;';
  sentinel.style.height = '100vh';
  sentinel.style.height = '100svh';
  document.body.prepend(sentinel);

  new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        video.play().catch(function () {});
      } else {
        video.pause();
      }
    });
  }).observe(sentinel);
})();
