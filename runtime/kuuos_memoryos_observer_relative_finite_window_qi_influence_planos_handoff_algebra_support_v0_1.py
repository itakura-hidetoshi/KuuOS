from __future__ import annotations

from typing import Any

from runtime.kuuos_memoryos_observer_relative_finite_window_qi_influence_planos_handoff_schema_support_v0_1 import (
    COMPONENTS,
    digest_object,
)


def zero_component_map() -> dict[str, int]:
    return {component: 0 for component in COMPONENTS}


def component_add(left: dict[str, int], right: dict[str, int]) -> dict[str, int]:
    return {component: left[component] + right[component] for component in COMPONENTS}


def component_scale(weight: int, values: dict[str, int]) -> dict[str, int]:
    return {component: weight * values[component] for component in COMPONENTS}


def component_dot(couplings: dict[str, int], values: dict[str, int]) -> int:
    return sum(couplings[component] * values[component] for component in COMPONENTS)


def weighted_window_components(
    lag_weights: list[int],
    window_records: list[dict[str, Any]],
) -> dict[str, int]:
    if len(lag_weights) != len(window_records):
        raise ValueError("lag_weight_window_length_mismatch")
    total = zero_component_map()
    for weight, record in zip(lag_weights, window_records):
        total = component_add(
            total,
            component_scale(weight, record["component_effects"]),
        )
    return total


def exact_discarded_tail_residue(
    discarded_tail_records: list[dict[str, Any]],
) -> dict[str, int]:
    total = zero_component_map()
    for record in discarded_tail_records:
        total = component_add(total, record["component_effects"])
    return total


def candidate_influence_profile(
    *,
    source_history_ids: list[str],
    candidate_couplings: list[dict[str, Any]],
    weighted_window: dict[str, int],
    discarded_tail_residue: dict[str, int],
    action_denominator: int,
) -> list[dict[str, Any]]:
    by_id = {item["history_id"]: item for item in candidate_couplings}
    output: list[dict[str, Any]] = []
    for history_id in source_history_ids:
        row = by_id[history_id]
        couplings = row["component_couplings"]
        window_influence = component_dot(couplings, weighted_window)
        tail_influence = component_dot(couplings, discarded_tail_residue)
        total_influence = window_influence + tail_influence
        base_action = row["base_action_numerator"]
        output.append(
            {
                "history_id": history_id,
                "base_action_numerator": base_action,
                "window_influence_numerator": window_influence,
                "tail_influence_numerator": tail_influence,
                "total_history_influence_numerator": total_influence,
                "conditioned_action_numerator": base_action + total_influence,
                "window_only_action_numerator": base_action + window_influence,
                "action_denominator": action_denominator,
                "support_retained": True,
            }
        )
    return output


def influence_handoff_observables(
    *,
    source_memoryos_v040_receipt: dict[str, Any],
    source_planos_v123_receipt: dict[str, Any],
    projection_records: list[dict[str, Any]],
    window_length: int,
    lag_weights: list[int],
    discarded_tail_residue: dict[str, int],
    candidate_couplings: list[dict[str, Any]],
    action_denominator: int,
    input_digest: str,
) -> dict[str, Any]:
    window_records = projection_records[-window_length:]
    tail_records = projection_records[:-window_length]
    weighted_window = weighted_window_components(lag_weights, window_records)
    profiles = candidate_influence_profile(
        source_history_ids=source_planos_v123_receipt["retained_history_ids"],
        candidate_couplings=candidate_couplings,
        weighted_window=weighted_window,
        discarded_tail_residue=discarded_tail_residue,
        action_denominator=action_denominator,
    )
    tail_nonzero = any(discarded_tail_residue.values())
    tail_sensitive_count = sum(
        item["tail_influence_numerator"] != 0 for item in profiles
    )
    observer_ids = [item["observer_id"] for item in projection_records]
    projection_digest = digest_object(
        {
            "record_ids": [item["record_id"] for item in projection_records],
            "record_digests": [item["record_digest"] for item in projection_records],
            "component_effects": [item["component_effects"] for item in projection_records],
            "window_length": window_length,
            "lag_weights": lag_weights,
            "discarded_tail_residue": discarded_tail_residue,
        }
    )
    handoff_digest = digest_object(
        {
            "input_digest": input_digest,
            "memoryos_v040_certificate_digest": source_memoryos_v040_receipt[
                "certificate_digest"
            ],
            "planos_v123_input_digest": source_planos_v123_receipt["input_digest"],
            "projection_digest": projection_digest,
            "candidate_profiles": profiles,
        }
    )
    return {
        "input_digest": input_digest,
        "source_memoryos_v040_certificate_digest": source_memoryos_v040_receipt[
            "certificate_digest"
        ],
        "source_memoryos_v040_record_ledger_digest": source_memoryos_v040_receipt[
            "record_ledger_digest"
        ],
        "source_memoryos_v040_temporal_cycle_digest": source_memoryos_v040_receipt[
            "temporal_cycle_digest"
        ],
        "source_planos_v123_input_digest": source_planos_v123_receipt["input_digest"],
        "component_names": list(COMPONENTS),
        "full_record_ids": [item["record_id"] for item in projection_records],
        "full_record_digests": [item["record_digest"] for item in projection_records],
        "full_record_count": len(projection_records),
        "window_record_ids": [item["record_id"] for item in window_records],
        "window_record_digests": [item["record_digest"] for item in window_records],
        "window_record_count": len(window_records),
        "discarded_tail_record_ids": [item["record_id"] for item in tail_records],
        "discarded_tail_record_digests": [item["record_digest"] for item in tail_records],
        "discarded_tail_record_count": len(tail_records),
        "lag_weights": lag_weights,
        "weighted_window_components": weighted_window,
        "discarded_tail_residue": discarded_tail_residue,
        "discarded_tail_residue_nonzero": tail_nonzero,
        "translation_residue_visible_record_count": sum(
            item["translation_residue_visible"] for item in projection_records
        ),
        "observation_backaction_visible_record_count": sum(
            item["observation_backaction_visible"] for item in projection_records
        ),
        "retained_observer_ids": source_memoryos_v040_receipt[
            "retained_observer_ids"
        ],
        "projection_observer_sequence": observer_ids,
        "retained_planos_history_ids": source_planos_v123_receipt[
            "retained_history_ids"
        ],
        "candidate_influence_profile": profiles,
        "candidate_count": len(profiles),
        "tail_sensitive_candidate_count": tail_sensitive_count,
        "tail_residue_changes_at_least_one_candidate": tail_sensitive_count > 0,
        "all_planos_histories_retained": (
            [item["history_id"] for item in profiles]
            == source_planos_v123_receipt["retained_history_ids"]
        ),
        "finite_window_is_suffix_projection": True,
        "full_history_replaced": False,
        "observer_relative_projection_preserved": True,
        "projection_digest": projection_digest,
        "influence_handoff_digest": handoff_digest,
    }


__all__ = [
    "candidate_influence_profile",
    "component_add",
    "component_dot",
    "component_scale",
    "exact_discarded_tail_residue",
    "influence_handoff_observables",
    "weighted_window_components",
    "zero_component_map",
]
