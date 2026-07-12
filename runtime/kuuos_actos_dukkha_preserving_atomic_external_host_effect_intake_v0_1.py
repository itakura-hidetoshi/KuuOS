#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
SOURCE_DIGEST_FIELD = (
    "actos_dukkha_preserving_single_use_effect_commit_intake_receipt_digest"
)
RECEIPT_DIGEST_FIELD = (
    "actos_dukkha_preserving_atomic_external_host_effect_intake_receipt_digest"
)
HOST_RECEIPT_DIGEST_FIELD = "external_host_effect_application_receipt_digest"

STATE_BEFORE = "effect_committed_host_not_applied"
STATE_AFTER = "host_effect_recorded_unobserved"
HOST_OUTCOME = "bounded_external_host_effect_applied"
INTAKE_OUTCOME = "bounded_external_host_effect_recorded_pending_observation"

HOST_RECEIPT_FIELDS = {
    "source_effect_commit_receipt_digest",
    "effect_commit_record_digest",
    "committed_effect_envelope_digest",
    "frontier_materialization_candidate_id",
    "frontier_adapter_id",
    "frontier_binding_digest",
    "requested_effect_tags",
    "host_effect_operation_digest",
    "host_effect_session_id",
    "host_effect_nonce_digest",
    "host_driver_id",
    "host_target_digest",
    "host_effect_started_epoch",
    "host_effect_completed_epoch",
    "maximum_host_effect_duration",
    "host_effect_outcome",
    "exactly_one_effect_applied",
    "tool_invocation_performed",
    "external_side_effect_performed",
    "compensation_route_digest",
    "observation_route_digest",
    "verification_route_digest",
    HOST_RECEIPT_DIGEST_FIELD,
}

CONTEXT_FIELDS = {
    "source_effect_commit_receipt_digest",
    "effect_commit_record_digest",
    "committed_effect_envelope_digest",
    HOST_RECEIPT_DIGEST_FIELD,
    "current_world_binding_digest",
    "current_world_model_state_digest",
    "current_world_model_revision",
    "current_world_lineage_digest",
    "source_commit_receipt_observed_epoch",
    "host_effect_intake_epoch",
    "maximum_host_effect_intake_delay",
    "host_effect_intake_session_id",
    "host_effect_intake_nonce_digest",
    "prior_host_effect_intake_session_ids",
    "prior_host_effect_application_receipt_digests",
    "prior_host_effect_intake_nonce_digests",
    "prior_applied_committed_effect_envelope_digests",
    "requested_host_effect_intake_operation_digest",
    "exact_host_effect_intake_cycle_digest",
    "host_effect_intake_context_digest",
}

SOURCE_TRUE = (
    "effect_commit_authorization_consumed",
    "effect_commit_authorization_token_marked_consumed",
    "single_use_effect_commit_authorization_replay_closed",
    "effect_commit_nonce_consumed",
    "effect_commit_nonce_replay_closed",
    "source_authorization_replay_closed",
    "effect_commit_authorization_token_replay_fresh_before_consumption",
    "effect_commit_nonce_replay_fresh_before_consumption",
    "source_authorization_replay_fresh_before_commit",
    "world_conditions_current",
    "effect_commit_delay_current",
    "exactly_one_effect_proposal_committed",
    "effect_commit_receipt_issued",
    "committed_effect_envelope_issued",
    "effect_commit_performed",
    "adapter_invocation_performed",
    "adapter_lease_use_consumed",
    "effect_scope_preserved",
    "effect_ceiling_preserved",
    "checkpoint_satisfied",
    "stop_conditions_current",
    "compensation_route_ready",
    "external_host_effect_intake_admitted",
    "external_host_effect_receipt_required",
    "persistent_world_state_unchanged",
    "observation_intake_required",
    "verification_intake_required",
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
    "effect_commit_authorization_double_consumed",
    "external_host_effect_performed",
    "tool_invocation_performed",
    "external_side_effect_performed",
    "observation_performed",
    "verification_completed",
    "selection_authority_granted_to_actos",
    "plan_revision_authority_granted_to_actos",
    "dukkha_minimization_authority_granted_to_actos",
    "execution_authority_granted",
    "execution_permission",
    "active_now",
)


