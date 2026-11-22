from __future__ import annotations

import unittest

from runtime import kuuos_root_map_closeout_observation_v0_55 as observation
from runtime import kuuos_root_map_deferral_closeout_v0_54 as closeout


class RootMapCloseoutObservationV055Tests(unittest.TestCase):
    def test_version_and_dependency(self) -> None:
        self.assertEqual(observation.VERSION, "kuuos_root_map_closeout_observation_v0_55")
        self.assertEqual(observation.DEPENDS_ON, closeout.VERSION)
        self.assertTrue(observation.READ_ONLY)
        self.assertTrue(observation.METADATA_ONLY)
        self.assertTrue(observation.OBSERVATION_ONLY)
        self.assertFalse(observation.FOLLOWUP_CREATED)

    def test_required_items_are_present(self) -> None:
        ids = set(observation.observation_item_ids())
        for item_id in observation.REQUIRED_OBSERVATION_ITEMS:
            self.assertIn(item_id, ids)

    def test_all_observation_items_pass(self) -> None:
        self.assertEqual(observation.failed_observation_items(), ())

    def test_observation_verifies(self) -> None:
        self.assertEqual(observation.observation_issues(), ())
        self.assertTrue(observation.verify_closeout_observation())

    def test_markdown_names_stable_record(self) -> None:
        markdown = observation.as_markdown()
        self.assertIn("closeout_verified", markdown)
        self.assertIn("followup_not_created", markdown)
        self.assertIn("stable_closeout_record", markdown)


if __name__ == "__main__":
    unittest.main()
