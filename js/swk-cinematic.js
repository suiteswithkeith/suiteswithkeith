/* Suites With Keith — cinematic helpers.
   Pauses the pinned hero video once it's scrolled out of view
   (the sticky hero stays geometrically in the viewport, so we
   watch a sentinel matching the first viewport-height instead). */
/* Count-up: the ledger numbers tick from zero when scrolled into view. */
(function () {
  var nums = document.querySelectorAll('.ledger .n');
  if (!nums.length || !('IntersectionObserver' in window)) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  function tick(el, delay) {
    var raw = el.textContent.trim();
    var target = parseInt(raw, 10);
    if (isNaN(target)) return;
    var padTo = raw.charAt(0) === '0' ? raw.length : 0;
    var duration = 1700;
    // Reserve the final width so the row doesn't shift as digits appear.
    el.style.minWidth = el.getBoundingClientRect().width + 'px';
    el.style.fontVariantNumeric = 'tabular-nums';
    el.textContent = padTo ? raw.replace(/\d/g, '0') : '0';
    var start = null;
    function frame(now) {
      if (start === null) start = now;
      var t = Math.min((now - start) / duration, 1);
      var eased = 1 - Math.pow(1 - t, 4);
      var s = String(Math.round(target * eased));
      while (s.length < padTo) s = '0' + s;
      el.textContent = s;
      if (t < 1) {
        requestAnimationFrame(frame);
      } else {
        el.textContent = raw;
        el.style.fontVariantNumeric = '';
      }
    }
    setTimeout(function () { requestAnimationFrame(frame); }, delay);
  }

  var seen = false;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting || seen) return;
      seen = true;
      io.disconnect();
      nums.forEach(function (el, i) { tick(el, i * 160); });
    });
  }, { threshold: 0.2 });
  io.observe(nums[0].closest('.ledger') || nums[0]);
})();

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
