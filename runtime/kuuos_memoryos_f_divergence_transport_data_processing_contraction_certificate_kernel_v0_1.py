from __future__ import annotations

from hashlib import sha256
import json
from math import gcd
from typing import Any, Mapping

from runtime.kuuos_memoryos_relative_entropy_transport_lebesgue_decomposition_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_MEMORYOS_V055_SCHEMA_VERSION,
    SOURCE_MEMORYOS_V054_SCHEMA_VERSION,
    EXPECTED_CROSSES,
    _normalize_source_memoryos_v054,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.f-divergence-transport-data-processing-"
    "contraction-certificate.v0.1"
)

GENERATOR_IDS = (
    "pearson_chi_square",
    "neyman_chi_square",
    "triangular_discrimination",
)

COARSE_BIN_IDS = ("early", "middle", "late")


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


def _determinant(cross: int) -> int:
    return 4 - cross * cross


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


def _fraction_nonnegative(value: Mapping[str, int]) -> bool:
    return value["numerator"] >= 0


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


def _normalize_source_memoryos_v055(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v055_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v055_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V055_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v055_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v055_certificate_digest_missing")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v055_certificate_digest_mismatch")

    observables = source.get("observables")
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v055_observables_invalid")
    observables = dict(observables)
    _require_boolean_fields(
        observables,
        (
            "source_memoryos_v054_exact",
            "source_memoryos_v053_exact",
            "source_density_transport_digest_bound",
            "source_density_cocycle_digest_bound",
            "source_jacobian_digest_bound",
            "reference_probability_masses_exact",
            "all_reference_likelihood_ratios_exact",
            "all_full_rank_relative_entropy_terms_invariant",
            "all_reverse_relative_entropy_terms_invariant",
            "all_relative_entropy_cocycles_exact",
            "full_rank_round_trip_relative_entropy_preserved",
            "all_singular_lebesgue_decompositions_exact",
            "singular_atomic_relative_entropy_retained",
            "rank_one_source_two_dimensional_kl_not_recovered",
            "all_decision_candidates_retained",
            "all_planos_histories_retained",
            "all_quotient_coordinate_probes_retained",
            "relational_frontier_preserved",
            "required_review_set_preserved",
            "dissent_visibility_preserved",
            "minority_visibility_preserved",
            "relative_entropy_witness_advisory_only",
            "relative_entropy_not_candidate_preference",
            "singular_decomposition_not_information_recovery",
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
            "source_memoryos_v054_mutated",
            "source_memoryos_v053_mutated",
            "source_decisionos_v06_mutated",
            "persistent_world_state_mutated",
            "verification_result_claimed",
            "truth_authority_granted",
        ),
        "source_memoryos_v055",
    )

    expected_counts = {
        "transition_count": 9,
        "full_rank_relative_entropy_transition_count": 4,
        "full_rank_probe_relative_entropy_record_count": 36,
        "singular_lebesgue_decomposition_transition_count": 2,
        "singular_probe_lebesgue_decomposition_record_count": 18,
        "singular_atomic_relative_entropy_record_count": 18,
        "rank_one_source_boundary_count": 3,
        "relative_entropy_cocycle_record_count": 27,
        "active_relative_entropy_cocycle_count": 8,
        "nontrivial_round_trip_relative_entropy_path_count": 2,
    }
    for field, expected in expected_counts.items():
        if observables.get(field) != expected:
            raise ValueError(f"source_memoryos_v055_{field}_mismatch")

    candidate_ids = observables.get("retained_decision_candidate_ids")
    if candidate_ids != [
        "continue",
        "hold",
        "reobserve",
        "terminate_candidate",
    ]:
        raise ValueError("source_memoryos_v055_candidate_order_mismatch")
    history_ids = observables.get("retained_history_ids")
    if (
        not isinstance(history_ids, list)
        or len(history_ids) != 2
        or len(set(history_ids)) != 2
    ):
        raise ValueError("source_memoryos_v055_history_support_invalid")
    probe_ids = observables.get("retained_probe_ids")
    if (
        not isinstance(probe_ids, list)
        or len(probe_ids) != 9
        or len(set(probe_ids)) != 9
        or any(not isinstance(probe_id, str) for probe_id in probe_ids)
    ):
        raise ValueError("source_memoryos_v055_probe_support_invalid")

    expected_p_masses = {
        probe_id: _fraction(ordinal, 45)
        for ordinal, probe_id in enumerate(probe_ids, start=1)
    }
    expected_q_masses = {
        probe_id: _fraction(10 - ordinal, 45)
        for ordinal, probe_id in enumerate(probe_ids, start=1)
    }
    if observables.get("reference_p_probe_masses") != expected_p_masses:
        raise ValueError("source_memoryos_v055_reference_p_mass_mismatch")
    if observables.get("reference_q_probe_masses") != expected_q_masses:
        raise ValueError("source_memoryos_v055_reference_q_mass_mismatch")

    transitions = observables.get("relative_entropy_transport_trajectory")
    transition_digest = observables.get("relative_entropy_transport_digest")
    if not isinstance(transitions, list) or len(transitions) != 9:
        raise ValueError("source_memoryos_v055_transition_trajectory_invalid")
    if canonical_digest(transitions) != transition_digest:
        raise ValueError("source_memoryos_v055_transition_digest_mismatch")

    expected_pairs = {
        (source_cross, target_cross)
        for source_cross in EXPECTED_CROSSES
        for target_cross in EXPECTED_CROSSES
    }
    transition_map: dict[tuple[int, int], dict[str, Any]] = {}
    for item in transitions:
        if not isinstance(item, Mapping):
            raise ValueError("source_memoryos_v055_transition_invalid")
        record = dict(item)
        pair = (
            record.get("source_cross_numerator"),
            record.get("target_cross_numerator"),
        )
        if pair not in expected_pairs or pair in transition_map:
            raise ValueError("source_memoryos_v055_transition_support_invalid")
        source_cross, target_cross = pair
        active = _determinant(source_cross) != 0 and _determinant(target_cross) != 0
        singular = _determinant(source_cross) != 0 and _determinant(target_cross) == 0
        rank_one_source = _determinant(source_cross) == 0
        if record.get("full_rank_relative_entropy_transport_active") is not active:
            raise ValueError("source_memoryos_v055_active_flag_mismatch")
        if record.get("singular_lebesgue_decomposition_active") is not singular:
            raise ValueError("source_memoryos_v055_singular_flag_mismatch")
        if record.get("rank_one_source_boundary") is not rank_one_source:
            raise ValueError("source_memoryos_v055_rank_one_flag_mismatch")
        full_rank_records = record.get("full_rank_probe_relative_entropy_records")
        singular_records = record.get("singular_probe_lebesgue_decomposition_records")
        if active:
            if (
                not isinstance(full_rank_records, list)
                or len(full_rank_records) != 9
                or singular_records != []
                or record.get("full_rank_relative_entropy_ledger_invariant") is not True
            ):
                raise ValueError("source_memoryos_v055_full_rank_records_invalid")
            if [r.get("probe_id") for r in full_rank_records] != probe_ids:
                raise ValueError("source_memoryos_v055_full_rank_probe_order_mismatch")
            for probe_id, probe_record in zip(probe_ids, full_rank_records, strict=True):
                if (
                    probe_record.get("p_source_mass") != expected_p_masses[probe_id]
                    or probe_record.get("q_source_mass") != expected_q_masses[probe_id]
                    or probe_record.get("relative_entropy_term_invariant") is not True
                    or probe_record.get("reverse_relative_entropy_term_invariant") is not True
                    or probe_record.get("p_mass_preserved") is not True
                    or probe_record.get("q_mass_preserved") is not True
                    or probe_record.get("probe_retained") is not True
                ):
                    raise ValueError("source_memoryos_v055_full_rank_probe_record_mismatch")
        elif singular:
            if (
                full_rank_records != []
                or not isinstance(singular_records, list)
                or len(singular_records) != 9
                or record.get("singular_lebesgue_decomposition_exact") is not True
            ):
                raise ValueError("source_memoryos_v055_singular_records_invalid")
            if [r.get("probe_id") for r in singular_records] != probe_ids:
                raise ValueError("source_memoryos_v055_singular_probe_order_mismatch")
            if not all(
                r.get("singular_atomic_relative_entropy_retained") is True
                and r.get("two_dimensional_relative_entropy_density_emitted") is False
                and r.get("probe_retained") is True
                for r in singular_records
            ):
                raise ValueError("source_memoryos_v055_singular_probe_record_mismatch")
        else:
            if full_rank_records != [] or singular_records != []:
                raise ValueError("source_memoryos_v055_rank_one_records_invalid")
            if record.get("rank_one_source_two_dimensional_kl_recovery_claimed") is not False:
                raise ValueError("source_memoryos_v055_rank_one_recovery_claim")
        transition_map[pair] = record
    if set(transition_map) != expected_pairs:
        raise ValueError("source_memoryos_v055_transition_support_incomplete")

    cocycles = observables.get("relative_entropy_cocycle_records")
    cocycle_digest = observables.get("relative_entropy_cocycle_digest")
    if not isinstance(cocycles, list) or len(cocycles) != 27:
        raise ValueError("source_memoryos_v055_cocycle_records_invalid")
    if canonical_digest(cocycles) != cocycle_digest:
        raise ValueError("source_memoryos_v055_cocycle_digest_mismatch")
    cocycle_map: dict[tuple[int, int, int], dict[str, Any]] = {}
    for item in cocycles:
        if not isinstance(item, Mapping):
            raise ValueError("source_memoryos_v055_cocycle_invalid")
        record = dict(item)
        triple = (
            record.get("source_cross_numerator"),
            record.get("middle_cross_numerator"),
            record.get("target_cross_numerator"),
        )
        if (
            any(cross not in EXPECTED_CROSSES for cross in triple)
            or triple in cocycle_map
        ):
            raise ValueError("source_memoryos_v055_cocycle_support_invalid")
        active = all(_determinant(cross) != 0 for cross in triple)
        if record.get("relative_entropy_cocycle_active") is not active:
            raise ValueError("source_memoryos_v055_cocycle_active_mismatch")
        if record.get("relative_entropy_cocycle_exact") is not active:
            raise ValueError("source_memoryos_v055_cocycle_exact_mismatch")
        if record.get("reverse_relative_entropy_cocycle_exact") is not active:
            raise ValueError("source_memoryos_v055_reverse_cocycle_exact_mismatch")
        cocycle_map[triple] = record
    if len(cocycle_map) != 27:
        raise ValueError("source_memoryos_v055_cocycle_support_incomplete")

    digest_fields = {
        "source_memoryos_v054_certificate_digest": "v054_certificate",
        "source_memoryos_v054_density_transport_digest": "v054_density_transport",
        "source_memoryos_v054_density_cocycle_digest": "v054_density_cocycle",
        "source_memoryos_v053_certificate_digest": "v053_certificate",
        "source_memoryos_v053_jacobian_digest": "v053_jacobian",
    }
    digests: dict[str, str] = {}
    for field, short_name in digest_fields.items():
        field_value = observables.get(field)
        if not isinstance(field_value, str) or not field_value:
            raise ValueError(f"source_memoryos_v055_{short_name}_digest_missing")
        digests[field] = field_value

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
            raise ValueError(f"source_memoryos_v055_{field}_invalid")
        review_fields[field] = list(items)

    return {
        "certificate_digest": digest,
        "relative_entropy_transport_digest": transition_digest,
        "relative_entropy_cocycle_digest": cocycle_digest,
        "candidate_ids": list(candidate_ids),
        "history_ids": list(history_ids),
        "probe_ids": list(probe_ids),
        "p_masses": expected_p_masses,
        "q_masses": expected_q_masses,
        "transitions": transition_map,
        "cocycles": cocycle_map,
        **digests,
        **review_fields,
    }


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
    raise ValueError("unknown_f_divergence_generator")


