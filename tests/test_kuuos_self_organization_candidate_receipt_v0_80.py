import json
import unittest

from runtime.kuuos_self_organization_candidate_receipt_v0_80 import (
    CANDIDATE_RECEIPT_PATH,
    candidate_receipt_issues,
    candidate_receipt_json,
    expected_candidate_receipt,
    load_candidate_receipt,
    verify_candidate_receipt,
)


class KuuOSSelfOrganizationCandidateReceiptV080Test(unittest.TestCase):
    def test_candidate_receipt_verifies(self):
        self.assertEqual((), candidate_receipt_issues())
        self.assertTrue(verify_candidate_receipt())

    def test_candidate_receipt_path(self):
        self.assertEqual("status/self_organization_candidate_receipt_v0_80.json", CANDIDATE_RECEIPT_PATH)

    def test_candidate_receipt_matches_expected(self):
        self.assertEqual(expected_candidate_receipt(), load_candidate_receipt())

    def test_candidate_receipt_json_round_trips(self):
        self.assertEqual(load_candidate_receipt(), json.loads(candidate_receipt_json()))

    def test_candidate_receipt_records_queue(self):
        receipt = load_candidate_receipt()
        self.assertEqual("queue_receipt_only", receipt["receipt_mode"])
        self.assertEqual("status/self_organization_candidate_queue_v0_79.json", receipt["candidate_queue"])
        self.assertEqual(4, receipt["candidate_count"])


if __name__ == "__main__":
    unittest.main()
