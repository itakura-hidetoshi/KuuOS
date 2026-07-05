from __future__ import annotations

import unittest

from runtime import kuuos_root_map_adoption_readiness_v0_50 as readiness
from runtime import kuuos_root_map_pre_adoption_review_v0_51 as review


class RootMapPreAdoptionReviewV051Tests(unittest.TestCase):
    def test_version_and_dependency(self) -> None:
        self.assertEqual(review.VERSION, "kuuos_root_map_pre_adoption_review_v0_51")
        self.assertEqual(review.DEPENDS_ON, readiness.VERSION)
        self.assertTrue(review.READ_ONLY)
        self.assertTrue(review.METADATA_ONLY)
        self.assertFalse(review.ADOPTION_AUTHORIZED)

    def test_required_items_are_present(self) -> None:
        ids = set(review.review_item_ids())
        for item_id in review.REQUIRED_REVIEW_ITEMS:
            self.assertIn(item_id, ids)

    def test_all_review_items_pass(self) -> None:
        self.assertEqual(review.failed_review_items(), ())
        self.assertEqual(set(review.passed_review_items()), set(review.REQUIRED_REVIEW_ITEMS))

    def test_pre_adoption_review_verifies(self) -> None:
        self.assertEqual(review.pre_adoption_review_issues(), ())
        self.assertTrue(review.verify_pre_adoption_review())

    def test_markdown_names_future_governance(self) -> None:
        markdown = review.as_markdown()
        self.assertIn("confirm_future_governance_required", markdown)
        self.assertIn("confirm_no_adoption_performed", markdown)
        self.assertIn("confirm_mutation_authority_absent", markdown)


if __name__ == "__main__":
    unittest.main()