def _coarse_bins(probe_ids: list[str]) -> list[dict[str, Any]]:
    return [
        {"bin_id": COARSE_BIN_IDS[0], "probe_ids": probe_ids[0:3]},
        {"bin_id": COARSE_BIN_IDS[1], "probe_ids": probe_ids[3:6]},
        {"bin_id": COARSE_BIN_IDS[2], "probe_ids": probe_ids[6:9]},
    ]


def _coarse_masses(
    bins: list[Mapping[str, Any]],
    masses: Mapping[str, Mapping[str, int]],
) -> dict[str, dict[str, int]]:
    return {
        str(bin_record["bin_id"]): _fraction_sum(
            [masses[probe_id] for probe_id in bin_record["probe_ids"]]
        )
        for bin_record in bins
    }


def _pearson_pairwise_gap(
    p_left: Mapping[str, int],
    q_left: Mapping[str, int],
    p_right: Mapping[str, int],
    q_right: Mapping[str, int],
) -> dict[str, Any]:
    fine = _fraction_add(
        _generator_contribution("pearson_chi_square", p_left, q_left),
        _generator_contribution("pearson_chi_square", p_right, q_right),
    )
    merged_p = _fraction_add(p_left, p_right)
    merged_q = _fraction_add(q_left, q_right)
    coarse = _generator_contribution(
        "pearson_chi_square", merged_p, merged_q
    )
    gap = _fraction_sub(fine, coarse)
    left_deviation = _fraction_sub(p_left, q_left)
    right_deviation = _fraction_sub(p_right, q_right)
    cross_difference = _fraction_sub(
        _fraction_product(q_right, left_deviation),
        _fraction_product(q_left, right_deviation),
    )
    formula = _fraction_quotient(
        _fraction_square(cross_difference),
        _fraction_product(
            _fraction_product(q_left, q_right),
            _fraction_add(q_left, q_right),
        ),
    )
    return {
        "p_left": dict(p_left),
        "q_left": dict(q_left),
        "p_right": dict(p_right),
        "q_right": dict(q_right),
        "merged_p": merged_p,
        "merged_q": merged_q,
        "fine_pearson_contribution": fine,
        "coarse_pearson_contribution": coarse,
        "contraction_gap": gap,
        "completed_square_gap": formula,
        "gap_identity_exact": gap == formula,
        "gap_nonnegative": _fraction_nonnegative(gap),
    }


