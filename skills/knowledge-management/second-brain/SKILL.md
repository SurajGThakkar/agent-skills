---
name: second-brain
description: >
  Set up, maintain, or operate a personal wiki vault (second brain).
  Three branches: **Setup**, **Maintain**, **Operate**. Trigger for:
  "set up my second brain", "lint my wiki", "schedule my vault operator",
  "check wiki health", "operate my second brain", or any vault bootstrap,
  maintenance, or operator task — even phrased casually.
---

# Second Brain

Bootstrap, maintain, or operate an LLM-managed personal wiki using the [LLM Wiki at Scale](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern. The LLM incrementally builds a persistent, interlinked wiki from raw sources — knowledge compiled once, kept current, compounding with every ingest.

Three branches. Read the disclosed file before executing.

---

## Shared Rules

- **TaskCreate visible.** Use TaskCreate to make stages visible to the user on every branch.
- **Scripts propose, LLM disposes.** Deterministic scripts hand clean worklists; the LLM exercises judgment. Never blind-apply script output.
- **Anti-bleed rule.** "Lean" applies ONLY to operational files (AGENTS.md, playbooks, scripts). Content generation — ingestion, entity extraction, concept pages — must be *relentless*: sprawling, exhaustive, granular. A rich source spawns 10-15 pages. If you produce one summary page, you are committing premature completion and stranding knowledge. The schema is lean so the *content* can be massive.
- **Handoff.** Day-to-day ingest and query run through the vault's own AGENTS.md (or CLAUDE.md) playbooks once live — not this skill.

---

## Branch: Setup

**When:** User wants a new vault, or to continue a partial bootstrap.
**Read:** `references/setup.md`
**Completion:** Every phase (Discovery → Scaffold → Interview → Inject → Build → Orient) completed. Zero `{...}` placeholders remaining in generated files. User oriented with core commands and a suggested first action.

---

## Branch: Maintain

**When:** User asks to lint, health-check, rebuild index, rotate logs, calibrate confidence, or normalize tags.
**Read:** `references/maintenance.md`
**Completion:** Lint loop exits with zero criticals. Index rebuilt. Log entry appended. Every worklist item accepted, modified, or declined by the user.

---

## Branch: Operate

**When:** User wants to build or schedule an autonomous wiki-maintenance Operator.
**Read:** `references/operator.md`
**Completion:** Operator prompt saved with zero `{{...}}` placeholders. Schedule wired via the schedule skill. User told the cadence and how to manage the trigger.
**Scope:** Pure wiki upkeep, scheduled and unattended — lint, the three safe fixers, index rebuild, log rotation, source-queue and scratch visibility — run locally against the vault with no external connectors and no MCP. It never resolves judgment calls (broken links, contradictions, tag drift) and never auto-ingests; both stay queued for a supervised session. Optionally researches open questions into `raw/scratch/` for later review — never into `wiki/`, and off by default.

---

## Reference Files

Progressive disclosure — load only for the active branch or on demand.

| File | Purpose | Branch |
|------|---------|--------|
| `references/setup.md` | Full setup workflow (Phases 0–E) | Setup |
| `references/maintenance.md` | Lint loop, script table, fix patterns | Maintain |
| `references/operator.md` | Operator build + schedule (Phases 0–4) | Operate |
| `references/AGENTS-template.md` | Schema template for new vaults | Setup |
| `references/llm-wiki-at-scale.md` | Architecture philosophy | Any (on demand) |
| `references/playbooks/*.md` | Vault playbook templates | Setup |
| `references/formats/*.md` | Page/index/log/tag format specs | Setup |
| `references/operator-prompt-template.md` | Rendered wiki-maintenance operator prompt | Operate |
