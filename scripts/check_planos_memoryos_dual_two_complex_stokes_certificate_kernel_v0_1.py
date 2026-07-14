#!/usr/bin/env python3
from __future__ import annotations

import copy
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_tetrahedral_bianchi_curvature_certificate_kernel_v0_1 import (
    issue_tetrahedral_bianchi_curvature_certificate,
)
from runtime.kuuos_memoryos_dual_two_complex_stokes_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_dual_two_complex_stokes_certificate,
)
from scripts.check_planos_memoryos_tetrahedral_bianchi_curvature_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v073_payload,
)


def source_memoryos_v073_certificate() -> dict[str, Any]:
    result = issue_tetrahedral_bianchi_curvature_certificate(
        build_memoryos_v073_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v073 = source_memoryos_v073_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v073_certificate": source_v073,
        "claims": _derive_observables(source_v073),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_dual_two_complex_stokes_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_dual_two_complex_stokes_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_dual_complex_stokes_record_count": 5,
        "dual_two_complex_incidence_record_count": 3,
        "glued_tetrahedral_cell_record_count": 4,
        "shared_face_holonomy_record_count": 4,
        "dual_edge_transport_record_count": 2,
        "shared_face_gluing_record_count": 2,
        "lattice_stokes_composition_record_count": 2,
        "cell_bianchi_defect_propagation_record_count": 2,
        "dual_boundary_wilson_record_count": 2,
        "dual_complex_confidence_record_count": 2,
        "dual_complex_memory_fusion_record_count": 2,
        "full_rank_transport_dual_complex_record_count": 8,
        "singular_atomic_dual_complex_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    gluing = obs["shared_face_gluing_records"]
    assert gluing == [
        {
            "profile_id": "compatible_curved",
            "left_shared_face": [1, 2, 0],
            "right_shared_face": [1, 2, 0],
            "transported_right_shared_face": [2, 0, 1],
            "inverse_orientation_match": True,
            "seam_gluing_defect": [0, 1, 2],
            "transformed_seam_gluing_defect": [0, 1, 2],
            "seam_defect_cycle_type": [1, 1, 1],
            "gauge_covariant": True,
        },
        {
            "profile_id": "mismatched_curved",
            "left_shared_face": [1, 2, 0],
            "right_shared_face": [1, 2, 0],
            "transported_right_shared_face": [1, 2, 0],
            "inverse_orientation_match": False,
            "seam_gluing_defect": [2, 0, 1],
            "transformed_seam_gluing_defect": [1, 2, 0],
            "seam_defect_cycle_type": [3],
            "gauge_covariant": True,
        },
    ]

    stokes = obs["lattice_stokes_composition_records"]
    assert stokes[0]["glued_outer_boundary_holonomy"] == [0, 1, 2]
    assert stokes[0]["shared_face_cancelled"]
    assert stokes[0]["lattice_stokes_closed"]
    assert stokes[1]["glued_outer_boundary_holonomy"] == [2, 0, 1]
    assert not stokes[1]["shared_face_cancelled"]
    assert not stokes[1]["lattice_stokes_closed"]

    propagation = obs["cell_bianchi_defect_propagation_records"]
    assert all(record["local_left_bianchi_defect"] == [0, 1, 2] for record in propagation)
    assert all(record["local_right_bianchi_defect"] == [0, 1, 2] for record in propagation)
    assert all(record["outer_boundary_equals_seam_defect"] for record in propagation)
    assert propagation[1]["seam_gluing_defect"] == [2, 0, 1]
    assert propagation[1]["glued_outer_boundary_holonomy"] == [2, 0, 1]

    wilson = obs["dual_boundary_wilson_records"]
    assert [record["glued_boundary_permutation_trace"] for record in wilson] == [3, 0]
    assert all(record["gauge_invariant"] for record in wilson)

    confidence = obs["dual_complex_confidence_records"]
    assert confidence[0]["source_base_confidence"] == {"numerator": 1, "denominator": 3}
    assert confidence[0]["dual_complex_gluing_penalty"] == {"numerator": 0, "denominator": 1}
    assert confidence[0]["dual_complex_adjusted_confidence"] == {
        "numerator": 1,
        "denominator": 3,
    }
    assert confidence[1]["dual_complex_gluing_penalty"] == {
        "numerator": 1,
        "denominator": 6,
    }
    assert confidence[1]["dual_complex_adjusted_confidence"] == {
        "numerator": 1,
        "denominator": 6,
    }

    for field in (
        "source_memoryos_v073_exact",
        "finite_s3_dual_two_complex_exact",
        "shared_face_opposite_orientation_gluing_exact",
        "lattice_stokes_composition_exact",
        "cell_bianchi_defect_propagation_exact",
        "seam_mismatch_detected_exact",
        "dual_boundary_wilson_gauge_invariant_exact",
        "dual_complex_adjusted_confidence_exact",
        "all_full_rank_transport_dual_complex_layer_commutes",
        "singular_atomic_dual_complex_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "gluing_defect_not_truth_authority",
        "stokes_review_not_candidate_ranking",
        "dual_gauge_transport_not_source_deletion",
        "future_only",
        "read_only",
    ):
        assert obs[field] is True, field

    for field in (
        "continuum_dual_complex_claimed",
        "physical_nonabelian_stokes_action_claimed",
        "universal_cell_complex_bianchi_claimed",
        "local_seam_component_used_as_truth",
        "stokes_review_used_as_candidate_ranking",
        "source_record_deleted_by_dual_gauge",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v073_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v073_certificate"]["certificate_digest"] = "0" * 64
    assert_rejects(
        tampered,
        "source_memoryos_v073_certificate_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["dual_edge_transport_records"][0]["seam_transport"] = [0, 1, 2]
    assert_rejects(tampered, "claim_mismatch_dual_edge_transport_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["cell_bianchi_defect_propagation_records"][1][
        "glued_outer_boundary_holonomy"
    ] = [0, 1, 2]
    assert_rejects(
        tampered,
        "claim_mismatch_cell_bianchi_defect_propagation_records",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["shared_face_gluing_records"][1][
        "inverse_orientation_match"
    ] = True
    assert_rejects(tampered, "claim_mismatch_shared_face_gluing_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["dual_complex_confidence_records"][1][
        "dual_complex_adjusted_confidence"
    ] = {"numerator": 1, "denominator": 3}
    assert_rejects(tampered, "claim_mismatch_dual_complex_confidence_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(tampered, "claim_mismatch_candidate_selection_performed")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_truth_claim"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_truth_claim")

    print(
        "PASS: MemoryOS v0.74 dual 2-complex shared-face gluing, "
        "lattice Stokes composition, and Bianchi-defect propagation"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
