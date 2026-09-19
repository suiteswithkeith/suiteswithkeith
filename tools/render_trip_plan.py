#!/usr/bin/env python3
"""Render Keith's research-trip working plan from proposals/data/<slug>.json.

Output is static HTML at proposals/<slug>.html in the jc-* itinerary design
(tools/itinerary/jc-base.css, itinerary-extra.css, trip-plan.css, jc-base.js).
Unlisted: noindex, not in the sitemap, not linked from anywhere.

One entry per night in blocks[].days[] (plus a final departure day). Nights
whose stay.status is confirmed or paid count toward the confirmed total; the
out-of-pocket total is summed from out_of_pocket[].

Usage:  python3 tools/render_trip_plan.py <slug>
"""
import datetime, html, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DONE = {'confirmed', 'paid'}
LABEL = {
    'confirmed': 'Confirmed', 'paid': 'Confirmed, paid', 'pending': 'Pending', 'open': 'Open',
    'suggested': 'Suggested', 'todo': 'To do', 'fallback': 'Fallback', 'ruled_out': 'Ruled out',
    'departure': 'Departure', 'info': '',
}


def e(s):
    return html.escape(str(s), quote=False).replace("'", '&rsquo;').replace('·', '&middot;')


def chip(status):
    lab = LABEL.get(status, '')
    return '<span class="jc-chip %s">%s</span>' % (status, e(lab)) if lab else ''


def day_bits(iso):
    d = datetime.date.fromisoformat(iso)
    return d, d.strftime('%A'), d.strftime('%B'), d.day, d.strftime('%b')


def long_date(iso):
    _, wd, month, n, _ = day_bits(iso)
    return '%s, %s %d' % (wd, month, n)


def day_id(iso):
    d = datetime.date.fromisoformat(iso)
    return '%s-%d' % (d.strftime('%b').lower(), d.day)


def eur(n):
    return '%s euros' % format(n, ',')


def render_item(it):
    status = it.get('status', 'info')
    w = [chip(status), '<strong class="jc-title">%s</strong>' % e(it['title'])]
    if it.get('detail'):
        w.append('<span class="jc-line">%s</span>' % e(it['detail']))
    if it.get('todo'):
        w.append('<span class="jc-todo"><b>To do</b> %s</span>' % e(it['todo']))
    cls = 'jc-item' + (' is-open' if status == 'open' else '')
    return '          <div class="%s"><span class="time">%s</span><span class="what">%s</span></div>' % (cls, e(it['time']), ''.join(w))


def render_stay(stay):
    status = stay['status']
    o = ['        <div class="jc-stay %s">' % status,
         '          <div class="jc-label">The night</div>',
         '          <div class="hotel">%s%s</div>' % (chip(status), e(stay['name']))]
    if stay.get('detail'):
        o.append('          <div class="hotel-note">%s</div>' % e(stay['detail']))
    if stay.get('options'):
        o.append('          <ul class="jc-options">')
        for op in stay['options']:
            o.append('            <li>%s<strong>%s</strong>%s</li>' % (
                chip(op['status']), e(op['name']),
                (' <span class="jc-line">%s</span>' % e(op['detail'])) if op.get('detail') else ''))
        o.append('          </ul>')
    if stay.get('todo'):
        o.append('          <span class="jc-todo"><b>To do</b> %s</span>' % e(stay['todo']))
    o.append('        </div>')
    return '\n'.join(o)


def render_day(d):
    _, wd, month, n, _ = day_bits(d['date'])
    o = ['      <div class="jc-night" id="%s" data-date="%s">' % (day_id(d['date']), d['date']),
         '        <div class="date">%s <em>%s %d</em> <span class="jc-today" hidden>Today</span></div>' % (wd, month, n)]
    if d.get('label'):
        o.append('        <p class="lab">%s</p>' % e(d['label']))
    if d.get('departure'):
        o.append('        <div class="jc-stay departure"><div class="hotel">%sNo night, trip ends</div></div>' % chip('departure'))
    else:
        o.append(render_stay(d['stay']))
    for it in d.get('items', []):
        o.append(render_item(it))
    if d.get('seen'):
        o.append('        <p class="jc-seen"><b>Properties seen</b>%s</p>' % e(d['seen']))
    o.append('      </div>')
    return '\n'.join(o)


