#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

VERSION = "kuuos_current_root_sequence_v0_41"
DEPENDS_ON = "kuuos_repository_frontier_summary_v0_40"
CURRENT_ROOT = "runtime/kuuos_current_check.py"


@dataclass(frozen=True)
class CurrentRootStep:
    step_id: str
    runner: str
    target: str
    required: bool
    note: str


CURRENT_ROOT_STEPS: tuple[CurrentRootStep, ...] = (
    CurrentRootStep(
        "closed-repository-root",
        "callable",
        "runtime.v124_checkpoint_reflog_runtime:run_v124",
        True,
        "Closed repository root remains first in the current check order.",
    ),
    CurrentRootStep(
        "lifecycle-completion-v0-36",
        "unittest",
        "tests.test_kuuos_lifecycle_completion_v0_36",
        True,
        "Lifecycle completion remains distinct from repository root checks.",
    ),
    CurrentRootStep(
        "repository-index-v0-37",
        "unittest",
        "tests.test_kuuos_repo_index_v0_37",
        True,
        "Repository line and root index remains explicit.",
    ),
    CurrentRootStep(
        "repository-structure-map-v0-38",
        "unittest",
        "tests.test_kuuos_repository_structure_map_v0_38",
        True,
        "Directory zone map remains checked from the current root.",
    ),
    CurrentRootStep(
        "repository-cleanup-proposals-v0-39",
        "unittest",
        "tests.test_kuuos_repository_cleanup_proposals_v0_39",
        True,
        "Cleanup proposals remain proposal-only and checked from the current root.",
    ),
    CurrentRootStep(
        "repository-frontier-summary-v0-40",
        "unittest",
        "tests.test_kuuos_repository_frontier_summary_v0_40",
        True,
        "Human-facing frontier summary remains linked to machine checks.",
    ),
    CurrentRootStep(
        "current-root-sequence-v0-41",
        "unittest",
        "tests.test_kuuos_current_root_sequence_v0_41",
        True,
        "Current root order is defined by this sequence layer.",
    ),
    CurrentRootStep(
        "manifest-index-v0-42",
        "unittest",
        "tests.test_kuuos_manifest_index_v0_42",
        True,
        "Manifest metadata index remains checked from the current root.",
    ),
    CurrentRootStep(
        "docs-index-v0-43",
        "unittest",
        "tests.test_kuuos_docs_index_v0_43",
        True,
        "Documentation index remains checked from the current root.",
    ),
    CurrentRootStep(
        "overview-index-v0-44",
        "unittest",
        "tests.test_kuuos_overview_index_v0_44",
        True,
        "Overview index remains checked from the current root.",
    ),
    CurrentRootStep(
        "ci-continuation-v0-45",
        "unittest",
        "tests.test_kuuos_ci_continuation_v0_45",
        True,
        "CI continuation observes every root step before deciding the final status.",
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
    required_targets = {
        "tests.test_kuuos_lifecycle_completion_v0_36",
        "tests.test_kuuos_repo_index_v0_37",
        "tests.test_kuuos_repository_structure_map_v0_38",
        "tests.test_kuuos_repository_cleanup_proposals_v0_39",
        "tests.test_kuuos_repository_frontier_summary_v0_40",
        "tests.test_kuuos_current_root_sequence_v0_41",
        "tests.test_kuuos_manifest_index_v0_42",
        "tests.test_kuuos_docs_index_v0_43",
        "tests.test_kuuos_overview_index_v0_44",
        "tests.test_kuuos_ci_continuation_v0_45",
    }
    missing = required_targets.difference(unittest_targets())
    if missing:
        issues.append("missing_unittest_target:" + ",".join(sorted(missing)))
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
