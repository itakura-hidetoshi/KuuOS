#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import re
import time
from typing import Any, Mapping

from runtime.kuuos_github_mcp_live_write_verification_v0_3 import _normalize_tool_payload
from runtime.kuuos_github_mcp_live_canary_v0_4 import (
    _is_pinned_official_image,
    _tool_returned_error,
)
from runtime.kuuos_github_mcp_server_bridge_v0_1 import (
    MCPTransport,
    OfficialGitHubMCPStdioClient,
    _append_jsonl,
    _is_write_tool,
    _mapping,
    _read_json,
    _safe_root,
    _sha256,
    _stdio_command,
    _tool_map,
    _write_json,
)

PLAN_VERSION = "kuuos_github_mcp_label_canary_plan_v0_6"
AUTHORITY_READY = "KUUOS_GITHUB_MCP_LABEL_CANARY_AUTHORITY_READY"
CONFIRMATION = "RUN_KUUOS_GITHUB_MCP_LABEL_CANARY"
VERIFIED = "KUUOS_GITHUB_MCP_LABEL_CANARY_VERIFIED"
COMPENSATED = "KUUOS_GITHUB_MCP_LABEL_CANARY_COMPENSATED"
BLOCKED = "KUUOS_GITHUB_MCP_LABEL_CANARY_BLOCKED"
NONCE_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{7,31}")
COLOR_PATTERN = re.compile(r"[0-9a-fA-F]{6}")


@dataclass(frozen=True)
class GitHubMCPLabelCanaryResult:
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
    label_name: str
    label_color: str
    label_description: str
    preflight_absent: bool
    created_verified: bool
    deleted_verified: bool
    compensation_attempted: bool
    compensation_deleted: bool
    records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _is_sha(value: Any) -> bool:
    text = str(value)
    return len(text) == 40 and all(ch in "0123456789abcdef" for ch in text.lower())


def _record(
    *,
    phase: str,
    tool: str,
    arguments: Mapping[str, Any],
    response: Mapping[str, Any],
    observed: Any,
    status: str,
    blockers: list[str],
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "phase": phase,
        "tool": tool,
        "arguments_digest": _sha256(arguments),
        "response": dict(response),
        "observed": observed,
        "observed_digest": _sha256(observed),
        "status": status,
        "blockers": sorted(set(blockers)),
        "epoch": int(time.time()),
    }
    record["record_digest"] = _sha256(record)
    return record


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("plan_version_invalid")
    repository = str(plan.get("repository_full_name", ""))
    if repository.count("/") != 1:
        blockers.append("repository_full_name_invalid")
    if str(plan.get("base_branch", "")) != "main":
        blockers.append("base_branch_not_main")
    if not _is_sha(plan.get("base_sha", "")):
        blockers.append("base_sha_invalid")
    if plan.get("write_capable") is not True:
        blockers.append("write_capable_not_true")
    if plan.get("read_only") is not False:
        blockers.append("label_canary_requires_read_only_false")
    if plan.get("lockdown_mode") is not True:
        blockers.append("lockdown_mode_not_true")
    if plan.get("execute_external_actions") is not True:
        blockers.append("plan_execute_external_actions_not_true")
    if plan.get("confirmation") != CONFIRMATION:
        blockers.append("plan_confirmation_invalid")

    nonce = str(plan.get("label_nonce", ""))
    if NONCE_PATTERN.fullmatch(nonce) is None:
        blockers.append("label_nonce_invalid")
    prefix = str(plan.get("label_prefix", ""))
    if prefix != "kuuos-mcp-canary-":
        blockers.append("label_prefix_invalid")
    color = str(plan.get("label_color", ""))
    if COLOR_PATTERN.fullmatch(color) is None:
        blockers.append("label_color_invalid")
    marker = str(plan.get("description_marker", ""))
    if marker != "KUUOS_GITHUB_MCP_LABEL_CANARY v0.6":
        blockers.append("description_marker_invalid")

    server = _mapping(plan.get("server"))
    if server.get("kind") != "official_github_mcp_server":
        blockers.append("server_kind_invalid")
    if not _is_pinned_official_image(server.get("image", "")):
        blockers.append("official_server_image_not_pinned")
    toolsets = server.get("toolsets")
    if not isinstance(toolsets, list) or set(str(item) for item in toolsets) != {"labels"}:
        blockers.append("labels_toolset_required")
    tools = server.get("tools")
    if not isinstance(tools, list) or set(str(item) for item in tools) != {
        "label_write",
        "get_label",
    }:
        blockers.append("label_canary_tool_allowlist_invalid")


