from __future__ import annotations

from typing import Any

from runtime.kuuos_memoryos_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_schema_support_v0_1 import digest_object

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


def _profile_by_id(source_memoryos_v041_receipt: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        item["history_id"]: item
        for item in source_memoryos_v041_receipt["candidate_influence_profile"]
    }


def memory_phase_profile(source_memoryos_v041_receipt: dict[str, Any]) -> list[dict[str, Any]]:
    by_id = _profile_by_id(source_memoryos_v041_receipt)
    output: list[dict[str, Any]] = []
    for history_id in source_memoryos_v041_receipt["retained_history_ids"]:
        row = by_id[history_id]
        conditioned_phase = row["conditioned_action_numerator"] % 4
        window_phase = row["window_only_action_numerator"] % 4
        tail_phase_shift = (conditioned_phase - window_phase) % 4
        output.append(
            {
                "history_id": history_id,
                "action_denominator": row["action_denominator"],
                "conditioned_action_numerator": row["conditioned_action_numerator"],
                "window_only_action_numerator": row["window_only_action_numerator"],
                "tail_influence_numerator": row["tail_influence_numerator"],
                "conditioned_phase_mod4": conditioned_phase,
                "window_only_phase_mod4": window_phase,
                "tail_phase_shift_mod4": tail_phase_shift,
                "tail_changes_phase": tail_phase_shift != 0,
                "conditioned_unit_real": gaussian_unit(conditioned_phase)[0],
                "conditioned_unit_imag": gaussian_unit(conditioned_phase)[1],
                "window_only_unit_real": gaussian_unit(window_phase)[0],
                "window_only_unit_imag": gaussian_unit(window_phase)[1],
            }
        )
    return output


def _deform_step(
    step: dict[str, Any],
    *,
    phase_by_id: dict[str, int],
    history_ids: list[str],
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
        (item["row_history_id"], item["column_history_id"]): item
        for item in entries
    }
    hermitian = all(
        by_pair[(row_id, column_id)]["real_numerator"]
        == by_pair[(column_id, row_id)]["real_numerator"]
        and by_pair[(row_id, column_id)]["imag_numerator"]
        == -by_pair[(column_id, row_id)]["imag_numerator"]
        for row_id in history_ids
        for column_id in history_ids
    )
    source_by_pair = {
        (item["row_history_id"], item["column_history_id"]): item
        for item in step["kernel_entries"]
    }
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
        "positive_semidefinite_by_diagonal_phase_congruence": (
            step["positive_semidefinite_by_convex_gram_construction"]
        ),
        "source_convex_gram_witness_retained": (
            step["positive_semidefinite_by_convex_gram_construction"]
        ),
        "kernel_entries": entries,
    }


def influence_conditioned_coherence_observables(
    *,
    source_memoryos_v041_receipt: dict[str, Any],
    source_planos_v123_kernel_receipt: dict[str, Any],
    input_digest: str,
) -> dict[str, Any]:
    history_ids = source_planos_v123_kernel_receipt["retained_history_ids"]
    phase_profile = memory_phase_profile(source_memoryos_v041_receipt)
    full_phase_by_id = {
        item["history_id"]: item["conditioned_phase_mod4"] for item in phase_profile
    }
    window_phase_by_id = {
        item["history_id"]: item["window_only_phase_mod4"] for item in phase_profile
    }
    full_trajectory = [
        _deform_step(step, phase_by_id=full_phase_by_id, history_ids=history_ids)
        for step in source_planos_v123_kernel_receipt["partial_dephasing_trajectory"]
    ]
    window_trajectory = [
        _deform_step(step, phase_by_id=window_phase_by_id, history_ids=history_ids)
        for step in source_planos_v123_kernel_receipt["partial_dephasing_trajectory"]
    ]
    changed_entries: list[dict[str, Any]] = []
    for full_step, window_step in zip(full_trajectory, window_trajectory):
        for full_entry, window_entry in zip(
            full_step["kernel_entries"], window_step["kernel_entries"]
        ):
            if (
                full_entry["real_numerator"] != window_entry["real_numerator"]
                or full_entry["imag_numerator"] != window_entry["imag_numerator"]
            ):
                changed_entries.append(
                    {
                        "dephasing_numerator": full_step["dephasing_numerator"],
                        "row_history_id": full_entry["row_history_id"],
                        "column_history_id": full_entry["column_history_id"],
                        "full_memory_real_numerator": full_entry["real_numerator"],
                        "full_memory_imag_numerator": full_entry["imag_numerator"],
                        "window_only_real_numerator": window_entry["real_numerator"],
                        "window_only_imag_numerator": window_entry["imag_numerator"],
                    }
                )
    tail_sensitive_steps = sorted(
        {item["dephasing_numerator"] for item in changed_entries}, reverse=True
    )
    source_kernel_digest = digest_object(
        source_planos_v123_kernel_receipt["partial_dephasing_trajectory"]
    )
    conditioned_kernel_digest = digest_object(full_trajectory)
    window_only_kernel_digest = digest_object(window_trajectory)
    deformation_digest = digest_object(
        {
            "input_digest": input_digest,
            "memory_phase_profile": phase_profile,
            "source_kernel_digest": source_kernel_digest,
            "conditioned_kernel_digest": conditioned_kernel_digest,
            "window_only_kernel_digest": window_only_kernel_digest,
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
        "source_planos_v123_input_digest": source_planos_v123_kernel_receipt[
            "input_digest"
        ],
        "retained_history_ids": history_ids,
        "history_count": len(history_ids),
        "dephasing_denominator": source_planos_v123_kernel_receipt[
            "dephasing_denominator"
        ],
        "dephasing_numerators": source_planos_v123_kernel_receipt[
            "dephasing_numerators"
        ],
        "memory_phase_profile": phase_profile,
        "full_memory_conditioned_trajectory": full_trajectory,
        "window_only_conditioned_trajectory": window_trajectory,
        "tail_sensitive_kernel_entries": changed_entries,
        "tail_sensitive_kernel_entry_count": len(changed_entries),
        "tail_sensitive_dephasing_numerators": tail_sensitive_steps,
        "tail_sensitive_step_count": len(tail_sensitive_steps),
        "discarded_tail_changes_coherence_kernel": bool(changed_entries),
        "all_conditioned_steps_hermitian": all(
            step["kernel_hermitian"] for step in full_trajectory
        ),
        "all_window_only_steps_hermitian": all(
            step["kernel_hermitian"] for step in window_trajectory
        ),
        "all_diagonals_preserved": all(
            step["diagonal_normalization_preserved"]
            for step in full_trajectory + window_trajectory
        ),
        "all_steps_psd_by_diagonal_phase_congruence": all(
            step["positive_semidefinite_by_diagonal_phase_congruence"]
            for step in full_trajectory + window_trajectory
        ),
        "all_history_pair_support_retained": all(
            len(step["kernel_entries"]) == len(history_ids) * len(history_ids)
            for step in full_trajectory + window_trajectory
        ),
        "amplitude_reweighting_performed": False,
        "kernel_entry_deletion_performed": False,
        "source_kernel_digest": source_kernel_digest,
        "conditioned_kernel_digest": conditioned_kernel_digest,
        "window_only_kernel_digest": window_only_kernel_digest,
        "coherence_deformation_digest": deformation_digest,
    }


__all__ = [
    "gaussian_conj",
    "gaussian_mul",
    "gaussian_unit",
    "influence_conditioned_coherence_observables",
    "memory_phase_profile",
    "phase_deform_entry",
]
