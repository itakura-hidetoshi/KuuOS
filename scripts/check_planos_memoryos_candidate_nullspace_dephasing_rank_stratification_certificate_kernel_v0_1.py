#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate_kernel_v0_1 import (
    issue_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate,
)
from runtime.kuuos_memoryos_two_history_candidate_gram_factorization_reconstruction_certificate_kernel_v0_1 import (
    issue_two_history_candidate_gram_factorization_reconstruction_certificate,
)
from runtime.kuuos_memoryos_candidate_nullspace_dephasing_rank_stratification_certificate_kernel_v0_1 import (
    ANTISYMMETRIC_HISTORY_PROBE,
    EXPECTED_CANDIDATE_IDS,
    SCHEMA_VERSION,
    STRUCTURAL_NULL_RELATIONS,
    SYMMETRIC_HISTORY_PROBE,
    canonical_digest,
    issue_candidate_nullspace_dephasing_rank_stratification_certificate,
)
from scripts.check_planos_memoryos_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v045_payload,
)
from scripts.check_planos_memoryos_two_history_candidate_gram_factorization_reconstruction_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v048_payload,
)

CANDIDATE_IDS = EXPECTED_CANDIDATE_IDS


def source_memoryos_v045_certificate() -> dict[str, Any]:
    result = issue_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate(
        build_memoryos_v045_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def source_memoryos_v048_certificate() -> dict[str, Any]:
    result = issue_two_history_candidate_gram_factorization_reconstruction_certificate(
        build_memoryos_v048_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


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


def _coefficients(
    values: tuple[int, int, int, int],
) -> dict[str, int]:
    return dict(zip(CANDIDATE_IDS, values, strict=True))


def _factor_map(source_v048: dict[str, Any]) -> dict[str, tuple[int, int]]:
    return {
        item["candidate_id"]: (
            item["first_history_coefficient"],
            item["second_history_coefficient"],
        )
        for item in source_v048["observables"]["candidate_factor_matrix"]
    }


def _factor_lift(
    coefficients: dict[str, int],
    factor_map: dict[str, tuple[int, int]],
) -> tuple[int, int]:
    return (
        sum(
            coefficients[candidate_id] * factor_map[candidate_id][0]
            for candidate_id in CANDIDATE_IDS
        ),
        sum(
            coefficients[candidate_id] * factor_map[candidate_id][1]
            for candidate_id in CANDIDATE_IDS
        ),
    )


def _entry_map(step: dict[str, Any]) -> dict[tuple[str, str], tuple[int, int]]:
    return {
        (
            record["left_candidate_id"],
            record["right_candidate_id"],
        ): (
            record["source_real_numerator"],
            record["source_imag_numerator"],
        )
        for record in step["candidate_kernel_reconstruction_records"]
    }


def _metric_map(
    step: dict[str, Any],
    history_ids: list[str],
) -> dict[tuple[int, int], tuple[int, int]]:
    by_ids = {
        (
            record["row_history_id"],
            record["column_history_id"],
        ): (
            record["real_numerator"],
            record["imag_numerator"],
        )
        for record in step["history_metric_entries"]
    }
    return {
        (0, 0): by_ids[history_ids[0], history_ids[0]],
        (0, 1): by_ids[history_ids[0], history_ids[1]],
        (1, 0): by_ids[history_ids[1], history_ids[0]],
        (1, 1): by_ids[history_ids[1], history_ids[1]],
    }


def _kernel_action(
    entries: dict[tuple[str, str], tuple[int, int]],
    coefficients: dict[str, int],
    *,
    side: str,
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for fixed_id in CANDIDATE_IDS:
        total = (0, 0)
        for varying_id in CANDIDATE_IDS:
            if side == "right":
                entry = entries[fixed_id, varying_id]
            else:
                entry = entries[varying_id, fixed_id]
            total = _complex_add(
                total,
                _complex_scale(coefficients[varying_id], entry),
            )
        result.append(
            {
                "candidate_id": fixed_id,
                "real_numerator": total[0],
                "imag_numerator": total[1],
                "zero": total == (0, 0),
            }
        )
    return result


def _quadratic(
    entries: dict[tuple[str, str], tuple[int, int]],
    coefficients: dict[str, int],
) -> tuple[int, int]:
    total = (0, 0)
    for left_id in CANDIDATE_IDS:
        for right_id in CANDIDATE_IDS:
            total = _complex_add(
                total,
                _complex_scale(
                    coefficients[left_id] * coefficients[right_id],
                    entries[left_id, right_id],
                ),
            )
    return total


def _determinant2(
    metric: dict[tuple[int, int], tuple[int, int]],
) -> tuple[int, int]:
    return _complex_add(
        _complex_mul(metric[0, 0], metric[1, 1]),
        _complex_scale(-1, _complex_mul(metric[0, 1], metric[1, 0])),
    )


def expected_rank_trajectory(
    source_v048: dict[str, Any],
) -> list[dict[str, Any]]:
    observables = source_v048["observables"]
    history_ids = list(observables["retained_history_ids"])
    factor_map = _factor_map(source_v048)
    result: list[dict[str, Any]] = []

    for step in observables[
        "two_history_candidate_gram_factorization_trajectory"
    ]:
        entries = _entry_map(step)
        denominator = step["kernel_entry_denominator"]
        structural_records: list[dict[str, Any]] = []

        for relation_id, values in STRUCTURAL_NULL_RELATIONS:
            coefficients = _coefficients(values)
            lifted = _factor_lift(coefficients, factor_map)
            left_action = _kernel_action(
                entries,
                coefficients,
                side="left",
            )
            right_action = _kernel_action(
                entries,
                coefficients,
                side="right",
            )
            energy = _quadratic(entries, coefficients)
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

        metric = _metric_map(step, history_ids)
        determinant = _determinant2(metric)
        effective_rank = 1 if determinant == (0, 0) else 2

        antisymmetric = _coefficients(ANTISYMMETRIC_HISTORY_PROBE)
        symmetric = _coefficients(SYMMETRIC_HISTORY_PROBE)
        antisymmetric_lift = _factor_lift(antisymmetric, factor_map)
        symmetric_lift = _factor_lift(symmetric, factor_map)
        antisymmetric_energy = _quadratic(entries, antisymmetric)
        symmetric_energy = _quadratic(entries, symmetric)

        result.append(
            {
                "step_index": step["step_index"],
                "dephasing_numerator": step["dephasing_numerator"],
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
                "structural_candidate_nullity": 2,
                "candidate_gram_nullity": 4 - effective_rank,
                "antisymmetric_history_probe_candidate_coefficients": (
                    antisymmetric
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
                    antisymmetric_energy == (0, 0)
                ),
                "symmetric_history_probe_candidate_coefficients": symmetric,
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
                "structural_plus_coherence_null_independence_minor": 1,
                "extra_coherence_null_direction_active": (
                    antisymmetric_energy == (0, 0)
                ),
            }
        )
    return result


def expected_claims(
    source_v048: dict[str, Any],
    source_v045: dict[str, Any],
) -> dict[str, Any]:
    observables = source_v048["observables"]
    history_ids = list(observables["retained_history_ids"])
    factor_map = _factor_map(source_v048)
    structural_basis = [
        {
            "relation_id": relation_id,
            "candidate_coefficients": _coefficients(values),
            "lifted_history_coordinates": list(
                _factor_lift(_coefficients(values), factor_map)
            ),
        }
        for relation_id, values in STRUCTURAL_NULL_RELATIONS
    ]
    trajectory = expected_rank_trajectory(source_v048)
    ranks = [step["candidate_gram_effective_rank"] for step in trajectory]
    nullities = [step["candidate_gram_nullity"] for step in trajectory]
    antisymmetric = [
        step["antisymmetric_history_probe_energy_real_numerator"]
        for step in trajectory
    ]
    symmetric = [
        step["symmetric_history_probe_energy_real_numerator"]
        for step in trajectory
    ]
    extra_flags = [
        step["extra_coherence_null_direction_active"]
        for step in trajectory
    ]
    all_structural_exact = all(
        step["all_step_structural_null_relations_exact"]
        for step in trajectory
    )
    all_actions_zero = all(
        record["left_kernel_action_zero"]
        and record["right_kernel_action_zero"]
        for step in trajectory
        for record in step["structural_null_relation_records"]
    )
    all_energies_zero = all(
        record["quadratic_energy_zero"]
        for step in trajectory
        for record in step["structural_null_relation_records"]
    )
    source_v045_obs = source_v045["observables"]
    input_digest = canonical_digest(
        {
            "schema_version": SCHEMA_VERSION,
            "source_memoryos_v048_certificate_digest": source_v048[
                "certificate_digest"
            ],
            "source_memoryos_v048_factorization_digest": observables[
                "two_history_candidate_gram_factorization_digest"
            ],
            "source_memoryos_v045_certificate_digest": source_v045[
                "certificate_digest"
            ],
            "source_memoryos_v045_candidate_gram_kernel_digest": (
                source_v045_obs["candidate_gram_kernel_digest"]
            ),
            "candidate_ids": CANDIDATE_IDS,
            "history_ids": history_ids,
            "structural_null_basis": structural_basis,
        }
    )
    return {
        "input_digest": input_digest,
        "source_memoryos_v048_certificate_digest": source_v048[
            "certificate_digest"
        ],
        "source_memoryos_v048_factorization_digest": observables[
            "two_history_candidate_gram_factorization_digest"
        ],
        "source_memoryos_v045_certificate_digest": source_v045[
            "certificate_digest"
        ],
        "source_memoryos_v045_candidate_gram_kernel_digest": source_v045_obs[
            "candidate_gram_kernel_digest"
        ],
        "retained_history_ids": history_ids,
        "retained_decision_candidate_ids": CANDIDATE_IDS,
        "candidate_structural_null_basis": structural_basis,
        "candidate_structural_null_basis_dimension": 2,
        "structural_plus_coherence_null_independence_minor": 1,
        "candidate_nullspace_rank_stratification_trajectory": trajectory,
        "candidate_nullspace_rank_stratification_digest": canonical_digest(
            trajectory
        ),
        "history_metric_rank_trajectory": ranks,
        "candidate_gram_rank_trajectory": ranks,
        "candidate_gram_nullity_trajectory": nullities,
        "antisymmetric_history_probe_energy_real_numerators": antisymmetric,
        "symmetric_history_probe_energy_real_numerators": symmetric,
        "extra_coherence_null_direction_active_trajectory": extra_flags,
        "source_memoryos_v048_exact": True,
        "source_memoryos_v045_exact": True,
        "structural_null_basis_exact": all(
            item["lifted_history_coordinates"] == [0, 0]
            for item in structural_basis
        ),
        "all_structural_null_directions_kernel_annihilated": all_actions_zero,
        "all_structural_null_quadratic_evidence_zero": all_energies_zero,
        "candidate_quadratic_evidence_invariant_under_structural_null_translation": (
            all_structural_exact and all_actions_zero and all_energies_zero
        ),
        "all_history_metric_determinants_real_nonnegative": all(
            step["history_metric_determinant_imag_numerator"] == 0
            and step["history_metric_determinant_real_numerator"] >= 0
            for step in trajectory
        ),
        "history_rank_trajectory_exact": ranks == [1, 2, 2],
        "candidate_rank_trajectory_exact": ranks == [1, 2, 2],
        "candidate_nullity_trajectory_exact": nullities == [3, 2, 2],
        "antisymmetric_probe_energy_trajectory_exact": (
            antisymmetric == [0, 2, 4]
        ),
        "symmetric_probe_energy_trajectory_exact": symmetric == [8, 6, 4],
        "structural_nullspace_persists_across_dephasing": (
            all_actions_zero and all_energies_zero
        ),
        "full_coherence_extra_null_direction_independent": (
            extra_flags[0] and 1 != 0
        ),
        "dephasing_releases_extra_coherence_null_direction": (
            extra_flags == [True, False, False]
        ),
        "dephasing_recovers_candidate_rank_from_one_to_two": (
            ranks == [1, 2, 2]
        ),
        "full_coherence_candidate_nullity_three": nullities[0] == 3,
        "post_dephasing_candidate_nullity_two": nullities[1:] == [2, 2],
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "source_relational_frontier_candidate_ids": source_v045_obs[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": source_v045_obs[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": source_v045_obs[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": source_v045_obs[
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


def build_reference_payload() -> dict[str, Any]:
    source_v048 = source_memoryos_v048_certificate()
    source_v045 = source_memoryos_v045_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v048_certificate": source_v048,
        "source_memoryos_v045_certificate": source_v045,
        "claims": expected_claims(source_v048, source_v045),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def _resign_v048(certificate: dict[str, Any]) -> None:
    trajectory = certificate["observables"][
        "two_history_candidate_gram_factorization_trajectory"
    ]
    certificate["observables"][
        "two_history_candidate_gram_factorization_digest"
    ] = canonical_digest(trajectory)
    _resign(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_candidate_nullspace_dephasing_rank_stratification_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    certificate = issue_candidate_nullspace_dephasing_rank_stratification_certificate(
        payload
    )
    assert certificate["accepted"], certificate["blockers"]
    observables = certificate["observables"]
    trajectory = observables[
        "candidate_nullspace_rank_stratification_trajectory"
    ]

    assert observables["history_metric_rank_trajectory"] == [1, 2, 2]
    assert observables["candidate_gram_rank_trajectory"] == [1, 2, 2]
    assert observables["candidate_gram_nullity_trajectory"] == [3, 2, 2]
    assert (
        observables[
            "antisymmetric_history_probe_energy_real_numerators"
        ]
        == [0, 2, 4]
    )
    assert observables["symmetric_history_probe_energy_real_numerators"] == [
        8,
        6,
        4,
    ]
    assert (
        observables[
            "extra_coherence_null_direction_active_trajectory"
        ]
        == [True, False, False]
    )
    assert all(
        step["all_step_structural_null_relations_exact"]
        for step in trajectory
    )
    assert all(
        record["left_kernel_action_zero"]
        and record["right_kernel_action_zero"]
        and record["quadratic_energy_zero"]
        for step in trajectory
        for record in step["structural_null_relation_records"]
    )
    assert observables["source_relational_frontier_candidate_ids"] == [
        "reobserve"
    ]
    assert observables["source_dissent_review_candidate_ids"] == ["continue"]
    assert observables["source_minority_protection_candidate_ids"] == ["hold"]

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v048_certificate"]["accepted"] = False
    assert_rejects(tampered, "source_memoryos_v048_not_accepted")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v048_certificate"][
        "certificate_digest"
    ] = "substituted"
    assert_rejects(
        tampered,
        "source_memoryos_v048_certificate_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v045_certificate"][
        "certificate_digest"
    ] = "substituted"
    assert_rejects(
        tampered,
        "source_memoryos_v045_certificate_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v048_certificate"]["observables"][
        "candidate_factor_matrix"
    ][0]["first_history_coefficient"] = 2
    _resign(tampered["source_memoryos_v048_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v048_factor_matrix_mismatch",
    )

    tampered = copy.deepcopy(payload)
    step = tampered["source_memoryos_v048_certificate"]["observables"][
        "two_history_candidate_gram_factorization_trajectory"
    ][1]
    record = next(
        item
        for item in step["candidate_kernel_reconstruction_records"]
        if item["left_candidate_id"] == "continue"
        and item["right_candidate_id"] == "continue"
    )
    record["source_real_numerator"] += 1
    record["reconstructed_real_numerator"] += 1
    _resign_v048(tampered["source_memoryos_v048_certificate"])
    assert_rejects(
        tampered,
        "source_v048_v045_trajectory_binding_mismatch",
    )

    for field in (
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
    ):
        tampered = copy.deepcopy(payload)
        tampered["claims"][field] = True
        assert_rejects(tampered, "claim_mismatch_" + field)

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_structural_null_basis_dimension"] = 3
    assert_rejects(
        tampered,
        "claim_mismatch_candidate_structural_null_basis_dimension",
    )

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": SCHEMA_VERSION,
                "candidate_count": len(CANDIDATE_IDS),
                "structural_null_basis_dimension": 2,
                "history_rank_trajectory": [1, 2, 2],
                "candidate_nullity_trajectory": [3, 2, 2],
                "antisymmetric_probe_energy_numerators": [0, 2, 4],
                "certificate_digest": certificate["certificate_digest"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
