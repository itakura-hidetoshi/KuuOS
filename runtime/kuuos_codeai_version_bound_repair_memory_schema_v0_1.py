from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping

from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import (
    CLASSIFICATION_DIGEST_FIELD as SOURCE_CLASSIFICATION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_CLASSIFICATION_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    canonical_json,
    digest_without,
    seal,
)

VERSION = "kuuos_codeai_version_bound_repair_memory_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Version-Bound Repair Memory v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_MEMORY_ONLY = "version_bound_repair_memory_only"
DISPOSITION_COMPLETED = "version_bound_repair_memory_completed"

OUTCOME_VERIFIED_EFFECTIVE = "verified_effective"
OUTCOME_VERIFIED_INEFFECTIVE = "verified_ineffective"
OUTCOME_INCONCLUSIVE = "inconclusive"
REPAIR_OUTCOMES = (
    OUTCOME_VERIFIED_EFFECTIVE,
    OUTCOME_VERIFIED_INEFFECTIVE,
    OUTCOME_INCONCLUSIVE,
)

RECOMMENDATION_HINT_AVAILABLE = "exact_version_bound_repair_hint_available"
RECOMMENDATION_NO_HINT = "no_exact_version_bound_repair_hint"
RECOMMENDATIONS = (RECOMMENDATION_HINT_AVAILABLE, RECOMMENDATION_NO_HINT)

REQUEST_DIGEST_FIELD = "codeai_version_bound_repair_memory_request_digest"
POLICY_DIGEST_FIELD = "codeai_version_bound_repair_memory_policy_digest"
REPAIR_PACKET_DIGEST_FIELD = "codeai_version_bound_repair_evidence_packet_digest"
REPAIR_RECORD_DIGEST_FIELD = "codeai_version_bound_repair_evidence_record_digest"
MEMORY_ENTRY_DIGEST_FIELD = "codeai_version_bound_repair_memory_entry_digest"
MEMORY_SNAPSHOT_DIGEST_FIELD = "codeai_version_bound_repair_memory_snapshot_digest"
RECEIPT_DIGEST_FIELD = "codeai_version_bound_repair_memory_receipt_digest"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]{1,127}$")

VERSION_BINDING_FIELDS = (
    "repository_full_name",
    "source_commit_sha",
    "source_repository_snapshot_digest",
    "source_candidate_digest",
    "typed_error_digest",
    "error_fingerprint",
    "classification_schema_version",
    "toolchain_digest",
    "dependency_manifest_digest",
    "repair_policy_digest",
)


@dataclass(frozen=True)
class CodeAIVersionBoundRepairMemoryResult:
    status: str
    issues: tuple[str, ...]
    snapshot: dict[str, Any] | None
    receipt: dict[str, Any] | None


def mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def digest_ok(value: Mapping[str, Any], field: str) -> bool:
    digest = value.get(field)
    return isinstance(digest, str) and SHA256.fullmatch(digest) is not None and digest == digest_without(value, field)


def nonnegative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def positive_int(value: Any) -> bool:
    return nonnegative_int(value) and value > 0


def unique_strings(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value))
        and (bool(value) or not nonempty)
    )


def _validate_binding_fields(value: Mapping[str, Any], prefix: str) -> list[str]:
    issues: list[str] = []
    if not isinstance(value.get("repository_full_name"), str) or not value["repository_full_name"]:
        issues.append(prefix + "_repository_invalid")
    if not isinstance(value.get("source_commit_sha"), str) or SHA40.fullmatch(value["source_commit_sha"]) is None:
        issues.append(prefix + "_source_commit_invalid")
    for field in (
        "source_repository_snapshot_digest",
        "source_candidate_digest",
        "typed_error_digest",
        "toolchain_digest",
        "dependency_manifest_digest",
        "repair_policy_digest",
    ):
        field_value = value.get(field)
        if not isinstance(field_value, str) or SHA256.fullmatch(field_value) is None:
            issues.append(prefix + "_digest_invalid:" + field)
    fingerprint = value.get("error_fingerprint")
    if not isinstance(fingerprint, str) or not fingerprint:
        issues.append(prefix + "_fingerprint_invalid")
    schema = value.get("classification_schema_version")
    if not isinstance(schema, str) or not schema:
        issues.append(prefix + "_classification_schema_invalid")
    return issues


