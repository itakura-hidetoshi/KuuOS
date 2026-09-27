#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import tempfile
from typing import Any

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from runtime.kuuos_runtime_development_mcp_federation_v7_19 import (
    ALIGNED_COMMITTED,
    DIRTY_ELSEWHERE,
    DIRTY_FRESH,
    DIRTY_STALE,
    OBSTRUCTED,
    PARTIAL,
    READY,
    REVISION_DIVERGENCE,
    CLEAN_BASELINE_MISMATCH,
    TARGET_BINDING_MISMATCH,
    UNTRACKED_FRESH,
    build_development_mcp_federation,
)

PLAN = "development_mcp_federation_plan_v7_19.json"
OBS = "development_mcp_workspace_observation_v7_19.json"
OUT = "development_mcp_federation_packet_v7_19.json"

HEAD = "1" * 40
REMOTE2 = "2" * 40


def h(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def plan() -> dict[str, Any]:
    return {
        "version": "kuuos_development_mcp_federation_plan_v7_19",
        "dirty_worktree_is_error": False,
        "dirty_worktree_may_continue_local_semantic_work": True,
        "remote_revision_mismatch_blocks_local_read_analysis": False,
        "remote_revision_mismatch_blocks_remote_mutation_without_reconciliation": True,
        "filesystem_observation_is_git_commit_authority": False,
        "lean_diagnostics_bound_to_file_bytes_digest": True,
        "lean_semantic_freshness_grants_git_write_authority": False,
        "git_commit_tree_excludes_uncommitted_bytes": True,
        "remote_mutation_requires_explicit_authority": True,
        "verified_compatible_mcp_transfers_source_authority": False,
    }


def authority() -> dict[str, Any]:
    return {
        "authority_status": "KUUOS_DEVELOPMENT_MCP_FEDERATION_AUTHORITY_READY",
        "plan_read_allowed": True,
        "workspace_observation_read_allowed": True,
        "output_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "development_mcp_federation_enabled": True,
        "apply_development_mcp_federation": True,
    }


def observation(
    *,
    remote_head: str = HEAD,
    local_head: str = HEAD,
    clean: bool = True,
    tracked: bool = True,
    fs_bytes: str = "committed",
    git_bytes: str = "committed",
    lean_bytes: str | None = None,
    fs_path: str = "formal/KUOS/Example.lean",
    lean_path: str | None = None,
    exists: bool = True,
) -> dict[str, Any]:
    fs_digest = h(fs_bytes) if exists else ""
    git_digest = h(git_bytes) if tracked else ""
    if lean_bytes is None:
        lean_bytes = fs_bytes
    if lean_path is None:
        lean_path = fs_path
    return {
        "version": "kuuos_development_mcp_workspace_observation_v7_19",
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "github_remote": {
            "exact_head_sha": remote_head,
            "observation_digest": h({"github": remote_head}),
        },
        "local_git": {
            "head_sha": local_head,
            "worktree_clean": clean,
            "staged_diff_digest": "" if clean else h("staged"),
            "unstaged_diff_digest": "" if clean else h("unstaged"),
            "untracked_paths_digest": "" if clean else h("untracked"),
            "observation_digest": h({"git": local_head, "clean": clean}),
        },
        "filesystem": {
            "path": fs_path,
            "exists": exists,
            "content_digest": fs_digest,
            "observation_digest": h({"fs": fs_path, "digest": fs_digest}),
        },
        "git_commit_baseline": {
            "path": fs_path,
            "tracked_at_head": tracked,
            "blob_digest": git_digest,
        },
        "lean_lsp": {
            "file_path": lean_path,
            "source_content_digest": h(lean_bytes) if exists else "",
            "diagnostics_digest": h({"lean": lean_path, "bytes": lean_bytes}) if exists else "",
            "observation_digest": h({"lsp": lean_path}),
        },
    }


def write(root: pathlib.Path, obs: dict[str, Any]) -> None:
    (root / PLAN).write_text(json.dumps(plan()), encoding="utf-8")
    (root / OBS).write_text(json.dumps(obs), encoding="utf-8")


def output(root: pathlib.Path) -> dict[str, Any]:
    return json.loads((root / OUT).read_text())


def run(root: pathlib.Path):
    return build_development_mcp_federation(
        runtime_context=ctx(root),
        authority_packet=authority(),
    )


def test_clean_exact_head_semantic_alignment() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write(root, observation())
        result = run(root)
        assert result.status == READY, result.to_dict()
        assert result.workspace_state == ALIGNED_COMMITTED
        assert result.remote_local_aligned is True
        assert result.target_matches_git_baseline is True
        assert result.lean_semantic_fresh is True
        assert result.local_semantic_work_allowed is True
        assert result.remote_mutation_eligible is True


def test_dirty_worktree_with_fresh_lean_semantics_is_valid_candidate() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write(
            root,
            observation(
                clean=False,
                fs_bytes="edited",
                git_bytes="committed",
                lean_bytes="edited",
            ),
        )
        result = run(root)
        assert result.status == READY, result.to_dict()
        assert result.workspace_state == DIRTY_FRESH
        assert result.local_semantic_work_allowed is True
        assert result.remote_mutation_eligible is True
        out = output(root)
        assert out["federation_boundary"]["dirty_worktree_is_error"] is False
        assert (
            out["workspace"]["next_route"]
            == "continue_local_repair_then_review_git_diff"
        )


def test_dirty_worktree_with_stale_lean_result_requires_reobservation_not_discard() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write(
            root,
            observation(
                clean=False,
                fs_bytes="edited-v2",
                git_bytes="committed",
                lean_bytes="edited-v1",
            ),
        )
        result = run(root)
        assert result.status == PARTIAL
        assert result.workspace_state == DIRTY_STALE
        assert result.local_semantic_work_allowed is True
        assert result.remote_mutation_eligible is False
        out = output(root)
        assert (
            out["workspace"]["next_route"]
            == "reobserve_lean_on_current_filesystem_bytes"
        )


def test_remote_local_revision_divergence_does_not_block_local_analysis() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write(
            root,
            observation(
                remote_head=REMOTE2,
                local_head=HEAD,
                clean=False,
                fs_bytes="local-candidate",
                git_bytes="committed",
                lean_bytes="local-candidate",
            ),
        )
        result = run(root)
        assert result.status == PARTIAL
        assert result.workspace_state == REVISION_DIVERGENCE
        assert result.remote_local_aligned is False
        assert result.local_semantic_work_allowed is True
        assert result.remote_mutation_eligible is False
        out = output(root)
        assert out["federation_boundary"][
            "remote_revision_mismatch_blocks_local_read_analysis"
        ] is False
        assert out["federation_boundary"][
            "remote_revision_mismatch_blocks_remote_mutation_without_reconciliation"
        ] is True


def test_clean_git_but_different_filesystem_bytes_is_true_cross_surface_obstruction() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write(
            root,
            observation(
                clean=True,
                fs_bytes="different",
                git_bytes="committed",
                lean_bytes="different",
            ),
        )
        result = run(root)
        assert result.status == OBSTRUCTED
        assert result.workspace_state == CLEAN_BASELINE_MISMATCH
        assert result.local_semantic_work_allowed is False


def test_untracked_file_can_receive_fresh_lean_semantics() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write(
            root,
            observation(
                clean=False,
                tracked=False,
                fs_bytes="new-file",
                lean_bytes="new-file",
            ),
        )
        result = run(root)
        assert result.status == READY
        assert result.workspace_state == UNTRACKED_FRESH
        assert result.local_semantic_work_allowed is True
        assert result.remote_mutation_eligible is False


def test_dirty_elsewhere_does_not_invalidate_selected_committed_file() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write(
            root,
            observation(
                clean=False,
                fs_bytes="committed",
                git_bytes="committed",
                lean_bytes="committed",
            ),
        )
        result = run(root)
        assert result.status == READY
        assert result.workspace_state == DIRTY_ELSEWHERE
        assert result.local_semantic_work_allowed is True


def test_lean_observation_for_other_file_is_obstruction_for_target_binding() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        write(
            root,
            observation(
                fs_path="formal/KUOS/Target.lean",
                lean_path="formal/KUOS/Other.lean",
            ),
        )
        result = run(root)
        assert result.status == OBSTRUCTED
        assert result.workspace_state == TARGET_BINDING_MISMATCH


def main() -> int:
    test_clean_exact_head_semantic_alignment()
    test_dirty_worktree_with_fresh_lean_semantics_is_valid_candidate()
    test_dirty_worktree_with_stale_lean_result_requires_reobservation_not_discard()
    test_remote_local_revision_divergence_does_not_block_local_analysis()
    test_clean_git_but_different_filesystem_bytes_is_true_cross_surface_obstruction()
    test_untracked_file_can_receive_fresh_lean_semantics()
    test_dirty_elsewhere_does_not_invalidate_selected_committed_file()
    test_lean_observation_for_other_file_is_obstruction_for_target_binding()
    print("PASS: KuuOS Development MCP Federation v7.19")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
