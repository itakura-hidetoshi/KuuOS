import json
import unittest

from runtime.kuuos_self_organization_candidate_receipt_v0_112 import (
    CANDIDATE_RECEIPT_PATH,
    candidate_receipt_issues,
    candidate_receipt_json,
    expected_candidate_receipt,
    expected_received_candidate_ids,
    load_candidate_receipt,
    verify_candidate_receipt,
)


class CandidateReceiptV0112Test(unittest.TestCase):
    def test_valid(self):
        self.assertEqual((), candidate_receipt_issues())
        self.assertTrue(verify_candidate_receipt())

    def test_path(self):
        self.assertEqual(
            "status/self_organization_candidate_receipt_v0_112.json",
            CANDIDATE_RECEIPT_PATH,
        )

    def test_expected(self):
        self.assertEqual(expected_candidate_receipt(), load_candidate_receipt())

    def test_json(self):
        self.assertEqual(load_candidate_receipt(), json.loads(candidate_receipt_json()))

    def test_received_candidate_ids(self):
        self.assertEqual(
            [
                "candidate-receipt-v0-112",
                "selection-policy-v0-113",
                "selected-next-action-v0-114",
                "bounded-change-plan-v0-115",
            ],
            expected_received_candidate_ids(),
        )
        self.assertEqual(4, load_candidate_receipt()["received_candidate_count"])

    def test_next_pointer(self):
        data = load_candidate_receipt()
        self.assertEqual("candidate_receipt_only", data["receipt_mode"])
        self.assertEqual("self_organization_next_cycle", data["receipt_scope"])
        self.assertEqual("status/self_organization_selection_policy_v0_113.json", data["next_artifact"])
        self.assertEqual("v0.113", data["next_stage"])


if __name__ == "__main__":
    unittest.main()
