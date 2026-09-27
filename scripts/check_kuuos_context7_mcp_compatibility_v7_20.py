#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import selectors
import subprocess
import time
from typing import Any, Mapping, Sequence

PROTOCOL_VERSION = "2025-11-25"
CONTEXT7_VERSION = "4.1.1"
UPSTREAM_SHA = "e275a848a420e0d11c2822f61201ee005bfd1133"

REQUIRED_TOOLS = {"resolve-library-id", "query-docs"}
LIBRARY_ID = re.compile(r"/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+")


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


class MCPClient:
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
            env={
                **os.environ,
                "NO_COLOR": "1",
            },
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
                    raise TimeoutError(f"context7_mcp_timeout:{method}")
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
                        "context7_mcp_closed:"
                        + str(self.process.poll())
                        + ":"
                        + stderr[-1600:]
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
                            "context7_rpc_error:"
                            + method
                            + ":"
                            + json.dumps(
                                message["error"],
                                ensure_ascii=False,
                            )[:1800]
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


def tool_map(response: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    result = response.get("result", {})
    if not isinstance(result, Mapping):
        return {}
    raw = result.get("tools", [])
    if not isinstance(raw, list):
        return {}
    return {
        str(item["name"]): dict(item)
        for item in raw
        if isinstance(item, Mapping) and item.get("name")
    }


def call_tool(
    client: MCPClient,
    name: str,
    arguments: Mapping[str, Any],
) -> dict[str, Any]:
    response = client.request(
        "tools/call",
        {"name": name, "arguments": dict(arguments)},
    )
    result = response.get("result", {})
    if isinstance(result, Mapping) and result.get("isError") is True:
        raise RuntimeError(
            "context7_tool_error:"
            + name
            + ":"
            + json.dumps(result, ensure_ascii=False)[:2200]
        )
    return response


def textual_payload(response: Mapping[str, Any]) -> str:
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


def package_version(root: pathlib.Path) -> str:
    completed = subprocess.run(
        [
            "npx",
            "-y",
            f"@upstash/context7-mcp@{CONTEXT7_VERSION}",
            "--help",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "context7_package_startup_failed:"
            + (completed.stderr or completed.stdout)[-1000:]
        )
    return CONTEXT7_VERSION


def live_probe(root: pathlib.Path) -> dict[str, Any]:
    command = [
        "npx",
        "-y",
        f"@upstash/context7-mcp@{CONTEXT7_VERSION}",
    ]
    client = MCPClient(command, cwd=root)
    try:
        initialized = client.request(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {
                    "name": "KuuOS Context7 MCP Compatibility Probe",
                    "version": "7.20",
                },
            },
        )
        client.notify("notifications/initialized")

        listed = client.request("tools/list")
        tools = tool_map(listed)
        missing = sorted(REQUIRED_TOOLS.difference(tools))
        if missing:
            raise RuntimeError(
                "context7_required_tools_missing:" + ",".join(missing)
            )

        resolved = call_tool(
            client,
            "resolve-library-id",
            {
                "libraryName": "Model Context Protocol",
                "query": (
                    "Find the current official Model Context Protocol "
                    "SDK/documentation project for MCP client and server development."
                ),
            },
        )
        resolved_text = textual_payload(resolved)
        ids = LIBRARY_ID.findall(resolved_text)
        if not ids:
            raise RuntimeError("context7_library_resolution_empty")
        library_id = ids[0]

        docs = call_tool(
            client,
            "query-docs",
            {
                "libraryId": library_id,
                "query": (
                    "How does the current MCP SDK initialize a client/server "
                    "session and list or call tools? Return relevant current API "
                    "documentation or examples."
                ),
            },
        )
        docs_text = textual_payload(docs)
        if len(docs_text.strip()) < 40:
            raise RuntimeError("context7_query_docs_empty")

        init_result = initialized.get("result", {})
        return {
            "protocol_version": (
                str(init_result.get("protocolVersion", ""))
                if isinstance(init_result, Mapping)
                else ""
            ),
            "listed_tool_count": len(tools),
            "listed_tools_digest": digest(sorted(tools)),
            "required_tools_present": True,
            "resolved_library_id_digest": digest(library_id),
            "resolved_result_digest": digest(resolved.get("result", {})),
            "query_docs_result_digest": digest(docs.get("result", {})),
            "query_docs_nonempty": True,
            "api_key_used": False,
            "write_tools_called": False,
        }
    finally:
        client.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument(
        "--receipt",
        default="context7_mcp_compatibility_receipt_v7_20.json",
    )
    args = parser.parse_args()

    root = pathlib.Path(args.repository_root).resolve()
    if not (root / ".git").exists():
        raise RuntimeError("kuuos_repository_root_invalid")

    version = package_version(root)
    result = live_probe(root)

    receipt = {
        "version": "kuuos_context7_mcp_compatibility_receipt_v7_20",
        "status": "KUUOS_CONTEXT7_MCP_COMPATIBILITY_VERIFIED",
        "context7": {
            "package_version": version,
            "upstream_master_sha": UPSTREAM_SHA,
            "remote_endpoint_documented": "https://mcp.context7.com/mcp",
            "local_stdio_probe_used": True,
        },
        "probe": result,
        "boundary": {
            "context7_is_repository_authority": False,
            "context7_is_lean_theorem_authority": False,
            "context7_is_exact_head_authority": False,
            "repository_local_code_outranks_context7_for_kuuos_behavior": True,
            "pinned_toolchain_outranks_context7_for_exact_lean_behavior": True,
            "documentation_can_inform_repairs": True,
            "documentation_may_replace_exact_local_evidence": False,
            "credentials_persisted": False,
            "source_authority_transferred": False,
        },
    }

    receipt_path = pathlib.Path(args.receipt)
    if not receipt_path.is_absolute():
        receipt_path = root / receipt_path
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
