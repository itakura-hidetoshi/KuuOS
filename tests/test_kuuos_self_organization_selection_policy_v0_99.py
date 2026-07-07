import json
import unittest

from runtime.kuuos_self_organization_selection_policy_v0_99 import (
    SELECTION_POLICY_PATH,
    expected_selection_policy,
    load_selection_policy,
    selection_policy_issues,
    selection_policy_json,
    verify_selection_policy,
)


class SelectionPolicyV099Test(unittest.TestCase):
    def test_valid(self):
        self.assertEqual((), selection_policy_issues())
        self.assertTrue(verify_selection_policy())

    def test_path(self):
        self.assertEqual("status/self_organization_selection_policy_v0_99.json", SELECTION_POLICY_PATH)

    def test_expected(self):
        self.assertEqual(expected_selection_policy(), load_selection_policy())

    def test_json(self):
        self.assertEqual(load_selection_policy(), json.loads(selection_policy_json()))

    def test_policy_only(self):
        data = load_selection_policy()
        self.assertEqual("policy_only", data["policy_mode"])
        self.assertFalse(data["effect_authorized"])
        self.assertFalse(data["selection_authorized"])
        self.assertIsNone(data["selection_output"])

    def test_next_pointer(self):
        data = load_selection_policy()
        self.assertEqual("status/self_organization_selected_next_action_v0_100.json", data["next_artifact"])
        self.assertEqual("v0.100", data["next_stage"])


if __name__ == "__main__":
    unittest.main()
