#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class QiObservabilityHealthBaselinePacketResult:
    health_baseline_version: str
    health_baseline_status: str
    health_baseline_packet_id: str
    health_baseline_root_digest: str
    source_trend_packet_id: str | None
    source_audit_root_digest: str | None
    source_last_entry_digest: str | None
    mean_reliability_score: float
    reliability_class: str | None
    reliability_trend: str | None
    review_recommended: bool
    review_reasons: list[str]
    observability_health_confirmed: bool
    confirmed_observability_packet: bool
    receipt_only_health_baseline: bool
    read_only_health_baseline: bool
    projection_only: bool
    ledger_append_performed: bool
    notification_sent: bool
    ticket_created: bool
    runtime_control_authority: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    health_baseline_packet: dict[str, Any]
    health_baseline_blockers: list[str]
    health_baseline_warnings: list[str]
    authority: str = "qi_observability_health_baseline_receipt_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in [
        "ledger_append_performed",
        "notification_sent",
        "ticket_created",
        "runtime_control_authority",
        "memory_write_performed",
        "memory_append_performed",
        "memory_overwrite_performed",
        "world_update_performed",
        "control_packet_mutation_performed",
        "probe_execution_performed",
        "grants_probe_execution_authority",
        "grants_world_update_authority",
        "grants_memory_overwrite_authority",
    ]:
        if key in packet and packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def build_qi_observability_health_baseline_packet(
    *,
    trend_packet: Mapping[str, Any],
    health_context: Mapping[str, Any] | None = None,
) -> QiObservabilityHealthBaselinePacketResult:
    trend = _mapping(trend_packet)
    ctx = _mapping(health_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("observability_health_baseline_enabled") is not True:
        blockers.append("observability_health_baseline_enabled_not_true")
    if ctx.get("confirmed_observability_required") is not True:
        blockers.append("confirmed_observability_required_not_true")
    if ctx.get("receipt_only_required") is not True:
        blockers.append("receipt_only_required_not_true")
    if ctx.get("read_only_required") is not True:
        blockers.append("read_only_required_not_true")
    if ctx.get("request_ledger_append") is True:
        blockers.append("ledger_append_requested")
    if ctx.get("request_notification_send") is True:
        blockers.append("notification_send_requested")
    if ctx.get("request_ticket_create") is True:
        blockers.append("ticket_create_requested")
    if ctx.get("request_runtime_control") is True:
        blockers.append("runtime_control_requested")
    if ctx.get("request_memory_write") is True or ctx.get("request_memory_append") is True:
        blockers.append("memory_write_or_append_requested")
    if ctx.get("request_world_update") is True:
        blockers.append("world_update_requested")
    if ctx.get("request_probe_execution") is True:
        blockers.append("probe_execution_requested")

    if trend.get("trend_status") != "QI_OBSERVABILITY_AUDIT_TREND_SUMMARY_READY":
        blockers.append("trend_summary_not_ready")
    if trend.get("read_only_summary") is not True:
        blockers.append("trend_summary_not_read_only")
    if trend.get("projection_only") is not True:
        blockers.append("trend_summary_not_projection_only")
    _require_false("trend_summary", trend, blockers)

    score = _float(trend.get("mean_reliability_score"), 0.0)
    reliability_class = str(trend.get("reliability_class")) if trend.get("reliability_class") else None
    reliability_trend = str(trend.get("reliability_trend")) if trend.get("reliability_trend") else None
    review_recommended = trend.get("review_recommended") is True
    review_reasons = trend.get("review_reasons") if isinstance(trend.get("review_reasons"), list) else []
    min_score = _float(ctx.get("min_confirmed_reliability_score"), 0.75)
    allow_watch = ctx.get("allow_watch_class") is True
    if score < min_score:
        blockers.append("mean_reliability_below_confirmed_threshold")
    if reliability_class == "review_required":
        blockers.append("reliability_class_review_required")
    if reliability_class == "watch" and not allow_watch:
        blockers.append("watch_class_not_allowed")
    if review_recommended and ctx.get("allow_confirm_with_review_recommended") is not True:
        blockers.append("review_recommended_not_allowed")

    material = {
        "source_trend_packet_id": trend.get("trend_packet_id"),
        "audit_root_digest": trend.get("audit_root_digest"),
        "last_entry_digest": trend.get("last_entry_digest"),
        "mean_reliability_score": round(score, 6),
        "reliability_class": reliability_class,
        "reliability_trend": reliability_trend,
        "review_recommended": review_recommended,
        "review_reasons": review_reasons,
        "health_context_id": ctx.get("health_context_id"),
        "receipt_only": True,
        "read_only": True,
    }
    root_digest = _sha_obj(material)
    packet_id = "qi-observe-health-" + root_digest[:16]
    ready = not blockers
    packet = dict(material)
    packet.update({
        "health_baseline_packet_id": packet_id,
        "health_baseline_version": "kuuos_runtime_daemon_qi_observability_health_baseline_packet_v0_2",
        "health_baseline_status": "QI_OBSERVABILITY_HEALTH_BASELINE_PACKET_READY" if ready else "QI_OBSERVABILITY_HEALTH_BASELINE_PACKET_BLOCKED",
        "health_baseline_root_digest": root_digest,
        "observability_health_confirmed": ready,
        "confirmed_observability_packet": ready,
        "receipt_only_health_baseline": True,
        "read_only_health_baseline": True,
        "projection_only": True,
        "ledger_append_performed": False,
        "notification_sent": False,
        "ticket_created": False,
        "runtime_control_authority": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "world_update_performed": False,
        "probe_execution_performed": False,
    })

    return QiObservabilityHealthBaselinePacketResult(
        health_baseline_version="kuuos_runtime_daemon_qi_observability_health_baseline_packet_v0_2",
        health_baseline_status="QI_OBSERVABILITY_HEALTH_BASELINE_PACKET_READY" if ready else "QI_OBSERVABILITY_HEALTH_BASELINE_PACKET_BLOCKED",
        health_baseline_packet_id=packet_id,
        health_baseline_root_digest=root_digest,
        source_trend_packet_id=str(trend.get("trend_packet_id")) if trend.get("trend_packet_id") else None,
        source_audit_root_digest=str(trend.get("audit_root_digest")) if trend.get("audit_root_digest") else None,
        source_last_entry_digest=str(trend.get("last_entry_digest")) if trend.get("last_entry_digest") else None,
        mean_reliability_score=score,
        reliability_class=reliability_class,
        reliability_trend=reliability_trend,
        review_recommended=review_recommended,
        review_reasons=[str(item) for item in review_reasons],
        observability_health_confirmed=ready,
        confirmed_observability_packet=ready,
        receipt_only_health_baseline=True,
        read_only_health_baseline=True,
        projection_only=True,
        ledger_append_performed=False,
        notification_sent=False,
        ticket_created=False,
        runtime_control_authority=False,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        health_baseline_packet=packet if ready else {},
        health_baseline_blockers=blockers,
        health_baseline_warnings=warnings,
    )
