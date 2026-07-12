#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
ACTIVATION_DIGEST_FIELD = (
    "actos_dukkha_preserving_frontier_plan_activation_receipt_digest"
)
AUTHORIZATION_DIGEST_FIELD = (
    "actos_dukkha_preserving_adapter_binding_authorization_intake_receipt_digest"
)
RECEIPT_DIGEST_FIELD = (
    "actos_dukkha_preserving_bounded_adapter_invocation_receipt_digest"
)
STATE_BEFORE = "activated_not_invoked"
STATE_AFTER = "invoked_effect_not_committed"
INVOCATION_OUTCOME = "bounded_effect_proposal_recorded"

FORBIDDEN_EFFECTS = frozenset(
    {
        "active_now",
        "candidate_substitution",
        "execution_permission",
        "external_side_effect",
        "persistent_world_mutation",
        "selection_authority_transfer",
        "tool_invocation",
        "unreviewed_scope_expansion",
    }
)

CONTEXT_FIELDS = {
    "source_activation_receipt_digest",
    "source_authorization_receipt_digest",
    "requested_frontier_candidate_id",
    "requested_frontier_adapter_id",
    "requested_frontier_binding_digest",
    "requested_frontier_lease_id",
    "lease_reservation_digest",
    "invocation_session_id",
    "invocation_intent_digest",
    "invocation_nonce_digest",
    "current_world_binding_digest",
    "current_world_model_state_digest",
    "current_world_model_revision",
    "current_world_lineage_digest",
    "activation_receipt_observed_epoch",
    "invocation_epoch",
    "maximum_invocation_delay",
    "prior_consumed_lease_reservation_digests",
    "prior_invocation_nonce_digests",
    "prior_invoked_frontier_candidate_ids",
    "requested_operation_digest",
    "exact_invocation_cycle_digest",
    "invocation_context_digest",
}

ACTIVATION_TRUE = (
    "activation_authorization_consumed",
    "activation_authorization_token_marked_consumed",
    "single_use_authorization_replay_closed",
    "plan_activation_performed",
    "frontier_candidate_activated",
    "exactly_one_frontier_activated",
    "activation_frontier_sequence_preserved",
    "completed_prefix_preserved",
    "later_candidates_remain_inactive",
    "adapter_binding_preserved",
    "adapter_invocation_intake_admitted",
    "adapter_registry_snapshot_unchanged",
    "world_conditions_current",
    "authorization_delay_current",
    "token_replay_fresh_before_consumption",
    "frontier_replay_fresh_before_activation",
    "checkpoint_guards_preserved",
    "stop_conditions_preserved",
    "evidence_lineage_preserved",
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
    "persistent_world_state_unchanged",
    "world_model_prediction_not_truth",
    "world_mutation_not_granted",
    "history_read_only",
    "qi_grants_no_authority",
    "future_only",
)

ACTIVATION_FALSE = (
    "adapter_lease_use_consumed",
    "selection_authority_granted_to_actos",
    "plan_revision_authority_granted_to_actos",
    "dukkha_minimization_authority_granted_to_actos",
    "adapter_invocation_performed",
    "tool_invocation_performed",
    "external_side_effect_performed",
    "execution_authority_granted",
    "execution_permission",
    "active_now",
)

AUTHORIZATION_TRUE = (
    "activation_authorization_admitted",
    "activation_authorization_receipt_issued",
    "single_use_authorization_reserved",
    "adapter_registry_snapshot_unchanged",
    "world_conditions_current",
    "freshness_current",
    "adapter_registry_ready",
    "frontier_lease_available",
    "session_intent_nonce_replay_fresh",
    "irreversible_step_reverification_satisfied",
    "adapter_binding_performed",
    "all_materialization_candidates_bound",
    "one_to_one_candidate_binding_preserved",
    "activation_frontier_sequence_preserved",
    "scope_and_effect_ceiling_exact",
    "checkpoint_guards_preserved",
    "stop_conditions_preserved",
    "evidence_lineage_preserved",
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
    "persistent_world_state_unchanged",
    "world_model_prediction_not_truth",
    "world_mutation_not_granted",
    "history_read_only",
    "qi_grants_no_authority",
    "future_only",
)

