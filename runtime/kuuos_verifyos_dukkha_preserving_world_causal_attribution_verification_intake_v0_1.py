#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_world_dukkha_preserving_world_fact_confirmation_disposition_intake_v0_1 import (
    CONTEXT_DIGEST_FIELD as SOURCE_FACT_CONTEXT_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_FACT_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD as SOURCE_FACT_REVIEW_DIGEST_FIELD,
    SOURCE_EVIDENCE_DIGEST_FIELD,
    SOURCE_MUTATION_DIGEST_FIELD,
    SOURCE_VERIFICATION_DIGEST_FIELD,
    SOURCE_VERIFICATION_REVIEW_DIGEST_FIELD,
    canonical_digest,
    compute_world_fact_confirmation_review_certificate_digest,
)
from runtime.kuuos_verifyos_dukkha_preserving_world_postcondition_verification_intake_v0_1 import (
    compute_world_postcondition_evidence_packet_digest,
    compute_world_postcondition_verification_review_certificate_digest,
)

STATUS_READY, STATUS_BLOCKED = "ready", "blocked"

RECEIPT_DIGEST_FIELD = (
    "verifyos_dukkha_preserving_world_causal_attribution_verification_intake_receipt_digest"
)
EVIDENCE_DIGEST_FIELD = "world_causal_attribution_evidence_packet_digest"
REVIEW_DIGEST_FIELD = "world_causal_attribution_verification_review_certificate_digest"
CONTEXT_DIGEST_FIELD = "world_causal_attribution_verification_intake_context_digest"

STATE_BEFORE = "world_candidate_bounded_fact_confirmed_causal_attribution_pending"
STATE_AFTER_SUPPORTED = (
    "world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_realization_pending"
)

DISPOSITION_SUPPORTED = "world_causal_attribution_verification_supported"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_CONTEXT_REFRESH = "causal_attribution_context_refresh_required"
DISPOSITION_REVIEW_REFRESH = "causal_attribution_review_refresh_required"
DISPOSITION_ADDITIONAL_EVIDENCE = "additional_causal_evidence_required"
DISPOSITION_CAUSAL_MODEL_REPAIR = "causal_model_repair_required"
DISPOSITION_INTERVENTION_REPAIR = "intervention_correspondence_repair_required"
DISPOSITION_TEMPORAL_REPAIR = "temporal_ordering_repair_required"
DISPOSITION_CONFOUNDING_REPAIR = "confounding_control_repair_required"
DISPOSITION_COUNTERFACTUAL_REPAIR = "counterfactual_support_repair_required"
DISPOSITION_ALTERNATIVE_CAUSE_REVIEW = "alternative_cause_review_required"
DISPOSITION_SELECTION_BIAS_REVIEW = "selection_bias_review_required"
DISPOSITION_MEASUREMENT_REPAIR = "measurement_validity_repair_required"
DISPOSITION_UNCERTAINTY_REPAIR = "uncertainty_repair_required"
DISPOSITION_CALIBRATION_REPAIR = "calibration_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "provenance_repair_required"
DISPOSITION_NONEXTERNALIZATION_REVIEW = "nonexternalization_review_required"
DISPOSITION_TRUTH_GENERALIZATION_REJECTED = "truth_generalization_rejected"
DISPOSITION_DUKKHA_OVERCLAIM_REJECTED = "dukkha_realization_overclaim_rejected"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"

EVIDENCE_FIELDS = {
    "source_world_fact_confirmation_receipt_digest",
    "source_world_postcondition_verification_receipt_digest",
    "source_world_mutation_application_receipt_digest",
    "source_world_fact_confirmation_review_certificate_digest",
    "source_world_fact_confirmation_record_digest",
    "source_world_fact_confirmation_debt_consumption_record_digest",
    "source_bounded_world_fact_status_binding_digest",
    "source_causal_attribution_verification_handoff_envelope_digest",
    "world_candidate_fact_digest",
    "world_candidate_relation_digest",
    "resulting_world_state_digest",
    "resulting_world_revision",
    "persistent_world_storage_target_digest",
    "expected_world_update_postcondition_digest",
    "causal_model_digest",
    "causal_query_digest",
    "intervention_digest",
    "exposure_digest",
    "outcome_digest",
    "counterfactual_estimand_digest",
    "identification_assumption_digests",
    "confounder_set_digests",
    "adjustment_strategy_digest",
    "temporal_ordering_evidence_digest",
    "intervention_correspondence_evidence_digest",
    "counterfactual_support_evidence_digest",
    "alternative_cause_assessment_digest",
    "selection_bias_assessment_digest",
    "measurement_validity_assessment_digest",
    "uncertainty_digest",
    "calibration_digest",
    "provenance_chain_digests",
    "tamper_evidence_digest",
    "protected_group_causal_impact_digest",
    "future_subject_causal_impact_digest",
    "realized_dukkha_observation_digest",
    "evidence_collector_id",
    "evidence_source_id",
    "collection_started_epoch",
    "collection_completed_epoch",
    "maximum_collection_duration",
    "independent_causal_evidence",
    "exactly_one_causal_evidence_collection",
    "world_mutation_performed_by_causal_evidence_collector",
    "generalized_truth_claimed",
    "causal_attribution_preconfirmed",
    "realized_dukkha_reduction_claimed",
    EVIDENCE_DIGEST_FIELD,
}

REVIEW_FIELDS = {
    "source_world_fact_confirmation_receipt_digest",
    "source_world_postcondition_verification_receipt_digest",
    "source_world_mutation_application_receipt_digest",
    EVIDENCE_DIGEST_FIELD,
    "source_bounded_world_fact_status_binding_digest",
    "source_causal_attribution_verification_handoff_envelope_digest",
    "world_candidate_fact_digest",
    "world_candidate_relation_digest",
    "resulting_world_state_digest",
    "resulting_world_revision",
    "persistent_world_storage_target_digest",
    "expected_world_update_postcondition_digest",
    "causal_model_digest",
    "causal_query_digest",
    "intervention_digest",
    "exposure_digest",
    "outcome_digest",
    "counterfactual_estimand_digest",
    "reviewer_id",
    "verification_method_digest",
    "verification_evidence_digest",
    "verification_review_started_epoch",
    "verification_review_completed_epoch",
    "maximum_verification_review_duration",
    "source_bounded_world_fact_confirmed",
    "causal_model_adequate",
    "causal_query_exactly_bounded",
    "intervention_correspondence_confirmed",
    "temporal_ordering_confirmed",
    "confounding_control_adequate",
    "counterfactual_support_adequate",
    "alternative_causes_assessed",
    "selection_bias_adequate",
    "measurement_validity_adequate",
    "uncertainty_adequate",
    "calibration_adequate",
    "provenance_continuity_preserved",
    "protected_group_nonexternalization_supported",
    "future_nonexternalization_supported",
    "no_truth_generalization",
    "no_dukkha_realization_overclaim",
    "generalized_truth_claimed",
    "causal_attribution_preconfirmed",
    "realized_dukkha_reduction_claimed",
    REVIEW_DIGEST_FIELD,
}

