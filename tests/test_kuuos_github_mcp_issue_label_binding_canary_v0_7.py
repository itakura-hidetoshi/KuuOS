from __future__ import annotations

import json
import pathlib
import tempfile
import unittest
from typing import Any, Mapping

from runtime.kuuos_github_mcp_issue_label_binding_canary_v0_7 import (
    AUTHORITY_READY,
    BLOCKED,
    COMPENSATED,
    CONFIRMATION,
    VERIFIED,
    build_github_mcp_issue_label_binding_canary,
)

BASE_SHA = "1cb3c4cceba77588403de9b8c1374bb93f1c9a0e"
REPOSITORY = "itakura-hidetoshi/KuuOS"
NONCE = "binding-v07-test-001"
ISSUE_NUMBER = 1701
TITLE = "[KuuOS MCP Issue Label Binding Canary v0.7]"
IMAGE = "ghcr.io/github/github-mcp-server@sha256:2b0c48b070f61e9d3969269ead600f62d00fb237b60ac849ef3d166ee7de9ad3"
VERSION = "kuuos_github_mcp_issue_label_binding_canary_request_v0_7"


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


class StatefulBindingTransport:
    def __init__(
        self,
        *,
        issue_write_read_only: bool = False,
        label_write_read_only: bool = False,
        issue_read_write: bool = False,
        get_label_write: bool = False,
        preexisting_issue_labels: list[str] | None = None,
        preexisting_label: bool = False,
        issue_identity_mismatch: bool = False,
        corrupt_label_created: bool = False,
        fail_create_after_apply: bool = False,
        fail_attach_after_apply: bool = False,
        fail_first_detach: bool = False,
        fail_first_delete: bool = False,
        fail_compensation_detach: bool = False,
        fail_compensation_delete: bool = False,
    ) -> None:
        self.issue_write_read_only = issue_write_read_only
        self.label_write_read_only = label_write_read_only
        self.issue_read_write = issue_read_write
        self.get_label_write = get_label_write
        self.issue_identity_mismatch = issue_identity_mismatch
        self.corrupt_label_created = corrupt_label_created
        self.fail_create_after_apply = fail_create_after_apply
        self.fail_attach_after_apply = fail_attach_after_apply
        self.fail_first_detach = fail_first_detach
        self.fail_first_delete = fail_first_delete
        self.fail_compensation_detach = fail_compensation_detach
        self.fail_compensation_delete = fail_compensation_delete
        self.calls: list[dict[str, Any]] = []
        self.detach_attempts = 0
        self.delete_attempts = 0
        self.issue_labels = list(preexisting_issue_labels or [])
        self.label: dict[str, Any] | None = None
        if preexisting_label:
            self.label = {
                "name": f"kuuos-mcp-binding-canary-{NONCE}",
                "color": "000000",
                "description": "preexisting",
            }
        self.issue = {
            "number": ISSUE_NUMBER,
            "title": TITLE,
            "body": json.dumps(
                {
                    "version": VERSION,
                    "confirmation": CONFIRMATION,
                    "expected_main_sha": BASE_SHA,
                    "transaction_nonce": NONCE,
                    "server_image": IMAGE,
                }
            ),
            "state": "open",
        }

    def list_tools(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": [
                    {
                        "name": "issue_write",
                        "inputSchema": {"type": "object"},
                        "annotations": {"readOnlyHint": self.issue_write_read_only},
                    },
                    {
                        "name": "issue_read",
                        "inputSchema": {"type": "object"},
                        "annotations": {"readOnlyHint": not self.issue_read_write},
                    },
                    {
                        "name": "label_write",
                        "inputSchema": {"type": "object"},
                        "annotations": {"readOnlyHint": self.label_write_read_only},
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
        if name == "issue_read" and args.get("method") == "get":
            observed = dict(self.issue)
            if self.issue_identity_mismatch:
                observed["title"] = "wrong"
            return _response(observed)
        if name == "issue_read" and args.get("method") == "get_labels":
            labels = []
            for label_name in self.issue_labels:
                if self.label and self.label.get("name") == label_name:
                    labels.append(dict(self.label))
                else:
                    labels.append({"name": label_name, "color": "000000", "description": "existing"})
            return _response({"labels": labels, "totalCount": len(labels)})
        if name == "get_label":
            if self.label is None:
                return _response(
                    f"label '{args['name']}' not found in {args['owner']}/{args['repo']}",
                    error=True,
                )
            observed = dict(self.label)
            if self.corrupt_label_created:
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
        if name == "issue_write" and args.get("method") == "update" and "labels" in args:
            labels = list(args["labels"])
            if labels:
                self.issue_labels = labels
                if self.fail_attach_after_apply:
                    return _response("attach response lost", error=True)
                return _response({"id": "1701", "url": "https://github.com/x/y/issues/1701"})
            self.detach_attempts += 1
            if self.fail_first_detach and self.detach_attempts == 1:
                return _response("first detach failed", error=True)
            if self.fail_compensation_detach:
                return _response("compensation detach failed", error=True)
            self.issue_labels = []
            return _response({"id": "1701", "url": "https://github.com/x/y/issues/1701"})
        if name == "label_write" and args.get("method") == "delete":
            self.delete_attempts += 1
            if self.fail_first_delete and self.delete_attempts == 1:
                return _response("first delete failed", error=True)
            if self.fail_compensation_delete and self.delete_attempts >= 2:
                return _response("compensation delete failed", error=True)
            if self.label is None:
                return _response("label not found", error=True)
            self.label = None
            return _response(f"label '{args['name']}' deleted successfully")
        return _response("unexpected tool", error=True)

    def close(self) -> None:
        return None


class BindingCanaryTests(unittest.TestCase):
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
            "compensating_issue_detach_allowed": True,
            "compensating_label_delete_allowed": True,
            "receipt_write_allowed": True,
            "audit_append_allowed": True,
        }
        self.context = {
            "runtime_root": str(self.root),
            "github_mcp_issue_label_binding_canary_enabled": True,
            "apply_github_mcp_issue_label_binding_canary": True,
            "execute_external_actions": True,
            "confirmation": CONFIRMATION,
            "repository_full_name": REPOSITORY,
            "base_sha": BASE_SHA,
            "transaction_nonce": NONCE,
            "request_issue_number": ISSUE_NUMBER,
            "mode": "mock",
        }

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write_plan(self, **overrides: Any) -> None:
        plan: dict[str, Any] = {
            "version": "kuuos_github_mcp_issue_label_binding_canary_plan_v0_7",
            "mode": "mock",
            "repository_full_name": REPOSITORY,
            "base_branch": "main",
            "base_sha": BASE_SHA,
            "write_capable": True,
            "read_only": False,
            "lockdown_mode": True,
            "execute_external_actions": True,
            "confirmation": CONFIRMATION,
            "transaction_nonce": NONCE,
            "request_issue_number": ISSUE_NUMBER,
            "request_issue_title": TITLE,
            "request_version_marker": VERSION,
            "label_prefix": "kuuos-mcp-binding-canary-",
            "label_color": "0e8a16",
            "label_description_marker": "KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY v0.7",
            "server": {
                "kind": "official_github_mcp_server",
                "launcher": "docker",
                "image": IMAGE,
                "token_env": "GITHUB_PERSONAL_ACCESS_TOKEN",
                "toolsets": ["issues", "labels"],
                "tools": ["issue_write", "issue_read", "label_write", "get_label"],
            },
        }
        plan.update(overrides)
        (self.root / "github_mcp_issue_label_binding_canary_plan_v0_7.json").write_text(json.dumps(plan))
        (self.root / "github_mcp_issue_label_binding_canary_authority_v0_7.json").write_text(json.dumps(self.authority))

    def _run(self, transport: StatefulBindingTransport, context: Mapping[str, Any] | None = None):
        return build_github_mcp_issue_label_binding_canary(
            runtime_context=dict(context or self.context),
            authority_packet=self.authority,
            transport=transport,
        )

    def test_full_binding_transaction_is_verified(self) -> None:
        self._write_plan()
        transport = StatefulBindingTransport()
        result = self._run(transport)
        self.assertEqual(result.status, VERIFIED)
        self.assertTrue(result.issue_identity_verified)
        self.assertTrue(result.issue_labels_preflight_empty)
        self.assertTrue(result.label_preflight_absent)
        self.assertTrue(result.label_created_verified)
        self.assertTrue(result.label_attached_verified)
        self.assertTrue(result.label_detached_verified)
        self.assertTrue(result.label_deleted_verified)
        self.assertEqual(transport.issue_labels, [])
        self.assertIsNone(transport.label)
        self.assertFalse(result.compensation_attempted)
        receipt = json.loads((self.root / "github_mcp_issue_label_binding_canary_receipt_v0_7.json").read_text())
        self.assertNotIn("GITHUB_PERSONAL_ACCESS_TOKEN", json.dumps(receipt))

    def test_wrong_confirmation_blocks(self) -> None:
        self._write_plan()
        result = self._run(StatefulBindingTransport(), dict(self.context, confirmation="wrong"))
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("runtime_confirmation_invalid", result.blockers)

    def test_request_identity_mismatch_blocks_before_writes(self) -> None:
        self._write_plan()
        transport = StatefulBindingTransport(issue_identity_mismatch=True)
        result = self._run(transport)
        self.assertEqual(result.status, BLOCKED)
        self.assertEqual([call["name"] for call in transport.calls], ["issue_read"])

    def test_preexisting_issue_labels_are_never_replaced(self) -> None:
        self._write_plan()
        transport = StatefulBindingTransport(preexisting_issue_labels=["do-not-touch"])
        result = self._run(transport)
        self.assertEqual(result.status, BLOCKED)
        self.assertEqual(transport.issue_labels, ["do-not-touch"])
        self.assertEqual([call["name"] for call in transport.calls], ["issue_read", "issue_read"])

    def test_preexisting_repository_label_is_never_deleted(self) -> None:
        self._write_plan()
        transport = StatefulBindingTransport(preexisting_label=True)
        result = self._run(transport)
        self.assertEqual(result.status, BLOCKED)
        self.assertIsNotNone(transport.label)
        self.assertEqual([call["name"] for call in transport.calls], ["issue_read", "issue_read", "get_label"])

    def test_tool_annotations_are_enforced(self) -> None:
        self._write_plan()
        for transport, blocker in [
            (StatefulBindingTransport(issue_write_read_only=True), "issue_write_not_classified_write"),
            (StatefulBindingTransport(label_write_read_only=True), "label_write_not_classified_write"),
            (StatefulBindingTransport(issue_read_write=True), "issue_read_not_classified_read_only"),
            (StatefulBindingTransport(get_label_write=True), "get_label_not_classified_read_only"),
        ]:
            result = self._run(transport)
            self.assertIn(blocker, result.blockers)

    def test_corrupt_created_label_is_compensated(self) -> None:
        self._write_plan()
        transport = StatefulBindingTransport(corrupt_label_created=True)
        result = self._run(transport)
        self.assertEqual(result.status, COMPENSATED)
        self.assertTrue(result.compensation_issue_detached)
        self.assertTrue(result.compensation_label_deleted)
        self.assertEqual(transport.issue_labels, [])
        self.assertIsNone(transport.label)

    def test_ambiguous_label_create_is_compensated(self) -> None:
        self._write_plan()
        transport = StatefulBindingTransport(fail_create_after_apply=True)
        result = self._run(transport)
        self.assertEqual(result.status, COMPENSATED)
        self.assertIsNone(transport.label)

    def test_ambiguous_attach_is_compensated(self) -> None:
        self._write_plan()
        transport = StatefulBindingTransport(fail_attach_after_apply=True)
        result = self._run(transport)
        self.assertEqual(result.status, COMPENSATED)
        self.assertEqual(transport.issue_labels, [])
        self.assertIsNone(transport.label)

    def test_failed_primary_detach_is_compensated(self) -> None:
        self._write_plan()
        transport = StatefulBindingTransport(fail_first_detach=True)
        result = self._run(transport)
        self.assertEqual(result.status, COMPENSATED)
        self.assertEqual(transport.detach_attempts, 2)
        self.assertEqual(transport.issue_labels, [])
        self.assertIsNone(transport.label)

    def test_failed_primary_label_delete_is_compensated(self) -> None:
        self._write_plan()
        transport = StatefulBindingTransport(fail_first_delete=True)
        result = self._run(transport)
        self.assertEqual(result.status, COMPENSATED)
        self.assertEqual(transport.delete_attempts, 2)
        self.assertIsNone(transport.label)

    def test_failed_compensation_detach_remains_blocked(self) -> None:
        self._write_plan()
        transport = StatefulBindingTransport(fail_attach_after_apply=True, fail_compensation_detach=True)
        result = self._run(transport)
        self.assertEqual(result.status, BLOCKED)
        self.assertFalse(result.compensation_issue_detached)
        self.assertEqual(transport.issue_labels, [f"kuuos-mcp-binding-canary-{NONCE}"])
        self.assertIsNotNone(transport.label)

    def test_failed_compensation_delete_remains_blocked(self) -> None:
        self._write_plan()
        transport = StatefulBindingTransport(fail_first_delete=True, fail_compensation_delete=True)
        result = self._run(transport)
        self.assertEqual(result.status, BLOCKED)
        self.assertTrue(result.compensation_issue_detached)
        self.assertFalse(result.compensation_label_deleted)
        self.assertEqual(transport.issue_labels, [])
        self.assertIsNotNone(transport.label)


if __name__ == "__main__":
    unittest.main()
