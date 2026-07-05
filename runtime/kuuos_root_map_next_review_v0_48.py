#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime import kuuos_root_map_status_v0_47 as status

VERSION = "kuuos_root_map_next_review_v0_48"
DEPENDS_ON = status.VERSION
READ_ONLY = True
METADATA_ONLY = True

REQUIRED_BOUNDARIES: tuple[str, ...] = (
    "no_mutation_authority",
    "no_file_movement",
    "no_deletion",
    "no_execution_authority",
    "no_lifecycle_authorization_change",
)


@dataclass(frozen=True)
class NextReviewItem:
    item_id: str
    source_row: str
    current_state: str
    next_step: str
    boundaries: tuple[str, ...]


NEXT_REVIEW_ITEMS: tuple[NextReviewItem, ...] = (
    NextReviewItem(
        "root-observation-continuation",
        "root",
        "present",
        "keep_current_root_observable_before_any_mutation",
        REQUIRED_BOUNDARIES,
    ),
    NextReviewItem(
        "map-stability-continuation",
        "map",
        "present",
        "keep_directory_zone_map_stable_before_cleanup",
        REQUIRED_BOUNDARIES,
    ),
    NextReviewItem(
        "ledger-binding-continuation",
        "ledger",
        "present",
        "preserve_existing_root_map_ledger_bindings",
        REQUIRED_BOUNDARIES,
    ),
    NextReviewItem(
        "status-to-next-review",
        "status",
        "present",
        "derive_next_read_only_metadata_candidate",
        REQUIRED_BOUNDARIES,
    ),
)


def review_ids() -> tuple[str, ...]:
    return tuple(item.item_id for item in NEXT_REVIEW_ITEMS)


def source_rows() -> tuple[str, ...]:
    return tuple(item.source_row for item in NEXT_REVIEW_ITEMS)


def next_steps() -> tuple[str, ...]:
    return tuple(item.next_step for item in NEXT_REVIEW_ITEMS)


def all_boundaries() -> tuple[str, ...]:
    values: list[str] = []
    for item in NEXT_REVIEW_ITEMS:
        values.extend(item.boundaries)
    return tuple(dict.fromkeys(values))


def next_review_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if not READ_ONLY:
        issues.append("not_read_only")
    if not METADATA_ONLY:
        issues.append("not_metadata_only")
    if not status.verify_root_map_status():
        issues.append("upstream_status_invalid")
    if len(review_ids()) != len(set(review_ids())):
        issues.append("duplicate_review_id")
    if len(next_steps()) != len(set(next_steps())):
        issues.append("duplicate_next_step")
    known_rows = set(status.row_ids())
    for item in NEXT_REVIEW_ITEMS:
        if item.source_row not in known_rows:
            issues.append("unknown_source_row:" + item.item_id)
        if item.current_state != "present":
            issues.append("unexpected_current_state:" + item.item_id)
        if not item.next_step:
            issues.append("missing_next_step:" + item.item_id)
        missing_boundaries = set(REQUIRED_BOUNDARIES).difference(item.boundaries)
        if missing_boundaries:
            issues.append(
                "missing_boundary:"
                + item.item_id
                + ":"
                + ",".join(sorted(missing_boundaries))
            )
    return tuple(issues)


def verify_next_review() -> bool:
    return not next_review_issues()


def as_markdown() -> str:
    rows = [
        "| Review | Source row | Current state | Next step | Boundaries |",
        "|---|---|---|---|---|",
    ]
    for item in NEXT_REVIEW_ITEMS:
        rows.append(
            f"| {item.item_id} | {item.source_row} | {item.current_state} | "
            f"`{item.next_step}` | {', '.join(item.boundaries)} |"
        )
    return "\n".join(rows)


if __name__ == "__main__":
    problems = next_review_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
