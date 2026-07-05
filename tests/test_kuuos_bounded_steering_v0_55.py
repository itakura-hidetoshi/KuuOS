from __future__ import annotations

import unittest

from runtime import kuuos_bounded_steering_v0_55 as compatibility


class KuuOSCompatibilityV055Tests(unittest.TestCase):
    def test_compatibility_layer_delegates(self) -> None:
        self.assertEqual(compatibility.VERSION, "kuuos_bounded_steering_v0_55")
        self.assertTrue(compatibility.READ_ONLY)
        self.assertTrue(compatibility.METADATA_ONLY)
        self.assertTrue(compatibility.DIRECT_EXECUTION)
        self.assertEqual(compatibility.ACTOR, "KuuOSAgent")
        self.assertEqual(compatibility.failed_steps(), ())
        self.assertEqual(compatibility.steering_issues(), ())
        self.assertTrue(compatibility.verify_bounded_steering())


if __name__ == "__main__":
    unittest.main()
