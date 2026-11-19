"""MemoryOS v0.35 original blocker/context/retrieval → Lean data conditions.

Uses the original MemoryOS snapshot and retrieval native validators and
rebuilds the same read-only retrieval from the *source snapshot*.
The nested Qi/non-Markov/WORLD Lean proof structures are not synthesized;
even PASS means only selected source-bound condition data, no blocker
release, no WORLD mutation, no durable append and no authority.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from typing import Any

from runtime.kuuos_lean_python_memory_world_native_v0_31 import (
    BLOCKED, NO_DATA, PASS, NativeMemoryWorldAudit, SourceException,
    packet, orig_digest, check_bool, match, success, missing, rejected,
)
from runtime.kuuos_memoryos_qi_world_blocker_integration_v0_35 import (
    validate_memoryos_qi_world_blocker_snapshot,
    validate_memoryos_conditioned_retrieval,
    build_memoryos_conditioned_retrieval,
)
from runtime.kuuos_lean_python_memory_obligations_v0_27 import (
    audit_witness as lean_data_check,
)

OS_NAME = "MemoryOS"
FORMAL_SOURCE = "formal/KUOS/OpenHorizon/MemoryOSQiWorldBlockerIntegrationKernelV0_35.lean"


def audit_native_memory_blocker(
    original_snapshot: Any,
    original_retrieval: Any,
) -> NativeMemoryWorldAudit:
    """Source-associated original kernel local invariants; no host operation."""
    try:
        snapshot = packet(original_snapshot, "MemoryOS.snapshot")
        retrieval = packet(original_retrieval, "MemoryOS.retrieval")
        source_digest = orig_digest([snapshot, retrieval])
        old = validate_memoryos_qi_world_blocker_snapshot(snapshot)
        new = validate_memoryos_conditioned_retrieval(retrieval)
        if old or new:
            raise SourceException(
                "MemoryOS:original_native_validator_rejected:"
                + ";".join(str(x) for x in (*old, *new))[:350])
        match(retrieval.get("source_memory_snapshot_digest"),
              snapshot.get("memory_snapshot_digest"),
              "MemoryOS:snapshot_retrieval_digest")
        # Validate the exact original source-derived retrieval route and
        # blocked capability evidence. This pure function cannot execute.
        replay = build_memoryos_conditioned_retrieval(
            snapshot=snapshot,
            requested_capabilities=retrieval["requested_capabilities"],
            query_id=retrieval["query_id"],
            created_at_ms=retrieval["created_at_ms"],
        )
        match(replay, retrieval, "MemoryOS:original_retrieval_replay")
        blocker = packet(snapshot.get("blocker_context"),
                         "MemoryOS.blocker_context")
        qi = packet(snapshot.get("qi_context"), "MemoryOS.qi_context")
        world = packet(snapshot.get("world_context"), "MemoryOS.world_context")
        append = packet(snapshot.get("append_candidate"), "MemoryOS.append_candidate")
        check_bool(qi, "process_history_preserved", True, "MemoryOS.qi")
        check_bool(qi, "snapshot_replacement_used", False, "MemoryOS.qi")
        check_bool(append, "append_only_required", True, "MemoryOS.append")
        check_bool(append, "memory_overwrite_performed", False, "MemoryOS.append")
        check_bool(retrieval, "candidate_context_only", True, "MemoryOS.retrieval")
        for name in ("automatic_plan_mutation", "automatic_blocker_discharge",
                     "automatic_world_commit", "automatic_execution", "truth_claim"):
            check_bool(retrieval, name, False, "MemoryOS.retrieval")
        if snapshot["memory_route"] != "PRESERVE_BLOCKED_CONTEXT":
            if snapshot["memory_route"] == "QUARANTINE_INCOMPLETE_BLOCKER_EVIDENCE":
                return NativeMemoryWorldAudit(
                    os_name=OS_NAME, status=NO_DATA,
                    issues=("MemoryOS:original_blocker_evidence_incomplete",),
                    original_source_digest=source_digest,
                    local_native_validator_passed=True,
                )
            raise SourceException("MemoryOS:unrecognized_memory_route")
        complete = blocker.get("all_required_blockers_active")
        active = blocker.get("active_blockers")
        if complete is not True or type(active) is not list or not active:
            raise SourceException("MemoryOS:source_blocker_not_active", NO_DATA)
        # Corresponds only to the SEVEN *flat* Bool conditions in the
        # v0.35 Lean composite theorem; not its nested proof structures.
        projection = {
            "blockerStoredAsContext": True,
            "blockerReleasedByMemory": bool(
                blocker.get("memory_may_discharge_blocker")
                or retrieval.get("automatic_blocker_discharge")),
            "missingEvidenceSilentlyRepaired": bool(
                blocker.get("memory_may_silently_repair_missing_evidence")),
            "worldProjectionReadOnly": world.get("projection_only"),
            "worldChangedByMemory": bool(
                world.get("memory_may_commit_world")
                or world.get("memory_may_rewrite_world")
                or append.get("world_update_performed")
                or retrieval.get("automatic_world_commit")),
            "retrievalCandidateOnly": retrieval.get("candidate_context_only"),
            "durableAppendClaimed": append.get(
                "durable_persistence_performed_by_this_kernel"),
        }
        verdict = lean_data_check(projection)
        if verdict.status != "LOCAL_CONDITIONS_CHECKED":
            raise SourceException("MemoryOS:selected_Lean_flat_conditions_not_met")
        if orig_digest([snapshot, retrieval]) != source_digest:
            raise SourceException("MemoryOS:original_source_mutated")
        return success(OS_NAME, [snapshot, retrieval], (
            "MemoryOS.snapshot.memory_snapshot_digest",
            "MemoryOS.snapshot.memory_route",
            "MemoryOS.snapshot.qi_context.process_history_preserved",
            "MemoryOS.snapshot.qi_context.snapshot_replacement_used",
            "MemoryOS.snapshot.blocker_context.active_blockers",
            "MemoryOS.snapshot.blocker_context.all_required_blockers_active",
            "MemoryOS.snapshot.blocker_context.memory_may_discharge_blocker",
            "MemoryOS.snapshot.blocker_context.memory_may_silently_repair_missing_evidence",
            "MemoryOS.snapshot.world_context.projection_only",
            "MemoryOS.snapshot.world_context.memory_may_commit_world",
            "MemoryOS.snapshot.append_candidate.append_only_required",
            "MemoryOS.snapshot.append_candidate.durable_persistence_performed_by_this_kernel",
            "MemoryOS.retrieval.source_memory_snapshot_digest",
            "MemoryOS.retrieval.candidate_context_only",
            "MemoryOS.retrieval.automatic_world_commit",
        ))
    except SourceException as exc:
        return NativeMemoryWorldAudit(
            os_name=OS_NAME, status=exc.status, issues=(exc.message,))
    except (TypeError, ValueError, UnicodeError, RecursionError,
            OverflowError, KeyError, AttributeError) as exc:
        return rejected(OS_NAME, "MemoryOS:source_exception:"
                        + type(exc).__name__)


__all__ = ("OS_NAME", "FORMAL_SOURCE", "audit_native_memory_blocker")
