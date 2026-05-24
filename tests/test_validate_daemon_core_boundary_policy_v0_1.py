import unittest

from scripts.validate_daemon_core_boundary_policy_v0_1 import main


class DaemonCoreBoundaryPolicyValidatorTests(unittest.TestCase):
    def test_validator_passes_repository_daemon_core(self):
        self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
