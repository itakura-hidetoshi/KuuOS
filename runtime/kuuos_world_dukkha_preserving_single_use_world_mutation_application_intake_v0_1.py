#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_world_dukkha_preserving_single_use_world_candidate_commit_authorization_intake_v0_1 import (
    RECEIPT_DIGEST_FIELD as SOURCE_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD as SOURCE_REVIEW_DIGEST_FIELD,
    canonical_digest,
    compute_world_candidate_commit_authorization_review_certificate_digest,
)

STATUS_READY, STATUS_BLOCKED = "ready", "blocked"

RECEIPT_DIGEST_FIELD = (
    "world_dukkha_preserving_single_use_world_mutation_application_intake_receipt_digest"
)
REVIEW_DIGEST_FIELD = "world_mutation_application_review_certificate_digest"
CONTEXT_DIGEST_FIELD = "world_mutation_application_intake_context_digest"

STATE_BEFORE = "world_candidate_commit_authorized_not_applied"
STATE_AFTER_READY = "world_candidate_commit_applied_world_fact_unconfirmed"

DISPOSITION_READY = "world_mutation_application_ready"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_CONTEXT_REFRESH = "world_mutation_application_context_refresh_required"
DISPOSITION_REVIEW_REFRESH = "world_mutation_application_review_refresh_required"
DISPOSITION_EXPIRED = "world_mutation_authorization_expired"
DISPOSITION_AUTHORIZATION_REVALIDATION = "world_mutation_authorization_revalidation_required"
DISPOSITION_CANDIDATE_REVALIDATION = "world_candidate_revalidation_required"
DISPOSITION_PATCH_REPAIR = "world_patch_repair_required"
DISPOSITION_PRECONDITION_REPAIR = "world_precondition_repair_required"
DISPOSITION_ATOMICITY_REPAIR = "world_atomicity_repair_required"
DISPOSITION_STORAGE_REPAIR = "world_storage_target_repair_required"
DISPOSITION_REVISION_REPAIR = "world_revision_repair_required"
DISPOSITION_POSTCONDITION_REPAIR = "world_postcondition_verification_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "provenance_repair_required"
DISPOSITION_OWNER_REJECTED = "mutation_owner_rejected"
DISPOSITION_NONEXTERNALIZATION_REVIEW = "nonexternalization_review_required"
DISPOSITION_DUKKHA_REVIEW = "dukkha_preservation_review_required"
DISPOSITION_COMPENSATION_REPAIR = "compensation_route_repair_required"
DISPOSITION_TRUTH_PROMOTION_REJECTED = "truth_promotion_rejected"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"

SOURCE_TRUE = (
    "source_world_disposition_receipt_supplied",
    "source_world_disposition_receipt_fully_revalidated",
    "source_world_candidate_prepared",
    "source_world_candidate_envelope_bound",
    "source_world_disposition_record_bound",
    "source_world_disposition_review_certificate_bound",
    "world_candidate_commit_authorization_review_certificate_bound",
    "authorization_owner_identity_bound",
    "authorization_scope_bound",
    "authorization_constraints_bound",
    "world_update_patch_bound",
    "world_update_precondition_bound",
    "world_update_postcondition_bound",
    "rollback_route_bound",
    "compensation_route_bound",
    "exactly_one_world_candidate_commit_authorization_receipt_issued",
    "world_candidate_commit_authorization_review_performed",
    "world_candidate_commit_authorization_granted",
    "bounded_world_candidate_commit_authorization_granted",
    "single_use_world_candidate_commit_authorization_granted",
    "world_candidate_commit_authorization_debt_consumed",
    "world_candidate_commit_authorization_debt_replay_closed",
    "world_candidate_commit_authorization_review_certificate_replay_closed",
    "world_commit_authorization_intake_nonce_consumed",
    "world_commit_authorization_intake_nonce_replay_closed",
    "source_world_candidate_replay_closed",
    "world_conditions_current",
    "world_candidate_commit_authorization_review_duration_current",
    "world_commit_authorization_intake_delay_current",
    "world_candidate_commit_authorization_expiry_current",
    "world_mutation_application_intake_admitted",
    "world_mutation_application_receipt_required",
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
    "world_candidate_commit_authorization_double_consumed",
    "world_candidate_commit_authorization_debt_open",
    "world_mutation_application_completed",
    "world_candidate_commit_completed",
    "world_fact_confirmed",
    "causal_attribution_confirmed",
    "dukkha_reduction_realized_confirmed",
    "host_operation_reexecuted",
    "observation_reperformed",
    "verification_reperformed",
    "world_disposition_reperformed",
    "tool_invocation_performed",
    "external_side_effect_performed",
    "persistent_host_state_changed_by_authorization",
    "persistent_world_state_changed_by_authorization",
    "compensation_performed",
    "automatic_truth_promotion",
    "automatic_plan_completion",
    "automatic_rollback",
    "automatic_compensation",
    "selection_authority_granted_to_world",
    "plan_revision_authority_granted_to_world",
    "dukkha_minimization_authority_granted_to_world",
    "general_execution_authority_granted",
    "execution_permission",
    "world_mutation_authority_granted",
    "active_now",
)

