#!/usr/bin/env python3
"""Draw the location map for a head-to-head page: a quiet, typographic SVG of
the county outlines (no tiles, no scripts) saved to images/maps/<slug>.svg, plus
the marker and label positions (as percentages) written back into the entry's
"map" block in phase1/src/data/versus.json. The page renders the labels in HTML
over the SVG, so the text stays readable at phone width.

Usage: python3 tools/render_versus_map.py <slug> [<slug> ...]      (versus.json pages)
       python3 tools/render_versus_map.py --region "Lake Como"         (every Italy page in a region,
                                                                       from tools/versus-maps/regions.json)

The entry's "map" block holds the inputs (everything else is computed):
  "map": {
    "data": "norcal-counties",            # tools/versus-maps/<data>.json
    "bbox": [west, south, east, north],   # degrees
    "highlight": ["Napa", "Sonoma"],       # counties drawn in the lighter land tone
    "markers": [ {"name", "place", "lat", "lon", "side": above|below|left|right,
                  "source": where the coordinates were checked} ],
    "labels":  [ {"text", "lat", "lon", "kind": "region"|"water"} ],
    "line": true,                          # dashed line + distance between the two markers
    "h2", "intro", "alt", "caption"        # copy, rendered by the page template
  }
Only use coordinates you have checked against a published source, and record
that source in the marker's "source" field.
"""
import glob, json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VJ = f'{ROOT}/phase1/src/data/versus.json'
W = 1000  # viewBox width

# Plaster & Shadow tones (see phase1/src/styles/tokens.css)
WATER = '#DADBD2'
LAND = '#ECE9E0'
LAND_HI = '#FBFAF6'
EDGE = 'rgba(22,23,18,.22)'
BRASS = '#836229'


def project(bbox):
    w, s, e, n = bbox
    k = math.cos(math.radians((s + n) / 2))
    scale = W / ((e - w) * k)
    H = (n - s) * scale

    def p(lon, lat):
        return ((lon - w) * k * scale, (n - lat) * scale)
    return p, H


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1e-9
    i, dmax = 0, 0
    for j in range(1, len(pts) - 1):
        d = abs(dy * pts[j][0] - dx * pts[j][1] + x2 * y1 - y2 * x1) / L
        if d > dmax:
            i, dmax = j, d
    if dmax <= eps:
        return [pts[0], pts[-1]]
    return rdp(pts[:i + 1], eps)[:-1] + rdp(pts[i:], eps)


def inside(pt, ring):
    x, y = pt
    c = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def miles(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a['lat'], a['lon'], b['lat'], b['lon']))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 3958.8 * math.asin(math.sqrt(h))


def ring_path(ring, p, H):
    # clamp to just outside the frame: off-screen detail collapses to a straight edge
    raw = [(min(max(x, -12), W + 12), min(max(y, -12), H + 12)) for x, y in (p(lon, lat) for lon, lat in ring)]
    h = len(raw) // 2  # closed ring: simplify each half, or the end points coincide
    pts = rdp(raw[:h + 1], 0.9)[:-1] + rdp(raw[h:], 0.9)
    return '' if len(pts) < 3 else 'M' + 'L'.join(f'{x:.0f},{y:.0f}' for x, y in pts) + 'Z'


def line_path(line, p):
    pts = rdp([p(lon, lat) for lon, lat in line], 0.9)
    return 'M' + 'L'.join(f'{x:.0f},{y:.0f}' for x, y in pts)


def nearest_on(rings, lat, lon):
    """Nearest vertex of any ring to a point: used to put a lakefront hotel on the shore."""
    best = min((((x - lon) * math.cos(math.radians(lat))) ** 2 + (y - lat) ** 2, x, y) for r in rings for x, y in r)
    return best[2], best[1]


