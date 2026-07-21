from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_environment_capsule_livelock_efficiency_gate_v0_1 import *
from scripts.build_codeai_environment_capsule_livelock_efficiency_gate_fixture_v0_1 import build_reference_fixture


class EnvironmentCapsuleLivelockEfficiencyGateTests(unittest.TestCase):
    def fixture(self):
        return deepcopy(build_reference_fixture())

    def run_fixture(self, fixture):
        return build_codeai_environment_capsule_livelock_efficiency_gate(
            request=fixture["request"],
            policy=fixture["policy"],
            router_admission=fixture["router_admission"],
            environment_capsule=fixture["environment_capsule"],
            progress_trace=fixture["progress_trace"],
        )

    def reseal(self, value, field):
        value.pop(field, None)
        value.update(seal(value, field))

    def reseal_capsule_and_trace(self, fixture):
        self.reseal(fixture["environment_capsule"], CAPSULE_DIGEST_FIELD)
        fixture["progress_trace"]["environment_capsule_digest"] = fixture["environment_capsule"][CAPSULE_DIGEST_FIELD]
        self.reseal(fixture["progress_trace"], TRACE_DIGEST_FIELD)

    def test_reference_admits_progress_efficiency(self):
        pack = self.fixture()["gate_pack"]
        self.assertEqual(pack["gate_decision"], DECISION_CONTINUE)
        self.assertEqual(pack["hold_reasons"], [])
        self.assertTrue(pack["environment_exact"])
        self.assertTrue(pack["capsule_reproducible"])
        self.assertTrue(pack["livelock_free"])
        self.assertTrue(pack["efficiency_within_budget"])
        self.assertEqual(pack["step_count"], 6)
        self.assertEqual(pack["total_progress_units"], 20)

    def test_result_preserves_no_effect_boundary(self):
        pack = self.fixture()["gate_pack"]
        self.assertTrue(pack["continuation_hint_only"])
        for field in (
            "continuation_authority_granted",
            "execution_authority_granted",
            "repository_mutation_performed",
            "git_authority_granted",
            "correctness_claimed",
        ):
            self.assertFalse(pack[field])

    def test_tampered_capsule_digest_blocks(self):
        fixture = self.fixture()
        fixture["environment_capsule"]["timezone"] = "Asia/Tokyo"
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("capsule_digest_mismatch", result.issues)

    def test_tampered_trace_digest_blocks(self):
        fixture = self.fixture()
        fixture["progress_trace"]["checkpoints"][0]["progress_units"] += 1
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("trace_digest_mismatch", result.issues)

    def test_capsule_binding_mismatch_blocks(self):
        fixture = self.fixture()
        fixture["environment_capsule"]["source_tree_digest"] = "1" * 64
        self.reseal_capsule_and_trace(fixture)
        result = self.run_fixture(fixture)
        self.assertTrue(any(issue.startswith("capsule_binding_mismatch:source_tree_digest") for issue in result.issues))

    def test_trace_binding_mismatch_blocks(self):
        fixture = self.fixture()
        fixture["progress_trace"]["gate_policy_digest"] = "2" * 64
        self.reseal(fixture["progress_trace"], TRACE_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertTrue(any(issue.startswith("trace_binding_mismatch:gate_policy_digest") for issue in result.issues))

    def test_router_manifest_tamper_blocks(self):
        fixture = self.fixture()
        fixture["router_admission"]["route_decision"] = "specialist_route_held"
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("router_manifest_digest_mismatch", result.issues)
        self.assertIn("router_route_not_admitted", result.issues)

    def test_network_enabled_holds(self):
        fixture = self.fixture()
        fixture["environment_capsule"]["network_access_allowed"] = True
        self.reseal_capsule_and_trace(fixture)
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.gate_pack["gate_decision"], DECISION_HOLD)
        self.assertIn("environment_capsule_network_enabled", result.gate_pack["hold_reasons"])

    def test_mutable_root_holds(self):
        fixture = self.fixture()
        fixture["environment_capsule"]["root_filesystem_immutable"] = False
        self.reseal_capsule_and_trace(fixture)
        result = self.run_fixture(fixture)
        self.assertIn("environment_capsule_not_immutable", result.gate_pack["hold_reasons"])

    def test_unverified_dependency_lock_holds(self):
        fixture = self.fixture()
        fixture["environment_capsule"]["dependency_lock_verified"] = False
        self.reseal_capsule_and_trace(fixture)
        result = self.run_fixture(fixture)
        self.assertIn("environment_dependency_lock_unverified", result.gate_pack["hold_reasons"])

    def test_self_report_only_capsule_holds(self):
        fixture = self.fixture()
        fixture["environment_capsule"]["self_report_only"] = True
        self.reseal_capsule_and_trace(fixture)
        result = self.run_fixture(fixture)
        self.assertIn("environment_capsule_self_report_only", result.gate_pack["hold_reasons"])

    def test_self_report_only_trace_holds(self):
        fixture = self.fixture()
        fixture["progress_trace"]["self_report_only"] = True
        self.reseal(fixture["progress_trace"], TRACE_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("progress_trace_self_report_only", result.gate_pack["hold_reasons"])

    def test_cycle_detected_holds(self):
        fixture = self.fixture()
        checkpoint = fixture["progress_trace"]["checkpoints"][2]
        checkpoint["progress_units"] = 0
        checkpoint["state_after_digest"] = fixture["progress_trace"]["checkpoints"][0]["state_before_digest"]
        self.reseal(fixture["progress_trace"], TRACE_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertEqual(result.gate_pack["gate_decision"], DECISION_HOLD)
        self.assertIn("livelock_cycle_detected", result.gate_pack["hold_reasons"])
        self.assertFalse(result.gate_pack["livelock_free"])

    def test_repeated_zero_progress_transition_holds(self):
        fixture = self.fixture()
        first = fixture["progress_trace"]["checkpoints"][2]
        second = fixture["progress_trace"]["checkpoints"][3]
        first["progress_units"] = 0
        second["progress_units"] = 0
        for field in ("state_before_digest", "action_digest", "state_after_digest"):
            second[field] = first[field]
        self.reseal(fixture["progress_trace"], TRACE_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("livelock_repeated_zero_progress_transition", result.gate_pack["hold_reasons"])

    def test_no_progress_streak_holds(self):
        fixture = self.fixture()
        for checkpoint in fixture["progress_trace"]["checkpoints"][1:4]:
            checkpoint["progress_units"] = 0
        self.reseal(fixture["progress_trace"], TRACE_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("livelock_no_progress_streak_exceeded", result.gate_pack["hold_reasons"])

    def test_step_budget_holds(self):
        fixture = self.fixture()
        fixture["policy"]["maximum_steps"] = 5
        self.reseal(fixture["policy"], POLICY_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("efficiency_step_budget_exceeded", result.gate_pack["hold_reasons"])

    def test_tool_call_budget_holds(self):
        fixture = self.fixture()
        fixture["policy"]["maximum_tool_calls"] = 8
        self.reseal(fixture["policy"], POLICY_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("efficiency_tool_call_budget_exceeded", result.gate_pack["hold_reasons"])

    def test_model_call_budget_holds(self):
        fixture = self.fixture()
        fixture["policy"]["maximum_model_calls"] = 5
        self.reseal(fixture["policy"], POLICY_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("efficiency_model_call_budget_exceeded", result.gate_pack["hold_reasons"])

    def test_token_budget_holds(self):
        fixture = self.fixture()
        fixture["policy"]["maximum_token_units"] = 45000
        self.reseal(fixture["policy"], POLICY_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("efficiency_token_budget_exceeded", result.gate_pack["hold_reasons"])

    def test_wall_clock_budget_holds(self):
        fixture = self.fixture()
        fixture["policy"]["maximum_wall_clock_ms"] = 1300000
        self.reseal(fixture["policy"], POLICY_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("efficiency_wall_clock_budget_exceeded", result.gate_pack["hold_reasons"])

    def test_failed_action_budget_holds(self):
        fixture = self.fixture()
        for checkpoint in fixture["progress_trace"]["checkpoints"][:3]:
            checkpoint["failed_action"] = True
        self.reseal(fixture["progress_trace"], TRACE_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("efficiency_failed_action_budget_exceeded", result.gate_pack["hold_reasons"])

    def test_insufficient_progress_holds(self):
        fixture = self.fixture()
        fixture["policy"]["minimum_total_progress_units"] = 21
        self.reseal(fixture["policy"], POLICY_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("efficiency_total_progress_insufficient", result.gate_pack["hold_reasons"])

    def test_request_authority_claim_blocks(self):
        fixture = self.fixture()
        fixture["request"]["claims_continuation_authority"] = True
        self.reseal(fixture["request"], REQUEST_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("request_claims_authority_or_correctness", result.issues)

    def test_policy_execution_authority_blocks(self):
        fixture = self.fixture()
        fixture["policy"]["allow_execution_authority"] = True
        self.reseal(fixture["policy"], POLICY_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("policy_effect_or_authority_enabled", result.issues)

    def test_nonconsecutive_checkpoint_indices_block(self):
        fixture = self.fixture()
        fixture["progress_trace"]["checkpoints"][2]["step_index"] = 9
        self.reseal(fixture["progress_trace"], TRACE_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("trace_checkpoint_indices_nonconsecutive", result.issues)

    def test_deterministic_pack_digest(self):
        first = self.fixture()["gate_pack"][PACK_DIGEST_FIELD]
        second = self.fixture()["gate_pack"][PACK_DIGEST_FIELD]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