def _error_text(response: Mapping[str, Any]) -> str:
    try:
        return json.dumps(response, ensure_ascii=False, sort_keys=True, default=str).lower()
    except Exception:  # noqa: BLE001
        return str(response).lower()


def _is_not_found_response(response: Mapping[str, Any]) -> bool:
    if not _tool_returned_error(response):
        return False
    text = _error_text(response)
    return "not found" in text or "404" in text


def _call_tool(
    transport: MCPTransport,
    *,
    phase: str,
    tool: str,
    arguments: Mapping[str, Any],
) -> tuple[dict[str, Any], Any, list[str]]:
    local: list[str] = []
    response: dict[str, Any]
    observed: Any = {}
    try:
        response = transport.call_tool(tool, arguments)
        if _tool_returned_error(response):
            local.append(f"{phase}_tool_returned_error")
        else:
            observed = _normalize_tool_payload(response)
    except Exception as exc:  # noqa: BLE001
        response = {"error": f"{type(exc).__name__}:{exc}"}
        local.append(f"{phase}_tool_exception")
    return response, observed, local


def _call_get_label(
    transport: MCPTransport,
    *,
    phase: str,
    arguments: Mapping[str, Any],
    expect_absent: bool,
) -> tuple[dict[str, Any], Any, list[str]]:
    local: list[str] = []
    response: dict[str, Any]
    observed: Any = {}
    try:
        response = transport.call_tool("get_label", arguments)
        if expect_absent:
            if _is_not_found_response(response):
                observed = {"absent": True, "name": str(arguments.get("name", ""))}
            elif _tool_returned_error(response):
                local.append(f"{phase}_unexpected_tool_error")
            else:
                observed = _normalize_tool_payload(response)
                local.append(f"{phase}_label_unexpectedly_present")
        elif _tool_returned_error(response):
            local.append(f"{phase}_tool_returned_error")
        else:
            observed = _normalize_tool_payload(response)
    except Exception as exc:  # noqa: BLE001
        response = {"error": f"{type(exc).__name__}:{exc}"}
        local.append(f"{phase}_tool_exception")
    return response, observed, local


def _label_blockers(
    *,
    observed: Any,
    expected_name: str,
    expected_color: str,
    expected_description: str,
) -> list[str]:
    local: list[str] = []
    label = _mapping(observed)
    if str(label.get("name", "")) != expected_name:
        local.append("observed_label_name_mismatch")
    if str(label.get("color", "")).lower() != expected_color.lower():
        local.append("observed_label_color_mismatch")
    if str(label.get("description", "")) != expected_description:
        local.append("observed_label_description_mismatch")
    return local


