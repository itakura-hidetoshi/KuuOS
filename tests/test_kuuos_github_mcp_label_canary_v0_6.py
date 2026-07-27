from __future__ import annotations

import json
import pathlib
import tempfile
import unittest
from typing import Any, Mapping

from runtime.kuuos_github_mcp_label_canary_v0_6 import (
    AUTHORITY_READY,
    BLOCKED,
    COMPENSATED,
    CONFIRMATION,
    VERIFIED,
    build_github_mcp_label_canary,
)

BASE_SHA = "45ace8b96a3e57a5f01910837ee14083fb784170"
REPOSITORY = "itakura-hidetoshi/KuuOS"
NONCE = "label-v06-test-001"
IMAGE = "ghcr.io/github/github-mcp-server@sha256:2b0c48b070f61e9d3969269ead600f62d00fb237b60ac849ef3d166ee7de9ad3"


def _response(payload: Any, *, error: bool = False) -> dict[str, Any]:
    text = payload if isinstance(payload, str) else json.dumps(payload)
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "isError": error,
            "content": [{"type": "text", "text": text}],
        },
    }


class StatefulLabelTransport:
    def __init__(
        self,
        *,
        label_write_read_only: bool = False,
        get_label_write: bool = False,
        preexisting: bool = False,
        corrupt_created: bool = False,
        fail_create_after_apply: bool = False,
        fail_first_delete: bool = False,
        fail_compensation: bool = False,
    ) -> None:
        self.label_write_read_only = label_write_read_only
        self.get_label_write = get_label_write
        self.corrupt_created = corrupt_created
        self.fail_create_after_apply = fail_create_after_apply
        self.fail_first_delete = fail_first_delete
        self.fail_compensation = fail_compensation
        self.calls: list[dict[str, Any]] = []
        self.delete_attempts = 0
        self.label: dict[str, Any] | None = None
        if preexisting:
            self.label = {
                "name": f"kuuos-mcp-canary-{NONCE}",
                "color": "000000",
                "description": "preexisting",
            }

    def list_tools(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": [
                    {
                        "name": "label_write",
                        "inputSchema": {"type": "object"},
                        "annotations": {
                            "readOnlyHint": self.label_write_read_only,
                            "destructiveHint": True,
                        },
                    },
                    {
                        "name": "get_label",
                        "inputSchema": {"type": "object"},
                        "annotations": {"readOnlyHint": not self.get_label_write},
                    },
                ]
            },
        }

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        args = dict(arguments)
        self.calls.append({"name": name, "arguments": args})
        if name == "get_label":
            if self.label is None:
                return _response(
                    f"label '{args['name']}' not found in {args['owner']}/{args['repo']}",
                    error=True,
                )
            observed = dict(self.label)
            if self.corrupt_created:
                observed["color"] = "ffffff"
            return _response(observed)
        if name == "label_write" and args.get("method") == "create":
            self.label = {
                "name": args["name"],
                "color": args["color"],
                "description": args.get("description", ""),
            }
            if self.fail_create_after_apply:
                return _response("create response lost", error=True)
            return _response(f"label '{args['name']}' created successfully")
        if name == "label_write" and args.get("method") == "delete":
            self.delete_attempts += 1
            if self.fail_first_delete and self.delete_attempts == 1:
                return _response("first delete failed", error=True)
            if self.fail_compensation and self.delete_attempts >= 2:
                return _response("compensation delete failed", error=True)
            if self.label is None:
                return _response(
                    f"label '{args['name']}' not found in {args['owner']}/{args['repo']}",
                    error=True,
                )
            self.label = None
            return _response(f"label '{args['name']}' deleted successfully")
        return _response("unexpected tool", error=True)

    def close(self) -> None:
        return None


