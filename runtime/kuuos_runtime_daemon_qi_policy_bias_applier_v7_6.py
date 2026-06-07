#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ALLOWED_QI_STATES = {
    "smooth_circulation",
    "observation_deficiency",
    "retry_stagnation",
    "review_constraint",
    "mixed_turbulence",
}

ALLOWED_BIASES = {
    "stable_continue",
    "observe_more",
    "retry_heavy",
    "hold_for_review",
}

BIAS_PROFILE = {
    "stable_continue": {"runner_mode_bias": "continue", "cycle_delta": 1, "step_delta": 1, "hold_bias": False},
    "observe_more": {"runner_mode_bias": "observe", "cycle_delta": 0, "step_delta": -1, "hold_bias": False},
    "retry_heavy": {"runner_mode_bias": "retry", "cycle_delta": -1, "step_delta": 1, "hold_bias": False},
    "hold_for_review": {"runner_mode_bias": "hold", "cycle_delta": -3, "step_delta": -3, "hold_bias": True},
}


@dataclass(frozen=True)
class QiPolicyBiasApplierResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    qi_state: str
    next_policy_bias: str
    runner_mode_bias: str
    bias_packet_path: str
    receipt_path: str
    audit_path: str
    bias_packet_written: bool
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


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _bounded(base: int, delta: int, low: int, high: int) -> int:
    return max(low, min(high, base + delta))


def _bias_packet(coupling: Mapping[str, Any], current_policy: Mapping[str, Any]) -> dict[str, Any]:
    bias = str(coupling.get("next_policy_bias", "observe_more"))
    profile = BIAS_PROFILE[bias]
    base_cycles = _i(current_policy.get("max_bridge_cycles"), 3)
    base_steps = _i(current_policy.get("max_loop_steps_per_cycle"), 3)
    return {
        "version": "qi_process_tensor_policy_bias_packet_v7_6",
        "qi_state": str(coupling.get("qi_state", "unknown")),
        "next_policy_bias": bias,
        "runner_mode_bias": profile["runner_mode_bias"],
        "suggested_max_bridge_cycles": _bounded(base_cycles, int(profile["cycle_delta"]), 1, 20),
        "suggested_max_loop_steps_per_cycle": _bounded(base_steps, int(profile["step_delta"]), 1, 20),
        "hold_bias": profile["hold_bias"],
        "source_coupling_digest": _sha(dict(coupling)),
        "current_policy_digest": _sha(dict(current_policy)),
        "boundary": {
            "bias_only": True,
            "does_not_overwrite_lifecycle_policy_packet": True,
            "does_not_run_runner": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_policy_bias_applier(*, runtime_context: Mapping[str, Any], qi_policy_bias_applier_license: Mapping[str, Any]) -> QiPolicyBiasApplierResult:
    ctx = _m(runtime_context)
    lic = _m(qi_policy_bias_applier_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    coupling_path = root / "qi_process_tensor_policy_coupling_packet.json"
    policy_path = root / "qi_github_actions_lifecycle_policy_packet.json"
    bias_path = root / "qi_process_tensor_policy_bias_packet.json"
    receipt_path = root / "qi_policy_bias_applier_receipt.json"
    audit_path = root / "qi_policy_bias_applier_audit.jsonl"

    if ctx.get("qi_policy_bias_applier_enabled") is not True:
        blockers.append("qi_policy_bias_applier_enabled_not_true")
    if ctx.get("apply_qi_policy_bias_applier") is not True:
        blockers.append("apply_qi_policy_bias_applier_not_true")
    if lic.get("license_status") != "QI_POLICY_BIAS_APPLIER_LICENSE_READY":
        blockers.append("qi_policy_bias_applier_license_not_ready")
    for name in ["coupling_packet_read_allowed", "current_policy_read_allowed", "bias_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    coupling = _read_json(coupling_path)
    policy = _read_json(policy_path)
    if not coupling:
        blockers.append("qi_process_tensor_policy_coupling_packet_missing_or_invalid")
    if not policy:
        blockers.append("lifecycle_policy_packet_missing_or_invalid")
    qi_state = str(coupling.get("qi_state", "unknown")) if coupling else "unknown"
    bias = str(coupling.get("next_policy_bias", "unknown")) if coupling else "unknown"
    if qi_state not in ALLOWED_QI_STATES:
        blockers.append("qi_state_not_allowlisted")
    if bias not in ALLOWED_BIASES:
        blockers.append("next_policy_bias_not_allowlisted")
    if coupling and coupling.get("qi_process_tensor_considered") is not True:
        blockers.append("qi_process_tensor_considered_not_true")
    if policy and policy.get("hold_required") is True and bias != "hold_for_review":
        warnings.append("current_policy_hold_required_bias_not_hold")

    packet: dict[str, Any] = {}
    written = False
    runner_mode_bias = "unknown"
    if not blockers:
        packet = _bias_packet(coupling, policy)
        runner_mode_bias = str(packet["runner_mode_bias"])
        _write_json(bias_path, packet)
        written = True

    status = "QI_POLICY_BIAS_APPLIER_READY" if not blockers else "QI_POLICY_BIAS_APPLIER_BLOCKED"
    packet_id = "qi-policy-bias-applier-" + _sha({"coupling": coupling, "policy": policy, "packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_policy_bias_applier_v7_6",
        "status": status,
        "packet_id": packet_id,
        "qi_state": qi_state,
        "next_policy_bias": bias,
        "runner_mode_bias": runner_mode_bias,
        "bias_packet_written": written,
        "bias_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiPolicyBiasApplierResult(
        "kuuos_runtime_daemon_qi_policy_bias_applier_v7_6",
        status,
        packet_id,
        str(root),
        qi_state,
        bias,
        runner_mode_bias,
        str(bias_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
