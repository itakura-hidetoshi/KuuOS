import unittest

from runtime.kuuos_runtime_daemon_precision_geometry_v0_1 import compile_precision_geometry

BELIEF_MANIFOLD = {
    "belief_coordinates": {
        "x_boundary": 0.9,
        "x_uncertainty": 0.4,
        "x_density": 0.7,
        "x_recovery": 0.8,
        "x_action": 0.5,
        "x_memory_continuity": 0.75,
        "x_nonmarkov_pressure": 0.6,
    }
}


class PrecisionGeometryTests(unittest.TestCase):
    def test_compile_directional_precision_weights(self):
        result = compile_precision_geometry(BELIEF_MANIFOLD)
        weights = result.precision_weights
        self.assertEqual(result.geometry_status, "PRECISION_GEOMETRY_COMPILED")
        self.assertIn("g_boundary", weights)
        self.assertIn("g_uncertainty", weights)
        self.assertIn("g_density", weights)
        self.assertIn("g_recovery", weights)
        self.assertIn("g_action", weights)
        self.assertIn("g_memory", weights)
        self.assertIn("g_nonmarkov", weights)
        self.assertGreater(weights["g_boundary"], weights["g_action"])
        self.assertGreater(weights["g_recovery"], 0.6)
        self.assertGreater(weights["g_nonmarkov"], 0.5)
        self.assertFalse(result.grants_execution_authority)

    def test_compile_diagonal_metric(self):
        result = compile_precision_geometry(BELIEF_MANIFOLD)
        metric = result.diagonal_metric
        self.assertIn("x_boundary", metric)
        self.assertIn("x_nonmarkov_pressure", metric)
        self.assertGreater(metric["x_boundary"], metric["x_action"])

    def test_compile_coupling_hints(self):
        result = compile_precision_geometry(BELIEF_MANIFOLD)
        coupling = result.coupling_hints
        self.assertIn("boundary_action_coupling", coupling)
        self.assertIn("density_recovery_coupling", coupling)
        self.assertIn("memory_uncertainty_coupling", coupling)
        self.assertIn("nonmarkov_density_coupling", coupling)
        self.assertGreater(coupling["density_recovery_coupling"], 0.4)


if __name__ == '__main__':
    unittest.main()
