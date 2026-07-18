#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_codeai_candidate_patch_envelope_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Candidate Patch v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

MODE_PROPOSAL_ONLY = "proposal_only"
MODE_HOLD = "hold"
MODE_DEGRADED_PROPOSAL = "degraded_proposal"
MODE_ABSTAIN = "abstain"
MODE_HANDOVER = "handover"
MODE_REJECTED = "rejected"

DISPOSITION_SUPPORTED = "candidate_patch_supported"
DISPOSITION_SOURCE_RECEIPT_REPAIR = (
    "source_observation_receipt_repair_required"
)
DISPOSITION_CANDIDATE_PROVENANCE_REPAIR = (
    "candidate_provenance_repair_required"
)
DISPOSITION_REPOSITORY_CORRESPONDENCE_REPAIR = (
    "repository_correspondence_repair_required"
)
DISPOSITION_PATCH_ARTIFACT_REPAIR = "patch_artifact_repair_required"
DISPOSITION_CANDIDATE_WINDOW_REPAIR = "candidate_window_repair_required"
DISPOSITION_REPLAY_REJECTED = "candidate_replay_conflict_rejected"
DISPOSITION_REPOSITORY_MUTATION_REJECTED = "repository_mutation_rejected"
DISPOSITION_AUTHORITY_ESCALATION_REJECTED = "authority_escalation_rejected"
DISPOSITION_UNSUPPORTED_PATCH_FORMAT_ABSTAINED = (
    "unsupported_patch_format_abstained"
)
DISPOSITION_PATCH_SYNTAX_REPAIR = "patch_syntax_repair_required"
DISPOSITION_PATH_ACCOUNTING_REPAIR = "path_accounting_repair_required"
DISPOSITION_CANDIDATE_SCOPE_REJECTED = "candidate_scope_violation_rejected"
DISPOSITION_CANDIDATE_BUDGET_REJECTED = "candidate_budget_exceeded_rejected"
DISPOSITION_CANDIDATE_CLARIFICATION_HOLD = "candidate_clarification_hold"
DISPOSITION_RISK_OWNERSHIP_HANDOVER = "risk_ownership_handover_required"
DISPOSITION_CANDIDATE_EVIDENCE_REPAIR = "candidate_evidence_repair_required"
DISPOSITION_CANDIDATE_EVIDENCE_DEGRADED = "candidate_evidence_degraded"

SOURCE_RECEIPT_DIGEST_FIELD = (
    "codeai_intent_repository_observation_receipt_digest"
)
CANDIDATE_DIGEST_FIELD = "codeai_candidate_patch_digest"
POLICY_DIGEST_FIELD = "codeai_candidate_patch_policy_digest"
RECEIPT_DIGEST_FIELD = "codeai_candidate_patch_receipt_digest"

SOURCE_RECEIPT_FIELDS = {
    "schema_version",
    "profile_version",
    "intent_packet_digest",
    "repository_observation_digest",
    "observation_policy_digest",
    "intent_id",
    "intent_revision",
    "source_actor_id",
    "authority_owner_id",
    "repository_full_name",
    "source_commit_sha",
    "resulting_commit_sha",
    "source_branch",
    "tree_digest",
    "observed_path_count",
    "unavailable_path_count",
    "declared_path_count",
    "baseline_checks_complete",
    "codeai_disposition",
    "operating_mode",
    "route_receipt_recorded",
    "codeai_profile_ready",
    "clarification_required",
    "reobservation_required",
    "abstained",
    "handover_required",
    "repository_observation_read_only",
    "code_change_candidate_created",
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
    "selection_authority_granted",
    "execution_authority_granted",
    "merge_authority_granted",
    "deployment_authority_granted",
    "secret_access_authority_granted",
    "intent_treated_as_truth",
    "repository_observation_treated_as_repository_truth",
    "validation_treated_as_correctness_proof",
    "history_read_only",
    "future_only",
    "active_now",
    SOURCE_RECEIPT_DIGEST_FIELD,
}

