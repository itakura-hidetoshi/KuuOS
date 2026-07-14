from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_candidate_nullspace_dephasing_rank_stratification_certificate_kernel_v0_1 import (
    EXPECTED_CANDIDATE_IDS,
    SCHEMA_VERSION as SOURCE_MEMORYOS_V049_SCHEMA_VERSION,
    STRUCTURAL_NULL_RELATIONS,
    _normalize_source_memoryos_v048,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.candidate-quotient-coordinate-canonicalization-"
    "certificate.v0.1"
)
MAXIMUM_ABSOLUTE_INTEGER = 10_000_000
EXPECTED_PROBE_VECTORS: tuple[
    tuple[str, tuple[int, int, int, int]], ...
] = (
    ("continue_basis", (1, 0, 0, 0)),
    ("hold_basis", (0, 1, 0, 0)),
    ("reobserve_basis", (0, 0, 1, 0)),
    ("terminate_basis", (0, 0, 0, 1)),
    ("first_structural_null", (1, 0, -1, -1)),
    ("second_structural_null", (0, 1, -1, 1)),
    ("antisymmetric_history_probe", (0, 0, 1, -1)),
    ("symmetric_history_probe", (0, 0, 1, 1)),
    ("mixed_candidate_probe", (2, -1, 3, 4)),
)


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _blocked(*blockers: str) -> dict[str, Any]:
    return {
        "accepted": False,
        "schema_version": SCHEMA_VERSION,
        "blockers": sorted(set(blockers)),
        "observables": {},
        "certificate_digest": None,
    }


def _coefficients(
    values: tuple[int, int, int, int],
) -> dict[str, int]:
    return dict(zip(EXPECTED_CANDIDATE_IDS, values, strict=True))


def _coordinates(coefficients: Mapping[str, int]) -> tuple[int, int]:
    return (
        coefficients["continue"]
        + coefficients["hold"]
        + coefficients["reobserve"],
        coefficients["continue"]
        - coefficients["hold"]
        + coefficients["terminate_candidate"],
    )


def _canonical_representative(
    coordinates: tuple[int, int],
) -> dict[str, int]:
    return {
        "continue": 0,
        "hold": 0,
        "reobserve": coordinates[0],
        "terminate_candidate": coordinates[1],
    }


def _difference(
    left: Mapping[str, int],
    right: Mapping[str, int],
) -> dict[str, int]:
    return {
        candidate_id: left[candidate_id] - right[candidate_id]
        for candidate_id in EXPECTED_CANDIDATE_IDS
    }


def _structural_combination(
    alpha: int,
    beta: int,
) -> dict[str, int]:
    first = _coefficients(STRUCTURAL_NULL_RELATIONS[0][1])
    second = _coefficients(STRUCTURAL_NULL_RELATIONS[1][1])
    return {
        candidate_id: alpha * first[candidate_id] + beta * second[candidate_id]
        for candidate_id in EXPECTED_CANDIDATE_IDS
    }


def _complex_add(
    left: tuple[int, int],
    right: tuple[int, int],
) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def _complex_scale(
    coefficient: int,
    value: tuple[int, int],
) -> tuple[int, int]:
    return coefficient * value[0], coefficient * value[1]


def _pairing(
    entries: Mapping[tuple[str, str], tuple[int, int]],
    left: Mapping[str, int],
    right: Mapping[str, int],
) -> tuple[int, int]:
    total = (0, 0)
    for left_id in EXPECTED_CANDIDATE_IDS:
        for right_id in EXPECTED_CANDIDATE_IDS:
            total = _complex_add(
                total,
                _complex_scale(
                    left[left_id] * right[right_id],
                    entries[left_id, right_id],
                ),
            )
    return total


