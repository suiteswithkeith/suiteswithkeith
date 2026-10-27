#!/usr/bin/env python3
"""Render an Italy head-to-head page (<slug>.html at the site root) from
tools/versus-italy/<slug>.json, in the layout of il-san-pietro-vs-le-sirenuse.html
(hero pair, choose columns, comparison table, verdict band, detail grid, FAQ,
inquiry form). The shared head styles, nav and footer are copied verbatim from
tools/versus-italy/_*.html.

Usage: python3 tools/render_vs_italy.py [<slug> ...]   (no args = every spec)

Spec fields: title, description and the hotel names in "a"/"b" are plain text.
Every other text field is HTML and is injected verbatim (use &rsquo;, &middot;,
and <a href="/hotels/...">...</a> links as on the reference page).
"""
import glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = f'{ROOT}/tools/versus-italy'
part = lambda n: open(f'{SPEC}/_{n}.html').read()
HEAD_STYLES, NAV, FOOTER = part('head_styles'), part('nav'), part('footer')

LINK = ('style="font-size:.72rem; font-weight:500; letter-spacing:.14em; '
        'text-transform:uppercase; color:var(--brass); text-decoration:none;"')


def attr(s):
    return html.escape(s, quote=True)


def plain(h):
    return html.unescape(re.sub(r'<[^>]+>', '', h)).strip()


def render(slug):
    v = json.load(open(f'{SPEC}/{slug}.json'))
    a, b = v['a'], v['b']
    url = f'https://suiteswithkeith.com/{slug}.html'
    og = v['hero'][0]['src']
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": plain(f['q']),
         "acceptedAnswer": {"@type": "Answer", "text": plain(f['a'])}} for f in v['faq']]},
        ensure_ascii=False)
    art_ld = json.dumps({"@context": "https://schema.org", "@type": "Article",
        "headline": plain(f"{v['h1_a']} {v['h1_b']}"),
        "author": {"@type": "Person", "name": "Keith Pence", "url": "https://suiteswithkeith.com/about.html"},
        "publisher": {"@type": "Organization", "name": "Suites With Keith", "url": "https://suiteswithkeith.com/"},
        "datePublished": v.get('date', '2026-10-27'), "image": f"https://suiteswithkeith.com{og}", "url": url},
        ensure_ascii=False)

    hero = ''.join(
        f'<img src="{h["src"]}" alt="{attr(h["alt"])}" fetchpriority="high" style="width:100%; height:100%; '
        f'object-fit:cover; display:block; object-position:{h.get("pos", "50% 50%")};">' for h in v['hero'])

    def choose_col(c, h):
        return (f'<div class="choose-col"><span class="eyebrow">Choose {h["short"]}</span><h3>{c["h3"]}</h3>'
                f'<p class="lead">{c["lead"]}</p>\n<a href="{h["href"]}" {LINK[:-1]} display:inline-block; margin-top:14px;">'
                f'My {h["short"]} review&nbsp;&rarr;</a>\n<figure style="margin:24px 0 0;"><img src="{c["img"]}" '
                f'alt="{attr(c["alt"])}" loading="lazy" decoding="async" style="aspect-ratio:16/10; object-fit:cover; '
                f'width:100%;"></figure></div>')

    rows = ''.join(f'<tr><td class="rowlabel">{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>' for r in v['rows'])
    band = ''.join(f'<p class="body-2 reveal" style="margin-top:22px; max-width:56ch;">{p}</p>' for p in v['band']['paras'])
    guide = ''.join(
        f'<div class="reveal"><figure class="vs-guide-img"><img src="{g["img"]}" alt="{attr(g["alt"])}" loading="lazy" '
        f'decoding="async"></figure><h3>{g["h3"]}</h3>' +
        ''.join(f'<p class="body-2">{p}</p>' for p in g['paras']) + '</div>' for g in v['guide'])
    faq = ''.join(f'<details><summary>{f["q"]}</summary><p class="body-2">{f["a"]}</p></details>' for f in v['faq'])
    related = ' '.join(f'<a href="{r["href"]}" {LINK}><span>{r["label"]}</span>&nbsp;&rarr;</a>' for r in v['related'])
    pair = f'{a["short"]} / {b["short"]}'

    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{attr(v["title"])}</title>
