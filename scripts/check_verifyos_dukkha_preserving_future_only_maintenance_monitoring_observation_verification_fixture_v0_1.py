from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_verifyos_dukkha_preserving_future_only_maintenance_monitoring_observation_verification_intake_v0_1 import *
from scripts.check_observeos_dukkha_preserving_future_only_maintenance_monitoring_observation_fixture_v0_1 import (
    build as build_observeos_v06,
)


def source():
    result = build_observeos_v06()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    return deepcopy(result.receipt)


def evidence(src):
    handoff = src["maintenance_monitoring_verification_handoff_envelope"]
    value = {
        "source_observeos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        "source_maintenance_monitoring_observation_evidence_packet_digest": src[SOURCE_EVIDENCE_DIGEST_FIELD],
        "source_maintenance_monitoring_observation_review_certificate_digest": src[SOURCE_REVIEW_DIGEST_FIELD],
        "source_maintenance_monitoring_observation_record_digest": src["maintenance_monitoring_observation_record_digest"],
        "source_maintenance_monitoring_observation_debt_consumption_record_digest": src["maintenance_monitoring_observation_debt_consumption_record_digest"],
        "source_maintenance_monitoring_verification_handoff_envelope_digest": src["maintenance_monitoring_verification_handoff_envelope_digest"],
        "world_candidate_fact_digest": src["world_candidate_fact_digest"],
        "world_candidate_relation_digest": src["world_candidate_relation_digest"],
        "resulting_world_state_digest": src["resulting_world_state_digest"],
        "resulting_world_revision": src["resulting_world_revision"],
        "future_only_learning_delta_digest": src["future_only_learning_delta_digest"],
        "maintenance_policy_candidate_digest": src["maintenance_policy_candidate_digest"],
        "baseline_observation_digest": handoff["baseline_observation_digest"],
        "durability_observation_digest": handoff["durability_observation_digest"],
        "adverse_effect_observation_digest": handoff["adverse_effect_observation_digest"],
        "distributional_observation_digest": handoff["distributional_observation_digest"],
        "observation_record_correspondence_digest": "verifyos-monitoring-observation-record-correspondence-v011-001",
        "maintenance_window_verification_digest": "verifyos-maintenance-window-verification-v011-001",
        "durability_verification_digest": "verifyos-durability-verification-v011-001",
        "adverse_effect_verification_digest": "verifyos-adverse-effect-verification-v011-001",
        "distributional_verification_digest": "verifyos-distributional-verification-v011-001",
        "reobservation_trigger_verification_digest": "verifyos-reobservation-trigger-verification-v011-001",
        "verification_artifact_digests": [
            "verifyos-monitoring-verification-artifact-v011-001",
            "verifyos-monitoring-verification-artifact-v011-002",
        ],
        "uncertainty_digest": "verifyos-monitoring-verification-uncertainty-v011-001",
        "calibration_digest": "verifyos-monitoring-verification-calibration-v011-001",
        "provenance_chain_digests": sorted(
            {
                src[SOURCE_RECEIPT_DIGEST_FIELD],
                src["maintenance_monitoring_observation_record_digest"],
                src["maintenance_monitoring_verification_handoff_envelope_digest"],
                "verifyos-monitoring-verification-provenance-v011-001",
            }
        ),
        "tamper_evidence_digest": "verifyos-monitoring-verification-tamper-v011-001",
        "protected_group_verification_impact_digest": "verifyos-monitoring-protected-impact-v011-001",
        "future_subject_verification_impact_digest": "verifyos-monitoring-future-impact-v011-001",
        "verifier_id": "verifyos-monitoring-verifier-v011",
        "evidence_source_id": "independent-monitoring-verification-source-v011",
        "verification_started_epoch": 154,
        "verification_completed_epoch": 155,
        "maximum_verification_duration": 4,
        "independent_maintenance_monitoring_verification_evidence": True,
        "exactly_one_monitoring_verification": True,
        "observation_recollected": False,
        "maintenance_action_performed": False,
        "current_world_mutation_performed": False,
        "current_plan_revised": False,
        "current_policy_activated": False,
        "learning_delta_activated": False,
        "generalized_benefit_claimed": False,
        "authority_escalation_claimed": False,
    }
    value[EVIDENCE_DIGEST_FIELD] = (
        compute_maintenance_monitoring_verification_evidence_packet_digest(value)
    )
    return value


