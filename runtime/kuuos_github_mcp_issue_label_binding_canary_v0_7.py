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

PLAN_VERSION = "kuuos_github_mcp_issue_label_binding_canary_plan_v0_7"
AUTHORITY_READY = "KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY_AUTHORITY_READY"
CONFIRMATION = "RUN_KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY"
VERIFIED = "KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY_VERIFIED"
COMPENSATED = "KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY_COMPENSATED"
BLOCKED = "KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY_BLOCKED"
NONCE_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{7,31}")
COLOR_PATTERN = re.compile(r"[0-9a-fA-F]{6}")


@dataclass(frozen=True)
class GitHubMCPIssueLabelBindingCanaryResult:
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
    request_issue_number: int
    label_name: str
    label_color: str
    label_description: str
    issue_identity_verified: bool
    issue_labels_preflight_empty: bool
    label_preflight_absent: bool
    label_created_verified: bool
    label_attached_verified: bool
    label_detached_verified: bool
    label_deleted_verified: bool
    compensation_attempted: bool
    compensation_issue_detached: bool
    compensation_label_deleted: bool
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
        blockers.append("binding_canary_requires_read_only_false")
    if plan.get("lockdown_mode") is not True:
        blockers.append("lockdown_mode_not_true")
    if plan.get("execute_external_actions") is not True:
        blockers.append("plan_execute_external_actions_not_true")
    if plan.get("confirmation") != CONFIRMATION:
        blockers.append("plan_confirmation_invalid")

    nonce = str(plan.get("transaction_nonce", ""))
    if NONCE_PATTERN.fullmatch(nonce) is None:
        blockers.append("transaction_nonce_invalid")
    issue_number = plan.get("request_issue_number")
    if not isinstance(issue_number, int) or issue_number <= 0:
        blockers.append("request_issue_number_invalid")
    if str(plan.get("request_issue_title", "")) != "[KuuOS MCP Issue Label Binding Canary v0.7]":
        blockers.append("request_issue_title_invalid")
    if str(plan.get("request_version_marker", "")) != "kuuos_github_mcp_issue_label_binding_canary_request_v0_7":
        blockers.append("request_version_marker_invalid")

    prefix = str(plan.get("label_prefix", ""))
    if prefix != "kuuos-mcp-binding-canary-":
        blockers.append("label_prefix_invalid")
    color = str(plan.get("label_color", ""))
    if COLOR_PATTERN.fullmatch(color) is None:
        blockers.append("label_color_invalid")
    marker = str(plan.get("label_description_marker", ""))
    if marker != "KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY v0.7":
        blockers.append("label_description_marker_invalid")

    server = _mapping(plan.get("server"))
    if server.get("kind") != "official_github_mcp_server":
        blockers.append("server_kind_invalid")
    if not _is_pinned_official_image(server.get("image", "")):
        blockers.append("official_server_image_not_pinned")
    toolsets = server.get("toolsets")
    if not isinstance(toolsets, list) or set(str(item) for item in toolsets) != {"issues", "labels"}:
        blockers.append("binding_canary_toolsets_invalid")
    tools = server.get("tools")
    if not isinstance(tools, list) or set(str(item) for item in tools) != {
        "issue_write",
        "issue_read",
        "label_write",
        "get_label",
    }:
        blockers.append("binding_canary_tool_allowlist_invalid")


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


def _issue_identity_blockers(
    *,
    observed: Any,
    issue_number: int,
    expected_title: str,
    expected_version: str,
    expected_confirmation: str,
    expected_base_sha: str,
    expected_nonce: str,
) -> list[str]:
    local: list[str] = []
    issue = _mapping(observed)
    if int(issue.get("number", 0) or 0) != issue_number:
        local.append("observed_issue_number_mismatch")
    if str(issue.get("title", "")) != expected_title:
        local.append("observed_issue_title_mismatch")
    if str(issue.get("state", "")).lower() != "open":
        local.append("observed_issue_state_not_open")
    body_text = str(issue.get("body", ""))
    try:
        body = json.loads(body_text)
    except json.JSONDecodeError:
        local.append("observed_issue_body_not_strict_json")
        return local
    if not isinstance(body, dict):
        local.append("observed_issue_body_not_object")
        return local
    expected_fields = {
        "version": expected_version,
        "confirmation": expected_confirmation,
        "expected_main_sha": expected_base_sha,
        "transaction_nonce": expected_nonce,
        "server_image": body.get("server_image"),
    }
    if set(body) != set(expected_fields):
        local.append("observed_issue_body_fields_invalid")
    for key, expected in expected_fields.items():
        if key == "server_image":
            if not _is_pinned_official_image(body.get(key, "")):
                local.append("observed_issue_server_image_not_pinned")
        elif body.get(key) != expected:
            local.append(f"observed_issue_{key}_mismatch")
    return local


