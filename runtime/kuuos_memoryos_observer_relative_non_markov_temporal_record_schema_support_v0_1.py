from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence

SCHEMA_VERSION = (
    "kuuos.memoryos.observer-relative-non-markov-temporal-record-certificate.v0.1"
)
ZERO_DIGEST = "0" * 64


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
    return value


def _nat(value: Any, field: str) -> int:
    result = _int(value, field)
    if result < 0:
        raise ValueError(field + "_invalid")
    return result


def _sequence(value: Any, field: str) -> list[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(field + "_invalid")
    return list(value)


def normalize_observers(value: Any, *, maximum_count: int = 64) -> list[dict[str, Any]]:
    rows = _sequence(value, "observers")
    if not rows or len(rows) > maximum_count:
        raise ValueError("observer_count_invalid")
    output: list[dict[str, Any]] = []
    ids: set[str] = set()
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("observer_row_invalid")
        observer_id = _text(row.get("observer_id"), "observer_id")
        if observer_id in ids:
            raise ValueError("observer_id_duplicate_" + observer_id)
        ids.add(observer_id)
        output.append(
            {
                "observer_id": observer_id,
                "observer_frame_digest": _text(
                    row.get("observer_frame_digest"), "observer_frame_digest"
                ),
                "instrument_family_digest": _text(
                    row.get("instrument_family_digest"), "instrument_family_digest"
                ),
                "observation_chart_digest": _text(
                    row.get("observation_chart_digest"), "observation_chart_digest"
                ),
                "absolute_observer": row.get("absolute_observer") is True,
            }
        )
    return sorted(output, key=lambda item: item["observer_id"])


_RECORD_TEXT_FIELDS = (
    "observer_id",
    "event_digest",
    "plan_future_ensemble_digest",
    "decision_present_cut_digest",
    "observation_operator_digest",
    "instrument_trace_digest",
    "pre_observer_state_digest",
    "post_observer_state_digest",
    "pre_world_state_digest",
    "post_world_state_digest",
    "backaction_digest",
    "residue_digest",
    "source_memoryos_v039_capsule_digest",
)


def _record_core(row: Mapping[str, Any], sequence_index: int, previous_digest: str) -> dict[str, Any]:
    record_id = _text(row.get("record_id"), "record_id")
    normalized: dict[str, Any] = {
        "record_id": record_id,
        "sequence_index": sequence_index,
        "previous_record_digest": previous_digest,
    }
    for field in _RECORD_TEXT_FIELDS:
        normalized[field] = _text(row.get(field), field)
    normalized["observation_value"] = _int(row.get("observation_value"), "observation_value")
    normalized["history_effect"] = _int(row.get("history_effect"), "history_effect")
    normalized["uncertainty_numerator"] = _nat(
        row.get("uncertainty_numerator"), "uncertainty_numerator"
    )
    normalized["uncertainty_denominator"] = _nat(
        row.get("uncertainty_denominator"), "uncertainty_denominator"
    )
    if normalized["uncertainty_denominator"] == 0:
        raise ValueError("uncertainty_denominator_zero_" + record_id)
    normalized["record_not_event_identity"] = (
        row.get("record_not_event_identity") is True
    )
    normalized["observer_changed_by_observation"] = (
        normalized["pre_observer_state_digest"]
        != normalized["post_observer_state_digest"]
    )
    normalized["world_changed_or_backaction_visible"] = (
        normalized["pre_world_state_digest"] != normalized["post_world_state_digest"]
        or normalized["backaction_digest"] != ZERO_DIGEST
    )
    normalized["record_digest"] = digest_object(normalized)
    return normalized


def build_record_chain(value: Any, *, maximum_count: int = 256) -> list[dict[str, Any]]:
    rows = _sequence(value, "records")
    if not rows or len(rows) > maximum_count:
        raise ValueError("record_count_invalid")
    output: list[dict[str, Any]] = []
    ids: set[str] = set()
    previous = ZERO_DIGEST
    for expected_index, row in enumerate(rows):
        if not isinstance(row, Mapping):
            raise ValueError("record_row_invalid")
        record_id = _text(row.get("record_id"), "record_id")
        if record_id in ids:
            raise ValueError("record_id_duplicate_" + record_id)
        ids.add(record_id)
        supplied_index = row.get("sequence_index", expected_index)
        if supplied_index != expected_index:
            raise ValueError("record_sequence_invalid_" + record_id)
        supplied_previous = row.get("previous_record_digest", previous)
        if supplied_previous != previous:
            raise ValueError("record_previous_digest_invalid_" + record_id)
        normalized = _record_core(row, expected_index, previous)
        supplied_digest = row.get("record_digest")
        if supplied_digest not in (None, "") and supplied_digest != normalized["record_digest"]:
            raise ValueError("record_digest_invalid_" + record_id)
        output.append(normalized)
        previous = normalized["record_digest"]
    return output


def normalize_translations(value: Any, *, maximum_count: int = 256) -> list[dict[str, Any]]:
    rows = _sequence(value, "translations")
    if len(rows) > maximum_count:
        raise ValueError("translation_count_invalid")
    output: list[dict[str, Any]] = []
    ids: set[str] = set()
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("translation_row_invalid")
        translation_id = _text(row.get("translation_id"), "translation_id")
        if translation_id in ids:
            raise ValueError("translation_id_duplicate_" + translation_id)
        ids.add(translation_id)
        source_value = _int(row.get("source_value"), "source_value")
        target_value = _int(row.get("target_value"), "target_value")
        offset = _int(row.get("offset_integer"), "offset_integer")
        translated = source_value + offset
        residue = target_value - translated
        supplied_translated = row.get("translated_value", translated)
        supplied_residue = row.get("translation_residue", residue)
        if supplied_translated != translated:
            raise ValueError("translation_value_invalid_" + translation_id)
        if supplied_residue != residue:
            raise ValueError("translation_residue_invalid_" + translation_id)
        output.append(
            {
                "translation_id": translation_id,
                "source_observer_id": _text(
                    row.get("source_observer_id"), "source_observer_id"
                ),
                "target_observer_id": _text(
                    row.get("target_observer_id"), "target_observer_id"
                ),
                "event_digest": _text(row.get("event_digest"), "event_digest"),
                "translation_map_digest": _text(
                    row.get("translation_map_digest"), "translation_map_digest"
                ),
                "offset_integer": offset,
                "source_value": source_value,
                "target_value": target_value,
                "translated_value": translated,
                "translation_residue": residue,
                "residue_visible": row.get("residue_visible") is True,
            }
        )
    return sorted(output, key=lambda item: item["translation_id"])


def normalize_integer_list(value: Any, field: str, *, maximum_count: int = 64) -> list[int]:
    rows = _sequence(value, field)
    if not rows or len(rows) > maximum_count:
        raise ValueError(field + "_count_invalid")
    return [_int(item, field) for item in rows]


def compute_input_digest(
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
) -> str:
    return digest_object(
        {
            "schema_version": SCHEMA_VERSION,
            "source_planos_v123_certificate_digest": source_planos_v123_certificate_digest,
            "source_decisionos_v06_certificate_digest": source_decisionos_v06_certificate_digest,
            "source_memoryos_v039_capsule_digest": source_memoryos_v039_capsule_digest,
            "source_world_model_digest": source_world_model_digest,
            "observers": observers,
            "records": records,
            "translations": translations,
            "memory_kernel_weights": memory_kernel_weights,
            "counterfactual_history_effects": counterfactual_history_effects,
            "present_signal": present_signal,
        }
    )
