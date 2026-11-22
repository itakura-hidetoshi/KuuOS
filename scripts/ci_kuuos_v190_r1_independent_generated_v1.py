#!/usr/bin/env python3
"""Independent exact-source kernel verification for actual MCP CodeAI generated v1.90 R1.
Only runs after successful same-workflow upstream; no source PR or Memory mutation.
"""
from __future__ import annotations
import hashlib,json,os,re,subprocess,sys,tempfile
from pathlib import Path
from scripts.ci_kuuos_v176_exact_source_audit_v1 import ROOT,STANDARD_AXIOMS,blob,verify_inputs
from scripts.kuuos_lean_mcp_repair_loop_v1 import mask_lean_comments
from scripts.check_kuuos_lean_mcp_fullsource_v1 import git_blob

UP=Path("/tmp/kuuos-v190-r1-upstream")
OUT=Path("/tmp/kuuos-v190-r1-independent")
ORIG=ROOT/"formal/KUOS/DependentOriginationSingleTriangleScalingFiltrationV1_90.lean"
CAND=ROOT/"formal/KUOS/DependentOriginationSingleTriangleScalingFiltrationCodeAICandidateR1V1_90.lean"
NS0="KUOS.DependentOriginationSingleTriangleScalingFiltrationV1_90"
NS1="KUOS.DependentOriginationSingleTriangleScalingFiltrationCodeAICandidateR1V1_90"
ORIG_BLOB="d6a76712776b4a1b289b89bd691fa6213f8d36ce"
PUBLIC=["singleTriangleScaling","minimalScaling_le_singleTriangleScaling","minimalToSingleTriangleScaling","SingleTriangleScalingEnrichmentIndex","singleTriangleScalingEnrichmentHom","singleTriangleScalingEnrichments","singleTriangleScalingEnrichment_mem","singleTriangleScalingEnrichments_le_simplexScalingEnrichments","finiteTriangleScaling","finiteTriangleScaling_empty","minimalScaling_le_finiteTriangleScaling","minimalToFiniteTriangleScaling","finiteTriangleInsertEnrichment","singleTrianglePushoutScaling_eq_finiteInsert","finiteTriangleInsertEnrichment_mem_llp","minimalToFiniteTriangleScaling_mem_llp","chosenThinTriangles","mem_chosenThinTriangles","minimalScaling_le_any","finiteTriangleScaling_chosenThinTriangles_eq","minimalToChosenSimplexScaling_mem_llp_of_singleTriangles","simplexScalingEnrichments_le_singleTriangleGenerated","singleTriangleScalingEnrichments_le_arbitraryGenerated","singleTriangle_presentation_eq_arbitraryScalingPresentation","standardArbitraryScalingObstructionClosed_iff_singleTriangles","not_standardArbitraryScalingObstructionClosed_of_singleTriangle_not_mem","not_standardCanonicalPresentationGapClosed_of_singleTriangle_not_mem"]
DECL=re.compile(r"(?m)^(?:@\[[^\]]+\]\s*)?(?:(?:private|noncomputable|protected|partial|unsafe)\s+)*(?:theorem|lemma|def|abbrev|structure|class|instance)\s+([^\s(:]+)")

