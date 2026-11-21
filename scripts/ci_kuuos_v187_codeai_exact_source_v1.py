#!/usr/bin/env python3
"""v1.87 Standard/Canonical gap CodeAI research: exact pinned 27-declaration proof audit.

Research candidate has one explicitly reviewed namespace open. Gap equality
remains a *predicate equivalent to geometric comparison*, not proved here.
The frozen historical source and current PR original are not changed.
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

MODULE="KUOS.DependentOriginationStandardCanonicalPresentationGapCodeAICandidateV1_87"
ORIGINAL=ROOT/"formal/KUOS/DependentOriginationStandardCanonicalPresentationGapV1_87.lean"
CANDIDATE=ROOT/"formal/KUOS/DependentOriginationStandardCanonicalPresentationGapCodeAICandidateV1_87.lean"
HISTORICAL=ROOT/"legacy/v5.291/formal/KUOS/DependentOriginationStandardCanonicalPresentationGapV1_87.lean"
ORIGINAL_BLOB="88181c3c721c129e2aa628406e3fbf77a89d4f91"
CANDIDATE_BLOB="35a7ee2fa0dbb9168d20ec9bd058d345b2495125"
PARENTS={
 "DependentOriginationGeneratedPresentationCompleteLatticeV1_86":"57e4436f389928864ebd75ef4b6a0a535b8d51c8",
 "DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85":"eff1b6d74800c4d3e1f37a6806ebf88ff8b6cd0e",
 "DependentOriginationGeneratedPresentationOrderReflectionV1_84":"5c1f7e9dc8fbb12bb901f4c67f0aad99543d49b9",
}
PUBLIC=["standardCanonicalLowerEnvelope","standardCanonicalUpperEnvelope","standardCanonicalPresentationInterval","lowerEnvelope_le_standardABC","lowerEnvelope_le_canonicalKuuOS","standardABC_le_upperEnvelope","canonicalKuuOS_le_upperEnvelope","le_lowerEnvelope_iff","upperEnvelope_le_iff","mem_standardCanonicalPresentationInterval_iff","standardABCPresentation_mem_interval","canonicalKuuOSPresentation_mem_interval","canonicalKuuOS_le_standardABC_iff_lowerEnvelope_eq_canonical","canonicalKuuOS_le_standardABC_iff_upperEnvelope_eq_standard","canonicalKuuOS_le_standardABC_iff_envelopes","standardABC_le_canonicalKuuOS_iff_lowerEnvelope_eq_standard","standardABC_le_canonicalKuuOS_iff_upperEnvelope_eq_canonical","standardABC_le_canonicalKuuOS_iff_envelopes","interval_eq_of_canonicalKuuOS_le_standardABC","interval_eq_of_standardABC_le_canonicalKuuOS","StandardCanonicalPresentationGapClosed","standardCanonicalPresentationGapClosed_iff","standardCanonicalPresentationGapClosed_iff_mutual_le","standardCanonicalPresentationGapClosed_iff_direct_generator_inclusions","interval_eq_of_positiveResidual","interval_eq_of_generatorwiseReverse","standardCanonicalPresentationGapClosed_iff_generatorwiseReverse_of_positiveResidual"]
PATCH=["open KUOS.DependentOriginationGeneratedPresentationCompleteLatticeV1_86","open KUOS.DependentOriginationGeneratedPresentationCompleteLatticeV1_86\nopen KUOS.DependentOriginationScaledTerminalRLPV1_41"]
DECL=re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")

def execute(out:Path)->dict:
    verify_inputs()
    for name,expected in PARENTS.items():
        if blob((ROOT/"formal/KUOS"/(name+".lean")).read_bytes())!=expected:
            raise AuditFailure("V187_PARENT_BLOB_MISMATCH "+name)
    raw_original=ORIGINAL.read_bytes()
    if blob(raw_original)!=ORIGINAL_BLOB or blob(HISTORICAL.read_bytes())!=ORIGINAL_BLOB:
        raise AuditFailure("V187_ORIGINAL_OR_FROZEN_CHANGED")
    raw=CANDIDATE.read_bytes()
    if blob(raw)!=CANDIDATE_BLOB:
        raise AuditFailure("V187_CANDIDATE_BLOB_MISMATCH")
    predicted=raw_original.decode("utf8").replace("KUOS.DependentOriginationStandardCanonicalPresentationGapV1_87","KUOS.DependentOriginationStandardCanonicalPresentationGapCodeAICandidateV1_87")
    old,new=PATCH
    if predicted.count(old)!=1:
        raise AuditFailure("V187_SOURCE_EDIT_PRECONDITION")
    predicted=predicted.replace(old,new)
    actual=raw.decode("utf8")
    if actual!=predicted:
        raise AuditFailure("V187_UNREVIEWED_SOURCE_EDIT")
    masked=mask_lean_comments(actual)
    if re.search(r"(?m)^\s*(?:axiom|sorry|admit)\b",masked):
        raise AuditFailure("V187_TRUST_BYPASS")
    inventory=DECL.findall(masked)
    if inventory!=PUBLIC or len(PUBLIC)!=27 or len(set(PUBLIC))!=27:
        raise AuditFailure("V187_PUBLIC_INVENTORY "+repr(inventory))
    head=os.environ.get("SOURCE_HEAD","")
    if not re.fullmatch(r"[a-f0-9]{40}",head):
        raise AuditFailure("V187_EXACT_HEAD_NO_DATA")
    out.mkdir(parents=True,exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("V187_APPEND_ONLY_RECEIPT_EXISTS")
    run_logged(["lake","-KleanArgs=-DwarningAsError=true",
        "-KleanArgs=-DsorryAsError=true","build",MODULE],out/"strict-build.log",4800)
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v187-axioms-") as d:
        a=Path(d)/"all-27.lean"
        a.write_text("import "+MODULE+"\n"+
            "".join("#print axioms "+MODULE+"."+name+"\n" for name in PUBLIC),
            encoding="utf8")
        run_logged(["lake","env","lean","-DwarningAsError=true",
            "-Dweak.sorryAsError=true",str(a)],out/"axiom-audit.log",1800)
    log=(out/"axiom-audit.log").read_text(errors="replace")
    reports={}
    for name in PUBLIC:
        full=MODULE+"."+name
        match=re.search(r"'"+re.escape(full)+r"'\s+depends on axioms:\s*\[([^\]]*)\]",log,re.S)
        if match:
            reports[name]=sorted(z.strip() for z in match.group(1).split(",") if z.strip())
        elif re.search(r"'"+re.escape(full)+r"'\s+does not depend on any axioms",log):
            reports[name]=[]
        else:
            raise AuditFailure("V187_PUBLIC_AXIOM_NO_DATA "+full)
    axioms=set(z for values in reports.values() for z in values)
    if axioms-STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("V187_NONSTANDARD_AXIOM "+repr(sorted(axioms-STANDARD_AXIOMS)))
    receipt={
      "kind":"KUUOS_V187_CODEAI_EXACT_SOURCE_27_AXIOM_AUDIT",
      "head":head,"source_blob":CANDIDATE_BLOB,
      "original_blob":ORIGINAL_BLOB,
      "source_sha256":hashlib.sha256(raw).hexdigest(),
      "public_declarations":len(reports),
      "lean_pin":"leanprover/lean4:v4.30.0-rc2",
      "mathlib_pin":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
      "axioms":sorted(axioms),"sorryAx":False,"warnings":0,"errors":0,
      "adopted_in_PR":False,
      "standard_canonical_equality_proved":False,
      "forward_endpoint_RLP_general_proved":False
    }
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("KUUOS_V187_CODEAI_KERNEL_GREEN "+json.dumps(receipt,ensure_ascii=False),flush=True)
    return receipt

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    try:
        execute(args.out.resolve())
        return 0
    except (AuditFailure,OSError,ValueError) as e:
        print("KUUOS_V187_CODEAI_HOLD "+json.dumps({
            "status":"UNAUTHENTICATED","obstruction":str(e),"merged":False}),
            file=sys.stderr,flush=True)
        return 2
if __name__=="__main__":
    sys.exit(main())
