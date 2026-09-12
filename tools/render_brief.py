#!/usr/bin/env python3
"""Render a hotel brief page (hotels/<slug>.html) from hotelbriefs.json,
using hotels/onero-milos.html as the fixed skeleton (head/style/nav/form/footer
copied verbatim, brief-specific content substituted)."""
import json, sys, re

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL_SLUG = 'onero-milos'

tpl = open(f'{ROOT}/hotels/{TPL_SLUG}.html').read()
briefs = json.load(open(f'{ROOT}/phase1/src/data/hotelbriefs.json'))
T = briefs[TPL_SLUG]

def esc_attr(s):
    return s

def build_variable_parts(b):
    slug = b['slug']
    url = f"https://suiteswithkeith.com/hotels/{slug}.html"
    headline = b['title'].split(' | ')[0]
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": headline,
        "description": b['description'],
        "image": "https://suiteswithkeith.com" + b['hero_img'],
        "author": {"@type": "Person", "name": "Keith Pence"},
        "publisher": {"@type": "Organization", "name": "Suites With Keith",
                      "logo": {"@type": "ImageObject", "url": "https://suiteswithkeith.com/favicon-32.png"}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url}
    }, ensure_ascii=False, separators=(',', ':'))

    stats = ' &nbsp;&middot;&nbsp; '.join(f"<b>{s['num']}</b> {s['label']}" for s in b['stats'])

    paras = b['intro_paras']
    deck = f'<p class="deck" style="max-width:48ch;">{paras[0]}</p>'
    body = ''.join(f'<p class="body-2 hb-p" style="margin-top:16px; max-width:58ch;">{p}</p>' for p in paras[1:])

    kv = ''.join(f'<div class="kv-row"><dt>{g["label"]}</dt><dd class="hb-dd">{g["html"]}</dd></div>' for g in b['glance'])

    def notes_html(notes):
        return ''.join(f'<p class="hb-note"><b>{n["b"]}</b> <span>{n["t"]}</span></p>' for n in notes)

    s0, s1 = b['sections']
    col0 = (f'<p class="stamp plain" style="font-weight:700; color:var(--brass-lit); margin-bottom:8px;">{s0["kicker"]}</p> '
            f'<h2 class="display-l" style="font-size:clamp(1.5rem,2.6vw,2rem); margin-bottom:20px;">{s0["h3"]}</h2> '
            f'{notes_html(s0["notes"])}')
    take = f' <div class="verdict" style="margin-top:24px; border-left-color:var(--brass-lit);"><p class="hb-take">{s1["take"]}</p></div>' if s1.get('take') else ''
    col1 = (f'<p class="stamp plain" style="font-weight:700; color:var(--brass-lit); margin-bottom:8px;">{s1["kicker"]}</p> '
            f'<h2 class="display-l" style="font-size:clamp(1.5rem,2.6vw,2rem); margin-bottom:20px;">{s1["h3"]}</h2> '
            f'{notes_html(s1["notes"])}{take}')

    related = ''.join(
        f'<a href="{r["href"]}" style="font-size:.72rem; font-weight:500; letter-spacing:.14em; text-transform:uppercase; '
        f'color:var(--brass); text-decoration:none;"><span>{r["label"]}</span> &rarr;</a>'
        for r in b['related'])

    return dict(url=url, ld=ld, stats=stats, deck=deck, body=body, kv=kv,
                col0=col0, col1=col1, related=related)

def render(slug):
    b = briefs[slug]
    v = build_variable_parts(b)
    t = build_variable_parts(T)
    out = tpl

    def swap(old, new, count=0):
        nonlocal out
        n = out.count(old)
        assert n >= 1, f"anchor not found: {old[:90]!r}"
        if count:
            assert n == count, f"anchor count {n} != {count}: {old[:90]!r}"
        out = out.replace(old, new)

    # head
    swap(f'<title>{T["title"]}</title>', f'<title>{b["title"]}</title>')
    swap(f'content="{T["description"]}"', f'content="{b["description"]}"', 2)
    swap(f'content="{T["title"]}"', f'content="{b["title"]}"')
    swap(f'href="https://suiteswithkeith.com/hotels/{TPL_SLUG}.html"', f'href="{v["url"]}"')
    swap(f'content="https://suiteswithkeith.com/hotels/{TPL_SLUG}.html"', f'content="{v["url"]}"')
    swap(t['ld'], v['ld'])
    swap(f'href="{T["hero_img"]}" fetchpriority', f'href="{b["hero_img"]}" fetchpriority')

    # hero
    swap(f'src="{T["hero_img"]}" alt=""', f'src="{b["hero_img"]}" alt=""')
    if not b.get('hero_scrim'):
        out = re.sub(r'<div style="position:absolute; inset:0; z-index:1; background:linear-gradient[^>]*></div>', '', out)
    swap(f'<p class="eyebrow">{T["eyebrow"]}</p>', f'<p class="eyebrow">{b["eyebrow"]}</p>')
    swap(f'style="margin-top:18px;">{T["h1"]}</h1>', f'style="margin-top:18px;">{b["h1"]}</h1>')
    swap(f'<p class="sub">{T["tagline"]}</p>', f'<p class="sub">{b["tagline"]}</p>')
    swap(f'<p class="hb-stats">{t["stats"]}</p>', f'<p class="hb-stats">{v["stats"]}</p>')

    # intro + glance
    swap(t['deck'], v['deck'])
    swap(t['body'], v['body'])
    swap(t['kv'], v['kv'])

    # extra photos section (template has one; replace or drop)
    swap(f' {T["extra_html"]} ', f' {b["extra_html"]} ' if b.get('extra_html') else ' ')

    # band columns
    swap(t['col0'], v['col0'])
    swap(t['col1'], v['col1'])

    # perks
    swap(f'>{T["perks_eyebrow"]}</span>', f'>{b["perks_eyebrow"]}</span>')
    swap(f'<h3 class="display-m">{T["perks_h3"]}</h3>', f'<h3 class="display-m">{b["perks_h3"]}</h3>')
    swap(f'style="margin-top:12px;">{T["perks_p"]}</p>', f'style="margin-top:12px;">{b["perks_p"]}</p>')

    # cta / form
    swap(f'margin-bottom:16px;">{T["cta_eyebrow"]}</span>', f'margin-bottom:16px;">{b["cta_eyebrow"]}</span>')
    swap(f'font-size:clamp(1.6rem,3vw,2.3rem);">{T["cta_h2"]}</h2>', f'font-size:clamp(1.6rem,3vw,2.3rem);">{b["cta_h2"]}</h2>')
    swap(f'name="_subject" value="{T["subject"]}"', f'name="_subject" value="{b["subject"]}"')
    swap(f'name="hotel" value="{T["hotel_name"]}"', f'name="hotel" value="{b["hotel_name"]}"')
    swap(f'name="page" value="hotels/{TPL_SLUG}.html"', f'name="page" value="hotels/{slug}.html"')
    swap(f'placeholder="{T["placeholder"]}" required', f'placeholder="{b["placeholder"]}" required')

    # related links
    swap(t['related'], v['related'])

    path = f'{ROOT}/hotels/{slug}.html'
    open(path, 'w').write(out)
    # sanity: no template-hotel leftovers
    plain = re.sub(r'<[^>]+>', ' ', out)
    for leftover in ['Onero', 'Milos', 'Parasporos', 'Adamas']:
        if leftover in plain:
            print(f'  WARNING: leftover {leftover!r} in {slug}')
    print('wrote', path, len(out), 'bytes')

for slug in sys.argv[1:]:
    render(slug)
