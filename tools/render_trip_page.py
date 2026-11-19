#!/usr/bin/env python3
"""Render a confirmed client itinerary page in the Kirk & Aubrey proposal style.

Usage: python3 -I tools/render_trip_page.py tools/trips/<page-id>.json [...]

Trip content lives in tools/trips/<id>.json. The Original Senses logistics
(ferries, transfers, boats, cars) are read from the JSON named in "logistics"
(tools/os_deposits/<id>.json), priced and deposited with the same rules as
tools/render_os_deposit.py. Writes the whole page to data["page"].

Boat or car rows in the logistics JSON may carry "photo": {"src", "alt"};
they render as a photo card. Stays may carry "atv_email" for the ATV note.
"""
import html
import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_os_deposit import GROUP_ORDER, GROUP_TITLES, RATES, KIND_OF_GROUP, compute, eur, nice_date  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

SERIF = "'Instrument Serif', Didot, Georgia, serif"

CSS = """
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#F2EFE6;color:#1F201A;font-family:'Newsreader',Georgia,'Times New Roman',serif;font-size:18px;line-height:1.6}
a{color:#836229}a:hover{color:#1F201A}
a:focus-visible{outline:2px solid #4A5040;outline-offset:3px}
img{max-width:100%;display:block}
p{margin:0}
.w{max-width:1180px;margin:0 auto}
.band{padding:96px 24px}
.b-cream{background:#F2EFE6}.b-stone{background:#E9E5DA}.b-ink{background:#161712;color:#F2EFE6}
.ey{font-family:%(s)s;text-transform:uppercase;letter-spacing:.2em;font-size:14px;color:#836229}
.b-ink .ey{color:#BE975A}
.lbl{font-family:%(s)s;text-transform:uppercase;letter-spacing:.2em;font-size:13px;color:#65665C}
.b-ink .lbl{color:#9A9B90}
h1,h2,h3{margin:0;font-family:%(s)s;font-weight:400}
h2{font-size:clamp(2rem,4vw,3rem);line-height:1.05}
h2 em,h1 em{font-style:italic}
.b-ink h2 em,.b-ink h1 em{color:#BE975A}
.muted{color:#65665C;font-size:16px}
.b-ink .muted{color:#9A9B90}
.stack{display:flex;flex-direction:column;gap:18px}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr));gap:44px;align-items:start}
figure{margin:0;display:flex;flex-direction:column;gap:12px}
figcaption{font-family:%(s)s;text-transform:uppercase;letter-spacing:.2em;font-size:13px;color:#65665C}
.b-ink figcaption{color:#9A9B90}
.band-fig{margin:0 auto 56px;max-width:1180px}
.band-fig img{width:100%%;height:600px;object-fit:cover}
/* header */
.hd{background:#161712;color:#F2EFE6;padding:104px 24px}
.hd .w{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));gap:56px;align-items:center}
.hd h1{font-size:clamp(3rem,6vw,5.4rem);line-height:1;letter-spacing:-.01em}
.hd .meta{font-family:%(s)s;text-transform:uppercase;letter-spacing:.2em;font-size:15px;color:#9A9B90}
.hd .intro{font-size:20px;max-width:680px}
.hd img{width:100%%;height:620px;object-fit:cover}
.seal{display:inline-flex;align-items:center;gap:10px;border:1px solid rgba(190,151,90,.5);color:#BE975A;padding:10px 16px;font-family:%(s)s;text-transform:uppercase;letter-spacing:.18em;font-size:13px;align-self:flex-start}
.seal::before{content:"";width:8px;height:8px;border-radius:50%%;background:#BE975A}
/* tables */
.tbl{border-top:1px solid rgba(22,23,18,.15)}
.b-ink .tbl,.b-ink .tbl>*{border-color:rgba(242,239,230,.18)!important}
.rt{display:grid;grid-template-columns:1.3fr 1fr 1.6fr .5fr;gap:24px;padding:18px 0;border-bottom:1px solid rgba(22,23,18,.15)}
.rt.h{padding:14px 0}
.rt>span:last-child{text-align:right}
.tag{display:inline-block;margin-left:10px;font-family:%(s)s;text-transform:uppercase;letter-spacing:.16em;font-size:12px;color:#4A5040;border:1px solid rgba(74,80,64,.45);padding:1px 8px;vertical-align:2px;white-space:nowrap}
.b-ink .tag{color:#BE975A;border-color:rgba(190,151,90,.5)}
.tag.soft{color:#836229;border-color:rgba(131,98,41,.45)}
.dy{display:grid;grid-template-columns:150px 1fr;gap:24px;padding:20px 0;border-bottom:1px solid rgba(22,23,18,.15)}
.dy .d{font-family:%(s)s;text-transform:uppercase;letter-spacing:.16em;font-size:14px;color:#836229;padding-top:3px}
.dy .t{font-family:%(s)s;font-size:24px;line-height:1.15}
.dy .n{font-size:16px;color:#65665C;margin-top:6px}
/* cards */
.card{background:#FBFAF6;border:1px solid rgba(22,23,18,.15);padding:32px;display:flex;flex-direction:column;gap:16px}
.b-ink .card{background:transparent;border-color:rgba(242,239,230,.18)}
.kv{display:flex;flex-direction:column}
.kv>div{display:grid;grid-template-columns:auto minmax(0,1fr);gap:24px;padding:12px 0;border-top:1px solid rgba(22,23,18,.15)}
.b-ink .kv>div{border-color:rgba(242,239,230,.18)}
.kv>div>span:last-child{text-align:right}
.kv .k{color:#65665C}
.b-ink .kv .k{color:#9A9B90}
.note{font-size:15px;color:#65665C;border-left:2px solid #BE975A;padding-left:14px}
.b-ink .note{color:#9A9B90}
/* logistics */
.lg-g{margin-top:8px}
.lg-r{display:grid;grid-template-columns:130px 1fr auto;gap:24px;padding:18px 0;border-top:1px solid rgba(22,23,18,.15)}
.lg-r .d{font-family:%(s)s;text-transform:uppercase;letter-spacing:.14em;font-size:13px;color:#836229;padding-top:4px}
.lg-r .t{font-family:%(s)s;font-size:22px;line-height:1.2}
.lg-r .n{font-size:16px;color:#65665C;margin-top:4px}
.lg-r .p{font-family:%(s)s;font-size:22px;text-align:right;white-space:nowrap}
.lg-r .p.pend{font-size:13px;text-transform:uppercase;letter-spacing:.16em;color:#836229;padding-top:6px}
.lg-r .ph{grid-column:2/4;margin-top:14px;max-width:720px}
.lg-r .ph img{width:100%%;height:auto}
.lg-r .ph figcaption{margin-top:8px}
.sum{display:grid;grid-template-columns:repeat(3,1fr);border:1px solid rgba(22,23,18,.15);margin-top:28px}
.sum>div{padding:24px 26px;display:flex;flex-direction:column;gap:6px}
.sum>div+div{border-left:1px solid rgba(22,23,18,.15)}
.sum .v{font-family:%(s)s;font-size:40px;line-height:1}
.sum .s{font-size:15px;color:#65665C}
.sum .now{background:#161712;color:#F2EFE6}
.sum .now .lbl{color:#BE975A}.sum .now .s{color:#9A9B90}
.btn{display:inline-block;background:#4A5040;color:#F2EFE6;text-decoration:none;padding:16px 28px;font-family:%(s)s;text-transform:uppercase;letter-spacing:.16em;font-size:15px;border:0}
.btn:hover{background:#1F201A;color:#F2EFE6}
.btn.off{background:transparent;color:#65665C;border:1px solid rgba(22,23,18,.25)}
.b-ink .btn.off{color:#9A9B90;border-color:rgba(242,239,230,.25)}
.btn.paid{background:#BE975A;color:#161712}
.cta{display:flex;flex-wrap:wrap;gap:20px 28px;align-items:center;margin-top:24px}
.lock{margin-top:24px;border:1px solid rgba(131,98,41,.35);background:#FBFAF6;padding:20px 24px;display:flex;flex-direction:column;gap:6px}
.cta .muted{flex:1;min-width:260px}
details.fine{margin-top:28px;border-top:1px solid rgba(22,23,18,.15);padding-top:16px}
details.fine summary{cursor:pointer;font-family:%(s)s;text-transform:uppercase;letter-spacing:.2em;font-size:13px;color:#65665C}
details.fine ul{margin:14px 0 0;padding-left:18px;font-size:15px;color:#65665C}
details.fine li{margin:6px 0}
/* next steps */
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr));gap:32px}
.steps>div{border-top:1px solid rgba(242,239,230,.18);padding-top:20px;display:flex;flex-direction:column;gap:8px}
.support>div{border-color:rgba(22,23,18,.15)}
.steps .num{font-family:%(s)s;font-size:40px;line-height:1;color:#BE975A}
.sig{border-top:1px solid rgba(242,239,230,.18);padding-top:24px;margin-top:24px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:16px}
.sig img{width:80px;height:80px;border-radius:50%%;object-fit:cover;border:2px solid rgba(255,255,255,.8)}
@media (max-width:700px){
  .band,.hd{padding-top:64px;padding-bottom:64px}
  .hd img{height:420px}
  .band-fig img{height:340px}
  .rt{grid-template-columns:1fr auto;gap:2px 16px}
  .rt.h{display:none}
  .rt>span:nth-child(1){grid-column:1/-1;font-size:15px;color:#65665C;order:-3}
  .rt>span:nth-child(2){order:-2;font-family:%(s)s;font-size:22px}
  .rt>span:nth-child(4){order:-1;font-family:%(s)s;font-size:22px}
  .rt>span:nth-child(4)::after{content:" nights";font-size:15px;color:#65665C}
  .rt>span:nth-child(3){grid-column:1/-1}
  .dy{grid-template-columns:1fr;gap:4px}
  .lg-r{grid-template-columns:1fr auto;gap:4px 16px}
  .lg-r .d{grid-column:1/-1}
  .lg-r .ph{grid-column:1/-1}
  .sum{grid-template-columns:1fr}
  .sum>div+div{border-left:0;border-top:1px solid rgba(22,23,18,.15)}
  .card{padding:24px}
}
""".replace("%(s)s", SERIF).replace("%%", "%")


