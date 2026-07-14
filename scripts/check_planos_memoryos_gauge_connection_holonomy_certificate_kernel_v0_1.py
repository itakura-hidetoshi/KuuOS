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

from runtime.kuuos_memoryos_collusion_correlation_weighted_cut_certificate_kernel_v0_1 import (
    issue_collusion_correlation_weighted_cut_certificate,
)
from runtime.kuuos_memoryos_gauge_connection_holonomy_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_gauge_connection_holonomy_certificate,
)
from scripts.check_planos_memoryos_collusion_correlation_weighted_cut_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v070_payload,
)


def source_memoryos_v070_certificate() -> dict[str, Any]:
    result = issue_collusion_correlation_weighted_cut_certificate(
        build_memoryos_v070_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v070 = source_memoryos_v070_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v070_certificate": source_v070,
        "claims": _derive_observables(source_v070),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_gauge_connection_holonomy_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_gauge_connection_holonomy_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_gauge_theory_record_count": 5,
        "local_memory_chart_record_count": 3,
        "gauge_parameter_record_count": 3,
        "connection_overlap_record_count": 6,
        "gauge_transformed_connection_record_count": 6,
        "holonomy_curvature_record_count": 2,
        "covariant_residual_record_count": 6,
        "tree_gauge_fixing_record_count": 3,
        "path_transport_holonomy_record_count": 2,
        "gauge_adjusted_confidence_record_count": 2,
        "full_rank_transport_gauge_record_count": 8,
        "singular_atomic_gauge_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    holonomy = obs["holonomy_curvature_records"]
    assert holonomy == [
        {
            "profile_id": "flat",
            "holonomy": {"numerator": 0, "denominator": 1},
            "transformed_holonomy": {"numerator": 0, "denominator": 1},
            "curvature_energy": {"numerator": 0, "denominator": 1},
            "flat": True,
            "curvature_flag_threshold": {"numerator": 1, "denominator": 2},
            "curvature_flagged": False,
            "gauge_invariant": True,
        },
        {
            "profile_id": "curved",
            "holonomy": {"numerator": 7, "denominator": 12},
            "transformed_holonomy": {"numerator": 7, "denominator": 12},
            "curvature_energy": {"numerator": 49, "denominator": 144},
            "flat": False,
            "curvature_flag_threshold": {"numerator": 1, "denominator": 2},
            "curvature_flagged": True,
            "gauge_invariant": True,
        },
    ]

    transformed = {
        (record["profile_id"], record["overlap_id"]): record[
            "transformed_connection_value"
        ]
        for record in obs["gauge_transformed_connection_records"]
    }
    assert transformed == {
        ("flat", "ab"): {"numerator": 1, "denominator": 30},
        ("flat", "bc"): {"numerator": 29, "denominator": 60},
        ("flat", "ca"): {"numerator": -31, "denominator": 60},
        ("curved", "ab"): {"numerator": 1, "denominator": 5},
        ("curved", "bc"): {"numerator": 17, "denominator": 30},
        ("curved", "ca"): {"numerator": -11, "denominator": 60},
    }

    residuals = {
        (record["profile_id"], record["overlap_id"]): record
        for record in obs["covariant_residual_records"]
    }
    for overlap in ("ab", "bc", "ca"):
        assert residuals[("flat", overlap)]["original_residual"] == {
            "numerator": 0,
            "denominator": 1,
        }
        assert residuals[("flat", overlap)]["gauge_invariant"]
    assert residuals[("curved", "ab")]["original_residual"] == {
        "numerator": 0,
        "denominator": 1,
    }
    assert residuals[("curved", "bc")]["original_residual"] == {
        "numerator": 0,
        "denominator": 1,
    }
    assert residuals[("curved", "ca")]["original_residual"] == {
        "numerator": -7,
        "denominator": 12,
    }
    assert all(record["gauge_invariant"] for record in residuals.values())

    assert obs["tree_gauge_fixing_records"] == [
        {
            "overlap_id": "ab",
            "tree_gauge_connection_value": {"numerator": 0, "denominator": 1},
            "expected_value": {"numerator": 0, "denominator": 1},
            "exact": True,
        },
        {
            "overlap_id": "bc",
            "tree_gauge_connection_value": {"numerator": 0, "denominator": 1},
            "expected_value": {"numerator": 0, "denominator": 1},
            "exact": True,
        },
        {
            "overlap_id": "ca",
            "tree_gauge_connection_value": {"numerator": 7, "denominator": 12},
            "expected_value": {"numerator": 7, "denominator": 12},
            "exact": True,
        },
    ]

    paths = {record["profile_id"]: record for record in obs["path_transport_holonomy_records"]}
    assert paths["flat"]["path_difference"] == {"numerator": 0, "denominator": 1}
    assert paths["curved"]["path_difference"] == {"numerator": 7, "denominator": 12}
    assert all(record["equals_holonomy"] for record in paths.values())

    confidence = {
        record["profile_id"]: record
        for record in obs["gauge_adjusted_confidence_records"]
    }
    assert confidence["flat"]["gauge_invariant_curvature_penalty"] == {
        "numerator": 0,
        "denominator": 1,
    }
    assert confidence["flat"]["gauge_adjusted_confidence"] == {
        "numerator": 3,
        "denominator": 4,
    }
    assert confidence["curved"]["gauge_invariant_curvature_penalty"] == {
        "numerator": 1,
        "denominator": 12,
    }
    assert confidence["curved"]["gauge_adjusted_confidence"] == {
        "numerator": 2,
        "denominator": 3,
    }

    for field in (
        "source_memoryos_v070_exact",
        "local_gauge_chart_atlas_exact",
        "additive_connection_transform_exact",
        "holonomy_gauge_invariant_exact",
        "curvature_energy_exact",
        "flatness_exact",
        "covariant_residual_exact",
        "tree_gauge_fixing_exact",
        "path_dependence_holonomy_exact",
        "curvature_flag_gauge_invariant_exact",
        "gauge_adjusted_confidence_exact",
        "all_full_rank_transport_gauge_layer_commutes",
        "singular_atomic_gauge_layer_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "gauge_curvature_not_truth_authority",
        "gauge_flag_not_candidate_ranking",
        "gauge_fixing_not_source_deletion",
        "future_only",
        "read_only",
    ):
        assert obs[field] is True, field

    for field in (
        "non_abelian_holonomy_claimed",
        "continuum_principal_bundle_claimed",
        "frame_dependent_component_used_as_truth",
        "gauge_flag_used_as_candidate_ranking",
        "source_record_deleted_by_gauge_fixing",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v070_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v070_certificate"]["certificate_digest"] = "0" * 64
    assert_rejects(tampered, "source_memoryos_v070_certificate_digest_mismatch")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["connection_overlap_records"][3]["connection_value"] = {
        "numerator": 0,
        "denominator": 1,
    }
    assert_rejects(tampered, "claim_mismatch_connection_overlap_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["holonomy_curvature_records"][1]["holonomy"] = {
        "numerator": 0,
        "denominator": 1,
    }
    assert_rejects(tampered, "claim_mismatch_holonomy_curvature_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["covariant_residual_records"][5]["transformed_residual"] = {
        "numerator": 0,
        "denominator": 1,
    }
    assert_rejects(tampered, "claim_mismatch_covariant_residual_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["tree_gauge_fixing_records"][2][
        "tree_gauge_connection_value"
    ] = {"numerator": 0, "denominator": 1}
    assert_rejects(tampered, "claim_mismatch_tree_gauge_fixing_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["gauge_adjusted_confidence_records"][1][
        "gauge_adjusted_confidence"
    ] = {"numerator": 3, "denominator": 4}
    assert_rejects(tampered, "claim_mismatch_gauge_adjusted_confidence_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["non_abelian_holonomy_claimed"] = True
    assert_rejects(tampered, "claim_mismatch_non_abelian_holonomy_claimed")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(tampered, "claim_mismatch_candidate_selection_performed")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_gauge_truth_claim"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_gauge_truth_claim")

    print(
        json.dumps(
            {
                "accepted": result["accepted"],
                "schema_version": result["schema_version"],
                "certificate_digest": result["certificate_digest"],
                "counts": expected_counts,
                "curved_holonomy": holonomy[1]["holonomy"],
                "curved_gauge_adjusted_confidence": confidence["curved"][
                    "gauge_adjusted_confidence"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
