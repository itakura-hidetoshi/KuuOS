from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_memoryos_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_algebra_support_v0_1 import influence_conditioned_coherence_observables
from runtime.kuuos_memoryos_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_certificate_support_v0_1 import expected_governance_claims
from runtime.kuuos_memoryos_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_schema_support_v0_1 import (
    SCHEMA_VERSION,
    compute_input_digest,
    digest_object,
    normalize_source_memoryos_v041_receipt,
    normalize_source_planos_v123_kernel_receipt,
)

TOP_LEVEL_FIELDS = {
    "schema_version",
    "source_memoryos_v041_receipt",
    "source_planos_v123_kernel_receipt",
    "claims",
}


def _claim_mismatches(claims: Mapping[str, Any], expected: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    for field, value in expected.items():
        if claims.get(field) != value:
            blockers.append("claim_mismatch_" + field)
    for field in sorted(set(claims) - set(expected)):
        blockers.append("unexpected_claim_" + field)
    return blockers


def issue_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping) or set(payload) != TOP_LEVEL_FIELDS:
        return {
            "accepted": False,
            "schema_version": SCHEMA_VERSION,
            "blockers": ["top_level_schema_invalid"],
            "observables": {},
        }
    try:
        if payload["schema_version"] != SCHEMA_VERSION:
            raise ValueError("schema_version_invalid")
        source_memory = normalize_source_memoryos_v041_receipt(
            payload["source_memoryos_v041_receipt"]
        )
        source_planos = normalize_source_planos_v123_kernel_receipt(
            payload["source_planos_v123_kernel_receipt"]
        )
    except ValueError as exc:
        return {
            "accepted": False,
            "schema_version": SCHEMA_VERSION,
            "blockers": [str(exc)],
            "observables": {},
        }

    blockers: list[str] = []
    if source_memory["source_planos_v123_input_digest"] != source_planos["input_digest"]:
        blockers.append("source_planos_v123_input_digest_binding_mismatch")
    if source_memory["retained_history_ids"] != source_planos["retained_history_ids"]:
        blockers.append("memoryos_planos_history_support_order_mismatch")

    normalized_input = {
        "source_memoryos_v041_receipt": source_memory,
        "source_planos_v123_kernel_receipt": source_planos,
    }
    input_digest = compute_input_digest(**normalized_input)
    observables = influence_conditioned_coherence_observables(
        source_memoryos_v041_receipt=source_memory,
        source_planos_v123_kernel_receipt=source_planos,
        input_digest=input_digest,
    )
    if not observables["discarded_tail_changes_coherence_kernel"]:
        blockers.append("discarded_tail_coherence_effect_missing")
    if not observables["all_conditioned_steps_hermitian"]:
        blockers.append("conditioned_kernel_hermiticity_failed")
    if not observables["all_diagonals_preserved"]:
        blockers.append("conditioned_kernel_diagonal_preservation_failed")
    if not observables["all_steps_psd_by_diagonal_phase_congruence"]:
        blockers.append("conditioned_kernel_psd_witness_failed")
    if not observables["all_history_pair_support_retained"]:
        blockers.append("conditioned_kernel_support_preservation_failed")

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
            "source_memoryos_v041_certificate_digest": source_memory[
                "certificate_digest"
            ],
            "source_memoryos_v041_influence_handoff_digest": source_memory[
                "influence_handoff_digest"
            ],
            "source_planos_v123_input_digest": source_planos["input_digest"],
        },
        "observables": deepcopy(observables),
        "governance": expected_governance_claims(),
        "certificate_digest": certificate_digest,
    }


__all__ = [
    "SCHEMA_VERSION",
    "issue_observer_relative_non_markov_influence_conditioned_planos_coherence_kernel_certificate",
]
