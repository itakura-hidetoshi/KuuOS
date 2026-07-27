from __future__ import annotations

import json
import pathlib
import tempfile
import unittest
from typing import Any, Mapping

from runtime.kuuos_github_mcp_live_canary_v0_4 import (
    AUTHORITY_READY,
    BLOCKED,
    COMPENSATED,
    CONFIRMATION,
    VERIFIED,
    build_github_mcp_live_canary,
)

BASE_SHA = "938081d3bc8b54b1e06d59474d8ada39b60dafd9"
REPOSITORY = "itakura-hidetoshi/KuuOS"


def _response(payload: Mapping[str, Any], *, error: bool = False) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "isError": error,
            "content": [{"type": "text", "text": json.dumps(dict(payload))}],
        },
    }


class StatefulCanaryTransport:
    def __init__(
        self,
        *,
        issue_write_read_only: bool = False,
        corrupt_open: bool = False,
        fail_first_close: bool = False,
        fail_compensation: bool = False,
    ) -> None:
        self.issue_write_read_only = issue_write_read_only
        self.corrupt_open = corrupt_open
        self.fail_first_close = fail_first_close
        self.fail_compensation = fail_compensation
        self.issue: dict[str, Any] | None = None
        self.calls: list[dict[str, Any]] = []
        self.close_attempts = 0

    def list_tools(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": [
                    {
                        "name": "issue_write",
                        "description": "write issue",
                        "inputSchema": {"type": "object"},
                        "annotations": {"readOnlyHint": self.issue_write_read_only},
                    },
                    {
                        "name": "issue_read",
                        "description": "read issue",
                        "inputSchema": {"type": "object"},
                        "annotations": {"readOnlyHint": True},
                    },
                ]
            },
        }

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        args = dict(arguments)
        self.calls.append({"name": name, "arguments": args})
        if name == "issue_write" and args.get("method") == "create":
            self.issue = {
                "number": 1400,
                "title": args["title"],
                "body": args.get("body", ""),
                "state": "open",
                "html_url": "https://github.com/itakura-hidetoshi/KuuOS/issues/1400",
            }
            return _response({"id": "1400", "url": self.issue["html_url"]})
        if name == "issue_write" and args.get("method") == "update":
            self.close_attempts += 1
            if self.fail_first_close and self.close_attempts == 1:
                return _response({"message": "first close failed"}, error=True)
            if self.fail_compensation and self.close_attempts >= 2:
                return _response({"message": "compensation failed"}, error=True)
            assert self.issue is not None
            self.issue["state"] = "closed"
            return _response({"id": "1400", "url": self.issue["html_url"]})
        if name == "issue_read":
            assert self.issue is not None
            observed = dict(self.issue)
            if self.corrupt_open and observed["state"] == "open":
                observed["title"] = "unexpected title"
            return _response(observed)
        return _response({"message": "unknown tool"}, error=True)

    def close(self) -> None:
        return None


class GitHubMCPLiveCanaryV04Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.authority = {
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
        self.context = {
            "runtime_root": str(self.root),
            "github_mcp_live_canary_enabled": True,
            "apply_github_mcp_live_canary": True,
            "execute_external_actions": True,
            "confirmation": CONFIRMATION,
            "repository_full_name": REPOSITORY,
            "base_sha": BASE_SHA,
            "run_identity": "test-1",
            "mode": "mock",
        }

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write_plan(self, **overrides: Any) -> dict[str, Any]:
        plan: dict[str, Any] = {
            "version": "kuuos_github_mcp_live_canary_plan_v0_4",
            "mode": "mock",
            "repository_full_name": REPOSITORY,
            "base_branch": "main",
            "base_sha": BASE_SHA,
            "write_capable": True,
            "read_only": False,
            "lockdown_mode": True,
            "execute_external_actions": True,
            "confirmation": CONFIRMATION,
            "title_prefix": "[KuuOS MCP Canary] reversible",
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
        plan.update(overrides)
        (self.root / "github_mcp_live_canary_plan_v0_4.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        (self.root / "github_mcp_live_canary_authority_v0_4.json").write_text(
            json.dumps(self.authority), encoding="utf-8"
        )
        return plan

    def test_create_verify_close_verify_is_verified(self) -> None:
        self._write_plan()
        transport = StatefulCanaryTransport()
        result = build_github_mcp_live_canary(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=transport,
        )
        self.assertEqual(result.status, VERIFIED)
        self.assertTrue(result.created_verified)
        self.assertTrue(result.closed_verified)
        self.assertEqual(result.issue_number, 1400)
        self.assertEqual(
            [call["name"] for call in transport.calls],
            ["issue_write", "issue_read", "issue_write", "issue_read"],
        )
        receipt = json.loads(
            (self.root / "github_mcp_live_canary_receipt_v0_4.json").read_text()
        )
        self.assertNotIn("GITHUB_PERSONAL_ACCESS_TOKEN", json.dumps(receipt))

    def test_runtime_confirmation_is_required(self) -> None:
        self._write_plan()
        result = build_github_mcp_live_canary(
            runtime_context=dict(self.context, confirmation="wrong"),
            authority_packet=self.authority,
            transport=StatefulCanaryTransport(),
        )
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("runtime_confirmation_invalid", result.blockers)

    def test_plan_confirmation_is_required(self) -> None:
        self._write_plan(confirmation="wrong")
        result = build_github_mcp_live_canary(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=StatefulCanaryTransport(),
        )
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("plan_confirmation_invalid", result.blockers)

    def test_official_image_must_be_pinned(self) -> None:
        plan = self._write_plan()
        plan["server"]["image"] = "ghcr.io/github/github-mcp-server:latest"
        (self.root / "github_mcp_live_canary_plan_v0_4.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        result = build_github_mcp_live_canary(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=StatefulCanaryTransport(),
        )
        self.assertIn("official_server_image_not_pinned", result.blockers)

    def test_issue_write_must_be_write_capable(self) -> None:
        self._write_plan()
        result = build_github_mcp_live_canary(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=StatefulCanaryTransport(issue_write_read_only=True),
        )
        self.assertIn("issue_write_not_classified_write", result.blockers)

    def test_open_observation_mismatch_is_compensated(self) -> None:
        self._write_plan()
        transport = StatefulCanaryTransport(corrupt_open=True)
        result = build_github_mcp_live_canary(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=transport,
        )
        self.assertEqual(result.status, COMPENSATED)
        self.assertTrue(result.compensation_attempted)
        self.assertTrue(result.compensation_closed)
        self.assertEqual(transport.issue["state"], "closed")

    def test_failed_primary_close_is_compensated(self) -> None:
        self._write_plan()
        transport = StatefulCanaryTransport(fail_first_close=True)
        result = build_github_mcp_live_canary(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=transport,
        )
        self.assertEqual(result.status, COMPENSATED)
        self.assertEqual(transport.close_attempts, 2)
        self.assertTrue(result.compensation_closed)

    def test_failed_compensation_remains_blocked(self) -> None:
        self._write_plan()
        transport = StatefulCanaryTransport(
            fail_first_close=True,
            fail_compensation=True,
        )
        result = build_github_mcp_live_canary(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=transport,
        )
        self.assertEqual(result.status, BLOCKED)
        self.assertFalse(result.compensation_closed)


if __name__ == "__main__":
    unittest.main()
