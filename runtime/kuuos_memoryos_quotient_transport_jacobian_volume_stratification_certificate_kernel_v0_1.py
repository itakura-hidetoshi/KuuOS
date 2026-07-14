from __future__ import annotations

from hashlib import sha256
import json
from math import gcd
from typing import Any, Mapping

from runtime.kuuos_memoryos_candidate_quotient_coordinate_canonicalization_certificate_kernel_v0_1 import (
    EXPECTED_PROBE_VECTORS,
)
from runtime.kuuos_memoryos_quotient_metric_covector_transport_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_MEMORYOS_V052_SCHEMA_VERSION,
    EXPECTED_CROSSES,
    _determinant,
    _matrix_list,
    _normalize_source_memoryos_v051,
    _transport,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.quotient-transport-jacobian-volume-stratification-"
    "certificate.v0.1"
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


def _mode_weights(cross: int) -> tuple[int, int]:
    return 2 + cross, 2 - cross


def _matvec(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    vector: tuple[int, int],
) -> tuple[int, int]:
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def _fraction(numerator: int, denominator: int) -> dict[str, int]:
    if denominator == 0:
        raise ValueError("fraction_denominator_zero")
    if denominator < 0:
        numerator = -numerator
        denominator = -denominator
    divisor = gcd(abs(numerator), denominator)
    return {
        "numerator": numerator // divisor,
        "denominator": denominator // divisor,
    }


def _fraction_product_exact(
    left: Mapping[str, int],
    right: Mapping[str, int],
    expected: Mapping[str, int],
) -> bool:
    return (
        left["numerator"]
        * right["numerator"]
        * expected["denominator"]
        == expected["numerator"]
        * left["denominator"]
        * right["denominator"]
    )


