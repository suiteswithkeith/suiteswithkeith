#!/usr/bin/env python3
"""Cut a small region out of the GSHHS full-resolution shorelines (public domain,
Wessel & Smith, as packaged in the basemap-data-hires wheel) and save it as
tools/versus-maps/<name>.json for tools/render_versus_map.py.

Usage: python3 tools/versus-maps/extract_gshhs.py <basemap_data dir> <name> <west> <south> <east> <north> [--rivers]

Get the data with: pip download basemap-data-hires --no-deps, then unzip the wheel
(the files are under mpl_toolkits/basemap_data).

Output: {"_source", "bbox", "land": [rings], "water": [rings], "borders": [lines]}
with [lon, lat] pairs. "land" = GSHHS levels 1 and 3 (land, islands in lakes);
"water" = level 2 (lakes); "borders" = national borders and, with --rivers,
"rivers" = rivers, both from the same package.
Rings are clamped to a margin around the bbox and lightly simplified (about 10 m),
which is all a framed map needs.
"""
import json, os, struct, sys

d, name = sys.argv[1], sys.argv[2]
w, s, e, n = map(float, sys.argv[3:7])
mw, mh = (e - w) * .15, (n - s) * .15
W, S, E, N = w - mw, s - mh, e + mw, n + mh
EPS = 1e-4  # degrees, ~10 m


def rdp(pts, eps=EPS):
    if len(pts) < 3:
        return pts
    stack, keep = [(0, len(pts) - 1)], {0, len(pts) - 1}
    while stack:
        a, b = stack.pop()
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1
        L = (dx * dx + dy * dy) ** .5
        i, dmax = 0, 0
        for j in range(a + 1, b):
            x, y = pts[j]
            dd = abs(dy * x - dx * y + x2 * y1 - y2 * x1) / L if L else ((x - x1) ** 2 + (y - y1) ** 2) ** .5
            if dd > dmax:
                i, dmax = j, dd
        if dmax > eps:
            keep.add(i); stack += [(a, i), (i, b)]
    return [pts[k] for k in sorted(keep)]


def clip(pts, closed):
    out, last = [], None
    for x, y in pts:
        p = (round(min(max(x, W), E), 5), round(min(max(y, S), N), 5))
        if p != last:
            out.append(p); last = p
    if closed and len(out) > 3:
        h = len(out) // 2
        out = rdp(out[:h + 1])[:-1] + rdp(out[h:])
    else:
        out = rdp(out)
    return [list(p) for p in out]


def read(base, levels=None):
    with open(f'{d}/{base}.dat', 'rb') as dat:
        for line in open(f'{d}/{base[:-2]}meta_f.dat'):
            f = line.split()
            typ, npts, south, north, off, nbytes = int(f[0]), int(f[2]), float(f[3]), float(f[4]), int(f[5]), int(f[6])
            if north < S or south > N or (levels and typ not in levels):
                continue
            dat.seek(off)
            raw = struct.unpack(f'<{npts * 2}f', dat.read(nbytes))
            pts = list(zip(raw[0::2], raw[1::2]))
            if any(W <= x <= E and S <= y <= N for x, y in pts):
                yield typ, pts


land, water, borders = [], [], []
for typ, pts in read('gshhs_f', (1, 2, 3)):
    (water if typ == 2 else land).append(clip(pts, True))
for _, pts in read('countries_f'):
    borders.append(clip(pts, False))
rivers = [clip(pts, False) for _, pts in read('rivers_f')] if '--rivers' in sys.argv else []
out = {'_source': 'GSHHS full-resolution shorelines (public domain; Wessel & Smith), via the basemap-data-hires package. '
                  'land = levels 1 and 3, water = level 2 (lakes). [lon, lat] rings.',
       'bbox': [w, s, e, n], 'land': land, 'water': water, 'borders': borders, 'rivers': rivers}
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{name}.json')
open(path, 'w').write(json.dumps(out, separators=(',', ':')))
print(name, 'land', len(land), 'water', len(water), 'borders', len(borders), 'rivers', len(rivers), f'{os.path.getsize(path) // 1024} KB')