def esc(s):
    return html.escape(s, quote=True)


def fig(img, cls="band-fig"):
    pos = f' style="object-position:{img["pos"]}"' if img.get("pos") else ""
    cap = f'<figcaption>{img["caption"]}</figcaption>' if img.get("caption") else ""
    return (f'<figure class="{cls}"><img loading="lazy" src="{esc(img["src"])}" alt="{esc(img["alt"])}"{pos}>'
            f'{cap}</figure>')


def kv(rows):
    return '<div class="kv">' + "".join(
        f'<div><span class="k">{k}</span><span>{v}</span></div>' for k, v in rows) + "</div>"


def header(t):
    hero = t["hero"]
    pos = f' style="object-position:{hero["pos"]}"' if hero.get("pos") else ""
    return (
        '<header class="hd"><div class="w">'
        '<div class="stack" style="gap:28px">'
        f'<p class="ey">{t["eyebrow"]}</p>'
        f'<h1>{t["h1"]}</h1>'
        f'<p class="meta">{t["meta"]}</p>'
        f'<p class="intro">{t["intro"]}</p>'
        f'<span class="seal">{t.get("seal", "Confirmed itinerary")}</span>'
        '</div>'
        f'<figure><img src="{esc(hero["src"])}" alt="{esc(hero["alt"])}"{pos}>'
        f'<figcaption>{hero["caption"]}</figcaption></figure>'
        '</div></header>')


