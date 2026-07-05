import unittest

from runtime.kuuos_current_status_pointer_v0_70 import (
    POINTER_PATH,
    expected_pointer,
    load_pointer,
    pointer_issues,
    verify_pointer,
)


class KuuOSCurrentStatusPointerV070Test(unittest.TestCase):
    def test_pointer_verifies(self):
        self.assertEqual((), pointer_issues())
        self.assertTrue(verify_pointer())

    def test_pointer_path_is_stable(self):
        self.assertEqual("status/current.json", POINTER_PATH)

    def test_pointer_matches_expected(self):
        self.assertEqual(expected_pointer(), load_pointer())

    def test_pointer_targets_current_index(self):
        pointer = load_pointer()
        self.assertEqual("status/kuuos_status_index_v0_69.json", pointer["current_status_index"])
        self.assertEqual("kuuos_current_root_sequence_v0_70", pointer["current_root_sequence"])
        self.assertEqual("current_pointer_not_authority_grant", pointer["authority_boundary"])


if __name__ == "__main__":
    unittest.main()
