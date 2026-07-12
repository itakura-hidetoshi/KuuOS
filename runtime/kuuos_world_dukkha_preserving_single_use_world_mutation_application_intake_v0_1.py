#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_world_dukkha_preserving_single_use_world_candidate_commit_authorization_intake_v0_1 import (
    RECEIPT_DIGEST_FIELD as SOURCE_DIGEST_FIELD,
    REVIEW_DIGEST_FIELD as SOURCE_AUTH_REVIEW_DIGEST_FIELD,
    canonical_digest,
)

STATUS_READY, STATUS_BLOCKED = "ready", "blocked"
RECEIPT_DIGEST_FIELD = "world_dukkha_preserving_single_use_world_mutation_application_intake_receipt_digest"
REVIEW_DIGEST_FIELD = "world_mutation_application_review_certificate_digest"
CONTEXT_DIGEST_FIELD = "world_mutation_application_intake_context_digest"
STATE_BEFORE = "world_candidate_commit_authorized_not_applied"
STATE_AFTER_READY = "world_candidate_mutation_applied_unverified"

DISPOSITION_READY = "world_mutation_application_ready"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_CONTEXT_REFRESH = "world_mutation_application_context_refresh_required"
DISPOSITION_REVIEW_REFRESH = "world_mutation_application_review_refresh_required"
DISPOSITION_AUTH_EXPIRED = "world_candidate_commit_authorization_expired"
DISPOSITION_AUTH_REVALIDATION = "world_candidate_commit_authorization_revalidation_required"
DISPOSITION_PATCH_REPAIR = "world_patch_repair_required"
DISPOSITION_PRECONDITION_REPAIR = "world_precondition_repair_required"
DISPOSITION_ENGINE_REJECTED = "world_mutation_engine_rejected"
DISPOSITION_ATOMICITY_REPAIR = "world_mutation_atomicity_repair_required"
DISPOSITION_POSTCONDITION_OBSERVATION = "world_postcondition_observation_required"
DISPOSITION_PROVENANCE_REPAIR = "provenance_repair_required"
DISPOSITION_NONEXTERNALIZATION_REVIEW = "nonexternalization_review_required"
DISPOSITION_DUKKHA_REVIEW = "dukkha_preservation_review_required"
DISPOSITION_COMPENSATION_REPAIR = "compensation_route_repair_required"
DISPOSITION_TRUTH_PROMOTION_REJECTED = "truth_promotion_rejected"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"

REVIEW_FIELDS = {
    "source_world_commit_authorization_receipt_digest",
    "world_candidate_commit_authorization_record_digest",
    "world_mutation_application_handoff_envelope_digest",
    SOURCE_AUTH_REVIEW_DIGEST_FIELD,
    "world_candidate_envelope_digest",
    "world_candidate_fact_digest",
    "world_candidate_relation_digest",
    "world_update_patch_digest",
    "world_update_precondition_digest",
    "world_update_postcondition_digest",
    "authorization_scope_digest",
    "authorization_constraints_digest",
    "authorization_owner_id",
    "authorization_expiry_epoch",
    "world_mutation_application_policy_digest",
    "rollback_route_digest",
    "compensation_route_digest",
    "mutation_engine_id",
    "mutation_target_world_binding_digest",
    "mutation_expected_pre_state_digest",
    "mutation_expected_post_state_digest",
    "mutation_transaction_id",
    "application_review_started_epoch",
    "application_review_completed_epoch",
    "maximum_application_review_duration",
    "source_authorization_valid",
    "candidate_identity_match",
    "patch_identity_match",
    "authorization_scope_match",
    "authorization_constraints_satisfied",
    "authorization_owner_confirmed",
    "world_preconditions_satisfied",
    "mutation_engine_admitted",
    "atomic_application_supported",
    "postcondition_observation_route_ready",
    "lineage_continuity_preserved",
    "responsibility_continuity_preserved",
    "dukkha_preservation_supported",
    "protected_group_nonexternalization_supported",
    "future_nonexternalization_supported",
    "compensation_route_ready",
    "world_fact_claimed",
    "causal_attribution_claimed",
    "realized_dukkha_reduction_claimed",
    REVIEW_DIGEST_FIELD,
}

