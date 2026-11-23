#!/usr/bin/env python3
"""Fail-closed source-aware sandbox Lean stage receipt, never proof authority.

Does not change theorem source. Distinguishes Lean process rc=0 from an
internal SymbolFrequency panic and requires clean logs before independent CI.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from scripts.codeai_v061_f112_fourteen_full_source_split import (
    ROOT, OUT, SOURCE_BLOB, assert_source as assert_fourteen_source, blob, SOURCE,
)
from scripts.codeai_v061_f112_fourteen_necessity_source_split import (
    SOURCE as NECESSITY_SOURCE, SOURCE_BLOB as NECESSITY_BLOB, assert_original as assert_necessity,
)

PREDECESSOR = ROOT / "artifacts/codeai-v061-f112-thirteen-full-decomposition"
NAMES = (
    ("13D", "thirteen_exact_core"),
    ("13D", "thirteen_exact_five_stage"),
    ("13D", "thirteen_original_import_shim"),
    ("14D", "fourteen_typed_square_comparison"),
    ("14D", "fourteen_thirteen_groupoid"),
    ("14D", "fourteen_necessity_core"),
    ("14D", "fourteen_necessity_middle"),
    ("14D", "fourteen_necessity_tail"),
    ("14D", "fourteen_necessity_original_name_shim"),
    ("14D", "generic_core"),
    ("14D", "fourteen_five_exchange"),
    ("14D", "fourteen_five_leftfirst"),
    ("14D", "fourteen_five_rightfirst"),
    ("14D", "fourteen_five_theorems"),
    ("14D", "original_module_import_shim"),
)
DIAGNOSTICS = re.compile(
    r"(?i)(?:PANIC at |Lean panicked|^\s*(?:error|warning):|sorryAx|"
    r"deterministic\) timeout at )"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--independent", action="store_true")
    args = parser.parse_args()
    source = assert_fourteen_source()
    necessity = assert_necessity()
    assert blob(SOURCE.read_bytes()) == SOURCE_BLOB
    assert blob(NECESSITY_SOURCE.read_bytes()) == NECESSITY_BLOB

    records = []
    faults = []
    for kind, name in NAMES:
        directory = PREDECESSOR if kind == "13D" else OUT
        log_path = directory / (name + ".log")
        exit_path = directory / (name + "-exit.txt")
        if not log_path.is_file() or not exit_path.is_file():
            faults.append({"stage": name, "reason": "NO_DATA: missing stage log/exit"})
            continue
        log_bytes = log_path.read_bytes()
        lines = log_bytes.decode("utf-8", "replace").splitlines()
        bad = [line[:240] for line in lines if DIAGNOSTICS.search(line)]
        code = exit_path.read_text().strip()
        if code != "0" or bad:
            faults.append({"stage": name, "rc": code, "diagnostic_excerpt": bad[:5]})
        records.append({
            "stage": name, "rc": code,
            "lean_log_sha256": hashlib.sha256(log_bytes).hexdigest(),
            "internal_diagnostics": len(bad),
        })

    smoke_exit = OUT / "import-smoke-exit.txt"
    if not smoke_exit.exists() or smoke_exit.read_text().strip() != "0":
        faults.append({"stage": "OriginalImportSmoke", "reason": "NO_DATA or nonzero rc"})
    smoke_log = OUT / "import-smoke.log"
    if not smoke_log.is_file() or DIAGNOSTICS.search(smoke_log.read_text()):
        faults.append({"stage": "OriginalImportSmoke", "reason": "missing log or Lean diagnostic"})
    necessity_manifest = OUT / "necessity/manifest.json"
    if not necessity_manifest.exists():
        faults.append({"stage": "NecessityManifest", "reason": "NO_DATA"})
    else:
        m = json.loads(necessity_manifest.read_text())
        if m["canonical_source_blob"] != NECESSITY_BLOB or m["six_original_declarations_unchanged"] is not True:
            faults.append({"stage": "NecessityManifest", "reason": "source mismatch"})
    five_manifest = OUT / "five-stage/manifest.json"
    if not five_manifest.is_file():
        faults.append({"stage": "FiveStageManifest", "reason": "NO_DATA"})
    else:
        m = json.loads(five_manifest.read_text())
        if (m.get("original_fourteen_source_blob") != SOURCE_BLOB
            or m.get("original_theorem_declarations_and_bodies_unchanged") is not True
            or m.get("original_axiom_audits") != 21):
            faults.append({"stage": "FiveStageManifest", "reason": "source mismatch"})
    if not args.independent:
        mcp_receipt = OUT / "real-lean-mcp-receipt.json"
        if not mcp_receipt.exists():
            faults.append({"stage": "LeanMCP", "reason": "NO_DATA"})
        else:
            rec = json.loads(mcp_receipt.read_text())
            if rec.get("status") != "LOCAL_SPLIT_IMPORT_MCP_SUCCESS_ONLY" or rec.get("partial") is not False:
                faults.append({"stage": "LeanMCP", "reason": "not clean"})
    out = {
        "schema": "kuuos.codeai.v061.f112.14d.sandbox_lean_gate.v1",
        "status": "CLEAN_LOCAL_LEAN_EVIDENCE_ONLY" if not faults else "HOLD_LEAN_DIAGNOSTIC_OBSTRUCTION",
        "original_14d_blob": SOURCE_BLOB,
        "original_necessity_blob": NECESSITY_BLOB,
        "independent_runner": bool(args.independent),
        "source_original_unchanged": True,
        "stage_records": records,
        "faults": faults,
        "independent_ci_claimed": False,
        "original_monolith_certified": False,
        "formal_adoption": False,
        "memory_verified_useful": False,
        "merge_authority": False,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "sandbox-gate.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print("CODEAI_F112_14D_SANDBOX_GATE", json.dumps(out, sort_keys=True), flush=True)
    return 0 if not faults else 1


if __name__ == "__main__":
    raise SystemExit(main())
