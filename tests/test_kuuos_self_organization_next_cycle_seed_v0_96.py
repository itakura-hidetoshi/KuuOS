import json
import unittest

from runtime.kuuos_self_organization_next_cycle_seed_v0_96 import (
    NEXT_CYCLE_SEED_PATH,
    expected_next_cycle_seed,
    load_next_cycle_seed,
    next_cycle_seed_issues,
    next_cycle_seed_json,
    verify_next_cycle_seed,
)


class NextCycleSeedV096Test(unittest.TestCase):
    def test_valid(self):
        self.assertEqual((), next_cycle_seed_issues())
        self.assertTrue(verify_next_cycle_seed())

    def test_path(self):
        self.assertEqual("status/self_organization_next_cycle_seed_v0_96.json", NEXT_CYCLE_SEED_PATH)

    def test_expected(self):
        self.assertEqual(expected_next_cycle_seed(), load_next_cycle_seed())

    def test_json(self):
        self.assertEqual(load_next_cycle_seed(), json.loads(next_cycle_seed_json()))

    def test_fields(self):
        data = load_next_cycle_seed()
        self.assertEqual("next_cycle_seed_only", data["seed_mode"])
        self.assertEqual("status/self_organization_candidate_queue_v0_97.json", data["next_artifact"])
        self.assertEqual("v0.97", data["next_stage"])


if __name__ == "__main__":
    unittest.main()