@dataclass
class ActOSDukkhaPreservingAtomicExternalHostEffectResult:
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


def compute_external_host_effect_application_receipt_digest(
    receipt: Mapping[str, Any],
) -> str:
    value = dict(receipt)
    value.pop(HOST_RECEIPT_DIGEST_FIELD, None)
    return canonical_digest(value)


def compute_host_effect_operation_digest(source: Mapping[str, Any]) -> str:
    envelope = source.get("committed_effect_envelope")
    envelope = dict(envelope) if isinstance(envelope, Mapping) else {}
    return canonical_digest(
        {
            "source_effect_commit_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
            "effect_commit_record_digest": source.get("effect_commit_record_digest"),
            "committed_effect_envelope_digest": source.get(
                "committed_effect_envelope_digest"
            ),
            "frontier_materialization_candidate_id": source.get(
                "invoked_frontier_candidate_id"
            ),
            "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
            "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
            "requested_effect_tags": envelope.get("requested_effect_tags"),
            "state_before": STATE_BEFORE,
            "state_after": STATE_AFTER,
        }
    )


def compute_host_effect_intake_context_digest(context: Mapping[str, Any]) -> str:
    value = dict(context)
    value.pop("host_effect_intake_context_digest", None)
    return canonical_digest(value)


def compute_requested_host_effect_intake_operation_digest(
    source: Mapping[str, Any], host_receipt: Mapping[str, Any]
) -> str:
    return canonical_digest(
        {
            "source_effect_commit_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
            "effect_commit_record_digest": source.get("effect_commit_record_digest"),
            "committed_effect_envelope_digest": source.get(
                "committed_effect_envelope_digest"
            ),
            HOST_RECEIPT_DIGEST_FIELD: host_receipt.get(HOST_RECEIPT_DIGEST_FIELD),
            "host_effect_operation_digest": host_receipt.get(
                "host_effect_operation_digest"
            ),
            "host_effect_outcome": host_receipt.get("host_effect_outcome"),
            "state_before": STATE_BEFORE,
            "state_after": STATE_AFTER,
        }
    )


def compute_exact_host_effect_intake_cycle_digest(
    source: Mapping[str, Any],
    host_receipt: Mapping[str, Any],
    context: Mapping[str, Any],
) -> str:
    return canonical_digest(
        {
            "source_effect_commit_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
            "effect_commit_record_digest": source.get("effect_commit_record_digest"),
            "committed_effect_envelope_digest": source.get(
                "committed_effect_envelope_digest"
            ),
            HOST_RECEIPT_DIGEST_FIELD: host_receipt.get(HOST_RECEIPT_DIGEST_FIELD),
            "host_effect_intake_session_id": context.get(
                "host_effect_intake_session_id"
            ),
            "host_effect_intake_nonce_digest": context.get(
                "host_effect_intake_nonce_digest"
            ),
            "host_effect_intake_epoch": context.get("host_effect_intake_epoch"),
            "current_world_model_revision": context.get(
                "current_world_model_revision"
            ),
            "requested_host_effect_intake_operation_digest": context.get(
                "requested_host_effect_intake_operation_digest"
            ),
        }
    )


