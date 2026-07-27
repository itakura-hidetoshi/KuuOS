from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from typing import Any, Mapping

from runtime.kuuos_github_mcp_sub_issue_bidirectional_canary_v0_9 import (
    BLOCKED,
    COMPENSATED,
    CONFIRMATION,
    REQUEST_TITLE,
    REQUEST_VERSION,
    VERIFIED,
    build_github_mcp_sub_issue_bidirectional_canary,
)
from scripts.check_kuuos_github_mcp_sub_issue_bidirectional_canary_v0_9 import (
    BASE_SHA,
    IMAGE,
    NONCE,
    PARENT,
    MockTransport,
    authority,
    plan,
    response,
)


def run_case(transport: MockTransport, *, plan_mutation=None, authority_mutation=None):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        current_plan = plan()
        current_authority = authority()
        if plan_mutation:
            plan_mutation(current_plan)
        if authority_mutation:
            authority_mutation(current_authority)
        (
            root / "github_mcp_sub_issue_bidirectional_canary_plan_v0_9.json"
        ).write_text(json.dumps(current_plan))
        (
            root / "github_mcp_sub_issue_bidirectional_canary_authority_v0_9.json"
        ).write_text(json.dumps(current_authority))
        return build_github_mcp_sub_issue_bidirectional_canary(
            runtime_context={
                "runtime_root": str(root),
                "github_mcp_sub_issue_bidirectional_canary_enabled": True,
                "apply_github_mcp_sub_issue_bidirectional_canary": True,
                "execute_external_actions": True,
                "confirmation": CONFIRMATION,
                "repository_full_name": "itakura-hidetoshi/KuuOS",
                "base_sha": BASE_SHA,
                "transaction_nonce": NONCE,
                "parent_issue_number": PARENT,
                "mode": "mock",
            },
            authority_packet=current_authority,
            transport=transport,
        )


class WrongAttachedParentTransport(MockTransport):
    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        result = super().call_tool(name, arguments)
        if name == "sub_issue_write" and arguments.get("method") == "add":
            assert self.child_parent is not None
            self.child_parent["number"] = PARENT + 1
        return result


class ResidualParentTransport(MockTransport):
    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        if name == "sub_issue_write" and arguments.get("method") == "remove":
            self.parent_children = []
            return response({"status": "removed"})
        return super().call_tool(name, arguments)


class PreexistingChildParentTransport(MockTransport):
    def __init__(self) -> None:
        super().__init__()
        self.parent_reads = 0

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        result = super().call_tool(name, arguments)
        if name == "issue_read" and arguments.get("method") == "get_parent":
            self.parent_reads += 1
            if self.parent_reads == 1:
                return response(
                    {
                        "parent": {
                            "number": 44,
                            "title": "unexpected",
                            "state": "OPEN",
                            "url": "https://github.com/itakura-hidetoshi/KuuOS/issues/44",
                            "repository": "itakura-hidetoshi/KuuOS",
                        }
                    }
                )
        return result


class WrongAnnotationTransport(MockTransport):
    def list_tools(self) -> dict[str, Any]:
        value = super().list_tools()
        value["result"]["tools"][1]["annotations"]["readOnlyHint"] = False
        return value


class EncodedParentTransport(MockTransport):
    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        if (
            name == "issue_read"
            and arguments.get("method") == "get"
            and arguments.get("issue_number") == PARENT
        ):
            body = json.dumps(
                {
                    "version": REQUEST_VERSION,
                    "confirmation": CONFIRMATION,
                    "expected_main_sha": BASE_SHA,
                    "transaction_nonce": NONCE,
                    "server_image": IMAGE,
                }
            ).replace('"', "&#34;")
            return response(
                {
                    "number": PARENT,
                    "title": REQUEST_TITLE,
                    "state": "open",
                    "body": body,
                }
            )
        return super().call_tool(name, arguments)


class SubIssueBidirectionalCanaryTests(unittest.TestCase):
    def test_complete_bidirectional_transaction_verifies(self):
        result = run_case(MockTransport())
        self.assertEqual(result.status, VERIFIED)
        self.assertTrue(result.child_parent_preflight_absent)
        self.assertTrue(result.child_parent_added_verified)
        self.assertTrue(result.child_parent_removed_verified)
        self.assertTrue(result.child_closed_verified)
        self.assertFalse(result.compensation_attempted)

    def test_wrong_attached_parent_compensates(self):
        transport = WrongAttachedParentTransport()
        result = run_case(transport)
        self.assertEqual(result.status, COMPENSATED)
        self.assertFalse(result.child_parent_added_verified)
        self.assertTrue(result.compensation_child_parent_removed)
        self.assertTrue(result.compensation_child_closed)
        self.assertIsNone(transport.child_parent)
        self.assertIn("observed_child_parent_number_mismatch", result.blockers)

    def test_residual_parent_after_remove_never_admits(self):
        transport = ResidualParentTransport()
        result = run_case(transport)
        self.assertEqual(result.status, BLOCKED)
        self.assertFalse(result.child_parent_removed_verified)
        self.assertFalse(result.compensation_child_parent_removed)
        self.assertIn("observed_child_parent_residual", result.blockers)

    def test_child_parent_must_start_absent(self):
        result = run_case(PreexistingChildParentTransport())
        self.assertEqual(result.status, COMPENSATED)
        self.assertFalse(result.child_parent_preflight_absent)
        self.assertTrue(result.compensation_child_parent_removed)

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

    def test_upward_read_authority_is_required_before_writes(self):
        transport = MockTransport()
        result = run_case(
            transport,
            authority_mutation=lambda value: value.update(
                {"upward_parent_reobservation_allowed": False}
            ),
        )
        self.assertEqual(result.status, BLOCKED)
        self.assertIsNone(transport.child)
        self.assertIn("upward_parent_reobservation_not_allowed", result.blockers)


if __name__ == "__main__":
    unittest.main()
