#!/usr/bin/env python3
"""AI-search (GEO) pass: keeps the site readable and current for ChatGPT, Claude,
Perplexity, Google AI Overviews and other answer engines.

Run from the repo root after adding or editing pages (and after any Astro or
generator rebuild, since rebuilt pages lose what this adds):

    python3 tools/geo.py

What it does, idempotently:
  1. Structured data (JSON-LD) on every page in sitemap.xml:
     - existing Article / Review / WebPage blocks get datePublished and
       dateModified from git history, and Keith's author link;
     - hotel pages with no review markup get a Review of the Hotel by Keith;
     - hotel "guide" pages with an Article get "about": the Hotel;
     - about.html gets a ProfilePage for Keith; other pages with no page-level
       markup get a WebPage block. Added blocks carry data-geo and are rebuilt
       on each run.
  2. sitemap.xml: a <lastmod> on every URL, plus any public hotels/*.html page
     that is missing.
  3. llms.txt: a plain-text map of the site for AI systems, rebuilt from page
     titles and meta descriptions.

Dates: dateModified is the last commit that touched the file, ignoring commits
whose message starts with "GEO:" (so committing this script's output does not
make every page look freshly updated). Commit its output with a "GEO:" message.
"""
import html as H
import json
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://suiteswithkeith.com/"
ABOUT = SITE + "about.html"
AUTHOR = {"@type": "Person", "name": "Keith Pence", "url": ABOUT}
PUBLISHER = {"@type": "Organization", "name": "Suites With Keith", "url": SITE}
PAGE_TYPES = {"Article", "Review", "WebPage", "CollectionPage", "BlogPosting", "ProfilePage", "AboutPage"}
TODAY = date.today().isoformat()

LD_RE = re.compile(r'<script type="application/ld\+json"( data-geo)?>(.*?)</script>\n?', re.S)