def compute_atomic_external_host_effect_bundle_digest(**fields: Any) -> str:
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
) -> tuple[str, dict, dict, dict, list[str], list[str]]:
    if not source:
        blockers.append("source_effect_commit_receipt_missing")
        return "", {}, {}, {}, [], []

    headers = {
        "kernel": "ActOS Dukkha-Preserving Single-Use Effect Commit Intake Kernel",
        "kernel_version": "v0.1",
        "actos_version": "v0.10",
        "status": "ACTOS_DUKKHA_PRESERVING_SINGLE_USE_EFFECT_COMMIT_RECORDED",
        "effect_commit_state_after": STATE_BEFORE,
    }
    for field, value in headers.items():
        if source.get(field) != value:
            blockers.append(f"source_{field}_invalid")

    digest = source.get(SOURCE_DIGEST_FIELD)
    if not isinstance(digest, str) or not digest:
        blockers.append("source_effect_commit_receipt_digest_missing")
        digest = ""
    else:
        unsigned = dict(source)
        unsigned.pop(SOURCE_DIGEST_FIELD, None)
        if digest != canonical_digest(unsigned):
            blockers.append("source_effect_commit_receipt_digest_mismatch")
        if digest != expected_digest:
            blockers.append("source_effect_commit_expected_binding_mismatch")

    for field in SOURCE_TRUE:
        if source.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in SOURCE_FALSE:
        if source.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")

    record_raw = source.get("effect_commit_record")
    record = dict(record_raw) if isinstance(record_raw, Mapping) else {}
    if not record:
        blockers.append("source_effect_commit_record_invalid")
    if source.get("effect_commit_record_digest") != canonical_digest(record):
        blockers.append("source_effect_commit_record_digest_mismatch")
    record_expected = {
        "source_effect_commit_authorization_receipt_digest": source.get(
            "source_effect_commit_authorization_receipt_digest"
        ),
        "source_invocation_receipt_digest": source.get(
            "source_invocation_receipt_digest"
        ),
        "effect_commit_authorization_record_digest": source.get(
            "source_effect_commit_authorization_record_digest"
        ),
        "effect_commit_authorization_token_digest": source.get(
            "source_effect_commit_authorization_token_digest"
        ),
        "adapter_result_envelope_digest": source.get(
            "source_adapter_result_envelope_digest"
        ),
        "invoked_frontier_candidate_id": source.get(
            "invoked_frontier_candidate_id"
        ),
        "invoked_frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
        "invoked_frontier_binding_digest": source.get(
            "invoked_frontier_binding_digest"
        ),
        "state_before": "authorized_not_committed",
        "state_after": STATE_BEFORE,
        "commit_outcome": "bounded_effect_committed_pending_external_host_effect",
    }
    for field, value in record_expected.items():
        if record.get(field) != value:
            blockers.append(f"source_effect_commit_record_{field}_mismatch")

    envelope_raw = source.get("committed_effect_envelope")
    envelope = dict(envelope_raw) if isinstance(envelope_raw, Mapping) else {}
    if not envelope:
        blockers.append("source_committed_effect_envelope_invalid")
    if source.get("committed_effect_envelope_digest") != canonical_digest(envelope):
        blockers.append("source_committed_effect_envelope_digest_mismatch")
    envelope_expected = {
        "frontier_materialization_candidate_id": source.get(
            "invoked_frontier_candidate_id"
        ),
        "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
        "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
        "source_adapter_result_envelope_digest": source.get(
            "source_adapter_result_envelope_digest"
        ),
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
    for field, value in envelope_expected.items():
        if envelope.get(field) != value:
            blockers.append(f"source_committed_effect_envelope_{field}_mismatch")
    effects_ok, _ = _strings(envelope.get("requested_effect_tags"), True)
    if not effects_ok:
        blockers.append("source_requested_effect_tags_invalid")

    consumption_raw = source.get("authorization_consumption_record")
    consumption = (
        dict(consumption_raw) if isinstance(consumption_raw, Mapping) else {}
    )
    if not consumption:
        blockers.append("source_authorization_consumption_record_invalid")
    if source.get("authorization_consumption_record_digest") != canonical_digest(
        consumption
    ):
        blockers.append("source_authorization_consumption_record_digest_mismatch")
    if consumption.get("authorization_consumed") is not True:
        blockers.append("source_authorization_not_consumed")
    if consumption.get("token_marked_consumed") is not True:
        blockers.append("source_authorization_token_not_marked_consumed")
    if consumption.get("double_consumption_performed") is not False:
        blockers.append("source_authorization_double_consumption_promoted")

    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_resulting_responsibility_invalid")
    return digest, record, envelope, consumption, lineage, responsibility


def _verify_host_receipt(
    host_receipt: dict,
    expected_digest: str,
    source: dict,
    blockers: list[str],
) -> tuple[str, bool]:
    if not host_receipt:
        blockers.append("external_host_effect_application_receipt_missing")
        return "", False
    if set(host_receipt) != HOST_RECEIPT_FIELDS:
        blockers.append("external_host_effect_application_receipt_schema_invalid")

    digest = host_receipt.get(HOST_RECEIPT_DIGEST_FIELD)
    if not isinstance(digest, str) or not digest:
        blockers.append("external_host_effect_application_receipt_digest_missing")
        digest = ""
    else:
        if digest != compute_external_host_effect_application_receipt_digest(
            host_receipt
        ):
            blockers.append("external_host_effect_application_receipt_digest_mismatch")
        if digest != expected_digest:
            blockers.append(
                "external_host_effect_application_receipt_expected_binding_mismatch"
            )

    envelope = source.get("committed_effect_envelope")
    envelope = dict(envelope) if isinstance(envelope, Mapping) else {}
    exact = {
        "source_effect_commit_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        "effect_commit_record_digest": source.get("effect_commit_record_digest"),
        "committed_effect_envelope_digest": source.get(
            "committed_effect_envelope_digest"
        ),
        "frontier_materialization_candidate_id": source.get(
            "invoked_frontier_candidate_id"
        ),
        "frontier_adapter_id": source.get("invoked_frontier_adapter_id"),
        "frontier_binding_digest": source.get("invoked_frontier_binding_digest"),
        "requested_effect_tags": envelope.get("requested_effect_tags"),
        "host_effect_operation_digest": compute_host_effect_operation_digest(source),
        "host_effect_outcome": HOST_OUTCOME,
        "exactly_one_effect_applied": True,
        "tool_invocation_performed": True,
        "external_side_effect_performed": True,
    }
    for field, value in exact.items():
        if host_receipt.get(field) != value:
            blockers.append(f"external_host_effect_application_{field}_mismatch")

    for field in (
        "host_effect_session_id",
        "host_effect_nonce_digest",
        "host_driver_id",
        "host_target_digest",
        "compensation_route_digest",
        "observation_route_digest",
        "verification_route_digest",
    ):
        if not isinstance(host_receipt.get(field), str) or not host_receipt.get(field):
            blockers.append(f"external_host_effect_application_{field}_invalid")

    for field in (
        "host_effect_started_epoch",
        "host_effect_completed_epoch",
        "maximum_host_effect_duration",
    ):
        value = host_receipt.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"external_host_effect_application_{field}_invalid")
    maximum = host_receipt.get("maximum_host_effect_duration")
    if not isinstance(maximum, int) or isinstance(maximum, bool) or not 1 <= maximum <= 64:
        blockers.append("external_host_effect_application_duration_bound_invalid")
    started = host_receipt.get("host_effect_started_epoch")
    completed = host_receipt.get("host_effect_completed_epoch")
    duration_current = all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in (started, completed, maximum)
    ) and 0 <= completed - started <= maximum
    if not duration_current:
        blockers.append("external_host_effect_application_duration_invalid")
    return digest, duration_current


