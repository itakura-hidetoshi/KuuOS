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

from runtime.kuuos_memoryos_stochastic_markov_kernel_f_divergence_sufficiency_certificate_kernel_v0_1 import (
    issue_stochastic_markov_kernel_f_divergence_sufficiency_certificate,
)
from runtime.kuuos_memoryos_reversible_markov_semigroup_entropy_production_certificate_kernel_v0_1 import (
    issue_reversible_markov_semigroup_entropy_production_certificate,
)
from runtime.kuuos_memoryos_log_sobolev_hypercontractive_mixing_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_log_sobolev_hypercontractive_mixing_certificate,
)
from scripts.check_planos_memoryos_stochastic_markov_kernel_f_divergence_sufficiency_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v057_payload,
)
from scripts.check_planos_memoryos_reversible_markov_semigroup_entropy_production_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v058_payload,
)


def source_memoryos_v057_certificate() -> dict[str, Any]:
    result = issue_stochastic_markov_kernel_f_divergence_sufficiency_certificate(
        build_memoryos_v057_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def source_memoryos_v058_certificate() -> dict[str, Any]:
    result = issue_reversible_markov_semigroup_entropy_production_certificate(
        build_memoryos_v058_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v058 = source_memoryos_v058_certificate()
    source_v057 = source_memoryos_v057_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v058_certificate": source_v058,
        "source_memoryos_v057_certificate": source_v057,
        "claims": _derive_observables(source_v058, source_v057),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_log_sobolev_hypercontractive_mixing_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_log_sobolev_hypercontractive_mixing_certificate(
        payload
    )
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    assert obs["log_sobolev_record_count"] == 1
    assert obs["reference_kl_envelope_record_count"] == 10
    assert obs["hypercontractive_schedule_record_count"] == 2
    assert obs["reference_total_variation_record_count"] == 10
    assert obs["worst_case_mixing_record_count"] == 9
    assert obs["mixing_threshold_record_count"] == 3
    assert (
        obs["full_rank_transport_log_sobolev_mixing_record_count"]
        == 8
    )
    assert obs["singular_atomic_log_sobolev_mixing_record_count"] == 4
    assert obs["rank_one_source_boundary_count"] == 3

    assert obs["log_sobolev_constant"] == {
        "numerator": 4,
        "denominator": 1,
    }
    mode = obs["log_sobolev_mode_record"]
    assert mode["chi_square_slow_coefficient"] == {
        "numerator": 6,
        "denominator": 1,
    }
    assert mode["chi_square_fast_coefficient"] == {
        "numerator": 18,
        "denominator": 1,
    }
    assert mode["dirichlet_slow_coefficient"] == {
        "numerator": 3,
        "denominator": 2,
    }
    assert mode["dirichlet_fast_coefficient"] == {
        "numerator": 27,
        "denominator": 2,
    }
    assert mode[
        "four_dirichlet_minus_chi_square_fast_coefficient"
    ] == {"numerator": 36, "denominator": 1}

    schedules = {
        item["schedule_id"]: item
        for item in obs["hypercontractive_schedule_records"]
    }
    assert schedules["one_step_centered_l2_to_l4"][
        "envelope_coefficient"
    ] == {"numerator": 243, "denominator": 256}
    assert schedules["two_step_centered_l2_to_linf"][
        "envelope_coefficient"
    ] == {"numerator": 243, "denominator": 256}
    assert all(
        item["hypercontractive_exact"]
        and item["coefficient_strictly_less_than_one"]
        for item in schedules.values()
    )

    expected_tv = [
        {"numerator": 3, "denominator": 20},
        {"numerator": 9, "denominator": 80},
        {"numerator": 27, "denominator": 320},
        {"numerator": 81, "denominator": 1280},
        {"numerator": 243, "denominator": 5120},
    ]
    for distribution_id in ("reference_p", "reference_q"):
        records = [
            item
            for item in obs["reference_total_variation_records"]
            if item["distribution_id"] == distribution_id
        ]
        assert [
            item["total_variation_to_uniform"] for item in records
        ] == expected_tv
        assert all(
            item["tv_squared_le_chi_square_quarter"]
            for item in records
        )

    mixing = obs["worst_case_mixing_records"]
    assert mixing[0]["worst_case_total_variation_squared_bound"] == {
        "numerator": 1,
        "denominator": 2,
    }
    assert mixing[4]["worst_case_total_variation_squared_bound"] == {
        "numerator": 6561,
        "denominator": 131072,
    }
    thresholds = {
        item["threshold_id"]: item
        for item in obs["mixing_threshold_records"]
    }
    assert thresholds["worst_case_tv_le_one_quarter"][
        "certified_time"
    ] == 4
    assert thresholds["worst_case_tv_le_one_eighth"][
        "certified_time"
    ] == 7
    assert thresholds["reference_tv_le_one_twentieth"][
        "certified_time"
    ] == 4
    assert all(
        item["certified"] and item["previous_bound_not_sufficient"]
        for item in thresholds.values()
    )

    assert all(
        item["all_likelihood_ratios_positive"]
        and item["mass_normalized"]
        and item["kl_le_chi_square_formally_bound"]
        and item["kl_le_four_dirichlet_formally_bound"]
        for item in obs["reference_kl_envelope_records"]
    )
    assert all(
        item["log_sobolev_transport_commutes"]
        and item["hypercontractive_envelope_transport_commutes"]
        and item["mixing_bound_transport_commutes"]
        for item in obs[
            "full_rank_transport_log_sobolev_mixing_records"
        ]
    )
    assert all(
        item["singular_atomic_log_sobolev_envelope_retained"]
        and item["singular_atomic_mixing_ledger_retained"]
        and not item["two_dimensional_target_density_emitted"]
        for item in obs[
            "singular_atomic_log_sobolev_mixing_records"
        ]
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v058_certificate"]["observables"][
        "entropy_trajectory_records"
    ][0]["trajectory"][0]["masses"]["early"] = {
        "numerator": 1,
        "denominator": 3,
    }
    _resign(tampered["source_memoryos_v058_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v058_entropy_trajectory_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v057_certificate"]["observables"][
        "stochastic_output_p_masses"
    ]["early"] = {"numerator": 1, "denominator": 2}
    _resign(tampered["source_memoryos_v057_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v057_reference_p_output_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["log_sobolev_constant"] = {
        "numerator": 3,
        "denominator": 1,
    }
    assert_rejects(
        tampered,
        "claim_mismatch_log_sobolev_constant",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["mixing_threshold_records"][0][
        "certified_time"
    ] = 3
    assert_rejects(
        tampered,
        "claim_mismatch_mixing_threshold_records",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_pruning_performed"] = True
    assert_rejects(
        tampered,
        "claim_mismatch_candidate_pruning_performed",
    )

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": result["schema_version"],
                "certificate_digest": result["certificate_digest"],
                "log_sobolev_mode_digest": obs[
                    "log_sobolev_mode_digest"
                ],
                "reference_kl_envelope_digest": obs[
                    "reference_kl_envelope_digest"
                ],
                "hypercontractive_schedule_digest": obs[
                    "hypercontractive_schedule_digest"
                ],
                "worst_case_mixing_digest": obs[
                    "worst_case_mixing_digest"
                ],
                "mixing_threshold_digest": obs[
                    "mixing_threshold_digest"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