# ---------- git dates ----------
def git_dates():
    """{path: (first_commit_date, last_non_GEO_commit_date)}"""
    out = subprocess.run(
        ["git", "log", "--format=\x01%cs\x02%s", "--name-only", "--no-renames"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout
    first, last = {}, {}
    for chunk in out.split("\x01")[1:]:
        head, _, files = chunk.partition("\n")
        day, _, subject = head.partition("\x02")
        geo = subject.startswith("GEO:")
        for f in files.split("\n"):
            f = f.strip()
            if not f:
                continue
            first[f] = day  # log is newest-first, so the final write is the oldest
            if not geo and f not in last:
                last[f] = day
    return {f: (first[f], last.get(f, first[f])) for f in first}


# ---------- html helpers ----------
def text(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", H.unescape(H.unescape(s))).strip()


def grab(pattern, h, default=""):
    m = re.search(pattern, h, re.S)
    return text(m.group(1)) if m else default


def page_info(h, url):
    title = grab(r"<title>(.*?)</title>", h)
    title = re.sub(r"\s*\|\s*Suites With Keith\s*$", "", title)
    img = grab(r'<meta property="og:image" content="([^"]+)"', h)
    if not img:
        m = re.search(r'<img src="(/images/[^"]+)"', h)
        img = SITE + m.group(1).lstrip("/") if m else ""
    return {
        "title": title,
        "desc": grab(r'<meta name="description" content="([^"]*)"', h),
        "h1": grab(r"<h1[^>]*>(.*?)</h1>", h),
        "eyebrow": grab(r'<p class="eyebrow">(.*?)</p>', h),
        "img": img,
        "url": url,
    }


def hotel_entity(info):
    loc = info["eyebrow"].split("·")[-1].strip() if "·" in info["eyebrow"] else ""
    hotel = {"@type": "Hotel", "name": info["h1"] or info["title"]}
    if loc:
        hotel["address"] = {"@type": "PostalAddress", "addressLocality": loc}
    if info["img"]:
        hotel["image"] = info["img"]
    return hotel


def dump(obj, spaced):
    s = json.dumps(obj, ensure_ascii=False) if spaced else json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return s.replace("</", "<\\/")


def objects(data):
    if isinstance(data, list):
        return data
    return data.get("@graph", [data])


def types_of(o):
    t = o.get("@type", [])
    return {t} if isinstance(t, str) else set(t)


# ---------- per page ----------
def process(path, h, dates):
    rel = path.relative_to(ROOT).as_posix()
    url = SITE + ("" if rel == "index.html" else rel)
    first, last = dates.get(rel, (TODAY, TODAY))
    info = page_info(h, url)
    is_hotel = rel.startswith("hotels/")

    h = re.sub(r'<script type="application/ld\+json" data-geo>.*?</script>\n?', "", h, flags=re.S)
    has_page_obj = has_hotel = has_review = False

    for m in LD_RE.finditer(h):
        if '"Hotel"' in m.group(2):
            has_hotel = True
        if re.search(r'"@type":\s*"Review"', m.group(2)):
            has_review = True

    def fix(m):
        nonlocal has_page_obj
        raw = m.group(2)
        try:
            data = json.loads(raw)
        except ValueError:
            return m.group(0)
        changed = False
        for o in objects(data):
            if not isinstance(o, dict) or not (types_of(o) & PAGE_TYPES):
                continue
            has_page_obj = True
            if o.get("dateModified") != last:
                o["dateModified"] = last
                changed = True
            if "datePublished" not in o:
                o["datePublished"] = first
                changed = True
            a = o.get("author")
            if isinstance(a, dict) and a.get("name") == "Keith Pence" and "url" not in a:
                a["url"] = ABOUT
                changed = True
            if is_hotel and not has_hotel and "Article" in types_of(o) and "about" not in o:
                o["about"] = hotel_entity(info)
                changed = True
        if not changed:
            return m.group(0)
        return f'<script type="application/ld+json">{dump(data, chr(34) + ": " in raw)}</script>' + (
            "\n" if m.group(0).endswith("\n") else "")

    h = LD_RE.sub(fix, h)

    added = None
    if is_hotel and not has_page_obj and not has_review:
        added = {
            "@context": "https://schema.org", "@type": "Review", "name": info["title"],
            "itemReviewed": hotel_entity(info), "author": AUTHOR, "publisher": PUBLISHER,
            "description": info["desc"], "datePublished": first, "dateModified": last, "url": url,
        }
    elif rel == "about.html":
        added = {
            "@context": "https://schema.org", "@type": "ProfilePage", "name": info["title"], "url": url,
            "description": info["desc"], "datePublished": first, "dateModified": last,
            "mainEntity": {
                "@type": "Person", "name": "Keith Pence", "url": ABOUT,
                "jobTitle": "Luxury Travel Advisor",
                "description": "Fora X travel advisor specializing in Europe, honeymoons and luxury hotels.",
                "affiliation": {"@type": "Organization", "name": "Fora Travel", "url": "https://www.foratravel.com/"},
                "knowsAbout": ["Luxury hotels", "Honeymoon planning", "Greek islands", "Italy", "Europe travel"],
                "sameAs": ["https://instagram.com/suiteswithkeith", "https://www.foratravel.com/advisor/keith-pence"],
            },
        }
    elif rel == "index.html":
        added = {"@context": "https://schema.org", "@type": "WebSite", "name": "Suites With Keith",
                 "url": SITE, "publisher": PUBLISHER, "author": AUTHOR, "inLanguage": "en"}
    elif not has_page_obj:
        added = {
            "@context": "https://schema.org", "@type": "WebPage", "name": info["title"], "url": url,
            "description": info["desc"], "author": AUTHOR, "publisher": PUBLISHER,
            "datePublished": first, "dateModified": last, "inLanguage": "en",
        }
        if info["img"]:
            added["image"] = info["img"]
    if added:
        added = {k: v for k, v in added.items() if v}
        h = h.replace("</head>", f'<script type="application/ld+json" data-geo>{dump(added, True)}</script>\n</head>', 1)
    return h, info, last


# ---------- sitemap ----------
def sitemap_paths(sm):
    out = []
    for loc in re.findall(r"<loc>(.*?)</loc>", sm):
        rel = loc.replace(SITE, "", 1) or "index.html"
        out.append((loc, rel + "index.html" if rel.endswith("/") else rel))
    return out


def add_missing_hotels(sm):
    listed = {rel for _, rel in sitemap_paths(sm)}
    add = ""
    for p in sorted((ROOT / "hotels").glob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel not in listed and "noindex" not in p.read_text(encoding="utf-8"):
            add += (f"  <url>\n    <loc>{SITE}{rel}</loc>\n    <changefreq>monthly</changefreq>\n"
                    f"    <priority>0.7</priority>\n  </url>\n")
    return sm.replace("</urlset>", add + "</urlset>") if add else sm


def set_lastmod(sm, lastmods):
    def one(m):
        block = re.sub(r"\s*<lastmod>.*?</lastmod>", "", m.group(0))
        loc = re.search(r"<loc>(.*?)</loc>", block).group(1)
        lm = lastmods.get(loc)
        return block.replace("</loc>", f"</loc>\n    <lastmod>{lm}</lastmod>", 1) if lm else block
    return re.sub(r"<url>.*?</url>", one, sm, flags=re.S)


# ---------- llms.txt ----------
LLMS_INTRO = """# Suites With Keith

> Suites With Keith is the website of Keith Pence, a luxury travel advisor with Fora Travel (Fora X) specializing in Europe, honeymoons and luxury hotels. It publishes Keith's first-hand hotel reviews, head-to-head hotel comparisons, rankings and destination guides, drawn from hotels he has stayed at or toured.

- Booking a hotel through Keith costs the same as booking direct, and usually adds Fora perks such as a space-available upgrade, daily breakfast and a hotel credit. Hotel bookings are complimentary.
- Comparison pages say whether Keith stayed at or toured each hotel, and when.
- To plan a trip, use the inquiry form on any page. More about Keith: {about}
""".format(about=ABOUT)

SKIP = re.compile(r"^(404|privacy|subscribe|subscriber-welcome|style-guide)\.html$")
SECTIONS = [
    ("About Keith and how booking works", lambda r: r in {
        "index.html", "about.html", "services.html", "planning-with-swk.html", "corporate-travel.html",
        "private-jet-charter.html", "private-boat-transfers.html"}),
    ("Rankings and best-of lists", lambda r: bool(re.search(
        r"(rankings|ranked|^top-|the-fifteen|worlds-50-best|^best-|matrix)", r))),
    ("Hotel comparisons (which one to book)", lambda r: "-vs-" in r),
    ("Hotel reviews", lambda r: r.startswith("hotels/")),
    ("Sample proposals and itineraries", lambda r: r.startswith("sample-")),
    ("Destination guides and trip planning", lambda r: True),
]


def build_llms(pages):
    groups = {name: [] for name, _ in SECTIONS}
    for rel, info in pages:
        if SKIP.match(rel):
            continue
        name = next(n for n, test in SECTIONS if test(rel))
        line = f"- [{info['title']}]({info['url']})"
        groups[name].append(line + (f": {info['desc']}" if info["desc"] else ""))
    out = LLMS_INTRO
    for name, _ in SECTIONS:
        if groups[name]:
            out += f"\n## {name}\n\n" + "\n".join(sorted(groups[name], key=str.lower)) + "\n"
    return out


def main():
    dates = git_dates()
    smp = ROOT / "sitemap.xml"
    sm = add_missing_hotels(smp.read_text(encoding="utf-8"))
    lastmods, pages, changed = {}, [], 0
    for loc, rel in sitemap_paths(sm):
        p = ROOT / rel
        if not p.exists():
            print("missing file for", loc)
            continue
        old = p.read_text(encoding="utf-8")
        new, info, last = process(p, old, dates)
        if new != old:
            p.write_text(new, encoding="utf-8")
            changed += 1
        lastmods[loc] = last
        pages.append((rel, info))
    smp.write_text(set_lastmod(sm, lastmods), encoding="utf-8")
    (ROOT / "llms.txt").write_text(build_llms(pages), encoding="utf-8")
    print(f"{len(pages)} pages checked, {changed} updated; sitemap.xml and llms.txt rebuilt")


if __name__ == "__main__":
    main()
