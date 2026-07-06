import unittest

from runtime.kuuos_current_root_sequence_v0_89 import (
    NEXT_CYCLE_SEED_FRONTIER,
    as_markdown,
    sequence_issues,
    unittest_targets,
    verify_current_root_sequence,
)


class CurrentRootSequenceV089Test(unittest.TestCase):
    def test_sequence_valid(self):
        self.assertEqual((), sequence_issues())
        self.assertTrue(verify_current_root_sequence())

    def test_frontier(self):
        self.assertEqual("kuuos_self_organization_next_cycle_seed_v0_89", NEXT_CYCLE_SEED_FRONTIER)

    def test_targets(self):
        targets = set(unittest_targets())
        self.assertIn("tests.test_kuuos_self_organization_next_cycle_seed_v0_89", targets)
        self.assertIn("tests.test_kuuos_current_root_sequence_v0_89", targets)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("next-cycle-seed-v0-89", text)
        self.assertIn("current-root-sequence-v0-89", text)


if __name__ == "__main__":
    unittest.main()
