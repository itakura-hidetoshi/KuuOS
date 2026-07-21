from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_codeai_trajectory_grounded_specialist_router_admission_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Trajectory-Grounded Specialist Router Admission v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_ADMISSION_ONLY = "trajectory_grounded_specialist_router_admission_only"
DISPOSITION_COMPLETED = "trajectory_grounded_specialist_router_admission_completed"

SUBTASK_KINDS = ("localize", "diagnose", "edit", "verify")
SPECIALIST_KINDS = ("formal", "behavioral", "adversarial", "maintainability")
DECISION_ADMIT = "specialist_route_admitted"
DECISION_HOLD = "specialist_route_held"

REQUEST_DIGEST_FIELD = "codeai_trajectory_grounded_specialist_router_request_digest"
POLICY_DIGEST_FIELD = "codeai_trajectory_grounded_specialist_router_policy_digest"
TRAJECTORY_DIGEST_FIELD = "codeai_trajectory_grounded_specialist_router_trajectory_digest"
SPECIALIST_DIGEST_FIELD = "codeai_trajectory_grounded_specialist_router_specialist_digest"
PACK_DIGEST_FIELD = "codeai_trajectory_grounded_specialist_router_admission_pack_digest"
RECEIPT_DIGEST_FIELD = "codeai_trajectory_grounded_specialist_router_admission_receipt_digest"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]{1,127}$")

BINDING_FIELDS = (
    "repository_full_name",
    "source_commit_sha",
    "source_tree_digest",
    "memory_pack_digest",
    "memory_receipt_digest",
    "subtask_kind",
    "subtask_contract_digest",
    "predecessor_output_digest",
    "dependency_slice_digest",
    "toolchain_digest",
    "environment_digest",
    "trajectory_contract_digest",
    "routing_policy_digest",
)

@dataclass(frozen=True)
class CodeAITrajectoryGroundedSpecialistRouterAdmissionResult:
    status: str
    issues: tuple[str, ...]
    admission_pack: dict[str, Any] | None
    receipt: dict[str, Any] | None


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return canonical_digest({key: item for key, item in value.items() if key != field})


def seal(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result[field] = digest_without(result, field)
    return result


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


def _validate_binding(value: Mapping[str, Any], prefix: str) -> list[str]:
    issues: list[str] = []
    if not isinstance(value.get("repository_full_name"), str) or not value["repository_full_name"]:
        issues.append(prefix + "_repository_invalid")
    if not isinstance(value.get("source_commit_sha"), str) or SHA40.fullmatch(value["source_commit_sha"]) is None:
        issues.append(prefix + "_source_commit_invalid")
    for field in (
        "source_tree_digest", "memory_pack_digest", "memory_receipt_digest",
        "subtask_contract_digest", "predecessor_output_digest", "dependency_slice_digest",
        "toolchain_digest", "environment_digest", "trajectory_contract_digest",
        "routing_policy_digest",
    ):
        item = value.get(field)
        if not isinstance(item, str) or SHA256.fullmatch(item) is None:
            issues.append(prefix + "_digest_invalid:" + field)
    if value.get("subtask_kind") not in SUBTASK_KINDS:
        issues.append(prefix + "_subtask_kind_invalid")
    return issues


def validate_request(request: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version", "profile_version", "request_id", "request_revision",
        *BINDING_FIELDS, "requested_specialist_kinds", "request_created_epoch",
        "unresolved_questions", "claims_selection_authority", "claims_dispatch_authority",
        "claims_execution_authority", "claims_repository_mutation_authority",
        "claims_git_authority", REQUEST_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(request)
    extra = set(request).difference(required)
    if missing:
        issues.append("request_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("request_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if request["schema_version"] != SCHEMA_VERSION or request["profile_version"] != PROFILE_VERSION:
        issues.append("request_profile_invalid")
    for field in ("request_id", "request_revision"):
        if not isinstance(request[field], str) or IDENTIFIER.fullmatch(request[field]) is None:
            issues.append("request_identifier_invalid:" + field)
    issues.extend(_validate_binding(request, "request_binding"))
    if not unique_strings(request["requested_specialist_kinds"], nonempty=True):
        issues.append("request_specialists_invalid")
    elif any(item not in SPECIALIST_KINDS for item in request["requested_specialist_kinds"]):
        issues.append("request_specialists_unknown")
    if not nonnegative_int(request["request_created_epoch"]):
        issues.append("request_epoch_invalid")
    if not unique_strings(request["unresolved_questions"]):
        issues.append("request_questions_invalid")
    for field in (
        "claims_selection_authority", "claims_dispatch_authority", "claims_execution_authority",
        "claims_repository_mutation_authority", "claims_git_authority",
    ):
        if not isinstance(request[field], bool):
            issues.append("request_boolean_invalid:" + field)
    if not digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("request_digest_mismatch")
    return sorted(set(issues))


def validate_policy(policy: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version", "profile_version",
        *{"expected_" + field for field in BINDING_FIELDS},
        "evaluation_epoch", "maximum_request_age", "maximum_trajectory_age",
        "maximum_evidence_age", "maximum_candidates", "minimum_exploration_turns",
        "minimum_observation_count", "minimum_execution_signal_count",
        "minimum_grounding_sources", "minimum_observable_artifacts", "minimum_fit_score",
        "minimum_reliability_score", "maximum_cost_units", "minimum_route_margin",
        "require_exact_binding", "require_partial_trajectory", "require_observable_artifacts",
        "require_independent_measurement", "require_specialist_alignment",
        "require_memory_pack_binding", "allow_route_hint", "allow_specialist_dispatch",
        "allow_candidate_selection", "allow_execution_authority",
        "allow_repository_mutation", "allow_git_authority", POLICY_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(policy)
    extra = set(policy).difference(required)
    if missing:
        issues.append("policy_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("policy_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if policy["schema_version"] != SCHEMA_VERSION or policy["profile_version"] != PROFILE_VERSION:
        issues.append("policy_profile_invalid")
    expected = {field: policy["expected_" + field] for field in BINDING_FIELDS}
    issues.extend(_validate_binding(expected, "policy_binding"))
    for field in (
        "evaluation_epoch", "maximum_request_age", "maximum_trajectory_age", "maximum_evidence_age",
        "maximum_candidates", "minimum_exploration_turns", "minimum_observation_count",
        "minimum_execution_signal_count", "minimum_grounding_sources", "minimum_observable_artifacts",
        "minimum_fit_score", "minimum_reliability_score", "maximum_cost_units",
        "minimum_route_margin",
    ):
        if not positive_int(policy[field]):
            issues.append("policy_positive_integer_invalid:" + field)
    for field in (
        "require_exact_binding", "require_partial_trajectory", "require_observable_artifacts",
        "require_independent_measurement", "require_specialist_alignment",
        "require_memory_pack_binding", "allow_route_hint", "allow_specialist_dispatch",
        "allow_candidate_selection", "allow_execution_authority", "allow_repository_mutation",
        "allow_git_authority",
    ):
        if not isinstance(policy[field], bool):
            issues.append("policy_boolean_invalid:" + field)
    if not digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("policy_digest_mismatch")
    return sorted(set(issues))


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAITrajectoryGroundedSpecialistRouterAdmissionResult", "canonical_digest",
    "canonical_json", "digest_without", "digest_ok", "mapping", "nonnegative_int",
    "positive_int", "seal", "unique_strings", "validate_policy", "validate_request",
]
