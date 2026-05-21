import unittest

from runtime.qi_cycle_runner_v0_1 import run_qi_cycle


BASE_STATE = {
    "cycle_id": "cycle-runner-001",
    "kernel_state": "candidate",
    "candidate_only": True,
    "nonfinal_marker": True,
    "two_truths_gap": True,
    "noncollapse_guard": True,
    "memory_overwrite_blocker": True,
    "world_identity_blocker": True,
    "runtime_variation_visible": True,
    "policy_candidate_receipt": True,
    "value_witness_receipt": True,
    "barrier_witness_receipt": True,
    "receipt_hash": True,
    "support_refs": True,
    "registry_key": True,
    "view_delivery_receipt": True,
    "channel_scope": True,
    "acknowledgment_marker": True,
}


class QiCycleRunnerTests(unittest.TestCase):
    def test_allow_candidate_goes_to_next_nonfinal_stage(self):
        decision = run_qi_cycle(BASE_STATE)
        self.assertEqual(decision.qi_signal, "ALLOW_CANDIDATE")
        self.assertEqual(decision.next_stage, "NEXT_NONFINAL_STAGE")
        self.assertFalse(decision.terminal_for_cycle)
        self.assertFalse(decision.grants_execution_authority)
        self.assertFalse(decision.grants_truth_authority)
        self.assertFalse(decision.grants_final_commitment_authority)
        self.assertFalse(decision.grants_memory_overwrite_authority)

    def test_hold_goes_to_hold_queue(self):
        state = dict(BASE_STATE)
        state["candidate_only"] = False
        decision = run_qi_cycle(state)
        self.assertEqual(decision.qi_signal, "HOLD")
        self.assertEqual(decision.next_stage, "HOLD_QUEUE")
        self.assertTrue(decision.terminal_for_cycle)

    def test_reobserve_goes_to_reobserve_queue(self):
        state = dict(BASE_STATE)
        state["runtime_variation_visible"] = False
        decision = run_qi_cycle(state)
        self.assertEqual(decision.qi_signal, "REOBSERVE")
        self.assertEqual(decision.next_stage, "REOBSERVE_QUEUE")
        self.assertTrue(decision.terminal_for_cycle)

    def test_lineage_recheck_goes_to_lineage_queue(self):
        state = dict(BASE_STATE)
        state["receipt_hash"] = False
        decision = run_qi_cycle(state)
        self.assertEqual(decision.qi_signal, "LINEAGE_RECHECK")
        self.assertEqual(decision.next_stage, "LINEAGE_RECHECK_QUEUE")
        self.assertTrue(decision.terminal_for_cycle)

    def test_delivery_recheck_goes_to_delivery_queue(self):
        state = dict(BASE_STATE)
        state["channel_scope"] = False
        decision = run_qi_cycle(state)
        self.assertEqual(decision.qi_signal, "DELIVERY_RECHECK")
        self.assertEqual(decision.next_stage, "DELIVERY_RECHECK_QUEUE")
        self.assertTrue(decision.terminal_for_cycle)

    def test_boundary_failure_goes_to_quarantine_queue(self):
        state = dict(BASE_STATE)
        state["noncollapse_guard"] = False
        decision = run_qi_cycle(state)
        self.assertEqual(decision.qi_signal, "QUARANTINE")
        self.assertEqual(decision.next_stage, "QUARANTINE_QUEUE")
        self.assertTrue(decision.terminal_for_cycle)
        self.assertIn("noncollapse_guard", decision.blocked_boundaries)


if __name__ == "__main__":
    unittest.main()
