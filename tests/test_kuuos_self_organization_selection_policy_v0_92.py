import json
import unittest

from runtime.kuuos_self_organization_selection_policy_v0_92 import (
    SELECTION_POLICY_PATH,
    expected_selection_policy,
    load_selection_policy,
    selection_policy_issues,
    selection_policy_json,
    verify_selection_policy,
)


class KuuOSSelfOrganizationSelectionPolicyV092Test(unittest.TestCase):
    def test_selection_policy_verifies(self):
        self.assertEqual((), selection_policy_issues())
        self.assertTrue(verify_selection_policy())

    def test_selection_policy_path(self):
        self.assertEqual("status/self_organization_selection_policy_v0_92.json", SELECTION_POLICY_PATH)

    def test_selection_policy_matches_expected(self):
        self.assertEqual(expected_selection_policy(), load_selection_policy())

    def test_selection_policy_json_round_trips(self):
        self.assertEqual(load_selection_policy(), json.loads(selection_policy_json()))

    def test_policy_only(self):
        policy = load_selection_policy()
        self.assertEqual("policy_only", policy["policy_mode"])
        self.assertFalse(policy["selection_authorized"])
        self.assertFalse(policy["effect_authorized"])
        self.assertIsNone(policy["selection_output"])
        self.assertEqual("lowest_expected_next_stage", policy["tie_breaker"])

    def test_next_stage_is_selected_next_action(self):
        policy = load_selection_policy()
        self.assertEqual("v0.93", policy["next_stage"])
        self.assertEqual("status/self_organization_selected_next_action_v0_93.json", policy["next_artifact"])


if __name__ == "__main__":
    unittest.main()
