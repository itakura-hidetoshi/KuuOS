from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping
import re

from runtime.kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    POLICY_DIGEST_FIELD as LIFECYCLE_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as LIFECYCLE_RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as LIFECYCLE_REQUEST_DIGEST_FIELD,
    STATE_DIGEST_FIELD as LIFECYCLE_STATE_DIGEST_FIELD,
    STATE_FIELDS,
    SOURCE_RECEIPT_DIGEST_FIELD as TRAJECTORY_RECEIPT_DIGEST_FIELD,
    STATUS_READY as LIFECYCLE_STATUS_READY,
    build_codeai_autonomous_git_lifecycle_envelope,
    canonical_digest,
)
from runtime.kuuos_codeai_autonomous_git_effect_reobservation_v0_1 import (
    DISPOSITION_COMPLETED as REOBSERVATION_COMPLETED,
    EVIDENCE_DIGEST_FIELD as REOBSERVATION_EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as REOBSERVATION_RECEIPT_DIGEST_FIELD,
)

VERSION = "kuuos_codeai_reobservation_gated_git_lifecycle_continuation_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Re-observation-Gated Git Lifecycle Continuation v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

REQUEST_DIGEST_FIELD = "codeai_reobservation_gated_git_lifecycle_continuation_request_digest"
POLICY_DIGEST_FIELD = "codeai_reobservation_gated_git_lifecycle_continuation_policy_digest"
REGISTRY_DIGEST_FIELD = "codeai_reobservation_gated_git_lifecycle_continuation_registry_digest"
EVIDENCE_DIGEST_FIELD = "codeai_reobservation_gated_git_lifecycle_continuation_evidence_digest"
RECEIPT_DIGEST_FIELD = "codeai_reobservation_gated_git_lifecycle_continuation_receipt_digest"

_SHA256 = re.compile(r"^[0-9a-f]{64}$")

SOURCE_REOBSERVATION_RECEIPT_FIELDS = {
    "schema_version", "profile_version", "source_lifecycle_receipt_digest",
    "source_execution_receipt_digest", "source_execution_evidence_digest",
    "reobservation_request_digest", "reobservation_policy_digest",
    "source_registry_digest", "next_registry_digest", "reobservation_evidence_digest",
    "lifecycle_state_digest", "lifecycle_id", "reobservation_id",
    "reobservation_session_id", "repository_full_name", "effect_phase",
    "source_execution_disposition", "codeai_disposition", "operating_mode",
    "route_receipt_recorded", "source_lifecycle_receipt_verified",
    "source_execution_receipt_verified", "source_execution_evidence_verified",
    "source_execution_receipt_consumed_for_reobservation", "reobservation_nonce_consumed",
    "registry_advanced_once", "exactly_one_adapter_invocation", "adapter_evidence_valid",
    "lifecycle_state_correspondence_confirmed", "source_effect_correspondence_confirmed",
    "fresh_lifecycle_state_issued", "reobservation_failure_recorded", "evidence_quarantined",
    "network_accessed", "secret_material_read", "git_write_performed",
    "deployment_performed", "effect_execution_performed",
    "automatic_successor_effect_authority_granted", "general_git_authority_granted",
    "general_successor_stage_authority_granted", "observation_treated_as_correctness",
    "merge_treated_as_truth", "history_read_only", "future_only", "active_now",
    REOBSERVATION_RECEIPT_DIGEST_FIELD,
}

SOURCE_REOBSERVATION_EVIDENCE_FIELDS = {
    "schema_version", "profile_version", "source_lifecycle_receipt_digest",
    "source_execution_receipt_digest", "source_execution_evidence_digest",
    "reobservation_request_digest", "effect_phase", "source_execution_disposition",
    "adapter_result", "adapter_evidence_valid", "adapter_evidence_issues",
    "lifecycle_state_correspondence_confirmed", "source_effect_correspondence_confirmed",
    "fresh_lifecycle_state_issued", REOBSERVATION_EVIDENCE_DIGEST_FIELD,
}

