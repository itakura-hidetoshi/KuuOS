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
from runtime.kuuos_memoryos_candidate_quotient_mode_diagonalization_inverse_certificate_kernel_v0_1 import (
    issue_candidate_quotient_mode_diagonalization_inverse_certificate,
)
from runtime.kuuos_memoryos_quotient_metric_covector_transport_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_quotient_metric_covector_transport_certificate,
)
from scripts.check_planos_memoryos_candidate_quotient_coordinate_canonicalization_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v050_payload,
)
from scripts.check_planos_memoryos_candidate_quotient_mode_diagonalization_inverse_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v051_payload,
)


def source_memoryos_v050_certificate() -> dict[str, Any]:
    result = issue_candidate_quotient_coordinate_canonicalization_certificate(
        build_memoryos_v050_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def source_memoryos_v051_certificate() -> dict[str, Any]:
    result = issue_candidate_quotient_mode_diagonalization_inverse_certificate(
        build_memoryos_v051_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v051 = source_memoryos_v051_certificate()
    source_v050 = source_memoryos_v050_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v051_certificate": source_v051,
        "source_memoryos_v050_certificate": source_v050,
        "claims": _derive_observables(source_v051, source_v050),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def _resign_v051(certificate: dict[str, Any]) -> None:
    trajectory = certificate["observables"][
        "candidate_quotient_mode_diagonalization_trajectory"
    ]
    certificate["observables"][
        "candidate_quotient_mode_diagonalization_digest"
    ] = canonical_digest(trajectory)
    _resign(certificate)


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


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_quotient_metric_covector_transport_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_quotient_metric_covector_transport_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    assert obs["transition_count"] == 9
    assert obs["probe_transport_record_count"] == 81
    assert obs["composition_record_count"] == 27
    assert obs["full_rank_transition_count"] == 6
    assert obs["rank_one_boundary_partial_transition_count"] == 3
    assert obs["reference_one_to_zero_transport_matrix"] == [
        [4, -2],
        [-2, 4],
    ]
    assert obs["reference_one_to_zero_transport_denominator"] == 3
    assert obs["reference_zero_to_one_transport_matrix"] == [
        [4, 2],
        [2, 4],
    ]
    assert obs["reference_zero_to_one_transport_denominator"] == 4

    transitions = obs["quotient_metric_covector_transport_trajectory"]
    one_to_zero = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 1
        and item["target_cross_numerator"] == 0
    )
    assert one_to_zero["full_rank_rational_transport_active"] is True
    assert one_to_zero["scaled_metric_transport_identity_exact"] is True
    assert all(
        item["scaled_transport_exact"]
        for item in one_to_zero["probe_transport_records"]
    )

    boundary = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 2
        and item["target_cross_numerator"] == 1
    )
    assert boundary["rank_one_boundary_partial_transport_only"] is True
    assert boundary["full_rank_rational_transport_active"] is False
    assert boundary["all_boundary_symmetric_partial_records_exact"] is True
    assert boundary[
        "all_boundary_antisymmetric_recovery_claims_false"
    ] is True

    assert all(
        item["composition_identity_exact"]
        for item in obs["quotient_metric_transport_composition_records"]
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v051_certificate"]["observables"][
        "candidate_quotient_mode_diagonalization_trajectory"
    ][1]["symmetric_mode_weight_numerator"] = 4
    _resign_v051(tampered["source_memoryos_v051_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v051_step_symmetric_weight_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v050_certificate"]["observables"][
        "candidate_quotient_canonicalization_records"
    ][0]["quotient_first_history_coordinate"] = 2
    _resign_v050(tampered["source_memoryos_v050_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v050_probe_coordinates_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"][
        "rank_one_boundary_antisymmetric_recovery_not_claimed"
    ] = False
    assert_rejects(
        tampered,
        "claim_mismatch_rank_one_boundary_antisymmetric_recovery_not_claimed",
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
                "transport_digest": obs[
                    "quotient_metric_covector_transport_digest"
                ],
                "composition_digest": obs[
                    "quotient_metric_transport_composition_digest"
                ],
                "transition_count": obs["transition_count"],
                "probe_transport_record_count": obs[
                    "probe_transport_record_count"
                ],
                "composition_record_count": obs["composition_record_count"],
                "full_rank_transition_count": obs[
                    "full_rank_transition_count"
                ],
                "rank_one_boundary_partial_transition_count": obs[
                    "rank_one_boundary_partial_transition_count"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
