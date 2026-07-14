from __future__ import annotations

from hashlib import sha256
import json
from math import gcd
from typing import Any, Mapping

from runtime.kuuos_memoryos_f_divergence_transport_data_processing_contraction_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_MEMORYOS_V056_SCHEMA_VERSION,
    SOURCE_MEMORYOS_V055_SCHEMA_VERSION,
    GENERATOR_IDS,
    COARSE_BIN_IDS,
    EXPECTED_CROSSES,
    _normalize_source_memoryos_v055,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.stochastic-markov-kernel-f-divergence-"
    "data-processing-sufficiency-certificate.v0.1"
)

SPLIT_TAGS = ("left", "right")
SPLIT_WEIGHTS = {
    "left": {"numerator": 1, "denominator": 3},
    "right": {"numerator": 2, "denominator": 3},
}
STOCHASTIC_KERNEL_WEIGHTS = {
    "early": {
        "early": {"numerator": 3, "denominator": 4},
        "middle": {"numerator": 1, "denominator": 4},
        "late": {"numerator": 0, "denominator": 1},
    },
    "middle": {
        "early": {"numerator": 1, "denominator": 4},
        "middle": {"numerator": 1, "denominator": 2},
        "late": {"numerator": 1, "denominator": 4},
    },
    "late": {
        "early": {"numerator": 0, "denominator": 1},
        "middle": {"numerator": 1, "denominator": 4},
        "late": {"numerator": 3, "denominator": 4},
    },
}


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


def _fraction(numerator: int, denominator: int) -> dict[str, int]:
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
    total = {"numerator": 0, "denominator": 1}
    for value in values:
        total = _fraction_add(total, value)
    return total


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


def _determinant(cross: int) -> int:
    return 4 - cross * cross


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


def _generator_contribution(
    generator_id: str,
    p_mass: Mapping[str, int],
    q_mass: Mapping[str, int],
) -> dict[str, int]:
    difference = _fraction_sub(p_mass, q_mass)
    square = _fraction_square(difference)
    if generator_id == "pearson_chi_square":
        return _fraction_quotient(square, q_mass)
    if generator_id == "neyman_chi_square":
        return _fraction_quotient(square, p_mass)
    if generator_id == "triangular_discrimination":
        return _fraction_quotient(square, _fraction_add(p_mass, q_mass))
    raise ValueError("generator_id_unknown")