REVIEW_FIELDS = {
    "source_world_candidate_commit_authorization_receipt_digest",
    "world_candidate_commit_authorization_record_digest",
    "world_candidate_commit_authorization_debt_consumption_record_digest",
    "world_mutation_application_handoff_envelope_digest",
    "source_world_candidate_envelope_digest",
    SOURCE_REVIEW_DIGEST_FIELD,
    "frontier_materialization_candidate_id",
    "frontier_adapter_id",
    "frontier_binding_digest",
    "world_candidate_fact_digest",
    "world_candidate_relation_digest",
    "world_update_patch_digest",
    "world_update_precondition_digest",
    "world_update_postcondition_digest",
    "authorization_scope_digest",
    "authorization_constraints_digest",
    "world_mutation_application_policy_digest",
    "rollback_route_digest",
    "compensation_route_digest",
    "authorization_owner_id",
    "authorization_expiry_epoch",
    "world_state_before_digest",
    "world_state_after_digest",
    "world_mutation_transaction_digest",
    "atomic_application_policy_digest",
    "persistent_world_storage_target_digest",
    "postcondition_verification_policy_digest",
    "mutation_owner_id",
    "application_review_started_epoch",
    "application_review_completed_epoch",
    "maximum_application_review_duration",
    "expected_world_model_revision_before",
    "expected_world_model_revision_after",
    "source_authorization_ready",
    "source_authorization_single_use",
    "source_authorization_unconsumed",
    "candidate_identity_match",
    "patch_identity_match",
    "world_patch_scope_conformant",
    "world_patch_ceiling_not_exceeded",
    "world_preconditions_revalidated",
    "atomic_application_supported",
    "persistent_world_storage_target_available",
    "revision_increment_exactly_one",
    "world_postconditions_verifiable",
    "lineage_continuity_preserved",
    "responsibility_continuity_preserved",
    "mutation_owner_confirmed",
    "dukkha_preservation_supported",
    "protected_group_nonexternalization_supported",
    "future_nonexternalization_supported",
    "rollback_route_ready",
    "compensation_route_ready",
    "no_causal_overclaim",
    "no_realized_dukkha_overclaim",
    "world_fact_claimed",
    "causal_attribution_claimed",
    "realized_dukkha_reduction_claimed",
    "tool_invocation_requested",
    "external_side_effect_requested",
    "world_mutation_already_performed",
    REVIEW_DIGEST_FIELD,
}

CONTEXT_FIELDS = {
    "source_world_candidate_commit_authorization_receipt_digest",
    REVIEW_DIGEST_FIELD,
    "current_world_binding_digest",
    "current_world_model_state_digest",
    "current_world_model_revision",
    "current_world_lineage_digest",
    "source_world_candidate_commit_authorized_epoch",
    "world_mutation_application_intake_epoch",
    "maximum_world_mutation_application_intake_delay",
    "world_mutation_application_intake_session_id",
    "world_mutation_application_intake_nonce_digest",
    "prior_world_mutation_application_intake_session_ids",
    "prior_world_mutation_application_review_certificate_digests",
    "prior_world_mutation_application_intake_nonce_digests",
    "prior_consumed_source_authorization_receipt_digests",
    "prior_applied_world_mutation_transaction_digests",
    "requested_world_mutation_application_operation_digest",
    "exact_world_mutation_application_cycle_digest",
    CONTEXT_DIGEST_FIELD,
}


@dataclass
class WORLDDukkhaPreservingSingleUseWorldMutationApplicationResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def _map(value: Any) -> dict:
    return dict(value) if isinstance(value, Mapping) else {}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    item = dict(value)
    item.pop(field, None)
    return canonical_digest(item)


def compute_world_mutation_application_review_certificate_digest(
    value: Mapping[str, Any],
) -> str:
    return _digest_without(value, REVIEW_DIGEST_FIELD)


def compute_world_mutation_application_intake_context_digest(
    value: Mapping[str, Any],
) -> str:
    return _digest_without(value, CONTEXT_DIGEST_FIELD)


def compute_world_mutation_application_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def _strings(value: Any, allow_empty: bool = False) -> tuple[bool, list[str]]:
    ok = isinstance(value, list) and (allow_empty or bool(value)) and all(
        isinstance(item, str) and item for item in value
    )
    values = list(value) if isinstance(value, list) else []
    return ok and values == sorted(values) and len(values) == len(set(values)), values


def _exact(
    actual: Mapping[str, Any],
    expected: Mapping[str, Any],
    prefix: str,
    blockers: list[str],
) -> None:
    blockers.extend(
        f"{prefix}_{key}_mismatch"
        for key, expected_value in expected.items()
        if actual.get(key) != expected_value
    )


def compute_requested_world_mutation_application_operation_digest(
    source: Mapping[str, Any],
    review: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_world_candidate_commit_authorization_receipt_digest": source.get(
                SOURCE_DIGEST_FIELD
            ),
            "world_candidate_commit_authorization_record_digest": source.get(
                "world_candidate_commit_authorization_record_digest"
            ),
            "world_mutation_application_handoff_envelope_digest": source.get(
                "world_mutation_application_handoff_envelope_digest"
            ),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
            "frontier_materialization_candidate_id": source.get(
                "invoked_frontier_candidate_id"
            ),
            "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
            "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
            "world_mutation_transaction_digest": review.get(
                "world_mutation_transaction_digest"
            ),
            "state_before": STATE_BEFORE,
            "ready_state_after": STATE_AFTER_READY,
        }
    )


def compute_exact_world_mutation_application_cycle_digest(
    source: Mapping[str, Any],
    review: Mapping[str, Any],
    context: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_world_candidate_commit_authorization_receipt_digest": source.get(
                SOURCE_DIGEST_FIELD
            ),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
            "world_mutation_transaction_digest": review.get(
                "world_mutation_transaction_digest"
            ),
            "world_mutation_application_intake_session_id": context.get(
                "world_mutation_application_intake_session_id"
            ),
            "world_mutation_application_intake_nonce_digest": context.get(
                "world_mutation_application_intake_nonce_digest"
            ),
            "world_mutation_application_intake_epoch": context.get(
                "world_mutation_application_intake_epoch"
            ),
            "current_world_model_revision": context.get("current_world_model_revision"),
            "requested_world_mutation_application_operation_digest": context.get(
                "requested_world_mutation_application_operation_digest"
            ),
        }
    )


