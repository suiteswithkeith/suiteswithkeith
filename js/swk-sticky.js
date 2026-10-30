/* Suites With Keith — mobile sticky CTA behaviour.
   One file, included on every page that carries .sticky-cta.

   The fixed button sat over whatever was underneath it the whole time,
   covering card text and photos while reading. Now it:
   - stays hidden until the reader is past the opening screen,
   - slides away while scrolling down (reading) and returns on scroll up,
   - stays hidden while the inquiry form or footer is on screen, where
     it would only duplicate (and cover) the real form. */
(function () {
  var cta = document.querySelector('.sticky-cta');
  if (!cta) return;

  var style = document.createElement('style');
  style.textContent =
    '.sticky-cta{transition:transform .32s ease,opacity .32s ease;will-change:transform}' +
    '.sticky-cta.is-hidden{transform:translateY(calc(100% + 24px));opacity:0;pointer-events:none}' +
    '@media (prefers-reduced-motion:reduce){.sticky-cta{transition:opacity .2s linear}}';
  document.head.appendChild(style);

  var lastY = window.scrollY;
  var goingDown = false;
  var blocked = 0; // count of form/footer elements currently on screen

  function update() {
    var pastHero = window.scrollY > window.innerHeight * 0.6;
    cta.classList.toggle('is-hidden', !pastHero || goingDown || blocked > 0);
  }

  window.addEventListener('scroll', function () {
    var y = window.scrollY;
    var d = y - lastY;
    if (Math.abs(d) > 6) {
      goingDown = d > 0;
      lastY = y;
    }
    update();
  }, { passive: true });

  if ('IntersectionObserver' in window) {
    var targets = document.querySelectorAll('#inquire, .inquire-form, footer');
    var seen = new Set();
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) seen.add(e.target); else seen.delete(e.target);
      });
      blocked = seen.size;
      update();
    });
    targets.forEach(function (t) { io.observe(t); });
  }

  cta.classList.add('is-hidden');
  update();
})();
