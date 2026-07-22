from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_external_corpus_acquisition_freeze_receipt_checks_v0_1 import (
    binding_mismatches,
    predecessor_digest,
    validate_predecessor_manifest,
)
from runtime.kuuos_codeai_external_corpus_acquisition_freeze_receipt_schema_v0_1 import *


def _blocked(*issues: str) -> CodeAIExternalCorpusAcquisitionFreezeResult:
    return CodeAIExternalCorpusAcquisitionFreezeResult(
        STATUS_BLOCKED, tuple(sorted(set(issues))), None, None
    )


def _receipt(pack: dict[str, Any]) -> dict[str, Any]:
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "freeze_pack_digest": pack[PACK_DIGEST_FIELD],
        "request_digest": pack["request_digest"],
        "policy_digest": pack["policy_digest"],
        "acquisition_observation_digest": pack["acquisition_observation_digest"],
        "predecessor_manifest_digest": pack["predecessor_manifest_digest"],
        "benchmark_id": pack["benchmark_id"],
        "dataset_name": pack["dataset_name"],
        "dataset_revision": pack["dataset_revision"],
        "dataset_split": pack["dataset_split"],
        "artifact_path": pack["artifact_path"],
        "artifact_sha256": pack["artifact_sha256"],
        "artifact_size_bytes": pack["artifact_size_bytes"],
        "row_count": pack["row_count"],
        "freeze_decision": pack["freeze_decision"],
        "hold_reasons": pack["hold_reasons"],
        "corpus_frozen": pack["corpus_frozen"],
        "solver_label_access_granted": False,
        "gold_patch_access_granted": False,
        "harness_execution_authority_granted": False,
        "repository_mutation_performed": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }
    return seal(receipt, RECEIPT_DIGEST_FIELD)


