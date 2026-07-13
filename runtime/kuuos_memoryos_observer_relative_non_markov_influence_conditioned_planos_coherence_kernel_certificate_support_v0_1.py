from __future__ import annotations


def expected_governance_claims() -> dict[str, bool]:
    return {
        "observer_relative_memory_influence_preserved": True,
        "finite_window_not_markov_replacement": True,
        "discarded_tail_residue_effect_visible": True,
        "memory_conditioning_is_diagonal_phase_congruence": True,
        "memory_phase_is_exact_mod4_encoding": True,
        "memory_phase_is_physical_time": False,
        "influence_functional_is_causal_truth": False,
        "all_planos_histories_retained": True,
        "all_history_pair_support_retained": True,
        "hermitian_symmetry_preserved": True,
        "diagonal_normalization_preserved": True,
        "positive_semidefinite_witness_preserved": True,
        "amplitude_reweighting_performed": False,
        "kernel_entry_deletion_performed": False,
        "history_pruning_performed": False,
        "history_ranking_performed": False,
        "representative_history_selected": False,
        "plan_selection_performed": False,
        "decision_commit_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v041_mutated": False,
        "source_planos_v123_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only_advisory_kernel": True,
        "read_only": True,
    }


__all__ = ["expected_governance_claims"]
