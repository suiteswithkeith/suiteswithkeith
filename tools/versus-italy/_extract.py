#!/usr/bin/env python3
"""Print a hotel/hub page as plain text with [IMG src | alt] markers. Usage: _extract.py <file.html>"""
import re, html, sys
s = open(sys.argv[1]).read()
s = re.sub(r'<script.*?</script>|<style.*?</style>|<nav.*?</nav>|<footer.*', '', s, flags=re.S)
s = re.sub(r'<img [^>]*?src="([^"]+)"[^>]*?alt="([^"]*)"[^>]*>', r'[IMG \1 | \2]', s)
s = re.sub(r'<(h[1-4]|p|li|dt|dd|tr|summary|figcaption)[^>]*>', '\n', s)
s = re.sub(r'<[^>]+>', ' ', s)
print(re.sub(r'\n\s*\n+', '\n', html.unescape(s)))
