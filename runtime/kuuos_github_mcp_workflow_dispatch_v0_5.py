#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import os
import re
import time
from typing import Any, Mapping

from runtime.kuuos_github_mcp_live_canary_v0_4 import (
    _is_pinned_official_image,
    _tool_returned_error,
)
from runtime.kuuos_github_mcp_live_write_verification_v0_3 import _normalize_tool_payload
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

PLAN_VERSION = "kuuos_github_mcp_workflow_dispatch_plan_v0_5"
AUTHORITY_READY = "KUUOS_GITHUB_MCP_WORKFLOW_DISPATCH_AUTHORITY_READY"
CONFIRMATION = "RUN_KUUOS_GITHUB_MCP_WORKFLOW_DISPATCH"
VERIFIED = "KUUOS_GITHUB_MCP_WORKFLOW_DISPATCH_VERIFIED"
MISMATCH_CANCELLED = "KUUOS_GITHUB_MCP_WORKFLOW_DISPATCH_MISMATCH_CANCELLED"
BLOCKED = "KUUOS_GITHUB_MCP_WORKFLOW_DISPATCH_BLOCKED"
NONCE_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{7,63}")


@dataclass(frozen=True)
class GitHubMCPWorkflowDispatchResult:
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
    workflow_id: str
    target_ref: str
    dispatch_nonce: str
    dispatch_accepted: bool
    run_observed: bool
    run_id: int
    run_url: str
    run_status: str
    run_head_sha: str
    mismatch_cancel_attempted: bool
    mismatch_cancelled: bool
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