def build(m, slug):
    """Draw images/maps/<slug>.svg for one map block and fill in its computed fields."""
    data = json.load(open(f'{ROOT}/tools/versus-maps/{m["data"]}.json'))
    p, H = project(m['bbox'])
    pct = lambda x, y: (round(100 * x / W, 2), round(100 * y / H, 2))

    if 'counties' in data:  # US county outlines: land shapes on water
        counties = data['counties']
        paths = [(''.join(ring_path(r, p, H) for r in rings), LAND_HI if name in m.get('highlight', []) else LAND)
                 for name, rings in counties.items()]
        land_rings, water_rings, bg = [r for rings in counties.values() for r in rings], [], WATER
        extra = ''
    else:  # GSHHS: coast and lakes; with no land rings the frame is all land (lakes only)
        land_rings, water_rings = data['land'], data['water']
        bg = WATER if land_rings else LAND_HI
        paths = [(ring_path(r, p, H), LAND_HI) for r in land_rings] + [(ring_path(r, p, H), WATER) for r in water_rings]
        extra = ''.join(f'<path d="{line_path(l, p)}" fill="none" stroke="#C9CBC0" stroke-width="1.6"/>' for l in data.get('rivers', []))
        extra += ''.join(f'<path d="{line_path(l, p)}" fill="none" stroke="{EDGE}" stroke-width="1" stroke-dasharray="5 4"/>'
                         for l in data.get('borders', []))
    edges = ''.join(f'<path d="{d}"/>' for d, _ in paths if d)
    edges = f'<g fill="none" stroke="{EDGE}" stroke-width="1" stroke-linejoin="round">{edges}</g>'
    fills = ''.join(f'<path d="{d}" fill="{fill}"/>' for d, fill in paths if d)

    def on_land(lat, lon):
        if land_rings and not any(inside((lon, lat), r) for r in land_rings):
            return False
        return not any(inside((lon, lat), r) for r in water_rings)

    for mk in m['markers']:
        if mk.get('snap') == 'water':
            mk['lat'], mk['lon'] = nearest_on(water_rings, mk['lat'], mk['lon'])
        elif not on_land(mk['lat'], mk['lon']):
            # a waterfront hotel can fall a few metres into the water on simplified shorelines: put it on the shore
            lat, lon = nearest_on(water_rings or land_rings, mk['lat'], mk['lon'])
            moved = miles({'lat': lat, 'lon': lon}, mk) * 1609
            if moved > 800:
                raise SystemExit(f'marker {moved:.0f} m off land: {mk["name"]}')
            print(f'  {mk["name"]}: moved {moved:.0f} m onto the shoreline')
            mk['lat'], mk['lon'] = lat, lon
    for lb in m.get('labels', []):
        assert on_land(lb['lat'], lb['lon']) == (lb['kind'] != 'water'), f'label misplaced: {lb["text"]}'

    line = ''
    if m.get('line') and len(m['markers']) == 2:
        (x1, y1), (x2, y2) = (p(mk['lon'], mk['lat']) for mk in m['markers'])
        line = (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{BRASS}" '
                f'stroke-width="1.5" stroke-dasharray="2 7" stroke-linecap="round" opacity=".75"/>')
        mi = miles(*m['markers'])
        m['distance_miles'] = round(mi)
        m['distance_text'] = 'Under a mile apart' if mi < 1 else f'About {round(mi)} mile{"s" if round(mi) != 1 else ""} apart'
        m['distance_pos'] = list(pct((x1 + x2) / 2, (y1 + y2) / 2))

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" preserveAspectRatio="xMidYMid slice">'
           f'<rect width="{W}" height="{H:.0f}" fill="{bg}"/>{fills}{extra}{edges}{line}</svg>\n')
    os.makedirs(f'{ROOT}/images/maps', exist_ok=True)
    open(f'{ROOT}/images/maps/{slug}.svg', 'w').write(svg)

    m['src'] = f'/images/maps/{slug}.svg'
    m['ratio'] = f'{W} / {H:.0f}'
    for mk in m['markers']:
        mk['pos'] = list(pct(*p(mk['lon'], mk['lat'])))
    for lb in m.get('labels', []):
        lb['pos'] = list(pct(*p(lb['lon'], lb['lat'])))
        lb['edge'] = not 18 <= lb['pos'][0] <= 82
    if len(m['markers']) == 2 and m.get('auto_sides'):
        a, b = m['markers']
        (ax, ay), (bx, by) = a['pos'], b['pos']
        north, south = (a, b) if ay <= by else (b, a)
        west, east = (a, b) if ax <= bx else (b, a)
        apart = math.hypot(ax - bx, ay - by)
        outward = abs(ax - bx) * 1.3 > abs(ay - by) and west['pos'][0] > 42 and east['pos'][0] < 58
        if outward:          # side by side with room: names go outward
            west['side'], east['side'] = 'left', 'right'
        else:                # otherwise stack: the northern name above, the southern below
            north['side'], south['side'] = 'above', 'below'
        for mk in m['markers']:  # a stacked name near the frame edge hangs inward instead of centring
            x = mk['pos'][0]
            mk['align'] = 'start' if mk['side'] in ('above', 'below') and x < 26 else (
                'end' if mk['side'] in ('above', 'below') and x > 74 else 'center')
        vertical = abs(ay - by) > abs(ax - bx)
        m['distance_pill'] = apart > 22 and (outward or vertical)
        # town labels that would sit under a hotel name are dropped for this page
        m['labels'] = [lb for lb in m.get('labels', []) if lb['kind'] == 'water' or all(
            abs(lb['pos'][0] - mk['pos'][0]) > 22 or abs(lb['pos'][1] - mk['pos'][1]) > 18 for mk in m['markers'])]
    print(f'wrote images/maps/{slug}.svg ({len(svg) // 1024} KB)', m.get('distance_text', ''))
    return m


