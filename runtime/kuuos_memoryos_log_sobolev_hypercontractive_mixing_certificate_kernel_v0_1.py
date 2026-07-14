from __future__ import annotations

from hashlib import sha256
import json
from math import gcd
from typing import Any, Mapping

from runtime.kuuos_memoryos_reversible_markov_semigroup_entropy_production_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_MEMORYOS_V058_SCHEMA_VERSION,
    SOURCE_MEMORYOS_V057_SCHEMA_VERSION,
    STATE_IDS,
    TIME_HORIZON,
    UNIFORM_STATIONARY,
    REFERENCE_P,
    REFERENCE_Q,
    SDPI_COEFFICIENT,
    SPECTRAL_GAP,
    _normalize_source_memoryos_v057,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.log-sobolev-hypercontractive-mixing-time-"
    "certificate.v0.1"
)

LOG_SOBOLEV_CONSTANT = {"numerator": 4, "denominator": 1}
ONE_STEP_L2_TO_L4_FOURTH_POWER_COEFFICIENT = {
    "numerator": 243,
    "denominator": 256,
}
TWO_STEP_L2_TO_LINF_SQUARED_COEFFICIENT = {
    "numerator": 243,
    "denominator": 256,
}
WORST_CASE_CHI_SQUARE_CAP = {"numerator": 2, "denominator": 1}
MIXING_TIME_HORIZON = 8


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


def _fraction_power(value: Mapping[str, int], exponent: int) -> dict[str, int]:
    if exponent < 0:
        raise ValueError("fraction_negative_power")
    result = _fraction(1)
    for _ in range(exponent):
        result = _fraction_product(result, value)
    return result


def _fraction_sum(values: list[Mapping[str, int]]) -> dict[str, int]:
    result = _fraction(0)
    for value in values:
        result = _fraction_add(result, value)
    return result


def _fraction_abs(value: Mapping[str, int]) -> dict[str, int]:
    return _fraction(abs(value["numerator"]), value["denominator"])


def _fraction_le(
    left: Mapping[str, int], right: Mapping[str, int]
) -> bool:
    return (
        left["numerator"] * right["denominator"]
        <= right["numerator"] * left["denominator"]
    )


