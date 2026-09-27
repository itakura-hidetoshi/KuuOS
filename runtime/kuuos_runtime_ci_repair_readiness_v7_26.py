#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_runtime_ci_repair_readiness_v7_26"
CI_ROUTING_VERSION = "kuuos_runtime_ci_observation_mcp_routing_v7_25"
FEDERATION_VERSION = "kuuos_runtime_development_mcp_federation_v7_19"

READY = "KUUOS_CI_REPAIR_READINESS_READY"
PARTIAL = "KUUOS_CI_REPAIR_READINESS_PARTIAL"
OBSTRUCTED = "KUUOS_CI_REPAIR_READINESS_OBSTRUCTED"
NOT_APPLICABLE = "KUUOS_CI_REPAIR_READINESS_NOT_APPLICABLE"
BLOCKED = "KUUOS_CI_REPAIR_READINESS_BLOCKED"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")

FRESH_LOCAL_STATES = {
    "aligned_committed_workspace",
    "dirty_local_candidate_semantically_fresh",
    "workspace_dirty_elsewhere_selected_file_committed",
    "untracked_local_candidate_semantically_fresh",
    "remote_local_revision_reconciliation_required",
}
STALE_SEMANTIC_STATES = {
    "dirty_local_candidate_semantic_reobservation_required",
    "untracked_local_candidate_semantic_reobservation_required",
}
OBSTRUCTED_STATES = {
    "clean_worktree_filesystem_git_baseline_obstruction",
    "filesystem_lean_target_binding_obstruction",
}


@dataclass(frozen=True)
class CIRepairReadinessResult:
    version: str
    status: str
    packet_id: str
    target_path: str
    ci_head_sha: str
    federation_remote_head_sha: str
    exact_head_context_fresh: bool
    full_target_file_audit_required: bool
    current_bytes_observed: bool
    lean_semantic_fresh: bool
    analysis_ready: bool
    local_repair_ready: bool
    remote_publish_ready: bool
    repair_candidate_retained: bool
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


def _digest(value: Any) -> str:
    text = str(value or "").strip()
    return text if SHA64.fullmatch(text) else ""


