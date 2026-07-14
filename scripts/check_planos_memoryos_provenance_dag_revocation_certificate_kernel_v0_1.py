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

from runtime.kuuos_memoryos_forgetting_aware_admission_certificate_kernel_v0_1 import (
    issue_forgetting_aware_admission_certificate,
)
from runtime.kuuos_memoryos_provenance_dag_revocation_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_provenance_dag_revocation_certificate,
)
from scripts.check_planos_memoryos_forgetting_aware_admission_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v067_payload,
)


def source_memoryos_v067_certificate() -> dict[str, Any]:
    result = issue_forgetting_aware_admission_certificate(
        build_memoryos_v067_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v067 = source_memoryos_v067_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v067_certificate": source_v067,
        "claims": _derive_observables(source_v067),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_provenance_dag_revocation_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_provenance_dag_revocation_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "provenance_node_record_count": 15,
        "provenance_edge_record_count": 9,
        "strict_reachability_record_count": 10,
        "conflict_component_record_count": 2,
        "revocation_propagation_record_count": 3,
        "multi_source_confidence_record_count": 4,
        "provenance_query_admission_record_count": 5,
        "full_rank_transport_provenance_dag_record_count": 8,
        "singular_atomic_provenance_dag_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    edges = {
        (record["parent_node_id"], record["child_node_id"])
        for record in obs["provenance_edge_records"]
    }
    assert edges == {
        ("language-source-a", "language-synthesis"),
        ("language-source-b", "language-synthesis"),
        ("frontier-v67", "frontier-v68"),
        ("policy-legacy-root", "policy-legacy-derived"),
        ("policy-legacy-derived", "policy-legacy-downstream"),
        ("policy-safe-source-a", "policy-safe-synthesis"),
        ("policy-safe-source-b", "policy-safe-synthesis"),
        ("operations-source-a", "operations-synthesis"),
        ("operations-source-b", "operations-synthesis"),
    }

    reachability = {
        (record["ancestor_node_id"], record["descendant_node_id"])
        for record in obs["strict_reachability_records"]
    }
    assert ("policy-legacy-root", "policy-legacy-downstream") in reachability
    assert ("policy-legacy-downstream", "policy-legacy-root") not in reachability

    components = {
        (record["claim_key"], record["scope"]): record
        for record in obs["conflict_component_records"]
    }
    assert set(components) == {
        ("project-frontier", "project"),
        ("retrieval-policy", "governance"),
    }
    assert components[("retrieval-policy", "governance")][
        "partial_order_not_forced_total"
    ]

    affected = {
        record["affected_node_id"]
        for record in obs["revocation_propagation_records"]
    }
    assert affected == {
        "policy-legacy-root",
        "policy-legacy-derived",
        "policy-legacy-downstream",
    }

    aggregates = {
        record["case_id"]: record["aggregate_confidence"]
        for record in obs["multi_source_confidence_records"]
    }
    assert aggregates == {
        "language-aggregate": {"numerator": 9, "denominator": 10},
        "frontier-aggregate": {"numerator": 1, "denominator": 1},
        "policy-safe-aggregate": {"numerator": 17, "denominator": 20},
        "operations-aggregate": {"numerator": 11, "denominator": 15},
    }

    admissions = {
        record["query_id"]: record["admitted_node_ids"]
        for record in obs["provenance_query_admission_records"]
    }
    assert admissions == {
        "profile-language-query": ["language-synthesis"],
        "project-frontier-query": ["frontier-v68"],
        "retrieval-policy-query": ["policy-safe-synthesis"],
        "memory-operations-query": ["operations-synthesis"],
        "authority-boundary-query": ["authority-source"],
    }

    for field in (
        "source_memoryos_v067_exact",
        "provenance_dag_cycle_free_exact",
        "provenance_edges_strictly_version_increasing_exact",
        "provenance_preorder_partial_order_exact",
        "conflict_components_partial_order_exact",
        "conflict_partial_order_not_forced_total",
        "revocation_propagation_exact",
        "revoked_descendants_excluded_exact",
        "multi_source_confidence_exact",
        "provenance_query_admission_exact",
        "source_records_preserved_under_revocation",
        "all_full_rank_transport_provenance_dag_commutes",
        "singular_atomic_provenance_dag_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "provenance_order_not_candidate_ranking",
        "confidence_aggregation_not_truth_authority",
        "revocation_not_source_deletion",
        "future_only",
        "read_only",
    ):
        assert obs[field] is True, field

    for field in (
        "cycle_accepted",
        "revoked_descendant_admitted",
        "source_record_deleted_by_revocation",
        "similarity_alone_grants_admission",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v067_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v067_certificate"]["certificate_digest"] = "0" * 64
    assert_rejects(
        tampered,
        "source_memoryos_v067_certificate_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["cycle_accepted"] = True
    assert_rejects(tampered, "claim_mismatch_cycle_accepted")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["revoked_descendant_admitted"] = True
    assert_rejects(tampered, "claim_mismatch_revoked_descendant_admitted")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["source_record_deleted_by_revocation"] = True
    assert_rejects(
        tampered,
        "claim_mismatch_source_record_deleted_by_revocation",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(tampered, "claim_mismatch_candidate_selection_performed")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["multi_source_confidence_records"][0][
        "aggregate_confidence"
    ] = {"numerator": 1, "denominator": 1}
    assert_rejects(tampered, "claim_mismatch_multi_source_confidence_records")

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
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
