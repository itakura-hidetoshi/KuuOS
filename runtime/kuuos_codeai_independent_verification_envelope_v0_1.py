#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    digest_without,
    seal,
)

VERSION = "kuuos_codeai_independent_verification_envelope_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Independent Verification v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

MODE_VERIFIED_PASS = "verified_pass"
MODE_VERIFIED_FAIL = "verified_fail"
MODE_HOLD = "hold"
MODE_DEGRADED_VERIFICATION = "degraded_verification"
MODE_ABSTAIN = "abstain"
MODE_HANDOVER = "handover"
MODE_REJECTED = "rejected"

OUTCOME_PASSED = "passed"
OUTCOME_FAILED = "failed"
OUTCOME_INCONCLUSIVE = "inconclusive"
OUTCOME_NOT_RECORDED = "not_recorded"

DISPOSITION_PASSED = "independent_verification_passed"
DISPOSITION_FAILED = "independent_verification_failed"
DISPOSITION_SOURCE_RECEIPT_REPAIR = "source_candidate_receipt_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "verification_provenance_repair_required"
DISPOSITION_INDEPENDENCE_REPAIR = "verifier_independence_repair_required"
DISPOSITION_CORRESPONDENCE_REPAIR = "verification_correspondence_repair_required"
DISPOSITION_EVIDENCE_INTEGRITY_REPAIR = "evidence_integrity_repair_required"
DISPOSITION_CHECK_ACCOUNTING_REPAIR = "check_accounting_repair_required"
DISPOSITION_WINDOW_REPAIR = "verification_window_repair_required"
DISPOSITION_REPLAY_REJECTED = "verification_replay_conflict_rejected"
DISPOSITION_REPOSITORY_MUTATION_REJECTED = "repository_mutation_rejected"
DISPOSITION_AUTHORITY_ESCALATION_REJECTED = "authority_escalation_rejected"
DISPOSITION_UNSUPPORTED_PROFILE_ABSTAINED = (
    "unsupported_verification_profile_abstained"
)
DISPOSITION_MANDATORY_EVIDENCE_HOLD = "mandatory_evidence_hold"
DISPOSITION_PROTOCOL_REPAIR = "verification_protocol_repair_required"
DISPOSITION_OUTCOME_REPAIR = "verification_outcome_repair_required"
DISPOSITION_FINDING_HANDOVER = "verification_finding_handover_required"
DISPOSITION_INCONCLUSIVE_HOLD = "verification_inconclusive_hold"
DISPOSITION_INCONCLUSIVE_DEGRADED = "verification_inconclusive_degraded"

EVIDENCE_DIGEST_FIELD = "codeai_independent_verification_evidence_digest"
POLICY_DIGEST_FIELD = "codeai_independent_verification_policy_digest"
RECEIPT_DIGEST_FIELD = "codeai_independent_verification_receipt_digest"

SOURCE_RECEIPT_FIELDS = {
    "schema_version",
    "profile_version",
    "source_observation_receipt_digest",
    "candidate_patch_digest",
    "candidate_policy_digest",
    "intent_packet_digest",
    "candidate_id",
    "candidate_revision",
    "producer_id",
    "repository_full_name",
    "source_commit_sha",
    "resulting_commit_sha",
    "patch_format",
    "patch_artifact_digest",
    "patch_size_bytes",
    "changed_path_count",
    "added_path_count",
    "modified_path_count",
    "deleted_path_count",
    "renamed_path_count",
    "declared_change_count",
    "codeai_disposition",
    "operating_mode",
    "route_receipt_recorded",
    "candidate_patch_artifact_parsed",
    "candidate_patch_recorded",
    "candidate_patch_ready",
    "clarification_required",
    "evidence_degraded",
    "abstained",
    "handover_required",
    "patch_candidate_only",
    "candidate_generated_by_kernel",
    "candidate_selected",
    "verification_lease_issued",
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
    "source_receipt_treated_as_successor_authority",
    "candidate_treated_as_correct",
    "validation_treated_as_correctness_proof",
    "history_read_only",
    "future_only",
    "active_now",
    SOURCE_RECEIPT_DIGEST_FIELD,
}

