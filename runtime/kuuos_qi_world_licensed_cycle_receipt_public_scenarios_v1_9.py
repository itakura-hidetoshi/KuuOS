from __future__ import annotations

import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_qi_world_licensed_blocker_discharge_v1_7 import (
    authority_packet_digest,
)
from runtime.kuuos_qi_world_licensed_cycle_receipt_public_v1_9 import (
    build_licensed_cycle_receipt,
    build_successor_authority_intake,
    build_successor_authority_requirement,
    successor_authority_intake_digest,
    successor_authority_requirement_digest,
    validate_successor_authority_intake,
    validate_successor_authority_requirement,
)
from runtime.kuuos_qi_world_licensed_cycle_receipt_scenarios_v1_9 import (
    _fresh_candidate,
    run_licensed_cycle_receipt_scenarios as _run_base_scenarios,
)


def _retag_requirement(requirement: dict) -> dict:
    requirement["successor_authority_requirement_digest"] = ""
    requirement["successor_authority_requirement_digest"] = (
        successor_authority_requirement_digest(requirement)
    )
    return requirement


def _retag_intake(intake: dict) -> dict:
    intake["successor_authority_intake_digest"] = ""
    intake["successor_authority_intake_digest"] = successor_authority_intake_digest(
        intake
    )
    return intake


def _expect_requirement_error(
    requirement: dict, receipt: dict, expected: str
) -> None:
    errors = validate_successor_authority_requirement(
        _retag_requirement(requirement),
        closed_cycle_receipt=receipt,
    )
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def _expect_intake_error(
    intake: dict,
    requirement: dict,
    receipt: dict,
    candidate: dict,
    expected: str,
) -> None:
    errors = validate_successor_authority_intake(
        _retag_intake(intake),
        requirement=requirement,
        closed_cycle_receipt=receipt,
        candidate_external_authority_packet=candidate,
    )
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def _bind_candidate_digest(intake: dict, candidate: dict) -> None:
    intake["candidate_external_authority_packet_digest"] = candidate[
        "external_authority_packet_digest"
    ]


def run_licensed_cycle_receipt_scenarios() -> dict:
    result = _run_base_scenarios()

    with tempfile.TemporaryDirectory(
        prefix="kuuos-licensed-cycle-public-v19-"
    ) as temporary:
        receipt = build_licensed_cycle_receipt(Path(temporary))
        requirement = build_successor_authority_requirement(receipt)
        candidate = _fresh_candidate(receipt)
        intake = build_successor_authority_intake(
            requirement=requirement,
            closed_cycle_receipt=receipt,
            candidate_external_authority_packet=candidate,
        )

        predecessor_ordinal_substitution = deepcopy(requirement)
        predecessor_ordinal_substitution["predecessor_cycle_ordinal"] = 9
        _expect_requirement_error(
            predecessor_ordinal_substitution,
            receipt,
            "successor_requirement_predecessor_ordinal_mismatch",
        )

        candidate_content_tamper = deepcopy(candidate)
        candidate_content_tamper["authority_id"] = "tampered-authority-id"
        _expect_intake_error(
            deepcopy(intake),
            requirement,
            receipt,
            candidate_content_tamper,
            "successor_candidate_authority_digest_invalid",
        )

        candidate_plan_tamper = deepcopy(candidate)
        candidate_plan_tamper["source_plan_state_digest"] = "wrong-plan-state"
        candidate_plan_tamper["external_authority_packet_digest"] = ""
        candidate_plan_tamper["external_authority_packet_digest"] = (
            authority_packet_digest(candidate_plan_tamper)
        )
        changed_intake = deepcopy(intake)
        _bind_candidate_digest(changed_intake, candidate_plan_tamper)
        _expect_intake_error(
            changed_intake,
            requirement,
            receipt,
            candidate_plan_tamper,
            "successor_candidate_plan_state_mismatch",
        )

        candidate_issuer_tamper = deepcopy(candidate)
        candidate_issuer_tamper["external_issuer"] = False
        candidate_issuer_tamper["external_authority_packet_digest"] = ""
        candidate_issuer_tamper["external_authority_packet_digest"] = (
            authority_packet_digest(candidate_issuer_tamper)
        )
        changed_intake = deepcopy(intake)
        _bind_candidate_digest(changed_intake, candidate_issuer_tamper)
        _expect_intake_error(
            changed_intake,
            requirement,
            receipt,
            candidate_issuer_tamper,
            "successor_candidate_external_issuer_required",
        )

        candidate_self_issue_tamper = deepcopy(candidate)
        candidate_self_issue_tamper["self_issued"] = True
        candidate_self_issue_tamper["external_authority_packet_digest"] = ""
        candidate_self_issue_tamper["external_authority_packet_digest"] = (
            authority_packet_digest(candidate_self_issue_tamper)
        )
        changed_intake = deepcopy(intake)
        _bind_candidate_digest(changed_intake, candidate_self_issue_tamper)
        _expect_intake_error(
            changed_intake,
            requirement,
            receipt,
            candidate_self_issue_tamper,
            "successor_candidate_self_issue_forbidden",
        )

        candidate_multiuse_tamper = deepcopy(candidate)
        candidate_multiuse_tamper["single_use"] = False
        candidate_multiuse_tamper["external_authority_packet_digest"] = ""
        candidate_multiuse_tamper["external_authority_packet_digest"] = (
            authority_packet_digest(candidate_multiuse_tamper)
        )
        changed_intake = deepcopy(intake)
        _bind_candidate_digest(changed_intake, candidate_multiuse_tamper)
        _expect_intake_error(
            changed_intake,
            requirement,
            receipt,
            candidate_multiuse_tamper,
            "successor_candidate_single_use_required",
        )

    result["independent_candidate_revalidation"] = True
    result["predecessor_ordinal_revalidation"] = True
    return result
