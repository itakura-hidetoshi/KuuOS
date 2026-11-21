#!/usr/bin/env python3
"""KuuOS v1.81 CodeAI: isolated, pinned strict Lean + exact 37 declaration axiom audit.
This certifies the candidate *only*, not parent PR acceptance or canonical comparison.
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

MODULE = "KUOS.DependentOriginationGeneratedPresentationQuotientCodeAICandidateV1_81"
CANDIDATE = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationQuotientCodeAICandidateV1_81.lean"
ORIGINAL = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationQuotientInvariantV1_81.lean"
CANDIDATE_BLOB = "0f1335c7854443156311b2ed7e329d3405e51ec3"
ORIGINAL_BLOB = "0a2ece6612bd717cd210c0222cf5a00bc04e4f37"
PARENTS = {
    "DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77": "d786495a68268e01634f6f8143ebe09241bffc3e",
    "DependentOriginationStandardABCPostEndpointCanonicalComparisonV1_78": "b406155d78506527b53549f0cf232d55f084ac86",
    "DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79": "cd9a58880341e70a2290387d21d144613464c8c0",
    "DependentOriginationGeneratedPresentationEndpointInvariantV1_80": "7be90de61f5c05456de6fa74dd1f262430486d84",
}
QUALIFIED = [
    "ScaledAnodynePresentation",
    "generatedPresentationSetoid",
    "GeneratedScaledAnodynePresentation",
    "presentationClass",
    "presentationClass_eq_iff",
    "presentationClass_eq_iff_generatedAnodyne_eq",
    "generatedAnodyneClass",
    "generatedAnodyneClass_presentationClass",
    "generatedFibrationClass",
    "generatedFibrationClass_presentationClass",
    "typeAEndpointGeneratorsGenerated",
    "typeAEndpointGeneratorsGenerated_presentationClass",
    "typeAEndpointStable",
    "typeAEndpointStable_presentationClass",
    "typeAEndpointLifting",
    "typeAEndpointLifting_presentationClass",
    "isWeakFactorizationSystem",
    "isWeakFactorizationSystem_presentationClass",
    "isFibrant",
    "isFibrant_presentationClass",
    "GeneratedPresentationTheory",
    "generatedTheory",
    "standardABCPresentation",
    "canonicalKuuOSPresentation",
    "standardABCPresentation_endpointGeneratorsGenerated",
    "standardABCPresentation_endpointStable",
    "standardABCPresentation_endpointLifting",
    "canonicalKuuOSPresentation_isWFS",
    "standardABC_eq_canonical_iff_mutualGeneration",
    "standardABC_eq_canonical_iff_generatedAnodyne_eq",
    "canonicalKuuOSPresentation_endpointStable_of_eq",
    "canonicalKuuOSPresentation_endpointLifting_of_eq",
    "standardABCPresentation_isWFS_of_eq",
    "standardABC_eq_canonical_of_positiveComparison",
    "canonicalKuuOSPresentation_endpointStable_of_positiveComparison",
    "canonicalKuuOSPresentation_endpointLifting_of_positiveComparison",
    "standardABCPresentation_isWFS_of_positiveComparison"
]
BARE = ["ScaledAnodynePresentation","generatedPresentationSetoid","GeneratedScaledAnodynePresentation","presentationClass","presentationClass_eq_iff","presentationClass_eq_iff_generatedAnodyne_eq","generatedAnodyneClass","generatedAnodyneClass_presentationClass","generatedFibrationClass","generatedFibrationClass_presentationClass","typeAEndpointGeneratorsGenerated","typeAEndpointGeneratorsGenerated_presentationClass","typeAEndpointStable","typeAEndpointStable_presentationClass","typeAEndpointLifting","typeAEndpointLifting_presentationClass","isWeakFactorizationSystem","isWeakFactorizationSystem_presentationClass","isFibrant","isFibrant_presentationClass","GeneratedPresentationTheory","generatedTheory","standardABCPresentation","canonicalKuuOSPresentation","standardABCPresentation_endpointGeneratorsGenerated","standardABCPresentation_endpointStable","standardABCPresentation_endpointLifting","canonicalKuuOSPresentation_isWFS","standardABC_eq_canonical_iff_mutualGeneration","standardABC_eq_canonical_iff_generatedAnodyne_eq","canonicalKuuOSPresentation_endpointStable_of_eq","canonicalKuuOSPresentation_endpointLifting_of_eq","standardABCPresentation_isWFS_of_eq","standardABC_eq_canonical_of_positiveComparison","canonicalKuuOSPresentation_endpointStable_of_positiveComparison","canonicalKuuOSPresentation_endpointLifting_of_positiveComparison","standardABCPresentation_isWFS_of_positiveComparison"]
DECL = re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")

def execute(out: Path) -> dict:
    verify_inputs()
    for name, expected in PARENTS.items():
        got = blob((ROOT / "formal/KUOS" / (name + ".lean")).read_bytes())
        if got != expected:
            raise AuditFailure("PARENT_BLOB_MISMATCH " + name + " " + got)
    if blob(ORIGINAL.read_bytes()) != ORIGINAL_BLOB:
        raise AuditFailure("ORIGINAL_181_CHANGED")
    raw = CANDIDATE.read_bytes()
    if blob(raw) != CANDIDATE_BLOB:
        raise AuditFailure("CANDIDATE_181_BLOB_MISMATCH")
    candidate = raw.decode("utf8")
    expected = ORIGINAL.read_text(encoding="utf8").replace(
        "open CategoryTheory\n",
        "open CategoryTheory\nopen KUOS.DependentOriginationScaledTerminalRLPV1_41\n"
    ).replace("KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81", "KUOS.DependentOriginationGeneratedPresentationQuotientCodeAICandidateV1_81")
    if candidate != expected:
        raise AuditFailure("V181_ONLY_NAMESPACE_OPEN_AND_MODULE_RENAME_ALLOWED")
    masked = mask_lean_comments(candidate)
    if re.search(r"(?m)^\s*(?:axiom|sorry|admit)\b", masked):
        raise AuditFailure("TRUST_BYPASS")
    if DECL.findall(masked) != BARE or len(QUALIFIED) != 37 or len(set(QUALIFIED)) != 37:
        raise AuditFailure("DECLARATION_INVENTORY")
    head = os.environ.get("SOURCE_HEAD", "")
    if re.fullmatch("[a-f0-9]{40}", head) is None:
        raise AuditFailure("NO_DATA_HEAD")
    out.mkdir(parents=True,exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("APPEND_ONLY_RECEIPT_EXISTS")
    run_logged(["lake","-KleanArgs=-DwarningAsError=true",
                "-KleanArgs=-DsorryAsError=true","build",MODULE],
               out / "strict-build.log",4800)
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v181-axiom-") as t:
        f=Path(t)/"all-37.lean"
        f.write_text("import "+MODULE+"\n"+
            "".join("#print axioms "+MODULE+"."+name+"\n" for name in QUALIFIED),
            encoding="utf8")
        run_logged(["lake","env","lean","-DwarningAsError=true",
                    "-Dweak.sorryAsError=true",str(f)],out/"axiom-audit.log",1800)
    log=(out/"axiom-audit.log").read_text(errors="replace")
    reports={}
    for name in QUALIFIED:
        fq=MODULE+"."+name
        m=re.search(r"'"+re.escape(fq)+r"'\s+depends on axioms:\s*\[([^\]]*)\]",log,re.S)
        if m: reports[name]=sorted(a.strip() for a in m.group(1).split(",") if a.strip())
        elif re.search(r"'"+re.escape(fq)+r"'\s+does not depend on any axioms",log):
            reports[name]=[]
        else: raise AuditFailure("AXIOM_REPORT_MISSING "+fq)
    union=set(ax for axs in reports.values() for ax in axs)
    if union-STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("EXTRA_AX_AND_SORRY "+",".join(sorted(union-STANDARD_AXIOMS)))
    receipt={"kind":"KUUOS_V181_CODEAI_EXACT_SOURCE_37_AXIOM_AUDIT",
        "head":head, "candidate_blob":CANDIDATE_BLOB,
        "original_blob":ORIGINAL_BLOB,
        "sha256":hashlib.sha256(raw).hexdigest(),
        "lean_pin":"leanprover/lean4:v4.30.0-rc2",
        "mathlib_pin":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
        "public_declarations":len(reports),"axioms":sorted(union),
        "sorryAx":False,"warnings":0,"errors":0,
        "original_source_adopted":False,"general_canonical_RLP":False,
        "independent_approval":"PENDING_UNTIL_WORKFLOW_SUCCESS"}
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("KUUOS_V181_CODEAI_KERNEL_GREEN "+json.dumps(receipt,ensure_ascii=False),flush=True)
    return receipt

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True,type=Path)
    args=ap.parse_args()
    try:
        execute(args.out.resolve())
        return 0
    except (AuditFailure,OSError,ValueError) as exc:
        print("KUUOS_V181_CODEAI_HOLD "+json.dumps({
            "status":"UNAUTHENTICATED","obstruction":str(exc),
            "original_source_adopted":False,"merged":False
        }),file=sys.stderr,flush=True)
        return 2

if __name__=="__main__":
    sys.exit(main())
