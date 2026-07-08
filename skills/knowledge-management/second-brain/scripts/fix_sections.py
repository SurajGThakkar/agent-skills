#!/usr/bin/env python3
"""Add missing standard sections to entity/concept/project/domain pages.

Generates the Sources section from frontmatter (real content); inserts light,
honest placeholders for Key Points / Connections / Open Questions that the
lint loop and hand-enrichment improve over time. Inserts in canonical order
(Overview, Key Points, Connections, Open Questions, Sources). Use --dry-run.
"""

import sys

from common import (scan_wiki, page_type, sources_list, has_section,
                    SECTION_ENFORCED_TYPES, STANDARD_SECTIONS)

DRY = "--dry-run" in sys.argv


def sources_block(fm, ptype):
    srcs = sources_list(fm)
    if srcs:
        bullets = "\n".join(f"- {s} — contributes to this page." for s in srcs)
    elif ptype == "domain":
        bullets = "- _Synthesizes the child pages linked in Connections; no single source._"
    else:
        bullets = "- _No dedicated source yet; see Connections._"
    return f"## Sources\n\n{bullets}\n"


BLOCKS = {
    "Key Points": "## Key Points\n\n- _Key takeaways are detailed in the Overview._\n",
    "Connections": "## Connections\n\n- _No cross-references yet — add links as they're discovered during ingest or lint._\n",
    "Open Questions": "## Open Questions\n\n- _None outstanding._\n",
}


def insert_before(text, marker, block):
    idx = text.find(marker)
    if idx == -1:
        return text.rstrip() + "\n\n" + block.strip() + "\n"
    # Normalize surrounding whitespace rather than assuming exactly one blank
    # line already exists — chained calls (e.g. Open Questions then Connections)
    # otherwise leave 0 or 1 newlines depending on what the previous call left.
    before = text[:idx].rstrip("\n")
    after = text[idx:].lstrip("\n")
    return before + "\n\n" + block.strip() + "\n\n" + after


def insert_first_section(text, block):
    first = text.find("\n## ")
    if first == -1:
        return text.rstrip() + "\n\n" + block.strip() + "\n"
    return text[:first + 1] + block.strip() + "\n\n" + text[first + 1:]


def insert_after_overview(text, block):
    ov = text.find("\n## Overview")
    anchor = text.find("\n## ", ov + 1) if ov != -1 else text.find("\n## ")
    if anchor == -1:
        return text.rstrip() + "\n\n" + block.strip() + "\n"
    return text[:anchor + 1] + block.strip() + "\n\n" + text[anchor + 1:]


def run():
    pages = scan_wiki()
    changed = []
    for slug, info in pages.items():
        ptype = page_type(info)
        if ptype not in SECTION_ENFORCED_TYPES:
            continue
        p = info["parsed"]
        missing = [s for s in STANDARD_SECTIONS if not has_section(p["sections"], s)]
        if not missing:
            continue
        fm = p["frontmatter"] or {}
        text = info["path"].read_text(encoding="utf-8")

        if "Sources" in missing:
            text = text.rstrip() + "\n\n" + sources_block(fm, ptype).strip() + "\n"
        if "Open Questions" in missing:
            text = insert_before(text, "\n## Sources", BLOCKS["Open Questions"])
        if "Connections" in missing:
            # Canonical order puts Connections right before Open Questions. By this
            # point "\n## Open Questions" exists in text whether it was already there
            # or was just inserted above, so the marker is always present.
            text = insert_before(text, "\n## Open Questions", BLOCKS["Connections"])
        if "Overview" in missing:
            text = insert_first_section(text, f"## Overview\n\n{p['summary']}\n")
        if "Key Points" in missing:
            text = insert_after_overview(text, BLOCKS["Key Points"])

        changed.append((slug, missing))
        if not DRY:
            info["path"].write_text(text, encoding="utf-8")
    verb = "Would fix" if DRY else "Fixed"
    print(f"{verb} sections on {len(changed)} page(s).")
    for slug, miss in changed:
        print(f"  {slug}: +{', '.join(miss)}")


if __name__ == "__main__":
    run()
