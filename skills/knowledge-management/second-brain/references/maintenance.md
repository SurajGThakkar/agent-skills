# Maintenance Mode

Disclosed reference for the Maintain branch of the `second-brain` skill. Read SKILL.md for branch routing and shared rules.

---

**The LLM runs all scripts.** When the user types a maintenance command (`lint`, `status`, `/lint`, "check wiki health", or similar), execute the relevant scripts immediately via `bash_tool` — do not instruct the user to open a terminal or run commands themselves. Present all proposed fixes as simple conversational choices, not patch diffs or raw JSON. Example pattern: "I found a broken link to 'AI Ethics' on your [[deep-learning]] page. Should I (1) repoint it to 'Artificial Intelligence Ethics', (2) remove the link, or (3) skip this one?"

**If any Python script fails with a PyYAML ImportError, automatically run `pip install pyyaml` (or politely ask the user to run it) and then retry the script.** Error handling is explicit and helpful; solve problems rather than punt to the user.

---

## The Lint Loop

The vault ships with deterministic Python scripts in `skills/wiki-maintenance/scripts/`. They parse markdown directly — no running Obsidian app required. Every finding ships a concrete fix. No flag-only.

1. **Scan**: `python3 skills/wiki-maintenance/scripts/lint.py`
   - Outputs `results.json` (machine-readable) and a dated report in `wiki/meta/lint-reports/`

2. **Review & Propose Fixes**: Read `skills/wiki-maintenance/results.json` (written by the lint script). The script proposes a worklist — you exercise judgment and propose semantic fixes for each item.
   - Broken link? Propose a repointed link based on Levenshtein distance or semantic similarity.
   - Tag drift? Propose a merge to the canonical form in the taxonomy.
   - Contradiction? Propose resolving the contradiction explicitly.
   - Confidence violation? Check if the page genuinely has enough sources to justify its rating.

3. **Walk and Fix**: Walk the user through each proposed fix item-by-item using `AskUserQuestion`. Instead of a flat binary choice, use per-finding sub-prompts that match the degrees of freedom for the fix type:
   - *For broken links:* "Apply with target [X] / Pick a different target / Decline"
   - *For tag drift:* "Merge / Edit text / Decline"
   - *For contradictions:* "Winner: [A] / [B] / defer to a third source -> Apply rewrite / Decline"
   *Scripts propose, the LLM disposes.*

   **Walk complete when every item in the worklist has been accepted, modified, or declined by the user.**

4. **Rebuild**: 
   - `python3 skills/wiki-maintenance/scripts/build_index.py` — regenerate the catalog
   - `python3 skills/wiki-maintenance/scripts/calibrate_confidence.py` — clear false flags
   - `python3 skills/wiki-maintenance/scripts/rotate_log.py` — archive old log entries if needed

5. **Verify**: Run `lint.py` again. Repeat until **zero criticals**.

6. **Log**: Append a maintenance entry to `log.md`.

---

## Available Scripts

| Script | Purpose |
|---|---|
| `lint.py` | Full health scan. Exits non-zero if criticals exist. |
| `build_index.py` | Regenerates `index.md` from page frontmatter. Never hand-edit the index. |
| `rotate_log.py [keep]` | Archives older log entries, keeps last `keep` (default 40). |
| `calibrate_confidence.py [--dry-run]` | Clears false confidence flags (e.g., entity marked `high` with < 2 sources). |
| `normalize_tags.py [--dry-run]` | Rewrites frontmatter `tags` lists in-place to canonical form per the merge map. |
| `fix_sections.py [--dry-run]` | Adds missing standard sections (Overview, Key Points, Connections, Open Questions, Sources) to entity/concept/project/domain pages. Generates Sources from frontmatter; inserts honest light placeholders for the rest. |
| `repo-capture.sh <org> <repo>` | Captures GitHub repo provenance metadata into `raw/repos/<org>--<repo>/_capture.yml`. Requires `gh` CLI for live data; gracefully stubs if unavailable. |
| `common.py` | Shared parser and vault scanner (imported by the others). |
