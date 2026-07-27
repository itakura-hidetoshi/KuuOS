#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import os
import time
from typing import Any, Callable, Mapping

from runtime.kuuos_github_mcp_server_bridge_v0_1 import (
    ALLOWED_TOOLSETS,
    OFFICIAL_IMAGE_PREFIX,
    MCPTransport,
    MockGitHubMCPTransport,
    OfficialGitHubMCPStdioClient,
    _append_jsonl,
    _is_write_tool,
    _mapping,
    _read_json,
    _repository_from_arguments,
    _safe_root,
    _sha256,
    _stdio_command,
    _string_list,
    _tool_map,
    _write_json,
)
from runtime.kuuos_runtime_daemon_qi_github_tool_bridge_v2_3 import (
    build_qi_github_tool_bridge,
)

PLAN_VERSION = "kuuos_github_mcp_server_bridge_plan_v0_2"
AUTHORITY_READY = "KUUOS_GITHUB_MCP_WRITE_AUTHORITY_READY"

DIRECT_MCP_EXACT_GIT_TOOLS = frozenset(
    {
        "create_branch",
        "create_or_update_file",
        "delete_file",
        "merge_pull_request",
        "push_files",
        "update_pull_request_branch",
    }
)

EXACT_GIT_ACTION_KINDS = frozenset(
    {
        "create_branch",
        "update_file",
        "file_patch",
        "merge_pr",
    }
)


@dataclass(frozen=True)
class GitHubMCPWriteBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    plan_path: str
    authority_path: str
    receipt_path: str
    audit_path: str
    delegation_plan_path: str
    mode: str
    repository_full_name: str
    base_branch: str
    base_sha: str
    read_only: bool
    lockdown_mode: bool
    direct_applied_count: int
    delegated_applied_count: int
    blocked_count: int
    skipped_count: int
    records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _is_sha(value: Any) -> bool:
    text = str(value)
    return len(text) == 40 and all(ch in "0123456789abcdef" for ch in text.lower())


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    repository = str(plan.get("repository_full_name", ""))
    if repository.count("/") != 1:
        blockers.append("repository_full_name_invalid")
    if not str(plan.get("base_branch", "")):
        blockers.append("base_branch_missing")
    if not _is_sha(plan.get("base_sha", "")):
        blockers.append("base_sha_invalid")
    if plan.get("write_capable") is not True:
        blockers.append("write_capable_not_true")
    if plan.get("read_only") is not False:
        blockers.append("write_capable_plan_requires_read_only_false")
    if plan.get("lockdown_mode") is not True:
        blockers.append("lockdown_mode_not_true")

    server = _mapping(plan.get("server"))
    if server.get("kind") != "official_github_mcp_server":
        blockers.append("server_kind_invalid")
    toolsets = _string_list(server.get("toolsets"))
    if not toolsets:
        blockers.append("toolsets_allowlist_empty")
    elif "all" in toolsets or any(toolset not in ALLOWED_TOOLSETS for toolset in toolsets):
        blockers.append("toolsets_not_bounded")
    tools = _string_list(server.get("tools"))
    if not tools:
        blockers.append("tools_allowlist_empty")
    image = str(server.get("image", OFFICIAL_IMAGE_PREFIX))
    if str(server.get("launcher", "docker")) == "docker" and not (
        image == OFFICIAL_IMAGE_PREFIX
        or image.startswith(OFFICIAL_IMAGE_PREFIX + ":")
        or (image.startswith(OFFICIAL_IMAGE_PREFIX) and "@sha256:" in image)
    ):
        blockers.append("official_image_required")


