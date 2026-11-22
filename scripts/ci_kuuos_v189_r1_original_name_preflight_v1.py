#!/usr/bin/env python3
"""KuuOS CodeAI v1.89 R1: original-module-name pre-adoption independent strict Lean and 22 public axiom reports.
Research-only. Original source/frozen history/PR remain untouched; never certify by CodeAI alone.
"""
from __future__ import annotations
import hashlib, json, re, os, subprocess, sys, tempfile
from pathlib import Path
from scripts.ci_kuuos_v176_exact_source_audit_v1 import ROOT, STANDARD_AXIOMS, blob, verify_inputs
from scripts.kuuos_lean_mcp_repair_loop_v1 import mask_lean_comments

MODULE="KUOS.DependentOriginationStandardArbitraryScalingWaypointV1_89"
ORIGINAL=ROOT/"formal/KUOS/DependentOriginationStandardArbitraryScalingWaypointV1_89.lean"
FROZEN=ROOT/"legacy/v5.291/formal/KUOS/DependentOriginationStandardArbitraryScalingWaypointV1_89.lean"
CANDIDATE=ROOT/"formal/KUOS/DependentOriginationStandardArbitraryScalingWaypointCodeAICandidateR1V1_89.lean"
PARENT=ROOT/"formal/KUOS/DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88.lean"
ORIGINAL_BLOB="8567232c840a05633f807e75c4684b970ecb7914"
HISTORY_BLOB="f5d06299e825ef784a7df25386b062b80c702f12"
PARENT_BLOB="60283850a5de58e88705735379f208dd31d797df"
CANDIDATE_BLOB="22f858a37cdc8b3be3c624d3d0fface05c3f9019"
NS="KUOS.DependentOriginationStandardArbitraryScalingWaypointCodeAICandidateR1V1_89"
PUBLIC=["arbitrarySimplexScalingPresentation","arbitrarySimplexScalingPresentation_le_canonicalKuuOS","arbitrarySimplexScalingPresentation_le_standardABC_iff","standardArbitraryScalingWaypoint","standardABC_le_arbitraryScalingWaypoint","arbitrarySimplexScalingPresentation_le_waypoint","arbitraryScalingWaypoint_le_upperEnvelope","lowerEnvelope_le_arbitraryScalingWaypoint","arbitraryScalingWaypoint_mem_standardCanonicalInterval","arbitraryScalingWaypoint_sup_canonical_eq_upperEnvelope","standardABC_inf_arbitraryScalingWaypoint","StandardArbitraryScalingObstructionClosed","standardArbitraryScalingObstructionClosed_iff_presentation_le","standardArbitraryScalingObstructionClosed_iff_generators_le","standardArbitraryScalingObstructionClosed_of_canonicalKuuOS_le_standardABC","standardArbitraryScalingObstructionClosed_of_positiveResidual","standardArbitraryScalingObstructionClosed_of_gapClosed","CanonicalBelowStandardAfterArbitraryScaling","canonicalKuuOS_le_standardABC_iff_scalingClosed_and_residual","not_canonicalKuuOS_le_standardABC_of_scalingObstruction_open","not_standardCanonicalPresentationGapClosed_of_scalingObstruction_open","standardCanonicalPresentationGapClosed_iff_reverse_scaling_residual"]
DECL=re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")
OUT=Path("/tmp/kuuos-v189-r1-original-name-22")

