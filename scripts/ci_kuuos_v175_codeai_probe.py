#!/usr/bin/env python3
"""KuuOS v1.75 bounded CodeAI full-source candidate comparison (NOT proof).

Never adopts source: historical originals and fixed dependencies must match.
Probe job success means only the 5-way comparison ran; per-candidate Lean results
are advisory until actual Lean MCP and independent 31-axiom certification.
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
from scripts.kuuos_lean_mcp_repair_loop_v1 import FORBIDDEN_NEW, mask_lean_comments

NS = "KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousBPhaseV1_75"
REL = "formal/" + NS.replace(".", "/") + ".lean"
BASE = "ac0abc7aa8f7c52c45ac0e2ed13d0cae71ada978"
V174 = "db34c44b30cbd6c5bd4aa113e320643aba21577c"
EXPECTED = {
    "baseline": "ac0abc7aa8f7c52c45ac0e2ed13d0cae71ada978",
    "explicit-universe": "e2604f4d4f215b1006b32fbdea826a216ef6289b",
    "class-reducible": "5754d9899f42f342c8bc1a35362b3952f31997a8",
    "raw-cellular-typed": "69f5fe2b78510ef3b7d36fbb7b0c210202a02e62",
    "scaled-pushout-universe": "f73c98a18e055140f75aeea012b168d0f37df2cb",
    "open-v149": "d6b6db23842aafd4a54aae1f3f43a1f3a40a00b5",
    "open-v149-inductive-where": "9eaf7fe74615bbd58ca4484c584b239656aba5f5",
    "inductive-where-only": "e4bd12d79ecbc2f519a177329dcf98437aeebb2e",
    "v175-v2-first-typed-pattern": "5171aa38dc1f9c779ad836d332125eb76e3fd4fa",
    "v175-v2-cofan-descent": "bb4e5d6e2aa4e7ba89b05fa385a039a5e821eb2a",
    "v175-v2-bmap-desc": "217ca069b5a1a6e7310c2ca0f32bcc452c92cd09",
    "v175-v3-typed-source-target": "206162efc208d705a2f074a249a086d70bc2ce7d",
    "v175-v3-typed-first-square": "74681fd75168c505d252da799598462d12e9cd7b",
    "v175-v3-cofan-universe": "b5d360052904bd982290874c007cd928dcea0dfb",
    "v175-v3-bmap-universe": "423f0246d9635433645dcb54f0cf8c3fb19d6ede"
}
OLD_FUNCTION = "(standardTypeABoundaryPrismRankFunction g)"
NEW_FUNCTION = "(standardTypeABoundaryPrismRankFunction.{u} g)"
OLD_RAW = "    standardABCRawCellularStep\n      (standardTypeABoundaryPrismRankAPhaseToSucc g j) := by\n  exact MorphismProperty.pushouts_mk\n    (standardTypeABoundaryPrism_rankB_scaled_isPushout g j)\n    (standardTypeABoundaryPrismRankBSigmaGeneratorHom_mem_coproductsABC g j)"
NEW_RAW = "    standardABCRawCellularStep.{u}\n      (standardTypeABoundaryPrismRankAPhaseToSucc.{u} g j) := by\n  exact MorphismProperty.pushouts_mk\n    (MorphismProperty.coproducts.{u}\n      (standardScaledAnodyneGeneratorsABC :\n        MorphismProperty (ScaledSSet.{u})))\n    (standardTypeABoundaryPrism_rankB_scaled_isPushout g j)\n    (standardTypeABoundaryPrismRankBSigmaGeneratorHom_mem_coproductsABC g j)"
OLD_PUSHOUT = "    IsPushout\n      (standardTypeABoundaryPrismRankBSourceSigmaToAPhase g j)\n      (standardTypeABoundaryPrismRankBSigmaGeneratorHom g j)\n      (standardTypeABoundaryPrismRankAPhaseToSucc g j)\n      (standardTypeABoundaryPrismRankBTargetSigmaToSucc g j) := by"
NEW_PUSHOUT = "    IsPushout.{u, u+1}\n      (standardTypeABoundaryPrismRankBSourceSigmaToAPhase.{u} g j)\n      (standardTypeABoundaryPrismRankBSigmaGeneratorHom.{u} g j)\n      (standardTypeABoundaryPrismRankAPhaseToSucc.{u} g j)\n      (standardTypeABoundaryPrismRankBTargetSigmaToSucc.{u} g j) := by"


def replace_once(source: str, old: str, new: str) -> str:
    assert source.count(old) == 1, ("source mismatch", old, source.count(old))
    return source.replace(old, new, 1)


def candidates(source: str) -> dict[str, str]:
    assert prior.blob(source.encode()) == BASE
    assert source.count(OLD_FUNCTION) == 35
    one = source.replace(OLD_FUNCTION, NEW_FUNCTION)
    two = one
    for name in (
        "standardTypeABoundaryPrismRankBSourceSigmaScaling",
        "standardTypeABoundaryPrismRankBTargetSigmaScaling",
    ):
        two = replace_once(two, "def " + name + "\n", "@[reducible] def " + name + "\n")
    three = replace_once(two, OLD_RAW, NEW_RAW)
    four = replace_once(three, OLD_PUSHOUT, NEW_PUSHOUT)
    result = {
        "baseline": source,
        "explicit-universe": one,
        "class-reducible": two,
        "raw-cellular-typed": three,
        "scaled-pushout-universe": four,
    }
    # Independent structural causes: missing v1.49 namespace and Lean4
    # inductive constructor syntax. Preserve all original 31 declarations.
    five = replace_once(four,
        "open KUOS.DependentOriginationScaledTerminalRLPV1_41\n",
        "open KUOS.DependentOriginationScaledTerminalRLPV1_41\n"
        "open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49\n")
    six = replace_once(five,
        "    (j : ℕ) : Type u\n  | q12\n",
        "    (j : ℕ) : Type u where\n  | q12\n")
    seven = replace_once(four,
        "    (j : ℕ) : Type u\n  | q12\n",
        "    (j : ℕ) : Type u where\n  | q12\n")
    result["open-v149"] = five
    result["open-v149-inductive-where"] = six
    result["inductive-where-only"] = seven
    # Second cause-separated group: reproduce new candidates from the
    # exact earlier near-green source; no original-source modification.
    manifest = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_cause_separated_hunks_v2.json"
    ).read_text(encoding="utf-8"))
    assert manifest["schema"] == "kuuos_v175_codeai_cause_separated_hunks_v2"
    assert manifest["base_candidate_blob"] == EXPECTED["open-v149-inductive-where"]
    assert manifest["original_blob"] == BASE
    assert manifest["historical_unchanged"] is True
    assert manifest["public_declarations_preserved"] == 31
    assert len(manifest["variants"]) == 3
    for item in manifest["variants"]:
        assert item["name"] not in result
        candidate = result["open-v149-inductive-where"]
        for hunk in item["patches"]:
            old, newer = hunk["old"], hunk["new"]
            assert candidate.count(old) == 1, ("stale v1.75", item["name"], hunk["name"])
            candidate = candidate.replace(old, newer, 1)
        assert prior.blob(candidate.encode()) == item["expected_blob"]
        result[item["name"]] = candidate
    # v3: isolate universe inference for source/target type B copies.
    # Use complete historical source-derived v2 candidates as exact bases.
    universe_manifest = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_universe_hunks_v3.json"
    ).read_text(encoding="utf-8"))
    assert universe_manifest["schema"] == "kuuos_v175_codeai_universe_hunks_v3"
    assert universe_manifest["baseline_blob"] == BASE
    assert universe_manifest["historical_unchanged"] is True
    assert universe_manifest["public_declarations_preserved"] == 31
    assert len(universe_manifest["variants"]) == 4
    for base_name, base_blob in universe_manifest["source_blobs"].items():
        assert prior.blob(result[base_name].encode()) == base_blob
    for item in universe_manifest["variants"]:
        assert item["name"] not in result
        candidate = result[item["base"]]
        for patch in item["patches"]:
            if patch["mode"] == "literal":
                assert candidate.count(patch["old"]) == patch["count"] == 1
                candidate = candidate.replace(patch["old"], patch["new"], 1)
            else:
                pattern = r"\b" + re.escape(patch["old"]) + r"\b(?!\.\{)"
                candidate, n = re.subn(pattern, patch["new"], candidate)
                assert n == patch["count"], (item["name"], patch["old"], n)
        assert prior.blob(candidate.encode()) == item["expected_blob"]
        result[item["name"]] = candidate
    assert set(result) == set(EXPECTED)
    # v4: additive and strictly source-bound root-cause comparisons.
    v4 = json.loads(pathlib.Path(
        "scripts/kuuos_v175_codeai_structural_hunks_v4.json"
    ).read_text(encoding="utf-8"))
    assert v4["schema"] == "kuuos_v175_codeai_structural_hunks_v4"
    assert v4["source_base"] == EXPECTED["open-v149-inductive-where"]
    assert v4["original_blob"] == BASE
    assert v4["historical_unchanged"] is True
    assert v4["public_declarations_preserved"] == 31
    assert len(v4["variants"]) == 4
    expected = dict(EXPECTED)
    for variant in v4["variants"]:
        assert variant["name"] not in result
        candidate = result[variant["base"]]
        for patch in variant["patches"]:
            old, new = patch["old"], patch["new"]
            assert patch["count"] >= 1
            assert candidate.count(old) == patch["count"], (variant["name"], patch["name"])
            candidate = candidate.replace(old, new)
        assert prior.blob(candidate.encode()) == variant["expected_blob"]
        result[variant["name"]] = candidate
        expected[variant["name"]] = variant["expected_blob"]
    names = prior.inventory(source)
    assert len(names) == len(set(names)) == 31
    assert "inductive StandardTypeABoundaryPrismRankBCell" in source
    for name, candidate in result.items():
        assert prior.blob(candidate.encode()) == expected[name], name
        assert prior.inventory(candidate) == names, name
        assert "inductive StandardTypeABoundaryPrismRankBCell" in candidate
        assert not FORBIDDEN_NEW.findall(mask_lean_comments(candidate)), name
    return result


def main() -> None:
    root = pathlib.Path.cwd()
    prior.pins(root)
    assert prior.blob((root / "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousAPhaseV1_74.lean").read_bytes()) == V174
    historical = (root / "legacy/v5.291" / REL).read_bytes()
    original = (root / REL).read_bytes()
    assert prior.blob(historical) == BASE
    assert prior.blob(original) == os.environ["CHECKOUT_BLOB"] == BASE
    assert len(os.environ["SOURCE_HEAD"]) == 40
    result = candidates(historical.decode())
    target = root / REL
    out = pathlib.Path("/tmp/kuuos-v175-codeai-probe")
    out.mkdir(parents=True, exist_ok=True)
    records = []
    try:
        for name, source in result.items():
            if os.environ.get("V4_ONLY", "0") == "1" and not name.startswith("v175-v4-"):
                continue
            target.write_text(source, encoding="utf-8")
            with tempfile.TemporaryDirectory(prefix="kuuos-v175-probe-") as directory:
                olean = pathlib.Path(directory) / "candidate.olean"
                cmd = [
                    "lake", "env", "lean", "-DwarningAsError=true",
                    "-Dweak.sorryAsError=true", "-o", str(olean), REL,
                ]
                p = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=1800)
                log = p.stdout + "\n" + p.stderr
                (out / (name + ".log")).write_text(log)
                errors = re.findall(r"(?m)^.*\berror(?:\([^)]*\))?:.*$", log)
                entry = {
                    "name": name,
                    "blob": prior.blob(source.encode()),
                    "sha256": hashlib.sha256(source.encode()).hexdigest(),
                    "head": os.environ["SOURCE_HEAD"],
                    "returncode": p.returncode,
                    "error_count": len(errors),
                    "first_errors": errors[:45],
                    "direct_lean_success": (p.returncode == 0 and olean.is_file()
                        and not errors and "sorryAx" not in log),
                    "real_mcp_certified": False,
                    "independent_axiom_certified": False,
                    "adopted": False,
                }
                records.append(entry)
                (out / "results.json").write_text(json.dumps(records, indent=2))
                print("KUUOS_V175_UNCERTIFIED_PROBE " + json.dumps(entry), flush=True)
    finally:
        target.write_bytes(original)
    assert target.read_bytes() == original
    print("KUUOS_V175_PROBE_FINISHED " + json.dumps({
        "tried": len(records),
        "direct_green": [x["name"] for x in records if x["direct_lean_success"]],
        "source_restored": True,
        "certified": False,
        "git_write_performed": False,
    }), flush=True)


if __name__ == "__main__":
    main()