EVIDENCE_FIELDS = {
    "verification_id",
    "verifier_id",
    "reviewer_id",
    "source_candidate_receipt_digest",
    "candidate_patch_digest",
    "patch_artifact_digest",
    "repository_full_name",
    "source_commit_sha",
    "evidence_format",
    "toolchain_digest",
    "environment_digest",
    "verification_protocol_digest",
    "check_ids",
    "passed_check_ids",
    "failed_check_ids",
    "skipped_check_ids",
    "declared_check_count",
    "evidence_artifact_digests",
    "finding_labels",
    "outcome_reason_ids",
    "planned_reproduction_attempts",
    "completed_reproduction_attempts",
    "successful_reproduction_attempts",
    "falsification_challenge_executed",
    "falsification_challenge_passed",
    "acceptance_criteria_satisfied",
    "evidence_conclusive",
    "declared_verification_outcome",
    "verification_started_epoch",
    "verification_completed_epoch",
    "verification_session_id",
    "verification_nonce_digest",
    "prior_verification_session_ids",
    "prior_verification_nonce_digests",
    "prior_evidence_digests",
    "prior_verification_receipt_digests",
    "evidence_integrity_confirmed",
    "provenance_integrity_confirmed",
    "source_correspondence_confirmed",
    "isolated_verification_executed",
    "verification_execution_performed_by_kernel",
    "live_repository_mutated_by_verifier",
    "repository_files_changed_by_kernel",
    "git_ref_changed_by_kernel",
    "branch_created_by_kernel",
    "commit_created_by_kernel",
    "push_performed_by_kernel",
    "pull_request_created_by_kernel",
    "external_side_effect_performed_by_kernel",
    "selection_authority_claimed",
    "verification_authority_claimed",
    "execution_authority_claimed",
    "merge_authority_claimed",
    "deployment_authority_claimed",
    "secret_access_authority_claimed",
    "generalized_truth_claimed",
    "correctness_proof_claimed",
    EVIDENCE_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_source_candidate_receipt_digest",
    "expected_candidate_patch_digest",
    "expected_repository_full_name",
    "expected_source_commit_sha",
    "allowed_evidence_formats",
    "allowed_toolchain_digests",
    "allowed_verifier_ids",
    "required_check_ids",
    "minimum_reproduction_attempts",
    "minimum_successful_reproduction_attempts",
    "require_falsification_challenge",
    "require_isolated_verification",
    "require_distinct_candidate_producer",
    "require_distinct_reviewer",
    "allow_skipped_checks",
    "allow_inconclusive_degradation",
    "known_finding_labels",
    "handover_finding_labels",
    "evaluation_epoch",
    "maximum_evidence_age",
    "maximum_verification_duration",
    POLICY_DIGEST_FIELD,
}

_SOURCE_STRING_FIELDS = (
    "schema_version",
    "profile_version",
    "source_observation_receipt_digest",
    "candidate_patch_digest",
    "candidate_policy_digest",
    "intent_packet_digest",
    "candidate_id",
    "candidate_revision",
    "producer_id",
    "repository_full_name",
    "source_commit_sha",
    "resulting_commit_sha",
    "patch_format",
    "patch_artifact_digest",
    "codeai_disposition",
    "operating_mode",
    SOURCE_RECEIPT_DIGEST_FIELD,
)

_SOURCE_NAT_FIELDS = (
    "patch_size_bytes",
    "changed_path_count",
    "added_path_count",
    "modified_path_count",
    "deleted_path_count",
    "renamed_path_count",
    "declared_change_count",
)

_SOURCE_BOOL_FIELDS = tuple(
    sorted(SOURCE_RECEIPT_FIELDS - set(_SOURCE_STRING_FIELDS) - set(_SOURCE_NAT_FIELDS))
)

