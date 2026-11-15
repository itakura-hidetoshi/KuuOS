#!/usr/bin/env python3
"""KuuOS v1.108: MemoryOS-routed CodeAI v1.99 four-implies-five actual horn proof.

Only the actual four visible faces from certified v1.107 and their arithmetic
dependency are used. No new axioms, sorry, RLP or fabricated visible face.
Failure diagnostics and causal hypotheses remain separate in MemoryOS.
"""
from __future__ import annotations
import json
from pathlib import Path
from scripts import kuuos_v1106_codeai_label_table_v1 as harness
from scripts.kuuos_v1103_codeai_structural_candidates_v1 import require_event
from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import route_candidates
from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory

TARGET="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourAllTetrahedraV1_108.lean"
MODULE="KUOS.DependentOriginationDoubleDeloopingTypeAFourAllTetrahedraV1_108"
PRIOR="formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107.lean"
PRIOR_BLOB="37c3e75c5d74c74b8d125983c9cd257f9757995a"
OUT=Path("/tmp/kuuos-v1108-codeai-four-imply-five")
MCP=Path("/tmp/kuuos-v1108-real-mcp-four-imply-five")
REPORT=Path("/tmp/kuuos-v1108-memoryos/context.json")
MEMORY=Path("memoryos/external/github/2026/11")

INTRO="""import KUOS.DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107

namespace KUOS.DependentOriginationDoubleDeloopingTypeAFourAllTetrahedraV1_108

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105
open KUOS.DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106
open KUOS.DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107

set_option maxHeartbeats 2000000

/-!
For inner indices 1, 2, 3, the four visible 3-faces of an actual type-A
four-horn determine the fifth missing tetrahedral equation through v1.99.
The theorem does not yet construct the Yoneda restriction or terminal RLP.
-/

/-- All five exact ten-label tetrahedral equations are forced by the
given actual type-(A) four-horn map, including the missing one. -/
theorem natFourHorn_all_five_tetrahedra
    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)
    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶
      natDoubleDeloopingScaledDuskin) :
    (natFourHornLabels i hi0 hi4 f).eq0123 ∧
    (natFourHornLabels i hi0 hi4 f).eq0124 ∧
    (natFourHornLabels i hi0 hi4 f).eq0134 ∧
    (natFourHornLabels i hi0 hi4 f).eq0234 ∧
    (natFourHornLabels i hi0 hi4 f).eq1234 := by
  let L : NatFourSimplexTriangleLabels := natFourHornLabels i hi0 hi4 f
  change L.eq0123 ∧ L.eq0124 ∧ L.eq0134 ∧ L.eq0234 ∧ L.eq1234
"""
COMMON="""  have h0123 : L.eq0123 :=
    natFourHorn_visible_face4_eq0123 i hi0 hi4 f h4
  have h1234 : L.eq1234 :=
    natFourHorn_visible_face0_eq1234 i hi0 hi4 f h0
  by_cases hi1 : i = (1 : Fin 5)
  · have h3 : (3 : Fin 5) ≠ i := by rw [hi1]; decide
    have h2 : (2 : Fin 5) ≠ i := by rw [hi1]; decide
    have h0124 : L.eq0124 :=
      natFourHorn_visible_face3_eq0124 i hi0 hi4 f h3
    have h0134 : L.eq0134 :=
      natFourHorn_visible_face2_eq0134 i hi0 hi4 f h2
    have h0234 : L.eq0234 :=
      natFour_typeA_index1_missing_face L h0123 h0124 h0134 h1234
    exact ⟨h0123, h0124, h0134, h0234, h1234⟩
  · by_cases hi2 : i = (2 : Fin 5)
    · have h3 : (3 : Fin 5) ≠ i := by rw [hi2]; decide
      have h1 : (1 : Fin 5) ≠ i := by rw [hi2]; decide
      have h0124 : L.eq0124 :=
        natFourHorn_visible_face3_eq0124 i hi0 hi4 f h3
      have h0234 : L.eq0234 :=
        natFourHorn_visible_face1_eq0234 i hi0 hi4 f h1
      have h0134 : L.eq0134 :=
        natFour_typeA_index2_missing_face L h0123 h0124 h0234 h1234
      exact ⟨h0123, h0124, h0134, h0234, h1234⟩
    · by_cases hi3 : i = (3 : Fin 5)
      · have h2 : (2 : Fin 5) ≠ i := by rw [hi3]; decide
        have h1 : (1 : Fin 5) ≠ i := by rw [hi3]; decide
        have h0134 : L.eq0134 :=
          natFourHorn_visible_face2_eq0134 i hi0 hi4 f h2
        have h0234 : L.eq0234 :=
          natFourHorn_visible_face1_eq0234 i hi0 hi4 f h1
        have h0124 : L.eq0124 :=
          natFour_typeA_index3_missing_face L h0123 h0134 h0234 h1234
        exact ⟨h0123, h0124, h0134, h0234, h1234⟩
      · have hv0 : 0 < i.val := (Fin.lt_def).mp hi0
        have hv4 : i.val < 4 := (Fin.lt_def).mp hi4
        have hn1 : i.val ≠ 1 := by
          intro h
          apply hi1
          apply Fin.ext
          simpa using h
        have hn2 : i.val ≠ 2 := by
          intro h
          apply hi2
          apply Fin.ext
          simpa using h
        have hn3 : i.val ≠ 3 := by
          intro h
          apply hi3
          apply Fin.ext
          simpa using h
        omega
"""
BOUNDS={
    "typed-val": """  have h0 : (0 : Fin 5) ≠ i := by
    intro h
    have hv : (0 : Fin 5).val = i.val := congrArg Fin.val h
    have hi : 0 < i.val := (Fin.lt_def).mp hi0
    omega
  have h4 : (4 : Fin 5) ≠ i := by
    intro h
    have hv : (4 : Fin 5).val = i.val := congrArg Fin.val h
    have hi : i.val < 4 := (Fin.lt_def).mp hi4
    omega
""",
    "subst-bounds": """  have h0 : (0 : Fin 5) ≠ i := by
    intro h
    subst i
    omega
  have h4 : (4 : Fin 5) ≠ i := by
    intro h
    subst i
    omega
""",
    "omega-bounds": """  have h0 : (0 : Fin 5) ≠ i := by omega
  have h4 : (4 : Fin 5) ≠ i := by omega
""",
}
TAIL="\nend KUOS.DependentOriginationDoubleDeloopingTypeAFourAllTetrahedraV1_108\n"

def candidates() -> dict[str,str]:
    proposed={name:INTRO+before+COMMON+TAIL for name,before in BOUNDS.items()}
    head,branch,tree=require_event()
    cases=read_observation_directory(MEMORY)
    filtered,receipt=route_candidates(proposed,cases,source_head=head,
                                      source_tree=tree,imported_blob=PRIOR_BLOB)
    if not filtered:
        raise RuntimeError("No admissible distinct candidates; keep NO_DATA")
    receipt["analogy_is_causal_hypothesis_only"]=True
    receipt["memory_grants_no_proof_authority"]=True
    REPORT.parent.mkdir(parents=True,exist_ok=False)
    REPORT.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print("KUUOS_V1108_MEMORYOS_PREFLIGHT "+json.dumps({
        "case_count":len(cases),"retained":list(filtered),
        "quarantined":receipt.get("quarantined"),
        "hints":receipt.get("analogical_hints"),
        "authority":False},sort_keys=True))
    return filtered

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
