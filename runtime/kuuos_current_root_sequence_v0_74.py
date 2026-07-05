#!/usr/bin/env python3
from __future__ import annotations

from runtime import kuuos_current_root_sequence_v0_73 as previous
from runtime.kuuos_current_root_sequence_v0_41 import CurrentRootStep

VERSION = "kuuos_current_root_sequence_v0_74"
DEPENDS_ON = previous.VERSION
CURRENT_ROOT = "runtime/kuuos_current_check.py"
CURRENT_STATUS_SURFACE_FRONTIER = "kuuos_current_status_surface_v0_74"

CURRENT_ROOT_STEPS: tuple[CurrentRootStep, ...] = previous.CURRENT_ROOT_STEPS + (
    CurrentRootStep(
        "current-status-surface-v0-74",
        "unittest",
        "tests.test_kuuos_current_status_surface_v0_74",
        True,
        "Current status surface must expose the verified manifest and resolved status artifact.",
    ),
    CurrentRootStep(
        "current-root-sequence-v0-74",
        "unittest",
        "tests.test_kuuos_current_root_sequence_v0_74",
        True,
        "This layer connects the current status surface into the current runtime root.",
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
    if not CURRENT_ROOT_STEPS:
        issues.append("empty_current_root_sequence")
    if CURRENT_ROOT_STEPS[0].runner != "callable":
        issues.append("first_step_not_callable_root")
    if CURRENT_ROOT_STEPS[0].target != "runtime.v124_checkpoint_reflog_runtime:run_v124":
        issues.append("first_step_target_invalid")
    for step in CURRENT_ROOT_STEPS:
        if step.runner not in {"callable", "unittest"}:
            issues.append("unknown_runner:" + step.step_id)
        if not step.required:
            issues.append("optional_step_not_allowed:" + step.step_id)
        if not step.target:
            issues.append("missing_target:" + step.step_id)
    required_targets = set(previous.unittest_targets()).union(
        {
            "tests.test_kuuos_current_status_surface_v0_74",
            "tests.test_kuuos_current_root_sequence_v0_74",
        }
    )
    missing = required_targets.difference(unittest_targets())
    if missing:
        issues.append("missing_unittest_target:" + ",".join(sorted(missing)))
    if CURRENT_STATUS_SURFACE_FRONTIER != "kuuos_current_status_surface_v0_74":
        issues.append("current_status_surface_frontier")
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
    raise SystemExit(0)
