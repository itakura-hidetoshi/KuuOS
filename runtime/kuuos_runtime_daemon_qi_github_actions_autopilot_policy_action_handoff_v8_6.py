#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ACTION_BY_PREPARED = {
    "merge_pull_request": "merge_pull_request",
    "rerun_failed_workflow_run_jobs": "rerun_failed_workflow_run_jobs",
    "commit_workflow_runs_reobserve": "reobserve_commit_workflow_runs",
}

CONNECTOR_ACTION_BY_KIND = {
    "merge_pull_request": "GitHub.merge_pull_request",
    "rerun_failed_workflow_run_jobs": "GitHub.rerun_failed_workflow_run_jobs",
    "reobserve_commit_workflow_runs": "GitHub.fetch_commit_workflow_runs",
}


@dataclass(frozen=True)
class QiGitHubActionsAutopilotPolicyActionHandoffResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    action_kind: str
    connector_action: str
    action_packet_path: str
    receipt_path: str
    audit_path: str
    action_packet_written: bool
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


def _runs(status: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = status.get("workflow_runs", [])
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _repo(query: Mapping[str, Any], pr: Mapping[str, Any], blockers: list[str]) -> str:
    repo = str(query.get("repo_full_name") or query.get("repository_full_name") or pr.get("repo_full_name") or pr.get("repository_full_name") or "").strip()
    if "/" not in repo:
        blockers.append("repo_full_name_invalid")
    return repo


def _pr_number(query: Mapping[str, Any], pr: Mapping[str, Any], blockers: list[str]) -> int:
    number = _i(query.get("pr_number", query.get("pull_number", pr.get("number", pr.get("pr_number")))), 0)
    if number <= 0:
        blockers.append("pr_number_invalid")
    return number


def _head_sha(query: Mapping[str, Any], pr: Mapping[str, Any], blockers: list[str]) -> str:
    head = pr.get("head")
    nested_sha = head.get("sha") if isinstance(head, Mapping) else ""
    sha = str(query.get("expected_head_sha") or query.get("head_sha") or pr.get("head_sha") or nested_sha or "").strip()
    if not sha:
        blockers.append("expected_head_sha_missing")
    return sha


def _commit_sha(query: Mapping[str, Any], pr: Mapping[str, Any], blockers: list[str]) -> str:
    sha = str(query.get("commit_sha") or query.get("head_sha") or pr.get("head_sha") or "").strip()
    if not sha:
        blockers.append("commit_sha_missing")
    return sha


def _failed_run_id(status: Mapping[str, Any], blockers: list[str]) -> int:
    for run in _runs(status):
        if str(run.get("status")) == "completed" and str(run.get("conclusion")) in {"failure", "cancelled", "timed_out"}:
            run_id = _i(run.get("id"), 0)
            if run_id > 0:
                return run_id
    blockers.append("failed_workflow_run_id_missing")
    return 0


def _validate_handoff(handoff: Mapping[str, Any], blockers: list[str]) -> tuple[str, str]:
    if handoff.get("handoff_allowed") is not True:
        blockers.append("handoff_allowed_not_true")
    if handoff.get("autopilot_state") != "policy_ready":
        blockers.append("handoff_state_not_policy_ready")
    prepared = str(handoff.get("action_prepared", "none"))
    kind = ACTION_BY_PREPARED.get(prepared, "unknown")
    if kind == "unknown":
        blockers.append("action_prepared_not_allowlisted")
    return prepared, kind


def _merge_payload(query: Mapping[str, Any], pr: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    return {
        "repository_full_name": _repo(query, pr, blockers),
        "pr_number": _pr_number(query, pr, blockers),
        "merge_method": str(query.get("merge_method", "merge")),
        "expected_head_sha": _head_sha(query, pr, blockers),
    }


def _rerun_payload(query: Mapping[str, Any], pr: Mapping[str, Any], status: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    return {
        "repo_full_name": _repo(query, pr, blockers),
        "run_id": _failed_run_id(status, blockers),
    }


def _reobserve_payload(query: Mapping[str, Any], pr: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    return {
        "repo_full_name": _repo(query, pr, blockers),
        "commit_sha": _commit_sha(query, pr, blockers),
    }


def _action_packet(kind: str, handoff: Mapping[str, Any], payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_autopilot_policy_action_handoff_packet_v8_6",
        "action_handoff_allowed": True,
        "action_kind": kind,
        "connector_action": CONNECTOR_ACTION_BY_KIND[kind],
        "connector_payload": dict(payload),
        "source_policy_decision": str(handoff.get("policy_decision", "unknown")),
        "source_action_prepared": str(handoff.get("action_prepared", "unknown")),
        "source_handoff_digest": _sha(dict(handoff)),
        "boundary": {
            "packet_only": True,
            "does_not_call_connector_inside_runtime": True,
            "requires_policy_ready_handoff": True,
            "execute_only_after_external_authorization": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_autopilot_policy_action_handoff(*, runtime_context: Mapping[str, Any], policy_action_handoff_license: Mapping[str, Any]) -> QiGitHubActionsAutopilotPolicyActionHandoffResult:
    ctx = _m(runtime_context)
    lic = _m(policy_action_handoff_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    handoff_path = root / "qi_github_actions_pr_live_autopilot_handoff_packet.json"
    query_path = root / "qi_github_actions_pr_live_query_packet.json"
    pr_path = root / "qi_github_actions_raw_pr_info_packet.json"
    status_path = root / "qi_github_actions_status_packet.json"
    action_packet_path = root / "qi_github_actions_autopilot_policy_action_handoff_packet.json"
    receipt_path = root / "qi_github_actions_autopilot_policy_action_handoff_receipt.json"
    audit_path = root / "qi_github_actions_autopilot_policy_action_handoff_audit.jsonl"

    if ctx.get("qi_github_actions_autopilot_policy_action_handoff_enabled") is not True:
        blockers.append("qi_github_actions_autopilot_policy_action_handoff_enabled_not_true")
    if ctx.get("apply_github_actions_autopilot_policy_action_handoff") is not True:
        blockers.append("apply_github_actions_autopilot_policy_action_handoff_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_AUTOPILOT_POLICY_ACTION_HANDOFF_LICENSE_READY":
        blockers.append("github_actions_autopilot_policy_action_handoff_license_not_ready")
    for name in ["handoff_packet_read_allowed", "context_packet_read_allowed", "action_handoff_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    handoff = _read_json(handoff_path)
    query = _read_json(query_path)
    pr = _read_json(pr_path)
    status_packet = _read_json(status_path)
    if not handoff:
        blockers.append("handoff_packet_missing_or_invalid")
    if not query:
        blockers.append("live_query_packet_missing_or_invalid")
    if not pr and handoff.get("action_prepared") == "merge_pull_request":
        blockers.append("raw_pr_info_packet_missing_or_invalid")
    if not status_packet and handoff.get("action_prepared") == "rerun_failed_workflow_run_jobs":
        blockers.append("status_packet_missing_or_invalid")

    prepared = "none"
    kind = "unknown"
    payload: dict[str, Any] = {}
    packet: dict[str, Any] = {}
    written = False
    if handoff:
        prepared, kind = _validate_handoff(handoff, blockers)
    if not blockers:
        if kind == "merge_pull_request":
            payload = _merge_payload(query, pr, blockers)
        elif kind == "rerun_failed_workflow_run_jobs":
            payload = _rerun_payload(query, pr, status_packet, blockers)
        elif kind == "reobserve_commit_workflow_runs":
            payload = _reobserve_payload(query, pr, blockers)
        if not blockers:
            packet = _action_packet(kind, handoff, payload)
            _write_json(action_packet_path, packet)
            written = True

    status = "QI_GITHUB_ACTIONS_AUTOPILOT_POLICY_ACTION_HANDOFF_READY" if not blockers else "QI_GITHUB_ACTIONS_AUTOPILOT_POLICY_ACTION_HANDOFF_BLOCKED"
    packet_id = "qi-github-actions-autopilot-policy-action-" + _sha({"handoff": handoff, "kind": kind, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_autopilot_policy_action_handoff_v8_6",
        "status": status,
        "packet_id": packet_id,
        "action_kind": kind,
        "connector_action": CONNECTOR_ACTION_BY_KIND.get(kind, "unknown"),
        "action_packet_written": written,
        "action_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsAutopilotPolicyActionHandoffResult(
        "kuuos_runtime_daemon_qi_github_actions_autopilot_policy_action_handoff_v8_6",
        status,
        packet_id,
        str(root),
        kind,
        CONNECTOR_ACTION_BY_KIND.get(kind, "unknown"),
        str(action_packet_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
