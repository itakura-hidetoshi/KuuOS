from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_verifyos_dukkha_preserving_future_only_policy_activation_review_intake_v0_1 import *
from scripts.check_learnos_dukkha_preserving_future_only_maintenance_disposition_fixture_v0_1 import (
    build as build_learnos_v05,
)

def source():
    result = build_learnos_v05()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    return deepcopy(result.receipt)

def evidence(src):
    record = src["future_only_maintenance_disposition_record"]
    value = {
        "source_learnos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        "source_maintenance_disposition_evidence_packet_digest": src[SOURCE_EVIDENCE_DIGEST_FIELD],
        "source_maintenance_disposition_review_certificate_digest": src[SOURCE_REVIEW_DIGEST_FIELD],
        "source_maintenance_disposition_record_digest": src["future_only_maintenance_disposition_record_digest"],
        "source_maintenance_disposition_debt_consumption_record_digest": src["future_only_maintenance_disposition_debt_consumption_record_digest"],
        "source_policy_activation_review_handoff_envelope_digest": src["policy_activation_review_handoff_envelope_digest"],
        "world_candidate_fact_digest": src["world_candidate_fact_digest"],
        "world_candidate_relation_digest": src["world_candidate_relation_digest"],
        "resulting_world_state_digest": src["resulting_world_state_digest"],
        "resulting_world_revision": src["resulting_world_revision"],
        "future_only_learning_delta_digest": src["future_only_learning_delta_digest"],
        "maintenance_policy_candidate_digest": src["maintenance_policy_candidate_digest"],
        "future_only_maintenance_objective_digest": record["future_only_maintenance_objective_digest"],
        "maintenance_noop_threshold_digest": record["maintenance_noop_threshold_digest"],
        "maintenance_escalation_trigger_digest": record["maintenance_escalation_trigger_digest"],
        "reobservation_schedule_digest": record["reobservation_schedule_digest"],
        "proposed_activation_scope_digest": "verifyos-policy-activation-scope-v012-001",
        "activation_precondition_set_digest": "verifyos-policy-activation-preconditions-v012-001",
        "bounded_subject_scope_digest": "verifyos-policy-bounded-subject-scope-v012-001",
        "activation_duration_limit_digest": "verifyos-policy-activation-duration-v012-001",
        "rollback_plan_digest": "verifyos-policy-rollback-plan-v012-001",
        "post_activation_monitoring_guard_digest": "verifyos-policy-monitoring-guard-v012-001",
        "policy_activation_review_artifact_digests": [
            "verifyos-policy-activation-review-artifact-v012-001",
            "verifyos-policy-activation-review-artifact-v012-002",
        ],
        "uncertainty_digest": "verifyos-policy-activation-review-uncertainty-v012-001",
        "calibration_digest": "verifyos-policy-activation-review-calibration-v012-001",
        "provenance_chain_digests": sorted({
            src[SOURCE_RECEIPT_DIGEST_FIELD],
            src["future_only_maintenance_disposition_record_digest"],
            src["policy_activation_review_handoff_envelope_digest"],
            "verifyos-policy-activation-review-provenance-v012-001",
        }),
        "tamper_evidence_digest": "verifyos-policy-activation-review-tamper-v012-001",
        "protected_group_review_impact_digest": "verifyos-policy-activation-review-protected-v012-001",
        "future_subject_review_impact_digest": "verifyos-policy-activation-review-future-v012-001",
        "review_assessor_id": "verifyos-policy-activation-review-assessor-v012",
        "evidence_source_id": "independent-policy-activation-review-source-v012",
        "assessment_started_epoch": 162,
        "assessment_completed_epoch": 163,
        "maximum_assessment_duration": 4,
        "independent_policy_activation_review_evidence": True,
        "exactly_one_policy_activation_review": True,
        "maintenance_policy_candidate_activated": False,
        "maintenance_monitoring_activated": False,
        "maintenance_action_performed": False,
        "current_world_mutation_performed": False,
        "current_plan_revised": False,
        "current_policy_activated": False,
        "learning_delta_activated": False,
        "activation_authorization_granted": False,
        "generalized_benefit_claimed": False,
        "authority_escalation_claimed": False,
    }
    value[EVIDENCE_DIGEST_FIELD] = compute_future_only_policy_activation_review_evidence_packet_digest(value)
    return value