REQUEST_FIELDS = {
    "continuation_id", "continuation_revision", "continuation_session_id",
    "continuation_nonce_digest", "source_reobservation_receipt_digest",
    "source_reobservation_evidence_digest", "source_lifecycle_receipt_digest",
    "source_lifecycle_state_digest", "source_trajectory_receipt_digest",
    "delegated_lifecycle_request_digest", "delegated_lifecycle_policy_digest",
    "lifecycle_id", "executor_id", "repository_full_name", "request_created_epoch",
    "provenance_integrity_confirmed", "source_correspondence_confirmed",
    REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_source_reobservation_receipt_digest",
    "expected_source_reobservation_evidence_digest",
    "expected_source_lifecycle_receipt_digest", "expected_source_lifecycle_state_digest",
    "expected_source_trajectory_receipt_digest", "expected_repository_full_name",
    "authorized_executor_ids", "maximum_request_age", "maximum_state_age",
    "maximum_registry_entries", "evaluation_epoch", "allow_lifecycle_evaluation",
    "allow_state_projection", "allow_automatic_effect_execution", POLICY_DIGEST_FIELD,
}

REGISTRY_FIELDS = {
    "registry_id", "registry_revision", "consumed_reobservation_receipt_digests",
    "consumed_continuation_nonce_digests", "consumed_count",
    "last_continuation_epoch", REGISTRY_DIGEST_FIELD,
}


