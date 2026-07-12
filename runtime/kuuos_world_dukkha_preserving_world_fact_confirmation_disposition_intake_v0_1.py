#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_verifyos_dukkha_preserving_world_postcondition_verification_intake_v0_1 import (
    CONTEXT_DIGEST_FIELD as SOURCE_VERIFICATION_CONTEXT_DIGEST_FIELD,
    EVIDENCE_DIGEST_FIELD as SOURCE_EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_VERIFICATION_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD as SOURCE_VERIFICATION_REVIEW_DIGEST_FIELD,
    SOURCE_DIGEST_FIELD as SOURCE_MUTATION_DIGEST_FIELD,
    canonical_digest,
    compute_world_postcondition_evidence_packet_digest,
    compute_world_postcondition_verification_review_certificate_digest,
)

STATUS_READY, STATUS_BLOCKED = "ready", "blocked"

RECEIPT_DIGEST_FIELD = (
    "world_dukkha_preserving_world_fact_confirmation_disposition_intake_receipt_digest"
)
REVIEW_DIGEST_FIELD = "world_fact_confirmation_review_certificate_digest"
CONTEXT_DIGEST_FIELD = "world_fact_confirmation_intake_context_digest"

STATE_BEFORE = "world_candidate_commit_postcondition_verified_world_fact_confirmation_pending"
STATE_AFTER_SUPPORTED = "world_candidate_bounded_fact_confirmed_causal_attribution_pending"

DISPOSITION_SUPPORTED = "world_fact_confirmation_supported"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_CONTEXT_REFRESH = "fact_confirmation_context_refresh_required"
DISPOSITION_REVIEW_REFRESH = "fact_confirmation_review_refresh_required"
DISPOSITION_ADDITIONAL_EVIDENCE = "additional_postcondition_evidence_required"
DISPOSITION_FACT_REPAIR = "candidate_fact_correspondence_repair_required"
DISPOSITION_RELATION_REPAIR = "candidate_relation_correspondence_repair_required"
DISPOSITION_STATE_REPAIR = "world_state_correspondence_repair_required"
DISPOSITION_REVISION_REPAIR = "world_revision_correspondence_repair_required"
DISPOSITION_STORAGE_REPAIR = "storage_persistence_repair_required"
DISPOSITION_CALIBRATION_REPAIR = "calibration_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "provenance_repair_required"
DISPOSITION_NONEXTERNALIZATION_REVIEW = "nonexternalization_review_required"
DISPOSITION_CAUSAL_OVERCLAIM_REJECTED = "causal_attribution_overclaim_rejected"
DISPOSITION_DUKKHA_OVERCLAIM_REJECTED = "dukkha_realization_overclaim_rejected"
DISPOSITION_TRUTH_PROMOTION_REJECTED = "truth_promotion_rejected"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"

REVIEW_FIELDS = {
    "source_world_postcondition_verification_receipt_digest",
    "source_world_mutation_application_receipt_digest",
    "source_world_postcondition_evidence_packet_digest",
    "source_world_postcondition_verification_review_certificate_digest",
    "source_world_postcondition_verification_record_digest",
    "source_world_postcondition_verification_debt_consumption_record_digest",
    "source_world_fact_confirmation_handoff_envelope_digest",
    "source_world_mutation_record_digest",
    "source_persisted_world_candidate_envelope_digest",
    "world_mutation_transaction_digest",
    "world_candidate_fact_digest",
    "world_candidate_relation_digest",
    "resulting_world_state_digest",
    "resulting_world_revision",
    "persistent_world_storage_target_digest",
    "expected_world_update_postcondition_digest",
    "uncertainty_digest",
    "calibration_digest",
    "provenance_chain_digests",
    "protected_group_observed_impact_digest",
    "future_subject_observed_impact_digest",
    "realized_dukkha_observation_digest",
    "fact_confirmation_reviewer_id",
    "fact_confirmation_method_digest",
    "fact_confirmation_evidence_digest",
    "fact_confirmation_review_started_epoch",
    "fact_confirmation_review_completed_epoch",
    "maximum_fact_confirmation_review_duration",
    "source_postcondition_verification_supported",
    "postcondition_evidence_sufficient",
    "candidate_fact_correspondence_confirmed",
    "candidate_relation_correspondence_confirmed",
    "world_state_correspondence_confirmed",
    "world_revision_correspondence_confirmed",
    "storage_persistence_confirmed",
    "calibration_adequate",
    "provenance_continuity_preserved",
    "protected_group_nonexternalization_supported",
    "future_nonexternalization_supported",
    "exact_bounded_fact_scope_preserved",
    "generalized_truth_claimed",
    "causal_attribution_claimed",
    "realized_dukkha_reduction_claimed",
    REVIEW_DIGEST_FIELD,
}

CONTEXT_FIELDS = {
    "source_world_postcondition_verification_receipt_digest",
    "source_world_mutation_application_receipt_digest",
    REVIEW_DIGEST_FIELD,
    "current_world_binding_digest",
    "current_world_model_state_digest",
    "current_world_model_revision",
    "current_persistent_world_storage_target_digest",
    "current_world_lineage_digest",
    "source_postcondition_verification_epoch",
    "world_fact_confirmation_intake_epoch",
    "maximum_world_fact_confirmation_intake_delay",
    "world_fact_confirmation_intake_session_id",
    "world_fact_confirmation_intake_nonce_digest",
    "prior_world_fact_confirmation_intake_session_ids",
    "prior_world_fact_confirmation_review_certificate_digests",
    "prior_world_fact_confirmation_intake_nonce_digests",
    "prior_confirmed_world_postcondition_verification_receipt_digests",
    "requested_world_fact_confirmation_operation_digest",
    "exact_world_fact_confirmation_cycle_digest",
    CONTEXT_DIGEST_FIELD,
}


@dataclass
class WORLDWorldFactConfirmationDispositionResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def _map(value: Any) -> dict:
    return dict(value) if isinstance(value, Mapping) else {}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    item = dict(value)
    item.pop(field, None)
    return canonical_digest(item)


def compute_world_fact_confirmation_review_certificate_digest(
    value: Mapping[str, Any],
) -> str:
    return _digest_without(value, REVIEW_DIGEST_FIELD)


def compute_world_fact_confirmation_intake_context_digest(
    value: Mapping[str, Any],
) -> str:
    return _digest_without(value, CONTEXT_DIGEST_FIELD)


def compute_world_fact_confirmation_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def _strings(value: Any, allow_empty: bool = False) -> tuple[bool, list[str]]:
    ok = isinstance(value, list) and (allow_empty or bool(value)) and all(
        isinstance(item, str) and item for item in value
    )
    items = list(value) if isinstance(value, list) else []
    return ok and items == sorted(items) and len(items) == len(set(items)), items


