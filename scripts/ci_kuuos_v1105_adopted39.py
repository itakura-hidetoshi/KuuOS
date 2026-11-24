#!/usr/bin/env python3
"""PR #3555 v1.105 adopted exact-source Lean 39-axiom audit.

Run only on the current PR branch HEAD. Compare the adopted active source with
the exact separately certified candidate and original archived source, exercise
the historical Public Proof Roots map, and independently inspect 39 axioms.
This does not prove the subsequent type-(C) pushout descent or global RLP.
"""
from __future__ import annotations
import ast
import json
import os
from pathlib import Path
import sys

from scripts import kuuos_sandbox_lean_cycle_v1 as cycle

ROOT=Path(__file__).resolve().parents[1]
BRANCH="fix/kuuos-v127-v129-ulift-20261115"
V105=ROOT/"formal/KUOS/DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105.lean"
ARCHIVE=ROOT/"legacy/v5.291/formal/KUOS/DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105.lean"
V104=ROOT/"formal/KUOS/DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104.lean"
GUARD=ROOT/"tests/test_public_root_restoration.py"
STAGING=ROOT/"formal/KUOS/.v1105-adopted-independent39"
OUT=Path("/tmp/kuuos-v1105-adopted-independent39")
NAMESPACE="KUOS.DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105"
CERTIFIED_BLOB="725b4d73037655576d495e32a6e202cd1affaf15"
ORIGINAL_BLOB="fb4d15a3467df69b8d2ba14276c2f4da6a1670d5"
V104_BLOB="5c911aaeb9a21baff57f6af8c8655309af47d027"
STANDARD={"propext","Classical.choice","Quot.sound"}

def check(cond, why):
    if not cond:
        raise RuntimeError("V1105_ADOPTED_HOLD:"+why)

def sha(path):
    check(path.is_file() and not path.is_symlink(),"NOT_REGULAR:"+str(path))
    return cycle.git_blob(path.read_bytes())

def mapping():
    tree=ast.parse(GUARD.read_text())
    vals=[st.value for st in tree.body
          if isinstance(st,ast.Assign) and
          len(st.targets)==1 and isinstance(st.targets[0],ast.Name) and
          st.targets[0].id=="PR3555_V1105_TYPE_C_OUTER_COCYCLE_REVIEWED_BLOB"]
    check(len(vals)==1,"PUBLIC_ROOT_MAP_EXACTLY_ONCE")
    return ast.literal_eval(vals[0])

def public_declarations(src):
    clean=cycle.without_comments_strings(src)
    found=list(cycle.DECL.finditer(clean))
    decls=[]
    seen=set()
    for m in found:
        if m.group(1)=="private":
            continue
        n=m.group(3)
        check(n not in seen,"DUPLICATE_PUBLIC_NAME:"+n)
        seen.add(n)
        decls.append(n)
    return decls

