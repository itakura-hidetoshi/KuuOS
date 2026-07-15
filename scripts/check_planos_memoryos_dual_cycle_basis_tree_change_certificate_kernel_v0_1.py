#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_branched_dual_graph_cycle_obstruction_certificate_kernel_v0_1 import (
    issue_branched_dual_graph_cycle_obstruction_certificate,
)
from runtime.kuuos_memoryos_dual_cycle_basis_tree_change_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_dual_cycle_basis_tree_change_certificate,
)
from scripts.check_planos_memoryos_branched_dual_graph_cycle_obstruction_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v076_payload,
)


def source_memoryos_v076_certificate() -> dict[str, Any]:
    result = issue_branched_dual_graph_cycle_obstruction_certificate(
        build_memoryos_v076_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v076 = source_memoryos_v076_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v076_certificate": source_v076,
        "claims": _derive_observables(source_v076),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_dual_cycle_basis_tree_change_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_dual_cycle_basis_tree_change_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_theta_cycle_basis_record_count": 5,
        "theta_dual_graph_incidence_record_count": 11,
        "theta_dual_graph_profile_record_count": 3,
        "theta_edge_transport_record_count": 18,
        "theta_path_transport_record_count": 9,
        "fundamental_cycle_basis_record_count": 6,
        "pairwise_cycle_holonomy_record_count": 9,
        "spanning_tree_basis_change_record_count": 3,
        "cycle_basis_relation_record_count": 3,
        "theta_target_defect_routing_record_count": 9,
        "theta_route_conjugacy_relation_record_count": 9,
        "theta_route_wilson_signature_record_count": 9,
        "complete_pairwise_cycle_signature_record_count": 3,
        "theta_cycle_basis_confidence_record_count": 3,
        "theta_cycle_basis_memory_fusion_record_count": 3,
        "full_rank_transport_theta_cycle_basis_record_count": 8,
        "singular_atomic_theta_cycle_basis_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    profiles = obs["theta_dual_graph_profile_records"]
    assert [record["profile_id"] for record in profiles] == [
        "flat_theta",
        "rank_one_cycle_theta",
        "rank_two_noncommuting_theta",
    ]
    assert [record["cycle_rank"] for record in profiles] == [2, 2, 2]
    assert profiles[0]["all_paths_agree"]
    assert not profiles[1]["all_paths_agree"]
    assert not profiles[2]["all_paths_agree"]
    assert [record["independent_cycle_support"] for record in profiles] == [0, 1, 2]

    cycles = obs["pairwise_cycle_holonomy_records"]
    grouped_cycles = {
        profile_id: [
            record["cycle_holonomy"]
            for record in cycles
            if record["profile_id"] == profile_id
        ]
        for profile_id in (
            "flat_theta",
            "rank_one_cycle_theta",
            "rank_two_noncommuting_theta",
        )
    }
    assert grouped_cycles == {
        "flat_theta": [[0, 1, 2], [0, 1, 2], [0, 1, 2]],
        "rank_one_cycle_theta": [[1, 0, 2], [0, 1, 2], [1, 0, 2]],
        "rank_two_noncommuting_theta": [
            [1, 0, 2],
            [0, 2, 1],
            [1, 2, 0],
        ],
    }
    assert all(record["gauge_covariant"] for record in cycles)

    basis_changes = obs["spanning_tree_basis_change_records"]
    assert all(record["basis_change_exact"] for record in basis_changes)
    assert all(record["basis_change_gauge_covariant"] for record in basis_changes)
    rank_two_change = next(
        record
        for record in basis_changes
        if record["profile_id"] == "rank_two_noncommuting_theta"
    )
    assert rank_two_change["source_basis"] == [[1, 0, 2], [0, 2, 1]]
    assert rank_two_change["target_basis"] == [[1, 0, 2], [1, 2, 0]]
    assert rank_two_change["basis_change_rule"] == ["a^-1", "a^-1*b"]

    relations = obs["cycle_basis_relation_records"]
    assert all(
        record["cycle12_equals_cycle01_inverse_cycle02"]
        and record["cycle02_equals_cycle01_cycle12"]
        and record["all_paths_agree_iff_basis_identity"]
        for record in relations
    )

    routing_relations = obs["theta_route_conjugacy_relation_records"]
    assert all(
        record["left_equals_cycle_conjugated_right"]
        and record["class_function_route_signatures_equal"]
        for record in routing_relations
    )
    route_wilson = obs["theta_route_wilson_signature_records"]
    assert all(
        record["class_function_signature_equal_to_target"]
        and record["frame_independent"]
        for record in route_wilson
    )

    signatures = obs["complete_pairwise_cycle_signature_records"]
    assert [record["trace_sum"] for record in signatures] == [9, 5, 2]
    assert all(
        not record["spanning_tree_route_privileged"]
        and record["tree0_reconstructs_cycle12"]
        and record["tree1_reconstructs_cycle02"]
        and record["gauge_invariant_class_signature"]
        for record in signatures
    )

    confidence = obs["theta_cycle_basis_confidence_records"]
    assert [
        record["complete_pairwise_cycle_penalty"] for record in confidence
    ] == [
        {"numerator": 0, "denominator": 1},
        {"numerator": 2, "denominator": 27},
        {"numerator": 7, "denominator": 54},
    ]
    assert [record["theta_adjusted_confidence"] for record in confidence] == [
        {"numerator": 1, "denominator": 3},
        {"numerator": 7, "denominator": 27},
        {"numerator": 11, "denominator": 54},
    ]

    for field in (
        "source_memoryos_v076_exact",
        "finite_s3_theta_dual_graph_exact",
        "theta_cycle_rank_two_exact",
        "fundamental_cycle_basis_exact",
        "basis_change_nielsen_relation_exact",
        "basis_change_gauge_covariant_exact",
        "all_paths_agree_iff_basis_identity_exact",
        "complete_pairwise_cycle_signature_tree_independent_exact",
        "pairwise_cycle_wilson_gauge_invariant_exact",
        "target_defect_three_route_relation_exact",
        "route_wilson_conjugacy_invariant_exact",
        "noncommutative_basis_order_dependence_exact",
        "theta_adjusted_confidence_exact",
        "all_full_rank_transport_theta_cycle_basis_layer_commutes",
        "singular_atomic_theta_cycle_basis_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "cycle_basis_not_truth_authority",
        "basis_change_review_not_candidate_ranking",
        "spanning_tree_change_not_source_deletion",
        "future_only",
        "read_only",
    ):
        assert obs[field] is True, field

    for field in (
        "continuum_theta_graph_claimed",
        "universal_cycle_basis_theorem_claimed",
        "physical_gauge_field_inference_claimed",
        "local_cycle_basis_component_used_as_truth",
        "basis_change_review_used_as_candidate_ranking",
        "source_record_deleted_by_tree_change",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v076_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v076_certificate"]["certificate_digest"] = "0" * 64
    assert_rejects(tampered, "source_memoryos_v076_certificate_digest_mismatch")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["theta_edge_transport_records"][8]["seam_transport"] = [
        0,
        1,
        2,
    ]
    assert_rejects(tampered, "claim_mismatch_theta_edge_transport_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["pairwise_cycle_holonomy_records"][8][
        "cycle_holonomy"
    ] = [2, 0, 1]
    assert_rejects(tampered, "claim_mismatch_pairwise_cycle_holonomy_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["spanning_tree_basis_change_records"][2][
        "basis_change_exact"
    ] = False
    assert_rejects(tampered, "claim_mismatch_spanning_tree_basis_change_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["theta_route_conjugacy_relation_records"][6][
        "left_equals_cycle_conjugated_right"
    ] = False
    assert_rejects(
        tampered,
        "claim_mismatch_theta_route_conjugacy_relation_records",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["theta_cycle_basis_confidence_records"][2][
        "theta_adjusted_confidence"
    ] = {"numerator": 1, "denominator": 3}
    assert_rejects(tampered, "claim_mismatch_theta_cycle_basis_confidence_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(tampered, "claim_mismatch_candidate_selection_performed")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_truth_claim"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_truth_claim")

    print(
        "PASS: MemoryOS v0.77 theta dual graph, rank-two cycle bases, "
        "spanning-tree change covariance, and complete pairwise signatures"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
