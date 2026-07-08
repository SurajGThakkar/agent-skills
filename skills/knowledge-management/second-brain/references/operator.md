# Operator Mode

Disclosed reference for the Operate branch of the `second-brain` skill. Read SKILL.md for branch routing and shared rules.

---

## Overview

Operate builds a standalone, autonomous prompt that runs the vault's own wiki-maintenance toolkit on a schedule, with no human in the loop for that run. One run = one session: scan, apply only the fixes that need no judgment call, rebuild the index, rotate the log, surface (never act on) the source-queue and scratch backlogs, optionally research open questions into `raw/scratch/`, log the run, stop.

This is the scheduled sibling of the Maintain branch's lint loop (`references/maintenance.md`), not a replacement for it. Anything a fix requires interpretation for — broken-link targets, contradictions, tag drift outside the canonical merge map — still needs a supervised `lint` session; the Operator queues it, it doesn't guess at it. Ingestion is never run unattended, for the same reason (`references/llm-wiki-at-scale.md`).

Research is the one optional exception to "nothing happens without the owner" — and even then, it only ever writes new files into `raw/scratch/`, never into `wiki/`, and never touches anything already in `raw/`. That's the same allowance `ingest.md` already uses when it saves a freshly-fetched URL; this just extends it to material the Operator went looking for on its own initiative. Turning it on doesn't change what gets ingested, only what's waiting, pre-researched, next time the owner reviews the backlog.

## Reference files

- `references/operator-prompt-template.md` — the prompt this phase renders. Read it before Phase 2.
- `references/maintenance.md` — the lint loop this reuses. Read it if you need to explain to the user why some fixes are deferred rather than applied.
- `references/llm-wiki-at-scale.md` — the ingestion-stays-supervised principle behind the "never auto-ingest" rule below.

## Hard rules

- **Vault must be set up first.** If `skills/wiki-maintenance/scripts/` doesn't exist, stop and direct the user to the Setup branch instead. Don't build an Operator for a vault that isn't ready to run one.
- **No judgment calls, ever.** The fix step is exactly the Unattended variant in `playbooks/lint.md` (deployed to the vault as `wiki/meta/playbooks/lint.md`) — nothing here restates which scripts run or in what order. Anything that variant excludes — broken-link targets, contradictions — stays in the report and the queue. This is AGENTS.md Operating Rule 11 ("scripts propose, the LLM disposes") applied to a run with nobody watching.
- **Never run ingest unattended.** Surface the `wiki/meta/source-queue.md` backlog — count and oldest entry — and stop there. Ingestion stays supervised, one source at a time.
- **Research never touches `wiki/` or existing `raw/` files, and respects its own budget.** If enabled, findings land only in new files under `raw/scratch/`, tagged `status: unreviewed`, capped at the run's research budget — the Operator places, never modifies, and the owner decides what gets ingested.
- **Respect the fix budget.** Stop applying fixes once the run hits the cap from Phase 1; queue the remainder rather than exceeding it silently.
- **Never touch the schema file.** `AGENTS.md`/`CLAUDE.md` belongs to Setup and the owner, not the Operator.
- **Default to defaults.** Don't re-litigate a choice the user already made in Phase 1 on a re-render; only revisit it if they explicitly want to change it.
- **One sanity pass for `{{`.** Never save a rendered prompt with placeholders still in it.
- **Always finish by scheduling.** Phase 4 is mandatory — a saved-but-unscheduled prompt hasn't accomplished anything.

## Phase 0: Silent discovery

Before asking anything, gather what's already knowable from the vault itself:

1. Confirm `skills/wiki-maintenance/scripts/` exists and contains `lint.py`, `fix_sections.py`, `normalize_tags.py`, `calibrate_confidence.py`, `build_index.py`, and `rotate_log.py` — the six this branch depends on (the folder also holds `common.py` and `repo-capture.sh`, which Operate never calls). If any are missing, this vault hasn't been through Setup — stop and say so rather than building an Operator with nothing to schedule.
2. Detect the schema file: `AGENTS.md` or `CLAUDE.md` at the vault root, whichever exists. Read it for `{OWNER_NAME}` and `{VAULT_NAME}`. Note which filename this vault actually uses — the rendered prompt needs to say the right one.
3. Check whether `wiki/meta/source-queue.md` exists. If the vault predates it, that's fine — the rendered prompt should treat "0 pending" as the default, not error.
4. Check whether `skills/wiki-maintenance/operator-prompt.md` already exists. If it does, this is a re-render, not a first build — read it, note the current cadence and fix budget, and only ask about them again in Phase 1 if the user wants to change something.

**Completion:** Vault confirmed ready (or the user has been redirected to Setup). Schema file identified and read. Owner and vault names captured.

## Phase 1: Ask only the gaps

Only ask what Phase 0 couldn't determine. Batch all three questions in one message; use structured input tools if the environment supports them.

**Q1 — Cadence.** How often should the Operator run?
- Daily (default — matches how quickly a personal vault accumulates enough drift to be worth clearing)
- Weekly (lower-activity vaults)
- Custom (a specific interval)

**Q2 — Fix budget.** Cap how many fixes the Operator applies in one unattended run before it stops and queues the rest for a supervised session:
- Light — up to 5
- Default — up to 20
- Heavy — up to 50
- Custom

**Q3 — Research budget.** Should the Operator research open questions overnight and stage findings in `raw/scratch/` for later review? Off by default — this only affects what's waiting for the owner, never what's actually ingested.
- Off (default)
- Light — up to 1 question/run
- Default — up to 3 questions/run
- Heavy — up to 7 questions/run
- Custom

If the scheduled environment turns out not to have search/fetch tools available, the rendered prompt skips this step gracefully and logs that rather than failing — nothing to verify in advance.

**Completion:** Cadence, fix budget, and research budget all set, answered or explicitly defaulted.

## Phase 2: Render

Fill `references/operator-prompt-template.md` with `{{OWNER_NAME}}`, `{{VAULT_NAME}}`, `{{SCHEMA_FILE}}`, `{{CADENCE_HUMAN}}`, `{{FIX_BUDGET}}`, `{{RESEARCH_BUDGET}}`, `{{TODAY}}`.

Sanity pass: search the rendered output for `{{`. If anything remains, fix it or flag it to the user — never save a prompt with unfilled placeholders.

**Completion:** Zero `{{...}}` remain in the rendered prompt.

## Phase 3: Save

Write the rendered prompt to `skills/wiki-maintenance/operator-prompt.md` — alongside the scripts it runs, consistent with AGENTS.md §1's framing of `skills/` as the vault's co-owned automation, not a separate top-level folder. Read it back once to confirm it saved as written.

**Completion:** The file exists at that path and reads back correctly.

## Phase 4: Schedule it (do not stop at "saved")

Immediately invoke the schedule skill via the Skill tool. Set:
- **Command:** run against `skills/wiki-maintenance/operator-prompt.md`
- **Working directory:** the vault root — this is what lets the Operator's own Bash/Read/Write/Glob calls resolve correctly; no external connector or MCP is needed for a purely local vault
- **Cadence:** whatever was set in Phase 1

After the schedule skill returns, tell the user the cadence, where the prompt lives, and how to pause, edit, or cancel the trigger. Do not stop at "saved" — a prompt that's written but never scheduled hasn't done anything.

**Completion:** Schedule confirmed active. User told the cadence and how to manage the trigger.
