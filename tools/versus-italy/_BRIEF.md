# Brief: writing Italy head-to-head pages for suiteswithkeith.com

You are writing hotel comparison ("vs") pages for Keith Pence's luxury travel advisor site. Each page is a JSON spec in
`tools/versus-italy/<slug>.json`, rendered to `/<slug>.html` by `python3 tools/render_vs_italy.py <slug>`.
These pages generate real client inquiries, so accuracy and voice matter more than speed.

## Read first
1. `tools/versus-italy/forestis-vs-aman-rosa-alpina.json` — the model spec. Copy its shape exactly (same keys, 10ish rows,
   3 band paras, exactly 4 guide sections each with an image and 2 paras, 5–6 FAQs, 3–5 related links).
2. `il-san-pietro-vs-le-sirenuse.html` — a finished page in Keith's voice. Also skim one existing vs page in your region if any
   (listed below) for tone.
3. For every hotel in your pairs: `python3 tools/versus-italy/_extract.py hotels/<file>.html` (plain-text dump with
   `[IMG src | alt]` markers), plus the destination hub page for your region. These are your ONLY sources of fact.

## Hard rules
- **No invented facts.** Every claim (room advice, distances, prices, amenities, opinions, rankings, who-it-suits) must come from
  Keith's hotel pages or hub page. If a comparison dimension isn't covered for a hotel, drop that row or phrase it from what is
  known. Do not use outside knowledge about the hotels. Do not invent opinions Keith didn't express; when Keith has a stated
  favourite/ranking (hub page "pick by trip", "my top pick", "close second", etc.), the verdict must agree with it.
- **Stamp must be truthful**, from each hotel page's own wording: "Stayed at X &middot; Toured Y &middot; October 2026",
  or "Stayed at both &middot; October 2026", "Toured both &middot; October 2026". Rome pages say "visited" for non-stayed hotels
  ("Stayed at the Eden &middot; Visited the Bulgari &middot; October 2026"). Lake Como's Grand Hotel Tremezzo and Villa d'Este:
  "Toured, with lunch". Never say stayed unless the hotel page says stayed.
- **Images:** only image paths that actually appear in that hotel's page (or hub page) and exist on disk. Reuse their alt text
  (you may shorten it). Hero = one image per hotel (a = left, b = right). Choose-column images and guide images should differ
  from the hero where the hotel has enough photos. Check every src exists with `ls`.
- **Voice:** first person as Keith, plain, warm, decisive, short sentences. Match the model. Style rules from a sitewide copy
  pass: NO em dashes (use commas, colons or periods), no "X, not Y" constructions, no stock travel words (nestled, boasts,
  oasis, gem, unparalleled, breathtaking, curated, elevate, indulge, haven, iconic is OK only if Keith's page uses it). Use HTML
  entities like the model (&rsquo; &middot; &amp;). Every mention of a hotel in band/guide/faq prose should link to its review
  (`<a href="/hotels/....html">`) the first time in each paragraph/answer, like the model.
- `a.short` / `b.short` are the short display names (e.g. "Hotel Eden", "Bulgari"). They drive "Choose X", "My X review",
  table headers and the form subject. Choose eyebrow is auto "Choose <short>".
- `h1_a` = "<A> or", `h1_b` = "<B>?". `place` = the eyebrow location (e.g. "Rome", "Lake Como", "Dolomites", "Amalfi Coast",
  "Venice"). Title format: "<A> vs <B>: <angle> (2026) | Suites With Keith" (keep under ~70 chars before the pipe if you can).
  Description: one sentence like the model, naming the visit type truthfully.
- `pitch`: one sentence variant of the model's Fora pitch, tailored with pair-specific things Keith arranges (from the pages).
- The `choose` order matches a/b. Put Keith's preferred hotel of the pair as "a" where he has a clear preference, and give it
  the h3 "My pick of the two". If it genuinely depends on the trip, both h3s can be "If you want ..." style.
- `related`: both reviews, 1–2 sibling vs pages from the full slug list below that share a hotel, and the region hub.
  Only link to slugs in the list below or pages that already exist.
- Don't edit any shared file (hotel pages, hubs, sitemap, renderer, other agents' specs). Only create your assigned JSON specs
  and run the renderer on them. The lead handles linking and sitemap.

## Verify before finishing
- `python3 tools/render_vs_italy.py <your slugs>` succeeds; JSON valid.
- Every `src=`/`href="/...` in your rendered pages resolves to an existing file (write a quick check).
- grep your specs for `—` (em dash) and fix any.
- Re-read each spec once against the source pages for factual accuracy, and fix anything you can't source.
- Report back: the slugs written, plus any pair where sources were thin and how you handled it. Keep the report short.

