#!/usr/bin/env python3
"""v1.106 source-exact isolated Lean diagnosis, no independent CI.

Read the entire 348-line original source without altering v1.105, the parent PR,
or historical v5.291. Preserve 18 names and actual Lean diagnostics. GREEN here
would be direct Lean only; a later axiom audit and real MCP are still required.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
from scripts import kuuos_sandbox_lean_cycle_v1 as cycle

ROOT=Path(__file__).resolve().parents[1]
BRANCH="research/v1106-codeai-original-direct-20261124"
OUT=Path("/tmp/kuuos-v1106-original-local-diagnostics")
SOURCE=ROOT/"formal/KUOS/DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.lean"
ARCHIVE=ROOT/"legacy/v5.291/formal/KUOS/DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.lean"
DEPENDENCY=ROOT/"formal/KUOS/DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105.lean"
V104=ROOT/"formal/KUOS/DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104.lean"
PINS={
    SOURCE:"6e06ac88c2b1cdadcb0d0f7496281892a3549c64",
    ARCHIVE:"6e06ac88c2b1cdadcb0d0f7496281892a3549c64",
    DEPENDENCY:"725b4d73037655576d495e32a6e202cd1affaf15",
    V104:"5c911aaeb9a21baff57f6af8c8655309af47d027",
}

def check(cond,msg):
    if not cond:
        raise cycle.Hold(msg)

def main():
    check(os.getenv("GITHUB_ACTIONS")=="true" and
          os.getenv("GITHUB_REF_NAME")==BRANCH,"WRONG_LOCAL_RESEARCH_RUN")
    check(not OUT.exists(),"APPEND_ONLY_OUTPUT_PATH_REUSED")
    OUT.mkdir()
    for path,sha in PINS.items():
        check(path.is_file() and not path.is_symlink() and
              cycle.git_blob(path.read_bytes())==sha,
              "FROZEN_SOURCE_BLOB_MISMATCH:"+str(path))
    check(cycle.git_blob((ROOT/"scripts/kuuos_sandbox_lean_cycle_v1.py").read_bytes())==
          "5383253dbe9cda9cab90a410c2fd66ee6b9d6f41",
          "CODEAI_ENGINE_PIN_DRIFT")
    env=cycle.require_pins(ROOT)
    code=SOURCE.read_text()
    stripped=cycle.without_comments_strings(code)
    matches=list(cycle.DECL.finditer(stripped))
    names=[m.group(3) for m in matches if m.group(1)!="private"]
    check(len(names)==18 and
          names[-1]=="standardGeneratedRight_ne_canonicalGeneratedRight",
          "PUBLIC_NAMES_18_CHANGED")
    check(cycle.imports(code)==[
        "KUOS.DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105"],
        "PREDECESSOR_IMPORT_CHANGED")
    check(not cycle.TRUST_BYPASS.search(stripped),"SOURCE_TRUST_BYPASS")
    run=cycle.run_lean(ROOT,SOURCE,OUT/"direct",seconds=850)
    receipt={
        "schema":"kuuos-v1106-original-source-lean-direct-only-v1",
        "source_head":os.environ.get("GITHUB_SHA"),
        "source_git_blob":PINS[SOURCE],
        "v105_git_blob":PINS[DEPENDENCY],
        "v104_git_blob":PINS[V104],
        "public_declarations":names,
        "pin":env,
        "direct_lean":run,
        "status":"LOCAL_DIRECT_GREEN_ONLY" if run["direct_success"]
                 else ("NO_DATA_TIMEOUT" if run["timed_out"] else "LOCAL_DIRECT_RED"),
        "axioms":None,"real_lean_mcp":None,
        "independent_ci_started":False,
        "parent_PR_3555_modified":False,
        "archived_original_mutated":False,
        "authority":"LOCAL_ONLY"
    }
    (OUT/"receipt.json").write_text(json.dumps(receipt,sort_keys=True,indent=2,ensure_ascii=False)+"\n")
    for p,sha in PINS.items():
        check(cycle.git_blob(p.read_bytes())==sha,"SOURCE_CHANGED_DURING_LOCAL")
    print("KUUOS_V1106_ORIGINAL_DIRECT",json.dumps({
        "status":receipt["status"],"errors":run["error_count"],
        "exit_code":run["exit_code"],"public_decls":18,
        "independent_ci":False},sort_keys=True),flush=True)
    return 0 if run["direct_success"] else 1

if __name__=="__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        OUT.mkdir(parents=True,exist_ok=True)
        (OUT/"obstruction.txt").write_text(type(e).__name__+": "+str(e)+"\n")
        print("KUUOS_V1106_ORIGINAL_DIRECT_HOLD",type(e).__name__,str(e),file=sys.stderr)
        raise SystemExit(2)
