#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


TERMINAL_STOP_CLASSES = {
    "await_dispatch_result",
    "await_external_call",
    "max_bridge_cycles_reached",
    "max_steps_reached",
    "waiting_for_external_observation",
    "waiting_for_connector_operation",
    "internal_loop_blocked",
    "external_bridge_blocked",
}


@dataclass(frozen=True)
class QiGitHubActionsBridgeLifecycleLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    source_status: str
    stop_reason: str
    cycles_recorded: int
    lifecycle_ledger_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
    ledger_appended: bool
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


def _read_last_digest(path: pathlib.Path) -> str:
    if not path.is_file():
        return "GENESIS"
    last = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            last = line
    if not last:
        return "GENESIS"
    try:
        payload = json.loads(last)
    except json.JSONDecodeError:
        return "CORRUPT_PREVIOUS_LEDGER_LINE"
    return str(payload.get("record_digest", _sha(payload)))


def _cycles(receipt: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = receipt.get("cycle_records", [])
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _cycle_record(source: Mapping[str, Any], cycle: Mapping[str, Any], prev_digest: str) -> dict[str, Any]:
    index = cycle.get("index")
    record = {
        "version": "qi_github_actions_bridge_lifecycle_cycle_record_v6_9",
        "record_type": "cycle",
        "source_packet_id": str(source.get("packet_id", "unknown")),
        "source_status": str(source.get("status", "unknown")),
        "stop_reason": str(source.get("stop_reason", "unknown")),
        "cycle_index": index,
        "internal_status": str(cycle.get("internal_status", "unknown")),
        "internal_stop_reason": str(cycle.get("internal_stop_reason", "unknown")),
        "internal_final_stage": str(cycle.get("internal_final_stage", "unknown")),
        "external_status": str(cycle.get("external_status", "unknown")),
        "external_selected_stage": str(cycle.get("external_selected_stage", "unknown")),
        "external_stage_result_class": str(cycle.get("external_stage_result_class", "unknown")),
        "internal_digest": str(cycle.get("internal_digest", "")),
        "external_digest": str(cycle.get("external_digest", "")),
        "prev_record_digest": prev_digest,
        "epoch": int(time.time()),
    }
    record["record_digest"] = _sha(record)
    return record


def _summary_record(source: Mapping[str, Any], cycle_records: list[dict[str, Any]], prev_digest: str) -> dict[str, Any]:
    stop_reason = str(source.get("stop_reason", "unknown"))
    record = {
        "version": "qi_github_actions_bridge_lifecycle_summary_record_v6_9",
        "record_type": "summary",
        "source_packet_id": str(source.get("packet_id", "unknown")),
        "source_status": str(source.get("status", "unknown")),
        "stop_reason": stop_reason,
        "terminal_stop_known": stop_reason in TERMINAL_STOP_CLASSES,
        "cycles_recorded": len(cycle_records),
        "final_internal_stage": str(source.get("final_internal_stage", "unknown")),
        "final_external_stage": str(source.get("final_external_stage", "unknown")),
        "cycle_record_digests": [str(c.get("record_digest", "")) for c in cycle_records],
        "prev_record_digest": prev_digest,
        "epoch": int(time.time()),
    }
    record["record_digest"] = _sha(record)
    return record


def build_qi_github_actions_bridge_lifecycle_ledger(*, runtime_context: Mapping[str, Any], lifecycle_ledger_license: Mapping[str, Any]) -> QiGitHubActionsBridgeLifecycleLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(lifecycle_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    source_path = root / "qi_github_actions_integrated_bridge_runner_receipt.json"
    ledger_path = root / "qi_github_actions_bridge_lifecycle_ledger.jsonl"
    summary_path = root / "qi_github_actions_bridge_lifecycle_summary.json"
    receipt_path = root / "qi_github_actions_bridge_lifecycle_ledger_receipt.json"
    audit_path = root / "qi_github_actions_bridge_lifecycle_ledger_audit.jsonl"

    if ctx.get("qi_github_actions_bridge_lifecycle_ledger_enabled") is not True:
        blockers.append("qi_github_actions_bridge_lifecycle_ledger_enabled_not_true")
    if ctx.get("apply_github_actions_bridge_lifecycle_ledger") is not True:
        blockers.append("apply_github_actions_bridge_lifecycle_ledger_not_true")
    if lic.get("license_status") != "QI_GITHUB_ACTIONS_BRIDGE_LIFECYCLE_LEDGER_LICENSE_READY":
        blockers.append("github_actions_bridge_lifecycle_ledger_license_not_ready")
    for name in ["integrated_runner_receipt_read_allowed", "lifecycle_ledger_append_allowed", "summary_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    source = _read_json(source_path)
    if not source:
        blockers.append("integrated_runner_receipt_missing_or_invalid")
    source_status = str(source.get("status", "unknown")) if source else "unknown"
    if source and source_status not in {"QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_READY", "QI_GITHUB_ACTIONS_INTEGRATED_BRIDGE_RUNNER_BLOCKED"}:
        blockers.append("integrated_runner_receipt_status_invalid")
    stop_reason = str(source.get("stop_reason", "unknown")) if source else "unknown"
    cycles = _cycles(source)
    if source and not cycles:
        warnings.append("integrated_runner_receipt_has_no_cycle_records")

    ledger_appended = False
    cycle_records: list[dict[str, Any]] = []
    summary: dict[str, Any] = {}
    if not blockers:
        prev = _read_last_digest(ledger_path)
        for cycle in cycles:
            record = _cycle_record(source, cycle, prev)
            _append_jsonl(ledger_path, record)
            cycle_records.append(record)
            prev = str(record["record_digest"])
        summary = _summary_record(source, cycle_records, prev)
        _append_jsonl(ledger_path, summary)
        _write_json(summary_path, summary)
        ledger_appended = True

    status = "QI_GITHUB_ACTIONS_BRIDGE_LIFECYCLE_LEDGER_READY" if not blockers else "QI_GITHUB_ACTIONS_BRIDGE_LIFECYCLE_LEDGER_BLOCKED"
    packet_id = "qi-github-actions-bridge-lifecycle-" + _sha({"source": source, "summary": summary, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_qi_github_actions_bridge_lifecycle_ledger_v6_9",
        "status": status,
        "packet_id": packet_id,
        "source_status": source_status,
        "stop_reason": stop_reason,
        "cycles_recorded": len(cycle_records),
        "ledger_appended": ledger_appended,
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return QiGitHubActionsBridgeLifecycleLedgerResult(
        "kuuos_runtime_daemon_qi_github_actions_bridge_lifecycle_ledger_v6_9",
        status,
        packet_id,
        str(root),
        source_status,
        stop_reason,
        len(cycle_records),
        str(ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        ledger_appended,
        blockers,
        warnings,
    )