def _verify_source(source: dict, expected: str, blockers: list[str]):
    if not source:
        blockers.append("source_world_candidate_commit_authorization_receipt_missing")
        return "", {}, [], []

    _exact(
        source,
        {
            "kernel": (
                "WORLD Dukkha-Preserving Single-Use World-Candidate Commit "
                "Authorization Intake Kernel"
            ),
            "kernel_version": "v0.1",
            "world_version": "v0.61",
            "status": (
                "WORLD_DUKKHA_PRESERVING_SINGLE_USE_WORLD_CANDIDATE_"
                "COMMIT_AUTHORIZATION_ROUTED"
            ),
            "world_candidate_commit_authorization_disposition": (
                "world_candidate_commit_authorization_ready"
            ),
            "world_candidate_commit_authorization_state_before": (
                "verified_host_effect_world_candidate_prepared_not_committed"
            ),
            "world_candidate_commit_authorization_state_after": STATE_BEFORE,
        },
        "source",
        blockers,
    )

    digest = source.get(SOURCE_DIGEST_FIELD, "")
    if not digest:
        blockers.append("source_world_candidate_commit_authorization_receipt_digest_missing")
    elif digest != _digest_without(source, SOURCE_DIGEST_FIELD):
        blockers.append("source_world_candidate_commit_authorization_receipt_digest_mismatch")
    if digest != expected:
        blockers.append("source_world_candidate_commit_authorization_expected_binding_mismatch")

    for field in SOURCE_TRUE:
        if source.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in SOURCE_FALSE:
        if source.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")

    source_review = _map(
        source.get("world_candidate_commit_authorization_review_certificate")
    )
    record = _map(source.get("world_candidate_commit_authorization_record"))
    debt = _map(
        source.get("world_candidate_commit_authorization_debt_consumption_record")
    )
    handoff = _map(source.get("world_mutation_application_handoff_envelope"))

    if not source_review:
        blockers.append("source_world_candidate_commit_authorization_review_invalid")
    elif source.get(SOURCE_REVIEW_DIGEST_FIELD) != (
        compute_world_candidate_commit_authorization_review_certificate_digest(
            source_review
        )
    ):
        blockers.append(
            "source_world_candidate_commit_authorization_review_digest_mismatch"
        )

    for name, item, field in (
        (
            "world_candidate_commit_authorization_record",
            record,
            "world_candidate_commit_authorization_record_digest",
        ),
        (
            "world_candidate_commit_authorization_debt_consumption_record",
            debt,
            "world_candidate_commit_authorization_debt_consumption_record_digest",
        ),
        (
            "world_mutation_application_handoff_envelope",
            handoff,
            "world_mutation_application_handoff_envelope_digest",
        ),
    ):
        if not item:
            blockers.append(f"source_{name}_invalid")
        elif source.get(field) != canonical_digest(item):
            blockers.append(f"source_{name}_digest_mismatch")

    _exact(
        record,
        {
            "source_world_disposition_receipt_digest": source.get(
                "source_world_disposition_receipt_digest"
            ),
            "world_disposition_record_digest": source.get(
                "source_world_disposition_record_digest"
            ),
            "world_candidate_envelope_digest": source.get(
                "source_world_candidate_envelope_digest"
            ),
            SOURCE_REVIEW_DIGEST_FIELD: source.get(SOURCE_REVIEW_DIGEST_FIELD),
            "frontier_materialization_candidate_id": source.get(
                "invoked_frontier_candidate_id"
            ),
            "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
            "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
            "authorization_owner_id": source_review.get("authorization_owner_id"),
            "authorization_scope_digest": source_review.get(
                "authorization_scope_digest"
            ),
            "authorization_constraints_digest": source_review.get(
                "authorization_constraints_digest"
            ),
            "authorization_expiry_epoch": source_review.get(
                "authorization_expiry_epoch"
            ),
            "world_candidate_commit_authorization_disposition": (
                "world_candidate_commit_authorization_ready"
            ),
            "state_before": (
                "verified_host_effect_world_candidate_prepared_not_committed"
            ),
            "state_after": STATE_BEFORE,
            "authorization_outcome": (
                "single_use_world_candidate_commit_authorized_not_applied"
            ),
        },
        "source_world_candidate_commit_authorization_record",
        blockers,
    )

    _exact(
        debt,
        {
            "source_world_disposition_receipt_digest": source.get(
                "source_world_disposition_receipt_digest"
            ),
            "world_candidate_envelope_digest": source.get(
                "source_world_candidate_envelope_digest"
            ),
            SOURCE_REVIEW_DIGEST_FIELD: source.get(SOURCE_REVIEW_DIGEST_FIELD),
            "world_candidate_commit_authorization_record_digest": source.get(
                "world_candidate_commit_authorization_record_digest"
            ),
            "world_candidate_commit_authorization_debt_consumed": True,
            "source_world_candidate_marked_commit_authorized": True,
            "double_world_candidate_commit_authorization_performed": False,
        },
        "source_world_candidate_commit_authorization_debt",
        blockers,
    )

    _exact(
        handoff,
        {
            "source_world_disposition_receipt_digest": source.get(
                "source_world_disposition_receipt_digest"
            ),
            "world_candidate_envelope_digest": source.get(
                "source_world_candidate_envelope_digest"
            ),
            "world_candidate_commit_authorization_record_digest": source.get(
                "world_candidate_commit_authorization_record_digest"
            ),
            SOURCE_REVIEW_DIGEST_FIELD: source.get(SOURCE_REVIEW_DIGEST_FIELD),
            "frontier_materialization_candidate_id": source.get(
                "invoked_frontier_candidate_id"
            ),
            "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
            "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
            "world_candidate_fact_digest": source_review.get(
                "world_candidate_fact_digest"
            ),
            "world_candidate_relation_digest": source_review.get(
                "world_candidate_relation_digest"
            ),
            "world_update_patch_digest": source_review.get("world_update_patch_digest"),
            "world_update_precondition_digest": source_review.get(
                "world_update_precondition_digest"
            ),
            "world_update_postcondition_digest": source_review.get(
                "world_update_postcondition_digest"
            ),
            "authorization_scope_digest": source_review.get(
                "authorization_scope_digest"
            ),
            "authorization_constraints_digest": source_review.get(
                "authorization_constraints_digest"
            ),
            "world_mutation_application_policy_digest": source_review.get(
                "world_mutation_application_policy_digest"
            ),
            "rollback_route_digest": source_review.get("rollback_route_digest"),
            "compensation_route_digest": source_review.get(
                "compensation_route_digest"
            ),
            "authorization_owner_id": source_review.get("authorization_owner_id"),
            "authorization_expiry_epoch": source_review.get(
                "authorization_expiry_epoch"
            ),
            "authorization_state": "authorized_single_use_not_applied",
            "candidate_commit_state": "authorized_not_applied",
            "world_fact_state": "candidate_only_not_fact",
            "causal_attribution_state": "not_confirmed",
            "dukkha_realization_state": "not_confirmed",
            "world_mutation_application_intake_admitted": True,
            "world_mutation_application_receipt_required": True,
            "single_use_authorization": True,
            "compensation_route_ready": True,
        },
        "source_world_mutation_application_handoff",
        blockers,
    )

    for field in (
        "world_candidate_fact_digest",
        "world_candidate_relation_digest",
        "world_update_patch_digest",
        "world_update_precondition_digest",
        "world_update_postcondition_digest",
        "authorization_scope_digest",
        "authorization_constraints_digest",
        "world_mutation_application_policy_digest",
        "rollback_route_digest",
        "compensation_route_digest",
        "authorization_owner_id",
    ):
        if not isinstance(handoff.get(field), str) or not handoff.get(field):
            blockers.append(f"source_world_mutation_handoff_{field}_invalid")

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
        blockers.append("world_mutation_application_review_certificate_missing")
        return "", False

    if set(review) != REVIEW_FIELDS:
        blockers.append("world_mutation_application_review_certificate_schema_invalid")

    digest = review.get(REVIEW_DIGEST_FIELD, "")
    if not digest:
        blockers.append("world_mutation_application_review_certificate_digest_missing")
    elif digest != compute_world_mutation_application_review_certificate_digest(review):
        blockers.append("world_mutation_application_review_certificate_digest_mismatch")
    if digest != expected:
        blockers.append("world_mutation_application_review_expected_binding_mismatch")

    _exact(
        review,
        {
            "source_world_candidate_commit_authorization_receipt_digest": source.get(
                SOURCE_DIGEST_FIELD
            ),
            "world_candidate_commit_authorization_record_digest": source.get(
                "world_candidate_commit_authorization_record_digest"
            ),
            "world_candidate_commit_authorization_debt_consumption_record_digest": source.get(
                "world_candidate_commit_authorization_debt_consumption_record_digest"
            ),
            "world_mutation_application_handoff_envelope_digest": source.get(
                "world_mutation_application_handoff_envelope_digest"
            ),
            "source_world_candidate_envelope_digest": source.get(
                "source_world_candidate_envelope_digest"
            ),
            SOURCE_REVIEW_DIGEST_FIELD: source.get(SOURCE_REVIEW_DIGEST_FIELD),
            "frontier_materialization_candidate_id": source.get(
                "invoked_frontier_candidate_id"
            ),
            "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
            "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
            "world_candidate_fact_digest": handoff.get("world_candidate_fact_digest"),
            "world_candidate_relation_digest": handoff.get(
                "world_candidate_relation_digest"
            ),
            "world_update_patch_digest": handoff.get("world_update_patch_digest"),
            "world_update_precondition_digest": handoff.get(
                "world_update_precondition_digest"
            ),
            "world_update_postcondition_digest": handoff.get(
                "world_update_postcondition_digest"
            ),
            "authorization_scope_digest": handoff.get("authorization_scope_digest"),
            "authorization_constraints_digest": handoff.get(
                "authorization_constraints_digest"
            ),
            "world_mutation_application_policy_digest": handoff.get(
                "world_mutation_application_policy_digest"
            ),
            "rollback_route_digest": handoff.get("rollback_route_digest"),
            "compensation_route_digest": handoff.get("compensation_route_digest"),
            "authorization_owner_id": handoff.get("authorization_owner_id"),
            "authorization_expiry_epoch": handoff.get("authorization_expiry_epoch"),
        },
        "world_mutation_application_review",
        blockers,
    )

    for field in (
        "world_state_before_digest",
        "world_state_after_digest",
        "world_mutation_transaction_digest",
        "atomic_application_policy_digest",
        "persistent_world_storage_target_digest",
        "postcondition_verification_policy_digest",
        "mutation_owner_id",
    ):
        if not isinstance(review.get(field), str) or not review.get(field):
            blockers.append(f"world_mutation_application_review_{field}_invalid")

    for field in (
        "source_authorization_ready",
        "source_authorization_single_use",
        "source_authorization_unconsumed",
        "candidate_identity_match",
        "patch_identity_match",
        "world_patch_scope_conformant",
        "world_patch_ceiling_not_exceeded",
        "world_preconditions_revalidated",
        "atomic_application_supported",
        "persistent_world_storage_target_available",
        "revision_increment_exactly_one",
        "world_postconditions_verifiable",
        "lineage_continuity_preserved",
        "responsibility_continuity_preserved",
        "mutation_owner_confirmed",
        "dukkha_preservation_supported",
        "protected_group_nonexternalization_supported",
        "future_nonexternalization_supported",
        "rollback_route_ready",
        "compensation_route_ready",
        "no_causal_overclaim",
        "no_realized_dukkha_overclaim",
        "world_fact_claimed",
        "causal_attribution_claimed",
        "realized_dukkha_reduction_claimed",
        "tool_invocation_requested",
        "external_side_effect_requested",
        "world_mutation_already_performed",
    ):
        if not isinstance(review.get(field), bool):
            blockers.append(f"world_mutation_application_review_{field}_invalid")

    for field in (
        "application_review_started_epoch",
        "application_review_completed_epoch",
        "maximum_application_review_duration",
        "expected_world_model_revision_before",
        "expected_world_model_revision_after",
    ):
        value = review.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"world_mutation_application_review_{field}_invalid")

    start = review.get("application_review_started_epoch")
    end = review.get("application_review_completed_epoch")
    maximum = review.get("maximum_application_review_duration")
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
    review: dict,
    blockers: list[str],
):
    if not context:
        blockers.append("world_mutation_application_intake_context_missing")
        return "", (False,) * 8

    if set(context) != CONTEXT_FIELDS:
        blockers.append("world_mutation_application_intake_context_schema_invalid")

    digest = context.get(CONTEXT_DIGEST_FIELD, "")
    if not digest:
        blockers.append("world_mutation_application_intake_context_digest_missing")
    elif digest != compute_world_mutation_application_intake_context_digest(context):
        blockers.append("world_mutation_application_intake_context_digest_mismatch")
    if digest != expected:
        blockers.append("world_mutation_application_intake_context_expected_binding_mismatch")

    _exact(
        context,
        {
            "source_world_candidate_commit_authorization_receipt_digest": source.get(
                SOURCE_DIGEST_FIELD
            ),
            REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        },
        "world_mutation_application_intake_context",
        blockers,
    )

    for field in (
        "current_world_binding_digest",
        "current_world_model_state_digest",
        "current_world_lineage_digest",
        "world_mutation_application_intake_session_id",
        "world_mutation_application_intake_nonce_digest",
        "requested_world_mutation_application_operation_digest",
        "exact_world_mutation_application_cycle_digest",
    ):
        if not isinstance(context.get(field), str) or not context.get(field):
            blockers.append(f"world_mutation_application_intake_context_{field}_invalid")

    for field in (
        "current_world_model_revision",
        "source_world_candidate_commit_authorized_epoch",
        "world_mutation_application_intake_epoch",
        "maximum_world_mutation_application_intake_delay",
    ):
        value = context.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"world_mutation_application_intake_context_{field}_invalid")

    world_current = all(
        context.get(key) == value
        for key, value in {
            "current_world_binding_digest": source.get("source_world_binding_digest"),
            "current_world_model_state_digest": source.get(
                "source_world_model_state_digest"
            ),
            "current_world_model_revision": source.get("source_world_model_revision"),
            "current_world_lineage_digest": source.get("source_world_lineage_digest"),
        }.items()
    )

    if context.get(
        "requested_world_mutation_application_operation_digest"
    ) != compute_requested_world_mutation_application_operation_digest(source, review):
        blockers.append("world_mutation_application_intake_context_operation_digest_mismatch")

    if context.get(
        "exact_world_mutation_application_cycle_digest"
    ) != compute_exact_world_mutation_application_cycle_digest(source, review, context):
        blockers.append("world_mutation_application_intake_context_cycle_digest_mismatch")

    authorized = context.get("source_world_candidate_commit_authorized_epoch")
    epoch = context.get("world_mutation_application_intake_epoch")
    maximum = context.get("maximum_world_mutation_application_intake_delay")
    delay_current = (
        all(
            isinstance(value, int) and not isinstance(value, bool)
            for value in (authorized, epoch, maximum)
        )
        and 1 <= maximum <= 64
        and 0 <= epoch - authorized <= maximum
    )

    expiry = review.get("authorization_expiry_epoch")
    expiry_current = (
        isinstance(epoch, int)
        and not isinstance(epoch, bool)
        and isinstance(expiry, int)
        and not isinstance(expiry, bool)
        and epoch <= expiry
    )

    values = []
    for field in (
        "prior_world_mutation_application_intake_session_ids",
        "prior_world_mutation_application_review_certificate_digests",
        "prior_world_mutation_application_intake_nonce_digests",
        "prior_consumed_source_authorization_receipt_digests",
        "prior_applied_world_mutation_transaction_digests",
    ):
        ok, items = _strings(context.get(field), True)
        if not ok:
            blockers.append(f"world_mutation_application_intake_context_{field}_invalid")
        values.append(items)

    sessions, reviews, nonces, sources, transactions = values
    return digest, (
        world_current,
        delay_current,
        expiry_current,
        context.get("world_mutation_application_intake_session_id") not in sessions,
        review.get(REVIEW_DIGEST_FIELD) not in reviews,
        context.get("world_mutation_application_intake_nonce_digest") not in nonces,
        source.get(SOURCE_DIGEST_FIELD) not in sources,
        review.get("world_mutation_transaction_digest") not in transactions,
    )


