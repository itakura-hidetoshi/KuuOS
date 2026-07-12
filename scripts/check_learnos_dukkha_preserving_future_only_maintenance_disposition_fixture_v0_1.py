from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_learnos_dukkha_preserving_future_only_maintenance_disposition_intake_v0_1 import *
from scripts.check_verifyos_dukkha_preserving_future_only_maintenance_monitoring_observation_verification_fixture_v0_1 import (
    build as build_verifyos_v011,
)


def source():
    result = build_verifyos_v011()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    return deepcopy(result.receipt)


def evidence(src):
    record = src["maintenance_monitoring_verification_record"]
    value = {
        "source_verifyos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        "source_monitoring_verification_evidence_packet_digest": src[SOURCE_EVIDENCE_DIGEST_FIELD],
        "source_monitoring_verification_review_certificate_digest": src[SOURCE_REVIEW_DIGEST_FIELD],
        "source_monitoring_verification_record_digest": src["maintenance_monitoring_verification_record_digest"],
        "source_monitoring_verification_debt_consumption_record_digest": src["maintenance_monitoring_verification_debt_consumption_record_digest"],
        "source_maintenance_disposition_handoff_envelope_digest": src["maintenance_disposition_handoff_envelope_digest"],
        "world_candidate_fact_digest": src["world_candidate_fact_digest"],
        "world_candidate_relation_digest": src["world_candidate_relation_digest"],
        "resulting_world_state_digest": src["resulting_world_state_digest"],
        "resulting_world_revision": src["resulting_world_revision"],
        "future_only_learning_delta_digest": src["future_only_learning_delta_digest"],
        "maintenance_policy_candidate_digest": src["maintenance_policy_candidate_digest"],
        "source_monitoring_observation_record_digest": src["source_maintenance_monitoring_observation_record_digest"],
        "verified_baseline_observation_digest": record["baseline_observation_digest"],
        "verified_durability_digest": record["durability_verification_digest"],
        "verified_adverse_effect_digest": record["adverse_effect_verification_digest"],
        "verified_distributional_digest": record["distributional_verification_digest"],
        "future_only_maintenance_objective_digest": "learnos-maintenance-objective-v05-001",
        "maintenance_noop_threshold_digest": "learnos-maintenance-noop-threshold-v05-001",
        "maintenance_escalation_trigger_digest": "learnos-maintenance-escalation-trigger-v05-001",
        "reobservation_schedule_digest": "learnos-maintenance-reobservation-schedule-v05-001",
        "evidence_retention_window_digest": "learnos-maintenance-retention-window-v05-001",
        "maintenance_disposition_artifact_digests": [
            "learnos-maintenance-disposition-artifact-v05-001",
            "learnos-maintenance-disposition-artifact-v05-002",
        ],
        "uncertainty_digest": "learnos-maintenance-disposition-uncertainty-v05-001",
        "calibration_digest": "learnos-maintenance-disposition-calibration-v05-001",
        "provenance_chain_digests": sorted(
            {
                src[SOURCE_RECEIPT_DIGEST_FIELD],
                src["maintenance_monitoring_verification_record_digest"],
                src["maintenance_disposition_handoff_envelope_digest"],
                "learnos-maintenance-disposition-provenance-v05-001",
            }
        ),
        "tamper_evidence_digest": "learnos-maintenance-disposition-tamper-v05-001",
        "protected_group_disposition_impact_digest": "learnos-maintenance-protected-impact-v05-001",
        "future_subject_disposition_impact_digest": "learnos-maintenance-future-impact-v05-001",
        "assessor_id": "learnos-maintenance-disposition-assessor-v05",
        "evidence_source_id": "independent-maintenance-disposition-source-v05",
        "assessment_started_epoch": 158,
        "assessment_completed_epoch": 159,
        "maximum_assessment_duration": 4,
        "independent_future_only_maintenance_disposition_evidence": True,
        "exactly_one_maintenance_disposition_assessment": True,
        "maintenance_policy_candidate_activated": False,
        "maintenance_monitoring_activated": False,
        "maintenance_action_performed": False,
        "current_world_mutation_performed": False,
        "current_plan_revised": False,
        "current_policy_activated": False,
        "learning_delta_activated": False,
        "generalized_benefit_claimed": False,
        "authority_escalation_claimed": False,
    }
    value[EVIDENCE_DIGEST_FIELD] = (
        compute_future_only_maintenance_disposition_evidence_packet_digest(value)
    )
    return value


