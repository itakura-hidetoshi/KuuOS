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

from runtime.kuuos_memoryos_wasserstein_marton_transport_certificate_kernel_v0_1 import (
    issue_wasserstein_marton_transport_certificate,
)
from runtime.kuuos_memoryos_kantorovich_lipschitz_mgf_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_kantorovich_lipschitz_mgf_certificate,
)
from scripts.check_planos_memoryos_wasserstein_marton_transport_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v062_payload,
)


def source_memoryos_v062_certificate() -> dict[str, Any]:
    result = issue_wasserstein_marton_transport_certificate(
        build_memoryos_v062_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v062 = source_memoryos_v062_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v062_certificate": source_v062,
        "claims": _derive_observables(source_v062),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_kantorovich_lipschitz_mgf_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_kantorovich_lipschitz_mgf_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "kantorovich_dual_witness_record_count": 5,
        "lipschitz_semigroup_profile_record_count": 33,
        "reference_observable_gap_record_count": 22,
        "reference_pair_observable_gap_record_count": 11,
        "finite_symbolic_mgf_record_count": 22,
        "marton_mgf_input_record_count": 22,
        "full_rank_transport_kantorovich_lipschitz_mgf_record_count": 8,
        "singular_atomic_kantorovich_lipschitz_mgf_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    dual = {x["record_id"]: x for x in obs["kantorovich_dual_witness_records"]}
    assert dual["slow_positive"]["explicit_optimizer"] == [
        {"numerator": 1, "denominator": 1},
        {"numerator": 0, "denominator": 1},
        {"numerator": -1, "denominator": 1},
    ]
    assert dual["slow_positive"]["dual_objective"] == {
        "numerator": 2,
        "denominator": 1,
    }
    assert dual["mixed_positive"]["dual_objective"] == {
        "numerator": 3,
        "denominator": 1,
    }
    assert all(
        x["centered_exact"]
        and x["optimizer_one_lipschitz"]
        and x["explicit_dual_equality"]
        and x["universal_dual_upper_bound_formally_proved"]
        for x in dual.values()
    )

    semigroup = {
        (x["observable_id"], x["horizon"]): x
        for x in obs["lipschitz_semigroup_profile_records"]
    }
    assert semigroup[("slow", 4)]["lipschitz_seminorm"] == {
        "numerator": 81,
        "denominator": 256,
    }
    assert semigroup[("fast", 4)]["lipschitz_seminorm"] == {
        "numerator": 3,
        "denominator": 256,
    }
    assert all(
        x["one_step_lipschitz_contraction"]
        and x["iterated_lipschitz_contraction"]
        and x["eigenmode_profile_exact"]
        for x in semigroup.values()
    )

    reference = obs["reference_observable_gap_records"]
    p0 = next(
        x
        for x in reference
        if x["distribution_id"] == "reference_p" and x["horizon"] == 0
    )
    assert p0["absolute_expectation_gap"] == {
        "numerator": 3,
        "denominator": 10,
    }
    assert p0["path_wasserstein_one"] == {
        "numerator": 3,
        "denominator": 10,
    }
    assert all(
        x["kantorovich_upper_bound"]
        and x["explicit_optimizer_equality"]
        and x["expected_geometric_profile_exact"]
        for x in reference
    )

    pair = obs["reference_pair_observable_gap_records"]
    assert pair[0]["absolute_expectation_gap"] == {
        "numerator": 3,
        "denominator": 5,
    }
    assert all(
        x["kantorovich_upper_bound"]
        and x["explicit_optimizer_equality"]
        and x["expected_geometric_profile_exact"]
        for x in pair
    )

    mgf = {
        (x["observable_id"], x["horizon"]): x
        for x in obs["finite_symbolic_mgf_records"]
    }
    assert mgf[("slow", 0)]["centered_exponents"] == [
        {"numerator": 1, "denominator": 1},
        {"numerator": 0, "denominator": 1},
        {"numerator": -1, "denominator": 1},
    ]
    assert mgf[("slow", 0)]["second_moment"] == {
        "numerator": 2,
        "denominator": 3,
    }
    assert mgf[("fast", 4)]["second_moment"] == {
        "numerator": 1,
        "denominator": 32768,
    }
    assert all(
        x["centered_exact"]
        and x["finite_symbolic_mgf_identity_exact"]
        and x["semigroup_scaled_exponents_exact"]
        and not x["general_gaussian_envelope_claimed"]
        for x in mgf.values()
    )

    marton_inputs = {
        (x["observable_id"], x["horizon"]): x
        for x in obs["marton_mgf_input_records"]
    }
    assert marton_inputs[("slow", 4)][
        "influence_weighted_lipschitz_sensitivity"
    ] == {"numerator": 14175, "denominator": 16384}
    assert marton_inputs[("fast", 4)][
        "influence_weighted_lipschitz_sensitivity"
    ] == {"numerator": 525, "denominator": 16384}
    assert all(
        x["finite_marton_mgf_input_retained"]
        and not x["path_space_gaussian_theorem_claimed"]
        for x in marton_inputs.values()
    )

    assert obs["three_point_kantorovich_duality_explicit_optimizer_exact"]
    assert obs["one_lipschitz_expectation_gap_bounded_by_wasserstein"]
    assert obs["reference_dual_optimizer_profiles_exact"]
    assert obs["reference_pair_dual_optimizer_profile_exact"]
    assert obs["kernel_lipschitz_contraction_three_quarters_exact"]
    assert obs["iterated_lipschitz_semigroup_contraction_exact"]
    assert obs["slow_fast_eigenmode_observable_profiles_exact"]
    assert obs["finite_symbolic_mgf_profiles_exact"]
    assert obs["marton_influence_mgf_inputs_exact"]
    assert obs["general_path_space_gaussian_theorem_not_claimed"]

    assert all(
        x["kantorovich_duality_commutes"]
        and x["lipschitz_semigroup_profile_commutes"]
        and x["finite_symbolic_mgf_terms_commute"]
        for x in obs["full_rank_transport_kantorovich_lipschitz_mgf_records"]
    )
    assert all(
        x["atomic_kantorovich_witness_retained"]
        and x["atomic_lipschitz_profile_retained"]
        and x["atomic_symbolic_mgf_terms_retained"]
        and not x["two_dimensional_target_density_emitted"]
        and not x["lost_coordinate_reconstructed"]
        for x in obs["singular_atomic_kantorovich_lipschitz_mgf_records"]
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v062_certificate"]["observables"][
        "marton_influence_profile_records"
    ][4]["influence_sum"] = {"numerator": 7, "denominator": 1}
    _resign(tampered["source_memoryos_v062_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v062_marton_influence_profile_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["kantorovich_dual_witness_records"][1][
        "dual_objective"
    ] = {"numerator": 1, "denominator": 1}
    assert_rejects(tampered, "claim_mismatch_kantorovich_dual_witness_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["kernel_lipschitz_contraction_three_quarters_exact"] = False
    assert_rejects(
        tampered,
        "claim_mismatch_kernel_lipschitz_contraction_three_quarters_exact",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["general_path_space_gaussian_theorem_not_claimed"] = False
    assert_rejects(
        tampered,
        "claim_mismatch_general_path_space_gaussian_theorem_not_claimed",
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
                "kantorovich_dual_witness_digest": obs[
                    "kantorovich_dual_witness_digest"
                ],
                "lipschitz_semigroup_profile_digest": obs[
                    "lipschitz_semigroup_profile_digest"
                ],
                "finite_symbolic_mgf_digest": obs["finite_symbolic_mgf_digest"],
                "marton_mgf_input_digest": obs["marton_mgf_input_digest"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