def _verify_context(
    context: dict,
    expected_digest: str,
    source: dict,
    host_receipt: dict,
    blockers: list[str],
) -> tuple[str, bool, bool, bool, bool, bool, bool]:
    if not context:
        blockers.append("host_effect_intake_context_missing")
        return "", False, False, False, False, False, False
    if set(context) != CONTEXT_FIELDS:
        blockers.append("host_effect_intake_context_schema_invalid")

    digest = context.get("host_effect_intake_context_digest")
    if not isinstance(digest, str) or not digest:
        blockers.append("host_effect_intake_context_digest_missing")
        digest = ""
    else:
        if digest != compute_host_effect_intake_context_digest(context):
            blockers.append("host_effect_intake_context_digest_mismatch")
        if digest != expected_digest:
            blockers.append("host_effect_intake_context_expected_binding_mismatch")

    string_fields = CONTEXT_FIELDS - {
        "current_world_model_revision",
        "source_commit_receipt_observed_epoch",
        "host_effect_intake_epoch",
        "maximum_host_effect_intake_delay",
        "prior_host_effect_intake_session_ids",
        "prior_host_effect_application_receipt_digests",
        "prior_host_effect_intake_nonce_digests",
        "prior_applied_committed_effect_envelope_digests",
        "host_effect_intake_context_digest",
    }
    for field in string_fields:
        if not isinstance(context.get(field), str) or not context.get(field):
            blockers.append(f"host_effect_intake_context_{field}_invalid")
    for field in (
        "current_world_model_revision",
        "source_commit_receipt_observed_epoch",
        "host_effect_intake_epoch",
        "maximum_host_effect_intake_delay",
    ):
        value = context.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"host_effect_intake_context_{field}_invalid")
    delay = context.get("maximum_host_effect_intake_delay")
    if not isinstance(delay, int) or isinstance(delay, bool) or not 1 <= delay <= 64:
        blockers.append("host_effect_intake_context_delay_bound_invalid")

    sessions_ok, sessions = _strings(
        context.get("prior_host_effect_intake_session_ids"), True
    )
    receipts_ok, receipts = _strings(
        context.get("prior_host_effect_application_receipt_digests"), True
    )
    nonces_ok, nonces = _strings(
        context.get("prior_host_effect_intake_nonce_digests"), True
    )
    envelopes_ok, envelopes = _strings(
        context.get("prior_applied_committed_effect_envelope_digests"), True
    )
    if not sessions_ok:
        blockers.append("host_effect_intake_context_sessions_invalid")
    if not receipts_ok:
        blockers.append("host_effect_intake_context_receipts_invalid")
    if not nonces_ok:
        blockers.append("host_effect_intake_context_nonces_invalid")
    if not envelopes_ok:
        blockers.append("host_effect_intake_context_envelopes_invalid")

    exact = {
        "source_effect_commit_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        "effect_commit_record_digest": source.get("effect_commit_record_digest"),
        "committed_effect_envelope_digest": source.get(
            "committed_effect_envelope_digest"
        ),
        HOST_RECEIPT_DIGEST_FIELD: host_receipt.get(HOST_RECEIPT_DIGEST_FIELD),
    }
    for field, value in exact.items():
        if context.get(field) != value:
            blockers.append(f"host_effect_intake_context_{field}_mismatch")

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
        "requested_host_effect_intake_operation_digest"
    ) != compute_requested_host_effect_intake_operation_digest(source, host_receipt):
        blockers.append("host_effect_intake_context_operation_digest_mismatch")
    if context.get(
        "exact_host_effect_intake_cycle_digest"
    ) != compute_exact_host_effect_intake_cycle_digest(source, host_receipt, context):
        blockers.append("host_effect_intake_context_cycle_digest_mismatch")

    observed = context.get("source_commit_receipt_observed_epoch")
    epoch = context.get("host_effect_intake_epoch")
    max_delay = context.get("maximum_host_effect_intake_delay")
    delay_current = all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in (observed, epoch, max_delay)
    ) and 0 <= epoch - observed <= max_delay

    session_fresh = context.get("host_effect_intake_session_id") not in sessions
    receipt_fresh = host_receipt.get(HOST_RECEIPT_DIGEST_FIELD) not in receipts
    nonce_fresh = context.get("host_effect_intake_nonce_digest") not in nonces
    envelope_fresh = source.get("committed_effect_envelope_digest") not in envelopes
    return (
        digest,
        world_current,
        delay_current,
        session_fresh,
        receipt_fresh,
        nonce_fresh,
        envelope_fresh,
    )