class GitHubMCPLabelCanaryV06Tests(unittest.TestCase):
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
            "compensating_delete_allowed": True,
            "receipt_write_allowed": True,
            "audit_append_allowed": True,
        }
        self.context = {
            "runtime_root": str(self.root),
            "github_mcp_label_canary_enabled": True,
            "apply_github_mcp_label_canary": True,
            "execute_external_actions": True,
            "confirmation": CONFIRMATION,
            "repository_full_name": REPOSITORY,
            "base_sha": BASE_SHA,
            "label_nonce": NONCE,
            "mode": "mock",
        }

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write_plan(self, **overrides: Any) -> dict[str, Any]:
        plan: dict[str, Any] = {
            "version": "kuuos_github_mcp_label_canary_plan_v0_6",
            "mode": "mock",
            "repository_full_name": REPOSITORY,
            "base_branch": "main",
            "base_sha": BASE_SHA,
            "write_capable": True,
            "read_only": False,
            "lockdown_mode": True,
            "execute_external_actions": True,
            "confirmation": CONFIRMATION,
            "label_nonce": NONCE,
            "label_prefix": "kuuos-mcp-canary-",
            "label_color": "5319e7",
            "description_marker": "KUUOS_GITHUB_MCP_LABEL_CANARY v0.6",
            "server": {
                "kind": "official_github_mcp_server",
                "launcher": "docker",
                "image": IMAGE,
                "token_env": "GITHUB_PERSONAL_ACCESS_TOKEN",
                "toolsets": ["labels"],
                "tools": ["label_write", "get_label"],
            },
        }
        plan.update(overrides)
        (self.root / "github_mcp_label_canary_plan_v0_6.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        (self.root / "github_mcp_label_canary_authority_v0_6.json").write_text(
            json.dumps(self.authority), encoding="utf-8"
        )
        return plan

    def _run(
        self,
        transport: StatefulLabelTransport,
        context: Mapping[str, Any] | None = None,
    ):
        return build_github_mcp_label_canary(
            runtime_context=dict(context or self.context),
            authority_packet=self.authority,
            transport=transport,
        )

    def test_create_observe_delete_observe_absent_is_verified(self) -> None:
        self._write_plan()
        transport = StatefulLabelTransport()
        result = self._run(transport)
        self.assertEqual(result.status, VERIFIED)
        self.assertTrue(result.preflight_absent)
        self.assertTrue(result.created_verified)
        self.assertTrue(result.deleted_verified)
        self.assertIsNone(transport.label)
        self.assertEqual(
            [call["name"] for call in transport.calls],
            ["get_label", "label_write", "get_label", "label_write", "get_label"],
        )
        receipt = json.loads(
            (self.root / "github_mcp_label_canary_receipt_v0_6.json").read_text()
        )
        self.assertNotIn("GITHUB_PERSONAL_ACCESS_TOKEN", json.dumps(receipt))

    def test_runtime_confirmation_is_required(self) -> None:
        self._write_plan()
        result = self._run(
            StatefulLabelTransport(),
            dict(self.context, confirmation="wrong"),
        )
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("runtime_confirmation_invalid", result.blockers)

    def test_plan_confirmation_is_required(self) -> None:
        self._write_plan(confirmation="wrong")
        result = self._run(StatefulLabelTransport())
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("plan_confirmation_invalid", result.blockers)

    def test_official_image_must_be_pinned(self) -> None:
        plan = self._write_plan()
        plan["server"]["image"] = "ghcr.io/github/github-mcp-server:latest"
        (self.root / "github_mcp_label_canary_plan_v0_6.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )
        result = self._run(StatefulLabelTransport())
        self.assertIn("official_server_image_not_pinned", result.blockers)

    def test_label_write_must_be_write_capable(self) -> None:
        self._write_plan()
        result = self._run(StatefulLabelTransport(label_write_read_only=True))
        self.assertIn("label_write_not_classified_write", result.blockers)

    def test_get_label_must_be_read_only(self) -> None:
        self._write_plan()
        result = self._run(StatefulLabelTransport(get_label_write=True))
        self.assertIn("get_label_not_classified_read_only", result.blockers)

    def test_preexisting_label_is_never_deleted(self) -> None:
        self._write_plan()
        transport = StatefulLabelTransport(preexisting=True)
        result = self._run(transport)
        self.assertEqual(result.status, BLOCKED)
        self.assertFalse(result.preflight_absent)
        self.assertIsNotNone(transport.label)
        self.assertEqual([call["name"] for call in transport.calls], ["get_label"])

    def test_created_observation_mismatch_is_compensated(self) -> None:
        self._write_plan()
        transport = StatefulLabelTransport(corrupt_created=True)
        result = self._run(transport)
        self.assertEqual(result.status, COMPENSATED)
        self.assertTrue(result.compensation_attempted)
        self.assertTrue(result.compensation_deleted)
        self.assertIsNone(transport.label)

    def test_ambiguous_create_response_is_compensated(self) -> None:
        self._write_plan()
        transport = StatefulLabelTransport(fail_create_after_apply=True)
        result = self._run(transport)
        self.assertEqual(result.status, COMPENSATED)
        self.assertTrue(result.compensation_deleted)
        self.assertIsNone(transport.label)

    def test_failed_primary_delete_is_compensated(self) -> None:
        self._write_plan()
        transport = StatefulLabelTransport(fail_first_delete=True)
        result = self._run(transport)
        self.assertEqual(result.status, COMPENSATED)
        self.assertEqual(transport.delete_attempts, 2)
        self.assertTrue(result.compensation_deleted)
        self.assertIsNone(transport.label)

    def test_failed_compensation_remains_blocked(self) -> None:
        self._write_plan()
        transport = StatefulLabelTransport(
            fail_first_delete=True,
            fail_compensation=True,
        )
        result = self._run(transport)
        self.assertEqual(result.status, BLOCKED)
        self.assertFalse(result.compensation_deleted)
        self.assertIsNotNone(transport.label)


if __name__ == "__main__":
    unittest.main()
