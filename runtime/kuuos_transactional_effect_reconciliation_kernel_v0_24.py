from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_act_os_kernel_v0_1 import validate_act_state
from runtime.kuuos_act_os_types_v0_1 import authorization_digest
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import (
    BLOCKED as HOST_BLOCKED,
    READY as HOST_READY,
    REPLAYED as HOST_REPLAYED,
    license_digest,
    projection_digest,
    receipt_digest as host_receipt_digest,
)
from runtime.kuuos_observe_os_kernel_v0_1 import validate_observe_state
from runtime.kuuos_verify_os_kernel_v0_1 import validate_verify_state
from runtime.kuuos_transactional_effect_types_v0_24 import (
    APPLY_RESULT_VERSION,
    COMPENSATION_MODES,
    COMPENSATION_REQUEST_VERSION,
    CONNECTOR_CONTRACT_VERSION,
    DECISION_VERSION,
    EVENT_VERSION,
    FINAL_RECEIPT_VERSION,
    INTENT_VERSION,
    NON_AUTHORITY_FLAGS,
    PHASES,
    RECONCILIATION_VERDICTS,
    RECONCILIATION_VERSION,
    REQUIRED_BOUNDARY,
    STATE_VERSION,
    TRANSACTION_ROUTES,
    apply_result_digest,
    compensation_request_digest,
    connector_contract_digest,
    copy_boundary,
    copy_non_authority,
    decision_digest,
    event_digest,
    final_receipt_digest,
    intent_digest,
    reconciliation_digest,
    require_bool,
    require_int,
    require_string,
    state_digest,
    unique_strings,
)


