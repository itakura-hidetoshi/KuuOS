#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


OS_NAMES = ("MemoryOS", "PlanOS", "RunGovernance")
DECISIONS = {"accept", "hold", "block"}
READINESS = {
    "accept": "ready",
    "hold": "needs_evidence",
    "block": "repair_required",
}
NEXT_ACTION = {
    "MemoryOS": {
        "accept": "stage_append_only_recall_anchor",
        "hold": "stage_memory_reobserve_request",
        "block": "stage_memory_repair_quarantine",
    },
    "PlanOS": {
        "accept": "stage_weighted_candidate_front",
        "hold": "stage_redecomposition_evidence_request",
        "block": "stage_plan_handoff_repair_quarantine",
    },
    "RunGovernance": {
        "accept": "stage_bounded_queue_gate_candidate",
        "hold": "stage_exit_blocker_review_request",
        "block": "stage_governance_repair_quarantine",
    },
}


@dataclass(frozen=True)
class TriOSFeedbackActionReadinessRouterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    memory_readiness: str
    plan_readiness: str
    run_governance_readiness: str
    readiness_packet_path: str
    receipt_path: str
    audit_path: str
    readiness_packet_written: bool
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


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _latest_decisions(summary: Mapping[str, Any], ledger_rows: list[dict[str, Any]]) -> dict[str, str]:
    decisions: dict[str, str] = {}
    from_summary = _m(summary.get("decisions"))
    for os_name in OS_NAMES:
        decision = str(from_summary.get(os_name, ""))
        if decision in DECISIONS:
            decisions[os_name] = decision
    if len(decisions) == len(OS_NAMES):
        return decisions
    for row in reversed(ledger_rows):
        os_name = str(row.get("target_os", ""))
        decision = str(row.get("decision", ""))
        if os_name in OS_NAMES and decision in DECISIONS and os_name not in decisions:
            decisions[os_name] = decision
    return {os_name: decisions.get(os_name, "block") for os_name in OS_NAMES}


