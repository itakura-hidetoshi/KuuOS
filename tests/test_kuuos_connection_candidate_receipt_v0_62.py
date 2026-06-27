import unittest

from runtime.kuuos_connection_candidate_receipt_v0_62 import ConnectionCandidatePolicy, evaluate_connection_candidate
from tests.kuuos_connection_candidate_fixture_v0_62 import fixture


class ConnectionCandidateReceiptV062Tests(unittest.TestCase):
    def test_change_budget_is_enforced(self):
        bundle, flat, _ = fixture()
        policy = ConnectionCandidatePolicy(max_changed_links=1)
        receipt = evaluate_connection_candidate(bundle, flat, policy=policy)
        self.assertFalse(receipt.admissible)
        self.assertIn("connection_change_budget_exceeded", receipt.blockers)


if __name__ == "__main__":
    unittest.main()
