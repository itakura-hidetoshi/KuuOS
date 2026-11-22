#!/usr/bin/env python3
"""Source-bound pinned Lean audit of v1.106 concrete B²N -> v1.87 gap obstruction.

Conditional universe-polymorphic identities and the specific universe-zero
non-closure are kept separate. No source replacement or PR adoption.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from scripts.ci_kuuos_v176_exact_source_audit_v1 import (
    AuditFailure, ROOT, STANDARD_AXIOMS, blob, run_logged, verify_inputs,
)
from scripts.kuuos_lean_mcp_repair_loop_v1 import mask_lean_comments

MODULE = "KUOS.DependentOriginationStandardCanonicalPresentationGapConcreteObstructionV1_87"
TARGET = ROOT / "formal/KUOS/DependentOriginationStandardCanonicalPresentationGapConcreteObstructionV1_87.lean"
TARGET_BLOB = "83b68916b2a1f7bf6b35d039c226125143555695"
PARENTS = {
    "DependentOriginationStandardCanonicalPresentationGapV1_87": "9718e8dcb1e366774374ddb3d084c5a80391d7e0",
    "DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106": "6e06ac88c2b1cdadcb0d0f7496281892a3549c64",
}
PUBLIC = [
    "gap_not_closed_universe_zero",
    "interval_contains_distinct_points_universe_zero",
    "no_positive_forward_residual_certificate_universe_zero",
]

def execute(out: Path) -> dict:
    verify_inputs()
    for name, expected in PARENTS.items():
        data = (ROOT / "formal/KUOS" / (name + ".lean")).read_bytes()
        if blob(data) != expected:
            raise AuditFailure("V187_CONCRETE_PARENT_CHANGED " + name)
    raw = TARGET.read_bytes()
    if blob(raw) != TARGET_BLOB:
        raise AuditFailure("V187_CONCRETE_CANDIDATE_BLOB_MISMATCH")
    masked = mask_lean_comments(raw.decode("utf8"))
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom|unsafe|native_decide)\b", masked):
        raise AuditFailure("V187_CONCRETE_TRUST_BYPASS")
    decl = re.findall(r"(?m)^theorem\s+([^\s(:]+)", masked)
    if decl != PUBLIC:
        raise AuditFailure("V187_CONCRETE_3_DECLARATIONS_DIFFER " + repr(decl))
    head = os.getenv("SOURCE_HEAD","")
    if not re.fullmatch(r"[a-f0-9]{40}",head):
        raise AuditFailure("V187_CONCRETE_HEAD_NO_DATA")
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        raise AuditFailure("V187_CONCRETE_APPEND_ONLY_RECEIPT_EXISTS")
    run_logged(["lake","-KleanArgs=-DwarningAsError=true",
                "-KleanArgs=-DsorryAsError=true","build",MODULE],
               out/"strict-build.log",4800)
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v187-concrete-") as t:
        f=Path(t)/"axioms.lean"
        f.write_text("import "+MODULE+"\n"+
          "".join("#print axioms "+MODULE+"."+name+"\n" for name in PUBLIC))
        run_logged(["lake","env","lean","-DwarningAsError=true",
                    "-Dweak.sorryAsError=true",str(f)],out/"axiom-audit.log",1800)
    log=(out/"axiom-audit.log").read_text(errors="replace")
    reports={}
    for name in PUBLIC:
        full=MODULE+"."+name
        m=re.search(r"'"+re.escape(full)+r"'\s+depends on axioms:\s*\[([^\]]*)\]",log,re.S)
        if m:
            reports[name]=sorted(s.strip() for s in m.group(1).split(",") if s.strip())
        elif re.search(r"'"+re.escape(full)+r"'\s+does not depend on any axioms",log):
            reports[name]=[]
        else:
            raise AuditFailure("V187_CONCRETE_AXIOM_NO_DATA "+name)
    used={x for items in reports.values() for x in items}
    if used-STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("V187_CONCRETE_NONSTANDARD_AXIOMS "+repr(sorted(used-STANDARD_AXIOMS)))
    receipt={
      "kind":"KUUOS_V187_B2N_UNIVERSE_ZERO_GAP_OBSTRUCTION_3_AXIOMS",
      "source_head":head,"candidate_blob":TARGET_BLOB,
      "source_sha256":hashlib.sha256(raw).hexdigest(),
      "parent_blobs":PARENTS,"public_declarations":len(reports),
      "axioms":sorted(used),"sorryAx":False,"warnings":0,"errors":0,
      "lean":"v4.30.0-rc2","mathlib":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
      "universe_zero_only":True,"all_universes_nonclosure":False,
      "global_fibrancy_proved":False,"merge_authorized":False,
    }
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("KUUOS_V187_B2N_UNIVERSE_ZERO_GAP_NONCLOSURE_GREEN "+
          json.dumps(receipt,ensure_ascii=False),flush=True)
    return receipt

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    opt=ap.parse_args()
    try:
        execute(opt.out.resolve())
        return 0
    except (AuditFailure, OSError, ValueError) as exc:
        print("KUUOS_V187_CONCRETE_GAP_HOLD "+str(exc),file=sys.stderr,flush=True)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