def run() -> int:
    verify_inputs()
    if blob(ORIGINAL.read_bytes()) != ORIGINAL_BLOB or blob(FROZEN.read_bytes()) != HISTORY_BLOB:
        raise RuntimeError("V189_R1_HISTORICAL_OR_ORIGINAL_DRIFT")
    if blob(PARENT.read_bytes()) != PARENT_BLOB or blob(CANDIDATE.read_bytes()) != CANDIDATE_BLOB:
        raise RuntimeError("V189_R1_PARENT_OR_CANDIDATE_DRIFT")
    source=mask_lean_comments(CANDIDATE.read_text())
    if DECL.findall(mask_lean_comments(ORIGINAL.read_text())) != PUBLIC or DECL.findall(source) != PUBLIC:
        raise RuntimeError("V189_R1_PUBLIC_SIGNATURE_NAMES_NOT_PRESERVED")
    if CANDIDATE.read_text().count(NS) != 2:
        raise RuntimeError("V189_R1_NAMESPACE_CONTRACT_MISMATCH")
    if CANDIDATE.read_text().replace("KUOS.DependentOriginationStandardArbitraryScalingWaypointCodeAICandidateR1V1_89","KUOS.DependentOriginationStandardArbitraryScalingWaypointV1_89") != ORIGINAL.read_text():
        raise RuntimeError("V189_R1_ORIGINAL_NOT_NAMESPACE_ONLY")
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom|unsafe|native_decide)\b",source):
        raise RuntimeError("V189_R1_TRUST_BYPASS")
    head=os.environ.get("SOURCE_HEAD","")
    if not re.fullmatch("[0-9a-f]{40}",head):
        raise RuntimeError("V189_R1_HEAD_NO_DATA")
    OUT.mkdir(parents=True,exist_ok=True)
    if any(OUT.iterdir()):
        raise RuntimeError("V189_R1_APPEND_ONLY_OUTPUT_CONFLICT")
    b=subprocess.run(["lake","-KleanArgs=-DwarningAsError=true",
      "-KleanArgs=-DsorryAsError=true","build",MODULE],
      capture_output=True,text=True,timeout=5100)
    log=b.stdout+"\n"+b.stderr
    (OUT/"strict-build.log").write_text(log)
    if b.returncode:
        errors=[s for s in log.splitlines() if "error:" in s or "unsolved goals" in s or "timeout" in s or "typeclass instance" in s]
        print("KUUOS_V189_R1_KERNEL_HOLD "+json.dumps({"head":head,"candidate_blob":CANDIDATE_BLOB,
          "returncode":b.returncode,"errors":errors[-40:],"certified":False}),flush=True)
        return 2
    with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v189-r1-axioms-") as d:
        f=Path(d)/"audit.lean"
        f.write_text("import "+MODULE+"\n"+"".join("#print axioms "+MODULE+"."+n+"\n" for n in PUBLIC))
        p=subprocess.run(["lake","env","lean","-DwarningAsError=true","-Dweak.sorryAsError=true",str(f)],
          capture_output=True,text=True,timeout=1800)
    log=p.stdout+"\n"+p.stderr
    (OUT/"axioms.log").write_text(log)
    if p.returncode:
        raise RuntimeError("V189_R1_AXIOM_AUDIT_FAILURE:"+str(p.returncode))
    reports={}
    for name in PUBLIC:
        full=MODULE+"."+name
        m=re.search("'"+re.escape(full)+r"'\s+depends on axioms:\s*\[([^\]]*)\]",log,re.S)
        if m: reports[name]=sorted(x.strip() for x in m.group(1).split(",") if x.strip())
        elif re.search("'"+re.escape(full)+r"'\s+does not depend on any axioms",log): reports[name]=[]
        else: raise RuntimeError("V189_R1_MISSING_AXIOM_REPORT:"+name)
    axioms=set(x for arr in reports.values() for x in arr)
    if axioms-STANDARD_AXIOMS or "sorryAx" in log:
        raise RuntimeError("V189_R1_NONSTANDARD_AXIOM:"+str(sorted(axioms)))
    rec={"kind":"KUUOS_V189_R1_ORIGINAL_NAME_PRE_ADOPTION_22_AXIOM_CERTIFICATE","source_head":head,
      "candidate_blob":CANDIDATE_BLOB,"original_blob":ORIGINAL_BLOB,"parent_blob":PARENT_BLOB,
      "source_sha256":hashlib.sha256(CANDIDATE.read_bytes()).hexdigest(),
      "public_declarations":22,"axioms":sorted(axioms),"errors":0,"warnings":0,"sorryAx":False,
      "lean":"v4.30.0-rc2","mathlib":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
      "preflight_original_name":True,"PR_adopted":False,"memory_promoted":False,"merge_authority":False}
    (OUT/"receipt.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n")
    print("KUUOS_V189_R1_ORIGINAL_NAME_PRE_ADOPTION_GREEN "+json.dumps(rec,ensure_ascii=False),flush=True)
    return 0

if __name__=="__main__":
    try:sys.exit(run())
    except Exception as exc:
        print("KUUOS_V189_R1_KERNEL_HOLD "+str(exc)[:700],file=sys.stderr,flush=True)
        sys.exit(3)
