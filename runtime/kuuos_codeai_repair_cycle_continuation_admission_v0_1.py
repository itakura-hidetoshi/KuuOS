#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import canonical_digest, seal
from runtime.kuuos_codeai_bounded_repair_cycle_orchestration_v0_1 import (
    DISPOSITION_ABORTED as SOURCE_DISPOSITION_ABORTED,
    DISPOSITION_FAILED as SOURCE_DISPOSITION_FAILED,
    MODE_BOUNDED_REPAIR_CYCLE as SOURCE_MODE,
    PROFILE_VERSION as SOURCE_PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
)

VERSION = "kuuos_codeai_repair_cycle_continuation_admission_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Repair Cycle Continuation Admission v0.1"
STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_CONTINUATION_ADMISSION = "repair_cycle_continuation_admission"
DISPOSITION_ADMITTED = "next_repair_cycle_admitted"
REQUEST_DIGEST_FIELD = "codeai_repair_cycle_continuation_request_digest"
POLICY_DIGEST_FIELD = "codeai_repair_cycle_continuation_policy_digest"
BUDGET_LEDGER_DIGEST_FIELD = "codeai_repair_cycle_budget_ledger_digest"
RECEIPT_DIGEST_FIELD = "codeai_repair_cycle_continuation_admission_receipt_digest"

_REQUEST_FIELDS = {
    "continuation_request_id",
    "continuation_request_revision",
    "source_cycle_receipt_digest",
    "source_selected_candidate_digest",
    "requested_next_cycle_index",
    "requested_candidate_reservation",
    "requested_provider_call_reservation",
    "requested_command_reservation",
    "requested_timeout_seconds_reservation",
    "requested_output_bytes_reservation",
    "continuation_nonce_digest",
    "requested_by_actor_id",
    "request_created_epoch",
    REQUEST_DIGEST_FIELD,
}

_POLICY_FIELDS = {
    "expected_source_cycle_receipt_digest",
    "expected_source_selected_candidate_digest",
    "expected_current_cycle_index",
    "maximum_cycle_count",
    "maximum_total_candidate_count",
    "maximum_total_provider_calls",
    "maximum_total_commands",
    "maximum_total_timeout_seconds",
    "maximum_total_output_bytes",
    "maximum_candidate_reservation_per_cycle",
    "maximum_provider_call_reservation_per_cycle",
    "maximum_command_reservation_per_cycle",
    "maximum_timeout_seconds_reservation_per_cycle",
    "maximum_output_bytes_reservation_per_cycle",
    "minimum_candidate_reservation",
    "minimum_provider_call_reservation",
    "minimum_command_reservation",
    "minimum_timeout_seconds_reservation",
    "minimum_output_bytes_reservation",
    "network_access_allowed",
    "secrets_allowed",
    "live_repository_access_allowed",
    "git_operations_allowed",
    "automatic_execution_allowed",
    "evaluation_epoch",
    "maximum_request_age",
    POLICY_DIGEST_FIELD,
}

_LEDGER_FIELDS = {
    "source_cycle_receipt_digest",
    "completed_cycle_count",
    "candidate_count_consumed",
    "provider_call_count_consumed",
    "command_count_consumed",
    "timeout_seconds_consumed",
    "output_bytes_consumed",
    "ledger_created_epoch",
    BUDGET_LEDGER_DIGEST_FIELD,
}

_BUDGET_DIMENSIONS = (
    ("candidate", "requested_candidate_reservation", "candidate_count_consumed",
     "maximum_total_candidate_count", "maximum_candidate_reservation_per_cycle",
     "minimum_candidate_reservation"),
    ("provider_call", "requested_provider_call_reservation", "provider_call_count_consumed",
     "maximum_total_provider_calls", "maximum_provider_call_reservation_per_cycle",
     "minimum_provider_call_reservation"),
    ("command", "requested_command_reservation", "command_count_consumed",
     "maximum_total_commands", "maximum_command_reservation_per_cycle",
     "minimum_command_reservation"),
    ("timeout_seconds", "requested_timeout_seconds_reservation", "timeout_seconds_consumed",
     "maximum_total_timeout_seconds", "maximum_timeout_seconds_reservation_per_cycle",
     "minimum_timeout_seconds_reservation"),
    ("output_bytes", "requested_output_bytes_reservation", "output_bytes_consumed",
     "maximum_total_output_bytes", "maximum_output_bytes_reservation_per_cycle",
     "minimum_output_bytes_reservation"),
)