def _extract_runs(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [dict(item) for item in payload if isinstance(item, Mapping)]
    value = _mapping(payload)
    for key in ("workflow_runs", "runs"):
        raw = value.get(key)
        if isinstance(raw, list):
            return [dict(item) for item in raw if isinstance(item, Mapping)]
    nested = value.get("workflow_runs")
    if isinstance(nested, Mapping):
        raw = nested.get("workflow_runs")
        if isinstance(raw, list):
            return [dict(item) for item in raw if isinstance(item, Mapping)]
    return []


def _run_id(run: Mapping[str, Any]) -> int:
    try:
        return int(run.get("id", 0) or 0)
    except (TypeError, ValueError):
        return 0


def _run_url(run: Mapping[str, Any]) -> str:
    return str(run.get("html_url", run.get("url", "")))


def _run_title(run: Mapping[str, Any]) -> str:
    return str(run.get("display_title", run.get("name", "")))


def _run_matches_scope(
    run: Mapping[str, Any],
    *,
    target_ref: str,
    nonce: str,
) -> bool:
    event = str(run.get("event", ""))
    branch = str(run.get("head_branch", run.get("branch", "")))
    return event == "workflow_dispatch" and branch == target_ref and nonce in _run_title(run)


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
        blockers.append("workflow_dispatch_requires_read_only_false")
    if plan.get("lockdown_mode") is not True:
        blockers.append("lockdown_mode_not_true")
    if plan.get("execute_external_actions") is not True:
        blockers.append("plan_execute_external_actions_not_true")
    if plan.get("confirmation") != CONFIRMATION:
        blockers.append("plan_confirmation_invalid")

    target = _mapping(plan.get("target"))
    workflow_id = str(target.get("workflow_id", ""))
    target_ref = str(target.get("ref", ""))
    expected_head_sha = str(target.get("expected_head_sha", ""))
    nonce = str(target.get("dispatch_nonce", ""))
    inputs = target.get("inputs")
    if not workflow_id or workflow_id.startswith("/") or ".." in workflow_id.split("/"):
        blockers.append("target_workflow_id_invalid")
    if target_ref != str(plan.get("base_branch", "")):
        blockers.append("target_ref_must_equal_base_branch")
    if expected_head_sha != str(plan.get("base_sha", "")):
        blockers.append("target_expected_head_sha_mismatch")
    if not NONCE_PATTERN.fullmatch(nonce):
        blockers.append("dispatch_nonce_invalid")
    if not isinstance(inputs, Mapping):
        blockers.append("target_inputs_invalid")
    elif str(inputs.get("dispatch_nonce", "")) != nonce:
        blockers.append("target_input_nonce_mismatch")

    server = _mapping(plan.get("server"))
    if server.get("kind") != "official_github_mcp_server":
        blockers.append("server_kind_invalid")
    if not _is_pinned_official_image(server.get("image", "")):
        blockers.append("official_server_image_not_pinned")
    toolsets = server.get("toolsets")
    if not isinstance(toolsets, list) or set(str(item) for item in toolsets) != {"actions"}:
        blockers.append("actions_toolset_required")
    tools = server.get("tools")
    if not isinstance(tools, list) or set(str(item) for item in tools) != {
        "actions_run_trigger",
        "actions_list",
    }:
        blockers.append("workflow_dispatch_tool_allowlist_invalid")


def build_github_mcp_workflow_dispatch(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
    transport: MCPTransport | None = None,
) -> GitHubMCPWorkflowDispatchResult:
    ctx = _mapping(runtime_context)
    authority = _mapping(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []

    root = _safe_root(ctx.get("runtime_root"), blockers)
    plan_path = root / "github_mcp_workflow_dispatch_plan_v0_5.json"
    authority_path = root / "github_mcp_workflow_dispatch_authority_v0_5.json"
    receipt_path = root / "github_mcp_workflow_dispatch_receipt_v0_5.json"
    audit_path = root / "github_mcp_workflow_dispatch_audit_v0_5.jsonl"

    if ctx.get("github_mcp_workflow_dispatch_enabled") is not True:
        blockers.append("github_mcp_workflow_dispatch_enabled_not_true")
    if ctx.get("apply_github_mcp_workflow_dispatch") is not True:
        blockers.append("apply_github_mcp_workflow_dispatch_not_true")
    if ctx.get("execute_external_actions") is not True:
        blockers.append("runtime_execute_external_actions_not_true")
    if ctx.get("confirmation") != CONFIRMATION:
        blockers.append("runtime_confirmation_invalid")
    if authority.get("authority_status") != AUTHORITY_READY:
        blockers.append("workflow_dispatch_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "tool_discovery_allowed",
        "external_action_allowed",
        "workflow_dispatch_allowed",
        "run_reobservation_allowed",
        "mismatched_run_cancel_allowed",
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

    owner, repo = (repository.split("/", 1) + [""])[:2]
    target = dict(_mapping(plan.get("target")))
    workflow_id = str(target.get("workflow_id", ""))
    target_ref = str(target.get("ref", ""))
    expected_head_sha = str(target.get("expected_head_sha", ""))
    dispatch_nonce = str(target.get("dispatch_nonce", ""))
    inputs = dict(_mapping(target.get("inputs")))
    server = dict(_mapping(plan.get("server")))

    poll_attempts = int(ctx.get("poll_attempts", 8) or 8)
    poll_interval = float(ctx.get("poll_interval_seconds", 2.0) or 0.0)
    if poll_attempts < 1 or poll_attempts > 30:
        blockers.append("poll_attempts_out_of_bounds")

    active_transport = transport
    owns_transport = False
    discovered_tools: dict[str, dict[str, Any]] = {}
    if not blockers and active_transport is None:
        if mode == "mock":
            blockers.append("mock_transport_required")
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
            listed = active_transport.list_tools()
            if "error" in listed:
                blockers.append("tool_discovery_protocol_error")
            else:
                discovered_tools = _tool_map(listed)
                for required in ("actions_run_trigger", "actions_list"):
                    if required not in discovered_tools:
                        blockers.append(f"required_tool_not_discovered:{required}")
                if "actions_run_trigger" in discovered_tools and not _is_write_tool(
                    "actions_run_trigger", discovered_tools["actions_run_trigger"]
                ):
                    blockers.append("actions_run_trigger_not_classified_write")
                if "actions_list" in discovered_tools and _is_write_tool(
                    "actions_list", discovered_tools["actions_list"]
                ):
                    blockers.append("actions_list_not_classified_read_only")
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"tool_discovery_failed:{type(exc).__name__}")

    list_args = {
        "method": "list_workflow_runs",
        "owner": owner,
        "repo": repo,
        "resource_id": workflow_id,
        "workflow_runs_filter": {
            "branch": target_ref,
            "event": "workflow_dispatch",
        },
        "page": 1,
        "per_page": 50,
    }
    baseline_ids: set[int] = set()
    if not blockers and active_transport is not None:
        response, observed, local = _call_tool(
            active_transport,
            phase="baseline",
            tool="actions_list",
            arguments=list_args,
        )
        if not local:
            baseline_ids = {_run_id(run) for run in _extract_runs(observed) if _run_id(run) > 0}
        records.append(
            _record(
                phase="baseline",
                tool="actions_list",
                arguments=list_args,
                response=response,
                observed=observed,
                status="observed" if not local else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    dispatch_accepted = False
    if not blockers and active_transport is not None:
        dispatch_args = {
            "method": "run_workflow",
            "owner": owner,
            "repo": repo,
            "workflow_id": workflow_id,
            "ref": target_ref,
            "inputs": inputs,
        }
        response, observed, local = _call_tool(
            active_transport,
            phase="dispatch",
            tool="actions_run_trigger",
            arguments=dispatch_args,
        )
        if not local:
            payload = _mapping(observed)
            status_code = int(payload.get("status_code", 0) or 0)
            if status_code != 204:
                local.append("dispatch_status_code_not_204")
            if str(payload.get("workflow_id", "")) != workflow_id:
                local.append("dispatch_workflow_id_mismatch")
            if str(payload.get("ref", "")) != target_ref:
                local.append("dispatch_ref_mismatch")
        dispatch_accepted = not local
        records.append(
            _record(
                phase="dispatch",
                tool="actions_run_trigger",
                arguments=dispatch_args,
                response=response,
                observed=observed,
                status="accepted" if not local else "blocked",
                blockers=local,
            )
        )
        blockers.extend(local)

    run_observed = False
    run_id = 0
    run_url = ""
    run_status = ""
    run_head_sha = ""
    mismatch_cancel_attempted = False
    mismatch_cancelled = False
    mismatch_run: dict[str, Any] | None = None

    if dispatch_accepted and active_transport is not None and not blockers:
        for attempt in range(poll_attempts):
            response, observed, local = _call_tool(
                active_transport,
                phase=f"reobserve_{attempt + 1}",
                tool="actions_list",
                arguments=list_args,
            )
            runs = _extract_runs(observed) if not local else []
            new_runs = [run for run in runs if _run_id(run) not in baseline_ids and _run_id(run) > 0]
            scoped = [
                run
                for run in new_runs
                if _run_matches_scope(run, target_ref=target_ref, nonce=dispatch_nonce)
            ]
            exact = [run for run in scoped if str(run.get("head_sha", "")) == expected_head_sha]
            mismatched = [run for run in scoped if str(run.get("head_sha", "")) != expected_head_sha]
            local_status = "not_found"
            if exact:
                selected = sorted(exact, key=_run_id)[0]
                run_observed = True
                run_id = _run_id(selected)
                run_url = _run_url(selected)
                run_status = str(selected.get("status", ""))
                run_head_sha = str(selected.get("head_sha", ""))
                local_status = "verified"
            elif mismatched:
                mismatch_run = sorted(mismatched, key=_run_id)[0]
                run_id = _run_id(mismatch_run)
                run_url = _run_url(mismatch_run)
                run_status = str(mismatch_run.get("status", ""))
                run_head_sha = str(mismatch_run.get("head_sha", ""))
                local.append("observed_run_head_sha_mismatch")
                local_status = "mismatch"
            records.append(
                _record(
                    phase=f"reobserve_{attempt + 1}",
                    tool="actions_list",
                    arguments=list_args,
                    response=response,
                    observed=observed,
                    status=local_status,
                    blockers=local,
                )
            )
            if run_observed or mismatch_run is not None:
                break
            if attempt + 1 < poll_attempts and poll_interval > 0:
                time.sleep(poll_interval)
        if not run_observed and mismatch_run is None:
            blockers.append("dispatched_run_not_observed")

    if mismatch_run is not None and active_transport is not None:
        mismatch_cancel_attempted = True
        cancel_args = {
            "method": "cancel_workflow_run",
            "owner": owner,
            "repo": repo,
            "run_id": _run_id(mismatch_run),
        }
        response, observed, local = _call_tool(
            active_transport,
            phase="cancel_mismatch",
            tool="actions_run_trigger",
            arguments=cancel_args,
        )
        if not local:
            payload = _mapping(observed)
            if int(payload.get("run_id", 0) or 0) != _run_id(mismatch_run):
                local.append("cancelled_run_id_mismatch")
            if int(payload.get("status_code", 0) or 0) not in {202, 409}:
                local.append("cancel_status_code_unexpected")
        mismatch_cancelled = not local
        records.append(
            _record(
                phase="cancel_mismatch",
                tool="actions_run_trigger",
                arguments=cancel_args,
                response=response,
                observed=observed,
                status="cancelled" if not local else "blocked",
                blockers=local,
            )
        )
        blockers.append("observed_run_head_sha_mismatch")
        warnings.extend(local)

    if owns_transport and active_transport is not None:
        active_transport.close()

    if dispatch_accepted and run_observed and run_head_sha == expected_head_sha and not blockers:
        status = VERIFIED
    elif mismatch_cancel_attempted and mismatch_cancelled:
        status = MISMATCH_CANCELLED
    else:
        status = BLOCKED

    packet_id = "kuuos-github-mcp-workflow-dispatch-" + _sha256(
        {
            "plan": plan,
            "records": records,
            "blockers": blockers,
            "run_id": run_id,
        }
    )[:16]
    receipt = {
        "version": "kuuos_github_mcp_workflow_dispatch_v0_5",
        "status": status,
        "packet_id": packet_id,
        "repository_full_name": repository,
        "base_branch": base_branch,
        "base_sha": base_sha,
        "workflow_id": workflow_id,
        "target_ref": target_ref,
        "dispatch_nonce": dispatch_nonce,
        "dispatch_accepted": dispatch_accepted,
        "run_observed": run_observed,
        "run_id": run_id,
        "run_url": run_url,
        "run_status": run_status,
        "run_head_sha": run_head_sha,
        "mismatch_cancel_attempted": mismatch_cancel_attempted,
        "mismatch_cancelled": mismatch_cancelled,
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

    return GitHubMCPWorkflowDispatchResult(
        "kuuos_github_mcp_workflow_dispatch_v0_5",
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
        workflow_id,
        target_ref,
        dispatch_nonce,
        dispatch_accepted,
        run_observed,
        run_id,
        run_url,
        run_status,
        run_head_sha,
        mismatch_cancel_attempted,
        mismatch_cancelled,
        records,
        sorted(set(blockers)),
        warnings,
    )
