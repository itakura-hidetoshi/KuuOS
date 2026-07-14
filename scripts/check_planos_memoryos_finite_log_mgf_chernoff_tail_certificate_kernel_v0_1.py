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

from runtime.kuuos_memoryos_kantorovich_lipschitz_mgf_certificate_kernel_v0_1 import (
    issue_kantorovich_lipschitz_mgf_certificate,
)
from runtime.kuuos_memoryos_finite_log_mgf_chernoff_tail_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_finite_log_mgf_chernoff_tail_certificate,
)
from scripts.check_planos_memoryos_kantorovich_lipschitz_mgf_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v063_payload,
)


def source_memoryos_v063_certificate() -> dict[str, Any]:
    result = issue_kantorovich_lipschitz_mgf_certificate(
        build_memoryos_v063_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v063 = source_memoryos_v063_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v063_certificate": source_v063,
        "claims": _derive_observables(source_v063),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_finite_log_mgf_chernoff_tail_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_finite_log_mgf_chernoff_tail_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "finite_log_mgf_record_count": 22,
        "finite_chernoff_transform_record_count": 44,
        "exact_tail_extinction_threshold_record_count": 4,
        "marton_chernoff_tail_input_record_count": 22,
        "full_rank_transport_log_mgf_chernoff_tail_record_count": 8,
        "singular_atomic_log_mgf_chernoff_tail_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    log_mgf = {
        (record["observable_id"], record["horizon"]): record
        for record in obs["finite_log_mgf_records"]
    }
    assert log_mgf[("slow", 0)]["centered_exponents"] == [
        {"numerator": 1, "denominator": 1},
        {"numerator": 0, "denominator": 1},
        {"numerator": -1, "denominator": 1},
    ]
    assert log_mgf[("fast", 2)]["centered_exponents"] == [
        {"numerator": 1, "denominator": 16},
        {"numerator": 1, "denominator": 16},
        {"numerator": -1, "denominator": 8},
    ]
    assert all(
        record["mgf_strictly_positive_formally_proved"]
        and record["exp_log_mgf_identity_formally_proved"]
        and record["log_mgf_zero_exact"]
        and not record["numeric_transcendental_approximation_used"]
        for record in log_mgf.values()
    )

    chernoff = {
        (record["observable_id"], record["horizon"], record["threshold_id"]): record
        for record in obs["finite_chernoff_transform_records"]
    }
    assert chernoff[("slow", 2, "half")]["exact_upper_tail_mass"] == {
        "numerator": 1,
        "denominator": 3,
    }
    assert chernoff[("slow", 3, "half")]["exact_upper_tail_mass"] == {
        "numerator": 0,
        "denominator": 1,
    }
    assert chernoff[("fast", 1, "quarter")]["exact_upper_tail_mass"] == {
        "numerator": 2,
        "denominator": 3,
    }
    assert chernoff[("fast", 2, "quarter")]["exact_upper_tail_mass"] == {
        "numerator": 0,
        "denominator": 1,
    }
    assert all(
        record["tail_mass_enumerated_exactly"]
        and record["chernoff_domination_formally_proved_for_all_nonnegative_lambda"]
        and record["exp_chernoff_transform_identity_formally_proved"]
        and not record["numeric_transcendental_approximation_used"]
        and not record["general_large_deviation_principle_claimed"]
        for record in chernoff.values()
    )

    thresholds = {
        record["record_id"]: record
        for record in obs["exact_tail_extinction_threshold_records"]
    }
    expected_thresholds = {
        "slow_half_tail_extinction": (2, 3),
        "slow_quarter_tail_extinction": (4, 5),
        "fast_half_tail_extinction": (0, 1),
        "fast_quarter_tail_extinction": (1, 2),
    }
    for record_id, (previous_horizon, certified_horizon) in expected_thresholds.items():
        record = thresholds[record_id]
        assert record["previous_horizon"] == previous_horizon
        assert record["certified_horizon"] == certified_horizon
        assert record["previous_tail_nonzero"]
        assert record["certified_tail_extinct"]
        assert record["all_earlier_tails_nonzero"]
        assert record["first_extinction_horizon_exact"]

    marton = obs["marton_chernoff_tail_input_records"]
    assert len(marton) == 22
    assert all(
        record["finite_chernoff_tail_input_retained"]
        and not record["path_space_gaussian_theorem_claimed"]
        and not record["general_large_deviation_principle_claimed"]
        for record in marton
    )

    assert obs["finite_log_mgf_profiles_exact"]
    assert obs["finite_chernoff_transform_profiles_exact"]
    assert obs["all_exact_tail_extinction_thresholds_exact"]
    assert obs["marton_chernoff_tail_inputs_exact"]
    assert obs["general_large_deviation_principle_not_claimed"]
    assert obs["general_path_space_gaussian_theorem_not_claimed"]

    assert all(
        record["finite_log_mgf_commutes"]
        and record["chernoff_transform_commutes"]
        and record["exact_tail_threshold_commutes"]
        for record in obs["full_rank_transport_log_mgf_chernoff_tail_records"]
    )
    assert all(
        record["atomic_log_mgf_terms_retained"]
        and record["atomic_chernoff_terms_retained"]
        and record["atomic_tail_threshold_retained"]
        and not record["two_dimensional_target_density_emitted"]
        and not record["lost_coordinate_reconstructed"]
        for record in obs["singular_atomic_log_mgf_chernoff_tail_records"]
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v063_certificate"]["observables"][
        "finite_symbolic_mgf_records"
    ][0]["second_moment"] = {"numerator": 7, "denominator": 1}
    _resign(tampered["source_memoryos_v063_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v063_finite_symbolic_mgf_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["exact_tail_extinction_threshold_records"][0][
        "certified_horizon"
    ] = 2
    assert_rejects(
        tampered,
        "claim_mismatch_exact_tail_extinction_threshold_records",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["general_large_deviation_principle_not_claimed"] = False
    assert_rejects(
        tampered,
        "claim_mismatch_general_large_deviation_principle_not_claimed",
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
                "finite_log_mgf_digest": obs["finite_log_mgf_digest"],
                "finite_chernoff_transform_digest": obs[
                    "finite_chernoff_transform_digest"
                ],
                "exact_tail_extinction_threshold_digest": obs[
                    "exact_tail_extinction_threshold_digest"
                ],
                "marton_chernoff_tail_input_digest": obs[
                    "marton_chernoff_tail_input_digest"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