def validate_request(request: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "memory_request_id",
        "memory_request_revision",
        "source_classification_digest",
        "source_classification_receipt_digest",
        "repair_evidence_packet_digest",
        *VERSION_BINDING_FIELDS,
        "request_created_epoch",
        "unresolved_memory_questions",
        "claims_repair_authority",
        "claims_execution_authority",
        "claims_git_authority",
        REQUEST_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(request)
    extra = set(request).difference(required)
    if missing:
        issues.append("memory_request_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("memory_request_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if request["schema_version"] != SCHEMA_VERSION or request["profile_version"] != PROFILE_VERSION:
        issues.append("memory_request_profile_invalid")
    for field in ("memory_request_id", "memory_request_revision"):
        if not isinstance(request[field], str) or IDENTIFIER.fullmatch(request[field]) is None:
            issues.append("memory_request_identifier_invalid:" + field)
    for field in (
        "source_classification_digest",
        "source_classification_receipt_digest",
        "repair_evidence_packet_digest",
    ):
        if not isinstance(request[field], str) or SHA256.fullmatch(request[field]) is None:
            issues.append("memory_request_digest_invalid:" + field)
    issues.extend(_validate_binding_fields(request, "memory_request_binding"))
    if not nonnegative_int(request["request_created_epoch"]):
        issues.append("memory_request_epoch_invalid")
    if not unique_strings(request["unresolved_memory_questions"]):
        issues.append("memory_request_questions_invalid")
    for field in (
        "claims_repair_authority",
        "claims_execution_authority",
        "claims_git_authority",
    ):
        if not isinstance(request[field], bool):
            issues.append("memory_request_boolean_invalid:" + field)
    if not digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("memory_request_digest_mismatch")
    return sorted(set(issues))


def validate_policy(policy: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "expected_source_classification_digest",
        "expected_source_classification_receipt_digest",
        "expected_repair_evidence_packet_digest",
        *{"expected_" + field for field in VERSION_BINDING_FIELDS},
        "evaluation_epoch",
        "maximum_request_age",
        "maximum_evidence_age",
        "maximum_memory_entries",
        "maximum_matched_entries",
        "allowed_repair_outcomes",
        "require_exact_version_binding",
        "require_complete_typed_error_correspondence",
        "require_independent_verification",
        "require_isolated_candidate_repair",
        "require_live_repository_unchanged",
        "allow_memory_hint",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_execution_authority",
        "allow_git_authority",
        POLICY_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(policy)
    extra = set(policy).difference(required)
    if missing:
        issues.append("memory_policy_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("memory_policy_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if policy["schema_version"] != SCHEMA_VERSION or policy["profile_version"] != PROFILE_VERSION:
        issues.append("memory_policy_profile_invalid")
    expected_bindings = {field: policy["expected_" + field] for field in VERSION_BINDING_FIELDS}
    issues.extend(_validate_binding_fields(expected_bindings, "memory_policy_binding"))
    for field in (
        "expected_source_classification_digest",
        "expected_source_classification_receipt_digest",
        "expected_repair_evidence_packet_digest",
    ):
        if not isinstance(policy[field], str) or SHA256.fullmatch(policy[field]) is None:
            issues.append("memory_policy_digest_invalid:" + field)
    for field in (
        "evaluation_epoch",
        "maximum_request_age",
        "maximum_evidence_age",
        "maximum_memory_entries",
        "maximum_matched_entries",
    ):
        if not positive_int(policy[field]):
            issues.append("memory_policy_positive_integer_invalid:" + field)
    if not unique_strings(policy["allowed_repair_outcomes"], nonempty=True):
        issues.append("memory_policy_outcomes_invalid")
    elif any(item not in REPAIR_OUTCOMES for item in policy["allowed_repair_outcomes"]):
        issues.append("memory_policy_outcome_unknown")
    for field in (
        "require_exact_version_binding",
        "require_complete_typed_error_correspondence",
        "require_independent_verification",
        "require_isolated_candidate_repair",
        "require_live_repository_unchanged",
        "allow_memory_hint",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_execution_authority",
        "allow_git_authority",
    ):
        if not isinstance(policy[field], bool):
            issues.append("memory_policy_boolean_invalid:" + field)
    if not digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("memory_policy_digest_mismatch")
    return sorted(set(issues))


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIVersionBoundRepairMemoryResult",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "digest_ok",
    "mapping",
    "nonnegative_int",
    "positive_int",
    "seal",
    "unique_strings",
    "validate_policy",
    "validate_request",
]
