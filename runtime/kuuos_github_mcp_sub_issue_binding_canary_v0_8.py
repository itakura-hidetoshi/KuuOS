#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import html
import json
import os
from pathlib import Path
import re
import time
from typing import Any, Mapping, Protocol

PLAN_VERSION = "kuuos_github_mcp_sub_issue_binding_canary_plan_v0_8"
REQUEST_VERSION = "kuuos_github_mcp_sub_issue_binding_canary_request_v0_8"
CHILD_VERSION = "kuuos_github_mcp_sub_issue_binding_canary_child_v0_8"
AUTHORITY_READY = "KUUOS_GITHUB_MCP_SUB_ISSUE_BINDING_CANARY_AUTHORITY_READY"
CONFIRMATION = "RUN_KUUOS_GITHUB_MCP_SUB_ISSUE_BINDING_CANARY"
VERIFIED = "KUUOS_GITHUB_MCP_SUB_ISSUE_BINDING_CANARY_VERIFIED"
COMPENSATED = "KUUOS_GITHUB_MCP_SUB_ISSUE_BINDING_CANARY_COMPENSATED"
BLOCKED = "KUUOS_GITHUB_MCP_SUB_ISSUE_BINDING_CANARY_BLOCKED"
REQUEST_TITLE = "[KuuOS MCP Sub-Issue Binding Canary v0.8]"
CHILD_TITLE_PREFIX = "[KuuOS MCP Sub-Issue Child v0.8] "
NONCE_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{7,31}")
SHA_PATTERN = re.compile(r"[0-9a-fA-F]{40}")
PINNED_IMAGE_PATTERN = re.compile(
    r"ghcr\.io/github/github-mcp-server@sha256:[0-9a-fA-F]{64}"
)


class MCPTransport(Protocol):
    def list_tools(self) -> dict[str, Any]: ...
    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]: ...
    def close(self) -> None: ...


