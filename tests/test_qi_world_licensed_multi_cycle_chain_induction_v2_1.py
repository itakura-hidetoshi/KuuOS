from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_qi_world_licensed_multi_cycle_chain_induction_v2_1 import (
    append_closed_cycle,
    build_closed_cycle_extension_witness,
    build_inductive_licensed_cycle_chain,
    validate_inductive_licensed_cycle_chain,
)


class LicensedMultiCycleChainInductionV21Tests(unittest.TestCase):
    def test_base_two_cycle_chain_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            chain = build_inductive_licensed_cycle_chain(Path(temporary))
            self.assertEqual([], validate_inductive_licensed_cycle_chain(chain))
            self.assertEqual(2, chain["cycle_count"])
            self.assertEqual([1, 2], chain["cycle_ordinals"])

    def test_append_third_cycle_preserves_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = build_inductive_licensed_cycle_chain(Path(temporary) / "base")
            witness = build_closed_cycle_extension_witness(base, nonce="unit-cycle-3")
            chain = append_closed_cycle(base, witness)
            self.assertEqual([], validate_inductive_licensed_cycle_chain(chain))
            self.assertEqual(base["cycle_nodes"], chain["cycle_nodes"][:2])
            self.assertEqual(3, chain["cycle_count"])
            self.assertFalse(chain["next_act_started"])

    def test_induction_extends_to_four_cycles(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = build_inductive_licensed_cycle_chain(Path(temporary) / "base")
            third = append_closed_cycle(
                base,
                build_closed_cycle_extension_witness(base, nonce="unit-cycle-3"),
            )
            fourth = append_closed_cycle(
                third,
                build_closed_cycle_extension_witness(third, nonce="unit-cycle-4"),
            )
            self.assertEqual([], validate_inductive_licensed_cycle_chain(fourth))
            self.assertEqual([1, 2, 3, 4], fourth["cycle_ordinals"])
            self.assertEqual(4, len(set(fourth["authority_packet_digests"])))
            self.assertTrue(fourth["all_receipts_non_consumable"])


if __name__ == "__main__":
    unittest.main()