CANDIDATE_FIELDS = {
    "candidate_id",
    "candidate_revision",
    "producer_id",
    "producer_session_id",
    "source_observation_receipt_digest",
    "intent_packet_digest",
    "repository_full_name",
    "source_commit_sha",
    "patch_format",
    "patch_artifact_digest",
    "patch_size_bytes",
    "changed_paths",
    "added_paths",
    "modified_paths",
    "deleted_paths",
    "renamed_from_paths",
    "renamed_to_paths",
    "declared_change_count",
    "requirement_trace_ids",
    "test_plan_ids",
    "risk_labels",
    "unresolved_candidate_questions",
    "candidate_created_epoch",
    "prior_candidate_digests",
    "prior_producer_session_ids",
    "candidate_provenance_confirmed",
    "binary_patch_present",
    "submodule_patch_present",
    "mode_change_present",
    "candidate_generated_by_kernel",
    "patch_applied_by_kernel",
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
    CANDIDATE_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_source_observation_receipt_digest",
    "expected_repository_full_name",
    "expected_source_commit_sha",
    "allowed_patch_formats",
    "maximum_patch_bytes",
    "maximum_changed_paths",
    "allowed_path_prefixes",
    "forbidden_path_prefixes",
    "allow_deletions",
    "allow_renames",
    "allow_binary_patches",
    "allow_submodule_patches",
    "allow_mode_changes",
    "require_requirement_trace",
    "require_test_plan",
    "allow_evidence_degradation",
    "known_risk_labels",
    "handover_risk_labels",
    "evaluation_epoch",
    "maximum_candidate_age",
    POLICY_DIGEST_FIELD,
}

_SOURCE_STRING_FIELDS = (
    "schema_version",
    "profile_version",
    "intent_packet_digest",
    "repository_observation_digest",
    "observation_policy_digest",
    "intent_id",
    "intent_revision",
    "source_actor_id",
    "authority_owner_id",
    "repository_full_name",
    "source_commit_sha",
    "resulting_commit_sha",
    "source_branch",
    "tree_digest",
    "codeai_disposition",
    "operating_mode",
    SOURCE_RECEIPT_DIGEST_FIELD,
)

_SOURCE_BOOL_FIELDS = tuple(sorted(
    SOURCE_RECEIPT_FIELDS
    - set(_SOURCE_STRING_FIELDS)
    - {"observed_path_count", "unavailable_path_count", "declared_path_count"}
))

_CANDIDATE_LIST_FIELDS = (
    "changed_paths",
    "added_paths",
    "modified_paths",
    "deleted_paths",
    "renamed_from_paths",
    "renamed_to_paths",
    "requirement_trace_ids",
    "test_plan_ids",
    "risk_labels",
    "unresolved_candidate_questions",
    "prior_candidate_digests",
    "prior_producer_session_ids",
)

_CANDIDATE_BOOL_FIELDS = (
    "candidate_provenance_confirmed",
    "binary_patch_present",
    "submodule_patch_present",
    "mode_change_present",
    "candidate_generated_by_kernel",
    "patch_applied_by_kernel",
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
)

