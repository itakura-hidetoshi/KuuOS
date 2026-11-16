#!/usr/bin/env python3
"""v1.112: CodeAI / MemoryOS fixed-source proof of every standard type-A horn.

The target property is literal source-bound cocycle completion for EVERY
StandardTypeAHornGeneratorIndex, followed by actual scaled lifts and RLP.
No assumption of 'all completions', no independent proof until CI.
Read historical failures as evidence and causal hints, not proof authority.
Runs on its own isolated validation-only descendant of certified PR #3548.
"""
from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path

from scripts import kuuos_v1106_codeai_label_table_v1 as harness
from scripts import kuuos_v1103_codeai_structural_candidates_v1 as v103
from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import route_candidates
from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory

REPO = "itakura-hidetoshi/KuuOS"
BRANCH = "research/kuuos-typeA-all-dimensions-v112-20261116"
BASE = "validation/kuuos-v1111-rlp-exact-source-20261115"
BASE_SHA = "66bd3e71739f8a841d7d2723ab45a1475fd276ca"
TARGET = "formal/KUOS/DependentOriginationDoubleDeloopingTypeAAllDimensionsV1_112.lean"
MODULE = "KUOS.DependentOriginationDoubleDeloopingTypeAAllDimensionsV1_112"
PRIOR = "formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111.lean"
PRIOR_BLOB = "35dc6ddf9bcd6ecd4f7141674e75055c306dbfe9"
OUT=Path("/tmp/kuuos-v1112-codeai-all-dimensions")
MCP=Path("/tmp/kuuos-v1112-real-mcp-all-dimensions")
REPORT=Path("/tmp/kuuos-v1112-memoryos/context.json")
MEMORY=Path("memoryos/external/github/2026/11")

INTRO="""import KUOS.DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111

namespace KUOS.DependentOriginationDoubleDeloopingTypeAAllDimensionsV1_112

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101
open KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105
open KUOS.DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111

set_option maxHeartbeats 2000000

/-!
Full degree-by-degree type-(A) completion for the concrete additive B^2 Nat
scaled Duskin nerve. Degree 2: zero cocycle, degree 3: both explicit
completions, degree 4: the independently certified actual four-horn lift,
degrees >=5: the actual visible cocycle. All constructors carry the original
horn map. This is a proof only of the STANDARD type-(A) generator family,
not forward endpoint pushout-products, arbitrary fibrancy or global descent.
-/

/-- The genuine fixed 2, 3, 4 and >=5 fillers cover every admissible
standard inner type-(A) horn, with the exact source map given. -/
theorem natDoubleDelooping_typeA_every_horn_cocycle_completion :
    HasAllStandardTypeAHornCocycleCompletions := by
"""
BODY="""  intro g f
  rcases g with ⟨n, i, hi0, hiN⟩
  have hLeft : 0 < i.val := (Fin.lt_def).mp hi0
  have hRight : i.val < n := (Fin.lt_def).mp hiN
  have hMin : 2 ≤ n := by omega
  by_cases hHigh : 5 ≤ n
  · exact natTypeAHigh_cocycle_completion ⟨n, i, hi0, hiN⟩ hHigh f
  have hCases : n = 2 ∨ n = 3 ∨ n = 4 := by omega
  rcases hCases with hTwo | hThree | hFour
  · subst n
    have hIdx : i = (1 : Fin 3) := by
      apply Fin.ext
      omega
    subst i
    exact natTypeATwo_zero_cocycle_completion f
  · subst n
    have hIdx : i = (1 : Fin 4) ∨ i = (2 : Fin 4) := by
      by_cases hOne : i.val = 1
      · left
        apply Fin.ext
        exact hOne
      · right
        apply Fin.ext
        omega
    rcases hIdx with hOne | hTwo
    · subst i
      exact natTypeAThreeI1_cocycle_completion f
    · subst i
      exact natTypeAThreeI2_cocycle_completion f
  · subst n
    exact ⟨natTypeAFourCocycleCompletion i hi0 hiN f⟩
"""
AFTER="""
/-- Every actual standard type-(A) horn map has an explicitly realized
scaled simplex lift whose composite equals its original horn map. -/
theorem natDoubleDelooping_typeA_every_horn_actual_lift
    (g : StandardTypeAHornGeneratorIndex)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin) :
    ∃ t : standardTypeAScaledSimplex g ⟶ natDoubleDeloopingScaledDuskin,
      standardTypeAScaledHornGeneratorHom g ≫ t = f := by
  rcases natDoubleDelooping_typeA_every_horn_cocycle_completion g f with ⟨K⟩
  exact ⟨K.toLift, K.toLift_fac⟩

/-- Every standard type-(A) generator has literal RLP against terminal B²ℕ. -/
theorem natDoubleDelooping_typeA_every_generator_rlp
    (g : StandardTypeAHornGeneratorIndex) :
    HasLiftingProperty (standardTypeAScaledHornGeneratorHom g)
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  exact natDoubleDelooping_hasLiftingProperty_standardTypeA_of_cocycleCompletions
    g (fun f => natDoubleDelooping_typeA_every_horn_cocycle_completion g f)

/-- Terminal B²ℕ lies in the right orthogonal of the COMPLETE STANDARD
type-(A) scaled inner-horn generator family, not an endpoint product family. -/
theorem natDoubleDelooping_typeA_full_standard_rlp :
    (standardTypeAScaledHornGenerators : MorphismProperty ScaledSSet).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  exact natDoubleDelooping_standardTypeA_rlp_of_cocycleCompletions
    natDoubleDelooping_typeA_every_horn_cocycle_completion

end KUOS.DependentOriginationDoubleDeloopingTypeAAllDimensionsV1_112
"""