def compute_requested_world_fact_confirmation_operation_digest(
    source_verification: Mapping[str, Any],
    source_mutation: Mapping[str, Any],
    review: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_world_postcondition_verification_receipt_digest": (
                source_verification.get(SOURCE_VERIFICATION_DIGEST_FIELD)
            ),
            "source_world_mutation_application_receipt_digest": source_mutation.get(
                SOURCE_MUTATION_DIGEST_FIELD
            ),
            "world_candidate_fact_digest": review.get("world_candidate_fact_digest"),
            "world_candidate_relation_digest": review.get(
                "world_candidate_relation_digest"
            ),
            "resulting_world_state_digest": review.get("resulting_world_state_digest"),
            "resulting_world_revision": review.get("resulting_world_revision"),
            "state_before": STATE_BEFORE,
            "supported_state_after": STATE_AFTER_SUPPORTED,
        }
    )


def compute_exact_world_fact_confirmation_cycle_digest(
    source_verification: Mapping[str, Any],
    source_mutation: Mapping[str, Any],
    review: Mapping[str, Any],
    context: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_world_postcondition_verification_receipt_digest": (
                source_verification.get(SOURCE_VERIFICATION_DIGEST_FIELD)
            ),
            "source_world_mutation_application_receipt_digest": source_mutation.get(
                SOURCE_MUTATION_DIGEST_FIELD
            ),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
            "world_fact_confirmation_intake_session_id": context.get(
                "world_fact_confirmation_intake_session_id"
            ),
            "world_fact_confirmation_intake_nonce_digest": context.get(
                "world_fact_confirmation_intake_nonce_digest"
            ),
            "world_fact_confirmation_intake_epoch": context.get(
                "world_fact_confirmation_intake_epoch"
            ),
            "current_world_model_revision": context.get("current_world_model_revision"),
            "requested_world_fact_confirmation_operation_digest": context.get(
                "requested_world_fact_confirmation_operation_digest"
            ),
        }
    )


def _verify_source_mutation(
    source: dict,
    expected: str,
    blockers: list[str],
) -> tuple[str, dict, dict, dict, dict, list[str], list[str]]:
    if not source:
        blockers.append("source_world_mutation_application_receipt_missing")
        return "", {}, {}, {}, {}, [], []

    digest = source.get(SOURCE_MUTATION_DIGEST_FIELD, "")
    if not digest:
        blockers.append("source_world_mutation_application_receipt_digest_missing")
    elif digest != _digest_without(source, SOURCE_MUTATION_DIGEST_FIELD):
        blockers.append("source_world_mutation_application_receipt_digest_mismatch")
    if digest != expected:
        blockers.append("source_world_mutation_application_expected_binding_mismatch")

    expected_fields = {
        "kernel_version": "v0.1",
        "world_version": "v0.62",
        "status": "WORLD_DUKKHA_PRESERVING_SINGLE_USE_WORLD_MUTATION_APPLICATION_ROUTED",
        "world_mutation_application_disposition": "world_mutation_application_ready",
        "world_mutation_application_state_after": (
            "world_candidate_commit_applied_world_fact_unconfirmed"
        ),
        "world_mutation_application_completed": True,
        "exactly_one_world_patch_applied": True,
        "world_mutation_transaction_atomic": True,
        "world_candidate_commit_completed": True,
        "single_use_world_candidate_commit_authorization_consumed": True,
        "persistent_world_model_state_changed": True,
        "world_model_revision_incremented_exactly_once": True,
        "world_postcondition_verification_completed": False,
        "world_postcondition_verification_debt_open": True,
        "world_fact_confirmed": False,
        "causal_attribution_confirmed": False,
        "dukkha_reduction_realized_confirmed": False,
        "tool_invocation_performed": False,
        "external_side_effect_performed": False,
        "general_world_mutation_authority_granted": False,
        "world_mutation_authority_granted": False,
    }
    for key, value in expected_fields.items():
        if source.get(key) != value:
            blockers.append(f"source_mutation_boundary_{key}_mismatch")

    mutation_record = _map(source.get("world_mutation_record"))
    persisted = _map(source.get("persisted_world_candidate_envelope"))
    handoff = _map(source.get("world_postcondition_verification_handoff_envelope"))
    application_review = _map(source.get("world_mutation_application_review_certificate"))

    for name, item, field in (
        ("world_mutation_record", mutation_record, "world_mutation_record_digest"),
        (
            "persisted_world_candidate_envelope",
            persisted,
            "persisted_world_candidate_envelope_digest",
        ),
        (
            "world_postcondition_verification_handoff_envelope",
            handoff,
            "world_postcondition_verification_handoff_envelope_digest",
        ),
    ):
        if not item:
            blockers.append(f"source_mutation_{name}_missing")
        elif source.get(field) != canonical_digest(item):
            blockers.append(f"source_mutation_{name}_digest_mismatch")

    required_persisted = {
        "world_candidate_commit_state": "applied_persisted_world_fact_unconfirmed",
        "world_fact_state": "persisted_candidate_not_verified_fact",
        "causal_attribution_state": "not_confirmed",
        "dukkha_realization_state": "not_confirmed",
        "postcondition_verification_intake_admitted": True,
        "postcondition_verification_receipt_required": True,
    }
    for key, value in required_persisted.items():
        if persisted.get(key) != value:
            blockers.append(f"source_mutation_persisted_{key}_mismatch")

    storage_target = application_review.get("persistent_world_storage_target_digest")
    if not isinstance(storage_target, str) or not storage_target:
        blockers.append("source_mutation_persistent_world_storage_target_invalid")

    cross_bindings = {
        "world_mutation_record_digest": source.get("world_mutation_record_digest"),
        "persisted_world_candidate_envelope_digest": source.get(
            "persisted_world_candidate_envelope_digest"
        ),
        "world_mutation_transaction_digest": mutation_record.get(
            "world_mutation_transaction_digest"
        ),
        "world_state_after_digest": persisted.get("world_state_after_digest"),
        "world_model_revision_after": persisted.get("world_model_revision_after"),
        "world_update_postcondition_digest": mutation_record.get(
            "world_update_postcondition_digest"
        ),
    }
    for key, value in cross_bindings.items():
        if handoff.get(key) != value:
            blockers.append(f"source_mutation_handoff_{key}_mismatch")

    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_mutation_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_mutation_resulting_responsibility_invalid")

    return (
        digest,
        mutation_record,
        persisted,
        handoff,
        application_review,
        lineage,
        responsibility,
    )


