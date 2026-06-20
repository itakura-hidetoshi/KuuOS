from __future__ import annotations

import unittest
from copy import deepcopy

from runtime.kuuos_os_qi_closed_loop_integration_v0_24 import (
    closed_loop_digest,
    validate_os_qi_closed_loop,
)
from runtime.kuuos_os_qi_closed_loop_scenarios_v0_24 import (
    _build_case,
    run_os_qi_closed_loop_scenarios,
)


class OSQiClosedLoopV024Tests(unittest.TestCase):
    def test_full_scenarios(self) -> None:
        result = run_os_qi_closed_loop_scenarios()
        self.assertEqual("KUUOS_OS_QI_CLOSED_LOOP_V0_24_OK", result["status"])
        self.assertEqual("decision_candidate_ready", result["ready_status"])
        self.assertEqual("contradiction_preserved", result["contradiction_status"])
        self.assertEqual("blocked", result["blocked_status"])
        self.assertTrue(result["nonmarkov_memory_visible"])
        self.assertFalse(result["candidate_selected"])
        self.assertFalse(result["plan_activated"])
        self.assertFalse(result["execution_permission"])
        self.assertFalse(result["memory_overwrite"])

    def test_candidate_selection_cannot_be_bypassed(self) -> None:
        case = _build_case("verified_success", "v024-test")
        from runtime.kuuos_os_qi_closed_loop_integration_v0_24 import build_os_qi_closed_loop

        receipt = build_os_qi_closed_loop(
            cycle_id="v024-test",
            semantic_plan=case["plan"],
            verification_receipt=case["verification"],
            cognitive_memory_receipt=case["memory"],
            observe_envelope=case["observe"],
            verify_envelope=case["verify"],
            qi_state=case["qi"],
        )
        tampered = deepcopy(receipt)
        tampered["decision_candidate_set"]["candidate_selected"] = True
        tampered["os_qi_closed_loop_digest"] = closed_loop_digest(tampered)
        self.assertIn("candidate_selection_bypass", validate_os_qi_closed_loop(tampered))


if __name__ == "__main__":
    unittest.main()
