#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import re
import time
from typing import Any, Mapping

VERSION = "kuuos_runtime_development_mcp_federation_v7_19"
PLAN_VERSION = "kuuos_development_mcp_federation_plan_v7_19"
OBSERVATION_VERSION = "kuuos_development_mcp_workspace_observation_v7_19"

READY = "KUUOS_DEVELOPMENT_MCP_FEDERATION_READY"
PARTIAL = "KUUOS_DEVELOPMENT_MCP_FEDERATION_PARTIAL"
OBSTRUCTED = "KUUOS_DEVELOPMENT_MCP_FEDERATION_OBSTRUCTED"
BLOCKED = "KUUOS_DEVELOPMENT_MCP_FEDERATION_BLOCKED"

ALIGNED_COMMITTED = "aligned_committed_workspace"
DIRTY_FRESH = "dirty_local_candidate_semantically_fresh"
DIRTY_STALE = "dirty_local_candidate_semantic_reobservation_required"
DIRTY_ELSEWHERE = "workspace_dirty_elsewhere_selected_file_committed"
UNTRACKED_FRESH = "untracked_local_candidate_semantically_fresh"
UNTRACKED_STALE = "untracked_local_candidate_semantic_reobservation_required"
REVISION_DIVERGENCE = "remote_local_revision_reconciliation_required"
CLEAN_BASELINE_MISMATCH = "clean_worktree_filesystem_git_baseline_obstruction"
TARGET_BINDING_MISMATCH = "filesystem_lean_target_binding_obstruction"
INCOMPLETE = "workspace_observation_incomplete"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class DevelopmentMCPFederationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    workspace_state: str
    target_path: str
    remote_local_aligned: bool
    target_matches_git_baseline: bool | None
    lean_semantic_fresh: bool | None
    local_semantic_work_allowed: bool
    remote_mutation_eligible: bool
    output_path: str
    receipt_path: str
    audit_path: str
    output_written: bool
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


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(dict(value), ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(value), ensure_ascii=False, sort_keys=True) + "\n")


def _digest(value: Any, field: str, blockers: list[str], *, optional: bool = False) -> str:
    text = str(value or "").strip()
    if optional and not text:
        return ""
    if not SHA64.fullmatch(text):
        blockers.append(field + "_invalid")
    return text


def _commit(value: Any, field: str, blockers: list[str]) -> str:
    text = str(value or "").strip()
    if not SHA40.fullmatch(text):
        blockers.append(field + "_invalid")
    return text


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    required_false = (
        "dirty_worktree_is_error",
        "remote_revision_mismatch_blocks_local_read_analysis",
        "filesystem_observation_is_git_commit_authority",
        "lean_semantic_freshness_grants_git_write_authority",
        "verified_compatible_mcp_transfers_source_authority",
    )
    for key in required_false:
        if plan.get(key) is not False:
            blockers.append(key + "_must_be_false")
    required_true = (
        "dirty_worktree_may_continue_local_semantic_work",
        "remote_revision_mismatch_blocks_remote_mutation_without_reconciliation",
        "lean_diagnostics_bound_to_file_bytes_digest",
        "git_commit_tree_excludes_uncommitted_bytes",
        "remote_mutation_requires_explicit_authority",
    )
    for key in required_true:
        if plan.get(key) is not True:
            blockers.append(key + "_must_be_true")


