from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence

SCHEMA_VERSION = (
    "kuuos.memoryos.observer-relative-finite-window-qi-influence-"
    "planos-handoff-certificate.v0.1"
)
SOURCE_MEMORYOS_V040_SCHEMA_VERSION = (
    "kuuos.memoryos.observer-relative-non-markov-temporal-record-certificate.v0.1"
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
MAXIMUM_WINDOW_LENGTH = 64
MAXIMUM_ABSOLUTE_INTEGER = 1_000_000


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


def normalize_component_map(value: Any, field: str) -> dict[str, int]:
    if not isinstance(value, Mapping) or set(value) != set(COMPONENTS):
        raise ValueError(field + "_schema_invalid")
    return {component: _int(value[component], field + "_" + component) for component in COMPONENTS}


def normalize_source_memoryos_v040_receipt(value: Any) -> dict[str, Any]:
    fields = {
        "accepted",
        "schema_version",
        "certificate_digest",
        "record_ledger_digest",
        "temporal_cycle_digest",
        "retained_record_ids",
        "retained_record_digests",
        "retained_observer_ids",
        "retained_translation_ids",
        "finite_non_markov_witness",
    }
    if not isinstance(value, Mapping) or set(value) != fields:
        raise ValueError("source_memoryos_v040_receipt_schema_invalid")
    if value["accepted"] is not True:
        raise ValueError("source_memoryos_v040_not_accepted")
    if value["schema_version"] != SOURCE_MEMORYOS_V040_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v040_schema_version_invalid")
    record_ids = _unique_texts(
        value["retained_record_ids"],
        "source_memoryos_v040_retained_record_ids",
        maximum_count=MAXIMUM_RECORD_COUNT,
    )
    record_digests = _unique_texts(
        value["retained_record_digests"],
        "source_memoryos_v040_retained_record_digests",
        maximum_count=MAXIMUM_RECORD_COUNT,
    )
    if len(record_ids) != len(record_digests):
        raise ValueError("source_memoryos_v040_record_binding_length_mismatch")
    observer_ids = _unique_texts(
        value["retained_observer_ids"],
        "source_memoryos_v040_retained_observer_ids",
        maximum_count=64,
    )
    translation_ids_raw = _sequence(
        value["retained_translation_ids"],
        "source_memoryos_v040_retained_translation_ids",
    )
    if len(translation_ids_raw) > MAXIMUM_RECORD_COUNT:
        raise ValueError("source_memoryos_v040_retained_translation_ids_count_invalid")
    translation_ids: list[str] = []
    seen_translation_ids: set[str] = set()
    for row in translation_ids_raw:
        item = _text(row, "source_memoryos_v040_retained_translation_ids")
        if item in seen_translation_ids:
            raise ValueError(
                "source_memoryos_v040_retained_translation_ids_duplicate_" + item
            )
        seen_translation_ids.add(item)
        translation_ids.append(item)
    normalized = {
        "accepted": True,
        "schema_version": SOURCE_MEMORYOS_V040_SCHEMA_VERSION,
        "certificate_digest": _text(
            value["certificate_digest"], "source_memoryos_v040_certificate_digest"
        ),
        "record_ledger_digest": _text(
            value["record_ledger_digest"], "source_memoryos_v040_record_ledger_digest"
        ),
        "temporal_cycle_digest": _text(
            value["temporal_cycle_digest"], "source_memoryos_v040_temporal_cycle_digest"
        ),
        "retained_record_ids": record_ids,
        "retained_record_digests": record_digests,
        "retained_observer_ids": observer_ids,
        "retained_translation_ids": translation_ids,
        "finite_non_markov_witness": value["finite_non_markov_witness"] is True,
    }
    expected_ledger_digest = digest_object(
        {
            "record_digests": record_digests,
            "observer_ids": observer_ids,
            "translation_ids": translation_ids,
        }
    )
    if normalized["record_ledger_digest"] != expected_ledger_digest:
        raise ValueError("source_memoryos_v040_record_ledger_digest_invalid")
    if not normalized["finite_non_markov_witness"]:
        raise ValueError("source_memoryos_v040_non_markov_witness_required")
    return normalized


def normalize_source_planos_v123_receipt(value: Any) -> dict[str, Any]:
    fields = {
        "accepted",
        "schema_version",
        "input_digest",
        "retained_history_ids",
        "all_histories_retained",
        "history_pruning_performed",
        "history_ranking_performed",
        "representative_history_selected",
    }
    if not isinstance(value, Mapping) or set(value) != fields:
        raise ValueError("source_planos_v123_receipt_schema_invalid")
    if value["accepted"] is not True:
        raise ValueError("source_planos_v123_not_accepted")
    if value["schema_version"] != SOURCE_PLANOS_V123_SCHEMA_VERSION:
        raise ValueError("source_planos_v123_schema_version_invalid")
    history_ids = _unique_texts(
        value["retained_history_ids"],
        "source_planos_v123_retained_history_ids",
        maximum_count=MAXIMUM_HISTORY_COUNT,
    )
    if value["all_histories_retained"] is not True:
        raise ValueError("source_planos_v123_all_histories_required")
    if value["history_pruning_performed"] is not False:
        raise ValueError("source_planos_v123_history_pruning_forbidden")
    if value["history_ranking_performed"] is not False:
        raise ValueError("source_planos_v123_history_ranking_forbidden")
    if value["representative_history_selected"] is not False:
        raise ValueError("source_planos_v123_representative_selection_forbidden")
    return {
        "accepted": True,
        "schema_version": SOURCE_PLANOS_V123_SCHEMA_VERSION,
        "input_digest": _text(
            value["input_digest"], "source_planos_v123_input_digest"
        ),
        "retained_history_ids": history_ids,
        "all_histories_retained": True,
        "history_pruning_performed": False,
        "history_ranking_performed": False,
        "representative_history_selected": False,
    }


def normalize_history_projection_records(
    value: Any,
    *,
    source_record_ids: list[str],
    source_record_digests: list[str],
    source_observer_ids: list[str],
    source_translation_ids: list[str],
) -> list[dict[str, Any]]:
    fields = {
        "record_id",
        "record_digest",
        "observer_id",
        "event_digest",
        "sequence_index",
        "component_effects",
        "translation_residue_visible",
        "observation_backaction_visible",
    }
    rows = _sequence(value, "history_projection_records")
    if not rows or len(rows) > MAXIMUM_RECORD_COUNT:
        raise ValueError("history_projection_record_count_invalid")
    if len(rows) != len(source_record_ids):
        raise ValueError("history_projection_source_record_count_mismatch")
    output: list[dict[str, Any]] = []
    observer_set = set(source_observer_ids)
    visible_translation_count = 0
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping) or set(row) != fields:
            raise ValueError(f"history_projection_record_schema_invalid_{index}")
        record_id = _text(row["record_id"], "history_projection_record_id")
        record_digest = _text(row["record_digest"], "history_projection_record_digest")
        if record_id != source_record_ids[index]:
            raise ValueError("history_projection_record_id_binding_mismatch_" + record_id)
        if record_digest != source_record_digests[index]:
            raise ValueError("history_projection_record_digest_binding_mismatch_" + record_id)
        sequence_index = _nat(row["sequence_index"], "history_projection_sequence_index")
        if sequence_index != index:
            raise ValueError("history_projection_sequence_not_contiguous_" + record_id)
        observer_id = _text(row["observer_id"], "history_projection_observer_id")
        if observer_id not in observer_set:
            raise ValueError("history_projection_observer_not_source_bound_" + observer_id)
        effects = normalize_component_map(
            row["component_effects"], "history_projection_component_effects"
        )
        translation_visible = row["translation_residue_visible"] is True
        if translation_visible:
            visible_translation_count += 1
            if effects["residue"] == 0:
                raise ValueError("visible_translation_residue_component_zero_" + record_id)
        observation_visible = row["observation_backaction_visible"] is True
        if not observation_visible and effects["observation"] != 0:
            raise ValueError("observation_backaction_hidden_" + record_id)
        output.append(
            {
                "record_id": record_id,
                "record_digest": record_digest,
                "observer_id": observer_id,
                "event_digest": _text(row["event_digest"], "history_projection_event_digest"),
                "sequence_index": sequence_index,
                "component_effects": effects,
                "translation_residue_visible": translation_visible,
                "observation_backaction_visible": observation_visible,
            }
        )
    if source_translation_ids and visible_translation_count == 0:
        raise ValueError("source_translation_residue_not_projected")
    return output


