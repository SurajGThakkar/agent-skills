---
title: "Playbook: Migrate"
type: meta
created: 2026-06-27
updated: 2026-06-27
sources: []
tags: [meta, playbook, workflow, setup]
confidence: high
---

# Playbook: Migrate

> Load this when {OWNER_NAME} is bringing an existing note collection into the vault. Triggered by "import my Notion", "migrate my Roam", "convert my existing notes", "I already have an Obsidian vault", etc.

## Principle

Migration is not a batch-ingest. Raw dumps of old notes are not sources — they're noise mixed with signal. The goal is to extract what's genuinely valuable and integrate it properly into the wiki structure, not to copy everything wholesale. Most migrations surface 20–40% of notes worth keeping; the rest is scaffolding, drafts, and duplicates.

## Phase 1: Triage (before touching the vault)

1. **Get an inventory.** Ask {OWNER_NAME} to share a list of their notes (filenames or folder structure is enough). If migrating from a live system, export first:
   - **Notion:** Settings → Export → Markdown & CSV
   - **Roam:** `...` menu → Export All → Markdown
   - **Obsidian (existing vault):** just point to the vault folder
   - **Bear / Apple Notes / Evernote:** export to markdown via the app's export function or a third-party tool

2. **Categorize the collection** (skim titles and folder structure, don't read everything):
   - **Evergreen notes** — standalone ideas, concepts, or references worth preserving as wiki pages
   - **Project notes** — active or past work, may become `project.md` pages
   - **Journal / diary entries** — chronological, rarely become wiki pages; optionally file as `personal/` raw sources
   - **Drafts and fleeting notes** — quick captures, usually discard or file as raw sources
   - **Reference lists / bookmarks** — may become source pages if the sources are worth ingesting individually

3. **Agree on scope with {OWNER_NAME}.** Don't migrate everything. Identify the 20-40 notes that are genuinely valuable and migrate those first. The rest can wait or be discarded.

## Phase 2: Convert to wiki pages

For each note worth migrating:

1. **Read it** and identify its type: entity, concept, project, domain, source, or comparison.
2. **Write a proper wiki page** from scratch using the correct template — do not copy-paste raw note content. Rewrite in the wiki's voice; add frontmatter, standard sections, and cross-references.
3. **File the original** in the correct `raw/` subdirectory (e.g., `raw/personal/` for journal entries, `raw/articles/` for imported article notes). Never put old notes directly in `wiki/` — they're raw material.
4. **Cross-reference** with existing wiki pages where the imported concept connects.

## Phase 3: Handle specific source types

### Obsidian vault (existing, unstructured)
- If the existing vault already has some structure (folders, tags, frontmatter), read `AGENTS.md` or `CLAUDE.md` if present to understand its schema.
- Run `grep -r "type:" <vault>/ --include="*.md" | head -20` to see if frontmatter typing is already in place.
- Migrate evergreen notes first; move daily notes and fleeting captures to `raw/personal/`.

### Notion pages
- Notion exports often have deeply nested structures. Flatten: top-level databases become `wiki/` pages, sub-pages become sections within those pages or separate pages.
- Clean up Notion's exported markdown quirks: remove `[Untitled]` headings, fix broken image links (images export as separate files), and strip the hex hash suffixes Notion appends to filenames.

### Roam Research
- Roam exports are heavily `[[linked]]`. Many links will reference pages that don't exist yet — treat these as candidates for new wiki pages.
- Daily notes (`[[2024-01-15]]` style) usually belong in `raw/personal/`, not `wiki/`.
- Block references (`((block-id))`) won't resolve in standard markdown — convert to prose or footnotes.

### Bear / Apple Notes
- These often lack structure — mostly prose with inline tags. Treat as raw material and rewrite into wiki pages rather than importing directly.

## Phase 4: Index, lint, log

After the migration batch:

1. **Regenerate the index:** `python3 skills/wiki-maintenance/scripts/build_index.py`
2. **Run lint:** `python3 skills/wiki-maintenance/scripts/lint.py` — expect broken links and missing frontmatter; the lint report is your cleanup worklist.
3. **Log** a migration entry in `log.md`:
   ```markdown
   ## [YYYY-MM-DD] ingest | Migration — {source system}
   Imported N notes from {source}. Created: N entity/concept pages, N project pages, N source pages.
   Filed N raw sources. Ran lint — N criticals to resolve.
   ```

## Guardrails

- Never overwrite existing wiki pages with imported content — merge carefully.
- Raw old notes go in `raw/`, not `wiki/`. Wiki pages are written from scratch.
- Don't migrate more than 20-30 notes in one session — quality degrades at scale. Run in batches.
- After migration, run `suggest` to find what's now newly connectable given the imported content.
