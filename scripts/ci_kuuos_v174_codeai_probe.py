#!/usr/bin/env python3
"""KuuOS v1.74 CodeAI: disposable version-bound pinned Lean candidate comparison.

A probe success only means the harness ran. Read each candidate's return code.
No original or history edits, no additional axioms, no sorry, no Git write.
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

NS = "KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousAPhaseV1_74"
REL = "formal/" + NS.replace(".", "/") + ".lean"
BASE = "f03e1d3aaba3803a77c50e935854ed215c0da0aa"
V173 = "08a532c2793a382a5a59f4aee887d5843704c2fd"
EXPECTED = {
    "baseline": BASE,
    "universe-locked": "61392920daadfe6b5b3ade423f654e20e3a65c77",
    "universe-reducible": "9ddee58c9bbe1cc1a7a824513b954b0de02ae73d",
    "universe-reducible-pushouts-mk": "5aa5103cc5b499edc69660367b63f19f58faba7d",
    "scope-W-ScalingLE": "e9ab4b2e3a880db110ee42342c33d33c554ed142",
    "scope-W-typed-cell": "24feed54afc35c96042e31103fa136453debd3be",
    "scope-W-Sigma-thinness": "a24355da496b7997ec6f76a9ae6e17cf1d7a87c3",
    "scope-W-Sigma-uniqueness": "b3c19bb2c882995e2f433653c4e1f978ac63ddb4",
    "scope-W-Sigma-fac-simp": "ce320a75630fb918bbcf353d17bb7e910fe7bc34",
    "v174-fac-only": "96ae1274393bca816c6c5936c81dcdbca8c76ff6",
    "v174-fac-pushout-universe": "8e6d5c6bd1d026c245995c789ec4233fecfd9b14",
    "v174-fac-pushout-raw-class": "93106a7bbdc0cbceb38477f33b736f4be9d37983",
    "v174-fac-raw-bmap": "90423ddb6094cec1536c3e6eb630fd531506f3ba",
    "v174-fac-raw-bmap-bound": "4b5f9fd06df6237ad001f978e5ff90ac69f9b0fc",
    "v174-fac-raw-bmap-bound-explicit": "80d9d139fad2faf7b9000542317ada775b07dce1",
}
OLD = "(standardTypeABoundaryPrismRankFunction g)"
NEW = "(standardTypeABoundaryPrismRankFunction.{u} g)"

def replace_once(s: str, old: str, new: str) -> str:
    assert s.count(old) == 1, ("unexpected Lean source version", old)
    return s.replace(old, new)

def candidates(historical: str) -> dict[str, str]:
    assert prior.blob(historical.encode()) == BASE
    assert historical.count(OLD) == 38
    one = historical.replace(OLD, NEW)
    two = one
    for name in (
        "standardTypeABoundaryPrismRankAHornSigmaScaling",
        "standardTypeABoundaryPrismRankASimplexSigmaScaling",
        "standardTypeABoundaryPrismRankAPhaseScaling",
    ):
        two = replace_once(two, "def " + name + "\n", "@[reducible] def " + name + "\n")
    three = replace_once(two, """  exact MorphismProperty.pushouts_mk
    (standardTypeABoundaryPrism_rankA_scaled_isPushout g j)
    (standardTypeABoundaryPrismRankASigmaCellHom_mem_coproductsABC g j)""",
        """  exact MorphismProperty.pushouts_mk
    (MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})))
    (standardTypeABoundaryPrism_rankA_scaled_isPushout g j)
    (standardTypeABoundaryPrismRankASigmaCellHom_mem_coproductsABC g j)""")
    result = {
        "baseline": historical, "universe-locked": one,
        "universe-reducible": two, "universe-reducible-pushouts-mk": three,
    }
    manifest = json.loads(
        pathlib.Path("scripts/kuuos_v174_codeai_cause_separated_hunks_v1.json").read_text(encoding="utf-8"))
    assert manifest["schema"] == "kuuos_v174_codeai_cause_separated_hunks_v1"
    assert manifest["base_candidate_blob"] == EXPECTED["universe-reducible-pushouts-mk"]
    assert manifest["public_declarations_preserved"] == 26
    assert manifest["historical_unchanged"] is True
    assert len(manifest["variants"]) == 5
    base_lines = three.split("\n")
    for item in manifest["variants"]:
        assert item["name"] not in result
        at = 0
        combined = []
        for h in item["patches"]:
            start, removed, added = h["start"], h["old"], h["new"]
            assert at <= start <= len(base_lines)
            assert base_lines[start:start + len(removed)] == removed
            combined.extend(base_lines[at:start])
            combined.extend(added)
            at = start + len(removed)
        combined.extend(base_lines[at:])
        result[item["name"]] = "\n".join(combined)
        assert prior.blob(result[item["name"]].encode()) == item["expected_blob"]
    assert set(result) == set(EXPECTED)
    # Second cause-separated CodeAI group: exact fixed Sigma.ι_desc factors,
    # rank-A pushout universe, explicit raw class and scaled target transport.
    manifest_v2 = json.loads(
        pathlib.Path("scripts/kuuos_v174_codeai_cause_separated_hunks_v2.json").read_text(encoding="utf-8"))
    assert manifest_v2["schema"] == "kuuos_v174_codeai_cause_separated_hunks_v2"
    assert manifest_v2["base_candidate_blob"] == EXPECTED["scope-W-Sigma-uniqueness"]
    assert manifest_v2["public_declarations_preserved"] == 26
    assert manifest_v2["historical_unchanged"] is True
    assert len(manifest_v2["variants"]) == 6
    base_v2_lines = result["scope-W-Sigma-uniqueness"].split("\n")
    for item in manifest_v2["variants"]:
        assert item["name"] not in result
        at = 0
        combined = []
        for h in item["patches"]:
            start, removed, added = h["start"], h["old"], h["new"]
            assert at <= start <= len(base_v2_lines)
            assert base_v2_lines[start:start + len(removed)] == removed
            combined.extend(base_v2_lines[at:start])
            combined.extend(added)
            at = start + len(removed)
        combined.extend(base_v2_lines[at:])
        result[item["name"]] = "\n".join(combined)
        assert prior.blob(result[item["name"]].encode()) == item["expected_blob"]
    assert set(result) == set(EXPECTED)
    names = prior.inventory(historical)
    assert len(names) == 26 and len(set(names)) == 26
    for name, text in result.items():
        assert prior.blob(text.encode()) == EXPECTED[name]
        assert prior.inventory(text) == names
        assert not FORBIDDEN_NEW.findall(mask_lean_comments(text)), name
    return result

def main() -> None:
    root = pathlib.Path.cwd()
    prior.pins(root)
    assert prior.blob((root / "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseScaledPushoutV1_73.lean").read_bytes()) == V173
    historical = (root / "legacy/v5.291" / REL).read_bytes()
    assert prior.blob(historical) == BASE
    original = (root / REL).read_bytes()
    assert prior.blob(original) == os.environ["CHECKOUT_BLOB"] == BASE
    assert len(os.environ["SOURCE_HEAD"]) == 40
    variants = candidates(historical.decode("utf-8"))
    out = pathlib.Path("/tmp/kuuos-v174-codeai-probe")
    out.mkdir(parents=True, exist_ok=True)
    target = root / REL
    summary = []
    try:
        for name, contents in variants.items():
            target.write_text(contents, encoding="utf-8")
            with tempfile.TemporaryDirectory(prefix="kuuos-v174-test-") as td:
                compiled = pathlib.Path(td) / "candidate.olean"
                cmd = ["lake", "env", "lean", "-DwarningAsError=true",
                       "-Dweak.sorryAsError=true", "-o", str(compiled), REL]
                result = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=1200)
                log = result.stdout + "\n" + result.stderr
                (out / (name + ".log")).write_text(log, encoding="utf-8")
                errors = re.findall(r"(?m)^.*\berror(?:\([^)]*\))?:.*$", log)
                record = {
                    "candidate": name, "blob": prior.blob(contents.encode()),
                    "sha256": hashlib.sha256(contents.encode()).hexdigest(),
                    "source_head": os.environ["SOURCE_HEAD"],
                    "returncode": result.returncode, "error_count": len(errors),
                    "first_errors": errors[:35],
                    "direct_lean_success": result.returncode == 0 and compiled.is_file()
                        and not errors and "sorryAx" not in log,
                    "real_mcp_certified": False, "independent_axiom_certified": False,
                    "adopted": False,
                }
                summary.append(record)
                (out / "results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
                print("KUUOS_V174_UNCERTIFIED_PROBE " + json.dumps(record), flush=True)
    finally:
        target.write_bytes(original)
    assert target.read_bytes() == original
    print("KUUOS_V174_PROBE_FINISHED " + json.dumps({
        "tried": len(summary), "direct_green":
            [r["candidate"] for r in summary if r["direct_lean_success"]],
        "source_restored": True, "certified": False, "git_write_performed": False,
    }), flush=True)

if __name__ == "__main__":
    main()
