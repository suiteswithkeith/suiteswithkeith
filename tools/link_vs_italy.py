#!/usr/bin/env python3
"""Cross-link the Italy head-to-head pages (Amalfi Coast, Rome, Dolomites, Venice,
Lake Como). Idempotent; rerun after adding a vs page.

- Each hotel review gets a "The head-to-heads" list (id="head-to-heads") of every
  vs page that compares it, inserted before the booking band (rebuilt if present).
- Each hub page gets a tile for every vs page in its region: existing tiles are
  kept as written, missing ones are appended (Rome and the Dolomites get the
  section created after their hotel list).
- sitemap.xml gets an entry for any vs page it is missing.

Usage: python3 tools/link_vs_italy.py
"""
import glob, html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LASTMOD = '2026-10-27'

REGIONS = {
    'positano-hotels.html': ['hotel-santa-caterina-amalfi', 'il-san-pietro-di-positano', 'le-sirenuse-positano',
                             'villa-treville-positano', 'borgo-santandrea-amalfi'],
    'rome.html': ['hotel-eden-rome', 'orient-express-la-minerva-rome', 'hotel-de-russie-rome', 'hassler-roma',
                  'bulgari-hotel-rome', 'corinthia-rome', 'hotel-de-la-ville-rome', 'casa-monti-rome'],
    'dolomites.html': ['forestis-dolomites', 'aman-rosa-alpina-dolomites', 'como-alpina-dolomites',
                       'gardena-grodnerhof-ortisei', 'miramonti-merano'],
    'venice.html': ['aman-venice', 'airelles-palladio-venice', 'danieli-four-seasons-venice', 'orient-express-venice'],
    'lake-como.html': ['grand-hotel-tremezzo-lake-como', 'il-sereno-lake-como', 'lake-como-edition',
                       'passalacqua-lake-como', 'villa-d-este-lake-como', 'villa-serbelloni-bellagio'],
}
# where a new hub section goes when the hub has none yet
HUB_ANCHOR = {'rome.html': '<section class="section" id="know"',
              'dolomites.html': '<section class="section" id="when"'}


def read(p):
    return open(f'{ROOT}/{p}').read()


def write(p, s):
    open(f'{ROOT}/{p}', 'w').write(s)


def plain(h):
    return html.unescape(re.sub(r'<[^>]+>', '', h)).strip()


def load_versus():
    """slug -> dict(hotels=[file, file], a, b, teaser)"""
    out = {}
    for path in sorted(glob.glob(f'{ROOT}/*-vs-*.html')):
        slug = os.path.basename(path)[:-5]
        s = open(path).read()
        thead = re.search(r'<thead>(.*?)</thead>', s, re.S)
        hotels = re.findall(r'href="/hotels/([a-z0-9-]+)\.html"', thead.group(1)) if thead else []
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
        if len(hotels) != 2 or not h1:
            continue
        names = plain(h1.group(1)).rstrip('?')
        if ' or ' not in names:
            continue
        a, b = names.split(' or ', 1)
        band = re.search(r'The question behind the question</span>\s*<h2[^>]*>(.*?)</h2>', s, re.S)
        sub = re.search(r'<p class="sub"[^>]*>(.*?)</p>', s, re.S)
        teaser = (band or sub).group(1).strip()
        out[slug] = dict(hotels=hotels, a=a.strip(), b=b.strip(), teaser=teaser)
    return out


def ent(t):
    return html.escape(t, quote=False).replace('’', '&rsquo;').replace("'", '&rsquo;')


def hotel_section(rows):
    items = ''.join(
        f'<div class="kv-row"><dt>{i:02d}</dt><dd><b><a href="/{slug}.html">{ent(v["a"])} <em>or</em> {ent(v["b"])}</a></b> '
        f'<span class="body-2">{v["teaser"]} <a href="/{slug}.html">Settle it &rarr;</a></span></dd></div>'
        for i, (slug, v) in enumerate(rows, 1))
    return ('<section class="section" id="head-to-heads"><div class="container"><div class="sec-head reveal">'
            '<span class="eyebrow">Torn between two?</span><h2 class="display-l">The head-to-heads</h2></div>'
            f'<dl class="kv reveal">{items}</dl></div></section>')


def tile(slug, v):
    return (f'<a class="vsi-tile" href="/{slug}.html"><span class="vsi-names">{ent(v["a"])} <em>or</em> {ent(v["b"])}</span>'
            f'<span class="vsi-q">{v["teaser"]}</span><span class="vsi-go">Settle it &rarr;</span></a>')


def link_hotels(versus):
    for hub, files in REGIONS.items():
        for f in files:
            p = f'hotels/{f}.html'
            rows = [(slug, v) for slug, v in versus.items() if f in v['hotels']]
            rows.sort(key=lambda r: max(files.index(h) if h in files else 99 for h in r[1]['hotels'] if h != f))
            if not rows:
                continue
            s = read(p)
            # keep teasers already written on this page
            old = re.search(r'<section class="section" id="head-to-heads">.*?</section>', s, re.S)
            kept = {} if not old else {
                m.group(1): m.group(2) for m in re.finditer(
                    r'<b><a href="/([a-z0-9-]+)\.html">.*?<span class="body-2">(.*?) <a href="/[a-z0-9-]+\.html">Settle it',
                    old.group(0))}
            rows = [(slug, dict(v, teaser=kept.get(slug, v['teaser']))) for slug, v in rows]
            s = re.sub(r'<section class="section" id="head-to-heads">.*?</section>\s*', '', s, flags=re.S)
            m = list(re.finditer(r'<section class="section band on-shadow">', s))
            inq = s.find('<section class="section inquire"')
            anchor = [x.start() for x in m if x.start() < inq][-1] if m else inq
            s = s[:anchor] + hotel_section(rows) + '\n' + s[anchor:]
            write(p, s)


def link_hubs(versus):
    for hub, files in REGIONS.items():
        s = read(hub)
        mine = [(slug, v) for slug, v in versus.items() if set(v['hotels']) <= set(files)]
        # region lists run in Keith's order of preference
        mine.sort(key=lambda r: sorted(files.index(h) for h in r[1]['hotels']))
        if 'id="head-to-heads"' not in s:
            sec = ('<section class="section" id="head-to-heads" style="padding-top:0; scroll-margin-top:70px;"><div class="container">\n'
                   '<div class="sec-head reveal"><span class="eyebrow">Torn between two?</span><h2 class="display-l">The head-to-heads</h2></div>\n'
                   '<div class="vsi-grid reveal">\n</div>\n</div></section>\n')
            i = s.find(HUB_ANCHOR[hub])
            assert i > 0, hub
            s = s[:i] + sec + s[i:]
        start = s.find('id="head-to-heads"')
        g = s.find('<div class="vsi-grid', start)
        end = s.find('</div>', g)
        assert g > 0 and end > g, hub
        grid = s[g:end]
        add = ''.join(tile(slug, v) for slug, v in mine if f'href="/{slug}.html"' not in grid)
        s = s[:end] + add + s[end:]
        write(hub, s)


def link_sitemap(versus):
    s = read('sitemap.xml')
    add = ''.join(f'  <url>\n    <loc>https://suiteswithkeith.com/{slug}.html</loc>\n    <lastmod>{LASTMOD}</lastmod>\n  </url>\n'
                  for slug in versus if f'/{slug}.html<' not in s)
    write('sitemap.xml', s.replace('</urlset>', add + '</urlset>'))


if __name__ == '__main__':
    v = load_versus()
    link_hotels(v)
    link_hubs(v)
    link_sitemap(v)
    print(f'linked {len(v)} vs pages')