_EVIDENCE_STRING_FIELDS = (
    "verification_id",
    "verifier_id",
    "reviewer_id",
    "source_candidate_receipt_digest",
    "candidate_patch_digest",
    "patch_artifact_digest",
    "repository_full_name",
    "source_commit_sha",
    "evidence_format",
    "toolchain_digest",
    "environment_digest",
    "verification_protocol_digest",
    "declared_verification_outcome",
    "verification_session_id",
    "verification_nonce_digest",
    EVIDENCE_DIGEST_FIELD,
)

_EVIDENCE_LIST_FIELDS = (
    "check_ids",
    "passed_check_ids",
    "failed_check_ids",
    "skipped_check_ids",
    "evidence_artifact_digests",
    "finding_labels",
    "outcome_reason_ids",
    "prior_verification_session_ids",
    "prior_verification_nonce_digests",
    "prior_evidence_digests",
    "prior_verification_receipt_digests",
)

_EVIDENCE_NAT_FIELDS = (
    "declared_check_count",
    "planned_reproduction_attempts",
    "completed_reproduction_attempts",
    "successful_reproduction_attempts",
    "verification_started_epoch",
    "verification_completed_epoch",
)

_EVIDENCE_BOOL_FIELDS = tuple(
    sorted(
        EVIDENCE_FIELDS
        - set(_EVIDENCE_STRING_FIELDS)
        - set(_EVIDENCE_LIST_FIELDS)
        - set(_EVIDENCE_NAT_FIELDS)
    )
)

_MUTATION_FIELDS = (
    "verification_execution_performed_by_kernel",
    "live_repository_mutated_by_verifier",
    "repository_files_changed_by_kernel",
    "git_ref_changed_by_kernel",
    "branch_created_by_kernel",
    "commit_created_by_kernel",
    "push_performed_by_kernel",
    "pull_request_created_by_kernel",
    "external_side_effect_performed_by_kernel",
)

