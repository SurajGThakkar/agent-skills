---
title: "Playbook: Suggest"
type: meta
created: 2026-06-27
updated: 2026-06-27
sources: []
tags: [meta, playbook, workflow]
confidence: high
---

# Playbook: Suggest

> Load this when {OWNER_NAME} runs `suggest` or asks for proactive ideas ("what should I read next?", "what questions should I be asking?", "what's missing from my wiki?"). This is the compounding feature — the wiki generates its own next questions rather than waiting passively for new sources.

## Principle

The second brain should get smarter about its own gaps over time. `suggest` is how that surfaces: it reads the current state of knowledge, identifies where coverage is thin or contradicted, and proposes specific next steps — not vague advice like "read more about AI" but concrete, actionable items tied to {OWNER_NAME}'s actual goals and current wiki state.

## Steps

1. **Harvest open questions** from across the wiki:
   ```bash
   grep -r "^## Open Questions" wiki/ --include="*.md" -l
   ```
   Then read each file's `## Open Questions` section. Collect all non-empty bullet points.

2. **Identify structural gaps** — read `index.md` and look for:
   - Concepts or entities referenced across 3+ pages (via `[[wikilink]]`) but lacking their own dedicated page (i.e., not listed in the index as a content page).
   - Pages with `confidence: low` or `confidence: speculative` that could be upgraded with a targeted web search or a single good source.
   - Domains in `wiki/domains/` with fewer than 2 sources in their `sources:` frontmatter — these are structural hubs with thin evidence.
   - Pages whose `updated:` date is more than 60 days old and are linked by 3+ other pages (high-centrality stale pages).

3. **Read the latest lint report** (if one exists in `wiki/meta/lint-reports/`): extract its gap analysis section if present. Contradictions and orphans listed there are high-priority inputs.

4. **Cross-reference with {OWNER_NAME}'s goals** from the profile page `[[{OWNER_SLUG}]]`: frame suggestions in terms of active projects and stated interests, not just wiki structure.

5. **Synthesize 3-5 concrete suggestions** across two categories:

   **Questions to ask the wiki** — things worth querying and filing as a synthesis page:
   - "How do your beliefs about [X] compare across your [N] most recent sources?"
   - "What's the common pattern between `[[concept-A]]` and `[[concept-B]]` given what you've read?"
   - "What's the strongest case against `[[your-current-view-on-topic]]`?"

   **Sources to find** — specific articles, papers, authors, repos, or talks to seek:
   - Named sources already referenced but not yet ingested ("`[[source-name]]` is cited on 3 pages but the source page is empty — the original is at [URL if known].")
   - Gaps your open questions point to ("Your open question on `[[concept]]` mentions needing data on X — a search for 'X site:scholar.google.com' should surface 2-3 candidates.")
   - Authoritative sources for low-confidence pages ("`[[entity]]` is marked `speculative` — it's well-covered in [specific book/talk/paper].")

6. **Persist to source queue** (offer, don't impose):
   After presenting suggestions, ask {OWNER_NAME}: "Want me to add these to your source queue so you don't lose them?"
   If yes, append to `wiki/meta/source-queue.md` (creating it if needed) using the format from [[log-format]] with type `suggest`:
   ```markdown
   ## [YYYY-MM-DD] suggest | Brief description
   Source or question details. Why it was flagged.
   ```
   The source queue is append-only. {OWNER_NAME} removes items manually when acted on, or the LLM can mark them `[done]` when an ingest completes.

## Guardrails

- Be **specific**. "Read more about machine learning" is not a suggestion. "The Bitter Lesson (Sutton, 2019) is referenced in `[[machine-learning]]` but never ingested — it's 1,200 words and directly addresses the open question in `[[deep-learning]]`" is a suggestion.
- Prioritize suggestions by **impact on {OWNER_NAME}'s active projects** (see profile), not by what would make the wiki structurally cleanest.
- Cap at 5 suggestions per run. More than that diffuses attention. Let the queue hold the rest.
