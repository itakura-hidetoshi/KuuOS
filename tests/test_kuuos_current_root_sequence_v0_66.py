import unittest

from runtime.kuuos_current_root_sequence_v0_66 import (
    CURRENT_ROOT_STEPS,
    PUBLIC_STATUS_FRONTIER,
    as_markdown,
    sequence_issues,
    step_ids,
    step_targets,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV066Test(unittest.TestCase):
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

    def test_readme_public_status_is_connected(self):
        self.assertEqual("kuuos_readme_public_status_v0_66", PUBLIC_STATUS_FRONTIER)
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_readme_public_status_v0_66", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_66", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("readme-public-status-v0-66", text)
        self.assertIn("current-root-sequence-v0-66", text)


if __name__ == "__main__":
    unittest.main()
