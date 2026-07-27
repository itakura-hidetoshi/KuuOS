#!/usr/bin/env python3
from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import selectors
import subprocess
import threading
import time
from typing import Any, Mapping, Protocol, Sequence

PROTOCOL_VERSION = "2025-11-25"
OFFICIAL_IMAGE_PREFIX = "ghcr.io/github/github-mcp-server"
DEFAULT_TOOLSETS = ("context", "repos", "issues", "pull_requests", "users")
ALLOWED_TOOLSETS = frozenset(
    {
        "context",
        "repos",
        "issues",
        "pull_requests",
        "users",
        "actions",
        "code_security",
        "dependabot",
        "discussions",
        "gists",
        "git",
        "labels",
        "notifications",
        "orgs",
        "projects",
        "secret_protection",
        "security_advisories",
        "stargazers",
    }
)
EXACT_SHA_GIT_MUTATION_TOOLS = frozenset(
    {
        "create_branch",
        "create_or_update_file",
        "delete_file",
        "merge_pull_request",
        "push_files",
        "update_pull_request_branch",
    }
)

WRITE_PREFIXES = (
    "add_",
    "assign_",
    "cancel_",
    "close_",
    "convert_",
    "create_",
    "delete_",
    "dismiss_",
    "enable_",
    "lock_",
    "mark_",
    "merge_",
    "fork_",
    "push_",
    "remove_",
    "reply_",
    "request_",
    "rerun_",
    "resolve_",
    "submit_",
    "unlock_",
    "unresolve_",
    "update_",
)


@dataclass(frozen=True)
class GitHubMCPBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    plan_path: str
    authority_path: str
    receipt_path: str
    audit_path: str
    mode: str
    repository_full_name: str
    base_branch: str
    base_sha: str
    read_only: bool
    lockdown_mode: bool
    applied_count: int
    blocked_count: int
    skipped_count: int
    records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class MCPTransport(Protocol):
    def list_tools(self) -> dict[str, Any]: ...

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]: ...

    def close(self) -> None: ...


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _safe_root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str) and item]


def _repository_from_arguments(arguments: Mapping[str, Any]) -> str:
    direct = str(
        arguments.get(
            "repository_full_name",
            arguments.get("repository", arguments.get("repo_full_name", "")),
        )
    )
    if direct and "/" in direct:
        return direct
    owner = str(arguments.get("owner", ""))
    repo = str(arguments.get("repo", arguments.get("repository_name", "")))
    return f"{owner}/{repo}" if owner and repo else ""


def _is_write_tool(name: str, metadata: Mapping[str, Any] | None = None) -> bool:
    annotations = _mapping(_mapping(metadata).get("annotations"))
    if annotations.get("readOnlyHint") is True:
        return False
    if annotations.get("readOnlyHint") is False:
        return True
    lowered = name.lower()
    return lowered.startswith(WRITE_PREFIXES) or any(
        marker in lowered
        for marker in (
            "_create_",
            "_delete_",
            "_merge_",
            "_update_",
            "_write_",
            "_mutate_",
        )
    )


