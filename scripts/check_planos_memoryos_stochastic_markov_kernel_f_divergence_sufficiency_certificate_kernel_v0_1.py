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

from runtime.kuuos_memoryos_relative_entropy_transport_lebesgue_decomposition_certificate_kernel_v0_1 import (
    issue_relative_entropy_transport_lebesgue_decomposition_certificate,
)
from runtime.kuuos_memoryos_f_divergence_transport_data_processing_contraction_certificate_kernel_v0_1 import (
    issue_f_divergence_transport_data_processing_contraction_certificate,
)
from runtime.kuuos_memoryos_stochastic_markov_kernel_f_divergence_sufficiency_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_stochastic_markov_kernel_f_divergence_sufficiency_certificate,
)
from scripts.check_planos_memoryos_relative_entropy_transport_lebesgue_decomposition_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v055_payload,
)
from scripts.check_planos_memoryos_f_divergence_transport_data_processing_contraction_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v056_payload,
)


def source_memoryos_v055_certificate() -> dict[str, Any]:
    result = issue_relative_entropy_transport_lebesgue_decomposition_certificate(
        build_memoryos_v055_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def source_memoryos_v056_certificate() -> dict[str, Any]:
    result = issue_f_divergence_transport_data_processing_contraction_certificate(
        build_memoryos_v056_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v056 = source_memoryos_v056_certificate()
    source_v055 = source_memoryos_v055_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v056_certificate": source_v056,
        "source_memoryos_v055_certificate": source_v055,
        "claims": _derive_observables(source_v056, source_v055),
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


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_stochastic_markov_kernel_f_divergence_sufficiency_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_stochastic_markov_kernel_f_divergence_sufficiency_certificate(
        payload
    )
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    assert obs["stochastic_kernel_row_count"] == 9
    assert obs["stochastic_kernel_entry_count"] == 27
    assert obs["stochastic_output_count"] == 3
    assert obs["stochastic_data_processing_record_count"] == 3
    assert obs["tagged_split_channel_entry_count"] == 18
    assert obs["tagged_split_output_count"] == 18
    assert obs["recovery_kernel_entry_count"] == 18
    assert obs["sufficient_probe_generator_record_count"] == 27
    assert obs["sufficient_generator_equality_record_count"] == 3
    assert obs[
        "full_rank_transport_markov_sufficiency_record_count"
    ] == 12
    assert obs["singular_stochastic_f_divergence_record_count"] == 6
    assert obs["rank_one_source_boundary_count"] == 3

    assert obs["stochastic_output_p_masses"] == {
        "early": {"numerator": 11, "denominator": 60},
        "middle": {"numerator": 1, "denominator": 3},
        "late": {"numerator": 29, "denominator": 60},
    }
    assert obs["stochastic_output_q_masses"] == {
        "early": {"numerator": 29, "denominator": 60},
        "middle": {"numerator": 1, "denominator": 3},
        "late": {"numerator": 11, "denominator": 60},
    }

    reference = {
        item["generator_id"]: item
        for item in obs["stochastic_reference_data_processing_records"]
    }
    assert reference["pearson_chi_square"][
        "stochastic_divergence_total"
    ] == {"numerator": 216, "denominator": 319}
    assert reference["pearson_chi_square"][
        "fine_to_stochastic_contraction_gap"
    ] == {"numerator": 582223, "denominator": 361746}
    assert reference["pearson_chi_square"][
        "coarse_to_stochastic_contraction_gap"
    ] == {"numerator": 525, "denominator": 638}
    assert reference["neyman_chi_square"][
        "stochastic_divergence_total"
    ] == {"numerator": 216, "denominator": 319}
    assert reference["triangular_discrimination"][
        "stochastic_divergence_total"
    ] == {"numerator": 27, "denominator": 100}
    assert reference["triangular_discrimination"][
        "fine_to_stochastic_contraction_gap"
    ] == {"numerator": 79, "denominator": 300}
    assert reference["triangular_discrimination"][
        "coarse_to_stochastic_contraction_gap"
    ] == {"numerator": 21, "denominator": 100}
    assert all(
        item["stochastic_strictly_less_than_fine"]
        and item[
            "stochastic_strictly_less_than_deterministic_coarse"
        ]
        for item in reference.values()
    )

    assert obs["reference_stochastic_kernel_sufficient"] is False
    assert obs["reference_stochastic_kernel_not_sufficient"] is True
    assert obs["explicit_recovery_kernel_exact"] is True
    assert obs["recovered_p_masses"] == {
        probe_id: payload["source_memoryos_v055_certificate"][
            "observables"
        ]["reference_p_probe_masses"][probe_id]
        for probe_id in obs["retained_probe_ids"]
    }
    assert obs["recovered_q_masses"] == {
        probe_id: payload["source_memoryos_v055_certificate"][
            "observables"
        ]["reference_q_probe_masses"][probe_id]
        for probe_id in obs["retained_probe_ids"]
    }
    assert all(
        item["split_equality_exact"]
        and item["recovery_equality_exact"]
        for item in obs["sufficient_probe_generator_records"]
    )
    assert all(
        item["explicit_sufficiency_equality_exact"]
        for item in obs["sufficient_generator_equality_records"]
    )
    assert all(
        item["stochastic_transport_invariant"]
        and item["sufficient_split_transport_invariant"]
        and item["transport_stochastic_channel_commutes"]
        and item["transport_sufficiency_channel_commutes"]
        for item in obs[
            "full_rank_transport_markov_sufficiency_records"
        ]
    )
    assert all(
        item["singular_atomic_stochastic_processing_retained"]
        and not item["two_dimensional_target_density_emitted"]
        for item in obs["singular_stochastic_f_divergence_records"]
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v056_certificate"]["observables"][
        "f_divergence_generator_reference_records"
    ][0]["coarse_divergence_total"] = {
        "numerator": 7,
        "denominator": 5,
    }
    _resign(tampered["source_memoryos_v056_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v056_pearson_chi_square_coarse_mismatch",
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
    tampered["claims"]["stochastic_output_p_masses"]["early"] = {
        "numerator": 1,
        "denominator": 2,
    }
    assert_rejects(
        tampered,
        "claim_mismatch_stochastic_output_p_masses",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["reference_stochastic_kernel_sufficient"] = True
    assert_rejects(
        tampered,
        "claim_mismatch_reference_stochastic_kernel_sufficient",
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
                "stochastic_markov_kernel_digest": obs[
                    "stochastic_markov_kernel_digest"
                ],
                "stochastic_reference_data_processing_digest": obs[
                    "stochastic_reference_data_processing_digest"
                ],
                "tagged_split_channel_digest": obs[
                    "tagged_split_channel_digest"
                ],
                "recovery_kernel_digest": obs[
                    "recovery_kernel_digest"
                ],
                "full_rank_transport_markov_sufficiency_digest": obs[
                    "full_rank_transport_markov_sufficiency_digest"
                ],
                "stochastic_data_processing_record_count": obs[
                    "stochastic_data_processing_record_count"
                ],
                "sufficient_probe_generator_record_count": obs[
                    "sufficient_probe_generator_record_count"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
