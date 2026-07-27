from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from typing import Any, Mapping

from runtime.kuuos_github_mcp_sub_issue_binding_canary_v0_8 import (
    BLOCKED,
    COMPENSATED,
    CONFIRMATION,
    REQUEST_TITLE,
    REQUEST_VERSION,
    VERIFIED,
    build_github_mcp_sub_issue_binding_canary,
)
from scripts.check_kuuos_github_mcp_sub_issue_binding_canary_v0_8 import (
    BASE_SHA,
    IMAGE,
    NONCE,
    PARENT,
    MockTransport,
    authority,
    plan,
    response,
)


def run_case(transport: MockTransport, *, plan_mutation=None):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        current_plan = plan()
        if plan_mutation:
            plan_mutation(current_plan)
        (root / "github_mcp_sub_issue_binding_canary_plan_v0_8.json").write_text(json.dumps(current_plan))
        (root / "github_mcp_sub_issue_binding_canary_authority_v0_8.json").write_text(json.dumps(authority()))
        return build_github_mcp_sub_issue_binding_canary(
            runtime_context={
                "runtime_root": str(root),
                "github_mcp_sub_issue_binding_canary_enabled": True,
                "apply_github_mcp_sub_issue_binding_canary": True,
                "execute_external_actions": True,
                "confirmation": CONFIRMATION,
                "repository_full_name": "itakura-hidetoshi/KuuOS",
                "base_sha": BASE_SHA,
                "transaction_nonce": NONCE,
                "parent_issue_number": PARENT,
                "mode": "mock",
            },
            authority_packet=authority(),
            transport=transport,
        )


class PreexistingTransport(MockTransport):
    def __init__(self):
        super().__init__()
        self.parent_children = [{"id": 1, "number": 99, "title": "preexisting"}]


class AddFailureTransport(MockTransport):
    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        if name == "sub_issue_write" and arguments.get("method") == "add":
            return response("injected add failure", error=True)
        return super().call_tool(name, arguments)


class WrongAnnotationTransport(MockTransport):
    def list_tools(self) -> dict[str, Any]:
        value = super().list_tools()
        value["result"]["tools"][1]["annotations"]["readOnlyHint"] = False
        return value


class EncodedParentTransport(MockTransport):
    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        if name == "issue_read" and arguments.get("method") == "get" and arguments.get("issue_number") == PARENT:
            body = json.dumps({
                "version": REQUEST_VERSION,
                "confirmation": CONFIRMATION,
                "expected_main_sha": BASE_SHA,
                "transaction_nonce": NONCE,
                "server_image": IMAGE,
            }).replace('"', "&#34;")
            return response({"number": PARENT, "title": REQUEST_TITLE, "state": "open", "body": body})
        return super().call_tool(name, arguments)


class SubIssueBindingCanaryTests(unittest.TestCase):
    def test_complete_transaction_verifies(self):
        result = run_case(MockTransport())
        self.assertEqual(result.status, VERIFIED)
        self.assertTrue(result.binding_added_verified)
        self.assertTrue(result.binding_removed_verified)
        self.assertTrue(result.child_closed_verified)
        self.assertFalse(result.compensation_attempted)

    def test_preexisting_sub_issue_blocks_without_child_creation(self):
        transport = PreexistingTransport()
        result = run_case(transport)
        self.assertEqual(result.status, BLOCKED)
        self.assertEqual(result.child_issue_number, 0)
        self.assertIn("parent_has_preexisting_or_residual_sub_issues", result.blockers)

    def test_partial_child_creation_compensates(self):
        transport = AddFailureTransport()
        result = run_case(transport)
        self.assertEqual(result.status, COMPENSATED)
        self.assertTrue(result.compensation_binding_removed)
        self.assertTrue(result.compensation_child_closed)
        self.assertEqual(transport.parent_children, [])
        self.assertEqual(transport.child["state"], "closed")

    def test_read_tool_must_be_read_only(self):
        result = run_case(WrongAnnotationTransport())
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("issue_read_not_classified_read_only", result.blockers)

    def test_official_single_html_entity_layer_is_accepted(self):
        result = run_case(EncodedParentTransport())
        self.assertEqual(result.status, VERIFIED)

    def test_unpinned_image_blocks(self):
        result = run_case(
            MockTransport(),
            plan_mutation=lambda value: value["server"].update(
                {"image": "ghcr.io/github/github-mcp-server:latest"}
            ),
        )
        self.assertEqual(result.status, BLOCKED)
        self.assertIn("official_server_image_not_pinned", result.blockers)


if __name__ == "__main__":
    unittest.main()