def _verify_source_verification(
    source: dict,
    expected: str,
    source_mutation: dict,
    blockers: list[str],
) -> tuple[str, dict, dict, dict, dict, dict, list[str], list[str], int]:
    if not source:
        blockers.append("source_world_postcondition_verification_receipt_missing")
        return "", {}, {}, {}, {}, {}, [], [], 0

    digest = source.get(SOURCE_VERIFICATION_DIGEST_FIELD, "")
    if not digest:
        blockers.append("source_world_postcondition_verification_receipt_digest_missing")
    elif digest != _digest_without(source, SOURCE_VERIFICATION_DIGEST_FIELD):
        blockers.append("source_world_postcondition_verification_receipt_digest_mismatch")
    if digest != expected:
        blockers.append("source_world_postcondition_verification_expected_binding_mismatch")

    expected_fields = {
        "kernel_version": "v0.1",
        "verifyos_version": "v0.8",
        "status": "VERIFYOS_DUKKHA_PRESERVING_WORLD_POSTCONDITION_VERIFICATION_ROUTED",
        "world_postcondition_verification_disposition": (
            "world_postcondition_verification_supported"
        ),
        "world_postcondition_verification_state_after": STATE_BEFORE,
        "source_world_mutation_application_receipt_fully_revalidated": True,
        "world_postcondition_verification_supported": True,
        "world_postcondition_verification_debt_consumed": True,
        "world_postcondition_verification_debt_replay_closed": True,
        "source_world_mutation_application_receipt_replay_closed": True,
        "world_postcondition_verification_debt_open": False,
        "world_fact_confirmation_intake_admitted": True,
        "world_fact_confirmation_receipt_required": True,
        "world_fact_confirmation_completed": False,
        "persistent_world_model_state_unchanged_by_verifier": True,
        "persistent_world_state_changed_by_verifier": False,
        "world_fact_confirmed": False,
        "causal_attribution_confirmed": False,
        "dukkha_reduction_realized_confirmed": False,
        "world_mutation_reperformed": False,
        "tool_invocation_performed": False,
        "external_side_effect_performed": False,
        "automatic_truth_promotion": False,
        "general_execution_authority_granted": False,
        "world_mutation_authority_granted": False,
    }
    for key, value in expected_fields.items():
        if source.get(key) != value:
            blockers.append(f"source_verification_boundary_{key}_mismatch")

    if source.get("source_world_mutation_application_receipt_digest") != source_mutation.get(
        SOURCE_MUTATION_DIGEST_FIELD
    ):
        blockers.append("source_verification_mutation_receipt_binding_mismatch")

    evidence = _map(source.get("world_postcondition_evidence_packet"))
    verification_review = _map(
        source.get("world_postcondition_verification_review_certificate")
    )
    verification_record = _map(source.get("world_postcondition_verification_record"))
    debt = _map(source.get("world_postcondition_verification_debt_consumption_record"))
    handoff = _map(source.get("world_fact_confirmation_handoff_envelope"))

    if not evidence:
        blockers.append("source_verification_world_postcondition_evidence_packet_missing")
    elif source.get(SOURCE_EVIDENCE_DIGEST_FIELD) != (
        compute_world_postcondition_evidence_packet_digest(evidence)
    ):
        blockers.append(
            "source_verification_world_postcondition_evidence_packet_digest_mismatch"
        )

    if not verification_review:
        blockers.append(
            "source_verification_world_postcondition_verification_review_certificate_missing"
        )
    elif source.get(SOURCE_VERIFICATION_REVIEW_DIGEST_FIELD) != (
        compute_world_postcondition_verification_review_certificate_digest(
            verification_review
        )
    ):
        blockers.append(
            "source_verification_world_postcondition_verification_review_certificate_digest_mismatch"
        )

    for name, item, field in (
        (
            "world_postcondition_verification_record",
            verification_record,
            "world_postcondition_verification_record_digest",
        ),
        (
            "world_postcondition_verification_debt_consumption_record",
            debt,
            "world_postcondition_verification_debt_consumption_record_digest",
        ),
        (
            "world_fact_confirmation_handoff_envelope",
            handoff,
            "world_fact_confirmation_handoff_envelope_digest",
        ),
    ):
        if not item:
            blockers.append(f"source_verification_{name}_missing")
        elif source.get(field) != canonical_digest(item):
            blockers.append(f"source_verification_{name}_digest_mismatch")

    if source.get(SOURCE_VERIFICATION_CONTEXT_DIGEST_FIELD) in (None, ""):
        blockers.append("source_verification_context_digest_missing")

    mutation_record = _map(source_mutation.get("world_mutation_record"))
    persisted = _map(source_mutation.get("persisted_world_candidate_envelope"))
    application_review = _map(
        source_mutation.get("world_mutation_application_review_certificate")
    )

    bindings = {
        "source_world_mutation_application_receipt_digest": source_mutation.get(
            SOURCE_MUTATION_DIGEST_FIELD
        ),
        "world_postcondition_verification_record_digest": source.get(
            "world_postcondition_verification_record_digest"
        ),
        "world_postcondition_verification_debt_consumption_record_digest": source.get(
            "world_postcondition_verification_debt_consumption_record_digest"
        ),
        SOURCE_EVIDENCE_DIGEST_FIELD: source.get(SOURCE_EVIDENCE_DIGEST_FIELD),
        SOURCE_VERIFICATION_REVIEW_DIGEST_FIELD: source.get(
            SOURCE_VERIFICATION_REVIEW_DIGEST_FIELD
        ),
        "world_mutation_record_digest": source_mutation.get("world_mutation_record_digest"),
        "persisted_world_candidate_envelope_digest": source_mutation.get(
            "persisted_world_candidate_envelope_digest"
        ),
        "world_candidate_fact_digest": persisted.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": persisted.get(
            "world_candidate_relation_digest"
        ),
        "world_mutation_transaction_digest": mutation_record.get(
            "world_mutation_transaction_digest"
        ),
        "world_update_postcondition_digest": mutation_record.get(
            "world_update_postcondition_digest"
        ),
        "world_state_after_digest": persisted.get("world_state_after_digest"),
        "world_model_revision_after": persisted.get("world_model_revision_after"),
    }
    for key, value in bindings.items():
        if handoff.get(key) != value:
            blockers.append(f"source_fact_confirmation_handoff_{key}_mismatch")

    if evidence.get("uncertainty_digest") in (None, ""):
        blockers.append("source_evidence_uncertainty_digest_missing")
    if evidence.get("calibration_digest") in (None, ""):
        blockers.append("source_evidence_calibration_digest_missing")
    provenance_ok, _ = _strings(evidence.get("provenance_chain_digests"))
    if not provenance_ok:
        blockers.append("source_evidence_provenance_chain_invalid")
    for field in (
        "protected_group_observed_impact_digest",
        "future_subject_observed_impact_digest",
        "realized_dukkha_observation_digest",
    ):
        if not isinstance(evidence.get(field), str) or not evidence.get(field):
            blockers.append(f"source_evidence_{field}_invalid")

    if application_review.get("persistent_world_storage_target_digest") in (None, ""):
        blockers.append("source_verification_storage_target_missing")

    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_verification_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_verification_resulting_responsibility_invalid")

    verification_epoch = verification_record.get(
        "world_postcondition_verification_intake_epoch"
    )
    if not isinstance(verification_epoch, int) or isinstance(verification_epoch, bool):
        blockers.append("source_verification_epoch_invalid")
        verification_epoch = 0

    return (
        digest,
        evidence,
        verification_review,
        verification_record,
        debt,
        handoff,
        lineage,
        responsibility,
        verification_epoch,
    )


