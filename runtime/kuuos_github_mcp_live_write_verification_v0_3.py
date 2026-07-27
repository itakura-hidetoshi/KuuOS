#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
import time
from typing import Any, Mapping

from runtime.kuuos_github_mcp_server_bridge_v0_1 import (
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
from runtime.kuuos_github_mcp_server_bridge_v0_2 import (
    AUTHORITY_READY,
    build_github_mcp_write_bridge,
)

PLAN_VERSION = "kuuos_github_mcp_live_write_verification_plan_v0_3"
AUTHORITY_V03_READY = "KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFICATION_AUTHORITY_READY"


@dataclass(frozen=True)
class GitHubMCPLiveWriteVerificationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    plan_path: str
    authority_path: str
    receipt_path: str
    audit_path: str
    write_receipt_path: str
    mode: str
    repository_full_name: str
    base_branch: str
    base_sha: str
    write_packet_id: str
    verified_count: int
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


def _normalize_tool_payload(response: Mapping[str, Any]) -> Any:
    if "error" in response:
        return {}
    raw: Any = response.get("result", response)
    if not isinstance(raw, Mapping):
        return raw
    structured = raw.get("structuredContent")
    if isinstance(structured, (Mapping, list)):
        return structured
    content = raw.get("content")
    if isinstance(content, list):
        for item in content:
            if not isinstance(item, Mapping):
                continue
            nested = item.get("structuredContent")
            if isinstance(nested, (Mapping, list)):
                return nested
            text = item.get("text")
            if isinstance(text, str):
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return {"text": text}
    return dict(raw)


def _path_get(value: Any, path: str) -> Any:
    if path in {"", "."}:
        return value
    current = value
    for token in path.split("."):
        if isinstance(current, Mapping):
            if token not in current:
                raise KeyError(path)
            current = current[token]
            continue
        if isinstance(current, list):
            try:
                current = current[int(token)]
            except (ValueError, IndexError) as exc:
                raise KeyError(path) from exc
            continue
        raise KeyError(path)
    return current


def _issue_number_from_url(value: Any) -> int:
    text = str(value).rstrip("/")
    tail = text.rsplit("/", 1)[-1]
    if not tail.isdigit() or int(tail) <= 0:
        raise ValueError("write_url_issue_number_invalid")
    return int(tail)


def _resolve_bindings(value: Any, write_payload: Any) -> Any:
    if isinstance(value, Mapping):
        if set(value) == {"$from_write"}:
            return _path_get(write_payload, str(value["$from_write"]))
        if set(value) == {"$issue_number_from_write_url"}:
            url = _path_get(write_payload, str(value["$issue_number_from_write_url"]))
            return _issue_number_from_url(url)
        return {
            str(key): _resolve_bindings(item, write_payload)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_resolve_bindings(item, write_payload) for item in value]
    return value


def _assertion_blockers(
    *,
    observed: Any,
    write_payload: Any,
    assertions: list[Mapping[str, Any]],
) -> list[str]:
    blockers: list[str] = []
    for index, assertion in enumerate(assertions):
        path = str(assertion.get("path", ""))
        try:
            actual = _path_get(observed, path)
        except KeyError:
            blockers.append(f"verification_path_missing:{index}:{path}")
            continue
        if "equals" in assertion:
            if actual != assertion.get("equals"):
                blockers.append(f"verification_equals_mismatch:{index}:{path}")
        elif "equals_write_path" in assertion:
            write_path = str(assertion.get("equals_write_path", ""))
            try:
                expected = _path_get(write_payload, write_path)
            except KeyError:
                blockers.append(f"write_path_missing:{index}:{write_path}")
                continue
            if actual != expected:
                blockers.append(f"verification_write_value_mismatch:{index}:{path}")
        elif "equals_write_url_issue_number" in assertion:
            write_path = str(assertion.get("equals_write_url_issue_number", ""))
            try:
                expected = _issue_number_from_url(_path_get(write_payload, write_path))
            except (KeyError, ValueError):
                blockers.append(f"write_issue_url_invalid:{index}:{write_path}")
                continue
            if actual != expected:
                blockers.append(f"verification_issue_number_mismatch:{index}:{path}")
        elif "contains" in assertion:
            expected = assertion.get("contains")
            if isinstance(actual, str):
                matched = str(expected) in actual
            elif isinstance(actual, (list, tuple, set)):
                matched = expected in actual
            elif isinstance(actual, Mapping):
                matched = expected in actual
            else:
                matched = False
            if not matched:
                blockers.append(f"verification_contains_mismatch:{index}:{path}")
        else:
            blockers.append(f"verification_assertion_operator_missing:{index}")
    return blockers


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
        blockers.append("live_write_verification_requires_read_only_false")
    if plan.get("lockdown_mode") is not True:
        blockers.append("lockdown_mode_not_true")
    if plan.get("execute_external_actions") is not True:
        blockers.append("plan_execute_external_actions_not_true")
    transactions = plan.get("transactions")
    if not isinstance(transactions, list) or not transactions:
        blockers.append("transactions_missing")


def _record(
    *,
    index: int,
    transaction: Mapping[str, Any],
    status: str,
    write_record: Mapping[str, Any],
    verification_tool: str,
    verification_arguments: Mapping[str, Any],
    verification_result: Mapping[str, Any],
    observed: Any,
    blockers: list[str],
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "index": index,
        "status": status,
        "transaction_digest": _sha256(transaction),
        "write_record_digest": str(write_record.get("record_digest", "")),
        "verification_tool": verification_tool,
        "verification_arguments_digest": _sha256(verification_arguments),
        "verification_result": dict(verification_result),
        "observed": observed,
        "observed_digest": _sha256(observed),
        "blockers": sorted(set(blockers)),
        "epoch": int(time.time()),
    }
    record["record_digest"] = _sha256(record)
    return record


def build_github_mcp_live_write_verification(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
    transport: MCPTransport | None = None,
    qi_transport: Any = None,
) -> GitHubMCPLiveWriteVerificationResult:
    ctx = _mapping(runtime_context)
    authority = _mapping(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []

    root = _safe_root(ctx.get("runtime_root"), blockers)
    plan_path = root / "github_mcp_live_write_verification_plan_v0_3.json"
    authority_path = root / "github_mcp_live_write_verification_authority_v0_3.json"
    receipt_path = root / "github_mcp_live_write_verification_receipt_v0_3.json"
    audit_path = root / "github_mcp_live_write_verification_audit_v0_3.jsonl"
    write_plan_path = root / "github_mcp_server_bridge_plan_v0_2.json"
    write_receipt_path = root / "github_mcp_server_bridge_receipt_v0_2.json"

    if ctx.get("github_mcp_live_write_verification_enabled") is not True:
        blockers.append("github_mcp_live_write_verification_enabled_not_true")
    if ctx.get("apply_github_mcp_live_write_verification") is not True:
        blockers.append("apply_github_mcp_live_write_verification_not_true")
    if ctx.get("execute_external_actions") is not True:
        blockers.append("runtime_execute_external_actions_not_true")
    if authority.get("authority_status") != AUTHORITY_V03_READY:
        blockers.append("live_write_verification_authority_not_ready")
    for field in (
        "plan_read_allowed",
        "tool_discovery_allowed",
        "external_action_allowed",
        "mcp_write_tool_call_allowed",
        "exact_git_delegation_allowed",
        "post_write_reobservation_allowed",
        "verification_tool_call_allowed",
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

    server = dict(_mapping(plan.get("server")))
    allowed_tools = frozenset(_string_list(server.get("tools")))
    transactions_raw = plan.get("transactions", [])
    transactions = (
        [dict(item) for item in transactions_raw if isinstance(item, Mapping)]
        if isinstance(transactions_raw, list)
        else []
    )

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
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"tool_discovery_failed:{type(exc).__name__}")

    write_operations = [dict(_mapping(transaction.get("write"))) for transaction in transactions]
    write_plan = {
        "version": "kuuos_github_mcp_server_bridge_plan_v0_2",
        "mode": mode,
        "repository_full_name": repository,
        "base_branch": base_branch,
        "base_sha": base_sha,
        "write_capable": True,
        "read_only": False,
        "lockdown_mode": True,
        "execute_external_actions": True,
        "server": server,
        "operations": write_operations,
    }
    write_result = None
    if not blockers and active_transport is not None:
        _write_json(write_plan_path, write_plan)
        v02_authority = dict(authority)
        v02_authority["authority_status"] = AUTHORITY_READY
        try:
            write_result = build_github_mcp_write_bridge(
                runtime_context={
                    "runtime_root": str(root),
                    "github_mcp_server_bridge_enabled": True,
                    "apply_github_mcp_server_bridge": True,
                    "execute_external_actions": True,
                },
                authority_packet=v02_authority,
                transport=active_transport,
                qi_transport=qi_transport,
            )
        except Exception as exc:  # noqa: BLE001
            blockers.append(f"write_bridge_exception:{type(exc).__name__}")

    if not blockers and write_result is not None and active_transport is not None:
        for index, transaction in enumerate(transactions):
            local_blockers: list[str] = []
            write_record = write_result.records[index] if index < len(write_result.records) else {}
            if write_record.get("status") != "applied":
                local_blockers.append("write_not_applied")
            write_payload = _normalize_tool_payload(_mapping(write_record.get("result")))
            verification = _mapping(transaction.get("verify"))
            verification_tool = str(verification.get("tool", ""))
            verification_arguments_raw = verification.get("arguments", {})
            try:
                verification_arguments = _resolve_bindings(
                    verification_arguments_raw, write_payload
                )
            except (KeyError, ValueError) as exc:
                verification_arguments = {}
                local_blockers.append(f"verification_binding_failed:{exc}")
            if not isinstance(verification_arguments, Mapping):
                verification_arguments = {}
                local_blockers.append("verification_arguments_invalid")
            if verification_tool not in allowed_tools:
                local_blockers.append("verification_tool_not_allowlisted")
            metadata = discovered_tools.get(verification_tool, {})
            if verification_tool not in discovered_tools:
                local_blockers.append("verification_tool_not_discovered")
            elif _is_write_tool(verification_tool, metadata):
                local_blockers.append("verification_tool_must_be_read_only")
            verify_repository = _repository_from_arguments(verification_arguments)
            if verify_repository != repository:
                local_blockers.append("verification_repository_scope_mismatch")
            verification_result: dict[str, Any] = {}
            observed: Any = {}
            if not local_blockers:
                try:
                    verification_result = active_transport.call_tool(
                        verification_tool, verification_arguments
                    )
                    if (
                        "error" in verification_result
                        or _mapping(verification_result.get("result")).get("isError") is True
                    ):
                        local_blockers.append("verification_tool_returned_error")
                    else:
                        observed = _normalize_tool_payload(verification_result)
                except Exception as exc:  # noqa: BLE001
                    verification_result = {"error": f"{type(exc).__name__}:{exc}"}
                    local_blockers.append("verification_tool_exception")
            assertions_raw = verification.get("assertions", [])
            assertions = (
                [item for item in assertions_raw if isinstance(item, Mapping)]
                if isinstance(assertions_raw, list)
                else []
            )
            if not assertions:
                local_blockers.append("verification_assertions_missing")
            if not local_blockers:
                local_blockers.extend(
                    _assertion_blockers(
                        observed=observed,
                        write_payload=write_payload,
                        assertions=assertions,
                    )
                )
            records.append(
                _record(
                    index=index,
                    transaction=transaction,
                    status="verified" if not local_blockers else "blocked",
                    write_record=write_record,
                    verification_tool=verification_tool,
                    verification_arguments=verification_arguments,
                    verification_result=verification_result,
                    observed=observed,
                    blockers=local_blockers,
                )
            )

    if owns_transport and active_transport is not None:
        active_transport.close()

    if authority.get("audit_append_allowed") is True:
        for record in records:
            _append_jsonl(audit_path, record)

    verified = sum(record.get("status") == "verified" for record in records)
    blocked_count = sum(record.get("status") == "blocked" for record in records)
    skipped = len(transactions) - len(records)
    if blockers:
        status = "KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFICATION_BLOCKED"
    elif blocked_count:
        status = "KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFICATION_PARTIAL"
    elif verified:
        status = "KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFIED"
    else:
        status = "KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFICATION_IDLE"

    write_packet_id = write_result.packet_id if write_result is not None else ""
    packet_id = "kuuos-github-mcp-live-verified-" + _sha256(
        {
            "plan": plan,
            "write_packet_id": write_packet_id,
            "records": records,
            "blockers": blockers,
        }
    )[:16]
    receipt = {
        "version": "kuuos_github_mcp_live_write_verification_v0_3",
        "status": status,
        "packet_id": packet_id,
        "mode": mode,
        "repository_full_name": repository,
        "base_branch": base_branch,
        "base_sha": base_sha,
        "write_packet_id": write_packet_id,
        "verified_count": verified,
        "blocked_count": blocked_count,
        "skipped_count": skipped,
        "records": records,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if authority.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)

    return GitHubMCPLiveWriteVerificationResult(
        "kuuos_github_mcp_live_write_verification_v0_3",
        status,
        packet_id,
        str(root),
        str(plan_path),
        str(authority_path),
        str(receipt_path),
        str(audit_path),
        str(write_receipt_path),
        mode,
        repository,
        base_branch,
        base_sha,
        write_packet_id,
        verified,
        blocked_count,
        skipped,
        records,
        sorted(set(blockers)),
        warnings,
    )
