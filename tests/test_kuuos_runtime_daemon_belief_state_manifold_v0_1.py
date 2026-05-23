import unittest

from runtime.kuuos_runtime_daemon_belief_state_manifold_v0_1 import compile_belief_state_manifold

FEATURE_BUNDLE = {
    "active_inference_inputs": {
        "tick_density": 6,
        "process_history_length": 4,
        "transition_support_count": 3,
        "memory_support_count": 2,
        "nonmarkov_support_count": 1,
        "missing_source_count": 1,
        "yinyang_polarity_state": "RECOVERY_YANG_PRESENT",
        "four_image_phase": "GREATER_YANG",
        "qique_regime": "NONMARKOV_MEMORY_ACTIVE",
        "emptiness_action": "CONTINUE_ADVISORY_ONLY",
        "wa_posture": "CONTINUE_HARMONIZED",
    },
    "hard_constraints": {
        "boundary_hard_constraint": False,
        "observation_hard_constraint": False,
    },
    "preference_priors": {
        "prefer_recovery_path": True,
    },
}


class BeliefStateManifoldTests(unittest.TestCase):
    def test_compile_continuous_belief_coordinates(self):
        result = compile_belief_state_manifold(FEATURE_BUNDLE)
        coords = result.belief_coordinates
        self.assertEqual(result.manifold_status, "BELIEF_STATE_MANIFOLD_COMPILED")
        self.assertIn("x_boundary", coords)
        self.assertIn("x_uncertainty", coords)
        self.assertIn("x_density", coords)
        self.assertIn("x_recovery", coords)
        self.assertIn("x_action", coords)
        self.assertIn("x_memory_continuity", coords)
        self.assertIn("x_nonmarkov_pressure", coords)
        self.assertGreater(coords["x_density"], 0.5)
        self.assertGreater(coords["x_memory_continuity"], 0.5)
        self.assertGreater(coords["x_nonmarkov_pressure"], 0.2)
        self.assertFalse(result.grants_execution_authority)

    def test_boundary_constraint_projects_to_boundary_coordinate(self):
        feature = dict(FEATURE_BUNDLE)
        feature["hard_constraints"] = {
            "boundary_hard_constraint": True,
            "observation_hard_constraint": False,
        }
        result = compile_belief_state_manifold(feature)
        self.assertEqual(result.belief_coordinates["x_boundary"], 1.0)

    def test_observation_constraint_projects_to_uncertainty(self):
        feature = dict(FEATURE_BUNDLE)
        feature["hard_constraints"] = {
            "boundary_hard_constraint": False,
            "observation_hard_constraint": True,
        }
        result = compile_belief_state_manifold(feature)
        self.assertGreater(result.belief_coordinates["x_uncertainty"], 0.3)


if __name__ == '__main__':
    unittest.main()
