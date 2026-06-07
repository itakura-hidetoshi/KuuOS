#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_integrated_bridge_runner_v6_8 import build_qi_github_actions_integrated_bridge_runner


ALLOWED_RUNNER_MODES = {
    "continue",
    "observe",
    "retry",
    "hold",
}


@dataclass(frozen=True)
class QiGitHubActionsPolicyAwareRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    runner_mode: str
    policy_hint: str
    execution_class: str
    integrated_runner_status: str
    receipt_path: str
    audit_path: str
    integrated_runner_invoked: bool
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


def _integrated_context(root: pathlib.Path, policy: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "qi_github_actions_integrated_bridge_runner_enabled": True,
        "apply_github_actions_integrated_bridge_runner": True,
        "runtime_root": str(root),
        "max_bridge_cycles": _i(policy.get("max_bridge_cycles"), 5),
        "max_loop_steps_per_cycle": _i(policy.get("max_loop_steps_per_cycle"), 5),
    }


def _integrated_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_LICENSE_READY",
        "internal_loop_run_allowed": True,
        "external_bridge_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def build_qi_github_actions_policy_aware_runner(*, runtime_context: Mapping[str, Any], policy_aware_runner_license: Mapping[str, Any]) -> QiGitHubActionsPolicyAwareRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(policy_aware_runner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    policy_path = root / "qi_github_actions_lifecycle_policy_packet.json"
    receipt_path = root / "qi_github_actions_policy_aware_runner_receipt.json"
    audit_path = root / "qi_github_actions_policy_aware_runner_audit.jsonl"

    if ctx.get("qi_github_actions_policy_aware_runner_enabled") is not True:
        blockers.append("qi_github_actions_policy_aware_runner_enabled_not_true")
    if ctx.get("apply_github_actions_policy_aware_runner") is not True:
        blockers.append("apply_github_actions_policy_aware_runner_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_POLICY_AWARE_RUNNER_LICENSE_READY":
        blockers.append("github_actions_policy_aware_runner_license_not_ready")
    for name in ["policy_packet_read_allowed", "integrated_runner_invoke_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    policy = _read_json(policy_path)
    if not policy:
        blockers.append("lifecycle_policy_packet_missing_or_invalid")
    runner_mode = str(policy.get("runner_mode", "unknown")) if policy else "unknown"
    policy_hint = str(policy.get("policy_hint", "unknown")) if policy else "unknown"
    if runner_mode not in ALLOWED_RUNNER_MODES:
        blockers.append("runner_mode_not_allowlisted")
    if runner_mode in ALLOWED_RUNNER_MODES and lic.get(f"allow_{runner_mode}_mode") is not True:
        blockers.append(f"{runner_mode}_mode_not_allowed_by_policy_aware_runner_license")
    if policy and policy.get("hold_required") is True and runner_mode != "hold":
        blockers.append("hold_required_but_runner_mode_not_hold")
    max_cycles = _i(policy.get("max_bridge_cycles"), 0) if policy else 0
    max_steps = _i(policy.get("max_loop_steps_per_cycle"), 0) if policy else 0
    if policy and (max_cycles < 1 or max_steps < 1):
        blockers.append("policy_runner_limits_invalid")

    integrated_result: Mapping[str, Any] = {}
    invoked = False
    execution_class = "not_run"
    integrated_status = "NOT_RUN"
    if not blockers:
        if runner_mode == "hold":
            execution_class = "policy_hold"
            integrated_status = "HELD"
        else:
            integrated_result = build_qi_github_actions_integrated_bridge_runner(
                runtime_context=_integrated_context(root, policy),
                integrated_bridge_runner_license=_integrated_license(),
            ).to_dict()
            invoked = True
            integrated_status = str(integrated_result.get("status", "unknown"))
            if integrated_status == "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_READY":
                execution_class = "policy_runner_completed"
            else:
                blockers.append("integrated_runner_not_ready")
                execution_class = "policy_runner_blocked"

    status = "QI_GITHUB_ACTIONS_POLICY_AWARE_RUNNER_READY" if not blockers else "QI_GITHUB_ACTIONS_POLICY_AWARE_RUNNER_BLOCKED"
    packet_id = "qi-github-actions-policy-aware-runner-" + _sha({"policy": policy, "integrated": integrated_result, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_policy_aware_runner_v7_2",
        "status": status,
        "packet_id": packet_id,
        "policy_hint": policy_hint,
        "runner_mode": runner_mode,
        "execution_class": execution_class,
        "integrated_runner_status": integrated_status,
        "integrated_runner_invoked": invoked,
        "integrated_result_digest": _sha(dict(integrated_result)),
        "policy_digest": _sha(policy),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsPolicyAwareRunnerResult(
        "kuuos_runtime_daemon_qi_github_actions_policy_aware_runner_v7_2",
        status,
        packet_id,
        str(root),
        runner_mode,
        policy_hint,
        execution_class,
        integrated_status,
        str(receipt_path),
        str(audit_path),
        invoked,
        blockers,
        warnings,
    )
