from __future__ import annotations

import unittest

from runtime import kuuos_root_map_next_review_v0_48 as review
from runtime import kuuos_root_map_status_v0_47 as status


class RootMapNextReviewV048Tests(unittest.TestCase):
    def test_version_and_dependency(self) -> None:
        self.assertEqual(review.VERSION, "kuuos_root_map_next_review_v0_48")
        self.assertEqual(review.DEPENDS_ON, status.VERSION)
        self.assertTrue(review.READ_ONLY)
        self.assertTrue(review.METADATA_ONLY)

    def test_review_items_are_unique(self) -> None:
        self.assertEqual(len(review.review_ids()), len(set(review.review_ids())))
        self.assertEqual(len(review.next_steps()), len(set(review.next_steps())))

    def test_review_sources_are_known_status_rows(self) -> None:
        known_rows = set(status.row_ids())
        for row in review.source_rows():
            self.assertIn(row, known_rows)
        self.assertIn("status", review.source_rows())
        self.assertIn("ledger", review.source_rows())

    def test_required_boundaries_are_present(self) -> None:
        boundaries = set(review.all_boundaries())
        for boundary in review.REQUIRED_BOUNDARIES:
            self.assertIn(boundary, boundaries)

    def test_next_review_verifies(self) -> None:
        self.assertEqual(review.next_review_issues(), ())
        self.assertTrue(review.verify_next_review())

    def test_markdown_names_next_review(self) -> None:
        markdown = review.as_markdown()
        self.assertIn("status-to-next-review", markdown)
        self.assertIn("derive_next_read_only_metadata_candidate", markdown)
        self.assertIn("no_mutation_authority", markdown)


if __name__ == "__main__":
    unittest.main()