def _verify_review(
    review: dict,
    expected: str,
    source_verification: dict,
    source_mutation: dict,
    blockers: list[str],
) -> tuple[str, bool]:
    if not review:
        blockers.append("world_fact_confirmation_review_certificate_missing")
        return "", False
    if set(review) != REVIEW_FIELDS:
        blockers.append("world_fact_confirmation_review_certificate_schema_invalid")

    digest = review.get(REVIEW_DIGEST_FIELD, "")
    if not digest:
        blockers.append("world_fact_confirmation_review_certificate_digest_missing")
    elif digest != compute_world_fact_confirmation_review_certificate_digest(review):
        blockers.append("world_fact_confirmation_review_certificate_digest_mismatch")
    if digest != expected:
        blockers.append("world_fact_confirmation_review_expected_binding_mismatch")

    evidence = _map(source_verification.get("world_postcondition_evidence_packet"))
    source_review = _map(
        source_verification.get("world_postcondition_verification_review_certificate")
    )
    verification_record = _map(
        source_verification.get("world_postcondition_verification_record")
    )
    debt = _map(
        source_verification.get("world_postcondition_verification_debt_consumption_record")
    )
    handoff = _map(source_verification.get("world_fact_confirmation_handoff_envelope"))
    mutation_record = _map(source_mutation.get("world_mutation_record"))
    persisted = _map(source_mutation.get("persisted_world_candidate_envelope"))
    application_review = _map(
        source_mutation.get("world_mutation_application_review_certificate")
    )

    bindings = {
        "source_world_postcondition_verification_receipt_digest": (
            source_verification.get(SOURCE_VERIFICATION_DIGEST_FIELD)
        ),
        "source_world_mutation_application_receipt_digest": source_mutation.get(
            SOURCE_MUTATION_DIGEST_FIELD
        ),
        "source_world_postcondition_evidence_packet_digest": source_verification.get(
            SOURCE_EVIDENCE_DIGEST_FIELD
        ),
        "source_world_postcondition_verification_review_certificate_digest": (
            source_verification.get(SOURCE_VERIFICATION_REVIEW_DIGEST_FIELD)
        ),
        "source_world_postcondition_verification_record_digest": source_verification.get(
            "world_postcondition_verification_record_digest"
        ),
        "source_world_postcondition_verification_debt_consumption_record_digest": (
            source_verification.get(
                "world_postcondition_verification_debt_consumption_record_digest"
            )
        ),
        "source_world_fact_confirmation_handoff_envelope_digest": source_verification.get(
            "world_fact_confirmation_handoff_envelope_digest"
        ),
        "source_world_mutation_record_digest": source_mutation.get(
            "world_mutation_record_digest"
        ),
        "source_persisted_world_candidate_envelope_digest": source_mutation.get(
            "persisted_world_candidate_envelope_digest"
        ),
        "world_mutation_transaction_digest": mutation_record.get(
            "world_mutation_transaction_digest"
        ),
        "world_candidate_fact_digest": persisted.get("world_candidate_fact_digest"),
        "world_candidate_relation_digest": persisted.get(
            "world_candidate_relation_digest"
        ),
        "resulting_world_state_digest": persisted.get("world_state_after_digest"),
        "resulting_world_revision": persisted.get("world_model_revision_after"),
        "persistent_world_storage_target_digest": application_review.get(
            "persistent_world_storage_target_digest"
        ),
        "expected_world_update_postcondition_digest": mutation_record.get(
            "world_update_postcondition_digest"
        ),
        "uncertainty_digest": evidence.get("uncertainty_digest"),
        "calibration_digest": evidence.get("calibration_digest"),
        "provenance_chain_digests": evidence.get("provenance_chain_digests"),
        "protected_group_observed_impact_digest": evidence.get(
            "protected_group_observed_impact_digest"
        ),
        "future_subject_observed_impact_digest": evidence.get(
            "future_subject_observed_impact_digest"
        ),
        "realized_dukkha_observation_digest": evidence.get(
            "realized_dukkha_observation_digest"
        ),
    }
    for key, value in bindings.items():
        if review.get(key) != value:
            blockers.append(f"world_fact_confirmation_review_{key}_mismatch")

    for field in (
        "fact_confirmation_reviewer_id",
        "fact_confirmation_method_digest",
        "fact_confirmation_evidence_digest",
    ):
        if not isinstance(review.get(field), str) or not review.get(field):
            blockers.append(f"world_fact_confirmation_review_{field}_invalid")

    for field in (
        "fact_confirmation_review_started_epoch",
        "fact_confirmation_review_completed_epoch",
        "maximum_fact_confirmation_review_duration",
        "resulting_world_revision",
    ):
        value = review.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"world_fact_confirmation_review_{field}_invalid")

    boolean_fields = REVIEW_FIELDS - {
        REVIEW_DIGEST_FIELD,
        "source_world_postcondition_verification_receipt_digest",
        "source_world_mutation_application_receipt_digest",
        "source_world_postcondition_evidence_packet_digest",
        "source_world_postcondition_verification_review_certificate_digest",
        "source_world_postcondition_verification_record_digest",
        "source_world_postcondition_verification_debt_consumption_record_digest",
        "source_world_fact_confirmation_handoff_envelope_digest",
        "source_world_mutation_record_digest",
        "source_persisted_world_candidate_envelope_digest",
        "world_mutation_transaction_digest",
        "world_candidate_fact_digest",
        "world_candidate_relation_digest",
        "resulting_world_state_digest",
        "resulting_world_revision",
        "persistent_world_storage_target_digest",
        "expected_world_update_postcondition_digest",
        "uncertainty_digest",
        "calibration_digest",
        "provenance_chain_digests",
        "protected_group_observed_impact_digest",
        "future_subject_observed_impact_digest",
        "realized_dukkha_observation_digest",
        "fact_confirmation_reviewer_id",
        "fact_confirmation_method_digest",
        "fact_confirmation_evidence_digest",
        "fact_confirmation_review_started_epoch",
        "fact_confirmation_review_completed_epoch",
        "maximum_fact_confirmation_review_duration",
    }
    for field in boolean_fields:
        if not isinstance(review.get(field), bool):
            blockers.append(f"world_fact_confirmation_review_{field}_invalid")

    if review.get("source_postcondition_verification_supported") is not True:
        blockers.append("world_fact_confirmation_review_source_not_supported")
    if verification_record.get("world_postcondition_verification_disposition") != (
        "world_postcondition_verification_supported"
    ):
        blockers.append("world_fact_confirmation_source_verification_record_not_supported")
    if debt.get("world_postcondition_verification_debt_consumed") is not True:
        blockers.append("world_fact_confirmation_source_verification_debt_not_consumed")
    if source_review.get("world_postcondition_satisfied") is not True:
        blockers.append("world_fact_confirmation_source_postcondition_not_satisfied")
    if handoff.get("world_fact_state") != (
        "postcondition_verified_fact_confirmation_pending"
    ):
        blockers.append("world_fact_confirmation_source_handoff_state_invalid")

    start = review.get("fact_confirmation_review_started_epoch")
    end = review.get("fact_confirmation_review_completed_epoch")
    maximum = review.get("maximum_fact_confirmation_review_duration")
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
    source_verification: dict,
    source_mutation: dict,
    review: dict,
    source_verification_epoch: int,
    blockers: list[str],
) -> tuple[str, tuple[bool, ...]]:
    if not context:
        blockers.append("world_fact_confirmation_intake_context_missing")
        return "", (False,) * 6
    if set(context) != CONTEXT_FIELDS:
        blockers.append("world_fact_confirmation_intake_context_schema_invalid")

    digest = context.get(CONTEXT_DIGEST_FIELD, "")
    if not digest:
        blockers.append("world_fact_confirmation_intake_context_digest_missing")
    elif digest != compute_world_fact_confirmation_intake_context_digest(context):
        blockers.append("world_fact_confirmation_intake_context_digest_mismatch")
    if digest != expected:
        blockers.append("world_fact_confirmation_context_expected_binding_mismatch")

    for key, value in {
        "source_world_postcondition_verification_receipt_digest": (
            source_verification.get(SOURCE_VERIFICATION_DIGEST_FIELD)
        ),
        "source_world_mutation_application_receipt_digest": source_mutation.get(
            SOURCE_MUTATION_DIGEST_FIELD
        ),
        REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
    }.items():
        if context.get(key) != value:
            blockers.append(f"world_fact_confirmation_context_{key}_mismatch")

    for field in (
        "current_world_binding_digest",
        "current_world_model_state_digest",
        "current_persistent_world_storage_target_digest",
        "current_world_lineage_digest",
        "world_fact_confirmation_intake_session_id",
        "world_fact_confirmation_intake_nonce_digest",
        "requested_world_fact_confirmation_operation_digest",
        "exact_world_fact_confirmation_cycle_digest",
    ):
        if not isinstance(context.get(field), str) or not context.get(field):
            blockers.append(f"world_fact_confirmation_context_{field}_invalid")

    for field in (
        "current_world_model_revision",
        "source_postcondition_verification_epoch",
        "world_fact_confirmation_intake_epoch",
        "maximum_world_fact_confirmation_intake_delay",
    ):
        value = context.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"world_fact_confirmation_context_{field}_invalid")

    persisted = _map(source_mutation.get("persisted_world_candidate_envelope"))
    application_review = _map(
        source_mutation.get("world_mutation_application_review_certificate")
    )
    expected_lineage = canonical_digest(source_verification.get("resulting_lineage_digests", []))
    world_current = all(
        context.get(key) == value
        for key, value in {
            "current_world_binding_digest": source_verification.get(
                "source_world_binding_digest"
            ),
            "current_world_model_state_digest": persisted.get("world_state_after_digest"),
            "current_world_model_revision": persisted.get("world_model_revision_after"),
            "current_persistent_world_storage_target_digest": application_review.get(
                "persistent_world_storage_target_digest"
            ),
            "current_world_lineage_digest": expected_lineage,
        }.items()
    )

    if context.get("source_postcondition_verification_epoch") != source_verification_epoch:
        blockers.append("world_fact_confirmation_context_source_epoch_mismatch")
    if context.get(
        "requested_world_fact_confirmation_operation_digest"
    ) != compute_requested_world_fact_confirmation_operation_digest(
        source_verification, source_mutation, review
    ):
        blockers.append("world_fact_confirmation_context_operation_digest_mismatch")
    if context.get(
        "exact_world_fact_confirmation_cycle_digest"
    ) != compute_exact_world_fact_confirmation_cycle_digest(
        source_verification, source_mutation, review, context
    ):
        blockers.append("world_fact_confirmation_context_cycle_digest_mismatch")

    verified = context.get("source_postcondition_verification_epoch")
    epoch = context.get("world_fact_confirmation_intake_epoch")
    maximum = context.get("maximum_world_fact_confirmation_intake_delay")
    delay_current = (
        all(
            isinstance(value, int) and not isinstance(value, bool)
            for value in (verified, epoch, maximum)
        )
        and 1 <= maximum <= 64
        and 0 <= epoch - verified <= maximum
    )

    values = []
    for field in (
        "prior_world_fact_confirmation_intake_session_ids",
        "prior_world_fact_confirmation_review_certificate_digests",
        "prior_world_fact_confirmation_intake_nonce_digests",
        "prior_confirmed_world_postcondition_verification_receipt_digests",
    ):
        ok, items = _strings(context.get(field), True)
        if not ok:
            blockers.append(f"world_fact_confirmation_context_{field}_invalid")
        values.append(items)
    sessions, reviews, nonces, sources = values

    return digest, (
        world_current,
        delay_current,
        context.get("world_fact_confirmation_intake_session_id") not in sessions,
        review.get(REVIEW_DIGEST_FIELD) not in reviews,
        context.get("world_fact_confirmation_intake_nonce_digest") not in nonces,
        source_verification.get(SOURCE_VERIFICATION_DIGEST_FIELD) not in sources,
    )


