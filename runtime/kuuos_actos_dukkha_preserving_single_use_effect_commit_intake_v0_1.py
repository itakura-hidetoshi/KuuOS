#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
SOURCE_DIGEST_FIELD = (
    "actos_dukkha_preserving_effect_commit_authorization_intake_receipt_digest"
)
RECEIPT_DIGEST_FIELD = (
    "actos_dukkha_preserving_single_use_effect_commit_intake_receipt_digest"
)

SOURCE_DISPOSITION = "effect_commit_authorization_ready"
STATE_BEFORE = "authorized_not_committed"
STATE_AFTER = "effect_committed_host_not_applied"
COMMIT_OUTCOME = "bounded_effect_committed_pending_external_host_effect"

CONTEXT_FIELDS = {
    "source_effect_commit_authorization_receipt_digest",
    "source_invocation_receipt_digest",
    "effect_commit_authorization_record_digest",
    "effect_commit_authorization_token_digest",
    "adapter_result_envelope_digest",
    "current_world_binding_digest",
    "current_world_model_state_digest",
    "current_world_model_revision",
    "current_world_lineage_digest",
    "authorization_receipt_observed_epoch",
    "effect_commit_epoch",
    "maximum_effect_commit_delay",
    "effect_commit_session_id",
    "effect_commit_nonce_digest",
    "prior_consumed_effect_commit_authorization_token_digests",
    "prior_effect_commit_nonce_digests",
    "prior_committed_authorization_receipt_digests",
    "requested_effect_commit_operation_digest",
    "exact_effect_commit_cycle_digest",
    "effect_commit_context_digest",
}

SOURCE_TRUE = (
    "effect_commit_authorization_admitted",
    "effect_commit_authorization_receipt_issued",
    "single_use_effect_commit_authorization_reserved",
    "effect_commit_authorization_token_replay_fresh",
    "effect_commit_intake_admitted",
    "effect_commit_review_supported",
    "world_conditions_current",
    "authorization_delay_current",
    "commit_session_replay_fresh",
    "commit_nonce_replay_fresh",
    "source_invocation_replay_fresh",
    "effect_scope_exact",
    "effect_ceiling_exact",
    "checkpoint_satisfied",
    "stop_conditions_current",
    "compensation_route_ready",
    "observation_route_ready",
    "verification_route_ready",
    "adapter_invocation_performed",
    "adapter_lease_use_consumed",
    "effect_proposal_recorded",
    "effect_commit_required",
    "persistent_world_state_unchanged",
    "observation_intake_required",
    "verification_debt_open",
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
    "world_model_prediction_not_truth",
    "world_mutation_not_granted",
    "history_read_only",
    "qi_grants_no_authority",
    "future_only",
)

SOURCE_FALSE = (
    "effect_commit_performed",
    "tool_invocation_performed",
    "external_side_effect_performed",
    "selection_authority_granted_to_actos",
    "plan_revision_authority_granted_to_actos",
    "dukkha_minimization_authority_granted_to_actos",
    "execution_authority_granted",
    "execution_permission",
    "active_now",
)


@dataclass
class ActOSDukkhaPreservingSingleUseEffectCommitResult:
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
        ).encode("utf-8")
    ).hexdigest()


def compute_effect_commit_context_digest(context: Mapping[str, Any]) -> str:
    value = dict(context)
    value.pop("effect_commit_context_digest", None)
    return canonical_digest(value)


