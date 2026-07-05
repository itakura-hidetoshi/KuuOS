#!/usr/bin/env python3
from __future__ import annotations

from runtime import kuuos_receipt_v0_58 as previous

VERSION = "kuuos_self_organization_boundary_v0_59"
DEPENDS_ON = previous.VERSION
READ_ONLY = True
METADATA_ONLY = True
DIRECT_EXECUTION = previous.DIRECT_EXECUTION
ACTOR = previous.ACTOR
RECEIPT = previous.RECEIPT
BOUNDARY = "self_organization_adoption_boundary"
ADOPTION_AUTHORIZED = False
MUTATION_AUTHORIZED = False
PR_PATH_REQUIRED = True
GATE_REQUIRED = True

BOUNDARY_RULES: tuple[str, ...] = (
    "receipt_verified_before_boundary",
    "no_adoption_authorization",
    "no_repository_mutation_authorization",
    "pull_request_path_required",
    "governance_gate_required",
)


def failed_steps() -> tuple[str, ...]:
    failed: list[str] = []
    if not previous.verify_receipt():
        failed.append("previous_receipt")
    if not READ_ONLY:
        failed.append("read_only")
    if not METADATA_ONLY:
        failed.append("metadata_only")
    if not DIRECT_EXECUTION:
        failed.append("direct_execution")
    if ACTOR != "KuuOSAgent":
        failed.append("actor")
    if RECEIPT != "self_organization_receipt":
        failed.append("receipt")
    if BOUNDARY != "self_organization_adoption_boundary":
        failed.append("boundary")
    if ADOPTION_AUTHORIZED:
        failed.append("adoption_authorized")
    if MUTATION_AUTHORIZED:
        failed.append("mutation_authorized")
    if not PR_PATH_REQUIRED:
        failed.append("pr_path")
    if not GATE_REQUIRED:
        failed.append("gate_path")
    if len(BOUNDARY_RULES) != 5:
        failed.append("boundary_rules")
    return tuple(failed)


def verify_self_organization_boundary() -> bool:
    return failed_steps() == ()


if __name__ == "__main__":
    if not verify_self_organization_boundary():
        print("\n".join(failed_steps()))
        raise SystemExit(1)
    print(VERSION)
