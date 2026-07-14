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

from runtime.kuuos_memoryos_modified_log_sobolev_hellinger_separation_certificate_kernel_v0_1 import (
    issue_modified_log_sobolev_hellinger_separation_certificate,
)
from runtime.kuuos_memoryos_bakry_emery_concentration_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_bakry_emery_concentration_certificate,
)
from scripts.check_planos_memoryos_modified_log_sobolev_hellinger_separation_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v060_payload,
)


def source_memoryos_v060_certificate() -> dict[str, Any]:
    result = issue_modified_log_sobolev_hellinger_separation_certificate(
        build_memoryos_v060_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v060 = source_memoryos_v060_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v060_certificate": source_v060,
        "claims": _derive_observables(source_v060),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_bakry_emery_concentration_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_bakry_emery_concentration_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "integrated_curvature_mode_record_count": 2,
        "functional_inequality_hierarchy_record_count": 1,
        "reference_hierarchy_profile_record_count": 22,
        "concentration_profile_record_count": 36,
        "concentration_threshold_record_count": 4,
        "full_rank_transport_curvature_concentration_record_count": 8,
        "singular_atomic_curvature_concentration_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    mode_records = {
        x["mode_id"]: x for x in obs["integrated_curvature_mode_records"]
    }
    slow = mode_records["antisymmetric_slow"]
    fast = mode_records["curvature_fast"]
    assert slow["chi_square"] == {"numerator": 6, "denominator": 1}
    assert slow["dirichlet_energy"] == {
        "numerator": 3,
        "denominator": 2,
    }
    assert slow["integrated_gamma_two"] == {
        "numerator": 3,
        "denominator": 8,
    }
    assert slow["generator_gap"] == {
        "numerator": 1,
        "denominator": 4,
    }
    assert slow["curvature_equality"]
    assert slow["poincare_equality"]
    assert fast["generator_gap"] == {
        "numerator": 3,
        "denominator": 4,
    }
    assert fast["integrated_gamma_two"] == {
        "numerator": 81,
        "denominator": 8,
    }
    assert fast["curvature_inequality_exact"]
    assert fast["poincare_inequality_exact"]
    assert not fast["curvature_equality"]
    assert not fast["poincare_equality"]

    hierarchy = obs["functional_inequality_hierarchy_record"]
    assert hierarchy["all_links_formally_proved"]
    assert hierarchy["curvature_sharp_on_slow_mode"]
    assert hierarchy["poincare_sharp_on_slow_mode"]
    assert hierarchy["fast_mode_strict_curvature_gap"]
    assert hierarchy["fast_mode_strict_poincare_gap"]

    for distribution_id in ("reference_p", "reference_q"):
        records = [
            x
            for x in obs["reference_hierarchy_profile_records"]
            if x["distribution_id"] == distribution_id
        ]
        assert len(records) == 11
        assert records[0]["chi_square"] == {
            "numerator": 27,
            "denominator": 200,
        }
        assert records[0]["dirichlet_energy"] == {
            "numerator": 27,
            "denominator": 800,
        }
        assert records[0]["integrated_gamma_two"] == {
            "numerator": 27,
            "denominator": 3200,
        }
        assert all(x["chi_square_equals_four_dirichlet"] for x in records)
        assert all(
            x["four_dirichlet_equals_sixteen_gamma_two"] for x in records
        )
        assert all(x["chi_square_decay_exact"] for x in records)
        assert all(
            x["relative_entropy_le_chi_square_formally_bound"] for x in records
        )

    for distribution_id in ("reference_p", "reference_q"):
        quarter = [
            x
            for x in obs["concentration_profile_records"]
            if x["distribution_id"] == distribution_id
            and x["threshold_id"] == "likelihood_deviation_quarter"
        ]
        eighth = [
            x
            for x in obs["concentration_profile_records"]
            if x["distribution_id"] == distribution_id
            and x["threshold_id"] == "likelihood_deviation_eighth"
        ]
        assert len(quarter) == 9
        assert len(eighth) == 9
        assert quarter[2]["tail_mass"] == {
            "numerator": 2,
            "denominator": 3,
        }
        assert quarter[3]["tail_mass"] == {
            "numerator": 0,
            "denominator": 1,
        }
        assert eighth[4]["tail_mass"] == {
            "numerator": 2,
            "denominator": 3,
        }
        assert eighth[5]["tail_mass"] == {
            "numerator": 0,
            "denominator": 1,
        }
        assert all(x["quadratic_concentration_exact"] for x in quarter + eighth)
        assert all(x["tail_profile_exact"] for x in quarter + eighth)

    thresholds = {
        (x["distribution_id"], x["threshold_id"]): x
        for x in obs["concentration_threshold_records"]
    }
    for distribution_id in ("reference_p", "reference_q"):
        assert thresholds[
            (distribution_id, "likelihood_deviation_quarter")
        ]["previous_time"] == 2
        assert thresholds[
            (distribution_id, "likelihood_deviation_quarter")
        ]["certified_time"] == 3
        assert thresholds[
            (distribution_id, "likelihood_deviation_eighth")
        ]["previous_time"] == 4
        assert thresholds[
            (distribution_id, "likelihood_deviation_eighth")
        ]["certified_time"] == 5
    assert all(
        x["previous_tail_active"]
        and x["certified_tail_zero"]
        and x["first_zero_time_exact"]
        for x in thresholds.values()
    )

    assert all(
        x["curvature_hierarchy_transport_commutes"]
        and x["concentration_profile_transport_commutes"]
        for x in obs["full_rank_transport_curvature_concentration_records"]
    )
    assert all(
        x["singular_atomic_curvature_ledger_retained"]
        and x["singular_atomic_concentration_ledger_retained"]
        and not x["two_dimensional_target_density_emitted"]
        and not x["lost_antisymmetric_information_reconstructed"]
        for x in obs["singular_atomic_curvature_concentration_records"]
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v060_certificate"]["observables"][
        "reference_separation_profile_records"
    ][0]["separation_to_uniform"] = {
        "numerator": 1,
        "denominator": 2,
    }
    _resign(tampered["source_memoryos_v060_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v060_reference_separation_profile_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["integrated_curvature_mode_records"][0][
        "curvature_lower_bound"
    ] = {"numerator": 1, "denominator": 3}
    assert_rejects(tampered, "claim_mismatch_integrated_curvature_mode_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["concentration_threshold_records"][0][
        "certified_time"
    ] = 2
    assert_rejects(tampered, "claim_mismatch_concentration_threshold_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(tampered, "claim_mismatch_candidate_selection_performed")

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": result["schema_version"],
                "certificate_digest": result["certificate_digest"],
                "integrated_curvature_mode_digest": obs[
                    "integrated_curvature_mode_digest"
                ],
                "functional_inequality_hierarchy_digest": obs[
                    "functional_inequality_hierarchy_digest"
                ],
                "reference_hierarchy_profile_digest": obs[
                    "reference_hierarchy_profile_digest"
                ],
                "concentration_profile_digest": obs[
                    "concentration_profile_digest"
                ],
                "concentration_threshold_digest": obs[
                    "concentration_threshold_digest"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
