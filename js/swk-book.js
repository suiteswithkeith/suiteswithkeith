/* Suites With Keith — client booking desk modal.
   One file, included on every page next to swk-events.js.

   Fora's portal (trips.foratravel.com) forbids framing (X-Frame-Options:
   DENY), so it cannot be embedded. Instead: any [data-swk-book] element
   opens a branded interstitial that frames the tool — quick self-serve
   bookings, full trips still go through Keith — then hands off to the
   portal in a new tab. The script also plants a "Client booking desk"
   link in the footer "Get in touch" column so the entry point exists
   site-wide without editing every page's markup.

   On hotel pages (/hotels/*) it additionally inserts a clients-only
   "private portal" card above the inquiry form: the hotel is bookable
   in the password-protected portal, access is granted personally —
   clients enter, everyone else is invited to request access.

   cta_click events fire from js/swk-events.js via data-gtag-label. */
(function () {
  var PORTAL = 'https://trips.foratravel.com/suites-with-keith/book';

  function init() {
    injectStyles();
    var modal = injectModal();
    injectFooterLink();
    injectHotelBand();
    injectVersusBand();

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
      '.swkb-card h2{margin:0 0 18px;font-family:var(--display,"DM Serif Display",Didot,Georgia,serif);font-weight:400;font-size:clamp(1.7rem,4.5vw,2.2rem);line-height:1.15;letter-spacing:.01em}',
      '.swkb-card p{margin:0 0 14px;font-family:var(--body,"Jost","Helvetica Neue",Arial,sans-serif);font-weight:300;font-size:.98rem;line-height:1.65}',
      '.swkb-actions{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin:26px 0 18px}',
      '.swkb-go{display:inline-block;padding:15px 28px;background:var(--olive,#4A5040);color:var(--plaster,#F2EFE6);font-family:var(--body,"Jost",sans-serif);font-size:.76rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;transition:background .18s ease}',
      '.swkb-go:hover{background:var(--shadow-2,#22231C)}',
      '.swkb-alt{font-family:var(--body,"Jost",sans-serif);font-size:.76rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--brass,#836229);text-decoration:none}',
      '.swkb-note{font-size:.82rem!important;color:var(--ash,#65665C);border-top:1px solid var(--hairline,rgba(22,23,18,.15));padding-top:16px;margin-bottom:0!important}',
      '.swkb-note a{color:var(--brass,#836229)}',
      '@media(max-width:560px){.swkb-card{padding:44px 26px 34px}}',
      /* clients-only portal card on hotel pages */
      '.swkx{padding-bottom:0}',
      '.swkx-card{position:relative;max-width:820px;margin:0 auto;background:var(--shadow,#161712);color:rgba(242,239,230,.9);padding:clamp(44px,6.5vw,68px) clamp(26px,5.5vw,64px);text-align:center;border:1px solid rgba(190,151,90,.4)}',
      '.swkx-card::after{content:"";position:absolute;inset:9px;border:1px solid rgba(190,151,90,.26);pointer-events:none}',
      '.swkx-eyebrow{margin:0 0 18px;font-family:var(--body,"Jost","Helvetica Neue",Arial,sans-serif);font-size:.7rem;font-weight:500;letter-spacing:.24em;text-transform:uppercase;color:var(--brass-lit,#BE975A)}',
      '.swkx-h{margin:0 auto 18px;max-width:22ch;font-family:var(--display,"DM Serif Display",Didot,Georgia,serif);font-weight:400;font-size:clamp(1.6rem,3.6vw,2.3rem);line-height:1.15;letter-spacing:.01em;color:var(--plaster,#F2EFE6)}',
      '.swkx-h em{font-style:italic;color:var(--brass-lit,#BE975A)}',
      '.swkx-p{margin:0 auto;max-width:52ch;font-family:var(--body,"Jost","Helvetica Neue",Arial,sans-serif);font-weight:300;font-size:.96rem;line-height:1.7;color:rgba(242,239,230,.76)}',
      '.swkx-actions{display:flex;flex-wrap:wrap;gap:14px 18px;align-items:center;justify-content:center;margin:28px 0 24px}',
      '.swkx-go{display:inline-block;padding:15px 28px;border:1px solid var(--brass-lit,#BE975A);color:var(--brass-lit,#BE975A);font-family:var(--body,"Jost",sans-serif);font-size:.76rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;transition:background .18s ease,color .18s ease}',
      '.swkx-go:hover{background:var(--brass-lit,#BE975A);color:var(--shadow,#161712)}',
      '.swkx-alt{font-family:var(--body,"Jost",sans-serif);font-size:.76rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:rgba(242,239,230,.82);text-decoration:none;border-bottom:1px solid rgba(242,239,230,.35);padding-bottom:3px}',
      '.swkx-alt:hover{color:var(--plaster,#F2EFE6);border-bottom-color:var(--brass-lit,#BE975A)}',
      '.swkx-note{margin:0 auto;max-width:54ch;padding-top:18px;border-top:1px solid rgba(242,239,230,.16);font-family:var(--body,"Jost",sans-serif);font-weight:300;font-size:.8rem;line-height:1.7;color:rgba(242,239,230,.58)}',
      '@media(max-width:560px){.swkx-card{padding:40px 22px 34px}}',
      /* "book through me" band and per-hotel asks on head-to-head pages */
      '.swkv-ask{display:inline-block;margin-top:22px;font-family:var(--body,"Jost",sans-serif);font-size:.74rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--brass,#836229);text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:3px}',
      '.swkv-ask:hover{color:var(--ink,#1F201A)}',
      '.swkv{padding-top:0}',
      '.swkv-card{display:grid;grid-template-columns:1fr;gap:30px;background:var(--plaster-deep,#E9E5DA);padding:clamp(30px,5vw,56px) clamp(24px,5vw,60px);border-top:2px solid var(--brass,#836229)}',
      '@media(min-width:900px){.swkv-card{grid-template-columns:1.1fr 1fr;gap:56px;align-items:center}}',
      '.swkv-card>*{min-width:0}',
      '.swkv-eyebrow{margin:0 0 14px;font-family:var(--body,"Jost",sans-serif);font-size:.72rem;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--brass,#836229)}',
      '.swkv-h{margin:0 0 16px;max-width:20ch;font-family:var(--display,"DM Serif Display",Didot,Georgia,serif);font-weight:400;font-size:clamp(1.6rem,3.4vw,2.2rem);line-height:1.15;letter-spacing:.01em;text-wrap:balance}',
      '.swkv-h em{font-style:italic;color:var(--brass,#836229)}',
      '.swkv-p{margin:0 0 24px;max-width:50ch;font-family:var(--body,"Jost",sans-serif);font-weight:300;font-size:.98rem;line-height:1.7}',
      '.swkv-go{display:inline-block;padding:15px 28px;background:var(--olive,#4A5040);color:var(--plaster,#F2EFE6);font-family:var(--body,"Jost",sans-serif);font-size:.76rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;transition:background .18s ease}',
      '.swkv-go:hover{background:var(--shadow,#161712)}',
      '.swkv-list{list-style:none;margin:0;padding:0;display:grid;gap:0}',
      '.swkv-list li{padding:16px 0;border-top:1px solid var(--hairline,rgba(22,23,18,.15));font-family:var(--body,"Jost",sans-serif);font-weight:300;font-size:.95rem;line-height:1.6}',
      '.swkv-list b{display:block;font-weight:500;margin-bottom:2px}',
      '.swkv-quote{grid-column:1/-1;margin:0;padding-top:28px;border-top:1px solid var(--hairline-firm,rgba(22,23,18,.32))}',
      '.swkv-quote p{margin:0;max-width:62ch;font-family:var(--display,"DM Serif Display",Didot,Georgia,serif);font-style:italic;font-size:clamp(1.1rem,2.2vw,1.35rem);line-height:1.5}',
      '.swkv-quote figcaption{margin-top:12px;font-family:var(--body,"Jost",sans-serif);font-size:.72rem;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--ash,#65665C)}'
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

  function injectHotelBand() {
    if (!/^\/hotels\//.test(location.pathname)) return;
    if (document.querySelector('.swkx-card')) return;
    var inquire = document.getElementById('inquire');
    if (!inquire || !inquire.parentNode) return;

    /* every hotel page carries the property name in the inquiry form */
    var field = document.querySelector('.inquire-form input[name="hotel"]');
    var name = field && field.value ? field.value.split(',')[0].trim() : '';

    var section = document.createElement('section');
    section.className = 'section swkx';
    section.innerHTML =
      '<div class="container">' +
        '<div class="swkx-card">' +
          '<p class="swkx-eyebrow">The Client Portal &middot; By Invitation</p>' +
          '<h2 class="swkx-h"><em></em> is in my private booking&nbsp;portal.</h2>' +
          '<p class="swkx-p">Clients of mine can book this hotel directly, any night of the year &mdash; the same rate you&rsquo;d pay the hotel, my Fora perks attached, and the reservation looked after from my desk. The portal is password-protected; access is something I grant personally.</p>' +
          '<div class="swkx-actions">' +
            '<a class="swkx-go" href="' + PORTAL + '" data-swk-book data-gtag-label="booking_desk" data-gtag-location="hotel_exclusive">Enter the client portal</a>' +
            '<a class="swkx-alt" href="#inquire" data-gtag-label="request_portal_access" data-gtag-location="hotel_exclusive">Request access</a>' +
          '</div>' +
          '<p class="swkx-note">Password protected. Already a client? Your login works above. If not &mdash; reach out to Keith below, and the door opens with your first trip.</p>' +
        '</div>' +
      '</div>';

    /* the hotel name goes in as text, never markup */
    var em = section.querySelector('.swkx-h em');
    if (name) {
      em.textContent = name;
    } else {
      em.textContent = 'This hotel';
    }

    inquire.parentNode.insertBefore(section, inquire);
  }

  /* Head-to-head pages (/x-vs-y.html): readers get their answer from the
     two "Choose…" cards and often leave before the form at the bottom.
     So, right where they decide:
     - an "Ask me about <hotel>" link under each card, which carries the
       hotel into the form (hidden field + heading) and jumps to it;
     - a "book through me" band after the cards: why booking with Keith
       is better than booking direct, at the same rate;
     - the phone sticky button speaks to the page ("Booking one of these?").
     Hotel names come from the comparison table's header row. */
  function injectVersusBand() {
    if (!/-vs-/.test(location.pathname)) return;
    if (document.querySelector('.swkv-card')) return;
    var choose = document.querySelector('.choose');
    var inquire = document.getElementById('inquire');
    var form = inquire && inquire.querySelector('form.inquire-form');
    if (!choose || !form) return;

    var names = [];
    var ths = document.querySelectorAll('table thead th');
    for (var i = 1; i < ths.length; i++) {
      names.push(ths[i].textContent.replace(/\?$/, '').trim());
    }

    /* 1 · an ask under each choice */
    var cols = choose.querySelectorAll('.choose-col');
    for (var c = 0; c < cols.length && c < names.length; c++) {
      if (!names[c]) continue;
      var a = document.createElement('a');
      a.className = 'swkv-ask';
      a.href = '#inquire';
      a.setAttribute('data-swkv-hotel', names[c]);
      a.setAttribute('data-gtag-label', 'versus_ask_hotel');
      a.setAttribute('data-gtag-location', 'choose_card');
      a.textContent = 'Ask me about ' + names[c] + ' →';
      cols[c].appendChild(a);
    }

    var heading = inquire.querySelector('h2');
    var interested = document.createElement('input');
    interested.type = 'hidden';
    interested.name = 'interested_in';
    form.appendChild(interested);

    document.addEventListener('click', function (e) {
      var ask = e.target.closest('[data-swkv-hotel]');
      if (!ask) return;
      var hotel = ask.getAttribute('data-swkv-hotel');
      interested.value = hotel;
      if (heading) heading.textContent = 'Leaning toward ' + hotel + '?';
      var when = form.querySelector('input[name="travel_dates"]');
      if (when) window.setTimeout(function () { when.focus({ preventScroll: true }); }, 450);
    });

    /* 2 · the band after the cards */
    var host = choose.closest('section');
    if (host && host.parentNode) {
      /* General client praise, one per page, picked from the page slug so it
         stays put. Same list, order and pick as phase1/src/data/clientquotes.js;
         Passalacqua pages always get C&J, who stayed there through Keith. */
      var quotes = [
        ['&ldquo;I love booking hotels through you. I&rsquo;m going to spread the word to everyone.&rdquo;', 'C&amp;J &middot; SWK Clients'],
        ['&ldquo;Worth its weight in gold. I won&rsquo;t ever book a stay without Keith again.&rdquo;', 'Caitlin M. &middot; SWK Client'],
        ['&ldquo;Keith made me believe in using travel agents again. He carefully put together thoughtful options and called out why he would choose each.&rdquo;', 'Stephanie F. &middot; SWK Client'],
        ['&ldquo;He handled everything, from booking to communications, and I didn&rsquo;t have to worry about a thing.&rdquo;', 'Nida T. &middot; SWK Client'],
        ['&ldquo;Luxury hotels naturally have many guests competing for attention, but having Keith in our corner made us feel like a priority throughout the entire experience.&rdquo;', 'Tyler &amp; Spencer C. &middot; SWK Clients']
      ];
      var slug = location.pathname.replace(/^.*\//, '').replace(/\.html$/, '');
      var pick = 0;
      if (!/passalacqua/.test(slug)) {
        var hsh = 0;
        for (var k = 0; k < slug.length; k++) hsh = (hsh * 31 + slug.charCodeAt(k)) >>> 0;
        pick = hsh % quotes.length;
      }
      var quote = '<figure class="swkv-quote">' +
          '<p>' + quotes[pick][0] + '</p>' +
          '<figcaption>' + quotes[pick][1] + '</figcaption>' +
        '</figure>';
      var section = document.createElement('section');
      section.className = 'section swkv';
      section.innerHTML =
        '<div class="container">' +
          '<div class="swkv-card">' +
            '<div>' +
              '<p class="swkv-eyebrow">Booking one of these?</p>' +
              '<h2 class="swkv-h">Book through me, and the hotel <em>knows you&rsquo;re coming.</em></h2>' +
              '<p class="swkv-p">I&rsquo;ve been to both of these hotels in person, and I&rsquo;ve personally vetted every hotel on this site. I know their teams, and I send them clients. They take extra care of Suites With Keith clients, and I make sure you&rsquo;re well looked after from the day you book to the day you check out.</p>' +
              '<a class="swkv-go" href="#inquire" data-gtag-label="versus_trust_cta" data-gtag-location="versus_band">Get my recommendation</a>' +
            '</div>' +
            '<ul class="swkv-list">' +
              '<li><b>The right room.</b>I know which rooms to ask for, and which ones to skip.</li>' +
              '<li><b>A note before you arrive.</b>The hotel hears from me about you, the occasion and how you like things.</li>' +
              '<li><b>Fora X perks.</b>Typically daily breakfast, a hotel credit and an upgrade when available.</li>' +
              '<li><b>The same rate as booking direct.</b>Plus a direct line to me while you&rsquo;re there.</li>' +
            '</ul>' +
            quote +
          '</div>' +
        '</div>';
      host.parentNode.insertBefore(section, host.nextSibling);
    }

    /* 3 · the phone sticky button */
    var sticky = document.querySelector('.sticky-cta');
    if (sticky) {
      sticky.textContent = 'Booking one of these? Ask me';
      sticky.setAttribute('data-gtag-label', 'versus_sticky');
      sticky.setAttribute('data-gtag-location', 'sticky_mobile');
    }
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