def compute_requested_effect_commit_operation_digest(
    source: Mapping[str, Any],
) -> str:
    envelope = source.get("adapter_result_envelope")
    envelope = dict(envelope) if isinstance(envelope, Mapping) else {}
    return canonical_digest(
        {
            "source_effect_commit_authorization_receipt_digest": source.get(
                SOURCE_DIGEST_FIELD
            ),
            "source_invocation_receipt_digest": source.get(
                "source_invocation_receipt_digest"
            ),
            "effect_commit_authorization_record_digest": source.get(
                "effect_commit_authorization_record_digest"
            ),
            "effect_commit_authorization_token_digest": source.get(
                "effect_commit_authorization_token_digest"
            ),
            "adapter_result_envelope_digest": source.get(
                "adapter_result_envelope_digest"
            ),
            "invoked_frontier_candidate_id": source.get(
                "invoked_frontier_candidate_id"
            ),
            "invoked_frontier_adapter_id": source.get(
                "invoked_frontier_adapter_id"
            ),
            "invoked_frontier_binding_digest": source.get(
                "invoked_frontier_binding_digest"
            ),
            "requested_effect_tags": envelope.get("requested_effect_tags"),
            "effect_commit_state_before": STATE_BEFORE,
            "effect_commit_state_after": STATE_AFTER,
        }
    )


def compute_exact_effect_commit_cycle_digest(
    source: Mapping[str, Any], context: Mapping[str, Any]
) -> str:
    return canonical_digest(
        {
            "source_effect_commit_authorization_receipt_digest": source.get(
                SOURCE_DIGEST_FIELD
            ),
            "source_invocation_receipt_digest": source.get(
                "source_invocation_receipt_digest"
            ),
            "effect_commit_authorization_record_digest": source.get(
                "effect_commit_authorization_record_digest"
            ),
            "effect_commit_authorization_token_digest": source.get(
                "effect_commit_authorization_token_digest"
            ),
            "adapter_result_envelope_digest": source.get(
                "adapter_result_envelope_digest"
            ),
            "effect_commit_session_id": context.get("effect_commit_session_id"),
            "effect_commit_nonce_digest": context.get(
                "effect_commit_nonce_digest"
            ),
            "effect_commit_epoch": context.get("effect_commit_epoch"),
            "current_world_model_revision": context.get(
                "current_world_model_revision"
            ),
            "requested_effect_commit_operation_digest": context.get(
                "requested_effect_commit_operation_digest"
            ),
        }
    )


def compute_single_use_effect_commit_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def _strings(value: Any, allow_empty: bool = False) -> tuple[bool, list[str]]:
    if not isinstance(value, list) or (not allow_empty and not value):
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    if value != sorted(value) or len(value) != len(set(value)):
        return False, []
    return True, list(value)


