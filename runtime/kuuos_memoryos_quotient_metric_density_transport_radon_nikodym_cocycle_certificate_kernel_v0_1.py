from __future__ import annotations

from hashlib import sha256
import json
from math import gcd
from typing import Any, Mapping

from runtime.kuuos_memoryos_quotient_transport_jacobian_volume_stratification_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_MEMORYOS_V053_SCHEMA_VERSION,
    SOURCE_MEMORYOS_V052_SCHEMA_VERSION,
    EXPECTED_CROSSES,
    _normalize_source_memoryos_v052,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.quotient-metric-density-transport-radon-nikodym-"
    "cocycle-certificate.v0.1"
)


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


def _mode_weights(cross: int) -> tuple[int, int]:
    return 2 + cross, 2 - cross


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


def _fraction_product(
    left: Mapping[str, int], right: Mapping[str, int]
) -> dict[str, int]:
    return _fraction(
        left["numerator"] * right["numerator"],
        left["denominator"] * right["denominator"],
    )


def _fraction_product_exact(
    left: Mapping[str, int],
    right: Mapping[str, int],
    expected: Mapping[str, int],
) -> bool:
    return _fraction_product(left, right) == dict(expected)


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


def _normalize_source_memoryos_v053(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v053_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v053_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V053_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v053_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v053_certificate_digest_missing")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v053_certificate_digest_mismatch")

    observables = source.get("observables")
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v053_observables_invalid")
    observables = dict(observables)
    _require_boolean_fields(
        observables,
        (
            "source_memoryos_v052_exact",
            "source_memoryos_v051_exact",
            "all_transport_mode_eigenvalues_exact",
            "all_transport_determinant_factorizations_exact",
            "all_full_rank_probe_mode_transports_exact",
            "all_normalized_mode_products_equal_jacobians",
            "all_raw_mode_composition_identities_exact",
            "all_active_normalized_mode_compositions_exact",
            "all_rank_one_boundary_symmetric_partial_transports_exact",
            "rank_one_boundary_has_no_two_dimensional_jacobian",
            "rank_one_boundary_antisymmetric_recovery_not_claimed",
            "reference_full_rank_mode_multipliers_exact",
            "reference_full_rank_jacobians_exact",
            "full_rank_round_trip_unit_jacobian_exact",
            "all_decision_candidates_retained",
            "all_planos_histories_retained",
            "relational_frontier_preserved",
            "required_review_set_preserved",
            "dissent_visibility_preserved",
            "minority_visibility_preserved",
            "jacobian_witness_advisory_only",
            "volume_distortion_not_candidate_preference",
            "rank_one_boundary_not_information_recovery",
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
            "source_memoryos_v052_mutated",
            "source_memoryos_v051_mutated",
            "source_decisionos_v06_mutated",
            "persistent_world_state_mutated",
            "verification_result_claimed",
            "truth_authority_granted",
        ),
        "source_memoryos_v053",
    )

    candidate_ids = observables.get("retained_decision_candidate_ids")
    if candidate_ids != [
        "continue",
        "hold",
        "reobserve",
        "terminate_candidate",
    ]:
        raise ValueError("source_memoryos_v053_candidate_order_mismatch")
    history_ids = observables.get("retained_history_ids")
    if (
        not isinstance(history_ids, list)
        or len(history_ids) != 2
        or len(set(history_ids)) != 2
    ):
        raise ValueError("source_memoryos_v053_history_support_invalid")

    expected_counts = {
        "transition_count": 9,
        "probe_mode_transport_record_count": 81,
        "composition_record_count": 27,
        "normalized_transport_count": 6,
        "invertible_full_rank_transition_count": 4,
        "full_rank_to_rank_one_volume_collapse_count": 2,
        "rank_one_source_boundary_count": 3,
        "normalized_composition_active_count": 12,
        "invertible_full_rank_path_count": 8,
    }
    for field, expected in expected_counts.items():
        if observables.get(field) != expected:
            raise ValueError(f"source_memoryos_v053_{field}_mismatch")

    transitions = observables.get("quotient_transport_jacobian_trajectory")
    jacobian_digest = observables.get("quotient_transport_jacobian_digest")
    if not isinstance(transitions, list) or len(transitions) != 9:
        raise ValueError("source_memoryos_v053_transition_trajectory_invalid")
    if canonical_digest(transitions) != jacobian_digest:
        raise ValueError("source_memoryos_v053_jacobian_digest_mismatch")

    expected_pairs = {
        (source_cross, target_cross)
        for source_cross in EXPECTED_CROSSES
        for target_cross in EXPECTED_CROSSES
    }
    transition_map: dict[tuple[int, int], dict[str, Any]] = {}
    probe_ids: list[str] | None = None
    for item in transitions:
        if not isinstance(item, Mapping):
            raise ValueError("source_memoryos_v053_transition_invalid")
        record = dict(item)
        pair = (
            record.get("source_cross_numerator"),
            record.get("target_cross_numerator"),
        )
        if pair not in expected_pairs or pair in transition_map:
            raise ValueError("source_memoryos_v053_transition_support_invalid")
        source_cross, target_cross = pair
        source_det, target_det = _determinant(source_cross), _determinant(target_cross)
        source_sym, source_anti = _mode_weights(source_cross)
        target_sym, target_anti = _mode_weights(target_cross)
        expected_values = {
            "source_metric_determinant": source_det,
            "target_metric_determinant": target_det,
            "normalized_transport_active": source_det != 0,
            "invertible_full_rank_transport": source_det != 0 and target_det != 0,
            "full_rank_to_rank_one_volume_collapse": source_det != 0 and target_det == 0,
            "rank_one_source_boundary": source_det == 0,
            "normalized_jacobian": _fraction(target_det, source_det) if source_det else None,
            "normalized_symmetric_mode_multiplier": _fraction(target_sym, source_sym) if source_det else None,
            "normalized_antisymmetric_mode_multiplier": _fraction(target_anti, source_anti) if source_det else None,
        }
        error_names = {
            "source_metric_determinant": "source_determinant",
            "target_metric_determinant": "target_determinant",
            "normalized_transport_active": "normalized_flag",
            "invertible_full_rank_transport": "invertible_flag",
            "full_rank_to_rank_one_volume_collapse": "collapse_flag",
            "rank_one_source_boundary": "boundary_flag",
            "normalized_jacobian": "normalized_jacobian",
            "normalized_symmetric_mode_multiplier": "symmetric_multiplier",
            "normalized_antisymmetric_mode_multiplier": "antisymmetric_multiplier",
        }
        for field, expected in expected_values.items():
            if record.get(field) != expected:
                raise ValueError(
                    f"source_memoryos_v053_{error_names[field]}_mismatch"
                )
        probe_records = record.get("probe_mode_transport_records")
        if not isinstance(probe_records, list) or len(probe_records) != 9:
            raise ValueError("source_memoryos_v053_probe_records_invalid")
        current_probe_ids = [probe.get("probe_id") for probe in probe_records]
        if (
            any(not isinstance(probe_id, str) for probe_id in current_probe_ids)
            or len(set(current_probe_ids)) != 9
        ):
            raise ValueError("source_memoryos_v053_probe_id_invalid")
        if probe_ids is None:
            probe_ids = list(current_probe_ids)
        elif current_probe_ids != probe_ids:
            raise ValueError("source_memoryos_v053_probe_order_mismatch")
        transition_map[pair] = record
    if set(transition_map) != expected_pairs:
        raise ValueError("source_memoryos_v053_transition_support_incomplete")

    compositions = observables.get("quotient_transport_mode_composition_records")
    mode_composition_digest = observables.get(
        "quotient_transport_mode_composition_digest"
    )
    if not isinstance(compositions, list) or len(compositions) != 27:
        raise ValueError("source_memoryos_v053_composition_records_invalid")
    if canonical_digest(compositions) != mode_composition_digest:
        raise ValueError("source_memoryos_v053_mode_composition_digest_mismatch")
    composition_map: dict[tuple[int, int, int], dict[str, Any]] = {}
    for item in compositions:
        if not isinstance(item, Mapping):
            raise ValueError("source_memoryos_v053_composition_invalid")
        record = dict(item)
        triple = (
            record.get("source_cross_numerator"),
            record.get("middle_cross_numerator"),
            record.get("target_cross_numerator"),
        )
        if (
            any(cross not in EXPECTED_CROSSES for cross in triple)
            or triple in composition_map
        ):
            raise ValueError("source_memoryos_v053_composition_support_invalid")
        source_cross, middle_cross, target_cross = triple
        normalized_active = (
            _determinant(source_cross) != 0 and _determinant(middle_cross) != 0
        )
        if record.get("raw_symmetric_mode_composition_exact") is not True:
            raise ValueError("source_memoryos_v053_raw_symmetric_composition_missing")
        if record.get("raw_antisymmetric_mode_composition_exact") is not True:
            raise ValueError("source_memoryos_v053_raw_antisymmetric_composition_missing")
        if record.get("normalized_composition_active") is not normalized_active:
            raise ValueError("source_memoryos_v053_normalized_composition_flag_mismatch")
        if record.get("normalized_mode_composition_exact") is not normalized_active:
            raise ValueError("source_memoryos_v053_normalized_composition_mismatch")
        if record.get("invertible_full_rank_path") is not (
            normalized_active and _determinant(target_cross) != 0
        ):
            raise ValueError("source_memoryos_v053_invertible_path_mismatch")
        composition_map[triple] = record
    if len(composition_map) != 27:
        raise ValueError("source_memoryos_v053_composition_support_incomplete")

    digest_fields = {
        "source_memoryos_v052_certificate_digest": "v052_certificate",
        "source_memoryos_v052_transport_digest": "v052_transport",
        "source_memoryos_v052_composition_digest": "v052_composition",
        "source_memoryos_v051_certificate_digest": "v051_certificate",
        "source_memoryos_v051_mode_diagonalization_digest": "v051_mode",
    }
    digests: dict[str, str] = {}
    for field, short_name in digest_fields.items():
        field_value = observables.get(field)
        if not isinstance(field_value, str) or not field_value:
            raise ValueError(f"source_memoryos_v053_{short_name}_digest_missing")
        digests[field] = field_value
    expected_input_digest = canonical_digest(
        {
            "schema_version": SOURCE_MEMORYOS_V053_SCHEMA_VERSION,
            "source_memoryos_v052_certificate_digest": digests[
                "source_memoryos_v052_certificate_digest"
            ],
            "source_memoryos_v052_transport_digest": digests[
                "source_memoryos_v052_transport_digest"
            ],
            "source_memoryos_v052_composition_digest": digests[
                "source_memoryos_v052_composition_digest"
            ],
            "source_memoryos_v051_certificate_digest": digests[
                "source_memoryos_v051_certificate_digest"
            ],
            "source_memoryos_v051_mode_digest": digests[
                "source_memoryos_v051_mode_diagonalization_digest"
            ],
            "candidate_ids": candidate_ids,
            "history_ids": history_ids,
        }
    )
    if observables.get("input_digest") != expected_input_digest:
        raise ValueError("source_memoryos_v053_input_digest_mismatch")

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
            raise ValueError(f"source_memoryos_v053_{field}_invalid")
        review_fields[field] = list(items)

    return {
        "certificate_digest": digest,
        "jacobian_digest": jacobian_digest,
        "mode_composition_digest": mode_composition_digest,
        "candidate_ids": list(candidate_ids),
        "history_ids": list(history_ids),
        "probe_ids": list(probe_ids or []),
        "transitions": transition_map,
        "compositions": composition_map,
        **digests,
        **review_fields,
    }


