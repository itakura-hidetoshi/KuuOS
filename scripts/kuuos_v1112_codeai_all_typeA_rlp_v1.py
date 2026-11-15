#!/usr/bin/env python3
"""v1.112 CodeAI: combine independently certified literal type-A fillers.

Actual n=2/n=3 sources are in v1.102, n=4 concrete RLP in v1.111,
and n>=5 literal high-dimensional cocycle in v1.103. Does not assume
HasAllStandardTypeAHornCocycleCompletions or RLP as a premise.

This research PR is validation-only and stacked on #3548's exact historical
import closure, not an independent promotion into main.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import re
import urllib.request

from scripts import kuuos_v1106_codeai_label_table_v1 as harness
from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import route_candidates
from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory

REPO="itakura-hidetoshi/KuuOS"
BRANCH="validation/kuuos-v1112-all-standard-typeA-rlp-20261115"
BASE="validation/kuuos-v1111-rlp-exact-source-20261115"
TARGET="formal/KUOS/DependentOriginationDoubleDeloopingAllStandardTypeACompletionV1_112.lean"
MODULE="KUOS.DependentOriginationDoubleDeloopingAllStandardTypeACompletionV1_112"
PRIOR="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111.lean"
PRIOR_BLOB="35dc6ddf9bcd6ecd4f7141674e75055c306dbfe9"
MEMORY=Path("memoryos/external/github/2026/11")
OUT=Path("/tmp/kuuos-v1112-codeai-all-typeA")
MCP=Path("/tmp/kuuos-v1112-real-mcp-all-typeA")
REPORT=Path("/tmp/kuuos-v1112-memoryos/feedback.json")

INTRO="""import KUOS.DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111

namespace KUOS.DependentOriginationDoubleDeloopingAllStandardTypeACompletionV1_112

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100
open KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101
open KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105
open KUOS.DependentOriginationDoubleDeloopingTypeAFourCocycleCompletionV1_111

set_option maxHeartbeats 2000000

/-!
All concrete standard type-(A) horn lifts into the additive double delooping:
n = 2 from v1.102; n = 3 from v1.102; n = 4 from v1.111;
n >= 5 from v1.103. This does not assert scaled type-(C) RLP,
forward endpoint RLP, global fibrancy, or an unverified descent to main.
-/

/-- Every actual scaled type-(A) inner horn has an explicit arithmetic
cocycle completion, by its proven geometric dimension case. -/
theorem natDoubleDelooping_allStandardTypeA_completions :
    HasAllStandardTypeAHornCocycleCompletions := by
  intro g f
  cases g with
  | mk n i hi0 hiLast =>
    have hleft : 0 < i.val := (Fin.lt_def).mp hi0
    have hright : i.val < n := by simpa using (Fin.lt_def).mp hiLast
    by_cases hn2 : n = 2
    · subst n
"""
CASE2={
"round1-explicit-fin-ext":"""      have hi1 : i = (1 : Fin 3) := by
        apply Fin.ext
        omega
      subst i
      exact natTypeATwo_zero_cocycle_completion f
""",
"round1-omega-fin-eq":"""      have hi1 : i = (1 : Fin 3) := by omega
      subst i
      exact natTypeATwo_zero_cocycle_completion f
""",
"round1-fin-cases":"""      fin_cases i <;> simp_all
      exact natTypeATwo_zero_cocycle_completion f
"""
}
CASE3={
"round1-explicit-fin-ext":"""    · by_cases hn3 : n = 3
      · subst n
        by_cases hi1 : i = (1 : Fin 4)
        · subst i
          exact natTypeAThreeI1_cocycle_completion f
        · have hi2 : i = (2 : Fin 4) := by
            apply Fin.ext
            have hn1 : i.val ≠ 1 := by
              intro h
              apply hi1
              apply Fin.ext
              simpa using h
            omega
          subst i
          exact natTypeAThreeI2_cocycle_completion f
