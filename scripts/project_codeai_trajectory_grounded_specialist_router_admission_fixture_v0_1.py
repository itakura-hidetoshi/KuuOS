from __future__ import annotations

from typing import Any, Mapping


def project_fixture(fixture: Mapping[str, Any]) -> dict[str, Any]:
    pack = fixture["admission_pack"]
    receipt = fixture["receipt"]
    return {
        "schema_version": pack["schema_version"],
        "profile_version": pack["profile_version"],
        "repository_full_name": pack["repository_full_name"],
        "source_commit_sha": pack["source_commit_sha"],
        "queried_subtask_kind": pack["queried_subtask_kind"],
        "exploration_turns": pack["exploration_turns"],
        "observation_count": pack["observation_count"],
        "execution_signal_count": pack["execution_signal_count"],
        "grounding_source_count": pack["grounding_source_count"],
        "observable_artifact_count": pack["observable_artifact_count"],
        "eligible_specialist_count": pack["eligible_specialist_count"],
        "excluded_specialist_count": pack["excluded_specialist_count"],
        "route_decision": pack["route_decision"],
        "selected_specialist_id": pack["selected_specialist_id"],
        "selected_specialist_kind": pack["selected_specialist_kind"],
        "selected_utility_score": pack["selected_utility_score"],
        "measurement_grounded": pack["measurement_grounded"],
        "exact_binding_verified": pack["exact_binding_verified"],
        "memory_pack_binding_verified": pack["memory_pack_binding_verified"],
        "specialist_alignment_verified": pack["specialist_alignment_verified"],
        "independent_measurement_verified": pack["independent_measurement_verified"],
        "route_hint_only": pack["route_hint_only"],
        "specialist_dispatched": pack["specialist_dispatched"],
        "candidate_selected": pack["candidate_selected"],
        "execution_authority_granted": pack["execution_authority_granted"],
        "repository_mutation_performed": pack["repository_mutation_performed"],
        "git_authority_granted": pack["git_authority_granted"],
        "correctness_claimed": pack["correctness_claimed"],
        "memory_pack_digest": pack["memory_pack_digest"],
        "memory_receipt_digest": pack["memory_receipt_digest"],
        "request_digest": pack["request_digest"],
        "policy_digest": pack["policy_digest"],
        "trajectory_digest": pack["trajectory_digest"],
        "admission_pack_digest": pack["codeai_trajectory_grounded_specialist_router_admission_pack_digest"],
        "receipt_digest": receipt["codeai_trajectory_grounded_specialist_router_admission_receipt_digest"],
    }


__all__ = ["project_fixture"]
