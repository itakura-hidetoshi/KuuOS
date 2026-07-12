#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_verifyos_dukkha_preserving_world_causal_attribution_verification_intake_v0_1 import (
    EVIDENCE_DIGEST_FIELD as SOURCE_CAUSAL_EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_CAUSAL_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD as SOURCE_CAUSAL_REVIEW_DIGEST_FIELD,
    canonical_digest,
    compute_world_causal_attribution_evidence_packet_digest,
    compute_world_causal_attribution_verification_review_certificate_digest,
)

STATUS_READY, STATUS_BLOCKED = "ready", "blocked"

RECEIPT_DIGEST_FIELD = (
    "verifyos_dukkha_preserving_realized_dukkha_verification_disposition_intake_receipt_digest"
)
EVIDENCE_DIGEST_FIELD = "realized_dukkha_verification_evidence_packet_digest"
REVIEW_DIGEST_FIELD = "realized_dukkha_verification_review_certificate_digest"
CONTEXT_DIGEST_FIELD = "realized_dukkha_verification_intake_context_digest"

STATE_BEFORE = (
    "world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_realization_pending"
)
STATE_AFTER_SUPPORTED = (
    "world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed"
)

DISPOSITION_SUPPORTED = "realized_dukkha_verification_supported"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_CONTEXT_REFRESH = "dukkha_realization_context_refresh_required"
DISPOSITION_REVIEW_REFRESH = "dukkha_realization_review_refresh_required"
DISPOSITION_ADDITIONAL_EVIDENCE = "additional_realized_dukkha_evidence_required"
DISPOSITION_BASELINE_REPAIR = "baseline_dukkha_correspondence_repair_required"
DISPOSITION_OUTCOME_REPAIR = "post_intervention_dukkha_correspondence_repair_required"
DISPOSITION_MEASUREMENT_REPAIR = "dukkha_measurement_validity_repair_required"
DISPOSITION_TEMPORAL_REPAIR = "dukkha_assessment_window_repair_required"
DISPOSITION_CAUSAL_BINDING_REPAIR = "causal_binding_correspondence_repair_required"
DISPOSITION_EFFECT_ESTIMATE_REPAIR = "dukkha_effect_estimate_repair_required"
DISPOSITION_DURABILITY_REVIEW = "dukkha_reduction_durability_review_required"
DISPOSITION_ADVERSE_OFFSET_REVIEW = "adverse_effect_offset_review_required"
DISPOSITION_DISTRIBUTIONAL_REVIEW = "distributional_impact_review_required"
DISPOSITION_UNCERTAINTY_REPAIR = "uncertainty_repair_required"
DISPOSITION_CALIBRATION_REPAIR = "calibration_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "provenance_repair_required"
DISPOSITION_NONEXTERNALIZATION_REVIEW = "nonexternalization_review_required"
DISPOSITION_OVERCLAIM_REJECTED = "dukkha_realization_overclaim_rejected"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"

EVIDENCE_FIELDS = {
    "source_world_causal_attribution_verification_receipt_digest",
    "source_world_fact_confirmation_receipt_digest",
    "source_world_causal_attribution_evidence_packet_digest",
    "source_world_causal_attribution_verification_review_certificate_digest",
    "source_world_causal_attribution_verification_record_digest",
    "source_world_causal_attribution_verification_debt_consumption_record_digest",
    "source_bounded_world_causal_attribution_binding_digest",
    "source_dukkha_realization_verification_handoff_envelope_digest",
    "world_candidate_fact_digest",
    "world_candidate_relation_digest",
    "resulting_world_state_digest",
    "resulting_world_revision",
    "persistent_world_storage_target_digest",
    "expected_world_update_postcondition_digest",
    "causal_model_digest",
    "causal_query_digest",
    "intervention_digest",
    "counterfactual_estimand_digest",
    "realized_dukkha_observation_digest",
    "baseline_dukkha_assessment_digest",
    "post_intervention_dukkha_assessment_digest",
    "dukkha_outcome_measure_specification_digest",
    "dukkha_assessment_window_digest",
    "minimum_clinically_meaningful_reduction_digest",
    "realized_dukkha_effect_estimate_digest",
    "realized_dukkha_effect_direction_digest",
    "realized_dukkha_effect_magnitude_digest",
    "realized_dukkha_confidence_interval_digest",
    "durability_evidence_digest",
    "adverse_effect_offset_assessment_digest",
    "distributional_impact_assessment_digest",
    "protected_group_realized_dukkha_impact_digest",
    "future_subject_realized_dukkha_impact_digest",
    "uncertainty_digest",
    "calibration_digest",
    "provenance_chain_digests",
    "tamper_evidence_digest",
    "evidence_collector_id",
    "evidence_source_id",
    "collection_started_epoch",
    "collection_completed_epoch",
    "maximum_collection_duration",
    "independent_realized_dukkha_evidence",
    "exactly_one_realized_dukkha_evidence_collection",
    "world_mutation_performed_by_evidence_collector",
    "causal_attribution_reopened",
    "realized_dukkha_reduction_preconfirmed",
    "generalized_benefit_claimed",
    EVIDENCE_DIGEST_FIELD,
}

REVIEW_FIELDS = {
    "source_world_causal_attribution_verification_receipt_digest",
    EVIDENCE_DIGEST_FIELD,
    "source_bounded_world_causal_attribution_binding_digest",
    "source_dukkha_realization_verification_handoff_envelope_digest",
    "world_candidate_fact_digest",
    "world_candidate_relation_digest",
    "resulting_world_state_digest",
    "resulting_world_revision",
    "causal_model_digest",
    "causal_query_digest",
    "intervention_digest",
    "counterfactual_estimand_digest",
    "realized_dukkha_observation_digest",
    "baseline_dukkha_assessment_digest",
    "post_intervention_dukkha_assessment_digest",
    "dukkha_outcome_measure_specification_digest",
    "dukkha_assessment_window_digest",
    "minimum_clinically_meaningful_reduction_digest",
    "realized_dukkha_effect_estimate_digest",
    "reviewer_id",
    "verification_method_digest",
    "verification_evidence_digest",
    "verification_review_started_epoch",
    "verification_review_completed_epoch",
    "maximum_verification_review_duration",
    "source_bounded_world_fact_confirmed",
    "source_causal_attribution_confirmed",
    "causal_binding_correspondence_confirmed",
    "baseline_correspondence_confirmed",
    "post_intervention_outcome_correspondence_confirmed",
    "measurement_validity_adequate",
    "assessment_window_adequate",
    "clinically_meaningful_reduction_supported",
    "effect_direction_supports_reduction",
    "effect_magnitude_adequate",
    "durability_adequate",
    "adverse_effect_offset_acceptable",
    "distributional_impact_acceptable",
    "uncertainty_adequate",
    "calibration_adequate",
    "provenance_continuity_preserved",
    "protected_group_nonexternalization_supported",
    "future_nonexternalization_supported",
    "exact_bounded_scope_preserved",
    "causal_attribution_reopened",
    "realized_dukkha_reduction_preconfirmed",
    "generalized_benefit_claimed",
    REVIEW_DIGEST_FIELD,
}

