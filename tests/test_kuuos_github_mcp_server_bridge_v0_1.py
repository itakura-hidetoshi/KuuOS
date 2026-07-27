from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest

from runtime.kuuos_github_mcp_server_bridge_v0_1 import (
    MockGitHubMCPTransport,
    OfficialGitHubMCPStdioClient,
    _is_write_tool,
    _stdio_command,
    build_github_mcp_server_bridge,
)

BASE_SHA = "ecb891a8dc2dc700ed0d888a889a308a4aef6900"
REPOSITORY = "itakura-hidetoshi/KuuOS"


def _tool(name: str, read_only: bool) -> dict[str, object]:
    return {
        "name": name,
        "description": name,
        "inputSchema": {"type": "object"},
        "annotations": {"readOnlyHint": read_only},
    }


class GitHubMCPServerBridgeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.authority = {
            "authority_status": "KUUOS_GITHUB_MCP_AUTHORITY_READY",
            "plan_read_allowed": True,
            "tool_discovery_allowed": True,
            "receipt_write_allowed": True,
            "audit_append_allowed": True,
            "external_action_allowed": False,
            "write_tool_call_allowed": False,
        }
        self.context = {
            "runtime_root": str(self.root),
            "github_mcp_server_bridge_enabled": True,
            "apply_github_mcp_server_bridge": True,
            "execute_external_actions": False,
        }

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write_plan(self, **overrides: object) -> dict[str, object]:
        plan: dict[str, object] = {
            "version": "kuuos_github_mcp_server_bridge_plan_v0_1",
            "mode": "mock",
            "repository_full_name": REPOSITORY,
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
                "tools": ["get_file_contents", "create_pull_request"],
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
        plan.update(overrides)
        (self.root / "github_mcp_server_bridge_plan.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        return plan

    def _transport(self) -> MockGitHubMCPTransport:
        return MockGitHubMCPTransport(
            [
                _tool("get_file_contents", True),
                _tool("create_pull_request", False),
                _tool("merge_pull_request", False),
            ]
        )

    def test_read_only_discovery_and_read_call_apply(self) -> None:
        self._write_plan()
        result = build_github_mcp_server_bridge(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=self._transport(),
        )
        self.assertEqual(result.status, "KUUOS_GITHUB_MCP_BRIDGE_APPLIED")
        self.assertEqual(result.applied_count, 2)
        self.assertEqual(result.blocked_count, 0)
        receipt = json.loads((self.root / "github_mcp_server_bridge_receipt.json").read_text())
        self.assertNotIn("GITHUB_PERSONAL_ACCESS_TOKEN", json.dumps(receipt))

    def test_read_only_blocks_write_tool(self) -> None:
        plan = self._write_plan()
        plan["operations"] = [
            {
                "kind": "call_tool",
                "tool": "create_pull_request",
                "arguments": {
                    "owner": "itakura-hidetoshi",
                    "repo": "KuuOS",
                    "base": "main",
                    "head": "integration/test",
                    "title": "test",
                },
                "approved": True,
                "expected_base_sha": BASE_SHA,
            }
        ]
        (self.root / "github_mcp_server_bridge_plan.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        result = build_github_mcp_server_bridge(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=self._transport(),
        )
        self.assertEqual(result.status, "KUUOS_GITHUB_MCP_BRIDGE_PARTIAL")
        self.assertIn("write_tool_blocked_by_read_only", result.records[0]["blockers"])

    def test_repository_mismatch_fails_closed(self) -> None:
        plan = self._write_plan()
        plan["operations"] = [
            {
                "kind": "call_tool",
                "tool": "get_file_contents",
                "arguments": {"owner": "other", "repo": "repo", "path": "README.md"},
            }
        ]
        (self.root / "github_mcp_server_bridge_plan.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        result = build_github_mcp_server_bridge(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=self._transport(),
        )
        self.assertIn("operation_repository_mismatch", result.records[0]["blockers"])

    def test_write_call_requires_all_gates_and_exact_base(self) -> None:
        plan = self._write_plan(read_only=False, execute_external_actions=True)
        plan["operations"] = [
            {
                "kind": "call_tool",
                "tool": "create_pull_request",
                "arguments": {
                    "owner": "itakura-hidetoshi",
                    "repo": "KuuOS",
                    "base": "main",
                    "head": "integration/test",
                    "title": "test",
                },
                "approved": True,
                "expected_base_sha": BASE_SHA,
            }
        ]
        (self.root / "github_mcp_server_bridge_plan.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        context = dict(self.context, execute_external_actions=True)
        authority = dict(
            self.authority,
            external_action_allowed=True,
            write_tool_call_allowed=True,
        )
        transport = self._transport()
        result = build_github_mcp_server_bridge(
            runtime_context=context,
            authority_packet=authority,
            transport=transport,
        )
        self.assertEqual(result.status, "KUUOS_GITHUB_MCP_BRIDGE_APPLIED")
        self.assertEqual(len(transport.calls), 1)

    def test_write_call_wrong_base_is_blocked(self) -> None:
        plan = self._write_plan(read_only=False, execute_external_actions=True)
        plan["operations"] = [
            {
                "kind": "call_tool",
                "tool": "create_pull_request",
                "arguments": {
                    "owner": "itakura-hidetoshi",
                    "repo": "KuuOS",
                    "base": "main",
                    "head": "integration/test",
                    "title": "test",
                },
                "approved": True,
                "expected_base_sha": "0" * 40,
            }
        ]
        (self.root / "github_mcp_server_bridge_plan.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        result = build_github_mcp_server_bridge(
            runtime_context=dict(self.context, execute_external_actions=True),
            authority_packet=dict(
                self.authority,
                external_action_allowed=True,
                write_tool_call_allowed=True,
            ),
            transport=self._transport(),
        )
        self.assertIn("expected_base_sha_mismatch", result.records[0]["blockers"])

    def test_exact_sha_git_mutation_is_held_in_v0_1(self) -> None:
        plan = self._write_plan(read_only=False, execute_external_actions=True)
        server = dict(plan["server"])
        server["tools"] = ["merge_pull_request"]
        plan["server"] = server
        plan["operations"] = [
            {
                "kind": "call_tool",
                "tool": "merge_pull_request",
                "arguments": {
                    "owner": "itakura-hidetoshi",
                    "repo": "KuuOS",
                    "pull_number": 1,
                },
                "approved": True,
                "expected_base_sha": BASE_SHA,
            }
        ]
        (self.root / "github_mcp_server_bridge_plan.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        result = build_github_mcp_server_bridge(
            runtime_context=dict(self.context, execute_external_actions=True),
            authority_packet=dict(
                self.authority,
                external_action_allowed=True,
                write_tool_call_allowed=True,
            ),
            transport=self._transport(),
        )
        self.assertIn("exact_sha_git_mutation_not_admitted_v0_1", result.records[0]["blockers"])

    def test_unbounded_toolset_is_rejected(self) -> None:
        plan = self._write_plan()
        server = dict(plan["server"])
        server["toolsets"] = ["all"]
        plan["server"] = server
        (self.root / "github_mcp_server_bridge_plan.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        result = build_github_mcp_server_bridge(
            runtime_context=self.context,
            authority_packet=self.authority,
            transport=self._transport(),
        )
        self.assertEqual(result.status, "KUUOS_GITHUB_MCP_BRIDGE_BLOCKED")
        self.assertIn("toolsets_not_bounded", result.blockers)

    def test_stdio_command_is_official_and_bounded(self) -> None:
        plan = self._write_plan()
        command, env = _stdio_command(plan["server"], plan)
        self.assertEqual(command[:4], ["docker", "run", "-i", "--rm"])
        self.assertEqual(command[-1], "ghcr.io/github/github-mcp-server")
        self.assertEqual(env["GITHUB_READ_ONLY"], "1")
        self.assertEqual(env["GITHUB_LOCKDOWN_MODE"], "1")
        self.assertNotIn("all", env["GITHUB_TOOLSETS"].split(","))

    def test_stdio_client_completes_mcp_lifecycle(self) -> None:
        server = self.root / "fake_mcp_server.py"
        server.write_text(
            """import json, sys
for line in sys.stdin:
    message = json.loads(line)
    if 'id' not in message:
        continue
    method = message.get('method')
    if method == 'initialize':
        result = {'protocolVersion': '2025-11-25', 'capabilities': {'tools': {}}, 'serverInfo': {'name': 'fake', 'version': '1'}}
    elif method == 'tools/list':
        result = {'tools': [{'name': 'get_file_contents', 'inputSchema': {'type': 'object'}, 'annotations': {'readOnlyHint': True}}]}
    elif method == 'tools/call':
        result = {'content': [{'type': 'text', 'text': 'ok'}], 'structuredContent': message['params'], 'isError': False}
    else:
        result = {}
    print(json.dumps({'jsonrpc': '2.0', 'id': message['id'], 'result': result}), flush=True)
""",
            encoding="utf-8",
        )
        client = OfficialGitHubMCPStdioClient(
            [sys.executable, "-u", str(server)],
            {},
            timeout_seconds=3,
        )
        try:
            listed = client.list_tools()
            self.assertEqual(listed["result"]["tools"][0]["name"], "get_file_contents")
            called = client.call_tool("get_file_contents", {"owner": "itakura-hidetoshi", "repo": "KuuOS"})
            self.assertFalse(called["result"]["isError"])
        finally:
            client.close()

    def test_write_classification_prefers_annotations(self) -> None:
        self.assertFalse(_is_write_tool("create_report", {"annotations": {"readOnlyHint": True}}))
        self.assertTrue(_is_write_tool("get_data", {"annotations": {"readOnlyHint": False}}))


if __name__ == "__main__":
    unittest.main()