def _normalize_source_memoryos_v056(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v056_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v056_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V056_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v056_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v056_certificate_digest_missing")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v056_certificate_digest_mismatch")

    observables = source.get("observables")
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v056_observables_invalid")
    observables = dict(observables)
    _require_boolean_fields(
        observables,
        (
            "source_memoryos_v055_exact",
            "source_memoryos_v054_exact",
            "source_relative_entropy_transport_digest_bound",
            "source_relative_entropy_cocycle_digest_bound",
            "source_density_transport_digest_bound",
            "generator_catalog_exact",
            "deterministic_channel_mass_preserving",
            "all_full_rank_f_divergence_terms_invariant",
            "all_catalog_data_processing_contractions_exact",
            "all_full_rank_transport_coarse_graining_commutes",
            "all_pearson_pairwise_merge_gaps_exact_nonnegative",
            "pearson_pairwise_gaps_sum_to_total_contraction",
            "all_f_divergence_cocycles_exact",
            "full_rank_round_trip_f_divergence_preserved",
            "singular_atomic_f_divergence_retained",
            "rank_one_source_two_dimensional_f_divergence_not_recovered",
            "all_decision_candidates_retained",
            "all_planos_histories_retained",
            "all_quotient_coordinate_probes_retained",
            "relational_frontier_preserved",
            "required_review_set_preserved",
            "dissent_visibility_preserved",
            "minority_visibility_preserved",
            "f_divergence_witness_advisory_only",
            "data_processing_not_candidate_pruning",
            "contraction_not_candidate_preference",
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
            "source_memoryos_v055_mutated",
            "source_memoryos_v054_mutated",
            "source_decisionos_v06_mutated",
            "persistent_world_state_mutated",
            "verification_result_claimed",
            "truth_authority_granted",
        ),
        "source_memoryos_v056",
    )

    expected_counts = {
        "generator_count": 3,
        "transition_count": 9,
        "full_rank_f_divergence_transition_count": 4,
        "full_rank_probe_f_divergence_record_count": 108,
        "singular_f_divergence_transition_count": 2,
        "singular_atomic_f_divergence_record_count": 54,
        "rank_one_source_boundary_count": 3,
        "coarse_graining_bin_count": 3,
        "deterministic_channel_row_count": 9,
        "data_processing_record_count": 12,
        "pearson_pairwise_merge_witness_count": 6,
        "f_divergence_cocycle_record_count": 27,
        "active_f_divergence_cocycle_count": 8,
        "nontrivial_round_trip_f_divergence_path_count": 2,
    }
    for field, expected in expected_counts.items():
        if observables.get(field) != expected:
            raise ValueError(f"source_memoryos_v056_{field}_mismatch")

    candidate_ids = observables.get("retained_decision_candidate_ids")
    if candidate_ids != [
        "continue",
        "hold",
        "reobserve",
        "terminate_candidate",
    ]:
        raise ValueError("source_memoryos_v056_candidate_order_mismatch")
    history_ids = observables.get("retained_history_ids")
    if (
        not isinstance(history_ids, list)
        or len(history_ids) != 2
        or len(set(history_ids)) != 2
    ):
        raise ValueError("source_memoryos_v056_history_support_invalid")
    probe_ids = observables.get("retained_probe_ids")
    if (
        not isinstance(probe_ids, list)
        or len(probe_ids) != 9
        or len(set(probe_ids)) != 9
        or any(not isinstance(item, str) for item in probe_ids)
    ):
        raise ValueError("source_memoryos_v056_probe_support_invalid")
    if observables.get("f_divergence_generator_ids") != list(GENERATOR_IDS):
        raise ValueError("source_memoryos_v056_generator_catalog_mismatch")

    expected_reference = {
        "pearson_chi_square": (
            _fraction(2593, 1134),
            _fraction(3, 2),
            _fraction(446, 567),
        ),
        "neyman_chi_square": (
            _fraction(2593, 1134),
            _fraction(3, 2),
            _fraction(446, 567),
        ),
        "triangular_discrimination": (
            _fraction(8, 15),
            _fraction(12, 25),
            _fraction(4, 75),
        ),
    }
    reference_records = observables.get(
        "f_divergence_generator_reference_records"
    )
    if not isinstance(reference_records, list) or len(reference_records) != 3:
        raise ValueError("source_memoryos_v056_reference_records_invalid")
    reference_map: dict[str, dict[str, Any]] = {}
    for item in reference_records:
        if not isinstance(item, Mapping):
            raise ValueError("source_memoryos_v056_reference_record_invalid")
        record = dict(item)
        generator_id = record.get("generator_id")
        if generator_id not in GENERATOR_IDS or generator_id in reference_map:
            raise ValueError("source_memoryos_v056_reference_support_invalid")
        expected_fine, expected_coarse, expected_gap = expected_reference[
            generator_id
        ]
        if record.get("fine_divergence_total") != expected_fine:
            raise ValueError(
                f"source_memoryos_v056_{generator_id}_fine_mismatch"
            )
        if record.get("coarse_divergence_total") != expected_coarse:
            raise ValueError(
                f"source_memoryos_v056_{generator_id}_coarse_mismatch"
            )
        if record.get("data_processing_contraction_gap") != expected_gap:
            raise ValueError(
                f"source_memoryos_v056_{generator_id}_gap_mismatch"
            )
        if (
            record.get("coarse_not_greater_than_fine") is not True
            or record.get("contraction_gap_nonnegative") is not True
        ):
            raise ValueError(
                f"source_memoryos_v056_{generator_id}_contraction_invalid"
            )
        reference_map[generator_id] = record

    bins = observables.get("deterministic_coarse_graining_bins")
    if (
        not isinstance(bins, list)
        or [item.get("bin_id") for item in bins] != list(COARSE_BIN_IDS)
        or any(len(item.get("probe_ids", [])) != 3 for item in bins)
    ):
        raise ValueError("source_memoryos_v056_coarse_bins_invalid")
    channel_rows = observables.get("deterministic_channel_rows")
    if not isinstance(channel_rows, list) or len(channel_rows) != 9:
        raise ValueError("source_memoryos_v056_channel_rows_invalid")
    if [item.get("probe_id") for item in channel_rows] != probe_ids:
        raise ValueError("source_memoryos_v056_channel_probe_order_mismatch")
    if any(
        item.get("transition_weight")
        != {"numerator": 1, "denominator": 1}
        for item in channel_rows
    ):
        raise ValueError("source_memoryos_v056_channel_weight_mismatch")

    transitions = observables.get("f_divergence_transport_trajectory")
    transition_digest = observables.get("f_divergence_transport_digest")
    if not isinstance(transitions, list) or len(transitions) != 9:
        raise ValueError("source_memoryos_v056_transition_trajectory_invalid")
    if canonical_digest(transitions) != transition_digest:
        raise ValueError("source_memoryos_v056_transition_digest_mismatch")
    expected_pairs = {
        (source_cross, target_cross)
        for source_cross in EXPECTED_CROSSES
        for target_cross in EXPECTED_CROSSES
    }
    transition_map: dict[tuple[int, int], dict[str, Any]] = {}
    for item in transitions:
        if not isinstance(item, Mapping):
            raise ValueError("source_memoryos_v056_transition_invalid")
        record = dict(item)
        pair = (
            record.get("source_cross_numerator"),
            record.get("target_cross_numerator"),
        )
        if pair not in expected_pairs or pair in transition_map:
            raise ValueError("source_memoryos_v056_transition_support_invalid")
        source_cross, target_cross = pair
        active = (
            _determinant(source_cross) != 0
            and _determinant(target_cross) != 0
        )
        singular = (
            _determinant(source_cross) != 0
            and _determinant(target_cross) == 0
        )
        rank_one_source = _determinant(source_cross) == 0
        if record.get("full_rank_f_divergence_transport_active") is not active:
            raise ValueError(
                "source_memoryos_v056_full_rank_transition_flag_mismatch"
            )
        if record.get("singular_f_divergence_boundary_active") is not singular:
            raise ValueError(
                "source_memoryos_v056_singular_transition_flag_mismatch"
            )
        if record.get("rank_one_source_boundary") is not rank_one_source:
            raise ValueError(
                "source_memoryos_v056_rank_one_source_flag_mismatch"
            )
        full_rank_records = record.get(
            "full_rank_probe_f_divergence_records"
        )
        singular_records = record.get(
            "singular_atomic_f_divergence_records"
        )
        if active:
            if (
                not isinstance(full_rank_records, list)
                or len(full_rank_records) != 27
                or singular_records != []
                or record.get("all_generator_ledgers_invariant") is not True
            ):
                raise ValueError(
                    "source_memoryos_v056_full_rank_records_invalid"
                )
        elif singular:
            if (
                full_rank_records != []
                or not isinstance(singular_records, list)
                or len(singular_records) != 27
                or record.get("singular_atomic_f_divergence_exact") is not True
            ):
                raise ValueError(
                    "source_memoryos_v056_singular_records_invalid"
                )
        else:
            if full_rank_records != [] or singular_records != []:
                raise ValueError(
                    "source_memoryos_v056_rank_one_records_invalid"
                )
            if record.get(
                "rank_one_source_two_dimensional_f_divergence_recovery_claimed"
            ) is not False:
                raise ValueError(
                    "source_memoryos_v056_rank_one_recovery_claimed"
                )
        transition_map[pair] = record
    if set(transition_map) != expected_pairs:
        raise ValueError("source_memoryos_v056_transition_support_incomplete")

    data_processing_records = observables.get(
        "full_rank_data_processing_records"
    )
    data_processing_digest = observables.get("data_processing_digest")
    if (
        not isinstance(data_processing_records, list)
        or len(data_processing_records) != 12
    ):
        raise ValueError(
            "source_memoryos_v056_data_processing_records_invalid"
        )
    if canonical_digest(data_processing_records) != data_processing_digest:
        raise ValueError(
            "source_memoryos_v056_data_processing_digest_mismatch"
        )
    if not all(
        item.get("source_data_processing_contraction_exact") is True
        and item.get("target_data_processing_contraction_exact") is True
        and item.get("transport_coarse_graining_commutes") is True
        for item in data_processing_records
    ):
        raise ValueError(
            "source_memoryos_v056_data_processing_exactness_mismatch"
        )

    cocycles = observables.get("f_divergence_cocycle_records")
    cocycle_digest = observables.get("f_divergence_cocycle_digest")
    if not isinstance(cocycles, list) or len(cocycles) != 27:
        raise ValueError("source_memoryos_v056_cocycle_records_invalid")
    if canonical_digest(cocycles) != cocycle_digest:
        raise ValueError("source_memoryos_v056_cocycle_digest_mismatch")

    digest_fields = (
        "source_memoryos_v055_certificate_digest",
        "source_memoryos_v055_relative_entropy_transport_digest",
        "source_memoryos_v055_relative_entropy_cocycle_digest",
        "source_memoryos_v054_certificate_digest",
        "source_memoryos_v054_density_transport_digest",
        "source_memoryos_v054_density_cocycle_digest",
    )
    digests: dict[str, str] = {}
    for field in digest_fields:
        value = observables.get(field)
        if not isinstance(value, str) or not value:
            raise ValueError(f"source_memoryos_v056_{field}_missing")
        digests[field] = value

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
            raise ValueError(f"source_memoryos_v056_{field}_invalid")
        review_fields[field] = list(items)

    return {
        "certificate_digest": digest,
        "transition_digest": transition_digest,
        "data_processing_digest": data_processing_digest,
        "cocycle_digest": cocycle_digest,
        "candidate_ids": list(candidate_ids),
        "history_ids": list(history_ids),
        "probe_ids": list(probe_ids),
        "reference_records": reference_map,
        "bins": [dict(item) for item in bins],
        "transitions": transition_map,
        **digests,
        **review_fields,
    }


