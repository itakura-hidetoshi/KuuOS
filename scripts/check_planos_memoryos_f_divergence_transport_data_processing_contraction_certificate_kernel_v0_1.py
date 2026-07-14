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

from runtime.kuuos_memoryos_quotient_metric_density_transport_radon_nikodym_cocycle_certificate_kernel_v0_1 import (
    issue_quotient_metric_density_transport_radon_nikodym_cocycle_certificate,
)
from runtime.kuuos_memoryos_relative_entropy_transport_lebesgue_decomposition_certificate_kernel_v0_1 import (
    issue_relative_entropy_transport_lebesgue_decomposition_certificate,
)
from runtime.kuuos_memoryos_f_divergence_transport_data_processing_contraction_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_f_divergence_transport_data_processing_contraction_certificate,
)
from scripts.check_planos_memoryos_quotient_metric_density_transport_radon_nikodym_cocycle_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v054_payload,
)
from scripts.check_planos_memoryos_relative_entropy_transport_lebesgue_decomposition_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v055_payload,
)


def source_memoryos_v054_certificate() -> dict[str, Any]:
    result = issue_quotient_metric_density_transport_radon_nikodym_cocycle_certificate(
        build_memoryos_v054_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def source_memoryos_v055_certificate() -> dict[str, Any]:
    result = issue_relative_entropy_transport_lebesgue_decomposition_certificate(
        build_memoryos_v055_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v055 = source_memoryos_v055_certificate()
    source_v054 = source_memoryos_v054_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v055_certificate": source_v055,
        "source_memoryos_v054_certificate": source_v054,
        "claims": _derive_observables(source_v055, source_v054),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def _resign_v055(certificate: dict[str, Any]) -> None:
    observables = certificate["observables"]
    observables["relative_entropy_transport_digest"] = canonical_digest(
        observables["relative_entropy_transport_trajectory"]
    )
    observables["relative_entropy_cocycle_digest"] = canonical_digest(
        observables["relative_entropy_cocycle_records"]
    )
    _resign(certificate)


def _resign_v054(certificate: dict[str, Any]) -> None:
    observables = certificate["observables"]
    observables["quotient_metric_density_transport_digest"] = canonical_digest(
        observables["quotient_metric_density_transport_trajectory"]
    )
    observables["radon_nikodym_cocycle_digest"] = canonical_digest(
        observables["radon_nikodym_cocycle_records"]
    )
    _resign(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_f_divergence_transport_data_processing_contraction_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_f_divergence_transport_data_processing_contraction_certificate(
        payload
    )
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    assert obs["generator_count"] == 3
    assert obs["transition_count"] == 9
    assert obs["full_rank_f_divergence_transition_count"] == 4
    assert obs["full_rank_probe_f_divergence_record_count"] == 108
    assert obs["singular_f_divergence_transition_count"] == 2
    assert obs["singular_atomic_f_divergence_record_count"] == 54
    assert obs["rank_one_source_boundary_count"] == 3
    assert obs["coarse_graining_bin_count"] == 3
    assert obs["deterministic_channel_row_count"] == 9
    assert obs["data_processing_record_count"] == 12
    assert obs["pearson_pairwise_merge_witness_count"] == 6
    assert obs["f_divergence_cocycle_record_count"] == 27
    assert obs["active_f_divergence_cocycle_count"] == 8
    assert obs["nontrivial_round_trip_f_divergence_path_count"] == 2

    assert obs["f_divergence_generator_ids"] == [
        "pearson_chi_square",
        "neyman_chi_square",
        "triangular_discrimination",
    ]
    assert obs["reference_pearson_fine_divergence"] == {
        "numerator": 2593,
        "denominator": 1134,
    }
    assert obs["reference_pearson_coarse_divergence"] == {
        "numerator": 3,
        "denominator": 2,
    }
    assert obs["reference_pearson_contraction_gap"] == {
        "numerator": 446,
        "denominator": 567,
    }
    assert obs["reference_neyman_fine_divergence"] == {
        "numerator": 2593,
        "denominator": 1134,
    }
    assert obs["reference_neyman_coarse_divergence"] == {
        "numerator": 3,
        "denominator": 2,
    }
    assert obs["reference_neyman_contraction_gap"] == {
        "numerator": 446,
        "denominator": 567,
    }
    assert obs["reference_triangular_fine_divergence"] == {
        "numerator": 8,
        "denominator": 15,
    }
    assert obs["reference_triangular_coarse_divergence"] == {
        "numerator": 12,
        "denominator": 25,
    }
    assert obs["reference_triangular_contraction_gap"] == {
        "numerator": 4,
        "denominator": 75,
    }
    assert obs["reference_pearson_pairwise_gap_total"] == {
        "numerator": 446,
        "denominator": 567,
    }

    assert obs["coarse_grained_p_masses"] == {
        "early": {"numerator": 2, "denominator": 15},
        "middle": {"numerator": 1, "denominator": 3},
        "late": {"numerator": 8, "denominator": 15},
    }
    assert obs["coarse_grained_q_masses"] == {
        "early": {"numerator": 8, "denominator": 15},
        "middle": {"numerator": 1, "denominator": 3},
        "late": {"numerator": 2, "denominator": 15},
    }
    assert all(
        item["gap_identity_exact"] and item["gap_nonnegative"]
        for item in obs["pearson_pairwise_merge_records"]
    )

    transitions = obs["f_divergence_transport_trajectory"]
    one_to_zero = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 1
        and item["target_cross_numerator"] == 0
    )
    assert one_to_zero["full_rank_f_divergence_transport_active"] is True
    assert one_to_zero["all_generator_ledgers_invariant"] is True
    assert len(one_to_zero["full_rank_probe_f_divergence_records"]) == 27
    assert all(
        item["f_divergence_contribution_invariant"]
        for item in one_to_zero["full_rank_probe_f_divergence_records"]
    )

    collapse = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 1
        and item["target_cross_numerator"] == 2
    )
    assert collapse["singular_f_divergence_boundary_active"] is True
    assert collapse["singular_atomic_f_divergence_exact"] is True
    assert len(collapse["singular_atomic_f_divergence_records"]) == 27
    assert all(
        item["singular_atomic_f_divergence_retained"]
        and not item["two_dimensional_f_divergence_density_emitted"]
        for item in collapse["singular_atomic_f_divergence_records"]
    )

    boundary = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 2
        and item["target_cross_numerator"] == 1
    )
    assert boundary["rank_one_source_boundary"] is True
    assert boundary[
        "rank_one_source_two_dimensional_f_divergence_recovery_claimed"
    ] is False
    assert all(
        ledger == []
        for ledger in boundary["target_f_divergence_ledgers"].values()
    )

    assert all(
        item["source_data_processing_contraction_exact"]
        and item["target_data_processing_contraction_exact"]
        and item["transport_coarse_graining_commutes"]
        for item in obs["full_rank_data_processing_records"]
    )
    assert all(
        not item["f_divergence_cocycle_active"]
        or item["all_generator_cocycles_exact"]
        for item in obs["f_divergence_cocycle_records"]
    )

    tampered = copy.deepcopy(payload)
    first_probe_id = obs["retained_probe_ids"][0]
    tampered["source_memoryos_v055_certificate"]["observables"][
        "reference_p_probe_masses"
    ][first_probe_id] = {"numerator": 2, "denominator": 45}
    _resign_v055(tampered["source_memoryos_v055_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v055_reference_p_mass_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered_transition = tampered["source_memoryos_v054_certificate"][
        "observables"
    ]["quotient_metric_density_transport_trajectory"][4]
    tampered_transition["radon_nikodym_density_multiplier"] = {
        "numerator": 7,
        "denominator": 5,
    }
    _resign_v054(tampered["source_memoryos_v054_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v054_radon_nikodym_density_multiplier_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["reference_pearson_contraction_gap"] = {
        "numerator": 1,
        "denominator": 1,
    }
    assert_rejects(
        tampered,
        "claim_mismatch_reference_pearson_contraction_gap",
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
                "f_divergence_transport_digest": obs[
                    "f_divergence_transport_digest"
                ],
                "data_processing_digest": obs[
                    "data_processing_digest"
                ],
                "f_divergence_cocycle_digest": obs[
                    "f_divergence_cocycle_digest"
                ],
                "generator_count": obs["generator_count"],
                "full_rank_probe_f_divergence_record_count": obs[
                    "full_rank_probe_f_divergence_record_count"
                ],
                "data_processing_record_count": obs[
                    "data_processing_record_count"
                ],
                "pearson_pairwise_merge_witness_count": obs[
                    "pearson_pairwise_merge_witness_count"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
