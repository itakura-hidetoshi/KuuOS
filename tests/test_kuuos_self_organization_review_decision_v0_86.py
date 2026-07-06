import json
import unittest

from runtime.kuuos_self_organization_review_decision_v0_86 import (
    REVIEW_DECISION_PATH,
    expected_review_decision,
    load_review_decision,
    review_decision_issues,
    review_decision_json,
    verify_review_decision,
)


class KuuOSReviewDecisionV086Test(unittest.TestCase):
    def test_review_decision_verifies(self):
        self.assertEqual((), review_decision_issues())
        self.assertTrue(verify_review_decision())

    def test_review_decision_path(self):
        self.assertEqual("status/self_organization_review_decision_v0_86.json", REVIEW_DECISION_PATH)

    def test_review_decision_matches_expected(self):
        self.assertEqual(expected_review_decision(), load_review_decision())

    def test_review_decision_json_round_trips(self):
        self.assertEqual(load_review_decision(), json.loads(review_decision_json()))

    def test_review_decision_is_record_only(self):
        decision = load_review_decision()
        self.assertEqual("review_decision_not_grant", decision["authority_boundary"])
        self.assertEqual("decision_record_only", decision["decision_mode"])
        self.assertEqual("v0.87", decision["next_request_stage"])
        self.assertEqual("status/self_organization_review_packet_v0_85.json", decision["source_packet"])


if __name__ == "__main__":
    unittest.main()
