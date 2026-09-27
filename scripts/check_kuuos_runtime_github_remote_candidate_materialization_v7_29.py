#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_github_remote_candidate_materialization_v7_29 import (
    ALREADY_PUBLISHED_CI_REOBSERVATION,
    AUTHORITY_REQUIRED,
    BRANCH_PUBLICATION_REQUIRED,
    BRANCH_RESELECTION_REQUIRED,
    MATERIALIZATION_OBSTRUCTION,
    MATERIALIZATION_REQUIRED,
    NOT_APPLICABLE,
    OBSTRUCTED,
    PARTIAL,
    PUBLISHED_BASE_RECONCILIATION,
    PUBLISHED_CI_REOBSERVATION,
    READY,
    build_github_remote_candidate_materialization,
)


def h(value) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


TARGET = "formal/KUOS/Example.lean"
PARENT = "a" * 40
LOCAL_COMMIT = "b" * 40
REMOTE_COMMIT = "c" * 40
TREE_DIGEST = "5" * 64
CONTENT_DIGEST = "3" * 64
MESSAGE_DIGEST = "6" * 64


def source(*, ready: bool = True) -> dict:
    paths = [TARGET]
    return {
        "version": "kuuos_runtime_git_admission_post_commit_coherence_v7_28",
        "status": (
            "KUUOS_GIT_ADMISSION_POST_COMMIT_READY"
            if ready
            else "KUUOS_GIT_ADMISSION_POST_COMMIT_PARTIAL"
        ),
        "packet_id": "post-commit",
        "target_path": TARGET,
        "admission_state": (
            "remote_publish_candidate_ready"
            if ready
            else "remote_publish_candidate_github_authority_required"
        ),
        "candidate_retained": True,
        "local_commit_admitted": True,
        "post_commit_git_fresh": True,
        "post_commit_filesystem_fresh": True,
        "post_commit_lean_fresh": True,
        "post_commit_lean_error_count": 0,
        "remote_revision_aligned": True,
        "remote_publish_candidate": True,
        "remote_publish_ready": ready,
        "next_route": (
            "perform_explicit_authorized_remote_publish_then_exact_head_reobserve"
            if ready
            else "retain_publish_candidate_and_acquire_github_write_authority"
        ),
        "evidence": {
            "source_repair_packet_digest": "1" * 64,
            "git_admission_receipt_digest": "4" * 64,
            "commit_parent_sha": PARENT,
            "commit_sha": LOCAL_COMMIT,
            "commit_tree_digest": TREE_DIGEST,
            "pre_commit_target_content_digest": CONTENT_DIGEST,
            "committed_target_content_digest": CONTENT_DIGEST,
            "post_commit_git_head_sha": LOCAL_COMMIT,
            "post_commit_git_observation_digest": "7" * 64,
            "post_commit_filesystem_content_digest": CONTENT_DIGEST,
            "post_commit_filesystem_observation_digest": "8" * 64,
            "post_commit_lean_source_content_digest": CONTENT_DIGEST,
            "post_commit_lean_diagnostics_digest": "9" * 64,
            "post_commit_lean_observation_digest": "0" * 64,
            "committed_changed_paths_digest": h(paths),
            "supporting_committed_path_count": 0,
            "workspace_write_authority_ready": True,
            "github_write_authority_ready": ready,
            "post_commit_worktree_clean": True,
            "local_commit_admission_is_remote_publish": False,
            "post_commit_semantic_success_grants_github_authority": False,
            "remote_publish_candidate_grants_github_authority": False,
            "raw_source_bytes_persisted": False,
            "raw_git_diff_persisted": False,
            "source_authority_transferred": False,
        },
        "blockers": [],
        "warnings": [],
    }


