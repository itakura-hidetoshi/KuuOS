#!/usr/bin/env python3
"""v1.76 exact-source CodeAI v5: rank-element extraction and colimit uniqueness.

Temporary Lean candidates only, generated from the v4 independently tested
best candidate (37 diagnostics). No theorem source adoption, no new axioms,
no trust bypass, no history mutation. Restore the original source in finally.
"""
from __future__ import annotations
import hashlib
import json
import os
import pathlib
import re
import subprocess
import tempfile
from scripts import ci_kuuos_v164_codeai as prior
from scripts import ci_kuuos_v176_rank_index_probe_v4 as v4
from scripts.kuuos_lean_mcp_repair_loop_v1 import FORBIDDEN_NEW, mask_lean_comments

ROOT = pathlib.Path(".").resolve()
REL = v4.REL
OUT = pathlib.Path("/tmp/kuuos-v176-codeai-rank-colimit-v5")
MANIFEST = "scripts/kuuos_v176_codeai_rank_colimit_v5.json"

RANK_OLD = """  have ht :
      t ∈
        (⊤ : (((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).Subcomplex)).obj d := by
    simp
  rw [← standardTypeABoundaryPrism_iSup_filtration g] at ht
  simp only [Subfunctor.iSup_obj, Set.mem_iUnion] at ht
  obtain ⟨j, hj⟩ := ht
  refine ⟨j, ⟨t, hj⟩, ?_⟩
  rfl"""
RANK_NEW_PREFIX = """  have hexists : ∃ (j : ℕ),
      t ∈ ((standardTypeABoundaryPrismRankFunction.{u} g).filtration j).obj d := by
    have ht :
        t ∈ (⊤ : (((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).Subcomplex)).obj d := by
"""
RANK_NEW_SUFFIX = """    rw [← standardTypeABoundaryPrism_iSup_filtration g] at ht
    simpa [Subfunctor.iSup_obj] using ht
  obtain ⟨j, hj⟩ := hexists
  refine ⟨j, ⟨t, hj⟩, ?_⟩
  rfl"""
TOP_PROOFS = {
    "top-change": """      change t ∈ (Set.univ : Set _)
      exact Set.mem_univ t
""",
    "top-simp": """      simp only [Subfunctor.top_obj, Set.mem_univ]
""",
}
UNIQ_OLD = """  uniq s m hm := by
    apply ScaledSSet.ScaledMap.ext
    apply (standardTypeABoundaryPrismRelativeCellComplex g).isColimit.hom_ext
    intro j
    have h := congrArg ScaledSSet.ScaledMap.map (hm j)
    simpa [standardTypeABoundaryPrismScaledRankCocone,
      standardTypeABoundaryPrismRankStageToCylinder,
      standardTypeABoundaryPrismScaledRankDesc,
      standardTypeABoundaryPrismUnderlyingRankCocone] using h"""
UNIQ_NEW = """  uniq s m hm := by
    apply ScaledSSet.ScaledMap.ext
    apply (standardTypeABoundaryPrismRelativeCellComplex g).isColimit.hom_ext
    intro j
    have h := congrArg ScaledSSet.ScaledMap.map (hm j)
    have hfac :=
      (standardTypeABoundaryPrismRelativeCellComplex g).isColimit.fac
        (standardTypeABoundaryPrismUnderlyingRankCocone g s) j
    calc
      (standardTypeABoundaryPrismRelativeCellComplex g).incl.app j ≫ m.map =
          (s.ι.app j).map := by
            change (standardTypeABoundaryPrismRankStageToCylinder g j).map ≫
              m.map = (s.ι.app j).map
            exact h
      _ = (standardTypeABoundaryPrismRelativeCellComplex g).incl.app j ≫
          (standardTypeABoundaryPrismRelativeCellComplex g).isColimit.desc
            (standardTypeABoundaryPrismUnderlyingRankCocone g s) := hfac.symm"""
OBJ_OLD = """  match Nat.bodd n with
  | false => standardTypeABoundaryPrismRankStage g (Nat.div2 n)
  | true => standardTypeABoundaryPrismRankAPhase g (Nat.div2 n)"""
OBJ_NEW = """  Nat.bitCasesOn n (fun b j =>
    if b then standardTypeABoundaryPrismRankAPhase g j
    else standardTypeABoundaryPrismRankStage g j)"""


