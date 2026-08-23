#!/usr/bin/env python3
"""Generate the 10 Greece hotel guide pages for suiteswithkeith.com."""
import html
from string import Template
from urllib.parse import quote

SITE = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))

PAGE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0J39101CS2"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-0J39101CS2');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$name Review — $locale | Suites With Keith</title>
<meta name="description" content="$meta_desc">
<link rel="canonical" href="https://suiteswithkeith.com/hotels/$slug.html">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="icon" href="../favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">

<meta property="og:type" content="article">
<meta property="og:title" content="$name Review — $locale | Suites With Keith">
<meta property="og:description" content="$meta_desc">
<meta property="og:url" content="https://suiteswithkeith.com/hotels/$slug.html">
<meta property="og:image" content="https://suiteswithkeith.com/images/$img_dir/$hero_img">
<meta property="og:site_name" content="Suites With Keith">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="$name Review — $locale | Suites With Keith">
<meta name="twitter:description" content="$meta_desc">
<meta name="twitter:image" content="https://suiteswithkeith.com/images/$img_dir/$hero_img">

<link rel="stylesheet" href="../styles.css">
<link rel="stylesheet" href="../guide.css">
<style>
  .glance-row { display: block; font-size: 0.88rem; color: var(--charcoal); padding: 9px 0; border-bottom: 1px solid var(--hairline); }
  .glance-row:last-child { border-bottom: none; }
  .glance-row .g-label { display: block; font-size: 0.64rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--olive-deep); font-weight: 600; margin-bottom: 2px; }
</style>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "$name Review — $locale",
  "description": "$meta_desc",
  "image": "https://suiteswithkeith.com/images/$img_dir/$hero_img",
  "author": { "@type": "Person", "name": "Keith Pence" },
  "publisher": {
    "@type": "Organization",
    "name": "Suites With Keith",
    "logo": { "@type": "ImageObject", "url": "https://suiteswithkeith.com/favicon-32.png" }
  },
  "mainEntityOfPage": { "@type": "WebPage", "@id": "https://suiteswithkeith.com/hotels/$slug.html" }
}
</script>
</head>
<body>

<nav class="site-nav">
  <div class="container">
    <a href="../index.html" class="nav-brand"><span class="nav-word">Suites With Keith</span></a>
    <div class="nav-links">
      <a href="../services.html">Services</a>
      <a href="../greece-collection.html">The Greece Collection</a>
      <a href="../destination-guides.html">Destination Guides</a>
      <a href="../rankings.html" class="active">Keith's Rankings</a>
      <a href="../about.html">About</a>
    </div>
  </div>
</nav>

<header class="rank-hero" style="background-image:url('../images/$img_dir/$hero_img');">
  <div class="container">
    <span class="eyebrow-mag">Hotel Guides &middot; $locale</span>
    <h1>$name</h1>
    <p class="tagline">$tagline</p>
    <div class="rank-stats">
      <div><span class="stat-num">$stat1_num</span><span class="stat-label">$stat1_label</span></div>
      <div><span class="stat-num">$stat2_num</span><span class="stat-label">$stat2_label</span></div>
    </div>
    <div style="margin-top:32px;">
      <a href="#inquire" class="btn btn-tan" data-gtag-label="inquire_to_book" data-gtag-location="hotel_hero">Inquire To Book</a>
    </div>
  </div>
</header>

<section class="rank-intro">
  <div class="container">
    <div>
$intro_paras
      <p><a href="../$rank_href" class="read-link">$related_text &rarr;</a></p>
    </div>
    <div class="rank-toc">
      <h4>At A Glance</h4>
      <span class="glance-row"><span class="g-label">$region_label</span>$region_html</span>
      <span class="glance-row"><span class="g-label">Style</span>$style_label</span>
      <span class="glance-row"><span class="g-label">Perfect For</span>$perfect_for</span>
      <span class="glance-row"><span class="g-label">My Ranking</span><a href="../$rank_href">$rank_text &rarr;</a></span>
    </div>
  </div>
</section>

<section class="rank-list">
  <div class="container">
    <div class="rank-card">
      <div class="rank-media">
        <img src="../images/$img_dir/$img2" alt="$name, $island">
      </div>
      <div class="rank-copy">
        <span class="rank-num">What Stood Out</span>
        <h3>The Details That Made The List</h3>
        <div class="rank-notes" style="margin-top:18px;">
$stood_out_notes
        </div>
      </div>
    </div>

    <div class="rank-card" style="display:block;">
      <div class="rank-copy" style="max-width:860px;">
        <span class="rank-num">Know Before You Book</span>
        <h3>$know_heading</h3>
        <div class="rank-notes" style="margin-top:18px;">
$know_notes
        </div>
        <p class="rank-take">$verdict</p>
      </div>
    </div>
  </div>
</section>

<section class="physical-note">
  <div class="container">
    <div class="print-callout">
      <span class="eyebrow-mag">Book $short_name Through Me</span>
      <h3>Same Rate, More Perks</h3>
      <p>$perks_html</p>
      <a href="#inquire" class="btn btn-olive" data-gtag-label="check_availability" data-gtag-location="hotel_perks">Check Availability</a>
    </div>
  </div>
</section>

<section class="guide-cta" id="inquire">
  <div class="container">
    <span class="eyebrow">Planning A Trip To $island?</span>
    <h2>$cta_line</h2>
    <form class="hotel-inquire-form" action="https://formspree.io/f/mjgnadov" method="POST">
      <input type="hidden" name="_subject" value="$plain_name Inquiry">
      <input type="hidden" name="hotel" value="$plain_name">
      <input type="hidden" name="page" value="hotels/$out_file">
      <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
      <div class="hi-step1">
        <label for="hi-when">When are you thinking?</label>
        <input id="hi-when" type="text" name="travel_dates" placeholder="Late June, 5 nights" required autocomplete="off">
      </div>
      <div class="hi-step2">
        <label for="hi-name">And where do I send the recommendation?</label>
        <input id="hi-name" type="text" name="name" placeholder="Name" required autocomplete="name">
        <input id="hi-email" type="email" name="email" placeholder="Email" required autocomplete="email">
      </div>
      <button type="submit" class="btn btn-tan" data-gtag-label="hotel_inquiry_send" data-gtag-location="hotel_cta">Send</button>
      <p class="hi-note">Traveling within the next 30 days? You&rsquo;ll hear from me today.</p>
      <p class="hi-status" role="status" aria-live="polite"></p>
    </form>
    <p style="margin-top:26px;"><a href="../$island_page" class="read-link">$cta_island_text &rarr;</a> &nbsp;&nbsp; <a href="../$cta2_href" class="read-link">$cta2_text &rarr;</a></p>
  </div>
</section>

<footer class="site-footer">
  <div class="container footer-signup">
    <p class="tagline">Subscribe to stay in the loop on all things luxury travel.</p>
    <div class="beehiiv-wrap">
      <script async src="https://subscribe-forms.beehiiv.com/v3/loader.js" data-beehiiv-form="02920925-682b-4b12-a526-e4fe0939610c"></script>
      <p class="signup-continue"><a href="../subscriber-welcome.html">Just subscribed? Continue to your welcome page &rarr;</a></p>
    </div>
  </div>
  <div class="container footer-grid">
    <div>
      <h4>Suites With Keith</h4>
      <p class="footer-slogan">Better Rooms. Better Trips.</p>
      <p>Luxury travel advisor specializing in Europe, honeymoons, hotel bookings, and personalized itineraries.</p>
    </div>
    <div class="footer-mid">
      <div class="footer-badge">SWK</div>
      <div class="partner-logos">
        <a href="https://www.virtuoso.com/advisor/keitpenc76094/" target="_blank" rel="noopener" aria-label="Keith Pence on Virtuoso"><img src="../images/logos/virtuoso.png" alt="Virtuoso"></a>
        <img src="../images/logos/fora-pro.png" alt="Fora Pro">
      </div>
    </div>
    <div class="footer-right">
      <h4>Get In Touch</h4>
      <p>keith.pence@fora.travel</p>
      <p><a href="https://instagram.com/suiteswithkeith">@suiteswithkeith</a></p>
      <p><a href="../privacy.html">Privacy Policy</a></p>
    </div>
  </div>
</footer>

