"""Replay durable real compiler observations; never promote them to new proofs."""
from pathlib import Path
import unittest
from runtime import kuuos_codeai_memoryos_lean_repair_v0_1 as m

class SeedEvidenceTests(unittest.TestCase):
    def test_real_failures_successes_and_repair_lineage(self):
        root=Path(__file__).resolve().parents[1]
        rows=m.load(root/'memoryos/lean_repairs/v0_1')
        self.assertEqual(len(rows),9)
        self.assertEqual(sum(r['outcome']=='direct_failure' for r in rows),6)
        self.assertEqual(sum(r['outcome']=='direct_success' for r in rows),3)
        self.assertEqual({r['evidence']['run_id'] for r in rows},{43687692238,43687986358,43689373291})
        self.assertEqual(sum(bool(r['related_ids']) for r in rows),1)
        for r in rows:
            m.validate(r)
            self.assertFalse(r['independent_ci_certified'])
            self.assertEqual(m.memoryos_context(r)['authority'],'external_pointer_only')
            # Legacy artifacts are not supplemented with invented exact bindings.
            self.assertIsNone(r['binding']['manifest_sha256'])
            self.assertNotEqual(m.guard(rows,r['binding'],r['candidate_blob'])['decision'],'BLOCK_EXACT_FAILED')
        self.assertTrue(any('⊢' in m.diagnostic(r) for r in rows if r['outcome']=='direct_failure'))

if __name__=='__main__':unittest.main()
