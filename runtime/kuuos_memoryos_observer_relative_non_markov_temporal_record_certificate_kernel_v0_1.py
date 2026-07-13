from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_memoryos_observer_relative_non_markov_temporal_record_algebra_support_v0_1 import (
    temporal_record_observables,
)
from runtime.kuuos_memoryos_observer_relative_non_markov_temporal_record_certificate_support_v0_1 import (
    expected_governance_claims,
)
from runtime.kuuos_memoryos_observer_relative_non_markov_temporal_record_schema_support_v0_1 import (
    SCHEMA_VERSION,
    build_record_chain,
    compute_input_digest,
    normalize_integer_list,
    normalize_observers,
    normalize_translations,
)


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(field + "_invalid")
    return value.strip()


def _int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(field + "_invalid")
    return value


def _claim_mismatches(claims: Mapping[str, Any], expected: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    for field, value in expected.items():
        if claims.get(field) != value:
            blockers.append("claim_mismatch_" + field)
    extra = sorted(set(claims) - set(expected))
    blockers.extend("unexpected_claim_" + field for field in extra)
    return blockers


def issue_observer_relative_non_markov_temporal_record_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    blockers: list[str] = []
    try:
        if payload.get("schema_version") != SCHEMA_VERSION:
            raise ValueError("schema_version_invalid")
        source_planos = _text(
            payload.get("source_planos_v123_certificate_digest"),
            "source_planos_v123_certificate_digest",
        )
        source_decisionos = _text(
            payload.get("source_decisionos_v06_certificate_digest"),
            "source_decisionos_v06_certificate_digest",
        )
        source_memoryos = _text(
            payload.get("source_memoryos_v039_capsule_digest"),
            "source_memoryos_v039_capsule_digest",
        )
        source_world = _text(
            payload.get("source_world_model_digest"), "source_world_model_digest"
        )
        observers = normalize_observers(payload.get("observers"))
        records = build_record_chain(payload.get("records"))
        translations = normalize_translations(payload.get("translations"))
        weights = normalize_integer_list(
            payload.get("memory_kernel_weights"), "memory_kernel_weights"
        )
        if any(weight < 0 for weight in weights):
            raise ValueError("memory_kernel_weight_negative")
        counterfactual = normalize_integer_list(
            payload.get("counterfactual_history_effects"),
            "counterfactual_history_effects",
        )
        present_signal = _int(payload.get("present_signal"), "present_signal")
    except ValueError as exc:
        return {
            "accepted": False,
            "schema_version": SCHEMA_VERSION,
            "blockers": [str(exc)],
            "observables": {},
        }

    observer_ids = {item["observer_id"] for item in observers}
    if any(item["absolute_observer"] for item in observers):
        blockers.append("absolute_observer_forbidden")

    records_by_key: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for record in records:
        if record["observer_id"] not in observer_ids:
            blockers.append("record_observer_missing_" + record["record_id"])
        if record["source_memoryos_v039_capsule_digest"] != source_memoryos:
            blockers.append("record_source_memoryos_mismatch_" + record["record_id"])
        if record["plan_future_ensemble_digest"] != source_planos:
            blockers.append("record_planos_digest_mismatch_" + record["record_id"])
        if record["decision_present_cut_digest"] != source_decisionos:
            blockers.append("record_decisionos_digest_mismatch_" + record["record_id"])
        if not record["record_not_event_identity"]:
            blockers.append("record_event_identity_forbidden_" + record["record_id"])
        records_by_key.setdefault(
            (record["observer_id"], record["event_digest"]), []
        ).append(record)

    for translation in translations:
        source_id = translation["source_observer_id"]
        target_id = translation["target_observer_id"]
        if source_id not in observer_ids:
            blockers.append(
                "translation_source_observer_missing_" + translation["translation_id"]
            )
        if target_id not in observer_ids:
            blockers.append(
                "translation_target_observer_missing_" + translation["translation_id"]
            )
        source_records = records_by_key.get(
            (source_id, translation["event_digest"]), []
        )
        target_records = records_by_key.get(
            (target_id, translation["event_digest"]), []
        )
        if len(source_records) != 1:
            blockers.append(
                "translation_source_record_not_unique_" + translation["translation_id"]
            )
        elif source_records[0]["observation_value"] != translation["source_value"]:
            blockers.append(
                "translation_source_value_mismatch_" + translation["translation_id"]
            )
        if len(target_records) != 1:
            blockers.append(
                "translation_target_record_not_unique_" + translation["translation_id"]
            )
        elif target_records[0]["observation_value"] != translation["target_value"]:
            blockers.append(
                "translation_target_value_mismatch_" + translation["translation_id"]
            )
        if not translation["residue_visible"]:
            blockers.append(
                "translation_residue_visibility_required_"
                + translation["translation_id"]
            )

    try:
        input_digest = compute_input_digest(
            source_planos_v123_certificate_digest=source_planos,
            source_decisionos_v06_certificate_digest=source_decisionos,
            source_memoryos_v039_capsule_digest=source_memoryos,
            source_world_model_digest=source_world,
            observers=observers,
            records=records,
            translations=translations,
            memory_kernel_weights=weights,
            counterfactual_history_effects=counterfactual,
            present_signal=present_signal,
        )
        observables = temporal_record_observables(
            source_planos_v123_certificate_digest=source_planos,
            source_decisionos_v06_certificate_digest=source_decisionos,
            source_memoryos_v039_capsule_digest=source_memoryos,
            source_world_model_digest=source_world,
            observers=observers,
            records=records,
            translations=translations,
            memory_kernel_weights=weights,
            counterfactual_history_effects=counterfactual,
            present_signal=present_signal,
            input_digest=input_digest,
        )
    except ValueError as exc:
        blockers.append(str(exc))
        observables = {}
        input_digest = ""

    if observables:
        expected_claims = {
            **observables,
            **expected_governance_claims(),
        }
        claims = payload.get("claims")
        if not isinstance(claims, Mapping):
            blockers.append("claims_invalid")
        else:
            blockers.extend(_claim_mismatches(claims, expected_claims))

    return {
        "accepted": not blockers,
        "schema_version": SCHEMA_VERSION,
        "blockers": sorted(set(blockers)),
        "observables": deepcopy(observables),
        "governance": expected_governance_claims(),
        "certificate_digest": input_digest if not blockers else "",
    }
