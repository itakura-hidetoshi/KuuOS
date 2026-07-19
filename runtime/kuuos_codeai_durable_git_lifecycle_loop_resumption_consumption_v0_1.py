#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping

from runtime.kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_types_v0_1 import (
    DISPOSITION_ADMITTED as SOURCE_DISPOSITION_ADMITTED,
    EVIDENCE_DIGEST_FIELD as SOURCE_EVIDENCE_DIGEST_FIELD,
    PROFILE_VERSION as SOURCE_PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as SOURCE_REGISTRY_DIGEST_FIELD,
    RESUME_INPUT_DIGEST_FIELD as SOURCE_RESUME_INPUT_DIGEST_FIELD,
    canonical_digest,
    digest_without,
)

VERSION = "kuuos_codeai_durable_git_lifecycle_loop_resumption_consumption_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Durable Git Lifecycle Loop Resumption Consumption v0.1"
EXECUTION_INPUT_PROFILE_VERSION = "CodeAI Durable Git Lifecycle Loop Execution Input v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

DISPOSITION_CONSUMED = "durable_git_lifecycle_loop_resumption_input_consumed"

REQUEST_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_consumption_request_digest"
POLICY_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_consumption_policy_digest"
REGISTRY_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_consumption_registry_digest"
EXECUTION_INPUT_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_execution_input_digest"
EVIDENCE_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_consumption_evidence_digest"
RECEIPT_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_consumption_receipt_digest"

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_IDENTIFIER = re.compile(r"^[A-Za-z0-9_.:/-]+$")

SOURCE_RESUME_INPUT_FIELDS = {
    "schema_version",
    "profile_version",
    "resume_input_id",
    "checkpoint_id",
    "checkpoint_envelope_digest",
    "source_persistence_receipt_digest",
    "source_persistence_registry_digest",
    "source_store_state_digest",
    "loop_id",
    "lifecycle_id",
    "repository_full_name",
    "loop_disposition",
    "prior_effect_count",
    "prior_maximum_effect_count",
    "final_lifecycle_receipt_digest",
    "final_lifecycle_state_digest",
    "final_lifecycle_completed",
    "final_execution_lease_issued",
    "resume_effect_budget",
    "resume_execution_command_budget",
    "resume_execution_output_bytes",
    "issued_epoch",
    "future_only",
    "active_now",
    "loop_execution_authorized",
    "git_effect_authorized",
    "automatic_resumption_authorized",
    "general_successor_stage_authority_granted",
    SOURCE_RESUME_INPUT_DIGEST_FIELD,
}

REQUEST_FIELDS = {
    "consumption_session_id",
    "consumption_nonce_digest",
    "source_resumption_receipt_digest",
    "source_resumption_evidence_digest",
    "source_resumption_registry_digest",
    "source_resume_input_digest",
    "checkpoint_id",
    "checkpoint_envelope_digest",
    "loop_id",
    "lifecycle_id",
    "repository_full_name",
    "consumer_id",
    "execution_session_id",
    "request_created_epoch",
    "consume_resume_input",
    "issue_execution_input",
    "source_correspondence_confirmed",
    REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_source_resumption_receipt_digest",
    "expected_source_resumption_evidence_digest",
    "expected_source_resumption_registry_digest",
    "expected_source_resume_input_digest",
    "expected_repository_full_name",
    "authorized_consumer_ids",
    "maximum_request_age",
    "maximum_registry_entries",
    "maximum_resume_effect_budget",
    "maximum_resume_execution_command_budget",
    "maximum_resume_execution_output_bytes",
    "evaluation_epoch",
    "allow_resume_input_consumption",
    "require_future_only_input",
    "require_inactive_input",
    "require_nonce_consumption",
    "allow_execution_input_issuance",
    "allow_loop_execution_during_consumption",
    "allow_git_effect_during_consumption",
    "allow_automatic_resumption",
    "allow_network_access",
    "allow_secret_material_read",
    "allow_general_successor_authority",
    POLICY_DIGEST_FIELD,
}

REGISTRY_FIELDS = {
    "registry_id",
    "registry_revision",
    "consumed_consumption_nonce_digests",
    "consumed_resumption_receipt_digests",
    "consumed_resume_input_digests",
    "issued_execution_input_digests",
    "successful_consumption_count",
    "last_consumption_epoch",
    REGISTRY_DIGEST_FIELD,
}


