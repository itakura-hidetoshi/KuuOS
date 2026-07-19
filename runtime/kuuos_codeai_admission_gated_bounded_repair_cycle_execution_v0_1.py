#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import canonical_digest, seal
from runtime.kuuos_codeai_repair_cycle_admission_consumption_v0_1 import (
    DISPOSITION_CONSUMED as ADMISSION_CONSUMPTION_DISPOSITION,
    EXECUTION_INPUT_DIGEST_FIELD,
    EXECUTION_INPUT_DISPOSITION,
    EXECUTION_INPUT_PROFILE_VERSION,
    MODE_ADMISSION_CONSUMPTION,
    MODE_BOUNDED_CYCLE_EXECUTION_INPUT,
    PROFILE_VERSION as ADMISSION_CONSUMPTION_PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD as ADMISSION_CONSUMPTION_RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as ADMISSION_CONSUMPTION_REGISTRY_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_verification_execution_v0_1 import (
    EVIDENCE_BUNDLE_DIGEST_FIELD,
    INDEPENDENT_EVIDENCE_DIGEST_FIELD,
    PLAN_DIGEST_FIELD,
)
from runtime.kuuos_codeai_bounded_repair_cycle_orchestration_v0_1 import (
    DISPOSITION_ABORTED as INNER_DISPOSITION_ABORTED,
    DISPOSITION_FAILED as INNER_DISPOSITION_FAILED,
    DISPOSITION_PASSED as INNER_DISPOSITION_PASSED,
    POLICY_DIGEST_FIELD as INNER_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as INNER_RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as INNER_REQUEST_DIGEST_FIELD,
    STATUS_READY as INNER_STATUS_READY,
    build_codeai_bounded_repair_cycle_orchestration,
    repair_candidate_set_digest,
)
from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    CANDIDATE_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_candidate_regeneration_common_v0_1 import (
    RECEIPT_DIGEST_FIELD as REGENERATION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_verification_guided_candidate_repair_regeneration_v0_1 import (
    RECEIPT_DIGEST_FIELD as REPAIR_RECEIPT_DIGEST_FIELD,
)

VERSION = "kuuos_codeai_admission_gated_bounded_repair_cycle_execution_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Admission-Gated Bounded Repair Cycle Execution v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_ADMISSION_GATED_EXECUTION = "admission_gated_bounded_repair_cycle_execution"
DISPOSITION_PASSED = "admitted_repair_cycle_verification_passed"
DISPOSITION_FAILED = "admitted_repair_cycle_verification_failed"
DISPOSITION_ABORTED = "admitted_repair_cycle_aborted_by_budget"
REQUEST_DIGEST_FIELD = "codeai_admission_gated_bounded_repair_cycle_execution_request_digest"
POLICY_DIGEST_FIELD = "codeai_admission_gated_bounded_repair_cycle_execution_policy_digest"
REGISTRY_DIGEST_FIELD = "codeai_admission_gated_bounded_repair_cycle_execution_registry_digest"
RECEIPT_DIGEST_FIELD = "codeai_admission_gated_bounded_repair_cycle_execution_receipt_digest"

_ALLOWED_STAGE_IDS = (
    "candidate_regeneration_adapter",
    "candidate_portfolio_selection",
    "isolated_candidate_application",
    "autonomous_verification_execution",
)

_REQUEST_FIELDS = {
    "execution_request_id",
    "execution_request_revision",
    "execution_input_digest",
    "admission_consumption_receipt_digest",
    "consumption_registry_digest",
    "cycle_index",
    "execution_session_id",
    "cycle_execution_nonce_digest",
    "executor_actor_id",
    "verification_id",
    "verifier_id",
    "reviewer_id",
    "evidence_format",
    "toolchain_digest",
    "environment_digest",
    "verification_protocol_digest",
    "request_created_epoch",
    REQUEST_DIGEST_FIELD,
}

_POLICY_FIELDS = {
    "expected_execution_input_digest",
    "expected_admission_consumption_receipt_digest",
    "expected_consumption_registry_digest",
    "expected_cycle_index",
    "expected_repository_full_name",
    "expected_source_commit_sha",
    "expected_executor_actor_id",
    "allowed_stage_ids",
    "maximum_executed_input_count",
    "maximum_candidate_count",
    "maximum_provider_call_count",
    "maximum_command_count",
    "maximum_total_timeout_seconds",
    "maximum_total_output_bytes",
    "network_access_allowed",
    "secrets_allowed",
    "live_repository_access_allowed",
    "git_operations_allowed",
    "merge_allowed",
    "deployment_allowed",
    "evaluation_epoch",
    "maximum_request_age",
    POLICY_DIGEST_FIELD,
}

_REGISTRY_FIELDS = {
    "registry_id",
    "registry_revision",
    "consumed_execution_input_digests",
    "consumed_cycle_execution_nonce_digests",
    "last_executed_cycle_index",
    "registry_created_epoch",
    REGISTRY_DIGEST_FIELD,
}

_PROVIDER_RESULT_FIELDS = {
    "provider_id",
    "provider_session_id",
    "provider_output_bytes",
    "generated_candidate_count",
    "source_repair_receipt",
    "source_regeneration_receipt",
    "repair_candidates",
    "network_used",
    "secret_accessed",
    "live_repository_accessed",
    "git_effect_performed",
}


@dataclass(frozen=True)
class AdmissionGatedCycleProviderInvocation:
    execution_input_digest: str
    cycle_index: int
    source_repair_receipt_digest: str
    source_regeneration_receipt_digest: str
    repair_candidate_set_digest: str
    verification_plan_digest: str
    repository_snapshot_digest: str
    maximum_candidate_count: int
    maximum_provider_call_count: int
    maximum_output_bytes: int
    network_access_allowed: bool
    secrets_allowed: bool
    live_repository_access_allowed: bool
    git_operations_allowed: bool


ProviderAdapter = Callable[[AdmissionGatedCycleProviderInvocation], Mapping[str, Any]]


@dataclass(frozen=True)
class CodeAIAdmissionGatedBoundedRepairCycleExecutionResult:
    status: str
    issues: tuple[str, ...]
    selected_candidate: Any | None
    resulting_repository_files: dict[str, str] | None
    evidence_bundle: dict[str, Any] | None
    independent_verification_evidence: dict[str, Any] | None
    next_registry: dict[str, Any] | None
    receipt: dict[str, Any] | None


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _nat(value: Any, *, positive: bool = False) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    if positive and value == 0:
        return None
    return value


def _unique_strings(value: Any, *, nonempty: bool = False) -> list[str] | None:
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


def _validate_admission_consumption_receipt(
    value: Any,
) -> tuple[Mapping[str, Any] | None, list[str]]:
    receipt = _mapping(value)
    if receipt is None:
        return None, ["admission_consumption_receipt_not_mapping"]
    issues: list[str] = []
    if not _digest_ok(receipt, ADMISSION_CONSUMPTION_RECEIPT_DIGEST_FIELD):
        issues.append("admission_consumption_receipt_digest_mismatch")
    if receipt.get("profile_version") != ADMISSION_CONSUMPTION_PROFILE_VERSION:
        issues.append("admission_consumption_profile_unsupported")
    if receipt.get("operating_mode") != MODE_ADMISSION_CONSUMPTION:
        issues.append("admission_consumption_mode_invalid")
    if receipt.get("codeai_disposition") != ADMISSION_CONSUMPTION_DISPOSITION:
        issues.append("admission_consumption_disposition_invalid")
    for field in (
        "route_receipt_recorded",
        "source_admission_verified",
        "source_admission_consumed",
        "admission_replay_excluded",
        "execution_nonce_replay_excluded",
        "registry_transition_verified",
        "exactly_one_execution_input_issued",
        "bounded_budget_mapping_verified",
        "bounded_cycle_execution_authority_granted",
    ):
        if receipt.get(field) is not True:
            issues.append("admission_consumption_required_true:" + field)
    for field in (
        "automatic_execution_authority_granted",
        "general_successor_stage_authority_granted",
        "cycle_execution_performed",
        "provider_invoked",
        "runner_invoked",
        "candidate_generated",
        "candidate_selected",
        "patch_applied",
        "verification_executed",
        "repository_mutation_performed",
        "git_ref_changed",
        "branch_created",
        "commit_created",
        "push_performed",
        "pull_request_created",
        "network_access_performed",
        "secret_access_performed",
        "merge_performed",
        "deployment_performed",
    ):
        if receipt.get(field) is not False:
            issues.append("admission_consumption_required_false:" + field)
    for field in (
        "source_admission_receipt_digest",
        "source_cycle_receipt_digest",
        "source_selected_candidate_digest",
        "next_consumption_registry_digest",
        "execution_input_digest",
        ADMISSION_CONSUMPTION_RECEIPT_DIGEST_FIELD,
    ):
        if not isinstance(receipt.get(field), str) or not receipt.get(field):
            issues.append("admission_consumption_invalid_string:" + field)
    for field in (
        "admitted_cycle_index",
        "source_registry_revision",
        "next_registry_revision",
        "source_consumed_admission_count",
        "next_consumed_admission_count",
    ):
        if _nat(receipt.get(field), positive=field in {"admitted_cycle_index", "next_registry_revision"}) is None:
            issues.append("admission_consumption_invalid_nat:" + field)
    if (
        _nat(receipt.get("source_registry_revision")) is not None
        and _nat(receipt.get("next_registry_revision")) is not None
        and int(receipt["next_registry_revision"]) != int(receipt["source_registry_revision"]) + 1
    ):
        issues.append("admission_consumption_registry_revision_step_invalid")
    if (
        _nat(receipt.get("source_consumed_admission_count")) is not None
        and _nat(receipt.get("next_consumed_admission_count")) is not None
        and int(receipt["next_consumed_admission_count"])
        != int(receipt["source_consumed_admission_count"]) + 1
    ):
        issues.append("admission_consumption_count_step_invalid")
    return receipt, issues


def _validate_execution_input(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    execution_input = _mapping(value)
    if execution_input is None:
        return None, ["execution_input_not_mapping"]
    issues: list[str] = []
    if not _digest_ok(execution_input, EXECUTION_INPUT_DIGEST_FIELD):
        issues.append("execution_input_digest_mismatch")
    if execution_input.get("profile_version") != EXECUTION_INPUT_PROFILE_VERSION:
        issues.append("execution_input_profile_unsupported")
    if execution_input.get("operating_mode") != MODE_BOUNDED_CYCLE_EXECUTION_INPUT:
        issues.append("execution_input_mode_invalid")
    if execution_input.get("codeai_disposition") != EXECUTION_INPUT_DISPOSITION:
        issues.append("execution_input_disposition_invalid")
    for field in (
        "source_admission_consumed",
        "one_cycle_only",
        "one_shot",
        "execution_input_active",
        "bounded_cycle_execution_authority_granted",
        "candidate_generation_authority_granted",
        "candidate_selection_authority_granted",
        "isolated_patch_application_authority_granted",
        "verification_execution_authority_granted",
    ):
        if execution_input.get(field) is not True:
            issues.append("execution_input_required_true:" + field)
    for field in (
        "execution_input_reusable",
        "execution_input_consumed",
        "automatic_execution_authority_granted",
        "network_access_authority_granted",
        "secret_access_authority_granted",
        "live_repository_access_authority_granted",
        "git_operations_authority_granted",
        "merge_authority_granted",
        "deployment_authority_granted",
        "general_successor_stage_authority_granted",
        "cycle_execution_performed",
        "provider_invoked",
        "runner_invoked",
        "candidate_generated",
        "candidate_selected",
        "patch_applied",
        "verification_executed",
        "repository_mutation_performed",
        "git_ref_changed",
        "network_access_performed",
        "secret_access_performed",
        "merge_performed",
        "deployment_performed",
        "automatic_execution_allowed",
    ):
        if execution_input.get(field) is not False:
            issues.append("execution_input_required_false:" + field)
    for field in (
        "source_admission_receipt_digest",
        "source_cycle_receipt_digest",
        "source_selected_candidate_digest",
        "source_repair_receipt_digest",
        "source_regeneration_receipt_digest",
        "repair_candidate_set_digest",
        "verification_plan_digest",
        "execution_session_id",
        "execution_nonce_digest",
        "consumer_actor_id",
        EXECUTION_INPUT_DIGEST_FIELD,
    ):
        if not isinstance(execution_input.get(field), str) or not execution_input.get(field):
            issues.append("execution_input_invalid_string:" + field)
    for field in (
        "cycle_index",
        "maximum_candidate_count",
        "maximum_provider_call_count",
        "maximum_command_count",
        "maximum_total_timeout_seconds",
        "maximum_total_output_bytes",
    ):
        if _nat(execution_input.get(field), positive=True) is None:
            issues.append("execution_input_invalid_positive_nat:" + field)
    return execution_input, issues


def _validate_consumption_registry(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    registry = _mapping(value)
    if registry is None:
        return None, ["consumption_registry_receipt_not_mapping"]
    issues: list[str] = []
    required = {
        "registry_id",
        "registry_revision",
        "consumed_admission_receipt_digests",
        "consumed_execution_nonce_digests",
        "last_consumed_cycle_index",
        "registry_created_epoch",
        ADMISSION_CONSUMPTION_REGISTRY_DIGEST_FIELD,
    }
    issues += _exact(registry, required, "consumption_registry_receipt")
    if issues:
        return registry, issues
    if not _digest_ok(registry, ADMISSION_CONSUMPTION_REGISTRY_DIGEST_FIELD):
        issues.append("consumption_registry_receipt_digest_mismatch")
    if not isinstance(registry["registry_id"], str) or not registry["registry_id"]:
        issues.append("consumption_registry_receipt_id_invalid")
    for field in ("registry_revision", "last_consumed_cycle_index", "registry_created_epoch"):
        if _nat(registry[field], positive=field == "registry_revision") is None:
            issues.append("consumption_registry_receipt_invalid_nat:" + field)
    admissions = _unique_strings(registry["consumed_admission_receipt_digests"])
    nonces = _unique_strings(registry["consumed_execution_nonce_digests"])
    if admissions is None:
        issues.append("consumption_registry_receipt_admission_history_invalid")
    if nonces is None:
        issues.append("consumption_registry_receipt_nonce_history_invalid")
    if admissions is not None and nonces is not None and len(admissions) != len(nonces):
        issues.append("consumption_registry_receipt_parallel_history_length_mismatch")
    return registry, issues


def _validate_request(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    request = _mapping(value)
    if request is None:
        return None, ["execution_request_not_mapping"]
    issues = _exact(request, _REQUEST_FIELDS, "execution_request")
    if issues:
        return request, issues
    for field in _REQUEST_FIELDS - {"cycle_index", "request_created_epoch", REQUEST_DIGEST_FIELD}:
        if not isinstance(request[field], str) or not request[field]:
            issues.append("execution_request_invalid_string:" + field)
    if _nat(request["cycle_index"], positive=True) is None:
        issues.append("execution_request_cycle_index_invalid")
    if _nat(request["request_created_epoch"]) is None:
        issues.append("execution_request_created_epoch_invalid")
    if not _digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("execution_request_digest_mismatch")
    return request, issues


def _validate_policy(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    policy = _mapping(value)
    if policy is None:
        return None, ["execution_policy_not_mapping"]
    issues = _exact(policy, _POLICY_FIELDS, "execution_policy")
    if issues:
        return policy, issues
    string_fields = {
        "expected_execution_input_digest",
        "expected_admission_consumption_receipt_digest",
        "expected_consumption_registry_digest",
        "expected_repository_full_name",
        "expected_source_commit_sha",
        "expected_executor_actor_id",
    }
    for field in string_fields:
        if not isinstance(policy[field], str) or not policy[field]:
            issues.append("execution_policy_invalid_string:" + field)
    stages = _unique_strings(policy["allowed_stage_ids"], nonempty=True)
    if stages is None:
        issues.append("execution_policy_allowed_stage_ids_invalid")
    elif tuple(stages) != _ALLOWED_STAGE_IDS:
        issues.append("execution_policy_allowed_stage_ids_not_exact")
    bool_fields = {
        "network_access_allowed",
        "secrets_allowed",
        "live_repository_access_allowed",
        "git_operations_allowed",
        "merge_allowed",
        "deployment_allowed",
    }
    for field in bool_fields:
        if not isinstance(policy[field], bool):
            issues.append("execution_policy_invalid_bool:" + field)
        elif policy[field] is not False:
            issues.append("execution_policy_required_false:" + field)
    nat_fields = _POLICY_FIELDS - string_fields - bool_fields - {"allowed_stage_ids", POLICY_DIGEST_FIELD}
    for field in nat_fields:
        if _nat(policy[field], positive=field not in {"evaluation_epoch"}) is None:
            issues.append("execution_policy_invalid_nat:" + field)
    if not _digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("execution_policy_digest_mismatch")
    return policy, issues


def _validate_execution_registry(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    registry = _mapping(value)
    if registry is None:
        return None, ["execution_registry_not_mapping"]
    issues = _exact(registry, _REGISTRY_FIELDS, "execution_registry")
    if issues:
        return registry, issues
    if not isinstance(registry["registry_id"], str) or not registry["registry_id"]:
        issues.append("execution_registry_id_invalid")
    for field in ("registry_revision", "last_executed_cycle_index", "registry_created_epoch"):
        if _nat(registry[field], positive=field == "registry_revision") is None:
            issues.append("execution_registry_invalid_nat:" + field)
    inputs = _unique_strings(registry["consumed_execution_input_digests"])
    nonces = _unique_strings(registry["consumed_cycle_execution_nonce_digests"])
    if inputs is None:
        issues.append("execution_registry_input_history_invalid")
    if nonces is None:
        issues.append("execution_registry_nonce_history_invalid")
    if inputs is not None and nonces is not None and len(inputs) != len(nonces):
        issues.append("execution_registry_parallel_history_length_mismatch")
    if not _digest_ok(registry, REGISTRY_DIGEST_FIELD):
        issues.append("execution_registry_digest_mismatch")
    return registry, issues


def _validate_repository(value: Any) -> tuple[dict[str, str] | None, list[str]]:
    repository = _mapping(value)
    if repository is None:
        return None, ["isolated_repository_snapshot_not_mapping"]
    if not all(isinstance(path, str) and path and isinstance(content, str) for path, content in repository.items()):
        return None, ["isolated_repository_snapshot_not_text_mapping"]
    return dict(repository), []


def _validate_provider_result(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    result = _mapping(value)
    if result is None:
        return None, ["provider_result_not_mapping"]
    issues = _exact(result, _PROVIDER_RESULT_FIELDS, "provider_result")
    if issues:
        return result, issues
    for field in ("provider_id", "provider_session_id"):
        if not isinstance(result[field], str) or not result[field]:
            issues.append("provider_result_invalid_string:" + field)
    for field in ("provider_output_bytes", "generated_candidate_count"):
        if _nat(result[field]) is None:
            issues.append("provider_result_invalid_nat:" + field)
    for field in ("network_used", "secret_accessed", "live_repository_accessed", "git_effect_performed"):
        if not isinstance(result[field], bool):
            issues.append("provider_result_invalid_bool:" + field)
        elif result[field] is not False:
            issues.append("provider_result_forbidden_effect:" + field)
    if _mapping(result["source_repair_receipt"]) is None:
        issues.append("provider_result_repair_receipt_not_mapping")
    if _mapping(result["source_regeneration_receipt"]) is None:
        issues.append("provider_result_regeneration_receipt_not_mapping")
    candidates = result["repair_candidates"]
    if not isinstance(candidates, Sequence) or isinstance(candidates, (str, bytes)) or not candidates:
        issues.append("provider_result_candidates_not_nonempty_sequence")
    return result, issues


def _build_inner_request(
    *, request: Mapping[str, Any], execution_input: Mapping[str, Any]
) -> dict[str, Any]:
    value = {
        "cycle_request_id": request["execution_request_id"] + ":bounded-cycle",
        "cycle_request_revision": request["execution_request_revision"],
        "cycle_index": int(request["cycle_index"]),
        "source_repair_receipt_digest": execution_input["source_repair_receipt_digest"],
        "source_regeneration_receipt_digest": execution_input["source_regeneration_receipt_digest"],
        "repair_candidate_set_digest": execution_input["repair_candidate_set_digest"],
        "verification_plan_digest": execution_input["verification_plan_digest"],
        "verification_id": request["verification_id"],
        "verifier_id": request["verifier_id"],
        "reviewer_id": request["reviewer_id"],
        "verification_session_id": request["execution_session_id"],
        "verification_nonce_digest": request["cycle_execution_nonce_digest"],
        "evidence_format": request["evidence_format"],
        "toolchain_digest": request["toolchain_digest"],
        "environment_digest": request["environment_digest"],
        "verification_protocol_digest": request["verification_protocol_digest"],
        "requested_by_actor_id": request["executor_actor_id"],
        "request_created_epoch": int(request["request_created_epoch"]),
    }
    return seal(value, INNER_REQUEST_DIGEST_FIELD)


def _evidence_usage(
    *, evidence_bundle: Mapping[str, Any], verification_plan: Mapping[str, Any]
) -> tuple[int, int, int]:
    records = evidence_bundle.get("records")
    if not isinstance(records, list):
        return 0, 0, 0
    record_ids = {
        record.get("check_id")
        for record in records
        if isinstance(record, Mapping) and isinstance(record.get("check_id"), str)
    }
    checks = verification_plan.get("checks")
    if not isinstance(checks, list):
        checks = []
    timeout_seconds = sum(
        int(check.get("timeout_seconds", 0))
        for check in checks
        if isinstance(check, Mapping) and check.get("check_id") in record_ids
    )
    output_bytes = sum(
        int(record.get("stdout_size_bytes", 0)) + int(record.get("stderr_size_bytes", 0))
        for record in records
        if isinstance(record, Mapping)
    )
    return len(records), timeout_seconds, output_bytes


def _build_next_registry(
    *, registry: Mapping[str, Any], execution_input_digest: str, request: Mapping[str, Any], policy: Mapping[str, Any]
) -> dict[str, Any]:
    value = {
        "registry_id": registry["registry_id"],
        "registry_revision": int(registry["registry_revision"]) + 1,
        "consumed_execution_input_digests": list(registry["consumed_execution_input_digests"]) + [execution_input_digest],
        "consumed_cycle_execution_nonce_digests": list(registry["consumed_cycle_execution_nonce_digests"]) + [request["cycle_execution_nonce_digest"]],
        "last_executed_cycle_index": int(request["cycle_index"]),
        "registry_created_epoch": int(policy["evaluation_epoch"]),
    }
    return seal(value, REGISTRY_DIGEST_FIELD)


def _build_receipt(
    *,
    admission_consumption_receipt: Mapping[str, Any],
    execution_input: Mapping[str, Any],
    consumption_registry: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    execution_registry: Mapping[str, Any],
    next_registry: Mapping[str, Any],
    provider_result: Mapping[str, Any],
    inner_result: Any,
    candidate_count: int,
    command_count: int,
    timeout_seconds: int,
    runner_output_bytes: int,
) -> dict[str, Any]:
    inner_receipt = inner_result.receipt
    assert inner_receipt is not None
    evidence_bundle = inner_result.evidence_bundle
    independent = inner_result.independent_verification_evidence
    assert evidence_bundle is not None and independent is not None
    inner_disposition = inner_receipt["codeai_disposition"]
    disposition = (
        DISPOSITION_PASSED
        if inner_disposition == INNER_DISPOSITION_PASSED
        else DISPOSITION_ABORTED
        if inner_disposition == INNER_DISPOSITION_ABORTED
        else DISPOSITION_FAILED
    )
    provider_output = int(provider_result["provider_output_bytes"])
    used_output = provider_output + runner_output_bytes
    used = {
        "candidate": candidate_count,
        "provider_call": 1,
        "command": command_count,
        "timeout_seconds": timeout_seconds,
        "output_bytes": used_output,
    }
    maximum = {
        "candidate": int(execution_input["maximum_candidate_count"]),
        "provider_call": int(execution_input["maximum_provider_call_count"]),
        "command": int(execution_input["maximum_command_count"]),
        "timeout_seconds": int(execution_input["maximum_total_timeout_seconds"]),
        "output_bytes": int(execution_input["maximum_total_output_bytes"]),
    }
    value: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_admission_consumption_receipt_digest": admission_consumption_receipt[ADMISSION_CONSUMPTION_RECEIPT_DIGEST_FIELD],
        "source_execution_input_digest": execution_input[EXECUTION_INPUT_DIGEST_FIELD],
        "source_consumption_registry_digest": consumption_registry[ADMISSION_CONSUMPTION_REGISTRY_DIGEST_FIELD],
        "execution_request_digest": request[REQUEST_DIGEST_FIELD],
        "execution_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_execution_registry_digest": execution_registry[REGISTRY_DIGEST_FIELD],
        "next_execution_registry_digest": next_registry[REGISTRY_DIGEST_FIELD],
        "source_repair_receipt_digest": execution_input["source_repair_receipt_digest"],
        "source_regeneration_receipt_digest": execution_input["source_regeneration_receipt_digest"],
        "repair_candidate_set_digest": execution_input["repair_candidate_set_digest"],
        "verification_plan_digest": execution_input["verification_plan_digest"],
        "bounded_cycle_receipt_digest": inner_receipt[INNER_RECEIPT_DIGEST_FIELD],
        "selected_candidate_digest": inner_result.selected_candidate.patch_candidate[CANDIDATE_DIGEST_FIELD],
        "resulting_repository_snapshot_digest": canonical_digest(inner_result.resulting_repository_files),
        "evidence_bundle_digest": evidence_bundle[EVIDENCE_BUNDLE_DIGEST_FIELD],
        "independent_verification_evidence_digest": independent[INDEPENDENT_EVIDENCE_DIGEST_FIELD],
        "provider_id": provider_result["provider_id"],
        "provider_session_id": provider_result["provider_session_id"],
        "cycle_index": int(request["cycle_index"]),
        "source_registry_revision": int(execution_registry["registry_revision"]),
        "next_registry_revision": int(next_registry["registry_revision"]),
        "source_consumed_execution_input_count": len(execution_registry["consumed_execution_input_digests"]),
        "next_consumed_execution_input_count": len(next_registry["consumed_execution_input_digests"]),
        "provider_output_bytes": provider_output,
        "runner_output_bytes": runner_output_bytes,
        "failed_check_count": int(inner_receipt["failed_check_count"]),
        "codeai_disposition": disposition,
        "operating_mode": MODE_ADMISSION_GATED_EXECUTION,
    }
    for label in ("candidate", "provider_call", "command", "timeout_seconds", "output_bytes"):
        value["maximum_" + label] = maximum[label]
        value["used_" + label] = used[label]
        value["unused_" + label] = maximum[label] - used[label]
    value.update(
        {
            "route_receipt_recorded": True,
            "admission_consumption_receipt_verified": True,
            "execution_input_verified": True,
            "execution_input_consumed": True,
            "execution_input_replay_excluded": True,
            "cycle_execution_nonce_replay_excluded": True,
            "consumption_registry_correspondence_verified": True,
            "execution_registry_transition_verified": True,
            "exact_cycle_lineage_verified": True,
            "exact_repository_commit_lineage_verified": True,
            "exact_repair_regeneration_candidate_lineage_verified": True,
            "exact_verification_plan_lineage_verified": True,
            "failed_candidate_excluded_from_reselection": bool(inner_receipt["failed_candidate_excluded_from_reselection"]),
            "allowed_stage_set_verified": True,
            "candidate_budget_verified": True,
            "provider_call_budget_verified": True,
            "command_budget_verified": True,
            "timeout_budget_verified": True,
            "output_budget_verified": True,
            "provider_invoked": True,
            "runner_invoked": command_count > 0,
            "candidate_generated": candidate_count > 0,
            "candidate_selected": True,
            "isolated_patch_application_performed": True,
            "verification_executed": True,
            "cycle_execution_performed": True,
            "cycle_completed": True,
            "cycle_verification_passed": disposition == DISPOSITION_PASSED,
            "cycle_aborted_by_budget": disposition == DISPOSITION_ABORTED,
            "next_cycle_eligible": bool(inner_receipt["next_cycle_eligible"]),
            "next_cycle_authority_granted": False,
            "input_repository_snapshot_mutated": False,
            "isolated_repository_snapshot_updated": True,
            "live_repository_patch_applied": False,
            "repository_mutation_performed": False,
            "git_ref_changed": False,
            "branch_created": False,
            "commit_created": False,
            "push_performed": False,
            "pull_request_created": False,
            "network_access_performed": False,
            "secret_access_performed": False,
            "merge_performed": False,
            "deployment_performed": False,
            "merge_authority_granted": False,
            "deployment_authority_granted": False,
            "general_successor_stage_authority_granted": False,
            "execution_input_consumption_treated_as_correctness": False,
            "admitted_execution_treated_as_successful_repair": False,
            "cycle_pass_treated_as_proof": False,
            "cycle_failure_treated_as_required_repair": False,
            "provider_output_treated_as_trusted_patch": False,
            "candidate_selection_treated_as_correctness": False,
            "isolated_application_treated_as_live_mutation": False,
            "verification_evidence_treated_as_merge_authority": False,
            "unused_budget_treated_as_reusable_authority": False,
            "completed_cycle_treated_as_unrestricted_continuation": False,
            "execution_receipt_treated_as_git_authority": False,
            "execution_receipt_treated_as_deployment_authority": False,
            "execution_receipt_treated_as_general_successor_authority": False,
            "history_read_only": True,
            "future_only": True,
            "active_now": False,
        }
    )
    return seal(value, RECEIPT_DIGEST_FIELD)


def build_codeai_admission_gated_bounded_repair_cycle_execution(
    *,
    admission_consumption_receipt: Any,
    execution_input: Any,
    consumption_registry_receipt: Any,
    execution_request: Any,
    execution_policy: Any,
    execution_registry: Any,
    isolated_repository_files: Any,
    verification_plan: Any,
    bounded_cycle_policy: Any,
    provider_adapter: ProviderAdapter,
    runner_adapter: Callable[[Any], Mapping[str, Any]],
) -> CodeAIAdmissionGatedBoundedRepairCycleExecutionResult:
    issues: list[str] = []
    consumption, found = _validate_admission_consumption_receipt(admission_consumption_receipt)
    issues += found
    bounded_input, found = _validate_execution_input(execution_input)
    issues += found
    consumption_registry, found = _validate_consumption_registry(consumption_registry_receipt)
    issues += found
    request, found = _validate_request(execution_request)
    issues += found
    policy, found = _validate_policy(execution_policy)
    issues += found
    registry, found = _validate_execution_registry(execution_registry)
    issues += found
    repository, found = _validate_repository(isolated_repository_files)
    issues += found
    plan = _mapping(verification_plan)
    if plan is None:
        issues.append("verification_plan_not_mapping")
    elif not _digest_ok(plan, PLAN_DIGEST_FIELD):
        issues.append("verification_plan_digest_mismatch")
    inner_policy = _mapping(bounded_cycle_policy)
    if inner_policy is None:
        issues.append("bounded_cycle_policy_not_mapping")
    elif not _digest_ok(inner_policy, INNER_POLICY_DIGEST_FIELD):
        issues.append("bounded_cycle_policy_digest_mismatch")
    if not callable(provider_adapter):
        issues.append("provider_adapter_not_callable")
    if not callable(runner_adapter):
        issues.append("runner_adapter_not_callable")
    required = (consumption, bounded_input, consumption_registry, request, policy, registry, repository, plan, inner_policy)
    if issues or any(item is None for item in required):
        return CodeAIAdmissionGatedBoundedRepairCycleExecutionResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None, None, None, None, None
        )
    assert consumption is not None and bounded_input is not None
    assert consumption_registry is not None and request is not None and policy is not None
    assert registry is not None and repository is not None and plan is not None and inner_policy is not None

    execution_input_digest = bounded_input[EXECUTION_INPUT_DIGEST_FIELD]
    consumption_digest = consumption[ADMISSION_CONSUMPTION_RECEIPT_DIGEST_FIELD]
    consumption_registry_digest = consumption_registry[ADMISSION_CONSUMPTION_REGISTRY_DIGEST_FIELD]
    plan_digest = plan[PLAN_DIGEST_FIELD]
    correspondences = (
        (consumption["execution_input_digest"], execution_input_digest, "consumption_execution_input"),
        (consumption["next_consumption_registry_digest"], consumption_registry_digest, "consumption_registry"),
        (bounded_input["source_admission_receipt_digest"], consumption["source_admission_receipt_digest"], "source_admission"),
        (bounded_input["cycle_index"], consumption["admitted_cycle_index"], "admitted_cycle"),
        (request["execution_input_digest"], execution_input_digest, "request_execution_input"),
        (request["admission_consumption_receipt_digest"], consumption_digest, "request_consumption_receipt"),
        (request["consumption_registry_digest"], consumption_registry_digest, "request_consumption_registry"),
        (request["cycle_index"], bounded_input["cycle_index"], "request_cycle"),
        (request["execution_session_id"], bounded_input["execution_session_id"], "request_session"),
        (request["executor_actor_id"], bounded_input["consumer_actor_id"], "request_actor"),
        (policy["expected_execution_input_digest"], execution_input_digest, "policy_execution_input"),
        (policy["expected_admission_consumption_receipt_digest"], consumption_digest, "policy_consumption_receipt"),
        (policy["expected_consumption_registry_digest"], consumption_registry_digest, "policy_consumption_registry"),
        (policy["expected_cycle_index"], bounded_input["cycle_index"], "policy_cycle"),
        (policy["expected_executor_actor_id"], bounded_input["consumer_actor_id"], "policy_actor"),
        (bounded_input["verification_plan_digest"], plan_digest, "verification_plan"),
        (consumption_registry["registry_revision"], consumption["next_registry_revision"], "consumption_registry_revision"),
        (len(consumption_registry["consumed_admission_receipt_digests"]), consumption["next_consumed_admission_count"], "consumption_registry_count"),
        (consumption_registry["last_consumed_cycle_index"], bounded_input["cycle_index"], "consumption_registry_cycle"),
    )
    for actual, expected, label in correspondences:
        if actual != expected:
            issues.append("admission_gated_execution_correspondence_mismatch:" + label)

    evaluation = int(policy["evaluation_epoch"])
    minimum_epoch = evaluation - int(policy["maximum_request_age"])
    for epoch, label in (
        (int(request["request_created_epoch"]), "request"),
        (int(registry["registry_created_epoch"]), "execution_registry"),
        (int(consumption_registry["registry_created_epoch"]), "consumption_registry"),
    ):
        if not minimum_epoch <= epoch <= evaluation:
            issues.append("admission_gated_execution_" + label + "_window_invalid")

    input_history = list(registry["consumed_execution_input_digests"])
    nonce_history = list(registry["consumed_cycle_execution_nonce_digests"])
    if execution_input_digest in input_history:
        issues.append("admission_gated_execution_input_replay_detected")
    if request["cycle_execution_nonce_digest"] in nonce_history:
        issues.append("admission_gated_execution_nonce_replay_detected")
    if len(input_history) >= int(policy["maximum_executed_input_count"]):
        issues.append("admission_gated_execution_registry_capacity_exhausted")
    if int(registry["last_executed_cycle_index"]) >= int(request["cycle_index"]):
        issues.append("admission_gated_execution_cycle_not_strictly_after_registry_frontier")

    budget_pairs = (
        ("maximum_candidate_count", "maximum_candidate_count"),
        ("maximum_provider_call_count", "maximum_provider_call_count"),
        ("maximum_command_count", "maximum_command_count"),
        ("maximum_total_timeout_seconds", "maximum_total_timeout_seconds"),
        ("maximum_total_output_bytes", "maximum_total_output_bytes"),
    )
    for policy_field, input_field in budget_pairs:
        if int(policy[policy_field]) > int(bounded_input[input_field]):
            issues.append("admission_gated_execution_policy_exceeds_input_budget:" + policy_field)

    inner_pairs = (
        ("maximum_candidate_count", "maximum_candidate_count"),
        ("maximum_command_count", "maximum_command_count"),
        ("maximum_total_timeout_seconds", "maximum_total_timeout_seconds"),
        ("maximum_total_output_bytes", "maximum_total_output_bytes"),
    )
    for inner_field, outer_field in inner_pairs:
        inner_value = inner_policy.get(inner_field)
        if _nat(inner_value, positive=True) is None:
            issues.append("bounded_cycle_policy_invalid_budget:" + inner_field)
        elif int(inner_value) > int(policy[outer_field]):
            issues.append("bounded_cycle_policy_exceeds_admitted_budget:" + inner_field)
    for field in ("network_access_allowed", "secrets_allowed", "live_repository_access_allowed", "git_operations_allowed"):
        if inner_policy.get(field) is not False:
            issues.append("bounded_cycle_policy_required_false:" + field)

    if issues:
        return CodeAIAdmissionGatedBoundedRepairCycleExecutionResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None, None, None, None, None
        )

    invocation = AdmissionGatedCycleProviderInvocation(
        execution_input_digest=execution_input_digest,
        cycle_index=int(request["cycle_index"]),
        source_repair_receipt_digest=str(bounded_input["source_repair_receipt_digest"]),
        source_regeneration_receipt_digest=str(bounded_input["source_regeneration_receipt_digest"]),
        repair_candidate_set_digest=str(bounded_input["repair_candidate_set_digest"]),
        verification_plan_digest=str(bounded_input["verification_plan_digest"]),
        repository_snapshot_digest=canonical_digest(repository),
        maximum_candidate_count=int(policy["maximum_candidate_count"]),
        maximum_provider_call_count=int(policy["maximum_provider_call_count"]),
        maximum_output_bytes=int(policy["maximum_total_output_bytes"]),
        network_access_allowed=False,
        secrets_allowed=False,
        live_repository_access_allowed=False,
        git_operations_allowed=False,
    )
    try:
        raw_provider_result = provider_adapter(invocation)
    except Exception as exc:
        return CodeAIAdmissionGatedBoundedRepairCycleExecutionResult(
            STATUS_BLOCKED,
            ("provider_adapter_exception:" + type(exc).__name__,),
            None, None, None, None, None, None,
        )
    provider_result, found = _validate_provider_result(raw_provider_result)
    issues += found
    if provider_result is None or issues:
        return CodeAIAdmissionGatedBoundedRepairCycleExecutionResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None, None, None, None, None
        )

    repair = _mapping(provider_result["source_repair_receipt"])
    regeneration = _mapping(provider_result["source_regeneration_receipt"])
    candidates = provider_result["repair_candidates"]
    assert repair is not None and regeneration is not None
    try:
        candidate_set_digest = repair_candidate_set_digest(candidates)
    except Exception as exc:
        issues.append("provider_candidate_set_invalid:" + type(exc).__name__)
        candidate_set_digest = None
    provider_output_bytes = int(provider_result["provider_output_bytes"])
    candidate_count = len(candidates)
    if int(provider_result["generated_candidate_count"]) != candidate_count:
        issues.append("provider_generated_candidate_count_mismatch")
    if candidate_count > int(policy["maximum_candidate_count"]):
        issues.append("provider_candidate_budget_exceeded")
    if 1 > int(policy["maximum_provider_call_count"]):
        issues.append("provider_call_budget_exceeded")
    if provider_output_bytes > int(policy["maximum_total_output_bytes"]):
        issues.append("provider_output_budget_exceeded")
    if provider_output_bytes + int(inner_policy["maximum_total_output_bytes"]) > int(policy["maximum_total_output_bytes"]):
        issues.append("combined_provider_and_verification_output_budget_exceeded")
    lineage_pairs = (
        (repair.get(REPAIR_RECEIPT_DIGEST_FIELD), bounded_input["source_repair_receipt_digest"], "repair_receipt"),
        (regeneration.get(REGENERATION_RECEIPT_DIGEST_FIELD), bounded_input["source_regeneration_receipt_digest"], "regeneration_receipt"),
        (candidate_set_digest, bounded_input["repair_candidate_set_digest"], "candidate_set"),
        (inner_policy.get("expected_source_repair_receipt_digest"), bounded_input["source_repair_receipt_digest"], "inner_policy_repair"),
        (inner_policy.get("expected_source_regeneration_receipt_digest"), bounded_input["source_regeneration_receipt_digest"], "inner_policy_regeneration"),
        (inner_policy.get("expected_repair_candidate_set_digest"), bounded_input["repair_candidate_set_digest"], "inner_policy_candidate_set"),
        (inner_policy.get("expected_verification_plan_digest"), plan_digest, "inner_policy_plan"),
        (inner_policy.get("expected_repository_full_name"), policy["expected_repository_full_name"], "inner_policy_repository"),
        (inner_policy.get("expected_source_commit_sha"), policy["expected_source_commit_sha"], "inner_policy_commit"),
    )
    for actual, expected, label in lineage_pairs:
        if actual != expected:
            issues.append("admission_gated_execution_lineage_mismatch:" + label)
    repositories = {
        item.patch_candidate.get("repository_full_name")
        for item in candidates
        if hasattr(item, "patch_candidate") and isinstance(item.patch_candidate, Mapping)
    }
    commits = {
        item.patch_candidate.get("source_commit_sha")
        for item in candidates
        if hasattr(item, "patch_candidate") and isinstance(item.patch_candidate, Mapping)
    }
    if repositories != {policy["expected_repository_full_name"]}:
        issues.append("admission_gated_execution_repository_lineage_invalid")
    if commits != {policy["expected_source_commit_sha"]}:
        issues.append("admission_gated_execution_commit_lineage_invalid")
    if issues:
        return CodeAIAdmissionGatedBoundedRepairCycleExecutionResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None, None, None, None, None
        )

    inner_request = _build_inner_request(request=request, execution_input=bounded_input)
    repository_before = deepcopy(repository)
    inner_result = build_codeai_bounded_repair_cycle_orchestration(
        source_repair_receipt=deepcopy(repair),
        source_regeneration_receipt=deepcopy(regeneration),
        repair_candidates=tuple(deepcopy(candidates)),
        repository_files=repository,
        cycle_request=inner_request,
        cycle_policy=deepcopy(inner_policy),
        verification_plan=deepcopy(plan),
        runner_adapter=runner_adapter,
    )
    if inner_result.status != INNER_STATUS_READY or inner_result.receipt is None:
        return CodeAIAdmissionGatedBoundedRepairCycleExecutionResult(
            STATUS_BLOCKED,
            tuple(sorted(set(["bounded_cycle_execution_blocked"] + list(inner_result.issues)))),
            inner_result.selected_candidate,
            inner_result.resulting_repository_files,
            inner_result.evidence_bundle,
            inner_result.independent_verification_evidence,
            None,
            None,
        )
    if repository != repository_before:
        return CodeAIAdmissionGatedBoundedRepairCycleExecutionResult(
            STATUS_BLOCKED,
            ("isolated_repository_input_mutated_during_execution",),
            inner_result.selected_candidate,
            inner_result.resulting_repository_files,
            inner_result.evidence_bundle,
            inner_result.independent_verification_evidence,
            None,
            None,
        )
    assert inner_result.evidence_bundle is not None
    command_count, timeout_seconds, runner_output_bytes = _evidence_usage(
        evidence_bundle=inner_result.evidence_bundle,
        verification_plan=plan,
    )
    actual_budget_checks = (
        (candidate_count, int(policy["maximum_candidate_count"]), "candidate"),
        (1, int(policy["maximum_provider_call_count"]), "provider_call"),
        (command_count, int(policy["maximum_command_count"]), "command"),
        (timeout_seconds, int(policy["maximum_total_timeout_seconds"]), "timeout_seconds"),
        (provider_output_bytes + runner_output_bytes, int(policy["maximum_total_output_bytes"]), "output_bytes"),
    )
    for used, limit, label in actual_budget_checks:
        if used > limit:
            issues.append("admission_gated_execution_actual_budget_exceeded:" + label)
    if issues:
        return CodeAIAdmissionGatedBoundedRepairCycleExecutionResult(
            STATUS_BLOCKED,
            tuple(sorted(set(issues))),
            inner_result.selected_candidate,
            inner_result.resulting_repository_files,
            inner_result.evidence_bundle,
            inner_result.independent_verification_evidence,
            None,
            None,
        )

    next_registry = _build_next_registry(
        registry=registry,
        execution_input_digest=execution_input_digest,
        request=request,
        policy=policy,
    )
    receipt = _build_receipt(
        admission_consumption_receipt=consumption,
        execution_input=bounded_input,
        consumption_registry=consumption_registry,
        request=request,
        policy=policy,
        execution_registry=registry,
        next_registry=next_registry,
        provider_result=provider_result,
        inner_result=inner_result,
        candidate_count=candidate_count,
        command_count=command_count,
        timeout_seconds=timeout_seconds,
        runner_output_bytes=runner_output_bytes,
    )
    return CodeAIAdmissionGatedBoundedRepairCycleExecutionResult(
        STATUS_READY,
        (),
        inner_result.selected_candidate,
        inner_result.resulting_repository_files,
        inner_result.evidence_bundle,
        inner_result.independent_verification_evidence,
        next_registry,
        receipt,
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "AdmissionGatedCycleProviderInvocation",
    "ProviderAdapter",
    "CodeAIAdmissionGatedBoundedRepairCycleExecutionResult",
    "build_codeai_admission_gated_bounded_repair_cycle_execution",
]
