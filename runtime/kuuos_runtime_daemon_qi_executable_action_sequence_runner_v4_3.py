#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_executable_action_dispatcher_v4_2 import ALLOWLISTED_ACTIONS, build_qi_executable_action_dispatcher


@dataclass(frozen=True)
class QiExecutableActionSequenceRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    sequence_length: int
    actions_run: int
    stop_reason: str
    receipt_path: str
    audit_path: str
    sequence_completed: bool
    blockers: list[str]
    warnings: list[str]
    action_records: list[dict[str, Any]]

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


def _sequence(packet: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = packet.get("sequence", [])
    if not isinstance(raw, list):
        return []
    out: list[dict[str, Any]] = []
    for item in raw:
        if isinstance(item, str):
            out.append({"action": item, "action_allowed": True, "action_context_patch": {}})
        elif isinstance(item, Mapping):
            out.append(dict(item))
    return out


def _dispatcher_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_executable_action_dispatcher_enabled": True,
        "apply_executable_action_dispatcher": True,
        "runtime_root": str(root),
    }


def _dispatcher_license(action: str) -> dict[str, Any]:
    return {
        "license_status": "QI_EXECUTABLE_ACTION_DISPATCHER_LICENSE_READY",
        "action_packet_read_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        f"allow_{action}_action": True,
    }


def _action_record(index: int, action: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "index": index,
        "action": action,
        "status": str(payload.get("status", "unknown")),
        "delegated_status": str(payload.get("delegated_status", "unknown")),
        "packet_id": str(payload.get("packet_id", "unknown")),
        "digest": _sha(dict(payload)),
        "epoch": int(time.time()),
    }


def build_qi_executable_action_sequence_runner(*, runtime_context: Mapping[str, Any], sequence_runner_license: Mapping[str, Any]) -> QiExecutableActionSequenceRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(sequence_runner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    sequence_packet_path = root / "qi_executable_action_sequence_packet.json"
    action_packet_path = root / "qi_executable_action_packet.json"
    receipt_path = root / "qi_executable_action_sequence_runner_receipt.json"
    audit_path = root / "qi_executable_action_sequence_runner_audit.jsonl"

    if ctx.get("qi_executable_action_sequence_runner_enabled") is not True:
        blockers.append("qi_executable_action_sequence_runner_enabled_not_true")
    if ctx.get("apply_executable_action_sequence_runner") is not True:
        blockers.append("apply_executable_action_sequence_runner_not_true")
    if lic.get("license_status") != "QI_EXECUTABLE_ACTION_SEQUENCE_RUNNER_LICENSE_READY":
        blockers.append("executable_action_sequence_runner_license_not_ready")
    for name in ["sequence_packet_read_allowed", "action_packet_write_allowed", "dispatcher_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read_json(sequence_packet_path)
    if not packet:
        blockers.append("sequence_packet_missing_or_invalid")
    if packet and packet.get("sequence_allowed") is not True:
        blockers.append("sequence_packet_sequence_allowed_not_true")
    actions = _sequence(packet)
    if packet and not actions:
        blockers.append("sequence_empty_or_invalid")
    cap = _i(ctx.get("max_sequence_actions", packet.get("max_sequence_actions", 5) if packet else 5), 5)
    if cap < 1:
        blockers.append("max_sequence_actions_invalid")
        cap = 0
    if cap > 20:
        warnings.append("max_sequence_actions_capped_to_20")
        cap = 20
    if len(actions) > cap:
        blockers.append("sequence_exceeds_cap")

    action_records: list[dict[str, Any]] = []
    stop_reason = "not_run"
    if not blockers:
        stop_reason = "sequence_completed"
        for index, item in enumerate(actions, start=1):
            action = str(item.get("action", "unknown"))
            if action not in ALLOWLISTED_ACTIONS:
                blockers.append("action_not_allowlisted")
                stop_reason = "blocked"
                break
            if item.get("action_allowed") is not True:
                blockers.append("action_packet_action_allowed_not_true")
                stop_reason = "blocked"
                break
            action_packet = {
                "action": action,
                "action_allowed": True,
                "action_context_patch": dict(_m(item.get("action_context_patch"))),
                "sequence_index": index,
                "sequence_source": "qi_executable_action_sequence_runner_v4_3",
            }
            _write_json(action_packet_path, action_packet)
            result = build_qi_executable_action_dispatcher(
                runtime_context=_dispatcher_context(root),
                dispatcher_license=_dispatcher_license(action),
            ).to_dict()
            action_records.append(_action_record(index, action, result))
            if result.get("status") != "QI_EXECUTABLE_ACTION_DISPATCHER_READY":
                blockers.append("delegated_action_blocked")
                stop_reason = "blocked"
                break

    sequence_completed = not blockers and len(action_records) == len(actions)
    status = "QI_EXECUTABLE_ACTION_SEQUENCE_RUNNER_READY" if sequence_completed else "QI_EXECUTABLE_ACTION_SEQUENCE_RUNNER_BLOCKED"
    packet_id = "qi-executable-action-sequence-" + _sha({"packet": packet, "records": action_records, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_executable_action_sequence_runner_v4_3",
        "status": status,
        "packet_id": packet_id,
        "sequence_length": len(actions),
        "actions_run": len(action_records),
        "stop_reason": stop_reason,
        "sequence_completed": sequence_completed,
        "action_records": action_records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiExecutableActionSequenceRunnerResult(
        "kuuos_runtime_daemon_qi_executable_action_sequence_runner_v4_3",
        status,
        packet_id,
        str(root),
        len(actions),
        len(action_records),
        stop_reason,
        str(receipt_path),
        str(audit_path),
        sequence_completed,
        blockers,
        warnings,
        action_records,
    )