AUTHORIZATION_FALSE = (
    "lease_use_consumed",
    "selection_authority_granted_to_actos",
    "plan_revision_authority_granted_to_actos",
    "dukkha_minimization_authority_granted_to_actos",
    "plan_activated",
    "adapter_invocation_performed",
    "tool_invocation_performed",
    "external_side_effect_performed",
    "execution_authority_granted",
    "execution_permission",
    "active_now",
)


@dataclass
class ActOSDukkhaPreservingBoundedAdapterInvocationResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def compute_invocation_context_digest(context: Mapping[str, Any]) -> str:
    value = dict(context)
    value.pop("invocation_context_digest", None)
    return canonical_digest(value)


def compute_lease_reservation_digest(
    authorization_receipt: Mapping[str, Any],
) -> str:
    record = authorization_receipt.get("authorization_record")
    record = record if isinstance(record, Mapping) else {}
    return canonical_digest(
        {
            "authorization_receipt_digest": authorization_receipt.get(
                AUTHORIZATION_DIGEST_FIELD
            ),
            "activation_authorization_token_digest": authorization_receipt.get(
                "activation_authorization_token_digest"
            ),
            "authorization_record_digest": authorization_receipt.get(
                "authorization_record_digest"
            ),
            "frontier_binding_digest": record.get("frontier_binding_digest"),
            "frontier_lease_id": authorization_receipt.get("frontier_lease_id"),
            "remaining_uses_before_reservation": authorization_receipt.get(
                "remaining_uses_before_reservation"
            ),
            "remaining_uses_after_reservation": authorization_receipt.get(
                "remaining_uses_after_reservation"
            ),
        }
    )


def compute_invocation_intent_digest(
    activation_receipt: Mapping[str, Any],
    binding: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "selected_candidate_id": activation_receipt.get("selected_candidate_id"),
            "selected_candidate_plan_intent_digest": activation_receipt.get(
                "selected_candidate_plan_intent_digest"
            ),
            "activated_frontier_candidate_id": activation_receipt.get(
                "activated_frontier_candidate_id"
            ),
            "activated_frontier_adapter_id": activation_receipt.get(
                "activated_frontier_adapter_id"
            ),
            "activated_frontier_binding_digest": activation_receipt.get(
                "activated_frontier_binding_digest"
            ),
            "requested_effect_tags": binding.get("requested_effect_tags"),
        }
    )


def compute_requested_operation_digest(
    activation_receipt: Mapping[str, Any],
    binding: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "frontier_materialization_candidate_id": activation_receipt.get(
                "activated_frontier_candidate_id"
            ),
            "frontier_adapter_id": activation_receipt.get(
                "activated_frontier_adapter_id"
            ),
            "frontier_binding_digest": activation_receipt.get(
                "activated_frontier_binding_digest"
            ),
            "frontier_lease_id": activation_receipt.get(
                "activated_frontier_lease_id"
            ),
            "capability_digest": binding.get("capability_digest"),
            "scope_digest": binding.get("scope_digest"),
            "effect_ceiling_digest": binding.get("effect_ceiling_digest"),
            "requested_effect_tags": binding.get("requested_effect_tags"),
            "state_before": STATE_BEFORE,
            "state_after": STATE_AFTER,
        }
    )


def compute_exact_invocation_cycle_digest(
    activation_receipt: Mapping[str, Any],
    authorization_receipt: Mapping[str, Any],
    context: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_activation_receipt_digest": activation_receipt.get(
                ACTIVATION_DIGEST_FIELD
            ),
            "source_authorization_receipt_digest": authorization_receipt.get(
                AUTHORIZATION_DIGEST_FIELD
            ),
            "source_activation_record_digest": activation_receipt.get(
                "activation_record_digest"
            ),
            "lease_reservation_digest": context.get("lease_reservation_digest"),
            "frontier_candidate_id": activation_receipt.get(
                "activated_frontier_candidate_id"
            ),
            "frontier_binding_digest": activation_receipt.get(
                "activated_frontier_binding_digest"
            ),
            "frontier_adapter_id": activation_receipt.get(
                "activated_frontier_adapter_id"
            ),
            "frontier_lease_id": activation_receipt.get(
                "activated_frontier_lease_id"
            ),
            "invocation_session_id": context.get("invocation_session_id"),
            "invocation_intent_digest": context.get("invocation_intent_digest"),
            "invocation_nonce_digest": context.get("invocation_nonce_digest"),
            "invocation_epoch": context.get("invocation_epoch"),
            "current_world_model_revision": context.get(
                "current_world_model_revision"
            ),
            "requested_operation_digest": context.get(
                "requested_operation_digest"
            ),
        }
    )