""",
"round1-omega-fin-eq":"""    · by_cases hn3 : n = 3
      · subst n
        by_cases hi1 : i = (1 : Fin 4)
        · subst i
          exact natTypeAThreeI1_cocycle_completion f
        · have hi2 : i = (2 : Fin 4) := by omega
          subst i
          exact natTypeAThreeI2_cocycle_completion f
""",
"round1-fin-cases":"""    · by_cases hn3 : n = 3
      · subst n
        fin_cases i <;> simp_all
        · exact natTypeAThreeI1_cocycle_completion f
        · exact natTypeAThreeI2_cocycle_completion f
"""
}
TAIL="""      · by_cases hn4 : n = 4
        · subst n
          exact natTypeAFourCocycleCompletion_nonempty i hi0 hiLast f
        · have hn5 : 5 ≤ n := by omega
          exact natTypeAHigh_cocycle_completion ⟨n, i, hi0, hiLast⟩ hn5 f

/-- Concrete additive double delooping has RLP against every literal
standard type-(A) scaled horn inclusion, not just four-dimensional ones. -/
theorem natDoubleDelooping_allStandardTypeA_rlp :
    (standardTypeAScaledHornGenerators : MorphismProperty ScaledSSet).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  exact natDoubleDelooping_standardTypeA_rlp_of_cocycleCompletions
    natDoubleDelooping_allStandardTypeA_completions

end KUOS.DependentOriginationDoubleDeloopingAllStandardTypeACompletionV1_112
"""

def require_event():
    event=json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    pr=event.get("pull_request",{})
    if event.get("repository",{}).get("full_name")!=REPO:
        raise RuntimeError("Repository identity does not match KuuOS")
    if pr.get("head",{}).get("ref")!=BRANCH or pr.get("base",{}).get("ref")!=BASE:
        raise RuntimeError("Exact validation-only head/base branch required")
    head=pr["head"]["sha"]
    token=os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Exact source GitHub observation requires token")
    req=urllib.request.Request(
       f"https://api.github.com/repos/{REPO}/git/commits/{head}",
       headers={"Accept":"application/vnd.github+json",
                "Authorization":"Bearer "+token,
                "User-Agent":"KuuOS-CodeAI-v1112"})
    with urllib.request.urlopen(req,timeout=45) as res:
        data=json.load(res)
    tree=data.get("tree",{}).get("sha")
    if data.get("sha")!=head or not isinstance(tree,str) or not re.fullmatch("[0-9a-f]{40}",tree):
        raise RuntimeError("Exact immutable source HEAD/tree not verified")
    return head,BRANCH,tree

def candidates():
    opts={name:INTRO+CASE2[name]+CASE3[name]+TAIL for name in CASE2}
    head,branch,tree=require_event()
    entries=read_observation_directory(MEMORY)
    filtered,history=route_candidates(opts,entries,source_head=head,
                   source_tree=tree,imported_blob=PRIOR_BLOB)
    if not filtered:
        raise RuntimeError("No admissible distinct CodeAI candidates: NO_DATA")
    history["memory_is_not_proof_or_commit_authority"]=True
    history["causal_explanations"]="UNVERIFIED_HYPOTHESIS"
    REPORT.parent.mkdir(parents=True,exist_ok=False)
    REPORT.write_text(json.dumps(history,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V1112_MEMORYOS_PREFLIGHT "+json.dumps({
        "cases":len(entries),"retained":list(filtered),
        "quarantined":history.get("quarantined"),
        "analogy":history.get("analogical_hints"),
        "proof_authority":False},sort_keys=True))
    return filtered

def main():
    harness.V105=PRIOR
    harness.V105_BLOB=PRIOR_BLOB
    harness.base.TARGET=TARGET
    harness.base.MODULE=MODULE
    harness.base.PREDECESSOR=PRIOR
    harness.base.ORIGINAL_V103_BLOB=PRIOR_BLOB
    harness.base.OUT=OUT
    harness.base.MCP_OUT=MCP
    harness.base.require_event=require_event
    harness.candidates=candidates
    return harness.main()

if __name__=="__main__":
    raise SystemExit(main())
