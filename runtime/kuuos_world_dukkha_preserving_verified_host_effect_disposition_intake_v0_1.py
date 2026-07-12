#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_verifyos_dukkha_preserving_observed_host_effect_verification_intake_v0_1 import (
    RECEIPT_DIGEST_FIELD as SOURCE_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD as SOURCE_REVIEW_DIGEST_FIELD,
    canonical_digest,
    compute_effect_verification_review_certificate_digest,
)

STATUS_READY, STATUS_BLOCKED = "ready", "blocked"
RECEIPT_DIGEST_FIELD = "world_dukkha_preserving_verified_host_effect_disposition_intake_receipt_digest"
REVIEW_DIGEST_FIELD = "world_disposition_review_certificate_digest"
STATE_BEFORE = "host_effect_verified_world_not_updated"
STATE_AFTER_READY = "verified_host_effect_world_candidate_prepared_not_committed"
DISPOSITION_READY = "world_candidate_admission_ready"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_CONTEXT_REFRESH = "world_disposition_context_refresh_required"
DISPOSITION_REVIEW_REFRESH = "world_disposition_review_refresh_required"
DISPOSITION_ADDITIONAL_OBSERVATION = "additional_observation_required"
DISPOSITION_VERIFICATION_REPAIR = "verification_repair_required"
DISPOSITION_CALIBRATION_REPAIR = "calibration_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "provenance_repair_required"
DISPOSITION_WORLD_PATCH_REPAIR = "world_patch_repair_required"
DISPOSITION_NONEXTERNALIZATION_REVIEW = "nonexternalization_review_required"
DISPOSITION_DUKKHA_REALIZATION_REVIEW = "dukkha_realization_review_required"
DISPOSITION_TRUTH_PROMOTION_REJECTED = "truth_promotion_rejected"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"

SOURCE_TRUE = (
    "source_observation_receipt_supplied",
    "source_observation_receipt_fully_revalidated",
    "effect_verification_review_certificate_bound",
    "verifier_identity_bound",
    "verification_method_bound",
    "verification_evidence_bound",
    "expected_effect_contract_bound",
    "observed_value_digest_bound",
    "uncertainty_digest_bound",
    "calibration_digest_bound",
    "provenance_chain_bound",
    "dukkha_impact_assessment_bound",
    "protected_group_impact_assessment_bound",
    "future_subject_impact_assessment_bound",
    "exactly_one_verification_receipt_issued",
    "verification_review_performed",
    "verification_completed",
    "effect_conformance_verified",
    "dukkha_preservation_verified",
    "protected_group_nonexternalization_verified",
    "future_nonexternalization_verified",
    "verification_debt_consumed",
    "verification_debt_replay_closed",
    "verification_review_certificate_replay_closed",
    "verification_intake_nonce_consumed",
    "verification_intake_nonce_replay_closed",
    "source_observation_receipt_replay_closed",
    "world_conditions_current",
    "verification_review_duration_current",
    "verification_intake_delay_current",
    "world_disposition_intake_admitted",
    "world_disposition_receipt_required",
    "persistent_world_model_state_unchanged",
    "compensation_route_ready",
    "effect_scope_preserved",
    "effect_ceiling_preserved",
    "checkpoint_guards_preserved",
    "stop_conditions_preserved",
    "evidence_lineage_preserved",
    "responsibility_lineage_preserved",
    "alternative_candidates_preserved",
    "dissent_preserved",
    "minority_preserved",
    "dukkha_reduction_support_preserved",
    "protected_group_nonexternalization_preserved",
    "future_nonexternalization_preserved",
    "revision_capacity_preserved",
    "persistent_loop_reduction_preserved",
    "single_scalar_utility_not_introduced",
    "selection_remains_decisionos_owned",
    "world_model_prediction_not_truth",
    "history_read_only",
    "qi_grants_no_authority",
    "future_only",
)
SOURCE_FALSE = (
    "verification_double_consumed",
    "verification_debt_open",
    "world_disposition_completed",
    "world_fact_confirmed",
    "causal_attribution_confirmed",
    "dukkha_reduction_realized_confirmed",
    "host_operation_reexecuted",
    "observation_reperformed",
    "tool_invocation_performed",
    "external_side_effect_performed",
    "persistent_host_state_changed_by_verification",
    "compensation_performed",
    "automatic_truth_promotion",
    "automatic_plan_completion",
    "automatic_rollback",
    "automatic_compensation",
    "selection_authority_granted_to_verifyos",
    "plan_revision_authority_granted_to_verifyos",
    "dukkha_minimization_authority_granted_to_verifyos",
    "general_execution_authority_granted",
    "execution_permission",
    "world_mutation_authority_granted",
    "active_now",
)