def compute_bounded_adapter_invocation_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def _strings(value: Any, *, empty: bool = False) -> tuple[bool, list[str]]:
    if not isinstance(value, list) or (not empty and not value):
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    if value != sorted(value) or len(value) != len(set(value)):
        return False, []
    return True, list(value)


def _verify_digest_bound_object(
    obj: dict,
    *,
    digest_field: str,
    expected_digest: str,
    prefix: str,
    blockers: list[str],
) -> str:
    digest = obj.get(digest_field)
    if not isinstance(digest, str) or not digest:
        blockers.append(f"{prefix}_digest_missing")
        return ""
    unsigned = dict(obj)
    unsigned.pop(digest_field, None)
    if digest != canonical_digest(unsigned):
        blockers.append(f"{prefix}_digest_mismatch")
    if digest != expected_digest:
        blockers.append(f"{prefix}_expected_binding_mismatch")
    return digest


def _verify_activation_receipt(
    source: dict,
    expected_digest: str,
    blockers: list[str],
) -> tuple[str, dict, list[str], list[str]]:
    if not source:
        blockers.append("source_activation_receipt_missing")
        return "", {}, [], []
    expected_headers = {
        "kernel": "ActOS Dukkha-Preserving Frontier Plan Activation Receipt Kernel",
        "kernel_version": "v0.1",
        "actos_version": "v0.7",
        "status": "ACTOS_DUKKHA_PRESERVING_FRONTIER_PLAN_ACTIVATION_READY",
        "activation_state_before": "bound_not_invoked",
        "activation_state_after": STATE_BEFORE,
    }
    for field, expected in expected_headers.items():
        if source.get(field) != expected:
            blockers.append(f"source_activation_{field}_invalid")
    digest = _verify_digest_bound_object(
        source,
        digest_field=ACTIVATION_DIGEST_FIELD,
        expected_digest=expected_digest,
        prefix="source_activation_receipt",
        blockers=blockers,
    )
    for field in ACTIVATION_TRUE:
        if source.get(field) is not True:
            blockers.append(f"source_activation_boundary_{field}_missing")
    for field in ACTIVATION_FALSE:
        if source.get(field) is not False:
            blockers.append(f"source_activation_boundary_{field}_promoted")

    raw_record = source.get("activation_record")
    record = dict(raw_record) if isinstance(raw_record, Mapping) else {}
    if not record:
        blockers.append("source_activation_record_invalid")
    if source.get("activation_record_digest") != canonical_digest(record):
        blockers.append("source_activation_record_digest_mismatch")
    exact_record = {
        "frontier_materialization_candidate_id": source.get(
            "activated_frontier_candidate_id"
        ),
        "frontier_adapter_id": source.get("activated_frontier_adapter_id"),
        "frontier_binding_digest": source.get(
            "activated_frontier_binding_digest"
        ),
        "frontier_lease_id": source.get("activated_frontier_lease_id"),
        "state_before": "bound_not_invoked",
        "state_after": STATE_BEFORE,
    }
    for field, expected in exact_record.items():
        if record.get(field) != expected:
            blockers.append(f"source_activation_record_{field}_mismatch")

    source_authorization_digest = source.get("source_authorization_receipt_digest")
    if not isinstance(source_authorization_digest, str) or not source_authorization_digest:
        blockers.append("source_activation_authorization_binding_missing")

    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_activation_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_activation_resulting_responsibility_invalid")
    return digest, record, lineage, responsibility


