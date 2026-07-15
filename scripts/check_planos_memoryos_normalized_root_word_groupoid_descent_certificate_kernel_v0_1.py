#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_all_root_chart_defect_aware_word_transport_certificate_kernel_v0_1 import (
    issue_all_root_chart_defect_aware_word_transport_certificate,
)
from runtime.kuuos_memoryos_normalized_root_word_groupoid_descent_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_normalized_root_word_groupoid_descent_certificate,
)
from scripts.check_planos_memoryos_all_root_chart_defect_aware_word_transport_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v080_payload,
)


def source_memoryos_v080_certificate() -> dict[str, Any]:
    result = issue_all_root_chart_defect_aware_word_transport_certificate(
        build_memoryos_v080_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v080 = source_memoryos_v080_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v080_certificate": source_v080,
        "claims": _derive_observables(source_v080),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_normalized_root_word_groupoid_descent_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_normalized_root_word_groupoid_descent_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_normalized_groupoid_record_count": 6,
        "normalized_route_slot_record_count": 12,
        "normalized_root_chart_record_count": 16,
        "normalized_root_coordinate_record_count": 48,
        "normalized_root_defect_record_count": 16,
        "normalized_transition_substitution_record_count": 64,
        "normalized_transition_identity_record_count": 16,
        "normalized_transition_composition_record_count": 256,
        "normalized_transition_inverse_record_count": 64,
        "normalized_transition_evaluation_compatibility_record_count": 640,
        "normalized_transport_path_independence_record_count": 256,
        "normalized_word_gauge_covariance_record_count": 160,
        "normalized_mixed_separator_record_count": 4,
        "source_confidence_preservation_record_count": 4,
        "normalized_groupoid_memory_fusion_record_count": 4,
        "full_rank_transport_normalized_groupoid_record_count": 8,
        "singular_atomic_normalized_groupoid_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    slot_rows = {
        (record["root_route_id"], record["slot_id"]): record["physical_route_id"]
        for record in obs["normalized_route_slot_records"]
    }
    assert slot_rows == {
        ("route-0", "slot-1"): "route-1",
        ("route-0", "slot-2"): "route-2",
        ("route-0", "slot-3"): "route-3",
        ("route-1", "slot-1"): "route-0",
        ("route-1", "slot-2"): "route-2",
        ("route-1", "slot-3"): "route-3",
        ("route-2", "slot-1"): "route-0",
        ("route-2", "slot-2"): "route-1",
        ("route-2", "slot-3"): "route-3",
        ("route-3", "slot-1"): "route-0",
        ("route-3", "slot-2"): "route-1",
        ("route-3", "slot-3"): "route-2",
    }
    assert all(
        record["self_coordinate_eliminated"]
        and record["source_root_coordinate_identity"]
        for record in obs["normalized_root_chart_records"]
    )

    substitutions = {
        (
            record["source_root_route_id"],
            record["target_root_route_id"],
            record["generator_id"],
        ): record["substitution_word"]
        for record in obs["normalized_transition_substitution_records"]
    }
    assert substitutions[("route-0", "route-2", "slot-3")] == [
        {"generator_id": "slot-2", "exponent": -1},
        {"generator_id": "slot-3", "exponent": 1},
    ]
    assert substitutions[("route-0", "route-2", "defect")] == [
        {"generator_id": "slot-2", "exponent": -1},
        {"generator_id": "defect", "exponent": 1},
        {"generator_id": "slot-2", "exponent": 1},
    ]
    assert substitutions[("route-2", "route-0", "slot-1")] == [
        {"generator_id": "slot-1", "exponent": -1},
        {"generator_id": "slot-2", "exponent": 1},
    ]

    assert all(
        record["identity_exact"]
        for record in obs["normalized_transition_identity_records"]
    )
    assert all(
        record["pair_groupoid_composition_exact"]
        for record in obs["normalized_transition_composition_records"]
    )
    assert all(
        record["inverse_transition_exact"]
        for record in obs["normalized_transition_inverse_records"]
    )
    assert all(
        record["transition_evaluation_compatible"]
        and record["transition_wilson_trace_compatible"]
        for record in obs["normalized_transition_evaluation_compatibility_records"]
    )
    assert all(
        record["transport_path_independent"]
        for record in obs["normalized_transport_path_independence_records"]
    )
    assert all(
        record["word_evaluation_gauge_covariant"]
        and record["word_wilson_trace_gauge_invariant"]
        for record in obs["normalized_word_gauge_covariance_records"]
    )

    separators = obs["normalized_mixed_separator_records"]
    assert [record["source_root_route_id"] for record in separators] == [
        "route-0", "route-1", "route-2", "route-3"
    ]
    assert all(record["ordered_ab_value"] == [0, 1, 2] for record in separators)
    assert all(record["ordered_ba_value"] == [2, 0, 1] for record in separators)
    assert all(record["ordered_ab_trace"] == 3 for record in separators)
    assert all(record["ordered_ba_trace"] == 0 for record in separators)
    assert all(record["normalized_groupoid_separator_exact"] for record in separators)

    expected_confidence = {
        "flat_four_route_atlas": {"numerator": 1, "denominator": 3},
        "single_support_atlas": {"numerator": 5, "denominator": 18},
        "ordered_ab_atlas": {"numerator": 11, "denominator": 54},
        "ordered_ba_atlas": {"numerator": 11, "denominator": 54},
    }
    for record in obs["source_confidence_preservation_records"]:
        expected = expected_confidence[record["profile_id"]]
        assert record["source_all_root_chart_adjusted_confidence"] == expected
        assert record["normalized_groupoid_adjusted_confidence"] == expected
        assert record["new_groupoid_penalty"] == {"numerator": 0, "denominator": 1}
        assert record["confidence_preserved_exactly"]

    required_true = (
        "source_memoryos_v080_exact",
        "finite_s3_normalized_root_groupoid_exact",
        "self_coordinate_elimination_exact",
        "three_route_slots_per_root_exact",
        "normalized_pair_groupoid_identity_exact",
        "normalized_pair_groupoid_composition_exact",
        "normalized_pair_groupoid_inverse_exact",
        "normalized_transition_evaluation_compatibility_exact",
        "normalized_transport_path_independence_exact",
        "normalized_word_gauge_covariance_exact",
        "normalized_word_wilson_gauge_invariant_exact",
        "normalized_mixed_separator_root_independent_exact",
        "source_confidence_preserved_exact",
        "no_new_confidence_penalty_introduced",
        "all_full_rank_transport_normalized_groupoid_layer_commutes",
        "singular_atomic_normalized_groupoid_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "normalized_groupoid_not_truth_authority",
        "groupoid_descent_review_not_candidate_ranking",
        "root_slot_elimination_not_source_deletion",
        "wilson_descent_not_candidate_selection",
        "future_only",
        "read_only",
    )
    for field in required_true:
        assert obs[field] is True, field

    required_false = (
        "universal_free_groupoid_presentation_claimed",
        "universal_character_variety_classification_claimed",
        "continuum_gauge_groupoid_claimed",
        "physical_gauge_field_inference_claimed",
        "normalized_word_used_as_truth",
        "groupoid_signature_used_as_candidate_ranking",
        "source_confidence_mutated",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v080_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    )
    for field in required_false:
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["claims"]["normalized_transition_identity_records"][0][
        "identity_exact"
    ] = False
    assert_rejects(tampered, "claim_mismatch_normalized_transition_identity_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["normalized_transition_composition_records"][17][
        "pair_groupoid_composition_exact"
    ] = False
    assert_rejects(tampered, "claim_mismatch_normalized_transition_composition_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["normalized_transition_inverse_records"][7][
        "inverse_transition_exact"
    ] = False
    assert_rejects(tampered, "claim_mismatch_normalized_transition_inverse_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["normalized_transition_evaluation_compatibility_records"][123][
        "target_chart_value"
    ] = [9, 9, 9]
    assert_rejects(
        tampered,
        "claim_mismatch_normalized_transition_evaluation_compatibility_records",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["normalized_mixed_separator_records"][2][
        "ordered_ab_trace"
    ] = 0
    assert_rejects(tampered, "claim_mismatch_normalized_mixed_separator_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["source_confidence_preservation_records"][0][
        "normalized_groupoid_adjusted_confidence"
    ] = {"numerator": 1, "denominator": 2}
    assert_rejects(tampered, "claim_mismatch_source_confidence_preservation_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["normalized_groupoid_not_truth_authority"] = False
    assert_rejects(tampered, "claim_mismatch_normalized_groupoid_not_truth_authority")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_truth_claim"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_truth_claim")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v080_certificate"]["observables"][
        "transported_mixed_separator_records"
    ][0]["ordered_ab_trace"] = 0
    assert_rejects(
        tampered,
        "source_memoryos_v080_certificate_digest_mismatch",
    )

    print("MemoryOS v0.81 normalized root-word groupoid descent checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
