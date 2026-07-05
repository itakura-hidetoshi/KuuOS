#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

VERSION = "kuuos_docs_index_v0_43"
DEPENDS_ON = "kuuos_manifest_index_v0_42"
CURRENT_ROOT = "runtime/kuuos_current_check.py"


@dataclass(frozen=True)
class DocsEntry:
    doc_id: str
    path: str
    role: str
    owner_line: str


DOCS_ENTRIES: tuple[DocsEntry, ...] = (
    DocsEntry(
        "repository-frontier-summary-v0-40",
        "docs/repository_frontier_summary_v0_40.md",
        "concise repository status frontier",
        "repository-self-organization",
    ),
    DocsEntry(
        "current-root-sequence-v0-41",
        "docs/current_root_sequence_v0_41.md",
        "current root run order summary",
        "repository-self-organization",
    ),
    DocsEntry(
        "manifest-index-v0-42",
        "docs/manifest_index_v0_42.md",
        "manifest metadata summary",
        "repository-self-organization",
    ),
    DocsEntry(
        "docs-index-v0-43",
        "docs/docs_index_v0_43.md",
        "documentation index summary",
        "repository-self-organization",
    ),
    DocsEntry(
        "overview-index-v0-44",
        "docs/overview_index_v0_44.md",
        "current organization overview summary",
        "repository-self-organization",
    ),
    DocsEntry(
        "ci-continuation-v0-45",
        "docs/ci_continuation_v0_45.md",
        "run-all-then-decide CI continuation summary",
        "repository-self-organization",
    ),
)


def doc_ids() -> tuple[str, ...]:
    return tuple(entry.doc_id for entry in DOCS_ENTRIES)


def doc_paths() -> tuple[str, ...]:
    return tuple(entry.path for entry in DOCS_ENTRIES)


def docs_index_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if len(doc_ids()) != len(set(doc_ids())):
        issues.append("duplicate_doc_id")
    if len(doc_paths()) != len(set(doc_paths())):
        issues.append("duplicate_doc_path")
    for entry in DOCS_ENTRIES:
        if not entry.path.startswith("docs/"):
            issues.append("doc_path_outside_docs:" + entry.doc_id)
        if not entry.path.endswith(".md"):
            issues.append("doc_path_not_markdown:" + entry.doc_id)
        if not entry.role:
            issues.append("missing_doc_role:" + entry.doc_id)
        if not entry.owner_line:
            issues.append("missing_owner_line:" + entry.doc_id)
    required = {
        "repository-frontier-summary-v0-40",
        "current-root-sequence-v0-41",
        "manifest-index-v0-42",
        "docs-index-v0-43",
        "overview-index-v0-44",
        "ci-continuation-v0-45",
    }
    missing = required.difference(doc_ids())
    if missing:
        issues.append("missing_doc_entry:" + ",".join(sorted(missing)))
    return tuple(issues)


def verify_docs_index() -> bool:
    return not docs_index_issues()


def as_markdown() -> str:
    rows = ["| Doc | Path | Role |", "|---|---|---|"]
    for entry in DOCS_ENTRIES:
        rows.append(f"| {entry.doc_id} | `{entry.path}` | {entry.role} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = docs_index_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