def write_block(path, key, block):
    """Replace or add one top-level key in a hand-formatted JSON file, leaving the rest as written."""
    txt = open(path).read()
    ascii_ = not any(ord(c) > 127 for c in txt)
    dump = json.dumps(block, indent=2, ensure_ascii=ascii_).replace('\n', '\n  ')
    i = txt.find(f'\n  "{key}":')
    if i >= 0:
        j = txt.index(':', i) + 1
        while txt[j] in ' \n':
            j += 1
        _, end = json.JSONDecoder().raw_decode(txt, j)
        new = txt[:j] + dump + txt[end:]
    else:
        body = txt.rstrip()
        new = body[:-1].rstrip() + f',\n  "{key}": ' + dump + '\n}' + ('\n' if txt.endswith('\n') else '')
    assert json.loads(new)[key] == json.loads(json.dumps(block))
    open(path, 'w').write(new)


def region(place):
    """Build the map for every Italy spec in a region, from tools/versus-maps/regions.json."""
    reg = json.load(open(f'{ROOT}/tools/versus-maps/regions.json'))[place]
    for path in sorted(glob.glob(f'{ROOT}/tools/versus-italy/[!_]*.json')):
        v = json.load(open(path))
        if v['place'] != place:
            continue
        slug = os.path.basename(path)[:-5]
        markers = []
        for h in (v['a'], v['b']):
            key = h['href'].rsplit('/', 1)[1][:-5]
            hot = reg['hotels'][key]
            markers.append({'name': h['short'], 'place': hot['place'], 'lat': hot['lat'], 'lon': hot['lon'],
                            **({'snap': hot['snap']} if hot.get('snap') else {}), 'source': hot['source']})
        a, b = markers
        intro = f'{a["name"]} is in {a["place"].split(" &middot; ")[0]}. {b["name"]} is in {b["place"].split(" &middot; ")[0]}. {reg["lede"]}'
        approx = [mk['name'] for mk, h in zip(markers, (v['a'], v['b']))
                  if reg['hotels'][h['href'].rsplit('/', 1)[1][:-5]].get('approx')]
        cap = 'Distance shown as the crow flies.'
        if approx:
            cap += f' {" and ".join(approx)} {"is" if len(approx) == 1 else "are"} marked at the village; the exact spot may differ slightly.'
        m = {'data': reg['data'], 'bbox': reg['bbox'], 'markers': markers, 'labels': [dict(l) for l in reg['labels']],
             'line': True, 'auto_sides': True, 'eyebrow': reg['eyebrow'], 'h2': reg['h2'], 'intro': intro,
             'alt': f'Map showing {a["name"]} in {plain(a["place"])} and {b["name"]} in {plain(b["place"])}'}
        build(m, slug)
        if not m['distance_pill']:
            cap = cap.replace('Distance shown as the crow flies.', m['distance_text'] + ', as the crow flies.')
        m['caption'] = cap
        write_block(path, 'map', m)


def plain(s):
    return s.replace('&middot;', '·').replace('&rsquo;', '’').replace('&amp;', '&')


if __name__ == '__main__':
    if sys.argv[1:2] == ['--region']:
        region(' '.join(sys.argv[2:]))
    else:
        versus = json.load(open(VJ))
        for slug in sys.argv[1:]:
            build(versus[slug]['map'], slug)
        open(VJ, 'w').write(json.dumps(versus, indent=1, ensure_ascii=False))
