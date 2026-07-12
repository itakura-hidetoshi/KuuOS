#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_world_dukkha_preserving_single_use_world_mutation_application_intake_v0_1 import (
    RECEIPT_DIGEST_FIELD as SOURCE_DIGEST_FIELD,
    canonical_digest,
)

STATUS_READY, STATUS_BLOCKED = "ready", "blocked"

RECEIPT_DIGEST_FIELD = (
    "verifyos_dukkha_preserving_world_postcondition_verification_intake_receipt_digest"
)
EVIDENCE_DIGEST_FIELD = "world_postcondition_evidence_packet_digest"
REVIEW_DIGEST_FIELD = "world_postcondition_verification_review_certificate_digest"
CONTEXT_DIGEST_FIELD = "world_postcondition_verification_intake_context_digest"

STATE_BEFORE = "world_candidate_commit_applied_world_fact_unconfirmed"
STATE_AFTER_SUPPORTED = (
    "world_candidate_commit_postcondition_verified_world_fact_confirmation_pending"
)

DISPOSITION_SUPPORTED = "world_postcondition_verification_supported"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_CONTEXT_REFRESH = "world_postcondition_verification_context_refresh_required"
DISPOSITION_REVIEW_REFRESH = "world_postcondition_verification_review_refresh_required"
DISPOSITION_ADDITIONAL_EVIDENCE = "additional_post_application_evidence_required"
DISPOSITION_CORRESPONDENCE_REPAIR = "world_mutation_correspondence_repair_required"
DISPOSITION_STATE_MISMATCH = "world_state_mismatch_detected"
DISPOSITION_REVISION_MISMATCH = "world_revision_mismatch_detected"
DISPOSITION_STORAGE_REPAIR = "world_storage_persistence_repair_required"
DISPOSITION_POSTCONDITION_REPAIR = "world_postcondition_repair_required"
DISPOSITION_CALIBRATION_REPAIR = "calibration_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "provenance_repair_required"
DISPOSITION_NONEXTERNALIZATION_REVIEW = "nonexternalization_review_required"
DISPOSITION_DUKKHA_REVIEW = "dukkha_realization_review_required"
DISPOSITION_TRUTH_PROMOTION_REJECTED = "truth_promotion_rejected"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"

EVIDENCE_FIELDS = {
    "source_world_mutation_application_receipt_digest",
    "world_mutation_application_record_digest",
    "world_candidate_commit_authorization_consumption_record_digest",
    "world_mutation_record_digest",
    "persisted_world_candidate_envelope_digest",
    "world_postcondition_verification_handoff_envelope_digest",
    "world_mutation_transaction_digest",
    "expected_world_update_postcondition_digest",
    "observed_world_state_digest",
    "observed_world_model_revision",
    "observed_persistent_world_storage_target_digest",
    "evidence_collector_id",
    "evidence_source_id",
    "collection_started_epoch",
    "collection_completed_epoch",
    "maximum_collection_duration",
    "raw_post_application_artifact_digest",
    "uncertainty_digest",
    "calibration_digest",
    "provenance_chain_digests",
    "tamper_evidence_digest",
    "protected_group_observed_impact_digest",
    "future_subject_observed_impact_digest",
    "realized_dukkha_observation_digest",
    "independent_post_application_evidence",
    "exactly_one_post_application_evidence_collection",
    "world_mutation_performed_by_evidence_collector",
    "world_fact_claimed",
    "causal_attribution_claimed",
    "realized_dukkha_reduction_claimed",
    EVIDENCE_DIGEST_FIELD,
}

REVIEW_FIELDS = {
    "source_world_mutation_application_receipt_digest",
    EVIDENCE_DIGEST_FIELD,
    "world_mutation_application_record_digest",
    "world_mutation_record_digest",
    "persisted_world_candidate_envelope_digest",
    "world_mutation_transaction_digest",
    "expected_world_update_postcondition_digest",
    "verifier_id",
    "verification_method_digest",
    "verification_evidence_digest",
    "verification_review_started_epoch",
    "verification_review_completed_epoch",
    "maximum_verification_review_duration",
    "source_mutation_applied",
    "mutation_transaction_correspondence_confirmed",
    "world_state_digest_matches",
    "world_revision_matches",
    "world_storage_persistence_confirmed",
    "world_postcondition_satisfied",
    "calibration_adequate",
    "provenance_continuity_preserved",
    "protected_group_nonexternalization_supported",
    "future_nonexternalization_supported",
    "realized_dukkha_assessment_adequate",
    "no_truth_overclaim",
    "no_causal_overclaim",
    "no_realized_dukkha_overclaim",
    "world_fact_claimed",
    "causal_attribution_claimed",
    "realized_dukkha_reduction_claimed",
    REVIEW_DIGEST_FIELD,
}

CONTEXT_FIELDS = {
    "source_world_mutation_application_receipt_digest",
    EVIDENCE_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD,
    "current_world_binding_digest",
    "current_world_model_state_digest",
    "current_world_model_revision",
    "current_world_lineage_digest",
    "source_world_mutation_applied_epoch",
    "world_postcondition_verification_intake_epoch",
    "maximum_world_postcondition_verification_intake_delay",
    "world_postcondition_verification_intake_session_id",
    "world_postcondition_verification_intake_nonce_digest",
    "prior_world_postcondition_verification_intake_session_ids",
    "prior_world_postcondition_evidence_packet_digests",
    "prior_world_postcondition_verification_review_certificate_digests",
    "prior_world_postcondition_verification_intake_nonce_digests",
    "prior_verified_world_mutation_application_receipt_digests",
    "requested_world_postcondition_verification_operation_digest",
    "exact_world_postcondition_verification_cycle_digest",
    CONTEXT_DIGEST_FIELD,
}


