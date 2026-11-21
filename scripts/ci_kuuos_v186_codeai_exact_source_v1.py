#!/usr/bin/env python3
"""v1.86 CodeAI isolated closure-operator/complete-lattice source-bound proof audit.

The candidate differs from frozen original only by explicitly opening the
ScaledSSet namespace and isolated module namespace. v1.85 parent is PR-adopted
but independent post-adoption proof gate is separate, not assumed.
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

MODULE="KUOS.DependentOriginationGeneratedPresentationCompleteLatticeCodeAICandidateV1_86"
ORIGINAL=ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationCompleteLatticeV1_86.lean"
CANDIDATE=ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationCompleteLatticeCodeAICandidateV1_86.lean"
HISTORICAL=ROOT / "legacy/v5.291/formal/KUOS/DependentOriginationGeneratedPresentationCompleteLatticeV1_86.lean"
ORIGINAL_BLOB="15fcc55183142ba4ad1fdf5d3ff402c5a2a0804b"
CANDIDATE_BLOB="0c4efd1ff7e6c0a0735aee2b8b6c939dbffebbc7"
PARENTS={
 "DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85":"eff1b6d74800c4d3e1f37a6806ebf88ff8b6cd0e",
 "DependentOriginationGeneratedPresentationOrderReflectionV1_84":"5c1f7e9dc8fbb12bb901f4c67f0aad99543d49b9",
 "DependentOriginationGeneratedPresentationPosetalReflectionV1_83":"3bc1f096876f8c7b799ae48f29419e6686e33c87",
}
PUBLIC=["orthogonalAnodyneClosure","orthogonalAnodyneClosure_apply","orthogonalAnodyneClosure_isClosed_iff","orthogonalFibrationClosure","orthogonalFibrationClosure_apply","orthogonalFibrationClosure_isClosed_iff","orthogonallySaturatedScaledAnodyneCompleteLattice","orthogonallySaturatedScaledFibrationCompleteLattice","saturatedAnodyne_iInf_val","saturatedAnodyne_iSup_val","saturatedFibration_iInf_val","saturatedFibration_iSup_val","generatedScaledAnodynePresentationCompleteLattice","presentationToSaturatedAnodyne_iSup","presentationToSaturatedAnodyne_iInf","presentationToSaturatedFibration_iSup","presentationToSaturatedFibration_iInf","generatedAnodyneClass_iSup","generatedAnodyneClass_iInf","generatedFibrationClass_iSup","generatedFibrationClass_iInf"]
PATCHES=[["open KUOS.DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85","open KUOS.DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85\nopen KUOS.DependentOriginationScaledTerminalRLPV1_41"],["    intro R A B p hp\n    intro X Y i hi","    intro R A B p hp X Y i hi"],["  generatedPresentationSaturatedAnodyneOrderIso.symm.toGaloisInsertion\n    .liftCompleteLattice","  (generatedPresentationSaturatedAnodyneOrderIso.symm.toGaloisInsertion).liftCompleteLattice"],["  exact map_iSup generatedPresentationSaturatedAnodyneOrderIso P","  exact map_iSup generatedPresentationSaturatedAnodyneOrderIso.toCompleteLatticeHom P"],["  exact map_iInf generatedPresentationSaturatedAnodyneOrderIso P","  exact map_iInf generatedPresentationSaturatedAnodyneOrderIso.toCompleteLatticeHom P"],["  simpa using\n    (map_iSup generatedPresentationSaturatedFibrationOrderIso P)","  exact map_iSup generatedPresentationSaturatedFibrationOrderIso.toCompleteLatticeHom P"],["  simpa using\n    (map_iInf generatedPresentationSaturatedFibrationOrderIso P)","  exact map_iInf generatedPresentationSaturatedFibrationOrderIso.toCompleteLatticeHom P"]]
DECL=re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")

def execute(out: Path) -> dict:
    verify_inputs()
    for module,expected in PARENTS.items():
        if blob((ROOT / "formal/KUOS" / (module + ".lean")).read_bytes()) != expected:
            raise AuditFailure("V186_PARENT_BLOB_MISMATCH "+module)
    raw_orig=ORIGINAL.read_bytes()
    if blob(raw_orig)!=ORIGINAL_BLOB or blob(HISTORICAL.read_bytes())!=ORIGINAL_BLOB:
        raise AuditFailure("V186_ORIGINAL_HISTORICAL_CHANGED")
    raw=CANDIDATE.read_bytes()
    if blob(raw)!=CANDIDATE_BLOB:
        raise AuditFailure("V186_CANDIDATE_CHANGED")
    predicted=raw_orig.decode("utf8").replace("KUOS.DependentOriginationGeneratedPresentationCompleteLatticeV1_86","KUOS.DependentOriginationGeneratedPresentationCompleteLatticeCodeAICandidateV1_86")
    for old,new in PATCHES:
        if predicted.count(old)!=1:
            raise AuditFailure("V186_PATCH_PRECONDITION "+old[:80])
        predicted=predicted.replace(old,new)
    actual=raw.decode("utf8")
    if actual!=predicted:
        raise AuditFailure("V186_UNREVIEWED_SOURCE_EDIT")
    masked=mask_lean_comments(actual)
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b",masked):
        raise AuditFailure("V186_TRUST_BYPASS")
    decls=DECL.findall(masked)
    if decls!=PUBLIC or len(PUBLIC)!=21 or len(set(PUBLIC))!=21:
        raise AuditFailure("V186_DECLARATION_INVENTORY "+repr(decls))
    head=os.environ.get("SOURCE_HEAD","")
    if not re.fullmatch(r"[a-f0-9]{40}",head):
        raise AuditFailure("V186_HEAD_NO_DATA")
    out.mkdir(parents=True,exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("V186_APPEND_ONLY_RECEIPT_EXISTS")
    run_logged(["lake","-KleanArgs=-DwarningAsError=true",
      "-KleanArgs=-DsorryAsError=true","build",MODULE],
      out/"strict-build.log",4800)
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v186-axioms-") as d:
        f=Path(d)/"all-21.lean"
        f.write_text("import "+MODULE+"\n"+
          "".join("#print axioms "+MODULE+"."+name+"\n" for name in PUBLIC),encoding="utf8")
        run_logged(["lake","env","lean","-DwarningAsError=true",
          "-Dweak.sorryAsError=true",str(f)],out/"axiom-audit.log",1800)
    log=(out/"axiom-audit.log").read_text(errors="replace")
    reports={}
    for name in PUBLIC:
        full=MODULE+"."+name
        found=re.search(r"'"+re.escape(full)+r"'\s+depends on axioms:\s*\[([^\]]*)\]",log,re.S)
        if found:
            reports[name]=sorted(x.strip() for x in found.group(1).split(",") if x.strip())
        elif re.search(r"'"+re.escape(full)+r"'\s+does not depend on any axioms",log):
            reports[name]=[]
        else:
            raise AuditFailure("V186_AXIOM_NO_DATA "+full)
    axioms=set(a for values in reports.values() for a in values)
    if axioms-STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("V186_NONSTANDARD_AXIOM "+repr(sorted(axioms-STANDARD_AXIOMS)))
    receipt={
      "kind":"KUUOS_V186_CODEAI_EXACT_SOURCE_21_AXIOM_AUDIT",
      "head":head,"source_blob":CANDIDATE_BLOB,"original_blob":ORIGINAL_BLOB,
      "sha256":hashlib.sha256(raw).hexdigest(),"public_declarations":len(reports),
      "lean_pin":"leanprover/lean4:v4.30.0-rc2",
      "mathlib_pin":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
      "axioms":sorted(axioms),"sorryAx":False,"warnings":0,"errors":0,
      "adopted_in_pr":False,"parent_v185_independent_gate_separate":True,
      "standard_equals_canonical_asserted":False,
      "general_forward_endpoint_RLP_asserted":False,
    }
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("KUUOS_V186_CODEAI_KERNEL_GREEN "+json.dumps(receipt,ensure_ascii=False),flush=True)
    return receipt

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    try:
        execute(args.out.resolve())
        return 0
    except (AuditFailure,OSError,ValueError) as err:
        print("KUUOS_V186_CODEAI_HOLD "+json.dumps({
            "status":"UNAUTHENTICATED","obstruction":str(err),"merged":False,
        }),file=sys.stderr,flush=True)
        return 2
if __name__=="__main__":
    sys.exit(main())