def _normalize_source_memoryos_v052(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v052_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v052_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V052_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v052_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v052_certificate_digest_missing")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v052_certificate_digest_mismatch")

    observables = source.get("observables")
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v052_observables_invalid")
    observables = dict(observables)

    required_true = (
        "source_memoryos_v051_exact",
        "source_memoryos_v050_exact",
        "all_scaled_metric_transport_identities_exact",
        "all_full_rank_probe_transports_exact",
        "all_transport_composition_identities_exact",
        "rank_one_boundary_uses_partial_symmetric_transport_only",
        "all_rank_one_boundary_symmetric_partial_transports_exact",
        "rank_one_boundary_antisymmetric_recovery_not_claimed",
        "reference_transport_matrices_exact",
        "full_rank_transport_denominators_exact",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "transport_witness_advisory_only",
        "rank_one_partial_transport_not_information_recovery",
        "transport_not_candidate_preference",
        "future_only",
        "read_only",
    )
    for field in required_true:
        if observables.get(field) is not True:
            raise ValueError("source_memoryos_v052_required_" + field)

    required_false = (
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v051_mutated",
        "source_memoryos_v050_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    )
    for field in required_false:
        if observables.get(field) is not False:
            raise ValueError("source_memoryos_v052_forbidden_" + field)

    candidate_ids = observables.get("retained_decision_candidate_ids")
    if candidate_ids != [
        "continue",
        "hold",
        "reobserve",
        "terminate_candidate",
    ]:
        raise ValueError("source_memoryos_v052_candidate_order_mismatch")
    history_ids = observables.get("retained_history_ids")
    if (
        not isinstance(history_ids, list)
        or len(history_ids) != 2
        or len(set(history_ids)) != 2
    ):
        raise ValueError("source_memoryos_v052_history_support_invalid")

    if observables.get("transition_count") != 9:
        raise ValueError("source_memoryos_v052_transition_count_mismatch")
    if observables.get("probe_transport_record_count") != 81:
        raise ValueError("source_memoryos_v052_probe_count_mismatch")
    if observables.get("composition_record_count") != 27:
        raise ValueError("source_memoryos_v052_composition_count_mismatch")
    if observables.get("full_rank_transition_count") != 6:
        raise ValueError("source_memoryos_v052_full_rank_count_mismatch")
    if observables.get("rank_one_boundary_partial_transition_count") != 3:
        raise ValueError("source_memoryos_v052_boundary_count_mismatch")

    transitions = observables.get("quotient_metric_covector_transport_trajectory")
    transition_digest = observables.get(
        "quotient_metric_covector_transport_digest"
    )
    if not isinstance(transitions, list) or len(transitions) != 9:
        raise ValueError("source_memoryos_v052_transition_trajectory_invalid")
    if canonical_digest(transitions) != transition_digest:
        raise ValueError("source_memoryos_v052_transition_digest_mismatch")

    probe_ids = [probe_id for probe_id, _ in EXPECTED_PROBE_VECTORS]
    expected_pairs = {
        (source_cross, target_cross)
        for source_cross in EXPECTED_CROSSES
        for target_cross in EXPECTED_CROSSES
    }
    normalized_transitions: dict[tuple[int, int], dict[str, Any]] = {}
    for item in transitions:
        if not isinstance(item, Mapping):
            raise ValueError("source_memoryos_v052_transition_invalid")
        record = dict(item)
        pair = (
            record.get("source_cross_numerator"),
            record.get("target_cross_numerator"),
        )
        if pair not in expected_pairs or pair in normalized_transitions:
            raise ValueError("source_memoryos_v052_transition_support_invalid")
        source_cross, target_cross = pair
        source_det = _determinant(source_cross)
        if record.get("source_metric_determinant_numerator") != source_det:
            raise ValueError("source_memoryos_v052_source_determinant_mismatch")
        if record.get("transport_numerator_matrix") != _matrix_list(
            _transport(source_cross, target_cross)
        ):
            raise ValueError("source_memoryos_v052_transport_matrix_mismatch")
        if record.get("scaled_metric_transport_identity_exact") is not True:
            raise ValueError("source_memoryos_v052_transport_identity_missing")
        if record.get("full_rank_rational_transport_active") is not (
            source_det != 0
        ):
            raise ValueError("source_memoryos_v052_full_rank_flag_mismatch")
        if record.get("rank_one_boundary_partial_transport_only") is not (
            source_det == 0
        ):
            raise ValueError("source_memoryos_v052_boundary_flag_mismatch")
        probe_records = record.get("probe_transport_records")
        if not isinstance(probe_records, list) or len(probe_records) != len(
            probe_ids
        ):
            raise ValueError("source_memoryos_v052_probe_records_invalid")
        seen: set[str] = set()
        for probe_record in probe_records:
            if not isinstance(probe_record, Mapping):
                raise ValueError("source_memoryos_v052_probe_record_invalid")
            probe_id = probe_record.get("probe_id")
            if probe_id not in probe_ids or probe_id in seen:
                raise ValueError("source_memoryos_v052_probe_id_invalid")
            seen.add(probe_id)
            if (
                probe_record.get("scaled_transport_exact") is not True
                or probe_record.get("boundary_symmetric_partial_exact")
                is not True
                or probe_record.get(
                    "boundary_antisymmetric_recovery_claimed"
                )
                is not False
                or probe_record.get("probe_retained") is not True
            ):
                raise ValueError("source_memoryos_v052_probe_witness_mismatch")
        normalized_transitions[pair] = record
    if set(normalized_transitions) != expected_pairs:
        raise ValueError("source_memoryos_v052_transition_support_incomplete")

    compositions = observables.get(
        "quotient_metric_transport_composition_records"
    )
    composition_digest = observables.get(
        "quotient_metric_transport_composition_digest"
    )
    if not isinstance(compositions, list) or len(compositions) != 27:
        raise ValueError("source_memoryos_v052_compositions_invalid")
    if canonical_digest(compositions) != composition_digest:
        raise ValueError("source_memoryos_v052_composition_digest_mismatch")
    triples: set[tuple[int, int, int]] = set()
    for item in compositions:
        if not isinstance(item, Mapping):
            raise ValueError("source_memoryos_v052_composition_invalid")
        triple = (
            item.get("source_cross_numerator"),
            item.get("middle_cross_numerator"),
            item.get("target_cross_numerator"),
        )
        if (
            any(cross not in EXPECTED_CROSSES for cross in triple)
            or triple in triples
        ):
            raise ValueError("source_memoryos_v052_composition_support_invalid")
        if item.get("composition_identity_exact") is not True:
            raise ValueError("source_memoryos_v052_composition_identity_missing")
        triples.add(triple)
    if len(triples) != 27:
        raise ValueError("source_memoryos_v052_composition_support_incomplete")

    source_v051_digest = observables.get(
        "source_memoryos_v051_certificate_digest"
    )
    source_v051_mode_digest = observables.get(
        "source_memoryos_v051_mode_diagonalization_digest"
    )
    if not isinstance(source_v051_digest, str) or not source_v051_digest:
        raise ValueError("source_memoryos_v052_v051_digest_missing")
    if (
        not isinstance(source_v051_mode_digest, str)
        or not source_v051_mode_digest
    ):
        raise ValueError("source_memoryos_v052_v051_mode_digest_missing")

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
            raise ValueError("source_memoryos_v052_" + field + "_invalid")
        review_fields[field] = list(items)

    return {
        "certificate_digest": digest,
        "transition_digest": transition_digest,
        "composition_digest": composition_digest,
        "candidate_ids": list(candidate_ids),
        "history_ids": list(history_ids),
        "transitions": normalized_transitions,
        "source_memoryos_v051_certificate_digest": source_v051_digest,
        "source_memoryos_v051_mode_digest": source_v051_mode_digest,
        **review_fields,
    }


def _derive_observables(
    source_memoryos_v052_certificate: Mapping[str, Any],
    source_memoryos_v051_certificate: Mapping[str, Any],
) -> dict[str, Any]:
    v052 = _normalize_source_memoryos_v052(source_memoryos_v052_certificate)
    v051 = _normalize_source_memoryos_v051(source_memoryos_v051_certificate)

    if (
        v052["source_memoryos_v051_certificate_digest"]
        != v051["certificate_digest"]
    ):
        raise ValueError("source_v052_v051_certificate_binding_mismatch")
    if v052["source_memoryos_v051_mode_digest"] != v051["trajectory_digest"]:
        raise ValueError("source_v052_v051_mode_binding_mismatch")
    if v052["candidate_ids"] != v051["candidate_ids"]:
        raise ValueError("source_v052_v051_candidate_support_mismatch")
    if v052["history_ids"] != v051["history_ids"]:
        raise ValueError("source_v052_v051_history_support_mismatch")

    probe_ids = [probe_id for probe_id, _ in EXPECTED_PROBE_VECTORS]
    transitions: list[dict[str, Any]] = []
    all_mode_eigenvalues_exact = True
    all_transport_determinants_exact = True
    all_full_rank_probe_modes_exact = True
    all_boundary_symmetric_partial_exact = True
    all_boundary_recovery_claims_false = True

    for source_cross in EXPECTED_CROSSES:
        source_symmetric, source_antisymmetric = _mode_weights(source_cross)
        source_determinant = _determinant(source_cross)
        for target_cross in EXPECTED_CROSSES:
            target_symmetric, target_antisymmetric = _mode_weights(
                target_cross
            )
            target_determinant = _determinant(target_cross)
            source_transition = v052["transitions"][
                source_cross,
                target_cross,
            ]
            transport = _transport(source_cross, target_cross)

            symmetric_eigen_numerator = (
                target_symmetric * source_antisymmetric
            )
            antisymmetric_eigen_numerator = (
                target_antisymmetric * source_symmetric
            )
            symmetric_action = _matvec(transport, (1, 1))
            antisymmetric_action = _matvec(transport, (1, -1))
            symmetric_eigen_exact = symmetric_action == (
                symmetric_eigen_numerator,
                symmetric_eigen_numerator,
            )
            antisymmetric_eigen_exact = antisymmetric_action == (
                antisymmetric_eigen_numerator,
                -antisymmetric_eigen_numerator,
            )
            transport_determinant_numerator = (
                symmetric_eigen_numerator
                * antisymmetric_eigen_numerator
            )
            determinant_factorization_exact = (
                transport_determinant_numerator
                == source_determinant * target_determinant
            )
            all_mode_eigenvalues_exact = (
                all_mode_eigenvalues_exact
                and symmetric_eigen_exact
                and antisymmetric_eigen_exact
            )
            all_transport_determinants_exact = (
                all_transport_determinants_exact
                and determinant_factorization_exact
            )

            normalized_active = source_determinant != 0
            invertible_active = (
                source_determinant != 0 and target_determinant != 0
            )
            volume_collapse = (
                source_determinant != 0 and target_determinant == 0
            )
            rank_one_boundary = source_determinant == 0

            symmetric_multiplier = (
                _fraction(target_symmetric, source_symmetric)
                if normalized_active
                else None
            )
            antisymmetric_multiplier = (
                _fraction(target_antisymmetric, source_antisymmetric)
                if normalized_active
                else None
            )
            normalized_jacobian = (
                _fraction(target_determinant, source_determinant)
                if normalized_active
                else None
            )
            mode_product_exact = (
                _fraction_product_exact(
                    symmetric_multiplier,
                    antisymmetric_multiplier,
                    normalized_jacobian,
                )
                if normalized_active
                else False
            )

            probe_records: list[dict[str, Any]] = []
            for probe_id in probe_ids:
                coordinates = v051["probe_coordinates"][probe_id]
                symmetric_coordinate = coordinates[0] + coordinates[1]
                antisymmetric_coordinate = coordinates[0] - coordinates[1]
                source_symmetric_dual = (
                    source_symmetric * symmetric_coordinate
                )
                source_antisymmetric_dual = (
                    source_antisymmetric * antisymmetric_coordinate
                )
                target_symmetric_dual = (
                    target_symmetric * symmetric_coordinate
                )
                target_antisymmetric_dual = (
                    target_antisymmetric * antisymmetric_coordinate
                )

                if normalized_active:
                    symmetric_exact = (
                        source_symmetric_dual
                        * symmetric_multiplier["numerator"]
                        == target_symmetric_dual
                        * symmetric_multiplier["denominator"]
                    )
                    antisymmetric_exact = (
                        source_antisymmetric_dual
                        * antisymmetric_multiplier["numerator"]
                        == target_antisymmetric_dual
                        * antisymmetric_multiplier["denominator"]
                    )
                    partial_symmetric_multiplier = None
                    boundary_symmetric_exact = True
                else:
                    symmetric_exact = False
                    antisymmetric_exact = False
                    partial_symmetric_multiplier = _fraction(
                        target_symmetric,
                        source_symmetric,
                    )
                    boundary_symmetric_exact = (
                        source_symmetric_dual
                        * partial_symmetric_multiplier["numerator"]
                        == target_symmetric_dual
                        * partial_symmetric_multiplier["denominator"]
                    )

                source_v052_probe = next(
                    item
                    for item in source_transition["probe_transport_records"]
                    if item["probe_id"] == probe_id
                )
                source_bound = (
                    source_v052_probe.get("quotient_coordinates")
                    == list(coordinates)
                    and source_v052_probe.get("scaled_transport_exact")
                    is True
                    and source_v052_probe.get(
                        "boundary_antisymmetric_recovery_claimed"
                    )
                    is False
                )
                all_full_rank_probe_modes_exact = (
                    all_full_rank_probe_modes_exact
                    and (
                        not normalized_active
                        or (symmetric_exact and antisymmetric_exact)
                    )
                    and source_bound
                )
                all_boundary_symmetric_partial_exact = (
                    all_boundary_symmetric_partial_exact
                    and (
                        not rank_one_boundary
                        or boundary_symmetric_exact
                    )
                )
                all_boundary_recovery_claims_false = (
                    all_boundary_recovery_claims_false
                    and not False
                )
                probe_records.append(
                    {
                        "probe_id": probe_id,
                        "quotient_coordinates": list(coordinates),
                        "symmetric_mode_coordinate": symmetric_coordinate,
                        "antisymmetric_mode_coordinate": (
                            antisymmetric_coordinate
                        ),
                        "source_symmetric_dual": source_symmetric_dual,
                        "source_antisymmetric_dual": (
                            source_antisymmetric_dual
                        ),
                        "target_symmetric_dual": target_symmetric_dual,
                        "target_antisymmetric_dual": (
                            target_antisymmetric_dual
                        ),
                        "normalized_symmetric_transport_exact": (
                            symmetric_exact
                        ),
                        "normalized_antisymmetric_transport_exact": (
                            antisymmetric_exact
                        ),
                        "boundary_partial_symmetric_multiplier": (
                            partial_symmetric_multiplier
                        ),
                        "boundary_partial_symmetric_transport_exact": (
                            boundary_symmetric_exact
                        ),
                        "boundary_antisymmetric_information_lost": (
                            rank_one_boundary
                            and antisymmetric_coordinate != 0
                            and target_antisymmetric != 0
                        ),
                        "boundary_antisymmetric_recovery_claimed": False,
                        "source_memoryos_v052_probe_bound": source_bound,
                        "probe_retained": True,
                    }
                )

            transitions.append(
                {
                    "source_cross_numerator": source_cross,
                    "target_cross_numerator": target_cross,
                    "source_symmetric_weight": source_symmetric,
                    "source_antisymmetric_weight": source_antisymmetric,
                    "target_symmetric_weight": target_symmetric,
                    "target_antisymmetric_weight": target_antisymmetric,
                    "source_metric_determinant": source_determinant,
                    "target_metric_determinant": target_determinant,
                    "transport_numerator_matrix": _matrix_list(transport),
                    "symmetric_mode_transport_eigen_numerator": (
                        symmetric_eigen_numerator
                    ),
                    "antisymmetric_mode_transport_eigen_numerator": (
                        antisymmetric_eigen_numerator
                    ),
                    "symmetric_mode_eigenvector_exact": (
                        symmetric_eigen_exact
                    ),
                    "antisymmetric_mode_eigenvector_exact": (
                        antisymmetric_eigen_exact
                    ),
                    "transport_determinant_numerator": (
                        transport_determinant_numerator
                    ),
                    "expected_source_target_determinant_product": (
                        source_determinant * target_determinant
                    ),
                    "transport_determinant_factorization_exact": (
                        determinant_factorization_exact
                    ),
                    "normalized_transport_active": normalized_active,
                    "invertible_full_rank_transport": invertible_active,
                    "full_rank_to_rank_one_volume_collapse": volume_collapse,
                    "rank_one_source_boundary": rank_one_boundary,
                    "normalized_symmetric_mode_multiplier": (
                        symmetric_multiplier
                    ),
                    "normalized_antisymmetric_mode_multiplier": (
                        antisymmetric_multiplier
                    ),
                    "normalized_jacobian": normalized_jacobian,
                    "normalized_mode_product_equals_jacobian": (
                        mode_product_exact
                    ),
                    "orientation_preserving_full_rank": (
                        invertible_active
                        and normalized_jacobian["numerator"] > 0
                        and normalized_jacobian["denominator"] > 0
                    ),
                    "rank_one_source_has_no_two_dimensional_jacobian": (
                        rank_one_boundary
                        and normalized_jacobian is None
                        and transport_determinant_numerator == 0
                    ),
                    "probe_mode_transport_records": probe_records,
                    "all_step_full_rank_probe_modes_exact": all(
                        (
                            not normalized_active
                            or (
                                record[
                                    "normalized_symmetric_transport_exact"
                                ]
                                and record[
                                    "normalized_antisymmetric_transport_exact"
                                ]
                            )
                        )
                        and record["source_memoryos_v052_probe_bound"]
                        for record in probe_records
                    ),
                    "all_step_boundary_symmetric_partial_exact": all(
                        not rank_one_boundary
                        or record[
                            "boundary_partial_symmetric_transport_exact"
                        ]
                        for record in probe_records
                    ),
                    "all_step_boundary_recovery_claims_false": all(
                        not record[
                            "boundary_antisymmetric_recovery_claimed"
                        ]
                        for record in probe_records
                    ),
                }
            )

    compositions: list[dict[str, Any]] = []
    all_mode_compositions_exact = True
    all_normalized_compositions_exact = True
    for source_cross in EXPECTED_CROSSES:
        source_symmetric, source_antisymmetric = _mode_weights(source_cross)
        source_determinant = _determinant(source_cross)
        for middle_cross in EXPECTED_CROSSES:
            middle_symmetric, middle_antisymmetric = _mode_weights(
                middle_cross
            )
            middle_determinant = _determinant(middle_cross)
            for target_cross in EXPECTED_CROSSES:
                target_symmetric, target_antisymmetric = _mode_weights(
                    target_cross
                )
                target_determinant = _determinant(target_cross)

                source_middle_symmetric = (
                    middle_symmetric * source_antisymmetric
                )
                middle_target_symmetric = (
                    target_symmetric * middle_antisymmetric
                )
                source_target_symmetric = (
                    target_symmetric * source_antisymmetric
                )
                source_middle_antisymmetric = (
                    middle_antisymmetric * source_symmetric
                )
                middle_target_antisymmetric = (
                    target_antisymmetric * middle_symmetric
                )
                source_target_antisymmetric = (
                    target_antisymmetric * source_symmetric
                )
                symmetric_composition_exact = (
                    middle_target_symmetric
                    * source_middle_symmetric
                    == middle_determinant * source_target_symmetric
                )
                antisymmetric_composition_exact = (
                    middle_target_antisymmetric
                    * source_middle_antisymmetric
                    == middle_determinant
                    * source_target_antisymmetric
                )
                raw_exact = (
                    symmetric_composition_exact
                    and antisymmetric_composition_exact
                )
                all_mode_compositions_exact = (
                    all_mode_compositions_exact and raw_exact
                )

                normalized_active = (
                    source_determinant != 0 and middle_determinant != 0
                )
                if normalized_active:
                    sym_source_middle = _fraction(
                        middle_symmetric,
                        source_symmetric,
                    )
                    sym_middle_target = _fraction(
                        target_symmetric,
                        middle_symmetric,
                    )
                    sym_source_target = _fraction(
                        target_symmetric,
                        source_symmetric,
                    )
                    anti_source_middle = _fraction(
                        middle_antisymmetric,
                        source_antisymmetric,
                    )
                    anti_middle_target = _fraction(
                        target_antisymmetric,
                        middle_antisymmetric,
                    )
                    anti_source_target = _fraction(
                        target_antisymmetric,
                        source_antisymmetric,
                    )
                    symmetric_normalized_exact = _fraction_product_exact(
                        sym_source_middle,
                        sym_middle_target,
                        sym_source_target,
                    )
                    antisymmetric_normalized_exact = (
                        _fraction_product_exact(
                            anti_source_middle,
                            anti_middle_target,
                            anti_source_target,
                        )
                    )
                    normalized_exact = (
                        symmetric_normalized_exact
                        and antisymmetric_normalized_exact
                    )
                else:
                    normalized_exact = False
                all_normalized_compositions_exact = (
                    all_normalized_compositions_exact
                    and (not normalized_active or normalized_exact)
                )
                compositions.append(
                    {
                        "source_cross_numerator": source_cross,
                        "middle_cross_numerator": middle_cross,
                        "target_cross_numerator": target_cross,
                        "raw_symmetric_mode_composition_exact": (
                            symmetric_composition_exact
                        ),
                        "raw_antisymmetric_mode_composition_exact": (
                            antisymmetric_composition_exact
                        ),
                        "normalized_composition_active": normalized_active,
                        "normalized_mode_composition_exact": (
                            normalized_exact
                        ),
                        "invertible_full_rank_path": (
                            source_determinant != 0
                            and middle_determinant != 0
                            and target_determinant != 0
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

    return {
        "input_digest": canonical_digest(
            {
                "schema_version": SCHEMA_VERSION,
                "source_memoryos_v052_certificate_digest": v052[
                    "certificate_digest"
                ],
                "source_memoryos_v052_transport_digest": v052[
                    "transition_digest"
                ],
                "source_memoryos_v052_composition_digest": v052[
                    "composition_digest"
                ],
                "source_memoryos_v051_certificate_digest": v051[
                    "certificate_digest"
                ],
                "source_memoryos_v051_mode_digest": v051[
                    "trajectory_digest"
                ],
                "candidate_ids": v052["candidate_ids"],
                "history_ids": v052["history_ids"],
            }
        ),
        "source_memoryos_v052_certificate_digest": v052[
            "certificate_digest"
        ],
        "source_memoryos_v052_transport_digest": v052["transition_digest"],
        "source_memoryos_v052_composition_digest": v052[
            "composition_digest"
        ],
        "source_memoryos_v051_certificate_digest": v051[
            "certificate_digest"
        ],
        "source_memoryos_v051_mode_diagonalization_digest": v051[
            "trajectory_digest"
        ],
        "retained_history_ids": v052["history_ids"],
        "retained_decision_candidate_ids": v052["candidate_ids"],
        "quotient_transport_jacobian_trajectory": transitions,
        "quotient_transport_jacobian_digest": canonical_digest(transitions),
        "quotient_transport_mode_composition_records": compositions,
        "quotient_transport_mode_composition_digest": canonical_digest(
            compositions
        ),
        "transition_count": len(transitions),
        "probe_mode_transport_record_count": sum(
            len(item["probe_mode_transport_records"])
            for item in transitions
        ),
        "composition_record_count": len(compositions),
        "normalized_transport_count": sum(
            item["normalized_transport_active"] for item in transitions
        ),
        "invertible_full_rank_transition_count": sum(
            item["invertible_full_rank_transport"] for item in transitions
        ),
        "full_rank_to_rank_one_volume_collapse_count": sum(
            item["full_rank_to_rank_one_volume_collapse"]
            for item in transitions
        ),
        "rank_one_source_boundary_count": sum(
            item["rank_one_source_boundary"] for item in transitions
        ),
        "normalized_composition_active_count": sum(
            item["normalized_composition_active"] for item in compositions
        ),
        "invertible_full_rank_path_count": sum(
            item["invertible_full_rank_path"] for item in compositions
        ),
        "reference_one_to_zero_symmetric_multiplier": one_to_zero[
            "normalized_symmetric_mode_multiplier"
        ],
        "reference_one_to_zero_antisymmetric_multiplier": one_to_zero[
            "normalized_antisymmetric_mode_multiplier"
        ],
        "reference_one_to_zero_jacobian": one_to_zero[
            "normalized_jacobian"
        ],
        "reference_zero_to_one_symmetric_multiplier": zero_to_one[
            "normalized_symmetric_mode_multiplier"
        ],
        "reference_zero_to_one_antisymmetric_multiplier": zero_to_one[
            "normalized_antisymmetric_mode_multiplier"
        ],
        "reference_zero_to_one_jacobian": zero_to_one[
            "normalized_jacobian"
        ],
        "source_memoryos_v052_exact": True,
        "source_memoryos_v051_exact": True,
        "all_transport_mode_eigenvalues_exact": (
            all_mode_eigenvalues_exact
        ),
        "all_transport_determinant_factorizations_exact": (
            all_transport_determinants_exact
        ),
        "all_full_rank_probe_mode_transports_exact": (
            all_full_rank_probe_modes_exact
        ),
        "all_normalized_mode_products_equal_jacobians": all(
            (
                not item["normalized_transport_active"]
                or item["normalized_mode_product_equals_jacobian"]
            )
            for item in transitions
        ),
        "all_raw_mode_composition_identities_exact": (
            all_mode_compositions_exact
        ),
        "all_active_normalized_mode_compositions_exact": (
            all_normalized_compositions_exact
        ),
        "all_rank_one_boundary_symmetric_partial_transports_exact": (
            all_boundary_symmetric_partial_exact
        ),
        "rank_one_boundary_has_no_two_dimensional_jacobian": all(
            (
                not item["rank_one_source_boundary"]
                or item[
                    "rank_one_source_has_no_two_dimensional_jacobian"
                ]
            )
            for item in transitions
        ),
        "rank_one_boundary_antisymmetric_recovery_not_claimed": (
            all_boundary_recovery_claims_false
        ),
        "reference_full_rank_mode_multipliers_exact": (
            one_to_zero["normalized_symmetric_mode_multiplier"]
            == {"numerator": 2, "denominator": 3}
            and one_to_zero["normalized_antisymmetric_mode_multiplier"]
            == {"numerator": 2, "denominator": 1}
            and zero_to_one["normalized_symmetric_mode_multiplier"]
            == {"numerator": 3, "denominator": 2}
            and zero_to_one[
                "normalized_antisymmetric_mode_multiplier"
            ]
            == {"numerator": 1, "denominator": 2}
        ),
        "reference_full_rank_jacobians_exact": (
            one_to_zero["normalized_jacobian"]
            == {"numerator": 4, "denominator": 3}
            and zero_to_one["normalized_jacobian"]
            == {"numerator": 3, "denominator": 4}
        ),
        "full_rank_round_trip_unit_jacobian_exact": (
            _fraction_product_exact(
                one_to_zero["normalized_jacobian"],
                zero_to_one["normalized_jacobian"],
                {"numerator": 1, "denominator": 1},
            )
        ),
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "source_relational_frontier_candidate_ids": v052[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": v052[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": v052[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": v052[
            "source_minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "jacobian_witness_advisory_only": True,
        "volume_distortion_not_candidate_preference": True,
        "rank_one_boundary_not_information_recovery": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v052_mutated": False,
        "source_memoryos_v051_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }


def issue_quotient_transport_jacobian_volume_stratification_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        observables = _derive_observables(
            payload.get("source_memoryos_v052_certificate"),
            payload.get("source_memoryos_v051_certificate"),
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))

    for field in (
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
    ):
        if observables.get(field) is not True:
            blockers.append("observable_required_" + field)

    for field in (
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
    ):
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
    "SOURCE_MEMORYOS_V052_SCHEMA_VERSION",
    "EXPECTED_CROSSES",
    "canonical_digest",
    "_derive_observables",
    "_normalize_source_memoryos_v052",
    "issue_quotient_transport_jacobian_volume_stratification_certificate",
]