def _verify_authorization_receipt(
    authorization: dict,
    expected_digest: str,
    activation: dict,
    blockers: list[str],
) -> tuple[str, dict, dict, int, int]:
    if not authorization:
        blockers.append("source_authorization_receipt_missing")
        return "", {}, {}, 0, 0
    expected_headers = {
        "kernel": "ActOS Dukkha-Preserving Adapter Binding and Activation Authorization Intake Kernel",
        "kernel_version": "v0.1",
        "actos_version": "v0.6",
        "status": "ACTOS_DUKKHA_PRESERVING_ADAPTER_BINDING_AUTHORIZATION_ROUTED",
        "authorization_disposition": "activation_authorization_ready",
    }
    for field, expected in expected_headers.items():
        if authorization.get(field) != expected:
            blockers.append(f"source_authorization_{field}_invalid")
    digest = _verify_digest_bound_object(
        authorization,
        digest_field=AUTHORIZATION_DIGEST_FIELD,
        expected_digest=expected_digest,
        prefix="source_authorization_receipt",
        blockers=blockers,
    )
    if activation.get("source_authorization_receipt_digest") != digest:
        blockers.append("activation_authorization_receipt_binding_mismatch")
    for field in AUTHORIZATION_TRUE:
        if authorization.get(field) is not True:
            blockers.append(f"source_authorization_boundary_{field}_missing")
    for field in AUTHORIZATION_FALSE:
        if authorization.get(field) is not False:
            blockers.append(f"source_authorization_boundary_{field}_promoted")

    raw_record = authorization.get("authorization_record")
    record = dict(raw_record) if isinstance(raw_record, Mapping) else {}
    if not record:
        blockers.append("source_authorization_record_invalid")
    if authorization.get("authorization_record_digest") != canonical_digest(record):
        blockers.append("source_authorization_record_digest_mismatch")

    raw_bindings = authorization.get("adapter_bindings")
    bindings = (
        [dict(item) for item in raw_bindings]
        if isinstance(raw_bindings, list)
        and raw_bindings
        and all(isinstance(item, Mapping) for item in raw_bindings)
        else []
    )
    if not bindings:
        blockers.append("source_authorization_bindings_invalid")
    if authorization.get("adapter_binding_count") != len(bindings):
        blockers.append("source_authorization_binding_count_mismatch")
    if authorization.get("adapter_binding_set_digest") != canonical_digest(bindings):
        blockers.append("source_authorization_binding_set_digest_mismatch")

    frontier_id = activation.get("activated_frontier_candidate_id")
    matches = [
        item
        for item in bindings
        if item.get("materialization_candidate_id") == frontier_id
    ]
    binding = matches[0] if len(matches) == 1 else {}
    if not binding:
        blockers.append("source_authorization_frontier_binding_not_unique")
    else:
        unsigned = dict(binding)
        supplied = unsigned.pop("binding_digest", None)
        if supplied != canonical_digest(unsigned):
            blockers.append("source_authorization_frontier_binding_digest_mismatch")
        exact_binding = {
            "binding_digest": activation.get("activated_frontier_binding_digest"),
            "adapter_id": activation.get("activated_frontier_adapter_id"),
            "lease_id": activation.get("activated_frontier_lease_id"),
            "binding_state": "bound_not_invoked",
        }
        for field, expected in exact_binding.items():
            if binding.get(field) != expected:
                blockers.append(f"source_authorization_binding_{field}_mismatch")
        effects_ok, effects = _strings(
            binding.get("requested_effect_tags"), empty=True
        )
        if not effects_ok:
            blockers.append("source_authorization_requested_effects_invalid")
        if FORBIDDEN_EFFECTS.intersection(effects):
            blockers.append("source_authorization_forbidden_effect")

    before = authorization.get("remaining_uses_before_reservation")
    after = authorization.get("remaining_uses_after_reservation")
    if not (
        isinstance(before, int)
        and not isinstance(before, bool)
        and isinstance(after, int)
        and not isinstance(after, bool)
        and after >= 0
        and after + 1 == before
    ):
        blockers.append("source_authorization_reservation_arithmetic_invalid")
        before, after = 0, 0
    return digest, record, binding, before, after


