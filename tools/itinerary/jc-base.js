(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Reveal days and chapters as they enter the viewport.
  var reveal = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); reveal.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0 });
  var hidden = document.querySelectorAll('.jc-daysec, .jc-chapter');
  hidden.forEach(function (el) { reveal.observe(el); });
  // Failsafe: nothing on this page may stay hidden, whatever the browser does.
  setTimeout(function () { hidden.forEach(function (el) { el.classList.add('in'); }); }, 2000);

  // Sticky date bar: show once the date grid has scrolled past.
  var bar = document.getElementById('datebar'), grid = document.getElementById('days');
  if (bar && grid) {
    var ticking = false;
    function placeBar() {
      ticking = false;
      bar.classList.toggle('on', grid.getBoundingClientRect().bottom < 0);
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(placeBar); }
    }, { passive: true });
    placeBar();

    // Highlight the section being read: the last one whose heading has passed
    // the top third of the screen. Scroll-driven, so short days are never skipped.
    var row = bar.querySelector('.row');
    var targets = Array.prototype.slice.call(document.querySelectorAll('.jc-daysec, #confirmations'));
    var links = {}; bar.querySelectorAll('a').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
    var current = null, marking = false, jumpingUntil = 0, settle = null;
    function slideRow() {
      if (!current) return;
      var left = current.offsetLeft - (row.clientWidth - current.offsetWidth) / 2;
      row.scrollTo({ left: Math.max(0, left), behavior: reduce ? 'auto' : 'smooth' });
    }
    function markCurrent() {
      marking = false;
      var line = window.innerHeight * 0.34, pick = null;
      for (var i = 0; i < targets.length; i++) {
        if (targets[i].getBoundingClientRect().top <= line) pick = targets[i]; else break;
      }
      var next = pick ? links[pick.id] : null;
      if (next === current) return;
      if (current) current.classList.remove('cur');
      current = next;
      if (!current) return;
      current.classList.add('cur');
      // While an anchor jump is animating, do not start a second smooth scroll:
      // Safari treats it as a cancel and the page stops at the first day it
      // passes. Slide the row once the jump has settled instead.
      if (Date.now() < jumpingUntil) {
        clearTimeout(settle); settle = setTimeout(slideRow, jumpingUntil - Date.now() + 50);
      } else {
        slideRow();
      }
    }
    window.addEventListener('scroll', function () {
      if (!marking) { marking = true; requestAnimationFrame(markCurrent); }
    }, { passive: true });
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]');
      if (a) jumpingUntil = Date.now() + 1400;
    });
    markCurrent();
  }
})();
