from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping

from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import (
    CLASSIFICATION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as CLASSIFICATION_RECEIPT_DIGEST_FIELD,
    FAMILY_DEPENDENCY,
    FAMILY_MATERIALIZATION,
    FAMILY_OPERATION_CONFLICT,
    FAMILY_POLICY_MARKER,
    FAMILY_SEMANTIC_NOOP,
    FAMILY_SYNTAX,
    FAMILY_TESTING,
    NOVELTY_NOVEL,
    ROUTE_CURRENT_IR_UNMATERIALIZABLE,
    ROUTE_EXTERNAL_EVIDENCE,
    ROUTE_LOCAL_REPAIR,
    canonical_digest,
    canonical_json,
    digest_without,
    seal,
)

VERSION = "kuuos_codeai_independent_test_strengthening_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Independent Test Strengthening v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_PLAN_ONLY = "independent_test_strengthening_plan_only"
DISPOSITION_COMPLETED = "independent_test_strengthening_completed"

REQUEST_DIGEST_FIELD = "codeai_independent_test_strengthening_request_digest"
POLICY_DIGEST_FIELD = "codeai_independent_test_strengthening_policy_digest"
CAPABILITY_CATALOG_DIGEST_FIELD = "codeai_independent_test_capability_catalog_digest"
OBLIGATION_DIGEST_FIELD = "codeai_independent_test_obligation_digest"
PLAN_DIGEST_FIELD = "codeai_independent_test_strengthening_plan_digest"
RECEIPT_DIGEST_FIELD = "codeai_independent_test_strengthening_receipt_digest"

CATEGORY_BASELINE = "baseline"
CATEGORY_ERROR_SPECIFIC = "error_specific"
CATEGORY_NOVELTY = "novelty"
CATEGORY_ROUTE = "route"
CATEGORY_ERROR_FREE = "error_free"
OBLIGATION_CATEGORIES = (
    CATEGORY_BASELINE,
    CATEGORY_ERROR_SPECIFIC,
    CATEGORY_NOVELTY,
    CATEGORY_ROUTE,
    CATEGORY_ERROR_FREE,
)

CHECK_SOURCE_LINEAGE_REPLAY = "source_lineage_replay"
CHECK_DETERMINISTIC_RECONSTRUCTION = "deterministic_reconstruction"
CHECK_CHANGED_PATH_COVERAGE = "changed_path_coverage"
CHECK_OPERATION_COLLISION_REPLAY = "operation_collision_replay"
CHECK_MATERIALIZATION_REPLAY = "materialization_replay"
CHECK_PARSE_NEGATIVE_CONTROL = "parse_negative_control"
CHECK_DEPENDENCY_CLOSURE = "dependency_closure"
CHECK_TEST_PLAN_COMPLETENESS = "test_plan_completeness"
CHECK_POLICY_MARKER_SCAN = "policy_marker_scan"
CHECK_MATERIAL_EFFECT_ASSERTION = "material_effect_assertion"
CHECK_NOVELTY_FALSIFICATION = "novelty_falsification"
CHECK_ERROR_FREE_MUTATION_PROBE = "error_free_mutation_probe"
CHECK_LOCAL_REPAIR_REGRESSION = "local_repair_regression"
CHECK_EXTERNAL_EVIDENCE_BINDING = "external_evidence_binding"
CHECK_UNMATERIALIZABILITY_REPRODUCTION = "unmaterializability_reproduction"

CHECK_KINDS = (
    CHECK_SOURCE_LINEAGE_REPLAY,
    CHECK_DETERMINISTIC_RECONSTRUCTION,
    CHECK_CHANGED_PATH_COVERAGE,
    CHECK_OPERATION_COLLISION_REPLAY,
    CHECK_MATERIALIZATION_REPLAY,
    CHECK_PARSE_NEGATIVE_CONTROL,
    CHECK_DEPENDENCY_CLOSURE,
    CHECK_TEST_PLAN_COMPLETENESS,
    CHECK_POLICY_MARKER_SCAN,
    CHECK_MATERIAL_EFFECT_ASSERTION,
    CHECK_NOVELTY_FALSIFICATION,
    CHECK_ERROR_FREE_MUTATION_PROBE,
    CHECK_LOCAL_REPAIR_REGRESSION,
    CHECK_EXTERNAL_EVIDENCE_BINDING,
    CHECK_UNMATERIALIZABILITY_REPRODUCTION,
)

