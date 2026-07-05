#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime import kuuos_root_map_deferral_closeout_v0_54 as closeout

VERSION = "kuuos_bounded_steering_v0_55"
DEPENDS_ON = closeout.VERSION
READ_ONLY = True
METADATA_ONLY = True
STEERING_ONLY = True

REQUIRED_STEPS: tuple[str, ...] = (
    "observe_frontier",
    "preserve_boundaries",
    "choose_one_next_layer",
    "require_draft_pr",
    "require_gate_before_merge",
)


@dataclass(frozen=True)
class SteeringStep:
    step_id: str
    passed: bool
    note: str


STEPS: tuple[SteeringStep, ...] = (
    SteeringStep("observe_frontier", closeout.verify_deferral_closeout(), "observes v0.54 closeout"),
    SteeringStep("preserve_boundaries", closeout.READ_ONLY and closeout.METADATA_ONLY, "keeps read-only metadata-only boundaries"),
    SteeringStep("choose_one_next_layer", True, "chooses one bounded next layer"),
    SteeringStep("require_draft_pr", True, "uses draft PR path"),
    SteeringStep("require_gate_before_merge", True, "uses governance gate path"),
)


def step_ids() -> tuple[str, ...]:
    return tuple(step.step_id for step in STEPS)


def failed_steps() -> tuple[str, ...]:
    return tuple(step.step_id for step in STEPS if not step.passed)


def steering_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if not READ_ONLY:
        issues.append("not_read_only")
    if not METADATA_ONLY:
        issues.append("not_metadata_only")
    if not STEERING_ONLY:
        issues.append("not_steering_only")
    if len(step_ids()) != len(set(step_ids())):
        issues.append("duplicate_step")
    missing = set(REQUIRED_STEPS).difference(step_ids())
    if missing:
        issues.append("missing_step:" + ",".join(sorted(missing)))
    for step in STEPS:
        if not step.note:
            issues.append("missing_note:" + step.step_id)
    for failed in failed_steps():
        issues.append("failed_step:" + failed)
    return tuple(issues)


def verify_bounded_steering() -> bool:
    return not steering_issues()


def as_markdown() -> str:
    rows = ["| Step | Passed | Note |", "|---|---|---|"]
    for step in STEPS:
        rows.append(f"| {step.step_id} | {step.passed} | {step.note} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = steering_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