def _probe_bin_id(ordinal: int) -> str:
    if ordinal <= 3:
        return "early"
    if ordinal <= 6:
        return "middle"
    return "late"


def _stochastic_kernel_rows(probe_ids: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ordinal, probe_id in enumerate(probe_ids, start=1):
        source_bin = _probe_bin_id(ordinal)
        weights = STOCHASTIC_KERNEL_WEIGHTS[source_bin]
        rows.append(
            {
                "probe_id": probe_id,
                "source_deterministic_bin_id": source_bin,
                "target_weights": {
                    target_id: dict(weights[target_id])
                    for target_id in COARSE_BIN_IDS
                },
                "row_mass": _fraction_sum(
                    [weights[target_id] for target_id in COARSE_BIN_IDS]
                ),
                "row_stochastic": _fraction_sum(
                    [weights[target_id] for target_id in COARSE_BIN_IDS]
                )
                == {"numerator": 1, "denominator": 1},
                "probe_retained": True,
            }
        )
    return rows


def _pushforward(
    probe_ids: list[str],
    masses: Mapping[str, Mapping[str, int]],
    rows: list[Mapping[str, Any]],
) -> dict[str, dict[str, int]]:
    row_map = {row["probe_id"]: row for row in rows}
    return {
        target_id: _fraction_sum(
            [
                _fraction_product(
                    masses[probe_id],
                    row_map[probe_id]["target_weights"][target_id],
                )
                for probe_id in probe_ids
            ]
        )
        for target_id in COARSE_BIN_IDS
    }


def _tagged_split(
    probe_ids: list[str],
    masses: Mapping[str, Mapping[str, int]],
) -> dict[str, dict[str, int]]:
    return {
        f"{probe_id}::{tag}": _fraction_product(
            masses[probe_id], SPLIT_WEIGHTS[tag]
        )
        for probe_id in probe_ids
        for tag in SPLIT_TAGS
    }


def _recover_tagged_split(
    probe_ids: list[str],
    split_masses: Mapping[str, Mapping[str, int]],
) -> dict[str, dict[str, int]]:
    return {
        probe_id: _fraction_sum(
            [
                split_masses[f"{probe_id}::{tag}"]
                for tag in SPLIT_TAGS
            ]
        )
        for probe_id in probe_ids
    }


def _derive_observables(
    source_memoryos_v056_certificate: Mapping[str, Any],
    source_memoryos_v055_certificate: Mapping[str, Any],
) -> dict[str, Any]:
    v056 = _normalize_source_memoryos_v056(
        source_memoryos_v056_certificate
    )
    v055 = _normalize_source_memoryos_v055(
        source_memoryos_v055_certificate
    )
    bindings = (
        v056["source_memoryos_v055_certificate_digest"]
        == v055["certificate_digest"],
        v056["source_memoryos_v055_relative_entropy_transport_digest"]
        == v055["relative_entropy_transport_digest"],
        v056["source_memoryos_v055_relative_entropy_cocycle_digest"]
        == v055["relative_entropy_cocycle_digest"],
        v056["candidate_ids"] == v055["candidate_ids"],
        v056["history_ids"] == v055["history_ids"],
        v056["probe_ids"] == v055["probe_ids"],
    )
    binding_errors = (
        "source_v056_v055_certificate_binding_mismatch",
        "source_v056_v055_relative_entropy_transport_binding_mismatch",
        "source_v056_v055_relative_entropy_cocycle_binding_mismatch",
        "source_v056_v055_candidate_support_mismatch",
        "source_v056_v055_history_support_mismatch",
        "source_v056_v055_probe_support_mismatch",
    )
    for exact, error in zip(bindings, binding_errors, strict=True):
        if not exact:
            raise ValueError(error)

    probe_ids = v056["probe_ids"]
    p_masses = v055["p_masses"]
    q_masses = v055["q_masses"]
    stochastic_rows = _stochastic_kernel_rows(probe_ids)
    stochastic_p = _pushforward(
        probe_ids, p_masses, stochastic_rows
    )
    stochastic_q = _pushforward(
        probe_ids, q_masses, stochastic_rows
    )
    expected_stochastic_p = {
        "early": _fraction(11, 60),
        "middle": _fraction(1, 3),
        "late": _fraction(29, 60),
    }
    expected_stochastic_q = {
        "early": _fraction(29, 60),
        "middle": _fraction(1, 3),
        "late": _fraction(11, 60),
    }
    if stochastic_p != expected_stochastic_p:
        raise ValueError("reference_stochastic_p_mass_mismatch")
    if stochastic_q != expected_stochastic_q:
        raise ValueError("reference_stochastic_q_mass_mismatch")

    stochastic_reference_records: list[dict[str, Any]] = []
    expected_stochastic_totals = {
        "pearson_chi_square": _fraction(216, 319),
        "neyman_chi_square": _fraction(216, 319),
        "triangular_discrimination": _fraction(27, 100),
    }
    expected_fine_to_stochastic_gaps = {
        "pearson_chi_square": _fraction(582223, 361746),
        "neyman_chi_square": _fraction(582223, 361746),
        "triangular_discrimination": _fraction(79, 300),
    }
    expected_coarse_to_stochastic_gaps = {
        "pearson_chi_square": _fraction(525, 638),
        "neyman_chi_square": _fraction(525, 638),
        "triangular_discrimination": _fraction(21, 100),
    }
    for generator_id in GENERATOR_IDS:
        source_reference = v056["reference_records"][generator_id]
        fine_total = source_reference["fine_divergence_total"]
        deterministic_coarse_total = source_reference[
            "coarse_divergence_total"
        ]
        output_contributions = {
            target_id: _generator_contribution(
                generator_id,
                stochastic_p[target_id],
                stochastic_q[target_id],
            )
            for target_id in COARSE_BIN_IDS
        }
        stochastic_total = _fraction_sum(
            list(output_contributions.values())
        )
        fine_gap = _fraction_sub(fine_total, stochastic_total)
        coarse_gap = _fraction_sub(
            deterministic_coarse_total, stochastic_total
        )
        if stochastic_total != expected_stochastic_totals[generator_id]:
            raise ValueError(
                f"reference_{generator_id}_stochastic_total_mismatch"
            )
        if fine_gap != expected_fine_to_stochastic_gaps[generator_id]:
            raise ValueError(
                f"reference_{generator_id}_fine_gap_mismatch"
            )
        if coarse_gap != expected_coarse_to_stochastic_gaps[generator_id]:
            raise ValueError(
                f"reference_{generator_id}_coarse_gap_mismatch"
            )
        stochastic_reference_records.append(
            {
                "generator_id": generator_id,
                "fine_divergence_total": fine_total,
                "deterministic_coarse_divergence_total": deterministic_coarse_total,
                "stochastic_output_contributions": output_contributions,
                "stochastic_divergence_total": stochastic_total,
                "fine_to_stochastic_contraction_gap": fine_gap,
                "coarse_to_stochastic_contraction_gap": coarse_gap,
                "stochastic_not_greater_than_deterministic_coarse": _fraction_le(
                    stochastic_total, deterministic_coarse_total
                ),
                "deterministic_coarse_not_greater_than_fine": _fraction_le(
                    deterministic_coarse_total, fine_total
                ),
                "stochastic_strictly_less_than_deterministic_coarse": _fraction_lt(
                    stochastic_total, deterministic_coarse_total
                ),
                "stochastic_strictly_less_than_fine": _fraction_lt(
                    stochastic_total, fine_total
                ),
            }
        )

    split_p = _tagged_split(probe_ids, p_masses)
    split_q = _tagged_split(probe_ids, q_masses)
    recovered_p = _recover_tagged_split(probe_ids, split_p)
    recovered_q = _recover_tagged_split(probe_ids, split_q)
    split_channel_entries = [
        {
            "source_probe_id": probe_id,
            "target_tagged_probe_id": f"{probe_id}::{tag}",
            "transition_weight": dict(SPLIT_WEIGHTS[tag]),
            "source_probe_retained": True,
        }
        for probe_id in probe_ids
        for tag in SPLIT_TAGS
    ]
    recovery_kernel_entries = [
        {
            "source_tagged_probe_id": f"{probe_id}::{tag}",
            "target_probe_id": probe_id,
            "transition_weight": {"numerator": 1, "denominator": 1},
        }
        for probe_id in probe_ids
        for tag in SPLIT_TAGS
    ]

    sufficient_probe_records: list[dict[str, Any]] = []
    sufficient_generator_records: list[dict[str, Any]] = []
    for generator_id in GENERATOR_IDS:
        source_ledger: list[dict[str, int]] = []
        split_ledger: list[dict[str, int]] = []
        for probe_id in probe_ids:
            source_contribution = _generator_contribution(
                generator_id,
                p_masses[probe_id],
                q_masses[probe_id],
            )
            left_id = f"{probe_id}::left"
            right_id = f"{probe_id}::right"
            left_contribution = _generator_contribution(
                generator_id, split_p[left_id], split_q[left_id]
            )
            right_contribution = _generator_contribution(
                generator_id, split_p[right_id], split_q[right_id]
            )
            split_sum = _fraction_add(
                left_contribution, right_contribution
            )
            recovered_contribution = _generator_contribution(
                generator_id,
                recovered_p[probe_id],
                recovered_q[probe_id],
            )
            source_ledger.append(source_contribution)
            split_ledger.extend(
                [left_contribution, right_contribution]
            )
            sufficient_probe_records.append(
                {
                    "generator_id": generator_id,
                    "probe_id": probe_id,
                    "source_contribution": source_contribution,
                    "left_tag_contribution": left_contribution,
                    "right_tag_contribution": right_contribution,
                    "split_contribution_sum": split_sum,
                    "recovered_contribution": recovered_contribution,
                    "split_equality_exact": split_sum
                    == source_contribution,
                    "recovery_equality_exact": recovered_contribution
                    == source_contribution,
                }
            )
        source_total = _fraction_sum(source_ledger)
        split_total = _fraction_sum(split_ledger)
        recovered_total = _fraction_sum(
            [
                _generator_contribution(
                    generator_id,
                    recovered_p[probe_id],
                    recovered_q[probe_id],
                )
                for probe_id in probe_ids
            ]
        )
        sufficient_generator_records.append(
            {
                "generator_id": generator_id,
                "source_f_divergence_total": source_total,
                "split_f_divergence_total": split_total,
                "recovered_f_divergence_total": recovered_total,
                "forward_data_processing_equality": split_total
                == source_total,
                "recovery_data_processing_equality": recovered_total
                == split_total,
                "explicit_sufficiency_equality_exact": (
                    source_total == split_total == recovered_total
                ),
            }
        )

    stochastic_reference_map = {
        item["generator_id"]: item
        for item in stochastic_reference_records
    }
    sufficient_reference_map = {
        item["generator_id"]: item
        for item in sufficient_generator_records
    }

    full_rank_transport_records: list[dict[str, Any]] = []
    singular_stochastic_records: list[dict[str, Any]] = []
    for source_cross in EXPECTED_CROSSES:
        for target_cross in EXPECTED_CROSSES:
            transition = v056["transitions"][
                source_cross, target_cross
            ]
            active = transition[
                "full_rank_f_divergence_transport_active"
            ]
            singular = transition[
                "singular_f_divergence_boundary_active"
            ]
            rho = transition[
                "source_radon_nikodym_density_multiplier"
            ]
            jacobian = transition["source_normalized_jacobian"]
            for generator_id in GENERATOR_IDS:
                if active:
                    target_stochastic_p = {
                        target_id: _fraction_product(
                            stochastic_p[target_id], rho
                        )
                        for target_id in COARSE_BIN_IDS
                    }
                    target_stochastic_q = {
                        target_id: _fraction_product(
                            stochastic_q[target_id], rho
                        )
                        for target_id in COARSE_BIN_IDS
                    }
                    target_stochastic_total = _fraction_sum(
                        [
                            _fraction_product(
                                _generator_contribution(
                                    generator_id,
                                    target_stochastic_p[target_id],
                                    target_stochastic_q[target_id],
                                ),
                                jacobian,
                            )
                            for target_id in COARSE_BIN_IDS
                        ]
                    )
                    target_split_total = _fraction_sum(
                        [
                            _fraction_product(
                                _generator_contribution(
                                    generator_id,
                                    _fraction_product(
                                        split_p[tagged_id], rho
                                    ),
                                    _fraction_product(
                                        split_q[tagged_id], rho
                                    ),
                                ),
                                jacobian,
                            )
                            for tagged_id in split_p
                        ]
                    )
                    source_stochastic_total = stochastic_reference_map[
                        generator_id
                    ]["stochastic_divergence_total"]
                    source_fine_total = sufficient_reference_map[
                        generator_id
                    ]["source_f_divergence_total"]
                    full_rank_transport_records.append(
                        {
                            "source_cross_numerator": source_cross,
                            "target_cross_numerator": target_cross,
                            "generator_id": generator_id,
                            "source_stochastic_divergence": source_stochastic_total,
                            "target_stochastic_divergence": target_stochastic_total,
                            "source_sufficient_split_divergence": source_fine_total,
                            "target_sufficient_split_divergence": target_split_total,
                            "stochastic_transport_invariant": (
                                target_stochastic_total
                                == source_stochastic_total
                            ),
                            "sufficient_split_transport_invariant": (
                                target_split_total == source_fine_total
                            ),
                            "transport_stochastic_channel_commutes": (
                                target_stochastic_total
                                == source_stochastic_total
                            ),
                            "transport_sufficiency_channel_commutes": (
                                target_split_total == source_fine_total
                            ),
                        }
                    )
                elif singular:
                    stochastic_ledger = {
                        target_id: _generator_contribution(
                            generator_id,
                            stochastic_p[target_id],
                            stochastic_q[target_id],
                        )
                        for target_id in COARSE_BIN_IDS
                    }
                    singular_stochastic_records.append(
                        {
                            "source_cross_numerator": source_cross,
                            "target_cross_numerator": target_cross,
                            "generator_id": generator_id,
                            "singular_stochastic_output_ledger": stochastic_ledger,
                            "singular_stochastic_f_divergence_total": _fraction_sum(
                                list(stochastic_ledger.values())
                            ),
                            "singular_atomic_stochastic_processing_retained": True,
                            "two_dimensional_target_density_emitted": False,
                        }
                    )

    reference_strict = all(
        item["stochastic_strictly_less_than_fine"]
        and item[
            "stochastic_strictly_less_than_deterministic_coarse"
        ]
        for item in stochastic_reference_records
    )
    split_mass_recovery_exact = (
        recovered_p == p_masses and recovered_q == q_masses
    )

    return {
        "input_digest": canonical_digest(
            {
                "schema_version": SCHEMA_VERSION,
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
                "source_memoryos_v055_certificate_digest": v055[
                    "certificate_digest"
                ],
                "candidate_ids": v056["candidate_ids"],
                "history_ids": v056["history_ids"],
                "probe_ids": probe_ids,
                "stochastic_kernel_weights": STOCHASTIC_KERNEL_WEIGHTS,
                "split_weights": SPLIT_WEIGHTS,
            }
        ),
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
        "source_memoryos_v055_certificate_digest": v055[
            "certificate_digest"
        ],
        "source_memoryos_v055_relative_entropy_transport_digest": v055[
            "relative_entropy_transport_digest"
        ],
        "source_memoryos_v055_relative_entropy_cocycle_digest": v055[
            "relative_entropy_cocycle_digest"
        ],
        "retained_history_ids": v056["history_ids"],
        "retained_decision_candidate_ids": v056["candidate_ids"],
        "retained_probe_ids": probe_ids,
        "f_divergence_generator_ids": list(GENERATOR_IDS),
        "stochastic_markov_kernel_rows": stochastic_rows,
        "stochastic_markov_kernel_digest": canonical_digest(
            stochastic_rows
        ),
        "stochastic_output_p_masses": stochastic_p,
        "stochastic_output_q_masses": stochastic_q,
        "stochastic_reference_data_processing_records": stochastic_reference_records,
        "stochastic_reference_data_processing_digest": canonical_digest(
            stochastic_reference_records
        ),
        "tagged_split_channel_entries": split_channel_entries,
        "tagged_split_channel_digest": canonical_digest(
            split_channel_entries
        ),
        "tagged_split_p_masses": split_p,
        "tagged_split_q_masses": split_q,
        "recovery_kernel_entries": recovery_kernel_entries,
        "recovery_kernel_digest": canonical_digest(
            recovery_kernel_entries
        ),
        "recovered_p_masses": recovered_p,
        "recovered_q_masses": recovered_q,
        "sufficient_probe_generator_records": sufficient_probe_records,
        "sufficient_probe_generator_digest": canonical_digest(
            sufficient_probe_records
        ),
        "sufficient_generator_equality_records": sufficient_generator_records,
        "sufficient_generator_equality_digest": canonical_digest(
            sufficient_generator_records
        ),
        "full_rank_transport_markov_sufficiency_records": full_rank_transport_records,
        "full_rank_transport_markov_sufficiency_digest": canonical_digest(
            full_rank_transport_records
        ),
        "singular_stochastic_f_divergence_records": singular_stochastic_records,
        "singular_stochastic_f_divergence_digest": canonical_digest(
            singular_stochastic_records
        ),
        "stochastic_kernel_row_count": len(stochastic_rows),
        "stochastic_kernel_entry_count": len(stochastic_rows)
        * len(COARSE_BIN_IDS),
        "stochastic_output_count": len(COARSE_BIN_IDS),
        "stochastic_data_processing_record_count": len(
            stochastic_reference_records
        ),
        "tagged_split_channel_entry_count": len(
            split_channel_entries
        ),
        "tagged_split_output_count": len(split_p),
        "recovery_kernel_entry_count": len(recovery_kernel_entries),
        "sufficient_probe_generator_record_count": len(
            sufficient_probe_records
        ),
        "sufficient_generator_equality_record_count": len(
            sufficient_generator_records
        ),
        "full_rank_transport_markov_sufficiency_record_count": len(
            full_rank_transport_records
        ),
        "singular_stochastic_f_divergence_record_count": len(
            singular_stochastic_records
        ),
        "rank_one_source_boundary_count": sum(
            transition["rank_one_source_boundary"]
            for transition in v056["transitions"].values()
        ),
        "source_memoryos_v056_exact": True,
        "source_memoryos_v055_exact": True,
        "source_f_divergence_transport_digest_bound": True,
        "source_data_processing_digest_bound": True,
        "source_f_divergence_cocycle_digest_bound": True,
        "stochastic_markov_kernel_row_stochastic": all(
            row["row_stochastic"] for row in stochastic_rows
        ),
        "stochastic_markov_kernel_preserves_total_mass": (
            _fraction_sum(list(stochastic_p.values()))
            == {"numerator": 1, "denominator": 1}
            and _fraction_sum(list(stochastic_q.values()))
            == {"numerator": 1, "denominator": 1}
        ),
        "all_stochastic_reference_data_processing_contractions_exact": all(
            item["stochastic_not_greater_than_deterministic_coarse"]
            and item["deterministic_coarse_not_greater_than_fine"]
            for item in stochastic_reference_records
        ),
        "all_stochastic_reference_contractions_strict": reference_strict,
        "reference_stochastic_kernel_sufficient": False,
        "reference_stochastic_kernel_not_sufficient": reference_strict,
        "tagged_split_channel_row_stochastic": all(
            _fraction_sum(list(SPLIT_WEIGHTS.values()))
            == {"numerator": 1, "denominator": 1}
            for _ in probe_ids
        ),
        "tagged_split_channel_preserves_total_mass": (
            _fraction_sum(list(split_p.values()))
            == {"numerator": 1, "denominator": 1}
            and _fraction_sum(list(split_q.values()))
            == {"numerator": 1, "denominator": 1}
        ),
        "explicit_recovery_kernel_exact": split_mass_recovery_exact,
        "all_tagged_split_recovery_masses_exact": split_mass_recovery_exact,
        "all_sufficient_probe_equalities_exact": all(
            item["split_equality_exact"]
            and item["recovery_equality_exact"]
            for item in sufficient_probe_records
        ),
        "all_sufficient_f_divergence_equalities_exact": all(
            item["explicit_sufficiency_equality_exact"]
            for item in sufficient_generator_records
        ),
        "all_full_rank_transport_stochastic_channel_commutes": all(
            item["stochastic_transport_invariant"]
            and item["transport_stochastic_channel_commutes"]
            for item in full_rank_transport_records
        ),
        "all_full_rank_transport_sufficiency_channel_commutes": all(
            item["sufficient_split_transport_invariant"]
            and item["transport_sufficiency_channel_commutes"]
            for item in full_rank_transport_records
        ),
        "singular_atomic_stochastic_processing_retained": all(
            item["singular_atomic_stochastic_processing_retained"]
            and not item["two_dimensional_target_density_emitted"]
            for item in singular_stochastic_records
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
        "source_relational_frontier_candidate_ids": v056[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": v056[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": v056[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": v056[
            "source_minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "markov_kernel_witness_advisory_only": True,
        "data_processing_not_candidate_pruning": True,
        "sufficiency_not_candidate_preference": True,
        "equality_witness_not_truth_authority": True,
        "singular_boundary_not_information_recovery": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v056_mutated": False,
        "source_memoryos_v055_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }


def issue_stochastic_markov_kernel_f_divergence_sufficiency_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        observables = _derive_observables(
            payload.get("source_memoryos_v056_certificate"),
            payload.get("source_memoryos_v055_certificate"),
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))

    required_true = (
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
    )
    required_false = (
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
    "SOURCE_MEMORYOS_V056_SCHEMA_VERSION",
    "SOURCE_MEMORYOS_V055_SCHEMA_VERSION",
    "GENERATOR_IDS",
    "COARSE_BIN_IDS",
    "SPLIT_TAGS",
    "SPLIT_WEIGHTS",
    "STOCHASTIC_KERNEL_WEIGHTS",
    "canonical_digest",
    "_derive_observables",
    "_normalize_source_memoryos_v056",
    "issue_stochastic_markov_kernel_f_divergence_sufficiency_certificate",
]
