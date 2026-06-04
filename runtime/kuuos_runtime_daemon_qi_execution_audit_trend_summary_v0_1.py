#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import pathlib
from typing import Any, Mapping


SAFE_ACTIONS = {"hold", "observe", "freeze", "handover"}
INTENT_ACTIONS = {"advance_tick", "notify", "ticket"}


@dataclass(frozen=True)
class QiExecutionAuditTrendSummaryResult:
    trend_version: str
    trend_status: str
    trend_packet_id: str
    ledger_path: str
    audit_entry_count: int
    audit_root_digest: str | None
    last_entry_digest: str | None
    staged_intent_count: int
    safe_fallback_count: int
    committed_execution_count: int
    action_counts: dict[str, int]
    guard_pass_rates: dict[str, float]
    mean_autonomy_reliability_score: float
    autonomy_reliability_class: str
    autonomy_trend: str
    review_recommended: bool
    review_reasons: list[str]
    read_only_summary: bool
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
    trend_packet: dict[str, Any]
    trend_blockers: list[str]
    trend_warnings: list[str]
    authority: str = "qi_execution_audit_trend_summary_read_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


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
        return "autonomy_reliability_rising"
    if s < -0.03:
        return "autonomy_reliability_falling"
    return "autonomy_reliability_flat"


def _class(score: float) -> str:
    if score >= 0.92:
        return "excellent"
    if score >= 0.80:
        return "stable"
    if score >= 0.60:
        return "watch"
    return "review_required"


def _require_false(prefix: str, packet: Mapping[str, Any], blockers: list[str]) -> None:
    for key in [
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
    ]:
        if key in packet and packet.get(key) is not False:
            blockers.append(f"{prefix}_{key}_not_false")


def _score_entry(entry: Mapping[str, Any]) -> float:
    score = 1.0
    if entry.get("execution_committed") is True:
        score -= 1.0
    selected = str(entry.get("selected_action") or "hold")
    if selected in SAFE_ACTIONS and entry.get("execution_intent_staged") is not True:
        score += 0.02
    if selected in INTENT_ACTIONS and entry.get("execution_intent_staged") is True and entry.get("authority_guard_passed") is True:
        score += 0.01
    for key in [
        "process_tensor_guard_passed",
        "decisionos_guard_passed",
        "cbf_guard_passed",
        "token_guard_passed",
        "recovery_guard_passed",
        "nonmarkov_guard_passed",
    ]:
        if entry.get(key) is not True:
            score -= 0.08
    if selected in INTENT_ACTIONS and entry.get("authority_guard_passed") is not True:
        score -= 0.20
    return max(0.0, min(1.0, score))


