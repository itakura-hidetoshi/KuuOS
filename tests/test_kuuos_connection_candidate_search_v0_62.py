import unittest

from runtime.kuuos_connection_candidate_search_v0_62 import search_connection_candidates
from tests.kuuos_connection_candidate_fixture_v0_62 import fixture


class ConnectionCandidateSearchV062(unittest.TestCase):
    def test_search_selects_flat_candidate(self):
        bundle, flat, _ = fixture()
        identity = bundle.group.identity()
        proposal = search_connection_candidates(bundle, {
            ("observe", "verify"): [identity],
            ("verify", "memory"): [identity],
        })
        self.assertEqual(proposal.route, "PROPOSE_CONNECTION_UPDATE")
        self.assertEqual(proposal.evaluated_candidates, 4)
        self.assertIsNotNone(proposal.selected_receipt)
        self.assertIsNotNone(proposal.selected_connection)
        self.assertEqual(proposal.selected_receipt.candidate_curvature.total_curvature, 0.0)
        self.assertEqual(proposal.selected_connection.to_dict(), flat.to_dict())
        self.assertFalse(proposal.state_write_performed)

    def test_empty_catalog_preserves_source(self):
        bundle, _, _ = fixture()
        proposal = search_connection_candidates(bundle, {})
        self.assertEqual(proposal.route, "PRESERVE_SOURCE_CONNECTION")
        self.assertEqual(proposal.evaluated_candidates, 1)
        self.assertEqual(proposal.admissible_candidates, 0)
        self.assertIsNone(proposal.selected_connection)


if __name__ == "__main__":
    unittest.main()
