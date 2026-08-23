/* Hotel-page inquiry: one-field ask, progressive disclosure, Formspree.
   Replaces the mailto: CTAs. generate_lead fires from js/swk-events.js
   (document-level capture submit listener) — do not fire it here. */
(function () {
  var form = document.querySelector('.hotel-inquire-form');
  if (!form) return;
  var step2 = form.querySelector('.hi-step2');
  var when = form.querySelector('input[name="travel_dates"]');
  var status = form.querySelector('.hi-status');
  var btn = form.querySelector('button[type="submit"]');

  /* Hidden only when JS runs: without JS the full form renders and posts
     natively to Formspree. */
  function reveal() { if (step2 && step2.hidden) step2.hidden = false; }
  if (step2 && when) {
    step2.hidden = true;
    when.addEventListener('focus', reveal);
    when.addEventListener('input', reveal);
    form.addEventListener('invalid', reveal, true);
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    btn.disabled = true;
    status.textContent = '';
    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    }).then(function (r) {
      if (!r.ok) throw new Error();
      form.reset();
      form.classList.add('hi-done');
      status.textContent = 'Got it. You’ll hear from me, not an autoresponder.';
    }).catch(function () {
      status.textContent = 'That didn’t send — email me directly at keith.pence@fora.travel.';
    }).then(function () { btn.disabled = false; });
  });
})();
