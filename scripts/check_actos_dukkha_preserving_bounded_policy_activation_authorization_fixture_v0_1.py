from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_actos_dukkha_preserving_bounded_policy_activation_authorization_intake_v0_1 import *
from scripts.check_verifyos_dukkha_preserving_future_only_policy_activation_review_fixture_v0_1 import (
    build as build_verifyos_v012,
)


def source():
    result = build_verifyos_v012()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    return deepcopy(result.receipt)


def evidence(src):
    record = src["future_only_policy_activation_review_record"]
    value = {
        "source_verifyos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        "source_policy_activation_review_evidence_packet_digest": src[
            SOURCE_EVIDENCE_DIGEST_FIELD
        ],
        "source_policy_activation_review_certificate_digest": src[
            SOURCE_REVIEW_DIGEST_FIELD
        ],
        "source_policy_activation_review_record_digest": src[
            "future_only_policy_activation_review_record_digest"
        ],
        "source_policy_activation_review_debt_consumption_record_digest": src[
            "future_only_policy_activation_review_debt_consumption_record_digest"
        ],
        "source_activation_authorization_handoff_envelope_digest": src[
            "activation_authorization_handoff_envelope_digest"
        ],
        "world_candidate_fact_digest": src["world_candidate_fact_digest"],
        "world_candidate_relation_digest": src["world_candidate_relation_digest"],
        "resulting_world_state_digest": src["resulting_world_state_digest"],
        "resulting_world_revision": src["resulting_world_revision"],
        "future_only_learning_delta_digest": src["future_only_learning_delta_digest"],
        "maintenance_policy_candidate_digest": src[
            "maintenance_policy_candidate_digest"
        ],
        "reviewed_activation_scope_digest": record[
            "proposed_activation_scope_digest"
        ],
        "reviewed_activation_precondition_set_digest": record[
            "activation_precondition_set_digest"
        ],
        "reviewed_bounded_subject_scope_digest": record[
            "bounded_subject_scope_digest"
        ],
        "reviewed_activation_duration_limit_digest": record[
            "activation_duration_limit_digest"
        ],
        "reviewed_rollback_plan_digest": record["rollback_plan_digest"],
        "reviewed_post_activation_monitoring_guard_digest": record[
            "post_activation_monitoring_guard_digest"
        ],
        "authorization_scope_digest": record["proposed_activation_scope_digest"],
        "authorization_precondition_set_digest": record[
            "activation_precondition_set_digest"
        ],
        "authorization_subject_scope_digest": record[
            "bounded_subject_scope_digest"
        ],
        "authorization_duration_limit_digest": record[
            "activation_duration_limit_digest"
        ],
        "authorization_rollback_plan_digest": record["rollback_plan_digest"],
        "authorization_monitoring_guard_digest": record[
            "post_activation_monitoring_guard_digest"
        ],
        "single_use_authorization_lease_digest": (
            "actos-policy-activation-single-use-lease-v012-001"
        ),
        "authorization_effect_ceiling_digest": (
            "actos-policy-activation-effect-ceiling-v012-001"
        ),
        "authorization_artifact_digests": [
            "actos-policy-activation-authorization-artifact-v012-001",
            "actos-policy-activation-authorization-artifact-v012-002",
        ],
        "uncertainty_digest": (
            "actos-policy-activation-authorization-uncertainty-v012-001"
        ),
        "calibration_digest": (
            "actos-policy-activation-authorization-calibration-v012-001"
        ),
        "provenance_chain_digests": sorted(
            {
                src[SOURCE_RECEIPT_DIGEST_FIELD],
                src["future_only_policy_activation_review_record_digest"],
                src["activation_authorization_handoff_envelope_digest"],
                "actos-policy-activation-authorization-provenance-v012-001",
            }
        ),
        "tamper_evidence_digest": (
            "actos-policy-activation-authorization-tamper-v012-001"
        ),
        "protected_group_authorization_impact_digest": (
            "actos-policy-activation-authorization-protected-v012-001"
        ),
        "future_subject_authorization_impact_digest": (
            "actos-policy-activation-authorization-future-v012-001"
        ),
        "authorization_assessor_id": (
            "actos-policy-activation-authorization-assessor-v012"
        ),
        "evidence_source_id": (
            "independent-policy-activation-authorization-source-v012"
        ),
        "assessment_started_epoch": 166,
        "assessment_completed_epoch": 167,
        "maximum_assessment_duration": 4,
        "independent_activation_authorization_evidence": True,
        "exactly_one_activation_authorization_assessment": True,
        "single_use_authorization_requested": True,
        "maintenance_policy_candidate_activated": False,
        "maintenance_monitoring_activated": False,
        "maintenance_action_performed": False,
        "current_world_mutation_performed": False,
        "current_plan_revised": False,
        "current_policy_activated": False,
        "learning_delta_activated": False,
        "policy_activation_performed": False,
        "generalized_benefit_claimed": False,
        "authority_escalation_claimed": False,
    }
    value[EVIDENCE_DIGEST_FIELD] = (
        compute_bounded_policy_activation_authorization_evidence_packet_digest(
            value
        )
    )
    return value


