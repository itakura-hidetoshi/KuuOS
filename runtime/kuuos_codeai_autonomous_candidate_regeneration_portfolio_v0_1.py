from __future__ import annotations
from typing import Any, Mapping, Sequence
from runtime.kuuos_codeai_autonomous_candidate_regeneration_common_v0_1 import *

def candidate_summary(item: GeneratedUnifiedDiffCandidate):
    candidate = item.patch_candidate
    return {
        "candidate_id": candidate["candidate_id"],
        "candidate_digest": candidate[CANDIDATE_DIGEST_FIELD],
        "patch_artifact_digest": candidate["patch_artifact_digest"],
        "changed_paths": list(candidate["changed_paths"]),
        "patch_size_bytes": int(candidate["patch_size_bytes"]),
        "risk_labels": list(candidate["risk_labels"]),
    }

def rank_key(item: GeneratedUnifiedDiffCandidate):
    candidate = item.patch_candidate
    return (len(candidate["changed_paths"]), int(candidate["patch_size_bytes"]),
            len(candidate["risk_labels"]), str(candidate["candidate_id"]))

def rerank(items: Sequence[GeneratedUnifiedDiffCandidate]):
    ordered = sorted(items, key=rank_key)
    return tuple(GeneratedUnifiedDiffCandidate(
        rank=index, proposal_id=item.proposal_id,
        patch_candidate=item.patch_candidate, patch_artifact=item.patch_artifact,
        candidate_receipt=item.candidate_receipt,
    ) for index, item in enumerate(ordered, start=1))

def validate_seed_candidates(value: Any, generation: Mapping[str, Any], source: Mapping[str, Any]):
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return None, ["seed_candidates_not_sequence"]
    candidates: list[GeneratedUnifiedDiffCandidate] = []
    issues: list[str] = []
    ids: set[str] = set(); digests: set[str] = set(); artifacts: set[str] = set()
    ranks: list[int] = []
    for index, item in enumerate(value):
        prefix = f"seed_candidate[{index}]"
        if not isinstance(item, GeneratedUnifiedDiffCandidate):
            issues.append(prefix + ":invalid_type"); continue
        candidate = item.patch_candidate; receipt = item.candidate_receipt
        if not isinstance(candidate, Mapping):
            issues.append(prefix + ":candidate_not_mapping"); continue
        if not isinstance(receipt, Mapping):
            issues.append(prefix + ":candidate_receipt_not_mapping")
        else:
            if receipt.get("candidate_patch_ready") is not True:
                issues.append(prefix + ":candidate_receipt_not_ready")
            if receipt.get("codeai_disposition") != "candidate_patch_supported":
                issues.append(prefix + ":candidate_receipt_not_supported")
        digest = candidate.get(CANDIDATE_DIGEST_FIELD)
        if not isinstance(digest, str) or not digest_ok(candidate, CANDIDATE_DIGEST_FIELD):
            issues.append(prefix + ":candidate_digest_mismatch")
        artifact = candidate.get("patch_artifact_digest")
        if artifact != patch_artifact_digest(item.patch_artifact):
            issues.append(prefix + ":patch_artifact_digest_mismatch")
        candidate_id = candidate.get("candidate_id")
        if candidate_id != item.proposal_id:
            issues.append(prefix + ":proposal_id_mismatch")
        if candidate.get("source_observation_receipt_digest") != source.get(SOURCE_RECEIPT_DIGEST_FIELD):
            issues.append(prefix + ":source_observation_receipt_mismatch")
        if candidate.get("repository_full_name") != source.get("repository_full_name"):
            issues.append(prefix + ":repository_mismatch")
        if candidate.get("source_commit_sha") != source.get("source_commit_sha"):
            issues.append(prefix + ":source_commit_mismatch")
        for seen, identity, issue in ((ids, candidate_id, "duplicate_candidate_id"),
                                      (digests, digest, "duplicate_candidate_digest"),
                                      (artifacts, artifact, "duplicate_patch_artifact_digest")):
            if not isinstance(identity, str) or not identity:
                issues.append(prefix + ":missing_identity")
            elif identity in seen:
                issues.append(prefix + ":" + issue)
            else:
                seen.add(identity)
        ranks.append(item.rank); candidates.append(item)
    if ranks != list(range(1, len(ranks) + 1)):
        issues.append("seed_candidate_ranks_not_contiguous")
    structured = generation.get("profile_version") == SOURCE_STRUCTURED_PROFILE
    ids_field = "generated_candidate_ids" if structured else "combined_candidate_ids"
    digests_field = "generated_candidate_digests" if structured else "combined_candidate_digests"
    if generation.get(ids_field) != [item.proposal_id for item in candidates]:
        issues.append("source_generation_candidate_ids_mismatch")
    if generation.get(digests_field) != [item.patch_candidate.get(CANDIDATE_DIGEST_FIELD) for item in candidates]:
        issues.append("source_generation_candidate_digests_mismatch")
    if not structured and generation.get("combined_patch_artifact_digests") != [
        item.patch_candidate.get("patch_artifact_digest") for item in candidates
    ]:
        issues.append("source_generation_patch_artifact_digests_mismatch")
    return candidates, issues

def repository_scope_issues(repository: Mapping[str, str], policy: Mapping[str, Any]):
    issues: list[str] = []
    for path in repository:
        if not isinstance(path, str) or not canonical_path(path):
            issues.append("repository_path_invalid"); continue
        if not any(path_has_prefix(path, prefix) for prefix in policy["allowed_repository_path_prefixes"]):
            issues.append("repository_path_not_allowed:" + path)
        if any(path_has_prefix(path, prefix) for prefix in policy["forbidden_repository_path_prefixes"]):
            issues.append("repository_path_forbidden:" + path)
    return issues

def prompt_packet(*, request, repository, adapter, round_index, attempt_index,
                  diversity_axis, feedback, candidates):
    return {
        "schema_version": SCHEMA_VERSION, "profile_version": PROFILE_VERSION,
        "request_digest": request[REQUEST_DIGEST_FIELD], "request_id": request["request_id"],
        "request_revision": request["request_revision"], "intent_text": request["intent_text"],
        "repository_snapshot_digest": canonical_digest(repository),
        "repository_files": dict(sorted(repository.items())),
        "adapter_id": adapter.adapter_id, "provider_id": adapter.provider_id,
        "model_id": adapter.model_id, "round_index": round_index,
        "attempt_index": attempt_index, "diversity_axis": diversity_axis,
        "feedback_reasons": list(feedback),
        "existing_candidate_summaries": [candidate_summary(item) for item in candidates],
        "forbidden_patch_artifact_digests": sorted(
            item.patch_candidate["patch_artifact_digest"] for item in candidates),
        "target_unique_candidate_count": request["target_unique_candidate_count"],
        "output_contract": {
            "format": "json_object_only", "required_fields": sorted(RAW_PROPOSAL_FIELDS),
            "edit_operations": ["add", "modify", "delete"],
            "complete_new_content_required": True,
            "unified_diff_syntax_forbidden": True,
            "semantic_duplicate_forbidden": True,
        },
        "regeneration_is_candidate_material_only": True,
        "selection_authority_granted": False,
        "verification_authority_granted": False,
        "execution_authority_granted": False,
    }

__all__ = [name for name in globals() if not name.startswith("__")]
