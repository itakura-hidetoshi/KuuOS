#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime import kuuos_root_map_deferral_closeout_v0_54 as closeout

VERSION = "kuuos_root_map_closeout_observation_v0_55"
DEPENDS_ON = closeout.VERSION
READ_ONLY = True
METADATA_ONLY = True
OBSERVATION_ONLY = True
FOLLOWUP_CREATED = False

REQUIRED_OBSERVATION_ITEMS: tuple[str, ...] = (
    "closeout_verified",
    "observation_only",
    "followup_not_created",
    "stable_closeout_record",
)


@dataclass(frozen=True)
class CloseoutObservationItem:
    item_id: str
    passed: bool
    note: str


OBSERVATION_ITEMS: tuple[CloseoutObservationItem, ...] = (
    CloseoutObservationItem(
        "closeout_verified",
        closeout.verify_deferral_closeout(),
        "v0.54 closeout verifies before observation",
    ),
    CloseoutObservationItem(
        "observation_only",
        OBSERVATION_ONLY,
        "this layer observes the closed segment only",
    ),
    CloseoutObservationItem(
        "followup_not_created",
        not FOLLOWUP_CREATED,
        "this layer creates no follow-up action",
    ),
    CloseoutObservationItem(
        "stable_closeout_record",
        True,
        "the closeout record remains stable for later audit",
    ),
)


def observation_item_ids() -> tuple[str, ...]:
    return tuple(item.item_id for item in OBSERVATION_ITEMS)


def failed_observation_items() -> tuple[str, ...]:
    return tuple(item.item_id for item in OBSERVATION_ITEMS if not item.passed)


def observation_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if not READ_ONLY:
        issues.append("not_read_only")
    if not METADATA_ONLY:
        issues.append("not_metadata_only")
    if not OBSERVATION_ONLY:
        issues.append("not_observation_only")
    if FOLLOWUP_CREATED:
        issues.append("followup_created")
    if len(observation_item_ids()) != len(set(observation_item_ids())):
        issues.append("duplicate_observation_item")
    missing = set(REQUIRED_OBSERVATION_ITEMS).difference(observation_item_ids())
    if missing:
        issues.append("missing_observation_item:" + ",".join(sorted(missing)))
    for item in OBSERVATION_ITEMS:
        if not item.note:
            issues.append("missing_note:" + item.item_id)
    for failed in failed_observation_items():
        issues.append("failed_observation_item:" + failed)
    return tuple(issues)


def verify_closeout_observation() -> bool:
    return not observation_issues()


def as_markdown() -> str:
    rows = ["| Observation item | Passed | Note |", "|---|---|---|"]
    for item in OBSERVATION_ITEMS:
        rows.append(f"| {item.item_id} | {item.passed} | {item.note} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = observation_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
