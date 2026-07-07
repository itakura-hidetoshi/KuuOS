import json
import unittest

from runtime.kuuos_self_organization_candidate_receipt_v0_91 import (
    CANDIDATE_RECEIPT_PATH,
    candidate_receipt_issues,
    candidate_receipt_json,
    expected_candidate_receipt,
    load_candidate_receipt,
    verify_candidate_receipt,
)


class KuuOSCandidateReceiptV091Test(unittest.TestCase):
    def test_receipt_verifies(self):
        self.assertEqual((), candidate_receipt_issues())
        self.assertTrue(verify_candidate_receipt())

    def test_receipt_path(self):
        self.assertEqual("status/self_organization_candidate_receipt_v0_91.json", CANDIDATE_RECEIPT_PATH)

    def test_receipt_matches_expected(self):
        self.assertEqual(expected_candidate_receipt(), load_candidate_receipt())

    def test_receipt_json_round_trips(self):
        self.assertEqual(load_candidate_receipt(), json.loads(candidate_receipt_json()))

    def test_receipt_next_stage(self):
        receipt = load_candidate_receipt()
        self.assertEqual("candidate_receipt_only", receipt["receipt_mode"])
        self.assertFalse(receipt["selection_authorized"])
        self.assertEqual("v0.92", receipt["next_stage"])
        self.assertEqual("status/self_organization_selection_policy_v0_92.json", receipt["next_artifact"])


if __name__ == "__main__":
    unittest.main()