@dataclass(frozen=True)
class GitHubMCPSubIssueBindingCanaryResult:
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
    binding_added_verified: bool
    binding_removed_verified: bool
    child_closed_verified: bool
    compensation_attempted: bool
    compensation_binding_removed: bool
    compensation_child_closed: bool
    records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _sha256(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(data).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name}: top-level JSON must be an object")
    return value


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(value), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, values: list[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for value in values:
            handle.write(json.dumps(dict(value), ensure_ascii=False, sort_keys=True) + "\n")


def _safe_root(value: Any, blockers: list[str]) -> Path:
    try:
        root = Path(str(value)).expanduser().resolve()
    except Exception:
        blockers.append("runtime_root_invalid")
        return Path.cwd()
    if not root.is_dir():
        blockers.append("runtime_root_missing")
    return root


def _tool_returned_error(response: Mapping[str, Any]) -> bool:
    if "error" in response:
        return True
    result = _mapping(response.get("result"))
    return result.get("isError") is True


def _normalize_tool_payload(response: Mapping[str, Any]) -> Any:
    result = _mapping(response.get("result"))
    content = result.get("content")
    if not isinstance(content, list) or not content:
        return result
    text_items = [
        str(item.get("text", ""))
        for item in content
        if isinstance(item, Mapping) and item.get("type") == "text"
    ]
    if not text_items:
        return result
    text = "\n".join(text_items)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _tool_map(response: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    result = _mapping(response.get("result"))
    tools = result.get("tools")
    if not isinstance(tools, list):
        return {}
    return {
        str(item.get("name")): dict(item)
        for item in tools
        if isinstance(item, Mapping) and item.get("name")
    }


def _is_write_tool(tool: Mapping[str, Any]) -> bool:
    annotations = _mapping(tool.get("annotations"))
    return annotations.get("readOnlyHint") is not True


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
    if plan.get("base_branch") != "main":
        blockers.append("base_branch_not_main")
    if SHA_PATTERN.fullmatch(str(plan.get("base_sha", ""))) is None:
        blockers.append("base_sha_invalid")
    if plan.get("write_capable") is not True:
        blockers.append("write_capable_not_true")
    if plan.get("read_only") is not False:
        blockers.append("sub_issue_canary_requires_read_only_false")
    if plan.get("lockdown_mode") is not True:
        blockers.append("lockdown_mode_not_true")
    if plan.get("execute_external_actions") is not True:
        blockers.append("plan_execute_external_actions_not_true")
    if plan.get("confirmation") != CONFIRMATION:
        blockers.append("plan_confirmation_invalid")
    if NONCE_PATTERN.fullmatch(str(plan.get("transaction_nonce", ""))) is None:
        blockers.append("transaction_nonce_invalid")
    parent = plan.get("parent_issue_number")
    if not isinstance(parent, int) or parent <= 0:
        blockers.append("parent_issue_number_invalid")
    if plan.get("request_issue_title") != REQUEST_TITLE:
        blockers.append("request_issue_title_invalid")
    if plan.get("request_version_marker") != REQUEST_VERSION:
        blockers.append("request_version_marker_invalid")
    if plan.get("child_title_prefix") != CHILD_TITLE_PREFIX:
        blockers.append("child_title_prefix_invalid")
    if plan.get("child_version_marker") != CHILD_VERSION:
        blockers.append("child_version_marker_invalid")
    server = _mapping(plan.get("server"))
    if server.get("kind") != "official_github_mcp_server":
        blockers.append("server_kind_invalid")
    if PINNED_IMAGE_PATTERN.fullmatch(str(server.get("image", ""))) is None:
        blockers.append("official_server_image_not_pinned")
    if set(map(str, server.get("toolsets", []))) != {"issues"}:
        blockers.append("sub_issue_canary_toolsets_invalid")
    if set(map(str, server.get("tools", []))) != {"issue_write", "issue_read", "sub_issue_write"}:
        blockers.append("sub_issue_canary_tool_allowlist_invalid")


def _strict_body(value: Any) -> Any:
    return json.loads(html.unescape(str(value)))


def _request_identity_blockers(
    observed: Any, *, issue_number: int, base_sha: str, nonce: str, image: str
) -> list[str]:
    local: list[str] = []
    issue = _mapping(observed)
    if int(issue.get("number", 0) or 0) != issue_number:
        local.append("observed_parent_issue_number_mismatch")
    if issue.get("title") != REQUEST_TITLE:
        local.append("observed_parent_issue_title_mismatch")
    if str(issue.get("state", "")).lower() != "open":
        local.append("observed_parent_issue_state_not_open")
    try:
        body = _strict_body(issue.get("body", ""))
    except (json.JSONDecodeError, TypeError, ValueError):
        local.append("observed_parent_issue_body_not_strict_json")
        return local
    expected = {
        "version": REQUEST_VERSION,
        "confirmation": CONFIRMATION,
        "expected_main_sha": base_sha,
        "transaction_nonce": nonce,
        "server_image": image,
    }
    if body != expected:
        local.append("observed_parent_issue_body_mismatch")
    return local


def _child_body(*, parent_issue_number: int, base_sha: str, nonce: str) -> dict[str, Any]:
    return {
        "version": CHILD_VERSION,
        "parent_issue_number": parent_issue_number,
        "base_sha": base_sha,
        "transaction_nonce": nonce,
    }


def _child_identity_blockers(
    observed: Any,
    *,
    issue_number: int,
    title: str,
    parent_issue_number: int,
    base_sha: str,
    nonce: str,
    expected_state: str,
) -> list[str]:
    local: list[str] = []
    issue = _mapping(observed)
    if int(issue.get("number", 0) or 0) != issue_number:
        local.append("observed_child_issue_number_mismatch")
    if issue.get("title") != title:
        local.append("observed_child_issue_title_mismatch")
    if str(issue.get("state", "")).lower() != expected_state:
        local.append(f"observed_child_issue_state_not_{expected_state}")
    try:
        body = _strict_body(issue.get("body", ""))
    except (json.JSONDecodeError, TypeError, ValueError):
        local.append("observed_child_issue_body_not_strict_json")
        return local
    if body != _child_body(
        parent_issue_number=parent_issue_number, base_sha=base_sha, nonce=nonce
    ):
        local.append("observed_child_issue_body_mismatch")
    return local


def _sub_issue_entries(observed: Any) -> tuple[list[dict[str, Any]], list[str]]:
    if not isinstance(observed, list):
        return [], ["observed_sub_issues_not_list"]
    entries: list[dict[str, Any]] = []
    local: list[str] = []
    for item in observed:
        entry = _mapping(item)
        number = int(entry.get("number", 0) or 0)
        title = str(entry.get("title", ""))
        if number <= 0 or not title:
            local.append("observed_sub_issue_identity_incomplete")
        entries.append(entry)
    return entries, local


def _sub_issue_set_blockers(
    observed: Any, *, expected_number: int | None, expected_title: str | None
) -> list[str]:
    entries, local = _sub_issue_entries(observed)
    if expected_number is None:
        if entries:
            local.append("parent_has_preexisting_or_residual_sub_issues")
        return local
    if len(entries) != 1:
        local.append("observed_sub_issue_count_not_one")
        return local
    entry = entries[0]
    if int(entry.get("number", 0) or 0) != expected_number:
        local.append("observed_sub_issue_number_mismatch")
    if str(entry.get("title", "")) != str(expected_title):
        local.append("observed_sub_issue_title_mismatch")
    return local


def _call_tool(
    transport: MCPTransport, *, phase: str, tool: str, arguments: Mapping[str, Any]
) -> tuple[dict[str, Any], Any, list[str]]:
    try:
        response = transport.call_tool(tool, arguments)
    except Exception as exc:
        return {"error": f"{type(exc).__name__}:{exc}"}, {}, [f"{phase}_tool_exception"]
    local: list[str] = []
    observed: Any = {}
    if _tool_returned_error(response):
        local.append(f"{phase}_tool_returned_error")
    else:
        observed = _normalize_tool_payload(response)
    return dict(response), observed, local


def _extract_created_child(observed: Any) -> tuple[int, int, list[str]]:
    payload = _mapping(observed)
    local: list[str] = []
    try:
        child_id = int(str(payload.get("id", "0")))
    except ValueError:
        child_id = 0
    url = str(payload.get("url", ""))
    try:
        child_number = int(url.rstrip("/").rsplit("/", 1)[-1])
    except (ValueError, IndexError):
        child_number = 0
    if child_id <= 0:
        local.append("created_child_id_invalid")
    if child_number <= 0:
        local.append("created_child_issue_number_invalid")
    return child_id, child_number, local


def _open_stdio_transport(server: Mapping[str, Any], plan: Mapping[str, Any]) -> MCPTransport:
    from runtime.kuuos_github_mcp_server_bridge_v0_1 import (
        OfficialGitHubMCPStdioClient,
        _stdio_command,
    )
    command, generated_env = _stdio_command(server, plan)
    return OfficialGitHubMCPStdioClient(command, generated_env)


def build_github_mcp_sub_issue_binding_canary(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
    transport: MCPTransport | None = None,
) -> GitHubMCPSubIssueBindingCanaryResult:
    ctx = _mapping(runtime_context)
    authority = _mapping(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []

    root = _safe_root(ctx.get("runtime_root"), blockers)
    plan_path = root / "github_mcp_sub_issue_binding_canary_plan_v0_8.json"
    authority_path = root / "github_mcp_sub_issue_binding_canary_authority_v0_8.json"
    receipt_path = root / "github_mcp_sub_issue_binding_canary_receipt_v0_8.json"
    audit_path = root / "github_mcp_sub_issue_binding_canary_audit_v0_8.jsonl"

    if ctx.get("github_mcp_sub_issue_binding_canary_enabled") is not True:
        blockers.append("github_mcp_sub_issue_binding_canary_enabled_not_true")
    if ctx.get("apply_github_mcp_sub_issue_binding_canary") is not True:
        blockers.append("apply_github_mcp_sub_issue_binding_canary_not_true")
    if ctx.get("execute_external_actions") is not True:
        blockers.append("runtime_execute_external_actions_not_true")
    if ctx.get("confirmation") != CONFIRMATION:
        blockers.append("runtime_confirmation_invalid")
    if authority.get("authority_status") != AUTHORITY_READY:
        blockers.append("sub_issue_binding_canary_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "tool_discovery_allowed",
        "external_action_allowed",
        "mcp_write_tool_call_allowed",
        "post_write_reobservation_allowed",
        "compensating_sub_issue_remove_allowed",
        "compensating_child_close_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if authority.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))

    try:
        plan = _read_json(plan_path)
    except Exception as exc:
        plan = {}
        blockers.append(f"plan_read_failed:{type(exc).__name__}")
    _validate_plan(plan, blockers)
    repository = str(plan.get("repository_full_name", ""))
    base_branch = str(plan.get("base_branch", ""))
    base_sha = str(plan.get("base_sha", ""))
    nonce = str(plan.get("transaction_nonce", ""))
    parent_issue_number = int(plan.get("parent_issue_number", 0) or 0)
    server = _mapping(plan.get("server"))
    server_image = str(server.get("image", ""))
    resolved_image_digest = str(ctx.get("resolved_image_digest", ""))
    mode = str(plan.get("mode", ctx.get("mode", "mock")))

    if mode not in {"mock", "stdio"}:
        blockers.append("mode_invalid")
    if ctx.get("repository_full_name", repository) != repository:
        blockers.append("runtime_repository_scope_mismatch")
    if ctx.get("base_sha", base_sha) != base_sha:
        blockers.append("runtime_base_sha_mismatch")
    if ctx.get("transaction_nonce", nonce) != nonce:
        blockers.append("runtime_transaction_nonce_mismatch")
    if int(ctx.get("parent_issue_number", parent_issue_number) or 0) != parent_issue_number:
        blockers.append("runtime_parent_issue_number_mismatch")
    if mode == "stdio" and not resolved_image_digest.startswith("sha256:"):
        blockers.append("resolved_image_digest_missing")

    owner, repo = (repository.split("/", 1) + [""])[:2]
    child_title = f"{CHILD_TITLE_PREFIX}{nonce}"
    child_body = _child_body(
        parent_issue_number=parent_issue_number, base_sha=base_sha, nonce=nonce
    )
    active_transport = transport
    owns_transport = False
    if not blockers and active_transport is None:
        token_env = str(server.get("token_env", "GITHUB_PERSONAL_ACCESS_TOKEN"))
        if not os.environ.get(token_env):
            blockers.append("github_personal_access_token_missing")
        else:
            try:
                active_transport = _open_stdio_transport(server, plan)
                owns_transport = True
            except Exception as exc:
                blockers.append(f"stdio_transport_build_failed:{type(exc).__name__}")

    if not blockers and active_transport is not None:
        try:
            discovered = _tool_map(active_transport.list_tools())
            for required in ("issue_write", "issue_read", "sub_issue_write"):
                if required not in discovered:
                    blockers.append(f"required_tool_not_discovered:{required}")
            for name in ("issue_write", "sub_issue_write"):
                if name in discovered and not _is_write_tool(discovered[name]):
                    blockers.append(f"{name}_not_classified_write")
            if "issue_read" in discovered and _is_write_tool(discovered["issue_read"]):
                blockers.append("issue_read_not_classified_read_only")
        except Exception as exc:
            blockers.append(f"tool_discovery_failed:{type(exc).__name__}")

    parent_identity_verified = False
    parent_subissues_preflight_empty = False
    child_created_verified = False
    binding_added_verified = False
    binding_removed_verified = False
    child_closed_verified = False
    compensation_attempted = False
    compensation_binding_removed = False
    compensation_child_closed = False
    child_issue_id = 0
    child_issue_number = 0
    child_create_attempted = False
    binding_add_attempted = False

    parent_get = {
        "method": "get", "owner": owner, "repo": repo,
        "issue_number": parent_issue_number,
    }
    parent_children = {
        "method": "get_sub_issues", "owner": owner, "repo": repo,
        "issue_number": parent_issue_number, "perPage": 100, "page": 1,
    }

    if not blockers and active_transport is not None:
        response, observed, local = _call_tool(
            active_transport, phase="verify_parent_issue", tool="issue_read", arguments=parent_get
        )
        if not local:
            local += _request_identity_blockers(
                observed, issue_number=parent_issue_number, base_sha=base_sha,
                nonce=nonce, image=server_image
            )
        parent_identity_verified = not local
        records.append(_record(
            phase="verify_parent_issue", tool="issue_read", arguments=parent_get,
            response=response, observed=observed,
            status="verified" if parent_identity_verified else "blocked", blockers=local
        ))
        blockers += local

    if parent_identity_verified and not blockers and active_transport is not None:
        response, observed, local = _call_tool(
            active_transport, phase="preflight_parent_sub_issues",
            tool="issue_read", arguments=parent_children
        )
        if not local:
            local += _sub_issue_set_blockers(
                observed, expected_number=None, expected_title=None
            )
        parent_subissues_preflight_empty = not local
        records.append(_record(
            phase="preflight_parent_sub_issues", tool="issue_read",
            arguments=parent_children, response=response, observed=observed,
            status="verified_empty" if parent_subissues_preflight_empty else "blocked",
            blockers=local
        ))
        blockers += local

    if parent_subissues_preflight_empty and not blockers and active_transport is not None:
        child_create_attempted = True
        create_args = {
            "method": "create", "owner": owner, "repo": repo,
            "title": child_title,
            "body": json.dumps(child_body, ensure_ascii=False, sort_keys=True),
        }
        response, observed, local = _call_tool(
            active_transport, phase="create_child_issue", tool="issue_write",
            arguments=create_args
        )
        if not local:
            child_issue_id, child_issue_number, extract_local = _extract_created_child(observed)
            local += extract_local
        records.append(_record(
            phase="create_child_issue", tool="issue_write", arguments=create_args,
            response=response, observed=observed,
            status="applied" if not local else "blocked", blockers=local
        ))
        blockers += local

    child_get: dict[str, Any] = {}
    if child_issue_number > 0:
        child_get = {
            "method": "get", "owner": owner, "repo": repo,
            "issue_number": child_issue_number,
        }
    if child_create_attempted and not blockers and active_transport is not None:
        response, observed, local = _call_tool(
            active_transport, phase="verify_child_created", tool="issue_read",
            arguments=child_get
        )
        if not local:
            local += _child_identity_blockers(
                observed, issue_number=child_issue_number, title=child_title,
                parent_issue_number=parent_issue_number, base_sha=base_sha,
                nonce=nonce, expected_state="open"
            )
        child_created_verified = not local
        records.append(_record(
            phase="verify_child_created", tool="issue_read", arguments=child_get,
            response=response, observed=observed,
            status="verified" if child_created_verified else "blocked", blockers=local
        ))
        blockers += local

    if child_created_verified and not blockers and active_transport is not None:
        binding_add_attempted = True
        add_args = {
            "method": "add", "owner": owner, "repo": repo,
            "issue_number": parent_issue_number, "sub_issue_id": child_issue_id,
        }
        response, observed, local = _call_tool(
            active_transport, phase="add_sub_issue_binding",
            tool="sub_issue_write", arguments=add_args
        )
        records.append(_record(
            phase="add_sub_issue_binding", tool="sub_issue_write",
            arguments=add_args, response=response, observed=observed,
            status="applied" if not local else "blocked", blockers=local
        ))
        blockers += local

    if binding_add_attempted and not blockers and active_transport is not None:
        response, observed, local = _call_tool(
            active_transport, phase="verify_sub_issue_binding_added",
            tool="issue_read", arguments=parent_children
        )
        if not local:
            local += _sub_issue_set_blockers(
                observed, expected_number=child_issue_number, expected_title=child_title
            )
        binding_added_verified = not local
        records.append(_record(
            phase="verify_sub_issue_binding_added", tool="issue_read",
            arguments=parent_children, response=response, observed=observed,
            status="verified" if binding_added_verified else "blocked", blockers=local
        ))
        blockers += local

    if binding_added_verified and not blockers and active_transport is not None:
        remove_args = {
            "method": "remove", "owner": owner, "repo": repo,
            "issue_number": parent_issue_number, "sub_issue_id": child_issue_id,
        }
        response, observed, local = _call_tool(
            active_transport, phase="remove_sub_issue_binding",
            tool="sub_issue_write", arguments=remove_args
        )
        records.append(_record(
            phase="remove_sub_issue_binding", tool="sub_issue_write",
            arguments=remove_args, response=response, observed=observed,
            status="applied" if not local else "blocked", blockers=local
        ))
        blockers += local

    if binding_added_verified and not blockers and active_transport is not None:
        response, observed, local = _call_tool(
            active_transport, phase="verify_sub_issue_binding_removed",
            tool="issue_read", arguments=parent_children
        )
        if not local:
            local += _sub_issue_set_blockers(
                observed, expected_number=None, expected_title=None
            )
        binding_removed_verified = not local
        records.append(_record(
            phase="verify_sub_issue_binding_removed", tool="issue_read",
            arguments=parent_children, response=response, observed=observed,
            status="verified_empty" if binding_removed_verified else "blocked",
            blockers=local
        ))
        blockers += local

    if binding_removed_verified and not blockers and active_transport is not None:
        close_args = {
            "method": "update", "owner": owner, "repo": repo,
            "issue_number": child_issue_number,
            "state": "closed", "state_reason": "completed",
        }
        response, observed, local = _call_tool(
            active_transport, phase="close_child_issue",
            tool="issue_write", arguments=close_args
        )
        records.append(_record(
            phase="close_child_issue", tool="issue_write", arguments=close_args,
            response=response, observed=observed,
            status="applied" if not local else "blocked", blockers=local
        ))
        blockers += local

    if binding_removed_verified and not blockers and active_transport is not None:
        response, observed, local = _call_tool(
            active_transport, phase="verify_child_closed",
            tool="issue_read", arguments=child_get
        )
        if not local:
            local += _child_identity_blockers(
                observed, issue_number=child_issue_number, title=child_title,
                parent_issue_number=parent_issue_number, base_sha=base_sha,
                nonce=nonce, expected_state="closed"
            )
        child_closed_verified = not local
        records.append(_record(
            phase="verify_child_closed", tool="issue_read", arguments=child_get,
            response=response, observed=observed,
            status="verified" if child_closed_verified else "blocked", blockers=local
        ))
        blockers += local

    primary_verified = (
        parent_identity_verified
        and parent_subissues_preflight_empty
        and child_created_verified
        and binding_added_verified
        and binding_removed_verified
        and child_closed_verified
        and not blockers
    )

    if (
        not primary_verified
        and child_issue_id > 0
        and child_issue_number > 0
        and active_transport is not None
    ):
        compensation_attempted = True
        remove_args = {
            "method": "remove", "owner": owner, "repo": repo,
            "issue_number": parent_issue_number, "sub_issue_id": child_issue_id,
        }
        response, observed, local = _call_tool(
            active_transport, phase="compensate_remove_sub_issue_binding",
            tool="sub_issue_write", arguments=remove_args
        )
        records.append(_record(
            phase="compensate_remove_sub_issue_binding", tool="sub_issue_write",
            arguments=remove_args, response=response, observed=observed,
            status="attempted", blockers=local
        ))
        response2, observed2, local2 = _call_tool(
            active_transport, phase="verify_compensation_binding_removed",
            tool="issue_read", arguments=parent_children
        )
        if not local2:
            local2 += _sub_issue_set_blockers(
                observed2, expected_number=None, expected_title=None
            )
        compensation_binding_removed = not local2
        records.append(_record(
            phase="verify_compensation_binding_removed", tool="issue_read",
            arguments=parent_children, response=response2, observed=observed2,
            status="verified_empty" if compensation_binding_removed else "blocked",
            blockers=local2
        ))

        close_args = {
            "method": "update", "owner": owner, "repo": repo,
            "issue_number": child_issue_number,
            "state": "closed", "state_reason": "not_planned",
        }
        response3, observed3, local3 = _call_tool(
            active_transport, phase="compensate_close_child_issue",
            tool="issue_write", arguments=close_args
        )
        records.append(_record(
            phase="compensate_close_child_issue", tool="issue_write",
            arguments=close_args, response=response3, observed=observed3,
            status="attempted", blockers=local3
        ))
        response4, observed4, local4 = _call_tool(
            active_transport, phase="verify_compensation_child_closed",
            tool="issue_read", arguments=child_get
        )
        if not local4:
            local4 += _child_identity_blockers(
                observed4, issue_number=child_issue_number, title=child_title,
                parent_issue_number=parent_issue_number, base_sha=base_sha,
                nonce=nonce, expected_state="closed"
            )
        compensation_child_closed = not local4
        records.append(_record(
            phase="verify_compensation_child_closed", tool="issue_read",
            arguments=child_get, response=response4, observed=observed4,
            status="verified" if compensation_child_closed else "blocked",
            blockers=local4
        ))

    if owns_transport and active_transport is not None:
        try:
            active_transport.close()
        except Exception as exc:
            warnings.append(f"transport_close_failed:{type(exc).__name__}")

    status = VERIFIED if primary_verified else BLOCKED
    if (
        not primary_verified
        and compensation_attempted
        and compensation_binding_removed
        and compensation_child_closed
    ):
        status = COMPENSATED

    packet_id = f"kuuos-github-mcp-sub-issue-binding-{_sha256([repository, base_sha, nonce, parent_issue_number])[:16]}"
    result = GitHubMCPSubIssueBindingCanaryResult(
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
        parent_subissues_preflight_empty=parent_subissues_preflight_empty,
        child_created_verified=child_created_verified,
        binding_added_verified=binding_added_verified,
        binding_removed_verified=binding_removed_verified,
        child_closed_verified=child_closed_verified,
        compensation_attempted=compensation_attempted,
        compensation_binding_removed=compensation_binding_removed,
        compensation_child_closed=compensation_child_closed,
        records=records,
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
    )
    if authority.get("receipt_write_allowed") is True:
        _write_json(receipt_path, result.to_dict())
    if authority.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, records)
    return result