def _verify_source(
    source: dict, expected_digest: str, blockers: list[str]
) -> tuple[str, dict, dict, list[str], list[str]]:
    if not source:
        blockers.append("source_effect_commit_authorization_receipt_missing")
        return "", {}, {}, [], []

    headers = {
        "kernel": "ActOS Dukkha-Preserving Effect Commit Authorization Intake Kernel",
        "kernel_version": "v0.1",
        "actos_version": "v0.9",
        "status": "ACTOS_DUKKHA_PRESERVING_EFFECT_COMMIT_AUTHORIZATION_ROUTED",
        "authorization_disposition": SOURCE_DISPOSITION,
        "effect_commit_state_after": STATE_BEFORE,
    }
    for field, value in headers.items():
        if source.get(field) != value:
            blockers.append(f"source_{field}_invalid")

    digest = source.get(SOURCE_DIGEST_FIELD)
    if not isinstance(digest, str) or not digest:
        blockers.append("source_effect_commit_authorization_receipt_digest_missing")
        digest = ""
    else:
        unsigned = dict(source)
        unsigned.pop(SOURCE_DIGEST_FIELD, None)
        if digest != canonical_digest(unsigned):
            blockers.append(
                "source_effect_commit_authorization_receipt_digest_mismatch"
            )
        if digest != expected_digest:
            blockers.append(
                "source_effect_commit_authorization_expected_binding_mismatch"
            )

    for field in SOURCE_TRUE:
        if source.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in SOURCE_FALSE:
        if source.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")

    record_raw = source.get("effect_commit_authorization_record")
    record = dict(record_raw) if isinstance(record_raw, Mapping) else {}
    record_digest = source.get("effect_commit_authorization_record_digest")
    if not record:
        blockers.append("source_effect_commit_authorization_record_invalid")
    if not isinstance(record_digest, str) or not record_digest:
        blockers.append("source_effect_commit_authorization_record_digest_missing")
    elif record_digest != canonical_digest(record):
        blockers.append("source_effect_commit_authorization_record_digest_mismatch")

    record_expected = {
        "source_invocation_receipt_digest": source.get(
            "source_invocation_receipt_digest"
        ),
        "invocation_record_digest": source.get("source_invocation_record_digest"),
        "adapter_result_envelope_digest": source.get(
            "adapter_result_envelope_digest"
        ),
        "lease_consumption_record_digest": source.get(
            "source_lease_consumption_record_digest"
        ),
        "effect_commit_review_certificate_digest": source.get(
            "effect_commit_review_certificate_digest"
        ),
        "effect_commit_authorization_context_digest": source.get(
            "effect_commit_authorization_context_digest"
        ),
        "invoked_frontier_candidate_id": source.get(
            "invoked_frontier_candidate_id"
        ),
        "invoked_frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
        "invoked_frontier_binding_digest": source.get(
            "invoked_frontier_binding_digest"
        ),
        "authorization_disposition": SOURCE_DISPOSITION,
        "effect_commit_authorization_admitted": True,
        "effect_commit_state": STATE_BEFORE,
    }
    for field, value in record_expected.items():
        if record.get(field) != value:
            blockers.append(f"source_authorization_record_{field}_mismatch")

    token_digest = source.get("effect_commit_authorization_token_digest")
    if not isinstance(token_digest, str) or not token_digest:
        blockers.append("source_effect_commit_authorization_token_digest_missing")
    else:
        expected_token = canonical_digest(
            {
                **record,
                "authorization_record_digest": record_digest,
                "effect_commit_authorization_policy_digest": source.get(
                    "effect_commit_authorization_policy_digest"
                ),
                "effect_commit_authorization_request_id": source.get(
                    "effect_commit_authorization_request_id"
                ),
            }
        )
        if token_digest != expected_token:
            blockers.append("source_effect_commit_authorization_token_digest_mismatch")

    envelope_raw = source.get("adapter_result_envelope")
    envelope = dict(envelope_raw) if isinstance(envelope_raw, Mapping) else {}
    if not envelope:
        blockers.append("source_adapter_result_envelope_invalid")
    if source.get("adapter_result_envelope_digest") != canonical_digest(envelope):
        blockers.append("source_adapter_result_envelope_digest_mismatch")
    envelope_expected = {
        "frontier_materialization_candidate_id": source.get(
            "invoked_frontier_candidate_id"
        ),
        "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
        "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
        "invocation_outcome": "bounded_effect_proposal_recorded",
        "effect_commit_state": "not_committed",
        "external_effect_requested": False,
        "tool_invocation_requested": False,
        "observation_intake_required": True,
        "verification_debt_open": True,
    }
    for field, value in envelope_expected.items():
        if envelope.get(field) != value:
            blockers.append(f"source_adapter_result_envelope_{field}_mismatch")
    effects_ok, _ = _strings(envelope.get("requested_effect_tags"), True)
    if not effects_ok:
        blockers.append("source_requested_effect_tags_invalid")

    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_resulting_responsibility_invalid")
    return digest, record, envelope, lineage, responsibility


