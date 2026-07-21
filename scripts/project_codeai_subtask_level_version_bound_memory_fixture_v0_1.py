from __future__ import annotations

from typing import Any, Mapping


def project_fixture(fixture: Mapping[str, Any]) -> dict[str, Any]:
    pack = fixture["memory_pack"]
    receipt = fixture["receipt"]
    return {
        "schema_version": pack["schema_version"],
        "profile_version": pack["profile_version"],
        "repository_full_name": pack["repository_full_name"],
        "source_commit_sha": pack["source_commit_sha"],
        "queried_subtask_kind": pack["queried_subtask_kind"],
        "corpus_entry_count": pack["corpus_entry_count"],
        "matched_entry_count": pack["matched_entry_count"],
        "excluded_entry_count": pack["excluded_entry_count"],
        "matched_entry_ids": [item["entry_id"] for item in pack["matched_entries"]],
        "recommendation": pack["recommendation"],
        "subtask_coverage": ["localize", "diagnose", "edit", "verify"],
        "exact_version_binding_verified": pack["exact_version_binding_verified"],
        "subtask_alignment_verified": pack["subtask_alignment_verified"],
        "dependency_alignment_verified": pack["dependency_alignment_verified"],
        "verifier_grounding_verified": pack["verifier_grounding_verified"],
        "holdout_protection_verified": pack["holdout_protection_verified"],
        "memory_read_only": pack["memory_read_only"],
        "repository_mutation_performed": pack["repository_mutation_performed"],
        "candidate_selected": pack["candidate_selected"],
        "repair_executed": pack["repair_executed"],
        "execution_authority_granted": pack["execution_authority_granted"],
        "git_authority_granted": pack["git_authority_granted"],
        "correctness_claimed": pack["correctness_claimed"],
        "future_success_claimed": pack["future_success_claimed"],
        "request_digest": pack["request_digest"],
        "policy_digest": pack["policy_digest"],
        "corpus_digest": pack["corpus_digest"],
        "memory_pack_digest": pack["codeai_subtask_level_version_bound_memory_pack_digest"],
        "receipt_digest": receipt["codeai_subtask_level_version_bound_memory_receipt_digest"],
    }


__all__ = ["project_fixture"]
