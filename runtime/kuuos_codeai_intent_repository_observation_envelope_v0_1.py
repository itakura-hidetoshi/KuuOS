#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_codeai_intent_repository_observation_envelope_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

MODE_READ_ONLY = "read_only"
MODE_HOLD = "hold"
MODE_DEGRADED_READ_ONLY = "degraded_read_only"
MODE_ABSTAIN = "abstain"
MODE_HANDOVER = "handover"
MODE_REJECTED = "rejected"

DISPOSITION_SUPPORTED = "intent_repository_observation_supported"
DISPOSITION_INTENT_PROVENANCE_REPAIR = "intent_provenance_repair_required"
DISPOSITION_REPOSITORY_IDENTITY_REPAIR = "repository_identity_repair_required"
DISPOSITION_REPOSITORY_SNAPSHOT_REPAIR = "repository_snapshot_repair_required"
DISPOSITION_PATH_ACCOUNTING_REPAIR = "path_accounting_repair_required"
DISPOSITION_BASELINE_EVIDENCE_REPAIR = "baseline_evidence_repair_required"
DISPOSITION_OBSERVATION_WINDOW_REPAIR = "observation_window_repair_required"
DISPOSITION_REPLAY_REJECTED = "observation_replay_conflict_rejected"
DISPOSITION_REPOSITORY_MUTATION_REJECTED = "repository_mutation_rejected"
DISPOSITION_AUTHORITY_ESCALATION_REJECTED = "authority_escalation_rejected"
DISPOSITION_INTENT_CLARIFICATION_HOLD = "intent_clarification_hold"
DISPOSITION_UNSUPPORTED_TOOLCHAIN_ABSTAINED = "unsupported_toolchain_abstained"
DISPOSITION_OWNERSHIP_HANDOVER = "ownership_handover_required"
DISPOSITION_PARTIAL_OBSERVATION_DEGRADED = "partial_observation_degraded"

INTENT_DIGEST_FIELD = "codeai_intent_packet_digest"
REPOSITORY_OBSERVATION_DIGEST_FIELD = "codeai_repository_observation_digest"
POLICY_DIGEST_FIELD = "codeai_observation_policy_digest"
RECEIPT_DIGEST_FIELD = "codeai_intent_repository_observation_receipt_digest"

INTENT_FIELDS = {
    "intent_id",
    "source_actor_id",
    "source_channel",
    "intent_revision",
    "requirements",
    "assumptions",
    "unresolved_questions",
    "preserved_invariants",
    "forbidden_changes",
    "success_criteria",
    "authority_owner_id",
    "intent_created_epoch",
    "prior_intent_digests",
    "intent_provenance_confirmed",
    INTENT_DIGEST_FIELD,
}

REPOSITORY_OBSERVATION_FIELDS = {
    "repository_full_name",
    "source_commit_sha",
    "source_branch",
    "tree_digest",
    "dependency_lock_digest",
    "toolchain_digest",
    "toolchain_supported",
    "observed_paths",
    "unavailable_paths",
    "declared_path_count",
    "baseline_check_digests",
    "baseline_checks_complete",
    "code_owner_scope_digest",
    "crosses_unowned_boundary",
    "observation_started_epoch",
    "observation_completed_epoch",
    "session_id",
    "nonce_digest",
    "prior_session_ids",
    "prior_nonce_digests",
    "prior_observation_digests",
    "observation_collected_by_kernel",
    "repository_files_changed_by_kernel",
    "git_ref_changed_by_kernel",
    "branch_created_by_kernel",
    "commit_created_by_kernel",
    "push_performed_by_kernel",
    "pull_request_created_by_kernel",
    "external_side_effect_performed_by_kernel",
    "selection_authority_claimed",
    "execution_authority_claimed",
    "merge_authority_claimed",
    "deployment_authority_claimed",
    "secret_access_authority_claimed",
    REPOSITORY_OBSERVATION_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_repository_full_name",
    "expected_source_commit_sha",
    "allowed_source_branches",
    "supported_toolchain_digests",
    "maximum_observed_paths",
    "maximum_observation_duration",
    "require_complete_baseline",
    "require_code_owner_scope",
    "allow_partial_observation",
    POLICY_DIGEST_FIELD,
}

_MUTATION_FIELDS = (
    "repository_files_changed_by_kernel",
    "git_ref_changed_by_kernel",
    "branch_created_by_kernel",
    "commit_created_by_kernel",
    "push_performed_by_kernel",
    "pull_request_created_by_kernel",
    "external_side_effect_performed_by_kernel",
)

_AUTHORITY_FIELDS = (
    "selection_authority_claimed",
    "execution_authority_claimed",
    "merge_authority_claimed",
    "deployment_authority_claimed",
    "secret_access_authority_claimed",
)

