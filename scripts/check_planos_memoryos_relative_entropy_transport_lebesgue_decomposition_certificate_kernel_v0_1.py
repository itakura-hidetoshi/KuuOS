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

from runtime.kuuos_memoryos_quotient_transport_jacobian_volume_stratification_certificate_kernel_v0_1 import (
    issue_quotient_transport_jacobian_volume_stratification_certificate,
)
from runtime.kuuos_memoryos_quotient_metric_density_transport_radon_nikodym_cocycle_certificate_kernel_v0_1 import (
    issue_quotient_metric_density_transport_radon_nikodym_cocycle_certificate,
)
from runtime.kuuos_memoryos_relative_entropy_transport_lebesgue_decomposition_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_relative_entropy_transport_lebesgue_decomposition_certificate,
)
from scripts.check_planos_memoryos_quotient_transport_jacobian_volume_stratification_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v053_payload,
)
from scripts.check_planos_memoryos_quotient_metric_density_transport_radon_nikodym_cocycle_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v054_payload,
)


def source_memoryos_v053_certificate() -> dict[str, Any]:
    result = issue_quotient_transport_jacobian_volume_stratification_certificate(
        build_memoryos_v053_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def source_memoryos_v054_certificate() -> dict[str, Any]:
    result = issue_quotient_metric_density_transport_radon_nikodym_cocycle_certificate(
        build_memoryos_v054_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v054 = source_memoryos_v054_certificate()
    source_v053 = source_memoryos_v053_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v054_certificate": source_v054,
        "source_memoryos_v053_certificate": source_v053,
        "claims": _derive_observables(source_v054, source_v053),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def _resign_v054(certificate: dict[str, Any]) -> None:
    observables = certificate["observables"]
    observables[
        "quotient_metric_density_transport_digest"
    ] = canonical_digest(
        observables["quotient_metric_density_transport_trajectory"]
    )
    observables["radon_nikodym_cocycle_digest"] = canonical_digest(
        observables["radon_nikodym_cocycle_records"]
    )
    _resign(certificate)


def _resign_v053(certificate: dict[str, Any]) -> None:
    observables = certificate["observables"]
    observables["quotient_transport_jacobian_digest"] = canonical_digest(
        observables["quotient_transport_jacobian_trajectory"]
    )
    observables[
        "quotient_transport_mode_composition_digest"
    ] = canonical_digest(
        observables["quotient_transport_mode_composition_records"]
    )
    _resign(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_relative_entropy_transport_lebesgue_decomposition_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_relative_entropy_transport_lebesgue_decomposition_certificate(
        payload
    )
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    assert obs["transition_count"] == 9
    assert obs["full_rank_relative_entropy_transition_count"] == 4
    assert obs["full_rank_probe_relative_entropy_record_count"] == 36
    assert obs["singular_lebesgue_decomposition_transition_count"] == 2
    assert obs[
        "singular_probe_lebesgue_decomposition_record_count"
    ] == 18
    assert obs["singular_atomic_relative_entropy_record_count"] == 18
    assert obs["rank_one_source_boundary_count"] == 3
    assert obs["relative_entropy_cocycle_record_count"] == 27
    assert obs["active_relative_entropy_cocycle_count"] == 8
    assert obs[
        "nontrivial_round_trip_relative_entropy_path_count"
    ] == 2

    assert obs["reference_p_mass_total"] == {
        "numerator": 1,
        "denominator": 1,
    }
    assert obs["reference_q_mass_total"] == {
        "numerator": 1,
        "denominator": 1,
    }
    assert obs["reference_first_probe_likelihood_ratio"] == {
        "numerator": 1,
        "denominator": 9,
    }
    assert obs["reference_middle_probe_likelihood_ratio"] == {
        "numerator": 1,
        "denominator": 1,
    }
    assert obs["reference_last_probe_likelihood_ratio"] == {
        "numerator": 9,
        "denominator": 1,
    }

    transitions = obs["relative_entropy_transport_trajectory"]
    one_to_zero = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 1
        and item["target_cross_numerator"] == 0
    )
    assert one_to_zero[
        "full_rank_relative_entropy_transport_active"
    ] is True
    assert one_to_zero[
        "full_rank_relative_entropy_ledger_invariant"
    ] is True
    assert len(
        one_to_zero["full_rank_probe_relative_entropy_records"]
    ) == 9
    assert all(
        item["likelihood_ratio_invariant"]
        and item["reverse_likelihood_ratio_invariant"]
        and item["p_mass_preserved"]
        and item["q_mass_preserved"]
        and item["relative_entropy_term_invariant"]
        and item["reverse_relative_entropy_term_invariant"]
        for item in one_to_zero[
            "full_rank_probe_relative_entropy_records"
        ]
    )

    collapse = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 1
        and item["target_cross_numerator"] == 2
    )
    assert collapse["singular_lebesgue_decomposition_active"] is True
    assert collapse["singular_lebesgue_decomposition_exact"] is True
    assert len(
        collapse["singular_probe_lebesgue_decomposition_records"]
    ) == 9
    assert all(
        item["p_absolutely_continuous_mass"]
        == {"numerator": 0, "denominator": 1}
        and item["q_absolutely_continuous_mass"]
        == {"numerator": 0, "denominator": 1}
        and item["p_lebesgue_decomposition_exact"]
        and item["q_lebesgue_decomposition_exact"]
        and item["singular_atomic_relative_entropy_retained"]
        and not item[
            "two_dimensional_relative_entropy_density_emitted"
        ]
        for item in collapse[
            "singular_probe_lebesgue_decomposition_records"
        ]
    )

    rank_one_source = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 2
        and item["target_cross_numerator"] == 1
    )
    assert rank_one_source["rank_one_source_boundary"] is True
    assert rank_one_source[
        "rank_one_source_two_dimensional_kl_recovery_claimed"
    ] is False
    assert rank_one_source[
        "target_relative_entropy_symbolic_ledger"
    ] == []

    cocycles = obs["relative_entropy_cocycle_records"]
    assert all(
        not item["relative_entropy_cocycle_active"]
        or (
            item["relative_entropy_cocycle_exact"]
            and item["reverse_relative_entropy_cocycle_exact"]
        )
        for item in cocycles
    )
    assert sum(
        item[
            "nontrivial_round_trip_relative_entropy_preserved"
        ]
        for item in cocycles
    ) == 2

    tampered = copy.deepcopy(payload)
    active_transition = tampered[
        "source_memoryos_v054_certificate"
    ]["observables"]["quotient_metric_density_transport_trajectory"][4]
    active_transition["radon_nikodym_density_multiplier"] = {
        "numerator": 7,
        "denominator": 5,
    }
    _resign_v054(
        tampered["source_memoryos_v054_certificate"]
    )
    assert_rejects(
        tampered,
        "source_memoryos_v054_radon_nikodym_density_multiplier_mismatch",
    )

    tampered = copy.deepcopy(payload)
    singular_transition = tampered[
        "source_memoryos_v054_certificate"
    ]["observables"]["quotient_metric_density_transport_trajectory"][3]
    singular_transition[
        "singular_probe_pushforward_records"
    ][0]["two_dimensional_target_density_emitted"] = True
    _resign_v054(
        tampered["source_memoryos_v054_certificate"]
    )
    assert_rejects(
        tampered,
        "source_memoryos_v054_singular_probe_witness_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered_jacobian = tampered[
        "source_memoryos_v053_certificate"
    ]["observables"]["quotient_transport_jacobian_trajectory"][4]
    tampered_jacobian["normalized_jacobian"] = {
        "numerator": 5,
        "denominator": 7,
    }
    _resign_v053(
        tampered["source_memoryos_v053_certificate"]
    )
    assert_rejects(
        tampered,
        "source_memoryos_v053_normalized_jacobian_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"][
        "singular_atomic_relative_entropy_retained"
    ] = False
    assert_rejects(
        tampered,
        "claim_mismatch_singular_atomic_relative_entropy_retained",
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
                "relative_entropy_transport_digest": obs[
                    "relative_entropy_transport_digest"
                ],
                "relative_entropy_cocycle_digest": obs[
                    "relative_entropy_cocycle_digest"
                ],
                "transition_count": obs["transition_count"],
                "full_rank_relative_entropy_transition_count": obs[
                    "full_rank_relative_entropy_transition_count"
                ],
                "full_rank_probe_relative_entropy_record_count": obs[
                    "full_rank_probe_relative_entropy_record_count"
                ],
                "singular_lebesgue_decomposition_transition_count": obs[
                    "singular_lebesgue_decomposition_transition_count"
                ],
                "active_relative_entropy_cocycle_count": obs[
                    "active_relative_entropy_cocycle_count"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