def review(src, ev):
    value = {
        "source_observeos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        EVIDENCE_DIGEST_FIELD: ev[EVIDENCE_DIGEST_FIELD],
        "source_maintenance_monitoring_observation_record_digest": src["maintenance_monitoring_observation_record_digest"],
        "source_maintenance_monitoring_verification_handoff_envelope_digest": src["maintenance_monitoring_verification_handoff_envelope_digest"],
        "world_candidate_fact_digest": ev["world_candidate_fact_digest"],
        "world_candidate_relation_digest": ev["world_candidate_relation_digest"],
        "resulting_world_state_digest": ev["resulting_world_state_digest"],
        "resulting_world_revision": ev["resulting_world_revision"],
        "future_only_learning_delta_digest": ev["future_only_learning_delta_digest"],
        "maintenance_policy_candidate_digest": ev["maintenance_policy_candidate_digest"],
        "reviewer_id": "verifyos-monitoring-verification-reviewer-v011",
        "review_method_digest": "verifyos-monitoring-verification-review-method-v011-001",
        "review_evidence_digest": "verifyos-monitoring-verification-review-evidence-v011-001",
        "review_started_epoch": 155,
        "review_completed_epoch": 156,
        "maximum_review_duration": 4,
        "source_receipt_correspondence_confirmed": True,
        "observation_record_correspondence_confirmed": True,
        "verification_handoff_correspondence_confirmed": True,
        "baseline_observation_correspondence_confirmed": True,
        "durability_verification_adequate": True,
        "adverse_effect_verification_adequate": True,
        "distributional_verification_adequate": True,
        "reobservation_trigger_verification_adequate": True,
        "uncertainty_adequate": True,
        "calibration_adequate": True,
        "provenance_continuity_preserved": True,
        "protected_group_nonexternalization_supported": True,
        "future_nonexternalization_supported": True,
        "no_current_state_mutation": True,
        "no_maintenance_action_performed": True,
        "no_authority_escalation": True,
    }
    value[REVIEW_DIGEST_FIELD] = (
        compute_maintenance_monitoring_verification_review_certificate_digest(value)
    )
    return value


def context(src, ev, rv):
    source_epoch = src["maintenance_monitoring_observation_record"][
        "monitoring_observation_intake_epoch"
    ]
    value = {
        "source_observeos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        EVIDENCE_DIGEST_FIELD: ev[EVIDENCE_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: rv[REVIEW_DIGEST_FIELD],
        "current_world_model_state_digest": src["resulting_world_state_digest"],
        "current_world_model_revision": src["resulting_world_revision"],
        "current_future_only_learning_delta_digest": src["future_only_learning_delta_digest"],
        "current_maintenance_policy_candidate_digest": src["maintenance_policy_candidate_digest"],
        "source_monitoring_observation_epoch": source_epoch,
        "monitoring_verification_intake_epoch": source_epoch + 4,
        "maximum_monitoring_verification_intake_delay": 12,
        "monitoring_verification_intake_session_id": "verifyos-monitoring-verification-v011-001",
        "monitoring_verification_intake_nonce_digest": "verifyos-monitoring-verification-nonce-v011-001",
        "prior_monitoring_verification_intake_session_ids": [],
        "prior_monitoring_verification_evidence_packet_digests": [],
        "prior_monitoring_verification_review_certificate_digests": [],
        "prior_monitoring_verification_intake_nonce_digests": [],
        "prior_monitoring_verification_source_receipt_digests": [],
        "requested_monitoring_verification_operation_digest": (
            compute_requested_monitoring_verification_operation_digest(src, ev, rv)
        ),
        "exact_monitoring_verification_cycle_digest": "",
    }
    value["exact_monitoring_verification_cycle_digest"] = (
        compute_exact_monitoring_verification_cycle_digest(src, ev, rv, value)
    )
    value[CONTEXT_DIGEST_FIELD] = (
        compute_maintenance_monitoring_verification_intake_context_digest(value)
    )
    return value


def redigest_evidence(value):
    value = deepcopy(value)
    value.pop(EVIDENCE_DIGEST_FIELD, None)
    value[EVIDENCE_DIGEST_FIELD] = (
        compute_maintenance_monitoring_verification_evidence_packet_digest(value)
    )
    return value


def redigest_review(value, ev):
    value = deepcopy(value)
    value[EVIDENCE_DIGEST_FIELD] = ev[EVIDENCE_DIGEST_FIELD]
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = (
        compute_maintenance_monitoring_verification_review_certificate_digest(value)
    )
    return value


def redigest_context(src, ev, rv, value):
    value = deepcopy(value)
    value[EVIDENCE_DIGEST_FIELD] = ev[EVIDENCE_DIGEST_FIELD]
    value[REVIEW_DIGEST_FIELD] = rv[REVIEW_DIGEST_FIELD]
    value["requested_monitoring_verification_operation_digest"] = (
        compute_requested_monitoring_verification_operation_digest(src, ev, rv)
    )
    value["exact_monitoring_verification_cycle_digest"] = (
        compute_exact_monitoring_verification_cycle_digest(src, ev, rv, value)
    )
    value.pop(CONTEXT_DIGEST_FIELD, None)
    value[CONTEXT_DIGEST_FIELD] = (
        compute_maintenance_monitoring_verification_intake_context_digest(value)
    )
    return value


