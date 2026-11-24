#!/usr/bin/env python3
"""Original-name v1.86 CodeAI-adopted source: exact fixed-pinned Lean and 21 axioms.

The 21-declaration candidate was independently certified at exact GitHub HEAD
d5a2103a1b53c6ef9682bee6c5fd6e32e83c18e8. The reviewed source adoption is namespace-only. Neither
that candidate SUCCESS nor this check authorizes a PR/main merge.
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

MODULE = "KUOS.DependentOriginationGeneratedPresentationCompleteLatticeV1_86"
ADOPTED = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationCompleteLatticeV1_86.lean"
CANDIDATE = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationCompleteLatticeCodeAICandidateV1_86.lean"
HISTORICAL = ROOT / "legacy/v5.291/formal/KUOS/DependentOriginationGeneratedPresentationCompleteLatticeV1_86.lean"
ADOPTED_BLOB = "57e4436f389928864ebd75ef4b6a0a535b8d51c8"
CANDIDATE_BLOB = "0c4efd1ff7e6c0a0735aee2b8b6c939dbffebbc7"
HISTORICAL_BLOB = "15fcc55183142ba4ad1fdf5d3ff402c5a2a0804b"
CERTIFIED_CANDIDATE_HEAD = "d5a2103a1b53c6ef9682bee6c5fd6e32e83c18e8"
CERTIFIED_CANDIDATE_RUN = 44960553362
PARENTS = {
    "DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85": "eff1b6d74800c4d3e1f37a6806ebf88ff8b6cd0e",
    "DependentOriginationGeneratedPresentationOrderReflectionV1_84": "5c1f7e9dc8fbb12bb901f4c67f0aad99543d49b9",
    "DependentOriginationGeneratedPresentationPosetalReflectionV1_83": "3bc1f096876f8c7b799ae48f29419e6686e33c87",
}
PUBLIC = ["orthogonalAnodyneClosure","orthogonalAnodyneClosure_apply","orthogonalAnodyneClosure_isClosed_iff","orthogonalFibrationClosure","orthogonalFibrationClosure_apply","orthogonalFibrationClosure_isClosed_iff","orthogonallySaturatedScaledAnodyneCompleteLattice","orthogonallySaturatedScaledFibrationCompleteLattice","saturatedAnodyne_iInf_val","saturatedAnodyne_iSup_val","saturatedFibration_iInf_val","saturatedFibration_iSup_val","generatedScaledAnodynePresentationCompleteLattice","presentationToSaturatedAnodyne_iSup","presentationToSaturatedAnodyne_iInf","presentationToSaturatedFibration_iSup","presentationToSaturatedFibration_iInf","generatedAnodyneClass_iSup","generatedAnodyneClass_iInf","generatedFibrationClass_iSup","generatedFibrationClass_iInf"]
DECL = re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")

def execute(out: Path) -> dict:
    verify_inputs()
    for module, expected in PARENTS.items():
        f = ROOT / "formal/KUOS" / (module + ".lean")
        if blob(f.read_bytes()) != expected:
            raise AuditFailure("V186_PARENT_BLOB_MISMATCH "+module)
    if blob(HISTORICAL.read_bytes()) != HISTORICAL_BLOB:
        raise AuditFailure("V186_HISTORICAL_BLOB_CHANGED")
    cert = CANDIDATE.read_bytes()
    if blob(cert) != CANDIDATE_BLOB:
        raise AuditFailure("V186_CERTIFIED_CODEAI_CHANGED")
    raw = ADOPTED.read_bytes()
    if blob(raw) != ADOPTED_BLOB:
        raise AuditFailure("V186_ADOPTED_SOURCE_CHANGED")
    predicted = cert.decode("utf8").replace("KUOS.DependentOriginationGeneratedPresentationCompleteLatticeCodeAICandidateV1_86", "KUOS.DependentOriginationGeneratedPresentationCompleteLatticeV1_86")
    actual = raw.decode("utf8")
    if actual != predicted:
        raise AuditFailure("V186_NOT_EXACT_NAMESPACE_ONLY_ADOPTION")
    masked = mask_lean_comments(actual)
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b", masked):
        raise AuditFailure("V186_TRUST_BYPASS")
    declarations = DECL.findall(masked)
    if declarations != PUBLIC or len(PUBLIC) != 21 or len(set(PUBLIC)) != 21:
        raise AuditFailure("V186_PUBLIC_DECLARATION_INVENTORY "+repr(declarations))
    head = os.environ.get("SOURCE_HEAD", "")
    if not re.fullmatch(r"[a-f0-9]{40}", head):
        raise AuditFailure("V186_EXACT_HEAD_NO_DATA")
    out.mkdir(parents=True, exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("V186_RECEIPT_APPEND_ONLY_VIOLATION")
    run_logged(
        ["lake", "-KleanArgs=-DwarningAsError=true",
         "-KleanArgs=-DsorryAsError=true", "build", MODULE],
        out/"strict-build.log", 4800,
    )
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v186-adopted-axioms-") as d:
        f = Path(d)/"all-21.lean"
        f.write_text("import "+MODULE+"\n"+
            "".join("#print axioms "+MODULE+"."+name+"\n" for name in PUBLIC),
            encoding="utf8")
        run_logged(
            ["lake", "env", "lean", "-DwarningAsError=true",
             "-Dweak.sorryAsError=true", str(f)],
            out/"axiom-audit.log", 1800,
        )
    log=(out/"axiom-audit.log").read_text(errors="replace")
    reports={}
    for name in PUBLIC:
        full=MODULE+"."+name
        m=re.search(r"'"+re.escape(full)+r"'\s+depends on axioms:\s*\[([^\]]*)\]",log,re.S)
        if m:
            reports[name]=sorted(a.strip() for a in m.group(1).split(",") if a.strip())
        elif re.search(r"'"+re.escape(full)+r"'\s+does not depend on any axioms",log):
            reports[name]=[]
        else:
            raise AuditFailure("V186_MISSING_AXIOM_REPORT "+full)
    axioms=set(a for arr in reports.values() for a in arr)
    if axioms-STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("V186_NONSTANDARD_AXIOM "+repr(sorted(axioms-STANDARD_AXIOMS)))
    receipt={
      "kind":"KUUOS_V186_PR_ADOPTED_EXACT_SOURCE_21_AXIOM_AUDIT",
      "head":head,"adopted_blob":ADOPTED_BLOB,
      "certified_candidate_blob":CANDIDATE_BLOB,
      "certified_candidate_head":CERTIFIED_CANDIDATE_HEAD,
      "certified_candidate_run":CERTIFIED_CANDIDATE_RUN,
      "historical_blob":HISTORICAL_BLOB,
      "source_sha256":hashlib.sha256(raw).hexdigest(),
      "public_declarations":len(reports),
      "lean_pin":"leanprover/lean4:v4.30.0-rc2",
      "mathlib_pin":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
      "axioms":sorted(axioms),"sorryAx":False,"warnings":0,"errors":0,
      "source_adopted_on_PR":True,"source_adopted_on_main":False,
      "standard_equals_canonical_asserted":False,
      "arbitrary_scaling_forward_RLP_asserted":False,
    }
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("KUUOS_V186_PR_ADOPTED_KERNEL_GREEN "+json.dumps(receipt,ensure_ascii=False),flush=True)
    return receipt

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    try:
        execute(args.out.resolve())
        return 0
    except (AuditFailure,OSError,ValueError) as e:
        print("KUUOS_V186_PR_ADOPTED_HOLD "+json.dumps(
            {"status":"UNAUTHENTICATED","obstruction":str(e),"merged":False}),
            file=sys.stderr,flush=True)
        return 2

if __name__=="__main__":
    sys.exit(main())