def build_connector_contract(
    *,
    connector_id: str,
    adapter_kind: str,
    trusted_registry_entry_digest: str,
    operation_allowlist: list[str],
    compensation_mode: str,
    compensation_operation_allowlist: list[str],
    observation_channel_ids: list[str],
) -> dict[str, Any]:
    mode = require_string(compensation_mode, "compensation_mode")
    if mode not in COMPENSATION_MODES:
        raise ValueError("compensation_mode_invalid")
    operations = unique_strings(operation_allowlist, "operation_allowlist")
    compensation_operations = unique_strings(
        compensation_operation_allowlist,
        "compensation_operation_allowlist",
        allow_empty=True,
    )
    if mode == "explicit_operation" and not compensation_operations:
        raise ValueError("explicit_compensation_operation_required")
    if mode != "explicit_operation" and compensation_operations:
        raise ValueError("compensation_operation_forbidden_for_mode")
    packet = {
        "version": CONNECTOR_CONTRACT_VERSION,
        "connector_id": require_string(connector_id, "connector_id"),
        "adapter_kind": require_string(adapter_kind, "adapter_kind"),
        "trusted_registry_entry_digest": require_string(
            trusted_registry_entry_digest, "trusted_registry_entry_digest"
        ),
        "operation_allowlist": operations,
        "compensation_mode": mode,
        "compensation_operation_allowlist": compensation_operations,
        "observation_channel_ids": unique_strings(
            observation_channel_ids, "observation_channel_ids"
        ),
        "supports_idempotency": True,
        "supports_exact_input_binding": True,
        "supports_exact_effect_receipts": True,
        "supports_world_observation": True,
        "connector_call_requires_actos": True,
        "connector_contract_read_only": True,
        "hidden_connector_call_forbidden": True,
        "direct_connector_call_performed": False,
        "non_authority": copy_non_authority(),
        "connector_contract_digest": "",
    }
    packet["connector_contract_digest"] = connector_contract_digest(packet)
    errors = validate_connector_contract(packet)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_connector_contract(contract: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if contract.get("version") != CONNECTOR_CONTRACT_VERSION:
            errors.append("connector_contract_version_invalid")
        for field in (
            "connector_id",
            "adapter_kind",
            "trusted_registry_entry_digest",
        ):
            require_string(contract.get(field), field)
        operations = unique_strings(contract.get("operation_allowlist"), "operation_allowlist")
        mode = require_string(contract.get("compensation_mode"), "compensation_mode")
        if mode not in COMPENSATION_MODES:
            errors.append("connector_compensation_mode_invalid")
        compensation_operations = unique_strings(
            contract.get("compensation_operation_allowlist"),
            "compensation_operation_allowlist",
            allow_empty=True,
        )
        if mode == "explicit_operation" and not compensation_operations:
            errors.append("connector_explicit_compensation_missing")
        if mode != "explicit_operation" and compensation_operations:
            errors.append("connector_compensation_operation_mode_mismatch")
        if set(compensation_operations) - set(operations):
            errors.append("connector_compensation_operation_not_allowlisted")
        unique_strings(contract.get("observation_channel_ids"), "observation_channel_ids")
        for field in (
            "supports_idempotency",
            "supports_exact_input_binding",
            "supports_exact_effect_receipts",
            "supports_world_observation",
            "connector_call_requires_actos",
            "connector_contract_read_only",
            "hidden_connector_call_forbidden",
        ):
            if contract.get(field) is not True:
                errors.append(f"connector_{field}_required")
        if contract.get("direct_connector_call_performed") is not False:
            errors.append("connector_direct_call_forbidden")
        if dict(contract.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("connector_authority_escalation")
        if contract.get("connector_contract_digest") != connector_contract_digest(
            contract
        ):
            errors.append("connector_contract_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_transaction_intent(
    *,
    transaction_id: str,
    prepared_act_state: Mapping[str, Any],
    connector_contract: Mapping[str, Any],
    intended_effect_digest: str,
    idempotency_key: str,
    timeout_ms: int,
    max_retries: int,
    compensation_operation_id: str = "",
    compensation_input_digest: str = "",
    noncompensability_reason_digest: str = "",
    prepared_at_ms: int,
) -> dict[str, Any]:
    act_errors = validate_act_state(prepared_act_state)
    if act_errors:
        raise ValueError("invalid_prepared_act_state:" + ";".join(act_errors))
    if prepared_act_state.get("current_phase") != "project":
        raise ValueError("transaction_prepare_requires_act_project_phase")
    if prepared_act_state.get("route") != "PENDING":
        raise ValueError("transaction_prepare_requires_pending_act")
    contract_errors = validate_connector_contract(connector_contract)
    if contract_errors:
        raise ValueError("invalid_connector_contract:" + ";".join(contract_errors))

    operation_id = require_string(prepared_act_state.get("operation_id"), "operation_id")
    if operation_id not in set(connector_contract.get("operation_allowlist", [])):
        raise ValueError("transaction_operation_not_connector_allowlisted")
    authorization = prepared_act_state.get("step_authorization")
    host_license = prepared_act_state.get("host_license")
    projection = prepared_act_state.get("host_projection")
    if not isinstance(authorization, Mapping):
        raise ValueError("transaction_step_authorization_missing")
    if not isinstance(host_license, Mapping):
        raise ValueError("transaction_host_license_missing")
    if not isinstance(projection, Mapping):
        raise ValueError("transaction_host_projection_missing")
    if authorization.get("step_authorization_digest") != authorization_digest(
        authorization
    ):
        raise ValueError("transaction_step_authorization_digest_invalid")
    if host_license.get("host_license_digest") != license_digest(host_license):
        raise ValueError("transaction_host_license_digest_invalid")
    if projection.get("projection_digest") != projection_digest(projection):
        raise ValueError("transaction_host_projection_digest_invalid")

    key = require_string(idempotency_key, "idempotency_key")
    if key != authorization.get("invocation_id"):
        raise ValueError("transaction_idempotency_key_must_bind_lower_invocation")
    prepared = require_int(prepared_at_ms, "prepared_at_ms")
    if prepared >= int(authorization.get("expires_at_ms", 0)):
        raise ValueError("transaction_prepare_after_authorization_expiry")
    if prepared >= int(host_license.get("expires_at_ms", 0)):
        raise ValueError("transaction_prepare_after_capability_lease_expiry")
    timeout = require_int(timeout_ms, "timeout_ms")
    if timeout < 1:
        raise ValueError("transaction_timeout_positive_required")
    retries = require_int(max_retries, "max_retries")

    mode = str(connector_contract["compensation_mode"])
    compensation_operation = str(compensation_operation_id)
    compensation_input = str(compensation_input_digest)
    noncompensability = str(noncompensability_reason_digest)
    if mode == "explicit_operation":
        require_string(compensation_operation, "compensation_operation_id")
        require_string(compensation_input, "compensation_input_digest")
        if compensation_operation not in set(
            connector_contract.get("compensation_operation_allowlist", [])
        ):
            raise ValueError("transaction_compensation_operation_not_allowlisted")
        if noncompensability:
            raise ValueError("transaction_noncompensability_reason_forbidden")
    else:
        if compensation_operation or compensation_input:
            raise ValueError("transaction_compensation_operation_forbidden")
        require_string(
            noncompensability,
            "noncompensability_reason_digest",
        )

    packet = {
        "version": INTENT_VERSION,
        "transaction_id": require_string(transaction_id, "transaction_id"),
        "lineage_id": require_string(prepared_act_state.get("lineage_id"), "lineage_id"),
        "source_act_id": require_string(prepared_act_state.get("act_id"), "source_act_id"),
        "source_prepared_act_state_digest": require_string(
            prepared_act_state.get("act_state_digest"),
            "source_prepared_act_state_digest",
        ),
        "source_plan_state_digest": require_string(
            prepared_act_state.get("source_plan_state_digest"),
            "source_plan_state_digest",
        ),
        "source_committed_plan_digest": require_string(
            prepared_act_state.get("source_committed_plan_digest"),
            "source_committed_plan_digest",
        ),
        "mission_contract_digest": require_string(
            prepared_act_state.get("mission_contract_digest"),
            "mission_contract_digest",
        ),
        "selected_step_id": require_string(
            prepared_act_state.get("selected_step_id"), "selected_step_id"
        ),
        "selected_step_digest": require_string(
            prepared_act_state.get("selected_step_digest"), "selected_step_digest"
        ),
        "operation_id": operation_id,
        "operation_input_digest": require_string(
            prepared_act_state.get("operation_input_digest"),
            "operation_input_digest",
        ),
        "intended_effect_digest": require_string(
            intended_effect_digest, "intended_effect_digest"
        ),
        "expected_observation_digest": require_string(
            prepared_act_state.get("expected_observation_digest"),
            "expected_observation_digest",
        ),
        "verification_criterion_digest": require_string(
            prepared_act_state.get("verification_criterion_digest"),
            "verification_criterion_digest",
        ),
        "connector_id": connector_contract["connector_id"],
        "connector_contract_digest": connector_contract[
            "connector_contract_digest"
        ],
        "step_authorization_digest": authorization["step_authorization_digest"],
        "capability_lease_digest": host_license["host_license_digest"],
        "host_projection_digest": projection["projection_digest"],
        "source_supervisor_bundle_digest": require_string(
            prepared_act_state.get("source_supervisor_bundle_digest"),
            "source_supervisor_bundle_digest",
        ),
        "idempotency_key": key,
        "timeout_ms": timeout,
        "max_retries": retries,
        "retry_requires_same_idempotency_key": True,
        "compensation_mode": mode,
        "compensation_operation_id": compensation_operation,
        "compensation_input_digest": compensation_input,
        "noncompensability_reason_digest": noncompensability,
        "prepared_at_ms": prepared,
        "prepare_performed_before_effect": True,
        "connector_call_performed_by_prepare": False,
        "exact_input_binding": True,
        "exact_capability_lease_binding": True,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "transaction_intent_digest": "",
    }
    packet["transaction_intent_digest"] = intent_digest(packet)
    errors = validate_transaction_intent(packet, connector_contract)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_transaction_intent(
    intent: Mapping[str, Any], connector_contract: Mapping[str, Any]
) -> list[str]:
    errors = [
        "connector:" + item for item in validate_connector_contract(connector_contract)
    ]
    try:
        if intent.get("version") != INTENT_VERSION:
            errors.append("transaction_intent_version_invalid")
        for field in (
            "transaction_id",
            "lineage_id",
            "source_act_id",
            "source_prepared_act_state_digest",
            "source_plan_state_digest",
            "source_committed_plan_digest",
            "mission_contract_digest",
            "selected_step_id",
            "selected_step_digest",
            "operation_id",
            "operation_input_digest",
            "intended_effect_digest",
            "expected_observation_digest",
            "verification_criterion_digest",
            "connector_id",
            "connector_contract_digest",
            "step_authorization_digest",
            "capability_lease_digest",
            "host_projection_digest",
            "source_supervisor_bundle_digest",
            "idempotency_key",
        ):
            require_string(intent.get(field), field)
        if intent.get("connector_id") != connector_contract.get("connector_id"):
            errors.append("transaction_connector_id_mismatch")
        if intent.get("connector_contract_digest") != connector_contract.get(
            "connector_contract_digest"
        ):
            errors.append("transaction_connector_contract_mismatch")
        if intent.get("operation_id") not in set(
            connector_contract.get("operation_allowlist", [])
        ):
            errors.append("transaction_operation_not_allowlisted")
        for field in ("timeout_ms", "max_retries", "prepared_at_ms"):
            require_int(intent.get(field), field)
        if int(intent.get("timeout_ms", 0)) < 1:
            errors.append("transaction_timeout_invalid")
        if intent.get("retry_requires_same_idempotency_key") is not True:
            errors.append("transaction_retry_idempotency_boundary_invalid")
        if intent.get("prepare_performed_before_effect") is not True:
            errors.append("transaction_prepare_order_invalid")
        if intent.get("connector_call_performed_by_prepare") is not False:
            errors.append("transaction_hidden_prepare_call_forbidden")
        if intent.get("exact_input_binding") is not True:
            errors.append("transaction_exact_input_binding_missing")
        if intent.get("exact_capability_lease_binding") is not True:
            errors.append("transaction_capability_lease_binding_missing")
        mode = str(intent.get("compensation_mode", ""))
        if mode != connector_contract.get("compensation_mode"):
            errors.append("transaction_compensation_mode_mismatch")
        if mode == "explicit_operation":
            require_string(
                intent.get("compensation_operation_id"),
                "compensation_operation_id",
            )
            require_string(
                intent.get("compensation_input_digest"),
                "compensation_input_digest",
            )
            if intent.get("compensation_operation_id") not in set(
                connector_contract.get("compensation_operation_allowlist", [])
            ):
                errors.append("transaction_compensation_not_allowlisted")
            if intent.get("noncompensability_reason_digest"):
                errors.append("transaction_noncompensability_reason_forbidden")
        else:
            if intent.get("compensation_operation_id") or intent.get(
                "compensation_input_digest"
            ):
                errors.append("transaction_compensation_operation_forbidden")
            require_string(
                intent.get("noncompensability_reason_digest"),
                "noncompensability_reason_digest",
            )
        if dict(intent.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("transaction_intent_authority_escalation")
        if dict(intent.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("transaction_intent_boundary_invalid")
        if intent.get("transaction_intent_digest") != intent_digest(intent):
            errors.append("transaction_intent_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_initial_transaction_state(
    *,
    intent: Mapping[str, Any],
    connector_contract: Mapping[str, Any],
    prepared_act_state: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_transaction_intent(intent, connector_contract)
    if errors:
        raise ValueError("invalid_transaction_intent:" + ";".join(errors))
    act_errors = validate_act_state(prepared_act_state)
    if act_errors:
        raise ValueError("invalid_prepared_act_state:" + ";".join(act_errors))
    if prepared_act_state.get("current_phase") != "project":
        raise ValueError("initial_transaction_requires_projected_act")
    checks = {
        "act_id": intent["source_act_id"],
        "act_state_digest": intent["source_prepared_act_state_digest"],
        "lineage_id": intent["lineage_id"],
        "operation_id": intent["operation_id"],
        "operation_input_digest": intent["operation_input_digest"],
        "selected_step_id": intent["selected_step_id"],
        "selected_step_digest": intent["selected_step_digest"],
        "host_license_digest": intent["capability_lease_digest"],
        "host_projection_digest": intent["host_projection_digest"],
    }
    for field, expected in checks.items():
        if prepared_act_state.get(field) != expected:
            raise ValueError(f"initial_transaction_{field}_mismatch")
    state = {
        "version": STATE_VERSION,
        "transaction_id": intent["transaction_id"],
        "lineage_id": intent["lineage_id"],
        "mission_contract_digest": intent["mission_contract_digest"],
        "transaction_intent": deepcopy(dict(intent)),
        "transaction_intent_digest": intent["transaction_intent_digest"],
        "connector_contract": deepcopy(dict(connector_contract)),
        "connector_contract_digest": connector_contract[
            "connector_contract_digest"
        ],
        "current_phase": "prepared",
        "route": "PENDING",
        "event_index": 0,
        "transaction_version": 0,
        "committed_records": 0,
        "updated_at_ms": require_int(now_ms, "now_ms"),
        "predecessor_transaction_state_digest": "",
        "transaction_state_digest": "",
        "final_act_state": {},
        "final_act_state_digest": "",
        "lower_act_route": "",
        "effect_recorded": False,
        "host_receipt_digest": "",
        "host_invocation_digest": "",
        "result_supervisor_bundle_digest": "",
        "slice_digest": "",
        "observe_state": {},
        "observe_state_digest": "",
        "observation_route": "",
        "evidence_packet_digest": "",
        "quality_report_digest": "",
        "comparison_receipt_digest": "",
        "reconciliation_receipt": {},
        "reconciliation_receipt_digest": "",
        "reconciliation_verdict": "",
        "verify_state": {},
        "verify_state_digest": "",
        "verification_route": "",
        "verification_evidence_digest": "",
        "transaction_decision": {},
        "transaction_decision_digest": "",
        "compensation_request": {},
        "compensation_request_digest": "",
        "final_receipt": {},
        "transaction_final_receipt_digest": "",
        "observation_required": False,
        "verification_required": False,
        "reobservation_required": False,
        "corrective_action_required": False,
        "automatic_compensation": False,
        "automatic_rollback": False,
        "automatic_truth_promotion": False,
        "automatic_plan_completion": False,
        "hidden_connector_call_performed": False,
        "processed_event_digests": [],
        "event_history": [],
        "record_summaries": [],
        "append_only": True,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
    }
    state["transaction_state_digest"] = state_digest(state)
    state_errors = validate_transaction_state(state)
    if state_errors:
        raise ValueError("invalid_initial_transaction_state:" + ";".join(state_errors))
    return state


def _next_phase(state: Mapping[str, Any]) -> str | None:
    phase = str(state.get("current_phase", ""))
    if phase == "prepared":
        return "effect_bound"
    if phase == "effect_bound":
        return "observed" if state.get("effect_recorded") is True else "decided"
    if phase == "observed":
        return "reconciled"
    if phase == "reconciled":
        return "verified"
    if phase == "verified":
        return "decided"
    if phase == "decided":
        return "committed"
    return None


def validate_transaction_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("transaction_state_version_invalid")
        for field in (
            "transaction_id",
            "lineage_id",
            "mission_contract_digest",
            "transaction_intent_digest",
            "connector_contract_digest",
        ):
            require_string(state.get(field), field)
        intent = state.get("transaction_intent")
        connector = state.get("connector_contract")
        if not isinstance(intent, Mapping) or not isinstance(connector, Mapping):
            errors.append("transaction_state_contracts_missing")
        else:
            errors.extend(
                "intent:" + item
                for item in validate_transaction_intent(intent, connector)
            )
            if state.get("transaction_intent_digest") != intent.get(
                "transaction_intent_digest"
            ):
                errors.append("transaction_state_intent_digest_mismatch")
            if state.get("connector_contract_digest") != connector.get(
                "connector_contract_digest"
            ):
                errors.append("transaction_state_connector_digest_mismatch")
        if state.get("current_phase") not in PHASES:
            errors.append("transaction_state_phase_invalid")
        if state.get("route") not in TRANSACTION_ROUTES:
            errors.append("transaction_state_route_invalid")
        for field in (
            "event_index",
            "transaction_version",
            "committed_records",
            "updated_at_ms",
        ):
            require_int(state.get(field), field)
        for field in (
            "effect_recorded",
            "observation_required",
            "verification_required",
            "reobservation_required",
            "corrective_action_required",
            "automatic_compensation",
            "automatic_rollback",
            "automatic_truth_promotion",
            "automatic_plan_completion",
            "hidden_connector_call_performed",
            "append_only",
            "memory_overwrite",
        ):
            require_bool(state.get(field), field)
        if state.get("automatic_compensation") is not False:
            errors.append("transaction_automatic_compensation_forbidden")
        if state.get("automatic_rollback") is not False:
            errors.append("transaction_automatic_rollback_forbidden")
        if state.get("automatic_truth_promotion") is not False:
            errors.append("transaction_truth_promotion_forbidden")
        if state.get("automatic_plan_completion") is not False:
            errors.append("transaction_plan_completion_forbidden")
        if state.get("hidden_connector_call_performed") is not False:
            errors.append("transaction_hidden_connector_call_forbidden")
        if state.get("append_only") is not True:
            errors.append("transaction_append_only_required")
        if state.get("memory_overwrite") is not False:
            errors.append("transaction_memory_overwrite_forbidden")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("transaction_state_authority_escalation")
        if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("transaction_state_boundary_invalid")
        processed = list(state.get("processed_event_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("transaction_processed_event_duplicate")
        if len(list(state.get("event_history", []))) != int(
            state.get("event_index", -1)
        ):
            errors.append("transaction_event_history_count_mismatch")
        if state.get("effect_recorded") is True:
            if state.get("lower_act_route") != "EFFECT_RECORDED":
                errors.append("transaction_effect_route_mismatch")
            for field in (
                "final_act_state_digest",
                "host_receipt_digest",
                "host_invocation_digest",
                "result_supervisor_bundle_digest",
                "slice_digest",
            ):
                require_string(state.get(field), field)
            if state.get("observation_required") is not True:
                errors.append("transaction_observation_debt_missing")
            if state.get("verification_required") is not True and state.get(
                "current_phase"
            ) not in {"verified", "decided", "committed"}:
                errors.append("transaction_verification_debt_lost_early")
        if state.get("route") == "NO_EFFECT_RECORDED" and state.get(
            "effect_recorded"
        ) is not False:
            errors.append("transaction_no_effect_route_invalid")
        if state.get("route") == "COMPENSATION_PROPOSED":
            if not state.get("compensation_request_digest"):
                errors.append("transaction_compensation_request_missing")
            if state.get("automatic_compensation") is not False:
                errors.append("transaction_compensation_autoexecution_forbidden")
        if state.get("route") == "EFFECT_CONFIRMED":
            if state.get("reconciliation_verdict") != "EFFECT_CONFIRMED":
                errors.append("transaction_confirmed_reconciliation_mismatch")
            if state.get("verification_route") != "VERIFICATION_PASSED":
                errors.append("transaction_confirmed_verification_mismatch")
        if state.get("current_phase") == "committed":
            if not state.get("transaction_final_receipt_digest"):
                errors.append("transaction_final_receipt_missing")
            if state.get("route") == "PENDING":
                errors.append("transaction_committed_route_pending")
        if state.get("transaction_state_digest") != state_digest(state):
            errors.append("transaction_state_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_transaction_event(
    *,
    state: Mapping[str, Any],
    target_phase: str,
    artifact_digest: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_transaction_state(state)
    if errors:
        raise ValueError("invalid_transaction_state:" + ";".join(errors))
    target = require_string(target_phase, "target_phase")
    expected = _next_phase(state)
    if target != expected:
        raise ValueError("transaction_event_phase_order_invalid")
    event = {
        "version": EVENT_VERSION,
        "transaction_id": state["transaction_id"],
        "lineage_id": state["lineage_id"],
        "expected_transaction_state_digest": state["transaction_state_digest"],
        "source_phase": state["current_phase"],
        "target_phase": target,
        "event_index": int(state["event_index"]) + 1,
        "artifact_digest": require_string(artifact_digest, "artifact_digest"),
        "payload": deepcopy(dict(payload)),
        "created_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "transaction_event_digest": "",
    }
    event["transaction_event_digest"] = event_digest(event)
    return event


def build_world_effect_reconciliation_receipt(
    *,
    state: Mapping[str, Any],
    reconciliation_id: str,
    verdict: str,
    prior_world_state_digest: str,
    observed_world_state_digest: str,
    observed_effect_digest: str,
    independent_world_evidence_digests: list[str],
    independent_source_ids: list[str],
    reconciliation_method_digest: str,
    rationale_digest: str,
    reconciled_at_ms: int,
) -> dict[str, Any]:
    if state.get("current_phase") != "observed":
        raise ValueError("reconciliation_requires_observed_state")
    normalized = require_string(verdict, "verdict")
    if normalized not in RECONCILIATION_VERDICTS:
        raise ValueError("reconciliation_verdict_invalid")
    observation_route = str(state.get("observation_route", ""))
    allowed_by_observation = {
        "OBSERVATION_MATCHED": {"EFFECT_CONFIRMED"},
        "OBSERVATION_DIVERGENT": {
            "EFFECT_PARTIAL",
            "EFFECT_NOT_OBSERVED",
            "EXTERNAL_STATE_CHANGED",
            "COMPENSATION_REQUIRED",
        },
        "OBSERVATION_INCONCLUSIVE": {
            "EFFECT_NOT_OBSERVED",
            "EXTERNAL_STATE_CHANGED",
        },
        "OBSERVATION_CONFLICTED": {
            "EFFECT_CONFLICTED",
            "COMPENSATION_REQUIRED",
        },
    }
    if normalized not in allowed_by_observation.get(observation_route, set()):
        raise ValueError("reconciliation_verdict_observation_route_mismatch")
    evidence = unique_strings(
        independent_world_evidence_digests,
        "independent_world_evidence_digests",
    )
    sources = unique_strings(independent_source_ids, "independent_source_ids")
    if len(sources) < 2:
        raise ValueError("reconciliation_independent_sources_insufficient")
    if normalized == "EFFECT_CONFIRMED" and observed_effect_digest != state[
        "transaction_intent"
    ]["intended_effect_digest"]:
        raise ValueError("confirmed_effect_digest_mismatch")
    packet = {
        "version": RECONCILIATION_VERSION,
        "reconciliation_id": require_string(
            reconciliation_id, "reconciliation_id"
        ),
        "transaction_id": state["transaction_id"],
        "transaction_intent_digest": state["transaction_intent_digest"],
        "final_act_state_digest": state["final_act_state_digest"],
        "host_receipt_digest": state["host_receipt_digest"],
        "host_invocation_digest": state["host_invocation_digest"],
        "observe_state_digest": state["observe_state_digest"],
        "comparison_receipt_digest": state["comparison_receipt_digest"],
        "intended_effect_digest": state["transaction_intent"][
            "intended_effect_digest"
        ],
        "prior_world_state_digest": require_string(
            prior_world_state_digest, "prior_world_state_digest"
        ),
        "observed_world_state_digest": require_string(
            observed_world_state_digest, "observed_world_state_digest"
        ),
        "observed_effect_digest": require_string(
            observed_effect_digest, "observed_effect_digest"
        ),
        "independent_world_evidence_digests": evidence,
        "independent_source_ids": sources,
        "reconciliation_method_digest": require_string(
            reconciliation_method_digest, "reconciliation_method_digest"
        ),
        "rationale_digest": require_string(rationale_digest, "rationale_digest"),
        "verdict": normalized,
        "tool_receipt_only": False,
        "world_observation_performed": True,
        "observation_is_verification": False,
        "reconciliation_is_truth": False,
        "causal_attribution_granted": False,
        "compensation_required": normalized == "COMPENSATION_REQUIRED",
        "reconciled_at_ms": require_int(reconciled_at_ms, "reconciled_at_ms"),
        "non_authority": copy_non_authority(),
        "reconciliation_receipt_digest": "",
    }
    packet["reconciliation_receipt_digest"] = reconciliation_digest(packet)
    errors = validate_reconciliation_receipt(packet, state)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_reconciliation_receipt(
    receipt: Mapping[str, Any], state: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != RECONCILIATION_VERSION:
            errors.append("reconciliation_version_invalid")
        for field in (
            "reconciliation_id",
            "transaction_id",
            "transaction_intent_digest",
            "final_act_state_digest",
            "host_receipt_digest",
            "host_invocation_digest",
            "observe_state_digest",
            "comparison_receipt_digest",
            "intended_effect_digest",
            "prior_world_state_digest",
            "observed_world_state_digest",
            "observed_effect_digest",
            "reconciliation_method_digest",
            "rationale_digest",
        ):
            require_string(receipt.get(field), field)
        bindings = {
            "transaction_id": state.get("transaction_id"),
            "transaction_intent_digest": state.get("transaction_intent_digest"),
            "final_act_state_digest": state.get("final_act_state_digest"),
            "host_receipt_digest": state.get("host_receipt_digest"),
            "host_invocation_digest": state.get("host_invocation_digest"),
            "observe_state_digest": state.get("observe_state_digest"),
            "comparison_receipt_digest": state.get("comparison_receipt_digest"),
            "intended_effect_digest": state.get("transaction_intent", {}).get(
                "intended_effect_digest"
            ),
        }
        for field, expected in bindings.items():
            if receipt.get(field) != expected:
                errors.append(f"reconciliation_{field}_mismatch")
        verdict = str(receipt.get("verdict", ""))
        if verdict not in RECONCILIATION_VERDICTS:
            errors.append("reconciliation_verdict_invalid")
        evidence = unique_strings(
            receipt.get("independent_world_evidence_digests"),
            "independent_world_evidence_digests",
        )
        sources = unique_strings(
            receipt.get("independent_source_ids"), "independent_source_ids"
        )
        if len(sources) < 2:
            errors.append("reconciliation_independent_sources_insufficient")
        if not evidence:
            errors.append("reconciliation_world_evidence_missing")
        if receipt.get("tool_receipt_only") is not False:
            errors.append("reconciliation_tool_receipt_only_forbidden")
        if receipt.get("world_observation_performed") is not True:
            errors.append("reconciliation_world_observation_required")
        if receipt.get("observation_is_verification") is not False:
            errors.append("reconciliation_observation_verification_boundary_invalid")
        if receipt.get("reconciliation_is_truth") is not False:
            errors.append("reconciliation_truth_claim_forbidden")
        if receipt.get("causal_attribution_granted") is not False:
            errors.append("reconciliation_causal_attribution_forbidden")
        if receipt.get("compensation_required") is not (
            verdict == "COMPENSATION_REQUIRED"
        ):
            errors.append("reconciliation_compensation_flag_invalid")
        require_int(receipt.get("reconciled_at_ms"), "reconciled_at_ms")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("reconciliation_authority_escalation")
        if receipt.get("reconciliation_receipt_digest") != reconciliation_digest(
            receipt
        ):
            errors.append("reconciliation_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_compensation_request(
    *,
    state: Mapping[str, Any],
    request_id: str,
    new_idempotency_key: str,
    proposed_plan_lineage_id: str,
    rationale_digest: str,
    requested_at_ms: int,
) -> dict[str, Any]:
    if state.get("current_phase") != "verified":
        raise ValueError("compensation_request_requires_verified_state")
    intent = state["transaction_intent"]
    if intent.get("compensation_mode") != "explicit_operation":
        raise ValueError("transaction_is_not_explicitly_compensable")
    new_key = require_string(new_idempotency_key, "new_idempotency_key")
    if new_key == intent.get("idempotency_key"):
        raise ValueError("compensation_must_use_new_idempotency_key")
    packet = {
        "version": COMPENSATION_REQUEST_VERSION,
        "request_id": require_string(request_id, "request_id"),
        "source_transaction_id": state["transaction_id"],
        "source_transaction_state_digest": state["transaction_state_digest"],
        "source_transaction_intent_digest": state["transaction_intent_digest"],
        "source_reconciliation_receipt_digest": state[
            "reconciliation_receipt_digest"
        ],
        "source_verify_state_digest": state["verify_state_digest"],
        "connector_id": intent["connector_id"],
        "compensation_operation_id": intent["compensation_operation_id"],
        "compensation_input_digest": intent["compensation_input_digest"],
        "new_idempotency_key": new_key,
        "proposed_plan_lineage_id": require_string(
            proposed_plan_lineage_id, "proposed_plan_lineage_id"
        ),
        "rationale_digest": require_string(rationale_digest, "rationale_digest"),
        "proposal_only": True,
        "requires_new_planos_synthesis": True,
        "requires_new_decisionos_selection": True,
        "requires_new_actos_authorization": True,
        "requires_new_capability_lease": True,
        "same_transaction_execution_forbidden": True,
        "automatic_execution": False,
        "automatic_rollback": False,
        "requested_at_ms": require_int(requested_at_ms, "requested_at_ms"),
        "non_authority": copy_non_authority(),
        "compensation_request_digest": "",
    }
    packet["compensation_request_digest"] = compensation_request_digest(packet)
    errors = validate_compensation_request(packet, state)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_compensation_request(
    request: Mapping[str, Any], state: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    try:
        if request.get("version") != COMPENSATION_REQUEST_VERSION:
            errors.append("compensation_request_version_invalid")
        intent = state.get("transaction_intent", {})
        bindings = {
            "source_transaction_id": state.get("transaction_id"),
            "source_transaction_state_digest": state.get("transaction_state_digest"),
            "source_transaction_intent_digest": state.get(
                "transaction_intent_digest"
            ),
            "source_reconciliation_receipt_digest": state.get(
                "reconciliation_receipt_digest"
            ),
            "source_verify_state_digest": state.get("verify_state_digest"),
            "connector_id": intent.get("connector_id"),
            "compensation_operation_id": intent.get("compensation_operation_id"),
            "compensation_input_digest": intent.get("compensation_input_digest"),
        }
        for field, expected in bindings.items():
            if request.get(field) != expected:
                errors.append(f"compensation_{field}_mismatch")
        for field in (
            "request_id",
            "new_idempotency_key",
            "proposed_plan_lineage_id",
            "rationale_digest",
        ):
            require_string(request.get(field), field)
        if request.get("new_idempotency_key") == intent.get("idempotency_key"):
            errors.append("compensation_idempotency_key_reuse_forbidden")
        for field in (
            "proposal_only",
            "requires_new_planos_synthesis",
            "requires_new_decisionos_selection",
            "requires_new_actos_authorization",
            "requires_new_capability_lease",
            "same_transaction_execution_forbidden",
        ):
            if request.get(field) is not True:
                errors.append(f"compensation_{field}_required")
        if request.get("automatic_execution") is not False:
            errors.append("compensation_automatic_execution_forbidden")
        if request.get("automatic_rollback") is not False:
            errors.append("compensation_automatic_rollback_forbidden")
        require_int(request.get("requested_at_ms"), "requested_at_ms")
        if dict(request.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("compensation_authority_escalation")
        if request.get("compensation_request_digest") != compensation_request_digest(
            request
        ):
            errors.append("compensation_request_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _decision_route(state: Mapping[str, Any]) -> str:
    if state.get("effect_recorded") is not True:
        return "NO_EFFECT_RECORDED"
    if state.get("reobservation_required") is True or state.get(
        "verification_route"
    ) == "VERIFICATION_INDETERMINATE":
        return "REOBSERVATION_REQUIRED"
    if (
        state.get("reconciliation_verdict") == "EFFECT_CONFIRMED"
        and state.get("verification_route") == "VERIFICATION_PASSED"
    ):
        return "EFFECT_CONFIRMED"
    if state.get("transaction_intent", {}).get("compensation_mode") == (
        "explicit_operation"
    ):
        return "COMPENSATION_PROPOSED"
    return "HANDOVER_REQUIRED"


def build_transaction_decision(
    *,
    state: Mapping[str, Any],
    compensation_request: Mapping[str, Any] | None = None,
    handover_reason_digest: str = "",
    reobservation_reason_digest: str = "",
    decided_at_ms: int,
) -> dict[str, Any]:
    if state.get("current_phase") not in {"effect_bound", "verified"}:
        raise ValueError("transaction_decision_phase_invalid")
    route = _decision_route(state)
    compensation = dict(compensation_request or {})
    if route == "COMPENSATION_PROPOSED":
        if not compensation:
            raise ValueError("transaction_compensation_request_required")
        errors = validate_compensation_request(compensation, state)
        if errors:
            raise ValueError("invalid_compensation_request:" + ";".join(errors))
    elif compensation:
        raise ValueError("transaction_unexpected_compensation_request")
    handover_reason = str(handover_reason_digest)
    reobserve_reason = str(reobservation_reason_digest)
    if route == "HANDOVER_REQUIRED":
        require_string(handover_reason, "handover_reason_digest")
    elif handover_reason:
        raise ValueError("transaction_unexpected_handover_reason")
    if route == "REOBSERVATION_REQUIRED":
        require_string(reobserve_reason, "reobservation_reason_digest")
    elif reobserve_reason:
        raise ValueError("transaction_unexpected_reobservation_reason")
    packet = {
        "version": DECISION_VERSION,
        "transaction_id": state["transaction_id"],
        "source_transaction_state_digest": state["transaction_state_digest"],
        "transaction_intent_digest": state["transaction_intent_digest"],
        "final_act_state_digest": state["final_act_state_digest"],
        "observe_state_digest": state["observe_state_digest"],
        "reconciliation_receipt_digest": state[
            "reconciliation_receipt_digest"
        ],
        "verify_state_digest": state["verify_state_digest"],
        "route": route,
        "compensation_request": deepcopy(compensation),
        "compensation_request_digest": str(
            compensation.get("compensation_request_digest", "")
        ),
        "handover_reason_digest": handover_reason,
        "reobservation_reason_digest": reobserve_reason,
        "effect_commit_is_truth": False,
        "automatic_compensation": False,
        "automatic_rollback": False,
        "automatic_plan_completion": False,
        "decision_grants_execution_authority": False,
        "decided_at_ms": require_int(decided_at_ms, "decided_at_ms"),
        "non_authority": copy_non_authority(),
        "transaction_decision_digest": "",
    }
    packet["transaction_decision_digest"] = decision_digest(packet)
    errors = validate_transaction_decision(packet, state)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_transaction_decision(
    decision: Mapping[str, Any], state: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    try:
        if decision.get("version") != DECISION_VERSION:
            errors.append("transaction_decision_version_invalid")
        expected_route = _decision_route(state)
        if decision.get("route") != expected_route:
            errors.append("transaction_decision_route_invalid")
        bindings = {
            "transaction_id": state.get("transaction_id"),
            "source_transaction_state_digest": state.get("transaction_state_digest"),
            "transaction_intent_digest": state.get("transaction_intent_digest"),
            "final_act_state_digest": state.get("final_act_state_digest"),
            "observe_state_digest": state.get("observe_state_digest"),
            "reconciliation_receipt_digest": state.get(
                "reconciliation_receipt_digest"
            ),
            "verify_state_digest": state.get("verify_state_digest"),
        }
        for field, expected in bindings.items():
            if decision.get(field) != expected:
                errors.append(f"transaction_decision_{field}_mismatch")
        if expected_route == "COMPENSATION_PROPOSED":
            request = decision.get("compensation_request")
            if not isinstance(request, Mapping):
                errors.append("transaction_decision_compensation_missing")
            else:
                errors.extend(
                    "compensation:" + item
                    for item in validate_compensation_request(request, state)
                )
                if decision.get("compensation_request_digest") != request.get(
                    "compensation_request_digest"
                ):
                    errors.append("transaction_decision_compensation_digest_mismatch")
        else:
            if decision.get("compensation_request") not in ({}, None):
                errors.append("transaction_decision_unexpected_compensation")
            if decision.get("compensation_request_digest"):
                errors.append("transaction_decision_unexpected_compensation_digest")
        if expected_route == "HANDOVER_REQUIRED":
            require_string(
                decision.get("handover_reason_digest"), "handover_reason_digest"
            )
        elif decision.get("handover_reason_digest"):
            errors.append("transaction_decision_unexpected_handover_reason")
        if expected_route == "REOBSERVATION_REQUIRED":
            require_string(
                decision.get("reobservation_reason_digest"),
                "reobservation_reason_digest",
            )
        elif decision.get("reobservation_reason_digest"):
            errors.append("transaction_decision_unexpected_reobservation_reason")
        for field in (
            "effect_commit_is_truth",
            "automatic_compensation",
            "automatic_rollback",
            "automatic_plan_completion",
            "decision_grants_execution_authority",
        ):
            if decision.get(field) is not False:
                errors.append(f"transaction_decision_{field}_forbidden")
        require_int(decision.get("decided_at_ms"), "decided_at_ms")
        if dict(decision.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("transaction_decision_authority_escalation")
        if decision.get("transaction_decision_digest") != decision_digest(decision):
            errors.append("transaction_decision_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_transaction_final_receipt(
    *, state: Mapping[str, Any], committed_at_ms: int
) -> dict[str, Any]:
    if state.get("current_phase") != "decided":
        raise ValueError("final_receipt_requires_decided_state")
    decision = state.get("transaction_decision")
    if not isinstance(decision, Mapping):
        raise ValueError("transaction_decision_missing")
    errors = validate_transaction_decision(decision, state)
    if errors:
        raise ValueError("invalid_transaction_decision:" + ";".join(errors))
    packet = {
        "version": FINAL_RECEIPT_VERSION,
        "transaction_id": state["transaction_id"],
        "transaction_intent_digest": state["transaction_intent_digest"],
        "source_transaction_state_digest": state["transaction_state_digest"],
        "connector_contract_digest": state["connector_contract_digest"],
        "final_act_state_digest": state["final_act_state_digest"],
        "host_receipt_digest": state["host_receipt_digest"],
        "host_invocation_digest": state["host_invocation_digest"],
        "observe_state_digest": state["observe_state_digest"],
        "reconciliation_receipt_digest": state[
            "reconciliation_receipt_digest"
        ],
        "verify_state_digest": state["verify_state_digest"],
        "transaction_decision_digest": state["transaction_decision_digest"],
        "route": decision["route"],
        "effect_recorded": state["effect_recorded"],
        "reconciliation_verdict": state["reconciliation_verdict"],
        "verification_route": state["verification_route"],
        "compensation_request_digest": state["compensation_request_digest"],
        "append_only_commit": True,
        "lower_receipts_remain_canonical": True,
        "tool_response_success_not_world_confirmation": True,
        "world_reconciliation_not_truth": True,
        "commit_grants_execution_authority": False,
        "commit_grants_final_authority": False,
        "memory_overwrite": False,
        "automatic_compensation": False,
        "automatic_rollback": False,
        "committed_at_ms": require_int(committed_at_ms, "committed_at_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "transaction_final_receipt_digest": "",
    }
    packet["transaction_final_receipt_digest"] = final_receipt_digest(packet)
    errors = validate_transaction_final_receipt(packet, state)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_transaction_final_receipt(
    receipt: Mapping[str, Any], state: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != FINAL_RECEIPT_VERSION:
            errors.append("transaction_final_receipt_version_invalid")
        bindings = {
            "transaction_id": state.get("transaction_id"),
            "transaction_intent_digest": state.get("transaction_intent_digest"),
            "source_transaction_state_digest": state.get("transaction_state_digest"),
            "connector_contract_digest": state.get("connector_contract_digest"),
            "final_act_state_digest": state.get("final_act_state_digest"),
            "host_receipt_digest": state.get("host_receipt_digest"),
            "host_invocation_digest": state.get("host_invocation_digest"),
            "observe_state_digest": state.get("observe_state_digest"),
            "reconciliation_receipt_digest": state.get(
                "reconciliation_receipt_digest"
            ),
            "verify_state_digest": state.get("verify_state_digest"),
            "transaction_decision_digest": state.get(
                "transaction_decision_digest"
            ),
            "route": state.get("route"),
            "effect_recorded": state.get("effect_recorded"),
            "reconciliation_verdict": state.get("reconciliation_verdict"),
            "verification_route": state.get("verification_route"),
            "compensation_request_digest": state.get(
                "compensation_request_digest"
            ),
        }
        for field, expected in bindings.items():
            if receipt.get(field) != expected:
                errors.append(f"transaction_final_{field}_mismatch")
        for field in (
            "append_only_commit",
            "lower_receipts_remain_canonical",
            "tool_response_success_not_world_confirmation",
            "world_reconciliation_not_truth",
        ):
            if receipt.get(field) is not True:
                errors.append(f"transaction_final_{field}_required")
        for field in (
            "commit_grants_execution_authority",
            "commit_grants_final_authority",
            "memory_overwrite",
            "automatic_compensation",
            "automatic_rollback",
        ):
            if receipt.get(field) is not False:
                errors.append(f"transaction_final_{field}_forbidden")
        require_int(receipt.get("committed_at_ms"), "committed_at_ms")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("transaction_final_authority_escalation")
        if dict(receipt.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("transaction_final_boundary_invalid")
        if receipt.get("transaction_final_receipt_digest") != final_receipt_digest(
            receipt
        ):
            errors.append("transaction_final_receipt_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _validate_event_base(
    state: Mapping[str, Any], event: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    if event.get("version") != EVENT_VERSION:
        errors.append("transaction_event_version_invalid")
    if event.get("transaction_id") != state.get("transaction_id"):
        errors.append("transaction_event_id_mismatch")
    if event.get("lineage_id") != state.get("lineage_id"):
        errors.append("transaction_event_lineage_mismatch")
    if event.get("transaction_event_digest") != event_digest(event):
        errors.append("transaction_event_digest_invalid")
    if dict(event.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("transaction_event_authority_escalation")
    if event.get("expected_transaction_state_digest") != state.get(
        "transaction_state_digest"
    ):
        errors.append("transaction_event_state_digest_stale")
    if event.get("source_phase") != state.get("current_phase"):
        errors.append("transaction_event_source_phase_stale")
    if event.get("target_phase") != _next_phase(state):
        errors.append("transaction_event_phase_order_invalid")
    if event.get("event_index") != int(state.get("event_index", -1)) + 1:
        errors.append("transaction_event_index_invalid")
    if int(event.get("created_at_ms", -1)) < int(state.get("updated_at_ms", 0)):
        errors.append("transaction_event_time_regression")
    return errors


def _apply_payload(
    state: dict[str, Any], phase: str, payload: Mapping[str, Any]
) -> None:
    intent = state["transaction_intent"]
    if phase == "effect_bound":
        act_state = payload.get("final_act_state")
        if not isinstance(act_state, Mapping):
            raise ValueError("final_act_state_required")
        errors = validate_act_state(act_state)
        if errors:
            raise ValueError("invalid_final_act_state:" + ";".join(errors))
        if act_state.get("current_phase") != "commit":
            raise ValueError("final_act_state_not_committed")
        checks = {
            "act_id": intent["source_act_id"],
            "lineage_id": intent["lineage_id"],
            "source_plan_state_digest": intent["source_plan_state_digest"],
            "source_committed_plan_digest": intent[
                "source_committed_plan_digest"
            ],
            "selected_step_id": intent["selected_step_id"],
            "selected_step_digest": intent["selected_step_digest"],
            "operation_id": intent["operation_id"],
            "operation_input_digest": intent["operation_input_digest"],
            "step_authorization_digest": intent["step_authorization_digest"],
            "host_license_digest": intent["capability_lease_digest"],
            "host_projection_digest": intent["host_projection_digest"],
            "source_supervisor_bundle_digest": intent[
                "source_supervisor_bundle_digest"
            ],
        }
        for field, expected in checks.items():
            if act_state.get(field) != expected:
                raise ValueError(f"final_act_state_{field}_mismatch")
        route = str(act_state.get("route", ""))
        if route == "REPLAYED" or act_state.get("host_receipt", {}).get(
            "status"
        ) == HOST_REPLAYED:
            raise ValueError(
                "lower_act_replay_requires_existing_transaction_receipt"
            )
        if route not in {"EFFECT_RECORDED", "BLOCKED"}:
            raise ValueError("final_act_route_invalid")
        receipt = act_state.get("host_receipt")
        if not isinstance(receipt, Mapping):
            raise ValueError("final_host_receipt_missing")
        if receipt.get("host_receipt_digest") != host_receipt_digest(receipt):
            raise ValueError("final_host_receipt_digest_invalid")
        state["final_act_state"] = deepcopy(dict(act_state))
        state["final_act_state_digest"] = act_state["act_state_digest"]
        state["lower_act_route"] = route
        if route == "EFFECT_RECORDED":
            if receipt.get("status") != HOST_READY:
                raise ValueError("effect_recorded_host_receipt_not_ready")
            if act_state.get("effect_recorded") is not True:
                raise ValueError("effect_recorded_flag_missing")
            state["effect_recorded"] = True
            state["host_receipt_digest"] = act_state["host_receipt_digest"]
            state["host_invocation_digest"] = act_state[
                "host_invocation_digest"
            ]
            state["result_supervisor_bundle_digest"] = act_state[
                "result_supervisor_bundle_digest"
            ]
            state["slice_digest"] = require_string(
                receipt.get("slice_digest"), "slice_digest"
            )
            state["observation_required"] = True
            state["verification_required"] = True
        else:
            if receipt.get("status") != HOST_BLOCKED:
                raise ValueError("blocked_act_host_receipt_mismatch")
            if act_state.get("effect_recorded") is not False:
                raise ValueError("blocked_act_effect_flag_invalid")
            state["effect_recorded"] = False
            state["observation_required"] = False
            state["verification_required"] = False
        return

    if phase == "observed":
        observe_state = payload.get("observe_state")
        if not isinstance(observe_state, Mapping):
            raise ValueError("observe_state_required")
        errors = validate_observe_state(observe_state)
        if errors:
            raise ValueError("invalid_observe_state:" + ";".join(errors))
        if observe_state.get("current_phase") != "commit":
            raise ValueError("observe_state_not_committed")
        if observe_state.get("source_act_state_digest") != state.get(
            "final_act_state_digest"
        ):
            raise ValueError("observe_source_act_state_mismatch")
        for field, expected in (
            ("host_receipt_digest", state["host_receipt_digest"]),
            ("host_invocation_digest", state["host_invocation_digest"]),
            (
                "expected_observation_digest",
                intent["expected_observation_digest"],
            ),
            (
                "verification_criterion_digest",
                intent["verification_criterion_digest"],
            ),
        ):
            if observe_state.get(field) != expected:
                raise ValueError(f"observe_{field}_mismatch")
        route = str(observe_state.get("route", ""))
        if route not in {
            "OBSERVATION_MATCHED",
            "OBSERVATION_DIVERGENT",
            "OBSERVATION_INCONCLUSIVE",
            "OBSERVATION_CONFLICTED",
        }:
            raise ValueError("observe_route_invalid")
        state["observe_state"] = deepcopy(dict(observe_state))
        state["observe_state_digest"] = observe_state["observe_state_digest"]
        state["observation_route"] = route
        state["evidence_packet_digest"] = observe_state[
            "evidence_packet_digest"
        ]
        state["quality_report_digest"] = observe_state[
            "quality_report_digest"
        ]
        state["comparison_receipt_digest"] = observe_state[
            "comparison_receipt_digest"
        ]
        state["reobservation_required"] = bool(
            observe_state.get("reobservation_required", False)
        )
        state["verification_required"] = True
        return

    if phase == "reconciled":
        receipt = payload.get("reconciliation_receipt")
        if not isinstance(receipt, Mapping):
            raise ValueError("reconciliation_receipt_required")
        errors = validate_reconciliation_receipt(receipt, state)
        if errors:
            raise ValueError("invalid_reconciliation_receipt:" + ";".join(errors))
        state["reconciliation_receipt"] = deepcopy(dict(receipt))
        state["reconciliation_receipt_digest"] = receipt[
            "reconciliation_receipt_digest"
        ]
        state["reconciliation_verdict"] = receipt["verdict"]
        return

    if phase == "verified":
        verify_state = payload.get("verify_state")
        if not isinstance(verify_state, Mapping):
            raise ValueError("verify_state_required")
        errors = validate_verify_state(verify_state)
        if errors:
            raise ValueError("invalid_verify_state:" + ";".join(errors))
        if verify_state.get("current_phase") != "commit":
            raise ValueError("verify_state_not_committed")
        if verify_state.get("source_observe_state_digest") != state.get(
            "observe_state_digest"
        ):
            raise ValueError("verify_source_observe_state_mismatch")
        for field, expected in (
            ("host_receipt_digest", state["host_receipt_digest"]),
            ("host_invocation_digest", state["host_invocation_digest"]),
            ("evidence_packet_digest", state["evidence_packet_digest"]),
            ("quality_report_digest", state["quality_report_digest"]),
            ("comparison_receipt_digest", state["comparison_receipt_digest"]),
        ):
            if verify_state.get(field) != expected:
                raise ValueError(f"verify_{field}_mismatch")
        route = str(verify_state.get("route", ""))
        if route not in {
            "VERIFICATION_PASSED",
            "VERIFICATION_FAILED",
            "VERIFICATION_INDETERMINATE",
        }:
            raise ValueError("verify_route_invalid")
        state["verify_state"] = deepcopy(dict(verify_state))
        state["verify_state_digest"] = verify_state["verify_state_digest"]
        state["verification_route"] = route
        state["verification_evidence_digest"] = verify_state[
            "verification_evidence_digest"
        ]
        state["verification_required"] = bool(
            verify_state.get("verification_required", False)
        )
        state["reobservation_required"] = bool(
            state["reobservation_required"]
            or verify_state.get("reobservation_required", False)
        )
        state["corrective_action_required"] = bool(
            verify_state.get("corrective_action_required", False)
        )
        return

    if phase == "decided":
        decision = payload.get("transaction_decision")
        if not isinstance(decision, Mapping):
            raise ValueError("transaction_decision_required")
        errors = validate_transaction_decision(decision, state)
        if errors:
            raise ValueError("invalid_transaction_decision:" + ";".join(errors))
        state["transaction_decision"] = deepcopy(dict(decision))
        state["transaction_decision_digest"] = decision[
            "transaction_decision_digest"
        ]
        state["route"] = decision["route"]
        compensation = decision.get("compensation_request", {})
        if isinstance(compensation, Mapping) and compensation:
            state["compensation_request"] = deepcopy(dict(compensation))
            state["compensation_request_digest"] = compensation[
                "compensation_request_digest"
            ]
        return

    if phase == "committed":
        receipt = payload.get("transaction_final_receipt")
        if not isinstance(receipt, Mapping):
            raise ValueError("transaction_final_receipt_required")
        errors = validate_transaction_final_receipt(receipt, state)
        if errors:
            raise ValueError("invalid_transaction_final_receipt:" + ";".join(errors))
        if payload.get("append_only_commit") is not True:
            raise ValueError("transaction_append_only_commit_required")
        if payload.get("memory_overwrite") is not False:
            raise ValueError("transaction_memory_overwrite_forbidden")
        if payload.get("automatic_compensation") is not False:
            raise ValueError("transaction_automatic_compensation_forbidden")
        if payload.get("automatic_rollback") is not False:
            raise ValueError("transaction_automatic_rollback_forbidden")
        if dict(payload.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            raise ValueError("transaction_commit_authority_escalation")
        state["final_receipt"] = deepcopy(dict(receipt))
        state["transaction_final_receipt_digest"] = receipt[
            "transaction_final_receipt_digest"
        ]
        return

    raise ValueError("transaction_target_phase_unsupported")


def _result(
    *,
    status: str,
    state: Mapping[str, Any],
    event_id: str,
    predecessor: str,
    errors: list[str],
) -> dict[str, Any]:
    packet = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "transaction_event_digest": event_id,
        "predecessor_transaction_state_digest": predecessor,
        "result_transaction_state_digest": state["transaction_state_digest"],
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "transaction_apply_result_digest": "",
    }
    packet["transaction_apply_result_digest"] = apply_result_digest(packet)
    return packet


def apply_transaction_event(
    state: Mapping[str, Any], event: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_transaction_state(state)
    if state_errors:
        raise ValueError("invalid_transaction_state:" + ";".join(state_errors))
    event_id = str(event.get("transaction_event_digest", ""))
    predecessor = str(state["transaction_state_digest"])
    if event_id and event_id in set(state.get("processed_event_digests", [])):
        return _result(
            status="REPLAYED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[],
        )
    errors = _validate_event_base(state, event)
    if errors:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=errors,
        )
    next_state = deepcopy(dict(state))
    phase = str(event["target_phase"])
    try:
        _apply_payload(next_state, phase, dict(event.get("payload", {})))
    except (TypeError, ValueError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[str(exc)],
        )
    next_state["predecessor_transaction_state_digest"] = predecessor
    next_state["current_phase"] = phase
    next_state["event_index"] = int(event["event_index"])
    next_state["updated_at_ms"] = int(event["created_at_ms"])
    next_state["processed_event_digests"] = list(
        next_state["processed_event_digests"]
    ) + [event_id]
    next_state["event_history"] = list(next_state["event_history"]) + [
        {
            "event_index": event["event_index"],
            "source_phase": event["source_phase"],
            "target_phase": phase,
            "artifact_digest": event["artifact_digest"],
            "transaction_event_digest": event_id,
            "created_at_ms": event["created_at_ms"],
        }
    ]
    if phase == "committed":
        next_state["transaction_version"] += 1
        next_state["committed_records"] += 1
        next_state["record_summaries"] = list(next_state["record_summaries"]) + [
            {
                "transaction_version": next_state["transaction_version"],
                "route": next_state["route"],
                "operation_id": next_state["transaction_intent"]["operation_id"],
                "idempotency_key": next_state["transaction_intent"][
                    "idempotency_key"
                ],
                "host_invocation_digest": next_state[
                    "host_invocation_digest"
                ],
                "reconciliation_verdict": next_state[
                    "reconciliation_verdict"
                ],
                "verification_route": next_state["verification_route"],
                "compensation_request_digest": next_state[
                    "compensation_request_digest"
                ],
                "transaction_final_receipt_digest": next_state[
                    "transaction_final_receipt_digest"
                ],
            }
        ]
    next_state["transaction_state_digest"] = ""
    next_state["transaction_state_digest"] = state_digest(next_state)
    next_errors = validate_transaction_state(next_state)
    if next_errors:
        raise ValueError("next_transaction_state_invalid:" + ";".join(next_errors))
    return _result(
        status="APPLIED",
        state=next_state,
        event_id=event_id,
        predecessor=predecessor,
        errors=[],
    )


__all__ = [
    "apply_transaction_event",
    "build_compensation_request",
    "build_connector_contract",
    "build_initial_transaction_state",
    "build_transaction_decision",
    "build_transaction_event",
    "build_transaction_final_receipt",
    "build_transaction_intent",
    "build_world_effect_reconciliation_receipt",
    "validate_compensation_request",
    "validate_connector_contract",
    "validate_reconciliation_receipt",
    "validate_transaction_decision",
    "validate_transaction_final_receipt",
    "validate_transaction_intent",
    "validate_transaction_state",
]
