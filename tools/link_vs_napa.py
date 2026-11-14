#!/usr/bin/env python3
"""Cross-link the Napa & Sonoma head-to-head pages. Idempotent; rerun after
adding a vs page (add it to PAGES first).

- Each hotel review gets a "The head-to-heads" list (id="head-to-heads") of
  every vs page that compares it, inserted before the booking band.
- napa-sonoma.html gets a tile for any vs page its head-to-heads grid is missing.
- sitemap.xml gets an entry for any vs page it is missing.

Usage: python3 tools/link_vs_napa.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LASTMOD = '2026-11-14'

# review file slugs, in Keith's Napa & Sonoma order (Auberge after the ranked nine)
ORDER = ['meadowood-napa-valley', 'four-seasons-napa-valley', 'montage-healdsburg', 'solage-calistoga',
         'macarthur-place-sonoma', 'stanly-ranch-napa', 'madrona-manor-healdsburg', 'carneros-resort-napa',
         'alila-napa-valley', 'auberge-du-soleil-napa']
NAME = {'meadowood-napa-valley': 'Meadowood', 'four-seasons-napa-valley': 'Four Seasons',
        'montage-healdsburg': 'Montage Healdsburg', 'solage-calistoga': 'Solage',
        'stanly-ranch-napa': 'Stanly Ranch', 'carneros-resort-napa': 'Carneros',
        'auberge-du-soleil-napa': 'Auberge du Soleil'}

# vs page -> (hotel a, hotel b, teaser)
PAGES = {
    'meadowood-vs-four-seasons-napa-valley': ('meadowood-napa-valley', 'four-seasons-napa-valley',
        'My #01 and #02. The benchmark or the all-rounder?'),
    'auberge-du-soleil-vs-meadowood': ('auberge-du-soleil-napa', 'meadowood-napa-valley',
        'Napa&rsquo;s two classics. The most romantic dinner, or the best service?'),
    'meadowood-vs-stanly-ranch': ('meadowood-napa-valley', 'stanly-ranch-napa',
        'The estate that sets the service bar, or the valley&rsquo;s boldest design statement.'),
    'solage-vs-four-seasons-napa-valley': ('solage-calistoga', 'four-seasons-napa-valley',
        'The Calistoga question: the design icon or the five-star apparatus.'),
    'four-seasons-napa-valley-vs-montage-healdsburg': ('four-seasons-napa-valley', 'montage-healdsburg',
        'The cross-valley call. The group trip or the two of you?'),
    'auberge-du-soleil-vs-montage-healdsburg': ('auberge-du-soleil-napa', 'montage-healdsburg',
        'My two favorite wine-country honeymoon hotels. Napa or Sonoma?'),
    'auberge-du-soleil-vs-stanly-ranch': ('auberge-du-soleil-napa', 'stanly-ranch-napa',
        'Two Auberge resorts. A romantic escape, or a contemporary resort?'),
    'carneros-resort-vs-stanly-ranch': ('carneros-resort-napa', 'stanly-ranch-napa',
        'The southern gateway. The postcard or the statement?'),
}


def read(p):
    return open(f'{ROOT}/{p}').read()


def write(p, s):
    open(f'{ROOT}/{p}', 'w').write(s)


def hotel_section(f):
    rows = [(slug, a, b, q) for slug, (a, b, q) in PAGES.items() if f in (a, b)]
    rows.sort(key=lambda r: ORDER.index(r[2] if r[1] == f else r[1]))
    items = ''.join(
        f'<div class="kv-row"><dt>{i:02d}</dt><dd><b><a href="/{slug}.html">{NAME[a]} <em>or</em> {NAME[b]}</a></b> '
        f'<span class="body-2">{q} <a href="/{slug}.html">Settle it &rarr;</a></span></dd></div>'
        for i, (slug, a, b, q) in enumerate(rows, 1))
    if not rows:
        return ''
    return ('<section class="section" id="head-to-heads"><div class="container"><div class="sec-head reveal">'
            '<span class="eyebrow">Torn between two?</span><h2 class="display-l">The head-to-heads</h2></div>'
            f'<dl class="kv reveal">{items}</dl></div></section>')


def link_hotels():
    for f in ORDER:
        p = f'hotels/{f}.html'
        sec = hotel_section(f)
        if not sec:
            continue
        s = read(p)
        s = re.sub(r'<section class="section" id="head-to-heads">.*?</section>\s*', '', s, flags=re.S)
        inq = s.find('<section class="section inquire"')
        bands = [m.start() for m in re.finditer(r'<section class="section band on-shadow">', s) if m.start() < inq]
        anchor = bands[-1] if bands else inq
        assert anchor > 0, p
        write(p, s[:anchor] + sec + '\n' + s[anchor:])


def link_hub():
    s = read('napa-sonoma.html')
    cid = 'data-astro-cid-slg2l3tr'
    tiles = [m.start() for m in re.finditer(r'<a class="vs-tile" href="/[a-z0-9-]+-vs-[a-z0-9-]+\.html"', s)]
    assert tiles
    end = s.find('</a>', tiles[-1]) + len('</a>')
    add = ''
    for slug, (a, b, q) in PAGES.items():
        if f'class="vs-tile" href="/{slug}.html"' in s:
            continue
        add += (f'<a class="vs-tile" href="/{slug}.html" {cid}> <span class="vs-names" {cid}><span {cid}>{NAME[a]}</span> '
                f'<em {cid}>or</em> <span {cid}>{NAME[b]}</span></span> <span class="vs-q" {cid}>{q}</span> '
                f'<span class="vs-go" {cid}>Settle it &rarr;</span> </a>')
    write('napa-sonoma.html', s[:end] + add + s[end:])


def link_sitemap():
    s = read('sitemap.xml')
    add = ''.join(f'  <url>\n    <loc>https://suiteswithkeith.com/{slug}.html</loc>\n    <lastmod>{LASTMOD}</lastmod>\n  </url>\n'
                  for slug in PAGES if f'/{slug}.html<' not in s)
    write('sitemap.xml', s.replace('</urlset>', add + '</urlset>'))


if __name__ == '__main__':
    link_hotels()
    link_hub()
    link_sitemap()
    print(f'linked {len(PAGES)} Napa & Sonoma vs pages')
