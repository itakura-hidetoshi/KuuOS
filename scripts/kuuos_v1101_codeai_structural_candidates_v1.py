#!/usr/bin/env python3
"""KuuOS CodeAI exact-HEAD v1.101 type/universe structural repair portfolio.

Read-only from Git; only temporarily edits source bytes in an isolated Actions
checkout and always restores originals. Independently compiles every proposal
with fixed Lean. CodeAI candidate generation is NOT theorem certification.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile
import time
import urllib.request

from runtime import kuuos_codeai_intent_repository_observation_envelope_v0_1 as obs
from runtime import kuuos_codeai_autonomous_unified_diff_candidates_v0_1 as diff
from runtime import kuuos_codeai_candidate_patch_envelope_v0_1 as patch
from scripts.check_kuuos_lean_mcp_fullsource_v1 import git_blob, sha256, imports_of, declarations_of

ROOT = Path(__file__).resolve().parents[1]
REPO = "itakura-hidetoshi/KuuOS"
TARGET = "formal/KUOS/DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101.lean"
MODULE = "KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101"
ORIGINAL_BLOB = "dfc083198b2fdbb29adf64106785b5d7f98ab4af"
PROMOTED_BLOB = "14bdc82293c14a367d9d7572ffb7b41c85eccdfe"
PREFIX = "open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100\n"


def require_event() -> tuple[str,str]:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    if event.get("number") != 3522 or event.get("repository",{}).get("full_name") != REPO:
        raise RuntimeError("exact parent PR event required")
    pr = event["pull_request"]
    source_head = pr["head"]["sha"]
    branch = pr["head"]["ref"]
    url = "https://api.github.com/repos/"+REPO+"/git/commits/"+source_head
    headers={"Accept":"application/vnd.github+json","User-Agent":"KuuOS-CodeAI-v1101"}
    token=os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("authenticated GitHub API token required for exact source/tree observation")
    headers["Authorization"]="Bearer "+token
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req,timeout=30) as response:
        data = json.load(response)
    tree = data.get("tree",{}).get("sha")
    if data.get("sha") != source_head or not isinstance(tree,str) or not re.fullmatch("[a-f0-9]{40}",tree):
        raise RuntimeError("exact GitHub source/tree unverified")
    return source_head,branch,tree


def replace_once(source: str, old: str, new: str, name: str) -> str:
    occurrences = source.count(old)
    if occurrences != 1:
        raise RuntimeError(f"v1.101 source drift: {name}: {occurrences}")
    return source.replace(old, new, 1)


def replace_once(source: str, old: str, new: str, label: str) -> str:
    if source.count(old) != 1:
        raise RuntimeError("v1.101 exact source drift: "+label)
    return source.replace(old,new,1)


def replace_once(source: str, old: str, new: str, label: str) -> str:
    n = source.count(old)
    if n != 1:
        raise RuntimeError(f"v1.101 exact source drift {label}: {n}")
    return source.replace(old, new, 1)


def variants(source: str) -> dict[str,str]:
    """Full-source namespace/Type-A RLP structural candidates.

    v1.100 defines the NatNormalizedDuskinCocycle TYPE in an imported
    namespace, whereas v1.101 defines TypeADistinguishedZero and its
    theorems under a *local* namespace with the same short suffix.
    Lean's dot projection searches the imported type's namespace and fails.
    Never change assumptions, imports, theorem names, or introduce axioms.
    """
    if source.count(PREFIX) != 1:
        raise RuntimeError("v1.101 source namespace mismatch")
    localPrefix = (
        "KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101."
        "NatNormalizedDuskinCocycle."
    )
    scope=source
    # Fix only exact declarations in their actual v1.101 namespace.
    repairs=(
        ("(zero n).TypeADistinguishedZero i",
         "TypeADistinguishedZero (zero n) i"),
        ("C.TypeADistinguishedZero i","TypeADistinguishedZero C i"),
        ("C.distinguishedZero_of_toSimplexMap_scaled_standardTypeA i",
         "distinguishedZero_of_toSimplexMap_scaled_standardTypeA C i"),
        ("C.toSimplexMap_scaled_standardTypeA_of_distinguishedZero i",
         "toSimplexMap_scaled_standardTypeA_of_distinguishedZero C i"),
        ("cocycle.TypeADistinguishedZero g.i",
         localPrefix+"TypeADistinguishedZero cocycle g.i"),
        ("K.cocycle.toSimplexMap_scaled_standardTypeA_of_distinguishedZero\n      g.i K.distinguished_zero",
         localPrefix+"toSimplexMap_scaled_standardTypeA_of_distinguishedZero\n"
         "      K.cocycle g.i K.distinguished_zero"),
    )
    expected_counts=[1,3,1,1,1,1]
    for (old,new),expected in zip(repairs,expected_counts):
        count=scope.count(old)
        if count!=expected:
            raise RuntimeError(f"v1.101 scope source drift {old}: {count}")
        scope=scope.replace(old,new)
    rlpOld=(
        "  rw [MorphismProperty.rlp_ofHoms_iff_hasLiftingProperty\n"
        "    StandardTypeAHornGeneratorIndex]\n"
        "  intro g\n"
        "  exact\n"
        "    natDoubleDelooping_hasLiftingProperty_standardTypeA_of_cocycleCompletions\n"
        "      g (H g)"
    )
    rlpNew=(
        "  intro X Y g hg\n"
        "  cases hg with\n"
        "  | mk i =>\n"
        "      exact natDoubleDelooping_hasLiftingProperty_standardTypeA_of_cocycleCompletions\n"
        "        i (H i)"
    )
    withRlp=replace_once(scope,rlpOld,rlpNew,"pinned mathlib ofHoms recursor")
    facOld=(
        "  apply ScaledSSet.ScaledMap.ext\n"
        "  simpa [standardTypeAScaledHornGeneratorHom, toLift] using K.restrict"
    )
    fac1=(
        "  apply ScaledSSet.ScaledMap.ext\n"
        "  simpa only [standardTypeAScaledHornGeneratorHom, toLift] using K.restrict"
    )
    fac2=(
        "  apply ScaledSSet.ScaledMap.ext\n"
        "  change ((Λ[g.n,g.i].ι : (Λ[g.n,g.i] : SSet) ⟶ (Δ[g.n] : SSet)) ≫\n"
        "    K.cocycle.toSimplexMap) = f.map\n"
        "  exact K.restrict"
    )
    # Round 2: IsScaledMap is NOT declared by the opened v1.19/v1.21
    # namespaces. Exact source is v1.22; import is transitive through v1.49.
    # Adding the local open changes neither theorem assumptions nor imports.
    # Distinguish the primary scoping error from downstream proof issues.
    openV122="open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22\n"
    def with_open(t: str) -> str:
        return replace_once(t, PREFIX, PREFIX+openV122, "open pinned v1.22 IsScaledMap")
    candidateScope=with_open(scope)
    candidateRlp=with_open(withRlp)
    candidateFacSimp=with_open(replace_once(withRlp,facOld,fac1,"fac simp only"))
    candidateFacChange=with_open(replace_once(withRlp,facOld,fac2,"fac direct cocycle"))
    return {
        "round1-local-NatCocycle-namespace":scope,
        "round1-namespace-and-RLP-family":withRlp,
        "round1-namespace-RLP-fac-simpa":replace_once(withRlp,facOld,fac1,"fac simp only"),
        "round1-namespace-RLP-fac-change":replace_once(withRlp,facOld,fac2,"fac direct cocycle"),
        "round2-open-IsScaledMap-local-scope":candidateScope,
        "round2-open-IsScaledMap-RLP":candidateRlp,
        "round2-open-IsScaledMap-fac-simpa":candidateFacSimp,
        "round2-open-IsScaledMap-fac-change":candidateFacChange,
    }


def read_example(filename: str) -> dict:
    return json.loads((ROOT/"examples"/filename).read_text(encoding="utf-8"))


def source_observation(head: str,branch: str,tree: str,source:bytes) -> dict:
    sample = read_example("codeai_intent_repository_observation_envelope_v0_1.json")
    t = int(time.time())
    intent = deepcopy(sample["intent_packet"])
    intent.update({
        "intent_id":"kuuos-v1101-typed-zero-"+head[:12],
        "source_actor_id":"codeai-proof-research",
        "source_channel":"github-parent-strict-lean-log",
        "requirements":["repair v1.101 typed Nat 2-cells and syntax without changing theorem statements"],
        "assumptions":["CodeAI proposals require pinned Lean4 direct check and independent CI"],
        "unresolved_questions":[],
        "preserved_invariants":["same root", "theorem statements unchanged", "no sorry or new axiom"],
        "forbidden_changes":["no theorem weakening", "no main merge", "no legacy changes"],
        "success_criteria":["exact source-bound candidate audit only"],
        "intent_created_epoch":t,
        "prior_intent_digests":[],
        "intent_provenance_confirmed":True,
    })
    intent = obs.seal(intent,obs.INTENT_DIGEST_FIELD)
    paths=[TARGET,"formal/KUOS/DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100.lean",
           "lean-toolchain","lake-manifest.json"]
    if any(not (ROOT/x).is_file() for x in paths):
        raise RuntimeError("required observed predecessor missing")
    toolchain=(ROOT/"lean-toolchain").read_text().strip()
    if toolchain!="leanprover/lean4:v4.30.0-rc2":
        raise RuntimeError("Lean pin changed")
    manifest=json.loads((ROOT/"lake-manifest.json").read_text())
    pinned=[x for x in manifest["packages"] if x.get("name")=="mathlib"]
    if len(pinned)!=1 or pinned[0].get("rev")!="5450b53e5ddc75d46418fabb605edbf36bd0beb6":
        raise RuntimeError("mathlib pin changed")
    repo = deepcopy(sample["repository_observation"])
    repo.update({
        "repository_full_name":REPO,
        "source_commit_sha":head,
        "source_branch":branch,
        "tree_digest":tree,
        "dependency_lock_digest":sha256((ROOT/"lake-manifest.json").read_bytes()),
        "toolchain_digest":"lean-4.30.0-rc2-python-3.12",
        "toolchain_supported":True,
        "observed_paths":paths,
        "unavailable_paths":[],
        "declared_path_count":len(paths),
        "baseline_check_digests":["v1101-exact-blob:"+git_blob(source),"import-v199:"+git_blob((ROOT/paths[1]).read_bytes())],
        "baseline_checks_complete":True,
        "code_owner_scope_digest":"repo-owner:"+REPO,
        "crosses_unowned_boundary":False,
        "observation_started_epoch":t,
        "observation_completed_epoch":int(time.time()),
        "session_id":"v1101-"+head[:16],
        "nonce_digest":hashlib.sha256((head+":v1101-actual").encode()).hexdigest(),
        "prior_session_ids":[],
        "prior_nonce_digests":[],
        "prior_observation_digests":[],
    })
    repo=obs.seal(repo,obs.REPOSITORY_OBSERVATION_DIGEST_FIELD)
    policy=deepcopy(sample["observation_policy"])
    policy.update({
        "expected_repository_full_name":REPO,
        "expected_source_commit_sha":head,
        "allowed_source_branches":[branch],
        "supported_toolchain_digests":["lean-4.30.0-rc2-python-3.12"],
        "require_complete_baseline":True,
        "require_code_owner_scope":True,
        "allow_partial_observation":False,
    })
    policy=obs.seal(policy,obs.POLICY_DIGEST_FIELD)
    result=obs.build_codeai_intent_repository_observation_envelope(
        intent_packet=intent,repository_observation=repo,observation_policy=policy)
    if result.status!=obs.STATUS_READY or result.receipt is None or result.receipt["codeai_disposition"]!=obs.DISPOSITION_SUPPORTED:
        raise RuntimeError("real v1.101 CodeAI observation refused:"+repr(result.issues))
    return result.receipt


def main() -> int:
    head,branch,tree=require_event()
    source_path=ROOT/TARGET
    original=source_path.read_bytes()
    # A kernel-green promoted blob is recompiled verbatim, never fed back
    # through original-source CodeAI patch generation.
    if git_blob(original) == PROMOTED_BLOB:
        record=source_observation(head,branch,tree,original)
        output=Path("/tmp/kuuos-v1101-codeai-type-probes")
        output.mkdir(parents=True,exist_ok=False)
        with tempfile.TemporaryDirectory(prefix="v1101-promoted-lean-") as td:
            done=subprocess.run([
                "lake","env","lean","-DwarningAsError=true",
                "-Dweak.sorryAsError=true","-o",td+"/promoted.olean",TARGET
            ],cwd=ROOT,capture_output=True,text=True,check=False,timeout=300)
            olean_exists=Path(td+"/promoted.olean").is_file()
        log=done.stdout+"\n"+done.stderr
        (output/"promoted-direct-lean.log").write_text(log,encoding="utf-8")
        row={"source_head":head,"source_tree":tree,
             "original_blob":ORIGINAL_BLOB,"promoted_blob":PROMOTED_BLOB,
             "observation_receipt":record[obs.RECEIPT_DIGEST_FIELD],
             "status":"SUCCESS" if done.returncode==0 and olean_exists else "FAILURE",
             "exit_code":done.returncode,"olean_exists":olean_exists,
             "source_restored":source_path.read_bytes()==original,
             "log_sha256":sha256(log.encode("utf-8")),
             "independent_ci_certified":False}
        (output/"portfolio_receipt.json").write_text(
            json.dumps(row,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        print("KUUOS_V1101_PROMOTED_EXACT_BLOB_DIRECT_LEAN "+
              json.dumps(row,sort_keys=True))
        return 0 if row["status"]=="SUCCESS" and row["source_restored"] else 2
    if git_blob(original)!=ORIGINAL_BLOB:
        raise RuntimeError("v1.101 source blob drift")
    record=source_observation(head,branch,tree,original)
    candidate_source=variants(original.decode("utf-8"))
    statements=lambda s:[
        (x["kind"],x["name_lexical"],x["signature_sha256"])
        for x in declarations_of(s,MODULE)]
    for name,src in candidate_source.items():
        if imports_of(src)!=imports_of(original.decode()):
            raise RuntimeError("changed v1.101 imports:"+name)
        # Only explicit Nat ascriptions (definitionally Nat Hom in the fixed
        # kernel) or exact qualified name/universe corrections are proposed.
        # Any lexical change remains UNADMITTED until the kernel verifies it.
        deltas=[x for x in statements(src) if x not in statements(original.decode())]
        print("KUUOS_V1101_LEXICAL_SIGNATURE_RECHECK "+
              json.dumps({"candidate":name,"changed_declaration_signatures":len(deltas),
                          "kernel_equivalence_required":bool(deltas)},sort_keys=True))
        for forbidden in ("sorry","admit","axiom","unsafe","native_decide"):
            if forbidden in src and forbidden not in original.decode():
                raise RuntimeError("new forbidden content:"+name)
    t=int(time.time())
    template=read_example("codeai_candidate_patch_envelope_v0_1.json")
    policy=deepcopy(template["candidate_policy"])
    policy.update({
        "expected_source_observation_receipt_digest":record[obs.RECEIPT_DIGEST_FIELD],
        "expected_repository_full_name":REPO,
        "expected_source_commit_sha":head,
        "allowed_patch_formats":["unified_diff"],
        "maximum_changed_paths":1,
        "allowed_path_prefixes":["formal/KUOS"],
        "forbidden_path_prefixes":["legacy"],
        "allow_deletions":False,
        "allow_renames":False,
        "allow_binary_patches":False,
        "allow_submodule_patches":False,
        "allow_mode_changes":False,
        "require_requirement_trace":True,
        "require_test_plan":True,
        "allow_evidence_degradation":False,
        "known_risk_labels":["formal-proof"],
        "handover_risk_labels":[],
        "evaluation_epoch":t+30,
        "maximum_candidate_age":3600,
    })
    policy=patch.seal(policy,patch.POLICY_DIGEST_FIELD)
    proposals=[{
        "proposal_id":"v1101-"+name+"-"+head[:10],
        "candidate_revision":"r1",
        "producer_id":"external-structural-Lean4-repair",
        "producer_session_id":"v1101-repair-"+str(i)+"-"+head[:10],
        "candidate_created_epoch":t,
        "edits":[{"path":TARGET,"operation":"modify","new_content":content}],
        "requirement_trace_ids":["v1101:NatHom-universe0-and-Lean-keyword"],
        "test_plan_ids":["v1101:exact-pinned-lake-env-lean"],
        "risk_labels":["formal-proof"],
        "unresolved_candidate_questions":[],
        "prior_candidate_digests":[],
        "prior_producer_session_ids":[],
    } for i,(name,content) in enumerate(candidate_source.items())]
    generated=diff.build_codeai_autonomous_unified_diff_candidates(
        source_observation_receipt=record,repository_files={TARGET:original.decode()},
        proposals=proposals,candidate_policy=policy)
    if generated.status!=diff.STATUS_READY or generated.receipt is None or len(generated.candidates)!=len(proposals):
        raise RuntimeError("CodeAI generation blocked:"+repr(generated.issues))
    output=Path("/tmp/kuuos-v1101-codeai-type-probes")
    if output.exists():
        raise RuntimeError("append-only output path already present")
    output.mkdir(parents=True,exist_ok=False)
    result={"head":head,"source_tree":tree,"original_blob":ORIGINAL_BLOB,
        "observation_receipt":record[obs.RECEIPT_DIGEST_FIELD],
        "portfolio_receipt":generated.receipt[diff.RECEIPT_DIGEST_FIELD],
        "candidates":[],"source_restored":False,"independent_ci_certified":False,
        "kernel_signature_equivalence_pending":True,"git_written":False}
    mode=stat.S_IMODE(source_path.stat().st_mode)
    try:
        for item in generated.candidates:
            expected={("v1101-"+name+"-"+head[:10]):name
                      for name in candidate_source}
            key=expected.get(item.patch_candidate["candidate_id"])
            if key is None:
                raise RuntimeError("CodeAI returned alien/ambiguous candidate ID")
            if item.patch_candidate["changed_paths"] != [TARGET]:
                raise RuntimeError("CodeAI altered candidate changed-path scope")
            updated=candidate_source[key].encode()
            row={"variant":key,"candidate_blob":git_blob(updated),
                 "candidate_sha256":sha256(updated),
                 "candidate_receipt":item.candidate_receipt["codeai_candidate_patch_receipt_digest"],
                 "status":"NOT_RUN"}
            try:
                source_path.write_bytes(updated)
                with tempfile.TemporaryDirectory(prefix="v1101-lean-") as td:
                    try:
                        done=subprocess.run([
                            "lake","env","lean","-DwarningAsError=true",
                            "-Dweak.sorryAsError=true","-o",td+"/probe.olean",TARGET
                        ],cwd=ROOT,capture_output=True,text=True,check=False,timeout=300)
                        outputText=done.stdout+"\n"+done.stderr
                        row["status"]="SUCCESS" if done.returncode==0 else "FAILURE"
                        row["exit_code"]=done.returncode
                        row["olean_exists"]=Path(td+"/probe.olean").is_file()
                    except subprocess.TimeoutExpired as ex:
                        row["status"]="TIMEOUT"
                        outputText=str(ex.stdout or "")+"\n"+str(ex.stderr or "")
                    (output/(key+".log")).write_text(outputText)
                    row["log_sha256"]=sha256(outputText.encode())
                    error_lines=[x for x in outputText.splitlines()
                        if "error:" in x or "error(" in x]
                    row["errors"]=[x[:480] for x in error_lines][:80]
                    row["error_count"]=len(error_lines)
            finally:
                source_path.write_bytes(original)
                source_path.chmod(mode)
                if source_path.read_bytes()!=original:
                    raise RuntimeError("v1.101 original not restored")
            result["candidates"].append(row)
            print("KUUOS_V1101_TYPED_CODEAI_CANDIDATE "+json.dumps(row,ensure_ascii=False,sort_keys=True))
    finally:
        source_path.write_bytes(original)
        source_path.chmod(mode)
        result["source_restored"]=source_path.read_bytes()==original
    (output/"portfolio_receipt.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    passed=[x for x in result["candidates"] if x["status"]=="SUCCESS"]
    print("KUUOS_V1101_TYPED_CODEAI_SUMMARY "+json.dumps({
        "source_head":head,"candidate_count":len(result["candidates"]),
        "strict_direct_success_count":len(passed),"source_restored":result["source_restored"],
        "portfolio_receipt":result["portfolio_receipt"],"independent_ci_certified":False
    },sort_keys=True))
    return 0 if result["source_restored"] else 2


if __name__=="__main__":
    raise SystemExit(main())
