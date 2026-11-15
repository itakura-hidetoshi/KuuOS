#!/usr/bin/env python3
"""KuuOS v1.110 round2 CodeAI x MemoryOS: exact v1.102 extensionality and no-op tactic repairs.

The round1 unknown identifier was observed. The missing v1.102 namespace is
a causal HYPOTHESIS, not attested until pinned direct Lean, then real MCP.
Independent exact-source CI is a separate stage and is not asserted here.
"""
from __future__ import annotations
import json
from pathlib import Path
from scripts import kuuos_v1110_codeai_horn_restriction_v1 as prior
from scripts import kuuos_v1106_codeai_label_table_v1 as harness
from scripts.kuuos_v1103_codeai_structural_candidates_v1 import require_event
from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import route_candidates
from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory

OUT=Path("/tmp/kuuos-v1110-codeai-round2")
MCP=Path("/tmp/kuuos-v1110-real-mcp-round2")
REPORT=Path("/tmp/kuuos-v1110-memoryos-round2/context.json")
EXTRA_OPEN="open KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102\n"
ANCHOR_OPEN="open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103\n"
EXT="natDuskinSimplex_eq_of_mapComp_eq"
EXT_FULL="KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102."+EXT
NOOP="  change (natTypeAFourHornCocycle i hi0 hi4 f).label a b c hab hbc = 0\n"

def candidates() -> dict[str,str]:
    if prior.INTRO.count(ANCHOR_OPEN)!=1:
        raise RuntimeError("exact v1.110 inherited names drift")
    if prior.AFTER.count("  apply "+EXT+"\n")!=1 or prior.AFTER.count(NOOP)!=1:
        raise RuntimeError("exact v1.110 source proof span drift")
    opened=prior.INTRO.replace(ANCHOR_OPEN, ANCHOR_OPEN+EXTRA_OPEN)
    no_noop=prior.AFTER.replace(NOOP,"")
    qualified=no_noop.replace("  apply "+EXT+"\n","  apply "+EXT_FULL+"\n")
    options={
      "round2-open-bycases-omega":
          opened+prior.VARIANTS["round1-bycases-omega"]+no_noop,
      "round2-open-bycases-prop-equalities":
          opened+prior.VARIANTS["round1-bycases-prop-equalities"]+no_noop,
      "round2-open-bycases-ltne":
          opened+prior.VARIANTS["round1-bycases-ltne"]+no_noop,
      "round2-qualified-bycases-omega":
          prior.INTRO+prior.VARIANTS["round1-bycases-omega"]+qualified,
      "round2-qualified-prop-equalities":
          prior.INTRO+prior.VARIANTS["round1-bycases-prop-equalities"]+qualified,
    }
    head,branch,tree=require_event()
    seen=read_observation_directory(prior.MEMORY)
    filtered,receipt=route_candidates(options,seen,
            source_head=head,source_tree=tree,imported_blob=prior.PRIOR_BLOB)
    if not filtered:
        raise RuntimeError("All exact candidate replay blocked, NO_DATA retained")
    receipt["error_cause_is_unverified_hypothesis"]=True
    receipt["memoryos_proof_authority"]=False
    REPORT.parent.mkdir(parents=True,exist_ok=False)
    REPORT.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print("KUUOS_V1110_ROUND2_MEMORYOS "+json.dumps({
      "memory_cases":len(seen),"candidates":list(filtered),
      "quarantined":receipt.get("quarantined"),
      "hints":receipt.get("analogical_hints"),
      "proven_theorems_by_memoryos":False},sort_keys=True))
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
