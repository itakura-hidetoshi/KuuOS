import json
import unittest

from runtime.kuuos_self_organization_completion_receipt_v0_88 import (
    COMPLETION_RECEIPT_PATH,
    completion_receipt_issues,
    completion_receipt_json,
    expected_completion_receipt,
    load_completion_receipt,
    verify_completion_receipt,
)


class KuuOSCompletionReceiptV088Test(unittest.TestCase):
    def test_completion_receipt_verifies(self):
        self.assertEqual((), completion_receipt_issues())
        self.assertTrue(verify_completion_receipt())

    def test_completion_receipt_path(self):
        self.assertEqual("status/self_organization_completion_receipt_v0_88.json", COMPLETION_RECEIPT_PATH)

    def test_completion_receipt_matches_expected(self):
        self.assertEqual(expected_completion_receipt(), load_completion_receipt())

    def test_completion_receipt_json_round_trips(self):
        self.assertEqual(load_completion_receipt(), json.loads(completion_receipt_json()))

    def test_completion_receipt_records_completed_stage(self):
        receipt = load_completion_receipt()
        self.assertEqual("completion_receipt_only", receipt["receipt_mode"])
        self.assertEqual("v0.87", receipt["completed_stage"])
        self.assertEqual("v0.89", receipt["next_stage"])
        self.assertEqual("status/self_organization_bounded_change_v0_87.json", receipt["source_bounded_change"])


if __name__ == "__main__":
    unittest.main()
