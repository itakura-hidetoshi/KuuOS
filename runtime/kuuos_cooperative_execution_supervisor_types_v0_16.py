#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import sha, without

VERSION = "kuuos_cooperative_execution_supervisor_v0_16"
JOB_VERSION = "kuuos_cooperative_execution_job_v0_16"
SLICE_VERSION = "kuuos_cooperative_execution_slice_v0_16"
STEP_RECEIPT_VERSION = "kuuos_cooperative_execution_step_receipt_v0_16"
YIELD_VERSION = "kuuos_cooperative_execution_yield_v0_16"
COMMAND_VERSION = "kuuos_cooperative_execution_command_v0_16"
BUNDLE_VERSION = "kuuos_cooperative_execution_supervisor_bundle_v0_16"
READY = "KUUOS_COOPERATIVE_EXECUTION_SUPERVISOR_V0_16_READY"
REPLAYED = "KUUOS_COOPERATIVE_EXECUTION_SUPERVISOR_V0_16_REPLAYED"

SUPERVISOR_STATES = frozenset(
    {
        "ready",
        "foreground_running",
        "foreground_yielded",
        "background_queued",
        "background_leased",
        "waiting_external",
        "budget_paused",
        "retry_backoff",
        "blocked_bug",
        "permission_blocked",
        "needs_user_input",
        "retry_exhausted",
        "completed",
        "cancelled",
    }
)

STEP_OUTCOMES = frozenset(
    {
        "success",
        "transient_error",
        "deterministic_bug",
        "waiting_external",
        "permission_denied",
        "needs_user_input",
        "cancelled",
    }
)

COMMAND_ACTIONS = frozenset(
    {
        "continue_foreground",
        "queue_background",
        "increase_budget",
        "reduce_scope",
        "retry_now",
        "retry_later",
        "revise_input",
        "grant_permission",
        "provide_input",
        "cancel_job",
    }
)

REQUIRED_BOUNDARY = {
    "allowlisted_operations_only": True,
    "bounded_slice_required": True,
    "cost_fit_required_before_step": True,
    "successful_step_receipt_required": True,
    "non_success_delegates_to_v0_15": True,
    "unfinished_foreground_slice_releases_prompt": True,
    "background_queue_explicit": True,
    "queued_does_not_mean_running": True,
    "completed_receipts_append_only": True,
    "slice_and_command_replay_idempotent": True,
    "lower_authority_preserved": True,
    "graph_semantics_forbidden": True,
}


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def manifest_digest(value: Mapping[str, Any]) -> str:
    return sha(
        {
            "job_id": str(value.get("job_id", "")),
            "manifest_revision": int(value.get("manifest_revision", 0) or 0),
            "steps": value.get("steps", []),
        }
    )


def job_state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "job_state_digest")


def step_receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "step_receipt_digest")


def yield_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "yield_digest")


def slice_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "slice_digest")


def command_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "command_digest")


def bundle_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "supervisor_bundle_digest")


def execution_key(
    *,
    job_id: str,
    manifest: str,
    step_id: str,
    attempt: int,
) -> str:
    return sha(
        {
            "job_id": job_id,
            "manifest_digest": manifest,
            "step_id": step_id,
            "attempt": int(attempt),
        }
    )