CONTEXT_FIELDS = {
    "source_world_commit_authorization_receipt_digest",
    REVIEW_DIGEST_FIELD,
    "current_world_binding_digest",
    "current_world_model_state_digest",
    "current_world_model_revision",
    "current_world_lineage_digest",
    "source_authorization_issued_epoch",
    "world_mutation_application_intake_epoch",
    "maximum_world_mutation_application_intake_delay",
    "world_mutation_application_intake_session_id",
    "world_mutation_application_intake_nonce_digest",
    "prior_world_mutation_application_intake_session_ids",
    "prior_world_mutation_application_review_certificate_digests",
    "prior_world_mutation_application_intake_nonce_digests",
    "prior_applied_world_commit_authorization_receipt_digests",
    "requested_world_mutation_application_operation_digest",
    "exact_world_mutation_application_cycle_digest",
    CONTEXT_DIGEST_FIELD,
}

@dataclass
class WORLDMutationApplicationResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def _map(value: Any) -> dict:
    return dict(value) if isinstance(value, Mapping) else {}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    item = dict(value)
    item.pop(field, None)
    return canonical_digest(item)


def compute_world_mutation_application_review_certificate_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, REVIEW_DIGEST_FIELD)


def compute_world_mutation_application_intake_context_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, CONTEXT_DIGEST_FIELD)


def compute_world_mutation_application_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def compute_requested_world_mutation_application_operation_digest(source: Mapping[str, Any], review: Mapping[str, Any]) -> str:
    return canonical_digest({
        "source_world_commit_authorization_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        "world_mutation_application_handoff_envelope_digest": source.get("world_mutation_application_handoff_envelope_digest"),
        REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        "world_update_patch_digest": review.get("world_update_patch_digest"),
        "mutation_transaction_id": review.get("mutation_transaction_id"),
        "state_before": STATE_BEFORE,
        "ready_state_after": STATE_AFTER_READY,
    })


def compute_exact_world_mutation_application_cycle_digest(source: Mapping[str, Any], review: Mapping[str, Any], context: Mapping[str, Any]) -> str:
    return canonical_digest({
        "source_world_commit_authorization_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        REVIEW_DIGEST_FIELD: review.get(REVIEW_DIGEST_FIELD),
        "world_mutation_application_intake_session_id": context.get("world_mutation_application_intake_session_id"),
        "world_mutation_application_intake_nonce_digest": context.get("world_mutation_application_intake_nonce_digest"),
        "world_mutation_application_intake_epoch": context.get("world_mutation_application_intake_epoch"),
        "current_world_model_revision": context.get("current_world_model_revision"),
        "requested_world_mutation_application_operation_digest": context.get("requested_world_mutation_application_operation_digest"),
    })


def _strings(value: Any, allow_empty: bool = False) -> tuple[bool, list[str]]:
    ok = isinstance(value, list) and (allow_empty or bool(value)) and all(isinstance(x, str) and x for x in value)
    items = list(value) if isinstance(value, list) else []
    return ok and items == sorted(items) and len(items) == len(set(items)), items


def _verify_source(source: dict, expected: str, blockers: list[str]) -> tuple[str, dict, list[str], list[str]]:
    if not source:
        blockers.append("source_world_commit_authorization_receipt_missing")
        return "", {}, [], []
    digest = source.get(SOURCE_DIGEST_FIELD, "")
    if not digest or digest != _digest_without(source, SOURCE_DIGEST_FIELD):
        blockers.append("source_world_commit_authorization_receipt_digest_mismatch")
    if digest != expected:
        blockers.append("source_world_commit_authorization_expected_binding_mismatch")
    expected_fields = {
        "world_version": "v0.61",
        "world_candidate_commit_authorization_disposition": "world_candidate_commit_authorization_ready",
        "world_candidate_commit_authorization_state_after": STATE_BEFORE,
        "world_candidate_commit_authorization_granted": True,
        "single_use_world_candidate_commit_authorization_granted": True,
        "world_candidate_commit_authorization_debt_consumed": True,
        "world_mutation_application_intake_admitted": True,
        "world_mutation_application_completed": False,
        "world_candidate_commit_completed": False,
        "persistent_world_model_state_unchanged": True,
        "world_fact_confirmed": False,
        "causal_attribution_confirmed": False,
        "dukkha_reduction_realized_confirmed": False,
        "world_mutation_authority_granted": False,
    }
    for key, value in expected_fields.items():
        if source.get(key) != value:
            blockers.append(f"source_boundary_{key}_mismatch")
    handoff = _map(source.get("world_mutation_application_handoff_envelope"))
    if not handoff or source.get("world_mutation_application_handoff_envelope_digest") != canonical_digest(handoff):
        blockers.append("source_world_mutation_application_handoff_invalid")
    required = {
        "authorization_state": "authorized_single_use_not_applied",
        "candidate_commit_state": "authorized_not_applied",
        "world_fact_state": "candidate_only_not_fact",
        "causal_attribution_state": "not_confirmed",
        "dukkha_realization_state": "not_confirmed",
        "world_mutation_application_intake_admitted": True,
        "world_mutation_application_receipt_required": True,
        "single_use_authorization": True,
        "compensation_route_ready": True,
    }
    for key, value in required.items():
        if handoff.get(key) != value:
            blockers.append(f"source_handoff_{key}_mismatch")
    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(source.get("resulting_responsibility_lineage_digests"))
    if not lineage_ok:
        blockers.append("source_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_resulting_responsibility_invalid")
    return digest, handoff, lineage, responsibility


