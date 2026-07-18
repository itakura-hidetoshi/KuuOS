#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping

from runtime.kuuos_codeai_independent_verification_envelope_v0_1 import (
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    digest_without,
    seal,
)

VERSION = "kuuos_codeai_autonomous_trajectory_synthesis_envelope_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Autonomous Trajectory Synthesis v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

MODE_AUTONOMOUS_READ_ONLY = "autonomous_read_only"
MODE_AUTONOMOUS_REPAIR = "autonomous_repair"
MODE_DEGRADED_AUTONOMY = "degraded_autonomy"
MODE_HOLD = "hold"
MODE_ABSTAIN = "abstain"
MODE_REJECTED = "rejected"

OUTCOME_PASSED = "passed"
OUTCOME_FAILED = "failed"
OUTCOME_INCONCLUSIVE = "inconclusive"

NEXT_DELIBERATION = "internal_deliberation_candidate"
NEXT_REPAIR = "internal_repair_candidate"
NEXT_REVERIFICATION = "internal_reverification_candidate"
NEXT_NOT_GENERATED = "not_generated"

DISPOSITION_DELIBERATION = "autonomous_deliberation_candidate_synthesized"
DISPOSITION_REPAIR = "autonomous_repair_candidate_synthesized"
DISPOSITION_REVERIFICATION = "autonomous_reverification_candidate_synthesized"
DISPOSITION_SOURCE_RECEIPT_REPAIR = (
    "source_verification_receipt_repair_required"
)
DISPOSITION_PROVENANCE_REPAIR = "trajectory_provenance_repair_required"
DISPOSITION_CORRESPONDENCE_REPAIR = "trajectory_correspondence_repair_required"
DISPOSITION_WINDOW_REPAIR = "trajectory_window_repair_required"
DISPOSITION_REPLAY_REJECTED = "trajectory_replay_conflict_rejected"
DISPOSITION_EFFECT_REQUEST_REJECTED = "repository_or_git_effect_request_rejected"
DISPOSITION_AUTHORITY_ESCALATION_REJECTED = "authority_escalation_rejected"
DISPOSITION_HANDOVER_DEFERRED = "external_handover_deferred"
DISPOSITION_UNSUPPORTED_FORMAT_ABSTAINED = (
    "unsupported_trajectory_format_abstained"
)
DISPOSITION_BUDGET_REJECTED = "trajectory_budget_rejected"
DISPOSITION_OUTCOME_POLICY_REPAIR = "verification_outcome_policy_repair_required"

REQUEST_DIGEST_FIELD = "codeai_autonomous_trajectory_request_digest"
POLICY_DIGEST_FIELD = "codeai_autonomous_trajectory_policy_digest"
RECEIPT_DIGEST_FIELD = "codeai_autonomous_trajectory_receipt_digest"

SOURCE_RECEIPT_FIELDS = {
    "schema_version",
    "profile_version",
    "source_candidate_receipt_digest",
    "candidate_patch_digest",
    "patch_artifact_digest",
    "verification_evidence_digest",
    "verification_policy_digest",
    "verification_id",
    "verifier_id",
    "reviewer_id",
    "candidate_id",
    "repository_full_name",
    "source_commit_sha",
    "resulting_commit_sha",
    "declared_check_count",
    "passed_check_count",
    "failed_check_count",
    "skipped_check_count",
    "codeai_disposition",
    "operating_mode",
    "verification_outcome",
    "route_receipt_recorded",
    "verification_completed",
    "verification_debt_open",
    "reverification_required",
    "candidate_verification_passed",
    "candidate_verification_failed",
    "evidence_degraded",
    "clarification_required",
    "abstained",
    "handover_required",
    "external_isolated_verification_reported",
    "verification_execution_performed_by_kernel",
    "candidate_selected",
    "candidate_applied",
    "execution_lease_issued",
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
    "merge_authority_granted",
    "deployment_authority_granted",
    "secret_access_authority_granted",
    "source_receipt_treated_as_verification_authority",
    "verification_treated_as_truth",
    "passed_treated_as_correctness_proof",
    "failed_treated_as_rejection_authority",
    "history_read_only",
    "future_only",
    "active_now",
    SOURCE_RECEIPT_DIGEST_FIELD,
}

