#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import canonical_digest, seal

VERSION = "kuuos_codeai_autonomous_verification_execution_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Autonomous Verification Execution v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_BOUNDED_ISOLATED_EXECUTION = "bounded_isolated_verification_execution"
DISPOSITION_COMPLETED = "verification_execution_completed"
DISPOSITION_COMPLETED_WITH_FAILURES = "verification_execution_completed_with_failures"
DISPOSITION_ABORTED_BY_BUDGET = "verification_execution_aborted_by_runtime_budget"

CANDIDATE_RECEIPT_DIGEST_FIELD = "codeai_candidate_patch_receipt_digest"
CANDIDATE_DIGEST_FIELD = "codeai_candidate_patch_digest"
APPLICATION_RECEIPT_DIGEST_FIELD = (
    "codeai_autonomous_isolated_candidate_application_receipt_digest"
)
PLAN_DIGEST_FIELD = "codeai_autonomous_verification_execution_plan_digest"
REQUEST_DIGEST_FIELD = "codeai_autonomous_verification_execution_request_digest"
POLICY_DIGEST_FIELD = "codeai_autonomous_verification_execution_policy_digest"
EVIDENCE_BUNDLE_DIGEST_FIELD = (
    "codeai_autonomous_verification_execution_evidence_bundle_digest"
)
RECEIPT_DIGEST_FIELD = "codeai_autonomous_verification_execution_receipt_digest"
INDEPENDENT_EVIDENCE_DIGEST_FIELD = "codeai_independent_verification_evidence_digest"

_CHECK_FIELDS = {
    "check_id",
    "executable",
    "arguments",
    "workdir",
    "timeout_seconds",
    "expected_exit_codes",
    "environment",
}
_PLAN_FIELDS = {
    "plan_id",
    "plan_revision",
    "checks",
    "plan_created_epoch",
    PLAN_DIGEST_FIELD,
}
_REQUEST_FIELDS = {
    "execution_request_id",
    "execution_request_revision",
    "source_candidate_receipt_digest",
    "source_application_receipt_digest",
    "candidate_digest",
    "patch_artifact_digest",
    "source_repository_snapshot_digest",
    "resulting_repository_snapshot_digest",
    "repository_full_name",
    "source_commit_sha",
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
    "expected_source_candidate_receipt_digest",
    "expected_source_application_receipt_digest",
    "expected_candidate_digest",
    "expected_patch_artifact_digest",
    "expected_source_repository_snapshot_digest",
    "expected_resulting_repository_snapshot_digest",
    "expected_repository_full_name",
    "expected_source_commit_sha",
    "expected_verification_plan_digest",
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
    "maximum_repository_path_count",
    "maximum_repository_snapshot_bytes",
    "network_access_allowed",
    "secrets_allowed",
    "live_repository_access_allowed",
    "git_operations_allowed",
    "evaluation_epoch",
    "maximum_request_age",
    POLICY_DIGEST_FIELD,
}
_RUNNER_RESULT_FIELDS = {
    "runner_id",
    "runner_session_id",
    "check_id",
    "exit_code",
    "stdout",
    "stderr",
    "duration_ms",
    "timed_out",
    "exception_type",
    "started_epoch",
    "completed_epoch",
    "network_used",
    "secret_accessed",
    "live_repository_accessed",
    "git_effect_performed",
}


@dataclass(frozen=True)
class VerificationExecutionInvocation:
    check_id: str
    executable: str
    arguments: tuple[str, ...]
    workdir: str
    timeout_seconds: int
    expected_exit_codes: tuple[int, ...]
    environment: tuple[tuple[str, str], ...]
    repository_files: Mapping[str, str]
    network_access_allowed: bool
    secrets_allowed: bool
    live_repository_access_allowed: bool
    git_operations_allowed: bool

    def digest_payload(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "executable": self.executable,
            "arguments": list(self.arguments),
            "workdir": self.workdir,
            "timeout_seconds": self.timeout_seconds,
            "expected_exit_codes": list(self.expected_exit_codes),
            "environment": dict(self.environment),
            "repository_snapshot_digest": canonical_digest(self.repository_files),
            "network_access_allowed": self.network_access_allowed,
            "secrets_allowed": self.secrets_allowed,
            "live_repository_access_allowed": self.live_repository_access_allowed,
            "git_operations_allowed": self.git_operations_allowed,
        }


RunnerAdapter = Callable[[VerificationExecutionInvocation], Mapping[str, Any]]


@dataclass(frozen=True)
class CodeAIAutonomousVerificationExecutionResult:
    status: str
    issues: tuple[str, ...]
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


