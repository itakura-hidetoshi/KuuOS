from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_digest(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _nat(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _positive_nat(value: Any) -> bool:
    return _nat(value) and value > 0


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def normalize_histories(
    values: Any,
    *,
    maximum_history_count: int,
    maximum_weight_numerator: int,
):
    fields = {
        "history_id",
        "terminal_state_id",
        "homotopy_class_id",
        "coherence_block_id",
        "weight_numerator",
        "phase_mod4",
        "source_v122_history_digest",
        "source_plan_digest",
        "source_homotopy_witness_digest",
    }
    blockers: list[str] = []
    output: list[dict] = []
    seen: set[str] = set()

    if not isinstance(values, list) or not values:
        return ["history_family_empty"], []
    if len(values) > maximum_history_count:
        return ["maximum_history_count_exceeded"], []

    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"history_schema_invalid_{index}")
            continue

        history_id = item["history_id"]
        if not _nonempty_text(history_id):
            blockers.append(f"history_id_invalid_{index}")
            continue
        if history_id in seen:
            blockers.append("duplicate_history_id")
            continue
        seen.add(history_id)

        for field in (
            "terminal_state_id",
            "homotopy_class_id",
            "coherence_block_id",
            "source_v122_history_digest",
            "source_plan_digest",
            "source_homotopy_witness_digest",
        ):
            if not _nonempty_text(item[field]):
                blockers.append(f"{field}_missing_{history_id}")

        weight = item["weight_numerator"]
        if not _positive_nat(weight) or weight > maximum_weight_numerator:
            blockers.append(f"history_weight_invalid_{history_id}")
            weight = 0

        phase = item["phase_mod4"]
        if phase not in (0, 1, 2, 3):
            blockers.append(f"history_phase_mod4_invalid_{history_id}")
            phase = 0

        output.append(
            {
                "history_id": history_id,
                "terminal_state_id": item["terminal_state_id"],
                "homotopy_class_id": item["homotopy_class_id"],
                "coherence_block_id": item["coherence_block_id"],
                "weight_numerator": weight,
                "phase_mod4": phase,
                "source_v122_history_digest": item["source_v122_history_digest"],
                "source_plan_digest": item["source_plan_digest"],
                "source_homotopy_witness_digest": item[
                    "source_homotopy_witness_digest"
                ],
            }
        )

    return blockers, sorted(output, key=lambda item: item["history_id"])


def normalize_dephasing_numerators(
    value: Any,
    *,
    denominator: int,
    maximum_step_count: int,
):
    blockers: list[str] = []
    if (
        not isinstance(value, list)
        or len(value) < 2
        or len(value) > maximum_step_count
        or any(not _nat(item) for item in value)
    ):
        return ["dephasing_numerator_sequence_invalid"], []

    output = list(value)
    if output[0] != denominator:
        blockers.append("dephasing_sequence_must_start_fully_coherent")
    if output[-1] != 0:
        blockers.append("dephasing_sequence_must_end_block_dephased")
    if any(item > denominator for item in output):
        blockers.append("dephasing_numerator_exceeds_denominator")
    if any(left <= right for left, right in zip(output, output[1:])):
        blockers.append("dephasing_numerators_must_strictly_decrease")

    return blockers, output


CLAIM_FIELDS = {
    "input_digest",
    "retained_history_ids",
    "history_count",
    "terminal_state_ids",
    "homotopy_class_ids",
    "coherence_block_ids",
    "history_amplitude_profile",
    "endpoint_intensity_profile",
    "block_amplitude_profile",
    "endpoint_coherent_kernel",
    "incoherent_mass_numerator_squared",
    "endpoint_gram_hilbert_schmidt_numerator_quartic",
    "block_gram_hilbert_schmidt_numerator_quartic",
    "cross_block_hilbert_schmidt_numerator_quartic",
    "partial_dephasing_trajectory",
    "trajectory_trace_preserved",
    "trajectory_cross_coherence_nonincreasing",
    "trajectory_purity_nonincreasing",
    "trajectory_mixedness_nondecreasing",
    "all_histories_retained",
    "homotopy_partition_exact",
    "exact_rational_partial_dephasing",
    "convex_gram_witness_used",
    "argmin_performed",
    "representative_history_selected",
    "history_ranking_performed",
    "history_pruning_performed",
    "activation_performed",
    "execution_permission",
    "source_v122_certificate_mutated",
    "persistent_world_state_mutated",
}


def normalize_claims(value: Any):
    if not isinstance(value, dict) or set(value) != CLAIM_FIELDS:
        return ["claims_schema_invalid"], {}
    return [], dict(value)


def compute_partial_dephasing_input_digest(**payload) -> str:
    return canonical_digest(payload)


__all__ = [
    "CLAIM_FIELDS",
    "canonical_digest",
    "compute_partial_dephasing_input_digest",
    "normalize_claims",
    "normalize_dephasing_numerators",
    "normalize_histories",
]