def _verify_review(review: dict, expected: str, source: dict, handoff: dict, blockers: list[str]) -> tuple[str, bool]:
    if not review:
        blockers.append("world_mutation_application_review_certificate_missing")
        return "", False
    if set(review) != REVIEW_FIELDS:
        blockers.append("world_mutation_application_review_certificate_schema_invalid")
    digest = review.get(REVIEW_DIGEST_FIELD, "")
    if not digest or digest != compute_world_mutation_application_review_certificate_digest(review):
        blockers.append("world_mutation_application_review_certificate_digest_mismatch")
    if digest != expected:
        blockers.append("world_mutation_application_review_expected_binding_mismatch")
    bindings = {
        "source_world_commit_authorization_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        "world_candidate_commit_authorization_record_digest": source.get("world_candidate_commit_authorization_record_digest"),
        "world_mutation_application_handoff_envelope_digest": source.get("world_mutation_application_handoff_envelope_digest"),
        SOURCE_AUTH_REVIEW_DIGEST_FIELD: source.get(SOURCE_AUTH_REVIEW_DIGEST_FIELD),
        "world_candidate_envelope_digest": source.get("source_world_candidate_envelope_digest"),
    }
    for key, value in bindings.items():
        if review.get(key) != value:
            blockers.append(f"world_mutation_application_review_{key}_mismatch")
    for key in (
        "world_candidate_fact_digest", "world_candidate_relation_digest", "world_update_patch_digest",
        "world_update_precondition_digest", "world_update_postcondition_digest", "authorization_scope_digest",
        "authorization_constraints_digest", "authorization_owner_id", "world_mutation_application_policy_digest",
        "rollback_route_digest", "compensation_route_digest",
    ):
        if review.get(key) != handoff.get(key):
            blockers.append(f"world_mutation_application_review_{key}_mismatch")
    for key in ("mutation_engine_id", "mutation_target_world_binding_digest", "mutation_expected_pre_state_digest", "mutation_expected_post_state_digest", "mutation_transaction_id"):
        if not isinstance(review.get(key), str) or not review.get(key):
            blockers.append(f"world_mutation_application_review_{key}_invalid")
    bool_fields = REVIEW_FIELDS - {REVIEW_DIGEST_FIELD} - {
        "source_world_commit_authorization_receipt_digest", "world_candidate_commit_authorization_record_digest",
        "world_mutation_application_handoff_envelope_digest", SOURCE_AUTH_REVIEW_DIGEST_FIELD,
        "world_candidate_envelope_digest", "world_candidate_fact_digest", "world_candidate_relation_digest",
        "world_update_patch_digest", "world_update_precondition_digest", "world_update_postcondition_digest",
        "authorization_scope_digest", "authorization_constraints_digest", "authorization_owner_id",
        "world_mutation_application_policy_digest", "rollback_route_digest", "compensation_route_digest",
        "mutation_engine_id", "mutation_target_world_binding_digest", "mutation_expected_pre_state_digest",
        "mutation_expected_post_state_digest", "mutation_transaction_id", "authorization_expiry_epoch",
        "application_review_started_epoch", "application_review_completed_epoch", "maximum_application_review_duration",
    }
    for key in bool_fields:
        if not isinstance(review.get(key), bool):
            blockers.append(f"world_mutation_application_review_{key}_invalid")
    start, end, maximum = review.get("application_review_started_epoch"), review.get("application_review_completed_epoch"), review.get("maximum_application_review_duration")
    duration = all(isinstance(x, int) and not isinstance(x, bool) and x >= 0 for x in (start, end, maximum)) and 1 <= maximum <= 64 and 0 <= end - start <= maximum
    if not duration:
        blockers.append("world_mutation_application_review_duration_invalid")
    return digest, duration


