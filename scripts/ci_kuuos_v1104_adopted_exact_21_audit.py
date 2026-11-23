#!/usr/bin/env python3
"""Exact-head PR #3555 post-adoption v1.104 Lean 21-axiom audit.

The same exact v1.104 Git blob was independently certified in an isolated
runner before PR adoption. This script recertifies the byte-identical formal
source after the source+Public Proof Roots hash guard commit. It cannot merge.
"""
from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import sys

from scripts import kuuos_sandbox_lean_cycle_v1 as cycle

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "fix/kuuos-v127-v129-ulift-20261115"
V104 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104.lean"
HISTORICAL = ROOT / "legacy/v5.291/formal/KUOS/DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104.lean"
V103 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103.lean"
V102 = ROOT / "formal/KUOS/DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102.lean"
GUARD = ROOT / "tests/test_public_root_restoration.py"
OUT = Path("/tmp/kuuos-v1104-adopted-21-independent")
STAGING = ROOT / "formal/KUOS/.v1104-adopted-21-axiom-audit"
AXIOM_LOG = OUT / "axioms.log"
NAMESPACE = "KUOS.DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104"
CERTIFIED_BLOB = "5c911aaeb9a21baff57f6af8c8655309af47d027"
HISTORICAL_BLOB = "dc75c6d91c317bc8d350c7c45d4268dce38bf06c"
V103_BLOB = "dbec61c9798481709f2deda0028e84b7515f209e"
V102_BLOB = "f8b492b210e5525990aa587fa2eb5c8648a5ff19"
STANDARD = {"propext", "Classical.choice", "Quot.sound"}

def check(cond, why):
    if not cond:
        raise RuntimeError("V1104_ADOPTED_HOLD:" + why)

def sha(path: Path) -> str:
    check(path.is_file() and not path.is_symlink(), "missing regular file: " + str(path))
    return cycle.git_blob(path.read_bytes())

def guard_manifest() -> dict:
    expr = ast.parse(GUARD.read_text(encoding="utf-8"))
    matches = [
        a.value for a in expr.body if isinstance(a, ast.Assign)
        and len(a.targets) == 1 and isinstance(a.targets[0], ast.Name)
        and a.targets[0].id == "PR3555_V1104_TYPE_A_DIM_FOUR_RLP_REVIEWED_BLOB"
    ]
    check(len(matches) == 1, "exactly one v1.104 reviewed source map required")
    return ast.literal_eval(matches[0])

def preflight():
    check(os.environ.get("GITHUB_ACTIONS") == "true" and
          os.environ.get("GITHUB_REF_NAME") == BRANCH,
          "must run on current exact PR branch push")
    check(sha(V104) == CERTIFIED_BLOB, "adopted source Git blob differs from R3-A")
    check(sha(HISTORICAL) == HISTORICAL_BLOB, "historical v1.104 altered")
    check(sha(V103) == V103_BLOB and sha(V102) == V102_BLOB,
          "dependency source differs from certified blobs")
    check(guard_manifest() == {
        "KUOS/DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104.lean":
            CERTIFIED_BLOB
    }, "public root exact blob guard not registered")
    require_import = [
        "KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103"
    ]
    code = V104.read_text()
    check(cycle.imports(code) == require_import, "noncanonical dependency import")
    check(not cycle.TRUST_BYPASS.search(cycle.without_comments_strings(code)),
          "Lean trust bypass expression detected")
    names = list(cycle.declarations(code))
    check(len(names) == 21 and names[-1] == "natDoubleDelooping_standardTypeA_rlp",
          "21 public declarations not preserved")
    check(cycle.require_pins(ROOT) == {
        "lean_toolchain": "leanprover/lean4:v4.30.0-rc2",
        "mathlib_sha": "5450b53e5ddc75d46418fabb605edbf36bd0beb6"
    }, "Lean/mathlib pin mismatch")
    check(not STAGING.exists() and not OUT.exists(), "append-only audit path already used")
    STAGING.mkdir(parents=True)
    OUT.mkdir(parents=True)
    (STAGING / "AxiomAudit.lean").write_text(code + "\n" +
        "\n".join("#print axioms " + NAMESPACE + "." + name for name in names) + "\n")
    (OUT / "preflight.json").write_text(json.dumps({
        "schema": "kuuos-v1104-postadoption-exact-head-v1",
        "head": os.environ.get("GITHUB_SHA"),
        "v104_blob": CERTIFIED_BLOB, "v103_blob": V103_BLOB,
        "historical_v104_blob": HISTORICAL_BLOB,
        "public_names": names, "independent_21_axioms": False,
        "formal_branch": BRANCH
    },sort_keys=True,indent=2) + "\n")
    print("KUUOS_V1104_ADOPTED_SOURCE_AND_PUBLIC_ROOT_EXACT",len(names),CERTIFIED_BLOB,flush=True)

def complete():
    check(OUT.is_dir() and (OUT / "preflight.json").is_file() and AXIOM_LOG.is_file(),
          "audit preflight or full Lean output missing")
    pre = json.loads((OUT / "preflight.json").read_text())
    check(pre["head"] == os.environ.get("GITHUB_SHA"), "head changed during audit")
    check(sha(V104) == CERTIFIED_BLOB and sha(HISTORICAL) == HISTORICAL_BLOB and
          sha(V103) == V103_BLOB and sha(V102) == V102_BLOB,
          "source changed during audit")
    result = cycle.audit_axioms(AXIOM_LOG.read_text(encoding="utf-8"),
                                pre["public_names"], NAMESPACE)
    check(result["checked"] == 21 and result["sorryAx"] is False
          and not set(result["allowed"]) - STANDARD,
          "independent adopted exact-head axiom audit incomplete")
    receipt = {
        "schema": "kuuos-v1104-postadoption-exact-head-v1",
        "head": pre["head"],
        "formal_source_git_blob": CERTIFIED_BLOB,
        "historical_legacy_blob_unchanged": True,
        "public_root_exact_guard": True,
        "strict_source_compiled": True,
        "axioms": result,
        "sorryAx": False,
        "warnings": 0, "errors": 0,
        "scope": "Adopted v1.104 21 public declarations only",
        "independent_adopted_kernel_success": True,
        "PR_governance_success": None,
        "PR_merged": False
    }
    (OUT / "receipt.json").write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V1104_ADOPTED_INDEPENDENT_21_AXIOMS_GREEN",
          json.dumps({"head":pre["head"],"blob":CERTIFIED_BLOB,"axioms":result},
                     sort_keys=True),flush=True)

if __name__ == "__main__":
    try:
        check(len(sys.argv) == 2 and sys.argv[1] in ("preflight","complete"),
              "expected preflight or complete")
        (preflight if sys.argv[1] == "preflight" else complete)()
    except Exception as e:
        OUT.mkdir(exist_ok=True)
        (OUT / "obstruction.txt").write_text(type(e).__name__ + ": " + str(e) + "\n")
        print("KUUOS_V1104_ADOPTED_HOLD",type(e).__name__,str(e),file=sys.stderr)
        raise SystemExit(2)
