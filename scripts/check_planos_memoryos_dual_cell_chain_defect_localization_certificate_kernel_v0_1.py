#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_dual_two_complex_stokes_certificate_kernel_v0_1 import (
    issue_dual_two_complex_stokes_certificate,
)
from runtime.kuuos_memoryos_dual_cell_chain_defect_localization_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_dual_cell_chain_defect_localization_certificate,
)
from scripts.check_planos_memoryos_dual_two_complex_stokes_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v074_payload,
)


def source_memoryos_v074_certificate() -> dict[str, Any]:
    result = issue_dual_two_complex_stokes_certificate(build_memoryos_v074_payload())
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v074 = source_memoryos_v074_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v074_certificate": source_v074,
        "claims": _derive_observables(source_v074),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_dual_cell_chain_defect_localization_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_dual_cell_chain_defect_localization_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_dual_cell_chain_record_count": 5,
        "dual_cell_chain_incidence_record_count": 7,
        "dual_cell_chain_profile_record_count": 4,
        "chain_seam_transport_record_count": 12,
        "localized_seam_defect_record_count": 12,
        "path_ordered_chain_composition_record_count": 4,
        "single_defect_localization_record_count": 1,
        "dual_cycle_holonomy_record_count": 2,
        "chain_boundary_wilson_record_count": 4,
        "chain_confidence_record_count": 4,
        "dual_cell_chain_memory_fusion_record_count": 4,
        "full_rank_transport_dual_cell_chain_record_count": 8,
        "singular_atomic_dual_cell_chain_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    profiles = obs["dual_cell_chain_profile_records"]
    assert [record["profile_id"] for record in profiles] == [
        "all_compatible_curved",
        "single_middle_mismatch_curved",
        "ordered_double_mismatch_ab",
        "ordered_double_mismatch_ba",
    ]
    assert profiles[0]["mismatch_indices"] == []
    assert profiles[1]["mismatch_indices"] == [1]
    assert profiles[2]["mismatch_indices"] == [0, 1]
    assert profiles[3]["mismatch_indices"] == [0, 1]

    compositions = obs["path_ordered_chain_composition_records"]
    boundaries = {
        record["profile_id"]: record["global_outer_boundary_holonomy"]
        for record in compositions
    }
    assert boundaries == {
        "all_compatible_curved": [0, 1, 2],
        "single_middle_mismatch_curved": [1, 2, 0],
        "ordered_double_mismatch_ab": [1, 2, 0],
        "ordered_double_mismatch_ba": [2, 0, 1],
    }
    assert compositions[0]["global_closure"]
    assert all(record["ordered_product_exact"] for record in compositions)

    localization = obs["single_defect_localization_records"]
    assert localization == [
        {
            "profile_id": "single_middle_mismatch_curved",
            "mismatch_index": 1,
            "preceding_path_transport": [1, 0, 2],
            "local_mismatch_defect": [2, 0, 1],
            "localized_mismatch_defect": [1, 2, 0],
            "global_outer_boundary_holonomy": [1, 2, 0],
            "global_equals_localized_mismatch": True,
            "conjugacy_class_preserved": True,
        }
    ]

    cycle = obs["dual_cycle_holonomy_records"]
    assert cycle[0]["closed_path"]
    assert cycle[1]["gauge_covariant"]
    assert cycle[1]["wilson_signature_invariant"]
    assert cycle[1]["cycle_holonomy"] == cycle[1]["expected_root_conjugate"]

    wilson = obs["chain_boundary_wilson_records"]
    assert [record["global_boundary_permutation_trace"] for record in wilson] == [
        3,
        0,
        0,
        0,
    ]
    assert all(record["frame_independent_class_signature"] for record in wilson)

    confidence = obs["chain_confidence_records"]
    assert confidence[0]["chain_defect_penalty"] == {
        "numerator": 0,
        "denominator": 1,
    }
    assert confidence[0]["chain_adjusted_confidence"] == {
        "numerator": 1,
        "denominator": 3,
    }
    for record in confidence[1:]:
        assert record["chain_defect_penalty"] == {
            "numerator": 1,
            "denominator": 6,
        }
        assert record["chain_adjusted_confidence"] == {
            "numerator": 1,
            "denominator": 6,
        }

    for field in (
        "source_memoryos_v074_exact",
        "finite_s3_dual_cell_chain_exact",
        "path_ordered_seam_transport_exact",
        "transported_local_defect_product_exact",
        "all_compatible_global_closure_exact",
        "single_mismatch_localization_exact",
        "single_mismatch_conjugacy_class_preserved",
        "multiple_mismatch_noncommutative_order_dependence_exact",
        "class_function_order_resolution_limit_recorded",
        "dual_cycle_holonomy_gauge_covariant_exact",
        "dual_cycle_wilson_gauge_invariant_exact",
        "chain_adjusted_confidence_exact",
        "all_full_rank_transport_dual_cell_chain_layer_commutes",
        "singular_atomic_dual_cell_chain_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "chain_defect_not_truth_authority",
        "chain_review_not_candidate_ranking",
        "path_transport_not_source_deletion",
        "future_only",
        "read_only",
    ):
        assert obs[field] is True, field

    for field in (
        "continuum_manifold_theorem_claimed",
        "universal_nonabelian_stokes_theorem_claimed",
        "physical_gauge_field_inference_claimed",
        "local_chain_component_used_as_truth",
        "chain_review_used_as_candidate_ranking",
        "source_record_deleted_by_chain_transport",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v074_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v074_certificate"]["certificate_digest"] = "0" * 64
    assert_rejects(tampered, "source_memoryos_v074_certificate_digest_mismatch")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["chain_seam_transport_records"][0]["seam_transport"] = [
        0,
        1,
        2,
    ]
    assert_rejects(tampered, "claim_mismatch_chain_seam_transport_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["localized_seam_defect_records"][4][
        "transported_seam_defect"
    ] = [2, 0, 1]
    assert_rejects(tampered, "claim_mismatch_localized_seam_defect_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["single_defect_localization_records"][0][
        "global_equals_localized_mismatch"
    ] = False
    assert_rejects(tampered, "claim_mismatch_single_defect_localization_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["path_ordered_chain_composition_records"][2][
        "global_outer_boundary_holonomy"
    ] = [2, 0, 1]
    assert_rejects(tampered, "claim_mismatch_path_ordered_chain_composition_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["chain_confidence_records"][1][
        "chain_adjusted_confidence"
    ] = {"numerator": 1, "denominator": 3}
    assert_rejects(tampered, "claim_mismatch_chain_confidence_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(tampered, "claim_mismatch_candidate_selection_performed")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_truth_claim"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_truth_claim")

    print(
        "PASS: MemoryOS v0.75 path-ordered dual-cell chains, single-defect "
        "localization, noncommutative mismatch ordering, and dual-cycle holonomy"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
