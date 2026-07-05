from __future__ import annotations

import unittest

from runtime import kuuos_root_map_v0_45 as root_map


class RootMapV045Tests(unittest.TestCase):
    def test_version_and_dependency(self) -> None:
        self.assertEqual(root_map.VERSION, "kuuos_root_map_v0_45")
        self.assertEqual(root_map.DEPENDS_ON, "kuuos_overview_index_v0_44")
        self.assertEqual(root_map.CURRENT_CHECK, "runtime/kuuos_current_check.py")

    def test_nodes_are_unique(self) -> None:
        self.assertEqual(len(root_map.node_ids()), len(set(root_map.node_ids())))
        self.assertEqual(len(root_map.node_paths()), len(set(root_map.node_paths())))

    def test_nodes_include_current_layers(self) -> None:
        self.assertIn("current-check", root_map.node_ids())
        self.assertIn("sequence", root_map.node_ids())
        self.assertIn("manifest-index", root_map.node_ids())
        self.assertIn("docs-index", root_map.node_ids())
        self.assertIn("overview-index", root_map.node_ids())
        self.assertIn("root-map", root_map.node_ids())

    def test_upstreams_are_known(self) -> None:
        known = set(root_map.node_ids())
        self.assertTrue(set(root_map.upstream_ids()).issubset(known))
        self.assertIn("overview-index", root_map.upstream_ids())

    def test_root_map_verifies(self) -> None:
        self.assertEqual(root_map.root_map_issues(), ())
        self.assertTrue(root_map.verify_root_map())

    def test_markdown_names_root_map(self) -> None:
        markdown = root_map.as_markdown()
        self.assertIn("root-map", markdown)
        self.assertIn("runtime/kuuos_root_map_v0_45.py", markdown)


if __name__ == "__main__":
    unittest.main()
