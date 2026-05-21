#!/usr/bin/env python3
"""KuuOS Queue Worker v0.1.

Processes append-only queue state produced by the KuuOS Queue Dispatcher.
The worker does not remove queue entries and does not execute actions.  It marks
receipt hashes as processed and appends non-authoritative action packets to an
outbox.

Priority is safety-first:
  QUARANTINE -> BOUNDARY_RECHECK -> LINEAGE_RECHECK -> DELIVERY_RECHECK
  -> REOBSERVE -> HOLD -> NEXT_NONFINAL_STAGE
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
import sys
from typing import Any, Mapping


QUEUE_PRIORITY = [
    "QUARANTINE_QUEUE",
    "BOUNDARY_RECHECK_QUEUE",
    "LINEAGE_RECHECK_QUEUE",
    "DELIVERY_RECHECK_QUEUE",
    "REOBSERVE_QUEUE",
    "HOLD_QUEUE",
    "NEXT_NONFINAL_STAGE",
]

ACTION_BY_QUEUE = {
    "QUARANTINE_QUEUE": "open_quarantine_review_packet",
    "BOUNDARY_RECHECK_QUEUE": "open_boundary_recheck_packet",
    "LINEAGE_RECHECK_QUEUE": "open_lineage_recheck_packet",
    "DELIVERY_RECHECK_QUEUE": "open_delivery_recheck_packet",
    "REOBSERVE_QUEUE": "open_reobserve_packet",
    "HOLD_QUEUE": "open_hold_review_packet",
    "NEXT_NONFINAL_STAGE": "open_next_nonfinal_candidate_packet",
}

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}


@dataclass(frozen=True)
class KuuOSQueueWorkerResult:
    worker_status: str
    selected_queue: str | None
    selected_receipt_hash: str | None
    action_packet: dict[str, Any] | None
    updated_worker_state: dict[str, Any]
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def empty_worker_state() -> dict[str, Any]:
    return {
        "version": "queue_worker_state_v0_1",
        "processed_receipt_hashes": [],
        "worker_log": [],
        "action_outbox": [],
        **NON_AUTHORITY_FLAGS,
    }


def _normalize_worker_state(worker_state: Mapping[str, Any] | None) -> dict[str, Any]:
    if worker_state is None:
        return empty_worker_state()
    state = deepcopy(dict(worker_state))
    state.setdefault("version", "queue_worker_state_v0_1")
    state.setdefault("processed_receipt_hashes", [])
    state.setdefault("worker_log", [])
    state.setdefault("action_outbox", [])
    for key, value in NON_AUTHORITY_FLAGS.items():
        state[key] = value
    return state


def _iter_queue_entries(queue_state: Mapping[str, Any]):
    queues = queue_state.get("queues", {})
    for queue_name in QUEUE_PRIORITY:
        entries = queues.get(queue_name, [])
        for index, entry in enumerate(entries):
            if isinstance(entry, Mapping):
                yield queue_name, index, entry


def _make_action_packet(queue_name: str, entry: Mapping[str, Any], processed_at: str) -> dict[str, Any]:
    receipt_hash = str(entry.get("receipt_hash", ""))
    return {
        "packet_version": "queue_action_packet_v0_1",
        "action_type": ACTION_BY_QUEUE.get(queue_name, "open_hold_review_packet"),
        "source_queue": queue_name,
        "cycle_id": entry.get("cycle_id"),
        "receipt_hash": receipt_hash,
        "previous_receipt_hash": entry.get("previous_receipt_hash"),
        "qi_signal": entry.get("qi_signal"),
        "qi_reason": entry.get("qi_reason"),
        "required_next_action": entry.get("required_next_action"),
        "opened_notices": list(entry.get("opened_notices", [])),
        "blocked_boundaries": list(entry.get("blocked_boundaries", [])),
        "missing_inputs": list(entry.get("missing_inputs", [])),
        "processed_at_utc": processed_at,
        "allowed_projection": ["queue_action_packet", "worker_log_entry"],
        **NON_AUTHORITY_FLAGS,
    }


def process_next_queue_item(queue_state: Mapping[str, Any], worker_state: Mapping[str, Any] | None = None) -> KuuOSQueueWorkerResult:
    state = _normalize_worker_state(worker_state)
    processed = set(str(item) for item in state.get("processed_receipt_hashes", []))
    processed_at = datetime.now(timezone.utc).isoformat()

    for queue_name, index, entry in _iter_queue_entries(queue_state):
        receipt_hash = str(entry.get("receipt_hash", ""))
        if not receipt_hash or receipt_hash in processed:
            continue
        packet = _make_action_packet(queue_name, entry, processed_at)
        state["processed_receipt_hashes"].append(receipt_hash)
        log_entry = {
            "processed_at_utc": processed_at,
            "source_queue": queue_name,
            "queue_index": index,
            "receipt_hash": receipt_hash,
            "action_type": packet["action_type"],
            **NON_AUTHORITY_FLAGS,
        }
        state["worker_log"].append(log_entry)
        state["action_outbox"].append(packet)
        return KuuOSQueueWorkerResult(
            worker_status="PROCESSED_ONE_APPEND_ONLY",
            selected_queue=queue_name,
            selected_receipt_hash=receipt_hash,
            action_packet=packet,
            updated_worker_state=state,
        )

    return KuuOSQueueWorkerResult(
        worker_status="NO_UNPROCESSED_QUEUE_ITEM",
        selected_queue=None,
        selected_receipt_hash=None,
        action_packet=None,
        updated_worker_state=state,
    )


def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        print("usage: kuuos_queue_worker_v0_1.py QUEUE_STATE.json [WORKER_STATE.json]", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as f:
        queue_state = json.load(f)
    worker_state = None
    if len(argv) == 3:
        with open(argv[2], "r", encoding="utf-8") as f:
            worker_state = json.load(f)
    result = process_next_queue_item(queue_state, worker_state)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
