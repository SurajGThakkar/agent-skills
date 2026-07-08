#!/usr/bin/env python3
"""Type-aware confidence calibration.

Only clears FALSE flags: downgrades high -> medium for entity/concept pages that
have < 2 sources AND are not first-party. Never touches source/domain (exempt) or
owned projects, and never overrides a deliberate rating beyond this rule.

Use --dry-run to preview.
"""

import re
import sys
from pathlib import Path

from common import scan_wiki, page_type, sources_list, is_first_party

DRY = "--dry-run" in sys.argv


def run():
    pages = scan_wiki()
    changed = []
    for slug, info in pages.items():
        if page_type(info) not in {"entity", "concept"}:
            continue
        fm = info["parsed"]["frontmatter"] or {}
        if fm.get("confidence") != "high":
            continue
        if len(sources_list(fm)) >= 2 or is_first_party(slug, fm):
            continue
        path = info["path"]
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        if not m:
            continue
        new_fm = re.sub(r"(?m)^(confidence:\s*)high\s*$", r"\1medium", m.group(1))
        if new_fm != m.group(1):
            changed.append(slug)
            if not DRY:
                path.write_text(text[:m.start(1)] + new_fm + text[m.end(1):], encoding="utf-8")
    verb = "Would calibrate" if DRY else "Calibrated"
    print(f"{verb} {len(changed)} entity/concept page(s) high -> medium: " +
          (", ".join(changed) if changed else "none"))


if __name__ == "__main__":
    run()
