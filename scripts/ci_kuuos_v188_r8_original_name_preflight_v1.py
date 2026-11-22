#!/usr/bin/env python3
"""CodeAI v1.88 R8 exact original-module-name preflight (research-only).

No PR adoption, no allowlist/root update, no merge authority. Original
source is used only on the isolated preflight branch. Exact namespace
correspondence with the R8 research candidate is required before Lean.
"""
from __future__ import annotations
import hashlib,json,os,re,subprocess,sys,tempfile
from pathlib import Path
from scripts.ci_kuuos_v176_exact_source_audit_v1 import ROOT,STANDARD_AXIOMS,blob,verify_inputs
from scripts.kuuos_lean_mcp_repair_loop_v1 import mask_lean_comments

MODULE="KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88"
ORIGINAL=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88.lean"
R8=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR8V1_88.lean"
HISTORY=ROOT/"legacy/v5.291/formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88.lean"
PARENT=ROOT/"formal/KUOS/DependentOriginationStandardCanonicalPresentationGapV1_87.lean"
ORIGINAL_NAME_BLOB="223a2f9a620af60b71a8be9a3562883c89aa0b72"
R8_BLOB="f37a0a5a166a9906fd13a91127107a028f9ed63d"
FROZEN_BLOB="ba6190c2b2f9dac0febfb6357e908e81601c79a1"
PARENT_BLOB="9718e8dcb1e366774374ddb3d084c5a80391d7e0"
OLD="KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractCodeAICandidateR8V1_88"
NEW="KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88"
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
OUT=Path("/tmp/kuuos-v188-r8-original-name-preflight")
def run():
    verify_inputs()
    original=ORIGINAL.read_bytes()
    candidate=R8.read_bytes()
    if blob(original)!=ORIGINAL_NAME_BLOB or blob(candidate)!=R8_BLOB:
        raise RuntimeError("V188_R8_ORIGINAL_NAME_SOURCE_BLOB_CHANGED")
    if blob(HISTORY.read_bytes())!=FROZEN_BLOB or blob(PARENT.read_bytes())!=PARENT_BLOB:
        raise RuntimeError("V188_R8_FROZEN_OR_PARENT_BLOB_CHANGED")
    s=candidate.decode("utf8")
    if s.count(OLD)!=2 or NEW in s or original.decode("utf8")!=s.replace(OLD,NEW):
        raise RuntimeError("V188_R8_NOT_EXACT_NAMESPACE_ONLY_ADOPTION")
    masked=mask_lean_comments(original.decode("utf8"))
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom|unsafe|native_decide)\b",masked):
        raise RuntimeError("V188_R8_ORIGINAL_NAME_TRUST_BYPASS")
    names=DECL.findall(masked)
    if names!=PUBLIC or len(PUBLIC)!=22:
        raise RuntimeError("V188_R8_ORIGINAL_NAME_DECLARATION_CHANGE "+repr(names))
    head=os.getenv("SOURCE_HEAD","")
    if not re.fullmatch("[a-f0-9]{40}",head):
        raise RuntimeError("V188_R8_ORIGINAL_NAME_HEAD_NO_DATA")
    OUT.mkdir(parents=True,exist_ok=True)
    if any(OUT.iterdir()):
        raise RuntimeError("V188_R8_ORIGINAL_NAME_RECEIPT_ALREADY_EXISTS")
    build=subprocess.run(["lake","-KleanArgs=-DwarningAsError=true",
        "-KleanArgs=-DsorryAsError=true","build",MODULE],
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=4900,text=True)
    (OUT/"strict-build.log").write_text(build.stdout)
    if build.returncode:
        lines=[s for s in build.stdout.splitlines() if s.startswith("error: ")]
        print("V188_R8_ORIGINAL_NAME_HOLD "+json.dumps({"build_exit":build.returncode,
          "error_count":len(lines),"head":head}),flush=True)
        for x in lines[:28]:print(x,flush=True)
        return 2
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v188-r8-original-audit-") as d:
        p=Path(d)/"all-22.lean"
        p.write_text("import "+MODULE+"\n"+"".join("#print axioms "+MODULE+"."+x+"\n" for x in PUBLIC))
        a=subprocess.run(["lake","env","lean","-DwarningAsError=true",
            "-Dweak.sorryAsError=true",str(p)],stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,text=True,timeout=1800)
    (OUT/"axiom-audit.log").write_text(a.stdout)
    if a.returncode: raise RuntimeError("V188_R8_ORIGINAL_NAME_AXIOM_AUDIT_FAILURE "+str(a.returncode))
    used=set()
    for x in PUBLIC:
        full=MODULE+"."+x
        e=re.search(r"'"+re.escape(full)+r"'\s+depends on axioms:\s*\[([^\]]*)\]",a.stdout,re.S)
        if e:used.update(z.strip() for z in e.group(1).split(",") if z.strip())
        elif not re.search(r"'"+re.escape(full)+r"'\s+does not depend on any axioms",a.stdout):
            raise RuntimeError("V188_R8_ORIGINAL_NAME_MISSING_AXIOM_RECEIPT "+x)
    if used-STANDARD_AXIOMS or "sorryAx" in a.stdout:
        raise RuntimeError("V188_R8_ORIGINAL_NAME_UNAUTHORIZED_AXIOMS "+repr(sorted(used)))
    receipt={"kind":"KUUOS_V188_R8_PRE_ADOPTION_ORIGINAL_NAME_22_AXIOMS",
      "source_head":head,"original_name_blob":ORIGINAL_NAME_BLOB,"r8_candidate_blob":R8_BLOB,
      "frozen_blob":FROZEN_BLOB,"parent_blob":PARENT_BLOB,
      "source_sha256":hashlib.sha256(original).hexdigest(),
      "declarations":len(names),"axioms":sorted(used),"errors":0,"warnings":0,"sorryAx":False,
      "lean":"v4.30.0-rc2","mathlib":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
      "preflight_only":True,"adopted_on_PR":False,"merge_authority":False}
    (OUT/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print("KUUOS_V188_R8_ORIGINAL_NAME_GREEN "+json.dumps(receipt,ensure_ascii=False),flush=True)
    return 0
if __name__=="__main__":
    try:sys.exit(run())
    except Exception as exc:
        print("KUUOS_V188_R8_ORIGINAL_NAME_HOLD "+str(exc)[:600],file=sys.stderr)
        sys.exit(3)
