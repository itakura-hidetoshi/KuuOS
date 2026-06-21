from __future__ import annotations

from collections.abc import Iterable

RECOVERY_VERSION = "kuuos_operational_agent_recovery_v1_1"


def recovery_decision_for(errors: Iterable[str]) -> str:
    """Map a finite blocker set to the existing adaptive recovery algebra.

    Classification is not recovery execution.  The adaptive transition kernel still
    requires a fresh authority receipt, lineage, activation and session where its
    recovery contract says so.
    """

    error_set = set(errors)
    if not error_set:
        return "CONTINUE"

    # An explicit request for an effect above the v1.1 ceiling is not silently
    # downgraded or retried.
    if error_set & {
        "external_commit_not_supported_by_v1_1",
        "human_approval_missing",
        "host_license_missing",
    }:
        return "REQUEST_HUMAN"

    if error_set & {
        "capability_epoch_stale",
        "capability_epoch_mismatch",
        "lease_capability_epoch_mismatch",
    }:
        return "REROTATE"

    if error_set & {
        "lease_inactive",
        "lease_expired",
        "lease_not_yet_active",
        "lease_use_limit_exhausted",
        "intent_replay_forbidden",
        "lease_validation_failed",
    }:
        return "REVALIDATE"

    if error_set & {
        "adapter_kind_mismatch",
        "operation_outside_capability",
        "resource_outside_capability",
        "operation_outside_lease",
        "resource_outside_lease",
        "effect_above_capability_ceiling",
        "effect_above_lease_ceiling",
    }:
        return "REPLAN"

    if error_set & {
        "owner_mismatch",
        "lineage_mismatch",
        "session_mismatch",
        "capability_id_mismatch",
        "adaptive_state_not_active",
        "adaptive_state_not_plan_stage",
        "adaptive_state_not_leased",
        "adaptive_session_missing",
    }:
        return "REQUEST_HUMAN"

    if error_set & {
        "adapter_exception",
        "adapter_result_invalid",
        "adapter_intent_mismatch",
        "adapter_external_commit_forbidden",
        "observer_exception",
        "observation_invalid",
        "verifier_exception",
        "verification_invalid",
        "learner_exception",
        "learning_invalid",
        "adaptive_state_invalid",
        "capability_missing",
        "capability_inactive",
        "capability_validation_failed",
        "intent_validation_failed",
    }:
        return "ABORT"

    return "REQUEST_HUMAN"
