import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_tick_scheduler_v0_1 import compile_qi_process_tensor_tick_scheduler


def actuator(advisory, **overrides):
    payload = {
        "next_tick_advisory": advisory,
        "sleep_scale_hint": 1.0,
        "max_steps_hint": 2,
        "compact_trace_hint": False,
        "reobserve_hint": False,
        "hold_transition_hint": False,
    }
    payload.update(overrides)
    return payload


class QiProcessTensorTickSchedulerTests(unittest.TestCase):
    def test_continue_schedule_is_bounded(self):
        result = compile_qi_process_tensor_tick_scheduler(
            actuator("CONTINUE_WITH_PROCESS_TENSOR_MONITOR"),
            base_sleep_seconds=2.0,
            base_max_ticks=5,
            base_max_steps_per_tick=2,
        )
        self.assertEqual(result.scheduler_status, "QI_PROCESS_TENSOR_TICK_SCHEDULER_CONTINUE")
        self.assertEqual(result.next_max_ticks_hint, 5)
        self.assertLessEqual(result.next_max_steps_per_tick_hint, 3)
        self.assertFalse(result.compact_before_next_tick)
        self.assertFalse(result.grants_execution_authority)

    def test_compact_schedule_sets_compact_hint(self):
        result = compile_qi_process_tensor_tick_scheduler(
            actuator("COMPACT_TRACE_THEN_CONTINUE", compact_trace_hint=True, max_steps_hint=2),
            base_sleep_seconds=1.0,
            base_max_ticks=8,
            base_max_steps_per_tick=4,
        )
        self.assertEqual(result.scheduler_status, "QI_PROCESS_TENSOR_TICK_SCHEDULER_COMPACT")
        self.assertTrue(result.compact_before_next_tick)
        self.assertFalse(result.reobserve_before_next_tick)
        self.assertLessEqual(result.next_max_ticks_hint, 5)
        self.assertLessEqual(result.next_max_steps_per_tick_hint, 2)

    def test_reobserve_schedule_shortens_ticks(self):
        result = compile_qi_process_tensor_tick_scheduler(
            actuator("REOBSERVE_QI_PROCESS_TENSOR", reobserve_hint=True, sleep_scale_hint=1.5),
            base_sleep_seconds=2.0,
            base_max_ticks=6,
            base_max_steps_per_tick=4,
        )
        self.assertEqual(result.scheduler_status, "QI_PROCESS_TENSOR_TICK_SCHEDULER_REOBSERVE")
        self.assertTrue(result.reobserve_before_next_tick)
        self.assertLessEqual(result.next_max_ticks_hint, 2)
        self.assertEqual(result.next_max_steps_per_tick_hint, 1)
        self.assertGreaterEqual(result.next_sleep_seconds_hint, 3.0)

    def test_hold_schedule_single_tick_reobserve(self):
        result = compile_qi_process_tensor_tick_scheduler(
            actuator("HOLD_AND_REOBSERVE_PROCESS_TENSOR", hold_transition_hint=True, sleep_scale_hint=1.75),
            base_sleep_seconds=1.0,
            base_max_ticks=10,
            base_max_steps_per_tick=5,
        )
        self.assertEqual(result.scheduler_status, "QI_PROCESS_TENSOR_TICK_SCHEDULER_HOLD")
        self.assertTrue(result.hold_until_observation)
        self.assertTrue(result.reobserve_before_next_tick)
        self.assertEqual(result.next_max_ticks_hint, 1)
        self.assertEqual(result.next_max_steps_per_tick_hint, 1)


if __name__ == "__main__":
    unittest.main()
