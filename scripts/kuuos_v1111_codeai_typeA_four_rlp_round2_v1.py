#!/usr/bin/env python3
"""v1.111 CodeAI round2: missing fixed namespace for actual terminal point.

The v1.111 round1 direct Lean diagnostic was an unknown identifier for
ScaledSSet.toPoint, not a proof of failed RLP. The definition lives in
v1.41. Reuse v1.111 exact theorem statements and genuine lift witness,
testing namespace open versus full-qualification under pinned direct Lean,
then selected green only with the real Lean MCP. MemoryOS has no authority.
"""
from __future__ import annotations
import json
from pathlib import Path
from scripts import kuuos_v1111_codeai_typeA_four_rlp_v1 as prior
from scripts import kuuos_v1106_codeai_label_table_v1 as harness
from scripts.kuuos_v1103_codeai_structural_candidates_v1 import require_event
from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import route_candidates
from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory

OUT=Path("/tmp/kuuos-v1111-codeai-rlp-round2")
MCP=Path("/tmp/kuuos-v1111-real-mcp-rlp-round2")
REPORT=Path("/tmp/kuuos-v1111-memoryos-round2/context.json")
ANCHOR="open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49\n"
OPEN41="open KUOS.DependentOriginationScaledTerminalRLPV1_41\n"
OLD="(ScaledSSet.toPoint natDoubleDeloopingScaledDuskin)"
FULL="(KUOS.DependentOriginationScaledTerminalRLPV1_41.ScaledSSet.toPoint natDoubleDeloopingScaledDuskin)"

def candidates() -> dict[str,str]:
    if prior.INTRO.count(ANCHOR)!=1 or prior.INTRO.count(OLD)!=1:
        raise RuntimeError("Exact v1.111 source signatures drift")
    opened=prior.INTRO.replace(ANCHOR,ANCHOR+OPEN41)
    qualified=prior.INTRO.replace(OLD,FULL)
    raw={
      "round2-open-exact-fun":opened+prior.VARIANTS["round1-rlp-exact-fun"]+prior.TAIL,
      "round2-open-apply":opened+prior.VARIANTS["round1-rlp-apply"]+prior.TAIL,
      "round2-open-explicit":opened+prior.VARIANTS["round1-rlp-explicit"]+prior.TAIL,
      "round2-qualified-exact-fun":qualified+prior.VARIANTS["round1-rlp-exact-fun"]+prior.TAIL,
      "round2-qualified-explicit":qualified+prior.VARIANTS["round1-rlp-explicit"]+prior.TAIL,
    }
    head,branch,tree=require_event()
    cases=read_observation_directory(prior.MEMORY)
    filtered,history=route_candidates(raw,cases,source_head=head,
                              source_tree=tree,imported_blob=prior.PRIOR_BLOB)
    if not filtered:
        raise RuntimeError("All exact source-bound candidates filtered, NO_DATA")
    history["causal_status"]="UNVERIFIED_HYPOTHESIS"
    history["memory_is_not_proof_authority"]=True
    REPORT.parent.mkdir(parents=True,exist_ok=False)
    REPORT.write_text(json.dumps(history,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V1111_ROUND2_MEMORYOS "+json.dumps({
        "cases":len(cases),"retained":list(filtered),
        "quarantined":history.get("quarantined"),
        "analogy":history.get("analogical_hints"),
        "proof_authority":False},sort_keys=True))
    return filtered

def main() -> int:
    harness.V105=prior.PRIOR
    harness.V105_BLOB=prior.PRIOR_BLOB
    harness.base.TARGET=prior.TARGET
    harness.base.MODULE=prior.MODULE
    harness.base.PREDECESSOR=prior.PRIOR
    harness.base.ORIGINAL_V103_BLOB=prior.PRIOR_BLOB
    harness.base.OUT=OUT
    harness.base.MCP_OUT=MCP
    harness.candidates=candidates
    return harness.main()

if __name__=="__main__":
    raise SystemExit(main())
