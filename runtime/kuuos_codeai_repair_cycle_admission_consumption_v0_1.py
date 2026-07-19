#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import canonical_digest, seal
from runtime.kuuos_codeai_repair_cycle_continuation_admission_v0_1 import (
    DISPOSITION_ADMITTED as ADMISSION_DISPOSITION_ADMITTED,
    MODE_CONTINUATION_ADMISSION as ADMISSION_MODE,
    PROFILE_VERSION as ADMISSION_PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD as ADMISSION_RECEIPT_DIGEST_FIELD,
)

VERSION = "kuuos_codeai_repair_cycle_admission_consumption_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Repair Cycle Admission Consumption v0.1"
EXECUTION_INPUT_PROFILE_VERSION = "CodeAI Repair Cycle Execution Input v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_ADMISSION_CONSUMPTION = "repair_cycle_admission_consumption"
MODE_BOUNDED_CYCLE_EXECUTION_INPUT = "bounded_repair_cycle_execution_input"
DISPOSITION_CONSUMED = "repair_cycle_admission_consumed"
EXECUTION_INPUT_DISPOSITION = "bounded_repair_cycle_execution_input_issued"
REQUEST_DIGEST_FIELD = "codeai_repair_cycle_admission_consumption_request_digest"
POLICY_DIGEST_FIELD = "codeai_repair_cycle_admission_consumption_policy_digest"
REGISTRY_DIGEST_FIELD = "codeai_repair_cycle_admission_consumption_registry_digest"
EXECUTION_INPUT_DIGEST_FIELD = "codeai_repair_cycle_execution_input_digest"
RECEIPT_DIGEST_FIELD = "codeai_repair_cycle_admission_consumption_receipt_digest"

_REQUEST_FIELDS = {
    "consumption_request_id",
    "consumption_request_revision",
    "admission_receipt_digest",
    "admitted_cycle_index",
    "source_cycle_receipt_digest",
    "source_selected_candidate_digest",
    "source_repair_receipt_digest",
    "source_regeneration_receipt_digest",
    "repair_candidate_set_digest",
    "verification_plan_digest",
    "execution_session_id",
    "execution_nonce_digest",
    "requested_by_actor_id",
    "request_created_epoch",
    REQUEST_DIGEST_FIELD,
}

_POLICY_FIELDS = {
    "expected_admission_receipt_digest",
    "expected_admitted_cycle_index",
    "expected_source_cycle_receipt_digest",
    "expected_source_selected_candidate_digest",
    "expected_source_repair_receipt_digest",
    "expected_source_regeneration_receipt_digest",
    "expected_repair_candidate_set_digest",
    "expected_verification_plan_digest",
    "expected_consumer_actor_id",
    "maximum_consumed_admission_count",
    "network_access_allowed",
    "secrets_allowed",
    "live_repository_access_allowed",
    "git_operations_allowed",
    "automatic_execution_allowed",
    "evaluation_epoch",
    "maximum_request_age",
    POLICY_DIGEST_FIELD,
}

_REGISTRY_FIELDS = {
    "registry_id",
    "registry_revision",
    "consumed_admission_receipt_digests",
    "consumed_execution_nonce_digests",
    "last_consumed_cycle_index",
    "registry_created_epoch",
    REGISTRY_DIGEST_FIELD,
}

_BUDGET_DIMENSIONS = (
    (
        "candidate",
        "reserved_candidate",
        "remaining_candidate_before_reservation",
        "remaining_candidate_after_reservation",
        "maximum_candidate_count",
    ),
    (
        "provider_call",
        "reserved_provider_call",
        "remaining_provider_call_before_reservation",
        "remaining_provider_call_after_reservation",
        "maximum_provider_call_count",
    ),
    (
        "command",
        "reserved_command",
        "remaining_command_before_reservation",
        "remaining_command_after_reservation",
        "maximum_command_count",
    ),
    (
        "timeout_seconds",
        "reserved_timeout_seconds",
        "remaining_timeout_seconds_before_reservation",
        "remaining_timeout_seconds_after_reservation",
        "maximum_total_timeout_seconds",
    ),
    (
        "output_bytes",
        "reserved_output_bytes",
        "remaining_output_bytes_before_reservation",
        "remaining_output_bytes_after_reservation",
        "maximum_total_output_bytes",
    ),
)


@dataclass(frozen=True)
class CodeAIRepairCycleAdmissionConsumptionResult:
    status: str
    issues: tuple[str, ...]
    execution_input: dict[str, Any] | None
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


