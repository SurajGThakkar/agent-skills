---
title: "Format: Index"
type: meta
created: 2026-06-22
updated: 2026-06-22
sources: []
tags: [meta, format, schema]
confidence: high
---

# Format: Index

> `index.md` is the content catalog and the agent's query-routing layer. It is **regenerated deterministically** by `skills/wiki-maintenance/scripts/build_index.py` — do not hand-edit its tables.

## How it is built

The script scans every page's frontmatter plus the one-line summary directly under the `# H1`. The LLM still authors that summary on each page; the script only assembles the catalog from it. This keeps a single source of truth and kills count/format drift.

- `meta` pages (playbooks, formats, lint reports, dashboards) are excluded from the catalog and from the page count.
- `Total pages` counts content pages only (entities, concepts, sources, projects, domains, comparisons, syntheses, queries).

## Structure

```markdown
# Wiki Index

> Last updated: YYYY-MM-DD | Total pages: N | Total sources: N

## Sources
| Page | Summary | Date | Source Type |

## Entities
| Page | Summary | Sources | Confidence |

## Concepts
| Page | Summary | Sources | Confidence |

## Projects
| Page | Summary | Status | Sources |

## Domains
| Page | Summary | Sources | Confidence |

## Comparisons
| Page | Summary | Date |

## Syntheses
| Page | Summary | Date | Sources |

## Queries
| Page | Summary | Date |

## Skills
| Skill | Summary | Status |
```

## Column rules

- **Sources** column = integer count derived from the page's `sources` frontmatter length (deterministic, no mixed formats). Syntheses may list their sources explicitly.
- **Status** (projects) = the page's `status` frontmatter.
- **Date** = `updated` (fallback `created`).
- **Source Type** = a human label per source (YouTube, Repository, Deep Research, Project, Personal, Template, etc.).
- **Skills** = owned packs under `skills/` (auto-listed from each `SKILL.md`). `.agents/skills/` and `skills-cursor/` are externally managed and not cataloged here.
