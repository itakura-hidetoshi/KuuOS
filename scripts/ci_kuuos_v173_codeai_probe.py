#!/usr/bin/env python3
"""v1.73 CodeAI version-bound candidate probes, isolated from exact adopted v1.72.

This is a disposable pinned Lean *probe*. A green result grants no proof authority.
Never change the historical file, another PR, a canonical branch, or any axiom.
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

REL = "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseScaledPushoutV1_73.lean"
NS = "KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseScaledPushoutV1_73"
BASE = "29c6caed55abb5ed3ae35d5ed5f457d1ce1731aa"
V172 = "79fd2591bf03e8b2dd2a49848a009699235eaef0"
UNIVERSE_LOCK = "a71c8c3cb21dd34cc1985fa2cbc5cac66cfbb3f4"
OLD = "(standardTypeABoundaryPrismRankFunction g)"
NEW = "(standardTypeABoundaryPrismRankFunction.{u} g)"

def candidates(historical: str) -> dict[str, str]:
    assert prior.blob(historical.encode()) == BASE
    assert historical.count(OLD) == 23
    locked = historical.replace(OLD, NEW)
    assert prior.blob(locked.encode()) == UNIVERSE_LOCK
    names = prior.inventory(historical)
    assert len(names) == 21 and len(set(names)) == 21
    assert prior.inventory(locked) == names
    return {"original-baseline": historical, "rank-function-universe-locked": locked}

def main() -> None:
    root = pathlib.Path.cwd()
    prior.pins(root)
    assert prior.blob((root / "formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72.lean").read_bytes()) == V172
    current = (root / REL).read_bytes()
    historical = (root / "legacy/v5.291" / REL).read_bytes()
    assert prior.blob(historical) == BASE
    results = candidates(historical.decode("utf-8"))
    assert current in (historical, results["rank-function-universe-locked"].encode())
    assert os.environ["CHECKOUT_BLOB"] == prior.blob(current)
    assert len(os.environ["SOURCE_HEAD"]) == 40
    out = pathlib.Path("/tmp/kuuos-v173-codeai-probe")
    out.mkdir(parents=True, exist_ok=True)
    target = root / REL
    summary = []
    try:
        for name, text in results.items():
            assert not FORBIDDEN_NEW.findall(mask_lean_comments(text)), name
            target.write_text(text, encoding="utf-8")
            with tempfile.TemporaryDirectory(prefix="v173-lean-") as td:
                olean = pathlib.Path(td) / "candidate.olean"
                command = ["lake", "env", "lean", "-DwarningAsError=true",
                           "-Dweak.sorryAsError=true", "-o", str(olean), REL]
                p = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=1200)
                log = p.stdout + "\n" + p.stderr
                (out / (name + ".log")).write_text(log, encoding="utf-8")
                errors = re.findall(r"(?m)^.*\berror(?:\([^)]*\))?:.*$", log)
                clean = p.returncode == 0 and olean.is_file() and not errors and "sorryAx" not in log
                record = {
                    "candidate": name, "blob": prior.blob(text.encode()),
                    "sha256": hashlib.sha256(text.encode()).hexdigest(),
                    "source_head": os.environ["SOURCE_HEAD"], "errors": len(errors),
                    "first_errors": errors[:35], "returncode": p.returncode,
                    "direct_lean_success": clean, "real_mcp_certified": False,
                    "independent_axiom_certified": False, "adopted": current == text.encode(),
                }
                summary.append(record)
                (out / "results.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
                print("KUUOS_V173_UNCERTIFIED_PROBE " + json.dumps(record), flush=True)
    finally:
        target.write_bytes(current)
    assert target.read_bytes() == current
    print("KUUOS_V173_PROBE_FINISHED " + json.dumps({
        "tried": len(summary),
        "direct_green": [r["candidate"] for r in summary if r["direct_lean_success"]],
        "source_restored": True, "certified": False, "main_modified": False,
    }), flush=True)

if __name__ == "__main__":
    main()
