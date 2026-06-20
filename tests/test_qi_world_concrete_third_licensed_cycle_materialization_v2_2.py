from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_qi_world_concrete_third_licensed_cycle_materialization_public_v2_2 import (
    build_concrete_three_cycle_bundle,
    validate_concrete_three_cycle_bundle,
    validate_third_closed_cycle_receipt,
)
from runtime.kuuos_qi_world_licensed_multi_cycle_chain_induction_v2_1 import (
    validate_closed_cycle_extension_witness,
    validate_inductive_licensed_cycle_chain,
)


class ConcreteThirdLicensedCycleMaterializationV22Tests(unittest.TestCase):
    def test_materializes_and_appends_real_third_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            bundle = build_concrete_three_cycle_bundle(Path(temporary))
            self.assertEqual([], validate_concrete_three_cycle_bundle(bundle))
            self.assertEqual(
                [],
                validate_third_closed_cycle_receipt(
                    bundle["third_cycle_receipt"]
                ),
            )
            self.assertEqual(
                [],
                validate_closed_cycle_extension_witness(
                    bundle["materialized_extension_witness"],
                    source_chain=bundle["source_two_cycle_chain"],
                ),
            )
            self.assertEqual(
                [],
                validate_inductive_licensed_cycle_chain(
                    bundle["three_cycle_chain"]
                ),
            )
            self.assertEqual([1, 2, 3], bundle["three_cycle_chain"]["cycle_ordinals"])
            self.assertTrue(bundle["third_act_effect_recorded"])
            self.assertTrue(bundle["third_native_closure_completed"])
            self.assertTrue(bundle["v2_1_induction_witness_realized"])
            self.assertFalse(bundle["next_act_started"])


if __name__ == "__main__":
    unittest.main()
