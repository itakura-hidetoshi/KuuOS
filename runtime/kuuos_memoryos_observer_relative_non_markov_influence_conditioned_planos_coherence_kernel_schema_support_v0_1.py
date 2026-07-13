from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence

SCHEMA_VERSION = (
    "kuuos.memoryos.observer-relative-non-markov-influence-conditioned-"
    "planos-coherence-kernel-certificate.v0.1"
)
SOURCE_MEMORYOS_V041_SCHEMA_VERSION = (
    "kuuos.memoryos.observer-relative-finite-window-qi-influence-"
    "planos-handoff-certificate.v0.1"
)
SOURCE_PLANOS_V123_SCHEMA_VERSION = (
    "kuuos.planos.finite-physical-quantum-qi-coherence-kernel-"
    "partial-dephasing-certificate.v0.1"
)
MAXIMUM_HISTORY_COUNT = 128
MAXIMUM_DEPHASING_STEP_COUNT = 64
MAXIMUM_ABSOLUTE_INTEGER = 10_000_000


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_object(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(field + "_invalid")
    return value.strip()


def _int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(field + "_invalid")
    if abs(value) > MAXIMUM_ABSOLUTE_INTEGER:
        raise ValueError(field + "_magnitude_exceeded")
    return value


def _nat(value: Any, field: str) -> int:
    result = _int(value, field)
    if result < 0:
        raise ValueError(field + "_invalid")
    return result


def _positive_nat(value: Any, field: str) -> int:
    result = _nat(value, field)
    if result == 0:
        raise ValueError(field + "_invalid")
    return result


def _sequence(value: Any, field: str) -> list[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(field + "_invalid")
    return list(value)


def _unique_texts(value: Any, field: str, *, maximum_count: int) -> list[str]:
    rows = _sequence(value, field)
    if not rows or len(rows) > maximum_count:
        raise ValueError(field + "_count_invalid")
    output: list[str] = []
    seen: set[str] = set()
    for row in rows:
        item = _text(row, field)
        if item in seen:
            raise ValueError(field + "_duplicate_" + item)
        seen.add(item)
        output.append(item)
    return output


def normalize_source_memoryos_v041_receipt(value: Any) -> dict[str, Any]:
    fields = {
        "accepted",
        "schema_version",
        "certificate_digest",
        "input_digest",
        "influence_handoff_digest",
        "source_planos_v123_input_digest",
        "retained_history_ids",
        "candidate_influence_profile",
        "all_planos_histories_retained",
        "history_pruning_performed",
        "history_ranking_performed",
        "representative_history_selected",
        "plan_selection_performed",
        "activation_performed",
        "execution_permission",
    }
    if not isinstance(value, Mapping) or set(value) != fields:
        raise ValueError("source_memoryos_v041_receipt_schema_invalid")
    if value["accepted"] is not True:
        raise ValueError("source_memoryos_v041_not_accepted")
    if value["schema_version"] != SOURCE_MEMORYOS_V041_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v041_schema_version_invalid")
    history_ids = _unique_texts(
        value["retained_history_ids"],
        "source_memoryos_v041_retained_history_ids",
        maximum_count=MAXIMUM_HISTORY_COUNT,
    )
    profile_rows = _sequence(
        value["candidate_influence_profile"],
        "source_memoryos_v041_candidate_influence_profile",
    )
    if len(profile_rows) != len(history_ids):
        raise ValueError("source_memoryos_v041_candidate_profile_count_mismatch")
    profile_fields = {
        "history_id",
        "base_action_numerator",
        "window_influence_numerator",
        "tail_influence_numerator",
        "total_history_influence_numerator",
        "conditioned_action_numerator",
        "window_only_action_numerator",
        "action_denominator",
        "support_retained",
    }
    by_id: dict[str, dict[str, Any]] = {}
    common_denominator: int | None = None
    for index, row in enumerate(profile_rows):
        if not isinstance(row, Mapping) or set(row) != profile_fields:
            raise ValueError(f"source_memoryos_v041_candidate_profile_schema_invalid_{index}")
        history_id = _text(row["history_id"], "source_memoryos_v041_history_id")
        if history_id in by_id:
            raise ValueError("source_memoryos_v041_history_id_duplicate_" + history_id)
        base = _int(row["base_action_numerator"], "source_memoryos_v041_base_action")
        window = _int(row["window_influence_numerator"], "source_memoryos_v041_window_influence")
        tail = _int(row["tail_influence_numerator"], "source_memoryos_v041_tail_influence")
        total = _int(row["total_history_influence_numerator"], "source_memoryos_v041_total_influence")
        conditioned = _int(row["conditioned_action_numerator"], "source_memoryos_v041_conditioned_action")
        window_only = _int(row["window_only_action_numerator"], "source_memoryos_v041_window_only_action")
        denominator = _positive_nat(row["action_denominator"], "source_memoryos_v041_action_denominator")
        if common_denominator is None:
            common_denominator = denominator
        elif denominator != common_denominator:
            raise ValueError("source_memoryos_v041_action_denominator_mismatch")
        if total != window + tail:
            raise ValueError("source_memoryos_v041_total_influence_identity_invalid_" + history_id)
        if conditioned != base + total:
            raise ValueError("source_memoryos_v041_conditioned_action_identity_invalid_" + history_id)
        if window_only != base + window:
            raise ValueError("source_memoryos_v041_window_only_action_identity_invalid_" + history_id)
        if conditioned - window_only != tail:
            raise ValueError("source_memoryos_v041_tail_difference_identity_invalid_" + history_id)
        if row["support_retained"] is not True:
            raise ValueError("source_memoryos_v041_support_not_retained_" + history_id)
        by_id[history_id] = {
            "history_id": history_id,
            "base_action_numerator": base,
            "window_influence_numerator": window,
            "tail_influence_numerator": tail,
            "total_history_influence_numerator": total,
            "conditioned_action_numerator": conditioned,
            "window_only_action_numerator": window_only,
            "action_denominator": denominator,
            "support_retained": True,
        }
    if set(by_id) != set(history_ids):
        raise ValueError("source_memoryos_v041_candidate_profile_support_mismatch")
    for field in (
        "all_planos_histories_retained",
        "history_pruning_performed",
        "history_ranking_performed",
        "representative_history_selected",
        "plan_selection_performed",
        "activation_performed",
        "execution_permission",
    ):
        expected = field == "all_planos_histories_retained"
        if value[field] is not expected:
            raise ValueError("source_memoryos_v041_governance_invalid_" + field)
    return {
        "accepted": True,
        "schema_version": SOURCE_MEMORYOS_V041_SCHEMA_VERSION,
        "certificate_digest": _text(value["certificate_digest"], "source_memoryos_v041_certificate_digest"),
        "input_digest": _text(value["input_digest"], "source_memoryos_v041_input_digest"),
        "influence_handoff_digest": _text(value["influence_handoff_digest"], "source_memoryos_v041_influence_handoff_digest"),
        "source_planos_v123_input_digest": _text(
            value["source_planos_v123_input_digest"],
            "source_memoryos_v041_source_planos_v123_input_digest",
        ),
        "retained_history_ids": history_ids,
        "candidate_influence_profile": [by_id[history_id] for history_id in history_ids],
        "action_denominator": common_denominator,
        "all_planos_histories_retained": True,
        "history_pruning_performed": False,
        "history_ranking_performed": False,
        "representative_history_selected": False,
        "plan_selection_performed": False,
        "activation_performed": False,
        "execution_permission": False,
    }


def _normalize_kernel_entries(value: Any, history_ids: list[str], step_index: int) -> list[dict[str, Any]]:
    rows = _sequence(value, f"source_planos_v123_kernel_entries_{step_index}")
    expected_count = len(history_ids) * len(history_ids)
    if len(rows) != expected_count:
        raise ValueError(f"source_planos_v123_kernel_support_count_invalid_{step_index}")
    fields = {"row_history_id", "column_history_id", "real_numerator", "imag_numerator"}
    by_pair: dict[tuple[str, str], dict[str, Any]] = {}
    history_set = set(history_ids)
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping) or set(row) != fields:
            raise ValueError(f"source_planos_v123_kernel_entry_schema_invalid_{step_index}_{index}")
        row_id = _text(row["row_history_id"], "source_planos_v123_kernel_row_history_id")
        column_id = _text(row["column_history_id"], "source_planos_v123_kernel_column_history_id")
        if row_id not in history_set or column_id not in history_set:
            raise ValueError("source_planos_v123_kernel_history_not_bound")
        pair = (row_id, column_id)
        if pair in by_pair:
            raise ValueError("source_planos_v123_kernel_pair_duplicate_" + row_id + "_" + column_id)
        by_pair[pair] = {
            "row_history_id": row_id,
            "column_history_id": column_id,
            "real_numerator": _int(row["real_numerator"], "source_planos_v123_kernel_real_numerator"),
            "imag_numerator": _int(row["imag_numerator"], "source_planos_v123_kernel_imag_numerator"),
        }
    expected_pairs = {(row_id, column_id) for row_id in history_ids for column_id in history_ids}
    if set(by_pair) != expected_pairs:
        raise ValueError(f"source_planos_v123_kernel_support_mismatch_{step_index}")
    for row_id in history_ids:
        for column_id in history_ids:
            entry = by_pair[(row_id, column_id)]
            reverse = by_pair[(column_id, row_id)]
            if entry["real_numerator"] != reverse["real_numerator"] or entry["imag_numerator"] != -reverse["imag_numerator"]:
                raise ValueError(f"source_planos_v123_kernel_not_hermitian_{step_index}_{row_id}_{column_id}")
        if by_pair[(row_id, row_id)]["imag_numerator"] != 0:
            raise ValueError(f"source_planos_v123_kernel_diagonal_not_real_{step_index}_{row_id}")
    return [by_pair[(row_id, column_id)] for row_id in history_ids for column_id in history_ids]


def normalize_source_planos_v123_kernel_receipt(value: Any) -> dict[str, Any]:
    fields = {
        "accepted",
        "schema_version",
        "input_digest",
        "retained_history_ids",
        "dephasing_denominator",
        "dephasing_numerators",
        "partial_dephasing_trajectory",
        "all_histories_retained",
        "history_pruning_performed",
        "history_ranking_performed",
        "representative_history_selected",
    }
    if not isinstance(value, Mapping) or set(value) != fields:
        raise ValueError("source_planos_v123_kernel_receipt_schema_invalid")
    if value["accepted"] is not True:
        raise ValueError("source_planos_v123_kernel_not_accepted")
    if value["schema_version"] != SOURCE_PLANOS_V123_SCHEMA_VERSION:
        raise ValueError("source_planos_v123_kernel_schema_version_invalid")
    history_ids = _unique_texts(
        value["retained_history_ids"],
        "source_planos_v123_kernel_retained_history_ids",
        maximum_count=MAXIMUM_HISTORY_COUNT,
    )
    denominator = _positive_nat(value["dephasing_denominator"], "source_planos_v123_dephasing_denominator")
    numerators_raw = _sequence(value["dephasing_numerators"], "source_planos_v123_dephasing_numerators")
    if not numerators_raw or len(numerators_raw) > MAXIMUM_DEPHASING_STEP_COUNT:
        raise ValueError("source_planos_v123_dephasing_numerator_count_invalid")
    numerators = [_nat(row, "source_planos_v123_dephasing_numerator") for row in numerators_raw]
    if any(row > denominator for row in numerators):
        raise ValueError("source_planos_v123_dephasing_numerator_out_of_range")
    if any(left <= right for left, right in zip(numerators, numerators[1:])):
        raise ValueError("source_planos_v123_dephasing_numerators_not_strictly_decreasing")
    trajectory_rows = _sequence(value["partial_dephasing_trajectory"], "source_planos_v123_partial_dephasing_trajectory")
    if len(trajectory_rows) != len(numerators):
        raise ValueError("source_planos_v123_trajectory_length_mismatch")
    step_fields = {
        "dephasing_numerator",
        "kernel_entry_denominator",
        "kernel_hermitian",
        "positive_semidefinite_by_convex_gram_construction",
        "kernel_entries",
    }
    trajectory: list[dict[str, Any]] = []
    for index, (row, numerator) in enumerate(zip(trajectory_rows, numerators)):
        if not isinstance(row, Mapping) or set(row) != step_fields:
            raise ValueError(f"source_planos_v123_trajectory_schema_invalid_{index}")
        if _nat(row["dephasing_numerator"], "source_planos_v123_step_numerator") != numerator:
            raise ValueError(f"source_planos_v123_step_numerator_mismatch_{index}")
        if _positive_nat(row["kernel_entry_denominator"], "source_planos_v123_kernel_entry_denominator") != denominator:
            raise ValueError(f"source_planos_v123_kernel_entry_denominator_mismatch_{index}")
        if row["kernel_hermitian"] is not True:
            raise ValueError(f"source_planos_v123_kernel_hermitian_witness_required_{index}")
        if row["positive_semidefinite_by_convex_gram_construction"] is not True:
            raise ValueError(f"source_planos_v123_psd_witness_required_{index}")
        entries = _normalize_kernel_entries(row["kernel_entries"], history_ids, index)
        trajectory.append(
            {
                "dephasing_numerator": numerator,
                "kernel_entry_denominator": denominator,
                "kernel_hermitian": True,
                "positive_semidefinite_by_convex_gram_construction": True,
                "kernel_entries": entries,
            }
        )
    if value["all_histories_retained"] is not True:
        raise ValueError("source_planos_v123_all_histories_required")
    for field in (
        "history_pruning_performed",
        "history_ranking_performed",
        "representative_history_selected",
    ):
        if value[field] is not False:
            raise ValueError("source_planos_v123_governance_invalid_" + field)
    return {
        "accepted": True,
        "schema_version": SOURCE_PLANOS_V123_SCHEMA_VERSION,
        "input_digest": _text(value["input_digest"], "source_planos_v123_input_digest"),
        "retained_history_ids": history_ids,
        "dephasing_denominator": denominator,
        "dephasing_numerators": numerators,
        "partial_dephasing_trajectory": trajectory,
        "all_histories_retained": True,
        "history_pruning_performed": False,
        "history_ranking_performed": False,
        "representative_history_selected": False,
    }


def compute_input_digest(**payload: Any) -> str:
    return digest_object(payload)


__all__ = [
    "SCHEMA_VERSION",
    "SOURCE_MEMORYOS_V041_SCHEMA_VERSION",
    "SOURCE_PLANOS_V123_SCHEMA_VERSION",
    "compute_input_digest",
    "digest_object",
    "normalize_source_memoryos_v041_receipt",
    "normalize_source_planos_v123_kernel_receipt",
]
