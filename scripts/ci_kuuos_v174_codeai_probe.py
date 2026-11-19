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