def _verify_context(
    context: dict,
    expected_digest: str,
    source: dict,
    blockers: list[str],
) -> tuple[str, bool, bool, bool, bool, bool]:
    if not context:
        blockers.append("effect_commit_context_missing")
        return "", False, False, False, False, False
    if set(context) != CONTEXT_FIELDS:
        blockers.append("effect_commit_context_schema_invalid")

    digest = context.get("effect_commit_context_digest")
    if not isinstance(digest, str) or not digest:
        blockers.append("effect_commit_context_digest_missing")
        digest = ""
    else:
        if digest != compute_effect_commit_context_digest(context):
            blockers.append("effect_commit_context_digest_mismatch")
        if digest != expected_digest:
            blockers.append("effect_commit_context_expected_binding_mismatch")

    string_fields = CONTEXT_FIELDS - {
        "current_world_model_revision",
        "authorization_receipt_observed_epoch",
        "effect_commit_epoch",
        "maximum_effect_commit_delay",
        "prior_consumed_effect_commit_authorization_token_digests",
        "prior_effect_commit_nonce_digests",
        "prior_committed_authorization_receipt_digests",
        "effect_commit_context_digest",
    }
    for field in string_fields:
        if not isinstance(context.get(field), str) or not context.get(field):
            blockers.append(f"effect_commit_context_{field}_invalid")
    for field in (
        "current_world_model_revision",
        "authorization_receipt_observed_epoch",
        "effect_commit_epoch",
        "maximum_effect_commit_delay",
    ):
        value = context.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"effect_commit_context_{field}_invalid")
    delay = context.get("maximum_effect_commit_delay")
    if not isinstance(delay, int) or isinstance(delay, bool) or not 1 <= delay <= 64:
        blockers.append("effect_commit_context_delay_bound_invalid")

    tokens_ok, tokens = _strings(
        context.get("prior_consumed_effect_commit_authorization_token_digests"),
        True,
    )
    nonces_ok, nonces = _strings(
        context.get("prior_effect_commit_nonce_digests"), True
    )
    sources_ok, sources = _strings(
        context.get("prior_committed_authorization_receipt_digests"), True
    )
    if not tokens_ok:
        blockers.append("effect_commit_context_consumed_tokens_invalid")
    if not nonces_ok:
        blockers.append("effect_commit_context_nonces_invalid")
    if not sources_ok:
        blockers.append("effect_commit_context_sources_invalid")

    exact = {
        "source_effect_commit_authorization_receipt_digest": source.get(
            SOURCE_DIGEST_FIELD
        ),
        "source_invocation_receipt_digest": source.get(
            "source_invocation_receipt_digest"
        ),
        "effect_commit_authorization_record_digest": source.get(
            "effect_commit_authorization_record_digest"
        ),
        "effect_commit_authorization_token_digest": source.get(
            "effect_commit_authorization_token_digest"
        ),
        "adapter_result_envelope_digest": source.get(
            "adapter_result_envelope_digest"
        ),
    }
    for field, value in exact.items():
        if context.get(field) != value:
            blockers.append(f"effect_commit_context_{field}_mismatch")

    world_expected = {
        "current_world_binding_digest": source.get("source_world_binding_digest"),
        "current_world_model_state_digest": source.get(
            "source_world_model_state_digest"
        ),
        "current_world_model_revision": source.get("source_world_model_revision"),
        "current_world_lineage_digest": source.get("source_world_lineage_digest"),
    }
    world_current = all(
        context.get(field) == value for field, value in world_expected.items()
    )

    if context.get(
        "requested_effect_commit_operation_digest"
    ) != compute_requested_effect_commit_operation_digest(source):
        blockers.append("effect_commit_context_operation_digest_mismatch")
    if context.get(
        "exact_effect_commit_cycle_digest"
    ) != compute_exact_effect_commit_cycle_digest(source, context):
        blockers.append("effect_commit_context_cycle_digest_mismatch")

    observed = context.get("authorization_receipt_observed_epoch")
    epoch = context.get("effect_commit_epoch")
    max_delay = context.get("maximum_effect_commit_delay")
    delay_current = all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in (observed, epoch, max_delay)
    ) and 0 <= epoch - observed <= max_delay

    token_fresh = source.get("effect_commit_authorization_token_digest") not in tokens
    nonce_fresh = context.get("effect_commit_nonce_digest") not in nonces
    source_fresh = source.get(SOURCE_DIGEST_FIELD) not in sources
    return digest, world_current, delay_current, token_fresh, nonce_fresh, source_fresh


