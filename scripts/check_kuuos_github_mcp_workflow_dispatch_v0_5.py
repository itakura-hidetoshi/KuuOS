#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import tempfile
from typing import Any, Mapping

from runtime.kuuos_github_mcp_workflow_dispatch_v0_5 import (
    AUTHORITY_READY,
    CONFIRMATION,
    VERIFIED,
    build_github_mcp_workflow_dispatch,
)

BASE_SHA = "f3eccd858acfda130554d552e4dd049a8fa34cd0"
NONCE = "dispatch-v05-check-001"
WORKFLOW_ID = "kuuos-github-mcp-live-canary-v0-4.yml"


class DispatchMockTransport:
    def __init__(self) -> None:
        self.list_calls = 0
        self.calls: list[dict[str, Any]] = []

    def list_tools(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": [
                    {
                        "name": "actions_run_trigger",
                        "inputSchema": {"type": "object"},
                        "annotations": {"readOnlyHint": False, "destructiveHint": True},
                    },
                    {
                        "name": "actions_list",
                        "inputSchema": {"type": "object"},
                        "annotations": {"readOnlyHint": True},
                    },
                ]
            },
        }

    @staticmethod
    def _response(payload: Any) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "isError": False,
                "content": [{"type": "text", "text": json.dumps(payload)}],
            },
        }

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        args = dict(arguments)
        self.calls.append({"name": name, "arguments": args})
        if name == "actions_list":
            self.list_calls += 1
            runs: list[dict[str, Any]] = []
            if self.list_calls > 1:
                runs.append(
                    {
                        "id": 250,
                        "event": "workflow_dispatch",
                        "head_branch": "main",
                        "head_sha": BASE_SHA,
                        "display_title": f"GitHub MCP live canary v0.4 · {NONCE}",
                        "status": "queued",
                        "html_url": "https://github.com/itakura-hidetoshi/KuuOS/actions/runs/250",
                    }
                )
            return self._response({"total_count": len(runs), "workflow_runs": runs})
        if name == "actions_run_trigger":
            return self._response(
                {
                    "message": "Workflow run has been queued",
                    "workflow_type": "workflow_file",
                    "workflow_id": WORKFLOW_ID,
                    "ref": "main",
                    "inputs": args.get("inputs", {}),
                    "status": "204 No Content",
                    "status_code": 204,
                }
            )
        raise RuntimeError(f"unexpected_tool:{name}")

    def close(self) -> None:
        return None


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        plan = {
            "version": "kuuos_github_mcp_workflow_dispatch_plan_v0_5",
            "mode": "mock",
            "repository_full_name": "itakura-hidetoshi/KuuOS",
            "base_branch": "main",
            "base_sha": BASE_SHA,
            "write_capable": True,
            "read_only": False,
            "lockdown_mode": True,
            "execute_external_actions": True,
            "confirmation": CONFIRMATION,
            "server": {
                "kind": "official_github_mcp_server",
                "launcher": "docker",
                "image": "ghcr.io/github/github-mcp-server:v1.0.5",
                "token_env": "GITHUB_PERSONAL_ACCESS_TOKEN",
                "toolsets": ["actions"],
                "tools": ["actions_run_trigger", "actions_list"],
            },
            "target": {
                "workflow_id": WORKFLOW_ID,
                "ref": "main",
                "expected_head_sha": BASE_SHA,
                "dispatch_nonce": NONCE,
                "inputs": {
                    "confirmation": "RUN_KUUOS_GITHUB_MCP_LIVE_CANARY",
                    "server_image": "ghcr.io/github/github-mcp-server:v1.0.5",
                    "dispatch_nonce": NONCE,
                },
            },
        }
        authority = {
            "authority_status": AUTHORITY_READY,
            "plan_read_allowed": True,
            "tool_discovery_allowed": True,
            "external_action_allowed": True,
            "workflow_dispatch_allowed": True,
            "run_reobservation_allowed": True,
            "mismatched_run_cancel_allowed": True,
            "receipt_write_allowed": True,
            "audit_append_allowed": True,
        }
        (root / "github_mcp_workflow_dispatch_plan_v0_5.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        (root / "github_mcp_workflow_dispatch_authority_v0_5.json").write_text(
            json.dumps(authority), encoding="utf-8"
        )
        transport = DispatchMockTransport()
        result = build_github_mcp_workflow_dispatch(
            runtime_context={
                "runtime_root": str(root),
                "github_mcp_workflow_dispatch_enabled": True,
                "apply_github_mcp_workflow_dispatch": True,
                "execute_external_actions": True,
                "confirmation": CONFIRMATION,
                "repository_full_name": "itakura-hidetoshi/KuuOS",
                "base_sha": BASE_SHA,
                "poll_attempts": 2,
                "poll_interval_seconds": 0,
                "mode": "mock",
            },
            authority_packet=authority,
            transport=transport,
        )
        assert result.status == VERIFIED, result.to_dict()
        assert result.dispatch_accepted is True
        assert result.run_observed is True
        assert result.run_id == 250
        assert result.run_head_sha == BASE_SHA
        assert [call["name"] for call in transport.calls] == [
            "actions_list",
            "actions_run_trigger",
            "actions_list",
        ]
        receipt = json.loads(
            (root / "github_mcp_workflow_dispatch_receipt_v0_5.json").read_text()
        )
        assert receipt["status"] == VERIFIED
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
