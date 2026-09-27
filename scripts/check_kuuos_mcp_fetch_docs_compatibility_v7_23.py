#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import selectors
import subprocess
import time
import urllib.error
import urllib.request
from typing import Any, Mapping, Sequence

FETCH_SOURCE_VERSION = "0.6.3"
FETCH_PUBLISHED_VERSION = "2026.8.18"
FETCH_MCP_SDK_VERSION = "1.29.0"
REFERENCE_SERVERS_SHA = "f46d9578190b476b3501923ea8977d899e8db2cb"

DOCS_ENDPOINT = "https://modelcontextprotocol.io/mcp"
DOCS_REPOSITORY_SHA = "ab3a39c13bd23be691c2760e1c6c5c15a64582e1"
MODERN_PROTOCOL_VERSION = "2026-07-28"
LEGACY_PROTOCOL_VERSION = "2025-11-25"
DOCS_TOOL = "search_model_context_protocol"
FETCH_PROBE_URL = (
    "https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/"
    + DOCS_REPOSITORY_SHA
    + "/README.md"
)

def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


class MCPStdioClient:
    def __init__(
        self,
        command: Sequence[str],
        *,
        cwd: pathlib.Path,
        timeout_seconds: float = 120.0,
    ) -> None:
        self.process = subprocess.Popen(
            list(command),
            cwd=str(cwd),
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )
        if self.process.stdin is None or self.process.stdout is None:
            raise RuntimeError("mcp_stdio_unavailable")
        self.stdin = self.process.stdin
        self.stdout = self.process.stdout
        self.stderr = self.process.stderr
        self.timeout = timeout_seconds
        self.next_id = 1

    def request(
        self,
        method: str,
        params: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        request_id = self.next_id
        self.next_id += 1
        payload: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
        }
        if params is not None:
            payload["params"] = dict(params)
        self.stdin.write(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
            + "\n"
        )
        self.stdin.flush()

        selector = selectors.DefaultSelector()
        selector.register(self.stdout, selectors.EVENT_READ)
        deadline = time.monotonic() + self.timeout
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError(f"mcp_timeout:{method}")
                if not selector.select(remaining):
                    continue
                line = self.stdout.readline()
                if line == "":
                    stderr = ""
                    if self.stderr is not None:
                        try:
                            stderr = self.stderr.read()
                        except Exception:
                            pass
                    raise RuntimeError(
                        "mcp_server_closed:"
                        + str(self.process.poll())
                        + ":"
                        + stderr[-1800:]
                    )
                line = line.strip()
                if not line:
                    continue
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(message, dict) and message.get("id") == request_id:
                    if "error" in message:
                        raise RuntimeError(
                            "mcp_rpc_error:"
                            + method
                            + ":"
                            + json.dumps(message["error"], ensure_ascii=False)
                        )
                    return message
        finally:
            selector.close()

    def notify(self, method: str) -> None:
        self.stdin.write(
            json.dumps({"jsonrpc": "2.0", "method": method}) + "\n"
        )
        self.stdin.flush()

    def close(self) -> None:
        try:
            self.stdin.close()
        except Exception:
            pass
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)


def tool_names(response: Mapping[str, Any]) -> set[str]:
    result = response.get("result", {})
    raw = result.get("tools", []) if isinstance(result, Mapping) else []
    if not isinstance(raw, list):
        return set()
    return {
        str(item.get("name"))
        for item in raw
        if isinstance(item, Mapping) and item.get("name")
    }


def result_text(response: Mapping[str, Any]) -> str:
    result = response.get("result", {})
    if not isinstance(result, Mapping):
        return ""
    parts: list[str] = []
    content = result.get("content", [])
    if isinstance(content, list):
        for item in content:
            if isinstance(item, Mapping) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
    structured = result.get("structuredContent")
    if structured is not None:
        parts.append(json.dumps(structured, ensure_ascii=False))
    return "\n".join(parts)


def verify_fetch_published_version(root: pathlib.Path) -> str:
    completed = subprocess.run(
        [
            "uv",
            "run",
            "--no-project",
            "--with",
            f"mcp-server-fetch=={FETCH_PUBLISHED_VERSION}",
            "--with",
            f"mcp=={FETCH_MCP_SDK_VERSION}",
            "python",
            "-c",
            (
                "import importlib.metadata as m; "
                "print(m.version('mcp-server-fetch'))"
            ),
        ],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=True,
        timeout=120,
    )
    version = completed.stdout.strip().splitlines()[-1].strip()
    if version != FETCH_PUBLISHED_VERSION:
        raise RuntimeError(
            "fetch_published_version_mismatch:"
            + version
            + ":"
            + FETCH_PUBLISHED_VERSION
        )
    return version


