from __future__ import annotations

import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_qi_world_concrete_third_licensed_cycle_materialization_public_v2_2 import (
    binding_digest,
    build_concrete_three_cycle_bundle,
    build_third_cycle_binding_receipt,
    validate_concrete_three_cycle_bundle,
    validate_third_closed_cycle_receipt,
    validate_third_cycle_binding_receipt,
)
from runtime.kuuos_qi_world_licensed_multi_cycle_chain_induction_v2_1 import (
    validate_closed_cycle_extension_witness,
    validate_inductive_licensed_cycle_chain,
)


class ConcreteThirdLicensedCycleMaterializationV22Tests(unittest.TestCase):
    def test_materializes_binds_and_appends_real_third_cycle(self) -> None:
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
            binding = build_third_cycle_binding_receipt(
                bundle["source_two_cycle_chain"],
                bundle["third_cycle_receipt"],
            )
            self.assertEqual([], validate_third_cycle_binding_receipt(binding))
            self.assertEqual(
                bundle["materialized_extension_witness"],
                binding["materialized_extension_witness"],
            )
            self.assertEqual(
                bundle["third_cycle_receipt_digest"],
                binding["third_cycle_receipt_digest"],
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

            closure_tamper = deepcopy(binding)
            closure_tamper["source_native_closure_receipt_digest"] = "0" * 64
            closure_tamper["third_cycle_binding_receipt_digest"] = ""
            closure_tamper["third_cycle_binding_receipt_digest"] = binding_digest(
                closure_tamper
            )
            self.assertIn(
                "binding_native_closure_digest_mismatch",
                validate_third_cycle_binding_receipt(closure_tamper),
            )

            witness_tamper = deepcopy(binding)
            witness_tamper["materialized_extension_witness"][
                "closed_cycle_receipt_digest"
            ] = "f" * 64
            witness_tamper["materialized_extension_witness"][
                "extension_witness_digest"
            ] = ""
            witness_tamper["third_cycle_binding_receipt_digest"] = ""
            witness_tamper["third_cycle_binding_receipt_digest"] = binding_digest(
                witness_tamper
            )
            errors = validate_third_cycle_binding_receipt(witness_tamper)
            self.assertTrue(
                "binding_witness_substitution" in errors
                or any(error.startswith("binding_witness_") for error in errors)
            )


if __name__ == "__main__":
    unittest.main()
