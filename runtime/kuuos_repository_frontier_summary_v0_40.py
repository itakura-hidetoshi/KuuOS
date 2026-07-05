#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime.kuuos_repository_cleanup_proposals_v0_39 import verify_cleanup_proposals
from runtime.kuuos_repository_structure_map_v0_38 import verify_repository_structure_map

VERSION = "kuuos_repository_frontier_summary_v0_40"
DEPENDS_ON = "kuuos_repository_cleanup_proposals_v0_39"
SUMMARY_DOC = "docs/repository_frontier_summary_v0_40.md"
CURRENT_ROOT = "runtime/kuuos_current_check.py"


@dataclass(frozen=True)
class FrontierItem:
    name: str
    status: str
    root: str
    note: str


FRONTIER_ITEMS: tuple[FrontierItem, ...] = (
    FrontierItem(
        "closed-repository-mutation",
        "closed-at-v1.24",
        "runtime/kuuos_v124_check.py",
        "Closed line. No automatic successor authority is created.",
    ),
    FrontierItem(
        "lifecycle-completion",
        "complete-at-v0.36",
        "tests.test_kuuos_lifecycle_completion_v0_36",
        "Terminal lifecycle completion is kept separate from repository mutation.",
    ),
    FrontierItem(
        "repository-index",
        "integrated-at-v0.37",
        "tests.test_kuuos_repo_index_v0_37",
        "Machine-readable index for current roots and major lines.",
    ),
    FrontierItem(
        "repository-structure-map",
        "integrated-at-v0.38",
        "tests.test_kuuos_repository_structure_map_v0_38",
        "Directory zones and cleanup boundaries.",
    ),
    FrontierItem(
        "repository-cleanup-proposals",
        "integrated-at-v0.39",
        "tests.test_kuuos_repository_cleanup_proposals_v0_39",
        "Read-only proposal list. No file movement or deletion is authorized.",
    ),
    FrontierItem(
        "repository-frontier-summary",
        "frontier-at-v0.40",
        "tests.test_kuuos_repository_frontier_summary_v0_40",
        "Human-facing summary document linked to machine-readable checks.",
    ),
)


def item_names() -> tuple[str, ...]:
    return tuple(item.name for item in FRONTIER_ITEMS)


def item_roots() -> tuple[str, ...]:
    return tuple(item.root for item in FRONTIER_ITEMS)


def summary_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if len(item_names()) != len(set(item_names())):
        issues.append("duplicate_frontier_item")
    if not SUMMARY_DOC.startswith("docs/"):
        issues.append("summary_doc_not_in_docs")
    if not verify_repository_structure_map():
        issues.append("structure_map_invalid")
    if not verify_cleanup_proposals():
        issues.append("cleanup_proposals_invalid")
    required = {
        "closed-repository-mutation",
        "lifecycle-completion",
        "repository-index",
        "repository-structure-map",
        "repository-cleanup-proposals",
        "repository-frontier-summary",
    }
    missing = required.difference(item_names())
    if missing:
        issues.append("frontier_item_missing:" + ",".join(sorted(missing)))
    if any("move" in item.note.lower() or "delete" in item.note.lower() for item in FRONTIER_ITEMS if item.name == "repository-frontier-summary"):
        issues.append("summary_item_contains_mutation_claim")
    return tuple(issues)


def verify_frontier_summary() -> bool:
    return not summary_issues()


def as_markdown() -> str:
    rows = ["| Item | Status | Root |", "|---|---|---|"]
    for item in FRONTIER_ITEMS:
        rows.append(f"| {item.name} | {item.status} | `{item.root}` |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = summary_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
