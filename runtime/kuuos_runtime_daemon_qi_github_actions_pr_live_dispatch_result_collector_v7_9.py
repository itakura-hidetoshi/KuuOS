#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


DISPATCH_PACKET_BY_TARGET = {
    "pr_info": "qi_github_actions_pr_live_dispatch_pr_info_packet.json",
    "commit_workflow_runs": "qi_github_actions_pr_live_dispatch_commit_workflow_runs_packet.json",
}

DISPATCH_RESULT_BY_TARGET = {
    "pr_info": "qi_github_actions_pr_live_dispatch_pr_info_result.json",
    "commit_workflow_runs": "qi_github_actions_pr_live_dispatch_commit_workflow_runs_result.json",
}

RESULT_KIND_BY_TARGET = {
    "pr_info": "pr_info",
    "commit_workflow_runs": "commit_workflow_runs",
}


@dataclass(frozen=True)
class QiGitHubActionsPrLiveDispatchResultCollectorResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    dispatch_target: str
    result_kind: str
    connector_result_path: str
    bridge_request_path: str
    receipt_path: str
    audit_path: str
    connector_result_written: bool
    bridge_request_written: bool
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


def _infer_target(root: pathlib.Path, ctx: Mapping[str, Any]) -> str:
    explicit = str(ctx.get("dispatch_target", ""))
    if explicit in DISPATCH_PACKET_BY_TARGET:
        return explicit
    for target in DISPATCH_PACKET_BY_TARGET:
        if _read_json(root / DISPATCH_RESULT_BY_TARGET[target]):
            return target
    for target in DISPATCH_PACKET_BY_TARGET:
        if _read_json(root / DISPATCH_PACKET_BY_TARGET[target]):
            return target
    return "unknown"


def _payload(result: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = result.get("connector_result")
    return nested if isinstance(nested, Mapping) else result


def _validate_result(target: str, payload: Mapping[str, Any], blockers: list[str]) -> None:
    if target == "pr_info":
        head = payload.get("head")
        nested_sha = head.get("sha") if isinstance(head, Mapping) else ""
        if not str(payload.get("head_sha") or nested_sha or "").strip():
            blockers.append("head_sha_missing")
        if not (payload.get("number") or payload.get("pr_number")):
            blockers.append("pr_number_missing")
    elif target == "commit_workflow_runs":
        runs = payload.get("workflow_runs")
        if not isinstance(runs, list) or not runs:
            blockers.append("workflow_runs_empty_or_invalid")


def _connector_result(dispatch: Mapping[str, Any], result: Mapping[str, Any], target: str) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_pr_live_connector_result_packet_from_dispatch_v7_9",
        "result_kind": RESULT_KIND_BY_TARGET[target],
        "connector_action": str(dispatch.get("connector_action", "unknown")),
        "connector_result": dict(_payload(result)),
        "result_expected_file": str(dispatch.get("result_expected_file", "unknown")),
        "source_dispatch_digest": _sha(dict(dispatch)),
        "source_dispatch_result_digest": _sha(dict(result)),
        "epoch": int(time.time()),
    }


def _bridge_request(dispatch: Mapping[str, Any], connector_result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "connector_action": str(dispatch.get("connector_action", "unknown")),
        "connector_payload": dict(_m(dispatch.get("connector_payload"))),
        "result_expected_file": str(dispatch.get("result_expected_file", "unknown")),
        "source_connector_result_digest": _sha(dict(connector_result)),
        "epoch": int(time.time()),
    }


def build_qi_github_actions_pr_live_dispatch_result_collector(*, runtime_context: Mapping[str, Any], pr_live_dispatch_result_collector_license: Mapping[str, Any]) -> QiGitHubActionsPrLiveDispatchResultCollectorResult:
    ctx = _m(runtime_context)
    lic = _m(pr_live_dispatch_result_collector_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    connector_result_path = root / "qi_github_actions_pr_live_connector_result_packet.json"
    bridge_request_path = root / "qi_github_actions_pr_live_connector_request.json"
    receipt_path = root / "qi_github_actions_pr_live_dispatch_result_collector_receipt.json"
    audit_path = root / "qi_github_actions_pr_live_dispatch_result_collector_audit.jsonl"

    if ctx.get("qi_github_actions_pr_live_dispatch_result_collector_enabled") is not True:
        blockers.append("qi_github_actions_pr_live_dispatch_result_collector_enabled_not_true")
    if ctx.get("apply_github_actions_pr_live_dispatch_result_collector") is not True:
        blockers.append("apply_github_actions_pr_live_dispatch_result_collector_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_LIVE_DISPATCH_RESULT_COLLECTOR_LICENSE_READY":
        blockers.append("github_actions_pr_live_dispatch_result_collector_license_not_ready")
    for name in ["dispatch_packet_read_allowed", "dispatch_result_read_allowed", "connector_result_write_allowed", "bridge_request_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    target = _infer_target(root, ctx)
    if target not in DISPATCH_PACKET_BY_TARGET:
        blockers.append("dispatch_target_not_allowlisted")
    if target in DISPATCH_PACKET_BY_TARGET and lic.get(f"allow_{target}_collect") is not True:
        blockers.append(f"{target}_not_allowed_by_pr_live_dispatch_result_collector_license")

    dispatch = _read_json(root / DISPATCH_PACKET_BY_TARGET.get(target, "missing")) if target in DISPATCH_PACKET_BY_TARGET else {}
    result = _read_json(root / DISPATCH_RESULT_BY_TARGET.get(target, "missing")) if target in DISPATCH_RESULT_BY_TARGET else {}
    if not dispatch:
        blockers.append("dispatch_packet_missing_or_invalid")
    if not result:
        blockers.append("dispatch_result_missing_or_invalid")
    if dispatch and str(dispatch.get("dispatch_target", "")) != target:
        blockers.append("dispatch_target_mismatch")
    if result and result.get("dispatch_result_allowed") is not True:
        blockers.append("dispatch_result_allowed_not_true")
    if target in DISPATCH_PACKET_BY_TARGET and result:
        _validate_result(target, _payload(result), blockers)

    connector_result: dict[str, Any] = {}
    connector_written = False
    bridge_written = False
    if not blockers:
        connector_result = _connector_result(dispatch, result, target)
        bridge = _bridge_request(dispatch, connector_result)
        _write_json(connector_result_path, connector_result)
        _write_json(bridge_request_path, bridge)
        connector_written = True
        bridge_written = True

    status = "QI_GITHUB_ACTIONS_PR_LIVE_DISPATCH_RESULT_COLLECTOR_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_LIVE_DISPATCH_RESULT_COLLECTOR_BLOCKED"
    packet_id = "qi-github-actions-pr-live-dispatch-result-" + _sha({"target": target, "dispatch": dispatch, "result": result, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_pr_live_dispatch_result_collector_v7_9",
        "status": status,
        "packet_id": packet_id,
        "dispatch_target": target,
        "result_kind": RESULT_KIND_BY_TARGET.get(target, "unknown"),
        "connector_result_written": connector_written,
        "bridge_request_written": bridge_written,
        "connector_result_digest": _sha(connector_result),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPrLiveDispatchResultCollectorResult(
        "kuuos_runtime_daemon_qi_github_actions_pr_live_dispatch_result_collector_v7_9",
        status,
        packet_id,
        str(root),
        target,
        RESULT_KIND_BY_TARGET.get(target, "unknown"),
        str(connector_result_path),
        str(bridge_request_path),
        str(receipt_path),
        str(audit_path),
        connector_written,
        bridge_written,
        blockers,
        warnings,
    )
