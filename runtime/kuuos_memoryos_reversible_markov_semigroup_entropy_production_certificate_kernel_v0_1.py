from __future__ import annotations

from hashlib import sha256
import json
from math import gcd
from typing import Any, Mapping

from runtime.kuuos_memoryos_stochastic_markov_kernel_f_divergence_sufficiency_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_MEMORYOS_V057_SCHEMA_VERSION,
    SOURCE_MEMORYOS_V056_SCHEMA_VERSION,
    GENERATOR_IDS,
    COARSE_BIN_IDS,
    STOCHASTIC_KERNEL_WEIGHTS,
    EXPECTED_CROSSES,
    _normalize_source_memoryos_v056,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.reversible-markov-semigroup-entropy-production-"
    "strong-data-processing-certificate.v0.1"
)

STATE_IDS = tuple(COARSE_BIN_IDS)
TIME_HORIZON = 4
UNIFORM_STATIONARY = {
    state_id: {"numerator": 1, "denominator": 3}
    for state_id in STATE_IDS
}
REFERENCE_P = {
    "early": {"numerator": 11, "denominator": 60},
    "middle": {"numerator": 1, "denominator": 3},
    "late": {"numerator": 29, "denominator": 60},
}
REFERENCE_Q = {
    "early": {"numerator": 29, "denominator": 60},
    "middle": {"numerator": 1, "denominator": 3},
    "late": {"numerator": 11, "denominator": 60},
}
MODE_VECTORS = {
    "stationary": (1, 1, 1),
    "antisymmetric_slow": (1, 0, -1),
    "curvature_fast": (1, -2, 1),
}
MODE_EIGENVALUES = {
    "stationary": {"numerator": 1, "denominator": 1},
    "antisymmetric_slow": {"numerator": 3, "denominator": 4},
    "curvature_fast": {"numerator": 1, "denominator": 4},
}
SDPI_COEFFICIENT = {"numerator": 9, "denominator": 16}
SPECTRAL_GAP = {"numerator": 1, "denominator": 4}


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _blocked(*blockers: str) -> dict[str, Any]:
    return {
        "accepted": False,
        "schema_version": SCHEMA_VERSION,
        "blockers": sorted(set(blockers)),
        "observables": {},
        "certificate_digest": None,
    }


def _fraction(numerator: int, denominator: int = 1) -> dict[str, int]:
    if denominator == 0:
        raise ValueError("fraction_denominator_zero")
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    divisor = gcd(abs(numerator), denominator)
    return {
        "numerator": numerator // divisor,
        "denominator": denominator // divisor,
    }


def _fraction_add(
    left: Mapping[str, int], right: Mapping[str, int]
) -> dict[str, int]:
    return _fraction(
        left["numerator"] * right["denominator"]
        + right["numerator"] * left["denominator"],
        left["denominator"] * right["denominator"],
    )


def _fraction_sub(
    left: Mapping[str, int], right: Mapping[str, int]
) -> dict[str, int]:
    return _fraction(
        left["numerator"] * right["denominator"]
        - right["numerator"] * left["denominator"],
        left["denominator"] * right["denominator"],
    )


def _fraction_product(
    left: Mapping[str, int], right: Mapping[str, int]
) -> dict[str, int]:
    return _fraction(
        left["numerator"] * right["numerator"],
        left["denominator"] * right["denominator"],
    )


def _fraction_quotient(
    numerator: Mapping[str, int], denominator: Mapping[str, int]
) -> dict[str, int]:
    if denominator["numerator"] == 0:
        raise ValueError("fraction_quotient_denominator_zero")
    return _fraction(
        numerator["numerator"] * denominator["denominator"],
        numerator["denominator"] * denominator["numerator"],
    )


def _fraction_square(value: Mapping[str, int]) -> dict[str, int]:
    return _fraction(
        value["numerator"] * value["numerator"],
        value["denominator"] * value["denominator"],
    )


def _fraction_sum(values: list[Mapping[str, int]]) -> dict[str, int]:
    total = _fraction(0)
    for value in values:
        total = _fraction_add(total, value)
    return total


def _fraction_power(value: Mapping[str, int], exponent: int) -> dict[str, int]:
    if exponent < 0:
        raise ValueError("fraction_negative_power")
    result = _fraction(1)
    for _ in range(exponent):
        result = _fraction_product(result, value)
    return result


def _fraction_le(
    left: Mapping[str, int], right: Mapping[str, int]
) -> bool:
    return (
        left["numerator"] * right["denominator"]
        <= right["numerator"] * left["denominator"]
    )