def _verify_context(
    context: dict,
    expected_digest: str,
    activation: dict,
    authorization: dict,
    binding: dict,
    blockers: list[str],
) -> tuple[str, str, bool, bool, bool, bool, bool]:
    if not context:
        blockers.append("invocation_context_missing")
        return "", "", False, False, False, False, False
    if set(context) != CONTEXT_FIELDS:
        blockers.append("invocation_context_schema_invalid")
    digest = context.get("invocation_context_digest")
    if not isinstance(digest, str) or not digest:
        blockers.append("invocation_context_digest_missing")
        digest = ""
    else:
        if digest != compute_invocation_context_digest(context):
            blockers.append("invocation_context_digest_mismatch")
        if digest != expected_digest:
            blockers.append("invocation_context_expected_binding_mismatch")

    list_fields = {
        "prior_consumed_lease_reservation_digests",
        "prior_invocation_nonce_digests",
        "prior_invoked_frontier_candidate_ids",
    }
    int_fields = {
        "current_world_model_revision",
        "activation_receipt_observed_epoch",
        "invocation_epoch",
        "maximum_invocation_delay",
    }
    for field in CONTEXT_FIELDS - list_fields - int_fields - {
        "invocation_context_digest"
    }:
        if not isinstance(context.get(field), str) or not context.get(field):
            blockers.append(f"invocation_context_{field}_invalid")
    for field in int_fields:
        value = context.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"invocation_context_{field}_invalid")
    bound = context.get("maximum_invocation_delay")
    if not isinstance(bound, int) or isinstance(bound, bool) or not 1 <= bound <= 64:
        blockers.append("invocation_context_delay_bound_invalid")

    prior: dict[str, list[str]] = {}
    for field in list_fields:
        valid, values = _strings(context.get(field), empty=True)
        if not valid:
            blockers.append(f"invocation_context_{field}_invalid")
        prior[field] = values

    expected_reservation = compute_lease_reservation_digest(authorization)
    exact = {
        "source_activation_receipt_digest": activation.get(
            ACTIVATION_DIGEST_FIELD
        ),
        "source_authorization_receipt_digest": authorization.get(
            AUTHORIZATION_DIGEST_FIELD
        ),
        "requested_frontier_candidate_id": activation.get(
            "activated_frontier_candidate_id"
        ),
        "requested_frontier_adapter_id": activation.get(
            "activated_frontier_adapter_id"
        ),
        "requested_frontier_binding_digest": activation.get(
            "activated_frontier_binding_digest"
        ),
        "requested_frontier_lease_id": activation.get(
            "activated_frontier_lease_id"
        ),
        "lease_reservation_digest": expected_reservation,
        "invocation_intent_digest": compute_invocation_intent_digest(
            activation, binding
        ),
        "current_world_binding_digest": activation.get(
            "source_world_binding_digest"
        ),
        "current_world_model_state_digest": activation.get(
            "source_world_model_state_digest"
        ),
        "current_world_model_revision": activation.get(
            "source_world_model_revision"
        ),
        "current_world_lineage_digest": activation.get(
            "source_world_lineage_digest"
        ),
    }
    for field, expected in exact.items():
        if context.get(field) != expected:
            blockers.append(f"invocation_context_{field}_mismatch")
    if context.get("requested_operation_digest") != compute_requested_operation_digest(
        activation, binding
    ):
        blockers.append("invocation_context_operation_digest_mismatch")
    if context.get("exact_invocation_cycle_digest") != (
        compute_exact_invocation_cycle_digest(activation, authorization, context)
    ):
        blockers.append("invocation_context_exact_cycle_digest_mismatch")

    world_current = all(
        context.get(field) == expected
        for field, expected in exact.items()
        if field.startswith("current_world_")
    )
    observed = context.get("activation_receipt_observed_epoch")
    epoch = context.get("invocation_epoch")
    delay = context.get("maximum_invocation_delay")
    delay_current = (
        all(
            isinstance(value, int) and not isinstance(value, bool)
            for value in (observed, epoch, delay)
        )
        and 0 <= epoch - observed <= delay
    )
    reservation_fresh = expected_reservation not in prior[
        "prior_consumed_lease_reservation_digests"
    ]
    nonce_fresh = context.get("invocation_nonce_digest") not in prior[
        "prior_invocation_nonce_digests"
    ]
    frontier_fresh = activation.get("activated_frontier_candidate_id") not in prior[
        "prior_invoked_frontier_candidate_ids"
    ]
    return (
        digest,
        expected_reservation,
        world_current,
        delay_current,
        reservation_fresh,
        nonce_fresh,
        frontier_fresh,
    )


