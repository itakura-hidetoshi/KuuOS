#!/usr/bin/env python3
"""KuuOS CodeAI v1.88 R6: exact-source pinned Strict Lean + 22 declaration axiom audit.

R1 is failed typed feedback; code edits are proposal-only until independent
kernel acceptance. Never adopt the original module or change historical roots.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from scripts.ci_kuuos_v176_exact_source_audit_v1 import (
    ROOT, STANDARD_AXIOMS, blob, verify_inputs,
)
from scripts.kuuos_lean_mcp_repair_loop_v1 import mask_lean_comments

MODULE="KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR9V1_88"
CANDIDATE=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR9V1_88.lean"
ORIGINAL=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88.lean"
HISTORY=ROOT/"legacy/v5.291/formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88.lean"
PARENT=ROOT/"formal/KUOS/DependentOriginationStandardCanonicalPresentationGapV1_87.lean"
CANDIDATE_BLOB="3b0b345b244e7d9b51b86a6fa1ffba03317f8a43"
ORIGINAL_BLOB="ba6190c2b2f9dac0febfb6357e908e81601c79a1"
PR_PARENT_BLOB="9718e8dcb1e366774374ddb3d084c5a80391d7e0"
REJECTED_R1_BLOB="e555c9eae00f348ef6b5fb7ed4827f0d8ec99a53"
PREVIOUS_R2=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR2V1_88.lean"
PREVIOUS_R2_BLOB="7b81ca36340ee69493df68a7d3671645c2f161e9"
PREVIOUS_R3=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR3V1_88.lean"
PREVIOUS_R3_BLOB="ddf2a7f102d5c111126c85f0d2be5ce49972cb97"
PREVIOUS_R4=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR4V1_88.lean"
PREVIOUS_R4_BLOB="68e2f4f3f8175d06ef22c32662883aeb59214db1"
PREVIOUS_R5=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR5V1_88.lean"
PREVIOUS_R5_BLOB="dd4e165cf61fc04aacedf3376878bba69aa058ac"
PREVIOUS_R6=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR6V1_88.lean"
PREVIOUS_R6_BLOB="a5622716d4d5c7d180f122b67602459fad144af4"
PREVIOUS_R7=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR7V1_88.lean"
PREVIOUS_R7_BLOB="e6801f096bc85b0b0111774c726c081341be81b2"
PREVIOUS_R8=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR8V1_88.lean"
PREVIOUS_R8_BLOB="f37a0a5a166a9906fd13a91127107a028f9ed63d"
PUBLIC=[
    "minimallyScaledSimplex",
    "minimalToChosenSimplexScaling",
    "minimalToChosenSimplexScaling_map",
    "minimalSimplexIntoAttachment",
    "chosenScaledEndpoint",
    "minimalAttachmentFirstProjection",
    "scaledCylinderFirstProjection",
    "simplexScalingToAttachmentArrow",
    "attachmentToSimplexScalingArrow",
    "minimalToChosenSimplexScaling_retractArrow",
    "minimalToChosenSimplexScaling_mem_of_attachment_mem",
    "minimalToChosenSimplexScaling_mem_canonicalGenerated",
    "SimplexScalingEnrichmentIndex",
    "simplexScalingEnrichmentHom",
    "simplexScalingEnrichments",
    "simplexScalingEnrichment_mem",
    "simplexScalingEnrichments_le_canonicalGenerated",
    "simplexScalingEnrichments_le_standardGenerated_of_canonicalGenerators_le",
    "simplexScalingEnrichments_le_standardGenerated_of_canonicalKuuOS_le_standardABC",
    "simplexScalingEnrichments_le_standardGenerated_of_positiveResidual",
    "not_canonicalKuuOS_le_standardABC_of_scalingEnrichment_not_mem",
    "not_standardCanonicalPresentationGapClosed_of_scalingEnrichment_not_mem",
]
PRIVATE=[
    "minimalSimplexIntoAttachment_comp_projection",
    "chosenScaledEndpoint_comp_projection",
]
DECL=re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")
OUT=Path("/tmp/kuuos-v188-r9-22")
def audit():
    verify_inputs()
    raw=CANDIDATE.read_bytes()
    if blob(PREVIOUS_R2.read_bytes())!=PREVIOUS_R2_BLOB:
        raise RuntimeError("V188_R7_PARENT_R2_BLOB_CHANGED")
    if blob(PREVIOUS_R3.read_bytes())!=PREVIOUS_R3_BLOB:
        raise RuntimeError("V188_R7_PARENT_R3_BLOB_CHANGED")
    if blob(PREVIOUS_R4.read_bytes())!=PREVIOUS_R4_BLOB:
        raise RuntimeError("V188_R7_PARENT_R4_BLOB_CHANGED")
    if blob(PREVIOUS_R5.read_bytes())!=PREVIOUS_R5_BLOB:
        raise RuntimeError("V188_R7_PARENT_R5_BLOB_CHANGED")
    if blob(PREVIOUS_R6.read_bytes())!=PREVIOUS_R6_BLOB:
        raise RuntimeError("V188_R7_PARENT_R6_BLOB_CHANGED")
    if blob(PREVIOUS_R7.read_bytes())!=PREVIOUS_R7_BLOB:
        raise RuntimeError("V188_R9_PARENT_R7_BLOB_CHANGED")
    if blob(PREVIOUS_R8.read_bytes())!=PREVIOUS_R8_BLOB:
        raise RuntimeError("V188_R9_PARENT_R8_BLOB_CHANGED")
    if blob(raw)!=CANDIDATE_BLOB or blob(ORIGINAL.read_bytes())!=ORIGINAL_BLOB:
        raise RuntimeError("V188_R9_PROPOSAL_SOURCE_OR_ORIGINAL_CHANGED")
    if blob(HISTORY.read_bytes())!=ORIGINAL_BLOB or blob(PARENT.read_bytes())!=PR_PARENT_BLOB:
        raise RuntimeError("V188_R9_FROZEN_OR_CERTIFIED_PARENT_CHANGED")
    baseline=ORIGINAL.read_text(encoding="utf8")
    r1=baseline.replace(
        "open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22",
        "open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19\nopen KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22"
    ).replace("Delta[","Δ[")
    if blob(r1.encode())!=REJECTED_R1_BLOB:
        raise RuntimeError("V188_R7_REJECTED_R1_RECONSTRUCTION_MISMATCH")
    source3=PREVIOUS_R3.read_text(encoding="utf8")
    old1="""      all_goals simp only [endpointIntoAttachment_ι_zero,
        endpointIntoAttachment_ι_one, SSet.ι₀_fst, SSet.ι₁_fst]
