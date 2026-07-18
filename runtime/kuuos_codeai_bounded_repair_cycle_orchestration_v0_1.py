#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    CANDIDATE_DIGEST_FIELD as PATCH_CANDIDATE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as CANDIDATE_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    patch_artifact_digest,
    seal,
)
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import (
    DISPOSITION_SYNTHESIZED as UNIFIED_DIFF_DISPOSITION_SYNTHESIZED,
    MODE_PROPOSAL_ONLY,
    RECEIPT_DIGEST_FIELD as UNIFIED_DIFF_RECEIPT_DIGEST_FIELD,
    GeneratedUnifiedDiffCandidate,
)
from runtime.kuuos_codeai_autonomous_candidate_regeneration_common_v0_1 import (
    DISPOSITION_NO_NOVEL_CANDIDATE as REGENERATION_DISPOSITION_NO_NOVEL,
    DISPOSITION_REGENERATED as REGENERATION_DISPOSITION_REGENERATED,
    PROFILE_VERSION as REGENERATION_PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD as REGENERATION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_verification_guided_candidate_repair_regeneration_v0_1 import (
    DISPOSITION_NO_NOVEL_CANDIDATE as REPAIR_DISPOSITION_NO_NOVEL,
    DISPOSITION_REGENERATED as REPAIR_DISPOSITION_REGENERATED,
    MODE_BOUNDED_FEEDBACK_REGENERATION,
    PROFILE_VERSION as REPAIR_PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD as REPAIR_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1 import (
    POLICY_DIGEST_FIELD as SELECTION_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SELECTION_RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as SELECTION_REQUEST_DIGEST_FIELD,
    STATUS_READY as SELECTION_STATUS_READY,
    SelectedVerificationCandidate,
    build_codeai_autonomous_candidate_portfolio_selection,
)
from runtime.kuuos_codeai_autonomous_isolated_candidate_application_v0_1 import (
    POLICY_DIGEST_FIELD as APPLICATION_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as APPLICATION_RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as APPLICATION_REQUEST_DIGEST_FIELD,
    STATUS_READY as APPLICATION_STATUS_READY,
    build_codeai_autonomous_isolated_candidate_application,
)
from runtime.kuuos_codeai_autonomous_verification_execution_v0_1 import (
    CANDIDATE_DIGEST_FIELD as RECEIPT_CANDIDATE_DIGEST_FIELD,
    CANDIDATE_RECEIPT_DIGEST_FIELD as EXECUTION_CANDIDATE_RECEIPT_DIGEST_FIELD,
    DISPOSITION_ABORTED_BY_BUDGET,
    DISPOSITION_COMPLETED,
    EVIDENCE_BUNDLE_DIGEST_FIELD,
    INDEPENDENT_EVIDENCE_DIGEST_FIELD,
    PLAN_DIGEST_FIELD,
    POLICY_DIGEST_FIELD as EXECUTION_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as EXECUTION_RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as EXECUTION_REQUEST_DIGEST_FIELD,
    RunnerAdapter,
    STATUS_READY as EXECUTION_STATUS_READY,
    build_codeai_autonomous_verification_execution,
)

VERSION = "kuuos_codeai_bounded_repair_cycle_orchestration_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Bounded Repair Cycle Orchestration v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_BOUNDED_REPAIR_CYCLE = "bounded_repair_cycle_orchestration"
DISPOSITION_PASSED = "repair_cycle_verification_passed"
DISPOSITION_FAILED = "repair_cycle_verification_failed"
DISPOSITION_ABORTED = "repair_cycle_verification_aborted_by_budget"
REQUEST_DIGEST_FIELD = "codeai_bounded_repair_cycle_orchestration_request_digest"
POLICY_DIGEST_FIELD = "codeai_bounded_repair_cycle_orchestration_policy_digest"
CANDIDATE_SET_DIGEST_FIELD = "codeai_bounded_repair_cycle_candidate_set_digest"
RECEIPT_DIGEST_FIELD = "codeai_bounded_repair_cycle_orchestration_receipt_digest"

_REQUEST_FIELDS = {
    "cycle_request_id",
    "cycle_request_revision",
    "cycle_index",
    "source_repair_receipt_digest",
    "source_regeneration_receipt_digest",
    "repair_candidate_set_digest",
    "verification_plan_digest",
    "verification_id",
    "verifier_id",
    "reviewer_id",
    "verification_session_id",
    "verification_nonce_digest",
    "evidence_format",
    "toolchain_digest",
    "environment_digest",
    "verification_protocol_digest",
    "requested_by_actor_id",
    "request_created_epoch",
    REQUEST_DIGEST_FIELD,
}

_POLICY_FIELDS = {
    "expected_source_repair_receipt_digest",
    "expected_source_regeneration_receipt_digest",
    "expected_repair_candidate_set_digest",
    "expected_repository_full_name",
    "expected_source_commit_sha",
    "expected_verification_plan_digest",
    "maximum_cycle_count",
    "maximum_candidate_count",
    "maximum_patch_bytes",
    "maximum_changed_paths",
    "allowed_risk_labels",
    "forbidden_risk_labels",
    "require_no_unresolved_questions",
    "allowed_path_prefixes",
    "forbidden_path_prefixes",
    "maximum_source_path_count",
    "maximum_source_snapshot_bytes",
    "maximum_result_path_count",
    "maximum_result_snapshot_bytes",
    "allow_additions",
    "allow_modifications",
    "allow_deletions",
    "require_exact_changed_path_accounting",
    "allowed_check_ids",
    "allowed_executable_prefixes",
    "allowed_workdir_prefixes",
    "environment_allowlist",
    "maximum_command_count",
    "maximum_timeout_seconds_per_check",
    "maximum_total_timeout_seconds",
    "maximum_stdout_bytes_per_check",
    "maximum_stderr_bytes_per_check",
    "maximum_total_output_bytes",
    "maximum_verification_repository_path_count",
    "maximum_verification_repository_snapshot_bytes",
    "network_access_allowed",
    "secrets_allowed",
    "live_repository_access_allowed",
    "git_operations_allowed",
    "evaluation_epoch",
    "maximum_request_age",
    POLICY_DIGEST_FIELD,
}


@dataclass(frozen=True)
class CodeAIBoundedRepairCycleOrchestrationResult:
    status: str
    issues: tuple[str, ...]
    selected_candidate: SelectedVerificationCandidate | None
    resulting_repository_files: dict[str, str] | None
    evidence_bundle: dict[str, Any] | None
    independent_verification_evidence: dict[str, Any] | None
    receipt: dict[str, Any] | None


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _nat(value: Any, *, positive: bool = False) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    if positive and value == 0:
        return None
    return value


def _strings(value: Any, *, nonempty: bool = False) -> list[str] | None:
    if not isinstance(value, list):
        return None
    if not all(isinstance(item, str) and item for item in value):
        return None
    if len(value) != len(set(value)) or (nonempty and not value):
        return None
    return list(value)


def _exact(value: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = fields.difference(value)
    extra = set(value).difference(fields)
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues


def _digest_ok(value: Mapping[str, Any], field: str) -> bool:
    return value.get(field) == canonical_digest({k: v for k, v in value.items() if k != field})


def _validate_request(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    request = _mapping(value)
    if request is None:
        return None, ["cycle_request_not_mapping"]
    issues = _exact(request, _REQUEST_FIELDS, "cycle_request")
    if issues:
        return request, issues
    for field in _REQUEST_FIELDS - {"cycle_index", "request_created_epoch", REQUEST_DIGEST_FIELD}:
        if not isinstance(request[field], str) or not request[field]:
            issues.append("cycle_request_invalid_string:" + field)
    if _nat(request["cycle_index"], positive=True) is None:
        issues.append("cycle_request_index_invalid")
    if _nat(request["request_created_epoch"]) is None:
        issues.append("cycle_request_created_epoch_invalid")
    if not _digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("cycle_request_digest_mismatch")
    return request, issues


def _validate_policy(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    policy = _mapping(value)
    if policy is None:
        return None, ["cycle_policy_not_mapping"]
    issues = _exact(policy, _POLICY_FIELDS, "cycle_policy")
    if issues:
        return policy, issues
    string_fields = {
        "expected_source_repair_receipt_digest",
        "expected_source_regeneration_receipt_digest",
        "expected_repair_candidate_set_digest",
        "expected_repository_full_name",
        "expected_source_commit_sha",
        "expected_verification_plan_digest",
    }
    for field in string_fields:
        if not isinstance(policy[field], str) or not policy[field]:
            issues.append("cycle_policy_invalid_string:" + field)
    list_fields = {
        "allowed_risk_labels",
        "forbidden_risk_labels",
        "allowed_path_prefixes",
        "forbidden_path_prefixes",
        "allowed_check_ids",
        "allowed_executable_prefixes",
        "allowed_workdir_prefixes",
        "environment_allowlist",
    }
    for field in list_fields:
        nonempty = field not in {
            "forbidden_risk_labels",
            "forbidden_path_prefixes",
            "environment_allowlist",
        }
        if _strings(policy[field], nonempty=nonempty) is None:
            issues.append("cycle_policy_invalid_string_list:" + field)
    bool_fields = {
        "require_no_unresolved_questions",
        "allow_additions",
        "allow_modifications",
        "allow_deletions",
        "require_exact_changed_path_accounting",
        "network_access_allowed",
        "secrets_allowed",
        "live_repository_access_allowed",
        "git_operations_allowed",
    }
    for field in bool_fields:
        if not isinstance(policy[field], bool):
            issues.append("cycle_policy_invalid_bool:" + field)
    for field in (
        "network_access_allowed",
        "secrets_allowed",
        "live_repository_access_allowed",
        "git_operations_allowed",
    ):
        if policy.get(field) is not False:
            issues.append("cycle_policy_required_false:" + field)
    nat_fields = _POLICY_FIELDS - string_fields - list_fields - bool_fields - {POLICY_DIGEST_FIELD}
    for field in nat_fields:
        if _nat(policy[field], positive=field != "evaluation_epoch") is None:
            issues.append("cycle_policy_invalid_nat:" + field)
    if not _digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("cycle_policy_digest_mismatch")
    return policy, issues


def _validate_repair_receipt(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    receipt = _mapping(value)
    if receipt is None:
        return None, ["source_repair_receipt_not_mapping"]
    issues: list[str] = []
    if not _digest_ok(receipt, REPAIR_RECEIPT_DIGEST_FIELD):
        issues.append("source_repair_receipt_digest_mismatch")
    if receipt.get("profile_version") != REPAIR_PROFILE_VERSION:
        issues.append("source_repair_profile_unsupported")
    if receipt.get("codeai_disposition") not in {
        REPAIR_DISPOSITION_REGENERATED,
        REPAIR_DISPOSITION_NO_NOVEL,
    }:
        issues.append("source_repair_disposition_invalid")
    if receipt.get("operating_mode") != MODE_BOUNDED_FEEDBACK_REGENERATION:
        issues.append("source_repair_mode_invalid")
    if receipt.get("route_receipt_recorded") is not True:
        issues.append("source_repair_route_not_recorded")
    if receipt.get("candidate_selected") is not False:
        issues.append("source_repair_candidate_already_selected")
    for field in (
        "patch_applied",
        "repository_mutation_performed",
        "git_ref_changed",
        "branch_created",
        "commit_created",
        "push_performed",
        "pull_request_created",
        "merge_performed",
        "deployment_performed",
        "secret_access_performed",
        "network_access_performed",
        "selection_authority_granted",
        "verification_authority_granted",
        "execution_authority_granted",
        "merge_authority_granted",
        "deployment_authority_granted",
        "secret_access_authority_granted",
        "successor_stage_authority_granted",
    ):
        if receipt.get(field) is not False:
            issues.append("source_repair_required_false:" + field)
    for field in (
        "downstream_regeneration_receipt_digest",
        "candidate_digest",
        "repository_full_name",
        "source_commit_sha",
        REPAIR_RECEIPT_DIGEST_FIELD,
    ):
        if not isinstance(receipt.get(field), str) or not receipt.get(field):
            issues.append("source_repair_invalid_string:" + field)
    return receipt, issues


def _validate_regeneration_receipt(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    receipt = _mapping(value)
    if receipt is None:
        return None, ["source_regeneration_receipt_not_mapping"]
    issues: list[str] = []
    if not _digest_ok(receipt, REGENERATION_RECEIPT_DIGEST_FIELD):
        issues.append("source_regeneration_receipt_digest_mismatch")
    if receipt.get("profile_version") != REGENERATION_PROFILE_VERSION:
        issues.append("source_regeneration_profile_unsupported")
    if receipt.get("codeai_disposition") not in {
        REGENERATION_DISPOSITION_REGENERATED,
        REGENERATION_DISPOSITION_NO_NOVEL,
    }:
        issues.append("source_regeneration_disposition_invalid")
    if receipt.get("operating_mode") != MODE_PROPOSAL_ONLY:
        issues.append("source_regeneration_mode_invalid")
    if receipt.get("route_receipt_recorded") is not True:
        issues.append("source_regeneration_route_not_recorded")
    if receipt.get("candidate_selected") is not False:
        issues.append("source_regeneration_candidate_already_selected")
    for field in (
        "repository_mutation_performed",
        "git_ref_changed",
        "branch_created",
        "commit_created",
        "push_performed",
        "pull_request_created",
        "merge_performed",
        "deployment_performed",
        "secret_access_performed",
        "selection_authority_granted",
        "verification_authority_granted",
        "execution_authority_granted",
    ):
        if receipt.get(field) is not False:
            issues.append("source_regeneration_required_false:" + field)
    return receipt, issues


def _validate_candidates(
    value: Any,
) -> tuple[tuple[GeneratedUnifiedDiffCandidate, ...] | None, str | None, list[str]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or not value:
        return None, None, ["repair_candidates_not_nonempty_sequence"]
    issues: list[str] = []
    candidates: list[GeneratedUnifiedDiffCandidate] = []
    ranks: set[int] = set()
    ids: set[str] = set()
    digests: set[str] = set()
    records: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        prefix = f"repair_candidate[{index}]"
        if not isinstance(item, GeneratedUnifiedDiffCandidate):
            issues.append(prefix + "_invalid_type")
            continue
        candidates.append(item)
        if _nat(item.rank, positive=True) is None:
            issues.append(prefix + "_rank_invalid")
        elif item.rank in ranks:
            issues.append(prefix + "_rank_duplicate")
        ranks.add(item.rank)
        candidate = _mapping(item.patch_candidate)
        receipt = _mapping(item.candidate_receipt)
        if candidate is None or receipt is None:
            issues.append(prefix + "_candidate_or_receipt_not_mapping")
            continue
        candidate_id = candidate.get("candidate_id")
        digest = candidate.get(PATCH_CANDIDATE_DIGEST_FIELD)
        artifact_digest = candidate.get("patch_artifact_digest")
        if not isinstance(candidate_id, str) or not candidate_id:
            issues.append(prefix + "_candidate_id_invalid")
        elif candidate_id != item.proposal_id:
            issues.append(prefix + "_candidate_id_mismatch")
        elif candidate_id in ids:
            issues.append(prefix + "_candidate_id_duplicate")
        ids.add(str(candidate_id))
        if not isinstance(digest, str) or not digest or not _digest_ok(
            candidate, PATCH_CANDIDATE_DIGEST_FIELD
        ):
            issues.append(prefix + "_candidate_digest_invalid")
        elif digest in digests:
            issues.append(prefix + "_candidate_digest_duplicate")
        digests.add(str(digest))
        if artifact_digest != patch_artifact_digest(item.patch_artifact):
            issues.append(prefix + "_artifact_digest_mismatch")
        if not _digest_ok(receipt, CANDIDATE_RECEIPT_DIGEST_FIELD):
            issues.append(prefix + "_candidate_receipt_digest_mismatch")
        if receipt.get("candidate_patch_ready") is not True:
            issues.append(prefix + "_candidate_receipt_not_ready")
        records.append(
            {
                "rank": item.rank,
                "candidate_id": candidate_id,
                "candidate_digest": digest,
                "patch_artifact_digest": artifact_digest,
            }
        )
    if candidates and ranks != set(range(1, len(candidates) + 1)):
        issues.append("repair_candidate_ranks_not_contiguous")
    digest = canonical_digest(records) if not issues else None
    return tuple(candidates), digest, issues


def repair_candidate_set_digest(value: Any) -> str:
    candidates, digest, issues = _validate_candidates(value)
    if issues or candidates is None or digest is None:
        raise ValueError(";".join(sorted(set(issues))))
    return digest


def _rerank(
    candidates: Sequence[GeneratedUnifiedDiffCandidate],
) -> tuple[GeneratedUnifiedDiffCandidate, ...]:
    return tuple(
        GeneratedUnifiedDiffCandidate(
            rank=index,
            proposal_id=item.proposal_id,
            patch_candidate=deepcopy(item.patch_candidate),
            patch_artifact=item.patch_artifact,
            candidate_receipt=deepcopy(item.candidate_receipt),
        )
        for index, item in enumerate(sorted(candidates, key=lambda x: (x.rank, x.proposal_id)), start=1)
    )


def _portfolio_projection(
    repair: Mapping[str, Any],
    candidates: Sequence[GeneratedUnifiedDiffCandidate],
) -> dict[str, Any]:
    return seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION + " portfolio projection",
            "source_repair_receipt_digest": repair[REPAIR_RECEIPT_DIGEST_FIELD],
            "generated_candidate_count": len(candidates),
            "generated_candidate_ids": [item.patch_candidate["candidate_id"] for item in candidates],
            "generated_candidate_digests": [
                item.patch_candidate[PATCH_CANDIDATE_DIGEST_FIELD] for item in candidates
            ],
            "codeai_disposition": UNIFIED_DIFF_DISPOSITION_SYNTHESIZED,
            "operating_mode": MODE_PROPOSAL_ONLY,
            "route_receipt_recorded": True,
            "candidate_selected": False,
            "projection_grants_selection_authority": False,
        },
        UNIFIED_DIFF_RECEIPT_DIGEST_FIELD,
    )


def _selection_inputs(
    *,
    projection: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    projection_digest = projection[UNIFIED_DIFF_RECEIPT_DIGEST_FIELD]
    selection_request = seal(
        {
            "selection_request_id": request["cycle_request_id"] + ":selection",
            "selection_request_revision": request["cycle_request_revision"],
            "source_portfolio_receipt_digest": projection_digest,
            "selection_purpose": "independent_verification",
            "requested_by_actor_id": request["requested_by_actor_id"],
            "request_created_epoch": request["request_created_epoch"],
        },
        SELECTION_REQUEST_DIGEST_FIELD,
    )
    selection_policy = seal(
        {
            "expected_source_portfolio_receipt_digest": projection_digest,
            "maximum_candidate_count": policy["maximum_candidate_count"],
            "maximum_patch_bytes": policy["maximum_patch_bytes"],
            "maximum_changed_paths": policy["maximum_changed_paths"],
            "allowed_risk_labels": list(policy["allowed_risk_labels"]),
            "forbidden_risk_labels": list(policy["forbidden_risk_labels"]),
            "require_no_unresolved_questions": policy["require_no_unresolved_questions"],
            "allowed_path_prefixes": list(policy["allowed_path_prefixes"]),
            "forbidden_path_prefixes": list(policy["forbidden_path_prefixes"]),
            "selection_strategy": "least_change_admissible",
            "evaluation_epoch": policy["evaluation_epoch"],
            "maximum_request_age": policy["maximum_request_age"],
        },
        SELECTION_POLICY_DIGEST_FIELD,
    )
    return selection_request, selection_policy


def _application_inputs(
    *,
    selection_receipt: Mapping[str, Any],
    selected: SelectedVerificationCandidate,
    repository: Mapping[str, str],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    selection_digest = selection_receipt[SELECTION_RECEIPT_DIGEST_FIELD]
    candidate = selected.patch_candidate
    candidate_digest = candidate[PATCH_CANDIDATE_DIGEST_FIELD]
    snapshot_digest = canonical_digest(repository)
    application_request = seal(
        {
            "application_request_id": request["cycle_request_id"] + ":application",
            "application_request_revision": request["cycle_request_revision"],
            "source_selection_receipt_digest": selection_digest,
            "selected_candidate_digest": candidate_digest,
            "source_repository_snapshot_digest": snapshot_digest,
            "application_purpose": "independent_verification_workspace",
            "requested_by_actor_id": request["requested_by_actor_id"],
            "request_created_epoch": request["request_created_epoch"],
        },
        APPLICATION_REQUEST_DIGEST_FIELD,
    )
    application_policy = seal(
        {
            "expected_source_selection_receipt_digest": selection_digest,
            "expected_selected_candidate_digest": candidate_digest,
            "expected_patch_artifact_digest": candidate["patch_artifact_digest"],
            "expected_repository_full_name": candidate["repository_full_name"],
            "expected_source_commit_sha": candidate["source_commit_sha"],
            "expected_source_repository_snapshot_digest": snapshot_digest,
            "maximum_source_path_count": policy["maximum_source_path_count"],
            "maximum_source_snapshot_bytes": policy["maximum_source_snapshot_bytes"],
            "maximum_result_path_count": policy["maximum_result_path_count"],
            "maximum_result_snapshot_bytes": policy["maximum_result_snapshot_bytes"],
            "maximum_patch_bytes": policy["maximum_patch_bytes"],
            "maximum_changed_paths": policy["maximum_changed_paths"],
            "allowed_path_prefixes": list(policy["allowed_path_prefixes"]),
            "forbidden_path_prefixes": list(policy["forbidden_path_prefixes"]),
            "allow_additions": policy["allow_additions"],
            "allow_modifications": policy["allow_modifications"],
            "allow_deletions": policy["allow_deletions"],
            "require_exact_changed_path_accounting":
                policy["require_exact_changed_path_accounting"],
            "evaluation_epoch": policy["evaluation_epoch"],
            "maximum_request_age": policy["maximum_request_age"],
        },
        APPLICATION_POLICY_DIGEST_FIELD,
    )
    return application_request, application_policy


def _execution_inputs(
    *,
    selected: SelectedVerificationCandidate,
    application_receipt: Mapping[str, Any],
    resulting_repository: Mapping[str, str],
    plan: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate_receipt = selected.candidate_receipt
    plan_digest = plan[PLAN_DIGEST_FIELD]
    execution_request = seal(
        {
            "execution_request_id": request["cycle_request_id"] + ":verification",
            "execution_request_revision": request["cycle_request_revision"],
            "source_candidate_receipt_digest":
                candidate_receipt[EXECUTION_CANDIDATE_RECEIPT_DIGEST_FIELD],
            "source_application_receipt_digest":
                application_receipt[APPLICATION_RECEIPT_DIGEST_FIELD],
            "candidate_digest": candidate_receipt[RECEIPT_CANDIDATE_DIGEST_FIELD],
            "patch_artifact_digest": candidate_receipt["patch_artifact_digest"],
            "source_repository_snapshot_digest":
                application_receipt["source_repository_snapshot_digest"],
            "resulting_repository_snapshot_digest": canonical_digest(resulting_repository),
            "repository_full_name": candidate_receipt["repository_full_name"],
            "source_commit_sha": candidate_receipt["source_commit_sha"],
            "verification_plan_digest": plan_digest,
            "verification_id": request["verification_id"],
            "verifier_id": request["verifier_id"],
            "reviewer_id": request["reviewer_id"],
            "verification_session_id": request["verification_session_id"],
            "verification_nonce_digest": request["verification_nonce_digest"],
            "evidence_format": request["evidence_format"],
            "toolchain_digest": request["toolchain_digest"],
            "environment_digest": request["environment_digest"],
            "verification_protocol_digest": request["verification_protocol_digest"],
            "requested_by_actor_id": request["requested_by_actor_id"],
            "request_created_epoch": request["request_created_epoch"],
        },
        EXECUTION_REQUEST_DIGEST_FIELD,
    )
    execution_policy = seal(
        {
            "expected_source_candidate_receipt_digest":
                candidate_receipt[EXECUTION_CANDIDATE_RECEIPT_DIGEST_FIELD],
            "expected_source_application_receipt_digest":
                application_receipt[APPLICATION_RECEIPT_DIGEST_FIELD],
            "expected_candidate_digest":
                candidate_receipt[RECEIPT_CANDIDATE_DIGEST_FIELD],
            "expected_patch_artifact_digest": candidate_receipt["patch_artifact_digest"],
            "expected_source_repository_snapshot_digest":
                application_receipt["source_repository_snapshot_digest"],
            "expected_resulting_repository_snapshot_digest":
                canonical_digest(resulting_repository),
            "expected_repository_full_name": candidate_receipt["repository_full_name"],
            "expected_source_commit_sha": candidate_receipt["source_commit_sha"],
            "expected_verification_plan_digest": plan_digest,
            "allowed_check_ids": list(policy["allowed_check_ids"]),
            "allowed_executable_prefixes": list(policy["allowed_executable_prefixes"]),
            "allowed_workdir_prefixes": list(policy["allowed_workdir_prefixes"]),
            "environment_allowlist": list(policy["environment_allowlist"]),
            "maximum_command_count": policy["maximum_command_count"],
            "maximum_timeout_seconds_per_check":
                policy["maximum_timeout_seconds_per_check"],
            "maximum_total_timeout_seconds": policy["maximum_total_timeout_seconds"],
            "maximum_stdout_bytes_per_check": policy["maximum_stdout_bytes_per_check"],
            "maximum_stderr_bytes_per_check": policy["maximum_stderr_bytes_per_check"],
            "maximum_total_output_bytes": policy["maximum_total_output_bytes"],
            "maximum_repository_path_count":
                policy["maximum_verification_repository_path_count"],
            "maximum_repository_snapshot_bytes":
                policy["maximum_verification_repository_snapshot_bytes"],
            "network_access_allowed": False,
            "secrets_allowed": False,
            "live_repository_access_allowed": False,
            "git_operations_allowed": False,
            "evaluation_epoch": policy["evaluation_epoch"],
            "maximum_request_age": policy["maximum_request_age"],
        },
        EXECUTION_POLICY_DIGEST_FIELD,
    )
    return execution_request, execution_policy


def _receipt(
    *,
    repair: Mapping[str, Any],
    regeneration: Mapping[str, Any],
    candidate_set_digest: str,
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    selection_receipt: Mapping[str, Any],
    selected: SelectedVerificationCandidate,
    application_receipt: Mapping[str, Any],
    resulting_repository: Mapping[str, str],
    execution_receipt: Mapping[str, Any],
    evidence_bundle: Mapping[str, Any],
    independent_evidence: Mapping[str, Any],
) -> dict[str, Any]:
    failed = int(execution_receipt["failed_check_count"])
    disposition = (
        DISPOSITION_ABORTED
        if execution_receipt["codeai_disposition"] == DISPOSITION_ABORTED_BY_BUDGET
        else DISPOSITION_PASSED
        if execution_receipt["codeai_disposition"] == DISPOSITION_COMPLETED and failed == 0
        else DISPOSITION_FAILED
    )
    cycle_index = int(request["cycle_index"])
    maximum_cycles = int(policy["maximum_cycle_count"])
    passed = disposition == DISPOSITION_PASSED
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_repair_receipt_digest": repair[REPAIR_RECEIPT_DIGEST_FIELD],
        "source_regeneration_receipt_digest":
            regeneration[REGENERATION_RECEIPT_DIGEST_FIELD],
        "repair_candidate_set_digest": candidate_set_digest,
        "cycle_request_digest": request[REQUEST_DIGEST_FIELD],
        "cycle_policy_digest": policy[POLICY_DIGEST_FIELD],
        "selection_receipt_digest": selection_receipt[SELECTION_RECEIPT_DIGEST_FIELD],
        "selected_candidate_id": selected.candidate_id,
        "selected_candidate_digest":
            selected.patch_candidate[PATCH_CANDIDATE_DIGEST_FIELD],
        "selected_patch_artifact_digest":
            selected.patch_candidate["patch_artifact_digest"],
        "application_receipt_digest":
            application_receipt[APPLICATION_RECEIPT_DIGEST_FIELD],
        "resulting_repository_snapshot_digest": canonical_digest(resulting_repository),
        "verification_execution_receipt_digest":
            execution_receipt[EXECUTION_RECEIPT_DIGEST_FIELD],
        "evidence_bundle_digest": evidence_bundle[EVIDENCE_BUNDLE_DIGEST_FIELD],
        "independent_verification_evidence_digest":
            independent_evidence[INDEPENDENT_EVIDENCE_DIGEST_FIELD],
        "cycle_index": cycle_index,
        "maximum_cycle_count": maximum_cycles,
        "failed_check_count": failed,
        "codeai_disposition": disposition,
        "operating_mode": MODE_BOUNDED_REPAIR_CYCLE,
        "route_receipt_recorded": True,
        "repair_lineage_verified": True,
        "regeneration_lineage_verified": True,
        "failed_candidate_excluded_from_reselection": True,
        "least_change_reselection_performed": True,
        "isolated_application_performed": True,
        "bounded_verification_execution_performed": True,
        "cycle_completed": True,
        "cycle_verification_passed": passed,
        "cycle_limit_reached": cycle_index >= maximum_cycles,
        "next_cycle_eligible": (not passed) and cycle_index < maximum_cycles,
        "next_cycle_authority_granted": False,
        "input_repository_snapshot_mutated": False,
        "live_repository_patch_applied": False,
        "repository_mutation_performed": False,
        "git_ref_changed": False,
        "branch_created": False,
        "commit_created": False,
        "push_performed": False,
        "pull_request_created": False,
        "merge_performed": False,
        "deployment_performed": False,
        "secret_access_performed": False,
        "network_access_performed": False,
        "selection_authority_granted": False,
        "verification_authority_granted": False,
        "execution_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "secret_access_authority_granted": False,
        "successor_stage_authority_granted": False,
        "cycle_orchestration_treated_as_correctness": False,
        "cycle_pass_treated_as_proof": False,
        "cycle_failure_treated_as_required_repair": False,
        "reselection_treated_as_correctness": False,
        "isolated_application_treated_as_live_mutation": False,
        "verification_evidence_treated_as_merge_authority": False,
        "next_cycle_eligibility_treated_as_authority": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    return seal(value, RECEIPT_DIGEST_FIELD)


def build_codeai_bounded_repair_cycle_orchestration(
    *,
    source_repair_receipt: Any,
    source_regeneration_receipt: Any,
    repair_candidates: Any,
    repository_files: Any,
    cycle_request: Any,
    cycle_policy: Any,
    verification_plan: Any,
    runner_adapter: RunnerAdapter,
) -> CodeAIBoundedRepairCycleOrchestrationResult:
    issues: list[str] = []
    repair, found = _validate_repair_receipt(source_repair_receipt)
    issues += found
    regeneration, found = _validate_regeneration_receipt(source_regeneration_receipt)
    issues += found
    candidates, candidate_set_digest, found = _validate_candidates(repair_candidates)
    issues += found
    repository = _mapping(repository_files)
    if repository is None or not all(
        isinstance(path, str) and isinstance(content, str)
        for path, content in (repository or {}).items()
    ):
        issues.append("repository_files_not_text_mapping")
        repository = None
    request, found = _validate_request(cycle_request)
    issues += found
    policy, found = _validate_policy(cycle_policy)
    issues += found
    plan = _mapping(verification_plan)
    if plan is None:
        issues.append("verification_plan_not_mapping")
    elif not _digest_ok(plan, PLAN_DIGEST_FIELD):
        issues.append("verification_plan_digest_mismatch")
    if not callable(runner_adapter):
        issues.append("runner_adapter_not_callable")
    required = (
        repair,
        regeneration,
        candidates,
        candidate_set_digest,
        repository,
        request,
        policy,
        plan,
    )
    if issues or any(item is None for item in required):
        return CodeAIBoundedRepairCycleOrchestrationResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None, None, None, None
        )
    assert repair is not None and regeneration is not None
    assert candidates is not None and candidate_set_digest is not None
    assert repository is not None and request is not None and policy is not None
    assert plan is not None

    repair_digest = repair[REPAIR_RECEIPT_DIGEST_FIELD]
    regeneration_digest = regeneration[REGENERATION_RECEIPT_DIGEST_FIELD]
    plan_digest = plan[PLAN_DIGEST_FIELD]
    pairs = (
        (repair["downstream_regeneration_receipt_digest"], regeneration_digest, "repair_regeneration"),
        (request["source_repair_receipt_digest"], repair_digest, "request_repair"),
        (request["source_regeneration_receipt_digest"], regeneration_digest, "request_regeneration"),
        (request["repair_candidate_set_digest"], candidate_set_digest, "request_candidate_set"),
        (request["verification_plan_digest"], plan_digest, "request_plan"),
        (policy["expected_source_repair_receipt_digest"], repair_digest, "policy_repair"),
        (policy["expected_source_regeneration_receipt_digest"], regeneration_digest, "policy_regeneration"),
        (policy["expected_repair_candidate_set_digest"], candidate_set_digest, "policy_candidate_set"),
        (policy["expected_verification_plan_digest"], plan_digest, "policy_plan"),
    )
    for actual, expected, label in pairs:
        if actual != expected:
            issues.append("repair_cycle_correspondence_mismatch:" + label)

    candidate_ids = [item.patch_candidate["candidate_id"] for item in candidates]
    candidate_digests = [
        item.patch_candidate[PATCH_CANDIDATE_DIGEST_FIELD] for item in candidates
    ]
    if regeneration.get("combined_candidate_count") != len(candidates):
        issues.append("repair_cycle_candidate_count_mismatch")
    if regeneration.get("combined_candidate_ids") != candidate_ids:
        issues.append("repair_cycle_candidate_ids_mismatch")
    if regeneration.get("combined_candidate_digests") != candidate_digests:
        issues.append("repair_cycle_candidate_digests_mismatch")
    if repair.get("combined_candidate_count") != len(candidates):
        issues.append("repair_receipt_candidate_count_mismatch")
    if regeneration.get("repository_snapshot_digest") != canonical_digest(repository):
        issues.append("repair_cycle_repository_snapshot_mismatch")
    if len(candidates) > int(policy["maximum_candidate_count"]):
        issues.append("repair_cycle_candidate_budget_exceeded")

    repositories = {item.patch_candidate.get("repository_full_name") for item in candidates}
    commits = {item.patch_candidate.get("source_commit_sha") for item in candidates}
    if len(repositories) != 1 or policy["expected_repository_full_name"] not in repositories:
        issues.append("repair_cycle_repository_correspondence_invalid")
    if len(commits) != 1 or policy["expected_source_commit_sha"] not in commits:
        issues.append("repair_cycle_commit_correspondence_invalid")

    cycle_index = int(request["cycle_index"])
    maximum_cycles = int(policy["maximum_cycle_count"])
    if cycle_index > maximum_cycles:
        issues.append("repair_cycle_index_exceeds_policy")
    evaluation = int(policy["evaluation_epoch"])
    created = int(request["request_created_epoch"])
    if not evaluation - int(policy["maximum_request_age"]) <= created <= evaluation:
        issues.append("repair_cycle_request_window_invalid")

    failed_digest = repair["candidate_digest"]
    eligible = [
        item for item in candidates
        if item.patch_candidate[PATCH_CANDIDATE_DIGEST_FIELD] != failed_digest
    ]
    if failed_digest not in candidate_digests:
        issues.append("repair_cycle_failed_candidate_missing_from_lineage")
    if not eligible:
        issues.append("repair_cycle_has_no_candidate_after_failed_candidate_exclusion")
    if issues:
        return CodeAIBoundedRepairCycleOrchestrationResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None, None, None, None
        )

    repository_before = canonical_digest(repository)
    eligible = list(_rerank(eligible))
    projection = _portfolio_projection(repair, eligible)
    selection_request, selection_policy = _selection_inputs(
        projection=projection, request=request, policy=policy
    )
    selection = build_codeai_autonomous_candidate_portfolio_selection(
        source_portfolio_receipt=projection,
        candidates=eligible,
        selection_request=selection_request,
        selection_policy=selection_policy,
    )
    if (
        selection.status != SELECTION_STATUS_READY
        or selection.receipt is None
        or selection.selected_candidate is None
    ):
        return CodeAIBoundedRepairCycleOrchestrationResult(
            STATUS_BLOCKED,
            tuple(sorted(set(["repair_cycle_selection_blocked"] + list(selection.issues)))),
            None,
            None,
            None,
            None,
            None,
        )

    selected = selection.selected_candidate
    application_request, application_policy = _application_inputs(
        selection_receipt=selection.receipt,
        selected=selected,
        repository=repository,
        request=request,
        policy=policy,
    )
    application = build_codeai_autonomous_isolated_candidate_application(
        source_selection_receipt=selection.receipt,
        selected_candidate=selected,
        repository_files=repository,
        application_request=application_request,
        application_policy=application_policy,
    )
    if (
        application.status != APPLICATION_STATUS_READY
        or application.receipt is None
        or application.resulting_repository_files is None
    ):
        return CodeAIBoundedRepairCycleOrchestrationResult(
            STATUS_BLOCKED,
            tuple(sorted(set(["repair_cycle_application_blocked"] + list(application.issues)))),
            selected,
            None,
            None,
            None,
            None,
        )

    execution_request, execution_policy = _execution_inputs(
        selected=selected,
        application_receipt=application.receipt,
        resulting_repository=application.resulting_repository_files,
        plan=plan,
        request=request,
        policy=policy,
    )
    execution = build_codeai_autonomous_verification_execution(
        source_candidate_receipt=selected.candidate_receipt,
        source_application_receipt=application.receipt,
        resulting_repository_files=application.resulting_repository_files,
        verification_plan=plan,
        execution_request=execution_request,
        execution_policy=execution_policy,
        runner_adapter=runner_adapter,
    )
    if (
        execution.status != EXECUTION_STATUS_READY
        or execution.receipt is None
        or execution.evidence_bundle is None
        or execution.independent_verification_evidence is None
    ):
        return CodeAIBoundedRepairCycleOrchestrationResult(
            STATUS_BLOCKED,
            tuple(sorted(set(["repair_cycle_verification_blocked"] + list(execution.issues)))),
            selected,
            application.resulting_repository_files,
            None,
            None,
            None,
        )
    if canonical_digest(repository) != repository_before:
        return CodeAIBoundedRepairCycleOrchestrationResult(
            STATUS_BLOCKED,
            ("input_repository_snapshot_mutated_during_repair_cycle",),
            selected,
            application.resulting_repository_files,
            execution.evidence_bundle,
            execution.independent_verification_evidence,
            None,
        )

    receipt = _receipt(
        repair=repair,
        regeneration=regeneration,
        candidate_set_digest=candidate_set_digest,
        request=request,
        policy=policy,
        selection_receipt=selection.receipt,
        selected=selected,
        application_receipt=application.receipt,
        resulting_repository=application.resulting_repository_files,
        execution_receipt=execution.receipt,
        evidence_bundle=execution.evidence_bundle,
        independent_evidence=execution.independent_verification_evidence,
    )
    return CodeAIBoundedRepairCycleOrchestrationResult(
        STATUS_READY,
        (),
        selected,
        application.resulting_repository_files,
        execution.evidence_bundle,
        execution.independent_verification_evidence,
        receipt,
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIBoundedRepairCycleOrchestrationResult",
    "repair_candidate_set_digest",
    "build_codeai_bounded_repair_cycle_orchestration",
]