def _classify(
    observation: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    github = _m(observation.get("github_remote"))
    git = _m(observation.get("local_git"))
    fs = _m(observation.get("filesystem"))
    baseline = _m(observation.get("git_commit_baseline"))
    lean = _m(observation.get("lean_lsp"))

    if observation.get("version") != OBSERVATION_VERSION:
        blockers.append("observation_version_invalid")
    if observation.get("repository_full_name") != "itakura-hidetoshi/KuuOS":
        blockers.append("repository_full_name_invalid")

    remote_head = _commit(github.get("exact_head_sha"), "github_exact_head_sha", blockers)
    local_head = _commit(git.get("head_sha"), "local_git_head_sha", blockers)

    if not isinstance(git.get("worktree_clean"), bool):
        blockers.append("worktree_clean_must_be_bool")
    worktree_clean = git.get("worktree_clean") is True

    target_path = str(fs.get("path", "")).strip()
    lean_path = str(lean.get("file_path", "")).strip()
    baseline_path = str(baseline.get("path", "")).strip()
    if not target_path:
        blockers.append("filesystem_target_path_missing")
    if lean_path and lean_path != target_path:
        target_binding_ok = False
    else:
        target_binding_ok = True
    if baseline_path and baseline_path != target_path:
        blockers.append("git_baseline_target_path_mismatch")

    fs_exists = fs.get("exists")
    if not isinstance(fs_exists, bool):
        blockers.append("filesystem_exists_must_be_bool")
        fs_exists = False

    tracked = baseline.get("tracked_at_head")
    if not isinstance(tracked, bool):
        blockers.append("tracked_at_head_must_be_bool")
        tracked = False

    fs_digest = _digest(
        fs.get("content_digest"),
        "filesystem_content_digest",
        blockers,
        optional=not fs_exists,
    )
    baseline_digest = _digest(
        baseline.get("blob_digest"),
        "git_baseline_blob_digest",
        blockers,
        optional=not tracked,
    )
    lean_source_digest = _digest(
        lean.get("source_content_digest"),
        "lean_source_content_digest",
        blockers,
        optional=not lean_path,
    )
    _digest(
        lean.get("diagnostics_digest"),
        "lean_diagnostics_digest",
        blockers,
        optional=not lean_path,
    )

    for provider, packet in (
        ("github", github),
        ("git", git),
        ("filesystem", fs),
        ("lean_lsp", lean),
    ):
        _digest(
            packet.get("observation_digest"),
            provider + "_observation_digest",
            blockers,
        )

    remote_local_aligned = remote_head == local_head
    target_matches_baseline: bool | None
    if tracked and fs_exists:
        target_matches_baseline = fs_digest == baseline_digest
    elif tracked != fs_exists:
        target_matches_baseline = False
    else:
        target_matches_baseline = None

    lean_semantic_fresh: bool | None = None
    if lean_path and fs_exists:
        lean_semantic_fresh = target_binding_ok and lean_source_digest == fs_digest

    staged = str(git.get("staged_diff_digest", "")).strip()
    unstaged = str(git.get("unstaged_diff_digest", "")).strip()
    untracked = str(git.get("untracked_paths_digest", "")).strip()
    for value, name in (
        (staged, "staged_diff_digest"),
        (unstaged, "unstaged_diff_digest"),
        (untracked, "untracked_paths_digest"),
    ):
        if value and not SHA64.fullmatch(value):
            blockers.append(name + "_invalid")

    if not target_binding_ok:
        state = TARGET_BINDING_MISMATCH
    elif not remote_local_aligned:
        state = REVISION_DIVERGENCE
    elif worktree_clean and tracked and target_matches_baseline is False:
        state = CLEAN_BASELINE_MISMATCH
    elif not fs_exists:
        state = INCOMPLETE
    elif not tracked:
        state = UNTRACKED_FRESH if lean_semantic_fresh else UNTRACKED_STALE
    elif not worktree_clean and target_matches_baseline is False:
        state = DIRTY_FRESH if lean_semantic_fresh else DIRTY_STALE
    elif not worktree_clean and target_matches_baseline is True:
        state = DIRTY_ELSEWHERE
    elif worktree_clean and target_matches_baseline is True:
        state = ALIGNED_COMMITTED if lean_semantic_fresh else DIRTY_STALE
    else:
        state = INCOMPLETE

    if state in {CLEAN_BASELINE_MISMATCH, TARGET_BINDING_MISMATCH}:
        status = OBSTRUCTED
    elif state in {
        DIRTY_STALE,
        UNTRACKED_STALE,
        REVISION_DIVERGENCE,
        INCOMPLETE,
    }:
        status = PARTIAL
    else:
        status = READY

    local_semantic_work_allowed = state not in {
        CLEAN_BASELINE_MISMATCH,
        TARGET_BINDING_MISMATCH,
        INCOMPLETE,
    }
    remote_mutation_eligible = (
        remote_local_aligned
        and state in {ALIGNED_COMMITTED, DIRTY_FRESH, DIRTY_ELSEWHERE}
        and lean_semantic_fresh is not False
    )

    if state == ALIGNED_COMMITTED:
        next_route = "continue_semantic_work_or_prepare_remote_operation"
    elif state == DIRTY_FRESH:
        next_route = "continue_local_repair_then_review_git_diff"
    elif state == DIRTY_ELSEWHERE:
        next_route = "continue_selected_file_semantics_review_other_local_diff"
    elif state == UNTRACKED_FRESH:
        next_route = "continue_local_semantics_then_decide_git_admission"
    elif state in {DIRTY_STALE, UNTRACKED_STALE}:
        next_route = "reobserve_lean_on_current_filesystem_bytes"
    elif state == REVISION_DIVERGENCE:
        next_route = "reconcile_remote_local_revision_before_remote_mutation"
    else:
        next_route = "repair_cross_surface_observation_binding"

    return {
        "workspace_state": state,
        "status": status,
        "target_path": target_path,
        "remote_head_sha": remote_head,
        "local_head_sha": local_head,
        "remote_local_aligned": remote_local_aligned,
        "worktree_clean": worktree_clean,
        "tracked_at_head": tracked,
        "filesystem_exists": fs_exists,
        "target_matches_git_baseline": target_matches_baseline,
        "lean_semantic_fresh": lean_semantic_fresh,
        "local_semantic_work_allowed": local_semantic_work_allowed,
        "remote_mutation_eligible_before_authority_check": remote_mutation_eligible,
        "next_route": next_route,
        "working_tree_candidate_digest": _sha(
            {
                "target_path": target_path,
                "filesystem_content_digest": fs_digest,
                "staged_diff_digest": staged,
                "unstaged_diff_digest": unstaged,
                "untracked_paths_digest": untracked,
            }
        ),
        "commit_baseline_digest": baseline_digest,
        "filesystem_content_digest": fs_digest,
        "lean_source_content_digest": lean_source_digest,
        "observations_digest": _sha(
            {
                "github": github.get("observation_digest"),
                "git": git.get("observation_digest"),
                "filesystem": fs.get("observation_digest"),
                "lean_lsp": lean.get("observation_digest"),
            }
        ),
    }


def build_development_mcp_federation(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
) -> DevelopmentMCPFederationResult:
    ctx = _m(runtime_context)
    authority_packet = _m(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []

    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "development_mcp_federation_plan_v7_19.json"
    observation_path = root / "development_mcp_workspace_observation_v7_19.json"
    output_path = root / "development_mcp_federation_packet_v7_19.json"
    receipt_path = root / "development_mcp_federation_receipt_v7_19.json"
    audit_path = root / "development_mcp_federation_audit_v7_19.jsonl"

    if ctx.get("development_mcp_federation_enabled") is not True:
        blockers.append("development_mcp_federation_enabled_not_true")
    if ctx.get("apply_development_mcp_federation") is not True:
        blockers.append("apply_development_mcp_federation_not_true")
    if (
        authority_packet.get("authority_status")
        != "KUUOS_DEVELOPMENT_MCP_FEDERATION_AUTHORITY_READY"
    ):
        blockers.append("development_mcp_federation_authority_not_ready")

    for field in (
        "plan_read_allowed",
        "workspace_observation_read_allowed",
        "output_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority_packet.get(field) is not True:
            blockers.append(field.replace("_allowed", "_not_allowed"))

    plan = _read_json(plan_path)
    observation = _read_json(observation_path)
    if not plan:
        blockers.append("development_mcp_federation_plan_missing_or_invalid")
    else:
        _validate_plan(plan, blockers)
    if not observation:
        blockers.append("development_mcp_workspace_observation_missing_or_invalid")

    classified: dict[str, Any] = {}
    if not blockers:
        classified = _classify(observation, blockers)

    if blockers:
        status = BLOCKED
        workspace_state = INCOMPLETE
    else:
        status = classified["status"]
        workspace_state = classified["workspace_state"]

    output: dict[str, Any] = {}
    output_written = False
    if not blockers:
        output = {
            "version": VERSION,
            "status": status,
            "workspace_state": workspace_state,
            "workspace": classified,
            "federation_boundary": {
                "github_remote_is_commit_collaboration_surface": True,
                "git_mcp_is_local_revision_surface": True,
                "filesystem_mcp_is_working_bytes_surface": True,
                "lean_lsp_is_semantic_surface": True,
                "dirty_worktree_is_error": False,
                "dirty_worktree_may_continue_local_semantic_work": True,
                "git_commit_tree_excludes_uncommitted_bytes": True,
                "lean_diagnostics_bound_to_file_bytes_digest": True,
                "remote_revision_mismatch_blocks_local_read_analysis": False,
                "remote_revision_mismatch_blocks_remote_mutation_without_reconciliation": True,
                "filesystem_observation_is_git_commit_authority": False,
                "lean_semantic_freshness_grants_git_write_authority": False,
                "remote_mutation_requires_explicit_authority": True,
                "verified_compatible_mcp_transfers_source_authority": False,
            },
            "compatibility_evidence": {
                "lean_lsp_v7_17": "manifests/kuuos_lean_lsp_mcp_compatibility_v7_17.json",
                "local_repository_v7_18": "manifests/kuuos_local_repository_mcp_compatibility_v7_18.json",
                "repository_git_revision_v0_83": "docs/KUUOS_REPOSITORY_GIT_REVISION_ADAPTER_v0_83.md",
            },
            "epoch": int(time.time()),
        }
        _write_json(output_path, output)
        output_written = True

    packet_id = "kuuos-development-mcp-federation-" + _sha(
        {
            "plan": plan,
            "observation": observation,
            "output": output,
            "blockers": sorted(set(blockers)),
        }
    )[:16]

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "workspace_state": workspace_state,
        "output_written": output_written,
        "output_digest": _sha(output),
        "dirty_worktree_is_error": False,
        "remote_revision_mismatch_blocks_local_read_analysis": False,
        "remote_mutation_requires_explicit_authority": True,
        "source_authority_transferred": False,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }

    if authority_packet.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if authority_packet.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "record_digest": _sha(receipt)})

    return DevelopmentMCPFederationResult(
        VERSION,
        status,
        packet_id,
        str(root),
        workspace_state,
        str(classified.get("target_path", "")),
        bool(classified.get("remote_local_aligned", False)),
        classified.get("target_matches_git_baseline"),
        classified.get("lean_semantic_fresh"),
        bool(classified.get("local_semantic_work_allowed", False)),
        bool(classified.get("remote_mutation_eligible_before_authority_check", False)),
        str(output_path),
        str(receipt_path),
        str(audit_path),
        output_written,
        sorted(set(blockers)),
        warnings,
    )
