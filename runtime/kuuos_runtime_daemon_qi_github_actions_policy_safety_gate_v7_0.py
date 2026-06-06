#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ALLOWED_POLICY_ACTIONS = {
    "merge_when_green",
    "rerun_when_failed",
    "reobserve_when_pending",
}

DEFAULT_REQUIRED_WORKFLOWS = [
    "All Governance Validation",
    "Core Governance Validation",
    "Emptiness Superposition Non-Collapse Validation",
    "Emptiness Two Truths Runtime Audit Validation",
    "KuuOS Runtime Full Check",
    "Qi Process Tensor Review Checks",
]


@dataclass(frozen=True)
class QiGitHubActionsPolicySafetyGateResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    gate_result: str
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


def _runs(status_packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = status_packet.get("workflow_runs", [])
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _required(intent: Mapping[str, Any], status_packet: Mapping[str, Any]) -> list[str]:
    raw = intent.get("required_workflows") or status_packet.get("required_workflows") or DEFAULT_REQUIRED_WORKFLOWS
    if isinstance(raw, list) and raw:
        return [str(x) for x in raw]
    return list(DEFAULT_REQUIRED_WORKFLOWS)


def _latest_by_name(runs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for run in runs:
        name = str(run.get("name", ""))
        if name and name not in latest:
            latest[name] = run
    return latest


def _enabled_actions(intent: Mapping[str, Any]) -> list[str]:
    return [name for name in ALLOWED_POLICY_ACTIONS if intent.get(name) is True]


def _validate_repo(value: Any, blockers: list[str]) -> str:
    repo = str(value or "").strip()
    if "/" not in repo:
        blockers.append("repo_full_name_invalid")
    return repo


def _validate_policy_intent(intent: Mapping[str, Any], status_packet: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> dict[str, Any]:
    if intent.get("policy_intent_allowed") is not True:
        blockers.append("policy_intent_allowed_not_true")
    repo = _validate_repo(intent.get("repo_full_name"), blockers)
    required = _required(intent, status_packet)
    runs = _runs(status_packet)
    if not runs:
        blockers.append("workflow_runs_empty_or_invalid")
    latest = _latest_by_name(runs)
    missing = [name for name in required if name not in latest]
    if missing:
        blockers.append("required_workflows_missing")
    actions = _enabled_actions(intent)
    if not actions:
        blockers.append("no_policy_action_enabled")
    unknown_actions = [str(x) for x in intent.get("enabled_actions", []) if str(x) not in ALLOWED_POLICY_ACTIONS] if isinstance(intent.get("enabled_actions"), list) else []
    if unknown_actions:
        blockers.append("unknown_policy_action_requested")
    if intent.get("merge_when_green") is True:
        if _i(intent.get("pr_number", intent.get("pull_number")), 0) <= 0:
            blockers.append("pr_number_invalid")
        if not str(intent.get("expected_head_sha", "")).strip():
            blockers.append("expected_head_sha_missing")
        if str(intent.get("base_branch", "main")) != "main":
            warnings.append("non_main_base_branch")
    if intent.get("rerun_when_failed") is True and intent.get("run_id") is not None and _i(intent.get("run_id"), 0) <= 0:
        blockers.append("run_id_invalid")
    if intent.get("reobserve_when_pending") is True and not str(intent.get("commit_sha", intent.get("expected_head_sha", ""))).strip():
        blockers.append("commit_sha_missing")
    return {
        "repo_full_name": repo,
        "required_workflows": required,
        "enabled_actions": actions,
        "missing_workflows": missing,
    }


def _policy_packet(intent: Mapping[str, Any], normalized: Mapping[str, Any]) -> dict[str, Any]:
    body = {
        "policy_allowed": True,
        "repo_full_name": normalized["repo_full_name"],
        "required_workflows": list(normalized["required_workflows"]),
        "merge_when_green": intent.get("merge_when_green") is True,
        "rerun_when_failed": intent.get("rerun_when_failed") is True,
        "reobserve_when_pending": intent.get("reobserve_when_pending") is True,
        "pr_number": _i(intent.get("pr_number", intent.get("pull_number")), 0),
        "expected_head_sha": str(intent.get("expected_head_sha", "")),
        "commit_sha": str(intent.get("commit_sha", intent.get("expected_head_sha", ""))),
        "merge_method": str(intent.get("merge_method", "merge")),
        "max_full_cycle_phases": _i(intent.get("max_full_cycle_phases", 4), 4),
        "max_loop_steps_per_phase": _i(intent.get("max_loop_steps_per_phase", 5), 5),
        "source_intent_digest": _sha(dict(intent)),
        "gate_version": "qi_github_actions_policy_safety_gate_v7_0",
        "epoch": int(time.time()),
    }
    if intent.get("run_id") is not None:
        body["run_id"] = _i(intent.get("run_id"), 0)
    return body


def build_qi_github_actions_policy_safety_gate(*, runtime_context: Mapping[str, Any], policy_safety_gate_license: Mapping[str, Any]) -> QiGitHubActionsPolicySafetyGateResult:
    ctx = _m(runtime_context)
    lic = _m(policy_safety_gate_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    intent_path = root / "qi_github_actions_policy_intent_packet.json"
    status_path = root / "qi_github_actions_status_packet.json"
    policy_path = root / "qi_github_actions_full_cycle_policy_packet.json"
    receipt_path = root / "qi_github_actions_policy_safety_gate_receipt.json"
    audit_path = root / "qi_github_actions_policy_safety_gate_audit.jsonl"

    if ctx.get("qi_github_actions_policy_safety_gate_enabled") is not True:
        blockers.append("qi_github_actions_policy_safety_gate_enabled_not_true")
    if ctx.get("apply_github_actions_policy_safety_gate") is not True:
        blockers.append("apply_github_actions_policy_safety_gate_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_POLICY_SAFETY_GATE_LICENSE_READY":
        blockers.append("github_actions_policy_safety_gate_license_not_ready")
    for name in ["policy_intent_read_allowed", "status_packet_read_allowed", "policy_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    intent = _read_json(intent_path)
    status_packet = _read_json(status_path)
    if not intent:
        blockers.append("policy_intent_packet_missing_or_invalid")
    if not status_packet:
        blockers.append("status_packet_missing_or_invalid")
    if status_packet and status_packet.get("github_actions_status_allowed") is not True:
        blockers.append("status_packet_allowed_not_true")

    normalized: dict[str, Any] = {}
    policy: dict[str, Any] = {}
    written = False
    gate_result = "blocked"
    if not blockers:
        normalized = _validate_policy_intent(intent, status_packet, blockers, warnings)
    if not blockers:
        policy = _policy_packet(intent, normalized)
        _write_json(policy_path, policy)
        written = True
        gate_result = "passed"

    status = "QI_GITHUB_ACTIONS_POLICY_SAFETY_GATE_READY" if not blockers else "QI_GITHUB_ACTIONS_POLICY_SAFETY_GATE_BLOCKED"
    packet_id = "qi-github-actions-policy-safety-gate-" + _sha({"intent": intent, "normalized": normalized, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_policy_safety_gate_v7_0",
        "status": status,
        "packet_id": packet_id,
        "gate_result": gate_result,
        "policy_packet_written": written,
        "policy_packet_digest": _sha(policy),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPolicySafetyGateResult(
        "kuuos_runtime_daemon_qi_github_actions_policy_safety_gate_v7_0",
        status,
        packet_id,
        str(root),
        gate_result,
        str(policy_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
