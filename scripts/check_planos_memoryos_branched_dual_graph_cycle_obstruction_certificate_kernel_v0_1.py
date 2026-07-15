#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_dual_cell_chain_defect_localization_certificate_kernel_v0_1 import (
    issue_dual_cell_chain_defect_localization_certificate,
)
from runtime.kuuos_memoryos_branched_dual_graph_cycle_obstruction_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_branched_dual_graph_cycle_obstruction_certificate,
)
from scripts.check_planos_memoryos_dual_cell_chain_defect_localization_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v075_payload,
)


def source_memoryos_v075_certificate() -> dict[str, Any]:
    result = issue_dual_cell_chain_defect_localization_certificate(
        build_memoryos_v075_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v075 = source_memoryos_v075_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v075_certificate": source_v075,
        "claims": _derive_observables(source_v075),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_branched_dual_graph_cycle_obstruction_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_branched_dual_graph_cycle_obstruction_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_branched_dual_graph_record_count": 5,
        "branched_dual_graph_incidence_record_count": 8,
        "branched_dual_graph_profile_record_count": 2,
        "branched_edge_transport_record_count": 8,
        "spanning_tree_route_record_count": 2,
        "alternative_path_comparison_record_count": 2,
        "cycle_obstruction_record_count": 2,
        "target_defect_routing_record_count": 4,
        "route_conjugacy_relation_record_count": 2,
        "route_wilson_signature_record_count": 4,
        "cycle_wilson_signature_record_count": 2,
        "branched_graph_confidence_record_count": 2,
        "branched_graph_memory_fusion_record_count": 2,
        "full_rank_transport_branched_graph_record_count": 8,
        "singular_atomic_branched_graph_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    profiles = obs["branched_dual_graph_profile_records"]
    assert [record["profile_id"] for record in profiles] == [
        "flat_diamond",
        "cycle_obstructed_diamond",
    ]
    assert profiles[0]["paths_agree"]
    assert not profiles[0]["cycle_obstructed"]
    assert not profiles[1]["paths_agree"]
    assert profiles[1]["cycle_obstructed"]

    path_records = obs["alternative_path_comparison_records"]
    assert path_records == [
        {
            "profile_id": "flat_diamond",
            "upper_path_transport": [1, 2, 0],
            "lower_path_transport": [1, 2, 0],
            "paths_agree": True,
            "path_agreement_iff_cycle_identity": True,
        },
        {
            "profile_id": "cycle_obstructed_diamond",
            "upper_path_transport": [0, 1, 2],
            "lower_path_transport": [1, 0, 2],
            "paths_agree": False,
            "path_agreement_iff_cycle_identity": True,
        },
    ]

    cycle_records = obs["cycle_obstruction_records"]
    assert cycle_records[0]["cycle_obstruction"] == [0, 1, 2]
    assert cycle_records[1]["cycle_obstruction"] == [1, 0, 2]
    assert all(record["gauge_covariant"] for record in cycle_records)
    assert all(
        record["transformed_cycle_obstruction"] == record["expected_root_conjugate"]
        for record in cycle_records
    )

    routing = obs["target_defect_routing_records"]
    obstructed = [
        record for record in routing
        if record["profile_id"] == "cycle_obstructed_diamond"
    ]
    assert [record["root_localized_defect"] for record in obstructed] == [
        [2, 0, 1],
        [1, 2, 0],
    ]
    assert obstructed[0]["root_localized_defect"] != obstructed[1][
        "root_localized_defect"
    ]

    relations = obs["route_conjugacy_relation_records"]
    assert all(
        record["upper_equals_cycle_conjugated_lower"] for record in relations
    )
    assert relations[0]["exact_route_representatives_equal"]
    assert not relations[1]["exact_route_representatives_equal"]
    assert all(
        record["class_function_route_signatures_equal"] for record in relations
    )

    route_wilson = obs["route_wilson_signature_records"]
    assert [record["localized_defect_trace"] for record in route_wilson] == [
        0,
        0,
        0,
        0,
    ]
    assert all(record["frame_independent"] for record in route_wilson)

    cycle_wilson = obs["cycle_wilson_signature_records"]
    assert [record["cycle_permutation_trace"] for record in cycle_wilson] == [3, 1]
    assert all(record["cycle_signature_gauge_invariant"] for record in cycle_wilson)

    confidence = obs["branched_graph_confidence_records"]
    assert confidence[0]["route_obstruction_penalty"] == {
        "numerator": 0,
        "denominator": 1,
    }
    assert confidence[0]["branched_graph_adjusted_confidence"] == {
        "numerator": 1,
        "denominator": 3,
    }
    assert confidence[1]["route_obstruction_penalty"] == {
        "numerator": 1,
        "denominator": 9,
    }
    assert confidence[1]["branched_graph_adjusted_confidence"] == {
        "numerator": 2,
        "denominator": 9,
    }

    for field in (
        "source_memoryos_v075_exact",
        "finite_s3_branched_dual_graph_exact",
        "diamond_incidence_exact",
        "spanning_tree_transport_exact",
        "alternative_path_comparison_exact",
        "path_agreement_iff_cycle_identity_exact",
        "cycle_obstruction_gauge_covariant_exact",
        "target_defect_route_relation_exact",
        "route_wilson_conjugacy_invariant_exact",
        "cycle_wilson_gauge_invariant_exact",
        "route_obstruction_confidence_exact",
        "all_full_rank_transport_branched_graph_layer_commutes",
        "singular_atomic_branched_graph_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "cycle_obstruction_not_truth_authority",
        "route_review_not_candidate_ranking",
        "spanning_tree_not_source_deletion",
        "future_only",
        "read_only",
    ):
        assert obs[field] is True, field

    for field in (
        "continuum_dual_graph_claimed",
        "universal_route_independence_claimed",
        "physical_gauge_field_inference_claimed",
        "local_route_component_used_as_truth",
        "route_review_used_as_candidate_ranking",
        "source_record_deleted_by_spanning_tree",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v075_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v075_certificate"]["certificate_digest"] = "0" * 64
    assert_rejects(
        tampered,
        "source_memoryos_v075_certificate_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["branched_edge_transport_records"][6][
        "seam_transport"
    ] = [0, 1, 2]
    assert_rejects(tampered, "claim_mismatch_branched_edge_transport_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["alternative_path_comparison_records"][1][
        "paths_agree"
    ] = True
    assert_rejects(
        tampered,
        "claim_mismatch_alternative_path_comparison_records",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["cycle_obstruction_records"][1][
        "cycle_obstruction"
    ] = [0, 1, 2]
    assert_rejects(tampered, "claim_mismatch_cycle_obstruction_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["target_defect_routing_records"][3][
        "root_localized_defect"
    ] = [2, 0, 1]
    assert_rejects(tampered, "claim_mismatch_target_defect_routing_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["route_conjugacy_relation_records"][1][
        "exact_route_representatives_equal"
    ] = True
    assert_rejects(
        tampered,
        "claim_mismatch_route_conjugacy_relation_records",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["branched_graph_confidence_records"][1][
        "branched_graph_adjusted_confidence"
    ] = {"numerator": 1, "denominator": 3}
    assert_rejects(tampered, "claim_mismatch_branched_graph_confidence_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(tampered, "claim_mismatch_candidate_selection_performed")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_truth_claim"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_truth_claim")

    print(
        "PASS: MemoryOS v0.76 branched dual diamond, spanning-tree and "
        "alternative-route comparison, cycle obstruction, and routed-defect "
        "conjugacy localization"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
