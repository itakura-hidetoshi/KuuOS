#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_rooted_route_atlas_nielsen_change_certificate_kernel_v0_1 import (
    issue_rooted_route_atlas_nielsen_change_certificate,
)
from runtime.kuuos_memoryos_free_group_mixed_wilson_word_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_free_group_mixed_wilson_word_certificate,
)
from scripts.check_planos_memoryos_rooted_route_atlas_nielsen_change_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v078_payload,
)


def source_memoryos_v078_certificate() -> dict[str, Any]:
    result = issue_rooted_route_atlas_nielsen_change_certificate(
        build_memoryos_v078_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v078 = source_memoryos_v078_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v078_certificate": source_v078,
        "claims": _derive_observables(source_v078),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_free_group_mixed_wilson_word_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_free_group_mixed_wilson_word_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_free_group_word_record_count": 6,
        "free_word_generator_record_count": 4,
        "canonical_free_word_record_count": 10,
        "nielsen_elementary_move_record_count": 3,
        "nielsen_generator_substitution_record_count": 4,
        "nielsen_word_involution_record_count": 10,
        "free_word_evaluation_record_count": 40,
        "nielsen_evaluation_compatibility_record_count": 40,
        "free_word_gauge_covariance_record_count": 40,
        "mixed_wilson_signature_record_count": 4,
        "order_separation_record_count": 2,
        "source_confidence_preservation_record_count": 4,
        "free_group_word_memory_fusion_record_count": 4,
        "full_rank_transport_free_group_word_record_count": 8,
        "singular_atomic_free_group_word_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    substitutions = {
        record["generator_id"]: record["substitution_word"]
        for record in obs["nielsen_generator_substitution_records"]
    }
    assert substitutions == {
        "cycle-01": [{"generator_id": "cycle-01", "exponent": -1}],
        "cycle-02": [
            {"generator_id": "cycle-01", "exponent": -1},
            {"generator_id": "cycle-02", "exponent": 1},
        ],
        "cycle-03": [
            {"generator_id": "cycle-01", "exponent": -1},
            {"generator_id": "cycle-03", "exponent": 1},
        ],
        "defect-0": [{"generator_id": "defect-0", "exponent": 1}],
    }
    assert all(
        record["returns_source_word"]
        for record in obs["nielsen_word_involution_records"]
    )
    assert all(
        record["nielsen_evaluation_compatible"]
        for record in obs["nielsen_evaluation_compatibility_records"]
    )
    assert all(
        record["word_evaluation_gauge_covariant"]
        and record["word_wilson_trace_gauge_invariant"]
        for record in obs["free_word_gauge_covariance_records"]
    )

    signatures = {
        record["profile_id"]: record["mixed_word_traces"]
        for record in obs["mixed_wilson_signature_records"]
    }
    assert signatures == {
        "flat_four_route_atlas": [0, 0, 0, 3],
        "single_support_atlas": [1, 0, 0, 3],
        "ordered_ab_atlas": [1, 1, 3, 0],
        "ordered_ba_atlas": [1, 1, 0, 0],
    }

    separation = obs["order_separation_records"]
    assert separation[0]["source_cycle_only_signatures_equal"]
    assert separation[0]["separator_word_id"] == "cycle-03-then-defect"
    assert separation[0]["ordered_ab_word_value"] == [0, 1, 2]
    assert separation[0]["ordered_ba_word_value"] == [2, 0, 1]
    assert separation[0]["ordered_ab_word_trace"] == 3
    assert separation[0]["ordered_ba_word_trace"] == 0
    assert separation[0]["gauge_invariant_mixed_word_separates"]
    assert separation[1]["exact_commutator_values_differ"]
    assert separation[1]["commutator_traces_equal"]
    assert separation[1]["single_commutator_class_trace_not_separator"]

    confidences = {
        record["profile_id"]: record
        for record in obs["source_confidence_preservation_records"]
    }
    expected_confidence = {
        "flat_four_route_atlas": {"numerator": 1, "denominator": 3},
        "single_support_atlas": {"numerator": 5, "denominator": 18},
        "ordered_ab_atlas": {"numerator": 11, "denominator": 54},
        "ordered_ba_atlas": {"numerator": 11, "denominator": 54},
    }
    for profile_id, expected in expected_confidence.items():
        record = confidences[profile_id]
        assert record["source_route_atlas_adjusted_confidence"] == expected
        assert record["free_group_word_adjusted_confidence"] == expected
        assert record["new_word_penalty"] == {"numerator": 0, "denominator": 1}
        assert record["confidence_preserved_exactly"]

    required_true = (
        "source_memoryos_v078_exact",
        "finite_s3_free_group_word_atlas_exact",
        "free_group_generator_assignment_exact",
        "nielsen_elementary_decomposition_exact",
        "nielsen_free_group_substitution_exact",
        "nielsen_free_group_involution_exact",
        "nielsen_evaluation_compatibility_exact",
        "arbitrary_word_gauge_covariance_exact",
        "arbitrary_word_wilson_gauge_invariant_exact",
        "cycle_only_class_signature_limit_preserved",
        "commutator_exact_representatives_retained",
        "commutator_class_trace_limit_recorded",
        "mixed_cycle_defect_word_separates_ordered_profiles_exact",
        "source_confidence_preserved_exact",
        "no_new_confidence_penalty_introduced",
        "all_full_rank_transport_free_group_word_layer_commutes",
        "singular_atomic_free_group_word_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "free_group_word_not_truth_authority",
        "mixed_word_review_not_candidate_ranking",
        "word_signature_not_candidate_selection",
        "free_word_expansion_not_source_deletion",
        "future_only",
        "read_only",
    )
    for field in required_true:
        assert obs[field] is True, field

    required_false = (
        "universal_free_group_classification_claimed",
        "universal_word_separator_claimed",
        "continuum_gauge_field_claimed",
        "physical_gauge_field_inference_claimed",
        "mixed_word_used_as_truth",
        "mixed_word_used_as_candidate_ranking",
        "source_confidence_mutated",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v078_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    )
    for field in required_false:
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["claims"]["nielsen_word_involution_records"][0][
        "returns_source_word"
    ] = False
    assert_rejects(tampered, "claim_mismatch_nielsen_word_involution_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["free_word_evaluation_records"][26][
        "permutation_trace"
    ] = 0
    assert_rejects(tampered, "claim_mismatch_free_word_evaluation_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["mixed_wilson_signature_records"][2][
        "mixed_word_traces"
    ] = [1, 1, 0, 0]
    assert_rejects(tampered, "claim_mismatch_mixed_wilson_signature_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["source_confidence_preservation_records"][0][
        "free_group_word_adjusted_confidence"
    ] = {"numerator": 1, "denominator": 2}
    assert_rejects(
        tampered, "claim_mismatch_source_confidence_preservation_records"
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["free_group_word_not_truth_authority"] = False
    assert_rejects(tampered, "claim_mismatch_free_group_word_not_truth_authority")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_truth_claim"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_truth_claim")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v078_certificate"]["observables"][
        "rooted_coordinate_atlas_records"
    ][0]["rooted_coordinates"][0] = [1, 0, 2]
    assert_rejects(
        tampered,
        "source_memoryos_v078_certificate_digest_mismatch",
    )

    print("MemoryOS v0.79 free-group mixed Wilson word checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