def review(src, ev):
    value = {
        "source_verifyos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        EVIDENCE_DIGEST_FIELD: ev[EVIDENCE_DIGEST_FIELD],
        "source_policy_activation_review_record_digest": src[
            "future_only_policy_activation_review_record_digest"
        ],
        "source_activation_authorization_handoff_envelope_digest": src[
            "activation_authorization_handoff_envelope_digest"
        ],
        "world_candidate_fact_digest": ev["world_candidate_fact_digest"],
        "world_candidate_relation_digest": ev["world_candidate_relation_digest"],
        "resulting_world_state_digest": ev["resulting_world_state_digest"],
        "resulting_world_revision": ev["resulting_world_revision"],
        "future_only_learning_delta_digest": ev["future_only_learning_delta_digest"],
        "maintenance_policy_candidate_digest": ev[
            "maintenance_policy_candidate_digest"
        ],
        "reviewer_id": "actos-policy-activation-authorization-reviewer-v012",
        "review_method_digest": (
            "actos-policy-activation-authorization-review-method-v012-001"
        ),
        "review_evidence_digest": (
            "actos-policy-activation-authorization-review-evidence-v012-001"
        ),
        "review_started_epoch": 167,
        "review_completed_epoch": 168,
        "maximum_review_duration": 4,
        "source_receipt_correspondence_confirmed": True,
        "policy_activation_review_record_correspondence_confirmed": True,
        "activation_authorization_handoff_correspondence_confirmed": True,
        "maintenance_policy_candidate_correspondence_confirmed": True,
        "authorization_scope_exactly_bounded": True,
        "activation_preconditions_adequate": True,
        "single_use_authorization_adequate": True,
        "rollback_plan_adequate": True,
        "post_activation_monitoring_guard_adequate": True,
        "uncertainty_adequate": True,
        "calibration_adequate": True,
        "provenance_continuity_preserved": True,
        "protected_group_nonexternalization_supported": True,
        "future_nonexternalization_supported": True,
        "no_current_state_mutation": True,
        "no_policy_activation": True,
        "no_maintenance_action_performed": True,
        "no_authority_escalation": True,
    }
    value[REVIEW_DIGEST_FIELD] = (
        compute_bounded_policy_activation_authorization_review_certificate_digest(
            value
        )
    )
    return value


def context(src, ev, rv):
    source_epoch = src["future_only_policy_activation_review_record"][
        "policy_activation_review_intake_epoch"
    ]
    value = {
        "source_verifyos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        EVIDENCE_DIGEST_FIELD: ev[EVIDENCE_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: rv[REVIEW_DIGEST_FIELD],
        "current_world_model_state_digest": src["resulting_world_state_digest"],
        "current_world_model_revision": src["resulting_world_revision"],
        "current_future_only_learning_delta_digest": src[
            "future_only_learning_delta_digest"
        ],
        "current_maintenance_policy_candidate_digest": src[
            "maintenance_policy_candidate_digest"
        ],
        "current_policy_activation_review_record_digest": src[
            "future_only_policy_activation_review_record_digest"
        ],
        "source_policy_activation_review_epoch": source_epoch,
        "activation_authorization_intake_epoch": source_epoch + 4,
        "maximum_activation_authorization_intake_delay": 12,
        "activation_authorization_intake_session_id": (
            "actos-policy-activation-authorization-v012-001"
        ),
        "activation_authorization_intake_nonce_digest": (
            "actos-policy-activation-authorization-nonce-v012-001"
        ),
        "prior_activation_authorization_intake_session_ids": [],
        "prior_activation_authorization_evidence_packet_digests": [],
        "prior_activation_authorization_review_certificate_digests": [],
        "prior_activation_authorization_intake_nonce_digests": [],
        "prior_activation_authorization_source_receipt_digests": [],
        "requested_activation_authorization_operation_digest": (
            compute_requested_activation_authorization_operation_digest(
                src, ev, rv
            )
        ),
        "exact_activation_authorization_cycle_digest": "",
    }
    value["exact_activation_authorization_cycle_digest"] = (
        compute_exact_activation_authorization_cycle_digest(src, ev, rv, value)
    )
    value[CONTEXT_DIGEST_FIELD] = (
        compute_bounded_policy_activation_authorization_intake_context_digest(
            value
        )
    )
    return value


def redigest_evidence(value):
    value = deepcopy(value)
    value.pop(EVIDENCE_DIGEST_FIELD, None)
    value[EVIDENCE_DIGEST_FIELD] = (
        compute_bounded_policy_activation_authorization_evidence_packet_digest(
            value
        )
    )
    return value


def redigest_review(value, ev):
    value = deepcopy(value)
    value[EVIDENCE_DIGEST_FIELD] = ev[EVIDENCE_DIGEST_FIELD]
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = (
        compute_bounded_policy_activation_authorization_review_certificate_digest(
            value
        )
    )
    return value


