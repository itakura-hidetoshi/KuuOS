#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
SOURCE_DIGEST_FIELD = "actos_dukkha_preserving_adapter_binding_authorization_intake_receipt_digest"
RECEIPT_DIGEST_FIELD = "actos_dukkha_preserving_frontier_plan_activation_receipt_digest"
AUTHORIZATION_READY = "activation_authorization_ready"
STATE_BEFORE = "bound_not_invoked"
STATE_AFTER = "activated_not_invoked"

CONTEXT_FIELDS = {
    "source_authorization_receipt_digest", "activation_token_digest",
    "requested_frontier_candidate_id", "requested_frontier_binding_digest",
    "requested_frontier_adapter_id", "requested_frontier_lease_id",
    "activation_session_id", "activation_intent_digest",
    "authorization_nonce_digest", "current_world_binding_digest",
    "current_world_model_state_digest", "current_world_model_revision",
    "current_world_lineage_digest", "authorization_receipt_observed_epoch",
    "activation_epoch", "maximum_activation_delay",
    "prior_consumed_authorization_token_digests",
    "prior_activated_frontier_candidate_ids",
    "requested_state_transition_digest", "exact_activation_cycle_digest",
    "activation_context_digest",
}

SOURCE_TRUE = (
    "activation_authorization_admitted", "activation_authorization_receipt_issued",
    "single_use_authorization_reserved", "adapter_registry_snapshot_unchanged",
    "world_conditions_current", "freshness_current", "adapter_registry_ready",
    "frontier_lease_available", "session_intent_nonce_replay_fresh",
    "irreversible_step_reverification_satisfied", "adapter_binding_performed",
    "all_materialization_candidates_bound", "one_to_one_candidate_binding_preserved",
    "activation_frontier_sequence_preserved", "scope_and_effect_ceiling_exact",
    "checkpoint_guards_preserved", "stop_conditions_preserved",
    "evidence_lineage_preserved", "alternative_candidates_preserved",
    "dissent_preserved", "minority_preserved", "dukkha_reduction_support_preserved",
    "protected_group_nonexternalization_preserved", "future_nonexternalization_preserved",
    "revision_capacity_preserved", "persistent_loop_reduction_preserved",
    "single_scalar_utility_not_introduced", "selection_remains_decisionos_owned",
    "persistent_world_state_unchanged", "world_model_prediction_not_truth",
    "world_mutation_not_granted", "history_read_only", "qi_grants_no_authority",
    "future_only",
)
SOURCE_FALSE = (
    "lease_use_consumed", "selection_authority_granted_to_actos",
    "plan_revision_authority_granted_to_actos",
    "dukkha_minimization_authority_granted_to_actos", "plan_activated",
    "adapter_invocation_performed", "tool_invocation_performed",
    "external_side_effect_performed", "execution_authority_granted",
    "execution_permission", "active_now",
)


@dataclass
class ActOSDukkhaPreservingFrontierActivationResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def canonical_digest(value: Any) -> str:
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":")).encode()).hexdigest()


def compute_activation_context_digest(context: Mapping[str, Any]) -> str:
    value = dict(context)
    value.pop("activation_context_digest", None)
    return canonical_digest(value)


def compute_requested_state_transition_digest(source: Mapping[str, Any]) -> str:
    return canonical_digest({
        "frontier_materialization_candidate_id": source.get("activation_frontier_candidate_id"),
        "frontier_adapter_id": source.get("frontier_adapter_id"),
        "frontier_lease_id": source.get("frontier_lease_id"),
        "state_before": STATE_BEFORE, "state_after": STATE_AFTER,
    })


def compute_exact_activation_cycle_digest(
    source: Mapping[str, Any], context: Mapping[str, Any]
) -> str:
    record = source.get("authorization_record")
    record = record if isinstance(record, Mapping) else {}
    return canonical_digest({
        "source_authorization_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        "source_authorization_record_digest": source.get("authorization_record_digest"),
        "activation_token_digest": source.get("activation_authorization_token_digest"),
        "frontier_materialization_candidate_id": source.get("activation_frontier_candidate_id"),
        "frontier_binding_digest": record.get("frontier_binding_digest"),
        "frontier_adapter_id": source.get("frontier_adapter_id"),
        "frontier_lease_id": source.get("frontier_lease_id"),
        "activation_session_id": context.get("activation_session_id"),
        "activation_intent_digest": context.get("activation_intent_digest"),
        "authorization_nonce_digest": context.get("authorization_nonce_digest"),
        "activation_epoch": context.get("activation_epoch"),
        "current_world_model_revision": context.get("current_world_model_revision"),
        "requested_state_transition_digest": context.get("requested_state_transition_digest"),
    })


