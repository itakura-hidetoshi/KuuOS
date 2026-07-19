#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping

from runtime.kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    PHASE_AWAIT_CHECKS,
    PHASE_COMPLETE,
    PHASE_CREATE_PR,
    PHASE_LOCAL_COMMIT,
    PHASE_MARK_PR_READY,
    PHASE_MERGE,
    PHASE_NONE,
    PHASE_PUSH,
    POLICY_DIGEST_FIELD as LIFECYCLE_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as LIFECYCLE_RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as LIFECYCLE_REQUEST_DIGEST_FIELD,
    SOURCE_RECEIPT_DIGEST_FIELD as TRAJECTORY_RECEIPT_DIGEST_FIELD,
    _source_supported as _trajectory_supported,
    _validate_source as _validate_trajectory_receipt,
    canonical_digest,
    digest_without,
)
from runtime.kuuos_codeai_autonomous_git_effect_execution_types_v0_1 import (
    DISPOSITION_COMPLETED as EXECUTION_COMPLETED,
    DISPOSITION_EVIDENCE_QUARANTINED as EXECUTION_QUARANTINED,
    DISPOSITION_FAILED as EXECUTION_FAILED,
    EVIDENCE_DIGEST_FIELD as EXECUTION_EVIDENCE_DIGEST_FIELD,
    POLICY_DIGEST_FIELD as EXECUTION_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as EXECUTION_RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as EXECUTION_REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as EXECUTION_REQUEST_DIGEST_FIELD,
    SUPPORTED_PHASES,
    GitEffectAdapter,
)
from runtime.kuuos_codeai_autonomous_git_effect_execution_validation_v0_1 import (
    _validate_registry as _validate_execution_registry,
    _validate_source as _validate_lifecycle_receipt,
)
from runtime.kuuos_codeai_autonomous_git_effect_execution_v0_1 import (
    build_codeai_autonomous_git_effect_execution,
)
from runtime.kuuos_codeai_autonomous_git_effect_reobservation_v0_1 import (
    DISPOSITION_COMPLETED as REOBSERVATION_COMPLETED,
    DISPOSITION_EVIDENCE_QUARANTINED as REOBSERVATION_QUARANTINED,
    DISPOSITION_FAILED as REOBSERVATION_FAILED,
    EVIDENCE_DIGEST_FIELD as REOBSERVATION_EVIDENCE_DIGEST_FIELD,
    POLICY_DIGEST_FIELD as REOBSERVATION_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as REOBSERVATION_RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as REOBSERVATION_REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as REOBSERVATION_REQUEST_DIGEST_FIELD,
    GitEffectReobservationAdapter,
    _validate_registry as _validate_reobservation_registry,
    build_codeai_autonomous_git_effect_reobservation,
)
from runtime.kuuos_codeai_reobservation_gated_git_lifecycle_continuation_v0_1 import (
    POLICY_DIGEST_FIELD as CONTINUATION_POLICY_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as CONTINUATION_RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as CONTINUATION_REGISTRY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD as CONTINUATION_REQUEST_DIGEST_FIELD,
    _validate_registry as _validate_continuation_registry,
    build_codeai_reobservation_gated_git_lifecycle_continuation,
)

VERSION = "kuuos_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Bounded Autonomous Git Lifecycle Loop Orchestration v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

DISPOSITION_COMPLETED = "bounded_autonomous_git_lifecycle_loop_completed"
DISPOSITION_TERMINAL_HOLD = "bounded_autonomous_git_lifecycle_loop_terminal_hold"
DISPOSITION_EFFECT_BUDGET_EXHAUSTED = "bounded_autonomous_git_lifecycle_effect_budget_exhausted"
DISPOSITION_EXECUTION_FAILED = "bounded_autonomous_git_lifecycle_execution_failed"
DISPOSITION_EXECUTION_QUARANTINED = "bounded_autonomous_git_lifecycle_execution_evidence_quarantined"
DISPOSITION_REOBSERVATION_FAILED = "bounded_autonomous_git_lifecycle_reobservation_failed"
DISPOSITION_REOBSERVATION_QUARANTINED = "bounded_autonomous_git_lifecycle_reobservation_evidence_quarantined"
DISPOSITION_STAGE_BLOCKED = "bounded_autonomous_git_lifecycle_stage_blocked"

REQUEST_DIGEST_FIELD = "codeai_bounded_autonomous_git_lifecycle_loop_request_digest"
POLICY_DIGEST_FIELD = "codeai_bounded_autonomous_git_lifecycle_loop_policy_digest"
REGISTRY_DIGEST_FIELD = "codeai_bounded_autonomous_git_lifecycle_loop_registry_digest"
EVIDENCE_DIGEST_FIELD = "codeai_bounded_autonomous_git_lifecycle_loop_evidence_digest"
RECEIPT_DIGEST_FIELD = "codeai_bounded_autonomous_git_lifecycle_loop_receipt_digest"

_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_BRANCH = re.compile(r"^(?!/)(?!.*(?:\.\.|//|@\{|\\|[~^:?*\[]))(?!.*\.$)[^\s]+$")

REQUEST_FIELDS = {
    "loop_id", "loop_revision", "loop_session_id", "loop_nonce_digest",
    "source_trajectory_receipt_digest", "initial_lifecycle_receipt_digest",
    "lifecycle_id", "executor_id", "observer_id", "repository_full_name",
    "source_commit_sha", "base_branch", "head_branch", "remote_name",
    "change_set_digest", "commit_message", "commit_message_digest", "merge_method",
    "pull_request_title", "pull_request_body", "pull_request_body_digest",
    "requested_max_effect_count", "prior_lifecycle_execution_session_ids",
    "prior_lifecycle_execution_nonce_digests", "prior_lifecycle_receipt_digests",
    "request_created_epoch", "provenance_integrity_confirmed",
    "source_correspondence_confirmed", REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_source_trajectory_receipt_digest", "expected_initial_lifecycle_receipt_digest",
    "expected_repository_full_name", "authorized_executor_ids", "authorized_observer_ids",
    "allowed_effect_phases", "allowed_base_branches", "allowed_head_branch_prefixes",
    "allowed_remote_names", "allowed_merge_methods", "required_check_names",
    "maximum_effect_count", "maximum_total_execution_command_count",
    "maximum_total_execution_output_bytes", "maximum_total_reobservation_command_count",
    "maximum_total_reobservation_output_bytes", "maximum_execution_command_count_per_effect",
    "maximum_execution_output_bytes_per_effect", "maximum_execution_timeout_seconds_per_effect",
    "maximum_reobservation_command_count_per_effect",
    "maximum_reobservation_output_bytes_per_effect", "maximum_request_age",
    "maximum_observation_age", "maximum_state_age", "maximum_registry_entries",
    "evaluation_epoch", "allow_local_commit", "allow_push",
    "allow_pull_request_creation", "allow_pull_request_readiness", "allow_merge",
    "allow_opaque_token_use", "allow_effect_execution", "allow_reobservation",
    "allow_continuation_evaluation", "allow_force_push",
    "allow_remote_branch_deletion", "allow_admin_merge_bypass", "allow_deployment",
    "allow_secret_material_read", "allow_networked_reobservation",
    "allow_human_handover", "allow_unbounded_continuation", POLICY_DIGEST_FIELD,
}

