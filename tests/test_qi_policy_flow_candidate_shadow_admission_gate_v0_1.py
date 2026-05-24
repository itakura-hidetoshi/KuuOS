import unittest

from runtime.kuuos_runtime_daemon_qi_policy_flow_candidate_shadow_admission_gate_v0_1 import (
    compile_qi_policy_flow_candidate_shadow_admission,
)


BASE_SHADOW = {
    "shadow_decision": "QI_POLICY_FLOW_CANDIDATE_SHADOW_EVALUATED",
    "shadow_reason": "candidate_shadow_evaluated_nonexecuting",
    "candidate_shadow_score": 0.85,
    "candidate_shadow_grade": "strong_shadow_candidate",
    "candidate_action": "prefer_observation_candidate",
    "candidate_class": "CANDIDATE_ADJUSTMENT_INFORMATION_GAIN",
    "candidate_priority": "high",
    "positive_terms": ["policy_mutation_blocked", "belief_update_blocked", "precision_commit_blocked"],
    "warning_terms": [],
    "blocker_terms": [],
    "boundary_markers": {
        "append_only": True,
        "candidate_only": True,
        "nonfinal_marker": True,
        "no_policy_mutation": True,
        "no_belief_update": True,
        "no_precision_commit": True,
    },
    "shadow_only": True,
    "read_only": True,
    "candidate_only": True,
    "nonfinal_marker": True,
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
    "grants_completed_identity_authority": False,
}


def shadow(**updates):
    value = dict(BASE_SHADOW)
    if "boundary_markers" not in updates:
        value["boundary_markers"] = dict(BASE_SHADOW["boundary_markers"])
    value.update(updates)
    return value


class QiPolicyFlowCandidateShadowAdmissionGateTests(unittest.TestCase):
    def test_admits_scored_shadow_candidate_with_boundaries(self):
        result = compile_qi_policy_flow_candidate_shadow_admission(shadow_evaluation=BASE_SHADOW)
        self.assertEqual(result.shadow_admission_decision, "QI_POLICY_FLOW_SHADOW_CANDIDATE_ADMITTED")
        self.assertEqual(result.admitted_shadow_candidate_action, "prefer_observation_candidate")
        self.assertEqual(result.admitted_shadow_score, 0.85)
        self.assertEqual(result.gate_blockers, [])
        self.assertTrue(result.shadow_only)
        self.assertTrue(result.read_only)
        self.assertFalse(result.grants_execution_authority)

    def test_blocks_low_score(self):
        result = compile_qi_policy_flow_candidate_shadow_admission(
            shadow_evaluation=shadow(candidate_shadow_score=0.25)
        )
        self.assertEqual(result.shadow_admission_decision, "QI_POLICY_FLOW_SHADOW_CANDIDATE_NOT_ADMITTED")
        self.assertIn("shadow_score_below_minimum", result.gate_blockers)
        self.assertIsNone(result.admitted_shadow_candidate_action)

    def test_blocks_evaluator_blockers(self):
        result = compile_qi_policy_flow_candidate_shadow_admission(
            shadow_evaluation=shadow(blocker_terms=["required_boundary_missing"])
        )
        self.assertEqual(result.shadow_admission_decision, "QI_POLICY_FLOW_SHADOW_CANDIDATE_NOT_ADMITTED")
        self.assertIn("shadow_evaluator_blockers_present", result.gate_blockers)

    def test_blocks_missing_boundary(self):
        markers = dict(BASE_SHADOW["boundary_markers"])
        markers["no_precision_commit"] = False
        result = compile_qi_policy_flow_candidate_shadow_admission(
            shadow_evaluation=shadow(boundary_markers=markers)
        )
        self.assertEqual(result.shadow_admission_decision, "QI_POLICY_FLOW_SHADOW_CANDIDATE_NOT_ADMITTED")
        self.assertIn("boundary_missing:no_precision_commit", result.gate_blockers)

    def test_blocks_authority_grant(self):
        result = compile_qi_policy_flow_candidate_shadow_admission(
            shadow_evaluation=shadow(grants_truth_authority=True)
        )
        self.assertEqual(result.shadow_admission_decision, "QI_POLICY_FLOW_SHADOW_CANDIDATE_NOT_ADMITTED")
        self.assertIn("authority_grant_detected:grants_truth_authority", result.gate_blockers)
        self.assertFalse(result.grants_truth_authority)

    def test_blocks_missing_shadow_evaluation(self):
        result = compile_qi_policy_flow_candidate_shadow_admission(shadow_evaluation={})
        self.assertEqual(result.shadow_admission_decision, "QI_POLICY_FLOW_SHADOW_CANDIDATE_NOT_ADMITTED")
        self.assertIn("shadow_evaluation_missing", result.gate_blockers)


if __name__ == "__main__":
    unittest.main()
