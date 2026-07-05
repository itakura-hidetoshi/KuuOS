import json
import unittest

from runtime.kuuos_current_resolved_status_artifact_v0_72 import (
    RESOLVED_STATUS_PATH,
    artifact_issues,
    artifact_json,
    expected_resolved_artifact,
    load_resolved_artifact,
    verify_artifact,
)


class KuuOSCurrentResolvedStatusArtifactV072Test(unittest.TestCase):
    def test_artifact_verifies(self):
        self.assertEqual((), artifact_issues())
        self.assertTrue(verify_artifact())

    def test_artifact_path_is_stable(self):
        self.assertEqual("status/current.resolved.json", RESOLVED_STATUS_PATH)

    def test_artifact_matches_resolver_output(self):
        self.assertEqual(expected_resolved_artifact(), load_resolved_artifact())

    def test_artifact_json_round_trips(self):
        self.assertEqual(load_resolved_artifact(), json.loads(artifact_json()))

    def test_artifact_preserves_boundaries(self):
        artifact = load_resolved_artifact()
        self.assertEqual("resolver_not_authority_grant", artifact["authority_boundary"])
        self.assertEqual("runtime/kuuos_current_status.py", artifact["stable_entrypoint"])
        self.assertTrue(artifact["pointer_verified"])
        self.assertTrue(artifact["status_index_verified"])
        self.assertTrue(artifact["snapshot_verified"])


if __name__ == "__main__":
    unittest.main()
