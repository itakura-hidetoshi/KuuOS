import json
import unittest

from runtime.kuuos_self_organization_selected_next_action_v0_93 import (
    SELECTED_NEXT_ACTION_PATH,
    expected_selected_candidate_id,
    expected_selected_next_action,
    load_selected_next_action,
    selected_next_action_issues,
    selected_next_action_json,
    verify_selected_next_action,
)


class KuuOSSelfOrganizationSelectedNextActionV093Test(unittest.TestCase):
    def test_selected_next_action_verifies(self):
        self.assertEqual((), selected_next_action_issues())
        self.assertTrue(verify_selected_next_action())

    def test_selected_next_action_path(self):
        self.assertEqual(
            "status/self_organization_selected_next_action_v0_93.json",
            SELECTED_NEXT_ACTION_PATH,
        )

    def test_selected_next_action_matches_expected(self):
        self.assertEqual(expected_selected_next_action(), load_selected_next_action())

    def test_selected_next_action_json_round_trips(self):
        self.assertEqual(load_selected_next_action(), json.loads(selected_next_action_json()))

    def test_selected_candidate(self):
        self.assertEqual("bounded-change-plan-v0-94", expected_selected_candidate_id())
        selected = load_selected_next_action()
        self.assertEqual("bounded-change-plan-v0-94", selected["selected_candidate_id"])
        self.assertEqual("bounded_change_plan_only", selected["selected_candidate_scope"])
        self.assertEqual("v0.94", selected["selected_next_stage"])

    def test_selection_only(self):
        selected = load_selected_next_action()
        self.assertEqual("selection_only", selected["selection_mode"])
        self.assertFalse(selected["effect_enabled"])
        self.assertEqual("selected_next_action_not_grant", selected["authority_boundary"])
        self.assertEqual("status/self_organization_bounded_change_plan_v0_94.json", selected["next_artifact"])


if __name__ == "__main__":
    unittest.main()
