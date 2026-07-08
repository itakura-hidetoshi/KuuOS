#!/usr/bin/env python3
from __future__ import annotations

from runtime import kuuos_current_root_sequence_v0_111 as previous
from runtime.kuuos_current_root_sequence_v0_41 import CurrentRootStep

VERSION = "kuuos_current_root_sequence_v0_112"
DEPENDS_ON = previous.VERSION
CURRENT_ROOT = "runtime/kuuos_current_check.py"
CANDIDATE_RECEIPT_FRONTIER = "kuuos_self_organization_candidate_receipt_v0_112"
SELF_CHECK_TARGET = "runtime.kuuos_current_root_sequence_v0_112:run_self_check"

CURRENT_ROOT_STEPS: tuple[CurrentRootStep, ...] = previous.CURRENT_ROOT_STEPS + (
    CurrentRootStep(
        "candidate-receipt-v0-112",
        "unittest",
        "tests.test_kuuos_self_organization_candidate_receipt_v0_112",
        True,
        "Candidate receipt v0.112 is verified.",
    ),
    CurrentRootStep(
        "current-root-sequence-v0-112",
        "callable",
        SELF_CHECK_TARGET,
        True,
        "Current root sequence v0.112 is verified.",
    ),
)


def step_ids() -> tuple[str, ...]:
    return tuple(step.step_id for step in CURRENT_ROOT_STEPS)


def step_targets() -> tuple[str, ...]:
    return tuple(step.target for step in CURRENT_ROOT_STEPS)


def unittest_targets() -> tuple[str, ...]:
    return tuple(step.target for step in CURRENT_ROOT_STEPS if step.runner == "unittest")


def callable_targets() -> tuple[str, ...]:
    return tuple(step.target for step in CURRENT_ROOT_STEPS if step.runner == "callable")


def sequence_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if not previous.verify_current_root_sequence():
        issues.append("previous_current_root_sequence")
    if len(step_ids()) != len(set(step_ids())):
        issues.append("duplicate_step_id")
    if len(step_targets()) != len(set(step_targets())):
        issues.append("duplicate_step_target")
    required_unittests = set(previous.unittest_targets()).union(
        {"tests.test_kuuos_self_organization_candidate_receipt_v0_112"}
    )
    missing_unittests = required_unittests.difference(unittest_targets())
    if missing_unittests:
        issues.append("missing_unittest_target:" + ",".join(sorted(missing_unittests)))
    if SELF_CHECK_TARGET not in callable_targets():
        issues.append("missing_self_check_target")
    if CANDIDATE_RECEIPT_FRONTIER != "kuuos_self_organization_candidate_receipt_v0_112":
        issues.append("candidate_receipt_frontier")
    return tuple(issues)


def verify_current_root_sequence() -> bool:
    return not sequence_issues()


def run_self_check() -> int:
    return 0 if verify_current_root_sequence() else 1


if __name__ == "__main__":
    problems = sequence_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(VERSION)
