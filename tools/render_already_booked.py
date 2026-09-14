#!/usr/bin/env python3
"""Render already-booked-<slug>.html from phase1/src/pages/already-booked-<slug>.astro
without node: already-booked-santorini.html supplies the head, nav, footer and scripts,
and the page body is rendered from the .astro source.

Assumptions (asserted where possible):
  * the .astro frontmatter holds one `const cards = [...]` array of single-quoted JS strings
  * the body uses one `{cards.map((c, i) => ( ... ))}` block, rendered here by
    render_card() — keep that template in sync with the Santorini/Mykonos pages
  * the <style> block is identical to already-booked-santorini.astro, so the compiled,
    scoped CSS (data-astro-cid-hydprnpr) in the Santorini head can be reused verbatim

Usage:  python3 tools/render_already_booked.py paros
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CID = 'data-astro-cid-hydprnpr'
VOID = {'img', 'input', 'br', 'hr', 'meta', 'link', 'source'}


def js_to_json(s):
    """Convert a JS array literal (single-quoted strings, bare keys, trailing commas) to JSON."""
    out, chunk, i, n = [], [], 0, len(s)

    def flush():
        t = ''.join(chunk)
        t = re.sub(r'(?<=[{,\s])([A-Za-z_]\w*)\s*:', r'"\1":', t)
        t = re.sub(r',\s*([\]}])', r'\1', t)
        out.append(t)
        chunk.clear()

    while i < n:
        c = s[i]
        if c == "'":
            flush()
            j, buf = i + 1, []
            while s[j] != "'":
                if s[j] == '\\':
                    buf.append(s[j + 1]); j += 2
                else:
                    buf.append(s[j]); j += 1
            out.append(json.dumps(''.join(buf), ensure_ascii=False))
            i = j + 1
        else:
            chunk.append(c); i += 1
    flush()
    return ''.join(out)


def render_card(c, i):
    band = i % 2 == 0
    notes = ''.join(f'<p class="ab-note"><b>{b}</b> <span>{t}</span></p>' for b, t in c['notes'])
    style = f' style="{c["imgStyle"]}"' if c.get('imgStyle') else ''
    return (
        f'<section class="section{" band on-shadow" if band else ""}" id="{c["id"]}" style="scroll-margin-top:70px;"> '
        f'<div class="container"> <div class="ab-grid{"" if band else " flip"}"> '
        f'<figure class="reveal ab-media"> <img src="{c["img"]}" alt="{c["alt"]}" width="1800" height="1300" '
        f'loading="{"eager" if i == 0 else "lazy"}" decoding="async"{style}> </figure> '
        f'<div class="reveal"> <span class="stamp plain" style="font-weight:700; color:{"var(--brass-lit)" if band else "var(--brass)"};">No. {c["num"]}</span> '
        f'<h2 class="display-l" style="margin-top:12px;">{c["h"]}</h2> '
        f'<p class="deck" style="margin-top:10px; font-size:1.05rem;">{c["tag"]}</p> '
        f'<p class="stamp plain ab-meta">{c["meta"]}</p> '
        f'<p class="body-2" style="margin-top:18px;">{c["desc"]}</p> '
        f'<div style="margin-top:22px;">{notes}</div> '
        f'<div class="verdict" style="margin-top:26px;"><p class="ab-take">{c["take"]}</p></div> '
        f'</div> </div> </div> </section>'
    )


def scope(body):
    """Add the scoped-style attribute to every opening tag (Astro does this for authored markup)."""
    def tag(m):
        name, attrs = m.group(1), m.group(2).rstrip()
        if attrs.endswith('/'):
            attrs = attrs[:-1].rstrip()
        if name.lower() in VOID:
            return f'<{name}{attrs} {CID}>'
        return f'<{name}{attrs} {CID}>'
    return re.sub(r'<([A-Za-z][A-Za-z0-9]*)((?:\s[^<>]*?)?)\s*/?>', tag, body)


def attr(v):
    return html.escape(v, quote=False).replace('"', '&quot;')


def main(slug):
    src = (ROOT / 'phase1/src/pages' / f'already-booked-{slug}.astro').read_text()
    skel = (ROOT / 'already-booked-santorini.html').read_text()

    fm, rest = re.match(r'---\n(.*?)\n---\n(.*)', src, re.S).groups()
    cards = json.loads(js_to_json(re.search(r'const cards = (\[.*\]);', fm, re.S).group(1)))

    props = dict(re.findall(r'(\w+)="([^"]*)"', re.search(r'<Layout(.*?)>', rest, re.S).group(1)))
    body = rest[rest.index('>', rest.index('<Layout')) + 1: rest.index('</Layout>')]

    # style block must match the skeleton's source so its compiled CSS applies
    style = re.search(r'<style>(.*?)</style>', rest, re.S).group(1)
    sant = (ROOT / 'phase1/src/pages/already-booked-santorini.astro').read_text()
    sant_style = re.search(r'<style>(.*?)</style>', sant, re.S).group(1)
    assert re.sub(r'\s+', ' ', style).strip() == re.sub(r'\s+', ' ', sant_style).strip(), 'style block differs from Santorini'

    m = re.search(r'\{cards\.map\(\(c, i\) => \(.*?\n\)\)\}', body, re.S)
    assert m, 'cards.map block not found'
    body = body[:m.start()] + ''.join(render_card(c, i) for i, c in enumerate(cards)) + body[m.end():]
    assert 'set:html' not in body and '{c.' not in body and '{cards' not in body

    body = re.sub(r'<!--.*?-->', '', body, flags=re.S)
    body = scope(body)
    body = re.sub(r'\s+', ' ', body).strip()

    pre = skel[:skel.index('<header class="hero"')]
    post = skel[skel.rindex('</section>') + len('</section>'):]

    sant_props = dict(re.findall(r'(\w+)="([^"]*)"', re.search(r'<Layout(.*?)>', sant, re.S).group(1)))
    for key, count in (('title', 2), ('description', 2), ('canonical', 2), ('preload', 1)):
        old, new = attr(sant_props[key]), attr(props[key])
        assert pre.count(old) == count, (key, pre.count(old))
        pre = pre.replace(old, new)

    out = ROOT / f'already-booked-{slug}.html'
    out.write_text(pre + body + post)
    print(f'wrote {out.name} ({out.stat().st_size} bytes, {len(cards)} cards)')


if __name__ == '__main__':
    main(sys.argv[1])
