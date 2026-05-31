import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
CASES = ROOT / "manifests" / "cbf_membrane_gap_kernel_validation_cases_v1_0.json"


class CBFMembraneGapValidationCasesTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(CASES.read_text(encoding="utf-8"))
        self.case_by_id = {case["case_id"]: case for case in self.data["cases"]}

    def expected(self, case_id):
        return self.case_by_id[case_id]["expected"]

    def test_version_is_fixed(self):
        self.assertEqual(
            self.data["validation_cases_version"],
            "cbf_membrane_gap_kernel_validation_cases_v1_0",
        )

    def test_cbf_pass_does_not_grant_execution_or_truth(self):
        execution = self.expected("cbf_pass_does_not_grant_execution")
        truth = self.expected("cbf_pass_does_not_grant_truth")
        self.assertFalse(execution["allowed"])
        self.assertEqual(execution["decision"], "BLOCK_AUTHORITY_BOUNDARY")
        self.assertFalse(truth["allowed"])
        self.assertEqual(truth["decision"], "BLOCK_AUTHORITY_BOUNDARY")

    def test_grave_negative_margin_cannot_be_averaged_away(self):
        expected = self.expected("grave_membrane_negative_margin_not_offset_by_average")
        self.assertFalse(expected["allowed"])
        self.assertEqual(expected["decision"], "BLOCK_MEMBRANE_BREACH")
        self.assertEqual(
            expected["reason_code"],
            "NEGATIVE_GRAVE_MARGIN_CANNOT_BE_AVERAGED_AWAY",
        )

    def test_local_pass_does_not_grant_global_pass(self):
        expected = self.expected("local_pass_does_not_grant_global_pass")
        self.assertFalse(expected["allowed"])
        self.assertEqual(expected["decision"], "LOCAL_PASS_GLOBAL_HOLD")
        self.assertEqual(expected["reason_code"], "GLUING_REQUIRED_FOR_GLOBAL_LICENSE")

    def test_cptp_pass_is_not_membrane_pass(self):
        expected = self.expected("cptp_pass_does_not_grant_membrane_pass")
        self.assertFalse(expected["allowed"])
        self.assertEqual(expected["decision"], "BLOCK_MEMBRANE_BREACH")
        self.assertEqual(expected["reason_code"], "CPTP_PASS_IS_NOT_MEMBRANE_PASS")

    def test_positive_expectation_cannot_mask_negative_spectral_mass(self):
        expected = self.expected("positive_expectation_cannot_mask_negative_spectral_mass")
        self.assertFalse(expected["allowed"])
        self.assertEqual(expected["decision"], "BLOCK_NEGATIVE_SPECTRAL_MASS")
        self.assertEqual(
            expected["reason_code"],
            "POSITIVE_EXPECTATION_CANNOT_MASK_NEGATIVE_SPECTRAL_MASS",
        )

    def test_domain_unclear_blocks_strong_pass(self):
        expected = self.expected("domain_unclear_blocks_strong_pass")
        self.assertFalse(expected["allowed"])
        self.assertEqual(expected["decision"], "HOLD_DOMAIN_UNCLEAR")
        self.assertEqual(expected["reason_code"], "UNBOUNDED_OPERATOR_DOMAIN_UNCLEAR")

    def test_projection_distortion_too_large_requires_handover(self):
        expected = self.expected("projected_pass_with_large_distortion_is_hold")
        self.assertFalse(expected["allowed"])
        self.assertEqual(expected["decision"], "HANDOVER_REQUIRED")
        self.assertEqual(expected["reason_code"], "PROJECTION_DISTORTION_TOO_LARGE")


if __name__ == "__main__":
    unittest.main()
