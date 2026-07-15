#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_global_section_group_anchor_coherence_certificate_kernel_v0_1 import (
    issue_global_section_group_anchor_coherence_certificate,
)
from runtime.kuuos_memoryos_global_observable_kernel_quotient_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_global_observable_kernel_quotient_certificate,
)
from scripts.check_planos_memoryos_global_section_group_anchor_coherence_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v083_payload,
)


def source_memoryos_v083_certificate() -> dict[str, Any]:
    result = issue_global_section_group_anchor_coherence_certificate(
        build_memoryos_v083_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v083 = source_memoryos_v083_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v083_certificate": source_v083,
        "claims": _derive_observables(source_v083),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_global_observable_kernel_quotient_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_global_observable_kernel_quotient_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_global_observable_quotient_record_count": 6,
        "observable_kernel_normality_record_count": 4,
        "observable_kernel_root_independence_record_count": 16,
        "observable_range_record_count": 4,
        "observable_range_root_independence_record_count": 16,
        "observable_first_isomorphism_record_count": 4,
        "observational_equivalence_record_count": 16,
        "observable_image_record_count": 8,
        "canonical_kernel_visibility_record_count": 4,
        "source_confidence_preservation_record_count": 4,
        "global_observable_quotient_memory_fusion_record_count": 4,
        "full_rank_transport_global_observable_quotient_record_count": 8,
        "singular_atomic_global_observable_quotient_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    assert all(
        record["kernel_is_subgroup"]
        and record["kernel_is_normal"]
        and record["identity_observable_exact"]
        for record in obs["observable_kernel_normality_records"]
    )
    assert all(
        record["evaluation_hom_equal"]
        and record["kernel_subgroups_equal"]
        for record in obs["observable_kernel_root_independence_records"]
    )
    assert all(
        record["evaluation_range_is_subgroup"]
        and record["range_restriction_exact"]
        for record in obs["observable_range_records"]
    )
    assert all(
        record["evaluation_hom_equal"]
        and record["range_subgroups_equal"]
        for record in obs["observable_range_root_independence_records"]
    )
    assert all(
        record["quotient_by_evaluation_kernel"]
        and record["range_target_exact"]
        and record["quotient_range_mul_equivalence_exact"]
        and record["representative_maps_to_exact_evaluation"]
        for record in obs["observable_first_isomorphism_records"]
    )
    assert all(
        record["ratio_in_kernel_iff_equal_evaluation"]
        and record["equivalence_is_exact_not_heuristic"]
        for record in obs["observational_equivalence_records"]
    )
    assert all(
        record["lies_in_evaluation_range"]
        and record["quotient_representative_image_exact"]
        for record in obs["observable_image_records"]
    )

    visibility = obs["canonical_kernel_visibility_records"]
    assert [record["root_route_id"] for record in visibility] == [
        "route-0", "route-1", "route-2", "route-3"
    ]
    assert all(record["ordered_ab_value"] == [0, 1, 2] for record in visibility)
    assert all(record["ordered_ba_value"] == [2, 0, 1] for record in visibility)
    assert all(record["ordered_ab_in_invisible_kernel"] for record in visibility)
    assert all(not record["ordered_ba_in_invisible_kernel"] for record in visibility)
    assert all(record["ordered_ba_visible_in_observable_quotient"] for record in visibility)
    assert all(record["kernel_visibility_separator_exact"] for record in visibility)

    expected_confidence = {
        "flat_four_route_atlas": {"numerator": 1, "denominator": 3},
        "single_support_atlas": {"numerator": 5, "denominator": 18},
        "ordered_ab_atlas": {"numerator": 11, "denominator": 54},
        "ordered_ba_atlas": {"numerator": 11, "denominator": 54},
    }
    for record in obs["source_confidence_preservation_records"]:
        expected = expected_confidence[record["profile_id"]]
        assert record["source_global_section_group_adjusted_confidence"] == expected
        assert record["global_observable_quotient_adjusted_confidence"] == expected
        assert record["new_observable_quotient_penalty"] == {
            "numerator": 0,
            "denominator": 1,
        }
        assert record["confidence_preserved_exactly"]

    required_true = (
        "source_memoryos_v083_exact",
        "finite_global_observable_quotient_exact",
        "evaluation_kernel_normal_exact",
        "evaluation_kernel_root_independent_exact",
        "evaluation_range_root_independent_exact",
        "quotient_range_first_isomorphism_exact",
        "observational_equivalence_exact",
        "quotient_wilson_factorization_exact",
        "canonical_ab_kernel_triviality_exact",
        "canonical_ba_observable_visibility_exact",
        "canonical_separator_survives_observable_quotient_exact",
        "source_confidence_preserved_exact",
        "no_new_confidence_penalty_introduced",
        "all_full_rank_transport_global_observable_quotient_layer_commutes",
        "singular_atomic_global_observable_quotient_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "global_observable_quotient_not_truth_authority",
        "kernel_review_not_candidate_pruning",
        "quotient_class_not_candidate_ranking",
        "observable_factorization_not_source_mutation",
        "future_only",
        "read_only",
    )
    for field in required_true:
        assert obs[field] is True, field

    required_false = (
        "universal_observable_moduli_classification_claimed",
        "continuum_character_variety_claimed",
        "physical_gauge_field_inference_claimed",
        "observable_quotient_used_as_truth",
        "kernel_membership_used_as_candidate_pruning",
        "quotient_class_used_as_candidate_ranking",
        "source_confidence_mutated",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v083_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    )
    for field in required_false:
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["claims"]["observable_kernel_normality_records"][0][
        "kernel_is_normal"
    ] = False
    assert_rejects(tampered, "claim_mismatch_observable_kernel_normality_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["observable_kernel_root_independence_records"][7][
        "kernel_subgroups_equal"
    ] = False
    assert_rejects(
        tampered, "claim_mismatch_observable_kernel_root_independence_records"
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["observable_first_isomorphism_records"][2][
        "quotient_range_mul_equivalence_exact"
    ] = False
    assert_rejects(tampered, "claim_mismatch_observable_first_isomorphism_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["observational_equivalence_records"][9][
        "ratio_in_kernel_iff_equal_evaluation"
    ] = False
    assert_rejects(tampered, "claim_mismatch_observational_equivalence_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["canonical_kernel_visibility_records"][1][
        "ordered_ba_visible_in_observable_quotient"
    ] = False
    assert_rejects(tampered, "claim_mismatch_canonical_kernel_visibility_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["source_confidence_preservation_records"][0][
        "global_observable_quotient_adjusted_confidence"
    ] = {"numerator": 1, "denominator": 2}
    assert_rejects(tampered, "claim_mismatch_source_confidence_preservation_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["global_observable_quotient_not_truth_authority"] = False
    assert_rejects(tampered, "claim_mismatch_global_observable_quotient_not_truth_authority")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_truth_claim"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_truth_claim")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v083_certificate"]["observables"][
        "canonical_section_group_separator_records"
    ][0]["ordered_ab_trace"] = 0
    assert_rejects(tampered, "source_memoryos_v083_certificate_digest_mismatch")

    print("MemoryOS v0.84 global observable kernel quotient checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
