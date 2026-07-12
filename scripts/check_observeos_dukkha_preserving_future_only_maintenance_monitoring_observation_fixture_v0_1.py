from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_observeos_dukkha_preserving_future_only_maintenance_monitoring_observation_intake_v0_1 import *
from scripts.check_learnos_dukkha_preserving_future_only_learning_maintenance_fixture_v0_1 import (
    build as build_learnos_v04,
)


def source():
    result = build_learnos_v04()
    assert result.status == STATUS_READY, result.blockers
    assert result.receipt is not None
    return deepcopy(result.receipt)


def evidence(src):
    learning = src["future_only_learning_evidence_packet"]
    delta = src["future_only_learning_delta_binding"]
    handoff = src["maintenance_monitoring_handoff_envelope"]
    value = {
        "source_learnos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        "source_future_only_learning_evidence_packet_digest": src[SOURCE_EVIDENCE_DIGEST_FIELD],
        "source_future_only_learning_review_certificate_digest": src[SOURCE_REVIEW_DIGEST_FIELD],
        "source_future_only_learning_record_digest": src["future_only_learning_record_digest"],
        "source_future_only_learning_debt_consumption_record_digest": src["future_only_learning_debt_consumption_record_digest"],
        "source_future_only_learning_delta_binding_digest": src["future_only_learning_delta_binding_digest"],
        "source_maintenance_monitoring_handoff_envelope_digest": src["maintenance_monitoring_handoff_envelope_digest"],
        "world_candidate_fact_digest": learning["world_candidate_fact_digest"],
        "world_candidate_relation_digest": learning["world_candidate_relation_digest"],
        "resulting_world_state_digest": learning["resulting_world_state_digest"],
        "resulting_world_revision": learning["resulting_world_revision"],
        "future_only_learning_delta_digest": delta["delta"],
        "maintenance_policy_candidate_digest": delta["maintenance"],
        "maintenance_window_digest": handoff["maintenance_window"],
        "durability_monitoring_specification_digest": handoff["durability"],
        "adverse_effect_monitoring_specification_digest": handoff["adverse"],
        "distributional_monitoring_specification_digest": handoff["distributional"],
        "reobservation_trigger_digest": handoff["reobservation"],
        "retention_window_digest": handoff["retention"],
        "observation_window_digest": "observeos-maintenance-observation-window-v06-001",
        "baseline_observation_digest": "observeos-maintenance-baseline-v06-001",
        "durability_observation_digest": "observeos-maintenance-durability-v06-001",
        "adverse_effect_observation_digest": "observeos-maintenance-adverse-v06-001",
        "distributional_observation_digest": "observeos-maintenance-distributional-v06-001",
        "raw_artifact_digests": [
            "observeos-maintenance-raw-artifact-v06-001",
            "observeos-maintenance-raw-artifact-v06-002",
        ],
        "uncertainty_digest": "observeos-maintenance-uncertainty-v06-001",
        "calibration_digest": "observeos-maintenance-calibration-v06-001",
        "provenance_chain_digests": sorted(
            {
                src[SOURCE_RECEIPT_DIGEST_FIELD],
                src["future_only_learning_delta_binding_digest"],
                src["maintenance_monitoring_handoff_envelope_digest"],
                "observeos-maintenance-provenance-v06-001",
            }
        ),
        "tamper_evidence_digest": "observeos-maintenance-tamper-v06-001",
        "protected_group_observation_impact_digest": "observeos-maintenance-protected-impact-v06-001",
        "future_subject_observation_impact_digest": "observeos-maintenance-future-impact-v06-001",
        "collector_id": "observeos-maintenance-observer-v06",
        "evidence_source_id": "independent-maintenance-monitoring-source-v06",
        "collection_started_epoch": 151,
        "collection_completed_epoch": 152,
        "maximum_collection_duration": 4,
        "independent_maintenance_monitoring_evidence": True,
        "exactly_one_monitoring_observation_collection": True,
        "maintenance_action_performed": False,
        "current_world_mutation_performed": False,
        "current_plan_revised": False,
        "current_policy_activated": False,
        "learning_delta_activated": False,
        "generalized_benefit_claimed": False,
        "authority_escalation_claimed": False,
    }
    value[EVIDENCE_DIGEST_FIELD] = (
        compute_maintenance_monitoring_observation_evidence_packet_digest(value)
    )
    return value


