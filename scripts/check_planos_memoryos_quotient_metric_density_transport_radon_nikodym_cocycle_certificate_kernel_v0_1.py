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

from runtime.kuuos_memoryos_quotient_metric_covector_transport_certificate_kernel_v0_1 import (
    issue_quotient_metric_covector_transport_certificate,
)
from runtime.kuuos_memoryos_quotient_transport_jacobian_volume_stratification_certificate_kernel_v0_1 import (
    issue_quotient_transport_jacobian_volume_stratification_certificate,
)
from runtime.kuuos_memoryos_quotient_metric_density_transport_radon_nikodym_cocycle_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_quotient_metric_density_transport_radon_nikodym_cocycle_certificate,
)
from scripts.check_planos_memoryos_quotient_metric_covector_transport_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v052_payload,
)
from scripts.check_planos_memoryos_quotient_transport_jacobian_volume_stratification_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v053_payload,
)


def source_memoryos_v052_certificate() -> dict[str, Any]:
    result = issue_quotient_metric_covector_transport_certificate(
        build_memoryos_v052_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def source_memoryos_v053_certificate() -> dict[str, Any]:
    result = issue_quotient_transport_jacobian_volume_stratification_certificate(
        build_memoryos_v053_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v053 = source_memoryos_v053_certificate()
    source_v052 = source_memoryos_v052_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v053_certificate": source_v053,
        "source_memoryos_v052_certificate": source_v052,
        "claims": _derive_observables(source_v053, source_v052),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


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


def _resign_v052(certificate: dict[str, Any]) -> None:
    observables = certificate["observables"]
    observables["quotient_metric_covector_transport_digest"] = canonical_digest(
        observables["quotient_metric_covector_transport_trajectory"]
    )
    observables["quotient_metric_transport_composition_digest"] = canonical_digest(
        observables["quotient_metric_transport_composition_records"]
    )
    _resign(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_quotient_metric_density_transport_radon_nikodym_cocycle_certificate(
        payload
    )
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_quotient_metric_density_transport_radon_nikodym_cocycle_certificate(
        payload
    )
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    assert obs["transition_count"] == 9
    assert obs["density_active_transition_count"] == 4
    assert obs["probe_density_transport_record_count"] == 36
    assert obs["singular_measure_collapse_transition_count"] == 2
    assert obs["singular_probe_pushforward_record_count"] == 18
    assert obs["rank_one_source_boundary_count"] == 3
    assert obs["density_cocycle_record_count"] == 27
    assert obs["active_density_cocycle_count"] == 8
    assert obs["nontrivial_round_trip_density_path_count"] == 2

    assert obs["reference_one_to_zero_symmetric_density_multiplier"] == {
        "numerator": 3,
        "denominator": 2,
    }
    assert obs["reference_one_to_zero_antisymmetric_density_multiplier"] == {
        "numerator": 1,
        "denominator": 2,
    }
    assert obs["reference_one_to_zero_radon_nikodym_multiplier"] == {
        "numerator": 3,
        "denominator": 4,
    }
    assert obs["reference_zero_to_one_symmetric_density_multiplier"] == {
        "numerator": 2,
        "denominator": 3,
    }
    assert obs["reference_zero_to_one_antisymmetric_density_multiplier"] == {
        "numerator": 2,
        "denominator": 1,
    }
    assert obs["reference_zero_to_one_radon_nikodym_multiplier"] == {
        "numerator": 4,
        "denominator": 3,
    }

    transitions = obs["quotient_metric_density_transport_trajectory"]
    one_to_zero = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 1
        and item["target_cross_numerator"] == 0
    )
    assert one_to_zero["density_transport_active"] is True
    assert one_to_zero["density_jacobian_reciprocal_exact"] is True
    assert one_to_zero["mode_density_product_equals_radon_nikodym"] is True
    assert len(one_to_zero["probe_density_transport_records"]) == 9
    assert all(
        item["pushforward_mass_preserved"]
        and item["pullback_density_recovers_source"]
        for item in one_to_zero["probe_density_transport_records"]
    )

    collapse = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 1
        and item["target_cross_numerator"] == 2
    )
    assert collapse["density_transport_active"] is False
    assert collapse[
        "full_rank_to_rank_one_singular_measure_boundary"
    ] is True
    assert collapse["radon_nikodym_density_multiplier"] is None
    assert collapse["source_normalized_jacobian"] == {
        "numerator": 0,
        "denominator": 1,
    }
    assert len(collapse["singular_probe_pushforward_records"]) == 9
    assert all(
        item["support_retained_as_singular_measure"]
        and not item["two_dimensional_target_density_emitted"]
        for item in collapse["singular_probe_pushforward_records"]
    )

    boundary = next(
        item
        for item in transitions
        if item["source_cross_numerator"] == 2
        and item["target_cross_numerator"] == 1
    )
    assert boundary["rank_one_source_boundary"] is True
    assert boundary["density_transport_active"] is False
    assert boundary["radon_nikodym_density_multiplier"] is None
    assert boundary[
        "rank_one_source_two_dimensional_density_recovery_claimed"
    ] is False

    compositions = obs["radon_nikodym_cocycle_records"]
    assert all(
        not item["density_cocycle_active"]
        or item["radon_nikodym_cocycle_exact"]
        for item in compositions
    )
    assert sum(
        item["nontrivial_round_trip_density_preserved"]
        for item in compositions
    ) == 2

    tampered = copy.deepcopy(payload)
    tampered_transition = tampered["source_memoryos_v053_certificate"][
        "observables"
    ]["quotient_transport_jacobian_trajectory"][4]
    tampered_transition["normalized_jacobian"] = {
        "numerator": 7,
        "denominator": 5,
    }
    _resign_v053(tampered["source_memoryos_v053_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v053_normalized_jacobian_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered_composition = tampered["source_memoryos_v053_certificate"][
        "observables"
    ]["quotient_transport_mode_composition_records"][13]
    tampered_composition["normalized_mode_composition_exact"] = False
    _resign_v053(tampered["source_memoryos_v053_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v053_normalized_composition_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered_v052_transition = tampered["source_memoryos_v052_certificate"][
        "observables"
    ]["quotient_metric_covector_transport_trajectory"][4]
    tampered_v052_transition["transport_numerator_matrix"][0][0] += 1
    _resign_v052(tampered["source_memoryos_v052_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v052_transport_matrix_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"][
        "rank_one_source_two_dimensional_density_not_recovered"
    ] = False
    assert_rejects(
        tampered,
        "claim_mismatch_rank_one_source_two_dimensional_density_not_recovered",
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
                "density_transport_digest": obs[
                    "quotient_metric_density_transport_digest"
                ],
                "radon_nikodym_cocycle_digest": obs[
                    "radon_nikodym_cocycle_digest"
                ],
                "transition_count": obs["transition_count"],
                "density_active_transition_count": obs[
                    "density_active_transition_count"
                ],
                "probe_density_transport_record_count": obs[
                    "probe_density_transport_record_count"
                ],
                "singular_measure_collapse_transition_count": obs[
                    "singular_measure_collapse_transition_count"
                ],
                "active_density_cocycle_count": obs[
                    "active_density_cocycle_count"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
