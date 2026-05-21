#!/usr/bin/env python3
"""Qi Cycle Runner v0.1.

Connects the executable Qi runtime evaluator to an OS candidate cycle.
The runner reads a candidate-cycle state, asks Qi for a bounded signal, and
returns a next-stage decision for the surrounding KuuOS runtime.

This is still candidate-only.  ALLOW_CANDIDATE only means "continue to the
next non-final stage"; it never means execution, truth, final commitment,
clinical authority, memory overwrite, theorem proof, or completed identity.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
import sys
from typing import Any, Mapping

try:
    from runtime.qi_runtime_binding_v0_1 import QiSignal, evaluate_qi_runtime_binding
except ModuleNotFoundError:  # direct script execution from runtime/
    from qi_runtime_binding_v0_1 import QiSignal, evaluate_qi_runtime_binding


NEXT_STAGE_BY_SIGNAL = {
    QiSignal.ALLOW_CANDIDATE.value: "NEXT_NONFINAL_STAGE",
    QiSignal.HOLD.value: "HOLD_QUEUE",
    QiSignal.REOBSERVE.value: "REOBSERVE_QUEUE",
    QiSignal.LINEAGE_RECHECK.value: "LINEAGE_RECHECK_QUEUE",
    QiSignal.DELIVERY_RECHECK.value: "DELIVERY_RECHECK_QUEUE",
    QiSignal.BOUNDARY_RECHECK.value: "BOUNDARY_RECHECK_QUEUE",
    QiSignal.QUARANTINE.value: "QUARANTINE_QUEUE",
}

TERMINAL_FOR_CYCLE = {
    QiSignal.ALLOW_CANDIDATE.value: False,
    QiSignal.HOLD.value: True,
    QiSignal.REOBSERVE.value: True,
    QiSignal.LINEAGE_RECHECK.value: True,
    QiSignal.DELIVERY_RECHECK.value: True,
    QiSignal.BOUNDARY_RECHECK.value: True,
    QiSignal.QUARANTINE.value: True,
}


@dataclass(frozen=True)
class QiCycleDecision:
    cycle_id: str
    kernel_state: str
    qi_signal: str
    qi_reason: str
    next_stage: str
    terminal_for_cycle: bool
    opened_notices: list[str]
    missing_inputs: list[str]
    blocked_boundaries: list[str]
    allowed_projection: list[str]
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_qi_cycle(state: Mapping[str, Any]) -> QiCycleDecision:
    receipt = evaluate_qi_runtime_binding(state)
    signal = receipt.qi_signal
    return QiCycleDecision(
        cycle_id=receipt.cycle_id,
        kernel_state=receipt.kernel_state,
        qi_signal=signal,
        qi_reason=receipt.qi_reason,
        next_stage=NEXT_STAGE_BY_SIGNAL.get(signal, "HOLD_QUEUE"),
        terminal_for_cycle=TERMINAL_FOR_CYCLE.get(signal, True),
        opened_notices=receipt.opened_notices,
        missing_inputs=receipt.missing_inputs,
        blocked_boundaries=receipt.blocked_boundaries,
        allowed_projection=receipt.allowed_projection,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: qi_cycle_runner_v0_1.py STATE.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as f:
        state = json.load(f)
    decision = run_qi_cycle(state)
    print(json.dumps(decision.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if decision.qi_signal != QiSignal.QUARANTINE.value else 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
