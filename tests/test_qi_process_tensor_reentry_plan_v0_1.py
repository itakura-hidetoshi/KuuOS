import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_reentry_plan_v0_1 import (
    compile_qi_process_tensor_reentry_plan,
)


class QiProcessTensorReentryPlanTests(unittest.TestCase):
    def test_hold_receipt_blocks_reentry(self):
        plan = compile_qi_process_tensor_reentry_plan(
            {
                "receipt_status": "QI_PROCESS_TENSOR_CLOSED_LOOP_HOLD",
                "closed_loop_next_state": "HOLD_UNTIL_OBSERVATION",
                "scheduled_next_sleep_seconds_hint": 2.0,
                "scheduled_next_max_ticks_hint": 1,
                "scheduled_next_max_steps_per_tick_hint": 1,
                "scheduled_hold_until_observation": True,
            }
        )
        self.assertEqual(plan.plan_status, "QI_PROCESS_TENSOR_REENTRY_HELD")
        self.assertEqual(plan.next_invocation_mode, "NO_REENTRY_UNTIL_OBSERVATION")
        self.assertTrue(plan.hold_until_observation)
        self.assertTrue(plan.reobserve_before_reentry)
        self.assertFalse(plan.grants_execution_authority)

    def test_reobserve_receipt_requires_reobserve_first(self):
        plan = compile_qi_process_tensor_reentry_plan(
            {
                "receipt_status": "QI_PROCESS_TENSOR_CLOSED_LOOP_REOBSERVE",
                "closed_loop_next_state": "REOBSERVE_BEFORE_NEXT_TICK",
                "scheduled_next_sleep_seconds_hint": 1.0,
                "scheduled_next_max_ticks_hint": 2,
                "scheduled_next_max_steps_per_tick_hint": 1,
                "scheduled_reobserve_before_next_tick": True,
            }
        )
        self.assertEqual(plan.plan_status, "QI_PROCESS_TENSOR_REENTRY_REOBSERVE_FIRST")
        self.assertEqual(plan.next_invocation_mode, "REOBSERVE_THEN_BOUNDED_REENTRY")
        self.assertTrue(plan.reobserve_before_reentry)
        self.assertFalse(plan.hold_until_observation)

    def test_compact_receipt_requires_compaction_first(self):
        plan = compile_qi_process_tensor_reentry_plan(
            {
                "receipt_status": "QI_PROCESS_TENSOR_CLOSED_LOOP_COMPACT",
                "closed_loop_next_state": "COMPACT_BEFORE_NEXT_TICK",
                "scheduled_next_sleep_seconds_hint": 0.5,
                "scheduled_next_max_ticks_hint": 3,
                "scheduled_next_max_steps_per_tick_hint": 2,
                "scheduled_compact_before_next_tick": True,
            }
        )
        self.assertEqual(plan.plan_status, "QI_PROCESS_TENSOR_REENTRY_COMPACT_FIRST")
        self.assertEqual(plan.next_invocation_mode, "COMPACT_THEN_BOUNDED_REENTRY")
        self.assertTrue(plan.compact_before_reentry)
        self.assertEqual(plan.recommended_max_ticks, 3)
        self.assertEqual(plan.recommended_max_steps_per_tick, 2)

    def test_continue_receipt_allows_bounded_reentry_plan(self):
        plan = compile_qi_process_tensor_reentry_plan(
            {
                "receipt_status": "QI_PROCESS_TENSOR_CLOSED_LOOP_CONTINUE",
                "closed_loop_next_state": "CONTINUE_NEXT_TICK",
                "scheduled_next_sleep_seconds_hint": 0.25,
                "scheduled_next_max_ticks_hint": 4,
                "scheduled_next_max_steps_per_tick_hint": 3,
            }
        )
        self.assertEqual(plan.plan_status, "QI_PROCESS_TENSOR_REENTRY_READY")
        self.assertEqual(plan.next_invocation_mode, "BOUNDED_REENTRY_READY")
        self.assertEqual(plan.runtime_hot_path_tier, "T0_hot_path_guard")
        self.assertEqual(plan.validation_tier, "T3_runtime_full_check")
        self.assertFalse(plan.grants_execution_authority)
        self.assertIn("nonexecuting_next_tick_plan", plan.allowed_projection)

    def test_quarantine_daemon_result_overrides_reentry(self):
        plan = compile_qi_process_tensor_reentry_plan(
            {
                "receipt_status": "QI_PROCESS_TENSOR_CLOSED_LOOP_CONTINUE",
                "closed_loop_next_state": "CONTINUE_NEXT_TICK",
            },
            {"daemon_status": "DAEMON_QUARANTINE_RETAINED_APPEND_ONLY"},
        )
        self.assertEqual(plan.plan_status, "QI_PROCESS_TENSOR_REENTRY_HELD")
        self.assertEqual(plan.next_invocation_mode, "NO_REENTRY_DURING_QUARANTINE")
        self.assertTrue(plan.hold_until_observation)


if __name__ == "__main__":
    unittest.main()
