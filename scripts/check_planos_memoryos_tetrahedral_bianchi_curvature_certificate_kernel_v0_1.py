#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_nonabelian_wilson_loop_certificate_kernel_v0_1 import (
    issue_nonabelian_wilson_loop_certificate,
)
from runtime.kuuos_memoryos_tetrahedral_bianchi_curvature_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_tetrahedral_bianchi_curvature_certificate,
)
from scripts.check_planos_memoryos_nonabelian_wilson_loop_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v072_payload,
)


def source_memoryos_v072_certificate() -> dict[str, Any]:
    result = issue_nonabelian_wilson_loop_certificate(
        build_memoryos_v072_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v072 = source_memoryos_v072_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v072_certificate": source_v072,
        "claims": _derive_observables(source_v072),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_tetrahedral_bianchi_curvature_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_tetrahedral_bianchi_curvature_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_lattice_bianchi_record_count": 5,
        "tetrahedron_vertex_frame_record_count": 4,
        "oriented_edge_transport_record_count": 12,
        "gauge_transformed_edge_record_count": 12,
        "plaquette_holonomy_record_count": 8,
        "tetrahedral_bianchi_record_count": 2,
        "wilson_composition_record_count": 2,
        "curvature_action_record_count": 2,
        "tetrahedral_memory_fusion_record_count": 2,
        "full_rank_transport_bianchi_record_count": 8,
        "singular_atomic_bianchi_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    curved_faces = [
        record
        for record in obs["plaquette_holonomy_records"]
        if record["profile_id"] == "curved"
    ]
    assert [record["face_id"] for record in curved_faces] == [
        "012", "023", "031", "123"
    ]
    assert [record["plaquette_holonomy"] for record in curved_faces] == [
        [1, 2, 0],
        [1, 0, 2],
        [1, 0, 2],
        [2, 0, 1],
    ]
    assert [record["permutation_trace"] for record in curved_faces] == [0, 1, 1, 0]
    assert [record["identity_wilson_value"] for record in curved_faces] == [0, 0, 0, 0]
    assert all(record["gauge_covariant"] for record in curved_faces)
    assert all(record["identity_class_gauge_invariant"] for record in curved_faces)

    bianchi = obs["tetrahedral_bianchi_records"]
    assert bianchi == [
        {
            "profile_id": "flat",
            "ordered_face_product": [0, 1, 2],
            "transported_face_123": [0, 1, 2],
            "bianchi_defect": [0, 1, 2],
            "transformed_bianchi_defect": [0, 1, 2],
            "discrete_bianchi_exact": True,
            "defect_identity": True,
            "gauge_covariant": True,
        },
        {
            "profile_id": "curved",
            "ordered_face_product": [1, 2, 0],
            "transported_face_123": [1, 2, 0],
            "bianchi_defect": [0, 1, 2],
            "transformed_bianchi_defect": [0, 1, 2],
            "discrete_bianchi_exact": True,
            "defect_identity": True,
            "gauge_covariant": True,
        },
    ]

    composition = obs["wilson_composition_records"]
    assert composition[0]["ordered_product_identity_wilson"] == 3
    assert composition[0]["face_123_identity_wilson"] == 3
    assert composition[1]["ordered_product_identity_wilson"] == 0
    assert composition[1]["face_123_identity_wilson"] == 0
    assert all(record["conjugacy_class_match"] for record in composition)
    assert all(record["wilson_composition_exact"] for record in composition)

    curvature = obs["curvature_action_records"]
    assert curvature[0]["average_identity_class_curvature_action"] == {
        "numerator": 0,
        "denominator": 1,
    }
    assert curvature[0]["curvature_adjusted_confidence"] == {
        "numerator": 1,
        "denominator": 2,
    }
    assert curvature[1]["average_identity_class_curvature_action"] == {
        "numerator": 1,
        "denominator": 6,
    }
    assert curvature[1]["curvature_adjusted_confidence"] == {
        "numerator": 1,
        "denominator": 3,
    }
    assert all(record["gauge_invariant"] for record in curvature)
    assert all(record["within_unit_interval"] for record in curvature)
    assert all(not record["physical_yang_mills_action"] for record in curvature)

    fusion = obs["tetrahedral_memory_fusion_records"]
    assert not fusion[0]["requires_review"]
    assert fusion[1]["requires_review"]
    assert fusion[1]["plaquette_cycle_signature"] == [[3], [2, 1], [2, 1], [3]]
    assert fusion[1]["bianchi_defect_identity"]
    assert fusion[1]["curvature_action"] == {"numerator": 1, "denominator": 6}

    for field in (
        "source_memoryos_v072_exact",
        "finite_s3_tetrahedral_lattice_exact",
        "oriented_edge_transport_exact",
        "plaquette_holonomy_gauge_covariant_exact",
        "tetrahedral_discrete_bianchi_exact",
        "bianchi_defect_identity_exact",
        "wilson_composition_conjugacy_exact",
        "curvature_action_gauge_invariant_exact",
        "curvature_adjusted_confidence_exact",
        "all_full_rank_transport_bianchi_layer_commutes",
        "singular_atomic_bianchi_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "bianchi_defect_not_truth_authority",
        "curvature_action_not_candidate_ranking",
        "plaquette_gauge_fixing_not_source_deletion",
        "future_only",
        "read_only",
    ):
        assert obs[field] is True, field

    for field in (
        "continuum_lattice_gauge_field_claimed",
        "physical_yang_mills_action_claimed",
        "universal_nonabelian_bianchi_theorem_claimed",
        "local_plaquette_component_used_as_truth",
        "curvature_review_used_as_candidate_ranking",
        "source_record_deleted_by_plaquette_gauge",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v072_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v072_certificate"]["certificate_digest"] = "0" * 64
    assert_rejects(
        tampered,
        "source_memoryos_v072_certificate_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["plaquette_holonomy_records"][4][
        "plaquette_holonomy"
    ] = [0, 1, 2]
    assert_rejects(tampered, "claim_mismatch_plaquette_holonomy_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["tetrahedral_bianchi_records"][1][
        "bianchi_defect"
    ] = [1, 2, 0]
    assert_rejects(tampered, "claim_mismatch_tetrahedral_bianchi_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["wilson_composition_records"][1][
        "face_123_identity_wilson"
    ] = 3
    assert_rejects(tampered, "claim_mismatch_wilson_composition_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["curvature_action_records"][1][
        "curvature_adjusted_confidence"
    ] = {"numerator": 1, "denominator": 2}
    assert_rejects(tampered, "claim_mismatch_curvature_action_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["physical_yang_mills_action_claimed"] = True
    assert_rejects(tampered, "claim_mismatch_physical_yang_mills_action_claimed")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(tampered, "claim_mismatch_candidate_selection_performed")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected")

    print(
        json.dumps(
            {
                "status": "ok",
                "schema_version": result["schema_version"],
                "certificate_digest": result["certificate_digest"],
                "memoryos_frontier": "MemoryOS v0.73",
                "tetrahedral_discrete_bianchi_exact": obs[
                    "tetrahedral_discrete_bianchi_exact"
                ],
                "curved_curvature_action": curvature[1][
                    "average_identity_class_curvature_action"
                ],
                "curved_adjusted_confidence": curvature[1][
                    "curvature_adjusted_confidence"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
