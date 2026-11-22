"""Build the editorial articles (best-of lists, hotel deep dives, essays).

Each page reuses the head boilerplate, nav, footer and scripts of
venice-new-luxury-hotels-2026.html so the new pages match the live site.
Article content lives in tools/editorials/*.py as a PAGE dict.

    python3 tools/build_editorials.py          # build every article
"""
import html
import importlib.util
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = (ROOT / "venice-new-luxury-hotels-2026.html").read_text()
SITE = "https://suiteswithkeith.com"

# ---- boilerplate sliced from the template --------------------------------
_icons_start = TEMPLATE.index('<link rel="icon"')
_icons_end = TEMPLATE.index("</script>", TEMPLATE.index("gtag('config'")) + len("</script>")
HEAD_TAIL = TEMPLATE[_icons_start:_icons_end]
STYLES = TEMPLATE[TEMPLATE.index("<style>.vs-guide"):TEMPLATE.index("</head>")]
NAV = re.search(r'<nav class="nav".*?</nav>', TEMPLATE, re.S).group(0)
FOOTER = TEMPLATE[TEMPLATE.index('<footer class="site">'):TEMPLATE.index('<a href="#inquire" class="btn sticky-cta"')]
SCRIPTS = TEMPLATE[TEMPLATE.index('<script type="module">'):]

EXTRA_CSS = (
    "<style>.ed-prose{max-width:62ch}.ed-prose p{margin-top:16px}"
    ".ed-prose h2{font-family:var(--display);font-weight:400;font-size:clamp(1.7rem,3.2vw,2.2rem);line-height:1.2;margin-top:clamp(48px,7vw,80px)}"
    ".ed-prose h2 .n{display:block;font-family:var(--body);font-size:13px;letter-spacing:.2em;color:var(--brass);margin-bottom:10px}"
    ".ed-prose ul{margin:16px 0 0;padding-left:18px}.ed-prose li{margin-top:8px}"
    ".ed-fig{margin:clamp(32px,5vw,48px) 0 0}.ed-fig img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block}"
    ".ed-fig figcaption{font-size:.85rem;color:var(--ash);margin-top:10px}"
    ".ed-pull{border-left:2px solid var(--brass);padding-left:20px;margin-top:28px;font-family:var(--display);font-size:1.35rem;line-height:1.45}"
    ".ed-pull cite{display:block;font-family:var(--body);font-style:normal;font-size:.85rem;color:var(--ash);margin-top:8px}"
    ".ed-skip{margin-top:clamp(40px,6vw,64px)}"
    "@media(max-width:719px){.ed-hero .hero-img{grid-template-columns:1fr!important}.ed-hero .hero-img img:not(:first-child){display:none}}"
    "</style>\n"
)

LINK_STYLE = ("font-size:13px; font-weight:400; letter-spacing:.2em; text-transform:uppercase; "
              "color:var(--brass); text-decoration:none; font-family: 'Instrument Serif', Didot, Georgia, serif;")


def text(s):
    """Plain text for meta/JSON-LD: drop tags, decode entities."""
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def attr(s):
    return html.escape(text(s), quote=True)


# ---- components ------------------------------------------------------------
def hero(p):
    imgs = p["hero_images"]
    cols = len(imgs)
    tags = "\n".join(
        f'<img src="{i["src"]}" alt="{attr(i["alt"])}" fetchpriority="high" style="width:100%; height:100%; '
        f'object-fit:cover; display:block; object-position:{i.get("pos", "50% 50%")};">' for i in imgs)
    return (f'<header class="hero ed-hero" style="min-height:min(82svh,760px);">\n'
            f'<div class="hero-img" style="display:grid; grid-template-columns:repeat({cols},1fr); gap:2px;">\n{tags}\n</div>\n'
            f'<div class="container"> <p class="eyebrow">{p["eyebrow"]}</p> <h1 class="display-xl vs-h1" style="max-width:18ch;">{p["h1"]}\n'
            f'</h1> <p class="sub" style="max-width:50ch;">{p["sub"]}</p> <p class="stamp" style="margin-top:20px;">{p["stamp"]}</p> </div>\n'
            f'</header>')


