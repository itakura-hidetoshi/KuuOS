from __future__ import annotations

import unittest
from copy import deepcopy

from runtime.kuuos_os_qi_cognitive_integration_scenarios_v0_23 import (
    _process_history,
    _verified_fixture,
    run_os_qi_cognitive_integration_scenarios,
)
from runtime.kuuos_os_qi_cognitive_integration_v0_23 import (
    build_cognitive_memory_packet,
    memory_digest,
    validate_cognitive_memory_packet,
)


class OSQiCognitiveIntegrationV023Tests(unittest.TestCase):
    def test_full_scenarios(self) -> None:
        result = run_os_qi_cognitive_integration_scenarios()
        self.assertEqual("KUUOS_OS_QI_COGNITIVE_INTEGRATION_V0_23_OK", result["status"])
        self.assertEqual("verified_ready", result["ready_status"])
        self.assertEqual("contradiction_visible", result["contradiction_status"])
        self.assertEqual("blocked_qi", result["short_history_status"])
        self.assertTrue(result["nonmarkov_feedback_preserved"])
        self.assertTrue(result["future_only_learning"])
        self.assertFalse(result["memory_overwrite_allowed"])
        self.assertFalse(result["effect_authority_granted"])

    def test_memory_consolidation_cannot_overwrite(self) -> None:
        contract, _, _, _, _, _ = _verified_fixture()
        packet = build_cognitive_memory_packet(
            mission_id=contract["mission_id"],
            chart_id="github-main",
            memory_id="memory-test",
            prior_memory_digest="prior",
            process_history=_process_history(),
            episodic_refs=[],
            semantic_claim_refs=[],
            strategy_refs=[],
            consolidation_candidates=[
                {"candidate_id": "candidate-1", "summary": "retain evidence"}
            ],
            created_at_ms=40,
        )
        tampered = deepcopy(packet)
        tampered["consolidation_candidates"][0]["overwrites_prior_memory"] = True
        tampered["cognitive_memory_digest"] = memory_digest(tampered)
        self.assertIn(
            "memory_consolidation_overwrite_forbidden",
            validate_cognitive_memory_packet(tampered),
        )

    def test_memory_packet_is_append_only_and_non_authoritative(self) -> None:
        contract, _, _, _, _, _ = _verified_fixture()
        packet = build_cognitive_memory_packet(
            mission_id=contract["mission_id"],
            chart_id="github-main",
            memory_id="memory-boundary-test",
            prior_memory_digest="prior",
            process_history=_process_history(),
            episodic_refs=[],
            semantic_claim_refs=[],
            strategy_refs=[],
            consolidation_candidates=[],
            created_at_ms=41,
        )
        self.assertTrue(packet["append_only"])
        self.assertFalse(packet["memory_overwrite_allowed"])
        self.assertFalse(packet["non_authority"]["grants_execution_authority"])
        self.assertFalse(packet["non_authority"]["grants_truth_authority"])


if __name__ == "__main__":
    unittest.main()