def main():
    verify_inputs()
    if OUT.exists() and list(OUT.iterdir()):raise RuntimeError("NO_APPEND_ONLY_OVERWRITE")
    OUT.mkdir(parents=True,exist_ok=True)
    baseline=ORIG.read_text()
    if blob(baseline.encode())!=ORIG_BLOB:raise RuntimeError("V190_ORIGINAL_DRIFT")
    r=json.loads((UP/"receipt.json").read_text())
    nr=json.loads((UP/"native-codeai-receipt.json").read_text())
    candidate=(UP/"candidate_R1_generated.lean").read_text()
    old="open Simplicial\n"
    new="open Simplicial\nopen KUOS.DependentOriginationNativeInfinityTwoScaledV1_19\n"
    if baseline.count(old)!=1 or baseline.count(NS0)!=2:
        raise RuntimeError("V190_R1_AMBIGUOUS_NAMESPACE_SOURCE")
    expected=baseline.replace(old,new).replace(NS0,NS1)
    if candidate!=expected:
        raise RuntimeError("V190_R1_NOT_ACTUAL_ERROR_GUIDED_ONE_OPEN_FIX")
    if (r["status"]!="LOCAL_TYPED_MCP_NATIVE_CODEAI_AND_LEAN_GREEN_UNADOPTED"
        or r["mcp_status"]!="ACTUAL_TYPED_PINNED_SOURCE_DIAGNOSTICS"
        or r["codeai_native_status"]!="ACTUAL_NATIVE_CANDIDATE_AND_REJECT"
        or not r["full_import_closure_captured"] or not r["source_unchanged"]):
        raise RuntimeError("V190_R1_ACTUAL_MCP_PROVENANCE_NOT_GREEN")
    if (git_blob(candidate.encode())!=r["candidate_git_blob"] or
        nr["candidate_source_blob"]!=r["candidate_git_blob"] or
        nr["boundary_statuses"]!=["CANDIDATE","REJECT"] or
        nr["proof_certified_by_codeai"] or nr["memory_admission"] or
        nr["git_or_merge_authority"]):
        raise RuntimeError("V190_R1_NATIVE_CANDIDATE_IDENTITY_OR_AUTHORITY")
    names=DECL.findall(mask_lean_comments(candidate))
    if names!=PUBLIC or DECL.findall(mask_lean_comments(baseline))!=PUBLIC:
        raise RuntimeError("V190_R1_PUBLIC_DECLARATIONS_NOT_PRESERVED")
    if re.search(r"(?m)^\s*(?:sorry|admit|axiom|unsafe|native_decide)\b",
                 mask_lean_comments(candidate)):
        raise RuntimeError("V190_R1_TRUST_BYPASS")
    if CAND.exists():raise RuntimeError("V190_R1_CANDIDATE_COMMITTED_BEFORE_VERIFICATION")
    try:
        CAND.write_text(candidate)
        cp=subprocess.run(["lake","-KleanArgs=-DwarningAsError=true",
                           "-KleanArgs=-DsorryAsError=true","build",NS1],
            capture_output=True,text=True,cwd=ROOT,timeout=4800)
        log=cp.stdout+"\n"+cp.stderr
        (OUT/"strict-build.log").write_text(log)
        if cp.returncode:
            print("KUUOS_V190_R1_INDEPENDENT_HOLD "+json.dumps({"returncode":cp.returncode,
              "errors":[x for x in log.splitlines() if "error:" in x][:35]}),flush=True)
            return 2
        with tempfile.TemporaryDirectory(dir=ROOT,prefix=".v190-r1-axioms-") as td:
            audit=Path(td)/"audit.lean"
            audit.write_text("import "+NS1+"\n"+
                "".join("#print axioms "+NS1+"."+n+"\n" for n in PUBLIC))
            proc=subprocess.run(["lake","env","lean","-DwarningAsError=true",
                  "-Dweak.sorryAsError=true",str(audit)],
                 cwd=ROOT,capture_output=True,text=True,timeout=1800)
        axiomslog=proc.stdout+"\n"+proc.stderr
        (OUT/"axioms.log").write_text(axiomslog)
        if proc.returncode:raise RuntimeError("V190_R1_INDEPENDENT_AXIOM_AUDIT_FAILED")
        found,ax={},set()
        for n in PUBLIC:
            full=NS1+"."+n
            m=re.search("'"+re.escape(full)+r"'\s+depends on axioms:\s*\[([^\]]*)\]",axiomslog,re.S)
            if m: v=sorted(a.strip() for a in m.group(1).split(",") if a.strip())
            elif re.search("'"+re.escape(full)+r"'\s+does not depend on any axioms",axiomslog):v=[]
            else:raise RuntimeError("V190_R1_MISSING_AXIOM_REPORT:"+n)
            found[n]=v
            ax.update(v)
        if ax-STANDARD_AXIOMS or "sorryAx" in axiomslog:
            raise RuntimeError("V190_R1_NONSTANDARD_AXIOM_OR_SORRY")
        receipt={"kind":"KUUOS_V190_R1_FROM_REAL_MCP_INDEPENDENT_27_LEAN_AXIOMS",
            "source_head":os.environ.get("SOURCE_HEAD",""),
            "original_blob":ORIG_BLOB,"generated_candidate_blob":r["candidate_git_blob"],
            "candidate_sha256":hashlib.sha256(candidate.encode()).hexdigest(),
            "declarations":27,"axioms":sorted(ax),"sorryAx":False,"errors":0,"warnings":0,
            "lean":"v4.30.0-rc2","mathlib":"5450b53e5ddc75d46418fabb605edbf36bd0beb6",
            "source_has_exact_diagnostic_guided_namespace_fix":True,
            "actual_mcp_diagnostics_received":True,"native_codeai_source_bound":True,
            "independent_four_family":"NO_DATA","MemoryOS_promoted":False,
            "PR_adopted":False,"merge_authority":False}
        (OUT/"receipt.json").write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
        print("KUUOS_V190_R1_INDEPENDENT_LEAN_GREEN "+json.dumps(receipt,sort_keys=True),flush=True)
        return 0
    finally:
        CAND.unlink(missing_ok=True)

if __name__=="__main__":
    try:sys.exit(main())
    except Exception as ex:
        print("KUUOS_V190_R1_INDEPENDENT_HOLD "+type(ex).__name__+": "+str(ex)[:1000],file=sys.stderr)
        sys.exit(3)
