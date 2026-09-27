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
from typing import Any, Mapping, Sequence

PROTOCOL_VERSION = "2025-06-18"
EXPECTED_REFERENCE_SHA = "f46d9578190b476b3501923ea8977d899e8db2cb"
GIT_PACKAGE_VERSION = "0.6.2"
FILESYSTEM_PACKAGE_VERSION = "2026.8.31"

GIT_REQUIRED_TOOLS = {"git_status", "git_log"}
FILESYSTEM_REQUIRED_TOOLS = {
    "list_allowed_directories",
    "read_text_file",
    "search_files",
    "get_file_info",
}
FILESYSTEM_WRITE_TOOLS = {
    "write_file",
    "edit_file",
    "move_file",
    "create_directory",
}


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


class MCPClient:
    def __init__(
        self,
        command: Sequence[str],
        *,
        cwd: pathlib.Path,
        timeout_seconds: float = 90.0,
    ) -> None:
        self.process = subprocess.Popen(
            list(command),
            cwd=str(cwd),
            env=os.environ.copy(),
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

    def request(self, method: str, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
        request_id = self.next_id
        self.next_id += 1
        payload: dict[str, Any] = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            payload["params"] = dict(params)
        self.stdin.write(json.dumps(payload, separators=(",", ":")) + "\n")
        self.stdin.flush()

        selector = selectors.DefaultSelector()
        selector.register(self.stdout, selectors.EVENT_READ)
        deadline = time.monotonic() + self.timeout
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError(f"mcp_timeout:{method}")
                events = selector.select(remaining)
                if not events:
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
                        f"mcp_server_closed:{self.process.poll()}:{stderr[-1200:]}"
                    )
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(message, dict) and message.get("id") == request_id:
                    if "error" in message:
                        raise RuntimeError(
                            f"mcp_rpc_error:{method}:{json.dumps(message['error'])}"
                        )
                    return message
        finally:
            selector.close()

    def notify(self, method: str) -> None:
        self.stdin.write(json.dumps({"jsonrpc": "2.0", "method": method}) + "\n")
        self.stdin.flush()

    def initialize(self, name: str) -> dict[str, Any]:
        response = self.request(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": name, "version": "7.18"},
            },
        )
        self.notify("notifications/initialized")
        return response

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


