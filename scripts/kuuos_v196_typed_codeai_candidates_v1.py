#!/usr/bin/env python3
"""KuuOS CodeAI exact-HEAD v1.96 type/universe structural repair portfolio.

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
TARGET = "formal/KUOS/DependentOriginationDoubleDeloopingThinComparisonZeroV1_96.lean"
MODULE = "KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96"
ORIGINAL_BLOB = "0c2c9f3599692613ea0c81d61b73e2a2b8d2d102"
PREFIX = "open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95\n"
ZERO_INSTANCE = """local instance instNatOneCellHomOfNatZero (f g : NatOneCell) :
    OfNat (Quiver.Hom.{0} f g) 0 where
  ofNat := (0 : Nat)
"""
HADD_INSTANCE = """local instance instNatOneCellHomHAdd (f g h : NatOneCell) :
    HAdd (Quiver.Hom.{0} f g) (Quiver.Hom.{0} g h)
      (Quiver.Hom.{0} f h) where
  hAdd := Nat.add
"""
EXPLICIT = "    change Nat.add alpha (inv alpha) = 0 at hinv"


def require_event() -> tuple[str,str]:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    if event.get("number") != 3522 or event.get("repository",{}).get("full_name") != REPO:
        raise RuntimeError("exact parent PR event required")
    pr = event["pull_request"]
    source_head = pr["head"]["sha"]
    branch = pr["head"]["ref"]
    url = "https://api.github.com/repos/"+REPO+"/git/commits/"+source_head
    req = urllib.request.Request(url, headers={"Accept":"application/vnd.github+json","User-Agent":"KuuOS-CodeAI-v196"})
    with urllib.request.urlopen(req,timeout=30) as response:
        data = json.load(response)
    tree = data.get("tree",{}).get("sha")
    if data.get("sha") != source_head or not isinstance(tree,str) or not re.fullmatch("[a-f0-9]{40}",tree):
        raise RuntimeError("exact GitHub source/tree unverified")
    return source_head,branch,tree


def variants(source: str) -> dict[str,str]:
    if source.count(PREFIX) != 1:
        raise RuntimeError("unexpected original v1.96 namespace")
    rename = source.replace("hλ","hLeftUnitor").replace("hρ","hRightUnitor")
    if rename == source or "have hλ" in rename:
        raise RuntimeError("syntax rename source drift")
    # The pinned kernel has established by rfl that every 2-cell Hom is Nat,
    # but OfNat class synthesis on dependent Quiver.Hom still fails. Encode Nat
    # first, then rely on definitional type equality. This does not discharge
    # proof statements; full Lean must verify all elaborated theorem types.
    code_lines = rename.splitlines(keepends=True)
    allowed = [51,56,68,83,97,99,101,114,116,118,135,171,174,180,188,200,204]
    for line in allowed:
        if code_lines[line-1].count("= 0") != 1:
            raise RuntimeError("typed Nat zero source anchor drift line "+str(line))
        code_lines[line-1] = code_lines[line-1].replace("= 0","= (0 : Nat)",1)
    typed = "".join(code_lines)
    h0a = "(0 : (sigma.map (𝟙 a)) ⟶ 𝟙 (sigma.obj a))"
    h0b = "(0 : (sigma.map (𝟙 b)) ⟶ 𝟙 (sigma.obj b))"
    if typed.count(h0a)!=1 or typed.count(h0b)!=1:
        raise RuntimeError("typed auxiliary 2-cell source anchor drift")
    typed = typed.replace(h0a,"(0 : Nat)").replace(h0b,"(0 : Nat)")
    typed_add = typed.replace(
        "change alpha + inv alpha = (0 : Nat) at hinv",
        "change Nat.add alpha (inv alpha) = (0 : Nat) at hinv",
    )
    if typed_add==typed:
        raise RuntimeError("Nat.add arithmetic source anchor drift")
    final = typed_add.replace(
        "KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83.canonicalKuuOSPresentation",
        "KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81.canonicalKuuOSPresentation",
    ).replace(
        "KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83.standardABCPresentation",
        "KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81.standardABCPresentation",
    )
    if final==typed_add:
        raise RuntimeError("qualified declaration names not found")
    final = final.replace(
        "¬ KUOS.DependentOriginationStandardArbitraryScalingWaypointV1_89.StandardArbitraryScalingObstructionClosed :=",
        "¬ KUOS.DependentOriginationStandardArbitraryScalingWaypointV1_89.StandardArbitraryScalingObstructionClosed.{0} :=",
    )
    # Use the exact pinned Nat kernel API instead of omega on an abstract
    # Quiver Hom (which is *definitionally* Nat, but is not recognized by omega).
    arith_before = """    change Nat.add alpha (inv alpha) = (0 : Nat) at hinv
    omega"""
    arith_after = """    change Nat.add alpha (inv alpha) = (0 : Nat) at hinv
    exact (Nat.eq_zero_of_add_eq_zero hinv).1"""
    if typed_add.count(arith_before)!=1:
        raise RuntimeError("pinned Nat.eq_zero_of_add_eq_zero anchor drift")
    lemma = typed_add.replace(arith_before,arith_after)

    # Avoid `rw` on a metavariable under eqToHom. Supply the exact
    # strictly unitary functor's map_id proof directly as a typed argument.
    proof = lemma
    for obj in ("a","b"):
        h = "eqToHom (by rw [sigma.map_id "+obj+"])"
        if proof.count(h)!=1:
            raise RuntimeError("map_id typed EqToHom source drift: "+obj)
        proof=proof.replace(h,"eqToHom (sigma.map_id "+obj+")")

    # LocallyDiscrete has a Discrete wrapper on source 1-morphisms.
    # It is not generally a Subsingleton without unfolding that wrapper.
    discrete=proof
    for obj,morph in (("a","f"),("b","g")):
        old="have h"+morph+" : "+morph+" = 𝟙 "+obj+" := Subsingleton.elim _ _"
        new="""have h"""+morph+" : "+morph+" = 𝟙 "+obj+""" := by
      apply Discrete.ext
      exact Subsingleton.elim _ _"""
        if discrete.count(old)!=1:
            raise RuntimeError("locally discrete Hom equality drift: "+obj)
        discrete=discrete.replace(old,new)

    # The two original omega goals are comparisons of the literal
    # comparison label 1 with Nat.zero. State the Nat goal explicitly.
    rest=discrete
    nondeg="""  rw [natNoninvertibleTriangle_comparison] at hzero
  omega"""
    nondeg_after="""  rw [natNoninvertibleTriangle_comparison] at hzero
  change (1 : Nat) = 0 at hzero
  exact Nat.one_ne_zero hzero"""
    if rest.count(nondeg)!=1: raise RuntimeError("nondegenerate proof source drift")
    rest=rest.replace(nondeg,nondeg_after)
    thin="""  rw [natDuskin_thin_iff_comparison_eq_zero,
    natNoninvertibleTriangle_comparison]
  omega"""
    thin_after="""  rw [natDuskin_thin_iff_comparison_eq_zero,
    natNoninvertibleTriangle_comparison]
  change (1 : Nat) ≠ 0
  exact Nat.one_ne_zero"""
    if rest.count(thin)!=1: raise RuntimeError("not-thin proof source drift")
    rest=rest.replace(thin,thin_after)

    # The final named endpoints actually live in v1.81, and the v1.95
    # exact theorem fixes the universe at 0. Fix only that referent.
    full=rest.replace(
        "KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83.canonicalKuuOSPresentation",
        "KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81.canonicalKuuOSPresentation",
    ).replace(
        "KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83.standardABCPresentation",
        "KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81.standardABCPresentation",
    ).replace(
        "StandardArbitraryScalingObstructionClosed :=",
        "StandardArbitraryScalingObstructionClosed.{0} :=",
    )
    if full == rest: raise RuntimeError("original v1.96 final declarations did not match")

    # StrictlyUnitaryLaxFunctor.mapId_isIso is present at the pinned mathlib
    # SHA. The actual map₂_leftUnitor goal contains `sigma.mapId a`, NOT
    # `eqToHom (sigma.map_id a)`. Their directions differ. Rewrite the term
    # genuinely occurring in the goal, retaining its IsIso certificate.
    mapid=full
    for obj,label in (("a","Left"),("b","Right")):
        old=("  have heq : eqToHom (sigma.map_id "+obj+") =\\n"+
             "      (0 : Nat) :=\\n"+
             "    NatDoubleDelooping.isIso_twoCell_eq_zero _\\n"+
             "  rw [hmap₂, h"+label+"Unitor, heq] at h")
        replacement=("  have hmapId : sigma.mapId "+obj+" = (0 : Nat) :=\\n"+
                     "    NatDoubleDelooping.isIso_twoCell_eq_zero _\\n"+
                     "  rw [hmap₂, h"+label+"Unitor, hmapId] at h")
        # Use actual newlines, not escaped \\n in string matching.
        old=old.replace(chr(92)+"n",chr(10))
        replacement=replacement.replace(chr(92)+"n",chr(10))
        if mapid.count(old)!=1:
            raise RuntimeError("v1.96 strict mapId goal source drift: "+obj)
        mapid=mapid.replace(old,replacement)
    # Avoid an unassigned polymorphic `u_1` in the original malformed last
    # endpoint theorem; the imported v1.95 conclusion is at universe 0.
    universe=mapid
    for name in ("canonicalKuuOSPresentation","standardABCPresentation"):
        occurrence=("DependentOriginationGeneratedPresentationQuotientInvariantV1_81."+name)
        if universe.count(occurrence)!=1:
            raise RuntimeError("presentation endpoint source drift: "+name)
        universe=universe.replace(occurrence,occurrence+".{0}")
    # Research-only: expression annotations affect lexical signatures but are
    # mathematically definitionally Nat (proven by `rfl` on exact Hom types).
    # Full Lean+Lean MCP and independent CI remain mandatory before adoption.
    return {
        "round5-mapId-isIso-zero":mapid,
        "round5-mapId-isIso-zero-universe0":universe,
    }


def read_example(filename: str) -> dict:
    return json.loads((ROOT/"examples"/filename).read_text(encoding="utf-8"))


def source_observation(head: str,branch: str,tree: str,source:bytes) -> dict:
    sample = read_example("codeai_intent_repository_observation_envelope_v0_1.json")
    t = int(time.time())
    intent = deepcopy(sample["intent_packet"])
    intent.update({
        "intent_id":"kuuos-v196-typed-zero-"+head[:12],
        "source_actor_id":"codeai-proof-research",
        "source_channel":"github-parent-strict-lean-log",
        "requirements":["repair v1.96 typed Nat 2-cells and syntax without changing theorem statements"],
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
    paths=[TARGET,"formal/KUOS/DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95.lean",
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
        "baseline_check_digests":["v196-exact-blob:"+ORIGINAL_BLOB,"import-v195:"+git_blob((ROOT/paths[1]).read_bytes())],
        "baseline_checks_complete":True,
        "code_owner_scope_digest":"repo-owner:"+REPO,
        "crosses_unowned_boundary":False,
        "observation_started_epoch":t,
        "observation_completed_epoch":int(time.time()),
        "session_id":"v196-"+head[:16],
        "nonce_digest":hashlib.sha256((head+":v196-actual").encode()).hexdigest(),
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
        raise RuntimeError("real v1.96 CodeAI observation refused:"+repr(result.issues))
    return result.receipt


def main() -> int:
    head,branch,tree=require_event()
    source_path=ROOT/TARGET
    original=source_path.read_bytes()
    if git_blob(original)!=ORIGINAL_BLOB:
        raise RuntimeError("v1.96 source blob drift")
    record=source_observation(head,branch,tree,original)
    candidate_source=variants(original.decode("utf-8"))
    statements=lambda s:[
        (x["kind"],x["name_lexical"],x["signature_sha256"])
        for x in declarations_of(s,MODULE)]
    for name,src in candidate_source.items():
        if imports_of(src)!=imports_of(original.decode()):
            raise RuntimeError("changed v1.96 imports:"+name)
        # Only explicit Nat ascriptions (definitionally Nat Hom in the fixed
        # kernel) or exact qualified name/universe corrections are proposed.
        # Any lexical change remains UNADMITTED until the kernel verifies it.
        deltas=[x for x in statements(src) if x not in statements(original.decode())]
        print("KUUOS_V196_LEXICAL_SIGNATURE_RECHECK "+
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
        "proposal_id":"v196-"+name+"-"+head[:10],
        "candidate_revision":"r1",
        "producer_id":"external-structural-Lean4-repair",
        "producer_session_id":"v196-repair-"+str(i)+"-"+head[:10],
        "candidate_created_epoch":t,
        "edits":[{"path":TARGET,"operation":"modify","new_content":content}],
        "requirement_trace_ids":["v196:NatHom-universe0-and-Lean-keyword"],
        "test_plan_ids":["v196:exact-pinned-lake-env-lean"],
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
    output=Path("/tmp/kuuos-v196-codeai-type-probes")
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
            expected={("v196-"+name+"-"+head[:10]):name
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
                with tempfile.TemporaryDirectory(prefix="v196-lean-") as td:
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
                    raise RuntimeError("v1.96 original not restored")
            result["candidates"].append(row)
            print("KUUOS_V196_TYPED_CODEAI_CANDIDATE "+json.dumps(row,ensure_ascii=False,sort_keys=True))
    finally:
        source_path.write_bytes(original)
        source_path.chmod(mode)
        result["source_restored"]=source_path.read_bytes()==original
    (output/"portfolio_receipt.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    passed=[x for x in result["candidates"] if x["status"]=="SUCCESS"]
    print("KUUOS_V196_TYPED_CODEAI_SUMMARY "+json.dumps({
        "source_head":head,"candidate_count":len(result["candidates"]),
        "strict_direct_success_count":len(passed),"source_restored":result["source_restored"],
        "portfolio_receipt":result["portfolio_receipt"],"independent_ci_certified":False
    },sort_keys=True))
    return 0 if result["source_restored"] else 2


if __name__=="__main__":
    raise SystemExit(main())
