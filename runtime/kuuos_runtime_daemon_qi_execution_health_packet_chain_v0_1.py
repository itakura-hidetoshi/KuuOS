#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


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
class QiExecutionHealthPacketChainResult:
    chain_version: str
    chain_status: str
    packet_chain_id: str
    packet_chain_root_digest: str
    source_health_baseline_packet_id: str | None
    source_confirmed_autonomy_packet_id: str | None
    autonomy_health_root_digest: str | None
    release_packet_id: str
    established_packet_id: str
    confirmed_baseline_packet_id: str
    finality_packet_id: str
    release_packet: dict[str, Any]
    established_packet: dict[str, Any]
    confirmed_baseline_packet: dict[str, Any]
    finality_packet: dict[str, Any]
    read_only_chain: bool
    projection_only: bool
    additive_only: bool
    tighten_only: bool
    same_root_required: bool
    ledger_append_performed: bool
    execution_committed: bool
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
    chain_blockers: list[str]
    chain_warnings: list[str]
    authority: str = "qi_execution_health_packet_chain_read_only_projection"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require_false(prefix: str, packet: Mapping[str, Any], keys: list[str], blockers: list[str]) -> None:
    for key in keys:
        if key in packet and packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def _health_source(packet: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = packet.get("health_baseline_packet")
    if isinstance(nested, Mapping) and nested:
        return nested
    return packet


def _confirmed_source(raw: Mapping[str, Any], health: Mapping[str, Any]) -> Mapping[str, Any]:
    for source in (raw.get("confirmed_autonomy_packet"), health.get("confirmed_autonomy_packet")):
        if isinstance(source, Mapping) and source:
            return source
    return {}


def build_qi_execution_health_packet_chain(
    *,
    health_baseline_packet: Mapping[str, Any],
    chain_context: Mapping[str, Any] | None = None,
) -> QiExecutionHealthPacketChainResult:
    ctx = _mapping(chain_context)
    raw = _mapping(health_baseline_packet)
    health = _health_source(raw)
    confirmed = _confirmed_source(raw, health)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("execution_health_packet_chain_enabled") is not True:
        blockers.append("execution_health_packet_chain_enabled_not_true")
    if ctx.get("read_only_chain_required") is not True:
        blockers.append("read_only_chain_required_not_true")
    if ctx.get("projection_only_required") is not True:
        blockers.append("projection_only_required_not_true")
    if ctx.get("additive_only_required") is not True:
        blockers.append("additive_only_required_not_true")
    if ctx.get("tighten_only_required") is not True:
        blockers.append("tighten_only_required_not_true")
    if ctx.get("same_root_required") is not True:
        blockers.append("same_root_required_not_true")

    for request_key in [
        "request_ledger_append",
        "request_execution_commit",
        "request_runtime_control",
        "request_scheduler_bypass",
        "request_notification_send",
        "request_ticket_create",
        "request_handover_perform",
        "request_memory_write",
        "request_memory_append",
        "request_world_update",
        "request_probe_execution",
        "request_authority_grant",
    ]:
        if ctx.get(request_key) is True:
            blockers.append(f"{request_key}_not_allowed")

    if health.get("health_status") != "QI_EXECUTION_HEALTH_BASELINE_READY":
        blockers.append("health_status_not_ready")
    if health.get("confirmed_autonomy") is not True:
        blockers.append("confirmed_autonomy_not_true")
    if health.get("confirmed_autonomy_scope") != "read_only_health_baseline_not_execution_authority":
        blockers.append("confirmed_autonomy_scope_invalid")
    if health.get("read_only_baseline") is not True:
        blockers.append("health_read_only_baseline_not_true")
    if health.get("projection_only") is not True:
        blockers.append("health_projection_only_not_true")

    _require_false("health", health, FORBIDDEN_EFFECT_KEYS, blockers)
    _require_false("raw_health_result", raw, FORBIDDEN_EFFECT_KEYS, blockers)
    _require_false("confirmed_autonomy", confirmed, FORBIDDEN_AUTHORITY_KEYS, blockers)

    if not confirmed:
        blockers.append("confirmed_autonomy_packet_missing")
    elif confirmed.get("confirmed_autonomy_scope") != "read_only_health_baseline_not_execution_authority":
        blockers.append("confirmed_autonomy_packet_scope_invalid")

    autonomy_health_root_digest = health.get("autonomy_health_root_digest", raw.get("autonomy_health_root_digest"))
    expected_root = ctx.get("expected_autonomy_health_root_digest")
    if expected_root is not None and str(expected_root) != str(autonomy_health_root_digest):
        blockers.append("autonomy_health_root_digest_mismatch")

    source_health_baseline_packet_id = health.get("health_baseline_packet_id", raw.get("health_baseline_packet_id"))
    source_confirmed_autonomy_packet_id = confirmed.get(
        "confirmed_autonomy_packet_id",
        health.get("confirmed_autonomy_packet_id", raw.get("confirmed_autonomy_packet_id")),
    )

    core = {
        "source_health_baseline_packet_id": source_health_baseline_packet_id,
        "source_confirmed_autonomy_packet_id": source_confirmed_autonomy_packet_id,
        "autonomy_health_root_digest": autonomy_health_root_digest,
        "chain_scope": "qi_execution_health_baseline_packet_chain",
        "read_only_chain": True,
        "projection_only": True,
        "additive_only": True,
        "tighten_only": True,
        "same_root_required": True,
        "execution_authority_granted": False,
    }
    packet_chain_root_digest = _sha_obj(core)
    packet_chain_id = "qi-exec-health-chain-" + packet_chain_root_digest[:16]
    release_packet_id = "qi-exec-health-release-" + _sha_obj({"chain": packet_chain_id, "stage": "release"})[:16]
    established_packet_id = "qi-exec-health-established-" + _sha_obj({"chain": packet_chain_id, "stage": "established"})[:16]
    confirmed_baseline_packet_id = "qi-exec-health-confirmed-" + _sha_obj({"chain": packet_chain_id, "stage": "confirmed_baseline"})[:16]
    finality_packet_id = "qi-exec-health-finality-" + _sha_obj({"chain": packet_chain_id, "stage": "finality"})[:16]

    ready = not blockers
    release_packet: dict[str, Any] = {}
    established_packet: dict[str, Any] = {}
    confirmed_baseline_packet: dict[str, Any] = {}
    finality_packet: dict[str, Any] = {}

    common_boundary = {
        "ledger_append_performed": False,
        "execution_committed": False,
        "runtime_control_performed": False,
        "scheduler_bypass_performed": False,
        "notification_sent": False,
        "ticket_created": False,
        "handover_performed": False,
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
    }

    if ready:
        release_packet = dict(core)
        release_packet.update(common_boundary)
        release_packet.update({
            "packet_id": release_packet_id,
            "packet_kind": "qi_execution_health_release_packet_v0_1",
            "packet_status": "QI_EXECUTION_HEALTH_RELEASE_PACKET_READY",
            "release_scope": "health_baseline_release_not_execution_release",
        })

        established_packet = dict(core)
        established_packet.update(common_boundary)
        established_packet.update({
            "packet_id": established_packet_id,
            "packet_kind": "qi_execution_health_established_packet_v0_1",
            "packet_status": "QI_EXECUTION_HEALTH_ESTABLISHED_PACKET_READY",
            "established_scope": "health_baseline_established_not_runtime_authority",
            "source_release_packet_id": release_packet_id,
        })

        confirmed_baseline_packet = dict(core)
        confirmed_baseline_packet.update(common_boundary)
        confirmed_baseline_packet.update({
            "packet_id": confirmed_baseline_packet_id,
            "packet_kind": "qi_execution_health_confirmed_baseline_packet_v0_1",
            "packet_status": "QI_EXECUTION_HEALTH_CONFIRMED_BASELINE_PACKET_READY",
            "confirmed_baseline_scope": "baseline_confirmation_not_execution_permission",
            "source_established_packet_id": established_packet_id,
        })

        finality_packet = dict(core)
        finality_packet.update(common_boundary)
        finality_packet.update({
            "packet_id": finality_packet_id,
            "packet_kind": "qi_execution_health_finality_packet_v0_1",
            "packet_status": "QI_EXECUTION_HEALTH_FINALITY_PACKET_READY",
            "finality_scope": "packet_chain_finality_not_authority_surface",
            "source_confirmed_baseline_packet_id": confirmed_baseline_packet_id,
            "packet_chain_id": packet_chain_id,
            "packet_chain_root_digest": packet_chain_root_digest,
        })

    return QiExecutionHealthPacketChainResult(
        chain_version="kuuos_runtime_daemon_qi_execution_health_packet_chain_v0_1",
        chain_status="QI_EXECUTION_HEALTH_PACKET_CHAIN_READY" if ready else "QI_EXECUTION_HEALTH_PACKET_CHAIN_BLOCKED",
        packet_chain_id=packet_chain_id,
        packet_chain_root_digest=packet_chain_root_digest,
        source_health_baseline_packet_id=str(source_health_baseline_packet_id) if source_health_baseline_packet_id is not None else None,
        source_confirmed_autonomy_packet_id=str(source_confirmed_autonomy_packet_id) if source_confirmed_autonomy_packet_id is not None else None,
        autonomy_health_root_digest=str(autonomy_health_root_digest) if autonomy_health_root_digest is not None else None,
        release_packet_id=release_packet_id,
        established_packet_id=established_packet_id,
        confirmed_baseline_packet_id=confirmed_baseline_packet_id,
        finality_packet_id=finality_packet_id,
        release_packet=release_packet,
        established_packet=established_packet,
        confirmed_baseline_packet=confirmed_baseline_packet,
        finality_packet=finality_packet,
        read_only_chain=True,
        projection_only=True,
        additive_only=True,
        tighten_only=True,
        same_root_required=True,
        ledger_append_performed=False,
        execution_committed=False,
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
        chain_blockers=blockers,
        chain_warnings=warnings,
    )
