#!/usr/bin/env python3
"""v1.105 CodeAI round2: explicit SSet universe and separately typed face.

Correction based on entire isolated pinned-Lean diagnostic blocks, not merely
reported error lines. Theorems/properties are not weakened, no sorry/axioms.
Stages remain CodeAI -> direct pinned Lean all -> only green real MCP -> CI.
"""
from __future__ import annotations

from pathlib import Path
from scripts import kuuos_v1105_codeai_visible_face_v1 as prior

NEWFACE = """\
/-- A concrete visible tetrahedron, with its source universe fixed to the
same universe as the scaled map in this fixed Lean/mathlib build. -/
def natTypeAFourFace
    (i j : Fin 5) (hj : j ≠ i) :
    (Λ[4, i] : SSet.{0}).obj (op ⦋3⦌) :=
  SSet.horn.face i j hj

"""

def round2_texts() -> dict[str,str]:
    header = prior.HEADER.replace("(Λ[g.n, g.i] : SSet)", "(Λ[g.n, g.i] : SSet.{0})")
    if header == prior.HEADER or header.count("SSet.{0}") != 2:
        raise RuntimeError("v1.105 horn source universe guard drift")
    tail = prior.TAIL
    anchor = "/-- Every literal visible codimension-one 3-face"
    if tail.count(anchor)!=1:
        raise RuntimeError("v1.105 face anchor drift")
    tail = tail.replace(anchor, NEWFACE + anchor, 1)
    old = ("    let x : (Λ[4, i] : SSet).obj (op ⦋3⦌) :=\n"
           "      SSet.horn.face i j hj\n")
    if tail.count(old)!=1:
        raise RuntimeError("v1.105 dependent local let drift")
    tail = tail.replace(old, "", 1)
    if tail.count(" f x\n") != 4:
        raise RuntimeError("v1.105 actual horn-face statement drift")
    tail = tail.replace(" f x\n", " f (natTypeAFourFace i j hj)\n")
    if tail.count(" f (SSet.horn.face i j hj)")!=1:
        raise RuntimeError("v1.105 proof argument drift")
    tail = tail.replace(" f (SSet.horn.face i j hj)",
                        " f (natTypeAFourFace i j hj)")
    tactics = {
        "round2-universe-visible-simpa":
            "  simpa [natHornTetraLabel, sigma, e01, e12, e23] using hcoc",
        "round2-universe-visible-simpa-only":
            "  simpa only [natHornTetraLabel, sigma, e01, e12, e23] using hcoc",
        "round2-universe-visible-reduce":
            "  simpa [natHornTetraLabel, sigma, e01, e12, e23, natOrdinalEdge] using hcoc",
    }
    return {key:header+proof+tail for key,proof in tactics.items()}

def main() -> int:
    prior.candidates=round2_texts
    prior.base.OUT=Path("/tmp/kuuos-v1105-codeai-round2")
    prior.base.MCP_OUT=Path("/tmp/kuuos-v1105-real-mcp-round2")
    return prior.main()

if __name__=="__main__":
    raise SystemExit(main())
