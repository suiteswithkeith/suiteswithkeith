#!/usr/bin/env python3
"""Extract hotel-guides.html (the grouped index of hotel reviews) into phase1/src/data/hotelguides.json."""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "phase1" / "src" / "data" / "hotelguides.json"


def clean(s):
    return re.sub(r"\s+", " ", s).strip() if isinstance(s, str) else s


def absolutize(html):
    return re.sub(r'(href)="(?!https?:|mailto:|#|/)', r'\1="/', html)


def main():
    html = (ROOT / "hotel-guides.html").read_text()
    title = re.search(r"<title>([^<]+)</title>", html).group(1)
    desc = re.search(r'<meta name="description" content="([^"]+)"', html).group(1)
    head = re.search(r"<h1>(.*?)</h1>\s*<p>(.*?)</p>", html, re.S)

    groups = []
    parts = re.split(r'<div class="hg-group-head">', html)[1:]
    for part in parts:
        h2 = clean(re.search(r"<h2>(.*?)</h2>", part, re.S).group(1))
        pm = re.search(r"</h2>\s*<p>(.*?)</p>", part, re.S)
        blurb = clean(absolutize(pm.group(1))) if pm else ""
        cards = []
        for card in re.split(r'<div class="guide-card">', part)[1:]:
            img = re.search(r"background-image:url\('([^']+)'\)", card)
            name = re.search(r"<h3>(.*?)</h3>", card, re.S)
            p = re.search(r"</h3>\s*<p>(.*?)</p>", card, re.S)
            href = re.search(r'<a href="([^"]+)" class="read-link">', card)
            if not (img and name and href):
                continue
            h = href.group(1)
            if not re.match(r"https?:|mailto:|#|/", h):
                h = "/" + h
            cards.append({
                "img": "/" + img.group(1),
                "name": clean(name.group(1)),
                "p": clean(p.group(1)) if p else "",
                "href": h,
            })
        groups.append({"h2": h2, "blurb": blurb, "cards": cards})

    data = {
        "title": title, "description": desc,
        "h1": clean(head.group(1)), "intro": clean(absolutize(head.group(2))),
        "groups": groups,
    }
    total = sum(len(g["cards"]) for g in groups)
    print("groups:", [(g["h2"][:30], len(g["cards"])) for g in groups], "total:", total)
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
