import unittest

from runtime.kuuos_queue_dispatcher_v0_1 import dispatch_candidate_cycle, empty_queue_state


BASE_RAW = {
    "cycle_id": "dispatch-001",
    "generated_at_utc": "2026-05-21T00:00:00+00:00",
    "dispatched_at_utc": "2026-05-21T00:00:01+00:00",
    "candidate_only": True,
    "nonfinal_marker": True,
    "two_truths_gap": True,
    "noncollapse_guard": True,
    "memory_overwrite_blocker": True,
    "world_identity_blocker": True,
    "physical_process_visible": True,
    "thermodynamic_activity_visible": True,
    "process_tensor_visible": True,
    "barrier_witness_visible": True,
    "receipt_hash": True,
    "support_refs": True,
    "registry_key": True,
    "view_delivery_receipt": True,
    "channel_scope": True,
    "acknowledgment_marker": True,
}


class KuuOSQueueDispatcherTests(unittest.TestCase):
    def test_allow_candidate_dispatches_to_next_nonfinal_stage(self):
        result = dispatch_candidate_cycle(BASE_RAW)
        self.assertEqual(result.dispatch_status, "DISPATCHED_APPEND_ONLY")
        self.assertEqual(result.target_queue, "NEXT_NONFINAL_STAGE")
        self.assertEqual(result.queue_lengths["NEXT_NONFINAL_STAGE"], 1)
        self.assertEqual(result.updated_queue_state["last_receipt_hash"], result.receipt_hash)
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)
        self.assertFalse(result.grants_final_commitment_authority)
        self.assertFalse(result.grants_memory_overwrite_authority)

    def test_reobserve_dispatches_to_reobserve_queue(self):
        raw = dict(BASE_RAW)
        raw["physical_process_visible"] = False
        raw["thermodynamic_activity_visible"] = False
        result = dispatch_candidate_cycle(raw)
        self.assertEqual(result.target_queue, "REOBSERVE_QUEUE")
        self.assertEqual(result.queue_lengths["REOBSERVE_QUEUE"], 1)
        self.assertIn("value_witness_receipt", result.candidate_cycle_receipt["missing_inputs"])

    def test_lineage_gap_dispatches_to_lineage_queue(self):
        raw = dict(BASE_RAW)
        raw["support_refs"] = False
        result = dispatch_candidate_cycle(raw)
        self.assertEqual(result.target_queue, "LINEAGE_RECHECK_QUEUE")
        self.assertEqual(result.queue_lengths["LINEAGE_RECHECK_QUEUE"], 1)

    def test_delivery_gap_dispatches_to_delivery_queue(self):
        raw = dict(BASE_RAW)
        raw["view_delivery_receipt"] = False
        result = dispatch_candidate_cycle(raw)
        self.assertEqual(result.target_queue, "DELIVERY_RECHECK_QUEUE")
        self.assertEqual(result.queue_lengths["DELIVERY_RECHECK_QUEUE"], 1)

    def test_boundary_failure_dispatches_to_quarantine_queue(self):
        raw = dict(BASE_RAW)
        raw["world_identity_blocker"] = False
        result = dispatch_candidate_cycle(raw)
        self.assertEqual(result.target_queue, "QUARANTINE_QUEUE")
        self.assertEqual(result.queue_lengths["QUARANTINE_QUEUE"], 1)
        self.assertIn("world_identity_blocker", result.candidate_cycle_receipt["blocked_boundaries"])

    def test_queue_state_appends_and_chains_previous_hash(self):
        first = dispatch_candidate_cycle(BASE_RAW)
        second_raw = dict(BASE_RAW)
        second_raw["cycle_id"] = "dispatch-002"
        second_raw["generated_at_utc"] = "2026-05-21T00:00:02+00:00"
        second_raw["dispatched_at_utc"] = "2026-05-21T00:00:03+00:00"
        second = dispatch_candidate_cycle(second_raw, first.updated_queue_state)
        self.assertEqual(second.previous_receipt_hash, first.receipt_hash)
        self.assertEqual(second.updated_queue_state["last_receipt_hash"], second.receipt_hash)
        self.assertEqual(second.queue_lengths["NEXT_NONFINAL_STAGE"], 2)
        self.assertEqual(len(second.updated_queue_state["dispatch_log"]), 2)

    def test_empty_queue_state_has_all_queues_and_no_authority(self):
        state = empty_queue_state()
        self.assertIn("NEXT_NONFINAL_STAGE", state["queues"])
        self.assertIn("QUARANTINE_QUEUE", state["queues"])
        self.assertFalse(state["grants_execution_authority"])
        self.assertFalse(state["grants_truth_authority"])
        self.assertFalse(state["grants_final_commitment_authority"])
        self.assertFalse(state["grants_memory_overwrite_authority"])


if __name__ == "__main__":
    unittest.main()
