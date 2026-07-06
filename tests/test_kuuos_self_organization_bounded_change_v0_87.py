import json
import unittest

from runtime.kuuos_self_organization_bounded_change_v0_87 import (
    BOUNDED_CHANGE_PATH,
    bounded_change_issues,
    bounded_change_json,
    expected_bounded_change,
    load_bounded_change,
    verify_bounded_change,
)


class KuuOSBoundedChangeV087Test(unittest.TestCase):
    def test_bounded_change_verifies(self):
        self.assertEqual((), bounded_change_issues())
        self.assertTrue(verify_bounded_change())

    def test_bounded_change_path(self):
        self.assertEqual("status/self_organization_bounded_change_v0_87.json", BOUNDED_CHANGE_PATH)

    def test_bounded_change_matches_expected(self):
        self.assertEqual(expected_bounded_change(), load_bounded_change())

    def test_bounded_change_json_round_trips(self):
        self.assertEqual(load_bounded_change(), json.loads(bounded_change_json()))

    def test_bounded_change_closes_review_loop(self):
        bounded = load_bounded_change()
        self.assertEqual("bounded_repository_change", bounded["change_mode"])
        self.assertTrue(bounded["review_loop_closed"])
        self.assertEqual("self_organization_current_root_artifact", bounded["change_scope"])
        self.assertEqual("v0.88", bounded["next_stage"])


if __name__ == "__main__":
    unittest.main()