REGISTRY_FIELDS = {
    "registry_id", "registry_revision", "consumed_initial_lifecycle_receipt_digests",
    "consumed_loop_nonce_digests", "completed_loop_count", "total_effect_count",
    "last_loop_epoch", REGISTRY_DIGEST_FIELD,
}

_REQUEST_STRING_FIELDS = REQUEST_FIELDS - {
    "requested_max_effect_count", "prior_lifecycle_execution_session_ids",
    "prior_lifecycle_execution_nonce_digests", "prior_lifecycle_receipt_digests",
    "request_created_epoch", "provenance_integrity_confirmed",
    "source_correspondence_confirmed", REQUEST_DIGEST_FIELD,
}
_POLICY_LIST_FIELDS = {
    "authorized_executor_ids", "authorized_observer_ids", "allowed_effect_phases",
    "allowed_base_branches", "allowed_head_branch_prefixes", "allowed_remote_names",
    "allowed_merge_methods", "required_check_names",
}
_POLICY_NAT_FIELDS = {
    "maximum_effect_count", "maximum_total_execution_command_count",
    "maximum_total_execution_output_bytes", "maximum_total_reobservation_command_count",
    "maximum_total_reobservation_output_bytes", "maximum_execution_command_count_per_effect",
    "maximum_execution_output_bytes_per_effect", "maximum_execution_timeout_seconds_per_effect",
    "maximum_reobservation_command_count_per_effect",
    "maximum_reobservation_output_bytes_per_effect", "maximum_request_age",
    "maximum_observation_age", "maximum_state_age", "maximum_registry_entries",
    "evaluation_epoch",
}
_POLICY_STRING_FIELDS = {
    "expected_source_trajectory_receipt_digest", "expected_initial_lifecycle_receipt_digest",
    "expected_repository_full_name", POLICY_DIGEST_FIELD,
}


@dataclass(frozen=True)
class CodeAIBoundedAutonomousGitLifecycleLoopResult:
    status: str
    issues: tuple[str, ...]
    evidence: dict[str, Any] | None
    next_loop_registry: dict[str, Any] | None
    next_execution_registry: dict[str, Any] | None
    next_reobservation_registry: dict[str, Any] | None
    next_continuation_registry: dict[str, Any] | None
    final_lifecycle_receipt: dict[str, Any] | None
    final_lifecycle_state: dict[str, Any] | None
    receipt: dict[str, Any] | None


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _nat(value: Any, *, positive: bool = False) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    if positive and value == 0:
        return None
    return value


def _strings(value: Any, *, nonempty: bool = False) -> tuple[str, ...] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return None
    parsed = tuple(value)
    if len(parsed) != len(set(parsed)):
        return None
    if nonempty and (not parsed or not all(parsed)):
        return None
    return parsed


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
    return value.get(field) == digest_without(value, field)


def _text_digest(label: str, value: str) -> str:
    return canonical_digest({label: value})


def _derived_digest(loop_id: str, iteration: int, kind: str, phase: str) -> str:
    return canonical_digest({
        "loop_id": loop_id,
        "iteration": iteration,
        "kind": kind,
        "phase": phase,
    })


def _validate_request(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, REQUEST_FIELDS, "bounded_git_lifecycle_loop_request")
    if issues:
        return issues
    for field in _REQUEST_STRING_FIELDS:
        if not isinstance(value.get(field), str) or not value[field]:
            issues.append("bounded_git_lifecycle_loop_request_invalid_string:" + field)
    if _nat(value.get("requested_max_effect_count"), positive=True) is None:
        issues.append("bounded_git_lifecycle_loop_request_invalid_positive_nat:requested_max_effect_count")
    if _nat(value.get("request_created_epoch")) is None:
        issues.append("bounded_git_lifecycle_loop_request_invalid_nat:request_created_epoch")
    histories = (
        "prior_lifecycle_execution_session_ids",
        "prior_lifecycle_execution_nonce_digests",
        "prior_lifecycle_receipt_digests",
    )
    for field in histories:
        parsed = _strings(value.get(field), nonempty=True)
        if parsed is None:
            issues.append("bounded_git_lifecycle_loop_request_invalid_history:" + field)
        elif field != "prior_lifecycle_execution_session_ids" and not all(
            _SHA256.fullmatch(item) for item in parsed
        ):
            issues.append("bounded_git_lifecycle_loop_request_invalid_digest_history:" + field)
    for field in ("provenance_integrity_confirmed", "source_correspondence_confirmed"):
        if value.get(field) is not True:
            issues.append("bounded_git_lifecycle_loop_request_required_true:" + field)
    digest_fields = (
        "loop_nonce_digest", "source_trajectory_receipt_digest",
        "initial_lifecycle_receipt_digest", "change_set_digest",
        "commit_message_digest", "pull_request_body_digest",
    )
    for field in digest_fields:
        if not isinstance(value.get(field), str) or not _SHA256.fullmatch(value[field]):
            issues.append("bounded_git_lifecycle_loop_request_invalid_digest:" + field)
    if not _digest_ok(value, REQUEST_DIGEST_FIELD):
        issues.append("bounded_git_lifecycle_loop_request_digest_mismatch")
    return issues