def _verify_context(context: dict, expected: str, source: dict, review: dict, blockers: list[str]) -> tuple[str, tuple[bool, ...]]:
    if not context:
        blockers.append("world_mutation_application_intake_context_missing")
        return "", (False,) * 7
    if set(context) != CONTEXT_FIELDS:
        blockers.append("world_mutation_application_intake_context_schema_invalid")
    digest = context.get(CONTEXT_DIGEST_FIELD, "")
    if not digest or digest != compute_world_mutation_application_intake_context_digest(context):
        blockers.append("world_mutation_application_intake_context_digest_mismatch")
    if digest != expected:
        blockers.append("world_mutation_application_context_expected_binding_mismatch")
    if context.get("source_world_commit_authorization_receipt_digest") != source.get(SOURCE_DIGEST_FIELD) or context.get(REVIEW_DIGEST_FIELD) != review.get(REVIEW_DIGEST_FIELD):
        blockers.append("world_mutation_application_context_source_binding_mismatch")
    world_current = all(context.get(k) == source.get(s) for k, s in (
        ("current_world_binding_digest", "source_world_binding_digest"),
        ("current_world_model_state_digest", "source_world_model_state_digest"),
        ("current_world_model_revision", "source_world_model_revision"),
        ("current_world_lineage_digest", "source_world_lineage_digest"),
    ))
    issued, epoch, maximum = context.get("source_authorization_issued_epoch"), context.get("world_mutation_application_intake_epoch"), context.get("maximum_world_mutation_application_intake_delay")
    delay_current = all(isinstance(x, int) and not isinstance(x, bool) for x in (issued, epoch, maximum)) and 1 <= maximum <= 64 and 0 <= epoch - issued <= maximum
    expiry_current = isinstance(review.get("authorization_expiry_epoch"), int) and epoch <= review.get("authorization_expiry_epoch")
    if context.get("requested_world_mutation_application_operation_digest") != compute_requested_world_mutation_application_operation_digest(source, review):
        blockers.append("world_mutation_application_context_operation_digest_mismatch")
    if context.get("exact_world_mutation_application_cycle_digest") != compute_exact_world_mutation_application_cycle_digest(source, review, context):
        blockers.append("world_mutation_application_context_cycle_digest_mismatch")
    lists = []
    for field in (
        "prior_world_mutation_application_intake_session_ids", "prior_world_mutation_application_review_certificate_digests",
        "prior_world_mutation_application_intake_nonce_digests", "prior_applied_world_commit_authorization_receipt_digests",
    ):
        ok, items = _strings(context.get(field), True)
        if not ok:
            blockers.append(f"world_mutation_application_context_{field}_invalid")
        lists.append(items)
    sessions, reviews, nonces, sources = lists
    return digest, (
        world_current, delay_current, expiry_current,
        context.get("world_mutation_application_intake_session_id") not in sessions,
        review.get(REVIEW_DIGEST_FIELD) not in reviews,
        context.get("world_mutation_application_intake_nonce_digest") not in nonces,
        source.get(SOURCE_DIGEST_FIELD) not in sources,
    )