CONTEXT_FIELDS = {
    "source_world_causal_attribution_verification_receipt_digest",
    EVIDENCE_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    "current_world_binding_digest",
    "current_world_model_state_digest",
    "current_world_model_revision",
    "current_persistent_world_storage_target_digest",
    "current_world_lineage_digest",
    "source_world_causal_attribution_verification_epoch",
    "realized_dukkha_verification_intake_epoch",
    "maximum_realized_dukkha_verification_intake_delay",
    "realized_dukkha_verification_intake_session_id",
    "realized_dukkha_verification_intake_nonce_digest",
    "prior_realized_dukkha_verification_intake_session_ids",
    "prior_realized_dukkha_evidence_packet_digests",
    "prior_realized_dukkha_verification_review_certificate_digests",
    "prior_realized_dukkha_verification_intake_nonce_digests",
    "prior_realized_dukkha_confirmed_causal_verification_receipt_digests",
    "requested_realized_dukkha_verification_operation_digest",
    "exact_realized_dukkha_verification_cycle_digest",
    CONTEXT_DIGEST_FIELD,
}


@dataclass
class VerifyOSRealizedDukkhaVerificationDispositionResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def _map(value: Any) -> dict:
    return dict(value) if isinstance(value, Mapping) else {}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    item = dict(value)
    item.pop(field, None)
    return canonical_digest(item)


def _strings(value: Any, allow_empty: bool = False) -> tuple[bool, list[str]]:
    ok = isinstance(value, list) and (allow_empty or bool(value)) and all(
        isinstance(item, str) and item for item in value
    )
    items = list(value) if isinstance(value, list) else []
    return ok and items == sorted(items) and len(items) == len(set(items)), items


def compute_realized_dukkha_verification_evidence_packet_digest(
    value: Mapping[str, Any],
) -> str:
    return _digest_without(value, EVIDENCE_DIGEST_FIELD)


def compute_realized_dukkha_verification_review_certificate_digest(
    value: Mapping[str, Any],
) -> str:
    return _digest_without(value, REVIEW_DIGEST_FIELD)


def compute_realized_dukkha_verification_intake_context_digest(
    value: Mapping[str, Any],
) -> str:
    return _digest_without(value, CONTEXT_DIGEST_FIELD)


def compute_realized_dukkha_verification_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def compute_requested_realized_dukkha_verification_operation_digest(
    source: Mapping[str, Any],
    evidence: Mapping[str, Any],
    review: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_world_causal_attribution_verification_receipt_digest": source.get(
                SOURCE_CAUSAL_DIGEST_FIELD
            ),
            EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
            "world_candidate_fact_digest": source.get("world_candidate_fact_digest"),
            "world_candidate_relation_digest": source.get(
                "world_candidate_relation_digest"
            ),
            "realized_dukkha_observation_digest": source.get(
                "world_causal_attribution_evidence_packet", {}
            ).get("realized_dukkha_observation_digest"),
            "realized_dukkha_effect_estimate_digest": evidence.get(
                "realized_dukkha_effect_estimate_digest"
            ),
            "state_before": STATE_BEFORE,
            "supported_state_after": STATE_AFTER_SUPPORTED,
        }
    )


def compute_exact_realized_dukkha_verification_cycle_digest(
    source: Mapping[str, Any],
    evidence: Mapping[str, Any],
    review: Mapping[str, Any],
    context: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_world_causal_attribution_verification_receipt_digest": source.get(
                SOURCE_CAUSAL_DIGEST_FIELD
            ),
            EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
            "realized_dukkha_verification_intake_session_id": context.get(
                "realized_dukkha_verification_intake_session_id"
            ),
            "realized_dukkha_verification_intake_nonce_digest": context.get(
                "realized_dukkha_verification_intake_nonce_digest"
            ),
            "realized_dukkha_verification_intake_epoch": context.get(
                "realized_dukkha_verification_intake_epoch"
            ),
            "current_world_model_revision": context.get("current_world_model_revision"),
            "requested_realized_dukkha_verification_operation_digest": context.get(
                "requested_realized_dukkha_verification_operation_digest"
            ),
        }
    )


