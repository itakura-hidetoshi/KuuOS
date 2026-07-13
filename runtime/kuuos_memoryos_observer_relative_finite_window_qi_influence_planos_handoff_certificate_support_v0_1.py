from __future__ import annotations


def expected_governance_claims() -> dict[str, bool]:
    return {
        "history_projection_read_only": True,
        "finite_window_projection_not_markov_reduction": True,
        "discarded_tail_residue_visible": True,
        "observer_relative_records_preserved": True,
        "translation_residue_preserved": True,
        "all_planos_histories_retained": True,
        "history_pruning_performed": False,
        "history_ranking_performed": False,
        "representative_history_selected": False,
        "plan_selection_performed": False,
        "decision_commit_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v040_mutated": False,
        "source_planos_v123_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only_advisory_handoff": True,
    }


__all__ = ["expected_governance_claims"]