def review(src, ev):
    value = {
        "source_verifyos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        EVIDENCE_DIGEST_FIELD: ev[EVIDENCE_DIGEST_FIELD],
        "source_monitoring_verification_record_digest": src["maintenance_monitoring_verification_record_digest"],
        "source_maintenance_disposition_handoff_envelope_digest": src["maintenance_disposition_handoff_envelope_digest"],
        "world_candidate_fact_digest": ev["world_candidate_fact_digest"],
        "world_candidate_relation_digest": ev["world_candidate_relation_digest"],
        "resulting_world_state_digest": ev["resulting_world_state_digest"],
        "resulting_world_revision": ev["resulting_world_revision"],
        "future_only_learning_delta_digest": ev["future_only_learning_delta_digest"],
        "maintenance_policy_candidate_digest": ev["maintenance_policy_candidate_digest"],
        "reviewer_id": "learnos-maintenance-disposition-reviewer-v05",
        "review_method_digest": "learnos-maintenance-disposition-review-method-v05-001",
        "review_evidence_digest": "learnos-maintenance-disposition-review-evidence-v05-001",
        "review_started_epoch": 159,
        "review_completed_epoch": 160,
        "maximum_review_duration": 4,
        "source_receipt_correspondence_confirmed": True,
        "monitoring_verification_record_correspondence_confirmed": True,
        "maintenance_disposition_handoff_correspondence_confirmed": True,
        "maintenance_policy_candidate_correspondence_confirmed": True,
        "maintenance_objective_adequate": True,
        "maintenance_noop_threshold_adequate": True,
        "maintenance_escalation_trigger_adequate": True,
        "reobservation_schedule_adequate": True,
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
        compute_future_only_maintenance_disposition_review_certificate_digest(value)
    )
    return value


def context(src, ev, rv):
    source_epoch = src["maintenance_monitoring_verification_record"][
        "monitoring_verification_intake_epoch"
    ]
    value = {
        "source_verifyos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        EVIDENCE_DIGEST_FIELD: ev[EVIDENCE_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: rv[REVIEW_DIGEST_FIELD],
        "current_world_model_state_digest": src["resulting_world_state_digest"],
        "current_world_model_revision": src["resulting_world_revision"],
        "current_future_only_learning_delta_digest": src["future_only_learning_delta_digest"],
        "current_maintenance_policy_candidate_digest": src["maintenance_policy_candidate_digest"],
        "source_monitoring_verification_epoch": source_epoch,
        "maintenance_disposition_intake_epoch": source_epoch + 4,
        "maximum_maintenance_disposition_intake_delay": 12,
        "maintenance_disposition_intake_session_id": "learnos-maintenance-disposition-v05-001",
        "maintenance_disposition_intake_nonce_digest": "learnos-maintenance-disposition-nonce-v05-001",
        "prior_maintenance_disposition_intake_session_ids": [],
        "prior_maintenance_disposition_evidence_packet_digests": [],
        "prior_maintenance_disposition_review_certificate_digests": [],
        "prior_maintenance_disposition_intake_nonce_digests": [],
        "prior_maintenance_disposition_source_receipt_digests": [],
        "requested_maintenance_disposition_operation_digest": (
            compute_requested_maintenance_disposition_operation_digest(src, ev, rv)
        ),
        "exact_maintenance_disposition_cycle_digest": "",
    }
    value["exact_maintenance_disposition_cycle_digest"] = (
        compute_exact_maintenance_disposition_cycle_digest(src, ev, rv, value)
    )
    value[CONTEXT_DIGEST_FIELD] = (
        compute_future_only_maintenance_disposition_intake_context_digest(value)
    )
    return value


def redigest_evidence(value):
    value = deepcopy(value)
    value.pop(EVIDENCE_DIGEST_FIELD, None)
    value[EVIDENCE_DIGEST_FIELD] = (
        compute_future_only_maintenance_disposition_evidence_packet_digest(value)
    )
    return value


def redigest_review(value, ev):
    value = deepcopy(value)
    value[EVIDENCE_DIGEST_FIELD] = ev[EVIDENCE_DIGEST_FIELD]
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = (
        compute_future_only_maintenance_disposition_review_certificate_digest(value)
    )
    return value


def redigest_context(src, ev, rv, value):
    value = deepcopy(value)
    value[EVIDENCE_DIGEST_FIELD] = ev[EVIDENCE_DIGEST_FIELD]
    value[REVIEW_DIGEST_FIELD] = rv[REVIEW_DIGEST_FIELD]
    value["requested_maintenance_disposition_operation_digest"] = (
        compute_requested_maintenance_disposition_operation_digest(src, ev, rv)
    )
    value["exact_maintenance_disposition_cycle_digest"] = (
        compute_exact_maintenance_disposition_cycle_digest(src, ev, rv, value)
    )
    value.pop(CONTEXT_DIGEST_FIELD, None)
    value[CONTEXT_DIGEST_FIELD] = (
        compute_future_only_maintenance_disposition_intake_context_digest(value)
    )
    return value