## Full slug list (all Italy vs pages that will exist; hub pages in brackets)
Dolomites [dolomites.html, dolomites-hotels.html]: forestis-vs-aman-rosa-alpina forestis-vs-como-alpina forestis-vs-gardena-grodnerhof
 forestis-vs-miramonti aman-rosa-alpina-vs-como-alpina aman-rosa-alpina-vs-gardena-grodnerhof aman-rosa-alpina-vs-miramonti
 como-alpina-vs-gardena-grodnerhof como-alpina-vs-miramonti gardena-grodnerhof-vs-miramonti
Rome [rome.html]: hotel-eden-vs-la-minerva hotel-eden-vs-hotel-de-russie hotel-eden-vs-hassler-roma hotel-eden-vs-bulgari-rome
 hotel-eden-vs-corinthia-rome hotel-eden-vs-hotel-de-la-ville hotel-eden-vs-casa-monti la-minerva-vs-hotel-de-russie
 la-minerva-vs-hassler-roma la-minerva-vs-bulgari-rome la-minerva-vs-corinthia-rome la-minerva-vs-hotel-de-la-ville
 la-minerva-vs-casa-monti hotel-de-russie-vs-hassler-roma hotel-de-russie-vs-bulgari-rome hotel-de-russie-vs-corinthia-rome
 hotel-de-russie-vs-hotel-de-la-ville hotel-de-russie-vs-casa-monti hassler-roma-vs-bulgari-rome hassler-roma-vs-corinthia-rome
 hassler-roma-vs-hotel-de-la-ville hassler-roma-vs-casa-monti bulgari-rome-vs-corinthia-rome bulgari-rome-vs-hotel-de-la-ville
 bulgari-rome-vs-casa-monti corinthia-rome-vs-hotel-de-la-ville corinthia-rome-vs-casa-monti hotel-de-la-ville-vs-casa-monti
Lake Como [lake-como.html, lake-como-hotels-ranked.html] existing: grand-hotel-tremezzo-vs-lake-como-edition
 grand-hotel-tremezzo-vs-passalacqua grand-hotel-tremezzo-vs-villa-d-este il-sereno-vs-passalacqua lake-como-edition-vs-il-sereno
 villa-d-este-vs-villa-serbelloni; new: grand-hotel-tremezzo-vs-il-sereno grand-hotel-tremezzo-vs-villa-serbelloni
 il-sereno-vs-villa-d-este il-sereno-vs-villa-serbelloni lake-como-edition-vs-passalacqua lake-como-edition-vs-villa-d-este
 lake-como-edition-vs-villa-serbelloni passalacqua-vs-villa-d-este passalacqua-vs-villa-serbelloni
Venice [venice.html] existing: aman-venice-vs-airelles-palladio aman-venice-vs-danieli-four-seasons aman-venice-vs-orient-express-venice
 airelles-palladio-vs-danieli-four-seasons orient-express-venice-vs-danieli-four-seasons; new: airelles-palladio-vs-orient-express-venice
Amalfi Coast [positano-hotels.html] existing: il-san-pietro-vs-le-sirenuse il-san-pietro-vs-villa-treville le-sirenuse-vs-villa-treville;
 new: il-san-pietro-vs-santa-caterina le-sirenuse-vs-santa-caterina villa-treville-vs-santa-caterina

Slug order is fixed (use exactly these filenames) even if you make the second-named hotel "a" in the spec.

## Hotel page files
Dolomites: hotels/forestis-dolomites, aman-rosa-alpina-dolomites, como-alpina-dolomites, gardena-grodnerhof-ortisei, miramonti-merano
 (also /forestis-villa-dolomites.html exists)
Rome: hotels/hotel-eden-rome, orient-express-la-minerva-rome, hotel-de-russie-rome, hassler-roma, bulgari-hotel-rome,
 corinthia-rome, hotel-de-la-ville-rome, casa-monti-rome (also /la-dolce-vita-orient-express.html)
Lake Como: hotels/grand-hotel-tremezzo-lake-como, il-sereno-lake-como, lake-como-edition, passalacqua-lake-como,
 villa-d-este-lake-como, villa-serbelloni-bellagio
Venice: hotels/airelles-palladio-venice, orient-express-venice (+ venice.html, venice-new-luxury-hotels-2026.html)
Amalfi: hotels/hotel-santa-caterina-amalfi, il-san-pietro-di-positano, le-sirenuse-positano, villa-treville-positano
