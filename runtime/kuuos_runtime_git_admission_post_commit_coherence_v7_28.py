#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_runtime_git_admission_post_commit_coherence_v7_28"
REPAIR_VERSION = "kuuos_runtime_bounded_lean_repair_loop_v7_27"
OBSERVATION_VERSION = "kuuos_git_admission_post_commit_observation_v7_28"

READY = "KUUOS_GIT_ADMISSION_POST_COMMIT_READY"
PARTIAL = "KUUOS_GIT_ADMISSION_POST_COMMIT_PARTIAL"
OBSTRUCTED = "KUUOS_GIT_ADMISSION_POST_COMMIT_OBSTRUCTED"
NOT_APPLICABLE = "KUUOS_GIT_ADMISSION_POST_COMMIT_NOT_APPLICABLE"

WORKSPACE_AUTHORITY_REQUIRED = "git_admission_workspace_authority_required"
COMMIT_RECEIPT_REQUIRED = "git_commit_receipt_required"
COMMIT_LINEAGE_OBSTRUCTION = "git_commit_lineage_obstruction"
POST_COMMIT_REOBSERVATION = "post_commit_cross_surface_reobservation_required"
POST_COMMIT_LEAN_REGRESSION = "post_commit_lean_semantic_regression"
REMOTE_REVISION_RECONCILIATION = "remote_revision_reconciliation_required_after_local_commit"
REMOTE_PUBLISH_AUTHORITY_REQUIRED = "remote_publish_candidate_github_authority_required"
REMOTE_PUBLISH_READY = "remote_publish_candidate_ready"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class GitAdmissionPostCommitResult:
    version: str
    status: str
    packet_id: str
    target_path: str
    admission_state: str
    candidate_retained: bool
    local_commit_admitted: bool
    post_commit_git_fresh: bool
    post_commit_filesystem_fresh: bool
    post_commit_lean_fresh: bool
    post_commit_lean_error_count: int
    remote_revision_aligned: bool
    remote_publish_candidate: bool
    remote_publish_ready: bool
    next_route: str
    evidence: dict[str, Any]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _digest(
    value: Any,
    name: str,
    blockers: list[str],
    *,
    optional: bool = False,
) -> str:
    text = str(value or "").strip()
    if optional and not text:
        return ""
    if SHA64.fullmatch(text) is None:
        blockers.append(name + "_invalid")
    return text


def _commit(
    value: Any,
    name: str,
    blockers: list[str],
    *,
    optional: bool = False,
) -> str:
    text = str(value or "").strip()
    if optional and not text:
        return ""
    if SHA40.fullmatch(text) is None:
        blockers.append(name + "_invalid")
    return text


def _bool(value: Any, name: str, blockers: list[str]) -> bool:
    if not isinstance(value, bool):
        blockers.append(name + "_must_be_bool")
        return False
    return value


def _nonnegative_int(value: Any, name: str, blockers: list[str]) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        blockers.append(name + "_invalid")
        return 0
    return value


def _paths(value: Any, blockers: list[str]) -> list[str]:
    if not isinstance(value, list):
        blockers.append("committed_changed_paths_not_list")
        return []
    out: list[str] = []
    for raw in value:
        path = str(raw).strip()
        if not path:
            blockers.append("committed_changed_path_empty")
            continue
        if path not in out:
            out.append(path)
    return out


