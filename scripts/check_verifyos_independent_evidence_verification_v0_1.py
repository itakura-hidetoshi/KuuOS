#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_observeos_sequential_epistemic_observability_common_v0_1 import (
    STATUS_BLOCKED,
    STATUS_READY,
    canonical_digest,
)
from runtime.kuuos_verifyos_sequential_epistemic_observation_verification_handoff_v0_1 import (
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_verifyos_independent_evidence_verification_v0_1 import (
    CONTEXT_DIGEST_FIELD,
    EVIDENCE_DIGEST_FIELD,
    EXECUTION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    DISPOSITION_ACCEPTANCE_REPAIR,
    DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
    DISPOSITION_CORRESPONDENCE_REPAIR,
    DISPOSITION_CURRENT_STATE_MUTATION_REJECTED,
    DISPOSITION_EVIDENCE_REPAIR,
    DISPOSITION_FAILED,
    DISPOSITION_INDETERMINATE,
    DISPOSITION_INDEPENDENCE_REPAIR,
    DISPOSITION_PASSED,
    DISPOSITION_PROTOCOL_REPAIR,
    DISPOSITION_REPLAY_REJECTED,
    DISPOSITION_REPRODUCTION_REPAIR,
    DISPOSITION_REVIEW_REPAIR,
    DISPOSITION_SOURCE_REPAIR,
    OUTCOME_FAILED,
    OUTCOME_INDETERMINATE,
    OUTCOME_PASSED,
    build_verifyos_independent_evidence_verification,
    compute_exact_verification_cycle_digest as cycle_digest,
    compute_independent_verification_context_digest as context_digest,
    compute_independent_verification_evidence_bundle_digest as evidence_digest,
    compute_independent_verification_execution_digest as execution_digest,
    compute_independent_verification_result_review_digest as review_digest,
    compute_requested_verification_operation_digest as operation_digest,
    compute_verification_bundle_digest as bundle_digest,
)
from scripts.check_verifyos_sequential_epistemic_observation_verification_handoff_v0_1 import (
    fixture as handoff_fixture,
    run as run_handoff,
)

POLICY = "verifyos-v0-14-policy"
RESPONSIBILITY = "verifyos-v0-14-responsibility"
VERIFICATION_ID = "independent-verification-001"


def source_handoff() -> dict:
    result = run_handoff(handoff_fixture())
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    return deepcopy(result.receipt)


def evidence(source: dict) -> dict:
    value = {
        "source_verification_handoff_receipt_digest": source[
            SOURCE_RECEIPT_DIGEST_FIELD
        ],
        "source_observability_receipt_digest": source[
            "source_observability_receipt_digest"
        ],
        "source_evidence_snapshot_digests": source["evidence_snapshot_digests"],
        "independent_evidence_source_ids": ["independent-source-v0-14-a"],
        "independent_evidence_artifact_digests": [
            "recomputed-uncertainty-artifact",
            "recomputed-calibration-artifact",
            "recomputed-shift-artifact",
        ],
        "recomputed_sequential_uncertainty_digest": "recomputed-cs-a",
        "recomputed_conformal_calibration_digest": "recomputed-conformal-a",
        "recomputed_distribution_shift_digest": "recomputed-adwin-a",
        "evidence_integrity_confirmed": True,
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
        "evidence_conclusive": True,
        "evidence_collected_epoch": 200,
    }
    value[EVIDENCE_DIGEST_FIELD] = evidence_digest(value)
    return value


def execution(source: dict, evidence_value: dict) -> dict:
    value = {
        "source_verification_handoff_receipt_digest": source[
            SOURCE_RECEIPT_DIGEST_FIELD
        ],
        EVIDENCE_DIGEST_FIELD: evidence_value[EVIDENCE_DIGEST_FIELD],
        "verification_protocol_digest": "protocol-a",
        "acceptance_criteria_digest": "criteria-a",
        "reproduction_plan_digest": "reproduction-a",
        "verifier_id": source["verifier_id"],
        "verification_scope": source["verification_scope"],
        "planned_reproduction_attempts": 2,
        "completed_reproduction_attempts": 2,
        "successful_reproduction_attempts": 2,
        "falsification_challenge_executed": True,
        "falsification_challenge_passed": True,
        "acceptance_criteria_satisfied": True,
        "execution_started_epoch": 201,
        "execution_completed_epoch": 205,
        "maximum_execution_duration": 20,
        "observation_recollection_performed": False,
        "current_state_mutation_performed": False,
        "authority_escalation_requested": False,
        "generalized_truth_claimed": False,
        "causal_verification_claimed": False,
        "verification_outcome": OUTCOME_PASSED,
    }
    value[EXECUTION_DIGEST_FIELD] = execution_digest(value)
    return value


def review(source: dict, execution_value: dict) -> dict:
    value = {
        "source_verification_handoff_receipt_digest": source[
            SOURCE_RECEIPT_DIGEST_FIELD
        ],
        EXECUTION_DIGEST_FIELD: execution_value[EXECUTION_DIGEST_FIELD],
        "reviewer_id": "verification-reviewer-b",
        "verifier_independence_confirmed": True,
        "reviewer_independence_confirmed": True,
        "evidence_integrity_adequate": True,
        "protocol_execution_adequate": True,
        "reproduction_adequate": True,
        "acceptance_adjudication_adequate": True,
        "outcome_supported": True,
        "no_observation_recollection": True,
        "no_current_state_mutation": True,
        "no_authority_escalation": True,
        "no_truth_claim": True,
        "no_causal_claim": True,
        "review_started_epoch": 206,
        "review_completed_epoch": 208,
        "maximum_review_duration": 10,
    }
    value[REVIEW_DIGEST_FIELD] = review_digest(value)
    return value


def context(
    source: dict,
    evidence_value: dict,
    execution_value: dict,
    review_value: dict,
) -> dict:
    value = {
        "source_verification_handoff_receipt_digest": source[
            SOURCE_RECEIPT_DIGEST_FIELD
        ],
        EVIDENCE_DIGEST_FIELD: evidence_value[EVIDENCE_DIGEST_FIELD],
        EXECUTION_DIGEST_FIELD: execution_value[EXECUTION_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: review_value[REVIEW_DIGEST_FIELD],
        "source_world_revision": source["resulting_world_revision"],
        "current_world_revision": source["resulting_world_revision"],
        "verification_session_id": "verification-session-a",
        "verification_nonce_digest": "verification-nonce-a",
        "prior_verification_session_ids": [],
        "prior_verification_nonce_digests": [],
        "prior_verification_execution_digests": [],
        "prior_verification_receipt_digests": [],
    }
    value["requested_verification_operation_digest"] = operation_digest(
        source, evidence_value, execution_value, review_value
    )
    value["exact_verification_cycle_digest"] = cycle_digest(
        source, evidence_value, execution_value, review_value, value
    )
    value[CONTEXT_DIGEST_FIELD] = context_digest(value)
    return value


def fixture() -> dict:
    source = source_handoff()
    evidence_value = evidence(source)
    execution_value = execution(source, evidence_value)
    review_value = review(source, execution_value)
    context_value = context(source, evidence_value, execution_value, review_value)
    return {
        "source": source,
        "evidence": evidence_value,
        "execution": execution_value,
        "review": review_value,
        "context": context_value,
    }


def rebind(value: dict) -> None:
    source = value["source"]
    evidence_value = value["evidence"]
    execution_value = value["execution"]
    review_value = value["review"]
    context_value = value["context"]

    source.pop(SOURCE_RECEIPT_DIGEST_FIELD, None)
    source[SOURCE_RECEIPT_DIGEST_FIELD] = canonical_digest(source)

    evidence_value.update(
        {
            "source_verification_handoff_receipt_digest": source[
                SOURCE_RECEIPT_DIGEST_FIELD
            ],
            "source_observability_receipt_digest": source[
                "source_observability_receipt_digest"
            ],
            "source_evidence_snapshot_digests": source[
                "evidence_snapshot_digests"
            ],
        }
    )
    evidence_value.pop(EVIDENCE_DIGEST_FIELD, None)
    evidence_value[EVIDENCE_DIGEST_FIELD] = evidence_digest(evidence_value)

    execution_value.update(
        {
            "source_verification_handoff_receipt_digest": source[
                SOURCE_RECEIPT_DIGEST_FIELD
            ],
            EVIDENCE_DIGEST_FIELD: evidence_value[EVIDENCE_DIGEST_FIELD],
            "verifier_id": source["verifier_id"],
            "verification_scope": source["verification_scope"],
        }
    )
    execution_value.pop(EXECUTION_DIGEST_FIELD, None)
    execution_value[EXECUTION_DIGEST_FIELD] = execution_digest(execution_value)

    review_value.update(
        {
            "source_verification_handoff_receipt_digest": source[
                SOURCE_RECEIPT_DIGEST_FIELD
            ],
            EXECUTION_DIGEST_FIELD: execution_value[EXECUTION_DIGEST_FIELD],
        }
    )
    review_value.pop(REVIEW_DIGEST_FIELD, None)
    review_value[REVIEW_DIGEST_FIELD] = review_digest(review_value)

    context_value.update(
        {
            "source_verification_handoff_receipt_digest": source[
                SOURCE_RECEIPT_DIGEST_FIELD
            ],
            EVIDENCE_DIGEST_FIELD: evidence_value[EVIDENCE_DIGEST_FIELD],
            EXECUTION_DIGEST_FIELD: execution_value[EXECUTION_DIGEST_FIELD],
            REVIEW_DIGEST_FIELD: review_value[REVIEW_DIGEST_FIELD],
            "source_world_revision": source["resulting_world_revision"],
        }
    )
    context_value["requested_verification_operation_digest"] = operation_digest(
        source, evidence_value, execution_value, review_value
    )
    context_value["exact_verification_cycle_digest"] = cycle_digest(
        source,
        evidence_value,
        execution_value,
        review_value,
        context_value,
    )
    context_value.pop(CONTEXT_DIGEST_FIELD, None)
    context_value[CONTEXT_DIGEST_FIELD] = context_digest(context_value)


def build_current(value: dict):
    source = value["source"]
    evidence_value = value["evidence"]
    execution_value = value["execution"]
    review_value = value["review"]
    context_value = value["context"]
    verification_bundle = bundle_digest(
        source_verification_handoff_receipt_digest=source[
            SOURCE_RECEIPT_DIGEST_FIELD
        ],
        independent_verification_evidence_bundle_digest=evidence_value[
            EVIDENCE_DIGEST_FIELD
        ],
        independent_verification_execution_digest=execution_value[
            EXECUTION_DIGEST_FIELD
        ],
        independent_verification_result_review_digest=review_value[
            REVIEW_DIGEST_FIELD
        ],
        independent_verification_context_digest=context_value[
            CONTEXT_DIGEST_FIELD
        ],
        requested_verification_operation_digest=context_value[
            "requested_verification_operation_digest"
        ],
        exact_verification_cycle_digest=context_value[
            "exact_verification_cycle_digest"
        ],
        verification_policy_digest=POLICY,
        verifyos_responsibility_digest=RESPONSIBILITY,
        verification_id=VERIFICATION_ID,
    )
    return build_verifyos_independent_evidence_verification(
        source_verification_handoff_receipt=source,
        expected_source_verification_handoff_receipt_digest=source[
            SOURCE_RECEIPT_DIGEST_FIELD
        ],
        independent_verification_evidence_bundle=evidence_value,
        expected_independent_verification_evidence_bundle_digest=evidence_value[
            EVIDENCE_DIGEST_FIELD
        ],
        independent_verification_execution=execution_value,
        expected_independent_verification_execution_digest=execution_value[
            EXECUTION_DIGEST_FIELD
        ],
        independent_verification_result_review=review_value,
        expected_independent_verification_result_review_digest=review_value[
            REVIEW_DIGEST_FIELD
        ],
        independent_verification_context=context_value,
        expected_independent_verification_context_digest=context_value[
            CONTEXT_DIGEST_FIELD
        ],
        verification_policy_digest=POLICY,
        verifyos_responsibility_digest=RESPONSIBILITY,
        verification_id=VERIFICATION_ID,
        verification_bundle_digest=verification_bundle,
    )


def run(value: dict):
    rebind(value)
    return build_current(value)


def assert_route(name: str, mutate, expected: str) -> None:
    value = fixture()
    mutate(value)
    result = run(value)
    assert result.status == STATUS_READY, (name, result.blockers)
    receipt = result.receipt
    assert receipt is not None
    assert receipt["verification_disposition"] == expected
    outcome_route = expected in {
        DISPOSITION_PASSED,
        DISPOSITION_FAILED,
        DISPOSITION_INDETERMINATE,
    }
    assert receipt["verification_completed"] is outcome_route
    assert receipt["verification_receipt_recorded"] is outcome_route
    if expected in {DISPOSITION_PASSED, DISPOSITION_FAILED}:
        assert receipt["verification_debt_open"] is False
        assert receipt["reobservation_required"] is False
    elif expected == DISPOSITION_INDETERMINATE:
        assert receipt["verification_debt_open"] is True
        assert receipt["reobservation_required"] is True
    else:
        assert receipt["verification_debt_open"] is True
        assert receipt["reobservation_required"] is False
    assert receipt["persistent_world_state_changed_by_verification"] is False
    assert receipt["world_disposition_candidate_generated"] is False
    assert receipt["tool_invocation_performed_by_kernel"] is False
    assert receipt["world_mutation_authority_granted"] is False
    assert receipt["execution_authority_granted"] is False
    assert receipt["generalized_truth_claimed"] is False
    assert receipt["causal_attribution_claimed"] is False
    assert receipt[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {
            key: item
            for key, item in receipt.items()
            if key != RECEIPT_DIGEST_FIELD
        }
    )


def set_failed(value: dict) -> None:
    value["execution"]["verification_outcome"] = OUTCOME_FAILED
    value["execution"]["successful_reproduction_attempts"] = 0
    value["execution"]["falsification_challenge_passed"] = False
    value["execution"]["acceptance_criteria_satisfied"] = False


def set_indeterminate(value: dict) -> None:
    value["evidence"]["evidence_conclusive"] = False
    value["execution"]["verification_outcome"] = OUTCOME_INDETERMINATE
    value["execution"]["completed_reproduction_attempts"] = 1
    value["execution"]["successful_reproduction_attempts"] = 0
    value["execution"]["acceptance_criteria_satisfied"] = False


def main() -> int:
    routes = (
        ("passed", lambda value: None, DISPOSITION_PASSED),
        ("failed", set_failed, DISPOSITION_FAILED),
        ("indeterminate", set_indeterminate, DISPOSITION_INDETERMINATE),
        (
            "source",
            lambda value: value["source"].__setitem__(
                "independent_verification_handoff_prepared", False
            ),
            DISPOSITION_SOURCE_REPAIR,
        ),
        (
            "correspondence",
            lambda value: value["evidence"].__setitem__(
                "source_correspondence_confirmed", False
            ),
            DISPOSITION_CORRESPONDENCE_REPAIR,
        ),
        (
            "independence",
            lambda value: value["review"].__setitem__(
                "verifier_independence_confirmed", False
            ),
            DISPOSITION_INDEPENDENCE_REPAIR,
        ),
        (
            "evidence",
            lambda value: value["evidence"].__setitem__(
                "evidence_integrity_confirmed", False
            ),
            DISPOSITION_EVIDENCE_REPAIR,
        ),
        (
            "protocol",
            lambda value: value["execution"].__setitem__(
                "falsification_challenge_executed", False
            ),
            DISPOSITION_PROTOCOL_REPAIR,
        ),
        (
            "reproduction",
            lambda value: value["review"].__setitem__(
                "reproduction_adequate", False
            ),
            DISPOSITION_REPRODUCTION_REPAIR,
        ),
        (
            "acceptance",
            lambda value: value["execution"].__setitem__(
                "acceptance_criteria_satisfied", False
            ),
            DISPOSITION_ACCEPTANCE_REPAIR,
        ),
        (
            "review",
            lambda value: value["review"].__setitem__("outcome_supported", False),
            DISPOSITION_REVIEW_REPAIR,
        ),
        (
            "replay",
            lambda value: value["context"]["prior_verification_session_ids"].append(
                value["context"]["verification_session_id"]
            ),
            DISPOSITION_REPLAY_REJECTED,
        ),
        (
            "mutation",
            lambda value: value["execution"].__setitem__(
                "current_state_mutation_performed", True
            ),
            DISPOSITION_CURRENT_STATE_MUTATION_REJECTED,
        ),
        (
            "authority",
            lambda value: value["execution"].__setitem__(
                "generalized_truth_claimed", True
            ),
            DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
        ),
    )
    for name, mutate, expected in routes:
        assert_route(name, mutate, expected)

    malformed = fixture()
    rebind(malformed)
    malformed["evidence"][EVIDENCE_DIGEST_FIELD] = "tampered"
    malformed_result = build_current(malformed)
    assert malformed_result.status == STATUS_BLOCKED
    assert malformed_result.receipt is None
    assert "independent_evidence_bundle_digest_mismatch" in malformed_result.blockers

    print(
        "PASS: VerifyOS v0.14 independent evidence verification "
        "validated all 14 disposition routes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
