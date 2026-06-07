#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ALLOWED_POLICY_HINTS = {
    "stable_continue",
    "observe_more",
    "retry_heavy",
    "hold_for_review",
}

POLICY_PROFILES = {
    "stable_continue": {
        "runner_mode": "continue",
        "max_bridge_cycles": 5,
        "max_loop_steps_per_cycle": 5,
        "prefer_observation": False,
        "prefer_retry": False,
        "hold_required": False,
    },
    "observe_more": {
        "runner_mode": "observe",
        "max_bridge_cycles": 4,
        "max_loop_steps_per_cycle": 3,
        "prefer_observation": True,
        "prefer_retry": False,
        "hold_required": False,
    },
    "retry_heavy": {
        "runner_mode": "retry",
        "max_bridge_cycles": 3,
        "max_loop_steps_per_cycle": 4,
        "prefer_observation": False,
        "prefer_retry": True,
        "hold_required": False,
    },
    "hold_for_review": {
        "runner_mode": "hold",
        "max_bridge_cycles": 1,
        "max_loop_steps_per_cycle": 1,
        "prefer_observation": False,
        "prefer_retry": False,
        "hold_required": True,
    },
}


@dataclass(frozen=True)
class QiGitHubActionsLifecyclePolicyApplierResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    policy_hint: str
    runner_mode: str
    policy_packet_path: str
    receipt_path: str
    audit_path: str
    policy_packet_written: bool
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


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


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _policy_packet(trend: Mapping[str, Any], hint: str) -> dict[str, Any]:
    profile = dict(POLICY_PROFILES[hint])
    return {
        "version": "qi_github_actions_lifecycle_policy_packet_v7_1",
        "policy_hint": hint,
        "runner_mode": profile["runner_mode"],
        "max_bridge_cycles": profile["max_bridge_cycles"],
        "max_loop_steps_per_cycle": profile["max_loop_steps_per_cycle"],
        "prefer_observation": profile["prefer_observation"],
        "prefer_retry": profile["prefer_retry"],
        "hold_required": profile["hold_required"],
        "trend_records_used": int(trend.get("records_used", 0) or 0),
        "trend_summary_records_used": int(trend.get("summary_records_used", 0) or 0),
        "trend_cycle_records_used": int(trend.get("cycle_records_used", 0) or 0),
        "source_trend_digest": _sha(dict(trend)),
        "boundary": {
            "policy_hint_only": True,
            "does_not_call_github_connector": True,
            "does_not_run_loop_inside_applier": True,
            "hold_required_blocks_autonomous_runner": profile["hold_required"],
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_lifecycle_policy_applier(*, runtime_context: Mapping[str, Any], policy_applier_license: Mapping[str, Any]) -> QiGitHubActionsLifecyclePolicyApplierResult:
    ctx = _m(runtime_context)
    lic = _m(policy_applier_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    trend_path = root / "qi_github_actions_lifecycle_trend_packet.json"
    policy_path = root / "qi_github_actions_lifecycle_policy_packet.json"
    receipt_path = root / "qi_github_actions_lifecycle_policy_applier_receipt.json"
    audit_path = root / "qi_github_actions_lifecycle_policy_applier_audit.jsonl"

    if ctx.get("qi_github_actions_lifecycle_policy_applier_enabled") is not True:
        blockers.append("qi_github_actions_lifecycle_policy_applier_enabled_not_true")
    if ctx.get("apply_github_actions_lifecycle_policy_applier") is not True:
        blockers.append("apply_github_actions_lifecycle_policy_applier_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_LIFECYCLE_POLICY_APPLIER_LICENSE_READY":
        blockers.append("github_actions_lifecycle_policy_applier_license_not_ready")
    for name in ["trend_packet_read_allowed", "policy_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    trend = _read_json(trend_path)
    if not trend:
        blockers.append("lifecycle_trend_packet_missing_or_invalid")
    hint = str(trend.get("policy_hint", "unknown")) if trend else "unknown"
    if hint not in ALLOWED_POLICY_HINTS:
        blockers.append("policy_hint_not_allowlisted")
    if hint in ALLOWED_POLICY_HINTS and lic.get(f"allow_{hint}_policy") is not True:
        blockers.append(f"{hint}_not_allowed_by_lifecycle_policy_applier_license")
    if trend and int(trend.get("summary_records_used", 0) or 0) == 0:
        warnings.append("trend_has_no_summary_records")

    packet: dict[str, Any] = {}
    written = False
    runner_mode = "unknown"
    if not blockers:
        packet = _policy_packet(trend, hint)
        runner_mode = str(packet["runner_mode"])
        _write_json(policy_path, packet)
        written = True

    status = "QI_GITHUB_ACTIONS_LIFECYCLE_POLICY_APPLIER_READY" if not blockers else "QI_GITHUB_ACTIONS_LIFECYCLE_POLICY_APPLIER_BLOCKED"
    packet_id = "qi-github-actions-lifecycle-policy-" + _sha({"trend": trend, "packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_lifecycle_policy_applier_v7_1",
        "status": status,
        "packet_id": packet_id,
        "policy_hint": hint,
        "runner_mode": runner_mode,
        "policy_packet_written": written,
        "policy_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsLifecyclePolicyApplierResult(
        "kuuos_runtime_daemon_qi_github_actions_lifecycle_policy_applier_v7_1",
        status,
        packet_id,
        str(root),
        hint,
        runner_mode,
        str(policy_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
