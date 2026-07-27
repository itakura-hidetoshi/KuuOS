from __future__ import annotations

import unittest

from runtime.kuuos_github_mcp_sub_issue_chain_reobservation_v1_0_2 import (
    MAX_PARENT_READ_ATTEMPTS,
    PARENT_READ_DELAY_SECONDS,
    build_github_mcp_sub_issue_chain_canary,
)
from runtime.kuuos_github_mcp_sub_issue_chain_canary_v1_0 import VERIFIED
from tests.test_kuuos_github_mcp_sub_issue_chain_reobservation_v1_0_1 import (
    DelayedAttachedParent,
    run_case,
)


class ExtendedWindowTests(unittest.TestCase):
    def test_live_window_is_bounded_to_sixty_seconds(self):
        self.assertEqual(MAX_PARENT_READ_ATTEMPTS, 30)
        self.assertEqual(PARENT_READ_DELAY_SECONDS, 2.0)

    def test_existing_delayed_parent_case_remains_verified(self):
        result = run_case(
            DelayedAttachedParent(),
            builder=build_github_mcp_sub_issue_chain_canary,
        )
        self.assertEqual(result.status, VERIFIED)


if __name__ == "__main__":
    unittest.main()
