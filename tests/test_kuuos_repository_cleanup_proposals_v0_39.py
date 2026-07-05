import unittest

from runtime.kuuos_repository_cleanup_proposals_v0_39 import (
    PROPOSALS,
    as_markdown,
    proposal_issues,
    target_zones,
    verify_cleanup_proposals,
)


class RepositoryCleanupProposalsV039Test(unittest.TestCase):
    def test_cleanup_proposals_valid(self):
        self.assertEqual((), proposal_issues())
        self.assertTrue(verify_cleanup_proposals())

    def test_no_move_or_delete_actions(self):
        for proposal in PROPOSALS:
            self.assertNotIn(proposal.action_kind, {"move-file", "delete-file"})
            self.assertTrue(proposal.forbidden_effects)

    def test_core_zones_have_proposals(self):
        zones = set(target_zones())
        self.assertIn("runtime/", zones)
        self.assertIn("docs/", zones)
        self.assertIn("manifests/", zones)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("docs-status-frontier-summary", text)
        self.assertIn("runtime-current-root-commentary", text)


if __name__ == "__main__":
    unittest.main()