def route(t):
    rows = "".join(
        f'<div class="rt"><span>{r["dates"]}</span><span>{r["where"]}</span>'
        f'<span>{r["stay"]}{"<span class=tag>" + r["tag"] + "</span>" if r.get("tag") else ""}</span>'
        f'<span>{r["nights"]}</span></div>' for r in t["route"])
    note = f'<p class="muted">{t["route_note"]}</p>' if t.get("route_note") else ""
    return (
        '<section class="band b-cream"><div class="w stack" style="gap:32px">'
        '<div class="stack" style="gap:12px"><p class="ey">The route</p>'
        f'<h2>{t["route_title"]}</h2></div>'
        '<div class="tbl"><div class="rt h lbl"><span>Dates</span><span>Where</span>'
        '<span>Where you\'ll stay</span><span>Nights</span></div>' + rows + '</div>'
        f'{note}</div></section>')


def days(t):
    rows = "".join(
        f'<div class="dy"><div class="d">{d["date"]}</div><div><div class="t">{d["title"]}'
        f'{"<span class=" + chr(34) + "tag" + (" soft" if d.get("soft") else "") + chr(34) + ">" + d["tag"] + "</span>" if d.get("tag") else ""}'
        f'</div>{"<div class=n>" + d["note"] + "</div>" if d.get("note") else ""}</div></div>'
        for d in t["days"])
    return (
        '<section class="band b-stone"><div class="w two">'
        '<div class="stack" style="position:sticky;top:24px">'
        '<p class="ey">Day by day</p>'
        f'<h2>{t.get("days_title", "How the trip <em>runs</em>")}</h2>'
        f'<p>{t.get("days_intro", "")}</p></div>'
        f'<div class="tbl">{rows}</div>'
        '</div></section>')