def build(**overrides):
    src = deepcopy(overrides.pop("source_verifyos_receipt", None) or source())
    ev = deepcopy(
        overrides.pop("future_only_maintenance_disposition_evidence_packet", None)
        or evidence(src)
    )
    rv = deepcopy(
        overrides.pop("future_only_maintenance_disposition_review_certificate", None)
        or review(src, ev)
    )
    cx = deepcopy(
        overrides.pop("future_only_maintenance_disposition_intake_context", None)
        or context(src, ev, rv)
    )

    source_digest = src.get(SOURCE_RECEIPT_DIGEST_FIELD, "source-missing")
    evidence_digest = ev.get(EVIDENCE_DIGEST_FIELD, "evidence-missing")
    review_digest = rv.get(REVIEW_DIGEST_FIELD, "review-missing")
    context_digest = cx.get(CONTEXT_DIGEST_FIELD, "context-missing")

    expected_source = overrides.pop(
        "expected_source_verifyos_receipt_digest", source_digest
    )
    expected_evidence = overrides.pop(
        "expected_future_only_maintenance_disposition_evidence_packet_digest",
        evidence_digest,
    )
    expected_review = overrides.pop(
        "expected_future_only_maintenance_disposition_review_certificate_digest",
        review_digest,
    )
    expected_context = overrides.pop(
        "expected_future_only_maintenance_disposition_intake_context_digest",
        context_digest,
    )
    policy = overrides.pop(
        "future_only_maintenance_disposition_policy_digest",
        "learnos-future-only-maintenance-disposition-policy-v05",
    )
    responsibility = overrides.pop(
        "learnos_maintenance_responsibility_digest",
        "learnos-maintenance-responsibility-v05",
    )
    request = overrides.pop(
        "future_only_maintenance_disposition_request_id",
        "learnos-maintenance-disposition-v05-001",
    )
    bundle = overrides.pop(
        "future_only_maintenance_disposition_bundle_digest",
        compute_future_only_maintenance_disposition_bundle_digest(
            source_verifyos_receipt_digest=source_digest,
            expected_source_verifyos_receipt_digest=expected_source,
            source_monitoring_verification_record_digest=src[
                "maintenance_monitoring_verification_record_digest"
            ],
            source_maintenance_disposition_handoff_envelope_digest=src[
                "maintenance_disposition_handoff_envelope_digest"
            ],
            future_only_maintenance_disposition_evidence_packet_digest=evidence_digest,
            expected_future_only_maintenance_disposition_evidence_packet_digest=expected_evidence,
            future_only_maintenance_disposition_review_certificate_digest=review_digest,
            expected_future_only_maintenance_disposition_review_certificate_digest=expected_review,
            future_only_maintenance_disposition_intake_context_digest=context_digest,
            expected_future_only_maintenance_disposition_intake_context_digest=expected_context,
            requested_maintenance_disposition_operation_digest=cx[
                "requested_maintenance_disposition_operation_digest"
            ],
            exact_maintenance_disposition_cycle_digest=cx[
                "exact_maintenance_disposition_cycle_digest"
            ],
            future_only_maintenance_disposition_policy_digest=policy,
            learnos_maintenance_responsibility_digest=responsibility,
            future_only_maintenance_disposition_request_id=request,
        ),
    )

    args = dict(
        source_verifyos_receipt=src,
        expected_source_verifyos_receipt_digest=expected_source,
        future_only_maintenance_disposition_evidence_packet=ev,
        expected_future_only_maintenance_disposition_evidence_packet_digest=expected_evidence,
        future_only_maintenance_disposition_review_certificate=rv,
        expected_future_only_maintenance_disposition_review_certificate_digest=expected_review,
        future_only_maintenance_disposition_intake_context=cx,
        expected_future_only_maintenance_disposition_intake_context_digest=expected_context,
        future_only_maintenance_disposition_policy_digest=policy,
        learnos_maintenance_responsibility_digest=responsibility,
        future_only_maintenance_disposition_request_id=request,
        future_only_maintenance_disposition_bundle_digest=bundle,
    )
    args.update(overrides)
    return build_learnos_dukkha_preserving_future_only_maintenance_disposition_intake(
        **args
    )
