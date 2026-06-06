#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_pr_live_snapshot_adapter_v7_3 import build_qi_github_actions_pr_live_snapshot_adapter


@dataclass(frozen=True)
class QiGitHubActionsPrLiveSnapshotCollectorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    collector_result: str
    adapter_status: str
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


def _raw_runs(packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = packet.get("workflow_runs")
    if isinstance(raw, list):
        return [dict(item) for item in raw if isinstance(item, Mapping)]
    nested = packet.get("connector_result")
    if isinstance(nested, Mapping):
        nr = nested.get("workflow_runs")
        if isinstance(nr, list):
            return [dict(item) for item in nr if isinstance(item, Mapping)]
    return []


def _repo(raw_pr: Mapping[str, Any], config: Mapping[str, Any], blockers: list[str]) -> str:
    repo = str(config.get("repo_full_name") or raw_pr.get("repo_full_name") or raw_pr.get("repository_full_name") or "").strip()
    if "/" not in repo:
        blockers.append("repo_full_name_invalid")
    return repo


def _pr_number(raw_pr: Mapping[str, Any], config: Mapping[str, Any], blockers: list[str]) -> int:
    number = _i(config.get("pr_number", config.get("pull_number", raw_pr.get("number", raw_pr.get("pr_number")))), 0)
    if number <= 0:
        blockers.append("pr_number_invalid")
    return number


def _head_sha(raw_pr: Mapping[str, Any], config: Mapping[str, Any], blockers: list[str]) -> str:
    sha = str(config.get("head_sha") or config.get("expected_head_sha") or raw_pr.get("head_sha") or raw_pr.get("head", {}).get("sha") if isinstance(raw_pr.get("head"), Mapping) else "").strip()
    if not sha:
        blockers.append("head_sha_missing")
    return sha


def _base_branch(raw_pr: Mapping[str, Any], config: Mapping[str, Any]) -> str:
    if config.get("base_branch"):
        return str(config.get("base_branch"))
    base = raw_pr.get("base")
    if isinstance(base, Mapping):
        return str(base.get("ref", "main"))
    return str(base or "main")


def _normalize_pr(raw_pr: Mapping[str, Any], config: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    return {
        "repo_full_name": _repo(raw_pr, config, blockers),
        "number": _pr_number(raw_pr, config, blockers),
        "state": str(raw_pr.get("state", "open")),
        "draft": raw_pr.get("draft") is True,
        "merged": raw_pr.get("merged") is True,
        "head_sha": _head_sha(raw_pr, config, blockers),
        "base": _base_branch(raw_pr, config),
        "source_raw_pr_digest": _sha(dict(raw_pr)),
        "epoch": int(time.time()),
    }


def _normalize_runs(raw_runs_packet: Mapping[str, Any], config: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    runs = _raw_runs(raw_runs_packet)
    if not runs:
        blockers.append("workflow_runs_empty_or_invalid")
    required = config.get("required_workflows") or raw_runs_packet.get("required_workflows")
    if not isinstance(required, list) or not required:
        required = [str(run.get("name", "")) for run in runs if run.get("name")]
    return {
        "required_workflows": [str(x) for x in required if str(x)],
        "workflow_runs": runs,
        "source_raw_runs_digest": _sha(dict(raw_runs_packet)),
        "epoch": int(time.time()),
    }


def _adapter_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_pr_live_snapshot_adapter_enabled": True,
        "apply_github_actions_pr_live_snapshot_adapter": True,
        "runtime_root": str(root),
    }


def _adapter_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_ADAPTER_LICENSE_READY",
        "pr_snapshot_read_allowed": True,
        "workflow_runs_read_allowed": True,
        "entry_packet_write_allowed": True,
        "entrypoint_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def build_qi_github_actions_pr_live_snapshot_collector(*, runtime_context: Mapping[str, Any], pr_live_snapshot_collector_license: Mapping[str, Any]) -> QiGitHubActionsPrLiveSnapshotCollectorResult:
    ctx = _m(runtime_context)
    lic = _m(pr_live_snapshot_collector_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    raw_pr_path = root / "qi_github_actions_raw_pr_info_packet.json"
    raw_runs_path = root / "qi_github_actions_raw_commit_workflow_runs_packet.json"
    config_path = root / "qi_github_actions_pr_live_policy_config.json"
    pr_snapshot_path = root / "qi_github_actions_pr_snapshot_packet.json"
    runs_packet_path = root / "qi_github_actions_commit_workflow_runs_packet.json"
    receipt_path = root / "qi_github_actions_pr_live_snapshot_collector_receipt.json"
    audit_path = root / "qi_github_actions_pr_live_snapshot_collector_audit.jsonl"

    if ctx.get("qi_github_actions_pr_live_snapshot_collector_enabled") is not True:
        blockers.append("qi_github_actions_pr_live_snapshot_collector_enabled_not_true")
    if ctx.get("apply_github_actions_pr_live_snapshot_collector") is not True:
        blockers.append("apply_github_actions_pr_live_snapshot_collector_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_COLLECTOR_LICENSE_READY":
        blockers.append("github_actions_pr_live_snapshot_collector_license_not_ready")
    for name in ["raw_pr_info_read_allowed", "raw_workflow_runs_read_allowed", "snapshot_packet_write_allowed", "adapter_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    raw_pr = _read_json(raw_pr_path)
    raw_runs = _read_json(raw_runs_path)
    config = _read_json(config_path) or {"adapter_allowed": True}
    if not raw_pr:
        blockers.append("raw_pr_info_packet_missing_or_invalid")
    if not raw_runs:
        blockers.append("raw_workflow_runs_packet_missing_or_invalid")
    if config.get("adapter_allowed") is not True:
        blockers.append("adapter_allowed_not_true")

    collector_result = "blocked"
    adapter_status = "NOT_RUN"
    policy_decision = "not_run"
    action_prepared = "none"
    stop_reason = "not_run"
    if not blockers:
        pr_snapshot = _normalize_pr(raw_pr, config, blockers)
        runs_packet = _normalize_runs(raw_runs, config, blockers)
        if not blockers:
            _write_json(pr_snapshot_path, pr_snapshot)
            _write_json(runs_packet_path, runs_packet)
            collector_result = "snapshot_packets_written"
            adapter = build_qi_github_actions_pr_live_snapshot_adapter(
                runtime_context=_adapter_context(root),
                pr_live_snapshot_adapter_license=_adapter_license(),
            ).to_dict()
            adapter_status = str(adapter.get("status", "unknown"))
            policy_decision = str(adapter.get("policy_decision", "unknown"))
            action_prepared = str(adapter.get("action_prepared", "none"))
            stop_reason = str(adapter.get("stop_reason", "unknown"))
            if adapter_status != "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_ADAPTER_READY":
                blockers.append("pr_live_snapshot_adapter_not_ready")
                stop_reason = "adapter_blocked"

    status = "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_COLLECTOR_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_LIVE_SNAPSHOT_COLLECTOR_BLOCKED"
    packet_id = "qi-github-actions-pr-live-snapshot-collector-" + _sha({"pr": raw_pr, "runs": raw_runs, "config": config, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_pr_live_snapshot_collector_v7_4",
        "status": status,
        "packet_id": packet_id,
        "collector_result": collector_result,
        "adapter_status": adapter_status,
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

    return QiGitHubActionsPrLiveSnapshotCollectorResult(
        "kuuos_runtime_daemon_qi_github_actions_pr_live_snapshot_collector_v7_4",
        status,
        packet_id,
        str(root),
        collector_result,
        adapter_status,
        policy_decision,
        action_prepared,
        stop_reason,
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