CONTEXT_FIELDS = {
    "source_world_fact_confirmation_receipt_digest",
    "source_world_postcondition_verification_receipt_digest",
    "source_world_mutation_application_receipt_digest",
    EVIDENCE_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    "current_world_binding_digest",
    "current_world_model_state_digest",
    "current_world_model_revision",
    "current_persistent_world_storage_target_digest",
    "current_world_lineage_digest",
    "source_world_fact_confirmation_epoch",
    "world_causal_attribution_verification_intake_epoch",
    "maximum_world_causal_attribution_verification_intake_delay",
    "world_causal_attribution_verification_intake_session_id",
    "world_causal_attribution_verification_intake_nonce_digest",
    "prior_world_causal_attribution_verification_intake_session_ids",
    "prior_world_causal_attribution_evidence_packet_digests",
    "prior_world_causal_attribution_verification_review_certificate_digests",
    "prior_world_causal_attribution_verification_intake_nonce_digests",
    "prior_causally_verified_world_fact_confirmation_receipt_digests",
    "requested_world_causal_attribution_verification_operation_digest",
    "exact_world_causal_attribution_verification_cycle_digest",
    CONTEXT_DIGEST_FIELD,
}


@dataclass
class VerifyOSWorldCausalAttributionVerificationResult:
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


def compute_world_causal_attribution_evidence_packet_digest(
    value: Mapping[str, Any],
) -> str:
    return _digest_without(value, EVIDENCE_DIGEST_FIELD)


def compute_world_causal_attribution_verification_review_certificate_digest(
    value: Mapping[str, Any],
) -> str:
    return _digest_without(value, REVIEW_DIGEST_FIELD)


def compute_world_causal_attribution_verification_intake_context_digest(
    value: Mapping[str, Any],
) -> str:
    return _digest_without(value, CONTEXT_DIGEST_FIELD)


def compute_world_causal_attribution_verification_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def compute_requested_world_causal_attribution_verification_operation_digest(
    source_fact: Mapping[str, Any],
    evidence: Mapping[str, Any],
    review: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_world_fact_confirmation_receipt_digest": source_fact.get(
                SOURCE_FACT_DIGEST_FIELD
            ),
            EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
            "world_candidate_fact_digest": source_fact.get("world_candidate_fact_digest"),
            "world_candidate_relation_digest": source_fact.get(
                "world_candidate_relation_digest"
            ),
            "causal_query_digest": evidence.get("causal_query_digest"),
            "counterfactual_estimand_digest": evidence.get(
                "counterfactual_estimand_digest"
            ),
            "state_before": STATE_BEFORE,
            "supported_state_after": STATE_AFTER_SUPPORTED,
        }
    )


def compute_exact_world_causal_attribution_verification_cycle_digest(
    source_fact: Mapping[str, Any],
    evidence: Mapping[str, Any],
    review: Mapping[str, Any],
    context: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_world_fact_confirmation_receipt_digest": source_fact.get(
                SOURCE_FACT_DIGEST_FIELD
            ),
            EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
            "world_causal_attribution_verification_intake_session_id": context.get(
                "world_causal_attribution_verification_intake_session_id"
            ),
            "world_causal_attribution_verification_intake_nonce_digest": context.get(
                "world_causal_attribution_verification_intake_nonce_digest"
            ),
            "world_causal_attribution_verification_intake_epoch": context.get(
                "world_causal_attribution_verification_intake_epoch"
            ),
            "current_world_model_revision": context.get("current_world_model_revision"),
            "requested_world_causal_attribution_verification_operation_digest": context.get(
                "requested_world_causal_attribution_verification_operation_digest"
            ),
        }
    )


def _verify_source_mutation(
    source: dict, expected: str, blockers: list[str]
) -> tuple[str, dict, dict, dict]:
    if not source:
        blockers.append("source_world_mutation_application_receipt_missing")
        return "", {}, {}, {}
    digest = source.get(SOURCE_MUTATION_DIGEST_FIELD, "")
    if not digest:
        blockers.append("source_world_mutation_application_receipt_digest_missing")
    elif digest != _digest_without(source, SOURCE_MUTATION_DIGEST_FIELD):
        blockers.append("source_world_mutation_application_receipt_digest_mismatch")
    if digest != expected:
        blockers.append("source_world_mutation_application_expected_binding_mismatch")
    for key, value in {
        "kernel_version": "v0.1",
        "world_version": "v0.62",
        "world_mutation_application_disposition": "world_mutation_application_ready",
        "world_mutation_application_state_after": (
            "world_candidate_commit_applied_world_fact_unconfirmed"
        ),
        "world_mutation_application_completed": True,
        "exactly_one_world_patch_applied": True,
        "world_mutation_transaction_atomic": True,
        "persistent_world_model_state_changed": True,
        "world_model_revision_incremented_exactly_once": True,
        "world_fact_confirmed": False,
        "causal_attribution_confirmed": False,
        "dukkha_reduction_realized_confirmed": False,
    }.items():
        if source.get(key) != value:
            blockers.append(f"source_mutation_boundary_{key}_mismatch")
    mutation = _map(source.get("world_mutation_record"))
    persisted = _map(source.get("persisted_world_candidate_envelope"))
    application_review = _map(source.get("world_mutation_application_review_certificate"))
    for name, item, field in (
        ("world_mutation_record", mutation, "world_mutation_record_digest"),
        (
            "persisted_world_candidate_envelope",
            persisted,
            "persisted_world_candidate_envelope_digest",
        ),
    ):
        if not item:
            blockers.append(f"source_mutation_{name}_missing")
        elif source.get(field) != canonical_digest(item):
            blockers.append(f"source_mutation_{name}_digest_mismatch")
    return digest, mutation, persisted, application_review


def _verify_source_verification(
    source: dict,
    expected: str,
    source_mutation: dict,
    blockers: list[str],
) -> tuple[str, dict]:
    if not source:
        blockers.append("source_world_postcondition_verification_receipt_missing")
        return "", {}
    digest = source.get(SOURCE_VERIFICATION_DIGEST_FIELD, "")
    if not digest:
        blockers.append("source_world_postcondition_verification_receipt_digest_missing")
    elif digest != _digest_without(source, SOURCE_VERIFICATION_DIGEST_FIELD):
        blockers.append("source_world_postcondition_verification_receipt_digest_mismatch")
    if digest != expected:
        blockers.append("source_world_postcondition_verification_expected_binding_mismatch")
    for key, value in {
        "kernel_version": "v0.1",
        "verifyos_version": "v0.8",
        "world_postcondition_verification_disposition": (
            "world_postcondition_verification_supported"
        ),
        "world_postcondition_verification_state_after": (
            "world_candidate_commit_postcondition_verified_world_fact_confirmation_pending"
        ),
        "world_postcondition_verification_supported": True,
        "world_postcondition_verification_debt_consumed": True,
        "world_fact_confirmation_receipt_required": True,
        "world_fact_confirmed": False,
        "causal_attribution_confirmed": False,
        "dukkha_reduction_realized_confirmed": False,
    }.items():
        if source.get(key) != value:
            blockers.append(f"source_verification_boundary_{key}_mismatch")
    if source.get("source_world_mutation_application_receipt_digest") != source_mutation.get(
        SOURCE_MUTATION_DIGEST_FIELD
    ):
        blockers.append("source_verification_mutation_binding_mismatch")
    evidence = _map(source.get("world_postcondition_evidence_packet"))
    source_review = _map(
        source.get("world_postcondition_verification_review_certificate")
    )
    if not evidence:
        blockers.append("source_verification_evidence_missing")
    elif source.get(SOURCE_EVIDENCE_DIGEST_FIELD) != (
        compute_world_postcondition_evidence_packet_digest(evidence)
    ):
        blockers.append("source_verification_evidence_digest_mismatch")
    if not source_review:
        blockers.append("source_verification_review_missing")
    elif source.get(SOURCE_VERIFICATION_REVIEW_DIGEST_FIELD) != (
        compute_world_postcondition_verification_review_certificate_digest(source_review)
    ):
        blockers.append("source_verification_review_digest_mismatch")
    for name, field in (
        (
            "world_postcondition_verification_record",
            "world_postcondition_verification_record_digest",
        ),
        (
            "world_postcondition_verification_debt_consumption_record",
            "world_postcondition_verification_debt_consumption_record_digest",
        ),
        (
            "world_fact_confirmation_handoff_envelope",
            "world_fact_confirmation_handoff_envelope_digest",
        ),
    ):
        item = _map(source.get(name))
        if not item:
            blockers.append(f"source_verification_{name}_missing")
        elif source.get(field) != canonical_digest(item):
            blockers.append(f"source_verification_{name}_digest_mismatch")
    return digest, evidence


