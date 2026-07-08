---
title: "Format: Tag Taxonomy"
type: meta
created: 2026-06-22
updated: 2026-06-22
sources: []
tags: [meta, format, schema]
confidence: high
---

# Format: Tag Taxonomy

> The controlled vocabulary for frontmatter `tags`. Tagging from this list keeps Dataview/Bases views and the graph clean. The linter checks tags against the merge map below and warns on drift, single-use tags, and hex codes. The vocabulary is extensible — add a tag here first, then use it.

## Rules

- Lowercase, hyphenated. No `#` prefix in frontmatter. No spaces.
- Prefer an existing tag over minting a near-duplicate.
- A tag should be used by **>= 2 pages**; single-use tags are merge/removal candidates.
- Never let a hex color (e.g. `#E8E8E8`) sit unescaped in a body — it indexes as a tag. Wrap in backticks.

## Canonical vocabulary (faceted)

**Nature** — `entity` `concept` `source` `project` `domain` `comparison` `synthesis` `query` `meta` `person` `company` `tool` `repository` `framework` `pattern` `methodology` `template`

**Domain** — `ai` `software-engineering` `design` `business` ← _seed with the owner's domains during setup; expand freely as sources are ingested_

**Theme** — `architecture` `performance` `leadership` `strategy` ← _seed with the owner's project themes during setup; expand freely as sources are ingested_

**Personal & ops** — `personal` `health` `goals` `lint` `playbook` `format`

## Merge map (drift -> canonical)

`MERGE_MAP` in `skills/wiki-maintenance/scripts/common.py` is the single place to configure this — both the linter's drift report and `normalize_tags.py`'s fixer read from it. It's empty by default; a starting point once you have real drift to fix might look like:

- `projects` -> `project`
- `metric` -> `metrics`
- `architect` -> `architecture`

## Deliberately distinct (do NOT merge)

These might cluster by prefix but mean different things:
- `person` vs `personal`

