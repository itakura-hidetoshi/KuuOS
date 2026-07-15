#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_dual_cycle_basis_tree_change_certificate_kernel_v0_1 import (
    issue_dual_cycle_basis_tree_change_certificate,
)
from runtime.kuuos_memoryos_rooted_route_atlas_nielsen_change_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_rooted_route_atlas_nielsen_change_certificate,
)
from scripts.check_planos_memoryos_dual_cycle_basis_tree_change_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v077_payload,
)


def source_memoryos_v077_certificate() -> dict[str, Any]:
    result = issue_dual_cycle_basis_tree_change_certificate(
        build_memoryos_v077_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v077 = source_memoryos_v077_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v077_certificate": source_v077,
        "claims": _derive_observables(source_v077),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_rooted_route_atlas_nielsen_change_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_rooted_route_atlas_nielsen_change_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_rooted_route_atlas_record_count": 5,
        "rooted_route_atlas_incidence_record_count": 14,
        "rooted_route_atlas_profile_record_count": 4,
        "rooted_route_edge_transport_record_count": 32,
        "rooted_route_path_transport_record_count": 16,
        "rooted_coordinate_atlas_record_count": 8,
        "rooted_route_pairwise_cycle_record_count": 24,
        "rooted_nielsen_rebase_record_count": 4,
        "rooted_route_cocycle_relation_record_count": 4,
        "four_route_target_defect_routing_record_count": 16,
        "four_route_defect_relation_record_count": 12,
        "four_route_wilson_signature_record_count": 16,
        "complete_six_cycle_signature_record_count": 4,
        "rooted_route_atlas_confidence_record_count": 4,
        "rooted_route_atlas_memory_fusion_record_count": 4,
        "full_rank_transport_rooted_route_atlas_record_count": 8,
        "singular_atomic_rooted_route_atlas_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    profiles = obs["rooted_route_atlas_profile_records"]
    assert [record["profile_id"] for record in profiles] == [
        "flat_four_route_atlas",
        "single_support_atlas",
        "ordered_ab_atlas",
        "ordered_ba_atlas",
    ]
    assert all(record["cycle_rank"] == 3 for record in profiles)
    assert profiles[0]["all_paths_agree"]
    assert not any(record["all_paths_agree"] for record in profiles[1:])

    coordinates = {
        record["profile_id"]: record["rooted_coordinates"]
        for record in obs["rooted_coordinate_atlas_records"]
        if record["root_route_id"] == "route-0"
    }
    assert coordinates["flat_four_route_atlas"] == [
        [0, 1, 2], [0, 1, 2], [0, 1, 2]
    ]
    assert coordinates["single_support_atlas"] == [
        [1, 0, 2], [0, 1, 2], [0, 1, 2]
    ]
    assert coordinates["ordered_ab_atlas"] == [
        [1, 0, 2], [0, 2, 1], [2, 0, 1]
    ]
    assert coordinates["ordered_ba_atlas"] == [
        [0, 2, 1], [1, 0, 2], [1, 2, 0]
    ]
    assert coordinates["ordered_ab_atlas"] != coordinates["ordered_ba_atlas"]

    rebase = obs["rooted_nielsen_rebase_records"]
    assert all(record["rebase_exact"] for record in rebase)
    assert all(record["rebase_involutive"] for record in rebase)
    assert all(record["rebase_gauge_covariant"] for record in rebase)
    assert all(
        record["nielsen_rule"] == ["a^-1", "a^-1*b", "a^-1*c"]
        for record in rebase
    )

    relations = obs["rooted_route_cocycle_relation_records"]
    assert all(
        record["cycle12_equals_cycle01_inverse_cycle02"]
        and record["cycle13_equals_cycle01_inverse_cycle03"]
        and record["cycle23_equals_cycle02_inverse_cycle03"]
        and record["all_paths_agree_iff_root0_coordinates_identity"]
        for record in relations
    )

    signatures = {
        record["profile_id"]: record
        for record in obs["complete_six_cycle_signature_records"]
    }
    assert signatures["ordered_ab_atlas"]["complete_pairwise_cycle_traces"] == [
        1, 1, 0, 0, 1, 1
    ]
    assert signatures["ordered_ba_atlas"]["complete_pairwise_cycle_traces"] == [
        1, 1, 0, 0, 1, 1
    ]
    assert obs["mirrored_order_class_signature_limit_recorded"]
    assert obs["exact_order_representatives_retained"]
    assert obs["noncommutative_coordinate_order_exact"]

    confidences = {
        record["profile_id"]: record["route_atlas_adjusted_confidence"]
        for record in obs["rooted_route_atlas_confidence_records"]
    }
    assert confidences == {
        "flat_four_route_atlas": {"numerator": 1, "denominator": 3},
        "single_support_atlas": {"numerator": 5, "denominator": 18},
        "ordered_ab_atlas": {"numerator": 11, "denominator": 54},
        "ordered_ba_atlas": {"numerator": 11, "denominator": 54},
    }

    assert obs["finite_s3_four_route_atlas_exact"]
    assert obs["four_route_cycle_rank_three_exact"]
    assert obs["rooted_coordinate_atlas_exact"]
    assert obs["rooted_rebase_nielsen_exact"]
    assert obs["rooted_rebase_involutive_exact"]
    assert obs["rooted_rebase_gauge_covariant_exact"]
    assert obs["pairwise_cycle_reconstruction_exact"]
    assert obs["all_paths_agree_iff_root_coordinates_identity_exact"]
    assert obs["route_atlas_gauge_covariant_exact"]
    assert obs["target_defect_four_route_relation_exact"]
    assert obs["route_wilson_conjugacy_invariant_exact"]
    assert obs["complete_pairwise_signature_tree_independent_exact"]
    assert obs["route_atlas_adjusted_confidence_exact"]
    assert obs["all_full_rank_transport_rooted_route_atlas_layer_commutes"]
    assert obs["singular_atomic_rooted_route_atlas_layer_retained"]
    assert obs["rooted_route_atlas_not_truth_authority"]
    assert obs["root_change_review_not_candidate_ranking"]
    assert obs["root_route_not_privileged_authority"]
    assert obs["rooted_coordinates_not_source_deletion"]
    assert not obs["candidate_ranking_performed"]
    assert not obs["candidate_selection_performed"]
    assert not obs["decision_commit_performed"]
    assert not obs["activation_performed"]
    assert not obs["execution_permission"]
    assert not obs["persistent_world_state_mutated"]
    assert not obs["truth_authority_granted"]

    tampered = copy.deepcopy(payload)
    tampered["claims"]["rooted_coordinate_atlas_records"][2]["rooted_coordinates"][0] = [
        0, 1, 2
    ]
    assert_rejects(tampered, "claim_mismatch_rooted_coordinate_atlas_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["rooted_nielsen_rebase_records"][0]["rebase_involutive"] = False
    assert_rejects(tampered, "claim_mismatch_rooted_nielsen_rebase_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["complete_six_cycle_signature_records"][2][
        "complete_pairwise_cycle_traces"
    ] = [1, 1, 0, 1, 1, 0]
    assert_rejects(tampered, "claim_mismatch_complete_six_cycle_signature_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["rooted_route_atlas_confidence_records"][1][
        "route_atlas_adjusted_confidence"
    ] = {"numerator": 1, "denominator": 3}
    assert_rejects(tampered, "claim_mismatch_rooted_route_atlas_confidence_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["rooted_route_atlas_not_truth_authority"] = False
    assert_rejects(tampered, "claim_mismatch_rooted_route_atlas_not_truth_authority")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_truth_claim"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_truth_claim")

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v077_certificate"]["observables"][
        "theta_dual_graph_profile_records"
    ][0]["cycle_rank"] = 99
    assert_rejects(
        tampered,
        "source_memoryos_v077_certificate_digest_mismatch",
    )

    print("MemoryOS v0.78 rooted route atlas Nielsen change checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
