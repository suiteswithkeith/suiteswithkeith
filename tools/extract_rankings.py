#!/usr/bin/env python3
"""Extract the rank-card ranking pages into phase1/src/data/rankings.json."""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "phase1" / "src" / "data" / "rankings.json"
SLUGS = ["napa-sonoma", "best-hotels-greece", "santorini-hotels-ranked"]


def absolutize(html):
    return re.sub(r'(src|href)="(?!https?:|mailto:|#|/)', r'\1="/', html)


def grab(pattern, text, flags=re.S, group=1, default=None):
    m = re.search(pattern, text, flags)
    return m.group(group).strip() if m else default


def clean(s):
    return re.sub(r"\s+", " ", s).strip() if isinstance(s, str) else s


def extract(slug):
    html = (ROOT / f"{slug}.html").read_text()
    g = {"slug": slug}
    g["title"] = grab(r"<title>([^<]+)</title>", html)
    g["description"] = grab(r'<meta name="description" content="([^"]+)"', html)
    g["hero_img"] = "/" + grab(r"rank-hero\" style=\"background-image:url\('([^']+)'\)", html)
    g["eyebrow"] = grab(r'rank-hero.*?<span class="eyebrow-mag">(.*?)</span>', html)
    g["h1"] = grab(r"rank-hero.*?<h1>(.*?)</h1>", html)
    g["tagline"] = grab(r'rank-hero.*?<p class="tagline">(.*?)</p>', html)
    g["stats"] = [
        {"num": clean(n), "label": clean(l)}
        for n, l in re.findall(r'<span class="stat-num">(.*?)</span><span class="stat-label">(.*?)</span>', html)
    ]
    intro = grab(r'<section class="rank-intro">(.*?)</section>', html)
    toc_start = intro.find('rank-toc')
    g["intro_paras"] = [clean(absolutize(p)) for p in re.findall(r"<p[^>]*>(.*?)</p>", intro[:toc_start], re.S)]
    g["toc"] = []
    for href, label in re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', intro[toc_start:], re.S):
        if not re.match(r"https?:|mailto:|#|/", href):
            href = "/" + href
        g["toc"].append({"href": href, "label": clean(re.sub(r"(&nbsp;|\s)*&rarr;", "", label))})

    g["cards"] = []
    ranklist = grab(r'<section class="rank-list"[^>]*>(.*?)</section>', html, default="")
    for block in re.split(r'<div class="rank-card[^"]*">', ranklist)[1:]:
        c = {}
        c["img"] = "/" + grab(r'<img src="([^"]+)"', block)
        c["img_alt"] = grab(r'<img src="[^"]+" alt="([^"]*)"', block, default="")
        c["num"] = grab(r'<span class="rank-num">([^<]*)</span>', block)
        c["name"] = clean(grab(r"<h3>(.*?)</h3>", block))
        c["tag"] = clean(grab(r'<p class="rank-tag">(.*?)</p>', block))
        c["bestfor"] = clean(grab(r'<p class="rank-bestfor">(.*?)</p>', block))
        c["desc"] = clean(grab(r'<p class="rank-desc">(.*?)</p>', block))
        c["notes"] = [
            {"b": clean(b), "t": clean(t)}
            for b, t in re.findall(r'<p class="note-item"><b>(.*?)</b>(.*?)</p>', block, re.S)
        ]
        c["perks_label"] = clean(grab(r'<span class="fora-perks-label">(.*?)</span>', block, default=""))
        c["perks_items"] = clean(grab(r'<span class="fora-perks-items">(.*?)</span>', block, default=""))
        c["take"] = clean(grab(r'<p class="rank-take">(.*?)</p>', block))
        m = re.search(r'<a href="(hotels/[^"]+)" class="read-link">(.*?)</a>', block, re.S)
        c["href"] = "/" + m.group(1) if m else None
        m2 = re.search(r'<img src="([^"]+)"[^>]*class="rank-img2"', block)
        if m2:
            c["img2"] = "/" + m2.group(1)
        g["cards"].append(c)

    g["winners"] = [
        {"cat": clean(c), "w": clean(w)}
        for c, w in re.findall(r'<li><span class="cat">(.*?)</span><span class="winner">(.*?)</span></li>', html, re.S)
    ]
    g["pairings"] = [
        {"q": clean(q), "a": clean(absolutize(a))}
        for q, a in re.findall(r'<li><span class="q">(.*?)</span><span class="a">(.*?)</span></li>', html, re.S)
    ]
    g["transfers"] = []
    tr = grab(r'<section class="section" id="transfers".*?</section>', html, group=0, default="")
    for h, body in re.findall(r"<h4>(.*?)</h4>\s*<p>(.*?)</p>\s*<p[^>]*><a href=\"([^\"]+)\"[^>]*>(.*?)</a></p>", tr, re.S)[:0]:
        pass
    for m in re.finditer(r'<h4>(.*?)</h4>\s*<p>(.*?)</p>\s*<p[^>]*><a href="([^"]+)"[^>]*>(.*?)</a></p>', tr, re.S):
        href = m.group(3)
        if not re.match(r"https?:|mailto:|#|/", href):
            href = "/" + href
        g["transfers"].append({
            "h": clean(m.group(1)), "p": clean(m.group(2)), "href": href,
            "label": clean(re.sub(r"(&nbsp;|\s)*&rarr;", "", m.group(4))),
        })
    g["kit"] = 'id="kit"' in html
    g["cta_eyebrow"] = clean(grab(r'guide-cta[^>]*>.*?<span class="eyebrow">(.*?)</span>', html, default=""))
    g["cta_h2"] = clean(grab(r'guide-cta[^>]*>.*?<h2>(.*?)</h2>', html, default=""))
    return g


def main():
    data = {s: extract(s) for s in SLUGS}
    for s, v in data.items():
        print(s, "cards", len(v["cards"]), "notes/card", [len(c["notes"]) for c in v["cards"]],
              "winners", len(v["winners"]), "pairings", len(v["pairings"]), "transfers", len(v["transfers"]),
              "stats", len(v["stats"]), "toc", len(v["toc"]), "intro", len(v["intro_paras"]))
        for c in v["cards"]:
            for req in ["img", "num", "name", "desc", "take"]:
                if not c.get(req):
                    print("  MISSING", req, "on", c.get("name"))
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
