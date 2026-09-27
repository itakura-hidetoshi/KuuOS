#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_bounded_lean_repair_loop_v7_27 import (
    BUDGET_REACHED,
    DIFF_REOBSERVATION,
    GIT_ADMISSION_READY,
    LEAN_ERRORS_REMAIN,
    NO_EFFECTIVE_EDIT,
    NOT_APPLICABLE,
    OBSTRUCTED,
    PARTIAL,
    READY,
    SEMANTIC_REOBSERVATION,
    build_bounded_lean_repair_loop,
)


def readiness(*, local_ready: bool = True) -> dict:
    return {
        "version": "kuuos_runtime_ci_repair_readiness_v7_26",
        "status": "KUUOS_CI_REPAIR_READINESS_READY" if local_ready else "KUUOS_CI_REPAIR_READINESS_PARTIAL",
        "packet_id": "ready-packet",
        "target_path": "formal/KUOS/Example.lean",
        "ci_head_sha": "a" * 40,
        "federation_remote_head_sha": "a" * 40,
        "exact_head_context_fresh": True,
        "full_target_file_audit_required": True,
        "current_bytes_observed": True,
        "lean_semantic_fresh": True,
        "analysis_ready": local_ready,
        "local_repair_ready": local_ready,
        "remote_publish_ready": False,
        "repair_candidate_retained": True,
        "next_route": "fixture",
        "evidence": {
            "repair_scope": "entire_target_file",
            "target_path": "formal/KUOS/Example.lean",
            "filesystem_content_digest": "1" * 64,
            "lean_source_content_digest": "1" * 64,
            "federation_observations_digest": "2" * 64,
            "workspace_state": "dirty_local_candidate_semantically_fresh",
            "remote_local_aligned": True,
            "target_matches_git_baseline": False,
            "ci_error_line_is_locator_not_scope": True,
            "full_target_file_audit_required": True,
            "raw_source_bytes_persisted_by_readiness_layer": False,
            "raw_ci_logs_persisted_by_readiness_layer": False,
            "source_authority_transferred": False,
        },
        "blockers": [],
        "warnings": [],
    }


def observation(
    *,
    iteration: int = 1,
    maximum: int = 4,
    edit_applied: bool = True,
    pre: str = "1" * 64,
    post: str = "3" * 64,
    lean_source: str = "3" * 64,
    errors: int = 0,
    git_target_post: str = "3" * 64,
    changed_paths: list[str] | None = None,
    lean_after: bool = True,
    diff_after: bool = True,
) -> dict:
    return {
        "version": "kuuos_bounded_lean_repair_observation_v7_27",
        "target_path": "formal/KUOS/Example.lean",
        "iteration_index": iteration,
        "max_iterations": maximum,
        "full_file_audit_completed": True,
        "full_file_audit_digest": "a" * 64,
        "edit_applied": edit_applied,
        "edit_receipt_digest": "b" * 64 if edit_applied else "",
        "pre_edit_content_digest": pre,
        "post_edit_content_digest": post,
        "filesystem_observation_digest": "c" * 64,
        "lean_observation_after_edit": lean_after,
        "lean_source_content_digest": lean_source,
        "lean_diagnostics_digest": "d" * 64,
        "lean_error_count": errors,
        "git_diff_observed_after_edit": diff_after,
        "git_diff_digest": "e" * 64,
        "git_diff_target_post_content_digest": git_target_post,
        "git_changed_paths": changed_paths or ["formal/KUOS/Example.lean"],
    }


def test_error_free_fresh_edit_is_git_admission_ready() -> None:
    result = build_bounded_lean_repair_loop(
        readiness_packet=readiness(),
        repair_observation=observation(),
    )
    assert result.status == READY, result.to_dict()
    assert result.repair_state == GIT_ADMISSION_READY
    assert result.local_repair_verified is True
    assert result.git_admission_ready is True
    assert result.remote_publish_ready is False
    assert result.evidence["repair_scope"] == "entire_target_file"
    assert result.evidence["ci_error_line_is_locator_not_scope"] is True