def _verify_source(
    source: dict,
    expected_digest: str,
    blockers: list[str],
) -> tuple[str, dict, dict, dict, dict, dict, dict, list[str], list[str], int]:
    if not source:
        blockers.append("source_world_causal_attribution_verification_receipt_missing")
        return "", {}, {}, {}, {}, {}, {}, [], [], 0

    digest = source.get(SOURCE_CAUSAL_DIGEST_FIELD, "")
    if not digest:
        blockers.append("source_world_causal_attribution_verification_receipt_digest_missing")
    elif digest != _digest_without(source, SOURCE_CAUSAL_DIGEST_FIELD):
        blockers.append("source_world_causal_attribution_verification_receipt_digest_mismatch")
    if digest != expected_digest:
        blockers.append("source_world_causal_attribution_verification_expected_binding_mismatch")

    expected = {
        "kernel_version": "v0.1",
        "verifyos_version": "v0.9",
        "status": "VERIFYOS_DUKKHA_PRESERVING_WORLD_CAUSAL_ATTRIBUTION_VERIFICATION_ROUTED",
        "world_causal_attribution_verification_disposition": (
            "world_causal_attribution_verification_supported"
        ),
        "world_causal_attribution_verification_state_after": STATE_BEFORE,
        "source_world_fact_confirmation_receipt_fully_revalidated": True,
        "source_world_postcondition_verification_receipt_fully_revalidated": True,
        "source_world_mutation_application_receipt_fully_revalidated": True,
        "bounded_world_fact_confirmed": True,
        "world_fact_confirmed": True,
        "world_fact_confirmation_scope_exactly_bounded": True,
        "generalized_world_truth_confirmed": False,
        "causal_attribution_confirmed": True,
        "causal_attribution_scope_exactly_bounded": True,
        "dukkha_realization_verification_intake_admitted": True,
        "dukkha_realization_verification_receipt_required": True,
        "dukkha_reduction_realized_confirmed": False,
        "persistent_world_model_state_unchanged_by_causal_verification": True,
        "persistent_world_state_changed_by_causal_verification": False,
        "world_model_revision_incremented_by_causal_verification": False,
        "world_mutation_reperformed": False,
        "world_patch_reapplied": False,
        "tool_invocation_performed": False,
        "external_side_effect_performed": False,
        "automatic_dukkha_realization_confirmation": False,
        "selection_authority_granted_to_verifyos": False,
        "plan_revision_authority_granted_to_verifyos": False,
        "dukkha_minimization_authority_granted_to_verifyos": False,
        "general_execution_authority_granted": False,
        "general_world_mutation_authority_granted": False,
        "world_mutation_authority_granted": False,
    }
    for key, value in expected.items():
        if source.get(key) != value:
            blockers.append(f"source_causal_boundary_{key}_mismatch")

    evidence = _map(source.get("world_causal_attribution_evidence_packet"))
    review = _map(source.get("world_causal_attribution_verification_review_certificate"))
    record = _map(source.get("world_causal_attribution_verification_record"))
    debt = _map(
        source.get("world_causal_attribution_verification_debt_consumption_record")
    )
    binding = _map(source.get("bounded_world_causal_attribution_binding"))
    handoff = _map(source.get("dukkha_realization_verification_handoff_envelope"))

    if not evidence:
        blockers.append("source_causal_evidence_packet_missing")
    elif source.get(SOURCE_CAUSAL_EVIDENCE_DIGEST_FIELD) != (
        compute_world_causal_attribution_evidence_packet_digest(evidence)
    ):
        blockers.append("source_causal_evidence_packet_digest_mismatch")

    if not review:
        blockers.append("source_causal_review_certificate_missing")
    elif source.get(SOURCE_CAUSAL_REVIEW_DIGEST_FIELD) != (
        compute_world_causal_attribution_verification_review_certificate_digest(review)
    ):
        blockers.append("source_causal_review_certificate_digest_mismatch")

    for name, item, field in (
        (
            "verification_record",
            record,
            "world_causal_attribution_verification_record_digest",
        ),
        (
            "debt_consumption_record",
            debt,
            "world_causal_attribution_verification_debt_consumption_record_digest",
        ),
        (
            "bounded_causal_binding",
            binding,
            "bounded_world_causal_attribution_binding_digest",
        ),
        (
            "dukkha_realization_handoff",
            handoff,
            "dukkha_realization_verification_handoff_envelope_digest",
        ),
    ):
        if not item:
            blockers.append(f"source_causal_{name}_missing")
        elif source.get(field) != canonical_digest(item):
            blockers.append(f"source_causal_{name}_digest_mismatch")

    if binding:
        if binding.get("causal_attribution_status") != (
            "confirmed_exact_bounded_relation_under_supplied_identification_assumptions"
        ):
            blockers.append("source_causal_binding_status_mismatch")
        if binding.get("generalization_beyond_bound") is not False:
            blockers.append("source_causal_binding_generalization_mismatch")
        if binding.get("dukkha_realization_state") != "not_confirmed":
            blockers.append("source_causal_binding_dukkha_state_mismatch")

    if handoff:
        cross = {
            "source_world_fact_confirmation_receipt_digest": source.get(
                "source_world_fact_confirmation_receipt_digest"
            ),
            "world_causal_attribution_verification_record_digest": source.get(
                "world_causal_attribution_verification_record_digest"
            ),
            "world_causal_attribution_verification_debt_consumption_record_digest": source.get(
                "world_causal_attribution_verification_debt_consumption_record_digest"
            ),
            "bounded_world_causal_attribution_binding_digest": source.get(
                "bounded_world_causal_attribution_binding_digest"
            ),
            "world_candidate_fact_digest": source.get("world_candidate_fact_digest"),
            "world_candidate_relation_digest": source.get(
                "world_candidate_relation_digest"
            ),
            "realized_dukkha_observation_digest": evidence.get(
                "realized_dukkha_observation_digest"
            ),
        }
        for key, value in cross.items():
            if handoff.get(key) != value:
                blockers.append(f"source_dukkha_handoff_{key}_mismatch")
        if handoff.get("causal_attribution_state") != (
            "confirmed_exact_bounded_relation"
        ):
            blockers.append("source_dukkha_handoff_causal_state_mismatch")
        if handoff.get("dukkha_realization_state") != (
            "pending_independent_verification"
        ):
            blockers.append("source_dukkha_handoff_state_mismatch")
        if handoff.get("dukkha_realization_verification_intake_admitted") is not True:
            blockers.append("source_dukkha_handoff_intake_not_admitted")
        if handoff.get("dukkha_realization_verification_receipt_required") is not True:
            blockers.append("source_dukkha_handoff_receipt_not_required")

    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_causal_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_causal_resulting_responsibility_invalid")

    source_epoch = record.get("world_causal_attribution_verification_intake_epoch")
    if not isinstance(source_epoch, int) or isinstance(source_epoch, bool):
        blockers.append("source_causal_verification_epoch_invalid")
        source_epoch = 0

    return (
        digest,
        evidence,
        review,
        record,
        debt,
        binding,
        handoff,
        lineage,
        responsibility,
        source_epoch,
    )


