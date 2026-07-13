from __future__ import annotations

from typing import Any

from runtime.kuuos_memoryos_observer_relative_temporal_window_coherence_cocycle_composition_schema_support_v0_1 import (
    COMPONENTS,
    digest_object,
)

Gaussian = tuple[int, int]


def gaussian_mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gaussian_conj(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def gaussian_unit(phase_mod4: int) -> Gaussian:
    return ((1, 0), (0, 1), (-1, 0), (0, -1))[phase_mod4 % 4]


def phase_deform_entry(value: Gaussian, row_phase_mod4: int, column_phase_mod4: int) -> Gaussian:
    return gaussian_mul(
        gaussian_mul(gaussian_unit(row_phase_mod4), value),
        gaussian_conj(gaussian_unit(column_phase_mod4)),
    )


def zero_component_map() -> dict[str, int]:
    return {component: 0 for component in COMPONENTS}


def component_add(left: dict[str, int], right: dict[str, int]) -> dict[str, int]:
    return {component: left[component] + right[component] for component in COMPONENTS}


def component_scale(weight: int, values: dict[str, int]) -> dict[str, int]:
    return {component: weight * values[component] for component in COMPONENTS}


def component_dot(couplings: dict[str, int], values: dict[str, int]) -> int:
    return sum(couplings[component] * values[component] for component in COMPONENTS)


def _records_by_id(source_memoryos_v041_receipt: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        record["record_id"]: record
        for record in source_memoryos_v041_receipt["history_projection_records"]
    }


def temporal_segment_components(
    *,
    source_memoryos_v041_receipt: dict[str, Any],
    temporal_segments: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    records = _records_by_id(source_memoryos_v041_receipt)
    output: list[dict[str, Any]] = []
    for segment in temporal_segments:
        total = zero_component_map()
        for record_id in segment["record_ids"]:
            total = component_add(total, records[record_id]["component_effects"])
        weighted = component_scale(segment["lag_weight"], total)
        output.append(
            {
                "segment_id": segment["segment_id"],
                "segment_kind": segment["segment_kind"],
                "record_ids": segment["record_ids"],
                "observer_id": segment["observer_id"],
                "lag_weight": segment["lag_weight"],
                "unweighted_components": total,
                "weighted_components": weighted,
                "translation_from_previous_id": segment["translation_from_previous_id"],
                "translation_residue_visible": segment["translation_residue_visible"],
            }
        )
    return output


def recompute_v041_candidate_profile(
    source_memoryos_v041_receipt: dict[str, Any],
) -> list[dict[str, Any]]:
    records = source_memoryos_v041_receipt["history_projection_records"]
    window_length = source_memoryos_v041_receipt["window_length"]
    tail_records = records[:-window_length]
    window_records = records[-window_length:]
    tail = zero_component_map()
    for record in tail_records:
        tail = component_add(tail, record["component_effects"])
    weighted_window = zero_component_map()
    for weight, record in zip(source_memoryos_v041_receipt["lag_weights"], window_records):
        weighted_window = component_add(
            weighted_window, component_scale(weight, record["component_effects"])
        )
    by_id = {
        row["history_id"]: row
        for row in source_memoryos_v041_receipt["candidate_couplings"]
    }
    output: list[dict[str, Any]] = []
    for history_id in source_memoryos_v041_receipt["retained_history_ids"]:
        coupling = by_id[history_id]
        window_influence = component_dot(
            coupling["component_couplings"], weighted_window
        )
        tail_influence = component_dot(coupling["component_couplings"], tail)
        base = coupling["base_action_numerator"]
        output.append(
            {
                "history_id": history_id,
                "base_action_numerator": base,
                "window_influence_numerator": window_influence,
                "tail_influence_numerator": tail_influence,
                "total_history_influence_numerator": window_influence + tail_influence,
                "conditioned_action_numerator": base + window_influence + tail_influence,
                "window_only_action_numerator": base + window_influence,
                "action_denominator": source_memoryos_v041_receipt["action_denominator"],
                "support_retained": True,
            }
        )
    return output


def candidate_segment_influence_profile(
    *,
    source_memoryos_v041_receipt: dict[str, Any],
    segment_components: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    couplings_by_id = {
        item["history_id"]: item
        for item in source_memoryos_v041_receipt["candidate_couplings"]
    }
    output: list[dict[str, Any]] = []
    for history_id in source_memoryos_v041_receipt["retained_history_ids"]:
        coupling = couplings_by_id[history_id]
        segments: list[dict[str, Any]] = []
        for segment in segment_components:
            influence = component_dot(
                coupling["component_couplings"], segment["weighted_components"]
            )
            segments.append(
                {
                    "segment_id": segment["segment_id"],
                    "segment_kind": segment["segment_kind"],
                    "observer_id": segment["observer_id"],
                    "influence_numerator": influence,
                    "phase_mod4": influence % 4,
                    "unit_real": gaussian_unit(influence % 4)[0],
                    "unit_imag": gaussian_unit(influence % 4)[1],
                    "phase_neutral": influence % 4 == 0,
                }
            )
        base = coupling["base_action_numerator"]
        total_influence = sum(item["influence_numerator"] for item in segments)
        tail_influence = sum(
            item["influence_numerator"]
            for item in segments
            if item["segment_kind"] == "discarded-tail"
        )
        window_influence = sum(
            item["influence_numerator"]
            for item in segments
            if item["segment_kind"] == "retained-window"
        )
        cumulative = base % 4
        cumulative_phases = [
            {
                "stage_id": "base-action",
                "phase_mod4": cumulative,
                "unit_real": gaussian_unit(cumulative)[0],
                "unit_imag": gaussian_unit(cumulative)[1],
            }
        ]
        for item in segments:
            cumulative = (cumulative + item["phase_mod4"]) % 4
            cumulative_phases.append(
                {
                    "stage_id": item["segment_id"],
                    "phase_mod4": cumulative,
                    "unit_real": gaussian_unit(cumulative)[0],
                    "unit_imag": gaussian_unit(cumulative)[1],
                }
            )
        output.append(
            {
                "history_id": history_id,
                "base_action_numerator": base,
                "base_phase_mod4": base % 4,
                "segments": segments,
                "tail_influence_numerator": tail_influence,
                "window_influence_numerator": window_influence,
                "total_history_influence_numerator": total_influence,
                "conditioned_action_numerator": base + total_influence,
                "conditioned_phase_mod4": (base + total_influence) % 4,
                "coarse_tail_phase_mod4": tail_influence % 4,
                "coarse_window_phase_mod4": window_influence % 4,
                "cumulative_phase_profile": cumulative_phases,
                "action_denominator": source_memoryos_v041_receipt["action_denominator"],
            }
        )
    return output


def _phase_map(profile: list[dict[str, Any]], field: str) -> dict[str, int]:
    return {item["history_id"]: item[field] for item in profile}


def _segment_phase_map(
    profile: list[dict[str, Any]], segment_id: str
) -> dict[str, int]:
    return {
        item["history_id"]: next(
            segment["phase_mod4"]
            for segment in item["segments"]
            if segment["segment_id"] == segment_id
        )
        for item in profile
    }


def _deform_step(
    step: dict[str, Any], *, phase_by_id: dict[str, int], history_ids: list[str]
) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for source in step["kernel_entries"]:
        value = source["real_numerator"], source["imag_numerator"]
        deformed = phase_deform_entry(
            value,
            phase_by_id[source["row_history_id"]],
            phase_by_id[source["column_history_id"]],
        )
        entries.append(
            {
                "row_history_id": source["row_history_id"],
                "column_history_id": source["column_history_id"],
                "real_numerator": deformed[0],
                "imag_numerator": deformed[1],
            }
        )
    by_pair = {
        (item["row_history_id"], item["column_history_id"]): item for item in entries
    }
    source_by_pair = {
        (item["row_history_id"], item["column_history_id"]): item
        for item in step["kernel_entries"]
    }
    hermitian = all(
        by_pair[(row_id, column_id)]["real_numerator"]
        == by_pair[(column_id, row_id)]["real_numerator"]
        and by_pair[(row_id, column_id)]["imag_numerator"]
        == -by_pair[(column_id, row_id)]["imag_numerator"]
        for row_id in history_ids
        for column_id in history_ids
    )
    diagonal_preserved = all(
        by_pair[(history_id, history_id)]["real_numerator"]
        == source_by_pair[(history_id, history_id)]["real_numerator"]
        and by_pair[(history_id, history_id)]["imag_numerator"]
        == source_by_pair[(history_id, history_id)]["imag_numerator"]
        for history_id in history_ids
    )
    return {
        "dephasing_numerator": step["dephasing_numerator"],
        "kernel_entry_denominator": step["kernel_entry_denominator"],
        "kernel_hermitian": hermitian,
        "diagonal_normalization_preserved": diagonal_preserved,
        "positive_semidefinite_by_diagonal_phase_congruence": step[
            "positive_semidefinite_by_diagonal_phase_congruence"
        ],
        "kernel_entries": entries,
    }


def deform_trajectory(
    trajectory: list[dict[str, Any]],
    *,
    phase_by_id: dict[str, int],
    history_ids: list[str],
) -> list[dict[str, Any]]:
    return [
        _deform_step(step, phase_by_id=phase_by_id, history_ids=history_ids)
        for step in trajectory
    ]


def observer_transition_profile(
    temporal_segments: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for previous, current in zip(temporal_segments, temporal_segments[1:]):
        observer_changed = previous["observer_id"] != current["observer_id"]
        output.append(
            {
                "from_segment_id": previous["segment_id"],
                "to_segment_id": current["segment_id"],
                "from_observer_id": previous["observer_id"],
                "to_observer_id": current["observer_id"],
                "observer_changed": observer_changed,
                "translation_id": current["translation_from_previous_id"],
                "translation_residue_visible": current[
                    "translation_residue_visible"
                ],
                "translation_required": observer_changed,
                "translation_compatible": (
                    (not observer_changed and current["translation_from_previous_id"] is None)
                    or (
                        observer_changed
                        and current["translation_from_previous_id"] is not None
                        and current["translation_residue_visible"]
                    )
                ),
            }
        )
    return output


def temporal_window_coherence_cocycle_observables(
    *,
    source_memoryos_v041_receipt: dict[str, Any],
    source_memoryos_v042_receipt: dict[str, Any],
    source_planos_v123_kernel_receipt: dict[str, Any],
    temporal_segments: list[dict[str, Any]],
    input_digest: str,
) -> dict[str, Any]:
    history_ids = source_planos_v123_kernel_receipt["retained_history_ids"]
    segment_components = temporal_segment_components(
        source_memoryos_v041_receipt=source_memoryos_v041_receipt,
        temporal_segments=temporal_segments,
    )
    profile = candidate_segment_influence_profile(
        source_memoryos_v041_receipt=source_memoryos_v041_receipt,
        segment_components=segment_components,
    )
    source_trajectory = source_planos_v123_kernel_receipt[
        "partial_dephasing_trajectory"
    ]
    base_phase = _phase_map(profile, "base_phase_mod4")
    refined_stages: list[dict[str, Any]] = []
    current_trajectory = deform_trajectory(
        source_trajectory, phase_by_id=base_phase, history_ids=history_ids
    )
    refined_stages.append(
        {
            "stage_id": "base-action",
            "phase_by_history": base_phase,
            "trajectory": current_trajectory,
        }
    )
    for segment in temporal_segments:
        segment_phase = _segment_phase_map(profile, segment["segment_id"])
        current_trajectory = deform_trajectory(
            current_trajectory,
            phase_by_id=segment_phase,
            history_ids=history_ids,
        )
        refined_stages.append(
            {
                "stage_id": segment["segment_id"],
                "phase_by_history": segment_phase,
                "trajectory": current_trajectory,
            }
        )
    refined_final = current_trajectory

    coarse_tail_phase = _phase_map(profile, "coarse_tail_phase_mod4")
    coarse_window_phase = _phase_map(profile, "coarse_window_phase_mod4")
    coarse_after_base = deform_trajectory(
        source_trajectory, phase_by_id=base_phase, history_ids=history_ids
    )
    coarse_after_tail = deform_trajectory(
        coarse_after_base,
        phase_by_id=coarse_tail_phase,
        history_ids=history_ids,
    )
    coarse_final = deform_trajectory(
        coarse_after_tail,
        phase_by_id=coarse_window_phase,
        history_ids=history_ids,
    )

    direct_phase = _phase_map(profile, "conditioned_phase_mod4")
    direct_final = deform_trajectory(
        source_trajectory, phase_by_id=direct_phase, history_ids=history_ids
    )
    source_v042_final = source_memoryos_v042_receipt[
        "full_memory_conditioned_trajectory"
    ]
    transitions = observer_transition_profile(temporal_segments)
    v041_recomputed = recompute_v041_candidate_profile(source_memoryos_v041_receipt)
    phase_neutral_segments = sorted(
        {
            segment["segment_id"]
            for item in profile
            for segment in item["segments"]
            if segment["phase_neutral"]
        }
    )
    all_stage_trajectories = [item["trajectory"] for item in refined_stages]
    all_steps = [
        step for trajectory in all_stage_trajectories for step in trajectory
    ] + [step for step in coarse_final + direct_final]
    source_kernel_digest = digest_object(source_trajectory)
    refined_digest = digest_object(refined_final)
    coarse_digest = digest_object(coarse_final)
    direct_digest = digest_object(direct_final)
    composition_digest = digest_object(
        {
            "input_digest": input_digest,
            "segment_components": segment_components,
            "candidate_segment_influence_profile": profile,
            "observer_transition_profile": transitions,
            "refined_final_digest": refined_digest,
            "coarse_final_digest": coarse_digest,
            "direct_final_digest": direct_digest,
        }
    )
    return {
        "input_digest": input_digest,
        "source_memoryos_v041_certificate_digest": source_memoryos_v041_receipt[
            "certificate_digest"
        ],
        "source_memoryos_v041_influence_handoff_digest": source_memoryos_v041_receipt[
            "influence_handoff_digest"
        ],
        "source_memoryos_v042_certificate_digest": source_memoryos_v042_receipt[
            "certificate_digest"
        ],
        "source_planos_v123_input_digest": source_planos_v123_kernel_receipt[
            "input_digest"
        ],
        "retained_history_ids": history_ids,
        "retained_record_ids": source_memoryos_v041_receipt["retained_record_ids"],
        "temporal_segment_ids": [item["segment_id"] for item in temporal_segments],
        "temporal_segment_count": len(temporal_segments),
        "temporal_segment_components": segment_components,
        "candidate_segment_influence_profile": profile,
        "observer_sequence": [item["observer_id"] for item in temporal_segments],
        "observer_transition_profile": transitions,
        "observer_translation_compatible": all(
            item["translation_compatible"] for item in transitions
        ),
        "v041_candidate_influence_profile_recomputed": v041_recomputed,
        "v041_candidate_influence_profile_exact": (
            v041_recomputed
            == source_memoryos_v041_receipt["candidate_influence_profile"]
        ),
        "refined_stage_trajectories": refined_stages,
        "refined_final_trajectory": refined_final,
        "coarse_final_trajectory": coarse_final,
        "direct_conditioned_trajectory": direct_final,
        "source_v042_conditioned_trajectory": source_v042_final,
        "refinement_coarsening_consistent": refined_final == coarse_final,
        "cocycle_direct_composition_consistent": refined_final == direct_final,
        "source_v042_trajectory_exact": refined_final == source_v042_final,
        "composition_associative": (
            refined_final == coarse_final == direct_final == source_v042_final
        ),
        "phase_neutral_segment_ids": phase_neutral_segments,
        "nonzero_phase_neutral_influence_visible": any(
            segment["phase_neutral"] and segment["influence_numerator"] != 0
            for item in profile
            for segment in item["segments"]
        ),
        "all_composed_steps_hermitian": all(
            step["kernel_hermitian"] for step in all_steps
        ),
        "all_composed_diagonals_preserved": all(
            step["diagonal_normalization_preserved"] for step in all_steps
        ),
        "all_composed_steps_psd_by_diagonal_phase_congruence": all(
            step["positive_semidefinite_by_diagonal_phase_congruence"]
            for step in all_steps
        ),
        "all_history_pair_support_retained": all(
            len(step["kernel_entries"]) == len(history_ids) * len(history_ids)
            for step in all_steps
        ),
        "source_kernel_digest": source_kernel_digest,
        "refined_final_kernel_digest": refined_digest,
        "coarse_final_kernel_digest": coarse_digest,
        "direct_final_kernel_digest": direct_digest,
        "source_v042_conditioned_kernel_digest": source_memoryos_v042_receipt[
            "conditioned_kernel_digest"
        ],
        "temporal_window_cocycle_composition_digest": composition_digest,
        "history_pruning_performed": False,
        "history_ranking_performed": False,
        "representative_history_selected": False,
        "plan_selection_performed": False,
        "decision_commit_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v041_mutated": False,
        "source_memoryos_v042_mutated": False,
        "source_planos_v123_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
    }


__all__ = [
    "candidate_segment_influence_profile",
    "component_add",
    "component_dot",
    "component_scale",
    "deform_trajectory",
    "gaussian_conj",
    "gaussian_mul",
    "gaussian_unit",
    "observer_transition_profile",
    "phase_deform_entry",
    "recompute_v041_candidate_profile",
    "temporal_segment_components",
    "temporal_window_coherence_cocycle_observables",
    "zero_component_map",
]
