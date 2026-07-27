#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import tempfile
from typing import Any, Mapping

from runtime.kuuos_github_mcp_live_canary_v0_4 import (
    AUTHORITY_READY,
    CONFIRMATION,
    VERIFIED,
    build_github_mcp_live_canary,
)

BASE_SHA = "938081d3bc8b54b1e06d59474d8ada39b60dafd9"


class CanaryMockTransport:
    def __init__(self) -> None:
        self.issue: dict[str, Any] | None = None
        self.calls: list[dict[str, Any]] = []

    def list_tools(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": [
                    {
                        "name": "issue_write",
                        "inputSchema": {"type": "object"},
                        "annotations": {"readOnlyHint": False},
                    },
                    {
                        "name": "issue_read",
                        "inputSchema": {"type": "object"},
                        "annotations": {"readOnlyHint": True},
                    },
                ]
            },
        }

    @staticmethod
    def _response(payload: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "isError": False,
                "content": [{"type": "text", "text": json.dumps(dict(payload))}],
            },
        }

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        args = dict(arguments)
        self.calls.append({"name": name, "arguments": args})
        if name == "issue_write" and args.get("method") == "create":
            self.issue = {
                "number": 1401,
                "title": args["title"],
                "body": args["body"],
                "state": "open",
                "html_url": "https://github.com/itakura-hidetoshi/KuuOS/issues/1401",
            }
            return self._response({"id": "1401", "url": self.issue["html_url"]})
        if name == "issue_write" and args.get("method") == "update":
            if self.issue is None:
                raise RuntimeError("issue_missing")
            self.issue["state"] = "closed"
            return self._response({"id": "1401", "url": self.issue["html_url"]})
        if name == "issue_read":
            if self.issue is None:
                raise RuntimeError("issue_missing")
            return self._response(self.issue)
        raise RuntimeError(f"unexpected_tool:{name}")

    def close(self) -> None:
        return None


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        plan = {
            "version": "kuuos_github_mcp_live_canary_plan_v0_4",
            "mode": "mock",
            "repository_full_name": "itakura-hidetoshi/KuuOS",
            "base_branch": "main",
            "base_sha": BASE_SHA,
            "write_capable": True,
            "read_only": False,
            "lockdown_mode": True,
            "execute_external_actions": True,
            "confirmation": CONFIRMATION,
            "title_prefix": "[KuuOS MCP Canary] deterministic",
            "body_marker": "KUUOS_GITHUB_MCP_LIVE_CANARY v0.4",
            "server": {
                "kind": "official_github_mcp_server",
                "launcher": "docker",
                "image": "ghcr.io/github/github-mcp-server:v1.0.5",
                "token_env": "GITHUB_PERSONAL_ACCESS_TOKEN",
                "toolsets": ["issues"],
                "tools": ["issue_write", "issue_read"],
            },
        }
        authority = {
            "authority_status": AUTHORITY_READY,
            "plan_read_allowed": True,
            "tool_discovery_allowed": True,
            "external_action_allowed": True,
            "mcp_write_tool_call_allowed": True,
            "post_write_reobservation_allowed": True,
            "compensating_close_allowed": True,
            "receipt_write_allowed": True,
            "audit_append_allowed": True,
        }
        (root / "github_mcp_live_canary_plan_v0_4.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        (root / "github_mcp_live_canary_authority_v0_4.json").write_text(
            json.dumps(authority), encoding="utf-8"
        )
        transport = CanaryMockTransport()
        result = build_github_mcp_live_canary(
            runtime_context={
                "runtime_root": str(root),
                "github_mcp_live_canary_enabled": True,
                "apply_github_mcp_live_canary": True,
                "execute_external_actions": True,
                "confirmation": CONFIRMATION,
                "repository_full_name": "itakura-hidetoshi/KuuOS",
                "base_sha": BASE_SHA,
                "run_identity": "deterministic-check",
                "mode": "mock",
            },
            authority_packet=authority,
            transport=transport,
        )
        assert result.status == VERIFIED, result.to_dict()
        assert result.created_verified is True
        assert result.closed_verified is True
        assert result.compensation_attempted is False
        assert transport.issue is not None and transport.issue["state"] == "closed"
        assert [call["name"] for call in transport.calls] == [
            "issue_write",
            "issue_read",
            "issue_write",
            "issue_read",
        ]
        receipt = json.loads(
            (root / "github_mcp_live_canary_receipt_v0_4.json").read_text()
        )
        assert receipt["status"] == VERIFIED
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
