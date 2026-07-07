import json
import unittest

from runtime.kuuos_self_organization_candidate_queue_v0_104 import (
    CANDIDATE_QUEUE_PATH,
    candidate_queue_issues,
    candidate_queue_json,
    expected_candidate_ids,
    expected_candidate_queue,
    load_candidate_queue,
    verify_candidate_queue,
)


class CandidateQueueV0104Test(unittest.TestCase):
    def test_valid(self):
        self.assertEqual((), candidate_queue_issues())
        self.assertTrue(verify_candidate_queue())

    def test_path(self):
        self.assertEqual(
            "status/self_organization_candidate_queue_v0_104.json",
            CANDIDATE_QUEUE_PATH,
        )

    def test_expected(self):
        self.assertEqual(expected_candidate_queue(), load_candidate_queue())

    def test_json(self):
        self.assertEqual(load_candidate_queue(), json.loads(candidate_queue_json()))

    def test_candidate_ids(self):
        self.assertEqual(
            [
                "candidate-receipt-v0-105",
                "selection-policy-v0-106",
                "selected-next-action-v0-107",
                "bounded-change-plan-v0-108",
            ],
            expected_candidate_ids(),
        )
        self.assertEqual(4, load_candidate_queue()["candidate_count"])

    def test_next_pointer(self):
        data = load_candidate_queue()
        self.assertEqual("candidate_queue_only", data["queue_mode"])
        self.assertEqual("self_organization_next_cycle", data["queue_scope"])
        self.assertEqual("status/self_organization_candidate_receipt_v0_105.json", data["next_artifact"])
        self.assertEqual("v0.105", data["next_stage"])


if __name__ == "__main__":
    unittest.main()
