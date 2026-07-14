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

from runtime.kuuos_memoryos_finite_legendre_optimizer_certificate_kernel_v0_1 import (
    issue_finite_legendre_optimizer_certificate,
)
from runtime.kuuos_memoryos_continuous_log_mgf_convexity_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_continuous_log_mgf_convexity_certificate,
)
from scripts.check_planos_memoryos_finite_legendre_optimizer_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v065_payload,
)


def source_memoryos_v065_certificate() -> dict[str, Any]:
    result = issue_finite_legendre_optimizer_certificate(
        build_memoryos_v065_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v065 = source_memoryos_v065_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v065_certificate": source_v065,
        "claims": _derive_observables(source_v065),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_continuous_log_mgf_convexity_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_continuous_log_mgf_convexity_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "derivative_curvature_profile_record_count": 22,
        "continuous_stationarity_input_record_count": 44,
        "continuous_finite_grid_comparison_record_count": 44,
        "bounded_interval_boundary_optimizer_record_count": 4,
        "marton_continuous_optimizer_input_record_count": 22,
        "full_rank_transport_continuous_optimizer_record_count": 8,
        "singular_atomic_continuous_optimizer_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    derivative_profiles = {
        (record["observable_id"], record["horizon"]): record
        for record in obs["derivative_curvature_profile_records"]
    }
    assert len(derivative_profiles) == 22
    slow_three = derivative_profiles[("slow", 3)]
    assert slow_three["support_values"] == [
        {"numerator": 27, "denominator": 64},
        {"numerator": 0, "denominator": 1},
        {"numerator": -27, "denominator": 64},
    ]
    assert slow_three["pairwise_curvature_terms"] == [
        {
            "left_state_index": 0,
            "right_state_index": 1,
            "exponent_coefficient": {"numerator": 27, "denominator": 64},
            "squared_gap": {"numerator": 729, "denominator": 4096},
            "nonnegative": True,
        },
        {
            "left_state_index": 0,
            "right_state_index": 2,
            "exponent_coefficient": {"numerator": 0, "denominator": 1},
            "squared_gap": {"numerator": 729, "denominator": 1024},
            "nonnegative": True,
        },
        {
            "left_state_index": 1,
            "right_state_index": 2,
            "exponent_coefficient": {"numerator": -27, "denominator": 64},
            "squared_gap": {"numerator": 729, "denominator": 4096},
            "nonnegative": True,
        },
    ]
    assert all(
        record["partition_strictly_positive_formally_proved"]
        and record["partition_derivative_formally_proved"]
        and record["first_moment_derivative_formally_proved"]
        and record["log_mgf_derivative_is_tilted_mean_formally_proved"]
        and record["tilted_mean_derivative_is_curvature_formally_proved"]
        and record["pairwise_square_curvature_identity_formally_proved"]
        and record["tilted_curvature_nonnegative_formally_proved"]
        and record["log_mgf_convex_on_real_formally_proved"]
        and not record["numeric_transcendental_approximation_used"]
        for record in derivative_profiles.values()
    )

    stationarity = {
        (
            record["observable_id"],
            record["horizon"],
            record["threshold_id"],
        ): record
        for record in obs["continuous_stationarity_input_records"]
    }
    assert len(stationarity) == 44
    slow_half = stationarity[("slow", 3, "half")]
    assert slow_half["threshold"] == {"numerator": 1, "denominator": 2}
    assert slow_half[
        "symbolic_stationary_equation"
    ] == "sum_i x_i*exp(lambda*x_i)/sum_i exp(lambda*x_i)=threshold"
    assert all(
        record[
            "legendre_derivative_is_threshold_minus_tilted_mean_formally_proved"
        ]
        and record["global_optimizer_implies_local_max_formally_proved"]
        and record["fermat_stationary_equation_formally_proved"]
        and not record["global_optimizer_existence_claimed"]
        and not record["closed_form_optimizer_claimed"]
        and not record["numeric_transcendental_root_used"]
        for record in stationarity.values()
    )

    comparisons = obs["continuous_finite_grid_comparison_records"]
    assert all(
        record[
            "continuous_global_rate_dominates_finite_grid_rate_formally_proved"
        ]
        and record[
            "continuous_global_envelope_le_finite_grid_envelope_formally_proved"
        ]
        and record["comparison_conditional_on_global_optimizer_witness"]
        and record["source_finite_optimizer_witness_retained"]
        and not record["numeric_transcendental_root_used"]
        for record in comparisons
    )

    boundary = {
        record["record_id"]: record
        for record in obs["bounded_interval_boundary_optimizer_records"]
    }
    assert set(boundary) == {
        "slow_half_tail_extinction",
        "slow_quarter_tail_extinction",
        "fast_half_tail_extinction",
        "fast_quarter_tail_extinction",
    }
    for record in boundary.values():
        assert record["interval_lower"] == {"numerator": 0, "denominator": 1}
        assert record["interval_upper"] == {"numerator": 4, "denominator": 1}
        assert record["continuous_interval_optimizer"] == {
            "numerator": 4,
            "denominator": 1,
        }
        assert record["all_support_below_threshold"]
        assert record["legendre_objective_monotone_on_interval_formally_proved"]
        assert record["tilt_four_continuous_interval_optimizer_formally_proved"]
        assert record["finite_rate_equals_tilt_four_objective_formally_proved"]
        assert not record["unbounded_optimizer_existence_claimed"]

    for field in (
        "all_partition_derivatives_exact",
        "all_log_mgf_derivatives_exact",
        "all_tilted_curvatures_nonnegative_exact",
        "all_log_mgf_profiles_convex_on_real_exact",
        "all_global_optimizer_stationary_equations_exact",
        "all_continuous_finite_grid_comparisons_exact",
        "all_bounded_interval_boundary_optimizers_exact",
        "marton_continuous_optimizer_inputs_exact",
        "all_full_rank_transport_continuous_optimizer_commutes",
        "singular_atomic_continuous_optimizer_retained",
        "unbounded_continuous_optimizer_existence_not_claimed",
        "closed_form_transcendental_optimizer_not_claimed",
        "general_cramer_theorem_not_claimed",
        "general_gartner_ellis_theorem_not_claimed",
        "general_large_deviation_principle_not_claimed",
        "general_path_space_gaussian_theorem_not_claimed",
        "rank_one_source_two_dimensional_recovery_not_claimed",
        "future_only",
        "read_only",
    ):
        assert obs[field] is True, field

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v065_certificate"]["observables"][
        "finite_legendre_rate_profile_records"
    ][0]["support_values"][0] = {"numerator": 99, "denominator": 1}
    _resign(tampered["source_memoryos_v065_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v065_finite_legendre_rate_profile_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["derivative_curvature_profile_records"][0][
        "tilted_curvature_nonnegative_formally_proved"
    ] = False
    assert_rejects(
        tampered,
        "claim_mismatch_derivative_curvature_profile_records",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"][
        "unbounded_continuous_optimizer_existence_not_claimed"
    ] = False
    assert_rejects(
        tampered,
        "claim_mismatch_unbounded_continuous_optimizer_existence_not_claimed",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(tampered, "claim_mismatch_candidate_selection_performed")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_continuous_truth"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_continuous_truth")

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": result["schema_version"],
                "certificate_digest": result["certificate_digest"],
                "derivative_curvature_profile_digest": obs[
                    "derivative_curvature_profile_digest"
                ],
                "continuous_stationarity_input_digest": obs[
                    "continuous_stationarity_input_digest"
                ],
                "continuous_finite_grid_comparison_digest": obs[
                    "continuous_finite_grid_comparison_digest"
                ],
                "bounded_interval_boundary_optimizer_digest": obs[
                    "bounded_interval_boundary_optimizer_digest"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
