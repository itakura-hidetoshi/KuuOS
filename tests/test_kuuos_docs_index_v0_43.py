import unittest

from runtime.kuuos_docs_index_v0_43 import (
    DOCS_ENTRIES,
    as_markdown,
    doc_ids,
    doc_paths,
    docs_index_issues,
    verify_docs_index,
)


class DocsIndexV043Test(unittest.TestCase):
    def test_docs_index_valid(self):
        self.assertEqual((), docs_index_issues())
        self.assertTrue(verify_docs_index())

    def test_doc_paths_are_unique_markdown_files(self):
        self.assertEqual(len(doc_paths()), len(set(doc_paths())))
        for path in doc_paths():
            self.assertTrue(path.startswith("docs/"))
            self.assertTrue(path.endswith(".md"))

    def test_entries_have_roles_and_owner_lines(self):
        for entry in DOCS_ENTRIES:
            self.assertTrue(entry.role)
            self.assertTrue(entry.owner_line)

    def test_current_doc_entry_is_present(self):
        self.assertIn("docs-index-v0-43", set(doc_ids()))

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("docs-index-v0-43", text)
        self.assertIn("manifest-index-v0-42", text)


if __name__ == "__main__":
    unittest.main()