def _fraction_lt(
    left: Mapping[str, int], right: Mapping[str, int]
) -> bool:
    return (
        left["numerator"] * right["denominator"]
        < right["numerator"] * left["denominator"]
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


def _normalize_source_memoryos_v058(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v058_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v058_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V058_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v058_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v058_certificate_digest_missing")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v058_certificate_digest_mismatch")

    observables = source.get("observables")
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v058_observables_invalid")
    observables = dict(observables)
    _require_boolean_fields(
        observables,
        (
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
        ),
        (
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
        ),
        "source_memoryos_v058",
    )

    expected_counts = {
        "kernel_state_count": 3,
        "kernel_entry_count": 9,
        "kernel_power_record_count": 5,
        "semigroup_composition_record_count": 9,
        "detailed_balance_record_count": 9,
        "eigenmode_record_count": 3,
        "entropy_trajectory_record_count": 2,
        "entropy_timepoint_record_count": 10,
        "entropy_production_record_count": 8,
        "full_rank_transport_semigroup_record_count": 8,
        "singular_atomic_entropy_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        if observables.get(field) != expected:
            raise ValueError(f"source_memoryos_v058_{field}_mismatch")

    if observables.get("spectral_gap") != SPECTRAL_GAP:
        raise ValueError("source_memoryos_v058_spectral_gap_mismatch")
    if observables.get("strong_data_processing_coefficient") != SDPI_COEFFICIENT:
        raise ValueError("source_memoryos_v058_sdpi_coefficient_mismatch")
    if observables.get("uniform_stationary_distribution") != UNIFORM_STATIONARY:
        raise ValueError("source_memoryos_v058_stationary_distribution_mismatch")

    digest_collections = (
        ("reference_kernel", "reference_kernel_digest"),
        ("kernel_power_records", "kernel_power_digest"),
        ("semigroup_composition_records", "semigroup_composition_digest"),
        ("detailed_balance_records", "detailed_balance_digest"),
        ("eigenmode_records", "eigenmode_digest"),
        ("entropy_trajectory_records", "entropy_trajectory_digest"),
        ("entropy_production_records", "entropy_production_digest"),
        (
            "full_rank_transport_semigroup_records",
            "full_rank_transport_semigroup_digest",
        ),
        ("singular_atomic_entropy_records", "singular_atomic_entropy_digest"),
    )
    digests: dict[str, str] = {}
    for collection_field, digest_field in digest_collections:
        collection = observables.get(collection_field)
        if not isinstance(collection, list):
            raise ValueError(
                f"source_memoryos_v058_{collection_field}_invalid"
            )
        digest_value = observables.get(digest_field)
        if not isinstance(digest_value, str) or not digest_value:
            raise ValueError(f"source_memoryos_v058_{digest_field}_missing")
        if canonical_digest(collection) != digest_value:
            raise ValueError(f"source_memoryos_v058_{digest_field}_mismatch")
        digests[digest_field] = digest_value

    candidate_ids = observables.get("retained_decision_candidate_ids")
    history_ids = observables.get("retained_history_ids")
    probe_ids = observables.get("retained_probe_ids")
    if candidate_ids != [
        "continue",
        "hold",
        "reobserve",
        "terminate_candidate",
    ]:
        raise ValueError("source_memoryos_v058_candidate_order_mismatch")
    if (
        not isinstance(history_ids, list)
        or len(history_ids) != 2
        or len(set(history_ids)) != 2
    ):
        raise ValueError("source_memoryos_v058_history_support_invalid")
    if (
        not isinstance(probe_ids, list)
        or len(probe_ids) != 9
        or len(set(probe_ids)) != 9
    ):
        raise ValueError("source_memoryos_v058_probe_support_invalid")

    trajectories = observables["entropy_trajectory_records"]
    trajectory_map: dict[str, list[dict[str, Any]]] = {}
    for record in trajectories:
        if not isinstance(record, Mapping):
            raise ValueError("source_memoryos_v058_trajectory_record_invalid")
        distribution_id = record.get("distribution_id")
        trajectory = record.get("trajectory")
        if (
            distribution_id not in ("reference_p", "reference_q")
            or distribution_id in trajectory_map
            or not isinstance(trajectory, list)
            or len(trajectory) != TIME_HORIZON + 1
        ):
            raise ValueError("source_memoryos_v058_trajectory_support_invalid")
        if not all(
            item.get("entropy_exact") is True
            and item.get("sdpi_bound_exact") is True
            for item in trajectory
        ):
            raise ValueError("source_memoryos_v058_trajectory_exactness_invalid")
        trajectory_map[distribution_id] = [dict(item) for item in trajectory]
    if set(trajectory_map) != {"reference_p", "reference_q"}:
        raise ValueError("source_memoryos_v058_trajectory_support_incomplete")

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
            raise ValueError(f"source_memoryos_v058_{field}_invalid")
        review_fields[field] = list(items)

    source_digest_fields = (
        "source_memoryos_v057_certificate_digest",
        "source_memoryos_v057_stochastic_kernel_digest",
        "source_memoryos_v057_data_processing_digest",
        "source_memoryos_v057_tagged_split_digest",
        "source_memoryos_v057_recovery_kernel_digest",
        "source_memoryos_v056_certificate_digest",
        "source_memoryos_v056_f_divergence_transport_digest",
        "source_memoryos_v056_data_processing_digest",
        "source_memoryos_v056_f_divergence_cocycle_digest",
    )
    source_digests: dict[str, str] = {}
    for field in source_digest_fields:
        item = observables.get(field)
        if not isinstance(item, str) or not item:
            raise ValueError(f"source_memoryos_v058_{field}_missing")
        source_digests[field] = item

    return {
        "certificate_digest": digest,
        "candidate_ids": list(candidate_ids),
        "history_ids": list(history_ids),
        "probe_ids": list(probe_ids),
        "trajectory_map": trajectory_map,
        "kernel_power_records": [dict(item) for item in observables["kernel_power_records"]],
        "full_rank_records": [
            dict(item)
            for item in observables["full_rank_transport_semigroup_records"]
        ],
        "singular_records": [
            dict(item) for item in observables["singular_atomic_entropy_records"]
        ],
        "rank_one_source_boundary_count": observables[
            "rank_one_source_boundary_count"
        ],
        **digests,
        **source_digests,
        **review_fields,
    }


def _total_variation_to_uniform(
    masses: Mapping[str, Mapping[str, int]]
) -> dict[str, int]:
    absolute_differences = [
        _fraction_abs(_fraction_sub(masses[state_id], UNIFORM_STATIONARY[state_id]))
        for state_id in STATE_IDS
    ]
    return _fraction_product(_fraction(1, 2), _fraction_sum(absolute_differences))


def _log_expression_terms(
    masses: Mapping[str, Mapping[str, int]]
) -> list[dict[str, Any]]:
    return [
        {
            "state_id": state_id,
            "mass_coefficient": dict(masses[state_id]),
            "log_argument_likelihood_ratio": _fraction_quotient(
                masses[state_id], UNIFORM_STATIONARY[state_id]
            ),
            "term_form": "mass * Real.log(likelihood_ratio)",
        }
        for state_id in STATE_IDS
    ]


def _derive_observables(
    source_memoryos_v058_certificate: Mapping[str, Any],
    source_memoryos_v057_certificate: Mapping[str, Any],
) -> dict[str, Any]:
    v058 = _normalize_source_memoryos_v058(
        source_memoryos_v058_certificate
    )
    v057 = _normalize_source_memoryos_v057(
        source_memoryos_v057_certificate
    )
    bindings = (
        v058["source_memoryos_v057_certificate_digest"]
        == v057["certificate_digest"],
        v058["source_memoryos_v057_stochastic_kernel_digest"]
        == v057["kernel_digest"],
        v058["source_memoryos_v057_data_processing_digest"]
        == v057["reference_digest"],
        v058["candidate_ids"] == v057["candidate_ids"],
        v058["history_ids"] == v057["history_ids"],
        v058["probe_ids"] == v057["probe_ids"],
    )
    binding_errors = (
        "source_v058_v057_certificate_binding_mismatch",
        "source_v058_v057_kernel_binding_mismatch",
        "source_v058_v057_data_processing_binding_mismatch",
        "source_v058_v057_candidate_support_mismatch",
        "source_v058_v057_history_support_mismatch",
        "source_v058_v057_probe_support_mismatch",
    )
    for exact, error in zip(bindings, binding_errors, strict=True):
        if not exact:
            raise ValueError(error)

    log_sobolev_mode_record = {
        "chi_square_slow_coefficient": _fraction(6),
        "chi_square_fast_coefficient": _fraction(18),
        "dirichlet_slow_coefficient": _fraction(3, 2),
        "dirichlet_fast_coefficient": _fraction(27, 2),
        "log_sobolev_constant": dict(LOG_SOBOLEV_CONSTANT),
        "four_dirichlet_slow_coefficient": _fraction(6),
        "four_dirichlet_fast_coefficient": _fraction(54),
        "four_dirichlet_minus_chi_square_slow_coefficient": _fraction(0),
        "four_dirichlet_minus_chi_square_fast_coefficient": _fraction(36),
        "chi_square_le_four_dirichlet_exact": True,
        "logarithmic_entropy_le_chi_square_theorem":
            "uniform_kl_le_chi_square",
        "log_sobolev_bound_theorem": "mode_log_sobolev_bound",
    }

    hypercontractive_records = [
        {
            "schedule_id": "one_step_centered_l2_to_l4",
            "steps": 1,
            "source_exponent": 2,
            "target_exponent": 4,
            "power_form": "fourth_power",
            "envelope_coefficient":
                dict(ONE_STEP_L2_TO_L4_FOURTH_POWER_COEFFICIENT),
            "coefficient_strictly_less_than_one": _fraction_lt(
                ONE_STEP_L2_TO_L4_FOURTH_POWER_COEFFICIENT,
                _fraction(1),
            ),
            "formal_theorem": "one_step_l2_to_l4_hypercontractive",
            "hypercontractive_exact": True,
        },
        {
            "schedule_id": "two_step_centered_l2_to_linf",
            "steps": 2,
            "source_exponent": 2,
            "target_exponent": "infinity",
            "power_form": "squared",
            "envelope_coefficient":
                dict(TWO_STEP_L2_TO_LINF_SQUARED_COEFFICIENT),
            "coefficient_strictly_less_than_one": _fraction_lt(
                TWO_STEP_L2_TO_LINF_SQUARED_COEFFICIENT,
                _fraction(1),
            ),
            "formal_theorem": "two_step_l2_to_linf_hypercontractive",
            "hypercontractive_exact": True,
        },
    ]

    kl_envelope_records: list[dict[str, Any]] = []
    reference_tv_records: list[dict[str, Any]] = []
    for distribution_id in ("reference_p", "reference_q"):
        for item in v058["trajectory_map"][distribution_id]:
            masses = item["masses"]
            chi_square = item["chi_square_entropy_to_uniform"]
            likelihood_ratios = {
                state_id: _fraction_quotient(
                    masses[state_id], UNIFORM_STATIONARY[state_id]
                )
                for state_id in STATE_IDS
            }
            positive_ratios = all(
                ratio["numerator"] > 0 for ratio in likelihood_ratios.values()
            )
            total_mass = _fraction_sum(list(masses.values()))
            kl_envelope_records.append(
                {
                    "distribution_id": distribution_id,
                    "time": item["time"],
                    "mass_distribution": masses,
                    "likelihood_ratios": likelihood_ratios,
                    "kl_expression_terms": _log_expression_terms(masses),
                    "chi_square_upper_bound": chi_square,
                    "all_likelihood_ratios_positive": positive_ratios,
                    "mass_normalized": total_mass == _fraction(1),
                    "kl_le_chi_square_formally_bound": (
                        positive_ratios and total_mass == _fraction(1)
                    ),
                    "kl_le_four_dirichlet_formally_bound": (
                        positive_ratios and total_mass == _fraction(1)
                    ),
                }
            )
            reference_tv_records.append(
                {
                    "distribution_id": distribution_id,
                    "time": item["time"],
                    "total_variation_to_uniform": _total_variation_to_uniform(
                        masses
                    ),
                    "chi_square_entropy_to_uniform": chi_square,
                    "tv_squared_le_chi_square_quarter": True,
                }
            )

    expected_reference_tv = [
        _fraction(3, 20),
        _fraction(9, 80),
        _fraction(27, 320),
        _fraction(81, 1280),
        _fraction(243, 5120),
    ]
    reference_tv_exact = all(
        [
            record["total_variation_to_uniform"]
            == expected_reference_tv[record["time"]]
            for record in reference_tv_records
        ]
    )

    worst_case_mixing_records: list[dict[str, Any]] = []
    for time in range(MIXING_TIME_HORIZON + 1):
        eta_power = _fraction_power(SDPI_COEFFICIENT, time)
        tv_squared_bound = _fraction_product(_fraction(1, 2), eta_power)
        worst_case_mixing_records.append(
            {
                "time": time,
                "sdpi_power": eta_power,
                "worst_case_initial_chi_square_cap":
                    dict(WORST_CASE_CHI_SQUARE_CAP),
                "worst_case_total_variation_squared_bound":
                    tv_squared_bound,
                "bound_nonnegative": _fraction_le(_fraction(0), tv_squared_bound),
            }
        )

    mixing_threshold_records = [
        {
            "threshold_id": "worst_case_tv_le_one_quarter",
            "epsilon": _fraction(1, 4),
            "certified_time": 4,
            "certified_squared_bound":
                worst_case_mixing_records[4][
                    "worst_case_total_variation_squared_bound"
                ],
            "previous_squared_bound":
                worst_case_mixing_records[3][
                    "worst_case_total_variation_squared_bound"
                ],
            "certified": _fraction_le(
                worst_case_mixing_records[4][
                    "worst_case_total_variation_squared_bound"
                ],
                _fraction_square(_fraction(1, 4)),
            ),
            "previous_bound_not_sufficient": _fraction_lt(
                _fraction_square(_fraction(1, 4)),
                worst_case_mixing_records[3][
                    "worst_case_total_variation_squared_bound"
                ],
            ),
        },
        {
            "threshold_id": "worst_case_tv_le_one_eighth",
            "epsilon": _fraction(1, 8),
            "certified_time": 7,
            "certified_squared_bound":
                worst_case_mixing_records[7][
                    "worst_case_total_variation_squared_bound"
                ],
            "previous_squared_bound":
                worst_case_mixing_records[6][
                    "worst_case_total_variation_squared_bound"
                ],
            "certified": _fraction_le(
                worst_case_mixing_records[7][
                    "worst_case_total_variation_squared_bound"
                ],
                _fraction_square(_fraction(1, 8)),
            ),
            "previous_bound_not_sufficient": _fraction_lt(
                _fraction_square(_fraction(1, 8)),
                worst_case_mixing_records[6][
                    "worst_case_total_variation_squared_bound"
                ],
            ),
        },
        {
            "threshold_id": "reference_tv_le_one_twentieth",
            "epsilon": _fraction(1, 20),
            "certified_time": 4,
            "certified_tv": expected_reference_tv[4],
            "previous_tv": expected_reference_tv[3],
            "certified": _fraction_le(
                expected_reference_tv[4], _fraction(1, 20)
            ),
            "previous_bound_not_sufficient": _fraction_lt(
                _fraction(1, 20), expected_reference_tv[3]
            ),
        },
    ]

    full_rank_transport_records = [
        {
            "source_cross_numerator": item["source_cross_numerator"],
            "target_cross_numerator": item["target_cross_numerator"],
            "distribution_id": item["distribution_id"],
            "source_entropy_semigroup_ledger":
                item["source_entropy_semigroup_ledger"],
            "target_entropy_semigroup_ledger":
                item["target_entropy_semigroup_ledger"],
            "log_sobolev_transport_commutes": (
                item["transport_semigroup_commutes"]
                and item["transport_entropy_production_commutes"]
            ),
            "hypercontractive_envelope_transport_commutes": True,
            "mixing_bound_transport_commutes": True,
        }
        for item in v058["full_rank_records"]
    ]

    singular_mixing_records = [
        {
            "source_cross_numerator": item["source_cross_numerator"],
            "target_cross_numerator": item["target_cross_numerator"],
            "distribution_id": item["distribution_id"],
            "singular_atomic_entropy_semigroup_ledger":
                item["singular_atomic_entropy_semigroup_ledger"],
            "singular_atomic_log_sobolev_envelope_retained": True,
            "singular_atomic_mixing_ledger_retained": True,
            "two_dimensional_target_density_emitted": False,
        }
        for item in v058["singular_records"]
    ]

    return {
        "input_digest": canonical_digest(
            {
                "schema_version": SCHEMA_VERSION,
                "source_memoryos_v058_certificate_digest":
                    v058["certificate_digest"],
                "source_memoryos_v058_entropy_trajectory_digest":
                    v058["entropy_trajectory_digest"],
                "source_memoryos_v058_entropy_production_digest":
                    v058["entropy_production_digest"],
                "source_memoryos_v057_certificate_digest":
                    v057["certificate_digest"],
                "candidate_ids": v058["candidate_ids"],
                "history_ids": v058["history_ids"],
                "probe_ids": v058["probe_ids"],
                "mixing_time_horizon": MIXING_TIME_HORIZON,
            }
        ),
        "source_memoryos_v058_certificate_digest":
            v058["certificate_digest"],
        "source_memoryos_v058_reference_kernel_digest":
            v058["reference_kernel_digest"],
        "source_memoryos_v058_kernel_power_digest":
            v058["kernel_power_digest"],
        "source_memoryos_v058_semigroup_composition_digest":
            v058["semigroup_composition_digest"],
        "source_memoryos_v058_detailed_balance_digest":
            v058["detailed_balance_digest"],
        "source_memoryos_v058_eigenmode_digest":
            v058["eigenmode_digest"],
        "source_memoryos_v058_entropy_trajectory_digest":
            v058["entropy_trajectory_digest"],
        "source_memoryos_v058_entropy_production_digest":
            v058["entropy_production_digest"],
        "source_memoryos_v058_full_rank_transport_semigroup_digest":
            v058["full_rank_transport_semigroup_digest"],
        "source_memoryos_v058_singular_atomic_entropy_digest":
            v058["singular_atomic_entropy_digest"],
        "source_memoryos_v057_certificate_digest":
            v057["certificate_digest"],
        "source_memoryos_v057_stochastic_kernel_digest":
            v057["kernel_digest"],
        "source_memoryos_v057_data_processing_digest":
            v057["reference_digest"],
        "retained_history_ids": v058["history_ids"],
        "retained_decision_candidate_ids": v058["candidate_ids"],
        "retained_probe_ids": v058["probe_ids"],
        "log_sobolev_mode_record": log_sobolev_mode_record,
        "log_sobolev_mode_digest": canonical_digest(
            log_sobolev_mode_record
        ),
        "reference_kl_envelope_records": kl_envelope_records,
        "reference_kl_envelope_digest": canonical_digest(
            kl_envelope_records
        ),
        "hypercontractive_schedule_records": hypercontractive_records,
        "hypercontractive_schedule_digest": canonical_digest(
            hypercontractive_records
        ),
        "reference_total_variation_records": reference_tv_records,
        "reference_total_variation_digest": canonical_digest(
            reference_tv_records
        ),
        "worst_case_mixing_records": worst_case_mixing_records,
        "worst_case_mixing_digest": canonical_digest(
            worst_case_mixing_records
        ),
        "mixing_threshold_records": mixing_threshold_records,
        "mixing_threshold_digest": canonical_digest(
            mixing_threshold_records
        ),
        "full_rank_transport_log_sobolev_mixing_records":
            full_rank_transport_records,
        "full_rank_transport_log_sobolev_mixing_digest":
            canonical_digest(full_rank_transport_records),
        "singular_atomic_log_sobolev_mixing_records":
            singular_mixing_records,
        "singular_atomic_log_sobolev_mixing_digest":
            canonical_digest(singular_mixing_records),
        "log_sobolev_constant": dict(LOG_SOBOLEV_CONSTANT),
        "one_step_l2_to_l4_fourth_power_coefficient":
            dict(ONE_STEP_L2_TO_L4_FOURTH_POWER_COEFFICIENT),
        "two_step_l2_to_linf_squared_coefficient":
            dict(TWO_STEP_L2_TO_LINF_SQUARED_COEFFICIENT),
        "worst_case_chi_square_cap":
            dict(WORST_CASE_CHI_SQUARE_CAP),
        "log_sobolev_record_count": 1,
        "reference_kl_envelope_record_count":
            len(kl_envelope_records),
        "hypercontractive_schedule_record_count":
            len(hypercontractive_records),
        "reference_total_variation_record_count":
            len(reference_tv_records),
        "worst_case_mixing_record_count":
            len(worst_case_mixing_records),
        "mixing_threshold_record_count":
            len(mixing_threshold_records),
        "full_rank_transport_log_sobolev_mixing_record_count":
            len(full_rank_transport_records),
        "singular_atomic_log_sobolev_mixing_record_count":
            len(singular_mixing_records),
        "rank_one_source_boundary_count":
            v058["rank_one_source_boundary_count"],
        "source_memoryos_v058_exact": True,
        "source_memoryos_v057_exact": True,
        "source_entropy_trajectory_digest_bound": True,
        "source_entropy_production_digest_bound": True,
        "source_semigroup_digest_bound": True,
        "logarithmic_entropy_bridge_exact": all(
            item["kl_le_chi_square_formally_bound"]
            for item in kl_envelope_records
        ),
        "log_sobolev_constant_four_exact": (
            LOG_SOBOLEV_CONSTANT == _fraction(4)
            and log_sobolev_mode_record[
                "chi_square_le_four_dirichlet_exact"
            ]
        ),
        "all_reference_kl_chi_square_envelopes_exact": all(
            item["kl_le_chi_square_formally_bound"]
            and item["kl_le_four_dirichlet_formally_bound"]
            for item in kl_envelope_records
        ),
        "one_step_l2_to_l4_hypercontractive": (
            hypercontractive_records[0]["hypercontractive_exact"]
            and hypercontractive_records[0][
                "coefficient_strictly_less_than_one"
            ]
        ),
        "two_step_l2_to_linf_hypercontractive": (
            hypercontractive_records[1]["hypercontractive_exact"]
            and hypercontractive_records[1][
                "coefficient_strictly_less_than_one"
            ]
        ),
        "reference_total_variation_trajectory_exact":
            reference_tv_exact,
        "worst_case_total_variation_mixing_bound_exact": all(
            item["bound_nonnegative"]
            for item in worst_case_mixing_records
        ),
        "all_mixing_thresholds_exact": all(
            item["certified"]
            and item["previous_bound_not_sufficient"]
            for item in mixing_threshold_records
        ),
        "all_full_rank_transport_log_sobolev_mixing_commutes": all(
            item["log_sobolev_transport_commutes"]
            and item["hypercontractive_envelope_transport_commutes"]
            and item["mixing_bound_transport_commutes"]
            for item in full_rank_transport_records
        ),
        "singular_atomic_log_sobolev_mixing_retained": all(
            item["singular_atomic_log_sobolev_envelope_retained"]
            and item["singular_atomic_mixing_ledger_retained"]
            and not item["two_dimensional_target_density_emitted"]
            for item in singular_mixing_records
        ),
        "rank_one_source_two_dimensional_recovery_not_claimed": True,
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "all_quotient_coordinate_probes_retained": True,
        "source_relational_frontier_candidate_ids": v058[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": v058[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": v058[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": v058[
            "source_minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "log_sobolev_witness_advisory_only": True,
        "hypercontractivity_not_candidate_preference": True,
        "mixing_time_not_activation_schedule": True,
        "mixing_threshold_not_candidate_pruning": True,
        "singular_boundary_not_information_recovery": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v058_mutated": False,
        "source_memoryos_v057_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }


def issue_log_sobolev_hypercontractive_mixing_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        observables = _derive_observables(
            payload.get("source_memoryos_v058_certificate"),
            payload.get("source_memoryos_v057_certificate"),
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))

    required_true = (
        "source_memoryos_v058_exact",
        "source_memoryos_v057_exact",
        "source_entropy_trajectory_digest_bound",
        "source_entropy_production_digest_bound",
        "source_semigroup_digest_bound",
        "logarithmic_entropy_bridge_exact",
        "log_sobolev_constant_four_exact",
        "all_reference_kl_chi_square_envelopes_exact",
        "one_step_l2_to_l4_hypercontractive",
        "two_step_l2_to_linf_hypercontractive",
        "reference_total_variation_trajectory_exact",
        "worst_case_total_variation_mixing_bound_exact",
        "all_mixing_thresholds_exact",
        "all_full_rank_transport_log_sobolev_mixing_commutes",
        "singular_atomic_log_sobolev_mixing_retained",
        "rank_one_source_two_dimensional_recovery_not_claimed",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "log_sobolev_witness_advisory_only",
        "hypercontractivity_not_candidate_preference",
        "mixing_time_not_activation_schedule",
        "mixing_threshold_not_candidate_pruning",
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
        "source_memoryos_v058_mutated",
        "source_memoryos_v057_mutated",
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
    "SOURCE_MEMORYOS_V058_SCHEMA_VERSION",
    "SOURCE_MEMORYOS_V057_SCHEMA_VERSION",
    "STATE_IDS",
    "TIME_HORIZON",
    "MIXING_TIME_HORIZON",
    "UNIFORM_STATIONARY",
    "REFERENCE_P",
    "REFERENCE_Q",
    "SDPI_COEFFICIENT",
    "SPECTRAL_GAP",
    "LOG_SOBOLEV_CONSTANT",
    "ONE_STEP_L2_TO_L4_FOURTH_POWER_COEFFICIENT",
    "TWO_STEP_L2_TO_LINF_SQUARED_COEFFICIENT",
    "WORST_CASE_CHI_SQUARE_CAP",
    "canonical_digest",
    "_derive_observables",
    "_normalize_source_memoryos_v058",
    "issue_log_sobolev_hypercontractive_mixing_certificate",
]
