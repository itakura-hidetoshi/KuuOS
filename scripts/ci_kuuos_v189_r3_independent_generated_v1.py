#!/usr/bin/env python3
"""Independent job: verify actual MCP-generated v1.89 R3 candidate, exact source and 22 Lean axioms.

Downloaded artifact must come from same GitHub workflow, upstream job completed
successfully; compare exact source bytes and provenance. Does not certify
other verifier families, update MemoryOS or touch the source PR.
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
from scripts.ci_kuuos_v176_exact_source_audit_v1 import ROOT, STANDARD_AXIOMS, blob, verify_inputs
from scripts.kuuos_lean_mcp_repair_loop_v1 import mask_lean_comments
from scripts.check_kuuos_lean_mcp_fullsource_v1 import git_blob
BASE=Path("/tmp/kuuos-v189-r3-upstream")
OUT=Path("/tmp/kuuos-v189-r3-independent")
R2="formal/KUOS/DependentOriginationStandardArbitraryScalingWaypointCodeAICandidateR2V1_89.lean"
R3="formal/KUOS/DependentOriginationStandardArbitraryScalingWaypointCodeAICandidateR3V1_89.lean"
NS2="KUOS.DependentOriginationStandardArbitraryScalingWaypointCodeAICandidateR2V1_89"
NS3="KUOS.DependentOriginationStandardArbitraryScalingWaypointCodeAICandidateR3V1_89"
R2_BLOB="556208d79118b5b8f332e7fc49ba3657c15b4c20"
OLD="  simpa [arbitrarySimplexScalingPresentation.{u}, standardABCPresentation.{u},\n"
NEW="  simpa [arbitrarySimplexScalingPresentation, standardABCPresentation,\n"
PUBLIC=[
"arbitrarySimplexScalingPresentation",
"arbitrarySimplexScalingPresentation_le_canonicalKuuOS",
"arbitrarySimplexScalingPresentation_le_standardABC_iff",
"standardArbitraryScalingWaypoint",
"standardABC_le_arbitraryScalingWaypoint",
"arbitrarySimplexScalingPresentation_le_waypoint",
"arbitraryScalingWaypoint_le_upperEnvelope",
"lowerEnvelope_le_arbitraryScalingWaypoint",
"arbitraryScalingWaypoint_mem_standardCanonicalInterval",
"arbitraryScalingWaypoint_sup_canonical_eq_upperEnvelope",
"standardABC_inf_arbitraryScalingWaypoint",
"StandardArbitraryScalingObstructionClosed",
"standardArbitraryScalingObstructionClosed_iff_presentation_le",
"standardArbitraryScalingObstructionClosed_iff_generators_le",
"standardArbitraryScalingObstructionClosed_of_canonicalKuuOS_le_standardABC",
"standardArbitraryScalingObstructionClosed_of_positiveResidual",
"standardArbitraryScalingObstructionClosed_of_gapClosed",
"CanonicalBelowStandardAfterArbitraryScaling",
"canonicalKuuOS_le_standardABC_iff_scalingClosed_and_residual",
"not_canonicalKuuOS_le_standardABC_of_scalingObstruction_open",
"not_standardCanonicalPresentationGapClosed_of_scalingObstruction_open",
"standardCanonicalPresentationGapClosed_iff_reverse_scaling_residual"]
DECL=re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|def|lemma|structure|instance|abbrev)\s+([^\s(:]+)")

def main():
    verify_inputs()
    if OUT.exists() and any(OUT.iterdir()):
        raise RuntimeError("APPEND_ONLY_RUN_OUTPUT_ALREADY_EXISTS")
    OUT.mkdir(parents=True,exist_ok=True)
    base_source=(ROOT/R2).read_text()
    if blob(base_source.encode())!=R2_BLOB:
        raise RuntimeError("R2_IMMUTABLE_SOURCE_CHANGED")
    receipt=json.loads((BASE/"receipt.json").read_text())
    native=json.loads((BASE/"codeai-native-receipt.json").read_text())
    generated=(BASE/"candidate_R3_generated.lean").read_text()
    expect=base_source.replace(OLD,NEW).replace(NS2,NS3)
    if base_source.count(OLD)!=1 or base_source.count(NS2)!=2 or generated!=expect:
        raise RuntimeError("R3_NOT_EXACT_DIAGNOSTIC_GENERATION")
    if (receipt["status"]!="LOCAL_REAL_MCP_CODEAI_AND_DIRECT_LEAN_GREEN_UNADOPTED"
        or not receipt["actual_mcp_called"] or not receipt["fullsource_ready"]
        or not receipt["source_restored"]
        or receipt["actual_verification_guided_regeneration_v01"]!="NO_DATA_NO_SEALED_EXECUTION_LINEAGE"):
        raise RuntimeError("SOURCE_MCP_OBSERVATION_OR_BOUNDARY_MISSING")
    if receipt["R3_source_git_blob"]!=git_blob(generated.encode()):
        raise RuntimeError("R3_ARTIFACT_GIT_BLOB_MISMATCH")
    if (native["candidate_source_blob"]!=receipt["R3_source_git_blob"]
        or native["boundary_statuses"]!=["CANDIDATE","REJECT"]
        or native["algorithmic_candidate_from_actual_mcp_feedback"] is not True
        or native["proof_certified_by_codeai"] or native["memory_admission"]):
        raise RuntimeError("NATIVE_CODEAI_RECEIPT_NOT_SOURCE_BOUND")
    if (DECL.findall(mask_lean_comments(base_source))!=PUBLIC or
        DECL.findall(mask_lean_comments(generated))!=PUBLIC):
        raise RuntimeError("R3_DECLARATION_NAMES_CHANGED")
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom|unsafe|native_decide)\b",
                  mask_lean_comments(generated)):
        raise RuntimeError("TRUST_BYPASS_IN_GENERATED_CANDIDATE")
    path=ROOT/R3
    if path.exists():
        raise RuntimeError("R3_PATH_MUST_BE_ABSENT_IN_COMMITTED_SOURCE")
    try:
        path.write_text(generated,encoding="utf8")
        build=subprocess.run(["lake","-KleanArgs=-DwarningAsError=true",
            "-KleanArgs=-DsorryAsError=true","build",NS3],
            cwd=ROOT,capture_output=True,text=True,timeout=4900)
        log=build.stdout+"\n"+build.stderr
        (OUT/"strict-build.log").write_text(log)
        if build.returncode:
            print("R3_INDEPENDENT_LEAN_FAILURE "+json.dumps({
              "returncode":build.returncode,
              "diagnostics":[x for x in log.splitlines() if "error:" in x][-30:]}),flush=True)
            return 2
        with tempfile.TemporaryDirectory(dir=ROOT,prefix=".kuuos-v189-r3-axioms-") as folder:
            audit=Path(folder)/"audit.lean"
            audit.write_text("import "+NS3+"\n"+
               "".join("#print axioms "+NS3+"."+name+"\n" for name in PUBLIC))
            check=subprocess.run(["lake","env","lean","-DwarningAsError=true",
                "-Dweak.sorryAsError=true",str(audit)],
                cwd=ROOT,capture_output=True,text=True,timeout=1800)
        output=check.stdout+"\n"+check.stderr
        (OUT/"axiom-audit.log").write_text(output)
        if check.returncode:
            print("R3_INDEPENDENT_AXIOM_SCRIPT_FAILURE "+str(check.returncode),flush=True)
            return 2
        reports,used={},set()
        for name in PUBLIC:
            key=NS3+"."+name
            m=re.search(r"'"+re.escape(key)+r"'\s+depends on axioms:\s*\[([^\]]*)\]",output,re.S)
            if m:
                axioms=sorted(x.strip() for x in m.group(1).split(",") if x.strip())
            elif re.search(r"'"+re.escape(key)+r"'\s+does not depend on any axioms",output):
                axioms=[]
            else:
                raise RuntimeError("MISSING_AXIOM_REPORT:"+key)
            used.update(axioms)
            reports[name]=axioms
        if used-STANDARD_AXIOMS or "sorryAx" in output:
            raise RuntimeError("NONSTANDARD_AXIOMS:"+str(sorted(used-STANDARD_AXIOMS)))
        result={"kind":"KUUOS_V189_R3_FROM_REAL_MCP_INDEPENDENT_FIXED_LEAN_22_AXIOMS",
          "verified_exact_execution_head":os.environ.get("SOURCE_HEAD",""),
          "candidate_blob":git_blob(generated.encode()),"candidate_sha256":hashlib.sha256(generated.encode()).hexdigest(),
          "R2_source_blob":R2_BLOB,"public_declarations":len(reports),
          "axioms":sorted(used),"errors":0,"warnings":0,"sorryAx":False,
          "lean":"v4.30.0-rc2","mathlib":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
          "local_mcp_provenance_preserved":True,
          "actual_codeai_native_candidate_receipt":True,"unadmitted_four_family_ensemble":True,
          "PR_adopted":False,"memory_promoted":False,"merge_authority":False}
        (OUT/"receipt.json").write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
        print("KUUOS_V189_R3_INDEPENDENT_LEAN_GREEN "+json.dumps(result,ensure_ascii=False),flush=True)
        return 0
    finally:
        path.unlink(missing_ok=True)

if __name__=="__main__":
    try:sys.exit(main())
    except Exception as exc:
        print("KUUOS_V189_R3_INDEPENDENT_HOLD "+type(exc).__name__+": "+str(exc)[:800],file=sys.stderr)
        sys.exit(3)
