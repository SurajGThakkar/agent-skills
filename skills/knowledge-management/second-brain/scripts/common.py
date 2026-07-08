"""Shared parsing + vault-scan helpers for the second-brain toolkit.

Reads markdown directly (no Obsidian required). Vault root is derived from this
file's location: skills/second-brain/scripts/common.py -> parents[3].
"""

import os
import re
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    raise SystemExit("PyYAML required: pip install pyyaml")

VAULT = Path(__file__).resolve().parents[3]
WIKI = VAULT / "wiki"
SKILLS = VAULT / "skills"

# --- VAULT CONFIGURATION ---
# Users should customize these to match their specific vault.
SKIP_DIRS = set()  # e.g., {"plinth-course"}
OWNED = set()  # e.g., {"suraj-thakkar", "my-project"}
OWNER_SLUG = "owner"  # e.g., "suraj-thakkar"
MERGE_MAP = {}  # e.g., {"projects": "project", "metric": "metrics"} -- used by BOTH lint.py's drift report and normalize_tags.py's fixer; edit only here.
# ---------------------------

CONTENT_TYPES = {
    "entity", "concept", "source", "project",
    "domain", "comparison", "synthesis", "query",
}
REQUIRED_FRONTMATTER = ["title", "type", "created", "updated", "sources", "tags", "confidence"]
VALID_CONFIDENCE = {"high", "medium", "low", "speculative"}
STANDARD_SECTIONS = ["Overview", "Key Points", "Connections", "Open Questions", "Sources"]
# Section structure is enforced only for these types.
SECTION_ENFORCED_TYPES = {"entity", "concept", "project", "domain"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def clean_slug(target: str) -> str:
    """Normalize a wikilink target to a comparable slug."""
    target = target.split("|")[0]  # drop display text
    target = target.split("#")[0]  # drop heading / block anchor
    target = target.replace("[[", "").replace("]]", "").strip()
    if target.lower().endswith(".md"):
        target = target[:-3]
    return target.strip().lower().replace(" ", "-")


META_LINE_RE = re.compile(r"^\*\*[^*]+:\*\*")  # e.g. "**Type:** ...", "**Author:** ..."


def first_summary_line(body: str) -> str:
    """The first real prose line after the H1 = the index summary.

    Skips headings, callouts, tables, images, and bold key:value metadata lines
    (so source pages that lead with '**Type:** ...' still yield a real summary).
    """
    m = H1_RE.search(body)
    start = m.end() if m else 0
    for line in body[start:].splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("|"):
            continue
        if s.startswith("!["):
            continue
        if META_LINE_RE.match(s):
            continue
        if s.startswith(("- ", "* ", "1. ")):
            return re.sub(r"^([-*]|\d+\.)\s+", "", s)
        return s
    return ""


def _strip_code(text: str) -> str:
    """Remove fenced and inline code so example wikilinks are not treated as real."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def parse(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fm, fm_error, body = {}, None, text
    m = FM_RE.match(text)
    if m:
        body = text[m.end():]
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except Exception as exc:  # noqa: BLE001
            fm_error = f"YAML parse error: {exc}"
    h1 = H1_RE.search(body)
    sections = {s for s in H2_RE.findall(body)}
    links = [clean_slug(t) for t in WIKILINK_RE.findall(_strip_code(text))]
    return {
        "frontmatter": fm,
        "fm_error": fm_error,
        "h1": h1.group(1).strip() if h1 else None,
        "summary": first_summary_line(body),
        "links": links,
        "sections": sections,
        "body": body,
        "raw": text,
        "chars": len(text),
    }


# Subtrees managed by other systems (not part of the knowledge-wiki schema).


def scan_wiki() -> dict:
    """Return slug -> {path, relpath, parsed} for every wiki/**/*.md page.

    Skips subtrees in SKIP_DIRS (externally managed workspaces).
    """
    pages = {}
    for root, dirs, files in os.walk(WIKI):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".md"):
                continue
            p = Path(root) / f
            slug = p.stem
            pages[slug] = {
                "path": p,
                "relpath": str(p.relative_to(VAULT)),
                "parsed": parse(p),
            }
    return pages


def has_section(sections, standard: str) -> bool:
    """A standard section counts as present if any H2 equals it or extends it
    (prefix), e.g. 'Open Questions & Risks' satisfies 'Open Questions'."""
    return any(s == standard or s.startswith(standard) for s in sections)


def page_type(info: dict) -> str:
    fm = info["parsed"]["frontmatter"]
    return (fm or {}).get("type", "") if isinstance(fm, dict) else ""


def sources_list(fm: dict) -> list:
    s = (fm or {}).get("sources", [])
    if not isinstance(s, list):
        s = [s] if s else []
    return s


def known_slugs(pages: dict) -> set:
    """All resolvable wikilink targets: every wiki page plus index and log."""
    return set(pages.keys()) | {"index", "log"}


def is_first_party(slug: str, fm: dict) -> bool:
    if slug in OWNED:
        return True
    for s in sources_list(fm):
        if OWNER_SLUG in str(s).lower():
            return True
    return False