def intro(p):
    body = "".join(f' <p class="body-2 reveal" style="margin-top:18px; max-width:60ch;">{b}</p>' for b in p["intro"])
    return (f' <section class="section">\n<div class="container" style="max-width:860px;"> '
            f'<p class="deck reveal" style="max-width:46ch;">{p["deck"]}</p>{body} </div>\n</section>')


def short_answer(sa):
    rows = []
    for r in sa["rows"]:
        name = (f'<a href="{r["href"]}" style="color:var(--band-ink); text-decoration:underline; text-decoration-color:var(--brass); '
                f'text-underline-offset:3px; font-weight:600;">{r["name"]}</a>') if r.get("href") else \
            f'<b style="color:var(--band-ink); font-weight:600;">{r["name"]}</b>'
        rows.append(f'<div class="kv-row band-row">\n<dt style="color:var(--brass);">{r["label"]}</dt>\n'
                    f'<dd style="color:var(--band-ink);">\n{name}'
                    f'<span class="body-2" style="color:var(--band-ash);">{r["text"]}</span>\n</dd>\n</div>')
    return (f' <section class="section band on-shadow" id="short-answer" style="scroll-margin-top:70px;">\n'
            f'<div class="container"> <div class="sec-head reveal">\n<span class="eyebrow">{sa.get("eyebrow", "The short answer")}</span>\n'
            f'<h2 class="display-l">{sa["title"]}</h2>\n</div> <dl class="kv reveal">\n' + "\n".join(rows) +
            '\n</dl> </div>\n</section>')


def section_head(eyebrow, title, deck=None):
    d = f'<p class="deck" style="margin-top:14px; max-width:52ch;">{deck}</p>' if deck else ""
    return (f'<div class="sec-head reveal">\n<span class="eyebrow">{eyebrow}</span>\n'
            f'<h2 class="display-l">{title}</h2>{d}\n</div>')


def hotel_block(h, idx):
    flip = " flip" if idx % 2 else ""
    href = h.get("href")
    def link(inner, **kw):
        return f'<a href="{href}">{inner}</a>' if href else inner
    img = f'<img src="{h["img"]["src"]}" alt="{attr(h["img"]["alt"])}" loading="lazy" decoding="async">'
    kv = "".join(
        f'\n<div class="kv-row">\n<dt>{k}</dt>\n<dd>{v}</dd>\n</div>' for k, v in h["kv"])
    body = "".join(f' <p class="body-2" style="margin-top:18px;">{b}</p>' for b in h["body"])
    btn = (f' <p style="margin-top:24px;">\n<a class="btn btn-ghost" href="{href}">{h.get("btn", "Read the full review")}</a>\n</p>'
           if href else "")
    notes = "\n".join(f'<p class="hp-note">\n<b>{b}</b> <span>{s}</span>\n</p>' for b, s in h["notes"])
    img2 = (f' <img src="{h["img2"]["src"]}" alt="{attr(h["img2"]["alt"])}" loading="lazy" decoding="async" '
            f'style="margin-top:24px; aspect-ratio:4/3; object-fit:cover;">') if h.get("img2") else ""
    return (f'<section class="section">\n<div class="container">\n'
            f'<div class="hp-block" id="{h["id"]}" style="scroll-margin-top:70px;"> <div class="hp-grid{flip}"> <figure class="reveal hp-media">\n'
            f'{link(img)}\n</figure> <div class="reveal"> <span class="eyebrow">{h["eyebrow"]}</span> '
            f'<h3 class="display-m hp-name" style="font-size:clamp(1.792rem,3.36vw,2.352rem); margin-top:12px;">\n{link(h["name"])}\n</h3> '
            f'<p class="deck" style="margin-top:8px; font-size:1.05rem;">{h["tagline"]}</p>{body} <dl class="kv" style="margin-top:26px;">{kv}\n</dl>{btn} </div> </div> '
            f'<div class="hp-notes"> <div class="reveal"> <p class="stamp plain" style="font-weight:400; color:var(--brass); margin-bottom:16px;">Keith&rsquo;s notes</p> {notes} </div> '
            f'<div class="reveal"> <p class="stamp plain" style="font-weight:400; color:var(--brass); margin-bottom:16px;">The verdict</p> '
            f'<div class="verdict">\n<p>{h["verdict"]}</p>\n</div>{img2} </div> </div> </div>\n</div>\n</section>')


