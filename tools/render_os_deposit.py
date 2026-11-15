#!/usr/bin/env python3
"""Render the Original Senses deposit block ("Secure the logistics") into a proposal page.

Data lives in tools/os_deposits/<page>.json. The block is written between
<!-- os-deposit --> and <!-- /os-deposit --> markers in the target page.

For bundled-export pages (dc-runtime), pass --inject: the block is written into
an outer-shell <script id="os-deposit-inject"> that inserts it into the rendered
page after unpack and re-inserts it if the runtime re-renders.

Usage:
  python3 tools/render_os_deposit.py tools/os_deposits/17e9e4f4c65ee639.json
  python3 tools/render_os_deposit.py tools/os_deposits/allison-noah-greece-2027.json --inject

Deposit maths follow the Original Senses payment policy:
  ground services (transfers, cars, experiences, insurance) 25%,
  ferry tickets 100%, private boat charters 30%.
Set "deposit" in the JSON to override with the exact amount on the payment link.
"""
import html
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RATES = {"ground": 0.25, "ferry": 1.0, "boat": 0.30}
GROUP_TITLES = {
    "transfers": "Private transfers",
    "ferries": "Ferries",
    "boats": "Boat days",
    "cars": "Car rental",
    "experiences": "Experiences",
    "other": "Travel insurance",
}
GROUP_ORDER = ["transfers", "ferries", "boats", "cars", "experiences", "other"]
KIND_OF_GROUP = {"transfers": "ground", "cars": "ground", "experiences": "ground",
                 "other": "ground", "ferries": "ferry", "boats": "boat"}

CSS = """
.osd{max-width:900px;margin:0 auto;padding:56px 40px 0;font-family:'Newsreader',Georgia,'Times New Roman',serif;color:#1F201A}
.osd *{box-sizing:border-box}
.osd-eyebrow{font-family:'Instrument Serif',Didot,Georgia,serif;font-size:.76rem;text-transform:uppercase;letter-spacing:.2em;color:#836229;margin:0 0 10px}
.osd h2.osd-h{font-family:'Instrument Serif',Didot,Georgia,serif;font-weight:400;font-size:1.8rem;line-height:1.15;margin:0 0 8px;color:#1F201A}
.osd-intro{font-size:.96rem;color:#65665C;line-height:1.6;margin:0 0 20px;max-width:640px}
.osd-card{border:1px solid rgba(22,23,18,.15);background:#FBFAF6;padding:8px 28px 24px}
.osd-gh{font-family:'Instrument Serif',Didot,Georgia,serif;font-size:.72rem;text-transform:uppercase;letter-spacing:.2em;color:#836229;border-bottom:1px solid rgba(22,23,18,.15);padding:18px 0 8px}
.osd-row{display:grid;grid-template-columns:110px 1fr auto;gap:16px;border-bottom:1px solid rgba(22,23,18,.08);padding:12px 0}
.osd-date{font-family:'Instrument Serif',Didot,Georgia,serif;font-size:.74rem;text-transform:uppercase;letter-spacing:.16em;color:#836229;padding-top:3px}
.osd-t{font-size:1rem;line-height:1.4}
.osd-n{font-size:.86rem;color:#65665C;line-height:1.5;margin-top:3px}
.osd-p{font-family:'Instrument Serif',Didot,Georgia,serif;font-size:1.05rem;white-space:nowrap;text-align:right;padding-top:1px}
.osd-p.pending{font-family:'Newsreader',Georgia,serif;font-size:.8rem;color:#8C8D82;font-style:italic}
.osd-sum{margin-top:22px;display:grid;grid-template-columns:1fr 1fr 1fr;border:1px solid rgba(22,23,18,.15)}
.osd-sum>div{padding:16px 18px;border-right:1px solid rgba(22,23,18,.15)}
.osd-sum>div:last-child{border-right:none}
.osd-sum .now{background:#161712;color:#F2EFE6}
.osd-k{font-family:'Instrument Serif',Didot,Georgia,serif;font-size:.68rem;text-transform:uppercase;letter-spacing:.2em;color:#8C8D82}
.osd-sum .now .osd-k{color:#BE975A}
.osd-v{font-family:'Instrument Serif',Didot,Georgia,serif;font-size:1.7rem;line-height:1.2;margin-top:4px}
.osd-s{font-size:.82rem;color:#65665C;margin-top:2px;line-height:1.4}
.osd-sum .now .osd-s{color:#9A9B90}
.osd-cta{display:flex;flex-wrap:wrap;align-items:center;gap:14px 20px;margin-top:20px}
.osd-btn{display:inline-block;background:#836229;color:#FBFAF6 !important;text-decoration:none !important;border:none !important;font-family:'Instrument Serif',Didot,Georgia,serif;font-size:.8rem;text-transform:uppercase;letter-spacing:.2em;padding:15px 26px}
.osd-btn:hover{background:#4A5040}
.osd-btn.off{background:transparent;color:#8C8D82 !important;border:1px solid #8C8D82 !important;cursor:default}
.osd-btn.paid{background:transparent;color:#4A5040 !important;border:1px solid #4A5040 !important;cursor:default}
.osd-how{font-size:.84rem;color:#65665C;line-height:1.5;flex:1 1 260px}
.osd-opt{margin-top:20px;border:1px dashed rgba(22,23,18,.25);padding:8px 28px 18px}
.osd-opt .osd-row:last-child{border-bottom:none}
.osd-opt-note{font-size:.86rem;color:#65665C;margin:12px 0 0}
.osd-fine{margin-top:18px;border-top:1px solid rgba(22,23,18,.15)}
.osd-fine summary{cursor:pointer;font-family:'Instrument Serif',Didot,Georgia,serif;font-size:.74rem;text-transform:uppercase;letter-spacing:.2em;color:#836229;padding:14px 0;list-style:none}
.osd-fine summary::-webkit-details-marker{display:none}
.osd-fine summary:after{content:' +'}
.osd-fine[open] summary:after{content:' \\2212'}
.osd-fine ul{margin:0 0 8px;padding-left:18px;font-size:.88rem;color:#65665C;line-height:1.55}
.osd-fine li{margin-bottom:6px}
@media(max-width:700px){
 .osd{padding:44px 20px 0}
 .osd-card,.osd-opt{padding-left:18px;padding-right:18px}
 .osd-sum{grid-template-columns:1fr}
 .osd-sum>div{border-right:none;border-bottom:1px solid rgba(22,23,18,.15)}
 .osd-sum>div:last-child{border-bottom:none}
 .osd-sum .now{order:-1}
}
@media(max-width:560px){
 .osd-row{grid-template-columns:1fr auto;gap:2px 12px}
 .osd-date{grid-column:1 / -1;padding-top:0}
 .osd-btn{width:100%;text-align:center}
}
"""