def render_groups(groups):
    o = ['        <div class="jc-groups">']
    for g in groups:
        o.append('          <div class="jc-group"><div class="title">%s</div>' % e(g['title']))
        if g.get('note'):
            o.append('            <p class="gnote">%s</p>' % e(g['note']))
        o.append('            <ul>')
        for it in g['items']:
            o.append('              <li>%s<strong>%s</strong>%s</li>' % (
                chip(it['status']), e(it['name']),
                (' <span class="jc-line">%s</span>' % e(it['detail'])) if it.get('detail') else ''))
        o.append('            </ul>\n          </div>')
    o.append('        </div>')
    return '\n'.join(o)


def render(data):
    m, blocks = data['meta'], data['blocks']
    css = ''.join((ROOT / 'tools/itinerary' / f).read_text() for f in ('jc-base.css', 'itinerary-extra.css', 'trip-plan.css'))
    base_js = (ROOT / 'tools/itinerary/jc-base.js').read_text()
    today_js = (ROOT / 'tools/itinerary/today.js').read_text().replace('America/Los_Angeles', m.get('timezone', 'Europe/Rome'))
    # The plan has no confirmations fold; today.js targets the datebar's confirmations link, keep the selector harmless.
    today_js = today_js.replace('.jc-daysec, #confirmations', '.jc-daysec')

    nights = [d for b in blocks for d in b['days'] if not d.get('departure')]
    total = (datetime.date.fromisoformat(m['trip_end']) - datetime.date.fromisoformat(m['trip_start'])).days
    assert len(nights) == total, 'expected %d night entries, found %d' % (total, len(nights))
    confirmed = sum(1 for d in nights if d['stay']['status'] in DONE)
    pending = sum(1 for d in nights if d['stay']['status'] == 'pending')
    open_n = total - confirmed - pending
    oop = data.get('out_of_pocket', [])
    oop_total = sum(x['amount'] for x in oop)

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
<!-- Generated by tools/render_trip_plan.py from proposals/data/%s.json. Edit the JSON, not this file. -->
<style>
%s</style>
<noscript><style>.jc-daysec, .jc-hero .inner > * { opacity: 1 !important; transform: none !important; } .jc-datebar { display: none; }</style></noscript>
</head>
<body>
<header class="jc-hero">
  <img src="%s" alt="%s" style="object-position: 50%% 55%%;">
  <div class="shade"></div>
  <div class="inner">
    <span class="jc-eyebrow">%s</span>
    <h1>%s <em>%s</em></h1>
    <p>%s</p>
  </div>
  <span class="cue" aria-hidden="true"></span>
</header>
''' % (e(m['page_title']), m['slug'], css, m['hero_image'], e(m['hero_alt']), e(m['hero_eyebrow']),
       e(m['hero_names']), e(m['hero_place']), e(m['hero_line'])))

    key = ' '.join('<span class="k">%s%s</span>' % (chip(k['status']), e(k['meaning'])) for k in data['key'])
    a('''
<section class="jc-intro">
  <div class="jc-container">
    <div class="grid">
      <div><span class="jc-eyebrow">%s</span></div>
      <div>
        <p>%s</p>
        <p class="small">%s</p>
        <div class="jc-numbers">
          <div><span class="lbl">Nights confirmed</span><span class="big">%d <small>of %d</small></span><span class="note">%d pending &middot; %d open</span></div>
          <div><span class="lbl">Out of pocket so far</span><span class="big">%s</span><span class="note">%s</span></div>
        </div>
        <div class="jc-key">%s</div>
      </div>
    </div>
  </div>
</section>
''' % (e(m['intro_eyebrow']), e(m['hello']), e(m['how_to_read']),
       confirmed, total, pending, open_n,
       e(eur(oop_total)), e(', '.join('%s %s' % (x['name'], eur(x['amount'])) for x in oop)), key))

    # Essentials + region grid
    a('''
<section class="jc-strip" id="days">
  <div class="jc-container">
    <span class="jc-eyebrow">Day by Day</span>
    <div class="jc-daylist">
''')
    for b in blocks:
        for d in b['days']:
            _, wd, _, n, mon = day_bits(d['date'])
            if d.get('departure'):
                stay, status = 'Depart Naples, trip ends', 'departure'
            else:
                stay, status = d['stay']['name'], d['stay']['status']
            a('      <a class="row %s" href="#%s" data-date="%s"><span class="d"><b>%s %d</b> %s</span><span class="s">%s</span><span class="l">%s</span>%s</a>\n'
              % (status, day_id(d['date']), d['date'], mon, n, wd[:3], e(stay), e(d.get('label', '')), chip(status)))
    a('''    </div>
    <span class="jc-eyebrow">Essentials</span>
    <div class="jc-transfers" style="margin: 18px 0 44px;">
