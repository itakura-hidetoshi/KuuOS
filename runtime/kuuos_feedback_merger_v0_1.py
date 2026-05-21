#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib
import json
import sys
from typing import Any, Mapping

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

RESOLVED_STATUS_TO_UPDATES = {
    "REOBSERVE_RESOLVED": {"runtime_variation_visible": True, "policy_candidate_receipt": True, "value_witness_receipt": True, "barrier_witness_receipt": True},
    "LINEAGE_RECHECK_RESOLVED": {"receipt_hash": True, "support_refs": True, "registry_key": True},
    "DELIVERY_RECHECK_RESOLVED": {"view_delivery_receipt": True, "channel_scope": True, "acknowledgment_marker": True},
    "BOUNDARY_RECHECK_RESOLVED": {"two_truths_gap": True, "noncollapse_guard": True, "memory_overwrite_blocker": True, "world_identity_blocker": True},
    "HOLD_REVIEW_RESOLVED": {"candidate_only": True, "nonfinal_marker": True},
    "CANDIDATE_NEXT_READY_NONFINAL": {"candidate_only": True, "nonfinal_marker": True, "ready_for_next_candidate_stage": True},
}

WAITING_STATUSES = {
    "REOBSERVE_WAITING",
    "LINEAGE_RECHECK_WAITING",
    "DELIVERY_RECHECK_WAITING",
    "BOUNDARY_RECHECK_WAITING",
    "HOLD_REVIEW_WAITING",
    "CANDIDATE_NEXT_WAITING",
    "QUARANTINE_REVIEW_WAITING",
}
QUARANTINE_RETAIN_STATUSES = {"QUARANTINE_REVIEWED_RETAINED"}

@dataclass(frozen=True)
class KuuOSFeedbackMergeResult:
    merge_status: str
    task_status: str
    next_raw_state: dict[str, Any]
    merge_receipt: dict[str, Any]
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _canonical_hash(payload: Mapping[str, Any]) -> str:
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _compact_qi_process_tensor_receipt(receipt: Mapping[str, Any] | None) -> dict[str, Any]:
    receipt = receipt or {}
    return {
        "process_tensor_visible": bool(receipt.get("process_tensor_visible", False)),
        "transition_continuity_visible": bool(receipt.get("transition_continuity_visible", False)),
        "memory_continuity_visible": bool(receipt.get("memory_continuity_visible", False)),
        "nonmarkov_memory_visible": bool(receipt.get("nonmarkov_memory_visible", False)),
        "process_history_length": int(receipt.get("process_history_length", 0) or 0),
        "transition_support_count": int(receipt.get("transition_support_count", 0) or 0),
        "memory_support_count": int(receipt.get("memory_support_count", 0) or 0),
        "nonmarkov_support_count": int(receipt.get("nonmarkov_support_count", 0) or 0),
        "missing_process_requirements": list(receipt.get("missing_process_requirements", [])),
        "process_tensor_reason": str(receipt.get("process_tensor_reason", "missing_process_tensor_receipt")),
        **NON_AUTHORITY_FLAGS,
    }


def _base_next_state(previous_raw_state: Mapping[str, Any], task_result_receipt: Mapping[str, Any]) -> dict[str, Any]:
    next_state = deepcopy(dict(previous_raw_state))
    next_state.setdefault("candidate_only", True)
    next_state.setdefault("nonfinal_marker", True)
    next_state["cycle_id"] = str(previous_raw_state.get("next_cycle_id") or f"{previous_raw_state.get('cycle_id', 'cycle')}-next")
    next_state["previous_cycle_id"] = previous_raw_state.get("cycle_id")
    source_receipt_hash = task_result_receipt.get("source_receipt_hash") or task_result_receipt.get("receipt_hash")
    if source_receipt_hash:
        next_state["previous_receipt_hash"] = str(source_receipt_hash)
    compact_process_receipt = _compact_qi_process_tensor_receipt(task_result_receipt.get("qi_process_tensor_receipt", {}))
    next_state["previous_qi_process_tensor_receipt"] = compact_process_receipt
    next_state["feedback_qi_process_tensor_receipt"] = compact_process_receipt
    next_state["feedback_qi_process_tensor_summary"] = compact_process_receipt
    next_state["feedback_source_task_hash"] = task_result_receipt.get("task_hash")
    next_state["feedback_source_result_hash"] = task_result_receipt.get("receipt_hash")
    next_state["feedback_applied_at_utc"] = datetime.now(timezone.utc).isoformat()
    for key, value in NON_AUTHORITY_FLAGS.items():
        next_state[key] = value
    return next_state


