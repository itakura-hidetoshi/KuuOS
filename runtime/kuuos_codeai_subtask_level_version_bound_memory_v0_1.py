from __future__ import annotations

from collections import Counter
from typing import Any

from runtime.kuuos_codeai_subtask_level_version_bound_memory_checks_v0_1 import (
    binding_mismatches, validate_corpus,
)
from runtime.kuuos_codeai_subtask_level_version_bound_memory_schema_v0_1 import *


def _blocked(*issues: str) -> CodeAISubtaskLevelVersionBoundMemoryResult:
    return CodeAISubtaskLevelVersionBoundMemoryResult(
        STATUS_BLOCKED, tuple(sorted(set(issues))), None, None
    )


def _receipt(pack: dict[str, Any]) -> dict[str, Any]:
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "memory_pack_digest": pack[PACK_DIGEST_FIELD],
        "request_digest": pack["request_digest"],
        "policy_digest": pack["policy_digest"],
        "corpus_digest": pack["corpus_digest"],
        "repository_full_name": pack["repository_full_name"],
        "source_commit_sha": pack["source_commit_sha"],
        "queried_subtask_kind": pack["queried_subtask_kind"],
        "matched_entry_count": pack["matched_entry_count"],
        "excluded_entry_count": pack["excluded_entry_count"],
        "recommendation": pack["recommendation"],
        "exact_version_binding_verified": True,
        "subtask_alignment_verified": True,
        "dependency_alignment_verified": True,
        "verifier_grounding_verified": True,
        "holdout_protection_verified": True,
        "memory_read_only": True,
        "repository_mutation_performed": False,
        "candidate_selected": False,
        "repair_executed": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
        "future_success_claimed": False,
    }
    return seal(receipt, RECEIPT_DIGEST_FIELD)


