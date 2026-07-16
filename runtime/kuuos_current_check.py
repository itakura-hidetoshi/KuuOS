#!/usr/bin/env python3
from __future__ import annotations

import runtime.kuuos_current_check_v0_95 as _base

_base.CURRENT_MEMORYOS_FRONTIER = "MemoryOS v0.97"
_base.CURRENT_FRONTIER_ARTIFACT = (
    "runtime/kuuos_memoryos_finite_family_signature_lattice_certificate_kernel_v0_1.py"
)
_NEW_STEPS = (
    (
        "memoryos-v0-96-pointed-choice-free-signature-lattice",
        "scripts/check_planos_memoryos_pointed_choice_free_signature_lattice_certificate_kernel_v0_1.py",
    ),
    (
        "memoryos-v0-97-finite-family-signature-lattice",
        "scripts/check_planos_memoryos_finite_family_signature_lattice_certificate_kernel_v0_1.py",
    ),
)
for _step in _NEW_STEPS:
    if _step not in _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS:
        _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS = (
            _base.MEMORYOS_ACTIVE_FRONTIER_TARGETS + (_step,)
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
