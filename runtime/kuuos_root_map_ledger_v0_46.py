#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

VERSION = "kuuos_root_map_ledger_v0_46"
DEPENDS_ON = "kuuos_root_map_v0_45"
CURRENT_CHECK = "runtime/kuuos_current_check.py"


@dataclass(frozen=True)
class LedgerRow:
    row_id: str
    source: str
    check: str
    status: str


LEDGER_ROWS: tuple[LedgerRow, ...] = (
    LedgerRow("current-check", "runtime/kuuos_current_check.py", "runtime.v124_checkpoint_reflog_runtime:run_v124", "checked"),
    LedgerRow("root-sequence", "runtime/kuuos_current_root_sequence_v0_41.py", "tests.test_kuuos_current_root_sequence_v0_41", "checked"),
    LedgerRow("root-map", "runtime/kuuos_root_map_v0_45.py", "tests.test_kuuos_root_map_v0_45", "checked"),
    LedgerRow("root-map-ledger", "runtime/kuuos_root_map_ledger_v0_46.py", "tests.test_kuuos_root_map_ledger_v0_46", "checked"),
)


def row_ids() -> tuple[str, ...]:
    return tuple(row.row_id for row in LEDGER_ROWS)


def row_sources() -> tuple[str, ...]:
    return tuple(row.source for row in LEDGER_ROWS)


def row_checks() -> tuple[str, ...]:
    return tuple(row.check for row in LEDGER_ROWS)


def ledger_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if len(row_ids()) != len(set(row_ids())):
        issues.append("duplicate_row_id")
    if len(row_sources()) != len(set(row_sources())):
        issues.append("duplicate_source")
    for row in LEDGER_ROWS:
        if not row.source:
            issues.append("missing_source:" + row.row_id)
        if not row.check:
            issues.append("missing_check:" + row.row_id)
        if row.status != "checked":
            issues.append("unexpected_status:" + row.row_id)
    required = {"current-check", "root-sequence", "root-map", "root-map-ledger"}
    missing = required.difference(row_ids())
    if missing:
        issues.append("missing_ledger_row:" + ",".join(sorted(missing)))
    return tuple(issues)


def verify_root_map_ledger() -> bool:
    return not ledger_issues()


def as_markdown() -> str:
    rows = ["| Row | Source | Check | Status |", "|---|---|---|---|"]
    for row in LEDGER_ROWS:
        rows.append(f"| {row.row_id} | `{row.source}` | `{row.check}` | {row.status} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = ledger_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
