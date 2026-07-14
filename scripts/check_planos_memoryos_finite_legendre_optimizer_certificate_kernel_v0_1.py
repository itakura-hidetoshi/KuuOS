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

from runtime.kuuos_memoryos_finite_log_mgf_chernoff_tail_certificate_kernel_v0_1 import (
    issue_finite_log_mgf_chernoff_tail_certificate,
)
from runtime.kuuos_memoryos_finite_legendre_optimizer_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_finite_legendre_optimizer_certificate,
)
from scripts.check_planos_memoryos_finite_log_mgf_chernoff_tail_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v064_payload,
)


def source_memoryos_v064_certificate() -> dict[str, Any]:
    result = issue_finite_log_mgf_chernoff_tail_certificate(
        build_memoryos_v064_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v064 = source_memoryos_v064_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v064_certificate": source_v064,
        "claims": _derive_observables(source_v064),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_finite_legendre_optimizer_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_finite_legendre_optimizer_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "finite_tilt_grid_record_count": 5,
        "finite_legendre_rate_profile_record_count": 44,
        "explicit_extinct_profile_optimizer_record_count": 4,
        "marton_legendre_optimizer_input_record_count": 22,
        "full_rank_transport_legendre_optimizer_record_count": 8,
        "singular_atomic_legendre_optimizer_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    tilt_grid = obs["finite_tilt_grid_records"]
    assert [record["tilt"] for record in tilt_grid] == [
        {"numerator": n, "denominator": 1} for n in range(5)
    ]
    assert all(
        record["tilt_nonnegative"]
        and record["tilt_at_most_four"]
        and record["exact_rational"]
        for record in tilt_grid
    )

    rate_profiles = {
        (
            record["observable_id"],
            record["horizon"],
            record["threshold_id"],
        ): record
        for record in obs["finite_legendre_rate_profile_records"]
    }
    assert len(rate_profiles) == 44
    slow_half = rate_profiles[("slow", 3, "half")]
    assert slow_half["support_values"] == [
        {"numerator": 27, "denominator": 64},
        {"numerator": 0, "denominator": 1},
        {"numerator": -27, "denominator": 64},
    ]
    assert len(slow_half["finite_tilt_candidates"]) == 5
    assert all(
        record["finite_argmax_exists_formally_proved"]
        and record["legendre_fenchel_rate_is_finite_grid_max"]
        and record["legendre_fenchel_rate_nonnegative_formally_proved"]
        and record["optimized_envelope_is_exp_neg_rate"]
        and record["optimized_envelope_tail_bound_formally_proved"]
        and not record["numeric_transcendental_approximation_used"]
        and not record["continuous_tilt_optimizer_claimed"]
        and not record["general_large_deviation_principle_claimed"]
        for record in rate_profiles.values()
    )

    explicit = {
        record["record_id"]: record
        for record in obs["explicit_extinct_profile_optimizer_records"]
    }
    expected_coefficients = {
        "slow_half_tail_extinction": [
            {"numerator": -5, "denominator": 16},
            {"numerator": -2, "denominator": 1},
            {"numerator": -59, "denominator": 16},
        ],
        "slow_quarter_tail_extinction": [
            {"numerator": -13, "denominator": 256},
            {"numerator": -1, "denominator": 1},
            {"numerator": -499, "denominator": 256},
        ],
        "fast_half_tail_extinction": [
            {"numerator": -1, "denominator": 1},
            {"numerator": -1, "denominator": 1},
            {"numerator": -4, "denominator": 1},
        ],
        "fast_quarter_tail_extinction": [
            {"numerator": -3, "denominator": 4},
            {"numerator": -3, "denominator": 4},
            {"numerator": -3, "denominator": 2},
        ],
    }
    for record_id, coefficients in expected_coefficients.items():
        record = explicit[record_id]
        assert record["selected_tilt"] == {
            "numerator": 4,
            "denominator": 1,
        }
        assert record["selected_envelope_exponent_coefficients"] == coefficients
        assert record["selected_tilt_is_grid_maximum"]
        assert record["all_support_strictly_below_threshold"]
        assert record["all_selected_exponent_coefficients_negative"]
        assert record["tail_extinct_exact"]
        assert record["tilt_four_is_finite_grid_optimizer_formally_proved"]
        assert record[
            "optimized_envelope_equals_tilt_four_formally_proved"
        ]
        assert not record["numeric_transcendental_approximation_used"]

    assert obs["finite_tilt_grid_exact"]
    assert obs["finite_legendre_optimizer_exists_for_all_profiles"]
    assert obs["finite_legendre_rate_nonnegative_exact"]
    assert obs["optimized_envelope_tail_bounds_exact"]
    assert obs["all_explicit_extinct_profile_tilt_four_optimizers_exact"]
    assert obs["marton_legendre_optimizer_inputs_exact"]
    assert obs["continuous_tilt_optimizer_not_claimed"]
    assert obs["general_large_deviation_principle_not_claimed"]
    assert obs["general_path_space_gaussian_theorem_not_claimed"]

    assert all(
        record["finite_legendre_rate_commutes"]
        and record["finite_optimizer_commutes"]
        and record["optimized_envelope_commutes"]
        for record in obs["full_rank_transport_legendre_optimizer_records"]
    )
    assert all(
        record["atomic_finite_legendre_candidates_retained"]
        and record["atomic_optimizer_witness_retained"]
        and record["atomic_optimized_envelope_retained"]
        and not record["two_dimensional_target_density_emitted"]
        and not record["lost_coordinate_reconstructed"]
        for record in obs["singular_atomic_legendre_optimizer_records"]
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v064_certificate"]["observables"][
        "exact_tail_extinction_threshold_records"
    ][0]["certified_horizon"] = 2
    _resign(tampered["source_memoryos_v064_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v064_exact_tail_extinction_threshold_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["explicit_extinct_profile_optimizer_records"][0][
        "selected_tilt"
    ] = {"numerator": 3, "denominator": 1}
    assert_rejects(
        tampered,
        "claim_mismatch_explicit_extinct_profile_optimizer_records",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["continuous_tilt_optimizer_not_claimed"] = False
    assert_rejects(
        tampered,
        "claim_mismatch_continuous_tilt_optimizer_not_claimed",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(tampered, "claim_mismatch_candidate_selection_performed")

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": result["schema_version"],
                "certificate_digest": result["certificate_digest"],
                "finite_tilt_grid_digest": obs["finite_tilt_grid_digest"],
                "finite_legendre_rate_profile_digest": obs[
                    "finite_legendre_rate_profile_digest"
                ],
                "explicit_extinct_profile_optimizer_digest": obs[
                    "explicit_extinct_profile_optimizer_digest"
                ],
                "marton_legendre_optimizer_input_digest": obs[
                    "marton_legendre_optimizer_input_digest"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
