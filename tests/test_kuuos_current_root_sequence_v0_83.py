import unittest

from runtime.kuuos_current_root_sequence_v0_83 import (
    EXECUTION_PLAN_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV083Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_execution_plan_frontier_is_connected(self):
        self.assertEqual("kuuos_self_organization_execution_plan_v0_83", EXECUTION_PLAN_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_self_organization_execution_plan_v0_83", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_83", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("execution-plan-v0-83", text)
        self.assertIn("current-root-sequence-v0-83", text)


if __name__ == "__main__":
    unittest.main()
