#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import difflib
from typing import Any, Mapping, Sequence

from runtime.kuuos_codeai_candidate_patch_envelope_v0_1 import (
    CANDIDATE_DIGEST_FIELD,
    POLICY_DIGEST_FIELD as CANDIDATE_POLICY_DIGEST_FIELD,
    SOURCE_RECEIPT_DIGEST_FIELD,
    STATUS_READY as CANDIDATE_STATUS_READY,
    build_codeai_candidate_patch_envelope,
    canonical_digest,
    patch_artifact_digest,
    seal,
)

VERSION = "kuuos_codeai_autonomous_unified_diff_candidates_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Autonomous Unified Diff Candidates v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

MODE_PROPOSAL_ONLY = "proposal_only"
DISPOSITION_SYNTHESIZED = "autonomous_unified_diff_candidates_synthesized"
DISPOSITION_NO_SUPPORTED_CANDIDATE = "no_supported_unified_diff_candidate"

RECEIPT_DIGEST_FIELD = "codeai_autonomous_unified_diff_candidates_receipt_digest"

_PROPOSAL_FIELDS = {
    "proposal_id",
    "candidate_revision",
    "producer_id",
    "producer_session_id",
    "candidate_created_epoch",
    "edits",
    "requirement_trace_ids",
    "test_plan_ids",
    "risk_labels",
    "unresolved_candidate_questions",
    "prior_candidate_digests",
    "prior_producer_session_ids",
}

_EDIT_FIELDS = {"path", "operation", "new_content"}
_ALLOWED_OPERATIONS = {"add", "modify", "delete"}


@dataclass(frozen=True)
class GeneratedUnifiedDiffCandidate:
    rank: int
    proposal_id: str
    patch_candidate: dict[str, Any]
    patch_artifact: str
    candidate_receipt: dict[str, Any]