@dataclass
class VerifyOSWorldPostconditionVerificationResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def _map(value: Any) -> dict:
    return dict(value) if isinstance(value, Mapping) else {}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    item = dict(value)
    item.pop(field, None)
    return canonical_digest(item)


def compute_world_postcondition_evidence_packet_digest(
    value: Mapping[str, Any],
) -> str:
    return _digest_without(value, EVIDENCE_DIGEST_FIELD)


def compute_world_postcondition_verification_review_certificate_digest(
    value: Mapping[str, Any],
) -> str:
    return _digest_without(value, REVIEW_DIGEST_FIELD)


def compute_world_postcondition_verification_intake_context_digest(
    value: Mapping[str, Any],
) -> str:
    return _digest_without(value, CONTEXT_DIGEST_FIELD)


def compute_world_postcondition_verification_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def _strings(value: Any, allow_empty: bool = False) -> tuple[bool, list[str]]:
    ok = isinstance(value, list) and (allow_empty or bool(value)) and all(
        isinstance(item, str) and item for item in value
    )
    items = list(value) if isinstance(value, list) else []
    return ok and items == sorted(items) and len(items) == len(set(items)), items


def compute_requested_world_postcondition_verification_operation_digest(
    source: Mapping[str, Any],
    evidence: Mapping[str, Any],
    review: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_world_mutation_application_receipt_digest": source.get(
                SOURCE_DIGEST_FIELD
            ),
            "world_mutation_record_digest": source.get("world_mutation_record_digest"),
            "persisted_world_candidate_envelope_digest": source.get(
                "persisted_world_candidate_envelope_digest"
            ),
            EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
            "state_before": STATE_BEFORE,
            "supported_state_after": STATE_AFTER_SUPPORTED,
        }
    )


def compute_exact_world_postcondition_verification_cycle_digest(
    source: Mapping[str, Any],
    evidence: Mapping[str, Any],
    review: Mapping[str, Any],
    context: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_world_mutation_application_receipt_digest": source.get(
                SOURCE_DIGEST_FIELD
            ),
            EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
            "world_postcondition_verification_intake_session_id": context.get(
                "world_postcondition_verification_intake_session_id"
            ),
            "world_postcondition_verification_intake_nonce_digest": context.get(
                "world_postcondition_verification_intake_nonce_digest"
            ),
            "world_postcondition_verification_intake_epoch": context.get(
                "world_postcondition_verification_intake_epoch"
            ),
            "current_world_model_revision": context.get("current_world_model_revision"),
            "requested_world_postcondition_verification_operation_digest": context.get(
                "requested_world_postcondition_verification_operation_digest"
            ),
        }
    )