def _normalize_source_memoryos_v049(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v049_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v049_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V049_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v049_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v049_certificate_digest_missing")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v049_certificate_digest_mismatch")

    observables = source.get("observables")
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v049_observables_invalid")
    observables = dict(observables)

    required_true = (
        "source_memoryos_v048_exact",
        "source_memoryos_v045_exact",
        "structural_null_basis_exact",
        "all_structural_null_directions_kernel_annihilated",
        "all_structural_null_quadratic_evidence_zero",
        "candidate_quadratic_evidence_invariant_under_structural_null_translation",
        "all_history_metric_determinants_real_nonnegative",
        "history_rank_trajectory_exact",
        "candidate_rank_trajectory_exact",
        "candidate_nullity_trajectory_exact",
        "antisymmetric_probe_energy_trajectory_exact",
        "symmetric_probe_energy_trajectory_exact",
        "structural_nullspace_persists_across_dephasing",
        "full_coherence_extra_null_direction_independent",
        "dephasing_releases_extra_coherence_null_direction",
        "dephasing_recovers_candidate_rank_from_one_to_two",
        "full_coherence_candidate_nullity_three",
        "post_dephasing_candidate_nullity_two",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "nullspace_witness_advisory_only",
        "null_direction_not_candidate_dispensability",
        "rank_recovery_not_candidate_preference",
        "future_only",
        "read_only",
    )
    for field in required_true:
        if observables.get(field) is not True:
            raise ValueError("source_memoryos_v049_required_" + field)

    required_false = (
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v048_mutated",
        "source_memoryos_v045_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    )
    for field in required_false:
        if observables.get(field) is not False:
            raise ValueError("source_memoryos_v049_forbidden_" + field)

    candidate_ids = observables.get("retained_decision_candidate_ids")
    if candidate_ids != EXPECTED_CANDIDATE_IDS:
        raise ValueError("source_memoryos_v049_candidate_order_mismatch")
    history_ids = observables.get("retained_history_ids")
    if (
        not isinstance(history_ids, list)
        or len(history_ids) != 2
        or len(set(history_ids)) != 2
        or any(not isinstance(item, str) or not item for item in history_ids)
    ):
        raise ValueError("source_memoryos_v049_history_ids_invalid")

    expected_basis = [
        {
            "relation_id": relation_id,
            "candidate_coefficients": _coefficients(values),
            "lifted_history_coordinates": [0, 0],
        }
        for relation_id, values in STRUCTURAL_NULL_RELATIONS
    ]
    if observables.get("candidate_structural_null_basis") != expected_basis:
        raise ValueError("source_memoryos_v049_structural_basis_mismatch")
    if observables.get("candidate_structural_null_basis_dimension") != 2:
        raise ValueError("source_memoryos_v049_structural_basis_dimension_invalid")

    trajectory = observables.get(
        "candidate_nullspace_rank_stratification_trajectory"
    )
    trajectory_digest = observables.get(
        "candidate_nullspace_rank_stratification_digest"
    )
    if not isinstance(trajectory, list) or not trajectory:
        raise ValueError("source_memoryos_v049_trajectory_invalid")
    if not isinstance(trajectory_digest, str) or not trajectory_digest:
        raise ValueError("source_memoryos_v049_trajectory_digest_missing")
    if canonical_digest(trajectory) != trajectory_digest:
        raise ValueError("source_memoryos_v049_trajectory_digest_mismatch")
    if observables.get("history_metric_rank_trajectory") != [1, 2, 2]:
        raise ValueError("source_memoryos_v049_history_rank_trajectory_mismatch")
    if observables.get("candidate_gram_rank_trajectory") != [1, 2, 2]:
        raise ValueError("source_memoryos_v049_candidate_rank_trajectory_mismatch")
    if observables.get("candidate_gram_nullity_trajectory") != [3, 2, 2]:
        raise ValueError("source_memoryos_v049_candidate_nullity_trajectory_mismatch")

    source_v048_digest = observables.get(
        "source_memoryos_v048_certificate_digest"
    )
    source_v048_factorization_digest = observables.get(
        "source_memoryos_v048_factorization_digest"
    )
    if not isinstance(source_v048_digest, str) or not source_v048_digest:
        raise ValueError("source_memoryos_v049_v048_digest_missing")
    if (
        not isinstance(source_v048_factorization_digest, str)
        or not source_v048_factorization_digest
    ):
        raise ValueError("source_memoryos_v049_v048_factorization_digest_missing")

    review_fields: dict[str, list[str]] = {}
    for field in (
        "source_relational_frontier_candidate_ids",
        "source_required_review_candidate_ids",
        "source_dissent_review_candidate_ids",
        "source_minority_protection_candidate_ids",
    ):
        value_field = observables.get(field)
        if (
            not isinstance(value_field, list)
            or len(value_field) != len(set(value_field))
            or any(item not in EXPECTED_CANDIDATE_IDS for item in value_field)
        ):
            raise ValueError("source_memoryos_v049_" + field + "_invalid")
        review_fields[field] = list(value_field)

    return {
        "certificate_digest": digest,
        "observables": observables,
        "candidate_ids": list(candidate_ids),
        "history_ids": list(history_ids),
        "trajectory": trajectory,
        "trajectory_digest": trajectory_digest,
        "source_memoryos_v048_certificate_digest": source_v048_digest,
        "source_memoryos_v048_factorization_digest": (
            source_v048_factorization_digest
        ),
        **review_fields,
    }


def issue_candidate_quotient_coordinate_canonicalization_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        source_v049 = _normalize_source_memoryos_v049(
            payload.get("source_memoryos_v049_certificate")
        )
        source_v048 = _normalize_source_memoryos_v048(
            payload.get("source_memoryos_v048_certificate")
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))

    if (
        source_v049["source_memoryos_v048_certificate_digest"]
        != source_v048["certificate_digest"]
    ):
        blockers.append("source_v049_v048_certificate_binding_mismatch")
    if (
        source_v049["source_memoryos_v048_factorization_digest"]
        != source_v048["trajectory_digest"]
    ):
        blockers.append("source_v049_v048_factorization_binding_mismatch")
    if source_v049["candidate_ids"] != source_v048["candidate_ids"]:
        blockers.append("source_v049_v048_candidate_support_mismatch")
    if source_v049["history_ids"] != source_v048["history_ids"]:
        blockers.append("source_v049_v048_history_support_mismatch")
    if len(source_v049["trajectory"]) != len(source_v048["trajectory"]):
        blockers.append("source_v049_v048_trajectory_length_mismatch")
    else:
        for rank_step, factor_step in zip(
            source_v049["trajectory"],
            source_v048["trajectory"],
            strict=True,
        ):
            if (
                rank_step.get("step_index") != factor_step["step_index"]
                or rank_step.get("dephasing_numerator")
                != factor_step["dephasing_numerator"]
                or rank_step.get("kernel_entry_denominator")
                != factor_step["kernel_entry_denominator"]
            ):
                blockers.append("source_v049_v048_step_binding_mismatch")
                break
    if blockers:
        return _blocked(*blockers)

    canonicalization_records: list[dict[str, Any]] = []
    probe_map: dict[str, dict[str, int]] = {}
    canonical_map: dict[str, dict[str, int]] = {}
    all_decompositions_exact = True
    all_coordinates_preserved = True
    all_canonical_unique = True

    for probe_id, values in EXPECTED_PROBE_VECTORS:
        original = _coefficients(values)
        coordinates = _coordinates(original)
        canonical = _canonical_representative(coordinates)
        residual = _difference(original, canonical)
        structural = _structural_combination(
            original["continue"],
            original["hold"],
        )
        canonical_coordinates = _coordinates(canonical)
        decomposition_exact = residual == structural
        coordinates_preserved = canonical_coordinates == coordinates
        canonical_unique = (
            canonical["continue"] == 0
            and canonical["hold"] == 0
            and canonical["reobserve"] == coordinates[0]
            and canonical["terminate_candidate"] == coordinates[1]
        )
        all_decompositions_exact = (
            all_decompositions_exact and decomposition_exact
        )
        all_coordinates_preserved = (
            all_coordinates_preserved and coordinates_preserved
        )
        all_canonical_unique = all_canonical_unique and canonical_unique
        probe_map[probe_id] = original
        canonical_map[probe_id] = canonical
        canonicalization_records.append(
            {
                "probe_id": probe_id,
                "source_candidate_coefficients": original,
                "quotient_first_history_coordinate": coordinates[0],
                "quotient_second_history_coordinate": coordinates[1],
                "canonical_candidate_coefficients": canonical,
                "structural_translation_alpha": original["continue"],
                "structural_translation_beta": original["hold"],
                "source_minus_canonical_coefficients": residual,
                "structural_null_combination_coefficients": structural,
                "source_equals_canonical_plus_structural_null": (
                    decomposition_exact
                ),
                "canonical_coordinates_preserved": coordinates_preserved,
                "canonical_continue_zero": canonical["continue"] == 0,
                "canonical_hold_zero": canonical["hold"] == 0,
                "canonical_representative_unique_in_chart": canonical_unique,
                "probe_retained": True,
            }
        )

    quotient_trajectory: list[dict[str, Any]] = []
    all_pairings_descend = True
    all_quadratics_descend = True
    for step in source_v048["trajectory"]:
        entries = step["entries"]
        pair_records: list[dict[str, Any]] = []
        quadratic_records: list[dict[str, Any]] = []
        for probe_id, _ in EXPECTED_PROBE_VECTORS:
            source_quadratic = _pairing(
                entries,
                probe_map[probe_id],
                probe_map[probe_id],
            )
            canonical_quadratic = _pairing(
                entries,
                canonical_map[probe_id],
                canonical_map[probe_id],
            )
            exact = source_quadratic == canonical_quadratic
            all_quadratics_descend = all_quadratics_descend and exact
            quadratic_records.append(
                {
                    "probe_id": probe_id,
                    "source_real_numerator": source_quadratic[0],
                    "source_imag_numerator": source_quadratic[1],
                    "canonical_real_numerator": canonical_quadratic[0],
                    "canonical_imag_numerator": canonical_quadratic[1],
                    "denominator": step["kernel_entry_denominator"],
                    "quadratic_evidence_descends_exactly": exact,
                }
            )
            for right_probe_id, _ in EXPECTED_PROBE_VECTORS:
                source_pairing = _pairing(
                    entries,
                    probe_map[probe_id],
                    probe_map[right_probe_id],
                )
                canonical_pairing = _pairing(
                    entries,
                    canonical_map[probe_id],
                    canonical_map[right_probe_id],
                )
                pairing_exact = source_pairing == canonical_pairing
                all_pairings_descend = (
                    all_pairings_descend and pairing_exact
                )
                pair_records.append(
                    {
                        "left_probe_id": probe_id,
                        "right_probe_id": right_probe_id,
                        "source_real_numerator": source_pairing[0],
                        "source_imag_numerator": source_pairing[1],
                        "canonical_real_numerator": canonical_pairing[0],
                        "canonical_imag_numerator": canonical_pairing[1],
                        "denominator": step["kernel_entry_denominator"],
                        "bilinear_pairing_descends_exactly": pairing_exact,
                        "ordered_probe_pair_retained": True,
                    }
                )
        quotient_trajectory.append(
            {
                "step_index": step["step_index"],
                "dephasing_numerator": step["dephasing_numerator"],
                "kernel_entry_denominator": step["kernel_entry_denominator"],
                "probe_quadratic_descent_records": quadratic_records,
                "ordered_probe_pair_descent_records": pair_records,
                "all_step_quadratic_evidence_descends_exactly": all(
                    item["quadratic_evidence_descends_exactly"]
                    for item in quadratic_records
                ),
                "all_step_bilinear_pairings_descend_exactly": all(
                    item["bilinear_pairing_descends_exactly"]
                    for item in pair_records
                ),
                "quotient_metric_rank": source_v049[
                    "observables"
                ]["candidate_gram_rank_trajectory"][step["step_index"]],
                "quotient_metric_nullity_removed": 2,
            }
        )

    input_digest = canonical_digest(
        {
            "schema_version": SCHEMA_VERSION,
            "source_memoryos_v049_certificate_digest": source_v049[
                "certificate_digest"
            ],
            "source_memoryos_v049_rank_digest": source_v049[
                "trajectory_digest"
            ],
            "source_memoryos_v048_certificate_digest": source_v048[
                "certificate_digest"
            ],
            "source_memoryos_v048_factorization_digest": source_v048[
                "trajectory_digest"
            ],
            "candidate_ids": source_v048["candidate_ids"],
            "history_ids": source_v048["history_ids"],
            "probe_vectors": [
                {"probe_id": probe_id, "coefficients": _coefficients(values)}
                for probe_id, values in EXPECTED_PROBE_VECTORS
            ],
        }
    )
    quotient_digest = canonical_digest(
        {
            "canonicalization_records": canonicalization_records,
            "quotient_trajectory": quotient_trajectory,
        }
    )
    observables = {
        "input_digest": input_digest,
        "source_memoryos_v049_certificate_digest": source_v049[
            "certificate_digest"
        ],
        "source_memoryos_v049_rank_stratification_digest": source_v049[
            "trajectory_digest"
        ],
        "source_memoryos_v048_certificate_digest": source_v048[
            "certificate_digest"
        ],
        "source_memoryos_v048_factorization_digest": source_v048[
            "trajectory_digest"
        ],
        "retained_history_ids": source_v048["history_ids"],
        "retained_decision_candidate_ids": source_v048["candidate_ids"],
        "quotient_coordinate_names": [
            "first_history_coordinate",
            "second_history_coordinate",
        ],
        "canonical_chart_fixed_zero_candidate_ids": ["continue", "hold"],
        "canonical_chart_anchor_candidate_ids": [
            "reobserve",
            "terminate_candidate",
        ],
        "probe_candidate_coefficient_vectors": [
            {"probe_id": probe_id, "coefficients": _coefficients(values)}
            for probe_id, values in EXPECTED_PROBE_VECTORS
        ],
        "candidate_quotient_canonicalization_records": (
            canonicalization_records
        ),
        "candidate_quotient_metric_descent_trajectory": quotient_trajectory,
        "candidate_quotient_coordinate_certificate_digest": quotient_digest,
        "probe_vector_count": len(EXPECTED_PROBE_VECTORS),
        "ordered_probe_pair_count_per_step": len(EXPECTED_PROBE_VECTORS) ** 2,
        "structural_null_dimension_quotiented": 2,
        "quotient_coordinate_dimension": 2,
        "source_memoryos_v049_exact": True,
        "source_memoryos_v048_exact": True,
        "all_probe_canonical_decompositions_exact": all_decompositions_exact,
        "all_probe_quotient_coordinates_preserved": all_coordinates_preserved,
        "all_probe_canonical_representatives_unique_in_chart": (
            all_canonical_unique
        ),
        "all_probe_quadratic_evidence_descends_to_quotient": (
            all_quadratics_descend
        ),
        "all_ordered_probe_pairings_descend_to_quotient": (
            all_pairings_descend
        ),
        "quotient_metric_rank_trajectory_preserved": [
            step["quotient_metric_rank"] for step in quotient_trajectory
        ]
        == [1, 2, 2],
        "structural_nullspace_removed_from_coordinates_not_candidates": True,
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "source_relational_frontier_candidate_ids": source_v049[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": source_v049[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": source_v049[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": source_v049[
            "source_minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "quotient_coordinate_witness_advisory_only": True,
        "canonical_representative_not_candidate_selection": True,
        "quotient_not_candidate_pruning": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v049_mutated": False,
        "source_memoryos_v048_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    required_true_fields = (
        "source_memoryos_v049_exact",
        "source_memoryos_v048_exact",
        "all_probe_canonical_decompositions_exact",
        "all_probe_quotient_coordinates_preserved",
        "all_probe_canonical_representatives_unique_in_chart",
        "all_probe_quadratic_evidence_descends_to_quotient",
        "all_ordered_probe_pairings_descend_to_quotient",
        "quotient_metric_rank_trajectory_preserved",
        "structural_nullspace_removed_from_coordinates_not_candidates",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "quotient_coordinate_witness_advisory_only",
        "canonical_representative_not_candidate_selection",
        "quotient_not_candidate_pruning",
        "future_only",
        "read_only",
    )
    for field in required_true_fields:
        if observables[field] is not True:
            blockers.append("observable_required_" + field)

    claims = payload.get("claims")
    if not isinstance(claims, Mapping):
        blockers.append("claims_invalid")
    else:
        for field, expected in observables.items():
            if claims.get(field) != expected:
                blockers.append("claim_mismatch_" + field)
        extra = sorted(set(claims) - set(observables))
        if extra:
            blockers.append("claim_extra_field_" + extra[0])

    if blockers:
        return _blocked(*blockers)
    certificate = {
        "accepted": True,
        "schema_version": SCHEMA_VERSION,
        "blockers": [],
        "observables": observables,
    }
    certificate["certificate_digest"] = canonical_digest(certificate)
    return certificate


__all__ = [
    "SCHEMA_VERSION",
    "SOURCE_MEMORYOS_V049_SCHEMA_VERSION",
    "EXPECTED_PROBE_VECTORS",
    "canonical_digest",
    "issue_candidate_quotient_coordinate_canonicalization_certificate",
]
