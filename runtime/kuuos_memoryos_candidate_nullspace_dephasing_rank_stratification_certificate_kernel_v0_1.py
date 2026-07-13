from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_two_history_candidate_gram_factorization_reconstruction_certificate_kernel_v0_1 import (
    _normalize_source_memoryos_v045,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.candidate-nullspace-dephasing-rank-stratification-"
    "certificate.v0.1"
)
SOURCE_MEMORYOS_V048_SCHEMA_VERSION = (
    "kuuos.memoryos.two-history-candidate-gram-factorization-"
    "reconstruction-certificate.v0.1"
)
EXPECTED_CANDIDATE_IDS = [
    "continue",
    "hold",
    "reobserve",
    "terminate_candidate",
]
MAXIMUM_CANDIDATE_COUNT = 128
MAXIMUM_HISTORY_COUNT = 128
MAXIMUM_DEPHASING_STEP_COUNT = 64
MAXIMUM_ABSOLUTE_INTEGER = 10_000_000

STRUCTURAL_NULL_RELATIONS: tuple[tuple[str, tuple[int, int, int, int]], ...] = (
    ("continue_minus_reobserve_minus_terminate", (1, 0, -1, -1)),
    ("hold_minus_reobserve_plus_terminate", (0, 1, -1, 1)),
)
ANTISYMMETRIC_HISTORY_PROBE = (0, 0, 1, -1)
SYMMETRIC_HISTORY_PROBE = (0, 0, 1, 1)


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


def _integer(value: Any, field: str, *, nonnegative: bool = False) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(field + "_invalid")
    if abs(value) > MAXIMUM_ABSOLUTE_INTEGER:
        raise ValueError(field + "_out_of_bounds")
    if nonnegative and value < 0:
        raise ValueError(field + "_negative")
    return value


def _string_ids(value: Any, field: str, maximum: int) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or len(value) > maximum
        or len(value) != len(set(value))
        or any(not isinstance(item, str) or not item for item in value)
    ):
        raise ValueError(field + "_invalid")
    return list(value)


def _review_ids(
    observables: Mapping[str, Any],
    field: str,
    candidate_ids: list[str],
) -> list[str]:
    value = observables.get(field)
    if (
        not isinstance(value, list)
        or len(value) != len(set(value))
        or any(item not in candidate_ids for item in value)
    ):
        raise ValueError("source_memoryos_v048_" + field + "_invalid")
    return list(value)


def _complex_add(
    left: tuple[int, int],
    right: tuple[int, int],
) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def _complex_mul(
    left: tuple[int, int],
    right: tuple[int, int],
) -> tuple[int, int]:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def _complex_scale(
    coefficient: int,
    value: tuple[int, int],
) -> tuple[int, int]:
    return coefficient * value[0], coefficient * value[1]


def _candidate_coefficients(
    values: tuple[int, int, int, int],
    candidate_ids: list[str],
) -> dict[str, int]:
    return dict(zip(candidate_ids, values, strict=True))


def _factor_lift(
    coefficients: Mapping[str, int],
    factor_map: Mapping[str, tuple[int, int]],
    candidate_ids: list[str],
) -> tuple[int, int]:
    return (
        sum(coefficients[candidate_id] * factor_map[candidate_id][0]
            for candidate_id in candidate_ids),
        sum(coefficients[candidate_id] * factor_map[candidate_id][1]
            for candidate_id in candidate_ids),
    )