_MUTATION_FIELDS = (
    "candidate_generated_by_kernel",
    "patch_applied_by_kernel",
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
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class PatchShape:
    changed_paths: tuple[str, ...]
    added_paths: tuple[str, ...]
    modified_paths: tuple[str, ...]
    deleted_paths: tuple[str, ...]
    renamed_from_paths: tuple[str, ...]
    renamed_to_paths: tuple[str, ...]
    binary_patch_present: bool
    submodule_patch_present: bool
    mode_change_present: bool


@dataclass(frozen=True)
class CodeAICandidatePatchResult:
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


def patch_artifact_digest(patch_artifact: str) -> str:
    return hashlib.sha256(patch_artifact.encode("utf-8")).hexdigest()


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


def _validate_source_receipt(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, SOURCE_RECEIPT_FIELDS, "source_receipt")
    if issues:
        return issues
    for field in _SOURCE_STRING_FIELDS:
        if not isinstance(value.get(field), str):
            issues.append("source_receipt_invalid_string:" + field)
    for field in ("observed_path_count", "unavailable_path_count", "declared_path_count"):
        if _nat(value.get(field)) is None:
            issues.append("source_receipt_invalid_nat:" + field)
    for field in _SOURCE_BOOL_FIELDS:
        if not isinstance(value.get(field), bool):
            issues.append("source_receipt_invalid_bool:" + field)
    if value.get(SOURCE_RECEIPT_DIGEST_FIELD) != digest_without(
        value, SOURCE_RECEIPT_DIGEST_FIELD
    ):
        issues.append("source_receipt_digest_mismatch")
    return issues


def _validate_candidate(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, CANDIDATE_FIELDS, "patch_candidate")
    if issues:
        return issues
    for field in (
        "candidate_id",
        "candidate_revision",
        "producer_id",
        "producer_session_id",
        "source_observation_receipt_digest",
        "intent_packet_digest",
        "repository_full_name",
        "source_commit_sha",
        "patch_format",
        "patch_artifact_digest",
        CANDIDATE_DIGEST_FIELD,
    ):
        if not isinstance(value.get(field), str):
            issues.append("patch_candidate_invalid_string:" + field)
    for field in _CANDIDATE_LIST_FIELDS:
        if _strings(value.get(field)) is None:
            issues.append("patch_candidate_invalid_string_list:" + field)
    for field in ("patch_size_bytes", "declared_change_count", "candidate_created_epoch"):
        if _nat(value.get(field)) is None:
            issues.append("patch_candidate_invalid_nat:" + field)
    for field in _CANDIDATE_BOOL_FIELDS:
        if not isinstance(value.get(field), bool):
            issues.append("patch_candidate_invalid_bool:" + field)
    if value.get(CANDIDATE_DIGEST_FIELD) != digest_without(value, CANDIDATE_DIGEST_FIELD):
        issues.append("patch_candidate_digest_mismatch")
    return issues


def _validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, POLICY_FIELDS, "candidate_policy")
    if issues:
        return issues
    for field in (
        "expected_source_observation_receipt_digest",
        "expected_repository_full_name",
        "expected_source_commit_sha",
        POLICY_DIGEST_FIELD,
    ):
        if not isinstance(value.get(field), str):
            issues.append("candidate_policy_invalid_string:" + field)
    for field in (
        "allowed_patch_formats",
        "allowed_path_prefixes",
        "forbidden_path_prefixes",
        "known_risk_labels",
        "handover_risk_labels",
    ):
        if _strings(value.get(field)) is None:
            issues.append("candidate_policy_invalid_string_list:" + field)
    for field in (
        "maximum_patch_bytes",
        "maximum_changed_paths",
        "maximum_candidate_age",
    ):
        if _positive_nat(value.get(field)) is None:
            issues.append("candidate_policy_invalid_positive_nat:" + field)
    if _nat(value.get("evaluation_epoch")) is None:
        issues.append("candidate_policy_invalid_evaluation_epoch")
    for field in (
        "allow_deletions",
        "allow_renames",
        "allow_binary_patches",
        "allow_submodule_patches",
        "allow_mode_changes",
        "require_requirement_trace",
        "require_test_plan",
        "allow_evidence_degradation",
    ):
        if not isinstance(value.get(field), bool):
            issues.append("candidate_policy_invalid_bool:" + field)
    for field in (
        "allowed_patch_formats",
        "allowed_path_prefixes",
        "known_risk_labels",
    ):
        parsed = _strings(value.get(field))
        if parsed is not None and (
            not parsed or not all(parsed) or len(parsed) != len(set(parsed))
        ):
            issues.append("candidate_policy_invalid_nonempty_unique_list:" + field)
    for field in ("forbidden_path_prefixes", "handover_risk_labels"):
        parsed = _strings(value.get(field))
        if parsed is not None and (
            not all(parsed) or len(parsed) != len(set(parsed))
        ):
            issues.append("candidate_policy_invalid_unique_list:" + field)
    known = _strings(value.get("known_risk_labels"))
    handover = _strings(value.get("handover_risk_labels"))
    if known is not None and handover is not None and not set(handover).issubset(known):
        issues.append("candidate_policy_handover_risk_not_known")
    if not isinstance(value.get("expected_source_observation_receipt_digest"), str) or not _SHA256.fullmatch(
        value["expected_source_observation_receipt_digest"]
    ):
        issues.append("candidate_policy_expected_source_receipt_digest_invalid")
    if not isinstance(value.get("expected_source_commit_sha"), str) or not _SHA40.fullmatch(
        value["expected_source_commit_sha"]
    ):
        issues.append("candidate_policy_expected_source_commit_sha_invalid")
    if value.get(POLICY_DIGEST_FIELD) != digest_without(value, POLICY_DIGEST_FIELD):
        issues.append("candidate_policy_digest_mismatch")
    return issues


