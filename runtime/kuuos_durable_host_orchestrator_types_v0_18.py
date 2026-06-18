#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import sha, without

VERSION = "kuuos_durable_host_invocation_orchestrator_v0_18"
STATE_VERSION = "kuuos_durable_host_orchestrator_state_v0_18"
WORKER_REPORT_VERSION = "kuuos_durable_host_worker_report_v0_18"
POLICY_VERSION = "kuuos_durable_host_orchestrator_policy_v0_18"
PLAN_VERSION = "kuuos_durable_host_orchestrator_plan_v0_18"
CYCLE_VERSION = "kuuos_durable_host_orchestrator_cycle_v0_18"
RECEIPT_VERSION = "kuuos_durable_host_orchestrator_receipt_v0_18"
DEAD_LETTER_VERSION = "kuuos_durable_host_dead_letter_v0_18"
DEAD_LETTER_RELEASE_VERSION = "kuuos_durable_host_dead_letter_release_v0_18"

READY = "KUUOS_DURABLE_HOST_ORCHESTRATOR_V0_18_READY"
BLOCKED = "KUUOS_DURABLE_HOST_ORCHESTRATOR_V0_18_BLOCKED"
REPLAYED = "KUUOS_DURABLE_HOST_ORCHESTRATOR_V0_18_REPLAYED"
IDLE = "KUUOS_DURABLE_HOST_ORCHESTRATOR_V0_18_IDLE"

BACKPRESSURE_CLASSES = frozenset(
    {
        "idle",
        "normal",
        "throttled",
        "saturated",
        "no_healthy_workers",
        "capability_gap_or_blocked",
    }
)

PERMANENT_CANDIDATE_BLOCKERS = frozenset(
    {
        "job_version_invalid",
        "job_manifest_digest_invalid",
        "job_state_digest_invalid",
        "job_current_step_index_invalid",
        "job_completed_prefix_invalid",
        "background_ticket_digest_invalid",
        "background_ticket_job_mismatch",
        "background_ticket_checkpoint_missing",
        "background_ticket_checkpoint_mismatch",
        "next_step_missing",
    }
)

NON_AUTHORITY_FLAGS = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}

REQUIRED_BOUNDARY = {
    "v017_eligibility_is_authoritative": True,
    "orchestrator_cannot_unblock_candidate": True,
    "host_license_remains_required": True,
    "one_assignment_per_worker_per_cycle": True,
    "one_assignment_per_job_per_cycle": True,
    "dispatch_capacity_is_finite": True,
    "worker_health_is_observational": True,
    "dead_letter_is_metadata_only": True,
    "dead_letter_release_is_explicit": True,
    "plan_replay_is_idempotent": True,
    "connector_call_inside_runtime_forbidden": True,
    "lower_authority_preserved": True,
    "graph_semantics_forbidden": True,
}


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return sha(without(value, field))


def orchestrator_state_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "orchestrator_state_digest")


def worker_report_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "worker_report_digest")


def policy_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "orchestrator_policy_digest")


def plan_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "orchestrator_plan_digest")


def cycle_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "orchestrator_cycle_digest")


def receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "orchestrator_receipt_digest")


def dead_letter_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "dead_letter_digest")


def dead_letter_release_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "dead_letter_release_digest")


def candidate_key(*, job_id: str, job_state_digest_value: str) -> str:
    return sha({"job_id": str(job_id), "job_state_digest": str(job_state_digest_value)})