def build_qi_execution_audit_trend_summary(
    *,
    ledger_path: str | pathlib.Path,
    trend_context: Mapping[str, Any] | None = None,
) -> QiExecutionAuditTrendSummaryResult:
    ctx = _mapping(trend_context)
    path = pathlib.Path(ledger_path)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("execution_audit_trend_summary_enabled") is not True:
        blockers.append("execution_audit_trend_summary_enabled_not_true")
    if ctx.get("read_only_summary_required") is not True:
        blockers.append("read_only_summary_required_not_true")
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

    try:
        entries = _read_jsonl(path)
    except Exception as exc:  # pragma: no cover
        entries = []
        blockers.append("execution_audit_ledger_parse_failed")
        warnings.append(str(exc))
    if not entries:
        blockers.append("execution_audit_ledger_empty")

    for entry in entries:
        if entry.get("intent_receipt_only") is not True:
            blockers.append("entry_not_intent_receipt_only")
            break
        if entry.get("read_only_receipt") is not True:
            blockers.append("entry_not_read_only_receipt")
            break
        if entry.get("projection_only_receipt") is not True:
            blockers.append("entry_not_projection_only_receipt")
            break
        _require_false("entry", entry, blockers)

    actions = [str(entry.get("selected_action") or "hold") for entry in entries]
    action_counts = {action: actions.count(action) for action in sorted(set(actions) | SAFE_ACTIONS | INTENT_ACTIONS)}
    staged_count = sum(1 for entry in entries if entry.get("execution_intent_staged") is True)
    committed_count = sum(1 for entry in entries if entry.get("execution_committed") is True)
    safe_count = sum(1 for action in actions if action in SAFE_ACTIONS)
    guard_keys = [
        "process_tensor_guard_passed",
        "decisionos_guard_passed",
        "cbf_guard_passed",
        "token_guard_passed",
        "authority_guard_passed",
        "recovery_guard_passed",
        "nonmarkov_guard_passed",
    ]
    guard_pass_rates = {
        key: _mean([1.0 if entry.get(key) is True else 0.0 for entry in entries])
        for key in guard_keys
    }
    entry_scores = [_score_entry(entry) for entry in entries]
    mean_score = _mean(entry_scores)
    reliability_class = _class(mean_score)
    autonomy_trend = _trend(entry_scores)
    review_reasons: list[str] = []
    if committed_count > 0:
        review_reasons.append("committed_execution_seen")
    if reliability_class == "review_required":
        review_reasons.append("low_autonomy_reliability")
    if autonomy_trend == "autonomy_reliability_falling":
        review_reasons.append("autonomy_reliability_falling")
    if guard_pass_rates.get("cbf_guard_passed", 1.0) < 0.8:
        review_reasons.append("cbf_guard_pass_rate_low")
    if guard_pass_rates.get("process_tensor_guard_passed", 1.0) < 0.8:
        review_reasons.append("process_tensor_guard_pass_rate_low")
    if staged_count > 0 and guard_pass_rates.get("authority_guard_passed", 0.0) < staged_count / max(1, len(entries)):
        review_reasons.append("authority_guard_inconsistency")
    review_recommended = bool(review_reasons)
    audit_root = _root_digest(entries)
    last_digest = _entry_digest(entries[-1]) if entries else None
    core = {
        "audit_root_digest": audit_root,
        "last_entry_digest": last_digest,
        "entry_count": len(entries),
        "mean_autonomy_reliability_score": round(mean_score, 6),
        "autonomy_reliability_class": reliability_class,
        "autonomy_trend": autonomy_trend,
        "read_only_summary": True,
        "projection_only": True,
    }
    trend_packet_id = "qi-exec-trend-" + _sha_obj(core)[:16]
    trend_packet = dict(core)
    trend_packet.update({
        "trend_packet_id": trend_packet_id,
        "trend_version": "kuuos_runtime_daemon_qi_execution_audit_trend_summary_v0_1",
        "trend_status": "QI_EXECUTION_AUDIT_TREND_SUMMARY_READY" if not blockers else "QI_EXECUTION_AUDIT_TREND_SUMMARY_BLOCKED",
        "staged_intent_count": staged_count,
        "safe_fallback_count": safe_count,
        "committed_execution_count": committed_count,
        "action_counts": action_counts,
        "guard_pass_rates": guard_pass_rates,
        "review_recommended": review_recommended,
        "review_reasons": review_reasons,
        "ledger_append_performed": False,
        "execution_committed": False,
        "runtime_control_performed": False,
        "scheduler_bypass_performed": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "world_update_performed": False,
        "probe_execution_performed": False,
    })
    ready = not blockers
    return QiExecutionAuditTrendSummaryResult(
        trend_version="kuuos_runtime_daemon_qi_execution_audit_trend_summary_v0_1",
        trend_status="QI_EXECUTION_AUDIT_TREND_SUMMARY_READY" if ready else "QI_EXECUTION_AUDIT_TREND_SUMMARY_BLOCKED",
        trend_packet_id=trend_packet_id,
        ledger_path=str(path),
        audit_entry_count=len(entries),
        audit_root_digest=audit_root,
        last_entry_digest=last_digest,
        staged_intent_count=staged_count,
        safe_fallback_count=safe_count,
        committed_execution_count=committed_count,
        action_counts=action_counts,
        guard_pass_rates=guard_pass_rates,
        mean_autonomy_reliability_score=mean_score,
        autonomy_reliability_class=reliability_class,
        autonomy_trend=autonomy_trend,
        review_recommended=review_recommended,
        review_reasons=review_reasons,
        read_only_summary=True,
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
        trend_packet=trend_packet if ready else {},
        trend_blockers=blockers,
        trend_warnings=warnings,
    )
