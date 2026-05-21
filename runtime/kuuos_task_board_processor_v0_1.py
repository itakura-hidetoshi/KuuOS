#!/usr/bin/env python3
"""KuuOS Task Board Processor v0.1.

Processes non-authoritative task packets from the Action Router task board.
It does not execute actions, finalize truth, overwrite memory, or make clinical
or theorem claims. It reads supplied evidence flags and appends a task result
receipt to an append-only review state.

Safety order:
  quarantine_tasks -> boundary_recheck_tasks -> lineage_recheck_tasks
  -> delivery_recheck_tasks -> reobserve_tasks -> hold_review_tasks
  -> candidate_next_tasks
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib
import json
import sys
from typing import Any, Mapping


TASK_PRIORITY = [
    "quarantine_tasks",
    "boundary_recheck_tasks",
    "lineage_recheck_tasks",
    "delivery_recheck_tasks",
    "reobserve_tasks",
    "hold_review_tasks",
    "candidate_next_tasks",
]

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

REQUIRED_EVIDENCE_BY_QUEUE = {
    "quarantine_tasks": ["boundary_review_evidence", "noncollapse_guard", "identity_blocker"],
    "boundary_recheck_tasks": ["boundary_review_evidence", "two_truths_gap", "noncollapse_guard"],
    "lineage_recheck_tasks": ["receipt_hash", "support_refs", "registry_key"],
    "delivery_recheck_tasks": ["view_delivery_receipt", "channel_scope", "acknowledgment_marker"],
    "reobserve_tasks": ["runtime_variation_visible", "policy_candidate_receipt", "value_witness_receipt", "barrier_witness_receipt"],
    "hold_review_tasks": ["candidate_only", "nonfinal_marker", "hold_review_evidence"],
    "candidate_next_tasks": ["candidate_only", "nonfinal_marker", "two_truths_gap", "noncollapse_guard"],
}

SUCCESS_STATUS_BY_QUEUE = {
    "quarantine_tasks": "QUARANTINE_REVIEWED_RETAINED",
    "boundary_recheck_tasks": "BOUNDARY_RECHECK_RESOLVED",
    "lineage_recheck_tasks": "LINEAGE_RECHECK_RESOLVED",
    "delivery_recheck_tasks": "DELIVERY_RECHECK_RESOLVED",
    "reobserve_tasks": "REOBSERVE_RESOLVED",
    "hold_review_tasks": "HOLD_REVIEW_RESOLVED",
    "candidate_next_tasks": "CANDIDATE_NEXT_READY_NONFINAL",
}

WAIT_STATUS_BY_QUEUE = {
    "quarantine_tasks": "QUARANTINE_REVIEW_WAITING",
    "boundary_recheck_tasks": "BOUNDARY_RECHECK_WAITING",
    "lineage_recheck_tasks": "LINEAGE_RECHECK_WAITING",
    "delivery_recheck_tasks": "DELIVERY_RECHECK_WAITING",
    "reobserve_tasks": "REOBSERVE_WAITING",
    "hold_review_tasks": "HOLD_REVIEW_WAITING",
    "candidate_next_tasks": "CANDIDATE_NEXT_WAITING",
}


@dataclass(frozen=True)
class KuuOSTaskBoardProcessResult:
    processor_status: str
    selected_task_queue: str | None
    selected_task_hash: str | None
    task_result_receipt: dict[str, Any] | None
    updated_review_state: dict[str, Any]
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def empty_review_state() -> dict[str, Any]:
    return {
        "version": "task_review_state_v0_1",
        "processed_task_hashes": [],
        "task_result_receipts": [],
        "review_log": [],
        **NON_AUTHORITY_FLAGS,
    }


def _normalize_review_state(review_state: Mapping[str, Any] | None) -> dict[str, Any]:
    if review_state is None:
        return empty_review_state()
    state = deepcopy(dict(review_state))
    state.setdefault("version", "task_review_state_v0_1")
    state.setdefault("processed_task_hashes", [])
    state.setdefault("task_result_receipts", [])
    state.setdefault("review_log", [])
    for key, value in NON_AUTHORITY_FLAGS.items():
        state[key] = value
    return state


def _truthy(state: Mapping[str, Any], key: str) -> bool:
    value = state.get(key, False)
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "present", "ok", "pass"}
    return bool(value)


def _canonical_hash(payload: Mapping[str, Any]) -> str:
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _task_hash(task_packet: Mapping[str, Any]) -> str:
    if task_packet.get("task_hash"):
        return str(task_packet["task_hash"])
    return _canonical_hash(task_packet)


def _iter_tasks(task_board: Mapping[str, Any]):
    queues = task_board.get("task_queues", {})
    for queue_name in TASK_PRIORITY:
        entries = queues.get(queue_name, [])
        for index, task in enumerate(entries):
            if isinstance(task, Mapping):
                yield queue_name, index, task


def _evaluate_task(queue_name: str, task: Mapping[str, Any], evidence: Mapping[str, Any]) -> tuple[str, list[str], list[str]]:
    required = REQUIRED_EVIDENCE_BY_QUEUE.get(queue_name, [])
    missing = [field for field in required if not _truthy(evidence, field)]
    if queue_name == "quarantine_tasks":
        # Quarantine tasks do not auto-release. Evidence only confirms review.
        if missing:
            return WAIT_STATUS_BY_QUEUE[queue_name], missing, ["quarantine_notice", "boundary_recheck_request"]
        return SUCCESS_STATUS_BY_QUEUE[queue_name], [], ["quarantine_review_receipt", "boundary_recheck_request"]
    if missing:
        return WAIT_STATUS_BY_QUEUE.get(queue_name, "TASK_WAITING"), missing, ["task_waiting_notice"]
    return SUCCESS_STATUS_BY_QUEUE.get(queue_name, "TASK_REVIEWED_NONFINAL"), [], ["task_result_receipt"]


def process_next_task(task_board: Mapping[str, Any], evidence: Mapping[str, Any], review_state: Mapping[str, Any] | None = None) -> KuuOSTaskBoardProcessResult:
    state = _normalize_review_state(review_state)
    processed = set(str(item) for item in state.get("processed_task_hashes", []))
    reviewed_at = datetime.now(timezone.utc).isoformat()

    for queue_name, index, task in _iter_tasks(task_board):
        task_hash = _task_hash(task)
        if task_hash in processed:
            continue
        task_status, missing, opened = _evaluate_task(queue_name, task, evidence)
        receipt_payload = {
            "packet_version": "task_result_receipt_v0_1",
            "task_hash": task_hash,
            "source_task_queue": queue_name,
            "task_queue_index": index,
            "task_type": task.get("task_type"),
            "cycle_id": task.get("cycle_id"),
            "source_receipt_hash": task.get("source_receipt_hash"),
            "source_action_hash": task.get("source_action_hash"),
            "qi_signal": task.get("qi_signal"),
            "qi_reason": task.get("qi_reason"),
            "task_status": task_status,
            "missing_evidence": missing,
            "opened_notices": opened,
            "reviewed_at_utc": reviewed_at,
            "allowed_projection": ["task_result_receipt", "review_log_entry"],
            **NON_AUTHORITY_FLAGS,
        }
        receipt_hash = _canonical_hash(receipt_payload)
        receipt = {"receipt_hash": receipt_hash, **receipt_payload}
        state["processed_task_hashes"].append(task_hash)
        state["task_result_receipts"].append(receipt)
        state["review_log"].append({
            "reviewed_at_utc": reviewed_at,
            "task_hash": task_hash,
            "task_result_receipt_hash": receipt_hash,
            "source_task_queue": queue_name,
            "task_status": task_status,
            **NON_AUTHORITY_FLAGS,
        })
        return KuuOSTaskBoardProcessResult(
            processor_status="PROCESSED_ONE_TASK_APPEND_ONLY",
            selected_task_queue=queue_name,
            selected_task_hash=task_hash,
            task_result_receipt=receipt,
            updated_review_state=state,
        )

    return KuuOSTaskBoardProcessResult(
        processor_status="NO_UNPROCESSED_TASK_PACKET",
        selected_task_queue=None,
        selected_task_hash=None,
        task_result_receipt=None,
        updated_review_state=state,
    )


def main(argv: list[str]) -> int:
    if len(argv) not in {3, 4}:
        print("usage: kuuos_task_board_processor_v0_1.py TASK_BOARD.json EVIDENCE.json [REVIEW_STATE.json]", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as f:
        task_board = json.load(f)
    with open(argv[2], "r", encoding="utf-8") as f:
        evidence = json.load(f)
    review_state = None
    if len(argv) == 4:
        with open(argv[3], "r", encoding="utf-8") as f:
            review_state = json.load(f)
    result = process_next_task(task_board, evidence, review_state)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
