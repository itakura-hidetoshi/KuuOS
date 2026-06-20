from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_qi_world_licensed_effect_evidence_closure_scenarios_v1_8 import (
    run_licensed_effect_evidence_closure_scenarios,
)
from runtime.kuuos_qi_world_licensed_effect_evidence_closure_v1_8 import (
    BLOCKER_ORDER,
    build_licensed_effect_evidence_closure_receipt,
    validate_licensed_effect_evidence_closure_receipt,
)


class QiWorldLicensedEffectEvidenceClosureV18Tests(unittest.TestCase):
    def test_closure_receipt_validates(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="kuuos-licensed-effect-evidence-v18-test-"
        ) as temporary:
            receipt = build_licensed_effect_evidence_closure_receipt(
                Path(temporary)
            )
            self.assertEqual(
                validate_licensed_effect_evidence_closure_receipt(receipt),
                [],
            )
            states = receipt["native_evidence_states"]
            self.assertEqual(
                states["ObserveOS"]["source_act_state_digest"],
                states["ActOS"]["act_state_digest"],
            )
            self.assertEqual(
                states["VerifyOS"]["source_observe_state_digest"],
                states["ObserveOS"]["observe_state_digest"],
            )
            self.assertEqual(
                states["LearnOS"]["source_verify_state_digest"],
                states["VerifyOS"]["verify_state_digest"],
            )
            self.assertEqual(
                receipt["next_cycle_artifacts"]["PlanOS"][
                    "next_plan_basis_digest"
                ],
                states["LearnOS"]["learning_delta_digest"],
            )

    def test_debts_are_closed_and_next_act_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="kuuos-licensed-effect-debt-v18-test-"
        ) as temporary:
            receipt = build_licensed_effect_evidence_closure_receipt(
                Path(temporary)
            )
            blocker = receipt["post_effect_blocker_certificate"]
            self.assertTrue(receipt["observation_debt_discharged"])
            self.assertTrue(receipt["verification_debt_discharged"])
            self.assertTrue(receipt["learning_recorded"])
            self.assertTrue(receipt["replan_debt_discharged"])
            self.assertTrue(receipt["next_act_not_started"])
            self.assertTrue(blocker["all_required_blockers_active"])
            self.assertEqual(blocker["missing_blockers"], [])
            self.assertEqual(
                list(blocker["composed_blocker_vector"]),
                list(BLOCKER_ORDER),
            )
            self.assertTrue(all(blocker["composed_blocker_vector"].values()))

    def test_world_and_history_boundaries_remain_fixed(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="kuuos-licensed-effect-world-v18-test-"
        ) as temporary:
            receipt = build_licensed_effect_evidence_closure_receipt(
                Path(temporary)
            )
            world = receipt["post_effect_world_projection"]
            self.assertTrue(world["projection_read_only"])
            self.assertFalse(world["runtime_updates_world"])
            self.assertFalse(world["exact_world_identified"])
            self.assertTrue(world["indra_transport_still_unrealized"])
            self.assertFalse(receipt["exact_world_updated"])
            self.assertFalse(receipt["history_overwritten"])
            self.assertFalse(receipt["truth_promoted"])

    def test_tamper_scenarios(self) -> None:
        result = run_licensed_effect_evidence_closure_scenarios()
        self.assertEqual(
            result["status"],
            "KUUOS_QI_WORLD_LICENSED_EFFECT_EVIDENCE_CLOSURE_V1_8_OK",
        )
        self.assertTrue(result["observation_debt_discharged"])
        self.assertTrue(result["verification_debt_discharged"])
        self.assertTrue(result["replan_debt_discharged"])
        self.assertTrue(result["next_act_not_started"])
        self.assertTrue(result["all_required_blockers_active"])
        self.assertTrue(result["indra_transport_still_unrealized"])
        self.assertFalse(result["exact_world_updated"])


if __name__ == "__main__":
    unittest.main()
