import json
import unittest

from runtime.kuuos_current_status_manifest_v0_73 import (
    MANIFEST_PATH,
    expected_manifest,
    load_manifest,
    manifest_issues,
    manifest_json,
    verify_manifest,
)


class KuuOSCurrentStatusManifestV073Test(unittest.TestCase):
    def test_manifest_verifies(self):
        self.assertEqual((), manifest_issues())
        self.assertTrue(verify_manifest())

    def test_manifest_path_is_stable(self):
        self.assertEqual("status/current.manifest.json", MANIFEST_PATH)

    def test_manifest_matches_expected(self):
        self.assertEqual(expected_manifest(), load_manifest())

    def test_manifest_json_round_trips(self):
        self.assertEqual(load_manifest(), json.loads(manifest_json()))

    def test_manifest_points_to_status_surface(self):
        manifest = load_manifest()
        self.assertEqual("status/current.json", manifest["current_pointer"])
        self.assertEqual("status/current.resolved.json", manifest["current_resolved_status"])
        self.assertEqual("runtime/kuuos_current_status.py", manifest["current_status_cli"])
        self.assertEqual("manifest_not_authority_grant", manifest["authority_boundary"])


if __name__ == "__main__":
    unittest.main()
