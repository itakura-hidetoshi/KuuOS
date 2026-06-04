#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


EXECUTABLE_ACTIONS = {"advance_tick", "notify", "ticket", "handover"}
NONEXEC_ACTIONS = {"hold", "observe", "freeze"}
ALL_ACTIONS = EXECUTABLE_ACTIONS | NONEXEC_ACTIONS

ACTION_ADAPTERS = {
    "advance_tick": "tick_step_adapter_dry_run",
    "notify": "notification_adapter_dry_run",
    "ticket": "ticket_adapter_dry_run",
    "handover": "handover_adapter_dry_run",
    "hold": "hold_noop_adapter",
    "observe": "observe_plan_adapter_dry_run",
    "freeze": "freeze_noop_adapter",
}

FORBIDDEN_EFFECT_KEYS = [
    "ledger_append_performed",
    "execution_committed",
    "runtime_control_performed",
    "scheduler_bypass_performed",
    "notification_sent",
    "ticket_created",
    "handover_performed",
    "memory_write_performed",
    "memory_append_performed",
    "memory_overwrite_performed",
    "world_update_performed",
    "control_packet_mutation_performed",
    "probe_execution_performed",
]

FORBIDDEN_AUTHORITY_KEYS = [
    "execution_authority_granted",
    "execution_commit_allowed",
    "runtime_control_allowed",
    "scheduler_bypass_allowed",
    "ledger_append_allowed",
    "memory_write_allowed",
    "world_update_allowed",
    "probe_execution_allowed",
]


@dataclass(frozen=True)
class QiBoundedExecutionMechanismResult:
    mechanism_version: str
    mechanism_status: str
    mechanism_packet_id: str
    selected_action: str
    adapter_name: str
    adapter_mode: str
    step_plan_id: str
    dry_run_actuator_receipt_id: str
    source_engine_packet_id: str | None
    source_packet_chain_id: str | None
    source_finality_packet_id: str | None
    input_intent_digest: str
    adapter_allowlist_digest: str
    idempotency_key: str
    step_plan: dict[str, Any]
    dry_run_actuator_receipt: dict[str, Any]
    adapter_prepared: bool
    dry_run_actuator_performed: bool
    execution_committed: bool
    staged_intent_only: bool
    bounded_adapter_only: bool
    dry_run_only: bool
    receipt_only: bool
    read_only: bool
    projection_only: bool
    ledger_append_performed: bool
    runtime_control_performed: bool
    scheduler_bypass_performed: bool
    notification_sent: bool
    ticket_created: bool
    handover_performed: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    execution_authority_granted: bool
    execution_commit_allowed: bool
    runtime_control_allowed: bool
    scheduler_bypass_allowed: bool
    ledger_append_allowed: bool
    memory_write_allowed: bool
    world_update_allowed: bool
    probe_execution_allowed: bool
    mechanism_blockers: list[str]
    mechanism_warnings: list[str]
    authority: str = "qi_bounded_execution_mechanism_dry_run_adapter"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _str(value: Any, default: str = "") -> str:
    return str(value) if value is not None else default


def _action(value: Any, default: str = "hold") -> str:
    text = str(value or default)
    return text if text in ALL_ACTIONS else default


