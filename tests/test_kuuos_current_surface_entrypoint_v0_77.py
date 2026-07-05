import json
import unittest

from runtime.kuuos_current_surface_entrypoint_v0_77 import (
    STABLE_ENTRYPOINT,
    STABLE_INDEX,
    STABLE_SURFACE_ARTIFACT,
    current_surface,
    current_surface_index,
    current_surface_json,
    entrypoint_issues,
    verify_entrypoint,
)


class KuuOSCurrentSurfaceEntrypointV077Test(unittest.TestCase):
    def test_entrypoint_verifies(self):
        self.assertEqual((), entrypoint_issues())
        self.assertTrue(verify_entrypoint())

    def test_stable_paths(self):
        self.assertEqual("runtime/kuuos_current_surface.py", STABLE_ENTRYPOINT)
        self.assertEqual("status/current.surface.index.json", STABLE_INDEX)
        self.assertEqual("status/current.surface.json", STABLE_SURFACE_ARTIFACT)

    def test_surface_index_points_to_surface_artifact(self):
        index = current_surface_index()
        self.assertEqual("status/current.surface.json", index["surface_artifact"])
        self.assertEqual(
            "runtime/kuuos_current_status_surface_artifact_v0_75.py",
            index["surface_artifact_runtime"],
        )

    def test_current_surface_payload(self):
        surface = current_surface()
        self.assertEqual("surface_not_authority_grant", surface["authority_boundary"])
        self.assertEqual("status/current.manifest.json", surface["stable_manifest"])
        self.assertEqual("status/current.resolved.json", surface["stable_resolved_status"])

    def test_current_surface_json_round_trips(self):
        self.assertEqual(current_surface(), json.loads(current_surface_json()))


if __name__ == "__main__":
    unittest.main()
