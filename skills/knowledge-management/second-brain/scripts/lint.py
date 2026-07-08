#!/usr/bin/env python3
"""Wiki linter — deterministic health scan (no Obsidian required).

Outputs:
  - skills/wiki-maintenance/results.json   (structured, machine-readable)
  - wiki/meta/lint-reports/lint-report-YYYY-MM-DD.md  (human report; skipped
    with --summary-only)

Flags:
  --summary-only  Scan and write results.json as usual, but skip generating
                   the dated markdown report. For frequent checks (e.g. the
                   `status` playbook) where a full report would just add
                   near-duplicate files to wiki/meta/lint-reports/ every run.

Exit code 0 if no criticals, 1 otherwise (so the lint loop can gate).
Criticals never auto-fix; this script only reports. Fixers are separate.
"""

import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

from common import (
    CONTENT_TYPES, REQUIRED_FRONTMATTER, VALID_CONFIDENCE, STANDARD_SECTIONS,
    SECTION_ENFORCED_TYPES, DATE_RE, VAULT, SKILLS,
    scan_wiki, page_type, sources_list, known_slugs, has_section,
    MERGE_MAP, OWNED, is_first_party,
)

SUMMARY_ONLY = "--summary-only" in sys.argv
HEX_IN_BODY_RE = re.compile(r"(?<![\w`])#[0-9A-Fa-f]{6}\b")
# Embeds/links to these are assets, not wiki pages — never "broken".
ASSET_EXTS = (".base", ".canvas", ".png", ".jpg", ".jpeg", ".gif", ".webp",
              ".svg", ".pdf", ".excalidraw", ".mp4", ".csv")


def run():
    pages = scan_wiki()
    known = known_slugs(pages)
    criticals, warnings = [], []
    inbound = {slug: set() for slug in pages}
    link_graph = {}
    tag_counter = Counter()

    for slug, info in pages.items():
        rel = info["relpath"]
        # Append-only records intentionally quote broken slugs and old schemas; treat as inert.
        if "/lint-reports/" in rel or "/log-archive/" in rel or "/lint-report-" in rel:
            continue
        p = info["parsed"]
        fm = p["frontmatter"] if isinstance(p["frontmatter"], dict) else {}
        ptype = page_type(info)

        # --- frontmatter integrity (critical) ---
        if p["fm_error"]:
            criticals.append({"file": rel, "type": "yaml_error", "msg": p["fm_error"]})
        if not fm:
            criticals.append({"file": rel, "type": "missing_frontmatter", "msg": "No frontmatter"})
        else:
            for key in REQUIRED_FRONTMATTER:
                if key not in fm:
                    criticals.append({"file": rel, "type": "missing_field", "msg": f"Missing '{key}'"})
            conf = fm.get("confidence")
            if conf and conf not in VALID_CONFIDENCE:
                criticals.append({"file": rel, "type": "bad_confidence", "msg": f"Invalid confidence '{conf}'"})
            for dk in ("created", "updated"):
                if dk in fm and not DATE_RE.match(str(fm[dk])):
                    criticals.append({"file": rel, "type": "bad_date", "msg": f"{dk}='{fm[dk]}' not ISO 8601"})
            tags = fm.get("tags", [])
            if isinstance(tags, list):
                for t in tags:
                    ts = str(t)
                    if ts.startswith("#"):
                        criticals.append({"file": rel, "type": "hash_tag", "msg": f"Tag '{ts}' has '#' prefix"})
                    tag_counter[ts.lstrip("#")] += 1

        # --- hex codes leaking as tags in body (warning) ---
        for hx in HEX_IN_BODY_RE.findall(p["raw"]):
            warnings.append({"file": rel, "type": "hex_in_body", "msg": f"Unescaped hex '{hx}' indexes as a tag"})
            break

        # --- section compliance (warning) ---
        if ptype in SECTION_ENFORCED_TYPES:
            missing = [s for s in STANDARD_SECTIONS if not has_section(p["sections"], s)]
            if missing:
                warnings.append({"file": rel, "type": "missing_sections", "msg": ", ".join(missing)})

        # --- type-aware confidence calibration (warning) ---
        if ptype in {"entity", "concept"}:
            if fm.get("confidence") == "high" and len(sources_list(fm)) < 2 and not is_first_party(slug, fm):
                warnings.append({"file": rel, "type": "confidence_calibration",
                                 "msg": f"high with {len(sources_list(fm))} source(s), not first-party"})

        # --- link integrity + inbound graph ---
        resolved = []
        for tgt in p["links"]:
            resolved.append(tgt)
            if tgt not in known:
                if tgt.endswith(ASSET_EXTS):
                    continue  # ![[file.base]] / image embeds are assets, not pages
                if tgt.startswith("_") or tgt.endswith(".md") or "raw" in tgt or "/" in tgt:
                    criticals.append({"file": rel, "type": "raw_bracket_link",
                                      "msg": f"Use backticks not [[ ]] for: {tgt}"})
                else:
                    criticals.append({"file": rel, "type": "broken_link", "msg": f"[[{tgt}]]"})
            elif tgt in inbound and ptype not in {"meta"}:
                # only content/non-meta pages count as inbound sources
                inbound[tgt].add(slug)
        link_graph[slug] = resolved

    # --- orphans (content pages with no non-meta inbound) ---
    orphans = []
    for slug, info in pages.items():
        ptype = page_type(info)
        if ptype not in CONTENT_TYPES:
            continue
        srcs = {s for s in inbound.get(slug, set())
                if s != slug and page_type(pages[s]) != "meta"}
        if not srcs:
            orphans.append({"file": info["relpath"], "slug": slug, "type": ptype})

    # --- reciprocal-link gaps (conceptual graph only) ---
    # Reciprocity is expected within entity/concept/project/domain. Sources, queries,
    # syntheses and comparisons are commonly cited without citing back, so they are
    # excluded as reciprocal targets to keep the worklist meaningful (not noise).
    graph_types = {"entity", "concept", "project", "domain"}
    recip = []
    for slug, info in pages.items():
        if page_type(info) not in graph_types:
            continue
        for tgt in set(link_graph.get(slug, [])):
            if tgt in pages and page_type(pages[tgt]) in graph_types and tgt != slug:
                if slug not in set(link_graph.get(tgt, [])):
                    recip.append({"from": slug, "to": tgt})

    # --- tag census ---
    drift = [{"tag": t, "count": tag_counter[t], "canonical": MERGE_MAP[t]}
             for t in tag_counter if t in MERGE_MAP]
    single_use = sorted([t for t, c in tag_counter.items() if c < 2])

    content_count = sum(1 for i in pages.values() if page_type(i) in CONTENT_TYPES)
    source_count = sum(1 for i in pages.values() if page_type(i) == "source")

    results = {
        "generated": str(date.today()),
        "content_pages": content_count,
        "sources": source_count,
        "total_files_scanned": len(pages),
        "criticals": criticals,
        "warnings": warnings,
        "orphans": orphans,
        "reciprocal_gaps": recip,
        "tags": {"unique": len(tag_counter), "drift": drift, "single_use": single_use,
                 "counts": dict(tag_counter.most_common())},
    }

    out = SKILLS / "wiki-maintenance" / "results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    if not SUMMARY_ONLY:
        write_report(results)

    if SUMMARY_ONLY:
        print(f"Lint (summary): {len(criticals)} criticals, {len(warnings)} warnings.")
    else:
        print(f"Lint: {len(criticals)} criticals, {len(warnings)} warnings, "
              f"{len(orphans)} orphans, {len(recip)} reciprocal gaps. "
              f"({content_count} content pages, {source_count} sources)")
    return 1 if criticals else 0


