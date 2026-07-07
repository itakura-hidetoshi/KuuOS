import json
import unittest

from runtime.kuuos_self_organization_completion_receipt_v0_102 import (
    COMPLETION_RECEIPT_PATH,
    completion_receipt_issues,
    completion_receipt_json,
    expected_completion_receipt,
    load_completion_receipt,
    verify_completion_receipt,
)


class CompletionReceiptV0102Test(unittest.TestCase):
    def test_valid(self):
        self.assertEqual((), completion_receipt_issues())
        self.assertTrue(verify_completion_receipt())

    def test_path(self):
        self.assertEqual(
            "status/self_organization_completion_receipt_v0_102.json",
            COMPLETION_RECEIPT_PATH,
        )

    def test_expected(self):
        self.assertEqual(expected_completion_receipt(), load_completion_receipt())

    def test_json(self):
        self.assertEqual(load_completion_receipt(), json.loads(completion_receipt_json()))

    def test_fields(self):
        data = load_completion_receipt()
        self.assertEqual("completion_receipt_only", data["receipt_mode"])
        self.assertEqual("v0.101", data["completed_stage"])
        self.assertEqual("status/self_organization_next_cycle_seed_v0_103.json", data["next_artifact"])
        self.assertEqual("v0.103", data["next_stage"])


if __name__ == "__main__":
    unittest.main()