REVIEW_FIELDS = {
    "source_verification_receipt_digest",
    "verification_record_digest",
    "world_disposition_handoff_envelope_digest",
    SOURCE_REVIEW_DIGEST_FIELD,
    "frontier_materialization_candidate_id",
    "frontier_adapter_id",
    "frontier_binding_digest",
    "requested_effect_tags",
    "observed_value_digest",
    "uncertainty_digest",
    "calibration_digest",
    "provenance_chain_digests",
    "world_candidate_fact_digest",
    "world_candidate_relation_digest",
    "world_update_patch_digest",
    "world_update_precondition_digest",
    "world_update_postcondition_digest",
    "causal_model_claim_digest",
    "realized_dukkha_assessment_digest",
    "protected_group_realized_impact_digest",
    "future_subject_realized_impact_digest",
    "world_disposition_reviewer_id",
    "world_disposition_review_started_epoch",
    "world_disposition_review_completed_epoch",
    "maximum_world_disposition_review_duration",
    "source_verification_supported",
    "evidence_sufficient_for_world_candidate",
    "uncertainty_acceptable_for_world_candidate",
    "calibration_sufficient",
    "provenance_complete",
    "effect_identity_match",
    "world_patch_scope_conformant",
    "world_patch_ceiling_not_exceeded",
    "lineage_continuity_preserved",
    "responsibility_continuity_preserved",
    "dukkha_realization_assessment_sufficient",
    "no_causal_overclaim",
    "no_realized_dukkha_overclaim",
    "protected_group_nonexternalization_supported",
    "future_nonexternalization_supported",
    "compensation_route_ready",
    "world_fact_claimed",
    "causal_attribution_claimed",
    "realized_dukkha_reduction_claimed",
    REVIEW_DIGEST_FIELD,
}

CONTEXT_FIELDS = {
    "source_verification_receipt_digest",
    REVIEW_DIGEST_FIELD,
    "current_world_binding_digest",
    "current_world_model_state_digest",
    "current_world_model_revision",
    "current_world_lineage_digest",
    "source_verification_receipt_verified_epoch",
    "world_disposition_intake_epoch",
    "maximum_world_disposition_intake_delay",
    "world_disposition_intake_session_id",
    "world_disposition_intake_nonce_digest",
    "prior_world_disposition_intake_session_ids",
    "prior_world_disposition_review_certificate_digests",
    "prior_world_disposition_intake_nonce_digests",
    "prior_disposed_source_verification_receipt_digests",
    "requested_world_disposition_operation_digest",
    "exact_world_disposition_cycle_digest",
    "world_disposition_intake_context_digest",
}


@dataclass
class WORLDDukkhaPreservingVerifiedHostEffectDispositionResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def _map(value: Any) -> dict:
    return dict(value) if isinstance(value, Mapping) else {}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    item = dict(value)
    item.pop(field, None)
    return canonical_digest(item)


def compute_world_disposition_review_certificate_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, REVIEW_DIGEST_FIELD)


def compute_world_disposition_intake_context_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "world_disposition_intake_context_digest")


def compute_verified_host_effect_world_disposition_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def _strings(value: Any, allow_empty: bool = False) -> tuple[bool, list[str]]:
    ok = isinstance(value, list) and (allow_empty or bool(value)) and all(
        isinstance(item, str) and item for item in value
    )
    values = list(value) if isinstance(value, list) else []
    return ok and values == sorted(values) and len(values) == len(set(values)), values


def _exact(actual: Mapping[str, Any], expected: Mapping[str, Any], prefix: str, blockers: list[str]) -> None:
    blockers.extend(
        f"{prefix}_{key}_mismatch" for key, value in expected.items() if actual.get(key) != value
    )


def compute_requested_world_disposition_operation_digest(
    source: Mapping[str, Any], review: Mapping[str, Any]
) -> str:
    return canonical_digest(
        {
            "source_verification_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
            "verification_record_digest": source.get("verification_record_digest"),
            "world_disposition_handoff_envelope_digest": source.get(
                "world_disposition_handoff_envelope_digest"
            ),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
            "frontier_materialization_candidate_id": source.get("invoked_frontier_candidate_id"),
            "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
            "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
            "state_before": STATE_BEFORE,
            "ready_state_after": STATE_AFTER_READY,
        }
    )


