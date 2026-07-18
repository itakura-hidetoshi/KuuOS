#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping, Sequence

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    CANDIDATE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as CANDIDATE_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    patch_artifact_digest,
    seal,
)
from runtime.kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1 import (
    DISPOSITION_SELECTED as SELECTION_DISPOSITION_SELECTED,
    MODE_SELECTION_ONLY,
    PROFILE_VERSION as SELECTION_PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD as SELECTION_RECEIPT_DIGEST_FIELD,
    SelectedVerificationCandidate,
)

VERSION = "kuuos_codeai_autonomous_isolated_candidate_application_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Autonomous Isolated Candidate Application v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_ISOLATED_MATERIALIZATION_ONLY = "isolated_materialization_only"
DISPOSITION_MATERIALIZED = "selected_candidate_isolated_snapshot_materialized"
APPLICATION_PURPOSE = "independent_verification_workspace"

REQUEST_DIGEST_FIELD = "codeai_autonomous_isolated_candidate_application_request_digest"
POLICY_DIGEST_FIELD = "codeai_autonomous_isolated_candidate_application_policy_digest"
RECEIPT_DIGEST_FIELD = "codeai_autonomous_isolated_candidate_application_receipt_digest"

_REQUEST_FIELDS = {
    "application_request_id",
    "application_request_revision",
    "source_selection_receipt_digest",
    "selected_candidate_digest",
    "source_repository_snapshot_digest",
    "application_purpose",
    "requested_by_actor_id",
    "request_created_epoch",
    REQUEST_DIGEST_FIELD,
}

_POLICY_FIELDS = {
    "expected_source_selection_receipt_digest",
    "expected_selected_candidate_digest",
    "expected_patch_artifact_digest",
    "expected_repository_full_name",
    "expected_source_commit_sha",
    "expected_source_repository_snapshot_digest",
    "maximum_source_path_count",
    "maximum_source_snapshot_bytes",
    "maximum_result_path_count",
    "maximum_result_snapshot_bytes",
    "maximum_patch_bytes",
    "maximum_changed_paths",
    "allowed_path_prefixes",
    "forbidden_path_prefixes",
    "allow_additions",
    "allow_modifications",
    "allow_deletions",
    "require_exact_changed_path_accounting",
    "evaluation_epoch",
    "maximum_request_age",
    POLICY_DIGEST_FIELD,
}

_HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?: .*)?$")
_DIFF_RE = re.compile(r"^diff --git a/(.+) b/(.+)$")


@dataclass(frozen=True)
class ParsedPatchSection:
    path: str
    operation: str
    old_label: str
    new_label: str
    hunks: tuple[tuple[int, int, int, int, tuple[str, ...]], ...]


@dataclass(frozen=True)
class CodeAIAutonomousIsolatedCandidateApplicationResult:
    status: str
    issues: tuple[str, ...]
    resulting_repository_files: dict[str, str] | None
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


def _path_has_prefix(path: str, prefix: str) -> bool:
    normalized = prefix.rstrip("/")
    return path == normalized or path.startswith(normalized + "/")


def _snapshot_size_bytes(repository: Mapping[str, str]) -> int:
    return sum(
        len(path.encode("utf-8")) + len(content.encode("utf-8"))
        for path, content in repository.items()
    )


def _validate_repository_files(value: Any) -> tuple[Mapping[str, str] | None, list[str]]:
    repository = _mapping(value)
    if repository is None:
        return None, ["repository_files_not_mapping"]
    issues: list[str] = []
    for path, content in repository.items():
        if not isinstance(path, str) or not _canonical_repository_path(path):
            issues.append("repository_file_path_invalid:" + str(path))
        if not _canonical_text(content):
            issues.append("repository_file_content_invalid:" + str(path))
    return repository, issues