def review(src, ev):
    value = {
        "source_learnos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        EVIDENCE_DIGEST_FIELD: ev[EVIDENCE_DIGEST_FIELD],
        "source_future_only_learning_delta_binding_digest": src["future_only_learning_delta_binding_digest"],
        "source_maintenance_monitoring_handoff_envelope_digest": src["maintenance_monitoring_handoff_envelope_digest"],
        "world_candidate_fact_digest": ev["world_candidate_fact_digest"],
        "world_candidate_relation_digest": ev["world_candidate_relation_digest"],
        "resulting_world_state_digest": ev["resulting_world_state_digest"],
        "resulting_world_revision": ev["resulting_world_revision"],
        "future_only_learning_delta_digest": ev["future_only_learning_delta_digest"],
        "maintenance_policy_candidate_digest": ev["maintenance_policy_candidate_digest"],
        "reviewer_id": "observeos-maintenance-observation-reviewer-v06",
        "verification_method_digest": "observeos-maintenance-observation-method-v06-001",
        "verification_evidence_digest": "observeos-maintenance-observation-review-evidence-v06-001",
        "review_started_epoch": 152,
        "review_completed_epoch": 153,
        "maximum_review_duration": 4,
        "source_receipt_correspondence_confirmed": True,
        "future_only_learning_delta_correspondence_confirmed": True,
        "maintenance_handoff_correspondence_confirmed": True,
        "maintenance_window_adequate": True,
        "durability_observation_adequate": True,
        "adverse_effect_observation_adequate": True,
        "distributional_observation_adequate": True,
        "reobservation_trigger_adequate": True,
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
        compute_maintenance_monitoring_observation_review_certificate_digest(value)
    )
    return value


def context(src, ev, rv):
    learning = src["future_only_learning_evidence_packet"]
    source_epoch = src["future_only_learning_record"]["epoch"]
    value = {
        "source_learnos_receipt_digest": src[SOURCE_RECEIPT_DIGEST_FIELD],
        EVIDENCE_DIGEST_FIELD: ev[EVIDENCE_DIGEST_FIELD],
        REVIEW_DIGEST_FIELD: rv[REVIEW_DIGEST_FIELD],
        "current_world_model_state_digest": learning["resulting_world_state_digest"],
        "current_world_model_revision": learning["resulting_world_revision"],
        "current_future_only_learning_delta_digest": learning["future_only_learning_delta_digest"],
        "current_maintenance_policy_candidate_digest": learning["maintenance_policy_candidate_digest"],
        "source_future_only_learning_epoch": source_epoch,
        "monitoring_observation_intake_epoch": source_epoch + 8,
        "maximum_monitoring_observation_intake_delay": 16,
        "monitoring_observation_intake_session_id": "observeos-maintenance-observation-v06-001",
        "monitoring_observation_intake_nonce_digest": "observeos-maintenance-observation-nonce-v06-001",
        "prior_monitoring_observation_intake_session_ids": [],
        "prior_monitoring_observation_evidence_packet_digests": [],
        "prior_monitoring_observation_review_certificate_digests": [],
        "prior_monitoring_observation_intake_nonce_digests": [],
        "prior_monitoring_observation_source_receipt_digests": [],
        "requested_monitoring_observation_operation_digest": (
            compute_requested_monitoring_observation_operation_digest(src, ev, rv)
        ),
        "exact_monitoring_observation_cycle_digest": "",
    }
    value["exact_monitoring_observation_cycle_digest"] = (
        compute_exact_monitoring_observation_cycle_digest(src, ev, rv, value)
    )
    value[CONTEXT_DIGEST_FIELD] = (
        compute_maintenance_monitoring_observation_intake_context_digest(value)
    )
    return value


def redigest_evidence(value):
    value = deepcopy(value)
    value.pop(EVIDENCE_DIGEST_FIELD, None)
    value[EVIDENCE_DIGEST_FIELD] = (
        compute_maintenance_monitoring_observation_evidence_packet_digest(value)
    )
    return value


def redigest_review(value, ev):
    value = deepcopy(value)
    value[EVIDENCE_DIGEST_FIELD] = ev[EVIDENCE_DIGEST_FIELD]
    value.pop(REVIEW_DIGEST_FIELD, None)
    value[REVIEW_DIGEST_FIELD] = (
        compute_maintenance_monitoring_observation_review_certificate_digest(value)
    )
    return value


def redigest_context(src, ev, rv, value):
    value = deepcopy(value)
    value[EVIDENCE_DIGEST_FIELD] = ev[EVIDENCE_DIGEST_FIELD]
    value[REVIEW_DIGEST_FIELD] = rv[REVIEW_DIGEST_FIELD]
    value["requested_monitoring_observation_operation_digest"] = (
        compute_requested_monitoring_observation_operation_digest(src, ev, rv)
    )
    value["exact_monitoring_observation_cycle_digest"] = (
        compute_exact_monitoring_observation_cycle_digest(src, ev, rv, value)
    )
    value.pop(CONTEXT_DIGEST_FIELD, None)
    value[CONTEXT_DIGEST_FIELD] = (
        compute_maintenance_monitoring_observation_intake_context_digest(value)
    )
    return value


