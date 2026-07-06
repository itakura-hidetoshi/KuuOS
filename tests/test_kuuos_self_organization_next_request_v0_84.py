import json
import unittest

from runtime.kuuos_self_organization_next_request_v0_84 import (
    ITEM_PATH,
    expected_item,
    item_issues,
    item_json,
    load_item,
    verify_item,
)


class KuuOSNextRequestV084Test(unittest.TestCase):
    def test_next_request_verifies(self):
        self.assertEqual((), item_issues())
        self.assertTrue(verify_item())

    def test_next_request_path(self):
        self.assertEqual("status/self_organization_next_request_v0_84.json", ITEM_PATH)

    def test_next_request_matches_expected(self):
        self.assertEqual(expected_item(), load_item())

    def test_next_request_json_round_trips(self):
        self.assertEqual(load_item(), json.loads(item_json()))

    def test_next_request_is_request_only(self):
        item = load_item()
        self.assertEqual("next_request_not_grant", item["authority_boundary"])
        self.assertEqual("request_only", item["request_mode"])
        self.assertEqual("v0.85", item["requested_next_stage"])
        self.assertEqual("status/self_organization_execution_plan_v0_83.json", item["plan"])


if __name__ == "__main__":
    unittest.main()
