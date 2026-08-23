#!/usr/bin/env python3
"""Extract the 20 hand-authored hotel 'brief' pages into phase1/src/data/hotelbriefs.json."""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "phase1" / "src" / "data" / "hotelbriefs.json"
SLUGS = [
    "acro-suites-crete", "capella-sydney", "cheval-blanc-paris", "claridges-london",
    "connaught-london", "ellerman-house-cape-town", "four-seasons-tamarindo",
    "lanesborough-london", "londolozi-south-africa", "luura-paros",
    "minos-beach-art-hotel-crete", "minos-palace-crete", "mombo-camp-botswana",
    "naviva-punta-mita", "odera-tinos", "perma-serifos", "raffles-london-owo",
    "ritz-paris", "royal-malewane-south-africa", "st-regis-punta-mita",
]


def absolutize(html):
    # ../foo -> /foo ; bare hotel links -> /hotels/foo
    html = re.sub(r'(src|href)="\.\./', r'\1="/', html)
    html = re.sub(r'(href)="(?!https?:|mailto:|#|/)', r'\1="/hotels/', html)
    return html


def grab(pattern, text, flags=re.S, group=1, default=None):
    m = re.search(pattern, text, flags)
    return m.group(group).strip() if m else default


def clean(s):
    return re.sub(r"\s+", " ", s).strip() if isinstance(s, str) else s


def extract(slug):
    html = (ROOT / "hotels" / f"{slug}.html").read_text()
    g = {"slug": slug}
    g["title"] = grab(r"<title>([^<]+)</title>", html)
    g["description"] = grab(r'<meta name="description" content="([^"]+)"', html)
    g["hero_img"] = grab(r"rank-hero\" style=\"background-image:url\('\.\.([^']+)'\)", html)
    g["eyebrow"] = clean(grab(r'rank-hero.*?<span class="eyebrow-mag">(.*?)</span>', html))
    g["h1"] = clean(grab(r"rank-hero.*?<h1>(.*?)</h1>", html))
    g["tagline"] = clean(grab(r'rank-hero.*?<p class="tagline">(.*?)</p>', html))
    g["stats"] = [
        {"num": clean(n), "label": clean(l)}
        for n, l in re.findall(r'<span class="stat-num">(.*?)</span><span class="stat-label">(.*?)</span>', html, re.S)
    ]
    intro = grab(r'<section class="rank-intro">(.*?)</section>', html)
    toc = intro.find("rank-toc")
    g["intro_paras"] = [clean(absolutize(p)) for p in re.findall(r"<p[^>]*>(.*?)</p>", intro[:toc], re.S)]
    g["glance"] = [
        {"label": clean(l), "html": clean(absolutize(v))}
        for l, v in re.findall(r'<span class="glance-row"><span class="g-label">(.*?)</span>(.*?)</span>\s*(?=<span class="glance-row"|</div>)', intro[toc:], re.S)
    ]
    g["sections"] = []
    for card in re.split(r'<div class="rank-card[^"]*"[^>]*>', html)[1:]:
        sec = {
            "kicker": clean(grab(r'<span class="rank-num">(.*?)</span>', card)),
            "h3": clean(grab(r"<h3>(.*?)</h3>", card)),
            "notes": [
                {"b": clean(absolutize(b)), "t": clean(absolutize(t))}
                for b, t in re.findall(r'<p class="note-item"><b>(.*?)</b>(.*?)</p>', card, re.S)
            ],
            "take": clean(absolutize(grab(r'<p class="rank-take">(.*?)</p>', card, default="") or "")) or None,
        }
        g["sections"].append(sec)
    # optional custom section between the intro and the note cards (e.g. Capella's map)
    mid = grab(r'</section>\s*(<section class="(?!rank-list)[^"]*">.*?</section>)\s*<section class="rank-list">', html, default=None)
    if mid:
        swaps = {"#f5f1e9": "#F2EFE6", "#6f745c": "#4A5040", "#c9b997": "#BE975A",
                 "rgba(245,241,233": "rgba(242,239,230", "rgba(201,185,151": "rgba(190,151,90",
                 "var(--font-display)": "var(--display)", "var(--charcoal)": "var(--ink)"}
        for a, b in swaps.items():
            mid = mid.replace(a, b)
        mid = absolutize(mid)
    g["extra_html"] = mid
    callout = grab(r'<div class="print-callout">(.*?)</div>', html, default="")
    g["perks_eyebrow"] = clean(grab(r'<span class="eyebrow-mag">(.*?)</span>', callout))
    g["perks_h3"] = clean(grab(r"<h3>(.*?)</h3>", callout))
    g["perks_p"] = clean(absolutize(grab(r"</h3>\s*<p>(.*?)</p>", callout, default="")))
    cta = grab(r'<section class="guide-cta"[^>]*>(.*?)</section>', html, default="")
    g["cta_eyebrow"] = clean(grab(r'<span class="eyebrow">(.*?)</span>', cta))
    g["cta_h2"] = clean(grab(r"<h2>(.*?)</h2>", cta))
    g["hotel_name"] = grab(r'name="hotel" value="([^"]+)"', html)
    g["subject"] = grab(r'name="_subject" value="([^"]+)"', html)
    g["placeholder"] = grab(r'id="hi-when"[^>]*placeholder="([^"]+)"', html, default="Late June, 5 nights")
    g["related"] = []
    for href, label in re.findall(r'<a href="([^"]+)" class="read-link">(.*?)(?:&nbsp;|\s)*&rarr;', cta, re.S):
        if href.startswith("../"):
            href = "/" + href[3:]
        elif not re.match(r"https?:|mailto:|#|/", href):
            href = "/hotels/" + href
        g["related"].append({"href": href, "label": clean(label)})
    return g


def main():
    data = {s: extract(s) for s in SLUGS}
    for s, v in data.items():
        probs = []
        for req in ["hero_img", "h1", "tagline", "perks_p", "cta_h2", "hotel_name"]:
            if not v.get(req):
                probs.append(req)
        print(s, "| stats", len(v["stats"]), "glance", len(v["glance"]), "sections",
              [len(x["notes"]) for x in v["sections"]], "related", len(v["related"]),
              ("MISSING: " + ",".join(probs)) if probs else "")
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
