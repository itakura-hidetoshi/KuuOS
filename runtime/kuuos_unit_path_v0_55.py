#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime import kuuos_root_map_deferral_closeout_v0_54 as closeout

VERSION = "kuuos_unit_path_v0_55"
DEPENDS_ON = closeout.VERSION
READ_ONLY = True
METADATA_ONLY = True
UNIT_PRESENT = True
PR_PATH_REQUIRED = True
GATE_REQUIRED = True

REQUIRED_STEPS: tuple[str, ...] = (
    "observe_frontier",
    "unit_present",
    "choose_one_next_layer",
    "use_pr_path",
    "use_gate_path",
)


@dataclass(frozen=True)
class UnitStep:
    step_id: str
    passed: bool
    note: str


STEPS: tuple[UnitStep, ...] = (
    UnitStep("observe_frontier", closeout.verify_deferral_closeout(), "observes v0.54 closeout"),
    UnitStep("unit_present", UNIT_PRESENT, "unit is present for this sequence"),
    UnitStep("choose_one_next_layer", True, "chooses one bounded next layer"),
    UnitStep("use_pr_path", PR_PATH_REQUIRED, "uses pull request path"),
    UnitStep("use_gate_path", GATE_REQUIRED, "uses governance gate path"),
)


def step_ids() -> tuple[str, ...]:
    return tuple(step.step_id for step in STEPS)


def failed_steps() -> tuple[str, ...]:
    return tuple(step.step_id for step in STEPS if not step.passed)


def unit_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if not READ_ONLY:
        issues.append("not_read_only")
    if not METADATA_ONLY:
        issues.append("not_metadata_only")
    if not UNIT_PRESENT:
        issues.append("unit_not_present")
    if not PR_PATH_REQUIRED:
        issues.append("pr_path_not_required")
    if not GATE_REQUIRED:
        issues.append("gate_not_required")
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


def verify_unit_path() -> bool:
    return not unit_issues()


def as_markdown() -> str:
    rows = ["| Step | Passed | Note |", "|---|---|---|"]
    for step in STEPS:
        rows.append(f"| {step.step_id} | {step.passed} | {step.note} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = unit_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
