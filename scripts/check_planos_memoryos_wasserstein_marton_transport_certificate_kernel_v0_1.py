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

from runtime.kuuos_memoryos_bakry_emery_concentration_certificate_kernel_v0_1 import (
    issue_bakry_emery_concentration_certificate,
)
from runtime.kuuos_memoryos_wasserstein_marton_transport_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_wasserstein_marton_transport_certificate,
)
from scripts.check_planos_memoryos_bakry_emery_concentration_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v061_payload,
)


def source_memoryos_v061_certificate() -> dict[str, Any]:
    result = issue_bakry_emery_concentration_certificate(
        build_memoryos_v061_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v061 = source_memoryos_v061_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v061_certificate": source_v061,
        "claims": _derive_observables(source_v061),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_wasserstein_marton_transport_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_wasserstein_marton_transport_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "kernel_row_optimal_coupling_record_count": 3,
        "pearson_transport_information_mode_record_count": 2,
        "reference_wasserstein_profile_record_count": 22,
        "reference_pair_wasserstein_profile_record_count": 11,
        "marton_state_pair_profile_record_count": 33,
        "marton_influence_profile_record_count": 11,
        "wasserstein_threshold_record_count": 6,
        "full_rank_transport_wasserstein_marton_record_count": 8,
        "singular_atomic_wasserstein_marton_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    couplings = {
        x["pair_id"]: x for x in obs["kernel_row_optimal_coupling_records"]
    }
    assert couplings["early_middle"]["coupling_cost"] == {
        "numerator": 3,
        "denominator": 4,
    }
    assert couplings["middle_late"]["coupling_cost"] == {
        "numerator": 3,
        "denominator": 4,
    }
    assert couplings["early_late"]["coupling_cost"] == {
        "numerator": 3,
        "denominator": 2,
    }
    assert all(
        x["source_marginal_exact"]
        and x["target_marginal_exact"]
        and x["coupling_cost_exact"]
        and x["optimality_formally_proved"]
        for x in couplings.values()
    )

    modes = {
        x["mode_id"]: x
        for x in obs["pearson_transport_information_mode_records"]
    }
    assert modes["antisymmetric_slow"]["path_wasserstein_one_squared"] == {
        "numerator": 4,
        "denominator": 1,
    }
    assert modes["antisymmetric_slow"][
        "pearson_transport_information_equality"
    ]
    assert modes["symmetric_fast"]["pearson_t1_right_hand_side"] == {
        "numerator": 12,
        "denominator": 1,
    }
    assert not modes["symmetric_fast"][
        "pearson_transport_information_equality"
    ]

    reference = [
        x
        for x in obs["reference_wasserstein_profile_records"]
        if x["distribution_id"] == "reference_p"
    ]
    assert reference[0]["wasserstein_to_stationary"] == {
        "numerator": 3,
        "denominator": 10,
    }
    assert reference[0]["wasserstein_squared"] == {
        "numerator": 9,
        "denominator": 100,
    }
    assert all(
        x["pearson_t1_equality"]
        and x["one_step_wasserstein_contraction_exact"]
        for x in reference
    )

    pair = obs["reference_pair_wasserstein_profile_records"]
    assert pair[0]["reference_p_q_wasserstein"] == {
        "numerator": 3,
        "denominator": 5,
    }
    assert all(x["one_step_contraction_exact"] for x in pair)

    marton = obs["marton_state_pair_profile_records"]
    endpoint = [x for x in marton if x["pair_id"] == "early_late"]
    assert endpoint[0]["iterated_wasserstein_distance"] == {
        "numerator": 2,
        "denominator": 1,
    }
    assert endpoint[8]["iterated_wasserstein_distance"] == {
        "numerator": 6561,
        "denominator": 32768,
    }
    assert all(
        x["exact_geometric_transport_profile"]
        and x["one_step_contraction_exact"]
        for x in marton
    )

    influence = obs["marton_influence_profile_records"]
    assert influence[0]["influence_sum"] == {
        "numerator": 0,
        "denominator": 1,
    }
    assert influence[1]["influence_sum"] == {
        "numerator": 1,
        "denominator": 1,
    }
    assert influence[4]["influence_sum"] == {
        "numerator": 175,
        "denominator": 64,
    }
    assert all(
        x["recursion_exact"]
        and x["strictly_below_four"]
        and x["variance_proxy_exact"]
        for x in influence
    )

    thresholds = {
        x["profile_id"]: x for x in obs["wasserstein_threshold_records"]
    }
    expected_threshold_times = {
        "reference_to_stationary_le_one_tenth": 4,
        "reference_to_stationary_le_one_twentieth": 7,
        "reference_pair_le_one_tenth": 7,
        "reference_pair_le_one_twentieth": 9,
        "adjacent_state_marton_le_one_quarter": 5,
        "endpoint_state_marton_le_one_quarter": 8,
    }
    for profile_id, certified_time in expected_threshold_times.items():
        assert thresholds[profile_id]["certified_time"] == certified_time
        assert thresholds[profile_id]["previous_value_not_sufficient"]
        assert thresholds[profile_id]["certified"]
        assert thresholds[profile_id]["first_certified_time_exact"]

    assert obs["path_metric_wasserstein_formula_exact"]
    assert obs["all_kernel_row_optimal_couplings_exact"]
    assert obs["dobrushin_wasserstein_coefficient_three_quarters_exact"]
    assert obs["coarse_ricci_curvature_quarter_exact"]
    assert obs["pearson_transport_information_constant_two_thirds_exact"]
    assert obs["pearson_transport_information_sharp_on_slow_mode"]
    assert obs["all_reference_wasserstein_profiles_exact"]
    assert obs["reference_pair_wasserstein_profile_exact"]
    assert obs["all_marton_state_pair_profiles_exact"]
    assert obs["all_marton_influence_profiles_exact"]
    assert obs["all_wasserstein_thresholds_exact"]

    assert all(
        x["pearson_transport_information_commutes"]
        and x["wasserstein_contraction_profile_commutes"]
        and x["marton_coupling_profile_commutes"]
        for x in obs["full_rank_transport_wasserstein_marton_records"]
    )
    assert all(
        x["singular_atomic_wasserstein_ledger_retained"]
        and x["singular_atomic_marton_ledger_retained"]
        and not x["two_dimensional_target_density_emitted"]
        for x in obs["singular_atomic_wasserstein_marton_records"]
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v061_certificate"]["observables"][
        "integrated_curvature_mode_records"
    ][0]["chi_square"] = {"numerator": 7, "denominator": 1}
    _resign(tampered["source_memoryos_v061_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v061_integrated_curvature_mode_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"][
        "dobrushin_wasserstein_coefficient_three_quarters_exact"
    ] = False
    assert_rejects(
        tampered,
        "claim_mismatch_dobrushin_wasserstein_coefficient_three_quarters_exact",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["wasserstein_threshold_records"][0][
        "certified_time"
    ] = 3
    assert_rejects(tampered, "claim_mismatch_wasserstein_threshold_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_pruning_performed"] = True
    assert_rejects(tampered, "claim_mismatch_candidate_pruning_performed")

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": result["schema_version"],
                "certificate_digest": result["certificate_digest"],
                "kernel_row_optimal_coupling_digest": obs[
                    "kernel_row_optimal_coupling_digest"
                ],
                "pearson_transport_information_mode_digest": obs[
                    "pearson_transport_information_mode_digest"
                ],
                "reference_wasserstein_profile_digest": obs[
                    "reference_wasserstein_profile_digest"
                ],
                "marton_state_pair_profile_digest": obs[
                    "marton_state_pair_profile_digest"
                ],
                "marton_influence_profile_digest": obs[
                    "marton_influence_profile_digest"
                ],
                "wasserstein_threshold_digest": obs[
                    "wasserstein_threshold_digest"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