def _verify_source_fact_confirmation(
    source: dict,
    expected: str,
    source_verification: dict,
    source_mutation: dict,
    blockers: list[str],
) -> tuple[str, dict, dict, dict, dict, list[str], list[str], int]:
    if not source:
        blockers.append("source_world_fact_confirmation_receipt_missing")
        return "", {}, {}, {}, {}, [], [], 0
    digest = source.get(SOURCE_FACT_DIGEST_FIELD, "")
    if not digest:
        blockers.append("source_world_fact_confirmation_receipt_digest_missing")
    elif digest != _digest_without(source, SOURCE_FACT_DIGEST_FIELD):
        blockers.append("source_world_fact_confirmation_receipt_digest_mismatch")
    if digest != expected:
        blockers.append("source_world_fact_confirmation_expected_binding_mismatch")
    for key, value in {
        "kernel_version": "v0.1",
        "world_version": "v0.63",
        "status": "WORLD_DUKKHA_PRESERVING_WORLD_FACT_CONFIRMATION_DISPOSITION_ROUTED",
        "world_fact_confirmation_disposition": "world_fact_confirmation_supported",
        "world_fact_confirmation_state_after": STATE_BEFORE,
        "source_world_postcondition_verification_receipt_fully_revalidated": True,
        "source_world_mutation_application_receipt_fully_revalidated": True,
        "world_fact_confirmation_supported": True,
        "world_fact_confirmation_debt_consumed": True,
        "world_fact_confirmation_debt_replay_closed": True,
        "world_fact_confirmation_debt_open": False,
        "bounded_world_fact_confirmed": True,
        "world_fact_confirmed": True,
        "world_fact_confirmation_scope_exactly_bounded": True,
        "generalized_world_truth_confirmed": False,
        "causal_attribution_verification_intake_admitted": True,
        "causal_attribution_verification_receipt_required": True,
        "causal_attribution_confirmed": False,
        "dukkha_reduction_realized_confirmed": False,
        "persistent_world_model_state_unchanged_by_fact_confirmation": True,
        "persistent_world_state_changed_by_fact_confirmation": False,
        "world_model_revision_incremented_by_fact_confirmation": False,
        "world_mutation_reperformed": False,
        "world_patch_reapplied": False,
        "tool_invocation_performed": False,
        "external_side_effect_performed": False,
        "general_execution_authority_granted": False,
        "world_mutation_authority_granted": False,
    }.items():
        if source.get(key) != value:
            blockers.append(f"source_fact_confirmation_boundary_{key}_mismatch")
    if source.get("source_world_postcondition_verification_receipt_digest") != (
        source_verification.get(SOURCE_VERIFICATION_DIGEST_FIELD)
    ):
        blockers.append("source_fact_confirmation_verification_binding_mismatch")
    if source.get("source_world_mutation_application_receipt_digest") != (
        source_mutation.get(SOURCE_MUTATION_DIGEST_FIELD)
    ):
        blockers.append("source_fact_confirmation_mutation_binding_mismatch")
    review = _map(source.get("world_fact_confirmation_review_certificate"))
    confirmation_record = _map(source.get("world_fact_confirmation_record"))
    debt = _map(source.get("world_fact_confirmation_debt_consumption_record"))
    fact_binding = _map(source.get("bounded_world_fact_status_binding"))
    causal_handoff = _map(
        source.get("causal_attribution_verification_handoff_envelope")
    )
    if not review:
        blockers.append("source_fact_confirmation_review_missing")
    elif source.get(SOURCE_FACT_REVIEW_DIGEST_FIELD) != (
        compute_world_fact_confirmation_review_certificate_digest(review)
    ):
        blockers.append("source_fact_confirmation_review_digest_mismatch")
    for name, item, field in (
        (
            "world_fact_confirmation_record",
            confirmation_record,
            "world_fact_confirmation_record_digest",
        ),
        (
            "world_fact_confirmation_debt_consumption_record",
            debt,
            "world_fact_confirmation_debt_consumption_record_digest",
        ),
        (
            "bounded_world_fact_status_binding",
            fact_binding,
            "bounded_world_fact_status_binding_digest",
        ),
        (
            "causal_attribution_verification_handoff_envelope",
            causal_handoff,
            "causal_attribution_verification_handoff_envelope_digest",
        ),
    ):
        if not item:
            blockers.append(f"source_fact_confirmation_{name}_missing")
        elif source.get(field) != canonical_digest(item):
            blockers.append(f"source_fact_confirmation_{name}_digest_mismatch")
    if not source.get(SOURCE_FACT_CONTEXT_DIGEST_FIELD):
        blockers.append("source_fact_confirmation_context_digest_missing")
    for key, value in {
        "bounded_world_fact_status": "confirmed_exact_bounded_proposition",
        "generalization_beyond_bound": False,
        "causal_attribution_state": "not_confirmed",
        "dukkha_realization_state": "not_confirmed",
    }.items():
        if fact_binding.get(key) != value:
            blockers.append(f"source_fact_binding_{key}_mismatch")
    for key, value in {
        "causal_attribution_state": "pending_independent_verification",
        "causal_attribution_intake_admitted": True,
        "causal_attribution_receipt_required": True,
        "dukkha_realization_state": "not_confirmed",
    }.items():
        if causal_handoff.get(key) != value:
            blockers.append(f"source_causal_handoff_{key}_mismatch")
    bindings = {
        "world_fact_confirmation_record_digest": source.get(
            "world_fact_confirmation_record_digest"
        ),
        "world_fact_confirmation_debt_consumption_record_digest": source.get(
            "world_fact_confirmation_debt_consumption_record_digest"
        ),
        "bounded_world_fact_status_binding_digest": source.get(
            "bounded_world_fact_status_binding_digest"
        ),
        "world_candidate_fact_digest": source.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": source.get(
            "world_candidate_relation_digest"
        ),
        "resulting_world_state_digest": source.get("source_world_model_state_digest"),
        "resulting_world_revision": source.get("source_world_model_revision"),
    }
    for key, value in bindings.items():
        if causal_handoff.get(key) != value:
            blockers.append(f"source_causal_handoff_{key}_mismatch")
    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_fact_confirmation_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_fact_confirmation_resulting_responsibility_invalid")
    epoch = confirmation_record.get("world_fact_confirmation_intake_epoch")
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0:
        blockers.append("source_world_fact_confirmation_epoch_invalid")
        epoch = 0
    return (
        digest,
        review,
        confirmation_record,
        debt,
        fact_binding,
        lineage,
        responsibility,
        epoch,
    )


