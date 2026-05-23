import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_actuator_v0_1 import compile_qi_process_tensor_actuator


def bundle(**overrides):
    active = {
        "process_tensor_visible": True,
        "process_history_length": 4,
        "transition_support_count": 3,
        "memory_support_count": 1,
        "nonmarkov_support_count": 0,
        "tick_density": 1,
    }
    active.update(overrides.pop("active", {}))
    primary = {
        "missing_process_requirements": [],
    }
    primary.update(overrides.pop("primary", {}))
    constraints = {
        "observation_hard_constraint": False,
    }
    constraints.update(overrides.pop("constraints", {}))
    return {
        "active_inference_inputs": active,
        "primary_qi_process_tensor": primary,
        "hard_constraints": constraints,
    }


def governor(**overrides):
    base = {
        "transition_mode": "STABLE_NO_RAMP",
        "oscillation_damping": 1.0,
        "ramp_fraction": 1.0,
    }
    base.update(overrides)
    return base


class QiProcessTensorActuatorTests(unittest.TestCase):
    def test_continue_when_continuity_is_supported(self):
        result = compile_qi_process_tensor_actuator(bundle(), governor())
        self.assertEqual(result.actuator_status, "QI_PROCESS_TENSOR_ACTUATOR_CONTINUE")
        self.assertEqual(result.next_tick_advisory, "CONTINUE_WITH_PROCESS_TENSOR_MONITOR")
        self.assertGreater(result.process_tensor_drive["continuity"], 0.9)
        self.assertFalse(result.grants_execution_authority)

    def test_nonmarkov_inertia_requests_trace_compaction(self):
        result = compile_qi_process_tensor_actuator(
            bundle(active={"nonmarkov_support_count": 3, "tick_density": 3}),
            governor(),
        )
        self.assertEqual(result.actuator_status, "QI_PROCESS_TENSOR_ACTUATOR_COMPACT")
        self.assertEqual(result.next_tick_advisory, "COMPACT_TRACE_THEN_CONTINUE")
        self.assertTrue(result.compact_trace_hint)
        self.assertGreaterEqual(result.process_tensor_drive["nonmarkov_inertia"], 0.7)

    def test_missing_requirements_request_reobserve(self):
        result = compile_qi_process_tensor_actuator(
            bundle(primary={"missing_process_requirements": ["transition", "memory", "nonmarkov"]}),
            governor(),
        )
        self.assertEqual(result.actuator_status, "QI_PROCESS_TENSOR_ACTUATOR_REOBSERVE")
        self.assertEqual(result.next_tick_advisory, "REOBSERVE_QI_PROCESS_TENSOR")
        self.assertTrue(result.reobserve_hint)
        self.assertGreaterEqual(result.process_tensor_drive["missingness_pressure"], 0.6)

    def test_low_governor_damping_holds_transition(self):
        result = compile_qi_process_tensor_actuator(
            bundle(),
            governor(transition_mode="HOLD_TRANSITION_REOBSERVE", oscillation_damping=0.2, ramp_fraction=0.0),
        )
        self.assertEqual(result.actuator_status, "QI_PROCESS_TENSOR_ACTUATOR_HOLD")
        self.assertEqual(result.next_tick_advisory, "HOLD_AND_REOBSERVE_PROCESS_TENSOR")
        self.assertTrue(result.hold_transition_hint)
        self.assertEqual(result.max_steps_hint, 1)


if __name__ == "__main__":
    unittest.main()
