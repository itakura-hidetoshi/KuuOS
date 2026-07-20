from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping

from runtime.kuuos_codeai_candidate_static_admissibility_preflight_schema_v0_1 import (
    DISPOSITION_ADMISSIBLE,
    DISPOSITION_HOLD,
    DISPOSITION_REJECTED,
    DISPOSITION_REPAIRABLE,
    SEVERITY_HOLD,
    SEVERITY_REJECT,
    SEVERITY_REPAIRABLE,
)
from runtime.kuuos_codeai_evidence_bearing_candidate_portfolio_schema_v0_1 import (
    PORTFOLIO_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as PORTFOLIO_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    canonical_json,
    digest_without,
    seal,
)
from runtime.kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1 import (
    EVIDENCE_DIGEST_FIELD as BASELINE_EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as BASELINE_RECEIPT_DIGEST_FIELD,
)

VERSION = "kuuos_codeai_typed_error_classification_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Typed Error Classification v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_CLASSIFICATION_ONLY = "typed_error_classification_only"
DISPOSITION_COMPLETED = "typed_error_classification_completed"

REQUEST_DIGEST_FIELD = "codeai_typed_error_classification_request_digest"
POLICY_DIGEST_FIELD = "codeai_typed_error_classification_policy_digest"
CLASSIFICATION_DIGEST_FIELD = "codeai_typed_error_classification_digest"
RECEIPT_DIGEST_FIELD = "codeai_typed_error_classification_receipt_digest"

FAMILY_OPERATION_CONFLICT = "operation_conflict"
FAMILY_MATERIALIZATION = "materialization"
FAMILY_SYNTAX = "syntax"
FAMILY_DEPENDENCY = "dependency"
FAMILY_TESTING = "testing"
FAMILY_POLICY_MARKER = "policy_marker"
FAMILY_SEMANTIC_NOOP = "semantic_noop"
ERROR_FAMILIES = (
    FAMILY_OPERATION_CONFLICT,
    FAMILY_MATERIALIZATION,
    FAMILY_SYNTAX,
    FAMILY_DEPENDENCY,
    FAMILY_TESTING,
    FAMILY_POLICY_MARKER,
    FAMILY_SEMANTIC_NOOP,
)

STAGE_TYPED_OPERATION = "typed_operation"
STAGE_MATERIALIZATION = "materialization"
STAGE_PARSE = "parse"
STAGE_DEPENDENCY_CORRESPONDENCE = "dependency_correspondence"
STAGE_TEST_PLAN_CORRESPONDENCE = "test_plan_correspondence"
STAGE_POLICY_MARKER = "policy_marker"
STAGE_MATERIAL_EFFECT = "material_effect"
ERROR_STAGES = (
    STAGE_TYPED_OPERATION,
    STAGE_MATERIALIZATION,
    STAGE_PARSE,
    STAGE_DEPENDENCY_CORRESPONDENCE,
    STAGE_TEST_PLAN_CORRESPONDENCE,
    STAGE_POLICY_MARKER,
    STAGE_MATERIAL_EFFECT,
)

ROUTE_LOCAL_REPAIR = "local_candidate_repair"
ROUTE_EXTERNAL_EVIDENCE = "external_evidence_required"
ROUTE_CURRENT_IR_UNMATERIALIZABLE = "current_ir_unmaterializable"
REPAIR_ROUTES = (
    ROUTE_LOCAL_REPAIR,
    ROUTE_EXTERNAL_EVIDENCE,
    ROUTE_CURRENT_IR_UNMATERIALIZABLE,
)

NOVELTY_KNOWN = "known_in_replay_baseline"
NOVELTY_NOVEL = "novel_to_replay_baseline"
NOVELTY_STATUSES = (NOVELTY_KNOWN, NOVELTY_NOVEL)

CLASSIFICATIONS = (
    DISPOSITION_ADMISSIBLE,
    DISPOSITION_REPAIRABLE,
    DISPOSITION_HOLD,
    DISPOSITION_REJECTED,
)
SEVERITIES = (SEVERITY_REPAIRABLE, SEVERITY_HOLD, SEVERITY_REJECT)
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
FINGERPRINT = re.compile(r"^[A-Z][A-Z0-9_]{2,95}$")

