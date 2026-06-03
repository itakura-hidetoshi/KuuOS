#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import pathlib
from typing import Any, Mapping


SEVERITY_WEIGHT = {
    "none": 1.0,
    "low": 0.9,
    "medium": 0.7,
    "high": 0.4,
    "critical": 0.1,
}


@dataclass(frozen=True)
class QiObservabilityAuditTrendSummaryResult:
    trend_version: str
    trend_status: str
    trend_packet_id: str
    ledger_path: str
    audit_entry_count: int
    audit_root_digest: str | None
    last_entry_digest: str | None
    mean_reliability_score: float
    reliability_class: str
    severity_counts: dict[str, int]
    alert_rate: float
    nonzero_alert_rate: float
    reliability_trend: str
    review_recommended: bool
    review_reasons: list[str]
    read_only_summary: bool
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
    trend_packet: dict[str, Any]
    trend_blockers: list[str]
    trend_warnings: list[str]
    authority: str = "qi_observability_audit_trend_summary_read_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        value = json.loads(line)
        if isinstance(value, dict):
            rows.append(value)
    return rows


def _entry_digest(entry: Mapping[str, Any]) -> str:
    digest = entry.get("entry_digest")
    return str(digest) if digest else _sha_obj(entry)


def _root_digest(entries: list[dict[str, Any]]) -> str | None:
    if not entries:
        return None
    return _sha_obj({"entry_digests": [_entry_digest(entry) for entry in entries]})


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _slope(values: list[float]) -> float:
    n = len(values)
    if n < 2:
        return 0.0
    xs = list(range(n))
    mx = sum(xs) / n
    my = sum(values) / n
    denom = sum((x - mx) ** 2 for x in xs)
    if denom == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, values)) / denom


def _trend(values: list[float]) -> str:
    s = _slope(values)
    if s > 0.03:
        return "reliability_rising"
    if s < -0.03:
        return "reliability_falling"
    return "reliability_flat"


def _class(score: float) -> str:
    if score >= 0.9:
        return "excellent"
    if score >= 0.75:
        return "stable"
    if score >= 0.5:
        return "watch"
    return "review_required"


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
    ]:
        if key in packet and packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def build_qi_observability_audit_trend_summary(
    *,
    ledger_path: str | pathlib.Path,
    trend_context: Mapping[str, Any] | None = None,
) -> QiObservabilityAuditTrendSummaryResult:
    ctx = _mapping(trend_context)
    path = pathlib.Path(ledger_path)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("audit_trend_summary_enabled") is not True:
        blockers.append("audit_trend_summary_enabled_not_true")
    if ctx.get("read_only_summary_required") is not True:
        blockers.append("read_only_summary_required_not_true")
    if ctx.get("projection_only_required") is not True:
        blockers.append("projection_only_required_not_true")
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

    try:
        entries = _read_jsonl(path)
    except Exception as exc:  # pragma: no cover
        entries = []
        blockers.append("audit_ledger_parse_failed")
        warnings.append(str(exc))
    if not entries:
        blockers.append("audit_ledger_empty")

    for entry in entries:
        if entry.get("read_only_review_receipt") is not True:
            blockers.append("entry_not_read_only_review_receipt")
            break
        if entry.get("append_only") is not True:
            blockers.append("entry_not_append_only")
            break
        _require_false("entry", entry, blockers)

    severities = [str(entry.get("alert_severity") or "none") for entry in entries]
    counts = {key: severities.count(key) for key in ["none", "low", "medium", "high", "critical"]}
    scores = [SEVERITY_WEIGHT.get(sev, 0.6) for sev in severities]
    mean_score = _mean(scores)
    alert_counts = [int(entry.get("alert_count") or 0) for entry in entries]
    alert_rate = _mean([float(value) for value in alert_counts])
    nonzero_rate = sum(1 for value in alert_counts if value > 0) / len(alert_counts) if alert_counts else 0.0
    reliability_trend = _trend(scores)
    reliability_class = _class(mean_score)
    review_reasons: list[str] = []
    if reliability_class == "review_required":
        review_reasons.append("low_mean_reliability_score")
    if reliability_trend == "reliability_falling":
        review_reasons.append("reliability_falling")
    if counts.get("critical", 0) > 0:
        review_reasons.append("critical_alert_seen")
    if nonzero_rate >= 0.5:
        review_reasons.append("frequent_nonzero_alerts")
    review_recommended = bool(review_reasons)
    audit_root = _root_digest(entries)
    last_digest = _entry_digest(entries[-1]) if entries else None
    core = {
        "audit_root_digest": audit_root,
        "last_entry_digest": last_digest,
        "entry_count": len(entries),
        "mean_reliability_score": round(mean_score, 6),
        "reliability_class": reliability_class,
        "reliability_trend": reliability_trend,
        "read_only_summary": True,
    }
    packet_id = "qi-audit-trend-" + _sha_obj(core)[:16]
    packet = dict(core)
    packet.update({
        "trend_packet_id": packet_id,
        "trend_version": "kuuos_runtime_daemon_qi_observability_audit_trend_summary_v0_2",
        "trend_status": "QI_OBSERVABILITY_AUDIT_TREND_SUMMARY_READY" if not blockers else "QI_OBSERVABILITY_AUDIT_TREND_SUMMARY_BLOCKED",
        "severity_counts": counts,
        "alert_rate": alert_rate,
        "nonzero_alert_rate": nonzero_rate,
        "review_recommended": review_recommended,
        "review_reasons": review_reasons,
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
    ready = not blockers
    return QiObservabilityAuditTrendSummaryResult(
        trend_version="kuuos_runtime_daemon_qi_observability_audit_trend_summary_v0_2",
        trend_status="QI_OBSERVABILITY_AUDIT_TREND_SUMMARY_READY" if ready else "QI_OBSERVABILITY_AUDIT_TREND_SUMMARY_BLOCKED",
        trend_packet_id=packet_id,
        ledger_path=str(path),
        audit_entry_count=len(entries),
        audit_root_digest=audit_root,
        last_entry_digest=last_digest,
        mean_reliability_score=mean_score,
        reliability_class=reliability_class,
        severity_counts=counts,
        alert_rate=alert_rate,
        nonzero_alert_rate=nonzero_rate,
        reliability_trend=reliability_trend,
        review_recommended=review_recommended,
        review_reasons=review_reasons,
        read_only_summary=True,
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
        trend_packet=packet if ready else {},
        trend_blockers=blockers,
        trend_warnings=warnings,
    )
