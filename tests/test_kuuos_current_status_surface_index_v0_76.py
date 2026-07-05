import json
import unittest

from runtime.kuuos_current_status_surface_index_v0_76 import (
    SURFACE_INDEX_PATH,
    expected_surface_index,
    load_surface_index,
    surface_index_issues,
    surface_index_json,
    verify_surface_index,
)


class KuuOSCurrentStatusSurfaceIndexV076Test(unittest.TestCase):
    def test_surface_index_verifies(self):
        self.assertEqual((), surface_index_issues())
        self.assertTrue(verify_surface_index())

    def test_surface_index_path_is_stable(self):
        self.assertEqual("status/current.surface.index.json", SURFACE_INDEX_PATH)

    def test_surface_index_matches_expected(self):
        self.assertEqual(expected_surface_index(), load_surface_index())

    def test_surface_index_json_round_trips(self):
        self.assertEqual(load_surface_index(), json.loads(surface_index_json()))

    def test_surface_index_points_to_surface_artifact(self):
        index = load_surface_index()
        self.assertEqual("status/current.surface.json", index["surface_artifact"])
        self.assertEqual("runtime/kuuos_current_status_surface_v0_74.py", index["surface_runtime"])
        self.assertEqual(
            "runtime/kuuos_current_status_surface_artifact_v0_75.py",
            index["surface_artifact_runtime"],
        )
        self.assertEqual("surface_index_not_authority_grant", index["authority_boundary"])


if __name__ == "__main__":
    unittest.main()
