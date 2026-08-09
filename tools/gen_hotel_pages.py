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
<title>$name Review — $island, Greece | Suites With Keith</title>
<meta name="description" content="$meta_desc">
<link rel="canonical" href="https://suiteswithkeith.com/hotels/$slug.html">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="icon" href="../favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">

<meta property="og:type" content="article">
<meta property="og:title" content="$name Review — $island, Greece | Suites With Keith">
<meta property="og:description" content="$meta_desc">
<meta property="og:url" content="https://suiteswithkeith.com/hotels/$slug.html">
<meta property="og:image" content="https://suiteswithkeith.com/images/hotels/$hero_img">
<meta property="og:site_name" content="Suites With Keith">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="$name Review — $island, Greece | Suites With Keith">
<meta name="twitter:description" content="$meta_desc">
<meta name="twitter:image" content="https://suiteswithkeith.com/images/hotels/$hero_img">

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
  "headline": "$name Review — $island, Greece",
  "description": "$meta_desc",
  "image": "https://suiteswithkeith.com/images/hotels/$hero_img",
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

<header class="rank-hero" style="background-image:url('../images/hotels/$hero_img');">
  <div class="container">
    <span class="eyebrow-mag">Hotel Guides &middot; $island, Greece</span>
    <h1>$name</h1>
    <p class="tagline">$tagline</p>
    <div class="rank-stats">
      <div><span class="stat-num">$stat1_num</span><span class="stat-label">$stat1_label</span></div>
      <div><span class="stat-num">$stat2_num</span><span class="stat-label">$stat2_label</span></div>
    </div>
    <div style="margin-top:32px;">
      <a href="$mailto" class="btn btn-tan">Inquire To Book</a>
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
      <span class="glance-row"><span class="g-label">Island</span><a href="../$island_page">$island Destination Guide &rarr;</a></span>
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
        <img src="../images/hotels/$img2" alt="$name, $island">
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
        <h3>The Fine Print, From Someone Who's Been</h3>
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
      <p>Rates through me are identical to booking direct &mdash; the perks are not. As a Fora advisor$partner_clause, my clients receive a space-available upgrade, daily breakfast, and a $credit_label &mdash; plus my direct line to the team on property before and during your stay.</p>
      <a href="$mailto" class="btn btn-olive">Check Availability</a>
    </div>
  </div>
</section>

<section class="guide-cta">
  <div class="container">
    <span class="eyebrow">Planning A Trip To $island?</span>
    <h2>I've personally $visited_verb $short_name. Let me match you to the right room, time it to the right season, and build the rest of the trip around it.</h2>
    <a href="$mailto" class="btn btn-tan">Plan Your Trip</a>
    <p style="margin-top:26px;"><a href="../$island_page" class="read-link">My $island Guide &rarr;</a> &nbsp;&nbsp; <a href="../$rank_href" class="read-link">$cta2_text &rarr;</a></p>
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
      <p>Luxury travel advisor specializing in Europe, honeymoons, hotel bookings, and personalized itineraries.</p>
    </div>
    <div class="footer-mid">
      <div class="footer-badge">SWK</div>
      <div class="partner-logos">
        <img src="../images/logos/virtuoso.png" alt="Virtuoso">
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
            ("A team that listens.", "A few finishes aren't holding up to the elements yet, but the staff was responsive and grateful — not defensive — when things were flagged. I can't say that about every hotel from this trip."),
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
        tagline="Authentic cave-style luxury in the heart of Oia — my top Santorini property until I experienced Canaves.",
        style_label="Cave-style boutique", perfect_for="Younger honeymooners, first-timers",
        credit_label="&euro;100 hotel credit", partner_clause=" with a preferred partnership at Andronis", visited_verb="toured every corner of",
        intro=[
            "This was actually my top property in Santorini until I experienced Canaves — which is to say it's a truly fantastic, top-notch hotel. Recently renovated, the rooms are authentic cave-style rooms with beautiful finishes and fixtures, and they're what people actually picture when they book Santorini.",
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
            ("Wellness isn't the selling point.", "The spa is small and the gym is adequate. If a serious gym matters, that's <a href=\"cali-mykonos.html\">Cali</a>."),
            ("The food wasn't my favorite of the trip.", "Perfectly good, not a destination in itself — happily, Mykonos dining is a short drive away."),
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
]

import os
os.makedirs(f"{SITE}/hotels", exist_ok=True)

for h in HOTELS:
    plain_name = html.unescape(h["name"])
    body = (
        "Hi Keith,%0A%0AI'm interested in " + quote(plain_name) + " on " + h["island"] +
        ".%0A%0AName: %0ATravel Dates: %0AOccasion: %0A%0A"
    )
    mailto = ("mailto:keith.pence@fora.travel?subject=" + quote(plain_name + " Inquiry") + "&body=" + body)
    out = PAGE.substitute(
        slug=h["slug"], name=h["name"], short_name=h["short_name"], island=h["island"],
        island_page=h["island_page"], rank_num=h.get("rank_num", ""), hero_img=h["hero_img"], img2=h["img2"],
        stat1_num=h.get("stat1_num", "#" + h.get("rank_num", "")),
        stat1_label=h.get("stat1_label", "In My Greece Top 10"),
        rank_href=h.get("rank_href", "best-hotels-greece.html"),
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
    )
    path = f"{SITE}/hotels/{h['slug']}.html"
    with open(path, "w") as f:
        f.write(out)
    print("wrote", path)
