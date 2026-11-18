#!/usr/bin/env python3
"""v1.72 version-bound CodeAI candidate PROBE. Zero proof authority; no source adoption.
Runs multiple source variants through the exact pinned Lean compiler in disposable CI.
A green direct result still requires real MCP and separate 26-axiom independent CI.
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

REL = "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72.lean"
BASE = "152c9b0bd44c22cd67059e25ed00784741d66488"
CANDIDATES = {
    "namespace-scope-only": "caa44f613bc9398470120ec05936580bad9dad37",
    "namespace-plus-finite-two-step": "123d2a5087f4a47bba187e38e55c856cb3485911",
    "api-open-pushout": "06623431bc5d29fef4fe35e9e2410fc999eae680",
    "api-iso": "a4cf793204006d6b35dafe4c84b4916964567731",
    "api-iso-transport": "8ec3779ccfab820166914fadf3bdd8cc4f939f2e",
    "universe-raw-pushout": "87c7cfddeeae12e56b80213fffd35a87fe406b33",
    "universe-generic-dim-iso": "a313c70660c73088230db20a4d66bafa3005f5d9",
    "universe-typed-transport": "3a900a024bf5e2818cd8516f5b6746b19c0b4577",
}
SCOPE_AT = "open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19\n"
SCOPE_ADD = "\n".join([
    "open KUOS.DependentOriginationScaledTerminalRLPV1_41",
    "open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49",
    "open KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53",
    "open KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59",
]) + "\n"
OLD_COMP = """    have hB :
        standardABCStrongCellularClosure
          (standardTypeABoundaryPrismCellCompletionHom g j c) :=
      MorphismProperty.le_transfiniteCompositions
        (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})) _ hBraw
    have hcomp :=
      (standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u})).comp_mem
        (standardTypeABoundaryPrismCellAPushoutHom g j c)
        (standardTypeABoundaryPrismCellCompletionHom g j c) hA hB"""
NEW_COMP = """    have hcomp :
        standardABCStrongCellularClosure
          (standardTypeABoundaryPrismCellAPushoutHom g j c ≫
            standardTypeABoundaryPrismCellCompletionHom g j c) := by
      change
        MorphismProperty.transfiniteCompositions.{u}
          (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
          (standardTypeABoundaryPrismCellAPushoutHom g j c ≫
            standardTypeABoundaryPrismCellCompletionHom g j c)
      exact
        (MorphismProperty.transfiniteCompositionsOfShape_le_transfiniteCompositions _ _)
          (MorphismProperty.TransfiniteCompositionOfShape.ofOrderIso
            (.ofComp _ _ hAraw hBraw)
            (orderIsoShrink.{u} (Fin 3)).symm).mem"""


def variants(original: str) -> dict[str, str]:
    assert prior.blob(original.encode()) == BASE
    assert original.count(SCOPE_AT) == 1
    names = prior.inventory(original)
    assert len(names) == 26
    scope = original.replace(SCOPE_AT, SCOPE_AT + SCOPE_ADD)
    assert scope.count(OLD_COMP) == 2
    two_step = scope.replace(OLD_COMP, NEW_COMP)
    variants = {
        "namespace-scope-only": scope,
        "namespace-plus-finite-two-step": two_step,
    }
    # The extra hypotheses are exact, read-only, version-bound CodeAI hunks.
    manifest = json.loads(
        pathlib.Path("scripts/kuuos_v172_cause_separated_hunks_v1.json").read_text(encoding="utf-8"))
    assert manifest["schema"] == "kuuos_v172_cause_separated_hunks_v1"
    assert manifest["base_scope_blob"] == CANDIDATES["namespace-scope-only"]
    assert manifest["historical_unchanged"] is True
    assert manifest["public_declarations_preserved"] == 26
    base_lines = scope.split("\n")
    for item in manifest["variants"]:
        assert item["name"] not in variants
        assert item["expected_blob"] == CANDIDATES[item["name"]]
        cursor = 0
        result_lines = []
        for h in item["patches"]:
            start, old, new = h["start"], h["old"], h["new"]
            assert cursor <= start <= len(base_lines)
            assert base_lines[start:start + len(old)] == old
            result_lines.extend(base_lines[cursor:start])
            result_lines.extend(new)
            cursor = start + len(old)
        result_lines.extend(base_lines[cursor:])
        variants[item["name"]] = "\n".join(result_lines)
    # Second cause-separated version: explicit universe sharing, typed pushout witnesses,
    # and a generic dimension-equality isomorphism. No historical-source mutation.
    manifest_v2 = json.loads(
        pathlib.Path("scripts/kuuos_v172_cause_separated_hunks_v2.json").read_text(encoding="utf-8"))
    assert manifest_v2["schema"] == "kuuos_v172_cause_separated_hunks_v2"
    assert manifest_v2["base_scope_blob"] == CANDIDATES["namespace-scope-only"]
    assert manifest_v2["historical_unchanged"] is True
    assert manifest_v2["public_declarations_preserved"] == 26
    for item in manifest_v2["variants"]:
        assert item["name"] not in variants
        assert item["expected_blob"] == CANDIDATES[item["name"]]
        cursor = 0
        result_lines = []
        for h in item["patches"]:
            start, old, new = h["start"], h["old"], h["new"]
            assert cursor <= start <= len(base_lines)
            assert base_lines[start:start + len(old)] == old
            result_lines.extend(base_lines[cursor:start])
            result_lines.extend(new)
            cursor = start + len(old)
        result_lines.extend(base_lines[cursor:])
        variants[item["name"]] = "\n".join(result_lines)
    assert set(variants) == set(CANDIDATES)
    for name, source in variants.items():
        assert prior.blob(source.encode()) == CANDIDATES[name], name
        assert prior.inventory(source) == names, ("public declarations changed", name)
    return variants


def main() -> None:
    root = pathlib.Path.cwd()
    prior.pins(root)
    assert prior.blob((root / "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismScaledRankFiltrationV1_71.lean").read_bytes()) == "f7d1e61cefa8e448fb3a8eb6c825a66e9c88db65"
    assert prior.blob((root / "formal/KUOS/DependentOriginationStandardABCLeibnizCellularComparisonV1_59.lean").read_bytes()) == "9388efc5b44873409133e30fbe7b30fbabdf6b52"
    original = (root / REL).read_bytes()
    assert prior.blob(original) == BASE
    target = root / REL
    out = pathlib.Path("/tmp/kuuos-v172-codeai-probe")
    out.mkdir(parents=True, exist_ok=True)
    source_map = {"negative-baseline": original.decode("utf-8"), **variants(original.decode("utf-8"))}
    results = []
    try:
        for name, source in source_map.items():
            from scripts.kuuos_lean_mcp_repair_loop_v1 import mask_lean_comments, FORBIDDEN_NEW
            assert not FORBIDDEN_NEW.findall(mask_lean_comments(source)), name
            target.write_text(source, encoding="utf-8")
            with tempfile.TemporaryDirectory(prefix="v172-lean-") as tmp:
                cmd = ["lake", "env", "lean", "-DwarningAsError=true",
                    "-Dweak.sorryAsError=true", "-o", str(pathlib.Path(tmp) / "candidate.olean"), REL]
                p = subprocess.run(cmd, cwd=root, text=True, capture_output=True, timeout=1200)
                log = p.stdout + "\n" + p.stderr
                (out / (name + ".log")).write_text(log, encoding="utf-8")
                error_lines = re.findall(r"(?m)^.*\berror(?:\([^)]*\))?:.*$", log)
                clean = p.returncode == 0 and (pathlib.Path(tmp) / "candidate.olean").is_file() and not error_lines and "sorryAx" not in log
                result = {
                    "candidate": name, "blob": prior.blob(source.encode()),
                    "sha256": hashlib.sha256(source.encode()).hexdigest(),
                    "source_head": os.environ.get("SOURCE_HEAD", "NO_DATA"),
                    "direct_lean_success": clean, "returncode": p.returncode,
                    "error_count": len(error_lines), "first_errors": error_lines[:30],
                    "real_mcp_certified": False, "independent_axiom_certified": False,
                    "adopted": False,
                }
                results.append(result)
                (out / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))
                print("KUUOS_V172_UNCERTIFIED_PROBE " + json.dumps(result), flush=True)
    finally:
        target.write_bytes(original)
    assert target.read_bytes() == original
    winners = [r for r in results[1:] if r["direct_lean_success"]]
    print("KUUOS_V172_PROBE_FINISHED " + json.dumps({
        "tried": len(results), "direct_green": [r["candidate"] for r in winners],
        "certified": False, "source_unmodified": True,
        "real_mcp_required": True, "independent_26_axiom_required": True,
    }), flush=True)


if __name__ == "__main__":
    main()
