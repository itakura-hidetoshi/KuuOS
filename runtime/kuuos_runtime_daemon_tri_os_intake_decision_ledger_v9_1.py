#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


OS_KEYS = {
    "MemoryOS": "memory_os_intake_ledger.jsonl",
    "PlanOS": "plan_os_intake_ledger.jsonl",
    "RunGovernance": "run_governance_intake_ledger.jsonl",
}
DECISIONS = {"accept", "hold", "block"}


@dataclass(frozen=True)
class TriOSIntakeDecisionLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    accepted_count: int
    held_count: int
    blocked_count: int
    unified_ledger_path: str
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


def _last_digest(path: pathlib.Path) -> str:
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


def _decision(packet: Mapping[str, Any], os_name: str) -> Mapping[str, Any]:
    return _m(_m(packet.get("decisions")).get(os_name))


def _record(packet: Mapping[str, Any], os_name: str, prev_unified: str, prev_os: str) -> dict[str, Any]:
    decision_packet = _decision(packet, os_name)
    decision = str(decision_packet.get("decision", "block"))
    blockers = decision_packet.get("blockers", []) if isinstance(decision_packet.get("blockers", []), list) else []
    warnings = decision_packet.get("warnings", []) if isinstance(decision_packet.get("warnings", []), list) else []
    rec = {
        "version": "tri_os_intake_decision_record_v9_1",
        "record_type": "tri_os_intake_decision",
        "target_os": os_name,
        "decision": decision,
        "blockers": blockers,
        "warnings": warnings,
        "source_intake_packet_digest": _sha(dict(packet)),
        "prev_unified_record_digest": prev_unified,
        "prev_os_record_digest": prev_os,
        "epoch": int(time.time()),
    }
    rec["record_digest"] = _sha(rec)
    return rec


def _summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    accepted = sum(1 for r in records if r.get("decision") == "accept")
    held = sum(1 for r in records if r.get("decision") == "hold")
    blocked = sum(1 for r in records if r.get("decision") == "block")
    summary = {
        "version": "tri_os_intake_decision_summary_v9_1",
        "accepted_count": accepted,
        "held_count": held,
        "blocked_count": blocked,
        "decisions": {str(r["target_os"]): str(r["decision"]) for r in records},
        "record_digests": {str(r["target_os"]): str(r["record_digest"]) for r in records},
        "boundary": {
            "ledger_only": True,
            "does_not_consume_memory": True,
            "does_not_commit_plan": True,
            "does_not_run_runner": True,
            "does_not_authorize_execution": True,
        },
        "epoch": int(time.time()),
    }
    summary["summary_digest"] = _sha(summary)
    return summary


def build_tri_os_intake_decision_ledger(*, runtime_context: Mapping[str, Any], intake_ledger_license: Mapping[str, Any]) -> TriOSIntakeDecisionLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(intake_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    intake_path = root / "tri_os_handoff_intake_decision_packet.json"
    unified_path = root / "tri_os_intake_decision_ledger.jsonl"
    summary_path = root / "tri_os_intake_decision_summary.json"
    receipt_path = root / "tri_os_intake_decision_ledger_receipt.json"
    audit_path = root / "tri_os_intake_decision_ledger_audit.jsonl"

    if ctx.get("tri_os_intake_decision_ledger_enabled") is not True:
        blockers.append("tri_os_intake_decision_ledger_enabled_not_true")
    if ctx.get("apply_tri_os_intake_decision_ledger") is not True:
        blockers.append("apply_tri_os_intake_decision_ledger_not_true")
    if lic.get("license_status") != "TRI_OS_INTAKE_DECISION_LEDGER_LICENSE_READY":
        blockers.append("tri_os_intake_decision_ledger_license_not_ready")
    for name in ["intake_packet_read_allowed", "unified_ledger_append_allowed", "os_ledger_append_allowed", "summary_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    intake = _read_json(intake_path)
    if not intake:
        blockers.append("tri_os_handoff_intake_decision_packet_missing_or_invalid")
    elif intake.get("tri_os_handoff_intake_considered") is not True:
        blockers.append("tri_os_handoff_intake_considered_not_true")
    if intake and intake.get("boundary", {}).get("does_not_authorize_execution") is not True:
        blockers.append("intake_execution_boundary_invalid")
    if intake and intake.get("boundary", {}).get("fail_closed_on_boundary_loss") is not True:
        blockers.append("intake_fail_closed_boundary_invalid")
    if intake:
        for os_name in OS_KEYS:
            decision = str(_decision(intake, os_name).get("decision", "missing"))
            if decision not in DECISIONS:
                blockers.append(f"{os_name.lower()}_decision_invalid")

    records: list[dict[str, Any]] = []
    appended = False
    summary: dict[str, Any] = {}
    if not blockers:
        prev_unified = _last_digest(unified_path)
        for os_name, file_name in OS_KEYS.items():
            os_path = root / file_name
            rec = _record(intake, os_name, prev_unified, _last_digest(os_path))
            _append_jsonl(os_path, rec)
            _append_jsonl(unified_path, rec)
            prev_unified = rec["record_digest"]
            records.append(rec)
        summary = _summary(records)
        _write_json(summary_path, summary)
        appended = True

    accepted = sum(1 for r in records if r.get("decision") == "accept")
    held = sum(1 for r in records if r.get("decision") == "hold")
    blocked = sum(1 for r in records if r.get("decision") == "block")
    status = "TRI_OS_INTAKE_DECISION_LEDGER_READY" if not blockers else "TRI_OS_INTAKE_DECISION_LEDGER_BLOCKED"
    packet_id = "tri-os-intake-decision-ledger-" + _sha({"records": records, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_tri_os_intake_decision_ledger_v9_1",
        "status": status,
        "packet_id": packet_id,
        "accepted_count": accepted,
        "held_count": held,
        "blocked_count": blocked,
        "ledger_appended": appended,
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return TriOSIntakeDecisionLedgerResult(
        "kuuos_runtime_daemon_tri_os_intake_decision_ledger_v9_1",
        status,
        packet_id,
        str(root),
        accepted,
        held,
        blocked,
        str(unified_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        appended,
        blockers,
        warnings,
    )
