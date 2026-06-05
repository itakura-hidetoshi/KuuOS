#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_autonomous_change_loop_v2_5 import build_qi_autonomous_change_loop


@dataclass(frozen=True)
class QiForwardChangeRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    input_packet_path: str
    normalized_packet_path: str
    receipt_path: str
    audit_path: str
    downstream_status: str
    forward_intent_seen: bool
    normalized: bool
    blockers: list[str]
    warnings: list[str]
    records: list[dict[str, Any]]

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


def _loop_license() -> dict[str, Any]:
    return {
        "license_status": "QI_AUTONOMOUS_CHANGE_LOOP_LICENSE_READY",
        "packet_read_allowed": True,
        "bridge_plan_write_allowed": True,
        "bridge_run_allowed": True,
        "automerge_packet_write_allowed": True,
        "automerge_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def _normalize_packet(packet: Mapping[str, Any]) -> tuple[dict[str, Any], bool, list[str]]:
    normalized = dict(packet)
    notes: list[str] = []
    mode = str(normalized.get("mode", "mock"))
    forward_intent = normalized.get("forward_intent") is True or normalized.get("explicit_change_loop_license") is True
    if forward_intent:
        normalized.setdefault("explicit_change_loop_license", True)
        normalized.setdefault("explicit_automerge_license", True)
        normalized.setdefault("merge_allowed", True)
        normalized.setdefault("pull_request_not_draft", True)
        normalized.setdefault("mergeable", True)
        normalized.setdefault("no_unresolved_blockers", True)
        normalized.setdefault("allowed_repository", True)
        normalized.setdefault("allowed_base_branch", True)
        if mode == "real":
            normalized["execute_external_actions"] = normalized.get("execute_external_actions", True)
        notes.append("forward_intent_normalized")
    return normalized, forward_intent, notes


def build_qi_forward_change_runner(*, runtime_context: Mapping[str, Any], runner_license_packet: Mapping[str, Any]) -> QiForwardChangeRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(runner_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    root = _root(ctx.get("runtime_root"), blockers)
    input_packet_path = root / "forward_change_packet.json"
    normalized_packet_path = root / "autonomous_change_loop_packet.json"
    receipt_path = root / "forward_change_receipt.json"
    audit_path = root / "forward_change_audit.jsonl"
    if ctx.get("qi_forward_change_runner_enabled") is not True:
        blockers.append("qi_forward_change_runner_enabled_not_true")
    if ctx.get("apply_forward_change_runner") is not True:
        blockers.append("apply_forward_change_runner_not_true")
    if lic.get("license_status") != "QI_FORWARD_CHANGE_RUNNER_LICENSE_READY":
        blockers.append("forward_change_runner_license_not_ready")
    for name in ["packet_read_allowed", "packet_write_allowed", "loop_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    packet = _read_json(input_packet_path)
    normalized_packet, forward_intent, notes = _normalize_packet(packet)
    warnings.extend(notes)
    downstream_status = "NOT_RUN"
    normalized = False
    if not forward_intent:
        blockers.append("forward_intent_missing")
    if not blockers:
        _write_json(normalized_packet_path, normalized_packet)
        normalized = True
        loop = build_qi_autonomous_change_loop(runtime_context={"qi_autonomous_change_loop_enabled": True, "apply_autonomous_change_loop": True, "runtime_root": str(root), "mode": str(normalized_packet.get("mode", "mock"))}, loop_license_packet=_loop_license())
        loop_payload = loop.to_dict()
        downstream_status = str(loop_payload.get("status"))
        records.append({"stage": "loop", "status": downstream_status, "digest": _sha(loop_payload), "epoch": int(time.time())})
        if downstream_status != "QI_AUTONOMOUS_CHANGE_LOOP_MERGED":
            blockers.append("downstream_loop_not_merged")
    if blockers:
        status = "QI_FORWARD_CHANGE_RUNNER_BLOCKED"
    else:
        status = "QI_FORWARD_CHANGE_RUNNER_MERGED"
    packet_id = "qi-forward-change-runner-" + _sha({"packet": packet, "records": records, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_forward_change_runner_v2_6", "status": status, "packet_id": packet_id, "downstream_status": downstream_status, "forward_intent_seen": forward_intent, "normalized": normalized, "records": records, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiForwardChangeRunnerResult("kuuos_runtime_daemon_qi_forward_change_runner_v2_6", status, packet_id, str(root), str(input_packet_path), str(normalized_packet_path), str(receipt_path), str(audit_path), downstream_status, forward_intent, normalized, blockers, warnings, records)
