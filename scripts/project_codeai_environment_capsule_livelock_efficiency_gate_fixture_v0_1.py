from __future__ import annotations

from typing import Any, Mapping


def project_fixture(fixture: Mapping[str, Any]) -> dict[str, Any]:
    pack = fixture["gate_pack"]
    receipt = fixture["receipt"]
    return {
        "schema_version": pack["schema_version"],
        "profile_version": pack["profile_version"],
        "repository_full_name": pack["repository_full_name"],
        "source_commit_sha": pack["source_commit_sha"],
        "selected_specialist_id": pack["selected_specialist_id"],
        "selected_specialist_kind": pack["selected_specialist_kind"],
        "selected_subtask_kind": pack["selected_subtask_kind"],
        "step_count": pack["step_count"],
        "tool_call_count": pack["tool_call_count"],
        "model_call_count": pack["model_call_count"],
        "token_units": pack["token_units"],
        "wall_clock_ms": pack["wall_clock_ms"],
        "failed_action_count": pack["failed_action_count"],
        "total_progress_units": pack["total_progress_units"],
        "distinct_state_count": pack["distinct_state_count"],
        "maximum_no_progress_streak": pack["maximum_no_progress_streak"],
        "repeated_zero_progress_transitions": pack["repeated_zero_progress_transitions"],
        "cycle_count": pack["cycle_count"],
        "cycle_detected": pack["cycle_detected"],
        "environment_exact": pack["environment_exact"],
        "predecessor_router_verified": pack["predecessor_router_verified"],
        "trace_grounded": pack["trace_grounded"],
        "capsule_reproducible": pack["capsule_reproducible"],
        "livelock_free": pack["livelock_free"],
        "efficiency_within_budget": pack["efficiency_within_budget"],
        "gate_decision": pack["gate_decision"],
        "hold_reasons": pack["hold_reasons"],
        "continuation_hint_only": pack["continuation_hint_only"],
        "continuation_authority_granted": pack["continuation_authority_granted"],
        "execution_authority_granted": pack["execution_authority_granted"],
        "repository_mutation_performed": pack["repository_mutation_performed"],
        "git_authority_granted": pack["git_authority_granted"],
        "correctness_claimed": pack["correctness_claimed"],
        "request_digest": pack["request_digest"],
        "policy_digest": pack["policy_digest"],
        "router_admission_manifest_digest": pack["router_admission_manifest_digest"],
        "router_admission_pack_digest": pack["router_admission_pack_digest"],
        "router_admission_receipt_digest": pack["router_admission_receipt_digest"],
        "environment_capsule_digest": pack["environment_capsule_digest"],
        "progress_trace_digest": pack["progress_trace_digest"],
        "gate_pack_digest": pack["codeai_environment_capsule_livelock_efficiency_gate_pack_digest"],
        "receipt_digest": receipt["codeai_environment_capsule_livelock_efficiency_gate_receipt_digest"],
    }


__all__ = ["project_fixture"]