def review(src, ev):
    value = {
        "source_learnos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        EVIDENCE_DIGEST_FIELD: ev[EVIDENCE_DIGEST_FIELD],
        "source_maintenance_disposition_record_digest": src["future_only_maintenance_disposition_record_digest"],
        "source_policy_activation_review_handoff_envelope_digest": src["policy_activation_review_handoff_envelope_digest"],
        "world_candidate_fact_digest": ev["world_candidate_fact_digest"],
        "world_candidate_relation_digest": ev["world_candidate_relation_digest"],
        "resulting_world_state_digest": ev["resulting_world_state_digest"],
        "resulting_world_revision": ev["resulting_world_revision"],
        "future_only_learning_delta_digest": ev["future_only_learning_delta_digest"],
        "maintenance_policy_candidate_digest": ev["maintenance_policy_candidate_digest"],
        "reviewer_id": "verifyos-policy-activation-reviewer-v012",
        "review_method_digest": "verifyos-policy-activation-review-method-v012-001",
        "review_evidence_digest": "verifyos-policy-activation-review-evidence-v012-001",
        "review_started_epoch": 163,
        "review_completed_epoch": 164,
        "maximum_review_duration": 4,
        "source_receipt_correspondence_confirmed": True,
        "maintenance_disposition_record_correspondence_confirmed": True,
        "policy_activation_review_handoff_correspondence_confirmed": True,
        "maintenance_policy_candidate_correspondence_confirmed": True,
        "policy_activation_scope_exactly_bounded": True,
        "activation_preconditions_adequate": True,
        "rollback_plan_adequate": True,
        "post_activation_monitoring_guard_adequate": True,
        "uncertainty_adequate": True,
        "calibration_adequate": True,
        "provenance_continuity_preserved": True,
        "protected_group_nonexternalization_supported": True,
        "future_nonexternalization_supported": True,
        "no_current_state_mutation": True,
        "no_policy_activation": True,
        "no_activation_authorization_granted": True,
        "no_maintenance_action_performed": True,
        "no_authority_escalation": True,
    }
    value[REVIEW_DIGEST_FIELD] = compute_future_only_policy_activation_review_certificate_digest(value)
    return value

def context(src, ev, rv):
    source_epoch = src["future_only_maintenance_disposition_record"]["maintenance_disposition_intake_epoch"]
    value = {
        "source_learnos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        EVIDENCE_DIGEST_FIELD: ev[EVIDENCE_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: rv[REVIEW_DIGEST_FIELD],
        "current_world_model_state_digest": src["resulting_world_state_digest"],
        "current_world_model_revision": src["resulting_world_revision"],
        "current_future_only_learning_delta_digest": src["future_only_learning_delta_digest"],
        "current_maintenance_policy_candidate_digest": src["maintenance_policy_candidate_digest"],
        "current_maintenance_disposition_record_digest": src["future_only_maintenance_disposition_record_digest"],
        "source_maintenance_disposition_epoch": source_epoch,
        "policy_activation_review_intake_epoch": source_epoch + 4,
        "maximum_policy_activation_review_intake_delay": 12,
        "policy_activation_review_intake_session_id": "verifyos-policy-activation-review-v012-001",
        "policy_activation_review_intake_nonce_digest": "verifyos-policy-activation-review-nonce-v012-001",
        "prior_policy_activation_review_intake_session_ids": [],
        "prior_policy_activation_review_evidence_packet_digests": [],
        "prior_policy_activation_review_certificate_digests": [],
        "prior_policy_activation_review_intake_nonce_digests": [],
        "prior_policy_activation_review_source_receipt_digests": [],
        "requested_policy_activation_review_operation_digest": compute_requested_policy_activation_review_operation_digest(src, ev, rv),
        "exact_policy_activation_review_cycle_digest": "",
    }
    value["exact_policy_activation_review_cycle_digest"] = compute_exact_policy_activation_review_cycle_digest(src, ev, rv, value)
    value[CONTEXT_DIGEST_FIELD] = compute_future_only_policy_activation_review_intake_context_digest(value)
    return value

def redigest_evidence(value):
    value = deepcopy(value); value.pop(EVIDENCE_DIGEST_FIELD, None)
    value[EVIDENCE_DIGEST_FIELD] = compute_future_only_policy_activation_review_evidence_packet_digest(value)
    return value

def redigest_review(value, ev):
    value = deepcopy(value); value[EVIDENCE_DIGEST_FIELD] = ev[EVIDENCE_DIGEST_FIELD]
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = compute_future_only_policy_activation_review_certificate_digest(value)
    return value

