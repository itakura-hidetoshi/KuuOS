"""WORLD: selected Lean theorem data obligations, v0.27.

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

OS_NAME = "WORLD"
LEAN_FILE = "formal/KUOS/OpenHorizon/AuthorizedAtomicWorldCommitKernelV0_34.lean"
THEOREMS = ["local_commit_authorization_does_not_shrink_open_horizon","atomic_world_commit_preserves_history_and_root","rollback_reference_is_not_automatic_history_deletion"]
FIELDS = ["localCommitAuthorizationFinite","localCommitAuthorizationSingleUse","openHorizonPreserved","globalCycleLimitAbsent","globalGenerationLimitAbsent","globalTimeHorizonLimitAbsent","atomicReplaceCommitted","oneAtomicStoreAndReceiptState","appendOnlyHistoryPreserved","immutableCommitReceipt","sameRootPreserved","constitutionalRootRewritten","memoryHistoryOverwritten","rollbackReferencePreserved","rollbackRequiresFreshAuthorization","rollbackDeletesHistory","automaticRollbackPerformed"]


def audit_witness(witness: Any):
    """Check selected source-named Lean obligations on observed data only."""
    v = Verifier(witness, fields=FIELDS)
    for key in ("localCommitAuthorizationFinite", "localCommitAuthorizationSingleUse",
                "openHorizonPreserved", "globalCycleLimitAbsent",
                "globalGenerationLimitAbsent", "globalTimeHorizonLimitAbsent",
                "atomicReplaceCommitted", "oneAtomicStoreAndReceiptState",
                "appendOnlyHistoryPreserved", "immutableCommitReceipt",
                "sameRootPreserved", "rollbackReferencePreserved",
                "rollbackRequiresFreshAuthorization"):
        v.flag(key, True)
    for key in ("constitutionalRootRewritten", "memoryHistoryOverwritten",
                "rollbackDeletesHistory", "automaticRollbackPerformed"):
        v.flag(key, False)
    return v.finish(OS_NAME, LEAN_FILE, THEOREMS)


def audit_native_state(state: Any):
    """Use the existing runtime OS registry and original source validators."""
    return original_state_audit(OS_NAME, state)