BASELINE_CHECKS = (
    CHECK_SOURCE_LINEAGE_REPLAY,
    CHECK_DETERMINISTIC_RECONSTRUCTION,
    CHECK_CHANGED_PATH_COVERAGE,
)

FAMILY_CHECK_KIND = {
    FAMILY_OPERATION_CONFLICT: CHECK_OPERATION_COLLISION_REPLAY,
    FAMILY_MATERIALIZATION: CHECK_MATERIALIZATION_REPLAY,
    FAMILY_SYNTAX: CHECK_PARSE_NEGATIVE_CONTROL,
    FAMILY_DEPENDENCY: CHECK_DEPENDENCY_CLOSURE,
    FAMILY_TESTING: CHECK_TEST_PLAN_COMPLETENESS,
    FAMILY_POLICY_MARKER: CHECK_POLICY_MARKER_SCAN,
    FAMILY_SEMANTIC_NOOP: CHECK_MATERIAL_EFFECT_ASSERTION,
}

ROUTE_CHECK_KIND = {
    ROUTE_LOCAL_REPAIR: CHECK_LOCAL_REPAIR_REGRESSION,
    ROUTE_EXTERNAL_EVIDENCE: CHECK_EXTERNAL_EVIDENCE_BINDING,
    ROUTE_CURRENT_IR_UNMATERIALIZABLE: CHECK_UNMATERIALIZABILITY_REPRODUCTION,
}

CHECK_CATEGORY = {
    **{kind: CATEGORY_BASELINE for kind in BASELINE_CHECKS},
    **{kind: CATEGORY_ERROR_SPECIFIC for kind in FAMILY_CHECK_KIND.values()},
    CHECK_NOVELTY_FALSIFICATION: CATEGORY_NOVELTY,
    CHECK_ERROR_FREE_MUTATION_PROBE: CATEGORY_ERROR_FREE,
    **{kind: CATEGORY_ROUTE for kind in ROUTE_CHECK_KIND.values()},
}

EXPECTED_EVIDENCE = {
    CHECK_SOURCE_LINEAGE_REPLAY: ("exact_source_commit", "classification_digest_correspondence"),
    CHECK_DETERMINISTIC_RECONSTRUCTION: ("repeatable_fixture", "stable_obligation_digest"),
    CHECK_CHANGED_PATH_COVERAGE: ("changed_path_inventory", "test_to_path_correspondence"),
    CHECK_OPERATION_COLLISION_REPLAY: ("conflicting_operation_witness", "collision_reproduction"),
    CHECK_MATERIALIZATION_REPLAY: ("exact_snapshot", "materialization_outcome"),
    CHECK_PARSE_NEGATIVE_CONTROL: ("parser_or_compiler_invocation", "negative_control_rejection"),
    CHECK_DEPENDENCY_CLOSURE: ("resolved_dependency_inventory", "locked_environment"),
    CHECK_TEST_PLAN_COMPLETENESS: ("required_test_plan_ids", "coverage_gap_closure"),
    CHECK_POLICY_MARKER_SCAN: ("forbidden_marker_scan", "marker_location_evidence"),
    CHECK_MATERIAL_EFFECT_ASSERTION: ("before_after_digest", "material_effect_witness"),
    CHECK_NOVELTY_FALSIFICATION: ("novel_error_challenge", "falsification_outcome"),
    CHECK_ERROR_FREE_MUTATION_PROBE: ("seeded_fault", "independent_detection_outcome"),
    CHECK_LOCAL_REPAIR_REGRESSION: ("pre_repair_failure", "post_repair_regression_result"),
    CHECK_EXTERNAL_EVIDENCE_BINDING: ("external_evidence_digest", "authority_owner_identity"),
    CHECK_UNMATERIALIZABILITY_REPRODUCTION: ("exact_ir_digest", "non_materialization_reproduction"),
}

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class CodeAIIndependentTestStrengtheningResult:
    status: str
    issues: tuple[str, ...]
    plan: dict[str, Any] | None
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


