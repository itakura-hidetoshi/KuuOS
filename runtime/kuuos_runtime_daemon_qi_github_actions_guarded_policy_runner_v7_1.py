#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_policy_safety_gate_v7_0 import build_qi_github_actions_policy_safety_gate
from runtime.kuuos_runtime_daemon_qi_github_actions_full_cycle_policy_runner_v6_9 import build_qi_github_actions_full_cycle_policy_runner


@dataclass(frozen=True)
class QiGitHubActionsGuardedPolicyRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    gate_status: str
    gate_result: str
    policy_runner_status: str
    policy_decision: str
    action_prepared: str
    stop_reason: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]
    records: list[dict[str, Any]]

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


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _gate_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_policy_safety_gate_enabled": True,
        "apply_github_actions_policy_safety_gate": True,
        "runtime_root": str(root),
    }


def _gate_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_POLICY_SAFETY_GATE_LICENSE_READY",
        "policy_intent_read_allowed": True,
        "status_packet_read_allowed": True,
        "policy_packet_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _runner_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_full_cycle_policy_runner_enabled": True,
        "apply_github_actions_full_cycle_policy_runner": True,
        "runtime_root": str(root),
    }


def _runner_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_FULL_CYCLE_POLICY_RUNNER_LICENSE_READY",
        "policy_packet_read_allowed": True,
        "status_packet_read_allowed": True,
        "direct_executor_run_allowed": True,
        "orchestrator_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _record(stage: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage": stage,
        "status": str(payload.get("status", "unknown")),
        "digest": _sha(dict(payload)),
        "blockers": list(payload.get("blockers", [])) if isinstance(payload.get("blockers", []), list) else [],
        "epoch": int(time.time()),
    }


def build_qi_github_actions_guarded_policy_runner(*, runtime_context: Mapping[str, Any], guarded_policy_runner_license: Mapping[str, Any]) -> QiGitHubActionsGuardedPolicyRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(guarded_policy_runner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    receipt_path = root / "qi_github_actions_guarded_policy_runner_receipt.json"
    audit_path = root / "qi_github_actions_guarded_policy_runner_audit.jsonl"

    if ctx.get("qi_github_actions_guarded_policy_runner_enabled") is not True:
        blockers.append("qi_github_actions_guarded_policy_runner_enabled_not_true")
    if ctx.get("apply_github_actions_guarded_policy_runner") is not True:
        blockers.append("apply_github_actions_guarded_policy_runner_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_GUARDED_POLICY_RUNNER_LICENSE_READY":
        blockers.append("github_actions_guarded_policy_runner_license_not_ready")
    for name in ["safety_gate_run_allowed", "policy_runner_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    records: list[dict[str, Any]] = []
    gate_status = "NOT_RUN"
    gate_result = "not_run"
    runner_status = "NOT_RUN"
    policy_decision = "not_run"
    action_prepared = "none"
    stop_reason = "not_run"

    if not blockers:
        gate = build_qi_github_actions_policy_safety_gate(
            runtime_context=_gate_context(root),
            policy_safety_gate_license=_gate_license(),
        ).to_dict()
        records.append(_record("v7_0_policy_safety_gate", gate))
        gate_status = str(gate.get("status", "unknown"))
        gate_result = str(gate.get("gate_result", "unknown"))
        if gate_status != "QI_GITHUB_ACTIONS_POLICY_SAFETY_GATE_READY" or gate_result != "passed":
            blockers.append("policy_safety_gate_not_passed")
            stop_reason = "gate_blocked"
        else:
            runner = build_qi_github_actions_full_cycle_policy_runner(
                runtime_context=_runner_context(root),
                policy_runner_license=_runner_license(),
            ).to_dict()
            records.append(_record("v6_9_full_cycle_policy_runner", runner))
            runner_status = str(runner.get("status", "unknown"))
            policy_decision = str(runner.get("policy_decision", "unknown"))
            action_prepared = str(runner.get("action_prepared", "none"))
            stop_reason = str(runner.get("stop_reason", "unknown"))
            if runner_status != "QI_GITHUB_ACTIONS_FULL_CYCLE_POLICY_RUNNER_READY":
                blockers.append("full_cycle_policy_runner_not_ready")
                stop_reason = "policy_runner_blocked"

    status = "QI_GITHUB_ACTIONS_GUARDED_POLICY_RUNNER_READY" if not blockers else "QI_GITHUB_ACTIONS_GUARDED_POLICY_RUNNER_BLOCKED"
    packet_id = "qi-github-actions-guarded-policy-" + _sha({"records": records, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_guarded_policy_runner_v7_1",
        "status": status,
        "packet_id": packet_id,
        "gate_status": gate_status,
        "gate_result": gate_result,
        "policy_runner_status": runner_status,
        "policy_decision": policy_decision,
        "action_prepared": action_prepared,
        "stop_reason": stop_reason,
        "records": records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsGuardedPolicyRunnerResult(
        "kuuos_runtime_daemon_qi_github_actions_guarded_policy_runner_v7_1",
        status,
        packet_id,
        str(root),
        gate_status,
        gate_result,
        runner_status,
        policy_decision,
        action_prepared,
        stop_reason,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
        records,
    )
