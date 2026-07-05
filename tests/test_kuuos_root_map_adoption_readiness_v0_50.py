from __future__ import annotations

import unittest

from runtime import kuuos_root_map_adoption_proposal_v0_49 as proposal
from runtime import kuuos_root_map_adoption_readiness_v0_50 as readiness


class RootMapAdoptionReadinessV050Tests(unittest.TestCase):
    def test_version_and_dependency(self) -> None:
        self.assertEqual(readiness.VERSION, "kuuos_root_map_adoption_readiness_v0_50")
        self.assertEqual(readiness.DEPENDS_ON, proposal.VERSION)
        self.assertTrue(readiness.READ_ONLY)
        self.assertTrue(readiness.METADATA_ONLY)
        self.assertFalse(readiness.ADOPTION_PERFORMED)

    def test_required_checks_are_present(self) -> None:
        ids = set(readiness.check_ids())
        for check_id in readiness.REQUIRED_READINESS_CHECKS:
            self.assertIn(check_id, ids)

    def test_all_checks_pass(self) -> None:
        self.assertEqual(readiness.failed_checks(), ())
        self.assertEqual(set(readiness.passed_checks()), set(readiness.REQUIRED_READINESS_CHECKS))

    def test_readiness_verifies(self) -> None:
        self.assertEqual(readiness.readiness_issues(), ())
        self.assertTrue(readiness.verify_adoption_readiness())

    def test_markdown_names_no_automatic_adoption(self) -> None:
        markdown = readiness.as_markdown()
        self.assertIn("automatic_adoption_blocked", markdown)
        self.assertIn("future_stage_required", markdown)
        self.assertIn("mutation_authority_absent", markdown)


if __name__ == "__main__":
    unittest.main()
