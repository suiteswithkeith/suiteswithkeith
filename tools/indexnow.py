#!/usr/bin/env python3
"""Tell Bing (and through it ChatGPT search), Yandex, Seznam and Naver that pages changed,
via IndexNow. Run from your own computer after the site has deployed:

    python3 tools/indexnow.py            # pages changed in the last commit
    python3 tools/indexnow.py HEAD~5     # pages changed since a git ref
    python3 tools/indexnow.py --all      # every URL in sitemap.xml (first run)

The key file /c60a42b02e91d9ed321abde8a6fd26d0.txt must stay published at the site root.
"""
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST = "suiteswithkeith.com"
KEY = "c60a42b02e91d9ed321abde8a6fd26d0"
SITE = f"https://{HOST}/"


def sitemap_urls():
    return re.findall(r"<loc>(.*?)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))


def changed_urls(ref):
    files = subprocess.run(["git", "diff", "--name-only", ref, "HEAD"], cwd=ROOT,
                           capture_output=True, text=True, check=True).stdout.split()
    listed = set(sitemap_urls())
    urls = {SITE if f == "index.html" else SITE + f for f in files if f.endswith(".html")}
    return sorted(urls & listed)


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "HEAD~1"
    urls = sitemap_urls() if arg == "--all" else changed_urls(arg)
    if not urls:
        print("No listed pages changed.")
        return
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"{SITE}{KEY}.txt",
                       "urlList": urls[:10000]}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"Submitted {len(urls)} URLs: HTTP {r.status}")


if __name__ == "__main__":
    main()