def _route(
    review: Mapping[str, Any],
    review_duration_current: bool,
    checks: tuple[bool, ...],
) -> str:
    (
        world_current,
        delay_current,
        session_fresh,
        review_fresh,
        nonce_fresh,
        source_fresh,
    ) = checks

    if not all((session_fresh, review_fresh, nonce_fresh, source_fresh)):
        return DISPOSITION_REPLAY_REJECTED
    if not world_current:
        return DISPOSITION_WORLD_REFRESH
    if not delay_current:
        return DISPOSITION_CONTEXT_REFRESH
    if not review_duration_current:
        return DISPOSITION_REVIEW_REFRESH
    if review.get("causal_attribution_claimed"):
        return DISPOSITION_CAUSAL_OVERCLAIM_REJECTED
    if review.get("realized_dukkha_reduction_claimed"):
        return DISPOSITION_DUKKHA_OVERCLAIM_REJECTED
    if review.get("generalized_truth_claimed") or not review.get(
        "exact_bounded_fact_scope_preserved"
    ):
        return DISPOSITION_TRUTH_PROMOTION_REJECTED
    if not review.get("postcondition_evidence_sufficient"):
        return DISPOSITION_ADDITIONAL_EVIDENCE
    if not review.get("candidate_fact_correspondence_confirmed"):
        return DISPOSITION_FACT_REPAIR
    if not review.get("candidate_relation_correspondence_confirmed"):
        return DISPOSITION_RELATION_REPAIR
    if not review.get("world_state_correspondence_confirmed"):
        return DISPOSITION_STATE_REPAIR
    if not review.get("world_revision_correspondence_confirmed"):
        return DISPOSITION_REVISION_REPAIR
    if not review.get("storage_persistence_confirmed"):
        return DISPOSITION_STORAGE_REPAIR
    if not review.get("calibration_adequate"):
        return DISPOSITION_CALIBRATION_REPAIR
    if not review.get("provenance_continuity_preserved"):
        return DISPOSITION_PROVENANCE_REPAIR
    if not review.get("protected_group_nonexternalization_supported") or not review.get(
        "future_nonexternalization_supported"
    ):
        return DISPOSITION_NONEXTERNALIZATION_REVIEW
    return DISPOSITION_SUPPORTED


