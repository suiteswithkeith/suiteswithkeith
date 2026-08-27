/* Suites With Keith — client booking desk modal.
   One file, included on every page next to swk-events.js.

   Fora's portal (trips.foratravel.com) forbids framing (X-Frame-Options:
   DENY), so it cannot be embedded. Instead: any [data-swk-book] element
   opens a branded interstitial that frames the tool — quick self-serve
   bookings, full trips still go through Keith — then hands off to the
   portal in a new tab. The script also plants a "Client booking desk"
   link in the footer "Get in touch" column so the entry point exists
   site-wide without editing every page's markup.

   cta_click events fire from js/swk-events.js via data-gtag-label. */
(function () {
  var PORTAL = 'https://trips.foratravel.com/suites-with-keith/book';

  function init() {
    injectStyles();
    var modal = injectModal();
    injectFooterLink();

    var lastFocus = null;

    function open() {
      lastFocus = document.activeElement;
      modal.hidden = false;
      /* next frame so the transition runs */
      requestAnimationFrame(function () { modal.classList.add('swkb-open'); });
      document.body.style.overflow = 'hidden';
      var x = modal.querySelector('.swkb-x');
      if (x) x.focus();
    }

    function close() {
      modal.classList.remove('swkb-open');
      document.body.style.overflow = '';
      window.setTimeout(function () { modal.hidden = true; }, 220);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    document.addEventListener('click', function (e) {
      var opener = e.target.closest('[data-swk-book]');
      if (opener) {
        e.preventDefault();
        open();
        return;
      }
      if (!modal.hidden) {
        if (e.target.closest('.swkb-x') || e.target === modal) close();
        /* let the portal link work normally, then dismiss */
        if (e.target.closest('.swkb-go')) close();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !modal.hidden) close();
    });
  }

  function injectStyles() {
    var css = [
      /* display:flex would override the hidden attribute's display:none —
         without this rule the invisible overlay covers the page and eats
         every click. */
      '.swkb-overlay[hidden]{display:none}',
      '.swkb-overlay{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;padding:20px;background:rgba(22,23,18,.62);opacity:0;transition:opacity .22s ease}',
      '.swkb-overlay.swkb-open{opacity:1}',
      '.swkb-card{position:relative;width:min(600px,100%);max-height:calc(100vh - 40px);overflow-y:auto;background:var(--plaster,#F2EFE6);color:var(--ink,#1F201A);padding:52px 48px 44px;box-shadow:0 30px 80px rgba(22,23,18,.45);transform:translateY(14px);transition:transform .22s ease}',
      '.swkb-open .swkb-card{transform:none}',
      '.swkb-x{position:absolute;top:14px;right:14px;width:40px;height:40px;border:0;background:none;color:var(--ash,#65665C);font-size:26px;line-height:1;cursor:pointer;font-family:inherit}',
      '.swkb-x:hover{color:var(--ink,#1F201A)}',
      '.swkb-eyebrow{margin:0 0 14px;font-family:var(--body,"Jost","Helvetica Neue",Arial,sans-serif);font-size:.72rem;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--brass,#836229)}',
      '.swkb-card h2{margin:0 0 18px;font-family:var(--display,"Bodoni Moda",Didot,"Times New Roman",serif);font-weight:400;font-size:clamp(1.7rem,4.5vw,2.2rem);line-height:1.15;letter-spacing:.01em}',
      '.swkb-card p{margin:0 0 14px;font-family:var(--body,"Jost","Helvetica Neue",Arial,sans-serif);font-weight:300;font-size:.98rem;line-height:1.65}',
      '.swkb-actions{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin:26px 0 18px}',
      '.swkb-go{display:inline-block;padding:15px 28px;background:var(--olive,#4A5040);color:var(--plaster,#F2EFE6);font-family:var(--body,"Jost",sans-serif);font-size:.76rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;transition:background .18s ease}',
      '.swkb-go:hover{background:var(--shadow-2,#22231C)}',
      '.swkb-alt{font-family:var(--body,"Jost",sans-serif);font-size:.76rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--brass,#836229);text-decoration:none}',
      '.swkb-note{font-size:.82rem!important;color:var(--ash,#65665C);border-top:1px solid var(--hairline,rgba(22,23,18,.15));padding-top:16px;margin-bottom:0!important}',
      '.swkb-note a{color:var(--brass,#836229)}',
      '@media(max-width:560px){.swkb-card{padding:44px 26px 34px}}'
    ].join('');
    var s = document.createElement('style');
    s.textContent = css;
    document.head.appendChild(s);
  }

  function injectModal() {
    var wrap = document.createElement('div');
    wrap.className = 'swkb-overlay';
    wrap.hidden = true;
    wrap.setAttribute('role', 'dialog');
    wrap.setAttribute('aria-modal', 'true');
    wrap.setAttribute('aria-labelledby', 'swkb-title');
    wrap.innerHTML =
      '<div class="swkb-card">' +
        '<button class="swkb-x" type="button" aria-label="Close">&times;</button>' +
        '<p class="swkb-eyebrow">For current clients</p>' +
        '<h2 id="swkb-title">A new way to book with me</h2>' +
        '<p>Browse hotels, compare rates and perks, and book on your own &mdash; my rates, Fora&nbsp;Reserve perks included, still booked under Suites With Keith. Handy for the simpler stays: a last-minute overnight, a quick weekend away, a hotel for a wedding, or when you already know exactly where you want to stay.</p>' +
        '<p>For a real trip &mdash; a honeymoon, an itinerary, anything with moving parts &mdash; that&rsquo;s still me, start to finish. And whatever you book here lands on my desk: I manage the reservation and VIP you with the hotel, same as always.</p>' +
        '<div class="swkb-actions">' +
          '<a class="swkb-go" href="' + PORTAL + '" target="_blank" rel="noopener" data-gtag-label="open_booking_desk" data-gtag-location="book_modal">Open the booking portal &rarr;</a>' +
          '<a class="swkb-alt" href="/index.html#inquire" data-gtag-label="plan_with_keith" data-gtag-location="book_modal">Plan a trip with me</a>' +
        '</div>' +
        '<p class="swkb-note">Client login required &mdash; the portal is open to current clients for now. Not every hotel is in it yet; if you don&rsquo;t see yours, <a href="mailto:keith.pence@fora.travel">email me</a> and I&rsquo;ll check. Not a client yet? <a href="/index.html#inquire">Start with one trip.</a></p>' +
      '</div>';
    document.body.appendChild(wrap);
    return wrap;
  }

  function injectFooterLink() {
    var heads = document.querySelectorAll('footer .col-h');
    for (var i = 0; i < heads.length; i++) {
      if (/get in touch/i.test(heads[i].textContent)) {
        var links = heads[i].parentElement.querySelector('.links');
        if (links && !links.querySelector('[data-swk-book]')) {
          var a = document.createElement('a');
          a.href = PORTAL;
          a.setAttribute('data-swk-book', '');
          a.setAttribute('data-gtag-label', 'booking_desk');
          a.setAttribute('data-gtag-location', 'footer');
          a.textContent = 'Client booking portal';
          links.appendChild(a);
        }
        return;
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