@dataclass(frozen=True)
class CodeAIReobservationGatedGitLifecycleContinuationResult:
    status: str
    issues: tuple[str, ...]
    evidence: dict[str, Any] | None
    next_registry: dict[str, Any] | None
    delegated_lifecycle_state: dict[str, Any] | None
    delegated_lifecycle_receipt: dict[str, Any] | None
    receipt: dict[str, Any] | None


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _exact_fields(value: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
    actual = set(value)
    issues: list[str] = []
    for field in sorted(fields - actual):
        issues.append(f"{prefix}_missing_field:{field}")
    for field in sorted(actual - fields):
        issues.append(f"{prefix}_extra_field:{field}")
    return issues


def _digest_ok(value: Mapping[str, Any], field: str) -> bool:
    digest = value.get(field)
    return isinstance(digest, str) and bool(_SHA256.fullmatch(digest)) and digest == canonical_digest(
        {key: item for key, item in value.items() if key != field}
    )


def _nat(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def _unique_digests(value: Any) -> tuple[str, ...] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return None
    parsed = tuple(value)
    if len(parsed) != len(set(parsed)) or not all(_SHA256.fullmatch(item) for item in parsed):
        return None
    return parsed


def _validate_reobservation_receipt(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, SOURCE_REOBSERVATION_RECEIPT_FIELDS, "source_reobservation_receipt")
    if issues:
        return issues
    if not _digest_ok(value, REOBSERVATION_RECEIPT_DIGEST_FIELD):
        issues.append("source_reobservation_receipt_digest_mismatch")
    required_true = (
        "route_receipt_recorded", "source_lifecycle_receipt_verified",
        "source_execution_receipt_verified", "source_execution_evidence_verified",
        "source_execution_receipt_consumed_for_reobservation", "reobservation_nonce_consumed",
        "registry_advanced_once", "exactly_one_adapter_invocation", "adapter_evidence_valid",
        "lifecycle_state_correspondence_confirmed", "source_effect_correspondence_confirmed",
        "fresh_lifecycle_state_issued", "history_read_only",
    )
    if value.get("codeai_disposition") != REOBSERVATION_COMPLETED:
        issues.append("source_reobservation_not_completed")
    for field in required_true:
        if value.get(field) is not True:
            issues.append(f"source_reobservation_required_true:{field}")
    required_false = (
        "reobservation_failure_recorded", "evidence_quarantined", "network_accessed",
        "secret_material_read", "git_write_performed", "deployment_performed",
        "effect_execution_performed", "automatic_successor_effect_authority_granted",
        "general_git_authority_granted", "general_successor_stage_authority_granted",
        "observation_treated_as_correctness", "merge_treated_as_truth", "active_now",
    )
    for field in required_false:
        if value.get(field) is not False:
            issues.append(f"source_reobservation_required_false:{field}")
    for field in (
        "source_lifecycle_receipt_digest", "source_execution_receipt_digest",
        "source_execution_evidence_digest", "reobservation_evidence_digest",
        "lifecycle_state_digest", REOBSERVATION_RECEIPT_DIGEST_FIELD,
    ):
        if not isinstance(value.get(field), str) or not _SHA256.fullmatch(value[field]):
            issues.append(f"source_reobservation_invalid_digest:{field}")
    return issues


def _validate_reobservation_evidence(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, SOURCE_REOBSERVATION_EVIDENCE_FIELDS, "source_reobservation_evidence")
    if issues:
        return issues
    if not _digest_ok(value, REOBSERVATION_EVIDENCE_DIGEST_FIELD):
        issues.append("source_reobservation_evidence_digest_mismatch")
    if value.get("adapter_evidence_valid") is not True:
        issues.append("source_reobservation_evidence_adapter_invalid")
    if value.get("lifecycle_state_correspondence_confirmed") is not True:
        issues.append("source_reobservation_evidence_state_correspondence_missing")
    if value.get("source_effect_correspondence_confirmed") is not True:
        issues.append("source_reobservation_evidence_effect_correspondence_missing")
    if value.get("fresh_lifecycle_state_issued") is not True:
        issues.append("source_reobservation_evidence_fresh_state_missing")
    if value.get("adapter_evidence_issues") != []:
        issues.append("source_reobservation_evidence_has_adapter_issues")
    return issues


def _validate_request(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, REQUEST_FIELDS, "continuation_request")
    if issues:
        return issues
    string_fields = REQUEST_FIELDS - {
        "request_created_epoch", "provenance_integrity_confirmed",
        "source_correspondence_confirmed", REQUEST_DIGEST_FIELD,
    }
    for field in string_fields:
        if not isinstance(value.get(field), str) or not value[field]:
            issues.append(f"continuation_request_invalid_string:{field}")
    digest_fields = {
        "continuation_nonce_digest", "source_reobservation_receipt_digest",
        "source_reobservation_evidence_digest", "source_lifecycle_receipt_digest",
        "source_lifecycle_state_digest", "source_trajectory_receipt_digest",
        "delegated_lifecycle_request_digest", "delegated_lifecycle_policy_digest",
    }
    for field in digest_fields:
        if not isinstance(value.get(field), str) or not _SHA256.fullmatch(value[field]):
            issues.append(f"continuation_request_invalid_digest:{field}")
    if _nat(value.get("request_created_epoch")) is None:
        issues.append("continuation_request_invalid_epoch")
    for field in ("provenance_integrity_confirmed", "source_correspondence_confirmed"):
        if value.get(field) is not True:
            issues.append(f"continuation_request_required_true:{field}")
    if not _digest_ok(value, REQUEST_DIGEST_FIELD):
        issues.append("continuation_request_digest_mismatch")
    return issues


def _validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, POLICY_FIELDS, "continuation_policy")
    if issues:
        return issues
    digest_fields = {
        "expected_source_reobservation_receipt_digest",
        "expected_source_reobservation_evidence_digest",
        "expected_source_lifecycle_receipt_digest", "expected_source_lifecycle_state_digest",
        "expected_source_trajectory_receipt_digest", POLICY_DIGEST_FIELD,
    }
    for field in digest_fields:
        if not isinstance(value.get(field), str) or not _SHA256.fullmatch(value[field]):
            issues.append(f"continuation_policy_invalid_digest:{field}")
    if not isinstance(value.get("expected_repository_full_name"), str) or not value["expected_repository_full_name"]:
        issues.append("continuation_policy_invalid_repository")
    executors = value.get("authorized_executor_ids")
    if not isinstance(executors, list) or not executors or len(executors) != len(set(executors)) or not all(isinstance(x, str) and x for x in executors):
        issues.append("continuation_policy_invalid_authorized_executors")
    for field in ("maximum_request_age", "maximum_state_age", "maximum_registry_entries"):
        parsed = _nat(value.get(field))
        if parsed is None or parsed == 0:
            issues.append(f"continuation_policy_invalid_positive_nat:{field}")
    if _nat(value.get("evaluation_epoch")) is None:
        issues.append("continuation_policy_invalid_evaluation_epoch")
    for field in ("allow_lifecycle_evaluation", "allow_state_projection", "allow_automatic_effect_execution"):
        if not isinstance(value.get(field), bool):
            issues.append(f"continuation_policy_invalid_bool:{field}")
    if not _digest_ok(value, POLICY_DIGEST_FIELD):
        issues.append("continuation_policy_digest_mismatch")
    return issues


def _validate_registry(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, REGISTRY_FIELDS, "continuation_registry")
    if issues:
        return issues
    if not isinstance(value.get("registry_id"), str) or not value["registry_id"]:
        issues.append("continuation_registry_invalid_id")
    for field in ("registry_revision", "consumed_count", "last_continuation_epoch"):
        if _nat(value.get(field)) is None:
            issues.append(f"continuation_registry_invalid_nat:{field}")
    receipts = _unique_digests(value.get("consumed_reobservation_receipt_digests"))
    nonces = _unique_digests(value.get("consumed_continuation_nonce_digests"))
    if receipts is None:
        issues.append("continuation_registry_invalid_receipt_history")
    if nonces is None:
        issues.append("continuation_registry_invalid_nonce_history")
    if receipts is not None and nonces is not None:
        if len(receipts) != len(nonces):
            issues.append("continuation_registry_parallel_history_mismatch")
        if value.get("consumed_count") != len(receipts):
            issues.append("continuation_registry_count_mismatch")
    if not _digest_ok(value, REGISTRY_DIGEST_FIELD):
        issues.append("continuation_registry_digest_mismatch")
    return issues


def _project_state_for_lifecycle_evaluation(
    state: Mapping[str, Any], lifecycle_policy: Mapping[str, Any], allow_projection: bool,
) -> tuple[dict[str, Any] | None, bool, tuple[str, ...]]:
    projected = dict(state)
    projection_performed = False
    if projected.get("checks_observed") is False and projected.get("required_check_names"):
        if not allow_projection:
            return None, False, ("continuation_state_projection_not_allowed",)
        if projected.get("successful_check_names") or projected.get("pending_check_names") or projected.get("failed_check_names"):
            return None, False, ("continuation_unobserved_checks_have_partition_entries",)
        projected["required_check_names"] = []
        projection_performed = True
    elif projected.get("checks_observed") is True:
        required = sorted(projected.get("required_check_names", []))
        if required != sorted(lifecycle_policy.get("required_check_names", [])):
            return None, False, ("continuation_observed_required_checks_policy_mismatch",)
    projected.pop(LIFECYCLE_STATE_DIGEST_FIELD, None)
    projected[LIFECYCLE_STATE_DIGEST_FIELD] = canonical_digest(projected)
    return projected, projection_performed, ()


def _next_registry(
    registry: Mapping[str, Any], source_receipt_digest: str, nonce_digest: str, epoch: int,
) -> dict[str, Any]:
    result = {
        "registry_id": registry["registry_id"],
        "registry_revision": registry["registry_revision"] + 1,
        "consumed_reobservation_receipt_digests": [
            *registry["consumed_reobservation_receipt_digests"], source_receipt_digest,
        ],
        "consumed_continuation_nonce_digests": [
            *registry["consumed_continuation_nonce_digests"], nonce_digest,
        ],
        "consumed_count": registry["consumed_count"] + 1,
        "last_continuation_epoch": epoch,
    }
    result[REGISTRY_DIGEST_FIELD] = canonical_digest(result)
    return result


def build_codeai_reobservation_gated_git_lifecycle_continuation(
    *,
    source_trajectory_receipt: Any,
    source_reobservation_receipt: Any,
    source_reobservation_evidence: Any,
    source_lifecycle_state: Any,
    continuation_request: Any,
    continuation_policy: Any,
    continuation_registry: Any,
    delegated_lifecycle_request: Any,
    delegated_lifecycle_policy: Any,
) -> CodeAIReobservationGatedGitLifecycleContinuationResult:
    reobs = _mapping(source_reobservation_receipt)
    reobs_evidence = _mapping(source_reobservation_evidence)
    state = _mapping(source_lifecycle_state)
    request = _mapping(continuation_request)
    policy = _mapping(continuation_policy)
    registry = _mapping(continuation_registry)
    delegated_request = _mapping(delegated_lifecycle_request)
    delegated_policy = _mapping(delegated_lifecycle_policy)
    trajectory = _mapping(source_trajectory_receipt)
    issues: list[str] = []
    if trajectory is None:
        issues.append("source_trajectory_receipt_not_mapping")
    if reobs is None:
        issues.append("source_reobservation_receipt_not_mapping")
    else:
        issues.extend(_validate_reobservation_receipt(reobs))
    if reobs_evidence is None:
        issues.append("source_reobservation_evidence_not_mapping")
    else:
        issues.extend(_validate_reobservation_evidence(reobs_evidence))
    if state is None:
        issues.append("source_lifecycle_state_not_mapping")
    else:
        issues.extend(_exact_fields(state, STATE_FIELDS, "source_lifecycle_state"))
        if not _digest_ok(state, LIFECYCLE_STATE_DIGEST_FIELD):
            issues.append("source_lifecycle_state_digest_mismatch")
    if request is None:
        issues.append("continuation_request_not_mapping")
    else:
        issues.extend(_validate_request(request))
    if policy is None:
        issues.append("continuation_policy_not_mapping")
    else:
        issues.extend(_validate_policy(policy))
    if registry is None:
        issues.append("continuation_registry_not_mapping")
    else:
        issues.extend(_validate_registry(registry))
    if delegated_request is None:
        issues.append("delegated_lifecycle_request_not_mapping")
    if delegated_policy is None:
        issues.append("delegated_lifecycle_policy_not_mapping")
    if issues or None in (trajectory, reobs, reobs_evidence, state, request, policy, registry, delegated_request, delegated_policy):
        return CodeAIReobservationGatedGitLifecycleContinuationResult(
            STATUS_BLOCKED, tuple(issues), None, None, None, None, None,
        )
    assert trajectory is not None and reobs is not None and reobs_evidence is not None
    assert state is not None and request is not None and policy is not None and registry is not None
    assert delegated_request is not None and delegated_policy is not None

    source_receipt_digest = reobs[REOBSERVATION_RECEIPT_DIGEST_FIELD]
    source_evidence_digest = reobs_evidence[REOBSERVATION_EVIDENCE_DIGEST_FIELD]
    state_digest = state[LIFECYCLE_STATE_DIGEST_FIELD]
    trajectory_digest = trajectory.get(TRAJECTORY_RECEIPT_DIGEST_FIELD)
    correspondence = (
        reobs["reobservation_evidence_digest"] == source_evidence_digest
        and reobs["lifecycle_state_digest"] == state_digest
        and reobs_evidence["source_lifecycle_receipt_digest"] == reobs["source_lifecycle_receipt_digest"]
        and reobs_evidence["source_execution_receipt_digest"] == reobs["source_execution_receipt_digest"]
        and reobs_evidence["source_execution_evidence_digest"] == reobs["source_execution_evidence_digest"]
        and state["lifecycle_id"] == reobs["lifecycle_id"] == request["lifecycle_id"]
        and state["repository_full_name"] == reobs["repository_full_name"] == request["repository_full_name"]
        and state["executor_id"] == request["executor_id"]
        and state["source_trajectory_receipt_digest"] == trajectory_digest
        and request["source_reobservation_receipt_digest"] == source_receipt_digest
        and request["source_reobservation_evidence_digest"] == source_evidence_digest
        and request["source_lifecycle_receipt_digest"] == reobs["source_lifecycle_receipt_digest"]
        and request["source_lifecycle_state_digest"] == state_digest
        and request["source_trajectory_receipt_digest"] == trajectory_digest
        and request["delegated_lifecycle_request_digest"] == delegated_request.get(LIFECYCLE_REQUEST_DIGEST_FIELD)
        and request["delegated_lifecycle_policy_digest"] == delegated_policy.get(LIFECYCLE_POLICY_DIGEST_FIELD)
        and policy["expected_source_reobservation_receipt_digest"] == source_receipt_digest
        and policy["expected_source_reobservation_evidence_digest"] == source_evidence_digest
        and policy["expected_source_lifecycle_receipt_digest"] == reobs["source_lifecycle_receipt_digest"]
        and policy["expected_source_lifecycle_state_digest"] == state_digest
        and policy["expected_source_trajectory_receipt_digest"] == trajectory_digest
        and policy["expected_repository_full_name"] == state["repository_full_name"]
        and request["executor_id"] in policy["authorized_executor_ids"]
    )
    if not correspondence:
        issues.append("continuation_source_correspondence_mismatch")
    evaluation_epoch = policy["evaluation_epoch"]
    if (
        request["request_created_epoch"] > evaluation_epoch
        or evaluation_epoch - request["request_created_epoch"] > policy["maximum_request_age"]
        or state["observed_at_epoch"] > evaluation_epoch
        or evaluation_epoch - state["observed_at_epoch"] > policy["maximum_state_age"]
    ):
        issues.append("continuation_freshness_window_violation")
    consumed_receipts = registry["consumed_reobservation_receipt_digests"]
    consumed_nonces = registry["consumed_continuation_nonce_digests"]
    if source_receipt_digest in consumed_receipts:
        issues.append("continuation_source_reobservation_receipt_replay")
    if request["continuation_nonce_digest"] in consumed_nonces:
        issues.append("continuation_nonce_replay")
    if registry["consumed_count"] >= policy["maximum_registry_entries"]:
        issues.append("continuation_registry_capacity_exhausted")
    if policy["allow_lifecycle_evaluation"] is not True:
        issues.append("continuation_lifecycle_evaluation_not_allowed")
    if policy["allow_automatic_effect_execution"] is not False:
        issues.append("continuation_automatic_effect_execution_not_denied")
    prior_receipts = delegated_request.get("prior_lifecycle_receipt_digests")
    if not isinstance(prior_receipts, list) or prior_receipts.count(reobs["source_lifecycle_receipt_digest"]) != 1:
        issues.append("continuation_prior_lifecycle_receipt_not_recorded_once")
    if delegated_request.get("execution_session_id") == reobs.get("reobservation_session_id"):
        issues.append("continuation_execution_session_not_fresh")
    if delegated_request.get("source_trajectory_receipt_digest") != trajectory_digest:
        issues.append("continuation_delegated_trajectory_mismatch")
    if delegated_request.get("lifecycle_id") != state["lifecycle_id"]:
        issues.append("continuation_delegated_lifecycle_mismatch")
    if delegated_request.get("repository_full_name") != state["repository_full_name"]:
        issues.append("continuation_delegated_repository_mismatch")
    if issues:
        return CodeAIReobservationGatedGitLifecycleContinuationResult(
            STATUS_BLOCKED, tuple(issues), None, None, None, None, None,
        )

    projected_state, projection_performed, projection_issues = _project_state_for_lifecycle_evaluation(
        state, delegated_policy, policy["allow_state_projection"]
    )
    if projection_issues or projected_state is None:
        return CodeAIReobservationGatedGitLifecycleContinuationResult(
            STATUS_BLOCKED, projection_issues, None, None, None, None, None,
        )

    delegated = build_codeai_autonomous_git_lifecycle_envelope(
        source_trajectory_receipt=trajectory,
        lifecycle_request=delegated_request,
        lifecycle_state=projected_state,
        lifecycle_policy=delegated_policy,
    )
    if delegated.status != LIFECYCLE_STATUS_READY or delegated.receipt is None:
        return CodeAIReobservationGatedGitLifecycleContinuationResult(
            STATUS_BLOCKED,
            tuple(f"delegated_lifecycle:{issue}" for issue in delegated.issues),
            None, None, projected_state, None, None,
        )

    next_registry = _next_registry(
        registry, source_receipt_digest, request["continuation_nonce_digest"], evaluation_epoch
    )
    delegated_receipt = delegated.receipt
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_reobservation_receipt_digest": source_receipt_digest,
        "source_reobservation_evidence_digest": source_evidence_digest,
        "source_lifecycle_state_digest": state_digest,
        "delegated_lifecycle_state_digest": projected_state[LIFECYCLE_STATE_DIGEST_FIELD],
        "delegated_lifecycle_request_digest": delegated_request[LIFECYCLE_REQUEST_DIGEST_FIELD],
        "delegated_lifecycle_policy_digest": delegated_policy[LIFECYCLE_POLICY_DIGEST_FIELD],
        "delegated_lifecycle_receipt_digest": delegated_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "state_projection_performed": projection_performed,
        "lifecycle_evaluation_succeeded": True,
        "one_effect_lease_issued": delegated_receipt["execution_lease_issued"],
        "next_effect_phase": delegated_receipt["next_effect_phase"],
        "codeai_disposition": delegated_receipt["codeai_disposition"],
    }
    evidence[EVIDENCE_DIGEST_FIELD] = canonical_digest(evidence)
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_reobservation_receipt_digest": source_receipt_digest,
        "source_reobservation_evidence_digest": source_evidence_digest,
        "source_lifecycle_receipt_digest": reobs["source_lifecycle_receipt_digest"],
        "source_lifecycle_state_digest": state_digest,
        "delegated_lifecycle_state_digest": projected_state[LIFECYCLE_STATE_DIGEST_FIELD],
        "delegated_lifecycle_request_digest": delegated_request[LIFECYCLE_REQUEST_DIGEST_FIELD],
        "delegated_lifecycle_policy_digest": delegated_policy[LIFECYCLE_POLICY_DIGEST_FIELD],
        "delegated_lifecycle_receipt_digest": delegated_receipt[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "continuation_request_digest": request[REQUEST_DIGEST_FIELD],
        "continuation_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_registry_digest": registry[REGISTRY_DIGEST_FIELD],
        "next_registry_digest": next_registry[REGISTRY_DIGEST_FIELD],
        "continuation_evidence_digest": evidence[EVIDENCE_DIGEST_FIELD],
        "lifecycle_id": request["lifecycle_id"],
        "continuation_id": request["continuation_id"],
        "continuation_session_id": request["continuation_session_id"],
        "repository_full_name": request["repository_full_name"],
        "executor_id": request["executor_id"],
        "codeai_disposition": delegated_receipt["codeai_disposition"],
        "operating_mode": delegated_receipt["operating_mode"],
        "next_effect_phase": delegated_receipt["next_effect_phase"],
        "route_receipt_recorded": True,
        "source_reobservation_receipt_verified": True,
        "source_reobservation_evidence_verified": True,
        "source_lifecycle_state_verified": True,
        "source_reobservation_receipt_consumed": True,
        "continuation_nonce_consumed": True,
        "registry_advanced_once": True,
        "exactly_one_lifecycle_evaluation": True,
        "state_projection_performed": projection_performed,
        "state_projection_factual_fields_changed": False,
        "delegated_lifecycle_receipt_issued": True,
        "one_effect_lease_issued": delegated_receipt["execution_lease_issued"],
        "local_commit_authority_granted": delegated_receipt["local_commit_authority_granted"],
        "push_authority_granted": delegated_receipt["push_authority_granted"],
        "pull_request_authority_granted": delegated_receipt["pull_request_authority_granted"],
        "pull_request_readiness_authority_granted": delegated_receipt["pull_request_readiness_authority_granted"],
        "merge_authority_granted": delegated_receipt["merge_authority_granted"],
        "checks_wait_required": delegated_receipt["checks_wait_required"],
        "automatic_effect_execution_performed": False,
        "reobservation_state_treated_as_authority": False,
        "checks_treated_as_correctness_proof": False,
        "merge_treated_as_truth": False,
        "general_git_authority_granted": False,
        "general_successor_stage_authority_granted": False,
        "deployment_authority_granted": False,
        "secret_access_authority_granted": False,
        "history_read_only": True,
        "future_only": delegated_receipt["future_only"],
        "active_now": delegated_receipt["active_now"],
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return CodeAIReobservationGatedGitLifecycleContinuationResult(
        STATUS_READY, (), evidence, next_registry, projected_state,
        delegated_receipt, receipt,
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIReobservationGatedGitLifecycleContinuationResult",
    "build_codeai_reobservation_gated_git_lifecycle_continuation",
    "canonical_digest",
]
