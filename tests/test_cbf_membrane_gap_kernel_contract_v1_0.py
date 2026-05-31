import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "manifests" / "cbf_membrane_gap_kernel_contract_v1_0.json"


class CBFMembraneGapKernelContractTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_contract_is_non_authoritative_membrane_license(self):
        self.assertEqual(
            self.data["contract_status"],
            "active_non_authoritative_membrane_license_kernel",
        )
        boundary = self.data["authority_boundary"]
        self.assertTrue(boundary["membrane_license_only"])
        self.assertFalse(boundary["cbf_truth_authority"])
        self.assertFalse(boundary["cbf_execute_authority"])
        self.assertFalse(boundary["cbf_final_commitment_authority"])
        self.assertFalse(boundary["cbf_memory_overwrite_authority"])
        self.assertFalse(boundary["cbf_theorem_authority"])
        self.assertFalse(boundary["cbf_clinical_authority"])

    def test_hard_and_grave_membranes_cannot_be_offset(self):
        tier_by_name = {tier["tier"]: tier for tier in self.data["membrane_tiers"]}
        for tier_name in ["grave", "hard"]:
            tier = tier_by_name[tier_name]
            self.assertFalse(tier["slack_allowed"])
            self.assertFalse(tier["average_offset_allowed"])
            self.assertFalse(tier["score_offset_allowed"])

    def test_core_decisions_include_hold_block_and_projection(self):
        decisions = set(self.data["decision_enum"])
        self.assertIn("PASS_PROJECTED", decisions)
        self.assertIn("REOBSERVE_REQUIRED", decisions)
        self.assertIn("REDECOMPOSE_REQUIRED", decisions)
        self.assertIn("BLOCK_MEMBRANE_BREACH", decisions)
        self.assertIn("BLOCK_NEGATIVE_SPECTRAL_MASS", decisions)
        self.assertIn("BLOCK_AUTHORITY_BOUNDARY", decisions)

    def test_forbidden_claims_block_authority_collapse(self):
        forbidden = set(self.data["forbidden_receipt_claims"])
        self.assertIn("grants_execution_authority", forbidden)
        self.assertIn("grants_truth_authority", forbidden)
        self.assertIn("proves_global_safety_from_local_pass_only", forbidden)
        self.assertIn("proves_strong_spectral_safety_from_expectation_only", forbidden)

    def test_runtime_tiering_cannot_open_execution_authority(self):
        tiering = self.data["runtime_tiering"]
        self.assertEqual(tiering["runtime_emit_tier"], "T0_hot_path_guard")
        self.assertFalse(tiering["may_open_execution_authority"])


if __name__ == "__main__":
    unittest.main()
