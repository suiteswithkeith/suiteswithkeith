#!/usr/bin/env python3
"""Draw the location map for a head-to-head page: a quiet, typographic SVG of
the county outlines (no tiles, no scripts) saved to images/maps/<slug>.svg, plus
the marker and label positions (as percentages) written back into the entry's
"map" block in phase1/src/data/versus.json. The page renders the labels in HTML
over the SVG, so the text stays readable at phone width.

Usage: python3 tools/render_versus_map.py <slug> [<slug> ...]

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
import json, math, os, sys

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


def render(slug, versus):
    m = versus[slug]['map']
    data = json.load(open(f'{ROOT}/tools/versus-maps/{m["data"]}.json'))['counties']
    p, H = project(m['bbox'])
    pct = lambda x, y: (round(100 * x / W, 2), round(100 * y / H, 2))

    paths = []
    for name, rings in data.items():
        d = ''
        for ring in rings:
            # clamp to just outside the frame: off-screen detail collapses to a straight edge
            raw = [(min(max(x, -12), W + 12), min(max(y, -12), H + 12)) for x, y in (p(lon, lat) for lon, lat in ring)]
            h = len(raw) // 2  # closed ring: simplify each half, or the end points coincide
            pts = rdp(raw[:h + 1], 0.9)[:-1] + rdp(raw[h:], 0.9)
            if len(pts) < 3:
                continue
            d += 'M' + 'L'.join(f'{x:.0f},{y:.0f}' for x, y in pts) + 'Z'
        paths.append((d, LAND_HI if name in m.get('highlight', []) else LAND))
    # fills first, then every outline on top, so shared borders draw once at full weight
    edges = ''.join(f'<path d="{d}"/>' for d, _ in paths)
    edges = f'<g fill="none" stroke="{EDGE}" stroke-width="1" stroke-linejoin="round">{edges}</g>'
    paths = [f'<path d="{d}" fill="{fill}"/>' for d, fill in paths]

    # sanity: every marker and region label must sit on land, water labels on water
    def on_land(lat, lon):
        return any(inside((lon, lat), r) for rings in data.values() for r in rings)
    for mk in m['markers']:
        assert on_land(mk['lat'], mk['lon']), f'marker off land: {mk["name"]}'
    for lb in m.get('labels', []):
        assert on_land(lb['lat'], lb['lon']) == (lb['kind'] != 'water'), f'label misplaced: {lb["text"]}'

    line = ''
    if m.get('line') and len(m['markers']) == 2:
        (x1, y1), (x2, y2) = (p(mk['lon'], mk['lat']) for mk in m['markers'])
        line = (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{BRASS}" '
                f'stroke-width="1.5" stroke-dasharray="2 7" stroke-linecap="round" opacity=".75"/>')
        mi = miles(*m['markers'])
        m['distance_miles'] = round(mi)
        m['distance_pos'] = list(pct((x1 + x2) / 2, (y1 + y2) / 2))

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" preserveAspectRatio="xMidYMid slice">'
           f'<rect width="{W}" height="{H:.0f}" fill="{WATER}"/>{"".join(paths)}{edges}{line}</svg>\n')
    os.makedirs(f'{ROOT}/images/maps', exist_ok=True)
    open(f'{ROOT}/images/maps/{slug}.svg', 'w').write(svg)

    m['src'] = f'/images/maps/{slug}.svg'
    m['ratio'] = f'{W} / {H:.0f}'
    for mk in m['markers']:
        mk['pos'] = list(pct(*p(mk['lon'], mk['lat'])))
    for lb in m.get('labels', []):
        lb['pos'] = list(pct(*p(lb['lon'], lb['lat'])))
    print(f'wrote images/maps/{slug}.svg ({len(svg) // 1024} KB)', '' if 'distance_miles' not in m else f'· {m["distance_miles"]} mi apart')


if __name__ == '__main__':
    versus = json.load(open(VJ))
    for slug in sys.argv[1:]:
        render(slug, versus)
    open(VJ, 'w').write(json.dumps(versus, indent=1, ensure_ascii=False))
