#!/usr/bin/env python3
"""KuuOS Closed Loop Driver v0.1.

Runs a bounded, non-authoritative multi-step KuuOS loop.

The driver repeatedly calls run_closed_loop_step and returns a bounded trace.
It is deliberately not an unbounded autonomous agent: max_steps is required,
stop reasons are explicit, and all outputs remain non-authoritative.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, asdict
import json
import sys
from typing import Any, Mapping, Sequence

try:
    from runtime.kuuos_closed_loop_v0_1 import empty_loop_state_bundle, run_closed_loop_step
except ModuleNotFoundError:  # direct script execution from runtime/
    from kuuos_closed_loop_v0_1 import empty_loop_state_bundle, run_closed_loop_step


NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

DEFAULT_MAX_STEPS = 3
MAX_HARD_LIMIT = 25


@dataclass(frozen=True)
class KuuOSClosedLoopDriverResult:
    driver_status: str
    stop_reason: str
    steps_run: int
    final_raw_state: dict[str, Any]
    final_state_bundle: dict[str, Any]
    step_trace: list[dict[str, Any]]
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False
    grants_clinical_authority: bool = False
    grants_theorem_authority: bool = False
    grants_completed_identity_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _normalize_max_steps(max_steps: int | None) -> int:
    if max_steps is None:
        return DEFAULT_MAX_STEPS
    if max_steps < 1:
        return 1
    return min(max_steps, MAX_HARD_LIMIT)


def _evidence_for_step(evidence_sequence: Sequence[Mapping[str, Any]] | Mapping[str, Any], step_index: int) -> Mapping[str, Any]:
    if isinstance(evidence_sequence, Mapping):
        return evidence_sequence
    if not evidence_sequence:
        return {}
    if step_index < len(evidence_sequence):
        return evidence_sequence[step_index]
    return evidence_sequence[-1]


def _stop_reason_from_step(step_result: Mapping[str, Any]) -> str | None:
    next_state = step_result.get("next_raw_state") or {}
    feedback_merge = step_result.get("feedback_merge") or {}
    task_processor = step_result.get("task_processor") or {}
    task_receipt = task_processor.get("task_result_receipt") or {}

    if next_state.get("quarantine_retained"):
        return "QUARANTINE_RETAINED"
    if next_state.get("feedback_waiting"):
        return "WAITING_FOR_MORE_EVIDENCE"
    if feedback_merge.get("merge_status") == "MERGED_UNKNOWN_HELD_APPEND_ONLY":
        return "UNKNOWN_RESULT_HELD"
    if task_receipt.get("task_status") == "CANDIDATE_NEXT_READY_NONFINAL":
        # Continue is allowed, but still non-final. Caller may stop at max_steps.
        return None
    return None


def run_closed_loop_driver(
    initial_raw_state: Mapping[str, Any],
    evidence_sequence: Sequence[Mapping[str, Any]] | Mapping[str, Any],
    *,
    max_steps: int | None = None,
    state_bundle: Mapping[str, Any] | None = None,
) -> KuuOSClosedLoopDriverResult:
    bounded_steps = _normalize_max_steps(max_steps)
    current_raw = deepcopy(dict(initial_raw_state))
    bundle = deepcopy(dict(state_bundle)) if state_bundle is not None else empty_loop_state_bundle()
    step_trace: list[dict[str, Any]] = []
    stop_reason = "MAX_STEPS_REACHED"

    for step_index in range(bounded_steps):
        evidence = _evidence_for_step(evidence_sequence, step_index)
        step = run_closed_loop_step(current_raw, evidence, bundle)
        step_dict = step.to_dict()
        step_summary = {
            "step_index": step_index,
            "raw_cycle_id": step.raw_cycle_id,
            "next_cycle_id": step.next_cycle_id,
            "loop_status": step.loop_status,
            "queue_target": step.queue_dispatch.get("target_queue"),
            "task_queue": step.action_router.get("target_task_queue"),
            "task_status": (step.task_processor.get("task_result_receipt") or {}).get("task_status"),
            "feedback_merge_status": (step.feedback_merge or {}).get("merge_status"),
            **NON_AUTHORITY_FLAGS,
        }
        step_trace.append(step_summary)
        bundle = step.updated_state_bundle
        if step.next_raw_state is not None:
            current_raw = step.next_raw_state
        reason = _stop_reason_from_step(step_dict)
        if reason is not None:
            stop_reason = reason
            break
    else:
        stop_reason = "MAX_STEPS_REACHED"

    driver_status = "DRIVER_STOPPED_APPEND_ONLY"
    if stop_reason == "MAX_STEPS_REACHED":
        driver_status = "DRIVER_MAX_STEPS_REACHED_APPEND_ONLY"
    elif stop_reason == "WAITING_FOR_MORE_EVIDENCE":
        driver_status = "DRIVER_WAITING_APPEND_ONLY"
    elif stop_reason == "QUARANTINE_RETAINED":
        driver_status = "DRIVER_QUARANTINE_RETAINED_APPEND_ONLY"

    return KuuOSClosedLoopDriverResult(
        driver_status=driver_status,
        stop_reason=stop_reason,
        steps_run=len(step_trace),
        final_raw_state=current_raw,
        final_state_bundle=bundle,
        step_trace=step_trace,
    )


def main(argv: list[str]) -> int:
    if len(argv) not in {3, 4, 5}:
        print("usage: kuuos_closed_loop_driver_v0_1.py RAW_STATE.json EVIDENCE_OR_SEQUENCE.json [MAX_STEPS] [STATE_BUNDLE.json]", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as f:
        raw_state = json.load(f)
    with open(argv[2], "r", encoding="utf-8") as f:
        evidence = json.load(f)
    max_steps = int(argv[3]) if len(argv) >= 4 else DEFAULT_MAX_STEPS
    state_bundle = None
    if len(argv) == 5:
        with open(argv[4], "r", encoding="utf-8") as f:
            state_bundle = json.load(f)
    result = run_closed_loop_driver(raw_state, evidence, max_steps=max_steps, state_bundle=state_bundle)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
