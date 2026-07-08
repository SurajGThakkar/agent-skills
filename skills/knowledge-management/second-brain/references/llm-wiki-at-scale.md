# LLM Wiki at Scale

A pattern for building personal knowledge bases using LLMs — hardened to stay fast, accurate, and low-maintenance as it grows.

> **Adapted and extended from Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).** The core idea is his; this version adds the operational layer for running it long-term: a lean always-on schema, a generated index, deterministic maintenance tooling, log rotation, and dashboards.

This is an idea file, it is designed to be copy pasted to your own LLM Agent (e.g. OpenAI Codex, Claude Code, OpenCode / Pi, or etc.). Its goal is to communicate the high level idea, but your agent will build out the specifics in collaboration with you.

> [!important] **Note to the Agent reading this:** When you build the user's schema, you must set an explicit **anti-pattern constraint** separating the operational layer from the content layer. You will be instructed to keep the schema *lean* to save **context load**, but you must not let that leanness bleed into your content extraction. Ensure your schema commands you to perform exhaustive **legwork** during ingest — a single rich source should spawn 10-15 pages. Optimizing for token efficiency during ingestion guarantees **premature completion** and strands knowledge.

## The core idea

Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation. Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time. Nothing is built up. NotebookLM, ChatGPT file uploads, and most RAG systems work this way.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources. When you add a new source, the LLM doesn't just index it for later retrieval. It reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting where new data contradicts old claims, strengthening or challenging the evolving synthesis. The knowledge is compiled once and then *kept current*, not re-derived on every query.

This is the key difference: **the wiki is a persistent, compounding artifact.** The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read. The wiki keeps getting richer with every source you add and every question you ask.

You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work — the summarizing, cross-referencing, filing, and bookkeeping that makes a knowledge base actually useful over time. In practice, I have the LLM agent open on one side and Obsidian open on the other. The LLM makes edits based on our conversation, and I browse the results in real time — following links, checking the graph view, reading the updated pages. Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.

This can apply to a lot of different contexts. A few examples:

