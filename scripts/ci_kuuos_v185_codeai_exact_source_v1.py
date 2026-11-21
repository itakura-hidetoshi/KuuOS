#!/usr/bin/env python3
"""KuuOS v1.85 fixed-point-order-iso CodeAI candidate, pinned 20 axiom audit.

Only an explicit reviewed namespace open and the isolated candidate namespace
may differ from frozen original. No main or PR source mutation is authorized.
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

MODULE = "KUOS.DependentOriginationGeneratedPresentationFixedPointOrderIsoCodeAICandidateV1_85"
ORIGINAL = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85.lean"
CANDIDATE = ROOT / "formal/KUOS/DependentOriginationGeneratedPresentationFixedPointOrderIsoCodeAICandidateV1_85.lean"
HISTORICAL = ROOT / "legacy/v5.291/formal/KUOS/DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85.lean"
ORIGINAL_BLOB = "97e364b48eb5632ab7f9f79b051f5b665445c682"
CANDIDATE_BLOB = "1666e8b6528e41b0c396e6cad91292c48f1947f9"
PARENTS = {
    "DependentOriginationGeneratedPresentationOrderReflectionV1_84": "5c1f7e9dc8fbb12bb901f4c67f0aad99543d49b9",
    "DependentOriginationGeneratedPresentationPosetalReflectionV1_83": "3bc1f096876f8c7b799ae48f29419e6686e33c87",
    "DependentOriginationGeneratedPresentationQuotientInvariantV1_81": "8ba7b0e6034a2e24b44587fb477c2192cffffeca",
}
PUBLIC = ["OrthogonallySaturatedScaledAnodyne","IsRightOrthogonallySaturated","OrthogonallySaturatedScaledFibration","generatedAnodyneClass_isOrthogonallySaturated","generatedFibrationClass_isRightOrthogonallySaturated","presentationToSaturatedAnodyne","saturatedAnodyneToPresentation","saturatedAnodyneToPresentation_presentationToSaturatedAnodyne","presentationToSaturatedAnodyne_saturatedAnodyneToPresentation","generatedPresentationSaturatedAnodyneOrderIso","generatedPresentationSaturatedAnodyneOrderIso_apply_val","presentationToSaturatedFibration","saturatedFibrationToPresentation","saturatedFibrationToPresentation_presentationToSaturatedFibration","presentationToSaturatedFibration_saturatedFibrationToPresentation","generatedPresentationSaturatedFibrationOrderIso","generatedPresentationSaturatedFibrationOrderIso_apply_val","saturatedAnodyneFibrationOrderIso","presentation_eq_iff_saturatedAnodyne_eq","presentation_eq_iff_saturatedFibration_eq"]
PATCH = ["open KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84","open KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84\nopen KUOS.DependentOriginationScaledTerminalRLPV1_41"]
DECL = re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")

def execute(out: Path) -> dict:
    verify_inputs()
    for module, expected in PARENTS.items():
        file = ROOT / "formal/KUOS" / (module + ".lean")
        if blob(file.read_bytes()) != expected:
            raise AuditFailure("V185_PARENT_BLOB_MISMATCH "+module)
    raw_original=ORIGINAL.read_bytes()
    if blob(raw_original)!=ORIGINAL_BLOB or blob(HISTORICAL.read_bytes())!=ORIGINAL_BLOB:
        raise AuditFailure("V185_ORIGINAL_OR_HISTORICAL_CHANGED")
    raw=CANDIDATE.read_bytes()
    if blob(raw)!=CANDIDATE_BLOB:
        raise AuditFailure("V185_CANDIDATE_BLOB_CHANGED")
    expected=raw_original.decode("utf8").replace(
        "KUOS.DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85", "KUOS.DependentOriginationGeneratedPresentationFixedPointOrderIsoCodeAICandidateV1_85")
    old,new=PATCH
    if expected.count(old)!=1:
        raise AuditFailure("V185_PATCH_PRECONDITION")
    expected=expected.replace(old,new)
    actual=raw.decode("utf8")
    if actual!=expected:
        raise AuditFailure("V185_UNREVIEWED_SOURCE_EDIT")
    masked=mask_lean_comments(actual)
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom)\b",masked):
        raise AuditFailure("V185_TRUST_BYPASS")
    declarations=DECL.findall(masked)
    if declarations!=PUBLIC or len(PUBLIC)!=20 or len(set(PUBLIC))!=20:
        raise AuditFailure("V185_DECLARATION_INVENTORY "+repr(declarations))
    head=os.environ.get("SOURCE_HEAD","")
    if not re.fullmatch(r"[a-f0-9]{40}",head):
        raise AuditFailure("V185_NO_DATA_HEAD")
    out.mkdir(parents=True,exist_ok=True)
    if list(out.iterdir()):
        raise AuditFailure("V185_APPEND_ONLY_RECEIPT_EXISTS")
    run_logged(["lake","-KleanArgs=-DwarningAsError=true",
        "-KleanArgs=-DsorryAsError=true","build",MODULE],
        out/"strict-build.log",4800)
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v185-axioms-") as d:
        audit=Path(d)/"all-20.lean"
        audit.write_text("import "+MODULE+"\n"+
            "".join("#print axioms "+MODULE+"."+name+"\n" for name in PUBLIC),
            encoding="utf8")
        run_logged(["lake","env","lean","-DwarningAsError=true",
            "-Dweak.sorryAsError=true",str(audit)],out/"axiom-audit.log",1800)
    log=(out/"axiom-audit.log").read_text(errors="replace")
    reports={}
    for name in PUBLIC:
        full=MODULE+"."+name
        match=re.search(r"'"+re.escape(full)+r"'\s+depends on axioms:\s*\[([^\]]*)\]",log,re.S)
        if match:
            reports[name]=sorted(a.strip() for a in match.group(1).split(",") if a.strip())
        elif re.search(r"'"+re.escape(full)+r"'\s+does not depend on any axioms",log):
            reports[name]=[]
        else:
            raise AuditFailure("V185_AXIOM_NO_DATA "+full)
    axioms=set(a for xs in reports.values() for a in xs)
    if axioms-STANDARD_AXIOMS or "sorryAx" in log:
        raise AuditFailure("V185_NONSTANDARD_AXIOM "+repr(sorted(axioms-STANDARD_AXIOMS)))
    receipt={
        "kind":"KUUOS_V185_CODEAI_EXACT_SOURCE_20_AXIOM_AUDIT",
        "head":head,"source_blob":CANDIDATE_BLOB,"original_blob":ORIGINAL_BLOB,
        "sha256":hashlib.sha256(raw).hexdigest(),
        "public_declarations":len(reports),
        "lean_pin":"leanprover/lean4:v4.30.0-rc2",
        "mathlib_pin":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
        "axioms":sorted(axioms),"sorryAx":False,"warnings":0,"errors":0,
        "original_source_adopted_in_PR":False,
        "standard_canonical_equivalence_asserted":False,
        "general_forward_endpoint_RLP_asserted":False,
    }
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("KUUOS_V185_CODEAI_KERNEL_GREEN "+json.dumps(receipt,ensure_ascii=False),flush=True)
    return receipt

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    try:
        execute(args.out.resolve())
        return 0
    except (AuditFailure,OSError,ValueError) as exc:
        print("KUUOS_V185_CODEAI_HOLD "+json.dumps({
            "status":"UNAUTHENTICATED","obstruction":str(exc),"merged":False,
        }),file=sys.stderr,flush=True)
        return 2

if __name__=="__main__":
    sys.exit(main())