def _route(
    review: Mapping[str, Any],
    duration_current: bool,
    checks: tuple[bool, ...],
) -> str:
    (
        world_current,
        delay_current,
        expiry_current,
        session_fresh,
        review_fresh,
        nonce_fresh,
        source_fresh,
        transaction_fresh,
    ) = checks

    if not all(
        (
            session_fresh,
            review_fresh,
            nonce_fresh,
            source_fresh,
            transaction_fresh,
        )
    ):
        return DISPOSITION_REPLAY_REJECTED
    if not world_current:
        return DISPOSITION_WORLD_REFRESH
    if not delay_current:
        return DISPOSITION_CONTEXT_REFRESH
    if not duration_current:
        return DISPOSITION_REVIEW_REFRESH
    if not expiry_current:
        return DISPOSITION_EXPIRED
    if any(
        review.get(field)
        for field in (
            "world_fact_claimed",
            "causal_attribution_claimed",
            "realized_dukkha_reduction_claimed",
            "tool_invocation_requested",
            "external_side_effect_requested",
            "world_mutation_already_performed",
        )
    ) or not review.get("no_causal_overclaim") or not review.get(
        "no_realized_dukkha_overclaim"
    ):
        return DISPOSITION_TRUTH_PROMOTION_REJECTED
    if not review.get("mutation_owner_confirmed"):
        return DISPOSITION_OWNER_REJECTED
    if not all(
        review.get(field)
        for field in (
            "source_authorization_ready",
            "source_authorization_single_use",
            "source_authorization_unconsumed",
        )
    ):
        return DISPOSITION_AUTHORIZATION_REVALIDATION
    if not review.get("candidate_identity_match"):
        return DISPOSITION_CANDIDATE_REVALIDATION
    if not all(
        review.get(field)
        for field in (
            "patch_identity_match",
            "world_patch_scope_conformant",
            "world_patch_ceiling_not_exceeded",
        )
    ):
        return DISPOSITION_PATCH_REPAIR
    if not review.get("world_preconditions_revalidated"):
        return DISPOSITION_PRECONDITION_REPAIR
    if not review.get("atomic_application_supported"):
        return DISPOSITION_ATOMICITY_REPAIR
    if not review.get("persistent_world_storage_target_available"):
        return DISPOSITION_STORAGE_REPAIR
    if (
        not review.get("revision_increment_exactly_one")
        or review.get("expected_world_model_revision_before")
        != review.get("expected_world_model_revision_after") - 1
    ):
        return DISPOSITION_REVISION_REPAIR
    if not review.get("world_postconditions_verifiable"):
        return DISPOSITION_POSTCONDITION_REPAIR
    if not review.get("lineage_continuity_preserved") or not review.get(
        "responsibility_continuity_preserved"
    ):
        return DISPOSITION_PROVENANCE_REPAIR
    if not review.get("protected_group_nonexternalization_supported") or not review.get(
        "future_nonexternalization_supported"
    ):
        return DISPOSITION_NONEXTERNALIZATION_REVIEW
    if not review.get("dukkha_preservation_supported"):
        return DISPOSITION_DUKKHA_REVIEW
    if not review.get("rollback_route_ready") or not review.get(
        "compensation_route_ready"
    ):
        return DISPOSITION_COMPENSATION_REPAIR
    return DISPOSITION_READY


