from __future__ import annotations

import unittest

from runtime import kuuos_bounded_steering_v0_55 as steering
from runtime import kuuos_root_map_deferral_closeout_v0_54 as closeout


class KuuOSBoundedSteeringV055Tests(unittest.TestCase):
    def test_version_and_dependency(self) -> None:
        self.assertEqual(steering.VERSION, "kuuos_bounded_steering_v0_55")
        self.assertEqual(steering.DEPENDS_ON, closeout.VERSION)
        self.assertTrue(steering.READ_ONLY)
        self.assertTrue(steering.METADATA_ONLY)
        self.assertTrue(steering.STEERING_ONLY)

    def test_required_steps_are_present(self) -> None:
        ids = set(steering.step_ids())
        for step_id in steering.REQUIRED_STEPS:
            self.assertIn(step_id, ids)

    def test_steering_verifies(self) -> None:
        self.assertEqual(steering.failed_steps(), ())
        self.assertEqual(steering.steering_issues(), ())
        self.assertTrue(steering.verify_bounded_steering())

    def test_markdown_names_gate_path(self) -> None:
        markdown = steering.as_markdown()
        self.assertIn("observe_frontier", markdown)
        self.assertIn("require_draft_pr", markdown)
        self.assertIn("require_gate_before_merge", markdown)


if __name__ == "__main__":
    unittest.main()
