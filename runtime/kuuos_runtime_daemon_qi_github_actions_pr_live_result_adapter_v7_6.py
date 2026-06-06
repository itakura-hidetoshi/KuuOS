#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_github_actions_pr_live_request_planner_v7_5 import build_qi_github_actions_pr_live_request_planner


RESULT_KINDS = {
    "pr_info",
    "commit_workflow_runs",
}


@dataclass(frozen=True)
class QiGitHubActionsPrLiveResultAdapterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    result_kind: str
    adapted_packet_path: str
    planner_status: str
    planner_stage: str
    policy_decision: str
    action_prepared: str
    stop_reason: str
    receipt_path: str
    audit_path: str
    adapted_packet_written: bool
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


def _payload(raw: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = raw.get("connector_result")
    return nested if isinstance(nested, Mapping) else raw


def _infer_kind(request: Mapping[str, Any], raw: Mapping[str, Any]) -> str:
    explicit = str(raw.get("result_kind") or request.get("result_kind") or "")
    if explicit in RESULT_KINDS:
        return explicit
    action = str(request.get("connector_action", raw.get("connector_action", "")))
    expected = str(request.get("result_expected_file", raw.get("result_expected_file", "")))
    if "get_pr_info" in action or "raw_pr_info" in expected:
        return "pr_info"
    if "fetch_commit_workflow_runs" in action or "raw_commit_workflow_runs" in expected:
        return "commit_workflow_runs"
    return "unknown"


def _repo_from_request(request: Mapping[str, Any]) -> str:
    payload = _m(request.get("connector_payload"))
    return str(payload.get("repo_full_name") or payload.get("repository_full_name") or "")


def _normalize_pr(payload: Mapping[str, Any], request: Mapping[str, Any]) -> dict[str, Any]:
    connector_payload = _m(request.get("connector_payload"))
    return {
        "repo_full_name": str(payload.get("repo_full_name") or payload.get("repository_full_name") or _repo_from_request(request)),
        "number": _i(payload.get("number", payload.get("pr_number", connector_payload.get("pr_number"))), 0),
        "state": str(payload.get("state", "open")),
        "merged": payload.get("merged") is True,
        "mergeable": payload.get("mergeable"),
        "draft": payload.get("draft") is True,
        "head_sha": str(payload.get("head_sha") or _m(payload.get("head")).get("sha") or ""),
        "base": str(payload.get("base") if not isinstance(payload.get("base"), Mapping) else _m(payload.get("base")).get("ref", "main")),
        "title": str(payload.get("title", "")),
        "source_raw_result_digest": _sha(dict(payload)),
        "source_request_digest": _sha(dict(request)),
        "epoch": int(time.time()),
    }


def _runs(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = payload.get("workflow_runs", [])
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _normalize_runs(payload: Mapping[str, Any], request: Mapping[str, Any]) -> dict[str, Any]:
    runs = _runs(payload)
    required = payload.get("required_workflows")
    if not isinstance(required, list) or not required:
        required = [str(run.get("name", "")) for run in runs if run.get("name")]
    return {
        "workflow_runs": runs,
        "required_workflows": [str(name) for name in required if str(name)],
        "source_raw_result_digest": _sha(dict(payload)),
        "source_request_digest": _sha(dict(request)),
        "epoch": int(time.time()),
    }


def _planner_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_github_actions_pr_live_request_planner_enabled": True,
        "apply_github_actions_pr_live_request_planner": True,
        "runtime_root": str(root),
    }


def _planner_license() -> dict[str, Any]:
    return {
        "license_status": "QI_GITHUB_ACTIONS_PR_LIVE_REQUEST_PLANNER_LICENSE_READY",
        "query_packet_read_allowed": True,
        "connector_request_write_allowed": True,
        "collector_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def build_qi_github_actions_pr_live_result_adapter(*, runtime_context: Mapping[str, Any], pr_live_result_adapter_license: Mapping[str, Any]) -> QiGitHubActionsPrLiveResultAdapterResult:
    ctx = _m(runtime_context)
    lic = _m(pr_live_result_adapter_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    request_path = root / "qi_github_actions_pr_live_connector_request.json"
    raw_result_path = root / "qi_github_actions_pr_live_connector_result_packet.json"
    receipt_path = root / "qi_github_actions_pr_live_result_adapter_receipt.json"
    audit_path = root / "qi_github_actions_pr_live_result_adapter_audit.jsonl"

    if ctx.get("qi_github_actions_pr_live_result_adapter_enabled") is not True:
        blockers.append("qi_github_actions_pr_live_result_adapter_enabled_not_true")
    if ctx.get("apply_github_actions_pr_live_result_adapter") is not True:
        blockers.append("apply_github_actions_pr_live_result_adapter_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_LIVE_RESULT_ADAPTER_LICENSE_READY":
        blockers.append("github_actions_pr_live_result_adapter_license_not_ready")
    for name in ["connector_request_read_allowed", "connector_result_read_allowed", "adapted_packet_write_allowed", "planner_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    request = _read_json(request_path)
    raw = _read_json(raw_result_path)
    if not request:
        blockers.append("connector_request_missing_or_invalid")
    if not raw:
        blockers.append("connector_result_missing_or_invalid")
    payload = _payload(raw)
    kind = _infer_kind(request, raw) if request or raw else "unknown"
    if kind not in RESULT_KINDS:
        blockers.append("result_kind_not_allowlisted")
    if kind in RESULT_KINDS and lic.get(f"allow_{kind}_result") is not True:
        blockers.append(f"{kind}_not_allowed_by_pr_live_result_adapter_license")

    adapted_path = root / "qi_github_actions_raw_pr_info_packet.json" if kind == "pr_info" else root / "qi_github_actions_raw_commit_workflow_runs_packet.json"
    adapted: dict[str, Any] = {}
    written = False
    planner_status = "NOT_RUN"
    planner_stage = "not_run"
    policy_decision = "not_run"
    action_prepared = "none"
    stop_reason = "not_run"
    if not blockers:
        if kind == "pr_info":
            adapted = _normalize_pr(payload, request)
            if not adapted.get("head_sha"):
                blockers.append("head_sha_missing")
            if _i(adapted.get("number"), 0) <= 0:
                blockers.append("pr_number_invalid")
        else:
            adapted = _normalize_runs(payload, request)
            if not adapted.get("workflow_runs"):
                blockers.append("workflow_runs_empty_or_invalid")
        if not blockers:
            _write_json(adapted_path, adapted)
            written = True
            if ctx.get("continue_planner") is not False:
                planner = build_qi_github_actions_pr_live_request_planner(
                    runtime_context=_planner_context(root),
                    pr_live_request_planner_license=_planner_license(),
                ).to_dict()
                planner_status = str(planner.get("status", "unknown"))
                planner_stage = str(planner.get("planner_stage", "unknown"))
                policy_decision = str(planner.get("policy_decision", "unknown"))
                action_prepared = str(planner.get("action_prepared", "none"))
                stop_reason = str(planner.get("stop_reason", "unknown"))
                if planner_status != "QI_GITHUB_ACTIONS_PR_LIVE_REQUEST_PLANNER_READY":
                    blockers.append("pr_live_request_planner_not_ready")
                    stop_reason = "planner_blocked"

    status = "QI_GITHUB_ACTIONS_PR_LIVE_RESULT_ADAPTER_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_LIVE_RESULT_ADAPTER_BLOCKED"
    packet_id = "qi-github-actions-pr-live-result-adapter-" + _sha({"request": request, "raw": raw, "kind": kind, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_pr_live_result_adapter_v7_6",
        "status": status,
        "packet_id": packet_id,
        "result_kind": kind,
        "adapted_packet_path": str(adapted_path),
        "adapted_packet_written": written,
        "planner_status": planner_status,
        "planner_stage": planner_stage,
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

    return QiGitHubActionsPrLiveResultAdapterResult(
        "kuuos_runtime_daemon_qi_github_actions_pr_live_result_adapter_v7_6",
        status,
        packet_id,
        str(root),
        kind,
        str(adapted_path),
        planner_status,
        planner_stage,
        policy_decision,
        action_prepared,
        stop_reason,
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
