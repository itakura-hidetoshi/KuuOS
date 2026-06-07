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

FEEDBACK_ACTIONS = {
    "MemoryOS": {
        "accept": "open_append_only_recall_anchor",
        "hold": "request_memory_reobserve_anchor",
        "block": "quarantine_memory_handoff",
    },
    "PlanOS": {
        "accept": "open_weighted_candidate_planning",
        "hold": "request_plan_redecomposition_evidence",
        "block": "block_plan_handoff_input",
    },
    "RunGovernance": {
        "accept": "open_bounded_queue_gate",
        "hold": "request_exit_blocker_review",
        "block": "block_governance_handoff_input",
    },
}


@dataclass(frozen=True)
class TriOSIntakeFeedbackRouterResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    memory_feedback_action: str
    plan_feedback_action: str
    run_governance_feedback_action: str
    feedback_packet_path: str
    receipt_path: str
    audit_path: str
    feedback_packet_written: bool
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


def _reason_window(os_name: str, ledger_rows: list[dict[str, Any]]) -> dict[str, Any]:
    relevant = [r for r in ledger_rows if str(r.get("target_os", "")) == os_name][-3:]
    return {
        "recent_decisions": [str(r.get("decision", "unknown")) for r in relevant],
        "recent_blockers": [b for r in relevant for b in (r.get("blockers", []) if isinstance(r.get("blockers", []), list) else [])][-5:],
        "recent_warnings": [w for r in relevant for w in (r.get("warnings", []) if isinstance(r.get("warnings", []), list) else [])][-5:],
        "recent_window_digest": _sha(relevant),
    }


def _feedback_for(os_name: str, decision: str, ledger_rows: list[dict[str, Any]]) -> dict[str, Any]:
    reasons = _reason_window(os_name, ledger_rows)
    return {
        "target_os": os_name,
        "intake_decision": decision,
        "feedback_action": FEEDBACK_ACTIONS[os_name][decision],
        "feedback_mode": {
            "accept": "open_next_stage",
            "hold": "request_more_evidence",
            "block": "quarantine_or_repair",
        }[decision],
        "reason_window": reasons,
        "boundary": {
            "feedback_only": True,
            "does_not_consume_memory": os_name == "MemoryOS",
            "does_not_commit_plan": os_name == "PlanOS",
            "does_not_run_runner": os_name == "RunGovernance",
            "does_not_authorize_execution": True,
        },
    }


def _packet(summary: Mapping[str, Any], ledger_rows: list[dict[str, Any]]) -> dict[str, Any]:
    decisions = _latest_decisions(summary, ledger_rows)
    feedback = {os_name: _feedback_for(os_name, decisions[os_name], ledger_rows) for os_name in OS_NAMES}
    return {
        "version": "tri_os_intake_feedback_router_packet_v9_2",
        "tri_os_intake_feedback_considered": True,
        "feedback": feedback,
        "feedback_counts": {
            "open_next_stage": sum(1 for v in feedback.values() if v["feedback_mode"] == "open_next_stage"),
            "request_more_evidence": sum(1 for v in feedback.values() if v["feedback_mode"] == "request_more_evidence"),
            "quarantine_or_repair": sum(1 for v in feedback.values() if v["feedback_mode"] == "quarantine_or_repair"),
        },
        "source_digests": {
            "intake_summary": _sha(dict(summary)),
            "intake_ledger_window": _sha(ledger_rows[-9:]),
        },
        "boundary": {
            "router_only": True,
            "feedback_only": True,
            "does_not_consume_memory": True,
            "does_not_commit_plan": True,
            "does_not_run_runner": True,
            "does_not_authorize_execution": True,
            "blocks_remain_blocks_until_repaired": True,
        },
        "epoch": int(time.time()),
    }


def build_tri_os_intake_feedback_router(*, runtime_context: Mapping[str, Any], feedback_router_license: Mapping[str, Any]) -> TriOSIntakeFeedbackRouterResult:
    ctx = _m(runtime_context)
    lic = _m(feedback_router_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    summary_path = root / "tri_os_intake_decision_summary.json"
    ledger_path = root / "tri_os_intake_decision_ledger.jsonl"
    packet_path = root / "tri_os_intake_feedback_router_packet.json"
    receipt_path = root / "tri_os_intake_feedback_router_receipt.json"
    audit_path = root / "tri_os_intake_feedback_router_audit.jsonl"

    if ctx.get("tri_os_intake_feedback_router_enabled") is not True:
        blockers.append("tri_os_intake_feedback_router_enabled_not_true")
    if ctx.get("apply_tri_os_intake_feedback_router") is not True:
        blockers.append("apply_tri_os_intake_feedback_router_not_true")
    if lic.get("license_status") != "TRI_OS_INTAKE_FEEDBACK_ROUTER_LICENSE_READY":
        blockers.append("tri_os_intake_feedback_router_license_not_ready")
    for name in ["intake_summary_read_allowed", "intake_ledger_read_allowed", "feedback_packet_write_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    summary = _read_json(summary_path)
    ledger_rows = [r for r in _read_jsonl(ledger_path) if r.get("record_type") == "tri_os_intake_decision"]
    if not summary:
        blockers.append("tri_os_intake_decision_summary_missing_or_invalid")
    if summary and summary.get("boundary", {}).get("does_not_authorize_execution") is not True:
        blockers.append("summary_execution_boundary_invalid")
    if not ledger_rows:
        warnings.append("tri_os_intake_decision_ledger_empty_or_missing")
    if summary:
        decisions = _m(summary.get("decisions"))
        for os_name in OS_NAMES:
            if str(decisions.get(os_name, "")) not in DECISIONS:
                blockers.append(f"{os_name.lower()}_summary_decision_invalid")

    packet: dict[str, Any] = {}
    written = False
    memory_action = plan_action = run_action = "unknown"
    if not blockers:
        packet = _packet(summary, ledger_rows)
        if packet.get("boundary", {}).get("does_not_authorize_execution") is not True:
            blockers.append("feedback_router_boundary_invalid")
        else:
            memory_action = str(packet["feedback"]["MemoryOS"]["feedback_action"])
            plan_action = str(packet["feedback"]["PlanOS"]["feedback_action"])
            run_action = str(packet["feedback"]["RunGovernance"]["feedback_action"])
            _write_json(packet_path, packet)
            written = True

    status = "TRI_OS_INTAKE_FEEDBACK_ROUTER_READY" if not blockers else "TRI_OS_INTAKE_FEEDBACK_ROUTER_BLOCKED"
    packet_id = "tri-os-intake-feedback-router-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_tri_os_intake_feedback_router_v9_2",
        "status": status,
        "packet_id": packet_id,
        "memory_feedback_action": memory_action,
        "plan_feedback_action": plan_action,
        "run_governance_feedback_action": run_action,
        "feedback_packet_written": written,
        "feedback_packet_digest": _sha(packet),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})
    return TriOSIntakeFeedbackRouterResult(
        "kuuos_runtime_daemon_tri_os_intake_feedback_router_v9_2",
        status,
        packet_id,
        str(root),
        memory_action,
        plan_action,
        run_action,
        str(packet_path),
        str(receipt_path),
        str(audit_path),
        written,
        blockers,
        warnings,
    )