def normalize_lag_weights(value: Any, *, window_length: int) -> list[int]:
    rows = _sequence(value, "lag_weights")
    if len(rows) != window_length:
        raise ValueError("lag_weight_window_length_mismatch")
    weights = [_nat(row, "lag_weight") for row in rows]
    if not any(weights):
        raise ValueError("lag_weights_all_zero")
    return weights


def normalize_candidate_couplings(
    value: Any,
    *,
    source_history_ids: list[str],
) -> list[dict[str, Any]]:
    fields = {"history_id", "base_action_numerator", "component_couplings"}
    rows = _sequence(value, "candidate_couplings")
    if not rows or len(rows) > MAXIMUM_HISTORY_COUNT:
        raise ValueError("candidate_coupling_count_invalid")
    by_id: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping) or set(row) != fields:
            raise ValueError(f"candidate_coupling_schema_invalid_{index}")
        history_id = _text(row["history_id"], "candidate_coupling_history_id")
        if history_id in by_id:
            raise ValueError("candidate_coupling_history_id_duplicate_" + history_id)
        by_id[history_id] = {
            "history_id": history_id,
            "base_action_numerator": _int(
                row["base_action_numerator"], "candidate_base_action_numerator"
            ),
            "component_couplings": normalize_component_map(
                row["component_couplings"], "candidate_component_couplings"
            ),
        }
    if set(by_id) != set(source_history_ids):
        raise ValueError("candidate_couplings_source_history_support_mismatch")
    return [by_id[history_id] for history_id in source_history_ids]


def compute_input_digest(**payload: Any) -> str:
    return digest_object(payload)


__all__ = [
    "COMPONENTS",
    "MAXIMUM_WINDOW_LENGTH",
    "SCHEMA_VERSION",
    "SOURCE_MEMORYOS_V040_SCHEMA_VERSION",
    "SOURCE_PLANOS_V123_SCHEMA_VERSION",
    "compute_input_digest",
    "digest_object",
    "normalize_candidate_couplings",
    "normalize_component_map",
    "normalize_history_projection_records",
    "normalize_lag_weights",
    "normalize_source_memoryos_v040_receipt",
    "normalize_source_planos_v123_receipt",
]
