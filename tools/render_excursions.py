#!/usr/bin/env python3
"""Render <slug>-excursions.html from tools/excursions/<slug>.json.

Skeleton is paros-excursions.html (head boilerplate, nav, inquire form, footer,
scripts). Adds a Leaflet map of the island's pins. Usage:
    python3 tools/render_excursions.py sifnos
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKELETON = ROOT / "paros-excursions.html"

LEAFLET_CSS = "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"
LEAFLET_JS = "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"

CATS = [
    ("eat", "Where to eat", "#836229"),
    ("beach", "Beaches", "#3D6B7A"),
    ("do", "Experiences", "#4A5040"),
    ("town", "Villages & ports", "#1F201A"),
]

EXTRA_CSS = """
.exc-map-wrap{margin-top:34px;border:1px solid var(--hairline);background:var(--lime)}
#exc-map{height:clamp(380px,62vh,560px);width:100%;background:var(--plaster-deep);z-index:0}
.exc-map-filters{display:flex;flex-wrap:wrap;gap:8px;padding:14px;border-bottom:1px solid var(--hairline)}
.exc-map-filters button{font-family:var(--stamp);font-size:.62rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--ink);background:transparent;border:1px solid var(--hairline-firm);padding:7px 12px;cursor:pointer;display:inline-flex;align-items:center;gap:8px}
.exc-map-filters button[aria-pressed="false"]{opacity:.4}
.exc-map-filters i{display:inline-block;width:9px;height:9px;border-radius:50%}
.exc-map-note{padding:10px 14px;font-size:.78rem;color:var(--ash-3);border-top:1px solid var(--hairline)}
.leaflet-popup-content-wrapper{border-radius:0;box-shadow:0 6px 24px rgba(22,23,18,.18)}
.leaflet-popup-content{margin:14px 16px;font-family:var(--body);font-size:.86rem;line-height:1.5;color:var(--ash)}
.leaflet-popup-content strong{display:block;font-family:var(--display);font-weight:500;font-size:1.02rem;color:var(--ink);margin-bottom:4px}
.leaflet-popup-content em{display:block;font-style:normal;font-family:var(--stamp);font-size:.58rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;margin-bottom:6px}
.exc-group{margin-top:44px}
.exc-group:first-of-type{margin-top:34px}
.exc-group-h{font-family:var(--stamp);font-size:.7rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--olive);padding-bottom:10px;border-bottom:1px solid var(--hairline)}
.exc-group .exc-grid{margin-top:22px}
.exc-link{margin-top:auto;padding-top:16px;font-family:var(--stamp);font-size:.66rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--brass);text-decoration:none}
.exc-link:hover{color:var(--ink)}
"""

e = html.escape


def card(c, num=None):
    out = ['<div class="exc-card">']
    if num:
        out.append(f'<span class="exc-num">{num}</span>')
    if c.get("chip"):
        out.append(f'<span class="exc-chip">{e(c["chip"])}</span>')
    out.append(f'<h3>{e(c["h"])}</h3>')
    out.append(f'<p class="exc-desc">{e(c["p"])}</p>')
    if c.get("verdict"):
        out.append(f'<p class="exc-verdict">{e(c["verdict"])}</p>')
    if c.get("url"):
        out.append(f'<a class="exc-link" href="{e(c["url"])}" target="_blank" rel="noopener">{e(c.get("link", "Website"))} &rarr;</a>')
    out.append("</div>")
    return " ".join(out)


def sec_head(eyebrow, h, intro=None, deck=None):
    s = '<div class="sec-head reveal">'
    if eyebrow:
        s += f' <span class="eyebrow">{e(eyebrow)}</span>'
    s += f' <h2 class="display-l" style="font-size:clamp(1.7rem,3.4vw,2.5rem);">{e(h)}</h2>'
    if deck:
        s += f' <p class="deck" style="margin-top:16px; max-width:56ch; font-style:italic;">{e(deck)}</p>'
    if intro:
        s += f' <p class="body-2" style="margin-top:16px; max-width:62ch;">{e(intro)}</p>'
    return s + " </div>"


def section(inner, style=""):
    st = f' style="{style}"' if style else ""
    return f'<section class="section"{st}> <div class="container"> {inner} </div> </section>'


def figure(src):
    return section(
        f'<figure class="reveal" style="margin:0;"> <img src="{src}" alt="" width="1600" height="820" '
        'loading="lazy" decoding="async" style="width:100%; aspect-ratio:2/1; object-fit:cover;"> </figure>',
        "padding-top:0;",
    )


def render(d):
    nums = ["One", "Two", "Three", "Four"]
    body = []
    body.append(
        f'<header class="hero" style="min-height:min(82svh,760px);"> <img class="hero-img" src="{d["hero"]}" alt="" '
        'width="1600" height="1200" fetchpriority="high"> <div class="container"> '
        '<p class="eyebrow">The Cyclades · Excursion Guide</p> '
        f'<h1 class="display-xl" style="margin-top:18px;">{e(d["island"])}</h1> <p class="sub">{e(d["sub"])}</p> '
        '<div class="hero-ctas"> <a class="btn" href="#inquire" data-gtag-label="send_picks" data-gtag-location="exc_hero">Send me your picks</a> '
        '<a class="btn btn-ghost on-shadow" href="#exc-map" style="border-color:rgba(242,239,230,.4); color:var(--band-ink);">See the map</a> '
        "</div> </div> </header>"
    )
    rules = "".join(card(r | {"p": r["p"]}, nums[i]) for i, r in enumerate(d["rules"]))
    body.append(section(
        sec_head("Start Here", "A menu, not a plan", deck="Read through, send me the ones you want, and I will build the days around them and hold the bookings that fill up first.")
        + f' <div class="exc-grid reveal exc-rules"> {rules} </div>'
    ))

    filters = "".join(
        f'<button type="button" data-cat="{k}" aria-pressed="true"><i style="background:{col}"></i>{e(lbl)}</button>'
        for k, lbl, col in CATS if any(p["c"] == k for p in d["pins"])
    )
    logistics = "".join(card(c) for c in d["logistics"])
    body.append(section(
        sec_head("The Shape Of It", "The island, and where everything sits", intro=d["map_intro"])
        + f' <div class="exc-map-wrap reveal"> <div class="exc-map-filters" role="group" aria-label="Show on map">{filters}</div>'
        ' <div id="exc-map" role="region" aria-label="Map of ' + e(d["island"]) + '"></div>'
        ' <p class="exc-map-note">Pins mark the area, not the front door. I send exact directions with your itinerary.</p> </div>'
        f' <div class="exc-grid reveal"> {logistics} </div>'
    ))
    body.append(figure(d["divider"]))

    for s in d["sections"]:
        cards = "".join(card(c) for c in s["cards"])
        body.append(section(sec_head(s["eyebrow"], s["h"], intro=s["intro"]) + f' <div class="exc-grid reveal"> {cards} </div>'))

    if d["eat"]:
        groups = "".join(
            f'<div class="exc-group reveal"> <p class="exc-group-h">{e(g["group"])}</p> '
            f'<div class="exc-grid"> {"".join(card(c) for c in g["items"])} </div> </div>'
            for g in d["eat"]
        )
        outro = f' <p class="body-2 reveal" style="margin-top:26px; max-width:62ch;">{e(d["eat_outro"])}</p>' if d["eat_outro"] else ""
        body.append(section(sec_head("The Tables", "Where I would eat", intro=d["eat_intro"]) + f" {groups}{outro}"))

    pins = json.dumps(d["pins"], ensure_ascii=False)
    colors = json.dumps({k: col for k, _, col in CATS})
    labels = json.dumps({k: lbl for k, lbl, _ in CATS})
    map_js = f"""<script src="{LEAFLET_JS}" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script>(function(){{if(!window.L)return;var P={pins},C={colors},N={labels};
var m=L.map('exc-map',{{scrollWheelZoom:false,zoomControl:true}}).setView({json.dumps(d["map"]["center"])},{d["map"]["zoom"]});
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{{z}}/{{y}}/{{x}}',{{maxZoom:16,attribution:'Tiles &copy; Esri, HERE, Garmin, &copy; OpenStreetMap contributors'}}).addTo(m);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Reference/MapServer/tile/{{z}}/{{y}}/{{x}}',{{maxZoom:16}}).addTo(m);
var g={{}};P.forEach(function(p){{(g[p.c]=g[p.c]||L.layerGroup().addTo(m));
var t=document.createElement('div'),s=document.createElement('strong'),c=document.createElement('em'),x=document.createElement('span');s.textContent=p.n;c.textContent=N[p.c];c.style.color=C[p.c];x.textContent=p.d;t.append(s,c,x);
L.circleMarker(p.ll,{{radius:p.c==='town'?6:8,color:'#FBFAF6',weight:2,fillColor:C[p.c],fillOpacity:1}}).bindPopup(t).addTo(g[p.c]);}});
m.fitBounds(L.latLngBounds(P.map(function(p){{return p.ll}})),{{padding:[24,24]}});
document.querySelectorAll('.exc-map-filters button').forEach(function(b){{b.addEventListener('click',function(){{var k=b.dataset.cat,on=b.getAttribute('aria-pressed')==='true';b.setAttribute('aria-pressed',String(!on));on?m.removeLayer(g[k]):g[k].addTo(m);}});}});
}})();</script>"""

    sk = SKELETON.read_text()
    head_end = sk.index("</style></head>")
    head = sk[:head_end]
    # Replace head metadata.
    t, desc = e(d["title"]), e(d["description"])
    url = f"https://suiteswithkeith.com/{d['slug']}-excursions.html"
    head = re.sub(r"<title>.*?</title>", f"<title>{t}</title>", head)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', head)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{t}">', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', head)
    head = head.replace("https://suiteswithkeith.com/paros-excursions.html", url)
    head = head.replace("/images/excursions/paros/44ae8908.webp", d["hero"])
    ld = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": d["title"].split(" | ")[0], "description": d["description"],
        "image": "https://suiteswithkeith.com" + d["hero"],
        "author": {"@type": "Person", "name": "Keith Pence"},
        "publisher": {"@type": "Organization", "name": "Suites With Keith", "logo": {"@type": "ImageObject", "url": "https://suiteswithkeith.com/favicon-32.png"}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
    }
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", head, flags=re.S)
    head = head.replace('<link rel="stylesheet" href="/assets/', f'<link rel="stylesheet" href="{LEAFLET_CSS}" crossorigin="anonymous" referrerpolicy="no-referrer"><link rel="stylesheet" href="/assets/', 1)
    head += EXTRA_CSS.strip() + "\n"

    nav_end = sk.index("</nav>") + len("</nav>")
    inq = sk.index('<section class="section inquire')
    fine = sk.index('<section class="section" style="padding:28px 0 60px;">')
    foot = sk.index("<footer")
    nav = sk[head_end:nav_end]
    inquire = sk[inq:fine]
    inquire = inquire.replace("Inquiry — Paros excursions", f"Inquiry: {d['island']} excursions")
    inquire = inquire.replace('value="paros-excursions"', f'value="{d["slug"]}-excursions"')
    inquire = inquire.replace('placeholder="Paros in September"', f'placeholder="{e(d["form_placeholder"])}"')
    inquire = inquire.replace("I’ll build the days around them — the boat held, tables booked, car and transfers arranged before you land",
                              "I’ll build the days around them: classes and guides booked, tables held, car and transfers arranged before you land")
    inquire = inquire.replace("Nights, budget, occasion &mdash; optional", "Nights, budget, occasion (optional)")
    fineprint = ('<section class="section" style="padding:28px 0 60px;"> <div class="container" style="max-width:760px; text-align:center;"> '
                 '<p class="small" style="color:var(--ash-3); line-height:1.8;">Every experience here is arranged privately and quoted for your dates and group size. '
                 f'I will confirm exactly before anything is held. More on where to stay in <a href="{d["guide"]}">my {e(d["island"])} guide</a>.</p> </div> </section> ')
    tail = sk[foot:]
    tail = tail.replace("</body>", map_js + " </body>")

    out = head + nav + "    " + " ".join(body) + " " + inquire + fineprint + " " + tail
    dest = ROOT / f"{d['slug']}-excursions.html"
    dest.write_text(out)
    print("wrote", dest.relative_to(ROOT))


if __name__ == "__main__":
    slug = sys.argv[1]
    render(json.loads((ROOT / "tools" / "excursions" / f"{slug}.json").read_text()))
