import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKET = ROOT / "manifests" / "cbf_membrane_gap_kernel_established_packet_v1_0.json"


class CBFMembraneGapEstablishedPacketTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(PACKET.read_text(encoding="utf-8"))

    def test_packet_identity_is_fixed(self):
        self.assertEqual(
            self.data["packet_version"],
            "cbf_membrane_gap_kernel_established_packet_v1_0",
        )
        self.assertEqual(self.data["packet_status"], "established_baseline")

    def test_packet_registers_all_cbf_validation_surfaces(self):
        self.assertEqual(
            self.data["root_contract"],
            "manifests/cbf_membrane_gap_kernel_contract_v1_0.json",
        )
        self.assertEqual(
            self.data["validator"],
            "scripts/validate_cbf_membrane_gap_kernel_contract_v1_0.py",
        )
        self.assertEqual(
            self.data["validation_case_checker"],
            "scripts/check_cbf_membrane_gap_validation_cases_v1_0.py",
        )
        self.assertEqual(
            self.data["established_packet_validator"],
            "scripts/validate_cbf_membrane_gap_kernel_established_packet_v1_0.py",
        )
        self.assertIn(
            "tests/test_cbf_membrane_gap_kernel_contract_v1_0.py",
            self.data["tests"],
        )
        self.assertIn(
            "tests/test_cbf_membrane_gap_validation_cases_v1_0.py",
            self.data["tests"],
        )

    def test_packet_preserves_non_authoritative_baseline_statement(self):
        statement = self.data["baseline_statement"]
        self.assertIn("CBF pass is not truth", statement)
        self.assertIn("not execution", statement)
        self.assertIn("CBF fail is not falsity", statement)

    def test_packet_core_invariants_are_present(self):
        invariants = set(self.data["core_invariants"])
        self.assertIn("membrane_license_only", invariants)
        self.assertIn("hard_and_grave_margins_cannot_be_offset", invariants)
        self.assertIn("belief_pass_is_not_true_state_proof", invariants)
        self.assertIn("local_pass_is_not_global_pass", invariants)
        self.assertIn("cptp_pass_is_not_membrane_pass", invariants)
        self.assertIn("expectation_pass_is_not_strong_spectral_pass", invariants)
        self.assertIn("negative_spectral_mass_blocks_strong_pass", invariants)
        self.assertIn("domain_unclear_blocks_strong_pass", invariants)

    def test_packet_runtime_binding_does_not_expand_authority(self):
        runtime = self.data["runtime_binding"]
        self.assertEqual(runtime["hot_path"], "bounded_local_receipt_only")
        self.assertEqual(runtime["full_contract_validation"], "ci_or_governance_tier")
        self.assertFalse(runtime["runtime_authority_expansion"])

    def test_packet_update_policy_is_additive_and_tighten_only(self):
        policy = self.data["update_policy"]
        self.assertTrue(policy["additive_only"])
        self.assertTrue(policy["tighten_only_default"])
        self.assertTrue(policy["same_root_required"])
        self.assertTrue(policy["overwrite_forbidden"])


if __name__ == "__main__":
    unittest.main()
