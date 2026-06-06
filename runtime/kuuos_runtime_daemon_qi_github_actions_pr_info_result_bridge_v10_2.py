#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


@dataclass(frozen=True)
class QiGitHubActionsPrInfoResultBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_state: str
    action_prepared: str
    raw_pr_info_path: str
    handoff_packet_path: str
    evaluation_packet_path: str
    receipt_path: str
    audit_path: str
    raw_pr_info_written: bool
    handoff_packet_written: bool
    evaluation_packet_written: bool
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


def _head_sha(pr: Mapping[str, Any]) -> str:
    head = pr.get("head")
    nested_sha = head.get("sha") if isinstance(head, Mapping) else ""
    return str(pr.get("head_sha") or nested_sha or "").strip()


def _repo(pr: Mapping[str, Any], call: Mapping[str, Any]) -> str:
    payload = _m(call.get("connector_payload"))
    return str(pr.get("repo_full_name") or pr.get("repository_full_name") or payload.get("repo_full_name") or payload.get("repository_full_name") or "").strip()


def _pr_number(pr: Mapping[str, Any], call: Mapping[str, Any]) -> int:
    payload = _m(call.get("connector_payload"))
    return _i(pr.get("number") or pr.get("pr_number") or payload.get("pr_number") or payload.get("pull_number"), 0)


def _validate_call(call: Mapping[str, Any], blockers: list[str]) -> None:
    if call.get("external_call_allowed") is not True:
        blockers.append("external_call_allowed_not_true")
    if call.get("connector_action") != "GitHub.get_pr_info":
        blockers.append("connector_action_mismatch")
    payload = _m(call.get("connector_payload"))
    repo = payload.get("repo_full_name") or payload.get("repository_full_name")
    if not isinstance(repo, str) or "/" not in repo:
        blockers.append("repo_full_name_invalid")
    if _i(payload.get("pr_number") or payload.get("pull_number"), 0) <= 0:
        blockers.append("pr_number_invalid")


def _validate_raw(raw: Mapping[str, Any], call: Mapping[str, Any], blockers: list[str]) -> Mapping[str, Any]:
    action = str(raw.get("connector_action", call.get("connector_action", "")))
    if action != "GitHub.get_pr_info":
        blockers.append("raw_result_connector_action_mismatch")
    pr = _payload(raw)
    repo = _repo(pr, call)
    if "/" not in repo:
        blockers.append("repo_full_name_missing")
    if _pr_number(pr, call) <= 0:
        blockers.append("pr_number_missing")
    if not _head_sha(pr):
        blockers.append("head_sha_missing")
    return pr


def _bridge_state(pr: Mapping[str, Any]) -> tuple[str, str, list[str]]:
    reasons: list[str] = []
    if str(pr.get("state", "open")) != "open":
        reasons.append("pr_not_open")
    if pr.get("draft") is True:
        reasons.append("pr_is_draft")
    if pr.get("merged") is True:
        reasons.append("pr_already_merged")
    mergeable = pr.get("mergeable")
    if mergeable is False:
        reasons.append("pr_not_mergeable")
    if reasons:
        return "merge_hold", "none", reasons
    return "merge_handoff_ready", "merge_pull_request", reasons


def _raw_pr_info_packet(pr: Mapping[str, Any], call: Mapping[str, Any], raw: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_policy_reentry_raw_pr_info_v10_2",
        "repo_full_name": _repo(pr, call),
        "number": _pr_number(pr, call),
        "state": str(pr.get("state", "open")),
        "draft": pr.get("draft") is True,
        "merged": pr.get("merged") is True,
        "mergeable": pr.get("mergeable"),
        "head_sha": _head_sha(pr),
        "base": pr.get("base"),
        "source_raw_result_digest": _sha(dict(raw)),
        "epoch": int(time.time()),
    }


def _handoff_packet(pr_packet: Mapping[str, Any], raw: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_policy_reentry_pr_info_handoff_packet_v10_2",
        "handoff_allowed": True,
        "autopilot_state": "policy_ready",
        "policy_decision": "policy_all_green_pr_refreshed",
        "action_prepared": "merge_pull_request",
        "raw_pr_info_digest": _sha(dict(pr_packet)),
        "source_raw_result_digest": _sha(dict(raw)),
        "boundary": {
            "handoff_only": True,
            "does_not_call_connector_inside_runtime": True,
            "does_not_apply_policy_action": True,
            "feeds_v8_6_policy_action_handoff": True,
        },
        "epoch": int(time.time()),
    }


