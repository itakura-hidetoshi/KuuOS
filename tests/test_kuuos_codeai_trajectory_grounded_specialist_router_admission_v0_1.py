from __future__ import annotations

from copy import deepcopy
import unittest

from runtime.kuuos_codeai_trajectory_grounded_specialist_router_admission_v0_1 import *
from scripts.build_codeai_trajectory_grounded_specialist_router_admission_fixture_v0_1 import build_reference_fixture


class TrajectoryGroundedSpecialistRouterAdmissionTests(unittest.TestCase):
    def fixture(self):
        return deepcopy(build_reference_fixture())

    def run_fixture(self, fixture):
        return build_codeai_trajectory_grounded_specialist_router_admission(
            request=fixture["request"],
            policy=fixture["policy"],
            trajectory=fixture["trajectory"],
            specialists=fixture["specialists"],
        )

    def reseal(self, value, field):
        value.pop(field, None)
        value.update(seal(value, field))

    def test_reference_admits_formal_specialist(self):
        fixture = self.fixture()
        pack = fixture["admission_pack"]
        self.assertEqual(pack["route_decision"], DECISION_ADMIT)
        self.assertEqual(pack["selected_specialist_id"], "specialist-formal-001")
        self.assertEqual(pack["selected_specialist_kind"], "formal")
        self.assertEqual(pack["eligible_specialist_count"], 4)
        self.assertTrue(pack["measurement_grounded"])

    def test_result_preserves_no_effect_boundary(self):
        pack = self.fixture()["admission_pack"]
        for field in (
            "specialist_dispatched", "candidate_selected", "execution_authority_granted",
            "repository_mutation_performed", "git_authority_granted", "correctness_claimed",
        ):
            self.assertFalse(pack[field])
        self.assertTrue(pack["route_hint_only"])

    def test_tampered_trajectory_digest_blocks(self):
        fixture = self.fixture()
        fixture["trajectory"]["observation_count"] += 1
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("trajectory_digest_mismatch", result.issues)

    def test_self_report_only_blocks(self):
        fixture = self.fixture()
        fixture["trajectory"]["self_report_only"] = True
        self.reseal(fixture["trajectory"], TRAJECTORY_DIGEST_FIELD)
        for specialist in fixture["specialists"]:
            specialist["measurement_packet_digest"] = fixture["trajectory"][TRAJECTORY_DIGEST_FIELD]
            self.reseal(specialist, SPECIALIST_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertIn("trajectory_self_report_only", result.issues)

    def test_incomplete_measurement_blocks(self):
        fixture = self.fixture()
        fixture["trajectory"]["measurement_complete"] = False
        self.reseal(fixture["trajectory"], TRAJECTORY_DIGEST_FIELD)
        for specialist in fixture["specialists"]:
            specialist["measurement_packet_digest"] = fixture["trajectory"][TRAJECTORY_DIGEST_FIELD]
            self.reseal(specialist, SPECIALIST_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("trajectory_measurement_incomplete", result.issues)

    def test_insufficient_exploration_blocks(self):
        fixture = self.fixture()
        fixture["trajectory"]["exploration_turns"] = 2
        self.reseal(fixture["trajectory"], TRAJECTORY_DIGEST_FIELD)
        for specialist in fixture["specialists"]:
            specialist["measurement_packet_digest"] = fixture["trajectory"][TRAJECTORY_DIGEST_FIELD]
            self.reseal(specialist, SPECIALIST_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("trajectory_turns_insufficient", result.issues)

    def test_memory_pack_mismatch_blocks(self):
        fixture = self.fixture()
        fixture["request"]["memory_pack_digest"] = "0" * 64
        self.reseal(fixture["request"], REQUEST_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertTrue(any(issue.startswith("request_policy_binding_mismatch:memory_pack_digest") for issue in result.issues))

    def test_specialist_binding_mismatch_excludes(self):
        fixture = self.fixture()
        specialist = fixture["specialists"][0]
        specialist["source_tree_digest"] = "1" * 64
        self.reseal(specialist, SPECIALIST_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.admission_pack["selected_specialist_id"], "specialist-behavioral-001")
        self.assertEqual(result.admission_pack["excluded_specialist_count"], 1)

    def test_subtask_mismatch_excludes(self):
        fixture = self.fixture()
        specialist = fixture["specialists"][0]
        specialist["supported_subtask_kind"] = "edit"
        self.reseal(specialist, SPECIALIST_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.admission_pack["selected_specialist_id"], "specialist-behavioral-001")

    def test_measurement_packet_mismatch_excludes(self):
        fixture = self.fixture()
        specialist = fixture["specialists"][0]
        specialist["measurement_packet_digest"] = "2" * 64
        self.reseal(specialist, SPECIALIST_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertEqual(result.admission_pack["selected_specialist_id"], "specialist-behavioral-001")

    def test_nonindependent_measurement_excludes(self):
        fixture = self.fixture()
        specialist = fixture["specialists"][0]
        specialist["independent_measurement"] = False
        self.reseal(specialist, SPECIALIST_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertEqual(result.admission_pack["selected_specialist_id"], "specialist-behavioral-001")

    def test_route_margin_conflict_holds(self):
        fixture = self.fixture()
        behavioral = fixture["specialists"][1]
        behavioral["fit_score"] = 94
        behavioral["reliability_score"] = 94
        behavioral["estimated_cost_units"] = 35
        behavioral["utility_score"] = 153
        self.reseal(behavioral, SPECIALIST_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.admission_pack["route_decision"], DECISION_HOLD)
        self.assertEqual(result.admission_pack["hold_reason"], "route_margin_not_met")
        self.assertIsNone(result.admission_pack["selected_specialist_id"])

    def test_no_admissible_specialist_holds(self):
        fixture = self.fixture()
        for specialist in fixture["specialists"]:
            specialist["fit_score"] = 10
            specialist["utility_score"] = specialist["fit_score"] + specialist["reliability_score"] - specialist["estimated_cost_units"]
            self.reseal(specialist, SPECIALIST_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.admission_pack["route_decision"], DECISION_HOLD)
        self.assertEqual(result.admission_pack["hold_reason"], "no_admissible_specialist")

    def test_request_authority_claim_blocks(self):
        fixture = self.fixture()
        fixture["request"]["claims_dispatch_authority"] = True
        self.reseal(fixture["request"], REQUEST_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("request_claims_authority", result.issues)

    def test_policy_dispatch_authority_blocks(self):
        fixture = self.fixture()
        fixture["policy"]["allow_specialist_dispatch"] = True
        self.reseal(fixture["policy"], POLICY_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertIn("policy_effect_or_authority_enabled", result.issues)

    def test_specialist_effect_claim_excludes(self):
        fixture = self.fixture()
        specialist = fixture["specialists"][0]
        specialist["specialist_dispatched"] = True
        self.reseal(specialist, SPECIALIST_DIGEST_FIELD)
        result = self.run_fixture(fixture)
        self.assertEqual(result.status, STATUS_READY)
        self.assertEqual(result.admission_pack["selected_specialist_id"], "specialist-behavioral-001")

    def test_deterministic_pack_digest(self):
        first = self.fixture()["admission_pack"][PACK_DIGEST_FIELD]
        second = self.fixture()["admission_pack"][PACK_DIGEST_FIELD]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
