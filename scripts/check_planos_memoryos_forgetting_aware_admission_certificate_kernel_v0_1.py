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

from runtime.kuuos_memoryos_continuous_log_mgf_convexity_certificate_kernel_v0_1 import (
    issue_continuous_log_mgf_convexity_certificate,
)
from runtime.kuuos_memoryos_forgetting_aware_admission_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_forgetting_aware_admission_certificate,
)
from scripts.check_planos_memoryos_continuous_log_mgf_convexity_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v066_payload,
)


def source_memoryos_v066_certificate() -> dict[str, Any]:
    result = issue_continuous_log_mgf_convexity_certificate(
        build_memoryos_v066_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source_v066 = source_memoryos_v066_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v066_certificate": source_v066,
        "claims": _derive_observables(source_v066),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def assert_rejects(payload: dict[str, Any], blocker: str) -> None:
    result = issue_forgetting_aware_admission_certificate(payload)
    assert not result["accepted"], result
    assert blocker in result["blockers"], result["blockers"]


def main() -> int:
    payload = build_reference_payload()
    result = issue_forgetting_aware_admission_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    expected_counts = {
        "literature_provenance_record_count": 8,
        "append_only_memory_archive_record_count": 10,
        "supersession_edge_record_count": 3,
        "effective_memory_record_count": 6,
        "query_conditioned_admission_record_count": 6,
        "freshest_admissible_record_count": 6,
        "forgetting_aware_loss_record_count": 4,
        "full_rank_transport_memory_admission_record_count": 8,
        "singular_atomic_memory_admission_record_count": 4,
        "rank_one_source_boundary_count": 3,
    }
    for field, expected in expected_counts.items():
        assert obs[field] == expected, (field, obs[field])

    literature_ids = {
        record["literature_id"] for record in obs["literature_provenance_records"]
    }
    assert literature_ids == {
        "arxiv:2506.06326",
        "arxiv:2505.00675",
        "arxiv:2502.12110",
        "arxiv:2504.19413",
        "arxiv:2601.03543",
        "arxiv:2602.16313",
        "arxiv:2604.20006",
        "arxiv:2606.06054",
    }

    edges = {
        (record["older_record_id"], record["newer_record_id"])
        for record in obs["supersession_edge_records"]
    }
    assert edges == {
        ("profile-language-v1", "profile-language-v2"),
        ("project-frontier-v65", "project-frontier-v66"),
        ("retrieval-policy-v1", "retrieval-policy-v2"),
    }

    effective = {
        record["record_id"]
        for record in obs["effective_memory_records"]
        if record["effective"]
    }
    assert effective == {
        "profile-language-v2",
        "project-frontier-v66",
        "retrieval-policy-v2",
        "authority-boundary-v1",
        "memory-operations-v1",
        "evaluation-loop-v1",
    }

    admissions = {
        record["query_id"]: record["admitted_record_ids"]
        for record in obs["query_conditioned_admission_records"]
    }
    assert admissions == {
        "profile-language-query": ["profile-language-v2"],
        "project-frontier-query": ["project-frontier-v66"],
        "retrieval-policy-query": ["retrieval-policy-v2"],
        "authority-boundary-query": ["authority-boundary-v1"],
        "memory-operations-query": ["memory-operations-v1"],
        "evaluation-loop-query": ["evaluation-loop-v1"],
    }

    losses = {
        record["case_id"]: record["forgetting_aware_loss"]
        for record in obs["forgetting_aware_loss_records"]
    }
    assert losses == {
        "fresh-perfect": {"numerator": 0, "denominator": 1},
        "fresh-missed": {"numerator": 1, "denominator": 4},
        "obsolete-reuse": {"numerator": 1, "denominator": 2},
        "missed-and-obsolete": {"numerator": 3, "denominator": 4},
    }

    for field in (
        "append_only_archive_exact",
        "all_record_provenance_digests_exact",
        "supersession_relation_exact",
        "obsolete_records_excluded_exact",
        "invalid_records_excluded_exact",
        "query_conditioned_admission_exact",
        "freshest_admissible_witnesses_exact",
        "forgetting_aware_loss_exact",
        "obsolete_reuse_penalized_exact",
        "literature_operations_bound",
        "memory_agent_environment_evaluation_bound",
        "all_full_rank_transport_memory_admission_commutes",
        "singular_atomic_memory_admission_retained",
        "all_decision_candidates_retained",
        "all_planos_histories_retained",
        "all_quotient_coordinate_probes_retained",
        "relational_frontier_preserved",
        "required_review_set_preserved",
        "dissent_visibility_preserved",
        "minority_visibility_preserved",
        "future_only",
        "read_only",
    ):
        assert obs[field] is True, field

    for field in (
        "similarity_alone_grants_admission",
        "obsolete_memory_admitted",
        "cross_scope_leakage_allowed",
        "automatic_forgetting_deletes_source_record",
        "memory_admission_triggers_action",
        "candidate_ranking_performed",
        "candidate_pruning_performed",
        "candidate_selection_performed",
        "decision_commit_performed",
        "decision_receipt_issued",
        "plan_synthesis_performed",
        "activation_performed",
        "execution_permission",
        "source_memoryos_v066_mutated",
        "source_decisionos_v06_mutated",
        "persistent_world_state_mutated",
        "verification_result_claimed",
        "truth_authority_granted",
    ):
        assert obs[field] is False, field

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v066_certificate"]["observables"][
        "derivative_curvature_profile_records"
    ][0]["horizon"] = 99
    _resign(tampered["source_memoryos_v066_certificate"])
    assert_rejects(
        tampered,
        "source_memoryos_v066_derivative_curvature_profile_digest_mismatch",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["append_only_memory_archive_records"][0]["version"] = 9
    assert_rejects(
        tampered,
        "claim_mismatch_append_only_memory_archive_records",
    )

    tampered = copy.deepcopy(payload)
    tampered["claims"]["obsolete_memory_admitted"] = True
    assert_rejects(tampered, "claim_mismatch_obsolete_memory_admitted")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["cross_scope_leakage_allowed"] = True
    assert_rejects(tampered, "claim_mismatch_cross_scope_leakage_allowed")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["memory_admission_triggers_action"] = True
    assert_rejects(tampered, "claim_mismatch_memory_admission_triggers_action")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    assert_rejects(tampered, "claim_mismatch_candidate_selection_performed")

    tampered = copy.deepcopy(payload)
    tampered["claims"]["unexpected_memory_authority"] = True
    assert_rejects(tampered, "unexpected_claim_unexpected_memory_authority")

    print(
        json.dumps(
            {
                "status": "PASS",
                "schema_version": result["schema_version"],
                "certificate_digest": result["certificate_digest"],
                "literature_provenance_digest": obs["literature_provenance_digest"],
                "append_only_memory_archive_digest": obs[
                    "append_only_memory_archive_digest"
                ],
                "supersession_edge_digest": obs["supersession_edge_digest"],
                "query_conditioned_admission_digest": obs[
                    "query_conditioned_admission_digest"
                ],
                "forgetting_aware_loss_digest": obs["forgetting_aware_loss_digest"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