def stay(s, bg):
    paras = "".join(f"<p>{p}</p>" for p in s["paras"])
    c = s["card"]
    perks = ""
    if c.get("perks"):
        perks = (f'<p class="ey" style="font-size:13px">{c.get("perks_title", "Included through Suites With Keith")}</p>'
                 f'<p style="font-size:16px">{c["perks"]}</p>')
    fine = f'<p class="muted" style="font-size:15px">{c["fine"]}</p>' if c.get("fine") else ""
    link = ""
    if c.get("link"):
        link = (f'<div><a class="btn" href="{esc(c["link"]["url"])}" target="_blank" rel="noopener">'
                f'{c["link"]["label"]}</a></div>')
    atv = ""
    if s.get("atv", True) and s.get("island", True):
        if s.get("atv_email"):
            atv = ('<p class="note">Rather have an ATV than a car ? For liability reasons I unfortunately '
                   'can\'t book ATVs, but the hotel can arrange one directly: '
                   f'<a href="mailto:{esc(s["atv_email"])}">{esc(s["atv_email"])}</a>.</p>')
        else:
            atv = ('<p class="note">Rather have an ATV than a car ? For liability reasons I unfortunately '
                   'can\'t book ATVs, but the hotel can arrange one directly, and I\'ll connect you '
                   'with the front desk.</p>')
    return (
        f'<section class="band {bg}">{fig(s["img"])}'
        '<div class="w two"><div class="stack">'
        f'<p class="ey">{s["num"]} · {s["where"]} · {s["dates"]}</p>'
        f'<h2>{s["headline"]}</h2>{paras}</div>'
        f'<div class="card"><p class="lbl">{c["label"]}<span class="tag">{c.get("tag", "Booked")}</span></p>'
        f'{kv(c["rows"])}{perks}{fine}{link}{atv}</div>'
        '</div></section>')


