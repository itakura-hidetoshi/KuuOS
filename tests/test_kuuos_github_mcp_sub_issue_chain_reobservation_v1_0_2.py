from __future__ import annotations

import unittest
from typing import Any, Mapping

from runtime.kuuos_github_mcp_sub_issue_chain_reobservation_v1_0_1 import (
    BoundedParentReobservationTransport,
)
from runtime.kuuos_github_mcp_sub_issue_chain_reobservation_v1_0_2 import (
    MAX_PARENT_READ_ATTEMPTS,
    PARENT_READ_DELAY_SECONDS,
)
from tests.test_kuuos_github_mcp_sub_issue_chain_reobservation_v1_0_1 import response


class FifthReadParentTransport:
    def __init__(self) -> None:
        self.parent_reads = 0

    def list_tools(self) -> dict[str, Any]:
        return {"result": {"tools": []}}

    def call_tool(self, name: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
        if name == "sub_issue_write":
            return response({"status": "ok"})
        if name == "issue_read" and arguments.get("method") == "get_parent":
            self.parent_reads += 1
            if self.parent_reads < 5:
                return response({"parent": None})
            return response({"parent": {"number": 1}})
        return response({})

    def close(self) -> None:
        return None


class ExtendedWindowTests(unittest.TestCase):
    def test_live_window_is_bounded_to_sixty_seconds(self) -> None:
        self.assertEqual(MAX_PARENT_READ_ATTEMPTS, 30)
        self.assertEqual(PARENT_READ_DELAY_SECONDS, 2.0)

    def test_parent_visible_after_original_bound_is_accepted(self) -> None:
        inner = FifthReadParentTransport()
        wrapped = BoundedParentReobservationTransport(
            inner,
            max_attempts=MAX_PARENT_READ_ATTEMPTS,
            delay_seconds=0,
        )
        wrapped.call_tool("sub_issue_write", {"method": "add"})
        result = wrapped.call_tool("issue_read", {"method": "get_parent"})
        self.assertIn('"number": 1', result["result"]["content"][0]["text"])
        self.assertEqual(inner.parent_reads, 5)
        self.assertEqual(wrapped.records[-1]["status"], "verified")


if __name__ == "__main__":
    unittest.main()
