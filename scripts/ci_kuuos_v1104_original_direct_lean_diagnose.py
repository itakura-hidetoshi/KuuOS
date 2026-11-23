#!/usr/bin/env python3
"""KuuOS v1.104: immutable source, fixed mathlib, direct Lean diagnosis ONLY.

No independent CI. Return success when an exact-source Lean FAILURE is
captured with actionable real diagnostics; never call that proof certification.
Original proof source and v1.102/v1.103 predecessor files are never mutated.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys

from scripts import kuuos_sandbox_lean_cycle_v1 as cycle

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "research/v1104-codeai-direct-diagnostic-20261123"
V104 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104.lean"
V103 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103.lean"
V102 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102.lean"
V104_SHA = "dc75c6d91c317bc8d350c7c45d4268dce38bf06c"
V103_SHA = "dbec61c9798481709f2deda0028e84b7515f209e"
V102_SHA = "f8b492b210e5525990aa587fa2eb5c8648a5ff19"
OUT = Path("/tmp/kuuos-v1104-original-direct-diagnostic")

def check(ok: bool, msg: str) -> None:
    if not ok:
        raise cycle.Hold(msg)

def main() -> int:
    check(os.environ.get("GITHUB_ACTIONS") == "true", "RUNTIME_OBSTRUCTION")
    check(os.environ.get("GITHUB_REF_NAME") == BRANCH, "SOURCE_OBSTRUCTION: wrong branch")
    pins = cycle.require_pins(ROOT, verify_binaries=True)
    sources = [(V104,V104_SHA),(V103,V103_SHA),(V102,V102_SHA)]
    for path, sha in sources:
        check(path.is_file() and not path.is_symlink() and
              cycle.git_blob(path.read_bytes()) == sha,
              "SOURCE_OBSTRUCTION: pinned file mismatched " + str(path))
    code = V104.read_text()
    names = list(cycle.declarations(code))
    check(len(names) == 21 and names[-1] == "natDoubleDelooping_standardTypeA_rlp",
          "DECLARATION_OBSTRUCTION: expected exactly 21 original public declarations")
    check(cycle.imports(code) ==
          ["KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103"],
          "IMPORT_OBSTRUCTION: original v1.104 import changed")
    check(not OUT.exists(), "APPEND_ONLY_OBSTRUCTION: diagnostic dir reused")
    OUT.mkdir(parents=True)
    result = cycle.run_lean(ROOT, V104, OUT / "direct", seconds=900)
    receipt = {
        "schema": "kuuos-v1104-original-diagnostic-only-v1",
        "status": "NOT_PROOF_CERTIFIED",
        "source_commit_sha": os.environ.get("GITHUB_SHA"),
        "source_blob": V104_SHA,
        "v103_certified_import_blob": V103_SHA,
        "v102_certified_import_blob": V102_SHA,
        "public_declarations": names,
        "pinned_environment": pins,
        "direct_lean": result,
        "independent_ci_started": False,
        "PR_source_mutated": False,
        "merge_authorized": False,
    }
    if result["direct_success"]:
        receipt["status"] = "LOCAL_DIRECT_GREEN_NOT_INDEPENDENT"
        report = OUT / "axioms.lean"
        qualified = ["KUOS.DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104."+name for name in names]
        report.write_text(code + "\n" + "\n".join("#print axioms "+name for name in qualified) + "\n")
        audit = cycle.run_lean(ROOT,report,OUT / "axiom_audit",seconds=900)
        receipt["local_axiom_audit"] = audit
        if audit["direct_success"]:
            receipt["local_axiom_classes"] = cycle.audit_axioms(
                (OUT / "axiom_audit" / "stdout.log").read_text(),
                names,"KUOS.DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104")
    else:
        receipt["status"] = ("SOURCE_DIRECT_LEAN_FAILED_DIAGNOSTIC_ONLY"
                             if result["exit_code"] != 0 and result["error_count"] > 0
                             else "NO_DATA_OR_TIME_LIMIT")
    (OUT / "receipt.json").write_text(json.dumps(
        receipt,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print("KUUOS_V1104_ORIGINAL_DIRECT_LEAN_DIAGNOSTIC_ONLY",json.dumps({
        "status":receipt["status"],"error_count":result["error_count"],
        "exit_code":result["exit_code"],"first_errors":result["first_errors"],
        "independent_ci_started":False,"source_mutated":False},sort_keys=True))
    check(cycle.git_blob(V104.read_bytes()) == V104_SHA and
          cycle.git_blob(V103.read_bytes()) == V103_SHA,
          "SOURCE_OBSTRUCTION: original or certified predecessor changed")
    return 0 if receipt["status"] in {
        "SOURCE_DIRECT_LEAN_FAILED_DIAGNOSTIC_ONLY","LOCAL_DIRECT_GREEN_NOT_INDEPENDENT"
    } else 2

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "obstruction.txt").write_text(
            type(exc).__name__ + ": " + str(exc) + "\n")
        print("KUUOS_V1104_DIAGNOSTIC_HOLD",str(exc),file=sys.stderr)
        raise SystemExit(2)
