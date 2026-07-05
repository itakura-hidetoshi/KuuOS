#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

from runtime import kuuos_root_map_adoption_proposal_v0_49 as proposal

VERSION = "kuuos_root_map_adoption_readiness_v0_50"
DEPENDS_ON = proposal.VERSION
READ_ONLY = True
METADATA_ONLY = True
ADOPTION_PERFORMED = False

REQUIRED_READINESS_CHECKS: tuple[str, ...] = (
    "proposal_verifies",
    "proposal_only_boundary_present",
    "automatic_adoption_blocked",
    "future_stage_required",
    "mutation_authority_absent",
)


@dataclass(frozen=True)
class ReadinessCheck:
    check_id: str
    passed: bool
    reason: str


READINESS_CHECKS: tuple[ReadinessCheck, ...] = (
    ReadinessCheck(
        "proposal_verifies",
        proposal.verify_adoption_proposal(),
        "v0.49 proposal has no local issues",
    ),
    ReadinessCheck(
        "proposal_only_boundary_present",
        "proposal_only" in proposal.proposal_boundaries(),
        "proposal remains a proposal and is not adopted",
    ),
    ReadinessCheck(
        "automatic_adoption_blocked",
        "no_automatic_adoption" in proposal.proposal_boundaries(),
        "adoption cannot happen automatically from the proposal layer",
    ),
    ReadinessCheck(
        "future_stage_required",
        "new_stage_required_for_adoption" in proposal.proposal_boundaries(),
        "any adoption requires a later governance layer",
    ),
    ReadinessCheck(
        "mutation_authority_absent",
        "no_mutation_authority" in proposal.proposal_boundaries(),
        "no repository mutation authority is present",
    ),
)


def check_ids() -> tuple[str, ...]:
    return tuple(item.check_id for item in READINESS_CHECKS)


def passed_checks() -> tuple[str, ...]:
    return tuple(item.check_id for item in READINESS_CHECKS if item.passed)


def failed_checks() -> tuple[str, ...]:
    return tuple(item.check_id for item in READINESS_CHECKS if not item.passed)


def readiness_issues() -> tuple[str, ...]:
    issues: list[str] = []
    if not READ_ONLY:
        issues.append("not_read_only")
    if not METADATA_ONLY:
        issues.append("not_metadata_only")
    if ADOPTION_PERFORMED:
        issues.append("adoption_performed")
    if len(check_ids()) != len(set(check_ids())):
        issues.append("duplicate_check_id")
    missing = set(REQUIRED_READINESS_CHECKS).difference(check_ids())
    if missing:
        issues.append("missing_readiness_check:" + ",".join(sorted(missing)))
    for check in READINESS_CHECKS:
        if not check.reason:
            issues.append("missing_reason:" + check.check_id)
    for failed in failed_checks():
        issues.append("failed_readiness_check:" + failed)
    return tuple(issues)


def verify_adoption_readiness() -> bool:
    return not readiness_issues()


def as_markdown() -> str:
    rows = ["| Check | Passed | Reason |", "|---|---|---|"]
    for check in READINESS_CHECKS:
        rows.append(f"| {check.check_id} | {check.passed} | {check.reason} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = readiness_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