def compute_exact_world_disposition_cycle_digest(
    source: Mapping[str, Any], review: Mapping[str, Any], context: Mapping[str, Any]
) -> str:
    return canonical_digest(
        {
            "source_verification_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
            "world_disposition_intake_session_id": context.get(
                "world_disposition_intake_session_id"
            ),
            "world_disposition_intake_nonce_digest": context.get(
                "world_disposition_intake_nonce_digest"
            ),
            "world_disposition_intake_epoch": context.get("world_disposition_intake_epoch"),
            "current_world_model_revision": context.get("current_world_model_revision"),
            "requested_world_disposition_operation_digest": context.get(
                "requested_world_disposition_operation_digest"
            ),
        }
    )


def _verify_source(source: dict, expected: str, blockers: list[str]):
    if not source:
        blockers.append("source_verification_receipt_missing")
        return "", {}, [], []
    _exact(
        source,
        {
            "kernel": "VerifyOS Dukkha-Preserving Observed Host-Effect Verification Intake Kernel",
            "kernel_version": "v0.1",
            "verifyos_version": "v0.7",
            "status": "VERIFYOS_DUKKHA_PRESERVING_OBSERVED_HOST_EFFECT_VERIFICATION_ROUTED",
            "verification_disposition": "effect_verification_supported",
            "verification_state_before": "host_effect_observed_unverified",
            "verification_state_after": STATE_BEFORE,
        },
        "source",
        blockers,
    )
    digest = source.get(SOURCE_DIGEST_FIELD, "")
    if not digest:
        blockers.append("source_verification_receipt_digest_missing")
    elif digest != _digest_without(source, SOURCE_DIGEST_FIELD):
        blockers.append("source_verification_receipt_digest_mismatch")
    if digest != expected:
        blockers.append("source_verification_expected_binding_mismatch")
    for field in SOURCE_TRUE:
        if source.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in SOURCE_FALSE:
        if source.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")

    source_review = _map(source.get("effect_verification_review_certificate"))
    record = _map(source.get("verification_record"))
    debt = _map(source.get("verification_debt_consumption_record"))
    handoff = _map(source.get("world_disposition_handoff_envelope"))
    if not source_review:
        blockers.append("source_effect_verification_review_invalid")
    elif source.get(SOURCE_REVIEW_DIGEST_FIELD) != compute_effect_verification_review_certificate_digest(
        source_review
    ):
        blockers.append("source_effect_verification_review_digest_mismatch")
    for name, item, field in (
        ("verification_record", record, "verification_record_digest"),
        ("verification_debt_consumption_record", debt, "verification_debt_consumption_record_digest"),
        ("world_disposition_handoff_envelope", handoff, "world_disposition_handoff_envelope_digest"),
    ):
        if not item:
            blockers.append(f"source_{name}_invalid")
        elif source.get(field) != canonical_digest(item):
            blockers.append(f"source_{name}_digest_mismatch")

    _exact(
        record,
        {
            "source_observation_receipt_digest": source.get("source_observation_receipt_digest"),
            SOURCE_REVIEW_DIGEST_FIELD: source.get(SOURCE_REVIEW_DIGEST_FIELD),
            "frontier_materialization_candidate_id": source.get("invoked_frontier_candidate_id"),
            "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
            "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
            "verification_disposition": "effect_verification_supported",
            "state_before": "host_effect_observed_unverified",
            "state_after": STATE_BEFORE,
            "verification_outcome": "bounded_host_effect_verification_supported_world_not_updated",
        },
        "source_verification_record",
        blockers,
    )
    if debt.get("verification_debt_consumed") is not True:
        blockers.append("source_verification_debt_not_consumed")
    if debt.get("source_observation_receipt_marked_verified") is not True:
        blockers.append("source_observation_receipt_not_marked_verified")
    if debt.get("double_verification_performed") is not False:
        blockers.append("source_double_verification_promoted")

    _exact(
        handoff,
        {
            "source_observation_receipt_digest": source.get("source_observation_receipt_digest"),
            "verification_record_digest": source.get("verification_record_digest"),
            SOURCE_REVIEW_DIGEST_FIELD: source.get(SOURCE_REVIEW_DIGEST_FIELD),
            "frontier_materialization_candidate_id": source.get("invoked_frontier_candidate_id"),
            "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
            "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
            "verification_disposition": "effect_verification_supported",
            "effect_conformance_verified": True,
            "dukkha_preservation_verified": True,
            "protected_group_nonexternalization_verified": True,
            "future_nonexternalization_verified": True,
            "world_fact_state": "not_promoted",
            "causal_attribution_state": "not_confirmed",
            "world_disposition_intake_admitted": True,
            "world_disposition_receipt_required": True,
            "compensation_route_ready": True,
        },
        "source_world_disposition_handoff",
        blockers,
    )
    requested_ok, requested = _strings(handoff.get("requested_effect_tags"), True)
    provenance_ok, provenance = _strings(handoff.get("provenance_chain_digests"))
    if not requested_ok:
        blockers.append("source_requested_effect_tags_invalid")
    if not provenance_ok:
        blockers.append("source_world_disposition_provenance_invalid")
    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_resulting_responsibility_invalid")
    return digest, handoff, lineage, responsibility