def merge_task_result_into_next_state(previous_raw_state: Mapping[str, Any], task_result_receipt: Mapping[str, Any]) -> KuuOSFeedbackMergeResult:
    task_status = str(task_result_receipt.get("task_status", "UNKNOWN_TASK_STATUS"))
    next_state = _base_next_state(previous_raw_state, task_result_receipt)
    applied_updates: dict[str, Any] = {}
    opened_notices = list(task_result_receipt.get("opened_notices", []))
    missing = list(task_result_receipt.get("missing_evidence", []))
    compact_process_receipt = _compact_qi_process_tensor_receipt(task_result_receipt.get("qi_process_tensor_receipt", {}))

    if task_status in RESOLVED_STATUS_TO_UPDATES:
        applied_updates = dict(RESOLVED_STATUS_TO_UPDATES[task_status])
        next_state.update(applied_updates)
        next_state["feedback_status"] = "RESOLVED_FOR_NEXT_CANDIDATE_CYCLE"
        next_state["feedback_waiting"] = False
        next_state["quarantine_retained"] = False
        merge_status = "MERGED_RESOLVED_APPEND_ONLY"
    elif task_status in WAITING_STATUSES:
        next_state["feedback_status"] = "WAITING_FOR_MORE_EVIDENCE"
        next_state["feedback_waiting"] = True
        next_state["feedback_missing_evidence"] = missing
        next_state["quarantine_retained"] = task_status == "QUARANTINE_REVIEW_WAITING"
        merge_status = "MERGED_WAITING_APPEND_ONLY"
    elif task_status in QUARANTINE_RETAIN_STATUSES:
        next_state["feedback_status"] = "QUARANTINE_RETAINED_FOR_NEXT_REVIEW"
        next_state["feedback_waiting"] = True
        next_state["quarantine_retained"] = True
        merge_status = "MERGED_QUARANTINE_RETAINED_APPEND_ONLY"
    else:
        next_state["feedback_status"] = "UNKNOWN_RESULT_HELD"
        next_state["feedback_waiting"] = True
        next_state["feedback_missing_evidence"] = missing
        merge_status = "MERGED_UNKNOWN_HELD_APPEND_ONLY"

    receipt_payload = {
        "packet_version": "feedback_merge_receipt_v0_1",
        "merge_status": merge_status,
        "task_status": task_status,
        "source_task_hash": task_result_receipt.get("task_hash"),
        "source_task_result_receipt_hash": task_result_receipt.get("receipt_hash"),
        "source_receipt_hash": task_result_receipt.get("source_receipt_hash"),
        "cycle_id": next_state.get("cycle_id"),
        "previous_cycle_id": next_state.get("previous_cycle_id"),
        "applied_updates": applied_updates,
        "opened_notices": opened_notices,
        "missing_evidence": missing,
        "quarantine_retained": bool(next_state.get("quarantine_retained", False)),
        "qi_process_tensor_receipt": compact_process_receipt,
        "qi_process_tensor_summary": compact_process_receipt,
        "allowed_projection": ["feedback_merge_receipt", "next_raw_state_candidate"],
        **NON_AUTHORITY_FLAGS,
    }
    receipt_hash = _canonical_hash(receipt_payload)
    merge_receipt = {"receipt_hash": receipt_hash, **receipt_payload}
    next_state["feedback_merge_receipt_hash"] = receipt_hash
    next_state["feedback_merge_status"] = merge_status
    return KuuOSFeedbackMergeResult(
        merge_status=merge_status,
        task_status=task_status,
        next_raw_state=next_state,
        merge_receipt=merge_receipt,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: kuuos_feedback_merger_v0_1.py PREVIOUS_RAW_STATE.json TASK_RESULT_RECEIPT.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as f:
        previous_raw_state = json.load(f)
    with open(argv[2], "r", encoding="utf-8") as f:
        task_result_receipt = json.load(f)
    result = merge_task_result_into_next_state(previous_raw_state, task_result_receipt)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