<script src="../track.js" defer></script>
<script src="../reveal.js" defer></script>
<script defer src="../js/hotel-inquire.js"></script>
<script defer src="../js/swk-events.js"></script>
</body>
</html>
""")

def note(b, t):
    return f'          <p class="note-item"><b>{b}</b> {t}</p>'

def para(t):
    return f'      <p>{t}</p>'

HOTELS = [
    dict(
        slug="canaves-epitome-santorini", name="Canaves Epitome", short_name="Epitome",
        island="Santorini", island_page="santorini.html", rank_num="01",
        hero_img="canaves-epitome-1.jpg", img2="canaves-epitome-2.jpg",
        stat2_num="53", stat2_label="Rooms, No Age Restrictions",
        meta_desc="Keith's firsthand review of Canaves Epitome — his favorite hotel across nine Greek islands, a short walk from Oia with the best sunset in Greece.",
        tagline="My favorite hotel across nine islands in the Cyclades — and perhaps one of the top three stays of my entire life.",
        style_label="Boutique luxury resort", perfect_for="Return visitors, families, privacy seekers",
        credit_label="hotel credit", partner_clause=" with a preferred partnership at Canaves", visited_verb="stayed at",
        intro=[
            "Wow, I don't really know what to say about Epitome, other than wow. It makes an excellent case for being the #1 hotel in Santorini — the only drawback, or benefit depending on your preference, is the location. Epitome sits a short walk from Oia near Ammoudi Bay rather than directly on the Caldera, and that single fact shapes everything about the experience.",
            "What it buys you is space and serenity. Landscaped gardens behind volcanic-rock walls make the common areas feel like a world away from the busy streets of Oia, and despite being more spread out than the Caldera hotels, its 53 rooms still feel boutique. There are no age restrictions here, which makes it one of the very few true luxury options on Santorini for families.",
            "And then there's the sunset. Because you're not tucked into the Caldera bowl, you watch an actual sunset into the Aegean rather than the sun disappearing behind the cliff — the best sunset in Greece, in my opinion.",
        ],
        stood_out=[
            ("The two-bedroom suites are the star.", "Separated by floor, with large pools, decks, and outdoor dining areas. Some rooms sit below the pool with views looking up into the water."),
            ("The best sunset in Greece.", "A real sunset into the open Aegean — something the Caldera hotels physically cannot offer."),
            ("Omnia was the best hotel restaurant I ate at across the entire trip.", "Poolside above Ammoudi Bay, and worth booking even if you stay elsewhere."),
            ("The gardens change the whole mood.", "Volcanic-rock walls and serious landscaping turn the common areas into a private world minutes from Oia's crowds."),
        ],
        know=[
            ("It's not on the Caldera.", "First-time visitors picturing the classic cliffside image are choosing a different experience here. If that image is non-negotiable, book <a href=\"canaves-oia-suites-santorini.html\">Canaves Oia Suites</a> instead."),
            ("Full-property buyouts are available.", "With no age restrictions once the contract is signed. For a dedicated villa buyout, though, see <a href=\"canaves-sunday-santorini.html\">Canaves Sunday</a> — my pick for the best villa in Santorini."),
            ("You still get the Canaves ecosystem.", "Easy shuttle access connects you to the other Canaves properties and their restaurants and spas."),
            ("Planning a wedding or full buyout?", "Epitome's buyouts, room blocks, and guest logistics are exactly what I do — start with my <a href=\"../santorini-weddings.html\">Santorini weddings page</a>."),
        ],
        verdict="If you're asking me for the single best hotel I experienced across the Greek islands on this trip — it's Canaves Epitome.",
    ),
    dict(
        slug="gundari-folegandros", name="Gundari", short_name="Gundari",
        island="Folegandros", island_page="folegandros.html", rank_num="02",
        hero_img="gundari-1.jpg", img2="gundari-2.jpg",
        stat2_num="27", stat2_label="Suites &amp; Villas, All With Plunge Pools",
        meta_desc="Keith's firsthand review of Gundari on Folegandros — a dark stone clifftop resort with the coolest infinity pool in the Cyclades.",
        tagline="A dark stone lodge on the cliff's edge of Folegandros — unlike anything I've ever seen.",
        style_label="Design-led clifftop resort", perfect_for="Honeymoons, anniversaries, remote luxury",
        credit_label="hotel credit", partner_clause="", visited_verb="visited",
        intro=[
            "You get picked up at the port — or helicopter charter directly in — and after a short five-minute drive, you hit a dirt road for the next eight to ten minutes out toward the cliff's edge. In the distance, a beautiful dark stone building blends into the horizon. It's unlike anything I've ever seen.",
            "Gundari has 27 suites and villas, all with endless ocean views and private plunge pools. Some are cave-style and more private, but because the property is so remote, there's no one wandering past your room anyway. Every little design detail was clearly thought through, down to the outdoor shower overlooking the Aegean.",
            "Because you can't fly to Folegandros and it sits on a somewhat obscure ferry line, the people who make it here really want to be here. Nearly every guest I met was a honeymooner — quiet, like-minded, and laid back. The island filters its own crowd.",
        ],
        stood_out=[
            ("The coolest infinity pool in the Cyclades.", "Without a doubt — cantilevered toward open sea, with nothing between you and the horizon."),
            ("The spa and gym punch far above the room count.", "Both were fantastic — rare for a property this remote."),
            ("The outdoor shower overlooking the Aegean.", "A small thing that captures how deliberately this place was designed."),
            ("A team that listens.", "When my clients flag anything at all, the team responds with genuine gratitude and speed — the kind of ownership mentality you hope for at this level."),
        ],
        know=[
            ("Give it three nights.", "Gundari and Folegandros really need three. If it's booked and you can only do two, I'd still go."),
            ("It pairs perfectly with Santorini.", "Folegandros is right next door, making Gundari an easy add-on for a honeymoon or anniversary trip."),
            ("Getting there takes intent.", "Ferry via a less-frequent line, or helicopter charter direct to the property — plan the crossing before you fall in love with the dates."),
        ],
        verdict="Folegandros is a fantastic island, and Gundari makes it even more special. Wow.",
    ),
    dict(
        slug="canaves-oia-suites-santorini", name="Canaves Oia Suites", short_name="Canaves Oia Suites",
        island="Santorini", island_page="santorini.html", rank_num="03",
        hero_img="canaves-oia-1.jpg", img2="canaves-oia-2.jpg",
        stat2_num="46", stat2_label="Suites &amp; Villas On The Caldera",
        meta_desc="Keith's firsthand review of Canaves Oia Suites — the classic Santorini caldera experience perfected, with the best spa on the Caldera.",
        tagline="The classic Santorini caldera experience, perfected — the best hotel I saw for first-time visitors.",
        style_label="Caldera luxury hotel", perfect_for="First-timers, honeymooners, 40+ couples",
        credit_label="&euro;100 hotel credit", partner_clause=" with a preferred partnership at Canaves", visited_verb="toured every corner of",
        intro=[
            "This was the best hotel I saw for first-time visitors to Santorini, and I'd be hard pressed to recommend any other hotel first if someone specifically wants the classic caldera-luxury experience.",
            "Recently completely renovated, it blew me away everywhere I looked: the quality of the finishes, the privacy — a genuine rarity on Santorini — the private water features, and the landscaping. It sits higher on the Caldera than most, which means more privacy, and every room has coverings above its outdoor spaces.",
            "There are 46 total suites and villas, including private two- and three-bedroom pool villas — something you almost never find in Oia or Imerovigli. Note the 13+ age requirement; families should look at sister property <a href=\"canaves-epitome-santorini.html\">Canaves Epitome</a> instead.",
        ],
        stood_out=[
            ("The River Pool Suite is the single best suite I saw in Greece.", "Across all 38 hotels on this trip. If it's available for your dates, stop deliberating."),
            ("The best spa product on the Caldera.", "Completely brand new, plus a large gym — neither is a given at caldera hotels."),
            ("Privacy engineered into the site.", "Set higher on the Caldera than most, with coverings above every room's outdoor space."),
            ("Private multi-bedroom villas.", "Two- and three-bedroom pool villas are nearly nonexistent in Oia — Canaves has them."),
        ],
        know=[
            ("There's a 13+ age requirement.", "Traveling with younger kids? <a href=\"canaves-epitome-santorini.html\">Epitome</a>, a short walk away, has no age restrictions."),
            ("Complete privacy doesn't exist on the Caldera.", "Anywhere. Canaves does a particularly good job with it, but set expectations accordingly."),
            ("Compare the top tier before booking.", "For honeymoons, weigh this against Andronis Boutique, Andronis Luxury Suites, and Canaves Ena — my <a href=\"../santorini-hotels-ranked.html\">Santorini ranking</a> breaks down all of them."),
        ],
        verdict="For first-timers, honeymooners, and 40+ couples who want the classic Santorini experience, this is the one.",
    ),
    dict(
        slug="parilio-paros", name="Parilio", short_name="Parilio",
        island="Paros", island_page="paros.html", rank_num="04",
        hero_img="parilio-1.jpg", img2="parilio-2.jpg",
        stat2_num="13", stat2_label="Villas &amp; Suites In The New Hilltop Collection",
        meta_desc="Keith's firsthand review of Parilio on Paros — the most beautiful design story in the Cyclades, with new hilltop villas and Sun Suites.",
        tagline="The most beautiful design story in the Cyclades, set in the golden light just outside Naoussa.",
        style_label="Design hotel &amp; villas", perfect_for="Design lovers, couples, families &amp; groups",
        credit_label="hotel credit", partner_clause="", visited_verb="stayed at",
        intro=[
            "As a design lover, Parilio was perhaps my favorite stay in the Cyclades. It's set just outside Naoussa, and while most rooms don't have ocean views, it genuinely doesn't matter — the property itself is so beautiful, and the way the light moves through it around twilight is magical.",
            "What I loved most, though, was the service: the staff actually cared to get to know you and your preferences by name. The food was fantastic, the massage was great, and the gym had everything you'd need with room to spare.",
            "As a bonus, Parilio guests can use the beach club at sister property <a href=\"cosme-paros.html\">Cosme</a> for free — which effectively gives you two of the best properties on Paros for the price of one.",
        ],
        stood_out=[
            ("Request the Sun Suite up at the villas.", "One of the three Sun Suites sits at the new hilltop villas, with ocean views and a massive private pool. Ask for that specific one when booking."),
            ("The new villas are a sneaky value.", "Three-bedroom villas run around $3,000&ndash;$3,500 per night in peak season — brand new, with full access to the hotel's amenities. For a group or family, that's genuinely reasonable at this level."),
            ("Twilight at the pool.", "The property's geometry and light around sunset are the most photographed thing on Paros for a reason."),
            ("Free access to Cosme's beach club.", "A short hop away, directly on the water in front of Cosme."),
        ],
        know=[
            ("Most rooms don't have ocean views.", "If waking up to water is the priority, look at <a href=\"cosme-paros.html\">Cosme</a> — or take the hilltop villas here."),
            ("July brings families to the pool.", "It was tranquil during my stay, but peak-summer guests told me to expect kids. That's Paros in July."),
            ("Torn between Parilio and Cosme?", "I wrote a full <a href=\"../cosme-vs-parilio-paros.html\">head-to-head comparison</a> after staying at both."),
        ],
        verdict="I'm very pro private-villas-at-hotels these days versus standalone villas — and Parilio's are the best case for it.",
    ),
    dict(
        slug="andronis-boutique-santorini", name="Andronis Boutique Hotel", short_name="Andronis Boutique",
        island="Santorini", island_page="santorini.html", rank_num="05",
        hero_img="andronis-boutique-1.jpg", img2="andronis-boutique-2.jpg",
        stat2_num="25", stat2_label="Suites &amp; Villas In Oia",
        meta_desc="Keith's firsthand review of Andronis Boutique Hotel — authentic renovated cave-style suites in Oia, every room with a plunge pool or jacuzzi.",
        tagline="Authentic cave-style luxury in the heart of Oia — the rooms first-time Santorini visitors are dreaming about.",
        style_label="Cave-style boutique", perfect_for="Younger honeymooners, first-timers",
        credit_label="&euro;100 hotel credit", partner_clause=" with a preferred partnership at Andronis", visited_verb="toured every corner of",
        intro=[
            "Andronis Boutique is a truly fantastic, top-notch hotel — firmly in the very top tier of my Santorini list. Recently renovated, the rooms are authentic cave-style rooms with beautiful finishes and fixtures, and they're what people actually picture when they book Santorini.",
            "Some of the suites are incredibly unique, particularly the two-level Eternal Suite, and every room has a plunge pool or jacuzzi — which isn't the case at the Canaves hotels. Rates also tend to land slightly below sister property Andronis Luxury Suites, which skews a little older; Boutique lends itself to younger honeymooners.",
            "Book dinner at Lycabettus — Andronis' famous cliffside restaurant — the moment you confirm your room. It fills faster than the hotels do.",
        ],
        stood_out=[
            ("Real cave-style rooms, beautifully renovated.", "Marble, wooden arches, and surprisingly bright interiors for cave architecture."),
            ("The two-level Eternal Suite.", "One of the most unique suites on the island."),
            ("A water feature in every room.", "Plunge pool or jacuzzi, no exceptions — not something the Canaves properties can say."),
            ("Priced below its flagship sibling.", "You give up very little versus Andronis Luxury Suites and usually pay less."),
        ],
        know=[
            ("The \"stay in Imerovigli to avoid crowds\" narrative doesn't hold here.", "At the top Oia properties, no one is walking directly in front of your room — while several Imerovigli hotels sit right on the Fira-to-Oia hiking path. If privacy matters, say so when booking."),
            ("Spa devotees should also look at Andronis Concept.", "Its spa near Imerovigli was one of my top five in the Cyclades."),
            ("Compare the whole top tier.", "Boutique, Luxury Suites, Canaves Ena, and Canaves Oia Suites — judged on the actual room, privacy, water feature, and price. My <a href=\"../santorini-hotels-ranked.html\">Santorini ranking</a> compares them all."),
        ],
        verdict="Between the top Oia properties you really can't go wrong — but Boutique's cave-style rooms are the real thing.",
    ),
    dict(
        slug="bill-and-coo-coast-mykonos", name="Bill &amp; Coo Coast", short_name="Bill &amp; Coo Coast",
        island="Mykonos", island_page="mykonos.html", rank_num="06",
        hero_img="billandcoo-coast-1.jpg", img2="billandcoo-coast-2.jpg",
        stat2_num="A+", stat2_label="Best Breakfasts I Had In Greece",
        meta_desc="Keith's firsthand review of Bill & Coo Coast — adults-only oceanfront suites on a protected Mykonos bay, with the best breakfasts in Greece.",
        tagline="Adults-only suites directly on a protected bay — the Bill &amp; Coo location I'd always choose.",
        style_label="Adults-only beachfront", perfect_for="Couples, beach club lovers",
        credit_label="hotel credit", partner_clause="", visited_verb="stayed with",
        intro=[
            "I stayed at Bill &amp; Coo's Mykonos Town property, but I preferred the Coast location for a few reasons: it's adults-only, it has a beautiful private beach club, rooms sit directly on the ocean, and the suites are massive and incredibly private — some with truly spectacular private pools.",
            "The Coast location also sits in a protected bay, so the meltemi winds that can whip the Town property's infinity pool are far more minimal here. In August, that difference is not academic.",
            "Like Cali and Kalesma, Bill &amp; Coo is independently owned, and many staff members have been there for multiple seasons. To me, that's one of the most reliable signs that things are working well behind the scenes.",
        ],
        stood_out=[
            ("The best breakfasts I had in Greece.", "At any hotel, on any island. I was usually full until dinner."),
            ("The private beach club.", "Extremely relaxing — and lunch at Beefbar on-site is fun, if a bit sceney."),
            ("Massive, genuinely private suites.", "Rooms directly on the water, several with remarkable private pools."),
            ("A big upgrade is coming.", "A massive new gym complex and spa are under construction, which should take the property to another level."),
        ],
        know=[
            ("Book Coast, not Town.", "If you have the choice, the protected bay, adults-only policy, and beachfront rooms make Coast the clear pick. The Town location's infinity pool gets windy in the meltemi."),
            ("It's adults-only &mdash; guests 17 and up.", "Traveling with kids on Mykonos? Look at <a href=\"cali-mykonos.html\">Cali</a> on the quieter east side."),
            ("The scene is there if you want it.", "Beefbar brings energy at lunch, and the hotel arranges transfers to the island's beach clubs — but the property itself stays calm."),
        ],
        verdict="If I had the choice, I'd always choose the Coast location over the Mykonos Town property.",
    ),
    dict(
        slug="kalesma-mykonos", name="Kalesma", short_name="Kalesma",
        island="Mykonos", island_page="mykonos.html", rank_num="07",
        hero_img="kalesma-1.jpg", img2="kalesma-2.jpg",
        stat2_num="Ornos", stat2_label="Set Above Ornos Bay, Very Central",
        meta_desc="Keith's firsthand review of Kalesma Mykonos — Cycladic minimalism in dark wood and marble above Ornos Bay, built for couples.",
        tagline="Cycladic minimalism in dark wood and marble, perched above Ornos Bay.",
        style_label="Design boutique", perfect_for="Couples, sunset lovers, slow evenings",
        credit_label="hotel credit", partner_clause="", visited_verb="stayed at",
        intro=[
            "Wow, Kalesma is such a beautiful property. The combination of Cycladic minimalism with dark woods and marble just works incredibly well, and the location is fantastic — set above Ornos Bay and very central on Mykonos.",
            "It's very much a couples-oriented property. Children are technically allowed, but I didn't see any during my two nights. Kalesma also recently completed an expansion — new suites, a second pool, and an additional restaurant — and I stayed in one of the junior suites at the new pool. This is a hotel built for slow evenings: I loved sitting in my jacuzzi with a glass of wine overlooking the bay so much that one night I skipped going out entirely and had dinner on my own patio.",
            "Cali had a somewhat more American, almost LA-like feel — Kalesma feels more laid back, and for some reason I still preferred it overall despite Cali's superior facilities.",
        ],
        stood_out=[
            ("The fire pit overlooking Delos.", "A fantastic place to sit around sunset before heading out to dinner."),
            ("The jacuzzi suites.", "A glass of wine, the bay below, golden hour — the memory that outlasted the trip."),
            ("The design language.", "Dark wood and marble against Cycladic white — restrained, warm, and unlike anything else on the island."),
            ("The location.", "Above Ornos, central to everything, without any of the Mykonos Town chaos."),
        ],
        know=[
            ("Request the junior suites left of the pool bar.", "They're more private than the one I stayed in — and interestingly, the base rooms above the junior suites are more private still."),
            ("Wellness is intimate, not the headline.", "The spa is small and the gym covers the basics — if a serious gym matters, that's <a href=\"cali-mykonos.html\">Cali</a>."),
            ("Dining is pleasant rather than the headline.", "Kalesma is about the design and the views — and Mykonos's remarkable restaurant scene is minutes away."),
        ],
        verdict="Cali is flashier on paper, but Kalesma's laid-back beauty is what won me over.",
    ),
    dict(
        slug="cali-mykonos", name="Cali", short_name="Cali",
        island="Mykonos", island_page="mykonos.html", rank_num="08",
        hero_img="cali-mykonos-1.jpg", img2="cali-mykonos-1.jpg",
        stat2_num="75lb", stat2_label="Dumbbells &mdash; Best Hotel Gym I've Seen",
        meta_desc="Keith's firsthand review of Cali Mykonos — an independent resort on the island's quiet east side with the best hotel gym he's ever seen.",
        tagline="An independent stunner on Mykonos's quiet east side — with the best hotel gym I've ever seen.",
        style_label="Independent luxury resort", perfect_for="Fitness-minded travelers, privacy seekers",
        credit_label="hotel credit", partner_clause="", visited_verb="visited",
        intro=[
            "I really loved Cali and think it's such a unique offering on Mykonos. Located on the island's quieter eastern side, it's another of Greece's incredible independent hotels with a strong sense of place — something I often find lacking at the big luxury brands.",
            "Service was extremely refined, with staff calling guests by name and anticipating needs. The infinity pool is one of the largest and most unique I saw in Greece, with real space between loungers — a small detail that changes the whole day.",
            "Many rooms have private plunge pools, and I found them to be very, very private — which is generally a rarity in Greece.",
        ],
        stood_out=[
            ("The gym is genuinely remarkable.", "Pilates reformers, squat racks, dumbbells up to 75 pounds, plus padel, tennis, and pickleball. I'd stay here again just for the gym."),
            ("The infinity pool.", "One of the largest and most distinctive in Greece, with generous spacing between loungers."),
            ("Truly private plunge pools.", "Many rooms have them, and unlike most of Greece, they actually feel private."),
            ("Refined, personal service.", "Staff greeted guests by name and anticipated needs — big-brand polish with independent-hotel soul."),
        ],
        know=[
            ("It's far from the party scene — by design.", "The hotel arranges boat or car transfers to the beach clubs and nightclubs if that's what you're after."),
            ("The vibe is a little LA.", "A somewhat American feel compared to Kalesma's laid-back Cycladic mood — pick your flavor of Mykonos."),
            ("Mykonos is a smart entry point.", "Easy to reach from Europe and the Middle East: fly in, move south through the Cyclades, and save Athens for a separate trip."),
        ],
        verdict="A genuinely remarkable property I'd happily return to — and I'd stay again just for that gym.",
    ),
    dict(
        slug="cosme-paros", name="Cosme", short_name="Cosme",
        island="Paros", island_page="paros.html", rank_num="09",
        hero_img="cosme-1.jpg", img2="cosme-2.jpg",
        stat2_num="XL", stat2_label="Base Rooms Bigger Than Most Junior Suites",
        meta_desc="Keith's firsthand review of Cosme on Paros — laid-back beachfront luxury steps from Naoussa, with a private beach club out front.",
        tagline="Laid-back beachfront luxury steps from Naoussa, with a private beach club out front.",
        style_label="Beachfront resort", perfect_for="Couples, families with teens, 4-night stays",
        credit_label="hotel credit", partner_clause="", visited_verb="stayed at",
        intro=[
            "I loved Cosme. The laid-back luxury beach vibe is really refreshing, and while the room rates are high, the base rooms are massive — larger than many hotels' junior suites.",
            "The service was refined, the dining was fantastic, and the location is hard to beat on Paros: walking distance to Naoussa, with a private beach club directly in front of the hotel.",
            "And despite what you may have heard, Paros is not \"the new Mykonos.\" Naoussa is lively and fun without the flashy scene. It's honestly just a really easy, nicely rounded Greek island — which is exactly what Cosme delivers as a hotel.",
        ],
        stood_out=[
            ("The base rooms are enormous.", "Bigger than many hotels' junior suites — the rare entry category I'd happily book."),
            ("The circular spa and gym buildings.", "Genuinely unique architecture, and both deliver."),
            ("The private beach club.", "Directly in front of the hotel — no shuttles, no reservations battle."),
            ("Enough to fill four nights.", "Between the beach club, spa, and dining, you could stay four nights without getting bored — rare on the islands."),
        ],
        know=[
            ("Skip the plunge-pool rooms overlooking the shared pool.", "The top categories have ocean-view plunge pools, but they overlook the main infinity pool and aren't particularly private. I'd opt for a suite set farther back."),
            ("Shoulder season is the play.", "In May or September/October, rates can drop dramatically from peak summer pricing."),
            ("Torn between Cosme and Parilio?", "I stayed at both and wrote a full <a href=\"../cosme-vs-parilio-paros.html\">head-to-head comparison</a> — and remember, Parilio guests share this beach club."),
        ],
        verdict="Paros is just a really easy, nicely rounded island — and Cosme is its best beach stay.",
    ),
    dict(
        slug="stamna-sifnos", name="Stamna", short_name="Stamna",
        island="Sifnos", island_page="sifnos.html", rank_num="10",
        hero_img="stamna-1.jpg", img2="stamna-2.jpg",
        stat2_num="$25", stat2_label="Per-Bag Laundry &mdash; A Quiet Hero",
        meta_desc="Keith's firsthand review of Stamna on Sifnos — a small, design-forward hotel above Apollonia on Greece's great foodie island.",
        tagline="A small, design-forward perch above Apollonia, on one of Greece's great foodie islands.",
        style_label="Design boutique", perfect_for="Slow travelers, foodies, design-conscious couples",
        credit_label="hotel credit", partner_clause="", visited_verb="stayed at",
        intro=[
            "After ten nights between Mykonos and Paros, arriving at Stamna after a somewhat brutal ferry ride was a fantastic respite. Set above some of Sifnos's best beaches and centrally located in Apollonia, it's a small, design-forward hotel with excellent dining on what's known as one of Greece's great foodie islands.",
            "The design is earthy, neutral, and calming, with a wonderful feeling of being perched above the Cyclades — views stretching as far as you can see. Service was warm and casual but still solid.",
            "Sifnos itself is one of my favorite Greek islands for slow travel: hiking, food, and a rugged mountainous landscape. Stamna is the pick if you want a smaller, design-conscious hotel rather than a traditional large luxury resort.",
        ],
        stood_out=[
            ("The dining.", "Excellent — on an island famous for its food, the hotel restaurant holds its own."),
            ("The perch.", "Views over the Cyclades stretching as far as you can see, from a calm hillside above Apollonia."),
            ("The design.", "Earthy, neutral, and calming — a hotel that knows exactly what it is."),
            ("The $25-per-bag laundry service.", "You can fit a surprising amount in one bag — a lifesaver on a multi-week island trip with only a carry-on."),
        ],
        know=[
            ("There's no spa or gym that I could find.", "If wellness facilities matter, this isn't the island stop for them."),
            ("The pool draws a mixed crowd.", "Young families and honeymooners share it, so it isn't always as relaxing as the setting suggests."),
            ("Sifnos rewards slow travel.", "Budget real time for the hiking trails, the villages, and the tavernas — this isn't a see-it-in-a-day island."),
        ],
        verdict="After ten nights between Mykonos and Paros, arriving at Stamna was a fantastic respite — exactly what you want Sifnos to be.",
    ),
    dict(
        slug="andronis-luxury-suites-santorini", name="Andronis Luxury Suites", short_name="Andronis Luxury Suites",
        island="Santorini", island_page="santorini.html",
        stat1_num="#04", stat1_label="In My Santorini Ranking",
        rank_href="santorini-hotels-ranked.html", rank_text="#04 in my Santorini ranking",
        related_text="See The Full Santorini Ranking", cta2_text="The Santorini Ranking",
        hero_img="grace-1.jpg", img2="grace-1.jpg",
        stat2_num="39", stat2_label="Suites &amp; Villas, All With Water Features",
        meta_desc="Keith's firsthand review of Andronis Luxury Suites — the refined flagship of the Andronis portfolio on the Oia caldera, home of Lycabettus.",
        tagline="The refined flagship of the Andronis portfolio — elegant, exclusive, and home to the island's most famous cliffside restaurant.",
        style_label="Flagship luxury suites", perfect_for="40+ couples, anniversaries, mobility-conscious travelers",
        credit_label="&euro;100 hotel credit", partner_clause=" with a preferred partnership at Andronis", visited_verb="toured every corner of",
        intro=[
            "The flagship of the Andronis portfolio is equally as beautiful as its younger sibling, <a href=\"andronis-boutique-santorini.html\">Andronis Boutique</a> — more exclusive on paper, refined, and elegant. If I'm honest, it felt a bit more old-school luxury than authentically Santorini, which is exactly why it works so well for a certain kind of trip.",
            "There are 39 suites and villas, all spacious, and every single room has a water feature — a plunge pool, a jacuzzi, or a full pool in the villas. The Mare Sanus Spa handles wellness, Miltos' Greek Table covers casual Greek dining, and select suites even come with complimentary use of a MINI Cooper Cabrio.",
            "And then there's Lycabettus — Andronis' famous cliffside restaurant, hailed by National Geographic for its location. It lives here, and it books out before the rooms do. Reserve your table the moment you confirm your stay.",
        ],
        stood_out=[
            ("Home of Lycabettus.", "The island's most famous cliffside table. Book it the same day you book the room — it fills faster than the hotel does."),
            ("Every room has a water feature.", "Plunge pool, jacuzzi, or a full pool in the villas — no exceptions across all 39 keys."),
            ("The best of the portfolio for mobility concerns.", "A few suites near check-in have only 15&ndash;20 stairs — no trekking hundreds of caldera steps to reach your room."),
            ("A MINI Cooper with select suites.", "Complimentary MINI Cooper Cabrio use comes with the top categories — a genuinely useful perk on Santorini."),
        ],
        know=[
            ("It reads old-school luxury, not cave-style Santorini.", "Refined and elegant rather than authentically Cycladic. If cave rooms are what you're picturing, that's <a href=\"andronis-boutique-santorini.html\">Boutique</a>."),
            ("Rates sit slightly above Andronis Boutique.", "And Boutique gives up very little — compare both in my <a href=\"../santorini-hotels-ranked.html\">Santorini ranking</a> before deciding."),
            ("The portfolio's best spa isn't here.", "Mare Sanus is good, but wellness devotees should look at <a href=\"andronis-concept-santorini.html\">Andronis Concept</a> — one of my top five spas in the Cyclades."),
        ],
        verdict="It lends itself perfectly to a 50+ clientele on anniversary trips — or returning to Santorini for the first time since their honeymoon. Also my pick when mobility is a factor.",
    ),
    dict(
        slug="andronis-concept-santorini", name="Andronis Concept", short_name="Andronis Concept",
        island="Santorini", island_page="santorini.html",
        stat1_num="#06", stat1_label="In My Santorini Ranking",
        rank_href="santorini-hotels-ranked.html", rank_text="#06 in my Santorini ranking",
        related_text="See The Full Santorini Ranking", cta2_text="The Santorini Ranking",
        hero_img="andronis-concept-1.jpg", img2="andronis-concept-1.jpg",
        stat2_num="28", stat2_label="Suites &amp; Villas, Each With Infinity Pool",
        meta_desc="Keith's firsthand review of Andronis Concept — the nicest spa he saw on Santorini, in warm earthy architecture near Imerovigli.",
        tagline="The nicest spa I saw on Santorini — maybe in the Cyclades — wrapped in warm, earthy architecture near Imerovigli.",
        style_label="Wellness resort", perfect_for="Wellness travelers, design lovers, 4+ night stays",
        credit_label="&euro;100 hotel credit", partner_clause=" with a preferred partnership at Andronis", visited_verb="toured every corner of",
        intro=[
            "Set near, but not in, Imerovigli, Concept is genuinely different from the rest of the Andronis portfolio — and from most of this island. The architecture breaks from the traditional white cave look with warm, earthy modern tones that blend into the volcanic landscape.",
            "The Kallos Spa is the nicest spa I saw on Santorini, and maybe in the Cyclades. Pair it with just 28 newly renovated suites and villas — each with a private terrace and infinity pool facing the caldera sunset — and Throubi, the on-site restaurant serving indigenous Greek delicacies, and you have a genuine wellness sanctuary rather than a hotel with a spa menu.",
            "Rooms are generous and feel very private. If this property were located in Oia instead, it'd probably be competing for one of my top three spots on the island.",
        ],
        stood_out=[
            ("Kallos Spa.", "The best spa product I saw on Santorini — possibly the Cyclades. Worth planning a slow-travel stay around."),
            ("Every suite has a private terrace and infinity pool.", "All 28 keys, all facing the caldera sunset."),
            ("Architecture that breaks the mold.", "Warm, earthy, modern tones that blend into the volcanic landscape instead of the standard white-cave look."),
            ("Built for longer stays.", "This is a four-plus-night property — the wellness programming and quiet setting reward guests who settle in."),
        ],
        know=[
            ("Some rooms sit directly on the Fira-to-Oia walking path.", "Not all, but a few have the hiking trail passing right in front — worth checking before booking, and worth telling me if privacy matters to you."),
            ("Family-friendly, but families are steered elsewhere.", "Andronis points families toward <a href=\"andronis-arcadia-santorini.html\">Arcadia</a>, whose resort setup fits them better."),
            ("It's near Imerovigli, not in it.", "You'll taxi or drive to dinner in Oia and Imerovigli proper — a fair trade for the quiet."),
        ],
        verdict="If this property were located in Oia instead, it'd probably be competing for one of my top three spots on the island.",
    ),
    dict(
        slug="andronis-arcadia-santorini", name="Andronis Arcadia", short_name="Andronis Arcadia",
        island="Santorini", island_page="santorini.html",
        stat1_num="#08", stat1_label="In My Santorini Ranking",
        rank_href="santorini-hotels-ranked.html", rank_text="#08 in my Santorini ranking",
        related_text="See The Full Santorini Ranking", cta2_text="The Santorini Ranking",
        hero_img="andronis-arcadia-1.jpg", img2="andronis-arcadia-1.jpg",
        stat2_num="114", stat2_label="Suites &amp; Villas, All With Private Pools",
        meta_desc="Keith's firsthand review of Andronis Arcadia — a true resort next to Canaves Epitome with sunset-facing rooms, huge private pools, and a bit of a scene.",
        tagline="A true resort next door to Canaves Epitome — sunset-facing rooms, some of the island's largest private pools, and a bit of a scene.",
        style_label="Full resort", perfect_for="Families, younger couples, scene-seekers",
        credit_label="&euro;100 hotel credit", partner_clause=" with a preferred partnership at Andronis", visited_verb="toured every corner of",
        intro=[
            "With 114 suites and villas, Arcadia reads as a true resort rather than a boutique hotel — the only property in the Andronis portfolio you could say that about. It sits just outside Oia proper, right next door to <a href=\"canaves-epitome-santorini.html\">Canaves Epitome</a>, with beautiful sunset-facing rooms and very private layouts.",
            "Every room has a private pool, including some of the largest on the island, and the family infrastructure is real: the ARCADemy kids club and the Evexia Spa give parents and kids somewhere to be at the same time.",
            "Then there's the scene. Pacman — with live music — and Beefbar Santorini are both on property, two very Mykonos-esque dining options that bring in a different vibe and clientele than the rest of the Andronis and Canaves portfolios. Great if you like that energy; something to know if you don't.",
        ],
        stood_out=[
            ("Every room has a private pool.", "Including some of the largest private pools on Santorini."),
            ("Real family infrastructure.", "The ARCADemy kids club plus resort-scale grounds make this the Andronis choice for families — and they'll tell you the same."),
            ("Sunset-facing, very private layouts.", "The same golden-hour orientation that makes neighboring Epitome special."),
            ("Pacman and Beefbar on property.", "Live music, scene energy, and two of the buzziest tables outside Oia's center."),
        ],
        know=[
            ("It's massive and spread out.", "You'll want a golf cart to get around in summer heat if there's no meltemi wind blowing."),
            ("The vibe is a choice.", "The Mykonos-esque dining scene draws a different clientele than the rest of this list — if you want exclusivity and quiet, book <a href=\"canaves-epitome-santorini.html\">Epitome</a> next door instead."),
            ("Resort scale means resort rhythm.", "This is the right Santorini hotel for travelers who want activity and options, not seclusion."),
            ("Planning a wedding here?", "Arcadia's scale makes it Santorini's best room-block hotel — weddings are exactly what I do, starting with my <a href=\"../santorini-weddings.html\">Santorini weddings page</a>."),
        ],
        verdict="Great if you like a bit of a scene; not the move if you want exclusivity and quiet.",
    ),
    dict(
        slug="canaves-ena-santorini", name="Canaves Ena", short_name="Canaves Ena",
        island="Santorini", island_page="santorini.html",
        stat1_num="#05", stat1_label="In My Santorini Ranking",
        rank_href="santorini-hotels-ranked.html", rank_text="#05 in my Santorini ranking",
        related_text="See The Full Santorini Ranking", cta2_text="The Santorini Ranking",
        hero_img="canaves-ena-1.jpg", img2="canaves-ena-1.jpg",
        stat2_num="18", stat2_label="Suites In 17th-Century Wine Caves",
        meta_desc="Keith's firsthand review of Canaves Ena — the original Canaves property, 18 intimate suites carved from 17th-century wine caves, renovated in 2024.",
        tagline="The OG of the Canaves portfolio — 18 intimate suites carved from 17th-century wine caves, freshly renovated.",
        style_label="Intimate caldera boutique", perfect_for="Value seekers, social travelers",
        credit_label="&euro;100 hotel credit", partner_clause=" with a preferred partnership at Canaves", visited_verb="toured every corner of",
        intro=[
            "Ena is where the Canaves story started — opened in the 80s by the same family that runs the portfolio today, in suites that trace back to 17th-century wine caves. It's a little more minimalist than its younger siblings, and a 2024 renovation brought it up to date beautifully.",
            "With just 18 suites, it feels genuinely intimate. Like <a href=\"canaves-oia-suites-santorini.html\">Canaves Oia Suites</a>, it sits higher on the Caldera, which means more privacy than most Caldera offerings — and the swim-up pool bar is a highlight, a fun social addition on an island where couples tend to keep to themselves. Adami, the restaurant alongside the main pool, handles authentic Greek gastronomy.",
            "Know the trade-offs: rooms run slightly smaller than Oia Suites, and not every room has a water feature the way the Andronis properties guarantee.",
        ],
        stood_out=[
            ("The swim-up bar.", "A fun, social addition on an island where most hotels are couples quietly keeping to themselves."),
            ("The heritage.", "17th-century wine caves, one family since the 80s — the most personal story on the Caldera."),
            ("Higher on the Caldera.", "Like Oia Suites, that elevation buys real privacy compared to most Caldera hotels."),
            ("The 2024 renovation.", "Minimalist but current — the update brought Ena fully up to the portfolio's standard."),
        ],
        know=[
            ("Not every room has a water feature.", "Unlike the Andronis properties — check your category if a plunge pool or jacuzzi matters."),
            ("Rooms are slightly smaller than Oia Suites.", "The intimacy is the point, but square footage isn't the selling feature here."),
            ("The value positioning doesn't always show up in the rate.", "It's framed as the accessible Canaves, but pricing almost always lands right where Andronis Boutique does — compare in my <a href=\"../santorini-hotels-ranked.html\">Santorini ranking</a>."),
        ],
        verdict="The team here — especially longtime sales director Des — is a big reason I trust sending clients to this property.",
    ),
    dict(
        slug="canaves-sunday-santorini", name="Canaves Sunday", short_name="Canaves Sunday",
        island="Santorini", island_page="santorini.html",
        stat1_num="8", stat1_label="Standalone Suites In The Heart Of Oia",
        rank_href="santorini-hotels-ranked.html", rank_text="The Canaves portfolio, ranked",
        related_text="See The Full Santorini Ranking", cta2_text="The Santorini Ranking",
        hero_img="canaves-sunday-1.jpg", img2="canaves-sunday-2.jpg",
        stat2_num="18", stat2_label="Bedrooms As A Full-Property Buyout",
        meta_desc="Keith's firsthand review of Canaves Sunday — a ten-bedroom villa plus eight standalone suites in the heart of Oia, an eighteen-bedroom buyout taken whole.",
        tagline="The Canaves you book when you want the whole thing to yourselves — a ten-bedroom villa plus eight standalone suites in the heart of Oia.",
        style_label="Relaxed boutique &amp; full buyout", perfect_for="Groups, celebrations, budget-conscious Canaves fans",
        credit_label="&euro;100 hotel credit", partner_clause=" with a preferred partnership at Canaves", visited_verb="toured every corner of",
        intro=[
            "Sunday is the entry point to the Canaves portfolio and the most relaxed of the collection in style — a ten-bedroom villa plus eight standalone suites set in the very heart of Oia's traditional town, with an exceptional three-to-one staff-to-guest ratio.",
            "The setup is simple: one master suite has a private pool, and the remaining accommodations share the main pool. Taken suite by suite, it's the most budget-friendly way into Canaves quality and Canaves service.",
            "But the real play is the buyout. Take the villa and all eight standalone units together and you have effectively an eighteen-bedroom private compound — with no age restrictions once the contract is signed — which makes Sunday my pick for the best villa in Santorini for a group of friends, a family milestone, or a celebration that wants Oia outside the front door.",
        ],
        stood_out=[
            ("The full-property buyout.", "The ten-bedroom villa plus all eight standalone suites — effectively eighteen bedrooms in the middle of Oia, and my pick for the best villa in Santorini."),
            ("A 3-to-1 staff-to-guest ratio.", "Villa privacy with hotel staffing is the combination standalone rentals can't match."),
            ("The heart-of-Oia location.", "The town's restaurants, galleries, and blue domes are outside the front door."),
            ("Canaves service at the friendliest rate.", "Suite for suite, the most accessible way into the portfolio."),
        ],
        know=[
            ("Only the master suite has a private pool.", "Everyone else shares the main pool — fine for a buyout group, worth knowing for a couple booking a single suite. Sunday guests can also use the pool at <a href=\"canaves-epitome-santorini.html\">Canaves Epitome</a>, a short shuttle away."),
            ("Age restrictions lift only on a buyout.", "Booked as individual suites, standard Canaves age policies apply; signed as a full-villa contract, kids of any age are welcome."),
            ("Book it as a celebration.", "This property makes the most sense taken whole — honeymoons and couples are better served at <a href=\"canaves-oia-suites-santorini.html\">Oia Suites</a> or <a href=\"canaves-epitome-santorini.html\">Epitome</a>."),
            ("Planning a wedding here?", "Buyouts, room blocks, and guest logistics are exactly what I do — start with my <a href=\"../santorini-weddings.html\">Santorini weddings page</a>."),
        ],
        verdict="For groups or buyouts needing flexibility and privacy, this is my pick for the best villa in Santorini — and the most budget-friendly door into Canaves.",
    ),
    dict(
        slug="grace-santorini", name="Grace Hotel Santorini", short_name="Grace",
        island="Santorini", island_page="santorini.html",
        stat1_num="#07", stat1_label="In My Santorini Ranking",
        rank_href="santorini-hotels-ranked.html", rank_text="#07 in my Santorini ranking",
        related_text="See The Full Santorini Ranking", cta2_text="The Santorini Ranking",
        hero_img="andronis-luxury-1.jpg", img2="andronis-luxury-1.jpg",
        stat2_num="Fog", stat2_label="Line &mdash; Sometimes You're Above It",
        meta_desc="Keith's firsthand review of Grace Hotel Santorini — high on the Imerovigli caldera, beautiful bright rooms, exceptional dining, and the caveats to know before booking.",
        tagline="Set so high on the Imerovigli caldera you're sometimes literally above the fog line — beautiful, with caveats worth knowing.",
        style_label="Caldera boutique", perfect_for="Honeymooners comfortable outside Oia",
        credit_label="&euro;100 hotel credit", partner_clause="", visited_verb="toured every corner of",
        intro=[
            "I wanted to love Grace more than I did. Set way up on the Caldera in Imerovigli, you're sometimes literally above the fog line — a genuinely unique feeling, and ideal for honeymooners okay with being outside Oia.",
            "The room design is simple, white, and elegant, and surprisingly bright for Santorini. The dining is exceptional too: Michelin-starred chef Lefteris Lazarou personally visits tables, and the food felt distinctly Greek yet modern.",
            "So why #07 in my <a href=\"../santorini-hotels-ranked.html\">Santorini ranking</a>? Mostly fit and pricing. Some rooms sit along the Fira-to-Oia walking path, so room selection really matters here — and at current rates, I often find the value equation stronger elsewhere on a very competitive island. When pricing aligns, Grace absolutely belongs in the conversation.",
        ],
        stood_out=[
            ("Above the fog line.", "The Imerovigli elevation gives Grace a caldera perspective no Oia hotel can match — on the right morning it's otherworldly."),
            ("Bright, elegant rooms.", "Simple and white, and surprisingly luminous for a caldera property — many Santorini rooms run dark; these don't."),
            ("Exceptional dining.", "Michelin-starred chef Lefteris Lazarou personally visits tables — distinctly Greek, yet modern."),
            ("A honeymoon feel without Oia's foot traffic.", "For couples happy to trade the Oia postcard for altitude and quiet, the setting delivers."),
        ],
        know=[
            ("Room selection matters here.", "Some rooms sit along the Fira-to-Oia walking path. Book through me and I'll make sure yours is one of the secluded ones."),
            ("Choose the outdoor water features.", "Between Grace's top categories, I'd guide you to the outdoor plunge-pool rooms over the indoor hot tub suites — ask me and I'll explain the trade-offs for your dates."),
            ("Compare before committing.", "At this rate level, it's worth weighing Grace against my top five in the <a href=\"../santorini-hotels-ranked.html\">Santorini ranking</a> — sometimes it wins, and I'll tell you when it does."),
        ],
        verdict="A genuinely beautiful property — at current rates I usually find stronger value elsewhere on the island, but when pricing aligns, Grace absolutely belongs in the conversation.",
    ),
    dict(
        slug="mystique-santorini", name="Mystique", short_name="Mystique",
        island="Santorini", island_page="santorini.html",
        stat1_num="#09", stat1_label="In My Santorini Ranking",
        rank_href="santorini-hotels-ranked.html", rank_text="#09 in my Santorini ranking",
        related_text="See The Full Santorini Ranking", cta2_text="The Santorini Ranking",
        hero_img="katikies-1.jpg", img2="katikies-1.jpg",
        stat2_num="35&ndash;45%", stat2_label="Of Stays Are Bonvoy Redemptions",
        meta_desc="Keith's firsthand review of Mystique Santorini — good bones and a great location, but rooms that need a renovation. Who it still makes sense for.",
        tagline="A storied caldera perch with the Empiria Group behind it &mdash; and my top Marriott Bonvoy play on Santorini while it awaits its next chapter.",
        style_label="Caldera resort (Marriott Luxury Collection)", perfect_for="Marriott Bonvoy redemptions",
        credit_label="hotel credit", partner_clause="", visited_verb="toured every corner of",
        intro=[
            "Mystique didn't connect with me the way the top of my list did — which genuinely surprised me, given how much I love the Empiria Group team behind some of the best hotels in the Cyclades.",
            "The rooms offer limited privacy, and the minimalist interiors read sparse to me — a setting this special deserves finishes to match. The signature earthy cave rooms also run dark and quiet: atmospheric for some travelers, austere for others.",
            "Here's useful context: I was told 35&ndash;45% of stays are Marriott Bonvoy redemptions, which makes this one of the highest-value points plays on the caldera. The bones and the location are genuinely good — with updated interiors, this property competes at the very top of the island.",
        ],
        stood_out=[
            ("The location and the bones.", "The caldera perch is real, and the sculpted architecture photographs beautifully — the raw material for a great hotel is all here."),
            ("The Empiria Group connection.", "The same team runs some of the best hotels in the Cyclades — which is exactly why I believe a renovation would change everything."),
            ("A points sweet spot.", "If you're sitting on Marriott Bonvoy points, this is one of the highest-value caldera redemptions that exists."),
            ("Earth tones instead of white.", "Mystique's warm, sculpted look is a genuine change from Santorini's standard whitewash — when it's lit well, it's special."),
        ],
        know=[
            ("Privacy is limited.", "More so than at the top of my list — room selection and expectations matter here, and I can help with both."),
            ("The cave rooms run dark and quiet.", "Signature Mystique — wonderfully moody for some travelers, spare for others. Ask me about specific categories before booking."),
            ("Paying cash? Let's compare.", "At cash rates, it's worth weighing against my <a href=\"../santorini-hotels-ranked.html\">top five on Santorini</a> — on points, it's hard to beat."),
        ],
        verdict="For now, it's my top Bonvoy-points play on the caldera — for cash stays, I tend to guide clients a notch up my list until the next chapter arrives.",
    ),
    dict(
        slug="katikies-santorini", name="Katikies Santorini", short_name="Katikies",
        island="Santorini", island_page="santorini.html",
        stat1_num="#10", stat1_label="In My Santorini Ranking",
        rank_href="santorini-hotels-ranked.html", rank_text="#10 in my Santorini ranking",
        related_text="See The Full Santorini Ranking", cta2_text="The Santorini Ranking",
        hero_img="mystique-1.jpg", img2="mystique-1.jpg",
        stat2_num="3", stat2_label="Caldera Properties In The Portfolio",
        meta_desc="Keith's firsthand review of the Katikies portfolio on Santorini — an undeniably beautiful setting with dated execution, and what would change his mind.",
        tagline="Three of the most beautiful positions on the caldera &mdash; an icon whose interiors are ready for their next chapter.",
        style_label="Caldera hotel portfolio", perfect_for="Katikies loyalists &mdash; and everyone else after the refresh",
        credit_label="hotel credit", partner_clause="", visited_verb="toured",
        intro=[
            "Katikies holds some of the most storied real estate on Santorini — the setting across all three Caldera properties is undeniably beautiful, the white terraced architecture is what half of the island's postcards are made of, and the spa at Pelagos House is expansive and genuinely impressive.",
            "Where the portfolio trails the top of my list is simple: the interiors haven't kept pace with the island's recent renovation wave — classic rather than current — and unlike Andronis or Canaves, the patios go without coverings, which costs both shade and privacy.",
            "The potential here is enormous. If Katikies follows Andronis and Canaves into continuous renovation, these locations compete with anything on the island — and I'll be first in line to re-review when that happens.",
        ],
        stood_out=[
            ("The setting.", "All three Caldera properties occupy genuinely beautiful positions — this is the terraced white Santorini everyone pictures."),
            ("The spa at Pelagos House.", "Expansive and impressive — the standout facility across the portfolio."),
            ("The photographs.", "The iconic white stairs and infinity pools still deliver the postcard, even where the rooms behind them don't."),
            ("The potential.", "Great bones, unbeatable locations — a renovation would move this portfolio right back up my ranking."),
        ],
        know=[
            ("No coverings over the patios.", "Unlike Andronis or Canaves, which means less shade and much less privacy on your terrace."),
            ("The interiors are classic rather than current.", "A furniture and finishes update would transform the experience — and the rate-to-experience math with it."),
            ("The honest math.", "Right now, $100&ndash;$200 more per night reaches my <a href=\"../santorini-hotels-ranked.html\">top five on Santorini</a> — a comparison worth making for your dates."),
        ],
        verdict="For now, my clients usually find the stronger value a notch up my list — and I'll be first in line to re-review the moment a refresh lands.",
    ),
    dict(
        slug="meadowood-napa-valley", name="Meadowood Napa Valley", short_name="Meadowood",
        island="Wine Country", island_page="napa-sonoma.html", img_dir="napa",
        locale="St. Helena, Napa Valley", region_label="Region",
        region_html="St. Helena, Napa Valley, California",
        stat1_num="#01", stat1_label="In My Napa &amp; Sonoma Ranking",
        rank_href="napa-sonoma.html", rank_text="#01 in my Napa &amp; Sonoma ranking",
        related_text="See The Full Napa &amp; Sonoma Ranking", cta_island_text="The Napa &amp; Sonoma Ranking",
        cta2_href="hotel-guides.html", cta2_text="All Hotel Guides",
        mailto_prep="in",
        hero_img="meadowood-1.jpg", img2="meadowood-2.jpg",
        stat2_num="~40", stat2_label="Cottages &mdash; Not A Bad Room Among Them",
        meta_desc="Keith's firsthand review of Meadowood Napa Valley — the benchmark of wine country after years of repeat stays. Service, cottages, spa, and who it's for.",
        tagline="The benchmark of wine country &mdash; Aman-level service, private cottages, and the property I measure every other Napa stay against.",
        style_label="Estate resort", perfect_for="Honeymoons, celebrations, wine lovers, returning visitors",
        perks_html="Rates through me are identical to booking direct &mdash; the perks are not. Meadowood is a Fora / Virtuoso preferred partner, and booking through me often includes an additional $500 property credit on top of standard amenities like breakfast and upgrade priority.",
        visited_verb="stayed many times at", credit_label="", partner_clause="",
        intro=[
            "There's something so special about Meadowood, and it's sort of hard to put your finger on it. Service is at Aman quality standards, with a real sense of place, spacious and fairly private cottages, a beautiful spa, and thoughtful turndown treats each evening.",
            "It's a small property — around 40 cottages tucked into a private wooded estate above St. Helena — and there really isn't a bad room to be had. That combination of intimacy and polish is why it holds #01 in my <a href=\"../napa-sonoma.html\">Napa &amp; Sonoma ranking</a> after years of repeat stays across the valley.",
            "Every time I go to Meadowood, I feel well taken care of — and I can't say that about every property on this list.",
        ],
        stood_out=[
            ("Service at Aman standards.", "The single biggest separator in wine country — you feel looked after from arrival to checkout."),
            ("The cottages.", "Spacious, private, and scattered through the estate's woods — around 40 keys total, with no bad rooms."),
            ("The tennis facility is a hidden gem.", "Beautiful courts with instructors I'd recommend in a heartbeat."),
            ("The details.", "Thoughtful turndown treats each evening, and a beautiful spa to build slow mornings around."),
        ],
        know=[
            ("Mind the stairs.", "About 90% of rooms aren't fully accessible, though buggies are available for those with mobility concerns."),
            ("It skews a bit older.", "The property tends to attract 40+ couples, though there's a family pool and it works well solo too."),
            ("Book through a Virtuoso partner.", "The additional credit — often $500 — meaningfully changes the math on a multi-night stay."),
        ],
        verdict="Every time I go to Meadowood, I feel well taken care of — and I can't say that about every property on this list.",
    ),
    dict(
        slug="four-seasons-napa-valley", name="Four Seasons Napa Valley", short_name="Four Seasons Napa",
        island="Wine Country", island_page="napa-sonoma.html", img_dir="napa",
        locale="Calistoga, Napa Valley", region_label="Region",
        region_html="Calistoga, Napa Valley, California",
        stat1_num="#02", stat1_label="In My Napa &amp; Sonoma Ranking",
        rank_href="napa-sonoma.html", rank_text="#02 in my Napa &amp; Sonoma ranking",
        related_text="See The Full Napa &amp; Sonoma Ranking", cta_island_text="The Napa &amp; Sonoma Ranking",
        cta2_href="hotel-guides.html", cta2_text="All Hotel Guides",
        mailto_prep="in",
        hero_img="four-seasons-1.jpg", img2="four-seasons-2.jpg",
        stat2_num="1&#9733;", stat2_label="Michelin Restaurant In The Vineyards",
        meta_desc="Keith's firsthand review of Four Seasons Napa Valley — four-plus stays in, the most versatile luxury resort in wine country, with a Michelin star on property.",
        tagline="Set within its own working vineyard in Calistoga &mdash; consistently excellent, and the rare wine country hotel that fits almost everyone.",
        style_label="Vineyard resort", perfect_for="Families, girls trips, couples, groups",
        perks_html="Rates through me are identical to booking direct &mdash; the perks are not. Four Seasons Napa Valley is a Fora / Virtuoso preferred partner, and booking through me sometimes includes a third or fourth night free on top of standard amenities like breakfast and upgrade priority.",
        visited_verb="stayed repeatedly at", credit_label="", partner_clause="",
        intro=[
            "I've stayed at Four Seasons Napa Valley four or five times now, and since they've worked out the early kinks, I think they've earned the #02 spot in my <a href=\"../napa-sonoma.html\">Napa &amp; Sonoma ranking</a>.",
            "Architecturally the hotel is beautiful, with a mix of dark, moody rooms and bright white farmhouse styles set within the vineyards. The pools are gorgeous, the one-star Michelin restaurant is fantastic, and I love the pool bar.",
            "What actually separates it from the property just below it on my list is simpler: service at genuine Four Seasons standard, applied to a resort that fits families, couples, girls trips, and multi-couple groups equally well.",
        ],
        stood_out=[
            ("Service at Four Seasons standard.", "Genuinely what separates it from the hotels below it — consistent across every stay I've had."),
            ("A Michelin star on property.", "The one-star restaurant is fantastic, and the pool bar is a favorite in its own right."),
            ("The architecture.", "Dark moody rooms or bright white farmhouse styles, set within a working vineyard."),
            ("It fits almost everyone.", "Families, couples, girls trips, and groups all genuinely work here — rare at this level."),
        ],
        know=[
            ("Request an upper floor if shower privacy matters.", "Some ground-floor outdoor showers face the pathways — easily handled at booking; just tell me."),
            ("Calistoga is the far end of the valley.", "Beautiful, quieter, and a longer drive from the southern wineries — plan tastings accordingly."),
            ("Watch for the free-night offers.", "Third or fourth night free shows up through preferred partner channels — it changes the math on longer stays."),
        ],
        verdict="It's a great property that lends itself to a large swath of people.",
    ),
    dict(
        slug="montage-healdsburg", name="Montage Healdsburg", short_name="Montage Healdsburg",
        island="Wine Country", island_page="napa-sonoma.html", img_dir="napa",
        locale="Healdsburg, Sonoma County", region_label="Region",
        region_html="Healdsburg, Sonoma County, California",
        stat1_num="#03", stat1_label="In My Napa &amp; Sonoma Ranking",
        rank_href="napa-sonoma.html", rank_text="#03 in my Napa &amp; Sonoma ranking",
        related_text="See The Full Napa &amp; Sonoma Ranking", cta_island_text="The Napa &amp; Sonoma Ranking",
        cta2_href="hotel-guides.html", cta2_text="All Hotel Guides",
        mailto_prep="in",
        hero_img="montage-1.jpg", img2="montage-3-firepit.jpg",
        stat2_num="20+", stat2_label="Stays &mdash; My Most-Returned-To Hotel",
        meta_desc="Keith's firsthand review of Montage Healdsburg after 20+ stays — vineyard rooms with fire pits, the best restaurant view in wine country, and what to book.",
        tagline="My home away from home &mdash; 20-plus stays in, the vineyard rooms and their fire pits still never get old.",
        style_label="Hillside vineyard resort", perfect_for="Wine lovers, couples, returning visitors",
        perks_html="Rates through me are identical to booking direct &mdash; the perks are not. Montage Healdsburg is a Fora / Virtuoso preferred partner, and booking through me sometimes includes a third or fourth night free on top of standard amenities like breakfast and upgrade priority.",
        visited_verb="stayed 20+ times at", credit_label="", partner_clause="",
        intro=[
            "I love the Montage and have stayed there at least 20 times over the past few years — more than any other hotel on my <a href=\"../napa-sonoma.html\">Napa &amp; Sonoma list</a>, which tells you most of what you need to know.",
            "It's perfectly situated just outside downtown Healdsburg, close to wineries, with a complimentary shuttle to the plaza. The dining has perhaps the best view of any restaurant on this list, and I actually prefer the vineyard rooms over the mountain or oak rooms.",
            "It's just a great property, and I feel lucky I've spent so many nights there.",
        ],
        stood_out=[
            ("Book a vineyard room.", "Waking up and sitting by your fire pit overlooking the vineyards never gets old — my clear pick over the mountain and oak categories."),
            ("The best restaurant view on my list.", "Dinner looks out over the vines and hills — no other wine country dining room matches it."),
            ("They remember you.", "One masseuse in particular I make a point to see every time I go — the returning-guest experience is real."),
            ("The Healdsburg shuttle.", "Complimentary rides to the plaza mean nobody argues about who's driving home from dinner."),
        ],
        know=[
            ("Twenty stays in, I notice the small things.", "A few more little misses lately than in year one — nothing that moves it from my top three, and the team always makes it right."),
            ("Choose your room category deliberately.", "Vineyard rooms are the property's magic; the others are lovely but miss the signature view."),
            ("Healdsburg is Sonoma, not Napa.", "A more relaxed, less commercial base — my preference, but know which valley you're signing up for."),
        ],
        verdict="It's just a great property, and I feel lucky I've spent so many nights there.",
    ),
    dict(
        slug="solage-calistoga", name="Solage Calistoga", short_name="Solage",
        island="Wine Country", island_page="napa-sonoma.html", img_dir="napa",
        locale="Calistoga, Napa Valley", region_label="Region",
        region_html="Calistoga, Napa Valley, California",
        stat1_num="#04", stat1_label="In My Napa &amp; Sonoma Ranking",
        rank_href="napa-sonoma.html", rank_text="#04 in my Napa &amp; Sonoma ranking",
        related_text="See The Full Napa &amp; Sonoma Ranking", cta_island_text="The Napa &amp; Sonoma Ranking",
        cta2_href="hotel-guides.html", cta2_text="All Hotel Guides",
        mailto_prep="in",
        hero_img="solage-1.jpg", img2="solage-2.jpg",
        stat2_num="Private", stat2_label="Gardens Or Terraces On Most Rooms",
        meta_desc="Keith's firsthand review of Solage Calistoga — iconic California wine country design, private terraces, and honest notes on where it trails the top three.",
        tagline="Iconic California wine country design &mdash; private gardens, a laid-back energy, and rates that undercut the hotels above it.",
        style_label="Design resort (Auberge)", perfect_for="Younger couples, families, girls trips",
        perks_html="Rates through me are identical to booking direct &mdash; the perks are not. Solage is a Fora / Virtuoso preferred partner, and booking through me sometimes includes a third or fourth night free on top of standard amenities like breakfast and upgrade priority.",
        visited_verb="stayed at", credit_label="", partner_clause="",
        intro=[
            "Solage is sort of iconic — it really defines California wine country luxury, and the design still holds up as the template half the newer properties are chasing.",
            "It sits at #04 on my <a href=\"../napa-sonoma.html\">Napa &amp; Sonoma list</a> mostly on polish: the experience is intentionally more relaxed than the white-glove properties above it, and the spa — a signature here — is due some love. I love the design, and most rooms have a private garden or terrace, some with private hot tubs.",
            "The math works in its favor: rates run lower than the top three, making it one of the strongest cost-to-experience options in the valley.",
        ],
        stood_out=[
            ("Real privacy.", "If you need a completely private terrace or garden, Solage is one of the best options on my entire list — some rooms add private hot tubs."),
            ("The design.", "Iconic Calistoga-modern that defined the look of California wine country luxury."),
            ("The value.", "Rates run meaningfully lower than the properties above it — strong cost-to-experience."),
            ("The energy.", "Younger, more relaxed, and less formal than the top of the list — a feature, not a bug, for the right trip."),
        ],
        know=[
            ("Set spa expectations.", "The spa is a big part of the Solage story and is due for a refresh — worth knowing as you plan treatments."),
            ("The vibe is relaxed, not white-glove.", "A more casual service style than Meadowood or Four Seasons — a feature for some trips, a trade-off for others."),
            ("Calistoga base.", "The far north end of the valley — quieter, hot-springs country, and a longer drive from southern Napa wineries."),
        ],
        verdict="A fantastic hotel — just not quite at the level of the three above it.",
    ),
    dict(
        slug="macarthur-place-sonoma", name="MacArthur Place", short_name="MacArthur Place",
        island="Wine Country", island_page="napa-sonoma.html", img_dir="napa",
        locale="Sonoma, California", region_label="Region",
        region_html="Downtown Sonoma, California",
        stat1_num="#05", stat1_label="In My Napa &amp; Sonoma Ranking",
        rank_href="napa-sonoma.html", rank_text="#05 in my Napa &amp; Sonoma ranking",
        related_text="See The Full Napa &amp; Sonoma Ranking", cta_island_text="The Napa &amp; Sonoma Ranking",
        cta2_href="hotel-guides.html", cta2_text="All Hotel Guides",
        mailto_prep="in",
        hero_img="macarthur.jpg", img2="macarthur.jpg",
        stat2_num="Walk", stat2_label="To Downtown Sonoma &mdash; No Driving Back",
        meta_desc="Keith's firsthand review of MacArthur Place — Sonoma's hidden gem, steps from downtown, with beautiful design, reasonable rates, and a freshly remodeled pool.",
        tagline="Sonoma's hidden gem &mdash; walk to the plaza, skip the designated driver, and pay less than the marquee names.",
        style_label="Boutique garden estate", perfect_for="Returning visitors, walkability, wine tasting",
        perks_html="Rates through me are identical to booking direct &mdash; the perks are not. MacArthur Place is a Fora / Virtuoso preferred partner, and booking through me includes preferred partner amenities like breakfast, property credits, and upgrade priority where available.",
        visited_verb="stayed at", credit_label="", partner_clause="",
        intro=[
            "I love MacArthur Place and think it's such a hidden gem in Sonoma. It's right next to downtown, so you can walk or bike into town, the design is beautiful, prices are reasonable, and the pool just finished an extensive remodel.",
            "The location advantage is bigger than it sounds: it's the easiest walk to town on my entire <a href=\"../napa-sonoma.html\">Napa &amp; Sonoma list</a>, which means nobody worries about driving back after a few glasses of wine.",
            "Downtown Sonoma itself is a big part of the draw — quaint, local, and less commercialized than Healdsburg, with easy access to Glen Ellen. And it's just an easy getaway from San Francisco.",
        ],
        stood_out=[
            ("The easiest walk to town on my list.", "Wine-taste all afternoon and stroll home — no designated driver required."),
            ("The design.", "A beautiful garden-estate feel that punches above its rate."),
            ("The freshly remodeled pool.", "Just finished an extensive renovation — the property's newest asset."),
            ("Downtown Sonoma.", "Quaint, local, and less commercialized than Healdsburg, with Glen Ellen close by."),
        ],
        know=[
            ("Wellness is modest here.", "The draw is the gardens, the remodeled pool, and the town — if a destination spa is central to your trip, I'd build that in elsewhere."),
            ("It's a boutique, not a resort.", "Fewer facilities than the marquee names — the town is your amenity."),
            ("Best as a second-trip base.", "Ideal for returning visitors who've done the Napa marquee circuit and want walkable, local wine country."),
        ],
        verdict="A great option for return visitors who'd rather not drive back to their hotel every night.",
    ),
    dict(
        slug="stanly-ranch-napa", name="Stanly Ranch", short_name="Stanly Ranch",
        island="Wine Country", island_page="napa-sonoma.html", img_dir="napa",
        locale="Carneros, Napa Valley", region_label="Region",
        region_html="Carneros, Napa Valley, California",
        stat1_num="#06", stat1_label="In My Napa &amp; Sonoma Ranking",
        rank_href="napa-sonoma.html", rank_text="#06 in my Napa &amp; Sonoma ranking",
        related_text="See The Full Napa &amp; Sonoma Ranking", cta_island_text="The Napa &amp; Sonoma Ranking",
        cta2_href="hotel-guides.html", cta2_text="All Hotel Guides",
        mailto_prep="in",
        hero_img="stanly-ranch.jpg", img2="stanly-ranch.jpg",
        stat2_num="Fire", stat2_label="Pits On Every Room's Terrace",
        meta_desc="Keith's firsthand review of Stanly Ranch — the most architecturally striking hotel in Napa, the prettiest spa, and why the location keeps it at #06.",
        tagline="Possibly the most architecturally striking hotel in wine country &mdash; with a location that never quite feels like wine country.",
        style_label="Modern ranch resort (Auberge)", perfect_for="Younger couples, wellness travelers, design lovers",
        perks_html="Rates through me are identical to booking direct &mdash; the perks are not. Stanly Ranch is a Fora / Virtuoso preferred partner, and booking through me sometimes includes a third or fourth night free on top of standard amenities like breakfast and upgrade priority.",
        visited_verb="stayed at", credit_label="", partner_clause="",
        intro=[
            "Stanly Ranch might be the most architecturally striking hotel on my <a href=\"../napa-sonoma.html\">Napa &amp; Sonoma list</a>. The spa is arguably the prettiest in the valley, every room has a large outdoor terrace with a fire pit, and Bear, the main restaurant, is one of the more interesting dining options in Napa.",
            "So why #06? The location doesn't quite deliver the classic wine country feeling. It's convenient to both Napa and Sonoma, but it sits out in the Carneros marshes — beautiful in its own way, just not the vineyard postcard most people fly in for.",
            "Beautiful, but I don't find myself wanting to go back as often as the hotels above it.",
        ],
        stood_out=[
            ("The architecture.", "Arguably the most striking design statement in wine country — modern ranch done at full conviction."),
            ("The spa.", "The prettiest in the valley in my book — wellness travelers should weight this heavily."),
            ("Fire pits on every terrace.", "Every room gets a large outdoor terrace with its own fire pit."),
            ("Bear.", "The main restaurant is one of the more interesting dining options in Napa right now."),
        ],
        know=[
            ("It doesn't feel like wine country.", "Convenient to both valleys, but set in the marshes — if the vineyard postcard is the point, look at <a href=\"montage-healdsburg.html\">Montage</a> or <a href=\"meadowood-napa-valley.html\">Meadowood</a>."),
            ("Terrace privacy varies.", "Some are wonderfully secluded, others more open — I'll steer you to the best-sited rooms."),
            ("The smart-room tech takes a night.", "Give the lighting controls an evening to learn — after that you're fluent."),
        ],
        verdict="Beautiful, but I don't find myself wanting to go back as often as the hotels above it.",
    ),
    dict(
        slug="madrona-manor-healdsburg", name="Madrona Manor", short_name="Madrona",
        island="Wine Country", island_page="napa-sonoma.html", img_dir="napa",
        locale="Healdsburg, Sonoma County", region_label="Region",
        region_html="Healdsburg, Sonoma County, California",
        stat1_num="#07", stat1_label="In My Napa &amp; Sonoma Ranking",
        rank_href="napa-sonoma.html", rank_text="#07 in my Napa &amp; Sonoma ranking",
        related_text="See The Full Napa &amp; Sonoma Ranking", cta_island_text="The Napa &amp; Sonoma Ranking",
        cta2_href="hotel-guides.html", cta2_text="All Hotel Guides",
        mailto_prep="in",
        hero_img="madrona.jpg", img2="madrona.jpg",
        stat2_num="Estate", stat2_label="Living &mdash; Not A Traditional Hotel",
        meta_desc="Keith's firsthand review of Madrona Manor — a Jay Jeffers-designed Healdsburg estate that feels like a home, and one of Sonoma's most romantic stays.",
        tagline="Not a hotel so much as someone's impossibly beautiful estate &mdash; and one of the most romantic front porches in Sonoma County.",
        style_label="Historic estate (Jay Jeffers design)", perfect_for="Couples, romantic getaways",
        perks_html="Rates through me are identical to booking direct &mdash; the perks are not. Madrona is a Fora / Virtuoso preferred partner, and booking through me includes preferred partner amenities like breakfast, property credits, and upgrade priority where available.",
        visited_verb="stayed at", credit_label="", partner_clause="",
        intro=[
            "Madrona Manor feels completely different from every other hotel on my <a href=\"../napa-sonoma.html\">Napa &amp; Sonoma list</a> — more like staying at someone's incredibly beautiful estate than a traditional luxury hotel.",
            "The design by Jay Jeffers is stunning, and sitting on the front porch with a glass of wine overlooking the vineyards is one of my favorite experiences anywhere in Sonoma County.",
            "The trade-offs are real but simple: there's no spa, the pool is underwhelming, and this is emphatically a couples property — I wouldn't recommend it for families. For a romantic weekend, none of that matters.",
        ],
        stood_out=[
            ("The Jay Jeffers design.", "A stunning estate restoration — every room feels collected rather than specified."),
            ("The front porch.", "A glass of wine overlooking the vineyards from that porch is one of my favorite moments in Sonoma County."),
            ("The estate feel.", "You're a houseguest, not a room number — completely different energy from every resort on this list."),
            ("E-bikes to Healdsburg Plaza.", "Just a few minutes away, while the property itself stays perfectly peaceful."),
        ],
        know=[
            ("No spa, and the pool is underwhelming.", "The main drawbacks on an otherwise special property — build your trip around the estate, not the facilities."),
            ("This is a couples property.", "I wouldn't recommend it for families — and that's precisely its charm."),
            ("An estate has estate quirks.", "Historic buildings mean character over uniformity — ask me which rooms suit you."),
        ],
        verdict="An easy recommendation for a romantic weekend with beautiful design and one of the most charming atmospheres in wine country.",
    ),
    dict(
        slug="carneros-resort-napa", name="Carneros Resort &amp; Spa", short_name="Carneros",
        island="Wine Country", island_page="napa-sonoma.html", img_dir="napa",
        locale="Carneros, Napa Valley", region_label="Region",
        region_html="Carneros, Napa Valley, California",
        stat1_num="#08", stat1_label="In My Napa &amp; Sonoma Ranking",
        rank_href="napa-sonoma.html", rank_text="#08 in my Napa &amp; Sonoma ranking",
        related_text="See The Full Napa &amp; Sonoma Ranking", cta_island_text="The Napa &amp; Sonoma Ranking",
        cta2_href="hotel-guides.html", cta2_text="All Hotel Guides",
        mailto_prep="in",
        hero_img="carneros.jpg", img2="carneros.jpg",
        stat2_num="Top 5", stat2_label="Potential &mdash; After A Renovation",
        meta_desc="Keith's firsthand review of Carneros Resort & Spa — sprawling grounds, private cottages, real wine country feel, and why it's overdue for a refresh.",
        tagline="Sprawling grounds, private cottages, and true wine country atmosphere &mdash; a beloved classic ready for its next chapter.",
        style_label="Cottage resort", perfect_for="Families, multi-couple groups, older couples",
        perks_html="Rates through me are identical to booking direct &mdash; the perks are not. Carneros is a Fora / Virtuoso preferred partner, and booking through me sometimes includes a third or fourth night free on top of standard amenities like breakfast and upgrade priority.",
        visited_verb="stayed multiple times at", credit_label="", partner_clause="",
        intro=[
            "Carneros has the potential to be a top-five property on my <a href=\"../napa-sonoma.html\">Napa &amp; Sonoma list</a> — it's a beloved classic that's ready for its next chapter.",
            "The grounds are sprawling and beautiful, every cottage has private outdoor space, and I actually prefer the location to Stanly Ranch — it feels much more like wine country.",
            "With a refresh, I honestly think this property moves several spots higher on my list. In the meantime, book it for what it does beautifully: space, privacy, and that unmistakable wine country feel.",
        ],
        stood_out=[
            ("It feels like wine country.", "I prefer this location to Stanly Ranch — the vineyard-and-barn landscape is the real thing."),
            ("Every cottage has private outdoor space.", "The layout is built for slow mornings on your own patio."),
            ("One of Napa's larger spas.", "Serious square footage — and, like the rooms, it will shine brightest after a refresh."),
            ("The two-bedroom residences are fantastic.", "The best product on the property — ideal for families and multi-couple groups."),
        ],
        know=[
            ("A refresh would change everything.", "The rooms and spa are ready for their next chapter — my ranking already prices that in."),
            ("Consistency varies.", "Some stays have been flawless, others less so — booking through me means someone is watching your file."),
            ("Book the residences if you can.", "I can't personally speak to the standard rooms, though most have private patios — the two-bedrooms are the play."),
        ],
        verdict="With a renovation, I honestly think this property could move several spots higher on this list.",
    ),
    dict(
        slug="alila-napa-valley", name="Alila Napa Valley", short_name="Alila",
        island="Wine Country", island_page="napa-sonoma.html", img_dir="napa",
        locale="St. Helena, Napa Valley", region_label="Region",
        region_html="St. Helena, Napa Valley, California",
        stat1_num="#09", stat1_label="In My Napa &amp; Sonoma Ranking",
        rank_href="napa-sonoma.html", rank_text="#09 in my Napa &amp; Sonoma ranking",
        related_text="See The Full Napa &amp; Sonoma Ranking", cta_island_text="The Napa &amp; Sonoma Ranking",
        cta2_href="hotel-guides.html", cta2_text="All Hotel Guides",
        mailto_prep="in",
        hero_img="alila.jpg", img2="alila.jpg",
        stat2_num="Walk", stat2_label="To Downtown St. Helena",
        meta_desc="Keith's firsthand review of Alila Napa Valley — a sleek modern hotel walkable to St. Helena, strongest for Hyatt points travelers.",
        tagline="A sleek modern hotel that happens to be in Napa &mdash; excellent location, walkable to St. Helena, strongest on points.",
        style_label="Modern boutique (Hyatt)", perfect_for="Hyatt loyalists, younger travelers",
        perks_html="Rates through me are identical to booking direct &mdash; the perks are not. Alila is a Fora / Virtuoso preferred partner, and booking through me includes preferred partner amenities like breakfast, property credits, and upgrade priority where available.",
        visited_verb="stayed at", credit_label="", partner_clause="",
        intro=[
            "I like Alila quite a bit. Its personality is contemporary-first rather than vineyard-romantic — a genuinely lovely modern hotel whose aesthetic will click instantly for some travelers, which is exactly how to choose it against the hotels above it on my <a href=\"../napa-sonoma.html\">Napa &amp; Sonoma list</a>.",
            "The location is excellent, though, and being able to walk into downtown St. Helena is a huge plus — one of the few walkable bases in the heart of the valley.",
            "Where it genuinely shines is for points travelers: if you're sitting on Hyatt points, this is one of the best redemptions in wine country.",
        ],
        stood_out=[
            ("Walkable to St. Helena.", "One of the few luxury bases where downtown dining is a stroll, not a drive."),
            ("Book a vineyard-facing room.", "Significantly better than the alternatives if you can get one."),
            ("The Hyatt points play.", "For World of Hyatt loyalists, one of wine country's best-value redemptions."),
            ("Clean modern design.", "Sleek and current — if you prefer contemporary over farmhouse, this is your aesthetic."),
        ],
        know=[
            ("Contemporary-first by design.", "More sleek retreat than vineyard estate — pick it because of that, not despite it."),
            ("The pool is intimate rather than resort-scale.", "Plan big pool days elsewhere and use Alila as your stylish, walkable base."),
            ("On points, it's a standout.", "At cash rates, compare against the list above for your dates — on Hyatt points, it's one of wine country's best redemptions."),
        ],
        verdict="A good hotel whose modern character is a matter of taste — my ranking reflects my own preference for vineyard romance more than any flaw in execution.",
    ),
]

import os, glob, importlib.util
os.makedirs(f"{SITE}/hotels", exist_ok=True)

# Additional hotel batches live in tools/hotel_data_*.py, each exporting HOTELS = [...]
for _mod_path in sorted(glob.glob(os.path.join(SITE, "tools", "hotel_data_*.py"))):
    _spec = importlib.util.spec_from_file_location(os.path.basename(_mod_path)[:-3], _mod_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    HOTELS += _mod.HOTELS

for h in HOTELS:
    plain_name = html.unescape(h["name"])
    body = (
        "Hi Keith,%0A%0AI'm interested in " + quote(plain_name) + " " + h.get("mailto_prep", "on") + " " + h["island"] +
        ".%0A%0AName: %0ATravel Dates: %0AOccasion: %0A%0A"
    )
    mailto = ("mailto:keith.pence@fora.travel?subject=" + quote(plain_name + " Inquiry") + "&body=" + body)
    rank_href_v = h.get("rank_href", "best-hotels-greece.html")
    perks_default = (
        "Rates through me are identical to booking direct &mdash; the perks are not. As a Fora advisor"
        + h.get("partner_clause", "")
        + ", my clients receive a space-available upgrade, daily breakfast, and a "
        + h.get("credit_label", "hotel credit")
        + " &mdash; plus my direct line to the team on property before and during your stay."
    )
    out = PAGE.substitute(
        locale=h.get("locale", h["island"] + ", Greece"),
        img_dir=h.get("img_dir", "hotels"),
        region_label=h.get("region_label", "Island"),
        region_html=h.get("region_html", '<a href="../' + h["island_page"] + '">' + h["island"] + ' Destination Guide &rarr;</a>'),
        perks_html=h.get("perks_html", perks_default),
        cta_island_text=h.get("cta_island_text", "My " + h["island"] + " Guide"),
        cta2_href=h.get("cta2_href", rank_href_v),
        slug=h["slug"], name=h["name"], short_name=h["short_name"], island=h["island"],
        island_page=h["island_page"], rank_num=h.get("rank_num", ""), hero_img=h["hero_img"],
        img2=h.get("img2", h["hero_img"]),
        know_heading=h.get("know_heading", "The Fine Print, From Someone Who's Been"),
        cta_line=h.get("cta_line", "I've personally " + h["visited_verb"] + " " + h["short_name"] + ". Let me match you to the right room, time it to the right season, and build the rest of the trip around it."),
        stat1_num=h.get("stat1_num", "#" + h.get("rank_num", "")),
        stat1_label=h.get("stat1_label", "In My Greece Top 10"),
        rank_href=rank_href_v,
        rank_text=h.get("rank_text", "#" + h.get("rank_num", "") + " of my Greece Top 10"),
        related_text=h.get("related_text", "See The Full Greece Top 10"),
        cta2_text=h.get("cta2_text", "The Greece Top 10"),
        stat2_num=h["stat2_num"], stat2_label=h["stat2_label"], meta_desc=h["meta_desc"],
        tagline=h["tagline"], style_label=h["style_label"], perfect_for=h["perfect_for"],
        credit_label=h["credit_label"], partner_clause=h["partner_clause"], visited_verb=h["visited_verb"],
        intro_paras="\n".join(para(p) for p in h["intro"]),
        stood_out_notes="\n".join(note(b, t) for b, t in h["stood_out"]),
        know_notes="\n".join(note(b, t) for b, t in h["know"]),
        verdict=h["verdict"], mailto=mailto,
        plain_name=html.escape(plain_name, quote=True), out_file=h["slug"] + ".html",
    )
    path = f"{SITE}/hotels/{h['slug']}.html"
    with open(path, "w") as f:
        f.write(out)
    print("wrote", path)
