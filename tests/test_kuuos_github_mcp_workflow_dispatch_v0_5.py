from __future__ import annotations

import json
import pathlib
import tempfile
import unittest
from typing import Any, Mapping

from runtime.kuuos_github_mcp_workflow_dispatch_v0_5 import (
    AUTHORITY_READY,
    BLOCKED,
    CONFIRMATION,
    MISMATCH_CANCELLED,
    VERIFIED,
    build_github_mcp_workflow_dispatch,
)

BASE_SHA = "f3eccd858acfda130554d552e4dd049a8fa34cd0"
REPOSITORY = "itakura-hidetoshi/KuuOS"
WORKFLOW_ID = "kuuos-github-mcp-live-canary-v0-4.yml"
NONCE = "dispatch-v05-test-001"


def _response(payload: Any, *, error: bool = False) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "isError": error,
            "content": [{"type": "text", "text": json.dumps(payload)}],
        },
    }


class WorkflowDispatchTransport:
    def __init__(
        self,
        *,
        observed: bool = True,
        wrong_head_sha: bool = False,
        trigger_read_only: bool = False,
        cancel_fails: bool = False,
    ) -> None:
        self.observed = observed
        self.wrong_head_sha = wrong_head_sha
        self.trigger_read_only = trigger_read_only
        self.cancel_fails = cancel_fails
        self.list_calls = 0
        self.calls: list[dict[str, Any]] = []
        self.cancelled = False

    def list_tools(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": [
                    {
                        "name": "actions_run_trigger",
                        "inputSchema": {"type": "object"},
                        "annotations": {"readOnlyHint": self.trigger_read_only, "destructiveHint": True},
                    },
                    {
                        "name": "actions_list",
                        "inputSchema": {"type": "object"},
                        "annotations": {"readOnlyHint": True},
                    },
                ]
            },
        }

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        args = dict(arguments)
        self.calls.append({"name": name, "arguments": args})
        if name == "actions_list":
            self.list_calls += 1
            runs: list[dict[str, Any]] = [
                {
                    "id": 100,
                    "event": "workflow_dispatch",
                    "head_branch": "main",
                    "head_sha": BASE_SHA,
                    "display_title": "old dispatch",
                    "status": "completed",
                    "html_url": "https://github.com/itakura-hidetoshi/KuuOS/actions/runs/100",
                }
            ]
            if self.list_calls > 1 and self.observed:
                runs.insert(
                    0,
                    {
                        "id": 200,
                        "event": "workflow_dispatch",
                        "head_branch": "main",
                        "head_sha": "0" * 40 if self.wrong_head_sha else BASE_SHA,
                        "display_title": f"GitHub MCP live canary v0.4 · {NONCE}",
                        "status": "queued",
                        "html_url": "https://github.com/itakura-hidetoshi/KuuOS/actions/runs/200",
                    },
                )
            return _response({"total_count": len(runs), "workflow_runs": runs})
        if name == "actions_run_trigger" and args.get("method") == "run_workflow":
            return _response(
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
        if name == "actions_run_trigger" and args.get("method") == "cancel_workflow_run":
            if self.cancel_fails:
                return _response({"message": "cancel failed"}, error=True)
            self.cancelled = True
            return _response(
                {
                    "message": "Workflow run has been cancelled",
                    "run_id": 200,
                    "status": "202 Accepted",
                    "status_code": 202,
                }
            )
        return _response({"message": "unexpected tool"}, error=True)

    def close(self) -> None:
        return None


class GitHubMCPWorkflowDispatchV05Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.authority = {
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
        self.context = {
            "runtime_root": str(self.root),
            "github_mcp_workflow_dispatch_enabled": True,
            "apply_github_mcp_workflow_dispatch": True,
            "execute_external_actions": True,
            "confirmation": CONFIRMATION,
            "repository_full_name": REPOSITORY,
            "base_sha": BASE_SHA,
            "poll_attempts": 2,
            "poll_interval_seconds": 0,
            "mode": "mock",
        }

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write_plan(self, **overrides: Any) -> dict[str, Any]:
        plan: dict[str, Any] = {
            "version": "kuuos_github_mcp_workflow_dispatch_plan_v0_5",
            "mode": "mock",
            "repository_full_name": REPOSITORY,
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
        plan.update(overrides)
        (self.root / "github_mcp_workflow_dispatch_plan_v0_5.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        (self.root / "github_mcp_workflow_dispatch_authority_v0_5.json").write_text(
            json.dumps(self.authority), encoding="utf-8"
        )
        return plan

    def _run(self, transport: WorkflowDispatchTransport, context: Mapping[str, Any] | None = None):
        return build_github_mcp_workflow_dispatch(
            runtime_context=dict(context or self.context),
            authority_packet=self.authority,
            transport=transport,
        )

    def test_dispatch_and_exact_run_reobservation_is_verified(self) -> None:
        self._write_plan()
        transport = WorkflowDispatchTransport()
        result = self._run(transport)
        self.assertEqual(result.status, VERIFIED)
        self.assertTrue(result.dispatch_accepted)
        self.assertTrue(result.run_observed)
        self.assertEqual(result.run_id, 200)
        self.assertEqual(result.run_head_sha, BASE_SHA)
        self.assertEqual(
            [call["name"] for call in transport.calls],
            ["actions_list", "actions_run_trigger", "actions_list"],
        )
        receipt = json.loads(
            (self.root / "github_mcp_workflow_dispatch_receipt_v0_5.json").read_text()
        )
        self.assertNotIn("GITHUB_PERSONAL_ACCESS_TOKEN", json.dumps(receipt))

    def test_runtime_confirmation_is_required(self) -> None:
        self._write_plan()
        context = dict(self.context, confirmation="wrong")
        result = self._run(WorkflowDispatchTransport(), context)
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("runtime_confirmation_invalid", result.blockers)

    def test_plan_confirmation_is_required(self) -> None:
        self._write_plan(confirmation="wrong")
        result = self._run(WorkflowDispatchTransport())
        self.assertIn("plan_confirmation_invalid", result.blockers)

    def test_actions_run_trigger_must_be_write_capable(self) -> None:
        self._write_plan()
        result = self._run(WorkflowDispatchTransport(trigger_read_only=True))
        self.assertIn("actions_run_trigger_not_classified_write", result.blockers)

    def test_target_expected_sha_must_equal_plan_base(self) -> None:
        plan = self._write_plan()
        plan["target"]["expected_head_sha"] = "1" * 40
        (self.root / "github_mcp_workflow_dispatch_plan_v0_5.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        result = self._run(WorkflowDispatchTransport())
        self.assertIn("target_expected_head_sha_mismatch", result.blockers)

    def test_dispatch_nonce_must_bind_target_input(self) -> None:
        plan = self._write_plan()
        plan["target"]["inputs"]["dispatch_nonce"] = "different-nonce"
        (self.root / "github_mcp_workflow_dispatch_plan_v0_5.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        result = self._run(WorkflowDispatchTransport())
        self.assertIn("target_input_nonce_mismatch", result.blockers)

    def test_missing_new_run_is_blocked(self) -> None:
        self._write_plan()
        result = self._run(WorkflowDispatchTransport(observed=False))
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("dispatched_run_not_observed", result.blockers)

    def test_wrong_head_run_is_cancelled_and_not_verified(self) -> None:
        self._write_plan()
        transport = WorkflowDispatchTransport(wrong_head_sha=True)
        result = self._run(transport)
        self.assertEqual(result.status, MISMATCH_CANCELLED)
        self.assertTrue(result.mismatch_cancel_attempted)
        self.assertTrue(result.mismatch_cancelled)
        self.assertTrue(transport.cancelled)
        self.assertFalse(result.run_observed)

    def test_failed_mismatch_cancellation_remains_blocked(self) -> None:
        self._write_plan()
        result = self._run(
            WorkflowDispatchTransport(wrong_head_sha=True, cancel_fails=True)
        )
        self.assertEqual(result.status, BLOCKED)
        self.assertTrue(result.mismatch_cancel_attempted)
        self.assertFalse(result.mismatch_cancelled)


if __name__ == "__main__":
    unittest.main()
