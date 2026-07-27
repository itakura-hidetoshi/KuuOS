from __future__ import annotations

import json
import pathlib
import tempfile
import unittest

from runtime.kuuos_github_mcp_server_bridge_v0_1 import _stdio_command
from runtime.kuuos_github_mcp_server_bridge_v0_2 import (
    MockGitHubMCPTransport,
    build_github_mcp_write_bridge,
)

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


class GitHubMCPServerBridgeV02Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.authority = {
            "authority_status": "KUUOS_GITHUB_MCP_WRITE_AUTHORITY_READY",
            "plan_read_allowed": True,
            "tool_discovery_allowed": True,
            "receipt_write_allowed": True,
            "audit_append_allowed": True,
            "external_action_allowed": True,
            "mcp_write_tool_call_allowed": True,
            "exact_git_delegation_allowed": True,
        }
        self.context = {
            "runtime_root": str(self.root),
            "github_mcp_server_bridge_enabled": True,
            "apply_github_mcp_server_bridge": True,
            "execute_external_actions": True,
        }

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write_plan(self, **overrides: object) -> dict[str, object]:
        plan: dict[str, object] = {
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
                        "title": "Write-capable bridge smoke test",
                        "body": "mock only",
                    },
                    "approved": True,
                    "expected_base_sha": BASE_SHA,
                },
            ],
        }
        plan.update(overrides)
        (self.root / "github_mcp_server_bridge_plan_v0_2.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        return plan

    def _transport(self, extra: list[dict[str, object]] | None = None) -> MockGitHubMCPTransport:
        tools = [_tool("issue_read", True), _tool("create_issue", False)]
        tools.extend(extra or [])
        return MockGitHubMCPTransport(tools)

    def test_direct_mcp_write_applies_when_all_authority_gates_pass(self) -> None:
        self._write_plan()
        transport = self._transport()
        result = build_github_mcp_write_bridge(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=transport,
        )
        self.assertEqual(result.status, "KUUOS_GITHUB_MCP_WRITE_BRIDGE_APPLIED")
        self.assertEqual(result.direct_applied_count, 1)
        self.assertEqual(result.delegated_applied_count, 0)
        self.assertEqual(len(transport.calls), 1)
        self.assertEqual(transport.calls[0]["name"], "create_issue")
        receipt = json.loads(
            (self.root / "github_mcp_server_bridge_receipt_v0_2.json").read_text()
        )
        self.assertNotIn("GITHUB_PERSONAL_ACCESS_TOKEN", json.dumps(receipt))

    def test_direct_write_requires_runtime_gate(self) -> None:
        self._write_plan()
        result = build_github_mcp_write_bridge(
            runtime_context=dict(self.context, execute_external_actions=False),
            authority_packet=self.authority,
            transport=self._transport(),
        )
        self.assertEqual(result.status, "KUUOS_GITHUB_MCP_WRITE_BRIDGE_PARTIAL")
        self.assertIn(
            "runtime_execute_external_actions_not_true",
            result.records[1]["blockers"],
        )

    def test_repository_mismatch_fails_closed(self) -> None:
        plan = self._write_plan()
        plan["operations"] = [
            {
                "kind": "call_tool",
                "tool": "create_issue",
                "arguments": {
                    "owner": "other",
                    "repo": "repo",
                    "title": "wrong repository",
                },
                "approved": True,
                "expected_base_sha": BASE_SHA,
            }
        ]
        (self.root / "github_mcp_server_bridge_plan_v0_2.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        result = build_github_mcp_write_bridge(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=self._transport(),
        )
        self.assertIn("operation_repository_mismatch", result.records[0]["blockers"])

    def test_direct_git_object_mutation_requires_exact_action_path(self) -> None:
        plan = self._write_plan()
        server = dict(plan["server"])
        server["tools"] = ["issue_read", "merge_pull_request"]
        plan["server"] = server
        plan["operations"] = [
            {
                "kind": "call_tool",
                "tool": "merge_pull_request",
                "arguments": {
                    "owner": "itakura-hidetoshi",
                    "repo": "KuuOS",
                    "pullNumber": 1347,
                },
                "approved": True,
                "expected_base_sha": BASE_SHA,
            }
        ]
        (self.root / "github_mcp_server_bridge_plan_v0_2.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        result = build_github_mcp_write_bridge(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=self._transport([_tool("merge_pull_request", False)]),
        )
        self.assertIn("exact_git_action_required", result.records[0]["blockers"])

    def test_exact_merge_is_delegated_with_expected_head_sha(self) -> None:
        plan = self._write_plan()
        plan["operations"] = [
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
            }
        ]
        (self.root / "github_mcp_server_bridge_plan_v0_2.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        result = build_github_mcp_write_bridge(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=self._transport(),
        )
        self.assertEqual(result.status, "KUUOS_GITHUB_MCP_WRITE_BRIDGE_APPLIED")
        self.assertEqual(result.delegated_applied_count, 1)
        self.assertEqual(result.records[0]["execution_path"], "exact_sha_rest_delegate")
        delegated_plan = json.loads(
            (self.root / "github_tool_bridge_plan.json").read_text()
        )
        self.assertEqual(delegated_plan["actions"][0]["expected_head_sha"], HEAD_SHA)

    def test_exact_action_wrong_base_is_blocked_before_delegation(self) -> None:
        plan = self._write_plan()
        plan["operations"] = [
            {
                "kind": "exact_git_action",
                "approved": True,
                "expected_base_sha": "0" * 40,
                "action": {
                    "kind": "create_branch",
                    "repository_full_name": REPOSITORY,
                    "base_branch": "main",
                    "branch": "integration/test",
                    "sha": BASE_SHA,
                },
            }
        ]
        (self.root / "github_mcp_server_bridge_plan_v0_2.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        result = build_github_mcp_write_bridge(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=self._transport(),
        )
        self.assertIn("expected_base_sha_mismatch", result.records[0]["blockers"])
        self.assertFalse((self.root / "github_tool_bridge_plan.json").exists())

    def test_write_capable_plan_rejects_read_only_mode(self) -> None:
        self._write_plan(read_only=True)
        result = build_github_mcp_write_bridge(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=self._transport(),
        )
        self.assertEqual(result.status, "KUUOS_GITHUB_MCP_WRITE_BRIDGE_BLOCKED")
        self.assertIn("write_capable_plan_requires_read_only_false", result.blockers)

    def test_stdio_environment_exposes_write_tools(self) -> None:
        plan = self._write_plan()
        command, env = _stdio_command(plan["server"], plan)
        self.assertEqual(command[:4], ["docker", "run", "-i", "--rm"])
        self.assertEqual(env["GITHUB_READ_ONLY"], "0")
        self.assertEqual(env["GITHUB_LOCKDOWN_MODE"], "1")
        self.assertIn("create_issue", env["GITHUB_TOOLS"].split(","))


if __name__ == "__main__":
    unittest.main()