def _verify_review(
    review: dict,
    expected: str,
    source: dict,
    handoff: dict,
    blockers: list[str],
):
    if not review:
        blockers.append("world_disposition_review_certificate_missing")
        return "", False
    if set(review) != REVIEW_FIELDS:
        blockers.append("world_disposition_review_certificate_schema_invalid")
    digest = review.get(REVIEW_DIGEST_FIELD, "")
    if not digest:
        blockers.append("world_disposition_review_certificate_digest_missing")
    elif digest != compute_world_disposition_review_certificate_digest(review):
        blockers.append("world_disposition_review_certificate_digest_mismatch")
    if digest != expected:
        blockers.append("world_disposition_review_expected_binding_mismatch")
    _exact(
        review,
        {
            "source_verification_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
            "verification_record_digest": source.get("verification_record_digest"),
            "world_disposition_handoff_envelope_digest": source.get(
                "world_disposition_handoff_envelope_digest"
            ),
            SOURCE_REVIEW_DIGEST_FIELD: source.get(SOURCE_REVIEW_DIGEST_FIELD),
            "frontier_materialization_candidate_id": source.get("invoked_frontier_candidate_id"),
            "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
            "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
            "requested_effect_tags": handoff.get("requested_effect_tags"),
            "observed_value_digest": handoff.get("observed_value_digest"),
            "uncertainty_digest": handoff.get("uncertainty_digest"),
            "calibration_digest": handoff.get("calibration_digest"),
            "provenance_chain_digests": handoff.get("provenance_chain_digests"),
        },
        "world_disposition_review",
        blockers,
    )
    for field in (
        "world_candidate_fact_digest",
        "world_candidate_relation_digest",
        "world_update_patch_digest",
        "world_update_precondition_digest",
        "world_update_postcondition_digest",
        "causal_model_claim_digest",
        "realized_dukkha_assessment_digest",
        "protected_group_realized_impact_digest",
        "future_subject_realized_impact_digest",
        "world_disposition_reviewer_id",
    ):
        if not isinstance(review.get(field), str) or not review.get(field):
            blockers.append(f"world_disposition_review_{field}_invalid")
    bool_fields = (
        "source_verification_supported",
        "evidence_sufficient_for_world_candidate",
        "uncertainty_acceptable_for_world_candidate",
        "calibration_sufficient",
        "provenance_complete",
        "effect_identity_match",
        "world_patch_scope_conformant",
        "world_patch_ceiling_not_exceeded",
        "lineage_continuity_preserved",
        "responsibility_continuity_preserved",
        "dukkha_realization_assessment_sufficient",
        "no_causal_overclaim",
        "no_realized_dukkha_overclaim",
        "protected_group_nonexternalization_supported",
        "future_nonexternalization_supported",
        "compensation_route_ready",
        "world_fact_claimed",
        "causal_attribution_claimed",
        "realized_dukkha_reduction_claimed",
    )
    for field in bool_fields:
        if not isinstance(review.get(field), bool):
            blockers.append(f"world_disposition_review_{field}_invalid")
    start = review.get("world_disposition_review_started_epoch")
    end = review.get("world_disposition_review_completed_epoch")
    maximum = review.get("maximum_world_disposition_review_duration")
    types_ok = all(
        isinstance(value, int) and not isinstance(value, bool) and value >= 0
        for value in (start, end, maximum)
    )
    if not types_ok:
        blockers.append("world_disposition_review_epoch_schema_invalid")
    return digest, types_ok and 1 <= maximum <= 64 and 0 <= end - start <= maximum


