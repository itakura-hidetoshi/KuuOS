#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_normalized_root_word_groupoid_descent_certificate_kernel_v0_1 import (
    issue_normalized_root_word_groupoid_descent_certificate,
)
from runtime.kuuos_memoryos_global_word_cech_descent_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_global_word_cech_descent_certificate,
)
from scripts.check_planos_memoryos_normalized_root_word_groupoid_descent_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v081_payload,
)


def source_memoryos_v081_certificate() -> dict[str, Any]:
    result = issue_normalized_root_word_groupoid_descent_certificate(
        build_memoryos_v081_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v081 = source_memoryos_v081_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v081_certificate": source_v081,
        "claims": _derive_observables(source_v081),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_global_word_cech_descent_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_global_word_cech_descent_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_global_word_descent_record_count": 6,
        "route_object_record_count": 4,
        "global_section_component_record_count": 4,
        "global_section_compatibility_record_count": 16,
        "descent_mismatch_record_count": 16,
        "descent_mismatch_cocycle_record_count": 64,
        "descent_mismatch_inverse_record_count": 16,
        "global_section_reconstruction_record_count": 16,
        "tampered_local_family_component_record_count": 4,
        "tampered_descent_mismatch_record_count": 16,
        "tampered_mismatch_cocycle_record_count": 64,
        "global_section_evaluation_record_count": 8,
        "global_wilson_descent_record_count": 2,
        "source_confidence_preservation_record_count": 4,
        "global_word_descent_memory_fusion_record_count": 4,
        "full_rank_transport_global_word_descent_record_count": 8,
        "singular_atomic_global_word_descent_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    assert [record["route_id"] for record in obs["route_object_records"]] == [
        "route-0", "route-1", "route-2", "route-3"
    ]
    assert all(
        record["descent_compatible"]
        for record in obs["global_section_compatibility_records"]
    )
    assert all(
        record["mismatch_is_identity"]
        for record in obs["descent_mismatch_records"]
    )
    assert all(
        record["nonabelian_cech_cocycle_exact"]
        for record in obs["descent_mismatch_cocycle_records"]
    )
    assert all(
        record["mismatch_inverse_exact"]
        for record in obs["descent_mismatch_inverse_records"]
    )
    assert all(
        record["reconstruction_exact"]
        for record in obs["global_section_reconstruction_records"]
    )

    tampered_components = obs["tampered_local_family_component_records"]
    assert [record["root_route_id"] for record in tampered_components] == [
        "route-0", "route-1", "route-2", "route-3"
    ]
    assert [record["component_changed"] for record in tampered_components] == [
        False, False, True, False
    ]
    tampered_mismatches = obs["tampered_descent_mismatch_records"]
    assert obs["tampered_mismatch_nontrivial_support_count"] == 6
    assert sum(record["mismatch_nontrivial"] for record in tampered_mismatches) == 6
    assert all(
        record["single_chart_tamper_localized_exact"]
        for record in tampered_mismatches
    )
    assert all(
        record["tampered_cocycle_exact"]
        for record in obs["tampered_mismatch_cocycle_records"]
    )

    evaluations = obs["global_section_evaluation_records"]
    ordered_ab = [r for r in evaluations if r["profile_id"] == "ordered_ab_atlas"]
    ordered_ba = [r for r in evaluations if r["profile_id"] == "ordered_ba_atlas"]
    assert len(ordered_ab) == len(ordered_ba) == 4
    assert all(record["exact_group_value"] == [0, 1, 2] for record in ordered_ab)
    assert all(record["wilson_trace"] == 3 for record in ordered_ab)
    assert all(record["exact_group_value"] == [2, 0, 1] for record in ordered_ba)
    assert all(record["wilson_trace"] == 0 for record in ordered_ba)
    wilson = {record["profile_id"]: record for record in obs["global_wilson_descent_records"]}
    assert wilson["ordered_ab_atlas"]["root_traces"] == [3, 3, 3, 3]
    assert wilson["ordered_ab_atlas"]["root_independent"]
    assert wilson["ordered_ba_atlas"]["root_traces"] == [0, 0, 0, 0]
    assert wilson["ordered_ba_atlas"]["root_independent"]

    expected_confidence = {
        "flat_four_route_atlas": {"numerator": 1, "denominator": 3},
        "single_support_atlas": {"numerator": 5, "denominator": 18},
        "ordered_ab_atlas": {"numerator": 11, "denominator": 54},
        "ordered_ba_atlas": {"numerator": 11, "denominator": 54},
    }
    for record in obs["source_confidence_preservation_records"]:
        expected = expected_confidence[record["profile_id"]]
        assert record["normalized_groupoid_adjusted_confidence"] == expected
        assert record["global_cech_descent_adjusted_confidence"] == expected
        assert record["new_global_descent_penalty"] == {
            "numerator": 0,
            "denominator": 1,
        }
        assert record["confidence_preserved_exactly"]

    required_true = (
        "source_memoryos_v081_exact",
        "finite_free_group_cech_descent_exact",
        "local_word_family_mismatch_exact",
        "nonabelian_mismatch_cocycle_exact",
        "mismatch_inverse_exact",
        "compatible_family_reconstruction_exact",
        "global_section_anchor_independence_exact",
        "global_section_evaluation_descent_exact",
        "global_wilson_descent_exact",
        "single_chart_tamper_localization_exact",
        "tampered_family_cocycle_exact",
        "canonical_separator_global_section_exact",
        "source_confidence_preserved_exact",
        "no_new_confidence_penalty_introduced",
        "all_full_rank_transport_global_descent_layer_commutes",
        "singular_atomic_global_descent_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "global_word_descent_not_truth_authority",
        "mismatch_review_not_candidate_ranking",
        "tamper_localization_not_source_deletion",
        "global_wilson_not_candidate_selection",
        "future_only",
        "read_only",
    )
    for field in required_true:
        assert obs[field] is True, field

    required_false = (
        "universal_sheaf_descent_claimed",
        "continuum_stack_claimed",
        "universal_nonabelian_cohomology_classification_claimed",
        "physical_gauge_field_inference_claimed",
        "global_section_used_as_truth",
        "mismatch_support_used_as_candidate_ranking",
        "source_confidence_mutated",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v081_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    )
    for field in required_false:
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["claims"]["descent_mismatch_cocycle_records"][17][
        "nonabelian_cech_cocycle_exact"
    ] = False
    assert_rejects(tampered, "claim_mismatch_descent_mismatch_cocycle_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["global_section_reconstruction_records"][7][
        "reconstruction_exact"
    ] = False
    assert_rejects(tampered, "claim_mismatch_global_section_reconstruction_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["tampered_descent_mismatch_records"][2][
        "mismatch_nontrivial"
    ] = False
    assert_rejects(tampered, "claim_mismatch_tampered_descent_mismatch_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["global_section_evaluation_records"][0][
        "wilson_trace"
    ] = 0
    assert_rejects(tampered, "claim_mismatch_global_section_evaluation_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["source_confidence_preservation_records"][0][
        "global_cech_descent_adjusted_confidence"
    ] = {"numerator": 1, "denominator": 2}
    assert_rejects(tampered, "claim_mismatch_source_confidence_preservation_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["global_word_descent_not_truth_authority"] = False
    assert_rejects(tampered, "claim_mismatch_global_word_descent_not_truth_authority")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_truth_claim"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_truth_claim")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v081_certificate"]["observables"][
        "normalized_mixed_separator_records"
    ][0]["ordered_ab_trace"] = 0
    assert_rejects(
        tampered,
        "source_memoryos_v081_certificate_digest_mismatch",
    )

    print("MemoryOS v0.82 global word non-Abelian Cech descent checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
