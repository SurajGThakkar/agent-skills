---
title: "Format: Page"
type: meta
created: 2026-06-22
updated: 2026-06-23
sources: []
tags: [meta, format, schema]
confidence: high
---

# Format: Page

> The canonical structure for every wiki page. Ready-to-copy templates live in `templates/` (one per type). This file is the spec the linter enforces.

## Which template to use?

When you're about to create a new wiki page, use this table to pick the right template and directory:

| What you're documenting | Template | Directory |
|---|---|---|
| An article, paper, video, podcast, transcript, or any consumed source | `source.md` | `wiki/sources/` |
| A real person, company, tool, product, or named project | `entity.md` | `wiki/entities/` |
| An abstract idea, technique, methodology, framework, or pattern | `concept.md` | `wiki/concepts/` |
| An active or past project {OWNER_NAME} is working on | `project.md` | `wiki/projects/` |
| A field or broad area of knowledge (e.g. "machine learning", "real estate") | `domain.md` | `wiki/domains/` |
| A side-by-side analysis of two or more things | `comparison.md` | `wiki/comparisons/` |
| A synthesized argument or thesis across multiple sources | `synthesis.md` | `wiki/syntheses/` |
| A question you asked and an answer worth preserving | `query.md` | `wiki/queries/` |
| A GitHub repository (produces 5 layered files) | `repo-*.md` set | `wiki/sources/<org>--<repo>/` |

**Decision shortcut when uncertain:** start with `source.md` for the document itself, then spin off `entity.md` or `concept.md` pages for the notable things it introduces. A single ingest typically creates 1 source page + 2–4 entity/concept pages, each pointing back to the source.

---

## Frontmatter (required on every page)

```yaml
---
title: "Page Title"
type: entity | concept | project | domain | source | comparison | synthesis | query | repo-overview | repo-architecture | repo-components | repo-dependencies | repo-relevance
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: ["[[source-slug]]"] # CRITICAL: You MUST wrap wikilinks in quotes in YAML arrays to avoid nested array parse errors (e.g. NEVER write [[[source-slug]]])
tags: [tag1, tag2]
confidence: high | medium | low | speculative
---
```

- `project` pages add `status: "..."` (and may add `team`, `domain`).
- `source` pages self-reference in `sources` (e.g. `["[[source-redis--redis]]"]`).
- `domain` pages may have `sources: []` (they are structural hubs).
- The five repo-distillation types (`repo-overview`, `repo-architecture`, `repo-components`, `repo-dependencies`, `repo-relevance`) add `repo_url`, `commit`, and `snapshot` (see below).

## Body structure

```markdown
# Page Title

Brief definition or one-line summary.   <- the index pulls THIS line; keep it tight (<= ~160 chars).

## Overview
Main content. 2-5 paragraphs for most pages.

## Key Points
- Bullet-pointed highlights

## Connections
- [[Related Page]] — relationship description

## Open Questions
- Unresolved items, contradictions, gaps

## Sources
- [[source-slug]] — what this source contributed
```

- The five sections above are required for `entity`, `concept`, `project`, `domain`. Pages may add extra sections freely (e.g. "Problem Space", "Core Dimensions").
- `source`, `comparison`, `synthesis`, `query`, and the five `repo-*` distillation types use their own template shapes (see `templates/`) and are not held to the five-section rule.

## Repo Distillation pages

Repository ingests produce five layered distillation files in `wiki/sources/org--repo/`. Each uses its own template and its own `type:` value (there is no shared `repo-distillation` type) plus this additional frontmatter:

```yaml
repo_url: "https://github.com/org/repo"
commit: "abc123def012"  # default branch HEAD at snapshot time
snapshot: YYYY-MM-DD     # when the distillation was created
```

The five layers (progressive disclosure — read on demand, never all at once). None are indexed by type in `index.md`; the umbrella `source.md` page for the repo is what's indexed, and it links out to these five as sub-detail:

| Layer | File | `type:` | Template | Purpose | Target |
|---|---|---|---|---|---|
| 1 | `_overview.md` | `repo-overview` | `templates/repo-overview.md` | What it is, tech stack, purpose | ~500 tokens |
| 2 | `_architecture.md` | `repo-architecture` | `templates/repo-architecture.md` | Core architecture, design patterns | ~1,000 tokens |
| 3 | `_components.md` | `repo-components` | `templates/repo-components.md` | Key components and public API/interfaces | ~1,000 tokens |
| 4 | `_dependencies.md` | `repo-dependencies` | `templates/repo-dependencies.md` | Internal and external dependencies | ~500 tokens |
| 5 | `_relevance.md` | `repo-relevance` | `templates/repo-relevance.md` | Strategic purpose, project connections | ~500 tokens |

`_relevance.md` is written **first** during ingest — strategic purpose drives extraction.

## Confidence rules (type-aware)

Confidence is an LLM/human judgment; the calibrator only clears false flags, never overrides a deliberate rating.

- **entity / concept:** `high` requires >= 2 corroborating sources — UNLESS first-party ({OWNER_NAME}'s own profile/work), which may be `high` with the owner as the source.
- **project (owned):** may be `high` ({OWNER_NAME} is the primary source).
- **source:** reflects the reliability of the source itself, not corroboration count. Exempt from the multi-source rule.
- **domain:** reflects the maturity of the overview and the strength of its inbound hub links, not `sources` count. Exempt from the multi-source rule.
- `medium` — single reliable source or reasonable inference. `low` — limited data, early signal. `speculative` — hypothesis, needs verification.

### Propagation when evidence conflicts

When a new source contradicts or significantly qualifies a claim on an existing page:

1. Add a `> [!warning]` callout on **both** the entity/concept page and the new source page, naming the contradiction explicitly.
2. **Downgrade:** if the new source is more recent and from a higher-quality venue, downgrade confidence by one step (`high → medium`, `medium → low`) and note `> Superseded in part by [[source-new]] on [date]`.
3. **Hold and flag:** if sources are of comparable authority, keep the current confidence level but add a `> [!question]` callout noting the open disagreement. Do not silently rewrite the claim.
4. **Upgrade:** a second independent corroborating source from a different venue upgrades `medium → high` for entity and concept pages. Note the new source in the page's `## Sources` section and update the `updated:` frontmatter date.
5. **Never silently overwrite** a claim — always log which source caused the change in the `## Sources` section of the page you're updating.

## Conventions

- **Filenames:** lowercase, hyphenated (`predictive-maintenance.md`). Repo sources may use `--`; versions may use `.`.
- **Wiki links:** always `[[double-bracket]]`. Link `[[index]]` / `[[log]]` (never `[[index.md]]`). Reference `raw/` files with backticks, never wikilinks.
- **Cross-references:** link aggressively — every mention of a page that exists gets a `[[wiki-link]]` — but only where the relationship is real.
- **Tags:** only from the controlled vocabulary in [[tag-taxonomy]].
- **Dates:** ISO 8601.
- **Callouts:** `> [!warning]` contradictions, `> [!tip]` recommendations, `> [!question]` open questions, `> [!example]` examples.
- **Highlights:** `==key claim==` for critical findings.
- **Block refs:** append `^block-id` to findings future queries may cite (`[[page#^block-id]]`).