def flights(t):
    f = t.get("flights")
    if not f:
        return ""
    rows = "".join(
        f'<div class="lg-r"><div class="d">{r["date"]}</div><div><div class="t">{r["title"]}'
        f'<span class="tag">{r.get("tag", "Booked")}</span></div>'
        f'<div class="n">{r["note"]}</div></div><div></div></div>' for r in f["rows"])
    refs = kv(f["refs"]) if f.get("refs") else ""
    return (
        '<section class="band b-cream"><div class="w two">'
        '<div class="stack"><p class="ey">Flights</p>'
        f'<h2>{f["title"]}</h2><p>{f["intro"]}</p>'
        f'<div class="card"><p class="lbl">Booking references</p>{refs}'
        f'<p class="muted" style="font-size:15px">{f.get("refs_note", "")}</p></div></div>'
        f'<div>{rows}</div></div></section>')


def lg_row(it):
    price = it.get("price")
    p = (f'<div class="p">{eur(price)}</div>' if price is not None
         else f'<div class="p pend">{esc(it.get("price_note", "Being priced"))}</div>')
    note = f'<div class="n">{it["note"]}</div>' if it.get("note") else ""
    tag = f'<span class="tag soft">{esc(it["flag"])}</span>' if it.get("flag") else ""
    ph = ""
    if it.get("photo") and (ROOT / it["photo"]["src"].lstrip("/")).exists():
        cap = f'<figcaption>{it["photo"]["caption"]}</figcaption>' if it["photo"].get("caption") else ""
        ph = (f'<figure class="ph"><img loading="lazy" src="{esc(it["photo"]["src"])}" '
              f'alt="{esc(it["photo"]["alt"])}">{cap}</figure>')
    return (f'<div class="lg-r"><div class="d">{esc(it.get("date", ""))}</div>'
            f'<div><div class="t">{it["title"]}{tag}</div>{note}</div>{p}{ph}</div>')