def _verify_context(
    context: dict,
    expected: str,
    source: dict,
    review: dict,
    blockers: list[str],
):
    if not context:
        blockers.append("world_disposition_intake_context_missing")
        return "", (False,) * 6
    if set(context) != CONTEXT_FIELDS:
        blockers.append("world_disposition_intake_context_schema_invalid")
    digest = context.get("world_disposition_intake_context_digest", "")
    if not digest:
        blockers.append("world_disposition_intake_context_digest_missing")
    elif digest != compute_world_disposition_intake_context_digest(context):
        blockers.append("world_disposition_intake_context_digest_mismatch")
    if digest != expected:
        blockers.append("world_disposition_intake_context_expected_binding_mismatch")
    _exact(
        context,
        {
            "source_verification_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        },
        "world_disposition_intake_context",
        blockers,
    )
    for field in (
        "current_world_binding_digest",
        "current_world_model_state_digest",
        "current_world_lineage_digest",
        "world_disposition_intake_session_id",
        "world_disposition_intake_nonce_digest",
        "requested_world_disposition_operation_digest",
        "exact_world_disposition_cycle_digest",
    ):
        if not isinstance(context.get(field), str) or not context.get(field):
            blockers.append(f"world_disposition_intake_context_{field}_invalid")
    for field in (
        "current_world_model_revision",
        "source_verification_receipt_verified_epoch",
        "world_disposition_intake_epoch",
        "maximum_world_disposition_intake_delay",
    ):
        value = context.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"world_disposition_intake_context_{field}_invalid")
    world_current = all(
        context.get(key) == value
        for key, value in {
            "current_world_binding_digest": source.get("source_world_binding_digest"),
            "current_world_model_state_digest": source.get("source_world_model_state_digest"),
            "current_world_model_revision": source.get("source_world_model_revision"),
            "current_world_lineage_digest": source.get("source_world_lineage_digest"),
        }.items()
    )
    if context.get(
        "requested_world_disposition_operation_digest"
    ) != compute_requested_world_disposition_operation_digest(source, review):
        blockers.append("world_disposition_intake_context_operation_digest_mismatch")
    if context.get("exact_world_disposition_cycle_digest") != compute_exact_world_disposition_cycle_digest(
        source, review, context
    ):
        blockers.append("world_disposition_intake_context_cycle_digest_mismatch")
    verified = context.get("source_verification_receipt_verified_epoch")
    epoch = context.get("world_disposition_intake_epoch")
    maximum = context.get("maximum_world_disposition_intake_delay")
    delay_current = all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in (verified, epoch, maximum)
    ) and 1 <= maximum <= 64 and 0 <= epoch - verified <= maximum
    values = []
    for field in (
        "prior_world_disposition_intake_session_ids",
        "prior_world_disposition_review_certificate_digests",
        "prior_world_disposition_intake_nonce_digests",
        "prior_disposed_source_verification_receipt_digests",
    ):
        ok, items = _strings(context.get(field), True)
        if not ok:
            blockers.append(f"world_disposition_intake_context_{field}_invalid")
        values.append(items)
    sessions, reviews, nonces, sources = values
    return digest, (
        world_current,
        delay_current,
        context.get("world_disposition_intake_session_id") not in sessions,
        review.get(REVIEW_DIGEST_FIELD) not in reviews,
        context.get("world_disposition_intake_nonce_digest") not in nonces,
        source.get(SOURCE_DIGEST_FIELD) not in sources,
    )


