import json
import unittest

from runtime.kuuos_self_organization_next_cycle_seed_v0_89 import (
    NEXT_CYCLE_SEED_PATH,
    expected_next_cycle_seed,
    load_next_cycle_seed,
    next_cycle_seed_issues,
    next_cycle_seed_json,
    verify_next_cycle_seed,
)


class KuuOSNextCycleSeedV089Test(unittest.TestCase):
    def test_next_cycle_seed_verifies(self):
        self.assertEqual((), next_cycle_seed_issues())
        self.assertTrue(verify_next_cycle_seed())

    def test_next_cycle_seed_path(self):
        self.assertEqual("status/self_organization_next_cycle_seed_v0_89.json", NEXT_CYCLE_SEED_PATH)

    def test_next_cycle_seed_matches_expected(self):
        self.assertEqual(expected_next_cycle_seed(), load_next_cycle_seed())

    def test_next_cycle_seed_json_round_trips(self):
        self.assertEqual(load_next_cycle_seed(), json.loads(next_cycle_seed_json()))

    def test_next_cycle_seed_names_queue(self):
        seed = load_next_cycle_seed()
        self.assertEqual("next_cycle_seed_only", seed["seed_mode"])
        self.assertEqual("v0.90", seed["next_stage"])
        self.assertEqual("status/self_organization_candidate_queue_v0_90.json", seed["next_artifact"])
        self.assertEqual("status/self_organization_completion_receipt_v0_88.json", seed["source_receipt"])


if __name__ == "__main__":
    unittest.main()
