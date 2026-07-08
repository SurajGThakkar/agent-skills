# AGENTS.md — LLM Wiki Schema (lean core)

> **Owner:** {OWNER_NAME} | **Vault:** {VAULT_NAME} | **Schema version:** 1.0 | **Last updated:** {TODAY}

This vault is {OWNER_NAME}'s **persistent, compounding second brain** — a structured, interlinked wiki maintained by an LLM. The LLM writes and maintains all wiki content; {OWNER_NAME} curates sources, directs analysis, and asks questions. The bookkeeping is the LLM's job so maintenance cost stays near zero.

This file is the always-on contract. Detailed workflow steps and format specs live in modules you load **on demand** (see §7). Read the matching module before performing a workflow — do not work from memory.

---

## 1. Three layers

- **`raw/`** — immutable source documents. The LLM **reads, never writes** here. Source of truth.
- **`wiki/`** — LLM-owned markdown. The LLM creates, updates, and reorganizes freely. {OWNER_NAME} reads/browses.
- **schema** — this `AGENTS.md` (co-evolved) + its modules in `wiki/meta/`. Either party proposes changes; changes are logged.
- **`skills/`** — co-owned automations (incl. the wiki-maintenance toolkit). {OWNER_NAME} may run scripts or intervene.

## 2. Directory map

```
{VAULT_NAME}/
├── AGENTS.md            ← this lean core
├── index.md             ← content catalog (auto-generated; never hand-edit tables)
├── log.md               ← chronological append-only activity log
├── raw/                 ← immutable sources: articles papers youtube repos books courses
│                          podcasts threads transcripts projects research personal data assets
│   └── repos/org--repo/ ← verbatim artifacts (READMEs, source dumps) + _capture.yml provenance
├── wiki/                ← LLM-owned pages
│   ├── entities/ concepts/ projects/ domains/ comparisons/ syntheses/ queries/
│   ├── sources/         ← source summaries + repo distillation subfolders
│   │   └── org--repo/   ← 5 layered distillation files (_overview … _relevance)
│   └── meta/            ← operational schema & health
│       ├── playbooks/   ← workflow detail (ingest, repo-ingest, query, lint, schema-update,
│       │                   status, suggest, migrate)
│       ├── formats/     ← specs (page, index, log, tag-taxonomy)
│       ├── source-queue.md ← persisted suggestions from lint/suggest (append-only)
│       ├── lint-reports/ log-archive/ dashboards/
├── skills/              ← agent skills, incl. wiki-maintenance/ (lint, build_index, rotate_log)
└── templates/           ← one page template per type (incl. repo-overview … repo-relevance)
```

Filing: drop each raw source in the subdirectory matching its kind (`youtube/`, `papers/`, `articles/`, `repos/org--repo/`, `projects/`, `research/`, `personal/`, etc.). Naming: lowercase, hyphenated; repos use `org--repo-name/`. Repo distillation files (LLM-authored) go in `wiki/sources/org--repo/`, not `raw/`.

## 3. Conventions (full spec: [[page-format]])

- Filenames lowercase-hyphenated. Wiki links `[[double-bracket]]`; link `[[index]]`/`[[log]]` (never `.md`); reference `raw/` files with backticks.
- Every page carries full frontmatter (`title, type, created, updated, sources, tags, confidence`); projects add `status`.
- Link aggressively but only where the relationship is real. Cite every claim to a `[[source-*]]` page. Flag contradictions on both pages.
- Tag only from the controlled vocabulary in [[tag-taxonomy]]. Confidence is type-aware (see [[page-format]]): `source`/`domain` are exempt from the multi-source rule; owned projects may be `high`.
- Dates ISO 8601. Use callouts (`> [!warning]/[!tip]/[!question]`), `==highlights==`, and `^block-ids` for citable findings.

## 4. Workflows — load the playbook first

Before performing any workflow, **read its playbook**. Each is one short file:

- **Ingest** a source → read [[ingest]]
- **Ingest a GitHub repo** → read [[repo-ingest]]
- **Query** the wiki → read [[query]]
- **Lint / health check** → read [[lint]] (a closed `lint → fix → verify → log` loop)
- **Change the schema** → read [[schema-update]]
- **Vault snapshot / stats** → read [[status]]
- **Proactive suggestions** → read [[suggest]]
- **Import from another PKM** → read [[migrate]]

## 5. Operating rules

1. Every interaction follows this schema.
2. Read before writing — check `index.md` to avoid duplicates.
3. Link aggressively (real relationships only); cite sources for every claim.
4. Flag contradictions explicitly on both pages.
5. Maintain confidence levels as evidence accumulates (type-aware).
6. Keep the index current — regenerate it via the toolkit, never hand-edit tables.
7. Log every ingest, query-save, lint, and schema change.
8. Suggest proactively — related questions, sources to seek, connections to explore.
9. Respect privacy — never expose personal information beyond what the owner has shared.
10. Holistic ingestion — find the strategic purpose of every source and operationalize it across the vault. **CRITICAL: The 'lean schema' directive applies ONLY to operational files (AGENTS.md, playbooks). It does NOT apply to content generation. Ingestions must be sprawling, comprehensive, and exhaustive, extracting every granular entity, concept, and technique (typically 10-15 pages per rich source) to prevent knowledge stranding.**
11. The LLM does the judgment work; scripts do deterministic bookkeeping and **propose** worklists. Never blind-apply script output.
12. Guard against concept bleeding: if you notice your extraction producing broad summaries instead of granular pages, you are bleeding the schema's brevity directive into content. Stop, reset, and extract relentlessly.
13. Deep Research Check: If you have insufficient information to provide a highly robust, holistic, and accurate answer for a complex goal, STOP and ask the user if they want you to perform a "deep research" phase (via web search or a research subagent) before generating a solution.
14. Guard against data loss: Never apply destructive cleanups on raw source files without first verifying that their contents have been fully ingested and distilled into the `wiki/` directory. If you must delete un-ingested raw source files for any reason, you MUST obtain explicit user consent first.

## 6. Maintenance

- Toolkit: `skills/wiki-maintenance/` reads markdown directly (no Obsidian required). Core scripts: `lint.py`, `build_index.py`, `rotate_log.py`, `calibrate_confidence.py`, `normalize_tags.py` (tag drift → canonical), `fix_sections.py` (add missing standard sections), `repo-capture.sh` (GitHub repo provenance).
- Cadence: run the lint loop ([[lint]]) on demand and after any large ingest; gate to **zero criticals**.
- Source queue: `wiki/meta/source-queue.md` — append-only list of suggested sources and questions, populated by [[lint]] and [[suggest]]. Review before each session.
- Human browsing: [[wiki-health-dashboard]] (Obsidian Bases views over frontmatter) complements the agent-facing [[index]].
- Obsidian CLI (`obsidian ...`) is optional enrichment, used only when the app is running.

## 7. Module index

- Playbooks: [[ingest]] · [[repo-ingest]] · [[query]] · [[lint]] · [[schema-update]] · [[status]] · [[suggest]] · [[migrate]]
- Formats: [[page-format]] · [[index-format]] · [[log-format]] · [[tag-taxonomy]]
- Profile: [[{OWNER_SLUG}]]

## 8. Commands

`ingest [source or URL]` · `query [question]` · `lint` · `update schema` · `status` · `suggest` · `migrate`

---

*Living document — evolves as the wiki grows. Detail lives in modules; this core stays lean.*
