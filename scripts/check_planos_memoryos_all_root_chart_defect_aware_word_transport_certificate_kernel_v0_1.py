#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_free_group_mixed_wilson_word_certificate_kernel_v0_1 import (
    issue_free_group_mixed_wilson_word_certificate,
)
from runtime.kuuos_memoryos_all_root_chart_defect_aware_word_transport_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_all_root_chart_defect_aware_word_transport_certificate,
)
from scripts.check_planos_memoryos_free_group_mixed_wilson_word_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v079_payload,
)


def source_memoryos_v079_certificate() -> dict[str, Any]:
    result = issue_free_group_mixed_wilson_word_certificate(
        build_memoryos_v079_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v079 = source_memoryos_v079_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v079_certificate": source_v079,
        "claims": _derive_observables(source_v079),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_all_root_chart_defect_aware_word_transport_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_all_root_chart_defect_aware_word_transport_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_all_root_chart_record_count": 6,
        "route_label_record_count": 4,
        "all_root_chart_record_count": 16,
        "root_chart_coordinate_record_count": 64,
        "root_chart_defect_record_count": 16,
        "root_chart_transition_record_count": 64,
        "root_chart_composition_record_count": 256,
        "root_chart_word_generator_record_count": 5,
        "canonical_root_chart_word_record_count": 10,
        "root_transition_substitution_record_count": 20,
        "root_transition_absorption_record_count": 16,
        "root_transition_evaluation_compatibility_record_count": 640,
        "root_chart_word_gauge_covariance_record_count": 160,
        "transported_mixed_separator_record_count": 4,
        "source_confidence_preservation_record_count": 4,
        "all_root_chart_memory_fusion_record_count": 4,
        "full_rank_transport_all_root_chart_record_count": 8,
        "singular_atomic_all_root_chart_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    assert [record["route_id"] for record in obs["route_label_records"]] == [
        "route-0", "route-1", "route-2", "route-3"
    ]
    assert all(
        record["root_coordinate_is_identity"]
        for record in obs["all_root_chart_records"]
    )
    assert all(
        record["direct_chart_equals_rebased_chart"]
        for record in obs["root_chart_transition_records"]
    )
    assert all(
        record["transition_composition_exact"]
        for record in obs["root_chart_composition_records"]
    )

    substitutions = {
        (record["target_root_route_id"], record["generator_id"]):
            record["substitution_word"]
        for record in obs["root_transition_substitution_records"]
    }
    assert substitutions[("route-2", "route-3")] == [
        {"generator_id": "route-2", "exponent": -1},
        {"generator_id": "route-3", "exponent": 1},
    ]
    assert substitutions[("route-2", "defect")] == [
        {"generator_id": "route-2", "exponent": -1},
        {"generator_id": "defect", "exponent": 1},
        {"generator_id": "route-2", "exponent": 1},
    ]
    assert all(
        record["first_after_second_equals_second"]
        for record in obs["root_transition_absorption_records"]
    )
    assert all(
        record["transition_evaluation_compatible"]
        and record["transition_wilson_trace_compatible"]
        for record in obs["root_transition_evaluation_compatibility_records"]
    )
    assert all(
        record["word_evaluation_gauge_covariant"]
        and record["word_wilson_trace_gauge_invariant"]
        for record in obs["root_chart_word_gauge_covariance_records"]
    )

    separators = obs["transported_mixed_separator_records"]
    assert [record["source_root_route_id"] for record in separators] == [
        "route-0", "route-1", "route-2", "route-3"
    ]
    assert all(record["ordered_ab_value"] == [0, 1, 2] for record in separators)
    assert all(record["ordered_ba_value"] == [2, 0, 1] for record in separators)
    assert all(record["ordered_ab_trace"] == 3 for record in separators)
    assert all(record["ordered_ba_trace"] == 0 for record in separators)
    assert all(record["root_independent_separator_exact"] for record in separators)

    chart_rows = {
        (record["profile_id"], record["root_route_id"]):
            record["all_route_mixed_traces"]
        for record in obs["all_root_chart_records"]
    }
    assert chart_rows[("ordered_ab_atlas", "route-0")] == [0, 1, 1, 3]
    assert chart_rows[("ordered_ab_atlas", "route-1")] == [1, 0, 3, 1]
    assert chart_rows[("ordered_ba_atlas", "route-2")] == [1, 3, 0, 1]
    assert chart_rows[("ordered_ba_atlas", "route-3")] == [3, 1, 1, 0]

    expected_confidence = {
        "flat_four_route_atlas": {"numerator": 1, "denominator": 3},
        "single_support_atlas": {"numerator": 5, "denominator": 18},
        "ordered_ab_atlas": {"numerator": 11, "denominator": 54},
        "ordered_ba_atlas": {"numerator": 11, "denominator": 54},
    }
    for record in obs["source_confidence_preservation_records"]:
        expected = expected_confidence[record["profile_id"]]
        assert record["source_free_group_word_adjusted_confidence"] == expected
        assert record["all_root_chart_adjusted_confidence"] == expected
        assert record["new_chart_penalty"] == {"numerator": 0, "denominator": 1}
        assert record["confidence_preserved_exactly"]

    required_true = (
        "source_memoryos_v079_exact",
        "finite_s3_all_root_chart_exact",
        "four_root_routes_complete",
        "root_chart_normalization_exact",
        "root_chart_coordinate_transition_exact",
        "root_chart_defect_transition_exact",
        "root_chart_transition_composition_exact",
        "root_transition_free_group_substitution_exact",
        "root_transition_absorption_exact",
        "root_transition_evaluation_compatibility_exact",
        "all_root_word_gauge_covariance_exact",
        "all_root_word_wilson_gauge_invariant_exact",
        "transported_mixed_separator_root_independent_exact",
        "source_confidence_preserved_exact",
        "no_new_confidence_penalty_introduced",
        "all_full_rank_transport_all_root_chart_layer_commutes",
        "singular_atomic_all_root_chart_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "all_root_chart_not_truth_authority",
        "root_transition_review_not_candidate_ranking",
        "transported_word_not_candidate_selection",
        "root_chart_expansion_not_source_deletion",
        "future_only",
        "read_only",
    )
    for field in required_true:
        assert obs[field] is True, field

    required_false = (
        "universal_character_variety_classification_claimed",
        "universal_root_word_separator_claimed",
        "continuum_gauge_groupoid_claimed",
        "physical_gauge_field_inference_claimed",
        "transported_separator_used_as_truth",
        "transported_separator_used_as_candidate_ranking",
        "source_confidence_mutated",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v079_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    )
    for field in required_false:
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["claims"]["root_chart_transition_records"][0][
        "defect_transition_exact"
    ] = False
    assert_rejects(tampered, "claim_mismatch_root_chart_transition_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["root_transition_absorption_records"][0][
        "first_after_second_equals_second"
    ] = False
    assert_rejects(tampered, "claim_mismatch_root_transition_absorption_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["transported_mixed_separator_records"][2][
        "ordered_ab_trace"
    ] = 0
    assert_rejects(tampered, "claim_mismatch_transported_mixed_separator_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["source_confidence_preservation_records"][0][
        "all_root_chart_adjusted_confidence"
    ] = {"numerator": 1, "denominator": 2}
    assert_rejects(tampered, "claim_mismatch_source_confidence_preservation_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["all_root_chart_not_truth_authority"] = False
    assert_rejects(tampered, "claim_mismatch_all_root_chart_not_truth_authority")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_truth_claim"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_truth_claim")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v079_certificate"]["observables"][
        "mixed_wilson_signature_records"
    ][2]["mixed_word_traces"] = [1, 1, 0, 0]
    assert_rejects(
        tampered,
        "source_memoryos_v079_certificate_digest_mismatch",
    )

    print("MemoryOS v0.80 all-root chart defect-aware word transport checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
