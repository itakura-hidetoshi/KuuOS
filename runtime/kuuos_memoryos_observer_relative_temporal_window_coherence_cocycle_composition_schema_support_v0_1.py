from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence

SCHEMA_VERSION = (
    "kuuos.memoryos.observer-relative-temporal-window-coherence-cocycle-"
    "composition-certificate.v0.1"
)
SOURCE_MEMORYOS_V041_SCHEMA_VERSION = (
    "kuuos.memoryos.observer-relative-finite-window-qi-influence-"
    "planos-handoff-certificate.v0.1"
)
SOURCE_MEMORYOS_V042_SCHEMA_VERSION = (
    "kuuos.memoryos.observer-relative-non-markov-influence-conditioned-"
    "planos-coherence-kernel-certificate.v0.1"
)
SOURCE_PLANOS_V123_SCHEMA_VERSION = (
    "kuuos.planos.finite-physical-quantum-qi-coherence-kernel-"
    "partial-dephasing-certificate.v0.1"
)
COMPONENTS: tuple[str, ...] = (
    "body",
    "boundary",
    "leak",
    "observation",
    "holonomy",
    "recovery",
    "rollback",
    "lockin",
    "residue",
)
MAXIMUM_RECORD_COUNT = 128
MAXIMUM_HISTORY_COUNT = 128
MAXIMUM_SEGMENT_COUNT = 128
MAXIMUM_DEPHASING_STEP_COUNT = 64
MAXIMUM_ABSOLUTE_INTEGER = 10_000_000


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_object(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(field + "_invalid")
    return value


def _sequence(value: Any, field: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ValueError(field + "_invalid")
    return value


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(field + "_invalid")
    return value.strip()


def _digest_text(value: Any, field: str) -> str:
    text = _text(value, field)
    if len(text) < 8:
        raise ValueError(field + "_invalid")
    return text


def _bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(field + "_invalid")
    return value


def _integer(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(field + "_invalid")
    if abs(value) > MAXIMUM_ABSOLUTE_INTEGER:
        raise ValueError(field + "_out_of_range")
    return value


def _positive_integer(value: Any, field: str) -> int:
    integer = _integer(value, field)
    if integer <= 0:
        raise ValueError(field + "_invalid")
    return integer


def _nonnegative_integer(value: Any, field: str) -> int:
    integer = _integer(value, field)
    if integer < 0:
        raise ValueError(field + "_invalid")
    return integer


def _unique_text_list(value: Any, field: str, maximum: int) -> list[str]:
    items = [_text(item, field) for item in _sequence(value, field)]
    if not items or len(items) > maximum or len(items) != len(set(items)):
        raise ValueError(field + "_invalid")
    return items


def normalize_component_map(value: Any, field: str) -> dict[str, int]:
    mapping = _mapping(value, field)
    if set(mapping) != set(COMPONENTS):
        raise ValueError(field + "_component_support_mismatch")
    return {component: _integer(mapping[component], field + "_" + component) for component in COMPONENTS}


def normalize_projection_records(
    value: Any,
    *,
    source_record_ids: list[str],
    source_record_digests: list[str],
    source_observer_ids: list[str],
) -> list[dict[str, Any]]:
    rows = list(_sequence(value, "history_projection_records"))
    if not rows or len(rows) > MAXIMUM_RECORD_COUNT:
        raise ValueError("history_projection_records_invalid")
    if len(rows) != len(source_record_ids) or len(source_record_ids) != len(source_record_digests):
        raise ValueError("history_projection_source_support_mismatch")
    output: list[dict[str, Any]] = []
    for index, raw in enumerate(rows):
        row = _mapping(raw, "history_projection_record")
        record_id = _text(row.get("record_id"), "history_projection_record_id")
        record_digest = _digest_text(row.get("record_digest"), "history_projection_record_digest")
        observer_id = _text(row.get("observer_id"), "history_projection_observer_id")
        sequence_index = _nonnegative_integer(
            row.get("sequence_index"), "history_projection_sequence_index"
        )
        if record_id != source_record_ids[index]:
            raise ValueError("history_projection_record_id_binding_mismatch_" + record_id)
        if record_digest != source_record_digests[index]:
            raise ValueError("history_projection_record_digest_binding_mismatch_" + record_id)
        if observer_id not in source_observer_ids:
            raise ValueError("history_projection_observer_not_source_bound_" + observer_id)
        if sequence_index != index:
            raise ValueError("history_projection_sequence_not_contiguous_" + record_id)
        output.append(
            {
                "record_id": record_id,
                "record_digest": record_digest,
                "observer_id": observer_id,
                "event_digest": _digest_text(
                    row.get("event_digest"), "history_projection_event_digest"
                ),
                "sequence_index": sequence_index,
                "component_effects": normalize_component_map(
                    row.get("component_effects"), "history_projection_component_effects"
                ),
                "translation_residue_visible": _bool(
                    row.get("translation_residue_visible"),
                    "history_projection_translation_residue_visible",
                ),
                "observation_backaction_visible": _bool(
                    row.get("observation_backaction_visible"),
                    "history_projection_observation_backaction_visible",
                ),
            }
        )
    return output


def normalize_candidate_couplings(
    value: Any, *, source_history_ids: list[str]
) -> list[dict[str, Any]]:
    rows = list(_sequence(value, "candidate_couplings"))
    if len(rows) != len(source_history_ids):
        raise ValueError("candidate_couplings_source_history_support_mismatch")
    output: list[dict[str, Any]] = []
    for index, raw in enumerate(rows):
        row = _mapping(raw, "candidate_coupling")
        history_id = _text(row.get("history_id"), "candidate_coupling_history_id")
        if history_id != source_history_ids[index]:
            raise ValueError("candidate_coupling_order_mismatch_" + history_id)
        output.append(
            {
                "history_id": history_id,
                "base_action_numerator": _integer(
                    row.get("base_action_numerator"),
                    "candidate_coupling_base_action_numerator",
                ),
                "component_couplings": normalize_component_map(
                    row.get("component_couplings"), "candidate_component_couplings"
                ),
            }
        )
    return output


def normalize_candidate_influence_profile(
    value: Any, *, source_history_ids: list[str]
) -> list[dict[str, Any]]:
    rows = list(_sequence(value, "candidate_influence_profile"))
    if len(rows) != len(source_history_ids):
        raise ValueError("candidate_influence_profile_support_mismatch")
    output: list[dict[str, Any]] = []
    for index, raw in enumerate(rows):
        row = _mapping(raw, "candidate_influence_profile_item")
        history_id = _text(row.get("history_id"), "candidate_influence_history_id")
        if history_id != source_history_ids[index]:
            raise ValueError("candidate_influence_profile_order_mismatch_" + history_id)
        output.append(
            {
                "history_id": history_id,
                "base_action_numerator": _integer(
                    row.get("base_action_numerator"), "candidate_influence_base_action"
                ),
                "window_influence_numerator": _integer(
                    row.get("window_influence_numerator"), "candidate_window_influence"
                ),
                "tail_influence_numerator": _integer(
                    row.get("tail_influence_numerator"), "candidate_tail_influence"
                ),
                "total_history_influence_numerator": _integer(
                    row.get("total_history_influence_numerator"),
                    "candidate_total_history_influence",
                ),
                "conditioned_action_numerator": _integer(
                    row.get("conditioned_action_numerator"),
                    "candidate_conditioned_action",
                ),
                "window_only_action_numerator": _integer(
                    row.get("window_only_action_numerator"),
                    "candidate_window_only_action",
                ),
                "action_denominator": _positive_integer(
                    row.get("action_denominator"), "candidate_action_denominator"
                ),
                "support_retained": _bool(
                    row.get("support_retained"), "candidate_support_retained"
                ),
            }
        )
    return output


def normalize_source_memoryos_v041_receipt(value: Any) -> dict[str, Any]:
    row = _mapping(value, "source_memoryos_v041_receipt")
    if row.get("schema_version") != SOURCE_MEMORYOS_V041_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v041_schema_invalid")
    if row.get("accepted") is not True:
        raise ValueError("source_memoryos_v041_not_accepted")
    record_ids = _unique_text_list(
        row.get("retained_record_ids"), "source_memoryos_v041_retained_record_ids", MAXIMUM_RECORD_COUNT
    )
    record_digests = _unique_text_list(
        row.get("retained_record_digests"),
        "source_memoryos_v041_retained_record_digests",
        MAXIMUM_RECORD_COUNT,
    )
    observer_ids = _unique_text_list(
        row.get("retained_observer_ids"),
        "source_memoryos_v041_retained_observer_ids",
        MAXIMUM_RECORD_COUNT,
    )
    translation_ids = _unique_text_list(
        row.get("retained_translation_ids"),
        "source_memoryos_v041_retained_translation_ids",
        MAXIMUM_RECORD_COUNT,
    )
    history_ids = _unique_text_list(
        row.get("retained_history_ids"),
        "source_memoryos_v041_retained_history_ids",
        MAXIMUM_HISTORY_COUNT,
    )
    records = normalize_projection_records(
        row.get("history_projection_records"),
        source_record_ids=record_ids,
        source_record_digests=record_digests,
        source_observer_ids=observer_ids,
    )
    window_length = _positive_integer(
        row.get("window_length"), "source_memoryos_v041_window_length"
    )
    if window_length > len(records):
        raise ValueError("source_memoryos_v041_window_length_exceeds_record_count")
    lag_weights = [
        _nonnegative_integer(item, "source_memoryos_v041_lag_weight")
        for item in _sequence(row.get("lag_weights"), "source_memoryos_v041_lag_weights")
    ]
    if len(lag_weights) != window_length or not any(lag_weights):
        raise ValueError("source_memoryos_v041_lag_weights_invalid")
    couplings = normalize_candidate_couplings(
        row.get("candidate_couplings"), source_history_ids=history_ids
    )
    profile = normalize_candidate_influence_profile(
        row.get("candidate_influence_profile"), source_history_ids=history_ids
    )
    return {
        "accepted": True,
        "schema_version": SOURCE_MEMORYOS_V041_SCHEMA_VERSION,
        "certificate_digest": _digest_text(
            row.get("certificate_digest"), "source_memoryos_v041_certificate_digest"
        ),
        "input_digest": _digest_text(
            row.get("input_digest"), "source_memoryos_v041_input_digest"
        ),
        "influence_handoff_digest": _digest_text(
            row.get("influence_handoff_digest"),
            "source_memoryos_v041_influence_handoff_digest",
        ),
        "source_memoryos_v040_record_ledger_digest": _digest_text(
            row.get("source_memoryos_v040_record_ledger_digest"),
            "source_memoryos_v040_record_ledger_digest",
        ),
        "source_memoryos_v040_temporal_cycle_digest": _digest_text(
            row.get("source_memoryos_v040_temporal_cycle_digest"),
            "source_memoryos_v040_temporal_cycle_digest",
        ),
        "source_planos_v123_input_digest": _digest_text(
            row.get("source_planos_v123_input_digest"),
            "source_memoryos_v041_source_planos_v123_input_digest",
        ),
        "retained_record_ids": record_ids,
        "retained_record_digests": record_digests,
        "retained_observer_ids": observer_ids,
        "retained_translation_ids": translation_ids,
        "retained_history_ids": history_ids,
        "history_projection_records": records,
        "window_length": window_length,
        "lag_weights": lag_weights,
        "candidate_couplings": couplings,
        "candidate_influence_profile": profile,
        "action_denominator": _positive_integer(
            row.get("action_denominator"), "source_memoryos_v041_action_denominator"
        ),
        "all_planos_histories_retained": _bool(
            row.get("all_planos_histories_retained"),
            "source_memoryos_v041_all_planos_histories_retained",
        ),
        "history_pruning_performed": _bool(
            row.get("history_pruning_performed"),
            "source_memoryos_v041_history_pruning_performed",
        ),
        "history_ranking_performed": _bool(
            row.get("history_ranking_performed"),
            "source_memoryos_v041_history_ranking_performed",
        ),
        "representative_history_selected": _bool(
            row.get("representative_history_selected"),
            "source_memoryos_v041_representative_history_selected",
        ),
        "plan_selection_performed": _bool(
            row.get("plan_selection_performed"),
            "source_memoryos_v041_plan_selection_performed",
        ),
        "activation_performed": _bool(
            row.get("activation_performed"),
            "source_memoryos_v041_activation_performed",
        ),
        "execution_permission": _bool(
            row.get("execution_permission"),
            "source_memoryos_v041_execution_permission",
        ),
    }


def normalize_kernel_entries(value: Any, *, history_ids: list[str], field: str) -> list[dict[str, Any]]:
    rows = list(_sequence(value, field))
    expected_count = len(history_ids) * len(history_ids)
    if len(rows) != expected_count:
        raise ValueError(field + "_support_count_invalid")
    output: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for raw in rows:
        row = _mapping(raw, field + "_entry")
        row_id = _text(row.get("row_history_id"), field + "_row_history_id")
        column_id = _text(row.get("column_history_id"), field + "_column_history_id")
        if row_id not in history_ids or column_id not in history_ids:
            raise ValueError(field + "_history_not_retained")
        pair = row_id, column_id
        if pair in seen:
            raise ValueError(field + "_duplicate_pair")
        seen.add(pair)
        output.append(
            {
                "row_history_id": row_id,
                "column_history_id": column_id,
                "real_numerator": _integer(row.get("real_numerator"), field + "_real_numerator"),
                "imag_numerator": _integer(row.get("imag_numerator"), field + "_imag_numerator"),
            }
        )
    expected_pairs = {(row_id, column_id) for row_id in history_ids for column_id in history_ids}
    if seen != expected_pairs:
        raise ValueError(field + "_pair_support_mismatch")
    return output


def normalize_kernel_trajectory(
    value: Any, *, history_ids: list[str], field: str
) -> list[dict[str, Any]]:
    rows = list(_sequence(value, field))
    if not rows or len(rows) > MAXIMUM_DEPHASING_STEP_COUNT:
        raise ValueError(field + "_invalid")
    output: list[dict[str, Any]] = []
    for index, raw in enumerate(rows):
        row = _mapping(raw, field + "_step")
        output.append(
            {
                "dephasing_numerator": _nonnegative_integer(
                    row.get("dephasing_numerator"), field + "_dephasing_numerator"
                ),
                "kernel_entry_denominator": _positive_integer(
                    row.get("kernel_entry_denominator"), field + "_kernel_entry_denominator"
                ),
                "kernel_hermitian": _bool(
                    row.get("kernel_hermitian"), field + "_kernel_hermitian"
                ),
                "diagonal_normalization_preserved": _bool(
                    row.get("diagonal_normalization_preserved", True),
                    field + "_diagonal_normalization_preserved",
                ),
                "positive_semidefinite_by_diagonal_phase_congruence": _bool(
                    row.get(
                        "positive_semidefinite_by_diagonal_phase_congruence",
                        row.get("positive_semidefinite_by_convex_gram_construction"),
                    ),
                    field + "_positive_semidefinite",
                ),
                "kernel_entries": normalize_kernel_entries(
                    row.get("kernel_entries"), history_ids=history_ids, field=field + f"_{index}"
                ),
            }
        )
    return output


def normalize_source_planos_v123_kernel_receipt(value: Any) -> dict[str, Any]:
    row = _mapping(value, "source_planos_v123_kernel_receipt")
    if row.get("schema_version") != SOURCE_PLANOS_V123_SCHEMA_VERSION:
        raise ValueError("source_planos_v123_schema_invalid")
    if row.get("accepted") is not True:
        raise ValueError("source_planos_v123_not_accepted")
    history_ids = _unique_text_list(
        row.get("retained_history_ids"),
        "source_planos_v123_retained_history_ids",
        MAXIMUM_HISTORY_COUNT,
    )
    trajectory = normalize_kernel_trajectory(
        row.get("partial_dephasing_trajectory"),
        history_ids=history_ids,
        field="source_planos_v123_trajectory",
    )
    numerators = [
        _nonnegative_integer(item, "source_planos_v123_dephasing_numerator")
        for item in _sequence(row.get("dephasing_numerators"), "source_planos_v123_dephasing_numerators")
    ]
    if numerators != [step["dephasing_numerator"] for step in trajectory]:
        raise ValueError("source_planos_v123_dephasing_trajectory_order_mismatch")
    return {
        "accepted": True,
        "schema_version": SOURCE_PLANOS_V123_SCHEMA_VERSION,
        "input_digest": _digest_text(row.get("input_digest"), "source_planos_v123_input_digest"),
        "retained_history_ids": history_ids,
        "dephasing_denominator": _positive_integer(
            row.get("dephasing_denominator"), "source_planos_v123_dephasing_denominator"
        ),
        "dephasing_numerators": numerators,
        "partial_dephasing_trajectory": trajectory,
        "all_histories_retained": _bool(
            row.get("all_histories_retained"), "source_planos_v123_all_histories_retained"
        ),
        "history_pruning_performed": _bool(
            row.get("history_pruning_performed"), "source_planos_v123_history_pruning_performed"
        ),
        "history_ranking_performed": _bool(
            row.get("history_ranking_performed"), "source_planos_v123_history_ranking_performed"
        ),
        "representative_history_selected": _bool(
            row.get("representative_history_selected"),
            "source_planos_v123_representative_history_selected",
        ),
    }


def normalize_source_memoryos_v042_receipt(value: Any) -> dict[str, Any]:
    row = _mapping(value, "source_memoryos_v042_receipt")
    if row.get("schema_version") != SOURCE_MEMORYOS_V042_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v042_schema_invalid")
    if row.get("accepted") is not True:
        raise ValueError("source_memoryos_v042_not_accepted")
    history_ids = _unique_text_list(
        row.get("retained_history_ids"),
        "source_memoryos_v042_retained_history_ids",
        MAXIMUM_HISTORY_COUNT,
    )
    trajectory = normalize_kernel_trajectory(
        row.get("full_memory_conditioned_trajectory"),
        history_ids=history_ids,
        field="source_memoryos_v042_conditioned_trajectory",
    )
    conditioned_digest = _digest_text(
        row.get("conditioned_kernel_digest"), "source_memoryos_v042_conditioned_kernel_digest"
    )
    if conditioned_digest != digest_object(trajectory):
        raise ValueError("source_memoryos_v042_conditioned_kernel_digest_invalid")
    return {
        "accepted": True,
        "schema_version": SOURCE_MEMORYOS_V042_SCHEMA_VERSION,
        "certificate_digest": _digest_text(
            row.get("certificate_digest"), "source_memoryos_v042_certificate_digest"
        ),
        "input_digest": _digest_text(row.get("input_digest"), "source_memoryos_v042_input_digest"),
        "source_memoryos_v041_certificate_digest": _digest_text(
            row.get("source_memoryos_v041_certificate_digest"),
            "source_memoryos_v042_source_memoryos_v041_certificate_digest",
        ),
        "source_memoryos_v041_influence_handoff_digest": _digest_text(
            row.get("source_memoryos_v041_influence_handoff_digest"),
            "source_memoryos_v042_source_memoryos_v041_influence_handoff_digest",
        ),
        "source_planos_v123_input_digest": _digest_text(
            row.get("source_planos_v123_input_digest"),
            "source_memoryos_v042_source_planos_v123_input_digest",
        ),
        "retained_history_ids": history_ids,
        "source_kernel_digest": _digest_text(
            row.get("source_kernel_digest"), "source_memoryos_v042_source_kernel_digest"
        ),
        "conditioned_kernel_digest": conditioned_digest,
        "full_memory_conditioned_trajectory": trajectory,
        "all_conditioned_steps_hermitian": _bool(
            row.get("all_conditioned_steps_hermitian"),
            "source_memoryos_v042_all_conditioned_steps_hermitian",
        ),
        "all_diagonals_preserved": _bool(
            row.get("all_diagonals_preserved"),
            "source_memoryos_v042_all_diagonals_preserved",
        ),
        "all_steps_psd_by_diagonal_phase_congruence": _bool(
            row.get("all_steps_psd_by_diagonal_phase_congruence"),
            "source_memoryos_v042_all_steps_psd",
        ),
        "all_history_pair_support_retained": _bool(
            row.get("all_history_pair_support_retained"),
            "source_memoryos_v042_all_history_pair_support_retained",
        ),
        "amplitude_reweighting_performed": _bool(
            row.get("amplitude_reweighting_performed"),
            "source_memoryos_v042_amplitude_reweighting_performed",
        ),
        "kernel_entry_deletion_performed": _bool(
            row.get("kernel_entry_deletion_performed"),
            "source_memoryos_v042_kernel_entry_deletion_performed",
        ),
    }


def normalize_temporal_segments(
    value: Any,
    *,
    source_record_ids: list[str],
    source_observer_ids: list[str],
    source_translation_ids: list[str],
) -> list[dict[str, Any]]:
    rows = list(_sequence(value, "temporal_segments"))
    if not rows or len(rows) > MAXIMUM_SEGMENT_COUNT:
        raise ValueError("temporal_segments_invalid")
    output: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for raw in rows:
        row = _mapping(raw, "temporal_segment")
        segment_id = _text(row.get("segment_id"), "temporal_segment_id")
        if segment_id in seen_ids:
            raise ValueError("temporal_segment_id_duplicate_" + segment_id)
        seen_ids.add(segment_id)
        kind = _text(row.get("segment_kind"), "temporal_segment_kind")
        if kind not in {"discarded-tail", "retained-window"}:
            raise ValueError("temporal_segment_kind_invalid_" + segment_id)
        record_ids = _unique_text_list(
            row.get("record_ids"), "temporal_segment_record_ids", MAXIMUM_RECORD_COUNT
        )
        if any(record_id not in source_record_ids for record_id in record_ids):
            raise ValueError("temporal_segment_record_not_source_bound_" + segment_id)
        observer_id = _text(row.get("observer_id"), "temporal_segment_observer_id")
        if observer_id not in source_observer_ids:
            raise ValueError("temporal_segment_observer_not_source_bound_" + observer_id)
        translation_id_raw = row.get("translation_from_previous_id")
        translation_id: str | None
        if translation_id_raw is None:
            translation_id = None
        else:
            translation_id = _text(
                translation_id_raw, "temporal_segment_translation_from_previous_id"
            )
            if translation_id not in source_translation_ids:
                raise ValueError("temporal_segment_translation_not_source_bound_" + translation_id)
        output.append(
            {
                "segment_id": segment_id,
                "segment_kind": kind,
                "record_ids": record_ids,
                "observer_id": observer_id,
                "lag_weight": _positive_integer(
                    row.get("lag_weight"), "temporal_segment_lag_weight"
                ),
                "source_sequence_start": _nonnegative_integer(
                    row.get("source_sequence_start"),
                    "temporal_segment_source_sequence_start",
                ),
                "source_sequence_end": _nonnegative_integer(
                    row.get("source_sequence_end"),
                    "temporal_segment_source_sequence_end",
                ),
                "translation_from_previous_id": translation_id,
                "translation_residue_visible": _bool(
                    row.get("translation_residue_visible"),
                    "temporal_segment_translation_residue_visible",
                ),
            }
        )
    return output


def compute_input_digest(
    *,
    source_memoryos_v041_receipt: dict[str, Any],
    source_memoryos_v042_receipt: dict[str, Any],
    source_planos_v123_kernel_receipt: dict[str, Any],
    temporal_segments: list[dict[str, Any]],
) -> str:
    return digest_object(
        {
            "source_memoryos_v041_receipt": source_memoryos_v041_receipt,
            "source_memoryos_v042_receipt": source_memoryos_v042_receipt,
            "source_planos_v123_kernel_receipt": source_planos_v123_kernel_receipt,
            "temporal_segments": temporal_segments,
        }
    )


__all__ = [
    "COMPONENTS",
    "SCHEMA_VERSION",
    "SOURCE_MEMORYOS_V041_SCHEMA_VERSION",
    "SOURCE_MEMORYOS_V042_SCHEMA_VERSION",
    "SOURCE_PLANOS_V123_SCHEMA_VERSION",
    "compute_input_digest",
    "digest_object",
    "normalize_component_map",
    "normalize_source_memoryos_v041_receipt",
    "normalize_source_memoryos_v042_receipt",
    "normalize_source_planos_v123_kernel_receipt",
    "normalize_temporal_segments",
]
