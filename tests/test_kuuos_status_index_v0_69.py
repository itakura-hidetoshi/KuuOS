import unittest

from runtime.kuuos_status_index_v0_69 import (
    INDEX_PATH,
    expected_index,
    index_issues,
    load_index,
    verify_index,
)


class KuuOSStatusIndexV069Test(unittest.TestCase):
    def test_index_verifies(self):
        self.assertEqual((), index_issues())
        self.assertTrue(verify_index())

    def test_index_path_is_status_artifact(self):
        self.assertEqual("status/kuuos_status_index_v0_69.json", INDEX_PATH)

    def test_index_matches_expected(self):
        self.assertEqual(expected_index(), load_index())

    def test_index_points_to_latest_snapshot(self):
        index = load_index()
        self.assertEqual(
            "status/kuuos_self_organization_status_v0_68.json",
            index["latest_self_organization_snapshot"],
        )
        self.assertEqual("kuuos_current_root_sequence_v0_68", index["current_root_sequence"])
        self.assertEqual("status_index_not_authority_grant", index["authority_boundary"])


if __name__ == "__main__":
    unittest.main()