def _exact_fields(value: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
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


def _unique_strings(value: Any, *, nonempty: bool = False) -> list[str] | None:
    if not isinstance(value, list):
        return None
    if not all(isinstance(item, str) and item for item in value):
        return None
    if len(value) != len(set(value)) or (nonempty and not value):
        return None
    return list(value)


def _unique_nats(value: Any, *, nonempty: bool = False) -> list[int] | None:
    if not isinstance(value, list):
        return None
    if not all(_nat(item) is not None for item in value):
        return None
    if len(value) != len(set(value)) or (nonempty and not value):
        return None
    return list(value)


def _canonical_repository_path(path: str) -> bool:
    segments = path.split("/")
    return (
        bool(path)
        and not path.startswith("/")
        and not path.endswith("/")
        and "\\" not in path
        and "\0" not in path
        and "\n" not in path
        and "\r" not in path
        and all(segment not in ("", ".", "..") for segment in segments)
    )


def _canonical_text(value: Any) -> bool:
    return (
        isinstance(value, str)
        and "\0" not in value
        and "\r" not in value
        and (not value or value.endswith("\n"))
    )


def _snapshot_size_bytes(repository: Mapping[str, str]) -> int:
    return sum(
        len(path.encode("utf-8")) + len(content.encode("utf-8"))
        for path, content in repository.items()
    )


def _path_has_prefix(path: str, prefix: str) -> bool:
    normalized = prefix.rstrip("/")
    if normalized in ("", "."):
        return True
    return path == normalized or path.startswith(normalized + "/")


def _text_prefix_match(value: str, prefix: str) -> bool:
    return value == prefix or value.startswith(prefix)


def _validate_repository_files(value: Any) -> tuple[Mapping[str, str] | None, list[str]]:
    repository = _mapping(value)
    if repository is None:
        return None, ["resulting_repository_files_not_mapping"]
    issues: list[str] = []
    for path, content in repository.items():
        if not isinstance(path, str) or not _canonical_repository_path(path):
            issues.append("repository_file_path_invalid:" + str(path))
        if not _canonical_text(content):
            issues.append("repository_file_content_invalid:" + str(path))
    return repository, issues


def _validate_candidate_receipt(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    receipt = _mapping(value)
    if receipt is None:
        return None, ["source_candidate_receipt_not_mapping"]
    issues: list[str] = []
    if not _digest_ok(receipt, CANDIDATE_RECEIPT_DIGEST_FIELD):
        issues.append("source_candidate_receipt_digest_mismatch")
    if receipt.get("profile_version") != "CodeAI Candidate Patch v0.1":
        issues.append("source_candidate_profile_unsupported")
    if receipt.get("codeai_disposition") != "candidate_patch_supported":
        issues.append("source_candidate_disposition_invalid")
    if receipt.get("candidate_patch_ready") is not True:
        issues.append("source_candidate_not_ready")
    for field in (
        CANDIDATE_DIGEST_FIELD,
        "patch_artifact_digest",
        "repository_full_name",
        "source_commit_sha",
        CANDIDATE_RECEIPT_DIGEST_FIELD,
    ):
        if not isinstance(receipt.get(field), str) or not receipt.get(field):
            issues.append("source_candidate_invalid_string:" + field)
    for field in (
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
    ):
        if receipt.get(field) is not False:
            issues.append("source_candidate_required_false:" + field)
    return receipt, issues


def _validate_application_receipt(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    receipt = _mapping(value)
    if receipt is None:
        return None, ["source_application_receipt_not_mapping"]
    issues: list[str] = []
    if not _digest_ok(receipt, APPLICATION_RECEIPT_DIGEST_FIELD):
        issues.append("source_application_receipt_digest_mismatch")
    if receipt.get("profile_version") != "CodeAI Autonomous Isolated Candidate Application v0.1":
        issues.append("source_application_profile_unsupported")
    for field in (
        "source_candidate_receipt_digest",
        "selected_candidate_digest",
        "selected_patch_artifact_digest",
        "source_repository_snapshot_digest",
        "resulting_repository_snapshot_digest",
        "repository_full_name",
        "source_commit_sha",
        APPLICATION_RECEIPT_DIGEST_FIELD,
    ):
        if not isinstance(receipt.get(field), str) or not receipt.get(field):
            issues.append("source_application_invalid_string:" + field)
    for field in (
        "isolated_patch_applied",
        "isolated_snapshot_materialized",
        "verification_workspace_ready",
        "source_snapshot_verified",
        "candidate_correspondence_verified",
    ):
        if receipt.get(field) is not True:
            issues.append("source_application_required_true:" + field)
    for field in (
        "input_repository_snapshot_mutated",
        "live_repository_patch_applied",
        "repository_mutation_performed",
        "git_ref_changed",
        "branch_created",
        "commit_created",
        "push_performed",
        "pull_request_created",
        "merge_performed",
        "deployment_performed",
        "secret_access_performed",
        "verification_executed",
        "verification_lease_issued",
        "execution_lease_issued",
    ):
        if receipt.get(field) is not False:
            issues.append("source_application_required_false:" + field)
    return receipt, issues


def _validate_check(value: Any, index: int) -> tuple[Mapping[str, Any] | None, list[str]]:
    check = _mapping(value)
    prefix = f"verification_plan_check[{index}]"
    if check is None:
        return None, [prefix + "_not_mapping"]
    issues = _exact_fields(check, _CHECK_FIELDS, prefix)
    if issues:
        return check, issues
    for field in ("check_id", "executable", "workdir"):
        if not isinstance(check[field], str) or not check[field]:
            issues.append(prefix + "_invalid_string:" + field)
    if _unique_strings(check["arguments"]) is None:
        issues.append(prefix + "_arguments_invalid")
    if _nat(check["timeout_seconds"], positive=True) is None:
        issues.append(prefix + "_timeout_invalid")
    if _unique_nats(check["expected_exit_codes"], nonempty=True) is None:
        issues.append(prefix + "_expected_exit_codes_invalid")
    environment = _mapping(check["environment"])
    if environment is None:
        issues.append(prefix + "_environment_not_mapping")
    elif not all(
        isinstance(key, str)
        and key
        and isinstance(item, str)
        and "\0" not in item
        and "\n" not in key
        and "=" not in key
        for key, item in environment.items()
    ):
        issues.append(prefix + "_environment_invalid")
    if isinstance(check.get("workdir"), str) and not _canonical_repository_path(check["workdir"]):
        if check["workdir"] != ".":
            issues.append(prefix + "_workdir_invalid")
    return check, issues


def _validate_plan(value: Any) -> tuple[Mapping[str, Any] | None, list[Mapping[str, Any]], list[str]]:
    plan = _mapping(value)
    if plan is None:
        return None, [], ["verification_plan_not_mapping"]
    issues = _exact_fields(plan, _PLAN_FIELDS, "verification_plan")
    if issues:
        return plan, [], issues
    for field in ("plan_id", "plan_revision"):
        if not isinstance(plan[field], str) or not plan[field]:
            issues.append("verification_plan_invalid_string:" + field)
    if _nat(plan["plan_created_epoch"]) is None:
        issues.append("verification_plan_created_epoch_invalid")
    if not isinstance(plan["checks"], list) or not plan["checks"]:
        issues.append("verification_plan_checks_invalid")
        checks: list[Mapping[str, Any]] = []
    else:
        checks = []
        for index, raw_check in enumerate(plan["checks"]):
            check, check_issues = _validate_check(raw_check, index)
            issues.extend(check_issues)
            if check is not None:
                checks.append(check)
        ids = [str(check.get("check_id", "")) for check in checks]
        if len(ids) != len(set(ids)):
            issues.append("verification_plan_check_id_duplicate")
    if not _digest_ok(plan, PLAN_DIGEST_FIELD):
        issues.append("verification_plan_digest_mismatch")
    return plan, checks, issues


def _validate_request(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    request = _mapping(value)
    if request is None:
        return None, ["verification_execution_request_not_mapping"]
    issues = _exact_fields(request, _REQUEST_FIELDS, "verification_execution_request")
    if issues:
        return request, issues
    for field in _REQUEST_FIELDS.difference({"request_created_epoch", REQUEST_DIGEST_FIELD}):
        if not isinstance(request[field], str) or not request[field]:
            issues.append("verification_execution_request_invalid_string:" + field)
    if _nat(request["request_created_epoch"]) is None:
        issues.append("verification_execution_request_created_epoch_invalid")
    if not _digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("verification_execution_request_digest_mismatch")
    return request, issues


def _validate_policy(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    policy = _mapping(value)
    if policy is None:
        return None, ["verification_execution_policy_not_mapping"]
    issues = _exact_fields(policy, _POLICY_FIELDS, "verification_execution_policy")
    if issues:
        return policy, issues
    string_fields = {
        field for field in _POLICY_FIELDS
        if field.startswith("expected_")
    }
    for field in string_fields:
        if not isinstance(policy[field], str) or not policy[field]:
            issues.append("verification_execution_policy_invalid_string:" + field)
    for field in (
        "allowed_check_ids",
        "allowed_executable_prefixes",
        "allowed_workdir_prefixes",
        "environment_allowlist",
    ):
        if _unique_strings(policy[field], nonempty=(field != "environment_allowlist")) is None:
            issues.append("verification_execution_policy_invalid_string_list:" + field)
    for field in (
        "maximum_command_count",
        "maximum_timeout_seconds_per_check",
        "maximum_total_timeout_seconds",
        "maximum_stdout_bytes_per_check",
        "maximum_stderr_bytes_per_check",
        "maximum_total_output_bytes",
        "maximum_repository_path_count",
        "maximum_repository_snapshot_bytes",
        "maximum_request_age",
    ):
        if _nat(policy[field], positive=True) is None:
            issues.append("verification_execution_policy_invalid_positive_nat:" + field)
    if _nat(policy["evaluation_epoch"]) is None:
        issues.append("verification_execution_policy_evaluation_epoch_invalid")
    for field in (
        "network_access_allowed",
        "secrets_allowed",
        "live_repository_access_allowed",
        "git_operations_allowed",
    ):
        if not isinstance(policy[field], bool):
            issues.append("verification_execution_policy_invalid_bool:" + field)
        elif policy[field] is not False:
            issues.append("verification_execution_policy_requires_false:" + field)
    if not _digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("verification_execution_policy_digest_mismatch")
    return policy, issues


def _validate_runner_result(value: Any, check_id: str) -> tuple[Mapping[str, Any] | None, list[str]]:
    result = _mapping(value)
    if result is None:
        return None, ["runner_result_not_mapping:" + check_id]
    issues = _exact_fields(result, _RUNNER_RESULT_FIELDS, "runner_result:" + check_id)
    if issues:
        return result, issues
    for field in ("runner_id", "runner_session_id", "check_id", "stdout", "stderr"):
        if not isinstance(result[field], str):
            issues.append("runner_result_invalid_string:" + check_id + ":" + field)
    if result.get("check_id") != check_id:
        issues.append("runner_result_check_id_mismatch:" + check_id)
    exit_code = result.get("exit_code")
    if exit_code is not None and (isinstance(exit_code, bool) or not isinstance(exit_code, int)):
        issues.append("runner_result_exit_code_invalid:" + check_id)
    if _nat(result.get("duration_ms")) is None:
        issues.append("runner_result_duration_invalid:" + check_id)
    for field in (
        "timed_out",
        "network_used",
        "secret_accessed",
        "live_repository_accessed",
        "git_effect_performed",
    ):
        if not isinstance(result.get(field), bool):
            issues.append("runner_result_invalid_bool:" + check_id + ":" + field)
    exception_type = result.get("exception_type")
    if exception_type is not None and (not isinstance(exception_type, str) or not exception_type):
        issues.append("runner_result_exception_type_invalid:" + check_id)
    for field in ("started_epoch", "completed_epoch"):
        if _nat(result.get(field)) is None:
            issues.append("runner_result_epoch_invalid:" + check_id + ":" + field)
    if (
        _nat(result.get("started_epoch")) is not None
        and _nat(result.get("completed_epoch")) is not None
        and result["started_epoch"] > result["completed_epoch"]
    ):
        issues.append("runner_result_window_invalid:" + check_id)
    return result, issues


def _bounded_excerpt(text: str, maximum_bytes: int) -> tuple[str, int, bool]:
    encoded = text.encode("utf-8")
    if len(encoded) <= maximum_bytes:
        return text, len(encoded), False
    bounded = encoded[:maximum_bytes]
    while True:
        try:
            excerpt = bounded.decode("utf-8")
            break
        except UnicodeDecodeError:
            bounded = bounded[:-1]
    return excerpt, len(encoded), True


def _preflight(
    *,
    source_candidate_receipt: Any,
    source_application_receipt: Any,
    resulting_repository_files: Any,
    verification_plan: Any,
    execution_request: Any,
    execution_policy: Any,
) -> tuple[
    Mapping[str, Any] | None,
    Mapping[str, Any] | None,
    Mapping[str, str] | None,
    Mapping[str, Any] | None,
    list[Mapping[str, Any]],
    Mapping[str, Any] | None,
    Mapping[str, Any] | None,
    list[str],
]:
    candidate, candidate_issues = _validate_candidate_receipt(source_candidate_receipt)
    application, application_issues = _validate_application_receipt(source_application_receipt)
    repository, repository_issues = _validate_repository_files(resulting_repository_files)
    plan, checks, plan_issues = _validate_plan(verification_plan)
    request, request_issues = _validate_request(execution_request)
    policy, policy_issues = _validate_policy(execution_policy)
    issues = (
        candidate_issues
        + application_issues
        + repository_issues
        + plan_issues
        + request_issues
        + policy_issues
    )
    return candidate, application, repository, plan, checks, request, policy, issues


def _correspondence_issues(
    *,
    candidate: Mapping[str, Any],
    application: Mapping[str, Any],
    repository: Mapping[str, str],
    plan: Mapping[str, Any],
    checks: Sequence[Mapping[str, Any]],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> list[str]:
    issues: list[str] = []
    candidate_receipt_digest = str(candidate[CANDIDATE_RECEIPT_DIGEST_FIELD])
    application_receipt_digest = str(application[APPLICATION_RECEIPT_DIGEST_FIELD])
    candidate_digest = str(candidate[CANDIDATE_DIGEST_FIELD])
    artifact_digest = str(candidate["patch_artifact_digest"])
    resulting_snapshot_digest = canonical_digest(repository)
    plan_digest = str(plan[PLAN_DIGEST_FIELD])
    pairs = (
        (application["source_candidate_receipt_digest"], candidate_receipt_digest, "application_candidate_receipt"),
        (application["selected_candidate_digest"], candidate_digest, "application_candidate"),
        (application["selected_patch_artifact_digest"], artifact_digest, "application_artifact"),
        (application["resulting_repository_snapshot_digest"], resulting_snapshot_digest, "application_result_snapshot"),
        (application["repository_full_name"], candidate["repository_full_name"], "application_repository"),
        (application["source_commit_sha"], candidate["source_commit_sha"], "application_source_commit"),
        (request["source_candidate_receipt_digest"], candidate_receipt_digest, "request_candidate_receipt"),
        (request["source_application_receipt_digest"], application_receipt_digest, "request_application_receipt"),
        (request["candidate_digest"], candidate_digest, "request_candidate"),
        (request["patch_artifact_digest"], artifact_digest, "request_artifact"),
        (request["source_repository_snapshot_digest"], application["source_repository_snapshot_digest"], "request_source_snapshot"),
        (request["resulting_repository_snapshot_digest"], resulting_snapshot_digest, "request_result_snapshot"),
        (request["repository_full_name"], candidate["repository_full_name"], "request_repository"),
        (request["source_commit_sha"], candidate["source_commit_sha"], "request_source_commit"),
        (request["verification_plan_digest"], plan_digest, "request_plan"),
        (policy["expected_source_candidate_receipt_digest"], candidate_receipt_digest, "policy_candidate_receipt"),
        (policy["expected_source_application_receipt_digest"], application_receipt_digest, "policy_application_receipt"),
        (policy["expected_candidate_digest"], candidate_digest, "policy_candidate"),
        (policy["expected_patch_artifact_digest"], artifact_digest, "policy_artifact"),
        (policy["expected_source_repository_snapshot_digest"], application["source_repository_snapshot_digest"], "policy_source_snapshot"),
        (policy["expected_resulting_repository_snapshot_digest"], resulting_snapshot_digest, "policy_result_snapshot"),
        (policy["expected_repository_full_name"], candidate["repository_full_name"], "policy_repository"),
        (policy["expected_source_commit_sha"], candidate["source_commit_sha"], "policy_source_commit"),
        (policy["expected_verification_plan_digest"], plan_digest, "policy_plan"),
    )
    for actual, expected, label in pairs:
        if actual != expected:
            issues.append("verification_execution_correspondence_mismatch:" + label)

    evaluation_epoch = int(policy["evaluation_epoch"])
    created_epoch = int(request["request_created_epoch"])
    if not evaluation_epoch - int(policy["maximum_request_age"]) <= created_epoch <= evaluation_epoch:
        issues.append("verification_execution_request_window_invalid")
    if int(plan["plan_created_epoch"]) > created_epoch:
        issues.append("verification_plan_created_after_request")
    if len(repository) > int(policy["maximum_repository_path_count"]):
        issues.append("verification_repository_path_budget_exceeded")
    if _snapshot_size_bytes(repository) > int(policy["maximum_repository_snapshot_bytes"]):
        issues.append("verification_repository_snapshot_budget_exceeded")
    if len(checks) > int(policy["maximum_command_count"]):
        issues.append("verification_command_count_budget_exceeded")
    if sum(int(check["timeout_seconds"]) for check in checks) > int(policy["maximum_total_timeout_seconds"]):
        issues.append("verification_total_timeout_budget_exceeded")

    allowed_ids = set(policy["allowed_check_ids"])
    allowed_environment = set(policy["environment_allowlist"])
    for check in checks:
        check_id = str(check["check_id"])
        if check_id not in allowed_ids:
            issues.append("verification_check_not_allowed:" + check_id)
        if not any(_text_prefix_match(str(check["executable"]), prefix) for prefix in policy["allowed_executable_prefixes"]):
            issues.append("verification_executable_not_allowed:" + check_id)
        if not any(_path_has_prefix(str(check["workdir"]), prefix) for prefix in policy["allowed_workdir_prefixes"]):
            issues.append("verification_workdir_not_allowed:" + check_id)
        if int(check["timeout_seconds"]) > int(policy["maximum_timeout_seconds_per_check"]):
            issues.append("verification_check_timeout_budget_exceeded:" + check_id)
        environment = _mapping(check["environment"])
        if environment is not None and not set(environment).issubset(allowed_environment):
            issues.append("verification_environment_not_allowed:" + check_id)
    return issues


def _record_from_exception(
    check: Mapping[str, Any],
    invocation_digest: str,
    exception: Exception,
    evaluation_epoch: int,
) -> dict[str, Any]:
    value = {
        "check_id": check["check_id"],
        "invocation_digest": invocation_digest,
        "runner_id": "runner_adapter_exception",
        "runner_session_id": "runner_adapter_exception",
        "execution_status": "runner_exception",
        "exit_code": None,
        "expected_exit_codes": list(check["expected_exit_codes"]),
        "stdout_digest": canonical_digest(""),
        "stderr_digest": canonical_digest(str(exception)),
        "stdout_excerpt": "",
        "stderr_excerpt": str(exception),
        "stdout_size_bytes": 0,
        "stderr_size_bytes": len(str(exception).encode("utf-8")),
        "stdout_truncated": False,
        "stderr_truncated": False,
        "duration_ms": 0,
        "timed_out": False,
        "exception_type": type(exception).__name__,
        "started_epoch": evaluation_epoch,
        "completed_epoch": evaluation_epoch,
        "network_used": False,
        "secret_accessed": False,
        "live_repository_accessed": False,
        "git_effect_performed": False,
        "runner_result_rejection_reasons": [],
    }
    value["record_digest"] = canonical_digest(value)
    return value


def _record_from_runner_result(
    *,
    check: Mapping[str, Any],
    invocation_digest: str,
    result: Mapping[str, Any],
    result_issues: Sequence[str],
    policy: Mapping[str, Any],
    remaining_output_budget: int,
) -> tuple[dict[str, Any], int, bool]:
    stdout = result.get("stdout") if isinstance(result.get("stdout"), str) else ""
    stderr = result.get("stderr") if isinstance(result.get("stderr"), str) else ""
    stdout_excerpt, stdout_size, stdout_truncated = _bounded_excerpt(
        stdout, int(policy["maximum_stdout_bytes_per_check"])
    )
    stderr_excerpt, stderr_size, stderr_truncated = _bounded_excerpt(
        stderr, int(policy["maximum_stderr_bytes_per_check"])
    )
    observed_size = stdout_size + stderr_size
    total_budget_exceeded = observed_size > remaining_output_budget
    side_effect = any(
        result.get(field) is True
        for field in (
            "network_used",
            "secret_accessed",
            "live_repository_accessed",
            "git_effect_performed",
        )
    )
    per_check_output_exceeded = stdout_truncated or stderr_truncated
    timed_out = result.get("timed_out") is True
    exception_type = result.get("exception_type")
    exit_code = result.get("exit_code")
    expected_exit_codes = set(check["expected_exit_codes"])
    if result_issues:
        execution_status = "runner_result_rejected"
    elif side_effect:
        execution_status = "runner_effect_rejected"
    elif total_budget_exceeded:
        execution_status = "total_output_budget_exceeded"
    elif per_check_output_exceeded:
        execution_status = "per_check_output_budget_exceeded"
    elif timed_out:
        execution_status = "timed_out"
    elif exception_type is not None:
        execution_status = "runner_exception"
    elif exit_code in expected_exit_codes:
        execution_status = "passed"
    else:
        execution_status = "failed"
    value = {
        "check_id": check["check_id"],
        "invocation_digest": invocation_digest,
        "runner_id": result.get("runner_id", ""),
        "runner_session_id": result.get("runner_session_id", ""),
        "execution_status": execution_status,
        "exit_code": exit_code,
        "expected_exit_codes": list(check["expected_exit_codes"]),
        "stdout_digest": canonical_digest(stdout),
        "stderr_digest": canonical_digest(stderr),
        "stdout_excerpt": stdout_excerpt,
        "stderr_excerpt": stderr_excerpt,
        "stdout_size_bytes": stdout_size,
        "stderr_size_bytes": stderr_size,
        "stdout_truncated": stdout_truncated,
        "stderr_truncated": stderr_truncated,
        "duration_ms": result.get("duration_ms", 0),
        "timed_out": timed_out,
        "exception_type": exception_type,
        "started_epoch": result.get("started_epoch", 0),
        "completed_epoch": result.get("completed_epoch", 0),
        "network_used": result.get("network_used", False),
        "secret_accessed": result.get("secret_accessed", False),
        "live_repository_accessed": result.get("live_repository_accessed", False),
        "git_effect_performed": result.get("git_effect_performed", False),
        "runner_result_rejection_reasons": list(result_issues),
    }
    value["record_digest"] = canonical_digest(value)
    return value, observed_size, total_budget_exceeded


def _evidence_bundle(
    records: Sequence[Mapping[str, Any]],
    plan: Mapping[str, Any],
    aborted_by_budget: bool,
) -> dict[str, Any]:
    passed = [record["check_id"] for record in records if record["execution_status"] == "passed"]
    failed = [
        record["check_id"]
        for record in records
        if record["execution_status"] != "passed"
    ]
    timed_out = [record["check_id"] for record in records if record["timed_out"]]
    exceptions = [
        record["check_id"]
        for record in records
        if record["execution_status"] == "runner_exception"
    ]
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "verification_plan_digest": plan[PLAN_DIGEST_FIELD],
        "check_ids": [record["check_id"] for record in records],
        "passed_check_ids": passed,
        "failed_check_ids": failed,
        "timed_out_check_ids": timed_out,
        "runner_exception_check_ids": exceptions,
        "declared_check_count": len(records),
        "passed_check_count": len(passed),
        "failed_check_count": len(failed),
        "execution_aborted_by_runtime_budget": aborted_by_budget,
        "records": [dict(record) for record in records],
    }
    return seal(value, EVIDENCE_BUNDLE_DIGEST_FIELD)


def _independent_verification_evidence(
    *,
    candidate: Mapping[str, Any],
    request: Mapping[str, Any],
    evidence_bundle: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    records = evidence_bundle["records"]
    passed = list(evidence_bundle["passed_check_ids"])
    failed = list(evidence_bundle["failed_check_ids"])
    all_passed = bool(records) and not failed
    started = min((int(record["started_epoch"]) for record in records), default=int(request["request_created_epoch"]))
    completed = max((int(record["completed_epoch"]) for record in records), default=int(policy["evaluation_epoch"]))
    outcome = "passed" if all_passed else "failed"
    finding_labels = [] if all_passed else ["verification_execution_failure"]
    outcome_reasons = ["all_declared_checks_passed"] if all_passed else ["one_or_more_declared_checks_failed"]
    value = {
        "verification_id": request["verification_id"],
        "verifier_id": request["verifier_id"],
        "reviewer_id": request["reviewer_id"],
        "source_candidate_receipt_digest": candidate[CANDIDATE_RECEIPT_DIGEST_FIELD],
        "candidate_patch_digest": candidate[CANDIDATE_DIGEST_FIELD],
        "patch_artifact_digest": candidate["patch_artifact_digest"],
        "repository_full_name": candidate["repository_full_name"],
        "source_commit_sha": candidate["source_commit_sha"],
        "evidence_format": request["evidence_format"],
        "toolchain_digest": request["toolchain_digest"],
        "environment_digest": request["environment_digest"],
        "verification_protocol_digest": request["verification_protocol_digest"],
        "check_ids": list(evidence_bundle["check_ids"]),
        "passed_check_ids": passed,
        "failed_check_ids": failed,
        "skipped_check_ids": [],
        "declared_check_count": int(evidence_bundle["declared_check_count"]),
        "evidence_artifact_digests": [
            evidence_bundle[EVIDENCE_BUNDLE_DIGEST_FIELD],
            *[record["record_digest"] for record in records],
        ],
        "finding_labels": finding_labels,
        "outcome_reason_ids": outcome_reasons,
        "planned_reproduction_attempts": 1,
        "completed_reproduction_attempts": 1,
        "successful_reproduction_attempts": 1 if all_passed else 0,
        "falsification_challenge_executed": False,
        "falsification_challenge_passed": False,
        "acceptance_criteria_satisfied": all_passed,
        "evidence_conclusive": True,
        "declared_verification_outcome": outcome,
        "verification_started_epoch": started,
        "verification_completed_epoch": completed,
        "verification_session_id": request["verification_session_id"],
        "verification_nonce_digest": request["verification_nonce_digest"],
        "prior_verification_session_ids": [],
        "prior_verification_nonce_digests": [],
        "prior_evidence_digests": [],
        "prior_verification_receipt_digests": [],
        "evidence_integrity_confirmed": True,
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
        "isolated_verification_executed": True,
        "verification_execution_performed_by_kernel": False,
        "live_repository_mutated_by_verifier": False,
        "repository_files_changed_by_kernel": False,
        "git_ref_changed_by_kernel": False,
        "branch_created_by_kernel": False,
        "commit_created_by_kernel": False,
        "push_performed_by_kernel": False,
        "pull_request_created_by_kernel": False,
        "external_side_effect_performed_by_kernel": False,
        "selection_authority_claimed": False,
        "verification_authority_claimed": False,
        "execution_authority_claimed": False,
        "merge_authority_claimed": False,
        "deployment_authority_claimed": False,
        "secret_access_authority_claimed": False,
        "generalized_truth_claimed": False,
        "correctness_proof_claimed": False,
    }
    return seal(value, INDEPENDENT_EVIDENCE_DIGEST_FIELD)


def _receipt(
    *,
    candidate: Mapping[str, Any],
    application: Mapping[str, Any],
    repository: Mapping[str, str],
    plan: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    evidence_bundle: Mapping[str, Any],
    independent_evidence: Mapping[str, Any],
    disposition: str,
) -> dict[str, Any]:
    failed_count = int(evidence_bundle["failed_check_count"])
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_candidate_receipt_digest": candidate[CANDIDATE_RECEIPT_DIGEST_FIELD],
        "source_application_receipt_digest": application[APPLICATION_RECEIPT_DIGEST_FIELD],
        "candidate_digest": candidate[CANDIDATE_DIGEST_FIELD],
        "patch_artifact_digest": candidate["patch_artifact_digest"],
        "source_repository_snapshot_digest": application["source_repository_snapshot_digest"],
        "resulting_repository_snapshot_digest": canonical_digest(repository),
        "repository_full_name": candidate["repository_full_name"],
        "source_commit_sha": candidate["source_commit_sha"],
        "verification_plan_digest": plan[PLAN_DIGEST_FIELD],
        "execution_request_digest": request[REQUEST_DIGEST_FIELD],
        "execution_policy_digest": policy[POLICY_DIGEST_FIELD],
        "evidence_bundle_digest": evidence_bundle[EVIDENCE_BUNDLE_DIGEST_FIELD],
        "independent_verification_evidence_digest": independent_evidence[INDEPENDENT_EVIDENCE_DIGEST_FIELD],
        "declared_check_count": int(evidence_bundle["declared_check_count"]),
        "passed_check_count": int(evidence_bundle["passed_check_count"]),
        "failed_check_count": failed_count,
        "timed_out_check_count": len(evidence_bundle["timed_out_check_ids"]),
        "runner_exception_check_count": len(evidence_bundle["runner_exception_check_ids"]),
        "codeai_disposition": disposition,
        "operating_mode": MODE_BOUNDED_ISOLATED_EXECUTION,
        "route_receipt_recorded": True,
        "source_correspondence_verified": True,
        "application_correspondence_verified": True,
        "resulting_snapshot_verified": True,
        "verification_plan_verified": True,
        "execution_policy_evaluated": True,
        "bounded_runner_invocation_performed": True,
        "verification_execution_completed": disposition != DISPOSITION_ABORTED_BY_BUDGET,
        "verification_execution_failed_checks_present": failed_count > 0,
        "independent_verification_evidence_projected": True,
        "input_repository_snapshot_mutated": False,
        "live_repository_access_performed": False,
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
        "execution_treated_as_correctness": False,
        "tests_passing_treated_as_proof": False,
        "verification_evidence_treated_as_merge_authority": False,
        "runner_exception_treated_as_success": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    return seal(value, RECEIPT_DIGEST_FIELD)


def build_codeai_autonomous_verification_execution(
    *,
    source_candidate_receipt: Any,
    source_application_receipt: Any,
    resulting_repository_files: Any,
    verification_plan: Any,
    execution_request: Any,
    execution_policy: Any,
    runner_adapter: RunnerAdapter,
) -> CodeAIAutonomousVerificationExecutionResult:
    (
        candidate,
        application,
        repository,
        plan,
        checks,
        request,
        policy,
        issues,
    ) = _preflight(
        source_candidate_receipt=source_candidate_receipt,
        source_application_receipt=source_application_receipt,
        resulting_repository_files=resulting_repository_files,
        verification_plan=verification_plan,
        execution_request=execution_request,
        execution_policy=execution_policy,
    )
    if (
        issues
        or candidate is None
        or application is None
        or repository is None
        or plan is None
        or request is None
        or policy is None
    ):
        return CodeAIAutonomousVerificationExecutionResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None, None
        )

    issues = _correspondence_issues(
        candidate=candidate,
        application=application,
        repository=repository,
        plan=plan,
        checks=checks,
        request=request,
        policy=policy,
    )
    if issues:
        return CodeAIAutonomousVerificationExecutionResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None, None
        )
    if not callable(runner_adapter):
        return CodeAIAutonomousVerificationExecutionResult(
            STATUS_BLOCKED, ("runner_adapter_not_callable",), None, None, None
        )

    repository_digest_before = canonical_digest(repository)
    records: list[dict[str, Any]] = []
    observed_output_bytes = 0
    aborted_by_budget = False
    for check in checks:
        if observed_output_bytes >= int(policy["maximum_total_output_bytes"]):
            aborted_by_budget = True
            break
        invocation = VerificationExecutionInvocation(
            check_id=str(check["check_id"]),
            executable=str(check["executable"]),
            arguments=tuple(check["arguments"]),
            workdir=str(check["workdir"]),
            timeout_seconds=int(check["timeout_seconds"]),
            expected_exit_codes=tuple(check["expected_exit_codes"]),
            environment=tuple(sorted(_mapping(check["environment"]).items())),
            repository_files=deepcopy(dict(repository)),
            network_access_allowed=False,
            secrets_allowed=False,
            live_repository_access_allowed=False,
            git_operations_allowed=False,
        )
        invocation_digest = canonical_digest(invocation.digest_payload())
        try:
            raw_result = runner_adapter(invocation)
        except Exception as exception:
            records.append(
                _record_from_exception(
                    check,
                    invocation_digest,
                    exception,
                    int(policy["evaluation_epoch"]),
                )
            )
            continue
        parsed_result, result_issues = _validate_runner_result(raw_result, invocation.check_id)
        if parsed_result is None:
            parsed_result = {
                "runner_id": "runner_result_rejected",
                "runner_session_id": "runner_result_rejected",
                "check_id": invocation.check_id,
                "exit_code": None,
                "stdout": "",
                "stderr": "",
                "duration_ms": 0,
                "timed_out": False,
                "exception_type": "InvalidRunnerResult",
                "started_epoch": int(policy["evaluation_epoch"]),
                "completed_epoch": int(policy["evaluation_epoch"]),
                "network_used": False,
                "secret_accessed": False,
                "live_repository_accessed": False,
                "git_effect_performed": False,
            }
        record, output_size, total_exceeded = _record_from_runner_result(
            check=check,
            invocation_digest=invocation_digest,
            result=parsed_result,
            result_issues=result_issues,
            policy=policy,
            remaining_output_budget=int(policy["maximum_total_output_bytes"]) - observed_output_bytes,
        )
        observed_output_bytes += output_size
        records.append(record)
        if total_exceeded:
            aborted_by_budget = True
            break

    if canonical_digest(repository) != repository_digest_before:
        return CodeAIAutonomousVerificationExecutionResult(
            STATUS_BLOCKED,
            ("input_repository_snapshot_mutated_during_execution",),
            None,
            None,
            None,
        )

    bundle = _evidence_bundle(records, plan, aborted_by_budget)
    independent_evidence = _independent_verification_evidence(
        candidate=candidate,
        request=request,
        evidence_bundle=bundle,
        policy=policy,
    )
    if aborted_by_budget:
        disposition = DISPOSITION_ABORTED_BY_BUDGET
    elif bundle["failed_check_count"]:
        disposition = DISPOSITION_COMPLETED_WITH_FAILURES
    else:
        disposition = DISPOSITION_COMPLETED
    receipt = _receipt(
        candidate=candidate,
        application=application,
        repository=repository,
        plan=plan,
        request=request,
        policy=policy,
        evidence_bundle=bundle,
        independent_evidence=independent_evidence,
        disposition=disposition,
    )
    return CodeAIAutonomousVerificationExecutionResult(
        STATUS_READY, (), bundle, independent_evidence, receipt
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "VerificationExecutionInvocation",
    "CodeAIAutonomousVerificationExecutionResult",
    "build_codeai_autonomous_verification_execution",
]
