#!/usr/bin/env python3
from __future__ import annotations

import runtime.kuuos_current_check_v0_94 as _base

_base.CURRENT_MEMORYOS_FRONTIER = "MemoryOS v0.95"
_base.CURRENT_FRONTIER_ARTIFACT = (
    "runtime/kuuos_memoryos_choice_free_signature_hull_kernel_order_duality_certificate_kernel_v0_1.py"
)
_NEW_STEP = (
    "memoryos-v0-95-choice-free-signature-hull-kernel-order-duality",
    "scripts/check_planos_memoryos_choice_free_signature_hull_kernel_order_duality_certificate_kernel_v0_1.py",
)
if _NEW_STEP not in _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS:
    _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS = (
        _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS + (_NEW_STEP,)
    )
_base.MEMORYOS_ACTIVE_FRONTIER_STEPS = tuple(
    _base._script_step(step_id, target, f"Validate {step_id}.")
    for step_id, target in _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS
)
_base.CURRENT_ROOT_STEPS = (
    _base.REPOSITORY_LINEAGE_STEPS
    + _base.PLANOS_ACTIVE_FRONTIER_STEPS
    + _base.DECISIONOS_ACTIVE_FRONTIER_STEPS
    + _base.MEMORYOS_ACTIVE_FRONTIER_STEPS
)

for _name, _value in vars(_base).items():
    if not _name.startswith("__"):
        globals()[_name] = _value

if __name__ == "__main__":
    raise SystemExit(_base.main())