@dataclass(frozen=True)
class CodeAIRepairCycleContinuationAdmissionResult:
    status: str
    issues: tuple[str, ...]
    receipt: dict[str, Any] | None


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _nat(value: Any, *, positive: bool = False) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    if positive and value == 0:
        return None
    return value


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


def _validate_source_receipt(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    receipt = _mapping(value)
    if receipt is None:
        return None, ["source_cycle_receipt_not_mapping"]
    issues: list[str] = []
    if not _digest_ok(receipt, SOURCE_RECEIPT_DIGEST_FIELD):
        issues.append("source_cycle_receipt_digest_mismatch")
    if receipt.get("profile_version") != SOURCE_PROFILE_VERSION:
        issues.append("source_cycle_profile_unsupported")
    if receipt.get("operating_mode") != SOURCE_MODE:
        issues.append("source_cycle_mode_invalid")
    if receipt.get("codeai_disposition") not in {
        SOURCE_DISPOSITION_FAILED,
        SOURCE_DISPOSITION_ABORTED,
    }:
        issues.append("source_cycle_disposition_not_continuable")
    required_true = (
        "route_receipt_recorded",
        "cycle_completed",
        "next_cycle_eligible",
        "history_read_only",
        "future_only",
    )
    for field in required_true:
        if receipt.get(field) is not True:
            issues.append("source_cycle_required_true:" + field)
    required_false = (
        "cycle_verification_passed",
        "cycle_limit_reached",
        "next_cycle_authority_granted",
        "active_now",
        "repository_mutation_performed",
        "git_ref_changed",
        "network_access_performed",
        "secret_access_performed",
        "merge_performed",
        "deployment_performed",
        "execution_authority_granted",
        "successor_stage_authority_granted",
    )
    for field in required_false:
        if receipt.get(field) is not False:
            issues.append("source_cycle_required_false:" + field)
    for field in (
        "selected_candidate_digest",
        SOURCE_RECEIPT_DIGEST_FIELD,
    ):
        if not isinstance(receipt.get(field), str) or not receipt.get(field):
            issues.append("source_cycle_invalid_string:" + field)
    cycle_index = _nat(receipt.get("cycle_index"), positive=True)
    maximum_cycle_count = _nat(receipt.get("maximum_cycle_count"), positive=True)
    if cycle_index is None:
        issues.append("source_cycle_index_invalid")
    if maximum_cycle_count is None:
        issues.append("source_cycle_maximum_invalid")
    if (
        cycle_index is not None
        and maximum_cycle_count is not None
        and cycle_index >= maximum_cycle_count
    ):
        issues.append("source_cycle_has_no_remaining_cycle_budget")
    return receipt, issues


def _validate_request(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    request = _mapping(value)
    if request is None:
        return None, ["continuation_request_not_mapping"]
    issues = _exact(request, _REQUEST_FIELDS, "continuation_request")
    if issues:
        return request, issues
    string_fields = {
        "continuation_request_id",
        "continuation_request_revision",
        "source_cycle_receipt_digest",
        "source_selected_candidate_digest",
        "continuation_nonce_digest",
        "requested_by_actor_id",
    }
    for field in string_fields:
        if not isinstance(request[field], str) or not request[field]:
            issues.append("continuation_request_invalid_string:" + field)
    nat_fields = _REQUEST_FIELDS - string_fields - {REQUEST_DIGEST_FIELD}
    for field in nat_fields:
        if _nat(request[field], positive=field != "request_created_epoch") is None:
            issues.append("continuation_request_invalid_nat:" + field)
    if not _digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("continuation_request_digest_mismatch")
    return request, issues


def _validate_policy(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    policy = _mapping(value)
    if policy is None:
        return None, ["continuation_policy_not_mapping"]
    issues = _exact(policy, _POLICY_FIELDS, "continuation_policy")
    if issues:
        return policy, issues
    string_fields = {
        "expected_source_cycle_receipt_digest",
        "expected_source_selected_candidate_digest",
    }
    for field in string_fields:
        if not isinstance(policy[field], str) or not policy[field]:
            issues.append("continuation_policy_invalid_string:" + field)
    bool_fields = {
        "network_access_allowed",
        "secrets_allowed",
        "live_repository_access_allowed",
        "git_operations_allowed",
        "automatic_execution_allowed",
    }
    for field in bool_fields:
        if not isinstance(policy[field], bool):
            issues.append("continuation_policy_invalid_bool:" + field)
        elif policy[field] is not False:
            issues.append("continuation_policy_required_false:" + field)
    nat_fields = _POLICY_FIELDS - string_fields - bool_fields - {POLICY_DIGEST_FIELD}
    for field in nat_fields:
        if _nat(policy[field], positive=field != "evaluation_epoch") is None:
            issues.append("continuation_policy_invalid_nat:" + field)
    for _, _, _, _, maximum_per_cycle, minimum in _BUDGET_DIMENSIONS:
        if (
            _nat(policy.get(maximum_per_cycle), positive=True) is not None
            and _nat(policy.get(minimum), positive=True) is not None
            and int(policy[minimum]) > int(policy[maximum_per_cycle])
        ):
            issues.append("continuation_policy_minimum_exceeds_cycle_maximum:" + minimum)
    if not _digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("continuation_policy_digest_mismatch")
    return policy, issues


def _validate_ledger(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    ledger = _mapping(value)
    if ledger is None:
        return None, ["budget_ledger_not_mapping"]
    issues = _exact(ledger, _LEDGER_FIELDS, "budget_ledger")
    if issues:
        return ledger, issues
    if not isinstance(ledger["source_cycle_receipt_digest"], str) or not ledger[
        "source_cycle_receipt_digest"
    ]:
        issues.append("budget_ledger_source_digest_invalid")
    for field in _LEDGER_FIELDS - {
        "source_cycle_receipt_digest",
        BUDGET_LEDGER_DIGEST_FIELD,
    }:
        if _nat(ledger[field], positive=False) is None:
            issues.append("budget_ledger_invalid_nat:" + field)
    if not _digest_ok(ledger, BUDGET_LEDGER_DIGEST_FIELD):
        issues.append("budget_ledger_digest_mismatch")
    return ledger, issues


def _receipt(
    *,
    source: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    ledger: Mapping[str, Any],
) -> dict[str, Any]:
    current = int(source["cycle_index"])
    admitted = int(request["requested_next_cycle_index"])
    value: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_cycle_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "source_selected_candidate_digest": source["selected_candidate_digest"],
        "continuation_request_digest": request[REQUEST_DIGEST_FIELD],
        "continuation_policy_digest": policy[POLICY_DIGEST_FIELD],
        "budget_ledger_digest": ledger[BUDGET_LEDGER_DIGEST_FIELD],
        "current_cycle_index": current,
        "admitted_cycle_index": admitted,
        "maximum_cycle_count": int(policy["maximum_cycle_count"]),
    }
    for label, requested, consumed, total, _, _ in _BUDGET_DIMENSIONS:
        reservation = int(request[requested])
        remaining_before = int(policy[total]) - int(ledger[consumed])
        value["reserved_" + label] = reservation
        value["remaining_" + label + "_before_reservation"] = remaining_before
        value["remaining_" + label + "_after_reservation"] = remaining_before - reservation
    value.update(
        {
            "codeai_disposition": DISPOSITION_ADMITTED,
            "operating_mode": MODE_CONTINUATION_ADMISSION,
            "route_receipt_recorded": True,
            "source_cycle_lineage_verified": True,
            "cycle_sequence_verified": True,
            "remaining_budget_verified": True,
            "exactly_one_next_cycle_admitted": True,
            "continuation_admission_authority_granted": True,
            "admission_scope": "one_sealed_next_cycle",
            "admission_reusable": False,
            "admission_consumed": False,
            "automatic_next_cycle_started": False,
            "cycle_execution_performed": False,
            "runner_invoked": False,
            "candidate_generated": False,
            "candidate_selected": False,
            "patch_applied": False,
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
            "automatic_execution_authority_granted": False,
            "merge_authority_granted": False,
            "deployment_authority_granted": False,
            "secret_access_authority_granted": False,
            "general_successor_stage_authority_granted": False,
            "admission_treated_as_execution": False,
            "admission_treated_as_correctness": False,
            "remaining_budget_treated_as_safe_outcome": False,
            "sequence_match_treated_as_success": False,
            "one_cycle_admission_treated_as_reusable_capability": False,
            "history_read_only": True,
            "future_only": True,
            "active_now": False,
        }
    )
    return seal(value, RECEIPT_DIGEST_FIELD)


def build_codeai_repair_cycle_continuation_admission(
    *,
    source_cycle_receipt: Any,
    continuation_request: Any,
    continuation_policy: Any,
    budget_ledger: Any,
) -> CodeAIRepairCycleContinuationAdmissionResult:
    issues: list[str] = []
    source, found = _validate_source_receipt(source_cycle_receipt)
    issues += found
    request, found = _validate_request(continuation_request)
    issues += found
    policy, found = _validate_policy(continuation_policy)
    issues += found
    ledger, found = _validate_ledger(budget_ledger)
    issues += found
    if issues or any(item is None for item in (source, request, policy, ledger)):
        return CodeAIRepairCycleContinuationAdmissionResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None
        )
    assert source is not None and request is not None
    assert policy is not None and ledger is not None

    source_digest = source[SOURCE_RECEIPT_DIGEST_FIELD]
    selected_digest = source["selected_candidate_digest"]
    correspondences = (
        (request["source_cycle_receipt_digest"], source_digest, "request_source_cycle"),
        (policy["expected_source_cycle_receipt_digest"], source_digest, "policy_source_cycle"),
        (ledger["source_cycle_receipt_digest"], source_digest, "ledger_source_cycle"),
        (
            request["source_selected_candidate_digest"],
            selected_digest,
            "request_selected_candidate",
        ),
        (
            policy["expected_source_selected_candidate_digest"],
            selected_digest,
            "policy_selected_candidate",
        ),
    )
    for actual, expected, label in correspondences:
        if actual != expected:
            issues.append("continuation_correspondence_mismatch:" + label)

    current = int(source["cycle_index"])
    maximum = int(source["maximum_cycle_count"])
    if int(policy["expected_current_cycle_index"]) != current:
        issues.append("continuation_current_cycle_index_mismatch")
    if int(policy["maximum_cycle_count"]) != maximum:
        issues.append("continuation_maximum_cycle_count_mismatch")
    if int(request["requested_next_cycle_index"]) != current + 1:
        issues.append("continuation_next_cycle_not_exact_successor")
    if int(request["requested_next_cycle_index"]) > maximum:
        issues.append("continuation_next_cycle_exceeds_maximum")
    if int(ledger["completed_cycle_count"]) != current:
        issues.append("continuation_ledger_completed_cycle_count_mismatch")

    evaluation = int(policy["evaluation_epoch"])
    minimum_epoch = evaluation - int(policy["maximum_request_age"])
    for epoch, label in (
        (int(request["request_created_epoch"]), "request"),
        (int(ledger["ledger_created_epoch"]), "ledger"),
    ):
        if not minimum_epoch <= epoch <= evaluation:
            issues.append("continuation_" + label + "_window_invalid")

    for (
        label,
        requested_field,
        consumed_field,
        total_field,
        per_cycle_field,
        minimum_field,
    ) in _BUDGET_DIMENSIONS:
        requested = int(request[requested_field])
        consumed = int(ledger[consumed_field])
        total = int(policy[total_field])
        per_cycle = int(policy[per_cycle_field])
        minimum_required = int(policy[minimum_field])
        if consumed > total:
            issues.append("continuation_budget_consumed_exceeds_total:" + label)
        if requested < minimum_required:
            issues.append("continuation_budget_reservation_below_minimum:" + label)
        if requested > per_cycle:
            issues.append("continuation_budget_reservation_exceeds_cycle_maximum:" + label)
        if consumed + requested > total:
            issues.append("continuation_budget_reservation_exceeds_remaining:" + label)

    if issues:
        return CodeAIRepairCycleContinuationAdmissionResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None
        )

    return CodeAIRepairCycleContinuationAdmissionResult(
        STATUS_READY,
        (),
        _receipt(source=source, request=request, policy=policy, ledger=ledger),
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIRepairCycleContinuationAdmissionResult",
    "build_codeai_repair_cycle_continuation_admission",
]