def _label_names(observed: Any) -> tuple[list[str], list[str]]:
    local: list[str] = []
    payload = _mapping(observed)
    labels = payload.get("labels")
    total = payload.get("totalCount")
    if not isinstance(labels, list):
        return [], ["observed_issue_labels_not_list"]
    names: list[str] = []
    for item in labels:
        label = _mapping(item)
        name = str(label.get("name", ""))
        if not name:
            local.append("observed_issue_label_name_missing")
        else:
            names.append(name)
    if not isinstance(total, int) or total != len(labels):
        local.append("observed_issue_label_total_count_mismatch")
    if len(names) != len(set(names)):
        local.append("observed_issue_label_names_not_unique")
    return sorted(names), local


def _issue_label_set_blockers(observed: Any, expected_names: set[str]) -> list[str]:
    names, local = _label_names(observed)
    if set(names) != expected_names:
        local.append("observed_issue_label_set_mismatch")
    return local


def build_github_mcp_issue_label_binding_canary(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
    transport: MCPTransport | None = None,
) -> GitHubMCPIssueLabelBindingCanaryResult:
    ctx = _mapping(runtime_context)
    authority = _mapping(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []

    root = _safe_root(ctx.get("runtime_root"), blockers)
    plan_path = root / "github_mcp_issue_label_binding_canary_plan_v0_7.json"
    authority_path = root / "github_mcp_issue_label_binding_canary_authority_v0_7.json"
    receipt_path = root / "github_mcp_issue_label_binding_canary_receipt_v0_7.json"
    audit_path = root / "github_mcp_issue_label_binding_canary_audit_v0_7.jsonl"

    if ctx.get("github_mcp_issue_label_binding_canary_enabled") is not True:
        blockers.append("github_mcp_issue_label_binding_canary_enabled_not_true")
    if ctx.get("apply_github_mcp_issue_label_binding_canary") is not True:
        blockers.append("apply_github_mcp_issue_label_binding_canary_not_true")
    if ctx.get("execute_external_actions") is not True:
        blockers.append("runtime_execute_external_actions_not_true")
    if ctx.get("confirmation") != CONFIRMATION:
        blockers.append("runtime_confirmation_invalid")
    if authority.get("authority_status") != AUTHORITY_READY:
        blockers.append("issue_label_binding_canary_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "tool_discovery_allowed",
        "external_action_allowed",
        "mcp_write_tool_call_allowed",
        "post_write_reobservation_allowed",
        "compensating_issue_detach_allowed",
        "compensating_label_delete_allowed",
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

    transaction_nonce = str(plan.get("transaction_nonce", ""))
    if str(ctx.get("transaction_nonce", transaction_nonce)) != transaction_nonce:
        blockers.append("runtime_transaction_nonce_mismatch")
    request_issue_number = int(plan.get("request_issue_number", 0) or 0)
    if int(ctx.get("request_issue_number", request_issue_number) or 0) != request_issue_number:
        blockers.append("runtime_request_issue_number_mismatch")
    request_issue_title = str(plan.get("request_issue_title", ""))
    request_version_marker = str(plan.get("request_version_marker", ""))

    label_name = f"{str(plan.get('label_prefix', ''))}{transaction_nonce}"
    label_color = str(plan.get("label_color", "")).lower()
    label_description = f"{str(plan.get('label_description_marker', ''))} {transaction_nonce}"

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
                for required in ("issue_write", "issue_read", "label_write", "get_label"):
                    if required not in discovered:
                        blockers.append(f"required_tool_not_discovered:{required}")
                for name in ("issue_write", "label_write"):
                    if name in discovered and not _is_write_tool(name, discovered[name]):
                        blockers.append(f"{name}_not_classified_write")
                for name in ("issue_read", "get_label"):
                    if name in discovered and _is_write_tool(name, discovered[name]):
                        blockers.append(f"{name}_not_classified_read_only")
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"tool_discovery_failed:{type(exc).__name__}")

    issue_identity_verified = False
    issue_labels_preflight_empty = False
    label_preflight_absent = False
    label_created_verified = False
    label_attached_verified = False
    label_detached_verified = False
    label_deleted_verified = False
    compensation_attempted = False
    compensation_issue_detached = False
    compensation_label_deleted = False
    label_create_attempted = False
    label_attach_attempted = False

    issue_get_args = {
        "method": "get",
        "owner": owner,
        "repo": repo,
        "issue_number": request_issue_number,
    }
    issue_labels_args = {
        "method": "get_labels",
        "owner": owner,
        "repo": repo,
        "issue_number": request_issue_number,
    }
    get_label_args = {"owner": owner, "repo": repo, "name": label_name}

    if not blockers and active_transport is not None:
        response, observed, local = _call_tool(
            active_transport,
            phase="verify_request_issue",
            tool="issue_read",
            arguments=issue_get_args,
        )
        if not local:
            local.extend(
                _issue_identity_blockers(
                    observed=observed,
                    issue_number=request_issue_number,
                    expected_title=request_issue_title,
                    expected_version=request_version_marker,
                    expected_confirmation=CONFIRMATION,
                    expected_base_sha=base_sha,
                    expected_nonce=transaction_nonce,
                )
            )
        issue_identity_verified = not local
        records.append(
            _record(
                phase="verify_request_issue",
                tool="issue_read",
                arguments=issue_get_args,
                response=response,
                observed=observed,
                status="verified" if issue_identity_verified else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if issue_identity_verified and not blockers and active_transport is not None:
        response, observed, local = _call_tool(
            active_transport,
            phase="preflight_issue_labels",
            tool="issue_read",
            arguments=issue_labels_args,
        )
        if not local:
            local.extend(_issue_label_set_blockers(observed, set()))
        issue_labels_preflight_empty = not local
        records.append(
            _record(
                phase="preflight_issue_labels",
                tool="issue_read",
                arguments=issue_labels_args,
                response=response,
                observed=observed,
                status="verified_empty" if issue_labels_preflight_empty else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if issue_labels_preflight_empty and not blockers and active_transport is not None:
        response, observed, local = _call_get_label(
            active_transport,
            phase="preflight_label",
            arguments=get_label_args,
            expect_absent=True,
        )
        label_preflight_absent = not local and _mapping(observed).get("absent") is True
        records.append(
            _record(
                phase="preflight_label",
                tool="get_label",
                arguments=get_label_args,
                response=response,
                observed=observed,
                status="verified_absent" if label_preflight_absent else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if label_preflight_absent and not blockers and active_transport is not None:
        label_create_attempted = True
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
            phase="create_label",
            tool="label_write",
            arguments=create_args,
        )
        records.append(
            _record(
                phase="create_label",
                tool="label_write",
                arguments=create_args,
                response=response,
                observed=observed,
                status="applied" if not local else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if label_create_attempted and not blockers and active_transport is not None:
        response, observed, local = _call_get_label(
            active_transport,
            phase="verify_label_created",
            arguments=get_label_args,
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
        label_created_verified = not local
        records.append(
            _record(
                phase="verify_label_created",
                tool="get_label",
                arguments=get_label_args,
                response=response,
                observed=observed,
                status="verified" if label_created_verified else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if label_created_verified and not blockers and active_transport is not None:
        label_attach_attempted = True
        attach_args = {
            "method": "update",
            "owner": owner,
            "repo": repo,
            "issue_number": request_issue_number,
            "labels": [label_name],
        }
        response, observed, local = _call_tool(
            active_transport,
            phase="attach_label",
            tool="issue_write",
            arguments=attach_args,
        )
        records.append(
            _record(
                phase="attach_label",
                tool="issue_write",
                arguments=attach_args,
                response=response,
                observed=observed,
                status="applied" if not local else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if label_attach_attempted and not blockers and active_transport is not None:
        response, observed, local = _call_tool(
            active_transport,
            phase="verify_label_attached",
            tool="issue_read",
            arguments=issue_labels_args,
        )
        if not local:
            local.extend(_issue_label_set_blockers(observed, {label_name}))
        label_attached_verified = not local
        records.append(
            _record(
                phase="verify_label_attached",
                tool="issue_read",
                arguments=issue_labels_args,
                response=response,
                observed=observed,
                status="verified" if label_attached_verified else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if label_attached_verified and not blockers and active_transport is not None:
        detach_args = {
            "method": "update",
            "owner": owner,
            "repo": repo,
            "issue_number": request_issue_number,
            "labels": [],
        }
        response, observed, local = _call_tool(
            active_transport,
            phase="detach_label",
            tool="issue_write",
            arguments=detach_args,
        )
        records.append(
            _record(
                phase="detach_label",
                tool="issue_write",
                arguments=detach_args,
                response=response,
                observed=observed,
                status="applied" if not local else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if label_attached_verified and not blockers and active_transport is not None:
        response, observed, local = _call_tool(
            active_transport,
            phase="verify_label_detached",
            tool="issue_read",
            arguments=issue_labels_args,
        )
        if not local:
            local.extend(_issue_label_set_blockers(observed, set()))
        label_detached_verified = not local
        records.append(
            _record(
                phase="verify_label_detached",
                tool="issue_read",
                arguments=issue_labels_args,
                response=response,
                observed=observed,
                status="verified_empty" if label_detached_verified else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if label_detached_verified and not blockers and active_transport is not None:
        delete_args = {
            "method": "delete",
            "owner": owner,
            "repo": repo,
            "name": label_name,
        }
        response, observed, local = _call_tool(
            active_transport,
            phase="delete_label",
            tool="label_write",
            arguments=delete_args,
        )
        records.append(
            _record(
                phase="delete_label",
                tool="label_write",
                arguments=delete_args,
                response=response,
                observed=observed,
                status="applied" if not local else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    if label_detached_verified and not blockers and active_transport is not None:
        response, observed, local = _call_get_label(
            active_transport,
            phase="verify_label_deleted",
            arguments=get_label_args,
            expect_absent=True,
        )
        label_deleted_verified = not local and _mapping(observed).get("absent") is True
        records.append(
            _record(
                phase="verify_label_deleted",
                tool="get_label",
                arguments=get_label_args,
                response=response,
                observed=observed,
                status="verified_absent" if label_deleted_verified else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    cleanup_needed = (
        issue_identity_verified
        and issue_labels_preflight_empty
        and (
            (label_attach_attempted and not label_detached_verified)
            or (label_create_attempted and label_preflight_absent and not label_deleted_verified)
        )
    )
    if cleanup_needed and active_transport is not None:
        compensation_attempted = True
        detach_args = {
            "method": "update",
            "owner": owner,
            "repo": repo,
            "issue_number": request_issue_number,
            "labels": [],
        }
        response, observed, local = _call_tool(
            active_transport,
            phase="compensating_issue_detach",
            tool="issue_write",
            arguments=detach_args,
        )
        records.append(
            _record(
                phase="compensating_issue_detach",
                tool="issue_write",
                arguments=detach_args,
                response=response,
                observed=observed,
                status="applied" if not local else "warning",
                blockers=local,
            )
        )
        if local:
            warnings.extend(local)

        read_response, read_observed, read_local = _call_tool(
            active_transport,
            phase="verify_compensating_issue_detach",
            tool="issue_read",
            arguments=issue_labels_args,
        )
        if not read_local:
            read_local.extend(_issue_label_set_blockers(read_observed, set()))
        compensation_issue_detached = not read_local
        records.append(
            _record(
                phase="verify_compensating_issue_detach",
                tool="issue_read",
                arguments=issue_labels_args,
                response=read_response,
                observed=read_observed,
                status="verified_empty" if compensation_issue_detached else "blocked",
                blockers=read_local,
            )
        )
        if read_local:
            warnings.extend(read_local)

        if label_create_attempted and label_preflight_absent and compensation_issue_detached:
            delete_args = {
                "method": "delete",
                "owner": owner,
                "repo": repo,
                "name": label_name,
            }
            delete_response, delete_observed, delete_local = _call_tool(
                active_transport,
                phase="compensating_label_delete",
                tool="label_write",
                arguments=delete_args,
            )
            records.append(
                _record(
                    phase="compensating_label_delete",
                    tool="label_write",
                    arguments=delete_args,
                    response=delete_response,
                    observed=delete_observed,
                    status="applied" if not delete_local else "warning",
                    blockers=delete_local,
                )
            )
            if delete_local:
                warnings.extend(delete_local)

            verify_response, verify_observed, verify_local = _call_get_label(
                active_transport,
                phase="verify_compensating_label_delete",
                arguments=get_label_args,
                expect_absent=True,
            )
            compensation_label_deleted = (
                not verify_local and _mapping(verify_observed).get("absent") is True
            )
            records.append(
                _record(
                    phase="verify_compensating_label_delete",
                    tool="get_label",
                    arguments=get_label_args,
                    response=verify_response,
                    observed=verify_observed,
                    status="verified_absent" if compensation_label_deleted else "blocked",
                    blockers=verify_local,
                )
            )
            if verify_local:
                warnings.extend(verify_local)
        else:
            compensation_label_deleted = not label_create_attempted

    if owns_transport and active_transport is not None:
        active_transport.close()

    verified_flags = (
        issue_identity_verified,
        issue_labels_preflight_empty,
        label_preflight_absent,
        label_created_verified,
        label_attached_verified,
        label_detached_verified,
        label_deleted_verified,
    )
    if all(verified_flags) and not blockers:
        status = VERIFIED
    elif (
        compensation_attempted
        and compensation_issue_detached
        and compensation_label_deleted
    ):
        status = COMPENSATED
    else:
        status = BLOCKED

    packet_id = "kuuos-github-mcp-issue-label-binding-canary-" + _sha256(
        {
            "plan": plan,
            "records": records,
            "blockers": blockers,
            "resolved_image_digest": resolved_image_digest,
        }
    )[:16]
    receipt = {
        "version": "kuuos_github_mcp_issue_label_binding_canary_v0_7",
        "status": status,
        "packet_id": packet_id,
        "repository_full_name": repository,
        "base_branch": base_branch,
        "base_sha": base_sha,
        "server_image": server_image,
        "resolved_image_digest": resolved_image_digest,
        "transaction_nonce": transaction_nonce,
        "request_issue_number": request_issue_number,
        "label_name": label_name,
        "label_color": label_color,
        "label_description": label_description,
        "issue_identity_verified": issue_identity_verified,
        "issue_labels_preflight_empty": issue_labels_preflight_empty,
        "label_preflight_absent": label_preflight_absent,
        "label_created_verified": label_created_verified,
        "label_attached_verified": label_attached_verified,
        "label_detached_verified": label_detached_verified,
        "label_deleted_verified": label_deleted_verified,
        "compensation_attempted": compensation_attempted,
        "compensation_issue_detached": compensation_issue_detached,
        "compensation_label_deleted": compensation_label_deleted,
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

    return GitHubMCPIssueLabelBindingCanaryResult(
        "kuuos_github_mcp_issue_label_binding_canary_v0_7",
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
        transaction_nonce,
        request_issue_number,
        label_name,
        label_color,
        label_description,
        issue_identity_verified,
        issue_labels_preflight_empty,
        label_preflight_absent,
        label_created_verified,
        label_attached_verified,
        label_detached_verified,
        label_deleted_verified,
        compensation_attempted,
        compensation_issue_detached,
        compensation_label_deleted,
        records,
        sorted(set(blockers)),
        warnings,
    )