def _verify_evidence(
    evidence: dict,
    expected: str,
    source_fact: dict,
    source_verification: dict,
    source_mutation: dict,
    blockers: list[str],
) -> tuple[str, bool, bool]:
    if not evidence:
        blockers.append("world_causal_attribution_evidence_packet_missing")
        return "", False, False
    if set(evidence) != EVIDENCE_FIELDS:
        blockers.append("world_causal_attribution_evidence_packet_schema_invalid")
    digest = evidence.get(EVIDENCE_DIGEST_FIELD, "")
    if not digest:
        blockers.append("world_causal_attribution_evidence_packet_digest_missing")
    elif digest != compute_world_causal_attribution_evidence_packet_digest(evidence):
        blockers.append("world_causal_attribution_evidence_packet_digest_mismatch")
    if digest != expected:
        blockers.append("world_causal_attribution_evidence_expected_binding_mismatch")
    bindings = {
        "source_world_fact_confirmation_receipt_digest": source_fact.get(
            SOURCE_FACT_DIGEST_FIELD
        ),
        "source_world_postcondition_verification_receipt_digest": (
            source_verification.get(SOURCE_VERIFICATION_DIGEST_FIELD)
        ),
        "source_world_mutation_application_receipt_digest": source_mutation.get(
            SOURCE_MUTATION_DIGEST_FIELD
        ),
        "source_world_fact_confirmation_review_certificate_digest": source_fact.get(
            SOURCE_FACT_REVIEW_DIGEST_FIELD
        ),
        "source_world_fact_confirmation_record_digest": source_fact.get(
            "world_fact_confirmation_record_digest"
        ),
        "source_world_fact_confirmation_debt_consumption_record_digest": source_fact.get(
            "world_fact_confirmation_debt_consumption_record_digest"
        ),
        "source_bounded_world_fact_status_binding_digest": source_fact.get(
            "bounded_world_fact_status_binding_digest"
        ),
        "source_causal_attribution_verification_handoff_envelope_digest": source_fact.get(
            "causal_attribution_verification_handoff_envelope_digest"
        ),
        "world_candidate_fact_digest": source_fact.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": source_fact.get(
            "world_candidate_relation_digest"
        ),
        "resulting_world_state_digest": source_fact.get(
            "source_world_model_state_digest"
        ),
        "resulting_world_revision": source_fact.get("source_world_model_revision"),
        "persistent_world_storage_target_digest": source_fact.get(
            "source_persistent_world_storage_target_digest"
        ),
        "expected_world_update_postcondition_digest": source_fact.get(
            "expected_world_update_postcondition_digest"
        ),
    }
    for key, value in bindings.items():
        if evidence.get(key) != value:
            blockers.append(f"world_causal_attribution_evidence_{key}_mismatch")
    for field in (
        "causal_model_digest",
        "causal_query_digest",
        "intervention_digest",
        "exposure_digest",
        "outcome_digest",
        "counterfactual_estimand_digest",
        "adjustment_strategy_digest",
        "temporal_ordering_evidence_digest",
        "intervention_correspondence_evidence_digest",
        "counterfactual_support_evidence_digest",
        "alternative_cause_assessment_digest",
        "selection_bias_assessment_digest",
        "measurement_validity_assessment_digest",
        "uncertainty_digest",
        "calibration_digest",
        "tamper_evidence_digest",
        "protected_group_causal_impact_digest",
        "future_subject_causal_impact_digest",
        "realized_dukkha_observation_digest",
        "evidence_collector_id",
        "evidence_source_id",
    ):
        if not isinstance(evidence.get(field), str) or not evidence.get(field):
            blockers.append(f"world_causal_attribution_evidence_{field}_invalid")
    for field in (
        "identification_assumption_digests",
        "confounder_set_digests",
        "provenance_chain_digests",
    ):
        ok, _ = _strings(evidence.get(field))
        if not ok:
            blockers.append(f"world_causal_attribution_evidence_{field}_invalid")
    for field in (
        "collection_started_epoch",
        "collection_completed_epoch",
        "maximum_collection_duration",
        "resulting_world_revision",
    ):
        value = evidence.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"world_causal_attribution_evidence_{field}_invalid")
    for field in (
        "independent_causal_evidence",
        "exactly_one_causal_evidence_collection",
        "world_mutation_performed_by_causal_evidence_collector",
        "generalized_truth_claimed",
        "causal_attribution_preconfirmed",
        "realized_dukkha_reduction_claimed",
    ):
        if not isinstance(evidence.get(field), bool):
            blockers.append(f"world_causal_attribution_evidence_{field}_invalid")
    start = evidence.get("collection_started_epoch")
    end = evidence.get("collection_completed_epoch")
    maximum = evidence.get("maximum_collection_duration")
    duration_current = (
        all(
            isinstance(value, int) and not isinstance(value, bool) and value >= 0
            for value in (start, end, maximum)
        )
        and 1 <= maximum <= 64
        and 0 <= end - start <= maximum
    )
    fact_reviewer = source_fact.get("world_fact_confirmation_review_certificate", {}).get(
        "fact_confirmation_reviewer_id"
    )
    independent = (
        evidence.get("independent_causal_evidence") is True
        and evidence.get("exactly_one_causal_evidence_collection") is True
        and evidence.get("world_mutation_performed_by_causal_evidence_collector") is False
        and evidence.get("evidence_collector_id") != fact_reviewer
        and evidence.get("evidence_source_id") != fact_reviewer
    )
    return digest, duration_current, independent


def _verify_review(
    review: dict,
    expected: str,
    source_fact: dict,
    source_verification: dict,
    source_mutation: dict,
    evidence: dict,
    blockers: list[str],
) -> tuple[str, bool]:
    if not review:
        blockers.append("world_causal_attribution_verification_review_certificate_missing")
        return "", False
    if set(review) != REVIEW_FIELDS:
        blockers.append("world_causal_attribution_verification_review_schema_invalid")
    digest = review.get(REVIEW_DIGEST_FIELD, "")
    if not digest:
        blockers.append("world_causal_attribution_verification_review_digest_missing")
    elif digest != (
        compute_world_causal_attribution_verification_review_certificate_digest(review)
    ):
        blockers.append("world_causal_attribution_verification_review_digest_mismatch")
    if digest != expected:
        blockers.append("world_causal_attribution_verification_review_expected_binding_mismatch")
    bindings = {
        "source_world_fact_confirmation_receipt_digest": source_fact.get(
            SOURCE_FACT_DIGEST_FIELD
        ),
        "source_world_postcondition_verification_receipt_digest": (
            source_verification.get(SOURCE_VERIFICATION_DIGEST_FIELD)
        ),
        "source_world_mutation_application_receipt_digest": source_mutation.get(
            SOURCE_MUTATION_DIGEST_FIELD
        ),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        "source_bounded_world_fact_status_binding_digest": source_fact.get(
            "bounded_world_fact_status_binding_digest"
        ),
        "source_causal_attribution_verification_handoff_envelope_digest": source_fact.get(
            "causal_attribution_verification_handoff_envelope_digest"
        ),
        "world_candidate_fact_digest": evidence.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": evidence.get(
            "world_candidate_relation_digest"
        ),
        "resulting_world_state_digest": evidence.get("resulting_world_state_digest"),
        "resulting_world_revision": evidence.get("resulting_world_revision"),
        "persistent_world_storage_target_digest": evidence.get(
            "persistent_world_storage_target_digest"
        ),
        "expected_world_update_postcondition_digest": evidence.get(
            "expected_world_update_postcondition_digest"
        ),
        "causal_model_digest": evidence.get("causal_model_digest"),
        "causal_query_digest": evidence.get("causal_query_digest"),
        "intervention_digest": evidence.get("intervention_digest"),
        "exposure_digest": evidence.get("exposure_digest"),
        "outcome_digest": evidence.get("outcome_digest"),
        "counterfactual_estimand_digest": evidence.get(
            "counterfactual_estimand_digest"
        ),
    }
    for key, value in bindings.items():
        if review.get(key) != value:
            blockers.append(f"world_causal_attribution_verification_review_{key}_mismatch")
    for field in (
        "reviewer_id",
        "verification_method_digest",
        "verification_evidence_digest",
    ):
        if not isinstance(review.get(field), str) or not review.get(field):
            blockers.append(f"world_causal_attribution_verification_review_{field}_invalid")
    for field in (
        "verification_review_started_epoch",
        "verification_review_completed_epoch",
        "maximum_verification_review_duration",
        "resulting_world_revision",
    ):
        value = review.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"world_causal_attribution_verification_review_{field}_invalid")
    boolean_fields = REVIEW_FIELDS - {
        REVIEW_DIGEST_FIELD,
        "source_world_fact_confirmation_receipt_digest",
        "source_world_postcondition_verification_receipt_digest",
        "source_world_mutation_application_receipt_digest",
        EVIDENCE_DIGEST_FIELD,
        "source_bounded_world_fact_status_binding_digest",
        "source_causal_attribution_verification_handoff_envelope_digest",
        "world_candidate_fact_digest",
        "world_candidate_relation_digest",
        "resulting_world_state_digest",
        "resulting_world_revision",
        "persistent_world_storage_target_digest",
        "expected_world_update_postcondition_digest",
        "causal_model_digest",
        "causal_query_digest",
        "intervention_digest",
        "exposure_digest",
        "outcome_digest",
        "counterfactual_estimand_digest",
        "reviewer_id",
        "verification_method_digest",
        "verification_evidence_digest",
        "verification_review_started_epoch",
        "verification_review_completed_epoch",
        "maximum_verification_review_duration",
    }
    for field in boolean_fields:
        if not isinstance(review.get(field), bool):
            blockers.append(f"world_causal_attribution_verification_review_{field}_invalid")
    start = review.get("verification_review_started_epoch")
    end = review.get("verification_review_completed_epoch")
    maximum = review.get("maximum_verification_review_duration")
    duration_current = (
        all(
            isinstance(value, int) and not isinstance(value, bool) and value >= 0
            for value in (start, end, maximum)
        )
        and 1 <= maximum <= 64
        and 0 <= end - start <= maximum
    )
    return digest, duration_current


