#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


WAIT_STAGES = {
    "await_connector_operation",
    "await_status_observation",
}


@dataclass(frozen=True)
class QiGitHubActionsExternalWaitResolverResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    wait_stage: str
    connector_action: str
    external_call_packet_path: str
    receipt_path: str
    audit_path: str
    external_call_packet_emitted: bool
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


def _select_wait(root: pathlib.Path, command_packet: Mapping[str, Any]) -> tuple[str, pathlib.Path, dict[str, Any]]:
    stage = str(command_packet.get("selected_stage", "unknown"))
    if stage == "await_connector_operation":
        path = root / "qi_github_actions_connector_execution_request.json"
        return stage, path, _read_json(path)
    if stage == "await_status_observation":
        path = root / "qi_github_actions_observation_connector_request.json"
        return stage, path, _read_json(path)
    if _read_json(root / "qi_github_actions_connector_execution_request.json"):
        path = root / "qi_github_actions_connector_execution_request.json"
        return "await_connector_operation", path, _read_json(path)
    path = root / "qi_github_actions_observation_connector_request.json"
    return "await_status_observation", path, _read_json(path)


def _external_call(stage: str, source_path: pathlib.Path, source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "qi_github_actions_external_call_packet_v6_3",
        "wait_stage": stage,
        "connector_action": str(source.get("connector_action", "unknown")),
        "connector_payload": dict(_m(source.get("connector_payload"))),
        "source_packet_path": str(source_path),
        "source_packet_digest": _sha(dict(source)),
        "result_expected_file": "qi_github_actions_connector_result_packet.json" if stage == "await_connector_operation" else "qi_github_actions_observation_connector_result_packet.json",
        "boundary": {
            "external_wait_resolution_only": True,
            "does_not_call_connector_inside_runtime": True,
            "expects_connector_result_packet_after_external_call": True,
        },
        "epoch": int(time.time()),
    }


def build_qi_github_actions_external_wait_resolver(*, runtime_context: Mapping[str, Any], external_wait_resolver_license: Mapping[str, Any]) -> QiGitHubActionsExternalWaitResolverResult:
    ctx = _m(runtime_context)
    lic = _m(external_wait_resolver_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    command_path = root / "qi_github_actions_loop_command_packet.json"
    external_call_packet_path = root / "qi_github_actions_external_call_packet.json"
    receipt_path = root / "qi_github_actions_external_wait_resolver_receipt.json"
    audit_path = root / "qi_github_actions_external_wait_resolver_audit.jsonl"

    if ctx.get("qi_github_actions_external_wait_resolver_enabled") is not True:
        blockers.append("qi_github_actions_external_wait_resolver_enabled_not_true")
    if ctx.get("apply_github_actions_external_wait_resolver") is not True:
        blockers.append("apply_github_actions_external_wait_resolver_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_EXTERNAL_WAIT_RESOLVER_LICENSE_READY":
        blockers.append("github_actions_external_wait_resolver_license_not_ready")
    for name in ["wait_state_read_allowed", "external_call_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    command_packet = _read_json(command_path)
    if not command_packet:
        warnings.append("loop_command_packet_missing_using_available_wait_source")
    wait_stage, source_path, source_packet = _select_wait(root, command_packet)
    if wait_stage not in WAIT_STAGES:
        blockers.append("wait_stage_not_allowlisted")
    if lic.get(f"allow_{wait_stage}_stage") is not True:
        blockers.append(f"{wait_stage}_not_allowed_by_external_wait_resolver_license")
    if not source_packet:
        blockers.append("wait_source_packet_missing_or_invalid")
    connector_action = str(source_packet.get("connector_action", "unknown")) if source_packet else "unknown"
    if connector_action == "unknown":
        blockers.append("connector_action_missing")
    connector_payload = _m(source_packet.get("connector_payload")) if source_packet else {}
    if not connector_payload:
        blockers.append("connector_payload_missing_or_invalid")

    payload = _external_call(wait_stage, source_path, source_packet)
    emitted = False
    if not blockers:
        _write_json(external_call_packet_path, payload)
        emitted = True
    status = "QI_GITHUB_ACTIONS_EXTERNAL_WAIT_RESOLVER_READY" if not blockers else "QI_GITHUB_ACTIONS_EXTERNAL_WAIT_RESOLVER_BLOCKED"
    packet_id = "qi-github-actions-external-wait-" + _sha({"stage": wait_stage, "source": source_packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_external_wait_resolver_v6_3",
        "status": status,
        "packet_id": packet_id,
        "wait_stage": wait_stage,
        "connector_action": connector_action,
        "external_call_packet_emitted": emitted,
        "external_call_digest": _sha(payload),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsExternalWaitResolverResult(
        "kuuos_runtime_daemon_qi_github_actions_external_wait_resolver_v6_3",
        status,
        packet_id,
        str(root),
        wait_stage,
        connector_action,
        str(external_call_packet_path),
        str(receipt_path),
        str(audit_path),
        emitted,
        blockers,
        warnings,
    )