def _validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, POLICY_FIELDS, "bounded_git_lifecycle_loop_policy")
    if issues:
        return issues
    for field in _POLICY_STRING_FIELDS:
        if not isinstance(value.get(field), str) or not value[field]:
            issues.append("bounded_git_lifecycle_loop_policy_invalid_string:" + field)
    for field in _POLICY_LIST_FIELDS:
        if _strings(value.get(field), nonempty=True) is None:
            issues.append("bounded_git_lifecycle_loop_policy_invalid_nonempty_unique_list:" + field)
    for field in _POLICY_NAT_FIELDS:
        if _nat(value.get(field), positive=field != "evaluation_epoch") is None:
            issues.append("bounded_git_lifecycle_loop_policy_invalid_nat:" + field)
    bool_fields = POLICY_FIELDS - _POLICY_STRING_FIELDS - _POLICY_LIST_FIELDS - _POLICY_NAT_FIELDS
    for field in bool_fields:
        if not isinstance(value.get(field), bool):
            issues.append("bounded_git_lifecycle_loop_policy_invalid_bool:" + field)
    if not _digest_ok(value, POLICY_DIGEST_FIELD):
        issues.append("bounded_git_lifecycle_loop_policy_digest_mismatch")
    return issues


def _validate_loop_registry(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, REGISTRY_FIELDS, "bounded_git_lifecycle_loop_registry")
    if issues:
        return issues
    if not isinstance(value.get("registry_id"), str) or not value["registry_id"]:
        issues.append("bounded_git_lifecycle_loop_registry_invalid_id")
    for field in (
        "registry_revision", "completed_loop_count", "total_effect_count", "last_loop_epoch"
    ):
        if _nat(value.get(field)) is None:
            issues.append("bounded_git_lifecycle_loop_registry_invalid_nat:" + field)
    histories = (
        "consumed_initial_lifecycle_receipt_digests", "consumed_loop_nonce_digests",
    )
    parsed: dict[str, tuple[str, ...] | None] = {}
    for field in histories:
        parsed[field] = _strings(value.get(field))
        if parsed[field] is None or not all(_SHA256.fullmatch(item) for item in parsed[field] or ()):
            issues.append("bounded_git_lifecycle_loop_registry_invalid_digest_history:" + field)
    if all(parsed[field] is not None for field in histories):
        if len(parsed[histories[0]] or ()) != len(parsed[histories[1]] or ()):
            issues.append("bounded_git_lifecycle_loop_registry_parallel_history_mismatch")
        if value.get("completed_loop_count") != len(parsed[histories[0]] or ()):
            issues.append("bounded_git_lifecycle_loop_registry_count_mismatch")
    if not _digest_ok(value, REGISTRY_DIGEST_FIELD):
        issues.append("bounded_git_lifecycle_loop_registry_digest_mismatch")
    return issues