def eur(x):
    x = round(x + 1e-9, 2)
    if abs(x - round(x)) < 0.005:
        return "€{:,.0f}".format(x)
    return "€{:,.2f}".format(x)


def esc(s):
    return html.escape(s, quote=True)


def nice_date(d):
    return d.strftime("%b ") + str(d.day) + d.strftime(", %Y")


def compute(data):
    total = 0.0
    dep = 0.0
    for g in GROUP_ORDER:
        for it in data.get("items", {}).get(g, []):
            if it.get("price") is None:
                continue
            total += it["price"]
            dep += it["price"] * RATES[it.get("kind", KIND_OF_GROUP[g])]
    if data.get("total") is not None and abs(data["total"] - total) > 0.01:
        sys.exit(f"total mismatch: items add to {total}, JSON says {data['total']}")
    if data.get("deposit") is not None:
        dep = data["deposit"]
    return total, round(dep, 2)


def row(it):
    price = it.get("price")
    p = f'<div class="osd-p">{eur(price)}</div>' if price is not None else \
        f'<div class="osd-p pending">{esc(it.get("price_note", "Being priced"))}</div>'
    note = f'<div class="osd-n">{it["note"]}</div>' if it.get("note") else ""
    return (f'<div class="osd-row"><div class="osd-date">{esc(it.get("date", ""))}</div>'
            f'<div><div class="osd-t">{it["title"]}</div>{note}</div>{p}</div>')


