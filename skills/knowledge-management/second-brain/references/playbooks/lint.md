---
title: "Playbook: Lint"
type: meta
created: 2026-06-22
updated: 2026-06-22
sources: []
tags: [meta, playbook, workflow, health]
confidence: high
---

# Playbook: Lint

> Load this for a health check. Lint is a **closed loop**, not just a scan: `lint -> fix -> verify -> log`. Run on demand and after any large ingest.

## The loop

1. **Scan (deterministic):** `python3 skills/wiki-maintenance/scripts/lint.py`. This reads markdown directly (no Obsidian required) and writes `skills/wiki-maintenance/results.json` plus a dated report into `wiki/meta/lint-reports/`. It computes: frontmatter validity, standard-section compliance (entity/concept/project/domain only), type-aware confidence calibration, broken links, orphans, reciprocal-link gaps, and a tag census against [[tag-taxonomy]].
2. **Judgment scan (LLM):** review the report for things scripts cannot judge — contradictions between pages, stale claims superseded by newer sources, important concepts mentioned but lacking a page, and `low`/`speculative` pages that new evidence could upgrade.
3. **Fix:** apply the deterministic fixers and your judgment fixes:
   - `build_index.py` — regenerate `index.md` (counts, Sources column, Skills table).
   - `calibrate_confidence.py` — clear false confidence flags type-aware (never override a deliberate rating).
   - `rotate_log.py` — archive old `log.md` entries if it has grown past the trailing window.
   - `normalize_tags.py` — rewrite frontmatter tags to canonical form per the merge map (use `--dry-run` first to preview).
   - `fix_sections.py` — add missing standard sections to entity/concept/project/domain pages (use `--dry-run` first; review generated placeholder text before committing).
   - Reciprocal links: the report proposes a worklist; **you decide** which back-links are semantically real and add them to the relevant `## Connections` sections. Do not blind-add — irrelevant links function as retrieval noise and make it harder to find the real connections later.
   - Tags: normalize to the controlled vocabulary; backtick-escape any hex codes in bodies.
4. **Verify:** re-run `lint.py`. The gate is **zero criticals** (broken links, missing frontmatter, parse failures). Warnings (sections, reciprocal gaps) are driven toward zero over time.
5. **Log:** append a `lint` entry to `log.md` per [[log-format]] and keep the dated report in `wiki/meta/lint-reports/`.

## Unattended variant

Used by the Operate branch's rendered prompt (`skills/wiki-maintenance/operator-prompt.md`) when nobody is present to answer questions. Same six scripts, same loop shape, with every step that needs a human's judgment either skipped or narrowed to what's already safe:

1. **Scan:** `lint.py --summary-only` instead of the full run — same computation, skips writing another dated report on top of the ones from real sessions (the same flag `status` uses, for the same reason).
2. **Judgment scan:** skipped entirely. Nobody's here to weigh contradictions or stale claims — they stay in the report for the next supervised session.
3. **Fix:** only `fix_sections.py`, `normalize_tags.py`, and `calibrate_confidence.py` run — each `--dry-run` first, then for real — up to the run's fix budget. `build_index.py` and `rotate_log.py` still run every time; they're deterministic, not judgment calls. Reciprocal links are never auto-added — that step is "you decide" even in the loop's normal form, so it has no unattended equivalent; it stays in the report.
4. **Verify:** re-run `lint.py --summary-only` for updated counts. The zero-criticals gate does not apply here — criticals never auto-fix by design, so this run isn't trying to clear them, only reporting accurately.
5. **Log:** one compact entry, not a full report.

Anything this variant can't resolve stays exactly where the normal loop already puts it — the dated report and the reciprocal-link worklist, waiting for the next `lint` session.

## Optional CLI enrichment (only if Obsidian is running)

- `obsidian unresolved verbose` — dangling wikilinks with source files
- `obsidian backlinks` on hub pages (`[[{OWNER_SLUG}]]`, all project pages)
- `obsidian tags sort=count counts` — cross-check the script's tag census
- `obsidian search:context query="Open Questions" path="wiki" format=json` — harvest open questions

## Gap output

End every lint with proactive suggestions: new questions to investigate and new sources to seek. Harvest `## Open Questions` across the wiki into the report's gap analysis.

After surfacing suggestions, **offer to persist them** to `wiki/meta/source-queue.md` (create if absent). This prevents good ideas from disappearing into chat history and makes them available to the `suggest` playbook in future sessions. Format matches the log contract so it's grep-parseable:

```markdown
## [YYYY-MM-DD] suggest | Brief description of source or question
Details: why it was flagged, URL if known, which wiki page it relates to.
```

The file is append-only. Items are removed manually by {OWNER_NAME} or marked `[done]` by the LLM when acted on.