<meta name="description" content="{attr(v["description"])}">
<link rel="canonical" href="{url}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{attr(v["title"])}">
<meta property="og:description" content="{attr(v["description"])}">
<meta property="og:image" content="https://suiteswithkeith.com{og}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" as="image" href="{og}" fetchpriority="high">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0J39101CS2"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-0J39101CS2');
</script>
<script type="application/ld+json">{faq_ld}</script>
<script type="application/ld+json">{art_ld}</script>
{HEAD_STYLES}</head>
<body>
{NAV}
<header class="hero" style="min-height:min(82svh,760px);">
<div class="hero-img" style="display:grid; grid-template-columns:repeat(2,1fr); gap:2px;">{hero}</div>
<div class="container"> <p class="eyebrow">Head-to-head &middot; {v["place"]}</p> <h1 class="display-xl vs-h1" style="max-width:18ch;">{v["h1_a"]} <em style="font-style:italic; color:inherit;">{v["h1_b"]}</em></h1> <p class="sub" style="max-width:50ch;">{v["sub"]}</p> <p class="stamp" style="margin-top:20px;">{v["stamp"]}</p> </div>
</header><section class="section"><div class="container"><div class="choose reveal">{choose_col(v["choose"][0], a)}{choose_col(v["choose"][1], b)}</div></div></section><section class="section" style="padding-top:0;"><div class="container"> <div class="sec-head reveal"><span class="eyebrow">Side by side</span><h2 class="display-l">How they compare</h2></div> <div class="table-wrap reveal"><table><thead><tr><th></th><th><a href="{a["href"]}" style="color:inherit;">{a["short"]}</a></th><th><a href="{b["href"]}" style="color:inherit;">{b["short"]}</a></th></tr></thead><tbody>{rows}</tbody></table></div> <p class="body-2 reveal small" style="margin-top:18px; max-width:62ch;">{v["pitch"]}</p> </div></section><section class="section band on-shadow"><div class="container" style="max-width:860px;"> <span class="eyebrow reveal" style="display:block; margin-bottom:16px;">The question behind the question</span> <h2 class="display-l reveal">{v["band"]["h2"]}</h2> {band} </div></section><section class="section"><div class="container"> <div class="sec-head reveal"><span class="eyebrow">The detail</span><h2 class="display-l">What to know before you choose</h2></div> <div class="vs-guide">{guide}</div> </div></section><section class="section" style="padding-top:0;"><div class="container" style="max-width:820px;"> <div class="sec-head reveal"><span class="eyebrow">Before you ask</span><h2 class="display-l">The questions I get</h2></div> <div class="vs-faq reveal">{faq}</div> </div></section><section class="section inquire" id="inquire"><div class="container">
<h2 class="display-l reveal">Still deciding?</h2>
<p class="deck reveal" style="margin:18px auto 0; max-width:42ch;">{v["inquire_deck"]}</p>
<form class="inquire-form reveal" action="https://formspree.io/f/mjgnadov" method="POST">
<input type="hidden" name="_subject" value="{attr(a["short"] + " vs " + b["short"])} Inquiry">
<input type="hidden" name="hotel" value="{attr(pair)}">
<input type="hidden" name="page" value="{slug}">
<input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
<div class="step1"><label for="q-when">When are you thinking?</label>
<input id="q-when" type="text" name="travel_dates" placeholder="{v.get("dates_placeholder", "September 2027 &middot; 4 nights")}" required autocomplete="off"></div>
<div class="step2"><label for="q-name">And where do I send the recommendation?</label>
<input id="q-name" type="text" name="name" placeholder="Name" required autocomplete="name">
<input id="q-email" type="email" name="email" placeholder="Email" required autocomplete="email">
<label for="q-details" style="margin-top:2px;">Anything else? Guests, budget, occasion (optional)</label>
<input id="q-details" type="text" name="details" placeholder="2 adults &middot; honeymoon" autocomplete="off"></div>
<button type="submit" class="btn" data-gtag-label="versus_inquiry_send" data-gtag-location="versus_cta">Send</button>
<p class="note">Traveling within the next 30 days? You will hear from me today.</p>
<p class="status" role="status" aria-live="polite"></p>
</form>
<p class="reveal" style="margin-top:26px; display:flex; gap:12px 32px; justify-content:center; flex-wrap:wrap;"> {related} </p>
</div></section>
{FOOTER.rstrip()}
'''
    open(f'{ROOT}/{slug}.html', 'w').write(out)
    return slug


if __name__ == '__main__':
    slugs = sys.argv[1:] or sorted(os.path.basename(p)[:-5] for p in glob.glob(f'{SPEC}/[!_]*.json'))
    for s in slugs:
        print('rendered', render(s))
