#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_executable_capability_router_v4_9 import CAPABILITY_INPUTS, build_qi_executable_capability_router


@dataclass(frozen=True)
class QiExecutableCapabilitySequenceRunnerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    sequence_length: int
    capabilities_run: int
    stop_reason: str
    receipt_path: str
    audit_path: str
    sequence_completed: bool
    blockers: list[str]
    warnings: list[str]
    capability_records: list[dict[str, Any]]

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
        if isinstance(item, Mapping):
            out.append(dict(item))
    return out


def _router_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "qi_executable_capability_router_enabled": True,
        "apply_executable_capability_router": True,
        "runtime_root": str(root),
    }


def _router_license(kind: str) -> dict[str, Any]:
    return {
        "license_status": "QI_EXECUTABLE_CAPABILITY_ROUTER_LICENSE_READY",
        "capability_packet_read_allowed": True,
        "delegated_packet_write_allowed": True,
        "delegated_run_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        f"allow_{kind}_capability": True,
    }


def _capability_record(index: int, kind: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "index": index,
        "capability_kind": kind,
        "status": str(payload.get("status", "unknown")),
        "delegated_status": str(payload.get("delegated_status", "unknown")),
        "packet_id": str(payload.get("packet_id", "unknown")),
        "digest": _sha(dict(payload)),
        "epoch": int(time.time()),
    }


def build_qi_executable_capability_sequence_runner(*, runtime_context: Mapping[str, Any], sequence_runner_license: Mapping[str, Any]) -> QiExecutableCapabilitySequenceRunnerResult:
    ctx = _m(runtime_context)
    lic = _m(sequence_runner_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    sequence_packet_path = root / "qi_executable_capability_sequence_packet.json"
    capability_packet_path = root / "qi_executable_capability_packet.json"
    receipt_path = root / "qi_executable_capability_sequence_runner_receipt.json"
    audit_path = root / "qi_executable_capability_sequence_runner_audit.jsonl"

    if ctx.get("qi_executable_capability_sequence_runner_enabled") is not True:
        blockers.append("qi_executable_capability_sequence_runner_enabled_not_true")
    if ctx.get("apply_executable_capability_sequence_runner") is not True:
        blockers.append("apply_executable_capability_sequence_runner_not_true")
    if lic.get("license_status") != "QI_EXECUTABLE_CAPABILITY_SEQUENCE_RUNNER_LICENSE_READY":
        blockers.append("executable_capability_sequence_runner_license_not_ready")
    for name in ["sequence_packet_read_allowed", "capability_packet_write_allowed", "capability_router_run_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read_json(sequence_packet_path)
    if not packet:
        blockers.append("capability_sequence_packet_missing_or_invalid")
    if packet and packet.get("sequence_allowed") is not True:
        blockers.append("capability_sequence_packet_allowed_not_true")
    items = _sequence(packet)
    if packet and not items:
        blockers.append("capability_sequence_empty_or_invalid")
    cap = _i(ctx.get("max_capability_sequence", packet.get("max_capability_sequence", 5) if packet else 5), 5)
    if cap < 1:
        blockers.append("max_capability_sequence_invalid")
        cap = 0
    if cap > 20:
        warnings.append("max_capability_sequence_capped_to_20")
        cap = 20
    if len(items) > cap:
        blockers.append("capability_sequence_exceeds_cap")

    records: list[dict[str, Any]] = []
    stop_reason = "not_run"
    if not blockers:
        stop_reason = "sequence_completed"
        for index, item in enumerate(items, start=1):
            kind = str(item.get("capability_kind", "unknown"))
            if kind not in CAPABILITY_INPUTS:
                blockers.append("capability_kind_not_allowlisted")
                stop_reason = "blocked"
                break
            if item.get("capability_allowed") is not True:
                blockers.append("capability_packet_allowed_not_true")
                stop_reason = "blocked"
                break
            delegated_input = dict(_m(item.get("delegated_input_packet")))
            if not delegated_input:
                blockers.append("delegated_input_packet_missing_or_invalid")
                stop_reason = "blocked"
                break
            capability_packet = {
                "capability_kind": kind,
                "capability_allowed": True,
                "delegated_input_packet": delegated_input,
                "runtime_context_patch": dict(_m(item.get("runtime_context_patch"))),
                "sequence_index": index,
                "sequence_source": "qi_executable_capability_sequence_runner_v5_0",
            }
            _write_json(capability_packet_path, capability_packet)
            result = build_qi_executable_capability_router(
                runtime_context=_router_context(root),
                capability_router_license=_router_license(kind),
            ).to_dict()
            records.append(_capability_record(index, kind, result))
            if result.get("status") != "QI_EXECUTABLE_CAPABILITY_ROUTER_READY":
                blockers.append("delegated_capability_blocked")
                stop_reason = "blocked"
                break

    sequence_completed = not blockers and len(records) == len(items)
    status = "QI_EXECUTABLE_CAPABILITY_SEQUENCE_RUNNER_READY" if sequence_completed else "QI_EXECUTABLE_CAPABILITY_SEQUENCE_RUNNER_BLOCKED"
    packet_id = "qi-executable-capability-sequence-" + _sha({"packet": packet, "records": records, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_executable_capability_sequence_runner_v5_0",
        "status": status,
        "packet_id": packet_id,
        "sequence_length": len(items),
        "capabilities_run": len(records),
        "stop_reason": stop_reason,
        "sequence_completed": sequence_completed,
        "capability_records": records,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiExecutableCapabilitySequenceRunnerResult(
        "kuuos_runtime_daemon_qi_executable_capability_sequence_runner_v5_0",
        status,
        packet_id,
        str(root),
        len(items),
        len(records),
        stop_reason,
        str(receipt_path),
        str(audit_path),
        sequence_completed,
        blockers,
        warnings,
        records,
    )
