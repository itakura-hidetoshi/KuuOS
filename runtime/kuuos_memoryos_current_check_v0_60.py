#!/usr/bin/env python3
from __future__ import annotations

import json

from runtime.kuuos_current_check import (
    CURRENT_MEMORYOS_FRONTIER as SOURCE_MEMORYOS_FRONTIER,
    MEMORYOS_ACTIVE_FRONTIER_STEPS as SOURCE_MEMORYOS_ACTIVE_FRONTIER_STEPS,
    _run_step,
)
from runtime.kuuos_current_root_sequence_v0_41 import CurrentRootStep

CURRENT_MEMORYOS_FRONTIER = "MemoryOS v0.60"
CURRENT_FRONTIER_ARTIFACT = (
    "runtime/kuuos_memoryos_modified_log_sobolev_hellinger_"
    "separation_certificate_kernel_v0_1.py"
)
V0_60_STEP = CurrentRootStep(
    "memoryos-v0-60-modified-log-sobolev-hellinger-separation",
    "script",
    "scripts/check_planos_memoryos_modified_log_sobolev_hellinger_separation_certificate_kernel_v0_1.py",
    True,
    "Validate modified logarithmic entropy decay, symbolic Hellinger envelopes, exact separation profiles, transport commutation, and singular boundaries.",
)
MEMORYOS_ACTIVE_FRONTIER_STEPS = SOURCE_MEMORYOS_ACTIVE_FRONTIER_STEPS + (V0_60_STEP,)


def summary() -> dict[str, object]:
    return {
        "source_memoryos_frontier": SOURCE_MEMORYOS_FRONTIER,
        "memoryos_frontier": CURRENT_MEMORYOS_FRONTIER,
        "memoryos_step_count": len(MEMORYOS_ACTIVE_FRONTIER_STEPS),
        "frontier_artifact": CURRENT_FRONTIER_ARTIFACT,
        "current_root_extension": "runtime/kuuos_memoryos_current_check_v0_60.py",
    }


def run_current() -> int:
    failures: list[str] = []
    total = len(MEMORYOS_ACTIVE_FRONTIER_STEPS)
    for ordinal, step in enumerate(MEMORYOS_ACTIVE_FRONTIER_STEPS, start=1):
        print(f"\n[{ordinal}/{total}] {step.step_id}", flush=True)
        try:
            status = _run_step(step.runner, step.target)
        except Exception as exc:
            status = 1
            print(f"current_root_exception:{step.step_id}:{type(exc).__name__}:{exc}")
        if status == 0:
            print(f"PASS: {step.step_id}", flush=True)
        elif step.required:
            failures.append(step.step_id)
    if failures:
        print("MEMORYOS v0.60 ROOT FAILED")
        for step_id in failures:
            print(f"- {step_id}")
        return 1
    print(f"PASS: {CURRENT_MEMORYOS_FRONTIER} cumulative root ({total} steps)")
    return 0


if __name__ == "__main__":
    print(json.dumps(summary(), ensure_ascii=False, sort_keys=True))
    raise SystemExit(run_current())
