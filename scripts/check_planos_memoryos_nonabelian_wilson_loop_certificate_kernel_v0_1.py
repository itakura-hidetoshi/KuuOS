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

from runtime.kuuos_memoryos_gauge_connection_holonomy_certificate_kernel_v0_1 import (
    issue_gauge_connection_holonomy_certificate,
)
from runtime.kuuos_memoryos_nonabelian_wilson_loop_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_nonabelian_wilson_loop_certificate,
)
from scripts.check_planos_memoryos_gauge_connection_holonomy_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v071_payload,
)


def source_memoryos_v071_certificate() -> dict[str, Any]:
    result = issue_gauge_connection_holonomy_certificate(
        build_memoryos_v071_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v071 = source_memoryos_v071_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v071_certificate": source_v071,
        "claims": _derive_observables(source_v071),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_nonabelian_wilson_loop_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_nonabelian_wilson_loop_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_nonabelian_gauge_record_count": 5,
        "local_memory_chart_record_count": 3,
        "nonabelian_gauge_frame_record_count": 3,
        "nonabelian_link_record_count": 6,
        "gauge_transformed_nonabelian_link_record_count": 6,
        "path_ordered_transport_record_count": 4,
        "nonabelian_commutator_record_count": 2,
        "nonabelian_holonomy_record_count": 2,
        "holonomy_conjugacy_class_record_count": 2,
        "wilson_character_record_count": 2,
        "nonabelian_tree_gauge_record_count": 6,
        "multi_chart_fusion_record_count": 2,
        "nonabelian_gauge_adjusted_confidence_record_count": 2,
        "full_rank_transport_nonabelian_record_count": 8,
        "singular_atomic_nonabelian_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    commutators = obs["nonabelian_commutator_records"]
    assert commutators == [
        {
            "profile_id": "flat",
            "commutator": [0, 1, 2],
            "commutator_identity": True,
            "path_order_noncommutative": False,
        },
        {
            "profile_id": "nonabelian",
            "commutator": [1, 2, 0],
            "commutator_identity": False,
            "path_order_noncommutative": True,
        },
    ]

    holonomies = obs["nonabelian_holonomy_records"]
    assert holonomies == [
        {
            "profile_id": "flat",
            "holonomy": [0, 1, 2],
            "transformed_holonomy": [0, 1, 2],
            "holonomy_order": 1,
            "flat": True,
            "representative_changed": False,
            "gauge_covariant": True,
        },
        {
            "profile_id": "nonabelian",
            "holonomy": [1, 2, 0],
            "transformed_holonomy": [2, 0, 1],
            "holonomy_order": 3,
            "flat": False,
            "representative_changed": True,
            "gauge_covariant": True,
        },
    ]

    wilson = obs["wilson_character_records"]
    assert wilson == [
        {
            "profile_id": "flat",
            "permutation_representation_trace": 3,
            "transformed_trace": 3,
            "normalized_wilson_character": {"numerator": 1, "denominator": 1},
            "gauge_invariant": True,
            "class_function_only": True,
        },
        {
            "profile_id": "nonabelian",
            "permutation_representation_trace": 0,
            "transformed_trace": 0,
            "normalized_wilson_character": {"numerator": 0, "denominator": 1},
            "gauge_invariant": True,
            "class_function_only": True,
        },
    ]

    confidence = obs["nonabelian_gauge_adjusted_confidence_records"]
    assert confidence[0]["source_base_confidence"] == {"numerator": 2, "denominator": 3}
    assert confidence[0]["wilson_deficit_penalty"] == {"numerator": 0, "denominator": 1}
    assert confidence[0]["nonabelian_gauge_adjusted_confidence"] == {
        "numerator": 2,
        "denominator": 3,
    }
    assert confidence[1]["wilson_deficit_penalty"] == {
        "numerator": 1,
        "denominator": 6,
    }
    assert confidence[1]["nonabelian_gauge_adjusted_confidence"] == {
        "numerator": 1,
        "denominator": 2,
    }

    tree = obs["nonabelian_tree_gauge_records"]
    for profile_id in ("flat", "nonabelian"):
        records = [record for record in tree if record["profile_id"] == profile_id]
        assert [record["link_id"] for record in records] == ["ab", "bc", "ca"]
        assert all(record["exact"] for record in records)
        assert records[0]["tree_gauge_link"] == [0, 1, 2]
        assert records[1]["tree_gauge_link"] == [0, 1, 2]

    fusion = obs["multi_chart_fusion_records"]
    assert fusion[0]["fusion_consistent"]
    assert not fusion[0]["fusion_requires_review"]
    assert not fusion[1]["fusion_consistent"]
    assert fusion[1]["fusion_requires_review"]
    assert fusion[1]["fusion_signature"] == {
        "conjugacy_cycle_type": [3],
        "wilson_trace": 0,
        "holonomy_order": 3,
    }

    for field in (
        "source_memoryos_v071_exact",
        "finite_s3_nonabelian_connection_exact",
        "path_ordered_transport_exact",
        "canonical_path_order_noncommutative_exact",
        "nonabelian_commutator_exact",
        "holonomy_gauge_covariant_exact",
        "holonomy_representative_changes_under_gauge",
        "holonomy_conjugacy_class_invariant_exact",
        "wilson_character_gauge_invariant_exact",
        "tree_gauge_fixing_nonabelian_exact",
        "multi_chart_fusion_conjugacy_exact",
        "nonabelian_gauge_adjusted_confidence_exact",
        "all_full_rank_transport_nonabelian_layer_commutes",
        "singular_atomic_nonabelian_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "wilson_loop_not_truth_authority",
        "fusion_review_not_candidate_ranking",
        "tree_gauge_not_source_deletion",
        "future_only",
        "read_only",
    ):
        assert obs[field] is True, field

    for field in (
        "continuum_principal_bundle_claimed",
        "physical_su3_gauge_field_claimed",
        "universal_statistical_optimum_claimed",
        "local_link_component_used_as_truth",
        "fusion_review_used_as_candidate_ranking",
        "source_record_deleted_by_tree_gauge",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v071_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v071_certificate"]["certificate_digest"] = "0" * 64
    assert_rejects(
        tampered,
        "source_memoryos_v071_certificate_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["path_ordered_transport_records"][2][
        "ordered_transport"
    ] = [0, 1, 2]
    assert_rejects(tampered, "claim_mismatch_path_ordered_transport_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["nonabelian_holonomy_records"][1][
        "transformed_holonomy"
    ] = [1, 2, 0]
    assert_rejects(tampered, "claim_mismatch_nonabelian_holonomy_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["wilson_character_records"][1][
        "permutation_representation_trace"
    ] = 3
    assert_rejects(tampered, "claim_mismatch_wilson_character_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["nonabelian_gauge_adjusted_confidence_records"][1][
        "nonabelian_gauge_adjusted_confidence"
    ] = {"numerator": 2, "denominator": 3}
    assert_rejects(
        tampered,
        "claim_mismatch_nonabelian_gauge_adjusted_confidence_records",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(tampered, "claim_mismatch_candidate_selection_performed")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_truth_claim"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_truth_claim")

    print(
        json.dumps(
            {
                "accepted": result["accepted"],
                "schema_version": result["schema_version"],
                "certificate_digest": result["certificate_digest"],
                "counts": expected_counts,
                "nonabelian_holonomy": holonomies[1]["holonomy"],
                "transformed_holonomy": holonomies[1]["transformed_holonomy"],
                "wilson_trace": wilson[1]["permutation_representation_trace"],
                "adjusted_confidence": confidence[1][
                    "nonabelian_gauge_adjusted_confidence"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
