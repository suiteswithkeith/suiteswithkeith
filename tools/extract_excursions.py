#!/usr/bin/env python3
"""Extract the bundled excursion decks into phase1/src/data/excursions.json.

The three excursion pages (santorini, paros, athens) are bundler decks whose
content only exists after the in-browser unpacker runs, so this reads
browser-unpacked DOM snapshots (document.documentElement.outerHTML saved to
<slug>-excursions-unpacked.html) from the directory given as argv[1].

Screens are the deck's data-screen-label sections. Each screen becomes a
generic block: eyebrow / title / note / intro / image / card groups, where a
card is {chip|num, title, ps[]} and each paragraph is classified as desc,
verdict (italic), price ("From ..." uppercase) or meta.
"""
import json, re, sys, pathlib
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "phase1" / "src" / "data" / "excursions.json"
SNAPDIR = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(".")
SLUGS = ["santorini", "paros", "athens"]


def txt(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip()


def style(el):
    return el.get("style", "") or ""


def is_up(el):
    return "uppercase" in style(el)


def is_it(el):
    return "italic" in style(el)


def bg_img(el):
    m = re.search(r'url\("?([^")]*images/excursions/[^")]+)"?\)', style(el))
    if not m:
        return None
    u = m.group(1)
    return u if u.startswith("/") else "/" + u


def classify_p(el):
    t = txt(el)
    if not t:
        return None
    if is_it(el):
        return {"kind": "verdict", "t": t}
    if is_up(el) and t.lower().startswith("from "):
        return {"kind": "price", "t": t}
    if re.match(r"(Dinner|Lunch|Don’t miss|Don't miss|Book|Note)[:…]", t):
        return {"kind": "meta", "t": t}
    return {"kind": "desc", "t": t}


def split_multi(div):
    """A grid child holding several h4 blocks is a container of sub-cards."""
    subs = div.find_all("div", recursive=False)
    if len(div.find_all("h4")) > 1 and not div.find("h3") and subs:
        return subs
    return None


def parse_card(div):
    card = {"chip": None, "num": None, "title": None, "ps": []}
    for el in div.descendants:
        if el.name is None:
            continue
        if el.name == "span" and is_up(el) and not card["chip"]:
            card["chip"] = txt(el)
        elif el.name == "div" and is_up(el) and not card["chip"] and not el.find(["h3", "h4", "p", "div"]):
            card["chip"] = txt(el)
        elif el.name == "p" and is_up(el) and not card["title"] and len(txt(el)) < 12:
            card["num"] = txt(el)
        elif el.name in ("h3", "h4") and not card["title"]:
            card["title"] = txt(el)
        elif el.name == "p" and card["title"]:
            c = classify_p(el)
            if c:
                card["ps"].append(c)
    return card if card["title"] else None


def parse_table_block(tb):
    blk = tb.parent
    b = {"eyebrow": None, "title": None, "paras": [], "head": [], "rows": []}
    for el in blk.find_all(["p", "h3"], recursive=False):
        t = txt(el)
        if not t:
            continue
        if el.name == "h3":
            b["title"] = t
        elif is_up(el) and len(t) < 40:
            b["eyebrow"] = t
        else:
            b["paras"].append(t)
    trs = tb.find_all("tr")
    b["head"] = [txt(c) for c in trs[0].find_all(["th", "td"])]
    b["rows"] = [[txt(c) for c in tr.find_all(["th", "td"])] for tr in trs[1:]]
    return b


def parse_screen(sec):
    s = {"label": sec.get("data-screen-label"), "eyebrow": None, "title": None,
         "note": None, "intro": [], "img": bg_img(sec), "groups": [], "outro": None}
    tb = sec.find("table")
    if tb is not None:
        s["table"] = parse_table_block(tb)
        tb.parent.decompose()
    grids = []
    for el in sec.descendants:
        if el.name is None:
            continue
        if el.name in ("h2", "h3") and not s["title"] and not any(g in el.parents for g in grids):
            s["title"] = txt(el)
            prev = el.find_previous(["p"])
            if prev is not None and is_up(prev) and len(txt(prev)) < 40:
                s["eyebrow"] = txt(prev)
        elif el.name == "div" and "grid-template" in style(el):
            if any(g in el.parents for g in grids):
                continue
            grids.append(el)
            items = []
            for d in el.find_all(["div", "p"], recursive=False):
                if d.name == "p":
                    # a bare description paragraph beside the name block (row grids)
                    c = classify_p(d)
                    if c and items:
                        items[-1]["ps"].append(c)
                    continue
                subs = split_multi(d)
                for dd in (subs or [d]):
                    c = parse_card(dd)
                    if c:
                        items.append(c)
            if items:
                s["groups"].append(items)
        elif el.name == "p" and s["title"] and not any(g in el.parents for g in grids):
            t = txt(el)
            if not t:
                continue
            if is_it(el) and not s["note"]:
                s["note"] = t
            elif not is_up(el) and len(t) > 30:
                (s["intro"] if not s["groups"] else [None]).append(t) if not s["groups"] else s.__setitem__("outro", t)
        if el.name == "div" and bg_img(el) and not s["img"]:
            s["img"] = bg_img(el)
    return s


def extract(slug):
    html = (SNAPDIR / f"{slug}-excursions-unpacked.html").read_text()
    soup = BeautifulSoup(html, "html.parser")
    screens = soup.select("[data-screen-label]")
    g = {"slug": slug}
    cover = screens[0]
    ps = [txt(p) for p in cover.find_all("p") if txt(p)]
    g["eyebrow"] = ps[0] if ps else ""
    g["h1"] = txt(cover.find("h1"))
    g["sub"] = ps[-1] if len(ps) > 1 else ""
    g["hero_img"] = bg_img(cover) or next((bg_img(d) for d in cover.find_all("div") if bg_img(d)), None)
    flow = []
    container = screens[1].parent
    for el in container.children:
        if el.name is None:
            continue
        if el.has_attr("data-screen-label"):
            lb = el.get("data-screen-label")
            if lb in ("Cover", "Closing"):
                continue
            flow.append(parse_screen(el))
        elif bg_img(el) and flow:
            flow[-1]["img_after"] = bg_img(el)
    # promote an intro-card into the screen header when the screen itself had no h2/h3
    for sc in flow:
        if not sc["title"] and sc["groups"]:
            first = sc["groups"][0][0]
            if first["ps"] and not first.get("chip"):
                sc["title"] = first["title"]
                sc["eyebrow"] = first.get("num")
                notes = [x["t"] for x in first["ps"] if x["kind"] in ("verdict", "desc")]
                sc["note"] = notes[0] if notes else None
                sc["groups"][0] = sc["groups"][0][1:]
                sc["groups"] = [gp for gp in sc["groups"] if gp]
    g["screens"] = flow
    closing = screens[-1]
    g["closing"] = {
        "title": txt(closing.find(["h2", "h3"])),
        "p": next((txt(p) for p in closing.find_all("p") if len(txt(p)) > 60), ""),
        "img": bg_img(closing) or next((bg_img(d) for d in closing.find_all("div") if bg_img(d)), None),
    }
    foot = soup.find("footer")
    g["footer_note"] = txt(foot.find("div")) if foot else ""
    return g


def main():
    data = {s: extract(s) for s in SLUGS}
    for s, v in data.items():
        print("=" * 30, s)
        print(" hero:", v["h1"], "|", (v["hero_img"] or "NO HERO"), "|", v["eyebrow"])
        for sc in v["screens"]:
            print(f"  [{sc['label']}] {sc['title']} | groups: {[len(x) for x in sc['groups']]} | img: {bool(sc['img'])} | intro {len(sc['intro'])} note {bool(sc['note'])} outro {bool(sc['outro'])}")
        print(" closing:", v["closing"]["title"], "| footer:", v["footer_note"][:60])
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
