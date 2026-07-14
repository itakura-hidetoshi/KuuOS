from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_candidate_quotient_coordinate_canonicalization_certificate_kernel_v0_1 import (
    EXPECTED_PROBE_VECTORS,
)
from runtime.kuuos_memoryos_candidate_quotient_mode_diagonalization_inverse_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_MEMORYOS_V051_SCHEMA_VERSION,
    _normalize_source_memoryos_v050,
)

SCHEMA_VERSION = "kuuos.memoryos.quotient-metric-covector-transport-certificate.v0.1"
EXPECTED_CROSSES = (2, 1, 0)
EXPECTED_RANKS = (1, 2, 2)


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


def _matrix(cross: int) -> tuple[tuple[int, int], tuple[int, int]]:
    return ((2, cross), (cross, 2))


def _adjugate(cross: int) -> tuple[tuple[int, int], tuple[int, int]]:
    return ((2, -cross), (-cross, 2))


def _determinant(cross: int) -> int:
    return 4 - cross * cross


def _matmul(
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


def _scale(
    scalar: int,
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    return (
        (scalar * matrix[0][0], scalar * matrix[0][1]),
        (scalar * matrix[1][0], scalar * matrix[1][1]),
    )


def _matvec(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    vector: tuple[int, int],
) -> tuple[int, int]:
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def _transport(
    source_cross: int,
    target_cross: int,
) -> tuple[tuple[int, int], tuple[int, int]]:
    return _matmul(_matrix(target_cross), _adjugate(source_cross))


def _matrix_list(
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> list[list[int]]:
    return [list(matrix[0]), list(matrix[1])]


def _normalize_source_memoryos_v051(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v051_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v051_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V051_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v051_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v051_certificate_digest_missing")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v051_certificate_digest_mismatch")

    obs = source.get("observables")
    if not isinstance(obs, Mapping):
        raise ValueError("source_memoryos_v051_observables_invalid")
    obs = dict(obs)

    for field in (
        "source_memoryos_v050_exact",
        "all_source_memoryos_v050_descent_records_bound",
        "all_probe_quadratic_evidence_mode_diagonalized",
        "all_ordered_probe_pairings_mode_diagonalized",
        "quotient_metric_determinant_factorization_exact",
        "integer_adjugate_identity_exact_across_trajectory",
        "full_coherence_rank_one_symmetric_mode_only",
        "post_dephasing_inverse_witness_exact",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "future_only",
        "read_only",
    ):
        if obs.get(field) is not True:
            raise ValueError("source_memoryos_v051_required_" + field)
    for field in (
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v050_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        if obs.get(field) is not False:
            raise ValueError("source_memoryos_v051_forbidden_" + field)

    candidate_ids = obs.get("retained_decision_candidate_ids")
    if candidate_ids != [
        "continue",
        "hold",
        "reobserve",
        "terminate_candidate",
    ]:
        raise ValueError("source_memoryos_v051_candidate_order_mismatch")
    history_ids = obs.get("retained_history_ids")
    if (
        not isinstance(history_ids, list)
        or len(history_ids) != 2
        or len(set(history_ids)) != 2
    ):
        raise ValueError("source_memoryos_v051_history_support_invalid")

    if obs.get("symmetric_mode_weight_trajectory") != [4, 3, 2]:
        raise ValueError("source_memoryos_v051_symmetric_weight_trajectory_mismatch")
    if obs.get("antisymmetric_mode_weight_trajectory") != [0, 1, 2]:
        raise ValueError("source_memoryos_v051_antisymmetric_weight_trajectory_mismatch")
    if obs.get("quotient_metric_determinant_trajectory") != [0, 3, 4]:
        raise ValueError("source_memoryos_v051_determinant_trajectory_mismatch")
    if obs.get("quotient_metric_rank_trajectory") != [1, 2, 2]:
        raise ValueError("source_memoryos_v051_rank_trajectory_mismatch")
    if obs.get("inverse_witness_active_trajectory") != [False, True, True]:
        raise ValueError("source_memoryos_v051_inverse_trajectory_mismatch")

    trajectory = obs.get("candidate_quotient_mode_diagonalization_trajectory")
    trajectory_digest = obs.get(
        "candidate_quotient_mode_diagonalization_digest"
    )
    if not isinstance(trajectory, list) or len(trajectory) != 3:
        raise ValueError("source_memoryos_v051_trajectory_invalid")
    if canonical_digest(trajectory) != trajectory_digest:
        raise ValueError("source_memoryos_v051_trajectory_digest_mismatch")

    expected_probe_ids = [probe_id for probe_id, _ in EXPECTED_PROBE_VECTORS]
    coordinates: dict[str, tuple[int, int]] = {}
    steps: list[dict[str, int]] = []
    for index, step in enumerate(trajectory):
        cross = EXPECTED_CROSSES[index]
        determinant = _determinant(cross)
        if step.get("step_index") != index:
            raise ValueError("source_memoryos_v051_step_index_invalid")
        if step.get("dephasing_numerator") != cross:
            raise ValueError("source_memoryos_v051_step_cross_mismatch")
        if step.get("symmetric_mode_weight_numerator") != 2 + cross:
            raise ValueError("source_memoryos_v051_step_symmetric_weight_mismatch")
        if step.get("antisymmetric_mode_weight_numerator") != 2 - cross:
            raise ValueError("source_memoryos_v051_step_antisymmetric_weight_mismatch")
        if step.get("quotient_metric_determinant_numerator") != determinant:
            raise ValueError("source_memoryos_v051_step_determinant_mismatch")
        if step.get("quotient_metric_rank") != EXPECTED_RANKS[index]:
            raise ValueError("source_memoryos_v051_step_rank_mismatch")
        if step.get("integer_adjugate_matrix") != _matrix_list(_adjugate(cross)):
            raise ValueError("source_memoryos_v051_step_adjugate_mismatch")
        scaled_identity = ((determinant, 0), (0, determinant))
        if (
            step.get("metric_times_adjugate") != _matrix_list(scaled_identity)
            or step.get("adjugate_times_metric") != _matrix_list(scaled_identity)
            or step.get("adjugate_inverse_witness_exact") is not True
        ):
            raise ValueError("source_memoryos_v051_step_adjugate_identity_mismatch")

        records = step.get("probe_mode_quadratic_records")
        if not isinstance(records, list) or len(records) != len(expected_probe_ids):
            raise ValueError("source_memoryos_v051_probe_records_invalid")
        step_coordinates: dict[str, tuple[int, int]] = {}
        for record in records:
            probe_id = record.get("probe_id")
            if probe_id not in expected_probe_ids or probe_id in step_coordinates:
                raise ValueError("source_memoryos_v051_probe_id_invalid")
            pair = (
                record.get("quotient_first_history_coordinate"),
                record.get("quotient_second_history_coordinate"),
            )
            if not all(isinstance(item, int) and not isinstance(item, bool) for item in pair):
                raise ValueError("source_memoryos_v051_probe_coordinates_invalid")
            if (
                record.get("symmetric_mode_coordinate") != pair[0] + pair[1]
                or record.get("antisymmetric_mode_coordinate") != pair[0] - pair[1]
                or record.get("mode_diagonalization_exact") is not True
                or record.get("source_memoryos_v050_quadratic_bound") is not True
            ):
                raise ValueError("source_memoryos_v051_probe_record_mismatch")
            step_coordinates[probe_id] = pair
        if index == 0:
            coordinates = step_coordinates
        elif coordinates != step_coordinates:
            raise ValueError("source_memoryos_v051_probe_coordinates_not_stable")
        steps.append(
            {
                "step_index": index,
                "cross": cross,
                "determinant": determinant,
                "rank": EXPECTED_RANKS[index],
            }
        )

    source_v050_digest = obs.get("source_memoryos_v050_certificate_digest")
    quotient_digest = obs.get(
        "source_memoryos_v050_quotient_coordinate_digest"
    )
    if not isinstance(source_v050_digest, str) or not source_v050_digest:
        raise ValueError("source_memoryos_v051_v050_digest_missing")
    if not isinstance(quotient_digest, str) or not quotient_digest:
        raise ValueError("source_memoryos_v051_v050_quotient_digest_missing")

    review_fields: dict[str, list[str]] = {}
    for field in (
        "source_relational_frontier_candidate_ids",
        "source_required_review_candidate_ids",
        "source_dissent_review_candidate_ids",
        "source_minority_protection_candidate_ids",
    ):
        items = obs.get(field)
        if (
            not isinstance(items, list)
            or len(items) != len(set(items))
            or any(item not in candidate_ids for item in items)
        ):
            raise ValueError("source_memoryos_v051_" + field + "_invalid")
        review_fields[field] = list(items)

    return {
        "certificate_digest": digest,
        "trajectory_digest": trajectory_digest,
        "candidate_ids": list(candidate_ids),
        "history_ids": list(history_ids),
        "probe_coordinates": coordinates,
        "steps": steps,
        "source_memoryos_v050_certificate_digest": source_v050_digest,
        "source_memoryos_v050_quotient_digest": quotient_digest,
        **review_fields,
    }


def _derive_observables(
    source_memoryos_v051_certificate: Mapping[str, Any],
    source_memoryos_v050_certificate: Mapping[str, Any],
) -> dict[str, Any]:
    v051 = _normalize_source_memoryos_v051(source_memoryos_v051_certificate)
    v050 = _normalize_source_memoryos_v050(source_memoryos_v050_certificate)
    if v051["source_memoryos_v050_certificate_digest"] != v050["certificate_digest"]:
        raise ValueError("source_v051_v050_certificate_binding_mismatch")
    if v051["source_memoryos_v050_quotient_digest"] != v050["quotient_digest"]:
        raise ValueError("source_v051_v050_quotient_binding_mismatch")
    if v051["candidate_ids"] != v050["candidate_ids"]:
        raise ValueError("source_v051_v050_candidate_support_mismatch")
    if v051["history_ids"] != v050["history_ids"]:
        raise ValueError("source_v051_v050_history_support_mismatch")
    for probe_id, coordinates in v051["probe_coordinates"].items():
        source_record = v050["records"][probe_id]
        if coordinates != (
            source_record["quotient_first_history_coordinate"],
            source_record["quotient_second_history_coordinate"],
        ):
            raise ValueError("source_v051_v050_probe_coordinate_binding_mismatch")

    probe_ids = [probe_id for probe_id, _ in EXPECTED_PROBE_VECTORS]
    transitions: list[dict[str, Any]] = []
    for source_cross in EXPECTED_CROSSES:
        source_det = _determinant(source_cross)
        for target_cross in EXPECTED_CROSSES:
            transport = _transport(source_cross, target_cross)
            left = _matmul(transport, _matrix(source_cross))
            right = _scale(source_det, _matrix(target_cross))
            records: list[dict[str, Any]] = []
            for probe_id in probe_ids:
                coordinates = v051["probe_coordinates"][probe_id]
                source_covector = _matvec(_matrix(source_cross), coordinates)
                target_covector = _matvec(_matrix(target_cross), coordinates)
                transported = _matvec(transport, source_covector)
                expected = (
                    source_det * target_covector[0],
                    source_det * target_covector[1],
                )
                symmetric = coordinates[0] + coordinates[1]
                antisymmetric = coordinates[0] - coordinates[1]
                source_symmetric_dual = (2 + source_cross) * symmetric
                target_symmetric_dual = (2 + target_cross) * symmetric
                boundary_exact = (
                    source_cross != 2
                    or (
                        source_symmetric_dual == 4 * symmetric
                        and (2 - source_cross) * antisymmetric == 0
                        and 4 * target_symmetric_dual
                        == (2 + target_cross) * source_symmetric_dual
                    )
                )
                records.append(
                    {
                        "probe_id": probe_id,
                        "quotient_coordinates": list(coordinates),
                        "source_metric_covector": list(source_covector),
                        "target_metric_covector": list(target_covector),
                        "transported_covector_numerator": list(transported),
                        "transport_denominator": source_det if source_det else None,
                        "expected_scaled_target_covector": list(expected),
                        "scaled_transport_exact": transported == expected,
                        "boundary_symmetric_partial_exact": boundary_exact,
                        "boundary_antisymmetric_recovery_claimed": False,
                        "probe_retained": True,
                    }
                )
            transitions.append(
                {
                    "source_cross_numerator": source_cross,
                    "target_cross_numerator": target_cross,
                    "source_metric_determinant_numerator": source_det,
                    "transport_numerator_matrix": _matrix_list(transport),
                    "transport_times_source_metric": _matrix_list(left),
                    "determinant_scaled_target_metric": _matrix_list(right),
                    "scaled_metric_transport_identity_exact": left == right,
                    "full_rank_rational_transport_active": source_det != 0,
                    "rank_one_boundary_partial_transport_only": source_det == 0,
                    "probe_transport_records": records,
                    "all_probe_scaled_transports_exact": all(
                        record["scaled_transport_exact"] for record in records
                    ),
                    "all_boundary_symmetric_partial_records_exact": all(
                        record["boundary_symmetric_partial_exact"]
                        for record in records
                    ),
                    "all_boundary_antisymmetric_recovery_claims_false": all(
                        not record["boundary_antisymmetric_recovery_claimed"]
                        for record in records
                    ),
                }
            )

    compositions: list[dict[str, Any]] = []
    for source_cross in EXPECTED_CROSSES:
        for middle_cross in EXPECTED_CROSSES:
            for target_cross in EXPECTED_CROSSES:
                composed = _matmul(
                    _transport(middle_cross, target_cross),
                    _transport(source_cross, middle_cross),
                )
                expected = _scale(
                    _determinant(middle_cross),
                    _transport(source_cross, target_cross),
                )
                compositions.append(
                    {
                        "source_cross_numerator": source_cross,
                        "middle_cross_numerator": middle_cross,
                        "target_cross_numerator": target_cross,
                        "composed_transport_numerator_matrix": _matrix_list(composed),
                        "middle_determinant_scaled_direct_transport_matrix": _matrix_list(expected),
                        "composition_identity_exact": composed == expected,
                    }
                )

    one_to_zero = next(
        item for item in transitions
        if item["source_cross_numerator"] == 1
        and item["target_cross_numerator"] == 0
    )
    zero_to_one = next(
        item for item in transitions
        if item["source_cross_numerator"] == 0
        and item["target_cross_numerator"] == 1
    )
    return {
        "input_digest": canonical_digest(
            {
                "schema_version": SCHEMA_VERSION,
                "source_memoryos_v051_certificate_digest": v051["certificate_digest"],
                "source_memoryos_v051_mode_digest": v051["trajectory_digest"],
                "source_memoryos_v050_certificate_digest": v050["certificate_digest"],
                "source_memoryos_v050_quotient_digest": v050["quotient_digest"],
                "candidate_ids": v051["candidate_ids"],
                "history_ids": v051["history_ids"],
            }
        ),
        "source_memoryos_v051_certificate_digest": v051["certificate_digest"],
        "source_memoryos_v051_mode_diagonalization_digest": v051["trajectory_digest"],
        "source_memoryos_v050_certificate_digest": v050["certificate_digest"],
        "source_memoryos_v050_quotient_coordinate_digest": v050["quotient_digest"],
        "retained_history_ids": v051["history_ids"],
        "retained_decision_candidate_ids": v051["candidate_ids"],
        "quotient_metric_covector_transport_trajectory": transitions,
        "quotient_metric_covector_transport_digest": canonical_digest(transitions),
        "quotient_metric_transport_composition_records": compositions,
        "quotient_metric_transport_composition_digest": canonical_digest(compositions),
        "transition_count": len(transitions),
        "probe_transport_record_count": sum(
            len(item["probe_transport_records"]) for item in transitions
        ),
        "composition_record_count": len(compositions),
        "full_rank_transition_count": sum(
            item["full_rank_rational_transport_active"] for item in transitions
        ),
        "rank_one_boundary_partial_transition_count": sum(
            item["rank_one_boundary_partial_transport_only"] for item in transitions
        ),
        "reference_one_to_zero_transport_matrix": one_to_zero["transport_numerator_matrix"],
        "reference_one_to_zero_transport_denominator": 3,
        "reference_zero_to_one_transport_matrix": zero_to_one["transport_numerator_matrix"],
        "reference_zero_to_one_transport_denominator": 4,
        "source_memoryos_v051_exact": True,
        "source_memoryos_v050_exact": True,
        "all_scaled_metric_transport_identities_exact": all(
            item["scaled_metric_transport_identity_exact"] for item in transitions
        ),
        "all_full_rank_probe_transports_exact": all(
            item["all_probe_scaled_transports_exact"]
            for item in transitions if item["full_rank_rational_transport_active"]
        ),
        "all_transport_composition_identities_exact": all(
            item["composition_identity_exact"] for item in compositions
        ),
        "rank_one_boundary_uses_partial_symmetric_transport_only": True,
        "all_rank_one_boundary_symmetric_partial_transports_exact": all(
            item["all_boundary_symmetric_partial_records_exact"]
            for item in transitions if item["rank_one_boundary_partial_transport_only"]
        ),
        "rank_one_boundary_antisymmetric_recovery_not_claimed": all(
            item["all_boundary_antisymmetric_recovery_claims_false"]
            for item in transitions if item["rank_one_boundary_partial_transport_only"]
        ),
        "reference_transport_matrices_exact": (
            one_to_zero["transport_numerator_matrix"] == [[4, -2], [-2, 4]]
            and zero_to_one["transport_numerator_matrix"] == [[4, 2], [2, 4]]
        ),
        "full_rank_transport_denominators_exact": True,
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "source_relational_frontier_candidate_ids": v051[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": v051[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": v051[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": v051[
            "source_minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "transport_witness_advisory_only": True,
        "rank_one_partial_transport_not_information_recovery": True,
        "transport_not_candidate_preference": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v051_mutated": False,
        "source_memoryos_v050_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }


def issue_quotient_metric_covector_transport_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")
    try:
        observables = _derive_observables(
            payload.get("source_memoryos_v051_certificate"),
            payload.get("source_memoryos_v050_certificate"),
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))

    for field in (
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
    ):
        if observables.get(field) is not True:
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
    "SOURCE_MEMORYOS_V051_SCHEMA_VERSION",
    "EXPECTED_CROSSES",
    "canonical_digest",
    "_derive_observables",
    "_normalize_source_memoryos_v051",
    "issue_quotient_metric_covector_transport_certificate",
]