def probe_fetch(root: pathlib.Path) -> dict[str, Any]:
    published_version = verify_fetch_published_version(root)
    command = [
        "uvx",
        "--from",
        f"mcp-server-fetch=={published_version}",
        "--with",
        f"mcp=={FETCH_MCP_SDK_VERSION}",
        "mcp-server-fetch",
    ]
    client = MCPStdioClient(command, cwd=root)
    try:
        initialized = client.request(
            "initialize",
            {
                "protocolVersion": LEGACY_PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {
                    "name": "KuuOS Fetch MCP Compatibility Probe",
                    "version": "7.23",
                },
            },
        )
        client.notify("notifications/initialized")
        listed = client.request("tools/list")
        names = tool_names(listed)
        if "fetch" not in names:
            raise RuntimeError("fetch_tool_missing")

        response = client.request(
            "tools/call",
            {
                "name": "fetch",
                "arguments": {
                    "url": FETCH_PROBE_URL,
                    "max_length": 2000,
                    "start_index": 0,
                    "raw": False,
                },
            },
        )
        text = result_text(response)
        if "Model Context Protocol" not in text:
            raise RuntimeError("fetch_result_missing_expected_marker")

        init_result = initialized.get("result", {})
        protocol_version = (
            str(init_result.get("protocolVersion", ""))
            if isinstance(init_result, Mapping)
            else ""
        )
        return {
            "source_tree_version": FETCH_SOURCE_VERSION,
            "published_package_version": published_version,
            "mcp_sdk_pin": FETCH_MCP_SDK_VERSION,
            "protocol_version": protocol_version,
            "listed_tool_count": len(names),
            "listed_tools_digest": digest(sorted(names)),
            "fetch_tool_present": True,
            "fetch_result_digest": digest(response.get("result", {})),
            "fetch_expected_marker_present": True,
            "fetch_probe_url_digest": digest(FETCH_PROBE_URL),
            "internal_network_target_used": False,
            "write_tools_called": False,
        }
    finally:
        client.close()


def parse_http_json(content_type: str, body: str) -> dict[str, Any]:
    stripped = body.strip()
    if "text/event-stream" in content_type:
        payloads: list[str] = []
        for line in stripped.splitlines():
            if line.startswith("data:"):
                payloads.append(line[5:].strip())
        for payload in reversed(payloads):
            try:
                value = json.loads(payload)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                return value
        raise RuntimeError("docs_sse_response_missing_json")
    value = json.loads(stripped)
    if not isinstance(value, dict):
        raise RuntimeError("docs_response_not_object")
    return value


def modern_meta() -> dict[str, Any]:
    return {
        "io.modelcontextprotocol/protocolVersion": MODERN_PROTOCOL_VERSION,
        "io.modelcontextprotocol/clientInfo": {
            "name": "KuuOS Official MCP Docs Compatibility Probe",
            "version": "7.23",
        },
        "io.modelcontextprotocol/clientCapabilities": {},
    }


def http_mcp_request(
    *,
    method: str,
    request_id: int,
    params: Mapping[str, Any],
    tool_name: str | None = None,
) -> dict[str, Any]:
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": dict(params),
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": MODERN_PROTOCOL_VERSION,
        "Mcp-Method": method,
        "User-Agent": "KuuOS-MCP-Compatibility/7.23",
    }
    if tool_name:
        headers["Mcp-Name"] = tool_name

    request = urllib.request.Request(
        DOCS_ENDPOINT,
        data=body,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            response_body = response.read().decode("utf-8", errors="replace")
            content_type = response.headers.get("Content-Type", "")
            result = parse_http_json(content_type, response_body)
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"docs_http_error:{exc.code}:{error_body[:1800]}"
        ) from exc

    if "error" in result:
        raise RuntimeError(
            "docs_rpc_error:"
            + method
            + ":"
            + json.dumps(result["error"], ensure_ascii=False)
        )
    return result


