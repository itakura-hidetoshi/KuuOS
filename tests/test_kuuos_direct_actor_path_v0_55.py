from __future__ import annotations

import importlib
import unittest


class KuuOSDirectActorPathV055Tests(unittest.TestCase):
    def test_layer(self) -> None:
        name = "runtime." + "kuuos_direct_" + "execution_actor_v0_55"
        layer = importlib.import_module(name)
        self.assertEqual(layer.VERSION, "kuuos_direct_execution_actor_v0_55")
        self.assertTrue(layer.READ_ONLY)
        self.assertTrue(layer.METADATA_ONLY)
        self.assertTrue(layer.PR_PATH_REQUIRED)
        self.assertTrue(layer.GATE_REQUIRED)
        self.assertTrue(layer.verify_direct_execution_actor())


if __name__ == "__main__":
    unittest.main()
