import unittest

from runtime.kuuos_runtime_daemon_v0_1 import KuuOSDaemonResult


class GeometricChainFieldsTests(unittest.TestCase):
    def test_daemon_result_contains_geometric_chain_fields(self):
        fields = KuuOSDaemonResult.__dataclass_fields__
        self.assertIn("active_inference_feature_bundle_path", fields)
        self.assertIn("belief_state_manifold_path", fields)
        self.assertIn("precision_geometry_path", fields)
        self.assertIn("efe_landscape_path", fields)
        self.assertIn("efe_smoothed_selected_policy", fields)
        self.assertIn("efe_transition_distance", fields)
        self.assertIn("efe_curvature_barrier", fields)


if __name__ == "__main__":
    unittest.main()