def _kernel_action(
    entries: Mapping[tuple[str, str], tuple[int, int]],
    coefficients: Mapping[str, int],
    candidate_ids: list[str],
    *,
    side: str,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for fixed_id in candidate_ids:
        total = (0, 0)
        for varying_id in candidate_ids:
            if side == "right":
                entry = entries[fixed_id, varying_id]
            elif side == "left":
                entry = entries[varying_id, fixed_id]
            else:
                raise ValueError("kernel_action_side_invalid")
            total = _complex_add(
                total,
                _complex_scale(coefficients[varying_id], entry),
            )
        records.append(
            {
                "candidate_id": fixed_id,
                "real_numerator": total[0],
                "imag_numerator": total[1],
                "zero": total == (0, 0),
            }
        )
    return records


def _quadratic_energy(
    entries: Mapping[tuple[str, str], tuple[int, int]],
    coefficients: Mapping[str, int],
    candidate_ids: list[str],
) -> tuple[int, int]:
    total = (0, 0)
    for left_id in candidate_ids:
        for right_id in candidate_ids:
            total = _complex_add(
                total,
                _complex_scale(
                    coefficients[left_id] * coefficients[right_id],
                    entries[left_id, right_id],
                ),
            )
    return total


def _history_determinant(
    metric: Mapping[tuple[int, int], tuple[int, int]],
) -> tuple[int, int]:
    return _complex_add(
        _complex_mul(metric[0, 0], metric[1, 1]),
        _complex_scale(-1, _complex_mul(metric[0, 1], metric[1, 0])),
    )


def _normalize_source_memoryos_v048(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v048_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v048_not_accepted")
    if source.get("schema_version") != SOURCE_MEMORYOS_V048_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v048_schema_invalid")
    digest = source.get("certificate_digest")
    if not isinstance(digest, str) or not digest:
        raise ValueError("source_memoryos_v048_certificate_digest_missing")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v048_certificate_digest_mismatch")

    observables = source.get("observables")
    if not isinstance(observables, Mapping):
        raise ValueError("source_memoryos_v048_observables_invalid")
    observables = dict(observables)

    for field in (
        "source_memoryos_v047_exact",
        "source_memoryos_v045_exact",
        "fixed_candidate_history_factor_rows_exact",
        "all_candidate_kernel_entries_reconstructed",
        "all_candidate_row_relations_exact",
        "all_candidate_column_relations_exact",
        "all_candidate_four_by_four_determinants_zero",
        "all_v047_triple_records_bound_to_factorization",
        "candidate_gram_rank_at_most_two_by_explicit_factorization",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "factorization_witness_advisory_only",
        "history_coordinate_anchors_not_candidate_priority",
        "rank_factorization_not_candidate_consensus",
        "future_only",
        "read_only",
    ):
        if observables.get(field) is not True:
            raise ValueError("source_memoryos_v048_required_" + field)

    for field in (
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v047_mutated",
        "source_memoryos_v045_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        if observables.get(field) is not False:
            raise ValueError("source_memoryos_v048_forbidden_" + field)

    candidate_ids = _string_ids(
        observables.get("retained_decision_candidate_ids"),
        "source_memoryos_v048_candidate_ids",
        MAXIMUM_CANDIDATE_COUNT,
    )
    if candidate_ids != EXPECTED_CANDIDATE_IDS:
        raise ValueError("source_memoryos_v048_candidate_order_mismatch")

    history_ids = _string_ids(
        observables.get("retained_history_ids"),
        "source_memoryos_v048_history_ids",
        MAXIMUM_HISTORY_COUNT,
    )
    if len(history_ids) != 2:
        raise ValueError("source_memoryos_v048_history_count_not_two")

    raw_factor_matrix = observables.get("candidate_factor_matrix")
    if (
        not isinstance(raw_factor_matrix, list)
        or len(raw_factor_matrix) != len(candidate_ids)
    ):
        raise ValueError("source_memoryos_v048_factor_matrix_invalid")
    factor_map: dict[str, tuple[int, int]] = {}
    for raw in raw_factor_matrix:
        if not isinstance(raw, Mapping):
            raise ValueError("source_memoryos_v048_factor_row_invalid")
        item = dict(raw)
        candidate_id = item.get("candidate_id")
        if candidate_id not in candidate_ids or candidate_id in factor_map:
            raise ValueError("source_memoryos_v048_factor_candidate_invalid")
        factor_map[candidate_id] = (
            _integer(
                item.get("first_history_coefficient"),
                "source_memoryos_v048_first_history_coefficient",
            ),
            _integer(
                item.get("second_history_coefficient"),
                "source_memoryos_v048_second_history_coefficient",
            ),
        )
    expected_factor_map = {
        "continue": (1, 1),
        "hold": (1, -1),
        "reobserve": (1, 0),
        "terminate_candidate": (0, 1),
    }
    if factor_map != expected_factor_map:
        raise ValueError("source_memoryos_v048_factor_matrix_mismatch")

    raw_trajectory = observables.get(
        "two_history_candidate_gram_factorization_trajectory"
    )
    if (
        not isinstance(raw_trajectory, list)
        or not raw_trajectory
        or len(raw_trajectory) > MAXIMUM_DEPHASING_STEP_COUNT
    ):
        raise ValueError("source_memoryos_v048_trajectory_invalid")
    trajectory_digest = observables.get(
        "two_history_candidate_gram_factorization_digest"
    )
    if not isinstance(trajectory_digest, str) or not trajectory_digest:
        raise ValueError("source_memoryos_v048_trajectory_digest_missing")
    if canonical_digest(raw_trajectory) != trajectory_digest:
        raise ValueError("source_memoryos_v048_trajectory_digest_mismatch")

    trajectory: list[dict[str, Any]] = []
    previous_dephasing_numerator: int | None = None
    expected_pairs = {
        (left_id, right_id)
        for left_id in candidate_ids
        for right_id in candidate_ids
    }
    expected_history_pairs = {
        (row_id, column_id)
        for row_id in history_ids
        for column_id in history_ids
    }

    for index, raw_step in enumerate(raw_trajectory):
        if not isinstance(raw_step, Mapping):
            raise ValueError("source_memoryos_v048_step_invalid")
        step = dict(raw_step)
        if step.get("step_index") != index:
            raise ValueError("source_memoryos_v048_step_index_invalid")
        for field in (
            "all_step_candidate_entries_reconstructed",
            "all_step_candidate_row_relations_exact",
            "all_step_candidate_column_relations_exact",
            "candidate_four_by_four_determinant_zero",
            "all_step_v047_triple_records_bound_to_factorization",
            "candidate_gram_rank_at_most_two_by_factorization",
        ):
            if step.get(field) is not True:
                raise ValueError("source_memoryos_v048_step_required_" + field)

        denominator = _integer(
            step.get("kernel_entry_denominator"),
            "source_memoryos_v048_denominator",
        )
        if denominator <= 0:
            raise ValueError("source_memoryos_v048_denominator_nonpositive")
        dephasing_numerator = _integer(
            step.get("dephasing_numerator"),
            "source_memoryos_v048_dephasing_numerator",
            nonnegative=True,
        )
        if (
            previous_dephasing_numerator is not None
            and dephasing_numerator >= previous_dephasing_numerator
        ):
            raise ValueError(
                "source_memoryos_v048_dephasing_not_strictly_decreasing"
            )
        previous_dephasing_numerator = dephasing_numerator

        raw_metric = step.get("history_metric_entries")
        if not isinstance(raw_metric, list):
            raise ValueError("source_memoryos_v048_history_metric_invalid")
        metric_by_ids: dict[tuple[str, str], tuple[int, int]] = {}
        for raw_entry in raw_metric:
            if not isinstance(raw_entry, Mapping):
                raise ValueError(
                    "source_memoryos_v048_history_metric_entry_invalid"
                )
            item = dict(raw_entry)
            pair = (
                item.get("row_history_id"),
                item.get("column_history_id"),
            )
            if pair not in expected_history_pairs or pair in metric_by_ids:
                raise ValueError(
                    "source_memoryos_v048_history_metric_pair_invalid"
                )
            metric_by_ids[pair] = (
                _integer(
                    item.get("real_numerator"),
                    "source_memoryos_v048_history_metric_real",
                ),
                _integer(
                    item.get("imag_numerator"),
                    "source_memoryos_v048_history_metric_imag",
                ),
            )
        if set(metric_by_ids) != expected_history_pairs:
            raise ValueError(
                "source_memoryos_v048_history_metric_support_mismatch"
            )
        for row_id in history_ids:
            diagonal = metric_by_ids[row_id, row_id]
            if diagonal[1] != 0 or diagonal[0] < 0:
                raise ValueError(
                    "source_memoryos_v048_history_metric_diagonal_invalid"
                )
            for column_id in history_ids:
                forward = metric_by_ids[row_id, column_id]
                reverse = metric_by_ids[column_id, row_id]
                if forward[0] != reverse[0] or forward[1] != -reverse[1]:
                    raise ValueError(
                        "source_memoryos_v048_history_metric_not_hermitian"
                    )

        raw_reconstruction = step.get(
            "candidate_kernel_reconstruction_records"
        )
        if not isinstance(raw_reconstruction, list):
            raise ValueError(
                "source_memoryos_v048_reconstruction_records_invalid"
            )
        entries: dict[tuple[str, str], tuple[int, int]] = {}
        for raw_record in raw_reconstruction:
            if not isinstance(raw_record, Mapping):
                raise ValueError(
                    "source_memoryos_v048_reconstruction_record_invalid"
                )
            record = dict(raw_record)
            pair = (
                record.get("left_candidate_id"),
                record.get("right_candidate_id"),
            )
            if pair not in expected_pairs or pair in entries:
                raise ValueError(
                    "source_memoryos_v048_reconstruction_pair_invalid"
                )
            if (
                record.get("factorization_reconstruction_exact") is not True
                or record.get("pair_retained") is not True
            ):
                raise ValueError(
                    "source_memoryos_v048_reconstruction_witness_missing"
                )
            source_entry = (
                _integer(
                    record.get("source_real_numerator"),
                    "source_memoryos_v048_source_real",
                ),
                _integer(
                    record.get("source_imag_numerator"),
                    "source_memoryos_v048_source_imag",
                ),
            )
            reconstructed_entry = (
                _integer(
                    record.get("reconstructed_real_numerator"),
                    "source_memoryos_v048_reconstructed_real",
                ),
                _integer(
                    record.get("reconstructed_imag_numerator"),
                    "source_memoryos_v048_reconstructed_imag",
                ),
            )
            if source_entry != reconstructed_entry:
                raise ValueError(
                    "source_memoryos_v048_reconstruction_value_mismatch"
                )
            entries[pair] = source_entry
        if set(entries) != expected_pairs:
            raise ValueError(
                "source_memoryos_v048_candidate_pair_support_mismatch"
            )
        for left_id in candidate_ids:
            diagonal = entries[left_id, left_id]
            if diagonal[1] != 0 or diagonal[0] < 0:
                raise ValueError(
                    "source_memoryos_v048_candidate_diagonal_invalid"
                )
            for right_id in candidate_ids:
                forward = entries[left_id, right_id]
                reverse = entries[right_id, left_id]
                if forward[0] != reverse[0] or forward[1] != -reverse[1]:
                    raise ValueError(
                        "source_memoryos_v048_candidate_kernel_not_hermitian"
                    )

        metric = {
            (0, 0): metric_by_ids[history_ids[0], history_ids[0]],
            (0, 1): metric_by_ids[history_ids[0], history_ids[1]],
            (1, 0): metric_by_ids[history_ids[1], history_ids[0]],
            (1, 1): metric_by_ids[history_ids[1], history_ids[1]],
        }
        anchor_binding = {
            (0, 0): entries["reobserve", "reobserve"],
            (0, 1): entries["reobserve", "terminate_candidate"],
            (1, 0): entries["terminate_candidate", "reobserve"],
            (1, 1): entries["terminate_candidate", "terminate_candidate"],
        }
        if metric != anchor_binding:
            raise ValueError(
                "source_memoryos_v048_history_anchor_binding_mismatch"
            )

        trajectory.append(
            {
                "step_index": index,
                "dephasing_numerator": dephasing_numerator,
                "kernel_entry_denominator": denominator,
                "history_metric": metric,
                "entries": entries,
            }
        )

    review_fields = {
        field: _review_ids(observables, field, candidate_ids)
        for field in (
            "source_relational_frontier_candidate_ids",
            "source_required_review_candidate_ids",
            "source_dissent_review_candidate_ids",
            "source_minority_protection_candidate_ids",
        )
    }
    source_v045_digest = observables.get(
        "source_memoryos_v045_certificate_digest"
    )
    source_v045_kernel_digest = observables.get(
        "source_memoryos_v045_candidate_gram_kernel_digest"
    )
    if not isinstance(source_v045_digest, str) or not source_v045_digest:
        raise ValueError("source_memoryos_v048_v045_digest_missing")
    if (
        not isinstance(source_v045_kernel_digest, str)
        or not source_v045_kernel_digest
    ):
        raise ValueError("source_memoryos_v048_v045_kernel_digest_missing")

    return {
        "certificate_digest": digest,
        "observables": observables,
        "candidate_ids": candidate_ids,
        "history_ids": history_ids,
        "factor_map": factor_map,
        "trajectory": trajectory,
        "trajectory_digest": trajectory_digest,
        "source_memoryos_v045_certificate_digest": source_v045_digest,
        "source_memoryos_v045_candidate_gram_kernel_digest": (
            source_v045_kernel_digest
        ),
        **review_fields,
    }


def issue_candidate_nullspace_dephasing_rank_stratification_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked("payload_invalid")
    blockers: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        blockers.append("schema_version_invalid")

    try:
        source = _normalize_source_memoryos_v048(
            payload.get("source_memoryos_v048_certificate")
        )
        source_v045 = _normalize_source_memoryos_v045(
            payload.get("source_memoryos_v045_certificate")
        )
    except ValueError as exc:
        return _blocked(*(blockers + [str(exc)]))

    if (
        source["source_memoryos_v045_certificate_digest"]
        != source_v045["certificate_digest"]
    ):
        blockers.append("source_v048_v045_certificate_binding_mismatch")
    if (
        source["source_memoryos_v045_candidate_gram_kernel_digest"]
        != source_v045["kernel_digest"]
    ):
        blockers.append("source_v048_v045_kernel_binding_mismatch")
    if source["candidate_ids"] != source_v045["candidate_ids"]:
        blockers.append("source_v048_v045_candidate_support_mismatch")
    if source["history_ids"] != source_v045["history_ids"]:
        blockers.append("source_v048_v045_history_support_mismatch")
    if source["factor_map"] != source_v045["coupling_map"]:
        blockers.append("source_v048_v045_factor_matrix_mismatch")
    if len(source["trajectory"]) != len(source_v045["trajectory"]):
        blockers.append("source_v048_v045_trajectory_length_mismatch")
    else:
        for v048_step, v045_step in zip(
            source["trajectory"],
            source_v045["trajectory"],
            strict=True,
        ):
            if (
                v048_step["step_index"] != v045_step["step_index"]
                or v048_step["dephasing_numerator"]
                != v045_step["dephasing_numerator"]
                or v048_step["kernel_entry_denominator"]
                != v045_step["kernel_entry_denominator"]
                or v048_step["entries"] != v045_step["entries"]
            ):
                blockers.append("source_v048_v045_trajectory_binding_mismatch")
                break
    if blockers:
        return _blocked(*blockers)

    candidate_ids = source["candidate_ids"]
    factor_map = source["factor_map"]
    structural_basis = [
        {
            "relation_id": relation_id,
            "candidate_coefficients": _candidate_coefficients(
                values,
                candidate_ids,
            ),
            "lifted_history_coordinates": list(
                _factor_lift(
                    _candidate_coefficients(values, candidate_ids),
                    factor_map,
                    candidate_ids,
                )
            ),
        }
        for relation_id, values in STRUCTURAL_NULL_RELATIONS
    ]

    structural_basis_exact = all(
        item["lifted_history_coordinates"] == [0, 0]
        for item in structural_basis
    )
    structural_plus_coherence_independence_minor = 1
    rank_trajectory: list[dict[str, Any]] = []
    all_structural_kernel_actions_zero = True
    all_structural_energies_zero = True
    all_history_determinants_real_nonnegative = True
    rank_values: list[int] = []
    nullity_values: list[int] = []
    antisymmetric_energies: list[int] = []
    symmetric_energies: list[int] = []
    extra_null_flags: list[bool] = []

    for source_step in source["trajectory"]:
        entries = source_step["entries"]
        denominator = source_step["kernel_entry_denominator"]
        structural_records: list[dict[str, Any]] = []
        for relation_id, values in STRUCTURAL_NULL_RELATIONS:
            coefficients = _candidate_coefficients(values, candidate_ids)
            lifted = _factor_lift(coefficients, factor_map, candidate_ids)
            left_action = _kernel_action(
                entries,
                coefficients,
                candidate_ids,
                side="left",
            )
            right_action = _kernel_action(
                entries,
                coefficients,
                candidate_ids,
                side="right",
            )
            energy = _quadratic_energy(
                entries,
                coefficients,
                candidate_ids,
            )
            left_zero = all(item["zero"] for item in left_action)
            right_zero = all(item["zero"] for item in right_action)
            energy_zero = energy == (0, 0)
            structural_records.append(
                {
                    "relation_id": relation_id,
                    "candidate_coefficients": coefficients,
                    "lifted_first_history_coordinate": lifted[0],
                    "lifted_second_history_coordinate": lifted[1],
                    "left_kernel_action": left_action,
                    "right_kernel_action": right_action,
                    "left_kernel_action_zero": left_zero,
                    "right_kernel_action_zero": right_zero,
                    "quadratic_energy_real_numerator": energy[0],
                    "quadratic_energy_imag_numerator": energy[1],
                    "quadratic_energy_denominator": denominator,
                    "quadratic_energy_zero": energy_zero,
                    "structural_null_relation_exact": (
                        lifted == (0, 0)
                        and left_zero
                        and right_zero
                        and energy_zero
                    ),
                }
            )
            all_structural_kernel_actions_zero = (
                all_structural_kernel_actions_zero
                and left_zero
                and right_zero
            )
            all_structural_energies_zero = (
                all_structural_energies_zero and energy_zero
            )

        metric = source_step["history_metric"]
        determinant = _history_determinant(metric)
        if determinant[1] != 0 or determinant[0] < 0:
            all_history_determinants_real_nonnegative = False
        if determinant == (0, 0):
            effective_rank = 1
        elif determinant[1] == 0 and determinant[0] > 0:
            effective_rank = 2
        else:
            effective_rank = 0
        candidate_nullity = len(candidate_ids) - effective_rank

        antisymmetric_coefficients = _candidate_coefficients(
            ANTISYMMETRIC_HISTORY_PROBE,
            candidate_ids,
        )
        symmetric_coefficients = _candidate_coefficients(
            SYMMETRIC_HISTORY_PROBE,
            candidate_ids,
        )
        antisymmetric_lift = _factor_lift(
            antisymmetric_coefficients,
            factor_map,
            candidate_ids,
        )
        symmetric_lift = _factor_lift(
            symmetric_coefficients,
            factor_map,
            candidate_ids,
        )
        antisymmetric_energy = _quadratic_energy(
            entries,
            antisymmetric_coefficients,
            candidate_ids,
        )
        symmetric_energy = _quadratic_energy(
            entries,
            symmetric_coefficients,
            candidate_ids,
        )
        antisymmetric_zero = antisymmetric_energy == (0, 0)

        rank_values.append(effective_rank)
        nullity_values.append(candidate_nullity)
        antisymmetric_energies.append(antisymmetric_energy[0])
        symmetric_energies.append(symmetric_energy[0])
        extra_null_flags.append(antisymmetric_zero)

        rank_trajectory.append(
            {
                "step_index": source_step["step_index"],
                "dephasing_numerator": source_step[
                    "dephasing_numerator"
                ],
                "kernel_entry_denominator": denominator,
                "structural_null_relation_records": structural_records,
                "all_step_structural_null_relations_exact": all(
                    item["structural_null_relation_exact"]
                    for item in structural_records
                ),
                "history_metric_determinant_real_numerator": determinant[0],
                "history_metric_determinant_imag_numerator": determinant[1],
                "history_metric_determinant_denominator": denominator**2,
                "history_metric_effective_rank": effective_rank,
                "candidate_gram_effective_rank": effective_rank,
                "structural_candidate_nullity": len(
                    STRUCTURAL_NULL_RELATIONS
                ),
                "candidate_gram_nullity": candidate_nullity,
                "antisymmetric_history_probe_candidate_coefficients": (
                    antisymmetric_coefficients
                ),
                "antisymmetric_history_probe_lifted_coordinates": list(
                    antisymmetric_lift
                ),
                "antisymmetric_history_probe_energy_real_numerator": (
                    antisymmetric_energy[0]
                ),
                "antisymmetric_history_probe_energy_imag_numerator": (
                    antisymmetric_energy[1]
                ),
                "antisymmetric_history_probe_energy_denominator": denominator,
                "antisymmetric_history_probe_is_kernel_null": (
                    antisymmetric_zero
                ),
                "symmetric_history_probe_candidate_coefficients": (
                    symmetric_coefficients
                ),
                "symmetric_history_probe_lifted_coordinates": list(
                    symmetric_lift
                ),
                "symmetric_history_probe_energy_real_numerator": (
                    symmetric_energy[0]
                ),
                "symmetric_history_probe_energy_imag_numerator": (
                    symmetric_energy[1]
                ),
                "symmetric_history_probe_energy_denominator": denominator,
                "symmetric_history_probe_positive": (
                    symmetric_energy[1] == 0
                    and symmetric_energy[0] > 0
                ),
                "structural_plus_coherence_null_independence_minor": (
                    structural_plus_coherence_independence_minor
                ),
                "extra_coherence_null_direction_active": antisymmetric_zero,
            }
        )

    expected_rank_trajectory = [1, 2, 2]
    expected_nullity_trajectory = [3, 2, 2]
    expected_antisymmetric_energies = [0, 2, 4]
    expected_symmetric_energies = [8, 6, 4]
    expected_extra_null_flags = [True, False, False]

    input_digest = canonical_digest(
        {
            "schema_version": SCHEMA_VERSION,
            "source_memoryos_v048_certificate_digest": source[
                "certificate_digest"
            ],
            "source_memoryos_v048_factorization_digest": source[
                "trajectory_digest"
            ],
            "source_memoryos_v045_certificate_digest": source_v045[
                "certificate_digest"
            ],
            "source_memoryos_v045_candidate_gram_kernel_digest": source_v045[
                "kernel_digest"
            ],
            "candidate_ids": candidate_ids,
            "history_ids": source["history_ids"],
            "structural_null_basis": structural_basis,
        }
    )
    rank_digest = canonical_digest(rank_trajectory)

    observables = {
        "input_digest": input_digest,
        "source_memoryos_v048_certificate_digest": source[
            "certificate_digest"
        ],
        "source_memoryos_v048_factorization_digest": source[
            "trajectory_digest"
        ],
        "source_memoryos_v045_certificate_digest": source_v045[
            "certificate_digest"
        ],
        "source_memoryos_v045_candidate_gram_kernel_digest": source_v045[
            "kernel_digest"
        ],
        "retained_history_ids": source["history_ids"],
        "retained_decision_candidate_ids": candidate_ids,
        "candidate_structural_null_basis": structural_basis,
        "candidate_structural_null_basis_dimension": len(
            STRUCTURAL_NULL_RELATIONS
        ),
        "structural_plus_coherence_null_independence_minor": (
            structural_plus_coherence_independence_minor
        ),
        "candidate_nullspace_rank_stratification_trajectory": (
            rank_trajectory
        ),
        "candidate_nullspace_rank_stratification_digest": rank_digest,
        "history_metric_rank_trajectory": rank_values,
        "candidate_gram_rank_trajectory": rank_values,
        "candidate_gram_nullity_trajectory": nullity_values,
        "antisymmetric_history_probe_energy_real_numerators": (
            antisymmetric_energies
        ),
        "symmetric_history_probe_energy_real_numerators": (
            symmetric_energies
        ),
        "extra_coherence_null_direction_active_trajectory": (
            extra_null_flags
        ),
        "source_memoryos_v048_exact": True,
        "source_memoryos_v045_exact": True,
        "structural_null_basis_exact": structural_basis_exact,
        "all_structural_null_directions_kernel_annihilated": (
            all_structural_kernel_actions_zero
        ),
        "all_structural_null_quadratic_evidence_zero": (
            all_structural_energies_zero
        ),
        "candidate_quadratic_evidence_invariant_under_structural_null_translation": (
            structural_basis_exact
            and all_structural_kernel_actions_zero
            and all_structural_energies_zero
        ),
        "all_history_metric_determinants_real_nonnegative": (
            all_history_determinants_real_nonnegative
        ),
        "history_rank_trajectory_exact": (
            rank_values == expected_rank_trajectory
        ),
        "candidate_rank_trajectory_exact": (
            rank_values == expected_rank_trajectory
        ),
        "candidate_nullity_trajectory_exact": (
            nullity_values == expected_nullity_trajectory
        ),
        "antisymmetric_probe_energy_trajectory_exact": (
            antisymmetric_energies
            == expected_antisymmetric_energies
        ),
        "symmetric_probe_energy_trajectory_exact": (
            symmetric_energies == expected_symmetric_energies
        ),
        "structural_nullspace_persists_across_dephasing": (
            all_structural_kernel_actions_zero
            and all_structural_energies_zero
        ),
        "full_coherence_extra_null_direction_independent": (
            structural_plus_coherence_independence_minor != 0
            and extra_null_flags[0]
        ),
        "dephasing_releases_extra_coherence_null_direction": (
            extra_null_flags == expected_extra_null_flags
        ),
        "dephasing_recovers_candidate_rank_from_one_to_two": (
            rank_values == expected_rank_trajectory
        ),
        "full_coherence_candidate_nullity_three": (
            nullity_values[0] == 3
        ),
        "post_dephasing_candidate_nullity_two": (
            nullity_values[1:] == [2, 2]
        ),
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "source_relational_frontier_candidate_ids": source[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": source[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": source[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": source[
            "source_minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "nullspace_witness_advisory_only": True,
        "null_direction_not_candidate_dispensability": True,
        "rank_recovery_not_candidate_preference": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v048_mutated": False,
        "source_memoryos_v045_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }

    for field in (
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
    ):
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
    "SOURCE_MEMORYOS_V048_SCHEMA_VERSION",
    "EXPECTED_CANDIDATE_IDS",
    "STRUCTURAL_NULL_RELATIONS",
    "ANTISYMMETRIC_HISTORY_PROBE",
    "SYMMETRIC_HISTORY_PROBE",
    "canonical_digest",
    "issue_candidate_nullspace_dephasing_rank_stratification_certificate",
]
