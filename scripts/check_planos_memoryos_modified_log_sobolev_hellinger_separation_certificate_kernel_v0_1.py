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

from runtime.kuuos_memoryos_reversible_markov_semigroup_entropy_production_certificate_kernel_v0_1 import (
    issue_reversible_markov_semigroup_entropy_production_certificate,
)
from runtime.kuuos_memoryos_log_sobolev_hypercontractive_mixing_certificate_kernel_v0_1 import (
    issue_log_sobolev_hypercontractive_mixing_certificate,
)
from runtime.kuuos_memoryos_modified_log_sobolev_hellinger_separation_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_modified_log_sobolev_hellinger_separation_certificate,
)
from scripts.check_planos_memoryos_reversible_markov_semigroup_entropy_production_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v058_payload,
)
from scripts.check_planos_memoryos_log_sobolev_hypercontractive_mixing_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v059_payload,
)


def source_memoryos_v058_certificate() -> dict[str, Any]:
    result = issue_reversible_markov_semigroup_entropy_production_certificate(
        build_memoryos_v058_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def source_memoryos_v059_certificate() -> dict[str, Any]:
    result = issue_log_sobolev_hypercontractive_mixing_certificate(
        build_memoryos_v059_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v059 = source_memoryos_v059_certificate()
    source_v058 = source_memoryos_v058_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v059_certificate": source_v059,
        "source_memoryos_v058_certificate": source_v058,
        "claims": _derive_observables(source_v059, source_v058),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_modified_log_sobolev_hellinger_separation_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_modified_log_sobolev_hellinger_separation_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "two_step_doeblin_record_count": 1,
        "two_step_decomposition_record_count": 9,
        "modified_entropy_block_record_count": 12,
        "reference_symbolic_kl_block_record_count": 24,
        "reference_hellinger_profile_record_count": 22,
        "reference_separation_profile_record_count": 22,
        "worst_case_separation_profile_record_count": 11,
        "cutoff_threshold_record_count": 5,
        "full_rank_transport_modified_entropy_profile_record_count": 8,
        "singular_atomic_modified_entropy_profile_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    assert obs["doeblin_stationary_weight"] == {
        "numerator": 3,
        "denominator": 16,
    }
    assert obs["doeblin_residual_weight"] == {
        "numerator": 13,
        "denominator": 16,
    }
    doeblin = obs["two_step_doeblin_record"]
    assert doeblin["weights_sum_to_one"]
    assert doeblin["residual_rows_stochastic"]
    assert doeblin["residual_columns_stochastic"]
    assert doeblin["residual_kernel_symmetric"]
    assert doeblin["all_decomposition_entries_exact"]
    assert all(
        x["decomposition_exact"]
        for x in obs["two_step_decomposition_records"]
    )

    blocks = obs["modified_entropy_block_records"]
    assert blocks[0]["modified_entropy_contraction_coefficient"] == {
        "numerator": 1,
        "denominator": 1,
    }
    assert blocks[1]["modified_entropy_contraction_coefficient"] == {
        "numerator": 13,
        "denominator": 16,
    }
    assert blocks[11]["physical_time"] == 22
    assert all(x["coefficient_nonnegative"] for x in blocks)

    for distribution_id in ("reference_p", "reference_q"):
        hellinger = [
            x
            for x in obs["reference_hellinger_profile_records"]
            if x["distribution_id"] == distribution_id
        ]
        separation = [
            x
            for x in obs["reference_separation_profile_records"]
            if x["distribution_id"] == distribution_id
        ]
        assert len(hellinger) == 11
        assert len(separation) == 11
        assert all(
            x["all_sqrt_arguments_nonnegative"]
            and x["hellinger_envelope_formally_bound"]
            for x in hellinger
        )
        assert all(x["separation_exact"] for x in separation)
        assert separation[0]["separation_to_uniform"] == {
            "numerator": 9,
            "denominator": 20,
        }
        assert separation[8]["separation_to_uniform"] == {
            "numerator": 59049,
            "denominator": 1310720,
        }

    worst = obs["worst_case_separation_profile_records"]
    assert all(x["profile_exact"] for x in worst)
    assert worst[0]["explicit_worst_case_separation"] == {
        "numerator": 1,
        "denominator": 1,
    }
    assert worst[7]["explicit_worst_case_separation"] == {
        "numerator": 205,
        "denominator": 1024,
    }
    assert worst[9]["explicit_worst_case_separation"] == {
        "numerator": 7381,
        "denominator": 65536,
    }

    thresholds = {
        x["threshold_id"]: x for x in obs["cutoff_threshold_records"]
    }
    assert thresholds["worst_case_separation_le_one_quarter"][
        "certified_index"
    ] == 7
    assert thresholds["worst_case_separation_le_one_eighth"][
        "certified_index"
    ] == 9
    assert thresholds["reference_separation_le_one_twentieth"][
        "certified_index"
    ] == 8
    assert thresholds["reference_hellinger_le_one_twentieth_envelope"][
        "certified_index"
    ] == 6
    assert thresholds["worst_case_kl_le_one_quarter_block"][
        "certified_physical_time"
    ] == 22
    assert all(
        x["certified"] and x["previous_value_not_sufficient"]
        for x in thresholds.values()
    )

    assert all(
        x["mass_normalized"]
        and x["modified_log_sobolev_decay_formally_bound"]
        for x in obs["reference_symbolic_kl_block_records"]
    )
    assert all(
        x["modified_log_sobolev_decay_transport_commutes"]
        and x["hellinger_profile_transport_commutes"]
        and x["separation_profile_transport_commutes"]
        for x in obs[
            "full_rank_transport_modified_entropy_profile_records"
        ]
    )
    assert all(
        x["singular_atomic_modified_entropy_ledger_retained"]
        and x["singular_atomic_hellinger_ledger_retained"]
        and x["singular_atomic_separation_ledger_retained"]
        and not x["two_dimensional_target_density_emitted"]
        for x in obs["singular_atomic_modified_entropy_profile_records"]
    )

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v059_certificate"]["observables"][
        "reference_total_variation_records"
    ][0]["total_variation_to_uniform"] = {
        "numerator": 1,
        "denominator": 2,
    }
    _resign(tampered["source_memoryos_v059_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v059_reference_total_variation_digest_mismatch",
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
    tampered["claims"]["doeblin_residual_weight"] = {
        "numerator": 3,
        "denominator": 4,
    }
    assert_rejects(tampered, "claim_mismatch_doeblin_residual_weight")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["cutoff_threshold_records"][0][
        "certified_index"
    ] = 6
    assert_rejects(tampered, "claim_mismatch_cutoff_threshold_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_pruning_performed"] = True
    assert_rejects(tampered, "claim_mismatch_candidate_pruning_performed")

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": result["schema_version"],
                "certificate_digest": result["certificate_digest"],
                "two_step_doeblin_digest": obs["two_step_doeblin_digest"],
                "modified_entropy_block_digest": obs[
                    "modified_entropy_block_digest"
                ],
                "reference_hellinger_profile_digest": obs[
                    "reference_hellinger_profile_digest"
                ],
                "reference_separation_profile_digest": obs[
                    "reference_separation_profile_digest"
                ],
                "worst_case_separation_profile_digest": obs[
                    "worst_case_separation_profile_digest"
                ],
                "cutoff_threshold_digest": obs["cutoff_threshold_digest"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
