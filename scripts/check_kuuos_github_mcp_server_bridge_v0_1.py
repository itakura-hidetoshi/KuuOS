#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import tempfile

from runtime.kuuos_github_mcp_server_bridge_v0_1 import (
    MockGitHubMCPTransport,
    build_github_mcp_server_bridge,
)

BASE_SHA = "ecb891a8dc2dc700ed0d888a889a308a4aef6900"


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        plan = {
            "version": "kuuos_github_mcp_server_bridge_plan_v0_1",
            "mode": "mock",
            "repository_full_name": "itakura-hidetoshi/KuuOS",
            "base_branch": "main",
            "base_sha": BASE_SHA,
            "read_only": True,
            "lockdown_mode": True,
            "execute_external_actions": False,
            "server": {
                "kind": "official_github_mcp_server",
                "launcher": "docker",
                "image": "ghcr.io/github/github-mcp-server",
                "token_env": "GITHUB_PERSONAL_ACCESS_TOKEN",
                "toolsets": ["context", "repos", "pull_requests"],
                "tools": ["get_file_contents"],
            },
            "operations": [
                {"kind": "list_tools"},
                {
                    "kind": "call_tool",
                    "tool": "get_file_contents",
                    "arguments": {
                        "owner": "itakura-hidetoshi",
                        "repo": "KuuOS",
                        "path": "README.md",
                        "ref": "main",
                    },
                },
            ],
        }
        (root / "github_mcp_server_bridge_plan.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        transport = MockGitHubMCPTransport(
            [
                {
                    "name": "get_file_contents",
                    "description": "Read repository contents",
                    "inputSchema": {"type": "object"},
                    "annotations": {"readOnlyHint": True},
                }
            ]
        )
        result = build_github_mcp_server_bridge(
            runtime_context={
                "runtime_root": str(root),
                "github_mcp_server_bridge_enabled": True,
                "apply_github_mcp_server_bridge": True,
                "execute_external_actions": False,
            },
            authority_packet={
                "authority_status": "KUUOS_GITHUB_MCP_AUTHORITY_READY",
                "plan_read_allowed": True,
                "tool_discovery_allowed": True,
                "receipt_write_allowed": True,
                "audit_append_allowed": True,
                "external_action_allowed": False,
                "write_tool_call_allowed": False,
            },
            transport=transport,
        )
        if result.status != "KUUOS_GITHUB_MCP_BRIDGE_APPLIED":
            print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
            return 1
        if result.applied_count != 2 or result.blocked_count != 0:
            print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
            return 1
        receipt = json.loads(pathlib.Path(result.receipt_path).read_text(encoding="utf-8"))
        if receipt["repository_full_name"] != "itakura-hidetoshi/KuuOS":
            return 1
        if receipt["read_only"] is not True or receipt["lockdown_mode"] is not True:
            return 1
        print("PASS: KuuOS GitHub MCP Server Bridge v0.1")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