def redigest_context(src, ev, rv, value):
    value = deepcopy(value)
    value[EVIDENCE_DIGEST_FIELD] = ev[EVIDENCE_DIGEST_FIELD]
    value[REVIEW_DIGEST_FIELD] = rv[REVIEW_DIGEST_FIELD]
    value["requested_activation_authorization_operation_digest"] = (
        compute_requested_activation_authorization_operation_digest(
            src, ev, rv
        )
    )
    value["exact_activation_authorization_cycle_digest"] = (
        compute_exact_activation_authorization_cycle_digest(
            src, ev, rv, value
        )
    )
    value.pop(CONTEXT_DIGEST_FIELD, None)
    value[CONTEXT_DIGEST_FIELD] = (
        compute_bounded_policy_activation_authorization_intake_context_digest(
            value
        )
    )
    return value


def build(**overrides):
    src = deepcopy(overrides.pop("source_verifyos_receipt", None) or source())
    ev = deepcopy(
        overrides.pop(
            "bounded_policy_activation_authorization_evidence_packet", None
        )
        or evidence(src)
    )
    rv = deepcopy(
        overrides.pop(
            "bounded_policy_activation_authorization_review_certificate", None
        )
        or review(src, ev)
    )
    cx = deepcopy(
        overrides.pop(
            "bounded_policy_activation_authorization_intake_context", None
        )
        or context(src, ev, rv)
    )

    source_digest = src.get(SOURCE_RECEIPT_DIGEST_FIELD, "source-missing")
    evidence_digest = ev.get(EVIDENCE_DIGEST_FIELD, "evidence-missing")
    review_digest = rv.get(REVIEW_DIGEST_FIELD, "review-missing")
    context_digest = cx.get(CONTEXT_DIGEST_FIELD, "context-missing")

    expected_source = overrides.pop(
        "expected_source_verifyos_receipt_digest",
        source_digest,
    )
    expected_evidence = overrides.pop(
        "expected_bounded_policy_activation_authorization_evidence_packet_digest",
        evidence_digest,
    )
    expected_review = overrides.pop(
        "expected_bounded_policy_activation_authorization_review_certificate_digest",
        review_digest,
    )
    expected_context = overrides.pop(
        "expected_bounded_policy_activation_authorization_intake_context_digest",
        context_digest,
    )
    policy = overrides.pop(
        "bounded_policy_activation_authorization_policy_digest",
        "actos-bounded-policy-activation-authorization-policy-v012",
    )
    responsibility = overrides.pop(
        "actos_policy_authorization_responsibility_digest",
        "actos-policy-authorization-responsibility-v012",
    )
    request = overrides.pop(
        "bounded_policy_activation_authorization_request_id",
        "actos-policy-activation-authorization-v012-001",
    )
    bundle = overrides.pop(
        "bounded_policy_activation_authorization_bundle_digest",
        compute_bounded_policy_activation_authorization_bundle_digest(
            source_verifyos_receipt_digest=source_digest,
            expected_source_verifyos_receipt_digest=expected_source,
            source_policy_activation_review_record_digest=src[
                "future_only_policy_activation_review_record_digest"
            ],
            source_activation_authorization_handoff_envelope_digest=src[
                "activation_authorization_handoff_envelope_digest"
            ],
            bounded_policy_activation_authorization_evidence_packet_digest=(
                evidence_digest
            ),
            expected_bounded_policy_activation_authorization_evidence_packet_digest=(
                expected_evidence
            ),
            bounded_policy_activation_authorization_review_certificate_digest=(
                review_digest
            ),
            expected_bounded_policy_activation_authorization_review_certificate_digest=(
                expected_review
            ),
            bounded_policy_activation_authorization_intake_context_digest=(
                context_digest
            ),
            expected_bounded_policy_activation_authorization_intake_context_digest=(
                expected_context
            ),
            requested_activation_authorization_operation_digest=cx[
                "requested_activation_authorization_operation_digest"
            ],
            exact_activation_authorization_cycle_digest=cx[
                "exact_activation_authorization_cycle_digest"
            ],
            bounded_policy_activation_authorization_policy_digest=policy,
            actos_policy_authorization_responsibility_digest=responsibility,
            bounded_policy_activation_authorization_request_id=request,
        ),
    )

    args = {
        "source_verifyos_receipt": src,
        "expected_source_verifyos_receipt_digest": expected_source,
        "bounded_policy_activation_authorization_evidence_packet": ev,
        "expected_bounded_policy_activation_authorization_evidence_packet_digest": (
            expected_evidence
        ),
        "bounded_policy_activation_authorization_review_certificate": rv,
        "expected_bounded_policy_activation_authorization_review_certificate_digest": (
            expected_review
        ),
        "bounded_policy_activation_authorization_intake_context": cx,
        "expected_bounded_policy_activation_authorization_intake_context_digest": (
            expected_context
        ),
        "bounded_policy_activation_authorization_policy_digest": policy,
        "actos_policy_authorization_responsibility_digest": responsibility,
        "bounded_policy_activation_authorization_request_id": request,
        "bounded_policy_activation_authorization_bundle_digest": bundle,
    }
    args.update(overrides)
    return (
        build_actos_dukkha_preserving_bounded_policy_activation_authorization_intake(
            **args
        )
    )
