#!/usr/bin/env python3
"""Transform greek-island-matrix.html's article body for the Phase 1 design system.

Extracts the <article class="swk-post"> body, absolutizes links, swaps the legacy
palette for Plaster & Shadow tokens, removes the floating CTA (Layout provides
the sticky mobile CTA), and points inquiry links at the page's own #inquire.
Output: phase1/src/data/matrix-body.html (injected via set:html).
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "greek-island-matrix.html"
OUT = ROOT / "phase1" / "src" / "data" / "matrix-body.html"

html = SRC.read_text()
body = html[html.find('<article class="swk-post">'):]
body = body[: body.find("</article>") + len("</article>")]

# root-relative links and images
body = re.sub(r'(src|href)="(?!https?:|mailto:|#|/)', r'\1="/', body)

# inquiry links to this page's own ask
body = body.replace('href="/index.html#inquire"', 'href="#inquire"')

# palette: legacy navy/gold/parchment -> shadow/brass/plaster
swaps = {
    "#12182A": "#161712",  # deep navy -> shadow
    "#1A2338": "#22231C",
    "#101627": "#161712",
    "#1C2436": "#1F201A",  # ink navy -> ink
    "#2A3244": "#3A3B33",
    "#26304A": "#2E2F27",
    "#3A455F": "#4A4B41",
    "#B7A37C": "#836229",  # gold on light -> brass
    "#C9B997": "#BE975A",  # gold on dark -> brass-lit
    "#C9BA96": "#BE975A",
    "#D9CFB8": "#C9C4B2",
    "#EDE7DA": "#F2EFE6",
    "#E8E4DA": "#F2EFE6",
    "#F5F1E9": "#F2EFE6",  # parchment panel -> plaster (deep handled by CSS)
    "#FFFDF8": "#F2EFE6",
    "#E6DECD": "#D8D3C3",  # hairline
    "#8C8577": "#65665C",  # soft ink -> ash
    "#2A2A26": "#1F201A",
    "#EBD9A8": "#BE975A",
}
for old, new in swaps.items():
    body = body.replace(old, new).replace(old.lower(), new)

# drop the floating CTA (Layout supplies the mobile sticky CTA)
body = re.sub(r'<a class="swk-float".*?</a>', "", body, flags=re.S)

OUT.write_text(body)
print("wrote", OUT, len(body), "bytes")
# sanity: unresolved legacy colors?
left = set(re.findall(r"#(?:12182A|1C2436|B7A37C|C9B997|F5F1E9|E6DECD|8C8577)", body, re.I))
print("unswapped:", left or "none")