def build_github_mcp_label_canary(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
    transport: MCPTransport | None = None,
) -> GitHubMCPLabelCanaryResult:
    ctx = _mapping(runtime_context)
    authority = _mapping(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []

    root = _safe_root(ctx.get("runtime_root"), blockers)
    plan_path = root / "github_mcp_label_canary_plan_v0_6.json"
    authority_path = root / "github_mcp_label_canary_authority_v0_6.json"
    receipt_path = root / "github_mcp_label_canary_receipt_v0_6.json"
    audit_path = root / "github_mcp_label_canary_audit_v0_6.jsonl"

    if ctx.get("github_mcp_label_canary_enabled") is not True:
        blockers.append("github_mcp_label_canary_enabled_not_true")
    if ctx.get("apply_github_mcp_label_canary") is not True:
        blockers.append("apply_github_mcp_label_canary_not_true")
    if ctx.get("execute_external_actions") is not True:
        blockers.append("runtime_execute_external_actions_not_true")
    if ctx.get("confirmation") != CONFIRMATION:
        blockers.append("runtime_confirmation_invalid")
    if authority.get("authority_status") != AUTHORITY_READY:
        blockers.append("label_canary_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "tool_discovery_allowed",
        "external_action_allowed",
        "mcp_write_tool_call_allowed",
        "post_write_reobservation_allowed",
        "compensating_delete_allowed",
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
    mode = str(plan.get("mode", ctx.get("mode", "mock")))
    if mode not in {"mock", "stdio"}:
        blockers.append("mode_invalid")
    if str(ctx.get("repository_full_name", repository)) != repository:
        blockers.append("runtime_repository_scope_mismatch")
    if str(ctx.get("base_sha", base_sha)) != base_sha:
        blockers.append("runtime_base_sha_mismatch")

    label_nonce = str(plan.get("label_nonce", ""))
    if str(ctx.get("label_nonce", label_nonce)) != label_nonce:
        blockers.append("runtime_label_nonce_mismatch")
    label_name = f"{str(plan.get('label_prefix', ''))}{label_nonce}"
    label_color = str(plan.get("label_color", "")).lower()
    label_description = f"{str(plan.get('description_marker', ''))} {label_nonce}"

    server = dict(_mapping(plan.get("server")))
    server_image = str(server.get("image", ""))
    resolved_image_digest = str(ctx.get("resolved_image_digest", ""))
    if mode == "stdio" and not resolved_image_digest.startswith("sha256:"):
        blockers.append("resolved_image_digest_missing")

    owner, repo = (repository.split("/", 1) + [""])[:2]
    active_transport = transport
    owns_transport = False
    if not blockers and active_transport is None:
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
                discovered = _tool_map(list_response)
                for required in ("label_write", "get_label"):
                    if required not in discovered:
                        blockers.append(f"required_tool_not_discovered:{required}")
                if "label_write" in discovered and not _is_write_tool(
                    "label_write", discovered["label_write"]
                ):
                    blockers.append("label_write_not_classified_write")
                if "get_label" in discovered and _is_write_tool(
                    "get_label", discovered["get_label"]
                ):
                    blockers.append("get_label_not_classified_read_only")
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"tool_discovery_failed:{type(exc).__name__}")

    preflight_absent = False
    created_verified = False
    deleted_verified = False
    compensation_attempted = False
    compensation_deleted = False
    create_attempted = False

    get_args = {"owner": owner, "repo": repo, "name": label_name}
    if not blockers and active_transport is not None:
        response, observed, local = _call_get_label(
            active_transport,
            phase="preflight",
            arguments=get_args,
            expect_absent=True,
        )
        preflight_absent = not local and _mapping(observed).get("absent") is True
        records.append(
            _record(
                phase="preflight",
                tool="get_label",
                arguments=get_args,
                response=response,
                observed=observed,
                status="verified_absent" if preflight_absent else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if preflight_absent and not blockers and active_transport is not None:
        create_attempted = True
        create_args = {
            "method": "create",
            "owner": owner,
            "repo": repo,
            "name": label_name,
            "color": label_color,
            "description": label_description,
        }
        response, observed, local = _call_tool(
            active_transport,
            phase="create",
            tool="label_write",
            arguments=create_args,
        )
        records.append(
            _record(
                phase="create",
                tool="label_write",
                arguments=create_args,
                response=response,
                observed=observed,
                status="applied" if not local else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if create_attempted and not blockers and active_transport is not None:
        response, observed, local = _call_get_label(
            active_transport,
            phase="verify_created",
            arguments=get_args,
            expect_absent=False,
        )
        if not local:
            local.extend(
                _label_blockers(
                    observed=observed,
                    expected_name=label_name,
                    expected_color=label_color,
                    expected_description=label_description,
                )
            )
        created_verified = not local
        records.append(
            _record(
                phase="verify_created",
                tool="get_label",
                arguments=get_args,
                response=response,
                observed=observed,
                status="verified" if created_verified else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if created_verified and not blockers and active_transport is not None:
        delete_args = {
            "method": "delete",
            "owner": owner,
            "repo": repo,
            "name": label_name,
        }
        response, observed, local = _call_tool(
            active_transport,
            phase="delete",
            tool="label_write",
            arguments=delete_args,
        )
        records.append(
            _record(
                phase="delete",
                tool="label_write",
                arguments=delete_args,
                response=response,
                observed=observed,
                status="applied" if not local else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if created_verified and not blockers and active_transport is not None:
        response, observed, local = _call_get_label(
            active_transport,
            phase="verify_deleted",
            arguments=get_args,
            expect_absent=True,
        )
        deleted_verified = not local and _mapping(observed).get("absent") is True
        records.append(
            _record(
                phase="verify_deleted",
                tool="get_label",
                arguments=get_args,
                response=response,
                observed=observed,
                status="verified_absent" if deleted_verified else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if (
        create_attempted
        and preflight_absent
        and not deleted_verified
        and active_transport is not None
    ):
        compensation_attempted = True
        delete_args = {
            "method": "delete",
            "owner": owner,
            "repo": repo,
            "name": label_name,
        }
        response, observed, local = _call_tool(
            active_transport,
            phase="compensating_delete",
            tool="label_write",
            arguments=delete_args,
        )
        records.append(
            _record(
                phase="compensating_delete",
                tool="label_write",
                arguments=delete_args,
                response=response,
                observed=observed,
                status="applied" if not local else "warning",
                blockers=local,
            )
        )
        if local:
            warnings.extend(local)

        read_response, read_observed, read_local = _call_get_label(
            active_transport,
            phase="verify_compensation",
            arguments=get_args,
            expect_absent=True,
        )
        compensation_deleted = (
            not read_local and _mapping(read_observed).get("absent") is True
        )
        records.append(
            _record(
                phase="verify_compensation",
                tool="get_label",
                arguments=get_args,
                response=read_response,
                observed=read_observed,
                status="verified_absent" if compensation_deleted else "blocked",
                blockers=read_local,
            )
        )
        if read_local:
            warnings.extend(read_local)

    if owns_transport and active_transport is not None:
        active_transport.close()

    if preflight_absent and created_verified and deleted_verified and not blockers:
        status = VERIFIED
    elif compensation_attempted and compensation_deleted:
        status = COMPENSATED
    else:
        status = BLOCKED

    packet_id = "kuuos-github-mcp-label-canary-" + _sha256(
        {
            "plan": plan,
            "records": records,
            "blockers": blockers,
            "resolved_image_digest": resolved_image_digest,
        }
    )[:16]
    receipt = {
        "version": "kuuos_github_mcp_label_canary_v0_6",
        "status": status,
        "packet_id": packet_id,
        "repository_full_name": repository,
        "base_branch": base_branch,
        "base_sha": base_sha,
        "server_image": server_image,
        "resolved_image_digest": resolved_image_digest,
        "label_name": label_name,
        "label_color": label_color,
        "label_description": label_description,
        "preflight_absent": preflight_absent,
        "created_verified": created_verified,
        "deleted_verified": deleted_verified,
        "compensation_attempted": compensation_attempted,
        "compensation_deleted": compensation_deleted,
        "records": records,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if authority.get("audit_append_allowed") is True:
        for record in records:
            _append_jsonl(audit_path, record)
    if authority.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)

    return GitHubMCPLabelCanaryResult(
        "kuuos_github_mcp_label_canary_v0_6",
        status,
        packet_id,
        str(root),
        str(plan_path),
        str(authority_path),
        str(receipt_path),
        str(audit_path),
        repository,
        base_branch,
        base_sha,
        server_image,
        resolved_image_digest,
        label_name,
        label_color,
        label_description,
        preflight_absent,
        created_verified,
        deleted_verified,
        compensation_attempted,
        compensation_deleted,
        records,
        sorted(set(blockers)),
        warnings,
    )
