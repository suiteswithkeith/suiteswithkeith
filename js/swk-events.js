/* Suites With Keith — shared GA4 event wiring.
   One file, included on every page; no-ops when gtag is absent.

   Events:
   - cta_click      any element carrying data-gtag-label / data-gtag-location
   - mailto_click   any mailto: link (interim visibility for hotel-page CTAs
                    until they move to the inquiry form)
   - generate_lead  submit on any Formspree form. This file is the single
                    source of truth for generate_lead — page scripts must not
                    fire it themselves, or leads double-count. Counted at
                    submit (after native validation), not at fetch success. */
(function () {
  if (!window.gtag) return;

  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-gtag-label]');
    if (el) {
      gtag('event', 'cta_click', {
        cta_label: el.getAttribute('data-gtag-label'),
        cta_location: el.getAttribute('data-gtag-location') || '',
        page_path: location.pathname
      });
      return;
    }
    var a = e.target.closest('a[href^="mailto:"]');
    if (a) {
      var subject = '';
      try {
        var m = a.getAttribute('href').match(/[?&]subject=([^&]*)/);
        if (m) subject = decodeURIComponent(m[1].replace(/\+/g, ' ')).slice(0, 80);
      } catch (err) { /* malformed href — send the event without a subject */ }
      gtag('event', 'mailto_click', {
        page_path: location.pathname,
        mail_subject: subject
      });
    }
  });

  /* Capture phase: runs before per-form handlers, so a page script calling
     stopPropagation() cannot silently unhook lead counting. */
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (f && typeof f.action === 'string' && f.action.indexOf('formspree.io') !== -1) {
      gtag('event', 'generate_lead', { form_location: location.pathname });
    }
  }, true);
})();

/* Anchor links on load. The site sets html{scroll-behavior:smooth}, and a
   smooth scroll to a #section started during page load gets cancelled, so a
   link like /#inquire opened from a DM or email lands at the top of the page.
   Jump to the target instantly instead, and back off once the visitor
   touches, scrolls or types. Separate from the analytics block above so it
   runs even when gtag is absent. */
(function () {
  var h = location.hash;
  if (!h || h.length < 2) return;
  var stop = false;
  ['touchstart', 'wheel', 'keydown'].forEach(function (e) {
    window.addEventListener(e, function () { stop = true; }, { passive: true, once: true });
  });
  function go() {
    if (stop) return;
    var el;
    try { el = document.getElementById(decodeURIComponent(h.slice(1))); } catch (e) { return; }
    if (!el) return;
    var d = document.documentElement, p = d.style.scrollBehavior;
    d.style.scrollBehavior = 'auto';
    el.scrollIntoView();
    d.style.scrollBehavior = p;
  }
  if (document.readyState !== 'loading') go();
  else document.addEventListener('DOMContentLoaded', go);
  window.addEventListener('load', function () { go(); setTimeout(go, 400); setTimeout(go, 1200); });
})();
