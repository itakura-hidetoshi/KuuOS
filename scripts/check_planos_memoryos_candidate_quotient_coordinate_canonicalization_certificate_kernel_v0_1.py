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

from runtime.kuuos_memoryos_candidate_nullspace_dephasing_rank_stratification_certificate_kernel_v0_1 import (
    issue_candidate_nullspace_dephasing_rank_stratification_certificate,
)
from runtime.kuuos_memoryos_two_history_candidate_gram_factorization_reconstruction_certificate_kernel_v0_1 import (
    issue_two_history_candidate_gram_factorization_reconstruction_certificate,
)
from runtime.kuuos_memoryos_candidate_quotient_coordinate_canonicalization_certificate_kernel_v0_1 import (
    EXPECTED_PROBE_VECTORS,
    SCHEMA_VERSION,
    _canonical_representative,
    _coefficients,
    _coordinates,
    _difference,
    _normalize_source_memoryos_v049,
    _pairing,
    _structural_combination,
    canonical_digest,
    issue_candidate_quotient_coordinate_canonicalization_certificate,
)
from scripts.check_planos_memoryos_candidate_nullspace_dephasing_rank_stratification_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v049_payload,
)
from scripts.check_planos_memoryos_two_history_candidate_gram_factorization_reconstruction_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v048_payload,
)


