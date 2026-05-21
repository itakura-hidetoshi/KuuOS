import unittest

from runtime.kuuos_action_router_v0_1 import empty_task_board, route_next_action
from runtime.kuuos_queue_dispatcher_v0_1 import dispatch_candidate_cycle, empty_queue_state
from runtime.kuuos_queue_worker_v0_1 import process_next_queue_item


BASE_RAW = {
    "cycle_id": "router-001",
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


def worker_state_for(raw):
    q = dispatch_candidate_cycle(raw, empty_queue_state()).updated_queue_state
    return process_next_queue_item(q).updated_worker_state


class KuuOSActionRouterTests(unittest.TestCase):
    def test_next_nonfinal_action_routes_to_candidate_next_tasks(self):
        worker = worker_state_for(BASE_RAW)
        result = route_next_action(worker)
        self.assertEqual(result.router_status, "ROUTED_ONE_APPEND_ONLY")
        self.assertEqual(result.target_task_queue, "candidate_next_tasks")
        self.assertEqual(len(result.updated_task_board["task_queues"]["candidate_next_tasks"]), 1)
        self.assertEqual(result.task_packet["task_status"], "OPEN_NON_AUTHORITATIVE")
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)
        self.assertFalse(result.grants_final_commitment_authority)
        self.assertFalse(result.grants_memory_overwrite_authority)

    def test_quarantine_action_routes_to_quarantine_tasks(self):
        raw = dict(BASE_RAW)
        raw["world_identity_blocker"] = False
        worker = worker_state_for(raw)
        result = route_next_action(worker)
        self.assertEqual(result.target_task_queue, "quarantine_tasks")
        self.assertEqual(result.task_packet["task_type"], "open_quarantine_review_packet")
        self.assertIn("world_identity_blocker", result.task_packet["blocked_boundaries"])

    def test_lineage_action_routes_to_lineage_tasks(self):
        raw = dict(BASE_RAW)
        raw["registry_key"] = False
        worker = worker_state_for(raw)
        result = route_next_action(worker)
        self.assertEqual(result.target_task_queue, "lineage_recheck_tasks")
        self.assertEqual(result.task_packet["task_type"], "open_lineage_recheck_packet")

    def test_delivery_action_routes_to_delivery_tasks(self):
        raw = dict(BASE_RAW)
        raw["acknowledgment_marker"] = False
        worker = worker_state_for(raw)
        result = route_next_action(worker)
        self.assertEqual(result.target_task_queue, "delivery_recheck_tasks")
        self.assertEqual(result.task_packet["task_type"], "open_delivery_recheck_packet")

    def test_reobserve_action_routes_to_reobserve_tasks(self):
        raw = dict(BASE_RAW)
        raw["physical_process_visible"] = False
        raw["thermodynamic_activity_visible"] = False
        worker = worker_state_for(raw)
        result = route_next_action(worker)
        self.assertEqual(result.target_task_queue, "reobserve_tasks")
        self.assertEqual(result.task_packet["task_type"], "open_reobserve_packet")

    def test_router_skips_already_routed_action(self):
        worker = worker_state_for(BASE_RAW)
        first = route_next_action(worker)
        second = route_next_action(worker, first.updated_task_board)
        self.assertEqual(second.router_status, "NO_UNROUTED_ACTION_PACKET")
        self.assertIsNone(second.task_packet)
        self.assertEqual(len(second.updated_task_board["routed_action_hashes"]), 1)

    def test_router_appends_multiple_actions(self):
        worker1 = worker_state_for(BASE_RAW)
        raw2 = dict(BASE_RAW)
        raw2["cycle_id"] = "router-002"
        raw2["generated_at_utc"] = "2026-05-21T00:01:00+00:00"
        worker2 = worker_state_for(raw2)
        combined_worker = dict(worker1)
        combined_worker["action_outbox"] = worker1["action_outbox"] + worker2["action_outbox"]
        first = route_next_action(combined_worker)
        second = route_next_action(combined_worker, first.updated_task_board)
        self.assertEqual(len(second.updated_task_board["routed_action_hashes"]), 2)
        self.assertEqual(len(second.updated_task_board["router_log"]), 2)
        self.assertEqual(len(second.updated_task_board["task_queues"]["candidate_next_tasks"]), 2)

    def test_empty_task_board_has_no_authority(self):
        board = empty_task_board()
        self.assertIn("candidate_next_tasks", board["task_queues"])
        self.assertIn("quarantine_tasks", board["task_queues"])
        self.assertFalse(board["grants_execution_authority"])
        self.assertFalse(board["grants_truth_authority"])
        self.assertFalse(board["grants_final_commitment_authority"])
        self.assertFalse(board["grants_memory_overwrite_authority"])


if __name__ == "__main__":
    unittest.main()