def _tool_map(list_result: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    result = _mapping(list_result.get("result", list_result))
    raw = result.get("tools", [])
    if not isinstance(raw, list):
        return {}
    mapped: dict[str, dict[str, Any]] = {}
    for item in raw:
        if isinstance(item, Mapping) and item.get("name"):
            mapped[str(item["name"])] = dict(item)
    return mapped


def _stdio_command(server: Mapping[str, Any], plan: Mapping[str, Any]) -> tuple[list[str], dict[str, str]]:
    launcher = str(server.get("launcher", "docker"))
    toolsets = _string_list(server.get("toolsets")) or list(DEFAULT_TOOLSETS)
    tools = _string_list(server.get("tools"))
    token_env = str(server.get("token_env", "GITHUB_PERSONAL_ACCESS_TOKEN"))
    env = {
        "GITHUB_TOOLSETS": ",".join(toolsets),
        "GITHUB_READ_ONLY": "1" if plan.get("read_only", True) is True else "0",
        "GITHUB_LOCKDOWN_MODE": "1" if plan.get("lockdown_mode", True) is True else "0",
    }
    if tools:
        env["GITHUB_TOOLS"] = ",".join(tools)
    if launcher == "docker":
        image = str(server.get("image", OFFICIAL_IMAGE_PREFIX))
        command = ["docker", "run", "-i", "--rm"]
        for key in sorted(env):
            command.extend(["-e", key])
        command.extend(["-e", token_env, image])
        return command, env
    if launcher == "binary":
        executable = pathlib.Path(str(server.get("executable", ""))).expanduser()
        if not executable.is_absolute():
            raise ValueError("binary_executable_must_be_absolute")
        return [str(executable), "stdio"], env
    raise ValueError("unsupported_launcher")


class OfficialGitHubMCPStdioClient:
    def __init__(
        self,
        command: Sequence[str],
        env: Mapping[str, str],
        *,
        timeout_seconds: float = 30.0,
    ) -> None:
        merged_env = os.environ.copy()
        merged_env.update({str(k): str(v) for k, v in env.items()})
        self._process = subprocess.Popen(
            list(command),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1,
            env=merged_env,
        )
        if self._process.stdin is None or self._process.stdout is None:
            raise RuntimeError("mcp_stdio_unavailable")
        self._stdin = self._process.stdin
        self._stdout = self._process.stdout
        self._timeout = timeout_seconds
        self._next_id = 1
        self._initialized = False
        self._stderr_lines: deque[str] = deque(maxlen=100)
        self._stderr_thread: threading.Thread | None = None
        if self._process.stderr is not None:
            self._stderr_thread = threading.Thread(
                target=self._drain_stderr,
                name="kuuos-github-mcp-stderr",
                daemon=True,
            )
            self._stderr_thread.start()

    def _drain_stderr(self) -> None:
        stream = self._process.stderr
        if stream is None:
            return
        for line in stream:
            self._stderr_lines.append(line.rstrip("\n"))

    def _request(self, method: str, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
        request_id = self._next_id
        self._next_id += 1
        payload: dict[str, Any] = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            payload["params"] = dict(params)
        self._stdin.write(json.dumps(payload, separators=(",", ":")) + "\n")
        self._stdin.flush()
        selector = selectors.DefaultSelector()
        selector.register(self._stdout, selectors.EVENT_READ)
        deadline = time.monotonic() + self._timeout
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError(f"mcp_timeout:{method}")
                events = selector.select(remaining)
                if not events:
                    continue
                line = self._stdout.readline()
                if line == "":
                    detail = self._stderr_lines[-1] if self._stderr_lines else ""
                    raise RuntimeError(
                        f"mcp_server_closed:{self._process.poll()}:{detail[:240]}"
                    )
                message = json.loads(line)
                if isinstance(message, dict) and message.get("id") == request_id:
                    return message
        finally:
            selector.close()

    def _notify(self, method: str, params: Mapping[str, Any] | None = None) -> None:
        payload: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = dict(params)
        self._stdin.write(json.dumps(payload, separators=(",", ":")) + "\n")
        self._stdin.flush()

    def _ensure_initialized(self) -> None:
        if self._initialized:
            return
        response = self._request(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {
                    "name": "KuuOS GitHub MCP Server Bridge",
                    "version": "0.1.0",
                },
            },
        )
        if "error" in response:
            raise RuntimeError(f"mcp_initialize_error:{response['error']}")
        self._notify("notifications/initialized")
        self._initialized = True

    def list_tools(self) -> dict[str, Any]:
        self._ensure_initialized()
        return self._request("tools/list", {})

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        self._ensure_initialized()
        return self._request("tools/call", {"name": name, "arguments": dict(arguments)})

    def close(self) -> None:
        if self._process.poll() is None:
            self._process.terminate()
            try:
                self._process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait(timeout=3)
        if self._stderr_thread is not None:
            self._stderr_thread.join(timeout=1)
        for stream in (self._process.stdin, self._process.stdout, self._process.stderr):
            if stream is not None and not stream.closed:
                stream.close()


class MockGitHubMCPTransport:
    def __init__(self, tools: Sequence[Mapping[str, Any]] | None = None) -> None:
        self.tools = [dict(item) for item in (tools or [])]
        self.calls: list[dict[str, Any]] = []

    def list_tools(self) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": 1, "result": {"tools": self.tools}}

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        call = {"name": name, "arguments": dict(arguments)}
        self.calls.append(call)
        return {
            "jsonrpc": "2.0",
            "id": len(self.calls) + 1,
            "result": {
                "content": [{"type": "text", "text": json.dumps(call, sort_keys=True)}],
                "structuredContent": call,
                "isError": False,
            },
        }

    def close(self) -> None:
        return None


def _validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != "kuuos_github_mcp_server_bridge_plan_v0_1":
        blockers.append("plan_version_invalid")
    repository = str(plan.get("repository_full_name", ""))
    if repository.count("/") != 1:
        blockers.append("repository_full_name_invalid")
    if not str(plan.get("base_branch", "")):
        blockers.append("base_branch_missing")
    base_sha = str(plan.get("base_sha", ""))
    if len(base_sha) != 40 or any(ch not in "0123456789abcdef" for ch in base_sha.lower()):
        blockers.append("base_sha_invalid")
    if plan.get("lockdown_mode") is not True:
        blockers.append("lockdown_mode_not_true")
    server = _mapping(plan.get("server"))
    if server.get("kind") != "official_github_mcp_server":
        blockers.append("server_kind_invalid")
    toolsets = _string_list(server.get("toolsets")) or list(DEFAULT_TOOLSETS)
    if "all" in toolsets or any(toolset not in ALLOWED_TOOLSETS for toolset in toolsets):
        blockers.append("toolsets_not_bounded")
    tools = _string_list(server.get("tools"))
    if not tools:
        blockers.append("tools_allowlist_empty")
    image = str(server.get("image", OFFICIAL_IMAGE_PREFIX))
    if str(server.get("launcher", "docker")) == "docker" and not (
        image == OFFICIAL_IMAGE_PREFIX or image.startswith(OFFICIAL_IMAGE_PREFIX + ":") or "@sha256:" in image and image.startswith(OFFICIAL_IMAGE_PREFIX)
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
    if plan.get("read_only", True) is True:
        blockers.append("write_tool_blocked_by_read_only")
    if runtime_context.get("execute_external_actions") is not True:
        blockers.append("runtime_execute_external_actions_not_true")
    if plan.get("execute_external_actions") is not True:
        blockers.append("plan_execute_external_actions_not_true")
    if authority.get("external_action_allowed") is not True:
        blockers.append("external_action_not_allowed")
    if authority.get("write_tool_call_allowed") is not True:
        blockers.append("write_tool_call_not_allowed")
    if operation.get("approved") is not True:
        blockers.append("operation_not_approved")
    if str(operation.get("expected_base_sha", "")) != str(plan.get("base_sha", "")):
        blockers.append("expected_base_sha_mismatch")
    return blockers


def build_github_mcp_server_bridge(
    *,
    runtime_context: Mapping[str, Any],
    authority_packet: Mapping[str, Any],
    transport: MCPTransport | None = None,
) -> GitHubMCPBridgeResult:
    ctx = _mapping(runtime_context)
    authority = _mapping(authority_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    root = _safe_root(ctx.get("runtime_root"), blockers)
    plan_path = root / "github_mcp_server_bridge_plan.json"
    authority_path = root / "github_mcp_server_bridge_authority.json"
    receipt_path = root / "github_mcp_server_bridge_receipt.json"
    audit_path = root / "github_mcp_server_bridge_audit.jsonl"

    if ctx.get("github_mcp_server_bridge_enabled") is not True:
        blockers.append("github_mcp_server_bridge_enabled_not_true")
    if ctx.get("apply_github_mcp_server_bridge") is not True:
        blockers.append("apply_github_mcp_server_bridge_not_true")
    if authority.get("authority_status") != "KUUOS_GITHUB_MCP_AUTHORITY_READY":
        blockers.append("github_mcp_authority_not_ready")
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
    read_only = plan.get("read_only", True) is True
    lockdown_mode = plan.get("lockdown_mode") is True
    mode = str(plan.get("mode", ctx.get("mode", "mock")))
    if mode not in {"mock", "stdio"}:
        blockers.append("mode_invalid")

    server = _mapping(plan.get("server"))
    allowed_tools = frozenset(_string_list(server.get("tools")))
    operations_raw = plan.get("operations", [])
    operations = [dict(item) for item in operations_raw if isinstance(item, Mapping)] if isinstance(operations_raw, list) else []
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

    if not blockers and active_transport is not None:
        for index, operation in enumerate(operations):
            kind = str(operation.get("kind", ""))
            local_blockers: list[str] = []
            result: dict[str, Any] = {}
            if kind == "list_tools":
                result = {"tools": sorted(discovered_tools)}
            elif kind == "call_tool":
                tool_name = str(operation.get("tool", ""))
                arguments = _mapping(operation.get("arguments"))
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
                    argument_base = str(arguments.get("base", arguments.get("base_branch", "")))
                    if argument_base and argument_base != base_branch:
                        local_blockers.append("write_base_branch_mismatch")
                    if tool_name in EXACT_SHA_GIT_MUTATION_TOOLS:
                        local_blockers.append("exact_sha_git_mutation_not_admitted_v0_1")
                    local_blockers.extend(
                        _write_gate_blockers(
                            runtime_context=ctx,
                            authority=authority,
                            plan=plan,
                            operation=operation,
                        )
                    )
                if not local_blockers:
                    try:
                        result = active_transport.call_tool(tool_name, arguments)
                        if "error" in result or _mapping(result.get("result")).get("isError") is True:
                            local_blockers.append("tool_call_returned_error")
                    except Exception as exc:  # noqa: BLE001
                        result = {"error": f"{type(exc).__name__}:{exc}"}
                        local_blockers.append("tool_call_exception")
            else:
                local_blockers.append("operation_kind_invalid")

            status = "applied" if not local_blockers else "blocked"
            record = {
                "index": index,
                "kind": kind,
                "tool": str(operation.get("tool", "")),
                "status": status,
                "operation_digest": _sha256(operation),
                "result": result,
                "blockers": sorted(set(local_blockers)),
                "epoch": int(time.time()),
            }
            record["record_digest"] = _sha256(record)
            if authority.get("audit_append_allowed") is True:
                _append_jsonl(audit_path, record)
            records.append(record)

    if owns_transport and active_transport is not None:
        active_transport.close()

    applied = sum(record.get("status") == "applied" for record in records)
    blocked = sum(record.get("status") == "blocked" for record in records)
    skipped = len(operations) - len(records)
    if blockers:
        status = "KUUOS_GITHUB_MCP_BRIDGE_BLOCKED"
    elif blocked:
        status = "KUUOS_GITHUB_MCP_BRIDGE_PARTIAL"
    elif applied:
        status = "KUUOS_GITHUB_MCP_BRIDGE_APPLIED"
    else:
        status = "KUUOS_GITHUB_MCP_BRIDGE_IDLE"
    packet_id = "kuuos-github-mcp-" + _sha256(
        {"plan": plan, "records": records, "blockers": blockers}
    )[:16]
    receipt = {
        "version": "kuuos_github_mcp_server_bridge_v0_1",
        "status": status,
        "packet_id": packet_id,
        "mode": mode,
        "repository_full_name": repository,
        "base_branch": base_branch,
        "base_sha": base_sha,
        "read_only": read_only,
        "lockdown_mode": lockdown_mode,
        "applied_count": applied,
        "blocked_count": blocked,
        "skipped_count": skipped,
        "records": records,
        "blockers": sorted(set(blockers)),
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if authority.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    return GitHubMCPBridgeResult(
        "kuuos_github_mcp_server_bridge_v0_1",
        status,
        packet_id,
        str(root),
        str(plan_path),
        str(authority_path),
        str(receipt_path),
        str(audit_path),
        mode,
        repository,
        base_branch,
        base_sha,
        read_only,
        lockdown_mode,
        applied,
        blocked,
        skipped,
        records,
        sorted(set(blockers)),
        warnings,
    )