def _write_gate_blockers(
    *,
    runtime_context: Mapping[str, Any],
    authority: Mapping[str, Any],
    plan: Mapping[str, Any],
    operation: Mapping[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if runtime_context.get("execute_external_actions") is not True:
        blockers.append("runtime_execute_external_actions_not_true")
    if plan.get("execute_external_actions") is not True:
        blockers.append("plan_execute_external_actions_not_true")
    if authority.get("external_action_allowed") is not True:
        blockers.append("external_action_not_allowed")
    if authority.get("mcp_write_tool_call_allowed") is not True:
        blockers.append("mcp_write_tool_call_not_allowed")
    if operation.get("approved") is not True:
        blockers.append("operation_not_approved")
    if str(operation.get("expected_base_sha", "")) != str(plan.get("base_sha", "")):
        blockers.append("expected_base_sha_mismatch")
    return blockers


def _exact_action_blockers(
    *,
    action: Mapping[str, Any],
    repository: str,
    base_branch: str,
    base_sha: str,
    authority: Mapping[str, Any],
) -> list[str]:
    blockers: list[str] = []
    kind = str(action.get("kind", ""))
    if kind not in EXACT_GIT_ACTION_KINDS:
        blockers.append("exact_git_action_kind_invalid")
    if authority.get("exact_git_delegation_allowed") is not True:
        blockers.append("exact_git_delegation_not_allowed")
    action_repository = str(action.get("repository_full_name", repository))
    if action_repository != repository:
        blockers.append("exact_git_action_repository_mismatch")
    action_base = str(action.get("base_branch", base_branch))
    if action_base != base_branch:
        blockers.append("exact_git_action_base_branch_mismatch")

    if kind == "create_branch":
        if not str(action.get("branch", "")):
            blockers.append("create_branch_name_missing")
        if not _is_sha(action.get("sha", "")):
            blockers.append("create_branch_sha_invalid")
    elif kind in {"update_file", "file_patch"}:
        if not str(action.get("branch", "")):
            blockers.append("file_action_branch_missing")
        if not str(action.get("path", "")):
            blockers.append("file_action_path_missing")
        if not str(action.get("sha", "")):
            blockers.append("file_action_content_sha_missing")
        expected_head = str(action.get("expected_branch_head_sha", ""))
        if expected_head and not _is_sha(expected_head):
            blockers.append("expected_branch_head_sha_invalid")
    elif kind == "merge_pr":
        try:
            pull_number = int(action.get("pr_number", 0) or 0)
        except (TypeError, ValueError):
            pull_number = 0
        if pull_number <= 0:
            blockers.append("merge_pr_number_invalid")
        if not _is_sha(action.get("expected_head_sha", "")):
            blockers.append("merge_expected_head_sha_invalid")
        if str(action.get("expected_base_sha", base_sha)) != base_sha:
            blockers.append("merge_expected_base_sha_mismatch")
    return blockers


def _record(
    *,
    index: int,
    kind: str,
    tool: str,
    execution_path: str,
    operation: Mapping[str, Any],
    status: str,
    result: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "index": index,
        "kind": kind,
        "tool": tool,
        "execution_path": execution_path,
        "status": status,
        "operation_digest": _sha256(operation),
        "result": dict(result),
        "blockers": sorted(set(blockers)),
        "epoch": int(time.time()),
    }
    record["record_digest"] = _sha256(record)
    return record


def build_github_mcp_write_bridge(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
    transport: MCPTransport | None = None,
    qi_transport: Callable[[str, Mapping[str, Any], str], dict[str, Any]] | None = None,
) -> GitHubMCPWriteBridgeResult:
    ctx = _mapping(runtime_context)
    authority = _mapping(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records_by_index: dict[int, dict[str, Any]] = {}

    root = _safe_root(ctx.get("runtime_root"), blockers)
    plan_path = root / "github_mcp_server_bridge_plan_v0_2.json"
    authority_path = root / "github_mcp_server_bridge_authority_v0_2.json"
    receipt_path = root / "github_mcp_server_bridge_receipt_v0_2.json"
    audit_path = root / "github_mcp_server_bridge_audit_v0_2.jsonl"
    delegation_plan_path = root / "github_tool_bridge_plan.json"

    if ctx.get("github_mcp_server_bridge_enabled") is not True:
        blockers.append("github_mcp_server_bridge_enabled_not_true")
    if ctx.get("apply_github_mcp_server_bridge") is not True:
        blockers.append("apply_github_mcp_server_bridge_not_true")
    if authority.get("authority_status") != AUTHORITY_READY:
        blockers.append("github_mcp_write_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "tool_discovery_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))

    plan = _read_json(plan_path)
    _validate_plan(plan, blockers)
    repository = str(plan.get("repository_full_name", ""))
    base_branch = str(plan.get("base_branch", ""))
    base_sha = str(plan.get("base_sha", ""))
    read_only = plan.get("read_only") is True
    lockdown_mode = plan.get("lockdown_mode") is True
    mode = str(plan.get("mode", ctx.get("mode", "mock")))
    if mode not in {"mock", "stdio"}:
        blockers.append("mode_invalid")

    server = _mapping(plan.get("server"))
    allowed_tools = frozenset(_string_list(server.get("tools")))
    operations_raw = plan.get("operations", [])
    operations = (
        [dict(item) for item in operations_raw if isinstance(item, Mapping)]
        if isinstance(operations_raw, list)
        else []
    )
    if not operations and not blockers:
        warnings.append("operations_empty")

    active_transport = transport
    owns_transport = False
    discovered_tools: dict[str, dict[str, Any]] = {}
    if not blockers and active_transport is None:
        if mode == "mock":
            active_transport = MockGitHubMCPTransport()
        else:
            token_env = str(server.get("token_env", "GITHUB_PERSONAL_ACCESS_TOKEN"))
            if not os.environ.get(token_env):
                blockers.append("github_personal_access_token_missing")
            else:
                try:
                    command, generated_env = _stdio_command(server, plan)
                    active_transport = OfficialGitHubMCPStdioClient(command, generated_env)
                    owns_transport = True
                except Exception as exc:  # noqa: BLE001
                    blockers.append(f"stdio_transport_build_failed:{type(exc).__name__}")

    if not blockers and active_transport is not None:
        try:
            list_response = active_transport.list_tools()
            if "error" in list_response:
                blockers.append("tool_discovery_protocol_error")
            else:
                discovered_tools = _tool_map(list_response)
                missing = sorted(tool for tool in allowed_tools if tool not in discovered_tools)
                if missing:
                    blockers.append("allowed_tools_not_discovered:" + ",".join(missing))
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"tool_discovery_failed:{type(exc).__name__}")

    delegated: list[tuple[int, dict[str, Any], dict[str, Any]]] = []
    if not blockers and active_transport is not None:
        for index, operation in enumerate(operations):
            kind = str(operation.get("kind", ""))
            if kind == "list_tools":
                records_by_index[index] = _record(
                    index=index,
                    kind=kind,
                    tool="",
                    execution_path="official_mcp",
                    operation=operation,
                    status="applied",
                    result={"tools": sorted(discovered_tools)},
                    blockers=[],
                )
                continue

            if kind == "call_tool":
                tool_name = str(operation.get("tool", ""))
                arguments = _mapping(operation.get("arguments"))
                local_blockers: list[str] = []
                metadata = discovered_tools.get(tool_name, {})
                if tool_name not in allowed_tools:
                    local_blockers.append("tool_not_allowlisted")
                if tool_name not in discovered_tools:
                    local_blockers.append("tool_not_discovered")
                argument_repository = _repository_from_arguments(arguments)
                if argument_repository and argument_repository != repository:
                    local_blockers.append("operation_repository_mismatch")
                is_write = _is_write_tool(tool_name, metadata)
                if is_write:
                    if argument_repository != repository:
                        local_blockers.append("write_repository_scope_missing_or_mismatched")
                    if tool_name in DIRECT_MCP_EXACT_GIT_TOOLS:
                        local_blockers.append("exact_git_action_required")
                    argument_base = str(arguments.get("base", arguments.get("base_branch", "")))
                    if argument_base and argument_base != base_branch:
                        local_blockers.append("write_base_branch_mismatch")
                    local_blockers.extend(
                        _write_gate_blockers(
                            runtime_context=ctx,
                            authority=authority,
                            plan=plan,
                            operation=operation,
                        )
                    )
                result: dict[str, Any] = {}
                if not local_blockers:
                    try:
                        result = active_transport.call_tool(tool_name, arguments)
                        if "error" in result or _mapping(result.get("result")).get("isError") is True:
                            local_blockers.append("tool_call_returned_error")
                    except Exception as exc:  # noqa: BLE001
                        result = {"error": f"{type(exc).__name__}:{exc}"}
                        local_blockers.append("tool_call_exception")
                records_by_index[index] = _record(
                    index=index,
                    kind=kind,
                    tool=tool_name,
                    execution_path="official_mcp",
                    operation=operation,
                    status="applied" if not local_blockers else "blocked",
                    result=result,
                    blockers=local_blockers,
                )
                continue

            if kind == "exact_git_action":
                action = dict(_mapping(operation.get("action")))
                local_blockers = _write_gate_blockers(
                    runtime_context=ctx,
                    authority=authority,
                    plan=plan,
                    operation=operation,
                )
                local_blockers.extend(
                    _exact_action_blockers(
                        action=action,
                        repository=repository,
                        base_branch=base_branch,
                        base_sha=base_sha,
                        authority=authority,
                    )
                )
                if local_blockers:
                    records_by_index[index] = _record(
                        index=index,
                        kind=kind,
                        tool=str(action.get("kind", "")),
                        execution_path="exact_sha_rest_delegate",
                        operation=operation,
                        status="blocked",
                        result={},
                        blockers=local_blockers,
                    )
                else:
                    action.setdefault("repository_full_name", repository)
                    action.setdefault("base_branch", base_branch)
                    delegated.append((index, operation, action))
                continue

            records_by_index[index] = _record(
                index=index,
                kind=kind,
                tool="",
                execution_path="none",
                operation=operation,
                status="blocked",
                result={},
                blockers=["operation_kind_invalid"],
            )

    if delegated and not blockers:
        qi_plan = {
            "mode": "mock" if mode == "mock" else "real",
            "execute_external_actions": plan.get("execute_external_actions") is True,
            "token_env": str(server.get("token_env", "GITHUB_PERSONAL_ACCESS_TOKEN")),
            "repository_full_name": repository,
            "base_branch": base_branch,
            "allowed_base_branch": base_branch,
            "actions": [action for _, _, action in delegated],
        }
        _write_json(delegation_plan_path, qi_plan)
        qi_license = {
            "license_status": "QI_GITHUB_TOOL_BRIDGE_LICENSE_READY",
            "plan_read_allowed": True,
            "external_action_allowed": (
                authority.get("external_action_allowed") is True
                and authority.get("exact_git_delegation_allowed") is True
            ),
            "receipt_write_allowed": authority.get("receipt_write_allowed") is True,
            "audit_append_allowed": authority.get("audit_append_allowed") is True,
        }
        try:
            qi_result = build_qi_github_tool_bridge(
                runtime_context={
                    "runtime_root": str(root),
                    "qi_github_tool_bridge_enabled": True,
                    "apply_github_tool_bridge": True,
                    "execute_external_actions": ctx.get("execute_external_actions") is True,
                },
                bridge_license_packet=qi_license,
                transport=qi_transport,
            )
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"exact_git_delegation_exception:{type(exc).__name__}")
            for index, operation, action in delegated:
                records_by_index[index] = _record(
                    index=index,
                    kind="exact_git_action",
                    tool=str(action.get("kind", "")),
                    execution_path="exact_sha_rest_delegate",
                    operation=operation,
                    status="blocked",
                    result={"error": f"{type(exc).__name__}:{exc}"},
                    blockers=["exact_git_delegation_exception"],
                )
        else:
            for offset, (index, operation, action) in enumerate(delegated):
                if offset < len(qi_result.records):
                    delegated_record = qi_result.records[offset]
                    delegated_blockers = [str(item) for item in delegated_record.get("blockers", [])]
                    status = (
                        "applied"
                        if delegated_record.get("status") == "applied" and not delegated_blockers
                        else "blocked"
                    )
                    result = _mapping(delegated_record.get("result"))
                else:
                    delegated_blockers = ["delegation_record_missing"]
                    status = "blocked"
                    result = {}
                records_by_index[index] = _record(
                    index=index,
                    kind="exact_git_action",
                    tool=str(action.get("kind", "")),
                    execution_path="exact_sha_rest_delegate",
                    operation=operation,
                    status=status,
                    result=result,
                    blockers=delegated_blockers,
                )
            if qi_result.blockers:
                warnings.append(
                    "exact_git_delegation_bridge_blockers:"
                    + ",".join(sorted(set(qi_result.blockers)))
                )

    if owns_transport and active_transport is not None:
        active_transport.close()

    records = [records_by_index[index] for index in sorted(records_by_index)]
    if authority.get("audit_append_allowed") is True:
        for record in records:
            _append_jsonl(audit_path, record)

    direct_applied = sum(
        record.get("status") == "applied"
        and record.get("execution_path") == "official_mcp"
        and record.get("kind") == "call_tool"
        for record in records
    )
    delegated_applied = sum(
        record.get("status") == "applied"
        and record.get("execution_path") == "exact_sha_rest_delegate"
        for record in records
    )
    blocked = sum(record.get("status") == "blocked" for record in records)
    skipped = len(operations) - len(records)
    if blockers:
        status = "KUUOS_GITHUB_MCP_WRITE_BRIDGE_BLOCKED"
    elif blocked:
        status = "KUUOS_GITHUB_MCP_WRITE_BRIDGE_PARTIAL"
    elif direct_applied or delegated_applied or any(
        record.get("kind") == "list_tools" and record.get("status") == "applied"
        for record in records
    ):
        status = "KUUOS_GITHUB_MCP_WRITE_BRIDGE_APPLIED"
    else:
        status = "KUUOS_GITHUB_MCP_WRITE_BRIDGE_IDLE"

    packet_id = "kuuos-github-mcp-write-" + _sha256(
        {"plan": plan, "records": records, "blockers": blockers}
    )[:16]
    receipt = {
        "version": "kuuos_github_mcp_server_bridge_v0_2",
        "status": status,
        "packet_id": packet_id,
        "mode": mode,
        "repository_full_name": repository,
        "base_branch": base_branch,
        "base_sha": base_sha,
        "read_only": read_only,
        "lockdown_mode": lockdown_mode,
        "direct_applied_count": direct_applied,
        "delegated_applied_count": delegated_applied,
        "blocked_count": blocked,
        "skipped_count": skipped,
        "records": records,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if authority.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)

    return GitHubMCPWriteBridgeResult(
        "kuuos_github_mcp_server_bridge_v0_2",
        status,
        packet_id,
        str(root),
        str(plan_path),
        str(authority_path),
        str(receipt_path),
        str(audit_path),
        str(delegation_plan_path),
        mode,
        repository,
        base_branch,
        base_sha,
        read_only,
        lockdown_mode,
        direct_applied,
        delegated_applied,
        blocked,
        skipped,
        records,
        sorted(set(blockers)),
        warnings,
    )
