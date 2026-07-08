# Second Brain Skill

An advanced, bespoke skill for configuring your AI agent to act as a **Personal Knowledge Manager (PKM)**. 

The `second-brain` skill enables your agent to autonomously setup, maintain, and operate an interconnected, LLM-managed wiki vault. It offloads cognitive load by allowing the agent to continuously index your insights, decisions, and workflows into a structured markdown graph.

## Features

- **Setup Branch:** Initializes a new markdown vault with a clean, hierarchical structure ready for ingestion.
- **Maintain Branch:** Automatically audits the vault, creates missing links, repairs broken references, and deduplicates redundant notes.
- **Operate Branch:** Actively answers your questions by traversing the vault's graph and synthesizing information from multiple notes.

## Installation

You can install this skill globally or on a per-project basis using the `skills.sh` CLI:

```bash
npx skills add surajthakkar/agent-skills --skill second-brain
```

## Usage

Once installed, simply invoke the skill in your chat prompt:

1. **To Setup:** "@second-brain initialize a new vault in the `./my-vault` directory."
2. **To Maintain:** "@second-brain run a maintenance audit on `./my-vault` and fix broken links."
3. **To Operate:** "@second-brain based on my notes in `./my-vault`, what was the consensus on the new architecture design?"

*For full technical details on how the agent interprets this skill, see the [`SKILL.md`](./SKILL.md) file.*
