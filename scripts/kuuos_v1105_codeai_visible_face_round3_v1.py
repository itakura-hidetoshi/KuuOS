#!/usr/bin/env python3
"""v1.105 CodeAI round3: dependent proof irrelevance / reducible index n=4.

Pinned Lean round2 rejects dependent by decide before reducing the
four-horn index. Proposals use a kernel theorem for 4<=4 or reduction first.
All candidate code generated from the exact previous typed source; no sorry,
new axiom, theorem weakening, Git mutation, or CI authority inference.
"""
from __future__ import annotations
from pathlib import Path
from scripts import kuuos_v1105_codeai_visible_face_round2_v1 as previous

OLD = "(natTypeAFourIndex i hi0 hi4) (by decide)"
NEWFORMS = {
    "round3-four-index-refl": "(natTypeAFourIndex i hi0 hi4) (Nat.le_refl 4)",
    "round3-four-index-tactic": "(natTypeAFourIndex i hi0 hi4) (by change (4 : Nat) ≤ 4; exact Nat.le_refl 4)",
    "round3-four-index-dsimp": "(natTypeAFourIndex i hi0 hi4) (by dsimp only [natTypeAFourIndex]; decide)",
}

def candidates() -> dict[str,str]:
    source = previous.round2_texts()["round2-universe-visible-simpa"]
    if source.count(OLD) != 5:
        raise RuntimeError("v1.105 dependent proof source drift: expected 5 exact occurrences")
    return {key:source.replace(OLD,term) for key,term in NEWFORMS.items()}

def main() -> int:
    previous.prior.candidates=candidates
    previous.prior.base.OUT=Path("/tmp/kuuos-v1105-codeai-round3")
    previous.prior.base.MCP_OUT=Path("/tmp/kuuos-v1105-real-mcp-round3")
    return previous.prior.main()

if __name__=="__main__":
    raise SystemExit(main())
