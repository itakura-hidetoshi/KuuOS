from __future__ import annotations

import json
import unittest
from typing import Any, Mapping

from runtime.kuuos_github_mcp_sub_issue_chain_parent_cross_observation_v1_1 import (
    ExactParentCrossObservationTransport,
)


def response(value: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {"content": [{"type": "text", "text": json.dumps(dict(value))}]},
    }


class NestedParentTransport:
    def __init__(self, *, child_has_parent: bool = True, parent_number: int = 10) -> None:
        self.child_has_parent = child_has_parent
        self.parent_number = parent_number
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def list_tools(self) -> dict[str, Any]:
        return {"result": {"tools": []}}

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        args = dict(arguments)
        self.calls.append((name, args))
        if name == "sub_issue_write":
            return response({"status": "ok"})
        if name == "issue_read" and args.get("method") == "get_parent":
            return response({"parent": None})
        if name == "issue_read" and args.get("method") == "get":
            number = int(args["issue_number"])
            if number == 11:
                return response(
                    {
                        "number": 11,
                        "has_parent": self.child_has_parent,
                        "parent_issue_url": "https://api.github.com/repos/o/r/issues/10"
                        if self.child_has_parent
                        else None,
                    }
                )
            if number == self.parent_number:
                return response({"number": self.parent_number, "title": "parent", "state": "open"})
        return response({})

    def close(self) -> None:
        return None


class ParentCrossObservationTests(unittest.TestCase):
    def test_exact_cross_observation_synthesizes_parent(self) -> None:
        inner = NestedParentTransport()
        wrapped = ExactParentCrossObservationTransport(inner, max_attempts=2, delay_seconds=0)
        wrapped.call_tool(
            "sub_issue_write",
            {"method": "add", "owner": "o", "repo": "r", "issue_number": 10, "sub_issue_id": 99},
        )
        result = wrapped.call_tool(
            "issue_read",
            {"method": "get_parent", "owner": "o", "repo": "r", "issue_number": 11},
        )
        observed = json.loads(result["result"]["content"][0]["text"])
        self.assertEqual(observed["parent"]["number"], 10)
        self.assertEqual(observed["parent"]["title"], "parent")
        self.assertEqual(observed["parent"]["repository"], "o/r")
        self.assertEqual(wrapped.records[-1]["phase"], "cross_observe_exact_parent_synthesis")
        self.assertEqual(wrapped.records[-1]["status"], "verified")

    def test_missing_child_parent_evidence_fails_closed(self) -> None:
        inner = NestedParentTransport(child_has_parent=False)
        wrapped = ExactParentCrossObservationTransport(inner, max_attempts=1, delay_seconds=0)
        wrapped.call_tool(
            "sub_issue_write",
            {"method": "add", "owner": "o", "repo": "r", "issue_number": 10, "sub_issue_id": 99},
        )
        result = wrapped.call_tool(
            "issue_read",
            {"method": "get_parent", "owner": "o", "repo": "r", "issue_number": 11},
        )
        observed = json.loads(result["result"]["content"][0]["text"])
        self.assertIsNone(observed["parent"])
        blockers = {b for record in wrapped.records for b in record.get("blockers", [])}
        self.assertIn("cross_child_has_parent_not_true", blockers)

    def test_remove_requires_direct_absence_only(self) -> None:
        inner = NestedParentTransport()
        wrapped = ExactParentCrossObservationTransport(inner, max_attempts=1, delay_seconds=0)
        wrapped.call_tool(
            "sub_issue_write",
            {"method": "remove", "owner": "o", "repo": "r", "issue_number": 10, "sub_issue_id": 99},
        )
        result = wrapped.call_tool(
            "issue_read",
            {"method": "get_parent", "owner": "o", "repo": "r", "issue_number": 11},
        )
        observed = json.loads(result["result"]["content"][0]["text"])
        self.assertIsNone(observed["parent"])
        self.assertFalse(any(record["phase"].startswith("cross_observe") for record in wrapped.records))


if __name__ == "__main__":
    unittest.main()
