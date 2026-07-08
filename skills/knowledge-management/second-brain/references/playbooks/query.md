---
title: "Playbook: Query"
type: meta
created: 2026-06-22
updated: 2026-06-22
sources: []
tags: [meta, playbook, workflow]
confidence: high
---

# Playbook: Query

> Load this when {OWNER_NAME} asks a question against the wiki.

## Steps

1. **Read `index.md`** to identify relevant wiki pages (the index is the routing layer; see [[index-format]]).
2. **Widen (optional, max 3 CLI calls, only if Obsidian is running):** if the question spans projects/domains/concepts not co-located in the index:
   - `obsidian search:context query="<key-term>" path="wiki" limit=10 format=json`
   - `obsidian backlinks file="<anchor-page>"` on the single most relevant page
   - Hard ceiling: read at most **15 pages** per query. If Obsidian is not running, skip — the index is the fallback.
3. **Read** the relevant pages (and raw sources if depth is needed).
4. **Synthesize** an answer with `[[page-name]]` citations. Match the output format to the question type:

   | Question type | Output format |
   |---|---|
   | Conceptual explanation or factual answer | Prose markdown (inline in chat or file as `query.md`) |
   | "Compare X vs Y" | Markdown comparison table + prose summary; file as `comparison.md` |
   | "Show me the relationship between..." | File as `synthesis.md` with a structured argument |
   | Data-driven analysis ("how has X changed over time?") | matplotlib chart via code execution, then file the chart + analysis |
   | "Give me a presentation on..." | Marp slide deck (frontmatter: `marp: true`) |
   | Multi-step decision or workflow | Numbered markdown list; file as `query.md` |

   When uncertain: default to prose markdown. The format should serve the question, not the other way around.

5. **Compound it.** If the answer is worth preserving, file it back as a page in `wiki/queries/` (`templates/query.md`) or `wiki/syntheses/` (`templates/synthesis.md`), then regenerate the index (`build_index.py`) and append to `log.md`. If not, deliver in chat only. **Good explorations should not disappear into chat history.**
6. **Note gaps** discovered during the query — suggest sources to investigate. If you found missing cross-links, fix them now (write-back strengthens future queries).

## Scaling note

The index-first routing in step 1 works well at moderate scale. When it strains (rough trigger: >250 content pages, or query routing feels slow or lossy), add an on-device markdown search engine.

**Recommended: [qmd](https://github.com/tobi/qmd)** — hybrid BM25 + vector + LLM re-rank, all on-device. Two interfaces:
- **CLI:** `qmd search "your query" --path wiki/` — shell out from within a session
- **MCP server:** exposes qmd as a native tool (add to your MCP config and the LLM can call it directly)

Install:
```bash
# Requires Go 1.21+
go install github.com/tobi/qmd@latest

# Index your wiki (run once, then re-index after large ingests)
qmd index wiki/

# Test a search
qmd search "machine learning gradient descent" --path wiki/ --top 5
```

Add qmd re-indexing to your lint loop (step 4 of [[lint]]) once installed. Until then, the index plus optional Obsidian CLI widen step is sufficient.
