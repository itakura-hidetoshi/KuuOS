import json
import unittest

from runtime.kuuos_self_organization_bounded_change_plan_v0_94 import (
    BOUNDED_CHANGE_PLAN_PATH,
    bounded_change_plan_issues,
    bounded_change_plan_json,
    expected_bounded_change_plan,
    load_bounded_change_plan,
    verify_bounded_change_plan,
)


class KuuOSSelfOrganizationBoundedChangePlanV094Test(unittest.TestCase):
    def test_bounded_change_plan_verifies(self):
        self.assertEqual((), bounded_change_plan_issues())
        self.assertTrue(verify_bounded_change_plan())

    def test_bounded_change_plan_path(self):
        self.assertEqual(
            "status/self_organization_bounded_change_plan_v0_94.json",
            BOUNDED_CHANGE_PLAN_PATH,
        )

    def test_bounded_change_plan_matches_expected(self):
        self.assertEqual(expected_bounded_change_plan(), load_bounded_change_plan())

    def test_bounded_change_plan_json_round_trips(self):
        self.assertEqual(load_bounded_change_plan(), json.loads(bounded_change_plan_json()))

    def test_plan_only(self):
        plan = load_bounded_change_plan()
        self.assertEqual("bounded_change_plan_only", plan["plan_mode"])
        self.assertFalse(plan["plan_enabled"])
        self.assertEqual("bounded_change_plan_not_grant", plan["authority_boundary"])
        self.assertEqual("bounded_change_plan_record_only", plan["scope_boundary"])

    def test_planned_next_stage(self):
        plan = load_bounded_change_plan()
        self.assertEqual("v0.95", plan["planned_next_stage"])
        self.assertEqual("status/self_organization_completion_receipt_v0_95.json", plan["planned_artifact"])
        self.assertEqual("runtime/kuuos_self_organization_completion_receipt_v0_95.py", plan["planned_runtime"])


if __name__ == "__main__":
    unittest.main()