def _strings(value: Any) -> list[str] | None:
    if not isinstance(value, list):
        return None
    if not all(isinstance(item, str) and item for item in value):
        return None
    if len(value) != len(set(value)):
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


def _validate_admission_receipt(
    value: Any,
) -> tuple[Mapping[str, Any] | None, list[str]]:
    receipt = _mapping(value)
    if receipt is None:
        return None, ["admission_receipt_not_mapping"]
    issues: list[str] = []
    if not _digest_ok(receipt, ADMISSION_RECEIPT_DIGEST_FIELD):
        issues.append("admission_receipt_digest_mismatch")
    if receipt.get("profile_version") != ADMISSION_PROFILE_VERSION:
        issues.append("admission_profile_unsupported")
    if receipt.get("operating_mode") != ADMISSION_MODE:
        issues.append("admission_mode_invalid")
    if receipt.get("codeai_disposition") != ADMISSION_DISPOSITION_ADMITTED:
        issues.append("admission_disposition_invalid")

    required_true = (
        "route_receipt_recorded",
        "source_cycle_lineage_verified",
        "cycle_sequence_verified",
        "remaining_budget_verified",
        "exactly_one_next_cycle_admitted",
        "continuation_admission_authority_granted",
        "history_read_only",
        "future_only",
    )
    for field in required_true:
        if receipt.get(field) is not True:
            issues.append("admission_required_true:" + field)

    required_false = (
        "admission_reusable",
        "admission_consumed",
        "automatic_next_cycle_started",
        "cycle_execution_performed",
        "runner_invoked",
        "candidate_generated",
        "candidate_selected",
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
        "execution_authority_granted",
        "automatic_execution_authority_granted",
        "general_successor_stage_authority_granted",
        "active_now",
    )
    for field in required_false:
        if receipt.get(field) is not False:
            issues.append("admission_required_false:" + field)

    for field in (
        ADMISSION_RECEIPT_DIGEST_FIELD,
        "source_cycle_receipt_digest",
        "source_selected_candidate_digest",
        "continuation_request_digest",
        "continuation_policy_digest",
        "budget_ledger_digest",
        "admission_scope",
    ):
        if not isinstance(receipt.get(field), str) or not receipt.get(field):
            issues.append("admission_invalid_string:" + field)

    current = _nat(receipt.get("current_cycle_index"), positive=True)
    admitted = _nat(receipt.get("admitted_cycle_index"), positive=True)
    maximum = _nat(receipt.get("maximum_cycle_count"), positive=True)
    if current is None:
        issues.append("admission_current_cycle_index_invalid")
    if admitted is None:
        issues.append("admission_admitted_cycle_index_invalid")
    if maximum is None:
        issues.append("admission_maximum_cycle_count_invalid")
    if current is not None and admitted is not None and admitted != current + 1:
        issues.append("admission_cycle_not_exact_successor")
    if admitted is not None and maximum is not None and admitted > maximum:
        issues.append("admission_cycle_exceeds_maximum")

    for label, reserved_field, before_field, after_field, _ in _BUDGET_DIMENSIONS:
        reserved = _nat(receipt.get(reserved_field), positive=True)
        before = _nat(receipt.get(before_field))
        after = _nat(receipt.get(after_field))
        if reserved is None:
            issues.append("admission_reserved_budget_invalid:" + label)
        if before is None:
            issues.append("admission_remaining_before_invalid:" + label)
        if after is None:
            issues.append("admission_remaining_after_invalid:" + label)
        if reserved is not None and before is not None and reserved > before:
            issues.append("admission_reserved_budget_exceeds_remaining:" + label)
        if (
            reserved is not None
            and before is not None
            and after is not None
            and after + reserved != before
        ):
            issues.append("admission_budget_conservation_mismatch:" + label)
    return receipt, issues


