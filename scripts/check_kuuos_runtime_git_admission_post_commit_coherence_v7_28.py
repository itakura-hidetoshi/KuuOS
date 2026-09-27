#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_git_admission_post_commit_coherence_v7_28 import (
    COMMIT_LINEAGE_OBSTRUCTION,
    COMMIT_RECEIPT_REQUIRED,
    NOT_APPLICABLE,
    OBSTRUCTED,
    PARTIAL,
    POST_COMMIT_LEAN_REGRESSION,
    POST_COMMIT_REOBSERVATION,
    READY,
    REMOTE_PUBLISH_AUTHORITY_REQUIRED,
    REMOTE_PUBLISH_READY,
    REMOTE_REVISION_RECONCILIATION,
    WORKSPACE_AUTHORITY_REQUIRED,
    build_git_admission_post_commit_coherence,
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


def repair(*, ready: bool = True) -> dict:
    return {
        "version": "kuuos_runtime_bounded_lean_repair_loop_v7_27",
        "status": (
            "KUUOS_BOUNDED_LEAN_REPAIR_LOOP_READY"
            if ready
            else "KUUOS_BOUNDED_LEAN_REPAIR_LOOP_PARTIAL"
        ),
        "packet_id": "repair-packet",
        "target_path": "formal/KUOS/Example.lean",
        "iteration_index": 1,
        "max_iterations": 4,
        "repair_state": (
            "repair_locally_verified_git_admission_ready"
            if ready
            else "post_edit_lean_errors_remain"
        ),
        "candidate_retained": True,
        "full_file_audit_bound": True,
        "edit_effect_observed": True,
        "lean_semantic_fresh": True,
        "lean_error_count": 0 if ready else 1,
        "git_diff_fresh": True,
        "local_repair_verified": ready,
        "git_admission_ready": ready,
        "remote_publish_ready": False,
        "next_route": (
            "prepare_git_admission_then_post_commit_reobservation"
            if ready
            else "continue_bounded_repair_from_current_post_edit_bytes"
        ),
        "evidence": {
            "repair_scope": "entire_target_file",
            "full_file_audit_digest": "a" * 64,
            "edit_receipt_digest": "b" * 64,
            "pre_edit_content_digest": "1" * 64,
            "post_edit_content_digest": "3" * 64,
            "filesystem_observation_digest": "c" * 64,
            "lean_source_content_digest": "3" * 64,
            "lean_diagnostics_digest": "d" * 64,
            "git_diff_digest": "e" * 64,
            "git_diff_target_post_content_digest": "3" * 64,
            "git_changed_paths_digest": "f" * 64,
            "supporting_changed_path_count": 0,
            "full_target_file_audit_required": True,
            "ci_error_line_is_locator_not_scope": True,
            "raw_source_bytes_persisted": False,
            "raw_git_diff_persisted": False,
            "repair_budget_is_semantic_truth": False,
            "budget_exhaustion_is_rejection": False,
            "source_authority_transferred": False,
        },
        "blockers": [],
        "warnings": [],
    }