def _preflight(
    source_observation_receipt: Any,
    patch_candidate: Any,
    patch_artifact: Any,
    candidate_policy: Any,
) -> tuple[
    Mapping[str, Any] | None,
    Mapping[str, Any] | None,
    str | None,
    Mapping[str, Any] | None,
    tuple[str, ...],
]:
    source = _mapping(source_observation_receipt)
    candidate = _mapping(patch_candidate)
    artifact = patch_artifact if isinstance(patch_artifact, str) else None
    policy = _mapping(candidate_policy)
    issues: list[str] = []
    if source is None:
        issues.append("source_receipt_not_mapping")
    else:
        issues.extend(_validate_source_receipt(source))
    if candidate is None:
        issues.append("patch_candidate_not_mapping")
    else:
        issues.extend(_validate_candidate(candidate))
    if artifact is None:
        issues.append("patch_artifact_not_string")
    if policy is None:
        issues.append("candidate_policy_not_mapping")
    else:
        issues.extend(_validate_policy(policy))
    return source, candidate, artifact, policy, tuple(issues)


def _nonempty_unique_strings(value: Any) -> bool:
    parsed = _strings(value)
    return (
        parsed is not None
        and bool(parsed)
        and all(parsed)
        and len(parsed) == len(set(parsed))
    )


def _unique_strings(value: Any) -> bool:
    parsed = _strings(value)
    return parsed is not None and len(parsed) == len(set(parsed))


def _unique_nonempty_items(value: Any) -> bool:
    parsed = _strings(value)
    return parsed is not None and all(parsed) and len(parsed) == len(set(parsed))


def _source_receipt_supported(source: Mapping[str, Any]) -> bool:
    false_fields = (
        "clarification_required",
        "reobservation_required",
        "abstained",
        "handover_required",
        "code_change_candidate_created",
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
        "selection_authority_granted",
        "execution_authority_granted",
        "merge_authority_granted",
        "deployment_authority_granted",
        "secret_access_authority_granted",
        "intent_treated_as_truth",
        "repository_observation_treated_as_repository_truth",
        "validation_treated_as_correctness_proof",
        "active_now",
    )
    return (
        source["schema_version"] == "v0.1"
        and source["profile_version"] == "CodeAI v0.1"
        and bool(_SHA256.fullmatch(source[SOURCE_RECEIPT_DIGEST_FIELD]))
        and bool(_SHA256.fullmatch(source["intent_packet_digest"]))
        and bool(_SHA256.fullmatch(source["repository_observation_digest"]))
        and bool(_SHA256.fullmatch(source["observation_policy_digest"]))
        and bool(_SHA40.fullmatch(source["source_commit_sha"]))
        and bool(source["intent_id"])
        and bool(source["intent_revision"])
        and bool(source["source_actor_id"])
        and bool(source["authority_owner_id"])
        and bool(source["repository_full_name"])
        and bool(source["source_branch"])
        and bool(source["tree_digest"])
        and source["codeai_disposition"] == "intent_repository_observation_supported"
        and source["operating_mode"] == "read_only"
        and source["route_receipt_recorded"] is True
        and source["codeai_profile_ready"] is True
        and source["repository_observation_read_only"] is True
        and source["baseline_checks_complete"] is True
        and source["history_read_only"] is True
        and source["future_only"] is True
        and source["source_commit_sha"] == source["resulting_commit_sha"]
        and source["observed_path_count"] + source["unavailable_path_count"]
        == source["declared_path_count"]
        and all(source[field] is False for field in false_fields)
    )


def _candidate_provenance_valid(candidate: Mapping[str, Any]) -> bool:
    return (
        candidate["candidate_provenance_confirmed"] is True
        and bool(candidate["candidate_id"])
        and bool(candidate["candidate_revision"])
        and bool(candidate["producer_id"])
        and bool(candidate["producer_session_id"])
        and bool(_SHA256.fullmatch(candidate["source_observation_receipt_digest"]))
        and bool(_SHA256.fullmatch(candidate["intent_packet_digest"]))
        and bool(_SHA40.fullmatch(candidate["source_commit_sha"]))
        and bool(_SHA256.fullmatch(candidate["patch_artifact_digest"]))
        and _unique_nonempty_items(candidate["prior_candidate_digests"])
        and all(
            _SHA256.fullmatch(digest)
            for digest in candidate["prior_candidate_digests"]
        )
        and _unique_nonempty_items(candidate["prior_producer_session_ids"])
        and _unique_nonempty_items(candidate["unresolved_candidate_questions"])
        and _unique_nonempty_items(candidate["requirement_trace_ids"])
        and _unique_nonempty_items(candidate["test_plan_ids"])
        and _unique_nonempty_items(candidate["risk_labels"])
    )


