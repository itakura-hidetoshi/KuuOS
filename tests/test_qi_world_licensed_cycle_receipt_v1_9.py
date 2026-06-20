from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_qi_world_licensed_cycle_receipt_scenarios_v1_9 import (
    run_licensed_cycle_receipt_scenarios,
)
from runtime.kuuos_qi_world_licensed_cycle_receipt_v1_9 import (
    build_licensed_cycle_receipt,
    build_successor_authority_requirement,
    validate_licensed_cycle_receipt,
    validate_successor_authority_requirement,
)


class QiWorldLicensedCycleReceiptV19Tests(unittest.TestCase):
    def test_closed_cycle_receipt_validates(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="kuuos-licensed-cycle-v19-test-"
        ) as temporary:
            receipt = build_licensed_cycle_receipt(Path(temporary))
            self.assertEqual(validate_licensed_cycle_receipt(receipt), [])
            self.assertTrue(receipt["cycle_closed"])
            self.assertTrue(receipt["closed_cycle_immutable"])
            self.assertTrue(receipt["closed_cycle_append_only"])
            self.assertTrue(receipt["receipt_replay_forbidden"])
            self.assertEqual(receipt["receipt_consumption_count"], 0)
            self.assertFalse(receipt["consumed_authority_inheritable"])
            self.assertFalse(receipt["consumed_authority_renewable"])
            self.assertFalse(receipt["next_act_started"])
            self.assertTrue(receipt["all_post_effect_blockers_active"])

    def test_successor_requirement_is_non_authoritative(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="kuuos-successor-requirement-v19-test-"
        ) as temporary:
            receipt = build_licensed_cycle_receipt(Path(temporary))
            requirement = build_successor_authority_requirement(receipt)
            self.assertEqual(
                validate_successor_authority_requirement(
                    requirement,
                    closed_cycle_receipt=receipt,
                ),
                [],
            )
            self.assertTrue(requirement["fresh_external_authority_required"])
            self.assertTrue(
                requirement["distinct_external_authority_digest_required"]
            )
            self.assertTrue(requirement["new_human_approval_required"])
            self.assertTrue(requirement["new_host_license_required"])
            self.assertTrue(
                requirement["explicit_v1_7_discharge_still_required"]
            )
            self.assertFalse(requirement["successor_act_started"])
            self.assertTrue(
                all(value is False for value in requirement["non_authority"].values())
            )

    def test_tamper_and_freshness_scenarios(self) -> None:
        result = run_licensed_cycle_receipt_scenarios()
        self.assertEqual(
            result["status"],
            "KUUOS_QI_WORLD_LICENSED_CYCLE_RECEIPT_V1_9_OK",
        )
        self.assertTrue(result["cycle_closed"])
        self.assertTrue(result["receipt_replay_forbidden"])
        self.assertFalse(result["consumed_authority_inheritable"])
        self.assertTrue(result["freshness_qualified"])
        self.assertFalse(result["successor_act_started"])
        self.assertTrue(result["explicit_v1_7_discharge_still_required"])


if __name__ == "__main__":
    unittest.main()
