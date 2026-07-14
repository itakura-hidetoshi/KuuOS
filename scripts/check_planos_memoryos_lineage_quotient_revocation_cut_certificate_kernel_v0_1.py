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
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_lineage_quotient_revocation_cut_certificate,
)
from runtime.kuuos_memoryos_provenance_dag_revocation_certificate_kernel_v0_1 import (
    issue_provenance_dag_revocation_certificate,
)
from scripts.check_planos_memoryos_provenance_dag_revocation_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v068_payload,
)


def source_memoryos_v068_certificate() -> dict[str, Any]:
    result = issue_provenance_dag_revocation_certificate(
        build_memoryos_v068_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v068 = source_memoryos_v068_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v068_certificate": source_v068,
        "claims": _derive_observables(source_v068),
    }


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_lineage_quotient_revocation_cut_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_lineage_quotient_revocation_cut_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_lineage_governance_record_count": 5,
        "lineage_evidence_record_count": 12,
        "duplicate_lineage_pair_record_count": 4,
        "lineage_quotient_record_count": 5,
        "dependency_adjusted_confidence_record_count": 5,
        "load_bearing_memory_record_count": 5,
        "revocation_path_record_count": 2,
        "revocation_cut_candidate_record_count": 4,
        "minimal_revocation_cut_record_count": 1,
        "full_rank_transport_lineage_quotient_record_count": 8,
        "singular_atomic_lineage_quotient_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    literature_ids = {
        record["literature_id"]
        for record in obs["literature_lineage_governance_records"]
    }
    assert literature_ids == {
        "arxiv:2602.17913",
        "arxiv:2605.25869",
        "arxiv:2606.24535",
        "arxiv:2606.29279",
        "arxiv:2607.01988",
    }

    duplicate_pairs = {
        (
            record["case_id"],
            record["left_evidence_id"],
            record["right_evidence_id"],
        )
        for record in obs["duplicate_lineage_pair_records"]
    }
    assert duplicate_pairs == {
        (
            "language-lineage",
            "language-user-root",
            "language-user-summary-copy",
        ),
        (
            "frontier-lineage",
            "frontier-main-root",
            "frontier-summary-copy",
        ),
        (
            "policy-lineage",
            "policy-memgate-root",
            "policy-memgate-rewrite",
        ),
        (
            "operations-lineage",
            "operations-taxonomy-root",
            "operations-taxonomy-rewrite",
        ),
    }

    quotient = {
        record["case_id"]: (
            record["raw_evidence_count"],
            record["independent_lineage_count"],
            record["raw_naive_confidence"],
            record["lineage_quotient_confidence"],
        )
        for record in obs["lineage_quotient_records"]
    }
    assert quotient == {
        "language-lineage": (
            3,
            2,
            {"numerator": 14, "denominator": 15},
            {"numerator": 9, "denominator": 10},
        ),
        "frontier-lineage": (
            2,
            1,
            {"numerator": 1, "denominator": 1},
            {"numerator": 1, "denominator": 1},
        ),
        "policy-lineage": (
            3,
            2,
            {"numerator": 53, "denominator": 60},
            {"numerator": 17, "denominator": 20},
        ),
        "operations-lineage": (
            3,
            2,
            {"numerator": 4, "denominator": 5},
            {"numerator": 11, "denominator": 15},
        ),
        "authority-lineage": (
            1,
            1,
            {"numerator": 1, "denominator": 1},
            {"numerator": 1, "denominator": 1},
        ),
    }

    adjusted = {
        record["case_id"]: record["adjusted_confidence"]
        for record in obs["dependency_adjusted_confidence_records"]
    }
    assert adjusted == {
        "language-lineage": {"numerator": 9, "denominator": 10},
        "frontier-lineage": {"numerator": 1, "denominator": 1},
        "policy-lineage": {"numerator": 17, "denominator": 20},
        "operations-lineage": {"numerator": 11, "denominator": 15},
        "authority-lineage": {"numerator": 1, "denominator": 1},
    }

    load_bearing = {
        record["case_id"]: record["single_load_bearing_memory"]
        for record in obs["load_bearing_memory_records"]
    }
    assert load_bearing == {
        "language-lineage": False,
        "frontier-lineage": True,
        "policy-lineage": False,
        "operations-lineage": False,
        "authority-lineage": True,
    }

    paths = {
        (record["target_node_id"], tuple(record["path"]))
        for record in obs["revocation_path_records"]
    }
    assert paths == {
        (
            "policy-legacy-derived",
            ("policy-legacy-root", "policy-legacy-derived"),
        ),
        (
            "policy-legacy-downstream",
            (
                "policy-legacy-root",
                "policy-legacy-derived",
                "policy-legacy-downstream",
            ),
        ),
    }

    assert obs["minimal_revocation_cut_records"] == [
        {
            "cut_node_ids": ["policy-legacy-derived"],
            "cut_cardinality": 1,
            "blocked_path_count": 2,
            "total_path_count": 2,
            "blocks_all_paths": True,
            "source_records_deleted": False,
            "inclusion_minimal": True,
            "audit_history_preserved": True,
            "revocation_frontier_only": True,
        }
    ]

    for field in (
        "source_memoryos_v068_exact",
        "lineage_duplicate_detection_exact",
        "lineage_root_partition_exact",
        "dependent_copy_weight_conservation_exact",
        "lineage_adjusted_confidence_exact",
        "derived_surface_confidence_not_promoted_exact",
        "confidence_inflation_prevention_exact",
        "single_load_bearing_memory_flagged_exact",
        "independent_redundancy_not_raw_copy_count_exact",
        "minimal_revocation_cut_exact",
        "revocation_cut_preserves_audit_history",
        "all_full_rank_transport_lineage_quotient_commutes",
        "singular_atomic_lineage_quotient_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "lineage_quotient_not_candidate_ranking",
        "confidence_adjustment_not_truth_authority",
        "minimal_cut_not_source_deletion",
        "future_only",
        "read_only",
    ):
        assert obs[field] is True, field

    for field in (
        "raw_copy_count_grants_independence",
        "derived_surface_confidence_promoted",
        "single_load_bearing_memory_silently_trusted",
        "nonminimal_revocation_cut_claimed_minimal",
        "source_record_deleted_by_revocation_cut",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v068_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        assert obs[field] is False, field

    for field in (
        "literature_lineage_governance_records",
        "lineage_evidence_records",
        "duplicate_lineage_pair_records",
        "lineage_quotient_records",
        "dependency_adjusted_confidence_records",
        "load_bearing_memory_records",
        "revocation_path_records",
        "revocation_cut_candidate_records",
        "minimal_revocation_cut_records",
        "full_rank_transport_lineage_quotient_records",
        "singular_atomic_lineage_quotient_records",
    ):
        digest_field = field.replace("records", "digest")
        assert canonical_digest(obs[field]) == obs[digest_field]

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v068_certificate"]["certificate_digest"] = "0" * 64
    assert_rejects(
        tampered,
        "source_memoryos_v068_certificate_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["raw_copy_count_grants_independence"] = True
    assert_rejects(
        tampered,
        "claim_mismatch_raw_copy_count_grants_independence",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["derived_surface_confidence_promoted"] = True
    assert_rejects(
        tampered,
        "claim_mismatch_derived_surface_confidence_promoted",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["dependency_adjusted_confidence_records"][0][
        "adjusted_confidence"
    ] = {"numerator": 1, "denominator": 1}
    assert_rejects(
        tampered,
        "claim_mismatch_dependency_adjusted_confidence_records",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["minimal_revocation_cut_records"][0][
        "cut_node_ids"
    ] = ["policy-legacy-downstream"]
    assert_rejects(
        tampered,
        "claim_mismatch_minimal_revocation_cut_records",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["source_record_deleted_by_revocation_cut"] = True
    assert_rejects(
        tampered,
        "claim_mismatch_source_record_deleted_by_revocation_cut",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(
        tampered,
        "claim_mismatch_candidate_selection_performed",
    )

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
