#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_ci_repair_readiness_v7_26 import (
    NOT_APPLICABLE,
    OBSTRUCTED,
    PARTIAL,
    READY,
    build_ci_repair_readiness,
)


def ci_packet(
    *,
    head: str = "a" * 40,
    target: str = "formal/KUOS/Example.lean",
    classification: str = "lean_ci_repair",
) -> dict:
    return {
        "version": "kuuos_runtime_ci_observation_mcp_routing_v7_25",
        "status": "KUUOS_CI_OBSERVATION_MCP_ROUTING_READY",
        "packet_id": "ci-packet",
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "expected_head_sha": head,
        "run_id": 123,
        "run_conclusion": "failure",
        "classification": classification,
        "target_path": target,
        "lean_signal": classification == "lean_ci_repair",
        "mcp_signal": False,
        "browser_signal": False,
        "full_target_file_audit_required": classification == "lean_ci_repair",
        "ci_error_line_is_locator_not_scope": classification == "lean_ci_repair",
        "routing_request": {},
        "routing_result": {},
        "blockers": [],
        "warnings": [],
    }


def federation_packet(
    *,
    remote_head: str = "a" * 40,
    local_head: str = "a" * 40,
    target: str = "formal/KUOS/Example.lean",
    state: str = "aligned_committed_workspace",
    fs_digest: str = "1" * 64,
    lean_digest: str = "1" * 64,
    lean_fresh: bool = True,
    local_work_allowed: bool = True,
    remote_local_aligned: bool = True,
    remote_mutation_eligible: bool = True,
    fs_exists: bool = True,
) -> dict:
    return {
        "version": "kuuos_runtime_development_mcp_federation_v7_19",
        "status": "KUUOS_DEVELOPMENT_MCP_FEDERATION_READY",
        "packet_id": "federation-packet",
        "workspace_state": state,
        "workspace": {
            "workspace_state": state,
            "target_path": target,
            "remote_head_sha": remote_head,
            "local_head_sha": local_head,
            "remote_local_aligned": remote_local_aligned,
            "worktree_clean": state == "aligned_committed_workspace",
            "tracked_at_head": True,
            "filesystem_exists": fs_exists,
            "target_matches_git_baseline": (
                state == "aligned_committed_workspace"
            ),
            "lean_semantic_fresh": lean_fresh,
            "local_semantic_work_allowed": local_work_allowed,
            "remote_mutation_eligible_before_authority_check": remote_mutation_eligible,
            "next_route": "fixture",
            "working_tree_candidate_digest": "2" * 64,
            "commit_baseline_digest": "3" * 64,
            "filesystem_content_digest": fs_digest if fs_exists else "",
            "lean_source_content_digest": lean_digest,
            "observations_digest": "4" * 64,
        },
        "federation_boundary": {},
        "compatibility_evidence": {},
        "epoch": 0,
    }


def authority(*, workspace: bool, github: bool) -> dict:
    return {
        "workspace_write_authority_ready": workspace,
        "github_write_authority_ready": github,
    }


def test_aligned_fresh_workspace_is_fully_ready() -> None:
    result = build_ci_repair_readiness(
        ci_routing_packet=ci_packet(),
        federation_packet=federation_packet(),
        authority_context=authority(workspace=True, github=True),
    )
    assert result.status == READY, result.to_dict()
    assert result.analysis_ready is True
    assert result.local_repair_ready is True
    assert result.remote_publish_ready is True
    assert result.full_target_file_audit_required is True
    assert result.evidence["repair_scope"] == "entire_target_file"


def test_dirty_fresh_workspace_allows_local_repair_but_not_publish() -> None:
    result = build_ci_repair_readiness(
        ci_routing_packet=ci_packet(),
        federation_packet=federation_packet(
            state="dirty_local_candidate_semantically_fresh",
            remote_mutation_eligible=True,
        ),
        authority_context=authority(workspace=True, github=True),
    )
    assert result.status == READY, result.to_dict()
    assert result.local_repair_ready is True
    assert result.remote_publish_ready is False
    assert result.next_route == "local_repair_then_reobserve_semantics_and_review_diff"


def test_revision_divergence_does_not_block_local_repair() -> None:
    result = build_ci_repair_readiness(
        ci_routing_packet=ci_packet(),
        federation_packet=federation_packet(
            local_head="b" * 40,
            state="remote_local_revision_reconciliation_required",
            remote_local_aligned=False,
            remote_mutation_eligible=False,
        ),
        authority_context=authority(workspace=True, github=True),
    )
    assert result.status == READY, result.to_dict()
    assert result.analysis_ready is True
    assert result.local_repair_ready is True
    assert result.remote_publish_ready is False
    assert result.next_route == "local_repair_allowed_reconcile_revision_before_publish"


def test_stale_lean_semantics_require_reobservation() -> None:
    result = build_ci_repair_readiness(
        ci_routing_packet=ci_packet(),
        federation_packet=federation_packet(
            state="dirty_local_candidate_semantic_reobservation_required",
            lean_digest="5" * 64,
            lean_fresh=False,
        ),
        authority_context=authority(workspace=True, github=True),
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.analysis_ready is False
    assert result.local_repair_ready is False
    assert result.next_route == "reobserve_lean_semantics_on_current_bytes"
    assert "lean_semantic_reobservation_required" in result.warnings


def test_stale_ci_head_does_not_auto_patch_current_workspace() -> None:
    result = build_ci_repair_readiness(
        ci_routing_packet=ci_packet(head="a" * 40),
        federation_packet=federation_packet(remote_head="b" * 40),
        authority_context=authority(workspace=True, github=True),
    )
    assert result.status == PARTIAL
    assert result.exact_head_context_fresh is False
    assert result.local_repair_ready is False
    assert result.repair_candidate_retained is True
    assert result.next_route == "reobserve_ci_on_current_remote_head"


def test_missing_workspace_authority_retains_candidate() -> None:
    result = build_ci_repair_readiness(
        ci_routing_packet=ci_packet(),
        federation_packet=federation_packet(),
        authority_context=authority(workspace=False, github=False),
    )
    assert result.status == PARTIAL
    assert result.analysis_ready is True
    assert result.local_repair_ready is False
    assert result.repair_candidate_retained is True
    assert result.next_route == "retain_repair_candidate_and_acquire_workspace_authority"


def test_target_binding_mismatch_is_obstruction() -> None:
    result = build_ci_repair_readiness(
        ci_routing_packet=ci_packet(target="formal/KUOS/A.lean"),
        federation_packet=federation_packet(target="formal/KUOS/B.lean"),
        authority_context=authority(workspace=True, github=True),
    )
    assert result.status == OBSTRUCTED
    assert "ci_federation_target_path_mismatch" in result.blockers


def test_nonlean_route_is_not_applicable() -> None:
    result = build_ci_repair_readiness(
        ci_routing_packet=ci_packet(
            target="",
            classification="mcp_spec_research",
        ),
        federation_packet=federation_packet(),
        authority_context=authority(workspace=True, github=True),
    )
    assert result.status == NOT_APPLICABLE
    assert result.local_repair_ready is False


def main() -> int:
    test_aligned_fresh_workspace_is_fully_ready()
    test_dirty_fresh_workspace_allows_local_repair_but_not_publish()
    test_revision_divergence_does_not_block_local_repair()
    test_stale_lean_semantics_require_reobservation()
    test_stale_ci_head_does_not_auto_patch_current_workspace()
    test_missing_workspace_authority_retains_candidate()
    test_target_binding_mismatch_is_obstruction()
    test_nonlean_route_is_not_applicable()
    print("PASS: KuuOS CI Repair Readiness v7.26")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