def _history(os_name: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    relevant = [r for r in rows if str(r.get("target_os", "")) == os_name][-5:]
    blockers = [b for r in relevant for b in (r.get("blockers", []) if isinstance(r.get("blockers", []), list) else [])][-8:]
    warnings = [w for r in relevant for w in (r.get("warnings", []) if isinstance(r.get("warnings", []), list) else [])][-8:]
    return {
        "recent_decisions": [str(r.get("decision", "unknown")) for r in relevant],
        "recent_blockers": blockers,
        "recent_warnings": warnings,
        "history_digest": _sha(relevant),
    }


def _readiness_for(os_name: str, decision: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    readiness = READINESS[decision]
    return {
        "target_os": os_name,
        "source_decision": decision,
        "readiness": readiness,
        "next_stage_action": NEXT_ACTION[os_name][decision],
        "history": _history(os_name, rows),
        "boundary": {
            "readiness_only": True,
            "does_not_consume_memory": os_name == "MemoryOS",
            "does_not_commit_plan": os_name == "PlanOS",
            "does_not_run_runner": os_name == "RunGovernance",
            "does_not_authorize_execution": True,
            "blocked_requires_repair_before_ready": decision == "block",
        },
    }


def _packet(summary: Mapping[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    decisions = _latest_decisions(summary, rows)
    readiness = {os_name: _readiness_for(os_name, decisions[os_name], rows) for os_name in OS_NAMES}
    return {
        "version": "tri_os_feedback_action_readiness_router_packet_v9_6",
        "tri_os_feedback_action_readiness_considered": True,
        "readiness": readiness,
        "readiness_counts": {
            "ready": sum(1 for v in readiness.values() if v["readiness"] == "ready"),
            "needs_evidence": sum(1 for v in readiness.values() if v["readiness"] == "needs_evidence"),
            "repair_required": sum(1 for v in readiness.values() if v["readiness"] == "repair_required"),
        },
        "source_digests": {
            "action_intake_summary": _sha(dict(summary)),
            "action_intake_ledger_window": _sha(rows[-9:]),
        },
        "boundary": {
            "router_only": True,
            "readiness_only": True,
            "does_not_consume_memory": True,
            "does_not_commit_plan": True,
            "does_not_run_runner": True,
            "does_not_authorize_execution": True,
            "repair_required_blocks_ready_state": True,
        },
        "epoch": int(time.time()),
    }


def build_tri_os_feedback_action_readiness_router(*, runtime_context: Mapping[str, Any], readiness_router_license: Mapping[str, Any]) -> TriOSFeedbackActionReadinessRouterResult:
    ctx = _m(runtime_context)
    lic = _m(readiness_router_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    summary_path = root / "tri_os_feedback_action_intake_decision_summary.json"
    ledger_path = root / "tri_os_feedback_action_intake_decision_ledger.jsonl"
    packet_path = root / "tri_os_feedback_action_readiness_router_packet.json"
    receipt_path = root / "tri_os_feedback_action_readiness_router_receipt.json"
    audit_path = root / "tri_os_feedback_action_readiness_router_audit.jsonl"

    if ctx.get("tri_os_feedback_action_readiness_router_enabled") is not True:
        blockers.append("tri_os_feedback_action_readiness_router_enabled_not_true")
    if ctx.get("apply_tri_os_feedback_action_readiness_router") is not True:
        blockers.append("apply_tri_os_feedback_action_readiness_router_not_true")
    if lic.get("license_status") != "TRI_OS_FEEDBACK_ACTION_READINESS_ROUTER_LICENSE_READY":
        blockers.append("tri_os_feedback_action_readiness_router_license_not_ready")
    for name in ["action_intake_summary_read_allowed", "action_intake_ledger_read_allowed", "readiness_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    summary = _read_json(summary_path)
    rows = [r for r in _read_jsonl(ledger_path) if r.get("record_type") == "tri_os_feedback_action_intake_decision"]
    if not summary:
        blockers.append("tri_os_feedback_action_intake_decision_summary_missing_or_invalid")
    if summary and summary.get("boundary", {}).get("does_not_authorize_execution") is not True:
        blockers.append("summary_execution_boundary_invalid")
    if summary and summary.get("boundary", {}).get("action_intake_history_only") is not True:
        blockers.append("summary_action_intake_history_boundary_invalid")
    if not rows:
        warnings.append("tri_os_feedback_action_intake_decision_ledger_empty_or_missing")
    if summary:
        decisions = _m(summary.get("decisions"))
        for os_name in OS_NAMES:
            if str(decisions.get(os_name, "")) not in DECISIONS:
                blockers.append(f"{os_name.lower()}_summary_decision_invalid")

    packet: dict[str, Any] = {}
    written = False
    memory_readiness = plan_readiness = run_readiness = "unknown"
    if not blockers:
        packet = _packet(summary, rows)
        if packet.get("boundary", {}).get("does_not_authorize_execution") is not True:
            blockers.append("readiness_router_boundary_invalid")
        else:
            memory_readiness = str(packet["readiness"]["MemoryOS"]["readiness"])
            plan_readiness = str(packet["readiness"]["PlanOS"]["readiness"])
            run_readiness = str(packet["readiness"]["RunGovernance"]["readiness"])
            _write_json(packet_path, packet)
            written = True

    status = "TRI_OS_FEEDBACK_ACTION_READINESS_ROUTER_READY" if not blockers else "TRI_OS_FEEDBACK_ACTION_READINESS_ROUTER_BLOCKED"
    packet_id = "tri-os-feedback-action-readiness-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_tri_os_feedback_action_readiness_router_v9_6",
        "status": status,
        "packet_id": packet_id,
        "memory_readiness": memory_readiness,
        "plan_readiness": plan_readiness,
        "run_governance_readiness": run_readiness,
        "readiness_packet_written": written,
        "readiness_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return TriOSFeedbackActionReadinessRouterResult(
        "kuuos_runtime_daemon_tri_os_feedback_action_readiness_router_v9_6",
        status,
        packet_id,
        str(root),
        memory_readiness,
        plan_readiness,
        run_readiness,
        str(packet_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