def observation(
    src: dict,
    *,
    authority: bool = True,
    attempted: bool = True,
    branch_attempted: bool = True,
    branch_absent: bool = True,
    branch_created: bool = True,
    preexisting_head: str = "",
    remote_commit: str = REMOTE_COMMIT,
    remote_blob_digest: str = CONTENT_DIGEST,
    remote_tree_digest: str = TREE_DIGEST,
    remote_message_digest: str = MESSAGE_DIGEST,
    remote_parent: str = PARENT,
    base_after: str = PARENT,
    post_branch_head: str | None = None,
) -> dict:
    if post_branch_head is None:
        post_branch_head = remote_commit if (branch_created or not branch_absent) else ""
    entries = [
        {
            "path": TARGET,
            "mode": "100644",
            "type": "blob",
            "local_content_digest": CONTENT_DIGEST,
            "remote_content_digest": remote_blob_digest,
            "remote_blob_sha": "d" * 40,
        }
    ]
    return {
        "version": "kuuos_github_remote_candidate_materialization_observation_v7_29",
        "source_post_commit_packet_digest": h(src),
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "base_branch": "main",
        "candidate_branch": "automation/repair-example",
        "github_write_authority_ready": authority,
        "external_action_allowed": authority,
        "materialization_attempted": attempted,
        "branch_publication_attempted": branch_attempted,
        "remote_base_before_sha": PARENT,
        "remote_base_tree_sha": "e" * 40,
        "remote_base_observation_digest": "a" * 64,
        "remote_object_materialization_receipt_digest": "b" * 64 if attempted else "",
        "materialized_entries": entries if attempted else [],
        "remote_tree_sha": "f" * 40 if attempted else "",
        "remote_tree_content_digest": remote_tree_digest if attempted else "",
        "local_commit_message_digest": MESSAGE_DIGEST if attempted else "",
        "remote_commit_message_digest": remote_message_digest if attempted else "",
        "remote_commit_sha": remote_commit if attempted else "",
        "remote_commit_parent_sha": remote_parent if attempted else "",
        "remote_object_observation_digest": "c" * 64 if attempted else "",
        "candidate_branch_absent_before": branch_absent,
        "candidate_branch_preexisting_head_sha": preexisting_head,
        "candidate_branch_created": branch_created,
        "post_publish_candidate_branch_head_sha": post_branch_head,
        "post_publish_remote_observation_digest": (
            "d" * 64 if post_branch_head else ""
        ),
        "remote_base_after_sha": base_after if post_branch_head else "",
    }


def test_distinct_remote_commit_identity_can_be_equivalent_publish_candidate() -> None:
    src = source()
    result = build_github_remote_candidate_materialization(
        post_commit_packet=src,
        observation=observation(src),
    )
    assert result.status == READY, result.to_dict()
    assert result.materialization_state == PUBLISHED_CI_REOBSERVATION
    assert result.remote_objects_equivalent is True
    assert result.git_commit_identity_equal is False
    assert result.remote_candidate_published is True
    assert result.remote_base_aligned is True
    assert result.ci_reobservation_required is True
    assert result.merge_candidate is False
    assert result.evidence["commit_presentation_relation"] == (
        "content_parent_message_equivalent_distinct_git_commit_identity"
    )
    assert (
        "remote_commit_sha_differs_from_local_commit_sha_due_to_commit_metadata_surface"
        in result.warnings
    )


def test_exact_git_commit_identity_is_allowed_but_not_required() -> None:
    src = source()
    result = build_github_remote_candidate_materialization(
        post_commit_packet=src,
        observation=observation(src, remote_commit=LOCAL_COMMIT),
    )
    assert result.status == READY
    assert result.git_commit_identity_equal is True
    assert result.evidence["commit_presentation_relation"] == (
        "exact_git_commit_identity"
    )