def _verify_evidence(
    evidence: dict,
    expected_digest: str,
    source: dict,
    blockers: list[str],
) -> tuple[str, bool, bool]:
    if not evidence:
        blockers.append("realized_dukkha_verification_evidence_packet_missing")
        return "", False, False
    if set(evidence) != EVIDENCE_FIELDS:
        blockers.append("realized_dukkha_verification_evidence_packet_schema_invalid")

    digest = evidence.get(EVIDENCE_DIGEST_FIELD, "")
    if not digest:
        blockers.append("realized_dukkha_verification_evidence_packet_digest_missing")
    elif digest != compute_realized_dukkha_verification_evidence_packet_digest(evidence):
        blockers.append("realized_dukkha_verification_evidence_packet_digest_mismatch")
    if digest != expected_digest:
        blockers.append("realized_dukkha_verification_evidence_expected_binding_mismatch")

    source_evidence = _map(source.get("world_causal_attribution_evidence_packet"))
    bindings = {
        "source_world_causal_attribution_verification_receipt_digest": source.get(
            SOURCE_CAUSAL_DIGEST_FIELD
        ),
        "source_world_fact_confirmation_receipt_digest": source.get(
            "source_world_fact_confirmation_receipt_digest"
        ),
        "source_world_causal_attribution_evidence_packet_digest": source.get(
            SOURCE_CAUSAL_EVIDENCE_DIGEST_FIELD
        ),
        "source_world_causal_attribution_verification_review_certificate_digest": source.get(
            SOURCE_CAUSAL_REVIEW_DIGEST_FIELD
        ),
        "source_world_causal_attribution_verification_record_digest": source.get(
            "world_causal_attribution_verification_record_digest"
        ),
        "source_world_causal_attribution_verification_debt_consumption_record_digest": source.get(
            "world_causal_attribution_verification_debt_consumption_record_digest"
        ),
        "source_bounded_world_causal_attribution_binding_digest": source.get(
            "bounded_world_causal_attribution_binding_digest"
        ),
        "source_dukkha_realization_verification_handoff_envelope_digest": source.get(
            "dukkha_realization_verification_handoff_envelope_digest"
        ),
        "world_candidate_fact_digest": source.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": source.get("world_candidate_relation_digest"),
        "resulting_world_state_digest": source.get("source_world_model_state_digest"),
        "resulting_world_revision": source.get("source_world_model_revision"),
        "persistent_world_storage_target_digest": source.get(
            "source_persistent_world_storage_target_digest"
        ),
        "expected_world_update_postcondition_digest": source_evidence.get(
            "expected_world_update_postcondition_digest"
        ),
        "causal_model_digest": source_evidence.get("causal_model_digest"),
        "causal_query_digest": source_evidence.get("causal_query_digest"),
        "intervention_digest": source_evidence.get("intervention_digest"),
        "counterfactual_estimand_digest": source_evidence.get(
            "counterfactual_estimand_digest"
        ),
        "realized_dukkha_observation_digest": source_evidence.get(
            "realized_dukkha_observation_digest"
        ),
    }
    for key, value in bindings.items():
        if evidence.get(key) != value:
            blockers.append(f"realized_dukkha_evidence_{key}_mismatch")

    required_strings = (
        "expected_world_update_postcondition_digest",
        "baseline_dukkha_assessment_digest",
        "post_intervention_dukkha_assessment_digest",
        "dukkha_outcome_measure_specification_digest",
        "dukkha_assessment_window_digest",
        "minimum_clinically_meaningful_reduction_digest",
        "realized_dukkha_effect_estimate_digest",
        "realized_dukkha_effect_direction_digest",
        "realized_dukkha_effect_magnitude_digest",
        "realized_dukkha_confidence_interval_digest",
        "durability_evidence_digest",
        "adverse_effect_offset_assessment_digest",
        "distributional_impact_assessment_digest",
        "protected_group_realized_dukkha_impact_digest",
        "future_subject_realized_dukkha_impact_digest",
        "uncertainty_digest",
        "calibration_digest",
        "tamper_evidence_digest",
        "evidence_collector_id",
        "evidence_source_id",
    )
    for field in required_strings:
        if not isinstance(evidence.get(field), str) or not evidence.get(field):
            blockers.append(f"realized_dukkha_evidence_{field}_invalid")

    provenance_ok, _ = _strings(evidence.get("provenance_chain_digests"))
    if not provenance_ok:
        blockers.append("realized_dukkha_evidence_provenance_chain_invalid")

    start = evidence.get("collection_started_epoch")
    end = evidence.get("collection_completed_epoch")
    maximum = evidence.get("maximum_collection_duration")
    duration_current = (
        isinstance(start, int)
        and not isinstance(start, bool)
        and isinstance(end, int)
        and not isinstance(end, bool)
        and isinstance(maximum, int)
        and not isinstance(maximum, bool)
        and start <= end
        and end - start <= maximum
    )

    independent = (
        evidence.get("independent_realized_dukkha_evidence") is True
        and evidence.get("exactly_one_realized_dukkha_evidence_collection") is True
        and evidence.get("world_mutation_performed_by_evidence_collector") is False
        and evidence.get("evidence_collector_id") != evidence.get("evidence_source_id")
    )

    return digest, duration_current, independent


def _verify_review(
    review: dict,
    expected_digest: str,
    source: dict,
    evidence: dict,
    blockers: list[str],
) -> tuple[str, bool]:
    if not review:
        blockers.append("realized_dukkha_verification_review_certificate_missing")
        return "", False
    if set(review) != REVIEW_FIELDS:
        blockers.append("realized_dukkha_verification_review_certificate_schema_invalid")

    digest = review.get(REVIEW_DIGEST_FIELD, "")
    if not digest:
        blockers.append("realized_dukkha_verification_review_certificate_digest_missing")
    elif digest != compute_realized_dukkha_verification_review_certificate_digest(review):
        blockers.append("realized_dukkha_verification_review_certificate_digest_mismatch")
    if digest != expected_digest:
        blockers.append("realized_dukkha_verification_review_expected_binding_mismatch")

    bindings = {
        "source_world_causal_attribution_verification_receipt_digest": source.get(
            SOURCE_CAUSAL_DIGEST_FIELD
        ),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        "source_bounded_world_causal_attribution_binding_digest": source.get(
            "bounded_world_causal_attribution_binding_digest"
        ),
        "source_dukkha_realization_verification_handoff_envelope_digest": source.get(
            "dukkha_realization_verification_handoff_envelope_digest"
        ),
        "world_candidate_fact_digest": evidence.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": evidence.get("world_candidate_relation_digest"),
        "resulting_world_state_digest": evidence.get("resulting_world_state_digest"),
        "resulting_world_revision": evidence.get("resulting_world_revision"),
        "causal_model_digest": evidence.get("causal_model_digest"),
        "causal_query_digest": evidence.get("causal_query_digest"),
        "intervention_digest": evidence.get("intervention_digest"),
        "counterfactual_estimand_digest": evidence.get("counterfactual_estimand_digest"),
        "realized_dukkha_observation_digest": evidence.get(
            "realized_dukkha_observation_digest"
        ),
        "baseline_dukkha_assessment_digest": evidence.get(
            "baseline_dukkha_assessment_digest"
        ),
        "post_intervention_dukkha_assessment_digest": evidence.get(
            "post_intervention_dukkha_assessment_digest"
        ),
        "dukkha_outcome_measure_specification_digest": evidence.get(
            "dukkha_outcome_measure_specification_digest"
        ),
        "dukkha_assessment_window_digest": evidence.get(
            "dukkha_assessment_window_digest"
        ),
        "minimum_clinically_meaningful_reduction_digest": evidence.get(
            "minimum_clinically_meaningful_reduction_digest"
        ),
        "realized_dukkha_effect_estimate_digest": evidence.get(
            "realized_dukkha_effect_estimate_digest"
        ),
    }
    for key, value in bindings.items():
        if review.get(key) != value:
            blockers.append(f"realized_dukkha_review_{key}_mismatch")

    for field in (
        "reviewer_id",
        "verification_method_digest",
        "verification_evidence_digest",
    ):
        if not isinstance(review.get(field), str) or not review.get(field):
            blockers.append(f"realized_dukkha_review_{field}_invalid")

    start = review.get("verification_review_started_epoch")
    end = review.get("verification_review_completed_epoch")
    maximum = review.get("maximum_verification_review_duration")
    duration_current = (
        isinstance(start, int)
        and not isinstance(start, bool)
        and isinstance(end, int)
        and not isinstance(end, bool)
        and isinstance(maximum, int)
        and not isinstance(maximum, bool)
        and start <= end
        and end - start <= maximum
    )

    return digest, duration_current


