#!/usr/bin/env python3
"""Extract the template-generated island guide pages into phase1/src/data/guides.json.

The six guides (santorini, mykonos, milos, sifnos, folegandros, athens) were all
generated from guide_template.html, so their markup is uniform enough for regex
extraction. Bespoke pages (montenegro, santorini-guide, napa-sonoma) are not
handled here.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "phase1" / "src" / "data" / "guides.json"
SLUGS = ["santorini", "mykonos", "milos", "sifnos", "folegandros", "athens"]


def absolutize(html: str) -> str:
    # root-relative asset and page links
    html = re.sub(r'(src|href)="(?!https?:|mailto:|#|/)', r'\1="/', html)
    return html


def grab(pattern, text, flags=re.S, group=1, default=None):
    m = re.search(pattern, text, flags)
    return m.group(group).strip() if m else default


def extract(slug: str) -> dict:
    html = (ROOT / f"{slug}.html").read_text()
    g = {"slug": slug}

    g["title"] = grab(r"<title>([^<]+)</title>", html)
    g["description"] = grab(r'<meta name="description" content="([^"]+)"', html)

    # hero
    g["hero_img"] = "/" + grab(r"guide-hero\" style=\"background-image:url\('([^']+)'\)", html)
    g["issue_tag"] = grab(r'<p class="issue-tag">(.*?)</p>', html)
    g["num"] = grab(r'<span class="num">([^<]*)</span>', html)
    g["h1"] = grab(r'guide-hero.*?<h1>([^<]+)</h1>', html)
    g["tagline"] = grab(r'guide-hero.*?<p class="tagline">(.*?)</p>', html)

    # at a glance
    aag = grab(r'<section class="at-a-glance">(.*?)</section>', html)
    g["aag_h2"] = grab(r"<h2>(.*?)</h2>", aag)
    g["already_booked"] = None
    m = re.search(r'<a href="(already-booked[^"]+)" class="read-link">([^<]+?)(?:&nbsp;|\s)*&rarr;', aag)
    if m:
        g["already_booked"] = {"href": "/" + m.group(1), "label": m.group(2).strip()}
    facts = grab(r'<div class="aag-facts">(.*?)<div class="aag-dontmiss">', aag)
    blocks = re.findall(r"<h4[^>]*>([^<]+)</h4>\s*<ul>(.*?)</ul>", facts, re.S)
    g["facts"] = [
        {"label": lbl.strip(), "items": re.findall(r"<li>(.*?)</li>", ul)} for lbl, ul in blocks
    ]
    dm = grab(r'<div class="aag-dontmiss">(.*?)</div>', aag)
    g["dont_miss"] = [
        {"h": h.strip(), "p": p.strip()}
        for h, p in re.findall(r"<h5>([^<]+)</h5>\s*<p>(.*?)</p>", dm)
    ]
    around = grab(r'<div class="aag-around">\s*<h4>Getting Around</h4>(.*?)</div>', aag)
    paras = re.findall(r"<p[^>]*>(.*?)</p>", around, re.S)
    g["around_text"] = absolutize(paras[0]) if paras else ""
    g["around_links"] = []
    for p in paras[1:]:
        m = re.search(r'<a href="([^"]+)"[^>]*>(.*?)(?:&nbsp;|\s)*&rarr;', p, re.S)
        if m:
            href = m.group(1)
            if not re.match(r"https?:|mailto:|#|/", href):
                href = "/" + href
            if g["already_booked"] and href == g["already_booked"]["href"]:
                continue
            g["around_links"].append({"href": href, "label": re.sub(r"\s+", " ", m.group(2)).strip()})
    g["verdict"] = grab(r'keiths-verdict">.*?<p>(.*?)</p>', aag)

    # stay areas
    sa = grab(r'<section class="stay-areas"[^>]*>(.*?)</section>', html, default="")
    g["stay_areas"] = [
        {"h": h.strip(), "p": p.strip()}
        for h, p in re.findall(r"<h4>([^<]+)</h4>\s*<p>(.*?)</p>", sa)
    ]

    # hotel profiles
    g["hotels"] = []
    for block in re.findall(r'<section class="hotel-profile"[^>]*>(.*?)</section>', html, re.S):
        h = {}
        h["img"] = "/" + grab(r'<img src="([^"]+)"', block)
        h["img_alt"] = grab(r'<img src="[^"]+" alt="([^"]*)"', block, default="")
        h["kicker"] = grab(r'<span class="eyebrow-tag">(.*?)</span>', block)
        h["name"] = grab(r"<h3>(.*?)</h3>", block)
        h["sub"] = grab(r'<p class="hotel-sub">(.*?)</p>', block)
        h["desc"] = grab(r'<p class="hotel-desc">(.*?)</p>', block)
        metas = re.findall(
            r'<span class="label">([^<]+)</span>\s*<span class="val">(.*?)</span>\s*</div>', block
        )
        for lbl, val in metas:
            lbl = lbl.strip().lower()
            note = grab(r'<span class="room-note">(.*?)</span>', val, default=None)
            clean = re.sub(r'<span class="room-note">.*?</span>', "", val, flags=re.S).strip()
            if "best for" in lbl:
                h["best_for"] = clean
            elif "rate" in lbl:
                h["rate"] = clean
            elif "room" in lbl:
                h["room"] = clean
                h["room_note"] = note
        h["href"] = None
        m = re.search(r'<a href="(hotels/[^"]+)" class="read-link">', block)
        if m:
            h["href"] = "/" + m.group(1)
        h["notes"] = [
            {"b": b.strip(), "t": re.sub(r"\s+", " ", t).strip()}
            for b, t in re.findall(r'<p class="note-item"><b>(.*?)</b>(.*?)</p>', block, re.S)
        ]
        h["take"] = grab(r'<p class="take-text">(.*?)</p>', block)
        imgs = re.findall(r'<img src="([^"]+)"[^>]*alt="([^"]*)"', block)
        if len(imgs) > 1:
            h["img2"] = "/" + imgs[-1][0]
            h["img2_alt"] = imgs[-1][1]
        g["hotels"].append(h)

    # three days
    td = grab(r'<section class="three-days"[^>]*>(.*?)</section>', html, default="")
    g["td_eyebrow"] = grab(r'<span class="eyebrow-mag">(.*?)</span>', td)
    g["td_h2"] = grab(r"<h2>(.*?)</h2>", td)
    g["td_deck"] = grab(r"<h2>.*?</h2>\s*<p>(.*?)</p>", td)
    g["td_photo"] = None
    m = re.search(r'td-photo">\s*<img src="([^"]+)" alt="([^"]*)"', td)
    if m:
        g["td_photo"] = {"src": "/" + m.group(1), "alt": m.group(2)}
    g["days"] = [
        {"h": h.strip(), "p": p.strip(), "meta": absolutize(meta.strip())}
        for h, p, meta in re.findall(
            r'<div class="td-day">\s*<h4>(.*?)</h4>\s*<p>(.*?)</p>\s*<div class="td-meta">(.*?)</div>', td, re.S
        )
    ]
    g["td_tip"] = grab(r'td-tip">.*?<p>(.*?)</p>', td)

    # cross-link note
    g["note_html"] = absolutize(grab(r'<section class="physical-note">.*?<p>(.*?)</p>', html, default="") or "")

    for k, v in list(g.items()):
        if isinstance(v, str):
            g[k] = re.sub(r"\s+", " ", v).strip()
    return g


def main():
    data = {s: extract(s) for s in SLUGS}
    # coverage report
    for s, g in data.items():
        print(
            f"{s}: hotels={len(g['hotels'])} facts={len(g['facts'])} dontmiss={len(g['dont_miss'])} "
            f"areas={len(g['stay_areas'])} days={len(g['days'])} links={len(g['around_links'])} "
            f"note={'y' if g['note_html'] else 'n'} booked={'y' if g['already_booked'] else 'n'}"
        )
        for req in ["hero_img", "h1", "tagline", "aag_h2", "verdict", "td_h2"]:
            if not g.get(req):
                print(f"  MISSING {req}", file=sys.stderr)
        for h in g["hotels"]:
            for req in ["img", "name", "desc", "take", "best_for", "rate", "room"]:
                if not h.get(req):
                    print(f"  hotel {h.get('name')}: MISSING {req}", file=sys.stderr)
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