def _repository_correspondence_valid(
    source: Mapping[str, Any],
    candidate: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> bool:
    return (
        candidate["source_observation_receipt_digest"]
        == source[SOURCE_RECEIPT_DIGEST_FIELD]
        == policy["expected_source_observation_receipt_digest"]
        and candidate["intent_packet_digest"] == source["intent_packet_digest"]
        and candidate["repository_full_name"]
        == source["repository_full_name"]
        == policy["expected_repository_full_name"]
        and candidate["source_commit_sha"]
        == source["source_commit_sha"]
        == policy["expected_source_commit_sha"]
    )


def _artifact_valid(candidate: Mapping[str, Any], artifact: str) -> bool:
    return (
        bool(artifact)
        and "\0" not in artifact
        and "\r" not in artifact
        and artifact.endswith("\n")
        and candidate["patch_size_bytes"] == len(artifact.encode("utf-8"))
        and candidate["patch_artifact_digest"] == patch_artifact_digest(artifact)
    )


def _window_valid(candidate: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    created = candidate["candidate_created_epoch"]
    evaluated = policy["evaluation_epoch"]
    return created <= evaluated and evaluated - created <= policy["maximum_candidate_age"]


def _replay_closed(candidate: Mapping[str, Any]) -> bool:
    return (
        candidate["producer_session_id"] not in candidate["prior_producer_session_ids"]
        and candidate[CANDIDATE_DIGEST_FIELD] not in candidate["prior_candidate_digests"]
    )


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
        and not path.startswith('"')
        and not path.endswith('"')
        and all(segment not in ("", ".", "..") for segment in segments)
    )


def _parse_diff_header(line: str) -> tuple[str, str] | None:
    prefix = "diff --git a/"
    if not line.startswith(prefix):
        return None
    body = line[len(prefix) :]
    marker = " b/"
    if body.count(marker) != 1:
        return None
    old_path, new_path = body.split(marker, 1)
    if not _canonical_repository_path(old_path) or not _canonical_repository_path(new_path):
        return None
    return old_path, new_path


def parse_unified_diff(patch_artifact: str) -> tuple[PatchShape | None, tuple[str, ...]]:
    sections: list[tuple[tuple[str, str], list[str]]] = []
    current_header: tuple[str, str] | None = None
    current_lines: list[str] = []
    issues: list[str] = []
    for line in patch_artifact.splitlines():
        if line.startswith("diff --git "):
            parsed = _parse_diff_header(line)
            if parsed is None:
                issues.append("patch_diff_header_invalid")
                current_header = None
                current_lines = []
                continue
            if current_header is not None:
                sections.append((current_header, current_lines))
            current_header = parsed
            current_lines = []
        elif current_header is None:
            if line:
                issues.append("patch_preamble_not_supported")
        else:
            current_lines.append(line)
    if current_header is not None:
        sections.append((current_header, current_lines))
    if not sections:
        issues.append("patch_has_no_diff_sections")
    if issues:
        return None, tuple(sorted(set(issues)))

    added: list[str] = []
    modified: list[str] = []
    deleted: list[str] = []
    renamed_from: list[str] = []
    renamed_to: list[str] = []
    touched: set[str] = set()
    binary_present = False
    submodule_present = False
    mode_change_present = False

    for (old_path, new_path), lines in sections:
        new_modes = [line for line in lines if line.startswith("new file mode ")]
        deleted_modes = [line for line in lines if line.startswith("deleted file mode ")]
        rename_from_lines = [line[len("rename from ") :] for line in lines if line.startswith("rename from ")]
        rename_to_lines = [line[len("rename to ") :] for line in lines if line.startswith("rename to ")]
        old_modes = [line for line in lines if line.startswith("old mode ")]
        changed_modes = [line for line in lines if line.startswith("new mode ")]
        has_hunk = any(line.startswith("@@ ") for line in lines)
        has_binary = any(
            line == "GIT binary patch" or line.startswith("Binary files ")
            for line in lines
        )
        has_submodule = any("160000" in line for line in lines if "mode" in line or line.startswith("index "))
        if len(new_modes) > 1 or len(deleted_modes) > 1:
            issues.append("patch_file_mode_marker_duplicate")
            continue
        if bool(rename_from_lines) != bool(rename_to_lines):
            issues.append("patch_rename_pair_incomplete")
            continue
        if len(rename_from_lines) > 1 or len(rename_to_lines) > 1:
            issues.append("patch_rename_pair_duplicate")
            continue
        if new_modes and deleted_modes:
            issues.append("patch_add_delete_conflict")
            continue
        has_rename = bool(rename_from_lines)
        has_mode_change = bool(old_modes or changed_modes)
        if has_rename:
            rename_from = rename_from_lines[0]
            rename_to = rename_to_lines[0]
            if (
                not _canonical_repository_path(rename_from)
                or not _canonical_repository_path(rename_to)
                or rename_from != old_path
                or rename_to != new_path
            ):
                issues.append("patch_rename_header_mismatch")
                continue
            paths = {rename_from, rename_to}
            renamed_from.append(rename_from)
            renamed_to.append(rename_to)
        elif new_modes:
            if old_path != new_path:
                issues.append("patch_added_path_header_mismatch")
                continue
            paths = {new_path}
            added.append(new_path)
        elif deleted_modes:
            if old_path != new_path:
                issues.append("patch_deleted_path_header_mismatch")
                continue
            paths = {old_path}
            deleted.append(old_path)
        else:
            if old_path != new_path:
                issues.append("patch_path_change_without_rename")
                continue
            paths = {old_path}
            modified.append(old_path)
        if not (has_hunk or has_binary or has_rename or new_modes or deleted_modes or has_mode_change):
            issues.append("patch_section_has_no_change_evidence")
            continue
        if touched.intersection(paths):
            issues.append("patch_path_repeated_across_sections")
            continue
        touched.update(paths)
        binary_present = binary_present or has_binary
        submodule_present = submodule_present or has_submodule
        mode_change_present = mode_change_present or has_mode_change

    if issues:
        return None, tuple(sorted(set(issues)))
    shape = PatchShape(
        changed_paths=tuple(sorted(touched)),
        added_paths=tuple(sorted(added)),
        modified_paths=tuple(sorted(modified)),
        deleted_paths=tuple(sorted(deleted)),
        renamed_from_paths=tuple(sorted(renamed_from)),
        renamed_to_paths=tuple(sorted(renamed_to)),
        binary_patch_present=binary_present,
        submodule_patch_present=submodule_present,
        mode_change_present=mode_change_present,
    )
    return shape, ()


def _path_accounting_valid(candidate: Mapping[str, Any], shape: PatchShape) -> bool:
    list_fields = (
        "changed_paths",
        "added_paths",
        "modified_paths",
        "deleted_paths",
        "renamed_from_paths",
        "renamed_to_paths",
    )
    for field in list_fields:
        values = tuple(candidate[field])
        if values != tuple(sorted(values)) or len(values) != len(set(values)):
            return False
        if not all(_canonical_repository_path(path) for path in values):
            return False
    return (
        tuple(candidate["changed_paths"]) == shape.changed_paths
        and tuple(candidate["added_paths"]) == shape.added_paths
        and tuple(candidate["modified_paths"]) == shape.modified_paths
        and tuple(candidate["deleted_paths"]) == shape.deleted_paths
        and tuple(candidate["renamed_from_paths"]) == shape.renamed_from_paths
        and tuple(candidate["renamed_to_paths"]) == shape.renamed_to_paths
        and candidate["declared_change_count"] == len(shape.changed_paths)
        and candidate["binary_patch_present"] is shape.binary_patch_present
        and candidate["submodule_patch_present"] is shape.submodule_patch_present
        and candidate["mode_change_present"] is shape.mode_change_present
    )


def _prefix_matches(path: str, prefix: str) -> bool:
    return path == prefix or path.startswith(prefix + "/")


def _scope_valid(shape: PatchShape, policy: Mapping[str, Any]) -> bool:
    allowed = tuple(policy["allowed_path_prefixes"])
    forbidden = tuple(policy["forbidden_path_prefixes"])
    if not _nonempty_unique_strings(
        policy["allowed_path_prefixes"]
    ) or not _unique_strings(policy["forbidden_path_prefixes"]):
        return False
    if not all(_canonical_repository_path(prefix) for prefix in allowed + forbidden):
        return False
    if any(not any(_prefix_matches(path, prefix) for prefix in allowed) for path in shape.changed_paths):
        return False
    if any(any(_prefix_matches(path, prefix) for prefix in forbidden) for path in shape.changed_paths):
        return False
    return (
        (policy["allow_deletions"] is True or not shape.deleted_paths)
        and (policy["allow_renames"] is True or not shape.renamed_from_paths)
        and (policy["allow_binary_patches"] is True or not shape.binary_patch_present)
        and (policy["allow_submodule_patches"] is True or not shape.submodule_patch_present)
        and (policy["allow_mode_changes"] is True or not shape.mode_change_present)
    )


def _budget_valid(candidate: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    return (
        candidate["patch_size_bytes"] <= policy["maximum_patch_bytes"]
        and candidate["declared_change_count"] <= policy["maximum_changed_paths"]
    )


def _evidence_missing(candidate: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    return (
        policy["require_requirement_trace"] is True
        and not candidate["requirement_trace_ids"]
    ) or (policy["require_test_plan"] is True and not candidate["test_plan_ids"])


def _risk_handover_required(candidate: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    risks = set(candidate["risk_labels"])
    known = set(policy["known_risk_labels"])
    handover = set(policy["handover_risk_labels"])
    return not risks.issubset(known) or bool(risks.intersection(handover))


def _disposition_and_mode(
    source: Mapping[str, Any],
    candidate: Mapping[str, Any],
    artifact: str,
    policy: Mapping[str, Any],
) -> tuple[str, str, bool]:
    if not _source_receipt_supported(source):
        return DISPOSITION_SOURCE_RECEIPT_REPAIR, MODE_REJECTED, False
    if not _candidate_provenance_valid(candidate):
        return DISPOSITION_CANDIDATE_PROVENANCE_REPAIR, MODE_REJECTED, False
    if not _repository_correspondence_valid(source, candidate, policy):
        return DISPOSITION_REPOSITORY_CORRESPONDENCE_REPAIR, MODE_REJECTED, False
    if not _artifact_valid(candidate, artifact):
        return DISPOSITION_PATCH_ARTIFACT_REPAIR, MODE_REJECTED, False
    if not _window_valid(candidate, policy):
        return DISPOSITION_CANDIDATE_WINDOW_REPAIR, MODE_REJECTED, False
    if not _replay_closed(candidate):
        return DISPOSITION_REPLAY_REJECTED, MODE_REJECTED, False
    if any(candidate[field] is True for field in _MUTATION_FIELDS):
        return DISPOSITION_REPOSITORY_MUTATION_REJECTED, MODE_REJECTED, False
    if any(candidate[field] is True for field in _AUTHORITY_FIELDS):
        return DISPOSITION_AUTHORITY_ESCALATION_REJECTED, MODE_REJECTED, False
    if (
        not _nonempty_unique_strings(policy["allowed_patch_formats"])
        or candidate["patch_format"] not in policy["allowed_patch_formats"]
    ):
        return DISPOSITION_UNSUPPORTED_PATCH_FORMAT_ABSTAINED, MODE_ABSTAIN, False
    if candidate["patch_format"] != "unified_diff":
        return DISPOSITION_UNSUPPORTED_PATCH_FORMAT_ABSTAINED, MODE_ABSTAIN, False
    shape, syntax_issues = parse_unified_diff(artifact)
    if syntax_issues or shape is None:
        return DISPOSITION_PATCH_SYNTAX_REPAIR, MODE_REJECTED, False
    if not _path_accounting_valid(candidate, shape):
        return DISPOSITION_PATH_ACCOUNTING_REPAIR, MODE_REJECTED, True
    if not _scope_valid(shape, policy):
        return DISPOSITION_CANDIDATE_SCOPE_REJECTED, MODE_REJECTED, True
    if not _budget_valid(candidate, policy):
        return DISPOSITION_CANDIDATE_BUDGET_REJECTED, MODE_REJECTED, True
    if candidate["unresolved_candidate_questions"]:
        return DISPOSITION_CANDIDATE_CLARIFICATION_HOLD, MODE_HOLD, True
    if _risk_handover_required(candidate, policy):
        return DISPOSITION_RISK_OWNERSHIP_HANDOVER, MODE_HANDOVER, True
    if _evidence_missing(candidate, policy):
        if policy["allow_evidence_degradation"] is True:
            return DISPOSITION_CANDIDATE_EVIDENCE_DEGRADED, MODE_DEGRADED_PROPOSAL, True
        return DISPOSITION_CANDIDATE_EVIDENCE_REPAIR, MODE_REJECTED, True
    return DISPOSITION_SUPPORTED, MODE_PROPOSAL_ONLY, True


def _receipt(
    source: Mapping[str, Any],
    candidate: Mapping[str, Any],
    policy: Mapping[str, Any],
    disposition: str,
    operating_mode: str,
    artifact_parsed: bool,
) -> dict[str, Any]:
    supported = disposition == DISPOSITION_SUPPORTED
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_observation_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "candidate_patch_digest": candidate[CANDIDATE_DIGEST_FIELD],
        "candidate_policy_digest": policy[POLICY_DIGEST_FIELD],
        "intent_packet_digest": candidate["intent_packet_digest"],
        "candidate_id": candidate["candidate_id"],
        "candidate_revision": candidate["candidate_revision"],
        "producer_id": candidate["producer_id"],
        "repository_full_name": candidate["repository_full_name"],
        "source_commit_sha": candidate["source_commit_sha"],
        "resulting_commit_sha": candidate["source_commit_sha"],
        "patch_format": candidate["patch_format"],
        "patch_artifact_digest": candidate["patch_artifact_digest"],
        "patch_size_bytes": candidate["patch_size_bytes"],
        "changed_path_count": len(candidate["changed_paths"]),
        "added_path_count": len(candidate["added_paths"]),
        "modified_path_count": len(candidate["modified_paths"]),
        "deleted_path_count": len(candidate["deleted_paths"]),
        "renamed_path_count": len(candidate["renamed_from_paths"]),
        "declared_change_count": candidate["declared_change_count"],
        "codeai_disposition": disposition,
        "operating_mode": operating_mode,
        "route_receipt_recorded": True,
        "candidate_patch_artifact_parsed": artifact_parsed,
        "candidate_patch_recorded": True,
        "candidate_patch_ready": supported,
        "clarification_required": operating_mode == MODE_HOLD,
        "evidence_degraded": operating_mode == MODE_DEGRADED_PROPOSAL,
        "abstained": operating_mode == MODE_ABSTAIN,
        "handover_required": operating_mode == MODE_HANDOVER,
        "patch_candidate_only": True,
        "candidate_generated_by_kernel": False,
        "candidate_selected": False,
        "verification_lease_issued": False,
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
        "verification_authority_granted": False,
        "execution_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "secret_access_authority_granted": False,
        "source_receipt_treated_as_successor_authority": False,
        "candidate_treated_as_correct": False,
        "validation_treated_as_correctness_proof": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return receipt


def build_codeai_candidate_patch_envelope(
    *,
    source_observation_receipt: Any,
    patch_candidate: Any,
    patch_artifact: Any,
    candidate_policy: Any,
) -> CodeAICandidatePatchResult:
    source, candidate, artifact, policy, issues = _preflight(
        source_observation_receipt,
        patch_candidate,
        patch_artifact,
        candidate_policy,
    )
    if (
        issues
        or source is None
        or candidate is None
        or artifact is None
        or policy is None
    ):
        return CodeAICandidatePatchResult(STATUS_BLOCKED, issues, None)
    disposition, operating_mode, artifact_parsed = _disposition_and_mode(
        source, candidate, artifact, policy
    )
    return CodeAICandidatePatchResult(
        STATUS_READY,
        (),
        _receipt(
            source,
            candidate,
            policy,
            disposition,
            operating_mode,
            artifact_parsed,
        ),
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAICandidatePatchResult",
    "PatchShape",
    "build_codeai_candidate_patch_envelope",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "parse_unified_diff",
    "patch_artifact_digest",
    "seal",
]