def build_actos_dukkha_preserving_atomic_external_host_effect_intake(
    *,
    source_effect_commit_receipt: Mapping[str, Any],
    expected_source_effect_commit_receipt_digest: str,
    external_host_effect_application_receipt: Mapping[str, Any],
    expected_external_host_effect_application_receipt_digest: str,
    host_effect_intake_context: Mapping[str, Any],
    expected_host_effect_intake_context_digest: str,
    host_effect_intake_policy_digest: str,
    actos_host_effect_intake_responsibility_digest: str,
    host_effect_intake_request_id: str,
    atomic_external_host_effect_bundle_digest: str,
) -> ActOSDukkhaPreservingAtomicExternalHostEffectResult:
    blockers: list[str] = []
    source = dict(source_effect_commit_receipt) if isinstance(
        source_effect_commit_receipt, Mapping
    ) else {}
    host_receipt = dict(external_host_effect_application_receipt) if isinstance(
        external_host_effect_application_receipt, Mapping
    ) else {}
    context = dict(host_effect_intake_context) if isinstance(
        host_effect_intake_context, Mapping
    ) else {}

    for name, value in {
        "expected_source_effect_commit_receipt_digest": (
            expected_source_effect_commit_receipt_digest
        ),
        "expected_external_host_effect_application_receipt_digest": (
            expected_external_host_effect_application_receipt_digest
        ),
        "expected_host_effect_intake_context_digest": (
            expected_host_effect_intake_context_digest
        ),
        "host_effect_intake_policy_digest": host_effect_intake_policy_digest,
        "actos_host_effect_intake_responsibility_digest": (
            actos_host_effect_intake_responsibility_digest
        ),
        "host_effect_intake_request_id": host_effect_intake_request_id,
        "atomic_external_host_effect_bundle_digest": (
            atomic_external_host_effect_bundle_digest
        ),
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    (
        source_digest,
        commit_record,
        committed_envelope,
        authorization_consumption,
        lineage,
        responsibility,
    ) = _verify_source(source, expected_source_effect_commit_receipt_digest, blockers)
    host_receipt_digest, host_duration_current = _verify_host_receipt(
        host_receipt,
        expected_external_host_effect_application_receipt_digest,
        source,
        blockers,
    )
    (
        context_digest,
        world_current,
        delay_current,
        session_fresh,
        receipt_fresh,
        nonce_fresh,
        envelope_fresh,
    ) = _verify_context(
        context,
        expected_host_effect_intake_context_digest,
        source,
        host_receipt,
        blockers,
    )

    if not host_duration_current:
        blockers.append("external_host_effect_application_not_current")
    if not world_current:
        blockers.append("host_effect_intake_world_refresh_required")
    if not delay_current:
        blockers.append("host_effect_intake_expired")
    if not session_fresh:
        blockers.append("host_effect_intake_session_replay_rejected")
    if not receipt_fresh:
        blockers.append("host_effect_application_receipt_replay_rejected")
    if not nonce_fresh:
        blockers.append("host_effect_intake_nonce_replay_rejected")
    if not envelope_fresh:
        blockers.append("committed_effect_envelope_replay_rejected")

    if not blockers:
        expected_bundle = compute_atomic_external_host_effect_bundle_digest(
            source_effect_commit_receipt_digest=source_digest,
            expected_source_effect_commit_receipt_digest=(
                expected_source_effect_commit_receipt_digest
            ),
            effect_commit_record_digest=source.get("effect_commit_record_digest"),
            committed_effect_envelope_digest=source.get(
                "committed_effect_envelope_digest"
            ),
            authorization_consumption_record_digest=source.get(
                "authorization_consumption_record_digest"
            ),
            external_host_effect_application_receipt_digest=host_receipt_digest,
            expected_external_host_effect_application_receipt_digest=(
                expected_external_host_effect_application_receipt_digest
            ),
            host_effect_intake_context_digest=context_digest,
            expected_host_effect_intake_context_digest=(
                expected_host_effect_intake_context_digest
            ),
            requested_host_effect_intake_operation_digest=context.get(
                "requested_host_effect_intake_operation_digest"
            ),
            exact_host_effect_intake_cycle_digest=context.get(
                "exact_host_effect_intake_cycle_digest"
            ),
            host_effect_intake_policy_digest=host_effect_intake_policy_digest,
            actos_host_effect_intake_responsibility_digest=(
                actos_host_effect_intake_responsibility_digest
            ),
            host_effect_intake_request_id=host_effect_intake_request_id,
        )
        if atomic_external_host_effect_bundle_digest != expected_bundle:
            blockers.append("atomic_external_host_effect_bundle_digest_mismatch")

    if blockers:
        return ActOSDukkhaPreservingAtomicExternalHostEffectResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    external_host_effect_record = {
        "source_effect_commit_receipt_digest": source_digest,
        "effect_commit_record_digest": source["effect_commit_record_digest"],
        "committed_effect_envelope_digest": source[
            "committed_effect_envelope_digest"
        ],
        "external_host_effect_application_receipt_digest": host_receipt_digest,
        "frontier_materialization_candidate_id": source[
            "invoked_frontier_candidate_id"
        ],
        "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "host_effect_intake_session_id": context["host_effect_intake_session_id"],
        "host_effect_intake_nonce_digest": context[
            "host_effect_intake_nonce_digest"
        ],
        "requested_host_effect_intake_operation_digest": context[
            "requested_host_effect_intake_operation_digest"
        ],
        "exact_host_effect_intake_cycle_digest": context[
            "exact_host_effect_intake_cycle_digest"
        ],
        "host_effect_intake_epoch": context["host_effect_intake_epoch"],
        "state_before": STATE_BEFORE,
        "state_after": STATE_AFTER,
        "intake_outcome": INTAKE_OUTCOME,
    }
    external_host_effect_record_digest = canonical_digest(external_host_effect_record)

    committed_effect_consumption_record = {
        "committed_effect_envelope_digest": source[
            "committed_effect_envelope_digest"
        ],
        "source_effect_commit_receipt_digest": source_digest,
        "external_host_effect_application_receipt_digest": host_receipt_digest,
        "external_host_effect_record_digest": external_host_effect_record_digest,
        "committed_effect_consumed": True,
        "committed_effect_marked_applied": True,
        "double_application_performed": False,
    }
    committed_effect_consumption_record_digest = canonical_digest(
        committed_effect_consumption_record
    )

    observation_handoff_envelope = {
        "source_effect_commit_receipt_digest": source_digest,
        "committed_effect_envelope_digest": source[
            "committed_effect_envelope_digest"
        ],
        "external_host_effect_application_receipt_digest": host_receipt_digest,
        "external_host_effect_record_digest": external_host_effect_record_digest,
        "frontier_materialization_candidate_id": source[
            "invoked_frontier_candidate_id"
        ],
        "frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "frontier_binding_digest": source["invoked_frontier_binding_digest"],
        "requested_effect_tags": list(committed_envelope["requested_effect_tags"]),
        "host_effect_state": "applied_unobserved",
        "observation_state": "not_observed",
        "verification_state": "verification_debt_open",
        "observation_intake_admitted": True,
        "observation_receipt_required": True,
        "verification_intake_required": True,
        "verification_intake_admitted": False,
        "compensation_route_ready": True,
    }
    observation_handoff_envelope_digest = canonical_digest(
        observation_handoff_envelope
    )

    resulting_lineage = sorted(
        set(lineage)
        | {
            source_digest,
            source["effect_commit_record_digest"],
            source["committed_effect_envelope_digest"],
            source["authorization_consumption_record_digest"],
            host_receipt_digest,
            context_digest,
            context["requested_host_effect_intake_operation_digest"],
            context["exact_host_effect_intake_cycle_digest"],
            external_host_effect_record_digest,
            committed_effect_consumption_record_digest,
            observation_handoff_envelope_digest,
            atomic_external_host_effect_bundle_digest,
        }
    )
    resulting_responsibility = sorted(
        set(responsibility)
        | {
            host_receipt["host_driver_id"],
            actos_host_effect_intake_responsibility_digest,
        }
    )

    receipt = {
        "kernel": "ActOS Dukkha-Preserving Atomic External Host-Effect Intake Kernel",
        "kernel_version": "v0.1",
        "actos_version": "v0.11",
        "status": "ACTOS_DUKKHA_PRESERVING_ATOMIC_EXTERNAL_HOST_EFFECT_RECORDED",
        "source_effect_commit_receipt_digest": source_digest,
        "source_effect_commit_authorization_receipt_digest": source[
            "source_effect_commit_authorization_receipt_digest"
        ],
        "source_invocation_receipt_digest": source[
            "source_invocation_receipt_digest"
        ],
        "source_activation_receipt_digest": source["source_activation_receipt_digest"],
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
        "source_effect_commit_record_digest": source[
            "effect_commit_record_digest"
        ],
        "source_committed_effect_envelope_digest": source[
            "committed_effect_envelope_digest"
        ],
        "source_authorization_consumption_record_digest": source[
            "authorization_consumption_record_digest"
        ],
        "external_host_effect_application_receipt": host_receipt,
        "external_host_effect_application_receipt_digest": host_receipt_digest,
        "host_effect_intake_context_digest": context_digest,
        "host_effect_intake_policy_digest": host_effect_intake_policy_digest,
        "actos_host_effect_intake_responsibility_digest": (
            actos_host_effect_intake_responsibility_digest
        ),
        "host_effect_intake_request_id": host_effect_intake_request_id,
        "atomic_external_host_effect_bundle_digest": (
            atomic_external_host_effect_bundle_digest
        ),
        "invoked_frontier_candidate_id": source[
            "invoked_frontier_candidate_id"
        ],
        "invoked_frontier_adapter_id": source["invoked_frontier_adapter_id"],
        "invoked_frontier_binding_digest": source[
            "invoked_frontier_binding_digest"
        ],
        "invoked_frontier_lease_id": source["invoked_frontier_lease_id"],
        "host_effect_state_before": STATE_BEFORE,
        "host_effect_state_after": STATE_AFTER,
        "external_host_effect_record": external_host_effect_record,
        "external_host_effect_record_digest": external_host_effect_record_digest,
        "committed_effect_consumption_record": committed_effect_consumption_record,
        "committed_effect_consumption_record_digest": (
            committed_effect_consumption_record_digest
        ),
        "observation_handoff_envelope": observation_handoff_envelope,
        "observation_handoff_envelope_digest": observation_handoff_envelope_digest,
        "external_host_effect_application_receipt_supplied": True,
        "canonical_host_effect_receipt_bound": True,
        "committed_effect_envelope_consumed": True,
        "committed_effect_envelope_marked_applied": True,
        "committed_effect_envelope_replay_closed": True,
        "committed_effect_envelope_double_applied": False,
        "host_effect_application_receipt_replay_closed": True,
        "host_effect_intake_nonce_consumed": True,
        "host_effect_intake_nonce_replay_closed": True,
        "source_effect_commit_replay_closed": True,
        "host_effect_intake_session_replay_fresh_before_intake": True,
        "host_effect_application_receipt_replay_fresh_before_intake": True,
        "host_effect_intake_nonce_replay_fresh_before_intake": True,
        "committed_effect_envelope_replay_fresh_before_application": True,
        "world_conditions_current": True,
        "host_effect_application_duration_current": True,
        "host_effect_intake_delay_current": True,
        "exactly_one_external_host_effect_recorded": True,
        "external_host_effect_receipt_issued": True,
        "external_host_effect_performed": True,
        "host_driver_tool_invocation_performed": True,
        "host_driver_external_side_effect_performed": True,
        "kernel_tool_invocation_performed": False,
        "kernel_external_side_effect_performed": False,
        "tool_invocation_performed": True,
        "external_side_effect_performed": True,
        "persistent_host_state_changed": True,
        "persistent_world_model_state_unchanged": True,
        "world_fact_confirmed": False,
        "causal_attribution_confirmed": False,
        "observation_intake_admitted": True,
        "observation_receipt_required": True,
        "observation_performed": False,
        "independent_world_evidence_present": False,
        "verification_intake_required": True,
        "verification_intake_admitted": False,
        "verification_completed": False,
        "verification_debt_open": True,
        "compensation_route_ready": True,
        "compensation_performed": False,
        "automatic_truth_promotion": False,
        "automatic_plan_completion": False,
        "automatic_rollback": False,
        "effect_scope_preserved": True,
        "effect_ceiling_preserved": True,
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
        "bounded_host_effect_authority_consumed": True,
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
    return ActOSDukkhaPreservingAtomicExternalHostEffectResult(
        STATUS_READY, [], receipt
    )