REQUEST_FIELDS = {
    "trajectory_id",
    "trajectory_revision",
    "synthesis_session_id",
    "synthesis_nonce_digest",
    "source_verification_receipt_digest",
    "source_candidate_receipt_digest",
    "candidate_patch_digest",
    "patch_artifact_digest",
    "repository_full_name",
    "source_commit_sha",
    "trajectory_format",
    "requested_step_count",
    "include_candidate_anchor",
    "include_verification_node",
    "autonomous_synthesis_requested",
    "external_handover_requested",
    "patch_generation_requested",
    "candidate_selection_requested",
    "execution_requested",
    "patch_application_requested",
    "repository_mutation_requested",
    "git_mutation_requested",
    "selection_authority_claimed",
    "verification_authority_claimed",
    "execution_authority_claimed",
    "merge_authority_claimed",
    "deployment_authority_claimed",
    "secret_access_authority_claimed",
    "request_created_epoch",
    "prior_synthesis_session_ids",
    "prior_synthesis_nonce_digests",
    "prior_trajectory_receipt_digests",
    "provenance_integrity_confirmed",
    "source_correspondence_confirmed",
    REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_source_verification_receipt_digest",
    "expected_source_candidate_receipt_digest",
    "expected_candidate_patch_digest",
    "expected_repository_full_name",
    "expected_source_commit_sha",
    "allowed_trajectory_formats",
    "allowed_verification_outcomes",
    "maximum_step_count",
    "allow_failed_repair_candidate",
    "allow_inconclusive_reverification_candidate",
    "require_passed_for_deliberation",
    "external_handover_enabled",
    "evaluation_epoch",
    "maximum_request_age",
    POLICY_DIGEST_FIELD,
}

_SOURCE_STRING_FIELDS = (
    "schema_version",
    "profile_version",
    "source_candidate_receipt_digest",
    "candidate_patch_digest",
    "patch_artifact_digest",
    "verification_evidence_digest",
    "verification_policy_digest",
    "verification_id",
    "verifier_id",
    "reviewer_id",
    "candidate_id",
    "repository_full_name",
    "source_commit_sha",
    "resulting_commit_sha",
    "codeai_disposition",
    "operating_mode",
    "verification_outcome",
    SOURCE_RECEIPT_DIGEST_FIELD,
)

_SOURCE_NAT_FIELDS = (
    "declared_check_count",
    "passed_check_count",
    "failed_check_count",
    "skipped_check_count",
)

_SOURCE_BOOL_FIELDS = tuple(
    sorted(SOURCE_RECEIPT_FIELDS - set(_SOURCE_STRING_FIELDS) - set(_SOURCE_NAT_FIELDS))
)

_REQUEST_STRING_FIELDS = (
    "trajectory_id",
    "trajectory_revision",
    "synthesis_session_id",
    "synthesis_nonce_digest",
    "source_verification_receipt_digest",
    "source_candidate_receipt_digest",
    "candidate_patch_digest",
    "patch_artifact_digest",
    "repository_full_name",
    "source_commit_sha",
    "trajectory_format",
    REQUEST_DIGEST_FIELD,
)

_REQUEST_LIST_FIELDS = (
    "prior_synthesis_session_ids",
    "prior_synthesis_nonce_digests",
    "prior_trajectory_receipt_digests",
)

_REQUEST_NAT_FIELDS = ("requested_step_count", "request_created_epoch")

_REQUEST_BOOL_FIELDS = tuple(
    sorted(
        REQUEST_FIELDS
        - set(_REQUEST_STRING_FIELDS)
        - set(_REQUEST_LIST_FIELDS)
        - set(_REQUEST_NAT_FIELDS)
    )
)

