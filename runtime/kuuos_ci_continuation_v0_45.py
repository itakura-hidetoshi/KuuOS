#!/usr/bin/env python3
from __future__ import annotations

import importlib
import io
import unittest
from dataclasses import dataclass
from typing import Callable, Iterable, Protocol

from runtime.kuuos_current_root_sequence_v0_41 import CURRENT_ROOT_STEPS

VERSION = "kuuos_ci_continuation_v0_45"
DEPENDS_ON = "kuuos_overview_index_v0_44"
POLICY = "run_all_then_decide"
SUCCESS_DECISION = "CONTINUE_TO_NEXT_STAGE_REVIEW"
FAILURE_DECISION = "REPAIR_FAILED_STEPS_BEFORE_CONTINUATION"

NON_AUTHORITY_BOUNDARIES: tuple[str, ...] = (
    "ci_success_does_not_grant_merge_authority",
    "ci_success_does_not_grant_theorem_authority",
    "continuation_does_not_execute_git_or_github_mutation",
    "failed_required_step_blocks_continuation",
)


class StepLike(Protocol):
    step_id: str
    runner: str
    target: str
    required: bool


@dataclass(frozen=True)
class ContinuationStep:
    step_id: str
    runner: str
    target: str
    required: bool


@dataclass(frozen=True)
class ContinuationStepResult:
    step_id: str
    runner: str
    target: str
    required: bool
    exit_code: int
    status: str
    detail: str


@dataclass(frozen=True)
class ContinuationReport:
    version: str
    policy: str
    decision: str
    all_steps_observed: bool
    required_failure_count: int
    results: tuple[ContinuationStepResult, ...]

    @property
    def passed(self) -> bool:
        return self.required_failure_count == 0 and self.all_steps_observed

    def failed_steps(self) -> tuple[str, ...]:
        return tuple(result.step_id for result in self.results if result.exit_code != 0)

    def observed_step_ids(self) -> tuple[str, ...]:
        return tuple(result.step_id for result in self.results)

    def as_markdown(self) -> str:
        rows = ["| Step | Runner | Status | Detail |", "|---|---|---|---|"]
        for result in self.results:
            rows.append(
                f"| {result.step_id} | {result.runner} | {result.status} | {result.detail} |"
            )
        rows.append(f"\nDecision: `{self.decision}`")
        return "\n".join(rows)


Executor = Callable[[StepLike], tuple[int, str]]


def _status_from_exit(exit_code: int) -> str:
    return "PASS" if exit_code == 0 else "FAIL"


def _run_unittest_module(module_name: str) -> tuple[int, str]:
    stream = io.StringIO()
    try:
        suite = unittest.defaultTestLoader.loadTestsFromName(module_name)
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    except Exception as exc:  # pragma: no cover - defensive CI surface
        return 1, "unittest_exception:" + exc.__class__.__name__
    if result.wasSuccessful():
        return 0, "unittest_passed"
    return 1, "unittest_failed"


def _run_callable(target: str) -> tuple[int, str]:
    try:
        module_name, function_name = target.split(":", 1)
        module = importlib.import_module(module_name)
        outcome = getattr(module, function_name)()
    except Exception as exc:  # pragma: no cover - defensive CI surface
        return 1, "callable_exception:" + exc.__class__.__name__
    exit_code = int(outcome)
    detail = "callable_passed" if exit_code == 0 else "callable_failed"
    return exit_code, detail


def _default_executor(step: StepLike) -> tuple[int, str]:
    if step.runner == "unittest":
        return _run_unittest_module(step.target)
    if step.runner == "callable":
        return _run_callable(step.target)
    return 1, "unknown_runner:" + step.runner


def _to_result(step: StepLike, executor: Executor) -> ContinuationStepResult:
    exit_code, detail = executor(step)
    return ContinuationStepResult(
        step.step_id,
        step.runner,
        step.target,
        step.required,
        exit_code,
        _status_from_exit(exit_code),
        detail,
    )


def run_ci_continuation(
    steps: Iterable[StepLike] = CURRENT_ROOT_STEPS,
    executor: Executor | None = None,
) -> ContinuationReport:
    step_tuple = tuple(steps)
    run_step = executor or _default_executor
    results = tuple(_to_result(step, run_step) for step in step_tuple)
    required_failures = tuple(
        result for result in results if result.required and result.exit_code != 0
    )
    all_observed = len(results) == len(step_tuple) and bool(step_tuple)
    decision = SUCCESS_DECISION if all_observed and not required_failures else FAILURE_DECISION
    return ContinuationReport(
        VERSION,
        POLICY,
        decision,
        all_observed,
        len(required_failures),
        results,
    )


def continuation_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if DEPENDS_ON != "kuuos_overview_index_v0_44":
        issues.append("invalid_dependency")
    if POLICY != "run_all_then_decide":
        issues.append("invalid_policy")
    if len(NON_AUTHORITY_BOUNDARIES) != len(set(NON_AUTHORITY_BOUNDARIES)):
        issues.append("duplicate_non_authority_boundary")
    required_boundaries = {
        "ci_success_does_not_grant_merge_authority",
        "ci_success_does_not_grant_theorem_authority",
        "continuation_does_not_execute_git_or_github_mutation",
        "failed_required_step_blocks_continuation",
    }
    missing_boundaries = required_boundaries.difference(NON_AUTHORITY_BOUNDARIES)
    if missing_boundaries:
        issues.append("missing_boundary:" + ",".join(sorted(missing_boundaries)))
    unittest_targets = {step.target for step in CURRENT_ROOT_STEPS if step.runner == "unittest"}
    if "tests.test_kuuos_ci_continuation_v0_45" not in unittest_targets:
        issues.append("missing_current_root_self_test")
    return tuple(issues)


def verify_ci_continuation() -> bool:
    return not continuation_issues()


def run_current_continuation() -> int:
    report = run_ci_continuation()
    print(report.as_markdown())
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(run_current_continuation())