"""
    old2="""      all_goals simp only [scaledEndpointZero, scaledEndpointOne,
        SSet.ι₀_fst, SSet.ι₁_fst]"""
    next2="""      all_goals first
        | exact (SSet.ι₀_fst (Δ[n] : SSet.{u}))
        | exact (SSet.ι₁_fst (Δ[n] : SSet.{u}))"""
    source_ns="KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR3V1_88"
    target_ns="KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR6V1_88"
    if source3.count(source_ns)!=2 or source3.count(old1)!=1 or source3.count(old2)!=1:
        raise RuntimeError("V188_R7_REVIEWED_SOURCE_RECONSTRUCTION_ANCHOR_MISSING")
    predicted=source3.replace(old1,"").replace(old2,next2).replace(source_ns,target_ns)
    if PREVIOUS_R6.read_text(encoding="utf8")!=predicted:
        raise RuntimeError("V188_R7_PARENT_R6_NOT_EXACT_R3_GOAL_GLUING")
    previous=PREVIOUS_R6.read_text(encoding="utf8")
    source_ns="KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR6V1_88"
    next_ns="KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR7V1_88"
    oldblock="""    · apply ScaledSSet.ScaledMap.ext
      fin_cases endpoint <;>
        simp [simplexScalingToAttachmentArrow,
          attachmentToSimplexScalingArrow,
          minimalSimplexIntoAttachment,
          minimalAttachmentFirstProjection,
          chosenScaledEndpoint,
          scaledCylinderFirstProjection,
          Category.assoc]"""
    newblock="""    · apply ScaledSSet.ScaledMap.ext
      change
        (endpointIntoAttachment n i endpoint ≫
          (hornCylinderAttachment n i endpoint).ι) ≫
          CartesianMonoidalCategory.fst _ _ = 𝟙 (Δ[n] : SSet.{u})
      fin_cases endpoint
      · simpa only [endpointIntoAttachment_ι_zero n i, SSet.ι₀_fst]
      · simpa only [endpointIntoAttachment_ι_one n i, SSet.ι₁_fst]"""
    if previous.count(oldblock)!=1 or previous.count(source_ns)!=2:
        raise RuntimeError("V188_R7_REPAIR_ANCHOR_NO_DATA")
    predicted=previous.replace(oldblock,newblock).replace(source_ns,next_ns)
    if PREVIOUS_R7.read_text(encoding="utf8")!=predicted:
        raise RuntimeError("V188_R8_PARENT_R7_NOT_EXACT_R6_REPAIR")
    source7=PREVIOUS_R7.read_text(encoding="utf8")
    ns7="KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR7V1_88"
    ns8="KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR8V1_88"
    old_tactic="""      fin_cases endpoint
      · simpa only [endpointIntoAttachment_ι_zero n i, SSet.ι₀_fst]
      · simpa only [endpointIntoAttachment_ι_one n i, SSet.ι₁_fst]"""
    new_tactic="""      fin_cases endpoint
      · exact
          (congrArg
            (fun f : (Δ[n] : SSet.{u}) ⟶ ((Δ[n] : SSet.{u}) ⊗ Δ[1]) =>
              f ≫ CartesianMonoidalCategory.fst _ _)
            (endpointIntoAttachment_ι_zero n i)).trans
            (SSet.ι₀_fst (Δ[n] : SSet.{u}))
      · exact
          (congrArg
            (fun f : (Δ[n] : SSet.{u}) ⟶ ((Δ[n] : SSet.{u}) ⊗ Δ[1]) =>
              f ≫ CartesianMonoidalCategory.fst _ _)
            (endpointIntoAttachment_ι_one n i)).trans
            (SSet.ι₁_fst (Δ[n] : SSet.{u}))"""
    if source7.count(ns7)!=2 or source7.count(old_tactic)!=1:
        raise RuntimeError("V188_R8_REPAIR_ANCHOR_NO_DATA")
    candidate_from_exact_history=source7.replace(old_tactic,new_tactic).replace(ns7,ns8)
    if PREVIOUS_R8.read_text(encoding="utf8")!=candidate_from_exact_history:
        raise RuntimeError("V188_R9_PARENT_R8_NOT_EXACT_SOURCE_BOUND_R7_REPAIR")
    if not all(t in raw.decode("utf8") for t in (
        "private theorem minimalSimplexIntoAttachment_comp_projection",
        "private theorem chosenScaledEndpoint_comp_projection",
        "exact minimalSimplexIntoAttachment_comp_projection n i endpoint",
        "exact chosenScaledEndpoint_comp_projection sDelta endpoint",
    )):
        raise RuntimeError("V188_R9_SPLIT_RETRACT_SIGNATURE_OR_USE_MISSING")
    masked=mask_lean_comments(raw.decode())
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom|unsafe|native_decide)\b", masked):
        raise RuntimeError("V188_R7_FORBIDDEN_TRUST_MARKER")
    actual=DECL.findall(masked)
    if actual != PUBLIC[:9] + PRIVATE + PUBLIC[9:] or len(PUBLIC)!=22 or len(PRIVATE)!=2:
        raise RuntimeError("V188_R9_DECLARATION_INVENTORY "+repr(actual))
    if not re.fullmatch("[0-9a-f]{40}",os.getenv("SOURCE_HEAD","")):
        raise RuntimeError("V188_R9_SOURCE_HEAD_NO_DATA")
    OUT.mkdir(parents=True,exist_ok=True)
    if any(OUT.iterdir()):
        raise RuntimeError("V188_R9_NOT_APPEND_ONLY")
    r=subprocess.run(["lake","-KleanArgs=-DwarningAsError=true",
        "-KleanArgs=-DsorryAsError=true","build",MODULE],
        text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=4900)
    (OUT/"strict-build.log").write_text(r.stdout)
    lines=r.stdout.splitlines()
    errors=[l for l in lines if l.startswith("error: ")]
    if r.returncode!=0 or errors:
        (OUT/"hold.json").write_text(json.dumps({
          "source_head":os.environ["SOURCE_HEAD"],"candidate_blob":CANDIDATE_BLOB,
          "status":"UNAUTHENTICATED","lean_exit":r.returncode,
          "errors":errors,"memory_admission":False,"merged":False
        },ensure_ascii=False,indent=2)+"\n")
        print("KUUOS_V188_R9_HOLD "+json.dumps({"status":"UNAUTHENTICATED",
           "errors":len(errors),"exit":r.returncode},ensure_ascii=False),flush=True)
        for e in errors[:30]:print(e,flush=True)
        return 2
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v188-r7-audit-") as d:
        f=Path(d)/"all-22.lean"
        f.write_text("import "+MODULE+"\n"+"".join(
            "#print axioms "+MODULE+"."+n+"\n" for n in PUBLIC),encoding="utf8")
        v=subprocess.run(["lake","env","lean","-DwarningAsError=true",
            "-Dweak.sorryAsError=true",str(f)],
            text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=1800)
    (OUT/"axiom-audit.log").write_text(v.stdout)
    if v.returncode!=0:raise RuntimeError("V188_R7_AXIOM_AUDIT_NONZERO "+str(v.returncode))
    used=set()
    for n in PUBLIC:
        full=MODULE+"."+n
        m=re.search(r"'"+re.escape(full)+r"'\s+depends on axioms:\s*\[([^\]]*)\]",v.stdout,re.S)
        if m:used.update(x.strip() for x in m.group(1).split(",") if x.strip())
        elif not re.search(r"'"+re.escape(full)+r"'\s+does not depend on any axioms",v.stdout):
            raise RuntimeError("V188_R7_AXIOM_REPORT_NO_DATA "+n)
    if used-STANDARD_AXIOMS or "sorryAx" in v.stdout:
        raise RuntimeError("V188_R7_UNAUTHORIZED_AXES "+repr(sorted(used)))
    receipt={"kind":"KUUOS_V188_R7_22_STRICT_LEAN_AXIOM_PROPOSAL",
       "source_head":os.environ["SOURCE_HEAD"],
       "candidate_blob":CANDIDATE_BLOB,
       "candidate_sha256":hashlib.sha256(raw).hexdigest(),
       "original_blob":ORIGINAL_BLOB,"rejected_r1_blob":REJECTED_R1_BLOB,
       "pr_parent_blob":PR_PARENT_BLOB,
       "public_declarations":len(PUBLIC),"axioms":sorted(used),
       "errors":0,"warnings":0,"sorryAx":False,
       "lean":"v4.30.0-rc2","mathlib":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
       "original_source_changed":False,"pr_adopted":False,"memory_promoted":False,
       "merge_authority":False}
    (OUT/"receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    print("KUUOS_V188_R9_22_GREEN "+json.dumps(receipt,ensure_ascii=False),flush=True)
    return 0

if __name__=="__main__":
    try: sys.exit(audit())
    except Exception as exc:
        print("KUUOS_V188_R9_FAILURE "+type(exc).__name__+": "+str(exc)[:800],file=sys.stderr)
        sys.exit(3)
