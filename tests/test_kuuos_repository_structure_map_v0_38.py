import unittest

from runtime.kuuos_repository_structure_map_v0_38 import (
    DIRECTORY_ZONES,
    as_markdown,
    structure_issues,
    verify_repository_structure_map,
    zone_paths,
)


class RepositoryStructureMapV038Test(unittest.TestCase):
    def test_structure_map_valid(self):
        self.assertEqual((), structure_issues())
        self.assertTrue(verify_repository_structure_map())

    def test_required_zones_are_present(self):
        paths = set(zone_paths())
        for path in ("runtime/", "tests/", "formal/", "docs/", "manifests/", "ci/check_registry.d/"):
            self.assertIn(path, paths)

    def test_runtime_and_docs_boundaries_are_separate(self):
        runtime_zone = next(zone for zone in DIRECTORY_ZONES if zone.path == "runtime/")
        docs_zone = next(zone for zone in DIRECTORY_ZONES if zone.path == "docs/")
        self.assertIn("pure Python runtime modules", runtime_zone.accepts)
        self.assertIn("long-form design prose", runtime_zone.rejects)
        self.assertIn("status notes", docs_zone.accepts)

    def test_markdown_summary(self):
        text = as_markdown()
        self.assertIn("runtime/", text)
        self.assertIn("formal/", text)
        self.assertIn("docs/", text)


if __name__ == "__main__":
    unittest.main()
