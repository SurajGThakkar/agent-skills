# AGENTS.md — Agent Skills Schema

> **Owner:** Suraj Thakkar | **Repository:** agent-skills

This repository houses a curated, modular collection of agent skills. The LLM maintains, enhances, and builds upon these skills to extend its own capabilities. 

This file is the operational contract for AI agents traversing or modifying this repository. **Be Bespoke, Succinct & Holistic.**

---

## 1. Structure

Skills are categorized under `skills/`:

- **`agent-ops/`** — Meta-skills for adapting and expanding agent capabilities.
- **`engineering/`** — Architectural alignment and engineering disciplines.
- **`knowledge-management/`** — Obsidian-native integrations and wiki maintenance.
- **`productivity/`** — Workflows for learning and personal development.
- **`assets/`** — Shared resources and global scripts.

## 2. Skill Conventions

- **Isolation:** Each skill resides in its own subfolder (e.g., `skills/knowledge-management/obsidian-cli/`).
- **The SKILL.md:** This is the execution entry point. It must contain YAML frontmatter (`name` and `description`).
- **Lean Core:** Keep `SKILL.md` under 500 lines. Offload complexity into `scripts/`, `examples/`, `resources/`, or `references/` subdirectories within the skill folder.
- **Bespoke & Succinct:** Instructions must be hyper-specific to the use case. Avoid generic platitudes.
- **Holistic Design:** Ensure a skill's inputs and outputs integrate cleanly with broader workflows (e.g., Obsidian Second Brain).

## 3. Registration

When creating or promoting a new skill, you must:
1. Add an entry in **`skills.sh.json`** under the appropriate category group.
2. Link the skill's `SKILL.md` in the top-level **`README.md`** alongside a one-line description.

*Note: Unregistered skills are considered orphaned and will not be loaded.*

## 4. Operating Rules

1. **Read before writing:** Always read a skill's `SKILL.md` and the `skills.sh.json` registry before making structural changes.
2. **Deterministic execution:** Automations and scripts do the heavy lifting; the LLM focuses on judgment, synthesis, and planning.
3. **Constraint Adherence:** Treat any negative constraint in a skill (e.g., "never edit this directly") as an absolute boundary. No lazy assumptions.
4. **Do no harm:** Never break existing skill integrations when refactoring. Ensure backward compatibility with existing vault workflows.

---

*Living document — keep it lean, keep it sharp.*