_SHA40 = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True)
class CodeAIObservationResult:
    status: str
    issues: tuple[str, ...]
    receipt: dict[str, Any] | None


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return canonical_digest({key: item for key, item in value.items() if key != field})


def seal(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    result[field] = canonical_digest(result)
    return result


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _nat(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _positive_nat(value: Any) -> int | None:
    parsed = _nat(value)
    return parsed if parsed is not None and parsed > 0 else None


def _strings(value: Any) -> tuple[str, ...] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return None
    return tuple(value)


def _exact_fields(value: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = fields.difference(value)
    extra = set(value).difference(fields)
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues


def _validate_intent_packet(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, INTENT_FIELDS, "intent_packet")
    if issues:
        return issues
    for field in (
        "intent_id",
        "source_actor_id",
        "source_channel",
        "intent_revision",
        "authority_owner_id",
        INTENT_DIGEST_FIELD,
    ):
        if not isinstance(value.get(field), str):
            issues.append("intent_packet_invalid_string:" + field)
    for field in (
        "requirements",
        "assumptions",
        "unresolved_questions",
        "preserved_invariants",
        "forbidden_changes",
        "success_criteria",
        "prior_intent_digests",
    ):
        if _strings(value.get(field)) is None:
            issues.append("intent_packet_invalid_string_list:" + field)
    if _nat(value.get("intent_created_epoch")) is None:
        issues.append("intent_packet_invalid_epoch")
    if not isinstance(value.get("intent_provenance_confirmed"), bool):
        issues.append("intent_packet_invalid_provenance_flag")
    if value.get(INTENT_DIGEST_FIELD) != digest_without(value, INTENT_DIGEST_FIELD):
        issues.append("intent_packet_digest_mismatch")
    return issues


def _validate_repository_observation(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(
        value, REPOSITORY_OBSERVATION_FIELDS, "repository_observation"
    )
    if issues:
        return issues
    for field in (
        "repository_full_name",
        "source_commit_sha",
        "source_branch",
        "tree_digest",
        "dependency_lock_digest",
        "toolchain_digest",
        "code_owner_scope_digest",
        "session_id",
        "nonce_digest",
        REPOSITORY_OBSERVATION_DIGEST_FIELD,
    ):
        if not isinstance(value.get(field), str):
            issues.append("repository_observation_invalid_string:" + field)
    for field in (
        "observed_paths",
        "unavailable_paths",
        "baseline_check_digests",
        "prior_session_ids",
        "prior_nonce_digests",
        "prior_observation_digests",
    ):
        if _strings(value.get(field)) is None:
            issues.append("repository_observation_invalid_string_list:" + field)
    for field in (
        "declared_path_count",
        "observation_started_epoch",
        "observation_completed_epoch",
    ):
        if _nat(value.get(field)) is None:
            issues.append("repository_observation_invalid_nat:" + field)
    for field in (
        "toolchain_supported",
        "baseline_checks_complete",
        "crosses_unowned_boundary",
        "observation_collected_by_kernel",
        *_MUTATION_FIELDS,
        *_AUTHORITY_FIELDS,
    ):
        if not isinstance(value.get(field), bool):
            issues.append("repository_observation_invalid_bool:" + field)
    if value.get(REPOSITORY_OBSERVATION_DIGEST_FIELD) != digest_without(
        value, REPOSITORY_OBSERVATION_DIGEST_FIELD
    ):
        issues.append("repository_observation_digest_mismatch")
    return issues


def _validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, POLICY_FIELDS, "observation_policy")
    if issues:
        return issues
    for field in (
        "expected_repository_full_name",
        "expected_source_commit_sha",
        POLICY_DIGEST_FIELD,
    ):
        if not isinstance(value.get(field), str):
            issues.append("observation_policy_invalid_string:" + field)
    for field in ("allowed_source_branches", "supported_toolchain_digests"):
        if _strings(value.get(field)) is None:
            issues.append("observation_policy_invalid_string_list:" + field)
    for field in ("maximum_observed_paths", "maximum_observation_duration"):
        if _positive_nat(value.get(field)) is None:
            issues.append("observation_policy_invalid_positive_nat:" + field)
    for field in (
        "require_complete_baseline",
        "require_code_owner_scope",
        "allow_partial_observation",
    ):
        if not isinstance(value.get(field), bool):
            issues.append("observation_policy_invalid_bool:" + field)
    if value.get(POLICY_DIGEST_FIELD) != digest_without(value, POLICY_DIGEST_FIELD):
        issues.append("observation_policy_digest_mismatch")
    return issues


def _preflight(
    intent_packet: Any,
    repository_observation: Any,
    observation_policy: Any,
) -> tuple[Mapping[str, Any] | None, Mapping[str, Any] | None, Mapping[str, Any] | None, tuple[str, ...]]:
    intent = _mapping(intent_packet)
    repository = _mapping(repository_observation)
    policy = _mapping(observation_policy)
    issues: list[str] = []
    if intent is None:
        issues.append("intent_packet_not_mapping")
    else:
        issues.extend(_validate_intent_packet(intent))
    if repository is None:
        issues.append("repository_observation_not_mapping")
    else:
        issues.extend(_validate_repository_observation(repository))
    if policy is None:
        issues.append("observation_policy_not_mapping")
    else:
        issues.extend(_validate_policy(policy))
    return intent, repository, policy, tuple(issues)


def _nonempty_unique_strings(value: Any) -> bool:
    parsed = _strings(value)
    return parsed is not None and all(parsed) and len(parsed) == len(set(parsed))


def _intent_provenance_valid(intent: Mapping[str, Any]) -> bool:
    return (
        intent["intent_provenance_confirmed"] is True
        and bool(intent["intent_id"])
        and bool(intent["source_actor_id"])
        and bool(intent["source_channel"])
        and bool(intent["intent_revision"])
        and bool(intent["authority_owner_id"])
        and _nonempty_unique_strings(intent["requirements"])
        and _nonempty_unique_strings(intent["preserved_invariants"])
        and _nonempty_unique_strings(intent["success_criteria"])
        and _nonempty_unique_strings(intent["forbidden_changes"])
        and _strings(intent["assumptions"]) is not None
        and _strings(intent["unresolved_questions"]) is not None
        and _strings(intent["prior_intent_digests"]) is not None
    )


def _repository_identity_valid(
    repository: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    return (
        repository["repository_full_name"] == policy["expected_repository_full_name"]
        and repository["source_commit_sha"] == policy["expected_source_commit_sha"]
        and bool(_SHA40.fullmatch(repository["source_commit_sha"]))
        and repository["source_branch"] in policy["allowed_source_branches"]
        and _nonempty_unique_strings(policy["allowed_source_branches"])
    )


def _snapshot_valid(
    repository: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    observed = _strings(repository["observed_paths"])
    unavailable = _strings(repository["unavailable_paths"])
    baseline = _strings(repository["baseline_check_digests"])
    return (
        bool(repository["tree_digest"])
        and bool(repository["dependency_lock_digest"])
        and bool(repository["toolchain_digest"])
        and observed is not None
        and unavailable is not None
        and baseline is not None
        and len(observed) > 0
        and repository["declared_path_count"] <= policy["maximum_observed_paths"]
        and (
            policy["require_code_owner_scope"] is False
            or bool(repository["code_owner_scope_digest"])
        )
    )


def _path_accounting_valid(repository: Mapping[str, Any]) -> bool:
    observed = tuple(repository["observed_paths"])
    unavailable = tuple(repository["unavailable_paths"])
    return (
        all(observed)
        and all(unavailable)
        and len(observed) == len(set(observed))
        and len(unavailable) == len(set(unavailable))
        and set(observed).isdisjoint(unavailable)
        and len(observed) + len(unavailable) == repository["declared_path_count"]
    )


def _baseline_valid(
    repository: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    baseline = tuple(repository["baseline_check_digests"])
    if len(baseline) != len(set(baseline)) or not all(baseline):
        return False
    if policy["require_complete_baseline"]:
        return repository["baseline_checks_complete"] is True and bool(baseline)
    return True


def _window_valid(
    repository: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    started = repository["observation_started_epoch"]
    completed = repository["observation_completed_epoch"]
    return started <= completed and completed - started <= policy["maximum_observation_duration"]


def _replay_closed(repository: Mapping[str, Any]) -> bool:
    return (
        bool(repository["session_id"])
        and bool(repository["nonce_digest"])
        and repository["session_id"] not in repository["prior_session_ids"]
        and repository["nonce_digest"] not in repository["prior_nonce_digests"]
        and repository[REPOSITORY_OBSERVATION_DIGEST_FIELD]
        not in repository["prior_observation_digests"]
    )


def _disposition_and_mode(
    intent: Mapping[str, Any],
    repository: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> tuple[str, str]:
    if not _intent_provenance_valid(intent):
        return DISPOSITION_INTENT_PROVENANCE_REPAIR, MODE_REJECTED
    if not _repository_identity_valid(repository, policy):
        return DISPOSITION_REPOSITORY_IDENTITY_REPAIR, MODE_REJECTED
    if not _snapshot_valid(repository, policy):
        return DISPOSITION_REPOSITORY_SNAPSHOT_REPAIR, MODE_REJECTED
    if not _path_accounting_valid(repository):
        return DISPOSITION_PATH_ACCOUNTING_REPAIR, MODE_REJECTED
    if not _baseline_valid(repository, policy):
        return DISPOSITION_BASELINE_EVIDENCE_REPAIR, MODE_REJECTED
    if not _window_valid(repository, policy):
        return DISPOSITION_OBSERVATION_WINDOW_REPAIR, MODE_REJECTED
    if not _replay_closed(repository):
        return DISPOSITION_REPLAY_REJECTED, MODE_REJECTED
    if repository["observation_collected_by_kernel"] is True or any(
        repository[field] is True for field in _MUTATION_FIELDS
    ):
        return DISPOSITION_REPOSITORY_MUTATION_REJECTED, MODE_REJECTED
    if any(repository[field] is True for field in _AUTHORITY_FIELDS):
        return DISPOSITION_AUTHORITY_ESCALATION_REJECTED, MODE_REJECTED
    if intent["unresolved_questions"]:
        return DISPOSITION_INTENT_CLARIFICATION_HOLD, MODE_HOLD
    if (
        repository["toolchain_supported"] is not True
        or repository["toolchain_digest"] not in policy["supported_toolchain_digests"]
    ):
        return DISPOSITION_UNSUPPORTED_TOOLCHAIN_ABSTAINED, MODE_ABSTAIN
    if repository["crosses_unowned_boundary"] is True:
        return DISPOSITION_OWNERSHIP_HANDOVER, MODE_HANDOVER
    if repository["unavailable_paths"]:
        if policy["allow_partial_observation"] is True:
            return DISPOSITION_PARTIAL_OBSERVATION_DEGRADED, MODE_DEGRADED_READ_ONLY
        return DISPOSITION_REPOSITORY_SNAPSHOT_REPAIR, MODE_REJECTED
    return DISPOSITION_SUPPORTED, MODE_READ_ONLY


def _receipt(
    intent: Mapping[str, Any],
    repository: Mapping[str, Any],
    policy: Mapping[str, Any],
    disposition: str,
    operating_mode: str,
) -> dict[str, Any]:
    supported = disposition == DISPOSITION_SUPPORTED
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "intent_packet_digest": intent[INTENT_DIGEST_FIELD],
        "repository_observation_digest": repository[
            REPOSITORY_OBSERVATION_DIGEST_FIELD
        ],
        "observation_policy_digest": policy[POLICY_DIGEST_FIELD],
        "intent_id": intent["intent_id"],
        "intent_revision": intent["intent_revision"],
        "source_actor_id": intent["source_actor_id"],
        "authority_owner_id": intent["authority_owner_id"],
        "repository_full_name": repository["repository_full_name"],
        "source_commit_sha": repository["source_commit_sha"],
        "resulting_commit_sha": repository["source_commit_sha"],
        "source_branch": repository["source_branch"],
        "tree_digest": repository["tree_digest"],
        "observed_path_count": len(repository["observed_paths"]),
        "unavailable_path_count": len(repository["unavailable_paths"]),
        "declared_path_count": repository["declared_path_count"],
        "baseline_checks_complete": repository["baseline_checks_complete"],
        "codeai_disposition": disposition,
        "operating_mode": operating_mode,
        "route_receipt_recorded": True,
        "codeai_profile_ready": supported,
        "clarification_required": operating_mode == MODE_HOLD,
        "reobservation_required": operating_mode == MODE_DEGRADED_READ_ONLY,
        "abstained": operating_mode == MODE_ABSTAIN,
        "handover_required": operating_mode == MODE_HANDOVER,
        "repository_observation_read_only": True,
        "code_change_candidate_created": False,
        "execution_lease_issued": False,
        "repository_mutation_performed": False,
        "git_ref_changed": False,
        "branch_created": False,
        "commit_created": False,
        "push_performed": False,
        "pull_request_created": False,
        "merge_performed": False,
        "deployment_performed": False,
        "secret_access_performed": False,
        "selection_authority_granted": False,
        "execution_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "secret_access_authority_granted": False,
        "intent_treated_as_truth": False,
        "repository_observation_treated_as_repository_truth": False,
        "validation_treated_as_correctness_proof": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return receipt


def build_codeai_intent_repository_observation_envelope(
    *,
    intent_packet: Any,
    repository_observation: Any,
    observation_policy: Any,
) -> CodeAIObservationResult:
    intent, repository, policy, issues = _preflight(
        intent_packet, repository_observation, observation_policy
    )
    if issues or intent is None or repository is None or policy is None:
        return CodeAIObservationResult(STATUS_BLOCKED, issues, None)
    disposition, operating_mode = _disposition_and_mode(intent, repository, policy)
    return CodeAIObservationResult(
        STATUS_READY,
        (),
        _receipt(intent, repository, policy, disposition, operating_mode),
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIObservationResult",
    "build_codeai_intent_repository_observation_envelope",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "seal",
]