def observation(
    repair_packet: dict,
    *,
    workspace: bool = True,
    github: bool = True,
    commit_created: bool = True,
    parent: str = "a" * 40,
    commit: str = "b" * 40,
    remote_head: str | None = None,
    git_head: str | None = None,
    pre: str = "3" * 64,
    committed: str = "3" * 64,
    fs: str = "3" * 64,
    lean: str = "3" * 64,
    lean_errors: int = 0,
    fs_path: str = "formal/KUOS/Example.lean",
    lean_path: str = "formal/KUOS/Example.lean",
    clean: bool = True,
    changed_paths: list[str] | None = None,
    include_post_observations: bool = True,
) -> dict:
    if remote_head is None:
        remote_head = parent
    if git_head is None:
        git_head = commit
    if changed_paths is None:
        changed_paths = ["formal/KUOS/Example.lean"]

    return {
        "version": "kuuos_git_admission_post_commit_observation_v7_28",
        "source_repair_packet_digest": h(repair_packet),
        "target_path": "formal/KUOS/Example.lean",
        "workspace_write_authority_ready": workspace,
        "github_write_authority_ready": github,
        "commit_created": commit_created,
        "git_admission_receipt_digest": "4" * 64 if commit_created else "",
        "commit_parent_sha": parent if commit_created else "",
        "commit_sha": commit if commit_created else "",
        "current_github_remote_head_sha": remote_head,
        "post_commit_git_head_sha": git_head if commit_created else "",
        "pre_commit_target_content_digest": pre if commit_created else "",
        "committed_target_content_digest": committed if commit_created else "",
        "commit_tree_digest": "5" * 64 if commit_created else "",
        "committed_changed_paths": changed_paths if commit_created else [],
        "post_commit_git_observation_digest": (
            "6" * 64 if commit_created and include_post_observations else ""
        ),
        "post_commit_worktree_clean": clean,
        "post_commit_filesystem_path": fs_path if commit_created else "",
        "post_commit_filesystem_content_digest": (
            fs if commit_created and include_post_observations else ""
        ),
        "post_commit_filesystem_observation_digest": (
            "7" * 64 if commit_created and include_post_observations else ""
        ),
        "post_commit_lean_path": lean_path if commit_created else "",
        "post_commit_lean_source_content_digest": (
            lean if commit_created and include_post_observations else ""
        ),
        "post_commit_lean_diagnostics_digest": (
            "8" * 64 if commit_created and include_post_observations else ""
        ),
        "post_commit_lean_observation_digest": (
            "9" * 64 if commit_created and include_post_observations else ""
        ),
        "post_commit_lean_error_count": lean_errors,
    }


def test_coherent_commit_with_github_authority_is_remote_publish_ready() -> None:
    r = repair()
    result = build_git_admission_post_commit_coherence(
        repair_packet=r,
        observation=observation(r),
    )
    assert result.status == READY, result.to_dict()
    assert result.admission_state == REMOTE_PUBLISH_READY
    assert result.local_commit_admitted is True
    assert result.post_commit_git_fresh is True
    assert result.post_commit_filesystem_fresh is True
    assert result.post_commit_lean_fresh is True
    assert result.remote_revision_aligned is True
    assert result.remote_publish_candidate is True
    assert result.remote_publish_ready is True
    assert result.next_route == (
        "perform_explicit_authorized_remote_publish_then_exact_head_reobserve"
    )


def test_missing_github_authority_retains_remote_publish_candidate() -> None:
    r = repair()
    result = build_git_admission_post_commit_coherence(
        repair_packet=r,
        observation=observation(r, github=False),
    )
    assert result.status == PARTIAL
    assert result.admission_state == REMOTE_PUBLISH_AUTHORITY_REQUIRED
    assert result.local_commit_admitted is True
    assert result.remote_publish_candidate is True
    assert result.remote_publish_ready is False
    assert result.candidate_retained is True


def test_missing_workspace_authority_retains_git_admission_candidate() -> None:
    r = repair()
    result = build_git_admission_post_commit_coherence(
        repair_packet=r,
        observation=observation(
            r,
            workspace=False,
            github=False,
            commit_created=False,
        ),
    )
    assert result.status == PARTIAL
    assert result.admission_state == WORKSPACE_AUTHORITY_REQUIRED
    assert result.candidate_retained is True
    assert result.local_commit_admitted is False
    assert result.next_route == (
        "retain_candidate_and_acquire_workspace_git_authority"
    )


def test_authorized_but_uncommitted_candidate_requests_commit_receipt() -> None:
    r = repair()
    result = build_git_admission_post_commit_coherence(
        repair_packet=r,
        observation=observation(
            r,
            workspace=True,
            github=False,
            commit_created=False,
        ),
    )
    assert result.status == PARTIAL
    assert result.admission_state == COMMIT_RECEIPT_REQUIRED
    assert result.local_commit_admitted is False
    assert result.candidate_retained is True


