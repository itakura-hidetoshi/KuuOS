import unittest

from runtime.qi_total_field_v0_1 import evaluate_qi_total_field, normalize_qi_total_field


BASE_RAW = {
    "cycle_id": "total-qi-001",
    "kernel_state": "candidate",
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


class QiTotalFieldTests(unittest.TestCase):
    def test_physical_qi_supports_runtime_and_value(self):
        raw = dict(BASE_RAW)
        raw["physical_process_visible"] = True
        raw["thermodynamic_activity_visible"] = True
        raw["process_tensor_visible"] = True
        normalized = normalize_qi_total_field(raw)
        self.assertTrue(normalized["runtime_variation_visible"])
        self.assertTrue(normalized["value_witness_receipt"])
        self.assertTrue(normalized["policy_candidate_receipt"])

    def test_total_field_allows_candidate_when_sources_cover_all_inputs(self):
        raw = dict(BASE_RAW)
        raw["physical_process_visible"] = True
        raw["process_tensor_visible"] = True
        result = evaluate_qi_total_field(raw)
        self.assertEqual(result.qi_cycle_decision["qi_signal"], "ALLOW_CANDIDATE")
        self.assertEqual(result.qi_cycle_decision["next_stage"], "NEXT_NONFINAL_STAGE")
        self.assertIn("physical_process_visible", result.source_support["physical_qi"])
        self.assertIn("process_tensor_visible", result.source_support["process_qi"])

    def test_physical_qi_cannot_override_boundary_failure(self):
        raw = dict(BASE_RAW)
        raw["physical_process_visible"] = True
        raw["process_tensor_visible"] = True
        raw["two_truths_gap"] = False
        result = evaluate_qi_total_field(raw)
        self.assertEqual(result.qi_cycle_decision["qi_signal"], "QUARANTINE")
        self.assertIn("two_truths_gap", result.qi_cycle_decision["blocked_boundaries"])

    def test_process_qi_without_physical_qi_still_needs_value_support(self):
        raw = dict(BASE_RAW)
        raw["process_tensor_visible"] = True
        result = evaluate_qi_total_field(raw)
        self.assertEqual(result.qi_cycle_decision["qi_signal"], "REOBSERVE")
        self.assertIn("value_witness_receipt", result.qi_cycle_decision["missing_inputs"])

    def test_lineage_gap_routes_to_lineage_recheck(self):
        raw = dict(BASE_RAW)
        raw["physical_process_visible"] = True
        raw["process_tensor_visible"] = True
        raw["registry_key"] = False
        result = evaluate_qi_total_field(raw)
        self.assertEqual(result.qi_cycle_decision["qi_signal"], "LINEAGE_RECHECK")
        self.assertEqual(result.qi_cycle_decision["next_stage"], "LINEAGE_RECHECK_QUEUE")

    def test_delivery_gap_routes_to_delivery_recheck(self):
        raw = dict(BASE_RAW)
        raw["physical_process_visible"] = True
        raw["process_tensor_visible"] = True
        raw["acknowledgment_marker"] = False
        result = evaluate_qi_total_field(raw)
        self.assertEqual(result.qi_cycle_decision["qi_signal"], "DELIVERY_RECHECK")
        self.assertEqual(result.qi_cycle_decision["next_stage"], "DELIVERY_RECHECK_QUEUE")

    def test_forbidden_authority_projection_quarantines(self):
        raw = dict(BASE_RAW)
        raw["physical_process_visible"] = True
        raw["process_tensor_visible"] = True
        raw["truth_commit"] = True
        result = evaluate_qi_total_field(raw)
        self.assertEqual(result.qi_cycle_decision["qi_signal"], "QUARANTINE")
        self.assertIn("truth_commit", result.qi_cycle_decision["blocked_boundaries"])


if __name__ == "__main__":
    unittest.main()
