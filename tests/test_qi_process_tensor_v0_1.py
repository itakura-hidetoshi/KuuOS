import unittest

from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor, enrich_state_with_qi_process_tensor
from runtime.qi_total_field_v0_1 import evaluate_qi_total_field, normalize_qi_total_field


BASE_RAW = {
    "cycle_id": "process-tensor-001",
    "candidate_only": True,
    "nonfinal_marker": True,
    "two_truths_gap": True,
    "noncollapse_guard": True,
    "memory_overwrite_blocker": True,
    "world_identity_blocker": True,
    "barrier_witness_visible": True,
    "receipt_hash": True,
    "support_refs": True,
    "registry_key": True,
    "view_delivery_receipt": True,
    "channel_scope": True,
    "acknowledgment_marker": True,
}

PROCESS_HISTORY = [
    {
        "step_id": "p0",
        "process_observation": "seed",
        "transition_visible": True,
        "memory_link_visible": True,
        "nonmarkov_link_visible": False,
    },
    {
        "step_id": "p1",
        "process_observation": "candidate_motion",
        "transition_visible": True,
        "memory_link_visible": False,
        "nonmarkov_link_visible": False,
    },
    {
        "step_id": "p2",
        "process_observation": "history_reentry",
        "transition_visible": True,
        "memory_link_visible": False,
        "nonmarkov_link_visible": True,
    },
]


class QiProcessTensorTests(unittest.TestCase):
    def test_process_history_generates_process_tensor_support(self):
        raw = dict(BASE_RAW)
        raw["process_history"] = list(PROCESS_HISTORY)
        receipt = evaluate_qi_process_tensor(raw)
        self.assertTrue(receipt.process_tensor_visible)
        self.assertTrue(receipt.transition_continuity_visible)
        self.assertTrue(receipt.memory_continuity_visible)
        self.assertTrue(receipt.nonmarkov_memory_visible)
        self.assertEqual(receipt.process_history_length, 3)
        self.assertEqual(receipt.transition_support_count, 3)
        self.assertEqual(receipt.memory_support_count, 1)
        self.assertEqual(receipt.nonmarkov_support_count, 1)
        self.assertEqual(receipt.process_tensor_reason, "process_tensor_support_visible")
        self.assertFalse(receipt.grants_execution_authority)
        self.assertFalse(receipt.grants_truth_authority)
        self.assertFalse(receipt.grants_final_commitment_authority)
        self.assertFalse(receipt.grants_memory_overwrite_authority)

    def test_process_tensor_enriches_state_for_total_field(self):
        raw = dict(BASE_RAW)
        raw["process_history"] = list(PROCESS_HISTORY)
        enriched = enrich_state_with_qi_process_tensor(raw)
        self.assertTrue(enriched["process_tensor_visible"])
        self.assertTrue(enriched["transition_continuity_visible"])
        self.assertTrue(enriched["memory_continuity_visible"])
        self.assertTrue(enriched["nonmarkov_memory_visible"])
        normalized = normalize_qi_total_field(raw)
        self.assertTrue(normalized["runtime_variation_visible"])
        self.assertTrue(normalized["policy_candidate_receipt"])

    def test_total_field_uses_process_history_without_explicit_flag(self):
        raw = dict(BASE_RAW)
        raw["process_history"] = list(PROCESS_HISTORY)
        raw["physical_process_visible"] = True
        result = evaluate_qi_total_field(raw)
        self.assertEqual(result.qi_cycle_decision["qi_signal"], "ALLOW_CANDIDATE")
        self.assertIn("process_tensor_visible", result.source_support["process_qi"])
        self.assertIn("nonmarkov_memory_visible", result.source_support["process_qi"])
        self.assertEqual(result.qi_total_reason, "normalized_total_qi_field_with_process_tensor_then_ran_qi_cycle")

    def test_total_field_exposes_process_tensor_receipt(self):
        raw = dict(BASE_RAW)
        raw["process_history"] = list(PROCESS_HISTORY)
        raw["physical_process_visible"] = True
        result = evaluate_qi_total_field(raw)
        receipt = result.qi_process_tensor_receipt
        self.assertTrue(receipt["process_tensor_visible"])
        self.assertTrue(receipt["transition_continuity_visible"])
        self.assertTrue(receipt["memory_continuity_visible"])
        self.assertTrue(receipt["nonmarkov_memory_visible"])
        self.assertEqual(receipt["process_history_length"], 3)
        self.assertEqual(receipt["transition_support_count"], 3)
        self.assertEqual(receipt["memory_support_count"], 1)
        self.assertEqual(receipt["nonmarkov_support_count"], 1)
        self.assertEqual(receipt["process_tensor_reason"], "process_tensor_support_visible")
        self.assertFalse(receipt["grants_execution_authority"])
        self.assertFalse(receipt["grants_truth_authority"])
        self.assertFalse(receipt["grants_final_commitment_authority"])
        self.assertFalse(receipt["grants_memory_overwrite_authority"])

    def test_boundary_failure_blocks_process_tensor_support(self):
        raw = dict(BASE_RAW)
        raw["process_history"] = list(PROCESS_HISTORY)
        raw["two_truths_gap"] = False
        receipt = evaluate_qi_process_tensor(raw)
        self.assertFalse(receipt.process_tensor_visible)
        self.assertEqual(receipt.process_tensor_reason, "boundary_blocks_process_tensor_support")
        self.assertIn("boundary_fields_visible", receipt.missing_process_requirements)

    def test_total_field_exposes_blocked_process_tensor_receipt(self):
        raw = dict(BASE_RAW)
        raw["process_history"] = list(PROCESS_HISTORY)
        raw["physical_process_visible"] = True
        raw["two_truths_gap"] = False
        result = evaluate_qi_total_field(raw)
        receipt = result.qi_process_tensor_receipt
        self.assertFalse(receipt["process_tensor_visible"])
        self.assertEqual(receipt["process_tensor_reason"], "boundary_blocks_process_tensor_support")
        self.assertIn("boundary_fields_visible", receipt["missing_process_requirements"])
        self.assertEqual(result.qi_cycle_decision["qi_signal"], "QUARANTINE")

    def test_short_history_requires_explicit_process_tensor_or_waits(self):
        raw = dict(BASE_RAW)
        raw["process_history"] = [PROCESS_HISTORY[0]]
        receipt = evaluate_qi_process_tensor(raw)
        self.assertFalse(receipt.process_tensor_visible)
        self.assertIn("process_history_min_length_or_explicit_process_tensor", receipt.missing_process_requirements)
        self.assertIn("transition_continuity_visible", receipt.missing_process_requirements)

    def test_explicit_process_tensor_still_non_authoritative(self):
        raw = dict(BASE_RAW)
        raw["process_tensor_visible"] = True
        raw["transition_continuity_visible"] = True
        raw["memory_continuity_visible"] = True
        receipt = evaluate_qi_process_tensor(raw)
        self.assertTrue(receipt.process_tensor_visible)
        self.assertFalse(receipt.grants_execution_authority)
        self.assertFalse(receipt.grants_truth_authority)


if __name__ == "__main__":
    unittest.main()
