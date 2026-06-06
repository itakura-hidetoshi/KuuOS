#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_guarded_policy_runner_v7_1 import build_qi_github_actions_guarded_policy_runner


DEFAULT_REQUIRED_WORKFLOWS = [
    "All Governance Validation",
    "Core Governance Validation",
    "Emptiness Superposition Non-Collapse Validation",
    "Emptiness Two Truths Runtime Audit Validation",
    "KuuOS Runtime Full Check",
    "Qi Process Tensor Review Checks",
]


@dataclass(frozen=True)
class QiGitHubActionsPrPolicyEntrypointResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    entry_result: str
    guarded_runner_status: str
    policy_decision: str
    action_prepared: str
    stop_reason: str
    receipt_path: str
    audit_path: str
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


def _runs(entry: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = entry.get("workflow_runs", [])
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _required(entry: Mapping[str, Any]) -> list[str]:
    raw = entry.get("required_workflows", DEFAULT_REQUIRED_WORKFLOWS)
    if isinstance(raw, list) and raw:
        return [str(x) for x in raw]
    return list(DEFAULT_REQUIRED_WORKFLOWS)


def _repo(entry: Mapping[str, Any], blockers: list[str]) -> str:
    repo = str(entry.get("repo_full_name", "")).strip()
    if "/" not in repo:
        blockers.append("repo_full_name_invalid")
    return repo


def _validate_entry(entry: Mapping[str, Any], blockers: list[str]) -> None:
    if entry.get("entry_allowed") is not True:
        blockers.append("entry_allowed_not_true")
    _repo(entry, blockers)
    if _i(entry.get("pr_number", entry.get("pull_number")), 0) <= 0:
        blockers.append("pr_number_invalid")
    if not str(entry.get("head_sha", entry.get("expected_head_sha", ""))).strip():
        blockers.append("head_sha_missing")
    if not str(entry.get("commit_sha", entry.get("head_sha", entry.get("expected_head_sha", "")))).strip():
        blockers.append("commit_sha_missing")
    if not _runs(entry):
        blockers.append("workflow_runs_empty_or_invalid")
    if not _required(entry):
        blockers.append("required_workflows_empty_or_invalid")


def _intent_packet(entry: Mapping[str, Any], source_digest: str) -> dict[str, Any]:
    head_sha = str(entry.get("head_sha", entry.get("expected_head_sha", "")))
    return {
        "policy_intent_allowed": True,
        "repo_full_name": str(entry.get("repo_full_name", "")),
        "required_workflows": _required(entry),
        "merge_when_green": entry.get("merge_when_green", True) is True,
        "rerun_when_failed": entry.get("rerun_when_failed", True) is True,
        "reobserve_when_pending": entry.get("reobserve_when_pending", True) is True,
        "pr_number": _i(entry.get("pr_number", entry.get("pull_number")), 0),
        "expected_head_sha": head_sha,
        "commit_sha": str(entry.get("commit_sha", head_sha)),
        "base_branch": str(entry.get("base_branch", "main")),
        "merge_method": str(entry.get("merge_method", "merge")),
        "source_entry_digest": source_digest,
        "epoch": int(time.time()),
    }


def _status_packet(entry: Mapping[str, Any], source_digest: str) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_status_packet_from_pr_policy_entrypoint_v7_2",
        "github_actions_status_allowed": True,
        "required_workflows": _required(entry),
        "workflow_runs": _runs(entry),
        "source_entry_digest": source_digest,
        "epoch": int(time.time()),
    }


def _runner_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_guarded_policy_runner_enabled": True,
        "apply_github_actions_guarded_policy_runner": True,
        "runtime_root": str(root),
    }


def _runner_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_GUARDED_POLICY_RUNNER_LICENSE_READY",
        "safety_gate_run_allowed": True,
        "policy_runner_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def build_qi_github_actions_pr_policy_entrypoint(*, runtime_context: Mapping[str, Any], pr_policy_entrypoint_license: Mapping[str, Any]) -> QiGitHubActionsPrPolicyEntrypointResult:
    ctx = _m(runtime_context)
    lic = _m(pr_policy_entrypoint_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    entry_path = root / "qi_github_actions_pr_policy_entry_packet.json"
    intent_path = root / "qi_github_actions_policy_intent_packet.json"
    status_path = root / "qi_github_actions_status_packet.json"
    receipt_path = root / "qi_github_actions_pr_policy_entrypoint_receipt.json"
    audit_path = root / "qi_github_actions_pr_policy_entrypoint_audit.jsonl"

    if ctx.get("qi_github_actions_pr_policy_entrypoint_enabled") is not True:
        blockers.append("qi_github_actions_pr_policy_entrypoint_enabled_not_true")
    if ctx.get("apply_github_actions_pr_policy_entrypoint") is not True:
        blockers.append("apply_github_actions_pr_policy_entrypoint_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_POLICY_ENTRYPOINT_LICENSE_READY":
        blockers.append("github_actions_pr_policy_entrypoint_license_not_ready")
    for name in ["entry_packet_read_allowed", "intent_packet_write_allowed", "status_packet_write_allowed", "guarded_runner_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    entry = _read_json(entry_path)
    if not entry:
        blockers.append("entry_packet_missing_or_invalid")
    if entry:
        _validate_entry(entry, blockers)

    entry_result = "blocked"
    runner_status = "NOT_RUN"
    policy_decision = "not_run"
    action_prepared = "none"
    stop_reason = "not_run"
    if not blockers:
        digest = _sha(entry)
        _write_json(intent_path, _intent_packet(entry, digest))
        _write_json(status_path, _status_packet(entry, digest))
        entry_result = "packets_written"
        runner = build_qi_github_actions_guarded_policy_runner(
            runtime_context=_runner_context(root),
            guarded_policy_runner_license=_runner_license(),
        ).to_dict()
        runner_status = str(runner.get("status", "unknown"))
        policy_decision = str(runner.get("policy_decision", "unknown"))
        action_prepared = str(runner.get("action_prepared", "none"))
        stop_reason = str(runner.get("stop_reason", "unknown"))
        if runner_status != "QI_GITHUB_ACTIONS_GUARDED_POLICY_RUNNER_READY":
            blockers.append("guarded_policy_runner_not_ready")
            stop_reason = "guarded_runner_blocked"

    status = "QI_GITHUB_ACTIONS_PR_POLICY_ENTRYPOINT_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_POLICY_ENTRYPOINT_BLOCKED"
    packet_id = "qi-github-actions-pr-policy-entrypoint-" + _sha({"entry": entry, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_pr_policy_entrypoint_v7_2",
        "status": status,
        "packet_id": packet_id,
        "entry_result": entry_result,
        "guarded_runner_status": runner_status,
        "policy_decision": policy_decision,
        "action_prepared": action_prepared,
        "stop_reason": stop_reason,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPrPolicyEntrypointResult(
        "kuuos_runtime_daemon_qi_github_actions_pr_policy_entrypoint_v7_2",
        status,
        packet_id,
        str(root),
        entry_result,
        runner_status,
        policy_decision,
        action_prepared,
        stop_reason,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