def test_missing_github_authority_retains_local_candidate() -> None:
    src = source()
    result = build_github_remote_candidate_materialization(
        post_commit_packet=src,
        observation=observation(
            src,
            authority=False,
            attempted=False,
            branch_attempted=False,
            branch_created=False,
        ),
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.materialization_state == AUTHORITY_REQUIRED
    assert result.candidate_retained is True
    assert result.remote_candidate_published is False


def test_authorized_candidate_without_materialization_requests_receipt() -> None:
    src = source()
    result = build_github_remote_candidate_materialization(
        post_commit_packet=src,
        observation=observation(
            src,
            attempted=False,
            branch_attempted=False,
            branch_created=False,
        ),
    )
    assert result.status == PARTIAL
    assert result.materialization_state == MATERIALIZATION_REQUIRED
    assert result.candidate_retained is True


def test_blob_content_mismatch_is_materialization_obstruction() -> None:
    src = source()
    result = build_github_remote_candidate_materialization(
        post_commit_packet=src,
        observation=observation(src, remote_blob_digest="7" * 64),
    )
    assert result.status == OBSTRUCTED
    assert result.materialization_state == MATERIALIZATION_OBSTRUCTION
    assert any(
        item.startswith("materialized_blob_content_digest_mismatch:")
        for item in result.blockers
    )
    assert result.evidence["partial_remote_objects_may_exist"] is True
    assert (
        "unreachable_remote_git_objects_may_exist_even_when_ref_publication_did_not_complete"
        in result.warnings
    )


def test_materialized_objects_can_wait_for_branch_publication() -> None:
    src = source()
    result = build_github_remote_candidate_materialization(
        post_commit_packet=src,
        observation=observation(
            src,
            branch_attempted=False,
            branch_created=False,
            post_branch_head="",
        ),
    )
    assert result.status == PARTIAL
    assert result.materialization_state == BRANCH_PUBLICATION_REQUIRED
    assert result.remote_objects_equivalent is True
    assert result.remote_candidate_published is False


def test_preexisting_conflicting_branch_requests_reselection_not_rematerialization() -> None:
    src = source()
    result = build_github_remote_candidate_materialization(
        post_commit_packet=src,
        observation=observation(
            src,
            branch_attempted=False,
            branch_absent=False,
            branch_created=False,
            preexisting_head="9" * 40,
            post_branch_head="9" * 40,
        ),
    )
    assert result.status == PARTIAL
    assert result.materialization_state == BRANCH_RESELECTION_REQUIRED
    assert result.remote_objects_equivalent is True
    assert result.candidate_retained is True


def test_preexisting_branch_already_at_remote_commit_is_idempotent() -> None:
    src = source()
    result = build_github_remote_candidate_materialization(
        post_commit_packet=src,
        observation=observation(
            src,
            branch_attempted=False,
            branch_absent=False,
            branch_created=False,
            preexisting_head=REMOTE_COMMIT,
            post_branch_head=REMOTE_COMMIT,
        ),
    )
    assert result.status == READY
    assert result.materialization_state == ALREADY_PUBLISHED_CI_REOBSERVATION
    assert result.remote_candidate_published is True
    assert result.merge_candidate is False


def test_base_movement_after_publish_retains_remote_candidate() -> None:
    src = source()
    result = build_github_remote_candidate_materialization(
        post_commit_packet=src,
        observation=observation(src, base_after="8" * 40),
    )
    assert result.status == PARTIAL
    assert result.materialization_state == PUBLISHED_BASE_RECONCILIATION
    assert result.remote_candidate_published is True
    assert result.remote_base_aligned is False
    assert result.candidate_retained is True
    assert result.next_route == (
        "retain_published_candidate_and_reconcile_updated_base"
    )


def test_nonready_v7_28_packet_is_not_applicable() -> None:
    src = source(ready=False)
    result = build_github_remote_candidate_materialization(
        post_commit_packet=src,
        observation=observation(
            src,
            authority=False,
            attempted=False,
            branch_attempted=False,
            branch_created=False,
        ),
    )
    assert result.status == NOT_APPLICABLE
    assert result.next_route == "return_to_v7_28_post_commit_coherence"


def main() -> int:
    test_distinct_remote_commit_identity_can_be_equivalent_publish_candidate()
    test_exact_git_commit_identity_is_allowed_but_not_required()
    test_missing_github_authority_retains_local_candidate()
    test_authorized_candidate_without_materialization_requests_receipt()
    test_blob_content_mismatch_is_materialization_obstruction()
    test_materialized_objects_can_wait_for_branch_publication()
    test_preexisting_conflicting_branch_requests_reselection_not_rematerialization()
    test_preexisting_branch_already_at_remote_commit_is_idempotent()
    test_base_movement_after_publish_retains_remote_candidate()
    test_nonready_v7_28_packet_is_not_applicable()
    print("PASS: KuuOS GitHub Remote Candidate Materialization v7.29")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
