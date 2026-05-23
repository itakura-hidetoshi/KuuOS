import unittest

from runtime.kuuos_runtime_daemon_qi_process_tensor_closed_loop_receipt_v0_1 import (
    compile_qi_process_tensor_closed_loop_receipt,
)


class QiProcessTensorClosedLoopReceiptTests(unittest.TestCase):
    def test_hold_scheduler_becomes_closed_loop_hold_receipt(self):
        receipt = compile_qi_process_tensor_closed_loop_receipt(
            {
                "daemon_status": "DAEMON_WAITING_APPEND_ONLY",
                "stop_reason": "WAITING_FOR_MORE_EVIDENCE",
                "ticks_run": 1,
                "qi_process_tensor_actuator_path": "daemon_qi_process_tensor_actuator_v0_1.json",
                "qi_process_tensor_tick_scheduler_path": "daemon_qi_process_tensor_tick_scheduler_v0_1.json",
            },
            {
                "next_tick_advisory": "HOLD_AND_REOBSERVE_PROCESS_TENSOR",
                "next_sleep_seconds_hint": 2.0,
                "next_max_ticks_hint": 1,
                "next_max_steps_per_tick_hint": 1,
                "compact_before_next_tick": False,
                "reobserve_before_next_tick": True,
                "hold_until_observation": True,
            },
        )
        self.assertEqual(receipt.receipt_status, "QI_PROCESS_TENSOR_CLOSED_LOOP_HOLD")
        self.assertEqual(receipt.closed_loop_next_state, "HOLD_UNTIL_OBSERVATION")
        self.assertTrue(receipt.observation_required)
        self.assertFalse(receipt.grants_execution_authority)
        self.assertFalse(receipt.grants_truth_authority)
        self.assertFalse(receipt.grants_final_commitment_authority)
        self.assertFalse(receipt.grants_memory_overwrite_authority)

    def test_compact_scheduler_becomes_closed_loop_compact_receipt(self):
        receipt = compile_qi_process_tensor_closed_loop_receipt(
            {"daemon_status": "DAEMON_MAX_TICKS_REACHED_APPEND_ONLY", "stop_reason": "MAX_TICKS_REACHED", "ticks_run": 3},
            {
                "next_tick_advisory": "COMPACT_TRACE_THEN_CONTINUE",
                "next_sleep_seconds_hint": 1.0,
                "next_max_ticks_hint": 3,
                "next_max_steps_per_tick_hint": 2,
                "compact_before_next_tick": True,
                "reobserve_before_next_tick": False,
                "hold_until_observation": False,
            },
        )
        self.assertEqual(receipt.receipt_status, "QI_PROCESS_TENSOR_CLOSED_LOOP_COMPACT")
        self.assertEqual(receipt.closed_loop_next_state, "COMPACT_BEFORE_NEXT_TICK")
        self.assertTrue(receipt.compact_required)
        self.assertFalse(receipt.observation_required)

    def test_continue_scheduler_remains_nonexecuting_receipt(self):
        receipt = compile_qi_process_tensor_closed_loop_receipt(
            {"daemon_status": "DAEMON_MAX_TICKS_REACHED_APPEND_ONLY", "stop_reason": "MAX_TICKS_REACHED", "ticks_run": 3},
            {
                "next_tick_advisory": "CONTINUE_WITH_PROCESS_TENSOR_MONITOR",
                "next_sleep_seconds_hint": 1.0,
                "next_max_ticks_hint": 3,
                "next_max_steps_per_tick_hint": 1,
                "compact_before_next_tick": False,
                "reobserve_before_next_tick": False,
                "hold_until_observation": False,
            },
        )
        self.assertEqual(receipt.receipt_status, "QI_PROCESS_TENSOR_CLOSED_LOOP_CONTINUE")
        self.assertEqual(receipt.closed_loop_next_state, "CONTINUE_NEXT_TICK")
        self.assertIn("nonexecuting_runtime_receipt", receipt.allowed_projection)
        self.assertFalse(receipt.grants_execution_authority)


if __name__ == "__main__":
    unittest.main()