def preflight():
    check(os.environ.get("GITHUB_ACTIONS")=="true" and
          os.environ.get("GITHUB_REF_NAME")==BRANCH,
          "NOT_CURRENT_PR_BRANCH_RUNNER")
    check(sha(V105)==CERTIFIED_BLOB,"FORMAL_V105_SOURCE_NOT_CERTIFIED")
    check(sha(ARCHIVE)==ORIGINAL_BLOB,"HISTORICAL_V105_SOURCE_MUTATED")
    check(sha(V104)==V104_BLOB,"CERTIFIED_V104_DEPENDENCY_MUTATED")
    check(mapping()=={
        "KUOS/DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105.lean":CERTIFIED_BLOB
    },"PUBLIC_ROOT_CERTIFICATE_MAP_MISMATCH")
    code=V105.read_text()
    orig=ARCHIVE.read_text()
    check(cycle.imports(code)==cycle.imports(orig)==[
        "KUOS.DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104"],
        "IMPORT_CONTRACT_CHANGED")
    check(not cycle.TRUST_BYPASS.search(cycle.without_comments_strings(code)),
          "TRUST_BYPASS_IN_ADOPTED_SOURCE")
    names=public_declarations(code)
    check(len(names)==39 and
          names==public_declarations(orig) and
          names[-1]=="natDoubleDelooping_hasAllStandardTypeCSourceCocycleCompletions",
          "DECLARATIONS_NOT_EXACT_OR_39")
    check(cycle.require_pins(ROOT)=={
        "lean_toolchain":"leanprover/lean4:v4.30.0-rc2",
        "mathlib_sha":"5450b53e5ddc75d46418fabb605edbf36bd0beb6"},
        "LEAN_MATHLIB_PIN_CHANGED")
    check(not OUT.exists() and not STAGING.exists(),
          "APPEND_ONLY_AUDIT_ALREADY_EXISTS")
    OUT.mkdir()
    STAGING.mkdir(parents=True)
    (STAGING/"AxiomAudit.lean").write_text(
        code+"\n"+"\n".join("#print axioms "+NAMESPACE+"."+name for name in names)+"\n")
    prepared={
        "schema":"kuuos-v1105-adopted39-source-exact-v1",
        "current_pr_head":os.environ.get("GITHUB_SHA"),
        "candidate_blob":CERTIFIED_BLOB,
        "legacy_original_blob":ORIGINAL_BLOB,
        "v104_import_blob":V104_BLOB,
        "names":names,
        "independent_adopted_certified":False,
        "source_integrity":True,
        "historical_snapshot_unchanged":True,
        "merged":False
    }
    (OUT/"prepared.json").write_text(json.dumps(prepared,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V1105_ADOPTED_EXACT_SOURCE_PREPARED",json.dumps({
        "head":prepared["current_pr_head"],
        "candidate":CERTIFIED_BLOB,
        "public_declarations":len(names)
    },sort_keys=True),flush=True)

def complete():
    check(OUT.is_dir() and (OUT/"prepared.json").is_file() and
          (OUT/"axioms.log").is_file(),"ADOPTED_LEAN_RECEIPTS_NOT_READY")
    prep=json.loads((OUT/"prepared.json").read_text())
    check(prep["current_pr_head"]==os.environ.get("GITHUB_SHA"),
          "EXACT_HEAD_CHANGED")
    check(sha(V105)==CERTIFIED_BLOB and
          sha(ARCHIVE)==ORIGINAL_BLOB and
          sha(V104)==V104_BLOB,"SOURCE_CHANGED_DURING_AUDIT")
    axioms=cycle.audit_axioms((OUT/"axioms.log").read_text(),
                              prep["names"],NAMESPACE)
    check(axioms["checked"]==39 and
          axioms["sorryAx"] is False and
          axioms["nonstandard"]==[] and
          not set(axioms["allowed"])-STANDARD,
          "ADOPTED_39_AXIOMS_NOT_CERTIFIED")
    receipt={
        "schema":"kuuos-v1105-adopted39-source-exact-v1",
        "source_head":prep["current_pr_head"],
        "formal_blob":CERTIFIED_BLOB,
        "original_archive_untouched":True,
        "public_roots_registered":True,
        "kernel_compiled":True,
        "axioms":axioms,
        "sorryAx":False,"warnings":0,"errors":0,
        "independent_adopted_success":True,
        "pr_governance_success":None,
        "pr_merged":False,
        "scope":"v1.105 outer horn cocycle completion only; pushout descent unproved"
    }
    (OUT/"receipt.json").write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
    print("KUUOS_V1105_ADOPTED_39_AXIOMS_GREEN",
          json.dumps({"head":prep["current_pr_head"],
                      "blob":CERTIFIED_BLOB,"axioms":axioms},sort_keys=True),flush=True)

if __name__=="__main__":
    try:
        check(len(sys.argv)==2 and sys.argv[1] in ("preflight","complete"),
              "EXPECTED_PREFLIGHT_OR_COMPLETE")
        (preflight if sys.argv[1]=="preflight" else complete)()
    except Exception as e:
        OUT.mkdir(exist_ok=True)
        (OUT/"obstruction.txt").write_text(type(e).__name__+": "+str(e)+"\n")
        print("KUUOS_V1105_ADOPTED_HOLD",type(e).__name__,str(e),file=sys.stderr)
        raise SystemExit(2)
