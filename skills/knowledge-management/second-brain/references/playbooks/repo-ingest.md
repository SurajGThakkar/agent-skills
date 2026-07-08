---
title: "Playbook: Repository Ingest"
type: meta
created: 2026-06-22
updated: 2026-06-23
sources: []
tags: [meta, playbook, workflow]
confidence: high
---

# Playbook: Repository Ingest

> Load this before adding a GitHub repository. Uses **Layered Distillation** — progressive disclosure optimized for token efficiency. For non-repo sources use [[ingest]].

## Principle

A repo ingest is **never** a filing task. Every repository has a strategic purpose tied to {OWNER_NAME}'s goals — active projects, career trajectory, relocation, wealth-building. Deduce that purpose **first**; it drives what you extract, how deep you go, and which wiki pages you touch. If a repo ingest only produced distillation files and a source page, you under-ingested.

## Steps

1. **Determine strategic purpose.** Before reading any code: why does {OWNER_NAME} care about this repo? What projects, skills, or career goals does it serve? Hold this answer — it drives everything.
2. **Capture provenance.** Run `bash skills/wiki-maintenance/scripts/repo-capture.sh <org> <repo>`. This creates `raw/repos/org--repo/_capture.yml` with pinned commit SHA, stars, license, and snapshot date.
3. **Research** the repository — structured method:
   - Read `README.md` → understand purpose, install, quickstart
   - Read directory tree (depth 2) → identify architecture
   - Read entry point + config files → extract patterns
   - Read `/docs` or `/api` if present → extract API surface
   - Read tests if architecture is unclear → understand contracts
4. **Discuss** key takeaways with {OWNER_NAME} — what it does, what's interesting, relevance to projects.
5. **Write `_relevance.md` FIRST** in `wiki/sources/org--repo/`, using `templates/repo-relevance.md`. Strategic purpose drives all subsequent extraction.
6. **Write the remaining 4 distillation files** in `wiki/sources/org--repo/`, using the corresponding templates (`repo-overview`, `repo-architecture`, `repo-components`, `repo-dependencies`). Copy `commit` and `snapshot` from `_capture.yml` into each file's frontmatter.
7. **Create/update** the `source-org--repo.md` page in `wiki/sources/` (use `templates/source.md`). This page is the entry point — it summarises the repo and links to the 5 distillation files via wikilinks.
8. **Radiate** — this is where the real work happens:
   - Create/update entity pages in `wiki/entities/` for the tool/project.
   - Create/update concept pages in `wiki/concepts/` for new patterns.
   - Cross-link to relevant project, domain, and comparison pages.
   - Flag contradictions with `> [!warning]` on both pages.
   - Add reciprocal back-links where relationships are real.
   - Aim for **10–15 total page touches** (creates + updates) — that's typical for a rich repo. The hard floor is 8; if you touched fewer than 8, you under-ingested.
9. **Regenerate the index** (`build_index.py`), **run lint** to verify zero criticals, and **append to `log.md`** per [[log-format]].

## Design principle

The agent reads `_overview.md` first (cheap). If a query demands depth, it reads `_architecture.md` or `_components.md` on demand. Never load all five files at once — load what you need. This is progressive disclosure: structure knowledge so targeted queries pull only what's needed.

All five distillation files live in `wiki/sources/org--repo/` — fully wikilinkable, linted, indexed, and part of the knowledge graph. Verbatim raw artifacts (READMEs, source dumps) and the `_capture.yml` provenance file stay in `raw/repos/org--repo/`.

## Guardrails

- 8 page touches minimum (10–15 is typical for a rich repo). If you only created distillation files and a source page, you under-ingested.
- Every distillation file **must** have complete frontmatter including `commit` and `snapshot` from `_capture.yml`.
- `_relevance.md` must be written **before** the other 4 files — purpose drives extraction.
- Tag only from the controlled vocabulary in [[tag-taxonomy]].
- Every factual claim on wiki pages must cite a `[[source-*]]` page.
- If the repo changes significantly, update the distillation files in `wiki/sources/` (they are LLM-owned, not immutable). Re-run `repo-capture.sh` to update `_capture.yml` provenance.
