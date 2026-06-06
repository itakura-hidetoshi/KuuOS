#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_pr_policy_entrypoint_v7_2 import build_qi_github_actions_pr_policy_entrypoint


DEFAULT_REQUIRED_WORKFLOWS = [
    "All Governance Validation",
    "Core Governance Validation",
    "Emptiness Superposition Non-Collapse Validation",
    "Emptiness Two Truths Runtime Audit Validation",
    "KuuOS Runtime Full Check",
    "Qi Process Tensor Review Checks",
]


@dataclass(frozen=True)
class QiGitHubActionsPrLiveSnapshotAdapterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    adapter_result: str
    entrypoint_status: str
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


def _runs(packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = packet.get("workflow_runs", [])
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _required(config: Mapping[str, Any], runs_packet: Mapping[str, Any]) -> list[str]:
    raw = config.get("required_workflows") or runs_packet.get("required_workflows") or DEFAULT_REQUIRED_WORKFLOWS
    if isinstance(raw, list) and raw:
        return [str(x) for x in raw]
    return list(DEFAULT_REQUIRED_WORKFLOWS)


def _repo(pr: Mapping[str, Any], config: Mapping[str, Any], blockers: list[str]) -> str:
    repo = str(config.get("repo_full_name") or pr.get("repo_full_name") or pr.get("repository_full_name") or "").strip()
    if "/" not in repo:
        blockers.append("repo_full_name_invalid")
    return repo


def _head_sha(pr: Mapping[str, Any], config: Mapping[str, Any], blockers: list[str]) -> str:
    sha = str(config.get("head_sha") or config.get("expected_head_sha") or pr.get("head_sha") or "").strip()
    if not sha:
        blockers.append("head_sha_missing")
    return sha


def _pr_number(pr: Mapping[str, Any], config: Mapping[str, Any], blockers: list[str]) -> int:
    number = _i(config.get("pr_number", config.get("pull_number", pr.get("number", pr.get("pr_number")))), 0)
    if number <= 0:
        blockers.append("pr_number_invalid")
    return number


def _validate(pr: Mapping[str, Any], runs_packet: Mapping[str, Any], config: Mapping[str, Any], blockers: list[str]) -> None:
    if config.get("adapter_allowed") is not True:
        blockers.append("adapter_allowed_not_true")
    state = str(pr.get("state", "open"))
    if state != "open":
        blockers.append("pr_not_open")
    if pr.get("draft") is True and config.get("allow_draft_pr") is not True:
        blockers.append("draft_pr_not_allowed")
    if pr.get("merged") is True:
        blockers.append("pr_already_merged")
    _repo(pr, config, blockers)
    _head_sha(pr, config, blockers)
    _pr_number(pr, config, blockers)
    if not _runs(runs_packet):
        blockers.append("workflow_runs_empty_or_invalid")
    if not _required(config, runs_packet):
        blockers.append("required_workflows_empty_or_invalid")


def _entry_packet(pr: Mapping[str, Any], runs_packet: Mapping[str, Any], config: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    head_sha = _head_sha(pr, config, blockers)
    return {
        "entry_allowed": True,
        "repo_full_name": _repo(pr, config, blockers),
        "pr_number": _pr_number(pr, config, blockers),
        "head_sha": head_sha,
        "commit_sha": str(config.get("commit_sha") or head_sha),
        "base_branch": str(config.get("base_branch") or pr.get("base") or "main"),
        "required_workflows": _required(config, runs_packet),
        "merge_when_green": config.get("merge_when_green", True) is True,
        "rerun_when_failed": config.get("rerun_when_failed", True) is True,
        "reobserve_when_pending": config.get("reobserve_when_pending", True) is True,
        "merge_method": str(config.get("merge_method", "merge")),
        "workflow_runs": _runs(runs_packet),
        "source_pr_snapshot_digest": _sha(dict(pr)),
        "source_runs_digest": _sha(dict(runs_packet)),
        "epoch": int(time.time()),
    }


def _entry_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_pr_policy_entrypoint_enabled": True,
        "apply_github_actions_pr_policy_entrypoint": True,
        "runtime_root": str(root),
    }


def _entry_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_PR_POLICY_ENTRYPOINT_LICENSE_READY",
        "entry_packet_read_allowed": True,
        "intent_packet_write_allowed": True,
        "status_packet_write_allowed": True,
        "guarded_runner_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def build_qi_github_actions_pr_live_snapshot_adapter(*, runtime_context: Mapping[str, Any], pr_live_snapshot_adapter_license: Mapping[str, Any]) -> QiGitHubActionsPrLiveSnapshotAdapterResult:
    ctx = _m(runtime_context)
    lic = _m(pr_live_snapshot_adapter_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    pr_path = root / "qi_github_actions_pr_snapshot_packet.json"
    runs_path = root / "qi_github_actions_commit_workflow_runs_packet.json"
    config_path = root / "qi_github_actions_pr_live_policy_config.json"
    entry_path = root / "qi_github_actions_pr_policy_entry_packet.json"
    receipt_path = root / "qi_github_actions_pr_live_snapshot_adapter_receipt.json"
    audit_path = root / "qi_github_actions_pr_live_snapshot_adapter_audit.jsonl"

    if ctx.get("qi_github_actions_pr_live_snapshot_adapter_enabled") is not True:
        blockers.append("qi_github_actions_pr_live_snapshot_adapter_enabled_not_true")
    if ctx.get("apply_github_actions_pr_live_snapshot_adapter") is not True:
        blockers.append("apply_github_actions_pr_live_snapshot_adapter_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_ADAPTER_LICENSE_READY":
        blockers.append("github_actions_pr_live_snapshot_adapter_license_not_ready")
    for name in ["pr_snapshot_read_allowed", "workflow_runs_read_allowed", "entry_packet_write_allowed", "entrypoint_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    pr = _read_json(pr_path)
    runs_packet = _read_json(runs_path)
    config = _read_json(config_path) or {"adapter_allowed": True}
    if not pr:
        blockers.append("pr_snapshot_packet_missing_or_invalid")
    if not runs_packet:
        blockers.append("workflow_runs_packet_missing_or_invalid")
    if pr and runs_packet:
        _validate(pr, runs_packet, config, blockers)

    adapter_result = "blocked"
    entrypoint_status = "NOT_RUN"
    policy_decision = "not_run"
    action_prepared = "none"
    stop_reason = "not_run"
    if not blockers:
        entry = _entry_packet(pr, runs_packet, config, blockers)
        if not blockers:
            _write_json(entry_path, entry)
            adapter_result = "entry_packet_written"
            entry_res = build_qi_github_actions_pr_policy_entrypoint(
                runtime_context=_entry_context(root),
                pr_policy_entrypoint_license=_entry_license(),
            ).to_dict()
            entrypoint_status = str(entry_res.get("status", "unknown"))
            policy_decision = str(entry_res.get("policy_decision", "unknown"))
            action_prepared = str(entry_res.get("action_prepared", "none"))
            stop_reason = str(entry_res.get("stop_reason", "unknown"))
            if entrypoint_status != "QI_GITHUB_ACTIONS_PR_POLICY_ENTRYPOINT_READY":
                blockers.append("pr_policy_entrypoint_not_ready")
                stop_reason = "entrypoint_blocked"

    status = "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_ADAPTER_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_ADAPTER_BLOCKED"
    packet_id = "qi-github-actions-pr-live-snapshot-" + _sha({"pr": pr, "runs": runs_packet, "config": config, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_pr_live_snapshot_adapter_v7_3",
        "status": status,
        "packet_id": packet_id,
        "adapter_result": adapter_result,
        "entrypoint_status": entrypoint_status,
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

    return QiGitHubActionsPrLiveSnapshotAdapterResult(
        "kuuos_runtime_daemon_qi_github_actions_pr_live_snapshot_adapter_v7_3",
        status,
        packet_id,
        str(root),
        adapter_result,
        entrypoint_status,
        policy_decision,
        action_prepared,
        stop_reason,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
