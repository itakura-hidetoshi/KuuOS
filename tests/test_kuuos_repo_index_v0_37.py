import unittest

from runtime.kuuos_repository_self_organization_v0_37 import organization_issues, verify_repository_self_organization, current_root


class RepoIndexV037Test(unittest.TestCase):
    def test_index_valid(self):
        self.assertEqual((), organization_issues())
        self.assertTrue(verify_repository_self_organization())

    def test_current_root_exists(self):
        root = current_root()
        self.assertEqual("current-root", root.role)
        self.assertIn("runtime/kuuos_v124_check.py", root.includes)


if __name__ == "__main__":
    unittest.main()