def _derive_observables(
    source_memoryos_v055_certificate: Mapping[str, Any],
    source_memoryos_v054_certificate: Mapping[str, Any],
) -> dict[str, Any]:
    v055 = _normalize_source_memoryos_v055(
        source_memoryos_v055_certificate
    )
    v054 = _normalize_source_memoryos_v054(
        source_memoryos_v054_certificate
    )
    bindings = (
        v055["source_memoryos_v054_certificate_digest"]
        == v054["certificate_digest"],
        v055["source_memoryos_v054_density_transport_digest"]
        == v054["density_transport_digest"],
        v055["source_memoryos_v054_density_cocycle_digest"]
        == v054["density_cocycle_digest"],
        v055["candidate_ids"] == v054["candidate_ids"],
        v055["history_ids"] == v054["history_ids"],
        v055["probe_ids"] == v054["probe_ids"],
    )
    binding_errors = (
        "source_v055_v054_certificate_binding_mismatch",
        "source_v055_v054_density_transport_binding_mismatch",
        "source_v055_v054_density_cocycle_binding_mismatch",
        "source_v055_v054_candidate_support_mismatch",
        "source_v055_v054_history_support_mismatch",
        "source_v055_v054_probe_support_mismatch",
    )
    for exact, error in zip(bindings, binding_errors, strict=True):
        if not exact:
            raise ValueError(error)

    bins = _coarse_bins(v055["probe_ids"])
    channel_rows = [
        {
            "probe_id": probe_id,
            "target_bin_id": next(
                bin_record["bin_id"]
                for bin_record in bins
                if probe_id in bin_record["probe_ids"]
            ),
            "transition_weight": {"numerator": 1, "denominator": 1},
        }
        for probe_id in v055["probe_ids"]
    ]
    p_coarse = _coarse_masses(bins, v055["p_masses"])
    q_coarse = _coarse_masses(bins, v055["q_masses"])

    generator_reference_records: list[dict[str, Any]] = []
    for generator_id in GENERATOR_IDS:
        fine_contributions = [
            _generator_contribution(
                generator_id,
                v055["p_masses"][probe_id],
                v055["q_masses"][probe_id],
            )
            for probe_id in v055["probe_ids"]
        ]
        coarse_contributions = [
            _generator_contribution(
                generator_id,
                p_coarse[bin_id],
                q_coarse[bin_id],
            )
            for bin_id in COARSE_BIN_IDS
        ]
        fine_total = _fraction_sum(fine_contributions)
        coarse_total = _fraction_sum(coarse_contributions)
        gap = _fraction_sub(fine_total, coarse_total)
        generator_reference_records.append(
            {
                "generator_id": generator_id,
                "fine_probe_contributions": fine_contributions,
                "coarse_bin_contributions": coarse_contributions,
                "fine_divergence_total": fine_total,
                "coarse_divergence_total": coarse_total,
                "data_processing_contraction_gap": gap,
                "coarse_not_greater_than_fine": _fraction_le(
                    coarse_total, fine_total
                ),
                "contraction_gap_nonnegative": _fraction_nonnegative(gap),
            }
        )

    pearson_merge_records: list[dict[str, Any]] = []
    for bin_record in bins:
        probe_a, probe_b, probe_c = bin_record["probe_ids"]
        first = _pearson_pairwise_gap(
            v055["p_masses"][probe_a],
            v055["q_masses"][probe_a],
            v055["p_masses"][probe_b],
            v055["q_masses"][probe_b],
        )
        first.update(
            {
                "bin_id": bin_record["bin_id"],
                "merge_stage": 1,
                "left_support": [probe_a],
                "right_support": [probe_b],
            }
        )
        second = _pearson_pairwise_gap(
            first["merged_p"],
            first["merged_q"],
            v055["p_masses"][probe_c],
            v055["q_masses"][probe_c],
        )
        second.update(
            {
                "bin_id": bin_record["bin_id"],
                "merge_stage": 2,
                "left_support": [probe_a, probe_b],
                "right_support": [probe_c],
            }
        )
        pearson_merge_records.extend([first, second])

    transitions: list[dict[str, Any]] = []
    full_rank_data_processing_records: list[dict[str, Any]] = []
    for source_cross in EXPECTED_CROSSES:
        for target_cross in EXPECTED_CROSSES:
            source_record = v055["transitions"][
                source_cross, target_cross
            ]
            active = source_record[
                "full_rank_relative_entropy_transport_active"
            ]
            singular = source_record[
                "singular_lebesgue_decomposition_active"
            ]
            rank_one_source = source_record["rank_one_source_boundary"]
            rho = source_record["source_radon_nikodym_density_multiplier"]
            jacobian = source_record["source_normalized_jacobian"]
            full_rank_records: list[dict[str, Any]] = []
            singular_records: list[dict[str, Any]] = []
            source_ledgers: dict[str, list[dict[str, int]]] = {}
            target_ledgers: dict[str, list[dict[str, int]]] = {}

            for generator_id in GENERATOR_IDS:
                source_ledger: list[dict[str, int]] = []
                target_ledger: list[dict[str, int]] = []
                for probe_id in v055["probe_ids"]:
                    p_mass = v055["p_masses"][probe_id]
                    q_mass = v055["q_masses"][probe_id]
                    source_contribution = _generator_contribution(
                        generator_id, p_mass, q_mass
                    )
                    source_ledger.append(source_contribution)
                    if active:
                        p_target_density = _fraction_product(p_mass, rho)
                        q_target_density = _fraction_product(q_mass, rho)
                        target_density_contribution = _generator_contribution(
                            generator_id,
                            p_target_density,
                            q_target_density,
                        )
                        target_mass_contribution = _fraction_product(
                            target_density_contribution, jacobian
                        )
                        target_ledger.append(target_mass_contribution)
                        full_rank_records.append(
                            {
                                "generator_id": generator_id,
                                "probe_id": probe_id,
                                "p_source_mass": p_mass,
                                "q_source_mass": q_mass,
                                "source_f_divergence_contribution": source_contribution,
                                "p_target_density": p_target_density,
                                "q_target_density": q_target_density,
                                "target_coordinate_cell_volume": jacobian,
                                "target_f_divergence_density_contribution": target_density_contribution,
                                "target_f_divergence_mass_contribution": target_mass_contribution,
                                "f_divergence_contribution_invariant": (
                                    target_mass_contribution
                                    == source_contribution
                                ),
                                "probe_retained": True,
                            }
                        )
                    elif singular:
                        target_ledger.append(source_contribution)
                        singular_records.append(
                            {
                                "generator_id": generator_id,
                                "probe_id": probe_id,
                                "p_singular_mass": p_mass,
                                "q_singular_mass": q_mass,
                                "source_f_divergence_contribution": source_contribution,
                                "singular_atomic_f_divergence_contribution": source_contribution,
                                "singular_atomic_f_divergence_retained": True,
                                "two_dimensional_f_divergence_density_emitted": False,
                                "probe_retained": True,
                            }
                        )
                source_ledgers[generator_id] = source_ledger
                target_ledgers[generator_id] = target_ledger

                if active:
                    p_target_by_probe = {
                        probe_id: _fraction_product(
                            v055["p_masses"][probe_id], rho
                        )
                        for probe_id in v055["probe_ids"]
                    }
                    q_target_by_probe = {
                        probe_id: _fraction_product(
                            v055["q_masses"][probe_id], rho
                        )
                        for probe_id in v055["probe_ids"]
                    }
                    p_target_coarse = _coarse_masses(
                        bins, p_target_by_probe
                    )
                    q_target_coarse = _coarse_masses(
                        bins, q_target_by_probe
                    )
                    source_fine = _fraction_sum(source_ledger)
                    source_coarse = _fraction_sum(
                        [
                            _generator_contribution(
                                generator_id,
                                p_coarse[bin_id],
                                q_coarse[bin_id],
                            )
                            for bin_id in COARSE_BIN_IDS
                        ]
                    )
                    target_fine = _fraction_sum(target_ledger)
                    target_coarse = _fraction_sum(
                        [
                            _fraction_product(
                                _generator_contribution(
                                    generator_id,
                                    p_target_coarse[bin_id],
                                    q_target_coarse[bin_id],
                                ),
                                jacobian,
                            )
                            for bin_id in COARSE_BIN_IDS
                        ]
                    )
                    source_gap = _fraction_sub(
                        source_fine, source_coarse
                    )
                    target_gap = _fraction_sub(
                        target_fine, target_coarse
                    )
                    full_rank_data_processing_records.append(
                        {
                            "source_cross_numerator": source_cross,
                            "target_cross_numerator": target_cross,
                            "generator_id": generator_id,
                            "source_fine_divergence": source_fine,
                            "source_coarse_divergence": source_coarse,
                            "source_contraction_gap": source_gap,
                            "target_fine_divergence": target_fine,
                            "target_coarse_divergence": target_coarse,
                            "target_contraction_gap": target_gap,
                            "source_data_processing_contraction_exact": (
                                _fraction_le(source_coarse, source_fine)
                                and _fraction_nonnegative(source_gap)
                            ),
                            "target_data_processing_contraction_exact": (
                                _fraction_le(target_coarse, target_fine)
                                and _fraction_nonnegative(target_gap)
                            ),
                            "transport_preserves_fine_divergence": (
                                target_fine == source_fine
                            ),
                            "transport_preserves_coarse_divergence": (
                                target_coarse == source_coarse
                            ),
                            "transport_preserves_contraction_gap": (
                                target_gap == source_gap
                            ),
                            "transport_coarse_graining_commutes": (
                                target_fine == source_fine
                                and target_coarse == source_coarse
                                and target_gap == source_gap
                            ),
                        }
                    )

            transitions.append(
                {
                    "source_cross_numerator": source_cross,
                    "target_cross_numerator": target_cross,
                    "full_rank_f_divergence_transport_active": active,
                    "singular_f_divergence_boundary_active": singular,
                    "rank_one_source_boundary": rank_one_source,
                    "source_radon_nikodym_density_multiplier": rho,
                    "source_normalized_jacobian": jacobian,
                    "source_f_divergence_ledgers": source_ledgers,
                    "target_f_divergence_ledgers": target_ledgers,
                    "full_rank_probe_f_divergence_records": full_rank_records,
                    "singular_atomic_f_divergence_records": singular_records,
                    "all_generator_ledgers_invariant": (
                        active
                        and all(
                            source_ledgers[generator_id]
                            == target_ledgers[generator_id]
                            for generator_id in GENERATOR_IDS
                        )
                        and all(
                            record[
                                "f_divergence_contribution_invariant"
                            ]
                            for record in full_rank_records
                        )
                    ),
                    "singular_atomic_f_divergence_exact": (
                        singular
                        and all(
                            record[
                                "singular_atomic_f_divergence_retained"
                            ]
                            and not record[
                                "two_dimensional_f_divergence_density_emitted"
                            ]
                            for record in singular_records
                        )
                    ),
                    "rank_one_source_two_dimensional_f_divergence_recovery_claimed": False,
                    "source_memoryos_v055_relative_entropy_bound": (
                        source_record[
                            "source_relative_entropy_symbolic_ledger"
                        ]
                        == source_record[
                            "target_relative_entropy_symbolic_ledger"
                        ]
                        if active or singular
                        else source_record[
                            "target_relative_entropy_symbolic_ledger"
                        ]
                        == []
                    ),
                }
            )

    transition_map = {
        (item["source_cross_numerator"], item["target_cross_numerator"]): item
        for item in transitions
    }
    compositions: list[dict[str, Any]] = []
    for source_cross in EXPECTED_CROSSES:
        for middle_cross in EXPECTED_CROSSES:
            for target_cross in EXPECTED_CROSSES:
                source_cocycle = v055["cocycles"][
                    source_cross, middle_cross, target_cross
                ]
                active = source_cocycle[
                    "relative_entropy_cocycle_active"
                ]
                source_middle = transition_map[
                    source_cross, middle_cross
                ]
                middle_target = transition_map[
                    middle_cross, target_cross
                ]
                source_target = transition_map[
                    source_cross, target_cross
                ]
                generator_exact = {
                    generator_id: (
                        active
                        and source_middle[
                            "all_generator_ledgers_invariant"
                        ]
                        and middle_target[
                            "all_generator_ledgers_invariant"
                        ]
                        and source_target[
                            "all_generator_ledgers_invariant"
                        ]
                        and source_middle["source_f_divergence_ledgers"][
                            generator_id
                        ]
                        == middle_target["source_f_divergence_ledgers"][
                            generator_id
                        ]
                        == source_target["source_f_divergence_ledgers"][
                            generator_id
                        ]
                    )
                    for generator_id in GENERATOR_IDS
                }
                compositions.append(
                    {
                        "source_cross_numerator": source_cross,
                        "middle_cross_numerator": middle_cross,
                        "target_cross_numerator": target_cross,
                        "f_divergence_cocycle_active": active,
                        "generator_cocycle_exact": generator_exact,
                        "all_generator_cocycles_exact": (
                            active and all(generator_exact.values())
                        ),
                        "nontrivial_round_trip_f_divergence_preserved": (
                            active
                            and source_cross == target_cross
                            and source_cross != middle_cross
                            and all(generator_exact.values())
                        ),
                        "source_memoryos_v055_entropy_cocycle_bound": (
                            source_cocycle[
                                "relative_entropy_cocycle_exact"
                            ]
                            is active
                        ),
                    }
                )

    active_transitions = [
        item
        for item in transitions
        if item["full_rank_f_divergence_transport_active"]
    ]
    singular_transitions = [
        item
        for item in transitions
        if item["singular_f_divergence_boundary_active"]
    ]
    active_cocycles = [
        item
        for item in compositions
        if item["f_divergence_cocycle_active"]
    ]
    pearson_reference = next(
        item
        for item in generator_reference_records
        if item["generator_id"] == "pearson_chi_square"
    )
    neyman_reference = next(
        item
        for item in generator_reference_records
        if item["generator_id"] == "neyman_chi_square"
    )
    triangular_reference = next(
        item
        for item in generator_reference_records
        if item["generator_id"] == "triangular_discrimination"
    )

    return {
        "input_digest": canonical_digest(
            {
                "schema_version": SCHEMA_VERSION,
                "source_memoryos_v055_certificate_digest": v055[
                    "certificate_digest"
                ],
                "source_memoryos_v055_relative_entropy_transport_digest": v055[
                    "relative_entropy_transport_digest"
                ],
                "source_memoryos_v055_relative_entropy_cocycle_digest": v055[
                    "relative_entropy_cocycle_digest"
                ],
                "source_memoryos_v054_certificate_digest": v054[
                    "certificate_digest"
                ],
                "source_memoryos_v054_density_transport_digest": v054[
                    "density_transport_digest"
                ],
                "candidate_ids": v055["candidate_ids"],
                "history_ids": v055["history_ids"],
                "probe_ids": v055["probe_ids"],
                "generator_ids": list(GENERATOR_IDS),
                "coarse_bins": bins,
            }
        ),
        "source_memoryos_v055_certificate_digest": v055[
            "certificate_digest"
        ],
        "source_memoryos_v055_relative_entropy_transport_digest": v055[
            "relative_entropy_transport_digest"
        ],
        "source_memoryos_v055_relative_entropy_cocycle_digest": v055[
            "relative_entropy_cocycle_digest"
        ],
        "source_memoryos_v054_certificate_digest": v054[
            "certificate_digest"
        ],
        "source_memoryos_v054_density_transport_digest": v054[
            "density_transport_digest"
        ],
        "source_memoryos_v054_density_cocycle_digest": v054[
            "density_cocycle_digest"
        ],
        "retained_history_ids": v055["history_ids"],
        "retained_decision_candidate_ids": v055["candidate_ids"],
        "retained_probe_ids": v055["probe_ids"],
        "f_divergence_generator_ids": list(GENERATOR_IDS),
        "f_divergence_generator_reference_records": generator_reference_records,
        "deterministic_coarse_graining_bins": bins,
        "deterministic_channel_rows": channel_rows,
        "coarse_grained_p_masses": p_coarse,
        "coarse_grained_q_masses": q_coarse,
        "pearson_pairwise_merge_records": pearson_merge_records,
        "f_divergence_transport_trajectory": transitions,
        "f_divergence_transport_digest": canonical_digest(transitions),
        "full_rank_data_processing_records": full_rank_data_processing_records,
        "data_processing_digest": canonical_digest(
            full_rank_data_processing_records
        ),
        "f_divergence_cocycle_records": compositions,
        "f_divergence_cocycle_digest": canonical_digest(compositions),
        "generator_count": len(GENERATOR_IDS),
        "transition_count": len(transitions),
        "full_rank_f_divergence_transition_count": len(active_transitions),
        "full_rank_probe_f_divergence_record_count": sum(
            len(item["full_rank_probe_f_divergence_records"])
            for item in transitions
        ),
        "singular_f_divergence_transition_count": len(singular_transitions),
        "singular_atomic_f_divergence_record_count": sum(
            len(item["singular_atomic_f_divergence_records"])
            for item in transitions
        ),
        "rank_one_source_boundary_count": sum(
            item["rank_one_source_boundary"] for item in transitions
        ),
        "coarse_graining_bin_count": len(bins),
        "deterministic_channel_row_count": len(channel_rows),
        "data_processing_record_count": len(
            full_rank_data_processing_records
        ),
        "pearson_pairwise_merge_witness_count": len(
            pearson_merge_records
        ),
        "f_divergence_cocycle_record_count": len(compositions),
        "active_f_divergence_cocycle_count": len(active_cocycles),
        "nontrivial_round_trip_f_divergence_path_count": sum(
            item[
                "nontrivial_round_trip_f_divergence_preserved"
            ]
            for item in compositions
        ),
        "reference_pearson_fine_divergence": pearson_reference[
            "fine_divergence_total"
        ],
        "reference_pearson_coarse_divergence": pearson_reference[
            "coarse_divergence_total"
        ],
        "reference_pearson_contraction_gap": pearson_reference[
            "data_processing_contraction_gap"
        ],
        "reference_neyman_fine_divergence": neyman_reference[
            "fine_divergence_total"
        ],
        "reference_neyman_coarse_divergence": neyman_reference[
            "coarse_divergence_total"
        ],
        "reference_neyman_contraction_gap": neyman_reference[
            "data_processing_contraction_gap"
        ],
        "reference_triangular_fine_divergence": triangular_reference[
            "fine_divergence_total"
        ],
        "reference_triangular_coarse_divergence": triangular_reference[
            "coarse_divergence_total"
        ],
        "reference_triangular_contraction_gap": triangular_reference[
            "data_processing_contraction_gap"
        ],
        "reference_pearson_pairwise_gap_total": _fraction_sum(
            [
                record["contraction_gap"]
                for record in pearson_merge_records
            ]
        ),
        "source_memoryos_v055_exact": True,
        "source_memoryos_v054_exact": True,
        "source_relative_entropy_transport_digest_bound": True,
        "source_relative_entropy_cocycle_digest_bound": True,
        "source_density_transport_digest_bound": True,
        "generator_catalog_exact": (
            list(GENERATOR_IDS)
            == [
                "pearson_chi_square",
                "neyman_chi_square",
                "triangular_discrimination",
            ]
        ),
        "deterministic_channel_mass_preserving": (
            len(channel_rows) == len(v055["probe_ids"])
            and all(
                row["transition_weight"]
                == {"numerator": 1, "denominator": 1}
                for row in channel_rows
            )
            and _fraction_sum(list(p_coarse.values()))
            == {"numerator": 1, "denominator": 1}
            and _fraction_sum(list(q_coarse.values()))
            == {"numerator": 1, "denominator": 1}
        ),
        "all_full_rank_f_divergence_terms_invariant": all(
            item["all_generator_ledgers_invariant"]
            and item["source_memoryos_v055_relative_entropy_bound"]
            for item in active_transitions
        ),
        "all_catalog_data_processing_contractions_exact": all(
            item["coarse_not_greater_than_fine"]
            and item["contraction_gap_nonnegative"]
            for item in generator_reference_records
        ),
        "all_full_rank_transport_coarse_graining_commutes": all(
            item["source_data_processing_contraction_exact"]
            and item["target_data_processing_contraction_exact"]
            and item["transport_coarse_graining_commutes"]
            for item in full_rank_data_processing_records
        ),
        "all_pearson_pairwise_merge_gaps_exact_nonnegative": all(
            item["gap_identity_exact"] and item["gap_nonnegative"]
            for item in pearson_merge_records
        ),
        "pearson_pairwise_gaps_sum_to_total_contraction": (
            _fraction_sum(
                [
                    record["contraction_gap"]
                    for record in pearson_merge_records
                ]
            )
            == pearson_reference["data_processing_contraction_gap"]
        ),
        "all_f_divergence_cocycles_exact": all(
            item["all_generator_cocycles_exact"]
            and item["source_memoryos_v055_entropy_cocycle_bound"]
            for item in active_cocycles
        ),
        "full_rank_round_trip_f_divergence_preserved": (
            sum(
                item[
                    "nontrivial_round_trip_f_divergence_preserved"
                ]
                for item in compositions
            )
            == 2
        ),
        "singular_atomic_f_divergence_retained": all(
            item["singular_atomic_f_divergence_exact"]
            for item in singular_transitions
        ),
        "rank_one_source_two_dimensional_f_divergence_not_recovered": all(
            not item[
                "rank_one_source_two_dimensional_f_divergence_recovery_claimed"
            ]
            and all(
                ledger == []
                for ledger in item["target_f_divergence_ledgers"].values()
            )
            for item in transitions
            if item["rank_one_source_boundary"]
        ),
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "all_quotient_coordinate_probes_retained": True,
        "source_relational_frontier_candidate_ids": v055[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": v055[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": v055[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": v055[
            "source_minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "f_divergence_witness_advisory_only": True,
        "data_processing_not_candidate_pruning": True,
        "contraction_not_candidate_preference": True,
        "singular_boundary_not_information_recovery": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v055_mutated": False,
        "source_memoryos_v054_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }


def issue_f_divergence_transport_data_processing_contraction_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        observables = _derive_observables(
            payload.get("source_memoryos_v055_certificate"),
            payload.get("source_memoryos_v054_certificate"),
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))

    required_true = (
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
        "source_memoryos_v055_mutated",
        "source_memoryos_v054_mutated",
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
    "SOURCE_MEMORYOS_V055_SCHEMA_VERSION",
    "SOURCE_MEMORYOS_V054_SCHEMA_VERSION",
    "EXPECTED_CROSSES",
    "GENERATOR_IDS",
    "COARSE_BIN_IDS",
    "canonical_digest",
    "_derive_observables",
    "_normalize_source_memoryos_v055",
    "issue_f_divergence_transport_data_processing_contraction_certificate",
]
