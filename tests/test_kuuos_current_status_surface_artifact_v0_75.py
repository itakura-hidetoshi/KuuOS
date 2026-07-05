import json
import unittest

from runtime.kuuos_current_status_surface_artifact_v0_75 import (
    SURFACE_ARTIFACT_PATH,
    artifact_issues,
    artifact_json,
    expected_surface_artifact,
    load_surface_artifact,
    verify_artifact,
)


class KuuOSCurrentStatusSurfaceArtifactV075Test(unittest.TestCase):
    def test_artifact_verifies(self):
        self.assertEqual((), artifact_issues())
        self.assertTrue(verify_artifact())

    def test_artifact_path_is_stable(self):
        self.assertEqual("status/current.surface.json", SURFACE_ARTIFACT_PATH)

    def test_artifact_matches_surface_output(self):
        self.assertEqual(expected_surface_artifact(), load_surface_artifact())

    def test_artifact_json_round_trips(self):
        self.assertEqual(load_surface_artifact(), json.loads(artifact_json()))

    def test_artifact_preserves_surface_boundaries(self):
        artifact = load_surface_artifact()
        self.assertEqual("surface_not_authority_grant", artifact["authority_boundary"])
        self.assertEqual("status/current.manifest.json", artifact["stable_manifest"])
        self.assertEqual("status/current.resolved.json", artifact["stable_resolved_status"])
        self.assertTrue(artifact["manifest_verified"])
        self.assertTrue(artifact["resolved_status_verified"])


if __name__ == "__main__":
    unittest.main()
