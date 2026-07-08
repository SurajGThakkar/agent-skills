---
title: "Playbook: Ingest"
type: meta
created: 2026-06-22
updated: 2026-06-22
sources: []
tags: [meta, playbook, workflow]
confidence: high
---

# Playbook: Ingest

> Load this before processing any new source. Triggered when {OWNER_NAME} provides an article, transcript, paper, journal entry, etc. For GitHub repositories use [[repo-ingest]] instead.

## Principle

An ingest is never a filing task. Every source has a strategic purpose tied to {OWNER_NAME}'s goals. Deduce that purpose first, then operationalize the knowledge across the vault — don't leave it stranded on an isolated source page.

## URL-first fast path

If {OWNER_NAME} provides a URL (rather than a file already in `raw/`), choose one of:

**Option A — Obsidian Web Clipper (recommended for image-rich pages):** Ask {OWNER_NAME} to use the [Obsidian Web Clipper](https://obsidian.md/clipper) browser extension to convert the page to markdown and save it to the correct `raw/` subdirectory. Then continue with the standard steps below. This preserves images and formatting better than a direct fetch.

**Option B — Direct fetch (fast path for text-heavy sources):**
1. `web_fetch <url>` — extract the article text.
2. Write to `raw/articles/<slug>.md` with a frontmatter header:
   ```yaml
   ---
   title: "{TITLE}"
   url: "{URL}"
   fetched: {TODAY}
   author: "{AUTHOR if detectable}"
   ---
   ```
3. Continue with the standard steps below from step 1.

Note: images embedded in URL sources will not be locally available via Option B. If the source is image-heavy or figures are central to its argument, flag this in the source page and recommend a re-clip with the browser extension.

## Steps

1. **Read** the source fully. Do not skim.
2. **Determine purpose & holistic linking.** Why is this valuable to {OWNER_NAME}'s overarching goals? Plan which entity/concept/project/query pages it should touch and what new pages it justifies.

> [!warning] **Concept bleeding check.** If your extraction plan creates fewer than 8 new or updated pages for a substantive source, you are bleeding the schema's brevity directive into content. Expand your plan before proceeding — extract every granular entity, concept, and technique. (8 is the same hard floor checked again in the Guardrails below — treat it as one bar, not two.)
3. **Discuss** 2-3 key takeaways with {OWNER_NAME} (highlights, surprises, initial reactions).
4. **File** the raw source into the correct `raw/` subdirectory if not already there. Never modify `raw/` content — only place it.
5. **Create** a source summary page in `wiki/sources/` from `templates/source.md`:
   - Full bibliographic info (title, author, date, URL if applicable)
   - 3-5 sentence summary, key claims & data points, notable quotes
   - Relevance to {OWNER_NAME}'s interests/projects
6. **Update** affected wiki pages: add new facts, update outdated claims, note contradictions on both pages, adjust confidence per the rules in [[page-format]], and add cross-references to the new source.
7. **Create** new entity/concept/topic pages for anything substantively covered that lacks a page (use the matching template in `templates/`).

**7a. Connection Alert.** Before moving to link-verification, check whether this source's core insight connects to any active project or concept cluster already in the wiki. Scan `[[{OWNER_SLUG}]]` (active projects) and `index.md` (existing concepts and domains). If a real, specific connection exists, surface it explicitly before the final report — for example: "This source connects directly to your `[[project-name]]` — specifically the section on [specific topic]. I've added a cross-reference." Generic observations don't count ("this relates to productivity"). Only flag connections that are specific enough that {OWNER_NAME} would say "I didn't think of that."

8. **Verify connections (toolkit-first):**
   - Run the linter: `python3 skills/wiki-maintenance/scripts/lint.py` and check the reciprocal-link worklist for the pages you touched. Add back-links where they are semantically real (scripts propose, you decide).
   - Optional enrichment if Obsidian is running: `obsidian backlinks file="<touched-page>"`, `obsidian links file="<source-page>"`, `obsidian tag name="<primary-tag>" verbose`.
9. **Regenerate the index:** `python3 skills/wiki-maintenance/scripts/build_index.py` (do not hand-edit `index.md` tables; see [[index-format]]).
10. **Append to `log.md`** per [[log-format]]. If the entry count now exceeds 40, proactively suggest running `rotate_log.py` before the next session.
11. **Report** to {OWNER_NAME}: what was created/updated, pages touched, open questions, and proactive suggestions (related questions, sources to seek).

## Guardrails

- **Completion criterion for step 7:** A single rich source typically spawns 10-15 wiki pages. Step 7 is not complete until you have created or updated at least 8 wiki pages for a substantive source. If you only created one source page, you under-ingested — go back and extract the granular entities, concepts, and techniques you skipped.
- Tag only from the controlled vocabulary in [[tag-taxonomy]].
- Cite every factual claim back to a `[[source-*]]` page.

## Image handling

If the source contains inline images or figures that are central to its argument:

1. **Read text first** (step 1 above) — build your initial understanding from text alone before looking at images.
2. **After discussing takeaways** (step 3), review images that were referenced in key claims. Use `view <path>` on locally-stored images (downloaded via Obsidian Web Clipper with the "Download attachments" hotkey). If images are only available as remote URLs, note their alt-text and surrounding context.
3. **Note image-derived insights** in the source summary page — flag which findings came from figures vs. text. This matters for reproducibility: "Key claim in §3 is supported by Figure 2 (stored at `raw/assets/figure-2.png`) — verify if claim holds from text alone."
4. **If images are missing or URL-only** and central to the source's argument, add an open question: "Figure 3 shows X — images not locally available. Re-clip with Obsidian Web Clipper to capture locally."