def source_memoryos_v048_certificate() -> dict[str, Any]:
    result = issue_two_history_candidate_gram_factorization_reconstruction_certificate(
        build_memoryos_v048_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def source_memoryos_v049_certificate() -> dict[str, Any]:
    result = issue_candidate_nullspace_dephasing_rank_stratification_certificate(
        build_memoryos_v049_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def expected_observables(
    source_v049_certificate: dict[str, Any],
    source_v048_certificate: dict[str, Any],
) -> dict[str, Any]:
    source_v049 = _normalize_source_memoryos_v049(source_v049_certificate)
    source_v048_obs = source_v048_certificate["observables"]
    source_v048_trajectory = source_v048_obs[
        "two_history_candidate_gram_factorization_trajectory"
    ]
    source_v048_entries = [
        {
            (
                record["left_candidate_id"],
                record["right_candidate_id"],
            ): (
                record["source_real_numerator"],
                record["source_imag_numerator"],
            )
            for record in step["candidate_kernel_reconstruction_records"]
        }
        for step in source_v048_trajectory
    ]

    canonicalization_records: list[dict[str, Any]] = []
    probe_map: dict[str, dict[str, int]] = {}
    canonical_map: dict[str, dict[str, int]] = {}
    for probe_id, values in EXPECTED_PROBE_VECTORS:
        original = _coefficients(values)
        coordinates = _coordinates(original)
        canonical = _canonical_representative(coordinates)
        residual = _difference(original, canonical)
        structural = _structural_combination(
            original["continue"],
            original["hold"],
        )
        probe_map[probe_id] = original
        canonical_map[probe_id] = canonical
        canonicalization_records.append(
            {
                "probe_id": probe_id,
                "source_candidate_coefficients": original,
                "quotient_first_history_coordinate": coordinates[0],
                "quotient_second_history_coordinate": coordinates[1],
                "canonical_candidate_coefficients": canonical,
                "structural_translation_alpha": original["continue"],
                "structural_translation_beta": original["hold"],
                "source_minus_canonical_coefficients": residual,
                "structural_null_combination_coefficients": structural,
                "source_equals_canonical_plus_structural_null": (
                    residual == structural
                ),
                "canonical_coordinates_preserved": (
                    _coordinates(canonical) == coordinates
                ),
                "canonical_continue_zero": canonical["continue"] == 0,
                "canonical_hold_zero": canonical["hold"] == 0,
                "canonical_representative_unique_in_chart": (
                    canonical
                    == {
                        "continue": 0,
                        "hold": 0,
                        "reobserve": coordinates[0],
                        "terminate_candidate": coordinates[1],
                    }
                ),
                "probe_retained": True,
            }
        )

    quotient_trajectory: list[dict[str, Any]] = []
    for step, entries in zip(
        source_v048_trajectory,
        source_v048_entries,
        strict=True,
    ):
        quadratic_records: list[dict[str, Any]] = []
        pair_records: list[dict[str, Any]] = []
        for probe_id, _ in EXPECTED_PROBE_VECTORS:
            source_quadratic = _pairing(
                entries,
                probe_map[probe_id],
                probe_map[probe_id],
            )
            canonical_quadratic = _pairing(
                entries,
                canonical_map[probe_id],
                canonical_map[probe_id],
            )
            quadratic_records.append(
                {
                    "probe_id": probe_id,
                    "source_real_numerator": source_quadratic[0],
                    "source_imag_numerator": source_quadratic[1],
                    "canonical_real_numerator": canonical_quadratic[0],
                    "canonical_imag_numerator": canonical_quadratic[1],
                    "denominator": step["kernel_entry_denominator"],
                    "quadratic_evidence_descends_exactly": (
                        source_quadratic == canonical_quadratic
                    ),
                }
            )
            for right_probe_id, _ in EXPECTED_PROBE_VECTORS:
                source_pairing = _pairing(
                    entries,
                    probe_map[probe_id],
                    probe_map[right_probe_id],
                )
                canonical_pairing = _pairing(
                    entries,
                    canonical_map[probe_id],
                    canonical_map[right_probe_id],
                )
                pair_records.append(
                    {
                        "left_probe_id": probe_id,
                        "right_probe_id": right_probe_id,
                        "source_real_numerator": source_pairing[0],
                        "source_imag_numerator": source_pairing[1],
                        "canonical_real_numerator": canonical_pairing[0],
                        "canonical_imag_numerator": canonical_pairing[1],
                        "denominator": step["kernel_entry_denominator"],
                        "bilinear_pairing_descends_exactly": (
                            source_pairing == canonical_pairing
                        ),
                        "ordered_probe_pair_retained": True,
                    }
                )
        quotient_trajectory.append(
            {
                "step_index": step["step_index"],
                "dephasing_numerator": step["dephasing_numerator"],
                "kernel_entry_denominator": step["kernel_entry_denominator"],
                "probe_quadratic_descent_records": quadratic_records,
                "ordered_probe_pair_descent_records": pair_records,
                "all_step_quadratic_evidence_descends_exactly": all(
                    item["quadratic_evidence_descends_exactly"]
                    for item in quadratic_records
                ),
                "all_step_bilinear_pairings_descend_exactly": all(
                    item["bilinear_pairing_descends_exactly"]
                    for item in pair_records
                ),
                "quotient_metric_rank": source_v049[
                    "observables"
                ]["candidate_gram_rank_trajectory"][step["step_index"]],
                "quotient_metric_nullity_removed": 2,
            }
        )

    input_digest = canonical_digest(
        {
            "schema_version": SCHEMA_VERSION,
            "source_memoryos_v049_certificate_digest": source_v049[
                "certificate_digest"
            ],
            "source_memoryos_v049_rank_digest": source_v049[
                "trajectory_digest"
            ],
            "source_memoryos_v048_certificate_digest": source_v048_certificate[
                "certificate_digest"
            ],
            "source_memoryos_v048_factorization_digest": source_v048_obs[
                "two_history_candidate_gram_factorization_digest"
            ],
            "candidate_ids": source_v048_obs[
                "retained_decision_candidate_ids"
            ],
            "history_ids": source_v048_obs["retained_history_ids"],
            "probe_vectors": [
                {"probe_id": probe_id, "coefficients": _coefficients(values)}
                for probe_id, values in EXPECTED_PROBE_VECTORS
            ],
        }
    )
    quotient_digest = canonical_digest(
        {
            "canonicalization_records": canonicalization_records,
            "quotient_trajectory": quotient_trajectory,
        }
    )
    return {
        "input_digest": input_digest,
        "source_memoryos_v049_certificate_digest": source_v049[
            "certificate_digest"
        ],
        "source_memoryos_v049_rank_stratification_digest": source_v049[
            "trajectory_digest"
        ],
        "source_memoryos_v048_certificate_digest": source_v048_certificate[
            "certificate_digest"
        ],
        "source_memoryos_v048_factorization_digest": source_v048_obs[
            "two_history_candidate_gram_factorization_digest"
        ],
        "retained_history_ids": source_v048_obs["retained_history_ids"],
        "retained_decision_candidate_ids": source_v048_obs[
            "retained_decision_candidate_ids"
        ],
        "quotient_coordinate_names": [
            "first_history_coordinate",
            "second_history_coordinate",
        ],
        "canonical_chart_fixed_zero_candidate_ids": ["continue", "hold"],
        "canonical_chart_anchor_candidate_ids": [
            "reobserve",
            "terminate_candidate",
        ],
        "probe_candidate_coefficient_vectors": [
            {"probe_id": probe_id, "coefficients": _coefficients(values)}
            for probe_id, values in EXPECTED_PROBE_VECTORS
        ],
        "candidate_quotient_canonicalization_records": (
            canonicalization_records
        ),
        "candidate_quotient_metric_descent_trajectory": quotient_trajectory,
        "candidate_quotient_coordinate_certificate_digest": quotient_digest,
        "probe_vector_count": len(EXPECTED_PROBE_VECTORS),
        "ordered_probe_pair_count_per_step": len(EXPECTED_PROBE_VECTORS) ** 2,
        "structural_null_dimension_quotiented": 2,
        "quotient_coordinate_dimension": 2,
        "source_memoryos_v049_exact": True,
        "source_memoryos_v048_exact": True,
        "all_probe_canonical_decompositions_exact": True,
        "all_probe_quotient_coordinates_preserved": True,
        "all_probe_canonical_representatives_unique_in_chart": True,
        "all_probe_quadratic_evidence_descends_to_quotient": True,
        "all_ordered_probe_pairings_descend_to_quotient": True,
        "quotient_metric_rank_trajectory_preserved": [
            step["quotient_metric_rank"] for step in quotient_trajectory
        ]
        == [1, 2, 2],
        "structural_nullspace_removed_from_coordinates_not_candidates": True,
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "source_relational_frontier_candidate_ids": source_v049[
            "source_relational_frontier_candidate_ids"
        ],
        "source_required_review_candidate_ids": source_v049[
            "source_required_review_candidate_ids"
        ],
        "source_dissent_review_candidate_ids": source_v049[
            "source_dissent_review_candidate_ids"
        ],
        "source_minority_protection_candidate_ids": source_v049[
            "source_minority_protection_candidate_ids"
        ],
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "quotient_coordinate_witness_advisory_only": True,
        "canonical_representative_not_candidate_selection": True,
        "quotient_not_candidate_pruning": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v049_mutated": False,
        "source_memoryos_v048_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }


def build_reference_payload() -> dict[str, Any]:
    source_v049 = source_memoryos_v049_certificate()
    source_v048 = source_memoryos_v048_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v049_certificate": source_v049,
        "source_memoryos_v048_certificate": source_v048,
        "claims": expected_observables(source_v049, source_v048),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def _resign_v049(certificate: dict[str, Any]) -> None:
    trajectory = certificate["observables"][
        "candidate_nullspace_rank_stratification_trajectory"
    ]
    certificate["observables"][
        "candidate_nullspace_rank_stratification_digest"
    ] = canonical_digest(trajectory)
    _resign(certificate)


def _resign_v048(certificate: dict[str, Any]) -> None:
    trajectory = certificate["observables"][
        "two_history_candidate_gram_factorization_trajectory"
    ]
    certificate["observables"][
        "two_history_candidate_gram_factorization_digest"
    ] = canonical_digest(trajectory)
    _resign(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_candidate_quotient_coordinate_canonicalization_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_candidate_quotient_coordinate_canonicalization_certificate(
        payload
    )
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    records = {
        item["probe_id"]: item
        for item in obs["candidate_quotient_canonicalization_records"]
    }
    assert records["continue_basis"]["canonical_candidate_coefficients"] == {
        "continue": 0,
        "hold": 0,
        "reobserve": 1,
        "terminate_candidate": 1,
    }
    assert records["hold_basis"]["canonical_candidate_coefficients"] == {
        "continue": 0,
        "hold": 0,
        "reobserve": 1,
        "terminate_candidate": -1,
    }
    assert records["first_structural_null"][
        "canonical_candidate_coefficients"
    ] == {
        "continue": 0,
        "hold": 0,
        "reobserve": 0,
        "terminate_candidate": 0,
    }
    assert records["mixed_candidate_probe"][
        "canonical_candidate_coefficients"
    ] == {
        "continue": 0,
        "hold": 0,
        "reobserve": 4,
        "terminate_candidate": 7,
    }
    trajectory = obs["candidate_quotient_metric_descent_trajectory"]
    assert [step["quotient_metric_rank"] for step in trajectory] == [1, 2, 2]
    assert all(
        len(step["ordered_probe_pair_descent_records"]) == 81
        for step in trajectory
    )
    assert all(
        step["all_step_bilinear_pairings_descend_exactly"]
        and step["all_step_quadratic_evidence_descends_exactly"]
        for step in trajectory
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v049_certificate"]["observables"][
        "candidate_structural_null_basis"
    ][0]["candidate_coefficients"]["continue"] = 2
    _resign_v049(tampered["source_memoryos_v049_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v049_structural_basis_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v048_certificate"]["observables"][
        "candidate_factor_matrix"
    ][0]["first_history_coefficient"] = 2
    _resign_v048(tampered["source_memoryos_v048_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v048_factor_matrix_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["canonical_chart_fixed_zero_candidate_ids"] = [
        "reobserve",
        "terminate_candidate",
    ]
    assert_rejects(
        tampered,
        "claim_mismatch_canonical_chart_fixed_zero_candidate_ids",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(
        tampered,
        "claim_mismatch_candidate_selection_performed",
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v049_certificate"]["observables"][
        "candidate_gram_rank_trajectory"
    ] = [2, 2, 2]
    _resign(tampered["source_memoryos_v049_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v049_candidate_rank_trajectory_mismatch",
    )

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": result["schema_version"],
                "certificate_digest": result["certificate_digest"],
                "quotient_digest": obs[
                    "candidate_quotient_coordinate_certificate_digest"
                ],
                "probe_vector_count": obs["probe_vector_count"],
                "ordered_probe_pair_count_per_step": obs[
                    "ordered_probe_pair_count_per_step"
                ],
                "quotient_rank_trajectory": [
                    step["quotient_metric_rank"] for step in trajectory
                ],
                "mixed_probe_coordinates": [
                    records["mixed_candidate_probe"][
                        "quotient_first_history_coordinate"
                    ],
                    records["mixed_candidate_probe"][
                        "quotient_second_history_coordinate"
                    ],
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
