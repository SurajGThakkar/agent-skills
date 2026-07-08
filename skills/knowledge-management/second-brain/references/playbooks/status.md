---
title: "Playbook: Status"
type: meta
created: 2026-06-27
updated: 2026-06-27
sources: []
tags: [meta, playbook, workflow]
confidence: high
---

# Playbook: Status

> Load this when {OWNER_NAME} runs `status` or asks for a vault snapshot ("how's the wiki?", "what have I been working on?", "how big is my vault?"). Produces a concise, at-a-glance health report in a single screen — no pagination.

## Steps

1. **Page counts:** read `index.md` header line (`> Last updated: ... | Total pages: N | Total sources: N`). If the index is stale (no header line or last-updated > 7 days ago), run `python3 skills/wiki-maintenance/scripts/build_index.py` first.

2. **Recent activity:** run `grep "^## \[" log.md | tail -5`. This returns the last 5 log entries (type + title + date) without loading the full log.

3. **Quick health check:** run `python3 skills/wiki-maintenance/scripts/lint.py --summary-only` and report the one-line critical/warning count it prints. (This skips writing a full dated report to `wiki/meta/lint-reports/` — appropriate here since `status` runs often and a full report on every check would just pile up near-duplicate files. Run plain `lint` instead when you actually want the detailed report.)

4. **Growth this month:** count pages created this month with:
   ```bash
   grep -rl "created: $(date +%Y-%m)" wiki/ --include="*.md" | grep -v "wiki/meta/" | wc -l
   ```

5. **Source queue:** check if `wiki/meta/source-queue.md` exists. If it does, run `grep "^## \[" wiki/meta/source-queue.md | wc -l` and surface the count.

6. **Scratch backlog:** check if `raw/scratch/` exists (only present if the Operator's research budget has ever been enabled). If it does, run `ls raw/scratch/ | wc -l` for the count and `find raw/scratch/ -mtime +30 | wc -l` to flag anything older than 30 days awaiting review.

7. **Report** — keep it to a single screen:
   ```
   ## Vault: {VAULT_NAME} — Status

   Pages: N total (entities: N, concepts: N, sources: N, projects: N, ...)
   Sources ingested: N
   Created this month: N pages

   Recent activity:
   - [date] ingest | Source title
   - [date] query  | Question saved
   - [date] lint   | Zero criticals
   ...

   Health: ✓ zero criticals   OR   ⚠ N criticals — run `lint` to resolve

   Source queue: N items pending   OR   (no queue yet)
   Scratch: N pending review[, N older than 30 days]   OR   (research not enabled)
   ```

8. **Suggest next action** based on what you see:
   - Criticals exist → "Run `lint` to resolve N critical issues."
   - No ingest in 7+ days → "You haven't ingested a source in a while. Run `suggest` for ideas."
   - Log > 40 entries → "Log is getting long — `rotate_log.py` will archive the older entries."
   - Source queue has items → "You have N sources queued — try `ingest [first item from queue]`."
   - Scratch has items → "The Operator researched N question(s) overnight — see `raw/scratch/`, and `ingest` whichever ones hold up."
   - Scratch has items older than 30 days → "N scratch item(s) have sat unreviewed for a month — worth a look, or say the word and I'll clear them out."
