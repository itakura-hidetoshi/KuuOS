#!/usr/bin/env python3
"""v1.120 CodeAI round3: exact contextual rewrite repair by equality transport.

Failure basis: source HEAD 921decee, run 43786351742. The three
identity-closed candidates failed at rw [heq] at hs at line 94, while
the namespace-only candidate also left the identity equation open.
Use new proof tactics without changing any theorem statement or premise.
Run existing pinned direct Lean portfolio, then green-only real Lean MCP,
then second direct Lean. This is an experiment, not an independent proof.
"""
from __future__ import annotations
from pathlib import Path
from scripts import kuuos_v120_codeai_induced_scaling_recovery_v1 as prior
from scripts.kuuos_lean_mcp_repair_loop_v1 import forbidden_code_constructs

OUT=Path("/tmp/kuuos-v120-codeai-round3")
MCP=Path("/tmp/kuuos-v120-real-mcp-round3")
PREVIOUS=prior.candidates
BAD_REWRITE="    rw [heq] at hs\n    exact hs"

def candidates(original: str) -> dict[str, str]:
    variants=PREVIOUS(original)
    if any(v.count(BAD_REWRITE)!=1 for v in variants.values()):
        raise RuntimeError("NO_DATA: v1.120 exact failed rewrite pattern drift")
    if variants["round2-explicit-id-comp"].count("    exact Category.id_comp f.map")!=1:
        raise RuntimeError("NO_DATA: Lean identity proof anchor drift")
    sources={
      "round3-congrArg-transport":
        variants["round2-explicit-id-comp"].replace(
            BAD_REWRITE,
            "    exact (congrArg (IsScaledMap sDelta sX) heq).mp hs"),
      "round3-eq-substitution":
        variants["round2-explicit-id-simp"].replace(
            BAD_REWRITE,
            "    exact heq ▸ hs"),
      "round3-simpa-transport":
        variants["round2-explicit-id-simp-general"].replace(
            BAD_REWRITE,
            "    simpa only [heq] using hs"),
      "round3-eqndrec-transport":
        variants["round2-explicit-id-comp"].replace(
            BAD_REWRITE,
            "    exact Eq.ndrec hs heq"),
    }
    if len({prior.blob(x.encode("utf-8")) for x in sources.values()})!=4:
        raise RuntimeError("NO_DATA: CodeAI candidates must have distinct blobs")
    for name,source in sources.items():
        if (source.count("theorem ")!=original.count("theorem ")
            or source.count("#print axioms")!=original.count("#print axioms")
            or not source.startswith(original.split("namespace ",1)[0])
            or forbidden_code_constructs(source)):
            raise RuntimeError("FORBIDDEN: source weakening, new axiom, sorry or changed inventory: "+name)
    return sources

def main() -> int:
    prior.candidates=candidates
    prior.OUT=OUT
    prior.MCP=MCP
    return prior.main()

if __name__=="__main__":
    raise SystemExit(main())
