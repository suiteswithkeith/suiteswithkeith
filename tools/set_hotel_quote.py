#!/usr/bin/env python3
"""Give a hotel review page its own client quote in the "Book … through me" band,
replacing the default (Carla's note).

Updates both the built page (hotels/<slug>.html) and the source data
(phase1/src/data/hotels.json → quote_html / quote_cite_html, read by
phase1/src/pages/hotels/[slug].astro), so a rebuild keeps it.

Usage:
  python3 tools/set_hotel_quote.py <slug> "<quote text>" "<Name> · <Hotel>" [--fora]

The quote is plain text (curly quotes are added). --fora appends a
"Verified review on Fora" link to Keith's Fora profile.
"""
import html, json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORA = 'https://www.foratravel.com/advisor/keith-pence'


def encode(s):
    s = html.escape(s, quote=False)
    return s.replace("'", '&rsquo;').replace('·', '&middot;')


def set_quote(slug, text, cite, fora):
    q = '&ldquo;' + encode(text) + '&rdquo;'
    c = encode(cite)
    if fora:
        c += (' &middot; <a href="' + FORA + '" target="_blank" rel="noopener" '
              'style="color:inherit;">Verified review on Fora</a>')

    page = f'{ROOT}/hotels/{slug}.html'
    t = open(page).read()
    t, n = re.subn(
        r'(<figure class="swk-quote[^>]*><blockquote[^>]*>).*?(</blockquote><figcaption[^>]*>).*?(</figcaption>)',
        lambda m: m.group(1) + q + m.group(2) + c + m.group(3), t, count=1, flags=re.S)
    if n != 1:
        sys.exit(f'no quote block in {page}')
    open(page, 'w').write(t)

    # source data: edit in place so the file's formatting is untouched
    data_path = f'{ROOT}/phase1/src/data/hotels.json'
    s = open(data_path).read()
    key = f'  "slug": "{slug}",\n'
    if s.count(key) != 1:
        print(f'note: {slug} not in hotels.json; built page updated only')
    else:
        s = re.sub(r'(  "slug": "' + re.escape(slug) + r'",\n)(  "quote_html": .*\n  "quote_cite_html": .*\n)?',
                   lambda m: m.group(1) + '  "quote_html": ' + json.dumps(q, ensure_ascii=False) + ',\n'
                   + '  "quote_cite_html": ' + json.dumps(c, ensure_ascii=False) + ',\n', s, count=1)
        json.loads(s)
        open(data_path, 'w').write(s)
    print('set', slug)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--fora']
    if len(args) != 3:
        sys.exit(__doc__)
    set_quote(args[0], args[1], args[2], '--fora' in sys.argv)
