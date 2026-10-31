#!/usr/bin/env python3
"""Render an unlisted client itinerary page from proposals/data/<slug>.json.

Output is static HTML at proposals/<slug>.html in the jc-* itinerary design
(tools/itinerary/jc-base.css and jc-base.js are lifted from the Ham & Hogue page).
All trip content lives in the JSON. This repo is public, so keep the JSON
client-safe: no client emails or phones, no prices, no internal notes.

Multiple stays: give "hotels" (a list) instead of "hotel". A hotel can carry
"bookings" ([{label, ref, status, check_in, check_out}]) in place of a single
"confirmation", for a stay split across reservations. meta.timezone sets the
Today highlight (default America/Los_Angeles).

meta.build:
  draft  amber "To be confirmed" chips plus dashed "For Keith" notes (keith_todo)
  final  chips only where a status is still open, "For Keith" notes hidden

Usage:  python3 tools/render_itinerary.py <slug>
"""
import datetime, html, json, pathlib, re, sys, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[1]
QUIET = {'confirmed', 'info', 'arranged_by_client', 'client_self_arranged'}
ORD = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']


def e(s):
    s = html.escape(str(s), quote=False).replace("'", '&rsquo;').replace('·', '&middot;')
    return s


def tel(num, scheme='tel'):
    digits = re.sub(r'\D', '', num)
    if len(digits) == 10:
        digits = '1' + digits
    return '%s:+%s' % (scheme, digits)


def maps(q):
    return 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(q, safe='')


def day_bits(iso):
    d = datetime.date.fromisoformat(iso)
    return d, d.strftime('%A'), d.strftime('%B'), d.day, d.strftime('%b')


def day_id(iso):
    d = datetime.date.fromisoformat(iso)
    return '%s-%d' % (d.strftime('%b').lower(), d.day)


def long_date(iso):
    d, wd, month, n, _ = day_bits(iso)
    return '%s, %s %d' % (wd, month, n)


def pin(b):
    """A bullet or stop: plain text, or {text, maps_query} with a Map pin link."""
    if isinstance(b, str):
        return e(b)
    out = e(b.get('text', ''))
    if b.get('maps_query'):
        out += ' <a class="jc-pin" href="%s" target="_blank" rel="noopener">Map</a>' % maps(b['maps_query'])
    return out


def render_event(ev, draft):
    status = ev.get('status', 'info')
    pending = status not in QUIET
    w = []
    if pending:
        w.append('<span class="jc-tbc">%s</span>' % e(ev.get('pending_label', 'To be confirmed')))
    if ev.get('traveler'):
        w.append('<span class="jc-who">%s</span>' % e(ev['traveler']))
    w.append('<strong class="jc-title">%s</strong>' % e(ev['title']))
    if status == 'confirmed':
        w.append('<span class="jc-ok" title="Confirmed">&#10003; Confirmed</span>')
    if ev.get('details'):
        w.append('<span class="jc-line">%s</span>' % e(ev['details']))
    if ev.get('bullets'):
        w.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % pin(b) for b in ev['bullets']))
    if ev.get('stops'):
        w.append('<ul class="jc-stops">%s</ul>' % ''.join(
            '<li><strong>%s</strong>%s</li>' % (
                e(' '.join(x for x in (s.get('time'), s['name']) if x)),
                pin({'text': '', 'maps_query': s.get('maps_query')}) + ((' <span class="jc-line">%s</span>' % e(s['note'])) if s.get('note') else ''))
            for s in ev['stops']))
    if ev.get('keith_note'):
        w.append('<span class="jc-note">%s</span>' % e(ev['keith_note']))
    meta = []
    if ev.get('location'):
        loc = e(ev['location'])
        if ev.get('maps_query'):
            loc += ' <a href="%s" target="_blank" rel="noopener">Map</a>' % maps(ev['maps_query'])
        meta.append(loc)
    if ev.get('distance'):
        meta.append(e(ev['distance']))
    bits = []
    if ev.get('party'):
        bits.append('Table for %d' % ev['party'] if ev.get('type') in ('dinner', 'lunch') else '%d guests' % ev['party'])
    if ev.get('seating'):
        bits.append(e(ev['seating']))
    if ev.get('booked_under'):
        bits.append('Booked under %s' % e(ev['booked_under']))
    if bits:
        meta.append(' &middot; '.join(bits))
    if ev.get('phone'):
        label = e(ev.get('phone_label', 'Call'))
        meta.append('%s <a class="jc-tel" href="%s">%s</a>' % (label, tel(ev['phone']), e(ev['phone'])))
    if ev.get('link'):
        meta.append('<a href="%s" target="_blank" rel="noopener">%s</a>' % (e(ev['link']), e(ev.get('link_label', 'Website'))))
    for m in meta:
        w.append('<span class="jc-meta">%s</span>' % m)
    if ev.get('confirmation'):
        ref = e(ev['confirmation'])
        if ev.get('paid_note'):
            ref += ' &middot; ' + e(ev['paid_note'])
        w.append('<span class="jc-ref">%s</span>' % ref)
    if draft and ev.get('keith_todo'):
        w.append('<span class="jc-todo"><b>For Keith</b> %s</span>' % e(ev['keith_todo']))
    cls = 'jc-item' + (' is-pending' if pending else '')
    return '          <div class="%s"><span class="time">%s</span><span class="what">%s</span></div>' % (
        cls, e(ev['time']), ''.join(w))


