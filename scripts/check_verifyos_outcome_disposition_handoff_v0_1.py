#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_observeos_sequential_epistemic_observability_common_v0_1 import (
    STATUS_BLOCKED,
    STATUS_READY,
    canonical_digest,
)
from runtime.kuuos_verifyos_independent_evidence_verification_v0_1 import (
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_verifyos_outcome_disposition_handoff_v0_1 import (
    CANDIDATE_ADOPT,
    CANDIDATE_DEFER,
    CANDIDATE_REJECT,
    CANDIDATE_REOBSERVE,
    CONTEXT_DIGEST_FIELD,
    DISPOSITION_ADOPT,
    DISPOSITION_APPEAL_REPAIR,
    DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
    DISPOSITION_AUTHORITY_REVIEW_REPAIR,
    DISPOSITION_CURRENT_STATE_MUTATION_REJECTED,
    DISPOSITION_DEBT_REPAIR,
    DISPOSITION_DEFER,
    DISPOSITION_EVIDENCE_REPAIR,
    DISPOSITION_OUTCOME_REPAIR,
    DISPOSITION_REJECT,
    DISPOSITION_REOBSERVE,
    DISPOSITION_REPLAY_REJECTED,
    DISPOSITION_SOURCE_REPAIR,
    DISPOSITION_WINDOW_REPAIR,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    build_verifyos_outcome_disposition_handoff,
    compute_exact_disposition_cycle_digest as cycle_digest,
    compute_outcome_disposition_bundle_digest as bundle_digest,
    compute_outcome_disposition_context_digest as context_digest,
    compute_outcome_disposition_request_digest as request_digest,
    compute_outcome_disposition_review_digest as review_digest,
    compute_requested_disposition_operation_digest as operation_digest,
)
from scripts.check_verifyos_independent_evidence_verification_v0_1 import (
    fixture as verification_fixture,
    run as run_verification,
    set_failed,
    set_indeterminate,
)

POLICY = "verifyos-v0-15-disposition-policy"
RESPONSIBILITY = "verifyos-v0-15-responsibility"
HANDOFF_ID = "outcome-disposition-handoff-001"


def source_receipt(outcome: str) -> dict:
    value = verification_fixture()
    if outcome == "failed":
        set_failed(value)
    elif outcome == "indeterminate":
        set_indeterminate(value)
    result = run_verification(value)
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    return deepcopy(result.receipt)


def request(source: dict, candidate: str) -> dict:
    indeterminate = source["verification_outcome"] == "indeterminate"
    value = {
        "source_verification_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "source_verification_outcome": source["verification_outcome"],
        "requested_disposition_candidate": candidate,
        "disposition_authority_source_digest": "governance-authority-source-a",
        "disposition_policy_digest": POLICY,
        "governance_review_route_digest": "governance-review-route-a",
        "appeal_review_route_digest": "appeal-review-route-a",
        "evidence_preservation_digest": "evidence-preservation-a",
        "source_evidence_artifact_digests": source[
            "independent_evidence_artifact_digests"
        ],
        "reobservation_scope_digests": (
            ["reobserve-calibration", "reobserve-shift"]
            if candidate == CANDIDATE_REOBSERVE
            else []
        ),
        "preserve_verification_debt": indeterminate,
        "requester_id": "disposition-requester-a",
        "request_created_epoch": 300,
        "request_expires_epoch": 320,
        "maximum_request_duration": 30,
        "current_state_mutation_requested": False,
        "policy_activation_requested": False,
        "execution_requested": False,
        "generalized_truth_claimed": False,
        "causal_attribution_claimed": False,
    }
    value[REQUEST_DIGEST_FIELD] = request_digest(value)
    return value


def review(source: dict, request_value: dict) -> dict:
    value = {
        "source_verification_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        REQUEST_DIGEST_FIELD: request_value[REQUEST_DIGEST_FIELD],
        "reviewer_id": "disposition-reviewer-b",
        "reviewer_independence_confirmed": True,
        "outcome_correspondence_confirmed": True,
        "authority_source_adequate": True,
        "evidence_preservation_confirmed": True,
        "appeal_route_confirmed": True,
        "open_debt_preserved": source["verification_debt_open"],
        "world_mutation_not_authorized": True,
        "policy_activation_not_authorized": True,
        "execution_not_authorized": True,
        "no_truth_claim": True,
        "no_causal_claim": True,
        "review_started_epoch": 301,
        "review_completed_epoch": 305,
        "maximum_review_duration": 10,
    }
    value[REVIEW_DIGEST_FIELD] = review_digest(value)
    return value


def context(source: dict, request_value: dict, review_value: dict) -> dict:
    value = {
        "source_verification_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        REQUEST_DIGEST_FIELD: request_value[REQUEST_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: review_value[REVIEW_DIGEST_FIELD],
        "source_world_revision": source["resulting_world_revision"],
        "current_world_revision": source["resulting_world_revision"],
        "disposition_session_id": "disposition-session-a",
        "disposition_nonce_digest": "disposition-nonce-a",
        "prior_disposition_session_ids": [],
        "prior_disposition_nonce_digests": [],
        "prior_disposition_request_digests": [],
        "prior_disposition_receipt_digests": [],
    }
    value["requested_disposition_operation_digest"] = operation_digest(
        source, request_value, review_value
    )
    value["exact_disposition_cycle_digest"] = cycle_digest(
        source, request_value, review_value, value
    )
    value[CONTEXT_DIGEST_FIELD] = context_digest(value)
    return value


def fixture(outcome: str = "passed", candidate: str = CANDIDATE_ADOPT) -> dict:
    source = source_receipt(outcome)
    request_value = request(source, candidate)
    review_value = review(source, request_value)
    context_value = context(source, request_value, review_value)
    return {
        "source": source,
        "request": request_value,
        "review": review_value,
        "context": context_value,
    }


def rebind(value: dict) -> None:
    source = value["source"]
    request_value = value["request"]
    review_value = value["review"]
    context_value = value["context"]

    source.pop(SOURCE_RECEIPT_DIGEST_FIELD, None)
    source[SOURCE_RECEIPT_DIGEST_FIELD] = canonical_digest(source)

    request_value.update(
        {
            "source_verification_receipt_digest": source[
                SOURCE_RECEIPT_DIGEST_FIELD
            ],
            "source_verification_outcome": source["verification_outcome"],
            "disposition_policy_digest": POLICY,
            "source_evidence_artifact_digests": source[
                "independent_evidence_artifact_digests"
            ],
        }
    )
    request_value.pop(REQUEST_DIGEST_FIELD, None)
    request_value[REQUEST_DIGEST_FIELD] = request_digest(request_value)

    review_value.update(
        {
            "source_verification_receipt_digest": source[
                SOURCE_RECEIPT_DIGEST_FIELD
            ],
            REQUEST_DIGEST_FIELD: request_value[REQUEST_DIGEST_FIELD],
        }
    )
    review_value.pop(REVIEW_DIGEST_FIELD, None)
    review_value[REVIEW_DIGEST_FIELD] = review_digest(review_value)

    context_value.update(
        {
            "source_verification_receipt_digest": source[
                SOURCE_RECEIPT_DIGEST_FIELD
            ],
            REQUEST_DIGEST_FIELD: request_value[REQUEST_DIGEST_FIELD],
            REVIEW_DIGEST_FIELD: review_value[REVIEW_DIGEST_FIELD],
            "source_world_revision": source["resulting_world_revision"],
        }
    )
    context_value["requested_disposition_operation_digest"] = operation_digest(
        source, request_value, review_value
    )
    context_value["exact_disposition_cycle_digest"] = cycle_digest(
        source, request_value, review_value, context_value
    )
    context_value.pop(CONTEXT_DIGEST_FIELD, None)
    context_value[CONTEXT_DIGEST_FIELD] = context_digest(context_value)


def build_current(value: dict):
    source = value["source"]
    request_value = value["request"]
    review_value = value["review"]
    context_value = value["context"]
    disposition_bundle = bundle_digest(
        source_verification_receipt_digest=source[SOURCE_RECEIPT_DIGEST_FIELD],
        outcome_disposition_request_digest=request_value[REQUEST_DIGEST_FIELD],
        outcome_disposition_review_digest=review_value[REVIEW_DIGEST_FIELD],
        outcome_disposition_context_digest=context_value[CONTEXT_DIGEST_FIELD],
        requested_disposition_operation_digest=context_value[
            "requested_disposition_operation_digest"
        ],
        exact_disposition_cycle_digest=context_value["exact_disposition_cycle_digest"],
        disposition_policy_digest=POLICY,
        verifyos_responsibility_digest=RESPONSIBILITY,
        disposition_handoff_id=HANDOFF_ID,
    )
    return build_verifyos_outcome_disposition_handoff(
        source_verification_receipt=source,
        expected_source_verification_receipt_digest=source[
            SOURCE_RECEIPT_DIGEST_FIELD
        ],
        outcome_disposition_request=request_value,
        expected_outcome_disposition_request_digest=request_value[
            REQUEST_DIGEST_FIELD
        ],
        outcome_disposition_review=review_value,
        expected_outcome_disposition_review_digest=review_value[
            REVIEW_DIGEST_FIELD
        ],
        outcome_disposition_context=context_value,
        expected_outcome_disposition_context_digest=context_value[
            CONTEXT_DIGEST_FIELD
        ],
        disposition_policy_digest=POLICY,
        verifyos_responsibility_digest=RESPONSIBILITY,
        disposition_handoff_id=HANDOFF_ID,
        disposition_bundle_digest=disposition_bundle,
    )


def run(value: dict):
    rebind(value)
    return build_current(value)


def assert_route(name: str, value: dict, expected: str) -> None:
    result = run(value)
    assert result.status == STATUS_READY, (name, result.blockers)
    receipt = result.receipt
    assert receipt is not None
    assert receipt["outcome_disposition_handoff_disposition"] == expected

    candidate_route = expected in {
        DISPOSITION_ADOPT,
        DISPOSITION_REJECT,
        DISPOSITION_DEFER,
        DISPOSITION_REOBSERVE,
    }
    assert receipt["outcome_disposition_handoff_prepared"] is candidate_route
    assert receipt["world_disposition_candidate_generated"] is candidate_route
    assert receipt["world_disposition_completed"] is False
    assert receipt["world_commit_ready"] is False
    assert receipt["persistent_world_state_changed_by_handoff"] is False
    assert receipt["tool_invocation_performed_by_kernel"] is False
    assert receipt["external_side_effect_performed_by_kernel"] is False
    assert receipt["world_adoption_authority_granted"] is False
    assert receipt["world_rejection_authority_granted"] is False
    assert receipt["world_mutation_authority_granted"] is False
    assert receipt["policy_activation_authority_granted"] is False
    assert receipt["execution_authority_granted"] is False
    assert receipt["observation_execution_authority_granted"] is False
    assert receipt["generalized_truth_claimed"] is False
    assert receipt["causal_attribution_claimed"] is False
    assert receipt[RECEIPT_DIGEST_FIELD] == canonical_digest(
        {
            key: item
            for key, item in receipt.items()
            if key != RECEIPT_DIGEST_FIELD
        }
    )


def main() -> int:
    assert_route("adopt", fixture(), DISPOSITION_ADOPT)
    assert_route("reject", fixture("failed", CANDIDATE_REJECT), DISPOSITION_REJECT)
    assert_route(
        "defer", fixture("indeterminate", CANDIDATE_DEFER), DISPOSITION_DEFER
    )
    assert_route(
        "reobserve",
        fixture("indeterminate", CANDIDATE_REOBSERVE),
        DISPOSITION_REOBSERVE,
    )

    value = fixture()
    value["source"]["verification_completed"] = False
    assert_route("source", value, DISPOSITION_SOURCE_REPAIR)

    value = fixture()
    value["request"]["requested_disposition_candidate"] = CANDIDATE_REJECT
    assert_route("outcome", value, DISPOSITION_OUTCOME_REPAIR)

    value = fixture()
    value["review"]["authority_source_adequate"] = False
    assert_route("authority-review", value, DISPOSITION_AUTHORITY_REVIEW_REPAIR)

    value = fixture()
    value["review"]["evidence_preservation_confirmed"] = False
    assert_route("evidence", value, DISPOSITION_EVIDENCE_REPAIR)

    value = fixture("failed", CANDIDATE_REJECT)
    value["review"]["appeal_route_confirmed"] = False
    assert_route("appeal", value, DISPOSITION_APPEAL_REPAIR)

    value = fixture("indeterminate", CANDIDATE_DEFER)
    value["request"]["preserve_verification_debt"] = False
    assert_route("debt", value, DISPOSITION_DEBT_REPAIR)

    value = fixture()
    value["request"]["request_expires_epoch"] = 400
    assert_route("window", value, DISPOSITION_WINDOW_REPAIR)

    value = fixture()
    value["context"]["prior_disposition_session_ids"].append(
        value["context"]["disposition_session_id"]
    )
    assert_route("replay", value, DISPOSITION_REPLAY_REJECTED)

    value = fixture()
    value["request"]["current_state_mutation_requested"] = True
    assert_route("mutation", value, DISPOSITION_CURRENT_STATE_MUTATION_REJECTED)

    value = fixture()
    value["request"]["generalized_truth_claimed"] = True
    assert_route("authority", value, DISPOSITION_AUTHORITY_ESCALATION_REJECTED)

    malformed = fixture()
    rebind(malformed)
    malformed["request"][REQUEST_DIGEST_FIELD] = "tampered"
    malformed_result = build_current(malformed)
    assert malformed_result.status == STATUS_BLOCKED
    assert malformed_result.receipt is None
    assert "disposition_request_digest_mismatch" in malformed_result.blockers

    print(
        "PASS: VerifyOS v0.15 outcome disposition handoff "
        "validated all 14 disposition routes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