def test_remaining_lean_errors_continue_candidate() -> None:
    result = build_bounded_lean_repair_loop(
        readiness_packet=readiness(),
        repair_observation=observation(iteration=2, maximum=4, errors=3),
    )
    assert result.status == PARTIAL
    assert result.repair_state == LEAN_ERRORS_REMAIN
    assert result.candidate_retained is True
    assert result.git_admission_ready is False
    assert result.next_route == "continue_bounded_repair_from_current_post_edit_bytes"


def test_budget_reached_is_not_rejection() -> None:
    result = build_bounded_lean_repair_loop(
        readiness_packet=readiness(),
        repair_observation=observation(iteration=4, maximum=4, errors=1),
    )
    assert result.status == PARTIAL
    assert result.repair_state == BUDGET_REACHED
    assert result.candidate_retained is True
    assert result.evidence["budget_exhaustion_is_rejection"] is False
    assert "repair_iteration_budget_reached_without_semantic_success" in result.warnings


def test_stale_semantics_request_reobservation() -> None:
    result = build_bounded_lean_repair_loop(
        readiness_packet=readiness(),
        repair_observation=observation(
            lean_source="4" * 64,
            lean_after=True,
        ),
    )
    assert result.status == PARTIAL
    assert result.repair_state == SEMANTIC_REOBSERVATION
    assert result.lean_semantic_fresh is False
    assert result.next_route == "reobserve_lean_semantics_on_post_edit_bytes"


def test_error_free_semantics_with_stale_diff_waits_for_git_reobservation() -> None:
    result = build_bounded_lean_repair_loop(
        readiness_packet=readiness(),
        repair_observation=observation(
            git_target_post="5" * 64,
        ),
    )
    assert result.status == PARTIAL
    assert result.repair_state == DIFF_REOBSERVATION
    assert result.local_repair_verified is True
    assert result.git_admission_ready is False
    assert result.next_route == "reobserve_git_diff_for_semantically_verified_bytes"


def test_preimage_mismatch_is_lineage_obstruction() -> None:
    result = build_bounded_lean_repair_loop(
        readiness_packet=readiness(),
        repair_observation=observation(pre="9" * 64),
    )
    assert result.status == OBSTRUCTED
    assert "edit_preimage_does_not_match_repair_ready_bytes" in result.blockers
    assert result.candidate_retained is True


def test_supporting_file_changes_are_reviewable_not_failure() -> None:
    result = build_bounded_lean_repair_loop(
        readiness_packet=readiness(),
        repair_observation=observation(
            changed_paths=[
                "formal/KUOS/Example.lean",
                "formal/KUOS/Support.lean",
            ]
        ),
    )
    assert result.status == READY
    assert result.git_admission_ready is True
    assert result.evidence["supporting_changed_path_count"] == 1
    assert "supporting_file_changes_present_review_before_git_admission" in result.warnings


def test_no_effective_edit_retains_candidate() -> None:
    result = build_bounded_lean_repair_loop(
        readiness_packet=readiness(),
        repair_observation=observation(post="1" * 64, lean_source="1" * 64, git_target_post="1" * 64),
    )
    assert result.status == PARTIAL
    assert result.repair_state == NO_EFFECTIVE_EDIT
    assert result.candidate_retained is True


def test_not_locally_ready_returns_to_readiness_layer() -> None:
    result = build_bounded_lean_repair_loop(
        readiness_packet=readiness(local_ready=False),
        repair_observation=observation(edit_applied=False, post="1" * 64, lean_source="1" * 64, git_target_post="1" * 64),
    )
    assert result.status == NOT_APPLICABLE
    assert result.next_route == "return_to_ci_repair_readiness"


def main() -> int:
    test_error_free_fresh_edit_is_git_admission_ready()
    test_remaining_lean_errors_continue_candidate()
    test_budget_reached_is_not_rejection()
    test_stale_semantics_request_reobservation()
    test_error_free_semantics_with_stale_diff_waits_for_git_reobservation()
    test_preimage_mismatch_is_lineage_obstruction()
    test_supporting_file_changes_are_reviewable_not_failure()
    test_no_effective_edit_retains_candidate()
    test_not_locally_ready_returns_to_readiness_layer()
    print("PASS: KuuOS Bounded Lean Repair Loop v7.27")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
