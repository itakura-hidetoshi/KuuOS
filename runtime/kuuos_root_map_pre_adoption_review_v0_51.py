#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime import kuuos_root_map_adoption_readiness_v0_50 as readiness

VERSION = "kuuos_root_map_pre_adoption_review_v0_51"
DEPENDS_ON = readiness.VERSION
READ_ONLY = True
METADATA_ONLY = True
ADOPTION_AUTHORIZED = False

REQUIRED_REVIEW_ITEMS: tuple[str, ...] = (
    "confirm_readiness_verified",
    "confirm_no_adoption_performed",
    "confirm_future_governance_required",
    "confirm_mutation_authority_absent",
)


@dataclass(frozen=True)
class PreAdoptionReviewItem:
    item_id: str
    passed: bool
    note: str


REVIEW_ITEMS: tuple[PreAdoptionReviewItem, ...] = (
    PreAdoptionReviewItem(
        "confirm_readiness_verified",
        readiness.verify_adoption_readiness(),
        "v0.50 readiness verifies before any adoption stage",
    ),
    PreAdoptionReviewItem(
        "confirm_no_adoption_performed",
        not readiness.ADOPTION_PERFORMED,
        "v0.50 explicitly records that adoption has not been performed",
    ),
    PreAdoptionReviewItem(
        "confirm_future_governance_required",
        "future_stage_required" in readiness.check_ids(),
        "future adoption must be introduced by a later governance layer",
    ),
    PreAdoptionReviewItem(
        "confirm_mutation_authority_absent",
        "mutation_authority_absent" in readiness.check_ids(),
        "no repository mutation authority is present in readiness",
    ),
)


def review_item_ids() -> tuple[str, ...]:
    return tuple(item.item_id for item in REVIEW_ITEMS)


def passed_review_items() -> tuple[str, ...]:
    return tuple(item.item_id for item in REVIEW_ITEMS if item.passed)


def failed_review_items() -> tuple[str, ...]:
    return tuple(item.item_id for item in REVIEW_ITEMS if not item.passed)


def pre_adoption_review_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if not READ_ONLY:
        issues.append("not_read_only")
    if not METADATA_ONLY:
        issues.append("not_metadata_only")
    if ADOPTION_AUTHORIZED:
        issues.append("adoption_authorized")
    if len(review_item_ids()) != len(set(review_item_ids())):
        issues.append("duplicate_review_item_id")
    missing = set(REQUIRED_REVIEW_ITEMS).difference(review_item_ids())
    if missing:
        issues.append("missing_review_item:" + ",".join(sorted(missing)))
    for item in REVIEW_ITEMS:
        if not item.note:
            issues.append("missing_note:" + item.item_id)
    for failed in failed_review_items():
        issues.append("failed_review_item:" + failed)
    return tuple(issues)


def verify_pre_adoption_review() -> bool:
    return not pre_adoption_review_issues()


def as_markdown() -> str:
    rows = ["| Review item | Passed | Note |", "|---|---|---|"]
    for item in REVIEW_ITEMS:
        rows.append(f"| {item.item_id} | {item.passed} | {item.note} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = pre_adoption_review_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
