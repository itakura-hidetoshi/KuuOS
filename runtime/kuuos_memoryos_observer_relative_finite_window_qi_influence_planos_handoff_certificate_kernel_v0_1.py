from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_memoryos_observer_relative_finite_window_qi_influence_planos_handoff_algebra_support_v0_1 import (
    exact_discarded_tail_residue,
    influence_handoff_observables,
)
from runtime.kuuos_memoryos_observer_relative_finite_window_qi_influence_planos_handoff_certificate_support_v0_1 import (
    expected_governance_claims,
)
from runtime.kuuos_memoryos_observer_relative_finite_window_qi_influence_planos_handoff_schema_support_v0_1 import (
    MAXIMUM_WINDOW_LENGTH,
    SCHEMA_VERSION,
    compute_input_digest,
    digest_object,
    normalize_candidate_couplings,
    normalize_component_map,
    normalize_history_projection_records,
    normalize_lag_weights,
    normalize_source_memoryos_v040_receipt,
    normalize_source_planos_v123_receipt,
)

TOP_LEVEL_FIELDS = {
    "schema_version",
    "source_memoryos_v040_receipt",
    "source_planos_v123_receipt",
    "history_projection_records",
    "window_length",
    "lag_weights",
    "discarded_tail_residue",
    "discarded_tail_residue_visible",
    "candidate_couplings",
    "action_denominator",
    "claims",
}


def _int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(field + "_invalid")
    return value


def _positive_int(value: Any, field: str) -> int:
    result = _int(value, field)
    if result <= 0:
        raise ValueError(field + "_invalid")
    return result


def _claim_mismatches(claims: Mapping[str, Any], expected: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    for field, value in expected.items():
        if claims.get(field) != value:
            blockers.append("claim_mismatch_" + field)
    for field in sorted(set(claims) - set(expected)):
        blockers.append("unexpected_claim_" + field)
    return blockers


def issue_observer_relative_finite_window_qi_influence_planos_handoff_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping) or set(payload) != TOP_LEVEL_FIELDS:
        return {
            "accepted": False,
            "schema_version": SCHEMA_VERSION,
            "blockers": ["top_level_schema_invalid"],
            "observables": {},
        }

    blockers: list[str] = []
    try:
        if payload["schema_version"] != SCHEMA_VERSION:
            raise ValueError("schema_version_invalid")
        source_memory = normalize_source_memoryos_v040_receipt(
            payload["source_memoryos_v040_receipt"]
        )
        source_planos = normalize_source_planos_v123_receipt(
            payload["source_planos_v123_receipt"]
        )
        projection_records = normalize_history_projection_records(
            payload["history_projection_records"],
            source_record_ids=source_memory["retained_record_ids"],
            source_record_digests=source_memory["retained_record_digests"],
            source_observer_ids=source_memory["retained_observer_ids"],
            source_translation_ids=source_memory["retained_translation_ids"],
        )
        window_length = _positive_int(payload["window_length"], "window_length")
        if window_length > MAXIMUM_WINDOW_LENGTH:
            raise ValueError("window_length_exceeded")
        if window_length > len(projection_records):
            raise ValueError("window_length_exceeds_record_count")
        lag_weights = normalize_lag_weights(
            payload["lag_weights"], window_length=window_length
        )
        tail_residue_claim = normalize_component_map(
            payload["discarded_tail_residue"], "discarded_tail_residue"
        )
        if payload["discarded_tail_residue_visible"] is not True:
            raise ValueError("discarded_tail_residue_visibility_required")
        candidate_couplings = normalize_candidate_couplings(
            payload["candidate_couplings"],
            source_history_ids=source_planos["retained_history_ids"],
        )
        action_denominator = _positive_int(
            payload["action_denominator"], "action_denominator"
        )
    except ValueError as exc:
        return {
            "accepted": False,
            "schema_version": SCHEMA_VERSION,
            "blockers": [str(exc)],
            "observables": {},
        }

    discarded_tail_records = projection_records[:-window_length]
    exact_tail_residue = exact_discarded_tail_residue(discarded_tail_records)
    if tail_residue_claim != exact_tail_residue:
        blockers.append("discarded_tail_residue_not_exact")

    if source_memory["retained_translation_ids"]:
        if not any(
            item["translation_residue_visible"] for item in projection_records
        ):
            blockers.append("translation_residue_projection_missing")
        if not any(item["component_effects"]["residue"] != 0 for item in projection_records):
            blockers.append("translation_residue_component_missing")

    if not all(
        item["observation_backaction_visible"]
        or item["component_effects"]["observation"] == 0
        for item in projection_records
    ):
        blockers.append("observation_backaction_visibility_violation")

    normalized_input = {
        "source_memoryos_v040_receipt": source_memory,
        "source_planos_v123_receipt": source_planos,
        "history_projection_records": projection_records,
        "window_length": window_length,
        "lag_weights": lag_weights,
        "discarded_tail_residue": exact_tail_residue,
        "discarded_tail_residue_visible": True,
        "candidate_couplings": candidate_couplings,
        "action_denominator": action_denominator,
    }
    input_digest = compute_input_digest(**normalized_input)
    observables = influence_handoff_observables(
        source_memoryos_v040_receipt=source_memory,
        source_planos_v123_receipt=source_planos,
        projection_records=projection_records,
        window_length=window_length,
        lag_weights=lag_weights,
        discarded_tail_residue=exact_tail_residue,
        candidate_couplings=candidate_couplings,
        action_denominator=action_denominator,
        input_digest=input_digest,
    )

    expected_claims = {**observables, **expected_governance_claims()}
    claims = payload["claims"]
    if not isinstance(claims, Mapping):
        blockers.append("claims_invalid")
    else:
        blockers.extend(_claim_mismatches(claims, expected_claims))

    certificate_digest = ""
    if not blockers:
        certificate_digest = digest_object(
            {
                "schema_version": SCHEMA_VERSION,
                "input_digest": input_digest,
                "observables": observables,
                "governance": expected_governance_claims(),
            }
        )

    return {
        "accepted": not blockers,
        "schema_version": SCHEMA_VERSION,
        "blockers": sorted(set(blockers)),
        "source_bindings": {
            "source_memoryos_v040_certificate_digest": source_memory[
                "certificate_digest"
            ],
            "source_memoryos_v040_record_ledger_digest": source_memory[
                "record_ledger_digest"
            ],
            "source_planos_v123_input_digest": source_planos["input_digest"],
        },
        "observables": deepcopy(observables),
        "governance": expected_governance_claims(),
        "certificate_digest": certificate_digest,
    }


__all__ = [
    "SCHEMA_VERSION",
    "issue_observer_relative_finite_window_qi_influence_planos_handoff_certificate",
]
