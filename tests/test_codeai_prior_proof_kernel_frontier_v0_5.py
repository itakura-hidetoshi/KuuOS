"""Bounded frontier selection contracts, not new Lean evidence."""
import copy
import unittest
from pathlib import Path

from runtime.kuuos_codeai_prior_proof_kernel_memory_v0_4 import load_packet
from scripts.codeai_prior_proof_kernel_frontier_v0_5 import PLANS, validate_frontier
from scripts.codeai_prior_proof_kernel_recall_v0_4 import BASE_TREES, LEC, QI

ROOT = Path(__file__).resolve().parents[1]


class FrontierTests(unittest.TestCase):
    def test_parent_packet_unchanged_and_all_recorded_direct_refs_selected(self):
        packet = load_packet(ROOT)
        self.assertEqual(packet["source_subtrees"], BASE_TREES)
        self.assertEqual(validate_frontier(packet), {
            LEC+"sourceGlobal_implies_shadowGlobal",
            LEC+"sourceGlobal_implies_overlapFaithful",
            LEC+"shadowGlobal_and_overlapFaithful_implies_sourceGlobal",
            QI+"nativeC60GaugeSlot_index"})

    def test_exactly_ten_new_existing_declaration_observations(self):
        packet = load_packet(ROOT)
        names = {name for p in PLANS for name in p["names"]}
        self.assertEqual(len(names), 10)
        self.assertFalse(names.intersection(r["name"] for r in packet["observations"]))
        self.assertIn(QI+"nativeC60GaugeSheng_index", names)
        self.assertIn(QI+"nativeC60GaugeKe_index", names)

    def test_tampered_parent_packet_holds(self):
        packet = copy.deepcopy(load_packet(ROOT))
        packet["observations"][0]["expected_direct_refs"] = []
        with self.assertRaisesRegex(ValueError, "prior packet identity drift"):
            validate_frontier(packet)


if __name__ == "__main__":
    unittest.main(verbosity=2)
