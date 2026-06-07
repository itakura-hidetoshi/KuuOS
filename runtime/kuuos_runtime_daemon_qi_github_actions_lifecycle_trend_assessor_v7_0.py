#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import collections
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


KNOWN_STOP_REASONS = {
    "await_dispatch_result",
    "await_external_call",
    "max_bridge_cycles_reached",
    "max_steps_reached",
    "waiting_for_external_observation",
    "waiting_for_connector_operation",
    "internal_loop_blocked",
    "external_bridge_blocked",
}

REVIEW_STOP_REASONS = {
    "internal_loop_blocked",
    "external_bridge_blocked",
}

RETRY_STOP_REASONS = {
    "await_dispatch_result",
    "waiting_for_connector_operation",
}

OBSERVE_STOP_REASONS = {
    "await_external_call",
    "waiting_for_external_observation",
}


@dataclass(frozen=True)
class QiGitHubActionsLifecycleTrendAssessorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    records_used: int
    cycle_records_used: int
    summary_records_used: int
    policy_hint: str
    trend_packet_path: str
    receipt_path: str
    audit_path: str
    trend_packet_written: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _i(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            out.append(value)
    return out


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _last(records: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    if limit <= 0:
        return []
    return records[-limit:]


def _counter(records: list[dict[str, Any]], key: str) -> dict[str, int]:
    c: collections.Counter[str] = collections.Counter()
    for item in records:
        value = str(item.get(key, "unknown"))
        c[value] += 1
    return dict(sorted(c.items()))


def _policy(summary_records: list[dict[str, Any]], cycle_records: list[dict[str, Any]]) -> str:
    if not summary_records and not cycle_records:
        return "observe_more"
    stops = [str(item.get("stop_reason", "unknown")) for item in summary_records]
    cycle_external = [str(item.get("external_selected_stage", "unknown")) for item in cycle_records]
    if any(s in REVIEW_STOP_REASONS for s in stops):
        return "hold_for_review"
    if stops and all(s == "await_dispatch_result" for s in stops[-min(len(stops), 3):]):
        return "stable_continue"
    retry_count = sum(1 for s in stops if s in RETRY_STOP_REASONS)
    observe_count = sum(1 for s in stops if s in OBSERVE_STOP_REASONS)
    if retry_count >= max(2, observe_count + 1):
        return "retry_heavy"
    if observe_count >= max(2, retry_count + 1):
        return "observe_more"
    if cycle_external and cycle_external.count("await_dispatch_result") >= max(2, len(cycle_external) // 2 + 1):
        return "stable_continue"
    return "observe_more"


def _trend_packet(records: list[dict[str, Any]], limit: int) -> dict[str, Any]:
    sample = _last(records, limit)
    cycle_records = [r for r in sample if r.get("record_type") == "cycle"]
    summary_records = [r for r in sample if r.get("record_type") == "summary"]
    policy = _policy(summary_records, cycle_records)
    unknown_stops = sorted({str(r.get("stop_reason", "unknown")) for r in summary_records if str(r.get("stop_reason", "unknown")) not in KNOWN_STOP_REASONS})
    return {
        "version": "qi_github_actions_lifecycle_trend_packet_v7_0",
        "records_used": len(sample),
        "cycle_records_used": len(cycle_records),
        "summary_records_used": len(summary_records),
        "policy_hint": policy,
        "stop_reason_counts": _counter(summary_records, "stop_reason"),
        "internal_final_stage_counts": _counter(cycle_records, "internal_final_stage"),
        "external_selected_stage_counts": _counter(cycle_records, "external_selected_stage"),
        "unknown_stop_reasons": unknown_stops,
        "ledger_sample_digest": _sha(sample),
        "epoch": int(time.time()),
    }


def build_qi_github_actions_lifecycle_trend_assessor(*, runtime_context: Mapping[str, Any], trend_assessor_license: Mapping[str, Any]) -> QiGitHubActionsLifecycleTrendAssessorResult:
    ctx = _m(runtime_context)
    lic = _m(trend_assessor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    ledger_path = root / "qi_github_actions_bridge_lifecycle_ledger.jsonl"
    trend_packet_path = root / "qi_github_actions_lifecycle_trend_packet.json"
    receipt_path = root / "qi_github_actions_lifecycle_trend_assessor_receipt.json"
    audit_path = root / "qi_github_actions_lifecycle_trend_assessor_audit.jsonl"

    if ctx.get("qi_github_actions_lifecycle_trend_assessor_enabled") is not True:
        blockers.append("qi_github_actions_lifecycle_trend_assessor_enabled_not_true")
    if ctx.get("apply_github_actions_lifecycle_trend_assessor") is not True:
        blockers.append("apply_github_actions_lifecycle_trend_assessor_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_LIFECYCLE_TREND_ASSESSOR_LICENSE_READY":
        blockers.append("github_actions_lifecycle_trend_assessor_license_not_ready")
    for name in ["lifecycle_ledger_read_allowed", "trend_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    limit = _i(ctx.get("trend_window_records", 50), 50)
    if limit < 1:
        blockers.append("trend_window_records_invalid")
        limit = 0
    if limit > 500:
        warnings.append("trend_window_records_capped_to_500")
        limit = 500

    records = _read_jsonl(ledger_path)
    if not records:
        blockers.append("lifecycle_ledger_empty_or_missing")
    packet: dict[str, Any] = {}
    written = False
    if not blockers:
        packet = _trend_packet(records, limit)
        _write_json(trend_packet_path, packet)
        written = True
    status = "QI_GITHUB_ACTIONS_LIFECYCLE_TREND_ASSESSOR_READY" if not blockers else "QI_GITHUB_ACTIONS_LIFECYCLE_TREND_ASSESSOR_BLOCKED"
    packet_id = "qi-github-actions-lifecycle-trend-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_lifecycle_trend_assessor_v7_0",
        "status": status,
        "packet_id": packet_id,
        "records_used": int(packet.get("records_used", 0)),
        "cycle_records_used": int(packet.get("cycle_records_used", 0)),
        "summary_records_used": int(packet.get("summary_records_used", 0)),
        "policy_hint": str(packet.get("policy_hint", "none")),
        "trend_packet_written": written,
        "trend_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsLifecycleTrendAssessorResult(
        "kuuos_runtime_daemon_qi_github_actions_lifecycle_trend_assessor_v7_0",
        status,
        packet_id,
        str(root),
        int(packet.get("records_used", 0)),
        int(packet.get("cycle_records_used", 0)),
        int(packet.get("summary_records_used", 0)),
        str(packet.get("policy_hint", "none")),
        str(trend_packet_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
