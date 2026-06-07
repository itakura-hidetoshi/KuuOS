#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ALLOWED_RUNNER_BIAS = {"continue", "observe", "retry", "hold"}
PROGRESS_CLASSES = {
    "safe_progress_continue",
    "observe_with_progress_obligation",
    "retry_with_rebalance_probe",
    "hold_with_review_exit",
    "progress_gap_detected",
}


@dataclass(frozen=True)
class QiProgressBearingSafetyGovernorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    runner_mode_bias: str
    progress_class: str
    progress_action: str
    safety_packet_path: str
    receipt_path: str
    audit_path: str
    safety_packet_written: bool
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


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _recent(rows: list[dict[str, Any]], n: int = 5) -> list[dict[str, Any]]:
    return rows[-n:] if n > 0 else []


def _completed_count(rows: list[dict[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("outcome_class") == "runner_completed")


def _blocked_count(rows: list[dict[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("outcome_class") == "blocked_or_not_run")


def _held_count(rows: list[dict[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("outcome_class") == "held_by_policy")


def _classify(bias: Mapping[str, Any], outcomes: list[dict[str, Any]]) -> tuple[str, str, list[str]]:
    runner_mode_bias = str(bias.get("runner_mode_bias", "unknown"))
    recent = _recent(outcomes, 5)
    completed = _completed_count(recent)
    blocked = _blocked_count(recent)
    held = _held_count(recent)
    reasons: list[str] = []
    if completed == 0 and (held + blocked) >= 3:
        reasons.append("recent_history_has_no_completed_progress")
        return "progress_gap_detected", "open_small_probe_or_review_exit", reasons
    if runner_mode_bias == "continue":
        reasons.append("stable_bias_allows_light_progress")
        return "safe_progress_continue", "advance_light", reasons
    if runner_mode_bias == "observe":
        reasons.append("observation_must_reduce_uncertainty")
        return "observe_with_progress_obligation", "observe_then_replan", reasons
    if runner_mode_bias == "retry":
        reasons.append("retry_requires_rebalance_probe")
        return "retry_with_rebalance_probe", "rebalance_then_retry", reasons
    if runner_mode_bias == "hold":
        reasons.append("hold_requires_review_exit")
        return "hold_with_review_exit", "hold_but_require_exit_condition", reasons
    reasons.append("unknown_bias")
    return "progress_gap_detected", "open_small_probe_or_review_exit", reasons


def _packet(bias: Mapping[str, Any], policy: Mapping[str, Any], outcomes: list[dict[str, Any]]) -> dict[str, Any]:
    progress_class, action, reasons = _classify(bias, outcomes)
    suggested_cycles = _i(bias.get("suggested_max_bridge_cycles"), _i(policy.get("max_bridge_cycles"), 1))
    suggested_steps = _i(bias.get("suggested_max_loop_steps_per_cycle"), _i(policy.get("max_loop_steps_per_cycle"), 1))
    return {
        "version": "qi_progress_bearing_safety_packet_v7_7",
        "progress_required": True,
        "progress_class": progress_class,
        "progress_action": action,
        "runner_mode_bias": str(bias.get("runner_mode_bias", "unknown")),
        "qi_state": str(bias.get("qi_state", "unknown")),
        "next_policy_bias": str(bias.get("next_policy_bias", "unknown")),
        "suggested_max_bridge_cycles": max(1, suggested_cycles),
        "suggested_max_loop_steps_per_cycle": max(1, suggested_steps),
        "review_exit_required": progress_class == "hold_with_review_exit",
        "small_probe_required": progress_class in {"progress_gap_detected", "observe_with_progress_obligation", "retry_with_rebalance_probe"},
        "progress_reason_codes": reasons,
        "source_bias_digest": _sha(dict(bias)),
        "current_policy_digest": _sha(dict(policy)),
        "recent_outcome_digest": _sha(_recent(outcomes, 5)),
        "boundary": {
            "progress_bearing_safety": True,
            "safety_without_progress_is_not_sufficient": True,
            "does_not_overwrite_policy": True,
            "does_not_run_runner": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_progress_bearing_safety_governor(*, runtime_context: Mapping[str, Any], progress_safety_license: Mapping[str, Any]) -> QiProgressBearingSafetyGovernorResult:
    ctx = _m(runtime_context)
    lic = _m(progress_safety_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    bias_path = root / "qi_process_tensor_policy_bias_packet.json"
    policy_path = root / "qi_github_actions_lifecycle_policy_packet.json"
    outcome_path = root / "qi_github_actions_policy_outcome_ledger.jsonl"
    safety_path = root / "qi_progress_bearing_safety_packet.json"
    receipt_path = root / "qi_progress_bearing_safety_governor_receipt.json"
    audit_path = root / "qi_progress_bearing_safety_governor_audit.jsonl"

    if ctx.get("qi_progress_bearing_safety_governor_enabled") is not True:
        blockers.append("qi_progress_bearing_safety_governor_enabled_not_true")
    if ctx.get("apply_qi_progress_bearing_safety_governor") is not True:
        blockers.append("apply_qi_progress_bearing_safety_governor_not_true")
    if lic.get("license_status") != "QI_PROGRESS_BEARING_SAFETY_GOVERNOR_LICENSE_READY":
        blockers.append("qi_progress_bearing_safety_governor_license_not_ready")
    for name in ["bias_packet_read_allowed", "current_policy_read_allowed", "policy_outcome_read_allowed", "safety_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    bias = _read_json(bias_path)
    policy = _read_json(policy_path)
    outcomes = _read_jsonl(outcome_path)
    if not bias:
        blockers.append("qi_process_tensor_policy_bias_packet_missing_or_invalid")
    if not policy:
        blockers.append("lifecycle_policy_packet_missing_or_invalid")
    if not outcomes:
        warnings.append("policy_outcome_ledger_empty_or_missing")
    runner_mode_bias = str(bias.get("runner_mode_bias", "unknown")) if bias else "unknown"
    if runner_mode_bias not in ALLOWED_RUNNER_BIAS:
        blockers.append("runner_mode_bias_not_allowlisted")
    if bias and bias.get("boundary", {}).get("bias_only") is not True:
        blockers.append("bias_packet_boundary_invalid")

    packet: dict[str, Any] = {}
    written = False
    progress_class = "unknown"
    action = "unknown"
    if not blockers:
        packet = _packet(bias, policy, outcomes)
        progress_class = str(packet["progress_class"])
        action = str(packet["progress_action"])
        if progress_class not in PROGRESS_CLASSES:
            blockers.append("progress_class_not_allowlisted")
        else:
            _write_json(safety_path, packet)
            written = True

    status = "QI_PROGRESS_BEARING_SAFETY_GOVERNOR_READY" if not blockers else "QI_PROGRESS_BEARING_SAFETY_GOVERNOR_BLOCKED"
    packet_id = "qi-progress-bearing-safety-" + _sha({"bias": bias, "policy": policy, "packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_progress_bearing_safety_governor_v7_7",
        "status": status,
        "packet_id": packet_id,
        "runner_mode_bias": runner_mode_bias,
        "progress_class": progress_class,
        "progress_action": action,
        "safety_packet_written": written,
        "safety_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiProgressBearingSafetyGovernorResult(
        "kuuos_runtime_daemon_qi_progress_bearing_safety_governor_v7_7",
        status,
        packet_id,
        str(root),
        runner_mode_bias,
        progress_class,
        action,
        str(safety_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
