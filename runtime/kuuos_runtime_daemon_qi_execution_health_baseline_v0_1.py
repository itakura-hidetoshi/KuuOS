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


@dataclass(frozen=True)
class QiExecutionHealthBaselineResult:
    health_version: str
    health_status: str
    health_baseline_packet_id: str
    confirmed_autonomy_packet_id: str
    autonomy_health_root_digest: str
    source_trend_packet_id: str | None
    audit_root_digest: str | None
    last_entry_digest: str | None
    audit_entry_count: int
    staged_intent_count: int
    safe_fallback_count: int
    committed_execution_count: int
    mean_autonomy_reliability_score: float
    reliability_threshold: float
    autonomy_reliability_class: str
    autonomy_trend: str
    review_recommended: bool
    review_reasons: list[str]
    confirmed_autonomy: bool
    confirmed_autonomy_scope: str
    confirmed_autonomy_packet: dict[str, Any]
    health_baseline_packet: dict[str, Any]
    read_only_baseline: bool
    projection_only: bool
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
    health_blockers: list[str]
    health_warnings: list[str]
    authority: str = "qi_execution_health_baseline_read_only_projection"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _number(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    return default


def _int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    return default


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in FORBIDDEN_EFFECT_KEYS:
        if key in packet and packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def _trend_source(packet: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = packet.get("trend_packet")
    if isinstance(nested, Mapping) and nested:
        return nested
    return packet


def build_qi_execution_health_baseline(
    *,
    trend_summary_packet: Mapping[str, Any],
    health_context: Mapping[str, Any] | None = None,
) -> QiExecutionHealthBaselineResult:
    ctx = _mapping(health_context)
    raw = _mapping(trend_summary_packet)
    trend = _trend_source(raw)
    blockers: list[str] = []
    warnings: list[str] = []

    threshold = _number(ctx.get("reliability_threshold"), 0.80)
    if threshold < 0.0 or threshold > 1.0:
        blockers.append("reliability_threshold_out_of_range")

    if ctx.get("execution_health_baseline_enabled") is not True:
        blockers.append("execution_health_baseline_enabled_not_true")
    if ctx.get("read_only_baseline_required") is not True:
        blockers.append("read_only_baseline_required_not_true")
    if ctx.get("projection_only_required") is not True:
        blockers.append("projection_only_required_not_true")

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
    ]:
        if ctx.get(request_key) is True:
            blockers.append(f"{request_key}_not_allowed")

    if trend.get("trend_status") != "QI_EXECUTION_AUDIT_TREND_SUMMARY_READY":
        blockers.append("trend_status_not_ready")
    if trend.get("read_only_summary") is not True:
        blockers.append("trend_read_only_summary_not_true")
    if trend.get("projection_only") is not True:
        blockers.append("trend_projection_only_not_true")

    _require_false("trend", trend, blockers)
    _require_false("raw_trend_result", raw, blockers)

    committed_count = _int(trend.get("committed_execution_count", raw.get("committed_execution_count")), 0)
    if committed_count != 0:
        blockers.append("committed_execution_count_not_zero")

    mean_score = _number(trend.get("mean_autonomy_reliability_score", raw.get("mean_autonomy_reliability_score")), 0.0)
    if mean_score < threshold:
        blockers.append("mean_autonomy_reliability_score_below_threshold")

    review_recommended = bool(trend.get("review_recommended", raw.get("review_recommended", False)))
    review_allowed = ctx.get("allow_review_recommended") is True
    if review_recommended and not review_allowed:
        blockers.append("review_recommended_without_explicit_allowance")
    if review_recommended and review_allowed:
        warnings.append("review_recommended_explicitly_allowed_for_baseline_record_only")

    audit_entry_count = _int(trend.get("audit_entry_count", trend.get("entry_count", raw.get("audit_entry_count"))), 0)
    staged_count = _int(trend.get("staged_intent_count", raw.get("staged_intent_count")), 0)
    safe_fallback_count = _int(trend.get("safe_fallback_count", raw.get("safe_fallback_count")), 0)
    source_trend_packet_id = trend.get("trend_packet_id", raw.get("trend_packet_id"))
    audit_root_digest = trend.get("audit_root_digest", raw.get("audit_root_digest"))
    last_entry_digest = trend.get("last_entry_digest", raw.get("last_entry_digest"))
    reliability_class = str(trend.get("autonomy_reliability_class", raw.get("autonomy_reliability_class", "unknown")))
    autonomy_trend = str(trend.get("autonomy_trend", raw.get("autonomy_trend", "unknown")))
    review_reasons = trend.get("review_reasons", raw.get("review_reasons", []))
    if not isinstance(review_reasons, list):
        review_reasons = []

    core = {
        "source_trend_packet_id": source_trend_packet_id,
        "audit_root_digest": audit_root_digest,
        "last_entry_digest": last_entry_digest,
        "audit_entry_count": audit_entry_count,
        "staged_intent_count": staged_count,
        "safe_fallback_count": safe_fallback_count,
        "committed_execution_count": committed_count,
        "mean_autonomy_reliability_score": round(mean_score, 6),
        "reliability_threshold": round(threshold, 6),
        "autonomy_reliability_class": reliability_class,
        "autonomy_trend": autonomy_trend,
        "review_recommended": review_recommended,
        "read_only_baseline": True,
        "projection_only": True,
    }
    autonomy_health_root_digest = _sha_obj(core)
    health_baseline_packet_id = "qi-exec-health-" + autonomy_health_root_digest[:16]
    confirmed_autonomy_packet_id = "qi-confirmed-autonomy-" + _sha_obj({
        "health_baseline_packet_id": health_baseline_packet_id,
        "autonomy_health_root_digest": autonomy_health_root_digest,
        "confirmed_scope": "read_only_health_baseline_not_execution_authority",
    })[:16]

    ready = not blockers
    confirmed_autonomy = ready
    health_baseline_packet: dict[str, Any] = {}
    confirmed_autonomy_packet: dict[str, Any] = {}
    if ready:
        health_baseline_packet = dict(core)
        health_baseline_packet.update({
            "health_version": "kuuos_runtime_daemon_qi_execution_health_baseline_v0_1",
            "health_status": "QI_EXECUTION_HEALTH_BASELINE_READY",
            "health_baseline_packet_id": health_baseline_packet_id,
            "autonomy_health_root_digest": autonomy_health_root_digest,
            "confirmed_autonomy_packet_id": confirmed_autonomy_packet_id,
            "confirmed_autonomy": True,
            "confirmed_autonomy_scope": "read_only_health_baseline_not_execution_authority",
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
        })
        confirmed_autonomy_packet = {
            "confirmed_autonomy_packet_id": confirmed_autonomy_packet_id,
            "source_health_baseline_packet_id": health_baseline_packet_id,
            "autonomy_health_root_digest": autonomy_health_root_digest,
            "confirmed_autonomy_status": "CONFIRMED_AUTONOMY_HEALTH_BASELINE_READY",
            "confirmed_autonomy_scope": "read_only_health_baseline_not_execution_authority",
            "execution_authority_granted": False,
            "execution_commit_allowed": False,
            "runtime_control_allowed": False,
            "scheduler_bypass_allowed": False,
            "ledger_append_allowed": False,
            "memory_write_allowed": False,
            "world_update_allowed": False,
            "probe_execution_allowed": False,
            "read_only_baseline": True,
            "projection_only": True,
        }

    return QiExecutionHealthBaselineResult(
        health_version="kuuos_runtime_daemon_qi_execution_health_baseline_v0_1",
        health_status="QI_EXECUTION_HEALTH_BASELINE_READY" if ready else "QI_EXECUTION_HEALTH_BASELINE_BLOCKED",
        health_baseline_packet_id=health_baseline_packet_id,
        confirmed_autonomy_packet_id=confirmed_autonomy_packet_id,
        autonomy_health_root_digest=autonomy_health_root_digest,
        source_trend_packet_id=str(source_trend_packet_id) if source_trend_packet_id is not None else None,
        audit_root_digest=str(audit_root_digest) if audit_root_digest is not None else None,
        last_entry_digest=str(last_entry_digest) if last_entry_digest is not None else None,
        audit_entry_count=audit_entry_count,
        staged_intent_count=staged_count,
        safe_fallback_count=safe_fallback_count,
        committed_execution_count=committed_count,
        mean_autonomy_reliability_score=mean_score,
        reliability_threshold=threshold,
        autonomy_reliability_class=reliability_class,
        autonomy_trend=autonomy_trend,
        review_recommended=review_recommended,
        review_reasons=[str(item) for item in review_reasons],
        confirmed_autonomy=confirmed_autonomy,
        confirmed_autonomy_scope="read_only_health_baseline_not_execution_authority",
        confirmed_autonomy_packet=confirmed_autonomy_packet,
        health_baseline_packet=health_baseline_packet,
        read_only_baseline=True,
        projection_only=True,
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
        health_blockers=blockers,
        health_warnings=warnings,
    )
