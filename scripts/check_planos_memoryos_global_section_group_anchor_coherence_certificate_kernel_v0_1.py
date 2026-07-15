#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_global_word_cech_descent_certificate_kernel_v0_1 import (
    issue_global_word_cech_descent_certificate,
)
from runtime.kuuos_memoryos_global_section_group_anchor_coherence_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_global_section_group_anchor_coherence_certificate,
)
from scripts.check_planos_memoryos_global_word_cech_descent_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v082_payload,
)


def source_memoryos_v082_certificate() -> dict[str, Any]:
    result = issue_global_word_cech_descent_certificate(
        build_memoryos_v082_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v082 = source_memoryos_v082_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v082_certificate": source_v082,
        "claims": _derive_observables(source_v082),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_global_section_group_anchor_coherence_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_global_section_group_anchor_coherence_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_global_section_group_record_count": 6,
        "section_group_operation_record_count": 4,
        "anchor_fiber_mul_equivalence_record_count": 4,
        "anchor_transport_mul_equivalence_record_count": 16,
        "anchor_transport_coherence_record_count": 64,
        "anchor_extension_coherence_record_count": 16,
        "global_evaluation_homomorphism_record_count": 8,
        "global_evaluation_root_independence_record_count": 2,
        "canonical_section_group_separator_record_count": 4,
        "source_confidence_preservation_record_count": 4,
        "global_section_group_memory_fusion_record_count": 4,
        "full_rank_transport_global_section_group_record_count": 8,
        "singular_atomic_global_section_group_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    assert all(
        record["closed_on_compatible_sections"]
        and record["group_law_exact"]
        for record in obs["section_group_operation_records"]
    )
    assert all(
        record["anchor_evaluation_is_monoid_hom"]
        and record["anchor_extension_is_monoid_hom"]
        and record["evaluation_after_extension_identity"]
        and record["extension_after_evaluation_identity"]
        and record["anchor_fiber_mul_equivalence_exact"]
        for record in obs["anchor_fiber_mul_equivalence_records"]
    )
    assert all(
        record["forward_transport_is_monoid_hom"]
        and record["reverse_transport_is_inverse"]
        and record["fiber_mul_equivalence_exact"]
        for record in obs["anchor_transport_mul_equivalence_records"]
    )
    assert all(
        record["two_step_equals_direct"]
        and record["anchor_transport_coherence_exact"]
        for record in obs["anchor_transport_coherence_records"]
    )
    assert all(
        record["transport_then_extend_equals_direct_extension"]
        and record["anchor_extension_coherence_exact"]
        for record in obs["anchor_extension_coherence_records"]
    )
    assert all(
        record["evaluation_map_one_exact"]
        and record["evaluation_map_mul_exact"]
        and record["global_evaluation_homomorphism_exact"]
        for record in obs["global_evaluation_homomorphism_records"]
    )
    assert all(
        record["group_value_root_independent"]
        and record["wilson_root_independent"]
        and record["evaluation_hom_root_independent_exact"]
        for record in obs["global_evaluation_root_independence_records"]
    )

    separators = obs["canonical_section_group_separator_records"]
    assert [record["root_route_id"] for record in separators] == [
        "route-0", "route-1", "route-2", "route-3"
    ]
    assert all(record["ordered_ab_value"] == [0, 1, 2] for record in separators)
    assert all(record["ordered_ba_value"] == [2, 0, 1] for record in separators)
    assert all(record["ordered_ab_trace"] == 3 for record in separators)
    assert all(record["ordered_ba_trace"] == 0 for record in separators)
    assert all(record["section_group_separator_exact"] for record in separators)

    expected_confidence = {
        "flat_four_route_atlas": {"numerator": 1, "denominator": 3},
        "single_support_atlas": {"numerator": 5, "denominator": 18},
        "ordered_ab_atlas": {"numerator": 11, "denominator": 54},
        "ordered_ba_atlas": {"numerator": 11, "denominator": 54},
    }
    for record in obs["source_confidence_preservation_records"]:
        expected = expected_confidence[record["profile_id"]]
        assert (
            record["source_global_cech_descent_adjusted_confidence"]
            == expected
        )
        assert record["global_section_group_adjusted_confidence"] == expected
        assert record["new_section_group_penalty"] == {
            "numerator": 0,
            "denominator": 1,
        }
        assert record["confidence_preserved_exactly"]

    required_true = (
        "source_memoryos_v082_exact",
        "finite_global_section_group_exact",
        "compatible_sections_form_subgroup_exact",
        "anchor_evaluation_monoid_hom_exact",
        "anchor_extension_monoid_hom_exact",
        "anchor_fiber_mul_equivalence_exact",
        "anchor_transport_mul_equivalence_exact",
        "anchor_transport_coherence_exact",
        "anchor_extension_coherence_exact",
        "global_evaluation_homomorphism_exact",
        "global_evaluation_hom_root_independent_exact",
        "global_section_wilson_root_independent_exact",
        "canonical_section_group_separator_exact",
        "source_confidence_preserved_exact",
        "no_new_confidence_penalty_introduced",
        "all_full_rank_transport_global_section_group_layer_commutes",
        "singular_atomic_global_section_group_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "global_section_group_not_truth_authority",
        "section_group_review_not_candidate_ranking",
        "anchor_choice_not_candidate_selection",
        "group_completion_not_source_mutation",
        "future_only",
        "read_only",
    )
    for field in required_true:
        assert obs[field] is True, field

    required_false = (
        "universal_section_group_classification_claimed",
        "universal_sheaf_descent_claimed",
        "continuum_stack_claimed",
        "physical_gauge_field_inference_claimed",
        "global_section_group_used_as_truth",
        "anchor_equivalence_used_as_candidate_ranking",
        "source_confidence_mutated",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v082_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    )
    for field in required_false:
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["claims"]["section_group_operation_records"][1][
        "group_law_exact"
    ] = False
    assert_rejects(tampered, "claim_mismatch_section_group_operation_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["anchor_fiber_mul_equivalence_records"][2][
        "anchor_fiber_mul_equivalence_exact"
    ] = False
    assert_rejects(
        tampered, "claim_mismatch_anchor_fiber_mul_equivalence_records"
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["anchor_transport_coherence_records"][17][
        "two_step_equals_direct"
    ] = False
    assert_rejects(
        tampered, "claim_mismatch_anchor_transport_coherence_records"
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["global_evaluation_homomorphism_records"][0][
        "evaluation_map_mul_exact"
    ] = False
    assert_rejects(
        tampered, "claim_mismatch_global_evaluation_homomorphism_records"
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["canonical_section_group_separator_records"][2][
        "ordered_ab_trace"
    ] = 0
    assert_rejects(
        tampered, "claim_mismatch_canonical_section_group_separator_records"
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["source_confidence_preservation_records"][0][
        "global_section_group_adjusted_confidence"
    ] = {"numerator": 1, "denominator": 2}
    assert_rejects(
        tampered, "claim_mismatch_source_confidence_preservation_records"
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["global_section_group_not_truth_authority"] = False
    assert_rejects(
        tampered, "claim_mismatch_global_section_group_not_truth_authority"
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_truth_claim"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_truth_claim")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v082_certificate"]["observables"][
        "descent_mismatch_records"
    ][0]["mismatch_is_identity"] = False
    assert_rejects(
        tampered,
        "source_memoryos_v082_certificate_digest_mismatch",
    )

    print(
        "MemoryOS v0.83 global section group anchor coherence checks passed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