_AUTHORITY_FIELDS = (
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
class CodeAIIndependentVerificationResult:
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
    issues = _exact_fields(value, SOURCE_RECEIPT_FIELDS, "source_candidate_receipt")
    if issues:
        return issues
    for field in _SOURCE_STRING_FIELDS:
        if not isinstance(value.get(field), str):
            issues.append("source_candidate_receipt_invalid_string:" + field)
    for field in _SOURCE_NAT_FIELDS:
        if _nat(value.get(field)) is None:
            issues.append("source_candidate_receipt_invalid_nat:" + field)
    for field in _SOURCE_BOOL_FIELDS:
        if not isinstance(value.get(field), bool):
            issues.append("source_candidate_receipt_invalid_bool:" + field)
    if value.get(SOURCE_RECEIPT_DIGEST_FIELD) != digest_without(
        value, SOURCE_RECEIPT_DIGEST_FIELD
    ):
        issues.append("source_candidate_receipt_digest_mismatch")
    return issues


def _validate_evidence(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, EVIDENCE_FIELDS, "verification_evidence")
    if issues:
        return issues
    for field in _EVIDENCE_STRING_FIELDS:
        if not isinstance(value.get(field), str):
            issues.append("verification_evidence_invalid_string:" + field)
    for field in _EVIDENCE_LIST_FIELDS:
        if _strings(value.get(field)) is None:
            issues.append("verification_evidence_invalid_string_list:" + field)
    for field in _EVIDENCE_NAT_FIELDS:
        if _nat(value.get(field)) is None:
            issues.append("verification_evidence_invalid_nat:" + field)
    for field in _EVIDENCE_BOOL_FIELDS:
        if not isinstance(value.get(field), bool):
            issues.append("verification_evidence_invalid_bool:" + field)
    if value.get(EVIDENCE_DIGEST_FIELD) != digest_without(value, EVIDENCE_DIGEST_FIELD):
        issues.append("verification_evidence_digest_mismatch")
    return issues


def _validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, POLICY_FIELDS, "verification_policy")
    if issues:
        return issues
    for field in (
        "expected_source_candidate_receipt_digest",
        "expected_candidate_patch_digest",
        "expected_repository_full_name",
        "expected_source_commit_sha",
        POLICY_DIGEST_FIELD,
    ):
        if not isinstance(value.get(field), str):
            issues.append("verification_policy_invalid_string:" + field)
    for field in (
        "allowed_evidence_formats",
        "allowed_toolchain_digests",
        "allowed_verifier_ids",
        "required_check_ids",
        "known_finding_labels",
        "handover_finding_labels",
    ):
        parsed = _strings(value.get(field))
        if parsed is None:
            issues.append("verification_policy_invalid_string_list:" + field)
        elif not parsed or not all(parsed) or len(parsed) != len(set(parsed)):
            issues.append("verification_policy_invalid_nonempty_unique_list:" + field)
    for field in (
        "minimum_reproduction_attempts",
        "minimum_successful_reproduction_attempts",
        "maximum_evidence_age",
        "maximum_verification_duration",
    ):
        if _positive_nat(value.get(field)) is None:
            issues.append("verification_policy_invalid_positive_nat:" + field)
    if _nat(value.get("evaluation_epoch")) is None:
        issues.append("verification_policy_invalid_evaluation_epoch")
    for field in (
        "require_falsification_challenge",
        "require_isolated_verification",
        "require_distinct_candidate_producer",
        "require_distinct_reviewer",
        "allow_skipped_checks",
        "allow_inconclusive_degradation",
    ):
        if not isinstance(value.get(field), bool):
            issues.append("verification_policy_invalid_bool:" + field)
    known = _strings(value.get("known_finding_labels"))
    handover = _strings(value.get("handover_finding_labels"))
    if known is not None and handover is not None and not set(handover).issubset(known):
        issues.append("verification_policy_handover_finding_not_known")
    if not isinstance(value.get("expected_source_candidate_receipt_digest"), str) or not _SHA256.fullmatch(
        value["expected_source_candidate_receipt_digest"]
    ):
        issues.append("verification_policy_expected_source_receipt_digest_invalid")
    if not isinstance(value.get("expected_candidate_patch_digest"), str) or not _SHA256.fullmatch(
        value["expected_candidate_patch_digest"]
    ):
        issues.append("verification_policy_expected_candidate_digest_invalid")
    if not isinstance(value.get("expected_source_commit_sha"), str) or not _SHA40.fullmatch(
        value["expected_source_commit_sha"]
    ):
        issues.append("verification_policy_expected_source_commit_invalid")
    minimum = _nat(value.get("minimum_reproduction_attempts"))
    successful = _nat(value.get("minimum_successful_reproduction_attempts"))
    if minimum is not None and successful is not None and successful > minimum:
        issues.append("verification_policy_successful_attempt_bound_invalid")
    if value.get(POLICY_DIGEST_FIELD) != digest_without(value, POLICY_DIGEST_FIELD):
        issues.append("verification_policy_digest_mismatch")
    return issues


def _preflight(
    source_candidate_receipt: Any,
    verification_evidence: Any,
    verification_policy: Any,
) -> tuple[
    Mapping[str, Any] | None,
    Mapping[str, Any] | None,
    Mapping[str, Any] | None,
    tuple[str, ...],
]:
    source = _mapping(source_candidate_receipt)
    evidence = _mapping(verification_evidence)
    policy = _mapping(verification_policy)
    issues: list[str] = []
    if source is None:
        issues.append("source_candidate_receipt_not_mapping")
    else:
        issues.extend(_validate_source_receipt(source))
    if evidence is None:
        issues.append("verification_evidence_not_mapping")
    else:
        issues.extend(_validate_evidence(evidence))
    if policy is None:
        issues.append("verification_policy_not_mapping")
    else:
        issues.extend(_validate_policy(policy))
    return source, evidence, policy, tuple(issues)


def _unique_nonempty_items(value: Any) -> bool:
    parsed = _strings(value)
    return parsed is not None and all(parsed) and len(parsed) == len(set(parsed))


