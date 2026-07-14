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

from runtime.kuuos_memoryos_candidate_quotient_coordinate_canonicalization_certificate_kernel_v0_1 import (
    issue_candidate_quotient_coordinate_canonicalization_certificate,
)
from runtime.kuuos_memoryos_two_history_candidate_gram_factorization_reconstruction_certificate_kernel_v0_1 import (
    issue_two_history_candidate_gram_factorization_reconstruction_certificate,
)
from runtime.kuuos_memoryos_candidate_quotient_mode_diagonalization_inverse_certificate_kernel_v0_1 import (
    EXPECTED_PROBE_VECTORS,
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_candidate_quotient_mode_diagonalization_inverse_certificate,
)
from scripts.check_planos_memoryos_candidate_quotient_coordinate_canonicalization_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v050_payload,
)
from scripts.check_planos_memoryos_two_history_candidate_gram_factorization_reconstruction_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v048_payload,
)


def source_memoryos_v050_certificate() -> dict[str, Any]:
    result = issue_candidate_quotient_coordinate_canonicalization_certificate(
        build_memoryos_v050_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def source_memoryos_v048_certificate() -> dict[str, Any]:
    result = issue_two_history_candidate_gram_factorization_reconstruction_certificate(
        build_memoryos_v048_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v050 = source_memoryos_v050_certificate()
    source_v048 = source_memoryos_v048_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v050_certificate": source_v050,
        "source_memoryos_v048_certificate": source_v048,
        "claims": _derive_observables(source_v050, source_v048),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def _resign_v050(certificate: dict[str, Any]) -> None:
    observables = certificate["observables"]
    observables["candidate_quotient_coordinate_certificate_digest"] = (
        canonical_digest(
            {
                "canonicalization_records": observables[
                    "candidate_quotient_canonicalization_records"
                ],
                "quotient_trajectory": observables[
                    "candidate_quotient_metric_descent_trajectory"
                ],
            }
        )
    )
    _resign(certificate)


def _resign_v048(certificate: dict[str, Any]) -> None:
    observables = certificate["observables"]
    observables["two_history_candidate_gram_factorization_digest"] = (
        canonical_digest(
            observables[
                "two_history_candidate_gram_factorization_trajectory"
            ]
        )
    )
    _resign(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_candidate_quotient_mode_diagonalization_inverse_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def _history_pairing(
    cross: int,
    left: tuple[int, int],
    right: tuple[int, int],
) -> int:
    return (
        2 * left[0] * right[0]
        + cross * left[0] * right[1]
        + cross * left[1] * right[0]
        + 2 * left[1] * right[1]
    )


def _mode_pairing_doubled(
    cross: int,
    left: tuple[int, int],
    right: tuple[int, int],
) -> int:
    return (
        (2 + cross) * (left[0] + left[1]) * (right[0] + right[1])
        + (2 - cross) * (left[0] - left[1]) * (right[0] - right[1])
    )


def main() -> int:
    payload = build_reference_payload()
    result = issue_candidate_quotient_mode_diagonalization_inverse_certificate(
        payload
    )
    assert result["accepted"], result["blockers"]
    observables = result["observables"]
    trajectory = observables[
        "candidate_quotient_mode_diagonalization_trajectory"
    ]

    assert observables["symmetric_mode_weight_trajectory"] == [4, 3, 2]
    assert observables["antisymmetric_mode_weight_trajectory"] == [0, 1, 2]
    assert observables["quotient_metric_determinant_trajectory"] == [0, 3, 4]
    assert observables["quotient_metric_rank_trajectory"] == [1, 2, 2]
    assert observables["inverse_witness_active_trajectory"] == [
        False,
        True,
        True,
    ]
    assert len(trajectory) == 3
    assert all(
        len(step["probe_mode_quadratic_records"])
        == len(EXPECTED_PROBE_VECTORS)
        for step in trajectory
    )
    assert all(
        len(step["ordered_probe_pair_mode_bilinear_records"])
        == len(EXPECTED_PROBE_VECTORS) ** 2
        for step in trajectory
    )

    source_records = {
        record["probe_id"]: record
        for record in payload["source_memoryos_v050_certificate"][
            "observables"
        ]["candidate_quotient_canonicalization_records"]
    }
    coordinates = {
        probe_id: (
            record["quotient_first_history_coordinate"],
            record["quotient_second_history_coordinate"],
        )
        for probe_id, record in source_records.items()
    }

    for step in trajectory:
        cross = step["dephasing_numerator"]
        determinant = 4 - cross * cross
        assert step["symmetric_mode_weight_numerator"] == 2 + cross
        assert step["antisymmetric_mode_weight_numerator"] == 2 - cross
        assert step["quotient_metric_determinant_numerator"] == determinant
        assert step["determinant_factorization_exact"]
        assert step["symmetric_mode_eigenvector_exact"]
        assert step["antisymmetric_mode_eigenvector_exact"]
        assert step["adjugate_inverse_witness_exact"]
        assert step["metric_times_adjugate"] == [
            [determinant, 0],
            [0, determinant],
        ]
        assert step["adjugate_times_metric"] == [
            [determinant, 0],
            [0, determinant],
        ]

        quadratic_records = {
            record["probe_id"]: record
            for record in step["probe_mode_quadratic_records"]
        }
        for probe_id, coordinate in coordinates.items():
            expected_source = _history_pairing(
                cross,
                coordinate,
                coordinate,
            )
            expected_mode = _mode_pairing_doubled(
                cross,
                coordinate,
                coordinate,
            )
            record = quadratic_records[probe_id]
            assert record["source_quadratic_real_numerator"] == expected_source
            assert (
                record["mode_diagonal_doubled_real_numerator"]
                == expected_mode
                == 2 * expected_source
            )
            assert record["mode_diagonalization_exact"]
            assert record["source_memoryos_v050_quadratic_bound"]

        pair_records = {
            (record["left_probe_id"], record["right_probe_id"]): record
            for record in step[
                "ordered_probe_pair_mode_bilinear_records"
            ]
        }
        for left_id, left in coordinates.items():
            for right_id, right in coordinates.items():
                expected_source = _history_pairing(cross, left, right)
                expected_mode = _mode_pairing_doubled(cross, left, right)
                record = pair_records[left_id, right_id]
                assert record["source_bilinear_real_numerator"] == expected_source
                assert (
                    record["mode_diagonal_doubled_real_numerator"]
                    == expected_mode
                    == 2 * expected_source
                )
                assert record["mode_diagonalization_exact"]
                assert record["source_memoryos_v050_pairing_bound"]

    mixed = next(
        record
        for record in trajectory[0]["probe_mode_quadratic_records"]
        if record["probe_id"] == "mixed_candidate_probe"
    )
    assert mixed["symmetric_mode_coordinate"] == 11
    assert mixed["antisymmetric_mode_coordinate"] == -3
    antisymmetric = next(
        record
        for record in trajectory[0]["probe_mode_quadratic_records"]
        if record["probe_id"] == "antisymmetric_history_probe"
    )
    assert antisymmetric["source_quadratic_real_numerator"] == 0
    assert trajectory[0]["full_coherence_rank_one"]
    assert not trajectory[0]["inverse_witness_active"]
    assert trajectory[1]["inverse_witness_active"]
    assert trajectory[2]["inverse_witness_active"]

    tampered = copy.deepcopy(payload)
    tampered_record = tampered["source_memoryos_v050_certificate"][
        "observables"
    ]["candidate_quotient_canonicalization_records"][0]
    tampered_record["quotient_first_history_coordinate"] = 2
    _resign_v050(tampered["source_memoryos_v050_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v050_probe_coordinates_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v050_certificate"]["observables"][
        "candidate_quotient_metric_descent_trajectory"
    ][0]["probe_quadratic_descent_records"][0][
        "canonical_real_numerator"
    ] += 1
    _resign_v050(tampered["source_memoryos_v050_certificate"])
    assert_rejects(
        tampered,
        "observable_required_all_source_memoryos_v050_descent_records_bound",
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
    tampered["claims"]["symmetric_mode_weight_trajectory"] = [4, 4, 2]
    assert_rejects(
        tampered,
        "claim_mismatch_symmetric_mode_weight_trajectory",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(
        tampered,
        "claim_mismatch_candidate_selection_performed",
    )

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": result["schema_version"],
                "certificate_digest": result["certificate_digest"],
                "mode_digest": observables[
                    "candidate_quotient_mode_diagonalization_digest"
                ],
                "probe_vector_count": observables["probe_vector_count"],
                "ordered_probe_pair_count_per_step": observables[
                    "ordered_probe_pair_count_per_step"
                ],
                "symmetric_mode_weights": observables[
                    "symmetric_mode_weight_trajectory"
                ],
                "antisymmetric_mode_weights": observables[
                    "antisymmetric_mode_weight_trajectory"
                ],
                "determinants": observables[
                    "quotient_metric_determinant_trajectory"
                ],
                "ranks": observables["quotient_metric_rank_trajectory"],
                "mixed_probe_modes": [11, -3],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
