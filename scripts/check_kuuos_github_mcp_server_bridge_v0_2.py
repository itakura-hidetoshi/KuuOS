#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import tempfile

from runtime.kuuos_github_mcp_server_bridge_v0_1 import MockGitHubMCPTransport
from runtime.kuuos_github_mcp_server_bridge_v0_2 import build_github_mcp_write_bridge

BASE_SHA = "4a49adf52a3918ce580ed670e0ff022f2b542a54"
HEAD_SHA = "e7094eda32abcf0cbbce626fc4394a9976971cd0"
REPOSITORY = "itakura-hidetoshi/KuuOS"


def _tool(name: str, read_only: bool) -> dict[str, object]:
    return {
        "name": name,
        "description": name,
        "inputSchema": {"type": "object"},
        "annotations": {"readOnlyHint": read_only},
    }


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        plan = {
            "version": "kuuos_github_mcp_server_bridge_plan_v0_2",
            "mode": "mock",
            "repository_full_name": REPOSITORY,
            "base_branch": "main",
            "base_sha": BASE_SHA,
            "write_capable": True,
            "read_only": False,
            "lockdown_mode": True,
            "execute_external_actions": True,
            "server": {
                "kind": "official_github_mcp_server",
                "launcher": "docker",
                "image": "ghcr.io/github/github-mcp-server",
                "token_env": "GITHUB_PERSONAL_ACCESS_TOKEN",
                "toolsets": ["context", "repos", "issues", "pull_requests"],
                "tools": ["issue_read", "create_issue"],
            },
            "operations": [
                {"kind": "list_tools"},
                {
                    "kind": "call_tool",
                    "tool": "create_issue",
                    "arguments": {
                        "owner": "itakura-hidetoshi",
                        "repo": "KuuOS",
                        "title": "mock write-capable check",
                    },
                    "approved": True,
                    "expected_base_sha": BASE_SHA,
                },
                {
                    "kind": "exact_git_action",
                    "approved": True,
                    "expected_base_sha": BASE_SHA,
                    "action": {
                        "kind": "merge_pr",
                        "repository_full_name": REPOSITORY,
                        "base_branch": "main",
                        "pr_number": 1347,
                        "merge_method": "merge",
                        "expected_base_sha": BASE_SHA,
                        "expected_head_sha": HEAD_SHA,
                    },
                },
            ],
        }
        authority = {
            "authority_status": "KUUOS_GITHUB_MCP_WRITE_AUTHORITY_READY",
            "plan_read_allowed": True,
            "tool_discovery_allowed": True,
            "receipt_write_allowed": True,
            "audit_append_allowed": True,
            "external_action_allowed": True,
            "mcp_write_tool_call_allowed": True,
            "exact_git_delegation_allowed": True,
        }
        (root / "github_mcp_server_bridge_plan_v0_2.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        transport = MockGitHubMCPTransport(
            [_tool("issue_read", True), _tool("create_issue", False)]
        )
        result = build_github_mcp_write_bridge(
            runtime_context={
                "runtime_root": str(root),
                "github_mcp_server_bridge_enabled": True,
                "apply_github_mcp_server_bridge": True,
                "execute_external_actions": True,
            },
            authority_packet=authority,
            transport=transport,
        )
        assert result.status == "KUUOS_GITHUB_MCP_WRITE_BRIDGE_APPLIED", result
        assert result.direct_applied_count == 1, result
        assert result.delegated_applied_count == 1, result
        assert result.blocked_count == 0, result
        assert len(transport.calls) == 1, transport.calls
        assert result.records[1]["execution_path"] == "official_mcp", result.records
        assert result.records[2]["execution_path"] == "exact_sha_rest_delegate", result.records
        receipt_text = (root / "github_mcp_server_bridge_receipt_v0_2.json").read_text()
        assert "GITHUB_PERSONAL_ACCESS_TOKEN" not in receipt_text
        assert (root / "github_mcp_server_bridge_audit_v0_2.jsonl").is_file()
        assert (root / "github_tool_bridge_plan.json").is_file()
    print("PASS: KuuOS GitHub MCP Server write-capable bridge v0.2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