def build_actos_dukkha_preserving_single_use_effect_commit_intake(
    *,
    source_effect_commit_authorization_receipt: Mapping[str, Any],
    expected_source_effect_commit_authorization_receipt_digest: str,
    effect_commit_context: Mapping[str, Any],
    expected_effect_commit_context_digest: str,
    effect_commit_policy_digest: str,
    actos_effect_commit_responsibility_digest: str,
    effect_commit_request_id: str,
    single_use_effect_commit_bundle_digest: str,
) -> ActOSDukkhaPreservingSingleUseEffectCommitResult:
    blockers: list[str] = []
    source = (
        dict(source_effect_commit_authorization_receipt)
        if isinstance(source_effect_commit_authorization_receipt, Mapping)
        else {}
    )
    context = (
        dict(effect_commit_context)
        if isinstance(effect_commit_context, Mapping)
        else {}
    )
    for name, value in {
        "expected_source_effect_commit_authorization_receipt_digest": (
            expected_source_effect_commit_authorization_receipt_digest
        ),
        "expected_effect_commit_context_digest": expected_effect_commit_context_digest,
        "effect_commit_policy_digest": effect_commit_policy_digest,
        "actos_effect_commit_responsibility_digest": (
            actos_effect_commit_responsibility_digest
        ),
        "effect_commit_request_id": effect_commit_request_id,
        "single_use_effect_commit_bundle_digest": (
            single_use_effect_commit_bundle_digest
        ),
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    source_digest, authorization_record, envelope, lineage, responsibility = (
        _verify_source(
            source,
            expected_source_effect_commit_authorization_receipt_digest,
            blockers,
        )
    )
    (
        context_digest,
        world_current,
        delay_current,
        token_fresh,
        nonce_fresh,
        source_fresh,
    ) = _verify_context(
        context,
        expected_effect_commit_context_digest,
        source,
        blockers,
    )

    if not world_current:
        blockers.append("effect_commit_world_refresh_required")
    if not delay_current:
        blockers.append("effect_commit_authorization_expired")
    if not token_fresh:
        blockers.append("effect_commit_authorization_token_replay_rejected")
    if not nonce_fresh:
        blockers.append("effect_commit_nonce_replay_rejected")
    if not source_fresh:
        blockers.append("effect_commit_source_replay_rejected")

    if not blockers:
        expected_bundle = compute_single_use_effect_commit_bundle_digest(
            source_effect_commit_authorization_receipt_digest=source_digest,
            expected_source_effect_commit_authorization_receipt_digest=(
                expected_source_effect_commit_authorization_receipt_digest
            ),
            source_invocation_receipt_digest=source.get(
                "source_invocation_receipt_digest"
            ),
            effect_commit_authorization_record_digest=source.get(
                "effect_commit_authorization_record_digest"
            ),
            effect_commit_authorization_token_digest=source.get(
                "effect_commit_authorization_token_digest"
            ),
            adapter_result_envelope_digest=source.get(
                "adapter_result_envelope_digest"
            ),
            effect_commit_context_digest=context_digest,
            expected_effect_commit_context_digest=(
                expected_effect_commit_context_digest
            ),
            requested_effect_commit_operation_digest=context.get(
                "requested_effect_commit_operation_digest"
            ),
            exact_effect_commit_cycle_digest=context.get(
                "exact_effect_commit_cycle_digest"
            ),
            effect_commit_policy_digest=effect_commit_policy_digest,
            actos_effect_commit_responsibility_digest=(
                actos_effect_commit_responsibility_digest
            ),
            effect_commit_request_id=effect_commit_request_id,
        )
        if single_use_effect_commit_bundle_digest != expected_bundle:
            blockers.append("single_use_effect_commit_bundle_digest_mismatch")

    if blockers:
        return ActOSDukkhaPreservingSingleUseEffectCommitResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    commit_record = {
        "source_effect_commit_authorization_receipt_digest": source_digest,
        "source_invocation_receipt_digest": source[
            "source_invocation_receipt_digest"
        ],
        "effect_commit_authorization_record_digest": source[
            "effect_commit_authorization_record_digest"
        ],
        "effect_commit_authorization_token_digest": source[
            "effect_commit_authorization_token_digest"
        ],
        "adapter_result_envelope_digest": source[
            "adapter_result_envelope_digest"
        ],
        "invoked_frontier_candidate_id": source[
            "invoked_frontier_candidate_id"
        ],
        "invoked_frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "invoked_frontier_binding_digest": source[
            "invoked_frontier_binding_digest"
        ],
        "effect_commit_session_id": context["effect_commit_session_id"],
        "effect_commit_nonce_digest": context["effect_commit_nonce_digest"],
        "requested_effect_commit_operation_digest": context[
            "requested_effect_commit_operation_digest"
        ],
        "exact_effect_commit_cycle_digest": context[
            "exact_effect_commit_cycle_digest"
        ],
        "effect_commit_epoch": context["effect_commit_epoch"],
        "state_before": STATE_BEFORE,
        "state_after": STATE_AFTER,
        "commit_outcome": COMMIT_OUTCOME,
    }
    commit_record_digest = canonical_digest(commit_record)

    committed_effect_envelope = {
        "frontier_materialization_candidate_id": source[
            "invoked_frontier_candidate_id"
        ],
        "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "source_adapter_result_envelope_digest": source[
            "adapter_result_envelope_digest"
        ],
        "requested_effect_tags": list(envelope["requested_effect_tags"]),
        "effect_commit_state": "committed",
        "external_host_effect_state": "not_applied",
        "observation_state": "not_observed",
        "verification_state": "verification_debt_open",
        "external_host_effect_intake_required": True,
        "external_host_effect_receipt_required": True,
        "observation_intake_required": True,
        "verification_intake_required": True,
        "compensation_route_ready": True,
    }
    committed_effect_envelope_digest = canonical_digest(committed_effect_envelope)

    authorization_consumption_record = {
        "effect_commit_authorization_token_digest": source[
            "effect_commit_authorization_token_digest"
        ],
        "source_effect_commit_authorization_receipt_digest": source_digest,
        "effect_commit_session_id": context["effect_commit_session_id"],
        "effect_commit_nonce_digest": context["effect_commit_nonce_digest"],
        "effect_commit_record_digest": commit_record_digest,
        "authorization_consumed": True,
        "token_marked_consumed": True,
        "double_consumption_performed": False,
    }
    authorization_consumption_record_digest = canonical_digest(
        authorization_consumption_record
    )

    resulting_lineage = sorted(
        set(lineage)
        | {
            source_digest,
            source["source_invocation_receipt_digest"],
            source["effect_commit_authorization_record_digest"],
            source["effect_commit_authorization_token_digest"],
            source["adapter_result_envelope_digest"],
            context_digest,
            context["requested_effect_commit_operation_digest"],
            context["exact_effect_commit_cycle_digest"],
            commit_record_digest,
            committed_effect_envelope_digest,
            authorization_consumption_record_digest,
            single_use_effect_commit_bundle_digest,
        }
    )
    resulting_responsibility = sorted(
        set(responsibility) | {actos_effect_commit_responsibility_digest}
    )

    receipt = {
        "kernel": "ActOS Dukkha-Preserving Single-Use Effect Commit Intake Kernel",
        "kernel_version": "v0.1",
        "actos_version": "v0.10",
        "status": "ACTOS_DUKKHA_PRESERVING_SINGLE_USE_EFFECT_COMMIT_RECORDED",
        "source_effect_commit_authorization_receipt_digest": source_digest,
        "source_invocation_receipt_digest": source[
            "source_invocation_receipt_digest"
        ],
        "source_activation_receipt_digest": source[
            "source_activation_receipt_digest"
        ],
        "source_authorization_receipt_digest": source[
            "source_authorization_receipt_digest"
        ],
        "source_materialization_receipt_digest": source[
            "source_materialization_receipt_digest"
        ],
        "source_verifyos_dukkha_certificate_digest": source[
            "source_verifyos_dukkha_certificate_digest"
        ],
        "source_plan_receipt_digest": source["source_plan_receipt_digest"],
        "source_concrete_plan_digest": source["source_concrete_plan_digest"],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest": source[
            "source_world_model_state_digest"
        ],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "selected_candidate_id": source["selected_candidate_id"],
        "selected_candidate_plan_intent_digest": source[
            "selected_candidate_plan_intent_digest"
        ],
        "dukkha_assessment_digest": source["dukkha_assessment_digest"],
        "reference_plan_digest": source["reference_plan_digest"],
        "adapter_registry_snapshot_digest": source[
            "adapter_registry_snapshot_digest"
        ],
        "source_effect_commit_authorization_record_digest": source[
            "effect_commit_authorization_record_digest"
        ],
        "source_effect_commit_authorization_token_digest": source[
            "effect_commit_authorization_token_digest"
        ],
        "source_adapter_result_envelope_digest": source[
            "adapter_result_envelope_digest"
        ],
        "effect_commit_context_digest": context_digest,
        "effect_commit_policy_digest": effect_commit_policy_digest,
        "actos_effect_commit_responsibility_digest": (
            actos_effect_commit_responsibility_digest
        ),
        "effect_commit_request_id": effect_commit_request_id,
        "single_use_effect_commit_bundle_digest": (
            single_use_effect_commit_bundle_digest
        ),
        "invoked_frontier_candidate_id": source[
            "invoked_frontier_candidate_id"
        ],
        "invoked_frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "invoked_frontier_binding_digest": source[
            "invoked_frontier_binding_digest"
        ],
        "invoked_frontier_lease_id": source["invoked_frontier_lease_id"],
        "effect_commit_state_before": STATE_BEFORE,
        "effect_commit_state_after": STATE_AFTER,
        "effect_commit_record": commit_record,
        "effect_commit_record_digest": commit_record_digest,
        "committed_effect_envelope": committed_effect_envelope,
        "committed_effect_envelope_digest": committed_effect_envelope_digest,
        "authorization_consumption_record": authorization_consumption_record,
        "authorization_consumption_record_digest": (
            authorization_consumption_record_digest
        ),
        "effect_commit_authorization_consumed": True,
        "effect_commit_authorization_token_marked_consumed": True,
        "single_use_effect_commit_authorization_replay_closed": True,
        "effect_commit_authorization_double_consumed": False,
        "effect_commit_nonce_consumed": True,
        "effect_commit_nonce_replay_closed": True,
        "source_authorization_replay_closed": True,
        "effect_commit_authorization_token_replay_fresh_before_consumption": True,
        "effect_commit_nonce_replay_fresh_before_consumption": True,
        "source_authorization_replay_fresh_before_commit": True,
        "world_conditions_current": True,
        "effect_commit_delay_current": True,
        "exactly_one_effect_proposal_committed": True,
        "effect_commit_receipt_issued": True,
        "committed_effect_envelope_issued": True,
        "effect_commit_performed": True,
        "adapter_invocation_performed": True,
        "adapter_lease_use_consumed": True,
        "effect_scope_preserved": True,
        "effect_ceiling_preserved": True,
        "checkpoint_satisfied": True,
        "stop_conditions_current": True,
        "compensation_route_ready": True,
        "external_host_effect_intake_admitted": True,
        "external_host_effect_receipt_required": True,
        "external_host_effect_performed": False,
        "tool_invocation_performed": False,
        "external_side_effect_performed": False,
        "persistent_world_state_unchanged": True,
        "observation_intake_required": True,
        "observation_performed": False,
        "verification_intake_required": True,
        "verification_completed": False,
        "verification_debt_open": True,
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
        "execution_authority_granted": False,
        "execution_permission": False,
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
    return ActOSDukkhaPreservingSingleUseEffectCommitResult(
        STATUS_READY, [], receipt
    )
