import unittest

from runtime.kuuos_runtime_daemon_four_image_phase_gauge_v0_1 import evaluate_daemon_four_image_phase


def yy(state, yin=0.4, yang=0.4, balance=1.0, switch=0.0, hint="CONTINUE_HARMONIZED"):
    return {
        "yinyang_polarity_state": state,
        "yin_load": yin,
        "yang_drive": yang,
        "polarity_balance": balance,
        "switch_risk": switch,
        "recommended_policy_hint": hint,
    }


class DaemonFourImagePhaseGaugeTests(unittest.TestCase):
    def test_balanced_light_yang(self):
        result = evaluate_daemon_four_image_phase(yy("BALANCED_FLOW", yin=0.35, yang=0.45))
        self.assertEqual(result.four_image_phase, "LESSER_YANG")
        self.assertEqual(result.phase_policy_hint, "CONTINUE_HARMONIZED")
        self.assertEqual(result.phase_reason, "balanced_flow_with_light_yang")
        self.assertFalse(result.grants_execution_authority)
        self.assertFalse(result.grants_truth_authority)

    def test_balanced_light_yin(self):
        result = evaluate_daemon_four_image_phase(yy("BALANCED_FLOW", yin=0.5, yang=0.35))
        self.assertEqual(result.four_image_phase, "LESSER_YIN")
        self.assertEqual(result.phase_policy_hint, "CONTINUE_WITH_COMPACT_MONITOR")
        self.assertEqual(result.phase_reason, "balanced_flow_with_light_yin")

    def test_yang_overdrive_becomes_greater_yang(self):
        result = evaluate_daemon_four_image_phase(yy("YANG_OVERDRIVE", yin=0.1, yang=0.9, hint="SLOW_DOWN_AND_REOBSERVE"))
        self.assertEqual(result.four_image_phase, "GREATER_YANG")
        self.assertEqual(result.phase_policy_hint, "SLOW_DOWN_AND_REOBSERVE")
        self.assertEqual(result.phase_reason, "yang_matured_into_overdrive")
        self.assertGreater(result.phase_maturity_score, 0.8)

    def test_yin_stagnation_becomes_greater_yin(self):
        result = evaluate_daemon_four_image_phase(yy("YIN_STAGNATION", yin=0.9, yang=0.1, hint="BRANCH_EXPLORE_LIGHTLY"))
        self.assertEqual(result.four_image_phase, "GREATER_YIN")
        self.assertEqual(result.phase_policy_hint, "REOPEN_RECOVERY_PATH")
        self.assertEqual(result.phase_reason, "yin_matured_into_stagnation")

    def test_false_yang_requires_reobserve(self):
        result = evaluate_daemon_four_image_phase(yy("FALSE_YANG", yin=0.5, yang=0.5, hint="REOBSERVE_QI_PROCESS"))
        self.assertEqual(result.four_image_phase, "GREATER_YANG")
        self.assertEqual(result.phase_policy_hint, "REOBSERVE_WITH_NON_REIFICATION")
        self.assertEqual(result.phase_reason, "yang_claim_requires_reobservation")

    def test_switching_unstable_becomes_greater_yin(self):
        result = evaluate_daemon_four_image_phase(yy("SWITCHING_UNSTABLE", yin=0.5, yang=0.5, switch=0.8, hint="HOLD_WITH_RECOVERY"))
        self.assertEqual(result.four_image_phase, "GREATER_YIN")
        self.assertEqual(result.phase_policy_hint, "HOLD_WITH_RECOVERY")
        self.assertGreater(result.phase_maturity_score, 0.7)

    def test_recovery_yang_becomes_lesser_yang(self):
        result = evaluate_daemon_four_image_phase(yy("RECOVERY_YANG_PRESENT", yin=0.45, yang=0.55, hint="CONTINUE_WITH_QI_MEMORY_MONITOR"))
        self.assertEqual(result.four_image_phase, "LESSER_YANG")
        self.assertEqual(result.phase_policy_hint, "CONTINUE_WITH_QI_MEMORY_MONITOR")
        self.assertEqual(result.phase_reason, "recovery_yang_present_but_not_overdrive")

    def test_boundary_yin_required_becomes_lesser_yin(self):
        result = evaluate_daemon_four_image_phase(yy("BOUNDARY_YIN_REQUIRED", yin=1.0, yang=0.0, hint="QUARANTINE_REVIEW"))
        self.assertEqual(result.four_image_phase, "LESSER_YIN")
        self.assertEqual(result.phase_policy_hint, "QUARANTINE_REVIEW")
        self.assertEqual(result.phase_reason, "yin_observation_or_boundary_required")


if __name__ == "__main__":
    unittest.main()
