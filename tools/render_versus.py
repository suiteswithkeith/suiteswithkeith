#!/usr/bin/env python3
"""Render a head-to-head page (<slug>.html at the site root) from its entry in
phase1/src/data/versus.json. This is the static twin of
phase1/src/layouts/Versus.astro: keep the two in step when the layout changes.

Usage: python3 tools/render_versus.py <slug> [<slug> ...]

The page shell (everything up to </nav> and from <footer> on: analytics, fonts,
shared CSS, nav, footer, scripts) is kept from the existing page, or copied from
REF_SLUG for a new page. The title, description, canonical, Open Graph tags,
preload and the Article JSON-LD are refreshed from the entry (the JSON-LD keeps
its existing dates and author link, which tools/geo.py maintains). Everything
between the nav and the footer is rebuilt from the entry.

Page order:
  1  header           eyebrow, h1_a / h1_b, deck, stamp
  2  choose           the two "Choose ..." cards (optional img per card)
  3  pair*            one large photograph of each hotel, side by side
  4  comparison       rows [label, a, b]; row_photos* add a photo pair under a row
  5  gallery*         gallery_h2, gallery [{hotel: a|b, ...photo}]
  6  map*             built by tools/render_versus_map.py (images/maps/<slug>.svg)
  7  verdict          final* ("So, which would I book?") or the classic verdict band
     guide*, faq*, inside*   (the long-form extras some pages carry)
  8  booking band     injected by js/swk-book.js right before #inquire
  9  inquire          the form
 10  keep reading     related links
  (* optional: a page without them renders exactly as before)

A photo is {"src", "alt", "w", "h", "cap", "pos"?} using an image already on
the site, or {"placeholder": "what the photo should show", "cap"} until Keith
has his own. Placeholders render as a marked plaster panel (class vs-ph,
data-placeholder) so they are easy to find: grep -n 'data-placeholder' *.html

Copy fields are HTML (entities, links) and are injected verbatim; title,
description, subject, hotel and placeholder are plain text.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF_SLUG = 'auberge-du-soleil-vs-montage-healdsburg'
LINK_STYLE = ('style="font-size:13px; font-weight:400; letter-spacing:.2em; text-transform:uppercase; '
              'color:var(--brass); text-decoration:none; font-family: \'Instrument Serif\', Didot, Georgia, serif;"')


def plain(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('\xa0', ' ').strip()


def attr(s):
    return html.escape(s, quote=True)


def names(g):
    return plain(g['h1_a']), plain(g['h1_b']).rstrip('?').strip()


# ── pieces ──────────────────────────────────────────────────────────────────
def photo(ph, hotel=None, eager=False):
    """One figure: a real image, or a clearly marked placeholder."""
    label = f'<span class="vs-fig-hotel">{hotel}</span>' if hotel else ''
    cap = f'<figcaption>{label}{ph.get("cap", "")}</figcaption>' if (hotel or ph.get('cap')) else ''
    if 'placeholder' in ph:
        what = ph['placeholder']
        aria = attr(f'Photograph to come{": " + plain(hotel) if hotel else ""}, {plain(what)}')
        return (f'<figure class="vs-fig vs-ph" data-placeholder="{attr(plain(what))}">'
                f'<div class="vs-ph-box" role="img" aria-label="{aria}">'
                f'<span class="vs-ph-mark">Photograph to come</span><span class="vs-ph-note">{what}</span></div>{cap}</figure>')
    pos = f' style="object-position:{ph["pos"]};"' if ph.get('pos') else ''
    size = f' width="{ph["w"]}" height="{ph["h"]}"' if ph.get('w') else ''
    load = '' if eager else ' loading="lazy"'
    return (f'<figure class="vs-fig"><img src="{ph["src"]}" alt="{ph["alt"]}"{size}{load} decoding="async"{pos}>'
            f'{cap}</figure>')


def sec_head(eyebrow, h2):
    return (f'<div class="sec-head reveal"> <span class="eyebrow">{eyebrow}</span> '
            f'<h2 class="display-l">{h2}</h2> </div>')


def header(g):
    return (f'<header class="section" style="padding-bottom:0;"> <div class="container"> '
            f'<p class="eyebrow reveal">{g["eyebrow"]}</p> '
            f'<h1 class="display-xl reveal vs-h1"><span>{g["h1_a"]}</span> or <em style="font-style:italic; color:var(--brass);">{g["h1_b"]}</em></h1> '
            f'<p class="deck reveal" style="margin-top:22px; max-width:48ch;">{g["deck"]}</p> '
            f'<p class="stamp reveal" style="margin-top:26px;">{g["stamp"]}</p> </div> </header>')


def choose(g):
    cols = ''
    for c in g['choose']:
        fig = ''
        if c.get('img'):
            fig = (f' <figure style="margin:24px 0 0;"><img src="{c["img"]}" alt="{c["alt"]}" width="{c["w"]}" height="{c["h"]}" '
                   f'loading="lazy" decoding="async" style="aspect-ratio:16/10; object-fit:cover; width:100%;"></figure>')
        cols += (f'<div class="choose-col"> <span class="eyebrow">{c["eyebrow"]}</span> <h3>{c["h3"]}</h3> '
                 f'<p class="lead">{c["lead"]}</p>{fig} </div>')
    return f'<section class="section"> <div class="container"> <div class="choose reveal"> {cols} </div> </div> </section>'


def pair(g):
    if not g.get('pair'):
        return ''
    a, b = names(g)
    figs = photo(g['pair'][0], a) + photo(g['pair'][1], b)
    return (f'<section class="section" style="padding-top:0;"> <div class="container"> '
            f'<div class="vs-pair reveal">{figs}</div> </div> </section>')


def comparison(g):
    a, b = names(g)
    pics = {p['after']: p for p in g.get('row_photos', [])}
    body = ''
    for label, ca, cb in g['rows']:
        p = pics.get(plain(label)) or pics.get(label)
        cls = ' class="vs-has-pics"' if p else ''
        body += f'<tr{cls}><td class="rowlabel">{label}</td><td>{ca}</td><td>{cb}</td></tr>'
        if p:
            body += (f'<tr class="vs-pics"><td class="vs-pics-mid" aria-hidden="true"></td>'
                     f'<td>{photo(p["a"], a)}</td><td>{photo(p["b"], b)}</td></tr>')
    foot = (f'<p class="body-2 reveal small" style="margin-top:18px; max-width:62ch;">{g["footnote"]}</p>'
            if g.get('footnote') else '')
    return (f'<section class="section" style="padding-top:0;"> <div class="container"> '
            f'{sec_head("Side by side", "How they <em>compare</em>")} '
            f'<div class="table-wrap vs-compare reveal"> <table> '
            f'<thead><tr><th></th><th>{a}</th><th>{b}</th></tr></thead> <tbody> {body} </tbody> </table> </div> '
            f'{foot} </div> </section>')


def gallery(g):
    if not g.get('gallery'):
        return ''
    nm = dict(zip('ab', names(g)))
    figs = ''.join(photo(p, nm.get(p.get('hotel'))) for p in g['gallery'])
    return (f'<section class="section" style="padding-top:0;"> <div class="container"> '
            f'{sec_head(g.get("gallery_eyebrow", "In pictures"), g.get("gallery_h2", "A closer look"))} '
            f'<div class="vs-gallery reveal">{figs}</div> </div> </section>')


def map_section(g):
    m = g.get('map')
    if not m or 'src' not in m:
        return ''
    pins = ''.join(
        f'<span class="vs-map-pin" data-side="{mk.get("side", "right")}" style="left:{mk["pos"][0]}%; top:{mk["pos"][1]}%;">'
        f'<span class="vs-map-name"><b>{mk["name"]}</b><span>{mk["place"]}</span></span></span>'
        for mk in m['markers'])
    labels = ''.join(
        f'<span class="vs-map-label{" is-water" if lb["kind"] == "water" else ""}" '
        f'style="left:{lb["pos"][0]}%; top:{lb["pos"][1]}%;">{lb["text"]}</span>'
        for lb in m.get('labels', []))
    dist = ''
    if m.get('distance_miles'):
        dist = (f'<span class="vs-map-distance" style="left:{m["distance_pos"][0]}%; top:{m["distance_pos"][1]}%;">'
                f'About {m["distance_miles"]} miles apart</span>')
    intro = f'<p class="body-2 reveal" style="margin:-12px 0 34px; max-width:60ch;">{m["intro"]}</p>' if m.get('intro') else ''
    cap = f'<figcaption>{m["caption"]}</figcaption>' if m.get('caption') else ''
    return (f'<section class="section" style="padding-top:0;"> <div class="container"> '
            f'{sec_head(m.get("eyebrow", "On the map"), m.get("h2", "Where they are"))} {intro}'
            f'<figure class="vs-map reveal"><div class="vs-map-frame" style="aspect-ratio:{m["ratio"]};">'
            f'<img src="{m["src"]}" alt="{m["alt"]}" loading="lazy" decoding="async">'
            f'<div aria-hidden="true">{labels}{dist}{pins}</div></div>{cap}</figure> </div> </section>')


def verdict(g):
    f = g.get('final')
    if f:
        nm = names(g)
        picks = ''.join(
            f'<div class="vs-pick"><span class="eyebrow">{p.get("eyebrow") or "Choose " + nm[i]}</span>'
            f'<h3>{p["h3"]}</h3><p class="body-2">{p["p"]}</p></div>'
            for i, p in enumerate(f['picks']))
        intro = f'<p class="body-2 reveal" style="margin-top:22px; max-width:56ch;">{f["intro"]}</p>' if f.get('intro') else ''
        close = f'<p class="vs-final-close body-2 reveal">{f["close"]}</p>' if f.get('close') else ''
        return (f'<section class="section band on-shadow vs-final" id="verdict"> <div class="container" style="max-width:1000px;"> '
                f'<span class="eyebrow reveal" style="display:block; margin-bottom:16px;">{f.get("eyebrow", "The verdict")}</span> '
                f'<h2 class="display-l reveal">{f.get("h2", "So, which would I book?")}</h2> {intro}'
                f'<div class="vs-final-picks reveal">{picks}</div> {close} </div> </section>')
    v = g['verdict']
    paras = ''.join(f'<p class="body-2 reveal" style="margin-top:22px; max-width:56ch;">{p}</p>' for p in v['paras'])
    return (f'<section class="section band on-shadow"> <div class="container" style="max-width:860px;"> '
            f'<span class="eyebrow reveal" style="display:block; margin-bottom:16px;">The question behind the question</span> '
            f'<h2 class="display-l reveal">{v["h2"]}</h2> {paras} </div> </section>')


def guide(g):
    if not g.get('guide'):
        return ''
    items = ''
    for s in g['guide']:
        if s.get('img2'):
            def fig(src, alt, w, h, cap):
                c = f'<figcaption>{cap}</figcaption>' if cap else ''
                return (f'<figure class="vs-guide-img"><img src="{src}" alt="{alt}" width="{w}" height="{h}" '
                        f'loading="lazy" decoding="async">{c}</figure>')
            img = (f'<div class="vs-guide-pair">{fig(s["img"], s["alt"], s["w"], s["h"], s.get("cap"))}'
                   f'{fig(s["img2"], s["alt2"], s["w2"], s["h2"], s.get("cap2"))}</div>')
        elif s.get('img'):
            img = (f'<figure class="vs-guide-img"><img src="{s["img"]}" alt="{s["alt"]}" width="{s["w"]}" height="{s["h"]}" '
                   f'loading="lazy" decoding="async"></figure>')
        else:
            img = ''
        paras = ''.join(f'<p class="body-2">{p}</p>' for p in s['paras'])
        items += f'<div class="reveal">{img}<h3>{s["h3"]}</h3>{paras}</div>'
    return (f'<section class="section"> <div class="container"> '
            f'{sec_head(g.get("guide_eyebrow", "The detail"), g.get("guide_h2", "What to know before you choose"))} '
            f'<div class="vs-guide">{items}</div> </div> </section>')


def faq(g):
    if not g.get('faq'):
        return ''
    qs = ''.join(f'<details><summary>{q}</summary><p class="body-2">{a}</p></details>' for q, a in g['faq'])
    return (f'<section class="section" style="padding-top:0;"> <div class="container" style="max-width:820px;"> '
            f'{sec_head("Before you ask", "The questions I get")} <div class="vs-faq reveal">{qs}</div> </div> </section>')


def inside(g):
    if not g.get('inside'):
        return ''
    tiles = ''.join(
        f'<a class="vsi-tile" href="{t["href"]}"> <span class="vsi-names">{t["label"]}</span> '
        f'<span class="vsi-q">{t["q"]}</span> <span class="vsi-go">{t.get("cta", "Settle it")} &rarr;</span> </a>'
        for t in g['inside'])
    return (f'<section class="section"> <div class="container"> <div class="sec-head reveal"> <span class="eyebrow">Zoom in</span> '
            f'<h2 class="display-l" style="font-size:clamp(1.792rem,3.584vw,2.576rem);">The decisions inside this one</h2> </div> '
            f'<div class="vsi-grid reveal"> {tiles} </div> </div> </section>')


def inquire(g, slug):
    return (
        '<section class="section inquire" id="inquire"> <div class="container"> '
        '<h2 class="display-l reveal">Still deciding?</h2> '
        '<p class="deck reveal" style="margin:18px auto 0; max-width:42ch;">Tell me your dates and I&rsquo;ll tell you which one fits, and which room to ask for. Book through me for Fora X perks and a hotel that knows you&rsquo;re coming, at the same rate as booking direct.</p> '
        '<form class="inquire-form reveal" action="https://formspree.io/f/mjgnadov" method="POST"> '
        f'<input type="hidden" name="_subject" value="{attr(g["subject"])}"> '
        f'<input type="hidden" name="hotel" value="{attr(g["hotel"])}"> '
        f'<input type="hidden" name="page" value="{slug}"> '
        '<input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off"> '
        '<div class="step1"> <label for="q-when">When are you thinking?</label> '
        f'<input id="q-when" type="text" name="travel_dates" placeholder="{attr(g["placeholder"])}" required autocomplete="off"> </div> '
        '<div class="step2"> <label for="q-name">And where do I send the recommendation?</label> '
        '<input id="q-name" type="text" name="name" placeholder="Name" required autocomplete="name"> '
        '<input id="q-email" type="email" name="email" placeholder="Email" required autocomplete="email"> '
        '<label for="q-details" style="margin-top:2px;">Anything else? Nights, budget, occasion (optional)</label> '
        '<input id="q-details" type="text" name="details" placeholder="7 nights · around $1,500/night · anniversary" autocomplete="off"> </div> '
        '<button type="submit" class="btn" data-gtag-label="versus_inquiry_send" data-gtag-location="versus_cta">Send</button> '
        '<p class="note">Traveling within the next 30 days? You&rsquo;ll hear from me today.</p> '
        '<p class="status" role="status" aria-live="polite"></p> </form> </div> </section>')


def related(g):
    if not g.get('related'):
        return ''
    links = ''.join(f'<a href="{r["href"]}" {LINK_STYLE}><span>{r["label"]}</span>&nbsp;&rarr;</a>' for r in g['related'])
    return (f'<section class="section vs-related"> <div class="container"> '
            f'<span class="eyebrow reveal" style="display:block; margin-bottom:22px;">Keep reading</span> '
            f'<p class="vs-related-links reveal">{links}</p> </div> </section>')


def body(g, slug):
    return '  '.join(x for x in (
        header(g), choose(g), pair(g), comparison(g), gallery(g), map_section(g), verdict(g),
        guide(g), faq(g), inside(g), inquire(g, slug), related(g)) if x)


# ── head ────────────────────────────────────────────────────────────────────
def uses_new_sections(g):
    return any(g.get(k) for k in ('pair', 'row_photos', 'gallery', 'map', 'final'))


def head(shell_head, g, slug):
    h = shell_head
    url = f'https://suiteswithkeith.com/{slug}.html'
    title, desc = attr(g['title']), attr(g['description'])
    h = re.sub(r'<title>.*?</title>', lambda _: f'<title>{title}</title>', h, flags=re.S)
    h = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*"', lambda m: m.group(1) + desc + '"', h)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + title + '"', h)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*"', lambda m: m.group(1) + url + '"', h)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*"', lambda m: m.group(1) + url + '"', h)
    image = g.get('ld_image') or g.get('preload')
    if g.get('preload'):
        h = re.sub(r'(<link rel="preload" as="image" href=")[^"]*"', lambda m: m.group(1) + g['preload'] + '"', h)

    def ld(m):
        d = json.loads(m.group(1))
        if d.get('@type') != 'Article':
            return m.group(0)
        d['headline'] = g['title'].split('|')[0].strip()
        d['description'] = g['description']
        if image:
            d['image'] = 'https://suiteswithkeith.com' + image
        d['mainEntityOfPage'] = {'@type': 'WebPage', '@id': url}
        return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + '</script>'
    h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, h, flags=re.S)

    css = '<link rel="stylesheet" href="/versus.css">'
    if uses_new_sections(g) and css not in h:
        h = h.replace('</head>', css + '</head>') if '</head>' in h else h + css
    return h


def render(slug, versus):
    g = versus[slug]
    path = f'{ROOT}/{slug}.html'
    shell = open(path if os.path.exists(path) else f'{ROOT}/{REF_SLUG}.html').read()
    i = shell.index('</nav>') + len('</nav>')
    j = shell.index('<footer')
    hi = shell.index('</head>')
    out = head(shell[:hi + 7], g, slug) + shell[hi + 7:i] + '  ' + body(g, slug) + '  ' + shell[j:]
    if not os.path.exists(path):
        # a new page copies the reference shell: swap the reference slug wherever the shell names it
        out = out.replace(f'/{REF_SLUG}.html', f'/{slug}.html')
    open(path, 'w').write(out)
    print('wrote', f'{slug}.html', f'({len(out) // 1024} KB)')


if __name__ == '__main__':
    versus = json.load(open(f'{ROOT}/phase1/src/data/versus.json'))
    for slug in sys.argv[1:]:
        render(slug, versus)
