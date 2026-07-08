---
title: "Format: Log"
type: meta
created: 2026-06-22
updated: 2026-06-22
sources: []
tags: [meta, format, schema]
confidence: high
---

# Format: Log

> `log.md` is the chronological, append-only record of wiki activity.

## Entry structure

```markdown
## [YYYY-MM-DD] type | Title
Brief description of what happened. Pages created: N. Pages updated: N.
- Created: [[page1]], [[page2]]
- Updated: [[page3]], [[page4]]
```

- **Valid types:** `ingest`, `query`, `lint`, `schema-update`, `maintenance`.
- Append-only; newest at the bottom.
- Parseable contract (must be preserved): `grep "^## \[" log.md | tail -5` returns the last 5 entries.

## Rotation policy

`log.md` is capped so it never bloats context:

- Keep the **trailing window** (current quarter + roughly the last 40 entries) in `log.md`.
- Archive older entries into `wiki/meta/log-archive/log-YYYY-Qn.md` (same format, same grep contract).
- `log.md` keeps a short "Archives" pointer list linking each archive file.
- Rotation is run by `skills/wiki-maintenance/scripts/rotate_log.py` during lint when the window is exceeded.
