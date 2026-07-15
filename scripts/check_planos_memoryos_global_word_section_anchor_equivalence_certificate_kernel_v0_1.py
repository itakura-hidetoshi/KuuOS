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
from runtime.kuuos_memoryos_global_word_section_anchor_equivalence_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_global_word_section_anchor_equivalence_certificate,
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
    result = issue_global_word_section_anchor_equivalence_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_global_word_section_anchor_equivalence_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_global_section_record_count": 6,
        "global_word_section_component_record_count": 160,
        "global_word_section_compatibility_record_count": 640,
        "anchor_reconstruction_record_count": 40,
        "anchor_fiber_equivalence_record_count": 4,
        "section_evaluation_descent_record_count": 640,
        "section_root_pair_wilson_record_count": 640,
        "canonical_global_section_separator_record_count": 4,
        "source_confidence_preservation_record_count": 4,
        "global_section_memory_fusion_record_count": 4,
        "full_rank_transport_global_section_record_count": 8,
        "singular_atomic_global_section_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    assert all(
        record["component_defined_by_direct_transport"]
        for record in obs["global_word_section_component_records"]
    )
    assert all(
        record["section_compatibility_exact"]
        for record in obs["global_word_section_compatibility_records"]
    )
    assert all(
        record["anchor_component_returns_original_word"]
        and record["section_reconstructed_from_anchor"]
        for record in obs["anchor_reconstruction_records"]
    )
    assert all(
        record["section_to_anchor_and_back_identity"]
        and record["anchor_to_section_and_back_identity"]
        and record["fiber_equivalence_exact"]
        for record in obs["anchor_fiber_equivalence_records"]
    )
    assert all(
        record["section_evaluation_equals_anchor_evaluation"]
        and record["section_wilson_equals_anchor_wilson"]
        for record in obs["section_evaluation_descent_records"]
    )
    assert all(
        record["root_pair_wilson_equal"]
        for record in obs["section_root_pair_wilson_records"]
    )

    separators = obs["canonical_global_section_separator_records"]
    assert [record["root_route_id"] for record in separators] == [
        "route-0", "route-1", "route-2", "route-3"
    ]
    assert all(record["ordered_ab_value"] == [0, 1, 2] for record in separators)
    assert all(record["ordered_ba_value"] == [2, 0, 1] for record in separators)
    assert all(record["ordered_ab_trace"] == 3 for record in separators)
    assert all(record["ordered_ba_trace"] == 0 for record in separators)
    assert all(record["global_section_separator_exact"] for record in separators)

    expected_confidence = {
        "flat_four_route_atlas": {"numerator": 1, "denominator": 3},
        "single_support_atlas": {"numerator": 5, "denominator": 18},
        "ordered_ab_atlas": {"numerator": 11, "denominator": 54},
        "ordered_ba_atlas": {"numerator": 11, "denominator": 54},
    }
    for record in obs["source_confidence_preservation_records"]:
        expected = expected_confidence[record["profile_id"]]
        assert record["source_normalized_groupoid_adjusted_confidence"] == expected
        assert record["global_section_adjusted_confidence"] == expected
        assert record["new_global_section_penalty"] == {
            "numerator": 0,
            "denominator": 1,
        }
        assert record["confidence_preserved_exactly"]

    required_true = (
        "source_memoryos_v081_exact",
        "finite_s3_global_word_section_exact",
        "global_section_compatibility_exact",
        "anchor_extension_exact",
        "anchor_reconstruction_exact",
        "anchor_fiber_equivalence_exact",
        "section_evaluation_root_independent_exact",
        "section_wilson_root_independent_exact",
        "canonical_global_section_separator_exact",
        "source_confidence_preserved_exact",
        "no_new_confidence_penalty_introduced",
        "all_full_rank_transport_global_section_layer_commutes",
        "singular_atomic_global_section_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "global_section_not_truth_authority",
        "section_descent_review_not_candidate_ranking",
        "anchor_selection_not_candidate_selection",
        "section_reconstruction_not_source_mutation",
        "future_only",
        "read_only",
    )
    for field in required_true:
        assert obs[field] is True, field

    required_false = (
        "universal_sheaf_classification_claimed",
        "universal_free_groupoid_presentation_claimed",
        "continuum_gauge_groupoid_claimed",
        "physical_gauge_field_inference_claimed",
        "global_section_used_as_truth",
        "global_section_used_as_candidate_ranking",
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
    tampered["claims"]["global_word_section_compatibility_records"][17][
        "section_compatibility_exact"
    ] = False
    assert_rejects(
        tampered, "claim_mismatch_global_word_section_compatibility_records"
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["anchor_fiber_equivalence_records"][2][
        "fiber_equivalence_exact"
    ] = False
    assert_rejects(tampered, "claim_mismatch_anchor_fiber_equivalence_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["section_evaluation_descent_records"][123][
        "section_wilson_equals_anchor_wilson"
    ] = False
    assert_rejects(tampered, "claim_mismatch_section_evaluation_descent_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["canonical_global_section_separator_records"][2][
        "ordered_ab_trace"
    ] = 0
    assert_rejects(
        tampered, "claim_mismatch_canonical_global_section_separator_records"
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["source_confidence_preservation_records"][0][
        "global_section_adjusted_confidence"
    ] = {"numerator": 1, "denominator": 2}
    assert_rejects(tampered, "claim_mismatch_source_confidence_preservation_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["global_section_not_truth_authority"] = False
    assert_rejects(tampered, "claim_mismatch_global_section_not_truth_authority")

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

    print("MemoryOS v0.82 global word-section anchor equivalence checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
