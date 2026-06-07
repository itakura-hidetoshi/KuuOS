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


KNOWN_OUTCOME_CLASSES = {
    "held_by_policy",
    "runner_completed",
    "blocked_or_not_run",
    "hold_policy_not_respected",
    "unknown_outcome",
}

POSITIVE_OUTCOMES = {
    "held_by_policy",
    "runner_completed",
}

NEGATIVE_OUTCOMES = {
    "blocked_or_not_run",
    "hold_policy_not_respected",
    "unknown_outcome",
}

POLICY_HINTS = {
    "stable_continue",
    "observe_more",
    "retry_heavy",
    "hold_for_review",
}


@dataclass(frozen=True)
class QiGitHubActionsPolicyEffectivenessAssessorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    records_used: int
    dominant_policy_hint: str
    effectiveness_hint: str
    effectiveness_packet_path: str
    receipt_path: str
    audit_path: str
    effectiveness_packet_written: bool
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


def _policy_stats(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = {}
    for hint in POLICY_HINTS:
        stats[hint] = {
            "total": 0,
            "positive": 0,
            "negative": 0,
            "held": 0,
            "completed": 0,
            "blocked": 0,
            "unknown": 0,
            "positive_rate": 0.0,
            "block_rate": 0.0,
        }
    for item in records:
        hint = str(item.get("policy_hint", "unknown"))
        if hint not in stats:
            stats[hint] = {
                "total": 0,
                "positive": 0,
                "negative": 0,
                "held": 0,
                "completed": 0,
                "blocked": 0,
                "unknown": 0,
                "positive_rate": 0.0,
                "block_rate": 0.0,
            }
        outcome = str(item.get("outcome_class", "unknown_outcome"))
        stats[hint]["total"] += 1
        if outcome in POSITIVE_OUTCOMES:
            stats[hint]["positive"] += 1
        if outcome in NEGATIVE_OUTCOMES:
            stats[hint]["negative"] += 1
        if outcome == "held_by_policy":
            stats[hint]["held"] += 1
        elif outcome == "runner_completed":
            stats[hint]["completed"] += 1
        elif outcome == "blocked_or_not_run":
            stats[hint]["blocked"] += 1
        else:
            stats[hint]["unknown"] += 1
    for hint, entry in stats.items():
        total = int(entry["total"])
        if total:
            entry["positive_rate"] = round(float(entry["positive"]) / total, 4)
            entry["block_rate"] = round(float(entry["blocked"]) / total, 4)
    return stats


def _dominant_policy(stats: Mapping[str, Mapping[str, Any]]) -> str:
    best = "none"
    best_total = -1
    best_rate = -1.0
    for hint, entry in stats.items():
        total = int(entry.get("total", 0) or 0)
        rate = float(entry.get("positive_rate", 0.0) or 0.0)
        if total > best_total or (total == best_total and rate > best_rate):
            best = str(hint)
            best_total = total
            best_rate = rate
    return best


def _hint(stats: Mapping[str, Mapping[str, Any]], records: list[dict[str, Any]]) -> str:
    if not records:
        return "collect_more_outcomes"
    review = stats.get("hold_for_review", {})
    if int(review.get("total", 0) or 0) and float(review.get("positive_rate", 0.0) or 0.0) >= 0.8:
        return "respect_hold_boundary"
    blocked_total = sum(int(entry.get("blocked", 0) or 0) for entry in stats.values())
    total = sum(int(entry.get("total", 0) or 0) for entry in stats.values())
    if total and blocked_total / total >= 0.4:
        return "reduce_autonomy_and_observe"
    stable = stats.get("stable_continue", {})
    if int(stable.get("total", 0) or 0) >= 2 and float(stable.get("positive_rate", 0.0) or 0.0) >= 0.75:
        return "prefer_stable_continue"
    observe = stats.get("observe_more", {})
    if int(observe.get("total", 0) or 0) >= 2 and float(observe.get("positive_rate", 0.0) or 0.0) >= 0.75:
        return "prefer_observe_more"
    retry = stats.get("retry_heavy", {})
    if int(retry.get("total", 0) or 0) >= 2 and float(retry.get("positive_rate", 0.0) or 0.0) >= 0.75:
        return "prefer_retry_heavy"
    return "collect_more_outcomes"


def _packet(records: list[dict[str, Any]], limit: int) -> dict[str, Any]:
    sample = _last(records, limit)
    stats = _policy_stats(sample)
    return {
        "version": "qi_github_actions_policy_effectiveness_packet_v7_4",
        "records_used": len(sample),
        "policy_stats": stats,
        "dominant_policy_hint": _dominant_policy(stats),
        "effectiveness_hint": _hint(stats, sample),
        "known_outcome_classes": sorted(KNOWN_OUTCOME_CLASSES),
        "unknown_outcome_classes": sorted({str(r.get("outcome_class", "unknown")) for r in sample if str(r.get("outcome_class", "unknown")) not in KNOWN_OUTCOME_CLASSES}),
        "ledger_sample_digest": _sha(sample),
        "epoch": int(time.time()),
    }


def build_qi_github_actions_policy_effectiveness_assessor(*, runtime_context: Mapping[str, Any], effectiveness_assessor_license: Mapping[str, Any]) -> QiGitHubActionsPolicyEffectivenessAssessorResult:
    ctx = _m(runtime_context)
    lic = _m(effectiveness_assessor_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    ledger_path = root / "qi_github_actions_policy_outcome_ledger.jsonl"
    packet_path = root / "qi_github_actions_policy_effectiveness_packet.json"
    receipt_path = root / "qi_github_actions_policy_effectiveness_assessor_receipt.json"
    audit_path = root / "qi_github_actions_policy_effectiveness_assessor_audit.jsonl"

    if ctx.get("qi_github_actions_policy_effectiveness_assessor_enabled") is not True:
        blockers.append("qi_github_actions_policy_effectiveness_assessor_enabled_not_true")
    if ctx.get("apply_github_actions_policy_effectiveness_assessor") is not True:
        blockers.append("apply_github_actions_policy_effectiveness_assessor_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_POLICY_EFFECTIVENESS_ASSESSOR_LICENSE_READY":
        blockers.append("github_actions_policy_effectiveness_assessor_license_not_ready")
    for name in ["policy_outcome_ledger_read_allowed", "effectiveness_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    limit = _i(ctx.get("effectiveness_window_records", 50), 50)
    if limit < 1:
        blockers.append("effectiveness_window_records_invalid")
        limit = 0
    if limit > 500:
        warnings.append("effectiveness_window_records_capped_to_500")
        limit = 500

    records = [r for r in _read_jsonl(ledger_path) if r.get("record_type") == "policy_outcome"]
    if not records:
        blockers.append("policy_outcome_ledger_empty_or_missing")
    packet: dict[str, Any] = {}
    written = False
    if not blockers:
        packet = _packet(records, limit)
        _write_json(packet_path, packet)
        written = True
    status = "QI_GITHUB_ACTIONS_POLICY_EFFECTIVENESS_ASSESSOR_READY" if not blockers else "QI_GITHUB_ACTIONS_POLICY_EFFECTIVENESS_ASSESSOR_BLOCKED"
    packet_id = "qi-github-actions-policy-effectiveness-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_policy_effectiveness_assessor_v7_4",
        "status": status,
        "packet_id": packet_id,
        "records_used": int(packet.get("records_used", 0)),
        "dominant_policy_hint": str(packet.get("dominant_policy_hint", "none")),
        "effectiveness_hint": str(packet.get("effectiveness_hint", "none")),
        "effectiveness_packet_written": written,
        "effectiveness_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsPolicyEffectivenessAssessorResult(
        "kuuos_runtime_daemon_qi_github_actions_policy_effectiveness_assessor_v7_4",
        status,
        packet_id,
        str(root),
        int(packet.get("records_used", 0)),
        str(packet.get("dominant_policy_hint", "none")),
        str(packet.get("effectiveness_hint", "none")),
        str(packet_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