def build(**overrides):
    src = deepcopy(overrides.pop("source_learnos_receipt", None) or source())
    ev = deepcopy(
        overrides.pop(
            "maintenance_monitoring_observation_evidence_packet", None
        )
        or evidence(src)
    )
    rv = deepcopy(
        overrides.pop(
            "maintenance_monitoring_observation_review_certificate", None
        )
        or review(src, ev)
    )
    cx = deepcopy(
        overrides.pop(
            "maintenance_monitoring_observation_intake_context", None
        )
        or context(src, ev, rv)
    )

    source_digest = src.get(SOURCE_RECEIPT_DIGEST_FIELD, "source-missing")
    evidence_digest = ev.get(EVIDENCE_DIGEST_FIELD, "evidence-missing")
    review_digest = rv.get(REVIEW_DIGEST_FIELD, "review-missing")
    context_digest = cx.get(CONTEXT_DIGEST_FIELD, "context-missing")

    expected_source = overrides.pop(
        "expected_source_learnos_receipt_digest", source_digest
    )
    expected_evidence = overrides.pop(
        "expected_maintenance_monitoring_observation_evidence_packet_digest",
        evidence_digest,
    )
    expected_review = overrides.pop(
        "expected_maintenance_monitoring_observation_review_certificate_digest",
        review_digest,
    )
    expected_context = overrides.pop(
        "expected_maintenance_monitoring_observation_intake_context_digest",
        context_digest,
    )
    policy = overrides.pop(
        "maintenance_monitoring_observation_policy_digest",
        "observeos-maintenance-monitoring-policy-v06",
    )
    responsibility = overrides.pop(
        "observeos_monitoring_responsibility_digest",
        "observeos-maintenance-monitoring-responsibility-v06",
    )
    request = overrides.pop(
        "maintenance_monitoring_observation_request_id",
        "observeos-maintenance-monitoring-v06-001",
    )
    bundle = overrides.pop(
        "future_only_maintenance_monitoring_observation_bundle_digest",
        compute_future_only_maintenance_monitoring_observation_bundle_digest(
            source_learnos_receipt_digest=source_digest,
            expected_source_learnos_receipt_digest=expected_source,
            source_future_only_learning_delta_binding_digest=src[
                "future_only_learning_delta_binding_digest"
            ],
            source_maintenance_monitoring_handoff_envelope_digest=src[
                "maintenance_monitoring_handoff_envelope_digest"
            ],
            maintenance_monitoring_observation_evidence_packet_digest=evidence_digest,
            expected_maintenance_monitoring_observation_evidence_packet_digest=expected_evidence,
            maintenance_monitoring_observation_review_certificate_digest=review_digest,
            expected_maintenance_monitoring_observation_review_certificate_digest=expected_review,
            maintenance_monitoring_observation_intake_context_digest=context_digest,
            expected_maintenance_monitoring_observation_intake_context_digest=expected_context,
            requested_monitoring_observation_operation_digest=cx[
                "requested_monitoring_observation_operation_digest"
            ],
            exact_monitoring_observation_cycle_digest=cx[
                "exact_monitoring_observation_cycle_digest"
            ],
            maintenance_monitoring_observation_policy_digest=policy,
            observeos_monitoring_responsibility_digest=responsibility,
            maintenance_monitoring_observation_request_id=request,
        ),
    )

    args = dict(
        source_learnos_receipt=src,
        expected_source_learnos_receipt_digest=expected_source,
        maintenance_monitoring_observation_evidence_packet=ev,
        expected_maintenance_monitoring_observation_evidence_packet_digest=expected_evidence,
        maintenance_monitoring_observation_review_certificate=rv,
        expected_maintenance_monitoring_observation_review_certificate_digest=expected_review,
        maintenance_monitoring_observation_intake_context=cx,
        expected_maintenance_monitoring_observation_intake_context_digest=expected_context,
        maintenance_monitoring_observation_policy_digest=policy,
        observeos_monitoring_responsibility_digest=responsibility,
        maintenance_monitoring_observation_request_id=request,
        future_only_maintenance_monitoring_observation_bundle_digest=bundle,
    )
    args.update(overrides)
    return build_observeos_dukkha_preserving_future_only_maintenance_monitoring_observation_intake(
        **args
    )
