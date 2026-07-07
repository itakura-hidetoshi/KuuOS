import json
import unittest

from runtime.kuuos_self_organization_candidate_queue_v0_90 import (
    CANDIDATE_QUEUE_PATH,
    candidate_queue_issues,
    candidate_queue_json,
    expected_candidate_ids,
    expected_candidate_queue,
    load_candidate_queue,
    verify_candidate_queue,
)


class KuuOSCandidateQueueV090Test(unittest.TestCase):
    def test_candidate_queue_verifies(self):
        self.assertEqual((), candidate_queue_issues())
        self.assertTrue(verify_candidate_queue())

    def test_candidate_queue_path(self):
        self.assertEqual("status/self_organization_candidate_queue_v0_90.json", CANDIDATE_QUEUE_PATH)

    def test_candidate_queue_matches_expected(self):
        self.assertEqual(expected_candidate_queue(), load_candidate_queue())

    def test_candidate_queue_json_round_trips(self):
        self.assertEqual(load_candidate_queue(), json.loads(candidate_queue_json()))

    def test_candidate_queue_names_next_receipt(self):
        queue = load_candidate_queue()
        self.assertEqual("candidate_queue_only", queue["queue_mode"])
        self.assertEqual("v0.91", queue["next_stage"])
        self.assertEqual("status/self_organization_candidate_receipt_v0_91.json", queue["next_artifact"])
        self.assertEqual(expected_candidate_ids(), queue["candidate_ids"])


if __name__ == "__main__":
    unittest.main()