def redigest_context(src, ev, rv, value):
    value = deepcopy(value)
    value[EVIDENCE_DIGEST_FIELD] = ev[EVIDENCE_DIGEST_FIELD]
    value[REVIEW_DIGEST_FIELD] = rv[REVIEW_DIGEST_FIELD]
    value["requested_policy_activation_review_operation_digest"] = compute_requested_policy_activation_review_operation_digest(src, ev, rv)
    value["exact_policy_activation_review_cycle_digest"] = compute_exact_policy_activation_review_cycle_digest(src, ev, rv, value)
    value.pop(CONTEXT_DIGEST_FIELD, None)
    value[CONTEXT_DIGEST_FIELD] = compute_future_only_policy_activation_review_intake_context_digest(value)
    return value

def build(**overrides):
    src = deepcopy(overrides.pop("source_learnos_receipt", None) or source())
    ev = deepcopy(overrides.pop("future_only_policy_activation_review_evidence_packet", None) or evidence(src))
    rv = deepcopy(overrides.pop("future_only_policy_activation_review_certificate", None) or review(src, ev))
    cx = deepcopy(overrides.pop("future_only_policy_activation_review_intake_context", None) or context(src, ev, rv))
    source_digest = src.get(SOURCE_RECEIPT_DIGEST_FIELD, "source-missing")
    evidence_digest = ev.get(EVIDENCE_DIGEST_FIELD, "evidence-missing")
    review_digest = rv.get(REVIEW_DIGEST_FIELD, "review-missing")
    context_digest = cx.get(CONTEXT_DIGEST_FIELD, "context-missing")
    expected_source = overrides.pop("expected_source_learnos_receipt_digest", source_digest)
    expected_evidence = overrides.pop("expected_future_only_policy_activation_review_evidence_packet_digest", evidence_digest)
    expected_review = overrides.pop("expected_future_only_policy_activation_review_certificate_digest", review_digest)
    expected_context = overrides.pop("expected_future_only_policy_activation_review_intake_context_digest", context_digest)
    policy = overrides.pop("future_only_policy_activation_review_policy_digest", "verifyos-future-only-policy-activation-review-policy-v012")
    responsibility = overrides.pop("verifyos_policy_review_responsibility_digest", "verifyos-policy-review-responsibility-v012")
    request = overrides.pop("future_only_policy_activation_review_request_id", "verifyos-policy-activation-review-v012-001")
    bundle = overrides.pop("future_only_policy_activation_review_bundle_digest",
        compute_future_only_policy_activation_review_bundle_digest(
            source_learnos_receipt_digest=source_digest,
            expected_source_learnos_receipt_digest=expected_source,
            source_maintenance_disposition_record_digest=src["future_only_maintenance_disposition_record_digest"],
            source_policy_activation_review_handoff_envelope_digest=src["policy_activation_review_handoff_envelope_digest"],
            future_only_policy_activation_review_evidence_packet_digest=evidence_digest,
            expected_future_only_policy_activation_review_evidence_packet_digest=expected_evidence,
            future_only_policy_activation_review_certificate_digest=review_digest,
            expected_future_only_policy_activation_review_certificate_digest=expected_review,
            future_only_policy_activation_review_intake_context_digest=context_digest,
            expected_future_only_policy_activation_review_intake_context_digest=expected_context,
            requested_policy_activation_review_operation_digest=cx["requested_policy_activation_review_operation_digest"],
            exact_policy_activation_review_cycle_digest=cx["exact_policy_activation_review_cycle_digest"],
            future_only_policy_activation_review_policy_digest=policy,
            verifyos_policy_review_responsibility_digest=responsibility,
            future_only_policy_activation_review_request_id=request,
        )
    )
    args = dict(
        source_learnos_receipt=src,
        expected_source_learnos_receipt_digest=expected_source,
        future_only_policy_activation_review_evidence_packet=ev,
        expected_future_only_policy_activation_review_evidence_packet_digest=expected_evidence,
        future_only_policy_activation_review_certificate=rv,
        expected_future_only_policy_activation_review_certificate_digest=expected_review,
        future_only_policy_activation_review_intake_context=cx,
        expected_future_only_policy_activation_review_intake_context_digest=expected_context,
        future_only_policy_activation_review_policy_digest=policy,
        verifyos_policy_review_responsibility_digest=responsibility,
        future_only_policy_activation_review_request_id=request,
        future_only_policy_activation_review_bundle_digest=bundle,
    )
    args.update(overrides)
    return build_verifyos_dukkha_preserving_future_only_policy_activation_review_intake(**args)