def _validate_selection_receipt(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    receipt = _mapping(value)
    if receipt is None:
        return None, ["source_selection_receipt_not_mapping"]
    issues: list[str] = []
    if not _digest_ok(receipt, SELECTION_RECEIPT_DIGEST_FIELD):
        issues.append("source_selection_receipt_digest_mismatch")
    if receipt.get("profile_version") != SELECTION_PROFILE_VERSION:
        issues.append("source_selection_profile_unsupported")
    if receipt.get("codeai_disposition") != SELECTION_DISPOSITION_SELECTED:
        issues.append("source_selection_disposition_invalid")
    if receipt.get("operating_mode") != MODE_SELECTION_ONLY:
        issues.append("source_selection_mode_invalid")
    for field in (
        "route_receipt_recorded",
        "candidate_selected",
        "selected_for_independent_verification",
        "selection_performed_by_kernel",
        "selection_authority_consumed_by_kernel",
    ):
        if receipt.get(field) is not True:
            issues.append("source_selection_required_true:" + field)
    for field in (
        "verification_lease_issued",
        "execution_lease_issued",
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
    ):
        if receipt.get(field) is not False:
            issues.append("source_selection_required_false:" + field)
    for field in (
        "selected_candidate_id",
        "selected_candidate_digest",
        "selected_patch_artifact_digest",
    ):
        if not isinstance(receipt.get(field), str) or not receipt.get(field):
            issues.append("source_selection_invalid_string:" + field)
    if _nat(receipt.get("selected_upstream_rank"), positive=True) is None:
        issues.append("source_selection_rank_invalid")
    return receipt, issues


def _validate_selected_candidate(value: Any) -> tuple[SelectedVerificationCandidate | None, list[str]]:
    if not isinstance(value, SelectedVerificationCandidate):
        return None, ["selected_candidate_invalid_type"]
    issues: list[str] = []
    candidate = _mapping(value.patch_candidate)
    candidate_receipt = _mapping(value.candidate_receipt)
    if candidate is None:
        return value, ["selected_patch_candidate_not_mapping"]
    if candidate_receipt is None:
        issues.append("selected_candidate_receipt_not_mapping")
    if candidate.get("candidate_id") != value.candidate_id:
        issues.append("selected_candidate_id_mismatch")
    if _nat(value.upstream_rank, positive=True) is None:
        issues.append("selected_candidate_rank_invalid")
    if not _digest_ok(candidate, CANDIDATE_DIGEST_FIELD):
        issues.append("selected_candidate_digest_mismatch")
    if candidate.get("patch_artifact_digest") != patch_artifact_digest(value.patch_artifact):
        issues.append("selected_patch_artifact_digest_mismatch")
    if candidate.get("patch_size_bytes") != len(value.patch_artifact.encode("utf-8")):
        issues.append("selected_patch_size_mismatch")
    if candidate.get("patch_format") != "unified_diff":
        issues.append("selected_patch_format_unsupported")
    for field in ("changed_paths", "added_paths", "modified_paths", "deleted_paths"):
        if _unique_strings(candidate.get(field), nonempty=(field == "changed_paths")) is None:
            issues.append("selected_candidate_invalid_path_list:" + field)
    if candidate_receipt is not None:
        if not _digest_ok(candidate_receipt, CANDIDATE_RECEIPT_DIGEST_FIELD):
            issues.append("selected_candidate_receipt_digest_mismatch")
        if candidate_receipt.get("candidate_patch_ready") is not True:
            issues.append("selected_candidate_receipt_not_ready")
        if candidate_receipt.get("codeai_disposition") != "candidate_patch_supported":
            issues.append("selected_candidate_receipt_not_supported")
    return value, issues


def _validate_request(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    request = _mapping(value)
    if request is None:
        return None, ["application_request_not_mapping"]
    issues = _exact_fields(request, _REQUEST_FIELDS, "application_request")
    if issues:
        return request, issues
    for field in (
        "application_request_id",
        "application_request_revision",
        "source_selection_receipt_digest",
        "selected_candidate_digest",
        "source_repository_snapshot_digest",
        "requested_by_actor_id",
    ):
        if not isinstance(request[field], str) or not request[field]:
            issues.append("application_request_invalid_string:" + field)
    if request["application_purpose"] != APPLICATION_PURPOSE:
        issues.append("application_request_purpose_invalid")
    if _nat(request["request_created_epoch"]) is None:
        issues.append("application_request_created_epoch_invalid")
    if not _digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("application_request_digest_mismatch")
    return request, issues


def _validate_policy(value: Any) -> tuple[Mapping[str, Any] | None, list[str]]:
    policy = _mapping(value)
    if policy is None:
        return None, ["application_policy_not_mapping"]
    issues = _exact_fields(policy, _POLICY_FIELDS, "application_policy")
    if issues:
        return policy, issues
    for field in (
        "expected_source_selection_receipt_digest",
        "expected_selected_candidate_digest",
        "expected_patch_artifact_digest",
        "expected_repository_full_name",
        "expected_source_commit_sha",
        "expected_source_repository_snapshot_digest",
    ):
        if not isinstance(policy[field], str) or not policy[field]:
            issues.append("application_policy_invalid_string:" + field)
    for field in (
        "maximum_source_path_count",
        "maximum_source_snapshot_bytes",
        "maximum_result_path_count",
        "maximum_result_snapshot_bytes",
        "maximum_patch_bytes",
        "maximum_changed_paths",
        "maximum_request_age",
    ):
        if _nat(policy[field], positive=True) is None:
            issues.append("application_policy_invalid_positive_nat:" + field)
    if _nat(policy["evaluation_epoch"]) is None:
        issues.append("application_policy_evaluation_epoch_invalid")
    for field in ("allowed_path_prefixes", "forbidden_path_prefixes"):
        if _unique_strings(policy[field], nonempty=(field == "allowed_path_prefixes")) is None:
            issues.append("application_policy_invalid_string_list:" + field)
    for field in (
        "allow_additions",
        "allow_modifications",
        "allow_deletions",
        "require_exact_changed_path_accounting",
    ):
        if not isinstance(policy[field], bool):
            issues.append("application_policy_invalid_bool:" + field)
    if not _digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("application_policy_digest_mismatch")
    return policy, issues


def _parse_unified_diff(artifact: str) -> tuple[list[ParsedPatchSection] | None, list[str]]:
    if not isinstance(artifact, str) or not artifact or not artifact.endswith("\n"):
        return None, ["patch_artifact_not_canonical_text"]
    lines = artifact.splitlines()
    sections: list[ParsedPatchSection] = []
    issues: list[str] = []
    index = 0
    seen_paths: set[str] = set()
    while index < len(lines):
        match = _DIFF_RE.fullmatch(lines[index])
        if match is None:
            issues.append(f"patch_line[{index + 1}]:diff_header_invalid")
            break
        left_path, right_path = match.group(1), match.group(2)
        if left_path != right_path or not _canonical_repository_path(left_path):
            issues.append(f"patch_line[{index + 1}]:diff_path_invalid")
            break
        path = left_path
        if path in seen_paths:
            issues.append("patch_path_duplicate:" + path)
            break
        seen_paths.add(path)
        index += 1
        mode: str | None = None
        if index < len(lines) and lines[index] == "new file mode 100644":
            mode = "add"
            index += 1
        elif index < len(lines) and lines[index] == "deleted file mode 100644":
            mode = "delete"
            index += 1
        if index + 1 >= len(lines) or not lines[index].startswith("--- ") or not lines[index + 1].startswith("+++ "):
            issues.append("patch_labels_missing:" + path)
            break
        old_label = lines[index][4:]
        new_label = lines[index + 1][4:]
        index += 2
        operation = mode or "modify"
        expected_labels = {
            "add": ("/dev/null", "b/" + path),
            "modify": ("a/" + path, "b/" + path),
            "delete": ("a/" + path, "/dev/null"),
        }[operation]
        if (old_label, new_label) != expected_labels:
            issues.append("patch_labels_invalid:" + path)
            break
        hunks: list[tuple[int, int, int, int, tuple[str, ...]]] = []
        while index < len(lines) and not lines[index].startswith("diff --git "):
            hunk_match = _HUNK_RE.fullmatch(lines[index])
            if hunk_match is None:
                issues.append(f"patch_line[{index + 1}]:hunk_header_invalid:{path}")
                break
            old_start = int(hunk_match.group(1))
            old_count = int(hunk_match.group(2) or "1")
            new_start = int(hunk_match.group(3))
            new_count = int(hunk_match.group(4) or "1")
            index += 1
            body: list[str] = []
            while index < len(lines):
                line = lines[index]
                if line.startswith("diff --git ") or line.startswith("@@ "):
                    break
                if not line or line[0] not in (" ", "+", "-"):
                    issues.append(f"patch_line[{index + 1}]:hunk_body_invalid:{path}")
                    break
                body.append(line)
                index += 1
            if issues:
                break
            hunks.append((old_start, old_count, new_start, new_count, tuple(body)))
        if issues:
            break
        if not hunks:
            issues.append("patch_hunks_missing:" + path)
            break
        sections.append(ParsedPatchSection(path, operation, old_label, new_label, tuple(hunks)))
    if issues:
        return None, sorted(set(issues))
    return sections, []


def _apply_hunks(old_content: str, section: ParsedPatchSection) -> tuple[str | None, list[str]]:
    old_lines = old_content.splitlines()
    result: list[str] = []
    old_index = 0
    issues: list[str] = []
    for hunk_index, (old_start, old_count, new_start, new_count, body) in enumerate(section.hunks):
        target_old_index = max(old_start - 1, 0)
        if target_old_index < old_index or target_old_index > len(old_lines):
            issues.append(f"{section.path}:hunk[{hunk_index}]:old_start_invalid")
            break
        new_prefix_length = len(result) + (target_old_index - old_index)
        expected_new_start = new_prefix_length + 1 if new_count > 0 else new_prefix_length
        if new_start not in (expected_new_start, max(expected_new_start - 1, 0)):
            issues.append(f"{section.path}:hunk[{hunk_index}]:new_start_invalid")
            break
        result.extend(old_lines[old_index:target_old_index])
        cursor = target_old_index
        old_seen = 0
        new_seen = 0
        for line_index, line in enumerate(body):
            prefix, text = line[0], line[1:]
            if prefix == " ":
                if cursor >= len(old_lines) or old_lines[cursor] != text:
                    issues.append(f"{section.path}:hunk[{hunk_index}].line[{line_index}]:context_mismatch")
                    break
                result.append(text)
                cursor += 1
                old_seen += 1
                new_seen += 1
            elif prefix == "-":
                if cursor >= len(old_lines) or old_lines[cursor] != text:
                    issues.append(f"{section.path}:hunk[{hunk_index}].line[{line_index}]:deletion_mismatch")
                    break
                cursor += 1
                old_seen += 1
            else:
                result.append(text)
                new_seen += 1
        if issues:
            break
        if old_seen != old_count or new_seen != new_count:
            issues.append(f"{section.path}:hunk[{hunk_index}]:line_count_mismatch")
            break
        old_index = cursor
    if issues:
        return None, issues
    result.extend(old_lines[old_index:])
    return ("\n".join(result) + ("\n" if result else "")), []


def _apply_sections(repository_files: Mapping[str, str], sections: Sequence[ParsedPatchSection]) -> tuple[dict[str, str] | None, list[str]]:
    result = dict(repository_files)
    issues: list[str] = []
    for section in sections:
        path = section.path
        exists = path in result
        if section.operation == "add":
            if exists:
                issues.append("add_path_already_exists:" + path)
                continue
            old_content = ""
        elif section.operation == "modify":
            if not exists:
                issues.append("modify_path_missing:" + path)
                continue
            old_content = result[path]
        else:
            if not exists:
                issues.append("delete_path_missing:" + path)
                continue
            old_content = result[path]
        new_content, hunk_issues = _apply_hunks(old_content, section)
        if hunk_issues or new_content is None:
            issues.extend(hunk_issues)
            continue
        if section.operation == "delete":
            if new_content:
                issues.append("delete_result_not_empty:" + path)
                continue
            del result[path]
        else:
            if not _canonical_text(new_content):
                issues.append("result_content_not_canonical:" + path)
                continue
            if section.operation == "modify" and new_content == old_content:
                issues.append("modify_result_unchanged:" + path)
                continue
            result[path] = new_content
    if issues:
        return None, sorted(set(issues))
    return result, []


def _receipt(*, selection_receipt: Mapping[str, Any], selected_candidate: SelectedVerificationCandidate, request: Mapping[str, Any], policy: Mapping[str, Any], source_repository_files: Mapping[str, str], resulting_repository_files: Mapping[str, str]) -> dict[str, Any]:
    candidate = selected_candidate.patch_candidate
    changed_paths = list(candidate["changed_paths"])
    result_digests = [
        {"path": path, "content_digest": canonical_digest(resulting_repository_files[path])}
        for path in changed_paths
        if path in resulting_repository_files
    ]
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_selection_receipt_digest": selection_receipt[SELECTION_RECEIPT_DIGEST_FIELD],
        "source_candidate_receipt_digest": selected_candidate.candidate_receipt[CANDIDATE_RECEIPT_DIGEST_FIELD],
        "selected_candidate_id": candidate["candidate_id"],
        "selected_candidate_digest": candidate[CANDIDATE_DIGEST_FIELD],
        "selected_patch_artifact_digest": candidate["patch_artifact_digest"],
        "application_request_digest": request[REQUEST_DIGEST_FIELD],
        "application_policy_digest": policy[POLICY_DIGEST_FIELD],
        "repository_full_name": candidate["repository_full_name"],
        "source_commit_sha": candidate["source_commit_sha"],
        "source_repository_snapshot_digest": canonical_digest(source_repository_files),
        "resulting_repository_snapshot_digest": canonical_digest(resulting_repository_files),
        "source_path_count": len(source_repository_files),
        "resulting_path_count": len(resulting_repository_files),
        "source_snapshot_size_bytes": _snapshot_size_bytes(source_repository_files),
        "resulting_snapshot_size_bytes": _snapshot_size_bytes(resulting_repository_files),
        "changed_paths": changed_paths,
        "added_paths": list(candidate["added_paths"]),
        "modified_paths": list(candidate["modified_paths"]),
        "deleted_paths": list(candidate["deleted_paths"]),
        "resulting_changed_path_digests": result_digests,
        "deleted_path_tombstones": list(candidate["deleted_paths"]),
        "codeai_disposition": DISPOSITION_MATERIALIZED,
        "operating_mode": MODE_ISOLATED_MATERIALIZATION_ONLY,
        "route_receipt_recorded": True,
        "application_policy_evaluated": True,
        "source_snapshot_verified": True,
        "selection_correspondence_verified": True,
        "candidate_correspondence_verified": True,
        "patch_artifact_parsed": True,
        "exact_changed_path_accounting_verified": True,
        "isolated_patch_applied": True,
        "isolated_snapshot_materialized": True,
        "verification_workspace_ready": True,
        "input_repository_snapshot_mutated": False,
        "live_repository_patch_applied": False,
        "live_repository_files_changed_by_kernel": False,
        "repository_mutation_performed": False,
        "git_ref_changed": False,
        "branch_created": False,
        "commit_created": False,
        "push_performed": False,
        "pull_request_created": False,
        "merge_performed": False,
        "deployment_performed": False,
        "secret_access_performed": False,
        "verification_executed": False,
        "verification_lease_issued": False,
        "execution_lease_issued": False,
        "successor_application_authority_granted": False,
        "verification_authority_granted": False,
        "execution_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "secret_access_authority_granted": False,
        "selected_candidate_treated_as_correct": False,
        "application_treated_as_verification": False,
        "materialization_treated_as_correctness_proof": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    return seal(value, RECEIPT_DIGEST_FIELD)


def build_codeai_autonomous_isolated_candidate_application(*, source_selection_receipt: Any, selected_candidate: Any, repository_files: Any, application_request: Any, application_policy: Any) -> CodeAIAutonomousIsolatedCandidateApplicationResult:
    selection_receipt, selection_issues = _validate_selection_receipt(source_selection_receipt)
    parsed_candidate, candidate_issues = _validate_selected_candidate(selected_candidate)
    repository, repository_issues = _validate_repository_files(repository_files)
    request, request_issues = _validate_request(application_request)
    policy, policy_issues = _validate_policy(application_policy)
    issues = selection_issues + candidate_issues + repository_issues + request_issues + policy_issues
    if issues or selection_receipt is None or parsed_candidate is None or repository is None or request is None or policy is None:
        return CodeAIAutonomousIsolatedCandidateApplicationResult(STATUS_BLOCKED, tuple(sorted(set(issues))), None, None)

    candidate = parsed_candidate.patch_candidate
    selection_digest = str(selection_receipt[SELECTION_RECEIPT_DIGEST_FIELD])
    candidate_digest = str(candidate[CANDIDATE_DIGEST_FIELD])
    artifact_digest = str(candidate["patch_artifact_digest"])
    snapshot_digest = canonical_digest(repository)

    if selection_receipt["selected_candidate_id"] != candidate["candidate_id"]:
        issues.append("selection_candidate_id_mismatch")
    if selection_receipt["selected_candidate_digest"] != candidate_digest:
        issues.append("selection_candidate_digest_mismatch")
    if selection_receipt["selected_patch_artifact_digest"] != artifact_digest:
        issues.append("selection_patch_artifact_digest_mismatch")
    if selection_receipt["selected_upstream_rank"] != parsed_candidate.upstream_rank:
        issues.append("selection_candidate_rank_mismatch")
    if request["source_selection_receipt_digest"] != selection_digest:
        issues.append("application_request_selection_receipt_mismatch")
    if policy["expected_source_selection_receipt_digest"] != selection_digest:
        issues.append("application_policy_selection_receipt_mismatch")
    if request["selected_candidate_digest"] != candidate_digest:
        issues.append("application_request_candidate_mismatch")
    if policy["expected_selected_candidate_digest"] != candidate_digest:
        issues.append("application_policy_candidate_mismatch")
    if policy["expected_patch_artifact_digest"] != artifact_digest:
        issues.append("application_policy_artifact_mismatch")
    if request["source_repository_snapshot_digest"] != snapshot_digest:
        issues.append("application_request_snapshot_mismatch")
    if policy["expected_source_repository_snapshot_digest"] != snapshot_digest:
        issues.append("application_policy_snapshot_mismatch")
    if policy["expected_repository_full_name"] != candidate["repository_full_name"]:
        issues.append("application_policy_repository_mismatch")
    if policy["expected_source_commit_sha"] != candidate["source_commit_sha"]:
        issues.append("application_policy_source_commit_mismatch")
    if len(repository) > policy["maximum_source_path_count"]:
        issues.append("source_path_count_budget_exceeded")
    if _snapshot_size_bytes(repository) > policy["maximum_source_snapshot_bytes"]:
        issues.append("source_snapshot_byte_budget_exceeded")
    if candidate["patch_size_bytes"] > policy["maximum_patch_bytes"]:
        issues.append("patch_byte_budget_exceeded")
    if candidate["declared_change_count"] > policy["maximum_changed_paths"]:
        issues.append("changed_path_budget_exceeded")
    evaluation_epoch = int(policy["evaluation_epoch"])
    created_epoch = int(request["request_created_epoch"])
    if not evaluation_epoch - int(policy["maximum_request_age"]) <= created_epoch <= evaluation_epoch:
        issues.append("application_request_window_invalid")
    for path in candidate["changed_paths"]:
        if not any(_path_has_prefix(path, prefix) for prefix in policy["allowed_path_prefixes"]):
            issues.append("changed_path_not_allowed:" + path)
        if any(_path_has_prefix(path, prefix) for prefix in policy["forbidden_path_prefixes"]):
            issues.append("changed_path_forbidden:" + path)
    if candidate["added_paths"] and not policy["allow_additions"]:
        issues.append("additions_not_allowed")
    if candidate["modified_paths"] and not policy["allow_modifications"]:
        issues.append("modifications_not_allowed")
    if candidate["deleted_paths"] and not policy["allow_deletions"]:
        issues.append("deletions_not_allowed")
    if issues:
        return CodeAIAutonomousIsolatedCandidateApplicationResult(STATUS_BLOCKED, tuple(sorted(set(issues))), None, None)

    sections, parse_issues = _parse_unified_diff(parsed_candidate.patch_artifact)
    if sections is None or parse_issues:
        return CodeAIAutonomousIsolatedCandidateApplicationResult(STATUS_BLOCKED, tuple(parse_issues), None, None)
    parsed_changed = [section.path for section in sections]
    parsed_added = [section.path for section in sections if section.operation == "add"]
    parsed_modified = [section.path for section in sections if section.operation == "modify"]
    parsed_deleted = [section.path for section in sections if section.operation == "delete"]
    if policy["require_exact_changed_path_accounting"]:
        if parsed_changed != candidate["changed_paths"]:
            issues.append("changed_path_accounting_mismatch")
        if parsed_added != candidate["added_paths"]:
            issues.append("added_path_accounting_mismatch")
        if parsed_modified != candidate["modified_paths"]:
            issues.append("modified_path_accounting_mismatch")
        if parsed_deleted != candidate["deleted_paths"]:
            issues.append("deleted_path_accounting_mismatch")
    if issues:
        return CodeAIAutonomousIsolatedCandidateApplicationResult(STATUS_BLOCKED, tuple(sorted(set(issues))), None, None)

    result_repository, application_issues = _apply_sections(repository, sections)
    if result_repository is None or application_issues:
        return CodeAIAutonomousIsolatedCandidateApplicationResult(STATUS_BLOCKED, tuple(application_issues), None, None)
    if len(result_repository) > policy["maximum_result_path_count"]:
        issues.append("result_path_count_budget_exceeded")
    if _snapshot_size_bytes(result_repository) > policy["maximum_result_snapshot_bytes"]:
        issues.append("result_snapshot_byte_budget_exceeded")
    if issues:
        return CodeAIAutonomousIsolatedCandidateApplicationResult(STATUS_BLOCKED, tuple(sorted(set(issues))), None, None)

    receipt = _receipt(
        selection_receipt=selection_receipt,
        selected_candidate=parsed_candidate,
        request=request,
        policy=policy,
        source_repository_files=repository,
        resulting_repository_files=result_repository,
    )
    return CodeAIAutonomousIsolatedCandidateApplicationResult(STATUS_READY, (), result_repository, receipt)


__all__ = [name for name in globals() if name.isupper()] + [
    "ParsedPatchSection",
    "CodeAIAutonomousIsolatedCandidateApplicationResult",
    "build_codeai_autonomous_isolated_candidate_application",
]
