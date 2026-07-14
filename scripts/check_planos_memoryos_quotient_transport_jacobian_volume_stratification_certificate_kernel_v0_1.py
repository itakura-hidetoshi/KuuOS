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

from runtime.kuuos_memoryos_candidate_quotient_mode_diagonalization_inverse_certificate_kernel_v0_1 import (
    issue_candidate_quotient_mode_diagonalization_inverse_certificate,
)
from runtime.kuuos_memoryos_quotient_metric_covector_transport_certificate_kernel_v0_1 import (
    issue_quotient_metric_covector_transport_certificate,
)
from runtime.kuuos_memoryos_quotient_transport_jacobian_volume_stratification_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_quotient_transport_jacobian_volume_stratification_certificate,
)
from scripts.check_planos_memoryos_candidate_quotient_mode_diagonalization_inverse_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v051_payload,
)
from scripts.check_planos_memoryos_quotient_metric_covector_transport_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v052_payload,
)


def source_memoryos_v051_certificate() -> dict[str, Any]:
    result = issue_candidate_quotient_mode_diagonalization_inverse_certificate(
        build_memoryos_v051_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def source_memoryos_v052_certificate() -> dict[str, Any]:
    result = issue_quotient_metric_covector_transport_certificate(
        build_memoryos_v052_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v052 = source_memoryos_v052_certificate()
    source_v051 = source_memoryos_v051_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v052_certificate": source_v052,
        "source_memoryos_v051_certificate": source_v051,
        "claims": _derive_observables(source_v052, source_v051),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def _resign_v052(certificate: dict[str, Any]) -> None:
    observables = certificate["observables"]
    observables["quotient_metric_covector_transport_digest"] = canonical_digest(
        observables["quotient_metric_covector_transport_trajectory"]
    )
    observables["quotient_metric_transport_composition_digest"] = canonical_digest(
        observables["quotient_metric_transport_composition_records"]
    )
    _resign(certificate)


def _resign_v051(certificate: dict[str, Any]) -> None:
    observables = certificate["observables"]
    observables[
        "candidate_quotient_mode_diagonalization_digest"
    ] = canonical_digest(
        observables["candidate_quotient_mode_diagonalization_trajectory"]
    )
    _resign(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_quotient_transport_jacobian_volume_stratification_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_quotient_transport_jacobian_volume_stratification_certificate(
        payload
    )
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    assert obs["transition_count"] == 9
    assert obs["probe_mode_transport_record_count"] == 81
    assert obs["composition_record_count"] == 27
    assert obs["normalized_transport_count"] == 6
    assert obs["invertible_full_rank_transition_count"] == 4
    assert obs["full_rank_to_rank_one_volume_collapse_count"] == 2
    assert obs["rank_one_source_boundary_count"] == 3
    assert obs["normalized_composition_active_count"] == 12
    assert obs["invertible_full_rank_path_count"] == 8

    assert obs["reference_one_to_zero_symmetric_multiplier"] == {
        "numerator": 2,
        "denominator": 3,
    }
    assert obs["reference_one_to_zero_antisymmetric_multiplier"] == {
        "numerator": 2,
        "denominator": 1,
    }
    assert obs["reference_one_to_zero_jacobian"] == {
        "numerator": 4,
        "denominator": 3,
    }
    assert obs["reference_zero_to_one_symmetric_multiplier"] == {
        "numerator": 3,
        "denominator": 2,
    }
    assert obs["reference_zero_to_one_antisymmetric_multiplier"] == {
        "numerator": 1,
        "denominator": 2,
    }
    assert obs["reference_zero_to_one_jacobian"] == {
        "numerator": 3,
        "denominator": 4,
    }

    transitions = obs["quotient_transport_jacobian_trajectory"]
    one_to_zero = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 1
        and item["target_cross_numerator"] == 0
    )
    assert one_to_zero["invertible_full_rank_transport"] is True
    assert one_to_zero["orientation_preserving_full_rank"] is True
    assert one_to_zero["normalized_mode_product_equals_jacobian"] is True
    assert one_to_zero["transport_determinant_numerator"] == 12

    collapse = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 1
        and item["target_cross_numerator"] == 2
    )
    assert collapse["normalized_transport_active"] is True
    assert collapse["full_rank_to_rank_one_volume_collapse"] is True
    assert collapse["normalized_jacobian"] == {
        "numerator": 0,
        "denominator": 1,
    }
    assert collapse["invertible_full_rank_transport"] is False

    boundary = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 2
        and item["target_cross_numerator"] == 1
    )
    assert boundary["rank_one_source_boundary"] is True
    assert boundary["normalized_transport_active"] is False
    assert boundary["normalized_jacobian"] is None
    assert boundary[
        "rank_one_source_has_no_two_dimensional_jacobian"
    ] is True
    assert boundary["all_step_boundary_symmetric_partial_exact"] is True
    assert boundary["all_step_boundary_recovery_claims_false"] is True

    compositions = obs["quotient_transport_mode_composition_records"]
    assert all(
        item["raw_symmetric_mode_composition_exact"]
        and item["raw_antisymmetric_mode_composition_exact"]
        for item in compositions
    )
    assert all(
        not item["normalized_composition_active"]
        or item["normalized_mode_composition_exact"]
        for item in compositions
    )

    tampered = copy.deepcopy(payload)
    tampered_transition = tampered["source_memoryos_v052_certificate"][
        "observables"
    ]["quotient_metric_covector_transport_trajectory"][4]
    tampered_transition["transport_numerator_matrix"][0][0] += 1
    _resign_v052(tampered["source_memoryos_v052_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v052_transport_matrix_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v051_certificate"]["observables"][
        "candidate_quotient_mode_diagonalization_trajectory"
    ][1]["antisymmetric_mode_weight_numerator"] = 2
    _resign_v051(tampered["source_memoryos_v051_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v051_step_antisymmetric_weight_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"][
        "rank_one_boundary_has_no_two_dimensional_jacobian"
    ] = False
    assert_rejects(
        tampered,
        "claim_mismatch_rank_one_boundary_has_no_two_dimensional_jacobian",
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
                "jacobian_digest": obs[
                    "quotient_transport_jacobian_digest"
                ],
                "composition_digest": obs[
                    "quotient_transport_mode_composition_digest"
                ],
                "transition_count": obs["transition_count"],
                "probe_mode_transport_record_count": obs[
                    "probe_mode_transport_record_count"
                ],
                "normalized_transport_count": obs[
                    "normalized_transport_count"
                ],
                "invertible_full_rank_transition_count": obs[
                    "invertible_full_rank_transition_count"
                ],
                "rank_one_source_boundary_count": obs[
                    "rank_one_source_boundary_count"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