def _route(review: Mapping[str, Any], duration: bool, checks: tuple[bool, ...]) -> str:
    world, delay, session, review_fresh, nonce, source = checks
    if not all((session, review_fresh, nonce, source)):
        return DISPOSITION_REPLAY_REJECTED
    if not world:
        return DISPOSITION_WORLD_REFRESH
    if not delay:
        return DISPOSITION_CONTEXT_REFRESH
    if not duration:
        return DISPOSITION_REVIEW_REFRESH
    if any(
        review.get(field)
        for field in (
            "world_fact_claimed",
            "causal_attribution_claimed",
            "realized_dukkha_reduction_claimed",
        )
    ) or not review.get("no_causal_overclaim") or not review.get("no_realized_dukkha_overclaim"):
        return DISPOSITION_TRUTH_PROMOTION_REJECTED
    if not review.get("source_verification_supported") or not review.get("effect_identity_match"):
        return DISPOSITION_VERIFICATION_REPAIR
    if not review.get("evidence_sufficient_for_world_candidate") or not review.get(
        "uncertainty_acceptable_for_world_candidate"
    ):
        return DISPOSITION_ADDITIONAL_OBSERVATION
    if not review.get("calibration_sufficient"):
        return DISPOSITION_CALIBRATION_REPAIR
    if not all(
        review.get(field)
        for field in (
            "provenance_complete",
            "lineage_continuity_preserved",
            "responsibility_continuity_preserved",
        )
    ):
        return DISPOSITION_PROVENANCE_REPAIR
    if not review.get("world_patch_scope_conformant") or not review.get(
        "world_patch_ceiling_not_exceeded"
    ):
        return DISPOSITION_WORLD_PATCH_REPAIR
    if not review.get("protected_group_nonexternalization_supported") or not review.get(
        "future_nonexternalization_supported"
    ):
        return DISPOSITION_NONEXTERNALIZATION_REVIEW
    if not review.get("dukkha_realization_assessment_sufficient"):
        return DISPOSITION_DUKKHA_REALIZATION_REVIEW
    return DISPOSITION_READY


