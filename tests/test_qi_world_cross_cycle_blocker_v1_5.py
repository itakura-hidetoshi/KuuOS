from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_qi_world_cross_cycle_blocker_scenarios_v1_5 import (
    run_cross_cycle_blocker_scenarios,
)
from runtime.kuuos_qi_world_cross_cycle_blocker_v1_5 import (
    BLOCKER_ORDER,
    blocker_identity,
    blocker_meet,
    blocker_weaker_or_equal,
    build_cross_cycle_blocker_receipt,
    validate_cross_cycle_blocker_receipt,
)


class QiWorldCrossCycleBlockerV15Tests(unittest.TestCase):
    def test_blocker_receipt_validates(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="kuuos-cross-cycle-blocker-test-"
        ) as temporary:
            receipt = build_cross_cycle_blocker_receipt(Path(temporary))
            self.assertEqual(validate_cross_cycle_blocker_receipt(receipt), [])
            certificate = receipt["blocker_certificate"]
            self.assertEqual(
                list(certificate["composed_blocker_vector"]),
                list(BLOCKER_ORDER),
            )
            self.assertTrue(
                all(certificate["composed_blocker_vector"].values())
            )
            self.assertTrue(receipt["unlicensed_transition_blocked"])
            self.assertFalse(receipt["next_act_started"])
            self.assertFalse(receipt["exact_world_updated"])
            self.assertFalse(receipt["previous_cycle_overwritten"])
            self.assertFalse(receipt["recursive_self_invocation_started"])

    def test_blocker_meet_semilattice_laws(self) -> None:
        identity = blocker_identity()
        a = dict(identity)
        b = dict(identity)
        c = dict(identity)
        a["present_activation_blocker"] = False
        b["world_identity_blocker"] = False
        c["truth_authority_blocker"] = False

        self.assertEqual(blocker_meet(a, identity), a)
        self.assertEqual(blocker_meet(identity, a), a)
        self.assertEqual(blocker_meet(a, b), blocker_meet(b, a))
        self.assertEqual(
            blocker_meet(blocker_meet(a, b), c),
            blocker_meet(a, blocker_meet(b, c)),
        )
        self.assertEqual(blocker_meet(a, a), a)
        self.assertTrue(blocker_weaker_or_equal(blocker_meet(a, b), a))
        self.assertTrue(blocker_weaker_or_equal(blocker_meet(a, b), b))

    def test_fail_closed_mutation_scenarios(self) -> None:
        result = run_cross_cycle_blocker_scenarios()
        self.assertEqual(
            result["status"],
            "KUUOS_QI_WORLD_CROSS_CYCLE_BLOCKER_V1_5_OK",
        )
        self.assertTrue(result["unlicensed_transition_blocked"])
        self.assertTrue(result["fail_closed_on_boundary_loss"])
        self.assertEqual(result["missing_blockers"], [])


if __name__ == "__main__":
    unittest.main()
