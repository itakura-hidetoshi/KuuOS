#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime import kuuos_root_map_adoption_deferral_v0_52 as deferral

VERSION = "kuuos_root_map_deferral_receipt_v0_53"
DEPENDS_ON = deferral.VERSION
READ_ONLY = True
METADATA_ONLY = True
RECEIPT_ONLY = True
REPOSITORY_CHANGE_RECORDED = False

REQUIRED_RECEIPT_ITEMS: tuple[str, ...] = (
    "deferral_verified",
    "receipt_only",
    "repository_change_not_recorded",
    "future_layer_required",
)


@dataclass(frozen=True)
class DeferralReceiptItem:
    item_id: str
    passed: bool
    note: str


RECEIPT_ITEMS: tuple[DeferralReceiptItem, ...] = (
    DeferralReceiptItem(
        "deferral_verified",
        deferral.verify_adoption_deferral(),
        "v0.52 deferral verifies before this receipt is recorded",
    ),
    DeferralReceiptItem(
        "receipt_only",
        RECEIPT_ONLY,
        "this layer is a receipt for the existing deferral state",
    ),
    DeferralReceiptItem(
        "repository_change_not_recorded",
        not REPOSITORY_CHANGE_RECORDED,
        "the receipt records no repository change",
    ),
    DeferralReceiptItem(
        "future_layer_required",
        "separate_future_layer_required" in deferral.deferral_item_ids(),
        "future action remains outside this receipt layer",
    ),
)


def receipt_item_ids() -> tuple[str, ...]:
    return tuple(item.item_id for item in RECEIPT_ITEMS)


def failed_receipt_items() -> tuple[str, ...]:
    return tuple(item.item_id for item in RECEIPT_ITEMS if not item.passed)


def receipt_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if not READ_ONLY:
        issues.append("not_read_only")
    if not METADATA_ONLY:
        issues.append("not_metadata_only")
    if not RECEIPT_ONLY:
        issues.append("not_receipt_only")
    if REPOSITORY_CHANGE_RECORDED:
        issues.append("repository_change_recorded")
    if len(receipt_item_ids()) != len(set(receipt_item_ids())):
        issues.append("duplicate_receipt_item")
    missing = set(REQUIRED_RECEIPT_ITEMS).difference(receipt_item_ids())
    if missing:
        issues.append("missing_receipt_item:" + ",".join(sorted(missing)))
    for item in RECEIPT_ITEMS:
        if not item.note:
            issues.append("missing_note:" + item.item_id)
    for failed in failed_receipt_items():
        issues.append("failed_receipt_item:" + failed)
    return tuple(issues)


def verify_deferral_receipt() -> bool:
    return not receipt_issues()


def as_markdown() -> str:
    rows = ["| Receipt item | Passed | Note |", "|---|---|---|"]
    for item in RECEIPT_ITEMS:
        rows.append(f"| {item.item_id} | {item.passed} | {item.note} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = receipt_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
