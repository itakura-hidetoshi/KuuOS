"""MemoryOS: selected Lean theorem data obligations, v0.27.

The source Lean structure contains proof fields not constructible by a
Python boolean packet. A LOCAL result checks supplied data conditions only,
not Lean-to-Python refinement, original-state authenticity or authority.
Original OS kernel is unmodified. Copyright Hidetoshi Itakura / 板倉英俊.
"""
from __future__ import annotations

from typing import Any
from runtime.kuuos_lean_python_per_os_contracts_v0_27 import (
    Verifier, original_state_audit,
)

OS_NAME = "MemoryOS"
LEAN_FILE = "formal/KUOS/OpenHorizon/MemoryOSQiWorldBlockerIntegrationKernelV0_35.lean"
THEOREMS = ["memory_cannot_discharge_blocker","memoryos_qi_world_blocker_integration_boundary"]
FIELDS = ["blockerStoredAsContext","blockerReleasedByMemory","missingEvidenceSilentlyRepaired","worldProjectionReadOnly","worldChangedByMemory","retrievalCandidateOnly","durableAppendClaimed"]


def audit_witness(witness: Any):
    """Check selected source-named Lean obligations on observed data only."""
    v = Verifier(witness, fields=FIELDS)
    for key in ("blockerStoredAsContext", "worldProjectionReadOnly",
                "retrievalCandidateOnly"):
        v.flag(key, True)
    for key in ("blockerReleasedByMemory", "missingEvidenceSilentlyRepaired",
                "worldChangedByMemory", "durableAppendClaimed"):
        v.flag(key, False)
    return v.finish(OS_NAME, LEAN_FILE, THEOREMS)


def audit_native_state(state: Any):
    """Use the existing runtime OS registry and original source validators."""
    return original_state_audit(OS_NAME, state)

