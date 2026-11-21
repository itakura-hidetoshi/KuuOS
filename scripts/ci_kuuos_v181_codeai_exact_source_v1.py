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
CANDIDATE_BLOB = "620fc8de4c148e99284db12fc94891322a3e4b60"
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
    # Explicit syntax/API repairs only. Every original occurrence and count is pinned.
    for before, after, count in [["open KUOS.DependentOriginationScaledTerminalRLPV1_41\n","open KUOS.DependentOriginationScaledTerminalRLPV1_41\nopen KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43\nopen KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46\nopen KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49\nopen KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50\nopen KUOS.DependentOriginationStandardTypeAScaledLeibnizPushoutV1_55\nopen KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59\n",1],["open KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80.\n  GeneratedScaledAnodynePresentationEquivalence","open KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80.GeneratedScaledAnodynePresentationEquivalence",1],["generatedPresentationSetoid (u := u)","generatedPresentationSetoid.{u}",2],["noncomputable theorem ","theorem ",3],["Quotient.sound K.toGeneratedPresentationEquivalence","Quotient.sound (KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80.StandardABCCanonicalPositiveComparisonCertificate.toGeneratedPresentationEquivalence K)",1]]:
        if expected.count(before) != count:
            raise AuditFailure("V181_REWRITE_COUNT_MISMATCH " + before[:60])
        expected = expected.replace(before, after)
    # Next stage: exact original-preserving quotient elaboration repairs, no hypothesis weakening.
    for before, after, count in [["  presentationClass\n    (standardScaledAnodyneGeneratorsABC :","  presentationClass.{u}\n    (standardScaledAnodyneGeneratorsABC :",1],["  presentationClass\n    (scaledHornAttachmentGenerators :","  presentationClass.{u}\n    (scaledHornAttachmentGenerators :",1],["  change\n    TypeAEndpointLeibnizGeneratorsGeneratedBy\n      (standardScaledAnodyneGeneratorsABC :\n        MorphismProperty (ScaledSSet.{u}))\n  exact standardABC_typeAEndpointLeibnizGeneratorsGenerated","  simpa only [standardABCPresentation] using\n    (typeAEndpointGeneratorsGenerated_presentationClass\n      (standardScaledAnodyneGeneratorsABC :\n        MorphismProperty (ScaledSSet.{u}))).2\n      standardABC_typeAEndpointLeibnizGeneratorsGenerated",1],["  change\n    TypeAEndpointLeibnizStableForPresentation\n      (standardScaledAnodyneGeneratorsABC :\n        MorphismProperty (ScaledSSet.{u}))\n  exact standardABC_typeAEndpointLeibnizStable","  simpa only [standardABCPresentation] using\n    (typeAEndpointStable_presentationClass\n      (standardScaledAnodyneGeneratorsABC :\n        MorphismProperty (ScaledSSet.{u}))).2\n      standardABC_typeAEndpointLeibnizStable",1],["  change\n    TypeAEndpointLeibnizLiftingForPresentation\n      (standardScaledAnodyneGeneratorsABC :\n        MorphismProperty (ScaledSSet.{u}))\n  exact standardABC_typeAEndpointLeibnizLifting","  simpa only [standardABCPresentation] using\n    (typeAEndpointLifting_presentationClass\n      (standardScaledAnodyneGeneratorsABC :\n        MorphismProperty (ScaledSSet.{u}))).2\n      standardABC_typeAEndpointLeibnizLifting",1],["  change\n    MorphismProperty.IsWeakFactorizationSystem\n      (canonicalGeneratedScaledAnodyne :\n        MorphismProperty (ScaledSSet.{u}))\n      (canonicalGeneratedScaledFibration :\n        MorphismProperty (ScaledSSet.{u}))\n  exact canonicalGeneratedScaledWeakFactorizationSystem_unconditional","  have hWFS : MorphismProperty.IsWeakFactorizationSystem\n      (externalGeneratedScaledAnodyne\n        (scaledHornAttachmentGenerators :\n          MorphismProperty (ScaledSSet.{u})))\n      (externalGeneratedScaledFibration\n        (scaledHornAttachmentGenerators :\n          MorphismProperty (ScaledSSet.{u}))) := by\n    change MorphismProperty.IsWeakFactorizationSystem\n      (canonicalGeneratedScaledAnodyne :\n        MorphismProperty (ScaledSSet.{u}))\n      (canonicalGeneratedScaledFibration :\n        MorphismProperty (ScaledSSet.{u}))\n    exact canonicalGeneratedScaledWeakFactorizationSystem_unconditional\n  simpa only [canonicalKuuOSPresentation] using\n    (isWeakFactorizationSystem_presentationClass\n      (scaledHornAttachmentGenerators :\n        MorphismProperty (ScaledSSet.{u}))).2 hWFS",1],["  exact presentationClass_eq_iff _ _","  simpa only [standardABCPresentation, canonicalKuuOSPresentation] using\n    (presentationClass_eq_iff\n      (standardScaledAnodyneGeneratorsABC :\n        MorphismProperty (ScaledSSet.{u}))\n      (scaledHornAttachmentGenerators :\n        MorphismProperty (ScaledSSet.{u})))",1],["  exact presentationClass_eq_iff_generatedAnodyne_eq _ _","  simpa only [standardABCPresentation, canonicalKuuOSPresentation,\n      standardGeneratedScaledAnodyneABC, canonicalGeneratedScaledAnodyne,\n      externalGeneratedScaledAnodyne] using\n    (presentationClass_eq_iff_generatedAnodyne_eq\n      (standardScaledAnodyneGeneratorsABC :\n        MorphismProperty (ScaledSSet.{u}))\n      (scaledHornAttachmentGenerators :\n        MorphismProperty (ScaledSSet.{u})))",1],["(h : standardABCPresentation = canonicalKuuOSPresentation)","(h : standardABCPresentation.{u} = canonicalKuuOSPresentation.{u})",3],["  rw [← h]\n  exact standardABCPresentation_endpointStable","  exact h ▸ standardABCPresentation_endpointStable.{u}",1],["  rw [← h]\n  exact standardABCPresentation_endpointLifting","  exact h ▸ standardABCPresentation_endpointLifting.{u}",1],["  rw [h]\n  exact canonicalKuuOSPresentation_isWFS","  exact h.symm ▸ canonicalKuuOSPresentation_isWFS.{u}",1],["  Quotient.sound (KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80.StandardABCCanonicalPositiveComparisonCertificate.toGeneratedPresentationEquivalence K)","  (standardABC_eq_canonical_iff_mutualGeneration.{u}).2\n    (KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80.StandardABCCanonicalPositiveComparisonCertificate.toGeneratedPresentationEquivalence.{u} K)",1],["  canonicalKuuOSPresentation_endpointStable_of_eq\n    (standardABC_eq_canonical_of_positiveComparison K)","  canonicalKuuOSPresentation_endpointStable_of_eq.{u}\n    (standardABC_eq_canonical_of_positiveComparison.{u} K)",1],["  canonicalKuuOSPresentation_endpointLifting_of_eq\n    (standardABC_eq_canonical_of_positiveComparison K)","  canonicalKuuOSPresentation_endpointLifting_of_eq.{u}\n    (standardABC_eq_canonical_of_positiveComparison.{u} K)",1],["  standardABCPresentation_isWFS_of_eq\n    (standardABC_eq_canonical_of_positiveComparison K)","  standardABCPresentation_isWFS_of_eq.{u}\n    (standardABC_eq_canonical_of_positiveComparison.{u} K)",1]]:
        if expected.count(before) != count:
            raise AuditFailure("V181_QUOTIENT_REWRITE_COUNT_MISMATCH " + before[:60])
        expected = expected.replace(before, after)
    # CodeAI structural-universe patch v3: explicit Lean universe identity only.
    # Each theorem statement has exactly the same proposition, now at the named .{u}.
    for before, after in [["theorem standardABCPresentation_endpointGeneratorsGenerated :\n    typeAEndpointGeneratorsGenerated standardABCPresentation := by","theorem standardABCPresentation_endpointGeneratorsGenerated :\n    typeAEndpointGeneratorsGenerated.{u} standardABCPresentation.{u} := by"],["theorem standardABCPresentation_endpointStable :\n    typeAEndpointStable standardABCPresentation := by","theorem standardABCPresentation_endpointStable :\n    typeAEndpointStable.{u} standardABCPresentation.{u} := by"],["theorem standardABCPresentation_endpointLifting :\n    typeAEndpointLifting standardABCPresentation := by","theorem standardABCPresentation_endpointLifting :\n    typeAEndpointLifting.{u} standardABCPresentation.{u} := by"],["theorem canonicalKuuOSPresentation_isWFS :\n    isWeakFactorizationSystem canonicalKuuOSPresentation := by","theorem canonicalKuuOSPresentation_isWFS :\n    isWeakFactorizationSystem.{u} canonicalKuuOSPresentation.{u} := by"],["theorem standardABC_eq_canonical_iff_mutualGeneration :\n    standardABCPresentation = canonicalKuuOSPresentation ↔","theorem standardABC_eq_canonical_iff_mutualGeneration :\n    standardABCPresentation.{u} = canonicalKuuOSPresentation.{u} ↔"],["theorem standardABC_eq_canonical_iff_generatedAnodyne_eq :\n    standardABCPresentation = canonicalKuuOSPresentation ↔","theorem standardABC_eq_canonical_iff_generatedAnodyne_eq :\n    standardABCPresentation.{u} = canonicalKuuOSPresentation.{u} ↔"],["(h : standardABCPresentation.{u} = canonicalKuuOSPresentation.{u}) :\n    typeAEndpointStable canonicalKuuOSPresentation := by","(h : standardABCPresentation.{u} = canonicalKuuOSPresentation.{u}) :\n    typeAEndpointStable.{u} canonicalKuuOSPresentation.{u} := by"],["(h : standardABCPresentation.{u} = canonicalKuuOSPresentation.{u}) :\n    typeAEndpointLifting canonicalKuuOSPresentation := by","(h : standardABCPresentation.{u} = canonicalKuuOSPresentation.{u}) :\n    typeAEndpointLifting.{u} canonicalKuuOSPresentation.{u} := by"],["(h : standardABCPresentation.{u} = canonicalKuuOSPresentation.{u}) :\n    isWeakFactorizationSystem standardABCPresentation := by","(h : standardABCPresentation.{u} = canonicalKuuOSPresentation.{u}) :\n    isWeakFactorizationSystem.{u} standardABCPresentation.{u} := by"],["theorem standardABC_eq_canonical_of_positiveComparison\n    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :\n    standardABCPresentation = canonicalKuuOSPresentation :=","theorem standardABC_eq_canonical_of_positiveComparison\n    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :\n    standardABCPresentation.{u} = canonicalKuuOSPresentation.{u} :="],["theorem canonicalKuuOSPresentation_endpointStable_of_positiveComparison\n    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :\n    typeAEndpointStable canonicalKuuOSPresentation :=","theorem canonicalKuuOSPresentation_endpointStable_of_positiveComparison\n    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :\n    typeAEndpointStable.{u} canonicalKuuOSPresentation.{u} :="],["theorem canonicalKuuOSPresentation_endpointLifting_of_positiveComparison\n    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :\n    typeAEndpointLifting canonicalKuuOSPresentation :=","theorem canonicalKuuOSPresentation_endpointLifting_of_positiveComparison\n    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :\n    typeAEndpointLifting.{u} canonicalKuuOSPresentation.{u} :="],["theorem standardABCPresentation_isWFS_of_positiveComparison\n    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :\n    isWeakFactorizationSystem standardABCPresentation :=","theorem standardABCPresentation_isWFS_of_positiveComparison\n    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :\n    isWeakFactorizationSystem.{u} standardABCPresentation.{u} :="]]:
        if expected.count(before) != 1:
            raise AuditFailure("V181_CODEAI_UNIVERSE_PATCH_ANCHOR " + before[:80])
        expected = expected.replace(before, after)
    if candidate != expected:
        raise AuditFailure("V181_ONLY_REVIEWED_REPAIRS_ALLOWED")
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