def validate_request(request: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "strengthening_id",
        "strengthening_revision",
        "repository_full_name",
        "source_commit_sha",
        "source_classification_digest",
        "source_classification_receipt_digest",
        "capability_catalog_digest",
        "request_created_epoch",
        "unresolved_strengthening_questions",
        "claims_authority",
        REQUEST_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(request)
    extra = set(request).difference(required)
    if missing:
        issues.append("strengthening_request_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("strengthening_request_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if request["schema_version"] != SCHEMA_VERSION or request["profile_version"] != PROFILE_VERSION:
        issues.append("strengthening_request_profile_invalid")
    for field in ("strengthening_id", "strengthening_revision", "repository_full_name"):
        if not isinstance(request[field], str) or not request[field]:
            issues.append("strengthening_request_string_invalid:" + field)
    if not isinstance(request["source_commit_sha"], str) or SHA40.fullmatch(request["source_commit_sha"]) is None:
        issues.append("strengthening_request_source_commit_invalid")
    for field in (
        "source_classification_digest",
        "source_classification_receipt_digest",
        "capability_catalog_digest",
    ):
        if not isinstance(request[field], str) or SHA256.fullmatch(request[field]) is None:
            issues.append("strengthening_request_digest_invalid:" + field)
    if not nonnegative_int(request["request_created_epoch"]):
        issues.append("strengthening_request_epoch_invalid")
    if not unique_strings(request["unresolved_strengthening_questions"]):
        issues.append("strengthening_request_questions_invalid")
    if not isinstance(request["claims_authority"], bool):
        issues.append("strengthening_request_authority_invalid")
    if not digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("strengthening_request_digest_mismatch")
    return sorted(set(issues))


def validate_policy(policy: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "expected_repository_full_name",
        "expected_source_commit_sha",
        "expected_source_classification_digest",
        "expected_source_classification_receipt_digest",
        "expected_capability_catalog_digest",
        "evaluation_epoch",
        "maximum_request_age",
        "maximum_candidates",
        "maximum_obligations",
        "require_exact_lineage",
        "require_baseline_obligations",
        "require_independent_runner",
        "require_isolated_execution",
        "require_falsification_for_novel_errors",
        "require_error_free_mutation_probe",
        "require_route_specific_obligations",
        "allow_test_generation",
        "allow_test_execution",
        "allow_candidate_selection",
        "allow_verification_authority",
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
        issues.append("strengthening_policy_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("strengthening_policy_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if policy["schema_version"] != SCHEMA_VERSION or policy["profile_version"] != PROFILE_VERSION:
        issues.append("strengthening_policy_profile_invalid")
    if not isinstance(policy["expected_repository_full_name"], str) or not policy["expected_repository_full_name"]:
        issues.append("strengthening_policy_repository_invalid")
    if not isinstance(policy["expected_source_commit_sha"], str) or SHA40.fullmatch(policy["expected_source_commit_sha"]) is None:
        issues.append("strengthening_policy_source_commit_invalid")
    for field in (
        "expected_source_classification_digest",
        "expected_source_classification_receipt_digest",
        "expected_capability_catalog_digest",
    ):
        if not isinstance(policy[field], str) or SHA256.fullmatch(policy[field]) is None:
            issues.append("strengthening_policy_digest_invalid:" + field)
    for field in ("evaluation_epoch", "maximum_request_age", "maximum_candidates", "maximum_obligations"):
        if not positive_int(policy[field]):
            issues.append("strengthening_policy_positive_integer_invalid:" + field)
    for field in (
        "require_exact_lineage",
        "require_baseline_obligations",
        "require_independent_runner",
        "require_isolated_execution",
        "require_falsification_for_novel_errors",
        "require_error_free_mutation_probe",
        "require_route_specific_obligations",
        "allow_test_generation",
        "allow_test_execution",
        "allow_candidate_selection",
        "allow_verification_authority",
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_execution_authority",
        "allow_git_authority",
    ):
        if not isinstance(policy[field], bool):
            issues.append("strengthening_policy_boolean_invalid:" + field)
    if not digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("strengthening_policy_digest_mismatch")
    return sorted(set(issues))


def validate_capability_catalog(catalog: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "catalog_id",
        "catalog_revision",
        "supported_check_kinds",
        "capability_count",
        "check_capabilities",
        "test_generation_performed",
        "test_execution_performed",
        "verification_authority_granted",
        "repository_mutation_performed",
        "git_effect_performed",
        CAPABILITY_CATALOG_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(catalog)
    extra = set(catalog).difference(required)
    if missing:
        issues.append("capability_catalog_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("capability_catalog_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if catalog["schema_version"] != SCHEMA_VERSION or catalog["profile_version"] != PROFILE_VERSION:
        issues.append("capability_catalog_profile_invalid")
    for field in ("catalog_id", "catalog_revision"):
        if not isinstance(catalog[field], str) or not catalog[field]:
            issues.append("capability_catalog_string_invalid:" + field)
    if not unique_strings(catalog["supported_check_kinds"]):
        issues.append("capability_catalog_supported_kinds_invalid")
    elif catalog["supported_check_kinds"] != sorted(catalog["supported_check_kinds"]):
        issues.append("capability_catalog_supported_kinds_not_sorted")
    elif any(kind not in CHECK_KINDS for kind in catalog["supported_check_kinds"]):
        issues.append("capability_catalog_unknown_check_kind")
    capabilities = catalog["check_capabilities"]
    if not isinstance(capabilities, list):
        issues.append("capability_catalog_capabilities_invalid")
        capabilities = []
    required_capability_fields = {
        "check_kind",
        "runner_profile",
        "evidence_format",
        "independent_runner",
        "isolated_execution",
        "mutation_capable",
        "falsification_capable",
    }
    seen: list[str] = []
    for index, capability in enumerate(capabilities):
        if not isinstance(capability, Mapping):
            issues.append(f"capability_catalog_entry_not_mapping:{index}")
            continue
        if set(capability) != required_capability_fields:
            issues.append(f"capability_catalog_entry_fields_invalid:{index}")
            continue
        kind = capability["check_kind"]
        if not isinstance(kind, str) or kind not in CHECK_KINDS:
            issues.append(f"capability_catalog_entry_kind_invalid:{index}")
        else:
            seen.append(kind)
        for field in ("runner_profile", "evidence_format"):
            if not isinstance(capability[field], str) or not capability[field]:
                issues.append(f"capability_catalog_entry_string_invalid:{index}:{field}")
        for field in ("independent_runner", "isolated_execution", "mutation_capable", "falsification_capable"):
            if not isinstance(capability[field], bool):
                issues.append(f"capability_catalog_entry_boolean_invalid:{index}:{field}")
    if len(seen) != len(set(seen)):
        issues.append("capability_catalog_duplicate_check_kind")
    if set(seen) != set(catalog["supported_check_kinds"]):
        issues.append("capability_catalog_supported_kind_correspondence_invalid")
    if not nonnegative_int(catalog["capability_count"]) or catalog["capability_count"] != len(capabilities):
        issues.append("capability_catalog_count_invalid")
    for field in (
        "test_generation_performed",
        "test_execution_performed",
        "verification_authority_granted",
        "repository_mutation_performed",
        "git_effect_performed",
    ):
        if catalog[field] is not False:
            issues.append("capability_catalog_effect_or_authority_present:" + field)
    if not digest_ok(catalog, CAPABILITY_CATALOG_DIGEST_FIELD):
        issues.append("capability_catalog_digest_mismatch")
    return sorted(set(issues))


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIIndependentTestStrengtheningResult",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "digest_ok",
    "mapping",
    "nonnegative_int",
    "positive_int",
    "seal",
    "unique_strings",
    "validate_capability_catalog",
    "validate_policy",
    "validate_request",
]
