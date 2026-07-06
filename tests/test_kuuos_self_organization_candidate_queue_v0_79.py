import json
import unittest

from runtime.kuuos_self_organization_candidate_queue_v0_79 import (
    CANDIDATE_QUEUE_PATH,
    candidate_queue_issues,
    candidate_queue_json,
    expected_candidate_queue,
    load_candidate_queue,
    verify_candidate_queue,
)


class KuuOSSelfOrganizationCandidateQueueV079Test(unittest.TestCase):
    def test_candidate_queue_verifies(self):
        self.assertEqual((), candidate_queue_issues())
        self.assertTrue(verify_candidate_queue())

    def test_candidate_queue_path(self):
        self.assertEqual("status/self_organization_candidate_queue_v0_79.json", CANDIDATE_QUEUE_PATH)

    def test_candidate_queue_matches_expected(self):
        self.assertEqual(expected_candidate_queue(), load_candidate_queue())

    def test_candidate_queue_json_round_trips(self):
        self.assertEqual(load_candidate_queue(), json.loads(candidate_queue_json()))

    def test_candidates_are_proposal_only(self):
        queue = load_candidate_queue()
        self.assertEqual("candidate_queue_not_authority_grant", queue["authority_boundary"])
        self.assertEqual("proposal_only", queue["generation_mode"])
        self.assertEqual("status/current.surface.index.json", queue["derived_from"])
        self.assertEqual("runtime/kuuos_current_surface.py", queue["stable_current_surface_cli"])
        candidate_ids = {candidate["candidate_id"] for candidate in queue["candidates"]}
        self.assertIn("candidate-receipt-v0-80", candidate_ids)
        self.assertIn("selection-policy-v0-81", candidate_ids)
        self.assertIn("selected-next-action-v0-82", candidate_ids)
        self.assertIn("execution-plan-v0-83", candidate_ids)


if __name__ == "__main__":
    unittest.main()
