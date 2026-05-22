import unittest

from runtime.kuuos_runtime_daemon_active_inference_feature_compiler_v0_1 import compile_active_inference_features

QI_SUMMARY = {
    "process_tensor_visible": True,
    "transition_continuity_visible": True,
    "memory_continuity_visible": True,
    "nonmarkov_memory_visible": True,
    "process_history_length": 3,
    "transition_support_count": 2,
    "memory_support_count": 1,
    "nonmarkov_support_count": 1,
    "missing_process_requirements": [],
    "process_tensor_reason": "process_tensor_support_visible",
}

YINYANG = {
    "yinyang_polarity_state": "RECOVERY_YANG_PRESENT",
    "yin_load": 0.5,
    "yang_drive": 0.6,
    "recommended_policy_hint": "CONTINUE_WITH_QI_MEMORY_MONITOR",
}

FOUR = {
    "four_image_phase": "LESSER_YANG",
    "phase_policy_hint": "CONTINUE_WITH_QI_MEMORY_MONITOR",
}

POLICY = {
    "recommended_tick_mode": "CONTINUE_WITH_QI_MEMORY_MONITOR",
    "daemon_qique_gauge": {
        "qique_regime": "NONMARKOV_MEMORY_ACTIVE",
        "recovery_budget_pressure": 0.1,
    },
}

EMPTINESS = {
    "recommended_emptiness_action": "CONTINUE_ADVISORY_ONLY",
}

WA = {
    "recommended_runtime_posture": "CONTINUE_HARMONIZED",
}


class ActiveInferenceFeatureCompilerTests(unittest.TestCase):
    def test_primary_qi_is_kernel_input_and_lenses_are_advisory(self):
        result = compile_active_inference_features(
            qi_process_tensor_summary=QI_SUMMARY,
            yinyang_result=YINYANG,
            four_image_result=FOUR,
            qi_policy_result=POLICY,
            emptiness_result=EMPTINESS,
            wa_result=WA,
            tick_density=2,
        )
        self.assertEqual(result.compiler_status, "FEATURES_COMPILED_WITH_PRIMARY_QI")
        self.assertEqual(result.primary_qi_process_tensor["process_tensor_visible"], True)
        self.assertEqual(result.active_inference_inputs["process_history_length"], 3)
        self.assertEqual(result.active_inference_inputs["yinyang_polarity_state"], "RECOVERY_YANG_PRESENT")
        self.assertEqual(result.active_inference_inputs["four_image_phase"], "LESSER_YANG")
        self.assertEqual(result.active_inference_inputs["qique_regime"], "NONMARKOV_MEMORY_ACTIVE")
        self.assertIn("feature_advisory_not_policy", result.allowed_projection)
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)

    def test_boundary_constraint_compiles_as_hard_constraint(self):
        yy = dict(YINYANG)
        yy["yinyang_polarity_state"] = "BOUNDARY_YIN_REQUIRED"
        policy = dict(POLICY)
        policy["recommended_tick_mode"] = "QUARANTINE_REVIEW"
        emptiness = dict(EMPTINESS)
        emptiness["recommended_emptiness_action"] = "HOLD_OR_QUARANTINE_NONFINAL"
        result = compile_active_inference_features(
            qi_process_tensor_summary=QI_SUMMARY,
            yinyang_result=yy,
            four_image_result=FOUR,
            qi_policy_result=policy,
            emptiness_result=emptiness,
            wa_result={"recommended_runtime_posture": "QUARANTINE_WITH_RETURN_PATH"},
            tick_density=1,
        )
        self.assertTrue(result.hard_constraints["boundary_hard_constraint"])
        self.assertTrue(result.hard_constraints["reification_hard_constraint"])
        self.assertEqual(result.preference_priors["wa_preferred_posture"], "QUARANTINE_WITH_RETURN_PATH")

    def test_missing_primary_qi_keeps_lenses_optional(self):
        result = compile_active_inference_features(
            qi_process_tensor_summary=None,
            yinyang_result=YINYANG,
            four_image_result=FOUR,
            qi_policy_result=POLICY,
            emptiness_result=EMPTINESS,
            wa_result=WA,
            tick_density=0,
        )
        self.assertEqual(result.compiler_status, "FEATURES_COMPILED_WITHOUT_PRIMARY_QI")
        self.assertIsNone(result.primary_qi_process_tensor)
        self.assertTrue(result.hard_constraints["observation_hard_constraint"])
        self.assertIn("qi_process_tensor_summary", result.hard_constraints["missing_requirements"])
        self.assertGreaterEqual(result.missing_source_count, 1)

    def test_four_image_and_wa_compile_to_preference_priors(self):
        result = compile_active_inference_features(
            qi_process_tensor_summary=QI_SUMMARY,
            yinyang_result=YINYANG,
            four_image_result={"four_image_phase": "GREATER_YIN"},
            qi_policy_result=POLICY,
            emptiness_result=EMPTINESS,
            wa_result={"recommended_runtime_posture": "HOLD_WITH_RECOVERY"},
            tick_density=1,
        )
        self.assertTrue(result.preference_priors["prefer_recovery_path"])
        self.assertFalse(result.preference_priors["avoid_nihilism"])

    def test_density_prior_compiles_from_tick_and_phase(self):
        result = compile_active_inference_features(
            qi_process_tensor_summary=QI_SUMMARY,
            yinyang_result=YINYANG,
            four_image_result={"four_image_phase": "GREATER_YANG"},
            qi_policy_result=POLICY,
            emptiness_result=EMPTINESS,
            wa_result=WA,
            tick_density=7,
        )
        self.assertTrue(result.preference_priors["prefer_compact_when_dense"])
        self.assertEqual(result.active_inference_inputs["tick_density"], 7)


if __name__ == "__main__":
    unittest.main()
