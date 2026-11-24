#!/usr/bin/env python3
"""Source-bound v1.76 RankFunctor index proof comparison. NOT certification.

Reconstructs the previously tested bit-step-rfl-lemmas candidate from frozen
legacy bytes and three existing source-bound manifests. Only temporary copies
of the still-unmodified v1.76 source are compiled. Original is restored.
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

ROOT = pathlib.Path(".").resolve()
REL = "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76.lean"
MANIFEST = "scripts/kuuos_v176_codeai_rank_index_v4.json"
OUT = pathlib.Path("/tmp/kuuos-v176-codeai-index-v4")

MAP_OLD = """  map {j k} f :=
    standardTypeABoundaryPrismRankStageHom g
      ((standardTypeABoundaryPrismRankFunction g).filtration_monotone
        (leOfHom f))"""
MAP_DIRECT = """  map {j k} f :=
    standardTypeABoundaryPrismRankStageHom g (leOfHom f)"""
MAP_EXPLICIT = """  map {j k} f :=
    standardTypeABoundaryPrismRankStageHom.{u} g (leOfHom f)"""


def apply_source_patches(source: str, patches: list[dict]) -> str:
    for p in patches:
        assert source.count(p["old"]) == p["count"], p["name"]
        source = source.replace(p["old"], p["new"])
    return source


def reconstruct(original: str) -> str:
    manifests = [
        json.loads((ROOT / "scripts/kuuos_v176_codeai_namespace_probe_v1.json").read_text()),
        json.loads((ROOT / "scripts/kuuos_v176_codeai_monotonicity_universe_v2.json").read_text()),
        json.loads((ROOT / "scripts/kuuos_v176_codeai_bit_recursion_v3.json").read_text()),
    ]
    stages = [
        ("imports", None),
        ("v176-v2-monotone-cylinder-u-thin", "imports"),
        ("bit-step-rfl-lemmas", "v176-v2-monotone-cylinder-u-thin"),
    ]
    s = original
    for manifest, (name, base) in zip(manifests, stages, strict=True):
        entry = next(v for v in manifest["variants"] if v["name"] == name)
        if base is not None:
            assert entry["base"] == base
        s = apply_source_patches(s, entry["patches"])
        assert prior.blob(s.encode("utf-8")) == entry["expected_blob"], name
    assert prior.blob(s.encode("utf-8")) == "6bc2b31ccc842af8253763f9e2c6d0888f2f9167"
    return s


def turn_bit_refine_into_cases(s: str) -> str:
    """Replace incorrect refine-with-uninferred-motive by cases in source scope."""
    head = "  refine Nat.bitCasesOn n ?_\n  intro b j\n  cases b with\n"
    tail = "\n@[simp]\ntheorem standardTypeABoundaryPrismAlternatingStep_bit_false"
    assert s.count(head) == 1 and s.count(tail) == 1
    begin = s.index(head)
    end = s.index(tail, begin)
    branches = s[begin + len(head):end]
    branches = "".join(("    " + line) if line.strip() else line
                       for line in branches.splitlines(keepends=True))
    return (s[:begin] +
            "  cases n using Nat.bitCasesOn with\n  | bit b j =>\n      cases b with\n" +
            branches + s[end:])


def candidate_for(base: str, operations: list[str]) -> str:
    s = base
    for operation in operations:
        if operation in ("map-index", "map-index-explicit"):
            assert s.count(MAP_OLD) == 1
            s = s.replace(MAP_OLD, MAP_DIRECT if operation == "map-index" else MAP_EXPLICIT)
        elif operation == "bit-cases":
            s = turn_bit_refine_into_cases(s)
        else:
            raise AssertionError(("unrecognized operation", operation))
    return s


def main() -> None:
    os.chdir(ROOT)
    prior.pins(ROOT)
    m = json.loads((ROOT / MANIFEST).read_text())
    assert m["schema"] == "kuuos_v176_codeai_rank_index_v4"
    assert m["all_candidates_uncertified"] is True
    assert m["original_blob"] == "c7fd4eb959d05a2eeb430ea39a12d04ed4030ee9"
    assert m["base_blob"] == "6bc2b31ccc842af8253763f9e2c6d0888f2f9167"
    assert m["dependency_blob"] == "e25e593ee859bbf66a26e8e83ee8d1a17d22659b"
    assert len(os.environ["SOURCE_HEAD"]) == 40
    target = ROOT / REL
    raw_bytes = target.read_bytes()
    historic = (ROOT / "legacy/v5.291" / REL).read_bytes()
    assert raw_bytes == historic, "v1.76 original changed: do not probe"
    assert prior.blob(raw_bytes) == m["original_blob"] == os.environ["SOURCE_BLOB"]
    dep = ROOT / "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousBPhaseV1_75.lean"
    assert prior.blob(dep.read_bytes()) == m["dependency_blob"]
    raw = raw_bytes.decode("utf-8")
    baseline = reconstruct(raw)
    inventory = prior.inventory(raw)
    assert len(inventory) >= 10 and len(set(inventory)) == len(inventory)
    assert prior.inventory(baseline) == inventory
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    try:
        for variant in m["variants"]:
            name = variant["name"]
            candidate = candidate_for(baseline, variant["operations"])
            assert prior.inventory(candidate) == inventory
            assert not FORBIDDEN_NEW.findall(mask_lean_comments(candidate)), name
            blob = prior.blob(candidate.encode("utf-8"))
            target.write_text(candidate, encoding="utf-8")
            try:
                with tempfile.TemporaryDirectory(prefix="kuuos-v176-v4-lean-") as td:
                    olean = pathlib.Path(td) / "test.olean"
                    proc = subprocess.run(
                        ["lake", "env", "lean", "-DwarningAsError=true",
                         "-Dweak.sorryAsError=true", "-Dpp.universes=true",
                         "-Dpp.explicit=true", "-Dpp.coercions.types=true",
                         "-o", str(olean), REL],
                        cwd=ROOT, capture_output=True, text=True, timeout=1800,
                    )
                    log = proc.stdout + "\n" + proc.stderr
                    errors = re.findall(r"(?m)^.*\berror(?:\([^)]*\))?:.*$", log)
                    green = proc.returncode == 0 and olean.exists() and not errors and "sorryAx" not in log
            finally:
                target.write_bytes(raw_bytes)
            (OUT / (name + ".log")).write_text(log, encoding="utf-8")
            row = {
                "head": os.environ["SOURCE_HEAD"], "source_blob": m["original_blob"],
                "dependency_blob": m["dependency_blob"], "baseline_blob": m["base_blob"],
                "name": name, "operations": variant["operations"],
                "candidate_blob": blob,
                "sha256": hashlib.sha256(candidate.encode()).hexdigest(),
                "returncode": proc.returncode, "diagnostic_count": len(errors),
                "first_errors": errors[:35], "direct_lean_success": green,
                "real_mcp_certified": False, "independent_axioms_certified": False,
                "adopted": False,
            }
            results.append(row)
            (OUT / "results.json").write_text(json.dumps(results, indent=2))
            print("KUUOS_V176_V4_UNCERTIFIED " + json.dumps(row), flush=True)
    finally:
        target.write_bytes(raw_bytes)
    assert target.read_bytes() == historic
    print("KUUOS_V176_V4_COMPARE_FINISHED " + json.dumps({
        "tried": len(results),
        "direct_green": [r["name"] for r in results if r["direct_lean_success"]],
        "source_restored": True,
        "adopted": False,
        "certified": False,
        "git_write_performed": False,
    }), flush=True)


if __name__ == "__main__":
    main()