def build_git_admission_post_commit_coherence(
    *,
    repair_packet: Mapping[str, Any],
    observation: Mapping[str, Any],
) -> GitAdmissionPostCommitResult:
    repair = _m(repair_packet)
    obs = _m(observation)
    blockers: list[str] = []
    warnings: list[str] = []

    if repair.get("version") != REPAIR_VERSION:
        blockers.append("repair_packet_version_invalid")
    if obs.get("version") != OBSERVATION_VERSION:
        blockers.append("observation_version_invalid")

    target_path = str(repair.get("target_path", "")).strip()
    observed_target = str(obs.get("target_path", "")).strip()
    if not target_path:
        blockers.append("repair_target_path_missing")
    if observed_target != target_path:
        blockers.append("observation_target_path_mismatch")

    repair_digest = _sha(repair)
    source_repair_digest = _digest(
        obs.get("source_repair_packet_digest"),
        "source_repair_packet_digest",
        blockers,
    )
    if source_repair_digest != repair_digest:
        blockers.append("source_repair_packet_digest_mismatch")

    candidate_retained = bool(repair.get("candidate_retained"))
    git_admission_ready = repair.get("git_admission_ready") is True

    if repair.get("repair_state") == "repair_locally_verified_git_admission_ready":
        if not git_admission_ready:
            blockers.append("repair_state_and_git_admission_ready_disagree")

    if not git_admission_ready:
        packet_id = "kuuos-git-admission-post-commit-" + _sha(
            {
                "repair_packet_digest": repair_digest,
                "target_path": target_path,
                "state": "not_applicable",
                "blockers": sorted(set(blockers)),
            }
        )[:16]
        return GitAdmissionPostCommitResult(
            VERSION,
            OBSTRUCTED if blockers else NOT_APPLICABLE,
            packet_id,
            target_path,
            "repair_not_git_admission_ready",
            candidate_retained,
            False,
            False,
            False,
            False,
            0,
            False,
            False,
            False,
            "return_to_bounded_lean_repair_loop",
            {
                "source_repair_packet_digest": repair_digest,
                "source_authority_transferred": False,
            },
            sorted(set(blockers)),
            warnings,
        )

    workspace_authority = _bool(
        obs.get("workspace_write_authority_ready"),
        "workspace_write_authority_ready",
        blockers,
    )
    github_authority = _bool(
        obs.get("github_write_authority_ready"),
        "github_write_authority_ready",
        blockers,
    )

    commit_created = _bool(
        obs.get("commit_created"),
        "commit_created",
        blockers,
    )
    receipt_digest = _digest(
        obs.get("git_admission_receipt_digest"),
        "git_admission_receipt_digest",
        blockers,
        optional=not commit_created,
    )

    parent_sha = _commit(
        obs.get("commit_parent_sha"),
        "commit_parent_sha",
        blockers,
        optional=not commit_created,
    )
    commit_sha = _commit(
        obs.get("commit_sha"),
        "commit_sha",
        blockers,
        optional=not commit_created,
    )
    remote_head = _commit(
        obs.get("current_github_remote_head_sha"),
        "current_github_remote_head_sha",
        blockers,
    )
    post_commit_git_head = _commit(
        obs.get("post_commit_git_head_sha"),
        "post_commit_git_head_sha",
        blockers,
        optional=not commit_created,
    )

    pre_commit_target_digest = _digest(
        obs.get("pre_commit_target_content_digest"),
        "pre_commit_target_content_digest",
        blockers,
        optional=not commit_created,
    )
    committed_target_digest = _digest(
        obs.get("committed_target_content_digest"),
        "committed_target_content_digest",
        blockers,
        optional=not commit_created,
    )
    commit_tree_digest = _digest(
        obs.get("commit_tree_digest"),
        "commit_tree_digest",
        blockers,
        optional=not commit_created,
    )

    fs_path = str(obs.get("post_commit_filesystem_path", "")).strip()
    fs_content_digest = _digest(
        obs.get("post_commit_filesystem_content_digest"),
        "post_commit_filesystem_content_digest",
        blockers,
        optional=not commit_created,
    )
    fs_observation_digest = _digest(
        obs.get("post_commit_filesystem_observation_digest"),
        "post_commit_filesystem_observation_digest",
        blockers,
        optional=not commit_created,
    )

    lean_path = str(obs.get("post_commit_lean_path", "")).strip()
    lean_source_digest = _digest(
        obs.get("post_commit_lean_source_content_digest"),
        "post_commit_lean_source_content_digest",
        blockers,
        optional=not commit_created,
    )
    lean_diagnostics_digest = _digest(
        obs.get("post_commit_lean_diagnostics_digest"),
        "post_commit_lean_diagnostics_digest",
        blockers,
        optional=not commit_created,
    )
    lean_observation_digest = _digest(
        obs.get("post_commit_lean_observation_digest"),
        "post_commit_lean_observation_digest",
        blockers,
        optional=not commit_created,
    )
    lean_error_count = _nonnegative_int(
        obs.get("post_commit_lean_error_count"),
        "post_commit_lean_error_count",
        blockers,
    )

    git_observation_digest = _digest(
        obs.get("post_commit_git_observation_digest"),
        "post_commit_git_observation_digest",
        blockers,
        optional=not commit_created,
    )
    post_commit_worktree_clean = _bool(
        obs.get("post_commit_worktree_clean"),
        "post_commit_worktree_clean",
        blockers,
    )
    changed_paths = _paths(
        obs.get("committed_changed_paths", []),
        blockers,
    )

    repair_evidence = _m(repair.get("evidence"))
    repaired_post_edit_digest = _digest(
        repair_evidence.get("post_edit_content_digest"),
        "repair_post_edit_content_digest",
        blockers,
    )
    repaired_git_diff_target_digest = _digest(
        repair_evidence.get("git_diff_target_post_content_digest"),
        "repair_git_diff_target_post_content_digest",
        blockers,
    )

    if workspace_authority is False:
        state = WORKSPACE_AUTHORITY_REQUIRED
        status = PARTIAL if not blockers else OBSTRUCTED
        next_route = "retain_candidate_and_acquire_workspace_git_authority"
        local_commit_admitted = False
        post_commit_git_fresh = False
        post_commit_filesystem_fresh = False
        post_commit_lean_fresh = False
        remote_revision_aligned = False
        remote_publish_candidate = False
        remote_publish_ready = False
    elif not commit_created:
        state = COMMIT_RECEIPT_REQUIRED
        status = PARTIAL if not blockers else OBSTRUCTED
        next_route = "perform_authorized_local_git_admission_then_emit_commit_receipt"
        local_commit_admitted = False
        post_commit_git_fresh = False
        post_commit_filesystem_fresh = False
        post_commit_lean_fresh = False
        remote_revision_aligned = False
        remote_publish_candidate = False
        remote_publish_ready = False
    else:
        if not receipt_digest:
            blockers.append("git_admission_receipt_digest_missing")
        if parent_sha == commit_sha:
            blockers.append("commit_sha_equals_parent_sha")
        if pre_commit_target_digest != repaired_post_edit_digest:
            blockers.append("commit_preimage_does_not_match_v7_27_post_edit_bytes")
        if committed_target_digest != repaired_post_edit_digest:
            blockers.append("committed_target_does_not_match_v7_27_post_edit_bytes")
        if committed_target_digest != repaired_git_diff_target_digest:
            blockers.append("committed_target_does_not_match_v7_27_git_diff_target")
        if target_path not in changed_paths:
            blockers.append("target_path_missing_from_committed_changed_paths")
        if fs_path != target_path:
            blockers.append("post_commit_filesystem_target_path_mismatch")
        if lean_path != target_path:
            blockers.append("post_commit_lean_target_path_mismatch")

        local_commit_admitted = not blockers
        post_commit_git_fresh = bool(
            commit_sha
            and post_commit_git_head
            and post_commit_git_head == commit_sha
            and git_observation_digest
        )
        post_commit_filesystem_fresh = bool(
            fs_content_digest
            and committed_target_digest
            and fs_content_digest == committed_target_digest
            and fs_observation_digest
        )
        post_commit_lean_fresh = bool(
            lean_source_digest
            and fs_content_digest
            and lean_source_digest == fs_content_digest
            and lean_observation_digest
            and lean_diagnostics_digest
        )
        remote_revision_aligned = bool(parent_sha and remote_head and parent_sha == remote_head)

        if not post_commit_worktree_clean:
            warnings.append(
                "post_commit_worktree_dirty_elsewhere_does_not_invalidate_committed_target"
            )
        supporting_paths = [path for path in changed_paths if path != target_path]
        if supporting_paths:
            warnings.append("supporting_committed_paths_present_review_before_remote_publish")

        if blockers:
            state = COMMIT_LINEAGE_OBSTRUCTION
            status = OBSTRUCTED
            next_route = "reestablish_git_admission_from_v7_27_verified_bytes"
            remote_publish_candidate = False
            remote_publish_ready = False
        elif not (
            post_commit_git_fresh
            and post_commit_filesystem_fresh
            and post_commit_lean_fresh
        ):
            state = POST_COMMIT_REOBSERVATION
            status = PARTIAL
            next_route = "reobserve_post_commit_git_filesystem_and_lean_surfaces"
            remote_publish_candidate = False
            remote_publish_ready = False
        elif lean_error_count > 0:
            state = POST_COMMIT_LEAN_REGRESSION
            status = PARTIAL
            next_route = "retain_local_commit_and_reenter_repair_from_post_commit_bytes"
            remote_publish_candidate = False
            remote_publish_ready = False
            warnings.append("post_commit_lean_errors_detected_after_precommit_success")
        elif not remote_revision_aligned:
            state = REMOTE_REVISION_RECONCILIATION
            status = PARTIAL
            next_route = "retain_local_commit_and_reconcile_remote_base_before_publish"
            remote_publish_candidate = False
            remote_publish_ready = False
        else:
            remote_publish_candidate = True
            if github_authority:
                state = REMOTE_PUBLISH_READY
                status = READY
                next_route = "perform_explicit_authorized_remote_publish_then_exact_head_reobserve"
                remote_publish_ready = True
            else:
                state = REMOTE_PUBLISH_AUTHORITY_REQUIRED
                status = PARTIAL
                next_route = "retain_publish_candidate_and_acquire_github_write_authority"
                remote_publish_ready = False

    evidence = {
        "source_repair_packet_digest": repair_digest,
        "git_admission_receipt_digest": receipt_digest,
        "commit_parent_sha": parent_sha,
        "commit_sha": commit_sha,
        "commit_tree_digest": commit_tree_digest,
        "pre_commit_target_content_digest": pre_commit_target_digest,
        "committed_target_content_digest": committed_target_digest,
        "post_commit_git_head_sha": post_commit_git_head,
        "post_commit_git_observation_digest": git_observation_digest,
        "post_commit_filesystem_content_digest": fs_content_digest,
        "post_commit_filesystem_observation_digest": fs_observation_digest,
        "post_commit_lean_source_content_digest": lean_source_digest,
        "post_commit_lean_diagnostics_digest": lean_diagnostics_digest,
        "post_commit_lean_observation_digest": lean_observation_digest,
        "committed_changed_paths_digest": _sha(changed_paths),
        "supporting_committed_path_count": len(
            [path for path in changed_paths if path != target_path]
        ),
        "workspace_write_authority_ready": workspace_authority,
        "github_write_authority_ready": github_authority,
        "post_commit_worktree_clean": post_commit_worktree_clean,
        "local_commit_admission_is_remote_publish": False,
        "post_commit_semantic_success_grants_github_authority": False,
        "remote_publish_candidate_grants_github_authority": False,
        "raw_source_bytes_persisted": False,
        "raw_git_diff_persisted": False,
        "source_authority_transferred": False,
    }

    packet_id = "kuuos-git-admission-post-commit-" + _sha(
        {
            "source_repair_packet_digest": repair_digest,
            "target_path": target_path,
            "state": state,
            "evidence": evidence,
            "blockers": sorted(set(blockers)),
            "warnings": sorted(set(warnings)),
        }
    )[:16]

    return GitAdmissionPostCommitResult(
        VERSION,
        status,
        packet_id,
        target_path,
        state,
        True,
        local_commit_admitted,
        post_commit_git_fresh,
        post_commit_filesystem_fresh,
        post_commit_lean_fresh,
        lean_error_count,
        remote_revision_aligned,
        remote_publish_candidate,
        remote_publish_ready,
        next_route,
        evidence,
        sorted(set(blockers)),
        sorted(set(warnings)),
    )