def build_world_dukkha_preserving_verified_host_effect_disposition_intake(
    *,
    source_verification_receipt: Mapping[str, Any],
    expected_source_verification_receipt_digest: str,
    world_disposition_review_certificate: Mapping[str, Any],
    expected_world_disposition_review_certificate_digest: str,
    world_disposition_intake_context: Mapping[str, Any],
    expected_world_disposition_intake_context_digest: str,
    world_disposition_intake_policy_digest: str,
    world_disposition_responsibility_digest: str,
    world_disposition_request_id: str,
    verified_host_effect_world_disposition_bundle_digest: str,
) -> WORLDDukkhaPreservingVerifiedHostEffectDispositionResult:
    blockers: list[str] = []
    source = _map(source_verification_receipt)
    review = _map(world_disposition_review_certificate)
    context = _map(world_disposition_intake_context)
    for name, value in {
        "expected_source_verification_receipt_digest": expected_source_verification_receipt_digest,
        "expected_world_disposition_review_certificate_digest": expected_world_disposition_review_certificate_digest,
        "expected_world_disposition_intake_context_digest": expected_world_disposition_intake_context_digest,
        "world_disposition_intake_policy_digest": world_disposition_intake_policy_digest,
        "world_disposition_responsibility_digest": world_disposition_responsibility_digest,
        "world_disposition_request_id": world_disposition_request_id,
        "verified_host_effect_world_disposition_bundle_digest": verified_host_effect_world_disposition_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    source_digest, handoff, lineage, responsibility = _verify_source(
        source, expected_source_verification_receipt_digest, blockers
    )
    review_digest, duration = _verify_review(
        review,
        expected_world_disposition_review_certificate_digest,
        source,
        handoff,
        blockers,
    )
    context_digest, checks = _verify_context(
        context,
        expected_world_disposition_intake_context_digest,
        source,
        review,
        blockers,
    )
    if not blockers:
        bundle = compute_verified_host_effect_world_disposition_bundle_digest(
            source_verification_receipt_digest=source_digest,
            expected_source_verification_receipt_digest=expected_source_verification_receipt_digest,
            verification_record_digest=source.get("verification_record_digest"),
            world_disposition_handoff_envelope_digest=source.get(
                "world_disposition_handoff_envelope_digest"
            ),
            world_disposition_review_certificate_digest=review_digest,
            expected_world_disposition_review_certificate_digest=expected_world_disposition_review_certificate_digest,
            world_disposition_intake_context_digest=context_digest,
            expected_world_disposition_intake_context_digest=expected_world_disposition_intake_context_digest,
            requested_world_disposition_operation_digest=context.get(
                "requested_world_disposition_operation_digest"
            ),
            exact_world_disposition_cycle_digest=context.get(
                "exact_world_disposition_cycle_digest"
            ),
            world_disposition_intake_policy_digest=world_disposition_intake_policy_digest,
            world_disposition_responsibility_digest=world_disposition_responsibility_digest,
            world_disposition_request_id=world_disposition_request_id,
        )
        if bundle != verified_host_effect_world_disposition_bundle_digest:
            blockers.append("verified_host_effect_world_disposition_bundle_digest_mismatch")
    if blockers:
        return WORLDDukkhaPreservingVerifiedHostEffectDispositionResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    disposition = _route(review, duration, checks)
    ready = disposition == DISPOSITION_READY
    state_after = STATE_AFTER_READY if ready else STATE_BEFORE
    record = {
        "source_verification_receipt_digest": source_digest,
        "verification_record_digest": source["verification_record_digest"],
        "world_disposition_handoff_envelope_digest": source[
            "world_disposition_handoff_envelope_digest"
        ],
        REVIEW_DIGEST_FIELD: review_digest,
        "frontier_materialization_candidate_id": source["invoked_frontier_candidate_id"],
        "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "world_disposition_reviewer_id": review["world_disposition_reviewer_id"],
        "world_disposition_intake_session_id": context[
            "world_disposition_intake_session_id"
        ],
        "world_disposition_intake_nonce_digest": context[
            "world_disposition_intake_nonce_digest"
        ],
        "world_disposition_intake_epoch": context["world_disposition_intake_epoch"],
        "world_disposition": disposition,
        "state_before": STATE_BEFORE,
        "state_after": state_after,
        "world_disposition_outcome": (
            "verified_host_effect_world_candidate_prepared_not_committed"
            if ready
            else "verified_host_effect_world_disposition_routed_without_candidate_commit"
        ),
    }
    record_digest = canonical_digest(record)
    debt = {
        "source_verification_receipt_digest": source_digest,
        REVIEW_DIGEST_FIELD: review_digest,
        "world_disposition_record_digest": record_digest,
        "world_disposition_debt_consumed": ready,
        "source_verification_receipt_marked_disposed": ready,
        "double_world_disposition_performed": False,
    }
    debt_digest = canonical_digest(debt)
    candidate = None
    candidate_digest = ""
    if ready:
        candidate = {
            "source_verification_receipt_digest": source_digest,
            "verification_record_digest": source["verification_record_digest"],
            "world_disposition_record_digest": record_digest,
            REVIEW_DIGEST_FIELD: review_digest,
            "frontier_materialization_candidate_id": source["invoked_frontier_candidate_id"],
            "frontier_adapter_id": source["invoked_frontier_adapter_id"],
            "frontier_binding_digest": source["invoked_frontier_binding_digest"],
            "requested_effect_tags": list(handoff["requested_effect_tags"]),
            "observed_value_digest": handoff["observed_value_digest"],
            "uncertainty_digest": handoff["uncertainty_digest"],
            "calibration_digest": handoff["calibration_digest"],
            "provenance_chain_digests": list(handoff["provenance_chain_digests"]),
            "world_candidate_fact_digest": review["world_candidate_fact_digest"],
            "world_candidate_relation_digest": review["world_candidate_relation_digest"],
            "world_update_patch_digest": review["world_update_patch_digest"],
            "world_update_precondition_digest": review["world_update_precondition_digest"],
            "world_update_postcondition_digest": review["world_update_postcondition_digest"],
            "causal_model_claim_digest": review["causal_model_claim_digest"],
            "realized_dukkha_assessment_digest": review[
                "realized_dukkha_assessment_digest"
            ],
            "world_candidate_state": "prepared_not_committed",
            "world_fact_state": "candidate_only_not_fact",
            "causal_attribution_state": "not_confirmed",
            "dukkha_realization_state": "not_confirmed",
            "world_commit_authorization_intake_admitted": True,
            "world_commit_authorization_receipt_required": True,
            "compensation_route_ready": True,
        }
        candidate_digest = canonical_digest(candidate)

    resulting_lineage = sorted(
        set(lineage)
        | {
            source_digest,
            source["verification_record_digest"],
            source["world_disposition_handoff_envelope_digest"],
            review_digest,
            context_digest,
            context["requested_world_disposition_operation_digest"],
            context["exact_world_disposition_cycle_digest"],
            record_digest,
            debt_digest,
            verified_host_effect_world_disposition_bundle_digest,
        }
        | ({candidate_digest} if candidate_digest else set())
    )
    resulting_responsibility = sorted(
        set(responsibility)
        | {
            review["world_disposition_reviewer_id"],
            world_disposition_responsibility_digest,
        }
    )
    world_current, delay_current, session_fresh, review_fresh, nonce_fresh, source_fresh = checks
    receipt = {
        "kernel": "WORLD Dukkha-Preserving Verified Host-Effect Disposition Intake Kernel",
        "kernel_version": "v0.1",
        "world_version": "v0.60",
        "status": "WORLD_DUKKHA_PRESERVING_VERIFIED_HOST_EFFECT_DISPOSITION_ROUTED",
        "source_verification_receipt_digest": source_digest,
        "source_observation_receipt_digest": source["source_observation_receipt_digest"],
        "source_host_effect_receipt_digest": source["source_host_effect_receipt_digest"],
        "source_verification_record_digest": source["verification_record_digest"],
        "source_world_disposition_handoff_envelope_digest": source[
            "world_disposition_handoff_envelope_digest"
        ],
        "source_effect_verification_review_certificate_digest": source[
            SOURCE_REVIEW_DIGEST_FIELD
        ],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source["source_world_model_state_digest"],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "selected_candidate_id": source["selected_candidate_id"],
        "invoked_frontier_candidate_id": source["invoked_frontier_candidate_id"],
        "invoked_frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "invoked_frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "world_disposition_review_certificate": review,
        REVIEW_DIGEST_FIELD: review_digest,
        "world_disposition_intake_context_digest": context_digest,
        "world_disposition_intake_policy_digest": world_disposition_intake_policy_digest,
        "world_disposition_responsibility_digest": world_disposition_responsibility_digest,
        "world_disposition_request_id": world_disposition_request_id,
        "verified_host_effect_world_disposition_bundle_digest": verified_host_effect_world_disposition_bundle_digest,
        "world_disposition": disposition,
        "world_disposition_state_before": STATE_BEFORE,
        "world_disposition_state_after": state_after,
        "world_disposition_record": record,
        "world_disposition_record_digest": record_digest,
        "world_disposition_debt_consumption_record": debt,
        "world_disposition_debt_consumption_record_digest": debt_digest,
        "world_candidate_envelope": candidate,
        "world_candidate_envelope_digest": candidate_digest,
    }
    receipt.update(
        {
            "source_verification_receipt_supplied": True,
            "source_verification_receipt_fully_revalidated": True,
            "source_verification_supported": True,
            "world_disposition_review_certificate_bound": True,
            "world_disposition_reviewer_identity_bound": True,
            "world_candidate_fact_digest_bound": True,
            "world_candidate_relation_digest_bound": True,
            "world_update_patch_digest_bound": True,
            "world_update_precondition_digest_bound": True,
            "world_update_postcondition_digest_bound": True,
            "causal_model_claim_digest_bound": True,
            "realized_dukkha_assessment_digest_bound": True,
            "protected_group_realized_impact_digest_bound": True,
            "future_subject_realized_impact_digest_bound": True,
            "exactly_one_world_disposition_receipt_issued": True,
            "world_disposition_review_performed": True,
            "world_candidate_prepared": ready,
            "exactly_one_world_candidate_prepared": ready,
            "world_disposition_debt_consumed": ready,
            "world_disposition_debt_replay_closed": ready,
            "world_disposition_double_consumed": False,
            "world_disposition_review_certificate_replay_closed": True,
            "world_disposition_intake_nonce_consumed": True,
            "world_disposition_intake_nonce_replay_closed": True,
            "source_verification_receipt_replay_closed": ready,
            "world_disposition_intake_session_replay_fresh_before_intake": session_fresh,
            "world_disposition_review_replay_fresh_before_intake": review_fresh,
            "world_disposition_intake_nonce_replay_fresh_before_intake": nonce_fresh,
            "source_verification_receipt_replay_fresh_before_disposition": source_fresh,
            "world_conditions_current": world_current,
            "world_disposition_review_duration_current": duration,
            "world_disposition_intake_delay_current": delay_current,
            "world_disposition_debt_open": not ready,
            "world_commit_authorization_intake_admitted": ready,
            "world_commit_authorization_receipt_required": ready,
            "world_commit_authorization_completed": False,
            "persistent_world_model_state_unchanged": True,
            "world_fact_confirmed": False,
            "causal_attribution_confirmed": False,
            "dukkha_reduction_realized_confirmed": False,
            "host_operation_reexecuted": False,
            "observation_reperformed": False,
            "verification_reperformed": False,
            "tool_invocation_performed": False,
            "external_side_effect_performed": False,
            "persistent_host_state_changed_by_world_disposition": False,
            "persistent_world_state_changed_by_world_disposition": False,
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
            "selection_authority_granted_to_world": False,
            "plan_revision_authority_granted_to_world": False,
            "dukkha_minimization_authority_granted_to_world": False,
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
    )
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return WORLDDukkhaPreservingVerifiedHostEffectDispositionResult(STATUS_READY, [], receipt)