def candidates() -> dict[str, str]:
    anchor = "    exact natTypeATwo_zero_cocycle_completion f"
    if BODY.count(anchor)!=1:
        raise RuntimeError("Exact small-dimension proof source drift")
    raw={
        "round1-direct-cases": INTRO+BODY+AFTER,
        "round1-simp-low-index": INTRO+BODY.replace(
            "    exact natTypeATwo_zero_cocycle_completion f",
            "    simpa [natTypeATwoIndex] using (natTypeATwo_zero_cocycle_completion f)"
        ).replace(
            "      exact natTypeAThreeI1_cocycle_completion f",
            "      simpa [natTypeAThreeIndex1] using (natTypeAThreeI1_cocycle_completion f)"
        ).replace(
            "      exact natTypeAThreeI2_cocycle_completion f",
            "      simpa [natTypeAThreeIndex2] using (natTypeAThreeI2_cocycle_completion f)"
        )+AFTER,
        "round1-nonempty-four-bytheorem": INTRO+BODY.replace(
            "    exact ⟨natTypeAFourCocycleCompletion i hi0 hiN f⟩",
            "    exact natTypeAFourCocycleCompletion_nonempty i hi0 hiN f"
        )+AFTER,
    }
    head,branch,tree=require_current_event()
    history=read_observation_directory(MEMORY)
    routed,receipt=route_candidates(raw,history,source_head=head,
                                    source_tree=tree,imported_blob=PRIOR_BLOB)
    if not routed:
        raise RuntimeError("No admissible distinct CodeAI candidate; preserve NO_DATA")
    receipt["cross_source_cause_status"]="UNVERIFIED_HYPOTHESIS"
    receipt["memory_proof_authority"]=False
    receipt["global_RLP_not_inferred"]=True
    REPORT.parent.mkdir(parents=True,exist_ok=False)
    REPORT.write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V1112_MEMORYOS_PREFLIGHT "+json.dumps({
       "memory_cases":len(history),
       "candidates":list(routed),
       "quarantined":receipt.get("quarantined"),
       "hints":receipt.get("analogical_hints"),
       "proof_authority":False},sort_keys=True))
    return routed

def require_current_event() -> tuple[str,str,str]:
    event=json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    pr=event.get("pull_request") or {}
    remote=event.get("repository") or {}
    head=pr.get("head") or {}
    base=pr.get("base") or {}
    if remote.get("full_name")!=REPO or not isinstance(event.get("number"),int) \
       or head.get("ref")!=BRANCH or base.get("ref")!=BASE \
       or base.get("sha")!=BASE_SHA or pr.get("draft") is not True \
       or head.get("repo",{}).get("full_name")!=REPO:
        raise RuntimeError("isolated v1.112 PR event, exact base and draft must match")
    commit=head.get("sha")
    if not isinstance(commit,str) or re.fullmatch("[0-9a-f]{40}",commit) is None:
        raise RuntimeError("missing actual PR HEAD")
    token=os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GitHub source/tree authenticated observation token missing")
    req=urllib.request.Request(
      f"https://api.github.com/repos/{REPO}/git/commits/{commit}",
      headers={"Accept":"application/vnd.github+json","Authorization":"Bearer "+token,
               "User-Agent":"KuuOS-v1112-exact-source-codeai"})
    with urllib.request.urlopen(req,timeout=45) as response:
        obj=json.load(response)
    tree=obj.get("tree",{}).get("sha")
    if obj.get("sha")!=commit or not isinstance(tree,str) or not re.fullmatch("[0-9a-f]{40}",tree):
        raise RuntimeError("source HEAD/tree receipt invalid")
    return commit,BRANCH,tree

def main() -> int:
    # This is NOT the archived #3522 event; check the actual isolated PR.
    # Keep the existing complete source-bound CodeAI+Lean-MCP execution
    # harness, but replace its old PR-number-specific observation gate.
    v103.require_event=require_current_event
    harness.base.require_event=require_current_event
    harness.V105=PRIOR
    harness.V105_BLOB=PRIOR_BLOB
    harness.base.TARGET=TARGET
    harness.base.MODULE=MODULE
    harness.base.PREDECESSOR=PRIOR
    harness.base.ORIGINAL_V103_BLOB=PRIOR_BLOB
    harness.base.OUT=OUT
    harness.base.MCP_OUT=MCP
    harness.candidates=candidates
    return harness.main()

if __name__=="__main__":
    raise SystemExit(main())
