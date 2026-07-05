import unittest

from runtime import kuuos_current_status


class KuuOSCurrentStatusCliV071Test(unittest.TestCase):
    def test_stable_cli_exports_resolver_surface(self):
        self.assertTrue(kuuos_current_status.verify_resolver())
        self.assertEqual((), kuuos_current_status.resolver_issues())
        self.assertIn("kuuos_current_status_resolver_v0_71", kuuos_current_status.resolved_status_json())

    def test_stable_cli_main_succeeds(self):
        self.assertEqual(0, kuuos_current_status.main())


if __name__ == "__main__":
    unittest.main()
