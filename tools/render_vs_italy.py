#!/usr/bin/env python3
"""Render Italy head-to-head pages from tools/versus-italy/<slug>.json.

The Italy pages now share one template with every other comparison page:
tools/render_versus.py (which reads these specs through italy_entry()). This
wrapper keeps the old command working.

Usage: python3 tools/render_vs_italy.py [<slug> ...]   (no args = every spec)

Spec fields: see tools/versus-italy/_BRIEF.md. Optional sections shared with the
rest of the site ("final", "map", "pair", "row_photos", "gallery") are
documented at the top of tools/render_versus.py.
"""
import glob, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_versus import ITALY, render  # noqa: E402

if __name__ == '__main__':
    slugs = sys.argv[1:] or sorted(os.path.basename(p)[:-5] for p in glob.glob(f'{ITALY}/[!_]*.json'))
    for s in slugs:
        render(s)
