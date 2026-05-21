#!/usr/bin/env python3
"""KuuOS Queue Dispatcher v0.1.

Turns a KuuOS candidate-cycle receipt into an append-only queue-state update.

Flow:
  raw Qi/OS state
    -> Qi Total Field
    -> Qi Runtime Binding
    -> Qi Cycle Runner
    -> Candidate Cycle Receipt
    -> Queue Dispatch State

This is still non-authoritative. Dispatching a receipt to a queue is not
execution, truth, final commitment, theorem proof, clinical action, memory
overwrite, or completed OS identity.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
import sys
from typing import Any, Mapping

try:
    from runtime.kuuos_candidate_cycle_v0_1 import KuuOSCandidateCycleReceipt, run_candidate_cycle
except ModuleNotFoundError:  # direct script execution from runtime/
    from kuuos_candidate_cycle_v0_1 import KuuOSCandidateCycleReceipt, run_candidate_cycle


QUEUE_NAMES = [
    "NEXT_NONFINAL_STAGE",
    "HOLD_QUEUE",
    "REOBSERVE_QUEUE",
    "LINEAGE_RECHECK_QUEUE",
    "DELIVERY_RECHECK_QUEUE",
    "BOUNDARY_RECHECK_QUEUE",
    "QUARANTINE_QUEUE",
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


@dataclass(frozen=True)
class KuuOSQueueDispatchResult:
    cycle_id: str
    dispatch_status: str
    target_queue: str
    receipt_hash: str
    previous_receipt_hash: str | None
    queue_lengths: dict[str, int]
    dispatch_notice: str
    candidate_cycle_receipt: dict[str, Any]
    updated_queue_state: dict[str, Any]
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def empty_queue_state() -> dict[str, Any]:
    return {
        "version": "queue_state_v0_1",
        "last_receipt_hash": None,
        "queues": {name: [] for name in QUEUE_NAMES},
        "dispatch_log": [],
        **NON_AUTHORITY_FLAGS,
    }


def _normalize_queue_state(queue_state: Mapping[str, Any] | None) -> dict[str, Any]:
    if queue_state is None:
        return empty_queue_state()
    state = deepcopy(dict(queue_state))
    state.setdefault("version", "queue_state_v0_1")
    state.setdefault("last_receipt_hash", None)
    queues = state.setdefault("queues", {})
    for name in QUEUE_NAMES:
        queues.setdefault(name, [])
    state.setdefault("dispatch_log", [])
    for key, value in NON_AUTHORITY_FLAGS.items():
        state[key] = value
    return state


def dispatch_candidate_cycle(raw_state: Mapping[str, Any], queue_state: Mapping[str, Any] | None = None) -> KuuOSQueueDispatchResult:
    state = _normalize_queue_state(queue_state)
    raw = dict(raw_state)
    if not raw.get("previous_receipt_hash") and state.get("last_receipt_hash"):
        raw["previous_receipt_hash"] = state["last_receipt_hash"]

    receipt: KuuOSCandidateCycleReceipt = run_candidate_cycle(raw)
    target_queue = receipt.next_queue if receipt.next_queue in QUEUE_NAMES else "HOLD_QUEUE"
    receipt_record = {
        "cycle_id": receipt.cycle_id,
        "receipt_hash": receipt.receipt_hash,
        "previous_receipt_hash": receipt.previous_receipt_hash,
        "cycle_status": receipt.cycle_status,
        "qi_signal": receipt.qi_signal,
        "qi_reason": receipt.qi_reason,
        "required_next_action": receipt.required_next_action,
        "opened_notices": receipt.opened_notices,
        "blocked_boundaries": receipt.blocked_boundaries,
        "missing_inputs": receipt.missing_inputs,
        "qi_process_tensor_receipt": receipt.qi_process_tensor_receipt,
        **NON_AUTHORITY_FLAGS,
    }
    state["queues"][target_queue].append(receipt_record)
    state["last_receipt_hash"] = receipt.receipt_hash
    dispatch_entry = {
        "dispatched_at_utc": str(raw.get("dispatched_at_utc") or datetime.now(timezone.utc).isoformat()),
        "cycle_id": receipt.cycle_id,
        "target_queue": target_queue,
        "receipt_hash": receipt.receipt_hash,
        "previous_receipt_hash": receipt.previous_receipt_hash,
        "qi_signal": receipt.qi_signal,
        "qi_process_tensor_receipt": receipt.qi_process_tensor_receipt,
        **NON_AUTHORITY_FLAGS,
    }
    state["dispatch_log"].append(dispatch_entry)
    queue_lengths = {name: len(state["queues"].get(name, [])) for name in QUEUE_NAMES}
    return KuuOSQueueDispatchResult(
        cycle_id=receipt.cycle_id,
        dispatch_status="DISPATCHED_APPEND_ONLY",
        target_queue=target_queue,
        receipt_hash=receipt.receipt_hash,
        previous_receipt_hash=receipt.previous_receipt_hash,
        queue_lengths=queue_lengths,
        dispatch_notice="candidate_cycle_receipt_appended_to_queue_without_authority_grant",
        candidate_cycle_receipt=receipt.to_dict(),
        updated_queue_state=state,
    )


def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        print("usage: kuuos_queue_dispatcher_v0_1.py RAW_QI_STATE.json [QUEUE_STATE.json]", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as f:
        raw_state = json.load(f)
    queue_state = None
    if len(argv) == 3:
        with open(argv[2], "r", encoding="utf-8") as f:
            queue_state = json.load(f)
    result = dispatch_candidate_cycle(raw_state, queue_state)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.target_queue != "QUARANTINE_QUEUE" else 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