FINDING_TAXONOMY: dict[str, tuple[str, str]] = {
    "create_path_operation_collision": (FAMILY_OPERATION_CONFLICT, STAGE_TYPED_OPERATION),
    "operation_range_collision": (FAMILY_OPERATION_CONFLICT, STAGE_TYPED_OPERATION),
    "create_path_already_exists": (FAMILY_MATERIALIZATION, STAGE_MATERIALIZATION),
    "existing_target_missing": (FAMILY_MATERIALIZATION, STAGE_MATERIALIZATION),
    "source_file_digest_mismatch": (FAMILY_MATERIALIZATION, STAGE_MATERIALIZATION),
    "insertion_line_out_of_range": (FAMILY_MATERIALIZATION, STAGE_MATERIALIZATION),
    "replacement_line_out_of_range": (FAMILY_MATERIALIZATION, STAGE_MATERIALIZATION),
    "materialized_text_not_canonical": (FAMILY_MATERIALIZATION, STAGE_MATERIALIZATION),
    "python_parse_failed": (FAMILY_SYNTAX, STAGE_PARSE),
    "lean_lexical_structure_unbalanced": (FAMILY_SYNTAX, STAGE_PARSE),
    "lean_duplicate_top_level_declaration": (FAMILY_SYNTAX, STAGE_PARSE),
    "internal_python_import_unresolved": (FAMILY_DEPENDENCY, STAGE_DEPENDENCY_CORRESPONDENCE),
    "external_python_dependency_unaccounted": (FAMILY_DEPENDENCY, STAGE_DEPENDENCY_CORRESPONDENCE),
    "internal_lean_import_unresolved": (FAMILY_DEPENDENCY, STAGE_DEPENDENCY_CORRESPONDENCE),
    "external_lean_dependency_unaccounted": (FAMILY_DEPENDENCY, STAGE_DEPENDENCY_CORRESPONDENCE),
    "test_plan_missing_from_catalog": (FAMILY_TESTING, STAGE_TEST_PLAN_CORRESPONDENCE),
    "changed_path_without_test_plan_coverage": (FAMILY_TESTING, STAGE_TEST_PLAN_CORRESPONDENCE),
    "forbidden_new_text_marker": (FAMILY_POLICY_MARKER, STAGE_POLICY_MARKER),
    "operation_has_no_material_effect": (FAMILY_SEMANTIC_NOOP, STAGE_MATERIAL_EFFECT),
}


@dataclass(frozen=True)
class CodeAITypedErrorClassificationResult:
    status: str
    issues: tuple[str, ...]
    classification: dict[str, Any] | None
    receipt: dict[str, Any] | None


def mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def digest_ok(value: Mapping[str, Any], field: str) -> bool:
    digest = value.get(field)
    return isinstance(digest, str) and SHA256.fullmatch(digest) is not None and digest == digest_without(value, field)


def unique_strings(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value))
        and (bool(value) or not nonempty)
    )


def nonnegative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def positive_int(value: Any) -> bool:
    return nonnegative_int(value) and value > 0


def fingerprint_for(code: str) -> str:
    return code.upper()


def repair_route_for(severity: str) -> str:
    return {
        SEVERITY_REPAIRABLE: ROUTE_LOCAL_REPAIR,
        SEVERITY_HOLD: ROUTE_EXTERNAL_EVIDENCE,
        SEVERITY_REJECT: ROUTE_CURRENT_IR_UNMATERIALIZABLE,
    }[severity]


