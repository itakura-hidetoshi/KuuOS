import unittest

from runtime.kuuos_repository_frontier_summary_v0_40 import (
    SUMMARY_DOC,
    as_markdown,
    item_names,
    item_roots,
    summary_issues,
    verify_frontier_summary,
)


class RepositoryFrontierSummaryV040Test(unittest.TestCase):
    def test_frontier_summary_valid(self):
        self.assertEqual((), summary_issues())
        self.assertTrue(verify_frontier_summary())

    def test_summary_doc_is_in_docs(self):
        self.assertTrue(SUMMARY_DOC.startswith("docs/"))

    def test_expected_frontier_items_are_present(self):
        names = set(item_names())
        for name in (
            "closed-repository-mutation",
            "lifecycle-completion",
            "repository-index",
            "repository-structure-map",
            "repository-cleanup-proposals",
            "repository-frontier-summary",
        ):
            self.assertIn(name, names)

    def test_roots_are_explicit(self):
        roots = set(item_roots())
        self.assertIn("runtime/kuuos_v124_check.py", roots)
        self.assertIn("tests.test_kuuos_repository_cleanup_proposals_v0_39", roots)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("repository-frontier-summary", text)
        self.assertIn("closed-repository-mutation", text)


if __name__ == "__main__":
    unittest.main()