def write_report(r):
    d = r["generated"]
    rep_dir = VAULT / "wiki" / "meta" / "lint-reports"
    rep_dir.mkdir(parents=True, exist_ok=True)
    crit_by = Counter(c["type"] for c in r["criticals"])
    warn_by = Counter(w["type"] for w in r["warnings"])
    lines = [
        "---", f'title: "Lint Report {d}"', "type: meta", f"created: {d}", f"updated: {d}",
        "sources: []", "tags: [meta, lint, health]", "confidence: high", "---", "",
        f"# Lint Report - {d}", "",
        f"> Content pages: {r['content_pages']} | Sources: {r['sources']} | "
        f"Files scanned: {r['total_files_scanned']}", "",
        f"**Criticals: {len(r['criticals'])}** | Warnings: {len(r['warnings'])} | "
        f"Orphans: {len(r['orphans'])} | Reciprocal gaps: {len(r['reciprocal_gaps'])}", "",
        "## Criticals (gate must reach 0)", "",
    ]
    if r["criticals"]:
        for t, n in crit_by.most_common():
            lines.append(f"- **{t}**: {n}")
        lines.append("")
        for c in r["criticals"][:60]:
            lines.append(f"  - `{c['file']}` — {c['type']}: {c['msg']}")
    else:
        lines.append("- None. Gate passed.")
    lines += ["", "## Warnings", ""]
    for t, n in warn_by.most_common():
        lines.append(f"- **{t}**: {n}")
    lines += ["", f"## Orphans ({len(r['orphans'])})", ""]
    for o in r["orphans"]:
        lines.append(f"- [[{o['slug']}]] ({o['type']})")
    lines += ["", "## Tag Health", "",
              f"- Unique tags: {r['tags']['unique']}",
              f"- Drift (merge to canonical): " +
              (", ".join(f"`{x['tag']}`->`{x['canonical']}`" for x in r['tags']['drift']) or "none"),
              f"- Single-use ({len(r['tags']['single_use'])}): " +
              (", ".join(f"`{t}`" for t in r['tags']['single_use']) or "none"),
              "", f"## Reciprocal-link worklist (first 40 of {len(r['reciprocal_gaps'])})",
              "", "_Scripts propose; the LLM decides which back-links are semantically real._", ""]
    for g in r["reciprocal_gaps"][:40]:
        lines.append(f"- [[{g['from']}]] -> [[{g['to']}]] (add reciprocal in [[{g['to']}]] Connections)")
    (rep_dir / f"lint-report-{d}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(run())
