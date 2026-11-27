"""R62 R2: preserve all R1 formulas and replace only the closed-table proof tactic."""
from runtime import kuuos_codeai_olean_contextual_recovery_duality_v1 as r1
from runtime.kuuos_codeai_olean_contextual_recovery_duality_v1 import *

def truth_table(recovery,obs,paths,budget):
    rows,original=r1.truth_table(recovery,obs,paths,budget)
    needle=" := by\n  decide\n\n"
    replacement=" := by\n  simp\n\n"
    if original.count(needle)!=2:
        raise ValueError("HOLD_R62_R1_PROOF_BOUNDARY")
    repaired=original.replace(needle,replacement)
    if repaired.replace(replacement,needle)!=original:
        raise ValueError("HOLD_R62_STATEMENT_DRIFT")
    return rows,repaired
