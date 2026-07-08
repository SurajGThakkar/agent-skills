---
title: "Wiki Health Dashboard"
type: meta
created: {TODAY}
updated: {TODAY}
tags: [meta, dashboard]
confidence: high
---

# Wiki Health Dashboard

> Auto-updating views powered by [Obsidian Dataview](https://github.com/blacksmithgu/obsidian-dataview). Install the **Dataview** community plugin to activate these panels. If you use the built-in **Bases** feature instead, see the query hints below each panel.
>
> This file is generated once during vault setup and then updates itself automatically as your wiki grows. You never need to edit it.

---

## Untagged Notes
*Pages that slipped through without a controlled-vocabulary tag — address these before the next ingest.*

```dataview
TABLE file.ctime AS "Created", type AS "Type"
FROM "wiki"
WHERE (!tags OR length(tags) = 0) AND type != "meta"
SORT file.ctime DESC
```

---

## Stale Projects
*Active projects with no updates in 90+ days — worth a quick status check.*

```dataview
TABLE status AS "Status", updated AS "Last Updated"
FROM "wiki/projects"
WHERE date(today) - date(updated) > dur(90 days)
SORT updated ASC
```

---

## Low Confidence Pages
*Pages marked `low` or `speculative` — candidates for a targeted search or new source.*

```dataview
TABLE type AS "Type", confidence AS "Confidence", updated AS "Updated"
FROM "wiki"
WHERE (confidence = "low" OR confidence = "speculative") AND type != "meta"
SORT updated ASC
LIMIT 25
```

---

## Recently Ingested (Last 14 Days)
*What's been added recently — a quick snapshot of momentum.*

```dataview
TABLE type AS "Type", tags AS "Tags"
FROM "wiki"
WHERE date(created) >= date(today) - dur(14 days) AND type != "meta"
SORT file.ctime DESC
```

---

## Confidence Distribution
*How the vault's knowledge is maturing at a glance.*

```dataview
TABLE length(rows) AS "Count", rows.file.link AS "Pages"
FROM "wiki"
WHERE type != "meta"
GROUP BY confidence
SORT confidence ASC
```

---

## Orphaned Pages
*Pages that exist but aren't linked from anywhere — risk of becoming dead ends.*

```dataview
TABLE type AS "Type", updated AS "Updated"
FROM "wiki"
WHERE length(file.inlinks) = 0 AND type != "meta"
SORT updated ASC
LIMIT 20
```

---

*Dashboard generated on {TODAY}. Powered by the LLM Wiki at Scale pattern — [[index]] is the agent-facing catalog; this file is the human-facing health view.*