def _verify_context(
    context: dict,
    expected: str,
    source_fact: dict,
    source_verification: dict,
    source_mutation: dict,
    evidence: dict,
    review: dict,
    source_epoch: int,
    blockers: list[str],
) -> tuple[str, tuple[bool, ...]]:
    if not context:
        blockers.append("world_causal_attribution_verification_intake_context_missing")
        return "", (False,) * 7
    if set(context) != CONTEXT_FIELDS:
        blockers.append("world_causal_attribution_verification_intake_context_schema_invalid")
    digest = context.get(CONTEXT_DIGEST_FIELD, "")
    if not digest:
        blockers.append("world_causal_attribution_verification_intake_context_digest_missing")
    elif digest != (
        compute_world_causal_attribution_verification_intake_context_digest(context)
    ):
        blockers.append("world_causal_attribution_verification_intake_context_digest_mismatch")
    if digest != expected:
        blockers.append("world_causal_attribution_verification_context_expected_binding_mismatch")
    for key, value in {
        "source_world_fact_confirmation_receipt_digest": source_fact.get(
            SOURCE_FACT_DIGEST_FIELD
        ),
        "source_world_postcondition_verification_receipt_digest": source_verification.get(
            SOURCE_VERIFICATION_DIGEST_FIELD
        ),
        "source_world_mutation_application_receipt_digest": source_mutation.get(
            SOURCE_MUTATION_DIGEST_FIELD
        ),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
    }.items():
        if context.get(key) != value:
            blockers.append(f"world_causal_attribution_verification_context_{key}_mismatch")
    for field in (
        "current_world_binding_digest",
        "current_world_model_state_digest",
        "current_persistent_world_storage_target_digest",
        "current_world_lineage_digest",
        "world_causal_attribution_verification_intake_session_id",
        "world_causal_attribution_verification_intake_nonce_digest",
        "requested_world_causal_attribution_verification_operation_digest",
        "exact_world_causal_attribution_verification_cycle_digest",
    ):
        if not isinstance(context.get(field), str) or not context.get(field):
            blockers.append(f"world_causal_attribution_verification_context_{field}_invalid")
    for field in (
        "current_world_model_revision",
        "source_world_fact_confirmation_epoch",
        "world_causal_attribution_verification_intake_epoch",
        "maximum_world_causal_attribution_verification_intake_delay",
    ):
        value = context.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"world_causal_attribution_verification_context_{field}_invalid")
    world_current = all(
        context.get(key) == value
        for key, value in {
            "current_world_binding_digest": source_fact.get("source_world_binding_digest"),
            "current_world_model_state_digest": source_fact.get(
                "source_world_model_state_digest"
            ),
            "current_world_model_revision": source_fact.get(
                "source_world_model_revision"
            ),
            "current_persistent_world_storage_target_digest": source_fact.get(
                "source_persistent_world_storage_target_digest"
            ),
            "current_world_lineage_digest": canonical_digest(
                source_fact.get("resulting_lineage_digests", [])
            ),
        }.items()
    )
    if context.get(
        "requested_world_causal_attribution_verification_operation_digest"
    ) != compute_requested_world_causal_attribution_verification_operation_digest(
        source_fact, evidence, review
    ):
        blockers.append("world_causal_attribution_verification_context_operation_digest_mismatch")
    if context.get(
        "exact_world_causal_attribution_verification_cycle_digest"
    ) != compute_exact_world_causal_attribution_verification_cycle_digest(
        source_fact, evidence, review, context
    ):
        blockers.append("world_causal_attribution_verification_context_cycle_digest_mismatch")
    epoch = context.get("world_causal_attribution_verification_intake_epoch")
    maximum = context.get("maximum_world_causal_attribution_verification_intake_delay")
    delay_current = (
        all(
            isinstance(value, int) and not isinstance(value, bool)
            for value in (source_epoch, epoch, maximum)
        )
        and context.get("source_world_fact_confirmation_epoch") == source_epoch
        and 1 <= maximum <= 64
        and 0 <= epoch - source_epoch <= maximum
    )
    values = []
    for field in (
        "prior_world_causal_attribution_verification_intake_session_ids",
        "prior_world_causal_attribution_evidence_packet_digests",
        "prior_world_causal_attribution_verification_review_certificate_digests",
        "prior_world_causal_attribution_verification_intake_nonce_digests",
        "prior_causally_verified_world_fact_confirmation_receipt_digests",
    ):
        ok, items = _strings(context.get(field), True)
        if not ok:
            blockers.append(f"world_causal_attribution_verification_context_{field}_invalid")
        values.append(items)
    sessions, evidences, reviews, nonces, sources = values
    return digest, (
        world_current,
        delay_current,
        context.get("world_causal_attribution_verification_intake_session_id")
        not in sessions,
        evidence.get(EVIDENCE_DIGEST_FIELD) not in evidences,
        review.get(REVIEW_DIGEST_FIELD) not in reviews,
        context.get("world_causal_attribution_verification_intake_nonce_digest")
        not in nonces,
        source_fact.get(SOURCE_FACT_DIGEST_FIELD) not in sources,
    )