def build_world_dukkha_preserving_world_fact_confirmation_disposition_intake(
    *,
    source_world_postcondition_verification_receipt: Mapping[str, Any],
    expected_source_world_postcondition_verification_receipt_digest: str,
    source_world_mutation_application_receipt: Mapping[str, Any],
    expected_source_world_mutation_application_receipt_digest: str,
    world_fact_confirmation_review_certificate: Mapping[str, Any],
    expected_world_fact_confirmation_review_certificate_digest: str,
    world_fact_confirmation_intake_context: Mapping[str, Any],
    expected_world_fact_confirmation_intake_context_digest: str,
    world_fact_confirmation_policy_digest: str,
    world_fact_confirmation_responsibility_digest: str,
    world_fact_confirmation_request_id: str,
    world_fact_confirmation_bundle_digest: str,
) -> WORLDWorldFactConfirmationDispositionResult:
    blockers: list[str] = []
    source_verification = _map(source_world_postcondition_verification_receipt)
    source_mutation = _map(source_world_mutation_application_receipt)
    review = _map(world_fact_confirmation_review_certificate)
    context = _map(world_fact_confirmation_intake_context)

    for name, value in {
        "expected_source_world_postcondition_verification_receipt_digest": (
            expected_source_world_postcondition_verification_receipt_digest
        ),
        "expected_source_world_mutation_application_receipt_digest": (
            expected_source_world_mutation_application_receipt_digest
        ),
        "expected_world_fact_confirmation_review_certificate_digest": (
            expected_world_fact_confirmation_review_certificate_digest
        ),
        "expected_world_fact_confirmation_intake_context_digest": (
            expected_world_fact_confirmation_intake_context_digest
        ),
        "world_fact_confirmation_policy_digest": world_fact_confirmation_policy_digest,
        "world_fact_confirmation_responsibility_digest": (
            world_fact_confirmation_responsibility_digest
        ),
        "world_fact_confirmation_request_id": world_fact_confirmation_request_id,
        "world_fact_confirmation_bundle_digest": world_fact_confirmation_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    (
        mutation_digest,
        mutation_record,
        persisted,
        mutation_handoff,
        application_review,
        mutation_lineage,
        mutation_responsibility,
    ) = _verify_source_mutation(
        source_mutation,
        expected_source_world_mutation_application_receipt_digest,
        blockers,
    )

    (
        verification_digest,
        evidence,
        source_review,
        verification_record,
        verification_debt,
        fact_handoff,
        verification_lineage,
        verification_responsibility,
        verification_epoch,
    ) = _verify_source_verification(
        source_verification,
        expected_source_world_postcondition_verification_receipt_digest,
        source_mutation,
        blockers,
    )

    review_digest, review_duration_current = _verify_review(
        review,
        expected_world_fact_confirmation_review_certificate_digest,
        source_verification,
        source_mutation,
        blockers,
    )

    context_digest, checks = _verify_context(
        context,
        expected_world_fact_confirmation_intake_context_digest,
        source_verification,
        source_mutation,
        review,
        verification_epoch,
        blockers,
    )

    if not blockers:
        bundle = compute_world_fact_confirmation_bundle_digest(
            source_world_postcondition_verification_receipt_digest=verification_digest,
            expected_source_world_postcondition_verification_receipt_digest=(
                expected_source_world_postcondition_verification_receipt_digest
            ),
            source_world_mutation_application_receipt_digest=mutation_digest,
            expected_source_world_mutation_application_receipt_digest=(
                expected_source_world_mutation_application_receipt_digest
            ),
            source_world_postcondition_evidence_packet_digest=source_verification.get(
                SOURCE_EVIDENCE_DIGEST_FIELD
            ),
            source_world_postcondition_verification_review_certificate_digest=(
                source_verification.get(SOURCE_VERIFICATION_REVIEW_DIGEST_FIELD)
            ),
            source_world_postcondition_verification_record_digest=(
                source_verification.get("world_postcondition_verification_record_digest")
            ),
            source_world_postcondition_verification_debt_consumption_record_digest=(
                source_verification.get(
                    "world_postcondition_verification_debt_consumption_record_digest"
                )
            ),
            source_world_fact_confirmation_handoff_envelope_digest=(
                source_verification.get("world_fact_confirmation_handoff_envelope_digest")
            ),
            source_world_mutation_record_digest=source_mutation.get(
                "world_mutation_record_digest"
            ),
            source_persisted_world_candidate_envelope_digest=source_mutation.get(
                "persisted_world_candidate_envelope_digest"
            ),
            world_candidate_fact_digest=review.get("world_candidate_fact_digest"),
            world_candidate_relation_digest=review.get(
                "world_candidate_relation_digest"
            ),
            resulting_world_state_digest=review.get("resulting_world_state_digest"),
            resulting_world_revision=review.get("resulting_world_revision"),
            persistent_world_storage_target_digest=review.get(
                "persistent_world_storage_target_digest"
            ),
            expected_world_update_postcondition_digest=review.get(
                "expected_world_update_postcondition_digest"
            ),
            world_fact_confirmation_review_certificate_digest=review_digest,
            expected_world_fact_confirmation_review_certificate_digest=(
                expected_world_fact_confirmation_review_certificate_digest
            ),
            world_fact_confirmation_intake_context_digest=context_digest,
            expected_world_fact_confirmation_intake_context_digest=(
                expected_world_fact_confirmation_intake_context_digest
            ),
            requested_world_fact_confirmation_operation_digest=context.get(
                "requested_world_fact_confirmation_operation_digest"
            ),
            exact_world_fact_confirmation_cycle_digest=context.get(
                "exact_world_fact_confirmation_cycle_digest"
            ),
            world_fact_confirmation_policy_digest=world_fact_confirmation_policy_digest,
            world_fact_confirmation_responsibility_digest=(
                world_fact_confirmation_responsibility_digest
            ),
            world_fact_confirmation_request_id=world_fact_confirmation_request_id,
        )
        if bundle != world_fact_confirmation_bundle_digest:
            blockers.append("world_fact_confirmation_bundle_digest_mismatch")

    if blockers:
        return WORLDWorldFactConfirmationDispositionResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    disposition = _route(review, review_duration_current, checks)
    supported = disposition == DISPOSITION_SUPPORTED
    state_after = STATE_AFTER_SUPPORTED if supported else STATE_BEFORE

    confirmation_record = {
        "source_world_postcondition_verification_receipt_digest": verification_digest,
        "source_world_mutation_application_receipt_digest": mutation_digest,
        "source_world_postcondition_evidence_packet_digest": source_verification[
            SOURCE_EVIDENCE_DIGEST_FIELD
        ],
        "source_world_postcondition_verification_review_certificate_digest": (
            source_verification[SOURCE_VERIFICATION_REVIEW_DIGEST_FIELD]
        ),
        "source_world_postcondition_verification_record_digest": source_verification[
            "world_postcondition_verification_record_digest"
        ],
        "source_world_postcondition_verification_debt_consumption_record_digest": (
            source_verification[
                "world_postcondition_verification_debt_consumption_record_digest"
            ]
        ),
        "source_world_fact_confirmation_handoff_envelope_digest": source_verification[
            "world_fact_confirmation_handoff_envelope_digest"
        ],
        REVIEW_DIGEST_FIELD: review_digest,
        "world_mutation_record_digest": source_mutation["world_mutation_record_digest"],
        "persisted_world_candidate_envelope_digest": source_mutation[
            "persisted_world_candidate_envelope_digest"
        ],
        "world_mutation_transaction_digest": review[
            "world_mutation_transaction_digest"
        ],
        "world_candidate_fact_digest": review["world_candidate_fact_digest"],
        "world_candidate_relation_digest": review[
            "world_candidate_relation_digest"
        ],
        "resulting_world_state_digest": review["resulting_world_state_digest"],
        "resulting_world_revision": review["resulting_world_revision"],
        "persistent_world_storage_target_digest": review[
            "persistent_world_storage_target_digest"
        ],
        "expected_world_update_postcondition_digest": review[
            "expected_world_update_postcondition_digest"
        ],
        "fact_confirmation_reviewer_id": review["fact_confirmation_reviewer_id"],
        "world_fact_confirmation_intake_session_id": context[
            "world_fact_confirmation_intake_session_id"
        ],
        "world_fact_confirmation_intake_nonce_digest": context[
            "world_fact_confirmation_intake_nonce_digest"
        ],
        "world_fact_confirmation_intake_epoch": context[
            "world_fact_confirmation_intake_epoch"
        ],
        "world_fact_confirmation_disposition": disposition,
        "state_before": STATE_BEFORE,
        "state_after": state_after,
        "bounded_world_fact_status": (
            "confirmed_exact_bounded_proposition"
            if supported
            else "postcondition_verified_fact_confirmation_pending"
        ),
        "causal_attribution_state": "not_confirmed",
        "dukkha_realization_state": "not_confirmed",
    }
    confirmation_record_digest = canonical_digest(confirmation_record)

    debt = {
        "source_world_postcondition_verification_receipt_digest": verification_digest,
        REVIEW_DIGEST_FIELD: review_digest,
        "world_fact_confirmation_record_digest": confirmation_record_digest,
        "world_fact_confirmation_debt_consumed": supported,
        "source_verification_receipt_marked_fact_confirmed": supported,
        "double_world_fact_confirmation_performed": False,
    }
    debt_digest = canonical_digest(debt)

    fact_status_binding = None
    fact_status_binding_digest = ""
    causal_handoff = None
    causal_handoff_digest = ""
    if supported:
        fact_status_binding = {
            "source_world_postcondition_verification_receipt_digest": verification_digest,
            "world_fact_confirmation_record_digest": confirmation_record_digest,
            "world_fact_confirmation_debt_consumption_record_digest": debt_digest,
            "persisted_world_candidate_envelope_digest": source_mutation[
                "persisted_world_candidate_envelope_digest"
            ],
            "world_candidate_fact_digest": review["world_candidate_fact_digest"],
            "world_candidate_relation_digest": review[
                "world_candidate_relation_digest"
            ],
            "resulting_world_state_digest": review["resulting_world_state_digest"],
            "resulting_world_revision": review["resulting_world_revision"],
            "persistent_world_storage_target_digest": review[
                "persistent_world_storage_target_digest"
            ],
            "expected_world_update_postcondition_digest": review[
                "expected_world_update_postcondition_digest"
            ],
            "bounded_world_fact_status": "confirmed_exact_bounded_proposition",
            "generalization_beyond_bound": False,
            "causal_attribution_state": "not_confirmed",
            "dukkha_realization_state": "not_confirmed",
        }
        fact_status_binding_digest = canonical_digest(fact_status_binding)
        causal_handoff = {
            "source_world_postcondition_verification_receipt_digest": verification_digest,
            "world_fact_confirmation_record_digest": confirmation_record_digest,
            "world_fact_confirmation_debt_consumption_record_digest": debt_digest,
            "bounded_world_fact_status_binding_digest": fact_status_binding_digest,
            "world_candidate_fact_digest": review["world_candidate_fact_digest"],
            "world_candidate_relation_digest": review[
                "world_candidate_relation_digest"
            ],
            "resulting_world_state_digest": review["resulting_world_state_digest"],
            "resulting_world_revision": review["resulting_world_revision"],
            "causal_attribution_state": "pending_independent_verification",
            "causal_attribution_intake_admitted": True,
            "causal_attribution_receipt_required": True,
            "dukkha_realization_state": "not_confirmed",
        }
        causal_handoff_digest = canonical_digest(causal_handoff)

    resulting_lineage = sorted(
        set(mutation_lineage)
        | set(verification_lineage)
        | {
            mutation_digest,
            verification_digest,
            source_mutation["world_mutation_record_digest"],
            source_mutation["persisted_world_candidate_envelope_digest"],
            source_verification[SOURCE_EVIDENCE_DIGEST_FIELD],
            source_verification[SOURCE_VERIFICATION_REVIEW_DIGEST_FIELD],
            source_verification["world_postcondition_verification_record_digest"],
            source_verification[
                "world_postcondition_verification_debt_consumption_record_digest"
            ],
            source_verification["world_fact_confirmation_handoff_envelope_digest"],
            review_digest,
            context_digest,
            context["requested_world_fact_confirmation_operation_digest"],
            context["exact_world_fact_confirmation_cycle_digest"],
            confirmation_record_digest,
            debt_digest,
            world_fact_confirmation_bundle_digest,
        }
        | ({fact_status_binding_digest} if fact_status_binding_digest else set())
        | ({causal_handoff_digest} if causal_handoff_digest else set())
    )
    resulting_responsibility = sorted(
        set(mutation_responsibility)
        | set(verification_responsibility)
        | {
            review["fact_confirmation_reviewer_id"],
            world_fact_confirmation_responsibility_digest,
        }
    )

    (
        world_current,
        delay_current,
        session_fresh,
        review_fresh,
        nonce_fresh,
        source_fresh,
    ) = checks

    receipt = {
        "kernel": "WORLD Dukkha-Preserving WORLD Fact-Confirmation Disposition Intake Kernel",
        "kernel_version": "v0.1",
        "world_version": "v0.63",
        "status": "WORLD_DUKKHA_PRESERVING_WORLD_FACT_CONFIRMATION_DISPOSITION_ROUTED",
        "source_world_postcondition_verification_receipt_digest": verification_digest,
        "source_world_mutation_application_receipt_digest": mutation_digest,
        "source_world_postcondition_evidence_packet_digest": source_verification[
            SOURCE_EVIDENCE_DIGEST_FIELD
        ],
        "source_world_postcondition_verification_review_certificate_digest": (
            source_verification[SOURCE_VERIFICATION_REVIEW_DIGEST_FIELD]
        ),
        "source_world_postcondition_verification_intake_context_digest": (
            source_verification[SOURCE_VERIFICATION_CONTEXT_DIGEST_FIELD]
        ),
        "source_world_postcondition_verification_record_digest": source_verification[
            "world_postcondition_verification_record_digest"
        ],
        "source_world_postcondition_verification_debt_consumption_record_digest": (
            source_verification[
                "world_postcondition_verification_debt_consumption_record_digest"
            ]
        ),
        "source_world_fact_confirmation_handoff_envelope_digest": source_verification[
            "world_fact_confirmation_handoff_envelope_digest"
        ],
        "source_world_mutation_record_digest": source_mutation[
            "world_mutation_record_digest"
        ],
        "source_persisted_world_candidate_envelope_digest": source_mutation[
            "persisted_world_candidate_envelope_digest"
        ],
        "source_world_binding_digest": source_verification["source_world_binding_digest"],
        "source_world_model_state_digest": review["resulting_world_state_digest"],
        "source_world_model_revision": review["resulting_world_revision"],
        "source_persistent_world_storage_target_digest": review[
            "persistent_world_storage_target_digest"
        ],
        "world_candidate_fact_digest": review["world_candidate_fact_digest"],
        "world_candidate_relation_digest": review[
            "world_candidate_relation_digest"
        ],
        "world_mutation_transaction_digest": review[
            "world_mutation_transaction_digest"
        ],
        "expected_world_update_postcondition_digest": review[
            "expected_world_update_postcondition_digest"
        ],
        "uncertainty_digest": review["uncertainty_digest"],
        "calibration_digest": review["calibration_digest"],
        "provenance_chain_digests": review["provenance_chain_digests"],
        "protected_group_observed_impact_digest": review[
            "protected_group_observed_impact_digest"
        ],
        "future_subject_observed_impact_digest": review[
            "future_subject_observed_impact_digest"
        ],
        "realized_dukkha_observation_digest": review[
            "realized_dukkha_observation_digest"
        ],
        "world_fact_confirmation_review_certificate": review,
        REVIEW_DIGEST_FIELD: review_digest,
        CONTEXT_DIGEST_FIELD: context_digest,
        "world_fact_confirmation_policy_digest": world_fact_confirmation_policy_digest,
        "world_fact_confirmation_responsibility_digest": (
            world_fact_confirmation_responsibility_digest
        ),
        "world_fact_confirmation_request_id": world_fact_confirmation_request_id,
        "world_fact_confirmation_bundle_digest": world_fact_confirmation_bundle_digest,
        "world_fact_confirmation_disposition": disposition,
        "world_fact_confirmation_state_before": STATE_BEFORE,
        "world_fact_confirmation_state_after": state_after,
        "world_fact_confirmation_record": confirmation_record,
        "world_fact_confirmation_record_digest": confirmation_record_digest,
        "world_fact_confirmation_debt_consumption_record": debt,
        "world_fact_confirmation_debt_consumption_record_digest": debt_digest,
        "bounded_world_fact_status_binding": fact_status_binding,
        "bounded_world_fact_status_binding_digest": fact_status_binding_digest,
        "causal_attribution_verification_handoff_envelope": causal_handoff,
        "causal_attribution_verification_handoff_envelope_digest": causal_handoff_digest,
        "source_world_postcondition_verification_receipt_supplied": True,
        "source_world_postcondition_verification_receipt_fully_revalidated": True,
        "source_world_postcondition_verification_supported": True,
        "source_world_mutation_application_receipt_supplied": True,
        "source_world_mutation_application_receipt_fully_revalidated": True,
        "source_world_mutation_record_bound": True,
        "source_persisted_world_candidate_bound": True,
        "source_postcondition_evidence_packet_bound": True,
        "source_postcondition_verification_review_bound": True,
        "source_postcondition_verification_record_bound": True,
        "source_postcondition_verification_debt_consumption_bound": True,
        "source_world_fact_confirmation_handoff_bound": True,
        "candidate_fact_digest_bound": True,
        "candidate_relation_digest_bound": True,
        "resulting_world_state_digest_bound": True,
        "resulting_world_revision_bound": True,
        "persistent_world_storage_target_bound": True,
        "expected_world_postcondition_bound": True,
        "uncertainty_bound": True,
        "calibration_bound": True,
        "provenance_bound": True,
        "protected_group_impact_bound": True,
        "future_subject_impact_bound": True,
        "realized_dukkha_observation_bound": True,
        "exactly_one_world_fact_confirmation_disposition_receipt_issued": True,
        "exactly_one_bounded_world_fact_confirmation_receipt_issued": supported,
        "world_fact_confirmation_review_performed": True,
        "world_fact_confirmation_supported": supported,
        "world_fact_confirmation_debt_consumed": supported,
        "world_fact_confirmation_debt_replay_closed": supported,
        "world_fact_confirmation_double_consumed": False,
        "world_fact_confirmation_review_certificate_replay_closed": True,
        "world_fact_confirmation_intake_nonce_consumed": True,
        "world_fact_confirmation_intake_nonce_replay_closed": True,
        "source_world_postcondition_verification_receipt_replay_closed": supported,
        "world_fact_confirmation_intake_session_replay_fresh_before_intake": (
            session_fresh
        ),
        "world_fact_confirmation_review_replay_fresh_before_intake": review_fresh,
        "world_fact_confirmation_intake_nonce_replay_fresh_before_intake": nonce_fresh,
        "source_world_postcondition_verification_receipt_replay_fresh_before_confirmation": (
            source_fresh
        ),
        "world_conditions_current": world_current,
        "world_fact_confirmation_review_duration_current": review_duration_current,
        "world_fact_confirmation_intake_delay_current": delay_current,
        "world_fact_confirmation_debt_open": not supported,
        "bounded_world_fact_confirmed": supported,
        "world_fact_confirmed": supported,
        "world_fact_confirmation_scope_exactly_bounded": supported,
        "generalized_world_truth_confirmed": False,
        "causal_attribution_verification_intake_admitted": supported,
        "causal_attribution_verification_receipt_required": supported,
        "causal_attribution_confirmed": False,
        "dukkha_reduction_realized_confirmed": False,
        "persistent_world_model_state_unchanged_by_fact_confirmation": True,
        "persistent_world_state_changed_by_fact_confirmation": False,
        "world_model_revision_incremented_by_fact_confirmation": False,
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
        "selection_authority_granted_to_world": False,
        "plan_revision_authority_granted_to_world": False,
        "dukkha_minimization_authority_granted_to_world": False,
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
    return WORLDWorldFactConfirmationDispositionResult(STATUS_READY, [], receipt)
