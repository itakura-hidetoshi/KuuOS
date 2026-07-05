from __future__ import annotations

import unittest

from runtime import kuuos_root_map_adoption_proposal_v0_49 as proposal
from runtime import kuuos_root_map_next_review_v0_48 as review


class RootMapAdoptionProposalV049Tests(unittest.TestCase):
    def test_version_and_dependency(self) -> None:
        self.assertEqual(proposal.VERSION, "kuuos_root_map_adoption_proposal_v0_49")
        self.assertEqual(proposal.DEPENDS_ON, review.VERSION)
        self.assertTrue(proposal.READ_ONLY)
        self.assertTrue(proposal.METADATA_ONLY)

    def test_selected_review_is_from_next_review(self) -> None:
        self.assertEqual(proposal.SELECTED_REVIEW_ID, "status-to-next-review")
        self.assertTrue(proposal.selected_review_exists())
        self.assertTrue(proposal.selected_next_step_matches())

    def test_boundaries_include_review_boundaries(self) -> None:
        boundaries = set(proposal.proposal_boundaries())
        for boundary in review.REQUIRED_BOUNDARIES:
            self.assertIn(boundary, boundaries)
        self.assertIn("proposal_only", boundaries)
        self.assertIn("no_automatic_adoption", boundaries)
        self.assertIn("new_stage_required_for_adoption", boundaries)

    def test_proposal_verifies(self) -> None:
        self.assertEqual(proposal.proposal_issues(), ())
        self.assertTrue(proposal.verify_adoption_proposal())

    def test_markdown_names_selected_review(self) -> None:
        markdown = proposal.as_markdown()
        self.assertIn("root-map-adoption-proposal-v0-49", markdown)
        self.assertIn("status-to-next-review", markdown)
        self.assertIn("proposal_only", markdown)


if __name__ == "__main__":
    unittest.main()