def build_world_dukkha_preserving_single_use_world_mutation_application_intake(
    *,
    source_world_candidate_commit_authorization_receipt: Mapping[str, Any],
    expected_source_world_candidate_commit_authorization_receipt_digest: str,
    world_mutation_application_review_certificate: Mapping[str, Any],
    expected_world_mutation_application_review_certificate_digest: str,
    world_mutation_application_intake_context: Mapping[str, Any],
    expected_world_mutation_application_intake_context_digest: str,
    world_mutation_application_policy_digest: str,
    world_mutation_application_responsibility_digest: str,
    world_mutation_application_request_id: str,
    world_mutation_application_bundle_digest: str,
) -> WORLDDukkhaPreservingSingleUseWorldMutationApplicationResult:
    blockers: list[str] = []
    source = _map(source_world_candidate_commit_authorization_receipt)
    review = _map(world_mutation_application_review_certificate)
    context = _map(world_mutation_application_intake_context)

    for name, value in {
        "expected_source_world_candidate_commit_authorization_receipt_digest": (
            expected_source_world_candidate_commit_authorization_receipt_digest
        ),
        "expected_world_mutation_application_review_certificate_digest": (
            expected_world_mutation_application_review_certificate_digest
        ),
        "expected_world_mutation_application_intake_context_digest": (
            expected_world_mutation_application_intake_context_digest
        ),
        "world_mutation_application_policy_digest": world_mutation_application_policy_digest,
        "world_mutation_application_responsibility_digest": (
            world_mutation_application_responsibility_digest
        ),
        "world_mutation_application_request_id": world_mutation_application_request_id,
        "world_mutation_application_bundle_digest": world_mutation_application_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    source_digest, handoff, lineage, responsibility = _verify_source(
        source,
        expected_source_world_candidate_commit_authorization_receipt_digest,
        blockers,
    )
    review_digest, duration_current = _verify_review(
        review,
        expected_world_mutation_application_review_certificate_digest,
        source,
        handoff,
        blockers,
    )
    context_digest, checks = _verify_context(
        context,
        expected_world_mutation_application_intake_context_digest,
        source,
        review,
        blockers,
    )

    if not blockers:
        bundle = compute_world_mutation_application_bundle_digest(
            source_world_candidate_commit_authorization_receipt_digest=source_digest,
            expected_source_world_candidate_commit_authorization_receipt_digest=(
                expected_source_world_candidate_commit_authorization_receipt_digest
            ),
            world_candidate_commit_authorization_record_digest=source.get(
                "world_candidate_commit_authorization_record_digest"
            ),
            world_mutation_application_handoff_envelope_digest=source.get(
                "world_mutation_application_handoff_envelope_digest"
            ),
            world_mutation_application_review_certificate_digest=review_digest,
            expected_world_mutation_application_review_certificate_digest=(
                expected_world_mutation_application_review_certificate_digest
            ),
            world_mutation_application_intake_context_digest=context_digest,
            expected_world_mutation_application_intake_context_digest=(
                expected_world_mutation_application_intake_context_digest
            ),
            requested_world_mutation_application_operation_digest=context.get(
                "requested_world_mutation_application_operation_digest"
            ),
            exact_world_mutation_application_cycle_digest=context.get(
                "exact_world_mutation_application_cycle_digest"
            ),
            world_mutation_transaction_digest=review.get(
                "world_mutation_transaction_digest"
            ),
            world_mutation_application_policy_digest=world_mutation_application_policy_digest,
            world_mutation_application_responsibility_digest=(
                world_mutation_application_responsibility_digest
            ),
            world_mutation_application_request_id=world_mutation_application_request_id,
        )
        if bundle != world_mutation_application_bundle_digest:
            blockers.append("world_mutation_application_bundle_digest_mismatch")

    if blockers:
        return WORLDDukkhaPreservingSingleUseWorldMutationApplicationResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    disposition = _route(review, duration_current, checks)
    ready = disposition == DISPOSITION_READY
    state_after = STATE_AFTER_READY if ready else STATE_BEFORE

    application_record = {
        "source_world_candidate_commit_authorization_receipt_digest": source_digest,
        "world_candidate_commit_authorization_record_digest": source[
            "world_candidate_commit_authorization_record_digest"
        ],
        "world_mutation_application_handoff_envelope_digest": source[
            "world_mutation_application_handoff_envelope_digest"
        ],
        REVIEW_DIGEST_FIELD: review_digest,
        "source_world_candidate_envelope_digest": source[
            "source_world_candidate_envelope_digest"
        ],
        "frontier_materialization_candidate_id": source[
            "invoked_frontier_candidate_id"
        ],
        "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "world_mutation_transaction_digest": review[
            "world_mutation_transaction_digest"
        ],
        "mutation_owner_id": review["mutation_owner_id"],
        "persistent_world_storage_target_digest": review[
            "persistent_world_storage_target_digest"
        ],
        "world_state_before_digest": review["world_state_before_digest"],
        "world_state_after_digest": review["world_state_after_digest"],
        "world_model_revision_before": review[
            "expected_world_model_revision_before"
        ],
        "world_model_revision_after": review["expected_world_model_revision_after"],
        "world_mutation_application_intake_session_id": context[
            "world_mutation_application_intake_session_id"
        ],
        "world_mutation_application_intake_nonce_digest": context[
            "world_mutation_application_intake_nonce_digest"
        ],
        "world_mutation_application_intake_epoch": context[
            "world_mutation_application_intake_epoch"
        ],
        "world_mutation_application_disposition": disposition,
        "state_before": STATE_BEFORE,
        "state_after": state_after,
        "application_outcome": (
            "single_use_bounded_world_mutation_applied_world_fact_unconfirmed"
            if ready
            else "world_mutation_application_routed_without_world_change"
        ),
    }
    application_record_digest = canonical_digest(application_record)

    authorization_consumption = {
        "source_world_candidate_commit_authorization_receipt_digest": source_digest,
        "world_candidate_commit_authorization_record_digest": source[
            "world_candidate_commit_authorization_record_digest"
        ],
        "world_mutation_application_handoff_envelope_digest": source[
            "world_mutation_application_handoff_envelope_digest"
        ],
        "world_mutation_transaction_digest": review[
            "world_mutation_transaction_digest"
        ],
        "world_mutation_application_record_digest": application_record_digest,
        "single_use_world_candidate_commit_authorization_consumed": ready,
        "source_authorization_receipt_marked_consumed": ready,
        "source_authorization_handoff_marked_applied": ready,
        "double_world_mutation_application_performed": False,
    }
    authorization_consumption_digest = canonical_digest(authorization_consumption)

    mutation_record = None
    mutation_record_digest = ""
    persisted_candidate = None
    persisted_candidate_digest = ""
    verification_handoff = None
    verification_handoff_digest = ""

    if ready:
        mutation_record = {
            "source_world_candidate_commit_authorization_receipt_digest": source_digest,
            "world_candidate_commit_authorization_record_digest": source[
                "world_candidate_commit_authorization_record_digest"
            ],
            "world_mutation_application_record_digest": application_record_digest,
            "world_candidate_envelope_digest": source[
                "source_world_candidate_envelope_digest"
            ],
            REVIEW_DIGEST_FIELD: review_digest,
            "world_mutation_transaction_digest": review[
                "world_mutation_transaction_digest"
            ],
            "world_update_patch_digest": handoff["world_update_patch_digest"],
            "world_update_precondition_digest": handoff[
                "world_update_precondition_digest"
            ],
            "world_update_postcondition_digest": handoff[
                "world_update_postcondition_digest"
            ],
            "world_state_before_digest": review["world_state_before_digest"],
            "world_state_after_digest": review["world_state_after_digest"],
            "world_model_revision_before": review[
                "expected_world_model_revision_before"
            ],
            "world_model_revision_after": review[
                "expected_world_model_revision_after"
            ],
            "persistent_world_storage_target_digest": review[
                "persistent_world_storage_target_digest"
            ],
            "mutation_owner_id": review["mutation_owner_id"],
            "exactly_one_world_patch_applied": True,
            "world_mutation_transaction_atomic": True,
            "persistent_world_model_state_changed": True,
            "world_candidate_commit_completed": True,
            "world_fact_confirmed": False,
            "causal_attribution_confirmed": False,
            "dukkha_reduction_realized_confirmed": False,
            "postcondition_verification_required": True,
            "compensation_route_ready": True,
        }
        mutation_record_digest = canonical_digest(mutation_record)

        persisted_candidate = {
            "source_world_candidate_commit_authorization_receipt_digest": source_digest,
            "world_mutation_application_record_digest": application_record_digest,
            "world_mutation_record_digest": mutation_record_digest,
            "world_mutation_transaction_digest": review[
                "world_mutation_transaction_digest"
            ],
            "frontier_materialization_candidate_id": source[
                "invoked_frontier_candidate_id"
            ],
            "frontier_adapter_id": source["invoked_frontier_adapter_id"],
            "frontier_binding_digest": source["invoked_frontier_binding_digest"],
            "world_candidate_fact_digest": handoff["world_candidate_fact_digest"],
            "world_candidate_relation_digest": handoff[
                "world_candidate_relation_digest"
            ],
            "world_update_patch_digest": handoff["world_update_patch_digest"],
            "world_state_after_digest": review["world_state_after_digest"],
            "world_model_revision_after": review[
                "expected_world_model_revision_after"
            ],
            "world_candidate_commit_state": "applied_persisted_world_fact_unconfirmed",
            "world_fact_state": "persisted_candidate_not_verified_fact",
            "causal_attribution_state": "not_confirmed",
            "dukkha_realization_state": "not_confirmed",
            "postcondition_verification_intake_admitted": True,
            "postcondition_verification_receipt_required": True,
            "compensation_route_ready": True,
        }
        persisted_candidate_digest = canonical_digest(persisted_candidate)

        verification_handoff = {
            "source_world_candidate_commit_authorization_receipt_digest": source_digest,
            "world_mutation_application_record_digest": application_record_digest,
            "authorization_consumption_record_digest": authorization_consumption_digest,
            "world_mutation_record_digest": mutation_record_digest,
            "persisted_world_candidate_envelope_digest": persisted_candidate_digest,
            "world_mutation_transaction_digest": review[
                "world_mutation_transaction_digest"
            ],
            "world_update_postcondition_digest": handoff[
                "world_update_postcondition_digest"
            ],
            "world_state_after_digest": review["world_state_after_digest"],
            "world_model_revision_after": review[
                "expected_world_model_revision_after"
            ],
            "postcondition_verification_policy_digest": review[
                "postcondition_verification_policy_digest"
            ],
            "world_fact_state": "unconfirmed_pending_postcondition_verification",
            "causal_attribution_state": "not_confirmed",
            "dukkha_realization_state": "not_confirmed",
            "postcondition_verification_intake_admitted": True,
            "postcondition_verification_receipt_required": True,
            "compensation_route_ready": True,
        }
        verification_handoff_digest = canonical_digest(verification_handoff)

    resulting_lineage = sorted(
        set(lineage)
        | {
            source_digest,
            source["world_candidate_commit_authorization_record_digest"],
            source["world_mutation_application_handoff_envelope_digest"],
            review_digest,
            context_digest,
            context["requested_world_mutation_application_operation_digest"],
            context["exact_world_mutation_application_cycle_digest"],
            application_record_digest,
            authorization_consumption_digest,
            world_mutation_application_bundle_digest,
        }
        | ({mutation_record_digest} if mutation_record_digest else set())
        | ({persisted_candidate_digest} if persisted_candidate_digest else set())
        | ({verification_handoff_digest} if verification_handoff_digest else set())
    )

    resulting_responsibility = sorted(
        set(responsibility)
        | {
            review["mutation_owner_id"],
            world_mutation_application_responsibility_digest,
        }
    )

    (
        world_current,
        delay_current,
        expiry_current,
        session_fresh,
        review_fresh,
        nonce_fresh,
        source_fresh,
        transaction_fresh,
    ) = checks

    receipt = {
        "kernel": "WORLD Dukkha-Preserving Single-Use World Mutation Application Intake Kernel",
        "kernel_version": "v0.1",
        "world_version": "v0.62",
        "status": "WORLD_DUKKHA_PRESERVING_SINGLE_USE_WORLD_MUTATION_APPLICATION_ROUTED",
        "source_world_candidate_commit_authorization_receipt_digest": source_digest,
        "source_world_disposition_receipt_digest": source[
            "source_world_disposition_receipt_digest"
        ],
        "source_verification_receipt_digest": source[
            "source_verification_receipt_digest"
        ],
        "source_world_candidate_commit_authorization_record_digest": source[
            "world_candidate_commit_authorization_record_digest"
        ],
        "source_world_candidate_commit_authorization_debt_consumption_record_digest": source[
            "world_candidate_commit_authorization_debt_consumption_record_digest"
        ],
        "source_world_mutation_application_handoff_envelope_digest": source[
            "world_mutation_application_handoff_envelope_digest"
        ],
        "source_world_candidate_envelope_digest": source[
            "source_world_candidate_envelope_digest"
        ],
        "source_world_candidate_commit_authorization_review_certificate_digest": source[
            SOURCE_REVIEW_DIGEST_FIELD
        ],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source["source_world_model_state_digest"],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "selected_candidate_id": source["selected_candidate_id"],
        "invoked_frontier_candidate_id": source["invoked_frontier_candidate_id"],
        "invoked_frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "invoked_frontier_binding_digest": source[
            "invoked_frontier_binding_digest"
        ],
        "world_mutation_application_review_certificate": review,
        REVIEW_DIGEST_FIELD: review_digest,
        CONTEXT_DIGEST_FIELD: context_digest,
        "world_mutation_application_policy_digest": world_mutation_application_policy_digest,
        "world_mutation_application_responsibility_digest": (
            world_mutation_application_responsibility_digest
        ),
        "world_mutation_application_request_id": world_mutation_application_request_id,
        "world_mutation_application_bundle_digest": world_mutation_application_bundle_digest,
        "world_mutation_application_disposition": disposition,
        "world_mutation_application_state_before": STATE_BEFORE,
        "world_mutation_application_state_after": state_after,
        "world_mutation_application_record": application_record,
        "world_mutation_application_record_digest": application_record_digest,
        "world_candidate_commit_authorization_consumption_record": authorization_consumption,
        "world_candidate_commit_authorization_consumption_record_digest": (
            authorization_consumption_digest
        ),
        "world_mutation_record": mutation_record,
        "world_mutation_record_digest": mutation_record_digest,
        "persisted_world_candidate_envelope": persisted_candidate,
        "persisted_world_candidate_envelope_digest": persisted_candidate_digest,
        "world_postcondition_verification_handoff_envelope": verification_handoff,
        "world_postcondition_verification_handoff_envelope_digest": (
            verification_handoff_digest
        ),
    }

    receipt.update(
        {
            "source_world_candidate_commit_authorization_receipt_supplied": True,
            "source_world_candidate_commit_authorization_receipt_fully_revalidated": True,
            "source_world_candidate_commit_authorization_ready": True,
            "source_single_use_authorization_bound": True,
            "source_world_mutation_application_handoff_bound": True,
            "source_world_candidate_envelope_bound": True,
            "source_world_candidate_commit_authorization_record_bound": True,
            "source_world_candidate_commit_authorization_review_certificate_bound": True,
            "world_mutation_application_review_certificate_bound": True,
            "mutation_owner_identity_bound": True,
            "world_mutation_transaction_bound": True,
            "world_state_before_digest_bound": True,
            "world_state_after_digest_bound": True,
            "world_update_patch_bound": True,
            "world_update_precondition_bound": True,
            "world_update_postcondition_bound": True,
            "persistent_world_storage_target_bound": True,
            "postcondition_verification_policy_bound": True,
            "rollback_route_bound": True,
            "compensation_route_bound": True,
            "exactly_one_world_mutation_application_receipt_issued": True,
            "world_mutation_application_review_performed": True,
            "world_mutation_application_completed": ready,
            "exactly_one_world_patch_applied": ready,
            "world_mutation_transaction_atomic": ready,
            "world_candidate_commit_completed": ready,
            "single_use_world_candidate_commit_authorization_consumed": ready,
            "world_candidate_commit_authorization_consumption_replay_closed": ready,
            "world_candidate_commit_authorization_double_consumed": False,
            "world_mutation_application_review_certificate_replay_closed": True,
            "world_mutation_application_intake_nonce_consumed": True,
            "world_mutation_application_intake_nonce_replay_closed": True,
            "source_world_candidate_commit_authorization_receipt_replay_closed": ready,
            "world_mutation_transaction_replay_closed": ready,
            "world_mutation_application_intake_session_replay_fresh_before_intake": (
                session_fresh
            ),
            "world_mutation_application_review_replay_fresh_before_intake": (
                review_fresh
            ),
            "world_mutation_application_intake_nonce_replay_fresh_before_intake": (
                nonce_fresh
            ),
            "source_authorization_receipt_replay_fresh_before_application": (
                source_fresh
            ),
            "world_mutation_transaction_replay_fresh_before_application": (
                transaction_fresh
            ),
            "world_conditions_current": world_current,
            "world_mutation_application_review_duration_current": duration_current,
            "world_mutation_application_intake_delay_current": delay_current,
            "source_world_candidate_commit_authorization_expiry_current": (
                expiry_current
            ),
            "world_mutation_application_debt_open": not ready,
            "persistent_world_model_state_unchanged": not ready,
            "persistent_world_model_state_changed": ready,
            "persistent_world_state_changed_by_mutation_application": ready,
            "world_model_revision_incremented_exactly_once": ready,
            "world_postcondition_verification_intake_admitted": ready,
            "world_postcondition_verification_receipt_required": ready,
            "world_postcondition_verification_completed": False,
            "world_postcondition_verification_debt_open": ready,
            "world_fact_confirmed": False,
            "causal_attribution_confirmed": False,
            "dukkha_reduction_realized_confirmed": False,
            "host_operation_reexecuted": False,
            "observation_reperformed": False,
            "verification_reperformed": False,
            "world_disposition_reperformed": False,
            "world_commit_authorization_reperformed": False,
            "tool_invocation_performed": False,
            "external_side_effect_performed": False,
            "persistent_host_state_changed_by_world_mutation": False,
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
            "bounded_world_mutation_authority_consumed": ready,
            "general_world_mutation_authority_granted": False,
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
    return WORLDDukkhaPreservingSingleUseWorldMutationApplicationResult(
        STATUS_READY, [], receipt
    )
