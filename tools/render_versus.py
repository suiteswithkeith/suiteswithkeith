#!/usr/bin/env python3
"""Render a head-to-head page (<slug>.html at the site root) from versus.json,
using four-seasons-astir-palace-vs-one-and-only-aesthesis.html as the fixed
skeleton (head/nav/form/footer copied verbatim, entry content substituted).

Usage: python3 tools/render_versus.py <slug> [<slug> ...]

Notes on escaping, matching the deployed Astro output:
- title/description/subject/hotel are PLAIN text in versus.json (raw &, real
  em dashes); they render with & as &amp; in text nodes and &#38; in attributes.
- Every other field is already entity-encoded HTML and is injected verbatim.
- The Astro layout emits "image":"https://suiteswithkeith.comundefined" in the
  JSON-LD (no image field); this renderer accepts an optional "ld_image" in the
  entry to emit a real image instead.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL_SLUG = 'four-seasons-astir-palace-vs-one-and-only-aesthesis'

tpl = open(f'{ROOT}/{TPL_SLUG}.html').read()
versus = json.load(open(f'{ROOT}/phase1/src/data/versus.json'))
T = versus[TPL_SLUG]

def esc_text(s):
    return s.replace('&', '&amp;')

def esc_attr(s):
    return s.replace('&', '&#38;')

def build(v, slug):
    url = f"https://suiteswithkeith.com/{slug}.html"
    headline = v['title'].split(' | ')[0]
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": headline,
        "description": v['description'],
        "image": "https://suiteswithkeith.com" + v.get('ld_image', 'undefined'),
        "author": {"@type": "Person", "name": "Keith Pence"},
        "publisher": {"@type": "Organization", "name": "Suites With Keith",
                      "logo": {"@type": "ImageObject", "url": "https://suiteswithkeith.com/favicon-32.png"}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url}
    }, ensure_ascii=False, separators=(',', ':'))

    choose = ''.join(
        f'<div class="choose-col"> <span class="eyebrow">{c["eyebrow"]}</span> <h3>{c["h3"]}</h3> '
        f'<p class="lead">{c["lead"]}</p>  </div>'
        for c in v['choose'])

    th_a, th_b = v['h1_a'], v['h1_b'].rstrip('?')
    thead = f'<thead><tr><th></th><th>{th_a}</th><th>{th_b}</th></tr></thead>'
    rows = ''.join(
        f'<tr><td class="rowlabel">{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>'
        for r in v['rows'])

    paras = ''.join(
        f'<p class="body-2 reveal" style="margin-top:22px; max-width:56ch;">{p}</p>'
        for p in v['verdict']['paras'])

    related = ''.join(
        f'<a href="{r["href"]}" style="font-size:.72rem; font-weight:500; letter-spacing:.14em; '
        f'text-transform:uppercase; color:var(--brass); text-decoration:none;"><span>{r["label"]}</span> &rarr;</a>'
        for r in v['related'])

    return dict(url=url, ld=ld, choose=choose, thead=thead, rows=rows,
                paras=paras, related=related)

def render(slug):
    v = versus[slug]
    b = build(v, slug)
    t = build(T, TPL_SLUG)
    out = tpl

    def swap(old, new, count=0):
        nonlocal out
        n = out.count(old)
        assert n >= 1, f"anchor not found: {old[:90]!r}"
        if count:
            assert n == count, f"anchor count {n} != {count}: {old[:90]!r}"
        out = out.replace(old, new)

    # head
    swap(f'<title>{esc_text(T["title"])}</title>', f'<title>{esc_text(v["title"])}</title>')
    swap(f'content="{esc_attr(T["description"])}"', f'content="{esc_attr(v["description"])}"', 2)
    swap(f'content="{esc_attr(T["title"])}"', f'content="{esc_attr(v["title"])}"')
    swap(f'href="https://suiteswithkeith.com/{TPL_SLUG}.html"', f'href="{b["url"]}"')
    swap(f'content="https://suiteswithkeith.com/{TPL_SLUG}.html"', f'content="{b["url"]}"')
    swap(t['ld'], b['ld'])

    # header
    swap(f'<p class="eyebrow reveal">{T["eyebrow"]}</p>', f'<p class="eyebrow reveal">{v["eyebrow"]}</p>')
    swap(f'<span>{T["h1_a"]}</span> or <em style="font-style:italic; color:var(--brass);">{T["h1_b"]}</em>',
         f'<span>{v["h1_a"]}</span> or <em style="font-style:italic; color:var(--brass);">{v["h1_b"]}</em>')
    swap(f'max-width:48ch;">{T["deck"]}</p>', f'max-width:48ch;">{v["deck"]}</p>')
    swap(f'margin-top:26px;">{T["stamp"]}</p>', f'margin-top:26px;">{v["stamp"]}</p>')

    # choose columns, table, footnote
    swap(t['choose'], b['choose'])
    swap(t['thead'], b['thead'])
    swap(t['rows'], b['rows'])
    swap(f'max-width:62ch;">{T["footnote"]}</p>', f'max-width:62ch;">{v["footnote"]}</p>')

    # verdict band
    swap(f'<h2 class="display-l reveal">{T["verdict"]["h2"]}</h2>',
         f'<h2 class="display-l reveal">{v["verdict"]["h2"]}</h2>')
    swap(t['paras'], b['paras'])

    # form
    swap(f'name="_subject" value="{esc_attr(T["subject"])}"', f'name="_subject" value="{esc_attr(v["subject"])}"')
    swap(f'name="hotel" value="{esc_attr(T["hotel"])}"', f'name="hotel" value="{esc_attr(v["hotel"])}"')
    swap(f'name="page" value="{TPL_SLUG}"', f'name="page" value="{slug}"')
    swap(f'placeholder="{T["placeholder"]}" required', f'placeholder="{v["placeholder"]}" required')

    # related links
    swap(t['related'], b['related'])

    path = f'{ROOT}/{slug}.html'
    open(path, 'w').write(out)
    print('wrote', path, len(out), 'bytes')

for slug in sys.argv[1:]:
    render(slug)
