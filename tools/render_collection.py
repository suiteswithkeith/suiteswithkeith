#!/usr/bin/env python3
"""Render napa-sonoma-collection.html from phase1/src/pages/napa-sonoma-collection.astro
without node: greece-collection.html supplies the head, nav, footer, Ask section and
scripts; the page body and the scoped <style> are rendered from the .astro source.

Assumptions (asserted where possible):
  * frontmatter holds `const toc`, `const more`, `const edit`, `const perks` literals
  * the body uses one `{toc.map(...)}`, `{edit.map(...)}` and `{perks.map(...)}` block,
    rendered here by the render_* functions — keep them in sync with the .astro markup
  * the <style> block is scoped the way Astro does it (attribute appended to every
    compound selector, `:global()` left alone) — scope_css() is checked against the
    Greece page's compiled CSS as a self-test

Usage:  python3 tools/render_collection.py
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SLUG = 'napa-sonoma-collection'
CID = 'data-astro-cid-nsc0f2a1'
GREECE_CID = 'data-astro-cid-e2zfk4rc'
VOID = {'img', 'input', 'br', 'hr', 'meta', 'link', 'source'}


def js_to_json(s):
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


def const(fm, name):
    m = re.search(r'const ' + name + r' = ([\[{].*?[\]}]);\n', fm, re.S)
    assert m, name
    return json.loads(js_to_json(m.group(1)))


# ---- scoped css -------------------------------------------------------------
def scope_selector(sel, cid):
    parts = re.split(r'(\s*[>+~]\s*|\s+)', sel.strip())
    out = []
    for p in parts:
        if not p or re.fullmatch(r'\s*[>+~]?\s*', p):
            out.append(p.strip() if p.strip() else ' ')
            continue
        if ':global(' in p:
            out.append(re.sub(r':global\((.*)\)', r'\1', p))
            continue
        m = re.match(r'^([^:]*)(:.*)?$', p)
        out.append(f'{m.group(1)}[{cid}]{m.group(2) or ""}')
    return ''.join(out)


def scope_css(css, cid):
    css = re.sub(r'\s+', ' ', css).strip()

    def block(body):
        res = []
        for rule in re.findall(r'([^{}]+)\{([^{}]*)\}', body):
            sel, decl = rule
            sels = ','.join(scope_selector(s, cid) for s in sel.split(','))
            decl = re.sub(r'\s*:\s*', ':', decl)
            decl = re.sub(r'\s*;\s*', ';', decl).strip().rstrip(';')
            decl = re.sub(r',\s+', ',', decl)
            res.append(f'{sels}{{{decl}}}')
        return ''.join(res)

    out, i = [], 0
    while i < len(css):
        m = re.match(r'\s*@media\s*([^{]+)\{', css[i:])
        if m:
            depth, j = 1, i + m.end()
            while depth:
                depth += {'{': 1, '}': -1}.get(css[j], 0); j += 1
            q = re.sub(r'\s*:\s*', ':', m.group(1).strip()).replace(' (', '(')
            out.append(f'@media{q}{{{block(css[i + m.end():j - 1])}}}')
            i = j
        else:
            m = re.match(r'\s*([^{]+)\{([^{}]*)\}', css[i:])
            if not m:
                break
            out.append(block(m.group(0)))
            i += m.end()
    return ''.join(out)


def selftest_scoper():
    src = (ROOT / 'phase1/src/pages/greece-collection.astro').read_text()
    css = re.search(r'<style>(.*)</style>', src, re.S).group(1)
    built = (ROOT / 'greece-collection.html').read_text()
    want = re.search(r'<style>(.*?)</style>', built, re.S).group(1).strip()
    got = scope_css(css, GREECE_CID)
    assert got == want, 'scope_css drifted from the Astro compiler:\n' + got[:400] + '\n--\n' + want[:400]


# ---- body -------------------------------------------------------------------
def cid_tags(markup):
    """Add the scope attribute to every tag in page-authored markup (not set:html content)."""
    return re.sub(r'<([a-z][a-z0-9]*)((?:\s+[^\s=>]+(?:="[^"]*")?)*)\s*>', lambda m: f'<{m.group(1)}{m.group(2)} {CID}>', markup)


def render_toc(toc, more):
    cards = []
    for t in toc:
        hotels = ''.join(f'<a class="gc-link" href="{h}" {CID}>{n}&nbsp;&rarr;</a>' for n, h in t['hotels'])
        cards.append(
            f'<div class="gc-toc-card reveal" {CID}> <img src="{t["img"]}" alt="{html.escape(html.unescape(t["name"]), quote=True)}" width="{t["w"]}" height="{t["h"]}" loading="lazy" decoding="async" {CID}> '
            f'<div {CID}> <span class="gc-num" {CID}>{t["num"]}</span> <h3 {CID}>{t["name"]}</h3> <p {CID}>{t["p"]}</p> '
            f'<span class="gc-hotels" {CID}>{hotels}</span> </div> </div>')
    cards.append(
        f'<a class="gc-toc-card reveal" href="{more["href"]}" {CID}> <img src="{more["img"]}" alt="{more["name"]}" width="{more["w"]}" height="{more["h"]}" loading="lazy" decoding="async" {CID}> '
        f'<div {CID}> <span class="gc-num" {CID}>+</span> <h3 {CID}>{more["name"]}</h3> <p {CID}>{more["p"]}</p> '
        f'<span class="gc-link" {CID}>{more["cta"]}&nbsp;&rarr;</span> </div> </a>')
    return ''.join(cards)


def render_edit(edit):
    return ''.join(
        f'<div class="gc-edit-item" {CID}> <h5 {CID}>{l}</h5> <span class="gc-winner" {CID}>{w}</span> <span class="gc-isle" {CID}>{i}</span> </div>'
        for l, w, i in edit)


def render_perks(perks):
    return ''.join(f'<div class="gc-perk reveal" {CID}> <h3 {CID}>{h}</h3> <p {CID}>{p}</p> </div>' for h, p in perks)


def render_ask(greece, props):
    ask = re.search(r'<section class="section inquire".*?</section>', greece, re.S).group(0)
    swaps = [
        ('Planning a Greece trip?', props['eyebrow']),
        ('Inquiry — The Greece Collection', props['subject']),
        ('value="greece-collection"', f'value="{props["page"]}"'),
        ('placeholder="The Cyclades in June"', f'placeholder="{props["placeholder"]}"'),
        ('Tell me where and when, and I’ll take it from there.', html.unescape(props['deck']).replace("'", '’')),
    ]
    for a, b in swaps:
        assert a in ask, a
        ask = ask.replace(a, b)
    return ask


def main():
    selftest_scoper()
    src = (ROOT / f'phase1/src/pages/{SLUG}.astro').read_text()
    greece = (ROOT / 'greece-collection.html').read_text()
    fm, rest = src.split('---\n')[1:3]
    toc, more, edit, perks = (const(fm, n) for n in ('toc', 'more', 'edit', 'perks'))

    layout = dict(re.findall(r'\n  (\w+)="([^"]*)"', rest.split('>\n<Fragment')[0]))
    body = re.search(r'</Fragment>\n(.*?)\n<Ask', rest, re.S).group(1)
    body = re.sub(r'\{toc\.map\(.*?\n      \)\)\}\n', '\n', body, flags=re.S)
    body = re.sub(r'\n      <a class="gc-toc-card reveal" href=\{more\.href\}>.*?</a>\n', '\n', body, flags=re.S)
    body = re.sub(r'\{edit\.map\(.*?\)\)\}', '@@EDIT@@', body, flags=re.S)
    body = re.sub(r'\{perks\.map\(.*?\)\)\}', '@@PERKS@@', body, flags=re.S)
    body = re.sub(r'<!--.*?-->\n', '', body)
    body = re.sub(r'\s*/>', '>', body)
    body = cid_tags(body)
    body = body.replace(f'<div class="gc-toc" {CID}>\n', f'<div class="gc-toc" {CID}> ' + render_toc(toc, more) + ' ')
    body = body.replace('@@EDIT@@', render_edit(edit)).replace('@@PERKS@@', render_perks(perks))
    body = re.sub(r'\n\s*', ' ', body).strip()
    body = re.sub(r'(<[a-z0-9]+[^>]*>) ', r'\1 ', body)
    assert '{' not in body, 'unrendered expression in body: ' + body[body.index('{') - 80:body.index('{') + 80]

    ask = dict(re.findall(r'\n  (\w+)="([^"]*)"', re.search(r'<Ask(.*?)/>', rest, re.S).group(1)))
    css = scope_css(re.search(r'<style>(.*)</style>', src, re.S).group(1), CID)

    out = greece
    head_swaps = [
        ('<title>The Greece Collection | Luxury Greece Honeymoon Guide</title>', f'<title>{html.escape(layout["title"])}</title>'),
        ('content="Issue No. 01 of The Greece Collection — a firsthand luxury travel and honeymoon guide to the Cyclades, featuring 38 hotels and seven destination guides."', f'content="{html.escape(layout["description"])}"'),
        ('content="The Greece Collection | Luxury Greece Honeymoon Guide"', f'content="{html.escape(layout["title"])}"'),
        ('greece-collection.html', f'{SLUG}.html'),
        ('/video/greece-collection-hero-poster.jpg" fetchpriority', f'{layout["preload"]}" fetchpriority'),
        ('https://suiteswithkeith.com/images/islands/cover.jpg', 'https://suiteswithkeith.com/images/napa/collection-cover.jpg'),
    ]
    for a, b in head_swaps:
        assert a in out, a
        out = out.replace(a, b)
    out = re.sub(r'<style>.*?</style>', lambda m: f'<style>{css}\n</style>', out, count=1, flags=re.S)
    start = out.index('<header class="hero"')
    end = out.index('<section class="section inquire"')
    out = out[:start] + body + ' ' + render_ask(greece, ask) + out[re.search(r'</section>', out[end:]).end() + end:]
    assert GREECE_CID not in out and 'Greece' not in re.sub(r'<script.*?</script>', '', out, flags=re.S).split('<body>')[1], 'Greece leftovers'
    (ROOT / f'{SLUG}.html').write_text(out)
    print('wrote', f'{SLUG}.html', len(out), 'bytes')


if __name__ == '__main__':
    main()