def patch(s: str, old: str, new: str, name: str) -> str:
    assert s.count(old) == 1, (name, s.count(old))
    return s.replace(old, new)


def candidate(base: str, operations: list[str]) -> str:
    s = base
    for operation in operations:
        if operation in TOP_PROOFS:
            s = patch(s, RANK_OLD,
                      RANK_NEW_PREFIX + TOP_PROOFS[operation] + RANK_NEW_SUFFIX,
                      operation)
        elif operation == "uniq-calc":
            s = patch(s, UNIQ_OLD, UNIQ_NEW, operation)
        elif operation == "bit-object":
            s = patch(s, OBJ_OLD, OBJ_NEW, operation)
        else:
            raise AssertionError(operation)
    return s


def main() -> None:
    os.chdir(ROOT)
    prior.pins(ROOT)
    m = json.loads((ROOT / MANIFEST).read_text())
    assert m["schema"] == "kuuos_v176_codeai_rank_colimit_v5"
    assert m["all_candidates_uncertified"] is True
    assert len(os.environ["SOURCE_HEAD"]) == 40
    target = ROOT / REL
    orig = target.read_bytes()
    historic = (ROOT / "legacy/v5.291" / REL).read_bytes()
    assert orig == historic, "original changed -- refuse to test stale candidates"
    assert prior.blob(orig) == m["source_blob"] == os.environ["SOURCE_BLOB"]
    dep = ROOT / "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousBPhaseV1_75.lean"
    assert prior.blob(dep.read_bytes()) == m["dependency_blob"]
    base = v4.candidate_for(v4.reconstruct(orig.decode()), ["map-index", "bit-cases"])
    assert prior.blob(base.encode()) == m["baseline_blob"]
    original_inv = prior.inventory(orig.decode())
    assert len(original_inv) >= 10 and len(set(original_inv)) == len(original_inv)
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    try:
        for v in m["variants"]:
            name = v["name"]
            s = candidate(base, v["operations"])
            assert prior.inventory(s) == original_inv
            assert not FORBIDDEN_NEW.findall(mask_lean_comments(s)), name
            sha = prior.blob(s.encode("utf8"))
            target.write_text(s, encoding="utf8")
            try:
                with tempfile.TemporaryDirectory(prefix="kuuos-v176-v5-lean-") as td:
                    olean = pathlib.Path(td) / "test.olean"
                    p = subprocess.run(
                        ["lake", "env", "lean", "-DwarningAsError=true",
                         "-Dweak.sorryAsError=true", "-Dpp.universes=true",
                         "-Dpp.explicit=true", "-Dpp.coercions.types=true",
                         "-o", str(olean), REL],
                        cwd=ROOT, capture_output=True, text=True, timeout=1800)
                    log = p.stdout + "\n" + p.stderr
                    errors = re.findall(r"(?m)^.*\berror(?:\([^)]*\))?:.*$", log)
                    ok = p.returncode == 0 and olean.exists() and not errors and "sorryAx" not in log
            finally:
                target.write_bytes(orig)
            (OUT / (name + ".log")).write_text(log, encoding="utf8")
            row = {"head": os.environ["SOURCE_HEAD"], "source_blob":m["source_blob"],
                   "name":name,"operations":v["operations"],"candidate_blob":sha,
                   "sha256":hashlib.sha256(s.encode()).hexdigest(),
                   "returncode":p.returncode,"errors":len(errors),
                   "first_errors":errors[:30],"direct_lean_success":ok,
                   "real_mcp_certified":False,
                   "independent_axioms_certified":False,"adopted":False}
            results.append(row)
            (OUT / "results.json").write_text(json.dumps(results, indent=2))
            print("KUUOS_V176_V5_UNCERTIFIED "+json.dumps(row),flush=True)
    finally:
        target.write_bytes(orig)
    assert target.read_bytes() == historic
    print("KUUOS_V176_V5_COMPARE_FINISHED "+json.dumps({
        "tried":len(results),
        "direct_green":[r["name"] for r in results if r["direct_lean_success"]],
        "source_restored":True,"certified":False,"adopted":False,
        "git_write_performed":False}),flush=True)


if __name__ == "__main__":
    main()