def _source_receipt_supported(source: Mapping[str, Any]) -> bool:
    false_fields = (
        "clarification_required",
        "evidence_degraded",
        "abstained",
        "handover_required",
        "candidate_generated_by_kernel",
        "candidate_selected",
        "verification_lease_issued",
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
        "source_receipt_treated_as_successor_authority",
        "candidate_treated_as_correct",
        "validation_treated_as_correctness_proof",
        "active_now",
    )
    return (
        source["schema_version"] == "v0.1"
        and source["profile_version"] == "CodeAI Candidate Patch v0.1"
        and source["codeai_disposition"] == "candidate_patch_supported"
        and source["operating_mode"] == "proposal_only"
        and source["route_receipt_recorded"] is True
        and source["candidate_patch_artifact_parsed"] is True
        and source["candidate_patch_recorded"] is True
        and source["candidate_patch_ready"] is True
        and source["patch_candidate_only"] is True
        and source["history_read_only"] is True
        and source["future_only"] is True
        and source["source_commit_sha"] == source["resulting_commit_sha"]
        and source["changed_path_count"] == source["declared_change_count"]
        and bool(_SHA256.fullmatch(source[SOURCE_RECEIPT_DIGEST_FIELD]))
        and bool(_SHA256.fullmatch(source["candidate_patch_digest"]))
        and bool(_SHA256.fullmatch(source["patch_artifact_digest"]))
        and bool(_SHA40.fullmatch(source["source_commit_sha"]))
        and bool(source["candidate_id"])
        and bool(source["producer_id"])
        and bool(source["repository_full_name"])
        and all(source[field] is False for field in false_fields)
    )


def _provenance_valid(evidence: Mapping[str, Any]) -> bool:
    digest_lists = (
        "evidence_artifact_digests",
        "prior_evidence_digests",
        "prior_verification_receipt_digests",
    )
    return (
        bool(evidence["verification_id"])
        and bool(evidence["verifier_id"])
        and bool(evidence["reviewer_id"])
        and bool(evidence["verification_session_id"])
        and bool(evidence["verification_nonce_digest"])
        and evidence["provenance_integrity_confirmed"] is True
        and _unique_nonempty_items(evidence["check_ids"])
        and _unique_nonempty_items(evidence["passed_check_ids"])
        and _unique_nonempty_items(evidence["failed_check_ids"])
        and _unique_nonempty_items(evidence["skipped_check_ids"])
        and _unique_nonempty_items(evidence["evidence_artifact_digests"])
        and _unique_nonempty_items(evidence["finding_labels"])
        and _unique_nonempty_items(evidence["outcome_reason_ids"])
        and _unique_nonempty_items(evidence["prior_verification_session_ids"])
        and _unique_nonempty_items(evidence["prior_verification_nonce_digests"])
        and _unique_nonempty_items(evidence["prior_evidence_digests"])
        and _unique_nonempty_items(evidence["prior_verification_receipt_digests"])
        and all(
            _SHA256.fullmatch(digest)
            for field in digest_lists
            for digest in evidence[field]
        )
        and all(
            _SHA256.fullmatch(digest)
            for digest in evidence["prior_verification_nonce_digests"]
        )
        and bool(_SHA256.fullmatch(evidence["verification_nonce_digest"]))
        and bool(_SHA256.fullmatch(evidence["source_candidate_receipt_digest"]))
        and bool(_SHA256.fullmatch(evidence["candidate_patch_digest"]))
        and bool(_SHA256.fullmatch(evidence["patch_artifact_digest"]))
        and bool(_SHA40.fullmatch(evidence["source_commit_sha"]))
    )


