import json
import unittest

from runtime.kuuos_self_organization_selection_policy_v0_113 import (
    SELECTION_POLICY_PATH,
    expected_selection_policy,
    load_selection_policy,
    selection_policy_issues,
    selection_policy_json,
    verify_selection_policy,
)


class SelectionPolicyV0113Test(unittest.TestCase):
    def test_valid(self):
        self.assertEqual((), selection_policy_issues())
        self.assertTrue(verify_selection_policy())

    def test_path(self):
        self.assertEqual(
            "status/self_organization_selection_policy_v0_113.json",
            SELECTION_POLICY_PATH,
        )

    def test_expected(self):
        self.assertEqual(expected_selection_policy(), load_selection_policy())

    def test_json(self):
        self.assertEqual(load_selection_policy(), json.loads(selection_policy_json()))

    def test_selected_candidate(self):
        data = load_selection_policy()
        self.assertEqual("selection-policy-v0-113", data["selected_candidate_id"])
        self.assertEqual("selection_policy_only", data["policy_mode"])
        self.assertEqual("self_organization_next_cycle", data["policy_scope"])

    def test_next_pointer(self):
        data = load_selection_policy()
        self.assertEqual("status/self_organization_selected_next_action_v0_114.json", data["next_artifact"])
        self.assertEqual("v0.114", data["next_stage"])


if __name__ == "__main__":
    unittest.main()
