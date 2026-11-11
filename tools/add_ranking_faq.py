#!/usr/bin/env python3
"""Add (or refresh) the FAQ section + FAQPage schema on the ranking pages.

Data: phase1/src/data/rankingfaqs.json, keyed by page slug, each with a
"title" and a "faq" list of [question, answer_html] pairs.

  python3 tools/add_ranking_faq.py            # every page in the JSON
  python3 tools/add_ranking_faq.py napa-sonoma

Idempotent: everything it writes sits between <!-- swk-faq --> markers and is
replaced on rerun. The section goes right before the #inquire band, and an
"FAQ" link is added to the page's "On this page" row when it has one.
Same markup and CSS as the FAQ on amalfi-coast.html (.vs-faq accordion).
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "phase1/src/data/rankingfaqs.json"

CSS = ('.vs-faq details{border-top:1px solid var(--hairline);padding:18px 0}'
       '.vs-faq details:last-child{border-bottom:1px solid var(--hairline)}'
       '.vs-faq summary{cursor:pointer;font-family:var(--display);font-size:1.344rem;list-style:none;position:relative;padding-right:28px}'
       '.vs-faq summary::-webkit-details-marker{display:none}'
       '.vs-faq summary::after{content:"+";position:absolute;right:0;top:0;color:var(--brass);font-family:var(--body)}'
       '.vs-faq details[open] summary::after{content:"\\2013"}'
       '.vs-faq details p{margin-top:12px;max-width:62ch}')


def plain(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def strip_old(s):
    s = re.sub(r"<!-- swk-faq-head -->.*?<!-- /swk-faq-head -->", "", s, flags=re.S)
    s = re.sub(r"<!-- swk-faq -->.*?<!-- /swk-faq -->", "", s, flags=re.S)
    s = re.sub(r"<!-- swk-faq-toc -->.*?<!-- /swk-faq-toc -->", "", s, flags=re.S)
    return s


def render(slug, entry):
    path = ROOT / f"{slug}.html"
    s = strip_old(path.read_text())
    faq = entry["faq"]
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
        for q, a in faq]}
    head = ('<!-- swk-faq-head --><script type="application/ld+json">'
            + json.dumps(schema, ensure_ascii=False).replace("</", "<\\/")
            + f'</script><style>{CSS}</style><!-- /swk-faq-head -->')
    items = "".join(f'<details><summary>{q}</summary><p class="body-2">{a}</p></details>' for q, a in faq)
    section = ('<!-- swk-faq --><section class="section" id="faq" style="scroll-margin-top:70px;">'
               '<div class="container" style="max-width:820px;">'
               '<div class="sec-head reveal"><span class="eyebrow">Before you ask</span>'
               f'<h2 class="display-l">{entry["title"]}</h2></div>'
               f'<div class="vs-faq reveal">{items}</div></div></section><!-- /swk-faq -->')

    assert s.count("</head>") == 1, slug
    s = s.replace("</head>", head + "</head>", 1)
    anchor = '<section class="section inquire band on-shadow" id="inquire"'
    assert s.count(anchor) == 1, f"{slug}: inquire anchor"
    s = s.replace(anchor, section + anchor, 1)

    # "On this page" row: copy the first #inquire toc-link (keeps the Astro cid attrs)
    m = re.search(r'<a class="toc-link" href="#inquire"([^>]*)><span([^>]*)>[^<]*</span>(&nbsp;)?&rarr;</a>', s)
    if m:
        link = f'<!-- swk-faq-toc --><a class="toc-link" href="#faq"{m.group(1)}><span{m.group(2)}>FAQ</span>{m.group(3) or ""}&rarr;</a> <!-- /swk-faq-toc -->'
        s = s[:m.start()] + link + s[m.start():]
    path.write_text(s)
    print(f"{slug}: {len(faq)} questions{'' if m else ' (no on-this-page row)'}")


def main():
    data = json.loads(DATA.read_text())
    for slug in sys.argv[1:] or data:
        render(slug, data[slug])


if __name__ == "__main__":
    main()
