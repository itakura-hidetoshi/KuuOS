#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime import kuuos_root_map_pre_adoption_review_v0_51 as review

VERSION = "kuuos_root_map_adoption_deferral_v0_52"
DEPENDS_ON = review.VERSION
READ_ONLY = True
METADATA_ONLY = True
ADOPTION_DEFERRED = True
CHANGE_PERFORMED = False

REQUIRED_DEFERRAL_ITEMS: tuple[str, ...] = (
    "pre_review_verified",
    "adoption_deferred",
    "change_not_performed",
    "separate_future_layer_required",
)


@dataclass(frozen=True)
class DeferralItem:
    item_id: str
    passed: bool
    note: str


DEFERRAL_ITEMS: tuple[DeferralItem, ...] = (
    DeferralItem(
        "pre_review_verified",
        review.verify_pre_adoption_review(),
        "v0.51 pre-adoption review verifies",
    ),
    DeferralItem(
        "adoption_deferred",
        ADOPTION_DEFERRED,
        "adoption is deferred by this layer",
    ),
    DeferralItem(
        "change_not_performed",
        not CHANGE_PERFORMED,
        "this layer records status only and performs no repository change",
    ),
    DeferralItem(
        "separate_future_layer_required",
        True,
        "any future action must use a separate branch and draft PR",
    ),
)


def deferral_item_ids() -> tuple[str, ...]:
    return tuple(item.item_id for item in DEFERRAL_ITEMS)


def failed_deferral_items() -> tuple[str, ...]:
    return tuple(item.item_id for item in DEFERRAL_ITEMS if not item.passed)


def deferral_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if not READ_ONLY:
        issues.append("not_read_only")
    if not METADATA_ONLY:
        issues.append("not_metadata_only")
    if not ADOPTION_DEFERRED:
        issues.append("adoption_not_deferred")
    if CHANGE_PERFORMED:
        issues.append("change_performed")
    if len(deferral_item_ids()) != len(set(deferral_item_ids())):
        issues.append("duplicate_deferral_item")
    missing = set(REQUIRED_DEFERRAL_ITEMS).difference(deferral_item_ids())
    if missing:
        issues.append("missing_deferral_item:" + ",".join(sorted(missing)))
    for item in DEFERRAL_ITEMS:
        if not item.note:
            issues.append("missing_note:" + item.item_id)
    for failed in failed_deferral_items():
        issues.append("failed_deferral_item:" + failed)
    return tuple(issues)


def verify_adoption_deferral() -> bool:
    return not deferral_issues()


def as_markdown() -> str:
    rows = ["| Deferral item | Passed | Note |", "|---|---|---|"]
    for item in DEFERRAL_ITEMS:
        rows.append(f"| {item.item_id} | {item.passed} | {item.note} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = deferral_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
