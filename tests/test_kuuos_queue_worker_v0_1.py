import unittest

from runtime.kuuos_queue_dispatcher_v0_1 import dispatch_candidate_cycle, empty_queue_state
from runtime.kuuos_queue_worker_v0_1 import empty_worker_state, process_next_queue_item


BASE_RAW = {
    "cycle_id": "worker-001",
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


def make_queue_state_with(*raw_states):
    queue_state = empty_queue_state()
    for raw in raw_states:
        result = dispatch_candidate_cycle(raw, queue_state)
        queue_state = result.updated_queue_state
    return queue_state


class KuuOSQueueWorkerTests(unittest.TestCase):
    def test_worker_processes_next_nonfinal_packet_append_only(self):
        queue_state = make_queue_state_with(BASE_RAW)
        result = process_next_queue_item(queue_state)
        self.assertEqual(result.worker_status, "PROCESSED_ONE_APPEND_ONLY")
        self.assertEqual(result.selected_queue, "NEXT_NONFINAL_STAGE")
        self.assertIsNotNone(result.action_packet)
        self.assertEqual(result.action_packet["action_type"], "open_next_nonfinal_candidate_packet")
        self.assertIn(result.selected_receipt_hash, result.updated_worker_state["processed_receipt_hashes"])
        self.assertEqual(len(result.updated_worker_state["action_outbox"]), 1)
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)
        self.assertFalse(result.grants_final_commitment_authority)
        self.assertFalse(result.grants_memory_overwrite_authority)

    def test_worker_prioritizes_quarantine_over_next_nonfinal(self):
        good = dict(BASE_RAW)
        good["cycle_id"] = "worker-good"
        bad = dict(BASE_RAW)
        bad["cycle_id"] = "worker-bad"
        bad["world_identity_blocker"] = False
        queue_state = make_queue_state_with(good, bad)
        result = process_next_queue_item(queue_state)
        self.assertEqual(result.selected_queue, "QUARANTINE_QUEUE")
        self.assertEqual(result.action_packet["action_type"], "open_quarantine_review_packet")
        self.assertEqual(result.action_packet["cycle_id"], "worker-bad")

    def test_worker_prioritizes_lineage_before_delivery_and_reobserve(self):
        reobserve = dict(BASE_RAW)
        reobserve["cycle_id"] = "worker-reobserve"
        reobserve["physical_process_visible"] = False
        reobserve["thermodynamic_activity_visible"] = False
        delivery = dict(BASE_RAW)
        delivery["cycle_id"] = "worker-delivery"
        delivery["channel_scope"] = False
        lineage = dict(BASE_RAW)
        lineage["cycle_id"] = "worker-lineage"
        lineage["registry_key"] = False
        queue_state = make_queue_state_with(reobserve, delivery, lineage)
        result = process_next_queue_item(queue_state)
        self.assertEqual(result.selected_queue, "LINEAGE_RECHECK_QUEUE")
        self.assertEqual(result.action_packet["action_type"], "open_lineage_recheck_packet")
        self.assertEqual(result.action_packet["cycle_id"], "worker-lineage")

    def test_worker_skips_already_processed_receipts(self):
        queue_state = make_queue_state_with(BASE_RAW)
        first = process_next_queue_item(queue_state)
        second = process_next_queue_item(queue_state, first.updated_worker_state)
        self.assertEqual(second.worker_status, "NO_UNPROCESSED_QUEUE_ITEM")
        self.assertIsNone(second.action_packet)
        self.assertEqual(len(second.updated_worker_state["action_outbox"]), 1)

    def test_worker_appends_multiple_packets_without_deleting_queue_entries(self):
        raw1 = dict(BASE_RAW)
        raw1["cycle_id"] = "worker-1"
        raw2 = dict(BASE_RAW)
        raw2["cycle_id"] = "worker-2"
        raw2["generated_at_utc"] = "2026-05-21T00:01:00+00:00"
        queue_state = make_queue_state_with(raw1, raw2)
        original_queue_len = len(queue_state["queues"]["NEXT_NONFINAL_STAGE"])
        first = process_next_queue_item(queue_state)
        second = process_next_queue_item(queue_state, first.updated_worker_state)
        self.assertEqual(len(queue_state["queues"]["NEXT_NONFINAL_STAGE"]), original_queue_len)
        self.assertEqual(len(second.updated_worker_state["processed_receipt_hashes"]), 2)
        self.assertEqual(len(second.updated_worker_state["action_outbox"]), 2)
        self.assertEqual(len(second.updated_worker_state["worker_log"]), 2)

    def test_empty_worker_state_has_no_authority(self):
        state = empty_worker_state()
        self.assertEqual(state["processed_receipt_hashes"], [])
        self.assertEqual(state["action_outbox"], [])
        self.assertFalse(state["grants_execution_authority"])
        self.assertFalse(state["grants_truth_authority"])
        self.assertFalse(state["grants_final_commitment_authority"])
        self.assertFalse(state["grants_memory_overwrite_authority"])


if __name__ == "__main__":
    unittest.main()
