import json
import unittest

from runtime.kuuos_self_organization_bounded_change_plan_v0_101 import (
    BOUNDED_CHANGE_PLAN_PATH,
    bounded_change_plan_issues,
    bounded_change_plan_json,
    expected_bounded_change_plan,
    load_bounded_change_plan,
    verify_bounded_change_plan,
)


class BoundedChangePlanV0101Test(unittest.TestCase):
    def test_valid(self):
        self.assertEqual((), bounded_change_plan_issues())
        self.assertTrue(verify_bounded_change_plan())

    def test_path(self):
        self.assertEqual(
            "status/self_organization_bounded_change_plan_v0_101.json",
            BOUNDED_CHANGE_PLAN_PATH,
        )

    def test_expected(self):
        self.assertEqual(expected_bounded_change_plan(), load_bounded_change_plan())

    def test_json(self):
        self.assertEqual(load_bounded_change_plan(), json.loads(bounded_change_plan_json()))

    def test_fields(self):
        data = load_bounded_change_plan()
        self.assertEqual("bounded_change_plan_only", data["plan_mode"])
        self.assertFalse(data["plan_enabled"])
        self.assertEqual("bounded_change_plan_record_only", data["scope_boundary"])
        self.assertEqual("status/self_organization_completion_receipt_v0_102.json", data["planned_artifact"])
        self.assertEqual("v0.102", data["planned_next_stage"])


if __name__ == "__main__":
    unittest.main()
