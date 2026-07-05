#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

VERSION = "kuuos_root_map_status_v0_47"
DEPENDS_ON = "kuuos_root_map_ledger_v0_46"
CURRENT_CHECK = "runtime/kuuos_current_check.py"


@dataclass(frozen=True)
class StatusRow:
    row_id: str
    item: str
    check: str
    state: str


STATUS_ROWS: tuple[StatusRow, ...] = (
    StatusRow("root", "runtime/kuuos_current_check.py", "runtime.v124_checkpoint_reflog_runtime:run_v124", "present"),
    StatusRow("sequence", "runtime/kuuos_current_root_sequence_v0_41.py", "tests.test_kuuos_current_root_sequence_v0_41", "present"),
    StatusRow("map", "runtime/kuuos_root_map_v0_45.py", "tests.test_kuuos_root_map_v0_45", "present"),
    StatusRow("ledger", "runtime/kuuos_root_map_ledger_v0_46.py", "tests.test_kuuos_root_map_ledger_v0_46", "present"),
    StatusRow("status", "runtime/kuuos_root_map_status_v0_47.py", "tests.test_kuuos_root_map_status_v0_47", "present"),
)


def row_ids() -> tuple[str, ...]:
    return tuple(row.row_id for row in STATUS_ROWS)


def items() -> tuple[str, ...]:
    return tuple(row.item for row in STATUS_ROWS)


def checks() -> tuple[str, ...]:
    return tuple(row.check for row in STATUS_ROWS)


def status_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if len(row_ids()) != len(set(row_ids())):
        issues.append("duplicate_row_id")
    if len(items()) != len(set(items())):
        issues.append("duplicate_item")
    for row in STATUS_ROWS:
        if not row.item:
            issues.append("missing_item:" + row.row_id)
        if not row.check:
            issues.append("missing_check:" + row.row_id)
        if row.state != "present":
            issues.append("unexpected_state:" + row.row_id)
    required = {"root", "sequence", "map", "ledger", "status"}
    missing = required.difference(row_ids())
    if missing:
        issues.append("missing_status_row:" + ",".join(sorted(missing)))
    return tuple(issues)


def verify_root_map_status() -> bool:
    return not status_issues()


def as_markdown() -> str:
    rows = ["| Row | Item | Check | State |", "|---|---|---|---|"]
    for row in STATUS_ROWS:
        rows.append(f"| {row.row_id} | `{row.item}` | `{row.check}` | {row.state} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = status_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
