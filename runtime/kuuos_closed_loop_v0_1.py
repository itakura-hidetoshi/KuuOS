#!/usr/bin/env python3
"""KuuOS Closed Loop Runner v0.1.

Runs one non-authoritative KuuOS loop step:

  raw Qi/OS state
    -> Queue Dispatcher
    -> Queue Worker
    -> Action Router
    -> Task Board Processor
    -> Feedback Merger
    -> next raw Qi/OS state

The runner only advances candidate state and appends receipts/logs. It never
executes actions, finalizes truth, overwrites memory, proves theorems, makes
clinical decisions, or creates completed OS identity.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, asdict
import json
import sys
from typing import Any, Mapping

try:
    from runtime.kuuos_action_router_v0_1 import route_next_action
    from runtime.kuuos_feedback_merger_v0_1 import merge_task_result_into_next_state
    from runtime.kuuos_queue_dispatcher_v0_1 import dispatch_candidate_cycle, empty_queue_state
    from runtime.kuuos_queue_worker_v0_1 import empty_worker_state, process_next_queue_item
    from runtime.kuuos_task_board_processor_v0_1 import empty_review_state, process_next_task
except ModuleNotFoundError:  # direct script execution from runtime/
    from kuuos_action_router_v0_1 import route_next_action
    from kuuos_feedback_merger_v0_1 import merge_task_result_into_next_state
    from kuuos_queue_dispatcher_v0_1 import dispatch_candidate_cycle, empty_queue_state
    from kuuos_queue_worker_v0_1 import empty_worker_state, process_next_queue_item
    from kuuos_task_board_processor_v0_1 import empty_review_state, process_next_task


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
class KuuOSClosedLoopResult:
    loop_status: str
    raw_cycle_id: str
    next_cycle_id: str | None
    queue_dispatch: dict[str, Any]
    queue_worker: dict[str, Any]
    action_router: dict[str, Any]
    task_processor: dict[str, Any]
    feedback_merge: dict[str, Any] | None
    next_raw_state: dict[str, Any] | None
    updated_state_bundle: dict[str, Any]
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def empty_loop_state_bundle() -> dict[str, Any]:
    return {
        "version": "closed_loop_state_bundle_v0_1",
        "queue_state": empty_queue_state(),
        "worker_state": empty_worker_state(),
        "task_board": None,
        "review_state": empty_review_state(),
        "loop_log": [],
        **NON_AUTHORITY_FLAGS,
    }


def _normalize_state_bundle(state_bundle: Mapping[str, Any] | None) -> dict[str, Any]:
    if state_bundle is None:
        return empty_loop_state_bundle()
    bundle = deepcopy(dict(state_bundle))
    base = empty_loop_state_bundle()
    bundle.setdefault("version", "closed_loop_state_bundle_v0_1")
    bundle.setdefault("queue_state", base["queue_state"])
    bundle.setdefault("worker_state", base["worker_state"])
    bundle.setdefault("task_board", base["task_board"])
    bundle.setdefault("review_state", base["review_state"])
    bundle.setdefault("loop_log", [])
    for key, value in NON_AUTHORITY_FLAGS.items():
        bundle[key] = value
    return bundle


def run_closed_loop_step(raw_state: Mapping[str, Any], evidence: Mapping[str, Any], state_bundle: Mapping[str, Any] | None = None) -> KuuOSClosedLoopResult:
    bundle = _normalize_state_bundle(state_bundle)

    dispatch = dispatch_candidate_cycle(raw_state, bundle.get("queue_state"))
    bundle["queue_state"] = dispatch.updated_queue_state

    worker = process_next_queue_item(bundle["queue_state"], bundle.get("worker_state"))
    bundle["worker_state"] = worker.updated_worker_state

    router = route_next_action(bundle["worker_state"], bundle.get("task_board"))
    bundle["task_board"] = router.updated_task_board

    processor = process_next_task(bundle["task_board"], evidence, bundle.get("review_state"))
    bundle["review_state"] = processor.updated_review_state

    feedback_result = None
    next_raw_state = None
    if processor.task_result_receipt is not None:
        feedback = merge_task_result_into_next_state(raw_state, processor.task_result_receipt)
        feedback_result = feedback.to_dict()
        next_raw_state = feedback.next_raw_state
        loop_status = "LOOP_STEP_COMPLETED_APPEND_ONLY"
        next_cycle_id = str(next_raw_state.get("cycle_id")) if next_raw_state else None
    else:
        loop_status = "LOOP_STEP_WAITING_NO_TASK_RESULT"
        next_cycle_id = None

    loop_log_entry = {
        "raw_cycle_id": raw_state.get("cycle_id"),
        "next_cycle_id": next_cycle_id,
        "dispatch_status": dispatch.dispatch_status,
        "worker_status": worker.worker_status,
        "router_status": router.router_status,
        "processor_status": processor.processor_status,
        "loop_status": loop_status,
        "queue_target": dispatch.target_queue,
        "task_queue": router.target_task_queue,
        "task_result_status": processor.task_result_receipt.get("task_status") if processor.task_result_receipt else None,
        **NON_AUTHORITY_FLAGS,
    }
    bundle["loop_log"].append(loop_log_entry)

    return KuuOSClosedLoopResult(
        loop_status=loop_status,
        raw_cycle_id=str(raw_state.get("cycle_id", "unknown-cycle")),
        next_cycle_id=next_cycle_id,
        queue_dispatch=dispatch.to_dict(),
        queue_worker=worker.to_dict(),
        action_router=router.to_dict(),
        task_processor=processor.to_dict(),
        feedback_merge=feedback_result,
        next_raw_state=next_raw_state,
        updated_state_bundle=bundle,
    )


def main(argv: list[str]) -> int:
    if len(argv) not in {3, 4}:
        print("usage: kuuos_closed_loop_v0_1.py RAW_STATE.json EVIDENCE.json [STATE_BUNDLE.json]", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as f:
        raw_state = json.load(f)
    with open(argv[2], "r", encoding="utf-8") as f:
        evidence = json.load(f)
    state_bundle = None
    if len(argv) == 4:
        with open(argv[3], "r", encoding="utf-8") as f:
            state_bundle = json.load(f)
    result = run_closed_loop_step(raw_state, evidence, state_bundle)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