def build_ci_repair_readiness(
    *,
    ci_routing_packet: Mapping[str, Any],
    federation_packet: Mapping[str, Any],
    authority_context: Mapping[str, Any],
) -> CIRepairReadinessResult:
    ci = _m(ci_routing_packet)
    federation = _m(federation_packet)
    authority = _m(authority_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ci.get("version") != CI_ROUTING_VERSION:
        blockers.append("ci_routing_version_invalid")
    if federation.get("version") != FEDERATION_VERSION:
        blockers.append("federation_version_invalid")

    classification = str(ci.get("classification", ""))
    target_path = str(ci.get("target_path", "")).strip()
    ci_head_sha = str(ci.get("expected_head_sha", "")).strip()

    if SHA40.fullmatch(ci_head_sha) is None:
        blockers.append("ci_head_sha_invalid")

    if classification != "lean_ci_repair":
        status = NOT_APPLICABLE if not blockers else BLOCKED
        packet_id = "kuuos-ci-repair-readiness-" + _sha(
            {
                "classification": classification,
                "ci_head_sha": ci_head_sha,
                "blockers": blockers,
            }
        )[:16]
        return CIRepairReadinessResult(
            VERSION,
            status,
            packet_id,
            target_path,
            ci_head_sha,
            "",
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            "no_lean_repair_readiness_required",
            {},
            sorted(set(blockers)),
            warnings,
        )

    if ci.get("full_target_file_audit_required") is not True:
        blockers.append("full_target_file_audit_boundary_missing")
    if ci.get("ci_error_line_is_locator_not_scope") is not True:
        blockers.append("ci_locator_scope_boundary_missing")
    if not target_path.endswith(".lean"):
        blockers.append("lean_target_path_invalid")

    workspace = _m(federation.get("workspace"))
    federation_state = str(federation.get("workspace_state", ""))
    federation_target = str(workspace.get("target_path", "")).strip()
    federation_remote_head = str(workspace.get("remote_head_sha", "")).strip()

    if SHA40.fullmatch(federation_remote_head) is None:
        blockers.append("federation_remote_head_invalid")
    if federation_target != target_path:
        blockers.append("ci_federation_target_path_mismatch")

    fs_digest = _digest(workspace.get("filesystem_content_digest"))
    lean_digest = _digest(workspace.get("lean_source_content_digest"))
    observations_digest = _digest(workspace.get("observations_digest"))

    current_bytes_observed = bool(
        workspace.get("filesystem_exists") is True and fs_digest
    )
    lean_semantic_fresh = bool(
        workspace.get("lean_semantic_fresh") is True
        and fs_digest
        and lean_digest
        and fs_digest == lean_digest
    )
    local_semantic_work_allowed = (
        workspace.get("local_semantic_work_allowed") is True
    )
    exact_head_context_fresh = (
        bool(ci_head_sha)
        and bool(federation_remote_head)
        and ci_head_sha == federation_remote_head
    )

    if federation_state in OBSTRUCTED_STATES:
        blockers.append("federation_cross_surface_obstruction")
    if federation_state in STALE_SEMANTIC_STATES:
        warnings.append("lean_semantic_reobservation_required")
    if not exact_head_context_fresh:
        warnings.append("ci_head_no_longer_matches_fresh_remote_head")
    if not current_bytes_observed:
        warnings.append("current_target_bytes_not_observed")
    if current_bytes_observed and not lean_semantic_fresh:
        warnings.append("lean_semantics_not_fresh_for_current_bytes")

    analysis_ready = bool(
        not blockers
        and exact_head_context_fresh
        and current_bytes_observed
        and lean_semantic_fresh
        and local_semantic_work_allowed
        and federation_state in FRESH_LOCAL_STATES
    )

    workspace_write_authority = (
        authority.get("workspace_write_authority_ready") is True
    )
    github_write_authority = (
        authority.get("github_write_authority_ready") is True
    )

    local_repair_ready = analysis_ready and workspace_write_authority

    aligned_committed = federation_state == "aligned_committed_workspace"
    remote_publish_ready = bool(
        local_repair_ready
        and aligned_committed
        and workspace.get("remote_local_aligned") is True
        and workspace.get("remote_mutation_eligible_before_authority_check")
        is True
        and github_write_authority
    )

    repair_candidate_retained = bool(
        classification == "lean_ci_repair"
        and target_path
        and not blockers
    )

    if blockers:
        status = OBSTRUCTED
        next_route = "repair_cross_surface_binding_before_edit"
    elif not exact_head_context_fresh:
        status = PARTIAL
        next_route = "reobserve_ci_on_current_remote_head"
    elif not current_bytes_observed:
        status = PARTIAL
        next_route = "observe_full_target_file_bytes"
    elif not lean_semantic_fresh:
        status = PARTIAL
        next_route = "reobserve_lean_semantics_on_current_bytes"
    elif not workspace_write_authority:
        status = PARTIAL
        next_route = "retain_repair_candidate_and_acquire_workspace_authority"
    else:
        status = READY
        if remote_publish_ready:
            next_route = "local_repair_then_reobserve_and_publish_when_still_aligned"
        elif workspace.get("remote_local_aligned") is not True:
            next_route = "local_repair_allowed_reconcile_revision_before_publish"
        else:
            next_route = "local_repair_then_reobserve_semantics_and_review_diff"

    evidence = {
        "repair_scope": "entire_target_file",
        "target_path": target_path,
        "filesystem_content_digest": fs_digest,
        "lean_source_content_digest": lean_digest,
        "federation_observations_digest": observations_digest,
        "workspace_state": federation_state,
        "remote_local_aligned": workspace.get("remote_local_aligned") is True,
        "target_matches_git_baseline": workspace.get(
            "target_matches_git_baseline"
        ),
        "ci_error_line_is_locator_not_scope": True,
        "full_target_file_audit_required": True,
        "raw_source_bytes_persisted_by_readiness_layer": False,
        "raw_ci_logs_persisted_by_readiness_layer": False,
        "source_authority_transferred": False,
    }

    packet_id = "kuuos-ci-repair-readiness-" + _sha(
        {
            "ci_packet_id": ci.get("packet_id"),
            "ci_head_sha": ci_head_sha,
            "federation_packet_id": federation.get("packet_id"),
            "federation_remote_head": federation_remote_head,
            "target_path": target_path,
            "evidence": evidence,
            "analysis_ready": analysis_ready,
            "local_repair_ready": local_repair_ready,
            "remote_publish_ready": remote_publish_ready,
            "blockers": sorted(set(blockers)),
            "warnings": sorted(set(warnings)),
        }
    )[:16]

    return CIRepairReadinessResult(
        VERSION,
        status,
        packet_id,
        target_path,
        ci_head_sha,
        federation_remote_head,
        exact_head_context_fresh,
        True,
        current_bytes_observed,
        lean_semantic_fresh,
        analysis_ready,
        local_repair_ready,
        remote_publish_ready,
        repair_candidate_retained,
        next_route,
        evidence,
        sorted(set(blockers)),
        sorted(set(warnings)),
    )
