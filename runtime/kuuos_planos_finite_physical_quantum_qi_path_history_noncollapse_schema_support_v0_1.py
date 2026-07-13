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


def _integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _unique_text(value: Any, seen: set[str], invalid: str, duplicate: str):
    if not _nonempty_text(value):
        return False, invalid
    if value in seen:
        return False, duplicate
    seen.add(value)
    return True, ""


def _normalize_integer_vector(
    value: Any,
    *,
    dimension: int,
    maximum_absolute_coordinate: int,
    error_prefix: str,
):
    if (
        not isinstance(value, list)
        or len(value) != dimension
        or any(
            not _integer(component)
            or abs(component) > maximum_absolute_coordinate
            for component in value
        )
    ):
        return [error_prefix + "_invalid"], []
    return [], list(value)


def normalize_states(
    values: Any,
    *,
    qi_dimension: int,
    maximum_state_count: int,
    maximum_absolute_qi_coordinate: int,
):
    if not isinstance(values, list) or not values:
        return ["state_set_empty"], []
    if len(values) > maximum_state_count:
        return ["maximum_state_count_exceeded"], []
    fields = {"state_id", "source_digest", "world_slice_digest", "qi_coordinate"}
    blockers: list[str] = []
    output: list[dict] = []
    seen: set[str] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"state_schema_invalid_{index}")
            continue
        state_id = item["state_id"]
        ok, reason = _unique_text(
            state_id,
            seen,
            f"state_id_invalid_{index}",
            "duplicate_state_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        if not _nonempty_text(item["source_digest"]):
            blockers.append(f"state_source_digest_missing_{state_id}")
        if not _nonempty_text(item["world_slice_digest"]):
            blockers.append(f"state_world_slice_digest_missing_{state_id}")
        vector_errors, vector = _normalize_integer_vector(
            item["qi_coordinate"],
            dimension=qi_dimension,
            maximum_absolute_coordinate=maximum_absolute_qi_coordinate,
            error_prefix=f"state_qi_coordinate_{state_id}",
        )
        blockers.extend(vector_errors)
        output.append(
            {
                "state_id": state_id,
                "source_digest": item["source_digest"],
                "world_slice_digest": item["world_slice_digest"],
                "qi_coordinate": vector,
            }
        )
    return blockers, sorted(output, key=lambda item: item["state_id"])


def normalize_transitions(
    values: Any,
    *,
    qi_dimension: int,
    maximum_transition_count: int,
    maximum_action_increment: int,
    maximum_absolute_qi_flux: int,
):
    if not isinstance(values, list) or not values:
        return ["transition_set_empty"], []
    if len(values) > maximum_transition_count:
        return ["maximum_transition_count_exceeded"], []
    fields = {
        "transition_id",
        "from_state_id",
        "to_state_id",
        "action_increment",
        "qi_flux_increment",
        "source_digest",
    }
    blockers: list[str] = []
    output: list[dict] = []
    seen: set[str] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"transition_schema_invalid_{index}")
            continue
        transition_id = item["transition_id"]
        ok, reason = _unique_text(
            transition_id,
            seen,
            f"transition_id_invalid_{index}",
            "duplicate_transition_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        for state_field in ("from_state_id", "to_state_id"):
            if not _nonempty_text(item[state_field]):
                blockers.append(f"{state_field}_invalid_{transition_id}")
        action = item["action_increment"]
        if not _nat(action) or action > maximum_action_increment:
            blockers.append(f"action_increment_invalid_{transition_id}")
        vector_errors, vector = _normalize_integer_vector(
            item["qi_flux_increment"],
            dimension=qi_dimension,
            maximum_absolute_coordinate=maximum_absolute_qi_flux,
            error_prefix=f"qi_flux_increment_{transition_id}",
        )
        blockers.extend(vector_errors)
        if not _nonempty_text(item["source_digest"]):
            blockers.append(f"transition_source_digest_missing_{transition_id}")
        output.append(
            {
                "transition_id": transition_id,
                "from_state_id": item["from_state_id"],
                "to_state_id": item["to_state_id"],
                "action_increment": action,
                "qi_flux_increment": vector,
                "source_digest": item["source_digest"],
            }
        )
    return blockers, sorted(output, key=lambda item: item["transition_id"])


def normalize_histories(
    values: Any,
    *,
    maximum_history_count: int,
    maximum_history_length: int,
):
    if not isinstance(values, list) or not values:
        return ["history_family_empty"], []
    if len(values) > maximum_history_count:
        return ["maximum_history_count_exceeded"], []
    fields = {
        "history_id",
        "scenario_id",
        "weight_numerator",
        "phase_mod2",
        "transition_ids",
        "source_plan_digest",
    }
    blockers: list[str] = []
    output: list[dict] = []
    seen: set[str] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"history_schema_invalid_{index}")
            continue
        history_id = item["history_id"]
        ok, reason = _unique_text(
            history_id,
            seen,
            f"history_id_invalid_{index}",
            "duplicate_history_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        if not _nonempty_text(item["scenario_id"]):
            blockers.append(f"scenario_id_invalid_{history_id}")
        if not _positive_nat(item["weight_numerator"]):
            blockers.append(f"history_weight_invalid_{history_id}")
        if item["phase_mod2"] not in (0, 1):
            blockers.append(f"history_phase_mod2_invalid_{history_id}")
        transition_ids = item["transition_ids"]
        if (
            not isinstance(transition_ids, list)
            or not transition_ids
            or len(transition_ids) > maximum_history_length
            or any(not _nonempty_text(value) for value in transition_ids)
        ):
            blockers.append(f"history_transition_sequence_invalid_{history_id}")
            transition_ids = []
        if not _nonempty_text(item["source_plan_digest"]):
            blockers.append(f"history_source_plan_digest_missing_{history_id}")
        output.append(
            {
                "history_id": history_id,
                "scenario_id": item["scenario_id"],
                "weight_numerator": item["weight_numerator"],
                "phase_mod2": item["phase_mod2"],
                "transition_ids": list(transition_ids),
                "source_plan_digest": item["source_plan_digest"],
            }
        )
    return blockers, sorted(output, key=lambda item: item["history_id"])


def normalize_claims(value: Any):
    fields = {
        "input_digest",
        "retained_history_ids",
        "history_count",
        "distinct_state_sequence_count",
        "partition_function_polynomial",
        "endpoint_interference_profile",
        "depth_state_marginals",
        "scenario_marginals",
        "branch_points",
        "reconvergence_points",
        "loop_history_ids",
        "pairwise_shared_prefix_profile",
        "all_histories_retained",
        "tree_assumption_required",
        "argmin_performed",
        "representative_history_selected",
        "history_ranking_performed",
        "history_pruning_performed",
        "activation_performed",
        "execution_permission",
        "source_v120_certificate_mutated",
        "source_path_homotopy_certificate_mutated",
        "persistent_world_state_mutated",
    }
    if not isinstance(value, dict) or set(value) != fields:
        return ["claims_schema_invalid"], {}
    return [], dict(value)


def compute_path_history_input_digest(**payload) -> str:
    return canonical_digest(payload)


__all__ = [
    "canonical_digest",
    "compute_path_history_input_digest",
    "normalize_claims",
    "normalize_histories",
    "normalize_states",
    "normalize_transitions",
]
