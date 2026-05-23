import unittest

from runtime.kuuos_runtime_daemon_v0_1 import KuuOSDaemonResult


class QiProcessTensorActuatorOutputFieldsTests(unittest.TestCase):
    def test_daemon_result_contains_actuator_fields(self):
        fields = KuuOSDaemonResult.__dataclass_fields__
        self.assertIn("qi_process_tensor_actuator_path", fields)
        self.assertIn("next_tick_advisory", fields)
        self.assertIn("actuator_sleep_scale_hint", fields)
        self.assertIn("actuator_max_steps_hint", fields)
        self.assertIn("actuator_compact_trace_hint", fields)
        self.assertIn("actuator_reobserve_hint", fields)
        self.assertIn("actuator_hold_transition_hint", fields)


if __name__ == "__main__":
    unittest.main()
