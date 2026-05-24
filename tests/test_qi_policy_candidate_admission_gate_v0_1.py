import unittest

from runtime.kuuos_runtime_daemon_qi_policy_candidate_admission_gate_v0_1 import (
    compile_qi_policy_candidate_admission,
)


BASE_ADAPTER = {
    "candidate_adjustment_class": "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN",
    "recommended_candidate_action": "prefer_observation_candidate",
    "candidate_priority": "high",
    "candidate_only": True,
    "nonfinal_marker": True,
    "policy_candidate_constraints": ["candidate_only", "nonfinal_marker", "no_policy_mutation"],
    "active_inference_constraints": ["no_belief_update", "no_precision_commit"],
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}


def adapter(**updates):
    value = dict(BASE_ADAPTER)
    value.update(updates)
    return value


class QiPolicyCandidateAdmissionGateTests(unittest.TestCase):
    def test_admits_candidate_only_nonfinal_adapter(self):
        result = compile_qi_policy_candidate_admission(candidate_adapter=BASE_ADAPTER)
        self.assertEqual(result.admission_decision, "QI_POLICY_CANDIDATE_ADMITTED")
        self.assertEqual(result.admitted_candidate_action, "prefer_observation_candidate")
        self.assertEqual(result.gate_blockers, [])
        self.assertEqual(result.missing_constraints, [])
        self.assertTrue(result.candidate_only)
        self.assertTrue(result.nonfinal_marker)
        self.assertFalse(result.grants_execution_authority)

    def test_blocks_missing_candidate_only_flag(self):
        result = compile_qi_policy_candidate_admission(candidate_adapter=adapter(candidate_only=False))
        self.assertEqual(result.admission_decision, "QI_POLICY_CANDIDATE_NOT_ADMITTED")
        self.assertIn("candidate_only_missing_or_false", result.gate_blockers)
        self.assertIsNone(result.admitted_candidate_action)

    def test_blocks_missing_nonfinal_marker(self):
        result = compile_qi_policy_candidate_admission(candidate_adapter=adapter(nonfinal_marker=False))
        self.assertEqual(result.admission_decision, "QI_POLICY_CANDIDATE_NOT_ADMITTED")
        self.assertIn("nonfinal_marker_missing_or_false", result.gate_blockers)

    def test_blocks_missing_required_constraints(self):
        result = compile_qi_policy_candidate_admission(candidate_adapter=adapter(
            policy_candidate_constraints=["candidate_only"],
            active_inference_constraints=["no_belief_update"],
        ))
        self.assertEqual(result.admission_decision, "QI_POLICY_CANDIDATE_NOT_ADMITTED")
        self.assertIn("required_constraints_missing", result.gate_blockers)
        self.assertIn("no_policy_mutation", result.missing_constraints)
        self.assertIn("nonfinal_marker", result.missing_constraints)
        self.assertIn("no_precision_commit", result.missing_constraints)

    def test_blocks_authority_grant(self):
        result = compile_qi_policy_candidate_admission(candidate_adapter=adapter(grants_truth_authority=True))
        self.assertEqual(result.admission_decision, "QI_POLICY_CANDIDATE_NOT_ADMITTED")
        self.assertIn("authority_grant_detected:grants_truth_authority", result.gate_blockers)
        self.assertFalse(result.grants_truth_authority)

    def test_blocks_missing_adapter(self):
        result = compile_qi_policy_candidate_admission(candidate_adapter={})
        self.assertEqual(result.admission_decision, "QI_POLICY_CANDIDATE_NOT_ADMITTED")
        self.assertIn("candidate_adapter_missing", result.gate_blockers)


if __name__ == "__main__":
    unittest.main()