''')
    for c in data['essentials']:
        a('      <div class="jc-card"><div class="route" style="margin-top:0;">%s</div><p class="detail">%s</p></div>\n' % (e(c['title']), e(c['text'])))
    a('''    </div>
    <span class="jc-eyebrow">Tap a Region</span>
    <div class="grid regions" style="margin-top:18px;">
''')
    for b in blocks:
        bn = [d for d in b['days'] if not d.get('departure')]
        bc = sum(1 for d in bn if d['stay']['status'] in DONE)
        cls = 'cell' + ('' if bc == len(bn) else (' part-cell' if bc else ' open-cell'))
        a('      <a class="%s" href="#%s"><span class="num">%s</span><div class="dates">%s</div><div class="place">%s</div><div class="nights">%d of %d nights confirmed</div></a>\n'
          % (cls, b['id'], e(b['dates']), e(b['name']), e(b['strip_label']), bc, len(bn)))
    a('    </div>\n  </div>\n</section>\n\n')

    a('<nav class="jc-datebar" id="datebar" aria-label="Jump to a region"><div class="row">')
    for b in blocks:
        _, _, _, n, mon = day_bits(b['days'][0]['date'])
        a('<a href="#%s"><b>%d</b>%s &middot; %s</a>' % (b['id'], n, mon, e(b['name'])))
    a('<a href="#outstanding" class="x">Outstanding</a></div></nav>\n')

    for b in blocks:
        a('''
<section class="jc-daysec" id="%s">
  <div class="jc-container">
    <div class="grid solo">
      <article class="copy">
        <span class="jc-eyebrow">%s</span>
        <h2>%s</h2>
        <p class="sub">%s</p>
''' % (b['id'], e(b['dates']), e(b['name']), e(b['summary'])))
        if b.get('drive'):
            a('        <p class="jc-drive">%s</p>\n' % e(b['drive']))
        a('\n'.join(render_day(d) for d in b['days']))
        if b.get('groups'):
            a('\n' + render_groups(b['groups']))
        a('''
        <a class="jc-back" href="#days">&uarr; All regions</a>
      </article>
    </div>
  </div>
</section>
''')

    # Outstanding + lists
    a('''
<section class="jc-section" id="outstanding" style="padding-top:80px; border-top:1px solid var(--hairline); scroll-margin-top:58px;">
  <div class="jc-container">
    <span class="jc-eyebrow">Ordered by Urgency</span>
    <h2>Outstanding</h2>
    <div class="jc-todo-cols">
''')
    for i, col in enumerate(data['outstanding']):
        a('      <div class="jc-todo-col%s"><div class="title">%s</div><ol start="%d">%s</ol></div>\n' % (
            ' urgent' if i == 0 else '', e(col['title']), col.get('start', 1),
            ''.join('<li>%s</li>' % e(x) for x in col['items'])))
    a('    </div>\n    <div class="jc-todo-cols" style="margin-top:44px;">\n')
    for col in data['lists']:
        a('      <div class="jc-todo-col"><div class="title">%s</div><ul>%s</ul></div>\n' % (
            e(col['title']), ''.join('<li>%s</li>' % e(x) for x in col['items'])))
    a('    </div>\n')
    a('    <p class="jc-money"><strong>Confirmed count:</strong> %d nights confirmed of %d, %d pending, %d open. <strong>Out of pocket so far:</strong> %s (%s).</p>\n' % (
        confirmed, total, pending, open_n, e(eur(oop_total)),
        e('; '.join('%s %s, %s' % (x['name'], eur(x['amount']), x['note']) if x.get('note') else '%s %s' % (x['name'], eur(x['amount'])) for x in oop))))
    a('  </div>\n</section>\n')

    a('''
<footer class="jc-footer">
  Suites With Keith &middot; Working plan, not a client document<br>
  This page updated %s</footer>

<script>
%s
%s</script>
</body>
</html>
''' % (datetime.date.fromisoformat(m['updated']).strftime('%B %-d, %Y'), base_js, today_js))

    out = ''.join(o)
    for bad in ('—', '&mdash;', '–', '&ndash;', '→'):
        assert bad not in out, 'dash or arrow found in output: %r' % bad
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    slug = sys.argv[1]
    data = json.loads((ROOT / 'proposals/data' / (slug + '.json')).read_text())
    assert data['meta']['slug'] == slug
    dest = ROOT / 'proposals' / (slug + '.html')
    dest.write_text(render(data))
    print('wrote', dest.relative_to(ROOT))


if __name__ == '__main__':
    main()
