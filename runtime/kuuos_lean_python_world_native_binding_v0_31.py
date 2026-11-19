"""WORLD v0.34 source-bound original atomic store/receipt → Lean data.

All five actual original input/output objects must be present:
verified candidate disposition, finite single-use authorization,
reconstructible commit request, recorded immutable receipt, and
committed native WORLD store. The ORIGINAL source validators verify
each, and the original request reconstruction matches exactly.

No new commit or side effect is performed. The local receipt can be
self-consistent without cryptographic evidence of its external issuer.
The Lean dependent VerifiedDisposition and kernel proof fields are
not constructed by this Python check.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from typing import Any

from runtime.kuuos_lean_python_memory_world_native_v0_31 import (
    BLOCKED, NO_DATA, PASS, SourceException, NativeMemoryWorldAudit,
    packet, check_bool, match, success, rejected,
)
from runtime.kuuos_authorized_atomic_world_commit_entry_v0_34 import (
    validate_world_store,
    validate_world_commit_authorization_receipt,
    validate_authorized_world_commit_request,
    validate_atomic_world_commit_receipt,
    build_authorized_world_commit_request,
)
from runtime.kuuos_lean_python_world_obligations_v0_27 import (
    audit_witness as lean_data_check,
)

OS_NAME = "WORLD"
FORMAL_SOURCE = "formal/KUOS/OpenHorizon/AuthorizedAtomicWorldCommitKernelV0_34.lean"


def audit_original_world_commit(
    source_disposition_envelope: Any,
    authorization_envelope: Any,
    request_envelope: Any,
    recorded_receipt_envelope: Any,
    world_store_envelope: Any,
) -> NativeMemoryWorldAudit:
    """Read-only source binding for a recorded completed atomic WORLD commit."""
    if any(x is None for x in (
        source_disposition_envelope, authorization_envelope,
        request_envelope, recorded_receipt_envelope, world_store_envelope,
    )):
        return NativeMemoryWorldAudit(
            OS_NAME, NO_DATA, ("WORLD:original_commit_source_missing",))
    try:
        disposition = packet(source_disposition_envelope, "WORLD.disposition")
        authorization = packet(authorization_envelope, "WORLD.authorization")
        request = packet(request_envelope, "WORLD.request")
        receipt = packet(recorded_receipt_envelope, "WORLD.receipt")
        store = packet(world_store_envelope, "WORLD.store")
        native_store = validate_world_store(store)
        auth = validate_world_commit_authorization_receipt(authorization)
        req = validate_authorized_world_commit_request(request)
        record = validate_atomic_world_commit_receipt(receipt)
        # Original replay checks the *same* verified disposition and
        # authorization/source binding; no host operation or WRITE occurs.
        recreated = build_authorized_world_commit_request(
            disposition, authorization, requested_at_ms=req["requested_at_ms"])
        match(recreated, request, "WORLD:exact_reconstructed_request")
        commits = native_store.get("commits")
        if type(commits) is not list or not commits:
            raise SourceException("WORLD:no_persisted_atomic_commit", NO_DATA)
        match(commits[-1], receipt, "WORLD:recorded_last_receipt")
        match(native_store["last_commit_digest"], receipt["body_digest"],
              "WORLD:last_immutable_commit_digest")
        match(native_store["generation"], record["generation_after"],
              "WORLD:recorded_generation")
        match(record["generation_before"] + 1, record["generation_after"],
              "WORLD:successor_generation")
        match(auth["authorization_id"], record["authorization_id"],
              "WORLD:single_use_authorization_id")
        match(authorization["body_digest"], record["authorization_digest"],
              "WORLD:authorization_digest")
        match(request["body_digest"], record["request_digest"],
              "WORLD:request_digest")
        match(native_store["root_lineage_digest"], record["root_lineage_digest"],
              "WORLD:same_root")
        match(native_store["world_store_id"], record["world_store_id"],
              "WORLD:store_identity")
        match(req["expected_generation"], record["generation_before"],
              "WORLD:expected_generation")
        match(req["candidate_world_fragment_digest"],
              record["committed_world_fragment_digest"],
              "WORLD:committed_fragment")
        match(req["expected_prior_commit_digest"],
              record["previous_commit_digest"],
              "WORLD:prior_commit")
        match(req["fencing_token"], record["fencing_token"],
              "WORLD:fencing")
        match(req["lease_epoch"], record["lease_epoch"], "WORLD:lease_epoch")
        for field in ("world_commit_is_truth", "world_commit_is_causal_attribution",
                      "automatic_mission_completion", "grants_plan_activation",
                      "grants_actos_invocation"):
            check_bool(record, field, False, "WORLD.receipt")

        for field in ("global_cycle_limit", "global_generation_limit",
                      "global_time_horizon_limit"):
            if native_store.get(field) is not None or record.get(field) is not None:
                raise SourceException("WORLD:open_horizon_cap_introduced:" + field)

        conditions = {
            "localCommitAuthorizationFinite":
                auth["issued_at_ms"] <= auth["not_before_ms"] <
                auth["expires_at_ms"] and
                auth["not_before_ms"] <= req["requested_at_ms"] <
                record["committed_at_ms"] + 1 <= auth["expires_at_ms"],
            "localCommitAuthorizationSingleUse":
                auth.get("single_use") and record.get("authorization_consumed"),
            "openHorizonPreserved":
                bool(native_store.get("open_horizon_preserved")
                     and record.get("open_horizon_preserved")
                     and auth.get("open_horizon_preserved")),
            "globalCycleLimitAbsent": native_store["global_cycle_limit"] is None,
            "globalGenerationLimitAbsent": native_store["global_generation_limit"] is None,
            "globalTimeHorizonLimitAbsent": native_store["global_time_horizon_limit"] is None,
            "atomicReplaceCommitted": record.get("atomic_replace_committed"),
            "oneAtomicStoreAndReceiptState":
                len(commits) == native_store["generation"]
                and commits[-1] == receipt,
            "appendOnlyHistoryPreserved":
                bool(native_store.get("append_only_history")
                     and record.get("append_only_history_preserved")),
            "immutableCommitReceipt": record.get("immutable_commit_receipt"),
            "sameRootPreserved":
                bool(record.get("same_root_preserved")
                     and record["root_lineage_digest"] ==
                     native_store["root_lineage_digest"]),
            "constitutionalRootRewritten": record.get("constitutional_root_rewritten"),
            "memoryHistoryOverwritten": record.get("memory_history_overwritten"),
            "rollbackReferencePreserved": record.get("rollback_reference_preserved"),
            "rollbackRequiresFreshAuthorization":
                record.get("rollback_requires_fresh_authorization"),
            "rollbackDeletesHistory": not record.get("rollback_is_not_history_deletion"),
            "automaticRollbackPerformed": record.get("automatic_rollback_performed"),
        }
        verdict = lean_data_check(conditions)
        if verdict.status != "LOCAL_CONDITIONS_CHECKED":
            raise SourceException("WORLD:selected_Lean_source_conditions_failed")
        return success(OS_NAME, [
            disposition, authorization, request, receipt, store,
        ], (
            "WORLD.original_verified_disposition.body_digest",
            "WORLD.authorization.body_digest",
            "WORLD.authorization.body.single_use",
            "WORLD.authorization.body.not_before_ms",
            "WORLD.authorization.body.expires_at_ms",
            "WORLD.request.body_digest",
            "WORLD.request.body.expected_generation",
            "WORLD.request.body.expected_prior_commit_digest",
            "WORLD.receipt.body_digest",
            "WORLD.receipt.body.authorization_consumed",
            "WORLD.receipt.body.atomic_replace_committed",
            "WORLD.receipt.body.append_only_history_preserved",
            "WORLD.receipt.body.immutable_commit_receipt",
            "WORLD.receipt.body.same_root_preserved",
            "WORLD.receipt.body.rollback_requires_fresh_authorization",
            "WORLD.receipt.body.rollback_is_not_history_deletion",
            "WORLD.store.body.root_lineage_digest",
            "WORLD.store.body.commits[-1].body_digest",
            "WORLD.store.body.generation",
            "WORLD.store.body.open_horizon_preserved",
            "WORLD.store.body.global_generation_limit",
        ))
    except SourceException as exc:
        return NativeMemoryWorldAudit(OS_NAME, exc.status, (exc.message,))
    except (TypeError, ValueError, KeyError, OverflowError, UnicodeError,
            RecursionError, AttributeError) as exc:
        return rejected(OS_NAME, "WORLD:original_native_source_invalid:"
                        + type(exc).__name__)


__all__ = ("OS_NAME", "FORMAL_SOURCE", "audit_original_world_commit")
