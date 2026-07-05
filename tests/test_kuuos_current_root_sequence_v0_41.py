import unittest

from runtime.kuuos_current_root_sequence_v0_41 import (
    CURRENT_ROOT_STEPS,
    as_markdown,
    sequence_issues,
    step_ids,
    step_targets,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV041Test(unittest.TestCase):
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

    def test_current_self_organization_tests_are_present(self):
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_repository_frontier_summary_v0_40", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_41", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("current-root-sequence-v0-41", text)
        self.assertIn("repository-frontier-summary-v0-40", text)


if __name__ == "__main__":
    unittest.main()