def build_actos_dukkha_preserving_bounded_adapter_invocation(
    *,
    source_activation_receipt: Mapping[str, Any],
    expected_source_activation_receipt_digest: str,
    source_authorization_receipt: Mapping[str, Any],
    expected_source_authorization_receipt_digest: str,
    invocation_context: Mapping[str, Any],
    expected_invocation_context_digest: str,
    invocation_policy_digest: str,
    actos_invocation_responsibility_digest: str,
    invocation_request_id: str,
    invocation_bundle_digest: str,
) -> ActOSDukkhaPreservingBoundedAdapterInvocationResult:
    blockers: list[str] = []
    activation = (
        dict(source_activation_receipt)
        if isinstance(source_activation_receipt, Mapping)
        else {}
    )
    authorization = (
        dict(source_authorization_receipt)
        if isinstance(source_authorization_receipt, Mapping)
        else {}
    )
    context = dict(invocation_context) if isinstance(invocation_context, Mapping) else {}
    for name, value in {
        "expected_source_activation_receipt_digest": (
            expected_source_activation_receipt_digest
        ),
        "expected_source_authorization_receipt_digest": (
            expected_source_authorization_receipt_digest
        ),
        "expected_invocation_context_digest": expected_invocation_context_digest,
        "invocation_policy_digest": invocation_policy_digest,
        "actos_invocation_responsibility_digest": (
            actos_invocation_responsibility_digest
        ),
        "invocation_request_id": invocation_request_id,
        "invocation_bundle_digest": invocation_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    activation_digest, activation_record, lineage, responsibility = (
        _verify_activation_receipt(
            activation, expected_source_activation_receipt_digest, blockers
        )
    )
    authorization_digest, authorization_record, binding, remaining_before, remaining_after = (
        _verify_authorization_receipt(
            authorization,
            expected_source_authorization_receipt_digest,
            activation,
            blockers,
        )
    )
    (
        context_digest,
        lease_reservation_digest,
        world_current,
        delay_current,
        reservation_fresh,
        nonce_fresh,
        frontier_fresh,
    ) = _verify_context(
        context,
        expected_invocation_context_digest,
        activation,
        authorization,
        binding,
        blockers,
    )

    if not world_current:
        blockers.append("invocation_world_refresh_required")
    if not delay_current:
        blockers.append("invocation_activation_receipt_expired")
    if not reservation_fresh:
        blockers.append("invocation_lease_reservation_replay_rejected")
    if not nonce_fresh:
        blockers.append("invocation_nonce_replay_rejected")
    if not frontier_fresh:
        blockers.append("invocation_frontier_replay_rejected")

    binding_digest = binding.get("binding_digest", "")
    if not blockers:
        expected_bundle = compute_bounded_adapter_invocation_bundle_digest(
            source_activation_receipt_digest=activation_digest,
            expected_source_activation_receipt_digest=(
                expected_source_activation_receipt_digest
            ),
            source_authorization_receipt_digest=authorization_digest,
            expected_source_authorization_receipt_digest=(
                expected_source_authorization_receipt_digest
            ),
            source_activation_record_digest=activation.get(
                "activation_record_digest"
            ),
            frontier_binding_digest=binding_digest,
            lease_reservation_digest=lease_reservation_digest,
            invocation_context_digest=context_digest,
            expected_invocation_context_digest=expected_invocation_context_digest,
            requested_operation_digest=context.get("requested_operation_digest"),
            exact_invocation_cycle_digest=context.get(
                "exact_invocation_cycle_digest"
            ),
            invocation_policy_digest=invocation_policy_digest,
            actos_invocation_responsibility_digest=(
                actos_invocation_responsibility_digest
            ),
            invocation_request_id=invocation_request_id,
        )
        if invocation_bundle_digest != expected_bundle:
            blockers.append("invocation_bundle_digest_mismatch")

    if blockers:
        return ActOSDukkhaPreservingBoundedAdapterInvocationResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    invocation_record = {
        "frontier_materialization_candidate_id": activation[
            "activated_frontier_candidate_id"
        ],
        "frontier_adapter_id": activation["activated_frontier_adapter_id"],
        "frontier_binding_digest": binding_digest,
        "frontier_lease_id": activation["activated_frontier_lease_id"],
        "lease_reservation_digest": lease_reservation_digest,
        "source_activation_record_digest": activation["activation_record_digest"],
        "source_authorization_record_digest": authorization[
            "authorization_record_digest"
        ],
        "invocation_session_id": context["invocation_session_id"],
        "invocation_intent_digest": context["invocation_intent_digest"],
        "invocation_nonce_digest": context["invocation_nonce_digest"],
        "requested_operation_digest": context["requested_operation_digest"],
        "exact_invocation_cycle_digest": context[
            "exact_invocation_cycle_digest"
        ],
        "invocation_epoch": context["invocation_epoch"],
        "state_before": STATE_BEFORE,
        "state_after": STATE_AFTER,
        "invocation_outcome": INVOCATION_OUTCOME,
    }
    invocation_record_digest = canonical_digest(invocation_record)
    result_envelope = {
        "frontier_materialization_candidate_id": activation[
            "activated_frontier_candidate_id"
        ],
        "frontier_adapter_id": activation["activated_frontier_adapter_id"],
        "frontier_binding_digest": binding_digest,
        "requested_effect_tags": list(binding["requested_effect_tags"]),
        "invocation_outcome": INVOCATION_OUTCOME,
        "effect_commit_state": "not_committed",
        "external_effect_requested": False,
        "tool_invocation_requested": False,
        "observation_intake_required": True,
        "verification_debt_open": True,
    }
    result_envelope_digest = canonical_digest(result_envelope)
    lease_consumption_record = {
        "frontier_lease_id": activation["activated_frontier_lease_id"],
        "lease_reservation_digest": lease_reservation_digest,
        "remaining_uses_before_reservation": remaining_before,
        "remaining_uses_after_reservation": remaining_after,
        "remaining_uses_at_invocation": remaining_after,
        "reservation_consumed": True,
        "double_decrement_performed": False,
        "invocation_record_digest": invocation_record_digest,
    }
    lease_consumption_record_digest = canonical_digest(lease_consumption_record)

    resulting_lineage = sorted(
        set(lineage)
        | {
            activation_digest,
            authorization_digest,
            activation["activation_record_digest"],
            authorization["authorization_record_digest"],
            binding_digest,
            lease_reservation_digest,
            context_digest,
            context["requested_operation_digest"],
            context["exact_invocation_cycle_digest"],
            invocation_record_digest,
            result_envelope_digest,
            lease_consumption_record_digest,
            invocation_bundle_digest,
        }
    )
    resulting_responsibility = sorted(
        set(responsibility) | {actos_invocation_responsibility_digest}
    )

    receipt = {
        "kernel": "ActOS Dukkha-Preserving Bounded Adapter Invocation Kernel",
        "kernel_version": "v0.1",
        "actos_version": "v0.8",
        "status": "ACTOS_DUKKHA_PRESERVING_BOUNDED_ADAPTER_INVOCATION_RECORDED",
        "source_activation_receipt_digest": activation_digest,
        "source_authorization_receipt_digest": authorization_digest,
        "source_materialization_receipt_digest": activation[
            "source_materialization_receipt_digest"
        ],
        "source_verifyos_dukkha_certificate_digest": activation[
            "source_verifyos_dukkha_certificate_digest"
        ],
        "source_plan_receipt_digest": activation["source_plan_receipt_digest"],
        "source_concrete_plan_digest": activation["source_concrete_plan_digest"],
        "source_world_binding_digest": activation["source_world_binding_digest"],
        "source_world_model_state_digest": activation[
            "source_world_model_state_digest"
        ],
        "source_world_model_revision": activation["source_world_model_revision"],
        "source_world_lineage_digest": activation["source_world_lineage_digest"],
        "selected_candidate_id": activation["selected_candidate_id"],
        "selected_candidate_plan_intent_digest": activation[
            "selected_candidate_plan_intent_digest"
        ],
        "dukkha_assessment_digest": activation["dukkha_assessment_digest"],
        "reference_plan_digest": activation["reference_plan_digest"],
        "adapter_registry_snapshot_digest": activation[
            "adapter_registry_snapshot_digest"
        ],
        "source_activation_record_digest": activation[
            "activation_record_digest"
        ],
        "source_authorization_record_digest": authorization[
            "authorization_record_digest"
        ],
        "invocation_context_digest": context_digest,
        "invocation_policy_digest": invocation_policy_digest,
        "actos_invocation_responsibility_digest": (
            actos_invocation_responsibility_digest
        ),
        "invocation_request_id": invocation_request_id,
        "invocation_bundle_digest": invocation_bundle_digest,
        "invoked_frontier_candidate_id": activation[
            "activated_frontier_candidate_id"
        ],
        "invoked_frontier_adapter_id": activation[
            "activated_frontier_adapter_id"
        ],
        "invoked_frontier_binding_digest": binding_digest,
        "invoked_frontier_lease_id": activation["activated_frontier_lease_id"],
        "lease_reservation_digest": lease_reservation_digest,
        "invocation_state_before": STATE_BEFORE,
        "invocation_state_after": STATE_AFTER,
        "invocation_record": invocation_record,
        "invocation_record_digest": invocation_record_digest,
        "adapter_result_envelope": result_envelope,
        "adapter_result_envelope_digest": result_envelope_digest,
        "lease_consumption_record": lease_consumption_record,
        "lease_consumption_record_digest": lease_consumption_record_digest,
        "adapter_invocation_performed": True,
        "adapter_host_invocation_performed": True,
        "exactly_one_adapter_invoked": True,
        "bounded_scope_preserved": True,
        "effect_ceiling_preserved": True,
        "activation_frontier_sequence_preserved": True,
        "completed_prefix_preserved": True,
        "later_candidates_remain_uninvoked": True,
        "adapter_lease_reservation_consumed": True,
        "adapter_lease_use_consumed": True,
        "adapter_lease_double_decremented": False,
        "lease_consumption_record_issued": True,
        "remaining_uses_before_reservation": remaining_before,
        "remaining_uses_after_reservation": remaining_after,
        "remaining_uses_at_invocation": remaining_after,
        "invocation_nonce_consumed": True,
        "invocation_nonce_replay_closed": True,
        "frontier_invocation_replay_closed": True,
        "invocation_result_envelope_issued": True,
        "effect_proposal_recorded": True,
        "effect_commit_required": True,
        "effect_commit_performed": False,
        "observation_intake_required": True,
        "verification_debt_open": True,
        "adapter_registry_snapshot_unchanged": True,
        "world_conditions_current": True,
        "invocation_delay_current": True,
        "lease_reservation_replay_fresh_before_consumption": True,
        "invocation_nonce_replay_fresh_before_consumption": True,
        "frontier_replay_fresh_before_invocation": True,
        "checkpoint_guards_preserved": True,
        "stop_conditions_preserved": True,
        "evidence_lineage_preserved": True,
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
        "selection_authority_granted_to_actos": False,
        "plan_revision_authority_granted_to_actos": False,
        "dukkha_minimization_authority_granted_to_actos": False,
        "tool_invocation_performed": False,
        "external_side_effect_performed": False,
        "execution_authority_granted": False,
        "execution_permission": False,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "resulting_lineage_digests": resulting_lineage,
        "resulting_responsibility_lineage_digests": resulting_responsibility,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return ActOSDukkhaPreservingBoundedAdapterInvocationResult(
        STATUS_READY, [], receipt
    )
