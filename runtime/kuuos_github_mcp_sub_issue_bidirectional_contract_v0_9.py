#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

PLAN_VERSION = "kuuos_github_mcp_sub_issue_bidirectional_canary_plan_v0_9"
REQUEST_VERSION = "kuuos_github_mcp_sub_issue_bidirectional_canary_request_v0_9"
CHILD_VERSION = "kuuos_github_mcp_sub_issue_bidirectional_canary_child_v0_9"
AUTHORITY_READY = "KUUOS_GITHUB_MCP_SUB_ISSUE_BIDIRECTIONAL_CANARY_AUTHORITY_READY"
CONFIRMATION = "RUN_KUUOS_GITHUB_MCP_SUB_ISSUE_BIDIRECTIONAL_CANARY"
VERIFIED = "KUUOS_GITHUB_MCP_SUB_ISSUE_BIDIRECTIONAL_CANARY_VERIFIED"
COMPENSATED = "KUUOS_GITHUB_MCP_SUB_ISSUE_BIDIRECTIONAL_CANARY_COMPENSATED"
BLOCKED = "KUUOS_GITHUB_MCP_SUB_ISSUE_BIDIRECTIONAL_CANARY_BLOCKED"
REQUEST_TITLE = "[KuuOS MCP Sub-Issue Bidirectional Canary v0.9]"
CHILD_TITLE_PREFIX = "[KuuOS MCP Sub-Issue Child v0.9] "


@dataclass(frozen=True)
class GitHubMCPSubIssueBidirectionalCanaryResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    plan_path: str
    authority_path: str
    receipt_path: str
    audit_path: str
    repository_full_name: str
    base_branch: str
    base_sha: str
    server_image: str
    resolved_image_digest: str
    transaction_nonce: str
    parent_issue_number: int
    child_issue_number: int
    child_issue_id: int
    child_title: str
    parent_identity_verified: bool
    parent_subissues_preflight_empty: bool
    child_created_verified: bool
    child_parent_preflight_absent: bool
    binding_added_verified: bool
    child_parent_added_verified: bool
    binding_removed_verified: bool
    child_parent_removed_verified: bool
    child_closed_verified: bool
    compensation_attempted: bool
    compensation_binding_removed: bool
    compensation_child_parent_removed: bool
    compensation_child_closed: bool
    records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def parent_exact_blockers(
    observed: Any,
    *,
    parent_issue_number: int,
    parent_title: str,
    repository_full_name: str,
) -> list[str]:
    payload = mapping(observed)
    parent = payload.get("parent")
    if not isinstance(parent, Mapping):
        return ["observed_child_parent_missing"]
    value = dict(parent)
    local: list[str] = []
    if int(value.get("number", 0) or 0) != parent_issue_number:
        local.append("observed_child_parent_number_mismatch")
    if str(value.get("title", "")) != parent_title:
        local.append("observed_child_parent_title_mismatch")
    if str(value.get("state", "")).lower() != "open":
        local.append("observed_child_parent_state_not_open")
    if str(value.get("repository", "")) != repository_full_name:
        local.append("observed_child_parent_repository_mismatch")
    expected_suffix = f"/issues/{parent_issue_number}"
    if not str(value.get("url", "")).rstrip("/").endswith(expected_suffix):
        local.append("observed_child_parent_url_mismatch")
    return local


def parent_absent_blockers(observed: Any) -> list[str]:
    payload = mapping(observed)
    if set(payload) != {"parent"}:
        return ["observed_child_parent_absence_shape_invalid"]
    if payload.get("parent") is not None:
        return ["observed_child_parent_residual"]
    return []


def validate_v0_9(
    *,
    ctx: Mapping[str, Any],
    authority: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if ctx.get("github_mcp_sub_issue_bidirectional_canary_enabled") is not True:
        blockers.append("github_mcp_sub_issue_bidirectional_canary_enabled_not_true")
    if ctx.get("apply_github_mcp_sub_issue_bidirectional_canary") is not True:
        blockers.append("apply_github_mcp_sub_issue_bidirectional_canary_not_true")
    if authority.get("authority_status") != AUTHORITY_READY:
        blockers.append("sub_issue_bidirectional_canary_authority_not_ready")
    for field in (
        "upward_parent_reobservation_allowed",
        "compensating_parent_reobservation_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    if plan.get("request_issue_title") != REQUEST_TITLE:
        blockers.append("request_issue_title_invalid")
    if plan.get("request_version_marker") != REQUEST_VERSION:
        blockers.append("request_version_marker_invalid")
    if plan.get("child_title_prefix") != CHILD_TITLE_PREFIX:
        blockers.append("child_title_prefix_invalid")
    if plan.get("child_version_marker") != CHILD_VERSION:
        blockers.append("child_version_marker_invalid")
    if plan.get("upward_read_method") != "get_parent":
        blockers.append("upward_read_method_invalid")
    if plan.get("require_child_parent_preflight_absent") is not True:
        blockers.append("child_parent_preflight_contract_missing")
    if plan.get("require_child_parent_exact_when_attached") is not True:
        blockers.append("child_parent_attached_contract_missing")
    if plan.get("require_child_parent_absent_after_remove") is not True:
        blockers.append("child_parent_remove_contract_missing")
    return blockers
