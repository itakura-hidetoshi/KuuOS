#!/usr/bin/env python3
"""KuuOS CodeAI v1.88 R2: exact-source pinned Strict Lean + 22 declaration axiom audit.

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

MODULE="KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR2V1_88"
CANDIDATE=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR2V1_88.lean"
ORIGINAL=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88.lean"
HISTORY=ROOT/"legacy/v5.291/formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88.lean"
PARENT=ROOT/"formal/KUOS/DependentOriginationStandardCanonicalPresentationGapV1_87.lean"
CANDIDATE_BLOB="7b81ca36340ee69493df68a7d3671645c2f161e9"
ORIGINAL_BLOB="ba6190c2b2f9dac0febfb6357e908e81601c79a1"
PR_PARENT_BLOB="9718e8dcb1e366774374ddb3d084c5a80391d7e0"
REJECTED_R1_BLOB="e555c9eae00f348ef6b5fb7ed4827f0d8ec99a53"
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
DECL=re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")
OUT=Path("/tmp/kuuos-v188-r2-22")
def audit():
    verify_inputs()
    raw=CANDIDATE.read_bytes()
    if blob(raw)!=CANDIDATE_BLOB or blob(ORIGINAL.read_bytes())!=ORIGINAL_BLOB:
        raise RuntimeError("V188_R2_PROPOSAL_SOURCE_OR_ORIGINAL_CHANGED")
    if blob(HISTORY.read_bytes())!=ORIGINAL_BLOB or blob(PARENT.read_bytes())!=PR_PARENT_BLOB:
        raise RuntimeError("V188_R2_FROZEN_OR_CERTIFIED_PARENT_CHANGED")
    baseline=ORIGINAL.read_text(encoding="utf8")
    r1=baseline.replace(
        "open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22",
        "open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19\nopen KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22"
    ).replace("Delta[","Δ[")
    if blob(r1.encode())!=REJECTED_R1_BLOB:
        raise RuntimeError("V188_R2_REJECTED_R1_RECONSTRUCTION_MISMATCH")
    masked=mask_lean_comments(raw.decode())
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom|unsafe|native_decide)\b", masked):
        raise RuntimeError("V188_R2_FORBIDDEN_TRUST_MARKER")
    actual=DECL.findall(masked)
    if actual!=PUBLIC or len(PUBLIC)!=22:
        raise RuntimeError("V188_R2_DECLARATION_INVENTORY "+repr(actual))
    if not re.fullmatch("[0-9a-f]{40}",os.getenv("SOURCE_HEAD","")):
        raise RuntimeError("V188_R2_SOURCE_HEAD_NO_DATA")
    OUT.mkdir(parents=True,exist_ok=True)
    if any(OUT.iterdir()):
        raise RuntimeError("V188_R2_NOT_APPEND_ONLY")
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
        print("KUUOS_V188_R2_HOLD "+json.dumps({"status":"UNAUTHENTICATED",
           "errors":len(errors),"exit":r.returncode},ensure_ascii=False),flush=True)
        for e in errors[:30]:print(e,flush=True)
        return 2
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v188-r2-audit-") as d:
        f=Path(d)/"all-22.lean"
        f.write_text("import "+MODULE+"\n"+"".join(
            "#print axioms "+MODULE+"."+n+"\n" for n in PUBLIC),encoding="utf8")
        v=subprocess.run(["lake","env","lean","-DwarningAsError=true",
            "-Dweak.sorryAsError=true",str(f)],
            text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=1800)
    (OUT/"axiom-audit.log").write_text(v.stdout)
    if v.returncode!=0:raise RuntimeError("V188_R2_AXIOM_AUDIT_NONZERO "+str(v.returncode))
    used=set()
    for n in PUBLIC:
        full=MODULE+"."+n
        m=re.search(r"'"+re.escape(full)+r"'\s+depends on axioms:\s*\[([^\]]*)\]",v.stdout,re.S)
        if m:used.update(x.strip() for x in m.group(1).split(",") if x.strip())
        elif not re.search(r"'"+re.escape(full)+r"'\s+does not depend on any axioms",v.stdout):
            raise RuntimeError("V188_R2_AXIOM_REPORT_NO_DATA "+n)
    if used-STANDARD_AXIOMS or "sorryAx" in v.stdout:
        raise RuntimeError("V188_R2_UNAUTHORIZED_AXES "+repr(sorted(used)))
    receipt={"kind":"KUUOS_V188_R2_22_STRICT_LEAN_AXIOM_PROPOSAL",
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
    print("KUUOS_V188_R2_22_GREEN "+json.dumps(receipt,ensure_ascii=False),flush=True)
    return 0

if __name__=="__main__":
    try: sys.exit(audit())
    except Exception as exc:
        print("KUUOS_V188_R2_FAILURE "+type(exc).__name__+": "+str(exc)[:800],file=sys.stderr)
        sys.exit(3)