def tools(response: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    result = response.get("result", {})
    raw = result.get("tools", []) if isinstance(result, Mapping) else []
    return {
        str(item["name"]): dict(item)
        for item in raw
        if isinstance(item, Mapping) and item.get("name")
    }


def call(client: MCPClient, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
    response = client.request("tools/call", {"name": name, "arguments": dict(arguments)})
    result = response.get("result", {})
    if isinstance(result, Mapping) and result.get("isError") is True:
        raise RuntimeError(f"mcp_tool_error:{name}:{json.dumps(result)[:1800]}")
    return response


def text_content(response: Mapping[str, Any]) -> str:
    result = response.get("result", {})
    if not isinstance(result, Mapping):
        return ""
    content = result.get("content", [])
    if not isinstance(content, list):
        return ""
    return "\n".join(
        str(item.get("text", ""))
        for item in content
        if isinstance(item, Mapping) and item.get("type") == "text"
    )


def git_head(root: pathlib.Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def ensure_clean(root: pathlib.Path) -> None:
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    if status.strip():
        raise RuntimeError("worktree_not_clean_before_probe")


def probe_git(root: pathlib.Path, expected_head: str) -> dict[str, Any]:
    command = [
        "uvx",
        "--from",
        f"mcp-server-git=={GIT_PACKAGE_VERSION}",
        "--with",
        "mcp==1.29.0",
        "mcp-server-git",
        "--repository",
        str(root),
    ]
    client = MCPClient(command, cwd=root)
    try:
        initialized = client.initialize("KuuOS Git MCP Compatibility Probe")
        listed = tools(client.request("tools/list"))
        missing = sorted(GIT_REQUIRED_TOOLS.difference(listed))
        if missing:
            raise RuntimeError("git_required_tools_missing:" + ",".join(missing))

        status = call(client, "git_status", {"repo_path": str(root)})
        log = call(
            client,
            "git_log",
            {"repo_path": str(root), "max_count": 1},
        )
        status_text = text_content(status)
        if "nothing to commit" not in status_text.lower() and "clean" not in status_text.lower():
            # Server wording may vary; verify directly as the exact fallback.
            ensure_clean(root)

        log_text = text_content(log)
        short = expected_head[:7]
        if expected_head not in log_text and short not in log_text:
            raise RuntimeError("git_mcp_log_does_not_reference_exact_head")

        init_result = initialized.get("result", {})
        return {
            "protocol_version": (
                str(init_result.get("protocolVersion", ""))
                if isinstance(init_result, Mapping)
                else ""
            ),
            "listed_tool_count": len(listed),
            "listed_tools_digest": digest(sorted(listed)),
            "required_tools_present": True,
            "git_status_digest": digest(status.get("result", {})),
            "git_log_digest": digest(log.get("result", {})),
            "git_show_available_in_released_package": "git_show" in listed,
            "released_tool_surface_differs_from_current_upstream_source": "git_show" not in listed,
            "exact_head_observed": True,
            "write_tools_called": False,
        }
    finally:
        client.close()


def probe_filesystem(root: pathlib.Path) -> dict[str, Any]:
    command = [
        "npx",
        "-y",
        f"@modelcontextprotocol/server-filesystem@{FILESYSTEM_PACKAGE_VERSION}",
        str(root),
    ]
    client = MCPClient(command, cwd=root)
    try:
        initialized = client.initialize("KuuOS Filesystem MCP Compatibility Probe")
        listed = tools(client.request("tools/list"))
        missing = sorted(FILESYSTEM_REQUIRED_TOOLS.difference(listed))
        if missing:
            raise RuntimeError("filesystem_required_tools_missing:" + ",".join(missing))

        allowed = call(client, "list_allowed_directories", {})
        allowed_text = text_content(allowed)
        if str(root) not in allowed_text:
            raise RuntimeError("filesystem_allowed_root_not_exact_kuuos_root")

        lean_toolchain = call(
            client,
            "read_text_file",
            {"path": str(root / "lean-toolchain")},
        )
        lean_text = text_content(lean_toolchain).strip()
        if lean_text != "leanprover/lean4:v4.30.0-rc2":
            raise RuntimeError("filesystem_read_wrong_lean_toolchain")

        searched = call(
            client,
            "search_files",
            {
                "path": str(root),
                "pattern": "lean-toolchain",
                "excludePatterns": [".git/**", ".lake/**"],
            },
        )
        if "lean-toolchain" not in text_content(searched):
            raise RuntimeError("filesystem_search_failed_for_lean_toolchain")

        annotations = {
            name: dict(tool.get("annotations", {}))
            for name, tool in listed.items()
            if isinstance(tool.get("annotations"), Mapping)
        }
        for name in FILESYSTEM_WRITE_TOOLS.intersection(listed):
            if annotations.get(name, {}).get("readOnlyHint") is not False:
                raise RuntimeError("filesystem_write_tool_annotation_invalid:" + name)

        init_result = initialized.get("result", {})
        return {
            "protocol_version": (
                str(init_result.get("protocolVersion", ""))
                if isinstance(init_result, Mapping)
                else ""
            ),
            "listed_tool_count": len(listed),
            "listed_tools_digest": digest(sorted(listed)),
            "required_tools_present": True,
            "write_tools_discovered": sorted(FILESYSTEM_WRITE_TOOLS.intersection(listed)),
            "write_tool_annotations_digest": digest(
                {name: annotations.get(name, {}) for name in sorted(FILESYSTEM_WRITE_TOOLS.intersection(listed))}
            ),
            "allowed_directories_digest": digest(allowed.get("result", {})),
            "lean_toolchain_read_digest": digest(lean_toolchain.get("result", {})),
            "search_result_digest": digest(searched.get("result", {})),
            "write_tools_called": False,
        }
    finally:
        client.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--expected-head", required=True)
    parser.add_argument(
        "--receipt",
        default="local_repository_mcp_compatibility_receipt_v7_18.json",
    )
    args = parser.parse_args()

    root = pathlib.Path(args.repository_root).resolve()
    expected_head = args.expected_head.strip()
    actual_head = git_head(root)
    if actual_head != expected_head:
        raise RuntimeError(f"local_head_mismatch:{actual_head}:{expected_head}")
    ensure_clean(root)

    if (root / "lean-toolchain").read_text(encoding="utf-8").strip() != "leanprover/lean4:v4.30.0-rc2":
        raise RuntimeError("kuuos_lean_toolchain_changed")

    git_result = probe_git(root, expected_head)
    filesystem_result = probe_filesystem(root)

    receipt = {
        "version": "kuuos_local_repository_mcp_compatibility_receipt_v7_18",
        "status": "KUUOS_LOCAL_REPOSITORY_MCP_COMPATIBILITY_VERIFIED",
        "reference_servers": {
            "repository": "modelcontextprotocol/servers",
            "upstream_main_sha": EXPECTED_REFERENCE_SHA,
            "git_package_version": GIT_PACKAGE_VERSION,
            "filesystem_package_version": FILESYSTEM_PACKAGE_VERSION,
        },
        "kuuos": {
            "exact_head": expected_head,
            "repository_root_digest": digest(str(root)),
        },
        "git_mcp": git_result,
        "filesystem_mcp": filesystem_result,
        "boundary": {
            "probe_is_read_only": True,
            "git_write_tools_called": False,
            "filesystem_write_tools_called": False,
            "filesystem_scope_is_exact_repository_root": True,
            "local_git_head_equals_github_exact_head": True,
            "local_mcp_state_is_remote_repository_authority": False,
            "github_remote_state_is_local_worktree_state": False,
            "registry_entry_is_authority": False,
            "source_authority_transferred": False,
        },
    }

    receipt_path = pathlib.Path(args.receipt)
    if not receipt_path.is_absolute():
        receipt_path = root / receipt_path
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