@dataclass(frozen=True)
class CodeAIAutonomousUnifiedDiffCandidatesResult:
    status: str
    issues: tuple[str, ...]
    candidates: tuple[GeneratedUnifiedDiffCandidate, ...]
    receipt: dict[str, Any] | None


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _nat(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _string_list(value: Any) -> list[str] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return None
    return value


def _nonempty_unique_strings(value: Any) -> bool:
    parsed = _string_list(value)
    return (
        parsed is not None
        and all(parsed)
        and len(parsed) == len(set(parsed))
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
        and all(segment not in ("", ".", "..") for segment in segments)
    )


def _canonical_text(value: Any) -> bool:
    return (
        isinstance(value, str)
        and "\0" not in value
        and "\r" not in value
        and (not value or value.endswith("\n"))
    )


def _validate_repository_files(repository_files: Any) -> tuple[Mapping[str, str] | None, list[str]]:
    repository = _mapping(repository_files)
    if repository is None:
        return None, ["repository_files_not_mapping"]
    issues: list[str] = []
    for path, content in repository.items():
        if not isinstance(path, str) or not _canonical_repository_path(path):
            issues.append("repository_file_path_invalid")
        if not _canonical_text(content):
            issues.append("repository_file_content_invalid:" + str(path))
    return repository, issues


def _validate_proposals(proposals: Any) -> tuple[list[Mapping[str, Any]] | None, list[str]]:
    if not isinstance(proposals, list) or not proposals:
        return None, ["proposals_not_nonempty_list"]
    issues: list[str] = []
    parsed: list[Mapping[str, Any]] = []
    proposal_ids: set[str] = set()
    session_ids: set[str] = set()
    for index, raw in enumerate(proposals):
        proposal = _mapping(raw)
        prefix = f"proposal[{index}]"
        if proposal is None:
            issues.append(prefix + ":not_mapping")
            continue
        missing = _PROPOSAL_FIELDS.difference(proposal)
        extra = set(proposal).difference(_PROPOSAL_FIELDS)
        if missing:
            issues.append(prefix + ":missing_fields:" + ",".join(sorted(missing)))
            continue
        if extra:
            issues.append(prefix + ":extra_fields:" + ",".join(sorted(extra)))
            continue
        for field in (
            "proposal_id",
            "candidate_revision",
            "producer_id",
            "producer_session_id",
        ):
            if not isinstance(proposal[field], str) or not proposal[field]:
                issues.append(prefix + ":invalid_string:" + field)
        if _nat(proposal["candidate_created_epoch"]) is None:
            issues.append(prefix + ":invalid_candidate_created_epoch")
        for field in (
            "requirement_trace_ids",
            "test_plan_ids",
            "risk_labels",
            "unresolved_candidate_questions",
            "prior_candidate_digests",
            "prior_producer_session_ids",
        ):
            if not _nonempty_unique_strings(proposal[field]):
                issues.append(prefix + ":invalid_string_list:" + field)
        proposal_id = proposal["proposal_id"]
        session_id = proposal["producer_session_id"]
        if isinstance(proposal_id, str):
            if proposal_id in proposal_ids:
                issues.append(prefix + ":duplicate_proposal_id")
            proposal_ids.add(proposal_id)
        if isinstance(session_id, str):
            if session_id in session_ids:
                issues.append(prefix + ":duplicate_producer_session_id")
            session_ids.add(session_id)
        edits = proposal["edits"]
        if not isinstance(edits, list) or not edits:
            issues.append(prefix + ":edits_not_nonempty_list")
            continue
        paths: set[str] = set()
        for edit_index, raw_edit in enumerate(edits):
            edit = _mapping(raw_edit)
            edit_prefix = f"{prefix}.edit[{edit_index}]"
            if edit is None:
                issues.append(edit_prefix + ":not_mapping")
                continue
            missing_edit = _EDIT_FIELDS.difference(edit)
            extra_edit = set(edit).difference(_EDIT_FIELDS)
            if missing_edit:
                issues.append(edit_prefix + ":missing_fields:" + ",".join(sorted(missing_edit)))
                continue
            if extra_edit:
                issues.append(edit_prefix + ":extra_fields:" + ",".join(sorted(extra_edit)))
                continue
            path = edit["path"]
            operation = edit["operation"]
            new_content = edit["new_content"]
            if not isinstance(path, str) or not _canonical_repository_path(path):
                issues.append(edit_prefix + ":path_invalid")
            elif path in paths:
                issues.append(edit_prefix + ":path_repeated")
            else:
                paths.add(path)
            if operation not in _ALLOWED_OPERATIONS:
                issues.append(edit_prefix + ":operation_invalid")
            if operation == "delete":
                if new_content is not None:
                    issues.append(edit_prefix + ":delete_new_content_must_be_null")
            elif not _canonical_text(new_content):
                issues.append(edit_prefix + ":new_content_invalid")
        parsed.append(proposal)
    return parsed, issues


def _unified_body(old_label: str, new_label: str, old_content: str, new_content: str) -> str:
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()
    lines = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=old_label,
            tofile=new_label,
            lineterm="",
        )
    )
    return "\n".join(lines) + ("\n" if lines else "")


def render_unified_diff(
    repository_files: Mapping[str, str], edits: Sequence[Mapping[str, Any]]
) -> tuple[str | None, dict[str, list[str]] | None, tuple[str, ...]]:
    issues: list[str] = []
    sections: list[tuple[str, str]] = []
    added: list[str] = []
    modified: list[str] = []
    deleted: list[str] = []

    for edit in sorted(edits, key=lambda item: str(item["path"])):
        path = str(edit["path"])
        operation = str(edit["operation"])
        new_content = edit["new_content"]
        exists = path in repository_files
        if operation == "add":
            if exists:
                issues.append("add_path_already_exists:" + path)
                continue
            assert isinstance(new_content, str)
            body = _unified_body("/dev/null", "b/" + path, "", new_content)
            section = (
                f"diff --git a/{path} b/{path}\n"
                "new file mode 100644\n"
                + body
            )
            added.append(path)
        elif operation == "modify":
            if not exists:
                issues.append("modify_path_missing:" + path)
                continue
            assert isinstance(new_content, str)
            old_content = repository_files[path]
            if old_content == new_content:
                issues.append("modify_has_no_change:" + path)
                continue
            body = _unified_body("a/" + path, "b/" + path, old_content, new_content)
            section = f"diff --git a/{path} b/{path}\n" + body
            modified.append(path)
        elif operation == "delete":
            if not exists:
                issues.append("delete_path_missing:" + path)
                continue
            old_content = repository_files[path]
            body = _unified_body("a/" + path, "/dev/null", old_content, "")
            section = (
                f"diff --git a/{path} b/{path}\n"
                "deleted file mode 100644\n"
                + body
            )
            deleted.append(path)
        else:
            issues.append("operation_invalid:" + path)
            continue
        sections.append((path, section))

    if issues:
        return None, None, tuple(sorted(set(issues)))
    artifact = "".join(section for _, section in sorted(sections))
    if not artifact.endswith("\n"):
        artifact += "\n"
    shape = {
        "changed_paths": sorted(added + modified + deleted),
        "added_paths": sorted(added),
        "modified_paths": sorted(modified),
        "deleted_paths": sorted(deleted),
    }
    return artifact, shape, ()