def _route(
    evidence: Mapping[str, Any],
    review: Mapping[str, Any],
    evidence_duration_current: bool,
    evidence_independent: bool,
    review_duration_current: bool,
    checks: tuple[bool, ...],
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
    if not delay_current or not evidence_duration_current:
        return DISPOSITION_CONTEXT_REFRESH
    if not review_duration_current:
        return DISPOSITION_REVIEW_REFRESH
    if (
        evidence.get("generalized_truth_claimed")
        or evidence.get("causal_attribution_preconfirmed")
        or review.get("generalized_truth_claimed")
        or review.get("causal_attribution_preconfirmed")
        or not review.get("no_truth_generalization")
    ):
        return DISPOSITION_TRUTH_GENERALIZATION_REJECTED
    if (
        evidence.get("realized_dukkha_reduction_claimed")
        or review.get("realized_dukkha_reduction_claimed")
        or not review.get("no_dukkha_realization_overclaim")
    ):
        return DISPOSITION_DUKKHA_OVERCLAIM_REJECTED
    if not evidence_independent:
        return DISPOSITION_ADDITIONAL_EVIDENCE
    if not review.get("source_bounded_world_fact_confirmed"):
        return DISPOSITION_ADDITIONAL_EVIDENCE
    if not review.get("causal_model_adequate") or not review.get(
        "causal_query_exactly_bounded"
    ):
        return DISPOSITION_CAUSAL_MODEL_REPAIR
    if not review.get("intervention_correspondence_confirmed"):
        return DISPOSITION_INTERVENTION_REPAIR
    if not review.get("temporal_ordering_confirmed"):
        return DISPOSITION_TEMPORAL_REPAIR
    if not review.get("confounding_control_adequate"):
        return DISPOSITION_CONFOUNDING_REPAIR
    if not review.get("counterfactual_support_adequate"):
        return DISPOSITION_COUNTERFACTUAL_REPAIR
    if not review.get("alternative_causes_assessed"):
        return DISPOSITION_ALTERNATIVE_CAUSE_REVIEW
    if not review.get("selection_bias_adequate"):
        return DISPOSITION_SELECTION_BIAS_REVIEW
    if not review.get("measurement_validity_adequate"):
        return DISPOSITION_MEASUREMENT_REPAIR
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
    return DISPOSITION_SUPPORTED


def build_verifyos_dukkha_preserving_world_causal_attribution_verification_intake(
    *,
    source_world_fact_confirmation_receipt: Mapping[str, Any],
    expected_source_world_fact_confirmation_receipt_digest: str,
    source_world_postcondition_verification_receipt: Mapping[str, Any],
    expected_source_world_postcondition_verification_receipt_digest: str,
    source_world_mutation_application_receipt: Mapping[str, Any],
    expected_source_world_mutation_application_receipt_digest: str,
    world_causal_attribution_evidence_packet: Mapping[str, Any],
    expected_world_causal_attribution_evidence_packet_digest: str,
    world_causal_attribution_verification_review_certificate: Mapping[str, Any],
    expected_world_causal_attribution_verification_review_certificate_digest: str,
    world_causal_attribution_verification_intake_context: Mapping[str, Any],
    expected_world_causal_attribution_verification_intake_context_digest: str,
    world_causal_attribution_verification_policy_digest: str,
    world_causal_attribution_verification_responsibility_digest: str,
    world_causal_attribution_verification_request_id: str,
    world_causal_attribution_verification_bundle_digest: str,
) -> VerifyOSWorldCausalAttributionVerificationResult:
    blockers: list[str] = []
    source_fact = _map(source_world_fact_confirmation_receipt)
    source_verification = _map(source_world_postcondition_verification_receipt)
    source_mutation = _map(source_world_mutation_application_receipt)
    evidence = _map(world_causal_attribution_evidence_packet)
    review = _map(world_causal_attribution_verification_review_certificate)
    context = _map(world_causal_attribution_verification_intake_context)
    required_strings = {
        "expected_source_world_fact_confirmation_receipt_digest": (
            expected_source_world_fact_confirmation_receipt_digest
        ),
        "expected_source_world_postcondition_verification_receipt_digest": (
            expected_source_world_postcondition_verification_receipt_digest
        ),
        "expected_source_world_mutation_application_receipt_digest": (
            expected_source_world_mutation_application_receipt_digest
        ),
        "expected_world_causal_attribution_evidence_packet_digest": (
            expected_world_causal_attribution_evidence_packet_digest
        ),
        "expected_world_causal_attribution_verification_review_certificate_digest": (
            expected_world_causal_attribution_verification_review_certificate_digest
        ),
        "expected_world_causal_attribution_verification_intake_context_digest": (
            expected_world_causal_attribution_verification_intake_context_digest
        ),
        "world_causal_attribution_verification_policy_digest": (
            world_causal_attribution_verification_policy_digest
        ),
        "world_causal_attribution_verification_responsibility_digest": (
            world_causal_attribution_verification_responsibility_digest
        ),
        "world_causal_attribution_verification_request_id": (
            world_causal_attribution_verification_request_id
        ),
        "world_causal_attribution_verification_bundle_digest": (
            world_causal_attribution_verification_bundle_digest
        ),
    }
    for name, value in required_strings.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")
    mutation_digest, mutation_record, persisted, application_review = (
        _verify_source_mutation(
            source_mutation,
            expected_source_world_mutation_application_receipt_digest,
            blockers,
        )
    )
    verification_digest, source_postcondition_evidence = _verify_source_verification(
        source_verification,
        expected_source_world_postcondition_verification_receipt_digest,
        source_mutation,
        blockers,
    )
    (
        fact_digest,
        source_fact_review,
        source_fact_record,
        source_fact_debt,
        source_fact_binding,
        source_lineage,
        source_responsibility,
        source_epoch,
    ) = _verify_source_fact_confirmation(
        source_fact,
        expected_source_world_fact_confirmation_receipt_digest,
        source_verification,
        source_mutation,
        blockers,
    )
    evidence_digest, evidence_duration_current, evidence_independent = _verify_evidence(
        evidence,
        expected_world_causal_attribution_evidence_packet_digest,
        source_fact,
        source_verification,
        source_mutation,
        blockers,
    )
    review_digest, review_duration_current = _verify_review(
        review,
        expected_world_causal_attribution_verification_review_certificate_digest,
        source_fact,
        source_verification,
        source_mutation,
        evidence,
        blockers,
    )
    context_digest, checks = _verify_context(
        context,
        expected_world_causal_attribution_verification_intake_context_digest,
        source_fact,
        source_verification,
        source_mutation,
        evidence,
        review,
        source_epoch,
        blockers,
    )
    if not blockers:
        bundle = compute_world_causal_attribution_verification_bundle_digest(
            source_world_fact_confirmation_receipt_digest=fact_digest,
            expected_source_world_fact_confirmation_receipt_digest=(
                expected_source_world_fact_confirmation_receipt_digest
            ),
            source_world_postcondition_verification_receipt_digest=verification_digest,
            expected_source_world_postcondition_verification_receipt_digest=(
                expected_source_world_postcondition_verification_receipt_digest
            ),
            source_world_mutation_application_receipt_digest=mutation_digest,
            expected_source_world_mutation_application_receipt_digest=(
                expected_source_world_mutation_application_receipt_digest
            ),
            source_world_fact_confirmation_review_certificate_digest=source_fact.get(
                SOURCE_FACT_REVIEW_DIGEST_FIELD
            ),
            source_world_fact_confirmation_record_digest=source_fact.get(
                "world_fact_confirmation_record_digest"
            ),
            source_world_fact_confirmation_debt_consumption_record_digest=source_fact.get(
                "world_fact_confirmation_debt_consumption_record_digest"
            ),
            source_bounded_world_fact_status_binding_digest=source_fact.get(
                "bounded_world_fact_status_binding_digest"
            ),
            source_causal_attribution_verification_handoff_envelope_digest=source_fact.get(
                "causal_attribution_verification_handoff_envelope_digest"
            ),
            world_causal_attribution_evidence_packet_digest=evidence_digest,
            expected_world_causal_attribution_evidence_packet_digest=(
                expected_world_causal_attribution_evidence_packet_digest
            ),
            world_causal_attribution_verification_review_certificate_digest=review_digest,
            expected_world_causal_attribution_verification_review_certificate_digest=(
                expected_world_causal_attribution_verification_review_certificate_digest
            ),
            world_causal_attribution_verification_intake_context_digest=context_digest,
            expected_world_causal_attribution_verification_intake_context_digest=(
                expected_world_causal_attribution_verification_intake_context_digest
            ),
            requested_world_causal_attribution_verification_operation_digest=context.get(
                "requested_world_causal_attribution_verification_operation_digest"
            ),
            exact_world_causal_attribution_verification_cycle_digest=context.get(
                "exact_world_causal_attribution_verification_cycle_digest"
            ),
            world_causal_attribution_verification_policy_digest=(
                world_causal_attribution_verification_policy_digest
            ),
            world_causal_attribution_verification_responsibility_digest=(
                world_causal_attribution_verification_responsibility_digest
            ),
            world_causal_attribution_verification_request_id=(
                world_causal_attribution_verification_request_id
            ),
        )
        if bundle != world_causal_attribution_verification_bundle_digest:
            blockers.append("world_causal_attribution_verification_bundle_digest_mismatch")
    if blockers:
        return VerifyOSWorldCausalAttributionVerificationResult(
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
    causal_record = {
        "source_world_fact_confirmation_receipt_digest": fact_digest,
        "source_world_postcondition_verification_receipt_digest": verification_digest,
        "source_world_mutation_application_receipt_digest": mutation_digest,
        EVIDENCE_DIGEST_FIELD: evidence_digest,
        REVIEW_DIGEST_FIELD: review_digest,
        "source_bounded_world_fact_status_binding_digest": source_fact[
            "bounded_world_fact_status_binding_digest"
        ],
        "world_candidate_fact_digest": evidence["world_candidate_fact_digest"],
        "world_candidate_relation_digest": evidence["world_candidate_relation_digest"],
        "resulting_world_state_digest": evidence["resulting_world_state_digest"],
        "resulting_world_revision": evidence["resulting_world_revision"],
        "causal_model_digest": evidence["causal_model_digest"],
        "causal_query_digest": evidence["causal_query_digest"],
        "intervention_digest": evidence["intervention_digest"],
        "exposure_digest": evidence["exposure_digest"],
        "outcome_digest": evidence["outcome_digest"],
        "counterfactual_estimand_digest": evidence["counterfactual_estimand_digest"],
        "reviewer_id": review["reviewer_id"],
        "world_causal_attribution_verification_intake_session_id": context[
            "world_causal_attribution_verification_intake_session_id"
        ],
        "world_causal_attribution_verification_intake_nonce_digest": context[
            "world_causal_attribution_verification_intake_nonce_digest"
        ],
        "world_causal_attribution_verification_intake_epoch": context[
            "world_causal_attribution_verification_intake_epoch"
        ],
        "world_causal_attribution_verification_disposition": disposition,
        "state_before": STATE_BEFORE,
        "state_after": state_after,
        "bounded_world_fact_status": "confirmed_exact_bounded_proposition",
        "causal_attribution_status": (
            "confirmed_exact_bounded_relation_under_supplied_identification_assumptions"
            if supported
            else "pending_independent_verification"
        ),
        "dukkha_realization_state": "not_confirmed",
    }
    causal_record_digest = canonical_digest(causal_record)
    debt = {
        "source_world_fact_confirmation_receipt_digest": fact_digest,
        EVIDENCE_DIGEST_FIELD: evidence_digest,
        REVIEW_DIGEST_FIELD: review_digest,
        "world_causal_attribution_verification_record_digest": causal_record_digest,
        "world_causal_attribution_verification_debt_consumed": supported,
        "source_fact_confirmation_receipt_marked_causally_verified": supported,
        "double_world_causal_attribution_verification_performed": False,
    }
    debt_digest = canonical_digest(debt)
    causal_binding = None
    causal_binding_digest = ""
    dukkha_handoff = None
    dukkha_handoff_digest = ""
    if supported:
        causal_binding = {
            "source_world_fact_confirmation_receipt_digest": fact_digest,
            "world_causal_attribution_verification_record_digest": causal_record_digest,
            "world_causal_attribution_verification_debt_consumption_record_digest": (
                debt_digest
            ),
            "bounded_world_fact_status_binding_digest": source_fact[
                "bounded_world_fact_status_binding_digest"
            ],
            "world_candidate_fact_digest": evidence["world_candidate_fact_digest"],
            "world_candidate_relation_digest": evidence[
                "world_candidate_relation_digest"
            ],
            "resulting_world_state_digest": evidence["resulting_world_state_digest"],
            "resulting_world_revision": evidence["resulting_world_revision"],
            "causal_model_digest": evidence["causal_model_digest"],
            "causal_query_digest": evidence["causal_query_digest"],
            "intervention_digest": evidence["intervention_digest"],
            "counterfactual_estimand_digest": evidence[
                "counterfactual_estimand_digest"
            ],
            "identification_assumption_digests": evidence[
                "identification_assumption_digests"
            ],
            "confounder_set_digests": evidence["confounder_set_digests"],
            "adjustment_strategy_digest": evidence["adjustment_strategy_digest"],
            "uncertainty_digest": evidence["uncertainty_digest"],
            "calibration_digest": evidence["calibration_digest"],
            "provenance_chain_digests": evidence["provenance_chain_digests"],
            "causal_attribution_status": (
                "confirmed_exact_bounded_relation_under_supplied_identification_assumptions"
            ),
            "generalization_beyond_bound": False,
            "dukkha_realization_state": "not_confirmed",
        }
        causal_binding_digest = canonical_digest(causal_binding)
        dukkha_handoff = {
            "source_world_fact_confirmation_receipt_digest": fact_digest,
            "world_causal_attribution_verification_record_digest": causal_record_digest,
            "world_causal_attribution_verification_debt_consumption_record_digest": (
                debt_digest
            ),
            "bounded_world_causal_attribution_binding_digest": causal_binding_digest,
            "world_candidate_fact_digest": evidence["world_candidate_fact_digest"],
            "world_candidate_relation_digest": evidence[
                "world_candidate_relation_digest"
            ],
            "realized_dukkha_observation_digest": evidence[
                "realized_dukkha_observation_digest"
            ],
            "causal_attribution_state": "confirmed_exact_bounded_relation",
            "dukkha_realization_state": "pending_independent_verification",
            "dukkha_realization_verification_intake_admitted": True,
            "dukkha_realization_verification_receipt_required": True,
        }
        dukkha_handoff_digest = canonical_digest(dukkha_handoff)
    resulting_lineage = sorted(
        set(source_lineage)
        | {
            fact_digest,
            verification_digest,
            mutation_digest,
            source_fact[SOURCE_FACT_REVIEW_DIGEST_FIELD],
            source_fact["world_fact_confirmation_record_digest"],
            source_fact["world_fact_confirmation_debt_consumption_record_digest"],
            source_fact["bounded_world_fact_status_binding_digest"],
            source_fact["causal_attribution_verification_handoff_envelope_digest"],
            evidence_digest,
            review_digest,
            context_digest,
            context["requested_world_causal_attribution_verification_operation_digest"],
            context["exact_world_causal_attribution_verification_cycle_digest"],
            causal_record_digest,
            debt_digest,
            world_causal_attribution_verification_bundle_digest,
        }
        | ({causal_binding_digest} if causal_binding_digest else set())
        | ({dukkha_handoff_digest} if dukkha_handoff_digest else set())
    )
    resulting_responsibility = sorted(
        set(source_responsibility)
        | {
            review["reviewer_id"],
            world_causal_attribution_verification_responsibility_digest,
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
        "kernel": (
            "VerifyOS Dukkha-Preserving WORLD Causal-Attribution Verification Intake Kernel"
        ),
        "kernel_version": "v0.1",
        "verifyos_version": "v0.9",
        "status": "VERIFYOS_DUKKHA_PRESERVING_WORLD_CAUSAL_ATTRIBUTION_VERIFICATION_ROUTED",
        "source_world_fact_confirmation_receipt_digest": fact_digest,
        "source_world_postcondition_verification_receipt_digest": verification_digest,
        "source_world_mutation_application_receipt_digest": mutation_digest,
        "source_world_fact_confirmation_review_certificate_digest": source_fact[
            SOURCE_FACT_REVIEW_DIGEST_FIELD
        ],
        "source_world_fact_confirmation_intake_context_digest": source_fact[
            SOURCE_FACT_CONTEXT_DIGEST_FIELD
        ],
        "source_world_fact_confirmation_record_digest": source_fact[
            "world_fact_confirmation_record_digest"
        ],
        "source_world_fact_confirmation_debt_consumption_record_digest": source_fact[
            "world_fact_confirmation_debt_consumption_record_digest"
        ],
        "source_bounded_world_fact_status_binding_digest": source_fact[
            "bounded_world_fact_status_binding_digest"
        ],
        "source_causal_attribution_verification_handoff_envelope_digest": source_fact[
            "causal_attribution_verification_handoff_envelope_digest"
        ],
        "source_world_binding_digest": source_fact["source_world_binding_digest"],
        "source_world_model_state_digest": source_fact[
            "source_world_model_state_digest"
        ],
        "source_world_model_revision": source_fact["source_world_model_revision"],
        "source_persistent_world_storage_target_digest": source_fact[
            "source_persistent_world_storage_target_digest"
        ],
        "world_candidate_fact_digest": source_fact["world_candidate_fact_digest"],
        "world_candidate_relation_digest": source_fact[
            "world_candidate_relation_digest"
        ],
        "world_causal_attribution_evidence_packet": evidence,
        EVIDENCE_DIGEST_FIELD: evidence_digest,
        "world_causal_attribution_verification_review_certificate": review,
        REVIEW_DIGEST_FIELD: review_digest,
        CONTEXT_DIGEST_FIELD: context_digest,
        "world_causal_attribution_verification_policy_digest": (
            world_causal_attribution_verification_policy_digest
        ),
        "world_causal_attribution_verification_responsibility_digest": (
            world_causal_attribution_verification_responsibility_digest
        ),
        "world_causal_attribution_verification_request_id": (
            world_causal_attribution_verification_request_id
        ),
        "world_causal_attribution_verification_bundle_digest": (
            world_causal_attribution_verification_bundle_digest
        ),
        "world_causal_attribution_verification_disposition": disposition,
        "world_causal_attribution_verification_state_before": STATE_BEFORE,
        "world_causal_attribution_verification_state_after": state_after,
        "world_causal_attribution_verification_record": causal_record,
        "world_causal_attribution_verification_record_digest": causal_record_digest,
        "world_causal_attribution_verification_debt_consumption_record": debt,
        "world_causal_attribution_verification_debt_consumption_record_digest": debt_digest,
        "bounded_world_causal_attribution_binding": causal_binding,
        "bounded_world_causal_attribution_binding_digest": causal_binding_digest,
        "dukkha_realization_verification_handoff_envelope": dukkha_handoff,
        "dukkha_realization_verification_handoff_envelope_digest": dukkha_handoff_digest,
        "source_world_fact_confirmation_receipt_supplied": True,
        "source_world_fact_confirmation_receipt_fully_revalidated": True,
        "source_world_postcondition_verification_receipt_supplied": True,
        "source_world_postcondition_verification_receipt_fully_revalidated": True,
        "source_world_mutation_application_receipt_supplied": True,
        "source_world_mutation_application_receipt_fully_revalidated": True,
        "source_bounded_world_fact_confirmed": True,
        "source_bounded_world_fact_status_binding_bound": True,
        "source_causal_attribution_handoff_bound": True,
        "causal_model_bound": True,
        "causal_query_bound": True,
        "intervention_bound": True,
        "counterfactual_estimand_bound": True,
        "identification_assumptions_bound": True,
        "confounder_set_bound": True,
        "adjustment_strategy_bound": True,
        "temporal_ordering_evidence_bound": True,
        "counterfactual_support_evidence_bound": True,
        "alternative_cause_assessment_bound": True,
        "selection_bias_assessment_bound": True,
        "measurement_validity_assessment_bound": True,
        "uncertainty_bound": True,
        "calibration_bound": True,
        "provenance_bound": True,
        "protected_group_causal_impact_bound": True,
        "future_subject_causal_impact_bound": True,
        "realized_dukkha_observation_bound": True,
        "exactly_one_world_causal_attribution_verification_receipt_issued": True,
        "world_causal_attribution_verification_performed": True,
        "world_causal_attribution_verification_supported": supported,
        "world_causal_attribution_verification_debt_consumed": supported,
        "world_causal_attribution_verification_debt_replay_closed": supported,
        "world_causal_attribution_verification_double_consumed": False,
        "world_causal_attribution_evidence_packet_replay_closed": True,
        "world_causal_attribution_verification_review_certificate_replay_closed": True,
        "world_causal_attribution_verification_intake_nonce_consumed": True,
        "world_causal_attribution_verification_intake_nonce_replay_closed": True,
        "source_world_fact_confirmation_receipt_replay_closed": supported,
        "world_causal_attribution_verification_intake_session_replay_fresh_before_intake": (
            session_fresh
        ),
        "world_causal_attribution_evidence_replay_fresh_before_intake": evidence_fresh,
        "world_causal_attribution_verification_review_replay_fresh_before_intake": (
            review_fresh
        ),
        "world_causal_attribution_verification_intake_nonce_replay_fresh_before_intake": (
            nonce_fresh
        ),
        "source_world_fact_confirmation_receipt_replay_fresh_before_verification": (
            source_fresh
        ),
        "world_conditions_current": world_current,
        "world_causal_attribution_evidence_collection_duration_current": (
            evidence_duration_current
        ),
        "world_causal_attribution_verification_review_duration_current": (
            review_duration_current
        ),
        "world_causal_attribution_verification_intake_delay_current": delay_current,
        "world_causal_attribution_verification_debt_open": not supported,
        "bounded_world_fact_confirmed": True,
        "world_fact_confirmed": True,
        "world_fact_confirmation_scope_exactly_bounded": True,
        "generalized_world_truth_confirmed": False,
        "causal_attribution_confirmed": supported,
        "causal_attribution_scope_exactly_bounded": supported,
        "dukkha_realization_verification_intake_admitted": supported,
        "dukkha_realization_verification_receipt_required": supported,
        "dukkha_reduction_realized_confirmed": False,
        "persistent_world_model_state_unchanged_by_causal_verification": True,
        "persistent_world_state_changed_by_causal_verification": False,
        "world_model_revision_incremented_by_causal_verification": False,
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
    return VerifyOSWorldCausalAttributionVerificationResult(
        STATUS_READY, [], receipt
    )