def compute_frontier_activation_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def _strings(value: Any, empty: bool = False) -> tuple[bool, list[str]]:
    if not isinstance(value, list) or (not empty and not value):
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    if value != sorted(value) or len(value) != len(set(value)):
        return False, []
    return True, list(value)


def _verify_source(source: dict, expected: str, blockers: list[str]):
    if not source:
        blockers.append("source_authorization_receipt_missing")
        return "", {}, {}, [], []
    headers = {
        "kernel": "ActOS Dukkha-Preserving Adapter Binding and Activation Authorization Intake Kernel",
        "kernel_version": "v0.1", "actos_version": "v0.6",
        "status": "ACTOS_DUKKHA_PRESERVING_ADAPTER_BINDING_AUTHORIZATION_ROUTED",
        "authorization_disposition": AUTHORIZATION_READY,
    }
    for field, value in headers.items():
        if source.get(field) != value:
            blockers.append(f"source_{field}_invalid")
    digest = source.get(SOURCE_DIGEST_FIELD)
    if not isinstance(digest, str) or not digest:
        blockers.append("source_authorization_receipt_digest_missing")
        digest = ""
    else:
        unsigned = dict(source); unsigned.pop(SOURCE_DIGEST_FIELD, None)
        if digest != canonical_digest(unsigned):
            blockers.append("source_authorization_receipt_digest_mismatch")
        if digest != expected:
            blockers.append("source_authorization_receipt_expected_binding_mismatch")
    for field in SOURCE_TRUE:
        if source.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in SOURCE_FALSE:
        if source.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")

    raw_record = source.get("authorization_record")
    record = dict(raw_record) if isinstance(raw_record, Mapping) else {}
    if not record:
        blockers.append("source_authorization_record_invalid")
    if source.get("authorization_record_digest") != canonical_digest(record):
        blockers.append("source_authorization_record_digest_mismatch")
    token = source.get("activation_authorization_token_digest")
    if not isinstance(token, str) or not token:
        blockers.append("source_activation_authorization_token_missing")
    elif token != canonical_digest({**record,
            "authorization_policy_digest": source.get("authorization_policy_digest"),
            "authorization_request_id": source.get("authorization_request_id")}):
        blockers.append("source_activation_authorization_token_mismatch")

    record_expect = {
        "frontier_materialization_candidate_id": source.get("activation_frontier_candidate_id"),
        "frontier_adapter_id": source.get("frontier_adapter_id"),
        "frontier_lease_id": source.get("frontier_lease_id"),
        "authorization_disposition": AUTHORIZATION_READY,
        "activation_authorization_admitted": True,
        "remaining_uses_before_reservation": source.get("remaining_uses_before_reservation"),
        "remaining_uses_after_reservation": source.get("remaining_uses_after_reservation"),
    }
    for field, value in record_expect.items():
        if record.get(field) != value:
            blockers.append(f"source_authorization_record_{field}_mismatch")
    before, after = source.get("remaining_uses_before_reservation"), source.get("remaining_uses_after_reservation")
    if not (isinstance(before, int) and not isinstance(before, bool)
            and isinstance(after, int) and not isinstance(after, bool)
            and after >= 0 and after + 1 == before):
        blockers.append("source_single_use_reservation_arithmetic_invalid")

    raw_bindings = source.get("adapter_bindings")
    bindings = [dict(item) for item in raw_bindings] if (
        isinstance(raw_bindings, list) and raw_bindings
        and all(isinstance(item, Mapping) for item in raw_bindings)) else []
    if not bindings:
        blockers.append("source_adapter_bindings_invalid")
    if source.get("adapter_binding_count") != len(bindings):
        blockers.append("source_adapter_binding_count_mismatch")
    if source.get("adapter_binding_set_digest") != canonical_digest(bindings):
        blockers.append("source_adapter_binding_set_digest_mismatch")
    frontier_matches = [item for item in bindings if item.get("materialization_candidate_id")
                        == source.get("activation_frontier_candidate_id")]
    frontier = frontier_matches[0] if len(frontier_matches) == 1 else {}
    if not frontier:
        blockers.append("source_frontier_binding_not_unique")
    else:
        unsigned = dict(frontier); binding_digest = unsigned.pop("binding_digest", None)
        if binding_digest != canonical_digest(unsigned):
            blockers.append("source_frontier_binding_digest_mismatch")
        if frontier.get("binding_state") != STATE_BEFORE:
            blockers.append("source_frontier_binding_state_invalid")
        if record.get("frontier_binding_digest") != binding_digest:
            blockers.append("source_authorization_record_binding_mismatch")
        if frontier.get("adapter_id") != source.get("frontier_adapter_id"):
            blockers.append("source_frontier_adapter_mismatch")
        if frontier.get("lease_id") != source.get("frontier_lease_id"):
            blockers.append("source_frontier_lease_mismatch")
    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(source.get("resulting_responsibility_lineage_digests"))
    if not lineage_ok: blockers.append("source_resulting_lineage_invalid")
    if not responsibility_ok: blockers.append("source_resulting_responsibility_invalid")
    return digest, record, frontier, lineage, responsibility


