from __future__ import annotations

import json
import pathlib
import tempfile
import unittest
from typing import Any, Mapping

from runtime.kuuos_github_mcp_live_write_verification_v0_3 import (
    build_github_mcp_live_write_verification,
)

BASE_SHA = "927680b2422cb523c8244b7fa527aea8126e08b4"
REPOSITORY = "itakura-hidetoshi/KuuOS"
TITLE = "KuuOS GitHub MCP live write verification smoke"
BODY = "mock transaction body"


def _tool(name: str, read_only: bool) -> dict[str, object]:
    return {
        "name": name,
        "description": name,
        "inputSchema": {"type": "object"},
        "annotations": {"readOnlyHint": read_only},
    }


class TransactionTransport:
    def __init__(
        self,
        *,
        observed_title: str = TITLE,
        verification_read_only: bool = True,
        write_url: str = "https://github.com/itakura-hidetoshi/KuuOS/issues/77",
    ) -> None:
        self.observed_title = observed_title
        self.verification_read_only = verification_read_only
        self.write_url = write_url
        self.calls: list[dict[str, Any]] = []

    def list_tools(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": [
                    _tool("create_issue", False),
                    _tool("issue_read", self.verification_read_only),
                ]
            },
        }

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        self.calls.append({"name": name, "arguments": dict(arguments)})
        if name == "create_issue":
            payload = {"id": "1001", "url": self.write_url}
        elif name == "issue_read":
            payload = {
                "number": 77,
                "title": self.observed_title,
                "body": BODY,
                "html_url": "https://github.com/itakura-hidetoshi/KuuOS/issues/77",
            }
        else:
            return {"jsonrpc": "2.0", "id": 9, "error": {"message": "unknown"}}
        return {
            "jsonrpc": "2.0",
            "id": len(self.calls) + 1,
            "result": {"content": [{"type": "text", "text": json.dumps(payload)}]},
        }

    def close(self) -> None:
        return None


class GitHubMCPLiveWriteVerificationV03Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.context = {
            "runtime_root": str(self.root),
            "github_mcp_live_write_verification_enabled": True,
            "apply_github_mcp_live_write_verification": True,
            "execute_external_actions": True,
        }
        self.authority = {
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

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _plan(self, **overrides: object) -> dict[str, object]:
        plan: dict[str, object] = {
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
                "tools": ["create_issue", "issue_read"],
            },
            "transactions": [
                {
                    "write": {
                        "kind": "call_tool",
                        "tool": "create_issue",
                        "arguments": {
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
                            {"path": "body", "equals": BODY},
                        ],
                    },
                }
            ],
        }
        plan.update(overrides)
        (self.root / "github_mcp_live_write_verification_plan_v0_3.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        return plan

    def _run(self, transport: TransactionTransport, **kwargs: object):
        return build_github_mcp_live_write_verification(
            runtime_context=kwargs.get("context", self.context),
            authority_packet=kwargs.get("authority", self.authority),
            transport=transport,
        )

    def test_write_then_readback_is_verified(self) -> None:
        self._plan()
        transport = TransactionTransport()
        result = self._run(transport)
        self.assertEqual(result.status, "KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFIED")
        self.assertEqual(result.verified_count, 1)
        self.assertEqual([call["name"] for call in transport.calls], ["create_issue", "issue_read"])
        self.assertEqual(transport.calls[1]["arguments"]["issue_number"], 77)
        self.assertEqual(result.records[0]["observed"]["title"], TITLE)

    def test_observed_mismatch_does_not_closeout(self) -> None:
        self._plan()
        result = self._run(TransactionTransport(observed_title="different"))
        self.assertEqual(result.status, "KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFICATION_PARTIAL")
        self.assertIn("verification_equals_mismatch:1:title", result.records[0]["blockers"])

    def test_verification_tool_must_be_read_only(self) -> None:
        self._plan()
        transport = TransactionTransport(verification_read_only=False)
        result = self._run(transport)
        self.assertIn("verification_tool_must_be_read_only", result.records[0]["blockers"])
        self.assertEqual([call["name"] for call in transport.calls], ["create_issue"])

    def test_verification_repository_scope_is_exact(self) -> None:
        plan = self._plan()
        transaction = dict(plan["transactions"][0])
        verify = dict(transaction["verify"])
        arguments = dict(verify["arguments"])
        arguments["owner"] = "other"
        verify["arguments"] = arguments
        transaction["verify"] = verify
        plan["transactions"] = [transaction]
        (self.root / "github_mcp_live_write_verification_plan_v0_3.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        result = self._run(TransactionTransport())
        self.assertIn("verification_repository_scope_mismatch", result.records[0]["blockers"])

    def test_invalid_write_url_cannot_bind_issue_number(self) -> None:
        self._plan()
        result = self._run(TransactionTransport(write_url="https://github.com/issues/not-a-number"))
        self.assertEqual(result.status, "KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFICATION_PARTIAL")
        self.assertTrue(
            any(blocker.startswith("verification_binding_failed:") for blocker in result.records[0]["blockers"])
        )

    def test_v03_rejects_read_only_plan(self) -> None:
        self._plan(read_only=True)
        transport = TransactionTransport()
        result = self._run(transport)
        self.assertEqual(result.status, "KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFICATION_BLOCKED")
        self.assertIn("live_write_verification_requires_read_only_false", result.blockers)
        self.assertEqual(transport.calls, [])

    def test_reobservation_authority_is_required(self) -> None:
        self._plan()
        authority = dict(self.authority, post_write_reobservation_allowed=False)
        result = self._run(TransactionTransport(), authority=authority)
        self.assertEqual(result.status, "KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFICATION_BLOCKED")
        self.assertIn("post_write_reobservation_not_allowed", result.blockers)


if __name__ == "__main__":
    unittest.main()
