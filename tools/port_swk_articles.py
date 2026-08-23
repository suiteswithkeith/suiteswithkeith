#!/usr/bin/env python3
"""Transform the swk-post editorial articles for the Phase 1 design system.

Handles greek-island-matrix, greece-honeymoon and greek-island-pairings:
extracts each <article class="swk-post">, absolutizes links, swaps the legacy
palette for Plaster & Shadow values, strips the floating CTA, points inquiry
links at each page's own #inquire, and extracts the FAQPage JSON-LD.
Outputs phase1/src/data/<slug>-body.html and <slug>-ld.json.
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "phase1" / "src" / "data"
SLUGS = ["greek-island-matrix", "greece-honeymoon", "greek-island-pairings", "planning-with-swk"]

SWAPS = {
    "#12182A": "#161712", "#1A2338": "#22231C", "#101627": "#161712",
    "#1C2436": "#1F201A", "#2A3244": "#3A3B33", "#26304A": "#2E2F27",
    "#3A455F": "#4A4B41", "#B7A37C": "#836229", "#C9B997": "#BE975A",
    "#C9BA96": "#BE975A", "#D9CFB8": "#C9C4B2", "#EDE7DA": "#F2EFE6",
    "#E8E4DA": "#F2EFE6", "#F5F1E9": "#F2EFE6", "#FFFDF8": "#F2EFE6",
    "#E6DECD": "#D8D3C3", "#E0D6C0": "#D8D3C3", "#8C8577": "#65665C",
    "#2A2A26": "#1F201A", "#EBD9A8": "#BE975A", "#EFE7D6": "#E9E5DA", "#5C5A53": "#65665C",
    "#4A4A44": "#65665C",
}


def port(slug):
    html = (ROOT / f"{slug}.html").read_text()
    body = html[html.find('<article class="swk-post">'):]
    body = body[: body.find("</article>") + len("</article>")]
    body = re.sub(r'(src|href)="(?!https?:|mailto:|#|/)', r'\1="/', body)
    body = body.replace('href="/index.html#inquire"', 'href="#inquire"')
    for old, new in SWAPS.items():
        body = body.replace(old, new).replace(old.lower(), new)
    body = re.sub(r'<a class="swk-float".*?</a>', "", body, flags=re.S)
    if slug == "greek-island-matrix":
        body = body.replace('class="swk-cta"', 'class="swk-cta-panel"')
    (OUTDIR / f"{slug}-body.html").write_text(body)

    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    faq = next((b for b in lds if '"FAQPage"' in b), None)
    if faq:
        (OUTDIR / f"{slug}-ld.json").write_text(json.dumps(json.loads(faq)))
    print(slug, len(body), "bytes; faq:", bool(faq))


for s in SLUGS:
    port(s)
