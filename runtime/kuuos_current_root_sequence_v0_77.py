#!/usr/bin/env python3
from __future__ import annotations

from runtime import kuuos_current_root_sequence_v0_76 as previous
from runtime.kuuos_current_root_sequence_v0_41 import CurrentRootStep

VERSION = "kuuos_current_root_sequence_v0_77"
DEPENDS_ON = previous.VERSION
CURRENT_ROOT = "runtime/kuuos_current_check.py"
CURRENT_SURFACE_ENTRYPOINT_FRONTIER = "kuuos_current_surface_entrypoint_v0_77"
STABLE_CURRENT_SURFACE_CLI = "runtime/kuuos_current_surface.py"

CURRENT_ROOT_STEPS: tuple[CurrentRootStep, ...] = previous.CURRENT_ROOT_STEPS + (
    CurrentRootStep(
        "current-surface-entrypoint-v0-77",
        "unittest",
        "tests.test_kuuos_current_surface_entrypoint_v0_77",
        True,
        "Current surface entrypoint is verified.",
    ),
    CurrentRootStep(
        "current-surface-cli-v0-77",
        "unittest",
        "tests.test_kuuos_current_surface_cli_v0_77",
        True,
        "Stable current surface CLI is verified.",
    ),
    CurrentRootStep(
        "current-root-sequence-v0-77",
        "unittest",
        "tests.test_kuuos_current_root_sequence_v0_77",
        True,
        "Current root sequence v0.77 is verified.",
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
    required_targets = set(previous.unittest_targets()).union(
        {
            "tests.test_kuuos_current_surface_entrypoint_v0_77",
            "tests.test_kuuos_current_surface_cli_v0_77",
            "tests.test_kuuos_current_root_sequence_v0_77",
        }
    )
    missing = required_targets.difference(unittest_targets())
    if missing:
        issues.append("missing_unittest_target:" + ",".join(sorted(missing)))
    if CURRENT_SURFACE_ENTRYPOINT_FRONTIER != "kuuos_current_surface_entrypoint_v0_77":
        issues.append("current_surface_entrypoint_frontier")
    if STABLE_CURRENT_SURFACE_CLI != "runtime/kuuos_current_surface.py":
        issues.append("stable_current_surface_cli")
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
