#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from typing import Any, Mapping

from runtime import kuuos_github_mcp_sub_issue_binding_canary_v0_8 as _base
from runtime.kuuos_github_mcp_sub_issue_bidirectional_contract_v0_9 import (
    AUTHORITY_READY,
    BLOCKED,
    CHILD_TITLE_PREFIX,
    CHILD_VERSION,
    COMPENSATED,
    CONFIRMATION,
    GitHubMCPSubIssueBidirectionalCanaryResult,
    PLAN_VERSION,
    REQUEST_TITLE,
    REQUEST_VERSION,
    VERIFIED,
    mapping,
    validate_v0_9,
)
from runtime.kuuos_github_mcp_sub_issue_bidirectional_transport_v0_9 import (
    BidirectionalTransport,
    merge_records,
    patched_base_constants,
)


def build_github_mcp_sub_issue_bidirectional_canary(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
    transport: _base.MCPTransport | None = None,
) -> GitHubMCPSubIssueBidirectionalCanaryResult:
    ctx = mapping(runtime_context)
    authority = mapping(authority_packet)
    warnings: list[str] = []
    root_blockers: list[str] = []
    root = _base._safe_root(ctx.get("runtime_root"), root_blockers)
    plan_path = root / "github_mcp_sub_issue_bidirectional_canary_plan_v0_9.json"
    authority_path = (
        root / "github_mcp_sub_issue_bidirectional_canary_authority_v0_9.json"
    )
    receipt_path = (
        root / "github_mcp_sub_issue_bidirectional_canary_receipt_v0_9.json"
    )
    audit_path = (
        root / "github_mcp_sub_issue_bidirectional_canary_audit_v0_9.jsonl"
    )

    try:
        plan = _base._read_json(plan_path)
    except Exception as exc:
        plan = {}
        root_blockers.append(f"plan_read_failed:{type(exc).__name__}")
    blockers = root_blockers + validate_v0_9(
        ctx=ctx,
        authority=authority,
        plan=plan,
    )
    with patched_base_constants():
        _base._validate_plan(plan, blockers)

    repository = str(plan.get("repository_full_name", ""))
    base_branch = str(plan.get("base_branch", ""))
    base_sha = str(plan.get("base_sha", ""))
    nonce = str(plan.get("transaction_nonce", ""))
    parent_issue_number = int(plan.get("parent_issue_number", 0) or 0)
    server = mapping(plan.get("server"))
    server_image = str(server.get("image", ""))
    resolved_image_digest = str(ctx.get("resolved_image_digest", ""))
    child_title = f"{CHILD_TITLE_PREFIX}{nonce}"

    base_result = None
    wrapped: BidirectionalTransport | None = None
    owned_transport = False
    inner_transport = transport

    if not blockers and inner_transport is None:
        token_env = str(
            server.get("token_env", "GITHUB_PERSONAL_ACCESS_TOKEN")
        )
        if not os.environ.get(token_env):
            blockers.append("github_personal_access_token_missing")
        else:
            try:
                inner_transport = _base._open_stdio_transport(server, plan)
                owned_transport = True
            except Exception as exc:
                blockers.append(
                    f"stdio_transport_build_failed:{type(exc).__name__}"
                )

    if not blockers and inner_transport is not None:
        wrapped = BidirectionalTransport(
            inner_transport,
            repository_full_name=repository,
            parent_issue_number=parent_issue_number,
        )
        with tempfile.TemporaryDirectory(prefix="kuuos-v09-base-") as tmp:
            adapter_root = Path(tmp)
            (
                adapter_root
                / "github_mcp_sub_issue_binding_canary_plan_v0_8.json"
            ).write_text(
                json.dumps(plan, ensure_ascii=False, sort_keys=True),
                encoding="utf-8",
            )
            (
                adapter_root
                / "github_mcp_sub_issue_binding_canary_authority_v0_8.json"
            ).write_text(
                json.dumps(authority, ensure_ascii=False, sort_keys=True),
                encoding="utf-8",
            )
            base_ctx = {
                "runtime_root": str(adapter_root),
                "github_mcp_sub_issue_binding_canary_enabled": True,
                "apply_github_mcp_sub_issue_binding_canary": True,
                "execute_external_actions": ctx.get(
                    "execute_external_actions"
                ),
                "confirmation": ctx.get("confirmation"),
                "repository_full_name": ctx.get(
                    "repository_full_name",
                    repository,
                ),
                "base_sha": ctx.get("base_sha", base_sha),
                "transaction_nonce": ctx.get(
                    "transaction_nonce",
                    nonce,
                ),
                "parent_issue_number": ctx.get(
                    "parent_issue_number",
                    parent_issue_number,
                ),
                "resolved_image_digest": resolved_image_digest,
                "mode": ctx.get("mode", plan.get("mode", "mock")),
            }
            with patched_base_constants():
                base_result = (
                    _base.build_github_mcp_sub_issue_binding_canary(
                        runtime_context=base_ctx,
                        authority_packet=authority,
                        transport=wrapped,
                    )
                )

    if owned_transport and inner_transport is not None:
        try:
            inner_transport.close()
        except Exception as exc:
            warnings.append(
                f"transport_close_failed:{type(exc).__name__}"
            )

    if base_result is None:
        records: list[dict[str, Any]] = []
        base_status = BLOCKED
        child_issue_number = 0
        child_issue_id = 0
        parent_identity_verified = False
        parent_subissues_preflight_empty = False
        child_created_verified = False
        binding_added_verified = False
        binding_removed_verified = False
        child_closed_verified = False
        compensation_attempted = False
        compensation_binding_removed = False
        compensation_child_closed = False
    else:
        records = merge_records(
            base_result.records,
            wrapped.extra_records if wrapped else {},
        )
        blockers.extend(base_result.blockers)
        if wrapped:
            blockers.extend(wrapped.extra_blockers)
        warnings.extend(base_result.warnings)
        base_status = base_result.status
        child_issue_number = base_result.child_issue_number
        child_issue_id = base_result.child_issue_id
        child_title = base_result.child_title
        parent_identity_verified = base_result.parent_identity_verified
        parent_subissues_preflight_empty = (
            base_result.parent_subissues_preflight_empty
        )
        child_created_verified = base_result.child_created_verified
        binding_added_verified = base_result.binding_added_verified
        binding_removed_verified = base_result.binding_removed_verified
        child_closed_verified = base_result.child_closed_verified
        compensation_attempted = base_result.compensation_attempted
        compensation_binding_removed = (
            base_result.compensation_binding_removed
        )
        compensation_child_closed = base_result.compensation_child_closed

    child_parent_preflight_absent = bool(
        wrapped and wrapped.child_parent_preflight_absent
    )
    child_parent_added_verified = bool(
        wrapped and wrapped.child_parent_added_verified
    )
    child_parent_removed_verified = bool(
        wrapped and wrapped.child_parent_removed_verified
    )
    compensation_child_parent_removed = bool(
        wrapped and wrapped.compensation_child_parent_removed
    )

    primary_verified = (
        base_status == VERIFIED
        and child_parent_preflight_absent
        and child_parent_added_verified
        and child_parent_removed_verified
        and not blockers
    )
    status = VERIFIED if primary_verified else BLOCKED
    if (
        not primary_verified
        and base_status == COMPENSATED
        and compensation_child_parent_removed
    ):
        status = COMPENSATED

    packet_id = (
        "kuuos-github-mcp-sub-issue-bidirectional-"
        + _base._sha256(
            [repository, base_sha, nonce, parent_issue_number]
        )[:16]
    )
    result = GitHubMCPSubIssueBidirectionalCanaryResult(
        version=PLAN_VERSION,
        status=status,
        packet_id=packet_id,
        runtime_root=str(root),
        plan_path=str(plan_path),
        authority_path=str(authority_path),
        receipt_path=str(receipt_path),
        audit_path=str(audit_path),
        repository_full_name=repository,
        base_branch=base_branch,
        base_sha=base_sha,
        server_image=server_image,
        resolved_image_digest=resolved_image_digest,
        transaction_nonce=nonce,
        parent_issue_number=parent_issue_number,
        child_issue_number=child_issue_number,
        child_issue_id=child_issue_id,
        child_title=child_title,
        parent_identity_verified=parent_identity_verified,
        parent_subissues_preflight_empty=(
            parent_subissues_preflight_empty
        ),
        child_created_verified=child_created_verified,
        child_parent_preflight_absent=(
            child_parent_preflight_absent
        ),
        binding_added_verified=binding_added_verified,
        child_parent_added_verified=child_parent_added_verified,
        binding_removed_verified=binding_removed_verified,
        child_parent_removed_verified=child_parent_removed_verified,
        child_closed_verified=child_closed_verified,
        compensation_attempted=compensation_attempted,
        compensation_binding_removed=compensation_binding_removed,
        compensation_child_parent_removed=(
            compensation_child_parent_removed
        ),
        compensation_child_closed=compensation_child_closed,
        records=records,
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
    )
    if authority.get("receipt_write_allowed") is True:
        _base._write_json(receipt_path, result.to_dict())
    if authority.get("audit_append_allowed") is True:
        _base._append_jsonl(audit_path, records)
    return result
