from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_candidate_nullspace_dephasing_rank_stratification_certificate_kernel_v0_1 import (
    _normalize_source_memoryos_v048,
)
from runtime.kuuos_memoryos_candidate_quotient_coordinate_canonicalization_certificate_kernel_v0_1 import (
    EXPECTED_PROBE_VECTORS,
    SCHEMA_VERSION as SOURCE_MEMORYOS_V050_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.candidate-quotient-mode-diagonalization-inverse-"
    "certificate.v0.1"
)
EXPECTED_CANDIDATE_IDS = [
    "continue",
    "hold",
    "reobserve",
    "terminate_candidate",
]
EXPECTED_DEPHASING_NUMERATORS = [2, 1, 0]
EXPECTED_QUOTIENT_RANKS = [1, 2, 2]
MAXIMUM_ABSOLUTE_INTEGER = 10_000_000


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


def _integer(value: Any, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(field + "_invalid")
    if abs(value) > MAXIMUM_ABSOLUTE_INTEGER:
        raise ValueError(field + "_out_of_bounds")
    return value


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


def _symmetric_mode(first: int, second: int) -> int:
    return first + second


def _antisymmetric_mode(first: int, second: int) -> int:
    return first - second


def _history_pairing(
    cross: int,
    left: tuple[int, int],
    right: tuple[int, int],
) -> int:
    return (
        2 * left[0] * right[0]
        + cross * left[0] * right[1]
        + cross * left[1] * right[0]
        + 2 * left[1] * right[1]
    )


def _mode_pairing_doubled(
    cross: int,
    left: tuple[int, int],
    right: tuple[int, int],
) -> int:
    return (
        (2 + cross)
        * _symmetric_mode(*left)
        * _symmetric_mode(*right)
        + (2 - cross)
        * _antisymmetric_mode(*left)
        * _antisymmetric_mode(*right)
    )


def _metric_product(
    left: tuple[tuple[int, int], tuple[int, int]],
    right: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    return (
        (
            left[0][0] * right[0][0] + left[0][1] * right[1][0],
            left[0][0] * right[0][1] + left[0][1] * right[1][1],
        ),
        (
            left[1][0] * right[0][0] + left[1][1] * right[1][0],
            left[1][0] * right[0][1] + left[1][1] * right[1][1],
        ),
    )


def _normalize_source_memoryos_v050(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v050_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v050_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V050_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v050_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v050_certificate_digest_missing")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v050_certificate_digest_mismatch")

    observables = source.get("observables")
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v050_observables_invalid")
    observables = dict(observables)

    required_true = (
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
    for field in required_true:
        if observables.get(field) is not True:
            raise ValueError("source_memoryos_v050_required_" + field)

    required_false = (
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v049_mutated",
        "source_memoryos_v048_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    )
    for field in required_false:
        if observables.get(field) is not False:
            raise ValueError("source_memoryos_v050_forbidden_" + field)

    candidate_ids = observables.get("retained_decision_candidate_ids")
    if candidate_ids != EXPECTED_CANDIDATE_IDS:
        raise ValueError("source_memoryos_v050_candidate_order_mismatch")
    history_ids = observables.get("retained_history_ids")
    if (
        not isinstance(history_ids, list)
        or len(history_ids) != 2
        or len(set(history_ids)) != 2
        or any(not isinstance(item, str) or not item for item in history_ids)
    ):
        raise ValueError("source_memoryos_v050_history_ids_invalid")

    if observables.get("quotient_coordinate_names") != [
        "first_history_coordinate",
        "second_history_coordinate",
    ]:
        raise ValueError("source_memoryos_v050_coordinate_names_mismatch")
    if observables.get("canonical_chart_fixed_zero_candidate_ids") != [
        "continue",
        "hold",
    ]:
        raise ValueError("source_memoryos_v050_fixed_chart_mismatch")
    if observables.get("canonical_chart_anchor_candidate_ids") != [
        "reobserve",
        "terminate_candidate",
    ]:
        raise ValueError("source_memoryos_v050_anchor_chart_mismatch")
    if observables.get("probe_vector_count") != len(EXPECTED_PROBE_VECTORS):
        raise ValueError("source_memoryos_v050_probe_count_mismatch")
    if (
        observables.get("ordered_probe_pair_count_per_step")
        != len(EXPECTED_PROBE_VECTORS) ** 2
    ):
        raise ValueError("source_memoryos_v050_pair_count_mismatch")
    if observables.get("structural_null_dimension_quotiented") != 2:
        raise ValueError("source_memoryos_v050_null_dimension_mismatch")
    if observables.get("quotient_coordinate_dimension") != 2:
        raise ValueError("source_memoryos_v050_quotient_dimension_mismatch")

    raw_probe_vectors = observables.get("probe_candidate_coefficient_vectors")
    expected_probe_vectors = [
        {"probe_id": probe_id, "coefficients": _coefficients(values)}
        for probe_id, values in EXPECTED_PROBE_VECTORS
    ]
    if raw_probe_vectors != expected_probe_vectors:
        raise ValueError("source_memoryos_v050_probe_vectors_mismatch")

    raw_records = observables.get(
        "candidate_quotient_canonicalization_records"
    )
    if (
        not isinstance(raw_records, list)
        or len(raw_records) != len(EXPECTED_PROBE_VECTORS)
    ):
        raise ValueError("source_memoryos_v050_canonical_records_invalid")
    records: dict[str, dict[str, Any]] = {}
    expected_probe_map = dict(EXPECTED_PROBE_VECTORS)
    for raw in raw_records:
        if not isinstance(raw, Mapping):
            raise ValueError("source_memoryos_v050_canonical_record_invalid")
        record = dict(raw)
        probe_id = record.get("probe_id")
        if probe_id not in expected_probe_map or probe_id in records:
            raise ValueError("source_memoryos_v050_probe_id_invalid")
        source_coefficients = record.get("source_candidate_coefficients")
        expected_coefficients = _coefficients(expected_probe_map[probe_id])
        if source_coefficients != expected_coefficients:
            raise ValueError("source_memoryos_v050_probe_coefficients_mismatch")
        coordinates = _coordinates(expected_coefficients)
        if (
            record.get("quotient_first_history_coordinate") != coordinates[0]
            or record.get("quotient_second_history_coordinate") != coordinates[1]
        ):
            raise ValueError("source_memoryos_v050_probe_coordinates_mismatch")
        expected_canonical = {
            "continue": 0,
            "hold": 0,
            "reobserve": coordinates[0],
            "terminate_candidate": coordinates[1],
        }
        if record.get("canonical_candidate_coefficients") != expected_canonical:
            raise ValueError("source_memoryos_v050_canonical_coefficients_mismatch")
        for field in (
            "source_equals_canonical_plus_structural_null",
            "canonical_coordinates_preserved",
            "canonical_continue_zero",
            "canonical_hold_zero",
            "canonical_representative_unique_in_chart",
            "probe_retained",
        ):
            if record.get(field) is not True:
                raise ValueError(
                    "source_memoryos_v050_canonical_record_required_" + field
                )
        records[probe_id] = record
    if set(records) != set(expected_probe_map):
        raise ValueError("source_memoryos_v050_probe_support_mismatch")

    trajectory = observables.get(
        "candidate_quotient_metric_descent_trajectory"
    )
    if not isinstance(trajectory, list) or len(trajectory) != 3:
        raise ValueError("source_memoryos_v050_trajectory_invalid")
    quotient_digest = observables.get(
        "candidate_quotient_coordinate_certificate_digest"
    )
    if not isinstance(quotient_digest, str) or not quotient_digest:
        raise ValueError("source_memoryos_v050_quotient_digest_missing")
    if canonical_digest(
        {
            "canonicalization_records": raw_records,
            "quotient_trajectory": trajectory,
        }
    ) != quotient_digest:
        raise ValueError("source_memoryos_v050_quotient_digest_mismatch")

    normalized_trajectory: list[dict[str, Any]] = []
    expected_probe_ids = {probe_id for probe_id, _ in EXPECTED_PROBE_VECTORS}
    expected_pairs = {
        (left_id, right_id)
        for left_id in expected_probe_ids
        for right_id in expected_probe_ids
    }
    for index, raw_step in enumerate(trajectory):
        if not isinstance(raw_step, Mapping):
            raise ValueError("source_memoryos_v050_step_invalid")
        step = dict(raw_step)
        if step.get("step_index") != index:
            raise ValueError("source_memoryos_v050_step_index_invalid")
        if (
            step.get("dephasing_numerator")
            != EXPECTED_DEPHASING_NUMERATORS[index]
        ):
            raise ValueError("source_memoryos_v050_dephasing_mismatch")
        denominator = _integer(
            step.get("kernel_entry_denominator"),
            "source_memoryos_v050_denominator",
        )
        if denominator <= 0:
            raise ValueError("source_memoryos_v050_denominator_nonpositive")
        if step.get("quotient_metric_rank") != EXPECTED_QUOTIENT_RANKS[index]:
            raise ValueError("source_memoryos_v050_rank_mismatch")
        if step.get("quotient_metric_nullity_removed") != 2:
            raise ValueError("source_memoryos_v050_nullity_removed_mismatch")
        if (
            step.get("all_step_quadratic_evidence_descends_exactly") is not True
            or step.get("all_step_bilinear_pairings_descend_exactly") is not True
        ):
            raise ValueError("source_memoryos_v050_step_descent_missing")

        raw_quadratics = step.get("probe_quadratic_descent_records")
        if (
            not isinstance(raw_quadratics, list)
            or len(raw_quadratics) != len(expected_probe_ids)
        ):
            raise ValueError("source_memoryos_v050_quadratics_invalid")
        quadratics: dict[str, dict[str, Any]] = {}
        for raw_quadratic in raw_quadratics:
            if not isinstance(raw_quadratic, Mapping):
                raise ValueError("source_memoryos_v050_quadratic_invalid")
            item = dict(raw_quadratic)
            probe_id = item.get("probe_id")
            if probe_id not in expected_probe_ids or probe_id in quadratics:
                raise ValueError("source_memoryos_v050_quadratic_probe_invalid")
            if item.get("quadratic_evidence_descends_exactly") is not True:
                raise ValueError("source_memoryos_v050_quadratic_descent_false")
            if item.get("denominator") != denominator:
                raise ValueError("source_memoryos_v050_quadratic_denominator_mismatch")
            quadratics[probe_id] = item

        raw_pairs = step.get("ordered_probe_pair_descent_records")
        if (
            not isinstance(raw_pairs, list)
            or len(raw_pairs) != len(expected_pairs)
        ):
            raise ValueError("source_memoryos_v050_pairs_invalid")
        pairs: dict[tuple[str, str], dict[str, Any]] = {}
        for raw_pair in raw_pairs:
            if not isinstance(raw_pair, Mapping):
                raise ValueError("source_memoryos_v050_pair_invalid")
            item = dict(raw_pair)
            pair = (item.get("left_probe_id"), item.get("right_probe_id"))
            if pair not in expected_pairs or pair in pairs:
                raise ValueError("source_memoryos_v050_pair_support_invalid")
            if (
                item.get("bilinear_pairing_descends_exactly") is not True
                or item.get("ordered_probe_pair_retained") is not True
            ):
                raise ValueError("source_memoryos_v050_pair_descent_false")
            if item.get("denominator") != denominator:
                raise ValueError("source_memoryos_v050_pair_denominator_mismatch")
            pairs[pair] = item
        normalized_trajectory.append(
            {
                "step_index": index,
                "dephasing_numerator": step["dephasing_numerator"],
                "kernel_entry_denominator": denominator,
                "quotient_metric_rank": step["quotient_metric_rank"],
                "quadratics": quadratics,
                "pairs": pairs,
            }
        )

    source_v048_digest = observables.get(
        "source_memoryos_v048_certificate_digest"
    )
    source_v048_factorization_digest = observables.get(
        "source_memoryos_v048_factorization_digest"
    )
    if not isinstance(source_v048_digest, str) or not source_v048_digest:
        raise ValueError("source_memoryos_v050_v048_digest_missing")
    if (
        not isinstance(source_v048_factorization_digest, str)
        or not source_v048_factorization_digest
    ):
        raise ValueError("source_memoryos_v050_v048_factorization_digest_missing")

    review_fields: dict[str, list[str]] = {}
    for field in (
        "source_relational_frontier_candidate_ids",
        "source_required_review_candidate_ids",
        "source_dissent_review_candidate_ids",
        "source_minority_protection_candidate_ids",
    ):
        field_value = observables.get(field)
        if (
            not isinstance(field_value, list)
            or len(field_value) != len(set(field_value))
            or any(item not in EXPECTED_CANDIDATE_IDS for item in field_value)
        ):
            raise ValueError("source_memoryos_v050_" + field + "_invalid")
        review_fields[field] = list(field_value)

    return {
        "certificate_digest": digest,
        "observables": observables,
        "candidate_ids": list(candidate_ids),
        "history_ids": list(history_ids),
        "records": records,
        "trajectory": normalized_trajectory,
        "quotient_digest": quotient_digest,
        "source_memoryos_v048_certificate_digest": source_v048_digest,
        "source_memoryos_v048_factorization_digest": (
            source_v048_factorization_digest
        ),
        **review_fields,
    }


def _derive_observables(
    source_memoryos_v050_certificate: Mapping[str, Any],
    source_memoryos_v048_certificate: Mapping[str, Any],
) -> dict[str, Any]:
    source_v050 = _normalize_source_memoryos_v050(
        source_memoryos_v050_certificate
    )
    source_v048 = _normalize_source_memoryos_v048(
        source_memoryos_v048_certificate
    )

    blockers: list[str] = []
    if (
        source_v050["source_memoryos_v048_certificate_digest"]
        != source_v048["certificate_digest"]
    ):
        blockers.append("source_v050_v048_certificate_binding_mismatch")
    if (
        source_v050["source_memoryos_v048_factorization_digest"]
        != source_v048["trajectory_digest"]
    ):
        blockers.append("source_v050_v048_factorization_binding_mismatch")
    if source_v050["candidate_ids"] != source_v048["candidate_ids"]:
        blockers.append("source_v050_v048_candidate_support_mismatch")
    if source_v050["history_ids"] != source_v048["history_ids"]:
        blockers.append("source_v050_v048_history_support_mismatch")
    if len(source_v050["trajectory"]) != len(source_v048["trajectory"]):
        blockers.append("source_v050_v048_trajectory_length_mismatch")
    if blockers:
        raise ValueError(blockers[0])

    probe_ids = [probe_id for probe_id, _ in EXPECTED_PROBE_VECTORS]
    probe_coordinates = {
        probe_id: (
            source_v050["records"][probe_id][
                "quotient_first_history_coordinate"
            ],
            source_v050["records"][probe_id][
                "quotient_second_history_coordinate"
            ],
        )
        for probe_id in probe_ids
    }

    trajectory: list[dict[str, Any]] = []
    all_quadratics_exact = True
    all_pairings_exact = True
    all_eigenvectors_exact = True
    all_determinants_exact = True
    all_inverse_witnesses_exact = True
    all_source_bindings_exact = True

    for quotient_step, factor_step in zip(
        source_v050["trajectory"],
        source_v048["trajectory"],
        strict=True,
    ):
        index = factor_step["step_index"]
        cross = factor_step["dephasing_numerator"]
        denominator = factor_step["kernel_entry_denominator"]
        if (
            quotient_step["step_index"] != index
            or quotient_step["dephasing_numerator"] != cross
            or quotient_step["kernel_entry_denominator"] != denominator
        ):
            raise ValueError("source_v050_v048_step_binding_mismatch")

        expected_metric = {
            (0, 0): (2, 0),
            (0, 1): (cross, 0),
            (1, 0): (cross, 0),
            (1, 1): (2, 0),
        }
        if factor_step["history_metric"] != expected_metric:
            raise ValueError("source_memoryos_v048_quotient_metric_mismatch")

        symmetric_weight = 2 + cross
        antisymmetric_weight = 2 - cross
        determinant = 4 - cross * cross
        metric = ((2, cross), (cross, 2))
        adjugate = ((2, -cross), (-cross, 2))
        metric_adjugate = _metric_product(metric, adjugate)
        adjugate_metric = _metric_product(adjugate, metric)
        expected_scaled_identity = ((determinant, 0), (0, determinant))
        determinant_factorization_exact = (
            determinant == symmetric_weight * antisymmetric_weight
        )
        inverse_witness_exact = (
            metric_adjugate == expected_scaled_identity
            and adjugate_metric == expected_scaled_identity
        )
        symmetric_action = (
            metric[0][0] + metric[0][1],
            metric[1][0] + metric[1][1],
        )
        antisymmetric_action = (
            metric[0][0] - metric[0][1],
            metric[1][0] - metric[1][1],
        )
        symmetric_eigenvector_exact = symmetric_action == (
            symmetric_weight,
            symmetric_weight,
        )
        antisymmetric_eigenvector_exact = antisymmetric_action == (
            antisymmetric_weight,
            -antisymmetric_weight,
        )
        all_eigenvectors_exact = (
            all_eigenvectors_exact
            and symmetric_eigenvector_exact
            and antisymmetric_eigenvector_exact
        )
        all_determinants_exact = (
            all_determinants_exact and determinant_factorization_exact
        )
        all_inverse_witnesses_exact = (
            all_inverse_witnesses_exact and inverse_witness_exact
        )

        quadratic_records: list[dict[str, Any]] = []
        for probe_id in probe_ids:
            coordinates = probe_coordinates[probe_id]
            symmetric_mode = _symmetric_mode(*coordinates)
            antisymmetric_mode = _antisymmetric_mode(*coordinates)
            source_value = _history_pairing(cross, coordinates, coordinates)
            diagonal_value = _mode_pairing_doubled(
                cross,
                coordinates,
                coordinates,
            )
            source_record = quotient_step["quadratics"][probe_id]
            source_bound = (
                source_record.get("canonical_real_numerator") == source_value
                and source_record.get("canonical_imag_numerator") == 0
                and source_record.get("source_real_numerator") == source_value
                and source_record.get("source_imag_numerator") == 0
            )
            exact = diagonal_value == 2 * source_value
            all_quadratics_exact = all_quadratics_exact and exact
            all_source_bindings_exact = all_source_bindings_exact and source_bound
            quadratic_records.append(
                {
                    "probe_id": probe_id,
                    "quotient_first_history_coordinate": coordinates[0],
                    "quotient_second_history_coordinate": coordinates[1],
                    "symmetric_mode_coordinate": symmetric_mode,
                    "antisymmetric_mode_coordinate": antisymmetric_mode,
                    "symmetric_mode_weight_numerator": symmetric_weight,
                    "antisymmetric_mode_weight_numerator": antisymmetric_weight,
                    "source_quadratic_real_numerator": source_value,
                    "source_quadratic_imag_numerator": 0,
                    "source_quadratic_denominator": denominator,
                    "mode_diagonal_doubled_real_numerator": diagonal_value,
                    "mode_diagonal_doubled_denominator": denominator,
                    "mode_diagonalization_exact": exact,
                    "source_memoryos_v050_quadratic_bound": source_bound,
                    "probe_retained": True,
                }
            )

        pair_records: list[dict[str, Any]] = []
        for left_id in probe_ids:
            for right_id in probe_ids:
                left = probe_coordinates[left_id]
                right = probe_coordinates[right_id]
                source_value = _history_pairing(cross, left, right)
                diagonal_value = _mode_pairing_doubled(cross, left, right)
                source_record = quotient_step["pairs"][left_id, right_id]
                source_bound = (
                    source_record.get("canonical_real_numerator") == source_value
                    and source_record.get("canonical_imag_numerator") == 0
                    and source_record.get("source_real_numerator") == source_value
                    and source_record.get("source_imag_numerator") == 0
                )
                exact = diagonal_value == 2 * source_value
                all_pairings_exact = all_pairings_exact and exact
                all_source_bindings_exact = (
                    all_source_bindings_exact and source_bound
                )
                pair_records.append(
                    {
                        "left_probe_id": left_id,
                        "right_probe_id": right_id,
                        "left_symmetric_mode_coordinate": _symmetric_mode(*left),
                        "left_antisymmetric_mode_coordinate": (
                            _antisymmetric_mode(*left)
                        ),
                        "right_symmetric_mode_coordinate": (
                            _symmetric_mode(*right)
                        ),
                        "right_antisymmetric_mode_coordinate": (
                            _antisymmetric_mode(*right)
                        ),
                        "source_bilinear_real_numerator": source_value,
                        "source_bilinear_imag_numerator": 0,
                        "source_bilinear_denominator": denominator,
                        "mode_diagonal_doubled_real_numerator": diagonal_value,
                        "mode_diagonal_doubled_denominator": denominator,
                        "mode_diagonalization_exact": exact,
                        "source_memoryos_v050_pairing_bound": source_bound,
                        "ordered_probe_pair_retained": True,
                    }
                )

        rank = 1 if determinant == 0 else 2
        full_coherence_rank_one = (
            cross == 2
            and antisymmetric_weight == 0
            and rank == 1
        )
        inverse_active = determinant != 0
        trajectory.append(
            {
                "step_index": index,
                "dephasing_numerator": cross,
                "kernel_entry_denominator": denominator,
                "symmetric_mode_weight_numerator": symmetric_weight,
                "antisymmetric_mode_weight_numerator": antisymmetric_weight,
                "mode_weight_denominator": denominator,
                "quotient_metric_determinant_numerator": determinant,
                "quotient_metric_determinant_denominator": denominator**2,
                "quotient_metric_rank": rank,
                "symmetric_mode_eigenvector_action": list(symmetric_action),
                "antisymmetric_mode_eigenvector_action": list(
                    antisymmetric_action
                ),
                "symmetric_mode_eigenvector_exact": (
                    symmetric_eigenvector_exact
                ),
                "antisymmetric_mode_eigenvector_exact": (
                    antisymmetric_eigenvector_exact
                ),
                "determinant_factorization_exact": (
                    determinant_factorization_exact
                ),
                "integer_adjugate_matrix": [
                    list(adjugate[0]),
                    list(adjugate[1]),
                ],
                "metric_times_adjugate": [
                    list(metric_adjugate[0]),
                    list(metric_adjugate[1]),
                ],
                "adjugate_times_metric": [
                    list(adjugate_metric[0]),
                    list(adjugate_metric[1]),
                ],
                "expected_determinant_scaled_identity": [
                    list(expected_scaled_identity[0]),
                    list(expected_scaled_identity[1]),
                ],
                "adjugate_inverse_witness_exact": inverse_witness_exact,
                "inverse_witness_active": inverse_active,
                "full_coherence_rank_one": full_coherence_rank_one,
                "probe_mode_quadratic_records": quadratic_records,
                "ordered_probe_pair_mode_bilinear_records": pair_records,
                "all_step_probe_quadratics_mode_diagonalized": all(
                    record["mode_diagonalization_exact"]
                    and record["source_memoryos_v050_quadratic_bound"]
                    for record in quadratic_records
                ),
                "all_step_ordered_pairings_mode_diagonalized": all(
                    record["mode_diagonalization_exact"]
                    and record["source_memoryos_v050_pairing_bound"]
                    for record in pair_records
                ),
            }
        )

    input_digest = canonical_digest(
        {
            "schema_version": SCHEMA_VERSION,
            "source_memoryos_v050_certificate_digest": source_v050[
                "certificate_digest"
            ],
            "source_memoryos_v050_quotient_digest": source_v050[
                "quotient_digest"
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
            "mode_basis": {
                "symmetric": [1, 1],
                "antisymmetric": [1, -1],
            },
        }
    )
    mode_digest = canonical_digest(trajectory)
    symmetric_weights = [
        step["symmetric_mode_weight_numerator"] for step in trajectory
    ]
    antisymmetric_weights = [
        step["antisymmetric_mode_weight_numerator"] for step in trajectory
    ]
    determinants = [
        step["quotient_metric_determinant_numerator"] for step in trajectory
    ]
    ranks = [step["quotient_metric_rank"] for step in trajectory]
    inverse_flags = [step["inverse_witness_active"] for step in trajectory]

    mixed_record = next(
        record
        for record in trajectory[0]["probe_mode_quadratic_records"]
        if record["probe_id"] == "mixed_candidate_probe"
    )

    return {
        "input_digest": input_digest,
        "source_memoryos_v050_certificate_digest": source_v050[
            "certificate_digest"
        ],
        "source_memoryos_v050_quotient_coordinate_digest": source_v050[
            "quotient_digest"
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
        "quotient_mode_names": [
            "symmetric_history_mode",
            "antisymmetric_history_mode",
        ],
        "quotient_mode_basis_vectors": {
            "symmetric_history_mode": [1, 1],
            "antisymmetric_history_mode": [1, -1],
        },
        "candidate_quotient_mode_diagonalization_trajectory": trajectory,
        "candidate_quotient_mode_diagonalization_digest": mode_digest,
        "probe_vector_count": len(EXPECTED_PROBE_VECTORS),
        "ordered_probe_pair_count_per_step": len(EXPECTED_PROBE_VECTORS) ** 2,
        "symmetric_mode_weight_trajectory": symmetric_weights,
        "antisymmetric_mode_weight_trajectory": antisymmetric_weights,
        "quotient_metric_determinant_trajectory": determinants,
        "quotient_metric_rank_trajectory": ranks,
        "inverse_witness_active_trajectory": inverse_flags,
        "source_memoryos_v050_exact": True,
        "source_memoryos_v048_exact": True,
        "all_source_memoryos_v050_descent_records_bound": (
            all_source_bindings_exact
        ),
        "symmetric_mode_eigenvector_exact_across_trajectory": (
            all_eigenvectors_exact
        ),
        "antisymmetric_mode_eigenvector_exact_across_trajectory": (
            all_eigenvectors_exact
        ),
        "all_probe_quadratic_evidence_mode_diagonalized": (
            all_quadratics_exact
        ),
        "all_ordered_probe_pairings_mode_diagonalized": (
            all_pairings_exact
        ),
        "quotient_metric_determinant_factorization_exact": (
            all_determinants_exact
        ),
        "integer_adjugate_identity_exact_across_trajectory": (
            all_inverse_witnesses_exact
        ),
        "full_coherence_rank_one_symmetric_mode_only": (
            trajectory[0]["full_coherence_rank_one"]
            and trajectory[0]["antisymmetric_mode_weight_numerator"] == 0
        ),
        "dephasing_releases_antisymmetric_mode": (
            antisymmetric_weights == [0, 1, 2]
        ),
        "post_dephasing_inverse_witness_exact": (
            inverse_flags == [False, True, True]
            and all(
                step["adjugate_inverse_witness_exact"]
                for step in trajectory[1:]
            )
        ),
        "mode_weight_trajectory_exact": (
            symmetric_weights == [4, 3, 2]
            and antisymmetric_weights == [0, 1, 2]
        ),
        "determinant_trajectory_exact": determinants == [0, 3, 4],
        "quotient_rank_trajectory_preserved": ranks == [1, 2, 2],
        "mixed_probe_mode_coordinates_exact": (
            mixed_record["symmetric_mode_coordinate"] == 11
            and mixed_record["antisymmetric_mode_coordinate"] == -3
        ),
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "source_relational_frontier_candidate_ids": source_v050[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": source_v050[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": source_v050[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": source_v050[
            "source_minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "mode_decomposition_witness_advisory_only": True,
        "rank_one_mode_not_candidate_consensus": True,
        "inverse_witness_not_decision_authority": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v050_mutated": False,
        "source_memoryos_v048_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }


def issue_candidate_quotient_mode_diagonalization_inverse_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        observables = _derive_observables(
            payload.get("source_memoryos_v050_certificate"),
            payload.get("source_memoryos_v048_certificate"),
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))

    required_true_fields = (
        "source_memoryos_v050_exact",
        "source_memoryos_v048_exact",
        "all_source_memoryos_v050_descent_records_bound",
        "symmetric_mode_eigenvector_exact_across_trajectory",
        "antisymmetric_mode_eigenvector_exact_across_trajectory",
        "all_probe_quadratic_evidence_mode_diagonalized",
        "all_ordered_probe_pairings_mode_diagonalized",
        "quotient_metric_determinant_factorization_exact",
        "integer_adjugate_identity_exact_across_trajectory",
        "full_coherence_rank_one_symmetric_mode_only",
        "dephasing_releases_antisymmetric_mode",
        "post_dephasing_inverse_witness_exact",
        "mode_weight_trajectory_exact",
        "determinant_trajectory_exact",
        "quotient_rank_trajectory_preserved",
        "mixed_probe_mode_coordinates_exact",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "mode_decomposition_witness_advisory_only",
        "rank_one_mode_not_candidate_consensus",
        "inverse_witness_not_decision_authority",
        "future_only",
        "read_only",
    )
    for field in required_true_fields:
        if observables.get(field) is not True:
            blockers.append("observable_required_" + field)

    required_false_fields = (
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v050_mutated",
        "source_memoryos_v048_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    )
    for field in required_false_fields:
        if observables.get(field) is not False:
            blockers.append("observable_forbidden_" + field)

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
    "SOURCE_MEMORYOS_V050_SCHEMA_VERSION",
    "EXPECTED_PROBE_VECTORS",
    "canonical_digest",
    "_derive_observables",
    "_normalize_source_memoryos_v050",
    "issue_candidate_quotient_mode_diagonalization_inverse_certificate",
]
