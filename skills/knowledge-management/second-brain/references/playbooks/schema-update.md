---
title: "Playbook: Schema Update"
type: meta
created: 2026-06-22
updated: 2026-06-22
sources: []
tags: [meta, playbook, workflow]
confidence: high
---

# Playbook: Schema Update

> Load this when changing how the wiki operates. `AGENTS.md` is co-evolved — either party can propose changes.

## Steps

1. **Discuss** the change and its rationale with {OWNER_NAME}.
2. **Decide where it lives.** Keep the lean core (`AGENTS.md`) small:
   - Behavioral contract, conventions, directory map, operating rules, workflow index -> edit `AGENTS.md`.
   - Workflow detail -> edit the relevant file in `wiki/meta/playbooks/`.
   - Format/spec detail -> edit the relevant file in `wiki/meta/formats/`.
   - Tooling behavior -> edit `skills/wiki-maintenance/`.
3. **Apply** the edit in the smallest correct location. Do not duplicate detail back into the core.
4. **Bump** the schema version and `Last updated` date in `AGENTS.md`.
5. **Log** a `schema-update` entry in `log.md` per [[log-format]].

## Version numbering

Use `MAJOR.MINOR` in the `Schema version:` field of `AGENTS.md`:

- **Minor** (`1.0 → 1.1`): additions that don't break existing pages or workflows. Examples: new playbook added, new tag in taxonomy, new section added to a format spec, new CLI script.
- **Major** (`1.x → 2.0`): structural changes that require touching existing pages or rewriting existing playbooks. Examples: renaming core directories, changing frontmatter fields required on all pages, splitting or merging playbooks, changing the confidence scale.

When bumping a major version, add a migration note to the log entry explaining what changed and what needs updating across existing pages (e.g., "All entity pages now require a `domain:` frontmatter field — run `fix_sections.py` then manually fill in domain for each entity page").

## Rule

The lean core stays the single human-readable entry point. Progressive disclosure means detail lives in modules the agent loads on demand — but the core must always link to every module so nothing is orphaned from the schema.

## Skill version upgrades

If the second-brain skill ships a new version, run `schema-update` mode: compare the new AGENTS-template.md and playbooks against the installed ones and apply only the delta — do not overwrite user customizations. Specifically:
- New playbook files: copy to `wiki/meta/playbooks/` and add a link in `AGENTS.md §7`.
- Changed playbook files: diff against the installed version; apply only non-customized sections.
- New scripts: copy to `skills/wiki-maintenance/scripts/`.
- AGENTS-template changes: review the diff and apply to `AGENTS.md` manually — the template is a starting point, not an overwrite target.

Log the upgrade as a `schema-update` entry: `## [DATE] schema-update | Skill upgrade to vX.Y`.
