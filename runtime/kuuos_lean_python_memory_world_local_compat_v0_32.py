"""KuuOS v0.32 — scoped native MemoryOS↔WORLD source compatibility.

This is NOT a proof of global descent/gluing. It checks that a native
MemoryOS snapshot, its read-only retrieval and one validated ORIGINAL
WORLD store share the *same exact* source digest, store ID, root lineage,
generation, fragment, commit pointer and history count. An optional
full original WORLD v0.34 disposition→authorization→request→persisted
receipt bundle can additionally be checked via v0.31 without invoking
any new atomic commit.

MemoryOS upstream episode/certificate provenance may still be mocked
or unauthenticated. Plain JSON copies only; no filesystem mutation,
no host authority, no universal Lean↔Python semantic refinement.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from runtime.kuuos_lean_python_memory_world_native_v0_31 import (
    PASS, BLOCKED, NO_DATA, packet, orig_digest, match, SourceException,
)
from runtime.kuuos_lean_python_memory_native_binding_v0_31 import (
    audit_native_memory_blocker,
)
from runtime.kuuos_lean_python_world_native_binding_v0_31 import (
    audit_original_world_commit,
)
from runtime.kuuos_authorized_atomic_world_commit_entry_v0_34 import (
    validate_world_store,
)

VERSION = "kuuos_lean_python_memory_world_local_compat_v0_32"
PARENT_SOURCE = "5c072a1a914b2e1c7a0083866af87398b56e879a"
SCOPED_STORE = "SCOPED_MEMORY_WORLD_STORE_COMPATIBLE"
SCOPED_COMMIT = "SCOPED_MEMORY_WORLD_COMMIT_COMPATIBLE"


@dataclass(frozen=True)
class LocalCompatibilityAudit:
    status: str
    issues: tuple[str, ...] = ()
    source_digest: str | None = None
    memory_native_validated: bool = False
    world_store_native_validated: bool = False
    same_exact_world_source_checked: bool = False
    original_world_commit_checked: bool = False
    complete_external_issuer_authenticated: bool = False
    memory_upstream_blocker_authenticated: bool = False
    formal_descent_certified: bool = False
    global_gluing_proved: bool = False
    whole_program_lean_python_refinement_proved: bool = False
    original_store_modified: bool = False
    world_commit_performed_by_auditor: bool = False
    execution_authority_granted: bool = False
    truth_authority_granted: bool = False
    root_rewrite_authority_granted: bool = False
    history_delete_authority_granted: bool = False


def _hold(status: str, reason: str) -> LocalCompatibilityAudit:
    return LocalCompatibilityAudit(status=status, issues=(reason,))


def audit_memory_world_compatibility(
    memory_snapshot: Any,
    memory_retrieval: Any,
    world_store_envelope: Any,
    *,
    source_disposition_envelope: Any = None,
    authorization_envelope: Any = None,
    request_envelope: Any = None,
    recorded_commit_receipt_envelope: Any = None,
) -> LocalCompatibilityAudit:
    """Check local native compatibility, NOT Lean descent certification."""
    if any(item is None for item in
           (memory_snapshot, memory_retrieval, world_store_envelope)):
        return _hold(NO_DATA, "source_memory_retrieval_or_world_store_missing")
    try:
        snapshot = packet(memory_snapshot, "MemoryOS.snapshot")
        retrieval = packet(memory_retrieval, "MemoryOS.retrieval")
        store = packet(world_store_envelope, "WORLD.store")
        before = orig_digest([snapshot, retrieval, store])
        memory = audit_native_memory_blocker(snapshot, retrieval)
        if memory.status != PASS:
            return _hold(memory.status, "MemoryOS:local_native_precondition:"
                         + ";".join(memory.issues))
        try:
            world = validate_world_store(store)
        except (ValueError, TypeError, KeyError, RecursionError, AttributeError):
            return _hold(BLOCKED, "WORLD:original_store_validator_failed")
        memory_projection = packet(
            snapshot.get("world_context"), "MemoryOS.world_context")
        exact_fields = (
            ("source_world_store_digest", snapshot["source_world_store_digest"],
             store["body_digest"]),
            ("world_store_id", memory_projection.get("world_store_id"),
             world["world_store_id"]),
            ("root_lineage_digest", memory_projection.get("root_lineage_digest"),
             world["root_lineage_digest"]),
            ("generation", memory_projection.get("generation"), world["generation"]),
            ("current_world_fragment_digest",
             memory_projection.get("current_world_fragment_digest"),
             world["current_world_fragment_digest"]),
            ("last_commit_digest", memory_projection.get("last_commit_digest"),
             world["last_commit_digest"]),
            ("commit_history_length", memory_projection.get("commit_history_length"),
             len(world["commits"])),
        )
        for label, observed, canonical in exact_fields:
            match(observed, canonical, "MemoryOS↔WORLD:" + label)
        if orig_digest([snapshot, retrieval, store]) != before:
            raise SourceException("source_mutated_by_local_compatibility_auditor")
        extra = (
            source_disposition_envelope, authorization_envelope,
            request_envelope, recorded_commit_receipt_envelope,
        )
        if any(x is not None for x in extra) and any(x is None for x in extra):
            return LocalCompatibilityAudit(
                status=NO_DATA,
                issues=("original_atomic_commit_provenance_incomplete",),
                source_digest=before,
                memory_native_validated=True,
                world_store_native_validated=True,
                same_exact_world_source_checked=True,
            )
        if all(x is not None for x in extra):
            committed = audit_original_world_commit(
                source_disposition_envelope, authorization_envelope,
                request_envelope, recorded_commit_receipt_envelope,
                store,
            )
            if committed.status != PASS:
                return LocalCompatibilityAudit(
                    status=committed.status,
                    issues=("WORLD:original_atomic_commit:" +
                            ";".join(committed.issues),),
                    source_digest=before,
                    memory_native_validated=True,
                    world_store_native_validated=True,
                    same_exact_world_source_checked=True,
                )
            return LocalCompatibilityAudit(
                status=SCOPED_COMMIT,
                source_digest=before,
                memory_native_validated=True,
                world_store_native_validated=True,
                same_exact_world_source_checked=True,
                original_world_commit_checked=True,
            )
        return LocalCompatibilityAudit(
            status=SCOPED_STORE,
            source_digest=before,
            memory_native_validated=True,
            world_store_native_validated=True,
            same_exact_world_source_checked=True,
            original_world_commit_checked=False,
        )
    except SourceException as exc:
        return _hold(exc.status, exc.message)
    except (ValueError, TypeError, KeyError, OverflowError,
            UnicodeError, RecursionError, AttributeError) as exc:
        return _hold(BLOCKED, "MemoryOS↔WORLD:source_exception:"
                     + type(exc).__name__)


__all__ = (
    "VERSION", "PARENT_SOURCE", "SCOPED_STORE", "SCOPED_COMMIT",
    "PASS", "BLOCKED", "NO_DATA", "LocalCompatibilityAudit",
    "audit_memory_world_compatibility",
)