def _build_patch_candidate(
    *,
    source_observation_receipt: Mapping[str, Any],
    proposal: Mapping[str, Any],
    patch_artifact: str,
    shape: Mapping[str, list[str]],
) -> dict[str, Any]:
    candidate = {
        "candidate_id": proposal["proposal_id"],
        "candidate_revision": proposal["candidate_revision"],
        "producer_id": proposal["producer_id"],
        "producer_session_id": proposal["producer_session_id"],
        "source_observation_receipt_digest": source_observation_receipt[
            SOURCE_RECEIPT_DIGEST_FIELD
        ],
        "intent_packet_digest": source_observation_receipt["intent_packet_digest"],
        "repository_full_name": source_observation_receipt["repository_full_name"],
        "source_commit_sha": source_observation_receipt["source_commit_sha"],
        "patch_format": "unified_diff",
        "patch_artifact_digest": patch_artifact_digest(patch_artifact),
        "patch_size_bytes": len(patch_artifact.encode("utf-8")),
        "changed_paths": shape["changed_paths"],
        "added_paths": shape["added_paths"],
        "modified_paths": shape["modified_paths"],
        "deleted_paths": shape["deleted_paths"],
        "renamed_from_paths": [],
        "renamed_to_paths": [],
        "declared_change_count": len(shape["changed_paths"]),
        "requirement_trace_ids": proposal["requirement_trace_ids"],
        "test_plan_ids": proposal["test_plan_ids"],
        "risk_labels": proposal["risk_labels"],
        "unresolved_candidate_questions": proposal[
            "unresolved_candidate_questions"
        ],
        "candidate_created_epoch": proposal["candidate_created_epoch"],
        "prior_candidate_digests": proposal["prior_candidate_digests"],
        "prior_producer_session_ids": proposal["prior_producer_session_ids"],
        "candidate_provenance_confirmed": True,
        "binary_patch_present": False,
        "submodule_patch_present": False,
        "mode_change_present": False,
        # This field belongs to the downstream Candidate Patch kernel. The
        # candidate is generated here, not by that kernel.
        "candidate_generated_by_kernel": False,
        "patch_applied_by_kernel": False,
        "repository_files_changed_by_kernel": False,
        "git_ref_changed_by_kernel": False,
        "branch_created_by_kernel": False,
        "commit_created_by_kernel": False,
        "push_performed_by_kernel": False,
        "pull_request_created_by_kernel": False,
        "external_side_effect_performed_by_kernel": False,
        "selection_authority_claimed": False,
        "execution_authority_claimed": False,
        "merge_authority_claimed": False,
        "deployment_authority_claimed": False,
        "secret_access_authority_claimed": False,
    }
    return seal(candidate, CANDIDATE_DIGEST_FIELD)


def _rank_key(item: tuple[dict[str, Any], str, dict[str, Any]]) -> tuple[int, int, int, str]:
    candidate, artifact, _ = item
    return (
        len(candidate["changed_paths"]),
        len(artifact.encode("utf-8")),
        len(candidate["risk_labels"]),
        candidate["candidate_id"],
    )