def build_codeai_subtask_level_version_bound_memory(
    *, request: Any, policy: Any, corpus: Any
) -> CodeAISubtaskLevelVersionBoundMemoryResult:
    request_map = mapping(request)
    policy_map = mapping(policy)
    corpus_map = mapping(corpus)
    if any(item is None for item in (request_map, policy_map, corpus_map)):
        return _blocked("input_not_mapping")
    assert request_map is not None and policy_map is not None and corpus_map is not None

    issues = validate_request(request_map) + validate_policy(policy_map) + validate_corpus(corpus_map)
    if issues:
        return _blocked(*issues)

    required_true = (
        "require_exact_version_binding", "require_subtask_alignment",
        "require_dependency_alignment", "require_verifier_grounding",
        "require_holdout_protection", "require_not_superseded", "allow_memory_hint",
    )
    if any(policy_map[field] is not True for field in required_true):
        return _blocked("policy_required_guarantee_disabled")
    forbidden = (
        "allow_repository_mutation", "allow_candidate_selection", "allow_repair_execution",
        "allow_execution_authority", "allow_git_authority",
    )
    if any(policy_map[field] is not False for field in forbidden):
        return _blocked("policy_effect_or_authority_enabled")
    if any(request_map[field] for field in (
        "claims_selection_authority", "claims_repair_authority",
        "claims_execution_authority", "claims_git_authority",
    )):
        return _blocked("request_claims_authority")
    if request_map["unresolved_questions"]:
        return _blocked("request_unresolved_questions_present")

    binding_issues = [
        "request_policy_binding_mismatch:" + field
        for field in VERSION_BINDING_FIELDS
        if request_map[field] != policy_map["expected_" + field]
    ]
    source_pairs = (
        (corpus_map["repository_full_name"], request_map["repository_full_name"], "corpus_repository_mismatch"),
        (corpus_map["temporal_corpus_digest"], request_map["temporal_corpus_digest"], "corpus_temporal_digest_mismatch"),
        (corpus_map["context_pack_digest"], request_map["context_pack_digest"], "corpus_context_digest_mismatch"),
        (corpus_map["verifier_ensemble_digest"], request_map["verifier_ensemble_digest"], "corpus_verifier_digest_mismatch"),
    )
    binding_issues.extend(code for left, right, code in source_pairs if left != right)
    if binding_issues:
        return _blocked(*binding_issues)

    evaluation_epoch = int(policy_map["evaluation_epoch"])
    request_epoch = int(request_map["request_created_epoch"])
    if not evaluation_epoch - int(policy_map["maximum_request_age"]) <= request_epoch <= evaluation_epoch:
        return _blocked("request_window_invalid")
    entries = corpus_map["entries"]
    if len(entries) > int(policy_map["maximum_corpus_entries"]):
        return _blocked("corpus_entry_budget_exceeded")

    matched: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    allowed = set(policy_map["allowed_outcomes"])
    for entry in entries:
        reasons: list[str] = []
        for field in binding_mismatches(entry, request_map):
            reasons.append("binding_mismatch:" + field)
        if entry["outcome"] not in allowed:
            reasons.append("outcome_not_allowed")
        if entry["derived_from_holdout"]:
            reasons.append("holdout_derived")
        if entry["superseded"]:
            reasons.append("superseded")
        if not evaluation_epoch - int(policy_map["maximum_entry_age"]) <= int(entry["evidence_created_epoch"]) <= evaluation_epoch:
            reasons.append("entry_window_invalid")
        for field in (
            "repository_mutation_performed", "candidate_selected", "repair_executed",
            "execution_authority_granted", "git_authority_granted",
            "correctness_claimed", "future_success_claimed",
        ):
            if entry[field]:
                reasons.append("forbidden_entry_claim:" + field)
        if reasons:
            reasons = sorted(set(reasons))
            counts.update(reasons)
            excluded.append({
                "entry_digest": entry[ENTRY_DIGEST_FIELD],
                "reasons": reasons,
            })
        else:
            matched.append(entry)
    if len(matched) > int(policy_map["maximum_matched_entries"]):
        return _blocked("matched_entry_budget_exceeded")

    recommendation = RECOMMENDATION_AVAILABLE if matched else RECOMMENDATION_NONE
    pack = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "request_id": request_map["request_id"],
        "request_revision": request_map["request_revision"],
        "request_digest": request_map[REQUEST_DIGEST_FIELD],
        "policy_digest": policy_map[POLICY_DIGEST_FIELD],
        "corpus_digest": corpus_map[CORPUS_DIGEST_FIELD],
        "repository_full_name": request_map["repository_full_name"],
        "source_commit_sha": request_map["source_commit_sha"],
        "source_tree_digest": request_map["source_tree_digest"],
        "temporal_corpus_digest": request_map["temporal_corpus_digest"],
        "context_pack_digest": request_map["context_pack_digest"],
        "verifier_ensemble_digest": request_map["verifier_ensemble_digest"],
        "queried_subtask_kind": request_map["subtask_kind"],
        "query_binding": {field: request_map[field] for field in VERSION_BINDING_FIELDS},
        "corpus_entry_count": len(entries),
        "matched_entries": matched,
        "matched_entry_count": len(matched),
        "excluded_entries": excluded,
        "excluded_entry_count": len(excluded),
        "exclusion_counts": dict(sorted(counts.items())),
        "recommendation": recommendation,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "operating_mode": MODE_MEMORY_ONLY,
        "exact_version_binding_verified": True,
        "subtask_alignment_verified": True,
        "dependency_alignment_verified": True,
        "verifier_grounding_verified": True,
        "holdout_protection_verified": True,
        "memory_read_only": True,
        "repository_mutation_performed": False,
        "candidate_selected": False,
        "repair_executed": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
        "future_success_claimed": False,
    }
    pack = seal(pack, PACK_DIGEST_FIELD)
    return CodeAISubtaskLevelVersionBoundMemoryResult(
        STATUS_READY, (), pack, _receipt(pack)
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAISubtaskLevelVersionBoundMemoryResult",
    "build_codeai_subtask_level_version_bound_memory",
    "canonical_digest", "canonical_json", "digest_without", "seal",
]