@dataclass(frozen=True)
class CodeAIDurableGitLifecycleLoopResumptionConsumptionResult:
    status: str
    issues: tuple[str, ...]
    execution_input: dict[str, Any] | None
    evidence: dict[str, Any] | None
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


def _strings(value: Any, *, nonempty: bool = False) -> tuple[str, ...] | None:
    if not isinstance(value, list):
        return None
    if not all(isinstance(item, str) and item for item in value):
        return None
    parsed = tuple(value)
    if len(parsed) != len(set(parsed)):
        return None
    if nonempty and not parsed:
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


def _validate_source_receipt(value: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    if not _digest_ok(value, SOURCE_RECEIPT_DIGEST_FIELD):
        issues.append("source_resumption_receipt_digest_mismatch")
    if value.get("profile_version") != SOURCE_PROFILE_VERSION:
        issues.append("source_resumption_receipt_profile_unsupported")
    if value.get("codeai_disposition") != SOURCE_DISPOSITION_ADMITTED:
        issues.append("source_resumption_receipt_disposition_invalid")
    required_true = (
        "route_receipt_recorded",
        "source_persistence_bundle_verified",
        "resumption_nonce_consumed",
        "resumption_registry_advanced_once",
        "read_adapter_invoked_once",
        "checkpoint_read_verified",
        "resume_input_issued",
        "future_only",
    )
    required_false = (
        "checkpoint_unavailable",
        "checkpoint_read_failed",
        "checkpoint_read_evidence_quarantined",
        "loop_execution_performed",
        "git_effect_performed",
        "automatic_resumption_performed",
        "network_accessed",
        "secret_material_read",
        "general_git_authority_granted",
        "general_successor_stage_authority_granted",
        "active_now",
    )
    for field in required_true:
        if value.get(field) is not True:
            issues.append("source_resumption_receipt_required_true:" + field)
    for field in required_false:
        if value.get(field) is not False:
            issues.append("source_resumption_receipt_required_false:" + field)
    for field in (
        "resumption_evidence_digest",
        "next_resumption_registry_digest",
        "resume_input_digest",
        "checkpoint_envelope_digest",
    ):
        if not isinstance(value.get(field), str) or not _SHA256.fullmatch(value[field]):
            issues.append("source_resumption_receipt_invalid_digest:" + field)
    for field in ("checkpoint_id", "loop_id", "lifecycle_id"):
        if not isinstance(value.get(field), str) or not _IDENTIFIER.fullmatch(value[field]):
            issues.append("source_resumption_receipt_invalid_identifier:" + field)
    repository = value.get("repository_full_name")
    if not isinstance(repository, str) or not _REPOSITORY.fullmatch(repository):
        issues.append("source_resumption_receipt_invalid_repository")
    return issues


def _validate_source_evidence(value: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    if not _digest_ok(value, SOURCE_EVIDENCE_DIGEST_FIELD):
        issues.append("source_resumption_evidence_digest_mismatch")
    if value.get("checkpoint_read_verified") is not True:
        issues.append("source_resumption_evidence_checkpoint_not_verified")
    if value.get("resume_input_issued") is not True:
        issues.append("source_resumption_evidence_resume_input_not_issued")
    for field in ("loop_executed", "git_effect_performed", "automatic_resumption_performed"):
        if value.get(field) is not False:
            issues.append("source_resumption_evidence_forbidden_effect:" + field)
    resume_digest = value.get("resume_input_digest")
    if not isinstance(resume_digest, str) or not _SHA256.fullmatch(resume_digest):
        issues.append("source_resumption_evidence_invalid_resume_input_digest")
    return issues


def _validate_source_registry(value: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    if not _digest_ok(value, SOURCE_REGISTRY_DIGEST_FIELD):
        issues.append("source_resumption_registry_digest_mismatch")
    for field in (
        "registry_revision",
        "resumption_attempt_count",
        "successful_resumption_admission_count",
        "last_resumption_epoch",
    ):
        if _nat(value.get(field)) is None:
            issues.append("source_resumption_registry_invalid_nat:" + field)
    checkpoints = _strings(value.get("admitted_checkpoint_ids"))
    envelopes = _strings(value.get("admitted_checkpoint_envelope_digests"))
    persistence_receipts = _strings(value.get("admitted_persistence_receipt_digests"))
    nonces = _strings(value.get("consumed_resumption_nonce_digests"))
    histories = {
        "admitted_checkpoint_ids": checkpoints,
        "admitted_checkpoint_envelope_digests": envelopes,
        "admitted_persistence_receipt_digests": persistence_receipts,
        "consumed_resumption_nonce_digests": nonces,
    }
    for field, parsed in histories.items():
        if parsed is None:
            issues.append("source_resumption_registry_invalid_history:" + field)
    if envelopes is not None and not all(_SHA256.fullmatch(item) for item in envelopes):
        issues.append("source_resumption_registry_invalid_envelope_digest")
    if persistence_receipts is not None and not all(_SHA256.fullmatch(item) for item in persistence_receipts):
        issues.append("source_resumption_registry_invalid_persistence_digest")
    if nonces is not None and not all(_SHA256.fullmatch(item) for item in nonces):
        issues.append("source_resumption_registry_invalid_nonce_digest")
    if checkpoints is not None and not all(_IDENTIFIER.fullmatch(item) for item in checkpoints):
        issues.append("source_resumption_registry_invalid_checkpoint_id")
    if checkpoints is not None and envelopes is not None and persistence_receipts is not None:
        successful = len(checkpoints)
        if not (successful == len(envelopes) == len(persistence_receipts)):
            issues.append("source_resumption_registry_parallel_history_mismatch")
        if value.get("successful_resumption_admission_count") != successful:
            issues.append("source_resumption_registry_success_count_mismatch")
    if nonces is not None and value.get("resumption_attempt_count") != len(nonces):
        issues.append("source_resumption_registry_attempt_count_mismatch")
    if value.get("registry_revision") != value.get("resumption_attempt_count"):
        issues.append("source_resumption_registry_revision_count_mismatch")
    return issues


def _validate_resume_input(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, SOURCE_RESUME_INPUT_FIELDS, "source_resume_input")
    if issues:
        return issues
    if not _digest_ok(value, SOURCE_RESUME_INPUT_DIGEST_FIELD):
        issues.append("source_resume_input_digest_mismatch")
    for field in (
        "checkpoint_envelope_digest",
        "source_persistence_receipt_digest",
        "source_persistence_registry_digest",
        "source_store_state_digest",
        "final_lifecycle_receipt_digest",
        "final_lifecycle_state_digest",
    ):
        if not isinstance(value.get(field), str) or not _SHA256.fullmatch(value[field]):
            issues.append("source_resume_input_invalid_digest:" + field)
    for field in ("resume_input_id", "checkpoint_id", "loop_id", "lifecycle_id"):
        if not isinstance(value.get(field), str) or not _IDENTIFIER.fullmatch(value[field]):
            issues.append("source_resume_input_invalid_identifier:" + field)
    if not isinstance(value.get("repository_full_name"), str) or not _REPOSITORY.fullmatch(
        value["repository_full_name"]
    ):
        issues.append("source_resume_input_invalid_repository")
    for field in (
        "prior_effect_count",
        "prior_maximum_effect_count",
        "resume_effect_budget",
        "resume_execution_command_budget",
        "resume_execution_output_bytes",
        "issued_epoch",
    ):
        if _nat(value.get(field), positive=field in {
            "resume_effect_budget",
            "resume_execution_command_budget",
            "resume_execution_output_bytes",
        }) is None:
            issues.append("source_resume_input_invalid_nat:" + field)
    if (
        _nat(value.get("prior_effect_count")) is not None
        and _nat(value.get("prior_maximum_effect_count")) is not None
        and value["prior_effect_count"] > value["prior_maximum_effect_count"]
    ):
        issues.append("source_resume_input_prior_effect_count_exceeds_maximum")
    for field in (
        "final_lifecycle_completed",
        "final_execution_lease_issued",
        "future_only",
        "active_now",
        "loop_execution_authorized",
        "git_effect_authorized",
        "automatic_resumption_authorized",
        "general_successor_stage_authority_granted",
    ):
        if not isinstance(value.get(field), bool):
            issues.append("source_resume_input_invalid_bool:" + field)
    if value.get("future_only") is not True:
        issues.append("source_resume_input_not_future_only")
    for field in (
        "active_now",
        "loop_execution_authorized",
        "git_effect_authorized",
        "automatic_resumption_authorized",
        "general_successor_stage_authority_granted",
    ):
        if value.get(field) is not False:
            issues.append("source_resume_input_required_false:" + field)
    return issues


def _validate_request(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, REQUEST_FIELDS, "resumption_consumption_request")
    if issues:
        return issues
    string_fields = REQUEST_FIELDS - {
        "request_created_epoch",
        "consume_resume_input",
        "issue_execution_input",
        "source_correspondence_confirmed",
        REQUEST_DIGEST_FIELD,
    }
    for field in string_fields:
        if not isinstance(value.get(field), str) or not value[field]:
            issues.append("resumption_consumption_request_invalid_string:" + field)
    for field in (
        "consumption_nonce_digest",
        "source_resumption_receipt_digest",
        "source_resumption_evidence_digest",
        "source_resumption_registry_digest",
        "source_resume_input_digest",
        "checkpoint_envelope_digest",
    ):
        if not isinstance(value.get(field), str) or not _SHA256.fullmatch(value[field]):
            issues.append("resumption_consumption_request_invalid_digest:" + field)
    for field in (
        "consumption_session_id",
        "checkpoint_id",
        "loop_id",
        "lifecycle_id",
        "consumer_id",
        "execution_session_id",
    ):
        if not _IDENTIFIER.fullmatch(value[field]):
            issues.append("resumption_consumption_request_invalid_identifier:" + field)
    if not _REPOSITORY.fullmatch(value["repository_full_name"]):
        issues.append("resumption_consumption_request_invalid_repository")
    if _nat(value.get("request_created_epoch")) is None:
        issues.append("resumption_consumption_request_invalid_epoch")
    for field in ("consume_resume_input", "issue_execution_input", "source_correspondence_confirmed"):
        if not isinstance(value.get(field), bool):
            issues.append("resumption_consumption_request_invalid_bool:" + field)
    if not _digest_ok(value, REQUEST_DIGEST_FIELD):
        issues.append("resumption_consumption_request_digest_mismatch")
    return issues


def _validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, POLICY_FIELDS, "resumption_consumption_policy")
    if issues:
        return issues
    for field in (
        "expected_source_resumption_receipt_digest",
        "expected_source_resumption_evidence_digest",
        "expected_source_resumption_registry_digest",
        "expected_source_resume_input_digest",
    ):
        if not isinstance(value.get(field), str) or not _SHA256.fullmatch(value[field]):
            issues.append("resumption_consumption_policy_invalid_digest:" + field)
    if not isinstance(value.get("expected_repository_full_name"), str) or not _REPOSITORY.fullmatch(
        value["expected_repository_full_name"]
    ):
        issues.append("resumption_consumption_policy_invalid_repository")
    consumers = _strings(value.get("authorized_consumer_ids"), nonempty=True)
    if consumers is None or not all(_IDENTIFIER.fullmatch(item) for item in consumers):
        issues.append("resumption_consumption_policy_invalid_consumers")
    for field in (
        "maximum_request_age",
        "maximum_registry_entries",
        "maximum_resume_effect_budget",
        "maximum_resume_execution_command_budget",
        "maximum_resume_execution_output_bytes",
        "evaluation_epoch",
    ):
        if _nat(value.get(field), positive=field != "evaluation_epoch") is None:
            issues.append("resumption_consumption_policy_invalid_nat:" + field)
    bool_fields = POLICY_FIELDS - {
        "expected_source_resumption_receipt_digest",
        "expected_source_resumption_evidence_digest",
        "expected_source_resumption_registry_digest",
        "expected_source_resume_input_digest",
        "expected_repository_full_name",
        "authorized_consumer_ids",
        "maximum_request_age",
        "maximum_registry_entries",
        "maximum_resume_effect_budget",
        "maximum_resume_execution_command_budget",
        "maximum_resume_execution_output_bytes",
        "evaluation_epoch",
        POLICY_DIGEST_FIELD,
    }
    for field in bool_fields:
        if not isinstance(value.get(field), bool):
            issues.append("resumption_consumption_policy_invalid_bool:" + field)
    if not _digest_ok(value, POLICY_DIGEST_FIELD):
        issues.append("resumption_consumption_policy_digest_mismatch")
    return issues


def _validate_registry(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, REGISTRY_FIELDS, "resumption_consumption_registry")
    if issues:
        return issues
    if not isinstance(value.get("registry_id"), str) or not _IDENTIFIER.fullmatch(value["registry_id"]):
        issues.append("resumption_consumption_registry_invalid_id")
    for field in (
        "registry_revision",
        "successful_consumption_count",
        "last_consumption_epoch",
    ):
        if _nat(value.get(field)) is None:
            issues.append("resumption_consumption_registry_invalid_nat:" + field)
    histories = {
        "consumed_consumption_nonce_digests": _strings(value.get("consumed_consumption_nonce_digests")),
        "consumed_resumption_receipt_digests": _strings(value.get("consumed_resumption_receipt_digests")),
        "consumed_resume_input_digests": _strings(value.get("consumed_resume_input_digests")),
        "issued_execution_input_digests": _strings(value.get("issued_execution_input_digests")),
    }
    for field, parsed in histories.items():
        if parsed is None:
            issues.append("resumption_consumption_registry_invalid_history:" + field)
        elif not all(_SHA256.fullmatch(item) for item in parsed):
            issues.append("resumption_consumption_registry_invalid_digest_history:" + field)
    if all(parsed is not None for parsed in histories.values()):
        count = len(histories["consumed_consumption_nonce_digests"] or ())
        if not all(len(parsed or ()) == count for parsed in histories.values()):
            issues.append("resumption_consumption_registry_parallel_history_mismatch")
        if value["successful_consumption_count"] != count:
            issues.append("resumption_consumption_registry_success_count_mismatch")
        if value["registry_revision"] != count:
            issues.append("resumption_consumption_registry_revision_count_mismatch")
    if not _digest_ok(value, REGISTRY_DIGEST_FIELD):
        issues.append("resumption_consumption_registry_digest_mismatch")
    return issues


def _source_correspondence(
    *,
    source_receipt: Mapping[str, Any],
    source_evidence: Mapping[str, Any],
    source_registry: Mapping[str, Any],
    resume_input: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> bool:
    return (
        source_receipt["resumption_evidence_digest"] == source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD]
        and source_receipt["next_resumption_registry_digest"] == source_registry[SOURCE_REGISTRY_DIGEST_FIELD]
        and source_receipt["resume_input_digest"] == resume_input[SOURCE_RESUME_INPUT_DIGEST_FIELD]
        and source_evidence["resume_input_digest"] == resume_input[SOURCE_RESUME_INPUT_DIGEST_FIELD]
        and resume_input["checkpoint_id"] in source_registry["admitted_checkpoint_ids"]
        and resume_input["checkpoint_envelope_digest"]
            in source_registry["admitted_checkpoint_envelope_digests"]
        and request["source_resumption_receipt_digest"] == source_receipt[SOURCE_RECEIPT_DIGEST_FIELD]
        and request["source_resumption_evidence_digest"] == source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD]
        and request["source_resumption_registry_digest"] == source_registry[SOURCE_REGISTRY_DIGEST_FIELD]
        and request["source_resume_input_digest"] == resume_input[SOURCE_RESUME_INPUT_DIGEST_FIELD]
        and request["checkpoint_id"] == source_receipt["checkpoint_id"] == resume_input["checkpoint_id"]
        and request["checkpoint_envelope_digest"]
            == source_receipt["checkpoint_envelope_digest"]
            == resume_input["checkpoint_envelope_digest"]
        and request["loop_id"] == source_receipt["loop_id"] == resume_input["loop_id"]
        and request["lifecycle_id"] == source_receipt["lifecycle_id"] == resume_input["lifecycle_id"]
        and request["repository_full_name"]
            == source_receipt["repository_full_name"]
            == resume_input["repository_full_name"]
        and policy["expected_source_resumption_receipt_digest"]
            == source_receipt[SOURCE_RECEIPT_DIGEST_FIELD]
        and policy["expected_source_resumption_evidence_digest"]
            == source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD]
        and policy["expected_source_resumption_registry_digest"]
            == source_registry[SOURCE_REGISTRY_DIGEST_FIELD]
        and policy["expected_source_resume_input_digest"]
            == resume_input[SOURCE_RESUME_INPUT_DIGEST_FIELD]
        and policy["expected_repository_full_name"] == resume_input["repository_full_name"]
        and request["consumer_id"] in policy["authorized_consumer_ids"]
    )


