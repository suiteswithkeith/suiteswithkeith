#!/usr/bin/env python3
"""Insert a "Doors I can open" section into an Italy destination page.

Content lives in tools/doors/<slug>.json:
    {
      "title": "Doors I can open in Rome",        # optional
      "deck": "One line under the heading.",       # optional
      "doors": [ {"h": "Short name", "p": "Two or three sentences."}, ... ],
      "replaces": ["do"]                            # optional: section ids to remove
    }

The section goes right after the "Where I'd stay" (#hotels) section, wrapped in
<!-- doors:start --> / <!-- doors:end --> so re-running replaces it in place.
No partner names, no prices: this is what Keith can arrange, in his voice.

Usage:
    python3 tools/render_doors.py rome            # writes rome.html
    python3 tools/render_doors.py rome --out x.html
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- doors:start -->", "<!-- doors:end -->"

NAMES = {
    "rome": "Rome",
    "florence": "Florence",
    "venice": "Venice",
    "amalfi-coast": "the Amalfi Coast",
    "lake-como": "Lake Como",
    "tuscany": "Tuscany",
    "dolomites": "the Dolomites",
}

CSS = """<style>
#doors .doors-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));margin-top:40px;border-top:1px solid var(--band-hairline);border-left:1px solid var(--band-hairline)}
#doors .door{border-right:1px solid var(--band-hairline);border-bottom:1px solid var(--band-hairline);padding:28px 24px 30px;display:flex;flex-direction:column;gap:12px}
#doors .door-n{font-family:var(--stamp);font-size:13px;letter-spacing:.2em;text-transform:uppercase;color:var(--brass-lit)}
#doors .door h3{margin:0;font-family:var(--display);font-weight:400;font-size:1.42rem;line-height:1.2;color:var(--band-ink)}
#doors .door p{margin:0;font-size:.95rem;line-height:1.6;color:var(--band-ash);text-wrap:pretty}
#doors .doors-cta{margin-top:36px;display:flex;flex-wrap:wrap;align-items:center;gap:18px}
#doors .doors-cta p{margin:0;max-width:52ch;color:var(--band-ash)}
</style>"""

WORDS = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]

e = html.escape


def build(slug, data):
    place = NAMES.get(slug, slug.replace("-", " ").title())
    title = data.get("title") or f"Doors I can open in {place}"
    deck = data.get("deck") or (
        "The experiences that don’t show up on a booking site. "
        "Tell me which ones sound like you and I’ll build the days around them."
    )
    cards = []
    for i, d in enumerate(data["doors"]):
        n = WORDS[i] if i < len(WORDS) else str(i + 1)
        cards.append(
            f'<div class="door reveal"><span class="door-n">{n}</span>'
            f'<h3>{e(d["h"])}</h3><p>{e(d["p"])}</p></div>'
        )
    return (
        f"{START}\n"
        f'<section class="section band on-shadow" id="doors" style="scroll-margin-top:70px;">\n'
        f"{CSS}\n"
        f'<div class="container">\n'
        f'<div class="sec-head reveal"><span class="eyebrow">Beyond the hotel</span>'
        f'<h2 class="display-l">{e(title)}</h2>\n'
        f'<p class="deck" style="margin-top:16px; max-width:54ch;">{e(deck)}</p></div>\n'
        f'<div class="doors-grid">{"".join(cards)}</div>\n'
        f'<div class="doors-cta reveal"><a class="btn btn-ghost" href="#inquire">Ask me about these</a>'
        f"<p>I arrange every one of these privately, and the best of them book up months ahead.</p></div>\n"
        f"</div>\n</section>\n{END}"
    )


def insert(page, block):
    if START in page:
        return re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, page, flags=re.S)
    m = re.search(r'<section[^>]*id="hotels"', page)
    if not m:
        raise SystemExit("no #hotels section found")
    # find the matching </section> for #hotels, accounting for nested sections
    depth, i = 0, m.start()
    for t in re.finditer(r"<section\b|</section>", page[m.start():]):
        depth += 1 if t.group(0) != "</section>" else -1
        if depth == 0:
            i = m.start() + t.end()
            break
    return page[:i] + "\n" + block + "\n" + page[i:]


def add_toc(page):
    """Add an "On this page" link to #doors right after the #hotels link."""
    if 'href="#doors"' in page:
        return page
    return re.sub(
        r'(<a class="toc-link" href="#hotels">[^<]*</a>)',
        r'\1 <a class="toc-link" href="#doors">Doors I can open</a>',
        page, count=1)


def drop_section(page, sid):
    """Remove a section (and its toc link) that the doors replace."""
    page = re.sub(r'\s*<a class="toc-link" href="#%s">[^<]*</a>' % sid, "", page)
    m = re.search(r'<section[^>]*id="%s"' % sid, page)
    if not m:
        return page
    end = page.index("</section>", m.start()) + len("</section>")
    return page[:m.start()] + page[end:]


def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    slug = args[0]
    out = Path(args[args.index("--out") + 1]) if "--out" in args else ROOT / f"{slug}.html"
    data = json.loads((ROOT / "tools" / "doors" / f"{slug}.json").read_text())
    page = (ROOT / f"{slug}.html").read_text()
    for sid in data.get("replaces", []):
        page = drop_section(page, sid)
    out.write_text(add_toc(insert(page, build(slug, data))))
    print(f"wrote {out} ({len(data['doors'])} doors)")


if __name__ == "__main__":
    main()