def build_codeai_external_corpus_acquisition_freeze_receipt(
    *, request: Any, policy: Any, predecessor_manifest: Any, acquisition_observation: Any
) -> CodeAIExternalCorpusAcquisitionFreezeResult:
    request_map = mapping(request)
    policy_map = mapping(policy)
    predecessor_map = mapping(predecessor_manifest)
    observation_map = mapping(acquisition_observation)
    if any(item is None for item in (request_map, policy_map, predecessor_map, observation_map)):
        return _blocked("input_not_mapping")
    assert request_map is not None and policy_map is not None
    assert predecessor_map is not None and observation_map is not None

    issues = (
        validate_request(request_map)
        + validate_policy(policy_map)
        + validate_predecessor_manifest(predecessor_map)
        + validate_observation(observation_map)
    )
    if issues:
        return _blocked(*issues)

    required_true = (
        "require_exact_binding", "require_predecessor_admitted", "require_pinned_revision",
        "require_artifact_sha256", "require_artifact_size", "require_row_count", "require_schema",
        "require_independent_observation", "require_content_addressed_storage", "require_immutable_freeze",
        "require_solver_field_partition", "allow_external_fetch_evidence",
    )
    if any(policy_map[field] is not True for field in required_true):
        return _blocked("policy_required_guarantee_disabled")
    forbidden_policy = (
        "allow_solver_label_access", "allow_gold_patch_access", "allow_harness_execution",
        "allow_repository_mutation", "allow_git_authority", "allow_correctness_claim",
    )
    if any(policy_map[field] is not False for field in forbidden_policy):
        return _blocked("policy_forbidden_authority_enabled")
    if any(request_map[field] for field in (
        "claims_solver_label_access", "claims_gold_patch_access", "claims_harness_execution_authority",
        "claims_repository_mutation_authority", "claims_git_authority", "claims_correctness",
    )):
        return _blocked("request_claims_forbidden_authority")
    if request_map["unresolved_questions"]:
        return _blocked("request_unresolved_questions_present")

    binding_issues = [
        "request_policy_binding_mismatch:" + field
        for field in BINDING_FIELDS
        if request_map[field] != policy_map["expected_" + field]
    ]
    binding_issues.extend(
        "observation_binding_mismatch:" + field
        for field in binding_mismatches(observation_map, request_map)
    )
    if binding_issues:
        return _blocked(*binding_issues)

    actual_predecessor_digest = predecessor_digest(predecessor_map)
    predecessor_issues = []
    if actual_predecessor_digest != request_map["predecessor_manifest_digest"]:
        predecessor_issues.append("predecessor_manifest_digest_mismatch")
    if predecessor_map["adapter_pack_digest"] != request_map["predecessor_adapter_pack_digest"]:
        predecessor_issues.append("predecessor_pack_digest_mismatch")
    if predecessor_map["receipt_digest"] != request_map["predecessor_adapter_receipt_digest"]:
        predecessor_issues.append("predecessor_receipt_digest_mismatch")
    if predecessor_issues:
        return _blocked(*predecessor_issues)

    evaluation_epoch = int(policy_map["evaluation_epoch"])
    if not (
        evaluation_epoch - int(policy_map["maximum_request_age"])
        <= int(request_map["request_created_epoch"])
        <= evaluation_epoch
    ):
        return _blocked("request_window_invalid")
    if not (
        evaluation_epoch - int(policy_map["maximum_observation_age"])
        <= int(observation_map["observation_created_epoch"])
        <= evaluation_epoch
    ):
        return _blocked("observation_window_invalid")

    hold_reasons: list[str] = []
    required_observation_true = (
        "fetch_completed", "network_access_performed_by_fetcher", "artifact_observed",
        "artifact_sha256_verified", "artifact_size_verified", "row_count_verified",
        "schema_verified", "solver_field_partition_verified", "content_addressed_storage",
        "immutable_freeze",
    )
    hold_reasons.extend(
        "acquisition_requirement_missing:" + field
        for field in required_observation_true
        if observation_map[field] is not True
    )
    required_observation_false = (
        "fetch_performed_by_kernel", "artifact_copy_committed_to_repository",
        "gold_patch_exposed_to_solver", "test_patch_exposed_to_solver",
        "evaluation_labels_exposed_to_solver", "harness_execution_performed",
        "repository_mutation_performed", "git_authority_granted", "correctness_claimed",
    )
    hold_reasons.extend(
        "acquisition_boundary_violated:" + field
        for field in required_observation_false
        if observation_map[field] is not False
    )
    if observation_map["observed_row_count"] != request_map["expected_row_count"]:
        hold_reasons.append("observed_row_count_mismatch")
    if tuple(observation_map["observed_schema_columns"]) != SCHEMA_COLUMNS:
        hold_reasons.append("observed_schema_columns_mismatch")
    if tuple(observation_map["solver_visible_fields"]) != SOLVER_VISIBLE_FIELDS:
        hold_reasons.append("solver_visible_fields_mismatch")
    if tuple(observation_map["restricted_evaluator_fields"]) != RESTRICTED_EVALUATOR_FIELDS:
        hold_reasons.append("restricted_evaluator_fields_mismatch")
    if set(observation_map["solver_visible_fields"]) & set(observation_map["restricted_evaluator_fields"]):
        hold_reasons.append("solver_restricted_field_overlap")

    hold_reasons = sorted(set(hold_reasons))
    freeze_decision = DECISION_ADMIT if not hold_reasons else DECISION_HOLD
    pack = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "request_id": request_map["request_id"],
        "request_revision": request_map["request_revision"],
        "request_digest": request_map[REQUEST_DIGEST_FIELD],
        "policy_digest": policy_map[POLICY_DIGEST_FIELD],
        "acquisition_observation_digest": observation_map[OBSERVATION_DIGEST_FIELD],
        "predecessor_manifest_digest": actual_predecessor_digest,
        "predecessor_adapter_pack_digest": request_map["predecessor_adapter_pack_digest"],
        "predecessor_adapter_receipt_digest": request_map["predecessor_adapter_receipt_digest"],
        "controller_repository": request_map["controller_repository"],
        "controller_source_commit_sha": request_map["controller_source_commit_sha"],
        "benchmark_id": request_map["benchmark_id"],
        "dataset_name": request_map["dataset_name"],
        "dataset_revision": request_map["dataset_revision"],
        "dataset_split": request_map["dataset_split"],
        "artifact_path": request_map["artifact_path"],
        "artifact_sha256": request_map["artifact_sha256"],
        "artifact_size_bytes": request_map["artifact_size_bytes"],
        "row_count": observation_map["observed_row_count"],
        "schema_digest": request_map["schema_digest"],
        "solver_visible_fields": list(observation_map["solver_visible_fields"]),
        "restricted_evaluator_fields": list(observation_map["restricted_evaluator_fields"]),
        "corpus_frozen": freeze_decision == DECISION_ADMIT,
        "freeze_decision": freeze_decision,
        "hold_reasons": hold_reasons,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "operating_mode": MODE_FREEZE_ONLY,
        "external_fetch_evidence_consumed": True,
        "fetch_performed_by_kernel": False,
        "artifact_copy_committed_to_repository": False,
        "solver_label_access_granted": False,
        "gold_patch_access_granted": False,
        "harness_execution_authority_granted": False,
        "repository_mutation_performed": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }
    pack = seal(pack, PACK_DIGEST_FIELD)
    return CodeAIExternalCorpusAcquisitionFreezeResult(
        STATUS_READY, (), pack, _receipt(pack)
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIExternalCorpusAcquisitionFreezeResult",
    "build_codeai_external_corpus_acquisition_freeze_receipt",
    "canonical_digest", "canonical_json", "digest_without", "seal",
]