def _policy_safe(
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    resume_input: Mapping[str, Any],
) -> bool:
    required = (
        policy["allow_resume_input_consumption"],
        policy["require_future_only_input"],
        policy["require_inactive_input"],
        policy["require_nonce_consumption"],
        policy["allow_execution_input_issuance"],
    )
    forbidden = (
        policy["allow_loop_execution_during_consumption"],
        policy["allow_git_effect_during_consumption"],
        policy["allow_automatic_resumption"],
        policy["allow_network_access"],
        policy["allow_secret_material_read"],
        policy["allow_general_successor_authority"],
    )
    return (
        all(required)
        and not any(forbidden)
        and request["consume_resume_input"] is True
        and request["issue_execution_input"] is True
        and request["source_correspondence_confirmed"] is True
        and resume_input["future_only"] is True
        and resume_input["active_now"] is False
        and resume_input["loop_execution_authorized"] is False
        and resume_input["git_effect_authorized"] is False
        and resume_input["automatic_resumption_authorized"] is False
        and resume_input["general_successor_stage_authority_granted"] is False
        and resume_input["resume_effect_budget"] <= policy["maximum_resume_effect_budget"]
        and resume_input["resume_execution_command_budget"]
            <= policy["maximum_resume_execution_command_budget"]
        and resume_input["resume_execution_output_bytes"]
            <= policy["maximum_resume_execution_output_bytes"]
    )


