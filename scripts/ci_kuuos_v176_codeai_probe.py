#!/usr/bin/env python3
"""Bounded v1.76 CodeAI candidate comparison, NOT proof certification.

Reads the frozen original in legacy/v5.291 and the same-root current source.
Never writes to GitHub; every compilation uses a temporary working copy and
restores exact checked-out bytes. Direct Lean successes need real MCP and
independent axiom audit before source adoption.
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

MANIFEST = "scripts/kuuos_v176_codeai_namespace_probe_v1.json"
OUT = pathlib.Path("/tmp/kuuos-v176-codeai-probe")

def main():
    root = pathlib.Path(".").resolve()
    os.chdir(root)
    prior.pins(root)
    m = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    assert m["schema"] == "kuuos_v176_codeai_namespace_probe_v1"
    rel = m["source_path"]
    target = root / rel
    original = target.read_bytes()
    historic = (root / "legacy/v5.291" / rel).read_bytes()
    assert historic == original, "Original v1.76 source has already changed; do not compare stale patches"
    assert prior.blob(historic) == m["source_blob"] == os.environ["SOURCE_BLOB"]
    assert prior.blob((root / m["required_dependency_path"]).read_bytes()) == m["required_dependency_blob"]
    assert m["legacy_unchanged"] is True
    assert len(os.environ["SOURCE_HEAD"]) == 40
    names = prior.inventory(original.decode("utf-8"))
    assert len(names) >= 10 and len(names) == len(set(names)), names
    # Reconstruct all original source-bounded candidates before comparing v2.
    seed = {}
    for entry in m["variants"]:
        candidate = historic.decode("utf-8")
        for patch in entry["patches"]:
            assert candidate.count(patch["old"]) == patch["count"]
            candidate = candidate.replace(patch["old"], patch["new"])
        assert prior.blob(candidate.encode()) == entry["expected_blob"]
        seed[entry["name"]] = candidate
    v2 = json.loads((root / "scripts/kuuos_v176_codeai_monotonicity_universe_v2.json").read_text(encoding="utf-8"))
    assert v2["schema"] == "kuuos_v176_codeai_monotonicity_universe_v2"
    assert v2["original_blob"] == m["source_blob"]
    assert v2["required_dependency_blob"] == m["required_dependency_blob"]
    assert v2["legacy_unchanged"] is True
    assert len(v2["variants"]) == 4
    seed2 = {}
    for variant in v2["variants"]:
        candidate = seed[variant["base"]]
        for patch in variant["patches"]:
            assert candidate.count(patch["old"]) == patch["count"]
            candidate = candidate.replace(patch["old"], patch["new"])
        assert prior.blob(candidate.encode()) == variant["expected_blob"]
        seed2[variant["name"]] = candidate
    v3 = json.loads((root / "scripts/kuuos_v176_codeai_bit_recursion_v3.json").read_text(encoding="utf-8"))
    assert v3["schema"] == "kuuos_v176_codeai_bit_recursion_v3"
    assert v3["source_blob"] == m["source_blob"]
    assert v3["all_candidates_uncertified"] is True
    assert len(v3["variants"]) == 3
    assert prior.blob(seed2["v176-v2-monotone-cylinder-u-thin"].encode()) == v3["baseline_blob"]
    records = []
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        for variant in v3["variants"]:
            name = variant["name"]
            candidate = seed2[variant["base"]]
            for p in variant["patches"]:
                assert candidate.count(p["old"]) == p["count"], (name, p["name"])
                candidate = candidate.replace(p["old"], p["new"])
            assert prior.inventory(candidate) == names, (name, "public inventory changed")
            assert not FORBIDDEN_NEW.findall(mask_lean_comments(candidate)), (name, "trust bypass")
            blob = prior.blob(candidate.encode("utf-8"))
            assert blob == variant["expected_blob"], (name, blob)
            target.write_text(candidate, encoding="utf-8")
            try:
                with tempfile.TemporaryDirectory(prefix="kuuos-v176-lean-") as td:
                    olean = pathlib.Path(td) / "test.olean"
                    p = subprocess.run(
                        ["lake", "env", "lean", "-DwarningAsError=true",
                         "-Dweak.sorryAsError=true",
                         "-Dpp.universes=true", "-Dpp.explicit=true",
                         "-Dpp.coercions.types=true",
                         "-o", str(olean), rel],
                        cwd=root, capture_output=True, text=True, timeout=1800,
                    )
                    log = p.stdout + "\n" + p.stderr
                    errors = re.findall(r"(?m)^.*\berror(?:\([^)]*\))?:.*$", log)
                    ok = p.returncode == 0 and olean.exists() and not errors and "sorryAx" not in log
            finally:
                target.write_bytes(original)
            (OUT / (name + ".log")).write_text(log, encoding="utf-8")
            entry = {
                "head": os.environ["SOURCE_HEAD"], "name": name,
                "blob": blob, "sha256": hashlib.sha256(candidate.encode()).hexdigest(),
                "returncode": p.returncode, "errors": len(errors),
                "first_errors": errors[:28], "direct_lean_success": ok,
                "real_mcp_certified": False,
                "independent_axioms_certified": False,
                "adopted": False,
            }
            records.append(entry)
            (OUT / "results.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
            print("KUUOS_V176_CODEAI_UNCERTIFIED " + json.dumps(entry), flush=True)
    finally:
        target.write_bytes(original)
    assert target.read_bytes() == original
    print("KUUOS_V176_COMPARE_FINISHED " + json.dumps({
        "tried": len(records),
        "direct_green": [r["name"] for r in records if r["direct_lean_success"]],
        "source_restored": True, "certified": False, "adopted": False,
        "git_write_performed": False,
    }), flush=True)

if __name__ == "__main__":
    main()
