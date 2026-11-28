"""Actual pinned Lean execution; all gate inputs and keys are synthetic."""
from __future__ import annotations
import copy
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import test_kuuos_verifyos_diverse_ledger_audit_v0_13 as fixture
from runtime import kuuos_verifyos_lean_egress_v0_17 as g

b,p=g.b,g.p


class EgressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=fixture.PairTests("test_real_pair_and_diverse_match")
        cls.addClassCleanup(cls.fixture.doCleanups)
        cls.snapshot,cls.args=cls.fixture.pair("correct")
        cls.bad_snapshot,cls.bad_args=cls.fixture.pair("wrong_count")
        lean=shutil.which("lean")
        if lean is None:
            raise RuntimeError("Pinned Lean is required; no skipped success")
        cls.lean=Path(lean).absolute()

    def issue(self,**changes):
        args=dict(self.args); args.update(changes)
        return p.strict(g.publication(self.snapshot,self.lean,**args))

    def test_actual_lean_publication_and_fresh_display(self):
        packet=g.publication(self.snapshot,self.lean,**self.args)
        obj=p.strict(packet)
        self.assertEqual(obj["status"],g.MATCH,obj)
        self.assertEqual(obj["answer_status"],"AMBIGUOUS_PARTIAL")
        self.assertEqual(len(obj["claims"]),18)
        self.assertEqual(sum(x["status"]=="OBSERVED_IN_ADMITTED_RECEIPT" for x in obj["claims"]),13)
        self.assertEqual(obj["execution"]["input_sha256"],b.sha(self.args["primary_raw"]))
        self.assertEqual(obj["execution"]["exit_code"],0)
        self.assertEqual(len(obj["execution"]["stages"]),4)
        self.assertTrue(all(obj[k] is False for k in g.BOUNDARY))
        observed,rc=g.verified_display(packet,self.snapshot,self.lean,**self.args)
        self.assertEqual((observed,rc),(packet,2))
        obj["claims"][0]["value"]="forged"
        blocked,rc=g.verified_display(b.canonical(obj),self.snapshot,self.lean,**self.args)
        self.assertEqual((p.strict(blocked)["reason"],rc),("PUBLICATION_MISMATCH",2))

    def test_common_mode_defect_stops_before_lean(self):
        with patch.object(g,"run_lean",side_effect=AssertionError("must not invoke")):
            out=p.strict(g.publication(self.bad_snapshot,self.lean,**self.bad_args))
            self.assertEqual(out["reason"],"DIVERSE_EVIDENCE_NOT_ADMITTED")

    def test_missing_witness_stops_before_lean(self):
        with patch.object(g,"run_lean",side_effect=AssertionError("must not invoke")):
            self.assertEqual(self.issue(witness_packet=None)["status"],"HOLD")

    def test_context_change_stops_before_lean(self):
        with patch.object(g,"run_lean",side_effect=AssertionError("must not invoke")):
            self.assertEqual(self.issue(context=dict(self.args["context"],turn_id="f"*64))["status"],"HOLD")

    def test_extra_admission_flag_is_not_accepted(self):
        with patch.object(g,"run_lean",side_effect=AssertionError("must not invoke")):
            self.assertEqual(self.issue(admitted=True)["status"],"HOLD")

    def test_extra_precomputed_lean_output_is_not_accepted(self):
        with patch.object(g,"run_lean",side_effect=AssertionError("must not invoke")):
            self.assertEqual(self.issue(lean_output={"status":g.MATCH})["status"],"HOLD")

    def test_changed_raw_input_stops_before_lean(self):
        with patch.object(g,"run_lean",side_effect=AssertionError("must not invoke")):
            self.assertEqual(self.issue(primary_raw=self.args["primary_raw"]+b" ")["status"],"HOLD")

    def test_source_pin_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name); target=root/"scripts"/"lean_probes"; target.mkdir(parents=True)
            for _,file,_ in g.SOURCES: shutil.copyfile(g.ROOT/"scripts"/"lean_probes"/file,target/file)
            with (target/g.SOURCES[-1][1]).open("ab") as f: f.write(b"\n")
            with patch.object(g,"ROOT",root):
                self.assertEqual(self.issue()["reason"],"LEAN_SOURCE_MISMATCH:ProjectionCLI")

    def test_unavailable_executable_holds(self):
        with tempfile.TemporaryDirectory() as name:
            out=p.strict(g.publication(self.snapshot,Path(name)/"absent",**self.args))
        self.assertEqual(out["status"],"HOLD")
        self.assertEqual(out["reason"],"TRUSTED_LEAN_PATH_REQUIRED")

    def test_actual_projection_disagreement_holds(self):
        # This is a lower-level negative test: the real Lean process computes
        # the correct value and cannot match a deliberately changed expectation.
        verified=g.d.verify_diverse(self.snapshot,**self.args)
        self.assertEqual(verified["status"],"DIVERSE_FROZEN_PROFILE_AGREEMENT_ONLY")
        rows=g.all_rows(self.args["primary_raw"],self.args["request"],verified["pair"]["primary"])
        rows[0]["value"]="wrong expected value"
        with self.assertRaisesRegex(ValueError,"LEAN_PYTHON_VALUE_MISMATCH"):
            g.run_lean(g.ROOT,self.lean,self.args["primary_raw"],self.args["request"],self.args["context"],rows)


if __name__=="__main__":
    unittest.main()
