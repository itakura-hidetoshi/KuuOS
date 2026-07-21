from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_act_os_fixture_v0_1 import host_inputs
from runtime.kuuos_qi_world_successor_cycle_materialization_public_scenarios_v2_0 import (
    run_successor_cycle_materialization_scenarios,
)
from runtime.kuuos_qi_world_successor_cycle_materialization_public_v2_0 import (
    build_successor_cycle_materialization_receipt,
    validate_successor_cycle_materialization_receipt,
)


class QiWorldSuccessorCycleMaterializationV20Tests(unittest.TestCase):
    def test_two_cycle_materialization_validates(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="kuuos-successor-cycle-v20-test-"
        ) as temporary:
            receipt = build_successor_cycle_materialization_receipt(
                Path(temporary)
            )
            _, _, host_license, _ = host_inputs(
                job_id="qi-world-v20-job",
                expires_at_ms=480_000,
            )
            self.assertEqual(
                validate_successor_cycle_materialization_receipt(
                    receipt,
                    host_license=host_license,
                ),
                [],
            )
            self.assertEqual(receipt["first_cycle_ordinal"], 1)
            self.assertEqual(receipt["second_cycle_ordinal"], 2)
            self.assertTrue(receipt["cycle_ordinals_strictly_increasing"])
            self.assertTrue(receipt["second_act_materialized"])
            self.assertTrue(receipt["second_effect_recorded"])
            self.assertTrue(receipt["second_observation_closed"])
            self.assertTrue(receipt["second_verification_closed"])
            self.assertTrue(receipt["second_learning_closed"])
            self.assertTrue(receipt["second_replan_closed"])
            self.assertTrue(receipt["second_cycle_closed"])
            self.assertFalse(receipt["third_act_started"])

    def test_authority_is_fresh_and_not_inherited(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="kuuos-successor-authority-v20-test-"
        ) as temporary:
            receipt = build_successor_cycle_materialization_receipt(
                Path(temporary)
            )
            predecessor = receipt["predecessor_cycle_receipt"]
            first_authority = predecessor[
                "source_v17_handoff_receipt"
            ]["external_authority_packet"]
            second_authority = receipt["successor_handoff_receipt"][
                "external_authority_packet"
            ]
            self.assertNotEqual(
                first_authority["external_authority_packet_digest"],
                second_authority["external_authority_packet_digest"],
            )
            self.assertNotEqual(
                first_authority["human_approval_receipt_digest"],
                second_authority["human_approval_receipt_digest"],
            )
            self.assertNotEqual(
                first_authority["host_license_digest"],
                second_authority["host_license_digest"],
            )
            self.assertFalse(receipt["predecessor_authority_inherited"])
            self.assertFalse(receipt["predecessor_authority_renewed"])
            self.assertTrue(receipt["second_authority_consumed_once"])
            self.assertFalse(receipt["second_authority_inheritable"])

    def test_native_second_cycle_is_closed_and_blocked_again(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="kuuos-successor-closure-v20-test-"
        ) as temporary:
            receipt = build_successor_cycle_materialization_receipt(
                Path(temporary)
            )
            handoff = receipt["successor_handoff_receipt"]
            closure = receipt["successor_closure_receipt"]
            blocker = closure["post_effect_blocker_certificate"]
            second = receipt["second_cycle_receipt"]
            self.assertTrue(handoff["effect_recorded"])
            self.assertEqual(handoff["release_consumption_count"], 1)
            self.assertTrue(closure["observation_debt_discharged"])
            self.assertTrue(closure["verification_debt_discharged"])
            self.assertTrue(closure["learning_recorded"])
            self.assertTrue(closure["replan_debt_discharged"])
            self.assertTrue(blocker["all_required_blockers_active"])
            self.assertEqual(blocker["missing_blockers"], [])
            self.assertTrue(second["cycle_closed"])
            self.assertTrue(second["all_post_effect_blockers_active"])
            self.assertFalse(second["next_act_started"])

    def test_tamper_scenarios(self) -> None:
        result = run_successor_cycle_materialization_scenarios()
        self.assertEqual(
            result["status"],
            "KUUOS_QI_WORLD_SUCCESSOR_CYCLE_MATERIALIZATION_V2_0_OK",
        )
        self.assertEqual(result["first_cycle_ordinal"], 1)
        self.assertEqual(result["second_cycle_ordinal"], 2)
        self.assertTrue(result["second_act_materialized"])
        self.assertTrue(result["second_cycle_closed"])
        self.assertTrue(result["all_second_post_effect_blockers_active"])
        self.assertFalse(result["third_act_started"])
        self.assertTrue(result["indra_transport_still_unrealized"])
        self.assertFalse(result["exact_world_updated"])


if __name__ == "__main__":
    unittest.main()
