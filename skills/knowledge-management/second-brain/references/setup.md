# Setup Mode

Disclosed reference for the Setup branch of the `second-brain` skill. Read SKILL.md for branch routing and shared rules.

---

## Quick Start (5 minutes — expand into full setup later)

Not ready for the full setup, or want to start ingesting immediately? This gets you to a working vault in one step. You can grow into the full structure anytime by running `/second-brain setup` again — the Phase 0 discovery check will detect your existing vault and continue where you left off.

```bash
# 1. Create the minimal directory structure
mkdir -p raw wiki wiki/meta/playbooks skills/wiki-maintenance/scripts templates

# 2. Copy the schema template from this skill into your vault
#    (Claude will do this for you — just confirm the vault path)

# 3. Create an empty index and log
touch index.md log.md
```

After these three steps, Claude will:
- Write a minimal `AGENTS.md` (or `CLAUDE.md`) with your name and vault name
- Copy the maintenance scripts into `skills/wiki-maintenance/scripts/`
- Run `ingest [your first source]` to get the vault started immediately

The full interview, tag taxonomy, project pages, and Obsidian orientation happen in the full setup when you're ready. Nothing is lost by starting small.

---

## Phase 0: Silent Discovery

Before creating files or asking questions, silently discover what the vault already knows to avoid redundant questions or destructive overwrites:
1. Verify the current working directory. Check if any of the target directories already exist.
2. **Look for any existing context the user has provided.** Common locations: `CLAUDE.md` or `AGENTS.md` at vault root, `Context/` directory, any file the user explicitly mentioned. Extract `{OWNER_NAME}` and `{VAULT_NAME}` from whatever exists. If nothing is found, note that you'll gather them in the interview — do not error.
3. **If target directories already exist:**
   - If `AGENTS.md` exists → read it. This is a **partial bootstrap** or a **re-run**.
     - Ask the user: "I see an existing vault. Do you want to (a) continue setup where it left off, or (b) start fresh? Starting fresh will overwrite schema and meta files but will never touch your `wiki/` pages or `raw/` sources."
   - If only scaffold directories exist but no `AGENTS.md` → safe to continue; treat as fresh.
   - Never overwrite files in `raw/` or `wiki/` without explicit user confirmation.

## Phase A: Scaffold

