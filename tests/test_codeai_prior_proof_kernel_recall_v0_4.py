"""Read-only synthetic parser regressions, not Lean evidence."""
import copy
import json
import unittest
from scripts.codeai_prior_proof_kernel_recall_v0_4 import read_direct,suffix,PREFIX

N="Kuu.Test.prior"
ENTRY={"name":N,"expected_direct_refs":["Kuu.Test.support"]}
ROW={"name":N,"type_pretty":"P → P","type_expr_repr":"fixture",
     "universe_parameters":[],"type_constants":["P"],
     "proof_constants":["Kuu.Test.support"],"axioms":["propext"]}

def fixture(row=ROW):
    return "'"+N+"' depends on axioms: [propext]\n"+PREFIX+json.dumps(row)+"\n"

class KernelRecallTests(unittest.TestCase):
    def test_observed_type_and_proof_refs(self):
        x=read_direct(fixture(),[ENTRY])
        self.assertEqual(x[0]["proof_constants"],["Kuu.Test.support"])
        self.assertTrue(x[0]["proof_body_observed"])
    def test_absent_duplicate_and_disagreement_hold(self):
        for log in ("",fixture()+fixture(),fixture().replace("[propext]","[Quot.sound]")):
            with self.subTest(log=log[:80]),self.assertRaises(ValueError):
                read_direct(log,[ENTRY])
    def test_unexpected_axiom_holds(self):
        r=copy.deepcopy(ROW);r["axioms"]=["otherAxiom"]
        with self.assertRaisesRegex(ValueError,"unexpected axiom"):
            read_direct(fixture(r).replace("[propext]","[otherAxiom]"),[ENTRY])
    def test_missing_direct_dependency_holds(self):
        r=copy.deepcopy(ROW);r["proof_constants"]=["Some.other"]
        with self.assertRaisesRegex(ValueError,"source proof dependency"):
            read_direct(fixture(r),[ENTRY])
    def test_warning_error_panic_and_sorry_hold(self):
        for diagnostic in ("warning: X","error: X","PANIC at X","sorryAx"):
            with self.subTest(diagnostic=diagnostic),self.assertRaises(ValueError):
                read_direct(fixture()+diagnostic,[ENTRY])
    def test_universes_scoped_off_for_axiom_report_only(self):
        text=suffix([N])
        self.assertIn("set_option pp.universes true",text)
        self.assertIn("set_option pp.universes false in\n#print axioms "+N,text)
        self.assertIn('#check @'+N,text)
        self.assertIn('info.levelParams.map Name.toString',text)

    def test_observed_universe_display_mismatch_remains_fail_closed(self):
        # Reproduce the failure observed in direct-0.log of run 45332533402.
        row=copy.deepcopy(ROW); row["axioms"]=["Classical.choice"]
        plain=fixture(row).replace("[propext]","[Classical.choice]")
        self.assertEqual(read_direct(plain,[ENTRY])[0]["axioms"],["Classical.choice"])
        decorated=plain.replace("[Classical.choice]","[Classical.choice.{u}]")
        with self.assertRaisesRegex(ValueError,"source-local axiom reports disagree"):
            read_direct(decorated,[ENTRY])
        with self.assertRaisesRegex(ValueError,"source-local axiom reports disagree"):
            read_direct(plain+"'"+N+"' depends on axioms: [Classical.choice.{u}]\n",[ENTRY])

    def test_name_injection_refused(self):
        self.assertIn("#check @"+N,suffix([N]))
        with self.assertRaises(ValueError):
            suffix([N+"\n#eval 2"])

if __name__=="__main__":
    unittest.main(verbosity=2)