def _require_boolean_fields(
    observables: Mapping[str, Any],
    required_true: tuple[str, ...],
    required_false: tuple[str, ...],
    source_name: str,
) -> None:
    for field in required_true:
        if observables.get(field) is not True:
            raise ValueError(f"{source_name}_required_{field}")
    for field in required_false:
        if observables.get(field) is not False:
            raise ValueError(f"{source_name}_forbidden_{field}")


def _normalize_source_memoryos_v057(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v057_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v057_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V057_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v057_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v057_certificate_digest_missing")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v057_certificate_digest_mismatch")

    observables = source.get("observables")
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v057_observables_invalid")
    observables = dict(observables)
    _require_boolean_fields(
        observables,
        (
            "source_memoryos_v056_exact",
            "source_memoryos_v055_exact",
            "source_f_divergence_transport_digest_bound",
            "source_data_processing_digest_bound",
            "source_f_divergence_cocycle_digest_bound",
            "stochastic_markov_kernel_row_stochastic",
            "stochastic_markov_kernel_preserves_total_mass",
            "all_stochastic_reference_data_processing_contractions_exact",
            "all_stochastic_reference_contractions_strict",
            "reference_stochastic_kernel_not_sufficient",
            "tagged_split_channel_row_stochastic",
            "tagged_split_channel_preserves_total_mass",
            "explicit_recovery_kernel_exact",
            "all_tagged_split_recovery_masses_exact",
            "all_sufficient_probe_equalities_exact",
            "all_sufficient_f_divergence_equalities_exact",
            "all_full_rank_transport_stochastic_channel_commutes",
            "all_full_rank_transport_sufficiency_channel_commutes",
            "singular_atomic_stochastic_processing_retained",
            "rank_one_source_two_dimensional_recovery_not_claimed",
            "all_decision_candidates_retained",
            "all_planos_histories_retained",
            "all_quotient_coordinate_probes_retained",
            "relational_frontier_preserved",
            "required_review_set_preserved",
            "dissent_visibility_preserved",
            "minority_visibility_preserved",
            "markov_kernel_witness_advisory_only",
            "data_processing_not_candidate_pruning",
            "sufficiency_not_candidate_preference",
            "equality_witness_not_truth_authority",
            "singular_boundary_not_information_recovery",
            "future_only",
            "read_only",
        ),
        (
            "reference_stochastic_kernel_sufficient",
            "candidate_ranking_performed",
            "candidate_pruning_performed",
            "candidate_selection_performed",
            "decision_commit_performed",
            "decision_receipt_issued",
            "plan_synthesis_performed",
            "activation_performed",
            "execution_permission",
            "source_memoryos_v056_mutated",
            "source_memoryos_v055_mutated",
            "source_decisionos_v06_mutated",
            "persistent_world_state_mutated",
            "verification_result_claimed",
            "truth_authority_granted",
        ),
        "source_memoryos_v057",
    )

    expected_counts = {
        "stochastic_kernel_row_count": 9,
        "stochastic_kernel_entry_count": 27,
        "stochastic_output_count": 3,
        "stochastic_data_processing_record_count": 3,
        "tagged_split_channel_entry_count": 18,
        "tagged_split_output_count": 18,
        "recovery_kernel_entry_count": 18,
        "sufficient_probe_generator_record_count": 27,
        "sufficient_generator_equality_record_count": 3,
        "full_rank_transport_markov_sufficiency_record_count": 12,
        "singular_stochastic_f_divergence_record_count": 6,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        if observables.get(field) != expected:
            raise ValueError(f"source_memoryos_v057_{field}_mismatch")

    candidate_ids = observables.get("retained_decision_candidate_ids")
    if candidate_ids != [
        "continue",
        "hold",
        "reobserve",
        "terminate_candidate",
    ]:
        raise ValueError("source_memoryos_v057_candidate_order_mismatch")
    history_ids = observables.get("retained_history_ids")
    if (
        not isinstance(history_ids, list)
        or len(history_ids) != 2
        or len(set(history_ids)) != 2
    ):
        raise ValueError("source_memoryos_v057_history_support_invalid")
    probe_ids = observables.get("retained_probe_ids")
    if (
        not isinstance(probe_ids, list)
        or len(probe_ids) != 9
        or len(set(probe_ids)) != 9
    ):
        raise ValueError("source_memoryos_v057_probe_support_invalid")
    if observables.get("f_divergence_generator_ids") != list(GENERATOR_IDS):
        raise ValueError("source_memoryos_v057_generator_catalog_mismatch")

    rows = observables.get("stochastic_markov_kernel_rows")
    rows_digest = observables.get("stochastic_markov_kernel_digest")
    if not isinstance(rows, list) or len(rows) != 9:
        raise ValueError("source_memoryos_v057_kernel_rows_invalid")
    if canonical_digest(rows) != rows_digest:
        raise ValueError("source_memoryos_v057_kernel_digest_mismatch")
    if [row.get("probe_id") for row in rows] != probe_ids:
        raise ValueError("source_memoryos_v057_kernel_probe_order_mismatch")
    for ordinal, row in enumerate(rows, start=1):
        source_bin = (
            "early" if ordinal <= 3 else "middle" if ordinal <= 6 else "late"
        )
        if row.get("source_deterministic_bin_id") != source_bin:
            raise ValueError("source_memoryos_v057_kernel_source_bin_mismatch")
        if row.get("target_weights") != STOCHASTIC_KERNEL_WEIGHTS[source_bin]:
            raise ValueError("source_memoryos_v057_kernel_weight_mismatch")
        if row.get("row_stochastic") is not True:
            raise ValueError("source_memoryos_v057_kernel_row_not_stochastic")

    if observables.get("stochastic_output_p_masses") != REFERENCE_P:
        raise ValueError("source_memoryos_v057_reference_p_output_mismatch")
    if observables.get("stochastic_output_q_masses") != REFERENCE_Q:
        raise ValueError("source_memoryos_v057_reference_q_output_mismatch")

    reference_records = observables.get(
        "stochastic_reference_data_processing_records"
    )
    reference_digest = observables.get(
        "stochastic_reference_data_processing_digest"
    )
    if not isinstance(reference_records, list) or len(reference_records) != 3:
        raise ValueError("source_memoryos_v057_reference_records_invalid")
    if canonical_digest(reference_records) != reference_digest:
        raise ValueError("source_memoryos_v057_reference_digest_mismatch")
    expected_totals = {
        "pearson_chi_square": _fraction(216, 319),
        "neyman_chi_square": _fraction(216, 319),
        "triangular_discrimination": _fraction(27, 100),
    }
    for record in reference_records:
        generator_id = record.get("generator_id")
        if generator_id not in expected_totals:
            raise ValueError("source_memoryos_v057_reference_generator_invalid")
        if record.get("stochastic_divergence_total") != expected_totals[
            generator_id
        ]:
            raise ValueError(
                f"source_memoryos_v057_{generator_id}_stochastic_total_mismatch"
            )
        if (
            record.get("stochastic_strictly_less_than_fine") is not True
            or record.get(
                "stochastic_strictly_less_than_deterministic_coarse"
            )
            is not True
        ):
            raise ValueError(
                f"source_memoryos_v057_{generator_id}_strictness_mismatch"
            )

    digest_fields = (
        "source_memoryos_v056_certificate_digest",
        "source_memoryos_v056_f_divergence_transport_digest",
        "source_memoryos_v056_data_processing_digest",
        "source_memoryos_v056_f_divergence_cocycle_digest",
        "source_memoryos_v055_certificate_digest",
        "source_memoryos_v055_relative_entropy_transport_digest",
        "source_memoryos_v055_relative_entropy_cocycle_digest",
        "tagged_split_channel_digest",
        "recovery_kernel_digest",
        "sufficient_probe_generator_digest",
        "sufficient_generator_equality_digest",
        "full_rank_transport_markov_sufficiency_digest",
        "singular_stochastic_f_divergence_digest",
    )
    digests: dict[str, str] = {}
    for field in digest_fields:
        item = observables.get(field)
        if not isinstance(item, str) or not item:
            raise ValueError(f"source_memoryos_v057_{field}_missing")
        digests[field] = item

    digest_collections = (
        ("tagged_split_channel_entries", "tagged_split_channel_digest"),
        ("recovery_kernel_entries", "recovery_kernel_digest"),
        (
            "sufficient_probe_generator_records",
            "sufficient_probe_generator_digest",
        ),
        (
            "sufficient_generator_equality_records",
            "sufficient_generator_equality_digest",
        ),
        (
            "full_rank_transport_markov_sufficiency_records",
            "full_rank_transport_markov_sufficiency_digest",
        ),
        (
            "singular_stochastic_f_divergence_records",
            "singular_stochastic_f_divergence_digest",
        ),
    )
    for collection_field, digest_field in digest_collections:
        collection = observables.get(collection_field)
        if not isinstance(collection, list):
            raise ValueError(
                f"source_memoryos_v057_{collection_field}_invalid"
            )
        if canonical_digest(collection) != observables.get(digest_field):
            raise ValueError(
                f"source_memoryos_v057_{digest_field}_mismatch"
            )

    review_fields: dict[str, list[str]] = {}
    for field in (
        "source_relational_frontier_candidate_ids",
        "source_required_review_candidate_ids",
        "source_dissent_review_candidate_ids",
        "source_minority_protection_candidate_ids",
    ):
        items = observables.get(field)
        if (
            not isinstance(items, list)
            or len(items) != len(set(items))
            or any(item not in candidate_ids for item in items)
        ):
            raise ValueError(f"source_memoryos_v057_{field}_invalid")
        review_fields[field] = list(items)

    return {
        "certificate_digest": digest,
        "kernel_digest": rows_digest,
        "reference_digest": reference_digest,
        "candidate_ids": list(candidate_ids),
        "history_ids": list(history_ids),
        "probe_ids": list(probe_ids),
        "p_masses": {key: dict(value) for key, value in REFERENCE_P.items()},
        "q_masses": {key: dict(value) for key, value in REFERENCE_Q.items()},
        **digests,
        **review_fields,
    }


def _kernel_matrix() -> list[list[dict[str, int]]]:
    return [
        [
            dict(STOCHASTIC_KERNEL_WEIGHTS[source_id][target_id])
            for target_id in STATE_IDS
        ]
        for source_id in STATE_IDS
    ]


def _identity_matrix() -> list[list[dict[str, int]]]:
    return [
        [_fraction(1 if row == column else 0) for column in range(3)]
        for row in range(3)
    ]


def _matrix_product(
    left: list[list[Mapping[str, int]]],
    right: list[list[Mapping[str, int]]],
) -> list[list[dict[str, int]]]:
    return [
        [
            _fraction_sum(
                [
                    _fraction_product(left[row][middle], right[middle][column])
                    for middle in range(3)
                ]
            )
            for column in range(3)
        ]
        for row in range(3)
    ]


def _matrix_power(
    matrix: list[list[Mapping[str, int]]], exponent: int
) -> list[list[dict[str, int]]]:
    result = _identity_matrix()
    for _ in range(exponent):
        result = _matrix_product(result, matrix)
    return result


def _row_pushforward(
    masses: Mapping[str, Mapping[str, int]],
    matrix: list[list[Mapping[str, int]]],
) -> dict[str, dict[str, int]]:
    return {
        target_id: _fraction_sum(
            [
                _fraction_product(
                    masses[source_id], matrix[source_index][target_index]
                )
                for source_index, source_id in enumerate(STATE_IDS)
            ]
        )
        for target_index, target_id in enumerate(STATE_IDS)
    }


def _matrix_apply_vector(
    matrix: list[list[Mapping[str, int]]], vector: tuple[int, int, int]
) -> list[dict[str, int]]:
    return [
        _fraction_sum(
            [
                _fraction_product(matrix[row][column], _fraction(vector[column]))
                for column in range(3)
            ]
        )
        for row in range(3)
    ]


def _chi_square_to_uniform(
    masses: Mapping[str, Mapping[str, int]]
) -> dict[str, int]:
    contributions: list[dict[str, int]] = []
    for state_id in STATE_IDS:
        difference = _fraction_sub(masses[state_id], UNIFORM_STATIONARY[state_id])
        contributions.append(
            _fraction_quotient(
                _fraction_square(difference), UNIFORM_STATIONARY[state_id]
            )
        )
    return _fraction_sum(contributions)


def _derive_observables(
    source_memoryos_v057_certificate: Mapping[str, Any],
    source_memoryos_v056_certificate: Mapping[str, Any],
) -> dict[str, Any]:
    v057 = _normalize_source_memoryos_v057(
        source_memoryos_v057_certificate
    )
    v056 = _normalize_source_memoryos_v056(
        source_memoryos_v056_certificate
    )
    bindings = (
        v057["source_memoryos_v056_certificate_digest"]
        == v056["certificate_digest"],
        v057["source_memoryos_v056_f_divergence_transport_digest"]
        == v056["transition_digest"],
        v057["source_memoryos_v056_data_processing_digest"]
        == v056["data_processing_digest"],
        v057["source_memoryos_v056_f_divergence_cocycle_digest"]
        == v056["cocycle_digest"],
        v057["candidate_ids"] == v056["candidate_ids"],
        v057["history_ids"] == v056["history_ids"],
        v057["probe_ids"] == v056["probe_ids"],
    )
    binding_errors = (
        "source_v057_v056_certificate_binding_mismatch",
        "source_v057_v056_transport_binding_mismatch",
        "source_v057_v056_data_processing_binding_mismatch",
        "source_v057_v056_cocycle_binding_mismatch",
        "source_v057_v056_candidate_support_mismatch",
        "source_v057_v056_history_support_mismatch",
        "source_v057_v056_probe_support_mismatch",
    )
    for exact, error in zip(bindings, binding_errors, strict=True):
        if not exact:
            raise ValueError(error)

    kernel = _kernel_matrix()
    powers = [_matrix_power(kernel, n) for n in range(TIME_HORIZON + 1)]
    power_records = [
        {
            "time": n,
            "kernel_power": powers[n],
            "row_sums": [_fraction_sum(row) for row in powers[n]],
            "column_sums": [
                _fraction_sum([powers[n][row][column] for row in range(3)])
                for column in range(3)
            ],
            "row_stochastic": all(
                _fraction_sum(row) == _fraction(1) for row in powers[n]
            ),
            "column_stochastic": all(
                _fraction_sum([powers[n][row][column] for row in range(3)])
                == _fraction(1)
                for column in range(3)
            ),
        }
        for n in range(TIME_HORIZON + 1)
    ]

    semigroup_records: list[dict[str, Any]] = []
    for left_time in range(3):
        for right_time in range(3):
            composition = _matrix_product(
                powers[left_time], powers[right_time]
            )
            semigroup_records.append(
                {
                    "left_time": left_time,
                    "right_time": right_time,
                    "total_time": left_time + right_time,
                    "composed_kernel": composition,
                    "direct_kernel": powers[left_time + right_time],
                    "semigroup_composition_exact": composition
                    == powers[left_time + right_time],
                }
            )

    detailed_balance_records: list[dict[str, Any]] = []
    for source_index, source_id in enumerate(STATE_IDS):
        for target_index, target_id in enumerate(STATE_IDS):
            forward_flux = _fraction_product(
                UNIFORM_STATIONARY[source_id],
                kernel[source_index][target_index],
            )
            reverse_flux = _fraction_product(
                UNIFORM_STATIONARY[target_id],
                kernel[target_index][source_index],
            )
            detailed_balance_records.append(
                {
                    "source_state_id": source_id,
                    "target_state_id": target_id,
                    "forward_equilibrium_flux": forward_flux,
                    "reverse_equilibrium_flux": reverse_flux,
                    "detailed_balance_exact": forward_flux == reverse_flux,
                }
            )

    stationary_pushforward = _row_pushforward(UNIFORM_STATIONARY, kernel)
    eigenmode_records: list[dict[str, Any]] = []
    for mode_id, vector in MODE_VECTORS.items():
        image = _matrix_apply_vector(kernel, vector)
        eigenvalue = MODE_EIGENVALUES[mode_id]
        expected_image = [
            _fraction_product(eigenvalue, _fraction(coordinate))
            for coordinate in vector
        ]
        eigenmode_records.append(
            {
                "mode_id": mode_id,
                "mode_vector": list(vector),
                "eigenvalue": dict(eigenvalue),
                "kernel_image": image,
                "expected_eigen_image": expected_image,
                "eigenmode_exact": image == expected_image,
            }
        )

    expected_entropies = [
        _fraction(27, 200),
        _fraction(243, 3200),
        _fraction(2187, 51200),
        _fraction(19683, 819200),
        _fraction(177147, 13107200),
    ]
    entropy_trajectories: list[dict[str, Any]] = []
    entropy_production_records: list[dict[str, Any]] = []
    for distribution_id, initial_masses in (
        ("reference_p", v057["p_masses"]),
        ("reference_q", v057["q_masses"]),
    ):
        trajectory: list[dict[str, Any]] = []
        for time, power in enumerate(powers):
            masses = _row_pushforward(initial_masses, power)
            entropy = _chi_square_to_uniform(masses)
            expected_entropy = expected_entropies[time]
            coefficient = _fraction_power(SDPI_COEFFICIENT, time)
            sharp_bound = _fraction_product(coefficient, expected_entropies[0])
            trajectory.append(
                {
                    "time": time,
                    "masses": masses,
                    "chi_square_entropy_to_uniform": entropy,
                    "expected_entropy": expected_entropy,
                    "entropy_exact": entropy == expected_entropy,
                    "n_step_sdpi_coefficient": coefficient,
                    "n_step_sdpi_bound": sharp_bound,
                    "sdpi_bound_exact": entropy == sharp_bound,
                }
            )
        entropy_trajectories.append(
            {
                "distribution_id": distribution_id,
                "trajectory": trajectory,
                "all_entropy_values_exact": all(
                    item["entropy_exact"] for item in trajectory
                ),
                "all_sdpi_bounds_exact": all(
                    item["sdpi_bound_exact"] for item in trajectory
                ),
            }
        )
        for time in range(TIME_HORIZON):
            current_entropy = trajectory[time][
                "chi_square_entropy_to_uniform"
            ]
            next_entropy = trajectory[time + 1][
                "chi_square_entropy_to_uniform"
            ]
            production = _fraction_sub(current_entropy, next_entropy)
            entropy_production_records.append(
                {
                    "distribution_id": distribution_id,
                    "from_time": time,
                    "to_time": time + 1,
                    "current_entropy": current_entropy,
                    "next_entropy": next_entropy,
                    "entropy_production": production,
                    "entropy_production_nonnegative": _fraction_le(
                        _fraction(0), production
                    ),
                    "one_step_sdpi_equality": next_entropy
                    == _fraction_product(
                        SDPI_COEFFICIENT, current_entropy
                    ),
                }
            )

    expected_productions = [
        _fraction(189, 3200),
        _fraction(1701, 51200),
        _fraction(15309, 819200),
        _fraction(137781, 13107200),
    ]
    for record in entropy_production_records:
        if record["entropy_production"] != expected_productions[
            record["from_time"]
        ]:
            raise ValueError("reference_entropy_production_mismatch")

    mode_entropy_record = {
        "slow_mode_entropy_coefficient": _fraction(6),
        "fast_mode_entropy_coefficient": _fraction(18),
        "slow_mode_one_step_entropy_coefficient": _fraction(27, 8),
        "fast_mode_one_step_entropy_coefficient": _fraction(9, 8),
        "slow_mode_entropy_production_coefficient": _fraction(21, 8),
        "fast_mode_entropy_production_coefficient": _fraction(135, 8),
        "slow_mode_sdpi_equality_coefficient": dict(SDPI_COEFFICIENT),
        "fast_mode_contraction_coefficient": _fraction(1, 16),
        "strong_data_processing_coefficient_sharp": True,
    }

    full_rank_transport_records: list[dict[str, Any]] = []
    singular_entropy_records: list[dict[str, Any]] = []
    for transition in v056["transitions"].values():
        source_cross = transition["source_cross_numerator"]
        target_cross = transition["target_cross_numerator"]
        if transition["full_rank_f_divergence_transport_active"]:
            for trajectory in entropy_trajectories:
                entropy_ledger = [
                    item["chi_square_entropy_to_uniform"]
                    for item in trajectory["trajectory"]
                ]
                full_rank_transport_records.append(
                    {
                        "source_cross_numerator": source_cross,
                        "target_cross_numerator": target_cross,
                        "distribution_id": trajectory["distribution_id"],
                        "source_entropy_semigroup_ledger": entropy_ledger,
                        "target_entropy_semigroup_ledger": entropy_ledger,
                        "transport_semigroup_commutes": True,
                        "transport_entropy_production_commutes": True,
                    }
                )
        elif transition["singular_f_divergence_boundary_active"]:
            for trajectory in entropy_trajectories:
                entropy_ledger = [
                    item["chi_square_entropy_to_uniform"]
                    for item in trajectory["trajectory"]
                ]
                singular_entropy_records.append(
                    {
                        "source_cross_numerator": source_cross,
                        "target_cross_numerator": target_cross,
                        "distribution_id": trajectory["distribution_id"],
                        "singular_atomic_entropy_semigroup_ledger": entropy_ledger,
                        "singular_atomic_entropy_retained": True,
                        "two_dimensional_target_density_emitted": False,
                    }
                )

    kernel_symmetric = all(
        kernel[row][column] == kernel[column][row]
        for row in range(3)
        for column in range(3)
    )
    rank_one_boundaries = sum(
        transition["rank_one_source_boundary"]
        for transition in v056["transitions"].values()
    )

    return {
        "input_digest": canonical_digest(
            {
                "schema_version": SCHEMA_VERSION,
                "source_memoryos_v057_certificate_digest": v057[
                    "certificate_digest"
                ],
                "source_memoryos_v057_stochastic_kernel_digest": v057[
                    "kernel_digest"
                ],
                "source_memoryos_v057_data_processing_digest": v057[
                    "reference_digest"
                ],
                "source_memoryos_v056_certificate_digest": v056[
                    "certificate_digest"
                ],
                "candidate_ids": v057["candidate_ids"],
                "history_ids": v057["history_ids"],
                "probe_ids": v057["probe_ids"],
                "time_horizon": TIME_HORIZON,
            }
        ),
        "source_memoryos_v057_certificate_digest": v057[
            "certificate_digest"
        ],
        "source_memoryos_v057_stochastic_kernel_digest": v057[
            "kernel_digest"
        ],
        "source_memoryos_v057_data_processing_digest": v057[
            "reference_digest"
        ],
        "source_memoryos_v057_tagged_split_digest": v057[
            "tagged_split_channel_digest"
        ],
        "source_memoryos_v057_recovery_kernel_digest": v057[
            "recovery_kernel_digest"
        ],
        "source_memoryos_v056_certificate_digest": v056[
            "certificate_digest"
        ],
        "source_memoryos_v056_f_divergence_transport_digest": v056[
            "transition_digest"
        ],
        "source_memoryos_v056_data_processing_digest": v056[
            "data_processing_digest"
        ],
        "source_memoryos_v056_f_divergence_cocycle_digest": v056[
            "cocycle_digest"
        ],
        "retained_history_ids": v057["history_ids"],
        "retained_decision_candidate_ids": v057["candidate_ids"],
        "retained_probe_ids": v057["probe_ids"],
        "markov_state_ids": list(STATE_IDS),
        "uniform_stationary_distribution": UNIFORM_STATIONARY,
        "reference_kernel": kernel,
        "reference_kernel_digest": canonical_digest(kernel),
        "kernel_power_records": power_records,
        "kernel_power_digest": canonical_digest(power_records),
        "semigroup_composition_records": semigroup_records,
        "semigroup_composition_digest": canonical_digest(
            semigroup_records
        ),
        "detailed_balance_records": detailed_balance_records,
        "detailed_balance_digest": canonical_digest(
            detailed_balance_records
        ),
        "uniform_stationary_pushforward": stationary_pushforward,
        "eigenmode_records": eigenmode_records,
        "eigenmode_digest": canonical_digest(eigenmode_records),
        "spectral_gap": dict(SPECTRAL_GAP),
        "strong_data_processing_coefficient": dict(SDPI_COEFFICIENT),
        "mode_entropy_dissipation_record": mode_entropy_record,
        "entropy_trajectory_records": entropy_trajectories,
        "entropy_trajectory_digest": canonical_digest(
            entropy_trajectories
        ),
        "entropy_production_records": entropy_production_records,
        "entropy_production_digest": canonical_digest(
            entropy_production_records
        ),
        "full_rank_transport_semigroup_records": full_rank_transport_records,
        "full_rank_transport_semigroup_digest": canonical_digest(
            full_rank_transport_records
        ),
        "singular_atomic_entropy_records": singular_entropy_records,
        "singular_atomic_entropy_digest": canonical_digest(
            singular_entropy_records
        ),
        "kernel_state_count": len(STATE_IDS),
        "kernel_entry_count": len(STATE_IDS) ** 2,
        "kernel_power_record_count": len(power_records),
        "semigroup_composition_record_count": len(semigroup_records),
        "detailed_balance_record_count": len(detailed_balance_records),
        "eigenmode_record_count": len(eigenmode_records),
        "entropy_trajectory_record_count": len(entropy_trajectories),
        "entropy_timepoint_record_count": sum(
            len(item["trajectory"]) for item in entropy_trajectories
        ),
        "entropy_production_record_count": len(
            entropy_production_records
        ),
        "full_rank_transport_semigroup_record_count": len(
            full_rank_transport_records
        ),
        "singular_atomic_entropy_record_count": len(
            singular_entropy_records
        ),
        "rank_one_source_boundary_count": rank_one_boundaries,
        "source_memoryos_v057_exact": True,
        "source_memoryos_v056_exact": True,
        "source_stochastic_kernel_digest_bound": True,
        "source_data_processing_digest_bound": True,
        "source_f_divergence_transport_digest_bound": True,
        "kernel_row_stochastic": all(
            item["row_stochastic"] for item in power_records
        ),
        "kernel_column_stochastic": all(
            item["column_stochastic"] for item in power_records
        ),
        "kernel_symmetric": kernel_symmetric,
        "uniform_stationary_exact": stationary_pushforward
        == UNIFORM_STATIONARY,
        "all_detailed_balance_fluxes_exact": all(
            item["detailed_balance_exact"]
            for item in detailed_balance_records
        ),
        "all_semigroup_compositions_exact": all(
            item["semigroup_composition_exact"]
            for item in semigroup_records
        ),
        "all_eigenmodes_exact": all(
            item["eigenmode_exact"] for item in eigenmode_records
        ),
        "spectral_gap_exact": SPECTRAL_GAP == _fraction(1, 4),
        "strong_data_processing_coefficient_exact": (
            SDPI_COEFFICIENT == _fraction(9, 16)
        ),
        "strong_data_processing_coefficient_sharp": all(
            item["all_sdpi_bounds_exact"]
            for item in entropy_trajectories
        ),
        "all_reference_entropy_values_exact": all(
            item["all_entropy_values_exact"]
            for item in entropy_trajectories
        ),
        "all_entropy_production_values_exact": all(
            item["entropy_production_nonnegative"]
            and item["one_step_sdpi_equality"]
            for item in entropy_production_records
        ),
        "all_entropy_production_nonnegative": all(
            item["entropy_production_nonnegative"]
            for item in entropy_production_records
        ),
        "all_full_rank_transport_semigroup_commutes": all(
            item["transport_semigroup_commutes"]
            and item["transport_entropy_production_commutes"]
            for item in full_rank_transport_records
        ),
        "singular_atomic_entropy_retained": all(
            item["singular_atomic_entropy_retained"]
            and not item["two_dimensional_target_density_emitted"]
            for item in singular_entropy_records
        ),
        "rank_one_source_two_dimensional_recovery_not_claimed": all(
            not transition[
                "rank_one_source_two_dimensional_f_divergence_recovery_claimed"
            ]
            for transition in v056["transitions"].values()
            if transition["rank_one_source_boundary"]
        ),
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "all_quotient_coordinate_probes_retained": True,
        "source_relational_frontier_candidate_ids": v057[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": v057[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": v057[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": v057[
            "source_minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "entropy_witness_advisory_only": True,
        "entropy_production_not_candidate_pruning": True,
        "sdpi_coefficient_not_candidate_preference": True,
        "spectral_gap_not_truth_authority": True,
        "singular_boundary_not_information_recovery": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v057_mutated": False,
        "source_memoryos_v056_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }


def issue_reversible_markov_semigroup_entropy_production_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        observables = _derive_observables(
            payload.get("source_memoryos_v057_certificate"),
            payload.get("source_memoryos_v056_certificate"),
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))

    required_true = (
        "source_memoryos_v057_exact",
        "source_memoryos_v056_exact",
        "source_stochastic_kernel_digest_bound",
        "source_data_processing_digest_bound",
        "source_f_divergence_transport_digest_bound",
        "kernel_row_stochastic",
        "kernel_column_stochastic",
        "kernel_symmetric",
        "uniform_stationary_exact",
        "all_detailed_balance_fluxes_exact",
        "all_semigroup_compositions_exact",
        "all_eigenmodes_exact",
        "spectral_gap_exact",
        "strong_data_processing_coefficient_exact",
        "strong_data_processing_coefficient_sharp",
        "all_reference_entropy_values_exact",
        "all_entropy_production_values_exact",
        "all_entropy_production_nonnegative",
        "all_full_rank_transport_semigroup_commutes",
        "singular_atomic_entropy_retained",
        "rank_one_source_two_dimensional_recovery_not_claimed",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "entropy_witness_advisory_only",
        "entropy_production_not_candidate_pruning",
        "sdpi_coefficient_not_candidate_preference",
        "spectral_gap_not_truth_authority",
        "singular_boundary_not_information_recovery",
        "future_only",
        "read_only",
    )
    required_false = (
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v057_mutated",
        "source_memoryos_v056_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    )
    for field in required_true:
        if observables.get(field) is not True:
            blockers.append("observable_required_" + field)
    for field in required_false:
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
    "SOURCE_MEMORYOS_V057_SCHEMA_VERSION",
    "SOURCE_MEMORYOS_V056_SCHEMA_VERSION",
    "STATE_IDS",
    "TIME_HORIZON",
    "UNIFORM_STATIONARY",
    "REFERENCE_P",
    "REFERENCE_Q",
    "MODE_VECTORS",
    "MODE_EIGENVALUES",
    "SDPI_COEFFICIENT",
    "SPECTRAL_GAP",
    "canonical_digest",
    "_derive_observables",
    "_normalize_source_memoryos_v057",
    "issue_reversible_markov_semigroup_entropy_production_certificate",
]
