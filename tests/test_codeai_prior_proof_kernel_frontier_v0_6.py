"""Bounded v0.6 reference selection, never positive Lean evidence."""
import copy
from pathlib import Path
import unittest

from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_5 import load_packets
from scripts.codeai_prior_proof_kernel_frontier_v0_6 import (
    PLANS, EXTERNAL_RECORDED_REFS, validate_frontier)

ROOT = Path(__file__).resolve().parents[1]


class FrontierTests(unittest.TestCase):
    def test_exact_unobserved_local_references_from_both_packets(self):
        parent, packet = load_packets(ROOT)
        rows = parent["observations"] + packet["observations"]
        old = {r["name"] for r in rows}
        refs = {n for r in rows for n in r["expected_direct_refs"]} - old
        local = validate_frontier(parent, packet)
        self.assertEqual(len(old), 13)
        self.assertEqual(len(local), 8)
        self.assertEqual(refs, local | EXTERNAL_RECORDED_REFS)
        self.assertEqual(EXTERNAL_RECORDED_REFS, {"congrArg"})
        self.assertFalse(local & old)
        self.assertEqual(len(local | old), 21)
        self.assertEqual(local, {n for p in PLANS for n in p["names"]})

    def test_five_source_modules_and_physical_bridge(self):
        self.assertEqual(len({p["path"] for p in PLANS}), 5)
        parent, packet = load_packets(ROOT)
        self.assertIn("Kuu.F112.Physical.slotIndex_ringSlot",
                      validate_frontier(parent, packet))

    def test_tampering_either_immutable_packet_holds(self):
        parent, packet = load_packets(ROOT)
        for p in (parent, packet):
            bad = copy.deepcopy(p)
            bad["observations"][0]["expected_direct_refs"] = []
            with self.assertRaises(ValueError):
                validate_frontier(bad if p is parent else parent,
                                  bad if p is packet else packet)


if __name__ == "__main__":
    unittest.main(verbosity=2)
