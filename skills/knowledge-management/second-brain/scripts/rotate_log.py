#!/usr/bin/env python3
"""Rotate log.md so it never bloats context.

Keeps the trailing window (default last 40 entries) in log.md; archives older
entries into wiki/meta/log-archive/log-YYYY-Qn.md (same format, same grep
contract). log.md keeps an Archives pointer list. Idempotent.
"""

import re
import sys
from pathlib import Path

from common import VAULT

KEEP = int(sys.argv[1]) if len(sys.argv) > 1 else 40
LOG = VAULT / "log.md"
ARCHIVE_DIR = VAULT / "wiki" / "meta" / "log-archive"
ENTRY_RE = re.compile(r"(?m)^## \[(\d{4})-(\d{2})-\d{2}\]")


def quarter(month: int) -> int:
    return (month - 1) // 3 + 1


def split_entries(text: str):
    idxs = [m.start() for m in ENTRY_RE.finditer(text)]
    preamble = text[:idxs[0]] if idxs else text
    entries = []
    for i, start in enumerate(idxs):
        end = idxs[i + 1] if i + 1 < len(idxs) else len(text)
        m = ENTRY_RE.match(text[start:])
        y, mo = int(m.group(1)), int(m.group(2))
        entries.append({"text": text[start:end].rstrip("\n"), "year": y, "q": quarter(mo)})
    return preamble, entries


def run():
    if not LOG.exists():
        print("No log.md found.")
        return
    _pre, entries = split_entries(LOG.read_text(encoding="utf-8"))
    if len(entries) <= KEEP:
        print(f"log.md has {len(entries)} entries (<= {KEEP}); no rotation needed.")
        return

    to_archive, keep = entries[:-KEEP], entries[-KEEP:]
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    buckets = {}
    for e in to_archive:
        buckets.setdefault((e["year"], e["q"]), []).append(e["text"])

    archive_files = []
    for (y, q), texts in sorted(buckets.items()):
        af = ARCHIVE_DIR / f"log-{y}-Q{q}.md"
        existing = af.read_text(encoding="utf-8") if af.exists() else (
            f"# Activity Log Archive — {y} Q{q}\n")
        af.write_text(existing.rstrip() + "\n\n" + "\n\n".join(texts) + "\n", encoding="utf-8")
        archive_files.append(af.stem)

    # all archive files (including pre-existing) for the pointer list
    all_archives = sorted(p.stem for p in ARCHIVE_DIR.glob("log-*.md"))
    pre = ["# Activity Log", "",
           "> Recent entries below. Older entries are archived; grep contract preserved (`grep \"^## \\[\" log.md`).",
           "", "## Archives", ""]
    pre += [f"- [[{name}]]" for name in all_archives]
    pre += [""]
    new_log = "\n".join(pre) + "\n" + "\n\n".join(e["text"] for e in keep) + "\n"
    LOG.write_text(new_log, encoding="utf-8")
    print(f"Archived {len(to_archive)} entries into {len(buckets)} file(s); kept last {len(keep)} in log.md.")


if __name__ == "__main__":
    run()
