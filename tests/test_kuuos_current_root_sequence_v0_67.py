import unittest

from runtime.kuuos_current_root_sequence_v0_67 import (
    CURRENT_ROOT_STEPS,
    STATUS_FRONTIER,
    as_markdown,
    sequence_issues,
    step_ids,
    step_targets,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV067Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_steps_are_unique(self):
        self.assertEqual(len(step_ids()), len(set(step_ids())))
        self.assertEqual(len(step_targets()), len(set(step_targets())))

    def test_first_step_is_closed_root_callable(self):
        first = CURRENT_ROOT_STEPS[0]
        self.assertEqual("callable", first.runner)
        self.assertEqual("runtime.v124_checkpoint_reflog_runtime:run_v124", first.target)

    def test_status_frontier_is_connected(self):
        self.assertEqual("kuuos_self_organization_status_v0_67", STATUS_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_self_organization_status_v0_67", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_67", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("self-organization-status-v0-67", text)
        self.assertIn("current-root-sequence-v0-67", text)


if __name__ == "__main__":
    unittest.main()
