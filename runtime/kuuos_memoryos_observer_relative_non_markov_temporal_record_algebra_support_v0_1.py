from __future__ import annotations

from collections import defaultdict
from typing import Any

from runtime.kuuos_memoryos_observer_relative_non_markov_temporal_record_schema_support_v0_1 import (
    digest_object,
)


def weighted_memory(kernel_weights: list[int], history_effects: list[int]) -> int:
    if len(kernel_weights) != len(history_effects):
        raise ValueError("memory_kernel_history_length_mismatch")
    return sum(weight * effect for weight, effect in zip(kernel_weights, history_effects))


def transition_context(
    present_signal: int,
    kernel_weights: list[int],
    history_effects: list[int],
) -> int:
    return present_signal + weighted_memory(kernel_weights, history_effects)


def translation_residual(source_value: int, target_value: int, offset: int) -> int:
    return target_value - (source_value + offset)


def event_observer_profile(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[record["event_digest"]].append(record)
    output: list[dict[str, Any]] = []
    for event_digest in sorted(grouped):
        members = grouped[event_digest]
        observer_ids = sorted({item["observer_id"] for item in members})
        output.append(
            {
                "event_digest": event_digest,
                "record_ids": [item["record_id"] for item in members],
                "observer_ids": observer_ids,
                "observer_count": len(observer_ids),
                "multiple_observer_records_retained": len(observer_ids) > 1,
            }
        )
    return output


def translation_residue_profile(
    translations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "translation_id": item["translation_id"],
            "source_observer_id": item["source_observer_id"],
            "target_observer_id": item["target_observer_id"],
            "event_digest": item["event_digest"],
            "source_value": item["source_value"],
            "target_value": item["target_value"],
            "translated_value": item["translated_value"],
            "translation_residue": item["translation_residue"],
            "residue_visible": item["residue_visible"],
            "exact_translation": item["translation_residue"] == 0,
        }
        for item in translations
    ]


def temporal_record_observables(
    *,
    source_planos_v123_certificate_digest: str,
    source_decisionos_v06_certificate_digest: str,
    source_memoryos_v039_capsule_digest: str,
    source_world_model_digest: str,
    observers: list[dict[str, Any]],
    records: list[dict[str, Any]],
    translations: list[dict[str, Any]],
    memory_kernel_weights: list[int],
    counterfactual_history_effects: list[int],
    present_signal: int,
    input_digest: str,
) -> dict[str, Any]:
    if len(records) < len(memory_kernel_weights):
        raise ValueError("insufficient_records_for_memory_kernel")
    retained = records[-len(memory_kernel_weights) :]
    history_effects = [item["history_effect"] for item in retained]
    if len(counterfactual_history_effects) != len(memory_kernel_weights):
        raise ValueError("counterfactual_history_length_mismatch")

    memory_a = weighted_memory(memory_kernel_weights, history_effects)
    memory_b = weighted_memory(
        memory_kernel_weights, counterfactual_history_effects
    )
    next_a = present_signal + memory_a
    next_b = present_signal + memory_b
    event_profile = event_observer_profile(records)
    residue_profile = translation_residue_profile(translations)
    ledger_digest = digest_object(
        {
            "record_digests": [item["record_digest"] for item in records],
            "observer_ids": [item["observer_id"] for item in observers],
            "translation_ids": [item["translation_id"] for item in translations],
        }
    )
    cycle_digest = digest_object(
        {
            "planos_future": source_planos_v123_certificate_digest,
            "decisionos_present": source_decisionos_v06_certificate_digest,
            "memoryos_past": ledger_digest,
            "prior_memoryos": source_memoryos_v039_capsule_digest,
            "world_model": source_world_model_digest,
        }
    )
    return {
        "input_digest": input_digest,
        "retained_observer_ids": [item["observer_id"] for item in observers],
        "retained_record_ids": [item["record_id"] for item in records],
        "retained_record_digests": [item["record_digest"] for item in records],
        "observer_count": len(observers),
        "record_count": len(records),
        "event_observer_profile": event_profile,
        "translation_residue_profile": residue_profile,
        "visible_translation_residue_count": sum(
            item["translation_residue"] != 0 for item in translations
        ),
        "observer_state_change_count": sum(
            item["observer_changed_by_observation"] for item in records
        ),
        "world_or_backaction_visible_count": sum(
            item["world_changed_or_backaction_visible"] for item in records
        ),
        "memory_kernel_weights": memory_kernel_weights,
        "retained_history_effects": history_effects,
        "counterfactual_history_effects": counterfactual_history_effects,
        "present_signal": present_signal,
        "history_memory_contribution": memory_a,
        "counterfactual_memory_contribution": memory_b,
        "next_context_from_retained_history": next_a,
        "next_context_from_counterfactual_history": next_b,
        "same_present_signal": True,
        "histories_differ": history_effects != counterfactual_history_effects,
        "next_contexts_differ": next_a != next_b,
        "finite_non_markov_witness": (
            history_effects != counterfactual_history_effects and next_a != next_b
        ),
        "record_ledger_digest": ledger_digest,
        "temporal_cycle_digest": cycle_digest,
        "temporal_roles": {
            "planos_role": "future_possibility_ensemble",
            "decisionos_role": "present_relational_cut",
            "memoryos_role": "observer_relative_append_only_past",
            "observe_role": "event_to_record_channel",
        },
        "all_records_not_event_identity": all(
            item["record_not_event_identity"] for item in records
        ),
        "multiple_observer_event_count": sum(
            item["multiple_observer_records_retained"] for item in event_profile
        ),
        "history_erased": False,
        "observer_privileged": False,
    }
