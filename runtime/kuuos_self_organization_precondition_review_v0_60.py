#!/usr/bin/env python3
from __future__ import annotations

from runtime import kuuos_self_organization_boundary_v0_59 as previous

VERSION = "kuuos_self_organization_precondition_review_v0_60"
DEPENDS_ON = previous.VERSION
READ_ONLY = True
METADATA_ONLY = True
DIRECT_EXECUTION = previous.DIRECT_EXECUTION
ACTOR = previous.ACTOR
BOUNDARY = previous.BOUNDARY
PRECONDITION_REVIEW = "self_organization_adoption_precondition_review"
ADOPTION_AUTHORIZED = False
MUTATION_AUTHORIZED = False
PR_PATH_REQUIRED = True
GATE_REQUIRED = True

PRECONDITIONS: tuple[str, ...] = (
    "boundary_verified",
    "receipt_chain_verified",
    "read_only_metadata_only_scope_preserved",
    "adoption_not_authorized",
    "mutation_not_authorized",
    "pull_request_path_required",
    "governance_gate_required",
)


def failed_steps() -> tuple[str, ...]:
    failed: list[str] = []
    if not previous.verify_self_organization_boundary():
        failed.append("previous_boundary")
    if not READ_ONLY:
        failed.append("read_only")
    if not METADATA_ONLY:
        failed.append("metadata_only")
    if not DIRECT_EXECUTION:
        failed.append("direct_execution")
    if ACTOR != "KuuOSAgent":
        failed.append("actor")
    if BOUNDARY != "self_organization_adoption_boundary":
        failed.append("boundary")
    if PRECONDITION_REVIEW != "self_organization_adoption_precondition_review":
        failed.append("precondition_review")
    if ADOPTION_AUTHORIZED:
        failed.append("adoption_authorized")
    if MUTATION_AUTHORIZED:
        failed.append("mutation_authorized")
    if not PR_PATH_REQUIRED:
        failed.append("pr_path")
    if not GATE_REQUIRED:
        failed.append("gate_path")
    if len(PRECONDITIONS) != 7:
        failed.append("preconditions")
    return tuple(failed)


def verify_precondition_review() -> bool:
    return failed_steps() == ()


if __name__ == "__main__":
    if not verify_precondition_review():
        print("\n".join(failed_steps()))
        raise SystemExit(1)
    print(VERSION)
