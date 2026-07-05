import unittest

from runtime.kuuos_manifest_index_v0_42 import (
    MANIFEST_ENTRIES,
    as_markdown,
    manifest_index_issues,
    manifest_paths,
    manifest_stages,
    verify_manifest_index,
)


class ManifestIndexV042Test(unittest.TestCase):
    def test_manifest_index_valid(self):
        self.assertEqual((), manifest_index_issues())
        self.assertTrue(verify_manifest_index())

    def test_manifest_paths_are_unique_json_files(self):
        self.assertEqual(len(manifest_paths()), len(set(manifest_paths())))
        for path in manifest_paths():
            self.assertTrue(path.startswith("manifests/"))
            self.assertTrue(path.endswith(".json"))

    def test_manifest_entries_are_small_metadata(self):
        for entry in MANIFEST_ENTRIES:
            self.assertLessEqual(entry.max_lines, 3)
            self.assertTrue(entry.depends_on)
            self.assertTrue(entry.role)

    def test_current_manifest_stage_is_present(self):
        self.assertIn("manifest-index-v0-42", set(manifest_stages()))

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("manifest-index-v0-42", text)
        self.assertIn("current-root-sequence-v0-41", text)


if __name__ == "__main__":
    unittest.main()
