import unittest

from runtime.kuuos_runtime_daemon_qi_supervised_loop_control_v0_1 import compile_qi_supervised_loop_control


class QiSupervisedLoopControlTests(unittest.TestCase):
    def test_allows_bounded_loop_when_enabled_and_not_stopped(self):
        control = compile_qi_supervised_loop_control(
            control_packet={
                "enabled": True,
                "stop_requested": False,
                "max_cycles": 3,
                "sleep_seconds_between_cycles": 0.0,
            },
            heartbeat_utc="2026-05-25T00:00:00Z",
        )
        self.assertEqual(control.control_status, "QI_SUPERVISED_LOOP_CONTROL_ALLOWED")
        self.assertTrue(control.loop_allowed)
        self.assertEqual(control.max_cycles, 3)
        self.assertEqual(control.control_blockers, [])
        self.assertTrue(control.control_only)
        self.assertTrue(control.read_only)
        self.assertFalse(control.grants_execution_authority)

    def test_blocks_when_disabled(self):
        control = compile_qi_supervised_loop_control(control_packet={"enabled": False, "max_cycles": 2})
        self.assertFalse(control.loop_allowed)
        self.assertEqual(control.control_reason, "loop_disabled")
        self.assertIn("loop_disabled", control.control_blockers)

    def test_blocks_when_stop_requested(self):
        control = compile_qi_supervised_loop_control(control_packet={"enabled": True, "stop_requested": True, "max_cycles": 2})
        self.assertFalse(control.loop_allowed)
        self.assertEqual(control.control_reason, "stop_requested")
        self.assertIn("stop_requested", control.control_blockers)

    def test_blocks_invalid_max_cycles_and_clamps_runtime_value(self):
        control = compile_qi_supervised_loop_control(control_packet={"enabled": True, "max_cycles": 0})
        self.assertFalse(control.loop_allowed)
        self.assertIn("max_cycles_below_one", control.control_blockers)
        self.assertEqual(control.max_cycles, 1)

    def test_missing_packet_uses_safe_defaults_with_warning(self):
        control = compile_qi_supervised_loop_control(control_packet={})
        self.assertTrue(control.loop_allowed)
        self.assertIn("control_packet_missing_using_safe_defaults", control.control_warnings)
        self.assertEqual(control.max_cycles, 1)
        self.assertFalse(control.grants_next_tick_execution_authority)


if __name__ == "__main__":
    unittest.main()
