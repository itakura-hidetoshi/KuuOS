import json
import unittest

from runtime import kuuos_current_surface


class KuuOSCurrentSurfaceCliV077Test(unittest.TestCase):
    def test_cli_exports_entrypoint_functions(self):
        self.assertTrue(kuuos_current_surface.verify_entrypoint())
        self.assertEqual((), kuuos_current_surface.entrypoint_issues())

    def test_cli_payload_round_trips(self):
        self.assertEqual(
            kuuos_current_surface.current_surface(),
            json.loads(kuuos_current_surface.current_surface_json()),
        )

    def test_cli_main_succeeds(self):
        self.assertEqual(0, kuuos_current_surface.main())

    def test_cli_reads_surface_index(self):
        index = kuuos_current_surface.current_surface_index()
        self.assertEqual("status/current.surface.json", index["surface_artifact"])


if __name__ == "__main__":
    unittest.main()
