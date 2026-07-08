#!/usr/bin/env python3
"""Normalize frontmatter tags to the controlled vocabulary (drift -> canonical).

Uses the MERGE_MAP configured in scripts/common.py -- the single place to
configure this for your vault (see also wiki/meta/formats/tag-taxonomy.md for
the human-readable description of the current mapping). Only rewrites inline
(`tags: [...]`) lists; block-style lists are reported and skipped for safety.
Use --dry-run to preview.
"""

import re
import sys
from pathlib import Path

from common import scan_wiki, MERGE_MAP

DRY = "--dry-run" in sys.argv
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TAGS_LINE = re.compile(r"(?m)^tags:[ \t]*(.*)$")


def run():
    pages = scan_wiki()
    changed, skipped = [], []
    for slug, info in pages.items():
        fm = info["parsed"]["frontmatter"] or {}
        tags = fm.get("tags")
        if not isinstance(tags, list) or not tags:
            continue
        merged = []
        for t in tags:
            c = MERGE_MAP.get(str(t), str(t))
            if c not in merged:
                merged.append(c)
        if merged == [str(t) for t in tags]:
            continue
        path = info["path"]
        text = path.read_text(encoding="utf-8")
        m = FM_RE.match(text)
        if not m:
            continue
        fm_text = m.group(1)
        lm = TAGS_LINE.search(fm_text)
        if not lm or not lm.group(1).strip().startswith("["):
            skipped.append(slug)  # block-style or unusual; leave for manual review
            continue
        new_fm = fm_text[:lm.start()] + f"tags: [{', '.join(merged)}]" + fm_text[lm.end():]
        changed.append(slug)
        if not DRY:
            path.write_text(text[:m.start(1)] + new_fm + text[m.end(1):], encoding="utf-8")
    verb = "Would normalize" if DRY else "Normalized"
    print(f"{verb} tags on {len(changed)} page(s): " + (", ".join(changed) if changed else "none"))
    if skipped:
        print(f"Skipped (block-style tags, review manually): {', '.join(skipped)}")


if __name__ == "__main__":
    run()