def _verify_context(context: dict, expected: str, source: dict,
                    record: dict, frontier: dict, blockers: list[str]):
    if not context:
        blockers.append("activation_context_missing")
        return "", False, False, False, False
    if set(context) != CONTEXT_FIELDS:
        blockers.append("activation_context_schema_invalid")
    digest = context.get("activation_context_digest")
    if not isinstance(digest, str) or not digest:
        blockers.append("activation_context_digest_missing"); digest = ""
    else:
        if digest != compute_activation_context_digest(context):
            blockers.append("activation_context_digest_mismatch")
        if digest != expected:
            blockers.append("activation_context_expected_binding_mismatch")
    string_fields = CONTEXT_FIELDS - {
        "current_world_model_revision", "authorization_receipt_observed_epoch",
        "activation_epoch", "maximum_activation_delay",
        "prior_consumed_authorization_token_digests",
        "prior_activated_frontier_candidate_ids", "activation_context_digest",
    }
    for field in string_fields:
        if not isinstance(context.get(field), str) or not context.get(field):
            blockers.append(f"activation_context_{field}_invalid")
    for field in ("current_world_model_revision", "authorization_receipt_observed_epoch",
                  "activation_epoch", "maximum_activation_delay"):
        value = context.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"activation_context_{field}_invalid")
    bound = context.get("maximum_activation_delay")
    if not isinstance(bound, int) or isinstance(bound, bool) or not 1 <= bound <= 64:
        blockers.append("activation_context_delay_bound_invalid")
    consumed_ok, consumed = _strings(context.get("prior_consumed_authorization_token_digests"), True)
    activated_ok, activated = _strings(context.get("prior_activated_frontier_candidate_ids"), True)
    if not consumed_ok: blockers.append("activation_context_consumed_tokens_invalid")
    if not activated_ok: blockers.append("activation_context_activated_frontiers_invalid")
    exact = {
        "source_authorization_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        "activation_token_digest": source.get("activation_authorization_token_digest"),
        "requested_frontier_candidate_id": source.get("activation_frontier_candidate_id"),
        "requested_frontier_binding_digest": frontier.get("binding_digest"),
        "requested_frontier_adapter_id": source.get("frontier_adapter_id"),
        "requested_frontier_lease_id": source.get("frontier_lease_id"),
        "activation_session_id": record.get("session_id"),
        "activation_intent_digest": record.get("intent_digest"),
        "authorization_nonce_digest": record.get("authorization_nonce_digest"),
        "current_world_binding_digest": source.get("source_world_binding_digest"),
        "current_world_model_state_digest": source.get("source_world_model_state_digest"),
        "current_world_model_revision": source.get("source_world_model_revision"),
        "current_world_lineage_digest": source.get("source_world_lineage_digest"),
    }
    for field, value in exact.items():
        if context.get(field) != value:
            blockers.append(f"activation_context_{field}_mismatch")
    if context.get("requested_state_transition_digest") != compute_requested_state_transition_digest(source):
        blockers.append("activation_context_state_transition_digest_mismatch")
    if context.get("exact_activation_cycle_digest") != compute_exact_activation_cycle_digest(source, context):
        blockers.append("activation_context_exact_cycle_digest_mismatch")
    observed, epoch, delay = (context.get("authorization_receipt_observed_epoch"),
        context.get("activation_epoch"), context.get("maximum_activation_delay"))
    delay_current = all(isinstance(v, int) and not isinstance(v, bool)
                        for v in (observed, epoch, delay)) and 0 <= epoch - observed <= delay
    token_fresh = source.get("activation_authorization_token_digest") not in consumed
    frontier_fresh = source.get("activation_frontier_candidate_id") not in activated
    world_current = all(context.get(field) == value for field, value in exact.items()
                        if field.startswith("current_world_"))
    return digest, world_current, delay_current, token_fresh, frontier_fresh