def validate_request(request: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    required = {
        "schema_version",
        "profile_version",
        "classification_id",
        "classification_revision",
        "repository_full_name",
        "source_commit_sha",
        "source_portfolio_digest",
        "source_portfolio_receipt_digest",
        "baseline_evidence_digest",
        "baseline_receipt_digest",
        "request_created_epoch",
        "unresolved_classification_questions",
        "claims_authority",
        REQUEST_DIGEST_FIELD,
    }
    missing = required.difference(request)
    extra = set(request).difference(required)
    if missing:
        issues.append("classification_request_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("classification_request_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if request["schema_version"] != SCHEMA_VERSION or request["profile_version"] != PROFILE_VERSION:
        issues.append("classification_request_profile_invalid")
    for field in ("classification_id", "classification_revision", "repository_full_name"):
        if not isinstance(request[field], str) or not request[field]:
            issues.append("classification_request_string_invalid:" + field)
    if not isinstance(request["source_commit_sha"], str) or SHA40.fullmatch(request["source_commit_sha"]) is None:
        issues.append("classification_request_source_commit_invalid")
    for field in (
        "source_portfolio_digest",
        "source_portfolio_receipt_digest",
        "baseline_evidence_digest",
        "baseline_receipt_digest",
    ):
        if not isinstance(request[field], str) or SHA256.fullmatch(request[field]) is None:
            issues.append("classification_request_digest_invalid:" + field)
    if not nonnegative_int(request["request_created_epoch"]):
        issues.append("classification_request_epoch_invalid")
    if not unique_strings(request["unresolved_classification_questions"]):
        issues.append("classification_request_questions_invalid")
    if not isinstance(request["claims_authority"], bool):
        issues.append("classification_request_authority_invalid")
    if not digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("classification_request_digest_mismatch")
    return sorted(set(issues))


def validate_policy(policy: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    required = {
        "schema_version",
        "profile_version",
        "expected_repository_full_name",
        "expected_source_commit_sha",
        "expected_source_portfolio_digest",
        "expected_source_portfolio_receipt_digest",
        "expected_baseline_evidence_digest",
        "expected_baseline_receipt_digest",
        "evaluation_epoch",
        "maximum_request_age",
        "maximum_candidates",
        "maximum_typed_errors",
        "require_exact_lineage",
        "require_complete_taxonomy",
        "require_finding_evidence_preservation",
        "allow_ranking",
        "allow_candidate_selection",
        "allow_verification_runner_invocation",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_execution_authority",
        "allow_git_authority",
        POLICY_DIGEST_FIELD,
    }
    missing = required.difference(policy)
    extra = set(policy).difference(required)
    if missing:
        issues.append("classification_policy_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("classification_policy_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if policy["schema_version"] != SCHEMA_VERSION or policy["profile_version"] != PROFILE_VERSION:
        issues.append("classification_policy_profile_invalid")
    for field in ("expected_repository_full_name",):
        if not isinstance(policy[field], str) or not policy[field]:
            issues.append("classification_policy_string_invalid:" + field)
    if not isinstance(policy["expected_source_commit_sha"], str) or SHA40.fullmatch(policy["expected_source_commit_sha"]) is None:
        issues.append("classification_policy_source_commit_invalid")
    for field in (
        "expected_source_portfolio_digest",
        "expected_source_portfolio_receipt_digest",
        "expected_baseline_evidence_digest",
        "expected_baseline_receipt_digest",
    ):
        if not isinstance(policy[field], str) or SHA256.fullmatch(policy[field]) is None:
            issues.append("classification_policy_digest_invalid:" + field)
    for field in ("evaluation_epoch", "maximum_request_age", "maximum_candidates", "maximum_typed_errors"):
        if not positive_int(policy[field]):
            issues.append("classification_policy_positive_integer_invalid:" + field)
    for field in (
        "require_exact_lineage",
        "require_complete_taxonomy",
        "require_finding_evidence_preservation",
        "allow_ranking",
        "allow_candidate_selection",
        "allow_verification_runner_invocation",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_execution_authority",
        "allow_git_authority",
    ):
        if not isinstance(policy[field], bool):
            issues.append("classification_policy_boolean_invalid:" + field)
    if not digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("classification_policy_digest_mismatch")
    return sorted(set(issues))


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAITypedErrorClassificationResult",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "digest_ok",
    "fingerprint_for",
    "mapping",
    "repair_route_for",
    "seal",
    "unique_strings",
    "validate_policy",
    "validate_request",
]
