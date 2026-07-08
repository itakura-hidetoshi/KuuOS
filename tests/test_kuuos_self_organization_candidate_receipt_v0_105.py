import json
import unittest

from runtime.kuuos_self_organization_candidate_receipt_v0_105 import (
    CANDIDATE_RECEIPT_PATH,
    candidate_receipt_issues,
    candidate_receipt_json,
    expected_candidate_receipt,
    load_candidate_receipt,
    verify_candidate_receipt,
)


class CandidateReceiptV0105Test(unittest.TestCase):
    def test_valid(self):
        self.assertEqual((), candidate_receipt_issues())
        self.assertTrue(verify_candidate_receipt())

    def test_path(self):
        self.assertEqual(
            "status/self_organization_candidate_receipt_v0_105.json",
            CANDIDATE_RECEIPT_PATH,
        )

    def test_expected(self):
        self.assertEqual(expected_candidate_receipt(), load_candidate_receipt())

    def test_json(self):
        self.assertEqual(load_candidate_receipt(), json.loads(candidate_receipt_json()))

    def test_receipt_fields(self):
        data = load_candidate_receipt()
        self.assertEqual("candidate_receipt_only", data["receipt_mode"])
        self.assertEqual("self_organization_next_cycle", data["receipt_scope"])
        self.assertFalse(data["selection_authorized"])
        self.assertEqual("status/self_organization_selection_policy_v0_106.json", data["next_artifact"])
        self.assertEqual("v0.106", data["next_stage"])


if __name__ == "__main__":
    unittest.main()