def logistics(t, data):
    total, dep = compute(data)
    due = date.fromisoformat(data["arrival"]) - timedelta(days=30)
    bal = total - dep
    out = ['<section class="band b-cream" id="deposit"><div class="w">',
           '<div class="two" style="margin-bottom:40px"><div class="stack">',
           '<p class="ey">Ferries, transfers &amp; boat days</p>',
           f'<h2>{data.get("heading", "Securing the <em>logistics</em>")}</h2></div>',
           f'<p style="align-self:end">{data["intro"]}</p></div>']
    for g in data.get("group_order", GROUP_ORDER):
        items = data.get("items", {}).get(g, [])
        if not items:
            continue
        out.append(f'<div class="lg-g"><p class="lbl" style="padding:10px 0">'
                   f'{esc(data.get("group_titles", {}).get(g, GROUP_TITLES[g]))}</p>')
        out.extend(lg_row(it) for it in items)
        out.append('</div>')
    out.append('<div class="sum">'
               f'<div><p class="lbl">Logistics total</p><p class="v">{eur(total)}</p>'
               f'<p class="s">{esc(data.get("total_note", "Everything above, for two"))}</p></div>'
               f'<div class="now"><p class="lbl">Deposit now</p><p class="v">{eur(dep)}</p>'
               '<p class="s">Confirms everything above</p></div>'
               f'<div><p class="lbl">Balance</p><p class="v">{eur(bal)}</p>'
               f'<p class="s">Due by {nice_date(due)}, 30 days before you arrive</p></div></div>')
    if data.get("status") == "paid":
        btn = '<span class="btn paid">Deposit received, thank you</span>'
    elif data.get("pay_url"):
        btn = (f'<a class="btn" href="{esc(data["pay_url"])}" target="_blank" rel="noopener">'
               f'Pay the {eur(dep)} deposit</a>')
    else:
        btn = '<span class="btn off">Payment link on its way</span>'
    items = data.get("items", {})
    ground = [g for g in ("transfers", "cars", "experiences") if items.get(g)]
    parts = []
    if ground:
        parts.append("25% of " + (ground[0] if len(ground) == 1 else ", ".join(ground[:-1]) + " and " + ground[-1]))
    priced = lambda g: [i for i in items.get(g, []) if i.get("price") is not None]
    if priced("ferries") and priced("flights"):
        parts.append("the full ferry and flight fares")
    elif priced("ferries"):
        parts.append("the full ferry fare" + ("s" if len(priced("ferries")) > 1 else ""))
    elif priced("flights"):
        parts.append("the full flight fare" + ("s" if len(priced("flights")) > 1 else ""))
    if items.get("boats"):
        bw = data.get("boat_word", "boat day")
        parts.append(f"{int(RATES['boat'] * 100)}% of " + (f"each {bw}" if len(items["boats"]) > 1 else f"the {bw}"))
    ptxt = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]
    how = data.get("how", f"The deposit covers {ptxt}. Boats and ferries go fast in high season, so it is worth locking them in early.")
    out.append(f'<div class="cta">{btn}<p class="muted">{how}</p></div>')
    if data.get("status") != "paid":
        lock = data.get("lock_by", "December 15, 2026")
        out.append('<div class="lock"><p class="ey" style="font-size:13px">Best to lock this in by ' + lock + '</p>'
                   '<p>Boat and ferry prices are live until they are booked, and the best boats and sailings for next summer go first. '
                   f'The deposit holds everything at today\'s prices, and the rest is not due until {nice_date(due)}.</p></div>')
    if data.get("pending_note"):
        out.append(f'<p class="note" style="margin-top:20px">{data["pending_note"]}</p>')
    opts = data.get("optional", [])
    if opts:
        out.append('<div class="card" style="margin-top:40px;gap:0">'
                   f'<p class="lbl" style="padding-bottom:10px">{esc(data.get("optional_title", "Add-ons, if you want them"))}</p>')
        out.extend(lg_row(it) for it in opts)
        out.append('<p class="muted" style="padding-top:14px;font-size:15px">' + data.get(
            "optional_note", "Not in the total above. Tell me and I will add any of these before you pay.") + '</p></div>')
    fine = [
        "Transfers, cars and experiences: €300 of the deposit is non-refundable if you cancel. "
        "From 30 to 21 days before arrival 30% is charged, 20 to 14 days 60%, and 13 days or less 100%.",
        "Ferry tickets are fully refundable up to 15 days before sailing, and the date can be changed within 2027.",
    ] + data.get("fine_after_ferry", []) + [
        data.get("fine_boat") or ("Boat days: 30% on confirmation, the rest plus VAT and fuel 30 days before arrival, with the same 30%, 60%, 100% scale inside 30 days. "
                                  "If the captain or port authority cancels for weather, you get it back less a €250 to €300 handling fee. "
                                  "Fuel can move with the market; you hear about any change in advance."),
        "Crew tips are not included; 10 to 15% is customary.",
        "Everything is arranged by Original Senses, my partner in Athens, under their full terms. Any change made once you are in Greece is charged in full.",
    ] + data.get("fine_extra", [])
    out.append('<details class="fine"><summary>Payment &amp; cancellation terms</summary><ul>' +
               "".join(f"<li>{f}</li>" for f in fine) + '</ul></details>')
    out.append('</div></section>')
    return "".join(out), total, dep, bal, due, btn


def next_steps(t, btn):
    steps = "".join(f'<div><p class="num">{i}</p><p>{s}</p></div>' for i, s in enumerate(t["next"], 1))
    return (
        '<section class="band b-ink" style="padding-bottom:120px"><div class="w stack" style="gap:32px">'
        '<p class="ey">Next steps</p>'
        f'<h2 style="font-size:clamp(2.2rem,5vw,3.6rem);line-height:1.02;max-width:820px">{t["next_title"]}</h2>'
        f'<div class="steps">{steps}</div>'
        f'<div class="cta" style="margin-top:8px">{btn.replace("btn off", "btn off")}</div>'
        '<div class="sig"><div style="display:flex;align-items:center;gap:18px">'
        '<img src="/images/personal/keith-headshot-square.jpg" alt="Keith Pence, luxury travel advisor" width="320" height="320" loading="lazy">'
        f'<p style="font-family:{SERIF};font-size:28px">Keith Pence <em style="color:#BE975A">· Suites With Keith</em></p></div>'
        f'<p class="lbl" style="align-self:center">+1 (415) 272-4316 · keith.pence@fora.travel</p></div>'
        '</div></section>')