def build_search_arguments(tool: Mapping[str, Any]) -> dict[str, Any]:
    schema = tool.get("inputSchema", {})
    if not isinstance(schema, Mapping):
        return {"query": "MCP tools/list protocol metadata 2026-07-28"}
    properties = schema.get("properties", {})
    if not isinstance(properties, Mapping):
        properties = {}
    required = schema.get("required", [])
    if not isinstance(required, list):
        required = []

    query = "MCP tools/list protocol metadata 2026-07-28"
    arguments: dict[str, Any] = {}
    for name in required:
        name = str(name)
        spec = properties.get(name, {})
        spec = spec if isinstance(spec, Mapping) else {}
        lowered = name.lower()
        if "query" in lowered or "search" in lowered or "term" in lowered:
            arguments[name] = query
        elif spec.get("type") == "integer":
            arguments[name] = 5
        elif spec.get("type") == "boolean":
            arguments[name] = False
        elif isinstance(spec.get("enum"), list) and spec["enum"]:
            arguments[name] = spec["enum"][0]
        else:
            arguments[name] = query

    if not arguments:
        if "query" in properties:
            arguments["query"] = query
        elif "search" in properties:
            arguments["search"] = query
        else:
            arguments["query"] = query
    return arguments


def probe_official_docs() -> dict[str, Any]:
    listed = http_mcp_request(
        method="tools/list",
        request_id=1,
        params={"_meta": modern_meta()},
    )
    result = listed.get("result", {})
    raw_tools = result.get("tools", []) if isinstance(result, Mapping) else []
    if not isinstance(raw_tools, list):
        raise RuntimeError("docs_tools_list_invalid")

    tools = {
        str(tool.get("name")): dict(tool)
        for tool in raw_tools
        if isinstance(tool, Mapping) and tool.get("name")
    }
    if DOCS_TOOL not in tools:
        raise RuntimeError(
            "official_docs_search_tool_missing:"
            + ",".join(sorted(tools))
        )

    arguments = build_search_arguments(tools[DOCS_TOOL])
    called = http_mcp_request(
        method="tools/call",
        request_id=2,
        params={
            "name": DOCS_TOOL,
            "arguments": arguments,
            "_meta": modern_meta(),
        },
        tool_name=DOCS_TOOL,
    )
    text = result_text(called)
    if len(text.strip()) < 40:
        raise RuntimeError("official_docs_search_result_empty")

    return {
        "endpoint": DOCS_ENDPOINT,
        "protocol_version": MODERN_PROTOCOL_VERSION,
        "stateless_request_model": True,
        "initialize_handshake_used": False,
        "listed_tool_count": len(tools),
        "listed_tools_digest": digest(sorted(tools)),
        "search_tool_present": True,
        "search_arguments_digest": digest(arguments),
        "search_result_digest": digest(called.get("result", {})),
        "search_result_nonempty": True,
        "credentials_used": False,
        "write_tools_called": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument(
        "--receipt",
        default="mcp_fetch_docs_compatibility_receipt_v7_23.json",
    )
    args = parser.parse_args()

    root = pathlib.Path(args.repository_root).resolve()
    if not (root / ".git").exists():
        raise RuntimeError("kuuos_repository_root_invalid")

    fetch = probe_fetch(root)
    docs = probe_official_docs()

    receipt = {
        "version": "kuuos_mcp_fetch_docs_compatibility_receipt_v7_23",
        "status": "KUUOS_MCP_FETCH_DOCS_COMPATIBILITY_VERIFIED",
        "upstream": {
            "reference_servers_sha": REFERENCE_SERVERS_SHA,
            "modelcontextprotocol_repository_sha": DOCS_REPOSITORY_SHA,
        },
        "fetch": fetch,
        "official_docs": docs,
        "boundary": {
            "both_surfaces_are_read_only": True,
            "fetch_may_access_internal_networks_in_general": True,
            "probe_accessed_internal_network": False,
            "official_docs_is_current_spec_reference_plane": True,
            "official_docs_is_kuuos_repository_authority": False,
            "fetch_content_is_kuuos_repository_authority": False,
            "external_content_may_replace_exact_local_evidence": False,
            "credentials_persisted": False,
            "source_authority_transferred": False,
        },
    }

    receipt_path = pathlib.Path(args.receipt)
    if not receipt_path.is_absolute():
        receipt_path = root / receipt_path
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
