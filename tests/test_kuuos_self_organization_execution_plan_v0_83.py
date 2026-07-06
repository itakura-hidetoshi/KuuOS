import json
import unittest

from runtime.kuuos_self_organization_execution_plan_v0_83 import (
    EXECUTION_PLAN_PATH,
    execution_plan_issues,
    execution_plan_json,
    expected_execution_plan,
    load_execution_plan,
    verify_execution_plan,
)


class KuuOSExecutionPlanV083Test(unittest.TestCase):
    def test_execution_plan_verifies(self):
        self.assertEqual((), execution_plan_issues())
        self.assertTrue(verify_execution_plan())

    def test_execution_plan_path(self):
        self.assertEqual("status/self_organization_execution_plan_v0_83.json", EXECUTION_PLAN_PATH)

    def test_execution_plan_matches_expected(self):
        self.assertEqual(expected_execution_plan(), load_execution_plan())

    def test_execution_plan_json_round_trips(self):
        self.assertEqual(load_execution_plan(), json.loads(execution_plan_json()))

    def test_execution_plan_is_plan_only(self):
        plan = load_execution_plan()
        self.assertEqual("execution_plan_not_grant", plan["authority_boundary"])
        self.assertEqual("plan_only", plan["plan_mode"])
        self.assertFalse(plan["plan_enabled"])
        self.assertEqual("v0.84", plan["planned_next_stage"])


if __name__ == "__main__":
    unittest.main()
