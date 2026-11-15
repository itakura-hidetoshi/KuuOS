#!/usr/bin/env python3
"""v1.107 CodeAI: transport actual four-horn 3-face equations to ten-label table.

Read source-bound, append-only MemoryOS hints before generating proof candidates.
Only exact source-bound failures can exclude identical byte-for-byte repeats.
Use pinned direct Lean for all candidates, then real Lean MCP for green only.
No candidate can be promoted or independently certified in this workflow.
"""
from __future__ import annotations
import json
from pathlib import Path

from scripts import kuuos_v1106_codeai_label_table_v1 as harness
from scripts.kuuos_v1103_codeai_structural_candidates_v1 import require_event
from runtime.kuuos_codeai_lean_failure_memoryos_v0_1 import route_candidates
from runtime.kuuos_codeai_lean_observation_intake_v0_2 import read_observation_directory

TARGET = "formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107.lean"
MODULE = "KUOS.DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107"
PRIOR = "formal/KUOS/DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106.lean"
PRIOR_BLOB = "99ca499c470ba7b190623ed9e90e3f8d2dfb8058"
MEMORY = Path("memoryos/external/github/2026/11")
REPORT = Path("/tmp/kuuos-v1107-memoryos/context.json")
OUT = Path("/tmp/kuuos-v1107-codeai-face-table")
MCP = Path("/tmp/kuuos-v1107-real-mcp-face-table")

INTRO = """import KUOS.DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106

namespace KUOS.DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107

open CategoryTheory
open Opposite
open Simplicial
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalCocycleV1_104
open KUOS.DependentOriginationDoubleDeloopingTypeAFourDimensionalFaceCoherenceV1_105
open KUOS.DependentOriginationDoubleDeloopingTypeAFourHornLabelTableV1_106

set_option maxHeartbeats 2000000

/-!
These theorems transport the additive equations of actual visible tetrahedra
through the given four-horn map to the ten labels already extracted in v1.106.
Each implication explicitly requires that the corresponding face is visible.
The missing face and the Yoneda realization are NOT assumed or proved here.
-/

"""
TAIL = "\nend KUOS.DependentOriginationDoubleDeloopingTypeAFourVisibleFaceTableV1_107\n"

# Face j of Delta[4] is the ordered tetrahedron with vertex j removed.
FACES = ((4, "eq0123"), (3, "eq0124"), (2, "eq0134"),
         (1, "eq0234"), (0, "eq1234"))

def proof(face: int, label: str, tactic: str) -> str:
    h = (
        "natTypeAFourVisibleFace_additive_cocycle\n"
        f"    i hi0 hi4 f ({face} : Fin 5) hj"
    )
    if tactic == "exact":
        return "  exact " + h + "\n"
    if tactic == "convert-rfl":
        return "  convert (" + h + ") using 1 <;> rfl\n"
    simp_rules = (
        "NatFourSimplexTriangleLabels." + label +
        ", NatTetrahedronEquation, natFourHornLabels,"
        " natHornTetraLabel, natTypeAFourFace"
    )
    if tactic == "simp":
        return "  simpa [" + simp_rules + "] using (" + h + ")\n"
    if tactic == "simp-only":
        return "  simpa only [" + simp_rules + "] using (" + h + ")\n"
    if tactic == "delta":
        return "  simpa [" + simp_rules + ", SSet.horn.face] using (" + h + ")\n"
    raise ValueError("Unknown tactic, NO_DATA")

def source(tactic: str) -> str:
    out=[INTRO]
    for face, label in FACES:
        out.append(
            f"/-- Real visible face {face} provides table equation {label}. -/\n"
            f"theorem natFourHorn_visible_face{face}_{label}\n"
            "    (i : Fin 5) (hi0 : 0 < i) (hi4 : i < Fin.last 4)\n"
            "    (f : standardTypeAScaledHorn (natTypeAFourIndex i hi0 hi4) ⟶\n"
            "      natDoubleDeloopingScaledDuskin)\n"
            f"    (hj : ({face} : Fin 5) ≠ i) :\n"
            f"    (natFourHornLabels i hi0 hi4 f).{label} := by\n"
            + proof(face,label,tactic)+"\n"
        )
    return "".join(out) + TAIL

def candidates() -> dict[str,str]:
    proposals = {f"round1-{tactic}":source(tactic) for tactic in
                 ("exact","convert-rfl","simp","simp-only","delta")}
    head,branch,tree=require_event()
    cases=read_observation_directory(MEMORY)
    filtered,route=route_candidates(proposals,cases,source_head=head,
                                   source_tree=tree,imported_blob=PRIOR_BLOB)
    if not filtered:
        raise RuntimeError("MemoryOS filtered all proposals; do not infer impossibility")
    route["candidate_obstruction_is_hypothesis"] = True
    route["proof_authority"] = False
    route["new_axioms"] = False
    REPORT.parent.mkdir(parents=True,exist_ok=False)
    REPORT.write_text(json.dumps(route,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V1107_MEMORYOS_PREFLIGHT " + json.dumps({
        "cases":len(cases),"retained":list(filtered),
        "quarantined":route.get("quarantined"),
        "analogical_hints":route.get("analogical_hints"),
        "authority":False},sort_keys=True))
    return filtered

def main() -> int:
    # The version-pinned v1.106 harness still checks the unchanged v1.103 root.
    harness.V105 = PRIOR
    harness.V105_BLOB = PRIOR_BLOB
    harness.base.TARGET = TARGET
    harness.base.MODULE = MODULE
    harness.base.PREDECESSOR = PRIOR
    harness.base.ORIGINAL_V103_BLOB = PRIOR_BLOB
    harness.base.OUT = OUT
    harness.base.MCP_OUT = MCP
    harness.candidates = candidates
    return harness.main()

if __name__ == "__main__":
    raise SystemExit(main())
