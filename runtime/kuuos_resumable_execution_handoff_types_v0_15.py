#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import sha, without

VERSION = "kuuos_resumable_execution_handoff_v0_15"
DECISION_VERSION = "kuuos_resumable_execution_handoff_decision_v0_15"
CHECKPOINT_VERSION = "kuuos_resumable_execution_checkpoint_v0_15"
FEEDBACK_VERSION = "kuuos_resumable_execution_feedback_v0_15"
TICKET_VERSION = "kuuos_resumable_execution_background_ticket_v0_15"
BUNDLE_VERSION = "kuuos_resumable_execution_handoff_bundle_v0_15"
READY = "KUUOS_RESUMABLE_EXECUTION_HANDOFF_V0_15_READY"
REPLAYED = "KUUOS_RESUMABLE_EXECUTION_HANDOFF_V0_15_REPLAYED"

RUNNING_STATE = "running"
NON_RUNNING_STATES = frozenset(
    {
        "background_queued",
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
PAUSED_OR_BLOCKED_STATES = frozenset(
    {
        "background_queued",
        "waiting_external",
        "budget_paused",
        "retry_backoff",
        "blocked_bug",
        "permission_blocked",
        "needs_user_input",
        "retry_exhausted",
    }
)
USER_GUIDANCE_STATES = frozenset(
    {
        "blocked_bug",
        "permission_blocked",
        "needs_user_input",
        "retry_exhausted",
    }
)
BACKGROUNDABLE_REASONS = frozenset(
    {
        "cost_budget_exhausted",
        "external_latency",
        "rate_limited",
        "transient_error",
        "timeout",
    }
)
DETERMINISTIC_BUG_KINDS = frozenset(
    {
        "deterministic_bug",
        "invariant_violation",
        "validation_bug",
        "serialization_bug",
    }
)
TRANSIENT_ERROR_KINDS = frozenset({"transient_error", "timeout", "rate_limit"})

REQUIRED_BOUNDARY = {
    "no_silent_pause_or_block": True,
    "every_non_running_state_has_feedback": True,
    "paused_or_blocked_releases_foreground_prompt": True,
    "background_queue_is_explicit": True,
    "background_queue_does_not_claim_execution": True,
    "deterministic_bug_not_blindly_retried": True,
    "retry_count_and_delay_visible": True,
    "checkpoint_digest_binding_required": True,
    "bounded_reclaimable_background_lease": True,
    "duplicate_attempt_idempotent": True,
    "lower_authority_preserved": True,
    "graph_semantics_forbidden": True,
}


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def checkpoint_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "checkpoint_digest")


def feedback_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "feedback_digest")


def ticket_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "background_ticket_digest")


def decision_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "handoff_decision_digest")


def bundle_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "handoff_bundle_digest")


def attempt_digest(value: Mapping[str, Any]) -> str:
    return sha(
        {
            "job_id": str(value.get("job_id", "")),
            "attempt_id": str(value.get("attempt_id", "")),
            "source_parent_digest": str(value.get("source_parent_digest", "")),
            "checkpoint_payload": value.get("checkpoint_payload", {}),
        }
    )