def _fresh_and_replay_closed(
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    registry: Mapping[str, Any],
) -> bool:
    age = policy["evaluation_epoch"] - request["request_created_epoch"]
    return (
        0 <= age <= policy["maximum_request_age"]
        and request["consumption_nonce_digest"] not in registry["consumed_consumption_nonce_digests"]
        and request["source_resumption_receipt_digest"]
            not in registry["consumed_resumption_receipt_digests"]
        and request["source_resume_input_digest"] not in registry["consumed_resume_input_digests"]
        and len(registry["consumed_consumption_nonce_digests"]) < policy["maximum_registry_entries"]
    )


def _execution_input(
    *,
    source_receipt: Mapping[str, Any],
    source_evidence: Mapping[str, Any],
    source_registry: Mapping[str, Any],
    resume_input: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": EXECUTION_INPUT_PROFILE_VERSION,
        "execution_input_id": request["execution_session_id"] + ":loop-execution-input",
        "source_resumption_receipt_digest": source_receipt[SOURCE_RECEIPT_DIGEST_FIELD],
        "source_resumption_evidence_digest": source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD],
        "source_resumption_registry_digest": source_registry[SOURCE_REGISTRY_DIGEST_FIELD],
        "source_resume_input_digest": resume_input[SOURCE_RESUME_INPUT_DIGEST_FIELD],
        "checkpoint_id": resume_input["checkpoint_id"],
        "checkpoint_envelope_digest": resume_input["checkpoint_envelope_digest"],
        "loop_id": resume_input["loop_id"],
        "lifecycle_id": resume_input["lifecycle_id"],
        "repository_full_name": resume_input["repository_full_name"],
        "prior_loop_disposition": resume_input["loop_disposition"],
        "prior_effect_count": resume_input["prior_effect_count"],
        "prior_maximum_effect_count": resume_input["prior_maximum_effect_count"],
        "resume_effect_budget": resume_input["resume_effect_budget"],
        "resume_execution_command_budget": resume_input["resume_execution_command_budget"],
        "resume_execution_output_bytes": resume_input["resume_execution_output_bytes"],
        "issued_epoch": policy["evaluation_epoch"],
        "one_shot": True,
        "reusable": False,
        "active_now": True,
        "loop_execution_authorized": True,
        "direct_git_effect_authorized": False,
        "automatic_execution_authorized": False,
        "network_access_authorized": False,
        "secret_material_read_authorized": False,
        "general_git_authority_granted": False,
        "general_successor_stage_authority_granted": False,
    }
    value[EXECUTION_INPUT_DIGEST_FIELD] = canonical_digest(value)
    return value