def _correspondence_valid(
    source: Mapping[str, Any], lifecycle: Mapping[str, Any], request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> bool:
    return (
        source[TRAJECTORY_RECEIPT_DIGEST_FIELD]
        == lifecycle["source_trajectory_receipt_digest"]
        == request["source_trajectory_receipt_digest"]
        == policy["expected_source_trajectory_receipt_digest"]
        and lifecycle[LIFECYCLE_RECEIPT_DIGEST_FIELD]
        == request["initial_lifecycle_receipt_digest"]
        == policy["expected_initial_lifecycle_receipt_digest"]
        and request["repository_full_name"]
        == source["repository_full_name"]
        == lifecycle["repository_full_name"]
        == policy["expected_repository_full_name"]
        and request["source_commit_sha"] == source["source_commit_sha"] == lifecycle["source_commit_sha"]
        and request["lifecycle_id"] == lifecycle["lifecycle_id"]
        and request["executor_id"] == lifecycle["executor_id"]
        and request["base_branch"] == lifecycle["base_branch"]
        and request["head_branch"] == lifecycle["head_branch"]
        and request["remote_name"] == lifecycle["remote_name"]
        and request["change_set_digest"] == lifecycle["change_set_digest"]
        and request["commit_message_digest"] == lifecycle["commit_message_digest"]
        and request["merge_method"] == lifecycle["merge_method"]
        and request["executor_id"] in policy["authorized_executor_ids"]
        and request["observer_id"] in policy["authorized_observer_ids"]
        and request["base_branch"] in policy["allowed_base_branches"]
        and any(request["head_branch"].startswith(prefix) for prefix in policy["allowed_head_branch_prefixes"])
        and request["remote_name"] in policy["allowed_remote_names"]
        and request["merge_method"] in policy["allowed_merge_methods"]
        and bool(_REPOSITORY.fullmatch(request["repository_full_name"]))
        and bool(_SHA40.fullmatch(request["source_commit_sha"]))
        and bool(_BRANCH.fullmatch(request["base_branch"]))
        and bool(_BRANCH.fullmatch(request["head_branch"]))
        and request["base_branch"] != request["head_branch"]
        and _text_digest("commit_message", request["commit_message"])
        == request["commit_message_digest"]
        and _text_digest("pull_request_body", request["pull_request_body"])
        == request["pull_request_body_digest"]
        and request["provenance_integrity_confirmed"] is True
        and request["source_correspondence_confirmed"] is True
    )


def _policy_safe(request: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    return (
        request["requested_max_effect_count"] <= policy["maximum_effect_count"]
        and set(policy["allowed_effect_phases"]).issubset(set(SUPPORTED_PHASES))
        and policy["allow_effect_execution"] is True
        and policy["allow_reobservation"] is True
        and policy["allow_continuation_evaluation"] is True
        and policy["allow_force_push"] is False
        and policy["allow_remote_branch_deletion"] is False
        and policy["allow_admin_merge_bypass"] is False
        and policy["allow_deployment"] is False
        and policy["allow_secret_material_read"] is False
        and policy["allow_networked_reobservation"] is False
        and policy["allow_human_handover"] is False
        and policy["allow_unbounded_continuation"] is False
    )


def _fresh_and_replay_closed(
    lifecycle: Mapping[str, Any], request: Mapping[str, Any], policy: Mapping[str, Any],
    registry: Mapping[str, Any],
) -> bool:
    now = policy["evaluation_epoch"]
    return (
        request["request_created_epoch"] <= now
        and now - request["request_created_epoch"] <= policy["maximum_request_age"]
        and registry["last_loop_epoch"] <= now
        and registry["completed_loop_count"] < policy["maximum_registry_entries"]
        and lifecycle[LIFECYCLE_RECEIPT_DIGEST_FIELD]
        not in registry["consumed_initial_lifecycle_receipt_digests"]
        and request["loop_nonce_digest"] not in registry["consumed_loop_nonce_digests"]
        and lifecycle[LIFECYCLE_RECEIPT_DIGEST_FIELD] in request["prior_lifecycle_receipt_digests"]
        and lifecycle["execution_session_id"] in request["prior_lifecycle_execution_session_ids"]
        and request["loop_nonce_digest"] not in request["prior_lifecycle_execution_nonce_digests"]
    )


def _next_loop_registry(
    registry: Mapping[str, Any], lifecycle_digest: str, nonce: str, effect_count: int, epoch: int,
) -> dict[str, Any]:
    value = {
        "registry_id": registry["registry_id"],
        "registry_revision": registry["registry_revision"] + 1,
        "consumed_initial_lifecycle_receipt_digests": [
            *registry["consumed_initial_lifecycle_receipt_digests"], lifecycle_digest,
        ],
        "consumed_loop_nonce_digests": [*registry["consumed_loop_nonce_digests"], nonce],
        "completed_loop_count": registry["completed_loop_count"] + 1,
        "total_effect_count": registry["total_effect_count"] + effect_count,
        "last_loop_epoch": epoch,
    }
    value[REGISTRY_DIGEST_FIELD] = canonical_digest(value)
    return value


def _execution_request(
    current: Mapping[str, Any], request: Mapping[str, Any], policy: Mapping[str, Any],
    iteration: int,
) -> dict[str, Any]:
    phase = current["next_effect_phase"]
    empty = phase != PHASE_CREATE_PR
    body = "" if empty else request["pull_request_body"]
    value = {
        "execution_id": f"{request['loop_id']}-execution-{iteration}",
        "execution_revision": str(iteration),
        "execution_session_id": f"{request['loop_session_id']}-execution-{iteration}",
        "execution_nonce_digest": _derived_digest(request["loop_id"], iteration, "execution_nonce", phase),
        "source_lifecycle_receipt_digest": current[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "lifecycle_id": current["lifecycle_id"],
        "executor_id": current["executor_id"],
        "repository_full_name": current["repository_full_name"],
        "source_commit_sha": current["source_commit_sha"],
        "base_branch": current["base_branch"],
        "head_branch": current["head_branch"],
        "remote_name": current["remote_name"],
        "merge_method": current["merge_method"],
        "change_set_digest": current["change_set_digest"],
        "commit_message": request["commit_message"] if phase == PHASE_LOCAL_COMMIT else "",
        "commit_message_digest": current["commit_message_digest"],
        "pull_request_title": request["pull_request_title"] if phase == PHASE_CREATE_PR else "",
        "pull_request_body": body,
        "pull_request_body_digest": _text_digest("pull_request_body", body),
        "pull_request_draft": phase == PHASE_CREATE_PR,
        "pull_request_number": current["pull_request_number"] if phase in {PHASE_MARK_PR_READY, PHASE_MERGE} else 0,
        "expected_head_sha": (
            current["source_commit_sha"] if phase == PHASE_LOCAL_COMMIT
            else current["pushed_head_sha"] if phase == PHASE_CREATE_PR
            else current["local_commit_sha"]
        ),
        "requested_effect_phase": phase,
        "request_created_epoch": policy["evaluation_epoch"],
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
    }
    value[EXECUTION_REQUEST_DIGEST_FIELD] = canonical_digest(value)
    return value


def _execution_policy(
    current: Mapping[str, Any], policy: Mapping[str, Any], remaining_commands: int,
    remaining_output: int,
) -> dict[str, Any]:
    value = {
        "expected_source_lifecycle_receipt_digest": current[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "expected_repository_full_name": current["repository_full_name"],
        "authorized_executor_ids": list(policy["authorized_executor_ids"]),
        "allowed_effect_phases": [current["next_effect_phase"]],
        "allowed_base_branches": list(policy["allowed_base_branches"]),
        "allowed_head_branch_prefixes": list(policy["allowed_head_branch_prefixes"]),
        "allowed_remote_names": list(policy["allowed_remote_names"]),
        "allowed_merge_methods": list(policy["allowed_merge_methods"]),
        "allow_local_commit": policy["allow_local_commit"],
        "allow_push": policy["allow_push"],
        "allow_pull_request_creation": policy["allow_pull_request_creation"],
        "allow_pull_request_readiness": policy["allow_pull_request_readiness"],
        "allow_merge": policy["allow_merge"],
        "allow_force_push": False,
        "allow_remote_branch_deletion": False,
        "allow_admin_merge_bypass": False,
        "allow_deployment": False,
        "allow_secret_material_read": False,
        "allow_opaque_token_use": policy["allow_opaque_token_use"],
        "maximum_command_count": min(
            policy["maximum_execution_command_count_per_effect"], remaining_commands
        ),
        "maximum_output_bytes": min(
            policy["maximum_execution_output_bytes_per_effect"], remaining_output
        ),
        "maximum_timeout_seconds": policy["maximum_execution_timeout_seconds_per_effect"],
        "maximum_request_age": policy["maximum_request_age"],
        "maximum_registry_entries": policy["maximum_registry_entries"],
        "evaluation_epoch": policy["evaluation_epoch"],
    }
    value[EXECUTION_POLICY_DIGEST_FIELD] = canonical_digest(value)
    return value


def _reobservation_request(
    current: Mapping[str, Any], execution_receipt: Mapping[str, Any],
    execution_evidence: Mapping[str, Any], request: Mapping[str, Any],
    policy: Mapping[str, Any], iteration: int,
) -> dict[str, Any]:
    phase = current["next_effect_phase"]
    value = {
        "reobservation_id": f"{request['loop_id']}-reobservation-{iteration}",
        "reobservation_revision": str(iteration),
        "reobservation_session_id": f"{request['loop_session_id']}-reobservation-{iteration}",
        "reobservation_nonce_digest": _derived_digest(
            request["loop_id"], iteration, "reobservation_nonce", phase
        ),
        "source_lifecycle_receipt_digest": current[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "source_execution_receipt_digest": execution_receipt[EXECUTION_RECEIPT_DIGEST_FIELD],
        "source_execution_evidence_digest": execution_evidence[EXECUTION_EVIDENCE_DIGEST_FIELD],
        "lifecycle_id": current["lifecycle_id"],
        "observer_id": request["observer_id"],
        "repository_full_name": current["repository_full_name"],
        "source_commit_sha": current["source_commit_sha"],
        "base_branch": current["base_branch"],
        "head_branch": current["head_branch"],
        "remote_name": current["remote_name"],
        "change_set_digest": current["change_set_digest"],
        "commit_message_digest": current["commit_message_digest"],
        "merge_method": current["merge_method"],
        "effect_phase": phase,
        "request_created_epoch": policy["evaluation_epoch"],
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
    }
    value[REOBSERVATION_REQUEST_DIGEST_FIELD] = canonical_digest(value)
    return value


def _reobservation_policy(
    current: Mapping[str, Any], execution_receipt: Mapping[str, Any],
    execution_evidence: Mapping[str, Any], policy: Mapping[str, Any],
    remaining_commands: int, remaining_output: int,
) -> dict[str, Any]:
    value = {
        "expected_source_lifecycle_receipt_digest": current[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "expected_source_execution_receipt_digest": execution_receipt[EXECUTION_RECEIPT_DIGEST_FIELD],
        "expected_source_execution_evidence_digest": execution_evidence[EXECUTION_EVIDENCE_DIGEST_FIELD],
        "expected_repository_full_name": current["repository_full_name"],
        "authorized_observer_ids": list(policy["authorized_observer_ids"]),
        "allowed_effect_phases": [current["next_effect_phase"]],
        "required_check_names": list(policy["required_check_names"]),
        "maximum_command_count": min(
            policy["maximum_reobservation_command_count_per_effect"], remaining_commands
        ),
        "maximum_output_bytes": min(
            policy["maximum_reobservation_output_bytes_per_effect"], remaining_output
        ),
        "maximum_request_age": policy["maximum_request_age"],
        "maximum_observation_age": policy["maximum_observation_age"],
        "maximum_registry_entries": policy["maximum_registry_entries"],
        "evaluation_epoch": policy["evaluation_epoch"],
        "network_access_allowed": False,
        "secret_access_allowed": False,
        "git_write_allowed": False,
        "deployment_allowed": False,
    }
    value[REOBSERVATION_POLICY_DIGEST_FIELD] = canonical_digest(value)
    return value


def _lifecycle_request(
    source: Mapping[str, Any], current: Mapping[str, Any], state: Mapping[str, Any],
    request: Mapping[str, Any], policy: Mapping[str, Any], iteration: int,
    prior_sessions: list[str], prior_nonces: list[str], prior_receipts: list[str],
) -> dict[str, Any]:
    phase = current["next_effect_phase"]
    session = f"{request['loop_session_id']}-lifecycle-{iteration}"
    nonce = _derived_digest(request["loop_id"], iteration, "lifecycle_nonce", phase)
    value = {
        "lifecycle_id": current["lifecycle_id"],
        "lifecycle_revision": str(iteration),
        "execution_session_id": session,
        "execution_nonce_digest": nonce,
        "source_trajectory_receipt_digest": source[TRAJECTORY_RECEIPT_DIGEST_FIELD],
        "repository_full_name": current["repository_full_name"],
        "source_commit_sha": current["source_commit_sha"],
        "executor_id": current["executor_id"],
        "base_branch": current["base_branch"],
        "head_branch": current["head_branch"],
        "remote_name": current["remote_name"],
        "change_set_digest": current["change_set_digest"],
        "commit_message_digest": current["commit_message_digest"],
        "merge_method": current["merge_method"],
        "local_commit_requested": True,
        "push_requested": True,
        "pull_request_requested": True,
        "merge_requested": True,
        "force_push_requested": False,
        "remote_branch_delete_requested": False,
        "admin_merge_requested": False,
        "human_handover_requested": False,
        "request_created_epoch": policy["evaluation_epoch"],
        "prior_execution_session_ids": list(prior_sessions),
        "prior_execution_nonce_digests": list(prior_nonces),
        "prior_lifecycle_receipt_digests": list(prior_receipts),
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
    }
    value[LIFECYCLE_REQUEST_DIGEST_FIELD] = canonical_digest(value)
    return value


def _lifecycle_policy(
    source: Mapping[str, Any], current: Mapping[str, Any], policy: Mapping[str, Any]
) -> dict[str, Any]:
    value = {
        "expected_source_trajectory_receipt_digest": source[TRAJECTORY_RECEIPT_DIGEST_FIELD],
        "expected_repository_full_name": current["repository_full_name"],
        "expected_source_commit_sha": current["source_commit_sha"],
        "authorized_executor_ids": list(policy["authorized_executor_ids"]),
        "allowed_base_branches": list(policy["allowed_base_branches"]),
        "allowed_head_branch_prefixes": list(policy["allowed_head_branch_prefixes"]),
        "allowed_remote_names": list(policy["allowed_remote_names"]),
        "allowed_merge_methods": list(policy["allowed_merge_methods"]),
        "required_check_names": list(policy["required_check_names"]),
        "allow_local_commit": policy["allow_local_commit"],
        "allow_push": policy["allow_push"],
        "allow_pull_request_creation": policy["allow_pull_request_creation"],
        "allow_pull_request_readiness": policy["allow_pull_request_readiness"],
        "allow_merge": policy["allow_merge"],
        "allow_force_push": False,
        "allow_remote_branch_deletion": False,
        "allow_admin_merge_bypass": False,
        "require_non_draft_for_merge": True,
        "require_mergeable": True,
        "require_head_sha_pin": True,
        "require_no_unresolved_blockers": True,
        "explicit_automerge_license": True,
        "evaluation_epoch": policy["evaluation_epoch"],
        "maximum_request_age": policy["maximum_request_age"],
        "maximum_state_age": policy["maximum_state_age"],
    }
    value[LIFECYCLE_POLICY_DIGEST_FIELD] = canonical_digest(value)
    return value


def _continuation_request(
    source: Mapping[str, Any], current: Mapping[str, Any],
    reobs: Mapping[str, Any], reobs_evidence: Mapping[str, Any],
    state: Mapping[str, Any], lifecycle_request: Mapping[str, Any],
    lifecycle_policy: Mapping[str, Any], request: Mapping[str, Any],
    policy: Mapping[str, Any], iteration: int,
) -> dict[str, Any]:
    value = {
        "continuation_id": f"{request['loop_id']}-continuation-{iteration}",
        "continuation_revision": str(iteration),
        "continuation_session_id": f"{request['loop_session_id']}-continuation-{iteration}",
        "continuation_nonce_digest": _derived_digest(
            request["loop_id"], iteration, "continuation_nonce", current["next_effect_phase"]
        ),
        "source_reobservation_receipt_digest": reobs[REOBSERVATION_RECEIPT_DIGEST_FIELD],
        "source_reobservation_evidence_digest": reobs_evidence[REOBSERVATION_EVIDENCE_DIGEST_FIELD],
        "source_lifecycle_receipt_digest": current[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "source_lifecycle_state_digest": state["codeai_autonomous_git_lifecycle_state_digest"],
        "source_trajectory_receipt_digest": source[TRAJECTORY_RECEIPT_DIGEST_FIELD],
        "delegated_lifecycle_request_digest": lifecycle_request[LIFECYCLE_REQUEST_DIGEST_FIELD],
        "delegated_lifecycle_policy_digest": lifecycle_policy[LIFECYCLE_POLICY_DIGEST_FIELD],
        "lifecycle_id": current["lifecycle_id"],
        "executor_id": current["executor_id"],
        "repository_full_name": current["repository_full_name"],
        "request_created_epoch": policy["evaluation_epoch"],
        "provenance_integrity_confirmed": True,
        "source_correspondence_confirmed": True,
    }
    value[CONTINUATION_REQUEST_DIGEST_FIELD] = canonical_digest(value)
    return value


def _continuation_policy(
    source: Mapping[str, Any], current: Mapping[str, Any],
    reobs: Mapping[str, Any], reobs_evidence: Mapping[str, Any],
    state: Mapping[str, Any], policy: Mapping[str, Any],
) -> dict[str, Any]:
    value = {
        "expected_source_reobservation_receipt_digest": reobs[REOBSERVATION_RECEIPT_DIGEST_FIELD],
        "expected_source_reobservation_evidence_digest": reobs_evidence[REOBSERVATION_EVIDENCE_DIGEST_FIELD],
        "expected_source_lifecycle_receipt_digest": current[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "expected_source_lifecycle_state_digest": state["codeai_autonomous_git_lifecycle_state_digest"],
        "expected_source_trajectory_receipt_digest": source[TRAJECTORY_RECEIPT_DIGEST_FIELD],
        "expected_repository_full_name": current["repository_full_name"],
        "authorized_executor_ids": list(policy["authorized_executor_ids"]),
        "maximum_request_age": policy["maximum_request_age"],
        "maximum_state_age": policy["maximum_state_age"],
        "maximum_registry_entries": policy["maximum_registry_entries"],
        "evaluation_epoch": policy["evaluation_epoch"],
        "allow_lifecycle_evaluation": True,
        "allow_state_projection": True,
        "allow_automatic_effect_execution": False,
    }
    value[CONTINUATION_POLICY_DIGEST_FIELD] = canonical_digest(value)
    return value

def _terminal_disposition(current: Mapping[str, Any]) -> str:
    if current.get("next_effect_phase") == PHASE_COMPLETE or current.get("codeai_disposition") == "autonomous_git_lifecycle_completed":
        return DISPOSITION_COMPLETED
    return DISPOSITION_TERMINAL_HOLD


def build_codeai_bounded_autonomous_git_lifecycle_loop_orchestration(
    *,
    source_trajectory_receipt: Any,
    initial_lifecycle_receipt: Any,
    loop_request: Any,
    loop_policy: Any,
    loop_registry: Any,
    execution_registry: Any,
    reobservation_registry: Any,
    continuation_registry: Any,
    execution_adapter: GitEffectAdapter,
    reobservation_adapter: GitEffectReobservationAdapter,
) -> CodeAIBoundedAutonomousGitLifecycleLoopResult:
    source = _mapping(source_trajectory_receipt)
    lifecycle = _mapping(initial_lifecycle_receipt)
    request = _mapping(loop_request)
    policy = _mapping(loop_policy)
    loop_reg = _mapping(loop_registry)
    execution_reg = _mapping(execution_registry)
    reobservation_reg = _mapping(reobservation_registry)
    continuation_reg = _mapping(continuation_registry)
    issues: list[str] = []
    if source is None:
        issues.append("source_trajectory_receipt_not_mapping")
    else:
        issues.extend(_validate_trajectory_receipt(source))
    if lifecycle is None:
        issues.append("initial_lifecycle_receipt_not_mapping")
    else:
        issues.extend(_validate_lifecycle_receipt(lifecycle))
    if request is None:
        issues.append("bounded_git_lifecycle_loop_request_not_mapping")
    else:
        issues.extend(_validate_request(request))
    if policy is None:
        issues.append("bounded_git_lifecycle_loop_policy_not_mapping")
    else:
        issues.extend(_validate_policy(policy))
    if loop_reg is None:
        issues.append("bounded_git_lifecycle_loop_registry_not_mapping")
    else:
        issues.extend(_validate_loop_registry(loop_reg))
    if execution_reg is None:
        issues.append("execution_registry_not_mapping")
    else:
        issues.extend(_validate_execution_registry(execution_reg))
    if reobservation_reg is None:
        issues.append("reobservation_registry_not_mapping")
    else:
        issues.extend(_validate_reobservation_registry(reobservation_reg))
    if continuation_reg is None:
        issues.append("continuation_registry_not_mapping")
    else:
        issues.extend(_validate_continuation_registry(continuation_reg))
    if issues or None in (
        source, lifecycle, request, policy, loop_reg, execution_reg,
        reobservation_reg, continuation_reg,
    ):
        return CodeAIBoundedAutonomousGitLifecycleLoopResult(
            STATUS_BLOCKED, tuple(issues), None, None, None, None, None, None, None, None,
        )
    assert source is not None and lifecycle is not None and request is not None and policy is not None
    assert loop_reg is not None and execution_reg is not None and reobservation_reg is not None
    assert continuation_reg is not None
    if not _trajectory_supported(source):
        issues.append("source_trajectory_receipt_not_supported")
    if not _correspondence_valid(source, lifecycle, request, policy):
        issues.append("bounded_git_lifecycle_loop_correspondence_mismatch")
    if not _policy_safe(request, policy):
        issues.append("bounded_git_lifecycle_loop_policy_not_safe")
    if not _fresh_and_replay_closed(lifecycle, request, policy, loop_reg):
        issues.append("bounded_git_lifecycle_loop_freshness_or_replay_violation")
    if issues:
        return CodeAIBoundedAutonomousGitLifecycleLoopResult(
            STATUS_BLOCKED, tuple(issues), None, None, None, None, None, None, None, None,
        )

    current = dict(lifecycle)
    final_state: dict[str, Any] | None = None
    execution_commands = 0
    execution_output = 0
    reobservation_commands = 0
    reobservation_output = 0
    effect_count = 0
    records: list[dict[str, Any]] = []
    disposition = _terminal_disposition(current) if not current["execution_lease_issued"] else ""
    stage_issues: list[str] = []

    prior_sessions = list(request["prior_lifecycle_execution_session_ids"])
    prior_nonces = list(request["prior_lifecycle_execution_nonce_digests"])
    prior_receipts = list(request["prior_lifecycle_receipt_digests"])

    for iteration in range(1, request["requested_max_effect_count"] + 1):
        if not current["execution_lease_issued"]:
            disposition = _terminal_disposition(current)
            break
        phase = current["next_effect_phase"]
        if phase not in policy["allowed_effect_phases"]:
            disposition = DISPOSITION_STAGE_BLOCKED
            stage_issues.append("current_effect_phase_not_allowed:" + str(phase))
            break
        remaining_exec_commands = policy["maximum_total_execution_command_count"] - execution_commands
        remaining_exec_output = policy["maximum_total_execution_output_bytes"] - execution_output
        remaining_reobs_commands = policy["maximum_total_reobservation_command_count"] - reobservation_commands
        remaining_reobs_output = policy["maximum_total_reobservation_output_bytes"] - reobservation_output
        if min(
            remaining_exec_commands, remaining_exec_output,
            remaining_reobs_commands, remaining_reobs_output,
        ) <= 0:
            disposition = DISPOSITION_EFFECT_BUDGET_EXHAUSTED
            break

        execution_request = _execution_request(current, request, policy, iteration)
        execution_policy = _execution_policy(
            current, policy, remaining_exec_commands, remaining_exec_output
        )
        execution_result = build_codeai_autonomous_git_effect_execution(
            source_lifecycle_receipt=current,
            execution_request=execution_request,
            execution_policy=execution_policy,
            execution_registry=execution_reg,
            adapter=execution_adapter,
        )
        if execution_result.status != STATUS_READY or execution_result.receipt is None or execution_result.evidence is None or execution_result.next_registry is None:
            disposition = DISPOSITION_STAGE_BLOCKED
            stage_issues.extend("execution:" + item for item in execution_result.issues)
            break
        execution_reg = execution_result.next_registry
        execution_receipt = execution_result.receipt
        execution_evidence = execution_result.evidence
        execution_adapter_result = execution_evidence["adapter_result"]
        execution_commands += execution_adapter_result["command_count"]
        execution_output += len(execution_adapter_result["stdout"].encode()) + len(
            execution_adapter_result["stderr"].encode()
        )

        reobservation_request = _reobservation_request(
            current, execution_receipt, execution_evidence, request, policy, iteration
        )
        reobservation_policy = _reobservation_policy(
            current, execution_receipt, execution_evidence, policy,
            policy["maximum_total_reobservation_command_count"] - reobservation_commands,
            policy["maximum_total_reobservation_output_bytes"] - reobservation_output,
        )
        reobservation_result = build_codeai_autonomous_git_effect_reobservation(
            source_lifecycle_receipt=current,
            source_execution_receipt=execution_receipt,
            source_execution_evidence=execution_evidence,
            reobservation_request=reobservation_request,
            reobservation_policy=reobservation_policy,
            reobservation_registry=reobservation_reg,
            adapter=reobservation_adapter,
        )
        if reobservation_result.status != STATUS_READY or reobservation_result.receipt is None or reobservation_result.evidence is None or reobservation_result.next_registry is None:
            disposition = DISPOSITION_STAGE_BLOCKED
            stage_issues.extend("reobservation:" + item for item in reobservation_result.issues)
            break
        reobservation_reg = reobservation_result.next_registry
        reobservation_receipt = reobservation_result.receipt
        reobservation_evidence = reobservation_result.evidence
        reobservation_adapter_result = reobservation_evidence["adapter_result"]
        reobservation_commands += reobservation_adapter_result["command_count"]
        reobservation_output += reobservation_adapter_result["output_bytes"]

        record: dict[str, Any] = {
            "iteration": iteration,
            "effect_phase": phase,
            "source_lifecycle_receipt_digest": current[LIFECYCLE_RECEIPT_DIGEST_FIELD],
            "execution_request_digest": execution_request[EXECUTION_REQUEST_DIGEST_FIELD],
            "execution_policy_digest": execution_policy[EXECUTION_POLICY_DIGEST_FIELD],
            "execution_receipt_digest": execution_receipt[EXECUTION_RECEIPT_DIGEST_FIELD],
            "execution_evidence_digest": execution_evidence[EXECUTION_EVIDENCE_DIGEST_FIELD],
            "execution_disposition": execution_receipt["codeai_disposition"],
            "execution_effect_completion_confirmed": execution_receipt["effect_completion_confirmed"],
            "reobservation_request_digest": reobservation_request[REOBSERVATION_REQUEST_DIGEST_FIELD],
            "reobservation_policy_digest": reobservation_policy[REOBSERVATION_POLICY_DIGEST_FIELD],
            "reobservation_receipt_digest": reobservation_receipt[REOBSERVATION_RECEIPT_DIGEST_FIELD],
            "reobservation_evidence_digest": reobservation_evidence[REOBSERVATION_EVIDENCE_DIGEST_FIELD],
            "reobservation_disposition": reobservation_receipt["codeai_disposition"],
            "fresh_lifecycle_state_issued": reobservation_receipt["fresh_lifecycle_state_issued"],
            "continuation_receipt_digest": "",
            "delegated_lifecycle_receipt_digest": "",
            "delegated_disposition": "",
            "delegated_next_effect_phase": "",
            "delegated_execution_lease_issued": False,
        }

        if reobservation_receipt["codeai_disposition"] != REOBSERVATION_COMPLETED or reobservation_result.lifecycle_state is None:
            records.append(record)
            if reobservation_receipt["codeai_disposition"] == REOBSERVATION_FAILED:
                disposition = DISPOSITION_REOBSERVATION_FAILED
            else:
                disposition = DISPOSITION_REOBSERVATION_QUARANTINED
            break

        final_state = reobservation_result.lifecycle_state
        lifecycle_request = _lifecycle_request(
            source, current, final_state, request, policy, iteration,
            prior_sessions, prior_nonces, prior_receipts,
        )
        lifecycle_policy = _lifecycle_policy(source, current, policy)
        continuation_request = _continuation_request(
            source, current, reobservation_receipt, reobservation_evidence,
            final_state, lifecycle_request, lifecycle_policy, request, policy, iteration,
        )
        continuation_policy = _continuation_policy(
            source, current, reobservation_receipt, reobservation_evidence,
            final_state, policy,
        )
        continuation_result = build_codeai_reobservation_gated_git_lifecycle_continuation(
            source_trajectory_receipt=source,
            source_reobservation_receipt=reobservation_receipt,
            source_reobservation_evidence=reobservation_evidence,
            source_lifecycle_state=final_state,
            continuation_request=continuation_request,
            continuation_policy=continuation_policy,
            continuation_registry=continuation_reg,
            delegated_lifecycle_request=lifecycle_request,
            delegated_lifecycle_policy=lifecycle_policy,
        )
        if continuation_result.status != STATUS_READY or continuation_result.receipt is None or continuation_result.delegated_lifecycle_receipt is None or continuation_result.next_registry is None:
            records.append(record)
            disposition = DISPOSITION_STAGE_BLOCKED
            stage_issues.extend("continuation:" + item for item in continuation_result.issues)
            break
        continuation_reg = continuation_result.next_registry
        continuation_receipt = continuation_result.receipt
        delegated = continuation_result.delegated_lifecycle_receipt
        record.update({
            "continuation_receipt_digest": continuation_receipt[CONTINUATION_RECEIPT_DIGEST_FIELD],
            "delegated_lifecycle_receipt_digest": delegated[LIFECYCLE_RECEIPT_DIGEST_FIELD],
            "delegated_disposition": delegated["codeai_disposition"],
            "delegated_next_effect_phase": delegated["next_effect_phase"],
            "delegated_execution_lease_issued": delegated["execution_lease_issued"],
        })
        records.append(record)
        effect_count += 1

        prior_sessions.append(lifecycle_request["execution_session_id"])
        prior_nonces.append(lifecycle_request["execution_nonce_digest"])
        prior_receipts.append(delegated[LIFECYCLE_RECEIPT_DIGEST_FIELD])
        current = delegated

        if execution_receipt["codeai_disposition"] != EXECUTION_COMPLETED:
            disposition = (
                DISPOSITION_EXECUTION_FAILED
                if execution_receipt["codeai_disposition"] == EXECUTION_FAILED
                else DISPOSITION_EXECUTION_QUARANTINED
            )
            break
        if not current["execution_lease_issued"]:
            disposition = _terminal_disposition(current)
            break
    else:
        disposition = (
            _terminal_disposition(current)
            if not current["execution_lease_issued"]
            else DISPOSITION_EFFECT_BUDGET_EXHAUSTED
        )

    next_loop_reg = _next_loop_registry(
        loop_reg, lifecycle[LIFECYCLE_RECEIPT_DIGEST_FIELD], request["loop_nonce_digest"],
        effect_count, policy["evaluation_epoch"],
    )
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_trajectory_receipt_digest": source[TRAJECTORY_RECEIPT_DIGEST_FIELD],
        "initial_lifecycle_receipt_digest": lifecycle[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "loop_request_digest": request[REQUEST_DIGEST_FIELD],
        "loop_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_loop_registry_digest": loop_reg[REGISTRY_DIGEST_FIELD],
        "next_loop_registry_digest": next_loop_reg[REGISTRY_DIGEST_FIELD],
        "iteration_records": records,
        "effect_count": effect_count,
        "execution_command_count": execution_commands,
        "execution_output_bytes": execution_output,
        "reobservation_command_count": reobservation_commands,
        "reobservation_output_bytes": reobservation_output,
        "final_lifecycle_receipt_digest": current[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "final_lifecycle_state_digest": (
            final_state["codeai_autonomous_git_lifecycle_state_digest"] if final_state else ""
        ),
        "final_lifecycle_disposition": current["codeai_disposition"],
        "final_next_effect_phase": current["next_effect_phase"],
        "final_execution_lease_issued": current["execution_lease_issued"],
        "stage_issues": stage_issues,
    }
    evidence[EVIDENCE_DIGEST_FIELD] = canonical_digest(evidence)

    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_trajectory_receipt_digest": source[TRAJECTORY_RECEIPT_DIGEST_FIELD],
        "initial_lifecycle_receipt_digest": lifecycle[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "loop_request_digest": request[REQUEST_DIGEST_FIELD],
        "loop_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_loop_registry_digest": loop_reg[REGISTRY_DIGEST_FIELD],
        "next_loop_registry_digest": next_loop_reg[REGISTRY_DIGEST_FIELD],
        "next_execution_registry_digest": execution_reg[EXECUTION_REGISTRY_DIGEST_FIELD],
        "next_reobservation_registry_digest": reobservation_reg[REOBSERVATION_REGISTRY_DIGEST_FIELD],
        "next_continuation_registry_digest": continuation_reg[CONTINUATION_REGISTRY_DIGEST_FIELD],
        "loop_evidence_digest": evidence[EVIDENCE_DIGEST_FIELD],
        "final_lifecycle_receipt_digest": current[LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "final_lifecycle_state_digest": (
            final_state["codeai_autonomous_git_lifecycle_state_digest"] if final_state else ""
        ),
        "loop_id": request["loop_id"],
        "loop_session_id": request["loop_session_id"],
        "lifecycle_id": request["lifecycle_id"],
        "repository_full_name": request["repository_full_name"],
        "codeai_disposition": disposition,
        "operating_mode": "bounded_synchronous_autonomous_git_lifecycle_loop",
        "route_receipt_recorded": True,
        "source_trajectory_receipt_verified": True,
        "initial_lifecycle_receipt_verified": True,
        "initial_lifecycle_receipt_consumed": True,
        "loop_nonce_consumed": True,
        "loop_registry_advanced_once": True,
        "effect_count": effect_count,
        "maximum_effect_count": request["requested_max_effect_count"],
        "effect_budget_exhausted": disposition == DISPOSITION_EFFECT_BUDGET_EXHAUSTED,
        "execution_command_count": execution_commands,
        "execution_output_bytes": execution_output,
        "reobservation_command_count": reobservation_commands,
        "reobservation_output_bytes": reobservation_output,
        "final_lifecycle_completed": disposition == DISPOSITION_COMPLETED,
        "final_execution_lease_issued": current["execution_lease_issued"],
        "automatic_unbounded_continuation_performed": False,
        "concurrent_effect_leases_executed": False,
        "force_push_performed": False,
        "remote_branch_deleted": False,
        "admin_merge_bypass_used": False,
        "deployment_performed": False,
        "secret_material_read": False,
        "human_handover_performed": False,
        "general_git_authority_granted": False,
        "general_successor_stage_authority_granted": False,
        "checks_treated_as_correctness": False,
        "merge_treated_as_truth": False,
        "history_read_only": False,
        "future_only": current["execution_lease_issued"],
        "active_now": False,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return CodeAIBoundedAutonomousGitLifecycleLoopResult(
        STATUS_READY, tuple(stage_issues), evidence, next_loop_reg, dict(execution_reg),
        dict(reobservation_reg), dict(continuation_reg), dict(current),
        dict(final_state) if final_state is not None else None, receipt,
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIBoundedAutonomousGitLifecycleLoopResult",
    "build_codeai_bounded_autonomous_git_lifecycle_loop_orchestration",
    "canonical_digest",
    "digest_without",
]