def _route(review: Mapping[str, Any], duration: bool, checks: tuple[bool, ...]) -> str:
    world, delay, expiry, session, review_fresh, nonce, source_fresh = checks
    if not all((session, review_fresh, nonce, source_fresh)):
        return DISPOSITION_REPLAY_REJECTED
    if not world:
        return DISPOSITION_WORLD_REFRESH
    if not delay:
        return DISPOSITION_CONTEXT_REFRESH
    if not duration:
        return DISPOSITION_REVIEW_REFRESH
    if not expiry:
        return DISPOSITION_AUTH_EXPIRED
    if any(review.get(k) for k in ("world_fact_claimed", "causal_attribution_claimed", "realized_dukkha_reduction_claimed")):
        return DISPOSITION_TRUTH_PROMOTION_REJECTED
    if not review.get("source_authorization_valid") or not review.get("authorization_owner_confirmed") or not review.get("authorization_scope_match") or not review.get("authorization_constraints_satisfied"):
        return DISPOSITION_AUTH_REVALIDATION
    if not review.get("candidate_identity_match") or not review.get("patch_identity_match"):
        return DISPOSITION_PATCH_REPAIR
    if not review.get("world_preconditions_satisfied"):
        return DISPOSITION_PRECONDITION_REPAIR
    if not review.get("mutation_engine_admitted"):
        return DISPOSITION_ENGINE_REJECTED
    if not review.get("atomic_application_supported"):
        return DISPOSITION_ATOMICITY_REPAIR
    if not review.get("postcondition_observation_route_ready"):
        return DISPOSITION_POSTCONDITION_OBSERVATION
    if not review.get("lineage_continuity_preserved") or not review.get("responsibility_continuity_preserved"):
        return DISPOSITION_PROVENANCE_REPAIR
    if not review.get("protected_group_nonexternalization_supported") or not review.get("future_nonexternalization_supported"):
        return DISPOSITION_NONEXTERNALIZATION_REVIEW
    if not review.get("dukkha_preservation_supported"):
        return DISPOSITION_DUKKHA_REVIEW
    if not review.get("compensation_route_ready"):
        return DISPOSITION_COMPENSATION_REPAIR
    return DISPOSITION_READY