def _derive_observables(
    source_memoryos_v053_certificate: Mapping[str, Any],
    source_memoryos_v052_certificate: Mapping[str, Any],
) -> dict[str, Any]:
    v053 = _normalize_source_memoryos_v053(source_memoryos_v053_certificate)
    v052 = _normalize_source_memoryos_v052(source_memoryos_v052_certificate)
    bindings = (
        v053["source_memoryos_v052_certificate_digest"] == v052["certificate_digest"],
        v053["source_memoryos_v052_transport_digest"] == v052["transition_digest"],
        v053["source_memoryos_v052_composition_digest"] == v052["composition_digest"],
        v053["candidate_ids"] == v052["candidate_ids"],
        v053["history_ids"] == v052["history_ids"],
    )
    binding_errors = (
        "source_v053_v052_certificate_binding_mismatch",
        "source_v053_v052_transport_binding_mismatch",
        "source_v053_v052_composition_binding_mismatch",
        "source_v053_v052_candidate_support_mismatch",
        "source_v053_v052_history_support_mismatch",
    )
    for exact, error in zip(bindings, binding_errors, strict=True):
        if not exact:
            raise ValueError(error)

    mass_denominator = sum(range(1, len(v053["probe_ids"]) + 1))
    transitions: list[dict[str, Any]] = []
    for source_cross in EXPECTED_CROSSES:
        source_det = _determinant(source_cross)
        source_sym, source_anti = _mode_weights(source_cross)
        for target_cross in EXPECTED_CROSSES:
            target_det = _determinant(target_cross)
            target_sym, target_anti = _mode_weights(target_cross)
            source_record = v053["transitions"][source_cross, target_cross]
            density_active = source_det != 0 and target_det != 0
            singular_collapse = source_det != 0 and target_det == 0
            rank_one_source = source_det == 0
            if density_active:
                sym_density = _fraction(source_sym, target_sym)
                anti_density = _fraction(source_anti, target_anti)
                density = _fraction(source_det, target_det)
                jacobian = source_record["normalized_jacobian"]
                mode_exact = _fraction_product_exact(sym_density, anti_density, density)
                reciprocal_exact = _fraction_product_exact(
                    density,
                    jacobian,
                    {"numerator": 1, "denominator": 1},
                )
            else:
                sym_density = anti_density = density = None
                jacobian = source_record["normalized_jacobian"]
                mode_exact = reciprocal_exact = False

            density_records: list[dict[str, Any]] = []
            singular_records: list[dict[str, Any]] = []
            for ordinal, source_probe in enumerate(
                source_record["probe_mode_transport_records"], start=1
            ):
                mass = _fraction(ordinal, mass_denominator)
                base = {
                    "probe_id": source_probe["probe_id"],
                    "quotient_coordinates": source_probe["quotient_coordinates"],
                    "source_mass_weight": mass,
                    "probe_retained": True,
                }
                if density_active:
                    target_density = _fraction_product(mass, density)
                    recovered = _fraction_product(target_density, jacobian)
                    density_records.append(
                        {
                            **base,
                            "source_coordinate_cell_volume": {
                                "numerator": 1,
                                "denominator": 1,
                            },
                            "target_coordinate_cell_volume": jacobian,
                            "source_density": mass,
                            "target_pushforward_density": target_density,
                            "pushforward_mass_weight": recovered,
                            "pullback_density": recovered,
                            "pushforward_mass_preserved": recovered == mass,
                            "pullback_density_recovers_source": recovered == mass,
                        }
                    )
                elif singular_collapse:
                    singular_records.append(
                        {
                            **base,
                            "singular_pushforward_mass_weight": mass,
                            "two_dimensional_target_density_emitted": False,
                            "support_retained_as_singular_measure": True,
                        }
                    )
            singular_exact = (
                not singular_collapse
                or (
                    jacobian == {"numerator": 0, "denominator": 1}
                    and density is None
                    and len(singular_records) == len(v053["probe_ids"])
                    and all(
                        record["support_retained_as_singular_measure"]
                        and not record["two_dimensional_target_density_emitted"]
                        for record in singular_records
                    )
                )
            )
            transitions.append(
                {
                    "source_cross_numerator": source_cross,
                    "target_cross_numerator": target_cross,
                    "source_metric_determinant": source_det,
                    "target_metric_determinant": target_det,
                    "density_transport_active": density_active,
                    "full_rank_to_rank_one_singular_measure_boundary": singular_collapse,
                    "rank_one_source_boundary": rank_one_source,
                    "symmetric_mode_density_multiplier": sym_density,
                    "antisymmetric_mode_density_multiplier": anti_density,
                    "radon_nikodym_density_multiplier": density,
                    "source_normalized_jacobian": jacobian,
                    "mode_density_product_equals_radon_nikodym": mode_exact,
                    "density_jacobian_reciprocal_exact": reciprocal_exact,
                    "probe_density_transport_records": density_records,
                    "singular_probe_pushforward_records": singular_records,
                    "finite_support_pushforward_pullback_exact": all(
                        record["pushforward_mass_preserved"]
                        and record["pullback_density_recovers_source"]
                        for record in density_records
                    ),
                    "singular_measure_boundary_exact": singular_exact,
                    "rank_one_source_two_dimensional_density_recovery_claimed": False,
                    "source_memoryos_v053_jacobian_bound": (
                        source_record["source_metric_determinant"] == source_det
                        and source_record["target_metric_determinant"] == target_det
                        and source_record["normalized_jacobian"] == jacobian
                    ),
                }
            )

    compositions: list[dict[str, Any]] = []
    for source_cross in EXPECTED_CROSSES:
        source_det = _determinant(source_cross)
        for middle_cross in EXPECTED_CROSSES:
            middle_det = _determinant(middle_cross)
            for target_cross in EXPECTED_CROSSES:
                target_det = _determinant(target_cross)
                active = source_det != 0 and middle_det != 0 and target_det != 0
                source_record = v053["compositions"][
                    source_cross, middle_cross, target_cross
                ]
                if active:
                    source_middle = _fraction(source_det, middle_det)
                    middle_target = _fraction(middle_det, target_det)
                    source_target = _fraction(source_det, target_det)
                    cocycle_exact = _fraction_product_exact(
                        source_middle, middle_target, source_target
                    )
                else:
                    source_middle = middle_target = source_target = None
                    cocycle_exact = False
                compositions.append(
                    {
                        "source_cross_numerator": source_cross,
                        "middle_cross_numerator": middle_cross,
                        "target_cross_numerator": target_cross,
                        "density_cocycle_active": active,
                        "source_to_middle_density_multiplier": source_middle,
                        "middle_to_target_density_multiplier": middle_target,
                        "source_to_target_density_multiplier": source_target,
                        "radon_nikodym_cocycle_exact": cocycle_exact,
                        "nontrivial_round_trip_density_preserved": (
                            active
                            and source_cross == target_cross
                            and source_cross != middle_cross
                            and source_target == {"numerator": 1, "denominator": 1}
                            and cocycle_exact
                        ),
                        "source_memoryos_v053_mode_composition_bound": (
                            source_record["raw_symmetric_mode_composition_exact"]
                            is True
                            and source_record[
                                "raw_antisymmetric_mode_composition_exact"
                            ]
                            is True
                            and (not active or source_record["invertible_full_rank_path"] is True)
                        ),
                    }
                )

    one_to_zero = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 1
        and item["target_cross_numerator"] == 0
    )
    zero_to_one = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 0
        and item["target_cross_numerator"] == 1
    )
    active_transitions = [item for item in transitions if item["density_transport_active"]]
    singular_transitions = [
        item
        for item in transitions
        if item["full_rank_to_rank_one_singular_measure_boundary"]
    ]
    active_cocycles = [item for item in compositions if item["density_cocycle_active"]]

    return {
        "input_digest": canonical_digest(
            {
                "schema_version": SCHEMA_VERSION,
                "source_memoryos_v053_certificate_digest": v053["certificate_digest"],
                "source_memoryos_v053_jacobian_digest": v053["jacobian_digest"],
                "source_memoryos_v053_mode_composition_digest": v053[
                    "mode_composition_digest"
                ],
                "source_memoryos_v052_certificate_digest": v052["certificate_digest"],
                "source_memoryos_v052_transport_digest": v052["transition_digest"],
                "candidate_ids": v053["candidate_ids"],
                "history_ids": v053["history_ids"],
                "probe_ids": v053["probe_ids"],
            }
        ),
        "source_memoryos_v053_certificate_digest": v053["certificate_digest"],
        "source_memoryos_v053_jacobian_digest": v053["jacobian_digest"],
        "source_memoryos_v053_mode_composition_digest": v053[
            "mode_composition_digest"
        ],
        "source_memoryos_v052_certificate_digest": v052["certificate_digest"],
        "source_memoryos_v052_transport_digest": v052["transition_digest"],
        "retained_history_ids": v053["history_ids"],
        "retained_decision_candidate_ids": v053["candidate_ids"],
        "retained_probe_ids": v053["probe_ids"],
        "quotient_metric_density_transport_trajectory": transitions,
        "quotient_metric_density_transport_digest": canonical_digest(transitions),
        "radon_nikodym_cocycle_records": compositions,
        "radon_nikodym_cocycle_digest": canonical_digest(compositions),
        "transition_count": len(transitions),
        "density_active_transition_count": len(active_transitions),
        "probe_density_transport_record_count": sum(
            len(item["probe_density_transport_records"]) for item in transitions
        ),
        "singular_measure_collapse_transition_count": len(singular_transitions),
        "singular_probe_pushforward_record_count": sum(
            len(item["singular_probe_pushforward_records"]) for item in transitions
        ),
        "rank_one_source_boundary_count": sum(
            item["rank_one_source_boundary"] for item in transitions
        ),
        "density_cocycle_record_count": len(compositions),
        "active_density_cocycle_count": len(active_cocycles),
        "nontrivial_round_trip_density_path_count": sum(
            item["nontrivial_round_trip_density_preserved"] for item in compositions
        ),
        "reference_one_to_zero_symmetric_density_multiplier": one_to_zero[
            "symmetric_mode_density_multiplier"
        ],
        "reference_one_to_zero_antisymmetric_density_multiplier": one_to_zero[
            "antisymmetric_mode_density_multiplier"
        ],
        "reference_one_to_zero_radon_nikodym_multiplier": one_to_zero[
            "radon_nikodym_density_multiplier"
        ],
        "reference_zero_to_one_symmetric_density_multiplier": zero_to_one[
            "symmetric_mode_density_multiplier"
        ],
        "reference_zero_to_one_antisymmetric_density_multiplier": zero_to_one[
            "antisymmetric_mode_density_multiplier"
        ],
        "reference_zero_to_one_radon_nikodym_multiplier": zero_to_one[
            "radon_nikodym_density_multiplier"
        ],
        "source_memoryos_v053_exact": True,
        "source_memoryos_v052_exact": True,
        "source_jacobian_digest_bound": True,
        "source_mode_composition_digest_bound": True,
        "source_memoryos_v052_transport_digest_bound": True,
        "all_full_rank_density_multipliers_exact": all(
            item["density_jacobian_reciprocal_exact"]
            and item["source_memoryos_v053_jacobian_bound"]
            for item in active_transitions
        ),
        "all_mode_density_products_exact": all(
            item["mode_density_product_equals_radon_nikodym"]
            for item in active_transitions
        ),
        "all_finite_support_pushforward_pullback_witnesses_exact": all(
            item["finite_support_pushforward_pullback_exact"]
            and len(item["probe_density_transport_records"]) == len(v053["probe_ids"])
            for item in active_transitions
        ),
        "all_active_radon_nikodym_cocycles_exact": all(
            item["radon_nikodym_cocycle_exact"]
            and item["source_memoryos_v053_mode_composition_bound"]
            for item in active_cocycles
        ),
        "full_rank_round_trip_density_preserved": (
            _fraction_product_exact(
                one_to_zero["radon_nikodym_density_multiplier"],
                zero_to_one["radon_nikodym_density_multiplier"],
                {"numerator": 1, "denominator": 1},
            )
            and sum(
                item["nontrivial_round_trip_density_preserved"]
                for item in compositions
            )
            == 2
        ),
        "full_rank_to_rank_one_is_singular_measure_boundary": all(
            item["singular_measure_boundary_exact"] for item in singular_transitions
        ),
        "rank_one_source_two_dimensional_density_not_recovered": all(
            item["radon_nikodym_density_multiplier"] is None
            and not item[
                "rank_one_source_two_dimensional_density_recovery_claimed"
            ]
            for item in transitions
            if item["rank_one_source_boundary"]
        ),
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "all_quotient_coordinate_probes_retained": True,
        "source_relational_frontier_candidate_ids": v053[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": v053[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": v053[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": v053[
            "source_minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "density_witness_advisory_only": True,
        "density_transport_not_candidate_preference": True,
        "singular_boundary_not_information_recovery": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v053_mutated": False,
        "source_memoryos_v052_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }


def issue_quotient_metric_density_transport_radon_nikodym_cocycle_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        observables = _derive_observables(
            payload.get("source_memoryos_v053_certificate"),
            payload.get("source_memoryos_v052_certificate"),
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))

    required_true = (
        "source_memoryos_v053_exact",
        "source_memoryos_v052_exact",
        "source_jacobian_digest_bound",
        "source_mode_composition_digest_bound",
        "source_memoryos_v052_transport_digest_bound",
        "all_full_rank_density_multipliers_exact",
        "all_mode_density_products_exact",
        "all_finite_support_pushforward_pullback_witnesses_exact",
        "all_active_radon_nikodym_cocycles_exact",
        "full_rank_round_trip_density_preserved",
        "full_rank_to_rank_one_is_singular_measure_boundary",
        "rank_one_source_two_dimensional_density_not_recovered",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "density_witness_advisory_only",
        "density_transport_not_candidate_preference",
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
        "source_memoryos_v053_mutated",
        "source_memoryos_v052_mutated",
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
    "SOURCE_MEMORYOS_V053_SCHEMA_VERSION",
    "SOURCE_MEMORYOS_V052_SCHEMA_VERSION",
    "EXPECTED_CROSSES",
    "canonical_digest",
    "_derive_observables",
    "_normalize_source_memoryos_v053",
    "issue_quotient_metric_density_transport_radon_nikodym_cocycle_certificate",
]