def _receipt(
    *,
    source_observation_receipt: Mapping[str, Any],
    repository_files: Mapping[str, str],
    proposals: Sequence[Mapping[str, Any]],
    candidate_policy: Mapping[str, Any],
    accepted: Sequence[tuple[dict[str, Any], str, dict[str, Any]]],
    rejection_issues: Sequence[str],
) -> dict[str, Any]:
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_observation_receipt_digest": source_observation_receipt[
            SOURCE_RECEIPT_DIGEST_FIELD
        ],
        "candidate_policy_digest": candidate_policy[CANDIDATE_POLICY_DIGEST_FIELD],
        "repository_snapshot_digest": canonical_digest(repository_files),
        "proposal_set_digest": canonical_digest(proposals),
        "generated_candidate_count": len(accepted),
        "generated_candidate_ids": [item[0]["candidate_id"] for item in accepted],
        "generated_candidate_digests": [item[0][CANDIDATE_DIGEST_FIELD] for item in accepted],
        "generated_patch_artifact_digests": [item[0]["patch_artifact_digest"] for item in accepted],
        "rejected_proposal_count": len(rejection_issues),
        "rejection_issues": list(rejection_issues),
        "codeai_disposition": (
            DISPOSITION_SYNTHESIZED if accepted else DISPOSITION_NO_SUPPORTED_CANDIDATE
        ),
        "operating_mode": MODE_PROPOSAL_ONLY,
        "route_receipt_recorded": True,
        "repository_snapshot_read_only": True,
        "structured_edits_consumed": True,
        "unified_diff_candidates_generated_by_kernel": bool(accepted),
        "candidate_ranking_generated_by_kernel": bool(accepted),
        "candidate_selected": False,
        "verification_lease_issued": False,
        "execution_lease_issued": False,
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
        "selection_authority_granted": False,
        "verification_authority_granted": False,
        "execution_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "secret_access_authority_granted": False,
        "generated_candidate_treated_as_correct": False,
        "validation_treated_as_correctness_proof": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    return seal(receipt, RECEIPT_DIGEST_FIELD)


def build_codeai_autonomous_unified_diff_candidates(
    *,
    source_observation_receipt: Any,
    repository_files: Any,
    proposals: Any,
    candidate_policy: Any,
) -> CodeAIAutonomousUnifiedDiffCandidatesResult:
    source = _mapping(source_observation_receipt)
    policy = _mapping(candidate_policy)
    repository, repository_issues = _validate_repository_files(repository_files)
    parsed_proposals, proposal_issues = _validate_proposals(proposals)
    issues: list[str] = []
    if source is None:
        issues.append("source_observation_receipt_not_mapping")
    if policy is None:
        issues.append("candidate_policy_not_mapping")
    issues.extend(repository_issues)
    issues.extend(proposal_issues)
    if issues or source is None or policy is None or repository is None or parsed_proposals is None:
        return CodeAIAutonomousUnifiedDiffCandidatesResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), (), None
        )

    accepted: list[tuple[dict[str, Any], str, dict[str, Any]]] = []
    rejection_issues: list[str] = []
    for proposal in parsed_proposals:
        artifact, shape, render_issues = render_unified_diff(
            repository, proposal["edits"]
        )
        if render_issues or artifact is None or shape is None:
            rejection_issues.extend(
                f"{proposal['proposal_id']}:{issue}" for issue in render_issues
            )
            continue
        candidate = _build_patch_candidate(
            source_observation_receipt=source,
            proposal=proposal,
            patch_artifact=artifact,
            shape=shape,
        )
        validation = build_codeai_candidate_patch_envelope(
            source_observation_receipt=source,
            patch_candidate=candidate,
            patch_artifact=artifact,
            candidate_policy=policy,
        )
        if validation.status != CANDIDATE_STATUS_READY or validation.receipt is None:
            rejection_issues.extend(
                f"{proposal['proposal_id']}:candidate_preflight:{issue}"
                for issue in validation.issues
            )
            continue
        if validation.receipt.get("candidate_patch_ready") is not True:
            rejection_issues.append(
                f"{proposal['proposal_id']}:candidate_route:"
                + str(validation.receipt.get("codeai_disposition"))
            )
            continue
        accepted.append((candidate, artifact, validation.receipt))

    accepted.sort(key=_rank_key)
    generated = tuple(
        GeneratedUnifiedDiffCandidate(
            rank=index + 1,
            proposal_id=item[0]["candidate_id"],
            patch_candidate=item[0],
            patch_artifact=item[1],
            candidate_receipt=item[2],
        )
        for index, item in enumerate(accepted)
    )
    receipt = _receipt(
        source_observation_receipt=source,
        repository_files=repository,
        proposals=parsed_proposals,
        candidate_policy=policy,
        accepted=accepted,
        rejection_issues=rejection_issues,
    )
    status = STATUS_READY if accepted else STATUS_BLOCKED
    return CodeAIAutonomousUnifiedDiffCandidatesResult(
        status,
        tuple(rejection_issues),
        generated,
        receipt,
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIAutonomousUnifiedDiffCandidatesResult",
    "GeneratedUnifiedDiffCandidate",
    "build_codeai_autonomous_unified_diff_candidates",
    "render_unified_diff",
]