def _require_false(prefix: str, packet: Mapping[str, Any], keys: list[str], blockers: list[str]) -> None:
    for key in keys:
        if key in packet and packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def _engine_source(packet: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = packet.get("execution_intent_packet")
    if isinstance(nested, Mapping) and nested:
        return nested
    return packet


def _chain_finality_source(packet: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = packet.get("finality_packet")
    if isinstance(nested, Mapping) and nested:
        return nested
    return packet


def _adapter_allowed(adapter_name: str, ctx: Mapping[str, Any]) -> bool:
    allowed = _list(ctx.get("allowed_adapters"))
    if not allowed:
        return adapter_name in ACTION_ADAPTERS.values()
    return adapter_name in {str(item) for item in allowed}


def _effectless_step_plan(*, selected_action: str, adapter_name: str, source_engine_packet_id: str | None, source_finality_packet_id: str | None, intent_digest: str, allowlist_digest: str) -> dict[str, Any]:
    idempotency_key = _sha_obj({
        "selected_action": selected_action,
        "adapter_name": adapter_name,
        "source_engine_packet_id": source_engine_packet_id,
        "source_finality_packet_id": source_finality_packet_id,
        "intent_digest": intent_digest,
        "adapter_allowlist_digest": allowlist_digest,
    })
    return {
        "step_plan_id": "qi-bounded-step-" + idempotency_key[:16],
        "selected_action": selected_action,
        "adapter_name": adapter_name,
        "adapter_mode": "dry_run_adapter_only",
        "source_engine_packet_id": source_engine_packet_id,
        "source_finality_packet_id": source_finality_packet_id,
        "input_intent_digest": intent_digest,
        "adapter_allowlist_digest": allowlist_digest,
        "idempotency_key": idempotency_key,
        "preconditions": [
            "engine_ready",
            "packet_chain_finality_ready",
            "bounded_adapter_scope_granted",
            "dry_run_only_required",
            "adapter_allowlisted",
            "all_external_side_effects_forbidden",
        ],
        "adapter_contract": {
            "external_side_effects_allowed": False,
            "commit_allowed": False,
            "notification_send_allowed": False,
            "ticket_create_allowed": False,
            "handover_perform_allowed": False,
            "memory_write_allowed": False,
            "world_update_allowed": False,
            "probe_execution_allowed": False,
        },
        "planned_effect": "dry_run_receipt_only",
    }


def build_qi_bounded_execution_mechanism(
    *,
    engine_packet: Mapping[str, Any],
    health_packet_chain: Mapping[str, Any],
    mechanism_context: Mapping[str, Any] | None = None,
) -> QiBoundedExecutionMechanismResult:
    raw_engine = _mapping(engine_packet)
    engine = _engine_source(raw_engine)
    raw_chain = _mapping(health_packet_chain)
    finality = _chain_finality_source(raw_chain)
    ctx = _mapping(mechanism_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("qi_bounded_execution_mechanism_enabled") is not True:
        blockers.append("qi_bounded_execution_mechanism_enabled_not_true")
    if ctx.get("bounded_adapter_scope_granted") is not True:
        blockers.append("bounded_adapter_scope_granted_not_true")
    if ctx.get("dry_run_only_required") is not True:
        blockers.append("dry_run_only_required_not_true")
    if ctx.get("staged_intent_only_required") is not True:
        blockers.append("staged_intent_only_required_not_true")
    if ctx.get("receipt_only_required") is not True:
        blockers.append("receipt_only_required_not_true")
    if ctx.get("read_only_required") is not True:
        blockers.append("read_only_required_not_true")
    if ctx.get("projection_only_required") is not True:
        blockers.append("projection_only_required_not_true")

    for request_key in [
        "request_execution_commit",
        "request_runtime_control",
        "request_scheduler_bypass",
        "request_notification_send",
        "request_ticket_create",
        "request_handover_perform",
        "request_ledger_append",
        "request_memory_write",
        "request_memory_append",
        "request_world_update",
        "request_probe_execution",
        "request_authority_grant",
    ]:
        if ctx.get(request_key) is True:
            blockers.append(f"{request_key}_not_allowed")

    if raw_engine.get("engine_status") != "QI_AUTONOMOUS_EXECUTION_ENGINE_READY":
        blockers.append("engine_status_not_ready")
    if raw_engine.get("execution_committed") is not False:
        blockers.append("engine_execution_committed_not_false")
    if raw_engine.get("receipt_only") is not True:
        blockers.append("engine_receipt_only_not_true")
    if raw_engine.get("read_only") is not True:
        blockers.append("engine_read_only_not_true")
    if raw_engine.get("projection_only") is not True:
        blockers.append("engine_projection_only_not_true")
    _require_false("engine", raw_engine, FORBIDDEN_EFFECT_KEYS, blockers)
    _require_false("engine_intent", engine, FORBIDDEN_EFFECT_KEYS, blockers)

    if raw_chain.get("chain_status") != "QI_EXECUTION_HEALTH_PACKET_CHAIN_READY":
        blockers.append("packet_chain_status_not_ready")
    if raw_chain.get("read_only_chain") is not True:
        blockers.append("packet_chain_read_only_not_true")
    if raw_chain.get("projection_only") is not True:
        blockers.append("packet_chain_projection_only_not_true")
    if raw_chain.get("same_root_required") is not True:
        blockers.append("packet_chain_same_root_not_true")
    if finality.get("packet_status") != "QI_EXECUTION_HEALTH_FINALITY_PACKET_READY":
        blockers.append("finality_packet_not_ready")
    if finality.get("finality_scope") != "packet_chain_finality_not_authority_surface":
        blockers.append("finality_scope_invalid")
    _require_false("packet_chain", raw_chain, FORBIDDEN_EFFECT_KEYS, blockers)
    _require_false("finality", finality, FORBIDDEN_EFFECT_KEYS, blockers)
    _require_false("finality", finality, FORBIDDEN_AUTHORITY_KEYS, blockers)

    selected_action = _action(raw_engine.get("selected_action", engine.get("selected_action")), "hold")
    adapter_name = ACTION_ADAPTERS[selected_action]
    if not _adapter_allowed(adapter_name, ctx):
        blockers.append("adapter_not_allowlisted")

    intent_staged = raw_engine.get("execution_intent_staged") is True or engine.get("execution_intent_staged") is True
    if selected_action in EXECUTABLE_ACTIONS and not intent_staged:
        blockers.append("executable_action_without_staged_intent")
    if selected_action in NONEXEC_ACTIONS:
        warnings.append("nonexecuting_action_uses_noop_or_plan_adapter")

    source_engine_packet_id = raw_engine.get("engine_packet_id", engine.get("engine_packet_id"))
    source_packet_chain_id = raw_chain.get("packet_chain_id", finality.get("packet_chain_id"))
    source_finality_packet_id = raw_chain.get("finality_packet_id", finality.get("packet_id"))
    input_intent_digest = _sha_obj({
        "raw_engine": dict(raw_engine),
        "engine_intent": dict(engine),
    })
    adapter_allowlist_digest = _sha_obj({
        "allowed_adapters": sorted(str(item) for item in _list(ctx.get("allowed_adapters"))),
        "default_allowlist_used": not bool(_list(ctx.get("allowed_adapters"))),
    })

    step_plan = _effectless_step_plan(
        selected_action=selected_action,
        adapter_name=adapter_name,
        source_engine_packet_id=_str(source_engine_packet_id, None),
        source_finality_packet_id=_str(source_finality_packet_id, None),
        intent_digest=input_intent_digest,
        allowlist_digest=adapter_allowlist_digest,
    )
    step_plan_id = str(step_plan["step_plan_id"])
    idempotency_key = str(step_plan["idempotency_key"])
    mechanism_packet_id = "qi-bounded-exec-" + _sha_obj({
        "step_plan_id": step_plan_id,
        "idempotency_key": idempotency_key,
        "selected_action": selected_action,
        "adapter_name": adapter_name,
    })[:16]
    dry_run_actuator_receipt_id = "qi-dry-run-actuator-" + _sha_obj({
        "mechanism_packet_id": mechanism_packet_id,
        "step_plan_id": step_plan_id,
        "idempotency_key": idempotency_key,
    })[:16]

    ready = not blockers
    dry_run_receipt: dict[str, Any] = {}
    if ready:
        dry_run_receipt = {
            "dry_run_actuator_receipt_id": dry_run_actuator_receipt_id,
            "mechanism_packet_id": mechanism_packet_id,
            "step_plan_id": step_plan_id,
            "selected_action": selected_action,
            "adapter_name": adapter_name,
            "adapter_mode": "dry_run_adapter_only",
            "adapter_prepared": True,
            "dry_run_actuator_performed": True,
            "execution_committed": False,
            "external_side_effects_performed": False,
            "runtime_control_performed": False,
            "scheduler_bypass_performed": False,
            "notification_sent": False,
            "ticket_created": False,
            "handover_performed": False,
            "ledger_append_performed": False,
            "memory_write_performed": False,
            "memory_append_performed": False,
            "memory_overwrite_performed": False,
            "world_update_performed": False,
            "control_packet_mutation_performed": False,
            "probe_execution_performed": False,
            "execution_authority_granted": False,
            "execution_commit_allowed": False,
            "runtime_control_allowed": False,
            "scheduler_bypass_allowed": False,
            "ledger_append_allowed": False,
            "memory_write_allowed": False,
            "world_update_allowed": False,
            "probe_execution_allowed": False,
            "idempotency_key": idempotency_key,
            "receipt_only": True,
            "read_only": True,
            "projection_only": True,
        }

    return QiBoundedExecutionMechanismResult(
        mechanism_version="kuuos_runtime_daemon_qi_bounded_execution_mechanism_v0_1",
        mechanism_status="QI_BOUNDED_EXECUTION_MECHANISM_READY" if ready else "QI_BOUNDED_EXECUTION_MECHANISM_BLOCKED",
        mechanism_packet_id=mechanism_packet_id,
        selected_action=selected_action,
        adapter_name=adapter_name,
        adapter_mode="dry_run_adapter_only",
        step_plan_id=step_plan_id,
        dry_run_actuator_receipt_id=dry_run_actuator_receipt_id,
        source_engine_packet_id=_str(source_engine_packet_id, None),
        source_packet_chain_id=_str(source_packet_chain_id, None),
        source_finality_packet_id=_str(source_finality_packet_id, None),
        input_intent_digest=input_intent_digest,
        adapter_allowlist_digest=adapter_allowlist_digest,
        idempotency_key=idempotency_key,
        step_plan=step_plan if ready else {},
        dry_run_actuator_receipt=dry_run_receipt,
        adapter_prepared=ready,
        dry_run_actuator_performed=ready,
        execution_committed=False,
        staged_intent_only=True,
        bounded_adapter_only=True,
        dry_run_only=True,
        receipt_only=True,
        read_only=True,
        projection_only=True,
        ledger_append_performed=False,
        runtime_control_performed=False,
        scheduler_bypass_performed=False,
        notification_sent=False,
        ticket_created=False,
        handover_performed=False,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        execution_authority_granted=False,
        execution_commit_allowed=False,
        runtime_control_allowed=False,
        scheduler_bypass_allowed=False,
        ledger_append_allowed=False,
        memory_write_allowed=False,
        world_update_allowed=False,
        probe_execution_allowed=False,
        mechanism_blockers=blockers,
        mechanism_warnings=warnings,
    )
