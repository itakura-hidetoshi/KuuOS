import unittest

from runtime.kuuos_self_organization_status_snapshot_v0_68 import (
    SNAPSHOT_PATH,
    expected_snapshot,
    load_snapshot,
    snapshot_issues,
    verify_snapshot,
)


class KuuOSSelfOrganizationStatusSnapshotV068Test(unittest.TestCase):
    def test_snapshot_verifies(self):
        self.assertEqual((), snapshot_issues())
        self.assertTrue(verify_snapshot())

    def test_snapshot_path_is_public_status_artifact(self):
        self.assertEqual("status/kuuos_self_organization_status_v0_68.json", SNAPSHOT_PATH)

    def test_snapshot_matches_expected_live_status(self):
        self.assertEqual(expected_snapshot(), load_snapshot())

    def test_snapshot_keeps_authority_boundary(self):
        snapshot = load_snapshot()
        self.assertEqual("active_state_not_unbounded_authority", snapshot["authority_boundary"])
        self.assertTrue(snapshot["active"])
        self.assertTrue(snapshot["bounded_execution_verified"])
        self.assertTrue(snapshot["current_root_sequence_verified"])
        self.assertTrue(snapshot["public_status_checked"])


if __name__ == "__main__":
    unittest.main()