Create these directories in the target path (the user's working directory unless they specify otherwise):

```
mkdir -p raw/{articles,papers,youtube,repos,books,courses,podcasts,threads,transcripts,projects,research,personal,assets}
mkdir -p wiki/{entities,concepts,projects,domains,comparisons,syntheses,queries,sources}
mkdir -p wiki/meta/{playbooks,formats,lint-reports,log-archive,dashboards}
mkdir -p skills/wiki-maintenance/scripts
mkdir -p templates
```

## Phase B: Onboarding interview

The interview populates the vault's initial context so it's personalized from day one. To make this easy for the user, explicitly invite varied inputs: Whisper dictation transcripts, pasted documents, or URLs.

Ask questions across **4 categories**. Accept any format: typed responses, pasted transcripts, links to online profiles, or "skip" to move on. The goal is a brain dump, not a quiz. **Batch all four categories into a single message** — don't ask them one at a time across four turns. If the environment supports structured input tools, use them for faster collection.

**CRITICAL RULE: Every output must be *bespoke*.** Templates are scaffolds to guide structure, not outputs. If a section lacks supporting data after the brain dump, omit the section entirely rather than leaving `[TBD]` placeholders. The final markdown must contain only real, provided data — no generic filler.

**Category 1 — You**
- Name, location, role/title, industry
- A one-sentence personal mission or what drives you
- How you'd want someone to introduce you in a room of people you respect
- 5 attributes that describe you (one or two words each)
- Are you a developer or do you regularly work with code and GitHub repositories? (yes/no — enables the code-tracking workflow)

**Category 2 — What you're building**
- Top 2-3 active projects (name, one-line purpose, status)
- What domain or field you're deepening expertise in
- Tools and platforms you use daily

**Category 3 — What you study**
- 3-5 topics you read about, watch, or research the most
- Podcasts, newsletters, YouTube channels, or authors you follow
- Any books or courses you're currently working through

**Category 4 — How this vault should work for you**
- What kinds of sources will you primarily ingest? (articles, papers, repos, transcripts, etc.)
- Do you prefer the LLM to be proactive (suggesting connections, related questions) or conservative (only doing what's asked)?
- Any topics, values, or priorities the LLM should always keep in mind when analyzing sources?

**After the interview:** if the user confirmed they are a developer in Category 1, note this in `AGENTS.md` and inform them that GitHub repository ingest is enabled via the `repo-ingest` playbook. Non-developers need never know this workflow exists — the repo playbook is opt-in, and its directory (`raw/repos/`) is inert for non-developers even though the scaffold includes it.

**Completion:** All 4 categories addressed (answered or explicitly skipped). At minimum, owner name and vault name captured.

## Phase C: Inject schemas and scripts

Read the templates from this skill's `references/` directory and write them to the target vault. Before writing, make every template *bespoke* — replace `{OWNER}`, `{OWNER_NAME}`, `{OWNER_SLUG}`, `{VAULT_NAME}`, `{TODAY}`, and any remaining `{...}` placeholders with the user's actual details gathered in Phase B. Do a final pass with `grep -r '{' <vault_path>` to catch any stragglers before handing off to the user.

| Source | Destination in new vault |
|---|---|
| `references/AGENTS-template.md` | `AGENTS.md` (vault root) |
| `references/playbooks/*.md` | `wiki/meta/playbooks/` |
| `references/formats/*.md` | `wiki/meta/formats/` |
| `templates/*.md` | `templates/` (vault root, includes `wiki-health-dashboard.md`) |

Copy the maintenance scripts from this skill's `scripts/` directory to `skills/wiki-maintenance/scripts/` in the new vault. These are the deterministic tools the vault will use for ongoing health checks. Note that `repo-capture.sh` is a shell script — make it executable after copying: `chmod +x skills/wiki-maintenance/scripts/repo-capture.sh`.

## Phase D: Build initial pages

Using the interview answers:

1. **Create `wiki/entities/{user-name}.md`** — the user's profile page. Use the `entity` template structure (frontmatter with title, type, created, updated, sources, tags, confidence). Fill in real data from the interview — never leave bracketed placeholders.

2. **Create project pages** — for each active project mentioned, create `wiki/projects/{project-name}.md` with a brief overview and status.

3. **Customize `wiki/meta/formats/tag-taxonomy.md`** — seed the controlled vocabulary with tags derived from the user's domains, interests, and project themes. Start lean (15-25 tags across Nature, Domain, and Theme facets). The taxonomy grows as sources are ingested.

4. **Update `AGENTS.md`** — fill in the owner name, vault name, and profile wikilink in the personalized copy.

5. **Create `index.md`** — run `python3 skills/wiki-maintenance/scripts/build_index.py` to generate the initial catalog.

6. **Create `log.md`** — write the first entry: vault bootstrapped, initial pages created.

7. **Generate health dashboard** — copy `templates/wiki-health-dashboard.md` to `wiki/meta/dashboards/wiki-health-dashboard.md`, replacing the `{TODAY}` placeholder with today's date. This gives the user pre-built Obsidian Dataview views (untagged notes, stale projects, low-confidence pages, recent ingests) that auto-update as the vault grows — no configuration required beyond installing the Dataview plugin.

**Completion:** Profile page created. At least one project page per active project mentioned. Tag taxonomy seeded. Index generated. Log initialized. Zero `{...}` placeholders remaining.

## Phase E: Confirm and orient

1. **Maintenance is built-in — just ask.** No terminal commands or cron jobs needed. The agent runs all maintenance scripts directly:
   - Type `lint` or "check my wiki health" → agent scans, proposes fixes, and walks you through each one conversationally
   - Type `status` → agent generates a vault snapshot
   - Type `suggest` → agent surfaces new connections and sources you're missing

2. Tell the user:
   - What was created (which pages, how many tags, the directory structure)
   - Recommend opening the folder in Obsidian
   - **Dashboard:** open `wiki/meta/dashboards/wiki-health-dashboard.md` in Obsidian with the **Dataview** plugin (or the built-in **Bases**) enabled
   - **Anti-Rot Tips:** Recommend the Obsidian Web Clipper extension for capturing raw sources. Recommend binding a hotkey to "Download attachments for current file" and setting a fixed local asset folder to prevent images from breaking.
   - Explain the core commands: `ingest [source]`, `query [question]`, `lint`, `status`, `suggest`, `migrate`
   - **Schema file naming:** The vault can use `AGENTS.md` (default, portable) or `CLAUDE.md` (Claude Code). Choose at setup time; be consistent.
   - Clarify the handoff: day-to-day ingest and query run through the vault's own schema playbooks, not this skill.
   - Suggest a natural first action based on what they told you (e.g., "You mentioned you're reading [book] — run `ingest [book chapter]` to get started.")

**Completion:** User has been told what was created, recommended Obsidian, shown core commands (`ingest`, `query`, `lint`, `status`, `suggest`, `migrate`), and given a suggested first action based on their interview answers.