def test_commit_preimage_mismatch_is_true_lineage_obstruction() -> None:
    r = repair()
    result = build_git_admission_post_commit_coherence(
        repair_packet=r,
        observation=observation(r, pre="f" * 64),
    )
    assert result.status == OBSTRUCTED
    assert result.admission_state == COMMIT_LINEAGE_OBSTRUCTION
    assert (
        "commit_preimage_does_not_match_v7_27_post_edit_bytes"
        in result.blockers
    )
    assert result.remote_publish_candidate is False


def test_stale_post_commit_lean_semantics_requests_reobservation() -> None:
    r = repair()
    result = build_git_admission_post_commit_coherence(
        repair_packet=r,
        observation=observation(r, lean="e" * 64),
    )
    assert result.status == PARTIAL
    assert result.admission_state == POST_COMMIT_REOBSERVATION
    assert result.local_commit_admitted is True
    assert result.post_commit_lean_fresh is False
    assert result.candidate_retained is True
    assert result.remote_publish_candidate is False


def test_post_commit_lean_error_is_regression_not_commit_erasure() -> None:
    r = repair()
    result = build_git_admission_post_commit_coherence(
        repair_packet=r,
        observation=observation(r, lean_errors=2),
    )
    assert result.status == PARTIAL
    assert result.admission_state == POST_COMMIT_LEAN_REGRESSION
    assert result.local_commit_admitted is True
    assert result.candidate_retained is True
    assert result.remote_publish_candidate is False
    assert result.next_route == (
        "retain_local_commit_and_reenter_repair_from_post_commit_bytes"
    )


def test_remote_head_move_retains_local_commit_for_reconciliation() -> None:
    r = repair()
    result = build_git_admission_post_commit_coherence(
        repair_packet=r,
        observation=observation(r, remote_head="c" * 40),
    )
    assert result.status == PARTIAL
    assert result.admission_state == REMOTE_REVISION_RECONCILIATION
    assert result.local_commit_admitted is True
    assert result.remote_revision_aligned is False
    assert result.candidate_retained is True
    assert result.remote_publish_candidate is False
    assert result.next_route == (
        "retain_local_commit_and_reconcile_remote_base_before_publish"
    )


def test_dirty_elsewhere_and_supporting_commit_paths_are_reviewable() -> None:
    r = repair()
    result = build_git_admission_post_commit_coherence(
        repair_packet=r,
        observation=observation(
            r,
            clean=False,
            changed_paths=[
                "formal/KUOS/Example.lean",
                "formal/KUOS/Support.lean",
            ],
        ),
    )
    assert result.status == READY
    assert result.admission_state == REMOTE_PUBLISH_READY
    assert result.remote_publish_ready is True
    assert (
        "post_commit_worktree_dirty_elsewhere_does_not_invalidate_committed_target"
        in result.warnings
    )
    assert (
        "supporting_committed_paths_present_review_before_remote_publish"
        in result.warnings
    )
    assert result.evidence["supporting_committed_path_count"] == 1


def test_not_git_admission_ready_returns_to_v7_27() -> None:
    r = repair(ready=False)
    result = build_git_admission_post_commit_coherence(
        repair_packet=r,
        observation=observation(
            r,
            workspace=False,
            github=False,
            commit_created=False,
        ),
    )
    assert result.status == NOT_APPLICABLE
    assert result.next_route == "return_to_bounded_lean_repair_loop"
    assert result.candidate_retained is True


def main() -> int:
    test_coherent_commit_with_github_authority_is_remote_publish_ready()
    test_missing_github_authority_retains_remote_publish_candidate()
    test_missing_workspace_authority_retains_git_admission_candidate()
    test_authorized_but_uncommitted_candidate_requests_commit_receipt()
    test_commit_preimage_mismatch_is_true_lineage_obstruction()
    test_stale_post_commit_lean_semantics_requests_reobservation()
    test_post_commit_lean_error_is_regression_not_commit_erasure()
    test_remote_head_move_retains_local_commit_for_reconciliation()
    test_dirty_elsewhere_and_supporting_commit_paths_are_reviewable()
    test_not_git_admission_ready_returns_to_v7_27()
    print("PASS: KuuOS Git Admission Post-Commit Coherence v7.28")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
