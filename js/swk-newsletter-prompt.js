/*!
 * Suites With Keith: soft newsletter prompt
 *
 * What it does
 *  - Counts the unique editorial pages a reader has opened (stored in localStorage).
 *  - On their Nth article (default 3), once they're halfway down the page or after
 *    25 seconds, slides a small card up from the bottom corner. It is never a
 *    full-screen overlay, so it stays clear of Google's intrusive-interstitial rules.
 *  - "Not now" hides it for 30 days. Subscribing hides it for good.
 *  - Never appears on the home page, inquiry, planning, proposal or service pages.
 *  - Comparison pages: put <div data-swk-newsletter-inline></div> at the end of the
 *    comparison. It is an invisible marker; when the reader scrolls to it, the same
 *    floating card slides in with "Enjoyed this comparison?" copy, on any visit count.
 *
 * Install: add one line before </body> on every page:
 *   <script src="/js/swk-newsletter-prompt.js" defer></script>
 *
 * Preview on any page: add ?swk-newsletter=preview to the URL.
 * Reset your own counter: add ?swk-newsletter=reset to the URL.
 */
(function () {
  "use strict";

  /* ------------------------------------------------------------------ */
  /* SETTINGS: edit these                                                */
  /* ------------------------------------------------------------------ */
  var CONFIG = {
    // How the email gets to Beehiiv. Pick one:
    //  "beehiiv-embed": paste your Beehiiv embed ID below. No backend needed.
    //     Beehiiv > Grow > Subscribe Forms > (your form) > Embed. The ID is the
    //     long code in https://embeds.beehiiv.com/XXXXXXXX
    //  "endpoint": your own brand-styled form that POSTs { email, source } as JSON
    //     to endpointUrl (a small serverless function that calls the Beehiiv API).
    // The site is static (GitHub Pages), so the endpoint is a Cloudflare Worker:
    // workers/subscribe/worker.js. Until endpointUrl is filled in, the script falls
    // back to the Beehiiv embed below.
    mode: "endpoint",
    beehiivEmbedId: "f7386044-3940-49ca-ab13-051728385b6d",
    endpointUrl: "https://swk-subscribe.keith-pence.workers.dev",

    showOnArticle: 3,          // prompt on the 3rd unique article
    scrollTrigger: 0.5,        // ...once they're 50% down the page
    timeTriggerMs: 25000,      // ...or after 25 seconds, whichever comes first
    snoozeDays: 30,            // "Not now" hides it this long

    // Pages that never count and never show the prompt. Paths are matched with
    // and without ".html" (GitHub Pages serves both). The inquiry form lives on
    // the home page (/index.html#inquire), so the home rules cover it.
    excludePaths: [
      /^\/$/,                                        // home + inquiry
      /^\/index(\.html)?$/,
      /^\/planning-with-swk/,                        // planning
      /^\/proposals\//,                              // client proposals
      /^\/sample-(proposal|itinerary)/,              // sample proposals
      /^\/guides\/sea-transfers-/,                   // unlisted client guides
      /^\/(services|corporate-travel|private-boat-transfers|amalfi-boat-transfers|private-jet-charter|hoper|santorini-weddings)(\.html)?$/, // service pages
      /^\/(subscribe|subscriber-welcome)(\.html)?$/, // signup + thank-you
      /^\/(404|privacy|style-guide|guide_template)(\.html)?$/,
      /^\/blueprint\//
    ],

    copy: {
      eyebrow: "The SWK Letter",
      headline: "New reviews, <em>first</em>.",
      body: "Firsthand hotel reviews, head-to-head comparisons and the trips I'm booking right now, a couple of times a month. Free.",
      button: "Subscribe",
      dismiss: "Not now",
      success: "You're in. Thank you for reading.",
      error: "Something went wrong. Please try again.",
      inlineHeadline: "Enjoyed this <em>comparison</em>?",
      inlineBody: "Get my next firsthand reviews and comparisons in your inbox before they go up on the site."
    }
  };
  /* ------------------------------------------------------------------ */

  var KEY = "swk_nl_v1";
  var now = Date.now();
  var DAY = 86400000;

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  function save(s) {
    try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) { /* storage blocked */ }
  }

  var params = new URLSearchParams(location.search);
  var flag = params.get("swk-newsletter");
  if (flag === "reset") {
    try { localStorage.removeItem(KEY); sessionStorage.removeItem("swk_nl_seen"); } catch (e) {}
  }
  var preview = flag === "preview";

  var state = load();
  state.pages = state.pages || [];

  var path = location.pathname.replace(/\/+$/, "") || "/";

  // Coming back from a Beehiiv email, the Beehiiv confirmation, or landing on the
  // welcome page Beehiiv redirects to counts as subscribed.
  if (/beehiiv/i.test(params.get("utm_source") || "") || params.has("subscribed") ||
      /^\/subscriber-welcome(\.html)?$/.test(path)) {
    state.subscribed = true;
    save(state);
  }

  var excluded = CONFIG.excludePaths.some(function (re) { return re.test(path); });
  var useEndpoint = CONFIG.mode === "endpoint" && !!CONFIG.endpointUrl;

  /* ---------------- styles (Plaster & Shadow) ---------------- */
  var css = [
    ".swk-nl{--plaster:#F2EFE6;--lime:#FBFAF6;--ink:#1F201A;--ash:#65665C;--brass:#836229;--olive:#4A5040;--olive-deep:#3B4033;--hair:rgba(22,23,18,.15);",
    "font-family:'Newsreader',Georgia,serif;color:var(--ink);box-sizing:border-box}",
    ".swk-nl *{box-sizing:border-box;border-radius:0}",
    ".swk-nl-card{position:fixed;z-index:9999;right:24px;bottom:24px;width:380px;max-width:calc(100vw - 32px);background:var(--lime);border:1px solid var(--hair);padding:28px 28px 22px;",
    "transform:translateY(16px);opacity:0;transition:transform .35s ease,opacity .35s ease}",
    ".swk-nl-card.is-open{transform:none;opacity:1}",
    ".swk-nl-close{position:absolute;top:10px;right:12px;background:none;border:0;font:400 22px/1 'Newsreader',Georgia,serif;color:var(--ash);cursor:pointer;padding:6px}",
    ".swk-nl-close:hover{color:var(--ink)}",
    ".swk-nl-eyebrow{font-family:'Instrument Serif',Georgia,serif;text-transform:uppercase;letter-spacing:.14em;font-size:12px;color:var(--brass);margin:0 0 10px}",
    ".swk-nl-h{font-family:'Instrument Serif',Georgia,serif;font-weight:400;font-size:30px;line-height:1.08;margin:0 0 10px}",
    ".swk-nl-h em{font-style:italic}",
    ".swk-nl-p{font-size:16px;line-height:1.5;color:var(--ash);margin:0 0 18px}",
    ".swk-nl-form{display:flex;gap:0;border:1px solid var(--ink)}",
    ".swk-nl-input{flex:1;min-width:0;border:0;background:#fff;padding:12px 14px;font:400 16px 'Newsreader',Georgia,serif;color:var(--ink)}",
    ".swk-nl-input:focus{outline:2px solid var(--olive);outline-offset:-2px}",
    ".swk-nl-btn{border:0;background:var(--olive);color:var(--plaster);padding:0 18px;font-family:'Instrument Serif',Georgia,serif;text-transform:uppercase;letter-spacing:.12em;font-size:13px;cursor:pointer}",
    ".swk-nl-btn:hover{background:var(--olive-deep)}",
    ".swk-nl-btn[disabled]{opacity:.6;cursor:default}",
    ".swk-nl-embed{width:100%;height:52px;border:0;display:block;background:transparent}",
    ".swk-nl-msg{font-size:14px;margin:10px 0 0;min-height:1em;color:var(--ash)}",
    ".swk-nl-later{display:inline-block;margin-top:12px;background:none;border:0;padding:0;font-family:'Instrument Serif',Georgia,serif;text-transform:uppercase;letter-spacing:.12em;font-size:12px;color:var(--ash);cursor:pointer;border-bottom:1px solid var(--hair)}",
    ".swk-nl-later:hover{color:var(--ink)}",
    ".swk-nl-inline{max-width:720px;margin:56px auto;border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);padding:36px 0}",
    ".swk-nl-inline .swk-nl-h{font-size:34px}",
    // The slot sits outside the page .container, so give it the site's 20px gutter on narrow screens.
    "@media (max-width:760px){.swk-nl-inline{margin-left:20px;margin-right:20px}}",
    "@media (max-width:600px){.swk-nl-card{right:0;left:0;bottom:0;width:100%;max-width:100%;border-left:0;border-right:0;border-bottom:0;padding:22px 20px 18px}",
    ".swk-nl-card .swk-nl-h{font-size:26px}.swk-nl-card .swk-nl-p{font-size:15px;margin-bottom:14px}}",
    "@media (prefers-reduced-motion:reduce){.swk-nl-card{transition:none}}"
  ].join("");

  function injectStyles() {
    if (document.getElementById("swk-nl-css")) return;
    var s = document.createElement("style");
    s.id = "swk-nl-css";
    s.textContent = css;
    document.head.appendChild(s);
  }

  /* ---------------- shared signup form ---------------- */
  function buildForm(source, onDone) {
    var wrap = document.createElement("div");

    if (!useEndpoint) {
      var f = document.createElement("iframe");
      f.className = "swk-nl-embed";
      f.title = "Subscribe to The SWK Letter";
      f.loading = "lazy";
      f.src = "https://embeds.beehiiv.com/" + encodeURIComponent(CONFIG.beehiivEmbedId) + "?slim=true";
      wrap.appendChild(f);
      // We can't see inside Beehiiv's iframe, so treat a click into it as intent
      // and stop prompting after this visit. The utm/?subscribed check catches the rest.
      window.addEventListener("blur", function () {
        if (document.activeElement === f) { onDone(true); }
      });
      return wrap;
    }

    var form = document.createElement("form");
    form.className = "swk-nl-form";
    form.noValidate = true;
    form.innerHTML =
      '<input class="swk-nl-input" type="email" aria-label="Email address" name="email" autocomplete="email" placeholder="Your email" required>' +
      '<button class="swk-nl-btn" type="submit">' + CONFIG.copy.button + "</button>" +
      // Honeypot: hidden from people, bots fill it, the Worker ignores those.
      '<input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">';
    var msg = document.createElement("p");
    msg.className = "swk-nl-msg";
    msg.setAttribute("aria-live", "polite");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = form.querySelector('input[name="email"]');
      var btn = form.querySelector("button");
      var email = (input.value || "").trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        msg.textContent = "Please enter a valid email.";
        input.focus();
        return;
      }
      btn.disabled = true;
      fetch(CONFIG.endpointUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, source: source, page: path, website: form.elements.website.value })
      }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        form.style.display = "none";
        msg.textContent = CONFIG.copy.success;
        onDone(true);
      }).catch(function () {
        btn.disabled = false;
        msg.textContent = CONFIG.copy.error;
      });
    });

    wrap.appendChild(form);
    wrap.appendChild(msg);
    return wrap;
  }

  function markSubscribed() {
    state.subscribed = true;
    save(state);
  }

  /* ---------------- end-of-comparison trigger ---------------- */
  // <div data-swk-newsletter-inline></div> is an invisible marker at the end of a
  // comparison. When the reader scrolls to it, the floating card slides in with the
  // comparison copy. Nothing renders in the page itself.
  function armAtMarker(marker) {
    function check() {
      // Fire once the marker is in the lower part of the screen (or above it).
      if (marker.getBoundingClientRect().top <= window.innerHeight * 0.85) {
        window.removeEventListener("scroll", check);
        openCard("comparison");
      }
    }
    window.addEventListener("scroll", check, { passive: true });
    setTimeout(check, 1500); // a reload that's already scrolled to the end
  }

  /* ---------------- slide-in card ---------------- */
  var card, lastFocus;

  function closeCard(snooze) {
    if (!card) return;
    if (snooze) { state.snoozedUntil = now + CONFIG.snoozeDays * DAY; save(state); }
    card.classList.remove("is-open");
    document.removeEventListener("keydown", onKey);
    var c = card;
    card = null;
    setTimeout(function () { c.remove(); }, 400);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function onKey(e) { if (e.key === "Escape") closeCard(true); }

  function openCard(variant) {
    if (card) return;
    var isComparison = variant === "comparison";
    injectStyles();
    lastFocus = document.activeElement;
    card = document.createElement("aside");
    card.className = "swk-nl swk-nl-card";
    card.setAttribute("role", "dialog");
    card.setAttribute("aria-label", "Subscribe to The SWK Letter");
    card.innerHTML =
      '<button class="swk-nl-close" type="button" aria-label="Close">&times;</button>' +
      '<p class="swk-nl-eyebrow">' + CONFIG.copy.eyebrow + "</p>" +
      '<h2 class="swk-nl-h">' + (isComparison ? CONFIG.copy.inlineHeadline : CONFIG.copy.headline) + "</h2>" +
      '<p class="swk-nl-p">' + (isComparison ? CONFIG.copy.inlineBody : CONFIG.copy.body) + "</p>";
    card.appendChild(buildForm(isComparison ? "comparison" : "slide-in", function (ok) {
      if (!ok) return;
      markSubscribed();
      if (useEndpoint) setTimeout(function () { closeCard(false); }, 2200);
    }));
    var later = document.createElement("button");
    later.type = "button";
    later.className = "swk-nl-later";
    later.textContent = CONFIG.copy.dismiss;
    card.appendChild(later);

    card.querySelector(".swk-nl-close").addEventListener("click", function () { closeCard(true); });
    later.addEventListener("click", function () { closeCard(true); });
    document.addEventListener("keydown", onKey);

    document.body.appendChild(card);
    requestAnimationFrame(function () { requestAnimationFrame(function () { card && card.classList.add("is-open"); }); });
    if (!preview) {
      // Only count it as shown once it has actually appeared, so leaving a page
      // before the trigger fires doesn't use up this visit's prompt.
      try { sessionStorage.setItem("swk_nl_seen", "1"); } catch (e) {}
      state.lastShown = now;
      save(state);
    }
  }

  function armTriggers(variant) {
    var fired = false;
    function fire() {
      if (fired) return;
      fired = true;
      window.removeEventListener("scroll", onScroll);
      clearTimeout(t);
      openCard(variant);
    }
    function onScroll() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      if (h <= 0 || window.scrollY / h >= CONFIG.scrollTrigger) fire();
    }
    var t = setTimeout(fire, CONFIG.timeTriggerMs);
    window.addEventListener("scroll", onScroll, { passive: true });
    setTimeout(onScroll, 1500); // short pages, or a reload that's already scrolled down
  }

  /* ---------------- run ---------------- */
  function run() {
    var marker = document.querySelector("[data-swk-newsletter-inline]");
    if (preview) { openCard(marker ? "comparison" : "article"); return; }
    if (excluded) return;

    if (state.pages.indexOf(path) === -1) {
      state.pages.push(path);
      if (state.pages.length > 200) state.pages = state.pages.slice(-200);
      save(state);
    }

    var snoozed = state.snoozedUntil && state.snoozedUntil > now;
    var shownThisSession = false;
    try { shownThisSession = sessionStorage.getItem("swk_nl_seen") === "1"; } catch (e) {}

    if (state.subscribed || snoozed || shownThisSession) return;

    // Comparison pages: slide in when the reader reaches the end of the comparison,
    // whatever their article count.
    if (marker) { armAtMarker(marker); return; }

    // Everything else: on the 3rd unique article, at 50% scroll or 25 seconds.
    if (state.pages.length < CONFIG.showOnArticle) return;
    armTriggers("article");
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
