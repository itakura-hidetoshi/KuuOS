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

from runtime.kuuos_memoryos_lineage_quotient_revocation_cut_certificate_kernel_v0_1 import (
    issue_lineage_quotient_revocation_cut_certificate,
)
from runtime.kuuos_memoryos_collusion_correlation_weighted_cut_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    issue_collusion_correlation_weighted_cut_certificate,
)
from scripts.check_planos_memoryos_lineage_quotient_revocation_cut_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v069_payload,
)


def source_memoryos_v069_certificate() -> dict[str, Any]:
    result = issue_lineage_quotient_revocation_cut_certificate(
        build_memoryos_v069_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v069 = source_memoryos_v069_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v069_certificate": source_v069,
        "claims": _derive_observables(source_v069),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_collusion_correlation_weighted_cut_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_collusion_correlation_weighted_cut_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_collusion_robustness_record_count": 5,
        "source_agent_record_count": 4,
        "collusion_pair_signal_record_count": 6,
        "suspected_collusion_pair_record_count": 1,
        "collusion_component_record_count": 3,
        "correlation_matrix_entry_record_count": 10,
        "effective_independent_source_count_record_count": 2,
        "robust_confidence_record_count": 1,
        "weighted_revocation_node_record_count": 6,
        "weighted_revocation_edge_record_count": 5,
        "weighted_revocation_path_record_count": 2,
        "weighted_revocation_cut_candidate_record_count": 32,
        "minimum_weighted_revocation_cut_record_count": 1,
        "full_rank_transport_collusion_robustness_record_count": 8,
        "singular_atomic_collusion_robustness_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    suspected = obs["suspected_collusion_pair_records"]
    assert [record["pair_id"] for record in suspected] == ["source-a::source-b"]
    assert suspected[0]["distinct_lineages"]
    assert suspected[0]["provenance_overlap"] == {
        "numerator": 3,
        "denominator": 4,
    }
    assert suspected[0]["behavioral_correlation"] == {
        "numerator": 7,
        "denominator": 8,
    }

    components = {
        tuple(record["source_ids"]): record
        for record in obs["collusion_component_records"]
    }
    assert set(components) == {
        ("source-a", "source-b"),
        ("source-c",),
        ("source-d",),
    }
    assert components[("source-a", "source-b")]["collusion_component"]
    assert not components[("source-a", "source-b")][
        "copies_counted_independently"
    ]

    effective = {
        record["profile_id"]: record["effective_independent_source_count"]
        for record in obs["effective_independent_source_count_records"]
    }
    assert effective == {
        "independent-baseline": {"numerator": 4, "denominator": 1},
        "observed-correlation": {"numerator": 32, "denominator": 11},
    }

    robust = obs["robust_confidence_records"]
    assert robust == [
        {
            "profile_id": "canonical-collusion-profile",
            "raw_source_count": 4,
            "collusion_component_count": 3,
            "raw_naive_confidence": {"numerator": 4, "denominator": 5},
            "component_capped_numerator": {"numerator": 9, "denominator": 4},
            "component_capped_confidence": {"numerator": 3, "denominator": 4},
            "confidence_inflation_removed": {"numerator": 1, "denominator": 20},
            "within_unit_interval": True,
            "collusive_component_weight_capped_at_one": True,
            "exact_rational": True,
        }
    ]

    minimum_cut = obs["minimum_weighted_revocation_cut_records"]
    assert minimum_cut == [
        {
            "cut_node_ids": ["legacy-branch-a", "legacy-branch-b"],
            "cut_cardinality": 2,
            "cut_weight": {"numerator": 2, "denominator": 1},
            "blocked_path_count": 2,
            "total_path_count": 2,
            "blocks_all_paths": True,
            "source_records_deleted": False,
            "minimum_weight": True,
            "unique_minimum_weight": True,
            "audit_history_preserved": True,
            "revocation_frontier_only": True,
        }
    ]

    hub_cut = next(
        record
        for record in obs["weighted_revocation_cut_candidate_records"]
        if record["cut_node_ids"] == ["legacy-hub"]
    )
    assert hub_cut["cut_cardinality"] == 1
    assert hub_cut["cut_weight"] == {"numerator": 3, "denominator": 1}
    assert hub_cut["blocks_all_paths"]

    for field in (
        "source_memoryos_v069_exact",
        "collusion_signal_fusion_exact",
        "distinct_lineage_collusion_detected_exact",
        "correlation_matrix_symmetric_exact",
        "effective_independent_source_count_exact",
        "positive_correlation_reduces_effective_count",
        "component_capped_robust_confidence_exact",
        "collusive_component_not_double_counted",
        "confidence_inflation_removed_exact",
        "minimum_weighted_revocation_cut_exact",
        "minimum_weight_cut_differs_from_minimum_cardinality_cut",
        "weighted_revocation_cut_preserves_audit_history",
        "all_full_rank_transport_collusion_robustness_commutes",
        "singular_atomic_collusion_robustness_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "collusion_detection_not_candidate_ranking",
        "robust_confidence_not_truth_authority",
        "weighted_cut_not_source_deletion",
        "future_only",
        "read_only",
    ):
        assert obs[field] is True, field

    for field in (
        "single_signal_collusion_claimed",
        "collusive_copies_counted_independently",
        "raw_source_count_used_as_effective_count",
        "minimum_cardinality_cut_claimed_weight_optimal",
        "source_record_deleted_by_weighted_cut",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v069_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v069_certificate"]["certificate_digest"] = "0" * 64
    assert_rejects(
        tampered,
        "source_memoryos_v069_certificate_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["suspected_collusion_pair_records"][0][
        "provenance_overlap"
    ] = {"numerator": 0, "denominator": 1}
    assert_rejects(tampered, "claim_mismatch_suspected_collusion_pair_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["effective_independent_source_count_records"][1][
        "effective_independent_source_count"
    ] = {"numerator": 4, "denominator": 1}
    assert_rejects(
        tampered,
        "claim_mismatch_effective_independent_source_count_records",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["robust_confidence_records"][0][
        "component_capped_confidence"
    ] = {"numerator": 4, "denominator": 5}
    assert_rejects(tampered, "claim_mismatch_robust_confidence_records")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["minimum_weighted_revocation_cut_records"][0][
        "cut_node_ids"
    ] = ["legacy-hub"]
    assert_rejects(
        tampered,
        "claim_mismatch_minimum_weighted_revocation_cut_records",
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
                "effective_independent_source_count": effective[
                    "observed-correlation"
                ],
                "robust_confidence": robust[0]["component_capped_confidence"],
                "minimum_weighted_cut": minimum_cut[0]["cut_node_ids"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
