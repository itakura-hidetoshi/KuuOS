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
    records = []
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        for variant in m["variants"]:
            name = variant["name"]
            candidate = historic.decode("utf-8")
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