def build_world_dukkha_preserving_single_use_world_mutation_application_intake(*, source_world_commit_authorization_receipt: Mapping[str, Any], expected_source_world_commit_authorization_receipt_digest: str, world_mutation_application_review_certificate: Mapping[str, Any], expected_world_mutation_application_review_certificate_digest: str, world_mutation_application_intake_context: Mapping[str, Any], expected_world_mutation_application_intake_context_digest: str, world_mutation_application_policy_digest: str, world_mutation_application_responsibility_digest: str, world_mutation_application_request_id: str, world_mutation_application_bundle_digest: str) -> WORLDMutationApplicationResult:
    blockers: list[str] = []
    source, review, context = _map(source_world_commit_authorization_receipt), _map(world_mutation_application_review_certificate), _map(world_mutation_application_intake_context)
    for name, value in {
        "expected_source_world_commit_authorization_receipt_digest": expected_source_world_commit_authorization_receipt_digest,
        "expected_world_mutation_application_review_certificate_digest": expected_world_mutation_application_review_certificate_digest,
        "expected_world_mutation_application_intake_context_digest": expected_world_mutation_application_intake_context_digest,
        "world_mutation_application_policy_digest": world_mutation_application_policy_digest,
        "world_mutation_application_responsibility_digest": world_mutation_application_responsibility_digest,
        "world_mutation_application_request_id": world_mutation_application_request_id,
        "world_mutation_application_bundle_digest": world_mutation_application_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")
    source_digest, handoff, lineage, responsibility = _verify_source(source, expected_source_world_commit_authorization_receipt_digest, blockers)
    review_digest, duration = _verify_review(review, expected_world_mutation_application_review_certificate_digest, source, handoff, blockers)
    context_digest, checks = _verify_context(context, expected_world_mutation_application_intake_context_digest, source, review, blockers)
    if not blockers:
        bundle = compute_world_mutation_application_bundle_digest(
            source_world_commit_authorization_receipt_digest=source_digest,
            expected_source_world_commit_authorization_receipt_digest=expected_source_world_commit_authorization_receipt_digest,
            world_candidate_commit_authorization_record_digest=source.get("world_candidate_commit_authorization_record_digest"),
            world_mutation_application_handoff_envelope_digest=source.get("world_mutation_application_handoff_envelope_digest"),
            world_mutation_application_review_certificate_digest=review_digest,
            expected_world_mutation_application_review_certificate_digest=expected_world_mutation_application_review_certificate_digest,
            world_mutation_application_intake_context_digest=context_digest,
            expected_world_mutation_application_intake_context_digest=expected_world_mutation_application_intake_context_digest,
            requested_world_mutation_application_operation_digest=context.get("requested_world_mutation_application_operation_digest"),
            exact_world_mutation_application_cycle_digest=context.get("exact_world_mutation_application_cycle_digest"),
            world_mutation_application_policy_digest=world_mutation_application_policy_digest,
            world_mutation_application_responsibility_digest=world_mutation_application_responsibility_digest,
            world_mutation_application_request_id=world_mutation_application_request_id,
        )
        if bundle != world_mutation_application_bundle_digest:
            blockers.append("world_mutation_application_bundle_digest_mismatch")
    if blockers:
        return WORLDMutationApplicationResult(STATUS_BLOCKED, sorted(set(blockers)), None)
    disposition = _route(review, duration, checks)
    ready = disposition == DISPOSITION_READY
    state_after = STATE_AFTER_READY if ready else STATE_BEFORE
    record = {
        "source_world_commit_authorization_receipt_digest": source_digest,
        "world_candidate_commit_authorization_record_digest": source["world_candidate_commit_authorization_record_digest"],
        "world_mutation_application_handoff_envelope_digest": source["world_mutation_application_handoff_envelope_digest"],
        REVIEW_DIGEST_FIELD: review_digest,
        "mutation_engine_id": review["mutation_engine_id"],
        "mutation_transaction_id": review["mutation_transaction_id"],
        "world_update_patch_digest": review["world_update_patch_digest"],
        "world_mutation_application_disposition": disposition,
        "state_before": STATE_BEFORE,
        "state_after": state_after,
        "application_outcome": "world_candidate_mutation_applied_unverified" if ready else "world_mutation_application_routed_without_application",
    }
    record_digest = canonical_digest(record)
    consumption = {
        "source_world_commit_authorization_receipt_digest": source_digest,
        "world_mutation_application_record_digest": record_digest,
        "single_use_authorization_consumed": ready,
        "source_authorization_marked_applied": ready,
        "double_world_mutation_application_performed": False,
    }
    consumption_digest = canonical_digest(consumption)
    mutation_receipt = None
    mutation_receipt_digest = ""
    verification_handoff = None
    verification_handoff_digest = ""
    if ready:
        mutation_receipt = {
            "source_world_commit_authorization_receipt_digest": source_digest,
            "world_candidate_envelope_digest": source["source_world_candidate_envelope_digest"],
            "world_mutation_application_record_digest": record_digest,
            "mutation_engine_id": review["mutation_engine_id"],
            "mutation_transaction_id": review["mutation_transaction_id"],
            "world_update_patch_digest": review["world_update_patch_digest"],
            "pre_state_digest": review["mutation_expected_pre_state_digest"],
            "post_state_digest": review["mutation_expected_post_state_digest"],
            "pre_world_model_revision": source["source_world_model_revision"],
            "post_world_model_revision": source["source_world_model_revision"] + 1,
            "application_state": "applied_atomically_unverified",
            "candidate_commit_state": "mutation_applied_postcondition_unverified",
            "world_fact_state": "not_promoted_pending_post_application_verification",
            "causal_attribution_state": "not_confirmed",
            "dukkha_realization_state": "not_confirmed",
            "single_use_authorization_consumed": True,
        }
        mutation_receipt_digest = canonical_digest(mutation_receipt)
        verification_handoff = {
            "world_mutation_application_receipt_digest": mutation_receipt_digest,
            "source_world_commit_authorization_receipt_digest": source_digest,
            "world_candidate_fact_digest": review["world_candidate_fact_digest"],
            "world_candidate_relation_digest": review["world_candidate_relation_digest"],
            "world_update_patch_digest": review["world_update_patch_digest"],
            "expected_post_state_digest": review["mutation_expected_post_state_digest"],
            "world_update_postcondition_digest": review["world_update_postcondition_digest"],
            "mutation_transaction_id": review["mutation_transaction_id"],
            "post_application_observation_required": True,
            "post_application_verification_required": True,
            "world_fact_promotion_not_authorized": True,
            "causal_attribution_not_authorized": True,
            "dukkha_realization_confirmation_not_authorized": True,
            "compensation_route_ready": True,
        }
        verification_handoff_digest = canonical_digest(verification_handoff)
    world_current, delay_current, expiry_current, session_fresh, review_fresh, nonce_fresh, source_fresh = checks
    resulting_lineage = sorted(set(lineage) | {source_digest, review_digest, context_digest, record_digest, consumption_digest, world_mutation_application_bundle_digest} | ({mutation_receipt_digest, verification_handoff_digest} if ready else set()))
    resulting_responsibility = sorted(set(responsibility) | {review["mutation_engine_id"], review["authorization_owner_id"], world_mutation_application_responsibility_digest})
    receipt = {
        "kernel": "WORLD Dukkha-Preserving Single-Use World Mutation Application Intake Kernel",
        "kernel_version": "v0.1",
        "world_version": "v0.62",
        "status": "WORLD_DUKKHA_PRESERVING_SINGLE_USE_WORLD_MUTATION_APPLICATION_ROUTED",
        "source_world_commit_authorization_receipt_digest": source_digest,
        "source_world_candidate_envelope_digest": source["source_world_candidate_envelope_digest"],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source["source_world_model_state_digest"],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "world_mutation_application_review_certificate": review,
        REVIEW_DIGEST_FIELD: review_digest,
        CONTEXT_DIGEST_FIELD: context_digest,
        "world_mutation_application_policy_digest": world_mutation_application_policy_digest,
        "world_mutation_application_responsibility_digest": world_mutation_application_responsibility_digest,
        "world_mutation_application_request_id": world_mutation_application_request_id,
        "world_mutation_application_bundle_digest": world_mutation_application_bundle_digest,
        "world_mutation_application_disposition": disposition,
        "world_mutation_application_state_before": STATE_BEFORE,
        "world_mutation_application_state_after": state_after,
        "world_mutation_application_record": record,
        "world_mutation_application_record_digest": record_digest,
        "world_mutation_authorization_consumption_record": consumption,
        "world_mutation_authorization_consumption_record_digest": consumption_digest,
        "world_mutation_application_receipt": mutation_receipt,
        "world_mutation_application_receipt_digest": mutation_receipt_digest,
        "post_application_verification_handoff_envelope": verification_handoff,
        "post_application_verification_handoff_envelope_digest": verification_handoff_digest,
        "source_world_commit_authorization_receipt_fully_revalidated": True,
        "source_single_use_authorization_valid": True,
        "world_mutation_application_review_certificate_bound": True,
        "mutation_engine_identity_bound": True,
        "mutation_transaction_bound": True,
        "world_patch_bound": True,
        "world_precondition_bound": True,
        "world_postcondition_bound": True,
        "exactly_one_world_mutation_application_intake_receipt_issued": True,
        "world_mutation_application_performed": ready,
        "world_mutation_applied_atomically": ready,
        "single_use_authorization_consumed": ready,
        "single_use_authorization_replay_closed": ready,
        "world_mutation_application_double_consumed": False,
        "source_authorization_replay_closed": ready,
        "world_mutation_application_debt_open": not ready,
        "world_conditions_current": world_current,
        "world_mutation_application_review_duration_current": duration,
        "world_mutation_application_intake_delay_current": delay_current,
        "world_candidate_commit_authorization_expiry_current": expiry_current,
        "world_mutation_application_intake_session_replay_fresh_before_intake": session_fresh,
        "world_mutation_application_review_replay_fresh_before_intake": review_fresh,
        "world_mutation_application_nonce_replay_fresh_before_intake": nonce_fresh,
        "source_authorization_replay_fresh_before_application": source_fresh,
        "world_candidate_commit_completed": ready,
        "persistent_world_model_state_changed": ready,
        "world_model_revision_incremented_once": ready,
        "post_application_observation_intake_admitted": ready,
        "post_application_verification_receipt_required": ready,
        "post_application_verification_completed": False,
        "world_fact_confirmed": False,
        "causal_attribution_confirmed": False,
        "dukkha_reduction_realized_confirmed": False,
        "automatic_truth_promotion": False,
        "automatic_causal_attribution": False,
        "automatic_dukkha_realization_confirmation": False,
        "host_operation_reexecuted": False,
        "observation_reperformed": False,
        "verification_reperformed": False,
        "world_disposition_reperformed": False,
        "authorization_reperformed": False,
        "tool_invocation_performed": False,
        "external_side_effect_outside_bounded_world_mutation": False,
        "compensation_route_ready": True,
        "compensation_performed": False,
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
        "general_world_mutation_authority_granted": False,
        "world_model_prediction_not_truth": True,
        "history_read_only_except_authorized_append": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "resulting_lineage_digests": resulting_lineage,
        "resulting_responsibility_lineage_digests": resulting_responsibility,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return WORLDMutationApplicationResult(STATUS_READY, [], receipt)