def _next_registry(
    registry: Mapping[str, Any],
    *,
    request: Mapping[str, Any],
    execution_input_digest: str,
    epoch: int,
) -> dict[str, Any]:
    value = dict(registry)
    value["registry_revision"] += 1
    value["consumed_consumption_nonce_digests"] = [
        *value["consumed_consumption_nonce_digests"],
        request["consumption_nonce_digest"],
    ]
    value["consumed_resumption_receipt_digests"] = [
        *value["consumed_resumption_receipt_digests"],
        request["source_resumption_receipt_digest"],
    ]
    value["consumed_resume_input_digests"] = [
        *value["consumed_resume_input_digests"],
        request["source_resume_input_digest"],
    ]
    value["issued_execution_input_digests"] = [
        *value["issued_execution_input_digests"],
        execution_input_digest,
    ]
    value["successful_consumption_count"] += 1
    value["last_consumption_epoch"] = epoch
    value.pop(REGISTRY_DIGEST_FIELD, None)
    value[REGISTRY_DIGEST_FIELD] = canonical_digest(value)
    return value


def build_codeai_durable_git_lifecycle_loop_resumption_consumption(
    *,
    resumption_receipt: Any,
    resumption_evidence: Any,
    resumption_registry: Any,
    resume_input: Any,
    consumption_request: Any,
    consumption_policy: Any,
    consumption_registry: Any,
) -> CodeAIDurableGitLifecycleLoopResumptionConsumptionResult:
    source_receipt = _mapping(resumption_receipt)
    source_evidence = _mapping(resumption_evidence)
    source_registry = _mapping(resumption_registry)
    source_input = _mapping(resume_input)
    request = _mapping(consumption_request)
    policy = _mapping(consumption_policy)
    registry = _mapping(consumption_registry)

    issues: list[str] = []
    for value, issue in (
        (source_receipt, "resumption_receipt_not_mapping"),
        (source_evidence, "resumption_evidence_not_mapping"),
        (source_registry, "resumption_registry_not_mapping"),
        (source_input, "resume_input_not_mapping"),
        (request, "consumption_request_not_mapping"),
        (policy, "consumption_policy_not_mapping"),
        (registry, "consumption_registry_not_mapping"),
    ):
        if value is None:
            issues.append(issue)
    if source_receipt is not None:
        issues.extend(_validate_source_receipt(source_receipt))
    if source_evidence is not None:
        issues.extend(_validate_source_evidence(source_evidence))
    if source_registry is not None:
        issues.extend(_validate_source_registry(source_registry))
    if source_input is not None:
        issues.extend(_validate_resume_input(source_input))
    if request is not None:
        issues.extend(_validate_request(request))
    if policy is not None:
        issues.extend(_validate_policy(policy))
    if registry is not None:
        issues.extend(_validate_registry(registry))

    if issues or any(
        value is None
        for value in (
            source_receipt,
            source_evidence,
            source_registry,
            source_input,
            request,
            policy,
            registry,
        )
    ):
        return CodeAIDurableGitLifecycleLoopResumptionConsumptionResult(
            STATUS_BLOCKED, tuple(issues), None, None, None, None
        )

    assert source_receipt is not None and source_evidence is not None
    assert source_registry is not None and source_input is not None
    assert request is not None and policy is not None and registry is not None

    if not _source_correspondence(
        source_receipt=source_receipt,
        source_evidence=source_evidence,
        source_registry=source_registry,
        resume_input=source_input,
        request=request,
        policy=policy,
    ):
        issues.append("resumption_consumption_source_correspondence_mismatch")
    if not _policy_safe(request, policy, source_input):
        issues.append("resumption_consumption_policy_not_safe")
    if not _fresh_and_replay_closed(request, policy, registry):
        issues.append("resumption_consumption_freshness_capacity_or_replay_violation")
    if issues:
        return CodeAIDurableGitLifecycleLoopResumptionConsumptionResult(
            STATUS_BLOCKED, tuple(issues), None, None, None, None
        )

    execution_input = _execution_input(
        source_receipt=source_receipt,
        source_evidence=source_evidence,
        source_registry=source_registry,
        resume_input=source_input,
        request=request,
        policy=policy,
    )
    next_registry = _next_registry(
        registry,
        request=request,
        execution_input_digest=execution_input[EXECUTION_INPUT_DIGEST_FIELD],
        epoch=policy["evaluation_epoch"],
    )
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_resumption_receipt_digest": source_receipt[SOURCE_RECEIPT_DIGEST_FIELD],
        "source_resumption_evidence_digest": source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD],
        "source_resumption_registry_digest": source_registry[SOURCE_REGISTRY_DIGEST_FIELD],
        "source_resume_input_digest": source_input[SOURCE_RESUME_INPUT_DIGEST_FIELD],
        "consumption_request_digest": request[REQUEST_DIGEST_FIELD],
        "consumption_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_consumption_registry_digest": registry[REGISTRY_DIGEST_FIELD],
        "next_consumption_registry_digest": next_registry[REGISTRY_DIGEST_FIELD],
        "execution_input_digest": execution_input[EXECUTION_INPUT_DIGEST_FIELD],
        "source_correspondence_verified": True,
        "resume_input_consumed": True,
        "execution_input_issued": True,
        "execution_input_active": True,
        "loop_execution_performed": False,
        "git_effect_performed": False,
        "automatic_resumption_performed": False,
        "network_accessed": False,
        "secret_material_read": False,
    }
    evidence[EVIDENCE_DIGEST_FIELD] = canonical_digest(evidence)
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_resumption_receipt_digest": source_receipt[SOURCE_RECEIPT_DIGEST_FIELD],
        "source_resumption_evidence_digest": source_evidence[SOURCE_EVIDENCE_DIGEST_FIELD],
        "source_resumption_registry_digest": source_registry[SOURCE_REGISTRY_DIGEST_FIELD],
        "source_resume_input_digest": source_input[SOURCE_RESUME_INPUT_DIGEST_FIELD],
        "consumption_request_digest": request[REQUEST_DIGEST_FIELD],
        "consumption_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_consumption_registry_digest": registry[REGISTRY_DIGEST_FIELD],
        "next_consumption_registry_digest": next_registry[REGISTRY_DIGEST_FIELD],
        "consumption_evidence_digest": evidence[EVIDENCE_DIGEST_FIELD],
        "execution_input_digest": execution_input[EXECUTION_INPUT_DIGEST_FIELD],
        "checkpoint_id": source_input["checkpoint_id"],
        "checkpoint_envelope_digest": source_input["checkpoint_envelope_digest"],
        "loop_id": source_input["loop_id"],
        "lifecycle_id": source_input["lifecycle_id"],
        "repository_full_name": source_input["repository_full_name"],
        "codeai_disposition": DISPOSITION_CONSUMED,
        "operating_mode": "durable_git_lifecycle_loop_resumption_consumption",
        "route_receipt_recorded": True,
        "source_resumption_bundle_verified": True,
        "source_resume_input_verified": True,
        "consumption_nonce_consumed": True,
        "consumption_registry_advanced_once": True,
        "resume_input_consumed": True,
        "execution_input_issued": True,
        "execution_input_one_shot": True,
        "execution_input_reusable": False,
        "execution_input_active": True,
        "loop_execution_authorized_for_successor": True,
        "direct_git_effect_authorized": False,
        "automatic_execution_authorized": False,
        "loop_execution_performed": False,
        "git_effect_performed": False,
        "automatic_resumption_performed": False,
        "network_accessed": False,
        "secret_material_read": False,
        "general_git_authority_granted": False,
        "general_successor_stage_authority_granted": False,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return CodeAIDurableGitLifecycleLoopResumptionConsumptionResult(
        STATUS_READY,
        (),
        execution_input,
        evidence,
        next_registry,
        receipt,
    )


__all__ = [
    "VERSION",
    "SCHEMA_VERSION",
    "PROFILE_VERSION",
    "EXECUTION_INPUT_PROFILE_VERSION",
    "STATUS_READY",
    "STATUS_BLOCKED",
    "DISPOSITION_CONSUMED",
    "REQUEST_DIGEST_FIELD",
    "POLICY_DIGEST_FIELD",
    "REGISTRY_DIGEST_FIELD",
    "EXECUTION_INPUT_DIGEST_FIELD",
    "EVIDENCE_DIGEST_FIELD",
    "RECEIPT_DIGEST_FIELD",
    "CodeAIDurableGitLifecycleLoopResumptionConsumptionResult",
    "build_codeai_durable_git_lifecycle_loop_resumption_consumption",
]