def render(data):
    total, dep = compute(data)
    arrive = date.fromisoformat(data["arrival"])
    due = arrive - timedelta(days=30)
    bal = total - dep
    w = f' style="max-width:{data["width"]}px"' if data.get("width") else ""
    out = [f'<section class="osd" id="deposit"{w}><style>{CSS.strip()}</style>']
    out.append('<div class="osd-eyebrow">Ferries, transfers &amp; boat days</div>')
    out.append(f'<h2 class="osd-h">{data.get("heading", "Securing the <em>logistics</em>")}</h2>')
    out.append(f'<p class="osd-intro">{data["intro"]}</p>')
    out.append('<div class="osd-card">')
    for g in GROUP_ORDER:
        items = data.get("items", {}).get(g, [])
        if not items:
            continue
        out.append(f'<div class="osd-gh">{esc(data.get("group_titles", {}).get(g, GROUP_TITLES[g]))}</div>')
        out.extend(row(it) for it in items)
    out.append('<div class="osd-sum">')
    out.append(f'<div><div class="osd-k">Trip total</div><div class="osd-v">{eur(total)}</div>'
               f'<div class="osd-s">{esc(data.get("total_note", "Everything above, for two"))}</div></div>')
    out.append(f'<div class="now"><div class="osd-k">Deposit now</div><div class="osd-v">{eur(dep)}</div>'
               f'<div class="osd-s">Confirms everything above</div></div>')
    out.append(f'<div><div class="osd-k">Balance</div><div class="osd-v">{eur(bal)}</div>'
               f'<div class="osd-s">Due by {nice_date(due)}, 30 days before you arrive</div></div>')
    out.append('</div>')
    status = data.get("status", "pending")
    if status == "paid":
        btn = '<span class="osd-btn paid">Deposit received, thank you</span>'
    elif data.get("pay_url"):
        btn = (f'<a class="osd-btn" href="{esc(data["pay_url"])}" target="_blank" rel="noopener">'
               f'Pay the {eur(dep)} deposit</a>')
    else:
        btn = '<span class="osd-btn off">Payment link on its way</span>'
    items = data.get("items", {})
    ground = [w for g, w in (("transfers", "transfers"), ("cars", "cars"), ("experiences", "experiences")) if items.get(g)]
    parts = []
    if ground:
        gtxt = ground[0] if len(ground) == 1 else ", ".join(ground[:-1]) + " and " + ground[-1]
        parts.append(f"25% of {gtxt}")
    if items.get("ferries"):
        parts.append("the full ferry fare" + ("s" if len(items["ferries"]) > 1 else ""))
    if items.get("boats"):
        parts.append("30% of " + ("each boat day" if len(items["boats"]) > 1 else "the boat day"))
    ptxt = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]
    how = data.get("how", f"The deposit covers {ptxt}. Nothing is booked until it is paid, and boats and ferries go fast in high season.")
    out.append(f'<div class="osd-cta">{btn}<div class="osd-how">{how}</div></div>')
    if data.get("pending_note"):
        out.append(f'<p class="osd-opt-note">{data["pending_note"]}</p>')
    out.append('</div>')
    opts = data.get("optional", [])
    if opts:
        out.append('<div class="osd-opt"><div class="osd-gh">' +
                   esc(data.get("optional_title", "Add-ons, if you want them")) + '</div>')
        out.extend(row(it) for it in opts)
        out.append('<p class="osd-opt-note">' + data.get(
            "optional_note", "Not in the total above. Tell me and I will add any of these before you pay.") + '</p></div>')
    fine = [
        "Transfers, cars and experiences: €300 of the deposit is non-refundable if you cancel. "
        "From 30 to 21 days before arrival 30% is charged, 20 to 14 days 60%, and 13 days or less 100%.",
        "Ferry tickets are fully refundable up to 15 days before sailing, and the date can be changed within 2027.",
        "Boat days: 30% on confirmation, the rest plus VAT and fuel 30 days before arrival, with the same 30%, 60%, 100% scale inside 30 days. "
        "If the captain or port authority cancels for weather, you get it back less a €250 to €300 handling fee. "
        "Fuel can move with the market; you hear about any change in advance.",
        "Crew tips are not included; 10 to 15% is customary.",
        "Everything is arranged by Original Senses, my partner in Athens, under their full terms. Any change made once you are in Greece is charged in full.",
    ] + data.get("fine_extra", [])
    out.append('<details class="osd-fine"><summary>Payment &amp; cancellation terms</summary><ul>' +
               "".join(f"<li>{f}</li>" for f in fine) + '</ul></details>')
    out.append('</section>')
    return "".join(out), total, dep, bal, due


def main():
    src = Path(sys.argv[1])
    data = json.loads(src.read_text())
    block, total, dep, bal, due = render(data)
    if "—" in block:
        sys.exit("em dash in block")
    page = ROOT / data["page"]
    text = page.read_text()
    if "--inject" in sys.argv:
        js_block = json.dumps(block).replace("</", "<\\/")
        anchor = json.dumps(data["inject_before"])
        script = (
            '<script id="os-deposit-inject">(function(){var B=' + js_block + ',A=' + anchor + ';'
            'function put(){if(document.getElementById("deposit"))return;var t=document.querySelector(A);'
            'if(!t||!t.parentElement)return;var w=document.createElement("div");w.innerHTML=B;'
            't.parentElement.insertBefore(w.firstChild,t);if(location.hash==="#deposit")w=null;}'
            'setInterval(put,500);})();</script>'
        )
        new, n = re.subn(r'<script id="os-deposit-inject">.*?</script>', lambda m: script, text, flags=re.S)
        if n == 0:
            new = text.replace("</head>", script + "</head>", 1)
    else:
        pat = re.compile(r"<!-- os-deposit -->.*?<!-- /os-deposit -->", re.S)
        if not pat.search(text):
            sys.exit(f"no <!-- os-deposit --> markers in {page}")
        new = pat.sub(lambda m: "<!-- os-deposit -->" + block + "<!-- /os-deposit -->", text)
    page.write_text(new)
    print(f"{page.name}: total {eur(total)}, deposit {eur(dep)}, balance {eur(bal)} due {due}")


if __name__ == "__main__":
    main()
