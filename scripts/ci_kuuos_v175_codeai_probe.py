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
    "inductive-where-only": "e4bd12d79ecbc2f519a177329dcf98437aeebb2e"
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
    assert set(result) == set(EXPECTED)
    names = prior.inventory(source)
    assert len(names) == len(set(names)) == 31
    assert "inductive StandardTypeABoundaryPrismRankBCell" in source
    for name, candidate in result.items():
        assert prior.blob(candidate.encode()) == EXPECTED[name], name
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
