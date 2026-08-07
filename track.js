/* Suites With Keith — lightweight GA4 event tracking.
   Sends named events for the actions that matter commercially:
   Hoper referral clicks, email clicks, contact form submits, CTA buttons. */
(function () {
  function send(name, params) {
    if (typeof window.gtag === 'function') {
      window.gtag('event', name, params || {});
    }
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a') : null;
    if (!a || !a.href) return;
    /* Pages with their own data-gtag handler (homepage) own those clicks. */
    if (a.hasAttribute('data-gtag-label')) return;
    var href = a.getAttribute('href') || '';
    var label = (a.textContent || '').trim().slice(0, 60);

    if (href.indexOf('flyhoper.com') !== -1) {
      send('hoper_referral_click', { link_text: label, page_path: location.pathname });
    } else if (href.indexOf('mailto:') === 0) {
      send('email_click', { link_text: label, page_path: location.pathname });
    } else if (a.classList.contains('btn')) {
      send('cta_click', { link_text: label, page_path: location.pathname });
    } else if (href.indexOf('instagram.com') !== -1) {
      send('instagram_click', { page_path: location.pathname });
    }
  }, true);

  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (f && f.classList && f.classList.contains('contact-form')) {
      send('contact_form_submit', { page_path: location.pathname });
    }
  }, true);
})();