def _verify_source(
    source: dict, expected: str, blockers: list[str]
) -> tuple[str, dict, dict, dict, dict, dict, list[str], list[str]]:
    if not source:
        blockers.append("source_world_mutation_application_receipt_missing")
        return "", {}, {}, {}, {}, {}, [], []

    digest = source.get(SOURCE_DIGEST_FIELD, "")
    if not digest:
        blockers.append("source_world_mutation_application_receipt_digest_missing")
    elif digest != _digest_without(source, SOURCE_DIGEST_FIELD):
        blockers.append("source_world_mutation_application_receipt_digest_mismatch")
    if digest != expected:
        blockers.append("source_world_mutation_application_expected_binding_mismatch")

    expected_fields = {
        "kernel_version": "v0.1",
        "world_version": "v0.62",
        "status": (
            "WORLD_DUKKHA_PRESERVING_SINGLE_USE_WORLD_MUTATION_APPLICATION_ROUTED"
        ),
        "world_mutation_application_disposition": "world_mutation_application_ready",
        "world_mutation_application_state_after": STATE_BEFORE,
        "world_mutation_application_completed": True,
        "exactly_one_world_patch_applied": True,
        "world_mutation_transaction_atomic": True,
        "world_candidate_commit_completed": True,
        "single_use_world_candidate_commit_authorization_consumed": True,
        "persistent_world_model_state_changed": True,
        "world_model_revision_incremented_exactly_once": True,
        "world_postcondition_verification_intake_admitted": True,
        "world_postcondition_verification_receipt_required": True,
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
            blockers.append(f"source_boundary_{key}_mismatch")

    application = _map(source.get("world_mutation_application_record"))
    consumption = _map(
        source.get("world_candidate_commit_authorization_consumption_record")
    )
    mutation = _map(source.get("world_mutation_record"))
    persisted = _map(source.get("persisted_world_candidate_envelope"))
    handoff = _map(source.get("world_postcondition_verification_handoff_envelope"))
    source_review = _map(source.get("world_mutation_application_review_certificate"))

    for name, item, field in (
        (
            "world_mutation_application_record",
            application,
            "world_mutation_application_record_digest",
        ),
        (
            "world_candidate_commit_authorization_consumption_record",
            consumption,
            "world_candidate_commit_authorization_consumption_record_digest",
        ),
        ("world_mutation_record", mutation, "world_mutation_record_digest"),
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
            blockers.append(f"source_{name}_missing")
        elif source.get(field) != canonical_digest(item):
            blockers.append(f"source_{name}_digest_mismatch")

    for key, value in {
        "world_candidate_commit_state": "applied_persisted_world_fact_unconfirmed",
        "world_fact_state": "persisted_candidate_not_verified_fact",
        "causal_attribution_state": "not_confirmed",
        "dukkha_realization_state": "not_confirmed",
        "postcondition_verification_intake_admitted": True,
        "postcondition_verification_receipt_required": True,
        "compensation_route_ready": True,
    }.items():
        if persisted.get(key) != value:
            blockers.append(f"source_persisted_candidate_{key}_mismatch")

    for key, value in {
        "world_fact_state": "unconfirmed_pending_postcondition_verification",
        "causal_attribution_state": "not_confirmed",
        "dukkha_realization_state": "not_confirmed",
        "postcondition_verification_intake_admitted": True,
        "postcondition_verification_receipt_required": True,
        "compensation_route_ready": True,
    }.items():
        if handoff.get(key) != value:
            blockers.append(f"source_verification_handoff_{key}_mismatch")

    cross_bindings = {
        "world_mutation_application_record_digest": source.get(
            "world_mutation_application_record_digest"
        ),
        "authorization_consumption_record_digest": source.get(
            "world_candidate_commit_authorization_consumption_record_digest"
        ),
        "world_mutation_record_digest": source.get("world_mutation_record_digest"),
        "persisted_world_candidate_envelope_digest": source.get(
            "persisted_world_candidate_envelope_digest"
        ),
    }
    for key, value in cross_bindings.items():
        if handoff.get(key) != value:
            blockers.append(f"source_verification_handoff_{key}_mismatch")

    if handoff.get("world_mutation_transaction_digest") != mutation.get(
        "world_mutation_transaction_digest"
    ):
        blockers.append("source_mutation_transaction_binding_mismatch")
    if handoff.get("world_state_after_digest") != persisted.get(
        "world_state_after_digest"
    ):
        blockers.append("source_post_state_binding_mismatch")
    if handoff.get("world_model_revision_after") != persisted.get(
        "world_model_revision_after"
    ):
        blockers.append("source_post_revision_binding_mismatch")
    if handoff.get("world_update_postcondition_digest") != mutation.get(
        "world_update_postcondition_digest"
    ):
        blockers.append("source_postcondition_binding_mismatch")

    storage_target = source_review.get("persistent_world_storage_target_digest")
    if not isinstance(storage_target, str) or not storage_target:
        blockers.append("source_persistent_world_storage_target_invalid")

    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_resulting_responsibility_invalid")

    return (
        digest,
        application,
        consumption,
        mutation,
        persisted,
        handoff,
        lineage,
        responsibility,
    )


def _verify_evidence(
    evidence: dict,
    expected: str,
    source: dict,
    application: dict,
    consumption: dict,
    mutation: dict,
    persisted: dict,
    handoff: dict,
    blockers: list[str],
) -> tuple[str, bool, bool]:
    if not evidence:
        blockers.append("world_postcondition_evidence_packet_missing")
        return "", False, False
    if set(evidence) != EVIDENCE_FIELDS:
        blockers.append("world_postcondition_evidence_packet_schema_invalid")

    digest = evidence.get(EVIDENCE_DIGEST_FIELD, "")
    if not digest:
        blockers.append("world_postcondition_evidence_packet_digest_missing")
    elif digest != compute_world_postcondition_evidence_packet_digest(evidence):
        blockers.append("world_postcondition_evidence_packet_digest_mismatch")
    if digest != expected:
        blockers.append("world_postcondition_evidence_expected_binding_mismatch")

    bindings = {
        "source_world_mutation_application_receipt_digest": source.get(
            SOURCE_DIGEST_FIELD
        ),
        "world_mutation_application_record_digest": source.get(
            "world_mutation_application_record_digest"
        ),
        "world_candidate_commit_authorization_consumption_record_digest": source.get(
            "world_candidate_commit_authorization_consumption_record_digest"
        ),
        "world_mutation_record_digest": source.get("world_mutation_record_digest"),
        "persisted_world_candidate_envelope_digest": source.get(
            "persisted_world_candidate_envelope_digest"
        ),
        "world_postcondition_verification_handoff_envelope_digest": source.get(
            "world_postcondition_verification_handoff_envelope_digest"
        ),
        "world_mutation_transaction_digest": mutation.get(
            "world_mutation_transaction_digest"
        ),
        "expected_world_update_postcondition_digest": mutation.get(
            "world_update_postcondition_digest"
        ),
    }
    for key, value in bindings.items():
        if evidence.get(key) != value:
            blockers.append(f"world_postcondition_evidence_{key}_mismatch")

    for field in (
        "observed_world_state_digest",
        "observed_persistent_world_storage_target_digest",
        "evidence_collector_id",
        "evidence_source_id",
        "raw_post_application_artifact_digest",
        "uncertainty_digest",
        "calibration_digest",
        "tamper_evidence_digest",
        "protected_group_observed_impact_digest",
        "future_subject_observed_impact_digest",
        "realized_dukkha_observation_digest",
    ):
        if not isinstance(evidence.get(field), str) or not evidence.get(field):
            blockers.append(f"world_postcondition_evidence_{field}_invalid")

    for field in (
        "observed_world_model_revision",
        "collection_started_epoch",
        "collection_completed_epoch",
        "maximum_collection_duration",
    ):
        value = evidence.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"world_postcondition_evidence_{field}_invalid")

    for field in (
        "independent_post_application_evidence",
        "exactly_one_post_application_evidence_collection",
        "world_mutation_performed_by_evidence_collector",
        "world_fact_claimed",
        "causal_attribution_claimed",
        "realized_dukkha_reduction_claimed",
    ):
        if not isinstance(evidence.get(field), bool):
            blockers.append(f"world_postcondition_evidence_{field}_invalid")

    provenance_ok, _ = _strings(evidence.get("provenance_chain_digests"))
    if not provenance_ok:
        blockers.append("world_postcondition_evidence_provenance_chain_invalid")

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

    mutation_owner = source.get("world_mutation_application_review_certificate", {}).get(
        "mutation_owner_id"
    )
    independent = (
        evidence.get("independent_post_application_evidence") is True
        and evidence.get("exactly_one_post_application_evidence_collection") is True
        and evidence.get("world_mutation_performed_by_evidence_collector") is False
        and evidence.get("evidence_collector_id") != mutation_owner
        and evidence.get("evidence_source_id") != mutation_owner
    )
    return digest, duration_current, independent


def _verify_review(
    review: dict,
    expected: str,
    source: dict,
    evidence: dict,
    blockers: list[str],
) -> tuple[str, bool]:
    if not review:
        blockers.append("world_postcondition_verification_review_certificate_missing")
        return "", False
    if set(review) != REVIEW_FIELDS:
        blockers.append("world_postcondition_verification_review_schema_invalid")

    digest = review.get(REVIEW_DIGEST_FIELD, "")
    if not digest:
        blockers.append("world_postcondition_verification_review_digest_missing")
    elif digest != compute_world_postcondition_verification_review_certificate_digest(
        review
    ):
        blockers.append("world_postcondition_verification_review_digest_mismatch")
    if digest != expected:
        blockers.append("world_postcondition_verification_review_expected_binding_mismatch")

    bindings = {
        "source_world_mutation_application_receipt_digest": source.get(
            SOURCE_DIGEST_FIELD
        ),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        "world_mutation_application_record_digest": source.get(
            "world_mutation_application_record_digest"
        ),
        "world_mutation_record_digest": source.get("world_mutation_record_digest"),
        "persisted_world_candidate_envelope_digest": source.get(
            "persisted_world_candidate_envelope_digest"
        ),
        "world_mutation_transaction_digest": source.get(
            "world_postcondition_verification_handoff_envelope", {}
        ).get("world_mutation_transaction_digest"),
        "expected_world_update_postcondition_digest": source.get(
            "world_postcondition_verification_handoff_envelope", {}
        ).get("world_update_postcondition_digest"),
    }
    for key, value in bindings.items():
        if review.get(key) != value:
            blockers.append(f"world_postcondition_verification_review_{key}_mismatch")

    for field in (
        "verifier_id",
        "verification_method_digest",
        "verification_evidence_digest",
    ):
        if not isinstance(review.get(field), str) or not review.get(field):
            blockers.append(f"world_postcondition_verification_review_{field}_invalid")

    for field in (
        "verification_review_started_epoch",
        "verification_review_completed_epoch",
        "maximum_verification_review_duration",
    ):
        value = review.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"world_postcondition_verification_review_{field}_invalid")

    for field in REVIEW_FIELDS - {
        REVIEW_DIGEST_FIELD,
        "source_world_mutation_application_receipt_digest",
        EVIDENCE_DIGEST_FIELD,
        "world_mutation_application_record_digest",
        "world_mutation_record_digest",
        "persisted_world_candidate_envelope_digest",
        "world_mutation_transaction_digest",
        "expected_world_update_postcondition_digest",
        "verifier_id",
        "verification_method_digest",
        "verification_evidence_digest",
        "verification_review_started_epoch",
        "verification_review_completed_epoch",
        "maximum_verification_review_duration",
    }:
        if not isinstance(review.get(field), bool):
            blockers.append(f"world_postcondition_verification_review_{field}_invalid")

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
    source: dict,
    evidence: dict,
    review: dict,
    blockers: list[str],
) -> tuple[str, tuple[bool, ...]]:
    if not context:
        blockers.append("world_postcondition_verification_intake_context_missing")
        return "", (False,) * 7
    if set(context) != CONTEXT_FIELDS:
        blockers.append("world_postcondition_verification_intake_context_schema_invalid")

    digest = context.get(CONTEXT_DIGEST_FIELD, "")
    if not digest:
        blockers.append("world_postcondition_verification_intake_context_digest_missing")
    elif digest != compute_world_postcondition_verification_intake_context_digest(context):
        blockers.append("world_postcondition_verification_intake_context_digest_mismatch")
    if digest != expected:
        blockers.append("world_postcondition_verification_context_expected_binding_mismatch")

    for key, value in {
        "source_world_mutation_application_receipt_digest": source.get(
            SOURCE_DIGEST_FIELD
        ),
        EVIDENCE_DIGEST_FIELD: evidence.get(EVIDENCE_DIGEST_FIELD),
        REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
    }.items():
        if context.get(key) != value:
            blockers.append(f"world_postcondition_verification_context_{key}_mismatch")

    for field in (
        "current_world_binding_digest",
        "current_world_model_state_digest",
        "current_world_lineage_digest",
        "world_postcondition_verification_intake_session_id",
        "world_postcondition_verification_intake_nonce_digest",
        "requested_world_postcondition_verification_operation_digest",
        "exact_world_postcondition_verification_cycle_digest",
    ):
        if not isinstance(context.get(field), str) or not context.get(field):
            blockers.append(f"world_postcondition_verification_context_{field}_invalid")

    for field in (
        "current_world_model_revision",
        "source_world_mutation_applied_epoch",
        "world_postcondition_verification_intake_epoch",
        "maximum_world_postcondition_verification_intake_delay",
    ):
        value = context.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"world_postcondition_verification_context_{field}_invalid")

    persisted = source.get("persisted_world_candidate_envelope", {})
    expected_lineage = canonical_digest(source.get("resulting_lineage_digests", []))
    world_current = all(
        context.get(key) == value
        for key, value in {
            "current_world_binding_digest": source.get("source_world_binding_digest"),
            "current_world_model_state_digest": persisted.get("world_state_after_digest"),
            "current_world_model_revision": persisted.get("world_model_revision_after"),
            "current_world_lineage_digest": expected_lineage,
        }.items()
    )

    if context.get(
        "requested_world_postcondition_verification_operation_digest"
    ) != compute_requested_world_postcondition_verification_operation_digest(
        source, evidence, review
    ):
        blockers.append("world_postcondition_verification_context_operation_digest_mismatch")
    if context.get(
        "exact_world_postcondition_verification_cycle_digest"
    ) != compute_exact_world_postcondition_verification_cycle_digest(
        source, evidence, review, context
    ):
        blockers.append("world_postcondition_verification_context_cycle_digest_mismatch")

    applied = context.get("source_world_mutation_applied_epoch")
    epoch = context.get("world_postcondition_verification_intake_epoch")
    maximum = context.get("maximum_world_postcondition_verification_intake_delay")
    delay_current = (
        all(
            isinstance(value, int) and not isinstance(value, bool)
            for value in (applied, epoch, maximum)
        )
        and 1 <= maximum <= 64
        and 0 <= epoch - applied <= maximum
    )

    values = []
    for field in (
        "prior_world_postcondition_verification_intake_session_ids",
        "prior_world_postcondition_evidence_packet_digests",
        "prior_world_postcondition_verification_review_certificate_digests",
        "prior_world_postcondition_verification_intake_nonce_digests",
        "prior_verified_world_mutation_application_receipt_digests",
    ):
        ok, items = _strings(context.get(field), True)
        if not ok:
            blockers.append(f"world_postcondition_verification_context_{field}_invalid")
        values.append(items)
    sessions, evidences, reviews, nonces, sources = values

    return digest, (
        world_current,
        delay_current,
        context.get("world_postcondition_verification_intake_session_id") not in sessions,
        evidence.get(EVIDENCE_DIGEST_FIELD) not in evidences,
        review.get(REVIEW_DIGEST_FIELD) not in reviews,
        context.get("world_postcondition_verification_intake_nonce_digest") not in nonces,
        source.get(SOURCE_DIGEST_FIELD) not in sources,
    )


