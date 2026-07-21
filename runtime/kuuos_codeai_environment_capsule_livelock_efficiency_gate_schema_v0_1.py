from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_codeai_environment_capsule_livelock_efficiency_gate_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Environment Capsule and Livelock-Efficiency Gate v0.1"
PREDECESSOR_PROFILE_VERSION = "CodeAI Trajectory-Grounded Specialist Router Admission v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_GATE_ONLY = "environment_capsule_livelock_efficiency_gate_only"
DISPOSITION_COMPLETED = "environment_capsule_livelock_efficiency_gate_completed"

SUBTASK_KINDS = ("localize", "diagnose", "edit", "verify")
SPECIALIST_KINDS = ("formal", "behavioral", "adversarial", "maintainability")
CHECKPOINT_PHASES = ("observe", "plan", "execute", "verify", "govern")
DECISION_CONTINUE = "progress_efficiency_admitted"
DECISION_HOLD = "progress_efficiency_held"

REQUEST_DIGEST_FIELD = "codeai_environment_capsule_livelock_efficiency_request_digest"
POLICY_DIGEST_FIELD = "codeai_environment_capsule_livelock_efficiency_policy_digest"
CAPSULE_DIGEST_FIELD = "codeai_environment_capsule_digest"
TRACE_DIGEST_FIELD = "codeai_progress_efficiency_trace_digest"
PACK_DIGEST_FIELD = "codeai_environment_capsule_livelock_efficiency_gate_pack_digest"
RECEIPT_DIGEST_FIELD = "codeai_environment_capsule_livelock_efficiency_gate_receipt_digest"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]{1,127}$")
VERSION_TEXT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:+/-]{0,127}$")

BINDING_FIELDS = (
    "repository_full_name",
    "source_commit_sha",
    "source_tree_digest",
    "router_admission_manifest_digest",
    "router_admission_pack_digest",
    "router_admission_receipt_digest",
    "selected_specialist_id",
    "selected_specialist_kind",
    "selected_subtask_kind",
    "dependency_slice_digest",
    "toolchain_digest",
    "environment_contract_digest",
    "progress_contract_digest",
    "gate_policy_digest",
)


@dataclass(frozen=True)
class CodeAIEnvironmentCapsuleLivelockEfficiencyGateResult:
    status: str
    issues: tuple[str, ...]
    gate_pack: dict[str, Any] | None
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
        "source_tree_digest",
        "router_admission_manifest_digest",
        "router_admission_pack_digest",
        "router_admission_receipt_digest",
        "dependency_slice_digest",
        "toolchain_digest",
        "environment_contract_digest",
        "progress_contract_digest",
        "gate_policy_digest",
    ):
        item = value.get(field)
        if not isinstance(item, str) or SHA256.fullmatch(item) is None:
            issues.append(prefix + "_digest_invalid:" + field)
    for field in ("selected_specialist_id",):
        item = value.get(field)
        if not isinstance(item, str) or IDENTIFIER.fullmatch(item) is None:
            issues.append(prefix + "_identifier_invalid:" + field)
    if value.get("selected_specialist_kind") not in SPECIALIST_KINDS:
        issues.append(prefix + "_specialist_kind_invalid")
    if value.get("selected_subtask_kind") not in SUBTASK_KINDS:
        issues.append(prefix + "_subtask_kind_invalid")
    return issues


def validate_request(request: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "request_id",
        "request_revision",
        *BINDING_FIELDS,
        "request_created_epoch",
        "unresolved_questions",
        "claims_continuation_authority",
        "claims_execution_authority",
        "claims_repository_mutation_authority",
        "claims_git_authority",
        "claims_correctness",
        REQUEST_DIGEST_FIELD,
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
    if not nonnegative_int(request["request_created_epoch"]):
        issues.append("request_epoch_invalid")
    if not unique_strings(request["unresolved_questions"]):
        issues.append("request_questions_invalid")
    for field in (
        "claims_continuation_authority",
        "claims_execution_authority",
        "claims_repository_mutation_authority",
        "claims_git_authority",
        "claims_correctness",
    ):
        if not isinstance(request[field], bool):
            issues.append("request_boolean_invalid:" + field)
    if not digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("request_digest_mismatch")
    return sorted(set(issues))


def validate_policy(policy: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        *{"expected_" + field for field in BINDING_FIELDS},
        "evaluation_epoch",
        "maximum_request_age",
        "maximum_capsule_age",
        "maximum_trace_age",
        "maximum_steps",
        "maximum_tool_calls",
        "maximum_model_calls",
        "maximum_token_units",
        "maximum_wall_clock_ms",
        "maximum_failed_actions",
        "maximum_no_progress_streak",
        "maximum_repeated_zero_progress_transitions",
        "maximum_cycle_count",
        "minimum_total_progress_units",
        "minimum_distinct_state_count",
        "require_exact_binding",
        "require_immutable_capsule",
        "require_complete_capsule",
        "require_observed_capsule",
        "require_dependency_lock",
        "require_network_disabled",
        "require_observable_trace",
        "require_cycle_free",
        "allow_continuation_hint",
        "allow_continuation_authority",
        "allow_execution_authority",
        "allow_repository_mutation",
        "allow_git_authority",
        "allow_correctness_claim",
        POLICY_DIGEST_FIELD,
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
        "evaluation_epoch",
        "maximum_request_age",
        "maximum_capsule_age",
        "maximum_trace_age",
        "maximum_steps",
        "maximum_tool_calls",
        "maximum_model_calls",
        "maximum_token_units",
        "maximum_wall_clock_ms",
        "maximum_failed_actions",
        "maximum_no_progress_streak",
        "maximum_repeated_zero_progress_transitions",
        "maximum_cycle_count",
        "minimum_total_progress_units",
        "minimum_distinct_state_count",
    ):
        if not nonnegative_int(policy[field]):
            issues.append("policy_integer_invalid:" + field)
    for field in (
        "maximum_request_age",
        "maximum_capsule_age",
        "maximum_trace_age",
        "maximum_steps",
        "maximum_tool_calls",
        "maximum_model_calls",
        "maximum_token_units",
        "maximum_wall_clock_ms",
        "minimum_total_progress_units",
        "minimum_distinct_state_count",
    ):
        if not positive_int(policy[field]):
            issues.append("policy_positive_integer_invalid:" + field)
    for field in (
        "require_exact_binding",
        "require_immutable_capsule",
        "require_complete_capsule",
        "require_observed_capsule",
        "require_dependency_lock",
        "require_network_disabled",
        "require_observable_trace",
        "require_cycle_free",
        "allow_continuation_hint",
        "allow_continuation_authority",
        "allow_execution_authority",
        "allow_repository_mutation",
        "allow_git_authority",
        "allow_correctness_claim",
    ):
        if not isinstance(policy[field], bool):
            issues.append("policy_boolean_invalid:" + field)
    if not digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("policy_digest_mismatch")
    return sorted(set(issues))


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIEnvironmentCapsuleLivelockEfficiencyGateResult",
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
