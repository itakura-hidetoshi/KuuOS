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

from runtime.kuuos_memoryos_f_divergence_transport_data_processing_contraction_certificate_kernel_v0_1 import (
    issue_f_divergence_transport_data_processing_contraction_certificate,
)
from runtime.kuuos_memoryos_stochastic_markov_kernel_f_divergence_sufficiency_certificate_kernel_v0_1 import (
    issue_stochastic_markov_kernel_f_divergence_sufficiency_certificate,
)
from runtime.kuuos_memoryos_reversible_markov_semigroup_entropy_production_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_reversible_markov_semigroup_entropy_production_certificate,
)
from scripts.check_planos_memoryos_f_divergence_transport_data_processing_contraction_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v056_payload,
)
from scripts.check_planos_memoryos_stochastic_markov_kernel_f_divergence_sufficiency_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v057_payload,
)


def source_memoryos_v056_certificate() -> dict[str, Any]:
    result = issue_f_divergence_transport_data_processing_contraction_certificate(
        build_memoryos_v056_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def source_memoryos_v057_certificate() -> dict[str, Any]:
    result = issue_stochastic_markov_kernel_f_divergence_sufficiency_certificate(
        build_memoryos_v057_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v057 = source_memoryos_v057_certificate()
    source_v056 = source_memoryos_v056_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v057_certificate": source_v057,
        "source_memoryos_v056_certificate": source_v056,
        "claims": _derive_observables(source_v057, source_v056),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_reversible_markov_semigroup_entropy_production_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_reversible_markov_semigroup_entropy_production_certificate(
        payload
    )
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    assert obs["kernel_state_count"] == 3
    assert obs["kernel_entry_count"] == 9
    assert obs["kernel_power_record_count"] == 5
    assert obs["semigroup_composition_record_count"] == 9
    assert obs["detailed_balance_record_count"] == 9
    assert obs["eigenmode_record_count"] == 3
    assert obs["entropy_trajectory_record_count"] == 2
    assert obs["entropy_timepoint_record_count"] == 10
    assert obs["entropy_production_record_count"] == 8
    assert obs["full_rank_transport_semigroup_record_count"] == 8
    assert obs["singular_atomic_entropy_record_count"] == 4
    assert obs["rank_one_source_boundary_count"] == 3

    assert obs["uniform_stationary_distribution"] == {
        "early": {"numerator": 1, "denominator": 3},
        "middle": {"numerator": 1, "denominator": 3},
        "late": {"numerator": 1, "denominator": 3},
    }
    assert obs["uniform_stationary_pushforward"] == obs[
        "uniform_stationary_distribution"
    ]
    assert obs["spectral_gap"] == {
        "numerator": 1,
        "denominator": 4,
    }
    assert obs["strong_data_processing_coefficient"] == {
        "numerator": 9,
        "denominator": 16,
    }

    powers = obs["kernel_power_records"]
    assert powers[0]["kernel_power"] == [
        [
            {"numerator": 1, "denominator": 1},
            {"numerator": 0, "denominator": 1},
            {"numerator": 0, "denominator": 1},
        ],
        [
            {"numerator": 0, "denominator": 1},
            {"numerator": 1, "denominator": 1},
            {"numerator": 0, "denominator": 1},
        ],
        [
            {"numerator": 0, "denominator": 1},
            {"numerator": 0, "denominator": 1},
            {"numerator": 1, "denominator": 1},
        ],
    ]
    assert powers[2]["kernel_power"] == [
        [
            {"numerator": 5, "denominator": 8},
            {"numerator": 5, "denominator": 16},
            {"numerator": 1, "denominator": 16},
        ],
        [
            {"numerator": 5, "denominator": 16},
            {"numerator": 3, "denominator": 8},
            {"numerator": 5, "denominator": 16},
        ],
        [
            {"numerator": 1, "denominator": 16},
            {"numerator": 5, "denominator": 16},
            {"numerator": 5, "denominator": 8},
        ],
    ]
    assert all(item["row_stochastic"] for item in powers)
    assert all(item["column_stochastic"] for item in powers)
    assert all(
        item["semigroup_composition_exact"]
        for item in obs["semigroup_composition_records"]
    )
    assert all(
        item["detailed_balance_exact"]
        for item in obs["detailed_balance_records"]
    )

    eigenmodes = {
        item["mode_id"]: item for item in obs["eigenmode_records"]
    }
    assert eigenmodes["stationary"]["eigenvalue"] == {
        "numerator": 1,
        "denominator": 1,
    }
    assert eigenmodes["antisymmetric_slow"]["eigenvalue"] == {
        "numerator": 3,
        "denominator": 4,
    }
    assert eigenmodes["curvature_fast"]["eigenvalue"] == {
        "numerator": 1,
        "denominator": 4,
    }
    assert all(item["eigenmode_exact"] for item in eigenmodes.values())

    expected_entropies = [
        {"numerator": 27, "denominator": 200},
        {"numerator": 243, "denominator": 3200},
        {"numerator": 2187, "denominator": 51200},
        {"numerator": 19683, "denominator": 819200},
        {"numerator": 177147, "denominator": 13107200},
    ]
    for trajectory_record in obs["entropy_trajectory_records"]:
        trajectory = trajectory_record["trajectory"]
        assert [
            item["chi_square_entropy_to_uniform"] for item in trajectory
        ] == expected_entropies
        assert all(item["entropy_exact"] for item in trajectory)
        assert all(item["sdpi_bound_exact"] for item in trajectory)

    expected_productions = [
        {"numerator": 189, "denominator": 3200},
        {"numerator": 1701, "denominator": 51200},
        {"numerator": 15309, "denominator": 819200},
        {"numerator": 137781, "denominator": 13107200},
    ]
    for distribution_id in ("reference_p", "reference_q"):
        records = [
            item
            for item in obs["entropy_production_records"]
            if item["distribution_id"] == distribution_id
        ]
        assert [item["entropy_production"] for item in records] == (
            expected_productions
        )
        assert all(item["entropy_production_nonnegative"] for item in records)
        assert all(item["one_step_sdpi_equality"] for item in records)

    mode_record = obs["mode_entropy_dissipation_record"]
    assert mode_record["slow_mode_entropy_production_coefficient"] == {
        "numerator": 21,
        "denominator": 8,
    }
    assert mode_record["fast_mode_entropy_production_coefficient"] == {
        "numerator": 135,
        "denominator": 8,
    }
    assert mode_record["strong_data_processing_coefficient_sharp"] is True

    assert all(
        item["transport_semigroup_commutes"]
        and item["transport_entropy_production_commutes"]
        for item in obs["full_rank_transport_semigroup_records"]
    )
    assert all(
        item["singular_atomic_entropy_retained"]
        and not item["two_dimensional_target_density_emitted"]
        for item in obs["singular_atomic_entropy_records"]
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
    tampered["source_memoryos_v056_certificate"]["observables"][
        "retained_history_ids"
    ][0] = "tampered-history"
    _resign(tampered["source_memoryos_v056_certificate"])
    assert_rejects(
        tampered,
        "source_v057_v056_certificate_binding_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["strong_data_processing_coefficient"] = {
        "numerator": 1,
        "denominator": 2,
    }
    assert_rejects(
        tampered,
        "claim_mismatch_strong_data_processing_coefficient",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["all_detailed_balance_fluxes_exact"] = False
    assert_rejects(
        tampered,
        "claim_mismatch_all_detailed_balance_fluxes_exact",
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
                "reference_kernel_digest": obs["reference_kernel_digest"],
                "kernel_power_digest": obs["kernel_power_digest"],
                "semigroup_composition_digest": obs[
                    "semigroup_composition_digest"
                ],
                "detailed_balance_digest": obs[
                    "detailed_balance_digest"
                ],
                "entropy_trajectory_digest": obs[
                    "entropy_trajectory_digest"
                ],
                "entropy_production_digest": obs[
                    "entropy_production_digest"
                ],
                "strong_data_processing_coefficient": obs[
                    "strong_data_processing_coefficient"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