def table(t):
    head = "".join(f"<th>{c}</th>" for c in [""] + t["cols"])
    rows = "".join(
        f'<tr><td class="rowlabel">{r[0]}</td>' + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>" for r in t["rows"])
    return (f'<section class="section" style="padding-top:0;">\n<div class="container"> {section_head(t["eyebrow"], t["title"])} '
            f'<div class="table-wrap reveal">\n<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>\n</div> </div>\n</section>')


def prose(s):
    """Free-form essay section: list of ("h2"|"p"|"pull"|"fig"|"ul"|"raw", value)."""
    out = []
    for kind, v in s["items"]:
        if kind == "h2":
            n, t = v
            out.append(f'<h2 id="{s.get("id_prefix", "p")}-{n}"><span class="n">{n}</span>{t}</h2>')
        elif kind == "p":
            out.append(f'<p class="body-2">{v}</p>')
        elif kind == "pull":
            q, cite = v
            out.append(f'<blockquote class="ed-pull">{q}<cite>{cite}</cite></blockquote>')
        elif kind == "fig":
            out.append(f'<figure class="ed-fig"><img src="{v["src"]}" alt="{attr(v["alt"])}" loading="lazy" decoding="async">'
                       + (f'<figcaption>{v["cap"]}</figcaption>' if v.get("cap") else "") + '</figure>')
        elif kind == "ul":
            out.append('<ul class="body-2">' + "".join(f"<li>{li}</li>" for li in v) + "</ul>")
        elif kind == "raw":
            out.append(v)
    head = section_head(s["eyebrow"], s["title"], s.get("deck")) if s.get("title") else ""
    pad = ' style="padding-top:0;"' if s.get("tight") else ""
    return (f'<section class="section"{pad}>\n<div class="container" style="max-width:860px;"> {head}'
            f'<div class="ed-prose reveal">' + "\n".join(out) + '</div> </div>\n</section>')


def tiles(t):
    items = "\n".join(
        f'<a class="vsi-tile" href="{x["href"]}"> <span class="vsi-names">{x["names"]}</span> '
        f'<span class="vsi-q">{x["q"]}</span> <span class="vsi-go">{x.get("go", "Settle it")}&nbsp;&rarr;</span> </a>' for x in t["items"])
    return (f'<section class="section" id="{t.get("id", "head-to-heads")}" style="padding-top:0; scroll-margin-top:70px;">\n'
            f'<div class="container"> {section_head(t["eyebrow"], t["title"])} <div class="vsi-grid reveal">\n{items}\n</div> </div>\n</section>')


def faq(items):
    d = "\n".join(f'<details>\n<summary>{q}</summary>\n<p class="body-2">{a}</p>\n</details>' for q, a in items)
    return (f'<section class="section" style="padding-top:0;">\n<div class="container" style="max-width:820px;"> '
            f'{section_head("Before you ask", "The questions I get")} <div class="vs-faq reveal">\n{d}\n</div> </div>\n</section>')


def inquire(p):
    q = p["inquire"]
    links = " ".join(f'<a href="{h}" style="{LINK_STYLE}">\n<span>{t}</span>&nbsp;&rarr;</a>' for t, h in q["links"])
    return f'''
<section class="section inquire" id="inquire">
<div class="container">
<h2 class="display-l reveal">{q["title"]}</h2>
<p class="deck reveal" style="margin:18px auto 0; max-width:42ch;">{q["deck"]}</p>
<form class="inquire-form reveal" action="https://formspree.io/f/mjgnadov" method="POST">
<input type="hidden" name="_subject" value="{attr(q["subject"])}">
<input type="hidden" name="hotel" value="{attr(q["hotel"])}">
<input type="hidden" name="page" value="{p["slug"]}">
<input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
<div class="step1">
<label for="q-when">When are you thinking?</label>
<input id="q-when" type="text" name="travel_dates" placeholder="{q.get("when", "June 2027 &middot; 7 nights")}" required autocomplete="off">
</div>
<div class="step2">
<label for="q-name">And where do I send the recommendation?</label>
<input id="q-name" type="text" name="name" placeholder="Name" required autocomplete="name">
<input id="q-email" type="email" name="email" placeholder="Email" required autocomplete="email">
<label for="q-details" style="margin-top:2px;">Anything else? Guests, budget, occasion (optional)</label>
<input id="q-details" type="text" name="details" placeholder="{q.get("details", "2 adults &middot; anniversary")}" autocomplete="off">
</div>
<button type="submit" class="btn" data-gtag-label="editorial_inquiry_send" data-gtag-location="editorial_cta">Send</button>
<p class="note">Traveling within the next 30 days? You will hear from me today.</p>
<p class="status" role="status" aria-live="polite">
</p>
</form>
<p class="reveal" style="margin-top:26px; display:flex; gap:12px 32px; justify-content:center; flex-wrap:wrap;"> {links} </p>
</div>
</section>
'''


# ---- page ------------------------------------------------------------------
def build(p):
    url = f'{SITE}/{p["slug"]}.html'
    og_img = SITE + p["og_image"]
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": text(q), "acceptedAnswer": {"@type": "Answer", "text": text(a)}} for q, a in p["faq"]]}
    ld_art = {"@context": "https://schema.org", "@type": "Article", "headline": text(p["headline"]),
              "author": {"@type": "Person", "name": "Keith Pence", "url": f"{SITE}/about.html"},
              "publisher": {"@type": "Organization", "name": "Suites With Keith", "url": f"{SITE}/"},
              "datePublished": p["date"], "dateModified": p["date"], "image": og_img, "url": url}
    title = attr(p["title"])
    desc = attr(p["description"])
    head = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(ld_art, ensure_ascii=False)}</script><link rel="preload" as="image" href="{p["hero_images"][0]["src"]}" fetchpriority="high">
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og_img}">
{HEAD_TAIL}


