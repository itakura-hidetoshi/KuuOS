import json
import unittest

from runtime.kuuos_self_organization_selected_next_action_v0_107 import (
    SELECTED_NEXT_ACTION_PATH,
    expected_selected_candidate_id,
    expected_selected_next_action,
    load_selected_next_action,
    selected_next_action_issues,
    selected_next_action_json,
    verify_selected_next_action,
)


class SelectedNextActionV0107Test(unittest.TestCase):
    def test_valid(self):
        self.assertEqual((), selected_next_action_issues())
        self.assertTrue(verify_selected_next_action())

    def test_path(self):
        self.assertEqual(
            "status/self_organization_selected_next_action_v0_107.json",
            SELECTED_NEXT_ACTION_PATH,
        )

    def test_expected(self):
        self.assertEqual(expected_selected_next_action(), load_selected_next_action())

    def test_json(self):
        self.assertEqual(load_selected_next_action(), json.loads(selected_next_action_json()))

    def test_selected_candidate(self):
        data = load_selected_next_action()
        self.assertEqual("bounded-change-plan-v0-108", expected_selected_candidate_id())
        self.assertEqual("bounded-change-plan-v0-108", data["selected_candidate_id"])
        self.assertEqual("bounded_change_plan_only", data["selected_candidate_scope"])
        self.assertEqual("v0.108", data["selected_next_stage"])
        self.assertEqual("status/self_organization_bounded_change_plan_v0_108.json", data["next_artifact"])
        self.assertEqual("v0.108", data["next_stage"])

    def test_selection_boundary(self):
        data = load_selected_next_action()
        self.assertEqual("selection_only", data["selection_mode"])
        self.assertFalse(data["effect_enabled"])
        self.assertEqual("selected_next_action_not_grant", data["authority_boundary"])


if __name__ == "__main__":
    unittest.main()
