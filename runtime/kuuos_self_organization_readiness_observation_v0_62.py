#!/usr/bin/env python3
from __future__ import annotations

from runtime import kuuos_self_organization_precondition_receipt_v0_61 as previous

VERSION = "kuuos_self_organization_readiness_observation_v0_62"
DEPENDS_ON = previous.VERSION
READ_ONLY = True
METADATA_ONLY = True
DIRECT_EXECUTION = previous.DIRECT_EXECUTION
ACTOR = previous.ACTOR
PRECONDITION_RECEIPT = previous.RECEIPT
PRECONDITIONS = previous.PRECONDITIONS
READINESS_OBSERVATION = "self_organization_readiness_observation"
READINESS_OBSERVED = True
ADOPTION_AUTHORIZED = False
MUTATION_AUTHORIZED = False
PR_PATH_REQUIRED = True
GATE_REQUIRED = True

OBSERVATION_FIELDS: tuple[str, ...] = (
    "precondition_receipt_verified",
    "preconditions_present",
    "readiness_observed",
    "read_only_metadata_only_scope_preserved",
    "adoption_not_authorized",
    "mutation_not_authorized",
    "pull_request_path_required",
    "governance_gate_required",
)

EXPECTED_PRECONDITIONS: tuple[str, ...] = (
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
    if not previous.verify_precondition_receipt():
        failed.append("previous_precondition_receipt")
    if not READ_ONLY:
        failed.append("read_only")
    if not METADATA_ONLY:
        failed.append("metadata_only")
    if not DIRECT_EXECUTION:
        failed.append("direct_execution")
    if ACTOR != "KuuOSAgent":
        failed.append("actor")
    if PRECONDITION_RECEIPT != "self_organization_precondition_receipt":
        failed.append("precondition_receipt")
    if PRECONDITIONS != EXPECTED_PRECONDITIONS:
        failed.append("preconditions")
    if READINESS_OBSERVATION != "self_organization_readiness_observation":
        failed.append("readiness_observation")
    if not READINESS_OBSERVED:
        failed.append("readiness_observed")
    if ADOPTION_AUTHORIZED:
        failed.append("adoption_authorized")
    if MUTATION_AUTHORIZED:
        failed.append("mutation_authorized")
    if not PR_PATH_REQUIRED:
        failed.append("pr_path")
    if not GATE_REQUIRED:
        failed.append("gate_path")
    if len(OBSERVATION_FIELDS) != 8:
        failed.append("observation_fields")
    return tuple(failed)


def verify_readiness_observation() -> bool:
    return failed_steps() == ()


if __name__ == "__main__":
    if not verify_readiness_observation():
        print("\n".join(failed_steps()))
        raise SystemExit(1)
    print(VERSION)