def _validate_request(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    request = _mapping(value)
    if request is None:
        return None, ["consumption_request_not_mapping"]
    issues = _exact(request, _REQUEST_FIELDS, "consumption_request")
    if issues:
        return request, issues
    string_fields = _REQUEST_FIELDS - {
        "admitted_cycle_index",
        "request_created_epoch",
        REQUEST_DIGEST_FIELD,
    }
    for field in string_fields:
        if not isinstance(request[field], str) or not request[field]:
            issues.append("consumption_request_invalid_string:" + field)
    if _nat(request["admitted_cycle_index"], positive=True) is None:
        issues.append("consumption_request_cycle_index_invalid")
    if _nat(request["request_created_epoch"]) is None:
        issues.append("consumption_request_created_epoch_invalid")
    if not _digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("consumption_request_digest_mismatch")
    return request, issues


def _validate_policy(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    policy = _mapping(value)
    if policy is None:
        return None, ["consumption_policy_not_mapping"]
    issues = _exact(policy, _POLICY_FIELDS, "consumption_policy")
    if issues:
        return policy, issues
    string_fields = {
        "expected_admission_receipt_digest",
        "expected_source_cycle_receipt_digest",
        "expected_source_selected_candidate_digest",
        "expected_source_repair_receipt_digest",
        "expected_source_regeneration_receipt_digest",
        "expected_repair_candidate_set_digest",
        "expected_verification_plan_digest",
        "expected_consumer_actor_id",
    }
    for field in string_fields:
        if not isinstance(policy[field], str) or not policy[field]:
            issues.append("consumption_policy_invalid_string:" + field)
    bool_fields = {
        "network_access_allowed",
        "secrets_allowed",
        "live_repository_access_allowed",
        "git_operations_allowed",
        "automatic_execution_allowed",
    }
    for field in bool_fields:
        if not isinstance(policy[field], bool):
            issues.append("consumption_policy_invalid_bool:" + field)
        elif policy[field] is not False:
            issues.append("consumption_policy_required_false:" + field)
    nat_fields = _POLICY_FIELDS - string_fields - bool_fields - {POLICY_DIGEST_FIELD}
    for field in nat_fields:
        if _nat(
            policy[field],
            positive=field not in {"evaluation_epoch"},
        ) is None:
            issues.append("consumption_policy_invalid_nat:" + field)
    if not _digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("consumption_policy_digest_mismatch")
    return policy, issues


def _validate_registry(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    registry = _mapping(value)
    if registry is None:
        return None, ["consumption_registry_not_mapping"]
    issues = _exact(registry, _REGISTRY_FIELDS, "consumption_registry")
    if issues:
        return registry, issues
    for field in ("registry_id",):
        if not isinstance(registry[field], str) or not registry[field]:
            issues.append("consumption_registry_invalid_string:" + field)
    for field in (
        "registry_revision",
        "last_consumed_cycle_index",
        "registry_created_epoch",
    ):
        if _nat(registry[field], positive=field == "registry_revision") is None:
            issues.append("consumption_registry_invalid_nat:" + field)
    admission_history = _strings(registry["consumed_admission_receipt_digests"])
    nonce_history = _strings(registry["consumed_execution_nonce_digests"])
    if admission_history is None:
        issues.append(
            "consumption_registry_invalid_string_list:"
            "consumed_admission_receipt_digests"
        )
    if nonce_history is None:
        issues.append(
            "consumption_registry_invalid_string_list:"
            "consumed_execution_nonce_digests"
        )
    if (
        admission_history is not None
        and nonce_history is not None
        and len(admission_history) != len(nonce_history)
    ):
        issues.append("consumption_registry_parallel_history_length_mismatch")
    if not _digest_ok(registry, REGISTRY_DIGEST_FIELD):
        issues.append("consumption_registry_digest_mismatch")
    return registry, issues


def _build_execution_input(
    *,
    admission: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": EXECUTION_INPUT_PROFILE_VERSION,
        "source_admission_receipt_digest": admission[ADMISSION_RECEIPT_DIGEST_FIELD],
        "source_cycle_receipt_digest": admission["source_cycle_receipt_digest"],
        "source_selected_candidate_digest": admission["source_selected_candidate_digest"],
        "source_repair_receipt_digest": request["source_repair_receipt_digest"],
        "source_regeneration_receipt_digest": request["source_regeneration_receipt_digest"],
        "repair_candidate_set_digest": request["repair_candidate_set_digest"],
        "verification_plan_digest": request["verification_plan_digest"],
        "cycle_index": int(admission["admitted_cycle_index"]),
        "execution_session_id": request["execution_session_id"],
        "execution_nonce_digest": request["execution_nonce_digest"],
        "consumer_actor_id": request["requested_by_actor_id"],
    }
    for _, reserved_field, _, _, output_field in _BUDGET_DIMENSIONS:
        value[output_field] = int(admission[reserved_field])
    value.update(
        {
            "codeai_disposition": EXECUTION_INPUT_DISPOSITION,
            "operating_mode": MODE_BOUNDED_CYCLE_EXECUTION_INPUT,
            "source_admission_consumed": True,
            "one_cycle_only": True,
            "one_shot": True,
            "execution_input_active": True,
            "execution_input_reusable": False,
            "execution_input_consumed": False,
            "bounded_cycle_execution_authority_granted": True,
            "candidate_generation_authority_granted": True,
            "candidate_selection_authority_granted": True,
            "isolated_patch_application_authority_granted": True,
            "verification_execution_authority_granted": True,
            "automatic_execution_authority_granted": False,
            "network_access_authority_granted": False,
            "secret_access_authority_granted": False,
            "live_repository_access_authority_granted": False,
            "git_operations_authority_granted": False,
            "merge_authority_granted": False,
            "deployment_authority_granted": False,
            "general_successor_stage_authority_granted": False,
            "cycle_execution_performed": False,
            "provider_invoked": False,
            "runner_invoked": False,
            "candidate_generated": False,
            "candidate_selected": False,
            "patch_applied": False,
            "verification_executed": False,
            "repository_mutation_performed": False,
            "git_ref_changed": False,
            "network_access_performed": False,
            "secret_access_performed": False,
            "merge_performed": False,
            "deployment_performed": False,
            "automatic_execution_allowed": bool(policy["automatic_execution_allowed"]),
            "history_read_only": True,
            "active_now": True,
        }
    )
    return seal(value, EXECUTION_INPUT_DIGEST_FIELD)


def _build_next_registry(
    *,
    registry: Mapping[str, Any],
    admission: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    value = {
        "registry_id": registry["registry_id"],
        "registry_revision": int(registry["registry_revision"]) + 1,
        "consumed_admission_receipt_digests": list(
            registry["consumed_admission_receipt_digests"]
        )
        + [admission[ADMISSION_RECEIPT_DIGEST_FIELD]],
        "consumed_execution_nonce_digests": list(
            registry["consumed_execution_nonce_digests"]
        )
        + [request["execution_nonce_digest"]],
        "last_consumed_cycle_index": int(admission["admitted_cycle_index"]),
        "registry_created_epoch": int(policy["evaluation_epoch"]),
    }
    return seal(value, REGISTRY_DIGEST_FIELD)


def _build_receipt(
    *,
    admission: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    registry: Mapping[str, Any],
    next_registry: Mapping[str, Any],
    execution_input: Mapping[str, Any],
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_admission_receipt_digest": admission[ADMISSION_RECEIPT_DIGEST_FIELD],
        "source_cycle_receipt_digest": admission["source_cycle_receipt_digest"],
        "source_selected_candidate_digest": admission["source_selected_candidate_digest"],
        "consumption_request_digest": request[REQUEST_DIGEST_FIELD],
        "consumption_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_consumption_registry_digest": registry[REGISTRY_DIGEST_FIELD],
        "next_consumption_registry_digest": next_registry[REGISTRY_DIGEST_FIELD],
        "execution_input_digest": execution_input[EXECUTION_INPUT_DIGEST_FIELD],
        "admitted_cycle_index": int(admission["admitted_cycle_index"]),
        "source_registry_revision": int(registry["registry_revision"]),
        "next_registry_revision": int(next_registry["registry_revision"]),
        "source_consumed_admission_count": len(
            registry["consumed_admission_receipt_digests"]
        ),
        "next_consumed_admission_count": len(
            next_registry["consumed_admission_receipt_digests"]
        ),
    }
    for label, reserved_field, _, _, output_field in _BUDGET_DIMENSIONS:
        value["reserved_" + label] = int(admission[reserved_field])
        value["execution_" + label + "_budget"] = int(execution_input[output_field])
    value.update(
        {
            "codeai_disposition": DISPOSITION_CONSUMED,
            "operating_mode": MODE_ADMISSION_CONSUMPTION,
            "route_receipt_recorded": True,
            "source_admission_verified": True,
            "source_admission_consumed": True,
            "admission_replay_excluded": True,
            "execution_nonce_replay_excluded": True,
            "registry_transition_verified": True,
            "exactly_one_execution_input_issued": True,
            "bounded_budget_mapping_verified": True,
            "consumption_authority_granted": True,
            "bounded_cycle_execution_authority_granted": True,
            "automatic_execution_authority_granted": False,
            "general_successor_stage_authority_granted": False,
            "cycle_execution_performed": False,
            "provider_invoked": False,
            "runner_invoked": False,
            "candidate_generated": False,
            "candidate_selected": False,
            "patch_applied": False,
            "verification_executed": False,
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
            "consumption_treated_as_execution": False,
            "consumption_treated_as_correctness": False,
            "reserved_budget_treated_as_consumed_budget": False,
            "execution_input_treated_as_success": False,
            "registry_receipt_treated_as_external_atomic_persistence": False,
            "one_shot_input_treated_as_reusable_capability": False,
            "history_read_only": True,
            "future_only": True,
            "active_now": False,
        }
    )
    return seal(value, RECEIPT_DIGEST_FIELD)


def build_codeai_repair_cycle_admission_consumption(
    *,
    admission_receipt: Any,
    consumption_request: Any,
    consumption_policy: Any,
    consumption_registry: Any,
) -> CodeAIRepairCycleAdmissionConsumptionResult:
    issues: list[str] = []
    admission, found = _validate_admission_receipt(admission_receipt)
    issues += found
    request, found = _validate_request(consumption_request)
    issues += found
    policy, found = _validate_policy(consumption_policy)
    issues += found
    registry, found = _validate_registry(consumption_registry)
    issues += found
    if issues or any(item is None for item in (admission, request, policy, registry)):
        return CodeAIRepairCycleAdmissionConsumptionResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None, None
        )
    assert admission is not None and request is not None
    assert policy is not None and registry is not None

    admission_digest = admission[ADMISSION_RECEIPT_DIGEST_FIELD]
    correspondences = (
        (request["admission_receipt_digest"], admission_digest, "request_admission"),
        (
            policy["expected_admission_receipt_digest"],
            admission_digest,
            "policy_admission",
        ),
        (
            request["admitted_cycle_index"],
            admission["admitted_cycle_index"],
            "request_cycle_index",
        ),
        (
            policy["expected_admitted_cycle_index"],
            admission["admitted_cycle_index"],
            "policy_cycle_index",
        ),
        (
            request["source_cycle_receipt_digest"],
            admission["source_cycle_receipt_digest"],
            "request_source_cycle",
        ),
        (
            policy["expected_source_cycle_receipt_digest"],
            admission["source_cycle_receipt_digest"],
            "policy_source_cycle",
        ),
        (
            request["source_selected_candidate_digest"],
            admission["source_selected_candidate_digest"],
            "request_selected_candidate",
        ),
        (
            policy["expected_source_selected_candidate_digest"],
            admission["source_selected_candidate_digest"],
            "policy_selected_candidate",
        ),
        (
            request["source_repair_receipt_digest"],
            policy["expected_source_repair_receipt_digest"],
            "source_repair_receipt",
        ),
        (
            request["source_regeneration_receipt_digest"],
            policy["expected_source_regeneration_receipt_digest"],
            "source_regeneration_receipt",
        ),
        (
            request["repair_candidate_set_digest"],
            policy["expected_repair_candidate_set_digest"],
            "repair_candidate_set",
        ),
        (
            request["verification_plan_digest"],
            policy["expected_verification_plan_digest"],
            "verification_plan",
        ),
        (
            request["requested_by_actor_id"],
            policy["expected_consumer_actor_id"],
            "consumer_actor",
        ),
    )
    for actual, expected, label in correspondences:
        if actual != expected:
            issues.append("consumption_correspondence_mismatch:" + label)

    evaluation = int(policy["evaluation_epoch"])
    minimum_epoch = evaluation - int(policy["maximum_request_age"])
    for epoch, label in (
        (int(request["request_created_epoch"]), "request"),
        (int(registry["registry_created_epoch"]), "registry"),
    ):
        if not minimum_epoch <= epoch <= evaluation:
            issues.append("consumption_" + label + "_window_invalid")

    consumed_admissions = list(registry["consumed_admission_receipt_digests"])
    consumed_nonces = list(registry["consumed_execution_nonce_digests"])
    if admission_digest in consumed_admissions:
        issues.append("consumption_admission_replay_detected")
    if request["execution_nonce_digest"] in consumed_nonces:
        issues.append("consumption_execution_nonce_replay_detected")
    if len(consumed_admissions) >= int(policy["maximum_consumed_admission_count"]):
        issues.append("consumption_registry_capacity_exhausted")
    if int(registry["last_consumed_cycle_index"]) >= int(admission["admitted_cycle_index"]):
        issues.append("consumption_cycle_not_strictly_after_registry_frontier")

    if issues:
        return CodeAIRepairCycleAdmissionConsumptionResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None, None
        )

    execution_input = _build_execution_input(
        admission=admission, request=request, policy=policy
    )
    next_registry = _build_next_registry(
        registry=registry, admission=admission, request=request, policy=policy
    )
    receipt = _build_receipt(
        admission=admission,
        request=request,
        policy=policy,
        registry=registry,
        next_registry=next_registry,
        execution_input=execution_input,
    )
    return CodeAIRepairCycleAdmissionConsumptionResult(
        STATUS_READY, (), execution_input, next_registry, receipt
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIRepairCycleAdmissionConsumptionResult",
    "build_codeai_repair_cycle_admission_consumption",
]