def _verify_context(
    context: dict,
    expected_digest: str,
    source: dict,
    evidence: dict,
    review: dict,
    source_epoch: int,
    blockers: list[str],
) -> tuple[str, tuple[bool, bool, bool, bool, bool, bool, bool]]:
    if not context:
        blockers.append("realized_dukkha_verification_intake_context_missing")
        return "", (False,) * 7
    if set(context) != CONTEXT_FIELDS:
        blockers.append("realized_dukkha_verification_intake_context_schema_invalid")

    digest = context.get(CONTEXT_DIGEST_FIELD, "")
    if not digest:
        blockers.append("realized_dukkha_verification_intake_context_digest_missing")
    elif digest != compute_realized_dukkha_verification_intake_context_digest(context):
        blockers.append("realized_dukkha_verification_intake_context_digest_mismatch")
    if digest != expected_digest:
        blockers.append("realized_dukkha_verification_intake_context_expected_binding_mismatch")

    bindings = {
        "source_world_causal_attribution_verification_receipt_digest": source.get(
            SOURCE_CAUSAL_DIGEST_FIELD
        ),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        "current_world_binding_digest": source.get("source_world_binding_digest"),
        "current_world_model_state_digest": source.get("source_world_model_state_digest"),
        "current_world_model_revision": source.get("source_world_model_revision"),
        "current_persistent_world_storage_target_digest": source.get(
            "source_persistent_world_storage_target_digest"
        ),
        "current_world_lineage_digest": canonical_digest(
            source.get("resulting_lineage_digests", [])
        ),
        "source_world_causal_attribution_verification_epoch": source_epoch,
    }
    world_current = True
    for key, value in bindings.items():
        if context.get(key) != value:
            if key.startswith("current_"):
                world_current = False
            else:
                blockers.append(f"realized_dukkha_context_{key}_mismatch")

    intake_epoch = context.get("realized_dukkha_verification_intake_epoch")
    maximum_delay = context.get("maximum_realized_dukkha_verification_intake_delay")
    delay_current = (
        isinstance(intake_epoch, int)
        and not isinstance(intake_epoch, bool)
        and isinstance(maximum_delay, int)
        and not isinstance(maximum_delay, bool)
        and source_epoch <= intake_epoch
        and intake_epoch - source_epoch <= maximum_delay
    )

    list_fields = (
        "prior_realized_dukkha_verification_intake_session_ids",
        "prior_realized_dukkha_evidence_packet_digests",
        "prior_realized_dukkha_verification_review_certificate_digests",
        "prior_realized_dukkha_verification_intake_nonce_digests",
        "prior_realized_dukkha_confirmed_causal_verification_receipt_digests",
    )
    lists: dict[str, list[str]] = {}
    for field in list_fields:
        ok, items = _strings(context.get(field), allow_empty=True)
        lists[field] = items
        if not ok:
            blockers.append(f"realized_dukkha_context_{field}_invalid")

    session = context.get("realized_dukkha_verification_intake_session_id")
    nonce = context.get("realized_dukkha_verification_intake_nonce_digest")
    if not isinstance(session, str) or not session:
        blockers.append("realized_dukkha_verification_intake_session_id_invalid")
    if not isinstance(nonce, str) or not nonce:
        blockers.append("realized_dukkha_verification_intake_nonce_digest_invalid")

    session_fresh = session not in lists[list_fields[0]]
    evidence_fresh = evidence.get(EVIDENCE_DIGEST_FIELD) not in lists[list_fields[1]]
    review_fresh = review.get(REVIEW_DIGEST_FIELD) not in lists[list_fields[2]]
    nonce_fresh = nonce not in lists[list_fields[3]]
    source_fresh = source.get(SOURCE_CAUSAL_DIGEST_FIELD) not in lists[list_fields[4]]

    requested = compute_requested_realized_dukkha_verification_operation_digest(
        source, evidence, review
    )
    if context.get("requested_realized_dukkha_verification_operation_digest") != requested:
        blockers.append("requested_realized_dukkha_verification_operation_digest_mismatch")

    cycle = compute_exact_realized_dukkha_verification_cycle_digest(
        source, evidence, review, context
    )
    if context.get("exact_realized_dukkha_verification_cycle_digest") != cycle:
        blockers.append("exact_realized_dukkha_verification_cycle_digest_mismatch")

    return digest, (
        world_current,
        delay_current,
        session_fresh,
        evidence_fresh,
        review_fresh,
        nonce_fresh,
        source_fresh,
    )


def _route(
    evidence: dict,
    review: dict,
    evidence_duration_current: bool,
    evidence_independent: bool,
    review_duration_current: bool,
    checks: tuple[bool, bool, bool, bool, bool, bool, bool],
) -> str:
    (
        world_current,
        delay_current,
        session_fresh,
        evidence_fresh,
        review_fresh,
        nonce_fresh,
        source_fresh,
    ) = checks
    if not all((session_fresh, evidence_fresh, review_fresh, nonce_fresh, source_fresh)):
        return DISPOSITION_REPLAY_REJECTED
    if not world_current:
        return DISPOSITION_WORLD_REFRESH
    if not delay_current:
        return DISPOSITION_CONTEXT_REFRESH
    if not review_duration_current:
        return DISPOSITION_REVIEW_REFRESH
    if not evidence_duration_current or not evidence_independent:
        return DISPOSITION_ADDITIONAL_EVIDENCE
    if evidence.get("generalized_benefit_claimed") or review.get("generalized_benefit_claimed"):
        return DISPOSITION_OVERCLAIM_REJECTED
    if evidence.get("realized_dukkha_reduction_preconfirmed") or review.get(
        "realized_dukkha_reduction_preconfirmed"
    ):
        return DISPOSITION_OVERCLAIM_REJECTED
    if evidence.get("causal_attribution_reopened") or review.get("causal_attribution_reopened"):
        return DISPOSITION_CAUSAL_BINDING_REPAIR
    if not review.get("source_bounded_world_fact_confirmed") or not review.get(
        "source_causal_attribution_confirmed"
    ):
        return DISPOSITION_CAUSAL_BINDING_REPAIR
    if not review.get("causal_binding_correspondence_confirmed"):
        return DISPOSITION_CAUSAL_BINDING_REPAIR
    if not review.get("baseline_correspondence_confirmed"):
        return DISPOSITION_BASELINE_REPAIR
    if not review.get("post_intervention_outcome_correspondence_confirmed"):
        return DISPOSITION_OUTCOME_REPAIR
    if not review.get("measurement_validity_adequate"):
        return DISPOSITION_MEASUREMENT_REPAIR
    if not review.get("assessment_window_adequate"):
        return DISPOSITION_TEMPORAL_REPAIR
    if not review.get("clinically_meaningful_reduction_supported"):
        return DISPOSITION_EFFECT_ESTIMATE_REPAIR
    if not review.get("effect_direction_supports_reduction") or not review.get(
        "effect_magnitude_adequate"
    ):
        return DISPOSITION_EFFECT_ESTIMATE_REPAIR
    if not review.get("durability_adequate"):
        return DISPOSITION_DURABILITY_REVIEW
    if not review.get("adverse_effect_offset_acceptable"):
        return DISPOSITION_ADVERSE_OFFSET_REVIEW
    if not review.get("distributional_impact_acceptable"):
        return DISPOSITION_DISTRIBUTIONAL_REVIEW
    if not review.get("uncertainty_adequate"):
        return DISPOSITION_UNCERTAINTY_REPAIR
    if not review.get("calibration_adequate"):
        return DISPOSITION_CALIBRATION_REPAIR
    if not review.get("provenance_continuity_preserved"):
        return DISPOSITION_PROVENANCE_REPAIR
    if not review.get("protected_group_nonexternalization_supported") or not review.get(
        "future_nonexternalization_supported"
    ):
        return DISPOSITION_NONEXTERNALIZATION_REVIEW
    if not review.get("exact_bounded_scope_preserved"):
        return DISPOSITION_OVERCLAIM_REJECTED
    return DISPOSITION_SUPPORTED


