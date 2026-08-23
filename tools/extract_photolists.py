#!/usr/bin/env python3
"""Extract the tp-card photo list pages (pools, tennis courts) into phase1/src/data/photolists.json."""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "phase1" / "src" / "data" / "photolists.json"
SLUGS = ["top-hotel-pools", "top-hotel-tennis-courts"]


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
    g["eyebrow"] = clean(grab(r'tp-hero.*?<span class="tp-eyebrow">(.*?)</span>', html))
    g["h1"] = clean(grab(r"tp-hero.*?<h1>(.*?)</h1>", html))
    g["sub"] = clean(grab(r"tp-hero.*?<h1>.*?</h1>\s*<p>(.*?)</p>", html))
    g["cards"] = []
    for block in re.split(r'<div class="tp-card[^"]*">', html)[1:]:
        c = {}
        c["img"] = "/" + grab(r"background-image:url\('([^']+)'\)", block)
        c["pos"] = grab(r"background-position:\s*([^;'\"]+)", block, default=None)
        c["num"] = grab(r'<span class="tp-num">([^<]*)</span>', block)
        c["name"] = clean(grab(r"<h3>(.*?)</h3>", block))
        c["loc"] = clean(grab(r'<p class="tp-loc">(.*?)</p>', block))
        c["price"] = clean(grab(r'<span class="tp-price">(.*?)</span>', block, default=""))
        c["fora"] = clean(grab(r'<span class="tp-fora">(.*?)</span>', block, default=""))
        c["desc"] = clean(grab(r'<p class="tp-desc">(.*?)</p>', block))
        m = re.search(r'<a href="(hotels/[^"]+)" class="read-link">', block)
        c["href"] = "/" + m.group(1) if m else None
        g["cards"].append(c)
    g["cta"] = clean(grab(r'tp-cta">\s*<div class="container">\s*<p>(.*?)</p>', html, default=""))
    return g


def main():
    data = {s: extract(s) for s in SLUGS}
    for s, v in data.items():
        print(s, "cards", len(v["cards"]), "hrefs", sum(1 for c in v["cards"] if c["href"]))
        for c in v["cards"]:
            for req in ["img", "num", "name", "loc", "desc"]:
                if not c.get(req):
                    print("  MISSING", req, c.get("name"))
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
