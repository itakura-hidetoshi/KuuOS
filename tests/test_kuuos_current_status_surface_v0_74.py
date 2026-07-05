import json
import unittest

from runtime.kuuos_current_status_surface_v0_74 import (
    STABLE_MANIFEST,
    STABLE_RESOLVED_STATUS,
    status_surface,
    surface_issues,
    surface_json,
    verify_surface,
)


class KuuOSCurrentStatusSurfaceV074Test(unittest.TestCase):
    def test_surface_verifies(self):
        self.assertEqual((), surface_issues())
        self.assertTrue(verify_surface())

    def test_stable_paths_are_manifest_and_resolved_status(self):
        self.assertEqual("status/current.manifest.json", STABLE_MANIFEST)
        self.assertEqual("status/current.resolved.json", STABLE_RESOLVED_STATUS)

    def test_surface_payload_has_expected_layers(self):
        surface = status_surface()
        self.assertEqual("v0.74", surface["surface_schema_version"])
        self.assertEqual("kuuos_current_status_surface_v0_74", surface["surface_frontier"])
        self.assertTrue(surface["manifest_verified"])
        self.assertTrue(surface["resolved_status_verified"])
        self.assertEqual("surface_not_authority_grant", surface["authority_boundary"])

    def test_surface_follows_manifest_to_resolved_status(self):
        surface = status_surface()
        self.assertEqual(
            "status/current.resolved.json",
            surface["manifest"]["current_resolved_status"],
        )
        self.assertEqual(
            "runtime/kuuos_current_status.py",
            surface["resolved_status"]["stable_entrypoint"],
        )

    def test_surface_json_round_trips(self):
        self.assertEqual(status_surface(), json.loads(surface_json()))


if __name__ == "__main__":
    unittest.main()