SUPPORT_DEFAULT = [
    ("24/7 while you travel", "Original Senses, my partner in Athens, monitors every flight, ferry and transfer while you are in Greece and is on call around the clock. If a ferry is delayed or the weather turns, they rebook and move your drivers before you have to ask."),
    ("Dining and beach clubs", "Once restaurants and beach clubs open their books for the 2027 season, we will help you book the tables and beds you want, from a long lunch by the water to the dress-up dinner."),
    ("Me, the whole way", "I stay your point person before and during the trip, with the hotels and Original Senses on the other end of every request."),
]


def support(t):
    items = t.get("support", SUPPORT_DEFAULT)
    cols = "".join(f'<div><p class="ey" style="font-size:13px">{h}</p><p style="margin-top:10px">{b}</p></div>' for h, b in items)
    return (
        '<section class="band b-stone"><div class="w stack" style="gap:32px">'
        '<div class="stack" style="gap:12px"><p class="ey">While you\'re in Greece</p>'
        '<h2>Looked after, <em>start to finish</em></h2></div>'
        f'<div class="steps support">{cols}</div></div></section>')


def ideas(t):
    items = t.get("ideas")
    if not items:
        return ""
    cards = "".join(
        f'<div><p class="ey" style="font-size:13px">{i["heading"]}</p>'
        f'<p style="font-family:{SERIF};font-size:26px;line-height:1.15;margin-top:10px">{i["title"]}</p>'
        f'<p style="margin-top:10px">{i["note"]}</p></div>'
        for i in items)
    return (
        '<section class="band b-cream"><div class="w stack" style="gap:32px">'
        '<div class="stack" style="gap:12px;max-width:760px"><p class="ey">Worth adding</p>'
        f'<h2>{t.get("ideas_title", "A few <em>ideas</em>")}</h2>'
        f'{"<p>" + t["ideas_intro"] + "</p>" if t.get("ideas_intro") else ""}</div>'
        f'<div class="steps support">{cards}</div></div></section>')


def render(t):
    data = json.loads((ROOT / t["logistics"]).read_text())
    lg, total, dep, bal, due, btn = logistics(t, data)
    bgs = t.get("stay_bands", ["b-stone", "b-cream", "b-ink", "b-stone", "b-cream", "b-ink"])
    stays = "".join(stay(s, bgs[i % len(bgs)]) for i, s in enumerate(t["stays"]))
    body = header(t) + route(t) + days(t) + stays + flights(t) + lg + ideas(t) + support(t) + next_steps(t, btn)
    page = (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="robots" content="noindex, nofollow">\n'
        f'<title>{t["title"]}</title>\n'
        '<meta name="description" content="A private itinerary from Suites With Keith.">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&amp;family=Newsreader:ital,wght@0,400;1,400&amp;display=swap" rel="stylesheet">\n'
        f'<style>{CSS}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n')
    return page, total, dep, bal, due


def main():
    for arg in sys.argv[1:]:
        t = json.loads(Path(arg).read_text())
        page, total, dep, bal, due = render(t)
        if "—" in page or "&mdash;" in page:
            sys.exit(f"em dash in {arg}")
        (ROOT / t["page"]).write_text(page)
        print(f'{t["page"]}: logistics {eur(total)}, deposit {eur(dep)}, balance {eur(bal)} due {due}')


if __name__ == "__main__":
    main()