def build_verifyos_dukkha_preserving_realized_dukkha_verification_disposition_intake(
    *,
    source_world_causal_attribution_verification_receipt: Mapping[str, Any],
    expected_source_world_causal_attribution_verification_receipt_digest: str,
    realized_dukkha_verification_evidence_packet: Mapping[str, Any],
    expected_realized_dukkha_verification_evidence_packet_digest: str,
    realized_dukkha_verification_review_certificate: Mapping[str, Any],
    expected_realized_dukkha_verification_review_certificate_digest: str,
    realized_dukkha_verification_intake_context: Mapping[str, Any],
    expected_realized_dukkha_verification_intake_context_digest: str,
    realized_dukkha_verification_policy_digest: str,
    realized_dukkha_verification_responsibility_digest: str,
    realized_dukkha_verification_request_id: str,
    realized_dukkha_verification_bundle_digest: str,
) -> VerifyOSRealizedDukkhaVerificationDispositionResult:
    blockers: list[str] = []
    source = _map(source_world_causal_attribution_verification_receipt)
    evidence = _map(realized_dukkha_verification_evidence_packet)
    review = _map(realized_dukkha_verification_review_certificate)
    context = _map(realized_dukkha_verification_intake_context)

    for name, value in {
        "expected_source_world_causal_attribution_verification_receipt_digest": (
            expected_source_world_causal_attribution_verification_receipt_digest
        ),
        "expected_realized_dukkha_verification_evidence_packet_digest": (
            expected_realized_dukkha_verification_evidence_packet_digest
        ),
        "expected_realized_dukkha_verification_review_certificate_digest": (
            expected_realized_dukkha_verification_review_certificate_digest
        ),
        "expected_realized_dukkha_verification_intake_context_digest": (
            expected_realized_dukkha_verification_intake_context_digest
        ),
        "realized_dukkha_verification_policy_digest": realized_dukkha_verification_policy_digest,
        "realized_dukkha_verification_responsibility_digest": (
            realized_dukkha_verification_responsibility_digest
        ),
        "realized_dukkha_verification_request_id": realized_dukkha_verification_request_id,
        "realized_dukkha_verification_bundle_digest": realized_dukkha_verification_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    (
        source_digest,
        source_evidence,
        source_review,
        source_record,
        source_debt,
        source_binding,
        source_handoff,
        source_lineage,
        source_responsibility,
        source_epoch,
    ) = _verify_source(
        source,
        expected_source_world_causal_attribution_verification_receipt_digest,
        blockers,
    )

    evidence_digest, evidence_duration_current, evidence_independent = _verify_evidence(
        evidence,
        expected_realized_dukkha_verification_evidence_packet_digest,
        source,
        blockers,
    )
    review_digest, review_duration_current = _verify_review(
        review,
        expected_realized_dukkha_verification_review_certificate_digest,
        source,
        evidence,
        blockers,
    )
    context_digest, checks = _verify_context(
        context,
        expected_realized_dukkha_verification_intake_context_digest,
        source,
        evidence,
        review,
        source_epoch,
        blockers,
    )

    if not blockers:
        bundle = compute_realized_dukkha_verification_bundle_digest(
            source_world_causal_attribution_verification_receipt_digest=source_digest,
            expected_source_world_causal_attribution_verification_receipt_digest=(
                expected_source_world_causal_attribution_verification_receipt_digest
            ),
            source_world_fact_confirmation_receipt_digest=source.get(
                "source_world_fact_confirmation_receipt_digest"
            ),
            source_world_causal_attribution_evidence_packet_digest=source.get(
                SOURCE_CAUSAL_EVIDENCE_DIGEST_FIELD
            ),
            source_world_causal_attribution_verification_review_certificate_digest=source.get(
                SOURCE_CAUSAL_REVIEW_DIGEST_FIELD
            ),
            source_world_causal_attribution_verification_record_digest=source.get(
                "world_causal_attribution_verification_record_digest"
            ),
            source_world_causal_attribution_verification_debt_consumption_record_digest=source.get(
                "world_causal_attribution_verification_debt_consumption_record_digest"
            ),
            source_bounded_world_causal_attribution_binding_digest=source.get(
                "bounded_world_causal_attribution_binding_digest"
            ),
            source_dukkha_realization_verification_handoff_envelope_digest=source.get(
                "dukkha_realization_verification_handoff_envelope_digest"
            ),
            realized_dukkha_verification_evidence_packet_digest=evidence_digest,
            expected_realized_dukkha_verification_evidence_packet_digest=(
                expected_realized_dukkha_verification_evidence_packet_digest
            ),
            realized_dukkha_verification_review_certificate_digest=review_digest,
            expected_realized_dukkha_verification_review_certificate_digest=(
                expected_realized_dukkha_verification_review_certificate_digest
            ),
            realized_dukkha_verification_intake_context_digest=context_digest,
            expected_realized_dukkha_verification_intake_context_digest=(
                expected_realized_dukkha_verification_intake_context_digest
            ),
            requested_realized_dukkha_verification_operation_digest=context.get(
                "requested_realized_dukkha_verification_operation_digest"
            ),
            exact_realized_dukkha_verification_cycle_digest=context.get(
                "exact_realized_dukkha_verification_cycle_digest"
            ),
            realized_dukkha_verification_policy_digest=(
                realized_dukkha_verification_policy_digest
            ),
            realized_dukkha_verification_responsibility_digest=(
                realized_dukkha_verification_responsibility_digest
            ),
            realized_dukkha_verification_request_id=realized_dukkha_verification_request_id,
        )
        if bundle != realized_dukkha_verification_bundle_digest:
            blockers.append("realized_dukkha_verification_bundle_digest_mismatch")

    if blockers:
        return VerifyOSRealizedDukkhaVerificationDispositionResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    disposition = _route(
        evidence,
        review,
        evidence_duration_current,
        evidence_independent,
        review_duration_current,
        checks,
    )
    supported = disposition == DISPOSITION_SUPPORTED
    state_after = STATE_AFTER_SUPPORTED if supported else STATE_BEFORE

    realization_record = {
        "source_world_causal_attribution_verification_receipt_digest": source_digest,
        EVIDENCE_DIGEST_FIELD: evidence_digest,
        REVIEW_DIGEST_FIELD: review_digest,
        "source_bounded_world_causal_attribution_binding_digest": source[
            "bounded_world_causal_attribution_binding_digest"
        ],
        "world_candidate_fact_digest": evidence["world_candidate_fact_digest"],
        "world_candidate_relation_digest": evidence["world_candidate_relation_digest"],
        "resulting_world_state_digest": evidence["resulting_world_state_digest"],
        "resulting_world_revision": evidence["resulting_world_revision"],
        "realized_dukkha_observation_digest": evidence[
            "realized_dukkha_observation_digest"
        ],
        "baseline_dukkha_assessment_digest": evidence[
            "baseline_dukkha_assessment_digest"
        ],
        "post_intervention_dukkha_assessment_digest": evidence[
            "post_intervention_dukkha_assessment_digest"
        ],
        "realized_dukkha_effect_estimate_digest": evidence[
            "realized_dukkha_effect_estimate_digest"
        ],
        "reviewer_id": review["reviewer_id"],
        "realized_dukkha_verification_intake_session_id": context[
            "realized_dukkha_verification_intake_session_id"
        ],
        "realized_dukkha_verification_intake_nonce_digest": context[
            "realized_dukkha_verification_intake_nonce_digest"
        ],
        "realized_dukkha_verification_intake_epoch": context[
            "realized_dukkha_verification_intake_epoch"
        ],
        "realized_dukkha_verification_disposition": disposition,
        "state_before": STATE_BEFORE,
        "state_after": state_after,
        "bounded_world_fact_status": "confirmed_exact_bounded_proposition",
        "causal_attribution_status": "confirmed_exact_bounded_relation",
        "dukkha_realization_status": (
            "confirmed_exact_bounded_realized_reduction"
            if supported
            else "pending_independent_verification"
        ),
    }
    realization_record_digest = canonical_digest(realization_record)

    debt = {
        "source_world_causal_attribution_verification_receipt_digest": source_digest,
        EVIDENCE_DIGEST_FIELD: evidence_digest,
        REVIEW_DIGEST_FIELD: review_digest,
        "realized_dukkha_verification_record_digest": realization_record_digest,
        "realized_dukkha_verification_debt_consumed": supported,
        "source_causal_verification_receipt_marked_dukkha_realized": supported,
        "double_realized_dukkha_verification_performed": False,
    }
    debt_digest = canonical_digest(debt)

    realization_binding = None
    realization_binding_digest = ""
    learning_handoff = None
    learning_handoff_digest = ""
    if supported:
        realization_binding = {
            "source_world_causal_attribution_verification_receipt_digest": source_digest,
            "realized_dukkha_verification_record_digest": realization_record_digest,
            "realized_dukkha_verification_debt_consumption_record_digest": debt_digest,
            "bounded_world_causal_attribution_binding_digest": source[
                "bounded_world_causal_attribution_binding_digest"
            ],
            "world_candidate_fact_digest": evidence["world_candidate_fact_digest"],
            "world_candidate_relation_digest": evidence[
                "world_candidate_relation_digest"
            ],
            "resulting_world_state_digest": evidence["resulting_world_state_digest"],
            "resulting_world_revision": evidence["resulting_world_revision"],
            "realized_dukkha_observation_digest": evidence[
                "realized_dukkha_observation_digest"
            ],
            "realized_dukkha_effect_estimate_digest": evidence[
                "realized_dukkha_effect_estimate_digest"
            ],
            "minimum_clinically_meaningful_reduction_digest": evidence[
                "minimum_clinically_meaningful_reduction_digest"
            ],
            "durability_evidence_digest": evidence["durability_evidence_digest"],
            "uncertainty_digest": evidence["uncertainty_digest"],
            "calibration_digest": evidence["calibration_digest"],
            "provenance_chain_digests": evidence["provenance_chain_digests"],
            "dukkha_realization_status": "confirmed_exact_bounded_realized_reduction",
            "generalization_beyond_bound": False,
            "automatic_plan_completion": False,
        }
        realization_binding_digest = canonical_digest(realization_binding)
        learning_handoff = {
            "source_world_causal_attribution_verification_receipt_digest": source_digest,
            "realized_dukkha_verification_record_digest": realization_record_digest,
            "realized_dukkha_verification_debt_consumption_record_digest": debt_digest,
            "bounded_realized_dukkha_confirmation_binding_digest": realization_binding_digest,
            "world_candidate_fact_digest": evidence["world_candidate_fact_digest"],
            "world_candidate_relation_digest": evidence[
                "world_candidate_relation_digest"
            ],
            "dukkha_realization_state": "confirmed_exact_bounded_reduction",
            "future_learning_intake_admitted": True,
            "future_learning_receipt_required": True,
            "historical_evidence_read_only": True,
        }
        learning_handoff_digest = canonical_digest(learning_handoff)

    resulting_lineage = sorted(
        set(source_lineage)
        | {
            source_digest,
            source[SOURCE_CAUSAL_EVIDENCE_DIGEST_FIELD],
            source[SOURCE_CAUSAL_REVIEW_DIGEST_FIELD],
            source["world_causal_attribution_verification_record_digest"],
            source[
                "world_causal_attribution_verification_debt_consumption_record_digest"
            ],
            source["bounded_world_causal_attribution_binding_digest"],
            source["dukkha_realization_verification_handoff_envelope_digest"],
            evidence_digest,
            review_digest,
            context_digest,
            context["requested_realized_dukkha_verification_operation_digest"],
            context["exact_realized_dukkha_verification_cycle_digest"],
            realization_record_digest,
            debt_digest,
            realized_dukkha_verification_bundle_digest,
        }
        | ({realization_binding_digest} if realization_binding_digest else set())
        | ({learning_handoff_digest} if learning_handoff_digest else set())
    )
    resulting_responsibility = sorted(
        set(source_responsibility)
        | {
            review["reviewer_id"],
            realized_dukkha_verification_responsibility_digest,
        }
    )

    (
        world_current,
        delay_current,
        session_fresh,
        evidence_fresh,
        review_fresh,
        nonce_fresh,
        source_fresh,
    ) = checks

    receipt = {
        "kernel": "VerifyOS Dukkha-Preserving Realized-Dukkha Verification Disposition Intake Kernel",
        "kernel_version": "v0.1",
        "verifyos_version": "v0.10",
        "status": "VERIFYOS_DUKKHA_PRESERVING_REALIZED_DUKKHA_VERIFICATION_DISPOSITION_ROUTED",
        "source_world_causal_attribution_verification_receipt_digest": source_digest,
        "source_world_fact_confirmation_receipt_digest": source[
            "source_world_fact_confirmation_receipt_digest"
        ],
        "source_world_causal_attribution_evidence_packet_digest": source[
            SOURCE_CAUSAL_EVIDENCE_DIGEST_FIELD
        ],
        "source_world_causal_attribution_verification_review_certificate_digest": source[
            SOURCE_CAUSAL_REVIEW_DIGEST_FIELD
        ],
        "source_world_causal_attribution_verification_record_digest": source[
            "world_causal_attribution_verification_record_digest"
        ],
        "source_world_causal_attribution_verification_debt_consumption_record_digest": source[
            "world_causal_attribution_verification_debt_consumption_record_digest"
        ],
        "source_bounded_world_causal_attribution_binding_digest": source[
            "bounded_world_causal_attribution_binding_digest"
        ],
        "source_dukkha_realization_verification_handoff_envelope_digest": source[
            "dukkha_realization_verification_handoff_envelope_digest"
        ],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source["source_world_model_state_digest"],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_persistent_world_storage_target_digest": source[
            "source_persistent_world_storage_target_digest"
        ],
        "world_candidate_fact_digest": source["world_candidate_fact_digest"],
        "world_candidate_relation_digest": source["world_candidate_relation_digest"],
        "realized_dukkha_verification_evidence_packet": evidence,
        EVIDENCE_DIGEST_FIELD: evidence_digest,
        "realized_dukkha_verification_review_certificate": review,
        REVIEW_DIGEST_FIELD: review_digest,
        CONTEXT_DIGEST_FIELD: context_digest,
        "realized_dukkha_verification_policy_digest": (
            realized_dukkha_verification_policy_digest
        ),
        "realized_dukkha_verification_responsibility_digest": (
            realized_dukkha_verification_responsibility_digest
        ),
        "realized_dukkha_verification_request_id": realized_dukkha_verification_request_id,
        "realized_dukkha_verification_bundle_digest": (
            realized_dukkha_verification_bundle_digest
        ),
        "realized_dukkha_verification_disposition": disposition,
        "realized_dukkha_verification_state_before": STATE_BEFORE,
        "realized_dukkha_verification_state_after": state_after,
        "realized_dukkha_verification_record": realization_record,
        "realized_dukkha_verification_record_digest": realization_record_digest,
        "realized_dukkha_verification_debt_consumption_record": debt,
        "realized_dukkha_verification_debt_consumption_record_digest": debt_digest,
        "bounded_realized_dukkha_confirmation_binding": realization_binding,
        "bounded_realized_dukkha_confirmation_binding_digest": realization_binding_digest,
        "future_learning_handoff_envelope": learning_handoff,
        "future_learning_handoff_envelope_digest": learning_handoff_digest,
        "source_world_causal_attribution_verification_receipt_supplied": True,
        "source_world_causal_attribution_verification_receipt_fully_revalidated": True,
        "source_bounded_world_fact_confirmed": True,
        "source_causal_attribution_confirmed": True,
        "source_causal_attribution_scope_exactly_bounded": True,
        "source_realized_dukkha_handoff_bound": True,
        "baseline_dukkha_assessment_bound": True,
        "post_intervention_dukkha_assessment_bound": True,
        "dukkha_outcome_measure_specification_bound": True,
        "dukkha_assessment_window_bound": True,
        "minimum_clinically_meaningful_reduction_bound": True,
        "realized_dukkha_effect_estimate_bound": True,
        "durability_evidence_bound": True,
        "adverse_effect_offset_assessment_bound": True,
        "distributional_impact_assessment_bound": True,
        "uncertainty_bound": True,
        "calibration_bound": True,
        "provenance_bound": True,
        "protected_group_realized_dukkha_impact_bound": True,
        "future_subject_realized_dukkha_impact_bound": True,
        "exactly_one_realized_dukkha_verification_receipt_issued": True,
        "realized_dukkha_verification_performed": True,
        "realized_dukkha_verification_supported": supported,
        "realized_dukkha_verification_debt_consumed": supported,
        "realized_dukkha_verification_debt_replay_closed": supported,
        "realized_dukkha_verification_double_consumed": False,
        "realized_dukkha_evidence_packet_replay_closed": True,
        "realized_dukkha_verification_review_certificate_replay_closed": True,
        "realized_dukkha_verification_intake_nonce_consumed": True,
        "realized_dukkha_verification_intake_nonce_replay_closed": True,
        "source_world_causal_attribution_verification_receipt_replay_closed": supported,
        "realized_dukkha_verification_intake_session_replay_fresh_before_intake": (
            session_fresh
        ),
        "realized_dukkha_evidence_replay_fresh_before_intake": evidence_fresh,
        "realized_dukkha_verification_review_replay_fresh_before_intake": review_fresh,
        "realized_dukkha_verification_intake_nonce_replay_fresh_before_intake": nonce_fresh,
        "source_world_causal_attribution_verification_receipt_replay_fresh_before_verification": (
            source_fresh
        ),
        "world_conditions_current": world_current,
        "realized_dukkha_evidence_collection_duration_current": (
            evidence_duration_current
        ),
        "realized_dukkha_verification_review_duration_current": review_duration_current,
        "realized_dukkha_verification_intake_delay_current": delay_current,
        "realized_dukkha_verification_debt_open": not supported,
        "bounded_world_fact_confirmed": True,
        "world_fact_confirmed": True,
        "world_fact_confirmation_scope_exactly_bounded": True,
        "generalized_world_truth_confirmed": False,
        "causal_attribution_confirmed": True,
        "causal_attribution_scope_exactly_bounded": True,
        "dukkha_reduction_realized_confirmed": supported,
        "dukkha_reduction_realized_scope_exactly_bounded": supported,
        "future_learning_intake_admitted": supported,
        "future_learning_receipt_required": supported,
        "persistent_world_model_state_unchanged_by_dukkha_verification": True,
        "persistent_world_state_changed_by_dukkha_verification": False,
        "world_model_revision_incremented_by_dukkha_verification": False,
        "world_mutation_reperformed": False,
        "world_patch_reapplied": False,
        "tool_invocation_performed": False,
        "external_side_effect_performed": False,
        "compensation_route_ready": True,
        "compensation_performed": False,
        "automatic_truth_generalization": False,
        "automatic_causal_attribution": False,
        "automatic_dukkha_realization_confirmation": False,
        "automatic_plan_completion": False,
        "automatic_rollback": False,
        "automatic_compensation": False,
        "effect_scope_preserved": True,
        "effect_ceiling_preserved": True,
        "checkpoint_guards_preserved": True,
        "stop_conditions_preserved": True,
        "evidence_lineage_preserved": True,
        "responsibility_lineage_preserved": True,
        "alternative_candidates_preserved": True,
        "dissent_preserved": True,
        "minority_preserved": True,
        "dukkha_reduction_support_preserved": True,
        "protected_group_nonexternalization_preserved": True,
        "future_nonexternalization_preserved": True,
        "revision_capacity_preserved": True,
        "persistent_loop_reduction_preserved": True,
        "single_scalar_utility_not_introduced": True,
        "selection_remains_decisionos_owned": True,
        "selection_authority_granted_to_verifyos": False,
        "plan_revision_authority_granted_to_verifyos": False,
        "dukkha_minimization_authority_granted_to_verifyos": False,
        "general_execution_authority_granted": False,
        "execution_permission": False,
        "general_world_mutation_authority_granted": False,
        "world_mutation_authority_granted": False,
        "world_model_prediction_not_truth": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "resulting_lineage_digests": resulting_lineage,
        "resulting_responsibility_lineage_digests": resulting_responsibility,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return VerifyOSRealizedDukkhaVerificationDispositionResult(
        STATUS_READY, [], receipt
    )