def build(**overrides):
    src = deepcopy(overrides.pop("source_observeos_receipt", None) or source())
    ev = deepcopy(
        overrides.pop("maintenance_monitoring_verification_evidence_packet", None)
        or evidence(src)
    )
    rv = deepcopy(
        overrides.pop("maintenance_monitoring_verification_review_certificate", None)
        or review(src, ev)
    )
    cx = deepcopy(
        overrides.pop("maintenance_monitoring_verification_intake_context", None)
        or context(src, ev, rv)
    )

    source_digest = src.get(SOURCE_RECEIPT_DIGEST_FIELD, "source-missing")
    evidence_digest = ev.get(EVIDENCE_DIGEST_FIELD, "evidence-missing")
    review_digest = rv.get(REVIEW_DIGEST_FIELD, "review-missing")
    context_digest = cx.get(CONTEXT_DIGEST_FIELD, "context-missing")

    expected_source = overrides.pop(
        "expected_source_observeos_receipt_digest", source_digest
    )
    expected_evidence = overrides.pop(
        "expected_maintenance_monitoring_verification_evidence_packet_digest",
        evidence_digest,
    )
    expected_review = overrides.pop(
        "expected_maintenance_monitoring_verification_review_certificate_digest",
        review_digest,
    )
    expected_context = overrides.pop(
        "expected_maintenance_monitoring_verification_intake_context_digest",
        context_digest,
    )
    policy = overrides.pop(
        "maintenance_monitoring_verification_policy_digest",
        "verifyos-maintenance-monitoring-verification-policy-v011",
    )
    responsibility = overrides.pop(
        "verifyos_monitoring_responsibility_digest",
        "verifyos-maintenance-monitoring-responsibility-v011",
    )
    request = overrides.pop(
        "maintenance_monitoring_verification_request_id",
        "verifyos-maintenance-monitoring-verification-v011-001",
    )
    bundle = overrides.pop(
        "future_only_maintenance_monitoring_verification_bundle_digest",
        compute_future_only_maintenance_monitoring_verification_bundle_digest(
            source_observeos_receipt_digest=source_digest,
            expected_source_observeos_receipt_digest=expected_source,
            source_maintenance_monitoring_observation_record_digest=src[
                "maintenance_monitoring_observation_record_digest"
            ],
            source_maintenance_monitoring_verification_handoff_envelope_digest=src[
                "maintenance_monitoring_verification_handoff_envelope_digest"
            ],
            maintenance_monitoring_verification_evidence_packet_digest=evidence_digest,
            expected_maintenance_monitoring_verification_evidence_packet_digest=expected_evidence,
            maintenance_monitoring_verification_review_certificate_digest=review_digest,
            expected_maintenance_monitoring_verification_review_certificate_digest=expected_review,
            maintenance_monitoring_verification_intake_context_digest=context_digest,
            expected_maintenance_monitoring_verification_intake_context_digest=expected_context,
            requested_monitoring_verification_operation_digest=cx[
                "requested_monitoring_verification_operation_digest"
            ],
            exact_monitoring_verification_cycle_digest=cx[
                "exact_monitoring_verification_cycle_digest"
            ],
            maintenance_monitoring_verification_policy_digest=policy,
            verifyos_monitoring_responsibility_digest=responsibility,
            maintenance_monitoring_verification_request_id=request,
        ),
    )

    args = dict(
        source_observeos_receipt=src,
        expected_source_observeos_receipt_digest=expected_source,
        maintenance_monitoring_verification_evidence_packet=ev,
        expected_maintenance_monitoring_verification_evidence_packet_digest=expected_evidence,
        maintenance_monitoring_verification_review_certificate=rv,
        expected_maintenance_monitoring_verification_review_certificate_digest=expected_review,
        maintenance_monitoring_verification_intake_context=cx,
        expected_maintenance_monitoring_verification_intake_context_digest=expected_context,
        maintenance_monitoring_verification_policy_digest=policy,
        verifyos_monitoring_responsibility_digest=responsibility,
        maintenance_monitoring_verification_request_id=request,
        future_only_maintenance_monitoring_verification_bundle_digest=bundle,
    )
    args.update(overrides)
    return build_verifyos_dukkha_preserving_future_only_maintenance_monitoring_observation_verification_intake(
        **args
    )