- **Personal**: tracking your own goals, health, psychology, self-improvement — filing journal entries, articles, podcast notes, and building up a structured picture of yourself over time.
- **Research**: going deep on a topic over weeks or months — reading papers, articles, reports, and incrementally building a comprehensive wiki with an evolving thesis.
- **Reading a book**: filing each chapter as you go, building out pages for characters, themes, plot threads, and how they connect. By the end you have a rich companion wiki. Think of fan wikis like [Tolkien Gateway](https://tolkiengateway.net/wiki/Main_Page) — thousands of interlinked pages covering characters, places, events, languages, built by a community of volunteers over years. You could build something like that personally as you read, with the LLM doing all the cross-referencing and maintenance.
- **Business/team**: an internal wiki maintained by LLMs, fed by Slack threads, meeting transcripts, project documents, customer calls. Possibly with humans in the loop reviewing updates. The wiki stays current because the LLM does the maintenance that no one on the team wants to do.
- **Competitive analysis, due diligence, trip planning, course notes, hobby deep-dives** — anything where you're accumulating knowledge over time and want it organized rather than scattered.

## Architecture

There are three layers:

**Raw sources** — your curated collection of source documents. Articles, papers, images, data files. These are immutable — the LLM reads from them but never modifies them. This is your source of truth.

**The wiki** — a directory of LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons, an overview, a synthesis. The LLM owns this layer entirely. It creates pages, updates them when new sources arrive, maintains cross-references, and keeps everything consistent. You read it; the LLM writes it.

**The schema** — a document (e.g. CLAUDE.md for Claude Code or AGENTS.md for Codex) that tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or maintaining the wiki. This is the key configuration file — it's what makes the LLM a disciplined wiki maintainer rather than a generic chatbot. You and the LLM co-evolve this over time as you figure out what works for your domain.

One thing to watch as you co-evolve it: this file is *always-on context* — it gets loaded on every single interaction. It's tempting to keep appending rules, workflows, and format specs until it's hundreds of lines long, but a bloated schema burns your context budget and actually *degrades* the LLM's focus — there's more to attend to and more to quietly forget. The fix is **progressive disclosure**: keep the schema a lean core (the layers, the conventions, the operating rules, and a short index of workflows) and move the detailed step-by-step for each workflow — how exactly to ingest, how to lint — and each format spec into separate files the LLM loads *on demand* only when it's doing that task. The core just says "before you ingest, read the ingest playbook." The always-on cost stays small while the detail stays available, and it scales: you can add as many playbooks as you like without growing the part that's always in context.

## Operations

**Ingest.** You drop a new source into the raw collection and tell the LLM to process it. An example flow: the LLM reads the source, discusses key takeaways with you, writes a summary page in the wiki, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log. A single source might touch 10-15 wiki pages. Personally I prefer to ingest sources one at a time and stay involved — I read the summaries, check the updates, and guide the LLM on what to emphasize. But you could also batch-ingest many sources at once with less supervision. It's up to you to develop the workflow that fits your style and document it in the schema for future sessions.

**Query.** You ask questions against the wiki. The LLM searches for relevant pages, reads them, and synthesizes an answer with citations. Answers can take different forms depending on the question — a markdown page, a comparison table, a slide deck (Marp), a chart (matplotlib), a canvas. The important insight: **good answers can be filed back into the wiki as new pages.** A comparison you asked for, an analysis, a connection you discovered — these are valuable and shouldn't disappear into chat history. This way your explorations compound in the knowledge base just like ingested sources do.

**Lint.** Periodically, health-check the wiki. Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search. The LLM is good at suggesting new questions to investigate and new sources to look for. Run lint as a *closed loop* rather than a one-off scan — **scan → fix → verify → log**, repeating until the wiki passes a clean bar (e.g. zero broken links, no missing frontmatter) — and lean on a script for the mechanical checks (see CLI tools below) so the LLM spends its effort on the judgment calls. This keeps the wiki healthy as it grows.

## Indexing and logging

Two special files help the LLM (and you) navigate the wiki as it grows. They serve different purposes:

**index.md** is content-oriented. It's a catalog of everything in the wiki — each page listed with a link, a one-line summary, and optionally metadata like date or source count. Organized by category (entities, concepts, sources, etc.). The LLM updates it on every ingest. When answering a query, the LLM reads the index first to find relevant pages, then drills into them. This works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and avoids the need for embedding-based RAG infrastructure.

An upgrade that pays off fast: once you're past a handful of pages, **generate the index from the pages themselves instead of having the LLM hand-edit it.** If every page carries structured frontmatter (title, type, tags, a one-line summary), a tiny script can rebuild the whole index deterministically — correct counts, every page present, nothing stale. A hand-maintained index inevitably drifts (a page gets renamed, a summary goes out of date, one gets forgotten), and a drifted index sends the LLM to the wrong pages. Since the index is what the LLM routes through, keeping it accurate is the single biggest lever on query quality — and generating it removes the most tedious bit of bookkeeping entirely.

**log.md** is chronological. It's an append-only record of what happened and when — ingests, queries, lint passes. A useful tip: if each entry starts with a consistent prefix (e.g. `## [2026-04-02] ingest | Article Title`), the log becomes parseable with simple unix tools — `grep "^## \[" log.md | tail -5` gives you the last 5 entries. The log gives you a timeline of the wiki's evolution and helps the LLM understand what's been done recently. Because it only ever grows, **rotate it** once it gets long: keep the most recent window (say the last ~40 entries) in `log.md` and archive older ones to a dated file. The recent slice is all the LLM needs for context; the archive preserves the full history without bloating the file that gets read.

## Optional: CLI tools

As the wiki grows, a handful of small command-line scripts — things the LLM runs by shelling out — take the maintenance burden close to zero. Think of them as deterministic bookkeeping: the LLM is excellent at reading and judgment, but it shouldn't be spending tokens (or risking mistakes) on mechanical, countable work. Useful ones, in rough order of when you'll want them:

- **Index generator** — rebuilds the catalog from page frontmatter (see above). Usually the first script worth writing.
- **Linter** — scans for broken links, orphan pages, missing frontmatter fields, and tag drift; writes a report and exits non-zero if anything's broken, so "is the wiki healthy?" has a deterministic answer.
- **Log rotator** — trims `log.md` to a recent window and archives the rest.
- **Calibrators** — flag pages whose metadata violates your own rules (e.g. a "high confidence" page backed by only one source).

The pattern that makes this safe is **scripts propose, the LLM disposes.** The scripts just parse the markdown files directly — no running app, no database — and hand the LLM a clean worklist; the LLM then makes the calls that need judgment (which contradiction is real, which cross-link is meaningful) and applies them. Never blind-apply a script's output — that's how noise creeps into the wiki.

A **search engine** over the wiki is the other big one — at small scale the index file is enough, but past a few hundred pages you'll want real search. [qmd](https://github.com/tobi/qmd) is a good option: a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device. It has both a CLI (so the LLM can shell out to it) and an MCP server (so the LLM can use it as a native tool). You can also start simpler — the LLM can help you vibe-code a naive search script when the need arises.

## Tips and tricks

- **Obsidian Web Clipper** is a browser extension that converts web articles to markdown. Very useful for quickly getting sources into your raw collection.
- **Download images locally.** In Obsidian Settings → Files and links, set "Attachment folder path" to a fixed directory (e.g. `raw/assets/`). Then in Settings → Hotkeys, search for "Download" to find "Download attachments for current file" and bind it to a hotkey (e.g. Ctrl+Shift+D). After clipping an article, hit the hotkey and all images get downloaded to local disk. This is optional but useful — it lets the LLM view and reference images directly instead of relying on URLs that may break. Note that LLMs can't natively read markdown with inline images in one pass — the workaround is to have the LLM read the text first, then view some or all of the referenced images separately to gain additional context. It's a bit clunky but works well enough.
- **Obsidian's graph view** is the best way to see the shape of your wiki — what's connected to what, which pages are hubs, which are orphans.
- **Marp** is a markdown-based slide deck format. Obsidian has a plugin for it. Useful for generating presentations directly from wiki content.
- **Dataview / Bases** turn page frontmatter into live dashboards. If your LLM writes consistent YAML frontmatter (type, tags, dates, confidence), Dataview (a plugin) or Bases (Obsidian's newer built-in) can generate dynamic tables — projects by status, pages by confidence, anything untouched in 90+ days. The key property is that these are *derived, read-only views*: they're always current and cost zero maintenance because they read the frontmatter rather than being hand-written. Keep a dashboard for yourself to browse, and let the LLM keep the terse `index.md` for routing — human surface and agent surface, both fed by the same clean metadata.
- **Keep a controlled tag vocabulary.** Left unchecked, tags sprawl — `ai`, `artificial-intelligence`, `AI`, `ml` all meaning roughly the same thing — which makes the graph and every frontmatter-driven view noisy. Maintain a short list of approved tags (in the schema or its own file) and have the linter flag anything off-list or used only once. A small, consistent tag set is what makes dashboards, filtering, and the graph view actually useful.
- The wiki is just a git repo of markdown files. You get version history, branching, and collaboration for free.

## Keeping it healthy as it grows

Everything above describes the pattern; this is what keeps it working once the wiki has hundreds of pages and months of history behind it. Two ideas do most of the heavy lifting:

**Keep always-on context lean.** Anything the LLM loads on *every* interaction — the schema above all — is a tax on focus and budget. Push detail into files loaded on demand (progressive disclosure), generate derived artifacts like the index rather than carrying them by hand, and rotate append-only logs. The goal is that the cost of *being oriented* stays roughly flat even as the wiki gets large.

**Split deterministic work from judgment.** The mechanical parts of maintenance — counting, cataloging, link-checking, tag-checking, format validation — are exactly what scripts are good at and what the LLM is wastefully expensive (and occasionally unreliable) at. Hand those to small tools that *propose* worklists. Reserve the LLM for what only it can do: deciding what a source means, what contradicts what, which connection is real, how the synthesis should shift. The wiki stays *trustworthy* because the boring checks are deterministic, and it stays *smart* because the judgment stays with the model.

Add each lever as its pain shows up rather than all at once — usually the generated index first, a real search engine last. None of it changes the core loop; it just keeps that loop cheap at scale.

## Why this works

The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. Updating cross-references, keeping summaries current, noting when new data contradicts old claims, maintaining consistency across dozens of pages. Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass. The wiki stays maintained because the cost of maintenance is near zero.

The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else.

The idea is related in spirit to Vannevar Bush's Memex (1945) — a personal, curated knowledge store with associative trails between documents. Bush's vision was closer to this than to what the web became: private, actively curated, with the connections between documents as valuable as the documents themselves. The part he couldn't solve was who does the maintenance. The LLM handles that.

## Note

This document is intentionally abstract. It describes the idea, not a specific implementation. The exact directory structure, the schema conventions, the page formats, the tooling — all of that will depend on your domain, your preferences, and your LLM of choice. Everything mentioned above is optional and modular — pick what's useful, ignore what isn't. For example: your sources might be text-only, so you don't need image handling at all. Your wiki might be small enough that the index file is all you need, no search engine required. You might not care about slide decks and just want markdown pages. You might want a completely different set of output formats. The right way to use this is to share it with your LLM agent and work together to instantiate a version that fits your needs. The document's only job is to communicate the pattern. Your LLM can figure out the rest.