def _route(
    source: Mapping[str, Any],
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

    if not all(
        (
            session_fresh,
            evidence_fresh,
            review_fresh,
            nonce_fresh,
            source_fresh,
        )
    ):
        return DISPOSITION_REPLAY_REJECTED
    if not world_current:
        return DISPOSITION_WORLD_REFRESH
    if not delay_current or not evidence_duration_current:
        return DISPOSITION_CONTEXT_REFRESH
    if not review_duration_current:
        return DISPOSITION_REVIEW_REFRESH
    if (
        evidence.get("world_fact_claimed")
        or evidence.get("causal_attribution_claimed")
        or evidence.get("realized_dukkha_reduction_claimed")
        or review.get("world_fact_claimed")
        or review.get("causal_attribution_claimed")
        or review.get("realized_dukkha_reduction_claimed")
        or not review.get("no_truth_overclaim")
        or not review.get("no_causal_overclaim")
        or not review.get("no_realized_dukkha_overclaim")
    ):
        return DISPOSITION_TRUTH_PROMOTION_REJECTED
    if not evidence_independent:
        return DISPOSITION_ADDITIONAL_EVIDENCE
    if not review.get("source_mutation_applied") or not review.get(
        "mutation_transaction_correspondence_confirmed"
    ):
        return DISPOSITION_CORRESPONDENCE_REPAIR

    persisted = source.get("persisted_world_candidate_envelope", {})
    source_review = source.get("world_mutation_application_review_certificate", {})
    if (
        evidence.get("observed_world_state_digest")
        != persisted.get("world_state_after_digest")
        or not review.get("world_state_digest_matches")
    ):
        return DISPOSITION_STATE_MISMATCH
    if (
        evidence.get("observed_world_model_revision")
        != persisted.get("world_model_revision_after")
        or not review.get("world_revision_matches")
    ):
        return DISPOSITION_REVISION_MISMATCH
    if (
        evidence.get("observed_persistent_world_storage_target_digest")
        != source_review.get("persistent_world_storage_target_digest")
        or not review.get("world_storage_persistence_confirmed")
    ):
        return DISPOSITION_STORAGE_REPAIR
    if not review.get("world_postcondition_satisfied"):
        return DISPOSITION_POSTCONDITION_REPAIR
    if not review.get("calibration_adequate"):
        return DISPOSITION_CALIBRATION_REPAIR
    if not review.get("provenance_continuity_preserved"):
        return DISPOSITION_PROVENANCE_REPAIR
    if not review.get("protected_group_nonexternalization_supported") or not review.get(
        "future_nonexternalization_supported"
    ):
        return DISPOSITION_NONEXTERNALIZATION_REVIEW
    if not review.get("realized_dukkha_assessment_adequate"):
        return DISPOSITION_DUKKHA_REVIEW
    return DISPOSITION_SUPPORTED


def build_verifyos_dukkha_preserving_world_postcondition_verification_intake(
    *,
    source_world_mutation_application_receipt: Mapping[str, Any],
    expected_source_world_mutation_application_receipt_digest: str,
    world_postcondition_evidence_packet: Mapping[str, Any],
    expected_world_postcondition_evidence_packet_digest: str,
    world_postcondition_verification_review_certificate: Mapping[str, Any],
    expected_world_postcondition_verification_review_certificate_digest: str,
    world_postcondition_verification_intake_context: Mapping[str, Any],
    expected_world_postcondition_verification_intake_context_digest: str,
    world_postcondition_verification_policy_digest: str,
    world_postcondition_verification_responsibility_digest: str,
    world_postcondition_verification_request_id: str,
    world_postcondition_verification_bundle_digest: str,
) -> VerifyOSWorldPostconditionVerificationResult:
    blockers: list[str] = []
    source = _map(source_world_mutation_application_receipt)
    evidence = _map(world_postcondition_evidence_packet)
    review = _map(world_postcondition_verification_review_certificate)
    context = _map(world_postcondition_verification_intake_context)

    for name, value in {
        "expected_source_world_mutation_application_receipt_digest": (
            expected_source_world_mutation_application_receipt_digest
        ),
        "expected_world_postcondition_evidence_packet_digest": (
            expected_world_postcondition_evidence_packet_digest
        ),
        "expected_world_postcondition_verification_review_certificate_digest": (
            expected_world_postcondition_verification_review_certificate_digest
        ),
        "expected_world_postcondition_verification_intake_context_digest": (
            expected_world_postcondition_verification_intake_context_digest
        ),
        "world_postcondition_verification_policy_digest": (
            world_postcondition_verification_policy_digest
        ),
        "world_postcondition_verification_responsibility_digest": (
            world_postcondition_verification_responsibility_digest
        ),
        "world_postcondition_verification_request_id": (
            world_postcondition_verification_request_id
        ),
        "world_postcondition_verification_bundle_digest": (
            world_postcondition_verification_bundle_digest
        ),
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    (
        source_digest,
        application,
        consumption,
        mutation,
        persisted,
        handoff,
        lineage,
        responsibility,
    ) = _verify_source(
        source,
        expected_source_world_mutation_application_receipt_digest,
        blockers,
    )
    evidence_digest, evidence_duration_current, evidence_independent = _verify_evidence(
        evidence,
        expected_world_postcondition_evidence_packet_digest,
        source,
        application,
        consumption,
        mutation,
        persisted,
        handoff,
        blockers,
    )
    review_digest, review_duration_current = _verify_review(
        review,
        expected_world_postcondition_verification_review_certificate_digest,
        source,
        evidence,
        blockers,
    )
    context_digest, checks = _verify_context(
        context,
        expected_world_postcondition_verification_intake_context_digest,
        source,
        evidence,
        review,
        blockers,
    )

    if not blockers:
        bundle = compute_world_postcondition_verification_bundle_digest(
            source_world_mutation_application_receipt_digest=source_digest,
            expected_source_world_mutation_application_receipt_digest=(
                expected_source_world_mutation_application_receipt_digest
            ),
            world_mutation_application_record_digest=source.get(
                "world_mutation_application_record_digest"
            ),
            world_mutation_record_digest=source.get("world_mutation_record_digest"),
            persisted_world_candidate_envelope_digest=source.get(
                "persisted_world_candidate_envelope_digest"
            ),
            world_postcondition_evidence_packet_digest=evidence_digest,
            expected_world_postcondition_evidence_packet_digest=(
                expected_world_postcondition_evidence_packet_digest
            ),
            world_postcondition_verification_review_certificate_digest=review_digest,
            expected_world_postcondition_verification_review_certificate_digest=(
                expected_world_postcondition_verification_review_certificate_digest
            ),
            world_postcondition_verification_intake_context_digest=context_digest,
            expected_world_postcondition_verification_intake_context_digest=(
                expected_world_postcondition_verification_intake_context_digest
            ),
            requested_world_postcondition_verification_operation_digest=context.get(
                "requested_world_postcondition_verification_operation_digest"
            ),
            exact_world_postcondition_verification_cycle_digest=context.get(
                "exact_world_postcondition_verification_cycle_digest"
            ),
            world_postcondition_verification_policy_digest=(
                world_postcondition_verification_policy_digest
            ),
            world_postcondition_verification_responsibility_digest=(
                world_postcondition_verification_responsibility_digest
            ),
            world_postcondition_verification_request_id=(
                world_postcondition_verification_request_id
            ),
        )
        if bundle != world_postcondition_verification_bundle_digest:
            blockers.append("world_postcondition_verification_bundle_digest_mismatch")

    if blockers:
        return VerifyOSWorldPostconditionVerificationResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    disposition = _route(
        source,
        evidence,
        review,
        evidence_duration_current,
        evidence_independent,
        review_duration_current,
        checks,
    )
    supported = disposition == DISPOSITION_SUPPORTED
    state_after = STATE_AFTER_SUPPORTED if supported else STATE_BEFORE

    verification_record = {
        "source_world_mutation_application_receipt_digest": source_digest,
        "world_mutation_application_record_digest": source[
            "world_mutation_application_record_digest"
        ],
        "world_mutation_record_digest": source["world_mutation_record_digest"],
        "persisted_world_candidate_envelope_digest": source[
            "persisted_world_candidate_envelope_digest"
        ],
        EVIDENCE_DIGEST_FIELD: evidence_digest,
        REVIEW_DIGEST_FIELD: review_digest,
        "world_mutation_transaction_digest": handoff[
            "world_mutation_transaction_digest"
        ],
        "world_state_after_digest": handoff["world_state_after_digest"],
        "world_model_revision_after": handoff["world_model_revision_after"],
        "world_update_postcondition_digest": handoff[
            "world_update_postcondition_digest"
        ],
        "verifier_id": review["verifier_id"],
        "world_postcondition_verification_intake_session_id": context[
            "world_postcondition_verification_intake_session_id"
        ],
        "world_postcondition_verification_intake_nonce_digest": context[
            "world_postcondition_verification_intake_nonce_digest"
        ],
        "world_postcondition_verification_intake_epoch": context[
            "world_postcondition_verification_intake_epoch"
        ],
        "world_postcondition_verification_disposition": disposition,
        "state_before": STATE_BEFORE,
        "state_after": state_after,
        "verification_outcome": (
            "postcondition_verified_world_fact_confirmation_pending"
            if supported
            else "postcondition_verification_routed_without_fact_confirmation"
        ),
    }
    verification_record_digest = canonical_digest(verification_record)

    debt = {
        "source_world_mutation_application_receipt_digest": source_digest,
        EVIDENCE_DIGEST_FIELD: evidence_digest,
        REVIEW_DIGEST_FIELD: review_digest,
        "world_postcondition_verification_record_digest": verification_record_digest,
        "world_postcondition_verification_debt_consumed": supported,
        "source_world_mutation_marked_postcondition_verified": supported,
        "double_world_postcondition_verification_performed": False,
    }
    debt_digest = canonical_digest(debt)

    fact_handoff = None
    fact_handoff_digest = ""
    if supported:
        fact_handoff = {
            "source_world_mutation_application_receipt_digest": source_digest,
            "world_postcondition_verification_record_digest": verification_record_digest,
            "world_postcondition_verification_debt_consumption_record_digest": (
                debt_digest
            ),
            EVIDENCE_DIGEST_FIELD: evidence_digest,
            REVIEW_DIGEST_FIELD: review_digest,
            "world_mutation_record_digest": source["world_mutation_record_digest"],
            "persisted_world_candidate_envelope_digest": source[
                "persisted_world_candidate_envelope_digest"
            ],
            "world_candidate_fact_digest": persisted["world_candidate_fact_digest"],
            "world_candidate_relation_digest": persisted[
                "world_candidate_relation_digest"
            ],
            "world_mutation_transaction_digest": handoff[
                "world_mutation_transaction_digest"
            ],
            "world_update_postcondition_digest": handoff[
                "world_update_postcondition_digest"
            ],
            "world_state_after_digest": handoff["world_state_after_digest"],
            "world_model_revision_after": handoff["world_model_revision_after"],
            "world_fact_state": "postcondition_verified_fact_confirmation_pending",
            "causal_attribution_state": "not_confirmed",
            "dukkha_realization_state": "not_confirmed",
            "world_fact_confirmation_intake_admitted": True,
            "world_fact_confirmation_receipt_required": True,
            "compensation_route_ready": True,
        }
        fact_handoff_digest = canonical_digest(fact_handoff)

    resulting_lineage = sorted(
        set(lineage)
        | {
            source_digest,
            source["world_mutation_application_record_digest"],
            source["world_mutation_record_digest"],
            source["persisted_world_candidate_envelope_digest"],
            evidence_digest,
            review_digest,
            context_digest,
            context["requested_world_postcondition_verification_operation_digest"],
            context["exact_world_postcondition_verification_cycle_digest"],
            verification_record_digest,
            debt_digest,
            world_postcondition_verification_bundle_digest,
        }
        | ({fact_handoff_digest} if fact_handoff_digest else set())
    )
    resulting_responsibility = sorted(
        set(responsibility)
        | {
            review["verifier_id"],
            world_postcondition_verification_responsibility_digest,
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
            "VerifyOS Dukkha-Preserving WORLD Postcondition Verification Intake Kernel"
        ),
        "kernel_version": "v0.1",
        "verifyos_version": "v0.8",
        "status": "VERIFYOS_DUKKHA_PRESERVING_WORLD_POSTCONDITION_VERIFICATION_ROUTED",
        "source_world_mutation_application_receipt_digest": source_digest,
        "source_world_mutation_application_record_digest": source[
            "world_mutation_application_record_digest"
        ],
        "source_world_candidate_commit_authorization_consumption_record_digest": source[
            "world_candidate_commit_authorization_consumption_record_digest"
        ],
        "source_world_mutation_record_digest": source["world_mutation_record_digest"],
        "source_persisted_world_candidate_envelope_digest": source[
            "persisted_world_candidate_envelope_digest"
        ],
        "source_world_postcondition_verification_handoff_envelope_digest": source[
            "world_postcondition_verification_handoff_envelope_digest"
        ],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": persisted["world_state_after_digest"],
        "source_world_model_revision": persisted["world_model_revision_after"],
        "source_world_lineage_digest": canonical_digest(
            source["resulting_lineage_digests"]
        ),
        "selected_candidate_id": source["selected_candidate_id"],
        "invoked_frontier_candidate_id": source["invoked_frontier_candidate_id"],
        "invoked_frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "invoked_frontier_binding_digest": source[
            "invoked_frontier_binding_digest"
        ],
        "world_postcondition_evidence_packet": evidence,
        EVIDENCE_DIGEST_FIELD: evidence_digest,
        "world_postcondition_verification_review_certificate": review,
        REVIEW_DIGEST_FIELD: review_digest,
        CONTEXT_DIGEST_FIELD: context_digest,
        "world_postcondition_verification_policy_digest": (
            world_postcondition_verification_policy_digest
        ),
        "world_postcondition_verification_responsibility_digest": (
            world_postcondition_verification_responsibility_digest
        ),
        "world_postcondition_verification_request_id": (
            world_postcondition_verification_request_id
        ),
        "world_postcondition_verification_bundle_digest": (
            world_postcondition_verification_bundle_digest
        ),
        "world_postcondition_verification_disposition": disposition,
        "world_postcondition_verification_state_before": STATE_BEFORE,
        "world_postcondition_verification_state_after": state_after,
        "world_postcondition_verification_record": verification_record,
        "world_postcondition_verification_record_digest": verification_record_digest,
        "world_postcondition_verification_debt_consumption_record": debt,
        "world_postcondition_verification_debt_consumption_record_digest": debt_digest,
        "world_fact_confirmation_handoff_envelope": fact_handoff,
        "world_fact_confirmation_handoff_envelope_digest": fact_handoff_digest,
        "source_world_mutation_application_receipt_supplied": True,
        "source_world_mutation_application_receipt_fully_revalidated": True,
        "source_world_mutation_application_ready": True,
        "source_world_mutation_record_bound": True,
        "source_persisted_world_candidate_bound": True,
        "source_postcondition_verification_handoff_bound": True,
        "independent_post_application_evidence_bound": True,
        "world_postcondition_verification_review_certificate_bound": True,
        "exactly_one_world_postcondition_verification_receipt_issued": True,
        "world_postcondition_verification_performed": True,
        "world_postcondition_verification_supported": supported,
        "world_postcondition_verification_debt_consumed": supported,
        "world_postcondition_verification_debt_replay_closed": supported,
        "world_postcondition_verification_double_consumed": False,
        "world_postcondition_evidence_packet_replay_closed": True,
        "world_postcondition_verification_review_certificate_replay_closed": True,
        "world_postcondition_verification_intake_nonce_consumed": True,
        "world_postcondition_verification_intake_nonce_replay_closed": True,
        "source_world_mutation_application_receipt_replay_closed": supported,
        "world_postcondition_verification_intake_session_replay_fresh_before_intake": (
            session_fresh
        ),
        "world_postcondition_evidence_replay_fresh_before_intake": evidence_fresh,
        "world_postcondition_verification_review_replay_fresh_before_intake": (
            review_fresh
        ),
        "world_postcondition_verification_intake_nonce_replay_fresh_before_intake": (
            nonce_fresh
        ),
        "source_world_mutation_application_receipt_replay_fresh_before_verification": (
            source_fresh
        ),
        "world_conditions_current": world_current,
        "world_postcondition_evidence_collection_duration_current": (
            evidence_duration_current
        ),
        "world_postcondition_verification_review_duration_current": (
            review_duration_current
        ),
        "world_postcondition_verification_intake_delay_current": delay_current,
        "world_postcondition_verification_debt_open": not supported,
        "world_fact_confirmation_intake_admitted": supported,
        "world_fact_confirmation_receipt_required": supported,
        "world_fact_confirmation_completed": False,
        "persistent_world_model_state_unchanged_by_verifier": True,
        "persistent_world_state_changed_by_verifier": False,
        "world_fact_confirmed": False,
        "causal_attribution_confirmed": False,
        "dukkha_reduction_realized_confirmed": False,
        "world_mutation_reperformed": False,
        "tool_invocation_performed": False,
        "external_side_effect_performed": False,
        "compensation_route_ready": True,
        "compensation_performed": False,
        "automatic_truth_promotion": False,
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
    return VerifyOSWorldPostconditionVerificationResult(STATUS_READY, [], receipt)
