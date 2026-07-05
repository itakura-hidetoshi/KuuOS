#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime import kuuos_root_map_deferral_receipt_v0_53 as receipt

VERSION = "kuuos_root_map_deferral_closeout_v0_54"
DEPENDS_ON = receipt.VERSION
READ_ONLY = True
METADATA_ONLY = True
CLOSEOUT_ONLY = True
FOLLOWUP_OPENED = False

REQUIRED_CLOSEOUT_ITEMS: tuple[str, ...] = (
    "receipt_verified",
    "closeout_only",
    "followup_not_opened",
    "audit_ready",
)


@dataclass(frozen=True)
class CloseoutItem:
    item_id: str
    passed: bool
    note: str


CLOSEOUT_ITEMS: tuple[CloseoutItem, ...] = (
    CloseoutItem(
        "receipt_verified",
        receipt.verify_deferral_receipt(),
        "v0.53 deferral receipt verifies before closeout",
    ),
    CloseoutItem(
        "closeout_only",
        CLOSEOUT_ONLY,
        "this layer only closes the current deferral receipt segment",
    ),
    CloseoutItem(
        "followup_not_opened",
        not FOLLOWUP_OPENED,
        "no follow-up action is opened by this layer",
    ),
    CloseoutItem(
        "audit_ready",
        True,
        "the receipt segment is ready for later audit as a bounded record",
    ),
)


def closeout_item_ids() -> tuple[str, ...]:
    return tuple(item.item_id for item in CLOSEOUT_ITEMS)


def failed_closeout_items() -> tuple[str, ...]:
    return tuple(item.item_id for item in CLOSEOUT_ITEMS if not item.passed)


def closeout_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if not READ_ONLY:
        issues.append("not_read_only")
    if not METADATA_ONLY:
        issues.append("not_metadata_only")
    if not CLOSEOUT_ONLY:
        issues.append("not_closeout_only")
    if FOLLOWUP_OPENED:
        issues.append("followup_opened")
    if len(closeout_item_ids()) != len(set(closeout_item_ids())):
        issues.append("duplicate_closeout_item")
    missing = set(REQUIRED_CLOSEOUT_ITEMS).difference(closeout_item_ids())
    if missing:
        issues.append("missing_closeout_item:" + ",".join(sorted(missing)))
    for item in CLOSEOUT_ITEMS:
        if not item.note:
            issues.append("missing_note:" + item.item_id)
    for failed in failed_closeout_items():
        issues.append("failed_closeout_item:" + failed)
    return tuple(issues)


def verify_deferral_closeout() -> bool:
    return not closeout_issues()


def as_markdown() -> str:
    rows = ["| Closeout item | Passed | Note |", "|---|---|---|"]
    for item in CLOSEOUT_ITEMS:
        rows.append(f"| {item.item_id} | {item.passed} | {item.note} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = closeout_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