def _evaluation_packet(state: str, action: str, pr_packet: Mapping[str, Any], reasons: list[str], raw: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_policy_reentry_pr_info_evaluation_packet_v10_2",
        "evaluation_allowed": True,
        "bridge_state": state,
        "action_prepared": action,
        "hold_reasons": reasons,
        "raw_pr_info": dict(pr_packet),
        "source_raw_result_digest": _sha(dict(raw)),
        "boundary": {
            "evaluation_only": True,
            "does_not_call_connector_inside_runtime": True,
            "does_not_apply_policy_action": True,
            "append_only_audit_surface": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_pr_info_result_bridge(*, runtime_context: Mapping[str, Any], pr_info_result_bridge_license: Mapping[str, Any]) -> QiGitHubActionsPrInfoResultBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(pr_info_result_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)

    call_path = root / "qi_github_actions_policy_reentry_external_call_packet.json"
    raw_path = root / "qi_github_actions_policy_reentry_pr_info_raw_result_packet.json"
    raw_pr_path = root / "qi_github_actions_raw_pr_info_packet.json"
    handoff_path = root / "qi_github_actions_pr_live_autopilot_handoff_packet.json"
    evaluation_path = root / "qi_github_actions_policy_reentry_pr_info_evaluation_packet.json"
    receipt_path = root / "qi_github_actions_pr_info_result_bridge_receipt.json"
    audit_path = root / "qi_github_actions_pr_info_result_bridge_audit.jsonl"

    if ctx.get("qi_github_actions_pr_info_result_bridge_enabled") is not True:
        blockers.append("qi_github_actions_pr_info_result_bridge_enabled_not_true")
    if ctx.get("apply_github_actions_pr_info_result_bridge") is not True:
        blockers.append("apply_github_actions_pr_info_result_bridge_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_PR_INFO_RESULT_BRIDGE_LICENSE_READY":
        blockers.append("github_actions_pr_info_result_bridge_license_not_ready")
    for name in ["external_call_packet_read_allowed", "raw_result_packet_read_allowed", "raw_pr_info_packet_write_allowed", "handoff_packet_write_allowed", "evaluation_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    call = _read_json(call_path)
    raw = _read_json(raw_path)
    if not call:
        blockers.append("external_call_packet_missing_or_invalid")
    if not raw:
        blockers.append("raw_result_packet_missing_or_invalid")
    if call:
        _validate_call(call, blockers)
    pr = _validate_raw(raw, call, blockers) if raw and call else {}

    bridge_state = "blocked"
    action = "none"
    pr_packet: dict[str, Any] = {}
    handoff: dict[str, Any] = {}
    evaluation: dict[str, Any] = {}
    raw_written = False
    handoff_written = False
    evaluation_written = False
    if not blockers:
        pr_packet = _raw_pr_info_packet(pr, call, raw)
        bridge_state, action, hold_reasons = _bridge_state(pr)
        if hold_reasons:
            warnings.extend(hold_reasons)
        evaluation = _evaluation_packet(bridge_state, action, pr_packet, hold_reasons, raw)
        _write_json(raw_pr_path, pr_packet)
        _write_json(evaluation_path, evaluation)
        raw_written = True
        evaluation_written = True
        if bridge_state == "merge_handoff_ready":
            handoff = _handoff_packet(pr_packet, raw)
            _write_json(handoff_path, handoff)
            handoff_written = True

    status = "QI_GITHUB_ACTIONS_PR_INFO_RESULT_BRIDGE_READY" if not blockers else "QI_GITHUB_ACTIONS_PR_INFO_RESULT_BRIDGE_BLOCKED"
    packet_id = "qi-github-actions-pr-info-result-bridge-" + _sha({"call": call, "raw": raw, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_pr_info_result_bridge_v10_2",
        "status": status,
        "packet_id": packet_id,
        "bridge_state": bridge_state,
        "action_prepared": action,
        "raw_pr_info_written": raw_written,
        "handoff_packet_written": handoff_written,
        "evaluation_packet_written": evaluation_written,
        "raw_pr_info_digest": _sha(pr_packet),
        "handoff_packet_digest": _sha(handoff),
        "evaluation_packet_digest": _sha(evaluation),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return QiGitHubActionsPrInfoResultBridgeResult(
        "kuuos_runtime_daemon_qi_github_actions_pr_info_result_bridge_v10_2",
        status,
        packet_id,
        str(root),
        bridge_state,
        action,
        str(raw_pr_path),
        str(handoff_path),
        str(evaluation_path),
        str(receipt_path),
        str(audit_path),
        raw_written,
        handoff_written,
        evaluation_written,
        blockers,
        warnings,
    )