def build_actos_dukkha_preserving_frontier_plan_activation_receipt(
    *, source_authorization_receipt: Mapping[str, Any],
    expected_source_authorization_receipt_digest: str,
    activation_context: Mapping[str, Any], expected_activation_context_digest: str,
    activation_policy_digest: str, actos_activation_responsibility_digest: str,
    activation_request_id: str, activation_bundle_digest: str,
) -> ActOSDukkhaPreservingFrontierActivationResult:
    blockers: list[str] = []
    source = dict(source_authorization_receipt) if isinstance(source_authorization_receipt, Mapping) else {}
    context = dict(activation_context) if isinstance(activation_context, Mapping) else {}
    for name, value in {
        "expected_source_authorization_receipt_digest": expected_source_authorization_receipt_digest,
        "expected_activation_context_digest": expected_activation_context_digest,
        "activation_policy_digest": activation_policy_digest,
        "actos_activation_responsibility_digest": actos_activation_responsibility_digest,
        "activation_request_id": activation_request_id,
        "activation_bundle_digest": activation_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value: blockers.append(f"{name}_missing")
    source_digest, record, frontier, lineage, responsibility = _verify_source(
        source, expected_source_authorization_receipt_digest, blockers)
    context_digest, world_current, delay_current, token_fresh, frontier_fresh = _verify_context(
        context, expected_activation_context_digest, source, record, frontier, blockers)
    if not world_current: blockers.append("activation_world_refresh_required")
    if not delay_current: blockers.append("activation_authorization_expired")
    if not token_fresh: blockers.append("activation_authorization_token_replay_rejected")
    if not frontier_fresh: blockers.append("activation_frontier_replay_rejected")
    if not blockers:
        expected_bundle = compute_frontier_activation_bundle_digest(
            source_authorization_receipt_digest=source_digest,
            expected_source_authorization_receipt_digest=expected_source_authorization_receipt_digest,
            activation_authorization_token_digest=source["activation_authorization_token_digest"],
            authorization_record_digest=source["authorization_record_digest"],
            activation_context_digest=context_digest,
            expected_activation_context_digest=expected_activation_context_digest,
            requested_state_transition_digest=context["requested_state_transition_digest"],
            exact_activation_cycle_digest=context["exact_activation_cycle_digest"],
            activation_policy_digest=activation_policy_digest,
            actos_activation_responsibility_digest=actos_activation_responsibility_digest,
            activation_request_id=activation_request_id)
        if activation_bundle_digest != expected_bundle:
            blockers.append("activation_bundle_digest_mismatch")
    if blockers:
        return ActOSDukkhaPreservingFrontierActivationResult(STATUS_BLOCKED, sorted(set(blockers)), None)

    activation_record = {
        "frontier_materialization_candidate_id": source["activation_frontier_candidate_id"],
        "frontier_adapter_id": source["frontier_adapter_id"],
        "frontier_binding_digest": frontier["binding_digest"],
        "frontier_lease_id": source["frontier_lease_id"],
        "activation_authorization_token_digest": source["activation_authorization_token_digest"],
        "source_authorization_record_digest": source["authorization_record_digest"],
        "activation_session_id": context["activation_session_id"],
        "activation_intent_digest": context["activation_intent_digest"],
        "authorization_nonce_digest": context["authorization_nonce_digest"],
        "requested_state_transition_digest": context["requested_state_transition_digest"],
        "exact_activation_cycle_digest": context["exact_activation_cycle_digest"],
        "activation_epoch": context["activation_epoch"],
        "state_before": STATE_BEFORE, "state_after": STATE_AFTER,
    }
    activation_record_digest = canonical_digest(activation_record)
    resulting_lineage = sorted(set(lineage) | {source_digest,
        source["activation_authorization_token_digest"], source["authorization_record_digest"],
        context_digest, context["requested_state_transition_digest"],
        context["exact_activation_cycle_digest"], activation_record_digest,
        activation_bundle_digest})
    resulting_responsibility = sorted(set(responsibility) | {actos_activation_responsibility_digest})
    receipt = {
        "kernel": "ActOS Dukkha-Preserving Frontier Plan Activation Receipt Kernel",
        "kernel_version": "v0.1", "actos_version": "v0.7",
        "status": "ACTOS_DUKKHA_PRESERVING_FRONTIER_PLAN_ACTIVATION_READY",
        "source_authorization_receipt_digest": source_digest,
        "source_materialization_receipt_digest": source["source_materialization_receipt_digest"],
        "source_verifyos_dukkha_certificate_digest": source["source_verifyos_dukkha_certificate_digest"],
        "source_plan_receipt_digest": source["source_plan_receipt_digest"],
        "source_concrete_plan_digest": source["source_concrete_plan_digest"],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source["source_world_model_state_digest"],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "selected_candidate_id": source["selected_candidate_id"],
        "selected_candidate_plan_intent_digest": source["selected_candidate_plan_intent_digest"],
        "dukkha_assessment_digest": source["dukkha_assessment_digest"],
        "reference_plan_digest": source["reference_plan_digest"],
        "adapter_registry_snapshot_digest": source["adapter_registry_snapshot_digest"],
        "authorization_context_digest": source["authorization_context_digest"],
        "source_authorization_record_digest": source["authorization_record_digest"],
        "activation_authorization_token_digest": source["activation_authorization_token_digest"],
        "activation_context_digest": context_digest,
        "activation_policy_digest": activation_policy_digest,
        "actos_activation_responsibility_digest": actos_activation_responsibility_digest,
        "activation_request_id": activation_request_id,
        "activation_bundle_digest": activation_bundle_digest,
        "activated_frontier_candidate_id": source["activation_frontier_candidate_id"],
        "activated_frontier_adapter_id": source["frontier_adapter_id"],
        "activated_frontier_binding_digest": frontier["binding_digest"],
        "activated_frontier_lease_id": source["frontier_lease_id"],
        "activation_state_before": STATE_BEFORE, "activation_state_after": STATE_AFTER,
        "activation_record": activation_record, "activation_record_digest": activation_record_digest,
        "activation_authorization_consumed": True,
        "activation_authorization_token_marked_consumed": True,
        "single_use_authorization_replay_closed": True,
        "plan_activation_performed": True, "frontier_candidate_activated": True,
        "exactly_one_frontier_activated": True,
        "activation_frontier_sequence_preserved": True,
        "completed_prefix_preserved": True, "later_candidates_remain_inactive": True,
        "adapter_binding_preserved": True, "adapter_invocation_intake_admitted": True,
        "adapter_lease_use_consumed": False, "adapter_registry_snapshot_unchanged": True,
        "world_conditions_current": True, "authorization_delay_current": True,
        "token_replay_fresh_before_consumption": True,
        "frontier_replay_fresh_before_activation": True,
        "checkpoint_guards_preserved": True, "stop_conditions_preserved": True,
        "evidence_lineage_preserved": True, "alternative_candidates_preserved": True,
        "dissent_preserved": True, "minority_preserved": True,
        "dukkha_reduction_support_preserved": True,
        "protected_group_nonexternalization_preserved": True,
        "future_nonexternalization_preserved": True,
        "revision_capacity_preserved": True, "persistent_loop_reduction_preserved": True,
        "single_scalar_utility_not_introduced": True,
        "selection_remains_decisionos_owned": True,
        "selection_authority_granted_to_actos": False,
        "plan_revision_authority_granted_to_actos": False,
        "dukkha_minimization_authority_granted_to_actos": False,
        "adapter_invocation_performed": False, "tool_invocation_performed": False,
        "external_side_effect_performed": False, "execution_authority_granted": False,
        "execution_permission": False, "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True, "world_mutation_not_granted": True,
        "history_read_only": True, "qi_grants_no_authority": True,
        "future_only": True, "active_now": False,
        "resulting_lineage_digests": resulting_lineage,
        "resulting_responsibility_lineage_digests": resulting_responsibility,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return ActOSDukkhaPreservingFrontierActivationResult(STATUS_READY, [], receipt)