{STYLES}{EXTRA_CSS}</head> <body>
{NAV}
'''
    parts = [hero(p), intro(p)]
    for s in p["sections"]:
        kind = s["kind"]
        if kind == "short_answer":
            parts.append(short_answer(s))
        elif kind == "hotels":
            if s.get("title"):
                parts.append(f'<section class="section" style="padding-bottom:0;">\n<div class="container"> '
                             f'{section_head(s["eyebrow"], s["title"], s.get("deck"))} </div>\n</section>')
            parts.extend(hotel_block(h, i) for i, h in enumerate(s["items"]))
        elif kind == "table":
            parts.append(table(s))
        elif kind == "prose":
            parts.append(prose(s))
        elif kind == "tiles":
            parts.append(tiles(s))
    parts.append(faq(p["faq"]))
    sticky = f'<a href="#inquire" class="btn sticky-cta" data-gtag-label="start_planning" data-gtag-location="sticky_mobile">{p.get("sticky", "Help me choose")}</a>\n'
    return head + " ".join(parts) + inquire(p) + FOOTER + sticky + SCRIPTS


def main():
    for f in sorted((ROOT / "tools" / "editorials").glob("*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        p = mod.PAGE
        out = ROOT / f'{p["slug"]}.html'
        out.write_text(build(p))
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