def _independence_valid(
    source: Mapping[str, Any], evidence: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    if policy["require_distinct_candidate_producer"] and (
        evidence["verifier_id"] == source["producer_id"]
        or evidence["reviewer_id"] == source["producer_id"]
    ):
        return False
    if policy["require_distinct_reviewer"] and evidence["reviewer_id"] == evidence["verifier_id"]:
        return False
    return True


def _correspondence_valid(
    source: Mapping[str, Any], evidence: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    return (
        evidence["source_candidate_receipt_digest"]
        == source[SOURCE_RECEIPT_DIGEST_FIELD]
        == policy["expected_source_candidate_receipt_digest"]
        and evidence["candidate_patch_digest"]
        == source["candidate_patch_digest"]
        == policy["expected_candidate_patch_digest"]
        and evidence["patch_artifact_digest"] == source["patch_artifact_digest"]
        and evidence["repository_full_name"]
        == source["repository_full_name"]
        == policy["expected_repository_full_name"]
        and evidence["source_commit_sha"]
        == source["source_commit_sha"]
        == policy["expected_source_commit_sha"]
        and evidence["source_correspondence_confirmed"] is True
    )


def _evidence_integrity_valid(
    evidence: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    return (
        evidence["evidence_integrity_confirmed"] is True
        and bool(evidence["environment_digest"])
        and bool(evidence["verification_protocol_digest"])
        and bool(evidence["toolchain_digest"])
        and bool(evidence["evidence_artifact_digests"])
        and (
            not policy["require_isolated_verification"]
            or evidence["isolated_verification_executed"] is True
        )
    )


def _check_accounting_valid(evidence: Mapping[str, Any]) -> bool:
    checks = tuple(evidence["check_ids"])
    passed = tuple(evidence["passed_check_ids"])
    failed = tuple(evidence["failed_check_ids"])
    skipped = tuple(evidence["skipped_check_ids"])
    partitions = (passed, failed, skipped)
    return (
        checks == tuple(sorted(checks))
        and all(part == tuple(sorted(part)) for part in partitions)
        and len(checks) == len(set(checks))
        and all(len(part) == len(set(part)) for part in partitions)
        and set(passed).isdisjoint(failed)
        and set(passed).isdisjoint(skipped)
        and set(failed).isdisjoint(skipped)
        and set(passed).union(failed, skipped) == set(checks)
        and evidence["declared_check_count"] == len(checks)
    )


def _window_valid(evidence: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    started = evidence["verification_started_epoch"]
    completed = evidence["verification_completed_epoch"]
    evaluated = policy["evaluation_epoch"]
    return (
        started <= completed <= evaluated
        and completed - started <= policy["maximum_verification_duration"]
        and evaluated - completed <= policy["maximum_evidence_age"]
    )


def _replay_closed(evidence: Mapping[str, Any]) -> bool:
    return (
        evidence["verification_session_id"] not in evidence["prior_verification_session_ids"]
        and evidence["verification_nonce_digest"] not in evidence["prior_verification_nonce_digests"]
        and evidence[EVIDENCE_DIGEST_FIELD] not in evidence["prior_evidence_digests"]
    )


def _supported_profile(evidence: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    return (
        evidence["evidence_format"] in policy["allowed_evidence_formats"]
        and evidence["toolchain_digest"] in policy["allowed_toolchain_digests"]
        and evidence["verifier_id"] in policy["allowed_verifier_ids"]
    )


def _mandatory_evidence_missing(
    evidence: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    required = set(policy["required_check_ids"])
    return (
        not required.issubset(evidence["check_ids"])
        or (
            not required.issubset(evidence["passed_check_ids"])
            and evidence["declared_verification_outcome"] == OUTCOME_PASSED
        )
        or (not policy["allow_skipped_checks"] and bool(evidence["skipped_check_ids"]))
    )


def _protocol_valid(evidence: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    planned = evidence["planned_reproduction_attempts"]
    completed = evidence["completed_reproduction_attempts"]
    successful = evidence["successful_reproduction_attempts"]
    return (
        planned >= policy["minimum_reproduction_attempts"]
        and completed == planned
        and successful <= completed
        and successful >= policy["minimum_successful_reproduction_attempts"]
        and (
            not policy["require_falsification_challenge"]
            or evidence["falsification_challenge_executed"] is True
        )
    )


def _outcome_consistent(evidence: Mapping[str, Any]) -> bool:
    outcome = evidence["declared_verification_outcome"]
    if outcome == OUTCOME_PASSED:
        return (
            evidence["evidence_conclusive"] is True
            and not evidence["failed_check_ids"]
            and not evidence["skipped_check_ids"]
            and evidence["acceptance_criteria_satisfied"] is True
            and (
                not evidence["falsification_challenge_executed"]
                or evidence["falsification_challenge_passed"] is True
            )
        )
    if outcome == OUTCOME_FAILED:
        return evidence["evidence_conclusive"] is True and (
            bool(evidence["failed_check_ids"])
            or evidence["acceptance_criteria_satisfied"] is False
            or (
                evidence["falsification_challenge_executed"] is True
                and evidence["falsification_challenge_passed"] is False
            )
        )
    if outcome == OUTCOME_INCONCLUSIVE:
        return evidence["evidence_conclusive"] is False
    return False


def _finding_handover_required(
    evidence: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    findings = set(evidence["finding_labels"])
    known = set(policy["known_finding_labels"])
    handover = set(policy["handover_finding_labels"])
    return not findings.issubset(known) or bool(findings.intersection(handover))


def _disposition_and_mode(
    source: Mapping[str, Any], evidence: Mapping[str, Any], policy: Mapping[str, Any]
) -> tuple[str, str]:
    if not _source_receipt_supported(source):
        return DISPOSITION_SOURCE_RECEIPT_REPAIR, MODE_REJECTED
    if not _provenance_valid(evidence):
        return DISPOSITION_PROVENANCE_REPAIR, MODE_REJECTED
    if not _independence_valid(source, evidence, policy):
        return DISPOSITION_INDEPENDENCE_REPAIR, MODE_REJECTED
    if not _correspondence_valid(source, evidence, policy):
        return DISPOSITION_CORRESPONDENCE_REPAIR, MODE_REJECTED
    if not _evidence_integrity_valid(evidence, policy):
        return DISPOSITION_EVIDENCE_INTEGRITY_REPAIR, MODE_REJECTED
    if not _check_accounting_valid(evidence):
        return DISPOSITION_CHECK_ACCOUNTING_REPAIR, MODE_REJECTED
    if not _window_valid(evidence, policy):
        return DISPOSITION_WINDOW_REPAIR, MODE_REJECTED
    if not _replay_closed(evidence):
        return DISPOSITION_REPLAY_REJECTED, MODE_REJECTED
    if any(evidence[field] is True for field in _MUTATION_FIELDS):
        return DISPOSITION_REPOSITORY_MUTATION_REJECTED, MODE_REJECTED
    if any(evidence[field] is True for field in _AUTHORITY_FIELDS):
        return DISPOSITION_AUTHORITY_ESCALATION_REJECTED, MODE_REJECTED
    if evidence["generalized_truth_claimed"] or evidence["correctness_proof_claimed"]:
        return DISPOSITION_AUTHORITY_ESCALATION_REJECTED, MODE_REJECTED
    if not _supported_profile(evidence, policy):
        return DISPOSITION_UNSUPPORTED_PROFILE_ABSTAINED, MODE_ABSTAIN
    if _mandatory_evidence_missing(evidence, policy):
        return DISPOSITION_MANDATORY_EVIDENCE_HOLD, MODE_HOLD
    if not _protocol_valid(evidence, policy):
        return DISPOSITION_PROTOCOL_REPAIR, MODE_REJECTED
    if not _outcome_consistent(evidence):
        return DISPOSITION_OUTCOME_REPAIR, MODE_REJECTED
    if _finding_handover_required(evidence, policy):
        return DISPOSITION_FINDING_HANDOVER, MODE_HANDOVER
    if evidence["declared_verification_outcome"] == OUTCOME_INCONCLUSIVE:
        if policy["allow_inconclusive_degradation"]:
            return DISPOSITION_INCONCLUSIVE_DEGRADED, MODE_DEGRADED_VERIFICATION
        return DISPOSITION_INCONCLUSIVE_HOLD, MODE_HOLD
    if evidence["declared_verification_outcome"] == OUTCOME_FAILED:
        return DISPOSITION_FAILED, MODE_VERIFIED_FAIL
    return DISPOSITION_PASSED, MODE_VERIFIED_PASS


def _recorded_outcome(disposition: str) -> str:
    if disposition == DISPOSITION_PASSED:
        return OUTCOME_PASSED
    if disposition == DISPOSITION_FAILED:
        return OUTCOME_FAILED
    if disposition in {DISPOSITION_INCONCLUSIVE_HOLD, DISPOSITION_INCONCLUSIVE_DEGRADED}:
        return OUTCOME_INCONCLUSIVE
    return OUTCOME_NOT_RECORDED


def _receipt(
    source: Mapping[str, Any],
    evidence: Mapping[str, Any],
    policy: Mapping[str, Any],
    disposition: str,
    operating_mode: str,
) -> dict[str, Any]:
    outcome = _recorded_outcome(disposition)
    completed = outcome != OUTCOME_NOT_RECORDED
    debt_open = outcome not in {OUTCOME_PASSED, OUTCOME_FAILED}
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_candidate_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "candidate_patch_digest": source["candidate_patch_digest"],
        "patch_artifact_digest": source["patch_artifact_digest"],
        "verification_evidence_digest": evidence[EVIDENCE_DIGEST_FIELD],
        "verification_policy_digest": policy[POLICY_DIGEST_FIELD],
        "verification_id": evidence["verification_id"],
        "verifier_id": evidence["verifier_id"],
        "reviewer_id": evidence["reviewer_id"],
        "candidate_id": source["candidate_id"],
        "repository_full_name": source["repository_full_name"],
        "source_commit_sha": source["source_commit_sha"],
        "resulting_commit_sha": source["source_commit_sha"],
        "declared_check_count": evidence["declared_check_count"],
        "passed_check_count": len(evidence["passed_check_ids"]),
        "failed_check_count": len(evidence["failed_check_ids"]),
        "skipped_check_count": len(evidence["skipped_check_ids"]),
        "codeai_disposition": disposition,
        "operating_mode": operating_mode,
        "verification_outcome": outcome,
        "route_receipt_recorded": True,
        "verification_completed": completed,
        "verification_debt_open": debt_open,
        "reverification_required": outcome == OUTCOME_INCONCLUSIVE,
        "candidate_verification_passed": outcome == OUTCOME_PASSED,
        "candidate_verification_failed": outcome == OUTCOME_FAILED,
        "evidence_degraded": operating_mode == MODE_DEGRADED_VERIFICATION,
        "clarification_required": operating_mode == MODE_HOLD,
        "abstained": operating_mode == MODE_ABSTAIN,
        "handover_required": operating_mode == MODE_HANDOVER,
        "external_isolated_verification_reported": evidence[
            "isolated_verification_executed"
        ],
        "verification_execution_performed_by_kernel": False,
        "candidate_selected": False,
        "candidate_applied": False,
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
        "source_receipt_treated_as_verification_authority": False,
        "verification_treated_as_truth": False,
        "passed_treated_as_correctness_proof": False,
        "failed_treated_as_rejection_authority": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return receipt


def build_codeai_independent_verification_envelope(
    *,
    source_candidate_receipt: Any,
    verification_evidence: Any,
    verification_policy: Any,
) -> CodeAIIndependentVerificationResult:
    source, evidence, policy, issues = _preflight(
        source_candidate_receipt, verification_evidence, verification_policy
    )
    if issues or source is None or evidence is None or policy is None:
        return CodeAIIndependentVerificationResult(STATUS_BLOCKED, issues, None)
    disposition, operating_mode = _disposition_and_mode(source, evidence, policy)
    return CodeAIIndependentVerificationResult(
        STATUS_READY,
        (),
        _receipt(source, evidence, policy, disposition, operating_mode),
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIIndependentVerificationResult",
    "build_codeai_independent_verification_envelope",
    "canonical_digest",
    "digest_without",
    "seal",
]
