from __future__ import annotations

import unittest
from typing import Any, Mapping

from runtime.kuuos_github_mcp_sub_issue_chain_reobservation_v1_0_1 import (
    BoundedParentReobservationTransport,
)


def response(value: Mapping[str, Any]) -> dict[str, Any]:
    import json
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {"content": [{"type": "text", "text": json.dumps(value)}]},
    }


class DelayedParentTransport:
    def __init__(self) -> None:
        self.parent_reads = 0
        self.mode = "present"

    def list_tools(self) -> dict[str, Any]:
        return {"result": {"tools": []}}

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        if name == "sub_issue_write":
            self.mode = str(arguments.get("method"))
            return response({"status": "ok"})
        if name == "issue_read" and arguments.get("method") == "get_parent":
            self.parent_reads += 1
            if self.mode == "add" and self.parent_reads < 3:
                return response({"parent": None})
            if self.mode == "remove" and self.parent_reads < 3:
                return response({"parent": {"number": 1}})
            return response(
                {"parent": {"number": 1}}
                if self.mode == "add"
                else {"parent": None}
            )
        return response({})

    def close(self) -> None:
        return None


class ReobservationTests(unittest.TestCase):
    def test_attached_parent_is_reobserved_within_bound(self) -> None:
        inner = DelayedParentTransport()
        wrapped = BoundedParentReobservationTransport(
            inner, max_attempts=4, delay_seconds=0
        )
        wrapped.call_tool("sub_issue_write", {"method": "add"})
        result = wrapped.call_tool("issue_read", {"method": "get_parent"})
        self.assertIn('"number": 1', result["result"]["content"][0]["text"])
        self.assertEqual(inner.parent_reads, 3)
        self.assertEqual(len(wrapped.records), 3)
        self.assertEqual(wrapped.records[-1]["status"], "verified")

    def test_absent_parent_is_reobserved_within_bound(self) -> None:
        inner = DelayedParentTransport()
        wrapped = BoundedParentReobservationTransport(
            inner, max_attempts=4, delay_seconds=0
        )
        wrapped.call_tool("sub_issue_write", {"method": "remove"})
        result = wrapped.call_tool("issue_read", {"method": "get_parent"})
        self.assertIn('"parent": null', result["result"]["content"][0]["text"])
        self.assertEqual(inner.parent_reads, 3)
        self.assertEqual(wrapped.records[-1]["status"], "verified")

    def test_bound_returns_last_observation_fail_closed(self) -> None:
        inner = DelayedParentTransport()
        wrapped = BoundedParentReobservationTransport(
            inner, max_attempts=2, delay_seconds=0
        )
        wrapped.call_tool("sub_issue_write", {"method": "add"})
        result = wrapped.call_tool("issue_read", {"method": "get_parent"})
        self.assertIn('"parent": null', result["result"]["content"][0]["text"])
        self.assertEqual(inner.parent_reads, 2)
        self.assertTrue(all(r["status"] == "retry" for r in wrapped.records))


if __name__ == "__main__":
    unittest.main()
