#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import tempfile
from typing import Any, Mapping

from runtime.kuuos_github_mcp_live_write_verification_v0_3 import (
    build_github_mcp_live_write_verification,
)

BASE_SHA = "927680b2422cb523c8244b7fa527aea8126e08b4"
REPOSITORY = "itakura-hidetoshi/KuuOS"
TITLE = "KuuOS GitHub MCP live write verification smoke"
BODY = "deterministic mock transaction"


def _tool(name: str, read_only: bool) -> dict[str, object]:
    return {
        "name": name,
        "description": name,
        "inputSchema": {"type": "object"},
        "annotations": {"readOnlyHint": read_only},
    }


class DeterministicLiveTransport:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.closed = False

    def list_tools(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {"tools": [_tool("issue_write", False), _tool("issue_read", True)]},
        }

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        self.calls.append({"name": name, "arguments": dict(arguments)})
        if name == "issue_write":
            if arguments.get("method") != "create":
                return {"jsonrpc": "2.0", "id": 2, "error": {"message": "wrong method"}}
            payload = {
                "id": "1001",
                "url": "https://github.com/itakura-hidetoshi/KuuOS/issues/77",
            }
        elif name == "issue_read":
            if int(arguments.get("issue_number", 0)) != 77:
                return {"jsonrpc": "2.0", "id": 3, "error": {"message": "wrong issue"}}
            payload = {
                "number": 77,
                "title": TITLE,
                "body": BODY,
                "html_url": "https://github.com/itakura-hidetoshi/KuuOS/issues/77",
            }
        else:
            return {"jsonrpc": "2.0", "id": 4, "error": {"message": "unknown tool"}}
        return {
            "jsonrpc": "2.0",
            "id": len(self.calls) + 1,
            "result": {"content": [{"type": "text", "text": json.dumps(payload)}]},
        }

    def close(self) -> None:
        self.closed = True


def _plan() -> dict[str, object]:
    return {
        "version": "kuuos_github_mcp_live_write_verification_plan_v0_3",
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
            "toolsets": ["context", "repos", "issues"],
            "tools": ["issue_write", "issue_read"],
        },
        "transactions": [
            {
                "write": {
                    "kind": "call_tool",
                    "tool": "issue_write",
                    "arguments": {
                        "method": "create",
                        "owner": "itakura-hidetoshi",
                        "repo": "KuuOS",
                        "title": TITLE,
                        "body": BODY,
                    },
                    "approved": True,
                    "expected_base_sha": BASE_SHA,
                },
                "verify": {
                    "tool": "issue_read",
                    "arguments": {
                        "method": "get",
                        "owner": "itakura-hidetoshi",
                        "repo": "KuuOS",
                        "issue_number": {"$issue_number_from_write_url": "url"},
                    },
                    "assertions": [
                        {"path": "number", "equals_write_url_issue_number": "url"},
                        {"path": "title", "equals": TITLE},
                        {"path": "body", "contains": "deterministic mock"},
                    ],
                },
            }
        ],
    }


def main() -> int:
    authority = {
        "authority_status": "KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFICATION_AUTHORITY_READY",
        "plan_read_allowed": True,
        "tool_discovery_allowed": True,
        "external_action_allowed": True,
        "mcp_write_tool_call_allowed": True,
        "exact_git_delegation_allowed": True,
        "post_write_reobservation_allowed": True,
        "verification_tool_call_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        (root / "github_mcp_live_write_verification_plan_v0_3.json").write_text(
            json.dumps(_plan()), encoding="utf-8"
        )
        transport = DeterministicLiveTransport()
        result = build_github_mcp_live_write_verification(
            runtime_context={
                "runtime_root": str(root),
                "github_mcp_live_write_verification_enabled": True,
                "apply_github_mcp_live_write_verification": True,
                "execute_external_actions": True,
            },
            authority_packet=authority,
            transport=transport,
        )
        assert result.status == "KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFIED", result.to_dict()
        assert result.verified_count == 1
        assert result.blocked_count == 0
        assert [call["name"] for call in transport.calls] == ["issue_write", "issue_read"]
        assert transport.calls[0]["arguments"]["method"] == "create"
        assert transport.calls[1]["arguments"]["issue_number"] == 77
        receipt = json.loads(
            (root / "github_mcp_live_write_verification_receipt_v0_3.json").read_text()
        )
        assert receipt["records"][0]["status"] == "verified"
        assert receipt["records"][0]["observed"]["number"] == 77
        assert "GITHUB_PERSONAL_ACCESS_TOKEN" not in json.dumps(receipt)
        audit_lines = (
            root / "github_mcp_live_write_verification_audit_v0_3.jsonl"
        ).read_text().splitlines()
        assert len(audit_lines) == 1
    print("PASS: GitHub MCP live write verification v0.3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
