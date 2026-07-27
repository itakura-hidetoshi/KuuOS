#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import os
import re
import time
from typing import Any, Mapping

from runtime.kuuos_github_mcp_live_write_verification_v0_3 import (
    _issue_number_from_url,
    _normalize_tool_payload,
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

PLAN_VERSION = "kuuos_github_mcp_live_canary_plan_v0_4"
AUTHORITY_READY = "KUUOS_GITHUB_MCP_LIVE_CANARY_AUTHORITY_READY"
CONFIRMATION = "RUN_KUUOS_GITHUB_MCP_LIVE_CANARY"
VERIFIED = "KUUOS_GITHUB_MCP_LIVE_CANARY_VERIFIED"
COMPENSATED = "KUUOS_GITHUB_MCP_LIVE_CANARY_COMPENSATED"
BLOCKED = "KUUOS_GITHUB_MCP_LIVE_CANARY_BLOCKED"
OFFICIAL_IMAGE_PREFIX = "ghcr.io/github/github-mcp-server"


@dataclass(frozen=True)
class GitHubMCPLiveCanaryResult:
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
    issue_number: int
    issue_url: str
    created_verified: bool
    closed_verified: bool
    compensation_attempted: bool
    compensation_closed: bool
    records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _is_sha(value: Any) -> bool:
    text = str(value)
    return len(text) == 40 and all(ch in "0123456789abcdef" for ch in text.lower())


def _is_pinned_official_image(value: Any) -> bool:
    text = str(value)
    if text.startswith(OFFICIAL_IMAGE_PREFIX + "@sha256:"):
        digest = text.split("@sha256:", 1)[1]
        return len(digest) == 64 and all(ch in "0123456789abcdef" for ch in digest.lower())
    if not text.startswith(OFFICIAL_IMAGE_PREFIX + ":"):
        return False
    tag = text.rsplit(":", 1)[1]
    return bool(re.fullmatch(r"(?:v\d+\.\d+\.\d+|sha-[0-9a-f]{7,40})", tag))


def _tool_returned_error(response: Mapping[str, Any]) -> bool:
    return "error" in response or _mapping(response.get("result")).get("isError") is True


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
    if not str(plan.get("base_branch", "")):
        blockers.append("base_branch_missing")
    if not _is_sha(plan.get("base_sha", "")):
        blockers.append("base_sha_invalid")
    if plan.get("write_capable") is not True:
        blockers.append("write_capable_not_true")
    if plan.get("read_only") is not False:
        blockers.append("live_canary_requires_read_only_false")
    if plan.get("lockdown_mode") is not True:
        blockers.append("lockdown_mode_not_true")
    if plan.get("execute_external_actions") is not True:
        blockers.append("plan_execute_external_actions_not_true")
    if plan.get("confirmation") != CONFIRMATION:
        blockers.append("plan_confirmation_invalid")
    server = _mapping(plan.get("server"))
    if server.get("kind") != "official_github_mcp_server":
        blockers.append("server_kind_invalid")
    if not _is_pinned_official_image(server.get("image", "")):
        blockers.append("official_server_image_not_pinned")
    tools = server.get("tools")
    if not isinstance(tools, list) or set(str(item) for item in tools) != {"issue_write", "issue_read"}:
        blockers.append("canary_tool_allowlist_invalid")
    title_prefix = str(plan.get("title_prefix", ""))
    body_marker = str(plan.get("body_marker", ""))
    if not title_prefix.startswith("[KuuOS MCP Canary]"):
        blockers.append("title_prefix_invalid")
    if "KUUOS_GITHUB_MCP_LIVE_CANARY" not in body_marker:
        blockers.append("body_marker_invalid")


def _issue_blockers(
    *,
    observed: Any,
    issue_number: int,
    title: str,
    body_marker: str,
    expected_state: str,
) -> list[str]:
    blockers: list[str] = []
    issue = _mapping(observed)
    if int(issue.get("number", 0) or 0) != issue_number:
        blockers.append("observed_issue_number_mismatch")
    if str(issue.get("title", "")) != title:
        blockers.append("observed_issue_title_mismatch")
    if body_marker not in str(issue.get("body", "")):
        blockers.append("observed_issue_body_marker_missing")
    if str(issue.get("state", "")).lower() != expected_state.lower():
        blockers.append(f"observed_issue_state_not_{expected_state.lower()}")
    return blockers


def _call_tool(
    transport: MCPTransport,
    *,
    phase: str,
    tool: str,
    arguments: Mapping[str, Any],
) -> tuple[dict[str, Any], Any, list[str]]:
    blockers: list[str] = []
    response: dict[str, Any]
    observed: Any = {}
    try:
        response = transport.call_tool(tool, arguments)
        if _tool_returned_error(response):
            blockers.append(f"{phase}_tool_returned_error")
        else:
            observed = _normalize_tool_payload(response)
    except Exception as exc:  # noqa: BLE001
        response = {"error": f"{type(exc).__name__}:{exc}"}
        blockers.append(f"{phase}_tool_exception")
    return response, observed, blockers


def build_github_mcp_live_canary(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
    transport: MCPTransport | None = None,
) -> GitHubMCPLiveCanaryResult:
    ctx = _mapping(runtime_context)
    authority = _mapping(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []

    root = _safe_root(ctx.get("runtime_root"), blockers)
    plan_path = root / "github_mcp_live_canary_plan_v0_4.json"
    authority_path = root / "github_mcp_live_canary_authority_v0_4.json"
    receipt_path = root / "github_mcp_live_canary_receipt_v0_4.json"
    audit_path = root / "github_mcp_live_canary_audit_v0_4.jsonl"

    if ctx.get("github_mcp_live_canary_enabled") is not True:
        blockers.append("github_mcp_live_canary_enabled_not_true")
    if ctx.get("apply_github_mcp_live_canary") is not True:
        blockers.append("apply_github_mcp_live_canary_not_true")
    if ctx.get("execute_external_actions") is not True:
        blockers.append("runtime_execute_external_actions_not_true")
    if ctx.get("confirmation") != CONFIRMATION:
        blockers.append("runtime_confirmation_invalid")
    if authority.get("authority_status") != AUTHORITY_READY:
        blockers.append("live_canary_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "tool_discovery_allowed",
        "external_action_allowed",
        "mcp_write_tool_call_allowed",
        "post_write_reobservation_allowed",
        "compensating_close_allowed",
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

    server = dict(_mapping(plan.get("server")))
    server_image = str(server.get("image", ""))
    resolved_image_digest = str(ctx.get("resolved_image_digest", ""))
    if mode == "stdio" and not resolved_image_digest.startswith("sha256:"):
        blockers.append("resolved_image_digest_missing")

    owner, repo = (repository.split("/", 1) + [""])[:2]
    run_identity = str(ctx.get("run_identity", plan.get("run_identity", "manual")))
    title = f"{str(plan.get('title_prefix', ''))} {run_identity}".strip()
    body_marker = str(plan.get("body_marker", ""))
    body = f"{body_marker}\n\nrun_identity: `{run_identity}`\nbase_sha: `{base_sha}`"

    active_transport = transport
    owns_transport = False
    discovered_tools: dict[str, dict[str, Any]] = {}
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
                discovered_tools = _tool_map(list_response)
                for required in ("issue_write", "issue_read"):
                    if required not in discovered_tools:
                        blockers.append(f"required_tool_not_discovered:{required}")
                if "issue_write" in discovered_tools and not _is_write_tool(
                    "issue_write", discovered_tools["issue_write"]
                ):
                    blockers.append("issue_write_not_classified_write")
                if "issue_read" in discovered_tools and _is_write_tool(
                    "issue_read", discovered_tools["issue_read"]
                ):
                    blockers.append("issue_read_not_classified_read_only")
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"tool_discovery_failed:{type(exc).__name__}")

    issue_number = 0
    issue_url = ""
    created_verified = False
    closed_verified = False
    compensation_attempted = False
    compensation_closed = False

    if not blockers and active_transport is not None:
        create_args = {
            "method": "create",
            "owner": owner,
            "repo": repo,
            "title": title,
            "body": body,
        }
        response, observed, local = _call_tool(
            active_transport, phase="create", tool="issue_write", arguments=create_args
        )
        if not local:
            try:
                issue_url = str(_mapping(observed).get("url", ""))
                issue_number = _issue_number_from_url(issue_url)
            except ValueError:
                local.append("create_issue_url_invalid")
        records.append(
            _record(
                phase="create",
                tool="issue_write",
                arguments=create_args,
                response=response,
                observed=observed,
                status="applied" if not local else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if issue_number > 0 and active_transport is not None and not blockers:
        read_open_args = {
            "method": "get",
            "owner": owner,
            "repo": repo,
            "issue_number": issue_number,
        }
        response, observed, local = _call_tool(
            active_transport, phase="verify_open", tool="issue_read", arguments=read_open_args
        )
        if not local:
            local.extend(
                _issue_blockers(
                    observed=observed,
                    issue_number=issue_number,
                    title=title,
                    body_marker=body_marker,
                    expected_state="open",
                )
            )
        created_verified = not local
        records.append(
            _record(
                phase="verify_open",
                tool="issue_read",
                arguments=read_open_args,
                response=response,
                observed=observed,
                status="verified" if not local else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if issue_number > 0 and active_transport is not None and not blockers:
        close_args = {
            "method": "update",
            "owner": owner,
            "repo": repo,
            "issue_number": issue_number,
            "state": "closed",
            "state_reason": "completed",
        }
        response, observed, local = _call_tool(
            active_transport, phase="close", tool="issue_write", arguments=close_args
        )
        records.append(
            _record(
                phase="close",
                tool="issue_write",
                arguments=close_args,
                response=response,
                observed=observed,
                status="applied" if not local else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if issue_number > 0 and active_transport is not None and not blockers:
        read_closed_args = {
            "method": "get",
            "owner": owner,
            "repo": repo,
            "issue_number": issue_number,
        }
        response, observed, local = _call_tool(
            active_transport, phase="verify_closed", tool="issue_read", arguments=read_closed_args
        )
        if not local:
            local.extend(
                _issue_blockers(
                    observed=observed,
                    issue_number=issue_number,
                    title=title,
                    body_marker=body_marker,
                    expected_state="closed",
                )
            )
        closed_verified = not local
        records.append(
            _record(
                phase="verify_closed",
                tool="issue_read",
                arguments=read_closed_args,
                response=response,
                observed=observed,
                status="verified" if not local else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if issue_number > 0 and active_transport is not None and not closed_verified:
        compensation_attempted = True
        close_args = {
            "method": "update",
            "owner": owner,
            "repo": repo,
            "issue_number": issue_number,
            "state": "closed",
            "state_reason": "completed",
        }
        response, observed, local = _call_tool(
            active_transport,
            phase="compensating_close",
            tool="issue_write",
            arguments=close_args,
        )
        records.append(
            _record(
                phase="compensating_close",
                tool="issue_write",
                arguments=close_args,
                response=response,
                observed=observed,
                status="applied" if not local else "blocked",
                blockers=local,
            )
        )
        read_args = {
            "method": "get",
            "owner": owner,
            "repo": repo,
            "issue_number": issue_number,
        }
        read_response, read_observed, read_local = _call_tool(
            active_transport,
            phase="verify_compensation",
            tool="issue_read",
            arguments=read_args,
        )
        if not read_local:
            read_local.extend(
                _issue_blockers(
                    observed=read_observed,
                    issue_number=issue_number,
                    title=title,
                    body_marker=body_marker,
                    expected_state="closed",
                )
            )
        compensation_closed = not read_local
        records.append(
            _record(
                phase="verify_compensation",
                tool="issue_read",
                arguments=read_args,
                response=read_response,
                observed=read_observed,
                status="verified" if not read_local else "blocked",
                blockers=read_local,
            )
        )
        if local:
            warnings.extend(local)
        if read_local:
            warnings.extend(read_local)

    if owns_transport and active_transport is not None:
        active_transport.close()

    if created_verified and closed_verified and not blockers:
        status = VERIFIED
    elif compensation_attempted and compensation_closed:
        status = COMPENSATED
    else:
        status = BLOCKED

    packet_id = "kuuos-github-mcp-live-canary-" + _sha256(
        {
            "plan": plan,
            "records": records,
            "blockers": blockers,
            "resolved_image_digest": resolved_image_digest,
        }
    )[:16]
    receipt = {
        "version": "kuuos_github_mcp_live_canary_v0_4",
        "status": status,
        "packet_id": packet_id,
        "repository_full_name": repository,
        "base_branch": base_branch,
        "base_sha": base_sha,
        "server_image": server_image,
        "resolved_image_digest": resolved_image_digest,
        "issue_number": issue_number,
        "issue_url": issue_url,
        "created_verified": created_verified,
        "closed_verified": closed_verified,
        "compensation_attempted": compensation_attempted,
        "compensation_closed": compensation_closed,
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

    return GitHubMCPLiveCanaryResult(
        "kuuos_github_mcp_live_canary_v0_4",
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
        issue_number,
        issue_url,
        created_verified,
        closed_verified,
        compensation_attempted,
        compensation_closed,
        records,
        sorted(set(blockers)),
        warnings,
    )
