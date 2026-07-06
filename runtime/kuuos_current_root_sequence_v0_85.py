#!/usr/bin/env python3
from __future__ import annotations

from runtime import kuuos_current_root_sequence_v0_84 as previous
from runtime.kuuos_current_root_sequence_v0_41 import CurrentRootStep

VERSION = "kuuos_current_root_sequence_v0_85"
DEPENDS_ON = previous.VERSION
CURRENT_ROOT = "runtime/kuuos_current_check.py"
REVIEW_PACKET_FRONTIER = "kuuos_self_organization_review_packet_v0_85"

CURRENT_ROOT_STEPS: tuple[CurrentRootStep, ...] = previous.CURRENT_ROOT_STEPS + (
    CurrentRootStep(
        "review-packet-v0-85",
        "unittest",
        "tests.test_kuuos_self_organization_review_packet_v0_85",
        True,
        "Review packet is verified.",
    ),
    CurrentRootStep(
        "current-root-sequence-v0-85",
        "unittest",
        "tests.test_kuuos_current_root_sequence_v0_85",
        True,
        "Current root sequence v0.85 is verified.",
    ),
)


def step_ids() -> tuple[str, ...]:
    return tuple(step.step_id for step in CURRENT_ROOT_STEPS)


def step_targets() -> tuple[str, ...]:
    return tuple(step.target for step in CURRENT_ROOT_STEPS)


def unittest_targets() -> tuple[str, ...]:
    return tuple(step.target for step in CURRENT_ROOT_STEPS if step.runner == "unittest")


def sequence_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if not previous.verify_current_root_sequence():
        issues.append("previous_current_root_sequence")
    if len(step_ids()) != len(set(step_ids())):
        issues.append("duplicate_step_id")
    if len(step_targets()) != len(set(step_targets())):
        issues.append("duplicate_step_target")
    required = set(previous.unittest_targets()).union(
        {
            "tests.test_kuuos_self_organization_review_packet_v0_85",
            "tests.test_kuuos_current_root_sequence_v0_85",
        }
    )
    missing = required.difference(unittest_targets())
    if missing:
        issues.append("missing_unittest_target:" + ",".join(sorted(missing)))
    if REVIEW_PACKET_FRONTIER != "kuuos_self_organization_review_packet_v0_85":
        issues.append("review_packet_frontier")
    return tuple(issues)


def verify_current_root_sequence() -> bool:
    return not sequence_issues()


def as_markdown() -> str:
    rows = ["| Step | Runner | Target |", "|---|---|---|"]
    for step in CURRENT_ROOT_STEPS:
        rows.append(f"| {step.step_id} | {step.runner} | `{step.target}` |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = sequence_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
