#!/usr/bin/env python3
"""v1.109 MemoryOS x CodeAI: actual four-horn normalized Duskin cocycle.

An independently certified v1.108 proof supplies all five tetrahedral
equations. Three proof constructions are compared under pinned direct Lean.
The realized comparison theorem is about triangles, NOT yet literal horn
restriction or scaled RLP. MemoryOS evidence only filters exact replay.
"""
from __future__ import annotations
import json
from pathlib import Path

from scripts import kuuos_v1106_codeai_label_table_v1 as harness
from scripts.kuuos_v1103_codeai_structural_candidates_v1 import require_event
from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import route_candidates
from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory

TARGET="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourActualCocycleV1_109.lean"
MODULE="KUOS.DependentOriginationDoubleDeloopingTypeAFourActualCocycleV1_109"
PRIOR="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourAllTetrahedraV1_108.lean"
PRIOR_BLOB="6071b265507c1798c8a61ce87a0a828713c97c63"
OUT=Path("/tmp/kuuos-v1109-codeai-actual-cocycle")
MCP=Path("/tmp/kuuos-v1109-real-mcp-actual-cocycle")
REPORT=Path("/tmp/kuuos-v1109-memoryos/context.json")
MEMORY=Path("memoryos/external/github/2026/11")

INTRO="""import KUOS.DependentOriginationDoubleDeloopingTypeAFourAllTetrahedraV1_108

namespace KUOS.DependentOriginationDoubleDeloopingTypeAFourActualCocycleV1_109

open CategoryTheory
open Opposite
open Simplicial
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalCocycleV1_104
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105
open KUOS.DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106
open KUOS.DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107
open KUOS.DependentOriginationDoubleDeloopingTypeAFourAllTetrahedraV1_108

set_option maxHeartbeats 2000000

/-!
The original scaled four-horn map, not arbitrary assumed tetrahedral laws,
induces a genuine normalized Nat Duskin cocycle on Delta[4]. By construction
its strict triangle labels and their Yoneda-realized comparisons agree
with the actual visible horn labels. Literal all-degree restriction and
distinguished-triangle scaledness remain independent future obligations.
-/

"""
HEADER="""/-- Construct a normalized Duskin four-cocycle from the actual scaled
four-horn map, using v1.108 to prove all five equations. -/
def natTypeAFourHornCocycle
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin) : NatNormalizedDuskinCocycle 4 """
VARIANTS={
    "round1-projection-typed":
        """ :=
  natFourCocycleOfLabels (natFourHornLabels i hi0 hi4 f)
    (natFourHorn_all_five_tetrahedra i hi0 hi4 f).1
    (natFourHorn_all_five_tetrahedra i hi0 hi4 f).2.1
    (natFourHorn_all_five_tetrahedra i hi0 hi4 f).2.2.1
    (natFourHorn_all_five_tetrahedra i hi0 hi4 f).2.2.2.1
    (natFourHorn_all_five_tetrahedra i hi0 hi4 f).2.2.2.2
""",
    "round1-rcases-five":
        """ := by
  rcases natFourHorn_all_five_tetrahedra i hi0 hi4 f with
    ⟨h0123, h0124, h0134, h0234, h1234⟩
  exact natFourCocycleOfLabels (natFourHornLabels i hi0 hi4 f)
    h0123 h0124 h0134 h0234 h1234
""",
    "round1-let-five":
        """ := by
  let L : NatFourSimplexTriangleLabels := natFourHornLabels i hi0 hi4 f
  have h : L.eq0123 ∧ L.eq0124 ∧ L.eq0134 ∧ L.eq0234 ∧ L.eq1234 :=
    natFourHorn_all_five_tetrahedra i hi0 hi4 f
  exact natFourCocycleOfLabels L h.1 h.2.1 h.2.2.1 h.2.2.2.1 h.2.2.2.2
""",
}
AFTER="""
/-- The constructed normalized cocycle reads the same ten-label table
on every ordered triple, with repeated-vertex normalization included. -/
theorem natTypeAFourHornCocycle_label
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (a b c : Fin 5) (hab : a ≤ b) (hbc : b ≤ c) :
    (natTypeAFourHornCocycle i hi0 hi4 f).label a b c hab hbc =
      natFourStrictLabel (natFourHornLabels i hi0 hi4 f) a b c := by
  rfl

/-- On strictly ordered triangles of the actual source horn, the cocycle
comparison is the original horn map's actual comparison label. -/
theorem natTypeAFourHornCocycle_strict
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (a b c : Fin 5) (hab : a < b) (hbc : b < c) :
    (natTypeAFourHornCocycle i hi0 hi4 f).label a b c
        (le_of_lt hab) (le_of_lt hbc) =
      natTypeAHornLabel (natTypeAFourIndex i hi0 hi4)
        (Nat.le_refl 4) f a b c (le_of_lt hab) (le_of_lt hbc) := by
  exact (natTypeAFourHornCocycle_label i hi0 hi4 f a b c
    (le_of_lt hab) (le_of_lt hbc)).trans
    (natFourHornLabels_strict i hi0 hi4 f a b c hab hbc)

/-- The Yoneda-realized comparison of every ordered triangle is precisely
the original horn's already-certified ten-label table, including degeneracies.
This does not itself assert equality of full simplicial horn maps. -/
theorem natTypeAFourHornCocycle_realized_triangle
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin)
    (a b c : Fin 5) (hab : a ≤ b) (hbc : b ≤ c) :
    duskinComparison
        ((natTypeAFourHornCocycle i hi0 hi4 f).toSimplexMap.app
          (op ⦋2⦌) (SSet.stdSimplex.triangle a b c hab hbc)) =
      natFourStrictLabel (natFourHornLabels i hi0 hi4 f) a b c := by
  exact (NatNormalizedDuskinCocycle.toSimplexMap_triangle_comparison
    (natTypeAFourHornCocycle i hi0 hi4 f) a b c hab hbc).trans
    (natTypeAFourHornCocycle_label i hi0 hi4 f a b c hab hbc)

end KUOS.DependentOriginationDoubleDeloopingTypeAFourActualCocycleV1_109
"""

def candidates() -> dict[str,str]:
    options={n:INTRO+HEADER+proof+AFTER for n,proof in VARIANTS.items()}
    head,branch,tree=require_event()
    remembered=read_observation_directory(MEMORY)
    retained,history=route_candidates(options,remembered,
                                     source_head=head,source_tree=tree,
                                     imported_blob=PRIOR_BLOB)
    if not retained:
        raise RuntimeError("MemoryOS exact replay blocks all candidates; NO_DATA")
    history["causal_diagnoses_unverified"]=True
    history["memoryos_does_not_certify_kernel"]=True
    REPORT.parent.mkdir(parents=True,exist_ok=False)
    REPORT.write_text(json.dumps(history,indent=2,sort_keys=True)+"\n")
    print("KUUOS_V1109_MEMORYOS_PREFLIGHT "+
      json.dumps({"prior_cases":len(remembered),"candidates":list(retained),
                  "quarantined":history.get("quarantined"),
                  "analogical_hints":history.get("analogical_hints"),
                  "proof_authority":False},sort_keys=True))
    return retained

def main() -> int:
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
