#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

VERSION = "kuuos_overview_index_v0_44"
DEPENDS_ON = "kuuos_docs_index_v0_43"
CURRENT_CHECK = "runtime/kuuos_current_check.py"


@dataclass(frozen=True)
class OverviewEntry:
    entry_id: str
    path: str
    role: str
    check: str


OVERVIEW_ENTRIES: tuple[OverviewEntry, ...] = (
    OverviewEntry("current-check", "runtime/kuuos_current_check.py", "entry point", "runtime.v124_checkpoint_reflog_runtime:run_v124"),
    OverviewEntry("sequence", "runtime/kuuos_current_root_sequence_v0_41.py", "ordered checks", "tests.test_kuuos_current_root_sequence_v0_41"),
    OverviewEntry("manifest-index", "runtime/kuuos_manifest_index_v0_42.py", "metadata list", "tests.test_kuuos_manifest_index_v0_42"),
    OverviewEntry("docs-index", "runtime/kuuos_docs_index_v0_43.py", "docs list", "tests.test_kuuos_docs_index_v0_43"),
    OverviewEntry("overview-index", "runtime/kuuos_overview_index_v0_44.py", "overview list", "tests.test_kuuos_overview_index_v0_44"),
)


def entry_ids() -> tuple[str, ...]:
    return tuple(entry.entry_id for entry in OVERVIEW_ENTRIES)


def entry_paths() -> tuple[str, ...]:
    return tuple(entry.path for entry in OVERVIEW_ENTRIES)


def overview_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if len(entry_ids()) != len(set(entry_ids())):
        issues.append("duplicate_entry_id")
    if len(entry_paths()) != len(set(entry_paths())):
        issues.append("duplicate_entry_path")
    for entry in OVERVIEW_ENTRIES:
        if not entry.path:
            issues.append("missing_path:" + entry.entry_id)
        if not entry.role:
            issues.append("missing_role:" + entry.entry_id)
        if not entry.check:
            issues.append("missing_check:" + entry.entry_id)
    required = {"current-check", "sequence", "manifest-index", "docs-index", "overview-index"}
    missing = required.difference(entry_ids())
    if missing:
        issues.append("missing_overview_entry:" + ",".join(sorted(missing)))
    return tuple(issues)


def verify_overview_index() -> bool:
    return not overview_issues()


def as_markdown() -> str:
    rows = ["| Entry | Path | Role | Check |", "|---|---|---|---|"]
    for entry in OVERVIEW_ENTRIES:
        rows.append(f"| {entry.entry_id} | `{entry.path}` | {entry.role} | `{entry.check}` |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = overview_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