def stay_refs(h):
    """One entry per reservation on a stay: the single confirmation, or each of h['bookings']."""
    out = []
    for b in h.get('bookings') or [{'ref': h['confirmation']}]:
        label = (e(b['label']) + ' &middot; ') if b.get('label') else ''
        if b.get('status', 'confirmed') in QUIET:
            ref = e(b['ref'])
            body = label + 'Confirmation ' + ref
        else:
            ref = '<span class="jc-tbc">%s</span>%s' % (e(b.get('pending_label', 'To be confirmed')), e(b.get('ref', '')))
            body = '<span class="jc-tbc">%s</span>%s%s' % (e(b.get('pending_label', 'To be confirmed')), label, e(b.get('ref', '')))
        out.append({'html': body, 'ref_only': ref,
                    'check_in': b.get('check_in', h['check_in']), 'check_out': b.get('check_out', h['check_out'])})
    return out


def render(data):
    m, days, k = data['meta'], data['days'], data['keith']
    hotels = data.get('hotels') or [data['hotel']]
    draft = m.get('build', 'draft') == 'draft'
    base_css = (ROOT / 'tools/itinerary/jc-base.css').read_text()
    extra_css = (ROOT / 'tools/itinerary/itinerary-extra.css').read_text()
    base_js = (ROOT / 'tools/itinerary/jc-base.js').read_text()
    today_js = (ROOT / 'tools/itinerary/today.js').read_text()

    o = []
    a = o.append
    a('''<!DOCTYPE html>
<html lang="en" class="js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>%s | Suites With Keith</title>
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="icon" href="../favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<link rel="stylesheet" href="../styles.css">
<!-- Generated by tools/render_itinerary.py from proposals/data/%s.json. Edit the JSON, not this file. -->
<style>
%s
%s</style>
<noscript><style>.jc-daysec, .jc-hero .inner > * { opacity: 1 !important; transform: none !important; } .jc-datebar { display: none; }</style></noscript>
</head>
<body%s data-tz="%s">
''' % (e(m['page_title']), m['slug'], base_css, extra_css, ' class="is-draft"' if draft else '',
       e(m.get('timezone', 'America/Los_Angeles'))))

    if draft:
        a('<div class="jc-draftbar">Draft for Keith &middot; not yet sent to the clients</div>\n')

    a('''<header class="jc-hero">
  <img src="%s" alt="%s" style="object-position: 50%% 60%%;">
  <div class="shade"></div>
  <div class="inner">
    <span class="jc-eyebrow">%s</span>
    <h1>%s <em>%s</em></h1>
    <p>%s</p>
  </div>
  <span class="cue" aria-hidden="true"></span>
</header>
''' % (m['hero_image'], e(m['hero_alt']), e(m['hero_eyebrow']), e(m['hero_names']), e(m['hero_place']), e(m['hero_line'])))

    a('''
<section class="jc-intro">
  <div class="jc-container">
    <div class="grid">
      <div><span class="jc-eyebrow">%s</span></div>
      <div>
        <p>%s</p>
        <p class="small">%s</p>
        <div class="jc-numbers">
          <div><span class="lbl">Keith, anytime</span><a href="%s">%s</a><span class="note">Call or <a class="inline" href="%s">text</a></span></div>
%s
        </div>
      </div>
    </div>
  </div>
</section>
''' % (e(m['intro_eyebrow']), e(m['hello']), e(m['how_to_read']),
       tel(k['phone']), e(k['phone'].replace('+1.', '').replace('.', '-')), tel(k['phone'], 'sms'),
       '\n'.join('          <div><span class="lbl">%s</span><a href="%s">%s</a><span class="note">%s</span></div>' % (
           e(h.get('short_name', h['name'])), tel(h['phone_voice']), e(h['phone_voice'].replace('.', '-')),
           ('Front desk &middot; or <a class="inline" href="%s">text %s</a>' % (tel(h['phone_text'], 'sms'), e(h['phone_text'].replace('.', '-'))))
           if h.get('phone_text') else 'Front desk')
           for h in hotels)))

    # At a glance: hotel card + day strip
    a('''
<section class="jc-strip" id="days">
  <div class="jc-container">
    <span class="jc-eyebrow">At a Glance</span>
''')
    for h in hotels:
        lines = ['      <div class="jc-label">%s</div>' % e(h.get('label', 'Your hotel, %d nights' % h['nights'])),
                 '      <div class="hotel"><a href="%s" target="_blank" rel="noopener">%s</a></div>' % (e(h['website']), e(h['name']))]
        room = ('<strong>%s.</strong>' % e(h['room'])) if h.get('room') else ''
        if h.get('room_details'):
            room += ' %s.' % e(h['room_details'])
        if room:
            lines.append('      <div class="hotel-note">%s</div>' % room.strip())
        lines.append('      <div class="hotel-note">%s <a class="jc-maplink" href="%s" target="_blank" rel="noopener">Map</a></div>' % (e(h['address']), maps(h['maps_query'])))
        lines.append('      <div class="hotel-note">Check in <strong>%s</strong> &middot; Check out <strong>%s</strong></div>' % (long_date(h['check_in']), long_date(h['check_out'])))
        call = 'Call <a class="jc-tel" href="%s">%s</a>' % (tel(h['phone_voice']), e(h['phone_voice'].replace('.', '-')))
        if h.get('phone_text'):
            call += ' &middot; Text <a class="jc-tel" href="%s">%s</a>' % (tel(h['phone_text'], 'sms'), e(h['phone_text'].replace('.', '-')))
        lines.append('      <div class="hotel-note">%s</div>' % call)
        for b in stay_refs(h):
            lines.append('      <div class="jc-ref">%s</div>' % b['html'])
        if draft and h.get('keith_todo'):
            lines.append('      <span class="jc-todo"><b>For Keith</b> %s</span>' % e(h['keith_todo']))
        a('    <div class="jc-hotel jc-glance">\n%s\n    </div>\n' % '\n'.join(lines))
    a('''    <span class="jc-eyebrow">Tap a Day</span>
    <div class="grid" style="margin-top:18px;">
''')
    for d in days:
        _, wd, _, n, mon = day_bits(d['date'])
        a('      <a class="cell" href="#%s" data-date="%s"><span class="num">%s</span><div class="dates">%s %d</div><div class="place">%s</div></a>\n'
          % (day_id(d['date']), d['date'], wd[:3], mon, n, e(d['strip_label'])))
    a('    </div>\n  </div>\n</section>\n\n')

    a('<nav class="jc-datebar" id="datebar" aria-label="Jump to a day"><div class="row">')
    for d in days:
        _, wd, _, n, mon = day_bits(d['date'])
        a('<a href="#%s"><b>%d</b>%s</a>' % (day_id(d['date']), n, mon))
    a('<a href="#confirmations" class="x">Confirmations</a></div></nav>\n')

    for i, d in enumerate(days):
        _, wd, month, n, _ = day_bits(d['date'])
        a('''
<section class="jc-daysec" id="%s" data-date="%s">
  <div class="jc-container">
    <div class="grid solo">
      <article class="copy">
        <span class="jc-eyebrow">Day %02d &middot; %s <span class="jc-today" hidden>Today</span></span>
        <h2>%s %d</h2>
        <p class="sub">%s</p>
        <p class="jc-summary">%s</p>
''' % (day_id(d['date']), d['date'], i + 1, wd, month, n, e(d['title']), e(d['summary'])))
        a('\n'.join(render_event(ev, draft) for ev in d['events']))
        a('''
        <a class="jc-back" href="#days">&uarr; All days</a>
      </article>
    </div>
  </div>
</section>
''')

    # Good to know
    a('''
<section class="jc-section" id="notes" style="padding-top:80px; border-top:1px solid var(--hairline);">
  <div class="jc-container">
    <span class="jc-eyebrow">The Fine Print</span>
    <h2>Good to know</h2>
    <div class="jc-transfers">
''')
    for g in data['good_to_know']:
        a('      <div class="jc-card"><div class="route" style="margin-top:0;">%s</div><p class="detail">%s</p></div>\n' % (e(g['title']), e(g['text'])))
    a('    </div>\n  </div>\n</section>\n')

    # Confirmations: open in the markup (no-JS and print), collapsed by script on load
    a('''
<section class="jc-section" id="confirmations">
  <div class="jc-container">
    <span class="jc-eyebrow">Everything in One Place</span>
    <details class="jc-fold" open>
      <summary><h2>Your confirmations</h2><span class="jc-fold-cue" aria-hidden="true"></span></summary>
      <div class="jc-confirm-grid">
        <div class="jc-confirm-col">
          <div class="title">Stay</div>
''')
    for h in hotels:
        for b in stay_refs(h):
            a('''          <div class="jc-confirm">
            <div class="name">%s</div>
            <div class="when">%s to %s &middot; %s</div>
            <div class="ref">%s</div>
          </div>
''' % (e(h['name']), long_date(b['check_in']), long_date(b['check_out']), e(h.get('room', '%d nights' % h['nights'])), b['ref_only']))
    a('''        </div>
        <div class="jc-confirm-col">
          <div class="title">Bookings</div>
''')
    for d in days:
        for ev in d['events']:
            if ev.get('type') == 'hotel' or not (ev.get('confirmation') or ev.get('status') not in QUIET):
                continue
            if ev.get('type') in ('arrival', 'free', 'lunch') and not ev.get('confirmation'):
                continue
            pending = ev.get('status') not in QUIET
            ref = e(ev.get('confirmation', ''))
            if pending and not (ev.get('pending_label') and ev.get('confirmation')):
                ref = '<span class="jc-tbc">To be confirmed</span>' + ((' ' + ref) if ref else '')
            under = (' &middot; under %s' % e(ev['booked_under'])) if ev.get('booked_under') else ''
            a('''          <div class="jc-confirm">
            <div class="name">%s</div>
            <div class="when">%s, %s%s</div>
            <div class="ref">%s</div>
          </div>
''' % (e(ev['title']), long_date(d['date']), e(ev['time']), under, ref))
    a('''        </div>
        <div class="jc-confirm-col jc-contact">
          <div class="title">Who to call</div>
''')
    for c in data['contacts']:
        lines = []
        for ln in c['lines']:
            num = ln.get('tel') or ln.get('sms')
            lines.append('%s <a href="%s">%s</a>' % (e(ln['label']), tel(num, 'sms' if ln.get('sms') else 'tel'), e(num)))
        note = ('<div class="when">%s</div>' % e(c['note'])) if c.get('note') else ''
        a('''          <div class="jc-confirm">
            <div class="name">%s</div>%s
            <div class="when">%s</div>
          </div>
''' % (e(c['name']), note, ' &middot; '.join(lines)))
    a('''        </div>
      </div>
    </details>
  </div>
</section>
''')

    # Keith
    a('''
<section class="jc-support" id="keith">
  <div class="jc-container">
    <div class="grid">
      <div>
        <span class="jc-eyebrow">While You&rsquo;re There</span>
        <div class="big">%s</div>
      </div>
      <div>
        <p>%s</p>
        <div class="jc-phone-row">
          <span class="label">Call or text</span>
          <a href="%s">%s</a>
        </div>
        <div class="jc-actions">
          <a href="%s">Call</a><a href="%s">Text</a><a href="mailto:%s">Email</a><a href="https://%s" target="_blank" rel="noopener">%s</a><a href="https://www.instagram.com/%s/" target="_blank" rel="noopener">@%s</a>
        </div>
        <div class="jc-sig">%s &middot; %s<br><a href="mailto:%s">%s</a></div>
      </div>
    </div>
  </div>
</section>

<footer class="jc-footer">
  Suites With Keith &middot; Curated by Keith Pence<br>
  This page updated %s</footer>

<script>
%s
%s</script>
</body>
</html>
''' % (e(k['headline']), e(k['note']), tel(k['phone']), e(k['phone'].replace('+1.', '')),
       tel(k['phone']), tel(k['phone'], 'sms'), e(k['email']), e(k['website']), e(k['website']),
       e(k['instagram']), e(k['instagram']), e(k['name']), e(k['title']), e(k['email']), e(k['email']),
       datetime.date.fromisoformat(m['updated']).strftime('%B %-d, %Y'), base_js, today_js))

    out = ''.join(o)
    for bad in ('—', '&mdash;', '–', '&ndash;'):
        assert bad not in out, 'dash found in output: %r' % bad
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    slug = sys.argv[1]
    data = json.loads((ROOT / 'proposals/data' / (slug + '.json')).read_text())
    assert data['meta']['slug'] == slug
    dest = ROOT / 'proposals' / (slug + '.html')
    dest.write_text(render(data))
    print('wrote', dest.relative_to(ROOT), '(%s build)' % data['meta'].get('build', 'draft'))


if __name__ == '__main__':
    main()