_EFFECT_REQUEST_FIELDS = (
    "patch_generation_requested",
    "candidate_selection_requested",
    "execution_requested",
    "patch_application_requested",
    "repository_mutation_requested",
    "git_mutation_requested",
)

_AUTHORITY_CLAIM_FIELDS = (
    "selection_authority_claimed",
    "verification_authority_claimed",
    "execution_authority_claimed",
    "merge_authority_claimed",
    "deployment_authority_claimed",
    "secret_access_authority_claimed",
)

_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class CodeAIAutonomousTrajectorySynthesisResult:
    status: str
    issues: tuple[str, ...]
    receipt: dict[str, Any] | None


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _nat(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _positive_nat(value: Any) -> int | None:
    parsed = _nat(value)
    return parsed if parsed is not None and parsed > 0 else None


def _strings(value: Any) -> tuple[str, ...] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return None
    return tuple(value)


def _exact_fields(value: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = fields.difference(value)
    extra = set(value).difference(fields)
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues


def _validate_source_receipt(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(
        value, SOURCE_RECEIPT_FIELDS, "source_verification_receipt"
    )
    if issues:
        return issues
    for field in _SOURCE_STRING_FIELDS:
        if not isinstance(value.get(field), str):
            issues.append("source_verification_receipt_invalid_string:" + field)
    for field in _SOURCE_NAT_FIELDS:
        if _nat(value.get(field)) is None:
            issues.append("source_verification_receipt_invalid_nat:" + field)
    for field in _SOURCE_BOOL_FIELDS:
        if not isinstance(value.get(field), bool):
            issues.append("source_verification_receipt_invalid_bool:" + field)
    if value.get(SOURCE_RECEIPT_DIGEST_FIELD) != digest_without(
        value, SOURCE_RECEIPT_DIGEST_FIELD
    ):
        issues.append("source_verification_receipt_digest_mismatch")
    return issues


def _validate_request(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, REQUEST_FIELDS, "trajectory_request")
    if issues:
        return issues
    for field in _REQUEST_STRING_FIELDS:
        if not isinstance(value.get(field), str):
            issues.append("trajectory_request_invalid_string:" + field)
    for field in _REQUEST_LIST_FIELDS:
        if _strings(value.get(field)) is None:
            issues.append("trajectory_request_invalid_string_list:" + field)
    for field in _REQUEST_NAT_FIELDS:
        if _nat(value.get(field)) is None:
            issues.append("trajectory_request_invalid_nat:" + field)
    for field in _REQUEST_BOOL_FIELDS:
        if not isinstance(value.get(field), bool):
            issues.append("trajectory_request_invalid_bool:" + field)
    if value.get(REQUEST_DIGEST_FIELD) != digest_without(value, REQUEST_DIGEST_FIELD):
        issues.append("trajectory_request_digest_mismatch")
    return issues


def _validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, POLICY_FIELDS, "trajectory_policy")
    if issues:
        return issues
    for field in (
        "expected_source_verification_receipt_digest",
        "expected_source_candidate_receipt_digest",
        "expected_candidate_patch_digest",
        "expected_repository_full_name",
        "expected_source_commit_sha",
        POLICY_DIGEST_FIELD,
    ):
        if not isinstance(value.get(field), str):
            issues.append("trajectory_policy_invalid_string:" + field)
    for field in ("allowed_trajectory_formats", "allowed_verification_outcomes"):
        parsed = _strings(value.get(field))
        if parsed is None:
            issues.append("trajectory_policy_invalid_string_list:" + field)
        elif not parsed or not all(parsed) or len(parsed) != len(set(parsed)):
            issues.append("trajectory_policy_invalid_nonempty_unique_list:" + field)
    for field in ("maximum_step_count", "maximum_request_age"):
        if _positive_nat(value.get(field)) is None:
            issues.append("trajectory_policy_invalid_positive_nat:" + field)
    if _nat(value.get("evaluation_epoch")) is None:
        issues.append("trajectory_policy_invalid_evaluation_epoch")
    for field in (
        "allow_failed_repair_candidate",
        "allow_inconclusive_reverification_candidate",
        "require_passed_for_deliberation",
        "external_handover_enabled",
    ):
        if not isinstance(value.get(field), bool):
            issues.append("trajectory_policy_invalid_bool:" + field)
    if value.get(POLICY_DIGEST_FIELD) != digest_without(value, POLICY_DIGEST_FIELD):
        issues.append("trajectory_policy_digest_mismatch")
    return issues


def _preflight(
    source_verification_receipt: Any,
    trajectory_request: Any,
    trajectory_policy: Any,
) -> tuple[
    Mapping[str, Any] | None,
    Mapping[str, Any] | None,
    Mapping[str, Any] | None,
    tuple[str, ...],
]:
    source = _mapping(source_verification_receipt)
    request = _mapping(trajectory_request)
    policy = _mapping(trajectory_policy)
    issues: list[str] = []
    if source is None:
        issues.append("source_verification_receipt_not_mapping")
    else:
        issues.extend(_validate_source_receipt(source))
    if request is None:
        issues.append("trajectory_request_not_mapping")
    else:
        issues.extend(_validate_request(request))
    if policy is None:
        issues.append("trajectory_policy_not_mapping")
    else:
        issues.extend(_validate_policy(policy))
    return source, request, policy, tuple(issues)


def _unique_nonempty_items(value: Any) -> bool:
    parsed = _strings(value)
    return parsed is not None and all(parsed) and len(parsed) == len(set(parsed))


def _source_receipt_supported(source: Mapping[str, Any]) -> bool:
    outcome = source["verification_outcome"]
    route_ok = (
        (
            outcome == OUTCOME_PASSED
            and source["codeai_disposition"] == "independent_verification_passed"
            and source["operating_mode"] == "verified_pass"
            and source["verification_debt_open"] is False
            and source["reverification_required"] is False
            and source["candidate_verification_passed"] is True
            and source["candidate_verification_failed"] is False
            and source["clarification_required"] is False
            and source["evidence_degraded"] is False
        )
        or (
            outcome == OUTCOME_FAILED
            and source["codeai_disposition"] == "independent_verification_failed"
            and source["operating_mode"] == "verified_fail"
            and source["verification_debt_open"] is False
            and source["reverification_required"] is False
            and source["candidate_verification_passed"] is False
            and source["candidate_verification_failed"] is True
            and source["clarification_required"] is False
            and source["evidence_degraded"] is False
        )
        or (
            outcome == OUTCOME_INCONCLUSIVE
            and source["codeai_disposition"]
            in {
                "verification_inconclusive_hold",
                "verification_inconclusive_degraded",
            }
            and source["operating_mode"] in {"hold", "degraded_verification"}
            and source["verification_debt_open"] is True
            and source["reverification_required"] is True
            and source["candidate_verification_passed"] is False
            and source["candidate_verification_failed"] is False
            and (
                (
                    source["operating_mode"] == "hold"
                    and source["clarification_required"] is True
                    and source["evidence_degraded"] is False
                )
                or (
                    source["operating_mode"] == "degraded_verification"
                    and source["clarification_required"] is False
                    and source["evidence_degraded"] is True
                )
            )
        )
    )
    false_fields = (
        "abstained",
        "handover_required",
        "verification_execution_performed_by_kernel",
        "candidate_selected",
        "candidate_applied",
        "execution_lease_issued",
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
        "merge_authority_granted",
        "deployment_authority_granted",
        "secret_access_authority_granted",
        "source_receipt_treated_as_verification_authority",
        "verification_treated_as_truth",
        "passed_treated_as_correctness_proof",
        "failed_treated_as_rejection_authority",
        "active_now",
    )
    return (
        source["schema_version"] == "v0.1"
        and source["profile_version"] == "CodeAI Independent Verification v0.1"
        and source["route_receipt_recorded"] is True
        and source["verification_completed"] is True
        and source["history_read_only"] is True
        and source["future_only"] is True
        and source["source_commit_sha"] == source["resulting_commit_sha"]
        and source["declared_check_count"]
        == source["passed_check_count"]
        + source["failed_check_count"]
        + source["skipped_check_count"]
        and bool(_SHA256.fullmatch(source[SOURCE_RECEIPT_DIGEST_FIELD]))
        and bool(_SHA256.fullmatch(source["source_candidate_receipt_digest"]))
        and bool(_SHA256.fullmatch(source["candidate_patch_digest"]))
        and bool(_SHA256.fullmatch(source["patch_artifact_digest"]))
        and bool(_SHA40.fullmatch(source["source_commit_sha"]))
        and bool(source["candidate_id"])
        and bool(source["repository_full_name"])
        and all(source[field] is False for field in false_fields)
        and route_ok
    )


def _provenance_valid(request: Mapping[str, Any]) -> bool:
    return (
        bool(request["trajectory_id"])
        and bool(request["trajectory_revision"])
        and bool(request["synthesis_session_id"])
        and bool(request["synthesis_nonce_digest"])
        and request["provenance_integrity_confirmed"] is True
        and _unique_nonempty_items(request["prior_synthesis_session_ids"])
        and _unique_nonempty_items(request["prior_synthesis_nonce_digests"])
        and _unique_nonempty_items(request["prior_trajectory_receipt_digests"])
        and bool(_SHA256.fullmatch(request["synthesis_nonce_digest"]))
        and all(
            _SHA256.fullmatch(item)
            for item in request["prior_synthesis_nonce_digests"]
        )
        and all(
            _SHA256.fullmatch(item)
            for item in request["prior_trajectory_receipt_digests"]
        )
        and bool(_SHA256.fullmatch(request["source_verification_receipt_digest"]))
        and bool(_SHA256.fullmatch(request["source_candidate_receipt_digest"]))
        and bool(_SHA256.fullmatch(request["candidate_patch_digest"]))
        and bool(_SHA256.fullmatch(request["patch_artifact_digest"]))
        and bool(_SHA40.fullmatch(request["source_commit_sha"]))
    )


def _correspondence_valid(
    source: Mapping[str, Any], request: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    return (
        request["source_verification_receipt_digest"]
        == source[SOURCE_RECEIPT_DIGEST_FIELD]
        == policy["expected_source_verification_receipt_digest"]
        and request["source_candidate_receipt_digest"]
        == source["source_candidate_receipt_digest"]
        == policy["expected_source_candidate_receipt_digest"]
        and request["candidate_patch_digest"]
        == source["candidate_patch_digest"]
        == policy["expected_candidate_patch_digest"]
        and request["patch_artifact_digest"] == source["patch_artifact_digest"]
        and request["repository_full_name"]
        == source["repository_full_name"]
        == policy["expected_repository_full_name"]
        and request["source_commit_sha"]
        == source["source_commit_sha"]
        == policy["expected_source_commit_sha"]
        and request["source_correspondence_confirmed"] is True
    )


def _window_valid(request: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    created = request["request_created_epoch"]
    evaluated = policy["evaluation_epoch"]
    return created <= evaluated and evaluated - created <= policy["maximum_request_age"]


def _replay_closed(request: Mapping[str, Any]) -> bool:
    return (
        request["synthesis_session_id"] not in request["prior_synthesis_session_ids"]
        and request["synthesis_nonce_digest"]
        not in request["prior_synthesis_nonce_digests"]
        and request[REQUEST_DIGEST_FIELD]
        not in request["prior_trajectory_receipt_digests"]
    )


def _budget_valid(request: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    return (
        request["autonomous_synthesis_requested"] is True
        and request["include_candidate_anchor"] is True
        and request["include_verification_node"] is True
        and request["requested_step_count"] == 2
        and request["requested_step_count"] <= policy["maximum_step_count"]
    )


def _outcome_policy_valid(
    source: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    outcome = source["verification_outcome"]
    if outcome not in policy["allowed_verification_outcomes"]:
        return False
    if outcome == OUTCOME_PASSED:
        return policy["require_passed_for_deliberation"] is True
    if outcome == OUTCOME_FAILED:
        return policy["allow_failed_repair_candidate"] is True
    if outcome == OUTCOME_INCONCLUSIVE:
        return policy["allow_inconclusive_reverification_candidate"] is True
    return False


def _disposition_and_mode(
    source: Mapping[str, Any], request: Mapping[str, Any], policy: Mapping[str, Any]
) -> tuple[str, str]:
    if not _source_receipt_supported(source):
        return DISPOSITION_SOURCE_RECEIPT_REPAIR, MODE_REJECTED
    if not _provenance_valid(request):
        return DISPOSITION_PROVENANCE_REPAIR, MODE_REJECTED
    if not _correspondence_valid(source, request, policy):
        return DISPOSITION_CORRESPONDENCE_REPAIR, MODE_REJECTED
    if not _window_valid(request, policy):
        return DISPOSITION_WINDOW_REPAIR, MODE_REJECTED
    if not _replay_closed(request):
        return DISPOSITION_REPLAY_REJECTED, MODE_REJECTED
    if any(request[field] is True for field in _EFFECT_REQUEST_FIELDS):
        return DISPOSITION_EFFECT_REQUEST_REJECTED, MODE_REJECTED
    if any(request[field] is True for field in _AUTHORITY_CLAIM_FIELDS):
        return DISPOSITION_AUTHORITY_ESCALATION_REJECTED, MODE_REJECTED
    if request["external_handover_requested"] or policy["external_handover_enabled"]:
        return DISPOSITION_HANDOVER_DEFERRED, MODE_HOLD
    if request["trajectory_format"] not in policy["allowed_trajectory_formats"]:
        return DISPOSITION_UNSUPPORTED_FORMAT_ABSTAINED, MODE_ABSTAIN
    if not _budget_valid(request, policy):
        return DISPOSITION_BUDGET_REJECTED, MODE_REJECTED
    if not _outcome_policy_valid(source, policy):
        return DISPOSITION_OUTCOME_POLICY_REPAIR, MODE_REJECTED
    if source["verification_outcome"] == OUTCOME_FAILED:
        return DISPOSITION_REPAIR, MODE_AUTONOMOUS_REPAIR
    if source["verification_outcome"] == OUTCOME_INCONCLUSIVE:
        return DISPOSITION_REVERIFICATION, MODE_DEGRADED_AUTONOMY
    return DISPOSITION_DELIBERATION, MODE_AUTONOMOUS_READ_ONLY


def _trajectory_nodes(source: Mapping[str, Any]) -> tuple[list[str], list[str]]:
    node_ids = ["candidate-lineage-anchor", "independent-verification"]
    node_digests = [
        canonical_digest(
            {
                "node_id": node_ids[0],
                "source_candidate_receipt_digest": source[
                    "source_candidate_receipt_digest"
                ],
                "candidate_patch_digest": source["candidate_patch_digest"],
                "patch_artifact_digest": source["patch_artifact_digest"],
            }
        ),
        canonical_digest(
            {
                "node_id": node_ids[1],
                "source_verification_receipt_digest": source[
                    SOURCE_RECEIPT_DIGEST_FIELD
                ],
                "verification_outcome": source["verification_outcome"],
                "verification_evidence_digest": source[
                    "verification_evidence_digest"
                ],
            }
        ),
    ]
    return node_ids, node_digests


def _next_step(disposition: str) -> str:
    if disposition == DISPOSITION_DELIBERATION:
        return NEXT_DELIBERATION
    if disposition == DISPOSITION_REPAIR:
        return NEXT_REPAIR
    if disposition == DISPOSITION_REVERIFICATION:
        return NEXT_REVERIFICATION
    return NEXT_NOT_GENERATED


def _receipt(
    source: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    disposition: str,
    operating_mode: str,
) -> dict[str, Any]:
    successful = disposition in {
        DISPOSITION_DELIBERATION,
        DISPOSITION_REPAIR,
        DISPOSITION_REVERIFICATION,
    }
    node_ids, node_digests = _trajectory_nodes(source) if successful else ([], [])
    next_step = _next_step(disposition)
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_verification_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "source_candidate_receipt_digest": source["source_candidate_receipt_digest"],
        "trajectory_request_digest": request[REQUEST_DIGEST_FIELD],
        "trajectory_policy_digest": policy[POLICY_DIGEST_FIELD],
        "candidate_id": source["candidate_id"],
        "candidate_patch_digest": source["candidate_patch_digest"],
        "patch_artifact_digest": source["patch_artifact_digest"],
        "verification_evidence_digest": source["verification_evidence_digest"],
        "verification_outcome": source["verification_outcome"],
        "trajectory_id": request["trajectory_id"],
        "trajectory_revision": request["trajectory_revision"],
        "trajectory_format": request["trajectory_format"],
        "repository_full_name": source["repository_full_name"],
        "source_commit_sha": source["source_commit_sha"],
        "resulting_commit_sha": source["source_commit_sha"],
        "trajectory_node_ids": node_ids,
        "trajectory_node_digests": node_digests,
        "trajectory_step_count": len(node_ids),
        "next_internal_step_kind": next_step,
        "codeai_disposition": disposition,
        "operating_mode": operating_mode,
        "route_receipt_recorded": True,
        "trajectory_synthesized_by_kernel": successful,
        "trajectory_read_only": True,
        "trajectory_complete_for_available_receipts": successful,
        "full_intent_lineage_reconstructed": False,
        "autonomous_deliberation_candidate_generated": next_step
        == NEXT_DELIBERATION,
        "autonomous_repair_candidate_generated": next_step == NEXT_REPAIR,
        "autonomous_reverification_candidate_generated": next_step
        == NEXT_REVERIFICATION,
        "clarification_required": operating_mode == MODE_HOLD,
        "evidence_degraded": operating_mode == MODE_DEGRADED_AUTONOMY,
        "abstained": operating_mode == MODE_ABSTAIN,
        "external_handover_deferred": disposition == DISPOSITION_HANDOVER_DEFERRED,
        "human_handover_performed": False,
        "external_authority_handover_performed": False,
        "candidate_selected": False,
        "patch_generated": False,
        "patch_applied": False,
        "execution_lease_issued": False,
        "repository_mutation_performed": False,
        "git_ref_changed": False,
        "branch_created": False,
        "commit_created": False,
        "push_performed": False,
        "pull_request_created": False,
        "merge_performed": False,
        "deployment_performed": False,
        "secret_access_performed": False,
        "selection_authority_granted": False,
        "verification_authority_granted": False,
        "execution_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "secret_access_authority_granted": False,
        "source_receipt_treated_as_successor_authority": False,
        "trajectory_treated_as_truth": False,
        "autonomous_candidate_treated_as_authority": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return receipt


def build_codeai_autonomous_trajectory_synthesis_envelope(
    *,
    source_verification_receipt: Any,
    trajectory_request: Any,
    trajectory_policy: Any,
) -> CodeAIAutonomousTrajectorySynthesisResult:
    source, request, policy, issues = _preflight(
        source_verification_receipt, trajectory_request, trajectory_policy
    )
    if issues or source is None or request is None or policy is None:
        return CodeAIAutonomousTrajectorySynthesisResult(
            STATUS_BLOCKED, issues, None
        )
    disposition, operating_mode = _disposition_and_mode(source, request, policy)
    return CodeAIAutonomousTrajectorySynthesisResult(
        STATUS_READY,
        (),
        _receipt(source, request, policy, disposition, operating_mode),
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIAutonomousTrajectorySynthesisResult",
    "build_codeai_autonomous_trajectory_synthesis_envelope",
    "canonical_digest",
    "digest_without",
    "seal",
]
